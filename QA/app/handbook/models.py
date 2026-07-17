"""Plain dataclasses for parsed handbook DOCX content. No FastAPI, no SQLAlchemy, no
Pydantic here -- this module must stay importable in complete isolation for parser unit
tests."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class HandbookTerm:
    term: str
    definition: str


@dataclass(frozen=True)
class HandbookQuestion:
    number: int
    question: str
    core: str
    explanation: str


@dataclass(frozen=True)
class HandbookTopic:
    slug: str
    order: int
    heading: str
    display_name: str
    question_range: str
    goal: str
    terms: list[HandbookTerm] = field(default_factory=list)
    common_mistakes: list[str] = field(default_factory=list)
    core_examples: list[str] = field(default_factory=list)
    questions: list[HandbookQuestion] = field(default_factory=list)

    @property
    def question_count(self) -> int:
        return len(self.questions)


@dataclass(frozen=True)
class ParsedHandbook:
    topics: list[HandbookTopic]
    glossary: list[HandbookTerm]
