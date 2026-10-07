# Test E2E — Android reference

Android with UiAutomator, because it drives every app on the device — a client app, another app's
dialog, a system permission prompt — where a Compose or Espresso test sees only its own app. Package
and module names below are placeholders.

## Where the tests live

An instrumented test runs inside the process of the app it targets, so a test in an app's own
`androidTest` dies the moment it stops or clears that app. Cross-app tests go in a test-only module
that instruments itself and drives the apps from outside:

```kotlin
// e2e/build.gradle.kts — apply the Kotlin plugin the way the project's other modules do
plugins { id("com.android.test") }

android {
    namespace = "com.example.e2e"
    compileSdk = <the project's compileSdk>
    targetProjectPath = ":app"
    experimentalProperties["android.experimental.self-instrumenting"] = true
    defaultConfig {
        minSdk = 30 // test names with spaces need 30 or above on Android
        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }
}

dependencies {
    implementation("androidx.test.ext:junit:<version>")
    implementation("androidx.test:runner:<version>")
    implementation("androidx.test.uiautomator:uiautomator:<version>")
}
```

Versions come from the project's version catalog where it has one. `targetProjectPath` names one app
the journey uses, which Gradle installs for a connected run; the test drives every app on the device
either way. Its tests sit in `src/main/`. Since it instruments only itself, its APK needs no particular
signing:
it drives whatever build of the apps is installed, one put on a car by adb included. The on-device
runner runs JUnit4; JUnit5 on a device needs a plugin of its own.

## A written test

```kotlin
@RunWith(AndroidJUnit4::class)
@LargeTest
class FeatureToggleE2eTest {

    private val instrumentation = InstrumentationRegistry.getInstrumentation()
    private val device = UiDevice.getInstance(instrumentation)

    @Before
    fun setUp() {
        // Every test starts from the same state, whatever ran before it
        shell("am force-stop $CLIENT_PACKAGE")
        shell("am force-stop $SERVICE_PACKAGE")
        check(shell("dumpsys account").contains(TEST_ACCOUNT)) { "Sign in $TEST_ACCOUNT on the device first" }
    }

    @Test
    fun `when the feature is turned on then the client shows it ready`() {
        // Given
        launch(CLIENT_PACKAGE)
        device.waitFor(By.text("Enable")).click()

        // When — the other app's dialog is answered
        device.waitFor(By.text("Allow")).click()

        // Then
        device.waitFor(By.text("READY"))
    }

    @Test
    fun `when the dependency is stopped then the client shows it blocked`() {
        // Given
        shell("am force-stop $DEPENDENCY_PACKAGE")
        launch(CLIENT_PACKAGE)

        // When
        device.waitFor(By.text("Enable")).click()

        // Then
        device.waitFor(By.textContains("BLOCKED"))
    }

    private fun launch(packageName: String) {
        val context = instrumentation.context
        val intent = context.packageManager.getLaunchIntentForPackage(packageName)
            ?.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TASK or Intent.FLAG_ACTIVITY_NEW_TASK)
            ?: error("$packageName is not installed")
        context.startActivity(intent)
        device.wait(Until.hasObject(By.pkg(packageName).depth(0)), TIMEOUT_MS)
    }

    private fun shell(command: String): String = device.executeShellCommand(command)

    private fun UiDevice.waitFor(selector: BySelector): UiObject2 =
        wait(Until.findObject(selector), TIMEOUT_MS) ?: error("Not on screen after ${TIMEOUT_MS}ms: $selector")

    private companion object {
        const val CLIENT_PACKAGE = "com.example.client"
        const val SERVICE_PACKAGE = "com.example.service"
        const val DEPENDENCY_PACKAGE = "com.example.dependency"
        const val TEST_ACCOUNT = "e2e-tester"
        const val TIMEOUT_MS = 10_000L
    }
}
```

## Start state by shell

The test's `executeShellCommand` runs as the shell user — the same as `adb shell`.

| To | Command |
|---|---|
| Wipe an app's data | `pm clear <package>` |
| Stop an app | `am force-stop <package>` |
| Grant or revoke a runtime permission | `pm grant <package> <permission>`, `pm revoke …` |
| Keep an app from starting | `pm disable-user --user 0 <package>`, back with `pm enable` — may need root on a locked build |
| Change a setting | `settings put <global\|secure\|system> <key> <value>` |

Anything the shell user can't do fails loudly; report it rather than working around it.

## Install and run without an IDE

```bash
./gradlew :app:assembleDebug :e2e:assembleDebug
adb -s <serial> install -r -t app/build/outputs/apk/debug/app-debug.apk     # skip to test the build already installed
adb -s <serial> install -r -t e2e/build/outputs/apk/debug/e2e-debug.apk
adb -s <serial> shell am instrument -w -e class com.example.e2e.FeatureToggleE2eTest com.example.e2e/androidx.test.runner.AndroidJUnitRunner
```

- **The instrumentation's name:** `adb shell pm list instrumentation`.
- **One test:** `-e class <class>#<method>`.
- **Attach a debugger first:** add `-e debug true`; the run waits until one attaches.
- **The build under test:** `adb shell dumpsys package <package> | grep -m1 versionName`.

## Watching

- **Emulator:** its own window.
- **A device or car:** `scrcpy -s <serial>` mirrors its screen; `--record run.mp4` keeps it.
- **Evidence for a failure:** `adb exec-out screencap -p > failure.png`, and
  `adb logcat -d -v time > failure.log`.

## Driving by adb

| To | Command |
|---|---|
| Read the screen | `adb shell uiautomator dump /sdcard/ui.xml && adb pull /sdcard/ui.xml` — find the node by `text` or `content-desc`, take the centre of its `bounds` |
| Tap | `adb shell input tap <x> <y>` |
| Type | `adb shell input text '<text>'` (spaces as `%s`) |
| Back, home | `adb shell input keyevent KEYCODE_BACK`, `KEYCODE_HOME` |
| Start an app | `adb shell monkey -p <package> 1`, or `am start -n <package>/<activity>` |
| What is on top | `adb shell dumpsys activity activities \| grep -m1 mResumedActivity` |
| Read the app's log | `adb shell date +%s` before the case, `adb logcat -d -T <those seconds>.000 -s <tag>` after — the epoch form has no space, so it also works from a test's shell call. Never `logcat -c`, which wipes the log for everyone on the device |

Dump the screen again after every tap: coordinates from an earlier dump go stale as soon as anything
moves.

## A journey inside one app

The real app, launched in the Compose test runner in its own device tests, with its real dependency
graph — no new module, only the app's UI test library.

```kotlin
@get:Rule val compose = createAndroidComposeRule<ExampleActivity>() // the real app and its real dependency graph

@After fun tearDown() { /* put back what the test changed, e.g. a debug switch */ }

fun ComposeTestRule.waitForNodeWithTag(tag: String, timeoutMs: Long = 10_000): SemanticsNodeInteraction {
    waitUntil(timeoutMs) { onAllNodesWithTag(tag).fetchSemanticsNodes().isNotEmpty() }
    return onNodeWithTag(tag)
}

fun ComposeTestRule.waitForNodeWithContentDescriptionEnabled(description: String, timeoutMs: Long = 10_000): SemanticsNodeInteraction {
    val node = hasContentDescription(description) and isEnabled()
    waitUntil(timeoutMs) { onAllNodes(node).fetchSemanticsNodes().isNotEmpty() }
    return onNode(node)
}
```

- **Real I/O:** wait for content with these before asserting — never assume it loaded at once. Wait for
  enabled where a control stays disabled while data loads.
- **Another environment:** swap it with a module loaded over the app's, override allowed.
- **Install with adb**, as in *Install and run without an IDE* — not `connectedDebugAndroidTest`, which
  uninstalls the app after the run, and its data and sign-in with it.
