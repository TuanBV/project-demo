"""Pure DTOs shared by every stage of the import pipeline (extractor -> parser -> validator ->
importer). No SQLAlchemy/FastAPI imports allowed here (see docs/architecture.md).
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class SuggestedConcept:
    name: str
    description: str
    weight: float
    required: bool
    keywords: list[str] = field(default_factory=list)


@dataclass
class ParsedQuestion:
    source_order: int
    category_name: str | None
    question_type: str
    language_scope: str
    difficulty: str
    content: str
    reference_answer: str | None = None
    explanation: str | None = None
    java_answer: str | None = None
    python_answer: str | None = None
    sql_answer: str | None = None
    keywords: list[str] = field(default_factory=list)
    required_keywords: list[str] = field(default_factory=list)
    optional_keywords: list[str] = field(default_factory=list)
    contradictions: list[str] = field(default_factory=list)
    suggested_concepts: list[SuggestedConcept] = field(default_factory=list)
    keywords_auto_generated: bool = False
    raw_content: str = ""
    warnings: list[str] = field(default_factory=list)
    # Multiple-choice: populated when the source spells out all 4 options explicitly
    # (spec section 10.2, "CATEGORY/QUESTION/A/B/C/D/CORRECT" or "OPTION/CORRECT_OPTION").
    # Empty when the source only has a question + correct answer (spec 9/10.1) -- the
    # importer then has to generate distractors and force needs_review.
    options: list[str] = field(default_factory=list)
    correct_option_index: int | None = None


@dataclass
class ParsedImportDocument:
    questions: list[ParsedQuestion] = field(default_factory=list)
    unparsed_segments: list[str] = field(default_factory=list)


@dataclass
class ValidatedQuestionItem:
    parsed: ParsedQuestion
    status: str  # VALID | WARNING | ERROR
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


@dataclass
class ValidatedImportDocument:
    items: list[ValidatedQuestionItem] = field(default_factory=list)
    unparsed_segments: list[str] = field(default_factory=list)


@dataclass
class ImportOptions:
    dry_run: bool = False
    duplicate_strategy: str = "SKIP"
    generate_concepts: bool = False
    default_category: str | None = None
    default_question_type: str = "TEXT"
    default_language_scope: str | None = None
    source_type: str = "PASTED_TEXT"
    source_name: str | None = None
    # "MULTIPLE_CHOICE" (default) or "FREE_TEXT" -- selects which rubric the importer
    # builds (options+distractors vs. legacy concepts/keywords).
    default_question_format: str = "MULTIPLE_CHOICE"


@dataclass
class ImportResultItem:
    source_order: int
    category: str | None
    question_type: str
    question: str
    answer: str | None
    status: str
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    question_id: int | None = None


@dataclass
class ImportSummaryData:
    categories_detected: int = 0
    questions_detected: int = 0
    valid_questions: int = 0
    warning_count: int = 0
    error_count: int = 0
    categories_created: int = 0
    questions_created: int = 0
    questions_updated: int = 0
    questions_skipped: int = 0
    questions_needs_review: int = 0


@dataclass
class ImportResult:
    dry_run: bool
    job_id: int | None
    summary: ImportSummaryData
    items: list[ImportResultItem]
    unparsed_segments: list[str] = field(default_factory=list)
