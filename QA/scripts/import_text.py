#!/usr/bin/env python
"""CLI: import questions from a pasted-text file (or stdin), same service as the API.

Usage:
    python scripts/import_text.py path/to/questions.txt [--dry-run] [options]
    cat questions.txt | python scripts/import_text.py -
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.db.session import SessionLocal  # noqa: E402
from app.importers.docx_extractor import PlainTextExtractor  # noqa: E402
from app.importers.dto import ImportOptions  # noqa: E402
from app.importers.text_parser import QuestionTextParser  # noqa: E402
from app.importers.validator import ImportValidationService  # noqa: E402
from app.repositories.category_repository import CategoryRepository  # noqa: E402
from app.repositories.import_repository import ImportRepository  # noqa: E402
from app.repositories.question_repository import QuestionRepository  # noqa: E402
from app.services.import_service import QuestionImportService  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Import questions from pasted text")
    parser.add_argument("path", help="Path to a text file, or '-' to read from stdin")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--duplicate-strategy", default="skip", choices=["skip", "update", "create_copy"]
    )
    parser.add_argument("--generate-concepts", action="store_true")
    parser.add_argument("--default-category", default=None)
    args = parser.parse_args()

    if args.path == "-":
        raw_content = sys.stdin.read()
    else:
        raw_content = Path(args.path).read_text(encoding="utf-8")

    if not raw_content.strip():
        print("Lỗi: nội dung rỗng.")
        raise SystemExit(1)

    text = PlainTextExtractor().extract(raw_content)
    document = QuestionTextParser().parse(text)
    validated = ImportValidationService().validate(document)

    db = SessionLocal()
    try:
        service = QuestionImportService(
            db=db,
            question_repository=QuestionRepository(db),
            category_repository=CategoryRepository(db),
            import_repository=ImportRepository(db),
        )
        options = ImportOptions(
            dry_run=args.dry_run,
            duplicate_strategy=args.duplicate_strategy.upper(),
            generate_concepts=args.generate_concepts,
            default_category=args.default_category,
            source_type="PASTED_TEXT",
            source_name=None,
        )
        result = service.import_document(validated, options)
        print(f"dry_run={result.dry_run} job_id={result.job_id}")
        print(result.summary)
        for item in result.items:
            print(f"[{item.status}] #{item.source_order} {item.category} :: {item.question[:60]}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
