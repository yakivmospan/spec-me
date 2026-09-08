# Builder

The template the agent setup is installed from: `core`, the engine every project gets, and profiles —
folders you drop in for what you want on top. Nothing under `core/` or `profiles/` names a project.
Why it works the way it does is `BUILDER-DESIGN.md`; this file is how.

## Setup

Put this folder at `.agents/builder/` in the project and ask the agent:

> Set up the agent setup here — follow `.agents/builder/SETUP.md`.

`SETUP.md` reads what the project already has, surveys the code, asks what it can't find out and which
profiles you want — for everyone or only for you — installs `core` by the tree below, drops each
chosen profile in whole, answers every form from the codebase, places each rule in the loader on your
yes, and deletes `.agents/builder/`. Run it again with the builder back in place to add a profile.

To develop the builder on a real project, use `SETUP-DEV.md` instead — *Develop the builder*.

## Usage

### Where every file lands

`SETUP.md` installs `core` by this tree, so keep it true when `core/` changes. A profile is not taken
apart: its whole folder goes to one place. How a file installs is its filename marker, in *Change the
builder*.

```
builder/
├── VERSION  CHANGELOG.md  README.md  BUILDER-DESIGN.md   not installed
├── SETUP.md  SETUP-DEV.md                                not installed — the setup prompts
├── CLAUDE-PROJECT-INSTRUCTIONS.md                        not installed — rebuilds a claude.ai project's Instructions
├── builder-dev-rules.builder.md                          linked by SETUP-DEV.md only, to
│                                                         .agents/.local/profiles/builder-dev/rules/always-on/
├── tests/                                                not installed — the builder's own suites
├── core/                                                 the engine, in every project
│   ├── CLAUDE.md                        → CLAUDE.md
│   ├── AGENTS.seed.md                   → AGENTS.md
│   ├── CONSTITUTION.seed.md             → .agents/CONSTITUTION.md
│   ├── README.seed.md                   → .agents/README.md
│   ├── PROFILE.builder.md               not installed — what core needs, read by SETUP.md
│   ├── rules/{always-on,on-demand}/     → .agents/core/rules/…   the project's core rules, mostly forms
│   ├── skills/                          → .agents/core/skills/   the five project-* skills
│   ├── agents/{claude,codex}/           → .agents/core/agents/…
│   ├── tests/                           → .agents/core/tests/    health report, behaviour suite
│   ├── settings/
│   │   ├── claude-settings.seed.json    → .claude/settings.json
│   │   ├── codex-config.toml            → .codex/config.toml
│   │   ├── agents.gitignore             → .agents/.gitignore
│   │   └── claude.gitignore             → .claude/.gitignore
│   └── map/SETUP-MAP.seed.html          → .agents/SETUP-MAP.html
├── profiles/README.md                   not installed — how to write a profile
└── profiles/<name>/                     → .agents/profiles/<name>/, whole
                                           or .agents/.local/profiles/<name>/, only for you
    ├── PROFILE.md                       what it is, what it needs, how to place and remove it
    ├── PROFILE.builder.md               not installed — detection and install notes, read by SETUP.md
    ├── rules/  skills/  agents/  templates/
    └── specs/                           specs only → .specs/README.md and .specs/.gitignore
```

Two loaders are not in the tree: `.agents/LOADER.md` and `.agents/.local/LOADER.md` are the project's
own files. The sync starts one where it is missing and reports every rule no line places; `SETUP.md`
places each on your yes.

The profiles here: `specs` (spec-driven development), `code-review`, `documentation` (comments and
READMEs kept true, with the rule that runs them mid-work), `testing`, `graphify` (dependency
questions through the graphify tool, for projects that use it), `ai-companion` (one person's
preferences for how the AI works beside them — answers, edits, a second look, handovers), and
`kotlin-android`, a stack.

### Update a project

There is no update step. To take a newer builder, put it back at `.agents/builder/` and compare by hand,
or ask an AI to; `python3 .agents/core/tests/health.py` lists every installed file that differs from
the builder while the builder is there, and `CHANGELOG.md` says what changed and why. A copied file can
be replaced; a form's answers are the project's.

### Develop the builder

A project has the user setup — the setup alone — or the developer setup, with `.agents/builder/` and
the developer rule beside it:

- **Switch to the developer setup** — put the builder at `.agents/builder/` and follow `SETUP-DEV.md`.
  On a project already set up, it compares the two once and asks which way each difference goes, then
  links the developer rule.
- **Develop** — every change to an installed file is made in its builder file too, as you work, with
  this tree, the design and the changelog kept current. Nothing to run.
- **Switch back** — copy the builder out, then follow `SETUP-DEV.md` and ask to switch back: it
  removes the developer rule and deletes `.agents/builder/`.

### Change the builder

Edit `core/` or `profiles/`, or develop in a project with the developer setup. Add a line to
`CHANGELOG.md` saying why, and bump `VERSION` for a release.

How a file installs is in its name. The marker is dropped at install, so `AGENTS.seed.md` lands as
`AGENTS.md`:

| Marker | Kind | Install |
|---|---|---|
| *(none)* | copied | byte for byte; an existing different file is left and reported, never overwritten |
| `.seed.` | a form | only if missing, then the project's; its `{{…}}` are questions answered by reading the codebase, never guessed |
| `.builder.` | stays here | never installed — read by a setup prompt |

- **Add a profile or a stack** — `profiles/README.md`: the folder, its card, install notes and forms,
  and how to try it before it ships.
- **Add to core** — only what every project needs, and nothing that names a profile.
- **Change the constitution** — a red flag: only on the user's request, confirmed twice. Edit
  `core/CONSTITUTION.seed.md`; the sync carries its marked core into `AGENTS.md`.
- **Change the map** — word and file counts are `build_setup_map.py`'s, rewritten in place; figures
  and captions are written by hand, and `build_setup_map.py --check` names a rule or skill with no row.

### Change stack

One stack per project; changing it is by hand, from the repository root:

```bash
rm -rf .agents/profiles/kotlin-android .agents/.local/profiles/kotlin-android
python3 .agents/core/skills/project-sync-profiles-and-skills/scripts/sync.py
```

The name is the old stack's. The sync drops its loader lines, and its answered code-style rule goes
with the folder. Then put the builder back, run `SETUP.md` and choose the
new stack. `.specs/02-tech.md` still describes the old one — describe it again with `spec-create`.

### Test the builder

```bash
python3 .agents/builder/tests/stress_profile_sync.py
```

The mechanical suite: installs, links, loaders and conflicts, in throwaway repositories.
`python3 .agents/core/tests/health.py` answers whether the setup in this project works, in one
report. Whether an agent follows any of it takes real sessions: `core/tests/behaviour/README.md`, or
ask for the `project-test-behaviour` skill.

## Troubleshooting

- **`SETUP.md` reports a file it didn't install** — an existing file differed from the builder's, and
  install never overwrites. Compare the two by hand, or ask an AI to.
- **A rule never loads** — no loader line names it; the sync reports it as unplaced. Place it.
- **A change made while developing isn't in the builder** — the developer rule wasn't loaded: it's
  missing from `.agents/.local/profiles/builder-dev/rules/always-on/`, or the session started before it
  was linked. Start a new session; if the link is missing, follow `SETUP-DEV.md` again.

## See also

- `BUILDER-DESIGN.md` — why the builder works the way it does, and what has to hold before release
- `CHANGELOG.md` — what each version changes, and why
