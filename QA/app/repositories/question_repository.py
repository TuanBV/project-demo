from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import joinedload, selectinload

from app.db.models.enums import Difficulty, LanguageScope, QuestionFormat, QuestionType
from app.db.models.evaluation import AnswerConcept
from app.db.models.question import Question
from app.db.models.question_option import QuestionOption
from app.repositories.base import BaseRepository


class QuestionRepository(BaseRepository[Question]):
    model = Question

    def get_with_rubric(self, question_id: int) -> Question | None:
        stmt = (
            select(Question)
            .options(
                selectinload(Question.concepts).selectinload(AnswerConcept.keywords),
                selectinload(Question.contradiction_rules),
                selectinload(Question.options),
                joinedload(Question.category),
            )
            .where(Question.id == question_id)
        )
        return self.db.execute(stmt).unique().scalar_one_or_none()

    def get_by_content_hash(self, content_hash: str) -> Question | None:
        stmt = select(Question).where(Question.content_hash == content_hash)
        return self.db.execute(stmt).scalar_one_or_none()

    def get_option(self, option_id: int) -> QuestionOption | None:
        return self.db.get(QuestionOption, option_id)

    def list_filtered(
        self,
        *,
        category_id: int | None = None,
        language_scope: LanguageScope | None = None,
        difficulty: Difficulty | None = None,
        question_type: QuestionType | None = None,
        active_only: bool = True,
        search: str | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list[Question], int]:
        stmt = select(Question).options(joinedload(Question.category))
        if active_only:
            stmt = stmt.where(Question.active.is_(True))
        if category_id is not None:
            stmt = stmt.where(Question.category_id == category_id)
        if language_scope is not None:
            stmt = stmt.where(Question.language_scope == language_scope)
        if difficulty is not None:
            stmt = stmt.where(Question.difficulty == difficulty)
        if question_type is not None:
            stmt = stmt.where(Question.question_type == question_type)
        if search:
            like = f"%{search.lower()}%"
            stmt = stmt.where(func.lower(Question.content).like(like))

        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = self.db.execute(count_stmt).scalar_one()

        stmt = stmt.order_by(Question.id).offset((page - 1) * page_size).limit(page_size)
        items = list(self.db.execute(stmt).unique().scalars().all())
        return items, total

    def list_candidates(
        self,
        *,
        category_id: int | None = None,
        language_scope: LanguageScope | None = None,
        difficulty: Difficulty | None = None,
        question_type: QuestionType | None = None,
        question_format: QuestionFormat | None = QuestionFormat.MULTIPLE_CHOICE,
        exclude_ids: list[int] | None = None,
    ) -> list[Question]:
        stmt = (
            select(Question)
            .options(selectinload(Question.options), joinedload(Question.category))
            .where(Question.active.is_(True), Question.needs_review.is_(False))
        )
        if question_format is not None:
            stmt = stmt.where(Question.question_format == question_format)
        if category_id is not None:
            stmt = stmt.where(Question.category_id == category_id)
        if language_scope is not None:
            stmt = stmt.where(Question.language_scope == language_scope)
        if difficulty is not None:
            stmt = stmt.where(Question.difficulty == difficulty)
        if question_type is not None:
            stmt = stmt.where(Question.question_type == question_type)
        if exclude_ids:
            stmt = stmt.where(Question.id.notin_(exclude_ids))
        candidates = list(self.db.execute(stmt).unique().scalars().all())

        if question_format == QuestionFormat.MULTIPLE_CHOICE:
            candidates = [c for c in candidates if self._has_valid_option_set(c)]
        return candidates

    @staticmethod
    def _has_valid_option_set(question: Question) -> bool:
        active_options = [o for o in question.options if o.active]
        if len(active_options) != 4:
            return False
        return sum(1 for o in active_options if o.is_correct) == 1
