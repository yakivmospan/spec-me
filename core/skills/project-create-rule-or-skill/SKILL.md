---
name: project-create-rule-or-skill
description: Use when asked to "write/create/add a rule or skill", "review this rule/skill", "fix/shorten a skill", "where should this rule go", "why didn't the skill trigger", or before changing any rule, loader, skill, agent, template, script or the map under .agents/ — decides what kind a piece of guidance is and where it goes, then writes, reviews and tests it so Claude and Codex load it at the right time. Not for finding conflicts between installed rules and skills (project-resolve-conflicts), a skill missing from Claude's list (project-sync-profiles-and-skills), scoring the whole setup (project-test-setup), READMEs, or code comments.
---

# Project Rule Skill

Guidance works when it loads at the right moment and says one thing in one place. Setups go wrong
between files.

## Non-negotiables

- **Every piece of guidance is one kind** (*The model*), placed one way. A rule is read where a loader
  line names it — on the always-on list, or at a step. A skill runs when a request matches its
  description, or when a line says "at this step, run the `name` skill". Nothing in a file's own
  frontmatter says when it loads, and no line lists a `SKILL.md` to read.
- **One skill, one trigger line** — in a rule of the skill's own profile when that profile already has
  a rule read at that step, otherwise in a loader, which is also where skills from several profiles are
  put in order. Two lines for one skill is an overlap for `project-resolve-conflicts`.
- **Core names no profile's files; a profile names only its own; only the loaders name across
  profiles.** Anything else points at nothing once that profile is gone. What core needs to know about a
  profile — a word-budget exception, its own self-check — goes in that profile's `PROFILE.md`. A skill
  you cannot edit — a plugin's, or one that ships with the tool — gets its trigger line in a loader.
  `AGENTS.md` is the root pointer, not a rule or skill.
- **Precedence lives only in `CONSTITUTION.md`'s *Which instruction wins*.** No rule or skill ranks
  itself against another; a code or docs skill carries the one line `templates/skill-template.md` opens
  with, word for word, and a skill that only reads and reports carries none.
- **No overlap.** Two rules, or two skills, covering the same point is a bug: narrow one, or combine them
  on the user's yes — never a table deciding which wins.
- **Point at a rule by name, never restate it** — the non-negotiables are the one exception.
- **A change leaves the setup better, never stricter than the constitution** — tested (*Testing*)
  unless the user skips it; a skipped test is reported as not tested.

## The model

| | Always-on | On-demand |
|---|---|---|
| **Core** — in every setup | `CONSTITUTION.md` and core's always-on rules | core's on-demand rules; the `project-*` skills |
| **A profile** — chosen at install or added later, for everyone or, from the local loader, only the user | its always-on rules | its on-demand rules and skills |

| The guidance is… | Kind | Placed by |
|---|---|---|
| A fact or constraint every task needs | Always-on rule — only if a task would go wrong without it | a line on the loader's always-on list |
| Facts one kind of work needs, no procedure: a format, a style, a project's conventions | On-demand rule | a line at the loader step it serves |
| A procedure, a checklist, or guidance a request should pull in | Skill | its description — plus one trigger line where work already under way must reach it |
| Deep reading or a run whose raw output shouldn't reach the conversation | Agent, in `.claude/agents/` and `.codex/agents/` | its description, and the rule or skill that hands it work |

**Why the trigger line:** in scored Claude sessions a skill ran mid-work 0 of 6 times on its
description alone and 12 of 12 with a line saying to run it; a line listing its `SKILL.md` was never
opened. Codex is untested.

**Names:** a rule file ends in `-rules.md`; `project-*-rules.md` is a form answered per project, and any
other rule is the same in every project that has it. `project-*` skills manage the setup.

## The budget

| Part | Target |
|---|---|
| Always-on rule | Under 300 words a file. Every word loads every session. By convention it sits in `rules/always-on/`, which is how a new loader places it. |
| On-demand rule | Under 1,000 words |
| Skill description | 70–100 words; Claude's limit is 1,024 characters |
| Skill body | Under 1,000 words; 1,500 at most, examples included. The rest goes to one `reference.md`, only if a run needs it. |

A profile may declare a larger budget for one of its own rules in its `PROFILE.md`'s `**Word budget:**`
line; the check allows only those. `scripts/skill_stats.py` counts skills, `wc -w` rules.

## Setup rules

| Rule | Detail |
|---|---|
| Both tools, always | Only files both read — `AGENTS.md`, `rules/`, a skill, a spec — or a script both run. Never a Claude hook, an `@` import beyond `CLAUDE.md`'s, `.claude/settings.json` or a Codex equivalent; work following an edit is a skill step. |
| Tier | Method and stack files are the same in every project; a sentence depending on one repository's answers — a spec's content, a form value, a setting — never goes in one. |
| Stack profile | Only what the next project on that stack would want unchanged; only `PROFILE.builder.md` names anything outside it. |
| Nothing machine-specific | No absolute paths, user names or hostnames; a script finds the repository root and accepts `--repo-root`. |
| Folders in `.agents/` | Only `rules/`, `skills/` and a developer's `builder/` are plain folders; machinery, personal files and generated output start with a dot. |
| Written to the agent | An instruction or a fact it acts on, never a note to whoever set it up; cite a rule by name. |
| Where it goes | Every project: the builder — the profile whose subject it serves — `testing`, `documentation`, `ai-companion` for how the AI works beside the user — or a new one when no subject fits, `profiles/<stack>/` for one stack's tools. This project only: `.agents/core/rules/` or `.agents/skills/`. Only the user: the same under `.agents/.local/`. A skill's scripts: its own `scripts/`, standard library only. |
| Templates are skeletons | Frontmatter, headings, one worked example per repeating shape, and a pointer at the rule governing each section — never the rule itself. |

## Writing a rule or skill

1. **Read what's there:** `LOADER.md` and the local one, the always-on rules, every skill's description
   (`python3 .agents/skills/project-create-rule-or-skill/scripts/skill_stats.py`), and the two or three files
   nearest this one — done when you can name anything already covering the same point. Something does:
   narrow the new one, or stop and ask whether to extend or merge. Changing a sibling needs the user's yes.
2. **Pin the job down.** In one message, with your inference beside each: the kind (*The model*);
   core or a profile's, and for everyone or only the user; for a skill, which requests should load it
   and which near misses shouldn't, in the user's words, and whether work already under way must reach
   it; what it produces; where it stops. Skip what the request already answers. **Wait for the answers.**
3. **Write to the budget.** A skill starts from `templates/skill-template.md`: triggers first in the
   description, then what it does in one clause, then **Not for** — naming the skill to use instead
   where it is core's or the same profile's, only the work otherwise. Every step ends in something
   checkable; every stop says what to tell the user. `reference.md` has bad and good examples.
4. **Test** (*Testing*), **wire in** (*Wiring*), and **report** its path, each test prompt and what it
   showed, and what was wired in.

## Reviewing, shortening or fixing

1. Read the file and the ones it names. For each point, note the line and a proposed fix:
   1. **Kind and placement** — the right kind; a rule named by a loader line, a skill by at most one
      trigger line.
   2. **Overlap** — nothing else covers the same point; no precedence stated.
   3. **Naming** — per the non-negotiables, and every named path, rule and skill exists.
   4. **Description** (skill) — triggers first, **Not for** per step 3 above.
   5. **Stops** — each says what to tell the user; flag "as appropriate", "handle".
   6. **Restated rules** — a passage copying a rule becomes a pointer.
   7. **Budget** — over it, or content not every run needs.
   8. **Both tools** — nothing one tool alone runs.
   9. **True to its rule** — each stop, exception and condition matches its rule; a new stop is a gate.
   10. **Agrees with its siblings** on every case they share.
2. **Asked only to review:** report per file, most serious first, and stop.
3. **Asked to change it** ("shorten", "fix", "trim"): the request is the go-ahead for findings that
   serve it. Apply those, list the others, then *Testing* and *Wiring*.

Several files changed together: `reference.md`'s *Changing several at once*.

## Diagnosing a skill that didn't load

1. **Find which way it missed.**
   - **A request** that should have matched: compare the user's exact words with the description — a
     missing trigger, or a sibling matching better, is the usual cause. Confirm with *Testing*'s
     trigger half. The fix is the description.
   - **Work already under way** reached the skill's moment and it didn't run: a description doesn't
     fire mid-work. The fix is a trigger line (*Wiring*), not a longer description. Guidance that must
     shape the work itself, whatever the wording, is a rule.
2. **Asked only why:** report the cause and the fix you'd propose — the description, or the line and
   where it goes — and stop.
3. **Asked to fix it:** make that change, then *Testing* and *Wiring*.

## Testing

A fresh agent (a subagent, where the tool has them) with 2–3 realistic prompts: one that should load
the file, one near miss.

- **Trigger:** every skill's description, the loaders and a prompt — what would it load? A wrong pick is
  a description or a line to fix.
- **Follow:** the file and a prompt — its steps, stops, and what it invented.
- **Regression**, for a changed skill: keep the old text, unless git tracks it. Run the same real prompts
  on both — twice each for a skill the user relies on — and have an agent blind to which is which grade
  them. Show the user both outputs; the new is recommended only if it does the same or better.

Fix and rerun, three rounds at most. No fresh agent: test yourself, and say so.

## Wiring

- **A rule** added: place it with a line in a loader — on the always-on list, or at the step it serves,
  where it belongs in the order — in the local loader when it's only the user's, creating `on-demand/`
  if missing. Show the user the line and where it goes, and write it on a yes. Renamed: change its line.
  Removed: the sync drops a line whose file is gone.
- **A skill** added, renamed or removed: run `project-sync-profiles-and-skills`. Nothing goes in a
  loader unless work already under way must reach it; then one trigger line, "at this step, run the
  `name` skill" — in a rule of its own profile read at that step, otherwise in a loader, the local one
  for a local skill. Renamed or removed: change or delete that line; the sync warns about a line naming
  a skill that isn't installed.
- **The map:** unless `project-sync-profiles-and-skills` just ran, run `python3 .agents/core/skills/project-sync-profiles-and-skills/scripts/build_setup_map.py`;
  write a row for anything undescribed.
- **The READMEs:** the section describing what changed — `.agents/README.md` for using the setup, a
  profile's own README for its process. They follow the rules and skills, never the reverse.
- **A changed skill's description** is re-read against its body.
- **From a builder block, where the project keeps `.agents/builder/`:** the same change in its block —
  even when installed only for the user.
- **Offer `project-resolve-conflicts`** when guidance was added, moved or combined.
