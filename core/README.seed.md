<!--
A form. Everything between `<!-- specs -->` and `<!-- /specs -->` describes the specs profile:
keep it if that profile was chosen, delete it if it was not. Then delete every fence and this
comment.
-->

# `.agents/` — the agent setup

The rules, skills and templates Claude and Codex follow in this repository — one setup both tools
read, installed from a builder.

## Setup

A setup prompt installed it. To add a profile later, put the builder back at `.agents/builder/` and run its `SETUP.md` again — it reports
what you have, what you don't, and what you have edited, then installs only what you pick. There is
still no update step for files you already have: a newer builder is compared by hand, or by an AI you
ask. Outside this folder the
setup is `AGENTS.md`, `CLAUDE.md`, `.claude/` and `.codex/`.

```
.agents/
├── CONSTITUTION.md  outranks every other rule and skill; AGENTS.md points here first
├── LOADER.md        this project's own — what to read and run at each step; the sync checks it
├── core/            the engine: its rules, the five project-* skills, the runner agent
├── profiles/        a profile per folder; drop one in, delete one to uninstall
├── skills/          links, so both tools find every profile's skills in one flat folder
├── .local/          yours only, gitignored — its own LOADER.md, profiles/, skills/
├── .cache/          written by scripts on this machine, gitignored
├── builder/         the builder itself — only where its developer set this project up
└── SETUP-MAP.html
```

What you may edit:

- **Your answers** — `AGENTS.md`, `.agents/CONSTITUTION.md`, any `project-*-rules.md`, `.claude/settings.json`
  and the map were installed as forms and answered from this codebase. They're this project's.
- **`CONSTITUTION.md`** — the constitution; changed only as it says.
- **`LOADER.md`** — this project's, edited by hand.
- **Everything else installed** — the other rules, skills, templates and scripts — came from the
  builder. Edit them as you need; a newer builder is compared by hand.
- **`.local/`** — yours alone, gitignored. Whether the rest of the setup is committed: the project's
  workflow rules, where installed.

## Usage

### How rules load

`AGENTS.md` points at `CONSTITUTION.md`, then `LOADER.md`, then `.local/LOADER.md` where it
exists. The loaders are this project's own files, edited by hand: a list of always-on rules, read at
the start of each session, then steps, each saying what to read and what to run before one kind of
work. A rule loads only where a line names it; `always-on/` and `on-demand/` are where it sits by
convention. `project-sync-profiles-and-skills` keeps both loaders honest: it removes a line whose file
is gone, reports a rule no line places — it never loads — and proposes where that rule goes.
`CONSTITUTION.md` and `project-ground-rules.md` come with `core`;
<!-- specs -->`spec-builder-rules.md` and the `spec-*-rules.md` in `on-demand/` come with
`specs`; <!-- /specs -->the rest were chosen at install.
Which instruction wins when two disagree is in `CONSTITUTION.md`'s *Which instruction wins*; a code or docs skill only
repeats the one line `project-create-rule-or-skill`'s *Non-negotiables* allows, which points at `AGENTS.md`. Where a
new rule goes, and how to write one: the `project-create-rule-or-skill` skill.

### How skills get used

Every skill's description is in context from the start of a session. Its body loads when you invoke
it by name — `/my-skill` in Claude, `$my-skill` in Codex — when the tool matches your request to the
description, which isn't guaranteed, or when a line at the step the work has reached says to run it.

### Rule, skill, or a line in the loader

An agent follows guidance only if it has it at the moment it matters, and it can't hold everything at
once. So guidance comes in three kinds, each reaching the agent a different way:

| | Always-on rule | On-demand rule | Skill |
|---|---|---|---|
| **Always in context** | the whole file | its line in a loader | its description |
| **What makes the rest load** | — | the work reaching the step its line sits at | a request matching the description, a trigger line, or you naming it |
| **Holds** | what every task needs | facts for one kind of work: a format, a style, conventions | a job with steps |

**A skill's description doesn't fire in the middle of other work.** Asked to fix a bug, an agent that
ends up editing Kotlin reads the code-style rule at its step, but skips a skill whose description says
"use after changing any Kotlin file". Real Claude Code sessions, scored from their transcripts:

| How the skill was reached | Used mid-work |
|---|---|
| its description only | 0 of 6 |
| a loader row listing its `SKILL.md` | 0 of 4 — never opened |
| a line in its profile's rule saying to run it | 6 of 6 |
| the same line in the loader | 6 of 6 |

A request matching the description did reach it (1 of 1). Tested on Claude only, Opus and Sonnet;
Codex is untested and may differ. Sonnet ran the skill's sweep but skipped its build step; Opus did
both.

**So a skill whose moment comes mid-work gets one trigger line** — "at this step, run the `name`
skill":

- **In a rule of its own profile**, when that profile already has a rule read at that step.
- **In a loader** otherwise, which is also where skills from several profiles running at one step are
  put in order.
- **One skill, one line.** A second is an overlap `project-resolve-conflicts` finds.

**The order is the line order.** An agent follows a loader top to bottom: within a step the line above
comes first, and the shared loader's lines come before your own.

One line of each:

- **Always-on rule**, on the always-on list: ``- `.agents/core/rules/always-on/project-ground-rules.md` ``
- **On-demand rule**, at a step: ``| write or change production code | `.agents/core/rules/on-demand/project-code-style-rules.md` | ``
- **Skill**, triggered at a step: ``| finish code work, before saying it's done | run the `code-clean-kotlin` skill | ``

Where a new piece of guidance goes, and what each kind may cost in words: the
`project-create-rule-or-skill` skill.

### Subagents

A subagent is a fourth kind: a worker the main agent hands one self-contained job to. It starts in
a fresh context — not your conversation — and hands back a summary.

| | Always-on rule | On-demand rule | Skill | Subagent |
|---|---|---|---|---|
| **Always in the main session** | the whole file | its loader line | its description | its description |
| **What starts it** | nothing, it's always read | the work reaching its step | a request matching it, or a trigger line | a handoff: its description matching, or a line saying "hand this to the `x` agent" |
| **Where it runs** | main session | main session | main session | its own fresh context, returning a summary |
| **Holds** | what every task needs | facts for one kind of work | a job with steps | a self-contained job, with its own tools and model |
| **Lives in** | `rules/always-on/` | `rules/on-demand/` | `skills/<name>/` | `agents/claude/<name>.md` and `agents/codex/<name>.toml` |
| **May name** | its own profile's files | its own profile's files | its own profile's files | its own profile's files |

Use one for work that runs on its own, reads a lot, and only its result matters: a review, writing
tests, a test run. Work that needs your decisions on the way, or guidance that shapes the main
conversation, stays a rule or a skill.

Defining one in a profile:

| Part | What goes there |
|---|---|
| `agents/claude/<name>.md` | `name`; `description` — what it does, and "use only from the `y` skill" when it is a step of one; the fewest `tools` it needs; `model`. The body is its instructions. |
| `agents/codex/<name>.toml` | the same agent for Codex, which does not read the `.md` — kept in step by hand |
| `skills:` in the `.md` | optional: skills of its own profile, loaded in full when it starts, so no description has to match |
| Its handoff | a skill of the same profile ("spawn the `x` agent"), or — when its moment comes mid-work — a trigger line in its profile's rule or in a loader |
| Linking and the map | the sync links it into `.claude/agents/` and `.codex/agents/`; give it a row in the map |

**Working across profiles** — two ways, neither naming another profile from inside one:

- **It finds what is installed.** Its instructions say which skills to read — "list
  `.agents/skills/*/SKILL.md` and read those about testing". Removing a profile means it finds less,
  never something missing. Being told to read them, it doesn't wait on a description to match.
- **The loader names them.** A line such as "at this step, hand the job to the `x` agent, with the `y`
  and `z` skills" — the loader may name anything installed.

Never list another profile's skill under `skills:` — it breaks when that profile goes, and what Claude
Code does with a `skills:` entry it cannot find is not documented. Not tested here yet: `skills:`
itself, whether a handoff line is followed mid-work, and whether Codex has anything like `skills:`.

<!-- specs -->
### How a change flows

The specs describe themselves in `.specs/README.md`, for any agent. Here, the skills walk a change
through that process:

1. **Describe it** — `spec-create` writes the spec files, each the whole spec as it should read afterwards,
   with `status: draft` and a `## Change` section saying why.
2. **Plan it, when the work needs it** — `spec-plan` writes `implementation-plan.md` with
   you: the design, then the tasks in order.
3. **Approve it** — you, in chat: each spec file you approve gets `status: approved`, and you're asked whether the rest go too. A spec written from
   code that already exists merges on that yes, unless the change also holds work still to build.
4. **Build it** — when you ask (asking approves a draft), `spec-plan` works through the tasks, stops where a task
   needs you to try it, and changes the plan with you when something turns out different.
5. **Merge it** — `spec-merge` asks once about each unchecked criterion — confirm, drop, or keep the
   change open — marks the spec files `merged`, copies them over their places in `.specs/`, and deletes
   the folder on your yes.

What each file holds, and what changing course mid-way does:
`profiles/specs/rules/on-demand/spec-change-rules.md`.

<!-- /specs -->

### Adding a skill

From the repository root:

```bash
mkdir -p .agents/skills/my-skill
$EDITOR .agents/skills/my-skill/SKILL.md   # frontmatter: name, description
python3 .agents/core/skills/project-sync-profiles-and-skills/scripts/sync.py
python3 .agents/core/skills/project-sync-profiles-and-skills/scripts/build_setup_map.py                      # the map counts skills too
```

If the skill's moment comes in the middle of other work, give it one trigger line too — see *Rule,
skill, or a line in the loader*. Where a skill belongs — here, locally, or in the builder — how to
write it to the shape both tools follow, and how to test it before relying on it: the
`project-create-rule-or-skill` skill.

### Your own rules and skills

```
.agents/.local/
├── profiles/<name>/   a profile only you get — same shape as a shared one
│   ├── rules/always-on/   read every session, once your LOADER.md's always-on list names it
│   ├── rules/on-demand/   read at the step a line in your LOADER.md places it
│   └── skills/            linked for both tools, and kept out of git
├── skills/            a loose skill of your own, from before profiles existed
├── tests/             what an audit of this setup recorded, on this machine
└── LOADER.md          yours, edited by hand — your rules and skills, added to the shared steps
```

A local rule or skill adds to the shared ones and never replaces one with the same name. The link
script lists a local skill's links in `.git/info/exclude`, so they stay out of git even where the setup is committed.

### A profile's card

Every profile has a `PROFILE.md`: what it is, and what the setup needs to know about it. Write the
lines that apply:

| Line | What it does |
|---|---|
| `**Depends on:**` | other profiles it can't work without — the sync warns when one is missing. Every profile depends on `core`, so it is never listed |
| `**To place it:**` | which loader step its rules go at |
| `**To remove it:**` | how to take it out cleanly |
| `**Word budget:**` | a rule of its own allowed more words than the usual limit, e.g. `` `some-rules.md` 1,600 `` |
| `**Self-check:**` | checks `project-test-setup` runs whenever this profile is installed — so a profile brings its own checks and takes them with it when removed |

The sync reads `**Depends on:**`; `project-test-setup` reads `**Word budget:**` and `**Self-check:**`.

### Checking the setup

Ask any agent to "validate the setup". `project-test-setup` reads the rules, loaders, skills, templates
and each profile's own checks, tests them against the constitution, and reports a score, what costs too many words, what
could go and what's left over — each fix as a small draft. It changes nothing but its local findings ledger; you pick what to apply.
It also runs each installed profile's own **Self-check**, from its `PROFILE.md` (*A profile's card*).

Ask to "check rules and skills for conflicts" after installing a rule or skill: `project-resolve-conflicts`
finds two that say different things or compete for the same request, and settles each with you — keep
one, narrow one, or combine them.

Ask to "test whether this rule or skill is actually followed": `project-test-behaviour` walks you
through real sessions one at a time, scores each from its transcript, and compares setups against a
baseline — how the numbers in *Rule, skill, or a line in the loader* were measured.

### The map

[`SETUP-MAP.html`](SETUP-MAP.html) draws the setup: what loads every session, what loads on a
loader row, and what each file costs in words. From the repository root:

```bash
open .agents/SETUP-MAP.html          # macOS — xdg-open on Linux, start on Windows
```

## Troubleshooting

- **A skill doesn't run when you asked for it** — its description matched your request loosely, or
  not at all. Invoke it by name, or ask `project-create-rule-or-skill` why it didn't trigger.
- **A skill never runs in the middle of other work** — a description only answers a request. Give it
  a trigger line at the step it belongs (*Rule, skill, or a line in the loader*).
- **A rule never loads** — no loader line places it. The sync reports it as `unplaced`; place it at
  the step it serves, where the sync skill proposes.
- **Claude or Codex doesn't see a new or local skill** — Claude sees a skill only through its link in
  `.claude/skills/`, and Codex a local skill only through its link in `.agents/skills/`. Run the link script
  above.
- **A new always-on rule isn't followed** — rules load at the start of a session. Start a new one.
- **`build_setup_map.py --check` reports a file that "exists but the map never mentions it"** — a new
  rule or skill has no row in `SETUP-MAP.html`. Add one saying what it's for.

## See also

- the `project-create-rule-or-skill` skill — how rules and skills are placed, written and tested
- `builder/README.md` and `builder/BUILDER-DESIGN.md` — how the builder works and why, where its
  developer keeps it
