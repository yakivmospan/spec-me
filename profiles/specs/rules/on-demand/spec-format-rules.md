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
owns:                         # glob(s) this spec is the source of truth for; [] is valid
  - "src/checkout/**"
ticket: PROJ-1234             # optional pointer, not a synced mirror
related: [feature.cart, tech]
updated: 2026-01-01           # the day this spec was last confirmed against its code
---
```

`updated:` moves when the spec is confirmed against its code: merging, a correction in place, a clean
check of its criteria, or a design recorded alongside its code (spec-architecture-rules' *Recording a decision*).

## Change
Only in a spec file inside a change, right under the title: why the spec is being written or changed,
in a sentence or two — or that the change removes it. When the change merges, it becomes the Change
history row, or is deleted.

## Acceptance criteria
`- [ ] **AC-n: {name}**`, then a sub-bullet each for Given, When, Then and any And, with `Verified:` last —
one scenario per criterion. A one-line "- [ ] retry on failure" isn't actionable. What a
clause may say: spec-style-rules' *Guarantee, not implementation*.

## How a criterion was confirmed
A criterion's proof sits under `Verified:`, one `Source:` per proof, as its last field:

```markdown
  - **Verified:**
    - **Source:** `UploadRetryTest.kt`
      - `when the connection drops then retries once`
    - **Source:** Manual
      - Dana, on a device, build 1.4.2
```

- **Automated proof:** `Source:` names one test file — by name, or by as much of the path as tells two
  apart — with the test functions declared in it under it, exactly as declared. Test names follow
  `02-tech.md` alone, never a criterion id.
- **Manual proof:** `Source: Manual`, with an optional description under it — who, where, which build.
- **Checkbox:** `[x]` when `Verified:` holds at least one source, `[ ]` when it holds none, or while a reworded criterion's tests
  are still to be changed — in a spec or in a change. A contract criterion is checked by its own proof or, when feature criteria name it, once all of
  them are; confirming it by hand confirms the unchecked ones too, as `Source: Manual` — in `.specs/` and
  in any open change's copy.

## Criteria a contract delegates
A contract owns no code, so a feature criterion that implements one of its criteria names it in its own
body: `(contract AC-2)`, or `` (`contract.other-thing` AC-2) `` when the spec relates to several
contracts. Its Intent names the contract.

## Contracts
Only for work spanning several modules: `.agents/profiles/specs/templates/spec-contract.md`, `owns: []`, the full
criteria at product level. Like a feature, it has an Intent; it adds `## Source` — where it came from: a ticket link, kept in step by hand
when the ticket changes, or "Originated here" — and `## Implementation`, a table of each feature spec and
module taking part and its role; which criteria each carries is named only in the feature criteria. A module in the Implementation table needn't be the
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
