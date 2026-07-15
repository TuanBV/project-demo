---
name: release-readiness
description: Verify MVP acceptance criteria, migrations, tests, security, documentation, and operations before release.
argument-hint: "[milestone or version]"
disable-model-invocation: true
---
Read `docs/acceptance-criteria.md` and inspect the diff since the release base. Run full quality gate, Docker config validation, security review, migration review, and critical flow tests. Return a release decision: READY, READY WITH FOLLOW-UPS, or NOT READY, with blocking evidence, rollback plan, and remaining risks. Do not deploy.
