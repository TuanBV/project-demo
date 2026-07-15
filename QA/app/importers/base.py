"""Protocols for the import pipeline (spec section 9). Implementations must stay DB-free."""

from __future__ import annotations

from typing import Protocol

from app.importers.dto import ParsedImportDocument, ValidatedImportDocument


class SourceTextExtractor(Protocol):
    def extract(self, source: object) -> str: ...


class QuestionDocumentParser(Protocol):
    def parse(self, content: str) -> ParsedImportDocument: ...

    def can_parse(self, content: str) -> bool: ...


class ImportValidator(Protocol):
    def validate(self, document: ParsedImportDocument) -> ValidatedImportDocument: ...
