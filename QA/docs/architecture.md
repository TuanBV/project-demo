# Architecture — Interview Review System

## Layers

```
API routes (app/api/routes/*)      -- HTTP only: parse request, call service, map to schema
Services (app/services/*)          -- business logic, orchestrates repositories + evaluation/importers
Repositories (app/repositories/*)  -- SQLAlchemy queries, no business rules
Evaluation (app/evaluation/*)      -- pure Python, no FastAPI/SQLAlchemy imports
Importers (app/importers/*)        -- pure Python DTOs + parsers, no DB access
Scheduling (app/scheduling/*)      -- review priority/next-review math, pure functions
DB models (app/db/models/*)        -- SQLAlchemy ORM, never returned directly from API
Schemas (app/schemas/*)            -- Pydantic request/response contracts
```

Dependency direction: routes -> services -> repositories/evaluation/importers/scheduling -> db.
Evaluation and importers never import SQLAlchemy or FastAPI; they operate on plain dataclasses,
which keeps them reusable from CLI scripts and unit-testable without a database.

## Import pipeline

```
DOCX file --DocxTextExtractor--> raw text
Pasted text --PlainTextExtractor--> raw text
                                        |
                                        v
                          QuestionDocumentParser (auto-picks
                          StructuredTextParser or InterviewDocumentParser
                          based on content shape)
                                        |
                                        v
                          ParsedImportDocument (DTO, no DB)
                                        |
                                        v
                          ImportValidationService -> ValidatedImportDocument
                                        |
                                        v
                          QuestionImportService (transactional; dry_run short-circuits
                          before any write; duplicate_strategy resolves content_hash clashes)
```

CLI scripts (`scripts/import_docx.py`, `scripts/import_text.py`) call the exact same
`QuestionImportService` used by the API — no duplicated business logic.

## Evaluation pipeline

```
submitted_answer
   -> TextNormalizer (unicode NFC, lowercase, whitespace, alias canonicalization,
                       diacritic-stripped variant, protects tokens like ==, *args, O(n))
   -> KeywordMatcher (EXACT / CONTAINS with word boundaries / FUZZY via RapidFuzz / ALIAS)
   -> KeywordAnswerEvaluator
        - per concept: best matching keyword wins (no double counting)
        - concept_score = earned_weight / total_weight * 100 (weights re-normalized if != 100)
        - answer_quality_factor caps score at KEYWORD_ONLY_MAXIMUM_SCORE when the answer looks
          like a bare keyword dump (short, no verbs/connectors, below minimum_token_count)
   -> ContradictionDetector (applies penalty / maximum_score cap AFTER concept scoring)
   -> classification via configurable thresholds
   -> FeedbackBuilder (template strings from matched/missing/partial/contradictions)
```

`AnswerEvaluator` is a `Protocol`; `KeywordAnswerEvaluator` is the only MVP implementation.
`SemanticAnswerEvaluator`/`HybridAnswerEvaluator`/`LlmAnswerEvaluator` are documented extension
points gated by `EVALUATOR_MODE`; selecting them today raises `EvaluatorNotConfiguredError`.

## Review scheduling

`ReviewScheduler` Protocol has two methods: `calculate_priority` (weighted formula from spec
section 15) and `calculate_next_review` (MVP: fixed-interval ladder keyed off score bucket,
documented as the seam where SM-2/FSRS would plug in later).

## Data model notes

- `content_hash` = sha256(normalized_category + normalized_question + question_type), computed by
  the importer DTO layer (not the DB) so CLI/dry-run paths can compute it without a session.
- JSON columns (`evaluation_json`, `summary_json`, `warnings_json`, `errors_json`,
  `parsed_data_json`) are used only for point-in-time snapshots/reports, never for fields that
  need indexed querying (those are normalized columns per section 8).
- All timestamps are stored UTC (`DateTime(timezone=True)`, default `func.now()`).

## Security boundaries

- Study API schemas (`StudyQuestionResponse`) never include reference_answer/concepts/keywords/
  contradictions/code answers. Admin schemas (`AdminQuestionResponse`) do.
- Uploaded DOCX is validated by extension + MIME sniff, size-capped, parsed from an in-memory
  buffer via `python-docx`, and any temp file is removed in a `finally` block.
- No user-submitted code or SQL is ever executed by the API process (`DisabledCodeRunner`,
  `DisabledSqlEvaluator` both return `NOT_CONFIGURED`).
- Global exception handler maps internal exceptions to generic error responses (no stack traces)
  and stamps a request/correlation id (`app/core/logging.py`, `app/core/exceptions.py`).

## Known MVP limitations (see README "Giới hạn hiện tại")

- Single implicit user, no auth/session.
- No real code/SQL execution/grading.
- Semantic/hybrid/LLM evaluators not implemented, only stubbed behind the Protocol.
- Review scheduler next-review formula is a simple heuristic, not SM-2/FSRS.
