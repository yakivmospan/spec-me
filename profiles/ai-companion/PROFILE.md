# ai-companion

How the AI works beside you, day to day: in a way that helps you work better and faster and
understand things better. One person's preferences for the companion itself — how it answers, how it
changes files, when it stops to think again, how it hands work over — not for any project's code.

| What | Kind | For |
|---|---|---|
| `answer-format-rules.md` | always-on rule | answers that read fast: the verdict first, plain words, choices only where yours to make |
| `file-edits-rules.md` | on-demand rule, before touching a file | every change made so it shows as a diff you can review |
| `one-head-good-two-better-rules.md` and its skill | on-demand rule, at a go-ahead with no plan; skill | a second look before acting on a go-ahead or adding scope nobody asked for |
| `design-quality-rules.md` | on-demand rule, before proposing, comparing or reviewing a design | designs that fit the system and last: the flow mapped first, shared types kept general, the codebase's own wiring, a shortcut only when you pick it |
| `ninja-mode-rules.md` | on-demand rule, before a commit message or anything posted to a forge or tracker; placed only in projects where you want it | nothing that leaves the machine shows that an AI helped, unless you say yes |
| `session-snapshot` | skill | a handoff note so work carries on in a new conversation |
| `pin-the-task` | skill, started from `answer-format-rules.md` | open questions pinned in a git-ignored `PINNED.md`, or under every reply, so none gets lost up the chat |
| `write-summary` | skill | a summary of whatever you name — open questions, decisions, how something works today — for its reader, handed over as a file and stored nowhere |
| `decipher-message` | skill | a heavy comment, report or draft retold as what is being asked and the answer, beside the original |
| `CLAUDE-PROJECT-INSTRUCTIONS.md` | text to paste | a claude.ai project's Instructions: these preferences in short, the project's files, and "scan" with a repository folder attached. Kept by hand — changed when you ask |

- **Take what you want.** Nothing here depends on anything else here, except the second-look rule and
  its skill, which go together, and `pin-the-task`, which the answer-format rule starts.
- **Usually yours alone:** install it under `.agents/.local/profiles/`, since these are one person's
  preferences.
- **To place it:** `answer-format-rules.md` goes on the loader's always-on list; the other rules
  are rows at the moments in the table above. For `decipher-message` to run
  on a drafted review comment, reply or spec text without being asked, add an on-demand loader row at
  the step where a draft is shown to you.
- **To remove it:** delete this folder and run `project-sync-profiles-and-skills`; it drops the
  loader lines.
