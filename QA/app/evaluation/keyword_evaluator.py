"""KeywordAnswerEvaluator: the MVP implementation of the AnswerEvaluator protocol.

Pipeline: normalize -> per-concept best-keyword match (no double counting) -> weighted
concept coverage -> contradiction penalty/cap -> answer-quality cap -> classification ->
template feedback. See docs/architecture.md for the full pipeline diagram.
"""

from __future__ import annotations

from app.core.config import get_settings
from app.evaluation.base import (
    AnswerEvaluator,
    EvaluationResult,
    MatchedConcept,
    MissingConcept,
    QuestionEvaluationData,
)
from app.evaluation.contradiction_detector import ContradictionDetector
from app.evaluation.feedback_builder import FeedbackBuilder
from app.evaluation.matcher import KeywordMatcher
from app.evaluation.normalizer import TextNormalizer

_CONNECTOR_WORDS = {
    "la",
    "co",
    "the",
    "vi",
    "boi",
    "nen",
    "do",
    "khi",
    "neu",
    "thi",
    "va",
    "hoac",
    "duoc",
    "khong",
    "hay",
    "voi",
    "cho",
    "tu",
    "den",
    "nhu",
    "which",
    "is",
    "are",
    "because",
    "when",
    "a",
    "an",
    "to",
    "that",
    "this",
    "can",
    "will",
    "not",
    "and",
    "or",
    "of",
    "in",
    "on",
    "with",
}

_MINIMUM_QUALITY_TOKENS = 4


class KeywordAnswerEvaluator(AnswerEvaluator):
    def __init__(
        self,
        normalizer: TextNormalizer | None = None,
        matcher: KeywordMatcher | None = None,
        contradiction_detector: ContradictionDetector | None = None,
        feedback_builder: FeedbackBuilder | None = None,
    ) -> None:
        self._normalizer = normalizer or TextNormalizer()
        self._matcher = matcher or KeywordMatcher()
        self._contradiction_detector = contradiction_detector or ContradictionDetector(
            self._matcher
        )
        self._feedback_builder = feedback_builder or FeedbackBuilder()
        self._settings = get_settings()

    def evaluate(self, question: QuestionEvaluationData, submitted_answer: str) -> EvaluationResult:
        settings = self._settings
        normalized = self._normalizer.normalize(submitted_answer or "")

        matched: list[MatchedConcept] = []
        partial: list[MatchedConcept] = []
        missing: list[MissingConcept] = []

        total_weight = sum(c.weight for c in question.concepts)
        if total_weight <= 0:
            total_weight = float(len(question.concepts)) or 1.0
            weights = {c.concept_id: 1.0 for c in question.concepts}
        else:
            weights = {c.concept_id: c.weight for c in question.concepts}

        earned_weight = 0.0

        if normalized.with_diacritics:
            for concept in question.concepts:
                weight = weights[concept.concept_id]
                best_fraction = 0.0
                best_keyword: str | None = None
                best_match_type: str | None = None
                best_similarity: float | None = None

                for kw in concept.keywords:
                    outcome = self._matcher.match(
                        normalized.with_diacritics,
                        normalized.without_diacritics,
                        kw.keyword,
                        kw.match_type,
                        kw.minimum_similarity,
                    )
                    if not outcome.matched:
                        continue
                    if kw.match_type == "FUZZY":
                        fraction = self._matcher.fuzzy_score_bucket(outcome.similarity)
                    else:
                        fraction = 1.0
                    if fraction > best_fraction:
                        best_fraction = fraction
                        best_keyword = kw.keyword
                        best_match_type = kw.match_type
                        best_similarity = outcome.similarity

                concept_max = weight / total_weight * 100
                concept_earned = concept_max * best_fraction
                earned_weight += weight * best_fraction

                if best_fraction >= 1.0:
                    matched.append(
                        MatchedConcept(
                            concept_id=concept.concept_id,
                            name=concept.name,
                            description=concept.description,
                            earned_score=concept_earned,
                            maximum_score=concept_max,
                            matched_keyword=best_keyword,
                            match_type=best_match_type,
                            similarity=best_similarity,
                        )
                    )
                elif best_fraction > 0:
                    partial.append(
                        MatchedConcept(
                            concept_id=concept.concept_id,
                            name=concept.name,
                            description=concept.description,
                            earned_score=concept_earned,
                            maximum_score=concept_max,
                            matched_keyword=best_keyword,
                            match_type=best_match_type,
                            similarity=best_similarity,
                        )
                    )
                else:
                    missing.append(
                        MissingConcept(
                            concept_id=concept.concept_id,
                            name=concept.name,
                            description=concept.description,
                            maximum_score=concept_max,
                        )
                    )
        else:
            for concept in question.concepts:
                weight = weights[concept.concept_id]
                concept_max = weight / total_weight * 100
                missing.append(
                    MissingConcept(
                        concept_id=concept.concept_id,
                        name=concept.name,
                        description=concept.description,
                        maximum_score=concept_max,
                    )
                )

        concept_coverage_score = earned_weight / total_weight * 100 if total_weight else 0.0

        contradiction_outcome = self._contradiction_detector.detect(
            question.contradiction_rules,
            normalized.with_diacritics,
            normalized.without_diacritics,
        )

        score = max(0.0, concept_coverage_score - contradiction_outcome.total_penalty)
        if contradiction_outcome.maximum_score_cap is not None:
            score = min(score, contradiction_outcome.maximum_score_cap)

        answer_quality_capped = False
        if settings.enable_answer_quality_factor and self._looks_like_keyword_dump(
            normalized.tokens, question.minimum_token_count
        ):
            if score > settings.keyword_only_maximum_score:
                score = settings.keyword_only_maximum_score
                answer_quality_capped = True

        score = round(min(100.0, max(0.0, score)), 2)
        classification = self._classify(score)
        feedback = self._feedback_builder.build(
            matched, partial, missing, contradiction_outcome.hits, classification
        )

        return EvaluationResult(
            score=score,
            classification=classification,
            matched_concepts=matched,
            partial_concepts=partial,
            missing_concepts=missing,
            contradictions=contradiction_outcome.hits,
            feedback=feedback,
            reference_answer=question.reference_answer,
            concept_coverage_score=round(concept_coverage_score, 2),
            contradiction_penalty=contradiction_outcome.total_penalty,
            answer_quality_capped=answer_quality_capped,
        )

    def _looks_like_keyword_dump(self, tokens: list[str], minimum_token_count: int) -> bool:
        required = max(minimum_token_count, _MINIMUM_QUALITY_TOKENS)
        if len(tokens) < required:
            return True
        has_connector = any(tok in _CONNECTOR_WORDS for tok in tokens)
        return not has_connector

    def _classify(self, score: float) -> str:
        settings = self._settings
        if score >= settings.correct_score_threshold:
            return "CORRECT"
        if score >= settings.mostly_correct_score_threshold:
            return "MOSTLY_CORRECT"
        if score >= settings.partially_correct_score_threshold:
            return "PARTIALLY_CORRECT"
        return "INCORRECT"
