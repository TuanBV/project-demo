"""StructuredTextParser: parses the CATEGORY:/QUESTION:/ANSWER:/--- block format
(spec section 5.3), plus the two multiple-choice variants (spec section 10.2):
  - CATEGORY/QUESTION/A/B/C/D/CORRECT (A-D letter)
  - CATEGORY/QUESTION/OPTION (repeated 4x)/CORRECT_OPTION (1-4)
Field names are case-insensitive; values may span multiple lines. Structural validation
of the option set (exactly 4, valid CORRECT reference, no duplicates) happens in
ImportValidationService, not here -- the parser only extracts what the text says.
"""

from __future__ import annotations

import re

from app.db.models.enums import Difficulty, LanguageScope, QuestionType
from app.importers.dto import ParsedImportDocument, ParsedQuestion

_SINGLE_VALUE_FIELDS = [
    "CATEGORY",
    "TYPE",
    "LANGUAGE",
    "DIFFICULTY",
    "QUESTION",
    "ANSWER",
    "EXPLANATION",
    "KEYWORDS",
    "REQUIRED_KEYWORDS",
    "OPTIONAL_KEYWORDS",
    "CONTRADICTIONS",
    "JAVA_ANSWER",
    "PYTHON_ANSWER",
    "SQL_ANSWER",
    "A",
    "B",
    "C",
    "D",
    "CORRECT",
    "CORRECT_OPTION",
]
_REPEATABLE_FIELDS = ["OPTION"]
_ALL_FIELD_NAMES = _SINGLE_VALUE_FIELDS + _REPEATABLE_FIELDS
_FIELD_RE = re.compile(
    r"^(" + "|".join(_ALL_FIELD_NAMES) + r")\s*:\s?(.*)$",
    re.IGNORECASE,
)
_SEPARATOR_RE = re.compile(r"^\s*-{3,}\s*$")

_VALID_TYPES = {t.value for t in QuestionType}
_VALID_LANGUAGES = {ls.value for ls in LanguageScope}
_VALID_DIFFICULTIES = {d.value for d in Difficulty}
_LETTER_TO_INDEX = {"A": 0, "B": 1, "C": 2, "D": 3}


def _split_csv(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def _split_contradictions(value: str | None) -> list[str]:
    if not value:
        return []
    if "|" in value:
        return [item.strip() for item in value.split("|") if item.strip()]
    return [value.strip()] if value.strip() else []


class StructuredTextParser:
    def can_parse(self, content: str) -> bool:
        return bool(re.search(r"^\s*QUESTION\s*:", content, re.IGNORECASE | re.MULTILINE))

    def parse(self, content: str) -> ParsedImportDocument:
        blocks = self._split_blocks(content)
        questions: list[ParsedQuestion] = []
        unparsed: list[str] = []

        order = 0
        for block in blocks:
            if not block.strip():
                continue
            fields, option_values = self._parse_block_fields(block)
            if "QUESTION" not in fields or not fields["QUESTION"].strip():
                if fields:
                    unparsed.append(block.strip())
                continue

            order += 1
            warnings: list[str] = []

            question_type = fields.get("TYPE", "TEXT").strip().upper()
            if question_type not in _VALID_TYPES:
                warnings.append(f"Loại câu hỏi không hợp lệ '{question_type}', dùng TEXT")
                question_type = "TEXT"

            language_scope = fields.get("LANGUAGE", "GENERAL").strip().upper()
            if language_scope not in _VALID_LANGUAGES:
                warnings.append(f"Phạm vi ngôn ngữ không hợp lệ '{language_scope}', dùng GENERAL")
                language_scope = "GENERAL"

            difficulty = fields.get("DIFFICULTY", "MEDIUM").strip().upper()
            if difficulty not in _VALID_DIFFICULTIES:
                warnings.append(f"Độ khó không hợp lệ '{difficulty}', dùng MEDIUM")
                difficulty = "MEDIUM"

            options, correct_option_index, mc_warnings = self._extract_options(
                fields, option_values
            )
            warnings.extend(mc_warnings)

            answer = fields.get("ANSWER", "").strip() or None
            if options and correct_option_index is not None:
                answer = options[correct_option_index]
            elif not answer:
                warnings.append("Thiếu đáp án tham khảo (ANSWER)")

            keywords = _split_csv(fields.get("KEYWORDS"))
            required_keywords = _split_csv(fields.get("REQUIRED_KEYWORDS"))
            optional_keywords = _split_csv(fields.get("OPTIONAL_KEYWORDS"))
            keywords_auto = (
                not keywords and not required_keywords and not optional_keywords and bool(answer)
            )

            questions.append(
                ParsedQuestion(
                    source_order=order,
                    category_name=fields.get("CATEGORY", "").strip() or None,
                    question_type=question_type,
                    language_scope=language_scope,
                    difficulty=difficulty,
                    content=fields["QUESTION"].strip(),
                    reference_answer=answer,
                    explanation=fields.get("EXPLANATION", "").strip() or None,
                    java_answer=fields.get("JAVA_ANSWER", "").strip() or None,
                    python_answer=fields.get("PYTHON_ANSWER", "").strip() or None,
                    sql_answer=fields.get("SQL_ANSWER", "").strip() or None,
                    keywords=keywords,
                    required_keywords=required_keywords,
                    optional_keywords=optional_keywords,
                    contradictions=_split_contradictions(fields.get("CONTRADICTIONS")),
                    keywords_auto_generated=keywords_auto,
                    raw_content=block.strip(),
                    warnings=warnings,
                    options=options,
                    correct_option_index=correct_option_index,
                )
            )

        return ParsedImportDocument(questions=questions, unparsed_segments=unparsed)

    @staticmethod
    def _extract_options(
        fields: dict[str, str], option_values: list[str]
    ) -> tuple[list[str], int | None, list[str]]:
        warnings: list[str] = []

        lettered = [fields.get(letter, "").strip() for letter in ("A", "B", "C", "D")]
        if any(lettered):
            options = [o for o in lettered if o]
            correct_raw = fields.get("CORRECT", "").strip().upper()
            correct_index = _LETTER_TO_INDEX.get(correct_raw)
            if correct_raw and correct_index is None:
                warnings.append(f"CORRECT không hợp lệ: '{correct_raw}' (phải là A/B/C/D)")
            return options, correct_index, warnings

        if option_values:
            correct_raw = fields.get("CORRECT_OPTION", "").strip()
            correct_position: int | None = None
            if correct_raw:
                try:
                    position = int(correct_raw)
                    correct_position = position - 1 if 1 <= position <= len(option_values) else None
                    if correct_position is None:
                        warnings.append(
                            f"CORRECT_OPTION không hợp lệ: '{correct_raw}' (phải trong 1-4)"
                        )
                except ValueError:
                    warnings.append(f"CORRECT_OPTION không hợp lệ: '{correct_raw}'")
            return option_values, correct_position, warnings

        return [], None, warnings

    @staticmethod
    def _split_blocks(content: str) -> list[str]:
        lines = content.split("\n")
        blocks: list[list[str]] = [[]]
        for line in lines:
            if _SEPARATOR_RE.match(line):
                blocks.append([])
            else:
                blocks[-1].append(line)
        return ["\n".join(block) for block in blocks]

    @staticmethod
    def _parse_block_fields(block: str) -> tuple[dict[str, str], list[str]]:
        fields: dict[str, str] = {}
        option_values: list[str] = []
        current_field: str | None = None
        buffer: list[str] = []

        def flush() -> None:
            if current_field == "OPTION":
                option_values.append("\n".join(buffer).strip())
            elif current_field is not None:
                fields[current_field] = "\n".join(buffer).strip()

        for line in block.split("\n"):
            match = _FIELD_RE.match(line)
            if match:
                flush()
                current_field = match.group(1).strip().upper()
                buffer = [match.group(2)]
            elif current_field is not None:
                buffer.append(line)
        flush()
        return fields, option_values
