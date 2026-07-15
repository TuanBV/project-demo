---
paths:
  - "frontend/src/tests/**/*"
  - "api/tests/**/*"
  - "tests/**/*"
---
# Testing Rules
- Replace playground tests with tests for real domain behavior.
- Test permissions, validation, not-found, conflict, and rollback paths—not only happy paths.
- Do not mock the unit under test; mock external boundaries.
- Every fixed bug gets a regression test that fails before the fix.
- Keep tests deterministic and independent of real email, social APIs, or external network.
