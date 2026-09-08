<!--
  An ARCHITECTURE.md — the docs-readme skill's structure. Required: Structure, Invariants. Keep the
  section order; delete any other section with nothing real under it. At the repository root only where
  nothing else — a spec, a design doc — already describes the architecture.
-->

# {{MODULE}} — architecture

Read before changing {{this module}}.

## Structure

{{The parts and how they depend on each other, one line each. A Mermaid diagram where it's clearer.}}

## Invariants

- **{{what must stay true}}** — {{why, and what breaks if it doesn't}}

## Concurrency and lifecycle

{{Threads and scopes, and what is created and torn down when.}}

## Decisions

{{A pointer to where the repository records its decisions. Where it records none: each choice, and
what it was chosen instead of.}}
