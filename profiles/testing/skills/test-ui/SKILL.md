---
name: test-ui
description: Use when asked to add, write or improve UI tests for screens, components or composables, verify UI state rendering, test user interactions, or test navigation triggered from the UI — writes tests that mount the screen with its state holder mocked, assert what renders and verify the events it receives. Not for ViewModel or store logic, or tests that name no kind for a class with no UI (test-unit), repository tests (test-unit, test-integration), or a journey across real apps on a device (test-e2e).
---

# Test UI

## Overview

UI tests verify that the **rendered UI matches expected state** and that **user interactions reach the state holder**. They complement state holder unit tests — those own business logic, UI tests own rendering contracts and event wiring.

Where a screen exposes two entries (overloads in Compose):
- **Public** — gets its state holder (a ViewModel, store or observable object) from dependency injection or the framework's plugin, used in production and in **all tests**
- **Private** — takes state and callbacks directly, used only for Previews

A screen with one entry, such as a Vue page, is mounted as it is.

Always test the **public entry**. The state holder is mocked through dependency injection or the plugin, so state is fully controlled. This means every assertion proves both that the UI renders correctly **and** that the value genuinely came from the state holder.

**The project's rules and the surrounding file come first — read what `AGENTS.md` loads for this work, if you haven't.**

---

## Key Principles & Structure Rules

| Rule | Detail |
|------|--------|
| **Cover all code paths** | Happy path, error conditions, and edge cases |
| **Always test the public entry** | Mount the screen's public entry with no arguments — dependency injection, or the framework's plugin, provides the mocked state holder |
| **Always mock the state holder** | Use the project's mocking library — one that returns defaults for calls not set up, where it has that — never a real state holder with real repositories |
| **Verify events on the state holder** | Verify the call on the mock — not an emitted events list |
| **Verify no-op interactions** | For interactions that must NOT fire an event (e.g. clicking an already-active element), verify the call never happened |
| **State assertions prove state holder wiring** | Because state comes from the mocked state holder, a passing assertion proves the wire is connected |
| **Prefer semantic finders** | Find by visible text or accessibility label before resorting to a test id |
| **Add test ids sparingly** | Only add a test id to ambiguous elements; mark it test-only where the language allows |
| **Scroll before asserting off-screen nodes** | For nodes that may be below the fold in a scrollable screen rendered with real layout — not a DOM without layout, such as jsdom — scroll the node into view and wait for the UI to settle before asserting visibility or enabled state. Asserting absence does not require scrolling where the framework checks the whole tree |
| **Querying nodes with the same text** | The single-node finder is the default — use it when the text is unique in the tree. Where it fails on text that appears more than once, that itself catches unintended duplicates; where it quietly returns the first match, as Vue Test Utils' `find` does, also check that exactly one node matches. Switch to the all-nodes finder only when the text is known to appear multiple times. **Take the first match only when you intentionally target a single node and the assertion is valid for any one instance** (e.g. a node that is unique in the tree). When a label is known to appear more than once, always assert **all** instances by iterating with index — this applies to every operation including visibility, enabled state, clicks, and scrolls. Taking the first and ignoring the rest is incorrect and gives false confidence regardless of the assertion type. To assert ALL instances are absent, assert the all-nodes finder returns none. For the index iteration pattern, define a reusable `assertAllNodesWithText` helper in the test file (see Template). |
| **One assertion per concept** | Each test verifies one logical UI contract |
| **Table tests** | Use when the same assertion must hold across multiple inputs. Two patterns are valid — choose based on diagnostic value: **(A) Individual test functions + private helper** — when each input is a semantically distinct state (e.g. `Loading`, `Error`) and a failing test name alone should identify the problem. **(B) Single test with a `for` loop** — when inputs are a flat homogeneous list (e.g. all field labels, all field values) and the assertion is structurally identical for each item; the item value itself provides sufficient failure diagnostics. Never use Pattern B when inputs produce structurally different assertions. |
| **Avoid code duplication** | Extract repetitive test logic into private helper functions. Examples: common setup for multiple test scenarios, repeated mock configurations, or shared assertion logic. Helper functions should have clear names and documentation. Always prefer DRY (Don't Repeat Yourself) — if the same setup or assertion sequence appears in 3+ tests, create a helper function. |
| **Given/When/Then comments** | In every test body |
| **When/then naming** | No camelCase — say the condition and the expected result in words, in the form the language allows (backticks in Kotlin, a string in JavaScript); keep them concise |
| **Ask before assuming** | If the screen's contract introduces a pattern, interaction, or UI structure not covered by this skill, ask for clarification before writing tests. Wrong tests that pass are worse than no tests |

---

## What to Test (Focus Areas)

**State rendering** — each state variant renders the correct content. Cover every distinct state and every distinct data condition that produces a different rendered output:
- Loading → spinner visible, content not visible
- Loaded (empty) → empty state message visible, list not visible
- Loaded (with data) → items visible with correct labels and values
- Error → error title visible, error cause surfaced in the UI
- Selection state → when a UI element can be active/inactive (e.g. a selected tab, a toggled chip), assert selected / not selected — not just visibility

**Extra state holder properties** — one test per property proving the UI effect is driven by the state holder's value, not hardcoded. Cover every property that independently affects the UI:
- Non-empty value → UI reacts (e.g. certain elements hidden, others appear)
- Empty/default value → UI shows its default shape

**Conditional visibility** — elements that appear, disappear, or change enabled state based on current state or state holder properties. Cover every element whose presence or enabled state is conditional:
- Enabled/disabled correctly per state
- Visible/hidden correctly per state or extra state holder property combination
- Where multiple states produce the same assertion, use the table test pattern to avoid duplication

**User interactions** — verify the state holder received the correct event, or the correct call where it takes calls (a store's `openDetail(id)` rather than an `OpenDetail(id)` event). Cover every interactive element with at least a positive case, and a negative case where the interaction should be a no-op:
- Item click → the state holder receives `OpenDetail(id)`
- Button click → the state holder receives `ExpectedEvent`
- Text input → the state holder receives `SearchQueryChanged(query)`
- No-op interaction → when an action should have no effect (e.g. re-selecting the already-active element), verify the event was never fired

**On open** — what the screen asks the state holder for by itself when it opens, such as a fetch: assert it was called exactly once. When a button makes the same call, such as Retry, the call made on open is already on the mock: clear the mock's calls after the screen opens, or expect two calls in total after the click. A plain "was called" check would pass even with Retry wired to nothing.

**Empty states** — distinct messages for semantically different empty conditions (e.g. "no data exists" vs "no data matches current filter"). Each distinct empty condition should have its own test.

---

## What NOT to Test in UI Tests

- State holder business logic (belongs in its unit tests)
- Repository data transformation (belongs in repository/interactor tests)
- Navigation stack correctness end-to-end (belongs in integration tests)
- Exact pixel layout or colors (fragile; prefer screenshot tests if needed)

---

## Templates

One section per platform in `reference.md` — Compose (Kotlin) today — with its tech stack, how the
rules above look there, and a template. No section for this project's platform: write the tests in the
idiom of its existing UI tests and libraries, never guessing a library's API, and offer to add the
section.
