# code-clean-kotlin reference

Worked examples a run opens when a non-negotiable in `SKILL.md` doesn't settle a case on its own.

## Wired, not hardcoded: a limit owned once

Two classes call the same outside app over one connection, and a call to it can hang and hold its
thread. The second class was built by copying the first, private pool included.

Bad — each class bounds its own calls, so a hung app holds four threads, and the copy has to be a
single only to keep its own limit:

```kotlin
class StatusChecker(...) {
    private val calls = CoroutineScope(SupervisorJob() + Dispatchers.IO.limitedParallelism(3))
}

class MapOpener(...) {
    private val calls = CoroutineScope(SupervisorJob() + Dispatchers.IO.limitedParallelism(1))
}
```

Good — the connection owns the one limit, every caller takes it, three threads in all, and the
opener is an ordinary factory again:

```kotlin
object AppConnection {
    val callDispatcher: CoroutineDispatcher = Dispatchers.IO.limitedParallelism(3)
}

class StatusChecker(callDispatcher: CoroutineDispatcher = AppConnection.callDispatcher)
class MapOpener(callDispatcher: CoroutineDispatcher = AppConnection.callDispatcher)
```

The same check catches two clients each building their own HTTP connection pool for one backend, or
two classes each holding their own rate-limit semaphore for one API: the limit belongs to what is
limited, not to whoever calls it first.
