---
id: feature.{{SLUG}}
title: {{FEATURE_NAME}}
status: draft
parent: architecture
owns:
  - "{{CODE_GLOB}}"
  - "{{TEST_GLOB — the module's own tests, where they don't already fall under the line above}}"
ticket: {{TICKET_KEY — e.g. PROJ-1234, or delete this line if there isn't one}}
related: []
---

<!--
  A skeleton, not a checklist: delete every heading you have nothing real to put under
  (spec-style-rules' *Every chapter earns its place*). The rules live in
  `.agents/profiles/specs/rules/on-demand/spec-format-rules.md` (what each section must contain) and
  `spec-style-rules.md` (how to phrase it) — read both before writing. They are not repeated here,
  because a copied template drifts from the rules the moment either changes.

  When Change history, Pitfalls and References are added: spec-format-rules and spec-style-rules.
  Delete every comment once the spec is written: a spec reads without this setup.
-->

# {{FEATURE_NAME}}

## Change
{{Why this spec is being written or changed, in a sentence or two.}}

## Intent
{{One paragraph: what this feature guarantees to the rest of the system. Not how. When it carries part of a contract, name the contract here.}}

## Acceptance criteria

<!-- Shape and proof: spec-format-rules' *Acceptance criteria* and *How a criterion was confirmed*;
     wording: spec-style-rules' *Guarantee, not implementation*. -->

- [ ] **AC-1: {{descriptive name}}**
  - **Given** {{the state before the trigger}}
  - **When** {{a single, specific action}}
  - **Then** {{observable outcome}} {{(contract AC-N), if it implements a contract criterion}}
  - **And** {{additional outcome, if there is one}}
  - **Verified:**
    - **Source:** `{{TestFile.kt — delete this source when no test proves it}}`
      - `{{test function name, exactly as declared}}`
    - **Source:** Manual
      - {{who, where, which build — optional; delete this source when there's no manual proof}}

## Constraints
<!-- spec-style-rules' *Obligation, not description*; a dependency edge is `01-architecture.md`'s Boundaries. -->
- **{{the obligation, as an imperative}}** — {{why, only when it isn't obvious}}
  - **Currently violated:** {{what breaks it today, and where that's tracked}}

## Public surface
<!-- Only what visibility modifiers can't state (*Point, don't repeat*, `Public surface`). -->
- **{{audience}}** — {{what it may use, as a rule rather than a list}}

## Decisions
<!-- spec-style-rules' *What was rejected*, *One owner per decision*, *Revising, not replacing*. -->
- **{{the choice, as a fact}}**
  - **Instead of** {{the rejected alternative}}
  - **Because** {{one clause, only if naming the alternative doesn't already explain it}}
  - **Revisit when** {{the condition that would reopen this}}

## Open questions
<!-- spec-style-rules' *Question and action*. -->
- [ ] **{{question}}**
  - **Action:** {{what resolves it, and who decides}}
