---
name: add-evaluator
description: Add a new free-text answer evaluator (semantic, hybrid, or LLM-based) for legacy FREE_TEXT questions. Use only for FREE_TEXT scoring changes — never for the default MULTIPLE_CHOICE flow.
allowed-tools: Read, Edit, Write, Grep, Bash(pytest tests/unit/evaluation*)
---

This only applies to the legacy `FREE_TEXT` question format. The default MULTIPLE_CHOICE
flow always grades via `MultipleChoiceGrader` (ID comparison) — never route MC through an
evaluator.

1. Implement the `AnswerEvaluator` Protocol from `app/evaluation/base.py`. The implementation
   must stay pure — no FastAPI or SQLAlchemy imports (see `architecture.md`).
2. Register the new mode through `EVALUATOR_MODE` (in `Settings`) and wire it into the
   factory at `app/api/dependencies.py::evaluation_service`.
3. Still apply `ContradictionDetector` after the coverage/similarity score, in the same place
   the existing evaluators do — don't change FREE_TEXT's overall scoring behavior as a side
   effect of adding a new evaluator.
4. Add unit tests under `tests/unit/evaluation/` following the existing evaluator test
   pattern (pure function tests, no DB).
5. Run `pytest tests/unit/evaluation`, then the full `verify-change` gate.
