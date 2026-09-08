# Kotlin and Android code style

<!--
  FILLING THIS IN (SETUP.md Step 6, or by hand later):

  Only what needs Kotlin or Android to be true. Everything a project would need whatever it is
  written in — logging, error handling, formatting, boundaries, new dependencies — belongs in the
  project's general code-style rule, not here. This profile names no file outside itself, so its
  folder can be lifted into a project that does not use this setup at all.

  Every row needs evidence — a file path, a symbol, a config key you have actually opened. The
  topics worth checking are in ../../PROFILE.builder.md's last section. Delete every row you have no
  evidence for, including all of these examples.
-->

## This project

| Topic | Rule |
|---|---|
| Coroutines | {{The rule that actually bites here — a blocking call needing an explicit dispatcher, a forbidden `runBlocking`, a scope that must be used.}} |
| Naming a signal | A `Flow` that says something changed is `<thing>Updates`, never `<thing>Changes`, with `_<thing>Updates` behind it; `on*` is for callbacks, not for a flow. {{Keep, change or delete to match this project.}} |
| State exposure | {{`StateFlow`, `LiveData`, or callbacks — one of them, named, with the others ruled out.}} |
| Dependency injection | {{Framework, where modules live, who calls the equivalent of `startKoin`, and whether library modules may. "No manual wiring, no second DI framework" is worth stating if true.}} |
| Visibility | {{Whether `internal` is the default — Kotlin's module-scoped visibility has no equivalent elsewhere, so say it here even though the general rule covers what public costs.}} |
