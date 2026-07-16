---
name: write-tests
description: Write a new unit or integration test following this project's pytest conventions. Use when adding tests for a service, repository, importer, evaluator, or API route.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash(pytest *)
---

1. Pick the right layer:
   - Pure logic (`app/evaluation/*`, `app/importers/*`, `app/scheduling/*`) →
     `tests/unit/evaluation/`, `tests/unit/importers/` — no DB, no HTTP, direct function
     calls.
   - Services/repositories → `tests/unit/services/` using the `db_session` fixture from
     `tests/conftest.py` (isolated in-memory SQLite per test, `StaticPool`).
   - Full request/response flows → `tests/integration/` using the `client` fixture
     (`TestClient` wired to the same `db_session`).
   - CLI seed/import scripts → `tests/unit/scripts/`, loading the script module via
     `importlib.util.spec_from_file_location` (scripts aren't a package) — see
     `tests/unit/scripts/test_seed_extended_topics.py` for the pattern.
2. Follow Arrange-Act-Assert. Name the test for the behavior, not the method
   (`test_submit_option_answer_correct`, not `test_submit`).
3. For MC-flow tests, build real 4-option questions via `AdminQuestionCreate(...,
   options=[...])` rather than FREE_TEXT-only fixtures, unless the test is specifically about
   legacy FREE_TEXT behavior (then pass `question_format=QuestionFormat.FREE_TEXT`
   explicitly).
4. Assert answer-leak prevention where relevant: a `StudyQuestionResponse`'s options must
   never contain `is_correct`.
5. Run the specific test file first, then the relevant subset from
   `testing-requirements.md`, then the full gate via `verify-change` if the change is broad.
