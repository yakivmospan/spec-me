---
name: code-query-dependencies
description: Use only when the user explicitly asks to use graphify, or names this skill — answers dependency, call-graph and structural questions (what calls, imports or inherits from something; how one part reaches another) with the `graphify` CLI, scoped to code only. Never proactive. Not for ordinary structural questions, which grep and reading answer.
---

# Code Query Dependencies

**Only on direct request** — the user asks for `graphify` or this skill by name. Grep and reading stay
the default, even for structural questions.

Every call runs with `--code-only`: no model call, and nothing leaves the machine. Output still costs
context, so pick the command from the table on the first try rather than exploring.

## What to do

1. Confirm `graphify` is on PATH. If it's missing, ask before installing it.
2. Build or refresh once per session, or after the code changed: `graphify extract . --code-only`.
3. Pick the narrowest command:

   | Need | Command |
   |---|---|
   | What depends on / calls / imports X (reverse lookup) | `graphify affected "<X>"` (add `--relation`/`--depth` as needed) |
   | How A reaches B | `graphify path "<A>" "<B>"` |
   | Explain one concept | `graphify explain "<concept>"` |
   | A broader natural-language question none of the above fits | `graphify query "<question>"` |

   If unsure of `affected`'s flags, run `graphify affected --help` once and reuse what you learn.
4. Use only the answer returned. Read `graphify-out/graph.json` directly only when no command covers
   the need.

## Why questions

A question about *why* something was built a certain way: where the repository keeps specs, their
Decisions come first; then `graphify explain` — `# NOTE:`/`# WHY:` comments in code are captured even
under `--code-only`.
