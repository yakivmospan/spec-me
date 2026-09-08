#!/usr/bin/env python3
"""Build the two snapshots this experiment compares.

  original   the setup exactly as it is now: on-demand rules, reached through LOADER.md rows
  intest     the same setup with every on-demand rule converted into a skill, LOADER's on-demand
             table empty, and nothing else touched

Both are real trees, not descriptions of trees, so either can be handed to a real agent CLI later
without redoing anything. Snapshots are throwaway: they go outside the repository by default.

    python3 prepare.py                          # generated descriptions: the variant's floor
    python3 prepare.py --descriptions descriptions.toml   # hand-written: the variant at its best
    python3 prepare.py --out /tmp/rules-vs-skills

It prints both paths and what each costs in always-on words, which is the one number the comparison
does not need an agent to measure.
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
COPIED = [".agents", ".claude", ".codex", ".specs", "AGENTS.md", "CLAUDE.md"]


def copy_tree(dest: Path):
    dest.mkdir(parents=True, exist_ok=True)
    for item in COPIED:
        src = REPO / item
        if not src.exists():
            continue
        target = dest / item
        if src.is_dir():
            shutil.copytree(src, target, symlinks=True)
        else:
            shutil.copy2(src, target)
    subprocess.run(["git", "init", "-q"], cwd=dest, check=True)
    subprocess.run(["git", "add", "-A"], cwd=dest, capture_output=True)
    subprocess.run(["git", "-c", "user.email=t@t", "-c", "user.name=t",
                    "commit", "-qm", "snapshot"], cwd=dest, capture_output=True)
    return dest


def always_on_words(root: Path):
    """What this variant costs before any request: always-on rules plus every skill description.

    Both halves matter here and they move in opposite directions, which is the whole point. Turning
    a rule into a skill does not change the body's cost, because both load lazily. It does move the
    trigger text from one table read once into a description carried for the whole session.
    """
    rules = 0
    for f in root.glob(".agents/**/rules/always-on/*.md"):
        rules += len(f.read_text(encoding="utf-8", errors="replace").split())
    descs = 0
    count = 0
    for f in root.glob(".agents/skills/*/SKILL.md"):
        text = f.read_text(encoding="utf-8", errors="replace")
        m = re.search(r"^description:\s*(.*(?:\n  .*)*)", text, re.M)
        if m:
            descs += len(m.group(1).split())
            count += 1
    loader = 0
    for name in (".agents/LOADER.md", ".agents/.local/LOADER.md"):
        f = root / name
        if f.is_file():
            loader += len(f.read_text(encoding="utf-8", errors="replace").split())
    return {"always_on_rules": rules, "skill_descriptions": descs, "skills": count,
            "loaders": loader, "total": rules + descs + loader}


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default=None, help="where the snapshots go")
    ap.add_argument("--descriptions", help="hand-written descriptions for the converted skills")
    args = ap.parse_args()

    out = Path(args.out).resolve() if args.out else Path("/tmp/rules-vs-skills").resolve()
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    original = copy_tree(out / "original")
    intest = copy_tree(out / "intest")

    cmd = [sys.executable, str(HERE / "skillify.py"), "--repo-root", str(intest)]
    if args.descriptions:
        d = Path(args.descriptions)
        cmd += ["--descriptions", str(d if d.is_absolute() else HERE / d)]
    done = subprocess.run(cmd, capture_output=True, text=True)
    print(done.stdout or done.stderr)
    if done.returncode != 0:
        sys.exit("skillify failed")

    manifest = {
        "when": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "descriptions": "hand-written" if args.descriptions else "generated",
        "original": str(original), "intest": str(intest),
        "cost": {"original": always_on_words(original), "intest": always_on_words(intest)},
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")

    a, b = manifest["cost"]["original"], manifest["cost"]["intest"]
    print(f"original  {original}")
    print(f"intest    {intest}   ({manifest['descriptions']} descriptions)")
    print("\nalways-on cost, in words, before any request is made:")
    print(f"{'':<22}{'original':>10}{'intest':>10}{'change':>10}")
    for key in ("always_on_rules", "skill_descriptions", "loaders", "total"):
        print(f"  {key:<20}{a[key]:>10}{b[key]:>10}{b[key] - a[key]:>+10}")
    print(f"  {'skills listed':<20}{a['skills']:>10}{b['skills']:>10}{b['skills'] - a['skills']:>+10}")
    print(f"\nmanifest written to {out / 'manifest.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
