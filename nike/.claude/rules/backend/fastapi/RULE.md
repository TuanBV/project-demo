---
paths:
  - "api/router/**/*.py"
  - "api/dependencies.py"
  - "api/decorators.py"
  - "api/main.py"
---
# FastAPI Rules
- Declare authentication and authorization visibly on each protected router/operation.
- Dependency failures must produce correct 401/403 status codes.
- Do not mutate request models via `.__dict__`; use supported Pydantic serialization.
- Add liveness/readiness endpoints without exposing configuration or credentials.
- Ensure middleware initializes variables before `try/finally` usage and preserves exceptions safely.
