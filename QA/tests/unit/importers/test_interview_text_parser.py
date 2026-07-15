from __future__ import annotations

from app.importers.interview_text_parser import InterviewDocumentParser

parser = InterviewDocumentParser()


def test_recognizes_category() -> None:
    content = (
        "PHAN I - NEN TANG OOP\n\nCau 1. Compiler la gi?\n\nTra loi: Bien dich toan bo ma nguon.\n"
    )
    doc = parser.parse(content)
    assert doc.questions[0].category_name == "NEN TANG OOP"


def test_recognizes_question() -> None:
    content = "Cau 1. Mutable la gi?\n\nTra loi: Co the thay doi.\n"
    doc = parser.parse(content)
    assert doc.questions[0].content == "Mutable la gi?"


def test_recognizes_answer() -> None:
    content = "Cau 1. Q?\n\nTra loi: Day la dap an.\n"
    doc = parser.parse(content)
    assert doc.questions[0].reference_answer == "Day la dap an."


def test_recognizes_java_answer() -> None:
    content = (
        "PHAN CODING\n\nBai 1. Viet ham cong\n\n"
        "Dap an Java:\npublic int add(int a, int b) { return a+b; }\n"
    )
    doc = parser.parse(content)
    assert "return a+b" in doc.questions[0].java_answer


def test_recognizes_python_answer() -> None:
    content = "Bai 1. Viet ham cong\n\nDap an Python:\ndef add(a, b):\n    return a + b\n"
    doc = parser.parse(content)
    assert "return a + b" in doc.questions[0].python_answer


def test_recognizes_sql_answer() -> None:
    content = "Bai 1. Dem don hang\n\nDap an SQL:\nSELECT COUNT(*) FROM orders;\n"
    doc = parser.parse(content)
    assert "SELECT COUNT(*)" in doc.questions[0].sql_answer


def test_recognizes_diem_can_danh_gia() -> None:
    content = (
        "Bai 1. Toi uu thuat toan\n\nTra loi: dung hai con tro.\n\n"
        "Diem can danh gia:\nO(n) thoi gian, O(1) bo nho.\n"
    )
    doc = parser.parse(content)
    assert "O(n)" in doc.questions[0].explanation


def test_question_type_from_section_header() -> None:
    content = "PHAN VII - BAI CODING KEM DAP AN\n\nBai 1. Viet ham\n\nTra loi: dung vong lap.\n"
    doc = parser.parse(content)
    assert doc.questions[0].question_type == "CODE"

    content_sql = "PHAN VIII - BAI SQL\n\nBai 1. Viet query\n\nTra loi: dung join.\n"
    doc_sql = parser.parse(content_sql)
    assert doc_sql.questions[0].question_type == "SQL"

    content_scenario = (
        "PHAN IX - TINH HUONG XU LY\n\nCau 1. Ban se lam gi?\n\nTra loi: Kiem tra log.\n"
    )
    doc_scenario = parser.parse(content_scenario)
    assert doc_scenario.questions[0].question_type == "SCENARIO"

    content_text = "PHAN I - CO BAN\n\nCau 1. La gi?\n\nTra loi: Dinh nghia co ban.\n"
    doc_text = parser.parse(content_text)
    assert doc_text.questions[0].question_type == "TEXT"


def test_non_contiguous_numbering() -> None:
    content = (
        "Cau 1. Q1?\n\nTra loi: A1.\n\nCau 5. Q2?\n\nTra loi: A2.\n\nCau 2. Q3?\n\nTra loi: A3.\n"
    )
    doc = parser.parse(content)
    assert len(doc.questions) == 3
    assert [q.content for q in doc.questions] == ["Q1?", "Q2?", "Q3?"]


def test_multi_line_paragraph_answer() -> None:
    content = "Cau 1. Q?\n\nTra loi: Dong thu nhat.\nDong thu hai.\nDong thu ba.\n"
    doc = parser.parse(content)
    answer = doc.questions[0].reference_answer
    assert "Dong thu nhat." in answer
    assert "Dong thu ba." in answer


def test_invalid_content_produces_no_questions() -> None:
    doc = parser.parse("Khong co gi lien quan den cau hoi ca, chi la van ban thuong.")
    assert doc.questions == []


def test_content_with_no_questions_returns_empty_and_unparsed() -> None:
    doc = parser.parse("PHAN I - CHUONG TRINH\n\nDay chi la mot doan gioi thieu khong co cau hoi.")
    assert doc.questions == []
