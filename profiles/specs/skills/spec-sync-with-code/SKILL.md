---
name: spec-sync-with-code
description: Use when asked to "verify the spec", "check the spec against the code", "is this spec still true", "run the spec's tests", or when the user accepts an offer to check a possibly stale spec — runs its criteria's tests, reads the code they don't cover, then settles each difference with you: hand a stale spec to spec-create, or record the code as the defect. Writes the result to INDEX.md, and runs in the background — on Codex, when asked. Not for a spec inside an open change (spec-create), its prose (spec-check-style), or the overviews (spec-rebuild-overviews).
---

# Spec Verify

A stale spec is one whose owned code changed after its `updated:` date: it may still be true, or not.
This finds out, without stopping the task that needed the spec.

## Non-negotiables

- **Run in the background** — on Codex, only when asked. The task that needed the spec keeps going; report when the check is done.
- **Reading never checks a criterion.**
- **A difference is a spec-vs-code conflict** — unless the spec sits in an open change whose edits
  already describe the code; name that change instead. Otherwise ask which side is right, one
  difference at a time, and act only on the answer. Never pick a side yourself: a stale spec and a
  buggy implementation look identical from here.
- **Check criteria and bump `updated:` only when the whole check is clean** — every listed test ran and passed,
  nothing read as *differs* or *can't tell*. Otherwise the spec isn't touched.
- **No test command you can't find in `.specs/02-tech.md`.** When you can't derive one, skip the tests,
  say so, and still read.
- **Record every run** with `scripts/record_check.py`, so `INDEX.md` shows it beside the spec while it's listed as possibly stale.

## 1. Tests

1. Collect every automated `Source:` under the spec's criteria — the test files and their tests.
2. Work out the command from `.specs/02-tech.md`'s Testing section: for a module-scoped command, the
   module each test file sits in.
3. Hand the run to the `runner` subagent. Note per criterion: all its tests passed, some failed (which),
   or not run.

## 2. Reading

For every criterion with no automated source, and for Intent, Constraints and Public surface: read the
code under the spec's `owns` — the `spec-architect` subagent for a wide glob — and mark each:

- **holds** — the code does what it says;
- **differs** — quote what the code does instead, with file and line;
- **can't tell** — say what's missing to decide.

A criterion confirmed by a person (`Source: Manual`) **holds** unless the code plainly **differs**; "can't tell" doesn't apply to it.

## 3. Finish

1. **Clean** — every listed test ran and passed, nothing differs or can't tell: check each unchecked criterion whose tests all passed,
   and set `updated:` to today.
2. **Not clean** — settle each difference with the user before touching anything:

   > 1. **{what the spec promises}** — the code does {what it does} (`path:line`).
   >    - **A:** **The spec is stale** — `spec-create` corrects it *(the code is the truth here)* ⭐
   >    - **B:** **The code is wrong** — the spec stands. This is a defect for the report, not an edit
   >    - **C:** **Can't tell yet** — leave both, recorded as *can't tell*

   One question per difference, and nothing changes before its answer. A spec whose differences all
   came back **B** or **C** is left exactly as it was — which is the old behaviour, now a result
   rather than the only option.

   `spec-create` makes the correction: in place for a `merged` spec, inside the change for one in an
   open change.
3. **Record, either way:**
   ```bash
   python3 .agents/skills/spec-sync-with-code/scripts/record_check.py feature.x --passed 47 --failed 1 \
     --differs AC-5 Intent --cant-tell AC-2
   ```
   Then run `spec-rebuild-overviews`, so `INDEX.md` shows the result.

## Report

Clean, in one line: "`feature.x` verified — tests green 47/47, reading holds; 3 criteria checked,
`updated:` bumped." Otherwise that line, then each failing test, difference and can't-tell with its quote, by priority,
Critical first:
- **Critical** — a checked criterion's test fails, or the code breaks a Constraint or its public surface;
- **High** — the code does something other than what a criterion or the Intent says, where a user or caller sees it;
- **Medium** — a difference only the code's own module sees, or a test that didn't run;
- **Low** — can't tell, or a difference in how the spec describes it rather than what it guarantees.

Then one question: for each difference, is the spec right or the code? Code right: `spec-create` corrects
the spec in place; spec right: fix the code. Tests not run: say so, never "tests green".
