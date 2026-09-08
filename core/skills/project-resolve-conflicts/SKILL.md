---
name: project-resolve-conflicts
description: Use when asked to "verify the rules", "check rules and skills for conflicts", "do these skills overlap", "merge these two skills", after the setup or an optional rule or skill is installed, or when a rule or skill offers it — finds installed rules and skills that say different things about the same point, compete for the same request, or load the wrong way, and walks the user through keeping one, narrowing one or combining both. Not for writing or reviewing one rule or skill (project-create-rule-or-skill), scoring the whole setup (project-test-setup), or a document disagreeing with the code it describes.
---

# Project Rule Verify

Rules and skills are written one at a time, and installed from different places — core, a
profile, only for the user. Each can be right alone and still collide with another. This finds the
collisions and settles each one with the user, in the files themselves: never with a table deciding
which wins.

## Non-negotiables

- **Nothing changes without the user's pick** for that finding; a finding left alone is fine.
- **Every finding quotes both sides** with `file:line`, and names the request or work where they meet.
- **The constitution is never a side to narrow or combine** — a clash with it is settled by bringing the other
  file in line; only a change to the constitution itself is a red flag.
- **A rule and a skill differing or repeating each other isn't a finding by itself** — `CONSTITUTION.md`'s
  *Which instruction wins* settles it. It is one when the skill's advice is wrong everywhere the rule applies.
- **Deliberate repetition isn't a finding:** non-negotiables restating a rule on purpose.
- **Changes follow `project-create-rule-or-skill`** — its model, naming, budget and *Wiring*, block included.

## 1. Inventory

Read both loaders, every always-on and on-demand rule, shared and local, every agent definition, and
every skill's description:

```bash
python3 .agents/skills/project-create-rule-or-skill/scripts/skill_stats.py
```

Done when you can list, for each file, its kind, whether it is core's, a profile's or the user's, and
the loader line or trigger line that reaches it, if any.

## 2. Checks

| Check | A finding |
|---|---|
| **Loading** | A loader line naming a file or skill that is not there; a rule no line places, which never loads; a line listing a skill's `SKILL.md` to read instead of saying to run the skill; one skill triggered from two lines — a rule and a loader, or two of either |
| **Competing skills or agents** | Two skill descriptions, or two agent descriptions, that match the same request with neither's **Not for** excluding it — two profiles each bringing a test-writing agent, say. Confirm with 2–3 realistic requests per pair, with a fresh agent where the tool has one |
| **Conflicts** | Two rules, or two skills, loading for the same work and saying different things about the same point |
| **Duplicates** | The same point in two files, agreeing today — the next conflict |
| **Precedence** | Any file other than `CONSTITUTION.md` ranking rules or skills — except the precedence line `project-create-rule-or-skill`'s *Non-negotiables* allows a code or docs skill; a skill that only reads and reports carries none, which is not a finding |
| **Naming** | A core file naming a profile's rule or skill; a profile naming another profile's — only the loaders name across profiles; `AGENTS.md` is the root pointer, not a rule or skill |

A match on descriptions is only a lead: open both bodies, and report it only if they really claim the same
work or say different things. A profile skill's **Not for** names work, not another profile's skill — it
still excludes. For a skill triggered from two lines, the one to keep is in a rule of its own profile
when that profile has a rule read at that step, in a loader otherwise.

## 3. Report

A table, most serious first — conflicts, then competing skills or agents, loading, precedence, naming,
duplicates: #, check, side A (`file:line`, quoted), side B (`file:line`, quoted), where they meet.
Nothing found: say so, with what was checked, and stop.

## 4. Settle each one

For each finding, a numbered question with lettered options, the recommended one first and why, each
naming the file it keeps:

- **Keep or narrow one side** — the other side's point is removed, or its description's **Not for** excludes the work.
- **Combine** — one file holds both, with a draft of the combined text and where it lives.
- **Leave it** — deliberate, with the reason.

Show the exact before and after for the recommended option. **Wait for the answers.**

## 5. Apply and recheck

Apply only the picked options, each per `project-create-rule-or-skill`'s *Wiring*. Then rerun *Checks* on every
file touched — a fix that creates a new finding is reported, never hidden.

## When the plan stops fitting

- **A merge would move guidance between core and a profile, or between two profiles** — say which
  files would then name which, and ask where it lives.
- **A local file and a shared one disagree** — local rules add to shared ones and never replace one:
  offer to narrow the local file, never to edit the shared one for one user.
- **Merged text would go over `project-create-rule-or-skill`'s budget** — say by how much, and offer what moves to
  a `reference.md` or goes.

## Report after applying

What was checked, each finding with the option picked, the files changed, and anything the recheck found.
