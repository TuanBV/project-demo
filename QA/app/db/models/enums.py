"""Enums shared by models, schemas and services (single source of truth)."""

from __future__ import annotations

import enum


class QuestionType(enum.StrEnum):
    TEXT = "TEXT"
    CODE = "CODE"
    SQL = "SQL"
    SCENARIO = "SCENARIO"


class QuestionFormat(enum.StrEnum):
    """How a question is answered. MULTIPLE_CHOICE is the default study flow; the others
    keep the legacy free-text evaluator (app/evaluation/*) alive for those rows only.
    """

    MULTIPLE_CHOICE = "MULTIPLE_CHOICE"
    FREE_TEXT = "FREE_TEXT"
    CODE = "CODE"
    SQL = "SQL"


class LanguageScope(enum.StrEnum):
    GENERAL = "GENERAL"
    JAVA = "JAVA"
    PYTHON = "PYTHON"
    SQL = "SQL"


class Difficulty(enum.StrEnum):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"


class SourceType(enum.StrEnum):
    DOCX = "DOCX"
    PASTED_TEXT = "PASTED_TEXT"
    MANUAL = "MANUAL"
    SEED = "SEED"
    API = "API"


class MatchType(enum.StrEnum):
    EXACT = "EXACT"
    CONTAINS = "CONTAINS"
    FUZZY = "FUZZY"
    ALIAS = "ALIAS"


class ImportStatus(enum.StrEnum):
    PENDING = "PENDING"
    PARSING = "PARSING"
    VALIDATING = "VALIDATING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class DuplicateStrategy(enum.StrEnum):
    SKIP = "SKIP"
    UPDATE = "UPDATE"
    CREATE_COPY = "CREATE_COPY"


class ImportItemStatus(enum.StrEnum):
    VALID = "VALID"
    WARNING = "WARNING"
    ERROR = "ERROR"
    NEEDS_REVIEW = "NEEDS_REVIEW"
    CREATED = "CREATED"
    UPDATED = "UPDATED"
    SKIPPED = "SKIPPED"


class QuestionValidationStatus(enum.StrEnum):
    VALID = "VALID"
    NEEDS_REVIEW = "NEEDS_REVIEW"
    INVALID = "INVALID"


class MasteryLevel(enum.StrEnum):
    NEW = "NEW"
    LEARNING = "LEARNING"
    FAMILIAR = "FAMILIAR"
    MASTERED = "MASTERED"


class StudyMode(enum.StrEnum):
    RANDOM = "RANDOM"
    CATEGORY = "CATEGORY"
    REVIEW = "REVIEW"
    EXAM = "EXAM"


class Classification(enum.StrEnum):
    CORRECT = "CORRECT"
    MOSTLY_CORRECT = "MOSTLY_CORRECT"
    PARTIALLY_CORRECT = "PARTIALLY_CORRECT"
    INCORRECT = "INCORRECT"
