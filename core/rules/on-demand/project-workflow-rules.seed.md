---
holds: the process around a change — committing, branching, requesting review, reading a failure
elsewhere:
  project-code-style-rules: naming convention, idiom, logging facade, error handling pattern, visibility, module boundary
  project-sensitive-paths-rules: ask before, do not touch, breaks the build for everyone
---
# Workflow rules

The loop around writing code: naming a branch, writing a commit, reading a failure, knowing what
is actually verified.

<!--
  FILLING THIS IN (SETUP.md Step 6, or by hand later):

  This file's topics are the same everywhere — that is why the template is here rather than in a
  stack profile — but every value in it is specific to one repository, and a wrong one is worse
  than a missing one. An agent that believes the wrong test command runs the wrong thing and
  reports success.

  Evidence, per section:
    Git       — `git log --oneline -30` and `git branch -a`. Read the real subjects; do not
                impose Conventional Commits on a repo that has never used them.
    CI        — the pipeline file itself (.github/workflows/*.yml, .gitlab-ci.yml, Jenkinsfile).
                List the jobs that gate a pull/merge request, and the exact command each runs.
    Gaps      — which modules or packages have tests that CI never runs. This is the part nobody
                writes down and everyone assumes wrongly.
    Local     — git hooks, pre-commit config, a formatter wired into the build.

  Delete any section this project genuinely has nothing for. An empty heading teaches nothing.
-->

## Git

| | |
|---|---|
| Commit subject | {{the real format, with a real example copied from `git log`}} |
| No ticket | {{what people actually write when there is no ticket — or delete this row}} |
| Branch | {{the real convention, with an example}} |
| Attribution | Never add `Co-Authored-By`, a generated-by line, or any other trailer naming the tool that wrote it — in a commit message or a request description. A commit says what changed. Delete this row only if the project wants such a trailer. |
| Review unit | {{pull requests / merge requests, and how they're referenced in commits}} |
| Never stage | {{paths deliberately excluded, and where that exclusion lives}} |

Commit or push only when asked. A commit message is the subject and as many short bullets as the
change needs — one line each, never paragraphs. The diff carries the detail. The subject says what
the change does overall; each bullet starts with Added, Changed or Removed and says in a few words
what, readable without the diff.

## Pull or merge request description

Short and scannable — the diff already says what changed:

- **Title:** the commit subject.
- **Why:** one or two lines, the reason the change exists.
- **What:** two to four bold labels, each with at most three one-line bullets.
- **Proof:** one line — what was run, and what still needs a person.

## What CI actually verifies

<!-- The point of this section is the gap between what the Commands table in .specs/02-tech.md implies and
     what the pipeline runs. State the narrower truth. -->

{{N}} job(s) gate a {{pull/merge}} request ({{pipeline file}}):

- **`{{job}}`** runs `{{exact command}}`. {{What that does and does not cover.}}

{{Which packages or modules have tests that never run in CI. Say plainly that a local run is the
only thing that will execute them, and give the command.}}

## Running the build, lint or tests

Run them through the `runner` agent, which reports only what failed, and work from its report
rather than the raw output.

## When a run fails

1. Read the failure, fix the code. If the fix isn't obvious, say what failed and stop — a green
   run bought by weakening the check is worse than a red one.
2. Never loosen a test to make a run pass without an explicit ask, with the reason.

## Local conveniences worth knowing

{{Hooks, auto-formatters, or generators that change files without being asked — anything that
  would otherwise show up as a diff nobody wrote. Delete the section if there are none.}}
