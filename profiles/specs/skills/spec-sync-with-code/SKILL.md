---
name: spec-sync-with-code
description: Use when asked to "verify the spec", "check the spec against the code", "is this spec still true", "run the spec's tests", or on the user's yes to checking a possibly stale spec — runs the tests its `owns` globs cover, reads the code for Behaviour lines they don't settle, then settles each difference with you: spec-create fixes a stale spec, or `Currently violated:` records the code as the defect. Records the result in INDEX.md; runs in the background — on Codex, when asked. Not for a spec inside an open change (spec-create), its prose (spec-check-style), or the overviews (spec-rebuild-overviews).
---

# Spec Verify

A stale spec is one whose owned code changed after its `updated:` date: it may still be true, or not.
This finds out, without stopping the task that needed the spec.

## Non-negotiables

- **Run in the background** — on Codex, only when asked. The task that needed the spec keeps going; report when the check is done.
- **A difference is a spec-vs-code conflict** — unless the spec sits in an open change whose edits
  already describe the code; name that change instead. Otherwise ask which side is right, one
  difference at a time, and act only on the answer. Never pick a side yourself: a stale spec and a
  buggy implementation look identical from here.
- **Bump `updated:` only when the whole check is clean** — every test under `owns` ran and passed,
  nothing read as *differs* or *can't tell*. Otherwise the spec changes only by the user's answers.
- **A Behaviour line no test covers is still a rule.** Read the code for it; never ask for a test.
- **No test command you can't find in `.specs/02-tech.md`.** When you can't derive one, skip the tests,
  say so, and still read.
- **Record every run** with `scripts/record_check.py`, so `INDEX.md` shows it beside the spec while it's listed as possibly stale.

## 1. Tests

1. Find the test files the spec's `owns` globs cover.
2. Work out the command from `.specs/02-tech.md`'s Testing section: for a module-scoped command, the
   module each test file sits in.
3. Hand the run to the `runner` subagent. Note how many passed and failed, and which failed.

## 2. Reading

A passing test settles a Behaviour line when it plainly checks what the line says. For every other
line, each line a failing test is about, and the Intent: read the code under `owns` — the
`spec-architect` subagent for a wide glob — and mark each:

- **holds** — the code does what it says;
- **differs** — quote what the code does instead, with file and line;
- **can't tell** — say what's missing to decide.

A line with `Currently violated:` holds while the code still breaks it as that sub-bullet says; code
that now follows the line differs from the sub-bullet.

## 3. Finish

1. **Clean** — every test ran and passed, nothing differs or can't tell: set `updated:` to today.
2. **Not clean** — settle each difference with the user before touching anything:

   > 1. **{the Behaviour line, or the Intent}** — the code does {what it does} (`path:line`).
   >    - **A:** **The spec is stale** — `spec-create` corrects it *(the code is the truth here)* ⭐
   >    - **B:** **The code is wrong** — the spec stands; add `- **Currently violated:** {what breaks it, and where that's tracked}` under the line
   >    - **C:** **Can't tell yet** — leave both, recorded as *can't tell*

   One question per difference, and nothing changes before its answer.

   `spec-create` makes the correction: in place for a `merged` spec, inside the change for one in an
   open change.
3. **Record, either way** — name each part by a few words of its Behaviour line, or `Intent`:
   ```bash
   python3 .agents/skills/spec-sync-with-code/scripts/record_check.py feature.x --passed 47 --failed 1 \
     --differs "retried once" Intent --cant-tell "signed-in account only"
   ```
   Then run `spec-rebuild-overviews`, so `INDEX.md` shows the result.

## Report

Clean, in one line: "`feature.x` matches its code — tests green 47/47, reading holds, `updated:` bumped."
Otherwise that line, then each failing test, difference and can't-tell with its quote, by priority,
Critical first:
- **Critical** — a test under `owns` fails;
- **High** — the code does something other than a Behaviour line or the Intent says, where a user or caller sees it;
- **Medium** — a difference only the code's own module sees, or a test that didn't run;
- **Low** — can't tell, or a difference in how the spec describes it rather than what it guarantees.

Then the Finish questions, one difference at a time. Tests not run: say so, never "tests green".
