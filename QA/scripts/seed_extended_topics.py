#!/usr/bin/env python
"""Seed the database with ~20 additional multiple-choice interview questions per existing
category (scripts/data/extended_topics/*.json), targeting a mid-level (~3 years experience)
backend developer: OOP, Java Core, Spring, Python Core, Python Backend, SQL, REST API, Git,
Testing, Vibe Coding & AI.

Each JSON file is a plain list of {"content", "explanation", "options": [{"content",
"is_correct"}x4]} objects. Reuses QuestionService/CategoryService directly -- no separate
seeding logic (see scripts/seed.py). Safe to re-run: each question's content_hash is checked
first and existing rows are skipped, so this can run on every container start without
creating duplicates.
"""

from __future__ import annotations

import json
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

DATA_DIR = Path(__file__).resolve().parent / "data" / "extended_topics"

_TOPIC_TO_CATEGORY = {
    "oop": "OOP",
    "java_core": "Java Core",
    "spring": "Spring",
    "python_core": "Python Core",
    "python_backend": "Python Backend",
    "sql": "SQL",
    "rest_api": "REST API",
    "git": "Git",
    "testing": "Testing",
    "vibe_coding_ai": "Vibe Coding & AI",
}


def load_topic_questions(topic_file: Path) -> list[dict]:
    return json.loads(topic_file.read_text(encoding="utf-8"))


def main() -> None:
    db = SessionLocal()
    try:
        category_service = CategoryService(CategoryRepository(db))
        question_service = QuestionService(QuestionRepository(db), CategoryRepository(db))
        question_repo = QuestionRepository(db)

        total_created = 0
        total_skipped = 0
        for topic, category_name in _TOPIC_TO_CATEGORY.items():
            topic_file = DATA_DIR / f"{topic}.json"
            questions = load_topic_questions(topic_file)
            category = category_service.get_or_create_by_name(category_name)

            created = 0
            skipped = 0
            for item in questions:
                content_hash = compute_content_hash(category.name, item["content"], "TEXT")
                if question_repo.get_by_content_hash(content_hash) is not None:
                    skipped += 1
                    continue

                data = AdminQuestionCreate(
                    category_id=category.id,
                    question_format=QuestionFormat.MULTIPLE_CHOICE,
                    content=item["content"],
                    explanation=item.get("explanation"),
                    options=item["options"],
                )
                question_service.create(data, source_type="SEED")
                created += 1

            print(f"{category_name}: {created} câu được tạo, {skipped} câu đã tồn tại")
            total_created += created
            total_skipped += skipped

        print(
            f"Seed extended topics hoàn tất: {total_created} câu được tạo, "
            f"{total_skipped} câu đã tồn tại."
        )
    finally:
        db.close()


if __name__ == "__main__":
    main()
