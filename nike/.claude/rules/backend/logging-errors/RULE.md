---
paths:
  - "api/core/**/*.py"
  - "api/router/common.py"
  - "api/helpers/response.py"
---
# Logging and Error Rules
- Use structured logs with request/correlation ID, route, status, and duration.
- Redact authorization, cookies, passwords, tokens, reset links, and sensitive body fields.
- Preserve stack traces internally while returning stable public error messages.
- Ensure error middleware never raises a second error while handling the first.
