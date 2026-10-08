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

## Behaviour

<!-- Shape: spec-format-rules' *Behaviour*; wording: spec-style-rules' *Guarantee, not implementation*. -->

- {{a rule the code follows on purpose, in one sentence}}
- {{a rule the code breaks today}}
  - **Currently violated:** {{what breaks it, and where that's tracked — delete when nothing does}}

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

## Future plans
<!-- spec-format-rules' *Future plans*. -->
- **{{the plan, as what it does}}**
  - **Why:** {{what it gives — delete when the title says it}}
  - **Not yet because:** {{delete when there's no reason beyond "not now"}}
  - **Take up when:** {{the condition — delete when unknown}}
