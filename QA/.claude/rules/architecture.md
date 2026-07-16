---
paths:
  - "app/**/*.py"
---

# Layering and purity constraints

- Layering is `API routes -> Services -> Repositories -> DB models`. Routes only parse the
  request, call a service, and map the result to a Pydantic schema. Business logic belongs
  in `app/services/*`, never in `app/api/routes/*`.
- `app/evaluation/*` and `app/importers/*` must **never** import FastAPI or SQLAlchemy. They
  are pure Python modules, testable without a DB or HTTP context. If a change requires either
  import inside these packages, the logic belongs in a service instead.
- SQLAlchemy ORM models are never returned directly from an API route. Always map through a
  Pydantic response schema (`app/schemas/*`), even when the shape looks identical to the ORM
  model.
- `app/importers/*` parsers must not access the database. A parser implements the
  `QuestionDocumentParser` Protocol (`can_parse` + `parse`) and returns a
  `ParsedImportDocument`; DB writes happen later in `QuestionImportService`.
- Don't create a second parser with its own duplicate-question-detection logic — reuse
  `QuestionTextParser`'s dispatch and `QuestionImportService`'s hashing.
- CLI scripts under `scripts/` call services directly (e.g. `QuestionService`,
  `CategoryService`) — never duplicate business logic inside a script.
