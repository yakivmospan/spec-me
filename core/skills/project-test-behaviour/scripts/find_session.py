#!/usr/bin/env python3
"""Find the Claude Code session a person ran for one test prompt, and say which model answered it.

A session is matched by its first typed message, never by being the newest: the session running the
test writes to the same folder, and it quotes every prompt it hands out. Sessions already scored are
passed with --skip so a repeat of the same prompt finds the next run.

Usage: python3 find_session.py "first line of the prompt" [--skip ID ...] [--repo-root PATH]
Prints one line per match, newest first: <path> <model(s)> <first message's start>.
"""
import argparse
import json
import re
import subprocess
from pathlib import Path


def repo_root(override):
    if override:
        return Path(override).resolve()
    out = subprocess.run(["git", "-C", str(Path(__file__).parent), "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True)
    return Path(out.stdout.strip() or Path.cwd())


def transcripts(root: Path):
    """Claude Code names the folder after the absolute path, every non-alphanumeric turned into a dash."""
    folder = Path.home() / ".claude/projects" / re.sub(r"[^A-Za-z0-9]", "-", str(root))
    return sorted(folder.glob("*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)


def first_typed_message(path: Path):
    """The first message a person typed; a skill's inserted text is marked isMeta and is not one."""
    for line in path.read_text(errors="replace").splitlines():
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if obj.get("type") != "user" or obj.get("isMeta"):
            continue
        content = (obj.get("message") or {}).get("content")
        if isinstance(content, str):
            return content
        texts = [c.get("text", "") for c in content or [] if isinstance(c, dict) and c.get("type") == "text"]
        if texts:
            return "\n".join(texts)
    return ""


def models(path: Path):
    found = set()
    for line in path.read_text(errors="replace").splitlines():
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if obj.get("type") == "assistant":
            found.add((obj.get("message") or {}).get("model") or "?")
    return sorted(found)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("prompt", help="the prompt's first line, or any part of it")
    parser.add_argument("--skip", nargs="*", default=[], help="session ids already scored")
    parser.add_argument("--repo-root")
    args = parser.parse_args()
    key = args.prompt.strip().lower()
    for path in transcripts(repo_root(args.repo_root)):
        if any(path.stem.startswith(s) for s in args.skip):
            continue
        first = first_typed_message(path)
        if key in first.lower():
            print(f"{path} {','.join(models(path))} {first.strip()[:60]!r}")


main()
