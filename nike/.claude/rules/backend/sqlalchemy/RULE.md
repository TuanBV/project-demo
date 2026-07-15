---
paths:
  - "api/models/**/*.py"
  - "api/*/repository.py"
  - "api/db/**/*.py"
---
# SQLAlchemy Rules
- Model and migration column types, nullability, indexes, and foreign keys must match.
- Use transaction boundaries for multi-table writes; rollback on failure.
- Prevent N+1 queries deliberately and verify join keys against relationships.
- Money uses `DECIMAL`, not `DOUBLE`/float.
- Enforce uniqueness and ownership in the database as well as application logic.
