# Spec style — reasoning and examples

Why each rule in `.agents/profiles/specs/rules/on-demand/spec-style-rules.md` exists, with bad and good examples. That
checklist is the source of the rules; where this file and it disagree, the checklist wins.

## The rules, explained

### Point, don't repeat

The test's commonest failure: prose the reader could get elsewhere. Link instead. Seven shapes
recur:
- *Within a file* — a sentence restating its own heading, an AC's own Given/When/Then, or
  something another section already said.
- *Across files* — re-deriving what a parent or referenced spec says. Point at it
  (`contract.X`'s AC-3) instead.
- *In `Constraints`* — a dependency edge ("leaf module, must not depend on…") is already an
  obligation in `01-architecture.md`'s Boundaries, which owns them, and the compiler enforces
  it besides. Link, don't restate. A constraint here is an obligation this module adds.
- *In `Public surface`* — `internal`/`private` already state it, and the compiler enforces it,
  so an inventory of public symbols is duplication that loses to the code the moment either
  changes. Say only what visibility can't: a boundary the language has no keyword for (a wire
  format, an RPC surface, a build variant that exports extra symbols), a difference between
  audiences, or which of several public things is the intended entry point. One bullet per
  audience reads best, since the audience split is usually the part no modifier can carry. Where
  "everything else is private" isn't true yet, say so — public-by-accident and public-by-intent
  look identical in the source, and that difference is worth a line.
- *In `Pitfalls`* — only what a reader would get **wrong**. Not a file map (`owns` plus `ls`
  already gives that, and never goes stale), not behaviour (the AC states it), not rationale
  (Decisions states it), not a rule you must follow (that's Constraints).
- *In `References`* — the pointer *is* the reference: don't enumerate a target's methods or
  summarise its rules, which lets a reader skip the document and then drift from it. Don't list
  a sibling spec either — `related:` owns those and is checked. But *do* name a same-module
  `ARCHITECTURE.md` or README: "they'd find it by listing the directory" is wrong, because a
  reader navigating by grep and path may never list it, and a filename alone doesn't say whether
  the document holds build steps or the invariants that aren't obvious from any single file.
  Say which, in a clause — that's what makes the pointer worth following.
- *Next to a citation* — `(see <file>)` is a citation, not licence to also restate what
  that file says. A quoted test name or docstring is the clearest version of this mistake.

Two things look like duplication but aren't. A checked criterion's proof — a test, or `Source: Manual` with its description —
is load-bearing, not decoration — see `spec-format-rules.md`'s "How a criterion was confirmed".
And a gratuitous comparison to another module
("unlike the legacy adapter, this one…") isn't duplication but is the same noise: it's a fact
about that other module. Keep it only if a reader would otherwise make the mistake it
represents.

### One sentence if one sentence does it

A paragraph is a smell — expand only when the requirement is genuinely non-obvious, never because
more words feel more thorough.

### Every chapter earns its place

The test applied to a whole heading: a section that would be empty or near-empty gets deleted, not
stubbed ("None.", "N/A", an empty list). Templates show a fully-fleshed spec, not a checklist to
fill mechanically. `Pitfalls` and `References` are written after implementation and review, and
`Pitfalls` is usually absent entirely — it holds only what a reader would conclude *wrongly* from
the code.

### What was rejected

A decision records it, not just what was chosen — the choice alone is usually visible in the code
— "the service lives in `app`" is answered by `ls`. What no amount of reading recovers is that a
standalone module was specified, built toward, and reversed. That's the half worth keeping, so it
gets its own field:

```markdown
- **{the choice, as a fact}**
  - **Instead of** {the alternative that was rejected}
  - **Because** {one clause — only when naming the alternative doesn't already explain it}
  - **Revisit when** {the condition that would legitimately reopen this}
  - **Replaced {date}:** {the earlier decision this overturned}
```

Only the choice and **Instead of** are usual; the last three appear when they apply. Keep each
to one line — the format buys terseness without losing the payload, so use it for that.

**The test:** would someone reading only the code plausibly propose the thing this rules out?
No → it isn't a Decision. An uncontested fact belongs in Constraints, a scope statement in
Intent, a behaviour in an AC. If you can't fill **Instead of**, that's the signal: nothing was
decided, something was just described.

### One owner per decision

A decision lives in exactly one spec — the narrowest whose scope covers everything it constrains.
Other specs link to it (`see contract.X's Decisions`) and never restate it, because two specs
holding the same decision reliably drift into two different subsets of the reasoning with neither
complete. Link in prose, never as a `- **bold**` bullet: a bullet in a Decisions section *is* an
entry, and re-creates the duplicate you were avoiding. `DECISIONS.md` lists every entry together,
which is the fastest way to catch this.

The narrowest owner is often not the file the code is in. A module that deliberately wraps the
platform logger instead of using the shared one reads as a code-style violation to anyone who
hasn't opened it, so it's a spec Decision even though it concerns a single module — a doc comment
there is invisible at the moment someone "fixes" the apparent violation. (Spec versus doc comment
in general: `spec-builder-rules.md`'s *Where a decision lives*.)

### Revising, not replacing

Update the entry in place and add `- **Replaced {date}:** {what it overturned}`. Don't leave the
old decision live somewhere else, and don't record the reversal only in Change history — a reader
who finds the superseded version first has no way to know it lost. A decision that's conditionally
live gets `- **Revisit when** {condition}` instead: that's a live decision with a known expiry,
not a superseded one.

### Obligation, not description

A constraint binds whoever changes this next. An acceptance criterion says what the system does
and its proof shows it holds; a constraint says what you may not do next, and nothing can prove it until
someone breaks it. That's why it has to be written down. Budgets, ordering and idempotency
guarantees, concurrency rules, build preconditions.

```markdown
- **{the obligation, as an imperative}** — {why, only when it isn't obvious}
  - **Currently violated:** {what breaks it today, and where}
```

If it describes what the code *is*, it belongs elsewhere: a dependency edge in
`01-architecture.md`'s Boundaries, a platform gotcha or a justified absence in `Pitfalls`, a
behaviour in an AC. The test: does this forbid a change someone would otherwise make?

### Question and action

An open question states those two things and nothing else. Background belongs in a linked spec or
ticket. One Action per question, on its own sub-bullet (*Sub-bullet per field*), never its own
checkbox — the question's `[ ]`/`[x]` is the entry's only state. A question needing several
independent actions is usually two questions filed as one. Resolving one strikes through both
lines and adds a third sub-bullet (`- [x] ~~**Question**~~` / `  - ~~**Action:** …~~` / `  -
Resolved: see Decisions → "{{name}}"`); the entry stays in place below the still-open ones, and
isn't deleted except on explicit user request.

### Guarantee, not implementation

An acceptance criterion says what a caller or future maintainer can rely on ("retries are capped
and self-healing"), not the tunable that produces it today ("1s, 2s, 4s, capped at 30s") — that
number lives in code and will drift out of sync the first time someone retunes it. Being
implemented doesn't license restating the implementation. Implementation values aren't only
numbers: a class name, a method call, a framework API (`LaunchedEffect`, a lifecycle callback), or
a state/intent type standing in for a plain description is the same mistake in a different
costume. A criterion should read fine to someone who has never opened this codebase's source. Name a
symbol only when it's the actual public surface the criterion is about — an exception a caller
catches, a method a caller invokes. If "And" chains three or more clauses, that's usually two
criteria wearing one AC number.

### Plain words, no filler

A spec is read by people new to the code and by agents: an everyday word says the same as a formal
one, and nobody has to look it up. Filler costs words and carries no information.

Bad:
> A client that predates this call must leverage the fallback in order to degrade gracefully.

Good:
> A client built before this call uses the fallback.

### Prose over ceremony

Don't reach for a table, a nested list, or a sub-heading when one sentence says the same thing —
structure should track genuine complexity, not habit.

### One row, one sentence: what changed

The ticket column and date already answer who and when; don't re-derive root cause, repro steps,
or a file-by-file account. Reasoning that still matters going forward belongs in Decisions or
Constraints as the current state, not preserved as a log entry. A row is for a change in
documented behaviour or requirements — a new AC, a changed constraint, a bug fix — never for an
editorial pass on the spec's own prose. Nor for creating the spec, narrowing an Open question,
adding a test, or a refactor or restyle that leaves behaviour alone — the current text already
shows where things stand, and the Decision or Open question holds the reasoning.

### Sub-bullet per field

An AC's Given/When/Then/And, an Open question's Action. For AC clauses it's a correctness issue:
Markdown preview collapses consecutive indented lines with no blank line between them into one
run-on paragraph, so the rendered page silently loses the clause structure. For an Action it's
legibility. Either way: a sub-bullet per field, never an em-dash continuation or a bare indented
line, with no reliance on trailing-space hard breaks an editor could strip.

### Verify against code

Open the file before writing a claim about it. Never reason about one from its name or from
memory. Applies
to a Decision's reasoning, an AC's guarantee, a file citation, a claim that something has or
lacks a test. Reasoning abstractly is how a Decision gets kept in a spec when it should have been
a one-line doc comment.

## Examples

One bad/good pair per rule that people get wrong in practice.

**Water in an Intent.** Bad:
> This feature is responsible for handling the processing of refunds. It manages the various state
> transitions and takes care of coordinating with the different systems involved in making sure
> everything works as expected when a refund needs to be issued.

Good:
> Issues refunds against a settled payment, reconciling the ledger and the gateway — the single
> entry point other code calls to move money back to a customer.

**An open question buried in narrative.** Bad:
> During implementation there was some discussion about what should happen when a refund is
> requested for an order that is still being captured, and it's not fully clear yet what the right
> behavior is here.

Good:
> - [ ] **Refund against an uncaptured payment**
>   - **Action:** decide whether `refund()` rejects, queues until capture settles, or voids the
>     authorisation instead.

**An AC restating implementation (*Guarantee, not implementation*).** Bad:
> - [x] **AC-3: Gateway calls retry with backoff**
>   Then it waits 1s, then 2s, then 4s, doubling up to a 30s cap, for up to
>   `GatewayConfig.maxAttempts` attempts — exactly as coded in `GatewayClient.send()` (confirmed by
>   `GatewayClientTest`'s "when the gateway keeps failing then retries to the max then fails")

Good:
> - [ ] **AC-3: Gateway calls are retried with capped backoff, and failure isn't sticky**
>   - **Then** the caller sees `GatewayUnavailable`, and the very next call starts a fresh retry
>     cycle with no extra action from the caller (schedule and cap: `GatewayConfig`)

The bad version is a transcript of one function plus a quoted test name. The good version states
the two things a caller must trust without reading the implementation: retries are bounded, and a
failure doesn't poison the client. The numbers stay in code, where they can change without the spec
lying.

**The same mistake with no numbers involved.** Bad:
> - **Then** state goes `Loading`, `LedgerRepository.fetchEntries()` is called, and each
>   `LedgerRow(id, amountMinor)` maps 1:1 to `Entry(id, amount = amountMinor / 100)`

Good:
> - **Then** a loading state shows while the ledger is being read, and each entry's amount is
>   presented in major units

The repository class, the DTO and the field names are wiring, not a claim a tester or a
non-programmer can check.

**Pitfalls used as a file map (*Point, don't repeat*).** Bad:
> Confirmed by reading every file in the module. Three pieces, each with one job: `RefundRequest`
> validates the input, `RefundProcessor` orchestrates the call, and `RefundLedger` records the
> result (see AC-3)…

Good — delete the whole section, and keep only what reading the code would get wrong:
> `PaymentGateway.void()` looks like the natural way to cancel an uncaptured charge, but it is
> wired only to the admin console's manual path, not to this flow — calling it here would bypass
> the ledger write.

The bad version is a directory listing with adjectives, plus an AC number. Nobody is misled by any
of it, so none of it earns a section. The good version states the one thing a reader *would* get
wrong: the function they are about to reuse isn't wired where they'd assume.

**References restating a target's contents.** Bad:
> - `payments-client`'s `Gateway` docs — the exact contract this service calls
>   (`authorize()`, `capture()`, `refund()`, and the exceptions and threading guarantees).
> - `feature.payments-client` — the client module this service exercises.

Good:
> - `payments-client`'s `Gateway` docs — the contract this service calls against.

The second line is already `related:` in the frontmatter, and it is checked. The method list is
exactly why to open the docs, not a reason to copy them here.

**A Change history row as an incident report.** Bad:
> | PAY-482 | Fixed a reported bug: after a gateway timeout the refund button stayed disabled
> forever… Root cause traced by reading `RefundProcessor` directly: once the retry budget is spent
> the state machine has no transition back to idle… |

Good:
> | PAY-482 | Fixed the refund button staying disabled after a gateway timeout by resetting state
> when the retry budget is spent | 2026-01-14 |

**A decision as narrative.** Bad:
> We talked about this for a while and initially considered putting the ledger in its own service,
> but after further discussion the team ultimately decided it should live in the checkout module.

Also bad — terse, but it threw away the only part that wasn't already in the code:
> - **The ledger lives in the checkout module.**

Good:
> - **The ledger lives in the checkout module**
>   - **Instead of** its own service
>   - **Because** every write is in the same transaction as the payment it records, and splitting
>     them would need a distributed commit to keep the two consistent
>   - **Revisit when** a second writer needs the ledger

The short version isn't wrong about the location — a directory listing already answers that. It's
wrong about what the entry is for. A future reader who can't see that a separate service was
considered will propose one, which is precisely what this decision exists to stop.

**Not a decision at all.** Bad:
> - **The four `RefundState` values are the contract's vocabulary — no new states** — REQUESTED /
>   SETTLED / REJECTED / FAILED are already shipped and cover every outcome in AC-1 – AC-9.

Nothing was rejected here; the published API's versioning rules already forbid adding a state.
There's no **Instead of** to write, because nobody chose anything. It's a constraint — file it
under Constraints and delete the entry.
