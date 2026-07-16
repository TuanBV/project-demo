#!/usr/bin/env python
"""Seed the database from the Java/Python Junior interview MC question bank
(scripts/data/java_python_mc/*.json, 112 questions across 11 categories).

Each JSON file is a plain list of {"content", "explanation", "options": [{"content",
"is_correct"}x4]} objects -- same shape as scripts/data/extended_topics/*.json. Reuses
QuestionService/CategoryService directly to insert MULTIPLE_CHOICE questions -- no separate
seeding logic, per project convention (see scripts/seed.py).

Safe to re-run: each question's content_hash is checked first and existing rows are
skipped, so this can run on every container start without creating duplicates.
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

DATA_DIR = Path(__file__).resolve().parent / "data" / "java_python_mc"

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
    "coding_challenges": "Coding Challenges",
    "tinh_huong_ky_thuat": "Tình huống kỹ thuật",
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
        total_questions = 0
        for topic, category_name in _TOPIC_TO_CATEGORY.items():
            topic_file = DATA_DIR / f"{topic}.json"
            questions = load_topic_questions(topic_file)
            total_questions += len(questions)
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

            total_created += created
            total_skipped += skipped

        print(
            f"Seed Java/Python MC hoàn tất: {total_created} câu được tạo, "
            f"{total_skipped} câu đã tồn tại (tổng {total_questions} câu trong tài liệu)."
        )
    finally:
        db.close()


if __name__ == "__main__":
    main()
