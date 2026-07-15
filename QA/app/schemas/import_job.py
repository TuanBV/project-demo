from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from app.db.models.enums import (
    DuplicateStrategy,
    ImportStatus,
    QuestionFormat,
    QuestionType,
    SourceType,
)


class TextImportRequest(BaseModel):
    content: str = Field(min_length=1)
    dry_run: bool = False
    duplicate_strategy: DuplicateStrategy = DuplicateStrategy.SKIP
    generate_concepts: bool = False
    default_category: str | None = None
    default_question_type: QuestionType = QuestionType.TEXT
    default_language_scope: str | None = None
    question_format: QuestionFormat = QuestionFormat.MULTIPLE_CHOICE


class ImportPreviewItem(BaseModel):
    source_order: int
    category: str | None
    question_type: str
    question: str
    answer: str | None
    status: str
    warnings: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)
    question_id: int | None = None


class ImportSummary(BaseModel):
    categories_detected: int = 0
    questions_detected: int = 0
    valid_questions: int = 0
    warning_count: int = 0
    error_count: int = 0
    categories_created: int = 0
    questions_created: int = 0
    questions_updated: int = 0
    questions_skipped: int = 0
    questions_needs_review: int = 0


class ImportResultResponse(BaseModel):
    dry_run: bool
    job_id: int | None
    summary: ImportSummary
    items: list[ImportPreviewItem]
    unparsed_segments: list[str] = Field(default_factory=list)


class ImportJobResponse(BaseModel):
    id: int
    source_type: SourceType
    source_name: str | None
    status: ImportStatus
    dry_run: bool
    duplicate_strategy: DuplicateStrategy
    summary: ImportSummary | None
    created_at: datetime
    completed_at: datetime | None
