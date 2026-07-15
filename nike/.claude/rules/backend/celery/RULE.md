---
paths:
  - "worker/**/*.py"
  - "api/tasks.py"
  - "docker-compose*.yml"
---
# Celery Rules
- Tasks are idempotent, retry only known transient failures, and log correlation IDs.
- Do not pass secrets or large binary payloads through the broker.
- Separate worker and beat concerns and test scheduling configuration.
- Define result retention, dead-letter/error handling, and graceful shutdown behavior.
