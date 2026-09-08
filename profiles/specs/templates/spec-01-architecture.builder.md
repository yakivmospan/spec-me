---
id: architecture
title: Architecture
status: merged
parent: product
owns:
  - "{{TOP_LEVEL_SOURCE_GLOB — e.g. src/**}}"
related: [tech]
updated: {{DATE}}
---

# Architecture

> This spec owns the source tree broadly. Feature specs own narrower globs and take precedence —
> most specific match wins.

## Shape
{{ARCHITECTURE_SUMMARY — one paragraph: layered? modular monolith? event-driven?}}

## Components
Each spec's `owns:` says which paths it owns. This table is the component map,
including the parts that have no spec yet.

| Component | Responsibility | Code |
|---|---|---|
| {{name}} | {{one line}} | `{{glob}}` |

## Boundaries
{{RULES — what may depend on what. State the direction of every allowed dependency.}}

## Cross-cutting concerns
{{logging, auth, error handling, config — where each lives and who owns it}}

## Decisions
<!-- Cross-cutting decisions only — ones no single feature spec's scope covers
     (*One owner per decision*). Same shape as anywhere else: no `Instead of` means nothing was
     decided, and `spec-rebuild-overviews` reports the entry (*What was rejected*). -->
- **{{the choice, as a fact}}**
  - **Instead of** {{the rejected alternative}}
