"""QuestionService: admin question CRUD, concept/keyword/contradiction management,
option management, and rubric/distractor suggestion. Business logic only; DB access goes
through repositories.
"""

from __future__ import annotations

from app.core.exceptions import NotFoundError, ValidationFailedError
from app.core.hashing import compute_content_hash
from app.db.models.enums import QuestionFormat
from app.db.models.evaluation import AnswerConcept, ConceptKeyword, ContradictionRule
from app.db.models.question import Question
from app.evaluation.normalizer import strip_diacritics
from app.importers.concept_suggester import ConceptSuggestionService
from app.importers.distractor_generator import (
    DistractorGenerator,
    RuleBasedDistractorGenerator,
    is_placeholder_distractor,
)
from app.importers.distractor_quality_validator import DistractorQualityValidator
from app.repositories.category_repository import CategoryRepository
from app.repositories.question_repository import QuestionRepository
from app.schemas.question import (
    AdminQuestionCreate,
    AdminQuestionUpdate,
    GenerateDistractorsRequest,
    GenerateDistractorsResponse,
    QuestionOptionCreate,
    SuggestedConcept,
    SuggestRubricRequest,
    ValidateQuestionResponse,
)
from app.services.question_option_service import OptionInput, QuestionOptionService


class QuestionService:
    def __init__(
        self,
        question_repository: QuestionRepository,
        category_repository: CategoryRepository,
        concept_suggester: ConceptSuggestionService | None = None,
        option_service: QuestionOptionService | None = None,
        distractor_generator: DistractorGenerator | None = None,
        quality_validator: DistractorQualityValidator | None = None,
    ) -> None:
        self._questions = question_repository
        self._categories = category_repository
        self._suggester = concept_suggester or ConceptSuggestionService()
        self._options = option_service or QuestionOptionService()
        self._distractor_generator = distractor_generator or RuleBasedDistractorGenerator()
        self._quality_validator = quality_validator or DistractorQualityValidator()

    def get(self, question_id: int) -> Question:
        question = self._questions.get_with_rubric(question_id)
        if question is None:
            raise NotFoundError(f"Question {question_id} not found")
        return question

    def list_filtered(self, **kwargs: object) -> tuple[list[Question], int]:
        return self._questions.list_filtered(**kwargs)  # type: ignore[arg-type]

    def create(self, data: AdminQuestionCreate, source_type: str = "MANUAL") -> Question:
        category_id = self._resolve_category(data.category_id, data.category_name)
        content_hash = compute_content_hash(
            self._category_name(category_id), data.content, data.question_type.value
        )
        question = Question(
            category_id=category_id,
            question_type=data.question_type,
            question_format=data.question_format,
            content=data.content,
            reference_answer=data.reference_answer,
            explanation=data.explanation,
            difficulty=data.difficulty,
            language_scope=data.language_scope,
            java_answer=data.java_answer,
            python_answer=data.python_answer,
            sql_answer=data.sql_answer,
            content_hash=content_hash,
            active=data.active,
            needs_review=data.needs_review,
            source_type=source_type,
            minimum_answer_length=data.minimum_answer_length,
            minimum_token_count=data.minimum_token_count,
        )
        if data.question_format == QuestionFormat.MULTIPLE_CHOICE:
            self._options.replace_options(question, self._to_option_inputs(data.options))
        self._apply_rubric(question, data.concepts, data.contradiction_rules)
        question = self._questions.add(question)
        self._questions.commit()
        return self.get(question.id)

    def update(self, question_id: int, data: AdminQuestionUpdate) -> Question:
        question = self.get(question_id)

        if data.category_id is not None:
            question.category_id = data.category_id
        if data.question_type is not None:
            question.question_type = data.question_type
        if data.question_format is not None:
            question.question_format = data.question_format
        if data.content is not None:
            question.content = data.content
        if data.reference_answer is not None:
            question.reference_answer = data.reference_answer
        if data.explanation is not None:
            question.explanation = data.explanation
        if data.difficulty is not None:
            question.difficulty = data.difficulty
        if data.language_scope is not None:
            question.language_scope = data.language_scope
        if data.java_answer is not None:
            question.java_answer = data.java_answer
        if data.python_answer is not None:
            question.python_answer = data.python_answer
        if data.sql_answer is not None:
            question.sql_answer = data.sql_answer
        if data.active is not None:
            question.active = data.active
        if data.needs_review is not None:
            question.needs_review = data.needs_review
        if data.minimum_answer_length is not None:
            question.minimum_answer_length = data.minimum_answer_length
        if data.minimum_token_count is not None:
            question.minimum_token_count = data.minimum_token_count

        question.content_hash = compute_content_hash(
            self._category_name(question.category_id),
            question.content,
            question.question_type.value,
        )

        if data.options is not None:
            self._options.replace_options(question, self._to_option_inputs(data.options))

        if data.concepts is not None or data.contradiction_rules is not None:
            self._apply_rubric(
                question,
                data.concepts if data.concepts is not None else [],
                data.contradiction_rules if data.contradiction_rules is not None else [],
                replace=True,
            )

        self._questions.commit()
        return self.get(question_id)

    def delete(self, question_id: int) -> None:
        question = self.get(question_id)
        self._questions.delete(question)
        self._questions.commit()

    def duplicate(self, question_id: int) -> Question:
        source = self.get(question_id)
        content_hash = compute_content_hash(
            self._category_name(source.category_id),
            f"{source.content} (copy)",
            source.question_type.value,
        )
        clone = Question(
            category_id=source.category_id,
            question_type=source.question_type,
            question_format=source.question_format,
            content=f"{source.content} (copy)",
            reference_answer=source.reference_answer,
            explanation=source.explanation,
            difficulty=source.difficulty,
            language_scope=source.language_scope,
            java_answer=source.java_answer,
            python_answer=source.python_answer,
            sql_answer=source.sql_answer,
            content_hash=content_hash,
            active=False,
            needs_review=source.needs_review,
            source_type=source.source_type,
            minimum_answer_length=source.minimum_answer_length,
            minimum_token_count=source.minimum_token_count,
        )
        if source.question_format == QuestionFormat.MULTIPLE_CHOICE and source.options:
            options = [
                OptionInput(
                    content=o.content,
                    is_correct=o.is_correct,
                    explanation=o.explanation,
                    auto_generated=False,
                )
                for o in sorted(source.options, key=lambda x: x.display_order)
            ]
            self._options.replace_options(clone, options)
        clone = self._questions.add(clone)
        self._questions.commit()
        return self.get(clone.id)

    def generate_distractors(
        self, request: GenerateDistractorsRequest
    ) -> GenerateDistractorsResponse:
        distractors = self._distractor_generator.generate(
            request.question, request.correct_answer, request.context, request.count
        )
        has_placeholder = any(is_placeholder_distractor(d) for d in distractors)
        warnings = self._quality_validator.validate(request.correct_answer, distractors)
        return GenerateDistractorsResponse(
            distractors=distractors, warnings=warnings, has_placeholder=has_placeholder
        )

    def regenerate_distractors(
        self, question_id: int, context: list[str] | None = None
    ) -> Question:
        question = self.get(question_id)
        correct = next((o for o in question.options if o.is_correct), None)
        if correct is None:
            raise ValidationFailedError("Câu hỏi chưa có đáp án đúng để tạo lại đáp án sai")

        distractors = self._distractor_generator.generate(
            question.content, correct.content, context, count=3
        )
        options = [
            OptionInput(content=correct.content, is_correct=True, explanation=correct.explanation)
        ]
        for text in distractors:
            options.append(OptionInput(content=text, is_correct=False, auto_generated=True))
        self._options.replace_options(question, options)
        question.needs_review = any(is_placeholder_distractor(d) for d in distractors)
        self._questions.commit()
        return self.get(question_id)

    def validate_question(self, question_id: int) -> ValidateQuestionResponse:
        question = self.get(question_id)
        errors: list[str] = []
        warnings: list[str] = []

        if question.question_format == QuestionFormat.MULTIPLE_CHOICE:
            active_options = [o for o in question.options if o.active]
            if len(active_options) != 4:
                errors.append(f"Cần đúng 4 đáp án active, hiện có {len(active_options)}")
            correct = [o for o in active_options if o.is_correct]
            if len(correct) != 1:
                errors.append(f"Cần đúng 1 đáp án đúng, hiện có {len(correct)}")
            if correct and len(active_options) == 4:
                wrong = [o.content for o in active_options if not o.is_correct]
                warnings.extend(self._quality_validator.validate(correct[0].content, wrong))

        if question.needs_review:
            warnings.append("Câu hỏi đang ở trạng thái cần review (needs_review=true)")

        if errors:
            status = "INVALID"
        elif warnings:
            status = "NEEDS_REVIEW"
        else:
            status = "VALID"
        return ValidateQuestionResponse(status=status, errors=errors, warnings=warnings)

    def suggest_rubric(self, request: SuggestRubricRequest) -> list[SuggestedConcept]:
        suggestions = self._suggester.suggest(request.question, request.reference_answer)
        return [
            SuggestedConcept(
                name=s.name,
                description=s.description,
                weight=s.weight,
                required=s.required,
                keywords=s.keywords,
            )
            for s in suggestions
        ]

    @staticmethod
    def _to_option_inputs(options: list[QuestionOptionCreate]) -> list[OptionInput]:
        return [
            OptionInput(
                content=o.content,
                is_correct=o.is_correct,
                explanation=o.explanation,
                auto_generated=o.auto_generated,
            )
            for o in options
        ]

    def _apply_rubric(
        self,
        question: Question,
        concepts: list,
        contradiction_rules: list,
        replace: bool = False,
    ) -> None:
        if replace:
            question.concepts.clear()
            question.contradiction_rules.clear()

        for concept_data in concepts:
            concept = AnswerConcept(
                name=concept_data.name,
                description=concept_data.description,
                weight=concept_data.weight,
                required=concept_data.required,
                auto_generated=concept_data.auto_generated,
                display_order=concept_data.display_order,
            )
            for kw in concept_data.keywords:
                concept.keywords.append(
                    ConceptKeyword(
                        keyword=kw.keyword,
                        normalized_keyword=strip_diacritics(kw.keyword).lower().strip(),
                        match_type=kw.match_type,
                        minimum_similarity=kw.minimum_similarity,
                        language=kw.language,
                        auto_generated=kw.auto_generated,
                        active=kw.active,
                    )
                )
            question.concepts.append(concept)

        for rule_data in contradiction_rules:
            question.contradiction_rules.append(
                ContradictionRule(
                    pattern=rule_data.pattern,
                    description=rule_data.description,
                    penalty=rule_data.penalty,
                    maximum_score=rule_data.maximum_score,
                    match_type=rule_data.match_type,
                    minimum_similarity=rule_data.minimum_similarity,
                    active=rule_data.active,
                )
            )

    def _resolve_category(self, category_id: int | None, category_name: str | None) -> int:
        if category_id is not None:
            category = self._categories.get(category_id)
            if category is None:
                raise NotFoundError(f"Category {category_id} not found")
            return category_id
        if category_name:
            existing = self._categories.get_by_name(category_name)
            if existing:
                return existing.id
            raise NotFoundError(
                f"Category '{category_name}' not found; create it first or pass category_id"
            )
        raise NotFoundError("category_id or category_name is required")

    def _category_name(self, category_id: int) -> str:
        category = self._categories.get(category_id)
        return category.name if category else ""
