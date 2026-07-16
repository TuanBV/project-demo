---
name: update-documentation
description: Keep CLAUDE.md, README.md, and docs/*.md in sync after a behavior or schema change. Use after implementing a feature or migration that changes setup steps, API behavior, or documented limitations.
allowed-tools: Read, Grep, Glob, Edit
---

This project treats `CLAUDE.md`, `README.md`, and `docs/*.md` as living documents that must
track real repository state, not aspirational plans.

1. Identify what actually changed: new/changed API endpoint, new env var, new migration, new
   CLI script, new limitation, or a limitation that's now resolved.
2. `CLAUDE.md` — update only if the change affects: the default study flow, the layering
   rules, a repository-wide invariant, or the "current limitations" list. Keep it short; move
   any new multi-step procedure into a skill instead of inlining it here.
3. `README.md` — update the relevant numbered section (setup, migrations, seeding, import
   formats, API groups, limitations) to match. Don't leave a documented command that no
   longer exists, and don't describe a command that hasn't actually been added.
4. `docs/architecture.md`, `docs/implementation-plan.md`,
   `docs/multiple-choice-migration-plan.md` — update only the specific section affected;
   these are historical/planning documents, not meant to be rewritten wholesale.
5. `.env.example` — if a new `Settings` field was added, add its default here too (see
   `configuration.md`).
6. Grep for the old command/behavior across `README.md`, `CLAUDE.md`, and `docs/*.md` before
   finishing, to catch stale references the first pass missed.
