#!/usr/bin/env python
"""Seed the database from the Java/Python Junior interview MC question bank
(scripts/data/java_python_mc_question_bank.txt, 112 questions across 9 sections).

Parses the plain-text bank (PHẦN <section header>, "Câu N. <question>", A/B/C/D options,
and a trailing "BẢNG ĐÁP ÁN" answer-key table mapping question number -> correct letter),
then reuses QuestionService/CategoryService directly to insert MULTIPLE_CHOICE questions --
no separate seeding logic, per project convention (see scripts/seed.py).

Safe to re-run: each question's content_hash is checked first and existing rows are
skipped, so this can run on every container start without creating duplicates.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.hashing import compute_content_hash  # noqa: E402
from app.db.models.enums import QuestionFormat  # noqa: E402
from app.db.session import SessionLocal  # noqa: E402
from app.repositories.category_repository import CategoryRepository  # noqa: E402
from app.repositories.question_repository import QuestionRepository  # noqa: E402
from app.schemas.question import AdminQuestionCreate  # noqa: E402
from app.services.category_service import CategoryService  # noqa: E402
from app.services.question_service import QuestionService  # noqa: E402

BANK_PATH = Path(__file__).resolve().parent / "data" / "java_python_mc_question_bank.txt"

_SECTION_RE = re.compile(r"^PHẦN\s+([IVX]+)\s*[–-]\s*(.+)$")
_QUESTION_RE = re.compile(r"^Câu\s+(\d+)(?:\s*\([^)]*\))?\.\s*(.*)$")
_OPTION_RE = re.compile(r"^([ABCD])\.\s?(.*)$")
_ANSWER_ENTRY_RE = re.compile(r"(\d+)\s*:\s*([ABCD])")

# Section roman numeral -> default category. Overridden per-question-number below for
# sections that mix multiple topics (VI) or that map to a single shared category (VII-IX).
_SECTION_CATEGORY = {
    "I": "OOP",
    "II": "Java Core",
    "III": "Spring",
    "IV": "Python Core",
    "V": "Python Backend",
    "VI": "SQL",  # overridden per-range below
    "VII": "Coding Challenges",
    "VIII": "SQL",
    "IX": "Tình huống kỹ thuật",
}

# Section VI covers SQL, REST API, Git and Testing questions in that order.
_SECTION_VI_OVERRIDES: dict[range, str] = {
    range(87, 92): "SQL",
    range(92, 95): "REST API",
    range(95, 97): "Git",
    range(97, 100): "Testing",
}


def _category_for(number: int, section_roman: str) -> str:
    if section_roman == "VI":
        for rng, name in _SECTION_VI_OVERRIDES.items():
            if number in rng:
                return name
    return _SECTION_CATEGORY[section_roman]


class _ParsedQuestion:
    def __init__(self, number: int, category: str, content: str) -> None:
        self.number = number
        self.category = category
        self.content = content
        self.option_texts: list[str] = []


def parse_bank(text: str) -> list[_ParsedQuestion]:
    lines = text.split("\n")
    questions: list[_ParsedQuestion] = []
    current_section = "I"
    current: _ParsedQuestion | None = None
    current_option: str | None = None

    def flush_option() -> None:
        nonlocal current_option
        current_option = None

    for line in lines:
        section_match = _SECTION_RE.match(line.strip())
        if section_match:
            current_section = section_match.group(1)
            current = None
            flush_option()
            continue

        if line.strip().startswith("BẢNG ĐÁP ÁN"):
            break

        question_match = _QUESTION_RE.match(line.strip())
        if question_match:
            number = int(question_match.group(1))
            category = _category_for(number, current_section)
            current = _ParsedQuestion(number, category, question_match.group(2).strip())
            questions.append(current)
            flush_option()
            continue

        option_match = _OPTION_RE.match(line.strip())
        if option_match and current is not None:
            current.option_texts.append(option_match.group(2).strip())
            current_option = option_match.group(1)
            continue

        if current_option is not None and current is not None and line.strip():
            current.option_texts[-1] = f"{current.option_texts[-1]} {line.strip()}"

    return questions


def parse_answer_key(text: str) -> dict[int, str]:
    idx = text.find("BẢNG ĐÁP ÁN")
    if idx == -1:
        raise ValueError("Không tìm thấy BẢNG ĐÁP ÁN trong tài liệu")
    table_text = text[idx:]
    end_idx = table_text.find("Ghi chú")
    if end_idx != -1:
        table_text = table_text[:end_idx]
    return {int(number): letter for number, letter in _ANSWER_ENTRY_RE.findall(table_text)}


_LETTER_TO_INDEX = {"A": 0, "B": 1, "C": 2, "D": 3}


def load_questions(bank_path: Path = BANK_PATH) -> list[_ParsedQuestion]:
    text = bank_path.read_text(encoding="utf-8")
    questions = parse_bank(text)
    answer_key = parse_answer_key(text)

    for question in questions:
        if len(question.option_texts) != 4:
            raise ValueError(
                f"Câu {question.number} có {len(question.option_texts)} đáp án, cần đúng 4"
            )
        if question.number not in answer_key:
            raise ValueError(f"Câu {question.number} thiếu đáp án đúng trong bảng đáp án")

    return questions


def _options_for(question: _ParsedQuestion, correct_letter: str) -> list[dict]:
    correct_index = _LETTER_TO_INDEX[correct_letter]
    return [
        {"content": text, "is_correct": i == correct_index}
        for i, text in enumerate(question.option_texts)
    ]


def main() -> None:
    text = BANK_PATH.read_text(encoding="utf-8")
    questions = parse_bank(text)
    answer_key = parse_answer_key(text)

    db = SessionLocal()
    try:
        category_service = CategoryService(CategoryRepository(db))
        question_service = QuestionService(QuestionRepository(db), CategoryRepository(db))
        question_repo = QuestionRepository(db)

        created = 0
        skipped = 0
        for question in questions:
            if len(question.option_texts) != 4:
                print(
                    f"Bỏ qua câu {question.number}: có {len(question.option_texts)} "
                    "đáp án, cần đúng 4"
                )
                continue
            correct_letter = answer_key.get(question.number)
            if correct_letter is None:
                print(f"Bỏ qua câu {question.number}: thiếu đáp án đúng trong bảng đáp án")
                continue

            category = category_service.get_or_create_by_name(question.category)
            content_hash = compute_content_hash(category.name, question.content, "TEXT")
            if question_repo.get_by_content_hash(content_hash) is not None:
                skipped += 1
                continue

            data = AdminQuestionCreate(
                category_id=category.id,
                question_format=QuestionFormat.MULTIPLE_CHOICE,
                content=question.content,
                options=_options_for(question, correct_letter),
            )
            question_service.create(data, source_type="SEED")
            created += 1

        print(
            f"Seed Java/Python MC hoàn tất: {created} câu được tạo, "
            f"{skipped} câu đã tồn tại (tổng {len(questions)} câu trong tài liệu)."
        )
    finally:
        db.close()


if __name__ == "__main__":
    main()
