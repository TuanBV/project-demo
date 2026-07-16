---
paths:
  - "app/**/*.py"
  - ".env.example"
  - "docker-compose.yml"
---

# Security constraints

- Never execute untrusted code or SQL submitted by a learner. `DisabledCodeRunner` /
  `DisabledSqlEvaluator` (when a `CODE` or `SQL` question type needs real execution support)
  must always return `NOT_CONFIGURED` rather than actually running anything. If real
  execution is ever implemented, it must run in an isolated sandbox — not inline in the
  request-handling process.
- Never trust client-supplied grading data — see `mc-integrity.md`. This is both a data
  integrity and a security boundary: a learner-controlled `is_correct` field would let a
  client fabricate a passing score.
- Never write secrets (API keys, passwords, tokens, connection strings) into tracked files.
  `.env` is gitignored (see `.gitignore`) and only `.env.example` (placeholder values, no
  real secrets) is tracked. Keep it that way — this repository's shared git history includes
  at least one prior incident of a real credential being committed in a sibling project, so
  treat this as a real risk, not a theoretical one.
- `app/core/config.py` reads all configuration from environment variables via
  `pydantic-settings` (`Settings(BaseSettings)`). Don't hardcode a threshold, secret, or
  connection string directly in application code — add it to `Settings` and `.env.example`
  instead (see `configuration.md`).
