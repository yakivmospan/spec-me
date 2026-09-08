---
name: session-snapshot
description: Use only when asked to "snapshot", "save our progress", "let's continue this later", "I need a new chat" or similar — writes a short handoff document so work continues in a brand-new conversation, attaching the files the next session needs instead of restating them. Never proactive, never because a conversation looks long. Not for a status summary in chat, recording a decision, or writing a README.
---

# Session Snapshot

**Only run this on direct request.** Do not suggest it, offer it, or produce it because the
conversation looks long or seems to be wrapping up — those are not requests, only the user asking is.

Produces a short markdown document plus a set of attached files — the actual sources the next
session needs, not a paraphrase of them.

## Attach real files, don't re-derive their content

A summary is lossy and can drift from what a file actually says; the file can't. The snapshot
document itself is only for what has no other home yet — decisions or context from *this
conversation* not yet written into any file.

## Which files to attach

- **If this repo has a `.specs/` tree**: identify which specs actually matter to what was being
  worked on — check `.specs/INDEX.md` for anything code-related, or just the specs that came up in
  conversation. Attach those files directly instead of describing their contents. Don't attach the
  whole tree indiscriminately — just what's relevant, so the user can drag-and-drop exactly what's
  needed and nothing else.
- **Any other file discussed or produced in the conversation** — source files, contracts,
  documents, diagrams — same treatment: name it and attach it rather than inlining it.
- If nothing produced or discussed exists as a file yet, there's nothing to attach — that's fine,
  the snapshot document alone covers it.

## What goes in the snapshot document itself

Only what isn't already captured in an attachable file:

1. **The goal.** One or two sentences — what's being built/solved/decided, and why.
2. **Key decisions made in this conversation that aren't yet written anywhere else**, each with
   its rationale. If a decision is already recorded in a spec's Decisions section, don't repeat it
   here — just note which spec has it.
3. **Open questions** raised but not yet resolved — kept clearly separate from settled decisions.
4. **Concrete next steps.**
5. **Which files are attached, and why each one matters** — one line per file, not a restatement
   of its content.

If the session is mid-flight, say so near the top ("Snapshot taken mid-session — the following was
still in progress: ...").

## When to write a full snapshot vs. a quick one

- **Full**: real decisions, a design, code/spec changes, or a multi-step task. Use the structure
  below.
- **Quick**: a simple conversation with no real branching decisions. Use only what applies — don't
  pad with empty headers.

## Output format

Always a markdown file, not inline chat text.

```markdown
# [Project/Task Name] — Session Snapshot

> Snapshot taken: [mid-session, still in progress | end of session]
> To resume: start a new conversation, upload this file plus the attached files below, and say
> what you want to pick up.

## Goal
[1-2 sentences]

## Attached
- `.specs/feature/checkout.md` — the spec being worked on
- `src/checkout/pay.ts` — [why this one, if not obvious]

## Decisions made this conversation (not yet in a spec)
| Decision | Why |
|---|---|

## Open questions
- [ ] ...

## Next steps
- [ ] ...
```

Adapt section names to fit the domain — this skeleton is a default, not a rigid template.

## After writing

1. Present the snapshot file together with every attached file in the same step, using whatever
   attachment mechanism the current tool provides — the point is the user gets everything to
   drag-and-drop in one place, not just the snapshot with a list of paths to go find themselves.
2. Keep the chat reply short: don't restate the snapshot's contents in prose. A one-line
   confirmation plus the files is enough. If mid-session, add a one-line reminder that the user can
   keep working here, or pick up fresh from the files later — their call.

