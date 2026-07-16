---
name: verify-change
description: Run this project's full quality gate (ruff format, ruff check, mypy, pytest with coverage) after making code changes. Use before saying a change is done, and always after touching evaluator/importer/submit/shuffle logic per testing-requirements.md.
allowed-tools: Bash(ruff format .), Bash(ruff check .), Bash(mypy app), Bash(pytest *), Bash(make check)
---

Run the project's quality gate and report the real results — never claim success without
running it.

1. Run `ruff format .` — auto-formats; note any files it changed.
2. Run `ruff check .` — must report "All checks passed!". If not, fix the reported issues
   (don't suppress with `noqa` unless the rule genuinely doesn't apply) and re-run.
3. Run `mypy app` — must report "Success: no issues found in N source files". Fix real type
   errors; don't add `# type: ignore` to hide a genuine mismatch.
4. Run `pytest --cov=app --cov-report=term-missing` — all tests must pass. If a test fails
   because of the change you just made, fix the code or the test (whichever is actually
   wrong), don't skip or delete the test to make it pass.
5. If any step required a fix, re-run the full sequence once more to confirm everything is
   green together, not just individually.

Equivalent shortcut: `make check` runs format + lint + typecheck + test in one command.

Report the actual pass/fail counts and coverage percentage — don't summarize as just "all
good" without the numbers.
