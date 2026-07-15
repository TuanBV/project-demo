"""ImportValidationService: structural validation + in-batch duplicate detection
(spec section 20 "Text import" rules, section 10.2 for explicit 4-option MC blocks).
Runs entirely on DTOs, no DB access.
"""

from __future__ import annotations

from app.core.hashing import compute_content_hash
from app.evaluation.normalizer import strip_diacritics
from app.importers.dto import (
    ParsedImportDocument,
    ParsedQuestion,
    ValidatedImportDocument,
    ValidatedQuestionItem,
)

_REQUIRED_OPTION_COUNT = 4


class ImportValidationService:
    def validate(self, document: ParsedImportDocument) -> ValidatedImportDocument:
        items: list[ValidatedQuestionItem] = []
        seen_hashes: set[str] = set()

        for parsed in document.questions:
            warnings = list(parsed.warnings)
            errors: list[str] = []

            if not parsed.content.strip():
                errors.append("Câu hỏi không được để trống")

            if parsed.options:
                errors.extend(self._validate_explicit_options(parsed))

            content_hash = compute_content_hash(
                parsed.category_name or "", parsed.content, parsed.question_type
            )
            if content_hash in seen_hashes:
                warnings.append("Trùng lặp với một câu hỏi khác trong cùng lần import")
            else:
                seen_hashes.add(content_hash)

            status = "ERROR" if errors else ("WARNING" if warnings else "VALID")
            items.append(
                ValidatedQuestionItem(
                    parsed=parsed, status=status, warnings=warnings, errors=errors
                )
            )

        return ValidatedImportDocument(items=items, unparsed_segments=document.unparsed_segments)

    @staticmethod
    def _validate_explicit_options(parsed: ParsedQuestion) -> list[str]:
        errors: list[str] = []
        options = parsed.options

        if len(options) != _REQUIRED_OPTION_COUNT:
            errors.append(f"Phải có đúng {_REQUIRED_OPTION_COUNT} đáp án, hiện có {len(options)}")

        if any(not o.strip() for o in options):
            errors.append("Đáp án không được để trống")

        normalized = [" ".join(strip_diacritics(o).lower().split()) for o in options]
        if len(set(normalized)) != len(normalized):
            errors.append("Các đáp án bị trùng nhau")

        if parsed.correct_option_index is None:
            errors.append("Không xác định được đáp án đúng (CORRECT/CORRECT_OPTION không hợp lệ)")
        elif not (0 <= parsed.correct_option_index < len(options)):
            errors.append("Đáp án đúng không nằm trong danh sách đáp án")

        return errors
