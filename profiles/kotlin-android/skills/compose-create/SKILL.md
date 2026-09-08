---
name: compose-create
description: >
  Use when asked to add, create, build, update or review a Compose screen, component, UI layout or
  Composable function, or about Compose state hoisting, recomposition or stability annotations —
  the structure, file layout, stability, performance and accessibility rules a Compose UI follows.
  Not for UI tests, or for ViewModel logic in isolation (a unit-test skill, where the project has one).
---

# Create or Update Compose Screen / Component

**The project's rules and the surrounding file come first — read what `AGENTS.md` loads for this work, if you haven't.**
Where the project hasn't decided, these rules fill the gap — its names too: `Intent`/`State` instead of
`Event`/`UiState`. Adding a library is the user's call — ask first.

Names in examples are placeholders for the project's own. Android and Material 3 APIs are shown;
Compose Multiplatform and other design systems use their own equivalents. A project with no Compose
theme gets no theme wrapper in previews.
Rules marked *(EAA)* are required where the product falls under the European Accessibility Act, and
good practice everywhere else.

## Rules

| Rule | Detail |
|------|--------|
| **Files** | Follow the project's own layout where it has one. Otherwise a screen gets its own package: `ExampleScreen.kt` holds the two entry points and the screen's previews; `ExampleUiState.kt` holds UiState and Event; each sub-component with its own preview, or longer than a screen of code, goes in its own file as `internal`, with its preview beside it. Only small single-use helpers stay `private` in the screen file. A file growing past ~400 lines splits along its components. |
| **Stateful and stateless split** | Every screen, and any reusable component that owns a ViewModel, has a ViewModel-connected entry point and a stateless one previews use — two overloads of one name, unless the project splits them its own way (e.g. `XScreen` + `XContent`). A screen's screen-local sub-components take plain values and lambdas, with no ViewModel entry point. |
| **Previews** | Screens: a preview per distinct UiState variant, in the project's preview style — light and dark where the app has a dark theme (`@PreviewLightDark` where the tooling has it). Reusable components: at least one preview. Screen-local sub-components: only if complex enough to warrant it — the parent screen preview covers simple cases. |
| **Hoist state** | State lives at the lowest common ancestor that needs it. Stop hoisting when only one composable needs the state. UI-only state (a dialog's visibility, an expanded row) stays in `rememberSaveable` unless the project keeps it in its screen state; anything the ViewModel must act on goes through an event. |
| **Pass plain values to children** | Children receive plain values, not entire state objects or `State<T>` wrappers. |
| **`onEvent` for screens** | A screen exposes `onEvent: (Event) -> Unit`. Its screen-local sub-components take `onEvent` when they raise several events, or a plain lambda when they raise one. Never pass ViewModel references into child composables. Reusable components expose typed lambdas (`onConfirm: () -> Unit`, etc.). |
| **Single sealed Event type** | All screen interactions go through one `sealed class` via `onEvent`. Never substitute multiple callback lambdas for a ViewModel interaction boundary. |
| **UiState and Event stability** | Don't assume a sealed hierarchy is inferred stable — the compiler judges the base type, and interfaces never are. Without strong skipping, annotate UiState and Event bases `@Immutable` when every subtype is; with it, this rarely matters. |
| **Stable collections** | Check whether the project's Compose compiler uses strong skipping (on by default from Kotlin 2.0.20). With it, a composable taking `List<T>` still skips when handed the same instance — emit a new list only when its contents change. Without it, `List<T>` makes the composable unskippable: use the project's immutable collection type (`ImmutableList<T>` from kotlinx.collections.immutable is the usual one), or annotate the holding UiState class `@Immutable`; ask before adding the library. |
| **`data class` with `val` only** | All UiState and UI model types use `val` properties only. |
| **`@Immutable` vs `@Stable`** | `@Immutable`: all properties are `val`, no mutations after construction. `@Stable`: `equals()` is reliable; may mutate but notifies Compose. Never apply `@Immutable` to a mutable type. |
| **Simple lambdas by default** | Plain inline lambdas are correct in most cases. Stabilise with `remember` only when profiling shows unnecessary recomposition. In `LazyColumn`, pass the screen's `onEvent` down and put the item id in the event — avoid `remember(item.id) { { ... } }` per item. |
| **`derivedStateOf`** | Use inside `remember { }` only when a UI-local value changes less frequently than its upstream state (e.g. scroll position → button visibility). Never for ViewModel data transformations. |
| **`remember` for expensive work** | Wrap expensive computations in `remember { }` with correct keys. Never place sorting, filtering, or mapping directly inside `items {}` — it re-runs every time an item composes, which during a scroll is constantly. |
| **Lazy layout keys** | Always pass a stable `key` to `items()`. Without it, list reorders recompose every item instead of just the moved one. |
| **Lambda modifiers for frame-rate state** | When state changes every frame (scroll offset, animation), use the lambda modifier variant: `Modifier.offset { }` not `Modifier.offset(y = )`, `Modifier.drawBehind { }` not `Modifier.background()`. The read moves to a later phase — placement for `offset { }`, drawing for `drawBehind { }` — so the change no longer recomposes. |
| **No backwards writes** | Never write to a `State` object after reading it in the same composition body — causes an infinite recomposition loop. Write only in event lambdas or `LaunchedEffect`. |
| **Side effects** | Collect one-off effects in the public overload only — through the project's side-effect helper where it has one, otherwise a lifecycle-aware collection in a `LaunchedEffect`. Never pass the effects flow down the tree. Concrete handlers go in `private suspend fun`s. |
| **Modifier convention** | `modifier: Modifier = Modifier` after required parameters, before optional styling. |
| **Dimensions** | Use the project's spacing or design-system tokens where it has them; otherwise follow the file's existing style. |
| **Content descriptions** | Every interactive or meaningful element has a `contentDescription` describing its **purpose** (not type, not appearance). Decorative elements: `contentDescription = null`. Always use `stringResource` — no hardcoded strings. List item descriptions must be unique per item. |
| **Touch target size** | Minimum 48dp × 48dp (Material; 44pt on iOS) for every interactive element. Use `Modifier.minimumInteractiveComponentSize()` or padding to reach the minimum when the visual is smaller. |
| **Text sizes in `sp`** | Always `sp` (or `MaterialTheme.typography`) for text — never `dp`. Layouts must survive font scale 200% — check with a `fontScale = 2f` preview in the project's preview style: use `wrapContentHeight()`, not fixed heights, on text containers. |
| **Semantics: merge related elements** | Wrap logically related composables (icon + title + subtitle) with `Modifier.semantics(mergeDescendants = true) {}` so TalkBack announces them as one unit. |
| **Semantics: headings** | Mark section headings with `Modifier.semantics { heading() }`. |
| **Semantics: custom interactive state** | Custom toggles/switches must expose `role` and `stateDescription` via `Modifier.semantics { role = Role.Switch; stateDescription = "..." }`. |
| **Live regions** | Dynamic content that updates without user interaction (status messages, async results) needs `Modifier.semantics { liveRegion = LiveRegionMode.Polite }`. |
| **Keyboard / Switch Access focus** | All interactive elements must be focusable and reachable in logical composition order. Custom dialogs trap focus while open (Material dialogs on Android already do). After a dialog closes, restore focus to a sensible element when one still exists, via `FocusRequester.requestFocus()` — and keep the restore target only while the dialog is open, so a restored process doesn't move focus. A control inside a row that is itself toggleable or clickable takes no focus of its own (`Modifier.focusProperties { canFocus = false }` on its wrapper). |
| **Colour alone** | Never convey information by colour alone — always pair with icon, label, or shape. |
| **Colour contrast (EAA)** | Normal text (< 18sp, or < 14sp bold): ≥ 4.5:1. Large text (≥ 18sp, or ≥ 14sp bold): ≥ 3:1. UI component boundaries and meaningful graphics: ≥ 3:1. Check all interactive states; disabled components are exempt. |
| **Flashing (EAA)** | Nothing may flash more than 3 times per second (WCAG 2.3.1). |
| **Session timeouts (EAA)** | Warn before session expiry; give ≥ 20 seconds to extend. Auto-advancing content must be pausable (WCAG 2.2.1). |
| **Form errors (EAA)** | Errors identified in text (not colour alone) with a correction suggestion. Error state announced via `Modifier.semantics { error("...") }` or a live region (WCAG 3.3.1 / 3.3.3). |
| **Gesture alternatives (EAA)** | Every multi-point or path-based gesture (swipe, pinch, drag) must have a single-pointer alternative (WCAG 2.5.1). |

## Steps

1. **Find the nearest existing screen** — one already doing the job gets extended, not duplicated. Note
   its names, file split, stateful/stateless split, preview style, DI accessor, theme, side-effect helper,
   spacing tokens and collection types — done when you can name each.
2. **Decide the files** per *Files* — done when every composable and type has one. For a new screen,
   `reference.md` has the template.
3. **Write or change the code** against the rules table.
4. **Tick the checklist below** item by item against every composable you wrote or changed; fix what
   fails. Gaps in code you didn't change go in the report, not the diff.
5. **Reviewing only:** tick the checklist the same way; report each failed item as one line —
   `**defect|risk|clarity** — file:line — what's wrong. Fix: …` — and stop.

## Checklist

**Architecture**
- [ ] Checked for an existing screen doing the job; names and shape match the nearest existing screen
- [ ] Files split per *Files*; no file past ~400 lines
- [ ] Every screen has a ViewModel-connected entry point and a stateless one; screen-local sub-components take plain values and lambdas
- [ ] Side effects collected once, in the public overload, through the project's helper where it has one

**State & events**
- [ ] `onEvent: (Event) -> Unit` everywhere; no ViewModel references below the public overload
- [ ] Children receive plain values, not state objects or `State<T>`
- [ ] State hoisted to lowest common ancestor only

**Stability**
- [ ] UiState and Event stability checked, not assumed; `@Immutable` where strong skipping is off and every subtype is immutable
- [ ] All UI model `data class` types use `val` only
- [ ] Collections use the project's immutable type, or the holding class is `@Immutable`

**Performance**
- [ ] Simple lambdas by default; `remember` only where profiling justifies it
- [ ] `LazyColumn` items get the screen's `onEvent`, with the id in the event; no per-item `remember` allocations
- [ ] `derivedStateOf` used only for UI-local derived state, not ViewModel data
- [ ] Expensive computations and list transformations wrapped in `remember`; none inside `items {}`
- [ ] Every `LazyColumn` / `LazyRow` `items()` call has a stable `key`
- [ ] Frame-rate state (animation, scroll offset) read via lambda modifiers
- [ ] No backwards writes

**Previews**
- [ ] Screens: a preview per UiState variant, in the project's style; layout checked at `fontScale = 2f`
- [ ] Reusable components: at least one preview
- [ ] Screen-local sub-components: preview only if complexity warrants it

**Accessibility**
- [ ] Every interactive/meaningful element has a `contentDescription` (purpose, not type); decorative elements have `null`
- [ ] All `contentDescription` strings use `stringResource`; list descriptions are unique per item
- [ ] Every interactive element meets 48dp × 48dp minimum touch target
- [ ] All text in `sp` or `MaterialTheme.typography`; text containers use `wrapContentHeight` not fixed heights
- [ ] Logically related elements use `semantics(mergeDescendants = true)`
- [ ] Section headings marked with `semantics { heading() }`
- [ ] Custom interactive elements expose `role` and `stateDescription` via semantics
- [ ] Dynamic content updates use `liveRegion = LiveRegionMode.Polite`
- [ ] All interactive elements keyboard/Switch Access focusable; dialogs trap and restore focus; the restore target lives only while the dialog is open
- [ ] A control inside a toggleable or clickable row takes no focus of its own
- [ ] Information never conveyed by colour alone
- [ ] Normal text contrast ≥ 4.5:1; large text ≥ 3:1; UI boundaries and meaningful graphics ≥ 3:1 (all states; disabled exempt)
- [ ] Nothing flashes > 3 times/second
- [ ] Session timeouts give ≥ 20s to extend; auto-advancing content is pausable
- [ ] Form errors identified in text with correction suggestion; announced via `semantics { error(...) }`
- [ ] Every swipe/pinch/drag gesture has a single-pointer alternative

**Misc**
- [ ] Every screen and reusable component takes `modifier: Modifier = Modifier`, applied to its root
- [ ] Dimensions use the project's tokens where it has them

## Report

Files created or changed, with line counts; rules that needed a fix; gaps left in existing code; and
anything a rule needed that the project lacks (a library, a token, a string).
