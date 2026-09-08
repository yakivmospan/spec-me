# Project Rule Skill — reference

Bad and good versions of the parts a rule or skill most often gets wrong, and how to change several at once. The rules are in `SKILL.md`.

## Description

Bad — no triggers, no boundary:
> Helps with releases and keeping the history in good shape.

Good:
> Use when asked to "write the release notes" or "what changed since the last tag" — drafts release
> notes from the changes merged since the last tag, user-facing ones first. Not for writing a commit
> message or tagging the release.

## Stop

Bad — the agent has to invent the behaviour:
> If the branch isn't ready, handle it appropriately.

Good:
> the branch has uncommitted changes — stop, and list them. Never stash or discard them on the user's
> behalf.

## Non-negotiable

Bad — needs a citation to mean anything:
> Follow the workflow rules' *Commit format*.

Good:
> **A commit subject says what the change does** — never a list of the files it touched; a reader
> should not need the diff to know what changed.

## Restated rule

Bad — a copy that drifts from its source:
> A branch is named `<type>/<ticket>-<slug>`, lowercase, with the ticket from the tracker, and…

Good:
> Name the branch per `project-workflow-rules.md`.

## Changing several at once

Two or more rules or skills that hand work to each other, changed in one go. Each can end up better and
the flow between them broken. So:

1. **Keep a copy** of every file it may touch, unless git tracks it, and say where.
2. **Baseline:** offer `project-test-setup` before the edits; on a yes, keep its scores and findings.
3. **Brief each helper by pointer:** the rule's name and the whole section it sits in, heading included —
   never a paraphrase, which drops the scope. Files that share a flow go to one helper, or are compared after.
4. **Walk each shared flow** across the edited files: every branch of an exception the pass touched, and
   the ordinary cases — the plain path, a change of mind half-way, "it's done" with a step left. Two
   files saying different things is fixed before anything is reported.
5. **Compare**, when the baseline ran: rerun `project-test-setup` the same way, and run `project-resolve-conflicts`.
   A new High or Critical finding, or one in a file the pass edited, is fixed before "done". Report before
   and after; restore from the copy only on the user's yes.
