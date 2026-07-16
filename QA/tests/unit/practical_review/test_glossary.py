"""Unit tests for the supplementary jargon glossary (app/practical_review/glossary.py)."""

from __future__ import annotations

from app.practical_review.glossary import GLOSSARY


def test_glossary_is_non_empty() -> None:
    assert len(GLOSSARY) > 0


def test_glossary_entries_have_term_and_definition() -> None:
    for entry in GLOSSARY:
        assert entry.term.strip()
        assert entry.definition.strip()


def test_glossary_terms_are_unique_case_insensitive() -> None:
    lowered = [entry.term.lower() for entry in GLOSSARY]
    assert len(lowered) == len(set(lowered))
