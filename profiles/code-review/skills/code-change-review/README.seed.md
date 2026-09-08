# code-change-review

Reviews one merge or pull request, or a branch before a request exists, through three read-only lanes,
and posts only what the user picks. It runs the other direction too: hand it the comments left on a
request and it works them one thread at a time. Works on any forge and any stack, because everything
specific to a project lives in a rule beside it rather than in the skill.

## Setup

Three pieces, and the third is the one that gets forgotten.

1. **The skill** — this folder, at `.agents/skills/code-change-review/`.
2. **Its three agents** — `code-reviewer-business`, `code-reviewer-technical` and `code-reviewer-security`, into
   `.claude/agents/` and `.codex/agents/`. Without them the main session runs all three lanes itself,
   which works but loses the fresh-eyes property: a lane that did not write the code reviews it.
3. **Its rule** — `project-review-rules.md` in this profile's own `rules/on-demand/`, plus a row in
   `LOADER.md`. Start from `project-review-rules.seed.md`, which is the form with the questions in it.

### Why the rule is separate, and why the skill never names it

The skill holds the method: three lanes, three severity gates, the evidence bar, the comment contract.
None of that changes between projects. What changes is every fact the method needs — and the skill is
written to reference nothing but `AGENTS.md`, so those facts have to arrive another way: the loader
reads the rule into the session before the review starts, and the skill uses what is already there.

The direction only goes one way. A loader row names a rule; a rule never names the skill; the skill
never names a rule. Point them at each other and the pair stops being installable on its own.

### What goes in the rule

| Section | What it answers | Why the review is worse without it |
|---|---|---|
| Where the work is reviewed | The forge, the project path a CLI needs, how a ticket id is derived | A lane cannot anchor a comment, or guesses the wrong repository |
| Requirement sources, in order | The tracker, the wiki pages, the in-repo specs, and which are mandatory for which areas | The business lane reports scope it cannot verify, or invents criteria |
| Reachability | Which modules ship ahead of the code that calls them, and the chain to follow — construction, injection, call site, and the flag guarding it | Severity inflates: dead code gets marked Required |
| Documents for a guideline claim | The official docs a claim must cite | Guidelines get quoted from memory, and memory is wrong |
| Performance claims | The dimension that actually bites here, and how to measure it | Unmeasured tidiness findings reach the author |
| Closing a review | The commands that end a review, and what a working copy needs before it can build | Findings stay prose because nobody believes a build is possible |

The last row earns its place: a rule that says a build cannot run is a rule that turns provable
findings into opinions. Say how the build *is* obtained.

## Usage

Invoke by name, or ask for a review of a request or a branch. The flow: freeze the candidate at fixed
refs, run the three lanes over the same diff in parallel, grade what they return, then post only what
the user selects.

Nothing is Required until it passes three gates in order — not pre-existing against the frozen base,
reachable in the shipped build, and proven rather than inferred. That ordering is what keeps a review
from drowning its author.

**The main session fetches the requirement documents.** A lane has no tracker or wiki access: paste
what it needs into its prompt, and name anything you could not retrieve. A lane that is handed the
requirement documents checks the change against criteria the code alone cannot express; a lane without
them reviews code against itself.

### Answering a review

Ask it to go through the comments on a request and it takes one thread at a time: explains what the
reviewer is saying and what the code does at the current head, triages it through the same three
gates, then closes it with any of a code change, a document change (a ticket, a criterion, a spec that
no longer matches) and a reply saying what was done and why.

This is the one mode that edits the author's code, and only per fix, after the user picks it: one
commit per thread, red-then-green where behaviour changes, and it never pushes. It never resolves a
thread it disagreed with, because that comment belongs to the reviewer who wrote it.

## Troubleshooting

- **Findings arrive as prose with no proof** — the lane believes it cannot build. Check what the rule
  says about obtaining a build; a probe that asserts the buggy behaviour and passes is enough to mark
  a finding PROVEN, and needs no patch.
- **A lane reports scope it cannot verify** — a requirement source in the rule was not retrieved, or
  was never passed into the prompt.
- **Severity looks inflated** — the reachability section of the rule is missing or thin, so a lane
  cannot tell shipped code from code that nothing calls yet.
- **The skill does not load on "review this code"** — that phrase belongs to a clean-code skill where
  one is installed. Name the request, or invoke this skill by name.

## See also

- `SKILL.md` — the gates, the comment contract and the workflow
- `reference.md` — the local and response modes, the code-suggestion contract, each forge's mechanics
