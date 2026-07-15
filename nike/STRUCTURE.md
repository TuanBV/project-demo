# Cấu trúc `.claude`

```text
.claude/
├── agents/
│   ├── architecture/project-architect/AGENT.md
│   ├── backend/fastapi-backend/AGENT.md
│   ├── frontend/vue-frontend/AGENT.md
│   ├── database/database-migration/AGENT.md
│   ├── quality/test-engineer/AGENT.md
│   ├── security/security-reviewer/AGENT.md
│   ├── devops/devops-reviewer/AGENT.md
│   └── review/code-reviewer/AGENT.md
├── skills/
│   ├── audit-project/SKILL.md
│   ├── fix-build/SKILL.md
│   ├── implement-feature/SKILL.md
│   ├── api-contract-check/SKILL.md
│   ├── database-migration/SKILL.md
│   ├── integration-test/SKILL.md
│   ├── security-review/SKILL.md
│   ├── quality-gate/SKILL.md
│   └── release-readiness/SKILL.md
├── rules/
│   ├── core/
│   ├── contracts/
│   ├── backend/
│   ├── frontend/
│   ├── quality/
│   ├── security/
│   └── infrastructure/
├── hooks/protect-files.mjs
├── README.md
├── settings.json
└── settings.local.example.json
```
