"""ReviewScheduler protocol (spec section 15). Pure functions, no DB/FastAPI imports so a
future SM-2/FSRS implementation can be dropped in without touching callers.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Protocol


@dataclass(frozen=True)
class ProgressSnapshot:
    attempt_count: int
    correct_count: int
    average_score: float
    best_score: float
    last_score: float
    mastery_level: str
    last_reviewed_at: datetime | None
    next_review_at: datetime | None
    # Multiple-choice specific (unused by the legacy WeightedReviewScheduler).
    incorrect_count: int = 0
    accuracy: float = 0.0
    last_is_correct: bool | None = None
    current_correct_streak: int = 0


@dataclass(frozen=True)
class ReviewSchedule:
    next_review_at: datetime
    mastery_level: str


class ReviewScheduler(Protocol):
    def calculate_priority(
        self, progress: ProgressSnapshot | None, current_time: datetime
    ) -> float: ...

    def calculate_next_review(
        self, progress: ProgressSnapshot, score: float, current_time: datetime
    ) -> ReviewSchedule: ...
