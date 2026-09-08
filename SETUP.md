# Setup

A prompt. With this folder at `.agents/builder/` — dropped in, or unpacked from the builder's zip —
tell the agent: *Set up the agent setup here — follow `.agents/builder/SETUP.md`.* It installs the
setup, then deletes the builder. Run it again later, with the builder dropped back in, to add a
profile to a project that already has it: Step 0 works out which run this is.

You are setting up an agent setup on this repository with **spec-me-builder**, in
`.agents/builder/`. Everything installs as a profile. `core`
is the base — how rules load, where skills live, the map, and the skills that write and check rules and
skills — and goes in on every first setup without being asked for. Spec-driven development is
`specs`, offered whole in Step 4 and requiring core; the steps that build a spec tree are
skipped when it is declined. Work through the steps in order.
**Never overwrite a file you did not generate. Never fill a placeholder with a plausible guess.**

One hard rule that overrides everything below: if you cannot find evidence for a value, leave the
placeholder and ask. A confidently wrong `AGENTS.md` poisons every future session in this repo.

You do all of it: copying each profile's files into place, linking
skills — and the judgement: which profile, which skills, and every answer that has to come from
reading this codebase. Where each block lands is the tree in `.agents/builder/README.md`; nothing
else maps it.

---

## Step 0 — Read the project's state

Work out which state this repository is in, say which and why in chat — two or three lines for
*Empty* or *Foreign*; an add run's report is Step 0.1's. Read whatever you need; install and change
nothing **in this step**.

**`.agents/builder/` is not evidence** — it is this builder, dropped in to run this prompt, and it is
there in every state. Ignore it, everything inside it, and `.git/`. A profile's own `rules/`,
`skills/` and `CLAUDE.md` under `.agents/builder/profiles/` belong to the builder, not to this
project.

**Evidence is a file that instructs an agent**: `AGENTS.md`, `CLAUDE.md`, `.cursor/rules/`,
`.github/copilot-instructions.md`, `GEMINI.md` or another tool's equivalent; a `.claude/` or `.codex/`
holding rules, skills or agents; anything under `.agents/` other than `builder/`; and a populated
`.specs/` or `docs/adr/`, which Step 7 must not walk over. Settings alone are not evidence — a
`.claude/` holding only `settings.json`, or a `.cursor/` with no `rules/`, instructs nobody. **The
list is examples, not a closed set**: judge by whether an agent would read the file as instructions.

**Is it ours?** Nothing is stamped on the project to say so — run the builder's own inventory from the
repository root and read its *Profiles* section:

```bash
python3 .agents/builder/core/skills/project-test-setup/scripts/validate_inventory.py
```

Its second line answers the question outright: **this setup is installed here: yes / no**. It counts
files sitting at paths only this setup uses — `.agents/CONSTITUTION.md`, `.agents/LOADER.md`,
`.agents/core/rules/`, `.agents/skills/` and `.agents/profiles/`.

Two things it deliberately does not do. It does not judge by **contents**: a project edits its
installed rules and skills and runs versions behind this builder, so a file that came from a profile
may share not one byte with the copy here — where it sits and what it is called do not change. And it
does not count **ordinary names**: `AGENTS.md`, `CLAUDE.md`, `.claude/settings.json` and a
`.gitignore` are files any project may write for itself, so a repository with a hand-made `AGENTS.md`
is Foreign, not ours.

Read that line and the profile lists under it; ignore the rest of the report here — its other sections
measure a setup that is not installed yet, and its exit code means nothing.

| Evidence | State | Route |
|---|---|---|
| None | **Empty** | A first setup: Steps 1-9 in order |
| Some, and *this setup is installed here* says no | **Foreign** — someone else's setup, or an earlier hand-made one | A first setup, on top: Steps 1-9, never overwriting what is there |
| *This setup is installed here* says yes, and `.agents/core/rules/` and `.agents/skills/` are both there | **Ours** | An add run: Step 0.1 |
| *This setup is installed here* says yes, but `.agents/core/rules/` or `.agents/skills/` is missing | **Half-removed** — the setup was deleted or only partly restored | Say so, treat it as Foreign, and ask before writing anything |

**No row fits** — stop and say what you found, rather than taking the nearest one. A first setup run
over something you did not understand is the one mistake here that cannot be undone from the report.

**Foreign is not a problem to solve.** Read it so you don't contradict it, report it, and never
rewrite or reinterpret what it says — and never convert another tool's setup into this one. Step 5
leaves an existing file and reports it rather than overwriting it, and Step 6 names the one thing
that may be added to a kept `AGENTS.md`: the lines telling an agent to read the loaders. Nothing else
is added to a foreign file.

### Step 0.1 — It is already set up

The engine is here, so most of what a first setup does is done. **Adding a profile is not a setup
run**: a profile is a folder. Say this plainly, then stop unless the user wants one of the two things
below.

```bash
cp -R <the profile folder> .agents/profiles/
python3 .agents/core/skills/project-sync-profiles-and-skills/scripts/sync.py
```

That links its skills, rules and agents where both tools look. Deleting the folder and running the
same command again is the uninstall. Removing part of it is deleting a subfolder. Editing it is
editing a text file in their repository — nothing here will ever overwrite it.

Run the sync now and read what it reports. Two lines need a person:

- **`seed …`** — a profile brought a form. Answer it into the project by reading the codebase, as
  Step 6 describes, and write the answer as a real file at its destination. Never link a form.
- **`unplaced …`** — a rule no loader line names, so it never loads. Place it as
  `project-sync-profiles-and-skills`'s *Place what the loaders miss* says: propose the step and where
  in the order, and write the line on the user's yes. The other loader warnings go the same way.

Then run `project-resolve-conflicts` and settle what it finds with the user: a profile doing a job
another installed profile already does — two test-writing agents, say — surfaces there.

Only these two bring the user back to this prompt:

1. **A form needs re-answering**, or was never answered — Step 6.
2. **`specs` was just dropped in and there is no `.specs/`** — Steps 3, 7 and 8 build the
   spec tree, which is the one thing a folder cannot bring with it.

## Step 1 — Survey the repository

Detect, do not assume:

- **Stack** — read the manifest: `package.json`, `build.gradle.kts`, `build.gradle`, `pom.xml`,
  `pyproject.toml`, `Cargo.toml`, `go.mod`, `Gemfile`, `*.csproj`. Note the project name field.
- **Commands** — the real ones. `scripts` in `package.json`; Gradle task names; `Makefile` or
  `justfile` targets; and above all the CI pipeline file, which is usually ground truth for what
  actually builds, tests, and lints.
- **Test framework** — from what is installed and imported, not from ecosystem defaults.
- **Structure** — top-level source directories, skipping build output, `node_modules`, `.git`.
- **Conventions** — skim 3-5 representative source files. Only record a convention you can point at
  actual code for. Do not import best practices this codebase does not follow.
- **Existing documentation** — `README.md`, `docs/**`, `ARCHITECTURE.md`, `CONTRIBUTING.md`, or
  similar. Read these before asking Step 4's questions — a goal, non-goal, or constraint already
  written down there is evidence to cite, not something to ask the user again.
- **Sensitive paths** — build config, CI, migrations, signing keys, infra, lint and formatter config, code generators.
- **Existing agent setup** — Step 0 already listed what counts and classified it. Read what it found
  in full now: all of it changes what you are allowed to write.
- **Whether the setup will be committed** — is `.agents/` or `.specs/` in `.gitignore` or
  `.git/info/exclude`? `project-workflow-rules.md` records it, where installed (Step 6).

## Step 2 — Choose the stack profile

*On an add run, Step 0.1 says what this step skips.*

`.agents/builder/profiles/` holds one folder per stack, and every other profile, which is not a
stack. A **feature profile** is one of those: one capability with everything it needs, offered as a
single yes or no. Its `PROFILE.builder.md` says
*All or nothing* and lists what installs, and the `**Depends on:**` line on its `PROFILE.md` names any
profile that has to go in with it — installed without a second question.
A stack profile is what is true of a *stack* rather than of a project: the skills built around its
test runner and UI framework, the tool commands a
permission list needs, and the topics a `project-code-style-rules.md` on that stack must answer. Getting this
wrong is how a Python service ends up with Kotlin skills presented as house rules, so it is decided
before anything is installed.

1. Read each stack profile's **Detection** section — every `profiles/*/PROFILE.builder.md` — against what
   Step 1 found.
2. **One matches** — use it.
3. **More than one matches** — the repository spans two stacks. Ask which one this setup is for;
   one setup holds one stack.
4. **None matches** — write one in `.agents/builder/profiles/<name>/`. Copy the nearest
   `PROFILE.builder.md` as a shape and replace every value from evidence in this repository:
   detection rule, real tool commands, and the
   code-style topics that actually bite on this stack. Add the stack's `rules/on-demand/*-code-style-rules.seed.md` in the
   shape of an existing one. Leave `skills/` empty rather than translating another stack's skills;
   a test skill for a runner you have not read is worse than none. A skill you do add must work in a
   repository with none of this setup — no reliance on `.specs/`, `.agents/` or another skill.

Say which profile you chose and why in the report. If you wrote a new one, say what is still empty
in it.

## Step 3 — Identify candidate features

*On an add run, Step 0.1 says what this step skips.*

**Only if `specs` looks likely** — you have not asked yet, so do this unless the repository makes
it pointless, and drop the result if Step 4 declines the profile.

Map source directories to candidate feature specs. A feature is a unit with its own public surface
and its own reason to change — usually a module, package, or top-level feature directory, not every
file. Aim for 3-10 candidates on a normal codebase; if you get 40, you are slicing too thin.

**On a large or long-lived codebase, do not try to reach full coverage.** Spec what you can
confidently characterize from the manifest, structure, and a representative skim — usually the
newest or most actively-touched areas, since those are what's about to be worked on anyway. Leave
everything else genuinely unspecced; that is the expected, normal state, not a shortfall to
apologize for in the report. Coverage grows one task at a time via `spec-create`
as work actually touches each area — that is the intended path, not a fallback for what setup
missed.

For each candidate, record: proposed slug, code glob, and one line on what it appears to do.

## Step 4 — Ask for what code cannot tell you

*On an add run, Step 0.1 says what this step skips.*

Present everything you inferred, then ask for the rest **in one batch**. Code can show you *what*;
it cannot show you *why*, *for whom*, or *what is deliberately excluded*. You need:

1. **Which profiles** — **skipped on an add run**: Step 0.1 already asked, and asking twice reads as
   not having listened. Otherwise one question per folder under `profiles/`, using its `PROFILE.md`
   to say what it brings, with your recommendation from Step 1 beside it (no Compose code → a stack
   profile is still worth it, but say why). Don't ask about `core`: it is the base and goes in either
   way. Today's set: `specs` is spec-driven development itself — say that Steps 3, 7 and 8's spec
   work goes with it; `code-review` is AI review of a merge or pull request; `testing` is how tests
   get written; `documentation` keeps comments and READMEs true as code changes; `graphify` answers
   dependency questions through that tool; `ai-companion` is one person's preferences for how the AI
   works beside them — recommend it for only the user; the stack profile is chosen in
   Step 2.

   **A profile is one yes or no, never a list of its parts.** Taking half of one is a thing to do
   later, by deleting folders inside it — not a question to answer before anyone has used it.
2. **Shared, or only you** — for each profile taken: `.agents/profiles/<name>/` for everyone, or
   `.agents/.local/profiles/<name>/` to keep it to yourself, gitignored. That is the whole choice.
   A profile declaring *All or nothing* in its `PROFILE.builder.md` still installs whole either way.
3. **Project goal** — what this is, who it's for, why it exists, and what "done" looks like.
4. **Non-goals** — what this project deliberately will not do or support.
5. **Constraints** — timeline, platform, compliance, performance budgets.
6. **Confirm the feature list** from Step 3 — corrections, merges, splits, missing ones.
7. **Anything from Step 1 you could not determine** — commands, sensitive paths, conventions.

Show your inferences alongside each question so the user is correcting rather than authoring.

## Step 5 — Install

Do this with `.agents/builder/` still in place — Step 9 deletes it. **Two different things happen
here**, and mixing them up is the one mistake to avoid:

- **The engine is installed.** Its files go to fixed destinations by the tree in
  `.agents/builder/README.md`, because they are forms about this repository and the files both tools
  read first. Copy them by the markers below.
- **Every other profile is dropped in.** Copy the whole folder to `.agents/profiles/<name>/` — do not
  take its files apart, do not copy them to destinations. Then run the sync once and it links
  everything:

  ```bash
  python3 .agents/core/skills/project-sync-profiles-and-skills/scripts/sync.py
  ```

  That is what makes deleting the folder later a complete uninstall. A profile whose `**Depends on:**`
  names another gets that folder too, without a second question.
How to install it is in its filename — a marker just before the extension, dropped from the
destination name (`AGENTS.seed.md` lands as `AGENTS.md`):

- **No marker — copied.** Byte for byte. A destination that already exists with different content
  is **left**: don't overwrite it, and list it in the report.
- **`.seed.` — a form.** Only if missing; an existing destination is **kept** — it is the project's,
  and Step 6 says what may be added to it.
- **`.builder.` — not installed.** Read here, like a stack's `PROFILE.builder.md`.

Never infer the kind from `{{…}}`: the spec templates are copied and keep theirs
on purpose.
- **A profile whose `PROFILE.builder.md` says *All or nothing*** — its folder goes in whole, or not
  at all. Never offer its skill, its agents or its rule separately: that file says why each part is
  useless without the others. It is one question in Step 4 and one line in the report.
- **Where a profile goes** — `.agents/profiles/<name>/` for everyone, `.agents/.local/profiles/<name>/`
  when the user wants it to themselves. That one choice is the whole question; there is no picking
  files out of a profile at install time. Wanting only part of one is a thing to do afterwards, by
  deleting folders inside it and running the sync again.
- **A profile's `.seed.` files** — answered where they sit, inside the profile, with the marker
  dropped: a rule the profile brought only makes sense with it, and deleting the folder takes the
  answer too. Delete the form once its answer is written.
- **No loader rows to keep or delete.** `LOADER.md` is the project's own file. The sync starts it where
  it is missing, with the always-on rules placed by their folder, and reports each on-demand rule as
  unplaced; a profile not installed brings no rule, so there is no line of it to delete.
- **The map** — delete the rows and boxes of every profile not installed. Without `specs`, delete its
  three figures too — the spine, ownership and the loop all draw the spec process — and the agents
  table under Reference; Encoding, the rest of Reference and Local still describe what was installed.
- **Not installed** — `.agents/builder/` itself, and every `.builder.` file.

Then:

- Create `.agents/.local/profiles/`, where anything the user keeps to themselves goes.
- Run the sync once more at the end: `python3 .agents/core/skills/project-sync-profiles-and-skills/scripts/sync.py`.
  `stubbed` in its summary means symlinks are unavailable here — fine; mention it once. It also
  starts `.agents/LOADER.md` where it is missing and reports every rule no line places. Place each
  now, as that skill's *Place what the loaders miss* says — one message of proposed lines, written on
  the user's yes. An add run on a project that already has a loader leaves its lines alone and places
  only the new rules.
- **Read its *Conflicts* block if there is one.** A fresh install into an empty repository has none;
  one here means the project already had a skill, an agent or a file by that name. Nothing was
  overwritten. Put each one in the report with the ways out the sync printed, and let the user
  choose — renaming or deleting someone's file to make a conflict go away is not yours to do.
- **Run `project-resolve-conflicts`** once everything is linked, and settle what it finds with the
  user. Profiles don't know about each other, so two can bring the same job under different names —
  two test-writing agents, say; a name clash is only the obvious case.
- **Record nothing.** No version file, no manifest. Which profile a file came from, and how it differs
  from this builder, are computed whenever the builder is present — the only time either question is
  asked. A stored version would be wrong the first time an add run left a file it did not install.
- Search every seeded file for `{{`. That list is Step 6's worklist. Installed spec templates keep placeholders on
  purpose; don't count them.

## Step 6 — Answer the seeded files

Fill only markers that are still literally `{{...}}`, and delete the filling instructions (an HTML
comment explaining how to fill the file, a `_comment` key) once a file is answered:

- **`AGENTS.md`** — the project name and one-line description, nothing more; it loads on every
  session. Stack and commands go in `02-tech.md`, structure in `01-architecture.md` (Step 7). If `AGENTS.md` already existed (`kept`), leave its content alone and append only what it
  lacks: the instruction to read `.agents/LOADER.md` and the local loader. If it already documents its
  own delegation or instruction-loading setup, do **not** add a second one — flag the overlap in
  the report and let the user consolidate. `CLAUDE.md` should contain `@AGENTS.md`; if an existing
  one doesn't import it, flag that.
- **`.agents/CONSTITUTION.md`** — if the project already had one, this is the file to talk about
  before touching: show what the form would add, say which of its own principles that overrides, and
  change it only on a yes. If it had none, the form is the starting point and is the project's from
  then on.
- **`.agents/core/rules/always-on/project-sensitive-paths-rules.md`**, where installed — only paths that exist: build config, CI, signing
  keys, local machine config, lint and formatter config, migrations, infra, code generators.
- **`.agents/core/rules/on-demand/project-code-style-rules.md`**, where installed — 3-8 real rows with code evidence, per the form's
  comment. Delete every row you have no evidence for; a table of general good practice is
  worse than a short one.
- **`.agents/core/rules/on-demand/project-workflow-rules.md`**, where installed — from `git log`, the pipeline file, and any git hooks
  or formatters wired into the build. The section that matters most is which tests CI *doesn't* run: nobody writes
  that down and everyone assumes wrongly. Say whether `.agents/` and `.specs/` are committed — other
  files point here for that answer.
- **`.agents/README.md`** — keep or delete each `<!-- specs -->` section by whether the profile was
  chosen, then delete the fences and the leading comment.
- **`.claude/settings.json`** — the `permissions` placeholders, from the profile's *Tool commands*
  table plus Step 1's findings, then delete `_comment`. If the file already existed, it was kept:
  change nothing in it **except** to add a `permissions` entry for a script this run installed, which
  Step 0.1 requires — without one, every run of that script asks.
- **`.specs/00-product.md`**, **`01-architecture.md`**, **`02-tech.md`** — Step 7.

`.agents/profiles/specs/rules/on-demand/spec-architecture-rules.md`, where `specs` installed it, is copied, not seeded — **leave it alone, and never add
this project's module boundaries to it.** It is method; the boundary graph is state, and
`.specs/01-architecture.md`'s Boundaries section owns it.

## Step 7 — Build the specs tree

**Only if `specs` was chosen.** Without it there is no spec tree, no `.specs/README.md` and no
templates: skip this step whole and say so in the report.

Create every spec from a template — the builder writes only `.specs/README.md` and `.specs/.gitignore`, in Step 5, and
frontmatter is never written from memory. The root specs' templates are `.builder.` files read from the builder,
since nothing needs them after this step; the feature template is the one Step 5 installed for
`spec-create`. Copy a template only where the spec doesn't exist yet:

| File | Copy of | Fill from |
|---|---|---|
| `.specs/00-product.md` | `.agents/builder/profiles/specs/templates/spec-00-product.builder.md` | Step 4 answers 3-5 |
| `.specs/01-architecture.md` | `.agents/builder/profiles/specs/templates/spec-01-architecture.builder.md` | Step 1 structure + Step 3 features |
| `.specs/02-tech.md` | `.agents/builder/profiles/specs/templates/spec-02-tech.builder.md` | Step 1 stack and commands. Its Testing section — framework, test command, file location, naming convention — is what the `spec-test-writer` subagent reads, so leave nothing out |
| `.specs/changes/<branch name>-<feature slug>/` | `.agents/profiles/specs/templates/spec-feature.md`, as `specs.feature.<slug>.md` with `status: draft` | one `spec-create` change per confirmed feature — it goes from `draft` to `merged` once the user confirms the reading |

A spec describes the code as it is. Work agreed or in progress lives in change folders under
`.specs/changes/`; setup writes only the feature changes above.

For each feature change:
- Set the new spec's `owns` to a glob you have **verified matches files on disk**.
- You are describing existing code from the outside, and the user has not confirmed your reading of
  it yet — Step 9's report says so; don't present it as settled.
- Write acceptance criteria from behaviour you can actually see in the code and its tests. Where the
  intent is unclear, write it as an **Open question** rather than a criterion. Under-specifying is
  recoverable; a confident wrong requirement is not.

If the repo already has specs, ADRs, or design docs elsewhere, do not migrate them silently. List
them in the report with a proposed destination and let the user decide.

Don't create contract specs during setup — that's a judgment call for new work, not something to
infer from existing structure. Leave it to `spec-create` later; setup only needs the feature tier.

## Step 8 — Index and map

```bash
python3 .agents/skills/spec-rebuild-overviews/scripts/build_index.py   # only with specs
python3 .agents/core/skills/project-sync-profiles-and-skills/scripts/build_setup_map.py
```

The first generates `.specs/INDEX.md`, `.specs/DECISIONS.md` and `.specs/OPEN-QUESTIONS.md`. Read
the Drift section and resolve or report every item. Unspecced areas are informational — a freshly
set-up tree has plenty.

The second refreshes the setup map's numbers and lists every rule or skill the map has no row for —
typically this project's own files. Add a row for each in `.agents/SETUP-MAP.html` saying what
it is for; that half of the map is written, not generated.

## Step 9 — Report

Delete `.agents/builder/` now. Search the seeded files and `.specs/` for `{{` once more, and end
with, in this order:

1. **Chosen** — every profile taken or declined, one line each, and whether it went to everyone or
   only the user; the stack profile and why; any profile dropped in because another's `**Depends on:**`
   named it.
2. **Created** — files written fresh.
3. **Extended** — pre-existing files appended to, and which sections were added.
4. **Left untouched** — every `kept` and `left` from Step 5, and why.
5. **Still needs input** — every `{{…}}` still left in a seeded file or a spec, and every open question in a spec, with
   the specific question attached. This is the most important section; do not compress it.
6. **Drift** — anything `build_index.py` reported under "Drift" that you did not resolve (real
   problems: a dangling glob, ambiguous ownership). Not "Not yet specced" gaps — those are expected.
7. A reminder that the feature changes under `.specs/changes/` are your reading of the code, not the
   author's, and wait for their approval — and that most of the codebase is likely still unspecced by design; coverage
   grows via `spec-create` as work touches each area, not as a scheduled task.
8. What `project-resolve-conflicts` found, and what the user picked for each.
9. **How to add a profile from now on** — copy the folder into `.agents/profiles/` and run the sync.
   They never need this prompt again for that. Deleting the folder and running the sync removes it.
