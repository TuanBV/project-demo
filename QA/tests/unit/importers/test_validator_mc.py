"""ImportValidationService structural checks for the explicit 4-option MC formats
(spec section 10.2 / 21 'Import text')."""

from __future__ import annotations

from app.importers.dto import ParsedImportDocument, ParsedQuestion
from app.importers.validator import ImportValidationService

validator = ImportValidationService()


def _mc_question(**overrides: object) -> ParsedQuestion:
    defaults = dict(
        source_order=1,
        category_name="Cat",
        question_type="TEXT",
        language_scope="GENERAL",
        difficulty="MEDIUM",
        content="Q?",
        options=["A", "B", "C", "D"],
        correct_option_index=1,
    )
    defaults.update(overrides)
    return ParsedQuestion(**defaults)  # type: ignore[arg-type]


def test_valid_four_options_pass() -> None:
    doc = ParsedImportDocument(questions=[_mc_question()])
    validated = validator.validate(doc)
    assert validated.items[0].status == "VALID"


def test_three_options_is_error() -> None:
    doc = ParsedImportDocument(questions=[_mc_question(options=["A", "B", "C"])])
    validated = validator.validate(doc)
    assert validated.items[0].status == "ERROR"
    assert any("4" in e for e in validated.items[0].errors)


def test_five_options_is_error() -> None:
    doc = ParsedImportDocument(questions=[_mc_question(options=["A", "B", "C", "D", "E"])])
    validated = validator.validate(doc)
    assert validated.items[0].status == "ERROR"


def test_missing_correct_index_is_error() -> None:
    doc = ParsedImportDocument(questions=[_mc_question(correct_option_index=None)])
    validated = validator.validate(doc)
    assert validated.items[0].status == "ERROR"
    assert any("đúng" in e for e in validated.items[0].errors)


def test_duplicate_options_is_error() -> None:
    doc = ParsedImportDocument(questions=[_mc_question(options=["A", "B", "A", "D"])])
    validated = validator.validate(doc)
    assert validated.items[0].status == "ERROR"
    assert any("trùng" in e for e in validated.items[0].errors)


def test_empty_option_is_error() -> None:
    doc = ParsedImportDocument(questions=[_mc_question(options=["A", "B", "", "D"])])
    validated = validator.validate(doc)
    assert validated.items[0].status == "ERROR"


def test_narrative_format_without_options_is_unaffected() -> None:
    doc = ParsedImportDocument(
        questions=[_mc_question(options=[], correct_option_index=None, reference_answer="A.")]
    )
    validated = validator.validate(doc)
    assert validated.items[0].status == "VALID"
