"""KeywordMatcher: finds the best match of a keyword inside a normalized answer.

Implements the four match types from the spec:
- EXACT: normalized keyword must equal a whole token/phrase span, not a substring.
- CONTAINS: keyword phrase appears as a word-boundary-safe substring.
- FUZZY: RapidFuzz partial-ratio against sliding windows of the answer, thresholded.
- ALIAS: matches after TextNormalizer's alias canonicalization already ran (so it is
  effectively CONTAINS on the canonicalized text) -- kept as an explicit type so callers
  can label/report it and tune minimum_similarity per keyword.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from rapidfuzz import fuzz

from app.core.config import get_settings

_MIN_EXACT_TOKEN_LENGTH = 3


@dataclass(frozen=True)
class MatchOutcome:
    matched: bool
    similarity: float
    matched_span: str | None


def _word_boundary_pattern(phrase: str) -> re.Pattern[str]:
    escaped = re.escape(phrase.strip())
    return re.compile(rf"(?<!\w){escaped}(?!\w)", re.IGNORECASE)


def _contains(haystack: str, phrase: str) -> MatchOutcome:
    phrase = phrase.strip()
    if not phrase:
        return MatchOutcome(False, 0.0, None)
    pattern = _word_boundary_pattern(phrase)
    match = pattern.search(haystack)
    if match:
        return MatchOutcome(True, 100.0, match.group(0))
    return MatchOutcome(False, 0.0, None)


def _exact(haystack: str, phrase: str) -> MatchOutcome:
    phrase = phrase.strip()
    tokens = haystack.split()
    phrase_tokens = phrase.split()
    if not phrase_tokens:
        return MatchOutcome(False, 0.0, None)
    window = len(phrase_tokens)
    for i in range(len(tokens) - window + 1):
        if tokens[i : i + window] == phrase_tokens:
            return MatchOutcome(True, 100.0, " ".join(phrase_tokens))
    return MatchOutcome(False, 0.0, None)


def _fuzzy(haystack: str, phrase: str, minimum_similarity: float) -> MatchOutcome:
    phrase = phrase.strip()
    if not phrase:
        return MatchOutcome(False, 0.0, None)
    tokens = haystack.split()
    window = max(len(phrase.split()), 1)
    best_score = 0.0
    best_span: str | None = None
    for i in range(len(tokens) - window + 1):
        candidate = " ".join(tokens[i : i + window])
        score = fuzz.ratio(phrase, candidate)
        if score > best_score:
            best_score = score
            best_span = candidate
    if not tokens:
        best_score = fuzz.ratio(phrase, haystack)
        best_span = haystack
    matched = best_score >= minimum_similarity
    return MatchOutcome(matched, best_score, best_span if matched else None)


class KeywordMatcher:
    """Stateless matcher; thresholds come from app config so they stay tunable."""

    def __init__(self) -> None:
        self._settings = get_settings()

    def match(
        self,
        normalized_answer_with_diacritics: str,
        normalized_answer_without_diacritics: str,
        keyword: str,
        match_type: str,
        minimum_similarity: float = 80.0,
    ) -> MatchOutcome:
        keyword = keyword.strip().lower()
        if not keyword:
            return MatchOutcome(False, 0.0, None)

        # Short keywords are ambiguous as substrings ("is" inside "list"), so force EXACT.
        effective_type = match_type
        if len(keyword.replace(" ", "")) < _MIN_EXACT_TOKEN_LENGTH and match_type == "CONTAINS":
            effective_type = "EXACT"

        candidates = [normalized_answer_with_diacritics, normalized_answer_without_diacritics]
        best = MatchOutcome(False, 0.0, None)
        for haystack in candidates:
            if effective_type in ("CONTAINS", "ALIAS"):
                outcome = _contains(haystack, keyword)
            elif effective_type == "EXACT":
                outcome = _exact(haystack, keyword)
            elif effective_type == "FUZZY":
                outcome = _fuzzy(haystack, keyword, minimum_similarity)
            else:
                outcome = MatchOutcome(False, 0.0, None)
            if outcome.matched and outcome.similarity > best.similarity:
                best = outcome
            if best.matched and best.similarity >= 100.0:
                break
        return best

    def fuzzy_score_bucket(self, similarity: float) -> float:
        """Map a raw fuzzy similarity to the partial-credit fraction per spec 12.1."""
        settings = self._settings
        if similarity >= settings.fuzzy_full_score_threshold:
            return 1.0
        if similarity >= settings.fuzzy_partial_high_threshold:
            return 0.75
        if similarity >= settings.fuzzy_partial_low_threshold:
            return 0.5
        return 0.0
