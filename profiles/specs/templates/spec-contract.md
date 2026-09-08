---
id: contract.{{SLUG}}
title: {{CONTRACT_NAME}}
status: draft
parent: architecture
owns: []
ticket: {{TICKET_KEY — or delete this line if there isn't one}}
related: []
---

<!--
  Only for work that fans out across multiple modules. Single-module work is a feature spec
  (`spec-feature.md`) — this tier buys nothing there. Contract mechanics (`owns: []`, the
  Implementation table, when a feature gets its own file) are in spec-format-rules' *Contracts*; prose rules are in
  `spec-style-rules.md`. Neither is repeated here.

  Delete any heading you have nothing real for (*Every chapter earns its place*), and every comment
  once the spec is written.
-->

# {{CONTRACT_NAME}}

## Change
{{Why this spec is being written or changed, in a sentence or two.}}

## Intent
{{One paragraph: what the flow guarantees across modules. Not how.}}

## Source
{{Where this came from — spec-format-rules' *Contracts*.}}

## Acceptance criteria

<!-- Shape and own proof: spec-format-rules' *Acceptance criteria* and *How a criterion was confirmed*;
     feature specs name these: *Criteria a contract delegates*. -->

- [ ] **AC-1: {{descriptive name}}**
  - **Given** {{precondition}}
  - **When** {{trigger}}
  - **Then** {{observable outcome}}
  - **Verified:**
    - **Source:** Manual
      - {{who, where — delete this source when nobody has confirmed it by hand}}

## Implementation

<!-- spec-format-rules' *Contracts*. -->

| Feature spec | Module | Role |
|---|---|---|
| `feature.{{slug}}` | new: `{{path}}` | {{what it does for this contract}} |
| `feature.{{slug}}` | existing: `{{path}}` | {{what it does for this contract}} |

## Decisions
<!-- spec-style-rules' *One owner per decision* and *What was rejected*. -->
- **{{the choice, as a fact}}**
  - **Instead of** {{the rejected alternative}}

## Open questions
<!-- Where a question goes: spec-change-rules' *The folder*; format: spec-style-rules' *Question and action*. -->
- [ ] **{{question}}**
  - **Action:** {{what resolves it, and who decides}}
