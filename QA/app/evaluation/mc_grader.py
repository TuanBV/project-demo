"""MultipleChoiceGrader: trivial selected-vs-correct grading for MC questions.

Deliberately has zero dependency on TextNormalizer/KeywordMatcher/ContradictionDetector --
multiple-choice grading is an ID comparison, not a text-similarity problem. The backend
never trusts an `is_correct` flag coming from the client; it always re-derives the result
from the option row fetched from the database.
"""

from __future__ import annotations

from dataclasses import dataclass

CORRECT_SCORE = 100.0
INCORRECT_SCORE = 0.0


@dataclass(frozen=True)
class McGradeResult:
    is_correct: bool
    score: float
    classification: str


class MultipleChoiceGrader:
    def grade(self, selected_option_id: int, correct_option_id: int) -> McGradeResult:
        is_correct = selected_option_id == correct_option_id
        return McGradeResult(
            is_correct=is_correct,
            score=CORRECT_SCORE if is_correct else INCORRECT_SCORE,
            classification="CORRECT" if is_correct else "INCORRECT",
        )
