# specs

Spec-driven development: specs as the memory every agent reads, changes that carry their own spec
files, and the skills, rules, templates and agents that work them.

- **Whole or not at all.** Its skills, rules and agents are useless apart — a change process with
  no rules, or rules nothing runs.
- **To remove it:** delete this folder and run `project-sync-profiles-and-skills`. Your `.specs/` tree stays; convert it
  first if you want it in another format.
- **Word budget:** `spec-builder-rules.md` 1,200; `spec-change-rules.md` 1,600
- **Self-check:**
  - **Read first:** `.specs/README.md`, the root specs (`.specs/0*.md`) and one open change, if there is one; measure with the two principles `spec-builder-rules.md` adds to the constitution as well. With no `.specs/`, skip every check below and say so, rather than scoring them as missing.
  - **Constitution:** with `.specs/README.md`, `spec-builder-rules.md`, `spec-change-rules.md`, `spec-format-rules.md`, `spec-create`, `spec-plan`, `spec-merge`, `spec-sync-with-code`, `spec-rebuild-overviews` with its script's messages, and the `spec-test-writer` agent open, walk each scenario below.
  - **Constitution:** a person confirms a criterion by hand, with no test — is it complete, with nothing warning, failing or asking for a test?
  - **Constitution:** an agent with none of this setup opens `.specs/README.md` — can it find a file's owner, the tie-break included, read, change, plan, build, merge and abandon a change, and read every frontmatter value and section a spec uses?
  - **Constitution:** a spec written from existing code — how many questions stand between it and `merged`, and is that the shortest path?
  - **Constitution:** someone changes their mind mid-build — does the flow stop building, or add an approval, beyond what *Back to draft* does?
  - **Constitution:** does any line, spec content included, argue for a test, check or gate, or defend not having one?
  - **Consistency:** `.agents/README.md` against `spec-builder-rules.md`.
  - **Consistency:** `.specs/README.md` against `spec-change-rules.md`, `spec-format-rules.md`, `spec-create`, `spec-plan` and `spec-merge`, asking of each pair: who approves, and what counts as approval — per file, together, by asking to build; when `updated:` moves; what needs a change and what is edited in place, a one-line fix included.
  - **Consistency:** `updated:`, `approved`, `merged`, checked and ticked, and merge each have one meaning everywhere — a spec merge is never a git merge.
  - **Load:** a typical task, counted in words — the inventory's every-session number, plus `.specs/README.md` up to `## Change what a spec guarantees`, `.specs/INDEX.md`, the largest `.specs/feature/*.md` standing in for the owning spec, and, for that spec, the ``### [`id`]`` section of `.specs/DECISIONS.md` for each spec in its `parent` chain and its `related` list — the chain followed by `id` across `.specs/**`, skipping `changes/`.
  - **Load:** one spec change end to end, counted in words — a typical task, plus `spec-change-rules.md`, `spec-format-rules.md` and `spec-style-rules.md`, and the bodies, after the frontmatter, of `spec-create`, `spec-plan` and `spec-merge`.
  - **Priority examples:** "merge it" about a merge request triggering the spec merge is High; `updated:` moving on any confirmation in one file and only on a clean check in another is Medium.
