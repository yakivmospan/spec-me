# Developer setup

A prompt for the builder's developer only — everyone else uses `SETUP.md`. It switches a project
between the **user setup**, the setup alone, and the **developer setup**: the setup,
`.agents/builder/`, and a local rule that makes every setup change in the builder too.

- To switch to the developer setup, with the builder at `.agents/builder/`: *Follow
  `.agents/builder/SETUP-DEV.md`.*
- To switch back: *Follow `.agents/builder/SETUP-DEV.md` — back to the user setup.*

## Switch to the developer setup

If `.agents/.local/profiles/builder-dev/rules/always-on/builder-dev-rules.md` already resolves, the project already has the
developer setup: say so, and stop.

1. **Not set up yet** — `SETUP.md`'s Step 0 reads *Empty* or *Foreign*: follow `.agents/builder/SETUP.md`, keeping
   `.agents/builder/` in its Step 9, then go to step 3.
2. **Already set up** — reconcile the project with the builder, once. Change nothing until the
   developer has chosen.
   1. **Compare.** Pair every file under `profiles/` with its installed copy by the tree in
      `.agents/builder/README.md`: copied files byte for byte, a skill as its whole folder; `.seed.` forms by shape only — sections, questions, fixed text — never the project's
      answers; and a profile file with
      no installed copy, or an installed rule, skill, template or script no profile carries, outside
      `.agents/.local/`. An optional skill or rule not installed for everyone, and an optional rule's
      `LOADER.md` row, isn't a difference.
   2. **Report.** One list: each file that differs, with a one-line summary, and each file on one
      side only. Give the count of identical files without listing them. Nothing records which side
      changed a file, so don't guess.
   3. **Ask**, per file or all at once: **to the builder**, **to the project**, or **skip**. For a
      form, *to the builder* carries only its shape into the `.seed.` block, and *to the project* only
      a missing section or question. Nothing naming this project goes into `profiles/` — say so, and
      skip it.
   4. **Apply** the choices, then rebuild the map: `python3 .agents/core/skills/project-sync-profiles-and-skills/scripts/build_setup_map.py`.
3. **Link the developer rule** — `.agents/.local/profiles/builder-dev/rules/always-on/builder-dev-rules.md` →
   `../../../../../builder/builder-dev-rules.builder.md`, a relative symlink; copy it only where
   symlinks aren't available. It loads from the next session: say so.

## Switch back to the user setup

1. Remind the developer to copy `.agents/builder/` out first — everything developed here is in it —
   and wait for a yes.
2. Delete the folder `.agents/.local/profiles/builder-dev/`, then `.agents/builder/`.
