# Specs

What this codebase guarantees, written down so any person or agent can rely on it and keep it true.
Plain Markdown: no tool, skill or script is needed to read a spec or to change one.

## What's here

```
.specs/
├── README.md             this file
├── 00-product.md         what the product is, who it's for, what it won't do
├── 01-architecture.md    modules and the boundaries between them
├── 02-tech.md            stack, commands, testing conventions
├── feature/              one spec per feature, nested freely
├── contract/             behaviour that spans several modules
├── changes/              specs being written or built, not merged yet — one folder per change
└── INDEX.md  DECISIONS.md  OPEN-QUESTIONS.md    generated overviews — optional, never committed;
                                                 when one looks stale, the specs win
```

## Find the spec for a file

- **By `owns`:** a spec lists the code it describes under `owns:` in its frontmatter. Search for a
  glob that matches the file; the most specific match owns it.
- **No match** is normal: much of the code may have no spec yet.
- **Check `changes/` too:** a spec being changed moves there — `specs.feature.logger.md` for
  `feature/logger.md` — and is missing from its usual place until the change merges.

## Read a spec

Frontmatter:

- **Always:** `id` — unique and dot-namespaced, like `feature.logger`; `title`; `status`; and `parent` — the
  id of the spec above it.
- **Optional:** `owns` — the code it describes, `[]` or left out when it owns none; `related`; `ticket`;
  and `updated` — the day it was last confirmed against the code.

`status` says how far a spec has come:

- `draft` — being written or designed; not approved yet.
- `approved` — the user said yes; the code may be built to it.
- `merged` — describes the code as it is now.

A spec outside `changes/` is `merged`; one inside is `draft` or `approved`.

Sections, each present only when it has something real:

- **Change** — only in a spec inside `changes/`: why it is being written or changed.
- **Intent** — what it guarantees to the rest of the system, not how — and, for a feature that carries
  part of a contract, which contract.
- **Acceptance criteria** — each a named *Given / When / Then*, with its proof under `Verified:`:
  - **Automated proof:** `Source:` a test file, with its test names under it.
  - **Manual proof:** `Source: Manual`, with an optional description, like who or where.
  - **Checkbox:** `[x]` when `Verified:` holds at least one source, `[ ]` when it holds none, or while a reworded criterion's tests are still to be changed — except a contract criterion (below).

  ```markdown
  - [x] **AC-1: A dropped upload is retried once**
    - **Given** an upload in progress
    - **When** the connection drops
    - **Then** it is retried once, then reported as failed
    - **Verified:**
      - **Source:** `UploadRetryTest.kt`
        - `when the connection drops then retries once`
      - **Source:** Manual
        - Dana, on a device, build 1.4.2
  ```
- **Constraints** — obligations a change must not break.
- **Public surface** — who may use what.
- **Decisions** — a choice, and what it ruled out under *Instead of*. Don't bring back a rejected
  option without saying so. Revising one: edit it in place and add `Replaced {date}:` with what it
  overturned.
- **Open questions** — undecided, each a `[ ]` checkbox with an *Action*. Never settle one by guessing;
  ask. Once answered, tick it, strike it through, add `- Resolved: see Decisions → "{name}"` — or `see the doc comment in {file}` for a file-scoped answer — and leave it in place.
- **Pitfalls** — what a reader would get wrong; **References** — pointers; **Change history** — a table with one row
  per change in documented behaviour or requirements: the ticket, one sentence and the date.

A contract spec (`contract.*`) owns no code, has an **Intent** like a feature, and adds **Source** — where it came from — and
**Implementation** — which features and modules take part, and their role; which criteria each carries is
named in the features' own criteria. A feature criterion that implements one of its criteria
names it, like `(contract AC-2)` — or `` (`contract.x` AC-2) `` when it relates to several contracts; the contract criterion is checked by its own proof or, when feature criteria
name it, once all of them are. Confirming it by hand confirms the unchecked ones too, as `Source: Manual`,
wherever the spec sits, in `.specs/` or in an open change.

## Change what a spec guarantees

- **Through a change:** a new spec, or a change to Intent, Acceptance criteria, Constraints or Public
  surface worth finding later.
- **Edited in place:** everything else — a typo, a Decision, an Open question, a criterion's proof, a one-line fix, a fix that
  makes the code do what a spec or an open change already says.
- **A spec behind code that's already right:** corrected in place on the user's yes — which confirms criteria
  without proof, or reworded, as `Source: Manual`, never one for something not built — with a Change history row (its ticket, or "No ticket")
  and `updated:`.
- **Not sure which way?** Ask whether the code is already right: if it is, an existing spec is corrected
  in place and a missing one is written from the code in a change; if not, the code follows the spec, through a change.
- **Keeping it honest:** code moved or deleted → update `owns`; a listed test renamed or removed → update its
  `Source:`; something a spec records as broken or pending fixed → correct every line that describes it.

1. **Open a change**
   - **Where:** a folder `.specs/changes/<branch-name>/` — a second change on the same branch adds what
     it's about: `<branch-name>-<topic>/`.
   - **Holds:** one file per spec it touches, named after where it lands with dots for slashes —
     `specs.feature.logger.md` lands at `.specs/feature/logger.md`.
   - **Each file:** the whole spec as it should read afterwards — the existing spec, moved in with
     `git mv` (plain `mv` where `.specs/` isn't in git) before it is edited, so git and the IDE show
     each edit as a diff; or a new one.
   - **Starts with:** `status: draft`, and a `## Change` section under its title saying why — for a new spec, its ticket in `ticket:`.
   - **Already in another open change:** edit it there, or wait for that change to merge.
   - **Nested folders:** a folder may group one story's tickets; each folder holding spec files is a
     change of its own, and merges on its own, in any order.
2. **Plan it** — once the user says the spec files read right, and only when the work needs
   a design or is worth splitting: `implementation-plan.md` in
   the folder.
   - **`## Design`:** how the specs become true, with each option not taken as
     `- **Not {option}:** {why}`.
   - **`## Tasks`:** numbered checkboxes in the order they run, each an instruction. An optional tag at the end,
     like `[AC-3]`, names the criteria a task closes — with the spec's name when the change holds several,
     like `[contract AC-2]`; an optional `- Check:` line under it names a test,
     or what to try by hand. A check needing a real push, pipeline or device is a task of its own.
   - **When needed:** `## Not in this change`. Anything undecided is an Open question in the spec.
   - **A new module, boundary or library:** `01-architecture.md` or `02-tech.md` moves into the
     change too; say so to the user before touching build files.
   - **A story folder with a contract:** its Design is the flow across modules, and its tasks are the
     module changes.
3. **Approve**
   - **Who:** the user — the person the agent is working with — reads each spec file, and the plan.
   - **Approving:** set `status: approved` on each file the user approves, and ask whether the rest go too;
     the plan is approved once every spec file is. Asking for a draft to be built approves it.
   - **A spec written from code that already exists:** approving it confirms its unchecked criteria as
     `Source: Manual`, unless the user says otherwise, and merges it, folder and all — go to step 5. A criterion for something not
     built yet is ahead of code: build it first, or drop it to a later change; the approval never confirms it,
     and a change that also holds work to build merges once that's built.
4. **Build**
   - **Tasks:** in order, re-reading the plan, and any spec file edited since, before each one. A task only a person can check waits
     for them, and what they saw goes on its Check line. If it didn't hold: fix it and try again, or change course
     when the design was wrong.
   - **Ticking:** a task when its checks hold. One blocked by an Open question waits; build what isn't
     blocked, and report it.
   - **No plan:** the criteria are the work; build each, add any proof a test gives, and say in the report
     what code was kept or dropped and which criteria wait for the user's word.
   - **Criteria:** add each one's proof under `Verified:`, and check it.
   - **Code behind its spec** while tasks — or, with no plan, criteria — are still open is expected, not a conflict.
5. **Merge** — when the user says it's done:
   - **Each spec file:** set `status: merged` and `updated:`.
   - **Its `## Change` section:** becomes a Change history row on an existing spec whose documented behaviour or requirements changed, or
     is deleted.
   - **Unchecked criteria:** each gets its own answer — the user confirms it (`Source: Manual`), drops it
     (into an Open question when it's still wanted), or the change stays open. A spec written from code's
     approval already gave these answers.
   - **Unticked tasks:** listed to the user.
   - **The plan:** a `Not` line someone reading only the code would propose again becomes a Decision in the spec, a flow across modules
     goes into the contract spec, and a module's non-obvious invariants into its `ARCHITECTURE.md` where it has
     one; the rest goes with the folder.
   - **Then:** `git mv` each file back to its place in `.specs/`, and delete the folder on the user's yes — only its own files while another change is nested
     in it; a folder left empty goes too.
   - **A removal:** a Change section that removes the spec deletes it instead.
- **Abandoning a change:** on the user's yes, move each spec it moved in back to its place with its
  edits undone — `git mv` it back, then `git checkout <branch it will merge into> -- .specs/<path>` —
  then delete the folder — only its own files while another change is
  nested in it; a folder left empty goes, the story folder above it included.

### Changing course

Any time before merging:

- **Pending tasks:** edit, add, reorder or delete them.
- **The design:** rewrite it to what's true now; the old approach becomes a `Not` line saying what was
  learned. A new module, boundary or library moves `01-architecture.md` or `02-tech.md` into the change.
- **Something already built:** a ticked task is never rewritten or unticked. The rework is a new task,
  placed among the pending ones where it should run.
- **A criterion edited:** in the user's own words, or a proposed wording they OK — either keeps its
  status. Its manual proof is cleared, and it's unchecked if no
  proof is left; its tests stay while they still check the new
  wording; where they or the built code don't, a new task changes them, and it's unchecked until that
  task is ticked — with no plan, until they're changed. Pending tasks tagged with it are edited to fit.
- **A criterion removed:** pending tasks tagged with it are deleted or re-tagged, and tests only it listed are
  named. If its code is already built, the
  user decides whether it goes — a removal task — or stays, noted under Not in this change. With no plan, kept code is said in the report.
- **Criterion ids:** a new criterion takes one past the highest id in the spec, and a task when there's a plan — a removed highest id can come back. A ticked task's tags name the criteria as they
  read when it was ticked.
- **Back to draft:** only the user sets `status: draft`, to rethink. Building stops; a half-built task stays unticked, its code as
  it is, said in the report. Approving again approves the spec and its plan; building continues
  from the first unticked task when the user asks.
- **The work reaches another module:** say so, and ask whether it becomes another spec file here or a
  change of its own.

## Why another spec format?

Same idea. Less paper.

| Per change | OpenSpec | Kiro | Ours |
|---|:---:|:---:|:---:|
| Files to write | 3 | 3 | **1** (2 with a plan) |
| Approval gates | 1 | 3 | **1** |
| Files left behind after merge | 3, archived | 3, forever | **0** |

| | OpenSpec | Kiro | Ours | + Simpler because | − Costs us |
|---|---|---|---|---|---|
| **A change** | delta blocks + `proposal.md` + `tasks.md` | permanent `requirements.md` + `design.md` + `tasks.md` | the spec itself, moved in and edited | `git mv` a file, done | a diff, not delta blocks |
| **After it lands** | change archived | docs kept forever | spec moved back, one decision line kept in it | one place to read | rationale lost unless written into a Decision |
| **Approval** | 1 gate | 3 gates, in sequence | 1 status per file | nothing to sequence | design not gated — flaws caught mid-build |
| **Cross-module work** | no concept | no concept | `contract` spec | tickets land independently | one more spec kind |

**Why ours:** one merged spec beats a pile of documents — OpenSpec's archived proposals nobody
reopens, or Kiro's per-feature files that keep growing and can drift from what's actually true. A
curated Decision lives right next to the guarantee it explains. The real risk is skipping that
write-up, not the missing archive — the original is still in `git log` either way.

**Why it's easy to adopt:** no required tooling, and partial coverage is normal, not an error. A team
new to spec-driven work can write one spec file and go, no CLI or three-gate flow to learn first. A
big existing project gains specs one module at a time, confirmed from the code that's already
there — no big-bang migration.

### Converting out

Not locked in — same Markdown shape everywhere: frontmatter, named sections, criteria with ids.

- **Specs → OpenSpec/Kiro baseline:** rename + reformat. Minutes.
- **Open change → delta or design+tasks:** diff + split. Minutes.
- **Merged spec → permanent design doc:** doesn't exist — write it, don't convert it.
