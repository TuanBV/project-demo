"""TextNormalizer: unicode/casing/whitespace normalization for answer scoring.

Produces both a diacritics-preserving and a diacritics-stripped variant so the matcher
can compare Vietnamese answers regardless of whether the learner typed accents, while
protecting technical tokens (==, *args, **kwargs, O(n), @Transactional, __init__, ...)
from being mangled by punctuation stripping.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import yaml

_ALIASES_PATH = Path(__file__).resolve().parent.parent / "resources" / "technical_aliases.yml"

_PROTECTED_PATTERNS = [
    r"==",
    r"!=",
    r">=",
    r"<=",
    r"\*\*[A-Za-z_]\w*",
    r"\*[A-Za-z_]\w*",
    r"\bO\([^)]*\)",
    r"@[A-Za-z_]\w*",
    r"__[A-Za-z_]+__",
    r"\?\s*extends\s+[A-Za-z_]\w*",
    r"\?\s*super\s+[A-Za-z_]\w*",
    r"\.class\b",
    r"\.java\b",
    r"\d+\.\d+",
    r"=",
]
_PROTECTED_RE = re.compile("|".join(_PROTECTED_PATTERNS), re.IGNORECASE)

_CAMEL_BOUNDARY_RE = re.compile(r"(?<=[a-z0-9])(?=[A-Z])")
_PUNCTUATION_RE = re.compile(r"[,\;:!?\"'`~^•·|\\/\[\]{}().]")
_WHITESPACE_RE = re.compile(r"\s+")
_DASH_RE = re.compile(r"[‐-―−]")
_QUOTE_MAP = str.maketrans({"‘": "'", "’": "'", "“": '"', "”": '"'})

_PLACEHOLDER_OPEN = ""
_PLACEHOLDER_CLOSE = ""
_PLACEHOLDER_RE = re.compile(f"{_PLACEHOLDER_OPEN}(\\d+){_PLACEHOLDER_CLOSE}")


@dataclass(frozen=True)
class NormalizedText:
    original: str
    with_diacritics: str
    without_diacritics: str
    tokens: list[str]

    @property
    def token_count(self) -> int:
        return len(self.tokens)

    @property
    def char_length(self) -> int:
        return len(self.with_diacritics)


@lru_cache(maxsize=1)
def _load_alias_map(path: str = str(_ALIASES_PATH)) -> list[tuple[str, str]]:
    """Return (value, canonical) pairs sorted longest-value-first for greedy replacement."""
    file_path = Path(path)
    if not file_path.exists():
        return []
    with file_path.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    pairs: list[tuple[str, str]] = []
    for entry in (data.get("aliases") or {}).values():
        canonical = str(entry["canonical"]).strip().lower()
        for value in entry.get("values", []):
            normalized_value = str(value).strip().lower()
            if normalized_value:
                pairs.append((normalized_value, canonical))
    pairs.sort(key=lambda pair: len(pair[0]), reverse=True)
    return pairs


def strip_diacritics(text: str) -> str:
    text = text.replace("đ", "d").replace("Đ", "D")
    decomposed = unicodedata.normalize("NFD", text)
    without_marks = "".join(ch for ch in decomposed if not unicodedata.combining(ch))
    return unicodedata.normalize("NFC", without_marks)


class TextNormalizer:
    def __init__(self, alias_pairs: list[tuple[str, str]] | None = None) -> None:
        self._alias_pairs = alias_pairs if alias_pairs is not None else _load_alias_map()
        self._alias_patterns = [
            (re.compile(rf"\b{re.escape(value)}\b", re.IGNORECASE), canonical)
            for value, canonical in self._alias_pairs
        ]

    def normalize(self, text: str) -> NormalizedText:
        original = text or ""
        nfc = unicodedata.normalize("NFC", original)
        protected_text, protected_tokens = self._protect(nfc)
        camel_split = _CAMEL_BOUNDARY_RE.sub(" ", protected_text)
        lowered = camel_split.lower()
        quotes_normalized = lowered.translate(_QUOTE_MAP)
        dashes_normalized = _DASH_RE.sub("-", quotes_normalized)
        underscored = dashes_normalized.replace("_", " ")
        cleaned = _PUNCTUATION_RE.sub(" ", underscored)
        collapsed = _WHITESPACE_RE.sub(" ", cleaned).strip()
        restored = self._restore(collapsed, protected_tokens)
        with_aliases = self._canonicalize_aliases(restored)
        with_diacritics = _WHITESPACE_RE.sub(" ", with_aliases).strip()
        without_diacritics = _WHITESPACE_RE.sub(" ", strip_diacritics(with_diacritics)).strip()
        tokens = with_diacritics.split() if with_diacritics else []
        return NormalizedText(
            original=original,
            with_diacritics=with_diacritics,
            without_diacritics=without_diacritics,
            tokens=tokens,
        )

    @staticmethod
    def _protect(text: str) -> tuple[str, list[str]]:
        tokens: list[str] = []

        def repl(match: re.Match[str]) -> str:
            tokens.append(match.group(0))
            return f" {_PLACEHOLDER_OPEN}{len(tokens) - 1}{_PLACEHOLDER_CLOSE} "

        return _PROTECTED_RE.sub(repl, text), tokens

    @staticmethod
    def _restore(text: str, tokens: list[str]) -> str:
        def repl(match: re.Match[str]) -> str:
            return tokens[int(match.group(1))].lower()

        return _PLACEHOLDER_RE.sub(repl, text)

    def _canonicalize_aliases(self, text: str) -> str:
        result = text
        for pattern, canonical in self._alias_patterns:
            result = pattern.sub(canonical, result)
        return result
