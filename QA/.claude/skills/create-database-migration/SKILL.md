---
name: create-database-migration
description: Create and verify an Alembic migration after changing a SQLAlchemy model in app/db/models/. Use whenever a model gains/loses a column, constraint, index, or foreign key.
allowed-tools: Bash(alembic *), Read, Edit, Grep
---

This project's SQLite target needs `render_as_batch=True` (already set in `alembic/env.py`)
and has caused real bugs when migrations were hand-written carelessly — follow every step.

1. Make the model change in `app/db/models/*.py` first.
2. Generate a draft migration: `alembic revision --autogenerate -m "<description>"`.
3. Open the generated file under `alembic/versions/` and fix it up:
   - Every `batch_op.create_foreign_key(...)` / `batch_op.drop_constraint(...)` needs an
     explicit name — never leave the first argument as `None` (SQLite batch mode raises
     `ValueError: Constraint must have a name`).
   - Any `sqlite_where=` / `postgresql_where=` argument on a partial index must be wrapped in
     `sa.text(...)`, not a raw string (`AttributeError: 'str' object has no attribute
     '_compiler_dispatch'` otherwise).
   - New non-nullable columns on a table that already has rows need a `server_default` so
     the backfill doesn't fail.
4. Round-trip the migration: `alembic upgrade head`, then `alembic downgrade -1`, then
   `alembic upgrade head` again. All three must succeed cleanly.
5. If the dev SQLite file (`data/app.db`) gets into a broken partial-migration state after a
   crash mid-migration, it's safe to delete it and re-run `alembic upgrade head` from clean —
   this is disposable dev/demo data, not anything to preserve. Re-seed afterward with the
   scripts documented in `CLAUDE.md`.
6. Run `pytest tests/unit/services` (or the full `verify-change` gate) to confirm nothing
   that depends on the changed schema broke.
