"""Distractor generation for multiple-choice questions (spec section 9.1).

Honest MVP scope: without an LLM, we cannot reliably fabricate plausible-but-wrong answers
from scratch. RuleBasedDistractorGenerator therefore tries two low-risk strategies —
confusable-term swap and borrowing real correct answers from sibling questions — and falls
back to an explicit placeholder (never a fabricated-looking "real" answer) when neither
strategy yields enough distinct candidates. Placeholder output must always drive
`needs_review=True` + `active=False` upstream (see QuestionImportService).
"""

from __future__ import annotations

import re
from typing import Protocol

from app.evaluation.normalizer import TextNormalizer

PLACEHOLDER_PREFIX = "Cần quản trị viên nhập đáp án sai"

# Small, hand-curated table of commonly-confused Junior-Dev technical term pairs. Swapping
# one for the other in the correct answer yields a distractor that reads naturally but is
# factually wrong -- a standard, low-risk item-bank technique.
_CONFUSABLE_PAIRS: dict[str, str] = {
    "compiler": "interpreter",
    "interpreter": "compiler",
    "mutable": "immutable",
    "immutable": "mutable",
    "list": "tuple",
    "tuple": "list",
    "thread": "process",
    "process": "thread",
    "primary key": "foreign key",
    "foreign key": "primary key",
    "inheritance": "polymorphism",
    "polymorphism": "inheritance",
    "encapsulation": "abstraction",
    "abstraction": "encapsulation",
    "synchronous": "asynchronous",
    "asynchronous": "synchronous",
    "stack": "queue",
    "queue": "stack",
    "get": "post",
    "post": "get",
    "unit test": "integration test",
    "integration test": "unit test",
    "merge": "rebase",
    "rebase": "merge",
}
_CONFUSABLE_RE = re.compile(
    "|".join(re.escape(term) for term in sorted(_CONFUSABLE_PAIRS, key=len, reverse=True)),
    re.IGNORECASE,
)


def is_placeholder_distractor(text: str) -> bool:
    return text.strip().startswith(PLACEHOLDER_PREFIX)


class DistractorGenerator(Protocol):
    def generate(
        self,
        question: str,
        correct_answer: str,
        context: list[str] | None = None,
        count: int = 3,
    ) -> list[str]: ...


class RuleBasedDistractorGenerator:
    def __init__(self, normalizer: TextNormalizer | None = None) -> None:
        self._normalizer = normalizer or TextNormalizer()

    def generate(
        self,
        question: str,
        correct_answer: str,
        context: list[str] | None = None,
        count: int = 3,
    ) -> list[str]:
        distractors: list[str] = []

        swapped = self._swap_confusable_terms(correct_answer)
        if swapped and self._is_distinct(swapped, correct_answer, distractors):
            distractors.append(swapped)

        for candidate in context or []:
            if len(distractors) >= count:
                break
            candidate = candidate.strip()
            if candidate and self._is_distinct(candidate, correct_answer, distractors):
                distractors.append(candidate)

        placeholder_index = 1
        while len(distractors) < count:
            distractors.append(f"{PLACEHOLDER_PREFIX} #{placeholder_index}")
            placeholder_index += 1

        return distractors[:count]

    def _swap_confusable_terms(self, text: str) -> str | None:
        match = _CONFUSABLE_RE.search(text)
        if not match:
            return None
        term = match.group(0)
        replacement = _CONFUSABLE_PAIRS[term.lower()]
        if term[:1].isupper():
            replacement = replacement[:1].upper() + replacement[1:]
        return text[: match.start()] + replacement + text[match.end() :]

    def _is_distinct(self, candidate: str, correct_answer: str, existing: list[str]) -> bool:
        candidate_key = self._normalizer.normalize(candidate).without_diacritics
        if not candidate_key:
            return False
        if candidate_key == self._normalizer.normalize(correct_answer).without_diacritics:
            return False
        for other in existing:
            if candidate_key == self._normalizer.normalize(other).without_diacritics:
                return False
        return True
