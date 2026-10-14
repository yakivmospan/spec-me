---
name: spec-plan
description: Use when asked to "plan this", "design this", "how should we build X", "compare approaches", "ask the architect", "implement PROJ-1234", "build the change", "continue the plan", "the design changed", or once a change's requirements are agreed — writes a change's design and tasks with the user, builds from them task by task when asked, updating specs in place as each lands, and reshapes the plan any time. Not for agreeing a change's requirements or writing a spec from code (spec-create), or folding a change in (spec-merge).
---

# Spec Implementation Plan

A change is its `implementation-plan.md`: Requirements say why and what must hold, Design how, Tasks
in what order. This skill holds the plan's life — writing it with the user, building from it, reshaping
it. The specs follow the code as each task lands; the plan carries the work between sessions.

## Non-negotiables

- **Requirements agreed first.** No Design or Tasks until the user has said the Requirements are right —
  agreed in chat. Grounding reading alone may come earlier, when the module split is unclear.
- **The user decides what only they can weigh** — product behaviour, scope, cost, a Decision in the
  way — from at least two options in one table. Engineering calls arrive decided, each with its
  reason; the user can overturn any.
- **Build only when asked.** Writing the plan never starts building: stop and say it's ready.
- **A spec documents what's built, never what's planned** (spec-change-rules' *While building*).
- **Never settle an Open question on your own.** Build what isn't blocked, and ask in one line.
- **A checkpoint waits for the person.** A task whose check only a person can make is ticked only after
  they say it held.

## 1. Before anything

1. Read, if not already read this session, `.agents/profiles/specs/rules/on-demand/spec-change-rules.md`, `spec-format-rules.md`, `spec-style-rules.md` — and `spec-architecture-rules.md` before a real design choice —
   the plan, and each spec it touches.
2. A plan already there is where the work left off: continue it, never restart.
3. Pick the part:
   - **No change yet:** open one through `spec-create`.
   - **Sent by `spec-create` for the module split:** *Write the plan* step 1 only, report which module
     owns what, and hand back.
   - **Asked to build:** *Build*.
   - **Requirements agreed, no Design or Tasks yet:** *Write the plan*.
   - **Something learned or changed, or the user reshapes the plan:** *Reshape*.

## 2. Write the plan

With the user, a section at a time:

1. **Ground it.** Read the code the change touches, and bring findings the design must act on, not a
   tour. Wide reading goes to the `spec-architect` subagent with a bounded brief: which modules, what to
   find out, the paths of the rules the loaders place at proposing a design, which it doesn't load on
   its own, and a request for one decided design.
2. **Design.**
   - **The design:** each engineering call with its reason in a line; one obvious way is a sentence or
     two. Each option weighed and dropped is a `Not` line with why.
   - **A choice the user must weigh:** the options in one table, on concrete tradeoffs. The user picks;
     the winner goes into Design, each other option as a `Not` line with why.
   - **A big change** — a contract, several modules: sub-headings per spec-change-rules' *The plan*. A
     story's plan says which module change carries which of the contract's requirements.
   - **Calls between packages or layers:** each new or changed one as a signature, per
     spec-change-rules' *The plan*, so the user sees each class's job before any code.
   - **A requirement has to change:** back to Requirements, with the user, first.
3. **Check the design before the user sees it** — whoever wrote it, this session included. For every
   added class, object or function in What changes: open the existing piece it names, and the code
   around it, and confirm that piece can't hold it; one that can, takes it, and the design changes.
   Then every kept piece: still the right owner? Then every changed one: each change — a rename, a
   move, wider visibility, a dropped branch — is one a task can't be built without, and the rest go:
   a `private const val API_HOST` a new caller needs loses `private`, it isn't moved and renamed.
   Every claim about how existing code behaves, in a row's reason or a `Not` line, is read in that
   code, never recalled: "the client binds only once the main screen opens" — read, it binds on first
   call. A copy of another repository's interface takes the whole upstream change, not the one call
   the design needs, and the design names what else it changes. Done when every row's and every `Not`
   line's reason holds up in the code, not when the design reads well.
4. **Tasks.** Instructions in the order they run, checks under a task where one proves it. Suggest
   checkpoints where the user would want to see it working.
5. **The OK.** Ask for it in one line, per spec-change-rules' *Approval*, and stop.

## 3. Build — only on request

1. **Scope:** the tasks the user named, or every unticked one. A draft asked to be built is approved by
   that request — set `status: approved` and say so.
2. **Before code:** read the project's code-style rules, where it has them, and the code the tasks
   touch; match their patterns.
3. **For each task, in order:**
   1. Re-read the plan.
   2. Build it. Tests, when wanted, go to `spec-test-writer` / `spec_test_writer`, pointed at the Requirements and
      the task's checks; runs go to `runner`.
   3. **A checkpoint** — stop, say what to try, and wait. Write what they saw on its Check line. If it
      didn't hold: a bug is fixed in place and tried again; a wrong design goes to *Reshape*.
   4. **When every check holds:** tick the task, and update the specs it moved in place.
   5. **Blocked by an Open question:** skip it and continue; report it.
4. **Every task ticked:** run `spec-rebuild-overviews`, and say it's ready to fold in.

## 4. Reshape

Per spec-change-rules' *Shaping the plan*: pending tasks, Requirements and Design are rewritten to
what's true now, and a dropped approach becomes a `Not` line. A changed Design goes back to the
`spec-architect` subagent, briefed as in *Write the plan*, when it touches more than one class; then
every Design line and every task, built ones included, is re-read against it, and one the change made
untrue is rewritten, its built code reworked. The user trying what's built and
adjusting changes the code and specs directly, with no new task. A reshape the user asked for needs no
new OK; one you propose waits for it, in one line. Then continue building where it left off, unless the
user set the plan back to `draft` or asked to stop.

## Report

- **Plan written:** the design, the choices the user made, what's still open and what each open
  question blocks, and "the plan is ready — say when to build".
- **Building:** tasks ticked, where it paused and what to try, what's blocked on what, and the specs
  updated.
