from __future__ import annotations

import pytest
from sqlalchemy.orm import Session

from app.importers.dto import (
    ImportOptions,
    ParsedQuestion,
    ValidatedImportDocument,
    ValidatedQuestionItem,
)
from app.repositories.category_repository import CategoryRepository
from app.repositories.import_repository import ImportRepository
from app.repositories.question_repository import QuestionRepository
from app.services.import_service import QuestionImportService


def _make_service(db: Session) -> QuestionImportService:
    return QuestionImportService(
        db=db,
        question_repository=QuestionRepository(db),
        category_repository=CategoryRepository(db),
        import_repository=ImportRepository(db),
    )


def _validated(question: ParsedQuestion, status: str = "VALID") -> ValidatedImportDocument:
    return ValidatedImportDocument(items=[ValidatedQuestionItem(parsed=question, status=status)])


def _question(**overrides: object) -> ParsedQuestion:
    defaults = dict(
        source_order=1,
        category_name="Test Cat",
        question_type="TEXT",
        language_scope="GENERAL",
        difficulty="MEDIUM",
        content="Cau hoi mau?",
        reference_answer="Dap an mau.",
        keywords=["mau", "test"],
    )
    defaults.update(overrides)
    return ParsedQuestion(**defaults)  # type: ignore[arg-type]


def test_dry_run_does_not_write_database(db_session: Session) -> None:
    service = _make_service(db_session)
    result = service.import_document(_validated(_question()), ImportOptions(dry_run=True))
    assert result.dry_run is True
    assert result.job_id is None
    assert QuestionRepository(db_session).get_by_content_hash("anything") is None
    assert len(CategoryRepository(db_session).list_all()) == 0


def test_import_without_explicit_options_needs_review(db_session: Session) -> None:
    """Question+correct-answer-only sources get auto-distractors and must be reviewed
    before they can appear in study (spec section 9.7/10.1)."""
    service = _make_service(db_session)
    result = service.import_document(_validated(_question()), ImportOptions(dry_run=False))
    assert result.summary.questions_created == 1
    assert result.summary.categories_created == 1
    assert result.items[0].status == "NEEDS_REVIEW"

    question_id = result.items[0].question_id
    saved = QuestionRepository(db_session).get_with_rubric(question_id)
    assert saved.needs_review is True
    assert saved.active is False
    assert len(saved.options) == 4
    assert sum(1 for o in saved.options if o.is_correct) == 1
    correct = next(o for o in saved.options if o.is_correct)
    assert correct.content == "Dap an mau."
    assert all(o.auto_generated for o in saved.options if not o.is_correct)


def test_import_with_explicit_four_options_is_active_immediately(db_session: Session) -> None:
    service = _make_service(db_session)
    question = _question(options=["Dap an mau.", "Sai 1", "Sai 2", "Sai 3"], correct_option_index=0)
    result = service.import_document(_validated(question), ImportOptions(dry_run=False))
    assert result.items[0].status == "CREATED"

    question_id = result.items[0].question_id
    saved = QuestionRepository(db_session).get_with_rubric(question_id)
    assert saved.needs_review is False
    assert saved.active is True
    assert len(saved.options) == 4
    assert all(not o.auto_generated for o in saved.options)


def test_reimport_with_skip_strategy(db_session: Session) -> None:
    service = _make_service(db_session)
    options_create = ImportOptions(dry_run=False, duplicate_strategy="SKIP")
    service.import_document(_validated(_question()), options_create)
    result2 = service.import_document(_validated(_question()), options_create)
    assert result2.summary.questions_skipped == 1
    assert result2.summary.questions_created == 0


def test_reimport_with_update_strategy(db_session: Session) -> None:
    service = _make_service(db_session)
    options = ImportOptions(dry_run=False, duplicate_strategy="UPDATE")
    service.import_document(_validated(_question()), options)
    updated_question = _question(reference_answer="Dap an da duoc cap nhat.")
    result2 = service.import_document(_validated(updated_question), options)
    assert result2.summary.questions_updated == 1
    question_id = result2.items[0].question_id
    assert question_id is not None
    question = QuestionRepository(db_session).get_with_rubric(question_id)
    assert question.reference_answer == "Dap an da duoc cap nhat."
    assert len(question.options) == 4
    correct = next(o for o in question.options if o.is_correct)
    assert correct.content == "Dap an da duoc cap nhat."


def test_reimport_with_create_copy_strategy(db_session: Session) -> None:
    service = _make_service(db_session)
    options = ImportOptions(dry_run=False, duplicate_strategy="CREATE_COPY")
    service.import_document(_validated(_question()), options)
    result2 = service.import_document(_validated(_question()), options)
    assert result2.summary.questions_created == 1
    assert len(CategoryRepository(db_session).list_all()[0].questions) == 2


def test_transaction_rollback_on_error(
    db_session: Session, monkeypatch: pytest.MonkeyPatch
) -> None:
    service = _make_service(db_session)

    def boom(*args: object, **kwargs: object) -> None:
        raise RuntimeError("forced failure")

    monkeypatch.setattr(service, "_build_mc_options", boom)
    with pytest.raises(RuntimeError):
        service.import_document(_validated(_question()), ImportOptions(dry_run=False))

    assert len(CategoryRepository(db_session).list_all()) == 0


def test_import_report_counts_are_accurate(db_session: Session) -> None:
    service = _make_service(db_session)
    doc = ValidatedImportDocument(
        items=[
            ValidatedQuestionItem(parsed=_question(source_order=1, content="Q1?"), status="VALID"),
            ValidatedQuestionItem(
                parsed=_question(source_order=2, content="Q2?"),
                status="WARNING",
                warnings=["thieu gi do"],
            ),
            ValidatedQuestionItem(
                parsed=_question(source_order=3, content=""), status="ERROR", errors=["rong"]
            ),
        ]
    )
    result = service.import_document(doc, ImportOptions(dry_run=False))
    assert result.summary.questions_detected == 3
    assert result.summary.error_count == 1
    assert result.summary.warning_count == 1
    assert result.summary.questions_created == 2


def test_auto_generated_distractors_are_flagged(db_session: Session) -> None:
    service = _make_service(db_session)
    question = _question(
        keywords=[], reference_answer="Mutable co the thay doi trang thai sau khi tao."
    )
    result = service.import_document(
        _validated(question), ImportOptions(dry_run=False, generate_concepts=True)
    )
    question_id = result.items[0].question_id
    saved = QuestionRepository(db_session).get_with_rubric(question_id)
    assert len(saved.options) == 4
    distractors = [o for o in saved.options if not o.is_correct]
    assert len(distractors) == 3
    assert all(o.auto_generated for o in distractors)


def test_free_text_format_still_builds_concepts(db_session: Session) -> None:
    """default_question_format=FREE_TEXT keeps the legacy concept/keyword rubric path."""
    service = _make_service(db_session)
    question = _question(keywords=["mau", "test"])
    result = service.import_document(
        _validated(question),
        ImportOptions(dry_run=False, default_question_format="FREE_TEXT"),
    )
    question_id = result.items[0].question_id
    saved = QuestionRepository(db_session).get_with_rubric(question_id)
    assert saved.question_format.value == "FREE_TEXT"
    assert len(saved.options) == 0
    assert len(saved.concepts) > 0


def test_text_import_has_pasted_text_source_type(db_session: Session) -> None:
    service = _make_service(db_session)
    result = service.import_document(
        _validated(_question()),
        ImportOptions(dry_run=False, source_type="PASTED_TEXT"),
    )
    question_id = result.items[0].question_id
    saved = QuestionRepository(db_session).get(question_id)
    assert saved.source_type.value == "PASTED_TEXT"
