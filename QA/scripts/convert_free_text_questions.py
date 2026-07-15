#!/usr/bin/env python
"""Convert legacy FREE_TEXT questions to MULTIPLE_CHOICE drafts (spec section 19).

Never destroys existing data: reference_answer/concepts/keywords/contradiction_rules stay
untouched (kept as historical context, visible in the admin edit screen) -- only
question_format/needs_review/active and the new 4-option set are written. Converted
questions are always created with needs_review=True, active=False so nothing reaches
learners until an admin reviews the auto-generated distractors.

Usage:
    python scripts/convert_free_text_questions.py --dry-run
    python scripts/convert_free_text_questions.py
    python scripts/convert_free_text_questions.py --generate-distractors
"""

from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import select  # noqa: E402

from app.db.models.enums import QuestionFormat  # noqa: E402
from app.db.models.question import Question  # noqa: E402
from app.db.session import SessionLocal  # noqa: E402
from app.importers.distractor_generator import RuleBasedDistractorGenerator  # noqa: E402
from app.services.question_option_service import OptionInput, QuestionOptionService  # noqa: E402

_MAX_SIBLING_CONTEXT = 10


def _placeholder_options(correct_answer: str) -> list[OptionInput]:
    options = [OptionInput(content=correct_answer, is_correct=True)]
    for i in range(1, 4):
        options.append(
            OptionInput(
                content=f"Cần quản trị viên nhập đáp án sai #{i}",
                is_correct=False,
                auto_generated=True,
            )
        )
    return options


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert legacy FREE_TEXT questions to MULTIPLE_CHOICE drafts"
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--generate-distractors",
        action="store_true",
        help="Attempt real distractor generation (confusable-term swap + sibling context) "
        "instead of leaving plain 'cần nhập đáp án sai' placeholders.",
    )
    args = parser.parse_args()

    db = SessionLocal()
    try:
        option_service = QuestionOptionService()
        generator = RuleBasedDistractorGenerator()

        stmt = select(Question).where(Question.question_format == QuestionFormat.FREE_TEXT)
        candidates = list(db.execute(stmt).scalars().all())

        by_category: dict[int, list[str]] = defaultdict(list)
        for q in candidates:
            if q.reference_answer:
                by_category[q.category_id].append(q.reference_answer)

        total = len(candidates)
        converted = 0
        needs_review = 0
        errors = 0

        for question in candidates:
            if not question.reference_answer or not question.reference_answer.strip():
                errors += 1
                print(f"[LỖI] Question {question.id}: không có reference_answer để chuyển đổi")
                continue

            correct_answer = question.reference_answer.strip()
            if args.generate_distractors:
                context = [
                    a for a in by_category.get(question.category_id, []) if a != correct_answer
                ][:_MAX_SIBLING_CONTEXT]
                distractors = generator.generate(question.content, correct_answer, context, count=3)
                options = [OptionInput(content=correct_answer, is_correct=True)]
                options.extend(
                    OptionInput(content=d, is_correct=False, auto_generated=True)
                    for d in distractors
                )
            else:
                options = _placeholder_options(correct_answer)

            if not args.dry_run:
                option_service.replace_options(question, options)
                question.question_format = QuestionFormat.MULTIPLE_CHOICE
                question.needs_review = True
                question.active = False

            converted += 1
            needs_review += 1
            print(
                f"[OK] Question {question.id}: {question.content[:60]!r} "
                "-> MULTIPLE_CHOICE (needs_review)"
            )

        if not args.dry_run:
            db.commit()

        print()
        print(f"Tổng số câu FREE_TEXT: {total}")
        print(f"Số câu chuyển đổi được: {converted}")
        print(f"Số câu cần review: {needs_review}")
        print(f"Số câu lỗi: {errors}")
        if args.dry_run:
            print("(dry-run: không có thay đổi nào được ghi vào database)")
    finally:
        db.close()


if __name__ == "__main__":
    main()
