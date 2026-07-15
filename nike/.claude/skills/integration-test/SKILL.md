---
name: integration-test
description: Add and run integration tests for an API or end-to-end domain flow.
argument-hint: "<flow, e.g. login-profile or cart-checkout>"
---
Create deterministic tests for `$ARGUMENTS` covering happy path, unauthorized/forbidden, validation, not-found/conflict, and transaction rollback where relevant. Use test configuration and fakes for external email/social services. Do not depend on real credentials or public network. Run targeted tests and report exact results.
