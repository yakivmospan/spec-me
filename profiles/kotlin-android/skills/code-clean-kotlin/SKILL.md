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
- **Names** — three principles for every new name; the names beside each show a miss, not a list to
  match against:
  - **One idea, one word, the file's.** A new name takes the word the file or codebase already uses
    for that idea; a second word for the same idea is never added, and your own word is the last
    choice. Beside `verifyRequirements` and `verifySilently` the new one is `verifyWithoutLeavingReady`, not
    `recheck`; a sibling that already says `NotSupported` is not joined by `TooOld`. Poor words are
    improved where the task touches them, said out loud.
  - **What it does, for any reader and any caller.** Said in words someone new reads without opening
    it — `saveWithRetry`, not `saveBehindSaver`. A member of a shared class is named for every caller,
    not the first one. A dependency a class takes is named by what the class asks of it, in the class's
    own verb — `isConnectionAllowed`, not `isSuperEvaReady`: the assistant asks whether it may
    connect, and need not know who answers.
  - **Read once, read right.** No two names a letter apart for different things — `SyncReason` beside
    `SyncerReason` — and no name that reads as something else: `verifyWhileReady` reads as a loop.
- **What's there stays** — a change touches existing code only as far as it needs: a name, where it
  lives and its comments stay unless they are wrong, and "I'd have named it differently" is not wrong.
  Opening something to a new caller changes its visibility and nothing else: `private const val
  BILLING_PACKAGE` another module needs becomes `const val BILLING_PACKAGE`, not `BillingClient.PACKAGE`;
  a case `CardDeclined` that now also covers an expired card keeps its name, not renamed `NotPaid`: the
  reason it carries says which. A rename to fit a new case is asked for first, never made on the way.
- **One class, one job; reuse before adding** — a class gets no method of a different kind because a
  caller needs both answers. First find what already gives it — a use case, an extension, a flow — and
  use that: `UploadFilesUseCase` doesn't grow `isOnline()` when `NetworkStateUseCase` already hands
  out the state and `NetworkState.isOnline` reads it.
- **Reads like a book** — top-down by the step-down rule: public entry points first, each function
  followed by the ones it calls, each at one level of abstraction, so a reader goes from what happens to
  how without jumping around. The same holds for packages: a glance at one shows what it offers — entry
  points and their data at the top, details in a sub-package named for what they are (never `impl`,
  `utils`, `helpers`); a sub-package holds several related files, not one or two.
- **Follow Kotlin idioms, not Java habits** — only what the project's Kotlin version supports.
- **Flat lambdas** — a lambda holds one expression; a branch or several statements inside one (`collect`,
  `let`, `onSuccess`, …) move to a named private function, so a chain reads one step per line. A single
  guard — one `if` with no `else` and no braces, around one call — may stay:
  `Listener { v -> if (!isMocked) target.on(v) }`. Builder and
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
- **One channel per outcome** — a function reports an outcome through its return value or through a
  callback, never both: `suspend fun verify(onFailure: suspend () -> Unit): Boolean` says "failed"
  twice. A `suspend` function already waits, so it answers by returning; a callback is only for a step
  the caller must run at a moment it can't reach itself, and then returns nothing.
- **KISS** — the simplest code that meets the requirement; nothing for a hypothetical.
- **Robust** — every failure and state handled; coroutine cancellation never swallowed.
- **Android** — work lives as long as its owner; nothing slow on the main thread; the process can die
  any time.
- **Work starts in `init` only for an observer** — only when all four hold: the work is the object's
  whole purpose; it runs in a scope passed in, so cancelling that scope stops it and nothing is told
  "start" or "stop"; it is cheap and invisible — no I/O, network, binder call or throw, which start on
  demand instead; and it touches only state already set up — no `open` or `abstract` call, no `this`
  handed out, easiest in a `final` class. A test passes its own scope and calls `runCurrent()` after
  building it.
- **Wired, not hardcoded** — a dependency, or a value that differs by build type or environment, comes
  in through the constructor and is chosen where the object is wired (the DI module), never hardcoded.
  An object lives as long as what it holds: one keeping nothing between calls is a DI factory, and
  state that must be shared — a pool bounding calls to one app — is owned once and passed in, never
  rebuilt per class (example: `reference.md`).
- **Complete** — nothing the change orphaned or made untrue stays.

## Steps

1. **Check what is being reviewed.** When the request could mean reviewing a merge request rather
   than cleaning up code, stop and ask which: a review is a different job with a different skill
   behind it. A branch diff to clean up is this skill's.
2. **Vocabulary before naming** — before any new name, write down the word the file and its siblings
   already use for that idea, and who reads the member; the name takes that word. Done when the name
   holds no word of your own, or you said why.
3. **Write or review** against the non-negotiables.
4. **Leftovers sweep** — from the repository root, run `python3 <this skill's folder>/scripts/stale_refs.py`
   (with `--base <commit>` when part of the change is already committed) and fix what it lists; delete
   what the change left unused.
5. **A fresh reader before reporting** — a fresh agent, where the tool has them, reviews the diff's
   names and structure with this skill; fix what it finds. Without one, say so.
6. **Run the tests or build** covering the change.

**Reviewing:** one line per finding — `**defect|risk|clarity** — file:line — what's wrong. Fix: …` —
by severity, then position. Asked only to review, stop there.

## Report

What changed or the findings, the sweep result, the test result.
