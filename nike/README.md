# Nike E-commerce (MVP in progress)

A partially implemented e-commerce demo:
- **Frontend**: Vue 3, Vite, Pinia, Vue Router, AJV validation, Tailwind (`frontend/`)
- **Backend**: FastAPI, Pydantic, SQLAlchemy, MySQL (`api/`)
- **Async**: Redis + Celery worker/beat (`worker/`)
- **Infra**: Docker Compose

See [`PROJECT-AUDIT.md`](PROJECT-AUDIT.md) for the current defect/risk list and [`docs/completion-roadmap.md`](docs/completion-roadmap.md) for what's left before this is a real MVP. This README only covers **how to run and test what exists today**.

## Prerequisites

- Docker + Docker Compose (recommended path), or:
  - Python 3.11, Node.js 18+, MySQL 8, Redis, for running services natively.

## 1. Configure environment

Nothing will start correctly with default/missing environment variables — copy the templates and fill them in:

```bash
cp .env.example .env                 # values consumed by docker-compose.yml (MYSQL_PASSWORD, MYSQL_DB)
cp api/env.example api/.env          # backend runtime config (JWT_SECRET, MAIL_*, DB creds, ...)
cp frontend/.env.example frontend/.env   # VITE_API_BASE_URL
```

Set real values for every `CHANGE_ME` in `api/.env`. **Never reuse any credential that ever appeared in this repository's history** — see [`SECURITY-NOTICE.md`](SECURITY-NOTICE.md); rotate the Gmail app password, JWT secret, and DB password before using this project beyond a local sandbox.

`MYSQL_PASSWORD` and `MYSQL_DB` in the root `.env` must match the values you put in `api/.env` — Compose uses the root `.env` to initialize the MySQL container, while the API reads `api/.env` directly.

## 2. Run with Docker Compose

```bash
docker compose up --build
```

This starts `mysql`, `redis`, `fastapi` (port `8000`), `worker`, `celery_beat`, and `frontend` (Vite dev server, port `5000`). MySQL is seeded from [`init.sql`](init.sql) on first boot (demo categories/products/users — inspect the file for exact rows).

- Frontend: http://localhost:5000
- API: http://localhost:8000 (interactive docs at `/docs`)
- Health checks: `GET /health/live`, `GET /health/ready`

The `storage`/`queue` services stay commented out in `docker-compose.yml` (unfinished, not part of the current MVP slice).

To stop:

```bash
docker compose down
```

Avoid `docker compose down --volumes`, `docker system prune`, or other destructive cleanup unless you intend to discard the database volume. If you ever need to reset the database, re-seed from `init.sql` — never copy credential values back from git history or old notes (see [`SECURITY-NOTICE.md`](SECURITY-NOTICE.md)).

## 3. Run the backend natively (alternative to Docker)

```bash
cd api
python -m venv .venv
.venv\Scripts\activate        # Windows; use `source .venv/bin/activate` on macOS/Linux
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Requires a reachable MySQL (`MYSQL_HOST_WRITE`/`MYSQL_HOST_READ`, default `localhost`) and Redis matching `api/.env`. There are no Alembic migrations yet ([`docs/completion-roadmap.md`](docs/completion-roadmap.md), Milestone 5) — schema comes solely from `init.sql`, run manually against your MySQL instance if not using Compose:

```bash
mysql -u <user> -p < init.sql
```

## 4. Run the frontend natively (alternative to Docker)

```bash
cd frontend
npm ci
npm run dev       # http://localhost:5000, calls VITE_API_BASE_URL directly from the browser
```

Production build:

```bash
npm run build      # outputs frontend/dist (gitignored, regenerate as needed)
npm run preview
```

## 5. Run the worker (Celery)

```bash
cd worker
pip install -r requirements.txt
celery -A worker worker --loglevel=info
celery -A worker beat --loglevel=info   # scheduled tasks, separate process
```

Needs `CELERY_BROKER_URL` / `CELERY_RESULT_BACKEND` pointing at Redis (see `docker-compose.yml` for the values used in-container).

## Tests

Frontend:

```bash
cd frontend
npm run test:unit -- --run
```

Currently one real suite: `src/tests/unit/NavBar.test.js` (3 tests, passing). There is no backend test suite yet (`pytest` is a declared dependency but no test files exist) — this is a tracked gap, not something hidden or worked around.

Backend syntax/import check (not a test suite, just a compile pass):

```bash
python -m compileall -q api worker queue storage
```

## Quality gates

```bash
node scripts/quality-gate.mjs --quick   # secret scan, merge-marker scan, Python compile
node scripts/quality-gate.mjs --full    # + frontend lint/test/build, dependency audit, docker compose config
```

Run `--quick` at milestones and `--full` before calling any slice done, per [`CLAUDE.md`](CLAUDE.md).

## Known gaps / troubleshooting

- **`api/.env` is currently tracked in git** with placeholder-only values after a prior secret-purge pass; it should not be a tracked file going forward (added to `.gitignore` in this pass) but removing it from the git index requires a deliberate, reviewed step — see [`PROJECT-AUDIT.md`](PROJECT-AUDIT.md) P0 #1 and [`SECURITY-NOTICE.md`](SECURITY-NOTICE.md). Do not commit real secrets into it.
- **Cart, checkout, orders, and slide management are not implemented end-to-end** — see [`PROJECT-AUDIT.md`](PROJECT-AUDIT.md) and [`docs/completion-roadmap.md`](docs/completion-roadmap.md) Milestones 3–4.
- **No database migrations** — schema changes must currently go through `init.sql`; this is a documented gap, not the intended long-term approach.
- If login/session doesn't persist on plain HTTP localhost, check the cookie `secure`/`samesite` settings against your `ENVIRONMENT` value in `api/.env`.
- If the API can't reach MySQL, confirm `MYSQL_HOST_WRITE`/`MYSQL_HOST_READ` match the actual host (`mysql` inside Compose's network, `localhost` when running natively).

## Security

Read [`SECURITY-NOTICE.md`](SECURITY-NOTICE.md) before doing anything with this repository beyond local experimentation. Never print, restore, or reuse any credential that appears in git history.
