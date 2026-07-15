from __future__ import annotations

from datetime import UTC, datetime

from app.scheduling.base import ProgressSnapshot
from app.scheduling.mc_scheduler import MultipleChoiceReviewScheduler

scheduler = MultipleChoiceReviewScheduler()


def _snapshot(**overrides: object) -> ProgressSnapshot:
    defaults: dict[str, object] = dict(
        attempt_count=0,
        correct_count=0,
        average_score=0.0,
        best_score=0.0,
        last_score=0.0,
        mastery_level="NEW",
        last_reviewed_at=None,
        next_review_at=None,
        incorrect_count=0,
        accuracy=0.0,
        last_is_correct=None,
        current_correct_streak=0,
    )
    defaults.update(overrides)
    return ProgressSnapshot(**defaults)  # type: ignore[arg-type]


def test_new_question_gets_high_priority() -> None:
    priority = scheduler.calculate_priority(None, datetime.now(UTC))
    assert priority > 0.9


def test_mastery_new_with_no_attempts() -> None:
    assert scheduler.calculate_mastery_level(0.0, 0) == "NEW"


def test_mastery_learning_below_60_accuracy() -> None:
    assert scheduler.calculate_mastery_level(50.0, 2) == "LEARNING"


def test_mastery_familiar_between_60_and_85() -> None:
    assert scheduler.calculate_mastery_level(70.0, 4) == "FAMILIAR"


def test_mastery_not_mastered_after_single_correct_answer() -> None:
    # 100% accuracy but only 1 correct attempt must not jump straight to MASTERED.
    assert scheduler.calculate_mastery_level(100.0, 1) == "FAMILIAR"


def test_mastery_mastered_requires_high_accuracy_and_three_correct() -> None:
    assert scheduler.calculate_mastery_level(90.0, 3) == "MASTERED"


def test_incorrect_answers_increase_priority() -> None:
    now = datetime.now(UTC)
    weak = _snapshot(attempt_count=10, correct_count=2, incorrect_count=8, accuracy=20.0)
    strong = _snapshot(attempt_count=10, correct_count=9, incorrect_count=1, accuracy=90.0)
    # Compare the deterministic components only (random factor is only 5% weight).
    weak_priority = scheduler.calculate_priority(weak, now)
    strong_priority = scheduler.calculate_priority(strong, now)
    assert weak_priority > strong_priority
