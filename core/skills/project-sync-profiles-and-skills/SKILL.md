---
name: project-sync-profiles-and-skills
description: Use after dropping a profile folder into .agents/profiles/, after deleting one, after adding, renaming or removing a skill or rule, after editing .agents/CONSTITUTION.md, or when asked to "sync profiles", "link skills", "relink" or "why can't Claude see my skill" — links every profile's skills and agents where both tools look, prunes links whose source is gone so deleting a folder is the uninstall, keeps both loaders honest, keeps a local profile out of git, and names every clash between two profiles or with a file of your own. Safe any time. Not for writing a rule or skill (project-create-rule-or-skill).
---

# Sync the profiles

A profile is a folder you drop into `.agents/profiles/` — or `.agents/.local/profiles/`, for yourself
alone. Its files stay in it. Both tools need a flat layout (`.claude/skills/<name>/SKILL.md`, one
level) and neither finds a nested folder, so nothing is visible until this links it.

The loaders are the project's own files, edited by hand: `.agents/LOADER.md`, committed, names only
what every clone has; `.agents/.local/LOADER.md` is one person's and adds to it. Each is an always-on
list, then steps, top to bottom — what to read and what to run before each kind of work. The line order
is the order. The script keeps them honest and decides nothing about where a line goes: it starts a
missing loader with the always-on rules placed by their folder, removes a line whose file is gone, and
warns about the rest. Placing is judgement, so it is yours, with the user (*Place what the loaders
miss*).

## Non-negotiables

- **One writer per destination.** A skill reaches `.agents/skills/` from exactly one place — a
  profile, or `.local/`. A single pass then serves Claude from there. Two passes writing one link
  never settle.
- **A real file is never replaced and never removed.** Only links, and the stubs written where
  symlinks are unavailable. Anything else there is someone's, and it is reported, not overwritten.
- **A `.seed.` file is never linked.** Its answer describes this repository, so it belongs to the
  project, not to the profile. Answer it into place as a real file.
- **The script edits no file's contents** beyond starting a missing loader and removing a loader line
  whose file is gone. Every other change to a loader is a line you propose and the user confirms.
- **A clash is never settled quietly.** Where two things want one name, the first in a fixed order
  wins — core, then the shared profiles by name, then your own — and every other claimant is
  printed with the ways out. The order is fixed so that two runs on one tree agree, and so that
  nothing dropped in later can take a name out from under the engine.

## Run it

From the repository root:

```bash
python3 .agents/core/skills/project-sync-profiles-and-skills/scripts/sync.py
python3 .agents/core/skills/project-sync-profiles-and-skills/scripts/build_setup_map.py
```

`--check` reports what would change and writes nothing. `--repo-root PATH` works on another checkout.

## Read what it says

| Line | What to do |
|---|---|
| `linked` / `pruned` | nothing — a link appeared, a deleted folder's link went, or a loader line whose file is gone was removed |
| `stubbed` | symlinks are unavailable here; it wrote a forwarding file instead. Fine, one extra read per use |
| `left alone` in the summary | a name was already taken by a real file; the *Conflicts* block below says by what |
| `conflict …` | read the block — it names everything that wanted that name and what each way out costs |
| `seed … answer it into the project` | a form arrived with a profile. Read the codebase and write the answer to its destination |
| `loader … started` | a loader was missing; it now holds the always-on rules. Every other rule follows as `unplaced` |
| `unplaced …` | a rule no loader line names, so it never loads — *Place what the loaders miss* |
| `… runs the \`x\` skill, which is not installed` | propose installing the profile that brings it, or deleting the line |
| `… which only you have — move that line` | a shared loader line names a local rule or skill; propose moving it to `.agents/.local/LOADER.md` |
| `… declares \`load-when:\`` | a key nothing reads any more; propose deleting it — a loader line decides when |

Only `seed` and the loader warnings need a person. Everything else is the folder telling the truth:
what is there is installed, what is gone is gone.

**One exception, and it is deliberate.** A profile's `.seed.` form is answered out of the folder —
into `.agents/core/rules/`, usually — and that answer describes this repository, so it is the
project's from then on. Deleting the profile takes its skills, agents and loader lines; it does not
take that answer, which keeps loading. Nothing here deletes your writing for you. `project-test-setup`
lists any answer whose profile has gone, under *Answered here, by a profile that is no longer
dropped in*, so the choice is yours and visible.

## Place what the loaders miss

For each `unplaced` rule:

1. **Read the rule and the loader it belongs in** — the shared one for a shared rule, the local one for
   a rule under `.agents/.local/`. Note what work the rule is for, and the steps already there.
2. **Propose one line** — the step, reusing an existing one where the rule serves the same work, or new
   wording in the loader's own style ("Before you…"); and where it goes in the order, named by the line
   it follows. Within a step, shared lines come before local ones. An always-on rule goes on the
   always-on list.
3. **Ask the user**, all the proposals in one message, and **write each on a yes** — the user's
   wording where they change it. A rule the user declines stays unplaced, and the next run says so
   again.

For each skill or local-path warning, propose the fix the table names and apply it on a yes. Never
move, delete or add a loader line without that yes. Where the fix is a trigger line for a skill,
`project-create-rule-or-skill`'s *Wiring* says where one goes.

## Conflicts

Each one is one name, with everything that wanted it, however many those are. Nothing is chosen for
you and nothing of yours is touched — so a run that reports conflicts has still done all the work it
could, and the tree is in a good state either way. Four kinds:

| It says | What happened | What to do |
|---|---|---|
| a real file already has that name | something you wrote sits where a profile's file would go | keep yours and the profile's copy stays unused; or move yours aside and run again; or rename one to keep both |
| more than one profile brings … by that name | two profiles carry the same skill or agent name | rename one to keep both, or delete the profile whose copy you do not want |
| this filesystem ignores case | two names differ only in case, so macOS and Windows see one name where Linux sees two | rename one so they differ by more than case, or the repository behaves differently per machine |
| a skill folder with no `SKILL.md` | half a skill, which would reach one tool and not the other | add `SKILL.md`, or delete the folder |

Report them to the user with the names as printed; do not rename or delete anything to make one go
away without asking, because every way out of the first two changes what someone else sees.

## When a skill still is not seen

Rules load at the start of a session and so do skill descriptions — start a new session before
concluding anything is wrong. Then check the link resolves, and that `.claude/skills/<name>/SKILL.md`
is readable through it.
