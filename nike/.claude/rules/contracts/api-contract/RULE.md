---
paths:
  - "api/router/**/*.py"
  - "api/schema/**/*.py"
  - "frontend/src/shared/service/**/*.js"
---
# API Contract Rules
- Reconcile backend routes with frontend repository calls before implementation.
- Use explicit request/response schemas and one shared error/pagination shape.
- Use appropriate HTTP status codes; do not turn every domain failure into HTTP 200.
- Keep URLs and versioning in configuration, not components.
- Add contract or integration tests whenever a route shape changes.
