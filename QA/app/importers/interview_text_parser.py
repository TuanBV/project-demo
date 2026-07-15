"""InterviewDocumentParser: parses the narrative PHẦN/Câu/Bài/Trả lời/Đáp án format
(spec section 5.1). Section headers containing "BÀI CODING"/"BÀI SQL"/"TÌNH HUỐNG" set the
question type for everything under them; numbering does not need to be contiguous.
"""

from __future__ import annotations

import re
from typing import Any

from app.evaluation.normalizer import strip_diacritics
from app.importers.dto import ParsedImportDocument, ParsedQuestion

_CATEGORY_RE = re.compile(r"^(?:PH[ẦA]N)\b\s*(.*)$", re.IGNORECASE)
_CAU_RE = re.compile(r"^(?:C[ÂA]U)\s+(\d+)\s*[\.:]?\s*(.*)$", re.IGNORECASE)
_BAI_RE = re.compile(r"^(?:B[ÀA]I)\s+(\d+)\s*[\.:]?\s*(.*)$", re.IGNORECASE)
_TRA_LOI_RE = re.compile(r"^(?:TR[ẢA]\s*L[ỜƠO]I)\s*:\s*(.*)$", re.IGNORECASE)
_DAP_AN_JAVA_RE = re.compile(r"^(?:[ĐD][ÁA]P\s*[ÁA]N\s*JAVA)\s*:\s*(.*)$", re.IGNORECASE)
_DAP_AN_PYTHON_RE = re.compile(r"^(?:[ĐD][ÁA]P\s*[ÁA]N\s*PYTHON)\s*:\s*(.*)$", re.IGNORECASE)
_DAP_AN_SQL_RE = re.compile(r"^(?:[ĐD][ÁA]P\s*[ÁA]N\s*SQL)\s*:\s*(.*)$", re.IGNORECASE)
_DIEM_RE = re.compile(r"^(?:[ĐD]I[ỂE]M\s*C[ẦA]N\s*[ĐD][ÁA]NH\s*GI[ÁA])\s*:\s*(.*)$", re.IGNORECASE)
_CATEGORY_PREFIX_RE = re.compile(r"^[IVXLCDM]+\s*[-–—.:]\s*", re.IGNORECASE)


class InterviewDocumentParser:
    def can_parse(self, content: str) -> bool:
        for line in content.split("\n"):
            stripped = line.strip()
            if not stripped:
                continue
            if _CAU_RE.match(stripped) or _BAI_RE.match(stripped) or _CATEGORY_RE.match(stripped):
                return True
        return False

    def parse(self, content: str) -> ParsedImportDocument:
        questions: list[ParsedQuestion] = []
        unparsed_segments: list[str] = []

        current_category: str | None = None
        current_type_hint = "TEXT"
        current: dict[str, Any] | None = None
        section: str | None = None
        order = 0

        def flush() -> None:
            nonlocal current
            if current is None:
                return
            content_text = "\n".join(current["content"]).strip()
            if not content_text:
                if current["raw"].strip():
                    unparsed_segments.append(current["raw"].strip())
                current = None
                return
            answer = "\n".join(current["answer"]).strip() or None
            warnings: list[str] = []
            if not answer:
                warnings.append("Thiếu đáp án tham khảo (Trả lời)")
            questions.append(
                ParsedQuestion(
                    source_order=current["order"],
                    category_name=current_category,
                    question_type=current["question_type"],
                    language_scope="GENERAL",
                    difficulty="MEDIUM",
                    content=content_text,
                    reference_answer=answer,
                    explanation="\n".join(current["explanation"]).strip() or None,
                    java_answer="\n".join(current["java"]).strip() or None,
                    python_answer="\n".join(current["python"]).strip() or None,
                    sql_answer="\n".join(current["sql"]).strip() or None,
                    keywords_auto_generated=bool(answer),
                    raw_content=current["raw"].strip(),
                    warnings=warnings,
                )
            )
            current = None

        for raw_line in content.split("\n"):
            line = raw_line.rstrip()
            stripped = line.strip()

            if not stripped:
                if current is not None and section is not None:
                    current[section].append("")
                    current["raw"] += raw_line + "\n"
                continue

            cat_match = _CATEGORY_RE.match(stripped)
            if cat_match:
                flush()
                header_rest = cat_match.group(1).strip()
                current_category = (
                    _CATEGORY_PREFIX_RE.sub("", header_rest).strip() or header_rest or stripped
                )
                ascii_header = strip_diacritics(stripped).lower()
                if "bai coding" in ascii_header:
                    current_type_hint = "CODE"
                elif "bai sql" in ascii_header:
                    current_type_hint = "SQL"
                elif "tinh huong" in ascii_header:
                    current_type_hint = "SCENARIO"
                else:
                    current_type_hint = "TEXT"
                section = None
                continue

            cau_match = _CAU_RE.match(stripped)
            bai_match = _BAI_RE.match(stripped)
            if cau_match or bai_match:
                flush()
                order += 1
                m = cau_match or bai_match
                assert m is not None
                rest = m.group(2).strip()
                current = {
                    "order": order,
                    "question_type": current_type_hint,
                    "content": [rest] if rest else [],
                    "answer": [],
                    "java": [],
                    "python": [],
                    "sql": [],
                    "explanation": [],
                    "raw": raw_line + "\n",
                }
                section = "content"
                continue

            if current is None:
                unparsed_segments.append(stripped)
                continue

            current["raw"] += raw_line + "\n"

            tl_match = _TRA_LOI_RE.match(stripped)
            if tl_match:
                section = "answer"
                if tl_match.group(1).strip():
                    current["answer"].append(tl_match.group(1).strip())
                continue

            java_match = _DAP_AN_JAVA_RE.match(stripped)
            if java_match:
                section = "java"
                if java_match.group(1).strip():
                    current["java"].append(java_match.group(1).strip())
                continue

            python_match = _DAP_AN_PYTHON_RE.match(stripped)
            if python_match:
                section = "python"
                if python_match.group(1).strip():
                    current["python"].append(python_match.group(1).strip())
                continue

            sql_match = _DAP_AN_SQL_RE.match(stripped)
            if sql_match:
                section = "sql"
                if sql_match.group(1).strip():
                    current["sql"].append(sql_match.group(1).strip())
                continue

            diem_match = _DIEM_RE.match(stripped)
            if diem_match:
                section = "explanation"
                if diem_match.group(1).strip():
                    current["explanation"].append(diem_match.group(1).strip())
                continue

            target = section or "content"
            current[target].append(stripped)

        flush()

        return ParsedImportDocument(questions=questions, unparsed_segments=unparsed_segments)
