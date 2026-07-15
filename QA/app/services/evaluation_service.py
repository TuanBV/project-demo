"""EvaluationService: bridges the DB layer (Question ORM w/ rubric) and the pure
evaluation engine (app/evaluation/*), converting ORM objects into DTOs.
"""

from __future__ import annotations

from app.core.exceptions import NotFoundError
from app.db.models.question import Question
from app.evaluation.base import (
    AnswerEvaluator,
    ConceptData,
    ContradictionRuleData,
    EvaluationResult,
    KeywordData,
    QuestionEvaluationData,
)
from app.repositories.question_repository import QuestionRepository


def to_evaluation_data(question: Question) -> QuestionEvaluationData:
    concepts = [
        ConceptData(
            concept_id=concept.id,
            name=concept.name,
            description=concept.description or concept.name,
            weight=concept.weight,
            required=concept.required,
            keywords=[
                KeywordData(
                    keyword=kw.keyword,
                    normalized_keyword=kw.normalized_keyword,
                    match_type=kw.match_type.value,
                    minimum_similarity=kw.minimum_similarity,
                    language=kw.language,
                )
                for kw in concept.keywords
                if kw.active
            ],
        )
        for concept in question.concepts
    ]
    rules = [
        ContradictionRuleData(
            pattern=rule.pattern,
            description=rule.description or rule.pattern,
            penalty=rule.penalty,
            maximum_score=rule.maximum_score,
            match_type=rule.match_type.value,
            minimum_similarity=rule.minimum_similarity,
        )
        for rule in question.contradiction_rules
        if rule.active
    ]
    return QuestionEvaluationData(
        question_id=question.id,
        content=question.content,
        reference_answer=question.reference_answer,
        concepts=concepts,
        contradiction_rules=rules,
        minimum_answer_length=question.minimum_answer_length,
        minimum_token_count=question.minimum_token_count,
    )


class EvaluationService:
    def __init__(self, question_repository: QuestionRepository, evaluator: AnswerEvaluator) -> None:
        self._questions = question_repository
        self._evaluator = evaluator

    def evaluate(self, question_id: int, submitted_answer: str) -> EvaluationResult:
        question = self._questions.get_with_rubric(question_id)
        if question is None:
            raise NotFoundError(f"Question {question_id} not found")
        data = to_evaluation_data(question)
        return self._evaluator.evaluate(data, submitted_answer)
