"""Pure-Python DTOs and Protocol for answer evaluation.

This module (and the rest of app/evaluation) must never import FastAPI or SQLAlchemy so it
stays independently unit-testable and reusable from the CLI / future services.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol


@dataclass(frozen=True)
class KeywordData:
    keyword: str
    normalized_keyword: str
    match_type: str  # EXACT | CONTAINS | FUZZY | ALIAS
    minimum_similarity: float = 80.0
    language: str | None = None


@dataclass(frozen=True)
class ConceptData:
    concept_id: int
    name: str
    description: str
    weight: float
    required: bool
    keywords: list[KeywordData] = field(default_factory=list)


@dataclass(frozen=True)
class ContradictionRuleData:
    pattern: str
    description: str
    penalty: float
    maximum_score: float | None
    match_type: str
    minimum_similarity: float = 85.0


@dataclass(frozen=True)
class QuestionEvaluationData:
    question_id: int
    content: str
    reference_answer: str | None
    concepts: list[ConceptData]
    contradiction_rules: list[ContradictionRuleData]
    minimum_answer_length: int = 0
    minimum_token_count: int = 0


@dataclass(frozen=True)
class MatchedConcept:
    concept_id: int
    name: str
    description: str
    earned_score: float
    maximum_score: float
    matched_keyword: str | None
    match_type: str | None
    similarity: float | None


@dataclass(frozen=True)
class MissingConcept:
    concept_id: int
    name: str
    description: str
    maximum_score: float


@dataclass(frozen=True)
class ContradictionHit:
    description: str
    matched_text: str
    penalty: float
    maximum_score: float | None


@dataclass(frozen=True)
class EvaluationResult:
    score: float
    classification: str
    matched_concepts: list[MatchedConcept]
    partial_concepts: list[MatchedConcept]
    missing_concepts: list[MissingConcept]
    contradictions: list[ContradictionHit]
    feedback: str
    reference_answer: str | None
    concept_coverage_score: float
    contradiction_penalty: float
    answer_quality_capped: bool


class AnswerEvaluator(Protocol):
    def evaluate(
        self,
        question: QuestionEvaluationData,
        submitted_answer: str,
    ) -> EvaluationResult: ...
