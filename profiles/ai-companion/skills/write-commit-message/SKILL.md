---
name: write-commit-message
description: Use when asked to "give me a commit message", "commit msg", "write the commit", "commit this", "is this message good", or when work under way reaches a commit — writes a short commit message someone who knows the product but not this work understands from `git log` alone: a subject saying what the product does differently, and a few bullets of one concrete change each. Not for a merge request description, release notes, or a changelog entry.
---

# Write a commit message

A commit message is read in `git log`, months later, by someone who knows the product but not this
work. Two things go wrong: a list of every edit with the reasons behind it, and lines so short they
mean nothing without the diff.

## Non-negotiables

- **The project's rules and the surrounding file come first — read what `AGENTS.md` loads for this work, if you haven't.**
- **The project's format wins** — subject prefix, bullet verbs, attribution; this skill shapes only
  the words.
- **Every line reads without the diff** — the thing named in product words, never a code name or a
  vague phrase like "can't be asked".
- **Only what a reviewer must know** — at most four bullets, never why, never every edit.

## Steps

1. **Read what changed** — `git status`, then the staged diff, or the whole working tree when nothing
   is staged, changes made before this conversation included. Nothing to commit: say so, and offer a message
   for the last commit, to amend. Done when you can say in one sentence what the product does
   differently.
2. **Subject** — that sentence, in the product's terms, not which code moved.
3. **Bullets** — one per change a reviewer must know, starting with the project's verb (Added, Changed,
   Removed where it has none): the thing, and what it does now, in about ten words — the subject
   already carries the context. Fold a small edit into the bullet it serves; leave out tests, renames
   and formatting unless they are the change. A bullet that says what another bullet's change does on
   success or failure, or that the specs now describe it, is that change restated, not a second one:
   fold it in. Test: does the reviewer learn of a different behaviour from this line alone?
4. **Read it cold** — each line as someone who hasn't seen the code: one that needs the diff gets the
   missing words; one that explains why loses them; one that tells no behaviour another line doesn't
   is folded into that line.

## Examples

Bad — every edit, code names and reasons:

```
PROJ-412: Reworked ReminderScheduler and updated docs

- Changed ReminderScheduler.schedule() to read QuietHoursRepository, because reminders fired at night
- Added QuietHoursRepositoryTest covering overnight ranges and the default
- Changed the reminders doc's rules and history table to match
- Changed formatting in ReminderModule.kt
```

Bad — one change told four times:

```
PROJ-412: Reminders wait until quiet hours are over

- Added a quiet hours check before a reminder goes off, run in the background so the app never waits
- Changed a reminder due during quiet hours to go off when they end
- Changed reminders to stay quiet during quiet hours
- Changed the reminders doc to describe quiet hours
```

Bad — short, but only readable with the diff:

```
PROJ-412: Changed reminders

- Added check
- Changed blocked case to wait
```

Good:

```
PROJ-412: Reminders wait until quiet hours are over

- Added a quiet hours check before a reminder goes off, which holds one due then until they end
- Changed a snoozed reminder to keep its quiet hours after the phone restarts
```

## Report

The message in a code block, ready to paste. Commit only when asked.
