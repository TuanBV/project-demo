# Claude Code kit — Interview Review System

This kit is scoped to this project only (`KIT_MODE=project`). It reflects the actual stack
and workflows found in this repository at the time of generation — not a generic template.

## 1. Detected stack

- **Language/runtime**: Python 3.12+ (`pyproject.toml: requires-python = ">=3.12"`)
- **Web framework**: FastAPI 0.115+, Uvicorn (`app/main.py`)
- **ORM/migrations**: SQLAlchemy 2.x + Alembic (`app/db/models/*`, `alembic/versions/*`,
  `render_as_batch=True` in `alembic/env.py` for SQLite)
- **Validation**: Pydantic v2 + pydantic-settings (`app/schemas/*`, `app/core/config.py`)
- **DB**: SQLite by default (`DATABASE_URL=sqlite:///./data/app.db`), Postgres-compatible
  (partial index conditions use `sqlite_where`/`postgresql_where`)
- **Templating/frontend**: Jinja2 + vanilla JS (`app/templates/*`, `app/static/js/*`) — no
  frontend framework/build step
- **Import formats**: `python-docx` (DOCX), custom text parsers (`app/importers/*`)
- **Testing**: pytest + pytest-cov, `httpx`/`TestClient` for integration tests
  (`tests/conftest.py`)
- **Lint/format/typecheck**: Ruff (format + lint), mypy (`pyproject.toml`)
- **Containerization**: Docker + Docker Compose (`Dockerfile`, `docker-compose.yml`)
- **Task runner**: `Makefile` (install/run/migrate/seed/test/lint/format/typecheck/check/
  docker-up/docker-down — all commands used below come from here or from `README.md`)
- **CI**: none found (no `.github/workflows`) — quality gate is run manually via `make check`

**Important repo-topology note**: this project's actual git root is the parent
`project-demo/` directory, which also contains an unrelated sibling project (`nike/`, a
Vue/Node app) sharing the same commit history. Several early-draft rules in this kit were
corrected after discovering that some commit messages that looked QA-relevant (a leaked-secret
fix, an env-driven CORS/cookie fix) actually touched only `nike/` files. See
`.claude/agents/architecture-researcher.md` and `.claude/agents/debugger.md`, which both
encode this check explicitly.

## 2. Kit architecture

| Need | Component | Why |
|---|---|---|
| Always-true facts (stack, layering, invariants summary) | `CLAUDE.md` | loaded every session |
| Path-scoped constraints (MC integrity, migrations, security, testing) | `.claude/rules/*.md` | loaded when touching matching files |
| Multi-step procedures (add import format, create migration, etc.) | `.claude/skills/*/SKILL.md` | loaded on demand, usable as `/skill-name` |
| Specialized read-mostly workers (research, debug, review) | `.claude/agents/*.md` | own context window, scoped tools |
| Deterministic automation (format-on-edit) | `.claude/settings.json` `hooks` + `.claude/scripts/hooks/*.py` | runs on every matching tool call |
| Tool/file permissions | `.claude/settings.json` `permissions` | least-privilege allow/ask/deny |
| External tool integration | *(none configured)* | no MCP need found — see §10 |

## 3. Files created

```text
CLAUDE.md                              # trimmed: facts only, procedures moved to skills
.claude/
├── README.md                          # this file
├── settings.json                      # permissions (least-privilege) + format-on-edit hook
├── rules/
│   ├── architecture.md                # layering, evaluation/importers purity, no-ORM-to-API
│   ├── mc-integrity.md                # 4-option/1-correct, no answer leak, backend shuffle
│   ├── database-migrations.md         # Alembic batch-mode gotchas
│   ├── security.md                    # no untrusted exec, no secrets, client-trust boundary
│   ├── testing-requirements.md        # mandatory test subsets per touched area
│   └── configuration.md               # Settings/.env.example convention
├── skills/
│   ├── verify-change/SKILL.md         # run the full quality gate
│   ├── prepare-commit/SKILL.md        # git add+commit (manual only)
│   ├── update-documentation/SKILL.md  # keep CLAUDE.md/README.md/docs/*.md in sync
│   ├── create-database-migration/SKILL.md
│   ├── add-import-format/SKILL.md
│   ├── add-evaluator/SKILL.md
│   ├── add-question-type/SKILL.md
│   ├── add-question-topic/SKILL.md    # bulk MC question seed-data workflow
│   ├── create-api-endpoint/SKILL.md
│   ├── run-local-stack/SKILL.md
│   ├── docker-verify/SKILL.md
│   └── write-tests/SKILL.md
├── agents/
│   ├── architecture-researcher.md     # read-only
│   ├── debugger.md                    # read-only
│   ├── test-engineer.md               # read-write (tests only)
│   ├── code-reviewer.md               # read-only
│   └── security-reviewer.md           # read-only
└── scripts/hooks/
    └── format_python_on_edit.py       # PostToolUse hook body (stdlib only)
```

## 4. Skills / slash commands

| Command | Purpose | Args | Model auto-invoke | Tools |
|---|---|---|---|---|
| `/verify-change` | Run `make check` equivalent (ruff format/check, mypy, pytest) | none | Yes | Bash (format/check/mypy/pytest/make) |
| `/prepare-commit` | Stage + commit with project-style message | none | **No** (manual only) | git status/diff/log/add/commit |
| `/update-documentation` | Sync CLAUDE.md/README.md/docs after a change | none | Yes | Read/Grep/Glob/Edit |
| `/create-database-migration` | Alembic revision + batch-mode fixups + round-trip test | none | Yes | alembic, Read/Edit |
| `/add-import-format` | Add a new DOCX/text import format | none | Yes | Read/Edit/Write/Grep/Glob, pytest importers |
| `/add-evaluator` | Add a new FREE_TEXT answer evaluator | none | Yes | Read/Edit/Write/Grep, pytest evaluation |
| `/add-question-type` | Add a new `QuestionType`/`QuestionFormat` value | none | Yes | Read/Edit/Grep, alembic |
| `/add-question-topic` | Add ~20 MC questions for a new category | none | Yes | Read/Write/Edit, seed script, pytest scripts |
| `/create-api-endpoint` | Add a FastAPI route following project layering | none | Yes | Read/Edit/Write/Grep/Glob |
| `/run-local-stack` | Start the app (venv or Docker) | none | Yes | make, docker compose, alembic, curl |
| `/docker-verify` | Build + verify Docker image on a disposable volume | none | Yes | docker build/run/volume/logs, curl |
| `/write-tests` | Write a test following project conventions | none | Yes | Read/Write/Edit/Grep/Glob, pytest |

Only `/prepare-commit` has a side effect (git commit) and requires explicit invocation.

## 5. Agents

| Agent | When to use | Model | Tools | Read-only? |
|---|---|---|---|---|
| `architecture-researcher` | Understand data/call flow before changing something | inherit | Read, Grep, Glob, git log/blame/show | Yes |
| `debugger` | Investigate a failing test / traceback / unexpected behavior | inherit | Read, Grep, Glob, pytest, python -c, alembic, docker logs, curl | Yes |
| `test-engineer` | Design/implement tests for a change | inherit | Read, Write, Edit, Grep, Glob, pytest | No (writes tests only) |
| `code-reviewer` | Project-specific invariant review (complements the global `/code-review` skill) | inherit | Read, Grep, Glob, git diff/log | Yes |
| `security-reviewer` | Project-specific security review (complements the global `/security-review` skill) | inherit | Read, Grep, Glob, git diff/log/show | Yes |

## 6. Hooks

| Event | Matcher | Script | Effect | Fail-open/closed | Test result |
|---|---|---|---|---|---|
| `PostToolUse` | `Edit\|Write` | `.claude/scripts/hooks/format_python_on_edit.py` | Runs `ruff format` on the single `.py` file just edited (no-op for other extensions) | **Fail-open** — any error (ruff missing, wrong tool, non-.py, missing file) exits 0 silently, never blocks the edit | PASS — see §8 |

No PreToolUse blocking hook was added: secret/sensitive-file protection is handled by
`permissions.deny` in `settings.json` instead (the more direct mechanism for that), so a
duplicate hook would add complexity without adding safety.

## 7. Permissions and security

**Allowed** (from `settings.json`): read-only git (`status`/`diff`/`log`/`show`/`branch`),
`make *` (all Makefile targets are non-destructive), `ruff format/check`, `mypy app`,
`pytest *`, `alembic *`, `python scripts/*.py`, `uvicorn app.main:app *`,
`docker compose up/build/down/logs`, `curl http://localhost:*`, reading `.env.example`.

**Ask first**: `docker build/run/volume/stop/rm` (broader than the Makefile's own
`docker compose` targets), `git add`/`git commit` (side effects — also gated by
`prepare-commit`'s own `disable-model-invocation: true`), `pip install *`,
`alembic downgrade *`.

**Denied**: reading/editing `.env` (real secrets) and `data/*.db*` (runtime DB files —
migrations are the only sanctioned way to change schema); force-push, `reset --hard`,
`git clean`, `branch -D`, `rm -rf *`.

**Secret protection**: `.env.example` stays readable/editable (placeholders only); `.env`
itself is denied for both Read and Edit. No secret was written into any kit file (scanned).

**Side-effect protection**: `prepare-commit` is the only skill with a git-writing side
effect, and it requires `disable-model-invocation: true` — Claude never invokes it on its
own.

## 8. Validation results

| Check | Status |
|---|---|
| All JSON files parse (`settings.json`) | PASS |
| All skill/agent YAML frontmatter parses, no duplicate names | PASS |
| All `paths:` globs in `.claude/rules/*.md` match real files | PASS |
| `ruff check .` on the whole repo (kit files are Markdown/JSON, no code impact) | PASS |
| `mypy app` | PASS (75 source files, no issues) |
| `pytest` (existing suite, unaffected by kit files) | PASS (182 passed) |
| Hook script: sample PostToolUse payload (Edit, `.py` file) → file reformatted | PASS |
| Hook script: non-Edit tool, non-`.py` file, missing file → no-op, exit 0 | PASS |
| Hook script: Unicode project path (`Máy tính`) → fixed `stdin.reconfigure(encoding="utf-8")` bug found and fixed during validation | PASS after fix |
| Secret scan on all new kit files | PASS (no secrets found) |
| MCP servers configured (`claude mcp list`) | SKIPPED — no `.mcp.json` created (no verified need, see §10) |
| `/doctor` | SKIPPED — not run in this non-interactive session |

## 9. How to add a new rule, skill, or agent

- **Rule**: new file in `.claude/rules/`, one topic per file, add `paths:` frontmatter if it
  only applies to specific files. Base it on an actual pattern you found in the code, not a
  generic best practice.
- **Skill**: new directory `.claude/skills/<name>/SKILL.md`. Add `disable-model-invocation:
  true` if it has a side effect (commit, deploy, external write). Keep the body under ~60
  lines; put anything longer in a supporting file in the same directory.
- **Agent**: new file `.claude/agents/<name>.md`. Give it a narrow, unambiguous trigger in
  `description`, and only the tools it actually needs — default to read-only (`Read, Grep,
  Glob`) unless it must write.

## 10. Recommendations not automatically applied

These weren't configured because this session found no concrete, verified need — adding them
speculatively would violate this kit's own "no fabricated config" rule.

- **GitHub MCP server**: the repo has a GitHub remote
  (`https://github.com/TuanBV/project-demo.git`) but no evidence of an issue-tracker-driven
  workflow (no `.github/` templates, no linked issues found). If you start using GitHub
  Issues/PRs as the primary workflow, a GitHub MCP server (or the `gh` CLI, already usable via
  Bash) would let Claude read/comment on issues and PRs directly.
- **Python LSP plugin**: not verified in this session whether an official Claude Code LSP
  plugin for Python is available for your installed version. Check
  `/plugin marketplace` inside an interactive session before adding one.
- **CI integration**: there's no `.github/workflows` in this repo. If you add CI, consider
  mirroring `make check` in the workflow so local and CI results can't diverge.

## Local-only files (don't commit)

- `.claude/settings.local.json` (not created by this kit, but if you add personal overrides,
  put them here — it's meant to be gitignored).
- `CLAUDE.local.md` (same idea, for personal-only instructions).

## Troubleshooting

- A skill not triggering automatically → check its `description` is specific enough, or
  invoke it directly with `/skill-name`.
- The format-on-edit hook seems to do nothing → confirm `.venv/Scripts/ruff.exe` (Windows) or
  `.venv/bin/ruff` (POSIX) exists; the hook falls back to a bare `ruff` on `PATH` otherwise
  and silently no-ops if that's not found either (by design — it fails open).
- If a rule/skill/agent references a file path that no longer exists after a refactor, update
  or remove the reference — don't leave stale evidence in the kit.
