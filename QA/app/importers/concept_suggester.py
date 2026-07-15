"""ConceptSuggestionService: heuristic (non-LLM) concept/keyword suggestion (spec section 10).

Splits the reference answer into clauses, treats each significant clause as a candidate
concept, and pulls keywords by filtering stopwords/short tokens. Everything produced here
must be flagged auto_generated=True by the caller -- suggestions are never auto-accepted.
"""

from __future__ import annotations

import re

from app.evaluation.normalizer import TextNormalizer, strip_diacritics
from app.importers.dto import SuggestedConcept

_STOPWORDS = {
    "la",
    "va",
    "co",
    "the",
    "cua",
    "mot",
    "nay",
    "do",
    "khi",
    "neu",
    "thi",
    "duoc",
    "cho",
    "tu",
    "den",
    "nhu",
    "hay",
    "hoac",
    "khong",
    "rat",
    "cac",
    "nhung",
    "voi",
    "de",
    "trong",
    "tren",
    "duoi",
    "sau",
    "truoc",
    "boi",
    "vi",
    "nen",
    "is",
    "are",
    "a",
    "an",
    "of",
    "and",
    "or",
    "to",
    "in",
    "on",
    "with",
    "that",
    "this",
    "can",
    "will",
    "not",
    "by",
    "for",
    "as",
}

_CLAUSE_SPLIT_RE = re.compile(
    r"(?<=[.!?;])\s+|\s+(?:nhưng|nhung|tuy nhiên|tuy nhien|however|but)\s+",
    re.IGNORECASE,
)
_MAX_CONCEPTS = 6
_MAX_KEYWORDS_PER_CONCEPT = 5
_MIN_CLAUSE_WORDS = 3
_MIN_KEYWORD_LENGTH = 3


class ConceptSuggestionService:
    def __init__(self, normalizer: TextNormalizer | None = None) -> None:
        self._normalizer = normalizer or TextNormalizer()

    def suggest(self, question: str, reference_answer: str) -> list[SuggestedConcept]:
        clauses = self._split_clauses(reference_answer)
        if not clauses:
            return []

        concepts: list[SuggestedConcept] = []
        n = len(clauses)
        base_weight = 100 // n
        weight_used = 0
        for index, clause in enumerate(clauses):
            is_last = index == n - 1
            weight = (100 - weight_used) if is_last else base_weight
            weight_used += weight
            keywords = self._extract_keywords(clause)
            concepts.append(
                SuggestedConcept(
                    name=self._derive_name(keywords, index),
                    description=clause.strip(),
                    weight=float(weight),
                    required=(index == 0),
                    keywords=keywords,
                )
            )
        return concepts

    def _split_clauses(self, text: str) -> list[str]:
        if not text or not text.strip():
            return []
        raw_clauses = _CLAUSE_SPLIT_RE.split(text)
        clauses = [c.strip(" .;!?\n\t") for c in raw_clauses if c and c.strip()]
        clauses = [c for c in clauses if len(c.split()) >= _MIN_CLAUSE_WORDS]
        return clauses[:_MAX_CONCEPTS]

    def _extract_keywords(self, clause: str) -> list[str]:
        normalized = self._normalizer.normalize(clause)
        significant: list[str] = []
        for tok in normalized.with_diacritics.split():
            ascii_tok = strip_diacritics(tok)
            if ascii_tok in _STOPWORDS or len(tok) < _MIN_KEYWORD_LENGTH:
                continue
            if tok not in significant:
                significant.append(tok)
        return significant[:_MAX_KEYWORDS_PER_CONCEPT]

    def _derive_name(self, keywords: list[str], index: int) -> str:
        if keywords:
            base = "_".join(strip_diacritics(k).lower().replace(" ", "_") for k in keywords[:2])
            if base:
                return base
        return f"concept_{index + 1}"
