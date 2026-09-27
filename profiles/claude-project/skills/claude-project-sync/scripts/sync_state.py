#!/usr/bin/env python3
"""Keep `.claude-project/SYNC.md` true: list what a Claude project syncs, and find edits it would miss.

A sync between the repository and the project tells which side changed a file by the file's last
change row, so this script only reads and lists — moving files is the project chat's job.

  link   add a row, never synced, for every file under .specs/, docs/ and print/ that has none;
         rows already there are kept as they are
  check  list files edited after their last change row, files with no row, and rows whose file is gone

Usage: python3 sync_state.py link|check [--repo-root PATH] [--check]
"""
import argparse
import re
import subprocess
from datetime import date
from pathlib import Path

SYNC = ".claude-project/SYNC.md"
FOLDERS = (".specs", "docs", "print")
# Written by a script, or the process's own guide: not the project's material.
GENERATED = {".specs/INDEX.md", ".specs/DECISIONS.md", ".specs/OPEN-QUESTIONS.md", ".specs/README.md"}
ROW = re.compile(r"^\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*·\s*([^|]+?)\s*\|\s*([^|]*?)\s*\|$")
DAY = re.compile(r"\b(\d{4}-\d{2}-\d{2})\b")


def repo_root(override):
    if override:
        return Path(override).resolve()
    out = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True)
    return Path(out.stdout.strip()) if out.returncode == 0 else Path.cwd()


def ignored(root: Path, paths):
    """The paths git ignores; none when this is not a repository."""
    if not paths:
        return set()
    out = subprocess.run(["git", "-C", str(root), "check-ignore", "--stdin"], input="\n".join(paths),
                         capture_output=True, text=True)
    return set(out.stdout.split("\n")) if out.returncode in (0, 1) else set()


def project_name(path: str):
    """A file's name in the project: its path with dots for slashes and no leading dot.

    A spec inside an open change already carries its future name — `specs.00-product.md` — so it keeps
    it. Anything else in a change folder, the plan above all, is the repository's own.
    """
    parts = path.split("/")
    if parts[:2] == [".specs", "changes"]:
        return parts[-1] if len(parts) == 4 and parts[-1].startswith("specs.") else None
    return path.lstrip(".").replace("/", ".")


def candidates(root: Path):
    """Every file the project should hold, as {repository path: project name}."""
    found = []
    for folder in FOLDERS:
        base = root / folder
        for f in sorted(base.rglob("*")) if base.is_dir() else []:
            rel = f.relative_to(root).as_posix()
            if f.is_file() and not f.name.startswith(".") and rel not in GENERATED:
                found.append(rel)
    skip = ignored(root, found)
    return {p: n for p in found if p not in skip and (n := project_name(p))}


def read_sync(root: Path):
    """The file's head lines and its rows, as (head, [(project name, repo, path, last synced)])."""
    path = root / SYNC
    if not path.is_file():
        return [], []
    head, rows = [], []
    for line in path.read_text().splitlines():
        m = ROW.match(line.strip())
        if m and m.group(1) != "Project file":
            rows.append(m.groups())
        elif not line.startswith("|") and not rows:
            head.append(line)
    return head, rows


def last_change(path: Path):
    """The day of a file's last change row, or None when it has no dated table row."""
    if path.suffix != ".md":
        return None
    days = [DAY.findall(line) for line in path.read_text(errors="replace").splitlines()
            if line.startswith("|")]
    days = [d[-1] for d in days if d]
    return days[-1] if days else None


def link(root: Path, check: bool):
    head, rows = read_sync(root)
    known = {r[2] for r in rows}
    repo = root.name
    added = [(n, repo, p, "never") for p, n in candidates(root).items() if p not in known]
    for n, _, p, _ in added:
        print(f"{'would add' if check else 'added'}  {p}  →  {n}")
    if not added:
        print("nothing to add — every file has a row")
        return 0
    if check:
        return 0
    head = head or ["# Sync — last: never", ""]
    while head and not head[-1].strip():
        head.pop()
    lines = head + ["", "| Project file | Repository · path | Last synced change |", "|---|---|---|"]
    lines += [f"| {n} | {r} · {p} | {s} |" for n, r, p, s in rows + added]
    (root / SYNC).parent.mkdir(parents=True, exist_ok=True)
    (root / SYNC).write_text("\n".join(lines) + "\n")
    print(f"\n{len(added)} row(s) added to {SYNC}, never synced")
    return 0


def check(root: Path):
    head, rows = read_sync(root)
    if not head and not rows:
        print(f"no {SYNC} — say \"link this repo\" first")
        return 1
    known = {r[2] for r in rows}
    unrecorded, gone = [], []
    for _, _, p, _ in rows:
        f = root / p
        if not f.is_file():
            gone.append(p)
            continue
        recorded = last_change(f)
        edited = date.fromtimestamp(f.stat().st_mtime).isoformat()
        if recorded and edited > recorded:
            unrecorded.append((p, recorded, edited))
    new = [p for p in candidates(root) if p not in known]
    for p, recorded, edited in unrecorded:
        print(f"no row   {p} — edited {edited}, last change row {recorded}")
    for p in new:
        print(f"new      {p} — not in {SYNC}")
    for p in gone:
        print(f"gone     {p} — in {SYNC}, not on disk")
    if not (unrecorded or new or gone):
        print("in step — every edit has its row, every file its line")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("command", choices=("link", "check"))
    ap.add_argument("--repo-root")
    ap.add_argument("--check", action="store_true", help="link: say what would be added, write nothing")
    args = ap.parse_args()
    root = repo_root(args.repo_root)
    raise SystemExit(link(root, args.check) if args.command == "link" else check(root))


if __name__ == "__main__":
    main()
