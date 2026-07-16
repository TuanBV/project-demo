---
name: prepare-commit
description: Stage and commit the current changes with a message matching this project's observed commit style. Only invoke when the user explicitly asks to commit.
disable-model-invocation: true
allowed-tools: Bash(git status), Bash(git diff *), Bash(git log *), Bash(git add *), Bash(git commit *)
---

Only run this when the user has explicitly asked for a commit in this turn — never invoke it
proactively.

1. Run `git status` and `git diff` (staged + unstaged) to see everything that would be
   committed. Run `git log --oneline -10` to see recent message style.
2. This repository's commit messages are in Vietnamese or English depending on the author and
   often (not always) use a `type(scope): description` prefix observed in history, e.g.
   `fix(security): ...`, `Add component Pagination`. Match the tone of recent commits rather
   than inventing a new convention.
3. Never commit `.env`, `data/*.db`, or any file that looks like it contains a real secret —
   if `git status` shows one staged, stop and flag it instead of committing.
4. Stage only the files relevant to the change (avoid `git add -A` if unrelated files are
   also dirty) and write a commit message describing *why*, not just *what* — one or two
   sentences.
5. After committing, run `git status` again to confirm the working tree is in the expected
   state.
6. Do not push unless the user separately asks to push.
