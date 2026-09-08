# Does the setup actually hold?

The suite next door, `stress_profile_sync.py`, proves the files and the links are right. It cannot
tell you whether an agent *follows* any of it. This one asks that question, by starting a real agent
in a throwaway copy of this setup and checking mechanically what it did.

It answers four things the mechanical suite cannot:

- **Does load change behaviour?** The same case runs with the window 0%, 25%, 75% or 100% full.
- **Does it survive a compaction?** At a high enough load the session is compacted mid-run, and the
  case still expects the constitution to be followed.
- **Does it recover by itself?** A case can accept *either* a correct answer *or* the agent going
  back and re-reading the file — recovering is a pass, guessing is not.
- **Is the wiring real?** Skills name subagents. A case checks the subagent was actually started.

## Running it

Two ways, and the first needs nothing installed.

### By hand, scoring the session afterwards

```bash
python3 run.py --prompts
```

prints every case prompt. Open a fresh session in this repository, send them one message each, then:

```bash
python3 run.py --transcript latest
```

Claude Code writes every session to `~/.claude/projects/<repo>/<id>.jsonl`, and that file holds the
same evidence a headless run would print — which files were opened, which skill was invoked, which
subagent was started, what was finally said. So a session someone drives by hand scores exactly like
an automated one, and the report says whether a compaction happened during it.

This is also the only way to measure the thing you actually use: a real session, with its real
system prompt, its real skill discovery and its real compaction.

### Headless, for the wide grid

The automated path needs an agent on `PATH`. Claude Code:

```bash
npm install -g @anthropic-ai/claude-code
```

Then, from this folder:

```bash
python3 run.py --agent claude --load 25 --repeats 3
```

```bash
python3 run.py --agent claude --load 0,25,75,100 --repeats 3
```

`--dry-run` starts no agent and prints each case's **floor**: what it scores when nothing happens at
all. A case whose floor is 100% measures nothing, and the report says so by name. A real run has to
beat its floor before its number means anything.

`--list` prints every case and what it checks. `--only <text>` narrows to matching cases.
`--transcript <file>` scores a particular session instead of the newest one.

### An agent this cannot start by itself

Some agents have no scriptable interface, and a subagent's internal steps are written down nowhere
readable. Both arrive the same way: one JSON file per case, named `<case-id>.json`.

```json
{"answer": "what it replied", "files_read": [], "skills_used": [], "agents_spawned": []}
```

```bash
python3 run.py --ingest <folder> --agent subagent
```

They are scored on exactly the same footing as everything else, with one difference that is stated
rather than hidden: the tool checks rest on the agent's own account of what it did, so they are
labelled *(agent's own word)* and the report counts how many. An agent describing its own actions is
weaker evidence than a recorded call — sometimes it is the only evidence available, and then it is
worth having, marked.

## Running the same checks again later, for free

Every run keeps the raw output of every take under `results/transcripts/`.

```bash
python3 run.py --rescore results/<a-run>.json
```

re-runs **today's** checks against sessions recorded whenever, with no agent and no cost. That is
what makes an agent CLI a one-off rather than a dependency: once behaviour is recorded, a check can
be rewritten and every past run re-judged on the new standard, so a number from months ago and one
from today are comparable.

## What the always-on budget is actually buying

The per-file cap is 300 words. It is stated once, in a table, justified by "every word loads every
session" — which is a reason to care about size, not evidence that 300 is the line. Nobody measured
it. So measure it:

```bash
python3 run.py --load 25 --repeats 3                    # today's rules
python3 run.py --load 25 --repeats 3 --inflate 3000     # as if the cap were much higher
```

Every run prints what the always-on rules actually cost in words, so two runs compare directly. The
padding is real guidance moved out of the on-demand rules, not invented text, because that is what
raising a cap looks like in practice — people move more into always-on. Filler would measure an
agent's patience with nonsense instead.

Read the result carefully. A score that holds at three times the rules says the cap is cheap
insurance and could be relaxed. A score that falls says the budget is load-bearing and the number
should be argued from the curve, not from a table.

## What one rule is actually buying

```bash
python3 run.py --ablate .agents/profiles/specs/rules/always-on/spec-builder-rules.md --load 25
```

runs everything with that file taken out, using the real uninstall — delete it, run the sync,
and it drops the file's `LOADER.md` line — so the copy is what a project that never had that rule would
have, not a broken one. Compare against a run that had it: **what the score loses is what the file
was buying.** A rule that costs 766 words every session and changes no score is a rule to argue
about.

## Cost, and why repeats

Every take is a real agent session in a fresh copy, and a take at 100% load makes the agent read a
hundred-odd files first. Fourteen cases, four loads, three takes is 168 sessions — start with one
load and one take while you are changing cases, and run the wide grid when you want a number to
keep. Scoring a session you drove by hand costs nothing beyond the session itself.

Three takes is the default because agents are not deterministic. One passing run is an anecdote.

## Adding an agent

Add a table to `agents.toml`. Nothing in `run.py` names a particular agent:

```toml
[my-agent]
command = ["my-agent", "--headless", "{prompt}"]
events = "jsonl"        # or "stream-json", or "text" when there is no structure
version = ["my-agent", "--version"]
```

Tool checks need `events` to be one of the JSON shapes; with `text` only the answer checks score, and
the rest are reported as failures rather than silently skipped.

## Adding a case

Add to `cases.toml`. Keep two things in mind, because both were got wrong here first:

- **A case must be able to fail.** Checks built only from `answer_lacks` and `file_unchanged` are
  satisfied by an agent that says nothing. Pair them with something only a real answer can pass.
- **`dimension` is what the score reports.** Cases group into it, so a run says which part is
  slipping rather than giving one number with no handle on it.

## Reading the score

A dimension is the mean of its cases; a case is the fraction of its checks that passed; overall is
the mean of the dimensions. Every run is written to `results/` with the agent, its version, the
builder version and the load, so:

```bash
python3 run.py --compare results/<older>.json results/<newer>.json
```

prints each dimension side by side with `better`, `same` or `WORSE`. That is the whole point of
storing runs: the question is not "is the score good" — it is "did it move, and which way".

## What this does not prove

A pass is evidence, not a guarantee: these are nine requests out of everything anyone might ask, and
the checks are mechanical, so an agent can satisfy one for the wrong reason. Treat a falling number
as a real signal and a perfect score as the absence of one.
