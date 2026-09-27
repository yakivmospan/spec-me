#!/usr/bin/env python3
"""One fingerprint for the files a snapshot was made from, so a copy of it can tell when it is behind.

The same files with the same content give the same fingerprint, in any order and on any machine; a
change to any of them, or a file added or gone, gives a different one. Paths are taken relative to
the repository root, so two checkouts of one project agree.

Usage: python3 fingerprint.py [--repo-root PATH] FILE...
Prints the fingerprint on the first line, then one line per file it could not read.
"""
import argparse
import hashlib
import subprocess
import sys
from pathlib import Path


def repo_root(override):
    if override:
        return Path(override).resolve()
    out = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True)
    return Path(out.stdout.strip()) if out.stdout.strip() else Path.cwd()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo-root")
    ap.add_argument("files", nargs="+")
    args = ap.parse_args()
    root = repo_root(args.repo_root)
    digest, missing = hashlib.sha256(), []
    for name in sorted({Path(f).resolve().relative_to(root).as_posix()
                        if Path(f).resolve().is_relative_to(root) else f for f in args.files}):
        path = root / name
        if not path.is_file():
            missing.append(name)
            continue
        digest.update(name.encode() + b"\0" + path.read_bytes() + b"\0")
    print(digest.hexdigest()[:12])
    for name in missing:
        print(f"missing {name}")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
