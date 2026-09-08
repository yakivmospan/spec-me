#!/usr/bin/env python3
"""Is this setup working? One answer, in the terms you would ask the question.

Runs everything there is to run and reports what it means, not what it ran. Nothing here is new
checking — it is the checks that already exist, asked as the questions a person actually has:
will my rules load, is anything broken, did something change that I did not change, does the
profile I just dropped in fit, and are the numbers moving the right way.

Usage: python3 health.py [--repo-root PATH]
Exit code is 0 when nothing needs you, 1 when something does.
"""
import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def repo_root(override):
    if override:
        return Path(override).resolve()
    out = subprocess.run(["git", "-C", str(HERE), "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True)
    return Path(out.stdout.strip()) if out.stdout.strip() else HERE.parents[2]


def plural(n, one, many=None):
    return f"{n} {one}" if n == 1 else f"{n} {many or one + 's'}"


def run(argv, cwd):
    try:
        got = subprocess.run(argv, cwd=cwd, capture_output=True, text=True, timeout=600)
        return got.returncode, got.stdout + got.stderr
    except (OSError, subprocess.TimeoutExpired) as exc:
        return 1, f"could not run: {exc}"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--repo-root")
    args = ap.parse_args()
    root = repo_root(args.repo_root)
    sys.path.insert(0, str(root / ".agents/core/skills/project-test-setup/scripts"))
    import validate_inventory as V

    needs_you, lines = [], []
    say = lines.append
    step = (lambda what: print(f"  … {what}", file=sys.stderr, flush=True))

    # --- will it load -----------------------------------------------------------------------------
    step("reading what loads")
    always = V.rule_paths(str(root), "always-on")
    on_demand = V.rule_paths(str(root), "on-demand")
    skills = V.skills(str(root))
    shared_words = sum(len(V.read(f).split()) for f in always if "/.local/" not in f)
    local_words = sum(len(V.read(f).split()) for f in always if "/.local/" in f)
    for f in ("AGENTS.md", "CLAUDE.md", ".agents/CONSTITUTION.md", ".agents/LOADER.md"):
        shared_words += len(V.read(os.path.join(str(root), f)).split())
    shared_words += sum(d for _, local, d, _ in skills if not local)
    say("## Will it all load?\n")
    say(f"Every session reads the constitution, **{len(always)} always-on rule(s)** and "
        f"**{len(skills)} skill description(s)**, then picks from **{len(on_demand)} on-demand "
        f"rule(s)** by what you are doing.")
    say(f"That costs **{shared_words:,} words** of the window before your task, plus "
        f"**{local_words:,}** for rules only you have." if local_words else
        f"That costs **{shared_words:,} words** of the window before your task.")
    unplaced = V.rule_paths(str(root), "unplaced")
    if unplaced:
        needs_you.append(f"{len(unplaced)} rule(s) no loader line names, so they never load: "
                         + ", ".join(f"`{os.path.basename(f)}`" for f in unplaced))

    # --- is anything broken -----------------------------------------------------------------------
    say("\n## Is anything broken?\n")
    step("checking every link resolves")
    code, sync_out = run([sys.executable, ".agents/core/skills/project-sync-profiles-and-skills/scripts/"
                          "sync.py", "--check"], root)
    broken = [n for d in (".agents/skills", ".claude/skills", ".claude/agents", ".codex/agents")
              for n in ((root / d).iterdir() if (root / d).is_dir() else []) if not n.exists()]
    conflicts = "name(s) in conflict" in sync_out
    dangling = [l for l in sync_out.splitlines() if l.startswith("pruned") and "LOADER.md named" in l]
    seeds = [l for l in sync_out.splitlines() if l.startswith("seed")]
    for line in sync_out.splitlines():
        if line.startswith("warn") and ("needs" in line or "not installed" in line):
            needs_you.append(line.replace("warn", "", 1).strip())
    if broken:
        needs_you.append(f"{len(broken)} link(s) point at nothing: "
                         + ", ".join(f"`{b.name}`" for b in broken[:4]))
    if conflicts:
        needs_you.append("two things want the same name — run the sync to see which, and what the "
                         "ways out cost")
    for d in dangling:
        needs_you.append("a loader line names a file that is gone — run the sync to drop it: "
                         + d.split(" named ", 1)[1].split(",")[0].strip())
    say("- Every skill and agent resolves for both tools." if not broken
        else f"- **{len(broken)} link(s) resolve to nothing.**")
    say("- No two things are fighting over a name." if not conflicts
        else "- **Two things want the same name.**")
    say("- Nothing is loaded from a file that is missing." if not dangling
        else f"- **{plural(len(dangling), 'rule')} named but absent.**")
    step("checking the map still matches the tree")
    code, map_out = run([sys.executable, ".agents/core/skills/project-sync-profiles-and-skills/scripts/"
                         "build_setup_map.py", "--check"], root)
    stale = [l for l in map_out.splitlines() if l.startswith("map:")]
    say("- The setup map still matches what is on disk." if not stale
        else f"- **The map is {plural(len(stale), 'count')} out of date.**")
    for l in stale:
        needs_you.append(l.replace("map:", "the map is stale —", 1).strip()
                         + " Run the sync to rebuild it.")
    if seeds:
        needs_you.append(f"{len(seeds)} form(s) arrived with a profile and still need answering")

    # --- did anything change that you did not change ----------------------------------------------
    say("\n## Did anything change that you did not?\n")
    step("running the engine's own suite (this is the slow part)")
    code, mech = run([sys.executable, ".agents/builder/tests/stress_profile_sync.py"], root)
    passed = re.search(r"(\d+)/(\d+) cases passed", mech)
    if passed and passed.group(1) != passed.group(2):
        needs_you.append(f"the engine's own behaviour changed: {passed.group(0)}")
    say(f"- The engine still does what it is supposed to: **{passed.group(0)}**." if passed
        else "- The engine's own suite did not run.")
    out = []
    V.profile_files(str(root), out)
    differs = [l for l in out if l.startswith("- differs:")]
    same = next((l for l in out if l.startswith("- identical:")), "")
    say(f"- Your files match the builder they came from: **{same.split(': ')[-1]} identical**, "
        f"**{len(differs)} changed**.")
    for d in differs:
        needs_you.append("changed from the builder's version — yours, or drift: "
                         + d.split("`")[1].split(" ")[0])

    # --- do the profiles fit ----------------------------------------------------------------------
    say("\n## Do the profiles fit together?\n")
    step("checking the profiles fit")
    states = V.profile_state(str(root)) or []
    for s in states:
        if not s["present"]:
            say(f"- `{s['name']}` — not installed ({s['total']} files available).")
            continue
        missing = s["total"] - s["here"]
        gap = (f", **{missing} file(s) missing**" if missing and s["whole"]
               else f", {missing} part(s) you removed" if missing else "")
        say(f"- `{s['name']}` — in place at `{s['present']}`{gap}.")
        if missing and s["whole"]:
            needs_you.append(f"`{s['name']}` installs whole and {missing} file(s) are missing")
    for section, fn in (("a profile names the engine without saying it needs it",
                         V.profile_independence),
                        ("the engine names one profile by name", V.engine_independence),
                        ("a row sits in the wrong rule", V.misplaced_rows),
                        ("an engine rule is written for one stack", V.stack_content_in_core)):
        got = []
        fn(str(root), got)
        found = [g for g in got if g.startswith("- ") and not g.startswith("- none")
                 and "no builder" not in g and "no stack profile" not in g
                 and "no engine form" not in g]
        if found:
            # the files, not a count — a number tells you nothing you can act on
            named = []
            for line in found:
                bits = re.findall(r"`([^`]+)`", line)
                if bits:
                    named.append(os.path.basename(bits[0].rstrip(":0123456789")))
            names = sorted(set(named))
            needs_you.append(f"{section}: " + ", ".join(f"`{n}`" for n in names[:4])
                             + (f" and {len(names) - 4} more" if len(names) > 4 else ""))

    # --- the numbers -------------------------------------------------------------------------------
    say("\n## The numbers\n")
    score = V.score_table(V.read(os.path.join(str(root), V.LEDGER)))
    overall = next((r for r in score if "Overall" in r), "")
    say(f"- Setup quality, from your own findings ledger: **{overall.split('**')[-2]}** out of 10."
        if "**" in overall else "- No findings ledger yet.")
    runs = sorted(list((root / ".agents/core/tests/behaviour/results").glob("*.json"))
                  + list((root / ".agents/.local/tests/behaviour").glob("*.json")),
                  key=lambda p: p.stat().st_mtime)
    runs = [r for r in runs if "dry" not in r.name]
    if runs:
        latest = json.loads(runs[-1].read_text())
        best = latest["runs"][-1]["overall"]
        say(f"- Agents actually following the setup: **{best:.0%}** "
            f"({latest['when'][:10]}, {len(latest['runs'][-1]['cases'])} cases).")
        if len(runs) > 1:
            prev = json.loads(runs[-2].read_text())["runs"][-1]["overall"]
            move = "the same as" if abs(best - prev) < 0.005 else (
                "better than" if best > prev else "**worse than**")
            say(f"- That is {move} the run before it ({prev:.0%}).")
            if best < prev:
                needs_you.append(f"agents follow the setup less well than last time "
                                 f"({prev:.0%} → {best:.0%})")
    else:
        say("- No agent has been scored against this setup yet.")

    print("# Your setup, right now\n")
    print("**Everything holds.**\n" if not needs_you
          else f"**{plural(len(needs_you), 'thing needs', 'things need')} you.**\n")
    print("\n".join(lines))
    if needs_you:
        print("\n## What needs you\n")
        for i, n in enumerate(needs_you, 1):
            print(f"{i}. {n}")
    return 1 if needs_you else 0


sys.exit(main())
