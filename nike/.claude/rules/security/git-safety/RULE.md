# Git Safety
- Work on a feature branch based on the latest agreed integration branch.
- Never directly push to protected branches.
- Rebase before PR when appropriate; use `--force-with-lease`, never plain `--force`.
- Do not discard unrelated user changes.
- Review staged diff and secret scan before commit.
- Prefer small conventional commits that each leave the project coherent.
