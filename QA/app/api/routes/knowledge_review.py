"""Read-only knowledge-review API: deliberately reveals the correct answer for browsing/
studying, unlike the quiz-facing endpoints in questions.py and study_sessions.py. Only
active, admin-approved (needs_review=False) questions are returned."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, question_service
from app.db.models.enums import QuestionFormat
from app.db.models.question import Question
from app.schemas.question import (
    CategorySummary,
    KnowledgeReviewItemResponse,
    KnowledgeReviewListResponse,
)
from app.services.question_service import QuestionService

router = APIRouter(tags=["knowledge-review"])


def _question_service(db: Session = Depends(get_db)) -> QuestionService:
    return question_service(db)


def _to_review_item(question: Question) -> KnowledgeReviewItemResponse:
    active_options = [o for o in question.options if o.active]
    explanation = question.explanation
    if question.question_format == QuestionFormat.MULTIPLE_CHOICE and active_options:
        correct_option = next((o for o in active_options if o.is_correct), None)
        correct_answer = correct_option.content if correct_option else ""
        if not explanation and correct_option is not None:
            explanation = correct_option.explanation
    else:
        correct_answer = question.reference_answer or ""

    return KnowledgeReviewItemResponse(
        id=question.id,
        category=CategorySummary(
            id=question.category_id,
            name=question.category.name if question.category else "",
        ),
        question_type=question.question_type,
        difficulty=question.difficulty,
        content=question.content,
        correct_answer=correct_answer,
        explanation=explanation,
    )


@router.get("/api/knowledge-review", response_model=KnowledgeReviewListResponse)
def list_knowledge_review(
    category_id: int | None = None,
    page: int = 1,
    page_size: int = 20,
    service: QuestionService = Depends(_question_service),
) -> KnowledgeReviewListResponse:
    questions, total = service.list_for_review(
        category_id=category_id, page=page, page_size=page_size
    )
    return KnowledgeReviewListResponse(
        items=[_to_review_item(q) for q in questions],
        total=total,
        page=page,
        page_size=page_size,
    )
