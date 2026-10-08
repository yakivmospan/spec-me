---
name: pin-the-rules
description: Use when the user says "pin rules", "pin the rules", "unpin rules", or asks once "which rules did you use", "which skills did you use" — keeps a status at the end of every reply, for the whole session, of which of this setup's rules and skills were loaded, which were used and in which reply, which this reply used and how, and which were missed; asked once, prints it once. Not for open questions and tasks (pin-the-task), rules that contradict each other (project-resolve-conflicts), or proving a rule is followed by scoring sessions (project-test-behaviour).
---

# Pin the Rules

Shows under every reply which of this setup's rules and skills the session has loaded, used and
missed, and when — so a rule that sits unread, or is skipped at its moment, is seen in the reply it
happens in. What goes wrong most: calling a rule used because it was loaded, and leaving a miss out
because nobody asked.

## Non-negotiables

- **Only what happened in this conversation.** Loaded: read with a tool call, or arrived in the
  context — `AGENTS.md`, a skill's text when it ran. Used: it changed something in a reply, and the
  status says what. Never from memory of a rule, never "probably"; unsure means not counted as used.
- **Misses are reported by the agent itself, in the reply it notices them.** A miss is a step reached
  without reading the rule or running the skill a loader line names for it; work a skill's own
  description says to run it for, done without running it; or a rule read and then not followed. It
  stays on the status for the rest of the session, with the reply it happened in.
- **A compaction drops earlier reads.** Rules read before one are listed under *Re-read* until read
  again — never shown as loaded from the summary alone.
- **While on, every reply carries it**, a one-line answer included, until "unpin rules".

## The status

The last thing in the reply — after `pin-the-task`'s pin or its file line, when one is there — under
its own separator, in plain italics, no bold:

```markdown
---
*🧩 Rules — reply 4*
- *This reply: answer-format (choices as a list) · file-edits (SKILL.md via Edit) · project-create-rule-or-skill (Testing step)*
- *Used before: constitution (r1) · one-head-good-two-better (r1) · pin-the-task (r1, r3) · project-workflow (r3)*
- *Loaded, not needed yet: spec-builder · project-ground-rules · project-sensitive-paths · builder-dev*
- *⚠ Missed: project-workflow — r2 ran the build before reading it · code-clean-kotlin — r2 changed Kotlin, not run*
```

- **What is listed:** the constitution, and every rule and skill under `.agents/`, shared and local —
  this skill and `pin-the-task` included. Not `AGENTS.md` or the loaders, which only route, and not
  the tool's own skills or plugins.
- **Names:** a rule by its file name without `-rules.md`, a skill by its name, the constitution as
  `constitution` — used when it decided something in the reply.
- **Reply numbers** count from the session's first reply; each status is the last one's number plus
  one. "r3" is reply 3.
- **This reply:** each rule or skill used in it, with what it changed in two to five words.
- **Used before:** each one used in an earlier reply, with those replies, latest last — four or more
  as a range, "r1–r4, r7". One used now and before sits in both lines.
- **Loaded, not needed yet:** loaded this session, and no reply so far did the work it is for. A
  rule whose work came up and wasn't followed is a miss, never here.
- **Missed:** each miss with its reply and what was skipped; "none" when there is none, so the check
  shows it ran. **⚠ Re-read:** a line only after a compaction, naming what to read again.
- **Short items.** A line may wrap; an item never runs past one clause.

## Steps

1. **Start** — on "pin rules": go over the conversation from its first reply, number the replies, and
   fill every line from what is still visible, misses included. Asked once — "which rules did you
   use" — without a pin: print the status once, in the same shape. Done when the status ends the
   reply.
2. **Every reply while pinned** — before writing it: list what this reply read or ran, and what each
   one used changed. Walk the loader steps this reply reached — `.agents/LOADER.md` and, where it
   exists, `.agents/.local/LOADER.md` — and check each named rule was read and each named skill ran,
   then each skill whose description matches what this reply did; a gap goes under *Missed*. Check the
   always-on rules against what this reply did; one not followed goes there too. Move the last
   reply's *This reply* items into *Used before*. Done when every loaded rule and skill sits in
   *This reply*, *Used before*, *Loaded, not needed yet* or *Missed*.
3. **Unpin** — "unpin rules" stops it; that reply and the ones after carry none.

## When the plan stops fitting

- **The reply count is lost** — a compaction with no status in its summary: say "count restarted
  after compaction" on the header line and number from 1 again.
- **A miss is noticed late** — while pinned, in a reply after the one it happened in: add it with the
  reply it happened in, and say so in the reply's first line. Misses found at *Start* are not late.
