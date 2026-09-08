---
name: spec-plan
description: Use when asked to "plan this", "design this", "how should we build X", "compare approaches", "ask the architect", "implement PROJ-1234", "build the change", "continue the plan", "the design changed", "rework what we built", or once a change's spec files are agreed — writes a change's implementation-plan.md (design and tasks) with the user, builds from it task by task when asked, and changes course mid-way. Not for writing requirements or a spec from code (spec-create), or approving a spec written from code and folding a change in (spec-merge).
---

# Spec Implementation Plan

A change's spec files say what will be true; its `implementation-plan.md` says how, and in what order.
This skill holds the plan's whole life: writing it with the user, building from it, and changing it when
the work or trying it shows something new. The file carries it between sessions.

## Non-negotiables

- **Spec files agreed first.** No Design or Tasks until the user has said the spec files say the right
  thing — agreed in chat, not yet `approved`. Grounding reading alone may come earlier, when shaping a
  change needs the module split.
- **The user decides a real choice.** At least two options in one table; the `spec-architect` subagent reads
  and proposes, never decides.
- **Build only when asked.** Writing the plan never starts building: stop and say it's ready.
- **A ticked task is never rewritten or unticked.** Rework is a new task among the pending ones.
- **Never settle an Open question, or edit or remove a criterion, on your own.** Build what isn't blocked,
  and ask.
- **A checkpoint waits for the person.** A task whose check only a person can make is ticked only after
  they say it held.

## 1. Before anything

1. Read, if not already read this session, `.agents/profiles/specs/rules/on-demand/spec-change-rules.md`, `spec-format-rules.md`, `spec-style-rules.md` — and `spec-architecture-rules.md` before a real design choice —
   and the whole change: every spec file, the plan if there is one, and each moved spec's diff —
   `git diff -M` against the branch the change will merge into — so you know what changes.
2. A plan already there is where the work left off: continue it, never restart.
3. Pick the part:
   - **No change yet:** work that changes a guarantee goes to `spec-create` first; a design that changes
     none is agreed in chat (spec-builder-rules' *Every task*).
   - **Sent by `spec-create` for the module split:** *Write the plan* step 1 only, report which module
     owns what, and hand back.
   - **Asked to build:** *Build*, with a plan or without one.
   - **No plan yet, and not asked to build:** when `spec-create` or the user already said one is needed,
     *Write the plan*; otherwise ask whether the work needs one — a real design choice, or enough work to split. No: approval goes ahead without one, and building waits to be asked. Yes: *Write the plan*.
   - **Something learned or changed mid-way, or the user sets the change back to draft:** *Change course*.

## 2. Write the plan

Once the spec files are agreed, copy `.agents/profiles/specs/templates/implementation-plan.md` into the change folder,
then with the user, a section at a time:

1. **Ground it.** Read the code the change touches, and bring findings the design must act on, not a
   tour. Wide reading goes to the `spec-architect` subagent with a bounded brief: which modules, what to find
   out.
2. **Design.**
   - **One obvious way:** a sentence or two, and say there was no real choice.
   - **A real choice:** the options in one table, on concrete tradeoffs — the `spec-architect` subagent
     compares them across modules. The user picks; the winner goes into Design, each other option as a
     `Not` line with why.
   - **A big change** — a contract, several modules: sub-headings such as Flow, Interfaces, State,
     Concurrency and failure, as spec-change-rules' *Implementation plan* lists. A story's plan says
     which module change carries which contract criteria.
   - **Decisions** per spec-change-rules' *Implementation plan*. **A guarantee that has to change** goes back to the spec files, with
     the user, first.
3. **Tasks.** Instructions in the order they run, tags at the end where a task closes a criterion,
   checks under a task where one proves it. Suggest checkpoints where the user would want to see it working; they edit them at *The OK*.
4. **The OK.** Run `spec-rebuild-overviews`, and report its drift with proposed fixes, and its warnings. Ask the user to approve the
   spec files per spec-change-rules' *Approval* — the plan is approved once every one is — and stop.

## 3. Build — only on request

1. **Scope:** the tasks the user named, or every unticked one. A draft asked to be built is approved by
   that request: set `approved` on every spec file it holds, unless the user names one, say so, and run
   `spec-rebuild-overviews`. **No plan:** the spec files' criteria are the tasks — proof and checkboxes per spec-change-rules'
   *While building*, and what a person saw goes in the report; when all are built, run `spec-rebuild-overviews` and say it's
   ready to fold into the specs, naming the criteria still waiting for the user's word.
2. **Before code:** read the project's code-style rules, where it has them, and the code the tasks
   touch; match their patterns.
3. **For each task, in order:**
   1. Re-read the plan, and any spec file edited since the last task.
   2. Build it. Tests, when wanted, go to `spec-test-writer` / `spec_test_writer`, pointed at the change's spec files, the task's criteria and
      its checks; runs go to `runner`.
   3. **A checkpoint** — a check only a person can make: stop, say what to try, and wait. Write what they
      saw on its Check line. If it didn't hold: a bug in what the task built is fixed in place and
      tried again; a wrong design or guarantee goes to *Change course* with them.
   4. **When every check holds:** tick the task; proof and checkboxes per spec-change-rules' *While building*.
   5. **Blocked by an Open question:** skip it and continue, per *While building*; report it.
4. **The plan stops fitting** — a wrong design, a choice nobody made, a guarantee that doesn't hold:
   stop, and go to *Change course* with the user.
5. **Every task ticked:** run `spec-rebuild-overviews`, and say it's ready to fold into the specs.

## 4. Change course

Follow spec-change-rules' *Changing course* — its table covers a changed design, built work, criteria
edited, added or removed, and work reaching another module. Beyond it:

- **Rework** usually goes right after the last ticked task.
- **A removed criterion** — when the user already said whether its code goes, don't ask again.
- **Back to draft** applies to every spec file unless the user names one, and building stops until they
  ask again.

Then run `spec-rebuild-overviews`, and report what changed. Building that was under way continues from the first unticked
task, at *Build* step 3 — unless the change was *Back to draft* or the user asked to stop; then wait to be
asked.

## Report

- **Plan written:** what the design is, the choices the user made, what's still open and what each
  open question blocks, and "the plan is ready — say when to build".
- **Building:** tasks ticked, criteria checked, where it paused and what to try, and what's blocked on
  what. Every task ticked: say it's ready to fold into the specs.
