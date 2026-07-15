# Nike E-commerce — Claude Code Project Instructions

## Mission
Complete this repository into a secure, testable MVP e-commerce system without rewriting it from scratch. Preserve the current Vue 3 + Vite + Pinia + AJV frontend and FastAPI + SQLAlchemy + MySQL + Redis + Celery backend unless an audited defect requires a focused change.

## Start here
1. Read `PROJECT-AUDIT.md`, `docs/completion-roadmap.md`, and `docs/acceptance-criteria.md`.
2. Run `/audit-project` when starting a new completion session.
3. Work in small vertical slices. A slice includes API contract, backend, frontend, tests, and documentation.
4. Run `/quality-gate quick` at milestones and `/quality-gate full` before declaring completion.

## Current blockers
- Frontend production build fails because `PostAddView.vue` imports missing `RichTextCustom.vue`; the existing file is named `RichTextCusTom.vue`.
- The NavBar test imports a nonexistent path.
- Frontend repositories call user/password-reset/post endpoints that the backend does not expose.
- Cart, order, checkout, and slide management are not implemented end to end.
- Secrets were committed. Never print, restore, or reuse historical credentials.

## Non-negotiable workflow
- Do not ask the user to choose routine implementation details. Use the roadmap and document reasonable assumptions.
- Do not edit `.env`, secret files, `.git`, or generated dependency directories.
- Never use `git reset --hard`, `git clean -fdx`, plain `git push --force`, destructive Docker prune commands, or database drops.
- Do not hide failures with broad exception handling, disabled lint rules, skipped tests, `any`-style untyped data, or hard-coded mock responses.
- Do not mass-format unrelated files. Existing CRLF noise must be normalized in an isolated commit.
- Do not add undocumented plugins. Prefer repository-local rules, agents, skills, and scripts.
- Never claim success unless the relevant commands were run and their results are reported.

## Definition of done
A feature is done only when:
- authorization and validation are correct;
- API and frontend contracts match;
- happy path plus important failure paths are tested;
- build, lint, and tests pass for changed areas;
- migrations and documentation are updated;
- no secret, debug output, placeholder, or dead code is introduced.

## Architecture boundaries
- `frontend/src/shared/service/repository/restful/`: HTTP transport only.
- `frontend/src/shared/service/*.service.js`: response handling and domain-oriented client logic.
- `frontend/src/stores/`: application state, not direct HTTP construction.
- `api/router/`: HTTP concerns and dependency/permission declarations.
- `api/*/service.py`: business rules and transaction orchestration.
- `api/*/repository.py`: persistence queries only.
- `api/schema/`: request/response contracts.
- Database schema changes must use migrations; keep `init.sql` as bootstrap/demo data only.

## Commands
- Quick gate: `node scripts/quality-gate.mjs --quick`
- Full gate: `node scripts/quality-gate.mjs --full`
- Frontend install: `cd frontend && npm ci`
- Frontend build: `cd frontend && npm run build`
- Frontend tests: `cd frontend && npm run test:unit -- --run`
- Backend syntax: `python -m compileall -q api worker queue storage`
- Docker validation: `docker compose config`

## Reporting
At the end of each milestone report: files changed, behavior completed, migrations, tests run and exact results, remaining risks, and the next prioritized slice.
