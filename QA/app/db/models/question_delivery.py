"""QuestionDelivery: the option order shown for one (session, question) pairing.

Written the first time a question is served in a session; read back on every subsequent
fetch of the same question in the same session so a page refresh never reshuffles the
options the learner is looking at (spec section 8, requirement 2).
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import ForeignKey, Integer, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class QuestionDelivery(Base):
    __tablename__ = "question_deliveries"
    __table_args__ = (
        UniqueConstraint(
            "session_id", "question_id", name="uq_question_deliveries_session_question"
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    session_id: Mapped[int] = mapped_column(
        ForeignKey("study_sessions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    question_id: Mapped[int] = mapped_column(
        ForeignKey("questions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    option_order_json: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False)
