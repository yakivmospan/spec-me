# Runs kept

**The record, not scratch. Don't clear it.**

One pair of files per experiment: `<stamp>-original.json` and `<stamp>-intest.json`, scored by the
behaviour suite, plus a `<stamp>-comparison.md` saying what moved and what it cost in always-on
words. The snapshots themselves are throwaway and are not kept — `prepare.py` rebuilds them from the
repository at any time, and a run's JSON records which builder version it came from.

Put them side by side with the suite's own comparison:

```bash
python3 ../../../core/tests/behaviour/run.py --compare <older>.json <newer>.json
```

Two things make an old run worth keeping. It is a point on a curve, and one point is not a curve: a
single pair of runs can only ever say "this much, once". And the suite can re-judge recorded runs
against today's checks with `--rescore`, so a check you improve later does not throw away the
evidence you already paid for.

The word counts in a comparison need no agent and do not drift between runs. Where a behavioural
difference is small and a cost difference is large, believe the cost.
