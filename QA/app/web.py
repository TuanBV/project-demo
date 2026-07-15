"""Server-rendered Jinja2 pages. Pages are thin shells; interactive behavior (fetching
questions, submitting answers, import preview) is vanilla JS calling the JSON API in
app/api/routes/* -- no business logic lives here (spec section 17).
"""

from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.api.dependencies import category_service, get_db, progress_service

router = APIRouter(include_in_schema=False)

TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@router.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    progress = progress_service(db)
    categories = category_service(db)
    overview = progress.overview()
    return templates.TemplateResponse(
        request,
        "index.html",
        {"overview": overview, "categories": categories.list_all(active_only=True)},
    )


@router.get("/study", response_class=HTMLResponse)
def study_page(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    categories = category_service(db)
    return templates.TemplateResponse(
        request, "study.html", {"categories": categories.list_all(active_only=True)}
    )


@router.get("/import", response_class=HTMLResponse)
def import_page(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    categories = category_service(db)
    return templates.TemplateResponse(
        request, "import.html", {"categories": categories.list_all(active_only=True)}
    )


@router.get("/admin/questions", response_class=HTMLResponse)
def question_list_page(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    categories = category_service(db)
    return templates.TemplateResponse(
        request, "admin/questions.html", {"categories": categories.list_all(active_only=True)}
    )


@router.get("/admin/questions/new", response_class=HTMLResponse)
def question_new_page(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    categories = category_service(db)
    return templates.TemplateResponse(
        request,
        "admin/question_form.html",
        {"categories": categories.list_all(active_only=True), "question_id": None},
    )


@router.get("/admin/questions/{question_id}/edit", response_class=HTMLResponse)
def question_edit_page(
    request: Request, question_id: int, db: Session = Depends(get_db)
) -> HTMLResponse:
    categories = category_service(db)
    return templates.TemplateResponse(
        request,
        "admin/question_form.html",
        {"categories": categories.list_all(active_only=True), "question_id": question_id},
    )


@router.get("/history", response_class=HTMLResponse)
def history_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "history.html", {})
