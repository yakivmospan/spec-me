# claude-project

A Claude project (claude.ai) and this repository, kept in step both ways: ideas sketched in the
project reach the repository, and what is done here reaches the project. A project can also start
empty and grow a repository later, or never need one. Claude only, for now.

| What | Kind | For |
|---|---|---|
| `templates/PROJECT-INSTRUCTIONS.md` | the project's side | pasted into the project's Instructions, after the snapshot of this setup — how the project chat keeps its files, works with a connected folder, and syncs on "push ideas", "pull updates" or "sync" |
| `claude-project-rules.md` | on-demand rule, before touching a file | every edit to a synced file gets its change row, so a sync can see it |
| `claude-project-sync` | skill | the Instructions to paste, stamped; `.claude-project/SYNC.md` built and checked; what the project wrote turned into proposals |

- **Depends on:** `specs` — the project's Instructions carry the specs profile's rules, and its files
  are specs.
- **State:** `.claude-project/SYNC.md` in the repository — what was last synced, one row per file, and
  the fingerprint of the Instructions last made.
- **To remove it:** delete this folder and run `project-sync-profiles-and-skills`; delete
  `.claude-project/` too if the project is not synced any more.
