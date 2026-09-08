---
name: docs-readme
description: Use when asked to "write a README", "document this module", "update the README", or when writing, reviewing or updating a README or an ARCHITECTURE.md — the repository root, a module, a tool or script folder — including any change that renames a command, path or public entry point one names. Enforces KISS and one structure per kind of file. Not for in-code comments, specs, or a README that documents a spec or agent-setup process.
---

# Docs README

A README answers one reader's first questions, in the order they ask them, then gets out of the way.
It isn't a spec, an API reference or a changelog — it points at those.

**The project's rules and the surrounding file come first — read what `AGENTS.md` loads for this work, if you haven't.**

## One file, one reader

| File | Reader | Template |
|---|---|---|
| Root `README.md` | someone new to the repository | `templates/README-root.md` |
| A module's or tool's `README.md` | someone using it from outside | `templates/README-module.md` |
| A module's `ARCHITECTURE.md` | someone changing it | `templates/ARCHITECTURE.md` |
| A module's `RELEASING.md` | whoever releases it — team-internal, never a consumer | `templates/RELEASING.md` |

- A folder gets a README only when it has an outside reader or a setup step.
- **No root `ARCHITECTURE.md` where the repository already describes its architecture** — a spec, a
  design doc. The root README points there. Where nothing does, the root `ARCHITECTURE.md` uses the
  same template, for the whole repository.
- A module's `ARCHITECTURE.md` covers that module's internals only. How modules relate to each other
  belongs at the root.
- A module gets a `RELEASING.md` only when it publishes something outside the repository and doing so
  takes more than "merge to main" — a tag pattern, a version rule, a manual override worth writing
  down. Its content is team process, never copied into or named from the README: a consumer of the
  module never sees it.
- Requirements and decisions belong in the repository's specs, where it has them. A README or an
  `ARCHITECTURE.md` points at them and never restates them.

## Structure

Copy the template beside this file, never write from memory. Its section names and order are fixed.
Required sections stay; any other section with nothing real under it is deleted, never left as a
stub. An existing file moves to the structure the first time a change touches it — never in a sweep.

## Rules, in priority order

1. **Lead with what it is and why you'd use it** — one or two sentences. No "Welcome", no history.
2. **Every command runs as written** — copy-pasteable, from the directory it names, and checked
   against the repository: the task, the path, the flag. Never from memory.
3. **Point, don't copy.** An API list belongs in the code's docs, a version in the build file,
   requirements in the specs. Name the entry point, and what's there.
4. **Don't state what's already obvious from context** — a file's own name or location already says
   it's internal, or a step; the syntax just shown already says a value is "just another version to
   paste." Adding a sentence confirming what the reader can already see is the same filler as an
   adjective, just longer.
5. **Say what readers get wrong** — the symptom they'd see, its cause, the fix. The code can't tell
   them that, which is what makes a README worth reading.
6. **One example, the smallest that works.** More only for genuinely different ways to use it, each
   shown once.
7. **Nothing that goes stale on its own** — no version numbers, dates, counts or "currently" that live
   somewhere else. Point at where they're kept.
8. **No ceremony** — no badges, table of contents, empty License or Contributing sections, or
   headings for their own sake. A table only where prose would scan worse.
9. **One fact per line in a dense step** — a list item carrying several facts becomes sub-bullets,
   one each, labelled with what that fact is: `- **Region:** …`. A paragraph inside a list item is the
   sign to split it. An item with one fact stays one line; a short lead-in after the item's label is
   fine when it holds for every sub-bullet.
10. **Plain words, no filler** — everyday words over formal ones: "made before", not "predates"; "use",
    not "leverage". "Simply", "just", "easy", "powerful", "seamless": delete on sight.

## Keeping it true

**A README follows its sources, never the other way.** The code, the build, the specs, a skill or a
rule defines a thing; the README describes it. A change goes into the source first, then the README
catches up — and a README already saying something never makes its source redundant.

A change that renames a command, a task, a path or a public entry point updates every README and
`ARCHITECTURE.md` that names it, in the same change. On review, check each command and path against
the repository before judging the prose.

## The delete test

Before finalizing any line: *if I deleted this, would its reader lose something they need, and
couldn't get faster from the code?* If no — delete it.

## Examples

Bad (opening water):
> Welcome to the Payments SDK! A powerful, easy-to-use library that provides a seamless way to
> interact with the payments service.

Good:
> Kotlin client for the payments service. Wraps its HTTP API in suspend calls, and retries idempotent
> requests without the caller managing it.

Bad (copying the API, which drifts from the code):
> ### Methods
> - `charge()` — charges a card
> - `refund()` — refunds a payment

Good:
> `PaymentsClient` is the entry point; its doc comments state each call's contract.

Bad (a command from memory):
> Run `./gradlew test` to run the tests.

Good (checked against the build):
> `./gradlew :payments-client:testDebugUnitTest` — the module's own unit tests.

Bad (a step as a paragraph):
> 1. **Install** — add the dependency to the app module's build file, sync, then add the `INTERNET`
>    permission to the manifest, since the client fails silently without it.

Good:
> 1. **Install**
>    - **Dependency:** add it to the app module's build file, then sync.
>    - **Permission:** `INTERNET` in the manifest — without it the client fails silently.

Good (what a reader would get wrong):
> Adding only `payments-client` compiles but fails at runtime: it needs `payments-model` on the
> classpath too.

Bad (`RELEASING.md`, restating what its own name and the line above already say):
> Team-internal — not part of what ships to a consumer; see `README.md`'s Dependency section for that.
>
> A snapshot build is consumed the same way as a release, just at a different version.

Good:
> Push a tag `payments-client-v<version>` …
