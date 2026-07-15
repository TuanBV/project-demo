"""WeightedReviewScheduler: MVP implementation of ReviewScheduler (spec section 15).

Priority formula is exactly the one from the spec. calculate_next_review uses a simple
fixed-interval mastery ladder -- intentionally simple so it can be swapped for SM-2/FSRS
later without touching any caller (they only depend on the ReviewScheduler Protocol).
"""

from __future__ import annotations

import random
from datetime import datetime, timedelta

from app.scheduling.base import ProgressSnapshot, ReviewSchedule

_MASTERY_LEVELS = ["NEW", "LEARNING", "REVIEWING", "MASTERED"]
_MASTERY_INTERVAL_DAYS = {"NEW": 1, "LEARNING": 3, "REVIEWING": 7, "MASTERED": 21}
_OVERDUE_NORMALIZATION_DAYS = 7.0
_LOW_ATTEMPT_NORMALIZATION = 5.0

_CORRECT_THRESHOLD = 85.0
_MOSTLY_CORRECT_THRESHOLD = 65.0
_PARTIALLY_CORRECT_THRESHOLD = 40.0


def _clamp01(value: float) -> float:
    return max(0.0, min(1.0, value))


class WeightedReviewScheduler:
    def calculate_priority(
        self, progress: ProgressSnapshot | None, current_time: datetime
    ) -> float:
        if progress is None or progress.attempt_count == 0:
            incorrect_factor = 1.0
            low_mastery_factor = 1.0
            overdue_factor = 1.0
            low_attempt_factor = 1.0
        else:
            incorrect_factor = _clamp01(1 - progress.correct_count / progress.attempt_count)
            mastery_index = (
                _MASTERY_LEVELS.index(progress.mastery_level)
                if progress.mastery_level in _MASTERY_LEVELS
                else 0
            )
            low_mastery_factor = _clamp01(1 - mastery_index / (len(_MASTERY_LEVELS) - 1))
            if progress.next_review_at is None:
                overdue_factor = 1.0
            else:
                overdue_days = (current_time - progress.next_review_at).total_seconds() / 86400
                overdue_factor = _clamp01(overdue_days / _OVERDUE_NORMALIZATION_DAYS)
            low_attempt_factor = _clamp01(1 - progress.attempt_count / _LOW_ATTEMPT_NORMALIZATION)

        random_factor = random.random()

        return (
            0.40 * incorrect_factor
            + 0.25 * low_mastery_factor
            + 0.20 * overdue_factor
            + 0.10 * low_attempt_factor
            + 0.05 * random_factor
        )

    def calculate_next_review(
        self, progress: ProgressSnapshot, score: float, current_time: datetime
    ) -> ReviewSchedule:
        current_index = (
            _MASTERY_LEVELS.index(progress.mastery_level)
            if progress.mastery_level in _MASTERY_LEVELS
            else 0
        )

        if score >= _CORRECT_THRESHOLD:
            next_index = min(current_index + 1, len(_MASTERY_LEVELS) - 1)
        elif score >= _MOSTLY_CORRECT_THRESHOLD:
            next_index = current_index
        elif score >= _PARTIALLY_CORRECT_THRESHOLD:
            next_index = max(current_index - 1, 0)
        else:
            next_index = 0

        new_level = _MASTERY_LEVELS[next_index]
        interval_days = _MASTERY_INTERVAL_DAYS[new_level]
        return ReviewSchedule(
            next_review_at=current_time + timedelta(days=interval_days),
            mastery_level=new_level,
        )
