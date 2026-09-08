---
name: spec-merge
description: Use when asked to "merge the spec", "fold the change into the specs", "close/finish the change", "I think it's done", or when the user approves a new spec written from existing code — merges a finished change under .specs/changes/ into .specs/: confirms its criteria, marks each spec file merged and moves it back to its place, keeps what the plan decided, adds Change history, deletes the folder, then syncs. Not for building a change (spec-plan), or a git merge request; abandoning a change is moving its specs back with their edits undone and deleting the rest on the user's yes.
---

# Spec Merge

A change merges when the user says it's done — or, for a spec written from code that already exists,
when they approve the reading. Until then, each spec the change edits lives in its folder, moved
there with `git mv`, and `.specs/` holds the rest.

## Non-negotiables

- **Only when the user says the change is done, or approves a spec written from code.** Unticked
  tasks are listed, never a reason to ask again. "Merge" alone may also mean the branch's MR or combining two rules or skills — ask which.
- **Every criterion is confirmed before it merges.** List the unchecked ones — for a contract criterion, with the feature criteria a yes also confirms — and ask once, each its own
  answer: confirmed by the user, as `Source: Manual`; dropped — into an Open question when it's still
  wanted; or the change stays open. For a
  spec written from code, that answer comes with the approval.
- **Show what the plan leaves behind before writing any of it**, so the user sees what is dropped.
- **Ask before deleting the change folder — approving a new spec written from code is that yes.** Where
  `.specs/` isn't committed, nothing brings it back. A change nested in it is never deleted with it.

## 1. Before merging

1. Read, if not already read this session, `.agents/profiles/specs/rules/on-demand/spec-change-rules.md`, `spec-format-rules.md` and
   `spec-style-rules.md`.
2. List any unticked tasks. Ask the one question about unchecked criteria, unless the approval already
   answered it; stop there if the user keeps the change open.

## 2. Move the spec files back

- **Each `specs.<path>.md`** moves to `.specs/<path>` with `git mv` — plain `mv` where `.specs/` isn't
  in git — so its history follows it: `specs.feature.logger.md` lands at `.specs/feature/logger.md`.
  Something already at that path is a conflict: show it and ask. Delete template comments and every
  heading left empty.
- **Status and date** — `status: merged` and `updated:` to today.
- **The Change section** — one Change history row on an existing spec whose documented behaviour or
  requirements changed; otherwise deleted.
- **A removal** — a spec file whose Change section removes the spec deletes it instead.
- **Criteria** — confirmed ones get `Source: Manual`; dropped ones leave the spec, into an Open question
  when still wanted. A contract criterion its checked feature criteria already cover isn't asked about
  (spec-format-rules' *How a criterion was confirmed*).

## 3. What the plan leaves behind

Show it as a list before writing any of it:

- **A `Not` line** someone reading only the code would propose again, with no Decision yet, becomes one.
- **A flow across modules** goes into the contract spec as who does what.
- **A module's non-obvious internal invariants** go into its `ARCHITECTURE.md`, where the module has one.
- **Interfaces and state machines** already live in the code and its doc comments; they and the rest are
  dropped.
- **Unticked tasks** are listed.

## 4. Finish

- For a change made ahead of code, offer `spec-check-style --fix` on the specs it touched; run it only on a
  yes.
- Report what merged, which criteria were confirmed or dropped, which tasks were left, what the plan
  left behind and what was dropped. Then delete the change folder — only its own files while a change is nested in it, and a parent folder left empty — on the user's yes, or on the
  approval of a new spec written from code. Whether or not the folder goes, run `spec-rebuild-overviews` and report its drift and warnings.
