from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, CheckConstraint, Float, ForeignKey, Integer, String, Text
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin
from app.db.models.enums import MatchType

if TYPE_CHECKING:
    from app.db.models.question import Question


class AnswerConcept(TimestampMixin, Base):
    __tablename__ = "answer_concepts"
    __table_args__ = (CheckConstraint("weight >= 0", name="ck_answer_concepts_weight_nonneg"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    question_id: Mapped[int] = mapped_column(
        ForeignKey("questions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    weight: Mapped[float] = mapped_column(Float, default=0, nullable=False)
    required: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    auto_generated: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    question: Mapped[Question] = relationship(back_populates="concepts")
    keywords: Mapped[list[ConceptKeyword]] = relationship(
        back_populates="concept", cascade="all, delete-orphan"
    )


class ConceptKeyword(TimestampMixin, Base):
    __tablename__ = "concept_keywords"
    __table_args__ = (
        CheckConstraint(
            "minimum_similarity >= 0 AND minimum_similarity <= 100",
            name="ck_concept_keywords_similarity_range",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    concept_id: Mapped[int] = mapped_column(
        ForeignKey("answer_concepts.id", ondelete="CASCADE"), nullable=False, index=True
    )
    keyword: Mapped[str] = mapped_column(String(300), nullable=False)
    normalized_keyword: Mapped[str] = mapped_column(String(300), nullable=False, index=True)
    match_type: Mapped[MatchType] = mapped_column(
        SAEnum(MatchType, native_enum=False, length=20), nullable=False, default=MatchType.CONTAINS
    )
    minimum_similarity: Mapped[float] = mapped_column(Float, default=80, nullable=False)
    language: Mapped[str | None] = mapped_column(String(20), nullable=True)
    auto_generated: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    concept: Mapped[AnswerConcept] = relationship(back_populates="keywords")


class ContradictionRule(TimestampMixin, Base):
    __tablename__ = "contradiction_rules"
    __table_args__ = (
        CheckConstraint("penalty >= 0", name="ck_contradiction_rules_penalty_nonneg"),
        CheckConstraint(
            "maximum_score IS NULL OR (maximum_score >= 0 AND maximum_score <= 100)",
            name="ck_contradiction_rules_max_score_range",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    question_id: Mapped[int] = mapped_column(
        ForeignKey("questions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    pattern: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    penalty: Mapped[float] = mapped_column(Float, default=20, nullable=False)
    maximum_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    match_type: Mapped[MatchType] = mapped_column(
        SAEnum(MatchType, native_enum=False, length=20), nullable=False, default=MatchType.CONTAINS
    )
    minimum_similarity: Mapped[float] = mapped_column(Float, default=85, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    question: Mapped[Question] = relationship(back_populates="contradiction_rules")
