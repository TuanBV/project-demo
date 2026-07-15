---
paths:
  - "frontend/src/shared/service/**/*.js"
  - "frontend/src/stores/**/*.js"
  - "frontend/src/router/**/*.js"
---
# Frontend Service and State Rules
- REST repositories only build requests; services map domain results; stores manage state.
- Never return `null` for every failure without preserving an actionable error.
- Configure API base URL with Vite environment variables.
- Router guards use explicit roles and avoid unnecessary session requests on every navigation.
- Cart/order state must be server-authoritative after authentication.
