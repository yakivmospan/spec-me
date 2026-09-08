# {{PROJECT_NAME}}

{{ONE_LINE_DESCRIPTION}}

Specs hold intent. Code holds behaviour. When they disagree, stop and reconcile. How to read and
change a spec, with or without the rules below: `.specs/README.md`.
{{keep this paragraph only if `specs` was chosen; drop it if it was not}}

## Rules

Before doing anything else this session, read `.agents/CONSTITUTION.md`, then `.agents/LOADER.md`,
and follow it. It lists every rule this repository shares. Then read `.agents/.local/LOADER.md` if
it is there — rules someone keeps to themselves, adding to the shared ones, and absent on most
machines.

**Read them again whenever you cannot quote them.** A long session gets compacted, and a file read
by a tool call is not part of what comes back — this file is. If you are unsure what the
constitution or a rule says, open it rather than working from memory of it.

The constitution's core is carried below so it survives that. It is **generated** by
`project-sync-profiles-and-skills` from `.agents/CONSTITUTION.md` — edit it there, never here. Leave the two
markers exactly as they are and run the sync; it fills them. Deleting them is allowed and means this
project does not want the copy — nothing else changes.

<!-- constitution core -->
<!-- /constitution core -->

Stack and commands are in `.specs/02-tech.md`; modules and their boundaries in
`.specs/01-architecture.md`.
{{keep this paragraph only if `specs` was chosen; without it, say where the stack, the commands and
the module layout are actually written down in this repository, or drop the paragraph}}
