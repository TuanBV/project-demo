---
paths:
  - "app/db/models/**/*.py"
  - "alembic/versions/**/*.py"
---

# Alembic migration requirements

- Any change to a model in `app/db/models/*` (`Question`, `QuestionOption`,
  `QuestionDelivery`, `Attempt`, `QuestionProgress`, `Category`, ...) requires a new Alembic
  migration in the same change. Don't leave the model and the schema out of sync.
- `alembic/env.py` already sets `render_as_batch=True` for both offline and online contexts —
  required because SQLite doesn't support most `ALTER TABLE` forms directly.
- In batch mode, every `batch_op.create_foreign_key(...)` and `batch_op.drop_constraint(...)`
  needs an explicit name argument. Passing `None` raises
  `ValueError: Constraint must have a name` under SQLite batch mode.
- If a migration defines a partial unique index (`sqlite_where=...` /
  `postgresql_where=...`), wrap the condition in `sa.text(...)`. A raw string raises
  `AttributeError: 'str' object has no attribute '_compiler_dispatch'` at migration time.
- Verify every new migration round-trips: `alembic upgrade head`, `alembic downgrade -1`,
  `alembic upgrade head` again, before considering the migration done.
- See the `create-database-migration` skill for the full step-by-step workflow.
