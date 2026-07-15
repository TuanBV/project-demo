"""StudyService: sessions, question selection (random/category/review), and grading.

The multiple-choice flow (select_question default / get_delivered_question /
submit_option_answer) is the default study flow. submit_attempt/_update_progress are the
original FREE_TEXT flow, kept working unchanged for `question_format=FREE_TEXT` rows and
the legacy `/evaluate` endpoint -- they intentionally still use WeightedReviewScheduler so
the multiple-choice mastery rule never contaminates free-text progress rows.
"""

from __future__ import annotations

import json
import random
from dataclasses import asdict
from datetime import UTC, datetime

from app.core.config import get_settings
from app.core.exceptions import NotFoundError, ValidationFailedError
from app.db.models.enums import Classification, Difficulty, LanguageScope, QuestionType, StudyMode
from app.db.models.question import Question
from app.db.models.question_delivery import QuestionDelivery
from app.db.models.question_option import QuestionOption
from app.db.models.study import Attempt, QuestionProgress, StudySession
from app.evaluation.base import AnswerEvaluator, EvaluationResult
from app.evaluation.mc_grader import MultipleChoiceGrader
from app.evaluation.normalizer import TextNormalizer
from app.repositories.question_repository import QuestionRepository
from app.repositories.study_repository import StudyRepository
from app.scheduling.base import ProgressSnapshot, ReviewScheduler
from app.scheduling.mc_scheduler import MultipleChoiceReviewScheduler
from app.scheduling.weighted_scheduler import WeightedReviewScheduler
from app.services.evaluation_service import to_evaluation_data
from app.services.option_order_service import OptionOrderService


class DeliveredQuestion:
    """A question + its options in the exact order shown to the learner for this session."""

    def __init__(self, question: Question, ordered_options: list[QuestionOption]) -> None:
        self.question = question
        self.ordered_options = ordered_options


class StudyService:
    def __init__(
        self,
        study_repository: StudyRepository,
        question_repository: QuestionRepository,
        evaluator: AnswerEvaluator,
        scheduler: ReviewScheduler | None = None,
        normalizer: TextNormalizer | None = None,
        option_order_service: OptionOrderService | None = None,
        mc_grader: MultipleChoiceGrader | None = None,
        mc_scheduler: MultipleChoiceReviewScheduler | None = None,
    ) -> None:
        self._study = study_repository
        self._questions = question_repository
        self._evaluator = evaluator
        self._scheduler = scheduler or WeightedReviewScheduler()
        self._normalizer = normalizer or TextNormalizer()
        self._option_order = option_order_service or OptionOrderService()
        self._mc_grader = mc_grader or MultipleChoiceGrader()
        self._mc_scheduler = mc_scheduler or MultipleChoiceReviewScheduler()
        self._settings = get_settings()

    # ------------------------------------------------------------------
    # Sessions
    # ------------------------------------------------------------------

    def start_session(
        self,
        mode: StudyMode,
        category_id: int | None,
        language_scope: LanguageScope | None,
    ) -> StudySession:
        session = StudySession(
            mode=mode,
            category_id=category_id,
            language_scope=language_scope,
            started_at=datetime.now(UTC),
            total_questions=0,
            answered_questions=0,
            total_score=0.0,
            average_score=0.0,
        )
        session = self._study.create_session(session)
        self._study.commit()
        return session

    def get_session(self, session_id: int) -> StudySession:
        session = self._study.get_session(session_id)
        if session is None:
            raise NotFoundError(f"Study session {session_id} not found")
        return session

    def attempted_question_ids(self, session_id: int) -> list[int]:
        return self._study.attempted_question_ids(session_id)

    def finish_session(self, session_id: int) -> StudySession:
        session = self.get_session(session_id)
        session.finished_at = datetime.now(UTC)
        self._study.commit()
        return session

    # ------------------------------------------------------------------
    # Question listing / selection
    # ------------------------------------------------------------------

    def list_questions(
        self,
        *,
        category_id: int | None = None,
        language_scope: LanguageScope | None = None,
        difficulty: Difficulty | None = None,
        question_type: QuestionType | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list[Question], int]:
        return self._questions.list_filtered(
            category_id=category_id,
            language_scope=language_scope,
            difficulty=difficulty,
            question_type=question_type,
            active_only=True,
            page=page,
            page_size=page_size,
        )

    def get_question(self, question_id: int) -> Question | None:
        return self._questions.get_with_rubric(question_id)

    def select_question(
        self,
        *,
        category_id: int | None = None,
        language_scope: LanguageScope | None = None,
        difficulty: Difficulty | None = None,
        question_type: QuestionType | None = None,
        exclude_ids: list[int] | None = None,
        unseen_only: bool = False,
        weak_only: bool = False,
        mode: StudyMode = StudyMode.RANDOM,
    ) -> Question | None:
        candidates = self._questions.list_candidates(
            category_id=category_id,
            language_scope=language_scope,
            difficulty=difficulty,
            question_type=question_type,
            exclude_ids=exclude_ids or [],
        )
        if not candidates:
            return None

        if unseen_only:
            unseen_ids = set(self._study.unseen_question_ids([c.id for c in candidates]))
            filtered = [c for c in candidates if c.id in unseen_ids]
            candidates = filtered or candidates

        if weak_only or mode == StudyMode.REVIEW:
            weak_ids = set(
                self._study.weak_question_ids(self._settings.mostly_correct_score_threshold)
            )
            if weak_only:
                filtered = [c for c in candidates if c.id in weak_ids]
                candidates = filtered or candidates

        if mode == StudyMode.REVIEW:
            return self._pick_by_priority(candidates)

        return random.choice(candidates)

    def _pick_by_priority(self, candidates: list[Question]) -> Question:
        now = datetime.now(UTC)
        weighted: list[tuple[float, Question]] = []
        for candidate in candidates:
            progress = self._study.get_progress(candidate.id)
            snapshot = self._to_snapshot(progress)
            priority = self._mc_scheduler.calculate_priority(snapshot, now)
            weighted.append((priority, candidate))

        total_priority = sum(p for p, _ in weighted)
        if total_priority <= 0:
            return random.choice(candidates)
        pick = random.uniform(0, total_priority)
        cumulative = 0.0
        for priority, candidate in weighted:
            cumulative += priority
            if pick <= cumulative:
                return candidate
        return weighted[-1][1]

    # ------------------------------------------------------------------
    # Multiple-choice delivery + answer submission (default study flow)
    # ------------------------------------------------------------------

    def get_delivered_question(self, session_id: int, question_id: int) -> DeliveredQuestion:
        """Fetch a question with options in the order shown for this session, creating
        and persisting that order on first delivery so a page refresh replays it exactly
        (spec section 8)."""
        question = self._questions.get_with_rubric(question_id)
        if question is None:
            raise NotFoundError(f"Question {question_id} not found")

        active_options = [o for o in question.options if o.active]
        delivery = self._study.get_delivery(session_id, question_id)
        if delivery is not None:
            order = json.loads(delivery.option_order_json)["option_ids"]
            by_id = {o.id: o for o in active_options}
            ordered = [by_id[oid] for oid in order if oid in by_id]
        else:
            ordered = self._option_order.shuffle_options(
                question_id, session_id, str(session_id), active_options
            )
            delivery = QuestionDelivery(
                session_id=session_id,
                question_id=question_id,
                option_order_json=json.dumps({"option_ids": [o.id for o in ordered]}),
                created_at=datetime.now(UTC),
            )
            self._study.create_delivery(delivery)
            self._study.commit()

        return DeliveredQuestion(question=question, ordered_options=ordered)

    def submit_option_answer(
        self,
        session_id: int,
        question_id: int,
        selected_option_id: int,
        response_time_seconds: float | None,
    ) -> tuple[Attempt, QuestionOption, list[QuestionOption], str | None]:
        session = self.get_session(session_id)
        if session.finished_at is not None:
            raise ValidationFailedError("Phiên luyện tập đã kết thúc")

        question = self._questions.get_with_rubric(question_id)
        if question is None or not question.active:
            raise NotFoundError(f"Question {question_id} not found")

        if self._study.get_attempt_for_question(session_id, question_id) is not None:
            raise ValidationFailedError("Câu hỏi này đã được trả lời trong phiên luyện tập này")

        delivery = self._study.get_delivery(session_id, question_id)
        if delivery is None:
            raise ValidationFailedError(
                "Câu hỏi chưa được cấp cho phiên này, vui lòng lấy câu hỏi trước khi trả lời"
            )
        delivered_ids = set(json.loads(delivery.option_order_json)["option_ids"])
        if selected_option_id not in delivered_ids:
            raise ValidationFailedError("Đáp án không nằm trong danh sách đã hiển thị")

        selected_option = next((o for o in question.options if o.id == selected_option_id), None)
        if selected_option is None:
            raise NotFoundError(f"Option {selected_option_id} not found")

        correct_option = next((o for o in question.options if o.is_correct), None)
        if correct_option is None:
            raise ValidationFailedError("Câu hỏi chưa có đáp án đúng được cấu hình")

        grade = self._mc_grader.grade(selected_option_id, correct_option.id)

        by_id = {o.id: o for o in question.options}
        ordered_ids = json.loads(delivery.option_order_json)["option_ids"]
        ordered_options = [by_id[oid] for oid in ordered_ids if oid in by_id]

        attempt = Attempt(
            session_id=session_id,
            question_id=question_id,
            selected_option_id=selected_option_id,
            correct_option_id=correct_option.id,
            is_correct=grade.is_correct,
            answer_order_json=json.dumps({"option_ids": ordered_ids}),
            score=grade.score,
            classification=Classification(grade.classification),
            response_time_seconds=response_time_seconds,
            created_at=datetime.now(UTC),
        )
        attempt = self._study.create_attempt(attempt)

        session.answered_questions += 1
        session.total_score += grade.score
        session.average_score = session.total_score / session.answered_questions
        session.total_questions = max(session.total_questions, session.answered_questions)

        self._update_mc_progress(question_id, grade.is_correct, selected_option_id)
        self._study.commit()
        explanation = question.explanation or correct_option.explanation
        return attempt, correct_option, ordered_options, explanation

    def _update_mc_progress(
        self, question_id: int, is_correct: bool, selected_option_id: int
    ) -> QuestionProgress:
        progress = self._study.get_progress(question_id)
        now = datetime.now(UTC)
        score = 100.0 if is_correct else 0.0
        if progress is None:
            progress = QuestionProgress(
                question_id=question_id,
                attempt_count=0,
                correct_count=0,
                incorrect_count=0,
                average_score=0.0,
                accuracy=0.0,
                best_score=0.0,
                last_score=0.0,
                current_correct_streak=0,
                best_correct_streak=0,
                mastery_level="NEW",
                created_at=now,
                updated_at=now,
            )

        progress.attempt_count += 1
        if is_correct:
            progress.correct_count += 1
            progress.current_correct_streak += 1
            progress.best_correct_streak = max(
                progress.best_correct_streak, progress.current_correct_streak
            )
        else:
            progress.incorrect_count += 1
            progress.current_correct_streak = 0

        progress.average_score = (
            progress.average_score * (progress.attempt_count - 1) + score
        ) / progress.attempt_count
        progress.accuracy = progress.correct_count / progress.attempt_count * 100
        progress.best_score = max(progress.best_score, score)
        progress.last_score = score
        progress.last_is_correct = is_correct
        progress.last_selected_option_id = selected_option_id

        snapshot = self._to_snapshot(progress)
        assert snapshot is not None
        schedule = self._mc_scheduler.calculate_next_review(snapshot, score, now)
        progress.mastery_level = schedule.mastery_level
        progress.next_review_at = schedule.next_review_at
        progress.last_reviewed_at = now
        progress.updated_at = now

        return self._study.save_progress(progress)

    # ------------------------------------------------------------------
    # Legacy FREE_TEXT flow (kept working, not used by the default MC study screen)
    # ------------------------------------------------------------------

    def submit_attempt(
        self,
        session_id: int,
        question_id: int,
        submitted_answer: str,
        response_time_seconds: float | None,
    ) -> tuple[Attempt, EvaluationResult]:
        session = self.get_session(session_id)
        question = self._questions.get_with_rubric(question_id)
        if question is None:
            raise NotFoundError(f"Question {question_id} not found")

        data = to_evaluation_data(question)
        result = self._evaluator.evaluate(data, submitted_answer)
        normalized = self._normalizer.normalize(submitted_answer)

        attempt = Attempt(
            session_id=session_id,
            question_id=question_id,
            submitted_answer=submitted_answer,
            normalized_answer=normalized.with_diacritics,
            score=result.score,
            classification=Classification(result.classification),
            evaluation_json=json.dumps(asdict(result), ensure_ascii=False),
            response_time_seconds=response_time_seconds,
            created_at=datetime.now(UTC),
        )
        attempt = self._study.create_attempt(attempt)

        session.answered_questions += 1
        session.total_score += result.score
        session.average_score = session.total_score / session.answered_questions
        session.total_questions = max(session.total_questions, session.answered_questions)

        self._update_progress(question_id, result.score)
        self._study.commit()
        return attempt, result

    def _update_progress(self, question_id: int, score: float) -> QuestionProgress:
        progress = self._study.get_progress(question_id)
        now = datetime.now(UTC)
        if progress is None:
            progress = QuestionProgress(
                question_id=question_id,
                attempt_count=0,
                correct_count=0,
                average_score=0.0,
                best_score=0.0,
                last_score=0.0,
                mastery_level="NEW",
                created_at=now,
                updated_at=now,
            )

        progress.attempt_count += 1
        if score >= self._settings.correct_score_threshold:
            progress.correct_count += 1
        else:
            progress.incorrect_count += 1
        progress.average_score = (
            progress.average_score * (progress.attempt_count - 1) + score
        ) / progress.attempt_count
        progress.best_score = max(progress.best_score, score)
        progress.last_score = score

        snapshot = self._to_snapshot(progress)
        assert snapshot is not None  # progress is never None at this point
        schedule = self._scheduler.calculate_next_review(snapshot, score, now)
        progress.mastery_level = schedule.mastery_level
        progress.next_review_at = schedule.next_review_at
        progress.last_reviewed_at = now
        progress.updated_at = now

        return self._study.save_progress(progress)

    @staticmethod
    def _to_snapshot(progress: QuestionProgress | None) -> ProgressSnapshot | None:
        if progress is None:
            return None
        return ProgressSnapshot(
            attempt_count=progress.attempt_count,
            correct_count=progress.correct_count,
            average_score=progress.average_score,
            best_score=progress.best_score,
            last_score=progress.last_score,
            mastery_level=progress.mastery_level,
            last_reviewed_at=progress.last_reviewed_at,
            next_review_at=progress.next_review_at,
            incorrect_count=progress.incorrect_count,
            accuracy=progress.accuracy,
            last_is_correct=progress.last_is_correct,
            current_correct_streak=progress.current_correct_streak,
        )
