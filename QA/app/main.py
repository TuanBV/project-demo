"""FastAPI application entry point. Wires routers, middleware, and the Jinja2 web UI."""

from __future__ import annotations

import time
import uuid
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles

from app.api.routes import (
    admin_questions,
    categories,
    health,
    imports,
    knowledge_review,
    progress,
    questions,
    study_sessions,
)
from app.core.config import get_settings
from app.core.exceptions import register_exception_handlers
from app.core.logging import configure_logging, get_logger, request_id_ctx
from app.practical_review.routes_api import router as practical_review_api_router
from app.practical_review.routes_web import router as practical_review_web_router
from app.web import router as web_router

settings = get_settings()
configure_logging(settings.log_level)
logger = get_logger(__name__)

app = FastAPI(title=settings.app_name, debug=settings.debug)

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
STATIC_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.middleware("http")
async def request_context_middleware(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", uuid.uuid4().hex[:16])
    token = request_id_ctx.set(request_id)
    start = time.monotonic()
    try:
        response: Response = await call_next(request)
    finally:
        request_id_ctx.reset(token)
    duration_ms = (time.monotonic() - start) * 1000
    response.headers["X-Request-ID"] = request_id
    logger.info(
        "%s %s -> %s (%.1fms)", request.method, request.url.path, response.status_code, duration_ms
    )
    return response


register_exception_handlers(app)

app.include_router(health.router)
app.include_router(categories.router)
app.include_router(questions.router)
app.include_router(knowledge_review.router)
app.include_router(admin_questions.router)
app.include_router(imports.router)
app.include_router(study_sessions.router)
app.include_router(progress.router)
app.include_router(practical_review_api_router)
app.include_router(practical_review_web_router)
app.include_router(web_router)
