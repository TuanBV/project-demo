#!/usr/bin/env python
"""PostToolUse hook: after Edit/Write touches a .py file in this project, run `ruff format`
on that single file only. Stdlib-only, cross-platform (Windows/macOS/Linux).

Reads the PostToolUse JSON payload from stdin (fields: tool_name, tool_input.file_path, cwd).
Fails open: any problem here (ruff missing, file outside the project, non-.py file) is a
silent no-op with exit code 0 -- this hook must never block or slow down normal edits.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def _find_ruff(project_dir: Path) -> str | None:
    for candidate in (
        project_dir / ".venv" / "Scripts" / "ruff.exe",  # Windows venv
        project_dir / ".venv" / "bin" / "ruff",  # POSIX venv
    ):
        if candidate.exists():
            return str(candidate)
    return "ruff"  # fall back to PATH; subprocess will fail open if not found


def main() -> int:
    # On Windows, sys.stdin otherwise decodes with the console's active codepage instead of
    # UTF-8, silently mangling any non-ASCII byte in the JSON payload (e.g. a Unicode
    # character in the project path) before json.load ever sees it.
    if hasattr(sys.stdin, "reconfigure"):
        sys.stdin.reconfigure(encoding="utf-8")

    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0

    if payload.get("tool_name") not in ("Edit", "Write"):
        return 0

    file_path = payload.get("tool_input", {}).get("file_path")
    if not file_path or not file_path.endswith(".py"):
        return 0

    project_dir = Path(payload.get("cwd") or ".").resolve()
    target = Path(file_path)
    if not target.is_absolute():
        target = project_dir / target
    if not target.exists():
        return 0

    ruff = _find_ruff(project_dir)
    try:
        subprocess.run(
            [ruff, "format", "--quiet", str(target)],
            cwd=str(project_dir),
            timeout=15,
            capture_output=True,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        pass  # fail open -- formatting is best-effort, never blocks the edit

    return 0


if __name__ == "__main__":
    sys.exit(main())
