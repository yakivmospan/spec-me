---
holds: how code in this repository is written — its conventions, not the process around it
elsewhere:
  project-workflow-rules: commit, branch, merge request, pull request, pipeline, CI, git hook, release, tag
  project-sensitive-paths-rules: ask before, do not touch, breaks the build for everyone
---
# Code style rules

<!--
  FILLING THIS IN (SETUP.md Step 6, or by hand later):

  One row per convention, and only where a competent developer would otherwise do something
  reasonable and wrong here. A row that restates general good practice is noise; delete it.

  Every row needs evidence — a file path, a symbol, a config key you have actually opened. A rule
  you cannot point at is a rule someone will "fix" next month.

  This file is the stack-agnostic half. Anything that only makes sense in one language or framework
  — its concurrency model, its UI state types, its DI container — belongs in the stack profile's own
  `*-code-style-rules.md`, which the loader lists in the same row as this one. Keeping them apart is what
  stops a Kotlin convention reaching a project that has no Kotlin in it.

  Expect 3-8 real rows. Delete every row you have no evidence for, including all of these examples.
-->

## This project

| Topic | Rule |
|---|---|
| Logging | {{Which façade or logger to call, with its path, and what is forbidden — the platform's raw logger, printing to stdout, or reaching past the façade. If some modules deliberately don't use it, say which and why, or someone will "fix" them.}} |
| Error handling | {{The project's retry and failure-escalation pattern and where it lives, plus what it is *not* — an in-call retry is not durability.}} |
| Visibility | {{What the default is, and what going public commits you to — usually a spec obligation the moment something outside the module can reach it.}} |
| Formatting | {{Whether the formatter runs automatically (a build step, a git hook) and whether lint is advisory or a gate. If builds silently reformat, say so — it explains diffs nobody wrote.}} |
| Module dependencies | {{Point at the architecture spec's Boundaries; never restate the graph here. Say what counts as a boundary change and that it needs flagging first.}} |
| New dependency | {{Whether adding one needs saying first, and where the existing list lives — a dependency duplicating something already there is a different conversation than a genuinely new need.}} |
