"""Parser + idempotent-insert coverage for scripts/seed_java_python_mc.py (Java/Python
Junior interview MC question bank, 112 questions across 9 sections)."""

from __future__ import annotations

import importlib.util
from pathlib import Path

from sqlalchemy.orm import Session

from app.repositories.category_repository import CategoryRepository
from app.repositories.question_repository import QuestionRepository

_MODULE_PATH = Path(__file__).resolve().parents[3] / "scripts" / "seed_java_python_mc.py"
_spec = importlib.util.spec_from_file_location("seed_java_python_mc", _MODULE_PATH)
assert _spec is not None and _spec.loader is not None
seed_java_python_mc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(seed_java_python_mc)


def test_parses_all_112_questions_with_four_options_each() -> None:
    questions = seed_java_python_mc.load_questions()
    assert len(questions) == 112
    for question in questions:
        assert len(question.option_texts) == 4
        assert all(text for text in question.option_texts)


def test_answer_key_covers_every_question_with_a_valid_letter() -> None:
    text = seed_java_python_mc.BANK_PATH.read_text(encoding="utf-8")
    answer_key = seed_java_python_mc.parse_answer_key(text)
    assert set(answer_key) == set(range(1, 113))
    assert all(letter in "ABCD" for letter in answer_key.values())


def test_section_vi_splits_into_sql_rest_git_testing() -> None:
    questions = {q.number: q for q in seed_java_python_mc.load_questions()}
    assert questions[87].category == "SQL"
    assert questions[91].category == "SQL"
    assert questions[92].category == "REST API"
    assert questions[94].category == "REST API"
    assert questions[95].category == "Git"
    assert questions[96].category == "Git"
    assert questions[97].category == "Testing"
    assert questions[99].category == "Testing"


def test_question_1_correct_answer_matches_answer_key() -> None:
    text = seed_java_python_mc.BANK_PATH.read_text(encoding="utf-8")
    questions = {q.number: q for q in seed_java_python_mc.parse_bank(text)}
    answer_key = seed_java_python_mc.parse_answer_key(text)
    q1 = questions[1]
    options = seed_java_python_mc._options_for(q1, answer_key[1])
    correct = [o for o in options if o["is_correct"]]
    assert len(correct) == 1
    assert correct[0]["content"].startswith("Compiler dịch toàn bộ")


def test_main_creates_valid_mc_questions_and_is_idempotent(db_session: Session) -> None:
    original_session_local = seed_java_python_mc.SessionLocal
    db_session.close = lambda: None  # type: ignore[method-assign] -- main() closes the db it's given
    try:
        seed_java_python_mc.SessionLocal = lambda: db_session  # type: ignore[method-assign]
        seed_java_python_mc.main()

        question_repo = QuestionRepository(db_session)
        category_repo = CategoryRepository(db_session)
        assert len(category_repo.list_all()) > 0

        from app.core.hashing import compute_content_hash

        checked = 0
        for question in seed_java_python_mc.load_questions():
            category = category_repo.get_by_name(question.category)
            assert category is not None
            content_hash = compute_content_hash(category.name, question.content, "TEXT")
            saved = question_repo.get_by_content_hash(content_hash)
            assert saved is not None
            assert len(saved.options) == 4
            assert sum(1 for o in saved.options if o.is_correct) == 1
            checked += 1
        assert checked == 112

        # Idempotent: re-running must not create duplicates.
        seed_java_python_mc.main()

        _, total = question_repo.list_filtered(page=1, page_size=1000)
        assert total == 112
    finally:
        seed_java_python_mc.SessionLocal = original_session_local
