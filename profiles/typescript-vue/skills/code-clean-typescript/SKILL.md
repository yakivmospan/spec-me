---
name: code-clean-typescript
description: Use after changing any TypeScript or Vue file and before reporting code work done, including as a step inside a larger task — a ticket, a feature, a bug fix. Also on a TypeScript sketch in chat, and on "clean this up", "clean up this branch", "refactor", "simplify", "review this code", "make it idiomatic", "dead code". Keeps TypeScript clean, simple and idiomatic — in `.ts` files and `.vue` components — and sweeps what a change left behind. Not for a merge request review, code comments, READMEs, what a test covers, component structure or accessibility (vue-create), or formatting the tools own.
---

# Code Clean — TypeScript

## Non-negotiables

- **The project's rules and the surrounding file come first — read what `AGENTS.md` loads for this work, if you haven't.**
- **Follow Clean Code principles** — intention-revealing names, small single-purpose functions, no
  duplication. A name that needs a comment beside it to say what it means is the wrong name: rename it
  and delete the comment. Duplication: a condition written in more than one place —
  `order.status === 'paid' && !order.refunded` — becomes one named function, `isSettled(order)`, or one
  `computed` in a component; the same value derived in a template and again in the script is one
  `computed` used by both.
- **Reads like a book** — top-down by the step-down rule: exported entry points first, each function
  followed by the ones it calls, each at one level of abstraction. In a `<script setup>`: props and
  emits, then state, then derived values, then handlers, then lifecycle. The same holds for folders: a
  glance at one shows what it offers — its public surface at the top (an `index.ts` where the project
  uses them), details in a sub-folder named for what they are, never `utils`, `helpers` or `misc`.
- **TypeScript idioms, not Java or old-JavaScript habits** — only what the project's TypeScript version
  and `target` support: `const` by default, never `var`; `async`/`await` over `.then` chains; optional
  chaining and `??` over hand-written guards; a plain object or function over a class holding no state;
  `satisfies` to check a literal without widening it.
- **Types tell the truth** — no `any`: take `unknown` and narrow it. No `as` to silence the checker and
  no non-null `!` where a check belongs: narrow with a condition or a type guard. A type is imported with
  `import type`. A function's parameters are its real inputs — never an options bag of which every call
  passes the same two keys.
- **Flat callbacks** — a callback (`map`, `filter`, `then`, a `watch` or event handler) holds one
  expression; a branch or several statements inside one move to a named function, so a chain reads one
  step per line. An arrow function whose whole body is one expression has an expression body —
  `(item) => item.id` — not `{ return item.id }`. A template handler calls one function —
  `@click="select(item)"` — never inline logic.
- **Flat control flow** — one level of branching per function: an `if` or `switch` inside another branch
  or a loop moves to a named function; a boolean parameter that picks between behaviours becomes two
  named functions; guard clauses return early at the top, never from deep inside a block.
- **Closed sets are unions** — a fixed set of cases that code branches on is a union of string literals,
  or a discriminated union with a `kind` field, handled by an exhaustive `switch` whose `default`
  assigns to `never` — never a `default` that quietly absorbs a new case, and never an `enum` mirrored
  beside a union. A return whose meaning needs its doc comment — a `boolean` that doesn't mean success,
  an `undefined` standing for two outcomes — is such a set: name each outcome.
- **KISS** — the simplest code that meets the requirement; nothing for a hypothetical.
- **Robust** — every promise is awaited, returned or deliberately handled — never left floating; no empty
  `catch`; an async result that arrives after its component is gone is ignored or aborted.
- **Reactivity** — work lives as long as its owner: a listener, timer or subscription a component or
  composable starts is stopped in `onScopeDispose` or `onUnmounted`. A derived value is a `computed`,
  never a `watch` that writes a `ref`. Reactive objects are not destructured into plain values
  (`toRefs` keeps them live). Nothing slow runs on the main thread in response to input.
- **Wired, not hardcoded** — a value that differs by environment comes from the build's environment
  (`import.meta.env` on Vite) or a parameter, never a literal in the module. State at module level is
  shared by the whole app — keep it only where that is the point.
- **Complete** — nothing the change orphaned or made untrue stays: an import, an export, a file, a prop,
  an emit, a template ref, a style.

## Steps

1. **Check what is being reviewed.** When the request could mean reviewing a merge request rather
   than cleaning up code, stop and ask which: a review is a different job with a different skill
   behind it. A branch diff to clean up is this skill's.
2. **Write or review** against the non-negotiables.
3. **Leftovers sweep** — from the repository root, run `python3 <this skill's folder>/scripts/stale_refs.py`
   (with `--base <commit>` when part of the change is already committed; `--all` for the whole
   repository) and fix what it lists — removed names still mentioned, imports of nothing, exports and
   files nothing imports, unused scoped styles. Each hit is a lead: confirm it before deleting. Then,
   where the project has `eslint-plugin-vue`, run ESLint on the changed `.vue` files with the unused-
   declaration rules switched on for that run only, never in the config:
   `npx eslint --no-cache --rule '{"vue/no-unused-properties":["warn",{"groups":["props"]}],"vue/no-unused-emit-declarations":"warn","vue/no-unused-refs":"warn"}' <files>`
   — and remove each unused prop, emit and template ref, with its callers.
4. **Run the type check, the linters and the tests** covering the change, by the script names in
   `package.json`. A lint script that fixes files rewrites them — read its diff before reporting.

**Reviewing:** one line per finding — `**defect|risk|clarity** — file:line — what's wrong. Fix: …` —
by severity, then position. Asked only to review, stop there.

## Report

What changed or the findings, the sweep result (the script and the ESLint run), the type-check, lint
and test results.
