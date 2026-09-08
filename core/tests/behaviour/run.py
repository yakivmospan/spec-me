#!/usr/bin/env python3
"""Ask a real agent to do real things here, at a chosen context load, and score what it did.

The mechanical suite next door proves the files and links are right. This one asks the other
question: with a window that is 10% full, or 75%, or full enough to be compacted, does the agent
still read the constitution, pick the right skill, delegate where a skill says to, and name only
paths that exist?

Every run happens in a throwaway copy of this repository's setup, never in the repository itself.
Every run is written to `results/` with its score, so two runs can be compared and the question
"are we getting better or worse" has an answer instead of an impression.

Usage:
  python3 run.py --agent claude --load 25 --repeats 3
  python3 run.py --agent claude --load 10,50,100          several loads in one go
  python3 run.py --list                                   the cases and what they check
  python3 run.py --dry-run                                exercise the scoring with no agent
  python3 run.py --compare results/A.json results/B.json  what moved between two runs
"""
import argparse
import hashlib
import json
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile
import tomllib
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _repo_root():
    """The repository this suite is measuring, however deep the suite itself sits.

    Asked of git rather than counted in parents, because the same file lives at two depths: the
    builder's source copy and the installed one.
    """
    out = subprocess.run(["git", "-C", str(HERE), "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True)
    return Path(out.stdout.strip()) if out.stdout.strip() else HERE.parents[3]


REPO = _repo_root()

# The install map that `project-test-setup` publishes. Imported rather than restated: a clean install
# built here has to land where a real one lands, and a second copy of that map would drift.
sys.path.insert(0, str(REPO / ".agents/core/skills/project-test-setup/scripts"))
try:
    import validate_inventory as V
except ImportError:  # the engine is not here; only --clean-install needs it
    V = None
SHARED_RESULTS = HERE / "results"
# A run scores one whole tree, so it cannot be split into a shared half and a local one the way a
# loader row can. What it can do is go to the side it belongs to: a run against a tree carrying
# profiles kept to one person recorded that person's rules, and their agent's answers about them,
# so it stays out of the committed folder.
LOCAL_RESULTS = REPO / ".agents/.local/tests/behaviour"


def local_profiles(root: Path):
    base = root / ".agents/.local/profiles"
    return sorted(p.name for p in base.iterdir() if p.is_dir()) if base.is_dir() else []


def results_home(mine):
    return LOCAL_RESULTS if mine else SHARED_RESULTS
# What the setup needs to behave the way it does here. Code is left out: none of these cases read it,
# and copying a whole Android tree for every repeat would cost minutes and prove nothing.
COPIED = [".agents", ".claude", ".codex", ".specs", "AGENTS.md", "CLAUDE.md"]
WORDS_PER_TOKEN = 0.75  # a rough English ratio; only used to size the filler, never to score


def load_config(name):
    with open(HERE / name, "rb") as f:
        return tomllib.load(f)


# --- the throwaway repository -------------------------------------------------------------------

def rule_folders(root: Path, kind):
    """Every always-on or on-demand rule folder a session actually loads from."""
    found = [root / ".agents/core/rules" / kind]
    for base in (root / ".agents/profiles", root / ".agents/.local/profiles"):
        for p in sorted(base.iterdir()) if base.is_dir() else []:
            found.append(p / "rules" / kind)
    return [f for f in found if f.is_dir()]


LOADERS = ((".agents/LOADER.md", False), (".agents/.local/LOADER.md", True))


def always_on_paths(root: Path):
    """Every rule the loaders' always-on lists name, as paths from the repository root.

    A loader that is not there yet is the one the sync would start: every rule in an always-on
    folder of its own kind, shared or local.
    """
    found = set()
    for rel, local in LOADERS:
        loader = root / rel
        if not loader.is_file():
            found.update(p for p in (r.relative_to(root).as_posix()
                                     for folder in rule_folders(root, "always-on")
                                     for r in folder.glob("*.md") if ".seed." not in r.name)
                         if p.startswith(".agents/.local/") == local)
            continue
        text = loader.read_text(errors="replace")
        if "<!-- always-on -->" in text and "<!-- /always-on -->" in text:
            block = text.split("<!-- always-on -->", 1)[1].split("<!-- /always-on -->", 1)[0]
            found.update(re.findall(r"`(\.agents/[^`\s]+\.md)`", block))
    return found


def loads_always(root: Path, rule: Path, always=None):
    """Whether this rule loads every session: one of the loaders' always-on lists names it."""
    listed = always_on_paths(root) if always is None else always
    return rule.relative_to(root).as_posix() in listed


def always_on_words(root: Path):
    """What the rules that load every session cost, in words — the number the budget is about."""
    total, always = 0, always_on_paths(root)
    for folder_kind in ("always-on", "on-demand"):
        for folder in rule_folders(root, folder_kind):
            for rule in folder.glob("*.md"):
                if ".seed." not in rule.name and loads_always(root, rule, always):
                    total += len(rule.read_text(errors="replace").split())
    return total


def place_always(root: Path, lines):
    """Add lines to the end of the shared loader's always-on list, as a person placing a rule would."""
    loader = root / ".agents/LOADER.md"
    text = loader.read_text() if loader.is_file() else ""
    if lines and "<!-- /always-on -->" in text:
        loader.write_text(text.replace("<!-- /always-on -->",
                                       "\n".join(lines) + "\n<!-- /always-on -->", 1))


def inflate(root: Path, target):
    """Grow the always-on rules to about `target` words, and say what was actually reached.

    This is the budget question made testable: the 300-word cap is a number nobody measured, so
    the only way to find out whether a bigger one costs anything is to raise it and look. The
    padding is real guidance moved out of the on-demand rules, not invented text, because that is
    what raising the cap looks like in practice — people move more into always-on. Filler would
    measure an agent's patience with nonsense instead.
    """
    have = always_on_words(root)
    if have >= target:
        return have
    pool = []
    for folder in rule_folders(root, "on-demand"):
        for rule in sorted(folder.glob("*.md")):
            if ".seed." not in rule.name:
                pool.append((rule.stem, rule.read_text(errors="replace")))
    if not pool:
        return have
    dest = root / ".agents/profiles/inflated/rules/always-on"
    dest.mkdir(parents=True, exist_ok=True)
    i, placed = 0, []
    while have < target and i < 200:
        name, body = pool[i % len(pool)]
        chunk = " ".join(body.split()[: max(50, (target - have))])
        out = dest / f"{name}-always-{i}-rules.md"
        out.write_text(f"# {name}, always on\n\n{chunk}\n")
        placed.append(f"- `{out.relative_to(root).as_posix()}`")
        have += len(chunk.split()) + 5
        i += 1
    place_always(root, placed)
    return always_on_words(root)


def plant(root: Path, fixtures):
    """Put a case's own files into the copy before the agent sees it.

    Some questions only exist in a tree that is not this one: two profiles clashing over a name, or
    a rule file carrying an instruction nobody sanctioned. A fixture builds that tree inside the
    throwaway copy, so the case can be about it without this repository ever holding it.
    """
    for f in fixtures or []:
        if "copy" in f:
            src, dest = root / f["copy"], root / f["to"]
            if src.is_dir():
                shutil.copytree(src, dest, symlinks=True)
            elif src.exists():
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dest)
            continue
        target = root / f["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(f.get("content", ""))


def clean_install(root: Path):
    """Build a fresh install straight from the builder, with nothing of this project in it.

    A run against a copy of this repository scores this repository: its answered forms, its local
    profiles, its specs. Useful, and not the same question as "what does a team get out of the
    box". This places the engine and drops every profile in, exactly as `SETUP.md` says, so the
    two numbers can be set beside each other and the gap read as what the project has added.

    The install map comes from `project-test-setup`, so a change to where files land cannot be true
    in one place and false in the other.
    """
    builder = REPO / ".agents/builder"
    if not builder.is_dir() or V is None:
        return None
    shutil.copytree(builder, root / ".agents/builder", symlinks=True)
    for rel, full in V.walk_builder(str(root), "core"):
        for dest in (V.core_destination(rel) or []):
            target = root / dest
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(full, target)
            break
    for folder in sorted((builder / "profiles").iterdir()):
        if not folder.is_dir():
            continue
        dest = root / ".agents/profiles" / folder.name
        shutil.copytree(folder, dest)
        # A form is answered out of the folder at install time. Copying it stands in for the
        # answering a person does, so the destination exists and the tree is shaped right.
        for seed in sorted(dest.rglob("*.seed.*")):
            rel = f"{folder.name}/{seed.relative_to(dest).as_posix()}"
            for target in (V.profile_destination(rel) or []):
                if "/.local/" in target:
                    continue
                (root / target).parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(seed, root / target)
                break
            seed.unlink()
        for only_builder in sorted(dest.rglob("*.builder.*")):
            only_builder.unlink()
    (root / ".agents/.local/profiles").mkdir(parents=True, exist_ok=True)
    return root


def make_sandbox(ablate=None, fixtures=None, inflate_to=None, clean=False):
    """A copy of the setup to run against, optionally with one rule taken out.

    Taking a rule out uses the real uninstall — delete the file, run the sync — so `LOADER.md` loses
    its line and the tree is exactly what a project that never had that rule would have.
    Anything else would measure a broken setup rather than a smaller one.
    """
    root = Path(tempfile.mkdtemp(prefix="behaviour-")).resolve()
    if clean:
        if clean_install(root) is None:
            sys.exit("error: --clean-install needs .agents/builder/, which is not here")
    else:
        for item in COPIED:
            src = REPO / item
            if not src.exists():
                continue
            dest = root / item
            if src.is_dir():
                shutil.copytree(src, dest, symlinks=True)
            else:
                shutil.copy2(src, dest)
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    plant(root, fixtures)
    reached = inflate(root, inflate_to) if inflate_to else None
    if ablate or fixtures or inflate_to or clean:
        if ablate:
            gone = root / ablate
            if gone.is_dir():
                shutil.rmtree(gone)
            elif gone.exists():
                gone.unlink()
        sync = root / ".agents/core/skills/project-sync-profiles-and-skills/scripts/sync.py"
        if sync.is_file():
            subprocess.run([sys.executable, str(sync), "--repo-root", str(root)],
                           capture_output=True, text=True)
    subprocess.run(["git", "add", "-A"], cwd=root, capture_output=True)
    return root, (reached if inflate_to else always_on_words(root))


def digest(path: Path):
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else ""


# --- filling the window -------------------------------------------------------------------------

def filler(root: Path, percent, window):
    """A preamble that makes the agent read real files until the window is about `percent` full.

    Real files, not invented text: what is being measured is whether the rules survive a window
    full of the work someone would actually be doing, and made-up filler does not sit in context
    the way a repository does.
    """
    if percent <= 0:
        return "", []
    target_words = int(window * percent / 100 * WORDS_PER_TOKEN)
    pool = []
    for base in (".specs", ".agents/profiles", ".agents/core"):
        for dirpath, _, files in os.walk(root / base):
            for f in files:
                p = Path(dirpath) / f
                if p.suffix in (".md", ".py", ".toml") and not p.is_symlink():
                    try:
                        pool.append((p, len(p.read_text(encoding="utf-8", errors="replace").split())))
                    except OSError:
                        pass
    random.Random(percent).shuffle(pool)
    picked, total = [], 0
    while total < target_words and pool:
        for p, n in list(pool):
            if total >= target_words:
                break
            picked.append(str(p.relative_to(root)))
            total += n
        if len(picked) > 400:  # a runaway guard, not a real limit
            break
    listing = "\n".join(f"- {p}" for p in picked)
    text = (f"First, read every one of these {len(picked)} files in full. Do not summarise them and "
            f"do not comment on them yet — you will need their content later.\n\n{listing}\n\n"
            "Now, with all of that read, here is the actual request.\n\n")
    return text, picked


# --- running one case ---------------------------------------------------------------------------

def run_agent(spec, prompt, cwd, timeout):
    argv = [a.replace("{prompt}", prompt).replace("{cwd}", str(cwd)) for a in spec["command"]]
    try:
        out = subprocess.run(argv, cwd=cwd, capture_output=True, text=True, timeout=timeout)
    except FileNotFoundError:
        return None, f"{argv[0]} is not installed — see the comment in agents.toml"
    except subprocess.TimeoutExpired:
        return None, f"no answer within {timeout}s"
    return out, None


def parse_events(text, how):
    """Tool calls and the final answer, read as tolerantly as possible.

    Agents disagree about their output shape and change it between versions, so nothing here
    depends on one schema: every JSON object in the stream is searched for anything that looks
    like a tool call, and every piece of assistant text is kept.
    """
    tools, said = [], []
    if how == "text":
        return [], text
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        stack = [obj]
        while stack:
            node = stack.pop()
            if isinstance(node, dict):
                if node.get("type") == "tool_use" and node.get("name"):
                    tools.append({"name": node["name"], "input": node.get("input") or {}})
                if node.get("type") == "text" and isinstance(node.get("text"), str):
                    said.append(node["text"])
                if isinstance(node.get("result"), str):
                    said.append(node["result"])
                stack += [v for v in node.values() if isinstance(v, (dict, list))]
            elif isinstance(node, list):
                stack += [v for v in node if isinstance(v, (dict, list))]
    return tools, "\n".join(said)


# --- the format every agent is scored from --------------------------------------------------------
#
# Whatever produced a session, it is scored from one neutral shape: a JSONL file whose objects are
# {"type": "tool_use", "name": ..., "input": {...}} and {"type": "text", "text": ...}, in order.
# Claude Code's stream-json and a Codex JSON run already parse into it; anything else needs a writer
# of about twenty lines. That is what keeps this suite from being about one vendor.
#
# An optional first line {"type": "meta", "evidence": "self-reported"} says the tool calls were not
# observed but described by the agent itself. Those checks still score, and the report says which
# ones rest on the agent's own word — weaker evidence than a recorded call, and never silently so.

def ingest(path: Path, answer, files_read=(), skills=(), agents=(), self_reported=True,
           files_edited=()):
    """Write one run into the neutral format, marked for how its tool calls were come by."""
    lines = [{"type": "meta", "evidence": "self-reported" if self_reported else "observed"}]
    for f in files_read:
        lines.append({"type": "tool_use", "name": "Read", "input": {"file_path": f}})
    for f in files_edited:
        lines.append({"type": "tool_use", "name": "Edit", "input": {"file_path": f}})
    for name in skills:
        lines.append({"type": "tool_use", "name": "Skill", "input": {"skill": name}})
    for name in agents:
        lines.append({"type": "tool_use", "name": "Agent", "input": {"subagent_type": name}})
    lines.append({"type": "text", "text": answer})
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(l) for l in lines) + "\n")
    return path


def evidence_of(raw):
    for line in raw.splitlines():
        if line.strip().startswith("{"):
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            if obj.get("type") == "meta":
                return obj.get("evidence", "observed")
            break
    return "observed"


OBSERVED_ONLY = {"read_file", "used_skill", "spawned_agent", "file_unchanged"}


# --- scoring a session that already happened ------------------------------------------------------

def project_dir(repo: Path):
    """Where Claude Code keeps this repository's session transcripts.

    The folder is the absolute path with every character that is not a letter or digit turned into
    a dash — so a user name with a dot or an @ in it lands somewhere the obvious guess would miss.
    """
    name = re.sub(r"[^A-Za-z0-9]", "-", str(repo))
    folder = Path.home() / ".claude/projects" / name
    if folder.is_dir():
        return folder
    tail = re.sub(r"[^A-Za-z0-9]", "-", repo.name)
    guesses = sorted((Path.home() / ".claude/projects").glob(f"*{tail}"))
    return guesses[-1] if guesses else folder


def read_transcript(path: Path):
    """Every user prompt, with the tool calls and assistant text that followed it.

    A transcript Claude Code wrote is the same evidence a headless run would print, and it is
    already on disk — so a session someone drives by hand scores exactly like an automated one.
    That is the whole reason this mode exists: a real session needs no CLI to be measured.
    """
    segments, current, compacted = [], None, False
    for line in path.read_text(errors="replace").splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        raw = json.dumps(obj)
        if "isCompactSummary" in raw and '"isCompactSummary":true' in raw.replace(" ", ""):
            compacted = True
        text_parts, tools = [], []
        stack = [obj]
        while stack:
            node = stack.pop()
            if isinstance(node, dict):
                if node.get("type") == "tool_use" and node.get("name"):
                    tools.append({"name": node["name"], "input": node.get("input") or {}})
                if node.get("type") == "text" and isinstance(node.get("text"), str):
                    text_parts.append(node["text"])
                stack += [v for v in node.values() if isinstance(v, (dict, list))]
            elif isinstance(node, list):
                stack += [v for v in node if isinstance(v, (dict, list))]
        # A message the person typed is stored as one plain string, not as text parts.
        message = obj.get("message")
        if isinstance(message, dict) and isinstance(message.get("content"), str):
            text_parts.append(message["content"])
        # A skill's text arrives as a user message marked isMeta; it belongs to the prompt before it.
        if obj.get("type") == "user" and text_parts and not obj.get("isMeta"):
            current = {"prompt": "\n".join(text_parts), "tools": [], "answer": [], "messages": []}
            segments.append(current)
        elif obj.get("type") == "assistant" and current is not None:
            current["tools"] += tools
            current["answer"] += text_parts
            # Kept per message, not merged, because one failure is only visible in the boundaries:
            # an answer chopped into fragments around tool calls reads as nothing to the person,
            # who sees the text and not the tool output.
            if text_parts or tools:
                current["messages"].append({"text": "\n".join(text_parts), "tools": len(tools)})
    for seg in segments:
        seg["answer"] = "\n".join(seg["answer"])
    return segments, compacted


def match_segment(case, segments):
    """The part of the session that answered this case, found by its own first line."""
    key = case["prompt"].strip().splitlines()[0][:60].lower()
    for seg in segments:
        if key in seg["prompt"].lower():
            return seg
    return None


def score_transcript(args):
    cases = load_config("cases.toml")["case"]
    path = Path(args.transcript)
    if str(path) == "latest":
        folder = project_dir(REPO)
        found = sorted(folder.glob("*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)
        if not found:
            sys.exit(f"error: no transcript under {folder}")
        path = found[0]
    mine = local_profiles(REPO)
    home = results_home(mine)
    home.mkdir(parents=True, exist_ok=True)
    keep = home / "transcripts" / f"session-{path.stem}.jsonl"
    keep.parent.mkdir(parents=True, exist_ok=True)
    if not keep.exists():
        shutil.copy2(path, keep)
    segments, compacted = read_transcript(path)
    print(f"transcript {path.name}: {len(segments)} prompt(s), "
          f"compaction {'happened' if compacted else 'did not happen'}\n")
    rows = []
    for case in cases:
        if args.only and args.only not in case["id"]:
            continue
        seg = match_segment(case, segments)
        if seg is None:
            print(f"--   {case['id']:<38} not asked in this session")
            continue
        ctx = {"tools": seg["tools"], "paths": tool_paths(seg["tools"]),
               "answer": seg["answer"], "root": REPO, "before": {},
               "fixtures": case.get("fixture"), "messages": seg.get("messages")}
        row = score_case(case, ctx, answered=bool(seg["answer"].strip()))
        rows.append(row)
        mark = "ok  " if row["score"] == 1 else ("FAIL" if row["score"] == 0 else "part")
        print(f"{mark} {case['id']:<38} {row['score']:5.0%}")
        for c in row["checks"]:
            if not c["pass"]:
                print(f"       missed: {c['label']}")
    if not rows:
        sys.exit("\nnothing scored — run `--prompts` to get the case prompts to paste into a session")
    by_dimension = {}
    for r in rows:
        by_dimension.setdefault(r["dimension"], []).append(r["score"])
    dimensions = {k: sum(v) / len(v) for k, v in sorted(by_dimension.items())}
    record = {
        "when": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "agent": args.agent + " (session)", "agent_version": "",
        "builder": (REPO / ".agents/builder/VERSION").read_text().strip(),
        "repeats": 1, "window": args.window, "dry_run": False, "compacted": compacted,
        "source": path.name, "tree": "this project", "local_profiles": mine,
        "runs": [{"load": "session", "cases": rows, "dimensions": dimensions,
                  "overall": sum(dimensions.values()) / len(dimensions)}],
    }
    home.mkdir(parents=True, exist_ok=True)
    stamp = record["when"].replace(":", "").replace("-", "")
    out = home / f"{stamp}-{args.agent}-session.json"
    out.write_text(json.dumps(record, indent=2) + "\n")
    print()
    print(report(record))
    print(f"\nwritten to {out.relative_to(REPO)}")
    return 0 if all(r["score"] == 1 for r in rows) else 1


def ingest_dir(args):
    """Score runs handed in as JSON, for an agent this cannot start itself.

    One file per case, named `<case-id>.json`, holding what the agent answered and what it says it
    did: {"answer": "...", "files_read": [], "skills_used": [], "agents_spawned": []}. A subagent,
    a colleague's session, or an agent with no scriptable interface all arrive this way, and they
    are scored on exactly the same footing as everything else — with the tool checks marked as the
    agent's own word, because that is what they are.
    """
    folder = Path(args.ingest)
    cases = {c["id"]: c for c in load_config("cases.toml")["case"]}
    mine = local_profiles(REPO)
    home = results_home(mine)
    archive = home / "transcripts" / f"ingested-{args.agent}"
    rows = []
    for handed in sorted(folder.glob("*.json")):
        case = cases.get(handed.stem)
        if case is None:
            print(f"--   {handed.stem:<38} no case by that id")
            continue
        got = json.loads(handed.read_text())
        kept = ingest(archive / f"{case['id']}-take0.jsonl", got.get("answer", ""),
                      got.get("files_read", ()), got.get("skills_used", ()),
                      got.get("agents_spawned", ()), self_reported=True,
                      files_edited=got.get("files_edited", ()))
        raw = kept.read_text()
        tools, answer = parse_events(raw, "jsonl")
        ctx = {"tools": tools, "paths": tool_paths(tools), "answer": answer, "root": REPO,
               "before": {}, "after": {}, "evidence": "self-reported",
               "fixtures": case.get("fixture")}
        row = score_case(case, ctx, answered=bool(answer.strip()))
        row["transcript"] = str(kept.relative_to(home))
        row["takes"] = [dict(row)]
        rows.append(row)
        mark = "ok  " if row["score"] == 1 else ("FAIL" if row["score"] == 0 else "part")
        print(f"{mark} {case['id']:<38} {row['score']:5.0%}")
        for c in row["checks"]:
            if not c["pass"]:
                print(f"       missed: {c['label']}")
    if not rows:
        sys.exit("nothing scored")
    by_dimension = {}
    for r in rows:
        by_dimension.setdefault(r["dimension"], []).append(r["score"])
    dimensions = {k: sum(v) / len(v) for k, v in sorted(by_dimension.items())}
    record = {"when": datetime.now(timezone.utc).isoformat(timespec="seconds"),
              "agent": args.agent, "agent_version": "", "events": "jsonl",
              "builder": (REPO / ".agents/builder/VERSION").read_text().strip(),
              "repeats": 1, "window": args.window, "dry_run": False, "ablated": args.ablate,
              "tree": "this project", "local_profiles": mine,
              "runs": [{"load": "subagent", "cases": rows, "dimensions": dimensions,
                        "overall": sum(dimensions.values()) / len(dimensions)}]}
    home.mkdir(parents=True, exist_ok=True)
    stamp = record["when"].replace(":", "").replace("-", "")
    out = home / f"{stamp}-{args.agent}-ingested.json"
    out.write_text(json.dumps(record, indent=2) + "\n")
    print()
    print(report(record))
    print(f"\nwritten to {out.relative_to(REPO)}")
    return 0


def prompts():
    """The case prompts, ready to paste into a session one at a time."""
    print("Start a fresh session in this repository and send these, one message each, in order.")
    print("Then score what happened with:  python3 run.py --transcript latest\n")
    for case in load_config("cases.toml")["case"]:
        print(f"--- {case['id']}  [{case['dimension']}]")
        print(case["prompt"].strip())
        print()
    return 0


# --- the checks -----------------------------------------------------------------------------------

# A path named in backticks. `@` and `+` are allowed because a home directory can contain them, and
# an agent that answers with absolute paths must not be scored as if it invented every one of them.
PATH_LIKE = re.compile(r"`([\w@+./-]+\.(?:md|py|toml|json|html|kt|ts|gitignore))`")


def resolve_named(root: Path, named: str):
    """Whether a path an answer named exists, however the answer chose to write it.

    An agent may answer with an absolute path, a repository-relative one, or one relative to a
    folder under discussion. All three are the same file to a reader, so all three count here;
    only a path that matches nothing is an invention.
    """
    candidate = Path(named)
    if candidate.is_absolute():
        return candidate.exists()
    if (root / named).exists():
        return True
    # a tail of a real path, e.g. the part after a home directory the regex could not match whole
    parts = Path(named).parts
    for cut in range(len(parts)):
        if (root / Path(*parts[cut:])).exists():
            return True
    # A bare filename is shorthand, not an invention: people and agents write `LOADER.md` for
    # `.agents/LOADER.md`. It counts when a file of that name is somewhere in the setup, and does
    # not when it is nowhere — which is the difference this check exists to find.
    if len(parts) == 1:
        for base in (".agents", ".specs", ".claude", ".codex"):
            folder = root / base
            if folder.is_dir() and any(folder.rglob(parts[0])):
                return True
    return False


def tool_paths(tools):
    out = set()
    for t in tools:
        for value in (t.get("input") or {}).values():
            if isinstance(value, str):
                out.add(value)
            elif isinstance(value, list):
                out.update(v for v in value if isinstance(v, str))
    return out


def check_one(check, ctx):
    kind = check["kind"]
    value = check.get("value", "")
    if kind == "any_of":
        return any(check_one(c, ctx)[0] for c in check["checks"]), "any of"
    if kind == "read_file":
        hit = any(value in p for p in ctx["paths"])
        return hit, f"read {value}"
    if kind == "used_skill":
        # Two ways an agent reaches a skill, and both count. It can invoke it as a tool, or it can
        # open `skills/<name>/SKILL.md` and follow it — the file is in the repository, after all.
        # Counting only the tool call scored a run as a miss when it had read the skill and obeyed
        # the one rule that skill alone asks for.
        blob = json.dumps(ctx["tools"])
        # `also` carries the names this skill used to have. Without it a rename silently voids every
        # recorded session: the run did reach the skill, under the name it had that day, and a
        # history that resets on every rename cannot answer "are we getting better or worse".
        names = [value] + list(check.get("also") or [])
        for name in names:
            invoked = f'"{name}"' in blob or f"/{name}/" in blob
            opened = any(f"skills/{name}/SKILL.md" in p for p in ctx["paths"])
            if invoked or opened:
                under = "" if name == value else f" (as `{name}`)"
                return True, (f"used {value}{under}" if invoked
                              else f"read {value}'s SKILL.md and followed it{under}")
        return False, f"used {value}"
    if kind == "spawned_agent":
        for t in ctx["tools"]:
            if t["name"] in ("Agent", "Task") and value in json.dumps(t.get("input") or {}):
                return True, f"spawned {value}"
        return False, f"spawned {value}"
    if kind == "answer_matches":
        # `also` holds what the thing used to be called, for the same reason `used_skill` has it:
        # an answer recorded before a rename named it correctly, and should not now read as wrong.
        for pattern in [value] + list(check.get("also") or []):
            if re.search(pattern, ctx["answer"], re.I):
                return True, f"answer matches /{pattern}/"
        return False, f"answer matches /{value}/"
    if kind == "answer_lacks":
        return not re.search(value, ctx["answer"], re.I), f"answer lacks /{value}/"
    if kind == "file_unchanged":
        # Two ways to know, and the run decides which is available. A sandbox run hashes the file
        # before and after, which is proof. Anything scored from a transcript instead asks whether
        # an editing tool ever named the file — which is what a transcript actually records, and
        # what a reader would look for. Falling back to a hash with nothing to compare it against
        # used to fail this check on every run that did not take one, marking the most important
        # safety case in the suite as broken when the agent had behaved perfectly.
        before = ctx.get("before") or {}
        after = ctx.get("after") or {}
        if value in before:
            return after.get(value, digest(ctx["root"] / value)) == before[value], f"{value} untouched"
        editors = ("edit", "write", "notebookedit", "multiedit")
        for t in ctx["tools"]:
            if t["name"].lower() in editors and value in json.dumps(t.get("input") or {}):
                return False, f"{value} was edited"
        return True, f"{value} untouched — nothing edited it"
    if kind == "answer_in_one_message":
        # Every message that carries text but is not the one holding the answer, and is too short
        # to be an answer itself. Those are the "about to do X" fragments: they cost the reader a
        # message and tell them nothing, because they cannot see what the tools returned.
        messages = ctx.get("messages")
        if messages is None:
            return True, "not a recorded session, so message boundaries are unknown"
        spoke = [m for m in messages if m["text"].strip()]
        limit = int(check.get("value") or 40)
        fragments = [m for m in spoke[:-1] if len(m["text"].split()) < limit]
        return (not fragments,
                "the answer came in one message" if not fragments
                else f"{len(fragments)} message(s) said only what was about to happen")
    if kind == "no_invented_path":
        # A case's own fixtures existed while the agent ran, whatever the tree looks like now. A
        # run scored later — or scored against this repository rather than the copy — would
        # otherwise punish the agent for naming a file the case itself put there.
        planted = {f["to"] if "copy" in f else f["path"] for f in ctx.get("fixtures") or []}
        named = set(PATH_LIKE.findall(ctx["answer"]))
        bad = sorted(p for p in named
                     if not resolve_named(ctx["root"], p)
                     and not any(p == q or q.endswith(p) or p.endswith(q) for q in planted))
        return not bad, ("named only paths that exist" if not bad
                         else f"named {len(bad)} path(s) that do not exist: {bad[:3]}")
    return False, f"unknown check `{kind}`"


def score_case(case, ctx, answered=True):  # noqa: C901 — one place, so the rules are in one place
    """Every check, plus the rule that an agent which said nothing passes nothing.

    Without that rule a case built only from `answer_lacks` and `file_unchanged` scores full marks
    when no agent ran at all: the checks are satisfied by silence. `--dry-run` prints exactly that
    number as the case's floor, so a case whose floor is 100% is visibly worthless and gets fixed.
    """
    rows = []
    for check in case.get("check", []):
        passed, label = check_one(check, ctx)
        weak = ctx.get("evidence") == "self-reported" and check["kind"] in OBSERVED_ONLY
        rows.append({"kind": check["kind"], "label": label + (" (agent's own word)" if weak else ""),
                     "pass": bool(passed), "evidence": "self-reported" if weak else "observed"})
    if not answered:
        for r in rows:
            r["pass"] = False
            r["label"] += " (no answer)"
    got = sum(r["pass"] for r in rows)
    return {"id": case["id"], "dimension": case["dimension"], "checks": rows,
            "score": got / len(rows) if rows else 0.0}


# --- a whole run -----------------------------------------------------------------------------------

def one_pass(case, spec, percent, window, timeout, dry, archive=None, take=0, ablate=None,
             inflate_to=None, clean=False):
    """One agent session, scored — and its raw output kept.

    The expensive half of this suite is starting an agent; the cheap half is deciding whether what
    it did was right. Keeping the raw output splits the two: a check can be rewritten and every
    session ever recorded re-scored against it, with no agent and no cost. See `--rescore`.
    """
    root, rule_words = make_sandbox(ablate=ablate, fixtures=case.get("fixture"),
                                    inflate_to=inflate_to, clean=clean)
    try:
        watched = [c["value"] for c in case.get("check", []) if c["kind"] == "file_unchanged"]
        before = {v: digest(root / v) for v in watched}
        preamble, picked = filler(root, percent, window)
        prompt = preamble + case["prompt"]
        raw = ""
        if dry:
            tools, answer, error = [], "", "dry run: no agent was started"
        else:
            out, error = run_agent(spec, prompt, root, timeout)
            raw = out.stdout if out else ""
            tools, answer = parse_events(raw, spec.get("events", "text")) if out else ([], "")
            if out and not answer:
                answer = raw[-4000:]
        after = {v: digest(root / v) for v in watched}
        ctx = {"tools": tools, "paths": tool_paths(tools), "answer": answer,
               "root": root, "before": before, "after": after,
               "fixtures": case.get("fixture")}
        row = score_case(case, ctx, answered=dry or bool(answer.strip()))
        row["files_preloaded"] = len(picked)
        row["always_on_words"] = rule_words
        row["error"] = error
        row["digests"] = {"before": before, "after": after}
        if archive and raw:
            archive.mkdir(parents=True, exist_ok=True)
            tag = f"-without-{Path(ablate).name}" if ablate else ""
            kept = archive / f"{case['id']}-load{percent}{tag}-take{take}.txt"
            kept.write_text(raw)
            row["transcript"] = str(kept.relative_to(home))
        return row
    finally:
        shutil.rmtree(root, ignore_errors=True)


def run(args):
    agents, cases = load_config("agents.toml"), load_config("cases.toml")["case"]
    if args.agent not in agents and not args.dry_run:
        sys.exit(f"error: no agent `{args.agent}` in agents.toml — have {', '.join(agents)}")
    spec = agents.get(args.agent, {"command": ["true"], "events": "text"})
    version = ""
    if not args.dry_run and spec.get("version"):
        got = subprocess.run(spec["version"], capture_output=True, text=True)
        version = got.stdout.strip() if got.returncode == 0 else "unknown"
    wanted = [c for c in cases if not args.only or args.only in c["id"]]
    started = datetime.now(timezone.utc).isoformat(timespec="seconds")
    mine = [] if args.clean_install else local_profiles(REPO)
    home = results_home(mine)
    archive = home / "transcripts" / (started.replace(":", "").replace("-", "") + "-" + args.agent)
    out_runs = []
    for percent in args.load:
        rows = []
        for case in wanted:
            takes = [one_pass(case, spec, percent, args.window, args.timeout, args.dry_run,
                              archive=archive, take=i, ablate=args.ablate,
                              inflate_to=args.inflate, clean=args.clean_install)
                     for i in range(args.repeats)]
            mean = sum(t["score"] for t in takes) / len(takes)
            rows.append({"id": case["id"], "dimension": case["dimension"], "score": mean,
                         "takes": takes})
            mark = "ok  " if mean == 1 else ("FAIL" if mean == 0 else "part")
            print(f"{mark} load {percent:>3}%  {case['id']:<38} {mean:5.0%}"
                  + (f"   {takes[0]['error']}" if takes[0].get("error") else ""))
        by_dimension = {}
        for r in rows:
            by_dimension.setdefault(r["dimension"], []).append(r["score"])
        dimensions = {k: sum(v) / len(v) for k, v in sorted(by_dimension.items())}
        out_runs.append({"load": percent, "cases": rows, "dimensions": dimensions,
                         "overall": sum(dimensions.values()) / len(dimensions) if dimensions else 0})
    record = {
        "when": started,
        "agent": args.agent, "agent_version": version,
        "events": spec.get("events", "text"),
        "builder": (REPO / ".agents/builder/VERSION").read_text().strip(),
        "repeats": args.repeats, "window": args.window, "dry_run": args.dry_run,
        "ablated": args.ablate, "inflated_to": args.inflate,
        "tree": "a clean install from the builder" if args.clean_install else "this project",
        "local_profiles": mine,
        "runs": out_runs,
    }
    home.mkdir(parents=True, exist_ok=True)
    stamp = record["when"].replace(":", "").replace("-", "")
    path = home / f"{stamp}-{args.agent}{'-dry' if args.dry_run else ''}.json"
    path.write_text(json.dumps(record, indent=2) + "\n")
    print()
    print(report(record))
    print(f"\nwritten to {path.relative_to(REPO)}")
    # Results land outside this folder whenever the repository has local profiles, so the path to
    # print has to be worked out rather than assumed. It used to assume, and every real run ended
    # in a traceback after the work was already done and saved.
    try:
        where = path.relative_to(HERE)
    except ValueError:
        where = os.path.relpath(path, HERE)
    print(f"compare with: python3 run.py --compare {where} <another>")
    return 0 if all(r["overall"] == 1 for r in out_runs) else 1


def rescore(path, events):
    """Run today's checks against sessions recorded earlier. No agent, no cost.

    This is what makes an agent CLI a one-off rather than a dependency: once a session is recorded,
    every later change to a check can be tested against it, and a number from months ago can be
    recomputed on the same footing as today's.
    """
    record = json.loads(Path(path).read_text())
    home = Path(path).resolve().parent
    cases = {c["id"]: c for c in load_config("cases.toml")["case"]}
    missing, rescored = 0, 0
    for run in record["runs"]:
        for row in run["cases"]:
            case = cases.get(row["id"])
            if case is None:
                continue
            fresh = []
            for take in row.get("takes", [row]):
                kept = take.get("transcript")
                if not kept or not (home / kept).is_file():
                    missing += 1
                    fresh.append(take)
                    continue
                raw = (home / kept).read_text()
                tools, answer = parse_events(raw, events)
                if not answer:
                    answer = raw[-4000:]
                digests = take.get("digests") or {}
                ctx = {"tools": tools, "paths": tool_paths(tools), "answer": answer,
                       "root": REPO, "before": digests.get("before", {}),
                       "after": digests.get("after", {}), "evidence": evidence_of(raw),
                       "fixtures": case.get("fixture")}
                scored = score_case(case, ctx, answered=bool(answer.strip()))
                scored["transcript"] = kept
                scored["digests"] = digests
                fresh.append(scored)
                rescored += 1
            row["takes"] = fresh
            row["score"] = sum(t["score"] for t in fresh) / len(fresh)
        by_dimension = {}
        for r in run["cases"]:
            by_dimension.setdefault(r["dimension"], []).append(r["score"])
        run["dimensions"] = {k: sum(v) / len(v) for k, v in sorted(by_dimension.items())}
        run["overall"] = (sum(run["dimensions"].values()) / len(run["dimensions"])
                          if run["dimensions"] else 0)
    record["when"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    record["rescored_from"] = str(Path(path).name)
    stamp = record["when"].replace(":", "").replace("-", "")
    out = home / f"{stamp}-{record['agent'].split()[0]}-rescored.json"
    out.write_text(json.dumps(record, indent=2) + "\n")
    print(f"re-scored {rescored} recorded session(s) against today's checks"
          + (f"; {missing} take(s) had nothing recorded" if missing else ""))
    print()
    print(report(record))
    print(f"\nwritten to {out.relative_to(REPO)}")
    print(f"compare with the original: python3 run.py --compare "
          f"{Path(path).name} {out.name}")
    return 0


def report(record):
    lines = [f"## {record['agent']} {record['agent_version']} — builder {record['builder']}"
             f" — {record['repeats']} take(s) per case", ""]
    if record.get("tree"):
        mine = record.get("local_profiles") or []
        where = (f" It carries {len(mine)} profile(s) kept to one person"
                 f" ({', '.join(f'`{m}`' for m in mine)}), so this run stays under `.agents/.local/`"
                 " and is not committed." if mine else
                 " Nothing in it belongs to one person, so this run is committed with the setup.")
        lines += [f"**Tree: {record['tree']}.**{where}", ""]
    reached = {c["takes"][0].get("always_on_words") for r in record["runs"] for c in r["cases"]
               if c.get("takes")} - {None}
    if reached:
        lines += [f"**Always-on rules: {max(reached)} words.** That is what every session pays "
                  "before a word of the task. Compare runs at different sizes to see what the "
                  "budget is buying.", ""]
    if record.get("ablated"):
        lines += [f"**Without `{record['ablated']}`.** Compare with a run that had it: what the"
                  " score loses is what that file was buying.", ""]
    dims = sorted({d for r in record["runs"] for d in r["dimensions"]})
    loads = [r["load"] for r in record["runs"]]
    lines.append("| Dimension | " + " | ".join((f"{l}% load" if isinstance(l, int) else str(l)) for l in loads) + " |")
    lines.append("|---" * (len(loads) + 1) + "|")
    for d in dims:
        cells = [f"{r['dimensions'].get(d, 0):.0%}" for r in record["runs"]]
        lines.append(f"| {d} | " + " | ".join(cells) + " |")
    lines.append("| **overall** | " + " | ".join(f"**{r['overall']:.0%}**" for r in record["runs"]) + " |")
    weak = sum(1 for r in record["runs"] for c in r["cases"]
               for t in c.get("takes", [c]) for k in t.get("checks", [])
               if k.get("evidence") == "self-reported")
    if weak:
        lines += ["", f"**{weak} check(s) rest on the agent's own account of what it did**, not on a"
                  " recorded tool call — a subagent's steps are not written down anywhere readable."
                  " Treat those as weaker evidence than the rest, and use a real session"
                  " (`--transcript`) when the number has to be relied on."]
    if record["dry_run"]:
        weak = sorted({c["id"] for r in record["runs"] for c in r["cases"] if c["score"] == 1})
        lines += ["", "This was a dry run, so these are **floors**: what each case scores when no"
                  " agent runs at all. A real run has to beat its floor to mean anything."]
        if weak:
            lines += ["", "**Worthless as written** — full marks with no agent, so they measure"
                      " nothing: " + ", ".join(f"`{w}`" for w in weak)]
    return "\n".join(lines)


def compare(a_path, b_path):
    a, b = (json.loads(Path(p).read_text()) for p in (a_path, b_path))
    print(f"A  {a['when']}  {a['agent']} {a['agent_version']}  builder {a['builder']}"
          f"  — {a.get('tree', 'this project')}")
    print(f"B  {b['when']}  {b['agent']} {b['agent_version']}  builder {b['builder']}"
          f"  — {b.get('tree', 'this project')}\n")
    a_by = {r["load"]: r for r in a["runs"]}
    b_by = {r["load"]: r for r in b["runs"]}
    print("| Load | Dimension | A | B | Move |")
    print("|---|---|---|---|---|")
    for load in sorted(set(a_by) & set(b_by)):
        for d in sorted(set(a_by[load]["dimensions"]) | set(b_by[load]["dimensions"])):
            x = a_by[load]["dimensions"].get(d, 0)
            y = b_by[load]["dimensions"].get(d, 0)
            arrow = "same" if abs(y - x) < 0.005 else ("better" if y > x else "WORSE")
            print(f"| {load}% | {d} | {x:.0%} | {y:.0%} | {arrow} {y - x:+.0%} |")
    for load in sorted(set(a_by) & set(b_by)):
        x, y = a_by[load]["overall"], b_by[load]["overall"]
        print(f"| {load}% | **overall** | **{x:.0%}** | **{y:.0%}** | **{y - x:+.0%}** |")
    only = (set(a_by) ^ set(b_by))
    if only:
        print(f"\nnot in both runs, so not compared: {sorted(only)}% load")
    return 0


def listing():
    for case in load_config("cases.toml")["case"]:
        print(f"{case['id']}  [{case['dimension']}]")
        for c in case.get("check", []):
            inner = c.get("checks")
            detail = " or ".join(f"{i['kind']} {i.get('value','')}" for i in inner) if inner \
                else f"{c['kind']} {c.get('value', '')}"
            print(f"    - {detail}")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--agent", default="claude", help="a table name in agents.toml")
    ap.add_argument("--load", default="0", help="context fill before the request, e.g. 25 or 10,50,100")
    ap.add_argument("--repeats", type=int, default=3, help="takes per case; agents are not deterministic")
    ap.add_argument("--window", type=int, default=200000, help="the model's context in tokens")
    ap.add_argument("--timeout", type=int, default=900, help="seconds for one take")
    ap.add_argument("--only", help="only cases whose id contains this")
    ap.add_argument("--list", action="store_true", help="print the cases and their checks")
    ap.add_argument("--dry-run", action="store_true", help="start no agent; exercise the machinery")
    ap.add_argument("--compare", nargs=2, metavar=("A", "B"), help="two result files")
    ap.add_argument("--transcript", help="score a session Claude Code already wrote; `latest` finds it")
    ap.add_argument("--prompts", action="store_true", help="print the case prompts to paste by hand")
    ap.add_argument("--rescore", help="re-run today's checks against a run's recorded sessions")
    ap.add_argument("--ingest", metavar="DIR", help="score results handed in as <case-id>.json files")
    ap.add_argument("--clean-install", action="store_true",
                    help="score a fresh install from the builder instead of this project's tree")
    ap.add_argument("--inflate", type=int, metavar="WORDS",
                    help="grow the always-on rules to about this many words first, to find out "
                         "what the budget is actually buying")
    ap.add_argument("--ablate", metavar="PATH",
                    help="take this file out of the copy first, so a run says what it was worth")
    args = ap.parse_args()
    if args.list:
        sys.exit(listing())
    if args.prompts:
        sys.exit(prompts())
    if args.ingest:
        sys.exit(ingest_dir(args))
    if args.rescore:
        agents = load_config("agents.toml")
        saved = json.loads(Path(args.rescore).read_text())
        events = saved.get("events") or agents.get(args.agent, {}).get("events", "stream-json")
        sys.exit(rescore(args.rescore, events))
    if args.compare:
        sys.exit(compare(*args.compare))
    if args.transcript:
        sys.exit(score_transcript(args))
    args.load = [int(x) for x in str(args.load).split(",")]
    sys.exit(run(args))


main()
