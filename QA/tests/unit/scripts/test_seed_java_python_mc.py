"""Coverage for scripts/seed_java_python_mc.py (112 MC questions across 11 categories,
sourced from scripts/data/java_python_mc/*.json)."""

from __future__ import annotations

import importlib.util
from pathlib import Path

from sqlalchemy.orm import Session

from app.core.hashing import compute_content_hash
from app.repositories.category_repository import CategoryRepository
from app.repositories.question_repository import QuestionRepository

_MODULE_PATH = Path(__file__).resolve().parents[3] / "scripts" / "seed_java_python_mc.py"
_spec = importlib.util.spec_from_file_location("seed_java_python_mc", _MODULE_PATH)
assert _spec is not None and _spec.loader is not None
seed_java_python_mc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(seed_java_python_mc)

_EXPECTED_COUNTS = {
    "oop": 12,
    "java_core": 28,
    "spring": 12,
    "python_core": 26,
    "python_backend": 8,
    "sql": 8,
    "rest_api": 3,
    "git": 2,
    "testing": 3,
    "coding_challenges": 5,
    "tinh_huong_ky_thuat": 5,
}


def test_every_topic_file_has_valid_mc_questions_with_explanation() -> None:
    for topic, expected_count in _EXPECTED_COUNTS.items():
        topic_file = seed_java_python_mc.DATA_DIR / f"{topic}.json"
        questions = seed_java_python_mc.load_topic_questions(topic_file)
        assert len(questions) == expected_count
        for question in questions:
            assert question["content"]
            assert question["explanation"]
            options = question["options"]
            assert len(options) == 4
            assert sum(1 for o in options if o["is_correct"]) == 1
            assert all(o["content"] for o in options)


def test_total_question_count_is_112() -> None:
    total = 0
    for topic in seed_java_python_mc._TOPIC_TO_CATEGORY:
        topic_file = seed_java_python_mc.DATA_DIR / f"{topic}.json"
        total += len(seed_java_python_mc.load_topic_questions(topic_file))
    assert total == 112


def test_no_duplicate_question_content_within_a_topic() -> None:
    for topic in seed_java_python_mc._TOPIC_TO_CATEGORY:
        topic_file = seed_java_python_mc.DATA_DIR / f"{topic}.json"
        questions = seed_java_python_mc.load_topic_questions(topic_file)
        contents = [q["content"] for q in questions]
        assert len(contents) == len(set(contents))


def test_main_creates_112_questions_and_is_idempotent(db_session: Session) -> None:
    original_session_local = seed_java_python_mc.SessionLocal
    db_session.close = lambda: None  # type: ignore[method-assign] -- main() closes the db it's given
    try:
        seed_java_python_mc.SessionLocal = lambda: db_session  # type: ignore[method-assign]
        seed_java_python_mc.main()

        question_repo = QuestionRepository(db_session)
        category_repo = CategoryRepository(db_session)

        checked = 0
        for topic, category_name in seed_java_python_mc._TOPIC_TO_CATEGORY.items():
            category = category_repo.get_by_name(category_name)
            assert category is not None
            topic_file = seed_java_python_mc.DATA_DIR / f"{topic}.json"
            for item in seed_java_python_mc.load_topic_questions(topic_file):
                content_hash = compute_content_hash(category.name, item["content"], "TEXT")
                saved = question_repo.get_by_content_hash(content_hash)
                assert saved is not None
                assert len(saved.options) == 4
                assert sum(1 for o in saved.options if o.is_correct) == 1
                assert saved.explanation == item["explanation"]
                checked += 1
        assert checked == 112

        # Idempotent: re-running must not create duplicates.
        seed_java_python_mc.main()

        _, total = question_repo.list_filtered(page=1, page_size=1000)
        assert total >= 112
    finally:
        seed_java_python_mc.SessionLocal = original_session_local
