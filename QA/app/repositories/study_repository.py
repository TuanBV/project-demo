from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from app.db.models.question_delivery import QuestionDelivery
from app.db.models.study import Attempt, QuestionProgress, StudySession


class StudyRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_session(self, session: StudySession) -> StudySession:
        self.db.add(session)
        self.db.flush()
        return session

    def get_session(self, session_id: int) -> StudySession | None:
        return self.db.get(StudySession, session_id)

    def create_attempt(self, attempt: Attempt) -> Attempt:
        self.db.add(attempt)
        self.db.flush()
        return attempt

    def get_progress(self, question_id: int, user_id: int | None = None) -> QuestionProgress | None:
        stmt = select(QuestionProgress).where(
            QuestionProgress.question_id == question_id,
            QuestionProgress.user_id.is_(user_id),
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def list_all_progress(self, user_id: int | None = None) -> list[QuestionProgress]:
        stmt = select(QuestionProgress).where(QuestionProgress.user_id.is_(user_id))
        return list(self.db.execute(stmt).scalars().all())

    def save_progress(self, progress: QuestionProgress) -> QuestionProgress:
        self.db.add(progress)
        self.db.flush()
        return progress

    def list_history(self, page: int = 1, page_size: int = 20) -> tuple[list[Attempt], int]:
        stmt = (
            select(Attempt).options(joinedload(Attempt.session)).order_by(Attempt.created_at.desc())
        )
        total = len(self.db.execute(stmt).scalars().all())
        stmt = stmt.offset((page - 1) * page_size).limit(page_size)
        items = list(self.db.execute(stmt).unique().scalars().all())
        return items, total

    def get_attempt(self, attempt_id: int) -> Attempt | None:
        return self.db.get(Attempt, attempt_id)

    def list_mc_attempts_chronological(self) -> list[Attempt]:
        stmt = (
            select(Attempt)
            .where(Attempt.is_correct.is_not(None))
            .order_by(Attempt.created_at.asc())
        )
        return list(self.db.execute(stmt).scalars().all())

    def most_selected_wrong_options(self, limit: int = 10) -> list[tuple[int, int, int]]:
        """Returns (question_id, selected_option_id, count) for incorrect attempts,
        most-selected first."""
        stmt = (
            select(
                Attempt.question_id,
                Attempt.selected_option_id,
                func.count().label("cnt"),
            )
            .where(Attempt.is_correct.is_(False), Attempt.selected_option_id.is_not(None))
            .group_by(Attempt.question_id, Attempt.selected_option_id)
            .order_by(func.count().desc())
            .limit(limit)
        )
        return [(row[0], row[1], row[2]) for row in self.db.execute(stmt).all()]

    def most_missed_question_ids(self, limit: int = 10) -> list[tuple[int, int, int]]:
        """Returns (question_id, incorrect_count, attempt_count) most-missed first."""
        stmt = (
            select(
                QuestionProgress.question_id,
                QuestionProgress.incorrect_count,
                QuestionProgress.attempt_count,
            )
            .where(QuestionProgress.incorrect_count > 0)
            .order_by(QuestionProgress.incorrect_count.desc())
            .limit(limit)
        )
        return [(row[0], row[1], row[2]) for row in self.db.execute(stmt).all()]

    def attempted_question_ids(self, session_id: int) -> list[int]:
        stmt = select(Attempt.question_id).where(Attempt.session_id == session_id)
        return list(self.db.execute(stmt).scalars().all())

    def get_attempt_for_question(self, session_id: int, question_id: int) -> Attempt | None:
        stmt = select(Attempt).where(
            Attempt.session_id == session_id, Attempt.question_id == question_id
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def get_delivery(self, session_id: int, question_id: int) -> QuestionDelivery | None:
        stmt = select(QuestionDelivery).where(
            QuestionDelivery.session_id == session_id,
            QuestionDelivery.question_id == question_id,
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def create_delivery(self, delivery: QuestionDelivery) -> QuestionDelivery:
        self.db.add(delivery)
        self.db.flush()
        return delivery

    def weak_question_ids(self, threshold: float, user_id: int | None = None) -> list[int]:
        stmt = select(QuestionProgress.question_id).where(
            QuestionProgress.user_id.is_(user_id),
            QuestionProgress.average_score < threshold,
        )
        return list(self.db.execute(stmt).scalars().all())

    def unseen_question_ids(
        self, all_question_ids: list[int], user_id: int | None = None
    ) -> list[int]:
        stmt = select(QuestionProgress.question_id).where(QuestionProgress.user_id.is_(user_id))
        seen = set(self.db.execute(stmt).scalars().all())
        return [qid for qid in all_question_ids if qid not in seen]

    def commit(self) -> None:
        self.db.commit()
