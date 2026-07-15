"""ProgressService: dashboard aggregates, weak-question lookup, and history."""

from __future__ import annotations

import json

from app.core.config import get_settings
from app.core.exceptions import NotFoundError
from app.db.models.enums import Difficulty
from app.db.models.study import Attempt
from app.repositories.category_repository import CategoryRepository
from app.repositories.question_repository import QuestionRepository
from app.repositories.study_repository import StudyRepository
from app.schemas.study import (
    AnsweredOptionResult,
    CategoryProgress,
    DifficultyProgress,
    HistoryItemResponse,
    MostMissedQuestion,
    MostSelectedWrongOption,
    WeakQuestionItem,
)


class ProgressService:
    def __init__(
        self,
        study_repository: StudyRepository,
        question_repository: QuestionRepository,
        category_repository: CategoryRepository | None = None,
    ) -> None:
        self._study = study_repository
        self._questions = question_repository
        self._categories = category_repository
        self._settings = get_settings()

    def overview(self) -> dict:
        _, total_questions = self._questions.list_filtered(active_only=True, page=1, page_size=1)
        progresses = self._study.list_all_progress()
        attempted = len(progresses)
        mastered = sum(1 for p in progresses if p.mastery_level == "MASTERED")
        average_score = sum(p.average_score for p in progresses) / attempted if attempted else 0.0

        total_attempts = sum(p.attempt_count for p in progresses)
        correct_count = sum(p.correct_count for p in progresses)
        incorrect_count = sum(p.incorrect_count for p in progresses)
        accuracy = correct_count / total_attempts * 100 if total_attempts else 0.0
        current_streak, best_streak = self._compute_streaks()

        return {
            "total_questions": total_questions,
            "attempted_questions": attempted,
            "unattempted_questions": max(0, total_questions - attempted),
            "mastered_questions": mastered,
            "average_score": round(average_score, 2),
            "total_attempts": total_attempts,
            "correct_count": correct_count,
            "incorrect_count": incorrect_count,
            "accuracy": round(accuracy, 2),
            "current_streak": current_streak,
            "best_streak": best_streak,
            "categories": self.categories_progress(),
            "difficulty": self.difficulty_progress(),
            "most_missed_questions": self.most_missed_questions(),
            "most_selected_wrong_options": self.most_selected_wrong_options(),
        }

    def _compute_streaks(self) -> tuple[int, int]:
        attempts = self._study.list_mc_attempts_chronological()
        best = 0
        running = 0
        for attempt in attempts:
            if attempt.is_correct:
                running += 1
                best = max(best, running)
            else:
                running = 0
        current = 0
        for attempt in reversed(attempts):
            if attempt.is_correct:
                current += 1
            else:
                break
        return current, best

    def categories_progress(self) -> list[CategoryProgress]:
        if self._categories is None:
            return []
        categories = self._categories.list_all(active_only=True)
        all_progress = self._study.list_all_progress()
        result: list[CategoryProgress] = []
        for category in categories:
            _, total = self._questions.list_filtered(
                category_id=category.id, active_only=True, page=1, page_size=1
            )
            question_ids = {q.id for q in self._questions.list_candidates(category_id=category.id)}
            category_progress = [p for p in all_progress if p.question_id in question_ids]
            attempted = len(category_progress)
            avg = sum(p.average_score for p in category_progress) / attempted if attempted else 0.0
            result.append(
                CategoryProgress(
                    category_id=category.id,
                    category_name=category.name,
                    total_questions=total,
                    attempted_questions=attempted,
                    average_score=round(avg, 2),
                )
            )
        return result

    def difficulty_progress(self) -> list[DifficultyProgress]:
        all_progress = {p.question_id: p for p in self._study.list_all_progress()}
        result: list[DifficultyProgress] = []
        for difficulty in (Difficulty.EASY, Difficulty.MEDIUM, Difficulty.HARD):
            questions, total = self._questions.list_filtered(
                difficulty=difficulty, active_only=True, page=1, page_size=1000
            )
            attempted = [q for q in questions if q.id in all_progress]
            correct = sum(all_progress[q.id].correct_count for q in attempted)
            attempts = sum(all_progress[q.id].attempt_count for q in attempted)
            accuracy = correct / attempts * 100 if attempts else 0.0
            result.append(
                DifficultyProgress(
                    difficulty=difficulty.value,
                    total_questions=total,
                    attempted_questions=len(attempted),
                    accuracy=round(accuracy, 2),
                )
            )
        return result

    def most_missed_questions(self, limit: int = 10) -> list[MostMissedQuestion]:
        rows = self._study.most_missed_question_ids(limit)
        items: list[MostMissedQuestion] = []
        for question_id, incorrect_count, attempt_count in rows:
            question = self._questions.get(question_id)
            if question is None:
                continue
            items.append(
                MostMissedQuestion(
                    question_id=question_id,
                    content=question.content,
                    category_name=question.category.name if question.category else "",
                    incorrect_count=incorrect_count,
                    attempt_count=attempt_count,
                )
            )
        return items

    def most_selected_wrong_options(self, limit: int = 10) -> list[MostSelectedWrongOption]:
        rows = self._study.most_selected_wrong_options(limit)
        items: list[MostSelectedWrongOption] = []
        for question_id, option_id, count in rows:
            question = self._questions.get_with_rubric(question_id)
            if question is None:
                continue
            option = next((o for o in question.options if o.id == option_id), None)
            items.append(
                MostSelectedWrongOption(
                    question_id=question_id,
                    question_content=question.content,
                    option_id=option_id,
                    option_content=option.content if option else "",
                    selected_count=count,
                )
            )
        return items

    def weak_questions(self, limit: int = 20) -> list[WeakQuestionItem]:
        weak_ids = self._study.weak_question_ids(self._settings.mostly_correct_score_threshold)
        items: list[WeakQuestionItem] = []
        for question_id in weak_ids[:limit]:
            question = self._questions.get(question_id)
            if question is None:
                continue
            progress = self._study.get_progress(question_id)
            items.append(
                WeakQuestionItem(
                    question_id=question_id,
                    content=question.content,
                    category_name=question.category.name if question.category else "",
                    average_score=progress.average_score if progress else 0.0,
                    attempt_count=progress.attempt_count if progress else 0,
                )
            )
        return items

    def history(self, page: int = 1, page_size: int = 20) -> tuple[list[HistoryItemResponse], int]:
        attempts, total = self._study.list_history(page, page_size)
        items: list[HistoryItemResponse] = []
        for attempt in attempts:
            items.append(self._to_history_item(attempt))
        return items, total

    def _to_history_item(self, attempt: Attempt) -> HistoryItemResponse:
        question = self._questions.get_with_rubric(attempt.question_id)
        options_snapshot: list[AnsweredOptionResult] | None = None
        explanation: str | None = None

        if attempt.selected_option_id is not None and question is not None:
            options_by_id = {o.id: o for o in question.options}
            order = (
                json.loads(attempt.answer_order_json)["option_ids"]
                if attempt.answer_order_json
                else list(options_by_id.keys())
            )
            options_snapshot = [
                AnsweredOptionResult(
                    id=oid,
                    content=options_by_id[oid].content,
                    is_selected=(oid == attempt.selected_option_id),
                    is_correct=(oid == attempt.correct_option_id),
                )
                for oid in order
                if oid in options_by_id
            ]
            correct_option = options_by_id.get(attempt.correct_option_id or -1)
            explanation = correct_option.explanation if correct_option else None

        return HistoryItemResponse(
            attempt_id=attempt.id,
            question_id=attempt.question_id,
            question_content=question.content if question else "",
            category_name=question.category.name if question and question.category else "",
            score=attempt.score,
            classification=attempt.classification.value,
            is_correct=attempt.is_correct,
            selected_option_id=attempt.selected_option_id,
            correct_option_id=attempt.correct_option_id,
            options=options_snapshot,
            explanation=explanation,
            response_time_seconds=attempt.response_time_seconds,
            created_at=attempt.created_at,
        )

    def get_attempt(self, attempt_id: int) -> Attempt:
        attempt = self._study.get_attempt(attempt_id)
        if attempt is None:
            raise NotFoundError(f"Attempt {attempt_id} not found")
        return attempt
