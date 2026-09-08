# Spec builder rules

Always-on. What every task in this spec-driven setup follows.

## Constitution

The constitution is `CONSTITUTION.md`, and it outranks this file too. These two principles are
what it adds where a project has specs:

- **A person's word is enough.** A criterion with `Source: Manual` under `Verified:` is complete.
  Tests are welcome, never demanded.
- **Specs are memory any agent can use.** A spec reads and changes correctly by hand, or with any
  agent or tool — no skill, rule, script or generated file from this setup is needed to understand
  one or to edit one. The setup helps; the specs never depend on it.

## Ground rules

| Rule | Detail |
|---|---|
| Specs vs. code | Stop and say so before writing anything; don't silently pick a side. Inside a change, code behind its spec files while its tasks — or, with no plan, its criteria — are still open is expected, not a conflict. |
| One owner per file | The most specific glob in `owns` wins — fewest wildcards, then most path segments. Two equal globs matching one file is a bug — flag it. |
| Where a decision lives | Inside one file → its doc comment; anywhere else, including a single-file decision that contradicts a project-wide rule → a spec Decision (spec-style-rules' *One owner per decision*). |

## Every task

1. Read `.specs/README.md` up to *Change what a spec guarantees*, once a session. For each file you'll
   edit, find its owning spec by `owns` — `INDEX.md` routes it when current — and read it; when it has moved into an open
   change, read it there — its `git diff -M` against the branch the change will merge into is what the change adds. No owner is normal, not a blocker. A spec `INDEX.md` lists as possibly
   stale: say so in one line, offer `spec-sync-with-code` once a session per spec — unless `spec-create`
   is about to move it into a change, which runs it — and carry on.
2. Before proposing an approach or explaining why something is built as it is, read the Decisions that
   bind it — the owning spec's, its parents', its `related` specs' and any pending change's
   (`.specs/DECISIONS.md` groups them); all of them only when the approach cuts across the tree.
   A Decision in the way is raised, never enforced: name it, say what changing it would affect and
   what it bought, weigh that against what the change gains, and give your read. Any Decision may be
   questioned unless it says otherwise — "we wrote it once" is not a reason, and a Decision already
   carrying a `Replaced` line is one the project has revised before. Answering an Open question, and
   the call on a Decision, stay the user's.
3. Anything that adds, changes or removes what a spec guarantees, worth finding later, starts as a
   change through `spec-create` before any code. Not needed for a one-line fix, a fix that makes code
   meet a criterion already written, or correcting a stale spec to code that's already right.
4. A module is added, a boundary moves, or there's a real choice between designs: design it with the
   user — inside a change through `spec-plan`, outside one in chat, recorded per
   `spec-architecture-rules.md`. The `spec-architect` subagent reads and compares; the user decides. It's
   not a file count.
5. Implement — inside a change, only when asked, through `spec-plan`.
6. New or changed public surface, when tests are wanted: the `spec-test-writer` / `spec_test_writer` subagent,
   pointed at the acceptance criteria and `.specs/02-tech.md`'s Testing section.
7. Build, lint or tests to check the result: the `runner` subagent, instead of reading raw output.
8. Work outside a change moved something a spec states — behaviour, surface, owned paths, something it
   records as broken or pending: update that spec alongside the code (*Keeping it honest*); inside a
   change, its spec files. No spec, and the work turned out substantial: consider `spec-create`.

On Codex, a step that hands work to a subagent or the background needs an explicit ask; without one,
work inline.

## Keeping it honest

| When | Do |
|---|---|
| A test a criterion lists is renamed, moved or deleted | Update the `Source:` under that criterion's `Verified:`. |
| You fixed or changed something a spec records as broken, missing or pending — a `Currently violated`, a Pitfall, an Open question | Search `.specs/` for it and correct every line that describes it; nothing detects this for you. |
| Code is deleted or moved | Update `owns`. |
| A spec is confirmed against its code — merged, corrected in place, a clean check, or a design recorded with its code | Set `updated` to that day — not while differences are still open. |
| A spec is behind code that's already right | On the user's yes, correct it in place — criteria without proof, or reworded, become `Source: Manual`, never one for something not built — with a Change history row (its ticket, or "No ticket") and `updated`. |
