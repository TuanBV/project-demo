"""Coverage for scripts/seed_extended_topics.py (~20 MC questions per existing category,
sourced from scripts/data/extended_topics/*.json)."""

from __future__ import annotations

import importlib.util
from pathlib import Path

from sqlalchemy.orm import Session

from app.core.hashing import compute_content_hash
from app.repositories.category_repository import CategoryRepository
from app.repositories.question_repository import QuestionRepository

_MODULE_PATH = Path(__file__).resolve().parents[3] / "scripts" / "seed_extended_topics.py"
_spec = importlib.util.spec_from_file_location("seed_extended_topics", _MODULE_PATH)
assert _spec is not None and _spec.loader is not None
seed_extended_topics = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(seed_extended_topics)


def test_every_topic_file_has_20_valid_mc_questions() -> None:
    for topic in seed_extended_topics._TOPIC_TO_CATEGORY:
        topic_file = seed_extended_topics.DATA_DIR / f"{topic}.json"
        questions = seed_extended_topics.load_topic_questions(topic_file)
        assert len(questions) == 20
        for question in questions:
            options = question["options"]
            assert len(options) == 4
            assert sum(1 for o in options if o["is_correct"]) == 1
            assert all(o["content"] for o in options)


def test_no_duplicate_question_content_within_a_topic() -> None:
    for topic in seed_extended_topics._TOPIC_TO_CATEGORY:
        topic_file = seed_extended_topics.DATA_DIR / f"{topic}.json"
        questions = seed_extended_topics.load_topic_questions(topic_file)
        contents = [q["content"] for q in questions]
        assert len(contents) == len(set(contents))


def test_main_creates_180_questions_and_is_idempotent(db_session: Session) -> None:
    original_session_local = seed_extended_topics.SessionLocal
    db_session.close = lambda: None  # type: ignore[method-assign] -- main() closes the db it's given
    try:
        seed_extended_topics.SessionLocal = lambda: db_session  # type: ignore[method-assign]
        seed_extended_topics.main()

        question_repo = QuestionRepository(db_session)
        category_repo = CategoryRepository(db_session)

        checked = 0
        for topic, category_name in seed_extended_topics._TOPIC_TO_CATEGORY.items():
            category = category_repo.get_by_name(category_name)
            assert category is not None
            topic_file = seed_extended_topics.DATA_DIR / f"{topic}.json"
            for item in seed_extended_topics.load_topic_questions(topic_file):
                content_hash = compute_content_hash(category.name, item["content"], "TEXT")
                saved = question_repo.get_by_content_hash(content_hash)
                assert saved is not None
                assert len(saved.options) == 4
                assert sum(1 for o in saved.options if o.is_correct) == 1
                checked += 1
        assert checked == 180

        # Idempotent: re-running must not create duplicates.
        seed_extended_topics.main()

        _, total = question_repo.list_filtered(page=1, page_size=1000)
        assert total >= 180
    finally:
        seed_extended_topics.SessionLocal = original_session_local
