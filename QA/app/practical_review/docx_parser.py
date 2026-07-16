"""Parses scripts/data/bo_cau_hoi_thuc_chien_java_python.docx -- the ONLY data source for
the practical-review area. Must never import or read anything under
scripts/data/java_python_mc/ or scripts/data/extended_topics/.

Expected structure (verified against the actual file before writing this parser):
  - Exactly 12 "Heading 1" paragraphs, one per topic, in document order.
  - Between headings, each question is a one-cell table whose cell contains exactly three
    non-empty paragraphs, in order:
      "Câu <n>. <question text>"
      "Đáp án: <answer text>"
      "Giải thích: <explanation text>"
  - Question numbers are globally sequential 1..240 with no gaps or duplicates.

Pure Python + python-docx only -- no FastAPI, no SQLAlchemy, importable standalone by both
scripts/extract_practical_review_docx.py and the FastAPI app.
"""

from __future__ import annotations

import re
from pathlib import Path

from docx import Document as _open_docx
from docx.document import Document
from docx.table import Table
from docx.text.paragraph import Paragraph

from app.practical_review.models import ParsedDocument, PracticalQuestion, PracticalTopic

# Positional (slug, ui_group) for the 12 topics, in the exact order they appear in the DOCX.
# The display name itself is taken from the DOCX heading text, never hardcoded here --
# slug/group are navigation metadata invented for this app, not source content.
_TOPIC_SLUGS_AND_GROUPS: list[tuple[str, str]] = [
    ("oop", "Java"),
    ("java-core", "Java"),
    ("spring", "Java"),
    ("python-core", "Python"),
    ("python-backend", "Python"),
    ("rest-api", "Backend nền tảng"),
    ("sql", "Backend nền tảng"),
    ("testing", "Backend nền tảng"),
    ("git", "Backend nền tảng"),
    ("vibe-coding-ai", "Thực chiến"),
    ("coding-challenges", "Thực chiến"),
    ("tinh-huong-ky-thuat", "Thực chiến"),
]

_HEADING_PREFIX_RE = re.compile(r"^Chủ đề\s+\d+\.\s*(.*)$")
_QUESTION_RE = re.compile(r"^Câu\s+(\d+)\.\s*(.*)$")
_ANSWER_RE = re.compile(r"^Đáp án:\s*(.*)$")
_EXPLANATION_RE = re.compile(r"^Giải thích:\s*(.*)$")


class DocxStructureError(ValueError):
    """Raised when the DOCX doesn't match the expected practical-review structure. Carries
    enough detail to fix the source file or the parser, never silently drops data."""


def _iter_block_items(document: Document):
    """Yield Paragraph/Table objects in actual document order (python-docx's own
    .paragraphs/.tables lists are separate and lose interleaving order)."""
    body = document.element.body
    for child in body.iterchildren():
        if child.tag.endswith("}p"):
            yield Paragraph(child, document)
        elif child.tag.endswith("}tbl"):
            yield Table(child, document)


def parse_docx(path: str | Path) -> ParsedDocument:
    path = Path(path)
    if not path.exists():
        raise DocxStructureError(f"Không tìm thấy file DOCX: {path}")

    document = _open_docx(str(path))

    topics: list[PracticalTopic] = []
    questions: list[PracticalQuestion] = []
    current_slug: str | None = None
    current_topic_name: str | None = None
    topic_question_counts: dict[str, int] = {}
    seen_numbers: set[int] = set()

    for block in _iter_block_items(document):
        if isinstance(block, Paragraph):
            if block.style and block.style.name == "Heading 1":
                heading = block.text.strip()
                order = len(topics) + 1
                if order > len(_TOPIC_SLUGS_AND_GROUPS):
                    raise DocxStructureError(
                        f"Tìm thấy nhiều hơn {len(_TOPIC_SLUGS_AND_GROUPS)} chủ đề "
                        f"(Heading 1) trong DOCX; chủ đề thừa: {heading!r}"
                    )
                slug, group = _TOPIC_SLUGS_AND_GROUPS[order - 1]
                match = _HEADING_PREFIX_RE.match(heading)
                display_name = match.group(1).strip() if match else heading
                current_slug = slug
                current_topic_name = heading
                topic_question_counts[slug] = 0
                topics.append(
                    PracticalTopic(
                        slug=slug,
                        order=order,
                        heading=heading,
                        display_name=display_name,
                        group=group,
                        question_count=0,  # filled in after the full pass below
                    )
                )
        elif isinstance(block, Table):
            if current_slug is None or current_topic_name is None:
                raise DocxStructureError(
                    "Tìm thấy table câu hỏi trước khi có Heading 1 chủ đề nào -- DOCX không "
                    "đúng cấu trúc mong đợi."
                )
            cell = block.rows[0].cells[0]
            paragraphs = [p.text.strip() for p in cell.paragraphs if p.text.strip()]
            if len(paragraphs) != 3:
                raise DocxStructureError(
                    f"Câu hỏi trong chủ đề {current_topic_name!r} có {len(paragraphs)} dòng "
                    f"nội dung (cần đúng 3: Câu/Đáp án/Giải thích). Nội dung: {paragraphs!r}"
                )
            q_line, a_line, e_line = paragraphs
            q_match = _QUESTION_RE.match(q_line)
            a_match = _ANSWER_RE.match(a_line)
            e_match = _EXPLANATION_RE.match(e_line)
            if not (q_match and a_match and e_match):
                raise DocxStructureError(
                    f"Câu hỏi trong chủ đề {current_topic_name!r} không đúng định dạng "
                    f"'Câu N. .../Đáp án: .../Giải thích: ...'. Nội dung: {paragraphs!r}"
                )

            number = int(q_match.group(1))
            if number in seen_numbers:
                raise DocxStructureError(f"Số thứ tự câu hỏi bị trùng: Câu {number}")
            seen_numbers.add(number)

            question_text = q_match.group(2).strip()
            answer_text = a_match.group(1).strip()
            explanation_text = e_match.group(1).strip()
            if not question_text or not answer_text or not explanation_text:
                raise DocxStructureError(
                    f"Câu {number} thiếu nội dung ở một trong ba trường câu hỏi/đáp án/giải thích."
                )

            questions.append(
                PracticalQuestion(
                    number=number,
                    topic_slug=current_slug,
                    topic_name=current_topic_name,
                    question=question_text,
                    answer=answer_text,
                    explanation=explanation_text,
                )
            )
            topic_question_counts[current_slug] += 1

    if len(topics) != len(_TOPIC_SLUGS_AND_GROUPS):
        raise DocxStructureError(
            f"Tìm thấy {len(topics)} chủ đề (Heading 1), cần đúng {len(_TOPIC_SLUGS_AND_GROUPS)}."
        )

    if questions:
        expected_range = set(range(1, len(questions) + 1))
        missing = sorted(expected_range - seen_numbers)
        if missing:
            raise DocxStructureError(
                f"Thiếu số thứ tự câu hỏi liên tục 1..{len(questions)}: {missing}"
            )

    topics = [
        PracticalTopic(
            slug=t.slug,
            order=t.order,
            heading=t.heading,
            display_name=t.display_name,
            group=t.group,
            question_count=topic_question_counts.get(t.slug, 0),
        )
        for t in topics
    ]

    return ParsedDocument(topics=topics, questions=questions)
