# Profile: code-review

A feature profile, not a stack profile. It holds one capability — reviewing a code change through
three read-only lanes — and everything that capability needs to work. It stays in the builder and is
never installed.

Nothing here is true of one project or one stack. The forge, the tracker and the commands are
questions the form asks; the method does not change between projects.

## All or nothing

**This profile installs whole or not at all.** `SETUP.md` offers it as one choice, not as four
optional pieces, and a "yes" installs every file in the tree below.

The parts are not independently useful, and half of it is worse than none:

- The **skill** without its **rule** has no forge to post to, no tracker to check scope against and no
  idea how a build is obtained. It degrades to reviewing code against itself.
- The **rule** without the **skill** is a file nothing reads.
- The **skill** without its **agents** still runs, but the main session performs all three lanes
  itself and loses the one property a subagent buys: a reviewer that did not write the code.
- The **rule** without its `LOADER.md` row never loads, which looks exactly like the rule being wrong.

A project that wants only part of this wants a different skill, not a subset of this one.

## What installs

| Block | Lands at |
|---|---|
| `skills/code-change-review/` | `.agents/skills/code-change-review/` |
| `skills/code-change-review/README.seed.md` | `.agents/skills/code-change-review/README.md` — a form: the
  method is forge-neutral here, and a project rewrites the page for its own forge, its setup steps and
  the gotchas that bit it |
| `agents/claude/reviewer-*.md` | `.claude/agents/` |
| `agents/codex/reviewer_*.toml` | `.codex/agents/` |
| `rules/on-demand/project-review-rules.seed.md` | answered where it sits, inside this profile; a line in `.agents/LOADER.md` places it, proposed when the sync reports it unplaced |

## Detection

None. A stack profile is chosen by reading the repository; this one is chosen by asking the user
whether the team wants AI review of its merge or pull requests. There is no evidence in a codebase
that answers that.

## What the project still has to answer

The form's questions, none of which the builder can guess:

- The forge, the project path a CLI needs, and how a ticket id is derived
- The requirement sources in order, and which are mandatory for which areas
- Which modules ship ahead of the code that calls them, and the chain that proves reachability
- The official documents a guideline claim must cite
- The performance dimension that bites here, and how to measure it
- The commands that close a review, and how a review copy obtains a build

The last one decides whether findings arrive proven or as opinions. A form answer claiming a build is
impossible turns every finding into prose.
