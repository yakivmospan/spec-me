# Profile: typescript-vue

TypeScript on Vue 3 — Vite, Vitest, Vue single-file components, Feature-Sliced Design friendly. What
this file holds is what `SETUP.md` needs to know about the stack. It stays in the builder and is never
installed.

Everything here is true of the stack. Nothing here names a particular project — see
`.agents/builder/profiles/README.md` (*What a profile may say*) for why that line matters.

## Detection

A repository is on this stack if a `package.json` lists `vue` (3.x) in any dependency field **and** it
uses TypeScript — `typescript` in a dependency field or a `tsconfig.json` — **and** it has `.vue`
sources. `vite` in `package.json` or a `vite.config.*` confirms the build half; Vitest with
`@vue/test-utils` confirms the component-test step of `vue-create`, which otherwise uses whatever runner
the project has. A `nuxt` dependency still matches, but Nuxt's file-based routing and auto-imports
decide where files go — say so when offering `vue-create`.

## Tool commands, for a permission allowlist

Read-only or routinely-safe commands that a per-project `.claude/settings.json` can allow without a
prompt, and the ones that should always ask:

| | |
|---|---|
| Allow | `npm run lint*`, `npm run type-check*`, `npm run test:unit*`, `npx vitest run*`, `npx vue-tsc*`, `npx eslint*`, `npx oxlint*`, `npm run format*`, `npm run build*`, `npm ls*` |
| Ask | `npm install*`, `npm uninstall*`, `npm update*`, `npm ci*`, any `npx` of a package the project doesn't list (it downloads one), `npm run dev*` and `npm run preview*` (they never exit), `npm publish*`, anything that deploys |
| Never | loosening an ESLint or oxlint rule, a `tsconfig` strictness flag (`strict`, `noUncheckedIndexedAccess`, …), adding `eslint-disable`, `@ts-ignore` or `@ts-expect-error`, or skipping a test (`.skip`, `.only`, `--passWithNoTests`) to make a run pass |

Script names vary by project — `test:unit`, `test`, `vitest`, a lint script that also fixes files.
Confirm against the real `scripts` in `package.json` rather than assuming the names above. Plain
`vitest` watches when run in a terminal; `vitest run` exits.

## What a project on this stack still has to answer for itself

These are the topics the code-style forms ask about. They are listed here because *which questions
matter* is a fact about the stack, while the answers are facts about one project.

**This profile's own form**, `rules/on-demand/typescript-vue-code-style-rules.seed.md` — only what
needs TypeScript or Vue to be true:

- Component API — `<script setup>` and the Composition API, or the Options API: pick one and say so
- Props, emits and `v-model` — type-based `defineProps<T>()`, how defaults are given, `defineModel`
- Shared state — composables, a reactive module, or a store library: pick one and say so
- TypeScript strictness — `strict`, `noUncheckedIndexedAccess`, type-only imports, the `any` policy,
  suppression comments
- Async and side effects in components — where data loads, watchers, cleanup
- Naming — component and composable files and names
- Import paths — aliases or relative paths, extensions, barrel files
- Layer imports, optional — Feature-Sliced Design's public API per slice, no cross-slice imports within
  a layer, layers importing only downward

**The project's general code-style rule** — the same questions every project answers, whatever it
is written in. Where this setup is installed that is the engine's own form; this profile names no
path outside itself, so its folder also works in a project that has never heard of the setup:

- Logging — which façade, and what is forbidden
- Error handling — the retry or failure-escalation pattern, if the project has one
- Formatting — whether the formatter runs automatically and whether lint gates
- Module boundaries and where the allowed dependency graph is written down; new dependencies; what
  going public commits you to

`LOADER.md` lists the two in one row, so both are read together. Keeping them apart is what stops a
Vue convention reaching a project with no Vue in it — `project-test-setup` reports engine rules written
in a stack's vocabulary, under *Stack wording in the engine's own rules*. The layer-imports row says
*how* a Feature-Sliced project imports; *which* layers and slices exist stays wherever the general
rule's module-boundaries answer points.
