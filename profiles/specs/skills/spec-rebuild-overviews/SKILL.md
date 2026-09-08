---
name: spec-rebuild-overviews
description: Use after any edit under .specs/, after moving or deleting code a spec's `owns` glob points at, when asked to "run spec-rebuild-overviews" or "rebuild the index", or when a generated file looks stale or a file's owning spec can't be found — rebuilds .specs/INDEX.md, DECISIONS.md and OPEN-QUESTIONS.md and reports drift and warnings. Not for reviewing spec prose (spec-check-style).
---

# Spec Sync

`.specs/INDEX.md`, `DECISIONS.md` and `OPEN-QUESTIONS.md` are generated from the spec tree and its open
changes, on each machine — `.specs/.gitignore` keeps them out of git, so they never conflict. Nothing
rebuilds them on its own. They are helpers: when one disagrees with the specs, the specs
win — regenerate rather than edit.

## Non-negotiables

- **Never fix drift silently.** Report each item with a proposed fix: a dangling `owns` glob may mean a
  deleted feature, which is the user's call.

## Run

```bash
python3 .agents/skills/spec-rebuild-overviews/scripts/build_index.py
python3 .agents/core/skills/project-sync-profiles-and-skills/scripts/build_setup_map.py
```

The second refreshes the setup map, which counts spec words too. `--check` writes nothing; `build_index.py`
exits non-zero on drift only, `build_setup_map.py` also when the map is out of date or a rule or skill is undescribed.

## What it generates

- **`INDEX.md`** — routing from code path to owning spec, open changes with their status, criteria
  checked and tasks done, the spec tree, drift, possibly-stale specs, and counts of violations and gaps.
- **`DECISIONS.md`** — every decision and what it rejected, one section per spec, then what open changes
  add.
- **`OPEN-QUESTIONS.md`** — every open question, one section per spec, then what each open change adds.

## Reading the results

- **Drift** — fails `--check`, structural only; each message and its fix: `reference.md`.
- **Warnings** — never fail. Each message, what it usually means and its fix: `reference.md`.
- **Possibly stale** — owned code has commits after the spec's `updated:`. `spec-sync-with-code` can confirm
  one; its last result shows beside the spec. A broad glob
  shows up often — a reason to ask whether that spec is too broad.
- **Known violations** — `Currently violated:` lines. Kept true per spec-builder-rules' *Keeping it honest*.
- **Pending changes** — any folder under `changes/` directly holding `specs.<path>.md` files; it folds
  in when the user says so.
- **Long Change history rows** (stdout) — past 35 words; rewrite as one sentence (spec-style-rules' *One
  row, one sentence*).
- **Not yet specced** — information only. Spec an area with `spec-create` when a task touches it, not
  because it is listed.

## Report

What changed in the routing table; each drift item with its proposed fix; warnings, briefly; unspecced
areas as a count, for information only.
