---
name: vue-create
description: >
  Use when asked to add, create, build, update or review a Vue page, view, screen, component, layout
  or composable, or about props and emits typing, `v-model`, state hoisting, reactivity or accessibility
  in a Vue UI — the file placement, component split, typing, reactivity, accessibility and component-test
  rules a Vue single-file component follows. Not for TypeScript cleanliness or what a change left behind
  (code-clean-typescript), or tests of logic with no component (a unit-test skill, where the project has one).
---

# Create or Update a Vue Page, Component or Composable

**The project's rules and the surrounding file come first — read what `AGENTS.md` loads for this work, if you haven't.**
Where the project hasn't decided, these rules fill the gap. Adding a library is the user's call — ask
first.

Names in examples are placeholders for the project's own. Vue 3.5 APIs are shown; on an older minor,
use the equivalent the project already uses. Rules marked *(EAA)* are required where the product
falls under the European Accessibility Act, and good practice everywhere else.

## Rules

| Rule | Detail |
|------|--------|
| **Files** | Follow the project's layout. In a Feature-Sliced Design project: a routed page in `pages/<slice>/`, a user action in `features/<slice>/`, a business object's model and UI in `entities/<slice>/`, domain-free building blocks in `shared/ui/`; inside a slice, segments such as `ui/`, `model/`, `api/`; the slice's public API (its `index.ts`, or the project's form of it) exports what others use, and nothing imports past it or from a slice on the same layer. One component per file, multi-word PascalCase; a component past ~200 lines splits along its parts. |
| **Script** | `<script setup lang="ts">`. Block order as the project's other components have it. |
| **Page and components** | A page wires: it reads route params, calls composables, passes plain values down and handles emitted events. Components below it take props and emit events, and know nothing of the router or a store. |
| **State in composables** | State and logic beyond display live in a composable, `useThing()`, returning refs, computeds and functions — testable without mounting. UI-only state (open, the active tab) stays a local `ref`. State lives at the lowest common ancestor that needs it, no higher. |
| **Props** | Type-based: `defineProps<Props>()`, with defaults by destructuring. Props are read-only: a child that wants a value changed emits. Pass plain values, never a whole store or a `Ref`. |
| **Emits and `v-model`** | `defineEmits<{ select: [id: string] }>()`, named for what happened (`select`, `close`), not for a handler. A two-way value is `defineModel<T>()`. |
| **Derived values** | A `computed` — never a method doing work in the template, never a `watch` writing a `ref`. |
| **Watchers** | Only for effects that leave the component: a request, storage, focus. Clean up with `onWatcherCleanup`; `immediate` only when it must run on load. |
| **Async data** | A component that loads shows loading, error and empty states. A request whose input changed or whose component unmounted is aborted or its result ignored. |
| **Lists** | `v-for` with a stable `:key` from the data, never the index of a list that changes. No `v-if` on a `v-for` element — filter in a `computed`. |
| **Large data** | Big data replaced rather than edited goes in a `shallowRef`. |
| **DOM access** | Only through template refs (`useTemplateRef`), never `document.querySelector` in a component. |
| **`v-html`** | Never with anything a user or a server could author — render it as text, or sanitise it with the project's sanitiser. |
| **Slots, `provide`** | Content that varies goes in a slot, not a growing set of boolean props. `provide`/`inject` only for a deep tree, typed with an `InjectionKey<T>`. |
| **Routes** | Pages load lazily — `component: () => import(…)`. Route params are read, converted and checked in the page, then passed down as typed props. |
| **Styles** | `<style scoped>` or a CSS module. Reach into a child only with `:deep()`, sparingly. The project's design tokens where it has them. |
| **Semantic elements** | `<button>` for an action, `<a href>` or `RouterLink` for navigation — never a clickable `<div>`. Native `<input>` with a `<label>`, native `<dialog>`. Headings in order, one `<h1>` per page. |
| **Accessible names** | Every control names its **purpose** in a visible label or `aria-label`; icon-only buttons included. Images have `alt`, empty for decoration. Text goes through the project's i18n where it has one. |
| **Keyboard** | Every action works from the keyboard in a logical order, with visible focus — `:focus-visible` is never removed without a replacement. No positive `tabindex`. |
| **Focus management** | After navigation, focus moves to the new page's heading or main region. A dialog traps focus while open (`showModal()` does) and returns it to its opener when it closes. |
| **Custom controls** | Expose role and state — `aria-pressed`, `aria-expanded`, `aria-checked` — or use the native element instead. |
| **Live regions** | Status and async results go in a polite live region (`role="status"`) that exists before its text changes. |
| **Colour alone** | Never convey information by colour alone — pair it with text, an icon or a shape. |
| **Contrast (EAA)** | Normal text ≥ 4.5:1; large text (≥ 24px, or ≥ 18.66px bold) ≥ 3:1; control boundaries and meaningful graphics ≥ 3:1, in every state; disabled controls exempt. |
| **Target size (EAA)** | At least 24 × 24 CSS px (WCAG 2.5.8); 44 × 44 for primary touch targets. |
| **Resize and reflow (EAA)** | Text in `rem`; no fixed heights on text containers; usable at 200% zoom and at 320 CSS px wide (WCAG 1.4.4, 1.4.10). |
| **Motion (EAA)** | Nothing flashes more than 3 times per second (WCAG 2.3.1). Animation respects `prefers-reduced-motion`. |
| **Timeouts (EAA)** | Warn before a session expires, with ≥ 20 seconds to extend; auto-advancing content can be paused (WCAG 2.2.1). |
| **Form errors (EAA)** | Identified in text with a correction suggestion, tied to the field by `aria-invalid` and `aria-describedby`, and announced (WCAG 3.3.1, 3.3.3). |
| **Dragging (EAA)** | Every drag or multi-point gesture has a single-pointer alternative (WCAG 2.5.1, 2.5.7). |
| **Component test** | Each new component or composable gets a test beside the project's others, with its test library — `@vue/test-utils` by default. Mount with props; find by role, label or text, never by a CSS class; trigger events and assert `emitted()`; `await` after each change. A composable is tested by calling it. Plugins the component needs (router, i18n, store) go in `global.plugins`, as test instances. |

## Steps

1. **Find the nearest existing component** — one already doing the job gets extended, not duplicated.
   Note its layer and slice, file names, block order, props and emits style, composable shape, test
   location and styling tokens — done when you can name each.
2. **Decide the files** per *Files* — done when every component, composable and type has one, and each
   slice's public API names what others will import. For a new page, `reference.md` has the template.
3. **Write or change the code** against the rules table.
4. **Write or update the component test**, and run it with the project's test script.
5. **Tick the checklist below** item by item against every component you wrote or changed; fix what
   fails. Gaps in code you didn't change go in the report, not the diff.
6. **Reviewing only:** tick the checklist the same way; report each failed item as one line —
   `**defect|risk|clarity** — file:line — what's wrong. Fix: …` — and stop.

## Checklist

**Structure**
- [ ] Checked for an existing component doing the job; names and shape match the nearest one
- [ ] Each file in its layer and slice; imports only through a slice's public API, only downward
- [ ] Page wires; components below take props and emit; logic beyond display in a composable

**Typing and reactivity**
- [ ] `<script setup lang="ts">`; type-based props and emits; `defineModel` for a two-way value
- [ ] No prop mutated; plain values passed down
- [ ] Derived values are `computed`; watchers only for outside effects, and cleaned up
- [ ] Loading, error and empty states; stale requests aborted or ignored
- [ ] `v-for` keys stable and from the data; no `v-if` beside `v-for`
- [ ] No `document` queries; no `v-html` with authored content

**Accessibility**
- [ ] Semantic elements; headings in order; every control labelled by purpose; images have `alt`
- [ ] Keyboard reachable with visible focus; focus moves on navigation; dialogs trap and return it
- [ ] Custom controls expose role and state; status in a polite live region
- [ ] Every *(EAA)* row and *Colour alone* checked

**Tests**
- [ ] A test per new component or composable, querying by role, label or text; it passes

## Report

Files created or changed, with line counts; rules that needed a fix; gaps left in existing code; the
test result; and anything a rule needed that the project lacks (a library, a token, a string).
