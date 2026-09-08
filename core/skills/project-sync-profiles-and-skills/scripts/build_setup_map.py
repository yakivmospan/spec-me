#!/usr/bin/env python3
"""Refresh the measured parts of .agents/SETUP-MAP.html from the files it describes.

Stdlib only, same as build_index.py.

The map is the one document here that describes the rules a second time, so it is the one that
can quietly stop being true. Two halves, and only one of them can be generated:

  Measured   — word counts, totals, file and skill counts. Mechanical, drifts on every edit, and
               worthless when wrong. This script owns it.
  Written    — the three figures, the captions, why each file exists, the honest note at the end.
               Judgement about a mechanism, not a readout of it. A human or an agent owns it, and
               generating it would turn the page into a directory listing with a nice font.

So this rewrites numbers in place and never touches prose. What it does do for the written half is
refuse to stay quiet about it: a rules or skills file the page has no `data-wc` for is reported,
because that means something was added and nobody has said what it is for.

Numbers live in the HTML as `data-wc="<repo-relative path>"` on whatever element shows them; the
trailing figure in that element's text is what gets replaced. Aggregates live between
`<!-- GEN:name -->` markers.

Personal files under .agents/.local/ are never counted on the shared page. When that folder exists,
their rows go to .agents/.cache/map-local.js instead, which the page's Local section loads with a
<script src> — a page opened from disk may load a script beside it, but may not fetch() one.
It writes no date or timestamp: one would make two identical setups differ.

Usage:
    python3 .agents/core/skills/project-sync-profiles-and-skills/scripts/build_setup_map.py [--repo-root <path>] [--check]

--check exits 1 if the map would change or a file is undescribed (map-local.js out of date is
informational), and writes nothing.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

MAP = ".agents/SETUP-MAP.html"
LOCAL = ".agents/.local"
SIDECAR = ".agents/.cache/map-local.js"


def rule_paths(root: Path, kind: str) -> list[Path]:
    """Every rule of this kind that loads: the project's own, then each profile's, shared and local.

    A rule is no longer copied into `.agents/core/rules/` — it stays in the profile that brought it, and
    `LOADER.md` names it by path. This has to look in the same places that file does.
    """
    found = list((root / ".agents/core/rules" / kind).glob("*.md"))
    for base in (root / ".agents/profiles", root / ".agents/.local/profiles"):
        for profile in sorted(base.iterdir()) if base.is_dir() else []:
            found += list((profile / "rules" / kind).glob("*.md"))
    return sorted(p for p in found if ".seed." not in p.name)


def shared_skills(root: Path) -> list[Path]:
    """Installed skills, minus the links into .agents/.local/ — those are one person's, not the setup's."""
    local = (root / LOCAL).resolve()
    return [
        path for path in sorted((root / ".agents/skills").glob("*/SKILL.md"))
        if not path.resolve().is_relative_to(local)
        and not (path.parent / ".forwarding-stub").is_file()  # a stub stands in for a local skill's link
    ]


# Files whose counts the page shows. Order is only for the report.
def tracked(root: Path) -> dict[str, int]:
    paths: list[Path] = [root / "AGENTS.md", root / "CLAUDE.md", root / ".agents/CONSTITUTION.md",
                         root / ".agents/LOADER.md"]
    paths += rule_paths(root, "always-on")
    paths += rule_paths(root, "on-demand")
    # The generated spec files differ per machine and are kept out of git, so the shared page never counts them.
    paths += [p for p in sorted((root / ".specs").glob("*.md")) if p.name not in {"INDEX.md", "DECISIONS.md", "OPEN-QUESTIONS.md"}]
    paths += shared_skills(root)
    counts = {}
    for path in paths:
        if path.is_file():
            counts[path.relative_to(root).as_posix()] = len(path.read_text(encoding="utf-8").split())
    return counts


def aggregates(root: Path, counts: dict[str, int]) -> dict[str, str]:
    def total(prefix: str) -> int:
        return sum(n for p, n in counts.items() if p.startswith(prefix))

    always_files = ["AGENTS.md", "CLAUDE.md", ".agents/LOADER.md", ".agents/CONSTITUTION.md"]
    descriptions = sum(  # every shared skill's description is in context from the start
        len(m.group(1).split()) for p in shared_skills(root)
        if (m := re.search(r"^description:\s*(.*)$", p.read_text(encoding="utf-8"), re.M))
    )
    def kind_total(kind):  # rules live in profiles now, so sum the files, not a path prefix
        return sum(counts.get(str(r.relative_to(root)), 0) for r in rule_paths(root, kind))

    always = sum(counts.get(p, 0) for p in always_files) + kind_total("always-on") + descriptions
    on_demand = kind_total("on-demand") + total(".agents/skills/")

    n_always = len(rule_paths(root, "always-on"))
    n_on_demand = len(rule_paths(root, "on-demand"))
    n_agents = len(list((root / ".claude/agents").glob("*.md")))
    n_specs = len([
        p for p in (root / ".specs").rglob("*.md")
        if p.name not in {"INDEX.md", "DECISIONS.md", "OPEN-QUESTIONS.md", "README.md"}
        and "changes" not in p.relative_to(root / ".specs").parts  # a spec in an open change counts once it merges
    ])

    return {
        "always": f"{always:,}",
        "ondemand": f"{on_demand:,}",
        "rules": str(n_always + n_on_demand),
        "rules_split": f"{n_always} always-on, {n_on_demand} conditional",
        "skills": str(len(shared_skills(root))),
        "agents": str(n_agents),
        "specs": str(n_specs),
    }


def sidecar(root: Path) -> str | None:
    """The Local section's data, or None when there is no .agents/.local/ to describe."""
    base = root / LOCAL
    if not base.is_dir():
        return None
    files = []
    for load, pattern, note in (
        ("always", "rules/LOADER.md", "Your loader, read every session after the shared one."),
        ("always", "rules/always-on/*.md", "Personal rule, read every session."),
        ("on demand", "rules/on-demand/*.md", "Personal rule; a row in your LOADER.md says when."),
        ("invoked", "skills/*/SKILL.md", "Personal skill, linked so both tools see it; its description loads every session."),
    ):
        for path in sorted(base.glob(pattern)):
            files.append({
                "path": path.relative_to(root / ".agents").as_posix(),
                "load": load,
                "note": note,
                "words": len(path.read_text(encoding="utf-8").split()),
            })
    return ("// Generated by .agents/core/skills/project-sync-profiles-and-skills/scripts/build_setup_map.py for the map's Local section. Do not edit.\n"
            f"window.MAP_LOCAL = {json.dumps(files, indent=2)};\n")


ELEMENT = re.compile(r'(<(\w+)[^>]*\bdata-wc="([^"]+)"[^>]*>)([^<]*)(</\2>)')
TRAILING_NUMBER = re.compile(r"[\d,]+\s*$")


def rewrite(html: str, counts: dict[str, int], agg: dict[str, str]) -> tuple[str, list[str]]:
    described: set[str] = set()
    missing: list[str] = []

    def swap(match: re.Match[str]) -> str:
        open_tag, _, path, text, close_tag = match.groups()
        described.add(path)
        if path not in counts:
            missing.append(f"{path}: the map shows a count for a file that no longer exists")
            return match.group(0)
        if not TRAILING_NUMBER.search(text):
            missing.append(f"{path}: data-wc element has no trailing number to replace")
            return match.group(0)
        return open_tag + TRAILING_NUMBER.sub(f"{counts[path]:,}", text) + close_tag

    html = ELEMENT.sub(swap, html)

    for name, value in agg.items():
        marker = re.compile(
            rf"(<!-- GEN:{name} -->)(.*?)(<!-- /GEN:{name} -->)", re.DOTALL
        )
        if not marker.search(html):
            missing.append(f"GEN:{name}: marker pair not found in the map")
            continue
        html = marker.sub(lambda m: m.group(1) + value + m.group(3), html)

    # The half this script can't write: a rule or skill nobody has described yet.
    for path in counts:
        if path in described:
            continue
        if path.startswith((".agents/core/rules/", ".agents/skills/")):
            missing.append(
                f"{path}: exists but the map never mentions it — add a row and a `data-wc`, "
                f"and say what it is for"
            )

    return html, missing


def find_repo_root() -> Path:
    """The folder holding `.agents/`, found from this script's own location, so it runs from anywhere."""
    for parent in Path(__file__).resolve().parents:
        if (parent / ".agents").is_dir():
            return parent
    return Path.cwd()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=None)
    parser.add_argument("--check", action="store_true", help="exit 1 on drift, write nothing")
    args = parser.parse_args()

    root = (args.repo_root or find_repo_root()).resolve()
    target = root / MAP
    if not target.is_file():
        print(f"error: {MAP} not found", file=sys.stderr)
        return 2

    counts = tracked(root)
    original = target.read_text(encoding="utf-8")
    updated, missing = rewrite(original, counts, aggregates(root, counts))
    changed = updated != original

    local_js = sidecar(root)
    sidecar_path = root / SIDECAR
    local_changed = local_js is not None and (
        not sidecar_path.is_file() or sidecar_path.read_text(encoding="utf-8") != local_js
    )

    if args.check:
        if changed:
            print(f"{MAP} is out of date — run build_setup_map.py", file=sys.stderr)
        if local_changed:
            print(f"({SIDECAR} is out of date — run build_setup_map.py; informational)", file=sys.stderr)
        for item in missing:
            print(f"map: {item}", file=sys.stderr)
        return 1 if (changed or missing) else 0

    if changed:
        target.write_text(updated, encoding="utf-8")
    if local_changed:
        sidecar_path.parent.mkdir(parents=True, exist_ok=True)
        sidecar_path.write_text(local_js, encoding="utf-8")
    print(f"{'updated' if changed else 'no change to'} {MAP} — {len(counts)} file(s) measured")
    if local_js is not None:
        print(f"{'updated' if local_changed else 'no change to'} {SIDECAR}")
    if missing:
        print(f"\n{len(missing)} thing(s) the script can't fix, because they need prose:")
        for item in missing:
            print(f"  - {item}")
        print(f"\nRows to write in the map: {MAP}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
