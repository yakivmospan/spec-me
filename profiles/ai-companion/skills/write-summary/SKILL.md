---
name: write-summary
description: Use when asked for "a summary of …", "summarise the open questions" or "the decisions" for a topic, "all open questions related to …", "what do we need to ask other teams about …", or "something I can send to the … team" — writes whatever the user names (open questions, decisions, how something works today, cases a team must handle) from the specs, the code and this conversation, in plain words, handed over as a file, stored nowhere. Not for one message in plain words (decipher-message), a handoff to a new conversation (session-snapshot), or the generated spec overviews.
---

# Write summary

A summary is only as good as its sources: the specs, the code, and what this conversation decided.
What goes wrong most: a decision that lives only in the chat, left out or quietly contradicted, and
internal names left in for a reader who can't look them up.

## Non-negotiables

- **The project's rules and the surrounding file come first — read what `AGENTS.md` loads for this work, if you haven't.**
- **Only facts that are true.** Every "how it works today" is checked in the code; one that can't be is
  attributed to its source ("seen on a car"), never guessed. What still happens today stays, even when
  an analysis found it.
- **For a reader outside the team, nothing internal:** no criterion ids, spec, file, class, function or
  test names, code calls, version labels or constant-style names, no design point still open inside the
  team, no history of how we got here. Links go to the tracker only. The reader's own words stay — a
  value in an API they use, a message format they receive, a label on their screen; a call is named by
  the action they know it as, a new version by what it brings, an app by what it is.
- **Stored nowhere, sent nowhere.** The summary is a file in the session's scratch space, handed to the
  user; it goes into the project only when they ask, where they say. Sending or posting it is theirs.

## Steps

1. **Pin the ask** — the kind (open questions, decisions, how it works today, cases, or what the user
   names), the topic (a feature, a contract and the specs its `related:` names, a change), and the
   reader (a team outside, our own team, the user). Missing: ask once, in one line. Done when all three
   are named.
2. **Chat decisions first** — list what this conversation decided about the topic that the specs don't
   hold yet, and offer to write it into the specs before summarising. On a no, the summary uses it
   anyway, as decided, never cited to the chat.
3. **Gather** — rebuild the project's generated spec overviews where it has them, then take what the
   kind asks for from the topic's specs and their copies in open changes. For questions: only
   unresolved ones, each with an owner — the team its Action asks, or, for our own check, the team the
   answer finally comes from; one only our team can answer stays out. Merge two only when one answer
   settles both.
4. **Check** — for each item, read the code it leans on and write down how it works today, starting with
   what goes wrong for the user now, if anything. Planned work is written as planned, with its ticket.
   Where the code disagrees with a spec, the summary follows the code and the report says so.
5. **Write** — in the shape `reference.md` gives for the kind, with its template in `templates/`. About
   150 words an item, plus any table; over that, cut before handing over.
6. **Plain words** — run the `decipher-message` skill on the draft, and take its plain version wherever
   it reads better without losing a fact.
7. **Scan** — search the draft for everything the non-negotiables keep out: ids, spec words, file and
   code names, calls with brackets, version labels, `ALL_CAPS_WITH_UNDERSCORES` names the reader doesn't
   type. Replace each with the reader's words. Done when none is left.
8. **Hand over** — save it in the session's scratch space as `<topic>-<kind>.md`, in kebab case, and
   give it to the user.

## When the plan stops fitting

- **Something already answered in the code or this session** — leave it out, say so, and offer to mark
  it resolved in its spec.
- **The user changes an item while reviewing** — change the spec too, on their yes, so the two agree.
- **The code disagrees with a spec** — say what each says, and offer to correct the spec; which side is
  wrong is the user's call.

## Report

The file, the items per group, what was left out or merged and why, the chat decisions used and whether
they went into the specs, every claim attributed rather than checked, and every place the code
disagreed with a spec.
