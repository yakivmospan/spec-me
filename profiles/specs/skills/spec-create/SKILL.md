---
name: spec-create
description: Use when asked to "create a spec", "spec out X", "start PROJ-1234", "add a feature", "change how X behaves", "update the spec", "bring the spec up to date with the code", "create a spec from code", when handed new requirements, or when spec-builder-rules.md's Every task sends work here — starts or continues a change under .specs/changes/, working out whether it's a new feature, a change to a spec, or code already written — or corrects a stale spec in place. Not for a one-line fix, planning or building (spec-plan) or merging (spec-merge).
---

# Spec Create

Every change to what a spec guarantees starts here: a new feature, a feature a spec already describes,
or code that exists with no spec or a stale one. The result is a change folder whose spec files say
what will be true, agreed with the user before any code. A spec it edits moves into the folder and
back at `spec-merge`; nothing else under `.specs/` changes — except a stale spec corrected in place.

## Non-negotiables

- **Ask what nobody has written down, before writing any spec file** — in one message, only what
  matters for this change: typically who consumes it and what breaks if it's wrong, the failure path,
  what isn't this change's job, which constraints are fixed, what proves it done. Put your inference
  beside each, and skip what a spec, ticket or the code already answers — saying which.
- **Never fill a gap with a plausible default.** Every unanswered question, and every assumption made to
  keep going, is an Open question with an Action.
- **Every criterion is Given/When/Then, confirmable without asking you, failure path covered by it or a sibling, and states
  a guarantee, not implementation** — no tunables, internal names or call sites.
- **From code, the code is ground truth.** Write what it does; unclear or wrong-looking behaviour is an
  Open question. Never loosen a constraint it no longer honours, or delete what it stopped doing, on
  your own — ask whether that was on purpose.
- **A Decision names what it rejected; a request that would re-decide one is raised as exactly that.**
- **Only the user approves, in chat.** Set `status: approved` only on an explicit yes. For a new spec
  written from code, that yes folds the change in and confirms its unchecked criteria, unless they say otherwise — say so when asking.

## 1. Find the starting point

Find the area by the `owns` globs (`.specs/INDEX.md` lists them), under other names too, and look at the code under it.

| What you find | Starting point | Spec file in the change |
|---|---|---|
| No spec covers it, and no code does it yet | **New** | a new spec, from `spec-feature.md` — or `spec-contract.md` |
| A spec covers it, and the requirements are changing | **Change** | that spec, moved in and edited |
| The code already does it, and no spec covers it | **From code** | a new spec describing the code |

Each spec file is shaped per spec-change-rules' *The folder*.

- **A `merged` spec the code has moved past, and the code is right** — no folder, so skip step 2's folder steps: draft the
  edit as *From code* describes, and write it on *The OK*'s yes.
- **"Update the spec", direction unclear** — spec-change-rules' *Which direction*.
- **One change can mix them** — a new spec and a moved one, or a new spec, written *From code*, for the part no
  spec covers.
- **The spec is already in an open change** — continue that change and edit it there as spec-change-rules'
  *Changing course* says. If it's unclear whether the work belongs there, ask
  whether to add it to that change or wait for that change to merge.
- **Unscoped** ("the specs are stale") — ask which area. A tree-wide sweep needs its own go-ahead.
- **Not a feature at all** — code callers merely borrow — gets no spec (spec-format-rules' *What counts
  as a feature*); say so and stop.

## 2. Shape the change

1. **Read**, if not already read this session, `.agents/profiles/specs/rules/on-demand/spec-change-rules.md`, `spec-format-rules.md` and
   `spec-style-rules.md`; `.specs/00-product.md`'s Non-goals — a change that contradicts one is a flag
   to raise, not something to write as asked; and every spec the change touches, whole.
2. **Resume rather than restart.** A folder for this branch or ticket already under `.specs/changes/`:
   continue it when it's the same work; different work gets its own folder, `<branch>-<topic>`.
3. **Check a spec you'll move against its code** — *Change* only. When `git log` shows commits to its
   `owns` code on a day after its `updated:`, or it has no `updated:`, run `spec-sync-with-code` unless
   it ran or was declined this session; keep eliciting while it runs. Move the spec in once its
   differences are settled, or the check declined, so the diff holds only new requirements.
4. **Module split**, for work ahead of code — *From code*, the code already shows which module owns what.
   Work that plausibly spans modules, or where which module owns what is itself a
   question, goes through `spec-plan`'s grounding before any requirement is written. The user naming
   the module settles it, unless the code shows the work reaches further — then say so. Work that does
   span modules gets a contract spec.
5. **Create the folder**, named per spec-change-rules' *The folder*.
6. **Elicit**, per the non-negotiables.
7. **Write the spec files**, adding what the starting point needs:

### New

- **`parent`** — `architecture` for a standalone feature or a contract; otherwise the feature it's part
  of, or the contract it implements.
- **`owns`** — the code and test globs the feature will live in; they may match nothing yet.
- **Intent** — what it guarantees to the rest of the system, not how.
- **Acceptance criteria** — from `AC-1`, unchecked.
- **Constraints** and **Public surface** — what elicitation settled. **Decisions** and **Open
  questions** — as they come up. **Pitfalls** and **References** — when the work finds them. No
  **Change history**.

### Change

- **Move the spec** into the folder per spec-change-rules' *The folder*, read it whole — Decisions and
  Open questions included — and edit it as it should read afterwards.
- **Handed new requirements** (a ticket, a document) — map them onto the criteria they add, change or
  remove, and show that mapping first.
- **Criteria** — ids per spec-change-rules' *Changing course*; a changed one is rewritten in place,
  keeping its id unless it no longer names the same guarantee. The report names any tests only a removed
  criterion listed.
- **What is approved with the change** and what is added any time: spec-change-rules' *What goes through a
  change*. A question this change
  answers is struck through in place, pointing at its Decision (spec-style-rules' *Question and action*).

### From code

- **Gather** the code and its tests. For a stale spec: the
  spec whole, and what changed since its `updated:` (`spec-rebuild-overviews`'s *Possibly stale*, then `git log` on
  its `owns`). Criteria in other open changes aren't the code's yet — leave them there. If you can't find the change described, show what you found and
  ask first.
- **Ask only what the code can't answer** — usually intent, the consumer and what's out of scope.
- **A stub is not behaviour.** A hardcoded return or a `// later` comment is an Open question, or — if the
  user wants it — a criterion built first (spec-change-rules' *Stages*).
- **Scope `owns` to what you describe** — narrow, real coverage beats a wide glob.
- **A Decision only where the user can name what was rejected** — the code rarely shows it, so ask.
- **A stale spec** — describe the code: new public surface gets criteria for success,
  failure and edge cases; changed behaviour is rewritten as the guarantee; an open question the code
  plainly answered becomes a Decision, or a doc comment when it's file-scoped, and is struck through.
- **Checkboxes** — a criterion a test already proves is checked, with the test under its
  `Verified:`; one the user confirms from the code is checked with `Source: Manual` under it; the rest stay unchecked.
- **Before asking for approval, re-read every criterion** — reading from code is where one
  turns into a transcript of the implementation.

## 3. The OK

Re-check every criterion against the non-negotiables, and that every open question names what it blocks.
Then:
- **A stale spec corrected in place** — show the edited criteria and ask once, per spec-builder-rules' *Keeping it
  honest*, saying what the yes confirms. Nothing merges; a no leaves it untouched.
- **From code** — ask for approval, saying the yes confirms any criterion without proof as
  `Source: Manual`, unless they say otherwise; the yes folds the change in through `spec-merge`.
- **A change mixing them** — follows *Ahead of code*: its new part is built before anything merges.
- **Ahead of code, one obvious way** — ask for approval now. An implementation plan comes only when
  the work is worth splitting (`spec-plan`).
- **Ahead of code, a real choice to make** — agree the spec files with the user, then continue in
  `spec-plan`; the approval comes with the plan.

Run `spec-rebuild-overviews`; when asking, report its drift with proposed fixes, and its warnings.

## Report

In plain words (spec-change-rules' *Talking to the user*): what the change will make true, what is still
open and what each open question blocks, and what you're waiting for — "your OK on what changes", or
"your OK on the requirements, then we plan".
