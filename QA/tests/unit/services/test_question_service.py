from __future__ import annotations

import pytest
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.db.models.enums import QuestionFormat
from app.repositories.category_repository import CategoryRepository
from app.repositories.question_repository import QuestionRepository
from app.schemas.category import CategoryCreate
from app.schemas.question import (
    AdminQuestionCreate,
    AdminQuestionUpdate,
    AnswerConceptCreate,
    ConceptKeywordCreate,
    SuggestRubricRequest,
)
from app.services.category_service import CategoryService
from app.services.question_service import QuestionService


def _services(db: Session) -> tuple[QuestionService, CategoryService]:
    return (
        QuestionService(QuestionRepository(db), CategoryRepository(db)),
        CategoryService(CategoryRepository(db)),
    )


def _concept() -> AnswerConceptCreate:
    return AnswerConceptCreate(
        name="main",
        description="Y chinh",
        weight=100,
        required=True,
        keywords=[ConceptKeywordCreate(keyword="tu khoa", match_type="CONTAINS")],
    )


def test_create_question_by_category_id(db_session: Session) -> None:
    question_service, category_service = _services(db_session)
    category = category_service.create(CategoryCreate(name="OOP"))
    question = question_service.create(
        AdminQuestionCreate(
            category_id=category.id,
            question_format=QuestionFormat.FREE_TEXT,
            content="Encapsulation la gi?",
            reference_answer="La che giau du lieu.",
            concepts=[_concept()],
        )
    )
    assert question.category_id == category.id
    assert len(question.concepts) == 1
    assert len(question.concepts[0].keywords) == 1


def test_create_question_by_category_name(db_session: Session) -> None:
    question_service, category_service = _services(db_session)
    category_service.create(CategoryCreate(name="Existing Cat"))
    question = question_service.create(
        AdminQuestionCreate(
            category_name="Existing Cat",
            question_format=QuestionFormat.FREE_TEXT,
            content="Q?",
            reference_answer="A.",
        )
    )
    assert question.category.name == "Existing Cat"


def test_create_question_missing_category_raises(db_session: Session) -> None:
    question_service, _ = _services(db_session)
    with pytest.raises(NotFoundError):
        question_service.create(
            AdminQuestionCreate(
                category_id=999, question_format=QuestionFormat.FREE_TEXT, content="Q?"
            )
        )


def test_create_question_unknown_category_name_raises(db_session: Session) -> None:
    question_service, _ = _services(db_session)
    with pytest.raises(NotFoundError):
        question_service.create(
            AdminQuestionCreate(
                category_name="Khong Ton Tai",
                question_format=QuestionFormat.FREE_TEXT,
                content="Q?",
            )
        )


def test_update_question_content_and_rubric(db_session: Session) -> None:
    question_service, category_service = _services(db_session)
    category = category_service.create(CategoryCreate(name="Update Cat"))
    question = question_service.create(
        AdminQuestionCreate(
            category_id=category.id,
            question_format=QuestionFormat.FREE_TEXT,
            content="Q goc?",
            reference_answer="A goc.",
        )
    )
    updated = question_service.update(
        question.id,
        AdminQuestionUpdate(content="Q da sua?", concepts=[_concept()], active=False),
    )
    assert updated.content == "Q da sua?"
    assert updated.active is False
    assert len(updated.concepts) == 1


def test_delete_question(db_session: Session) -> None:
    question_service, category_service = _services(db_session)
    category = category_service.create(CategoryCreate(name="Delete Cat"))
    question = question_service.create(
        AdminQuestionCreate(
            category_id=category.id,
            question_format=QuestionFormat.FREE_TEXT,
            content="Q?",
            reference_answer="A.",
        )
    )
    question_service.delete(question.id)
    with pytest.raises(NotFoundError):
        question_service.get(question.id)


def test_suggest_rubric_returns_concepts(db_session: Session) -> None:
    question_service, _ = _services(db_session)
    suggestions = question_service.suggest_rubric(
        SuggestRubricRequest(
            question="Mutable la gi?",
            reference_answer="Mutable co the thay doi sau khi tao. Immutable thi khong.",
        )
    )
    assert len(suggestions) > 0
    assert all(s.weight > 0 for s in suggestions)


def test_list_filtered_by_category(db_session: Session) -> None:
    question_service, category_service = _services(db_session)
    cat_a = category_service.create(CategoryCreate(name="Filter A"))
    category_service.create(CategoryCreate(name="Filter B"))
    question_service.create(
        AdminQuestionCreate(
            category_id=cat_a.id,
            question_format=QuestionFormat.FREE_TEXT,
            content="Q trong A?",
            reference_answer="A.",
        )
    )
    items, total = question_service.list_filtered(category_id=cat_a.id, active_only=True)
    assert total == 1
    assert items[0].category_id == cat_a.id


def test_create_multiple_choice_question_with_options(db_session: Session) -> None:
    question_service, category_service = _services(db_session)
    category = category_service.create(CategoryCreate(name="MC Cat"))
    question = question_service.create(
        AdminQuestionCreate(
            category_id=category.id,
            content="JVM la gi?",
            options=[
                {"content": "May ao thuc thi Java bytecode.", "is_correct": True},
                {"content": "Trinh bien dich source code.", "is_correct": False},
                {"content": "Thu vien giao dien.", "is_correct": False},
                {"content": "He quan tri CSDL.", "is_correct": False},
            ],
        )
    )
    assert question.question_format.value == "MULTIPLE_CHOICE"
    assert len(question.options) == 4
    assert sum(1 for o in question.options if o.is_correct) == 1
