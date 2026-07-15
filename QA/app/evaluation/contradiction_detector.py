"""Detects contradictory statements in a submitted answer (spec section 12.3).

Applies a negative-pattern guard (spec section 13, item 2): a contradiction rule that
matches only because it sits right after a negation word ("không", "chưa", "not", ...)
is suppressed, since that usually means the learner correctly negated the wrong claim
(e.g. "volatile KHÔNG đảm bảo count++ là atomic" must not be flagged as the contradiction
"volatile đảm bảo count++ là atomic").
"""

from __future__ import annotations

from dataclasses import dataclass

from app.evaluation.base import ContradictionHit, ContradictionRuleData
from app.evaluation.matcher import KeywordMatcher
from app.evaluation.normalizer import strip_diacritics

_NEGATION_WORDS = {"khong", "chua", "chang", "not", "never", "no", "deny", "denies"}
_NEGATION_WINDOW = 3


@dataclass(frozen=True)
class ContradictionOutcome:
    hits: list[ContradictionHit]
    total_penalty: float
    maximum_score_cap: float | None


class ContradictionDetector:
    def __init__(self, matcher: KeywordMatcher | None = None) -> None:
        self._matcher = matcher or KeywordMatcher()

    def detect(
        self,
        rules: list[ContradictionRuleData],
        normalized_with_diacritics: str,
        normalized_without_diacritics: str,
    ) -> ContradictionOutcome:
        hits: list[ContradictionHit] = []
        total_penalty = 0.0
        cap: float | None = None
        answer_tokens = normalized_without_diacritics.split()

        for rule in rules:
            outcome = self._matcher.match(
                normalized_with_diacritics,
                normalized_without_diacritics,
                rule.pattern,
                rule.match_type,
                rule.minimum_similarity,
            )
            if not outcome.matched:
                continue
            if outcome.matched_span and self._is_negated(answer_tokens, outcome.matched_span):
                continue
            hits.append(
                ContradictionHit(
                    description=rule.description or rule.pattern,
                    matched_text=outcome.matched_span or rule.pattern,
                    penalty=rule.penalty,
                    maximum_score=rule.maximum_score,
                )
            )
            total_penalty += rule.penalty
            if rule.maximum_score is not None:
                cap = rule.maximum_score if cap is None else min(cap, rule.maximum_score)

        return ContradictionOutcome(hits=hits, total_penalty=total_penalty, maximum_score_cap=cap)

    @staticmethod
    def _is_negated(answer_tokens: list[str], matched_span: str) -> bool:
        span_tokens = strip_diacritics(matched_span).lower().split()
        if not span_tokens:
            return False
        span_len = len(span_tokens)
        for i in range(len(answer_tokens) - span_len + 1):
            if answer_tokens[i : i + span_len] == span_tokens:
                start = max(0, i - _NEGATION_WINDOW)
                preceding = answer_tokens[start:i]
                if any(tok in _NEGATION_WORDS for tok in preceding):
                    return True
        return False
