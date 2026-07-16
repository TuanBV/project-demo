"""Pydantic response schemas for /api/practical-review/*. Deliberately independent of
app/schemas/question.py and app/schemas/study.py -- this feature has its own response
shapes and must not import quiz-related schemas."""

from __future__ import annotations

from pydantic import BaseModel

from app.practical_review.models import PracticalQuestion, PracticalTopic


class TopicSummarySchema(BaseModel):
    slug: str
    order: int
    display_name: str
    group: str
    question_count: int

    @classmethod
    def from_topic(cls, topic: PracticalTopic) -> TopicSummarySchema:
        return cls(
            slug=topic.slug,
            order=topic.order,
            display_name=topic.display_name,
            group=topic.group,
            question_count=topic.question_count,
        )


class QuestionSchema(BaseModel):
    number: int
    topic_slug: str
    topic_name: str
    question: str
    answer: str
    explanation: str

    @classmethod
    def from_question(cls, question: PracticalQuestion) -> QuestionSchema:
        return cls(
            number=question.number,
            topic_slug=question.topic_slug,
            topic_name=question.topic_name,
            question=question.question,
            answer=question.answer,
            explanation=question.explanation,
        )


class TopicDetailSchema(BaseModel):
    topic: TopicSummarySchema
    questions: list[QuestionSchema]


class SearchResultSchema(BaseModel):
    query: str
    total: int
    items: list[QuestionSchema]


class SourceInfoSchema(BaseModel):
    source: str
    topic_count: int
    question_count: int
    topics: list[TopicSummarySchema]
