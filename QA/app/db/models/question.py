from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin
from app.db.models.enums import (
    Difficulty,
    LanguageScope,
    QuestionFormat,
    QuestionType,
    SourceType,
)

if TYPE_CHECKING:
    from app.db.models.category import Category
    from app.db.models.evaluation import AnswerConcept, ContradictionRule
    from app.db.models.question_option import QuestionOption


class Question(TimestampMixin, Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="CASCADE"), nullable=False, index=True
    )
    question_type: Mapped[QuestionType] = mapped_column(
        SAEnum(QuestionType, native_enum=False, length=20), nullable=False
    )
    question_format: Mapped[QuestionFormat] = mapped_column(
        SAEnum(QuestionFormat, native_enum=False, length=20),
        nullable=False,
        default=QuestionFormat.MULTIPLE_CHOICE,
    )
    needs_review: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    reference_answer: Mapped[str | None] = mapped_column(Text, nullable=True)
    explanation: Mapped[str | None] = mapped_column(Text, nullable=True)
    difficulty: Mapped[Difficulty] = mapped_column(
        SAEnum(Difficulty, native_enum=False, length=20),
        nullable=False,
        default=Difficulty.MEDIUM,
    )
    language_scope: Mapped[LanguageScope] = mapped_column(
        SAEnum(LanguageScope, native_enum=False, length=20),
        nullable=False,
        default=LanguageScope.GENERAL,
    )
    java_answer: Mapped[str | None] = mapped_column(Text, nullable=True)
    python_answer: Mapped[str | None] = mapped_column(Text, nullable=True)
    sql_answer: Mapped[str | None] = mapped_column(Text, nullable=True)
    content_hash: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    source_type: Mapped[SourceType] = mapped_column(
        SAEnum(SourceType, native_enum=False, length=20), nullable=False
    )
    source_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    source_order: Mapped[int | None] = mapped_column(Integer, nullable=True)
    minimum_answer_length: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    minimum_token_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    category: Mapped[Category] = relationship(back_populates="questions")
    concepts: Mapped[list[AnswerConcept]] = relationship(
        back_populates="question",
        cascade="all, delete-orphan",
        order_by="AnswerConcept.display_order",
    )
    contradiction_rules: Mapped[list[ContradictionRule]] = relationship(
        back_populates="question", cascade="all, delete-orphan"
    )
    options: Mapped[list[QuestionOption]] = relationship(
        back_populates="question",
        cascade="all, delete-orphan",
        order_by="QuestionOption.display_order",
    )
