# Claude Kit Validation

Validation date: 2026-07-15

## Kit checks
- `.claude/settings.json`: valid JSON.
- Secret/protected-file hook: allows a normal source file and blocks `api/.env` with exit code 2.
- Rules: 19, organized recursively as `<group>/<rule>/RULE.md`.
- Specialized agents: 8, organized recursively as `<group>/<agent>/AGENT.md`.
- Skills/workflows: 9, each using `<skill>/SKILL.md`.
- `node scripts/quality-gate.mjs --quick`: PASS (secret scan, merge markers, Python syntax).

## Existing project baseline exposed by the full gate
`node scripts/quality-gate.mjs --full` correctly returns FAIL because the application is not complete yet:
- frontend lint: 15 errors and 12,419 warnings;
- frontend unit tests: one failed suite caused by an invalid NavBar import;
- frontend production build: missing/case-mismatched `RichTextCustom.vue`;
- production dependency audit: 15 vulnerabilities (2 low, 6 moderate, 5 high, 2 critical);
- Docker validation skipped in the audit environment because Docker was unavailable;
- backend tests skipped because the repository contains no Python test files.

These are project defects recorded in `PROJECT-AUDIT.md`; they are not hidden or auto-fixed by the kit.
