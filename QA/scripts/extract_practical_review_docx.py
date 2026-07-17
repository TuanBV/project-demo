#!/usr/bin/env python
"""Extract + validate scripts/data/so_tay_on_tap_sap_xep_theo_chu_de_uu_tien.docx and print a
report.

This script is a standalone diagnostic/regeneration tool for the practical-review area --
the running FastAPI app does NOT depend on its output; it parses the DOCX directly at
startup via app.practical_review.store.get_store() (cached in memory, parsed once).

Running this script writes app/practical_review/generated/questions.json, a deterministic,
UTF-8, human-inspectable dump of the same parse for offline review/debugging. Re-running it
against an unchanged DOCX reproduces the same topics/questions content every time (only the
"generated_at" timestamp differs).

Usage:
    python scripts/extract_practical_review_docx.py [--check-only]

--check-only: run validation and print the report without writing the generated JSON file.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.practical_review.docx_parser import DocxStructureError, parse_docx  # noqa: E402
from app.practical_review.store import DOCX_PATH, PROJECT_ROOT  # noqa: E402

GENERATED_DIR = Path(__file__).resolve().parent.parent / "app" / "practical_review" / "generated"
GENERATED_PATH = GENERATED_DIR / "questions.json"


def build_report(document) -> list[str]:  # type: ignore[no-untyped-def]
    lines = []
    lines.append(f"Tổng số chủ đề: {len(document.topics)}")
    lines.append(f"Tổng số câu hỏi: {len(document.questions)}")
    lines.append("")
    lines.append("Chi tiết theo chủ đề:")
    for topic in sorted(document.topics, key=lambda t: t.order):
        lines.append(
            f"  {topic.order:2d}. [{topic.slug}] {topic.display_name} "
            f"({topic.question_count} câu, nhóm: {topic.group})"
        )
    return lines


def to_generated_payload(document) -> dict:  # type: ignore[no-untyped-def]
    return {
        "source": DOCX_PATH.relative_to(PROJECT_ROOT).as_posix(),
        "generated_at": datetime.now(UTC).isoformat(),
        "topic_count": len(document.topics),
        "question_count": len(document.questions),
        "topics": [
            {
                "slug": t.slug,
                "order": t.order,
                "heading": t.heading,
                "display_name": t.display_name,
                "group": t.group,
                "question_count": t.question_count,
            }
            for t in sorted(document.topics, key=lambda t: t.order)
        ],
        "questions": [
            {
                "number": q.number,
                "topic_slug": q.topic_slug,
                "topic_name": q.topic_name,
                "question": q.question,
                "answer": q.answer,
                "explanation": q.explanation,
            }
            for q in sorted(document.questions, key=lambda q: q.number)
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Chỉ chạy validation và in báo cáo, không viết file generated JSON",
    )
    args = parser.parse_args()

    print(f"Đang đọc: {DOCX_PATH}")
    try:
        document = parse_docx(DOCX_PATH)
    except DocxStructureError as exc:
        print(f"LỖI cấu trúc DOCX: {exc}")
        return 1

    for line in build_report(document):
        print(line)

    if args.check_only:
        print("\n(--check-only: không viết file generated)")
        return 0

    GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    payload = to_generated_payload(document)
    GENERATED_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"\nĐã viết: {GENERATED_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
