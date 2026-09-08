#!/usr/bin/env python3
"""Record one spec-sync-with-code run in .agents/.cache/spec-checks.json, where spec-rebuild-overviews shows it in INDEX.md.

    python3 record_check.py <spec id> [--passed N] [--failed N]
                            [--differs PART ...] [--cant-tell PART ...] [--repo-root PATH]

One entry per spec id; a new run replaces the last one.
"""
from __future__ import annotations

import argparse
import json
import subprocess
from datetime import date
from pathlib import Path


def find_repo_root(override: str | None) -> Path:
    if override:
        return Path(override).resolve()
    here = Path(__file__).resolve()
    try:
        result = subprocess.run(
            ["git", "-C", str(here.parent), "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, timeout=10,
        )
        if result.returncode == 0:
            return Path(result.stdout.strip())
    except (OSError, subprocess.SubprocessError):
        pass
    # .agents/skills/spec-sync-with-code/scripts/record_check.py
    return here.parents[4]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("spec_id")
    parser.add_argument("--passed", type=int, default=0)
    parser.add_argument("--failed", type=int, default=0)
    parser.add_argument("--differs", nargs="*", default=[])
    parser.add_argument("--cant-tell", nargs="*", default=[])
    parser.add_argument("--repo-root")
    args = parser.parse_args()

    path = find_repo_root(args.repo_root) / ".agents" / ".cache" / "spec-checks.json"
    checks: dict = {}
    if path.is_file():
        try:
            checks = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            checks = {}

    checks[args.spec_id] = {
        "date": date.today().isoformat(),
        "passed": args.passed,
        "failed": args.failed,
        "differs": args.differs,
        "cant_tell": args.cant_tell,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(checks, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"recorded {args.spec_id} in {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
