# UI test reference

One section per platform, each with its tech stack, how the skill's rules look there, and a template. A
new platform adds a section with the same parts.

## Compose (Kotlin)

Copied from the skill body unchanged. Compose Multiplatform, because that is what it was written for —
the structure is the point. Translate to the framework this project runs.

### Tech Stack

We are using `compose.uiTest`, `kotlin.test`, `mockk`, and `koin-test`.

---

### Compose and Koin rules

| Rule | Detail |
|------|--------|
| **Re-register Koin fresh per test** | Call `startKoin` inside `launchScreen`, `stopKoin` in `@AfterTest` — never share Koin state between tests |
| **Use `viewModel { }` DSL** | Not `single { }` — the public overload resolves via `koinViewModel()` which requires the ViewModel scope |
| **No `Dispatchers.setMain`** | Compose test framework manages its own dispatcher via `runComposeUiTest` |
| **`waitForIdle()` after interactions** | Always call after triggering clicks or input changes before asserting — no import needed, it's a method on `ComposeUiTest` |
| **`assertDoesNotExist()` needs no import** | It's a method on `SemanticsNodeInteraction`, not a top-level function |
| **Match a lazy list's row by position** | Rows of a lazy list with no node of their own are all siblings, so a sibling matcher finds every row; match a row's button by its position instead |

---

### How the rules look in Compose

| Rule | Detail |
|------|--------|
| **Always test the public overload** | Mount `ExampleScreen()` with no arguments — Koin provides the mocked ViewModel |
| **Always mock the ViewModel** | Use `mockk(relaxed = true)` — never use a real ViewModel with real repositories |
| **Verify events on the ViewModel** | Use `verify { mockViewModel.onEvent(...) }` — not an emitted events list |
| **Verify no-op interactions** | For interactions that must NOT fire an event (e.g. clicking an already-active element), use `verify(exactly = 0) { mockViewModel.onEvent(...) }` |
| **Prefer semantic finders** | Use `onNodeWithText`, `onNodeWithContentDescription` before resorting to `onNodeWithTag` |
| **Add test tags sparingly** | Only add `Modifier.testTag(...)` to ambiguous composables; annotate with `@VisibleForTesting` |
| **Scroll before asserting off-screen nodes** | For nodes that may be below the fold in a scrollable screen, call `performScrollTo()` followed by `waitForIdle()` before asserting visibility or enabled state. `assertDoesNotExist()` does not require scrolling — it checks the semantic tree directly |
| **Querying nodes with the same text** | `onNodeWithText` is the default — use it when the text is unique in the tree. It crashes if the same text appears more than once, which itself catches unintended duplicates. Switch to `onAllNodesWithText(...)` only when the text is known to appear multiple times. **Use `onFirst()` only when you intentionally target a single node and the assertion is valid for any one instance** (e.g. a node that is unique in the tree). When a label is known to appear more than once, always assert **all** instances by iterating with index — this applies to every operation including visibility, enabled state, clicks, and scrolls. Using `onFirst()` and ignoring the rest is incorrect and gives false confidence regardless of the assertion type. To assert ALL instances are absent, use `onAllNodesWithText(...).fetchSemanticsNodes()` and assert the result is empty. For the index iteration pattern, define a reusable `assertAllNodesWithText` helper in the test class (see Template). |
| **One assertion per concept** | Each `@Test` verifies one logical UI contract |
| **Table tests** | Use when the same assertion must hold across multiple inputs. Two patterns are valid — choose based on diagnostic value: **(A) Individual `@Test` functions + private helper** — when each input is a semantically distinct state (e.g. `Loading`, `Error`) and a failing test name alone should identify the problem. **(B) Single `@Test` with a `for` loop** — when inputs are a flat homogeneous list (e.g. all field labels, all field values) and the assertion is structurally identical for each item; the item value itself provides sufficient failure diagnostics. Never use Pattern B when inputs produce structurally different assertions. |
| **When/then naming** | No camelCase, Kotlin backtick names, keep them concise |

---

### Examples in Compose

Each screen exposes two overloads:
- **Public** — resolves ViewModel via `koinViewModel()`, used in production and in **all tests**
- **Private** — accepts `state`, `searchQuery`, `onEvent` directly, used only for Previews

Always test the **public overload**. The ViewModel is mocked via Koin so state is fully controlled.

**State rendering** — each `UiState` variant renders the correct content.
- Selection state → when a UI element can be active/inactive (e.g. a selected tab, a toggled chip), assert `assertIsSelected()` / `assertIsNotSelected()` — not just visibility

**Conditional visibility**
- Enabled/disabled correctly per `UiState`
- Visible/hidden correctly per `UiState` or extra ViewModel property combination

**User interactions**
- Item click → `verify { mockViewModel.onEvent(OpenDetail(id)) }`
- Button click → `verify { mockViewModel.onEvent(ExpectedEvent) }`
- Text input → `verify { mockViewModel.onEvent(SearchQueryChanged(query)) }`
- No-op interaction → when an action should have no effect (e.g. re-selecting the already-active element), verify the event was never fired: `verify(exactly = 0) { mockViewModel.onEvent(ExpectedEvent) }`

---

### Template
```kotlin
import androidx.compose.ui.test.ComposeUiTest
import androidx.compose.ui.test.ExperimentalTestApi
import androidx.compose.ui.test.assertHasClickAction
import androidx.compose.ui.test.assertIsDisplayed
import androidx.compose.ui.test.assertIsEnabled
import androidx.compose.ui.test.assertIsNotEnabled
import androidx.compose.ui.test.assertIsNotSelected
import androidx.compose.ui.test.assertIsSelected
import androidx.compose.ui.test.onAllNodesWithText
import androidx.compose.ui.test.onNodeWithContentDescription
import androidx.compose.ui.test.onNodeWithTag
import androidx.compose.ui.test.onNodeWithText
import androidx.compose.ui.test.performClick
import androidx.compose.ui.test.performScrollTo
import androidx.compose.ui.test.performTextInput
import androidx.compose.ui.test.runComposeUiTest
import io.mockk.clearAllMocks
import io.mockk.every
import io.mockk.mockk
import io.mockk.verify
import kotlinx.coroutines.flow.MutableStateFlow
import org.koin.core.context.startKoin
import org.koin.core.context.stopKoin
import org.koin.core.module.dsl.viewModel
import org.koin.dsl.module
import kotlin.test.AfterTest
import kotlin.test.BeforeTest
import kotlin.test.Test

@OptIn(ExperimentalTestApi::class)
class ExampleScreenTest {

    // -------------------------------------------------------------------------
    // Infrastructure
    // -------------------------------------------------------------------------

    private val mockViewModel: ExampleViewModel = mockk(relaxed = true)

    // -------------------------------------------------------------------------
    // Lifecycle
    // -------------------------------------------------------------------------

    @BeforeTest
    fun setup() {
        // Set default fallback state for all ViewModel properties
        every { mockViewModel.state } returns MutableStateFlow(ExampleUiState.Loading)
        every { mockViewModel.extraProperty } returns MutableStateFlow("")
    }

    @AfterTest
    fun tearDown() {
        stopKoin()
        clearAllMocks()
    }

    // -------------------------------------------------------------------------
    // Helpers
    // -------------------------------------------------------------------------

    private fun launchScreen(
        state: ExampleUiState,
        extraProperty: String = "",
        block: ComposeUiTest.() -> Unit
    ) = runComposeUiTest {
        every { mockViewModel.state } returns MutableStateFlow(state)
        every { mockViewModel.extraProperty } returns MutableStateFlow(extraProperty)
        startKoin {
            modules(module { viewModel { mockViewModel } })
        }
        setContent { ExampleScreen() }
        block()
    }

    /**
     * Scrolls to and asserts [assertion] on every node matching [text].
     * Use when a label appears more than once in the tree (e.g. "Name", "App Icon")
     * and every instance must satisfy the same condition.
     */
    private fun ComposeUiTest.assertAllNodesWithText(
        text: String,
        assertion: SemanticsNodeInteraction.() -> Unit
    ) {
        val count = onAllNodesWithText(text).fetchSemanticsNodes().size
        for (i in 0 until count) {
            onAllNodesWithText(text)[i].performScrollTo()
            waitForIdle()
            onAllNodesWithText(text)[i].assertion()
        }
    }

    // -------------------------------------------------------------------------
    // State rendering — one section per UiState variant
    // -------------------------------------------------------------------------

    @Test
    fun `when ViewModel state is X then correct content is displayed`() =
        launchScreen(ExampleUiState.X) {
            // Given — ViewModel provides X state

            // When
            waitForIdle()

            // Then
            onNodeWithTag(TAG_EXAMPLE).assertIsDisplayed()
        }

    // -------------------------------------------------------------------------
    // Extra ViewModel properties — one section per property
    // -------------------------------------------------------------------------

    @Test
    fun `when ViewModel property is Y then UI reacts accordingly`() =
        launchScreen(state = ExampleUiState.Loaded(...), extraProperty = "value") {
            // Given — ViewModel provides non-empty extraProperty

            // When
            waitForIdle()

            // Then
            onNodeWithText("Element").assertDoesNotExist()
        }

    // -------------------------------------------------------------------------
    // Conditional visibility — table test pattern for repeated assertions
    // -------------------------------------------------------------------------

    @Test
    fun `when ViewModel state is loading then action button is disabled`() =
        assertActionButtonDisabled(ExampleUiState.Loading)

    @Test
    fun `when ViewModel state is error then action button is disabled`() =
        assertActionButtonDisabled(ExampleUiState.Error(cause = null))

    private fun assertActionButtonDisabled(state: ExampleUiState) =
        launchScreen(state) {
            // Given — ViewModel provides a state where the button should be disabled

            // When
            waitForIdle()

            // Then
            onNodeWithContentDescription("Action").assertIsNotEnabled()
        }

    // -------------------------------------------------------------------------
    // Interactions — one test per interactive element
    // -------------------------------------------------------------------------

    @Test
    fun `when user clicks X then ViewModel onEvent is called with X event`() =
        launchScreen(ExampleUiState.Loaded(...)) {
            // Given

            // When
            waitForIdle()
            onNodeWithText("Element").performClick()
            waitForIdle()

            // Then
            verify { mockViewModel.onEvent(ExampleEvent.X) }
        }

    @Test
    fun `when user clicks already active element then ViewModel onEvent is not called`() =
        launchScreen(ExampleUiState.Loaded(...)) {
            // Given — element is already in the active state

            // When
            waitForIdle()
            onNodeWithText("Active Element").performClick()
            waitForIdle()

            // Then
            verify(exactly = 0) { mockViewModel.onEvent(ExampleEvent.X) }
        }
}
```
