# Profile: core

The base of the setup, and the one profile every other one is built on. It holds the constitution, how
rules load, where skills live, what the map draws, and the skills that write and check rules and
skills — and nothing about specs. It stays in the builder and is never installed.

Nothing here is true of one project or one stack. Which rules a project ends up with, and which
commands go in its permission list, are questions its forms ask; how a rule gets loaded at all does
not change between projects.

## Installed, not dropped in

**This is the one profile whose files are placed.** Everything else is a folder copied whole to
`.agents/profiles/` and linked by `project-sync-profiles-and-skills`. The engine cannot work that way:
`AGENTS.md`, `CONSTITUTION.md` and `.claude/settings.json` are the files both tools read first, at
fixed paths, and their content is answers about this repository. A form cannot be linked, because its
answer belongs to the project, not to the profile.

The engine is also what makes drop-in possible: `project-sync-profiles-and-skills` ships here.

## All or nothing

**This profile installs whole or not at all**, and declining it means declining the setup: without
`AGENTS.md` and `LOADER.md` nothing tells either tool to read a rule, so every other profile's
rules land in folders no session opens.

The parts are not independently useful:

- **`CONSTITUTION.md`** outranks every other rule and skill in the setup, and carries *Which
  instruction wins*. Without it nothing settles two rules that disagree, and a profile's rules have
  no measure to be judged against.
- **`AGENTS.md` without `LOADER.md`** points at a file that isn't there, and **`LOADER.md` without
  `AGENTS.md`** is a file nothing points at. The two are one mechanism.
- The **settings** carry the permission paths for the skills below; without them every script run asks.
- The **map** and `build_setup_map.py` measure `.agents/core/rules/` and `.agents/skills/` — the folders
  this profile establishes.
- **`project-sync-profiles-and-skills`** carries the only script that links `.agents/skills/` into
  `.claude/skills/`. Without it Codex sees the skills and Claude does not.
- **`project-create-rule-or-skill`** and **`project-resolve-conflicts`** write a rule or skill into
  this loading system and settle two that collide in it. They describe the mechanism this profile is.

## Why the setup's own tooling is here, not with the specs

`project-test-setup` scores whatever a project actually installed — every profile it took, plus
the rules and skills it wrote itself — and reports what costs too many words, what overlaps and what
is left over. `project-resolve-conflicts` settles two that say different things. Both are about the
setup, not about specs, and both get *more* useful as a project adds profiles and edits: that is the
point of keeping them in the base rather than behind a profile a team may not take.

Its spec-process checks are skipped, not failed, where `specs` was not installed.

## What installs

| Block | Lands at |
|---|---|
| `AGENTS.seed.md` | `AGENTS.md` |
| `CONSTITUTION.seed.md` | `.agents/CONSTITUTION.md` |
| `CLAUDE.md` | `CLAUDE.md` |
| `README.seed.md` | `.agents/README.md` |
| `rules/always-on/project-ground-rules.md` | `.agents/core/rules/always-on/` |
| `rules/always-on/project-sensitive-paths-rules.seed.md` | `.agents/core/rules/always-on/project-sensitive-paths-rules.md` |
| `rules/on-demand/project-code-style-rules.seed.md` | `.agents/core/rules/on-demand/project-code-style-rules.md` |
| `rules/on-demand/project-workflow-rules.seed.md` | `.agents/core/rules/on-demand/project-workflow-rules.md` |
| `skills/project-*/` | `.agents/skills/` |
| `agents/claude/runner.md` | `.claude/agents/` |
| `agents/codex/runner.toml` | `.codex/agents/` |
| `map/SETUP-MAP.seed.html` | `.agents/SETUP-MAP.html` |
| `settings/claude-settings.seed.json` | `.claude/settings.json` |
| `settings/codex-config.toml` | `.codex/config.toml` |
| `settings/agents.gitignore`, `settings/claude.gitignore` | `.agents/.gitignore`, `.claude/.gitignore` |

`project-ground-rules.md` was optional under `profiles/general/` before 0.4.0. It is the base — KISS, no
guessing, one thing per change — so it comes with the base. `CONSTITUTION.md` is new in 0.4.0:
the setup-wide half of what was `spec-builder-rules.md`'s *Constitution* section, plus its *Which
instruction wins* row. Changing it is a red flag under its own first principle.

## Required by

Every profile, which is why none lists core. A profile's `## Requires` section names the other
profiles that have to be installed with it; `SETUP.md` installs what a chosen profile requires
without asking again.

## Detection

None, and none is needed: this is the base. `SETUP.md` installs it on every first setup. The only time
it is not installed is when a profile is being added to a project that already has it.

## What the project still has to answer

Its forms, none of which the builder can guess:

- `AGENTS.md` — the project name and one line on what it is; it loads every session
- `.agents/LOADER.md` — not a form but the project's own file: the sync starts it with the always-on
  rules, and each on-demand rule it reports unplaced gets a line at the step it serves, on the user's yes
- `.claude/settings.json` — the permission paths, from the stack profile's *Tool commands* table
- `.agents/README.md` — which of its `<!-- specs -->` sections survive
