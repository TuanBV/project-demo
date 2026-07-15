"""Study-facing question API. Never returns is_correct/correct_option_id/reference_answer/
concepts/keywords/contradictions/code answers (spec section 6.1) -- only
StudyQuestionResponse is used here. These bare (session-less) endpoints shuffle options
ad-hoc without persisting the order; POST /api/study-sessions/{id}/next is the flow that
guarantees stable ordering across refreshes within a session.
"""

from __future__ import annotations

import random

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.dependencies import evaluation_service, get_db, study_service
from app.core.exceptions import NotFoundError
from app.db.models.enums import Difficulty, LanguageScope, QuestionType, StudyMode
from app.db.models.question import Question
from app.schemas.evaluation import EvaluationResultSchema
from app.schemas.question import CategorySummary, StudyQuestionOptionResponse, StudyQuestionResponse
from app.schemas.study import SubmitAttemptRequest
from app.services.evaluation_service import EvaluationService
from app.services.study_service import StudyService

router = APIRouter(tags=["questions"])


def _study_service(db: Session = Depends(get_db)) -> StudyService:
    return study_service(db)


def _evaluation_service(db: Session = Depends(get_db)) -> EvaluationService:
    return evaluation_service(db)


def _to_study_response(question: Question) -> StudyQuestionResponse:
    active_options = [o for o in question.options if o.active]
    shuffled = random.sample(active_options, k=len(active_options))
    return StudyQuestionResponse(
        id=question.id,
        category=CategorySummary(
            id=question.category_id,
            name=question.category.name if question.category else "",
        ),
        question_type=question.question_type,
        difficulty=question.difficulty,
        language_scope=question.language_scope,
        content=question.content,
        options=[StudyQuestionOptionResponse(id=o.id, content=o.content) for o in shuffled],
    )


@router.get("/api/questions", response_model=list[StudyQuestionResponse])
def list_questions(
    category_id: int | None = None,
    language_scope: LanguageScope | None = None,
    difficulty: Difficulty | None = None,
    question_type: QuestionType | None = None,
    page: int = 1,
    page_size: int = 20,
    service: StudyService = Depends(_study_service),
) -> list[StudyQuestionResponse]:
    questions, _ = service.list_questions(
        category_id=category_id,
        language_scope=language_scope,
        difficulty=difficulty,
        question_type=question_type,
        page=page,
        page_size=page_size,
    )
    return [_to_study_response(q) for q in questions]


@router.get("/api/questions/random", response_model=StudyQuestionResponse)
def random_question(
    category_id: int | None = None,
    language_scope: LanguageScope | None = None,
    difficulty: Difficulty | None = None,
    question_type: QuestionType | None = None,
    exclude_ids: list[int] = Query(default_factory=list),
    unseen_only: bool = False,
    weak_only: bool = False,
    mode: StudyMode = StudyMode.RANDOM,
    service: StudyService = Depends(_study_service),
) -> StudyQuestionResponse:
    question = service.select_question(
        category_id=category_id,
        language_scope=language_scope,
        difficulty=difficulty,
        question_type=question_type,
        exclude_ids=exclude_ids,
        unseen_only=unseen_only,
        weak_only=weak_only,
        mode=mode,
    )
    if question is None:
        raise NotFoundError("Không còn câu hỏi phù hợp với bộ lọc đã chọn")
    return _to_study_response(question)


@router.get("/api/questions/next", response_model=StudyQuestionResponse)
def next_question(
    category_id: int | None = None,
    language_scope: LanguageScope | None = None,
    difficulty: Difficulty | None = None,
    question_type: QuestionType | None = None,
    exclude_ids: list[int] = Query(default_factory=list),
    unseen_only: bool = False,
    weak_only: bool = False,
    mode: StudyMode = StudyMode.RANDOM,
    service: StudyService = Depends(_study_service),
) -> StudyQuestionResponse:
    return random_question(
        category_id=category_id,
        language_scope=language_scope,
        difficulty=difficulty,
        question_type=question_type,
        exclude_ids=exclude_ids,
        unseen_only=unseen_only,
        weak_only=weak_only,
        mode=mode,
        service=service,
    )


@router.get("/api/questions/{question_id}", response_model=StudyQuestionResponse)
def get_question(
    question_id: int, service: StudyService = Depends(_study_service)
) -> StudyQuestionResponse:
    question = service.get_question(question_id)
    if question is None:
        raise NotFoundError(f"Question {question_id} not found")
    return _to_study_response(question)


@router.post(
    "/api/questions/{question_id}/evaluate",
    response_model=EvaluationResultSchema,
    deprecated=True,
    summary="Legacy FREE_TEXT evaluation (deprecated for MULTIPLE_CHOICE questions)",
)
def evaluate_answer(
    question_id: int,
    request: SubmitAttemptRequest,
    service: EvaluationService = Depends(_evaluation_service),
) -> EvaluationResultSchema:
    result = service.evaluate(question_id, request.submitted_answer)
    return EvaluationResultSchema.model_validate(result, from_attributes=True)
