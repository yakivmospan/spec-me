#!/usr/bin/env python3
"""List declarations a change removed or renamed that are still mentioned somewhere.

Compares the working tree (staged, unstaged and untracked files) with a git ref, collects the names
declared on removed lines that no added line declares again and no file still declares, and prints
every remaining mention of each — in code, comments, docs or specs. Any language: declarations are
recognised by their keyword (fun, def, class, val, ...), so a hit is a lead to check, not a verdict.

Usage: python3 stale_refs.py [--base REF] [--repo-root PATH] [--exclude DIR ...] [--max-hits N]
"""
import argparse
import os
import re
import subprocess
import sys

KEYWORDS = (
    r"fun|def|function|func|fn|class|interface|object|enum|struct|trait|protocol|record|typealias"
)
# A keyword followed by another keyword is a modifier (`enum class X`, `fun interface X`): the name comes
# after the last one.
DECLARATION = re.compile(
    rf"\b(?:{KEYWORDS})\s+(?!(?:{KEYWORDS})\b)(?:[A-Za-z_][\w<>, ?]*\.)?([A-Za-z_]\w*)"
)
# A variable counts only as a member or a top-level value: with a modifier, or indented at most one
# level. Local variables and parameters come and go with their function and are too common to track.
VARIABLE = re.compile(
    r"^(?:\s{0,4}|\s*(?:(?:private|protected|internal|public|override|open|lateinit|const|static|"
    r"export|readonly)\s+)+)(?:val|var|let|const)\s+([A-Za-z_]\w*)"
)
SKIPPED_DIRS = {
    ".git", ".gradle", ".idea", ".cache", ".venv", "venv", "node_modules", "build", "out", "dist",
    "target", "__pycache__", ".next", ".dart_tool", "Pods", "graphify-out",
}
OWN_FOLDER = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
MIN_NAME_LENGTH = 3
MAX_FILE_BYTES = 1_000_000


def git(root, *args):
    result = subprocess.run(["git", "-C", root, *args], capture_output=True, text=True)
    if result.returncode != 0:
        sys.exit(f"stale_refs: git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout


def repo_root(override):
    if override:
        return os.path.abspath(override)
    return git(os.getcwd(), "rev-parse", "--show-toplevel").strip()


def declared_names(lines):
    names = set()
    for line in lines:
        names.update(match.group(1) for match in DECLARATION.finditer(line))
        variable = VARIABLE.match(line)
        if variable:
            names.add(variable.group(1))
    return {name for name in names if len(name) >= MIN_NAME_LENGTH}


def changed_lines(root, base):
    removed, added = [], []
    for line in git(root, "diff", "--unified=0", "--no-color", "--no-ext-diff", base).splitlines():
        if line.startswith("---") or line.startswith("+++"):
            continue
        if line.startswith("-"):
            removed.append(line[1:])
        elif line.startswith("+"):
            added.append(line[1:])
    for path in git(root, "ls-files", "--others", "--exclude-standard").splitlines():
        added.extend(read_text(os.path.join(root, path)) or [])
    return removed, added


def read_text(path):
    try:
        if os.path.getsize(path) > MAX_FILE_BYTES:
            return None
        with open(path, "rb") as file:
            data = file.read()
    except OSError:
        return None
    if b"\0" in data[:4096]:
        return None
    return data.decode("utf-8", errors="replace").splitlines()


def mention_pattern(name):
    """A plain lowercase word (`trigger`, `recheck`) is everyday prose too, so only its code-shaped
    mentions count: called, reached with a dot, or in backticks. Any other name counts wherever it stands."""
    escaped = re.escape(name)
    if re.fullmatch(r"[a-z]+", name):
        return re.compile(rf"(?:\.{escaped}\b|\b{escaped}\s*\(|`{escaped}\b)")
    return re.compile(rf"\b{escaped}\b")


def text_files(root, excluded):
    for directory, subdirectories, files in os.walk(root):
        relative = os.path.relpath(directory, root)
        subdirectories[:] = [
            name for name in subdirectories
            if name not in SKIPPED_DIRS and os.path.normpath(os.path.join(relative, name)) not in excluded
        ]
        if os.path.realpath(directory).startswith(OWN_FOLDER):
            continue
        for name in files:
            path = os.path.join(directory, name)
            lines = read_text(path)
            if lines is not None:
                yield os.path.relpath(path, root), lines


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--base", default="HEAD", help="git ref to compare the working tree with (default: HEAD)")
    parser.add_argument("--repo-root", help="repository root (default: found with git)")
    parser.add_argument("--exclude", nargs="*", default=[], help="directories to skip, relative to the root")
    parser.add_argument("--max-hits", type=int, default=20, help="mentions shown per name (default: 20)")
    args = parser.parse_args()

    root = repo_root(args.repo_root)
    removed, added = changed_lines(root, args.base)
    candidates = declared_names(removed) - declared_names(added)
    if not candidates:
        print("stale_refs: the change removed no declarations")
        return

    excluded = {os.path.normpath(path) for path in args.exclude}
    files = list(text_files(root, excluded))
    still_declared = declared_names(line for _, lines in files for line in lines)
    gone = sorted(candidates - still_declared)
    if not gone:
        print("stale_refs: no stale references")
        return

    patterns = {name: mention_pattern(name) for name in gone}
    mentions = {name: [] for name in gone}
    for path, lines in files:
        for number, line in enumerate(lines, start=1):
            for name, pattern in patterns.items():
                if pattern.search(line):
                    mentions[name].append(f"{path}:{number}: {line.strip()[:160]}")

    stale = {name: hits for name, hits in mentions.items() if hits}
    if not stale:
        print("stale_refs: no stale references")
        return
    print(f"stale_refs: {len(stale)} removed or renamed declaration(s) still mentioned")
    for name, hits in stale.items():
        print(f"\n{name} — {len(hits)} mention(s)")
        for hit in hits[: args.max_hits]:
            print(f"  {hit}")
        if len(hits) > args.max_hits:
            print(f"  … {len(hits) - args.max_hits} more")


if __name__ == "__main__":
    main()
