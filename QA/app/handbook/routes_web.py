"""Server-rendered, read-only pages for the handbook viewer. Everything is rendered
server-side from HandbookStore -- no API, no client-side JS, no progress tracking. Uses its
own Jinja2Templates instance pointed at the shared app/templates directory -- no import from
app.web or app.practical_review, to keep this module's dependency surface self-contained."""

from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.core.exceptions import NotFoundError
from app.handbook.store import HandbookStore, get_store

router = APIRouter(include_in_schema=False)

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@router.get("/handbook", response_class=HTMLResponse)
def overview_page(request: Request, store: HandbookStore = Depends(get_store)) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        "handbook/overview.html",
        {
            "topics": store.list_topics(),
            "question_count": store.question_count,
            "topic_count": store.topic_count,
        },
    )


@router.get("/handbook/topics/{topic_slug}", response_class=HTMLResponse)
def topic_page(
    request: Request, topic_slug: str, store: HandbookStore = Depends(get_store)
) -> HTMLResponse:
    topic = store.get_topic(topic_slug)
    if topic is None:
        raise NotFoundError(f"Không tìm thấy chủ đề '{topic_slug}'")
    return templates.TemplateResponse(request, "handbook/topic.html", {"topic": topic})


@router.get("/handbook/glossary", response_class=HTMLResponse)
def glossary_page(request: Request, store: HandbookStore = Depends(get_store)) -> HTMLResponse:
    return templates.TemplateResponse(
        request, "handbook/glossary.html", {"terms": store.list_glossary()}
    )
