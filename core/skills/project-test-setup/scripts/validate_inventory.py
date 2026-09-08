#!/usr/bin/env python3
"""The mechanical half of project-test-setup, so every run starts from the same facts.

Prints markdown: the score from the findings ledger, word counts against the budgets, the load numbers with every term, builder profile
files against their installed files, retired names still mentioned, paths named in prose that don't
exist, skill links, and the map check. Every list is sorted, so two runs on one tree print the same.
Hits are leads for the reader to open, not verdicts.

Usage: python3 validate_inventory.py [--repo-root PATH] [--write-score]
"""
import argparse
import filecmp
import math
import os
import re
import subprocess
import sys

# A profile raises one of its own files' limit on its PROFILE.md's `**Word budget:**` line.
ALWAYS_ON_WORDS, ON_DEMAND_WORDS = 300, 1000
DESCRIPTION_MIN, DESCRIPTION_MAX, BODY_MAX = 70, 100, 1500
# The shared loader is committed; the local one names what only its owner has.
LOADERS = (".agents/LOADER.md", ".agents/.local/LOADER.md")
LOADER_PATH = re.compile(r"`(\.agents/[^`\s]+\.md)`")
TEXT_SUFFIXES = (".md", ".toml", ".json", ".py", ".sh", ".ps1", ".gitignore")
SKIPPED = ("/.local/backups/", "/.cache/", "SETUP-MAP", "/__pycache__/", "/map/",
           "/builder/profiles/",  # a profile file naming its own destination is not a missing path
           "/builder/tests/",  # the suite names paths that exist only inside its throwaway repos
           "/tests/behaviour/")  # its cases name planted files, and its results are records, not prose
HISTORY_FILES = ("BUILDER-DESIGN.md", "CHANGELOG.md")
AREAS = ["Constitution", "Consistency", "Load", "Simplification", "Leftovers"]
COST = {"Critical": 3, "High": 2, "Medium": 1, "Low": 0.25}


def repo_root(override):
    if override:
        return os.path.abspath(override)
    here = os.path.dirname(os.path.realpath(__file__))
    out = subprocess.run(["git", "-C", here, "rev-parse", "--show-toplevel"], capture_output=True, text=True)
    return out.stdout.strip() or os.getcwd()


def read(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as file:
            return file.read()
    except OSError:
        return ""


def words(text):
    return len(text.split())


def split_skill(text):
    match = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
    if not match:
        return "", text
    front, body = match.groups()
    desc = re.search(r"^description:\s*(>-?|\|)?\s*(.*?)(?=^\w[\w-]*:|\Z)", front, re.S | re.M)
    return (desc.group(2) if desc else ""), body


def skills(root):
    """(name, is_local, description words, body words), sorted by name."""
    folder = os.path.join(root, ".agents", "skills")
    out = []
    for name in sorted(os.listdir(folder)) if os.path.isdir(folder) else []:
        path = os.path.join(folder, name, "SKILL.md")
        if not os.path.isfile(path):
            continue
        is_local = "/.local/" in os.path.realpath(os.path.join(folder, name)) + "/"
        desc, body = split_skill(read(path))
        out.append((name, is_local, words(desc), words(body)))
    return out


def md_files(folder):
    return sorted(f for f in os.listdir(folder) if f.endswith(".md")) if os.path.isdir(folder) else []


def loader_placements(root):
    """Where the two loaders place rules: the always-on paths, and each table row as (step, paths).

    The loaders are the project's own files, and a line naming a rule's path is what places it.
    """
    always, rows = set(), []
    for rel in LOADERS:
        in_always = False
        for line in read(os.path.join(root, rel)).splitlines():
            if line.strip() in ("<!-- always-on -->", "<!-- /always-on -->"):
                in_always = line.strip() == "<!-- always-on -->"
                continue
            paths = LOADER_PATH.findall(line)
            if in_always:
                always.update(paths)
            elif paths and line.lstrip().startswith("|"):
                step = line.strip().strip("|").split("|")[0].strip().lower()
                rows.append((step, set(paths)))
    return always, rows


def rule_kind(root, path, placements):
    """When a rule loads, by the loaders: `always-on`, `on-demand`, or `unplaced` when no line names it."""
    rel = os.path.relpath(path, root).replace(os.sep, "/")
    always, rows = placements
    if rel in always:
        return "always-on"
    return "on-demand" if any(rel in paths for _, paths in rows) else "unplaced"


def rule_paths(root, kind, scope="all"):
    """Every rule of this kind, wherever it sits.

    The kind comes from the loaders — listed always-on, named in a table row, or neither, so it never
    loads. Both folders are walked either way, so a rule filed in the wrong one is still counted
    where it actually loads.
    """
    placements = loader_placements(root)
    found = []
    for folder_kind in ("always-on", "on-demand"):
        core = os.path.join(root, ".agents/core/rules", folder_kind)
        here = [] if scope == "local" else [os.path.join(core, f) for f in md_files(core)]
        bases = {"all": (".agents/profiles", ".agents/.local/profiles"),
                 "shared": (".agents/profiles",), "local": (".agents/.local/profiles",)}[scope]
        for base in bases:
            folder = os.path.join(root, base)
            for name in sorted(os.listdir(folder)) if os.path.isdir(folder) else []:
                sub = os.path.join(folder, name, "rules", folder_kind)
                here += [os.path.join(sub, f) for f in md_files(sub)]
        found += [f for f in here if rule_kind(root, f, placements) == kind]
    return [f for f in sorted(found) if ".seed." not in os.path.basename(f)]


def load_numbers(root, skill_rows, out):
    terms = [(p, words(read(os.path.join(root, p))))
             for p in ("AGENTS.md", "CLAUDE.md", ".agents/CONSTITUTION.md", ".agents/LOADER.md")]
    terms += [(os.path.relpath(f, root), words(read(f))) for f in rule_paths(root, "always-on", "shared")]
    descriptions = sum(d for _, local, d, _ in skill_rows if not local)
    session = sum(n for _, n in terms) + descriptions
    out.append("### Every session (shared): %d" % session)
    out += [f"- `{p}` {n}" for p, n in terms]
    out.append(f"- shared skill descriptions {descriptions}")

    local_terms = [(os.path.relpath(f, root), words(read(f)))
                   for f in rule_paths(root, "always-on", "local")]
    local_descriptions = sum(d for _, is_local, d, _ in skill_rows if is_local)
    out.append("\n### Local layer, every session: %d" % (sum(n for _, n in local_terms) + local_descriptions))
    out += [f"- `{p}` {n}" for p, n in local_terms] + [f"- local skill descriptions {local_descriptions}"]

    unplaced = rule_paths(root, "unplaced")
    if unplaced:
        out.append("\n### Unplaced, so never loaded")
        out += [f"- `{os.path.relpath(f, root)}` — no loader line names it" for f in unplaced]


def word_budgets(root):
    """Per-file word limits the installed profiles raise, from each `PROFILE.md`'s `**Word budget:**` line."""
    cards = [os.path.join(root, ".agents", "core", "PROFILE.md")]
    for base in (".agents/profiles", ".agents/.local/profiles"):
        folder = os.path.join(root, base)
        cards += [os.path.join(folder, n, "PROFILE.md") for n in sorted(os.listdir(folder))] if os.path.isdir(folder) else []
    limits = {}
    for card in cards:
        for line in read(card).splitlines():
            if line.lstrip("- ").startswith("**Word budget:**"):
                for name, n in re.findall(r"`([^`]+)`\s+([\d,]+)", line):
                    limits[name] = int(n.replace(",", ""))
    return limits


def budgets(root, skill_rows, out):
    flags, raised = [], word_budgets(root)
    for kind, limit in (("always-on", ALWAYS_ON_WORDS), ("on-demand", ON_DEMAND_WORDS)):
        for path in rule_paths(root, kind):
            name, n = os.path.basename(path), words(read(path))
            cap = raised.get(name, limit)
            if n > cap:
                flags.append(f"- {kind} rule `{os.path.relpath(path, root)}`: {n} words, over {cap}")
    for name, is_local, desc, body in skill_rows:
        where = "local" if is_local else "shared"
        if not DESCRIPTION_MIN <= desc <= DESCRIPTION_MAX:
            flags.append(f"- skill `{name}` ({where}): description {desc} words, outside {DESCRIPTION_MIN}–{DESCRIPTION_MAX}")
        if body > BODY_MAX:
            flags.append(f"- skill `{name}` ({where}): body {body} words, over {BODY_MAX}")
    out.append("## Budgets\n")
    out += flags or ["- nothing over budget"]
    out.append("\n| Skill | Where | Description | Body |\n|---|---|---|---|")
    out += [f"| {n} | {'local' if l else 'shared'} | {d} | {b} |" for n, l, d, b in skill_rows]


# The engine's files are placed at fixed paths, because they are the files both tools read first and
# forms about this repository. Everything under `profiles/` is a folder dropped in whole instead.
CORE_DESTINATIONS = {
    "CLAUDE.md": "CLAUDE.md",
    "AGENTS.seed.md": "AGENTS.md",
    "CONSTITUTION.seed.md": ".agents/CONSTITUTION.md",
    "README.seed.md": ".agents/README.md",
    "settings/claude-settings.seed.json": ".claude/settings.json",
    "settings/codex-config.toml": ".codex/config.toml",
    "settings/agents.gitignore": ".agents/.gitignore",
    "settings/claude.gitignore": ".claude/.gitignore",
    "map/SETUP-MAP.seed.html": ".agents/SETUP-MAP.html",
}
# What a profile carries that does not stay inside its own folder.
PROFILE_DESTINATIONS = {
    "specs/specs/README.md": ".specs/README.md",
    "specs/specs/.gitignore": ".specs/.gitignore",
}


def core_destination(rel):
    """Where a file under `builder/core/` installs. None when nothing installs it."""
    if ".builder." in os.path.basename(rel):
        return None
    if rel in CORE_DESTINATIONS:
        return [CORE_DESTINATIONS[rel]]
    if rel.split("/")[0] in ("skills", "rules", "agents", "tests"):
        # A core form is answered in place, with the marker dropped: the questions it asks are
        # about this repository, and core is what owns that folder.
        return [".agents/core/" + rel.replace(".seed.", ".")]
    return None


def profile_destination(rel):
    """Where a file under `builder/profiles/` installs.

    A profile is dropped in whole, so almost everything lands at the same path inside
    `.agents/profiles/<name>/` — or under `.agents/.local/profiles/` when it is the user's alone.
    A `.seed.` file is the exception: it is a form about this repository, so it is answered into
    the engine's own rules folder rather than left in the profile.
    """
    name, _, tail = rel.partition("/")
    if not tail or ".builder." in os.path.basename(tail):
        return None
    if rel in PROFILE_DESTINATIONS:
        return [PROFILE_DESTINATIONS[rel]]
    if ".seed." in os.path.basename(tail):
        # Answered where it sits. A profile never writes into `.agents/core/rules/`: one folder has
        # one writer, and a profile that seeded into core could leave a rule behind when its folder
        # was deleted — the one hole in "delete it and it is gone".
        tail = tail.replace(".seed.", ".")
    return [f".agents/profiles/{name}/{tail}", f".agents/.local/profiles/{name}/{tail}"]


def comparable(rel, destination_of):
    """Where a file's content can be compared with what it installed.

    [] for a form or a builder-only file — a form differs from its answer by design, and a
    `.builder.` file is never installed. None when nothing maps it.
    """
    if ".seed." in os.path.basename(rel) or ".builder." in os.path.basename(rel):
        return []
    return destination_of(rel)


def walk_builder(root, kind):
    """Every file under `builder/<kind>/`, as (path relative to that folder, full path)."""
    base = os.path.join(root, ".agents", "builder", kind)
    if not os.path.isdir(base):
        return None
    out = []
    for dirpath, _, files in os.walk(base):
        for f in sorted(files):
            rel = os.path.relpath(os.path.join(dirpath, f), base)
            if "__pycache__" not in rel and not f.startswith("."):
                out.append((rel.replace(os.sep, "/"), os.path.join(dirpath, f)))
            elif f.startswith(".") and "__pycache__" not in rel:
                out.append((rel.replace(os.sep, "/"), os.path.join(dirpath, f)))
    return sorted(out)


def profile_files(root, out):
    """What the builder holds against what is installed, for the engine and for each profile."""
    out.append("## Builder files against installed files\n")
    core = walk_builder(root, "core")
    if core is None:
        out.append("- no builder here")
        return
    same, differ, missing, unmapped = 0, [], [], []
    absent = {s["name"] for s in (profile_state(root) or []) if not s["present"]}
    groups = [("core/", core, core_destination)]
    profiles_here = walk_builder(root, "profiles")
    if profiles_here is not None:
        groups.append(("profiles/", profiles_here, profile_destination))
    for prefix, rows, destination_of in groups:
        for rel, full in rows:
            targets = comparable(rel, destination_of)
            if targets == []:
                continue
            if targets is None:
                unmapped.append(prefix + rel)
                continue
            if prefix == "profiles/" and rel.split("/")[0] in absent:
                continue  # the whole profile was never dropped in; one line below says so
            found = next((t for t in targets if os.path.exists(os.path.join(root, t))), None)
            if not found:
                missing.append(prefix + rel)
            elif filecmp.cmp(full, os.path.join(root, found), shallow=False):
                same += 1
            else:
                differ.append(f"{prefix}{rel} \u2192 {found}")
    out.append(f"- identical: {same}")
    out += [f"- differs: `{d}`" for d in sorted(differ)]
    out += [f"- `{name}` is not dropped in, so none of its files are here" for name in sorted(absent)]
    out += [f"- no installed file: `{m}`" for m in sorted(missing)]
    out += [f"- not mapped by this script, compare by hand: `{u}`" for u in sorted(unmapped)]
    out.append("")
    out.append("A file that differs is either the project's own edit or drift from this builder's"
               " version. This check cannot tell those apart — open it and decide.")


def setup_files(root):
    paths = ["AGENTS.md", "CLAUDE.md", ".specs/README.md"]
    for top in (".agents", ".claude/agents", ".codex"):
        for dirpath, _, files in os.walk(os.path.join(root, top), followlinks=True):
            for f in files:
                full = os.path.join(dirpath, f)
                rel = os.path.relpath(full, root)
                if f.endswith(TEXT_SUFFIXES) and not any(s in "/" + rel for s in SKIPPED):
                    paths.append(rel)
    seen, unique = set(), []
    for p in sorted(set(paths)):
        real = os.path.realpath(os.path.join(root, p))
        if os.path.isfile(real) and real not in seen:
            seen.add(real)
            unique.append(p)
    return unique


def retired_names(root, files, out):
    builder = os.path.join(root, ".agents", "builder")
    names = set()
    for f in HISTORY_FILES:
        for line in read(os.path.join(builder, f)).splitlines():
            if "Instead of" in line or "Replaced" in line or "named `" in line:
                names.update(re.findall(r"`([a-z][a-z0-9-]*(?:-rules\.md|\.md|-[a-z0-9-]+))`", line))
    existing = set()
    for p in files:
        existing.add(os.path.basename(p))
        existing.update(p.split("/"))
    # A name the builder still ships is not retired — it belongs to a profile this project has not
    # installed. Without this, every uninstalled profile's files read as retired, which is exactly
    # backwards on the one run where an uninstalled profile is the subject.
    profiles_dir = os.path.join(builder, "profiles")
    for dirpath, dirnames, filenames in os.walk(profiles_dir):
        existing.update(filenames)
        existing.update(dirnames)
        existing.update(f.replace(".seed.", ".") for f in filenames)
    retired = sorted(n for n in names if n not in existing)
    hits = []
    for name in retired:
        pattern = re.compile(rf"(?<![\w.-]){re.escape(name)}(?![\w-])")
        for p in files:
            if os.path.basename(p) in HISTORY_FILES:
                continue
            for number, line in enumerate(read(os.path.join(root, p)).splitlines(), 1):
                if pattern.search(line):
                    hits.append(f"- `{name}` — {p}:{number}")
    out.append("## Retired names still mentioned\n")
    out.append(f"Names checked ({len(retired)}): " + (", ".join(f"`{n}`" for n in retired) or "none"))
    out += hits or ["- none"]


def missing_paths(root, files, out):
    token = re.compile(r"`([.\w][\w./-]*/[\w.-]+)`")
    leads = []
    for p in files:
        if os.path.basename(p) in HISTORY_FILES:
            continue
        here = os.path.dirname(p)
        skill_dir = re.match(r"(.*?/skills/[^/]+)/", p + "/")
        bases = ["", ".agents", ".agents/builder", ".agents/builder/profiles", ".specs", here] + ([skill_dir.group(1)] if skill_dir else [])
        for number, line in enumerate(read(os.path.join(root, p)).splitlines(), 1):
            for t in token.findall(line):
                if any(c in t for c in "*{}<>") or t.startswith(("http", "~", "/")):
                    continue
                if not any(os.path.exists(os.path.join(root, b, t.rstrip("/"))) for b in bases):
                    leads.append(f"- `{t}` — {p}:{number}")
    out.append("## Paths named that don't exist (leads: examples and history are fine)\n")
    out += leads or ["- none"]


def half_up(value, places=0):
    scale = 10 ** places
    return math.floor(value * scale + 0.5) / scale


LEDGER = os.path.join(".agents", ".local", "tests", "validate-findings.md")


def score_table(text):
    counts = {area: {} for area in AREAS}
    findings = text.split("## Findings", 1)[-1]
    for line in findings.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 6 or cells[1] not in counts or cells[2] not in COST:
            continue
        if cells[5] == "open":
            counts[cells[1]][cells[2]] = counts[cells[1]].get(cells[2], 0) + 1
    scores, rows = {}, ["| Area | Open | Score |", "|---|---|---|"]
    for area in AREAS:
        raw = 10 - sum(COST[p] * n for p, n in counts[area].items())
        scores[area] = max(1, int(half_up(raw)))
        open_list = ", ".join(f"{n} {p}" for p, n in sorted(counts[area].items(), key=lambda i: -COST[i[0]]))
        rows.append(f"| {area} | {open_list or 'none'} | {scores[area]} ({raw:g}) |")
    overall = (3 * scores["Constitution"] + sum(scores[a] for a in AREAS[1:])) / 7
    rows.append(f"| **Overall** | | **{half_up(overall, 1):.1f}** |")
    return rows


def ledger_score(root, out):
    path = os.path.join(root, LEDGER)
    out.append("## Score from the ledger\n")
    if not os.path.isfile(path):
        out.append("- no ledger yet: this run's findings count")
        return
    out += score_table(read(path))


def write_score(root):
    """Rewrites the ledger's *Score* section from its own findings, so the ledger shows the current state."""
    path = os.path.join(root, LEDGER)
    text = read(path)
    if "## Findings" not in text:
        sys.exit(f"{LEDGER} has no '## Findings' heading")
    head, findings = text.split("## Findings", 1)
    head = head.split("## Score", 1)[0].rstrip() + "\n\n"
    block = "## Score\n\nWritten by `validate_inventory.py --write-score` from the findings below.\n\n"
    block += "\n".join(score_table(text)) + "\n\n"
    with open(path, "w", encoding="utf-8") as f:
        f.write(head + block + "## Findings" + findings)


def links(root, out):
    agents, claude = os.path.join(root, ".agents", "skills"), os.path.join(root, ".claude", "skills")
    a = sorted(os.listdir(agents)) if os.path.isdir(agents) else []
    c = sorted(os.listdir(claude)) if os.path.isdir(claude) else []
    broken = sorted(n for n in c if not os.path.exists(os.path.join(claude, n)))
    out.append("## Skill links\n")
    out.append(f"- `.agents/skills/`: {len(a)}; `.claude/skills/`: {len(c)}")
    out += [f"- not linked for Claude: `{n}`" for n in a if n not in c]
    out += [f"- link for something gone: `{n}`" for n in c if n not in a]
    out += [f"- broken link: `{n}`" for n in broken]


def map_check(root, out):
    script = os.path.join(root, ".agents", "core", "skills", "project-sync-profiles-and-skills",
                          "scripts", "build_setup_map.py")
    out.append("## Map check\n")
    if not os.path.isfile(script):
        out.append("- no map script")
        return
    run = subprocess.run([sys.executable, script, "--check"], cwd=root, capture_output=True, text=True)
    text = (run.stdout + run.stderr).strip()
    out.append(f"- exit {run.returncode}" + (":\n```\n" + text + "\n```" if text else ", nothing reported"))


# Paths only this setup uses, which is what says it is installed here at all.
OUR_PATHS = (".agents/core/", ".agents/profiles/", ".agents/skills/", ".agents/.local/profiles/",
             ".agents/.local/skills/", ".agents/CONSTITUTION.md")


def dropped_in(root, name):
    """Where a profile's folder is, or None when it was never dropped in."""
    for base in (".agents/profiles", ".agents/.local/profiles"):
        if os.path.isdir(os.path.join(root, base, name)):
            return f"{base}/{name}"
    return None


def profile_state(root):
    """Per profile: what it carries, how much of it is there, what it needs, and where it landed."""
    base = os.path.join(root, ".agents", "builder", "profiles")
    if not os.path.isdir(base):
        return None
    states = []
    for name in sorted(os.listdir(base)):
        folder = os.path.join(base, name)
        if not os.path.isdir(folder):
            continue
        total, here, rows = 0, 0, 0
        for dirpath, _, files in os.walk(folder):
            for f in files:
                rel = os.path.relpath(os.path.join(dirpath, f), base).replace(os.sep, "/")
                if "__pycache__" in rel:
                    continue
                targets = profile_destination(rel)
                if not targets:
                    continue
                total += 1
                if any(os.path.exists(os.path.join(root, t)) for t in targets):
                    here += 1
                if "/rules/on-demand/" in "/" + rel:
                    rows += 1
        requires, whole = [], False
        profile_md = os.path.join(folder, "PROFILE.builder.md")
        if os.path.isfile(profile_md):
            text = read(profile_md)
            whole = "## All or nothing" in text
            match = re.search(r"^## Requires\n(.*?)(?=^## |\Z)", text, re.S | re.M)
            if match:
                # `core` is a real requirement even though it is not a folder under `profiles/` —
                # filtering by that alone dropped every declared dependency on the engine.
                requires = [n for n in re.findall(r"`([a-z0-9-]+)`", match.group(1))
                            if n == "core" or os.path.isdir(os.path.join(base, n))]
        states.append({"name": name, "total": total, "here": here, "whole": whole,
                       "requires": requires, "rows": rows, "present": dropped_in(root, name)})
    return states


def own_files(root):
    """Installed skills and rules no profile carries — the project's own."""
    owned = set()
    for rel, _ in (walk_builder(root, "profiles") or []):
        owned.update(profile_destination(rel) or [])
    for rel, _ in (walk_builder(root, "core") or []):
        owned.update(core_destination(rel) or [])
    mine = {"skills": [], "rules": []}
    skills_dir = os.path.join(root, ".agents", "skills")
    for name in sorted(os.listdir(skills_dir)) if os.path.isdir(skills_dir) else []:
        real = os.path.realpath(os.path.join(skills_dir, name))
        target = os.path.relpath(real, root).replace(os.sep, "/") + "/SKILL.md"
        if os.path.isfile(os.path.join(root, target)) and target not in owned:
            mine["skills"].append(name + (" (yours only)" if "/.local/" in "/" + target else ""))
    for kind in ("always-on", "on-demand", "unplaced"):
        for f in rule_paths(root, kind):
            target = os.path.relpath(f, root).replace(os.sep, "/")
            if target not in owned:
                mine["rules"].append(target)
    return mine


def engine_independence(root, out):
    """The engine naming a profile by name.

    Core ships to every project. Naming `.agents/profiles/` is its job — it links them and audits
    them. Naming `kotlin-android` is a dependency on a folder most projects will not have, and it
    reads as a broken reference the moment they do not.
    """
    out.append("## The engine naming a profile\n")
    hits = []
    for base in (os.path.join(root, ".agents", "core"),
                 os.path.join(root, ".agents", "builder", "core")):
        for dirpath, _, files in os.walk(base):
            if "/tests/" in dirpath + "/" or "__pycache__" in dirpath or "/map" in dirpath:
                continue  # the suites use fixtures, and the map is a picture of what is installed
            for f in files:
                if not f.endswith(TEXT_SUFFIXES):
                    continue
                full = os.path.join(dirpath, f)
                for n, line in enumerate(read(full).splitlines(), 1):
                    for m in re.finditer(r"\.agents/(?:\.local/)?profiles/([a-z0-9-]+)", line):
                        hits.append((os.path.relpath(full, root), n, m.group(1)))
    if not hits:
        out.append("- none: the engine names the profiles folder, never a profile in it")
        return
    for rel, n, name in sorted(set(hits)):
        out.append(f"- `{rel}:{n}` names the profile `{name}`.")
    out.append("")
    out.append("Say it without the name where you can — *that stack's own code-style rule* reads the"
               " same and holds in a project that never took the profile. Where the engine really"
               " does need to know, it should say what it does when the profile is absent.")


def profile_independence(root, out):
    """Profiles naming the engine without declaring they need it.

    A profile's folder should lift into a project that never installed this setup. The moment one
    of its files names `.agents/core/…`, it only works here. A profile may depend on the engine —
    `specs` does — but then it says so in `## Requires`, and the dependency is a decision somebody
    made rather than a path that crept in.
    """
    base = os.path.join(root, ".agents", "builder", "profiles")
    out.append("## Profiles reaching into the engine\n")
    if not os.path.isdir(base):
        out.append("- no builder here, so profiles cannot be checked")
        return
    declared = {s["name"]: s["requires"] for s in (profile_state(root) or [])}
    hits = []
    for name in sorted(os.listdir(base)):
        if "core" in declared.get(name, []):
            continue
        for dirpath, _, files in os.walk(os.path.join(base, name)):
            for f in files:
                if "__pycache__" in dirpath or not f.endswith(TEXT_SUFFIXES):
                    continue
                full = os.path.join(dirpath, f)
                for n, line in enumerate(read(full).splitlines(), 1):
                    if ".agents/core/" in line:
                        hits.append((os.path.relpath(full, base), n, name))
    if not hits:
        out.append("- none: every profile that names the engine declares `core` under `## Requires`")
        return
    for rel, line, name in sorted(hits):
        out.append(f"- `{rel}:{line}` names `.agents/core/`, but `{name}` does not declare `core`"
                   " under `## Requires`.")
    out.append("")
    out.append("Either say the profile needs the engine, or say the same thing without the path —"
               " *the project's general code-style rule* reads the same to a person and keeps the"
               " folder liftable into a repository that never installed this setup.")


def declared_scopes(root):
    """What each engine form says it holds, and the phrases that mean another rule owns it.

    Authored in the form's frontmatter, not inferred from its words: a prototype that guessed from
    vocabulary put "retry and failure escalation" in the workflow rule, because "failure" appears
    in "read a build or lint failure". One shared word is not evidence. A phrase someone chose is.
    """
    out = {}
    for kind in ("always-on", "on-demand"):
        folder = os.path.join(root, ".agents", "builder", "core", "rules", kind)
        for f in sorted(os.listdir(folder)) if os.path.isdir(folder) else []:
            front = re.match(r"^---\n(.*?)\n---", read(os.path.join(folder, f)), re.S)
            if not front:
                continue
            block = re.search(r"^elsewhere:\n((?:  .+\n?)+)", front.group(1), re.M)
            if not block:
                continue
            owners = {}
            for line in block.group(1).splitlines():
                sibling, _, phrases = line.strip().partition(":")
                owners[sibling] = [t.strip().lower() for t in phrases.split(",") if t.strip()]
            out[f.replace(".seed.", ".")] = owners
    return out


def misplaced_rows(root, out):
    """Rows in an engine rule written in a sibling rule's language."""
    scopes = declared_scopes(root)
    out.append("## Rows that may belong in another engine rule\n")
    if not scopes:
        out.append("- no engine form declares an `elsewhere:` block, so there is nothing to check against")
        return
    hits = []
    for kind in ("always-on", "on-demand"):
        folder = os.path.join(root, ".agents", "core", "rules", kind)
        for f in md_files(folder):
            if f not in scopes:
                continue
            for line in read(os.path.join(folder, f)).splitlines():
                if not line.startswith("|") or "---" in line or line.startswith("| Topic"):
                    continue
                # Prose only, and whole words only. Code spans are names, not statements: `TAG`
                # in a logging example is not the git tag the workflow rule means, and `ci` inside
                # "decision" is not continuous integration.
                low = re.sub(r"`[^`]*`", " ", line).lower()
                for sibling, phrases in scopes[f].items():
                    found = [t for t in phrases
                             if re.search(r"\b" + re.escape(t) + r"\b", low)]
                    if found:
                        label = line.strip("| ").split("|")[0].strip()[:40] or line.strip()[:40]
                        hits.append((f, label, sibling, found))
    if not hits:
        out.append("- none: every row reads like the rule it is in")
        return
    for f, label, sibling, found in sorted(hits):
        out.append(f"- `{f}` row *{label}* uses " + ", ".join(f"`{t}`" for t in found[:3])
                   + f", which its form gives to `{sibling}`.")
    out.append("")
    out.append("Each engine form declares what it holds and which phrases belong to a sibling. A hit"
               " means a row reads like the other rule's subject — move it, or if it genuinely"
               " belongs here, the form's `elsewhere:` list is the thing to correct.")


def stack_vocabulary(root):
    """Per stack profile, the file and command names that identify its technology.

    A stack is a profile carrying *Tool commands* — every profile has a *Detection* section, so
    that alone does not tell a stack from a feature. The terms come from those two sections only,
    and only from backticks: `build.gradle.kts` and `AndroidManifest.xml` identify a stack, while
    ordinary prose identifies nothing and matches everything.
    """
    base = os.path.join(root, ".agents", "builder", "profiles")
    out = {}
    for name in sorted(os.listdir(base)) if os.path.isdir(base) else []:
        profile_md = os.path.join(base, name, "PROFILE.builder.md")
        if not os.path.isfile(profile_md):
            continue
        text = read(profile_md)
        if not re.search(r"^## Tool commands", text, re.M):
            continue
        terms = set()
        for heading in ("Detection", "Tool commands"):
            block = re.search(rf"^## {heading}.*?\n(.*?)(?=^## |\Z)", text, re.S | re.M)
            if block:
                terms |= set(re.findall(r"`([A-Za-z][\w.+-]{2,})`", block.group(1)))
        # a bare word is a coincidence waiting to happen; a dotted or hyphenated name is a thing
        out[name] = {t.lower() for t in terms if len(t) > 3}
    return out


def stack_content_in_core(root, out):
    """Core rules written in a stack's vocabulary — a lead that they belong in that stack's profile.

    Two or more identifying terms, because one is a coincidence. A hit is a lead to open, not a
    verdict: a repository fact can legitimately name a build file.
    """
    vocab = stack_vocabulary(root)
    out.append("## Stack wording in the engine's own rules\n")
    if not vocab:
        out.append("- no stack profile in the builder, so there is nothing to compare against")
        return
    # Only where the content has somewhere to go. A stack rule the loaders read at the same step as a
    # core rule — both always-on, or rows for the same step — is that somewhere; without one, stack
    # words in a core rule are the form doing its job — `project-sensitive-paths-rules` answers with
    # this repository's build files whatever the stack, and a warning that can never clear is one
    # nobody reads.
    always, rows = loader_placements(root)
    steps = {None: set(always)}
    for step, paths in rows:
        steps.setdefault(step, set()).update(paths)
    stack_home = re.compile(r"\.agents/(?:\.local/)?profiles/([a-z0-9-]+)/rules/")
    hits = set()
    for together in steps.values():
        homes = {}
        for path in together:
            match = stack_home.match(path)
            if match and match.group(1) in vocab:
                homes[match.group(1)] = match.group(0)
        for path in sorted(p for p in together if p.startswith(".agents/core/rules/")):
            body = {w.lower() for w in re.findall(r"[A-Za-z][\w.+-]{2,}", read(os.path.join(root, path)))}
            for name, home in homes.items():
                shared = sorted(body & vocab[name])
                if len(shared) >= 2:
                    hits.add((path, name, home, tuple(shared)))
    if not hits:
        out.append("- none: no engine rule is written for a stack that ships a rule of its own for"
                   " the same step")
        return
    for path, name, home, shared in sorted(hits):
        out.append(f"- `{path}` uses {len(shared)} term(s) belonging to `{name}`: "
                   + ", ".join(f"`{t}`" for t in shared[:6])
                   + f". If those rows only make sense on that stack, they belong in `{home}`.")
    out.append("")
    out.append("The engine's rules go to every project that installs this setup, whatever it is"
               " written in. A row that only holds on one stack is one a project on another stack"
               " reads and cannot act on. This is a lead, not a verdict: a repository fact may name"
               " a build file for a good reason.")


def profiles(root, out):
    out.append("## Profiles\n")
    states = profile_state(root)
    if states is None:
        out.append("- no builder here, so what is available cannot be read")
        return
    builder = read(os.path.join(root, ".agents", "builder", "VERSION")).strip() or "unknown"
    ours = sorted(p for p in OUR_PATHS if os.path.exists(os.path.join(root, p)))
    out.append(f"- builder here: {builder}. Nothing records which version the project was installed"
               " at — what actually differs from this builder is under *Builder files against"
               " installed files*.")
    out.append(f"- **this setup is installed here: {'yes' if ours else 'no'}** — {len(ours)} path(s)"
               " only this setup uses are present. A count of zero means the repository is not ours,"
               " whatever else it has: `AGENTS.md`, `CLAUDE.md` and `.claude/settings.json` are"
               " ordinary names any project may own, so they never answer this question.")
    out.append("")
    for heading, keep in (
            ("### Dropped in", lambda s: s["present"] and s["here"] == s["total"]),
            ("### Dropped in, with parts taken out",
             lambda s: s["present"] and s["here"] < s["total"] and not s["whole"]),
            ("### Dropped in but incomplete — it installs whole, and some of it is gone",
             lambda s: s["present"] and s["here"] < s["total"] and s["whole"]),
            ("### Not dropped in", lambda s: not s["present"])):
        rows = [s for s in states if keep(s)]
        if not rows:
            continue
        out.append(heading + "\n")
        for s in rows:
            line = (f"- `{s['name']}` — {s['total']} files, none here" if not s["present"]
                    else f"- `{s['name']}` at `{s['present']}/` — {s['here']}/{s['total']} files")
            if s["requires"]:
                line += "; requires " + ", ".join(f"`{r}`" for r in s["requires"])
            if s["rows"] and s["present"] and s["here"] < s["total"]:
                line += f"; {s['rows']} on-demand rule(s) that `LOADER.md` would name"
            out.append(line)
        out.append("")
    orphans = []
    for state in states:
        if state["present"]:
            continue
        folder = os.path.join(root, ".agents", "builder", "profiles", state["name"])
        for dirpath, _, files in os.walk(folder):
            for f in files:
                if ".seed." not in f:
                    continue
                rel = os.path.relpath(os.path.join(dirpath, f), os.path.dirname(folder))
                for target in (profile_destination(rel.replace(os.sep, "/")) or []):
                    if os.path.exists(os.path.join(root, target)):
                        orphans.append((target, state["name"]))
                        break
    if orphans:
        out.append("### Answered here, by a profile that is no longer dropped in\n")
        out += [f"- `{t}` — the form came with `{n}`" for t, n in sorted(set(orphans))]
        out.append("")
        out.append("Deleting a profile's folder takes its skills, agents and loader rows with it, but"
                   " not this: a form's answer describes the repository, so it is the project's and"
                   " is never deleted for you. Keep it if it still says something true, or delete it"
                   " by hand. Until then it loads every session with nothing behind it.")
        out.append("")
    mine = own_files(root)
    if mine["skills"] or mine["rules"]:
        out.append("### Yours, carried by no profile\n")
        out += [f"- skill `{s}`" for s in mine["skills"]] + [f"- rule `{r}`" for r in mine["rules"]]
        out.append("")
    out.append("A profile is installed by dropping its folder into `.agents/profiles/`, or"
               " `.agents/.local/profiles/` to keep it to yourself, and uninstalled by deleting that"
               " folder and running `project-sync-profiles-and-skills`. Taking parts out of a folder is a"
               " supported choice, so *with parts taken out* is not a fault — except where the"
               " profile declares *All or nothing*, and then it is.")


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--repo-root")
    parser.add_argument("--write-score", action="store_true", help="rewrite the ledger's Score section and stop")
    args = parser.parse_args()
    root = repo_root(args.repo_root)
    if args.write_score:
        write_score(root)
        return
    rows = skills(root)
    files = setup_files(root)
    out = ["# Validate inventory\n"]
    ledger_score(root, out)
    out.append("")
    out.append("## Load\n")
    load_numbers(root, rows, out)
    out.append("")
    budgets(root, rows, out)
    out.append("")
    profiles(root, out)
    out.append("")
    profile_files(root, out)
    out.append("")
    stack_content_in_core(root, out)
    out.append("")
    misplaced_rows(root, out)
    out.append("")
    profile_independence(root, out)
    out.append("")
    engine_independence(root, out)
    out.append("")
    retired_names(root, files, out)
    out.append("")
    missing_paths(root, files, out)
    out.append("")
    links(root, out)
    out.append("")
    map_check(root, out)
    print("\n".join(out))


if __name__ == "__main__":
    main()
