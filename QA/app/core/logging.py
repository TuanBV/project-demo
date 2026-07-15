"""Structured logging setup with request/correlation id support."""

from __future__ import annotations

import contextvars
import logging
import sys
import uuid

request_id_ctx: contextvars.ContextVar[str] = contextvars.ContextVar("request_id", default="-")


class RequestIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id_ctx.get()
        return True


def configure_logging(level: str = "INFO") -> None:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter(
            fmt="%(asctime)s %(levelname)s [%(request_id)s] %(name)s: %(message)s",
        )
    )
    handler.addFilter(RequestIdFilter())

    root = logging.getLogger()
    root.setLevel(level)
    root.handlers = [handler]


def new_request_id() -> str:
    return uuid.uuid4().hex[:16]


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
