---
id: product
title: {{PROJECT_NAME}}
status: merged
parent: null
owns: []
related: [architecture, tech]
updated: {{DATE}}
---

# {{PROJECT_NAME}}

## Goal
{{PROJECT_GOAL — what this is, who it's for, and why it exists rather than using something that
  already exists. One or two paragraphs. This is the thing an agent should read first to
  understand what "done" looks like — don't split it across separate Problem/Purpose sections
  that just repeat each other.}}

## Users
{{TARGET_USERS — one line. "N/A, internal tooling" is a valid answer; don't pad this if there
  isn't a distinct user beyond the team building it.}}

## Non-goals
{{NON_GOALS — what this deliberately will not do or support, and why. This is what stops an
  agent from "helpfully" adding scope, so be concrete: "no multi-tenant support (single customer
  for now)" is useful, "keep it simple" is not.}}

## Glossary
{{DOMAIN_TERMS — one line each, and only terms that recur across specs while no single file
  defines them: a product noun, a team or system outside this repo, a named flow, an acronym in
  the codebase whose meaning isn't in the code. Not general programming or platform vocabulary,
  which is assumed. Where a term is used but nobody has recorded what it stands for, say that
  outright instead of guessing — an inferred expansion is worse than an admitted gap, because the
  next reader can't tell which it was. Delete this heading if the project has no such terms.}}
