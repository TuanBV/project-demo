"""MultipleChoiceReviewScheduler: priority formula + mastery rule for the MC study flow
(spec sections 16-17). Kept separate from WeightedReviewScheduler (still used by legacy
FREE_TEXT review) so neither formula change affects the other's tests.
"""

from __future__ import annotations

import random
from datetime import datetime, timedelta

from app.scheduling.base import ProgressSnapshot, ReviewSchedule

_OVERDUE_NORMALIZATION_DAYS = 7.0
_LOW_ATTEMPT_NORMALIZATION = 5.0
_MASTERY_MIN_CORRECT_STREAK_FOR_MASTERED = 3
_LEARNING_ACCURACY_CEILING = 60.0
_FAMILIAR_ACCURACY_CEILING = 85.0

_MASTERY_INTERVAL_DAYS = {
    "NEW": 1,
    "LEARNING": 1,
    "FAMILIAR": 4,
    "MASTERED": 14,
}


def _clamp01(value: float) -> float:
    return max(0.0, min(1.0, value))


class MultipleChoiceReviewScheduler:
    def calculate_priority(
        self, progress: ProgressSnapshot | None, current_time: datetime
    ) -> float:
        if progress is None or progress.attempt_count == 0:
            incorrect_rate = 1.0
            recently_incorrect = 1.0
            overdue_factor = 1.0
            low_attempt_factor = 1.0
        else:
            incorrect_rate = _clamp01(progress.incorrect_count / progress.attempt_count)
            recently_incorrect = 1.0 if progress.last_is_correct is False else 0.0
            if progress.next_review_at is None:
                overdue_factor = 1.0
            else:
                overdue_days = (current_time - progress.next_review_at).total_seconds() / 86400
                overdue_factor = _clamp01(overdue_days / _OVERDUE_NORMALIZATION_DAYS)
            low_attempt_factor = _clamp01(1 - progress.attempt_count / _LOW_ATTEMPT_NORMALIZATION)

        random_factor = random.random()

        return (
            0.45 * incorrect_rate
            + 0.25 * recently_incorrect
            + 0.15 * overdue_factor
            + 0.10 * low_attempt_factor
            + 0.05 * random_factor
        )

    def calculate_mastery_level(self, accuracy: float, correct_count: int) -> str:
        if correct_count == 0 and accuracy == 0.0:
            return "NEW"
        if accuracy < _LEARNING_ACCURACY_CEILING:
            return "LEARNING"
        if accuracy < _FAMILIAR_ACCURACY_CEILING:
            return "FAMILIAR"
        if correct_count >= _MASTERY_MIN_CORRECT_STREAK_FOR_MASTERED:
            return "MASTERED"
        return "FAMILIAR"

    def calculate_next_review(
        self, progress: ProgressSnapshot, score: float, current_time: datetime
    ) -> ReviewSchedule:
        mastery_level = self.calculate_mastery_level(progress.accuracy, progress.correct_count)
        interval_days = _MASTERY_INTERVAL_DAYS[mastery_level]
        return ReviewSchedule(
            next_review_at=current_time + timedelta(days=interval_days),
            mastery_level=mastery_level,
        )
