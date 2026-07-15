---
name: database-migration
description: Design and implement a reversible Alembic migration aligned with SQLAlchemy models and bootstrap data.
argument-hint: "<schema change>"
disable-model-invocation: true
---
For `$ARGUMENTS`, inspect model and SQL history, define invariants, create a reversible migration, update models and seed/bootstrap documentation, and provide upgrade/downgrade verification. Consider existing data, lock duration, indexes, foreign keys, precision, uniqueness, and rollback. Never drop data casually.
