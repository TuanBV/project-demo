"""Admin question API: full rubric CRUD, rubric suggestion, and test-evaluation."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import evaluation_service, get_db, question_service
from app.db.models.enums import Difficulty, LanguageScope, QuestionType
from app.schemas.evaluation import EvaluationResultSchema
from app.schemas.question import (
    AdminQuestionCreate,
    AdminQuestionListItem,
    AdminQuestionResponse,
    AdminQuestionUpdate,
    GenerateDistractorsRequest,
    GenerateDistractorsResponse,
    SuggestRubricRequest,
    SuggestRubricResponse,
    TestEvaluationRequest,
    ValidateQuestionResponse,
)
from app.services.evaluation_service import EvaluationService
from app.services.question_service import QuestionService

router = APIRouter(tags=["admin-questions"])


def _service(db: Session = Depends(get_db)) -> QuestionService:
    return question_service(db)


def _eval_service(db: Session = Depends(get_db)) -> EvaluationService:
    return evaluation_service(db)


@router.get("/api/admin/questions", response_model=list[AdminQuestionListItem])
def list_questions(
    category_id: int | None = None,
    language_scope: LanguageScope | None = None,
    difficulty: Difficulty | None = None,
    question_type: QuestionType | None = None,
    active: bool | None = None,
    search: str | None = None,
    page: int = 1,
    page_size: int = 20,
    service: QuestionService = Depends(_service),
) -> list[AdminQuestionListItem]:
    questions, _ = service.list_filtered(
        category_id=category_id,
        language_scope=language_scope,
        difficulty=difficulty,
        question_type=question_type,
        active_only=bool(active) if active is not None else False,
        search=search,
        page=page,
        page_size=page_size,
    )
    return [AdminQuestionListItem.model_validate(q, from_attributes=True) for q in questions]


@router.get("/api/admin/questions/{question_id}", response_model=AdminQuestionResponse)
def get_question(
    question_id: int, service: QuestionService = Depends(_service)
) -> AdminQuestionResponse:
    question = service.get(question_id)
    return AdminQuestionResponse.model_validate(question, from_attributes=True)


@router.post("/api/admin/questions", response_model=AdminQuestionResponse, status_code=201)
def create_question(
    data: AdminQuestionCreate, service: QuestionService = Depends(_service)
) -> AdminQuestionResponse:
    question = service.create(data)
    return AdminQuestionResponse.model_validate(question, from_attributes=True)


@router.put("/api/admin/questions/{question_id}", response_model=AdminQuestionResponse)
def update_question(
    question_id: int, data: AdminQuestionUpdate, service: QuestionService = Depends(_service)
) -> AdminQuestionResponse:
    question = service.update(question_id, data)
    return AdminQuestionResponse.model_validate(question, from_attributes=True)


@router.delete("/api/admin/questions/{question_id}", status_code=204)
def delete_question(question_id: int, service: QuestionService = Depends(_service)) -> None:
    service.delete(question_id)


@router.post("/api/admin/questions/suggest-rubric", response_model=SuggestRubricResponse)
def suggest_rubric(
    request: SuggestRubricRequest, service: QuestionService = Depends(_service)
) -> SuggestRubricResponse:
    concepts = service.suggest_rubric(request)
    return SuggestRubricResponse(concepts=concepts)


@router.post(
    "/api/admin/questions/{question_id}/test-evaluation", response_model=EvaluationResultSchema
)
def test_evaluation(
    question_id: int,
    request: TestEvaluationRequest,
    service: EvaluationService = Depends(_eval_service),
) -> EvaluationResultSchema:
    result = service.evaluate(question_id, request.submitted_answer)
    return EvaluationResultSchema.model_validate(result, from_attributes=True)


@router.post(
    "/api/admin/questions/{question_id}/duplicate",
    response_model=AdminQuestionResponse,
    status_code=201,
)
def duplicate_question(
    question_id: int, service: QuestionService = Depends(_service)
) -> AdminQuestionResponse:
    question = service.duplicate(question_id)
    return AdminQuestionResponse.model_validate(question, from_attributes=True)


@router.post(
    "/api/admin/questions/generate-distractors", response_model=GenerateDistractorsResponse
)
def generate_distractors(
    request: GenerateDistractorsRequest, service: QuestionService = Depends(_service)
) -> GenerateDistractorsResponse:
    return service.generate_distractors(request)


@router.post(
    "/api/admin/questions/{question_id}/regenerate-distractors",
    response_model=AdminQuestionResponse,
)
def regenerate_distractors(
    question_id: int, service: QuestionService = Depends(_service)
) -> AdminQuestionResponse:
    question = service.regenerate_distractors(question_id)
    return AdminQuestionResponse.model_validate(question, from_attributes=True)


@router.post("/api/admin/questions/{question_id}/validate", response_model=ValidateQuestionResponse)
def validate_question(
    question_id: int, service: QuestionService = Depends(_service)
) -> ValidateQuestionResponse:
    return service.validate_question(question_id)
