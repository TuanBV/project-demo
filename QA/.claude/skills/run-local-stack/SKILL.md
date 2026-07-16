---
name: run-local-stack
description: Start the app locally for development, either via a Python virtualenv or via Docker Compose. Use when asked to run, start, or restart the app.
allowed-tools: Bash(make *), Bash(docker compose *), Bash(alembic *), Bash(python scripts/seed*.py), Bash(curl *)
---

Two supported ways to run this project — pick based on what the user asked for or what's
already running.

## Local venv (fast iteration)

```bash
python -m venv .venv && source .venv/Scripts/activate   # Windows Git Bash
pip install -e ".[dev]"
alembic upgrade head
python scripts/seed.py
python scripts/seed_java_python_mc.py
python scripts/seed_extended_topics.py
uvicorn app.main:app --reload
```

Or shorter, once the venv exists: `make install`, `make migrate`, `make seed`, `make run`.

## Docker Compose (closer to how it actually deploys)

```bash
docker compose up -d --build
```

The container's `CMD` already runs `alembic upgrade head` then both seed scripts before
starting `uvicorn`, so a fresh volume ends up fully seeded automatically — no separate seed
step needed for Docker.

## After starting, confirm it's actually up

```bash
curl -s http://localhost:8000/api/health
```

Should return `{"status":"ok"}`. If using Docker, also check `docker compose logs --tail=20`
for the seed summary lines before assuming it's ready.
