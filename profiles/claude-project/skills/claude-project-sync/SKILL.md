---
name: claude-project-sync
description: Use when asked for a "snapshot for the claude project", "new Instructions for the claude.ai project", to "link this repo" to a Claude project, to "check the Claude project sync", to go through what the project chat wrote here, when "push" or "pull my ideas" is said in this repository, or when the claude-project rule offers a snapshot — the repository's side of a claude.ai project kept in step: its Instructions to paste, stamped; `.claude-project/SYNC.md` built and checked; the project's writing turned into proposals. Not for a snapshot for any other chat (project-context-snapshot), or syncing profiles (project-sync-profiles-and-skills).
---

# Claude project sync

The repository's side of a Claude project kept in step with it. The project chat moves the files, on
the user's word; this makes its Instructions, keeps `.claude-project/SYNC.md` true, and brings back
what the project decided. What most often goes wrong: Instructions pasted from an old snapshot, so
the project works to rules the repository has since changed.

## Non-negotiables

- **The project's rules and the surrounding file come first — read what `AGENTS.md` loads for this work, if you haven't.**
- **Nothing moves between the two sides from here.** This writes `SYNC.md` and the snapshot; a file
  reaches the project only through the project chat.
- **Every snapshot is made fresh** by `project-context-snapshot` — never edited by hand, never reused.

## Snapshot for the claude project

1. **Run the `project-context-snapshot` skill** with this scope, which it takes as given, and
   `claude-project` as the scope's name: the profiles `core`, `ai-companion` and `specs` where
   installed — `core` meaning the constitution and the rules the loaders name from `.agents/core/`,
   not its skills — without the project overview; the specs' own content reaches the project by
   sync, not in its Instructions. Two more files go into the stamp's fingerprint, though neither is
   condensed: `.agents/LOADER.md`, whose rows say when each rule applies, and this profile's
   `templates/PROJECT-INSTRUCTIONS.md`. Done when it reports its fingerprint.
2. **Add the project's part** — the whole of `templates/PROJECT-INSTRUCTIONS.md`, copied after the
   snapshot's text, with no stamp of its own. Save the result to
   `.agents/.cache/snapshot-claude-project.md`.
3. **Record the stamp** — in `.claude-project/SYNC.md`, the line under the heading reads
   `Instructions: {fingerprint}`, added or replaced. With no `SYNC.md` yet, run *Link this repo*
   first.
4. **Hand it over** — show the whole text, and tell the user: paste it into the project's
   Instructions, replacing what is there; the project notices when it falls behind again.

With no repository — a project that has none — run this in any session that has the builder, taking
the profiles from `.agents/builder/profiles/`, and skip step 3.

## Link this repo

1. Run `python3 .agents/profiles/claude-project/skills/claude-project-sync/scripts/sync_state.py link --check`
   and show what it would add: a row, never synced, for each file under `.specs/`, `docs/` and
   `print/` that has none. Rows already there stay as they are.
2. On a yes, run it without `--check`. Then *Snapshot for the claude project*, unless the user only
   wanted the list.

## Adopt what the project wrote

After the project set up this repository itself ("set up the PC side"), or after a sync brought in
more than a spec or two.

1. **Read what arrived** — every file `SYNC.md` lists, and `NOTES.md` if it came along.
2. **Propose, never apply**, each as one line with the file it came from:
   - a spec whose shape differs from `.specs/README.md` → hand it to the `spec-create` skill to
     correct in place;
   - work the setup has a profile for and this repository lacks — reviews, tests, a stack → install
     that profile;
   - a way of working the project states that no rule here holds → a rule, through the
     `project-create-rule-or-skill` skill.
3. Ask once for all of them, and act only on each yes.

## Check sync

1. Run `python3 .agents/profiles/claude-project/skills/claude-project-sync/scripts/sync_state.py check`.
   It lists files edited after their last change row, files with no row, and rows whose file is gone.
   It reads the day a file was last saved, so an edit the same day as its row is not caught.
2. **For each edit with no row**, propose the row — the date and one sentence on what changed, from
   the file's diff where git has one — and add it on a yes. A new file gets *Link this repo*; a gone
   one is named, for the user to decide on in the project chat.

## "Push" or "pull" said here

Files move only in the project chat, where they can reach both sides. Say so, and that "push ideas",
"pull updates" or "sync" is said there, with this folder connected. Offer *Check sync* meanwhile, so
every edit here has its row before the project looks.

## When the plan stops fitting

- **`project-context-snapshot` is not installed** — say so; the core skill comes with the builder's
  core, so the setup is older than this profile.
- **`SYNC.md`'s rows name another repository** — this one is not the project's only repository; add
  rows for this one only, under its own name.

## Report

What was made or changed — the snapshot's path and fingerprint, the rows added, the rows proposed —
then what the user does next, in one line.
