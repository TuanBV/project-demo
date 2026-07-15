"""QuestionOption: one of the 4 answer choices for a MULTIPLE_CHOICE question.

Exactly-one-correct is enforced at two layers: a partial unique index here (at most one
`is_correct=True` row per question_id — SQLite/Postgres both support partial indexes) and
QuestionOptionService running the full 4-option/1-correct check inside a transaction (see
docs/multiple-choice-migration-plan.md section 1) since "exactly one" (not just "at most
one") needs a row-count check a single-column index can't express.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, CheckConstraint, ForeignKey, Index, Integer, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.db.models.question import Question


class QuestionOption(TimestampMixin, Base):
    __tablename__ = "question_options"
    __table_args__ = (
        CheckConstraint("length(trim(content)) > 0", name="ck_question_options_content_nonempty"),
        Index(
            "ux_question_options_one_correct",
            "question_id",
            unique=True,
            sqlite_where=text("is_correct = 1"),
            postgresql_where=text("is_correct = true"),
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    question_id: Mapped[int] = mapped_column(
        ForeignKey("questions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    normalized_content: Mapped[str] = mapped_column(String(500), nullable=False, index=True)
    is_correct: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    auto_generated: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    explanation: Mapped[str | None] = mapped_column(Text, nullable=True)
    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    question: Mapped[Question] = relationship(back_populates="options")
