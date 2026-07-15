"""QuestionTextParser: single entry point shared by DOCX and pasted-text imports.

Auto-detects whether the content uses the structured CATEGORY/QUESTION/ANSWER block
format or the narrative PHẦN/Câu/Trả lời format and dispatches to the matching parser,
so business logic for recognizing questions lives in exactly one place per format
(spec section 5.2: "Text importer phải dùng chung parsing pipeline với DOCX importer").
"""

from __future__ import annotations

from app.importers.dto import ParsedImportDocument
from app.importers.interview_text_parser import InterviewDocumentParser
from app.importers.structured_text_parser import StructuredTextParser


class QuestionTextParser:
    def __init__(
        self,
        structured_parser: StructuredTextParser | None = None,
        interview_parser: InterviewDocumentParser | None = None,
    ) -> None:
        self._structured = structured_parser or StructuredTextParser()
        self._interview = interview_parser or InterviewDocumentParser()

    def can_parse(self, content: str) -> bool:
        return self._structured.can_parse(content) or self._interview.can_parse(content)

    def parse(self, content: str) -> ParsedImportDocument:
        if self._structured.can_parse(content):
            return self._structured.parse(content)
        return self._interview.parse(content)
