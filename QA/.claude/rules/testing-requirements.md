---
paths:
  - "app/evaluation/**/*.py"
  - "app/importers/**/*.py"
  - "app/services/study_service.py"
  - "app/services/question_option_service.py"
  - "app/services/option_order_service.py"
  - "app/scheduling/**/*.py"
---

# Mandatory test runs for this area

Changes to evaluator, importer, submit (grading), or shuffle logic have caused regressions
before in this project (see the multiple-choice migration history) — always re-run the
relevant tests, don't rely on reading the diff alone.

- After touching `app/evaluation/*`: `pytest tests/unit/evaluation`.
- After touching `app/importers/*`: `pytest tests/unit/importers`.
- After touching `app/services/study_service.py`, `question_option_service.py`, or
  `option_order_service.py`: at minimum
  `pytest tests/unit/services/test_study_service.py tests/unit/services/test_question_option_service.py`.
- Prefer the full gate (`make check` — `ruff format`, `ruff check`, `mypy app`, `pytest
  --cov=app --cov-report=term-missing`) over the minimal subset whenever the change touches
  more than one of the areas above, or before considering a task complete. See the
  `verify-change` skill.
- Never claim a change is complete or working if `make check` hasn't actually been run and
  passed.
