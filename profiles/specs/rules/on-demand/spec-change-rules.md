# Spec change rules

How what a spec guarantees changes — the source for this setup. `.specs/README.md` describes the same
process for people and agents without it, and follows this file. The spec files a change carries follow
`spec-format-rules.md` and `spec-style-rules.md`.

## What goes through a change
A new spec, and any added, changed or removed guarantee worth finding later — Intent, Acceptance criteria, Constraints,
Public surface. `spec-create` writes the spec files, `spec-plan` plans and builds, and
`spec-merge` folds the change in.

Edited directly, with no change: a typo or a stale reference; a Decision, Open question, Pitfall or
Reference; a criterion's checkbox or its `Verified:` proof; a one-line fix; and a fix that makes the code do what a spec
or an open change already says. A `merged` spec the code has moved past, with the code right, is
corrected in place too (spec-builder-rules' *Keeping it honest*).

**Which direction.** "Update the spec" can mean the requirements are changing, so the code will
follow, or the code is already right and the spec is stale — then an existing spec is corrected in place, and
a missing one is written from the code in a change. When the request doesn't say, ask whether
the code is already right before starting either.

## Stages
| `status` | Means |
|---|---|
| `draft` | Not approved yet — the spec files are being written, then the implementation plan once the user says they read right |
| `approved` | The user said yes — building happens here, changes of course included |
| `merged` | Merged into `.specs/` — describes the code as it is |

- **Ahead of code:** draft → approved → merged.
- **A new spec from code:** draft → merged. There is nothing to build: the user's yes confirms the reading —
  its unchecked criteria included, as `Source: Manual`, unless they say otherwise — and the change
  merges, folder and all. A criterion describing something not built yet is ahead of code: build it
  first, or drop it to a later change — the yes never confirms it, and a change that also holds work ahead of
  code merges once that work is built.
- **Back to draft:** only the user sets it. Building stops; ticked tasks and the code stay, and a half-built task stays
  unticked with its code as it is, said in the report. Approving again approves the spec and its plan; building continues from the first unticked task when the user asks.

## The folder
`.specs/changes/<branch name>/` — the branch's own name: `PROJ-1234-Saved-Searches`, or
`Saved-Searches` with no ticket. With no branch yet, use the name it will get, and ask for the ticket
if there is one. A second change on the same branch adds what it's about: `PROJ-1234-Saved-Searches-Settings`.
Templates: `.agents/profiles/specs/templates/`.

```
PROJ-1234-Saved-Searches/
├── specs.feature.saved-searches.md    a new spec, landing at .specs/feature/saved-searches.md
├── specs.01-architecture.md           .specs/01-architecture.md, moved in and edited
└── implementation-plan.md             optional — the design and the tasks
```

- **A spec file is the whole spec as it should read afterwards** — the one in `.specs/`, moved in with
  `git mv` (plain `mv` where `.specs/` isn't in git) before it is edited so git shows each edit as a
  diff, or a new one from `spec-feature.md` or `spec-contract.md` — with `status: draft` and a `## Change` section
  under its title: why, in a sentence or two, and, for a new spec, its ticket in `ticket:`. Never a list of edits to apply.
- **A spec already in another open change** — edit it there, or ask whether to wait until that
  change merges; a spec is in one change at a time.
- **A question spanning several specs** goes in the contract spec they share, or in the spec it blocks.
- **Folders may nest** to group one story's tickets; each folder holding spec files is a change of its own.
  Each merges on its own, in any order; a spec that names one still in a change reads it there. Deleting
  a folder — once merged, or abandoned after each spec it moved in has gone back to its place with its
  edits undone (`git mv` it back, then `git checkout <branch it will merge into> -- .specs/<path>`) — removes its own spec files and plan, never a change nested in it; a
  folder left empty goes, the story folder above it included.

## Approval
`status: approved` in a spec file, set only on the user's yes in chat, per file — approving one, ask once
whether the rest of the change's files go too. The plan counts as approved once every spec file is. The user asking to build a draft is that yes: set `approved`, and say so.

## Implementation plan
`implementation-plan.md`, from `.agents/profiles/specs/templates/implementation-plan.md` — only when the work needs a
design or is worth splitting.

- **Design** — how the spec files become true: a sentence for a small change; for a big one,
  sub-headings such as Flow, Interfaces, State, Concurrency and failure, or Security, with Mermaid for
  diagrams and interfaces as signatures, only where they cross a module or process boundary.
  - **Each option not taken:** `- **Not {option}:** {why}`. A choice someone reading only the code would
    propose again is also a Decision in the owning spec file, written as it's made.
  - **A new module, a moved boundary, a new library:** `01-architecture.md` or `02-tech.md` moved into
    the change, flagged to the user. Build files are sensitive paths.
  - **A story folder holding a contract:** its Design covers the flow across modules and which module
    change carries which contract criteria; its tasks are the module changes. A module's own plan covers
    that module only.
- **Tasks** — numbered checkboxes, each an instruction in plain words, in the order they run.
  - **Tags:** at the end and optional — `[AC-3]`, `[AC-3, AC-4]`, or `[contract AC-2]` naming the spec when it
    isn't the change's only one. A task may close no criterion.
  - **Checks:** optional `- Check:` sub-bullets — a test name and its file, or what to try by hand. A
    check only a person can make turns its task into a checkpoint. A check that needs something outside
    the session — a real push, pipeline or device — is a task of its own, holding only the check; the
    code task ticks without it.
- **Not in this change** — what a reader would expect and won't find. Something undecided is an Open
  question in the spec file it concerns.

## While building
- **Order:** the tasks in order, re-reading the plan, and any spec file edited since, before each one.
- **Ticking:** a task when its checks hold. A checkpoint waits for the person; what they saw goes on its
  Check line.
- **Proof:** a passing test goes under its criterion's `Verified:`; a person's confirmation as
  `Source: Manual`.
- **Blocked:** an Open question blocking a task is never settled by picking an interpretation. Build what
  isn't blocked, and report the rest.

## Changing course
At any stage before merging:

| What changes | What to do |
|---|---|
| Pending tasks | Edit, add, reorder or delete them. |
| The design | Rewrite Design to what's true now; the old approach becomes a `Not` line saying what was learned. The pending tasks follow. A new module, boundary or library moves `01-architecture.md` or `02-tech.md` into the change, flagged to the user. |
| Something already built | A ticked task is never rewritten or unticked. The rework is a new task, placed among the pending ones where it should run; fixing a task number another task cites isn't a rewrite. |
| A criterion's wording | The user's own wording is applied and shown; wording you had to interpret is shown and asked first. Either way the spec keeps its status. Clear its manual proof — the person confirmed the old wording. Tests or built code that no longer match get a new task; its checkbox follows spec-format-rules' *How a criterion was confirmed*. Pending tasks tagged with it are edited to fit. |
| A new criterion | One past the highest id in the spec, and a task for it. |
| A removed criterion | Deleted. Pending tasks tagged with it are deleted or re-tagged — say which. Already built: ask once whether the code goes; yes is a removal task, no is a line under Not in this change. Name any tests only it listed. |
| The work reaches another module | Say so, and ask: another spec file in this change, or a change of its own. |

A ticked task's tags are history: they name the criteria as they read when it was ticked, even when an id
has since been removed and given to a new criterion — never updated, never a question. With no plan there are no tasks to add:
rework happens when the user asks to build, and code kept after a removal is said in the report.

## Merging
A change merges when the user says it's done, and every criterion is confirmed first — confirmed by the
user as `Source: Manual`, dropped — into an Open question when it's still wanted — or the change stays
open. How: `spec-merge`.

## Talking to the user
Plain words — *waiting for your OK*, *building*, *ready to fold into the specs* — never "phase",
"delta" or "sub-change".
