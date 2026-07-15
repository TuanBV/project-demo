"""OptionOrderService: deterministic per-delivery option shuffling (spec section 8).

Shuffling happens server-side, never in JavaScript. The shuffle is seeded from
(question_id, session_id, attempt_token) so it is reproducible without a DB round-trip;
StudyService additionally persists the resulting order in QuestionDelivery so a page
refresh replays the exact same order even if this function were ever called again.
"""

from __future__ import annotations

import random
from typing import TypeVar

T = TypeVar("T")


class OptionOrderService:
    def shuffle_options(
        self,
        question_id: int,
        session_id: int,
        attempt_token: str,
        options: list[T],
    ) -> list[T]:
        seed_key = f"{question_id}:{session_id}:{attempt_token}"
        rng = random.Random(seed_key)
        shuffled = list(options)
        rng.shuffle(shuffled)
        return shuffled
