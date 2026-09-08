---
name: test-plan-manual
description: Use when asked to "write a test plan", "make a manual test plan", "turn this runbook into a test plan", or when a task's only proof needs a real MR, tag push, device or registry that can't run in this session — turns a checklist someone has to run by hand into a numbered, checkboxed list of test cases: Preconditions, Steps, Expected, an optional Result, and, where an implementation-plan.md exists, the task it closes. Also when the person reports how a case went ("TC-4 failed: …") — records it under that case. Not for automated tests or writing an implementation plan.
---

# Manual Test Plan

A manual test plan turns steps a person has to run by hand — a narrative runbook, or a task whose
Check needs a real MR, tag push, device or registry — into cases that read the same way every time
and get reported on one at a time.

## Non-negotiables
- **One case, one thing to observe** — a step trying two independent behaviors (two modules, two
  devices) splits into two cases, never one case with "or" in its Steps. A single trigger that proves
  two separately-checkable outcomes (one tag push that both publishes and leaves other jobs untouched)
  still splits: each outcome gets its own case and its own pass/fail record, even sharing one Steps
  line via "see TC-n's Steps."
- **Order cases the way a person will actually run them**, not a plan's task order; a case that needs
  another's output says so in its own Preconditions.
- **Where an implementation-plan.md exists, `Closes:` names the task(s) each case confirms** — nothing
  else in this plan restates that task's content.
- **No `.specs/` required** — a repository with no implementation plan gets the same cases with no
  `Closes:` line.
- **The checkbox follows the latest run; Result is optional** — `[x]` once the latest run passed,
  `[ ]` while it fails or hasn't run. **Result** is added only when a run has something worth keeping:
  a failure, a partial pass, a note or the builds it ran on. It holds one sub-bullet per such run,
  newest last, so a retest shows what changed. Expected never changes to fit a result.

## Structure
Copy `templates/manual-test-plan.md` beside this file, never write from memory:

```
1. [ ] **TC-n: {what it proves, one clause}**
   - **Preconditions:** {state the case needs before it starts}
   - **Steps:** {what the person does}
   - **Expected:** {what tells them it passed}
   - **Closes:** {the task(s) it confirms — omit where there's no plan}
   - **Result:** {optional — only once a run has something worth keeping; one sub-bullet per run}
     - {date}, {builds or versions under test}: {pass | fail | partly}. {what happened}
```

## Writing cases
1. Read the runbook, or the plan's unticked "verify for real" tasks — one case per Check.
2. Name what actually changed hands — a tag, a version, a job, a file path — never "the module" or
   "it".
3. A Steps or Expected field that already reads as more than one clause splits onto its own
   sub-bullets, the same rule as any dense list item.

## Reporting back
Close the plan with a line asking the person to report each case's outcome — in any words, naming the
case. On a report:
1. Set the checkbox from this run, and when it passed, tick any plan task its `Closes:` names. A bare
   "passed" needs nothing more.
2. When the report carries more — a failure, a partial pass, a note, the builds — add a sub-bullet
   under that case's **Result** (create it if missing): the date, the builds named, pass, fail or
   partly, and what happened in a sentence, citing any finding it confirms.
3. A date or build the report doesn't give is written as not recorded, never guessed.
4. A new problem the report describes goes wherever the plan lists findings, if it has such a list.

## Examples

Good — one behavior, named:
> 1. [ ] **TC-4: `deploy:payments-client` publishes on its release tag**
>    - **Preconditions:** the build's version is the one to release.
>    - **Steps:** push tag `payments-client-v<version>`.
>    - **Expected:** the job runs and publishes; the registry shows the new version.
>    - **Closes:** Task 8.

Bad — two behaviors folded into one case:
> 1. [ ] **TC-2: the API check fails on a breaking change in either module**
>    - **Steps:** change a public method's signature in `payments-client` or `payments-model`; push.
