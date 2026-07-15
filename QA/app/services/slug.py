"""Shared slug generation, used by category and (indirectly) import services."""

from __future__ import annotations

import re

from app.evaluation.normalizer import strip_diacritics

_NON_SLUG_RE = re.compile(r"[^a-z0-9]+")


def slugify(value: str) -> str:
    ascii_value = strip_diacritics(value).lower()
    slug = _NON_SLUG_RE.sub("-", ascii_value).strip("-")
    return slug or "category"
