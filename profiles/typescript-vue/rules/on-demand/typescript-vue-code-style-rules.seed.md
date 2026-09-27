# TypeScript and Vue code style

<!--
  FILLING THIS IN (SETUP.md Step 6, or by hand later):

  Only what needs TypeScript or Vue to be true. Everything a project would need whatever it is
  written in — logging, error handling, formatting, boundaries, new dependencies — belongs in the
  project's general code-style rule, not here. This profile names no file outside itself, so its
  folder can be lifted into a project that does not use this setup at all.

  Every row needs evidence — a file path, a symbol, a config key you have actually opened. The
  topics worth checking are in ../../PROFILE.builder.md's last section. On a young codebase most
  rows can only be answered from config: keep the question in a row the code can't answer yet, and
  delete a row the project will never need.
-->

## This project

| Topic | Rule |
|---|---|
| Component API | {{`<script setup>` with the Composition API, or the Options API — one, named, with the other ruled out; and whether `lang="ts"` is enforced, and by what.}} |
| Props, emits, `v-model` | {{Type-based `defineProps<Props>()` or runtime props; how defaults are given; emits typed as `defineEmits<{ name: [payload] }>()`; `defineModel` or a `modelValue` prop and emit.}} |
| Shared state | {{Pinia, composables, or a module-level `reactive`/`ref` — one, named, and where shared state lives.}} |
| TypeScript strictness | {{The flags that change how code is written — `strict`, `noUncheckedIndexedAccess`, `verbatimModuleSyntax` and so `import type` — with the config they come from; the `any` and `@ts-…` comment policy and the lint rule enforcing it; whether non-null `!` is allowed.}} |
| Async and side effects | {{Where a component loads data; `watch` or `watchEffect`, and when; how listeners, timers and requests a component starts are cleaned up.}} |
| Naming | {{Component names — multi-word, and the lint rule if one enforces it; file names for components and composables; what a composable returns.}} |
| Import paths | {{The alias (`@/` → `src/`, say) and where it is configured; when an import uses it rather than a relative path; whether `.vue` and `.ts` extensions are written; whether folders are imported through an `index.ts`.}} |
| Layer imports | {{Only where the source is layered — Feature-Sliced Design or similar: the layers top to bottom, that a layer imports only downward and slices on one layer don't import each other, a slice's public API, and any escape hatch. Delete the row where the source isn't layered.}} |
