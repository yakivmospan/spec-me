---
id: tech
title: Tech context
status: merged
parent: product
owns: []
related: [architecture]
updated: {{DATE}}
---

# Tech context

| | |
|---|---|
| Primary language | {{LANGUAGE}} |
| Runtime | {{RUNTIME}} |
| Framework | {{FRAMEWORK}} |
| Build tool | {{BUILD_TOOL}} |
| Storage | {{STORAGE}} |
| Network | {{NETWORK}} |

## Commands

| | |
|---|---|
| Build | `{{BUILD_COMMAND}}` |
| Test | see Testing's *Run with* |
| Lint | `{{LINT_COMMAND}}` |
| Format | `{{FORMATTER_COMMAND}}` |

## Testing
The fact, not the methodology — the stack's testing skills own how to write a test; this is only
what's configured. The `spec-test-writer` subagent reads this section for its framework and command.

| | |
|---|---|
| Test framework | {{TEST_FRAMEWORK — e.g. JUnit5 + kotlinx-coroutines-test + mockk, pytest, Vitest}} |
| Run with | `{{TEST_COMMAND}}` |
| Test files live at | {{TEST_LOCATION_CONVENTION}} |
| Naming convention | {{TEST_NAMING_CONVENTION — e.g. backtick-name Given/When/Then, `methodName_condition_expectedResult`}}. No criterion id in a test name: a test covering a criterion is listed under its `Verified:`. |

## Key libraries
{{LIBRARY — why it is here, and what it would cost to remove. Only load-bearing ones.}}

## Development setup
{{SETUP — what a new machine needs before the build works}}

## Technical constraints
{{CONSTRAINTS — min SDK, browser support, latency budget, offline requirements}}

## Development approach
{{APPROACH — TDD? trunk-based? release cadence?}}
