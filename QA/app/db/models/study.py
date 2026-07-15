from __future__ import annotations

from datetime import datetime

from sqlalchemy import Enum as SAEnum
from sqlalchemy import Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.models.enums import Classification, LanguageScope, StudyMode


class StudySession(Base):
    __tablename__ = "study_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    mode: Mapped[StudyMode] = mapped_column(
        SAEnum(StudyMode, native_enum=False, length=20), nullable=False
    )
    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL"), nullable=True
    )
    language_scope: Mapped[LanguageScope | None] = mapped_column(
        SAEnum(LanguageScope, native_enum=False, length=20), nullable=True
    )
    started_at: Mapped[datetime] = mapped_column(nullable=False)
    finished_at: Mapped[datetime | None] = mapped_column(nullable=True)
    total_questions: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    answered_questions: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_score: Mapped[float] = mapped_column(Float, default=0, nullable=False)
    average_score: Mapped[float] = mapped_column(Float, default=0, nullable=False)

    attempts: Mapped[list[Attempt]] = relationship(
        back_populates="session", cascade="all, delete-orphan"
    )


class Attempt(Base):
    __tablename__ = "attempts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    session_id: Mapped[int] = mapped_column(
        ForeignKey("study_sessions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    question_id: Mapped[int] = mapped_column(
        ForeignKey("questions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    # Legacy free-text fields (FREE_TEXT question_format only) -- nullable so MC attempts
    # don't populate them, and old rows stay readable in history unchanged.
    submitted_answer: Mapped[str | None] = mapped_column(Text, nullable=True)
    normalized_answer: Mapped[str | None] = mapped_column(Text, nullable=True)
    evaluation_json: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Multiple-choice fields.
    selected_option_id: Mapped[int | None] = mapped_column(
        ForeignKey("question_options.id", ondelete="SET NULL"), nullable=True
    )
    correct_option_id: Mapped[int | None] = mapped_column(
        ForeignKey("question_options.id", ondelete="SET NULL"), nullable=True
    )
    is_correct: Mapped[bool | None] = mapped_column(nullable=True)
    answer_order_json: Mapped[str | None] = mapped_column(Text, nullable=True)

    score: Mapped[float] = mapped_column(Float, nullable=False)
    classification: Mapped[Classification] = mapped_column(
        SAEnum(Classification, native_enum=False, length=30), nullable=False
    )
    response_time_seconds: Mapped[float | None] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(nullable=False)

    session: Mapped[StudySession] = relationship(back_populates="attempts")


class QuestionProgress(Base):
    __tablename__ = "question_progress"
    __table_args__: tuple = ()

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    question_id: Mapped[int] = mapped_column(
        ForeignKey("questions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    attempt_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    correct_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    incorrect_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    average_score: Mapped[float] = mapped_column(Float, default=0, nullable=False)
    accuracy: Mapped[float] = mapped_column(Float, default=0, nullable=False)
    best_score: Mapped[float] = mapped_column(Float, default=0, nullable=False)
    last_score: Mapped[float] = mapped_column(Float, default=0, nullable=False)
    current_correct_streak: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    best_correct_streak: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    last_is_correct: Mapped[bool | None] = mapped_column(nullable=True)
    last_selected_option_id: Mapped[int | None] = mapped_column(
        ForeignKey("question_options.id", ondelete="SET NULL"), nullable=True
    )
    mastery_level: Mapped[str] = mapped_column(String(20), default="NEW", nullable=False)
    last_reviewed_at: Mapped[datetime | None] = mapped_column(nullable=True)
    next_review_at: Mapped[datetime | None] = mapped_column(nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(nullable=False)
    updated_at: Mapped[datetime] = mapped_column(nullable=False)
