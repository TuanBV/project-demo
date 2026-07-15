from __future__ import annotations

from app.evaluation.matcher import KeywordMatcher
from app.evaluation.normalizer import TextNormalizer

normalizer = TextNormalizer()
matcher = KeywordMatcher()


def _normalized(text: str) -> tuple[str, str]:
    n = normalizer.normalize(text)
    return n.with_diacritics, n.without_diacritics


def test_exact_match() -> None:
    wd, wod = _normalized("visibility la dieu volatile dam bao")
    outcome = matcher.match(wd, wod, "visibility", "EXACT")
    assert outcome.matched
    assert outcome.similarity == 100.0


def test_contains_match() -> None:
    wd, wod = _normalized("garbage collector tu dong don rac")
    outcome = matcher.match(wd, wod, "garbage collector", "CONTAINS")
    assert outcome.matched


def test_word_boundary_short_keyword_forced_exact() -> None:
    wd, wod = _normalized("day la mot list cac phan tu")
    outcome = matcher.match(wd, wod, "is", "CONTAINS")
    assert not outcome.matched


def test_fuzzy_typo_match() -> None:
    wd, wod = _normalized("day la mutabel object")
    outcome = matcher.match(wd, wod, "mutable", "FUZZY", minimum_similarity=70)
    assert outcome.matched


def test_fuzzy_below_threshold_no_match() -> None:
    wd, wod = _normalized("hoan toan khong lien quan gi ca")
    outcome = matcher.match(wd, wod, "polymorphism", "FUZZY", minimum_similarity=70)
    assert not outcome.matched


def test_alias_match_after_normalization() -> None:
    wd, wod = _normalized("day la kieu bat bien")
    outcome = matcher.match(wd, wod, "immutable", "ALIAS")
    assert outcome.matched


def test_short_keyword_does_not_match_substring_of_longer_word() -> None:
    wd, wod = _normalized("toi thich list nay")
    outcome = matcher.match(wd, wod, "is", "CONTAINS")
    assert not outcome.matched


def test_fuzzy_score_bucket_thresholds() -> None:
    assert matcher.fuzzy_score_bucket(95) == 1.0
    assert matcher.fuzzy_score_bucket(85) == 0.75
    assert matcher.fuzzy_score_bucket(75) == 0.5
    assert matcher.fuzzy_score_bucket(50) == 0.0
