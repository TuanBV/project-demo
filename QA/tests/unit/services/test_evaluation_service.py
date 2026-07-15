"""EvaluationService: legacy FREE_TEXT evaluation path (kept for /evaluate + question
question_format=FREE_TEXT). Must keep working exactly as before the MC migration."""

from __future__ import annotations

import pytest
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.db.models.enums import QuestionFormat
from app.evaluation.keyword_evaluator import KeywordAnswerEvaluator
from app.repositories.category_repository import CategoryRepository
from app.repositories.question_repository import QuestionRepository
from app.schemas.category import CategoryCreate
from app.schemas.question import AdminQuestionCreate, AnswerConceptCreate, ConceptKeywordCreate
from app.services.category_service import CategoryService
from app.services.evaluation_service import EvaluationService
from app.services.question_service import QuestionService


def _services(db: Session) -> tuple[EvaluationService, QuestionService, CategoryService]:
    evaluation_service = EvaluationService(QuestionRepository(db), KeywordAnswerEvaluator())
    question_service = QuestionService(QuestionRepository(db), CategoryRepository(db))
    category_service = CategoryService(CategoryRepository(db))
    return evaluation_service, question_service, category_service


def test_evaluate_free_text_question_scores_correctly(db_session: Session) -> None:
    evaluation_service, question_service, category_service = _services(db_session)
    category = category_service.create(CategoryCreate(name="Eval Cat"))
    question = question_service.create(
        AdminQuestionCreate(
            category_id=category.id,
            question_format=QuestionFormat.FREE_TEXT,
            content="JVM la gi?",
            reference_answer="JVM la may ao thuc thi Java bytecode.",
            concepts=[
                AnswerConceptCreate(
                    name="main",
                    description="JVM la may ao thuc thi bytecode",
                    weight=100,
                    required=True,
                    keywords=[ConceptKeywordCreate(keyword="bytecode", match_type="CONTAINS")],
                )
            ],
        )
    )

    result = evaluation_service.evaluate(question.id, "JVM thuc thi Java bytecode")
    assert result.score == 100.0
    assert result.classification == "CORRECT"


def test_evaluate_missing_question_raises(db_session: Session) -> None:
    evaluation_service, _, _ = _services(db_session)
    with pytest.raises(NotFoundError):
        evaluation_service.evaluate(999, "answer")


def test_evaluate_missing_concepts_scores_zero(db_session: Session) -> None:
    evaluation_service, question_service, category_service = _services(db_session)
    category = category_service.create(CategoryCreate(name="Eval Cat 2"))
    question = question_service.create(
        AdminQuestionCreate(
            category_id=category.id,
            question_format=QuestionFormat.FREE_TEXT,
            content="Q?",
            reference_answer="A.",
            concepts=[
                AnswerConceptCreate(
                    name="main",
                    description="desc",
                    weight=100,
                    required=True,
                    keywords=[
                        ConceptKeywordCreate(keyword="tu khoa duy nhat", match_type="CONTAINS")
                    ],
                )
            ],
        )
    )
    result = evaluation_service.evaluate(question.id, "cau tra loi khong lien quan gi ca")
    assert result.score == 0.0
