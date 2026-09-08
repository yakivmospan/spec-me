# Profile: kotlin-android

Kotlin on Android — Gradle, JUnit, Jetpack Compose. What this file holds is what `SETUP.md` needs to
know about the stack. It stays in the builder and is never installed.

Everything here is true of the stack. Nothing here names a particular project — see
`.agents/builder/README.md` (*Change the builder*, *Add a stack*) for why that line matters.

## Detection

A repository is on this stack if it has `build.gradle.kts` or `build.gradle` **and** Kotlin sources
under `**/src/main/{java,kotlin}/**`. An `AndroidManifest.xml` or the `com.android.*` Gradle plugin
confirms the Android half; without it, the Compose skill is not worth installing.

## Tool commands, for a permission allowlist

Read-only or routinely-safe commands that a per-project `.claude/settings.json` can allow without a
prompt, and the ones that should always ask:

| | |
|---|---|
| Allow | `./gradlew *:testDebugUnitTest*`, `./gradlew *detekt*`, `./gradlew *ktlint*` |
| Ask | `./gradlew assemble*`, `./gradlew install*`, anything that signs or publishes |
| Never | loosening `detekt.yml`, a ktlint filter, or a test to make a run pass |

Task names vary by project — `testDebugUnitTest`, `test`, a custom alias. Confirm
against the real Gradle tasks rather than assuming the defaults above.

## What a project on this stack still has to answer for itself

These are the topics the code-style forms ask about. They are listed here because *which questions
matter* is a fact about the stack, while the answers are facts about one project.

**This profile's own form**, `rules/on-demand/kotlin-code-style-rules.seed.md` — only what needs
Kotlin or Android to be true:

- Asynchrony — the coroutine rules that actually bite: dispatchers, blocking calls, scopes
- State exposure — `StateFlow`, `LiveData`, callbacks: pick one and say so
- Dependency injection — which framework, where modules live, who starts the graph
- Visibility — whether `internal` is the default, Kotlin's module scope having no equivalent elsewhere

**The project's general code-style rule** — the same questions every project answers, whatever it
is written in. Where this setup is installed that is the engine's own form; this profile names no
path outside itself, so its folder also works in a project that has never heard of the setup:

- Logging — which façade, and what is forbidden
- Error handling — the retry or failure-escalation pattern, if the project has one
- Formatting — whether the formatter runs automatically and whether lint gates
- Module boundaries, new dependencies, and what going public commits you to

`LOADER.md` lists the two in one row, so both are read together. Keeping
them apart is what stops a Kotlin convention reaching a project with no Kotlin in it —
`project-test-setup` reports engine rules written in a stack's vocabulary, under *Stack wording in the
engine's own rules*.
- Module dependencies — where the allowed dependency graph is written down
