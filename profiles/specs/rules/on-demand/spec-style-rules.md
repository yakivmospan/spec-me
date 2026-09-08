# Spec style rules

KISS for spec content: every sentence taxes every future reader, human or agent. This is the checklist
to draft against. Why each rule exists, with a bad and a good example of each:
`.agents/skills/spec-check-style/reference.md` — read an entry when a line here doesn't settle a case.

## The delete test

Before finalizing any sentence, section or chapter: *if I deleted this, would a reader lose information
they actually need?* If not, delete it.

## Get these right while drafting

### What was rejected
A Decision records the choice **and what it ruled out** — the half the code can't show:
`- **{the choice}**`, then `- **Instead of** {…}`; `Because`, `Revisit when` and `Replaced {date}:` only
when they apply, one line each. **Test:** would someone reading only the code propose what this rules
out? With no **Instead of** to write, it isn't a Decision — it's a Constraint, Intent or an AC.

### One owner per decision
A decision lives in one spec, the narrowest whose scope covers everything it constrains. Others link to
it in prose, never as a bullet. A single-file decision that contradicts a project-wide rule is still a
spec Decision: a doc comment is invisible to whoever "fixes" the apparent violation.

### Revising, not replacing
Update the entry in place and add `- **Replaced {date}:** {what it overturned}`. Never leave the old
decision live elsewhere, or record the reversal only in Change history.

### Guarantee, not implementation
A criterion says what a caller can rely on — not the tunable, class, method, framework API or state type
that produces it today. Name a symbol only when it is the public surface the criterion is about.
**Test:** it reads fine to someone who has never opened the source. Three or more "And"s is usually two
criteria.

### Obligation, not description
A Constraint forbids a change someone would otherwise make — a budget, an ordering, idempotency,
concurrency, a build precondition — as an imperative, with `- **Currently violated:** {…}` where the code
breaks it today. **Test:** does it forbid something? A dependency edge belongs to `01-architecture.md`'s
Boundaries, a gotcha to Pitfalls, a behaviour to an AC.

### Question and action
An Open question holds the question and one **Action** sub-bullet, nothing else; its `[ ]`/`[x]` is its
only state. Resolving it strikes both lines through and adds `- Resolved: see Decisions → "{name}"`, or `see the doc comment in {file}` for a file-scoped answer. It
stays in place, deleted only when the user asks. Several independent actions are several questions.

### Verify against code
Open the file before writing any claim about it — a Decision's reasoning, a guarantee, a file
citation, whether something has a test. Never from a name or from memory.

### Point, don't repeat
Link rather than restate what is said elsewhere: in the same file, in a parent or referenced spec, a
dependency edge in Constraints, a symbol inventory in Public surface — which says only what visibility
can't: a wire format, an audience split, the intended entry point. Pitfalls hold only what a reader would
get **wrong**; References point without summarising, and never list a `related:` sibling. A checked criterion's
proof — a test, or `Source: Manual` with its description — is not a repeat.

## Polish — `spec-check-style --fix` catches these when it runs

### One sentence if one sentence does it
A paragraph is a smell. Expand only for a genuinely non-obvious requirement.

### Every chapter earns its place
A section with nothing real is deleted, never stubbed. Pitfalls and References are written when the
work finds them, and Pitfalls is usually absent.

### Plain words, no filler
Everyday words over formal ones: "made before", not "predates"; "use", not "leverage". A name from the
code stays. "Simply", "just", "basically", "in order to", "robust", "seamless": delete on sight.

### Prose over ceremony
No table, nested list or sub-heading where one sentence says the same thing.

### One row, one sentence
A Change history row says what changed in documented behaviour or requirements, in one sentence — not
the root cause, repro or a file list. No row for creating a spec, an Open question, a test, a refactor or
an editorial pass.

### Sub-bullet per field
Each Given, When, Then and And, and each Action, on its own sub-bullet — Markdown collapses consecutive
indented lines into one run-on paragraph.
