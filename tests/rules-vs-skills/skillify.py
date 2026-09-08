#!/usr/bin/env python3
"""Turn every on-demand rule in one copy of the setup into a skill.

The proposal this tests: on-demand rules are a contraption, and a rule's `load-when:` is really a skill
description wearing a hat. If that is true, converting them should cost nothing — the same guidance
reaches the agent at the same moment, through one mechanism instead of two.

So convert them, honestly, and measure. For each on-demand rule this:

  * reads its `load-when:` and its body,
  * writes a skill next door whose description is built from that `load-when:`,
  * deletes the rule,
  * runs the real sync, so `LOADER.md` rebuilds with an empty on-demand table.

Nothing here is reversible in place: run it against a snapshot, never the repository you work in.
It refuses to run anywhere that looks like a working tree with uncommitted changes.

    python3 skillify.py --repo-root <a snapshot>
    python3 skillify.py --repo-root <a snapshot> --dry-run

The description is generated, not hand-written, and that is the fairest reading of the proposal:
"their when == skill description". It is also the test's main weakness, and the README says so — a
person writing these by hand would do better, so a loss here is a floor on the variant, not a
verdict on it.
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

RULE_GLOBS = (
    ".agents/core/rules/on-demand/*.md",
    ".agents/profiles/*/rules/on-demand/*.md",
    ".agents/.local/profiles/*/rules/on-demand/*.md",
)

# A description is capped the same way a hand-written one is, so the variant is not handed an
# advantage the budget would never allow.
MAX_WORDS = 100


def frontmatter(text):
    """The frontmatter dict and the body, for a file that starts with a `---` block."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    head, body = text[3:end], text[end + 4:]
    meta = {}
    for line in head.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    return meta, body.lstrip("\n")


def summarise(body):
    """The rule's title and its first sentence with any substance, for the 'what it does' half.

    A one-word opener like "Always-on." or "Stack-agnostic." says nothing to someone deciding
    whether to load the file, so keep looking until a sentence carries some weight. Handing the
    variant a useless description would rig the result.
    """
    title, first = "", ""
    for line in body.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("# ") and not title:
            title = line[2:].strip()
            continue
        if not title or line.startswith(("#", "|", "-", ">", "```", "*")):
            continue
        for sentence in re.split(r"(?<=[.!?])\s+", line):
            if len(sentence.split()) >= 6:
                first = sentence.strip()
                break
        if first:
            break
    return title, first


def describe(when, title, first):
    """Build a skill description out of the rule's own `load-when:` and its opening.

    Triggers first, then what it does — the order this setup's own skill rules ask for.
    """
    when = when.strip().rstrip(".")
    lead = f"Use before you {when}." if when else "Use for this project's conventions."
    what = first or f"{title}."
    what = re.sub(r"\s+", " ", what).strip()
    words = (lead + " " + what).split()
    if len(words) > MAX_WORDS:
        words = words[:MAX_WORDS]
        text = " ".join(words).rstrip(",;:") + "."
    else:
        text = lead + " " + what
    return re.sub(r"\s+", " ", text).strip()


def skill_home(rule: Path, root: Path):
    """Where the skill goes: the `skills/` folder beside the `rules/` the rule came from."""
    rel = rule.relative_to(root)
    parts = list(rel.parts)
    i = parts.index("rules")
    name = rule.stem[:-6] if rule.stem.endswith("-rules") else rule.stem
    return root.joinpath(*parts[:i], "skills", name, "SKILL.md"), name


def overrides(path: Path):
    """Hand-written descriptions, so the variant can be measured at its best as well as its floor.

    A generated description is the honest floor of "their when == skill description". It is not the
    ceiling: a person would write better ones, and a proposal deserves to be judged at its best. Put
    one `name = "description"` line per skill in a file and pass `--descriptions <file>`; anything
    not named there stays generated.
    """
    if not path:
        return {}
    text = Path(path).read_text(encoding="utf-8")
    out = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        out[k.strip()] = v.strip().strip('"')
    return out


def convert(root: Path, dry=False, hand=None):
    found = []
    for pattern in RULE_GLOBS:
        found.extend(sorted(root.glob(pattern)))
    if not found:
        print("no on-demand rules found — nothing to convert")
        return []
    hand = hand or {}
    done = []
    for rule in found:
        meta, body = frontmatter(rule.read_text(encoding="utf-8"))
        when = meta.get("load-when", "")
        title, first = summarise(body)
        _, name_preview = skill_home(rule, root)
        desc = hand.get(name_preview) or describe(when, title, first)
        target, name = skill_home(rule, root)
        done.append({"rule": str(rule.relative_to(root)), "skill": str(target.relative_to(root)),
                     "name": name, "when": when, "description": desc,
                     "hand_written": name in hand,
                     "words": len(desc.split()), "body_words": len(body.split())})
        if dry:
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(f"---\nname: {name}\ndescription: {desc}\n---\n\n{body}",
                          encoding="utf-8")
        rule.unlink()
    return done


def resync(root: Path):
    sync = root / ".agents/core/skills/project-sync-profiles-and-skills/scripts/sync.py"
    if not sync.is_file():
        print("warning: no sync.py in this copy — LOADER.md was not rebuilt")
        return
    out = subprocess.run([sys.executable, str(sync), "--repo-root", str(root)],
                         capture_output=True, text=True)
    print((out.stdout or out.stderr).strip())


def guard(root: Path):
    """Refuse a repository someone is working in. This deletes rule files."""
    if not (root / ".agents").is_dir():
        sys.exit(f"error: no .agents/ under {root}")
    dirty = subprocess.run(["git", "status", "--porcelain"], cwd=root,
                           capture_output=True, text=True)
    if dirty.returncode == 0 and dirty.stdout.strip():
        sys.exit(f"error: {root} has uncommitted changes. Run this against a snapshot, never a "
                 f"tree you work in.")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--repo-root", required=True, help="the snapshot to convert, in place")
    ap.add_argument("--dry-run", action="store_true", help="print what would change, touch nothing")
    ap.add_argument("--force", action="store_true", help="skip the uncommitted-changes guard")
    ap.add_argument("--descriptions", help="hand-written descriptions, to measure the variant at "
                                           "its best instead of its generated floor")
    args = ap.parse_args()

    root = Path(args.repo_root).resolve()
    if not args.force and not args.dry_run:
        guard(root)

    done = convert(root, dry=args.dry_run, hand=overrides(args.descriptions))
    for d in done:
        mark = "hand-written" if d["hand_written"] else "generated"
        print(f"{d['rule']}\n  -> {d['skill']}  ({d['body_words']} body words)")
        print(f"     description ({d['words']} words, {mark}): {d['description']}")
    if not args.dry_run and done:
        resync(root)
    print(f"\n{len(done)} on-demand rule(s) "
          f"{'would be' if args.dry_run else 'were'} converted to skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
