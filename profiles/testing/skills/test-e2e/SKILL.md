---
name: test-e2e
description: Use when asked for "e2e tests", "end-to-end tests", "test it on the device", "run it on the emulator or the car", "check it on the device without me clicking", "automate this manual check" or "run the test plan on the device", or to prove a user journey across real apps on a real device — writes instrumented tests that drive the real apps and runs them, visibly on screen, or drives the device over adb through a manual test plan's cases. Not for one class or a few components (test-unit, test-integration), or writing a manual test plan (test-plan-manual).
---

# Test E2E

Proves a user journey on a real device — an emulator or a car — the way a person would click it, with
nothing mocked, on screen for anyone who wants to watch. What goes wrong most: asserting on something no user or client
can see, sleeping instead of waiting, and a test that stops the app it runs inside.

## Non-negotiables

- **The project's rules and the surrounding file come first — read what `AGENTS.md` loads for this work, if you haven't.**
- **Nothing mocked** — the real apps, against the backend the build points at.
- **One journey per test, and no test relies on another** — each sets its own start state, so any one
  runs alone and in any order.
- **A test never stops or clears the app it runs inside** — cross-app tests run from a test-only
  module in their own process (`reference.md`).
- **Wait, never sleep** — on the element, the state or the log line, with a timeout whose failure
  names what was expected.
- **Assert what a user or a client sees** — a screen, a dialog, a state a client reads, a line the app
  logs on purpose — never an internal field.
- **Backend writes only on a test account**, undone at the end where the app offers a way. Not sure the
  signed-in account is one: ask before the first run.
- **Every failure is reported with its assertion and its log**; a pass by name.

## Before starting

1. Find how this project builds and installs each app the journey uses, and which devices it targets —
   its tech notes or build files. Not written down: stop and ask, and on the user's yes write the
   answer where the project keeps such facts.
2. `adb devices -l` lists the device. None: stop and ask which to connect — an emulator, or a car over
   USB or the network. Read the build under test (`reference.md`) for the report.
3. **For a written test:** a test-only module and a UI automation library that crosses apps —
   UiAutomator on Android. Missing: propose the module, its build file and the dependency line as a
   change of its own — a new module is a boundary change, and build files are sensitive paths
   (`project-sensitive-paths-rules`) — and wait for a yes. A no: offer to drive the check over adb
   instead.

## Write a test

1. **Name the journey** from the user's side — the start state, what they do, what they see — done
   when it reads as one Given/When/Then.
2. **Set the start state in the test** by shell command (`reference.md`) — app data, permissions, a
   dependency stopped — or, where shell can't, through a client's own UI as the test's first Given
   steps. What neither can set — a signed-in account, an agreement — is checked at the start and fails
   the test naming what is missing; no way to check it: ask what the test may assume.
3. **Drive it** through the UI, or the entry points a real client uses — an intent, a bound service —
   never anything internal. A control with no text or description to find it by: say so, and ask
   before adding a test tag to production code.
4. **Assert** per the non-negotiables — done when a failing assertion says what the user saw instead.
5. **Place it** in the test-only module, the file ending in `E2eTest`, with Given/When/Then comments and
   when/then names as the project names tests.
6. **Run it** on the device without an IDE (`reference.md`, which also says how to watch). Done when
   it passed twice in a row, or its failure is reported.
7. **A manual test plan has this journey as a case:** add `Automated:` to that case, naming the test.

## Drive a manual test plan

For a check not worth a test, or a plan the user asks to run:

1. **Find the case.** No plan file, or no case for this check: ask whether to write the plan first,
   through `test-plan-manual`, or run this one check and report it in chat.
2. **For each case, in the order written** — set its Preconditions and do its Steps over adb
   (`reference.md`), then check its Expected against the screen and the log. Say each step in a line as
   it happens, so the user can follow on screen.
3. **Record each outcome** — in the plan, as `test-plan-manual`'s *Reporting back* says, when the user
   asked to run the plan; in chat for a single check. Name the device with the builds, and save a
   failure's screenshot outside the repository, its path in the report.
4. **A step adb can't do** — a physical button, speaking, listening — leaves the case not run, with
   why; never guess its result.

## When the plan stops fitting

- **A screen or dialog nothing expected** — stop, take a screenshot, and report it with the step that
  led there; never tap it away.
- **The device disconnects or reboots mid-run** — stop and say which test or case was running.
- **Passes and fails on the same build** — stop, report both runs, and propose what to wait on instead;
  never add a sleep or a retry to hide it.
- **A step needs root or a permission the device refuses** — say which command, and ask whether to skip
  that step or use a build that allows it.

## What to test

Journeys across screens and apps; what shows once the backend or a dependency has answered; the state a
stopped dependency or a revoked permission leaves — not a crash or a blank screen; and recovery once the
cause is fixed. Not here: logic (`test-unit`), wiring between components (`test-integration`), each
render state of one screen.

## Report

Per test or case: its name, the device and build, pass or fail, and each failure's output. Then what
wasn't run and why, and the plan file where outcomes were recorded.
