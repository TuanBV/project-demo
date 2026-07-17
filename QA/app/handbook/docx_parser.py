"""Parses scripts/data/so_tay_on_tap_de_doc_noi_bat.docx -- the ONLY data source for the
handbook viewer. Must never import or read anything under scripts/data/java_python_mc/ or
scripts/data/extended_topics/, and must not depend on app/practical_review/*.

Expected structure (verified against the actual file before writing this parser):
  - Exactly 11 "Heading 1" paragraphs matching "CHỦ ĐỀ <n> — <name>" (one per topic, in
    document order), followed by a final "Heading 1" appendix
    "PHỤ LỤC A — TỪ ĐIỂN THUẬT NGỮ" containing one large (term, definition) table.
  - Within each topic, in order: a "Phạm vi câu hỏi: ..." paragraph, a "Mục tiêu: ..."
    paragraph, a small (term, definition) table ("1. Thuật ngữ / Khái niệm"), zero or more
    "List Bullet" paragraphs ("2. Sai lầm thường gặp"), zero or more "Code Block" paragraphs
    ("3. Ví dụ cốt lõi" -- each may carry a leading "[Text]" line to strip), and finally
    20 (or fewer, for the two Python topics) "Memory Card"-styled Q&A triples:
    "CÂU <n>  |  <question>", "TRẢ LỜI CỐT LÕI:  <core answer>", and optionally
    "GIẢI THÍCH:  <explanation>" (not always present -- explanation may be "").
  - Question numbers are globally unique but not contiguous (same underlying 207-question
    bank as practical_review, reordered by priority topic).

Pure Python + python-docx only -- no FastAPI, no SQLAlchemy, importable standalone.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from docx import Document as _open_docx
from docx.document import Document
from docx.table import Table
from docx.text.paragraph import Paragraph

from app.handbook.models import HandbookQuestion, HandbookTerm, HandbookTopic, ParsedHandbook

# Positional (slug) for the 11 topics, in the exact order they appear in the DOCX. The
# display name itself is taken from the DOCX heading text, never hardcoded here.
_TOPIC_SLUGS: list[str] = [
    "ai-coding",
    "du-an-production",
    "java-core",
    "oop-solid",
    "spring-boot",
    "git",
    "thuat-toan",
    "rest-api",
    "sql-database",
    "python-core",
    "python-backend",
]

_TOPIC_HEADING_RE = re.compile(r"^CHỦ ĐỀ\s+\d+\s*—\s*(.*)$")
_RANGE_RE = re.compile(r"^Phạm vi câu hỏi:\s*(.*)$")
_GOAL_RE = re.compile(r"^Mục tiêu:\s*(.*)$")
_QUESTION_RE = re.compile(r"^CÂU\s+(\d+)\s*\|\s*(.*)$")
_CORE_RE = re.compile(r"^TRẢ LỜI CỐT LÕI:\s*(.*)$")
_DEEP_RE = re.compile(r"^GIẢI THÍCH:\s*(.*)$")
_CODE_BLOCK_PLACEHOLDER_RE = re.compile(r"^\[Text\]\n?")


class DocxStructureError(ValueError):
    """Raised when the DOCX doesn't match the expected handbook structure. Carries enough
    detail to fix the source file or the parser, never silently drops data."""


@dataclass
class _PendingQuestion:
    number: int
    question: str
    core: str | None = None
    deep: str | None = None


@dataclass
class _PendingTopic:
    slug: str
    order: int
    heading: str
    display_name: str
    question_range: str = ""
    goal: str = ""
    terms: list[HandbookTerm] = field(default_factory=list)
    common_mistakes: list[str] = field(default_factory=list)
    core_examples: list[str] = field(default_factory=list)
    questions: list[HandbookQuestion] = field(default_factory=list)


def _iter_block_items(document: Document):
    """Yield Paragraph/Table objects in actual document order (python-docx's own
    .paragraphs/.tables lists are separate and lose interleaving order)."""
    body = document.element.body
    for child in body.iterchildren():
        if child.tag.endswith("}p"):
            yield Paragraph(child, document)
        elif child.tag.endswith("}tbl"):
            yield Table(child, document)


def _parse_terms_table(table: Table) -> list[HandbookTerm]:
    terms = []
    for row in table.rows[1:]:  # skip header row
        cells = row.cells
        term = cells[0].text.strip()
        definition = cells[1].text.strip()
        if term and definition:
            terms.append(HandbookTerm(term=term, definition=definition))
    return terms


def parse_docx(path: str | Path) -> ParsedHandbook:
    path = Path(path)
    if not path.exists():
        raise DocxStructureError(f"Không tìm thấy file DOCX: {path}")

    document = _open_docx(str(path))

    topics: list[_PendingTopic] = []
    appendix_glossary: list[HandbookTerm] = []
    seen_numbers: set[int] = set()

    current: _PendingTopic | None = None
    current_question: _PendingQuestion | None = None
    in_appendix = False

    def finalize_question() -> None:
        nonlocal current_question
        if current_question is None:
            return
        assert current is not None
        question_text = current_question.question.strip()
        core_text = current_question.core.strip() if current_question.core is not None else ""
        if not question_text or not core_text:
            raise DocxStructureError(
                f"Câu {current_question.number} thiếu nội dung câu hỏi hoặc phần 'TRẢ LỜI CỐT LÕI'."
            )
        deep_text = current_question.deep.strip() if current_question.deep is not None else ""
        current.questions.append(
            HandbookQuestion(
                number=current_question.number,
                question=question_text,
                core=core_text,
                explanation=deep_text,
            )
        )
        current_question = None

    for block in _iter_block_items(document):
        if isinstance(block, Paragraph):
            style_name = block.style.name if block.style else None
            text = block.text.strip()

            if style_name == "Heading 1":
                finalize_question()
                topic_match = _TOPIC_HEADING_RE.match(text)
                if topic_match is None:
                    current = None
                    in_appendix = text.startswith("PHỤ LỤC")
                    continue
                in_appendix = False
                order = len(topics) + 1
                if order > len(_TOPIC_SLUGS):
                    raise DocxStructureError(
                        f"Tìm thấy nhiều hơn {len(_TOPIC_SLUGS)} chủ đề (Heading 1 dạng "
                        f"'CHỦ ĐỀ n — ...') trong DOCX; chủ đề thừa: {text!r}"
                    )
                current = _PendingTopic(
                    slug=_TOPIC_SLUGS[order - 1],
                    order=order,
                    heading=text,
                    display_name=topic_match.group(1).strip(),
                )
                topics.append(current)
                continue

            if current is None or not text:
                continue

            range_match = _RANGE_RE.match(text)
            if range_match is not None:
                current.question_range = range_match.group(1).strip()
                continue
            goal_match = _GOAL_RE.match(text)
            if goal_match is not None:
                current.goal = goal_match.group(1).strip()
                continue

            if style_name == "List Bullet":
                current.common_mistakes.append(text)
                continue
            if style_name == "Code Block":
                current.core_examples.append(_CODE_BLOCK_PLACEHOLDER_RE.sub("", text).strip())
                continue
            if style_name != "Memory Card":
                continue

            question_match = _QUESTION_RE.match(text)
            if question_match is not None:
                finalize_question()
                number = int(question_match.group(1))
                if number in seen_numbers:
                    raise DocxStructureError(f"Số thứ tự câu hỏi bị trùng: {number}")
                seen_numbers.add(number)
                current_question = _PendingQuestion(number=number, question=question_match.group(2))
                continue
            if current_question is None:
                continue  # stray "Memory Card" text outside any question -- ignore defensively
            core_match = _CORE_RE.match(text)
            if core_match is not None:
                current_question.core = core_match.group(1)
                continue
            deep_match = _DEEP_RE.match(text)
            if deep_match is not None:
                current_question.deep = deep_match.group(1)

        elif isinstance(block, Table):
            if in_appendix:
                appendix_glossary = _parse_terms_table(block)
            elif current is not None and not current.terms:
                current.terms = _parse_terms_table(block)

    finalize_question()

    if len(topics) != len(_TOPIC_SLUGS):
        raise DocxStructureError(
            f"Tìm thấy {len(topics)} chủ đề (Heading 1 dạng 'CHỦ ĐỀ n — ...'), "
            f"cần đúng {len(_TOPIC_SLUGS)}."
        )

    final_topics = [
        HandbookTopic(
            slug=t.slug,
            order=t.order,
            heading=t.heading,
            display_name=t.display_name,
            question_range=t.question_range,
            goal=t.goal,
            terms=t.terms,
            common_mistakes=t.common_mistakes,
            core_examples=t.core_examples,
            questions=t.questions,
        )
        for t in topics
    ]

    return ParsedHandbook(topics=final_topics, glossary=appendix_glossary)
