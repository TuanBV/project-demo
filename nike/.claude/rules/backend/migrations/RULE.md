---
paths:
  - "api/models/**/*.py"
  - "migrations/**/*"
  - "alembic/**/*"
  - "init.sql"
---
# Migration Rules
- Introduce Alembic before evolving the schema further.
- Every model change includes a reversible migration and data/backfill considerations.
- Never edit production data manually as the migration strategy.
- Keep seed/demo data separate from schema creation and never seed active tokens.
