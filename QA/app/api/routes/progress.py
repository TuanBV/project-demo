from __future__ import annotations

import json

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, progress_service
from app.core.exceptions import NotFoundError
from app.schemas.study import HistoryItemResponse, ProgressOverviewResponse, WeakQuestionItem
from app.services.progress_service import ProgressService

router = APIRouter(tags=["progress"])


def _service(db: Session = Depends(get_db)) -> ProgressService:
    return progress_service(db)


@router.get("/api/progress/overview", response_model=ProgressOverviewResponse)
def progress_overview(service: ProgressService = Depends(_service)) -> ProgressOverviewResponse:
    return ProgressOverviewResponse(**service.overview())


@router.get("/api/progress/categories")
def progress_categories(service: ProgressService = Depends(_service)) -> list:
    return service.categories_progress()


@router.get("/api/progress/weak-questions", response_model=list[WeakQuestionItem])
def weak_questions(
    limit: int = 20, service: ProgressService = Depends(_service)
) -> list[WeakQuestionItem]:
    return service.weak_questions(limit)


@router.get("/api/history", response_model=list[HistoryItemResponse])
def history(
    page: int = 1, page_size: int = 20, service: ProgressService = Depends(_service)
) -> list[HistoryItemResponse]:
    items, _ = service.history(page, page_size)
    return items


@router.get("/api/history/{attempt_id}")
def history_detail(attempt_id: int, service: ProgressService = Depends(_service)) -> dict:
    attempt = service.get_attempt(attempt_id)
    if attempt is None:
        raise NotFoundError(f"Attempt {attempt_id} not found")
    return {
        "attempt_id": attempt.id,
        "question_id": attempt.question_id,
        "score": attempt.score,
        "classification": attempt.classification.value,
        "is_correct": attempt.is_correct,
        "selected_option_id": attempt.selected_option_id,
        "correct_option_id": attempt.correct_option_id,
        "submitted_answer": attempt.submitted_answer,
        "evaluation": json.loads(attempt.evaluation_json) if attempt.evaluation_json else None,
        "response_time_seconds": attempt.response_time_seconds,
        "created_at": attempt.created_at.isoformat(),
    }
