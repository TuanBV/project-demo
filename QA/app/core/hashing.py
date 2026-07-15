"""content_hash computation shared by question_service and the import pipeline (spec section 7)."""

from __future__ import annotations

import hashlib
import re

from app.evaluation.normalizer import strip_diacritics

_WHITESPACE_RE = re.compile(r"\s+")


def _normalize_key(value: str) -> str:
    ascii_value = strip_diacritics(value or "").lower()
    return _WHITESPACE_RE.sub(" ", ascii_value).strip()


def compute_content_hash(category_name: str, question_content: str, question_type: str) -> str:
    normalized = (
        f"{_normalize_key(category_name)}|{_normalize_key(question_content)}|"
        f"{question_type.strip().upper()}"
    )
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()
