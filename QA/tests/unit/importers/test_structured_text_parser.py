from __future__ import annotations

from app.importers.structured_text_parser import StructuredTextParser

parser = StructuredTextParser()


def test_parses_category_question_answer_format() -> None:
    content = (
        "CATEGORY: Java Core\n"
        "TYPE: TEXT\n"
        "QUESTION: JVM la gi?\n"
        "ANSWER: JVM thuc thi bytecode.\n"
        "KEYWORDS: jvm, bytecode\n"
        "---\n"
    )
    doc = parser.parse(content)
    assert len(doc.questions) == 1
    q = doc.questions[0]
    assert q.category_name == "Java Core"
    assert q.content == "JVM la gi?"
    assert q.reference_answer == "JVM thuc thi bytecode."
    assert q.keywords == ["jvm", "bytecode"]


def test_field_names_case_insensitive() -> None:
    content = "category: Python Core\nquestion: Generator la gi?\nanswer: Sinh du lieu lazy.\n"
    doc = parser.parse(content)
    assert doc.questions[0].category_name == "Python Core"


def test_separator_splits_multiple_questions() -> None:
    content = (
        "CATEGORY: A\nQUESTION: Q1?\nANSWER: A1.\n---\nCATEGORY: B\nQUESTION: Q2?\nANSWER: A2.\n"
    )
    doc = parser.parse(content)
    assert len(doc.questions) == 2
    assert doc.questions[0].category_name == "A"
    assert doc.questions[1].category_name == "B"


def test_missing_category_allowed() -> None:
    content = "QUESTION: Q khong co category?\nANSWER: A.\n"
    doc = parser.parse(content)
    assert doc.questions[0].category_name is None


def test_missing_answer_produces_warning() -> None:
    content = "CATEGORY: A\nQUESTION: Q thieu dap an?\n"
    doc = parser.parse(content)
    assert doc.questions[0].reference_answer is None
    assert any("đáp án" in w.lower() for w in doc.questions[0].warnings)


def test_missing_question_skips_block() -> None:
    content = "CATEGORY: A\nANSWER: A khong co cau hoi.\n"
    doc = parser.parse(content)
    assert len(doc.questions) == 0


def test_multiple_questions_in_one_text() -> None:
    content = "\n".join(f"CATEGORY: Cat{i}\nQUESTION: Q{i}?\nANSWER: A{i}.\n---" for i in range(5))
    doc = parser.parse(content)
    assert len(doc.questions) == 5


def test_multiline_code_answer() -> None:
    content = (
        "CATEGORY: Code\nTYPE: CODE\nQUESTION: Viet ham cong hai so\n"
        "ANSWER: Cong hai bien.\n"
        "JAVA_ANSWER: public int add(int a, int b) {\n    return a + b;\n}\n"
    )
    doc = parser.parse(content)
    assert "return a + b;" in doc.questions[0].java_answer


def test_multiline_sql_answer() -> None:
    content = (
        "CATEGORY: SQL\nTYPE: SQL\nQUESTION: Dem so don hang\n"
        "ANSWER: Dung group by.\n"
        "SQL_ANSWER: SELECT customer_id, COUNT(*)\nFROM orders\nGROUP BY customer_id;\n"
    )
    doc = parser.parse(content)
    assert "GROUP BY customer_id;" in doc.questions[0].sql_answer


def test_can_parse_detects_structured_format() -> None:
    assert parser.can_parse("QUESTION: abc?\nANSWER: def.\n")
    assert not parser.can_parse("Cau 1. abc?\nTra loi: def.\n")


def test_parses_abcd_options_and_correct_letter() -> None:
    content = (
        "CATEGORY: Java Core\n"
        "QUESTION: JVM la gi?\n"
        "A: Cong cu bien dich.\n"
        "B: May ao thuc thi Java bytecode.\n"
        "C: Thu vien giao dien.\n"
        "D: He quan tri CSDL.\n"
        "CORRECT: B\n"
    )
    doc = parser.parse(content)
    q = doc.questions[0]
    assert q.options == [
        "Cong cu bien dich.",
        "May ao thuc thi Java bytecode.",
        "Thu vien giao dien.",
        "He quan tri CSDL.",
    ]
    assert q.correct_option_index == 1
    assert q.reference_answer == "May ao thuc thi Java bytecode."


def test_parses_option_field_and_correct_option_number() -> None:
    content = (
        "CATEGORY: Java Core\n"
        "QUESTION: JVM la gi?\n"
        "OPTION: Cong cu bien dich.\n"
        "OPTION: May ao thuc thi Java bytecode.\n"
        "OPTION: Thu vien giao dien.\n"
        "OPTION: He quan tri CSDL.\n"
        "CORRECT_OPTION: 2\n"
    )
    doc = parser.parse(content)
    q = doc.questions[0]
    assert len(q.options) == 4
    assert q.correct_option_index == 1


def test_invalid_correct_letter_produces_warning() -> None:
    content = "CATEGORY: Cat\nQUESTION: Q?\nA: 1\nB: 2\nC: 3\nD: 4\nCORRECT: Z\n"
    doc = parser.parse(content)
    q = doc.questions[0]
    assert q.correct_option_index is None
    assert any("CORRECT" in w for w in q.warnings)


def test_invalid_correct_option_number_produces_warning() -> None:
    content = (
        "CATEGORY: Cat\nQUESTION: Q?\nOPTION: 1\nOPTION: 2\nOPTION: 3\nOPTION: 4\n"
        "CORRECT_OPTION: 9\n"
    )
    doc = parser.parse(content)
    q = doc.questions[0]
    assert q.correct_option_index is None
    assert any("CORRECT_OPTION" in w for w in q.warnings)
