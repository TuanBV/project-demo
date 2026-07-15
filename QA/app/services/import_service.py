"""QuestionImportService: the only place import DTOs turn into database writes.

dry_run short-circuits before any write. Real imports run inside one transaction per
job; duplicate_strategy resolves content_hash clashes (SKIP/UPDATE/CREATE_COPY). Used
identically by the API routes and the CLI scripts (spec section 27).

Default output is a MULTIPLE_CHOICE question (spec sections 9-10):
- explicit 4-option sources (A/B/C/D or OPTION/CORRECT_OPTION) become an active question
  immediately -- the validator already confirmed exactly 4 distinct options + 1 correct.
- question+correct-answer-only sources (narrative PHẦN/Câu/Trả lời or CATEGORY/QUESTION/
  ANSWER) get 3 auto-generated distractors and are always created with
  needs_review=True, active=False so an admin must review before they reach learners.

The legacy concept/keyword rubric builder (_build_concepts/_attach_rubric) is kept,
unused by this default path, for FREE_TEXT imports (ImportOptions.default_question_format
explicitly set to "FREE_TEXT").
"""

from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import asdict
from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.core.hashing import compute_content_hash
from app.db.models.category import Category
from app.db.models.enums import (
    Difficulty,
    ImportItemStatus,
    ImportStatus,
    LanguageScope,
    MatchType,
    QuestionFormat,
    QuestionType,
)
from app.db.models.evaluation import AnswerConcept, ConceptKeyword, ContradictionRule
from app.db.models.import_job import ImportItem, ImportJob
from app.db.models.question import Question
from app.evaluation.normalizer import strip_diacritics
from app.importers.concept_suggester import ConceptSuggestionService
from app.importers.distractor_generator import DistractorGenerator, RuleBasedDistractorGenerator
from app.importers.dto import (
    ImportOptions,
    ImportResult,
    ImportResultItem,
    ImportSummaryData,
    ParsedQuestion,
    SuggestedConcept,
    ValidatedImportDocument,
    ValidatedQuestionItem,
)
from app.repositories.category_repository import CategoryRepository
from app.repositories.import_repository import ImportRepository
from app.repositories.question_repository import QuestionRepository
from app.services.question_option_service import OptionInput, QuestionOptionService
from app.services.slug import slugify

_DEFAULT_KEYWORD_SIMILARITY = 80.0
_DEFAULT_CONTRADICTION_PENALTY = 20.0
_DEFAULT_CONTRADICTION_SIMILARITY = 85.0
_MAX_SIBLING_CONTEXT = 10


class QuestionImportService:
    def __init__(
        self,
        db: Session,
        question_repository: QuestionRepository,
        category_repository: CategoryRepository,
        import_repository: ImportRepository,
        concept_suggester: ConceptSuggestionService | None = None,
        option_service: QuestionOptionService | None = None,
        distractor_generator: DistractorGenerator | None = None,
    ) -> None:
        self._db = db
        self._questions = question_repository
        self._categories = category_repository
        self._imports = import_repository
        self._suggester = concept_suggester or ConceptSuggestionService()
        self._options = option_service or QuestionOptionService()
        self._distractor_generator = distractor_generator or RuleBasedDistractorGenerator()

    def list_jobs(self, page: int = 1, page_size: int = 20) -> tuple[list[ImportJob], int]:
        return self._imports.list_jobs(page, page_size)

    def get_job(self, job_id: int) -> ImportJob | None:
        return self._imports.get(job_id)

    def import_document(
        self, validated: ValidatedImportDocument, options: ImportOptions
    ) -> ImportResult:
        summary = self._build_summary(validated)
        sibling_answers = self._build_sibling_answer_map(validated, options)

        if options.dry_run:
            items = [
                ImportResultItem(
                    source_order=item.parsed.source_order,
                    category=item.parsed.category_name or options.default_category,
                    question_type=item.parsed.question_type,
                    question=item.parsed.content,
                    answer=item.parsed.reference_answer,
                    status=item.status,
                    warnings=item.warnings,
                    errors=item.errors,
                )
                for item in validated.items
            ]
            return ImportResult(
                dry_run=True,
                job_id=None,
                summary=summary,
                items=items,
                unparsed_segments=validated.unparsed_segments,
            )

        job = ImportJob(
            source_type=options.source_type,
            source_name=options.source_name,
            status=ImportStatus.PARSING,
            dry_run=False,
            duplicate_strategy=options.duplicate_strategy,
        )
        job = self._imports.add(job)

        result_items: list[ImportResultItem] = []
        try:
            for item in validated.items:
                result_items.append(self._import_one(job, item, options, summary, sibling_answers))
            summary.questions_needs_review = sum(
                1 for i in result_items if i.status == "NEEDS_REVIEW"
            )

            job.status = ImportStatus.COMPLETED
            job.completed_at = datetime.now(UTC)
            job.summary_json = json.dumps(asdict(summary))
            self._db.commit()
        except Exception:
            self._db.rollback()
            raise

        return ImportResult(
            dry_run=False,
            job_id=job.id,
            summary=summary,
            items=result_items,
            unparsed_segments=validated.unparsed_segments,
        )

    @staticmethod
    def _build_sibling_answer_map(
        validated: ValidatedImportDocument, options: ImportOptions
    ) -> dict[str, list[str]]:
        by_category: dict[str, list[str]] = defaultdict(list)
        for item in validated.items:
            if item.status == "ERROR" or not item.parsed.reference_answer:
                continue
            category = (item.parsed.category_name or options.default_category or "").strip()
            by_category[category].append(item.parsed.reference_answer)
        return by_category

    def _import_one(
        self,
        job: ImportJob,
        item: ValidatedQuestionItem,
        options: ImportOptions,
        summary: ImportSummaryData,
        sibling_answers: dict[str, list[str]],
    ) -> ImportResultItem:
        parsed = item.parsed

        if item.status == "ERROR":
            self._imports.add_item(
                ImportItem(
                    import_job_id=job.id,
                    source_order=parsed.source_order,
                    raw_content=parsed.raw_content,
                    status=ImportItemStatus.ERROR,
                    warnings_json=json.dumps(item.warnings) if item.warnings else None,
                    errors_json=json.dumps(item.errors) if item.errors else None,
                )
            )
            return ImportResultItem(
                source_order=parsed.source_order,
                category=parsed.category_name or options.default_category,
                question_type=parsed.question_type,
                question=parsed.content,
                answer=parsed.reference_answer,
                status="ERROR",
                warnings=item.warnings,
                errors=item.errors,
            )

        category_name = (parsed.category_name or options.default_category or "").strip()
        if not category_name:
            self._imports.add_item(
                ImportItem(
                    import_job_id=job.id,
                    source_order=parsed.source_order,
                    raw_content=parsed.raw_content,
                    status=ImportItemStatus.ERROR,
                    errors_json=json.dumps(["Không xác định được category"]),
                )
            )
            return ImportResultItem(
                source_order=parsed.source_order,
                category=None,
                question_type=parsed.question_type,
                question=parsed.content,
                answer=parsed.reference_answer,
                status="ERROR",
                errors=["Không xác định được category"],
            )

        category = self._categories.get_by_name(category_name)
        if category is None:
            category = Category(name=category_name, slug=slugify(category_name))
            category = self._categories.add(category)
            summary.categories_created += 1

        question_type = QuestionType(parsed.question_type)
        content_hash = compute_content_hash(category.name, parsed.content, question_type.value)
        existing = self._questions.get_by_content_hash(content_hash)

        question_format = QuestionFormat(options.default_question_format)
        mc_options: list[OptionInput] = []
        needs_review = False
        if question_format == QuestionFormat.MULTIPLE_CHOICE:
            mc_options, needs_review = self._build_mc_options(
                parsed, category_name, sibling_answers
            )

        if existing is None:
            question = self._new_question(
                category.id,
                parsed,
                question_type,
                content_hash,
                options.source_type,
                question_format,
                needs_review,
            )
            if question_format == QuestionFormat.MULTIPLE_CHOICE:
                self._options.replace_options(question, mc_options)
            else:
                concepts, auto_generated = self._build_concepts(parsed, options)
                self._attach_rubric(question, concepts, auto_generated, parsed.contradictions)
            question = self._questions.add(question)
            summary.questions_created += 1
            status = "CREATED"
        else:
            status, question = self._resolve_duplicate(
                existing,
                parsed,
                question_type,
                category.id,
                mc_options,
                needs_review,
                question_format,
                options,
                summary,
            )

        self._imports.add_item(
            ImportItem(
                import_job_id=job.id,
                source_order=parsed.source_order,
                raw_content=parsed.raw_content,
                status=ImportItemStatus[status],
                question_id=question.id,
                warnings_json=json.dumps(item.warnings) if item.warnings else None,
            )
        )
        result_status = "NEEDS_REVIEW" if needs_review and status == "CREATED" else status
        return ImportResultItem(
            source_order=parsed.source_order,
            category=category.name,
            question_type=parsed.question_type,
            question=parsed.content,
            answer=parsed.reference_answer,
            status=result_status,
            warnings=item.warnings,
            errors=item.errors,
            question_id=question.id,
        )

    def _build_mc_options(
        self,
        parsed: ParsedQuestion,
        category_name: str,
        sibling_answers: dict[str, list[str]],
    ) -> tuple[list[OptionInput], bool]:
        if parsed.options and parsed.correct_option_index is not None:
            return (
                [
                    OptionInput(content=text, is_correct=(i == parsed.correct_option_index))
                    for i, text in enumerate(parsed.options)
                ],
                False,
            )

        correct_answer = parsed.reference_answer or ""
        context = [a for a in sibling_answers.get(category_name, []) if a != correct_answer][
            :_MAX_SIBLING_CONTEXT
        ]
        distractors = self._distractor_generator.generate(
            parsed.content, correct_answer, context, count=3
        )
        built = [OptionInput(content=correct_answer, is_correct=True)]
        built.extend(
            OptionInput(content=d, is_correct=False, auto_generated=True) for d in distractors
        )
        return built, True

    def _resolve_duplicate(
        self,
        existing: Question,
        parsed: ParsedQuestion,
        question_type: QuestionType,
        category_id: int,
        mc_options: list[OptionInput],
        needs_review: bool,
        question_format: QuestionFormat,
        options: ImportOptions,
        summary: ImportSummaryData,
    ) -> tuple[str, Question]:
        strategy = options.duplicate_strategy
        if strategy == "UPDATE":
            existing.reference_answer = parsed.reference_answer
            existing.explanation = parsed.explanation
            existing.java_answer = parsed.java_answer
            existing.python_answer = parsed.python_answer
            existing.sql_answer = parsed.sql_answer
            existing.difficulty = Difficulty(parsed.difficulty)
            existing.language_scope = LanguageScope(parsed.language_scope)
            existing.question_format = question_format
            if question_format == QuestionFormat.MULTIPLE_CHOICE:
                existing.needs_review = needs_review
                existing.active = existing.active and not needs_review
                self._options.replace_options(existing, mc_options)
            else:
                concepts, auto_generated = self._build_concepts(parsed, options)
                self._attach_rubric(
                    existing, concepts, auto_generated, parsed.contradictions, replace=True
                )
            summary.questions_updated += 1
            return "UPDATED", existing
        if strategy == "CREATE_COPY":
            content_hash = compute_content_hash(
                str(category_id), f"{parsed.content}#{parsed.source_order}", question_type.value
            )
            question = self._new_question(
                category_id,
                parsed,
                question_type,
                content_hash,
                options.source_type,
                question_format,
                needs_review,
            )
            if question_format == QuestionFormat.MULTIPLE_CHOICE:
                self._options.replace_options(question, mc_options)
            else:
                concepts, auto_generated = self._build_concepts(parsed, options)
                self._attach_rubric(question, concepts, auto_generated, parsed.contradictions)
            question = self._questions.add(question)
            summary.questions_created += 1
            return "CREATED", question
        summary.questions_skipped += 1
        return "SKIPPED", existing

    @staticmethod
    def _new_question(
        category_id: int,
        parsed: ParsedQuestion,
        question_type: QuestionType,
        content_hash: str,
        source_type: str,
        question_format: QuestionFormat,
        needs_review: bool,
    ) -> Question:
        return Question(
            category_id=category_id,
            question_type=question_type,
            question_format=question_format,
            content=parsed.content,
            reference_answer=parsed.reference_answer,
            explanation=parsed.explanation,
            difficulty=Difficulty(parsed.difficulty),
            language_scope=LanguageScope(parsed.language_scope),
            java_answer=parsed.java_answer,
            python_answer=parsed.python_answer,
            sql_answer=parsed.sql_answer,
            content_hash=content_hash,
            active=not needs_review,
            needs_review=needs_review,
            source_type=source_type,
            source_order=parsed.source_order,
        )

    def _build_concepts(
        self, parsed: ParsedQuestion, options: ImportOptions
    ) -> tuple[list[SuggestedConcept], bool]:
        """Legacy FREE_TEXT rubric builder -- unused by the default MC import path."""
        if parsed.required_keywords or parsed.optional_keywords:
            concepts: list[SuggestedConcept] = []
            has_both = bool(parsed.required_keywords) and bool(parsed.optional_keywords)
            if parsed.required_keywords:
                concepts.append(
                    SuggestedConcept(
                        name="required",
                        description="Các ý bắt buộc",
                        weight=70.0 if has_both else 100.0,
                        required=True,
                        keywords=parsed.required_keywords,
                    )
                )
            if parsed.optional_keywords:
                concepts.append(
                    SuggestedConcept(
                        name="optional",
                        description="Các ý bổ sung",
                        weight=30.0 if has_both else 100.0,
                        required=False,
                        keywords=parsed.optional_keywords,
                    )
                )
            return concepts, False

        if parsed.keywords:
            return [
                SuggestedConcept(
                    name="noi_dung_chinh",
                    description=parsed.content[:100],
                    weight=100.0,
                    required=True,
                    keywords=parsed.keywords,
                )
            ], False

        if options.generate_concepts and parsed.reference_answer:
            return self._suggester.suggest(parsed.content, parsed.reference_answer), True

        return [], False

    @staticmethod
    def _attach_rubric(
        question: Question,
        concepts: list[SuggestedConcept],
        auto_generated: bool,
        contradictions: list[str],
        replace: bool = False,
    ) -> None:
        """Legacy FREE_TEXT rubric attacher -- unused by the default MC import path."""
        if replace:
            question.concepts.clear()
            question.contradiction_rules.clear()

        for order, concept in enumerate(concepts):
            answer_concept = AnswerConcept(
                name=concept.name,
                description=concept.description,
                weight=concept.weight,
                required=concept.required,
                auto_generated=auto_generated,
                display_order=order,
            )
            for keyword in concept.keywords:
                answer_concept.keywords.append(
                    ConceptKeyword(
                        keyword=keyword,
                        normalized_keyword=strip_diacritics(keyword).lower().strip(),
                        match_type=MatchType.CONTAINS,
                        minimum_similarity=_DEFAULT_KEYWORD_SIMILARITY,
                        auto_generated=auto_generated,
                        active=True,
                    )
                )
            question.concepts.append(answer_concept)

        should_add_contradictions = replace or (contradictions and not question.contradiction_rules)
        if should_add_contradictions:
            for phrase in contradictions:
                question.contradiction_rules.append(
                    ContradictionRule(
                        pattern=phrase,
                        description=phrase,
                        penalty=_DEFAULT_CONTRADICTION_PENALTY,
                        maximum_score=None,
                        match_type=MatchType.CONTAINS,
                        minimum_similarity=_DEFAULT_CONTRADICTION_SIMILARITY,
                        active=True,
                    )
                )

    @staticmethod
    def _build_summary(validated: ValidatedImportDocument) -> ImportSummaryData:
        categories = {
            (item.parsed.category_name or "").strip().lower()
            for item in validated.items
            if item.parsed.category_name
        }
        return ImportSummaryData(
            categories_detected=len(categories),
            questions_detected=len(validated.items),
            valid_questions=sum(1 for i in validated.items if i.status != "ERROR"),
            warning_count=sum(1 for i in validated.items if i.warnings),
            error_count=sum(1 for i in validated.items if i.status == "ERROR"),
        )
