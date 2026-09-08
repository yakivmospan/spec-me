# Unit test templates

Copied from the skill body unchanged. Kotlin, because that is what they were written for —
the structure is the point, not the annotations. Translate to the framework this project runs.

## Tech Stack

This skill assumes `kotlinx-coroutines-test`, `mockk`, and robolectric — confirm against this
project's actual configured stack, including whether it's JUnit4 or JUnit5.

---

## Template — JUnit4

A one-time shared rule, defined once in a test-utils source set — not repeated per test class.
JUnit4 has no `@BeforeEach`/`@AfterEach` to hook class-wide setup into, so a `TestWatcher` rule is
what avoids repeating `Dispatchers.setMain`/`resetMain` by hand in every class's `@Before`:

```kotlin
@ExperimentalCoroutinesApi
class MainDispatcherRule(
    private val dispatcher: TestDispatcher = StandardTestDispatcher()
) : TestWatcher() {
    override fun starting(description: Description) {
        Dispatchers.setMain(dispatcher)
    }
    override fun finished(description: Description) {
        Dispatchers.resetMain()
    }
}
```

The per-class template. `@RunWith(RobolectricTestRunner::class)` is required for Robolectric under
JUnit4 (there's no `@ExtendWith`-style opt-in the way JUnit5 has) — drop it if a given test class
doesn't need Robolectric:

```kotlin
@RunWith(RobolectricTestRunner::class)
@OptIn(ExperimentalCoroutinesApi::class)
class ExampleTemplateTest {

    @get:Rule
    val mainDispatcherRule = MainDispatcherRule()

    private val testDispatcher = StandardTestDispatcher()
    private val testScope = TestScope(testDispatcher)

    // Mocked dependencies/constants/variables go here

    @Before
    fun setup() {
        // Initialize mocked dependencies/variables here.
        // MainDispatcherRule already called Dispatchers.setMain — don't repeat it here.
    }

    @After
    fun tearDown() {
        clearAllMocks()
        // Any additional clean ups.
        // MainDispatcherRule already calls Dispatchers.resetMain automatically.
    }

    // If possible and suitable, create default mocks to avoid duplication
    private fun successResult(output: ..) = {}
    private fun failedResult(error: Throwable) = {}
    private fun mockDefaults() {
        every { .. } returns successResult(..)
        every { .. } returns successResult(..)
    }

    @Test
    fun `when all commands succeed then returns correct value`() = runTest {
        // Given

        // When

        // Then
    }

    @Test
    fun `when command fails then it throws exception`() = runTest {
        // Given

        // When

        // Then
    }

    // Other groups follow the same logic
}
```

## Template — JUnit5

Robolectric under JUnit5 needs its Jupiter extension registered on the class — the exact
annotation/extension class name has changed across Robolectric versions, so verify it against
whatever Robolectric version this project actually has configured, rather than trusting this
literally; the shape is right even if the exact name has moved on. Drop it entirely for a test
class that doesn't need Robolectric:

```kotlin
@ExtendWith(RobolectricExtension::class) // verify this class name against your Robolectric version
@OptIn(ExperimentalCoroutinesApi::class)
class ExampleTemplateTest {

    private val testDispatcher = StandardTestDispatcher()
    private val testScope = TestScope(testDispatcher)

    // Mocked dependencies/constants/variables go here

    @BeforeEach
    fun setup() {
        Dispatchers.setMain(testDispatcher)
        // Initialize mocked dependencies/variables here
    }

    @AfterEach
    fun tearDown() {
        Dispatchers.resetMain()
        clearAllMocks()
        // Any additional clean ups
    }

    // If possible and suitable, create default mocks to avoid duplication
    private fun successResult(output: ..) = {}
    private fun failedResult(error: Throwable) = {}
    private fun mockDefaults() {
        every { .. } returns successResult(..)
        every { .. } returns successResult(..)
    }

    @Test
    fun `when all commands succeed then returns correct value`() = runTest {
        // Given

        // When

        // Then
    }

    @Test
    fun `when command fails then it throws exception`() = runTest {
        // Given

        // When

        // Then
    }

    // Other groups follow the same logic
}
```

---

