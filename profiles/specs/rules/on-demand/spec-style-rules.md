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
`- **{the choice}**`, then `- **Instead of** {…}`, where an option tried and dropped also goes, with
what went wrong in a clause. `Because`, `Revisit when` and a cost the choice accepts only when they
apply, a sentence or two each. A rule the choice produces is a Behaviour line, not part of the
Decision. Past about ten Decisions, group them under the bold labels the spec's Behaviour uses.
**Test:** would someone reading only the code propose what this rules out? With no **Instead of** to
write, it isn't a Decision — it's Intent or a Behaviour line. A wording, a name or a signature the
code shows — a dialog's text, `NotSupported` over `TooOld`, a `Unit` return over a `Boolean` — is never
one either: the code already says it, and nothing is gained by saying it twice.

### One owner per decision
A decision lives in one spec, the narrowest whose scope covers everything it constrains. Others link to
it in prose, never as a bullet. A single-file decision that contradicts a project-wide rule is still a
spec Decision: a doc comment is invisible to whoever "fixes" the apparent violation.

### Revising, not replacing
Edit the entry in place to the choice that holds now; the overturned one joins its **Instead of**, with
what was learned, and Change history gets a dated row; no story of earlier versions inside the
Decision. Never leave the old
decision live elsewhere, or record the reversal only in Change history.

### Guarantee, not implementation
A Behaviour line says what a caller can rely on — not the tunable, class, method, framework API or state
type that produces it today. Name a symbol only when it is the public surface the line is about.
**Test:** it reads fine to someone who has never opened the source. A line needing three or more
clauses is usually two lines. A dependency edge belongs to `01-architecture.md`'s Boundaries, a gotcha
to Pitfalls.

### Features, as a user says it
`00-product.md`'s Features say what a user can do, in their words — "Make it warmer or cooler, or turn
on pet mode", not "Climate — power, AC, fan" — under headings a user would use. A spec that describes
one is named in brackets at the end of its line; with none, nothing is named.

### Question and action
An Open question holds the question, in bold, and one **Action** sub-bullet, nothing else — no
checkbox. Once answered it is deleted: the answer lives on as a Decision, a doc comment or the code.
Several independent actions are several questions.

### Verify against code
Open the file before writing any claim about it — a Decision's reasoning, a guarantee, a file
citation, whether something has a test. Never from a name or from memory.

### Point, don't repeat
Link rather than restate what is said elsewhere: in the same file, in a parent or referenced spec, or
in the code — a list of public symbols repeats it; a Behaviour line says only what visibility can't: a
wire format, who may call, the intended entry point. Pitfalls hold only what a reader would get
**wrong**; References point without summarising, and never list a `related:` sibling. A rule the
code's own docs already state belongs to the doc its reader opens — a module's users: its README, or
the doc comment on the call; its maintainers: its `ARCHITECTURE.md` or other docs in the repo — and the
spec points there, keeping only what no such doc says. Docs outside the repo (a vendor's interface
document, a wiki) are pointed at under References, never copied; a rule we own never lives only there.

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
A Change history row says what changed in documented behaviour or requirements, or which Decision was
revised, in one sentence — not
the root cause, repro or a file list. No row for creating a spec, an Open question, a test, a refactor or
an editorial pass.

### Sub-bullet per field
Each Instead of, Action and Future plan field on its own sub-bullet — Markdown collapses consecutive
indented lines into one run-on paragraph.
