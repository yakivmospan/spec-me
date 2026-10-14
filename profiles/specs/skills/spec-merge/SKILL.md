---
name: spec-merge
description: Use when asked to "fold in", "save what we did", "close/finish the change", "I think it's done", or "abandon the change" — folds a planned change under .specs/changes/ in: checks the specs document what's built, writes what the plan decided, then deletes the plan or cuts it to the unbuilt rest for later. Not for building a change (spec-plan), or a git merge request.
---

# Spec Merge

A change is a plan; the specs were updated in place as it was built. Folding in makes sure they say
everything the build settled, and decides what happens to the plan.

## Non-negotiables

- **Fold in what's built; never stop the user's work for it.** Unticked tasks never block the fold.
  "Merge" alone may also mean the branch's MR or combining two rules or skills — ask which, in one line.
- **A spec documents only what's built** — a requirement not built yet stays out of Behaviour.
- **One question at most:** where the unbuilt rest goes, when the user hasn't said
  (spec-change-rules' *Folding in*).
- **Where `.specs/` isn't committed, ask before deleting the plan** — nothing brings it back.

## 1. Read

Read, if not already read this session, `.agents/profiles/specs/rules/on-demand/spec-change-rules.md`, `spec-format-rules.md` and
`spec-style-rules.md`, the plan, and each spec it touches.

## 2. Bring the specs up to date

For each spec the built tasks touched — missed while building, or settled since:

- **Behaviour, Intent, `owns`** — to what's built; `updated:` to today.
- **A Change history row** for this change, if it has none yet, on a spec whose documented behaviour
  or requirements changed.
- **A `Not` line** someone reading only the code would propose again, with no Decision yet, becomes one.
- **A Finding that still holds** goes into the spec it concerns: a Behaviour line when the code does it
  on purpose, a Pitfall when a reader would get it wrong.
- **A flow across modules** goes into the contract spec as who does what; **a module's non-obvious
  invariants** into its `ARCHITECTURE.md`, where it has one.

## 3. The plan

- **Nothing left, or the rest into Future plans:** each unbuilt requirement becomes a Future plan in
  the spec it belongs to, then delete the folder — only its own plan while a change is nested in it, and a parent
  folder left empty.
- **Kept for later:** cut the plan to the unbuilt requirements and tasks, with a line under its
  title saying what they wait on; add a Future plan pointing at it to each spec it touches.
- **Abandoned:** delete the folder; built code and spec edits stay unless the user asks to undo them.

## 4. Finish

Run `spec-rebuild-overviews`. Report in a few lines: what the specs gained, where the rest went, and
drift the rebuild found. Then go back to what the user was doing.
