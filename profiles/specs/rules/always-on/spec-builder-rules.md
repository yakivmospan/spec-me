# Spec builder rules

Always-on. What every task in this spec-driven setup follows.

## Constitution

The constitution is `CONSTITUTION.md`, and it outranks this file too. These two principles are
what it adds where a project has specs:

- **A person's word is enough.** A Behaviour line the user agreed to is complete with no test behind
  it. Tests are welcome, never demanded.
- **Specs are memory any agent can use.** A spec reads and changes correctly by hand, or with any
  agent or tool — no skill, rule, script or generated file from this setup is needed to understand
  one or to edit one. The setup helps; the specs never depend on it.

## Ground rules

| Rule | Detail |
|---|---|
| Specs vs. code | As *Code first* in the ground rules says. A spec documents what's built; a plan says what will be — code behind an open plan is expected, not a conflict. |
| One owner per file | The most specific glob in `owns` wins — fewest wildcards, then most path segments. Two equal globs matching one file is a bug — flag it. |
| Where a decision lives | Inside one file → its doc comment; anywhere else, including a single-file decision that contradicts a project-wide rule → a spec Decision (spec-style-rules' *One owner per decision*). |

## Two ways to work

- **Shaping, the default.** Build what the user asks, let them try it, adjust, repeat — no change
  folder, plan or approval. A spec the work moves is edited in place as you go: Behaviour to what's
  built, a Decision for an option tried and dropped, one Change history row for the work, not per
  tweak. Inside a planned change too, where a tweak adds no task.
- **Planning, only when asked** — "plan", "design", "spec this out": `spec-create`, then `spec-plan`.
  Work that adds a module, moves a boundary or has a real design choice: suggest planning once.
- **Only a red flag interrupts:** the work would break something the request didn't mean to change —
  another feature, saved data, the build — or goes against a Decision. Say it in one line and wait.
  A Behaviour line the request itself changes is no red flag; spec bookkeeping is done and reported,
  never asked.
- **Every question or suggestion is one line,** readable at a glance; while shaping, one at a time.

## Every task

1. Read `.specs/README.md` up to *Change what a spec guarantees*, once a session. For each file you'll
   edit, find its owning spec by `owns` — `INDEX.md` routes it when current — and read it, and the
   plan of any open change that touches it. No owner is normal, not a blocker. A spec
   `INDEX.md` lists as possibly stale: say so in one line, offer `spec-sync-with-code` once a session
   per spec, and carry on.
2. Before proposing an approach or explaining why something is built as it is, read the Decisions that
   bind it — the owning spec's, its parents' and its `related` specs' (`.specs/DECISIONS.md` groups
   them); all of them only when the approach cuts across the tree.
   A Decision in the way is raised, never enforced: name it, say what changing it would affect and
   what it bought, weigh that against what the change gains, and give your read. Any Decision may be
   questioned unless it says otherwise — "we wrote it once" is not a reason, and a Decision whose
   *Instead of* names an option tried and dropped is one the project has revised before. Answering an Open question, and
   the call on a Decision, stay the user's.
3. Shape, or plan when asked (*Two ways to work*).
4. A module is added, a boundary moves, or there's a real choice between designs: design it with the
   user — inside a change through `spec-plan`, outside one in chat, recorded per
   `spec-architecture-rules.md`. The `spec-architect` subagent reads and compares; the user decides. It's
   not a file count.
5. Implement — inside a planned change, only when asked, through `spec-plan`.
6. New or changed public surface, when tests are wanted: the `spec-test-writer` / `spec_test_writer` subagent,
   pointed at the owning spec's Behaviour and `.specs/02-tech.md`'s Testing section.
7. Build, lint or tests to check the result: the `runner` subagent, instead of reading raw output.

On Codex, a step that hands work to a subagent or the background needs an explicit ask; without one,
work inline.

## Keeping it honest

| When | Do |
|---|---|
| You fixed or changed something a spec records as broken, missing or pending — a Pitfall, a Future plan, an Open question | Search `.specs/` for it and correct every line that describes it; nothing detects this for you. |
| Code or tests are deleted or moved | Update `owns`. |
| A spec is confirmed against its code — updated as the code moved, corrected in place, a clean check, or a design recorded with its code | Set `updated` to that day — not while differences are still open. |
| A spec is behind code that's already right | Correct it in place, with a Change history row (its ticket, or "No ticket") and `updated` — straight away when your own work moved it, otherwise on the user's yes. |
