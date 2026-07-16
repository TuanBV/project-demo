---
name: create-api-endpoint
description: Add a new FastAPI route following this project's layering and response-schema conventions. Use when asked to add or change an API endpoint.
allowed-tools: Read, Edit, Write, Grep, Glob
---

1. Put the route in the matching file under `app/api/routes/` (or create a new one for a new
   resource) — the route body only parses the request, calls a service method, and maps the
   result to a response schema. No business logic in the route (see `architecture.md`).
2. Add/extend the service method in `app/services/*` that actually implements the behavior,
   using a repository from `app/repositories/*` for persistence.
3. Define request/response shapes in `app/schemas/*` as Pydantic models. Never return a
   SQLAlchemy model instance directly from a route.
4. If the endpoint is study-facing (anything under `/api/questions`, `/api/study-sessions`),
   double-check against `mc-integrity.md` — it must not leak `is_correct` or any other
   answer-revealing field.
5. If the endpoint deprecates or replaces an older one, mark the old one
   `deprecated=True` in its route decorator rather than deleting it outright, matching how
   `/evaluate` and the old `/attempts` endpoint were handled during the MC migration.
6. Add integration tests under `tests/integration/` using the `client` fixture from
   `tests/conftest.py`.
7. Run the full `verify-change` gate before calling it done.
