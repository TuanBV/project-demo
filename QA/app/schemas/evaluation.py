from __future__ import annotations

from pydantic import BaseModel


class MatchedConceptSchema(BaseModel):
    concept_id: int
    name: str
    description: str
    earned_score: float
    maximum_score: float
    matched_keyword: str | None
    match_type: str | None
    similarity: float | None


class MissingConceptSchema(BaseModel):
    concept_id: int
    name: str
    description: str
    maximum_score: float


class ContradictionHitSchema(BaseModel):
    description: str
    matched_text: str
    penalty: float
    maximum_score: float | None


class EvaluationResultSchema(BaseModel):
    score: float
    classification: str
    matched_concepts: list[MatchedConceptSchema]
    partial_concepts: list[MatchedConceptSchema]
    missing_concepts: list[MissingConceptSchema]
    contradictions: list[ContradictionHitSchema]
    feedback: str
    reference_answer: str | None
    concept_coverage_score: float
    contradiction_penalty: float
    answer_quality_capped: bool
