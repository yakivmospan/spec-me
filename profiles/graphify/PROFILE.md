# graphify

Dependency and call-graph questions answered with the [graphify](https://pypi.org/project/graphifyy/)
command-line tool, for a project or a person that uses it.

- **Tool:** the `graphify` command on the PATH. The skill checks and asks before installing it.
- **No rule to place.** `code-query-dependencies` runs only when asked for by name or for graphify,
  on purpose: grep and reading stay the default for structural questions, so nothing triggers it
  mid-work.
- **To remove it:** delete this folder and run `project-sync-profiles-and-skills`.

## Beside graphify's own skill

`graphify install` copies graphify's own `graphify` skill into your personal skills folder
(`~/.claude/skills/graphify/` for Claude), where every project on your machine sees it; with
`--project` it goes into this project's `.claude/` instead, which the sync leaves alone. On request it
also adds a section to a project's `CLAUDE.md` and a git hook that rebuilds the graph. Don't use
`--strict` here: its hook blocks an agent's first file read in a session until a graphify query has
run, which fights every rule and skill that reads files. The two skills answer different needs:

| | `code-query-dependencies` (this profile) | `graphify` (graphify's own) |
|---|---|---|
| **For** | one question about the code: what calls, imports or inherits from X; how A reaches B | building and exploring the whole graph: code, docs, papers, images, the HTML view and the report |
| **Runs** | `--code-only` every time: no model call, nothing leaves the machine | may use a model for docs and images — Gemini with a key, otherwise the session itself and its subagents |
| **Starts** | only when you ask for it or for graphify | on any question about the codebase, whenever `graphify-out/` exists |
| **Size when it runs** | about 300 words | about 5,200 words |
| **Who has it** | whoever has this profile — the team when shared | whoever ran `graphify install` |

- **Ask for this profile's skill** for a quick, private answer about dependencies.
- **Ask for graphify's own** to build or refresh the graph, include non-code files, or get its report.
- **Both installed:** graphify's description claims any codebase question, so ordinary questions can
  drift to it. Name the one you want. If you only ever want the code-only answers,
  `graphify uninstall` removes its skill from every tool it installed into — without `--purge` it
  keeps `graphify-out/`.
