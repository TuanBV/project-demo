from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from app.db.models.enums import Difficulty, LanguageScope, QuestionType, StudyMode
from app.schemas.evaluation import EvaluationResultSchema


class StartSessionRequest(BaseModel):
    mode: StudyMode = StudyMode.RANDOM
    category_id: int | None = None
    language_scope: LanguageScope | None = None


class StudySessionResponse(BaseModel):
    id: int
    mode: StudyMode
    category_id: int | None
    language_scope: LanguageScope | None
    started_at: datetime
    finished_at: datetime | None
    total_questions: int
    answered_questions: int
    average_score: float


class SubmitAttemptRequest(BaseModel):
    """Legacy free-text submit request -- FREE_TEXT questions only (see /evaluate)."""

    question_id: int
    submitted_answer: str = Field(default="", max_length=20000)
    response_time_seconds: float | None = None


class AttemptResponse(BaseModel):
    id: int
    question_id: int
    score: float
    classification: str
    evaluation: EvaluationResultSchema
    response_time_seconds: float | None
    created_at: datetime


class SubmitOptionAnswerRequest(BaseModel):
    selected_option_id: int
    response_time_seconds: float | None = None


class AnsweredOptionResult(BaseModel):
    id: int
    content: str
    is_selected: bool
    is_correct: bool


class SubmitOptionAnswerResponse(BaseModel):
    attempt_id: int
    question_id: int
    selected_option_id: int
    correct_option_id: int
    is_correct: bool
    score: float
    explanation: str | None
    options: list[AnsweredOptionResult]


class CategoryProgress(BaseModel):
    category_id: int
    category_name: str
    total_questions: int
    attempted_questions: int
    average_score: float


class DifficultyProgress(BaseModel):
    difficulty: str
    total_questions: int
    attempted_questions: int
    accuracy: float


class MostMissedQuestion(BaseModel):
    question_id: int
    content: str
    category_name: str
    incorrect_count: int
    attempt_count: int


class MostSelectedWrongOption(BaseModel):
    question_id: int
    question_content: str
    option_id: int
    option_content: str
    selected_count: int


class ProgressOverviewResponse(BaseModel):
    total_questions: int
    attempted_questions: int
    unattempted_questions: int
    mastered_questions: int
    average_score: float
    total_attempts: int = 0
    correct_count: int = 0
    incorrect_count: int = 0
    accuracy: float = 0.0
    current_streak: int = 0
    best_streak: int = 0
    categories: list[CategoryProgress]
    difficulty: list[DifficultyProgress] = Field(default_factory=list)
    most_missed_questions: list[MostMissedQuestion] = Field(default_factory=list)
    most_selected_wrong_options: list[MostSelectedWrongOption] = Field(default_factory=list)


class WeakQuestionItem(BaseModel):
    question_id: int
    content: str
    category_name: str
    average_score: float
    attempt_count: int


class HistoryItemResponse(BaseModel):
    attempt_id: int
    question_id: int
    question_content: str
    category_name: str
    score: float
    classification: str
    is_correct: bool | None = None
    selected_option_id: int | None = None
    correct_option_id: int | None = None
    options: list[AnsweredOptionResult] | None = None
    explanation: str | None = None
    response_time_seconds: float | None
    created_at: datetime


class RandomSelectionQuery(BaseModel):
    category_id: int | None = None
    language_scope: LanguageScope | None = None
    difficulty: Difficulty | None = None
    question_type: QuestionType | None = None
    exclude_ids: list[int] = Field(default_factory=list)
    unseen_only: bool = False
    weak_only: bool = False
