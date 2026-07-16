"""Parser tests for app/practical_review/docx_parser.py. Split into:
- tests against the REAL source DOCX (scripts/data/bo_cau_hoi_thuc_chien_java_python.docx)
  -- the only data source allowed for this feature.
- tests against small synthetic DOCX files built with python-docx, to exercise error
  paths (missing field, duplicate number, wrong topic count) without touching the real
  source file.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from docx import Document

from app.practical_review.docx_parser import DocxStructureError, parse_docx
from app.practical_review.store import DOCX_PATH

pytestmark = pytest.mark.skipif(
    not DOCX_PATH.exists(), reason="scripts/data/bo_cau_hoi_thuc_chien_java_python.docx missing"
)


def _add_question_table(
    document: Document, number: int, question: str, answer: str, explanation: str
) -> None:
    table = document.add_table(rows=1, cols=1)
    cell = table.rows[0].cells[0]
    cell.paragraphs[0].text = f"Câu {number}. {question}"
    cell.add_paragraph(f"Đáp án: {answer}")
    cell.add_paragraph(f"Giải thích: {explanation}")


def _build_minimal_valid_docx(
    path: Path, topic_count: int = 12, questions_per_topic: int = 1
) -> None:
    document = Document()
    number = 1
    for topic_index in range(1, topic_count + 1):
        document.add_heading(f"Chủ đề {topic_index:02d}. Chủ đề số {topic_index}", level=1)
        for _ in range(questions_per_topic):
            _add_question_table(
                document,
                number,
                f"Câu hỏi số {number}?",
                f"Đáp án số {number}",
                f"Giải thích số {number}",
            )
            number += 1
    document.save(str(path))


class TestRealDocx:
    def test_parses_exactly_12_topics(self) -> None:
        parsed = parse_docx(DOCX_PATH)
        assert len(parsed.topics) == 12

    def test_parses_exactly_240_questions(self) -> None:
        parsed = parse_docx(DOCX_PATH)
        assert len(parsed.questions) == 240

    def test_each_topic_has_20_questions(self) -> None:
        parsed = parse_docx(DOCX_PATH)
        for topic in parsed.topics:
            assert topic.question_count == 20

    def test_question_numbers_are_sequential_1_to_240_no_duplicates(self) -> None:
        parsed = parse_docx(DOCX_PATH)
        numbers = [q.number for q in parsed.questions]
        assert sorted(numbers) == list(range(1, 241))
        assert len(numbers) == len(set(numbers))

    def test_every_question_has_non_empty_fields(self) -> None:
        parsed = parse_docx(DOCX_PATH)
        for question in parsed.questions:
            assert question.question.strip()
            assert question.answer.strip()
            assert question.explanation.strip()

    def test_preserves_vietnamese_unicode(self) -> None:
        parsed = parse_docx(DOCX_PATH)
        question_one = next(q for q in parsed.questions if q.number == 1)
        # Real Vietnamese diacritics must round-trip exactly, not mojibake.
        assert (
            "ế" in question_one.question
            or "ự" in question_one.question
            or "ậ" in question_one.question
        )

    def test_topic_slugs_are_unique_and_expected(self) -> None:
        parsed = parse_docx(DOCX_PATH)
        slugs = [t.slug for t in parsed.topics]
        assert len(slugs) == len(set(slugs))
        assert slugs == [
            "oop",
            "java-core",
            "spring",
            "python-core",
            "python-backend",
            "rest-api",
            "sql",
            "testing",
            "git",
            "vibe-coding-ai",
            "coding-challenges",
            "tinh-huong-ky-thuat",
        ]

    def test_does_not_read_java_python_mc_json(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Guard: the parser must only touch the DOCX file, never
        scripts/data/java_python_mc/*.json."""
        import pathlib

        original_read_text = pathlib.Path.read_text

        def _guarded_read_text(self: pathlib.Path, *args: object, **kwargs: object) -> str:
            assert "java_python_mc" not in str(self), f"Parser must not read {self}"
            return original_read_text(self, *args, **kwargs)

        monkeypatch.setattr(pathlib.Path, "read_text", _guarded_read_text)
        parse_docx(DOCX_PATH)


class TestSyntheticDocxErrorPaths:
    def test_valid_minimal_docx_parses(self, tmp_path: Path) -> None:
        path = tmp_path / "valid.docx"
        _build_minimal_valid_docx(path, topic_count=12, questions_per_topic=2)
        parsed = parse_docx(path)
        assert len(parsed.topics) == 12
        assert len(parsed.questions) == 24

    def test_missing_topic_raises(self, tmp_path: Path) -> None:
        path = tmp_path / "missing_topic.docx"
        _build_minimal_valid_docx(path, topic_count=11, questions_per_topic=1)
        with pytest.raises(DocxStructureError, match="chủ đề"):
            parse_docx(path)

    def test_too_many_topics_raises(self, tmp_path: Path) -> None:
        path = tmp_path / "extra_topic.docx"
        _build_minimal_valid_docx(path, topic_count=13, questions_per_topic=1)
        with pytest.raises(DocxStructureError):
            parse_docx(path)

    def test_duplicate_question_number_raises(self, tmp_path: Path) -> None:
        document = Document()
        document.add_heading("Chủ đề 01. A", level=1)
        _add_question_table(document, 1, "Q1?", "A1", "E1")
        _add_question_table(document, 1, "Q1 again?", "A1b", "E1b")
        for topic_index in range(2, 13):
            document.add_heading(f"Chủ đề {topic_index:02d}. Topic {topic_index}", level=1)
            _add_question_table(document, topic_index + 1, f"Q{topic_index}?", "A", "E")
        path = tmp_path / "dup.docx"
        document.save(str(path))
        with pytest.raises(DocxStructureError, match="trùng"):
            parse_docx(path)

    def test_missing_field_in_cell_raises(self, tmp_path: Path) -> None:
        document = Document()
        document.add_heading("Chủ đề 01. A", level=1)
        table = document.add_table(rows=1, cols=1)
        cell = table.rows[0].cells[0]
        cell.paragraphs[0].text = "Câu 1. Question only, no answer or explanation"
        for topic_index in range(2, 13):
            document.add_heading(f"Chủ đề {topic_index:02d}. Topic {topic_index}", level=1)
            _add_question_table(document, topic_index, f"Q{topic_index}?", "A", "E")
        path = tmp_path / "missing_field.docx"
        document.save(str(path))
        with pytest.raises(DocxStructureError):
            parse_docx(path)

    def test_malformed_prefix_raises(self, tmp_path: Path) -> None:
        document = Document()
        document.add_heading("Chủ đề 01. A", level=1)
        table = document.add_table(rows=1, cols=1)
        cell = table.rows[0].cells[0]
        cell.paragraphs[0].text = "Question 1: no Vietnamese prefix"
        cell.add_paragraph("Đáp án: something")
        cell.add_paragraph("Giải thích: something else")
        for topic_index in range(2, 13):
            document.add_heading(f"Chủ đề {topic_index:02d}. Topic {topic_index}", level=1)
            _add_question_table(document, topic_index, f"Q{topic_index}?", "A", "E")
        path = tmp_path / "malformed.docx"
        document.save(str(path))
        with pytest.raises(DocxStructureError):
            parse_docx(path)

    def test_missing_file_raises(self, tmp_path: Path) -> None:
        with pytest.raises(DocxStructureError, match="Không tìm thấy"):
            parse_docx(tmp_path / "does_not_exist.docx")
