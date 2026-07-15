---
paths:
  - "Dockerfile*"
  - "docker-compose*.yml"
  - "**/Dockerfile*"
---
# Docker Rules
- Use reproducible dependency installs and non-root runtime users where practical.
- Do not bake `.env` or credentials into images.
- Add healthchecks and dependency readiness, not only startup order.
- Separate development and production commands/profiles.
- Avoid destructive prune instructions in the primary README.
