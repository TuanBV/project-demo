# Implementation Plan — Interview Review System

Status legend: [x] done, [~] partial, [ ] not started

## Assumptions (since some requirements were ambiguous)

- Single-user MVP: `user_id` columns exist but are nullable and unused (no auth yet). All
  "current user" scoped queries operate on `user_id IS NULL` rows.
- `EVALUATOR_MODE` config selects the evaluator strategy; only `keyword` is implemented in MVP,
  others (`semantic`, `hybrid`, `llm`) raise `NotConfiguredError` if selected.
- DOCX/text import share one parsing pipeline (`StructuredTextParser` for `CATEGORY:`/`QUESTION:`
  block format, `InterviewDocumentParser` for `PHẦN`/`Câu`/`Trả lời` narrative format). The
  extractor auto-detects which parser applies per document/paste.
- CodeRunner/SqlEvaluator are stub abstractions (`DisabledCodeRunner`, `DisabledSqlEvaluator`)
  that persist attempts but never execute untrusted code/SQL, per security requirements.
- SQLite is the default dev database; `DATABASE_URL` env var swaps to Postgres without code
  changes (SQLAlchemy handles dialect differences; Alembic migrations are written to be
  dialect-agnostic where practical).
- Frontend is server-rendered Jinja2 + vanilla JS/CSS (no SPA framework), per the "no React
  unless already used" instruction — the existing `nike` project (Vue) is a sibling, unrelated
  repo and is not touched.
- Weighted review scheduler (Section 15) is implemented with the exact formula given; SM-2/FSRS
  are left as documented extension points (`ReviewScheduler` Protocol).

## Phase 1 — Foundation
- [x] Project scaffold, `pyproject.toml`, directory layout
- [x] `app/core/config.py` (Pydantic Settings, reads `.env`)
- [x] `app/core/logging.py` (structured logging + request id)
- [x] `app/core/exceptions.py` (business exceptions + global handlers)
- [x] `app/db/base.py`, `app/db/session.py`
- [x] SQLAlchemy models (category, question, evaluation, import_job, study)
- [x] Alembic setup + initial migration
- [x] Repository base
- [x] Health API (`/api/health`)
- Gate: `ruff check .`, `mypy app`, `pytest`

## Phase 2 — Question management
- [x] Category CRUD (service + repository + API)
- [x] Question CRUD incl. concepts/keywords/contradiction rules
- [x] Admin DTOs vs Study DTOs (answer never leaks pre-submit)
- [x] Seed script with 15+ questions across required topics

## Phase 3 — Evaluation engine
- [x] `TextNormalizer` (unicode, case, Vietnamese diacritics, technical token guards, aliases)
- [x] `technical_aliases.yml`
- [x] `KeywordMatcher` (EXACT/CONTAINS/FUZZY/ALIAS, word-boundary safe)
- [x] `KeywordAnswerEvaluator` (concept coverage, weighting, answer-quality factor)
- [x] `ContradictionDetector`
- [x] `FeedbackBuilder` (template-based)
- [x] Evaluation API + test-evaluation admin endpoint
- [x] Unit tests

## Phase 4 — Import pipeline
- [x] Shared DTOs (`ParsedImportDocument`, `ParsedQuestion`, etc.)
- [x] `DocxTextExtractor`, `PlainTextExtractor`
- [x] `InterviewDocumentParser` (PHẦN/Câu/Trả lời/Đáp án Java/Đáp án Python/Điểm cần đánh giá)
- [x] `StructuredTextParser` (CATEGORY/QUESTION/ANSWER/--- blocks)
- [x] `ImportValidationService`
- [x] `ConceptSuggestionService` (heuristic, non-LLM)
- [x] `QuestionImportService` (dry-run, duplicate strategy, transactional import, ImportJob/Item)
- [x] DOCX + text import APIs, CLI scripts
- [x] Tests

## Phase 5 — Study workflow
- [x] StudySession/Attempt/QuestionProgress models & services
- [x] Random selection with filters, weighted review scheduler
- [x] History & progress endpoints

## Phase 6 — Web UI
- [x] Base layout, home dashboard
- [x] Study screen + result panel
- [x] Import tabs (DOCX/paste/manual) + preview table
- [x] Question management list/edit
- [x] History view

## Phase 7 — Packaging
- [x] Dockerfile, docker-compose.yml, `.env.example`, Makefile
- [x] README.md, CLAUDE.md, docs/architecture.md

## Final quality gate
- [x] `ruff format .`
- [x] `ruff check .`
- [x] `mypy app`
- [x] `pytest`
- [x] `alembic upgrade head`
- [x] Manual smoke test via running server

See final report at the end of the session for concrete results (pass/fail counts).
