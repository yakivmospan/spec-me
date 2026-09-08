#!/usr/bin/env python3
"""Run the engine against throwaway repos, and check what it did.

Every case builds a fresh repository in a temporary folder, copies this repo's own `.agents/core`
into it so the real scripts are the ones under test, drops profiles in or takes them away, and then
asserts on the tree and on what the run printed. Nothing here touches the repository you are in.

Usage: python3 stress_profile_sync.py [-k SUBSTRING] [-v]
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
CORE = REPO / ".agents/core"
BUILDER = REPO / ".agents/builder"

# The install map that `project-test-setup` publishes. Importing it rather than restating it is the
# point: if the two ever disagree, a real install would break and these cases break with it.
sys.path.insert(0, str(CORE / "skills/project-test-setup/scripts"))
import validate_inventory as V
SYNC = ".agents/core/skills/project-sync-profiles-and-skills/scripts/sync.py"

CASES = []


def case(fn):
    CASES.append(fn)
    return fn


class Case:
    """One scenario's verdict: every failed expectation, in the order they were checked."""

    def __init__(self, name):
        self.name = name
        self.fails = []
        self.notes = []

    def ok(self, cond, msg):
        if not cond:
            self.fails.append(msg)
        return bool(cond)

    def note(self, msg):
        self.notes.append(msg)


# --- building a repository ----------------------------------------------------------------------

def make_repo(git=True):
    root = Path(tempfile.mkdtemp(prefix="sync-stress-")).resolve()
    (root / ".agents").mkdir()
    shutil.copytree(CORE, root / ".agents/core", symlinks=True)
    (root / "AGENTS.md").write_text("# Test repo\n")
    if git:
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    return root


def mkskill(folder: Path, name, desc="what it does", body="Body.\n", skill_md=True):
    d = folder / name
    d.mkdir(parents=True, exist_ok=True)
    if skill_md:
        (d / "SKILL.md").write_text(f"---\nname: {name}\ndescription: {desc}\n---\n\n{body}")
    return d


def mkrule(profile: Path, kind, name, body="Rule body.\n"):
    d = profile / "rules" / kind
    d.mkdir(parents=True, exist_ok=True)
    (d / name).write_text(body)
    return d / name


def write_loader(root: Path, always=(), rows=(), local=False):
    """A loader kept by hand, the way a project keeps its own: paths from the root, rows as (step, cell)."""
    lines = ["# Rule loader", "", "Our own words, which the sync must leave as they are.", "",
             "<!-- always-on -->"] + [f"- `{p}`" for p in always] + [
             "<!-- /always-on -->", "", "<!-- on-demand table -->", "| Before you… | Read or run |",
             "|---|---|"] + [f"| {step} | {cell} |" for step, cell in rows] + [
             "<!-- /on-demand table -->", ""]
    path = root / (".agents/.local/LOADER.md" if local else ".agents/LOADER.md")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines))
    return path


def always_block(text):
    return text.split("<!-- always-on -->", 1)[1].split("<!-- /always-on -->", 1)[0]


def rel(root: Path, path: Path):
    return path.relative_to(root).as_posix()


def mkprofile(root: Path, name, local=False, skills=(), claude=(), codex=()):
    base = root / (".agents/.local/profiles" if local else ".agents/profiles")
    p = base / name
    p.mkdir(parents=True, exist_ok=True)
    for s in skills:
        mkskill(p / "skills", s)
    for a in claude:
        (p / "agents/claude").mkdir(parents=True, exist_ok=True)
        (p / "agents/claude" / a).write_text("---\nname: x\n---\nagent\n")
    for a in codex:
        (p / "agents/codex").mkdir(parents=True, exist_ok=True)
        (p / "agents/codex" / a).write_text("name = 'x'\n")
    return p


def sync(root: Path, *args, timeout=60):
    out = subprocess.run([sys.executable, str(root / SYNC), "--repo-root", str(root), *args],
                         capture_output=True, text=True, timeout=timeout)
    return out


def summary(out):
    """The counts line as a dict, so a case can assert on numbers instead of prose."""
    for line in (out.stdout or "").splitlines():
        if line.startswith(("changed:", "would change:")):
            body = line.split(":", 1)[1]
            nums, key = {}, []
            for token in body.split():
                if token.isdigit():
                    nums[" ".join(key)] = int(token)
                    key = []
                else:
                    key.append(token)
            return nums
    return {}


def links_in(root: Path, dest):
    d = root / dest
    return sorted(p.name for p in d.iterdir()) if d.is_dir() else []


def target_of(root: Path, path):
    p = root / path
    return os.readlink(p) if p.is_symlink() else None


def excludes(root: Path):
    f = root / ".git/info/exclude"
    return f.read_text().splitlines() if f.is_file() else []


# --- the drop-in round trip ---------------------------------------------------------------------

@case
def core_only_links_itself(c):
    r = make_repo()
    out = sync(r)
    c.ok(out.returncode == 0, f"core-only run failed: {out.stderr.strip()}")
    names = links_in(r, ".agents/skills")
    c.ok("project-test-setup" in names, "core's skills did not reach .agents/skills")
    c.ok(links_in(r, ".claude/skills") == names, ".claude/skills does not mirror .agents/skills")
    c.ok(links_in(r, ".claude/agents") == ["runner.md"], f"claude agents: {links_in(r, '.claude/agents')}")
    c.ok(links_in(r, ".codex/agents") == ["runner.toml"], f"codex agents: {links_in(r, '.codex/agents')}")
    return r


@case
def second_run_changes_nothing(c):
    r = make_repo()
    mkprofile(r, "alpha", skills=["alpha-one", "alpha-two"], claude=["ax.md"], codex=["ax.toml"])
    sync(r)
    out = sync(r)
    s = summary(out)
    c.ok(s.get("linked") == 0 and s.get("pruned") == 0 and s.get("stubbed") == 0,
         f"a second run was not a no-op: {s}")
    c.ok("nothing to do" in out.stdout, f"a second run still reported work:\n{out.stdout}")
    return r


@case
def drop_in_then_remove_round_trip(c):
    r = make_repo()
    mkprofile(r, "alpha", skills=["alpha-one", "alpha-two"], claude=["ax.md"], codex=["ax.toml"])
    sync(r)
    before = links_in(r, ".agents/skills")
    c.ok("alpha-one" in before and "alpha-two" in before, "a dropped profile's skills did not link")
    c.ok("ax.md" in links_in(r, ".claude/agents"), "a dropped profile's claude agent did not link")
    shutil.rmtree(r / ".agents/profiles/alpha")
    out = sync(r)
    c.ok(summary(out).get("pruned") == 6, f"removing the folder pruned {summary(out).get('pruned')}, want 6"
         " — two skills in two places, and two agents")
    c.ok("alpha-one" not in links_in(r, ".agents/skills"), "a pruned skill is still in .agents/skills")
    c.ok("alpha-one" not in links_in(r, ".claude/skills"), "a pruned skill is still in .claude/skills")
    c.ok("ax.md" not in links_in(r, ".claude/agents"), "a pruned agent is still in .claude/agents")
    mkprofile(r, "alpha", skills=["alpha-one", "alpha-two"], claude=["ax.md"], codex=["ax.toml"])
    sync(r)
    c.ok(links_in(r, ".agents/skills") == before, "putting the folder back did not restore the links")
    return r


@case
def removing_part_of_a_profile_removes_that_part(c):
    r = make_repo()
    p = mkprofile(r, "alpha", skills=["alpha-one", "alpha-two"])
    sync(r)
    shutil.rmtree(p / "skills/alpha-two")
    sync(r)
    c.ok("alpha-one" in links_in(r, ".agents/skills"), "removing one skill removed the other too")
    c.ok("alpha-two" not in links_in(r, ".claude/skills"), "the removed skill is still linked for Claude")
    return r


@case
def a_local_profile_stays_out_of_git(c):
    r = make_repo()
    mkprofile(r, "mine", local=True, skills=["mine-one"])
    mkprofile(r, "shared", skills=["shared-one"])
    sync(r)
    ex = excludes(r)
    c.ok("/.agents/skills/mine-one" in ex, f"a local skill was not excluded from git: {ex}")
    c.ok("/.claude/skills/mine-one" in ex, f"a local skill was not excluded for Claude: {ex}")
    c.ok("/.agents/skills/shared-one" not in ex, "a shared skill was excluded from git, and should not be")
    shutil.rmtree(r / ".agents/.local/profiles/mine")
    sync(r)
    c.ok("/.agents/skills/mine-one" not in excludes(r), "the exclude line outlived the local profile")
    return r


@case
def loose_local_skills_still_work(c):
    r = make_repo()
    mkskill(r / ".agents/.local/skills", "loose-one")
    sync(r)
    c.ok("loose-one" in links_in(r, ".agents/skills"), "a loose local skill did not link")
    c.ok("loose-one" in links_in(r, ".claude/skills"), "a loose local skill did not reach Claude")
    return r


@case
def check_mode_writes_nothing(c):
    r = make_repo()
    sync(r)
    mkprofile(r, "alpha", skills=["alpha-one"])
    out = sync(r, "--check")
    c.ok(summary(out).get("linked") == 2, f"--check did not report the work: {summary(out)}")
    c.ok("alpha-one" not in links_in(r, ".agents/skills"), "--check wrote a link anyway")
    return r


# --- the loader ---------------------------------------------------------------------------------

@case
def a_missing_loader_is_started_with_always_on_rules_by_folder(c):
    r = make_repo()
    p = mkprofile(r, "alpha", skills=["alpha-one"])
    ground = rel(r, mkrule(p, "always-on", "alpha-ground-rules.md"))
    change = rel(r, mkrule(p, "on-demand", "alpha-change-rules.md"))
    out = sync(r)
    loader = r / ".agents/LOADER.md"
    c.ok(loader.is_file(), "no loader was started for a project that had none")
    if not loader.is_file():
        return r
    text = loader.read_text()
    c.ok(ground in always_block(text), "the started loader does not list an always-on rule")
    c.ok(change not in text, "the script placed an on-demand rule, which is the user's call")
    c.ok("started" in out.stdout, f"starting the loader was not reported:\n{out.stdout}")
    c.ok(f"unplaced {change}" in out.stdout, f"the on-demand rule was not reported unplaced:\n{out.stdout}")
    c.ok(f"unplaced {ground}" not in out.stdout, "a placed always-on rule was reported unplaced")
    c.ok(not (r / ".agents/.local/LOADER.md").exists(), "a local loader was started with no local rules")
    return r


@case
def a_hand_written_line_survives_a_second_run(c):
    r = make_repo()
    p = mkprofile(r, "alpha", skills=["alpha-one"])
    ground = rel(r, mkrule(p, "always-on", "alpha-ground-rules.md"))
    change = rel(r, mkrule(p, "on-demand", "alpha-change-rules.md"))
    sync(r)
    text = (r / ".agents/LOADER.md").read_text()
    text = text.replace("<!-- /on-demand table -->",
                        f"| change a thing | `{change}` |\n"
                        "| say it is done | run the `alpha-one` skill |\n<!-- /on-demand table -->")
    text += "\nA note of our own, in our own words.\n"
    (r / ".agents/LOADER.md").write_text(text)
    out = sync(r)
    out2 = sync(r)
    c.ok((r / ".agents/LOADER.md").read_text() == text, "the sync rewrote a loader kept by hand")
    c.ok(ground in always_block(text), "the always-on line was lost")
    for o in (out, out2):
        c.ok(f"unplaced {change}" not in o.stdout, "a rule placed by hand is still reported unplaced")
        c.ok("alpha-one" not in o.stdout.split("changed:", 1)[-1],
             f"an installed skill named in a row was warned about:\n{o.stdout}")
    return r


@case
def a_line_whose_rule_is_gone_is_pruned(c):
    r = make_repo()
    p = mkprofile(r, "alpha")
    ground = rel(r, mkrule(p, "always-on", "alpha-ground-rules.md"))
    solo = rel(r, mkrule(p, "on-demand", "alpha-solo-rules.md"))
    left = rel(r, mkrule(p, "on-demand", "alpha-left-rules.md"))
    right = rel(r, mkrule(p, "on-demand", "alpha-right-rules.md"))
    keep = rel(r, mkrule(p, "always-on", "alpha-keep-rules.md"))
    write_loader(r, always=[ground, keep],
                 rows=[("do the solo thing", f"`{solo}`"),
                       ("do the pair thing", f"`{left}` and `{right}`")])
    for gone in (ground, solo, left):
        (r / gone).unlink()
    out = sync(r)
    text = (r / ".agents/LOADER.md").read_text()
    c.ok(ground not in text, "a list line naming a deleted rule was kept")
    c.ok(keep in always_block(text), "pruning took a list line whose rule is still there")
    c.ok("do the solo thing" not in text, "a row naming only a deleted rule was kept")
    c.ok("do the pair thing" in text and right in text, "a row lost the rule that is still there")
    c.ok(left not in text, "a row still names the deleted one of its two rules")
    c.ok("Our own words, which the sync must leave as they are." in text, "pruning touched the prose")
    for gone in (ground, solo, left):
        c.ok(f"named {gone}" in out.stdout, f"pruning `{gone}` was not reported:\n{out.stdout}")
    again = sync(r)
    c.ok("pruned  .agents/LOADER.md" not in again.stdout, "pruning is not stable on a second run")
    return r


@case
def an_unplaced_rule_is_reported(c):
    r = make_repo()
    p = mkprofile(r, "alpha")
    ground = rel(r, mkrule(p, "always-on", "alpha-ground-rules.md"))
    write_loader(r, always=[ground])
    before = (r / ".agents/LOADER.md").read_text()
    late = rel(r, mkrule(p, "always-on", "alpha-late-rules.md"))
    out = sync(r)
    c.ok(f"unplaced {late}" in out.stdout,
         f"a rule no line names, which never loads, passed in silence:\n{out.stdout}")
    c.ok((r / ".agents/LOADER.md").read_text() == before,
         "the sync placed a rule itself in a loader that already exists")
    return r


@case
def a_named_skill_that_is_not_installed_is_warned(c):
    r = make_repo()
    mkprofile(r, "alpha", skills=["alpha-one"])
    write_loader(r, rows=[("finish the work", "run the `ghost-skill` skill"),
                          ("say it is done", "run the `alpha-one` skill")])
    out = sync(r)
    c.ok("`ghost-skill` skill, which is not installed" in out.stdout,
         f"a line running a skill that is not here passed in silence:\n{out.stdout}")
    c.ok("`alpha-one` skill, which is not installed" not in out.stdout, "an installed skill was warned about")
    c.ok("ghost-skill" in (r / ".agents/LOADER.md").read_text(),
         "the sync deleted a person's line instead of warning about it")
    return r


@case
def a_local_skill_or_path_in_the_shared_loader_is_warned(c):
    r = make_repo()
    mine = mkprofile(r, "mine", local=True, skills=["mine-one"])
    own = rel(r, mkrule(mine, "always-on", "my-own-rules.md"))
    write_loader(r, always=[own], rows=[("finish the work", "run the `mine-one` skill")])
    write_loader(r, always=[own], local=True)
    out = sync(r)
    c.ok(f"names {own}, which only you have" in out.stdout,
         f"a local path in the committed loader passed in silence:\n{out.stdout}")
    c.ok("`mine-one` skill, which only you have" in out.stdout,
         f"a local skill run from the committed loader passed in silence:\n{out.stdout}")
    c.ok(".agents/.local/LOADER.md names" not in out.stdout and
         ".agents/.local/LOADER.md runs" not in out.stdout,
         "the local loader was warned for naming its owner's own files")
    c.ok(".agents/LOADER.md names .agents/.local/LOADER.md" not in out.stdout,
         "the shared loader pointing at the local one was taken for a placement")
    return r


@case
def a_rule_or_skill_declaring_load_when_is_warned(c):
    r = make_repo()
    p = mkprofile(r, "alpha", skills=["alpha-one"])
    old = rel(r, mkrule(p, "on-demand", "alpha-old-rules.md", body="---\nload-when: changing a thing\n---\n\nBody.\n"))
    older = rel(r, mkrule(p, "on-demand", "alpha-older-rules.md", body="---\nwhen: always\n---\n\nBody.\n"))
    skill = p / "skills/alpha-one/SKILL.md"
    skill.write_text("---\nname: alpha-one\ndescription: what it does\nload-when: finishing\n---\n\nBody.\n")
    out = sync(r)
    for carrier in (old, older, rel(r, skill)):
        c.ok(f"{carrier} declares `load-when:`" in out.stdout,
             f"`{carrier}` still carries a loading key and was not told:\n{out.stdout}")
    c.ok(old not in (r / ".agents/LOADER.md").read_text(), "the old key still placed a rule")
    return r


@case
def check_mode_writes_no_loader(c):
    r = make_repo()
    p = mkprofile(r, "alpha")
    mkrule(p, "always-on", "alpha-ground-rules.md")
    out = sync(r, "--check")
    c.ok(not (r / ".agents/LOADER.md").exists(), "--check started a loader anyway")
    c.ok("started" in out.stdout, "--check did not say it would start the loader")
    solo = rel(r, mkrule(p, "on-demand", "alpha-solo-rules.md"))
    loader = write_loader(r, rows=[("do the solo thing", f"`{solo}`")])
    (r / solo).unlink()
    before = loader.read_text()
    out = sync(r, "--check")
    c.ok(loader.read_text() == before, "--check pruned a loader line anyway")
    c.ok(f"named {solo}" in out.stdout, "--check did not say it would prune the line")
    return r


@case
def a_removed_profile_leaves_no_loader_line(c):
    r = make_repo()
    p = mkprofile(r, "alpha", skills=["alpha-one"])
    ground = rel(r, mkrule(p, "always-on", "alpha-ground-rules.md"))
    change = rel(r, mkrule(p, "on-demand", "alpha-change-rules.md"))
    sync(r)
    text = (r / ".agents/LOADER.md").read_text().replace(
        "<!-- /on-demand table -->", f"| change a thing | `{change}` |\n<!-- /on-demand table -->")
    (r / ".agents/LOADER.md").write_text(text)
    shutil.rmtree(r / ".agents/profiles/alpha")
    out = sync(r)
    text = (r / ".agents/LOADER.md").read_text()
    c.ok("profiles/alpha" not in text, f"the loader still names a profile that is gone:\n{text}")
    c.ok("change a thing" not in text, "the row of a deleted profile's rule was kept")
    c.ok(f"named {ground}" in out.stdout and f"named {change}" in out.stdout,
         "the lines that went were not reported")
    c.ok("pruned  .agents/LOADER.md" not in sync(r).stdout, "the loader is not stable after the removal")
    return r


@case
def a_rule_seed_is_never_listed(c):
    r = make_repo()
    p = mkprofile(r, "alpha")
    mkrule(p, "always-on", "alpha-ground-rules.seed.md")
    sync(r)
    c.ok("alpha-ground-rules" not in (r / ".agents/LOADER.md").read_text(),
         "a form was listed in the loader as a live rule")
    return r


# --- conflicts ----------------------------------------------------------------------------------

@case
def a_real_folder_is_never_replaced(c):
    r = make_repo()
    mkprofile(r, "alpha", skills=["alpha-one"])
    mine = mkskill(r / ".agents/skills", "alpha-one", desc="the project's own, written by hand")
    (mine / "SKILL.md").write_text("mine\n")
    out = sync(r)
    c.ok((r / ".agents/skills/alpha-one/SKILL.md").read_text() == "mine\n",
         "a real folder was replaced by a link")
    c.ok("alpha-one" in out.stdout, "the clash with a real folder was not reported")
    c.ok("conflict" in out.stdout.lower(), "a real folder in the way is not reported as a conflict")
    c.ok("alpha" in out.stdout and "profiles/alpha" in out.stdout,
         "the report does not say which profile wanted that name")
    return r


@case
def two_profiles_wanting_one_name_is_reported(c):
    r = make_repo()
    mkprofile(r, "alpha", skills=["shared-name"])
    mkprofile(r, "beta", skills=["shared-name"])
    out = sync(r)
    c.ok("conflict" in out.stdout.lower(), f"two profiles claiming one name passed silently:\n{out.stdout}")
    c.ok("alpha" in out.stdout and "beta" in out.stdout, "the report does not name both claimants")
    target = target_of(r, ".agents/skills/shared-name")
    c.ok(target and "alpha" in target, f"the winner is not the first profile in order: {target}")
    out2 = sync(r)
    c.ok(summary(out2).get("linked") == 0, f"a conflict makes the run flap between the two: {summary(out2)}")
    return r


@case
def a_local_profile_may_not_shadow_a_shared_one(c):
    r = make_repo()
    mkprofile(r, "shared", skills=["same-name"])
    mkprofile(r, "mine", local=True, skills=["same-name"])
    out = sync(r)
    c.ok("conflict" in out.stdout.lower(), "a local profile shadowing a shared one passed silently")
    c.ok("/.agents/profiles/shared/" in os.path.realpath(r / ".agents/skills/same-name"),
         "the local copy won, and a shared profile should come first")
    return r


@case
def an_agent_name_clash_is_reported(c):
    r = make_repo()
    mkprofile(r, "alpha", claude=["runner.md"])
    out = sync(r)
    c.ok("conflict" in out.stdout.lower(),
         f"a profile shadowing core's agent passed silently:\n{out.stdout}")
    c.ok("/core/" in (target_of(r, ".claude/agents/runner.md") or ""),
         "core lost its own agent to a dropped profile")
    return r


@case
def a_skill_without_skill_md_is_reported(c):
    r = make_repo()
    p = mkprofile(r, "alpha")
    mkskill(p / "skills", "alpha-broken", skill_md=False)
    out = sync(r)
    c.ok("alpha-broken" in out.stdout, "a skill folder with no SKILL.md was not mentioned")
    c.ok("SKILL.md" in out.stdout, "the report does not say what is missing")
    c.ok("alpha-broken" not in links_in(r, ".claude/skills") or
         "alpha-broken" in links_in(r, ".claude/skills"),
         "unreachable")
    seen_codex = "alpha-broken" in links_in(r, ".agents/skills")
    seen_claude = "alpha-broken" in links_in(r, ".claude/skills")
    c.ok(seen_codex == seen_claude,
         "a skill with no SKILL.md reached one tool but not the other, without a word")
    return r


@case
def a_stray_file_in_skills_is_not_a_skill(c):
    r = make_repo()
    p = mkprofile(r, "alpha", skills=["alpha-one"])
    (p / "skills/README.md").write_text("notes\n")
    out = sync(r)
    c.ok("README.md" not in links_in(r, ".agents/skills"), "a loose file was linked as if it were a skill")
    return r


@case
def a_link_pointing_somewhere_else_is_retargeted(c):
    r = make_repo()
    mkprofile(r, "alpha", skills=["alpha-one"])
    sync(r)
    dest = r / ".claude/skills/alpha-one"
    dest.unlink()
    dest.symlink_to("../../somewhere/else")
    out = sync(r)
    # Claude's folder mirrors `.agents/skills`, which is itself the link into the profile, so what
    # matters is where the chain ends, not what the first hop says.
    c.ok("/profiles/alpha/" in os.path.realpath(r / ".claude/skills/alpha-one"),
         f"a hand-pointed link still ends up at {os.path.realpath(r / '.claude/skills/alpha-one')}")
    c.ok(summary(sync(r)).get("linked") == 0, "a repointed link is not stable on the next run")
    return r


@case
def a_broken_link_is_cleared(c):
    r = make_repo()
    (r / ".claude/skills").mkdir(parents=True)
    (r / ".claude/skills/ghost").symlink_to("../../.agents/profiles/gone/skills/ghost")
    out = sync(r)
    c.ok(not (r / ".claude/skills/ghost").is_symlink(), "a link to nothing was left in place")
    return r


@case
def a_foreign_link_is_left_alone(c):
    r = make_repo()
    (r / "elsewhere/keeper").mkdir(parents=True)
    (r / "elsewhere/keeper/SKILL.md").write_text("---\nname: keeper\n---\nkeep me\n")
    (r / ".claude/skills").mkdir(parents=True)
    (r / ".claude/skills/keeper").symlink_to("../../elsewhere/keeper")
    sync(r)
    c.ok((r / ".claude/skills/keeper").is_symlink(), "a link someone else made was pruned")
    return r


# --- stress and odd trees -----------------------------------------------------------------------

@case
def many_profiles_and_skills(c):
    r = make_repo()
    for i in range(12):
        mkprofile(r, f"p{i:02d}", skills=[f"p{i:02d}-s{j}" for j in range(8)])
    started = time.time()
    out = sync(r)
    c.note(f"12 profiles x 8 skills in {time.time() - started:.1f}s")
    c.ok(out.returncode == 0, f"a wide tree failed: {out.stderr.strip()[:300]}")
    want = 96 + len(links_in(r, ".agents/core/skills"))
    c.ok(len(links_in(r, ".agents/skills")) == want, f"links: {len(links_in(r, '.agents/skills'))}, want {want}")
    c.ok(summary(sync(r)).get("linked") == 0, "a wide tree is not stable on a second run")
    return r


@case
def names_with_spaces_and_unicode(c):
    r = make_repo()
    mkprofile(r, "alpha", skills=["skill with spaces", "skill-ünïcode"])
    out = sync(r)
    c.ok(out.returncode == 0, f"odd names crashed the run: {out.stderr.strip()[:300]}")
    c.ok("skill with spaces" in links_in(r, ".claude/skills"), "a name with spaces did not link")
    c.ok("skill-ünïcode" in links_in(r, ".claude/skills"), "a name with accents did not link")
    return r


@case
def a_case_only_clash_is_reported(c):
    r = make_repo()
    mkprofile(r, "alpha", skills=["Alpha-One"])
    mkprofile(r, "beta", skills=["alpha-one"])
    out = sync(r)
    insensitive = (r / ".agents/skills/Alpha-One").exists() and (r / ".agents/skills/alpha-one").exists()
    if not insensitive:
        c.note("this filesystem tells the two names apart, so there is nothing to clash")
        return r
    c.ok("conflict" in out.stdout.lower(),
         f"on a filesystem that ignores case, two names became one silently:\n{out.stdout}")
    return r


@case
def a_loop_inside_a_profile_does_not_hang(c):
    r = make_repo()
    p = mkprofile(r, "alpha", skills=["alpha-one"])
    (p / "skills/alpha-one/self").symlink_to("../../../alpha")
    try:
        out = sync(r, timeout=30)
        c.ok(out.returncode == 0, f"a loop inside a profile failed the run: {out.stderr.strip()[:200]}")
    except subprocess.TimeoutExpired:
        c.fails.append("a symlink loop inside a profile hung the run")
    return r


@case
def a_profile_that_is_a_symlink_works(c):
    r = make_repo()
    outside = r / "outside/alpha"
    mkskill(outside / "skills", "alpha-one")
    (r / ".agents/profiles").mkdir(parents=True, exist_ok=True)
    (r / ".agents/profiles/alpha").symlink_to("../../outside/alpha")
    out = sync(r)
    c.ok("alpha-one" in links_in(r, ".agents/skills"), "a profile reached by a link was not read")
    c.ok(summary(sync(r)).get("linked") == 0, "a profile reached by a link is not stable")
    return r


@case
def a_destination_that_cannot_be_written_is_reported(c):
    r = make_repo()
    mkprofile(r, "alpha", skills=["alpha-one"])
    (r / ".claude/skills").mkdir(parents=True)
    os.chmod(r / ".claude/skills", 0o500)
    try:
        out = sync(r, timeout=30)
        c.ok(out.returncode == 0, f"a read-only destination crashed the run:\n{out.stderr.strip()[:400]}")
        c.ok("alpha-one" in out.stdout, "a destination that could not be written was not named")
    finally:
        os.chmod(r / ".claude/skills", 0o700)
    return r


@case
def no_git_still_works(c):
    r = make_repo(git=False)
    mkprofile(r, "alpha", skills=["alpha-one"])
    out = sync(r)
    c.ok(out.returncode == 0, f"a tree with no git failed: {out.stderr.strip()[:300]}")
    c.ok("alpha-one" in links_in(r, ".claude/skills"), "no git meant no links")
    return r


@case
def an_empty_profile_folder_is_harmless(c):
    r = make_repo()
    (r / ".agents/profiles/empty").mkdir(parents=True)
    out = sync(r)
    c.ok(out.returncode == 0, f"an empty profile folder failed the run: {out.stderr.strip()[:200]}")
    return r


@case
def a_file_where_a_profile_should_be_is_ignored(c):
    r = make_repo()
    (r / ".agents/profiles").mkdir(parents=True)
    (r / ".agents/profiles/notes.md").write_text("not a profile\n")
    out = sync(r)
    c.ok(out.returncode == 0, f"a stray file beside the profiles failed the run: {out.stderr.strip()[:200]}")
    return r


@case
def an_agent_with_the_wrong_suffix_is_skipped(c):
    r = make_repo()
    p = mkprofile(r, "alpha")
    (p / "agents/claude").mkdir(parents=True)
    (p / "agents/claude/notes.txt").write_text("x\n")
    sync(r)
    c.ok("notes.txt" not in links_in(r, ".claude/agents"), "a file that is not an agent was linked as one")
    return r


# --- a whole setup, installed from the builder the way SETUP.md says -----------------------------

def install_from_builder(root: Path, profiles_wanted):
    """Copy the engine to its fixed paths, then drop each wanted profile in as a folder."""
    shutil.copytree(BUILDER, root / ".agents/builder", symlinks=True)
    placed = []
    for rel, full in V.walk_builder(str(root), "core"):
        for dest in (V.core_destination(rel) or []):
            target = root / dest
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(full, target)
            placed.append(dest)
            break
    for name in profiles_wanted:
        src = root / ".agents/builder/profiles" / name
        dest = root / ".agents/profiles" / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(src, dest)
        # A form is a question about this repository, so it is answered out of the folder, not left
        # in it. Copying it stands in for the answering a real install does by hand.
        for seed in sorted(dest.rglob("*.seed.*")):
            rel = f"{name}/{seed.relative_to(dest).as_posix()}"
            for target in (V.profile_destination(rel) or []):
                if "/.local/" in target:
                    continue
                (root / target).parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(seed, root / target)
                break
            seed.unlink()
        for leftover in sorted(dest.rglob("*.builder.*")):
            leftover.unlink()
    return placed


@case
def a_whole_setup_installs_from_the_builder(c):
    r = Path(tempfile.mkdtemp(prefix="sync-install-")).resolve()
    subprocess.run(["git", "init", "-q"], cwd=r, check=True)
    wanted = sorted(p.name for p in (BUILDER / "profiles").iterdir() if p.is_dir())
    install_from_builder(r, wanted)

    for must in ("AGENTS.md", "CLAUDE.md", ".agents/CONSTITUTION.md", ".claude/settings.json",
                 ".codex/config.toml", ".agents/README.md", ".agents/SETUP-MAP.html",
                 ".agents/core/skills/project-sync-profiles-and-skills/scripts/sync.py"):
        c.ok((r / must).exists(), f"the engine did not install `{must}`")
    if c.fails:
        return r

    out = sync(r)
    c.ok(out.returncode == 0, f"the first sync of a fresh install failed: {out.stderr.strip()[:400]}")
    c.ok("name(s) in conflict" not in out.stdout,
         f"a clean install out of the box reports conflicts:\n{out.stdout}")

    # Every skill every profile carries is reachable from both tools, by both names.
    want = set()
    for name in wanted:
        folder = r / ".agents/profiles" / name / "skills"
        want |= {s.name for s in folder.iterdir() if s.is_dir()} if folder.is_dir() else set()
    want |= {s.name for s in (r / ".agents/core/skills").iterdir() if s.is_dir()}
    c.note(f"{len(wanted)} profiles, {len(want)} skills")
    for tool in (".agents/skills", ".claude/skills"):
        missing = sorted(want - set(links_in(r, tool)))
        c.ok(not missing, f"{tool} is missing {missing}")
    for name in sorted(want):
        c.ok((r / ".claude/skills" / name / "SKILL.md").is_file(),
             f"`{name}` does not resolve to a SKILL.md through the links")

    # The started loader places every always-on rule a profile brought; each on-demand one waits,
    # reported unplaced, for the step the user picks. No shipped rule or skill carries a loading key.
    loader = (r / ".agents/LOADER.md").read_text()
    for name in wanted:
        for kind in ("always-on", "on-demand"):
            folder = r / ".agents/profiles" / name / "rules" / kind
            for rule in sorted(folder.iterdir()) if folder.is_dir() else []:
                path = rule.relative_to(r).as_posix()
                if kind == "always-on":
                    c.ok(path in always_block(loader), f"the started loader does not list `{path}`")
                else:
                    c.ok(f"unplaced {path}" in out.stdout, f"`{path}` was not reported unplaced")
    c.ok("declares `load-when:`" not in out.stdout,
         "a file the builder ships still carries `load-when:`:\n"
         + "\n".join(l for l in out.stdout.splitlines() if "load-when" in l))

    c.ok(summary(sync(r)).get("linked") == 0, "a fresh install is not stable on a second run")
    return r


@case
def a_profile_can_be_taken_out_of_a_whole_setup(c):
    r = Path(tempfile.mkdtemp(prefix="sync-install-")).resolve()
    subprocess.run(["git", "init", "-q"], cwd=r, check=True)
    wanted = sorted(p.name for p in (BUILDER / "profiles").iterdir() if p.is_dir())
    install_from_builder(r, wanted)
    sync(r)
    before = set(links_in(r, ".claude/skills"))
    victim = "specs" if "specs" in wanted else wanted[0]
    theirs = {s.name for s in (r / ".agents/profiles" / victim / "skills").iterdir() if s.is_dir()}
    kept = sorted(r.joinpath(".agents/profiles", victim).rglob("*"))

    shutil.rmtree(r / ".agents/profiles" / victim)
    out = sync(r)
    after = set(links_in(r, ".claude/skills"))
    c.ok(after == before - theirs, f"deleting `{victim}` left {sorted(after & theirs)} behind")
    c.ok(victim not in (r / ".agents/LOADER.md").read_text(),
         f"the loader still names `{victim}`'s rules after the folder was deleted")
    c.ok(not [p for p in (r / ".claude/skills").iterdir() if not p.exists()],
         "deleting a profile left a link pointing at nothing")

    shutil.copytree(BUILDER / "profiles" / victim, r / ".agents/profiles" / victim)
    for leftover in sorted((r / ".agents/profiles" / victim).rglob("*.seed.*")):
        leftover.unlink()
    for leftover in sorted((r / ".agents/profiles" / victim).rglob("*.builder.*")):
        leftover.unlink()
    sync(r)
    c.ok(set(links_in(r, ".claude/skills")) == before, "putting the folder back did not restore it")
    c.note(f"removed and restored `{victim}` ({len(theirs)} skills, {len(kept)} files)")
    return r


@case
def a_profile_moved_to_local_still_works(c):
    r = Path(tempfile.mkdtemp(prefix="sync-install-")).resolve()
    subprocess.run(["git", "init", "-q"], cwd=r, check=True)
    install_from_builder(r, ["ai-companion"])
    sync(r)
    before = set(links_in(r, ".claude/skills"))
    (r / ".agents/.local/profiles").mkdir(parents=True)
    shutil.move(str(r / ".agents/profiles/ai-companion"), str(r / ".agents/.local/profiles/ai-companion"))
    out = sync(r)
    c.ok(set(links_in(r, ".claude/skills")) == before,
         "moving a profile to the local folder lost its skills")
    c.ok("name(s) in conflict" not in out.stdout,
         f"moving a profile to the local folder reported a conflict:\n{out.stdout}")
    ex = excludes(r)
    for name in sorted(before - set(links_in(r, ".agents/core/skills"))):
        c.ok(f"/.claude/skills/{name}" in ex, f"`{name}` became private but is not excluded from git")
    return r


# --- what survives a compaction ------------------------------------------------------------------

@case
def the_constitution_core_is_carried_into_agents_md(c):
    r = make_repo()
    (r / ".agents/CONSTITUTION.md").write_text(
        "# Constitution\n\nPreamble that may be summarised away.\n\n"
        "<!-- carried -->\n- **A red flag.** Never on your own initiative.\n<!-- /carried -->\n\n"
        "Trailing note.\n")
    (r / "AGENTS.md").write_text("# Test repo\n\n<!-- constitution core -->\n<!-- /constitution core -->\n")
    sync(r)
    text = (r / "AGENTS.md").read_text()
    c.ok("A red flag." in text, "the carried section did not reach AGENTS.md")
    c.ok("Preamble that may be summarised away" not in text,
         "AGENTS.md carries more than the marked section")
    c.ok("Trailing note" not in text, "AGENTS.md carries more than the marked section")
    c.ok(summary(sync(r)).get("linked") == 0, "carrying the core is not stable on a second run")
    return r


@case
def editing_the_constitution_updates_the_carried_copy(c):
    r = make_repo()
    (r / ".agents/CONSTITUTION.md").write_text(
        "# Constitution\n\n<!-- carried -->\n- **First.**\n<!-- /carried -->\n")
    (r / "AGENTS.md").write_text("# Test\n\n<!-- constitution core -->\n<!-- /constitution core -->\n")
    sync(r)
    (r / ".agents/CONSTITUTION.md").write_text(
        "# Constitution\n\n<!-- carried -->\n- **First.**\n- **Second.**\n<!-- /carried -->\n")
    out = sync(r)
    c.ok("- **Second.**" in (r / "AGENTS.md").read_text(),
         "changing the constitution left the carried copy stale")
    c.ok("AGENTS.md" in out.stdout, "the run did not say it had refreshed AGENTS.md")
    return r


@case
def an_agents_md_without_markers_is_left_alone(c):
    r = make_repo()
    (r / ".agents/CONSTITUTION.md").write_text(
        "# Constitution\n\n<!-- carried -->\n- **A red flag.**\n<!-- /carried -->\n")
    mine = "# My project\n\nMy own rules, my own file.\n"
    (r / "AGENTS.md").write_text(mine)
    sync(r)
    c.ok((r / "AGENTS.md").read_text() == mine,
         "an AGENTS.md with no markers was edited anyway")
    return r


@case
def a_constitution_without_markers_is_reported(c):
    r = make_repo()
    (r / ".agents/CONSTITUTION.md").write_text("# Constitution\n\nNothing marked here.\n")
    (r / "AGENTS.md").write_text("# Test\n\n<!-- constitution core -->\n<!-- /constitution core -->\n")
    out = sync(r)
    c.ok("carried" in out.stdout, f"an unmarked constitution passed silently:\n{out.stdout}")
    return r


@case
def a_local_rule_stays_out_of_the_shared_loader(c):
    r = make_repo()
    shared = mkprofile(r, "team")
    mkrule(shared, "always-on", "team-rules.md")
    mine = mkprofile(r, "mine", local=True)
    mkrule(mine, "always-on", "my-own-rules.md")
    other = rel(r, mkrule(mine, "on-demand", "my-other-rules.md"))
    out = sync(r)
    top = (r / ".agents/LOADER.md").read_text()
    local = (r / ".agents/.local/LOADER.md")
    c.ok("team-rules.md" in top, "the shared loader lost a shared rule")
    c.ok(".agents/.local/profiles" not in top,
         "the shared loader names a local path, which every teammate would be told to read")
    c.ok(local.is_file(), "no local loader was started for a local profile's rules")
    if not local.is_file():
        return r
    c.ok("my-own-rules.md" in always_block(local.read_text()), "the local loader is missing a local rule")
    c.ok(f"unplaced {other} — no line in .agents/.local/LOADER.md" in out.stdout,
         f"the local on-demand rule was not reported unplaced in the local loader:\n{out.stdout}")
    c.ok("team-rules.md" not in local.read_text(), "the local loader repeats a shared rule")
    return r


@case
def the_shared_loader_does_not_change_when_local_profiles_go(c):
    r = make_repo()
    shared = mkprofile(r, "team")
    mkrule(shared, "always-on", "team-rules.md")
    mine = mkprofile(r, "mine", local=True)
    mkrule(mine, "always-on", "my-own-rules.md")
    sync(r)
    before = (r / ".agents/LOADER.md").read_text()
    # what a teammate has: everything except the gitignored folder
    shutil.rmtree(r / ".agents/.local")
    sync(r)
    c.ok((r / ".agents/LOADER.md").read_text() == before,
         "the committed loader changed on a machine with no local profiles — it would churn in git")
    c.ok(not (r / ".agents/.local/LOADER.md").exists(), "a local loader was written with nothing in it")
    return r


@case
def the_local_loader_loses_the_line_of_its_last_rule(c):
    r = make_repo()
    mine = mkprofile(r, "mine", local=True)
    own = rel(r, mkrule(mine, "always-on", "my-own-rules.md"))
    sync(r)
    loader = r / ".agents/.local/LOADER.md"
    c.ok(loader.is_file() and own in loader.read_text(), "no local loader was started")
    (r / own).unlink()
    out = sync(r)
    # The loader is its owner's file: it stays, and only the line whose file went goes with it.
    c.ok(loader.is_file(), "the sync deleted a loader someone keeps by hand")
    c.ok(own not in loader.read_text(), "the local loader still names a rule that is gone")
    c.ok(f"pruned  .agents/.local/LOADER.md named {own}" in out.stdout, "the pruned line was not reported")
    return r


@case
def a_loose_skill_dropped_into_the_shared_folder_works(c):
    r = make_repo()
    mkprofile(r, "team", skills=["team-one"])
    sync(r)
    mkskill(r / ".agents/skills", "my-loose-skill", desc="written by hand, brought by no profile")
    out = sync(r)
    c.ok("my-loose-skill" in links_in(r, ".claude/skills"), "a hand-written skill did not reach Claude")
    c.ok((r / ".claude/skills/my-loose-skill/SKILL.md").is_file(), "it does not resolve through the link")
    c.ok("conflict" not in out.stdout, f"a plain drop reported a conflict:\n{out.stdout}")
    for _ in range(2):
        sync(r)
    kept = r / ".agents/skills/my-loose-skill"
    c.ok(kept.is_dir() and not kept.is_symlink(),
         "the sync turned a real folder into a link, or pruned it")
    c.ok(summary(sync(r)).get("linked") == 0, "a loose skill makes the run unstable")
    return r


@case
def a_profile_says_what_it_needs_and_is_told_when_it_is_missing(c):
    r = make_repo()
    p = mkprofile(r, "needy", skills=["needy-one"])
    (p / "PROFILE.md").write_text("# needy\n\n- **Depends on:** `toolbox`\n")
    out = sync(r)
    c.ok("toolbox" in out.stdout and "needy" in out.stdout,
         f"an unmet requirement passed in silence:\n{out.stdout}")
    c.ok("needy-one" in links_in(r, ".claude/skills"),
         "an unmet requirement stopped the rest of the work — it is a warning, not a gate")
    mkprofile(r, "toolbox")
    c.ok("toolbox" not in sync(r).stdout, "the warning outlived the missing profile")
    return r


@case
def a_card_that_needs_no_other_profile_is_fine(c):
    r = make_repo()
    p = mkprofile(r, "alpha")
    (p / "PROFILE.md").write_text("# alpha\n\nWhat it is.\n")
    out = sync(r)
    c.ok("says it depends on" not in out.stdout,
         f"a card with no **Depends on:** was warned about:\n{out.stdout}")
    return r


def run(pattern, verbose):
    rows, kept = [], []
    for fn in CASES:
        if pattern and pattern not in fn.__name__:
            continue
        c = Case(fn.__name__)
        started = time.time()
        root = None
        try:
            root = fn(c)
        except Exception as exc:  # a crash is a failure, not a stopped suite
            c.fails.append(f"raised {type(exc).__name__}: {exc}")
        rows.append((c, time.time() - started))
        if root and not verbose:
            shutil.rmtree(root, ignore_errors=True)
        elif root:
            kept.append(root)
    width = max(len(c.name) for c, _ in rows) if rows else 0
    bad = 0
    for c, secs in rows:
        mark = "ok  " if not c.fails else "FAIL"
        print(f"{mark} {c.name:<{width}}  {secs:4.1f}s")
        for note in c.notes:
            print(f"       note: {note}")
        for f in c.fails:
            print(f"       {f}")
        bad += bool(c.fails)
    print(f"\n{len(rows) - bad}/{len(rows)} cases passed")
    for k in kept:
        print(f"kept {k}")
    return 1 if bad else 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("-k", dest="pattern", help="only cases whose name contains this")
    ap.add_argument("-v", dest="verbose", action="store_true", help="keep the temporary repositories")
    a = ap.parse_args()
    sys.exit(run(a.pattern, a.verbose))
