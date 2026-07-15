from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.core.config import get_settings
from app.db.models.enums import (
    Difficulty,
    LanguageScope,
    MatchType,
    QuestionFormat,
    QuestionType,
    SourceType,
)


class CategorySummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class QuestionOptionCreate(BaseModel):
    content: str = Field(min_length=1)
    is_correct: bool = False
    explanation: str | None = None
    auto_generated: bool = False

    @field_validator("content")
    @classmethod
    def content_not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("option content must not be empty")
        return value


class QuestionOptionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    content: str
    is_correct: bool
    explanation: str | None
    auto_generated: bool
    display_order: int
    active: bool


def _validate_option_set(options: list[QuestionOptionCreate]) -> None:
    settings = get_settings()
    if len(options) != settings.multiple_choice_option_count:
        raise ValueError(
            f"Phải có đúng {settings.multiple_choice_option_count} đáp án, hiện có {len(options)}"
        )
    correct = sum(1 for o in options if o.is_correct)
    if correct != settings.multiple_choice_correct_option_count:
        raise ValueError(
            f"Phải có đúng {settings.multiple_choice_correct_option_count} đáp án đúng, "
            f"hiện có {correct}"
        )
    seen: set[str] = set()
    for option in options:
        key = " ".join(option.content.strip().lower().split())
        if key in seen:
            raise ValueError(f"Các đáp án không được trùng nhau: '{option.content}'")
        seen.add(key)


class ConceptKeywordCreate(BaseModel):
    keyword: str = Field(min_length=1, max_length=300)
    match_type: MatchType = MatchType.CONTAINS
    minimum_similarity: float = Field(default=80.0, ge=0, le=100)
    language: str | None = None
    auto_generated: bool = False
    active: bool = True


class ConceptKeywordResponse(ConceptKeywordCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    normalized_keyword: str


class AnswerConceptCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    description: str | None = None
    weight: float = Field(default=0, ge=0)
    required: bool = False
    auto_generated: bool = False
    display_order: int = 0
    keywords: list[ConceptKeywordCreate] = Field(default_factory=list)

    @field_validator("keywords")
    @classmethod
    def no_empty_keywords(cls, value: list[ConceptKeywordCreate]) -> list[ConceptKeywordCreate]:
        for kw in value:
            if not kw.keyword.strip():
                raise ValueError("keyword must not be empty")
        return value


class AnswerConceptResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    weight: float
    required: bool
    auto_generated: bool
    display_order: int
    keywords: list[ConceptKeywordResponse] = Field(default_factory=list)


class ContradictionRuleCreate(BaseModel):
    pattern: str = Field(min_length=1, max_length=500)
    description: str | None = None
    penalty: float = Field(default=20, ge=0)
    maximum_score: float | None = Field(default=None, ge=0, le=100)
    match_type: MatchType = MatchType.CONTAINS
    minimum_similarity: float = Field(default=85.0, ge=0, le=100)
    active: bool = True


class ContradictionRuleResponse(ContradictionRuleCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int


class AdminQuestionCreate(BaseModel):
    category_id: int | None = None
    category_name: str | None = None
    question_type: QuestionType = QuestionType.TEXT
    question_format: QuestionFormat = QuestionFormat.MULTIPLE_CHOICE
    content: str = Field(min_length=1)
    reference_answer: str | None = None
    explanation: str | None = None
    difficulty: Difficulty = Difficulty.MEDIUM
    language_scope: LanguageScope = LanguageScope.GENERAL
    java_answer: str | None = None
    python_answer: str | None = None
    sql_answer: str | None = None
    active: bool = True
    needs_review: bool = False
    minimum_answer_length: int = 0
    minimum_token_count: int = 0
    options: list[QuestionOptionCreate] = Field(default_factory=list)
    concepts: list[AnswerConceptCreate] = Field(default_factory=list)
    contradiction_rules: list[ContradictionRuleCreate] = Field(default_factory=list)

    @field_validator("content")
    @classmethod
    def content_not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("content must not be empty")
        return value

    @model_validator(mode="after")
    def validate_options(self) -> AdminQuestionCreate:
        if self.question_format == QuestionFormat.MULTIPLE_CHOICE:
            _validate_option_set(self.options)
        return self


class AdminQuestionUpdate(BaseModel):
    category_id: int | None = None
    question_type: QuestionType | None = None
    question_format: QuestionFormat | None = None
    content: str | None = None
    reference_answer: str | None = None
    explanation: str | None = None
    difficulty: Difficulty | None = None
    language_scope: LanguageScope | None = None
    java_answer: str | None = None
    python_answer: str | None = None
    sql_answer: str | None = None
    active: bool | None = None
    needs_review: bool | None = None
    minimum_answer_length: int | None = None
    minimum_token_count: int | None = None
    options: list[QuestionOptionCreate] | None = None
    concepts: list[AnswerConceptCreate] | None = None
    contradiction_rules: list[ContradictionRuleCreate] | None = None

    @model_validator(mode="after")
    def validate_options(self) -> AdminQuestionUpdate:
        if self.options is not None:
            _validate_option_set(self.options)
        return self


class AdminQuestionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    category_id: int
    question_type: QuestionType
    question_format: QuestionFormat
    content: str
    reference_answer: str | None
    explanation: str | None
    difficulty: Difficulty
    language_scope: LanguageScope
    java_answer: str | None
    python_answer: str | None
    sql_answer: str | None
    active: bool
    needs_review: bool
    source_type: SourceType
    source_name: str | None
    minimum_answer_length: int
    minimum_token_count: int
    options: list[QuestionOptionResponse] = Field(default_factory=list)
    concepts: list[AnswerConceptResponse] = Field(default_factory=list)
    contradiction_rules: list[ContradictionRuleResponse] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime


class AdminQuestionListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    category_id: int
    question_type: QuestionType
    question_format: QuestionFormat
    content: str
    difficulty: Difficulty
    language_scope: LanguageScope
    active: bool
    needs_review: bool
    source_type: SourceType


class StudyQuestionOptionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    content: str


class StudyQuestionResponse(BaseModel):
    """Never includes is_correct/correct_option_id/reference_answer/concepts/keywords/
    contradictions/code answers -- study API must not leak the answer (spec section 6.1)."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    category: CategorySummary
    question_type: QuestionType
    difficulty: Difficulty
    language_scope: LanguageScope
    content: str
    options: list[StudyQuestionOptionResponse] = Field(default_factory=list)


class SuggestRubricRequest(BaseModel):
    question: str = Field(min_length=1)
    reference_answer: str = Field(min_length=1)
    language_scope: LanguageScope = LanguageScope.GENERAL


class SuggestedKeyword(BaseModel):
    keyword: str
    language: str | None = None


class SuggestedConcept(BaseModel):
    name: str
    description: str
    weight: float
    required: bool
    keywords: list[str]


class SuggestRubricResponse(BaseModel):
    concepts: list[SuggestedConcept]


class TestEvaluationRequest(BaseModel):
    submitted_answer: str = Field(min_length=0)


class GenerateDistractorsRequest(BaseModel):
    question: str = Field(min_length=1)
    correct_answer: str = Field(min_length=1)
    context: list[str] = Field(default_factory=list)
    count: int = 3


class GenerateDistractorsResponse(BaseModel):
    distractors: list[str]
    warnings: list[str] = Field(default_factory=list)
    has_placeholder: bool = False


class ValidateQuestionResponse(BaseModel):
    status: str
    errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
