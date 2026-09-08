---
name: one-head-good-two-better
description: Use when the user says "apply", "let's go", "do it", "go ahead" or similar with no plan agreed yet, asks for a second look first, or — mid-task included — before adding real scope to guard against a failure mode nobody reported. Checks the request against the project's rules, a simpler or safer way, or whether the edge case is real, then proceeds, asks one question, or stops with a draft. Not for the go-ahead of an agreed plan, in chat or an approved file, comparing designs, reviewing a file, questions, or ordinary mid-task work.
---

# One head good, two better

Before acting on a go-ahead with no agreed plan behind it, take one honest look at what was asked. The
point is catching the few requests that would be built wrong or redone — not reviewing everything.

## Look for

Only these. Anything smaller isn't worth the user's attention.

1. **Breaks the project's own rules** — `AGENTS.md`, `CLAUDE.md`, the rules they load, recorded
   decisions, where the project has them. Name the rule and its file.
2. **Rework ahead** — the request contradicts itself or something agreed earlier in the conversation,
   or leaves open a choice that decides the outcome.
3. **A clearly better way** — much simpler, already in the codebase, or the request treats a symptom.
4. **Hard to undo** — deletes data, touches something shared or outward-facing, a big blast radius
   for a small ask.

Read only what judging needs: the rules already in context, the files the request names. Don't
research.

## Verdict — exactly one

**Go** — nothing above applies. Don't mention the review; do the work.

**Adjust** — the direction is right, and one to three small things would make it better. One short
message, then wait:

> Before I start: {each adjustment, one line}.
>
> Go with these adjustments? I recommend it, because {one clause}.
>
> 1. **With these** ⭐
> 2. **As you asked**

**Stop** — a rule is broken, rework is likely, or there's a clearly better way. Stop:

> 🚩 {what's wrong, in one line}
> - {why — with the rule or file it comes from} (at most three)
>
> A small draft of the other way:
> {5–15 lines — a tree, a sketch, a table: enough to see the difference, not a solution}
>
> Build from this draft? I recommend it, because {one clause}.
>
> 1. **From this draft** ⭐
> 2. **As asked**

## Before you propose one

The same habit turned on your own answer, and the one that is easiest to skip: the first workable
idea arrives before any other, and writing it down feels like deciding. It is not.

- **Find a second way before you name a first.** Two is enough to judge by, never the number you
  show: every option you found goes in the draft, and the lettered choice under it stays the one
  question of direction.
- **Say what each one you turned down costs.** A rejected option with no reason is decoration; the
  reason is the only part the user can argue with.
- **"There is only one way" is an answer. "I did not look" is not.** Where a second genuinely does
  not exist, say so in the same breath, so the user knows the ground was covered.
- **Check before you conclude, not after.** Announcing a verdict and then going to verify it means
  the verdict came from nowhere, even on the occasions it turns out right.

One cheap test: if the answer would be the same had you spent no time on it, you have not compared
anything yet.

## Keep it cheap

- One verdict per request. Once the user answers, do what they chose — no second review.
- The user overruling a flag is an answer, not a new trigger.
- Unsure between Go and Adjust → Go. Unsure between Adjust and Stop → Adjust, unless a project
  rule is broken.
- No praise, no restating the request.
