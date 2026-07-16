---
name: docker-verify
description: Build the Docker image and verify it boots cleanly from an empty volume (migrations run, both seed scripts run idempotently, health check passes) before trusting a Docker-related change. Use after editing the Dockerfile, docker-compose.yml, or a seed script that runs in the container CMD.
allowed-tools: Bash(docker compose build *), Bash(docker volume create *), Bash(docker run *), Bash(docker logs *), Bash(docker stop *), Bash(docker volume rm *), Bash(curl *), Bash(docker compose up *)
---

Verify a Docker-affecting change against a disposable volume before touching the real dev
container, so a broken `CMD` chain or seed script doesn't corrupt `data/app.db`.

1. Build: `docker compose build api`.
2. Create a throwaway volume and run a fresh container against it (different container/volume
   name than the real dev stack, different host port if the real one is already running):
   ```bash
   docker volume create qa_verify_tmp
   docker run --rm -d --name qa_verify_tmp -v qa_verify_tmp:/app/data -p 8009:8000 qa-api:latest
   ```
3. `docker logs qa_verify_tmp` — confirm the migration ran, both seed scripts printed a
   "created"/"already exists" summary with no traceback, and uvicorn started.
4. `curl -s http://localhost:8009/api/health` — expect `{"status":"ok"}`.
5. `docker restart qa_verify_tmp`, wait a couple seconds, check logs again — the seed scripts
   must report 0 newly created / everything already exists (idempotency check).
6. Clean up: `docker stop qa_verify_tmp && docker volume rm qa_verify_tmp`.
7. Only after this passes, recreate the real dev container if needed:
   `docker compose up -d --build`.

Never run this against the real `qa-api-1` container/volume directly — that's what step 2's
disposable volume is for.
