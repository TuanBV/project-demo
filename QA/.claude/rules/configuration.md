---
paths:
  - "app/core/config.py"
  - ".env.example"
---

# Configuration conventions

- All thresholds and scoring weights live in `Settings` (`app/core/config.py`,
  `pydantic-settings`, read from `.env`) — never hardcode a number like a score threshold, a
  fuzzy-match cutoff, or `multiple_choice_option_count` / `multiple_choice_correct_option_count`
  directly in service/evaluation code.
- Every new setting added to `Settings` must also get a documented default in `.env.example`
  with the other keys in the same thematic group (MC study flow, FREE_TEXT thresholds,
  import limits, ...). Don't add a setting that silently relies on a Pydantic default with no
  corresponding `.env.example` entry — the file is the operator-facing source of truth for
  what's configurable.
- Don't put a real secret value in `.env.example` — see `security.md`.
