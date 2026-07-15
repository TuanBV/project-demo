---
name: fix-build
description: Repair frontend/backend build, import, lint, and test-startup blockers with minimal behavioral change.
argument-hint: "[frontend|backend|docker|all]"
disable-model-invocation: true
---
Reproduce the failure first. Fix root causes, not symptoms. Do not combine mass formatting with behavioral changes. Add a regression test where relevant. Run the targeted command after each coherent fix, then `node scripts/quality-gate.mjs --quick`. Report before/after results and any remaining unrelated failures.
