---
name: security-review
description: Run a structured security review and, when requested, fix findings without exposing secrets.
argument-hint: "[review|fix] [area]"
disable-model-invocation: true
---
Use the `nike-security-reviewer` agent for review mode. Inspect auth, authorization, object ownership, cookies/CORS/JWT, password/reset, uploads, SQL/query construction, secrets, logs, dependencies, Docker, and external integrations. Rank findings with file references and exploit scenarios. In fix mode address Critical/High findings first, add regression tests, and run the security plus full quality gates.
