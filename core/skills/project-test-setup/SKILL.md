---
name: project-test-setup
description: Use only when asked to "validate the setup", "review the setup", "review our spec setup", "audit the agent setup", "check the setup against the constitution", "score the setup", "find leftovers in the setup", or "how many words or tokens does the setup load" — reads the rules, loaders, skills, templates, agents, each profile's own checks and the builder, tests them against the constitution, measures their load, reports a score, findings and drafted proposals, editing only its ledger. Not for writing or reviewing one rule or skill (project-create-rule-or-skill), conflicts between rules and skills (project-resolve-conflicts), or a spec's prose or structure.
---

# Project Validate

A read-only review of the whole setup against its constitution: what breaks it, what contradicts, what
costs too many words, what could go, and what's left over. One report; the user decides what changes.

## Non-negotiables

- **Only on direct request, and read only.** Edit nothing but the findings ledger — not even an obvious
  typo; it goes in the report.
- **The constitution is the measure, never the subject.** Never question a principle, and never
  propose anything stricter than it allows. A rule asking for more than it allows is reported as a
  proposal to bring that rule in line.
- **A constitution conflict is the constitution contradicting itself or its source, the `.agents/builder/core/CONSTITUTION.seed.md` form, when present, or wording that reads
  against its own intent** — reported on its own with the exact wording to change, never a principle to
  weaken or tighten. Applying one follows the constitution's own rule: show it, ask, and ask once more.
- **Every finding cites `file:line` and quotes the words.** Open the file; when unsure it's a problem,
  it goes under *Questions*.
- **Every proposal needs a reason and a small draft** — a principle it serves, a contradiction or
  leftover it removes, or words it saves. "Cleaner" alone isn't a reason.
- **Deliberate repetition isn't a finding:** a skill's non-negotiables restate rules on purpose.
- **Same depth every run.** Every run starts from `scripts/validate_inventory.py` and the findings ledger
  `.agents/.local/tests/validate-findings.md`, where it exists; rechecks every open finding; asks every question in
  `reference.md` of every comparison *Checks* lists, and runs every installed profile's self-check; rates by its priority examples; and scores the ledger by *Report*'s
  formula. Settled choices come only from `.agents/.local/tests/validate-accepted.md`: one met there goes under
  *Considered and left alone*, never a finding.

## 1. Read

1. Run `python3 .agents/skills/project-test-setup/scripts/validate_inventory.py` from the repository root —
   load, budgets, profile files against installed files, retired names, missing paths, links, the map check.
   Its output, the ledger and `reference.md` are every reader's starting point. Then
   `.agents/CONSTITUTION.md`, the constitution — the measure for everything below.
2. **The setup:** `AGENTS.md`, `CLAUDE.md`, both loaders, `.agents/core/rules/`, every dropped-in
   profile's `PROFILE.md`, `rules/` and `templates/`, every shared `.agents/skills/*/SKILL.md` with its
   `reference.md` and scripts, `.claude/agents/`, `.codex/agents/`, `.claude/settings.json`,
   `.codex/config.toml`, `.agents/README.md`, and `.agents/.local/` except its backups.
3. **Each installed profile's self-check:** the checks its `PROFILE.md` lists under **Self-check**,
   and the files they name. Where a check says to skip when its files
   aren't there, skip it and say so in the report rather than scoring it as missing.
4. **The builder**, when `.agents/builder/` is there: `BUILDER-DESIGN.md`,
   `CHANGELOG.md`, `README.md`, `SETUP.md`, `SETUP-DEV.md` and `profiles/`. Its README's tree maps each block to where it's installed:
   a block without a marker should match its installed file; a `.seed.` block is a form the project
   answered, so it differs by design; a `.builder.` block is never installed; a profile skill is
   installed only where it was chosen.

Rules and skills define the process; `.agents/README.md`, and any README a profile's self-check names,
describe it and follow them. With subagents, give each check below to its own reader with this skill, the inventory output and
its check's name — nothing else, no hints about recent work — and merge what they find; without, work
through the checks in order. After the report, update the ledger: each open finding's status, and each new
finding with the next id in its area under its `## Findings`; then run the inventory with `--write-score`
so its `## Score` shows the current state.

## 2. Checks

### Constitution
Walk each scenario, and say whether the setup honours every principle — naming the file and line that
breaks one:
- A person confirms work by hand, with no test: is it complete, with nothing warning, failing or
  pushing for a test?
- Someone changes their mind mid-way: does the flow absorb it without ceremony?
- Anywhere: a warning that something won't work without stricter checks, or proposed enforcement?

### Consistency
Every one of these, quoting both sides:
- `.agents/README.md` against both loaders, `CONSTITUTION.md` and `project-create-rule-or-skill`'s model.
- **The loaders** against what is installed: a rule no line places, which never loads (the inventory's
  *Unplaced, so never loaded*); a line naming a file or a skill that isn't there; a shared line naming something only
  one person has; a line listing a `SKILL.md` to read instead of saying to run the skill; and one skill
  run from two lines — a rule and a loader, or two of either.
- Every skill's description and sections against `project-create-rule-or-skill`'s template; every agent against the
  rules it reads.
- When the builder is there: its `README.md` tree, `SETUP.md` and `SETUP-DEV.md` against `profiles/`; each
  `.seed.` form against its installed file by shape; the inventory's differing profile files.
- These terms, each with one meaning everywhere: done, the user, red flag, shared and local.

Rules and skills conflicting with each other are `project-resolve-conflicts`'s: offer it when you see one.

### Load
The inventory's numbers and budget flags, never an estimate:
- **Every session:** `AGENTS.md`, `CLAUDE.md`, the loader, the always-on rules, and every shared
  skill's description — and the local layer's on top.
- **A piece of work:** each number a profile's **Self-check** defines, counted as it says from the
  every-session number, in words.

Flag a rule over its budget — `project-create-rule-or-skill`'s, or the larger one its profile's
`PROFILE.md` declares under **Word budget** — a shared skill over that skill's budget, a rule restated
outside non-negotiables, always-on content only some tasks need, and a generated file read every
session that could be read on demand.

### Simplification
Steps, fields, statuses, warnings or files nobody would miss; two skills or rules doing one job;
instructions an agent would follow the same way without them. For each, say what breaks if it goes —
if nothing does, it's a proposal.

### Leftovers
Open every lead in the inventory's *Retired names*, *Paths named*, *Skill links* and *Map check*, then:
- A skill, rule, template, script or field named in prose that doesn't exist.
- A retired name still used as current: a name the builder's CHANGELOG or decisions record as replaced. History — a CHANGELOG entry, an *Instead of*
  or *Replaced* line — is fine.
- A skill with no link in `.claude/skills/`, or a link for something gone; whatever
  `build_setup_map.py --check` reports about the map — never read the map's HTML for this.
- Script warnings or code paths for removed concepts.
- An unmarked block with no installed file, or the reverse.

### Profiles' self-checks
Each installed profile's **Self-check** list, from *Read*. A finding goes in the area its check names,
rated by the profile's priority examples where it gives some.

## Report

Plain words, in this order. Keep it to what matters: group small leftovers into one finding.

1. **Profiles** — what is installed, what is not, what the project has edited since, and what is the
   project's own rather than a profile's. `validate_inventory.py`'s *Profiles* section computes it;
   `SETUP.md`'s Step 0.1 reads this section when adding a profile.
2. **Score** — a table with a score for each area: Follows the constitution, Consistency, Load,
   Simplification, Leftovers. Each is 10 − 3 per Critical − 2 per High − 1 per Medium − 0.25 per Low
   finding still open in the ledger in that area, at least 1, rounded half up; **Overall** = (3 ×
   constitution + the other four) ÷ 7, to one decimal. Copy it from the inventory's *Score from the
   ledger*, never work it out: new findings and fixes count from the next run, once in the ledger. With
   no ledger yet, work it out from this run's findings; a finding counts in one area only.
3. **Ledger** — each open finding's id and its status now: still open, fixed, or accepted.
4. **Coverage** — for each check, what was compared, from its list in *Checks* and each profile's
   self-check, and anything not reached or skipped, with why.
5. **Constitution conflicts** — the constitution contradicting itself or its source, the builder's `CONSTITUTION.md` block, when present, or reading against its
   own intent, with the exact wording to change — or "none".
6. **Findings** new this run, by priority, Critical first — a table: #, priority, area, `file:line`, what's wrong
   (quoted), impact on real work. Priority per `reference.md`'s examples.
7. **Proposals**, in the priority of what they fix, only for findings worth fixing:

   ```markdown
   #### P1: {title}
   - **Fixes:** #{n} ({priority})
   - **Why it's needed:** {the principle, contradiction, leftover or cost it removes, and what goes wrong without it}
   - **Saves:** {words per session or per change, or "clarity only"}
   - **Risk:** {what could get worse}
   - **Draft:** {the smallest before and after}
   ```
8. **Considered and left alone** — what looked wrong but is deliberate, one line each.
9. **Questions** — what needs the user; a question already answered in `validate-accepted.md` isn't one.

End by asking which proposals to apply, and stop. Applying them later is a change to the setup:
`project-create-rule-or-skill` first.
