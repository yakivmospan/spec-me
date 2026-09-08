#!/usr/bin/env python3
"""Print every skill's full description and its word counts against project-create-rule-or-skill's budget.

Stdlib only. Reads `.agents/skills/*/SKILL.md`, following links, so user-only skills linked in from
`.agents/.local/skills/` are listed too and marked `local`. Counts are whitespace-separated words, the
same as `wc -w`: the description, and the body below the frontmatter with examples included.

Usage:
    python3 .agents/skills/project-create-rule-or-skill/scripts/skill_stats.py [--repo-root <path>] [name ...]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

DESCRIPTION_WORDS = 100
DESCRIPTION_CHARS = 1024
BODY_WORDS = 1500
BODY_LINES = 500


def find_repo_root(start: Path) -> Path:
    for candidate in [start, *start.parents]:
        if (candidate / ".agents" / "skills").is_dir():
            return candidate
    sys.exit("No .agents/skills/ above this script; pass --repo-root.")


def split(text: str) -> tuple[str, str]:
    """Frontmatter and body. A file without frontmatter is all body."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return "", text
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return "\n".join(lines[1:i]), "\n".join(lines[i + 1:])
    return "", text


def description(frontmatter: str) -> str:
    """The `description:` value, including a folded or literal block (`>` or `|`) spanning lines."""
    lines = frontmatter.splitlines()
    for i, line in enumerate(lines):
        if not line.startswith("description:"):
            continue
        value = line[len("description:"):].strip()
        if value and value[0] not in ">|":
            return value.strip("\"'")
        continued = []
        for more in lines[i + 1:]:
            if more and not more[0].isspace():
                break
            continued.append(more.strip())
        return " ".join(part for part in continued if part)
    return ""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("names", nargs="*", help="only these skills")
    parser.add_argument("--repo-root", type=Path)
    args = parser.parse_args()

    root = args.repo_root or find_repo_root(Path(__file__).resolve().parent)
    local = (root / ".agents" / ".local" / "skills").resolve()
    found = set()

    for skill_md in sorted((root / ".agents" / "skills").glob("*/SKILL.md")):
        name = skill_md.parent.name
        if args.names and name not in args.names:
            continue
        found.add(name)
        frontmatter, body = split(skill_md.read_text(encoding="utf-8"))
        desc = description(frontmatter)
        desc_words, desc_chars = len(desc.split()), len(desc)
        body_words, body_lines = len(body.split()), len(body.splitlines())
        flags = [f"description over {DESCRIPTION_WORDS} words"] * (desc_words > DESCRIPTION_WORDS)
        flags += [f"description over {DESCRIPTION_CHARS} characters (Anthropic's guidance)"] * (desc_chars > DESCRIPTION_CHARS)
        flags += [f"body over {BODY_WORDS} words"] * (body_words > BODY_WORDS)
        flags += [f"body over {BODY_LINES} lines (Anthropic's guidance)"] * (body_lines > BODY_LINES)
        where = "local" if skill_md.resolve().is_relative_to(local) or (skill_md.parent / ".forwarding-stub").is_file() else "shared"
        print(f"## {name} ({where}) — description {desc_words} words / {desc_chars} chars, "
              f"body {body_words} words / {body_lines} lines" + (f" — {'; '.join(flags)}" if flags else ""))
        print(desc or "(no description)")
        print()
    unknown = [name for name in args.names if name not in found]
    for name in unknown:
        print(f"error: no skill named {name!r} — no .agents/skills/{name}/SKILL.md", file=sys.stderr)
    return 1 if unknown else 0


if __name__ == "__main__":
    sys.exit(main())
