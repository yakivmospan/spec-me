# Profiles

A profile is a folder of rules, skills, agents and templates that a project takes whole: dropped into
`.agents/profiles/`, it reaches both Claude and Codex after one sync; deleted, it is gone after the
next. Write one here, in the builder, when the same guidance should reach more than one project.

## Setup

Work in a project with the developer setup (`../SETUP-DEV.md`), so every file is tried on real code
as you write it. Start from the profile nearest to yours and delete what you don't need — from the
repository root:

```bash
cp -R .agents/builder/profiles/testing .agents/builder/profiles/my-profile
```

`testing` is the smallest shape: a card and skills. `kotlin-android` is the shape of a stack,
`code-review` of a profile that only works whole.

## Usage

### The folder

```
profiles/<name>/
├── PROFILE.md                 the card — installed with the folder
├── PROFILE.builder.md         optional — install notes for SETUP.md, never installed
├── rules/always-on/           read every session, once a loader line names it
├── rules/on-demand/           read at the loader step a line places it at
├── skills/<skill>/            SKILL.md, plus its reference.md, templates or scripts
├── agents/claude/  agents/codex/   one subagent as .md for Claude and .toml for Codex, kept in step by hand
└── templates/                 files its skills copy
```

Keep only the folders you use.

### `PROFILE.md` — the card

Installed with the folder. It opens with what the profile is in a sentence or two, then the lines
that apply:

```markdown
# testing

How tests get written here: unit tests in isolation, integration tests across real components, and
manual test plans for the proof no automated test can reach.

- **Take what you want.** Nothing here depends on anything else here.
- **To remove it:** delete this folder and run `project-sync-profiles-and-skills`.
```

- **Who reads it:**
  - **`SETUP.md`:** offers the profile with it, one question per profile.
  - **The sync:** `**Depends on:**`, and warns when a profile named there is missing.
  - **`SETUP.md`:** `**Depends on:**` too, and installs a profile named there along with this one.
  - **`project-test-setup`:** `**Word budget:**` and `**Self-check:**`.
- **Every line and what it does:** `../core/README.seed.md`, *A profile's card*. `specs`' card is the
  fullest example.

### `PROFILE.builder.md` — install notes

Never installed — only `SETUP.md` reads it. Write one only when the setup has to know something a
card can't say:

- **A stack:** `## Detection`, how `SETUP.md` recognises a repository on it; the tool commands a
  permission list allows; the topics its code-style form asks. Shape: `kotlin-android`.
- **Whole or not at all:** *All or nothing*, and why each part is useless without the others, so it
  is offered as one yes or no. Shape: `code-review`.

Neither applies — no file. `testing`, `graphify` and `ai-companion` have none.

### Seeds — forms a project answers

A file whose name holds `.seed.` is a form, not a copy. Its `{{…}}` are questions the agent answers
by reading the codebase at install, never by guessing; a comment at its top says how. It is answered
where it sits, inside the profile, with the marker dropped — `kotlin-code-style-rules.seed.md` becomes
`kotlin-code-style-rules.md` — and from then on it is the project's: a newer builder never
overwrites it, and deleting the profile takes it too.

Make a file a seed only when its content differs per project — a stack's style conventions, the
forge and tracker `code-review` posts to. The method itself stays a plain file, the same everywhere.
How each marker installs: `../README.md`, *Change the builder*.

### What a profile may say

- **Only its own files.** Never another profile's rule or skill — only the loaders name across
  profiles. A skill that works with others lists what is installed and reads it, as `spec-test-writer`
  does.
- **Nothing about one project.** The test: would the next project want this sentence unchanged?
  Anything that isn't goes into a seed.
- **One trigger line for a skill that runs mid-work** — "run the `name` skill", in the profile's own
  rule read at that step.
- **Word budgets** and how to write, review and test each rule and skill: the
  `project-create-rule-or-skill` skill.

### Try it and ship it

1. **The map:** a row for each rule, skill and agent in `../core/map/SETUP-MAP.seed.html`.
2. **Install it into a project** — for everyone, or into `.agents/.local/profiles/` for yourself:

   ```bash
   cp -R .agents/builder/profiles/my-profile .agents/profiles/
   python3 .agents/core/skills/project-sync-profiles-and-skills/scripts/sync.py
   ```

   - **`seed …`:** a form to answer into the project; a form is never linked.
   - **`unplaced …`:** a rule no loader line names; place it, or it never loads.
3. **The mechanical suite:** `python3 .agents/builder/tests/stress_profile_sync.py`.
4. **The changelog:** a line in `../CHANGELOG.md` saying what the profile brings and why.

## Troubleshooting

- **A rule never loads** — no loader line names it. The sync lists it as `unplaced`; place it.
- **The sync reports a name in conflict** — two profiles ship a skill or agent with the same name.
  The first in its order keeps the link — core, the shared profiles by name, then your own — and it
  prints the ways out. Rename one.
- **The sync warns that a profile is missing** — `**Depends on:**` names a profile that isn't installed.
  Install it, or drop the line if the profile works without it.
- **A form's `{{…}}` stayed after install** — the file has no `.seed.` in its name, so it was copied
  as-is. The marker decides, never the braces: the spec templates keep theirs on purpose.

## See also

- `../README.md` — the builder: what lands where, the markers, developing the builder
- `../SETUP.md` — how a profile is offered (Step 4), installed (Step 5) and its forms answered (Step 6)
- `../core/README.seed.md` — *A profile's card*, and how rules, skills and agents are placed
- `project-create-rule-or-skill` — writing and testing a rule or skill
