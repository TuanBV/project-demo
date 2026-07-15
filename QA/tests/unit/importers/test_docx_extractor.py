from __future__ import annotations

import io

import docx
import pytest

from app.core.exceptions import MalformedDocumentError
from app.importers.docx_extractor import DocxTextExtractor
from app.importers.text_parser import QuestionTextParser

extractor = DocxTextExtractor()
parser = QuestionTextParser()


def _build_docx(paragraphs: list[str]) -> bytes:
    document = docx.Document()
    for text in paragraphs:
        document.add_paragraph(text)
    buffer = io.BytesIO()
    document.save(buffer)
    return buffer.getvalue()


def test_extract_preserves_paragraph_order() -> None:
    content = _build_docx(
        ["PHAN I - JAVA CORE", "", "Cau 1. JVM la gi?", "", "Tra loi: JVM thuc thi bytecode."]
    )
    text = extractor.extract(content)
    doc = parser.parse(text)
    assert doc.questions[0].category_name == "JAVA CORE"
    assert doc.questions[0].content == "JVM la gi?"
    assert doc.questions[0].reference_answer == "JVM thuc thi bytecode."


def test_extract_recognizes_java_python_sql_and_explanation() -> None:
    content = _build_docx(
        [
            "PHAN VII - BAI CODING KEM DAP AN",
            "",
            "Bai 1. Tim phan tu lon nhat",
            "",
            "Tra loi: Duyet mang mot lan.",
            "",
            "Dap an Java:",
            "public int max(int[] a) { return 0; }",
            "",
            "Dap an Python:",
            "def max_val(a): return max(a)",
            "",
            "Diem can danh gia:",
            "O(n) thoi gian, O(1) bo nho.",
        ]
    )
    text = extractor.extract(content)
    doc = parser.parse(text)
    q = doc.questions[0]
    assert q.question_type == "CODE"
    assert "public int max" in q.java_answer
    assert "def max_val" in q.python_answer
    assert "O(n)" in q.explanation


def test_non_contiguous_numbering_in_docx() -> None:
    content = _build_docx(
        [
            "Cau 1. Q1?",
            "",
            "Tra loi: A1.",
            "",
            "Cau 9. Q2?",
            "",
            "Tra loi: A2.",
        ]
    )
    text = extractor.extract(content)
    doc = parser.parse(text)
    assert len(doc.questions) == 2


def test_invalid_docx_file_raises() -> None:
    with pytest.raises(MalformedDocumentError):
        extractor.extract(b"not a real docx file at all")


def test_docx_with_no_text_raises() -> None:
    empty_docx = _build_docx([])
    with pytest.raises(MalformedDocumentError):
        extractor.extract(empty_docx)
