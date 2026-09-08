# Profile: specs

Spec-driven development: specs as the memory every agent reads, changes that carry their own spec
files, and the skills, rules, templates and agents that work them. It stays in the builder and is
never installed.

This is what `spec-me` means as a product. Nothing here is true of one project or one stack — the
stack, the commands and the tracker are questions the specs themselves answer; the method does not
change between projects.

## How it arrives

**Dropped in, not installed.** Copy this folder to `.agents/profiles/specs/` and run
`project-sync-profiles-and-skills`; it links the six skills, the always-on rule, the four on-demand rules
and the two agents from where the folder sits. Deleting the folder and running the sync again removes
every one of them. The one thing the folder cannot bring is the spec tree itself — `SETUP.md`'s
Steps 3, 7 and 8 write `.specs/`, because those files describe this repository.

## What it takes from core

No other profile is required. Like every profile it runs on core, which every setup has: the
constitution these rules answer to is core's `CONSTITUTION.md`, and this profile's
`spec-builder-rules.md` adds the two principles that only make sense with specs. Every rule here loads
through core's `AGENTS.md` and `LOADER.md`, every skill here is linked by core's
`project-sync-profiles-and-skills`, and the `runner` these skills hand runs to is core's. Core names
none of this profile's files: `PROFILE.md` declares what core needs to know —
the larger word budgets of `spec-builder-rules.md` and `spec-change-rules.md`, and the checks
`project-test-setup` runs on the spec process.

## All or nothing

**This profile installs whole or not at all.** `SETUP.md` offers it as one choice, not as a list of
skills, and a "yes" installs every file in the tree below.

The parts are not independently useful:

- The **skills** without `spec-builder-rules.md` are six skills nothing invokes. Its *Every task*
  section is what sends a task to `spec-create` in the first place; without it they sit in the list
  waiting for someone to remember them by name.
- The **rules** without the **skills** describe a process no skill performs, and their `LOADER.md`
  rows point at method for work that never starts.
- The **spec templates** without `spec-create` are shapes nothing copies, and `.specs/README.md`
  without the tree is a guide to a folder that does not exist.
- The **agents** read a change's spec files and `.specs/02-tech.md`. With no spec tree, `spec-architect`
  compares designs against nothing and `spec-test-writer` has no acceptance criteria to derive cases from.

A project that wants specs without the process wants `.specs/README.md` and a text editor — the
constitution says a spec reads and changes correctly without any of this.

## What installs

| Block | Lands at |
|---|---|
| `skills/spec-*/` | `.agents/skills/` |
| `rules/always-on/spec-builder-rules.md` | stays here; `LOADER.md`'s always-on list names it where it sits |
| `rules/on-demand/spec-*-rules.md` | stays here; a line in `.agents/LOADER.md` places each at its step, proposed when the sync reports it unplaced |
| `templates/spec-feature.md`, `spec-contract.md`, `implementation-plan.md` | `.agents/profiles/specs/templates/` |
| `templates/spec-0*.builder.md` | nowhere — read by `SETUP.md` to write the root specs |
| `specs/README.md`, `specs/.gitignore` | `.specs/` |
| `agents/claude/{spec-architect,spec-test-writer}.md` | `.claude/agents/` |
| `agents/codex/{spec-architect,spec-test-writer}.toml` | `.codex/agents/` |
| the spec sections of core's `AGENTS.seed.md` and `README.seed.md` | `AGENTS.md`, `.agents/README.md` |

`SETUP.md`'s Step 3 (candidate features), Step 7 (the specs tree) and its `build_index.py` run in
Step 8 belong to this profile too: they are skipped whole when it is declined.

## Detection

None. A stack profile is chosen by reading the repository; this one is chosen by asking the user
whether the team wants spec-driven development. A codebase with no specs in it is not evidence
either way — that is every codebase before the first one.

## What the project still has to answer

Nothing in the profile is a form. What the specs need comes from `SETUP.md`'s own questions — the
project goal, its non-goals, its constraints, and the confirmed feature list — and lands in
`.specs/00-product.md`, `01-architecture.md` and `02-tech.md`, not in a rule here.

The one thing to get right is `02-tech.md`'s Testing section: the framework, the test command, where
tests live and how they are named. That is what the `spec-test-writer` agent reads, and it is wrong in
silence when it is wrong.
