---
name: audit-project
description: Reproduce the project baseline, compare it with PROJECT-AUDIT.md, and produce an updated prioritized plan without editing product code.
argument-hint: "[optional area: auth|catalog|cart|orders|devops|all]"
disable-model-invocation: true
---
Read `PROJECT-AUDIT.md`, `docs/completion-roadmap.md`, manifests, routes, models, and the area named in `$ARGUMENTS` (default `all`). Run only non-destructive baseline checks. Update the audit only when evidence changed. Return: current architecture, reproduced failures, security blockers, API gaps, a P0/P1/P2 backlog, and the smallest next vertical slice. Do not modify application code.
