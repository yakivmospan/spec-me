---
name: remember-mistake
description: Use when the user points at something you produced as wrong — "bad example", "another bad example", "I don't like this", "what?", "this is not clear" at a quoted line — or says "remember this mistake", "don't do this again", "I want us not to make mistakes like this again", "add this to the rules", "learn from this". Fixes the thing pointed at, then finds the rule, skill, agent or memory that governs that kind of work and writes the mistake into it as a check with the real before-and-after as its example, so no later session repeats it. Not for a new rule or skill with no mistake behind it (project-create-rule-or-skill), a preference or fact to remember, or a correction the user says is one-off.
---

# Remember a mistake

A correction that stays in the chat is gone at the next session. This writes it where the work that
went wrong is governed, as a check a cold reader applies plus the real example, so the same mistake
can't come back. What most often goes wrong: the lesson lands as a vague sentence in the wrong file,
true but never checked.

## Non-negotiables

- **The project's rules and the surrounding file come first — read what `AGENTS.md` loads for this work, if you haven't.**
- **A mistake becomes a check, never a note** — a line a reader tests their work against, in the
  section where that check already happens: a non-negotiable, a numbered step, an Examples list.
- **The principle, then the case** — one sentence that covers every instance of the mistake, with
  the real case as its example; a line only this case would trigger is a note, and a chain of cases
  glued to a rule is several notes. The example shows what a miss looks like so the principle is
  recognised in a case it doesn't name; it is never a word to ban or a pattern to match without
  thinking. Test: name a second, different instance the line also catches.
- **The real example, generalised** — the actual before and after from the work, with project names
  and internals swapped for generic ones, since a rule or skill is the same in every project.
- **One home** — the narrowest file already governing that kind of work. Two files saying it is an
  overlap for `project-resolve-conflicts`.
- **A lesson about the craft travels** — a mistake in how code, comments or docs are written goes
  into the skill or method rule that every project installs, and its builder copy, never into a
  project-only rule or this project's memory; only a fact about this repository stays here.
- **Memory only on the user's yes to the exact text** — never saved silently.

## Steps

1. **Fix the instance first** — the line, comment or code the user pointed at is corrected before
   anything is recorded, so the lesson has its real after, through the skill that governs that kind
   of work (a comment: `docs-incode`; Kotlin: `code-clean-kotlin`). A pointer with no words ("what?",
   "bad example") is still a correction: work out what is wrong from the file and the rules, and say
   it back in one line. Done when the user sees the fix.
2. **Sweep the change** — every other instance of the same mistake in the current change is found
   and fixed before anything is recorded: a correction names one line, the mistake is a kind. Done
   when the report can list each instance found, or say the sweep found none.
3. **Pin the mistake** — three lines at most: what was done, what should have been done, why it
   matters. Done when it quotes the user's correction or they agree with the wording.
4. **Find the home.** In this order, stopping at the first that fits:
   1. the skill that was running, or should have been, when the mistake was made;
   2. the rule the loader reads at that step (`.agents/LOADER.md`, then `.agents/.local/LOADER.md`);
   3. an agent whose job it was (`.claude/agents/`, `.codex/agents/`);
   4. memory, only for how to work with this user rather than how to do the work.
   `ls -l .agents/skills` lists the skills and where each really lives; `grep` finds the point
   itself. Done when you can name the file, the section and the line it goes next to. Already there:
   say so, and sharpen that line only if the mistake slipped past it. Nothing fits: stop and offer
   `project-create-rule-or-skill`.
5. **Write it**, in that file's own voice and shape:
   - a skill: a non-negotiable or a step, `**Rule** — why in one clause: bad → good`, and the pair
     under its Examples where it has them;
   - a rule: one line or row shaped like its neighbours;
   - an agent: one line in its instructions;
   - memory: one fact file in the memory folder's shape, shown to the user before it is saved.
   Keep the file inside its budget (`project-create-rule-or-skill`'s *The budget*); over it, move
   examples to its `reference.md`. Mirror the change in the builder's copy where `.agents/builder/`
   holds one; it is a symlink, so look with `ls .agents/builder/` or `find -L`. Done when the new line
   reads as a check and the example is generic.
6. **Prove it sticks** — a fresh agent gets the changed file and the original situation, and must
   produce the corrected result unprompted. Fails: sharpen the line and try once more; still failing:
   say so.
7. **Wire** — a changed file needs nothing; a new skill or rule goes through
   `project-sync-profiles-and-skills` and gets its loader line.

## When the plan stops fitting

- **The mistake came from a rule that is wrong, not missing** — stop and show the rule; changing it
  is the user's call.
- **Two files could both hold it** — take the one read at the moment of the mistake, name the other,
  and offer `project-resolve-conflicts`.
- **The correction is a preference, not a mistake** — say so and offer memory, on the user's yes, or
  the ai-companion rules instead.

## Report

The fix made; the other instances the sweep found and fixed, or that it found none; the mistake in
two lines; the file, section and exact lines written; the builder mirror; the test prompt and what
the fresh agent did; anything not done and why.
