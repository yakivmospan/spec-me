---
name: decipher-message
description: Use when the user says "I don't understand this", "decipher", "in plain words", "explain like a person", "what are they asking" or "what does this comment mean" about a review comment, an agent's report or your own draft, and when a loader line sends a drafted review comment, reply or spec text here before the user sees it. Rewrites it as what is being asked and the answer, in everyday words, printed beside the original. Not for explaining what code does, or writing a review reply from scratch.
---

# Decipher a message

Turns a message written for agents (a review comment, an agent's report, your own draft) into what a
person would say across a desk: what is being asked, and the answer. What most often goes wrong: the
plain version quietly drops a fact, or turns a guess into a certainty.

## Non-negotiables

- **Beside, never instead.** Print the plain version under the original, or under a one-line pointer
  when the original is on screen just above. The user picks which to use; never swap one for the
  other in a post, a file or a draft another skill is holding.
- **Same facts, fewer words.** Every claim in the plain version is in the original, or in code read
  this session that the answer depends on; a fact that doesn't change the answer stays out. Nothing
  softened, nothing dropped that changes the answer. A guess
  stays a guess ("I read this, didn't run it"). Where the original is wrong, say so in a line of its
  own.
- **Code first.** Where the message leans on code you haven't read, read it before writing the
  answer. Still can't tell: say "I don't know" and what would settle it.

## Steps

1. **The question** — "What they're asking:", one to three sentences, the way the person would ask it
   out loud: the worry, not the mechanism. A report or draft that asks nothing gets "What it says:"
   instead. Done when it names no file, class, flag or ticket id, unless the question is about that
   name; a product name people use, like "the Settings app", is fine.
2. **The answer** — "The answer:", two to five sentences: the outcome first, then why, then what the
   original got wrong, if anything. Plain words per `answer-format-rules.md`. Done when someone who
   hasn't opened the code can follow it.
3. **A reply, when there is a thread to answer** — what a person would type: three sentences or
   fewer, with at most one `path:line`, for the one claim a reader would want to check. When another
   skill owns the thread, this reply sits beside that skill's draft as the other option, and keeps
   that skill's writing rules for posted text. Done when it reads aloud without stumbling.
4. **Show both** — the original or its pointer, then the plain version, then the reply. Posting stays
   with whatever owns the thread, behind its own ask.

## When the plan stops fitting

- **The original can be read two ways** — give both readings in a line each and ask which was meant;
  write the answer only for the one confirmed.
- **Staying true needs a caveat** — keep it, as one plain clause. Shorter never beats true.
- **The code moved since the message was written** — say in a clause which version the answer
  describes: the one the message saw, or the one there now, and whether that is committed.

## Report

The original or its pointer, "What they're asking" (or "What it says"), "The answer", then the reply
when there is one. Worked examples, and a plain version that went wrong: `reference.md`.
