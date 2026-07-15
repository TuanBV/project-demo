---
name: implement-feature
description: Implement one complete vertical feature slice across schema, backend, frontend, tests, migration, and documentation.
argument-hint: "<feature and acceptance criteria>"
disable-model-invocation: true
---
Implement `$ARGUMENTS` as a vertical slice. First map existing contracts and obtain a plan from the project architect when cross-cutting. Define acceptance tests, then implement the smallest coherent changes. Include authorization, validation, persistence, error states, frontend state, tests, migration, and docs. Run targeted checks and the full quality gate. Do not leave placeholders or unrelated refactors.
