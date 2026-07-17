"""In-memory store for the handbook DOCX content. Parses the DOCX exactly once per process
(functools.lru_cache) and serves every request from memory -- never re-parses the file per
HTTP request. No database, no dependency on the quiz or practical-review features."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from app.handbook.docx_parser import parse_docx
from app.handbook.models import HandbookTerm, HandbookTopic, ParsedHandbook

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DOCX_PATH = PROJECT_ROOT / "scripts" / "data" / "so_tay_on_tap_de_doc_noi_bat.docx"


class HandbookStore:
    def __init__(self, document: ParsedHandbook, source_path: Path) -> None:
        self._topics_by_slug: dict[str, HandbookTopic] = {t.slug: t for t in document.topics}
        self._topics_ordered: list[HandbookTopic] = sorted(document.topics, key=lambda t: t.order)
        self._glossary: list[HandbookTerm] = list(document.glossary)
        self.source_path = source_path

    def list_topics(self) -> list[HandbookTopic]:
        return list(self._topics_ordered)

    def get_topic(self, slug: str) -> HandbookTopic | None:
        return self._topics_by_slug.get(slug)

    def list_glossary(self) -> list[HandbookTerm]:
        return list(self._glossary)

    @property
    def question_count(self) -> int:
        return sum(t.question_count for t in self._topics_ordered)

    @property
    def topic_count(self) -> int:
        return len(self._topics_ordered)

    @property
    def source_display_path(self) -> str:
        try:
            return self.source_path.relative_to(PROJECT_ROOT).as_posix()
        except ValueError:
            return str(self.source_path)


@lru_cache(maxsize=1)
def get_store() -> HandbookStore:
    document = parse_docx(DOCX_PATH)
    return HandbookStore(document, DOCX_PATH)
