---
name: add-question-type
description: Add a new value to QuestionType or QuestionFormat. Use when the project needs to represent a new kind of question (e.g. a new CODE/SQL variant) beyond the existing enum values.
allowed-tools: Read, Edit, Grep, Bash(alembic *)
---

1. Add the new value to `QuestionType` or `QuestionFormat` in `app/db/models/enums.py`.
2. Create the matching Alembic migration — see the `create-database-migration` skill for the
   batch-mode gotchas (SQLite enum-backed columns, constraint naming).
3. If the new type needs real code or SQL execution, use the `CodeRunner` / `SqlEvaluator`
   Protocol abstraction rather than executing anything inline — see `security.md` (must
   return `NOT_CONFIGURED` until a real sandboxed implementation exists).
4. If the new type needs to be recognized from a special import header, update the relevant
   parser — see the `add-import-format` skill.
5. Run the full `verify-change` gate before calling it done.
