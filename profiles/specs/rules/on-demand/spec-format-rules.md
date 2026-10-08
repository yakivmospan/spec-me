# Spec format rules

The shape of a spec: what each section must contain and how it changes over time. `.specs/README.md`
is the reader's view of the same shape; this adds what a writer needs. Read with
`spec-style-rules.md`, which owns the words. A spec reads and changes correctly without this setup: no
pointer into `.agents/`, no skill name, no meaning only a script supplies.

## Frontmatter
Required: `id`, `title`, `status`, `parent`. `status` is `merged` for a spec in `.specs/`, and `draft` or
`approved` for a spec file in a change (`spec-change-rules.md`'s *Stages*).

```yaml
---
id: feature.checkout          # unique, dot-namespaced
title: Checkout flow
status: merged                # draft or approved in a change; merged once merged
parent: architecture          # id of the parent spec, not its filename; only product has parent: null
owns:                         # glob(s) this spec is the source of truth for, its tests included; [] is valid
  - "src/checkout/**"
  - "test/checkout/**"
ticket: PROJ-1234             # optional pointer, not a synced mirror
related: [feature.cart, tech]
updated: 2026-01-01           # the day this spec was last confirmed against its code
---
```

`owns` lists the spec's tests as well as its code, where they don't already fall under a code glob:
the tests are the proof of its Behaviour, and this is how a reader finds them.

`updated:` moves when the spec is confirmed against its code: merging, a correction in place, a clean
check against its code, or a design recorded alongside its code (spec-architecture-rules' *Recording a decision*).

## Change
Only in a spec file inside a change, right under the title: why the spec is being written or changed,
in a sentence or two — or that the change removes it. When the change merges, it becomes the Change
history row, or is deleted.

## Behaviour
One bullet per rule the code follows on purpose, a sentence or two at most: what a caller can rely on.
List what a reader could get wrong or that was a real choice — an edge case, a failure, timing or
order, who may call, a wire format, an obligation a change must not break — and leave out the happy
path anyone would expect. Past about ten lines, group them under bold labels. No ids, Given/When/Then,
checkboxes or test names: the tests are the proof, found through `owns`, and a line no test covers is
still a rule. A rule the code breaks today keeps its line, with
`- **Currently violated:** {what breaks it, and where that's tracked}` under it. What the code does
that nobody chose — found while writing a spec from code, a likely bug — is not a rule: it goes under
Pitfalls, with an Open question on whether it should change. Wording:
spec-style-rules' *Guarantee, not implementation*.

```markdown
## Behaviour
- A dropped upload is retried once, then reported as failed.
- Only the signed-in account's uploads are sent; another account's stay queued.
- Calls before `init` fail without reaching the network.
  - **Currently violated:** `refresh()` still sends; PROJ-1300.
```

## Contracts
Only for work spanning several modules: `.agents/profiles/specs/templates/spec-contract.md`, `owns: []`, its
Behaviour at product level — what holds across the modules. Like a feature, it has an Intent; it adds `## Source` — where it came from: a ticket link, kept in step by hand
when the ticket changes, or "Originated here" — and `## Implementation`, a table of each feature spec and
module taking part and its role. A feature taking part names the contract in its Intent. A module in the Implementation table needn't be the
contract's child — `parent: architecture` suits a shared component several contracts rely on.
Whether a feature gets its own spec or folds into an existing one is a size call.

## What counts as a feature
A behavioural contract something else depends on — an end user, another team, or other code here.
Code that callers merely borrow, like a retry helper, gets no spec: document it in
`01-architecture.md`'s Cross-cutting concerns or `02-tech.md`'s Key libraries.

## Change history
A `| Ticket | Change | Date |` table, one row per change in documented behaviour or requirements — "No ticket" is
valid for a hotfix or a code-first reconciliation — written when a change merges, or alongside the
code outside a change. What qualifies and how to word it: spec-style-rules' *One row, one sentence*.

## Open questions
Never resolve one by picking something plausible: capture the decision first — a Decisions entry,
or the code itself for a pure implementation call. Format and resolve lifecycle: spec-style-rules'
*Question and action*.

## Future plans
What the user wants later, decided or only an idea. Not a guarantee: nothing here is built or tested,
and a change that takes one up deletes it and writes its Behaviour lines. Something undecided that blocks
work now is an Open question instead.

```markdown
- **{the plan, as what it does}**
  - **Why:** {what it gives, only when the title doesn't say it}
  - **Not yet because:** {only when there's a reason beyond "not now"}
  - **Take up when:** {the condition, if known}
```
