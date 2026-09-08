# ai-companion

How the AI works beside you, day to day: in a way that helps you work better and faster and
understand things better. One person's preferences for the companion itself — how it answers, how it
changes files, when it stops to think again, how it hands work over — not for any project's code.

| What | Kind | For |
|---|---|---|
| `answer-format-rules.md` | always-on rule | answers that read fast: the verdict first, plain words, choices only where yours to make |
| `file-edits-rules.md` | always-on rule | every change made so it shows as a diff you can review |
| `one-head-good-two-better-rules.md` and its skill | always-on rule, skill | a second look before acting on a go-ahead or adding scope nobody asked for |
| `session-snapshot` | skill | a handoff note so work carries on in a new conversation |
| `pin-the-task` | skill, started from `answer-format-rules.md` | open questions pinned under every reply, so none gets lost up the chat |

- **Take what you want.** Nothing here depends on anything else here, except the second-look rule and
  its skill, which go together, and `pin-the-task`, which the answer-format rule starts.
- **Usually yours alone:** install it under `.agents/.local/profiles/`, since these are one person's
  preferences.
- **To place it:** the three rules go on the loader's always-on list.
- **To remove it:** delete this folder and run `project-sync-profiles-and-skills`; it drops the
  loader lines.
