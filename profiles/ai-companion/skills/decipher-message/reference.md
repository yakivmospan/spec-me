# decipher-message: examples

Each example keeps the original's facts and loses its shorthand. The names are made up; the shapes
are real ones.

## A reviewer's question, and a draft answer as heavy as the question

**Original comment:**

> This MR removes the in-app consent UI entirely: ConsentScreen (410), ConsentDialog (300),
> ConsentViewModel (190) and all localized PDFs under assets/legal/. After it the app cannot show the
> terms on its own; only AccountHub can, through the sync service. What happens on a device where
> AccountHub is older than this contract, or where the bind is refused? The consent gate is the one
> flow where "no UI at all" is not a safe fallback, and PrefsStore still carries LEGACY_KEY_TERMS for
> the migration, so the old acceptance is remembered but no longer re-displayable.

**Original draft answer:**

> **On a device whose AccountHub predates this contract, or where the bind is refused, sync stays off
> for that account and the worker never starts.**
>
> - **Nothing starts without the new consent.** The worker starts only for an account that finished
>   onboarding and still holds every permission (`IsSyncEnabled.kt:25`, checked by
>   `WorkerStarter.kt:25` before any start). Only an enable call through this service sets that...
> - **The old acceptance is not kept.** `PrefsStore.kt:65` deletes `LEGACY_KEY_TERMS` and the
>   per-account consent keys once, and nothing reads them...

**Plain version:**

> **What they're asking:** we deleted the app's own terms screen, so only AccountHub can show the
> terms now. What if a phone has an older AccountHub that can't? Is the user stuck with no way to
> agree?
>
> **The answer:** sync just stays off on that phone. Only AccountHub can turn it on, and nothing starts
> until it has, so the worst case is no sync, never sync running without consent. The reviewer's
> point about the old acceptance being remembered is wrong: the saved flag is deleted on first start,
> not reused.

**Reply a person would write:**

> Sync just stays off there. Only AccountHub can turn it on, and nothing starts until it has, so a
> phone with an older AccountHub gets no sync rather than sync without consent. The acceptance saved
> by the old screen isn't reused either: it's deleted on first start (`PrefsStore.kt:65`).

## An agent's finding

**Original:**

> F-3 [Must to have] INFERRED — `UploadWorker.kt:88` regenerates the idempotency key
> (`UUID.randomUUID()` at :92) on every attempt; on process death between enqueue and ack,
> at-least-once delivery degrades to at-least-twice under retry. See K4, TC-12.

**Plain version:**

> **What it says:** if the app is killed after sending an upload but before the server confirms it,
> the retry sends it with a new id, so the server can get the same upload twice. Nobody ran this; it
> comes from reading the code.
>
> **The answer:** it matters only if the server doesn't drop duplicates on its own. Worth checking
> before fixing.

## A plain version that went wrong

> **What it says:** uploads get sent twice after a crash.

Shorter, and false twice over: "can" became "do", and the reader no longer knows nobody ran it. The
plain version above keeps both.
