---
name: pin-the-task
description: Use when the user says "pin it", "pin the task", "pin and fold it", "unpin", "resume Task 1", or answers by a pinned id — "1.2 B", "resolve Task 1", "Task 1 rest as recommended" — and when answer-format-rules sends a reply here because it leaves two or more questions open. Keeps a pinned list of open tasks and questions at the end of every reply, updated as the user answers them in any order, so nothing asked earlier is lost up the chat. Not for a handoff to a new conversation (session-snapshot) or remembering a preference across sessions.
---

# Pin the Task

Keeps every open question in sight: a short pinned list under each reply, updated as the user answers
in any order, one aside at a time. What goes wrong most: a pinned line long enough to wrap, and an
item updated from a guess at what an aside meant.

## Non-negotiables

- **While a pin is active, it ends every reply** — a short answer or a side question included — until
  the user says "unpin".
- **Only the user's words close or change an item.** An aside that might touch one is asked about in a
  line, never applied on a guess.
- **Ids never move.** A task keeps its number until it is unpinned; its items keep theirs, closed
  ones included. A new task takes the next number.
- **The pin is the latest state.** Where it and an earlier message disagree, the pin is right, and the
  item says what changed.

## The pin

Under a separator line, in plain italics — no bold anywhere, so the pin sits quietly under the
reply — as a markdown task list so the boxes render:

```markdown
---
*📌 Pinned — reply "3.2 B", "resolve Task 3", or "Task 3 rest as recommended"; a task's start: search "Task <number> starts"*

*⚔️ Main quests*
- *~~Task 1: pin-the-task skill~~ (closed — all ⭐; "show Task 1")*

*Task 3: Setup conflicts*
- [ ] *3.1 · Stale check: offer or run — A rule defers ⭐ · B offer · C leave*
- [x] *▶ ~~3.2 · Who edits a stale spec~~ (A: spec-create edits it)*
- [ ] *⏳ 3.3 · Test run on a device — waiting on Dana*

---
*🧭 Side quests*
- *Task 2: Release checklist (folded — 2.1 A, 2 open; "resume Task 2")*

---
```

- **Tasks:** each headed `Task N: {name}`, numbered from 1 across the pin in the order pinned. Items
  number within their task: 1.1, 1.2.
- **Two groups:** *⚔️ Main quests* — tasks the user pinned; *🧭 Side quests* — tasks pinned
  because a reply left questions open. A task stays in the group it started in.
- **Inside a group:** its folded tasks first, closed and parked alike, one list item each; then its
  open tasks. No separator inside a group: one separator line before each group and one after the
  last. A group with no tasks is left out.
- **Where a task started:** the reply that pins a task opens with `*📌 Task N starts here*`, so
  searching "Task 3 starts" jumps back to it. The pin never writes that phrase with a real number —
  it would match every pin — only the top line's `Task <number> starts`. The chat gives no link to an
  earlier message; never write one.
- **One line per item, about 70 characters, never wrapping:** a title of about five words, then each
  option in one to three words, the recommended one marked ⭐. The full question stays in the
  message that asked it; the pin only names it.
- **States:** `[ ]` open. `[x]` closed — the title struck through, the pick in brackets; a changed pick
  reads "(B, was A)". ⏳ before the title — waiting on someone else. ⚠ — a caution to keep in sight,
  like "don't push before 1.3".
- **Closed items fold** in a task still open: the ones closed before this reply share one line at
  its top, `- [x] *~~4.1 – 4.3~~ (all ⭐; "show Task 4")*`, their picks written as a folded task's
  are. An item closed in this reply keeps its own line until the next, so its pick is seen once.
- **▶** right after the box marks the item the conversation is on now.
- **A task with every item closed** folds into its crossed-out name and keeps its decisions on that
  line: "all ⭐" when every pick was the recommended one, otherwise each id with its pick while that
  fits, otherwise how many were decided. "show Task N" lists its items and picks again, once.
- **A parked task** — "pin and fold it", or "fold Task N" — shows only its heading, not crossed out,
  with what is decided and what is open: `*Task 3: Release checklist (folded — 3.1 A, 2 open;
  "resume Task 3")*`. Its closed items keep their picks while it is folded.
  "unfold Task N" or "resume Task N" opens it again, and resuming moves ▶ to its first open item.

## The header

A reply that moves to a different item — or back to one after a detour — opens with one line naming
it, and the answer starts on the next line:

```markdown
*📍 Working on: 2.3 — pin replaces end status*
```

A reply that stays on the same item carries none; the ▶ shows where things are. A reply about
something outside the pin: `*📍 Working on: side question*`.

## Steps

1. **Start** — on "pin it": pin what the last reply left open, or what the user names; on "pin and
   fold it", pin it parked. On a reply that
   leaves two or more questions open: pin them as a new side quest, parked — the questions sit right
   above it; it unfolds when the user resumes it or answers one of its items. Done when the pin
   ends that reply.
2. **Every reply after** — map what the user said onto items: an id ("1.2 B"), "rest as recommended"
   (each open item in that task takes its ⭐), or plain words plainly about one item. Update the
   states, move ▶, add the header on a switch. Done when the pin matches everything said so far.
3. **A new question mid-work** — add it to the task it belongs to, or pin a new task.
4. **Unpin** — "unpin" drops the whole pin; "unpin Task 1" drops one task, and the others keep their
   numbers.

## When the plan stops fitting

- **An answer could belong to two items** — ask which, in one line, and update neither until told.
- **An item can't be named in about 70 characters** — shorten the title further; if it still can't,
  split it into two items and say so.
