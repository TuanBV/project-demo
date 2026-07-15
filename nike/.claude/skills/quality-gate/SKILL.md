---
name: quality-gate
description: Run the repository quality gate and explain failures without making unrelated fixes.
argument-hint: "[quick|full|security]"
disable-model-invocation: true
---
Run `node scripts/quality-gate.mjs --$ARGUMENTS`, defaulting to `--quick`. Summarize each check as pass/fail/skip, preserve the first actionable error for failures, and distinguish environmental setup failures from code defects. Do not claim completion on a failing full gate.
