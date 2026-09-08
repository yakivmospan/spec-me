# Builder development

Always-on, local — linked by `SETUP-DEV.md` while this project has the developer setup, and
unlinked when it switches back to the user setup.

- **Every change to an installed copied file is made in its profile too**, in the same step — the
  tree in `.agents/builder/README.md` says which profile file. A new shared rule, skill, template or script is added
  to both, and a deleted one deleted from both; one only under `.agents/.local/` stays out of the builder
  unless it came from a profile.
- **A form's shape goes to its `.seed.` file** — a section, a question, fixed text. This project's
  answers never do.
- **What the change means for the builder goes with it** — the README tree for a new or moved profile file,
  `BUILDER-DESIGN.md` for a decision about how the builder works, a `CHANGELOG.md` line for what a
  release brings.
- **Nothing of this project goes into `.agents/builder/`** — no product, module, package or people
  names, ticket keys, real dates, or examples retold from its work. Carrying a change across strips
  them; an example taken from here is retold in a neutral domain.
- **Local and by hand is the intended state.** Running `spec-rebuild-overviews` by hand, no CI job, no hooks —
  none of these is a gap to close or raise.
- **Adding a profile is a re-run of `SETUP.md`; updating files the project already has is not.**
  Adding is supported — Step 0 detects the state and installs on top. Taking newer versions of files
  already installed stays by hand, or by asking an AI to compare. Never suggest update tooling for
  that, and never suggest keeping the builder once the project switches back to the user setup.
- **Don't mention any of this** — it is part of the edit.
