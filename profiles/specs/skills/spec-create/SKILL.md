---
name: spec-create
description: Use when asked to "spec out X", "spec this out", "start PROJ-1234 as a planned change", "what should X do", "create a spec from code", "bring the spec up to date with the code", or when spec-plan needs a change opened — opens a planned change under .specs/changes/ and agrees its requirements with the user, or writes a spec from existing code, or corrects a stale one, in place. Not for everyday building and tweaking, which edits specs in place; designing or building a change (spec-plan); or folding one in (spec-merge).
---

# Spec Create

Two jobs. **A planned change** — the user asked to plan or spec work ahead of code (spec-builder-rules'
*Two ways to work*): open its plan and agree its Requirements — why, and what must hold once it's built.
**A spec from code** — code that exists with no spec or a stale one: write the spec in place in
`.specs/`. Specs never move into a change.

## Non-negotiables

- **Ask what nobody has written down, before writing** — only what matters, the most important
  first, each one line with your inference beside it, at most three at a time: typically who consumes
  it and what breaks if it's wrong, the failure path, what isn't this change's job, what proves it
  done. Skip what a spec, ticket or the code already answers.
- **Never fill a gap with a plausible default.** Every unanswered question, and every assumption made to
  keep going, is an Open question with an Action.
- **Every requirement and Behaviour line states a guarantee, not implementation** — no tunables,
  internal names or call sites — and the failure path has a line.
- **From code, the code is ground truth.** Write what it does, as a Behaviour line or a Pitfall. Never
  loosen a rule it no longer honours, or delete what it stopped doing, on your own — ask whether that
  was on purpose.
- **A Decision names what it rejected; a request that would re-decide one is raised as exactly that.**
- **Only the user approves, in chat** — a plan's `status: approved`, or a spec written from code.

## 1. Find the starting point

Find the area by the `owns` globs (`.specs/INDEX.md` lists them), under other names too, and look at
the code under it.

| What you find | Starting point |
|---|---|
| Work ahead of code — new, or changing what a spec says | **A planned change** |
| The code already does it, and no spec covers it, or its spec is stale | **From code** |

- **"Update the spec", direction unclear** — spec-change-rules' *Which direction*.
- **A plan for this branch or ticket already under `.specs/changes/`** — continue it when it's the same
  work; different work gets its own folder, `<branch>-<topic>`.
- **Unscoped** ("the specs are stale") — ask which area. A tree-wide sweep needs its own go-ahead.
- **Not a feature at all** — code callers merely borrow — gets no spec (spec-format-rules' *What counts
  as a feature*); say so and stop.

Read, if not already read this session, `.agents/profiles/specs/rules/on-demand/spec-change-rules.md`, `spec-format-rules.md` and
`spec-style-rules.md`; `.specs/00-product.md`'s Non-goals — work that contradicts one is a red flag
to raise; and every spec the work touches, whole.

## 2. A planned change

1. **Check the specs it touches against their code.** One with commits to its `owns` code after its
   `updated:`: offer `spec-sync-with-code` once, in one line, and keep going.
2. **Module split.** Work that plausibly spans modules, or where which module owns what is itself a
   question, goes through `spec-plan`'s grounding first. Work that does span modules gets a contract
   spec, named among the specs it touches.
3. **Create the folder** and copy `.agents/profiles/specs/templates/implementation-plan.md` into it,
   named per spec-change-rules' *The folder*.
4. **Elicit**, per the non-negotiables. Handed requirements (a ticket, a document): restate them as
   plain lines by topic, and show what you changed or left out.
5. **Write Requirements**, per spec-change-rules' *The plan*.
6. **Then:** continue in `spec-plan` for Design and Tasks; the OK comes once, on the whole plan.

## 3. From code

- **Gather** the code and its tests. For a stale spec: the spec whole, and what changed since its
  `updated:` (`git log` on its `owns`).
- **Ask only what the code can't answer** — usually intent, the consumer and what's out of scope.
- **A stub is not behaviour.** A hardcoded return or a `// later` comment is an Open question.
- **Scope `owns` to what you describe**, its tests included — narrow, real coverage beats a wide glob.
- **A Decision only where the user can name what was rejected** — the code rarely shows it, so ask.
- **Write it in place**, from `spec-feature.md` or `spec-contract.md` for a new one, then show it and
  ask once; a no leaves `.specs/` as it was. A stale spec corrected gets a Change history row and
  `updated:`.

## Report

Run `spec-rebuild-overviews`. In plain words (spec-change-rules' *Talking to the user*): what will be
true, what's still open and what each open question blocks, and what you're waiting for.
