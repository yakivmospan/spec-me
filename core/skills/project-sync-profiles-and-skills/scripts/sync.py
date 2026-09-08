#!/usr/bin/env python3
"""Make every dropped-in profile visible to both tools, say what clashes, and prune what is gone.

A profile is a folder you drop into `.agents/profiles/` — or `.agents/.local/profiles/`, for yourself
alone. Its files stay there. This links them where Claude and Codex look, because both require a flat
layout (`.claude/skills/<name>/SKILL.md`, one level) and neither discovers a nested folder.

Deleting the folder and running this again is the uninstall: a link whose source is gone is pruned.
A real file is never replaced and never removed — only links, and the forwarding stubs written where
symlinks are unavailable. An answer written from one of its `.seed.` forms sits inside the folder
and goes with it.

Two things can want one name. That is never resolved silently: the first claimant in a fixed order
wins — core, then the shared profiles in name order, then your own — and everything else is printed
under *Conflicts* with the ways out.

Usage: python3 sync.py [--repo-root PATH] [--check]
"""
import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

# a profile's folder -> where each tool looks for it, and which files belong there
SLOTS = [
    # Skills go to `.agents/skills` only, which is where Codex looks. Claude is served by mirroring
    # that one folder below, so each destination has a single writer and a second run changes nothing.
    ("skills", ".agents/skills", None),
    ("agents/claude", ".claude/agents", ".md"),
    ("agents/codex", ".codex/agents", ".toml"),
]
STUB = ".forwarding-stub"

# Every folder this script may write a link into — what it prunes from, and what it excludes in.
DESTINATIONS = [".agents/skills", ".claude/skills", ".claude/agents", ".codex/agents"]

# The block this script owns inside .git/info/exclude. Everything between the two lines is rewritten
# on every run, so a profile you delete cannot leave a line behind.
EXCLUDE_HEAD = "# profile-sync: yours alone, rewritten on every run — do not edit between these lines"
EXCLUDE_TAIL = "# /profile-sync"


def repo_root(override):
    if override:
        return Path(override).resolve()
    here = Path(__file__).resolve()
    out = subprocess.run(["git", "-C", str(here.parent), "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True)
    return Path(out.stdout.strip()) if out.stdout.strip() else here.parents[3]


def ours(path: Path) -> bool:
    """A link or stub this script wrote, as opposed to something a person put there."""
    return path.is_symlink() or (path / STUB).is_file()


def ignores_case(root: Path) -> bool:
    """Whether this filesystem treats two names that differ only in case as one name."""
    return (root / ".agents").is_dir() and (root / ".AGENTS").is_dir()


# --- the exclude file ---------------------------------------------------------------------------

def git_exclude_file(root: Path):
    out = subprocess.run(["git", "-C", str(root), "rev-parse", "--git-path", "info/exclude"],
                         capture_output=True, text=True)
    if out.returncode or not out.stdout.strip():
        return None
    p = Path(out.stdout.strip())
    return p if p.is_absolute() else root / p


def write_excludes(root: Path, lines, warn):
    """Put every private path in one owned block, in one pass. Read once, written once.

    Rewriting the whole block is what keeps a deleted profile from leaving its line behind: the
    block is built from what is there now, never edited entry by entry.
    """
    path = git_exclude_file(root)
    if path is None:
        return
    wanted = sorted(set(lines))
    try:
        old = path.read_text().splitlines() if path.exists() else []
        kept, skipping = [], False
        for line in old:
            if line == EXCLUDE_HEAD:
                skipping = True
                continue
            if line == EXCLUDE_TAIL:
                skipping = False
                continue
            # Lines this script wrote before it owned a block, including ones for folders the
            # setup has since stopped using, so an old tree cleans itself up.
            legacy = ("/.agents/rules/", "/.agents/.local/rules/")
            if skipping or line.startswith(legacy) or any(line.startswith(f"/{d}/") for d in DESTINATIONS):
                continue
            kept.append(line)
        while kept and not kept[-1].strip():
            kept.pop()
        body = kept + ([EXCLUDE_HEAD] + wanted + [EXCLUDE_TAIL] if wanted else [])
        if body == old:
            return
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(body) + ("\n" if body else ""))
    except OSError:
        warn(f"could not write {path} — add these by hand so they never reach a commit: "
             + ", ".join(wanted))


# --- placing one link ---------------------------------------------------------------------------

def write_stub(link: Path, source: Path):
    """No symlinks here: leave a real file that sends the agent to the source."""
    link.mkdir(parents=True, exist_ok=True)
    (link / STUB).touch()
    head, seen = [], 0
    for line in (source / "SKILL.md").read_text().splitlines():
        head.append(line)
        if line == "---":
            seen += 1
            if seen == 2:
                break
    (link / "SKILL.md").write_text("\n".join(head) + f"""

> Forwarding stub. The real skill lives at `{source}/SKILL.md`.
> Read that file now and follow it. Any scripts it names are relative to that folder, not this one.
""")


def remove(path: Path):
    if path.is_symlink() or path.is_file():
        path.unlink()
    else:
        for child in sorted(path.rglob("*"), reverse=True):
            child.unlink() if not child.is_dir() else child.rmdir()
        path.rmdir()


def place(link: Path, source: Path, check):
    """Point `link` at `source`. Returns 'linked', 'stubbed', 'same', 'taken', 'unwritable' or 'would'."""
    rel = os.path.relpath(source, link.parent)
    if link.is_symlink() and os.readlink(link) == rel:
        return "same"
    if (link.exists() or link.is_symlink()) and not ours(link):
        return "taken"
    if check:
        return "would"
    try:
        if link.exists() or link.is_symlink():
            remove(link)
        link.parent.mkdir(parents=True, exist_ok=True)
        link.symlink_to(rel)
        return "linked"
    except OSError:
        if not (source / "SKILL.md").is_file():
            return "unwritable"
        try:
            write_stub(link, source)
            return "stubbed"
        except OSError:
            return "unwritable"


# --- reading the tree ---------------------------------------------------------------------------

def profiles(root: Path):
    """Every profile in the order that decides who wins a name: core, then shared, then yours.

    `.agents/core/` has a profile's shape and is linked the same way, but it lives at the root
    instead of under `profiles/`, because it is the one that cannot be dropped or deleted: it is
    what links the others, holds the constitution's ground rules and answers the project's forms.
    It goes first so that nothing dropped in later can take a name out from under it.
    """
    core = root / ".agents/core"
    if core.is_dir():
        yield core, False
    for base, local in ((root / ".agents/profiles", False), (root / ".agents/.local/profiles", True)):
        for folder in sorted(base.iterdir()) if base.is_dir() else []:
            if folder.is_dir():
                yield folder, local


def claims(root: Path, report):
    """What every source wants, in winning order: one entry per link this run would write.

    Built entirely from the profiles, never from what is already on disk, so `--check` shows the
    same work the real run would do.
    """
    out, seeds, broken = [], [], []
    for profile, is_local in profiles(root):
        for slot, dest, suffix in SLOTS:
            src = profile / slot
            for item in sorted(src.iterdir()) if src.is_dir() else []:
                if ".seed." in item.name:
                    seeds.append(item.relative_to(root))
                    continue
                if suffix:
                    if not item.is_file() or not item.name.endswith(suffix):
                        continue
                else:
                    if not item.is_dir():
                        continue  # a stray note beside the skills is not a skill
                    if not (item / "SKILL.md").is_file():
                        broken.append(item.relative_to(root))
                        continue  # half a skill reaches neither tool, rather than one of them
                out.append({"dest": root / dest / item.name, "source": item,
                            "owner": profile.name, "local": is_local})

    # Loose local skills, the way to keep one to yourself from before profiles existed.
    loose = root / ".agents/.local/skills"
    for skill in sorted(loose.iterdir()) if loose.is_dir() else []:
        if not skill.is_dir():
            continue
        if not (skill / "SKILL.md").is_file():
            broken.append(skill.relative_to(root))
            continue
        out.append({"dest": root / ".agents/skills" / skill.name, "source": skill,
                    "owner": ".local/skills", "local": True})
    return out, seeds, broken


def mirror_claims(root: Path, winners):
    """Every skill Codex can see must reach Claude too — including ones no profile brought.

    The mirror always points at `.agents/skills/<name>`, never into the profile, so this folder has
    one writer and the chain is the same whether the skill came from a profile or was written here.
    """
    shared = root / ".agents/skills"
    names = {}
    for c in winners:
        if c["dest"].parent == shared:
            names[c["dest"].name] = c["local"]
    for skill in sorted(shared.iterdir()) if shared.is_dir() else []:
        if skill.name not in names and skill.is_dir() and (skill / "SKILL.md").is_file():
            names[skill.name] = "/.local/" in os.path.realpath(skill)
    return [{"dest": root / ".claude/skills" / name, "source": shared / name,
             "owner": "the shared skills folder", "local": local}
            for name, local in sorted(names.items())]


def resolve(cands, fold):
    """First claim wins; every later one is a conflict. Returns (winners, clashes)."""
    seen, winners, clashes = {}, [], []
    for c in cands:
        key = str(c["dest"]).casefold() if fold else str(c["dest"])
        if key in seen:
            clashes.append((seen[key], c))
            continue
        seen[key] = c
        winners.append(c)
    return winners, clashes


# --- the loader ---------------------------------------------------------------------------------

# The shared loader is committed; the local one sits in the gitignored folder and names what only
# its owner has. Both are the project's files, edited by hand — this script only keeps them honest.
LOADERS = ((".agents/LOADER.md", False), (".agents/.local/LOADER.md", True))
RULE_PATH = re.compile(r"`(\.agents/[^`\s]+\.md)`")
# A line runs a skill by naming it this way, which is what lets a missing one be found.
SKILL_NAMED = re.compile(r"the `([a-z0-9][a-z0-9-]*)` skill")
LOADING_KEYS = ("load-when:", "when:")


def named_paths(text):
    """The files loader text names. The constitution and the loaders themselves are the prose around
    the placements, not placements: the shared loader points at the local one, which a teammate's
    clone does not have, and that line must not be pruned for it."""
    return [p for p in RULE_PATH.findall(text)
            if p not in dict(LOADERS) and p != ".agents/CONSTITUTION.md"]


def unmet_requirements(root: Path):
    """What a dropped-in profile says it depends on, and has not got.

    Read from each profile's own `PROFILE.md`, which ships with the folder — the builder's
    `PROFILE.builder.md` is never installed, so on a normal setup nothing else would know what
    depends on what.
    """
    here = {name for name, _ in ((p.name, p) for p, _ in profiles(root))}
    missing = []
    for profile, _ in profiles(root):
        card = profile / "PROFILE.md"
        if not card.is_file():
            continue
        for line in card.read_text(errors="replace").splitlines():
            if not line.lstrip("- ").startswith("**Depends on:**"):
                continue
            for need in re.findall(r"`([a-z0-9-]+)`", line):
                if need not in here:
                    missing.append((profile.name, need))
    return missing


def rule_files(root: Path):
    """Every rule here, from core and each profile, as (path, is_local, folder). A form is not a rule yet."""
    out = []
    for profile, is_local in profiles(root):
        for folder_kind in ("always-on", "on-demand"):
            folder = profile / "rules" / folder_kind
            for rule in sorted(folder.iterdir()) if folder.is_dir() else []:
                if rule.suffix == ".md" and ".seed." not in rule.name and rule.is_file():
                    out.append((rule.relative_to(root).as_posix(), is_local, folder_kind))
    return out


def installed_skills(root: Path):
    """Every skill name here, mapped to whether only this person has it."""
    found = {}
    for profile, is_local in profiles(root):
        folder = profile / "skills"
        for skill in sorted(folder.iterdir()) if folder.is_dir() else []:
            if (skill / "SKILL.md").is_file():
                found.setdefault(skill.name, is_local)
    # `.agents/skills/` holds links; only a real folder there is a skill someone made by hand.
    for folder, is_local in ((root / ".agents/.local/skills", True), (root / ".agents/skills", False)):
        for skill in sorted(folder.iterdir()) if folder.is_dir() else []:
            if not skill.is_symlink() and (skill / "SKILL.md").is_file():
                found.setdefault(skill.name, is_local)
    return found


def declares_loading_key(path: Path) -> bool:
    text = path.read_text(errors="replace")
    if not text.startswith("---\n"):
        return False
    return any(line.startswith(LOADING_KEYS) for line in text.split("---", 2)[1].splitlines())


def starter_loader(rules, local: bool):
    """A loader for a project that has none: always-on rules placed by their folder, nothing else.

    Where an on-demand rule goes is judgement the script cannot make, so those are left for the sync
    skill to propose and the user to confirm; each is reported as unplaced until then.
    """
    always = [f"- `{path}`" for path, _, folder in rules if folder == "always-on"]
    if local:
        head = """# Rule loader — yours alone

What you, and only you, read and run at each step. Your file: edit it by hand. It adds to
`.agents/LOADER.md` and never replaces a line in it; within a step, the shared lines come first.
`project-sync-profiles-and-skills` removes a line whose file is gone and reports a rule of yours no
line places.

**Every session, after the shared loader:**"""
    else:
        head = """# Rule loader

What an agent reads, and what it runs, at each step of the work — the project's file, edited by hand.
`project-sync-profiles-and-skills` keeps it honest: it removes a line whose file is gone, and reports a
rule no line places, which never loads. Name only what every clone has; your own go in
`.agents/.local/LOADER.md`.

**Every session, before any task:** read `.agents/CONSTITUTION.md` first — it outranks everything
below — then each of these:"""
    return f"""{head}

<!-- always-on -->
{chr(10).join(always) if always else "- none"}
<!-- /always-on -->

**At each step, top to bottom:** read the files a row names, and run a skill a row names as "the
`name` skill".

<!-- on-demand table -->
| Before you… | Read or run |
|---|---|
<!-- /on-demand table -->
"""


def prune(text: str, root: Path):
    """The loader without the files that are gone, and the paths it dropped.

    A list line names one file, so it goes whole. A table row loses the missing path, and goes whole
    once it names nothing else.
    """
    out, gone = [], []
    for line in text.splitlines(keepends=True):
        missing = [p for p in named_paths(line) if not (root / p).exists()]
        if not missing:
            out.append(line)
            continue
        gone += missing
        cells = line.rstrip("\n").split("|")
        if not line.lstrip().startswith("|") or len(cells) < 4:
            continue
        kept = [part for part in re.split(r"\s+and\s+", cells[2].strip())
                if part.strip("` ") not in missing]
        if kept:
            out.append("|".join(cells[:2] + [f" {' and '.join(kept)} "] + cells[3:]) + "\n")
    return "".join(out), gone


def check_loaders(root: Path, check: bool, report, warnings):
    """Keep both loaders honest without deciding anything a person should.

    Each loader is the project's own file. This starts one where it is missing, drops a line whose file
    is gone, and says what it cannot fix: a rule no line places, a skill a line runs that is not here,
    and a shared line naming something only one person has.
    """
    rules = rule_files(root)
    skills = installed_skills(root)
    for rel, mine in LOADERS:
        path = root / rel
        own = [r for r in rules if r[1] == mine]
        if path.is_file():
            text = path.read_text()
        elif own:
            text = starter_loader(own, mine)
            report(f"loader  {rel} — started, always-on rules placed by their folder")
            if not check:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text)
        else:
            continue
        kept, gone = prune(text, root)
        for missing in gone:
            report(f"pruned  {rel} named {missing}, which is gone")
        if gone and not check:
            path.write_text(kept)
        named = set(named_paths(kept))
        for rule, _, _ in own:
            if rule not in named:
                warnings.append(f"unplaced {rule} — no line in {rel} names it, so it never loads. "
                                f"Put it at the step it serves; the sync skill proposes where")
        for skill in dict.fromkeys(SKILL_NAMED.findall(kept)):
            if skill not in skills:
                warnings.append(f"{rel} runs the `{skill}` skill, which is not installed — install it, "
                                f"or delete that line")
            elif skills[skill] and not mine:
                warnings.append(f"{rel} runs the `{skill}` skill, which only you have — move that line "
                                f"to .agents/.local/LOADER.md")
        if not mine:
            for local in sorted(p for p in named if p.startswith(".agents/.local/")):
                warnings.append(f"{rel} names {local}, which only you have — move that line to "
                                f".agents/.local/LOADER.md")
    carriers = [rule for rule, _, _ in rules if declares_loading_key(root / rule)]
    for profile, _ in profiles(root):
        folder = profile / "skills"
        carriers += [(s / "SKILL.md").relative_to(root).as_posix()
                     for s in (sorted(folder.iterdir()) if folder.is_dir() else [])
                     if (s / "SKILL.md").is_file() and declares_loading_key(s / "SKILL.md")]
    for carrier in carriers:
        warnings.append(f"{carrier} declares `load-when:`, which nothing reads — a loader line decides "
                        f"when it is read or run; delete the key")


def carried_core(root: Path):
    """The part of the constitution marked to survive a compaction, or "" when nothing is marked."""
    text = (root / ".agents/CONSTITUTION.md").read_text() if (root / ".agents/CONSTITUTION.md").is_file() else ""
    if "<!-- carried -->" not in text or "<!-- /carried -->" not in text:
        return ""
    return text.split("<!-- carried -->", 1)[1].split("<!-- /carried -->", 1)[0].strip()


def write_agents_core(root: Path, check: bool, report):
    """Copy the constitution's carried section into AGENTS.md, between its own markers.

    `AGENTS.md` is put in front of an agent again on every request; a file read by a tool call is
    not, and a long session's compaction can summarise it away. So the part that would cause harm if
    it were forgotten is carried here, generated from the one source so the two cannot drift.

    A project whose `AGENTS.md` has no markers is left completely alone — this never adds a section
    to someone's file, it only keeps one that is already there up to date.
    """
    agents = root / "AGENTS.md"
    head, tail = "<!-- constitution core -->", "<!-- /constitution core -->"
    if not agents.is_file():
        return
    text = agents.read_text()
    if head not in text or tail not in text:
        return
    core = carried_core(root)
    if not core:
        report("warn    .agents/CONSTITUTION.md has no <!-- carried --> section, so AGENTS.md's "
               "copy of it cannot be rebuilt")
        return
    before, rest = text.split(head, 1)
    _, after = rest.split(tail, 1)
    body = f"{before}{head}\n{core}\n{tail}{after}"
    if body == text:
        return
    report("core    AGENTS.md — the constitution's carried section, refreshed")
    if not check:
        agents.write_text(body)


def rebuild_map(root: Path, check: bool, report):
    """The map is derived state too, so it is rebuilt here rather than by a command to remember."""
    script = Path(__file__).parent / "build_setup_map.py"
    if check or not script.is_file():
        return
    out = subprocess.run([sys.executable, str(script), "--repo-root", str(root)],
                         capture_output=True, text=True)
    for line in (out.stdout or "").splitlines():
        if line.strip() and "no change" not in line:
            report(f"map     {line.strip()}")


# --- saying what clashed ------------------------------------------------------------------------

class Conflicts:
    """One block per name, however many things wanted it.

    A name is the unit a person can act on, so everything competing for one name is reported
    together: a second block about the same path would only read as a second problem.
    """

    def __init__(self, root: Path):
        self.root = root
        self.by_dest = {}
        self.incomplete = []

    def rel(self, path):
        return Path(path).relative_to(self.root).as_posix()

    def at(self, dest):
        return self.by_dest.setdefault(dest, {"claims": [], "taken": False, "unwritable": False,
                                              "cased": False})

    def wants(self, dest, claim, cased=False):
        entry = self.at(dest)
        if claim not in entry["claims"]:
            entry["claims"].append(claim)
        entry["cased"] = entry["cased"] or cased

    def taken(self, dest, claim):
        self.wants(dest, claim)
        self.at(dest)["taken"] = True

    def unwritable(self, dest, claim):
        self.wants(dest, claim)
        self.at(dest)["unwritable"] = True

    def half_a_skill(self, path):
        self.incomplete.append(path)

    def count(self):
        return len(self.by_dest) + len(self.incomplete)

    def owner(self, claim):
        return f"`{self.rel(claim['source'])}` (profile `{claim['owner']}`)"

    def render(self):
        out = []
        for path in sorted(self.incomplete):
            out += [f"conflict  {path}",
                    "          a skill folder with no `SKILL.md`, so neither tool was given it —"
                    " half a skill reaching one tool and not the other would be worse than none.",
                    "          Ways out: add `SKILL.md` to that folder, or remove the folder.", ""]
        for dest in sorted(self.by_dest, key=str):
            e, claims = self.by_dest[dest], self.by_dest[dest]["claims"]
            what = "skill" if "skills/" in str(dest) else "agent"
            out.append(f"conflict  {self.rel(dest)}")
            if e["unwritable"]:
                out += [f"          could not be written, so this {what} is not reachable there",
                        f"          wants it   {self.owner(claims[0])}",
                        f"          Ways out: check what owns `{self.rel(dest.parent)}` and what it"
                        " allows, then run this again.", ""]
                continue
            if e["taken"]:
                out.append(f"          in the way a real file or folder, not a link — yours, not a"
                           f" profile's. It was left exactly as it is.")
                for c in claims:
                    out.append(f"          wants it   {self.owner(c)}")
                out += ["          Ways out:",
                        "            - keep yours — nothing to do; the profile's copy stays unused",
                        "            - use the profile's — move your own aside, then run this again",
                        "            - keep both — rename one of them", ""]
                continue
            if e["cased"]:
                out.append("          this filesystem ignores case, so these names are one name here."
                           " On Linux both would work, so the repository would behave differently there.")
            else:
                out.append(f"          more than one profile brings {'a' if what == 'skill' else 'an'}"
                           f" {what} by that name")
            out.append(f"          using      {self.owner(claims[0])}")
            for c in claims[1:]:
                out.append(f"          unused     {self.owner(c)}")
            out += [f"          `{claims[0]['owner']}` wins because the order is fixed: core, then the"
                    " shared profiles by name, then your own.",
                    "          Ways out: rename one of them to keep both, or remove the profile whose"
                    " copy you do not want.", ""]
        return out


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--repo-root")
    parser.add_argument("--check", action="store_true", help="report what would change, write nothing")
    args = parser.parse_args()
    root = repo_root(args.repo_root)
    if not (root / ".agents").is_dir():
        sys.exit(f"error: no .agents/ under {root} — run from inside the repo")

    fold = ignores_case(root)
    lines, warnings = [], []
    conflicts = Conflicts(root)
    counts = {"linked": 0, "stubbed": 0, "same": 0, "taken": 0, "unwritable": 0, "would": 0, "pruned": 0}

    cands, seeds, broken = claims(root, lines.append)
    winners, clashes = resolve(cands, fold)
    winners += mirror_claims(root, winners)
    winners, more = resolve(winners, fold)
    clashes += more

    for name in broken:
        conflicts.half_a_skill(name.as_posix())
    for won, lost in clashes:
        conflicts.wants(won["dest"], won)
        conflicts.wants(won["dest"], lost, cased=str(won["dest"]) != str(lost["dest"]))

    wanted, private = set(), set()
    for c in winners:
        wanted.add(c["dest"])
        if c["local"]:
            private.add("/" + c["dest"].relative_to(root).as_posix())
        result = place(c["dest"], c["source"], args.check)
        counts[result] += 1
        if result in ("linked", "stubbed"):
            lines.append(f"{result:<7} {c['dest'].relative_to(root)}")
        elif result == "taken":
            conflicts.taken(c["dest"], c)
        elif result == "unwritable":
            conflicts.unwritable(c["dest"], c)

    # Prune: ours, and nothing wants it any more.
    for dest in DESTINATIONS:
        folder = root / dest
        for existing in sorted(folder.iterdir()) if folder.is_dir() else []:
            if existing in wanted or not ours(existing):
                continue
            # Only remove what this script could have made: a link into core, a profile or a local
            # skill, or one into `.agents/skills`, or one that no longer resolves. A link someone
            # else put here — the builder's developer rule, say — is not ours to prune.
            target = os.readlink(existing) if existing.is_symlink() else ""
            known = ("/profiles/", "/core/", "/.local/skills/", ".agents/skills/")
            if existing.is_symlink() and existing.exists() and not any(m in target for m in known):
                continue
            counts["pruned"] += 1
            lines.append(f"pruned  {existing.relative_to(root)} — its source is gone")
            if not args.check:
                remove(existing)

    if not args.check:
        write_excludes(root, private, warnings.append)

    for who, need in unmet_requirements(root):
        warnings.append(f"`{who}` says it depends on `{need}`, which is not here. Drop that in, or take "
                        f"`{who}` out — half of a pair does less than nothing.")
    check_loaders(root, args.check, lines.append, warnings)
    write_agents_core(root, args.check, lines.append)
    rebuild_map(root, args.check, lines.append)

    print("\n".join(lines) if lines else "nothing to do")
    print()
    verb = "would change" if args.check else "changed"
    print(f"{verb}: linked {counts['linked'] + counts['would']}  stubbed {counts['stubbed']}  "
          f"unchanged {counts['same']}  pruned {counts['pruned']}  left alone {counts['taken']}")
    if conflicts.count():
        print(f"\n{conflicts.count()} name(s) in conflict. Nothing was chosen for you, and nothing"
              " of yours was touched:\n")
        print("\n".join(conflicts.render()))
    for s in sorted(seeds):
        print(f"seed    {s} — answer it into the project; a form is never linked")
    for w in warnings:
        print(f"warn    {w}")
    if counts["stubbed"]:
        print("note: stubs cost an extra file read. For real symlinks on Windows, enable Developer "
              "Mode and set git config core.symlinks true")


main()
