# Claude project

This repository is kept in step with a Claude project (claude.ai) through `.claude-project/SYNC.md`.
A sync tells which side changed a file by the file's last change row, so a change without a row is
invisible to it.

- **A file `SYNC.md` lists gets a change row with every edit** — a spec's Change history, or for any
  other file a table at its end: `| Date | Change |`. A printed sheet or a data file, which can't hold
  one, is compared by content instead; leave it as it is.
- **A new file under `.specs/`, `docs/` or `print/`** gets a row in `SYNC.md` only on a yes: offer it
  once, when the file is created.
- **A change to a rule, a loader, a skill or the constitution** leaves the project's pasted
  Instructions behind: say so once, and offer the `claude-project-sync` skill's "snapshot for the
  claude project".
- **Never sync from here unasked.** Moving files between the repository and the project is the
  project chat's job, on the user's word.
