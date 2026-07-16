"""Read-only JSON API for the practical-review study guide. Never touches Question,
QuestionOption, StudySession, or Attempt -- reads only from the in-memory DOCX-backed store
(app.practical_review.store.get_store)."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query

from app.core.exceptions import NotFoundError
from app.practical_review.schemas import (
    QuestionSchema,
    SearchResultSchema,
    SourceInfoSchema,
    TopicDetailSchema,
    TopicSummarySchema,
)
from app.practical_review.store import PracticalReviewStore, get_store

router = APIRouter(prefix="/api/practical-review", tags=["practical-review"])


@router.get("/topics", response_model=list[TopicSummarySchema])
def list_topics(store: PracticalReviewStore = Depends(get_store)) -> list[TopicSummarySchema]:
    return [TopicSummarySchema.from_topic(t) for t in store.list_topics()]


@router.get("/topics/{topic_slug}", response_model=TopicDetailSchema)
def get_topic(
    topic_slug: str, store: PracticalReviewStore = Depends(get_store)
) -> TopicDetailSchema:
    topic = store.get_topic(topic_slug)
    if topic is None:
        raise NotFoundError(f"Không tìm thấy chủ đề '{topic_slug}'")
    questions = store.list_questions(topic_slug)
    return TopicDetailSchema(
        topic=TopicSummarySchema.from_topic(topic),
        questions=[QuestionSchema.from_question(q) for q in questions],
    )


@router.get("/questions/{question_number}", response_model=QuestionSchema)
def get_question(
    question_number: int, store: PracticalReviewStore = Depends(get_store)
) -> QuestionSchema:
    question = store.get_question(question_number)
    if question is None:
        raise NotFoundError(f"Không tìm thấy câu hỏi số {question_number}")
    return QuestionSchema.from_question(question)


@router.get("/search", response_model=SearchResultSchema)
def search(
    q: str = Query(default=""),
    topic_slug: str | None = None,
    store: PracticalReviewStore = Depends(get_store),
) -> SearchResultSchema:
    if topic_slug is not None and store.get_topic(topic_slug) is None:
        raise NotFoundError(f"Không tìm thấy chủ đề '{topic_slug}'")
    results = store.search(q, topic_slug=topic_slug)
    return SearchResultSchema(
        query=q,
        total=len(results),
        items=[QuestionSchema.from_question(r) for r in results],
    )


@router.get("/source-info", response_model=SourceInfoSchema)
def source_info(store: PracticalReviewStore = Depends(get_store)) -> SourceInfoSchema:
    return SourceInfoSchema(
        source=store.source_display_path,
        topic_count=store.topic_count,
        question_count=store.question_count,
        topics=[TopicSummarySchema.from_topic(t) for t in store.list_topics()],
    )
