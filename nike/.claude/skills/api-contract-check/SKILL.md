---
name: api-contract-check
description: Compare frontend REST calls with FastAPI routes and schemas, then identify or fix contract drift.
argument-hint: "[check|fix] [domain]"
---
Enumerate backend methods/paths and frontend repository calls for the requested domain. Compare HTTP method, path, params/body, authentication, response payload, status/error behavior, and nullability. In `check` mode return a table of mismatches. In `fix` mode repair one domain coherently and add contract/integration tests.
