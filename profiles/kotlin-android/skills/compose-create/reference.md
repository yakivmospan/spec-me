# Compose — reference

Examples for `SKILL.md`. Names are placeholders for the project's own.

## Template — a new screen

Three files in the screen's package, per *Files*. A larger screen adds one file per sub-component.

`ExampleUiState.kt`

```kotlin
// ImmutableList / persistentListOf come from kotlinx.collections.immutable; use the project's own
// collection type if it has one.

sealed class ExampleUiState {
    data object Loading : ExampleUiState()
    data class Loaded(val items: ImmutableList<ItemUi>) : ExampleUiState()
    data object Error : ExampleUiState()
}

sealed class ExampleEvent {
    data class ItemClicked(val id: String) : ExampleEvent()
    data object RetryClicked : ExampleEvent()
}
```

`ExampleScreen.kt`

```kotlin
@Composable
fun ExampleScreen(
    modifier: Modifier = Modifier,
    viewModel: ExampleViewModel = koinViewModel(), // the project's DI accessor
) {
    val state by viewModel.state.collectAsStateWithLifecycle()
    SideEffects(viewModel.sideEffects) { /* handle side effects */ } // the project's helper
    ExampleScreen(state = state, onEvent = viewModel::onEvent, modifier = modifier)
}

@Composable
private fun ExampleScreen(
    state: ExampleUiState,
    onEvent: (ExampleEvent) -> Unit,
    modifier: Modifier = Modifier,
) {
    when (state) {
        ExampleUiState.Loading   -> LoadingContent(modifier)
        is ExampleUiState.Loaded -> LoadedContent(items = state.items, onEvent = onEvent, modifier = modifier)
        ExampleUiState.Error     -> ErrorContent(onRetry = { onEvent(ExampleEvent.RetryClicked) }, modifier = modifier)
    }
}

@Composable
private fun LoadingContent(modifier: Modifier = Modifier) {
    val loadingLabel = stringResource(R.string.loading)
    Box(modifier = modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
        CircularProgressIndicator(modifier = Modifier.semantics { contentDescription = loadingLabel })
    }
}

@Composable
private fun ErrorContent(
    onRetry: () -> Unit,
    modifier: Modifier = Modifier,
) {
    Column(
        modifier = modifier.fillMaxSize(),
        verticalArrangement = Arrangement.Center,
        horizontalAlignment = Alignment.CenterHorizontally,
    ) {
        Text(
            text = stringResource(R.string.error_generic),
            modifier = Modifier.semantics { liveRegion = LiveRegionMode.Polite },
        )
        Spacer(modifier = Modifier.height(Spacing.small))
        Button(onClick = onRetry) { Text(stringResource(R.string.retry)) }
    }
}

@PreviewLightDark
@Composable
private fun ExampleScreenLoadingPreview() {
    AppTheme { ExampleScreen(state = ExampleUiState.Loading, onEvent = {}) }
}

@PreviewLightDark
@Composable
private fun ExampleScreenLoadedPreview() {
    AppTheme {
        ExampleScreen(
            state = ExampleUiState.Loaded(
                items = persistentListOf(
                    ItemUi(id = "1", title = "Item One"),
                    ItemUi(id = "2", title = "Item Two"),
                )
            ),
            onEvent = {},
        )
    }
}

@PreviewLightDark
@Composable
private fun ExampleScreenErrorPreview() {
    AppTheme { ExampleScreen(state = ExampleUiState.Error, onEvent = {}) }
}

@Preview(fontScale = 2f, name = "Large font")
@Composable
private fun ExampleScreenLargeFontPreview() {
    AppTheme {
        ExampleScreen(
            state = ExampleUiState.Loaded(items = persistentListOf(ItemUi("1", "Item One"))),
            onEvent = {},
        )
    }
}
```

`ExampleItemList.kt` — a sub-component with its own preview, so its own file:

```kotlin
@Composable
internal fun LoadedContent(
    items: ImmutableList<ItemUi>,
    onEvent: (ExampleEvent) -> Unit,
    modifier: Modifier = Modifier,
) {
    LazyColumn(modifier = modifier) {
        items(items, key = { it.id }) { item ->
            ItemRow(item = item, onEvent = onEvent)
        }
    }
}

@Composable
internal fun ItemRow(
    item: ItemUi,
    onEvent: (ExampleEvent) -> Unit,
    modifier: Modifier = Modifier,
) {
    Row(
        modifier = modifier
            .fillMaxWidth()
            .clickable { onEvent(ExampleEvent.ItemClicked(item.id)) }
            .padding(horizontal = Spacing.medium, vertical = Spacing.small) // the project's tokens
            .semantics(mergeDescendants = true) {}
    ) {
        Text(item.title)
    }
}

@PreviewLightDark
@Composable
private fun ItemRowPreview() {
    AppTheme { ItemRow(item = ItemUi(id = "1", title = "Item One"), onEvent = {}) }
}
```

## Non-obvious semantics APIs

```kotlin
// Merge related elements into one TalkBack announcement.
Row(modifier = Modifier.semantics(mergeDescendants = true) {}) { ... }

// Mark a heading so TalkBack users can jump between sections.
Text(modifier = Modifier.semantics { heading() }, ...)

// Expose state on a custom toggle. Strings are resolved outside the semantics block.
val enabledLabel = stringResource(R.string.state_enabled)
Box(modifier = Modifier.semantics { role = Role.Switch; stateDescription = enabledLabel })

// Announce dynamic content updates automatically.
Text(modifier = Modifier.semantics { liveRegion = LiveRegionMode.Polite }, ...)

// Announce form field errors.
val emailError = stringResource(R.string.error_invalid_email)
OutlinedTextField(modifier = Modifier.semantics { error(emailError) }, ...)
```
