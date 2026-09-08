# Changelog

What each builder version brings, in prose, and why — so a project comparing itself with a newer
builder by hand can decide what to take.

## 0.5.0 — unreleased

### Skills named for the moment you reach for them
- `project-profile-sync` → **`project-sync-profiles-and-skills`**, `project-rule-skill` →
  **`project-create-rule-or-skill`**, `project-rule-verify` → **`project-resolve-conflicts`**,
  `project-validate` → **`project-test-setup`**. *Verify* and *validate* were the same word, and
  `check-setup` failed the test that matters: opening the folder and not knowing what it was. "Check"
  works when the object is concrete — `spec-check-style` keeps it — and fails when the object is
  everything.
- `spec-review` → **`spec-check-style`**, `spec-verify` → **`spec-sync-with-code`**, `spec-rebuild`
  → **`spec-rebuild-overviews`**. Each takes a word the domain already used: *style* from
  `spec-style-rules.md`, *overviews* from `.specs/.gitignore`.
- **`spec-sync-with-code` now earns its name.** It used to report a divergence and stop, sending you
  to `spec-create`. It settles each one with you — the spec is stale, or the code is the defect —
  because a name promising reconciliation has to reconcile. A stale spec still goes to `spec-create`
  for the edit itself, so one skill writes spec content and *Keeping it honest*'s `updated:` and
  `Source: Manual` are never skipped.
- **A profile ships a `PROFILE.md`** saying what it is, what it depends on and how to remove it, and
  `project-sync-profiles-and-skills` warns when a declared requirement is missing. `**Depends on:**`
  (once `**Needs:**`, and `## Requires` in `SETUP.md`, which no profile ever had) names
  other profiles only: every card used to list `core`, which every setup has and which only the sync —
  part of core — ever checked, so the line could never warn about anything.

### Skills that belong to everyone stopped being one stack's
- **`test-integration` moved to `general`.** Its own description says "across any software
  architecture layer"; it was sitting in `kotlin-android`, where a project on another stack could
  never see it.
- **`test-unit` moved too, and split**: 740 words of principles in the skill, 523 words of JUnit4
  and JUnit5 templates in `reference.md` that load only when opened. A project on any stack gets the
  half that is true everywhere.
- **That move broke the skill, and the suite caught it.** Genericising the description removed
  `ViewModels`, `coroutine flows` and `with mockk` — the words that matched. Three runs in a row
  stopped reaching the skill while their *output* stayed good, because the sibling test files carry
  the same conventions. Judged on output alone it would have shipped. Generality means adding the
  general words beside the concrete ones, not deleting them.

### Documentation became a profile of its own
- **`documentation` holds `docs-incode` and `docs-readme`,** moved out of `general`, and
  `docs-rules.md`, the on-demand rule that runs them before code work is reported done and when a
  change renames something a README names. In `general` they ran only when a request matched them,
  which is the route real sessions skipped mid-work; a rule read at that step is the route they
  followed. Place `docs-rules.md` after a stack's code-style rule in the same loader row, so the
  code is cleaned up before its comments are fixed. The `docs-incode` line follows the tested
  pattern but was not itself tested.
- **The builder's `README.md` describes the builder again.** It had been overwritten with a copy of
  the installed setup's README; it is rewritten for the current tree — `core/` installed to fixed
  places, profiles dropped in whole — starting from the last builder README, in a backup of
  2026-09-17.

### `general` became `ai-companion`
- **The catch-all is gone.** `general` held "what suits any stack and belongs to no one subject";
  each of its skills turned out to have a subject — `documentation`, `graphify` — and what stayed is
  one person's preferences for how the AI works beside them: how answers read, how files are edited,
  a second look before acting, a handover note. It is renamed for that, and a skill or rule with no
  profile to join now starts one named for its subject.
- **A project taking this version** renames `.agents/.local/profiles/general/` (or the shared one) to
  `ai-companion/`, points its loader's always-on lines at the new paths, and runs the sync — which
  otherwise prunes those lines and reports the rules unplaced.

### A tool's skill gets a tool's profile
- **`code-query-dependencies` moved from `general` to a new `graphify` profile.** It only works with
  the `graphify` command installed, so in `general` — "anything any stack may want" — every project
  carried its description whether or not it used graphify.
- **Its card says how it differs from graphify's own skill**, which `graphify install` puts in each
  person's own skills: ours answers one dependency question, code-only and only when asked; theirs
  builds and explores the whole graph and claims any codebase question. It says which to ask for,
  and warns off `graphify install --strict`, whose hook blocks the first file read of a session.

### The loader is the project's again, and a skill is reached by a line
- **Both loaders are the project's own files, edited by hand**, not generated. Each is an always-on
  list, then steps, top to bottom, saying what to read and what to run before each kind of work — and
  the line order is the order. Order is decided best by the one owner who sees all of it; independent
  profile authors each picking a moment word collide, and nobody sees why.
- **Rules and skills no longer carry a `when:` or `load-when:` key.** A loader line alone places a
  rule, its always-on list included, so no second copy can drift from it.
- **A skill whose moment comes mid-work gets one trigger line**, "at this step, run the `name`
  skill" — in a rule of its own profile when that profile has a rule read at that step, otherwise in a
  loader. In real Claude Code sessions scored from their transcripts, a skill with only its
  description was used mid-work 0 of 6 times, one a loader row listed by its `SKILL.md` was never
  opened (0 of 4), and a trigger line worked 12 of 12, in a rule or in the loader alike. Tested on
  Claude Opus and Sonnet only; Codex is untested.
- **The sync keeps the loaders honest instead of writing them.** It starts a missing loader with the
  always-on rules placed by their folder, removes a line whose file is gone, and warns about a rule no
  line places, a skill a line runs that is not installed, a local path in the shared loader, and a
  file still declaring `load-when:`. Placing a rule is judgement: the sync skill proposes the line and
  the user confirms it.
- **Core names no profile's files.** A profile's `PROFILE.md` declares what core needs — a
  `**Word budget:**` exception and a `**Self-check:**` list `project-test-setup` runs — so the spec
  checks and budgets core's setup skills carried now travel with `specs`.
- **A project taking this version:** its loaders become its own files — keep them as they are; delete
  every `load-when:` key from its rules and skills, which the sync warns about until it is gone; and
  place each rule the sync reports unplaced, at the step it serves.

### The code outranks a document on what the system does today
- **`project-ground-rules.md` gained a *Code first* row.** An agent explaining or investigating read
  the specs and answered from them, when the code, which the spec can lag or miss, is what runs. The
  row covers any claim about the code — behaviour, structure, names, commands, config — before it is
  stated, planned on or written down, also before a claim is taken back. A spec, doc, comment or
  ticket is a claim to check, and a difference is named with an offer to fix the stale side — which
  side is wrong stays the user's call. It replaced *No guessing*'s one code-reading sentence.
  *Specs vs. code* in `spec-builder-rules.md` still governs edits.

### A spec is checked against its code before a change moves it in
- **`spec-create` gained a step for a *Change*:** when the spec's owned code has commits after its
  `updated:`, or it has none, `spec-sync-with-code` runs before the spec moves in. A change opened on
  a stale spec carried the old reading into its new criteria, and its diff mixed the correction with
  the new requirements. The only warning was an offer from `INDEX.md`, which is git-ignored and may
  not exist; the step reads git directly. A check already run, or declined, this session counts, and
  spec-builder-rules' offer gives way to the step, which it outranked — so the two never ask twice. To stay under the skill budget, a step
  repeating section 1 went, and the move bullet now points at spec-change-rules' *The folder*.

### No trace of the project it was built in
- **Worked examples retold in neutral domains.** The review reference's replies and findings, the
  manual test plan's cases, a spec change folder's name and a script comment had been lifted from the
  project the builder was developed in — its module names, a real ticket number, real dates, its
  setup flow. They now tell the same lessons about a checkout, a payments client and saved searches.
- **The developer rule says what "nothing of this project" covers:** product, module, package and
  people names, ticket keys, real dates, and examples retold from its work. Carrying a change into
  the builder strips them.

### Each profile brings its own test writer
- **`specs`' agents are `spec-architect` and `spec-test-writer`** (Codex: `spec_architect`,
  `spec_test_writer`), named for the profile that ships them.
- **`testing` has its own `test-writer`,** which writes tests from the code's behaviour with the
  installed testing skills — so a project with testing and no specs still hands test writing to an
  agent. A project with both keeps whichever it wants.
- **`SETUP.md` runs `project-resolve-conflicts` after every install and every added profile,** instead
  of offering it, and that skill now compares agents' descriptions as well as skills'. Profiles don't
  know about each other, so two doing one job under different names is found there, with no line in
  either profile declaring it.

### The same habits in a claude.ai project
- **`CLAUDE-PROJECT-INSTRUCTIONS.md`** rebuilds a Claude project's Instructions from the constitution,
  the ground rules, `ai-companion` and your own preferences, as one self-contained document, and
  lists what changed since the last one. A chat project reads no files, so the builder is the source
  and the Instructions are its copy.
- **The chat keeps the project's files in the shape `.specs/` has** — an `INDEX.md`, the product
  spec, a spec per feature, material named by its future repository path, an inbox for what has no
  home — and saves only what the user asks to save. A product started in chat moves into a
  repository by renaming its files. The chat starts those files itself from a description of what
  is being built, and keeps several products apart, each in its own tree, with a `shared.` tree
  between them. An existing project converts on request: a plan first — where each piece goes, what
  merges, what goes, where files disagree — then writing on a yes, and deleting old files only on
  another.

### Writing a profile has its own page
- **`profiles/README.md`** says how to write a profile of your own: the folder, `PROFILE.md`,
  `PROFILE.builder.md`, seeds, what a profile may name, and how to try it. The same facts sat in two
  short bullets of the builder README, a table in the installed README and three steps of `SETUP.md`,
  and nothing walked someone through making one.
- **A profile's form is answered inside the profile.** `SETUP.md` sent a rule form's answer to
  `.agents/core/rules/`, while `code-review`'s notes and every installed answer kept it in the
  profile. The profile wins: its rule means nothing without it, and removing the folder now removes
  the answer too.

### Cleaning up a branch is not reviewing it
- **`code-clean-kotlin` takes "clean up this branch" and leaves merge request reviews** to the review
  profile. "Review this code" matched both it and `code-change-review`, and its first step turned a
  branch diff away as another skill's job — so a cleanup of a branch's changes had no home.

### Commit messages say what changed without the diff
- **The workflow rule's commit format gained a default shape**: the subject says what the change
  does overall, and each bullet starts with Added, Changed or Removed and says in a few words what.
  A first draft that listed files, tests and spec edits read as a tour of the diff; the reader
  wanted the change itself. It sits in core, so every project starts with it and changes it in its
  own copy.

### The behaviour suite, corrected by using it
- **Reading a skill counts as using it.** `used_skill` only counted Skill tool calls, so a run that
  opened `skills/<name>/SKILL.md` and followed its most distinctive rule scored as a miss.
- **A rename no longer voids the history.** `used_skill` and `answer_matches` take an `also` list of
  former names. Renaming the skills dropped the archived baseline from 100% to 79%, measuring the
  renames rather than any agent; with the aliases it reads 95%, and the rest is recorded prose
  naming paths that have since moved.

### Four verbs, and a profile that says what it is
- **The setup skills are named for the moment you reach for them**, not for what their code does.
  `project-profile-sync` became **`project-sync-profiles-and-skills`** — it stopped being only about profiles, and now
  keeps both loaders honest and writes the constitution's core in `AGENTS.md` and the map. `project-rule-skill`
  became **`project-create-rule-or-skill`**, `project-rule-verify` became
  **`project-resolve-conflicts`**, and `project-validate` became **`project-test-setup`**.
  *Verify* and *validate* are the same word, and nothing in either name said one was about a pair
  and the other about everything.
- **A profile ships a `PROFILE.md`** saying what it is, what it needs, whether it splits, and how to
  remove it. Its `PROFILE.builder.md` says some of that already and is never installed, so a
  dropped-in folder used to carry no word about itself.
- **`project-sync-profiles-and-skills` reports an unmet requirement.** It reads `**Depends on:**` from that card. A warning,
  not a gate: the rest of the work still happens.
- **One report for a person**, `core/tests/health.py`. It runs everything there is to run and
  answers the questions someone actually has — will my rules load, is anything broken, did something
  change that I did not change, do the profiles fit, are the numbers moving the right way — without
  naming a single script. Exit code says whether anything needs you.

### One writer per folder, in the install path too
- **The engine's rules are the engine's forms.** `project-sensitive-paths-rules`,
  `project-workflow-rules` and the general half of `project-code-style-rules` moved from the
  profiles that used to seed them into `core/rules/`. Those profiles were writing into a folder none
  of them owned — the same *one writer per destination* the sync is built on, broken where nobody
  had looked.
- **The test is not "is the answer about the repository" — all of them are.** It is *does the
  question still have an answer with the profile gone*. Sensitive paths, workflow and general code
  style do. `project-review-rules` does not: its own form says "install this file only where
  `code-change-review` was chosen", so it stays with `code-review` and is answered inside it.
- **That closes the one hole in "delete it and it is gone".** A profile that seeded into core left
  its rule behind when the folder was deleted, still loading every session with nothing behind it.
  Nothing seeds into core now, so nothing can be orphaned. `project-test-setup` keeps the check as a
  net, under *Answered here, by a profile that is no longer dropped in*.
- **Code style is two rules, not one.** The engine asks what every project answers — logging, error
  handling, formatting, boundaries, new dependencies, what going public costs. A stack profile asks
  only what needs its language to be true: for `kotlin-android`, coroutines, state exposure, DI and
  `internal`. `LOADER.md` lists the two in one row, so both load together.
  Before this, a Kotlin code-style form was the only code-style form, so a project on another stack
  got none at all unless it took a stack profile.
- **`project-test-setup` reports engine rules written in a stack's vocabulary.** Two or more file or
  command names out of a stack's *Detection* and *Tool commands* sections — `build.gradle.kts`,
  `detekt.yml`, a Gradle task — say the row probably belongs in that stack's profile, and name the
  profile to move it to, or to drop in if it is not there. A lead, not a verdict: a repository fact
  may name a build file for a good reason. It found three on its first run, two of them real.

### The rules now survive a long session
- **The constitution's core is carried into `AGENTS.md`**, generated from a `<!-- carried -->`
  section by the sync. `AGENTS.md` is put in front of an agent again on every request; a file read by
  a tool call is not, and a compaction can summarise that reading away — so the pointer survived and
  everything it pointed at did not. What would cause harm if forgotten is now carried; the rest is
  still read once. One source, generated copy, so the two cannot drift, and an `AGENTS.md` without
  the markers is left completely alone.
- **`AGENTS.md` says to re-read rather than work from memory** of a rule it cannot quote.
- The carried section costs about 250 words on every request. That is the price of it being
  compaction-proof, and it is why only part of the constitution is inside the markers.

### A second suite, for whether an agent follows any of it
- **`core/tests/behaviour/`** starts a real agent in a throwaway copy of the setup and checks mechanically
  what it did: which files it read, which skill it used, which subagent it started, whether every
  path it named exists, whether a file it was told not to touch is unchanged.
- **Context load is a dimension.** The same case runs with the window 0%, 25%, 75% or 100% full,
  filled by making the agent read real files from the repository, because whether a rule holds at
  10% and fails at 90% is the difference between a setup that works and one that demos.
- **Runs are stored and compared.** Each run keeps the agent, its version, the builder version and
  the load; `--compare` prints every dimension side by side with better, same or WORSE. An agent is
  not deterministic, so one number means nothing and the movement means everything.
- **Any agent, by config.** `agents.toml` holds the argv and how to read the output; `run.py` names
  no agent. Claude and Codex entries ship; a third is a table.
- **A session you drove by hand scores like an automated one.** `--prompts` prints the cases,
  `--transcript latest` reads what Claude Code wrote to `~/.claude/projects/` and scores it, and the
  report says whether a compaction happened during that session. No CLI has to be installed, and it
  measures a real session rather than a headless approximation of one.
- **Fourteen cases across ten dimensions**, including the ones this version added: a conflict is
  reported and nothing is settled quietly, a sensitive path is asked about first, a profile is
  dropped in rather than copied out file by file, and two rules that disagree are named as a setup
  bug with `project-resolve-conflicts` offered.
- **Scoring is offline, so an agent CLI is a one-off and not a dependency.** Every take's raw
  output is kept under `results/transcripts/`, and `--rescore` re-runs today's checks against
  sessions recorded at any time in the past. A check can be rewritten and every past run re-judged
  on the new standard, which is what makes a number from months ago comparable with today's.
- **`--ingest` takes results as `<case-id>.json`** for an agent that cannot be started as a
  subprocess — another vendor's tool, a colleague's session, or a subagent, whose internal steps
  are recorded nowhere readable. Those runs score on the same footing, with the tool checks labelled
  *(agent's own word)* and counted in the report, because an agent describing its own actions is
  weaker evidence than a recorded call and should never quietly pass as the same thing.
- **`--inflate <words>` says what the always-on budget is buying.** It grows the always-on rules to
  a chosen size using real guidance moved out of the on-demand rules, then runs the cases, so the
  300-word-per-file cap — stated once in a table and never measured — can be argued from a curve
  instead of from a number nobody set deliberately. Every run now reports what the always-on rules
  actually cost.
- **`--ablate <path>` says what one rule is buying.** It removes the file with the real uninstall —
  delete, re-sync, the sync removes its loader line — so the run measures a genuinely smaller setup rather than
  a broken one. What the score loses is what the file was worth.
- **A case can build the tree it needs.** `fixture` plants files into the throwaway copy before the
  agent sees it — two profiles clashing over one name, or a rule file carrying an instruction
  nobody sanctioned — so a case can be about a tree this repository never holds.
- **`file_unchanged` asks the right question.** It compares hashes where a run took them, and
  otherwise asks whether any editing tool named the file, which is what a transcript actually
  records. Falling back to a hash with nothing to compare against had been marking the suite's most
  important safety case as failed while the agent had behaved perfectly.
- **`--dry-run` prints each case's floor** — what it scores with no agent at all. Two cases here were
  worthless when first written, passing on silence alone, and the floor is what showed it.

### Conflicts are named, never settled quietly
- **The sync reports every clash**, one block per name, with everything that wanted it and what each
  way out costs. Four kinds: a real file of yours already holding the name, two profiles carrying the
  same skill or agent name, two names that differ only in case on a filesystem that ignores case, and
  a skill folder with no `SKILL.md`. Before this, the first was a one-line `skip` and the other three
  passed silently — the second and third by overwriting whichever link was written first.
- **Who wins is fixed and stated**: core, then the shared profiles by name, then your own. It is
  fixed so two runs on one tree agree, and so nothing dropped in later can take a name out from
  under the engine. A profile carrying `runner.md` used to displace core's.
- **Nothing of yours is touched to make a conflict go away.** A run that reports conflicts has still
  done every other piece of work, so the tree is usable either way.

### The engine, made honest
- **`--check` shows what the real run would do.** It used to read Claude's folder off disk, so a
  skill's second link was invisible until the first had been written — the preview under-reported
  every new profile.
- **Half a skill reaches neither tool.** A folder with no `SKILL.md` used to link for Codex and not
  for Claude, with nothing said.
- **A stray file beside the skills is not a skill**, and a read-only destination is reported rather
  than ending the run in a traceback.
- **`.git/info/exclude` is one owned block, rewritten each run.** Per-entry editing left a line
  behind for every local profile ever deleted, and missed `.claude/skills/` entirely, so a private
  profile was only half private. Rewriting the block also dropped a `git` call per entry: a tree with
  a hundred skills went from 11s to under a second.
- **A test suite**, `builder/tests/stress_profile_sync.py`: 32 cases in throwaway repositories, from
  the drop-in round trip to symlink loops, unicode names, no git at all, and a whole setup installed
  from this builder and then taken apart again. It imports `project-test-setup`'s install map rather
  than restating it, so the two cannot drift apart without a case failing.

### Leftovers from the move to drop-in
- **Rules that no profile could find.** The spec skills, agents and templates named their rules at
  `.agents/core/rules/`, where those rules stopped living when `specs` became a folder you drop in.
  Nineteen files, and every one of them a rule that would not have loaded.
- **`project-test-setup` compared the builder against a copy-install** and reported four of four
  profiles as incomplete when nothing was wrong. It now compares folder to folder for a profile and
  destination by destination for the engine: 41 files matched before, 68 now, with one real
  difference left.
- **`LOADER.seed.md` and `LOADER-local.seed.md` are gone.** The sync starts a missing loader itself;
  a form beside that could only contradict it, and `SETUP.md` said both at once.
- **`CONSTITUTION.seed.md` sits at `core/`**, not as a rule named `constitution-rules.md` under
  `core/rules/always-on/`, which is where it had been left and where nothing installed it.
- **One path for the scripts.** `.agents/core/skills/…` everywhere, because `.agents/skills/…` is a
  link that does not exist yet when `SETUP.md` first needs to run the sync.

`SETUP.md` runs more than once. A profile written after a project was set up can now reach that
project: drop the builder back in and run the prompt again.

### Two modes, one prompt
- **Step 0 reads the project's state** instead of stopping. Four outcomes: *Empty*, *Foreign*
  (someone else's setup — read it, report it, never convert it), *Ours* (an add run), and
  and *Half-removed* — the setup is recognisably here but `.agents/core/rules/` or `.agents/skills/` is gone, which stops to ask.
  `.agents/builder/` is explicitly not evidence — it is there in every state.
- **The state table is exhaustive, and says so.** Four rows — *Empty*, *Foreign*, *Ours*,
  *Half-removed* — plus an explicit "no row fits, stop and ask". Evidence is defined by a principle
  (a file that instructs an agent) with the marker list given as examples, so `GEMINI.md` or
  `.github/copilot-instructions.md` count without being named; settings alone do not. Step 1 points
  at Step 0's list instead of carrying a shorter one of its own.
- **Step 0.1 is the add run.** It reports what is installed, what is not, what the project has edited
  and what is the project's own, then asks which profiles to add. Steps 2, 3 and 4 skip what the
  project already answered; Step 6 adds loader and map rows instead of filling a fresh form.
- **No second prompt.** Steps 5 and 7 were already written to survive a re-run — an existing copied
  file is left, an existing form is kept, a spec template is copied only where the spec is missing —
  so the change is one step, not a new file. An `ADD-PROFILE.md` was designed and dropped for this
  reason.
- **`.agents/SETUP-VERSION` is gone.** It was the setup's last piece of stored state and it could not
  be right: an add run leaves files it did not install, so no single version describes the tree. It
  was also fragile — deleting that one line made a working setup read as *Foreign*, and a first setup
  would have run over it. A project that had it can delete it.
- **"Is this ours?" is computed, by presence.** Step 0 runs the builder's inventory and asks which
  profile destinations hold files. Not by content: a project edits its rules and skills and runs
  versions behind, so an installed file may share no bytes with the builder's copy, while its path and
  name stay put.

### The state report
- **`validate_inventory.py` has a *Profiles* section**: version installed against builder version,
  which profiles are installed, which are *Incomplete* (a whole-or-nothing profile missing part of
  itself — a broken install, not a choice), which are partly installed by design, which are absent
  with their `## Requires` and rule count, and which skills and rules are the project's own rather
  than a profile's.
- **It no longer claims a differing file is the project's edit.** A project one version behind shows
  every file the builder changed as differing, and nothing here can tell that from a real edit. The
  report says so, and neither case is overwritten.
- **Less noise:** a profile that is absent entirely is one line, not one per file, and a profile file
  naming its own destination no longer counts as a missing path.
- **`project-test-setup` reports profiles first**, and `SETUP.md`'s Step 0.1 reads that section.

- **A file whose name its tool fixes never says a profile is installed.** `AGENTS.md`, `CLAUDE.md`,
  `.claude/settings.json` and the gitignores are names any project may own, so they are counted in
  what a profile *adds* and ignored when deciding whether it is *there*. Without that, every
  repository in the world with a root `AGENTS.md` reported `core` as a broken install.
- **A profile that is not installed says what it adds**, not a fraction of itself.
- **A name the builder still ships is not "retired".** The check reported every uninstalled profile's
  files as retired names, which is backwards on the one run where an uninstalled profile is the
  subject.
- **Step 6 no longer contradicts the add run** about `.claude/settings.json`: an existing file is kept
  except for a `permissions` entry for a script this run installed. **Step 4 no longer re-asks**
  which feature profiles to add — Step 0.1 asked already.

### Tested
Against four fixture repositories — empty, foreign, ours-without-specs and ours-with-edits — by
agents following Step 0 with no write access, re-run after each round of fixes. That found the
*Empty* row being unmatchable (the builder's own folder made every repository look foreign), Step 0
contradicting Step 6 about touching a kept `AGENTS.md`, the edit-versus-version-drift claim, Step 0.1
skipping Step 6 entirely, a state table that was not exhaustive, and the ordinary-names false signal
above — none of which were visible by reading.

## 0.4.0 — unreleased

The product splits in two. `core` is the base a project can take on its own; `specs`
is spec-driven development on top of it.

### Split
- **`core/`** holds the loading system (`AGENTS.seed.md`, `CLAUDE.md`, both
  `LOADER` seeds), `.agents/README.md`'s seed, `project-ground-rules.md`, the settings and gitignores,
  `build_setup_map.py` with the map seed, the `runner` agent, and the four `project-*` skills.
  Nothing in it mentions a spec.
- **`profiles/specs/`** is the old `spec-me` profile minus those: the six `spec-*`
  skills, `spec-builder-rules.md`, the `spec-*-rules.md`, the spec templates, `.specs/README.md`, and
  the `architect` and `test-writer` agents.
- **`profiles/` is now profiles only**, beside `builder-dev-rules.builder.md`. There is no mandatory
  block left.
- **`project-ground-rules.md` moved from `profiles/general/` to core.** It was optional; KISS, no guessing and
  one thing per change are the base, so they come with the base.
- **`runner` takes its command from the caller**, falling back to wherever the project documents its
  commands, instead of naming `.specs/02-tech.md` outright. It works in a setup with no specs now.
- **`project-test-setup` skips its spec checks** rather than failing them where `specs`
  was not installed.

### Profiles you drop in
- **A profile is a folder now, not files a prompt copies out.** Copy it to `.agents/profiles/<name>/`
  and run `project-sync-profiles-and-skills`; it links the profile's skills, rules and agents where both
  tools look. Delete the folder, run the sync, and every link goes with it — that is the uninstall.
  Want part of it? Delete a subfolder. Want to change it? It is a text file in your repository, and
  nothing installs over it.
- **`spec-core` is `core`**, and it is the only profile whose files are placed, because
  its content is forms about the project and the files both tools read first.
- **`project-link-skills` is `project-sync-profiles-and-skills`**, and one `sync.py`
  replaces the bash and PowerShell pair. Its rule is **one writer per destination**: a skill reaches
  `.agents/skills/` from exactly one place, and a single pass serves Claude from there.
- **An on-demand rule carries its own `when:`**, and the sync rebuilds `LOADER.md`'s table from the
  rules that are actually there, between markers, leaving the rest of the file alone. A dropped-in
  rule brings its trigger; a deleted one takes its row with it. That was the last thing a folder
  could not keep honest.
- **A `.seed.` is never linked.** Its answer describes the repository, so the sync reports it and an
  agent answers it into place as a real file the project owns.
- **`SETUP.md` shrank.** Step 0.1 no longer walks an add run — it says a profile is a folder, runs the
  sync, and sends the user back only for an unanswered form or a missing spec tree.

### The constitution
- **`CONSTITUTION.md` is a core rule now.** Its four setup-wide principles — *Changing the
  constitution is a red flag*, *Simple beats strict*, *Never argue for strictness*, *Safety and honesty
  aren't strictness* — and the *Which instruction wins* row moved out of `spec-builder-rules.md`
  verbatim.
- **`spec-builder-rules.md` keeps the two that need specs** — *A person's word is enough* and *Specs
  are memory any agent can use* — plus *Specs vs. code*, *One owner per file*, *Where a decision
  lives*, *Every task* and *Keeping it honest*. Its Constitution section now points at core's file.
- **One sentence was reworded, with the user's agreement asked twice** as the constitution's own first
  principle requires: "entering spec-driven development in small steps" became "adopting this setup in
  small steps", because core cannot assume specs. No principle changed.
- **A project that had 0.3.0** copies the four principles and the precedence row into a new
  `.agents/CONSTITUTION.md` and deletes them from `spec-builder-rules.md`.

### Fixed
- **`code-change-review`'s `README.md` is a `.seed.` form**, not a copied file. The profile carries the
  forge-neutral page; a project rewrites it for its own forge, setup steps and troubleshooting, and
  that difference is now by design instead of a mismatch the inventory reports.

### Flattened
- **`blocks/` is gone.** Once every installable file belonged to a profile, that folder held nothing
  but `profiles/`, so `profiles/` moved up to `builder/` and `builder-dev-rules.builder.md` with it.
  The decision that put blocks one level down is kept and marked *Changed*: its reason was to avoid a
  `builder/skills/` that skill globs would match, and a profile folder still avoids it.
- **"Block" is no longer the word.** The docs and the setup prompts say a profile's files. The install
  markers are unchanged — no marker copies, `.seed.` is a form, `.builder.` stays in the builder.
- **`validate_inventory.py` walks `builder/profiles/`** and reports "profile files against installed
  files"; its path mapping now reads `<profile>/<kind>/…`.
- **A project that had 0.3.0** needs no change: nothing installed ever pointed inside `blocks/`.

### Depends
- **A profile declares `## Requires`.** `specs` requires `core`; `SETUP.md` installs
  what a chosen profile requires without a second question, and never asks about core at all — it is
  the base on every first setup.
- **Why the setup's own tooling sits in core:** validate, rule-verify, rule-skill and link-skills score
  and repair whatever a project installed, across every profile it took and every edit it made since.
  They are most useful where a team's process is least standard, which is the wrong place to hide them
  behind a profile.

### Still to come
Two directions are written into `BUILDER-DESIGN.md` under *Parked directions*, not built: installing a
profile onto a project that already has the setup (with a fit check before, and help merging or
replacing what is there), and a validation report a team can share.

## 0.3.0 — unreleased

The setup gets a name. What the builder installs is **spec-me** — spec-driven development — and the
builder is **spec-me-builder**, released from the `spec-me` repository.

### Named
- **The ten skills are `spec-*`, in two families.** The six that work a spec keep their old word:
  `spec-create` → `spec-create`, `spec-implementation-plan` → `spec-plan`, and `spec-merge`,
  `spec-check-style`, `spec-rebuild-overviews`, `spec-sync-with-code` the same way. The four that work the setup itself keep
  theirs: `project-test-setup` → `project-test-setup`, and `project-create-rule-or-skill`,
  `project-resolve-conflicts`, `project-link-skills` → `project-*`.
- **The families are the seam.** `/spec-` narrows to all ten in both tools, `/project-` to
  the four that know nothing about specs — which is the line a later version would cut along if the
  setup's own tooling is split out of spec-me.
- **Grouping is by name, not by folder.** Claude and Codex both need a flat `skills/<name>/SKILL.md`,
  and the `plugin:skill` form is a Claude Code plugin, which Codex does not read.
- **A project that had 0.2.0** renames the ten skill folders, the `name:` in each `SKILL.md` and every
  reference to them in its rules, its map and its own files, then relinks:
  `python3 .agents/skills/project-sync-profiles-and-skills/scripts/sync.py`. Nothing under `.specs/` names a
  skill, so the specs are untouched.

### Packaged
- **`profiles/spec-me/` holds the whole spec system** — the ten skills, `spec-builder-rules.md`
  with the constitution in it, the `spec-*-rules.md`, the spec templates, `.specs/README.md` and the
  `architect`, `test-writer` and `runner` agents. `profiles/skills/`, `profiles/rules/{always-on,on-demand}/`
  and `profiles/agents/` are gone — no skill, rule or agent is mandatory now. `runner` went with the rest
  because it takes its command from `.specs/02-tech.md`, and only `spec-builder-rules.md`,
  `spec-sync-with-code` and `spec-plan` invoke it.
- **It installs whole or not at all**, like `code-change-review`, and `SETUP.md` asks for it first in
  Step 4. Declining it skips Step 3, Step 7 and the `build_index.py` run in Step 8.
- **Declining it costs two things**, written down in its `PROFILE.builder.md`: no always-on rule ships,
  and there is no script to link skills into `.claude/skills/` — `project-sync-profiles-and-skills` carries it.
  Splitting those setup-wide parts into a mandatory core is a later change.
- **`builder-dev-rules.builder.md` sits at `profiles/` directly**, since `profiles/rules/` held nothing
  else once the spec rules moved, and the rule is never installed — `SETUP-DEV.md` links it. A
  developer setup made with 0.2.0 has a symlink pointing at the old path; remake it.
- **The map's three figures are spec-me's** — the spine, ownership and the loop all draw the spec
  process, and the agents table with them. `SETUP.md` Step 5 says to delete them when the profile is
  declined; Encoding, the rest of Reference and Local stay.
- **`build_setup_map.py`, the rule templates and the settings stay in the core.** The script only
  counts what is installed, and `AGENTS.md` → `LOADER.md` is the wiring every profile's rules need —
  `code-change-review`'s form and a stack's code-style rule load through the same loader row mechanism.
- **`.agents/README.md` is a form now** (`profiles/README.seed.md`): its `<!-- spec-me -->` sections are
  kept or deleted at install. `AGENTS.seed.md` and `LOADER.seed.md` mark their spec parts the same way.

## 0.2.0 — unreleased

The first release: a spec-driven agent setup for Claude and Codex, installed into any project by an
agent, once.

### Setting up
- **`SETUP.md`** is the prompt that sets up a project from `builder/`, once.
  - It surveys the codebase, picks the stack profile, and offers the optional skills — for everyone
    or only for you.
  - It installs every block where the README tree says, answers each form by reading the code, and
    writes the root specs.
  - It writes the builder version to `.agents/SETUP-VERSION`, reports anything still unanswered, and
    deletes `.agents/builder/`.
- **`SETUP-DEV.md`** switches a project between the user setup and the developer setup, for the builder's developer.
  Switching in, it compares the project with the builder once, asks which way each difference goes,
  and links a local rule that makes every later setup change in the builder too — tree, design and
  changelog included. Switching back removes the rule and the builder.
- **No update step.** A project takes a newer builder by comparing it by hand, or by asking an AI to.
- **One constitution.** The *Constitution* section of `spec-builder-rules.md` is the only source, copied
  at install with the rest of the file.
- **One model for guidance.** Each piece is mandatory or optional, and always-on or on-demand. An
  on-demand rule loads by a `LOADER.md` row, a skill only by its description — never both — and which
  instruction wins is stated once, in `spec-builder-rules.md`. Two rules or skills saying different
  things is a bug to settle in the files, not a ranking table: Claude Code's and Codex's own guidance
  works the same way.
- **`project-create-rule-or-skill`** decides what kind a piece of guidance is and where it goes, and writes and
  reviews rules and skills to one shape — triggers first in the description,
  non-negotiables, checkable steps and stops, a word budget its `skill_stats.py` counts — and tests a new
  skill, or a changed description or steps, with a fresh agent unless the user skips it. A changed skill
  keeps its old text and is run against it, so a fix never leaves it worse or stricter than its rule; a
  change to skills that hand work to each other keeps a copy first, walks the flows they share, and
  compares `project-test-setup` before and after when the user wants it. A changed skill the user relies
  on is backed up and run against the old one on the same real prompts, two runs each, graded blind;
  the user sees the outputs and decides, with the new recommended only if it does the same or better. It holds the rules for changing
  the setup itself, so no rule file is read for that.
- **`project-resolve-conflicts`** finds installed rules and skills that say different things, compete for the
  same request or load the wrong way, and settles each with the user — keep one, narrow one, or merge
  them. Setup offers it when optional rules or skills were installed.
- **`project-test-setup` gives the same depth every run**: a `validate_inventory.py` script collects the mechanical facts — load, budgets, blocks against installed files, retired names, missing paths, links — each check walks a fixed list of comparisons, scores come from the findings by formula, readers get only the skill and their check, settled choices live in a local `validate-accepted.md`, every run first rechecks a local findings ledger, `validate-findings.md`, and every reader asks the same questions and rates by the same examples, both in `reference.md`. The score counts only the ledger's open findings and the inventory script works it out, so two runs over the same setup score the same; new findings and fixes count from the next run. `--write-score` keeps the current score at the top of the ledger.
- **`project-test-setup`** reviews the whole setup on request, read only: it tests the rules, skills and
  spec process against the constitution, and reports a score, token load, what could be simpler and
  what's left over — each proposal with its reason and a small draft.
- **Free rearranging.** There is no script or manifest, so blocks can be moved between folders,
  renamed and regrouped. The README tree is the only record of where each block lands.
- **Install kind in the filename.** A file with no marker is copied, `.seed.` is a form the project
  fills in, and `.builder.` stays in the builder.
- **No mandatory file names an optional rule or skill, and an optional one names no other.** An optional
  on-demand rule is wired in by a `LOADER.md` row, kept only where it was installed.

### The spec system
- **The `.specs/` tree**: a product, architecture and tech spec, then contract and feature specs.
  Every spec declares the code it owns.
  - **`.specs/README.md`** describes the specs for any agent or person — finding the spec for a file,
    reading one, changing one — so they work as memory without this setup. It follows the rules and
    skills that define the process: a change to how specs work updates it in the same change.
  - The feature, contract and implementation-plan templates are installed, for the spec skills. The three root-spec
    templates are `.builder.` files: `SETUP.md` reads them once, and nothing needs them after.
  - `02-tech.md` holds the build, test, lint and format commands. `AGENTS.md` holds only the project's
    name, one line on what it is, and the pointer to the rule loaders.
- **Rules**:
  - `LOADER.md` in each rules folder, shared and local, saying what loads and when — `AGENTS.md`
    only points at the two;
  - `spec-builder-rules.md`, the one mandatory always-on file: the constitution, outranking every other
    rule — this version is for entering spec-driven development in small steps, so no agent argues for
    strictness, while asking before a sensitive path or a destructive action stays — which instruction
    wins, the every-task flow, and keeping specs honest;
  - optional, chosen at install: `project-ground-rules.md` (KISS, no invented facts, scope, saying "I don't
    know"), and `project-sensitive-paths-rules.md`, the files an agent must ask before touching — `.agents/core/rules/`
    among them, so both tools ask, not only Claude;
  - `spec-format-rules.md` and `spec-style-rules.md` — a short drafting checklist, its reasoning and
    examples kept with `spec-check-style` — read before writing a spec;
  - `spec-change-rules.md`, read before starting, planning, building or folding in a change — how a merge
    is done lives in `spec-merge`, the only one that does it; `spec-sync-with-code` counts a criterion a person
    confirmed as holding unless the code plainly differs;
  - `spec-architecture-rules.md`, read before a design choice — a proposal compares approaches only
    when there is a real choice;
  - optional project forms `project-workflow-rules.md` and `project-code-style-rules.md`, read before
    the work they cover.
- **The person in chat approves**, merges and decides — the README says "the user" throughout, and a
  build with no plan ends when the criteria are built, naming those still waiting for the user's word.
  A change of mind mid-build doesn't stop building unless it goes back to draft or the user says stop; a
  spec written from code skips the module-split step; a task reads a spec where it sits, in a change when it has moved there, and the plan only when building.
- **Wording settled after a second full review**: "merge" alone may mean a git merge, so `spec-merge`
  asks; `updated:` also moves when a design is recorded alongside its code; the architect proposes one
  obvious way as such; a spec change can be abandoned on the user's yes, by moving its specs back unedited and deleting its folder.
- **Changes**: every edit to what a spec guarantees goes through `.specs/changes/<branch>/` (a second change on it: `<branch>-<topic>/`) — each spec it
  touches, moved in with `git mv` so git and the IDE show every edit as a diff, with its why in a `## Change` section, and one `implementation-plan.md` —
  design, then tasks — only when the work needs it. It folds in by moving each spec back to its place, so a spec at its place always describes the code as it is. Work across modules gets a contract spec, and each change folds in on its
  own; deleting a story folder never deletes a change nested in it. Reports to the user use plain words, not phase or skill names.
  - A `merged` spec the code has moved past, with the code right, is corrected in place — a Change
    history row, "No ticket" when there's none — without a change. A design outside a change is agreed
    in chat and recorded in `01-architecture.md` the same way.
  - A contract's Implementation table names who takes part and their role; the features' own criteria
    say which contract criteria they carry, and a contract criterion is checked once those are, or by its own
    proof — confirming it by hand confirms them too.
  - A task is an instruction in plain words, tagged at the end with the criteria it closes, if any. A
    check only a person can make turns it into a checkpoint, so building pauses where you want to try it.
  - **Changing course is part of the flow.** A design is rewritten, with the old approach kept as a
    `Not` line saying what was learned; built work changes through a new task, since a ticked one is
    never rewritten; an edited criterion keeps its approval on the user's OK, and a task changes
    its tests or code where they no longer match. A new criterion's id is one past the highest.
  - `.agents/README.md` walks through a change's steps and who approves what, so a person new to the
    setup sees the flow without reading the rules first.
- **Every spec has a `status`**: `draft` and `approved` in a change, `merged` once folded in — so any
  single file says how far it has come. Approval is per file; approving one asks whether the rest go too. A spec written from code that already exists goes from `draft`
  straight to `merged`, since there is nothing to build. Nothing folds in unconfirmed: each unchecked
  criterion is confirmed by the user as `Source: Manual`, dropped, or the change stays open.
- **A checkbox shows its proof**: each criterion lists its proof under `Verified:` — a test file with its
  tests, or `Source: Manual` with an optional description — and `[x]` means it holds at least one;
  `spec-rebuild-overviews` warns when the two disagree.
- **Rule files end in `-rules`**, so a rule reads as one wherever it's referenced.
- **Generated overviews stay out of git.** `.specs/.gitignore` keeps `INDEX.md`, `DECISIONS.md` and
  `OPEN-QUESTIONS.md` local, so branches never conflict on them, and they can show what only one machine
  knows, like the last `spec-sync-with-code` result.
- **Spec skills**:
  - `spec-create` starts every change — a new feature, a changed one, or code that exists — working out
    which itself, through one approval only the user gives, and corrects a stale spec in place;
  - `spec-plan` writes a change's plan with the user, the `architect` subagent proposing,
    builds from it when asked, and changes it mid-way; a task whose only proof needs something outside the
    session — a real tag push, MR pipeline or device — is split into a code task and a check-only task;
  - `spec-merge` folds a change into its specs by moving them back, keeps what its plan decided, and
    deletes the folder;
  - `spec-sync-with-code` checks a spec when asked, and is offered when a task relies on one marked possibly stale.
    It runs in the background — its tests run, its code read for the rest — and records the result for `INDEX.md`;
  - `spec-check-style` checks specs against the style rules;
  - `spec-rebuild-overviews` generates `INDEX.md`, `DECISIONS.md` and `OPEN-QUESTIONS.md` — helpers, where the specs
    win any disagreement — the last two grouped by spec so a task reads only the sections it touches;
  - each spec skill opens with its non-negotiables, so the rules that stop an agent deciding on its
    own apply without following a citation.
- **`spec-rebuild-overviews --check`** fails only on the tree's structure — dangling globs and ids, ambiguous
  ownership, a change's spec file that can't land where it's named. The rest it reports
  without failing, among them constraints recorded as currently violated, and Change history rows too
  long to be one sentence.
  A manual test plan kept beside the spec it tests, `<spec>.manual-test-plan.md`, isn't read as a spec.

- **One answer per question across rules, skills and READMEs**:
  - approval is per file everywhere, and `updated:` moves on the same four events everywhere;
  - criteria are *checked*, tasks and open questions *ticked*;
  - "combine" for two rules or skills, and "merge" for specs and git;
  - `project-test-setup` reports *constitution conflicts*, so "red flag" keeps its one meaning;
  - `.specs/README.md` gains the one-line-fix exemption, `ticket:` for a new spec, the check-only task, the doc-comment `Resolved:` form, and the emptied story folder going with an abandoned change;
  - `project-create-rule-or-skill`'s *Wiring* names the README section to update and re-reads a changed skill's description against its body, so these copies stop drifting.

- **Less read twice**: inside an open change an agent reads the change's copy and `diff`s it against the spec instead of reading both; `spec-create` reads the change rules only if not already read; the architecture rules load only for a real design choice; editing only `owns` or `updated:` loads no format or style rules; skill steps point at the rules they used to copy; `spec-check-style` opens a `reference.md` entry only when the checklist doesn't settle a finding.

### Agents
- **Agents for both tools**: `architect` reads and proposes, never edits, `runner` runs build, lint and tests and
  reports failures, and `test-writer` derives tests from acceptance criteria, finding the stack's
  testing skills in `.agents/skills/`.
- **No hooks.** Nothing runs on its own in one tool only: `spec-rebuild-overviews` rebuilds the spec index, and
  `build_setup_map.py` the map, as steps both tools follow.
- **An optional skill may bring its own agents**, from a profile's `agents/claude/` and
  `agents/codex/`, installed only where that skill was chosen. `profiles/agents/` keeps the three every
  setup gets. The reason is cost: an agent's description sits in every session whether or not anything
  can invoke it, so an agent nobody has the skill for is pure load.
- **`reviewer-business`, `reviewer-technical`, `reviewer-security`**: the three read-only lanes
  `code-change-review` runs, each with its model and effort pinned so two people get the same reviewer.
  None of them may edit a file or post anywhere; the main session verifies the load-bearing claims and
  owns the verdict. A local review always uses a lane that did not author the candidate, which is the
  property a subagent buys and a skill cannot.

### Profiles
- **`general`**: optional skills for any stack — `session-snapshot`,
  `code-query-dependencies` (named `project-query-dependencies` until 2026-09-16, when `project-` came to mean
  the setup's own skills), `docs-readme` — one structure for READMEs, ARCHITECTURE.md and now
  `RELEASING.md` (a module's own release process — team-internal, never shipped to or named from its
  README) — and `one-head-good-two-better`, a second look at a go-ahead with no agreed plan behind it.
  `docs-readme` also gained a rule against restating what a file's own name or a line just above it
  already makes obvious. `test-plan-manual` is new: it turns a runbook, or a plan's tasks whose only
  proof needs a real MR, tag push, device or registry, into numbered, checkboxed test cases —
  Preconditions, Steps, Expected, an optional Result that keeps one line per run worth noting, so a retest shows what changed,
  and, only where an implementation-plan.md exists, the task each closes; it works the same with no
  `.specs/` tree at all. A person reports a case's outcome in their own words, and the agent adds it
  under that case's Result. `one-head-good-two-better` also fires
  mid-task, before adding real scope to guard against a failure mode nobody has actually reported —
  learned from a session that kept elaborating a CI staleness guard for drift that had never happened.
  `docs-incode` is its own small skill for comments.
- **`code-change-review` is a profile of its own, installed whole.** Its skill, its three lane agents
  and its form rule move out of `general/` into `profiles/code-review/`, offered as one yes or
  no. A subset installs something that looks like a reviewer and is not one: without the rule it has no
  forge, no requirement sources and no way to obtain a build, so every finding degrades to prose. This
  is the first profile that is not a stack.
- **`code-change-review`** is new: one merge or pull request, or a branch before a request exists, through
  business, technical and security lanes, reporting Required / Must to have / Cosmetic with
  `path:line` evidence and posting only what the user picks. Three gates decide severity before a
  category is assigned — pre-existing against the immutable base, reachable in the shipped build
  through the flag guarding the call site, then PROVEN against INFERRED — so a finding has to survive
  all three to block a merge. Every write to a forge or tracker waits for an explicit selection, code
  suggestions need an executed red-then-green, and a finding justified only by performance or tidiness
  needs a measured benefit or it stays out of the request. It runs the other direction as well: a
  response mode works the comments left on a request one thread at a time, triaging each through the
  same three gates, closing it with a code change, a document change or both, and replying with what
  was done and why. That is the one mode allowed to edit the author's code, per fix and per approval,
  and it never resolves a thread it disagreed with. Forge mechanics and the local and response modes
  live in its `reference.md`; GitLab is the forge written up so far. Ported from a working
  personal setup and measured against the reviews it had already produced.
- **Optional skills name no other skill.** Each profile skill's **Not for** names the work, never a skill,
  so a skill reads and works the same whatever else is installed; mandatory skills still name each other
  as steps of their flow. Their one line that the project's rules come first now points at `AGENTS.md`,
  the entry both tools already read — so a skill that fires mid-session brings the loader back with it,
  while still naming no rule file. A skill that only reads and reports carries no such line.
- **`kotlin-android`**: stack detection and tool commands, a `project-code-style-rules` form, and
  the `test-unit`, `test-integration`, `compose-create` and `code-clean-kotlin` skills —
  `compose-create` gained a *Files* rule — a screen, its UiState and each sizeable sub-component in their
  own files, nothing past ~400 lines — and numbered steps ending in its checklist, with the template in
  `reference.md`; tested blind against the previous version, two runs each, it built smaller files with
  no broken rules and reviewed about as well. Its focus rule also keeps a dialog's focus target only while
  the dialog is open, a control inside a toggleable row takes no focus of its own, and the checklist asks
  every screen and component for a `modifier`.
  `code-clean-kotlin` is the one clean-code skill, kept short on purpose: follow Clean Code principles and
  Kotlin idioms, flat lambdas and flat control flow (a nested branch or a Boolean flag becomes a named function), a repeated condition as one named extension or function, KISS, robust,
  complete — and a `stale_refs.py` sweep that lists removed declarations still
  mentioned anywhere. Clean code lives per profile, not in `general`: another stack's version starts from
  this one.

### Personal and visual
- **`answer-format-rules.md`**, optional and always-on, shapes replies in one place: the verdict first, a choice only when it isn't settled or easy to change (numbered, lettered, the recommended one `A` with ⭐), one issue as **Issue** and **Fix** with only what the user must act on, several findings as one table ranked by cost times how often with the steps after it, full results with a summary beside them, and plain everyday words — which `docs-incode`, `docs-readme` and `spec-style-rules.md` ask of comments, READMEs and specs too. It replaces `off-the-fence-rules.md`.
- **Only `rules/` and `skills/` are plain folders in `.agents/`**, and `builder/` where its developer keeps it. `.local/`, `.scripts/`,
  `.templates/` and `.cache/` start with a dot.
- **`.agents/.local/`**: gitignored, and created at install with an empty `LOADER.md`.
  - It holds personal rules and skills that are never shared or synced.
  - `project-sync-profiles-and-skills` links skills for both tools, local ones included, and keeps the local
    links out of git.
- **A profile holds optional rules as well as skills**: `profiles/general/rules/` and
  `profiles/<stack>/rules/` hold optional rules alongside `skills/`, asked and installed the same way
  — everyone, only the user, or skip. `profiles/rules/` at the top level, outside any profile, stays
  mandatory for every project. `profiles/general/rules/always-on/` holds `project-ground-rules.md`,
  `project-sensitive-paths-rules.seed.md`, `answer-format-rules.md` and `one-head-good-two-better-rules.md`.
- **The setup map**: an HTML page showing what loads when, and why.
  - `build_setup_map.py` keeps it current. Its every-session total counts what really loads — `AGENTS.md`,
    `CLAUDE.md`, the loader, the always-on rules and every shared skill's description — and its spec count
    leaves out the specs inside open changes.
  - Local files show in their own section, from `.agents/.cache/map-local.js`.
