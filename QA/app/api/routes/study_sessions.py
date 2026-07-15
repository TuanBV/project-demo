from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, study_service
from app.core.exceptions import NotFoundError
from app.db.models.study import StudySession as StudySessionModel
from app.schemas.evaluation import EvaluationResultSchema
from app.schemas.question import CategorySummary, StudyQuestionOptionResponse, StudyQuestionResponse
from app.schemas.study import (
    AnsweredOptionResult,
    AttemptResponse,
    StartSessionRequest,
    StudySessionResponse,
    SubmitAttemptRequest,
    SubmitOptionAnswerRequest,
    SubmitOptionAnswerResponse,
)
from app.services.study_service import StudyService

router = APIRouter(tags=["study-sessions"])


def _service(db: Session = Depends(get_db)) -> StudyService:
    return study_service(db)


def _session_response(session: StudySessionModel) -> StudySessionResponse:
    return StudySessionResponse(
        id=session.id,
        mode=session.mode,
        category_id=session.category_id,
        language_scope=session.language_scope,
        started_at=session.started_at,
        finished_at=session.finished_at,
        total_questions=session.total_questions,
        answered_questions=session.answered_questions,
        average_score=session.average_score,
    )


@router.post("/api/study-sessions", response_model=StudySessionResponse, status_code=201)
def create_session(
    request: StartSessionRequest, service: StudyService = Depends(_service)
) -> StudySessionResponse:
    session = service.start_session(request.mode, request.category_id, request.language_scope)
    return _session_response(session)


@router.get("/api/study-sessions/{session_id}", response_model=StudySessionResponse)
def get_session(session_id: int, service: StudyService = Depends(_service)) -> StudySessionResponse:
    session = service.get_session(session_id)
    return _session_response(session)


@router.post("/api/study-sessions/{session_id}/next", response_model=StudyQuestionResponse)
def next_question(
    session_id: int, service: StudyService = Depends(_service)
) -> StudyQuestionResponse:
    session = service.get_session(session_id)
    exclude_ids = service.attempted_question_ids(session_id)
    question = service.select_question(
        category_id=session.category_id,
        language_scope=session.language_scope,
        exclude_ids=exclude_ids,
        mode=session.mode,
    )
    if question is None:
        raise NotFoundError("Không còn câu hỏi phù hợp cho phiên luyện tập này")

    delivered = service.get_delivered_question(session_id, question.id)
    return StudyQuestionResponse(
        id=delivered.question.id,
        category=CategorySummary(
            id=delivered.question.category_id,
            name=delivered.question.category.name if delivered.question.category else "",
        ),
        question_type=delivered.question.question_type,
        difficulty=delivered.question.difficulty,
        language_scope=delivered.question.language_scope,
        content=delivered.question.content,
        options=[
            StudyQuestionOptionResponse(id=o.id, content=o.content)
            for o in delivered.ordered_options
        ],
    )


@router.post(
    "/api/study-sessions/{session_id}/questions/{question_id}/answer",
    response_model=SubmitOptionAnswerResponse,
)
def submit_option_answer(
    session_id: int,
    question_id: int,
    request: SubmitOptionAnswerRequest,
    service: StudyService = Depends(_service),
) -> SubmitOptionAnswerResponse:
    attempt, correct_option, ordered_options, explanation = service.submit_option_answer(
        session_id, question_id, request.selected_option_id, request.response_time_seconds
    )
    return SubmitOptionAnswerResponse(
        attempt_id=attempt.id,
        question_id=question_id,
        selected_option_id=request.selected_option_id,
        correct_option_id=correct_option.id,
        is_correct=bool(attempt.is_correct),
        score=attempt.score,
        explanation=explanation,
        options=[
            AnsweredOptionResult(
                id=o.id,
                content=o.content,
                is_selected=o.id == request.selected_option_id,
                is_correct=o.is_correct,
            )
            for o in ordered_options
        ],
    )


@router.post(
    "/api/study-sessions/{session_id}/attempts",
    response_model=AttemptResponse,
    deprecated=True,
    summary="Legacy FREE_TEXT attempt submission (deprecated for MULTIPLE_CHOICE questions)",
)
def submit_attempt(
    session_id: int, request: SubmitAttemptRequest, service: StudyService = Depends(_service)
) -> AttemptResponse:
    attempt, result = service.submit_attempt(
        session_id, request.question_id, request.submitted_answer, request.response_time_seconds
    )
    return AttemptResponse(
        id=attempt.id,
        question_id=attempt.question_id,
        score=attempt.score,
        classification=attempt.classification.value,
        evaluation=EvaluationResultSchema.model_validate(result, from_attributes=True),
        response_time_seconds=attempt.response_time_seconds,
        created_at=attempt.created_at,
    )


@router.post("/api/study-sessions/{session_id}/finish", response_model=StudySessionResponse)
def finish_session(
    session_id: int, service: StudyService = Depends(_service)
) -> StudySessionResponse:
    session = service.finish_session(session_id)
    return _session_response(session)
