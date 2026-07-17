"""Server-rendered pages for the practical-review area. Pages are thin shells; all data
fetching happens client-side against /api/practical-review/* (practical_review.js). Uses its
own Jinja2Templates instance pointed at the shared app/templates directory -- no import from
app.web, to keep this module's dependency surface self-contained."""

from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.core.exceptions import NotFoundError
from app.practical_review.store import PracticalReviewStore, get_store

router = APIRouter(include_in_schema=False)

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@router.get("/practical-review", response_class=HTMLResponse)
def overview_page(
    request: Request, store: PracticalReviewStore = Depends(get_store)
) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        "practical_review/overview.html",
        {
            "topics": store.list_topics(),
            "question_count": store.question_count,
            "topic_count": store.topic_count,
        },
    )


@router.get("/practical-review/search", response_class=HTMLResponse)
def search_page(request: Request, store: PracticalReviewStore = Depends(get_store)) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        "practical_review/search.html",
        {"topics": store.list_topics(), "question_count": store.question_count},
    )


@router.get("/practical-review/topics/{topic_slug}", response_class=HTMLResponse)
def topic_page(
    request: Request, topic_slug: str, store: PracticalReviewStore = Depends(get_store)
) -> HTMLResponse:
    topic = store.get_topic(topic_slug)
    if topic is None:
        raise NotFoundError(f"Không tìm thấy chủ đề '{topic_slug}'")
    return templates.TemplateResponse(request, "practical_review/topic.html", {"topic": topic})


@router.get("/practical-review/topics/{topic_slug}/study", response_class=HTMLResponse)
def topic_study_page(
    request: Request, topic_slug: str, store: PracticalReviewStore = Depends(get_store)
) -> HTMLResponse:
    topic = store.get_topic(topic_slug)
    if topic is None:
        raise NotFoundError(f"Không tìm thấy chủ đề '{topic_slug}'")
    return templates.TemplateResponse(request, "practical_review/study.html", {"topic": topic})
