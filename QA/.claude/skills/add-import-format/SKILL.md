---
name: add-import-format
description: Add support for a new question import text format (DOCX or pasted text). Use when asked to support a new structured or narrative format for bulk-importing questions.
allowed-tools: Read, Edit, Write, Grep, Glob, Bash(pytest tests/unit/importers*)
---

1. If the new format needs data the current `ParsedQuestion` DTO doesn't carry (e.g. a new
   kind of option list), add the field to `ParsedQuestion` in `app/importers/dto.py`.
2. Write the new parser as a class implementing the `QuestionDocumentParser` Protocol
   (`can_parse(text) -> bool`, `parse(text) -> ParsedImportDocument`). It must not touch the
   database — see `architecture.md`.
3. Register it in `QuestionTextParser` in priority order of `can_parse` — don't create a
   second dispatcher.
4. If the format has explicit options (not just question+answer), add count/duplicate
   validation to `ImportValidationService._validate_explicit_options` — don't write a
   separate validator for the new format.
5. Add unit tests under `tests/unit/importers/`, reusing the existing
   `QuestionImportService` rather than re-implementing import logic in the test.
6. Run `pytest tests/unit/importers` to confirm, then the full `verify-change` gate before
   calling it done.
