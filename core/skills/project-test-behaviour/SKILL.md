---
name: project-test-behaviour
description: Use when asked to "test whether this rule or skill is actually followed", "check if the agent uses skill X", "prove this works", "compare with and without this line", or "run a behaviour test" — walks the user through real sessions one at a time, scores each from its transcript, and compares setups against a baseline. Not for checking the setup's files against the constitution without running anything (project-test-setup), or running a project's own tests.
---

# Project Test Behaviour

Whether a rule or skill is followed can only be seen in real sessions: this runs them with the user,
one prompt at a time, and reports what an agent actually did. The result most often goes wrong when a
session is found by being the newest — the session running the test is newer — or when a prompt
names the mechanism it is testing.

## Non-negotiables

- **The user runs the sessions; you score them.** One step at a time, in chat: what to open, which
  model, the exact prompt. Wait for "done" before the next step. Nothing is written as a plan file.
- **Every setup is measured against a baseline** — the same prompt with the thing under test absent —
  and at least 3 sessions per setup and model. A gap smaller than that says nothing; say so.
- **Find a session by its first message** with `scripts/find_session.py`, never "latest", and score
  only a session whose model is the one planned.
- **A prompt never names the rule, skill or convention under test** — it asks for ordinary work.
- **Change only what was agreed.** Setups are moved between variants by you, named to the user each
  time, and put back at the end. Never commit.

## Before starting

1. `git status --short` is empty — if not, stop and ask the user to commit or stash, because every
   session's edits are undone with `git checkout` and must not touch their work.
2. Agree in one message: the claim under test, each setup (the baseline first), the prompt, what
   counts as a pass (a file read, a skill used, a step of it applied), the models, and the run count.
   Wait for a yes.
3. Add the case to `.agents/core/tests/behaviour/cases.toml` (the suite's check kinds are listed at its
   top) and confirm `python3 .agents/core/tests/behaviour/run.py --dry-run --only <case>` scores 0% —
   a case that passes with no agent measures nothing.

## Steps

1. **Set up the first setup** — make the agreed change, show the user what moved. Done when
   `git status --short` is still clean apart from `.agents/`, which git does not track.
2. **Hand out one run** — a new session on the main folder, not a worktree (a worktree has no
   `.agents/`), the model to pick before sending, the prompt in a code block, and "tell me `<id>`
   done". Done when the user says so.
3. **Score it**:
   - `python3 .agents/core/skills/project-test-behaviour/scripts/find_session.py "<prompt's first
     line>" --skip <ids scored so far>` — the top line is the run; a model other than the planned one
     means it is not scored: say so and hand the step out again.
   - `python3 .agents/core/tests/behaviour/run.py --transcript <path> --only <case>`.
   - Read the session's tool calls for what the checks cannot see: whether the loaders and the rule
     were read, and which of the skill's steps ran.
   - `git status --short`, then `git checkout -- <each file the session changed>` and nothing else.
   Done when the score, the model and one sentence on what happened are in chat, and the tree is clean.
4. **Next run, or next setup** — repeat 2–3 until the setup has its runs, then move to the next setup
   (step 1) and say what changed. After the last run, put every setup change back and show the diff.

## When the plan stops fitting

- **A run shows something the claim did not expect** — a file never read, a step skipped: record it,
  finish the setup's runs, and raise it with the verdict; never change the setup mid-way.
- **The first setups already settle the question** (0 of 3 against 3 of 3) — say so and ask whether
  the remaining runs are still worth the user's time.
- **The finder returns nothing** — the prompt was changed or pasted into a running session; ask the
  user to open a new session and paste it exactly.
- **The agent tool is not Claude Code** — its sessions are not written where the finder looks; say
  that this skill scores Claude Code sessions only.

## Report

A table per setup and model: runs, passes, and what the passing runs did. Then the verdict in one
sentence, what it rests on (tool version, models, prompt, run count), and what it does not show. Offer
to record the verdict where the design or the README needs it; write it only on the user's yes.
