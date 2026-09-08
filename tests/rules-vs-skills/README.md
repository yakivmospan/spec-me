# Are on-demand rules worth keeping?

One argument, settled by measurement rather than opinion: a rule's `load-when:` looks a lot like a skill
description, and the `LOADER.md` row looks a lot like a second mechanism doing the first one's job.
If that is right, converting every on-demand rule into a skill should cost nothing and simplify the
setup. If it is wrong, the conversion should lose something you can point at.

This folder builds both shapes and runs the same cases against each.

| | |
|---|---|
| **original** | the setup as it stands: on-demand rules, reached through `LOADER.md` rows |
| **intest** | every on-demand rule converted to a skill, `LOADER.md`'s on-demand table empty |

The cases live with the rest of the behaviour suite, in
`.agents/builder/core/tests/behaviour/cases.toml` under the dimension **on-demand loading**. They are
written so either shape can win: each asks whether the agent reached a piece of guidance at all, by
whichever route its own tree offers, so a check passes on `read_file` of the rule *or* `used_skill`
of the skill that rule became. A case that named a mechanism would measure the conversion instead of
the setup.

## Result

Answered, by transcripts rather than by this folder: the sessions scored on 2026-09-23 and 24 and
recorded in `.agents/builder/BUILDER-DESIGN.md` (Decisions → *Installing*, "One model for guidance")
opened every rule a loader row listed and none of the skills beside it, and reached a skill mid-work
only through a line saying to run it — never through its description alone. On-demand rules stay.

The scripts here read a `load-when:` that rules no longer carry, since the loader alone places them.
They are kept as a record of how the question was asked, not to be rerun.

## Running it

```bash
python3 prepare.py --descriptions descriptions.toml
```

builds both snapshots under `/tmp/rules-vs-skills/` and prints what each costs in always-on words.
That number needs no agent and is worth having on its own.

Then run the behaviour suite in each snapshot. Inside a snapshot the whole setup is present, so the
harness scores against that variant's tree rather than this repository's:

```bash
cd /tmp/rules-vs-skills/original/.agents/builder/core/tests/behaviour
python3 run.py --agent claude --only ondemand --repeats 3
```

and the same in `intest/`. Then put the two result files side by side:

```bash
python3 run.py --compare <original-run>.json <intest-run>.json
```

With no agent CLI installed, the suite's `--ingest` path takes the same cases driven by hand or by
subagents — one `<case-id>.json` per case holding `answer`, `files_read` and `skills_used`:

```bash
python3 run.py --ingest /tmp/rules-vs-skills/ingest/original --agent subagent
```

Those runs are scored on the same footing as any other and labelled *(agent's own word)*, because the
tool checks then rest on the agent's own account rather than a recorded call.

## Both descriptions, not one

`skillify.py` generates each skill's description from the rule's `load-when:`. That is the literal reading
of the proposal and it is the variant's **floor**.

`descriptions.toml` holds hand-written ones, with triggers first and a `Not for` separating each from
its neighbours. That is the variant's **ceiling**, and it is the fairer comparison: a proposal should
be judged at its best, not at the quality of a generator.

```bash
python3 prepare.py                                    # floor
python3 prepare.py --descriptions descriptions.toml   # ceiling
```

A result that only holds at the floor is a result about the generator. Run both before believing
either.

## What this cannot tell you

Say it plainly, because the number will outlive the memory of how it was made.

- **A snapshot is not a session.** The fidelity that matters most — a real session's own skill
  injection, its compaction, four hours of unrelated context — is exactly what a one-shot case does
  not reproduce. The failure this whole question came from was a five-hour session; nothing here runs
  for five hours.
- **`--ingest` results are self-reported.** An agent saying it read a file is weaker evidence than a
  recorded call. Install an agent CLI and the same cases produce observed evidence instead.
- **Six cases is six requests.** They cover each on-demand rule once. They do not cover a rule being
  needed twice, or needed late, which is where the original complaint lived.
- **A snapshot carries no source tree.** `prepare.py` copies what the behaviour suite copies —
  `.agents/`, `.specs/`, `AGENTS.md`, `CLAUDE.md` — so a case that asks for a change to a Kotlin file
  cannot open one. Every run in the first experiment said so and answered from the rules instead.
  It hits both shapes equally, so the comparison stands, but the absolute scores are lower than a
  real session's would be. Widening `COPIED` is the fix if that ever matters.
- **The always-on word count is the one hard number here.** It needs no agent, does not vary between
  runs, and is worth more than a small behavioural difference measured once.

Treat a large, repeated gap as a real signal. Treat a small one as noise until three runs say
otherwise — and read `results/README.md` before deleting anything, because a curve needs its old
points.
