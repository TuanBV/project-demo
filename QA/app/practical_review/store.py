"""In-memory store for the practical-review DOCX content. Parses the DOCX exactly once per
process (functools.lru_cache) and serves every request from memory -- never re-parses the
file per HTTP request. No database, no dependency on the quiz feature's models."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from app.practical_review.docx_parser import parse_docx
from app.practical_review.models import ParsedDocument, PracticalQuestion, PracticalTopic
from app.practical_review.text_utils import normalize_for_search

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DOCX_PATH = PROJECT_ROOT / "scripts" / "data" / "so_tay_on_tap_sap_xep_theo_chu_de_uu_tien.docx"


class PracticalReviewStore:
    def __init__(self, document: ParsedDocument, source_path: Path) -> None:
        self._topics_by_slug: dict[str, PracticalTopic] = {t.slug: t for t in document.topics}
        self._topics_ordered: list[PracticalTopic] = sorted(document.topics, key=lambda t: t.order)
        self._questions_by_number: dict[int, PracticalQuestion] = {
            q.number: q for q in document.questions
        }
        self._questions_by_topic: dict[str, list[PracticalQuestion]] = {}
        for question in document.questions:
            self._questions_by_topic.setdefault(question.topic_slug, []).append(question)
        for bucket in self._questions_by_topic.values():
            bucket.sort(key=lambda q: q.number)
        self._all_questions: list[PracticalQuestion] = sorted(
            document.questions, key=lambda q: q.number
        )
        self.source_path = source_path

    def list_topics(self) -> list[PracticalTopic]:
        return list(self._topics_ordered)

    def get_topic(self, slug: str) -> PracticalTopic | None:
        return self._topics_by_slug.get(slug)

    def list_questions(self, topic_slug: str | None = None) -> list[PracticalQuestion]:
        if topic_slug is None:
            return list(self._all_questions)
        return list(self._questions_by_topic.get(topic_slug, []))

    def get_question(self, number: int) -> PracticalQuestion | None:
        return self._questions_by_number.get(number)

    def search(self, query: str, topic_slug: str | None = None) -> list[PracticalQuestion]:
        normalized_query = normalize_for_search(query.strip())
        if not normalized_query:
            return []
        candidates = self.list_questions(topic_slug)
        results = []
        for question in candidates:
            haystack = normalize_for_search(
                f"{question.topic_name} {question.question} {question.answer} "
                f"{question.explanation}"
            )
            if normalized_query in haystack:
                results.append(question)
        return results

    @property
    def question_count(self) -> int:
        return len(self._all_questions)

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
def get_store() -> PracticalReviewStore:
    document = parse_docx(DOCX_PATH)
    return PracticalReviewStore(document, DOCX_PATH)
