# Spec change rules

How a planned change works — the source for this setup. `.specs/README.md` describes the same
process for people and agents without it, and follows this file. Specs follow `spec-format-rules.md`
and `spec-style-rules.md`.

## What goes through a change
Work the user asks to plan (spec-builder-rules' *Two ways to work*). A change is a plan: it says what
will be done. Specs say what is — they stay in `.specs/` and are updated in place as the work is
built, the same as when shaping. `spec-create` opens a change and agrees its requirements, `spec-plan`
designs and builds it, and `spec-merge` folds it in.

**Which direction.** "Update the spec" can mean the requirements are changing, so the code will
follow, or the code is already right and the spec is stale — then the spec is corrected in place, and
a missing one is written from the code. When the request doesn't say, ask in one line whether the
code is already right.

## The folder
`.specs/changes/<branch name>/implementation-plan.md` — the branch's own name: `PROJ-1234-Saved-Searches`,
or `Saved-Searches` with no ticket. With no branch yet, use the name it will get, and ask for the
ticket if there is one. A second change on the same branch adds what it's about:
`PROJ-1234-Saved-Searches-Settings`. Template: `.agents/profiles/specs/templates/implementation-plan.md`.

Folders may nest to group one story's tickets; each folder holding a plan is a change of its own, and
folds in on its own, in any order.

## The plan
Frontmatter `status: draft` until the user's OK, then `approved`. The user shapes any part of it, any
time; nothing in it is fixed until it's built.

- **Requirements** — why, in a sentence or two, then what must hold once it's built: plain lines
  grouped by topic as the user would name them — rules, edge cases, failure paths. Never a log of spec
  edits, stage tags or spec section names; the specs follow the code as it lands. Anything undecided
  is an Open question here, with an Action. It ends with one line naming the specs it touches. What
  the user agrees to.
- **Findings** — when there are any: how things really behave, learned while doing the work — on a
  device, in a log, from another team — each dated, with where. A record, not a requirement; folding
  in moves what still holds into the specs.
- **Design** — how, readable by someone joining cold: why and what before how. A small change:
  Overview and Alternatives considered. A bigger one, the template's parts, as a design doc: Context —
  which Requirements topic it builds, since Requirements are the goals and Not in this change the
  non-goals, never repeated here — Overview with one Mermaid component diagram marking new, changed and deleted
  pieces, Scenarios as numbered steps, Detailed design per piece — responsibility, interface,
  behaviour, failures — Cross-cutting, What changes — each added piece naming the existing one that
  could hold it and why it can't — and Alternatives considered.
  - **Every new or changed call between packages or layers** — a use case, a public method on another
    package's class, a dependency a constructor takes — as a signature with the class that owns it, at
    a high level. What happens inside one package is left to building.
  - **Each option not taken:** `- **Not {option}:** {why}` — an approach someone would propose again,
    never a wording, a name or a signature the code shows (spec-style-rules' *What was rejected*).
  - **A new module, a moved boundary, a new library:** say so to the user; `01-architecture.md` or
    `02-tech.md` is updated as it's built. Build files are sensitive paths.
  - **A story folder holding a contract:** its Design covers the flow across modules and what each
    module change does for it; its tasks are the module changes.
- **Tasks** — checkboxes, each an instruction in plain words, in the order they run, its number inside
  the bold title (`- [ ] **3. …**`): a number before the box is hidden by most viewers, and one right
  after it starts a list of its own.
  - **Checks:** optional `- Check:` sub-bullets — a test name and its file, or what to try by hand. A
    check only a person can make turns its task into a checkpoint. A check that needs something outside
    the session — a real push, pipeline or device — is a task of its own, holding only the check.
- **Not in this change** — what a reader would expect and won't find.

## Approval
The user's OK on the plan, in chat: set `status: approved`. Asking to build a draft is that OK — set it
and say so. Only the user sets it back to `draft`, to rethink; building stops until they ask again.

## While building
- **Order:** the tasks in order, re-reading the plan before each one.
- **Specs follow the code:** as a task lands, update in place each spec it moved — Behaviour, Intent,
  `owns`, and a Decision for a `Not` line someone reading only the code would propose again — with
  `updated:` and, once per change, a Change history row. A new spec is written when its first piece
  lands. A spec documents what's built, never what's planned.
- **Ticking:** a task when its checks hold. A checkpoint waits for the person; what they saw goes on
  its Check line.
- **Blocked:** an Open question blocking a task is never settled by picking an interpretation. Build
  what isn't blocked, and report the rest.

## Shaping the plan
Any time: edit, add, reorder or delete pending tasks; rewrite Requirements and Design to what's true
now — a dropped approach becomes a `Not` line saying what was learned. Shaping what's built — the user
tries it and adjusts — changes the code and the specs directly, and adds no task. The work reaching
another module: say so in one line, and ask whether it joins this plan or gets its own.

## Folding in
"Fold in", "save what's done" or "it's done", through `spec-merge`. The specs already document what's
built. Unbuilt work goes where the user said — "we'll continue later" keeps the plan; when they
haven't said, one question: "The rest — into Future plans, or keep the plan for later?" Into Future
plans: the folder goes. Kept: the plan, its status unchanged, is cut to what isn't built and what it waits on, and each spec
it touches gets a Future plan pointing at it, so anyone on the team can pick it up.

**Abandoning:** on the user's yes, delete the folder. Code and spec edits already made stay unless the
user asks to undo them.

## Talking to the user
Plain words — *waiting for your OK*, *building*, *ready to fold in* — never "phase", "delta" or
"sub-change".
