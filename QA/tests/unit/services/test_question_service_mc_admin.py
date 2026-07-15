"""QuestionService admin helpers specific to the MC flow: duplicate, distractor
generation/regeneration, and structural validation (spec section 13)."""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.repositories.category_repository import CategoryRepository
from app.repositories.question_repository import QuestionRepository
from app.schemas.category import CategoryCreate
from app.schemas.question import AdminQuestionCreate, GenerateDistractorsRequest
from app.services.category_service import CategoryService
from app.services.question_service import QuestionService


def _services(db: Session) -> tuple[QuestionService, CategoryService]:
    return (
        QuestionService(QuestionRepository(db), CategoryRepository(db)),
        CategoryService(CategoryRepository(db)),
    )


def _mc_question(question_service: QuestionService, category_id: int):
    return question_service.create(
        AdminQuestionCreate(
            category_id=category_id,
            content="JVM la gi?",
            options=[
                {"content": "May ao thuc thi Java bytecode.", "is_correct": True},
                {"content": "Trinh bien dich.", "is_correct": False},
                {"content": "Thu vien giao dien.", "is_correct": False},
                {"content": "He quan tri CSDL.", "is_correct": False},
            ],
        )
    )


def test_duplicate_clones_question_inactive(db_session: Session) -> None:
    question_service, category_service = _services(db_session)
    category = category_service.create(CategoryCreate(name="Dup Cat"))
    original = _mc_question(question_service, category.id)

    clone = question_service.duplicate(original.id)
    assert clone.id != original.id
    assert clone.active is False
    assert len(clone.options) == 4
    assert "(copy)" in clone.content


def test_generate_distractors_returns_three_with_metadata(db_session: Session) -> None:
    question_service, _ = _services(db_session)
    result = question_service.generate_distractors(
        GenerateDistractorsRequest(
            question="Compiler la gi?",
            correct_answer="Compiler dich toan bo ma nguon truoc khi chay.",
            count=3,
        )
    )
    assert len(result.distractors) == 3
    assert isinstance(result.warnings, list)
    assert isinstance(result.has_placeholder, bool)


def test_regenerate_distractors_replaces_auto_generated_options(db_session: Session) -> None:
    question_service, category_service = _services(db_session)
    category = category_service.create(CategoryCreate(name="Regen Cat"))
    question = _mc_question(question_service, category.id)

    updated = question_service.regenerate_distractors(question.id)
    correct = [o for o in updated.options if o.is_correct]
    distractors = [o for o in updated.options if not o.is_correct]
    assert len(correct) == 1
    assert correct[0].content == "May ao thuc thi Java bytecode."
    assert len(distractors) == 3
    assert all(o.auto_generated for o in distractors)


def test_validate_question_reports_valid_for_well_formed_mc(db_session: Session) -> None:
    question_service, category_service = _services(db_session)
    category = category_service.create(CategoryCreate(name="Validate Cat"))
    question = _mc_question(question_service, category.id)

    result = question_service.validate_question(question.id)
    assert result.status == "VALID"
    assert result.errors == []


def test_validate_question_flags_needs_review(db_session: Session) -> None:
    question_service, category_service = _services(db_session)
    category = category_service.create(CategoryCreate(name="Validate Cat 2"))
    question = question_service.create(
        AdminQuestionCreate(
            category_id=category.id,
            content="Q?",
            needs_review=True,
            active=False,
            options=[
                {"content": "Dung.", "is_correct": True},
                {"content": "Sai 1.", "is_correct": False},
                {"content": "Sai 2.", "is_correct": False},
                {"content": "Sai 3.", "is_correct": False},
            ],
        )
    )
    result = question_service.validate_question(question.id)
    assert result.status == "NEEDS_REVIEW"
