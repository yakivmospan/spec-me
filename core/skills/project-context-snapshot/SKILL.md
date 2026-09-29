---
name: project-context-snapshot
description: Use when asked to "snapshot the project", "make a context snapshot", "give me instructions I can paste into another chat", "snapshot" a named profile, "snapshot the specs", or when another skill passes a scope — condenses the setup installed here (the constitution, core's rules, each profile's rules and skills) and, where asked, this project's specs into one short text any chat or agent can follow without the repository, with a stamp that shows when it is behind. Not for handing over this conversation, writing a README, rebuilding the spec overviews, or a claude.ai project's Instructions, which are kept by hand.
---

# Project context snapshot

One text that gives a chat with no access to this repository the way this project works, and — when
asked — what the project is. What most often goes wrong: the condensed text gains a rule no source
holds, or keeps a step only a tool can take.

## Non-negotiables

- **Only what the sources say.** Every line traces to a file in the source list; nothing from general
  practice, nothing softened. Shorter never beats true.
- **Made fresh, never from an earlier snapshot.** An old one is a claim, not a source.
- **Written for a chat with no files, scripts, subagents or tools.** A step only a tool can take stays
  out, or becomes one line naming it and where it runs.

## Scope

| Asked for | Sources |
|---|---|
| the project — the default | the constitution, every rule both loaders name, every installed profile's skills, and the project overview |
| named profiles | only theirs — installed, or from `.agents/builder/profiles/<name>/` when the builder is here |
| the specs | the project overview alone |
| a scope another skill passes | exactly its list, and the overview only if it says so |

"Without X" or "without the overview" narrows any of these.

## Steps

1. **Collect the sources the scope names**, in loader order — the constitution first where the
   scope includes it: each rule file the loaders name for the scope's profiles, then the `SKILL.md`
   of every skill folder in those profiles — no loader lists skills. A profile's card, a skill's `reference.md` or templates, and a skill's working
   files (a pin, a cache) are not sources. For the overview: `AGENTS.md`, `.specs/00-product.md`,
   `.specs/02-tech.md`, each feature spec's frontmatter and Intent, and the open questions. Done
   when the list is written down — it is also the stamp's input.
2. **Condense each profile into its own section**, the constitution first where it is in scope:
   - a rule becomes the behaviour it asks for, in short imperative bullets;
   - a skill becomes "when {its triggers}: {its steps a person can follow by hand}";
   - a format stays literal: a block, template or example the source shows in a code block is
     copied whole into one — never retold — and every marker (⭐ ▶ ⏳ ⚠ 📌 📍 and the like) stays
     the character itself, never a word for it;
   - a profile with nothing a chat can do gets one line saying so.
   Done when every source is in a section or named in that line.
3. **The overview**, when in scope: the product in one paragraph, its non-goals, each feature in
   one line with its status, the open questions that block work, the stack in one line, and the
   paths to ask before touching.
4. **Stamp** — run `python3 .agents/core/skills/project-context-snapshot/scripts/fingerprint.py`
   with every source file. The text's first line is
   `<!-- context snapshot · {scope} · {date} · {fingerprint} -->`. The same fingerprint again means
   nothing it came from has changed.
5. **Write and show** — save it to `.agents/.cache/snapshot-{scope}.md`, overwriting an earlier one,
   and show the whole text.

## When the plan stops fitting

- **A named profile is neither installed nor in the builder** — say so, list what is, and stop.
- **The script reports a missing file** — name it, drop it from the sources, and run it again.
- **Two sources disagree** — keep both in the text, marked as a conflict; don't pick one.

## Report

The file's path, the scope, the fingerprint, and one line per section on what it holds — then the
text. Nothing else to decide.
