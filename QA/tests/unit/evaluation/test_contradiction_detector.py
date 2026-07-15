from __future__ import annotations

from app.evaluation.base import ContradictionRuleData
from app.evaluation.contradiction_detector import ContradictionDetector
from app.evaluation.normalizer import TextNormalizer

normalizer = TextNormalizer()
detector = ContradictionDetector()


def _detect(rules: list[ContradictionRuleData], answer: str):
    n = normalizer.normalize(answer)
    return detector.detect(rules, n.with_diacritics, n.without_diacritics)


def test_contradiction_detected_when_wrong_claim_present() -> None:
    rules = [ContradictionRuleData("count++ la atomic", "sai", 30, None, "CONTAINS")]
    outcome = _detect(rules, "volatile dam bao count++ la atomic")
    assert len(outcome.hits) == 1
    assert outcome.total_penalty == 30


def test_negation_guard_suppresses_false_positive() -> None:
    rules = [ContradictionRuleData("count++ la atomic", "sai", 30, None, "CONTAINS")]
    outcome = _detect(rules, "volatile khong dam bao count++ la atomic")
    assert len(outcome.hits) == 0
    assert outcome.total_penalty == 0


def test_maximum_score_cap_is_minimum_across_rules() -> None:
    rules = [
        ContradictionRuleData("a sai", "sai a", 10, 60, "CONTAINS"),
        ContradictionRuleData("b sai", "sai b", 10, 40, "CONTAINS"),
    ]
    outcome = _detect(rules, "day la a sai va b sai luon")
    assert outcome.maximum_score_cap == 40
