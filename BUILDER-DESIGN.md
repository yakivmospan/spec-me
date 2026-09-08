# spec-me-builder design

## Intent
A template of the agent setup. Drop `builder/` into a project, ask an agent to set it up, and get
rules, skills, spec scaffolding and the setup map shaped to that project — the first time, and again
each time a profile is added to it. Its developer tests
it inside real projects with `SETUP-DEV.md`; releases live in the `spec-me` repository.

The thing it installs is **spec-me**, in two parts. **`core` is the engine**: the files both tools
read first, how rules load, where skills go, the settings, the map, the `runner` agent and the five
`project-*` skills. It is the one thing a prompt places, and the only thing setup has to install.
**Everything else is a profile you drop in** — `specs`, `code-review`, `ai-companion`, a stack — a folder
copied whole into `.agents/profiles/` and linked from where it sits. The builder is
`spec-me-builder`.

This file holds why the builder works the way it does, and what has to hold before it is released.
How it works — where every profile file lands, filename markers, who gets which — is `README.md`. Everything here yields to the constitution in `core/CONSTITUTION.seed.md`, and a decision that
makes adoption harder is revisited under it, not defended.

## Use cases

The three flows the builder exists to serve. They are the measure for anything added here: a change
that serves none of them is scope.

### Adopting it in steps

The common case, and the one that shapes the most.

1. Someone drops the builder in — a folder, a zip, a URL — and asks for `core`.
2. The setup prompt installs it, reports what it left alone, and helps settle whatever collides with
   what the repository already has.
3. They work for a while, adding rules, skills and scripts of their own. `project-create-rule-or-skill`
   writes them; `project-resolve-conflicts` and `project-test-setup` keep the set honest.
4. Later they want specs. They drop the builder in again and ask for `specs`. **The same
   prompt runs**, checks that profile's `Requires` are met, checks its rules against theirs, and
   installs on top of what they have built.
5. More profiles, more files of their own, and files they delete themselves, in any order.
6. They may want out of a profile: convert the specs to another format, then remove `specs`.
7. A later profile may carry that conversion — an `openspec` profile that installs openspec and
   rewrites the specs into its format, reading git history to rebuild what changed when.

### Taking it all at once

1. Someone drops the builder in and asks what there is.
2. The prompt shows the profiles and helps them choose.
3. It installs the chosen set, answers every form from the codebase, and writes the root specs.

### Developing the builder

1. Its developer runs spec-me inside a real project.
2. They test features and prompts against real work.
3. They add skills, delete skills, and move the structure around.
4. Every change lands in the installed setup and in the builder together, so `builder/` can be
   dropped into its own repository at any point. `SETUP-DEV.md` and `builder-dev-rules.md` are this
   flow, and it is the only one running today.

## Constraints
- **Nothing under `profiles/` names a project, and a file is either copied or seeded, never both** —
  when a copied file needs a project value, move the value into a form. A copied file holding one
  project's value needs a hand merge on every improvement.
- **Never overwrite; delete only the builder** — install leaves an existing different file and
  reports it, and a setup prompt deletes nothing but `.agents/builder/`.

## Decisions

### Structure
- **Installed files are copies; only skill links, and the developer rule's link, point elsewhere**
  - **Instead of** symlinks from the project into the builder, for the developer too
  - **Because** `builder/` has to be removable without breaking a project, and a developer moves
    between the developer and the user setup by adding or deleting that folder. The developer rule exists only
    while the builder does, so its link can't drift from the file it points at, and stops loading if the builder goes
- **In `.agents/`, only `rules/` and `skills/` are plain folders; the rest start with a dot**
  - **Instead of** `local/`, `scripts/` and `templates/` beside them
  - **Because** rules and skills are what anyone browses; the rest is machinery, personal files or
    generated output, and a dot keeps it out of the way. `builder/` stays plain where its developer keeps it
- **Rule files end in `-rules`**
  - **Instead of** bare names like `architecture.md` and `workflow.md`
  - **Because** a rule reads as one wherever it's referenced, and `spec-architecture-rules.md` can't be
    mistaken for the `01-architecture.md` spec
- **Everything installable sits under `builder/profiles/`, one folder per profile**
  - **Instead of** `builder/skills/` and `builder/rules/`; and instead of the `builder/blocks/` layer
    that held them until 0.4.0
  - **Because** `builder/skills/` and `builder/rules/` match every skill and rule glob alongside
    `.agents/`, and a profile folder does not
  - **Changed 0.4.0:** once the mandatory files became `core`, `blocks/` held nothing but
    `profiles/`, so the layer went and `profiles/` moved up. The reason above still holds — there is
    still no `builder/skills/`
- **The folder decides who gets a skill or rule: the profile whose subject it serves, on any stack,
  or `profiles/<stack>/{skills,rules}/` on one**
  - **Instead of** `skills/mandatory/` + `skills/optional/`, a `required` flag, or a `stacks/` folder
  - **Because** a flag beside a folder can contradict it, and moving the folder is the whole change
  - **Replaced 2026-09-24:** `profiles/general/` as a catch-all for "any stack, no one subject". Its
    skills each turned out to have a subject — `documentation`, `graphify` — and what stayed is one
    person's preferences for how the AI works beside them, now `ai-companion`
  - **Changed 2026-09-21:** `profiles/skills/` and `profiles/rules/{always-on,on-demand}/` were the
    "always" case; the spec system moved into `profiles/specs/`, so no skill and no rule is
    mandatory now
- **A profile's skills are listed only by its `skills/` folder**
  - **Instead of** a skills table in each profile file, and a `general` profile file holding only
    that table
  - **Because** the folder and each skill's own description already say it, and a table beside
    them drifts
- **A script lives in the skill that uses it; a profile`s `scripts/` holds only scripts no skill owns**
  - **Instead of** one shared scripts folder
  - **Because** permission paths in `.claude/settings.json` point into the skills
- **A profile installs only its chosen skills; the profile and its forms stay in the builder**
  - **Superseded 0.5.0** by *A profile is a folder you drop in*: the folder goes into the project
    whole, `PROFILE.builder.md` and all, and nothing is chosen file by file at install time. What
    survives of this decision is that a `.builder.` file never installs, and a form is answered out
    of the folder rather than left in it
  - **Instead of** `.agents/PROFILE.md`, or `.agents/stack/<name>/` with the code-style template
  - **Because** only `SETUP.md` read a profile or a form; in a project it would have been a
    leftover. `spec-test-writer` finds the testing skills by reading `.agents/skills/`
- **One README for the installed setup, in chapters**
  - **Instead of** separate READMEs for the stack, the profiles and `.local/`
  - **Because** they repeated each other
- **Every agent ships in a profile, with what invokes it**
  - **Instead of** `profiles/agents/`, which every setup gets
  - **Because** an agent's description loads in every session, so one whose skill was never chosen is
    load nobody can use; a profile already decides who gets the skill, and the agents follow it
- **A subagent is a fourth kind, beside always-on rules, on-demand rules and skills: a self-contained
  job handed over whole, whose summary is all that comes back. Guidance that shapes the main session,
  and work that needs the user's decisions on the way, stays a rule or a skill**
  - **Instead of** an agent as a persona carrying a whole capability — its skills preloaded, its
    workflows, the other agents it works with — as shared collections of agents often do
  - **Because** a subagent starts in a fresh context, without the conversation or the loaders the main
    session read, and cannot ask the user until it has finished. The main session hands work to it
    by matching its description, the route a skill's description failed mid-work (Decisions →
    *Installing*), so one whose moment comes mid-work gets a line saying "hand this to the `x` agent",
    in its profile's rule or a loader, as a skill does
- **A subagent names only its own profile's files. Across profiles it finds installed skills by
  instruction, or the loader passes their names in**
  - **Instead of** a `skills:` list naming another profile's skill
  - **Because** a profile naming outside itself breaks the day that profile is removed, and what
    Claude Code does with a `skills:` entry it cannot find is not documented. An agent told to "list
    `.agents/skills/*/SKILL.md` and read those about testing" — `spec-test-writer` does — finds whatever is
    installed and nothing that is not; being told to read, it does not wait on a description to match.
    A loader may name anything installed, so "hand this to the `x` agent, with the `y` skill" joins
    profiles there, as it does for rules
- **One `runner`, in core; a profile hands it the command, and core's workflow rule sends every
  build, lint and test run to it**
  - **Instead of** a runner per profile — `specs-runner`, `code-review-runner`
  - **Because** the job is the same everywhere — run a command, report only what failed — and only
    the command differs, which the calling skill passes in. Several agents with one job and near-same
    descriptions are an overlap the main session picks between blindly. Without the workflow rule's
    line, a project lacking `specs` reached `runner` by its description alone
  - **Revisit when** a profile needs a different job, not a different command — then it is an agent
    named for that job, not a second runner
- **A capability that needs a skill, its agents and a form rule together is one profile, installed whole**
  - **Instead of** four optional pieces offered separately under `profiles/general/`
  - **Because** the parts are not independently useful and a subset looks like a working install: the
    skill without its rule has no forge, no tracker and no way to obtain a build, so it reviews code
    against itself and reports opinions where it should report proof
  - **Also** a profile stops being a stack-only idea; a feature profile has no *Detection* section,
    because no evidence in a codebase says whether a team wants the capability
- **The product is an engine and a set of profiles, not one bundle**
  - **Changed 0.5.0:** `core` stopped being a profile among profiles and became the engine at
    `.agents/core/`, the one thing a prompt places. `specs` stopped being installed and became a
    folder dropped into `.agents/profiles/`
  - **Instead of** the spec system as the builder's mandatory core, with the profiles as extras; and
    instead of one `spec-me` profile holding both, which 0.3.0 shipped
  - **Because** the builder installs an agent setup, and spec-driven development is one thing that
    setup can do. Splitting them names the part that is true whatever a team's process is — how a rule
    gets loaded, how a skill becomes visible, what the map measures — and lets a project take it alone.
    The skills are named after the product — `spec-create`, `spec-rebuild-overviews`, `project-test-setup`
    — so they read as one group in a list both tools sort alphabetically, with `project-*` as
    the sub-family that works the setup rather than a spec
  - **Also** the grouping is by name prefix, not by folder or a `spec-me:` namespace: both tools
    require a flat `skills/<name>/SKILL.md`, and the namespaced form is a Claude Code plugin, which
    Codex does not read
  - **Also** the setup's own tooling — validate, rule-verify, rule-skill, profile-sync — is in core
    because it scores and repairs whatever a project installed, across every profile it took and every
    edit it made since. It is most useful exactly where the process is least standard
- **A profile declares the other profiles it needs in `## Requires`, and the setup installs them
  without asking. `core` is never listed: every setup has it, and a check against it could never
  fail where anything is there to run it**
  - **Instead of** a dependency list in `SETUP.md`, or trusting the user to pick both halves
  - **Because** the alternative is a project that answers "no" to core and gets a `specs`
    whose rules nothing loads — a broken install that looks like a choice. One section beside *All or
    nothing* keeps the fact next to the profile that owns it
- **`SETUP.md` has two modes, and there is no second prompt**
  - **Instead of** an `ADD-PROFILE.md` beside it, or a `.agents/.profiles/` store with links that a
    profile could be enabled and disabled through
  - **Because** the prompt was already built to survive a second run — Step 5 leaves a copied file
    that exists and keeps an existing form, Step 7 copies a spec template only where the spec is
    missing — so a second prompt would have duplicated all of it to change one step. Step 0 now reads
    the project's state and routes; Step 0.1 holds everything an add run skips
  - **Also** a profile store would make an installed file's real home the store, so a project's own
    edit becomes a fork the next install overwrites. `.agents/README.md` promises the opposite: the
    installed rules and skills are the project's to edit
  - **Also** the builder is present whenever the setup changes — someone drops it back in to add a
    profile — so which profile a file came from is computed, never stored
  - **What it unlocks:** a profile written after a project was set up can reach that project. Without
    it, every new profile was only ever installable on new repositories
- **A profile is a folder you drop in, not files a prompt copies out**
  - **Instead of** `SETUP.md` installing each profile's files to their destinations, which 0.5.0's
    first half did, with an add run to install one later and a computed answer to which profile a
    file came from
  - **Because** every question that machinery answered stops being a question. Uninstall is deleting
    the folder. Provenance is the path. Editing is editing a text file in your own repository, and
    nothing can overwrite it because nothing installs over it. Taking part of a profile is deleting a
    subfolder
  - **Cost, accepted:** both tools need a flat layout — `.claude/skills/<name>/SKILL.md`, one level —
    so a profile folder is invisible until something links it. One script does that and prunes links
    whose source is gone, which is what makes deleting a folder an uninstall. The chain is already
    proven: a local skill today reaches Claude through two symlinks
  - **Supersedes** Step 0's add-run mode and the *Profiles* report's reason for existing. Both stay
    useful for the engine, which is still installed by a prompt; neither is needed to add a profile
- **The engine is the only thing a prompt installs**
  - **Instead of** every profile being installed, or nothing being installed
  - **Because** two things can't be dropped in: a form whose answer describes this repository
    (`AGENTS.md`, `LOADER.md`, `.claude/settings.json`, the `project-*-rules.md`), and the root specs.
    Those need an agent reading the codebase. Everything else is a folder, so setup shrinks to
    answering forms and then telling the user they can drag profiles in whenever they like
- **The constitution is one document the project owns, and no profile may write to it**
  - **Instead of** a `CONSTITUTION.seed.md` per profile merged in at install; a `rules/constitution/`
    folder profiles drop files into; or the constitution split across an engine file and a profile's
    always-on rule, which 0.5.0's first half shipped
  - **Because** a folder you drop in must not be able to change what outranks every rule and skill in
    your project. Making that impossible is worth more than letting a profile ship a principle, and it
    removes the merge engine, the eligibility rule and the confirmation step that letting it would
    have needed
  - **Also** it costs almost nothing: a profile's principles live in its always-on rules, which already
    outrank every skill, and `project-sensitive-paths-rules.md` already guards `.agents/core/rules/**`.
    Anything you want constitutional you paste in yourself, which is the only way anything should get
    in there
  - **Where it lives:** `.agents/CONSTITUTION.md`, read before any rule, shipped by the engine as a
    seed and the project's from then on
- **No spec-check CI job is offered in this version**
  - **Instead of** offering one at setup and recording the answer in `project-workflow-rules.md`, or a
    template copied into the project
  - **Because** proposing enforcement goes against the constitution
  - **Replaced 2026-09-14:** the job offered at setup; then a parked job file

### Installing
- **No script and no manifest: agents install by reading the profiles, and `README.md`'s tree
  is the only record of where each file lands**
  - **Instead of** `build.py` with `manifest.toml` and a fingerprint per file; mirroring the
    project's layout inside `profiles/`; or a mapping table in a skill
  - **Because** files get dragged and regrouped between profiles, and stored paths break under that
- **The install kind is a filename marker: `.seed.`, `.builder.`, or none for copied**
  - **Instead of** a `seeded` label in the README tree, repeated as name lists in both skills, or
    detecting `{{…}}`
  - **Because** the marker moves with the file. Copied spec templates contain
    `{{…}}` too. Copied is the unmarked kind because `SKILL.md` and script paths can't be renamed
- **An agent answers a form by reading the code**
  - **Instead of** a render step filling placeholders from stored answers
  - **Because** answers are judgement in prose (*"Timber; never `Log.d`"*), not values
- **Core names no profile; a profile names only its own rules and skills; only the loaders name
  across profiles; none names the builder unconditionally. An on-demand rule is wired in by a
  `LOADER.md` row, a skill by its description and by a line saying when to run it — in its own
  profile's rule, or in a loader — an always-on rule by the loader's always-on list; the developer's rule is a `.builder.` file only `SETUP-DEV.md` links, into
  `.agents/.local/`**
  - **Instead of** optional regions — `<!-- if skill:<name> -->` and `<!-- if builder -->` lines in
    copied files, trimmed at install and restored when pushing back; a project-level rule file joining
    skills from several profiles; and a trigger rule inside each profile
  - **Because** copied files stay identical to the profile files they came from, and the loader is
    the project's own file, the one place that sees every profile. A core file naming a profile makes
    core depend on something that depends on core; a profile's rule naming another profile's skill
    points at nothing once that profile is deleted
  - **Replaced 2026-09-24:** "no mandatory file names an optional rule or skill, an optional one
    names no other", which left a skill no way to be reached by the work
  - **Replaced 2026-09-16:** optional skills naming another conditionally, and loader rows for skills
- **One model for guidance: always-on and on-demand rules, and skills. A rule is read from its
  loader row; a skill runs when a request matches its description, or when a line says "at this step,
  run this skill" — in a rule of the skill's own profile when that profile already has a rule read at
  that step, otherwise in a loader, which is also where skills from several profiles are put in
  order. One skill, one such line. Precedence is stated once, in constitution-rules' *Which
  instruction wins***
  - **Instead of** loader rows listing a skill's file to read, ranking tables between overlapping
    skills, and precedence written in each rule and skill that needed it
  - **Because** an agent reads a file a row points to only when it is a rule. In real sessions scored
    with `core/tests/behaviour/run.py --transcript`, on 2026-09-23 and 24, sessions that read the
    loader opened every rule a row listed and none of the skills beside them — 0 of 4, with the row at
    the end of the work (sessions `89e92cfd`, `6d901680`, `9ce570a6`) and at its start, in the same row
    as a rule that was opened (`2a64d9d9`). An instruction, "before saying it's done, run
    `code-clean-kotlin`", got the skill called, its sweep run and the module compiled 3 of 3 inside a
    rule (`693dab5f`, `cba5553d`, `e25daf2e`), and 3 of 3 as a row of the loader itself (`0e493294`,
    `c49e345e`, `dfd13269`). The loader line needs no rule file per trigger. With neither — only the
    skill's description, which says "use after changing any Kotlin file and before reporting code work
    done" — it was used 0 of 3 (`706d4a03`, `6780e5b0`, `aaf6e400`), so the line, not the
    description, is what reaches a skill mid-work. The runs above were Claude Code 2.1.280 on
    `claude-opus-5-5`; repeated on `claude-sonnet-5` the same day, a line in the rule gave 3 of 3
    (`208256ea`, `856d44c9`, `8dbb69e5`), a line in the loader 3 of 3 (`fd5ae9bf`, `bb501fa7`,
    `67829147`), and the description alone 0 of 3 (`2eee3a6a`, `4d4020bd`, `6542dff9`) — Sonnet ran
    the skill's sweep but, unlike Opus, never its build step. Codex and other models are untested, and
    may reach a skill by its description where Claude did not. A table between
    overlapping skills only moved an overlap somewhere every new skill had to update, and precedence
    in nine files kept contradicting itself. Two rules or skills saying different things is a bug,
    settled in the files by `project-resolve-conflicts`
  - **Revisit when** a new transcript-scored run shows a skill whose file a row lists being opened
  - **Replaced 2026-09-24:** skills declaring their own `load-when:` for a loader row, the "second
    door" 0.5.0 added; the runs above are why it went
  - **Replaced 2026-09-16:** *When several skills apply* tables in both loaders, and the shared
    loader's order section
- **The loader is the project's own file: its steps, in order, say what to read and what to run.
  The sync starts a missing one with the always-on rules placed by their folder and reports every other
  rule unplaced; it keeps both loaders honest, and its skill proposes where a new rule goes**
  - **Instead of** a loader generated from each rule's `load-when:`, a list of moments core
    publishes, and an order number in each rule
  - **Because** order is decided best by the one owner who sees all of it — the project — and an
    agent follows the order of the text, so the text is the order. Independent profile authors
    picking moment words or numbers collide, and nobody sees why. The sync script removes a row whose
    file is gone, reports a rule no row places — it never loads — and warns about a skill a line names
    that is not installed. Placing a new rule is judgement, so the sync skill's agent proposes a row
    from the rule's content and the steps already there, and the user confirms. The shared loader
    names only shared rules and skills. A rule carries no `load-when:`: the loader alone says where it
    sits, its always-on list included, so no second copy of that can drift from it
  - **Replaced 2026-09-24:** the loader generated from each rule's `load-when:`, which 0.5.0 chose to
    stop a hand-written table leaving a row behind a removed profile; the sync's pruning does that job
    now, and the key goes from every rule
- **A profile declares in its `PROFILE.md` what core needs to know about it — a word-budget
  exception, its own self-check — and core reads that**
  - **Instead of** core's setup skills naming a profile's files, as `project-test-setup`,
    `project-create-rule-or-skill` and `project-resolve-conflicts` named `specs`' 27 times
  - **Because** those were left over from when the spec system was part of core, and every one broke
    the day `specs` was not installed
- **The project's own rules stay in `core/rules/`, seeded and answered there; they name no profile**
  - **Instead of** a `profiles/project/` holding every answered file, which would leave core a plain
    copy of the builder's
  - **Because** `core/rules/` reads as what it is — this project's core rules — and a seeded file is
    already told apart by its `.seed.` marker, so an update replaces the copied files and leaves the
    answered ones. What made core depend on a profile was core's setup skills naming `specs`, not
    where the answers live
- **Everything a profile can't run without, always-on, is one file in that profile; the rest is
  optional and chosen at install**
  - **Instead of** `core-rules.md`, `spec-rules.md` and `setup-constitution-rules.md` all mandatory,
    with general ground rules, sensitive paths and a workflow form installed in every project
  - **Because** one file is what a project must keep, and general rules — KISS, sensitive paths, a
    project's code style and workflow — are a project's choice. Their names say which: `spec-*` is
    mandatory, `project-*-rules.md` a project's own form
  - **Replaced 2026-09-16:** the three always-on files; `architecture-rules.md`, `code-style-rules.md`
    and `workflow-rules.md`, renamed `spec-architecture-rules.md`, `project-code-style-rules.md` and
    `project-workflow-rules.md`
- **No hooks: work that has to follow an edit is a step in a skill both tools run**
  - **Instead of** Claude hooks that rebuild the spec index and the map after an edit and load the
    code rules before the first production edit
  - **Because** a hook reaches one tool only, so every rule still had to work without it, and
    `.claude/settings.json` needed a merge kind of its own just to carry them
- **The builder writes only `.specs/README.md` and `.specs/.gitignore`; `SETUP.md` writes the root specs from `.builder.`
  templates that stay in the builder**
  - **Instead of** writing nothing under `.specs/`; seeding the three root specs from the builder, or
    installing their templates
  - **Because** the README is the same in every project and is what makes the specs readable without
    the setup, while specs are written in the project under the user's review, one template can't be
    both copied and seeded, and an installed template nothing reads again is a leftover
  - **Replaced 2026-09-14:** the builder writing nothing under `.specs/`
- **One stack per project, with no removal: `SETUP.md` adds profiles but never swaps a stack, and
  asks when two profiles match**
  - **Instead of** two stacks in one setup, or an uninstall step
  - **Because** without removal, a second install puts a second stack beside the first; changing
    stack is by hand (`README.md`)

- **A clash between two names is reported, never settled quietly**
  - **Instead of** last writer wins, which is what the sync did until 0.5.0 — a profile dropped in
    later silently took `runner.md` from the engine, and two profiles carrying one skill name
    produced whichever link was written last
  - **Because** dropping a folder in is meant to be safe to try. It is only safe if the thing that
    goes wrong is visible: every clash is one block naming every claimant and what each way out
    costs, and nothing of the user's is touched to make one go away
  - **Also** who wins is fixed and stated — core, then the shared profiles by name, then the user's
    own — so two runs on one tree agree, and nothing dropped in later can take a name from the
    engine. A fixed order is a tie-break, not a resolution: the clash is still reported

- **A profile groups by subject only where every part of it is stack-agnostic**
  - **Instead of** grouping by subject wherever it reads well — a `testing` profile holding
    `test-unit`, `test-integration` and `test-plan-manual` was refused once for exactly that reason
  - **Because** the axis that makes a profile droppable is stack versus general. When `test-unit`
    was 16 Kotlin references deep, a `testing` profile would have shipped mockk guidance to a
    project with no Kotlin in it. Splitting the Kotlin templates into its `reference.md` made all
    three stack-agnostic, and only then did the subject grouping become safe
  - **Also** there is no catch-all profile. A skill or rule with no profile to join starts one named
    for its subject, however small — a subject is what a person decides to drop or keep, and a
    catch-all makes them take all of it
  - **Replaced 2026-09-24:** "this is what `general` is for: what suits any stack and belongs to no
    one subject", emptied by `documentation` and `graphify` and renamed `ai-companion`

### Proving it
- **Two suites, because the setup has two halves that fail differently**
  - **Instead of** one suite, or trusting a run of `project-test-setup` to cover both
  - **Because** `tests/stress_profile_sync.py` answers *are the files and links right* — filesystem
    questions, cheap, deterministic, run on every change. `core/tests/behaviour/` answers *does an agent
    follow any of it* — which needs a real agent session and is neither cheap nor deterministic. A
    single suite would either be too slow to run often or too shallow to mean anything
- **The mechanical suite imports the install map it is testing against**
  - **Instead of** restating where each file lands
  - **Because** the map lives in `project-test-setup`, and a copy of it in the tests would drift until
    the tests passed against a layout no install produces. Importing it means a disagreement between
    the two is a failing case, not a silent divergence
- **The behaviour suite scores by dimension, stores every run, and compares two runs**
  - **Instead of** a pass/fail, or one overall number
  - **Because** an agent is not deterministic, so a single figure moves on its own and tells nobody
    anything. The question worth answering is *did it move, and which way* — which needs runs kept
    with the agent, its version, the builder version and the context load they ran at
  - **Also** `--dry-run` prints each case's floor: what it scores when no agent runs at all. A case
    that scores full marks on a floor run measures nothing, and the report names it. Two cases here
    were written that way first
- **Context load is a test dimension, not an afterthought**
  - **Because** the setup's rules are read once, by a tool call, at the start of a session — and a
    long session is compacted, which can summarise that reading away. Whether a rule holds at 10%
    of a window and fails at 90% is the difference between a setup that works and one that works
    in demos. This is also why the constitution's core is carried into `AGENTS.md`

### Updating
- **The constitution has one source — `core/CONSTITUTION.seed.md` — seeded once and the project's
  from then on, with its core carried into `AGENTS.md` by the sync**
  - **Changed 0.5.0:** it is a form, not a copied rule. A project that already has a constitution
    keeps it; the form is shown, what it would add is named, and it changes only on the user's yes,
    because changing a constitution is the setup's own red flag
  - **Also 0.5.0:** the section between `<!-- carried -->` markers is generated into `AGENTS.md`
    between markers of its own, and re-generated on every sync. `AGENTS.md` is put in front of an
    agent again on every request; a file read by a tool call is not, and a long session's compaction
    can summarise it away. So the part that would cause harm if forgotten is the part that is
    carried, and it is generated rather than written twice so the two cannot drift. An `AGENTS.md`
    without the markers is left completely alone — the copy is offered, never imposed
  - **Changed 0.4.0:** it was the *Constitution* section of `spec-builder-rules.md`; the setup-wide
    principles and *Which instruction wins* moved to core, the two spec ones stayed with the specs
  - **Instead of** `CONSTITUTION.md` at the builder's root, copied by setup into a seeded
    `setup-constitution-rules.md`; the builder's copy and the seed edited together; or builder-only
    principles about setup and updates
  - **Because** one text can't drift, a copied block compares byte for byte with its installed file,
    and a copy survives setup deleting the builder. How the builder is set up and updated is a decision
    in this file, not a principle
  - **Replaced 2026-09-14:** a builder constitution with three setup principles, kept in step with the seed
  - **Replaced 2026-09-16:** `CONSTITUTION.md` and its seed, on the user's twice-confirmed yes
    by hand
- **Setup runs once, and this version has no update step: a newer builder is compared by hand, or by
  an AI the user asks**
  - **Instead of** `project-update`, one skill pairing a project with a builder in both directions
  - **Because** a team entering spec-driven development runs a setup once; tooling for later versions
    waits until someone needs it
  - **Replaced 2026-09-14:** `project-update`
- **Setup is a prompt, not a skill: `SETUP.md` for a team's project, `SETUP-DEV.md` for the developer's**
  - **Instead of** a `project-init` skill
  - **Because** it runs once, from a folder deleted afterwards, so nothing needs to discover it
  - **Replaced 2026-09-14:** the `project-init` skill
- **Switching between the user and the developer setup is by hand, through `SETUP-DEV.md`; syncing
  under the developer setup is automatic, through a local always-on rule that makes every setup change in the builder too**
  - **Instead of** reconciling on every run, with the developer resolving each difference; symlinks
    from the project into the builder; or `builder-sync-rules.md`, loaded wherever the builder was kept
  - **Because** the developer wants changes in the templates, design and README as they're made, so
    differences only pile up under the user setup — resolved once, when switching to the developer setup — and a local
    rule loads for the developer alone
  - **Replaced 2026-09-14:** `builder-sync-rules.md`; then reconciling on every `SETUP-DEV.md` run
- **The project records nothing about its own install**
  - **Instead of** a `BUILD.md` listing the profile, the skills taken and declined, whether the
    builder is kept and the files kept different on purpose; or a `.baseline/` copy or a
    fingerprint per file
  - **Because** the folders already show what is installed, and a hand-kept list drifts
  - **Changed 0.5.0:** `.agents/SETUP-VERSION` went too. It was the last stored state, and it was
    wrong by construction — an add run leaves files it did not install, so one version number cannot
    describe the tree. Worse, deleting the file turned a working setup into *Foreign*, and a first
    setup would then run over it. Step 0 now asks the inventory which profile destinations hold files
  - **Also** the test is presence, never content: a project edits its installed rules and skills and
    runs versions behind, so a file that came from a profile may share not one byte with the copy in
    the builder. Where it sits and what it is called do not change

### Local
- **`.agents/.local/` is additive only**
  - **Instead of** local overrides of shared rules
  - **Revisit when** a real conflict appears
- **`.agents/.local/profiles/` is created at install, empty**
  - **Changed 0.5.0:** it holds profiles now, not a second rules tree and a second loader
  - **Instead of** appearing with the first local profile
  - **Because** a folder that appears later is one nobody finds
- **Nothing under `.agents/.local/` is recorded or synced**
  - **Instead of** a receipt of local installs
  - **Because** the folder is the mechanism; taking a skill for everyone is how it gets updates
- **Two loaders: `.agents/LOADER.md` for what everyone has, `.agents/.local/LOADER.md` for what one
  person has; within a step, the shared lines come first. The local loader may repeat the shared
  steps, so its owner sees the whole order**
  - **Changed 2026-09-24:** both are hand-kept files the sync checks, not generated (Decisions →
    *Installing*, "The loader is the project's own file"); the split below still holds
  - **Changed 0.5.0:** there were two hand-written loaders, one per rules folder. They became one
    generated file — and that was wrong, because the one file is committed while `.local/` is not.
    A local rule's path in a committed loader is a row every teammate is told to read and cannot;
    worse, the loader being generated meant it gained and lost those rows depending on whose machine
    last ran the sync, churning in git. Two generated loaders, split by whether the rule ships
  - **Instead of** a loader per rules folder, or `AGENTS.md` carrying the table itself
  - **Because** a rule now stays inside the profile that brought it, so a folder can no longer be
    the list. The sync's pruning is what makes deleting a profile a complete uninstall: the lines go
    with the folder, and no line can name a rule that is not there
  - **Instead of, also** a hand-written table nothing checked — which is what left a dangling row
    behind every removed profile until 0.5.0

### The map
- **The map is seeded**
  - **Instead of** copied
  - **Because** `build_setup_map.py` and people edit it per project, so a copy would always differ
- **The map is a local file, never published**
  - **Instead of** a hosted copy
  - **Because** a hosted copy goes stale the moment the local file changes, and only one of the two
    tools can push one
- **What a script writes on one machine lives in `.agents/.cache/`**
  - **Instead of** beside the personal rules and skills in `.agents/.local/`
  - **Because** `.local/` holds what a person writes, and `.cache/` what a script regenerates

### The spec lifecycle
- **The specs describe themselves: `.specs/README.md` says how to find, read and change one, following
  the rules and skills that define the process**
  - **Instead of** the process living only in `.agents/core/rules/` and the spec skills; or the README as the
    single source the skills point at
  - **Because** specs are memory any agent can use (the constitution), and `.agents/` may be neither
    committed nor installed — while a README written from its sources never quietly becomes one
- **Work not folded in yet lives in `.specs/changes/<branch>/` (a second one on it: `<branch>-<topic>/`) — each spec it touches,
  moved in with `git mv`, and an `implementation-plan.md` when the work needs one — and folds into
  `.specs/` by moving each spec back to its place**
  - **Instead of** editing a spec at its place ahead of the code; Kiro-style requirements, design and
    tasks files kept per feature for good; or a whole copy of each spec, folded in by copying it over
    its place
  - **Because** a spec at its place then always describes the code as it is, and no finished task list
    or stale design is left for later sessions to read. A move, unlike a copy, shows every edit as a
    diff in git, the IDE and the merge request, and leaves no second version to reconcile at merge —
    at the cost of one spec being in only one change at a time
  - **Replaced 2026-09-19:** a whole copy of each spec, folded in by copying it over its place
- **A spec's criteria stay in the spec file**
  - **Instead of** a separate requirements file beside each spec
  - **Because** criteria outlive the change that added them, and Constraints, Pitfalls and Change
    history refer to them by id
- **Every spec has a `status`: `draft` or `approved` inside a change, `merged` everywhere else; only the
  user approves**
  - **Instead of** no `status`, with an `approved:` date in a change's `proposal.md`; `active` for the
    third, which reads as *being worked on*; or a folder per status
  - **Because** any single file then says how far it has come, to a person or any agent; the three names
    don't overlap the way `draft` once meant both *not agreed* and *being built*; and a status in a header
    moves no files
  - **Replaced 2026-09-14:** no `status`, with two `approved:` dates and four phases; then one `approved:`
    date in `proposal.md`
  - **Replaced 2026-09-15:** the third status was named `current`
- **Every way into a spec starts a change, through one skill — `spec-create` — and
  `spec-plan` and `spec-merge` finish it**
  - **Instead of** `spec-new`, `spec-update` and `spec-from-code` as three entry skills; or skills
    writing specs directly, beside a separate `change-*` skill family
  - **Because** a spec written from code is a reading the user has to confirm — already what a change
    carries. Three doors made the user pick one and collided on "create/update the spec"; the agent can
    tell the starting point from the specs and the code, asking only whether the code is already right
  - **Replaced 2026-09-13:** three entry skills, one per starting point
- **A `merged` spec the code has moved past, with the code right, is corrected in place — a Change
  history row, "No ticket" when there's none, and `updated:`**
  - **Instead of** a change folder with the spec moved in, an approval and a fold-in for a spec that was only behind
  - **Because** nothing is being decided: the code already is what the spec should say, so one question
    to the user is the whole review, and the row keeps the history a change would have
- **A design outside a change — a new module or a moved boundary — is agreed in chat and recorded in
  `01-architecture.md`, with a Change history row and `updated:`**
  - **Instead of** opening a change only to hold a design, or an architecture-only plan file
  - **Because** chat is the simplest place to agree it, and the Decision and the row in the spec that
    owns the boundary keep what a change's plan would have
- **A change folder holds only spec files, and one `implementation-plan.md` — design, then tasks —
  when the work needs it**
  - **Instead of** a `proposal.md` beside the spec files; separate `design.md` and `tasks.md`; or the
    same files and two approvals at every size, with a contract change's `tasks.md` listing its
    sub-changes
  - **Because** each spec file already carries its why, in a `## Change` section, and its approval, in
    `status` — a proposal only repeated them. Design and tasks are both the how: most designs fit in two
    lines above the tasks they explain, and a big one grows sub-headings in the same file
  - **Replaced 2026-09-14:** every change with the same files and two approvals; then a `proposal.md`
    holding the why and the approval; then separate `design.md` and `tasks.md`
- **Changing course adds, never rewrites: a ticked task stays, rework is a new task, and an edited
  criterion keeps its approval on the user's OK**
  - **Instead of** rewriting or unticking built tasks; or any edit to an approved guarantee sending the
    spec back to `draft`
  - **Because** building is where the user tests and adapts, so the plan stays a record of what was
    tried and what was found, and an approval survives the ordinary back-and-forth. Only the user sets a
    spec back to `draft`, to stop and rethink
- **A new criterion's id is one past the highest in the spec**
  - **Instead of** never reusing a removed id
  - **Because** the highest id is always in the file, while a removed one leaves no trace to check
    against. A removed highest id coming back is fine: a ticked task's tags are history, naming the
    criteria as they read when it was ticked
  - **Replaced 2026-09-14:** removed ids never reused
- **A spec written from code that already exists goes from `draft` straight to `merged`**
  - **Instead of** approving it, then folding it in as a second step
  - **Because** there is nothing to build: the approval is the user confirming the reading
- **Nothing folds in unconfirmed: each unchecked criterion is confirmed by the user, dropped, or keeps
  the change open**
  - **Instead of** criteria folding in unchecked, marked not confirmed yet
  - **Because** a `merged` spec describes the code as it is, so an unconfirmed criterion in it is a
    claim nobody made — and a person's word is enough, so one question settles every one of them
- **Reports to the user use plain words, not phase or skill names**
  - **Instead of** "Phase: Planning", "delta", "sub-change"
  - **Because** the lifecycle is the agent's to know; the user should never have to learn it
- **A criterion lists its proof under `Verified:` — test files with their tests, or `Source: Manual` —
  and its checkbox shows whether it has any; a spec may hold unchecked criteria**
  - **Instead of** a spec holding complete criteria only, with `--check` failing a checked box without a
    listed test or `verified:` escape; a bare checkbox with its proof optional; a `Verified: Yes/No` field beside the checkbox; flat
    `Source:`/`Tests:` fields beside a one-line `Verified:`; or a baseline ratcheting
    down unverified criteria
  - **Because** a person's word is enough (the constitution), but has to be written down to be seen at a
    glance rather than dug out of `git blame` — so a checked box with no proof is a warning, never a failure
  - **Replaced 2026-09-14:** complete, evidenced criteria only; then a bare checkbox with its proof
    optional; then flat `Source:`/`Tests:` fields beside a one-line `Verified:`
- **Work across modules gets a contract spec its features point at; each change folds in on its own**
  - **Instead of** a contract change holding a sub-change per feature, merged together
  - **Because** a story's tickets finish at different times, and gating one on another blocked finished
    work
  - **Replaced 2026-09-14:** contract changes merged together with their sub-changes
- **A contract's Implementation table names who takes part and their role; which contract criteria a
  feature carries is written once, as `(contract AC-n)` in the feature's own criteria**
  - **Instead of** a `Satisfies` column listing criteria per feature beside the same tags in the features
  - **Because** two mappings drift, and the one beside the criterion is the one updated when it changes.
    A contract criterion is checked by its own proof or once its feature criteria are; confirming it by
    hand confirms them too, since a person trying the whole flow tried each part of it
  - **Replaced 2026-09-14:** a traceability matrix in the contract's Implementation table
- **A change's spec files sit flat in its folder, one per spec, each named after the path it lands at
  (`specs.feature.logger.md`) and each the whole spec as it should read afterwards**
  - **Instead of** a delta applied section by section — ADDED, MODIFIED, REMOVED, RESOLVED; one
    requirements file holding criteria only; one target spec per change; or a `specs/` tree mirroring
    `.specs/`
  - **Because** a whole copy folds in by copying over, which any agent can do; one ticket can touch
    several specs; a file's name is where it lands; and a mirrored tree buried each spec several folders
    deep
  - **Replaced 2026-09-14:** a `specs/` tree inside each change, mirroring `.specs/`; then deltas applied
    section by section
- **One skill holds a plan's whole life — writing it, building from it, changing course — and the
  architect subagent proposes**
  - **Instead of** the architect subagent deciding, with `design.md` shaped by one paragraph; or a
    design skill and a build skill handing over to each other
  - **Because** a plan is a conversation the user has to steer and resume, and changes of course are
    frequent: a handover between two skills mid-build is where an agent skips the other skill's rules
  - **Replaced 2026-09-14:** `spec-design` writing `design.md` and `tasks.md`, and `spec-apply` building
    from them
- **Each spec skill opens with its non-negotiables, stated inline**
  - **Instead of** skills that only point at the rule files, leaving every rule one or more citations away
  - **Because** each hop is a chance the rule never loads, and the few rules that stop an agent deciding
    on its own drowned among formatting rules of equal weight. The rule files stay the source; the
    inline list is short enough to check against them
- **`DECISIONS.md` and `OPEN-QUESTIONS.md` are grouped by spec**
  - **Instead of** one whole-tree table each, read in full on every task
  - **Because** a spec's own entries already come with reading it, so a task needs only its parent
    chain's and related specs' sections — and a whole-tree table grows with coverage
- **The generated overviews are never committed — `.specs/.gitignore` keeps them local**
  - **Instead of** committing `INDEX.md`, `DECISIONS.md` and `OPEN-QUESTIONS.md` with the specs
  - **Because** every change rebuilds them, so a team on branches would conflict on nearly every merge;
    `spec-rebuild-overviews` rebuilds them in seconds, no spec depends on them, and a local copy can show what only
    one machine knows, like the last `spec-sync-with-code` result
- **Where guidance goes, its shape and its testing live in a mandatory `project-create-rule-or-skill` skill; conflicts
  between installed rules and skills are settled by a mandatory `project-resolve-conflicts`**
  - **Instead of** a `setup-rules.md` rule beside a `project-skill` skill, or relying on Claude's own
    skill-creator; and conflicts left to `project-test-setup`'s read-only report
  - **Because** a shape needs a template and a test procedure, which a rule table can't carry; the
    model is read only when the setup changes, so it belongs in a skill; a Claude-only skill reaches one
    tool; and settling a conflict takes the user's pick and an edit, which a read-only review can't make
  - **Replaced 2026-09-16:** `setup-rules.md` and `project-skill`
- **The setup is validated by a mandatory, read-only skill run on request — `project-test-setup`**
  - **Instead of** a prompt kept beside `SETUP.md`, which a user install deletes with the builder; a
    scoring script; or a check that runs every session or in CI
  - **Because** judging the setup against the constitution — contradictions, what could go — takes
    reading, not a script; every project keeps the skill after install; and on request keeps its cost
    out of ordinary sessions. It proposes, never edits, and never proposes strictness
- **Each principle has one owning rule; other rules point at it, and only a skill's non-negotiables
  restate it**
  - **Instead of** the same principle restated in each rule file that touches it
  - **Because** every copy is one more place for the rules to disagree
- **`spec-style-rules.md` is a drafting checklist; the reasoning and examples live in `spec-check-style`'s
  `reference.md`**
  - **Instead of** one 2,800-word file loaded on every spec edit
  - **Because** polish is caught by `spec-check-style --fix`, offered at merge, so drafting needs the rules,
    not the essay

## Acceptance criteria

What has to hold before 0.1.0 is released. Unchecked means not yet run.

- [ ] **AC-1: `SETUP.md` sets up a project by reading alone**
  - **Given** a repository with no agent setup and `builder/` at `.agents/builder/`
  - **When** `SETUP.md` runs
  - **Then** every block lands where `README.md`'s tree says, the map has rows only for the optional
    skills and rules it installed, and `LOADER.md` only for its on-demand rules
  - **And** every `{{` left in a form is listed in the final report, and `.agents/builder/` is gone
- [ ] **AC-7: A new form needs only the README tree**
  - **Given** a new `.seed.` block, with only `README.md`'s tree updated
  - **When** `SETUP.md` runs
  - **Then** it is installed as a form, with no change to `SETUP.md`
- [ ] **AC-12: Switching to the developer setup reconciles a project once**
  - **Given** a project with the user setup from this builder, with one installed rule edited, and `builder/`
    put back at `.agents/builder/`
  - **When** `SETUP-DEV.md` runs
  - **Then** it reports that rule as the only difference and changes nothing before the developer
    chooses
  - **And** once the choice is applied, the developer rule is linked into
    `.agents/.local/profiles/builder-dev/rules/always-on/`
- [ ] **AC-13: Under the developer setup, a setup change reaches the builder as it's made**
  - **Given** a project with the developer setup, in a session started after the developer rule was linked
  - **When** an agent changes an installed rule
  - **Then** the profile has the same change, with no step run or asked about
- [ ] **AC-10: Local additions show only in the map's Local section**
  - **Given** a local rule and a local skill
  - **When** the map is opened from `file://`
  - **Then** the Local section lists both, and the shared rows don't include the local skill
  - **Note:** an agent rendered it in headless Chrome during development; a person hasn't looked yet
- [x] **AC-11: Local skill links stay out of git**
  - **Given** a skill in `.agents/.local/skills/`
  - **When** `project-sync-profiles-and-skills` runs, and again after the skill is removed
  - **Then** it is linked for both tools with both links excluded from git, and the links are then
    pruned
  - **Verified:**
    - **Source:** Manual
      - during development

## Where it is going

Not built yet: the direction the next changes are measured against.

- **Two repositories.** `spec-me` ships `core` and the `specs` profile. Every other profile —
  `code-review`, `documentation`, `graphify`, `ai-companion`, `kotlin-android` and `testing` today —
  moves to `spec-me-profiles`, its
  author's own collection: shared, but still theirs.
- **Anyone can publish profiles.** A profile is more than a skill: a set of skills, rules and agents
  that work together. As with skills today, anyone can write their own and keep them in their own
  repository; `spec-me-profiles` is one collection, not the only source.
- **Three layers, each for a different reader** (Decisions → *Installing*).
  - **Core** — the engine every project shares, and the project's own core rules, which the whole
    team is bound by: the ground rules, and each form answered for this project, such as what may and
    may not be done in git and the required commit format. It names no profile.
  - **A profile** — adds to core for a particular need: a stack, a way of working, a tool. It names
    only its own files.
  - **`.local`** — one person's preferences on top, never committed.
- **For example**, core's workflow rule says what the team may do in git and in what format; a
  `git-worker` profile brings the skills that do the work around git, and the project's loader says at
  which step each one runs.

## Gaps against the use cases

Named, not designed. Each says which use-case step it serves, so none is rediscovered as a bug.

- **Closed 0.5.0: `LOADER.md` keeping honest** — *Adopting it in steps*, 6. A hand-written table
  left a row behind every removed profile. The loader stays the project's own file, and the sync
  removes a line whose file is gone and reports a rule no line places (Decisions → *Installing*), so
  deleting a folder takes its lines with it. First closed by generating the loader from each rule's
  `load-when:`, replaced 2026-09-24. Checked by the loader cases in `tests/stress_profile_sync.py`.
- **Nothing measures whether a profile is worth its load** — all three flows. Load is measured in
  words by `project-test-setup`, and behaviour is scored by `core/tests/behaviour/`, but the two are not
  joined up: there is no answer to "this rule costs 700 words every session — does removing it
  change what an agent does". Joining them is a case that runs with a rule present and absent and
  diffs the score.
- **Step 4 asks profile by profile, and never shows the list** — *Taking it all at once*, 2. A
  presentation change, not a mechanism.
- **A validation report a team can share** — all three flows. `project-test-setup` writes to a
  local ledger; the wanted shape is a report a person hands to teammates, so a change to the team's
  flow can be checked before it destabilises everyone's sessions. 0.5.0 made the installed profile
  set, not one profile, the unit being reported on; what is left is a destination a teammate opens.

## Open questions
- [ ] **How a project gets the builder once it has its own repository**
  - **Action:** decide at the move — likely versions tagged there, with `SETUP.md` explaining
    the fetch.
- [ ] **How a project gets a profile from `spec-me-profiles`, or from anyone else's collection**
  - **Action:** decide with the split (*Where it is going*): whether the setup prompt fetches a
    profile by URL, or a person drops the folder in as today.
- [x] ~~**What decides the order when several skills run at one moment?**~~
  - ~~**Action:** two profiles' trigger rules at the same moment land in one loader row with no order
    between them. Decide with the user before the trigger rules are built.~~
  - Resolved: see Decisions → "The loader is the project's own file"
- [ ] **Does a subagent's handoff hold mid-work, and does `skills:` do what the docs say?**
  - **Action:** before building on either, run `project-test-behaviour` on a "hand this to the `x`
    agent" line against the description alone, and on an agent with a `skills:` entry of its own
    profile; check whether Codex has anything like `skills:`.
- [ ] **May a profile change what core says, or only add to it?**
  - **Action:** *Where it is going* says a profile adapts core to a need, while `.agents/.local/` is
    additive only (Decisions → *Local*). Settle whether a profile may replace a core rule — say, a
    stricter commit format — or only add beside it, with *Which instruction wins* settling a clash.

## References
- `README.md` — where every block lands, the filename markers, and how to set up and change
  the builder.
- `SETUP.md` and `SETUP-DEV.md` — the setup steps these decisions shape.
- `CHANGELOG.md` — what changed between versions, and why.
- `tests/stress_profile_sync.py` — the mechanical suite: the files and links, in throwaway repos.
- `core/tests/behaviour/README.md` — the behaviour suite: what a real agent does, at a chosen context
  load, scored so two runs compare.
