---
name: code-clean-kotlin
description: Use after changing any Kotlin file and before reporting code work done, including as a step inside a larger task — a ticket, a feature, a bug fix. Also on a Kotlin sketch in chat, and on "clean this up", "clean up this branch", "refactor", "simplify", "review this code", "make it idiomatic", "this looks like Java". Keeps Kotlin clean, simple and idiomatic, and sweeps what a change left behind. Not for a merge request review, code comments or KDoc, READMEs, what a test covers, Compose UI structure, choosing between designs, or formatting ktlint and detekt own.
---

# Code Clean — Kotlin

## Non-negotiables

- **The project's rules and the surrounding file come first — read what `AGENTS.md` loads for this work, if you haven't.**
- **Follow Clean Code principles** — intention-revealing names, small single-purpose functions, no
  duplication. A name that needs a comment beside it to say what it means is the wrong name: rename it
  and delete the comment. Duplication: a condition written in more than one place — `state == ServiceState.READY` — becomes one
  named extension, `val ServiceState.isReady`; one computed from a flow's current values and again from
  its emissions — `state.value.isReady && …` beside `combine(state, …) { s, … -> s.isReady && … }` — becomes
  one function taking the values, called from both.
- **Reads like a book** — top-down by the step-down rule: public entry points first, each function
  followed by the ones it calls, each at one level of abstraction, so a reader goes from what happens to
  how without jumping around. The same holds for packages: a glance at one shows what it offers — entry
  points and their data at the top, details in a sub-package named for what they are (never `impl`,
  `utils`, `helpers`); a sub-package holds several related files, not one or two.
- **Follow Kotlin idioms, not Java habits** — only what the project's Kotlin version supports.
- **Flat lambdas** — a lambda holds one expression; a branch or several statements inside one (`collect`,
  `let`, `onSuccess`, …) move to a named private function, so a chain reads one step per line. Builder and
  DSL blocks — `apply`, a Koin `module`, Composable content, a test body — are exempt. An expression body
  ending in a multi-line trailing lambda starts on the signature line — `fun x(): T = call(a) { p ->` —
  rather than breaking after `=`. A function whose whole body is one expression — any call, with or without a
  trailing lambda, a `when`, or an `if`/`else` whose branches are single expressions — is an expression
  body, `fun x() = context.startActivity(…)` or `fun x() = when {`, not a block wrapping it, unless the
  expression's type is not the function's (a `Unit` function whose call returns a value, an assignment);
  a public one, or one the compiler cannot infer (recursion), declares its return type. A lambda that wraps others —
  `launch`, `init`, `collect` — holds one call on one line: a multi-line `when`, `if` or chain inside one
  moves to a named function, and a flow is collected with `onEach(::handler).launchIn(scope)`, never
  `scope.launch { flow.collect { } }`. A lambda that only negates its parameter is
  `{ !it }` — `dropWhile { !it }` — and a non-null `Boolean` is never compared with `== false`.
- **Flat control flow** — one level of branching per function: a `when` or `if` inside another branch or a
  loop moves to a named function; a Boolean parameter that picks between behaviours becomes two named
  functions, branched on once at the top; no `continue`, `break` or `return` from inside a nested block —
  "do it again" is a named function calling itself or its own loop.
- **Closed sets are sealed** — a fixed set of types that code branches on is a `sealed interface` with an
  exhaustive `when`, never an `else` branch or an enum mirrored beside it. Tests fake a sealed type with
  mockk, not a subclass. A return whose meaning needs its KDoc to be read — a `Boolean` that doesn't
  mean success, a `null` standing for two different outcomes — is one of these sets: name each outcome
  in a sealed result instead.
- **KISS** — the simplest code that meets the requirement; nothing for a hypothetical.
- **Robust** — every failure and state handled; coroutine cancellation never swallowed.
- **Android** — work lives as long as its owner; nothing slow on the main thread; the process can die
  any time.
- **Complete** — nothing the change orphaned or made untrue stays.

## Steps

1. **Check what is being reviewed.** When the request could mean reviewing a merge request rather
   than cleaning up code, stop and ask which: a review is a different job with a different skill
   behind it. A branch diff to clean up is this skill's.
2. **Write or review** against the non-negotiables.
3. **Leftovers sweep** — from the repository root, run `python3 <this skill's folder>/scripts/stale_refs.py`
   (with `--base <commit>` when part of the change is already committed) and fix what it lists; delete
   what the change left unused.
4. **Run the tests or build** covering the change.

**Reviewing:** one line per finding — `**defect|risk|clarity** — file:line — what's wrong. Fix: …` —
by severity, then position. Asked only to review, stop there.

## Report

What changed or the findings, the sweep result, the test result.
