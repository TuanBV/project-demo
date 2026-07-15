---
paths:
  - "frontend/src/validations/**/*.js"
  - "frontend/src/locales/**/*.json"
  - "api/schema/**/*.py"
---
# Validation and i18n Rules
- Frontend validation improves UX; backend validation remains authoritative.
- Keep validation rules aligned across client and server with tests for edge cases.
- User-facing text belongs in locale resources; do not mix English, Vietnamese, and Japanese literals in transport/error code.
- Dates, numbers, currency, and pluralization must be locale-aware.
