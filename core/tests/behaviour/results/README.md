# Runs kept

**This folder is the record, not scratch. Don't clear it.**

Each run writes one JSON here — the agent, its version, the builder version, the context load, and
every check's verdict — and the raw output of every take under `transcripts/`. Both together are
what make a number from months ago comparable with one from today:

```bash
python3 ../run.py --rescore <a-run>.json
```

re-runs **today's** checks against sessions recorded whenever, with no agent and no cost. Change a
check and every past run can be re-judged on the new standard. Delete these files and that is gone
for good — the sessions cannot be re-created, only re-run at full price.

`--compare <older>.json <newer>.json` prints each dimension side by side with better, same or WORSE.

## Commit these, unless your team decides otherwise

Nothing here is gitignored, and that is deliberate rather than an oversight. A score only the person
who ran it can see settles no argument: the value is the curve, and a curve needs runs from before
you were asked the question. Fifteen sessions is about 90 KB.

It is still your team's call. Reasons you might not: runs hold whatever the agent wrote, so a case
touching something private ends up here; and a repository where everyone runs the suite collects
runs faster than anyone reads them. Either way, decide it once and write it down — the bad outcome
is a folder nobody commits and nobody deletes.

A `-dry.json` file is from `--dry-run`: no agent ran, so it records each case's floor rather than
any agent's behaviour. Those are safe to delete.
