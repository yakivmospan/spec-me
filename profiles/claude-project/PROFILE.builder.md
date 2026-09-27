# Profile: claude-project

A feature profile, Claude only: a claude.ai project and a repository kept in step. It stays in the
builder and is never installed.

## All or nothing

**This profile installs whole or not at all.** The template without the skill is Instructions nobody
stamps, so the project never learns it is behind; the skill without the rule syncs files whose edits
leave no row, so a sync cannot see them; the rule without the skill offers a snapshot nothing makes.

## What installs

| Block | Lands at |
|---|---|
| `skills/claude-project-sync/` | `.agents/skills/claude-project-sync/`, linked by the sync |
| `rules/on-demand/claude-project-rules.md` | stays here; a line in `.agents/LOADER.md` places it at "touch, edit or propose a change to any file" |
| `templates/PROJECT-INSTRUCTIONS.md` | stays here; the skill copies it into each snapshot |

`.claude-project/SYNC.md` is not installed: the skill's *Link this repo* writes it, from the files
this repository has.

## Detection

None. Chosen by asking whether the user keeps a Claude project for this work.

## Requires

`core`, for `project-context-snapshot`, and `specs`.
