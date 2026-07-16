"""Self-contained text helpers for practical_review search -- deliberately not importing
app.evaluation.normalizer (which is part of the FREE_TEXT quiz evaluator) to keep this
module's dependency surface at zero shared app code, per the isolation requirement."""

from __future__ import annotations

import unicodedata


def strip_diacritics(value: str) -> str:
    """Fold Vietnamese diacritics for approximate ("không dấu") search matching."""
    normalized = unicodedata.normalize("NFD", value)
    without_marks = "".join(ch for ch in normalized if unicodedata.category(ch) != "Mn")
    return without_marks.replace("đ", "d").replace("Đ", "D")


def normalize_for_search(value: str) -> str:
    return strip_diacritics(value).lower()
