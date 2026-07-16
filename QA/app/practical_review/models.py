"""Plain dataclasses for parsed DOCX content. No FastAPI, no SQLAlchemy, no Pydantic here --
this module must stay importable in complete isolation for parser unit tests."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PracticalTopic:
    slug: str
    order: int
    heading: str
    display_name: str
    group: str
    question_count: int


@dataclass(frozen=True)
class PracticalQuestion:
    number: int
    topic_slug: str
    topic_name: str
    question: str
    answer: str
    explanation: str


@dataclass(frozen=True)
class ParsedDocument:
    topics: list[PracticalTopic]
    questions: list[PracticalQuestion]
