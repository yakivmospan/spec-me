---
name: test-unit
description: Use when writing unit tests, or tests that name no kind, for ViewModels, view models, repositories, interactors, or other business-logic classes — testing coroutine flows, state emissions, error handling, or mocking dependencies with mockk, Mockito or any other mocking library. Ready templates for JUnit4 and JUnit5 are in reference.md; check what this project configures first. Not for tests asked to run several real components together or to replace mocks with fakes, or UI rendering tests.
---

# Test Unit

## Overview

Unit tests verify individual functions and methods in isolation. Each test covers one logical concept — happy path, error condition, or edge case — with all external dependencies mocked.

**The project's rules and the surrounding file come first — read what `AGENTS.md` loads for this work, if you haven't.**

---

## Key Principles & Structure Rules

| Rule | Detail |
|------|--------|
| **Test in isolation** | Mock all external dependencies — databases, APIs, file systems |
| **Cover all code paths** | Happy path, error conditions, and edge cases |
| **Full output assertion** | Verify the complete output object, not individual fields. For example, the full UiState, the full domain model, or the complete result wrapper |
| **One assertion per concept** | Each `@Test` verifies one logical contract |
| **Table tests** | Use when the same assertion must hold across multiple inputs. Two patterns are valid — choose based on diagnostic value: **(A) Individual `@Test` functions + private helper** — when each input is a semantically distinct case (e.g. different exception types, different error states) and a failing test name alone should identify the problem. **(B) Single `@Test` with a `for` loop** — when inputs are a flat homogeneous list (e.g. a set of invalid values, a set of equivalent keys) and the assertion is structurally identical for each item; the item value itself provides sufficient failure diagnostics. Never use Pattern B when inputs produce structurally different assertions. |
| **Avoid code duplication** | Extract repetitive test logic into private helper functions. Examples: common setup for multiple test scenarios, repeated mock configurations, or shared assertion logic. Helper functions should have clear names. Always prefer DRY (Don't Repeat Yourself) — if the same setup or assertion sequence appears in 3+ tests, create a helper function. |
| **No reflection** | There must be a public API that drives the state being tested |
| **No deprecated classes** | Unless absolutely necessary |
| **No matchers on real objects** | Use full object comparison instead |
| **`@VisibleForTesting`** | If private implementation is needed for testing, propose making it `internal` |
| **Given/When/Then comments** | In every test body |
| **When/then naming** | No camelCase. Say the condition and the expected result in words, in whatever form the language allows — backticks in Kotlin, underscores elsewhere. Keep them concise |
| **Full API surface coverage** | For classes with multiple public entry points that share underlying logic (e.g. `execute()` and `executionFlow()`), every behaviour — happy path, error, edge case — must be verified through each public entry point explicitly |
| **Orchestration, not just invocation** | When a method coordinates multiple dependencies, verify it as a whole: call order (`coVerifyOrder`), *actual* data flowing between calls (not `any()`), full state-transition sequence (not just the end value), all side effects of one call asserted together in one test, and one test per failure source showing *that* failure surfaces correctly |

---

## What to Test

**Happy path** — correct output for valid inputs and successful dependencies

**Error conditions** — network failures, timeouts, unavailable resources, error propagation

**Edge cases** — empty inputs, null values, boundary conditions, concurrent access

**Orchestration** — ordering, data handoff, state transitions, multi-effect completion, and per-failure-point attribution for methods that coordinate multiple dependencies

**Scope and cancellation** — For classes that accept a `CoroutineScope`, always test: caller cancellation does not affect execution on the provided scope; app scope cancellation stops execution; callbacks and side effects still run to completion when the caller cancels; internal state is consistent after cancellation

**System behavior** — Consider how the class behaves as a component in a larger system, not just in isolation. Ask: what happens under concurrent access from multiple callers? What happens when the environment it depends on (scope, lifecycle, external state) changes or is torn down? What guarantees does it make to its collaborators when things go wrong?
## Templates

Concrete templates live in `reference.md` — a full test class for each of JUnit4 and JUnit5, with
the coroutine, flow and mocking setup spelled out. They are written in Kotlin because that is where
they came from; the shape they show is the shape any framework's version takes. Open them when you
want something to copy, and translate the annotations to what this project actually runs.

Everything above is what decides whether the test is any good, and none of it changes with the
language.

