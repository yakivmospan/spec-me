# specs

Spec-driven development: specs as the memory every agent reads, kept to the code as it's shaped,
plans for the work worth thinking through first, and the skills, rules, templates and agents that
work them.

- **Whole or not at all.** Its skills, rules and agents are useless apart — a change process with
  no rules, or rules nothing runs.
- **To remove it:** delete this folder and run `project-sync-profiles-and-skills`. Your `.specs/` tree stays; convert it
  first if you want it in another format.
- **Word budget:** `spec-builder-rules.md` 1,200; `spec-change-rules.md` 1,600
- **Self-check:**
  - **Read first:** `.specs/README.md`, the root specs (`.specs/0*.md`) and one open change, if there is one; measure with the two principles `spec-builder-rules.md` adds to the constitution as well. With no `.specs/`, skip every check below and say so, rather than scoring them as missing.
  - **Constitution:** with `.specs/README.md`, `spec-builder-rules.md`, `spec-change-rules.md`, `spec-format-rules.md`, `spec-create`, `spec-plan`, `spec-merge`, `spec-sync-with-code`, `spec-rebuild-overviews` with its script's messages, and the `spec-test-writer` agent open, walk each scenario below.
  - **Constitution:** a Behaviour line the user agreed to has no test behind it — is it complete, with nothing warning, failing or asking for a test?
  - **Constitution:** an agent with none of this setup opens `.specs/README.md` — can it find a file's owner, the tie-break included, read and change a spec, plan, build, fold in and abandon a change, and read every frontmatter value and section a spec uses?
  - **Constitution:** a small tweak while shaping — does anything send it into a change, or ask about specs before the work is done?
  - **Constitution:** someone reshapes the plan or what's built mid-build — does the flow stop building, add a task or add an approval?
  - **Constitution:** fold in partway through a plan — how many questions stand between the request and the user's next task?
  - **Constitution:** does any line, spec content included, argue for a test, check or gate, or defend not having one?
  - **Consistency:** `.agents/README.md` against `spec-builder-rules.md`.
  - **Consistency:** `.specs/README.md` against `spec-change-rules.md`, `spec-format-rules.md`, `spec-create`, `spec-plan` and `spec-merge`, asking of each pair: what counts as approving a plan; when `updated:` moves; what needs a plan and what is shaped in place.
  - **Consistency:** `updated:`, `approved`, ticked and fold in each have one meaning everywhere — folding in is never a git merge.
  - **Load:** a typical task, counted in words — the inventory's every-session number, plus `.specs/README.md` up to `## Change what a spec guarantees`, `.specs/INDEX.md`, the largest `.specs/feature/*.md` standing in for the owning spec, and, for that spec, the ``### [`id`]`` section of `.specs/DECISIONS.md` for each spec in its `parent` chain and its `related` list — the chain followed by `id` across `.specs/**`, skipping `changes/`.
  - **Load:** one spec change end to end, counted in words — a typical task, plus `spec-change-rules.md`, `spec-format-rules.md` and `spec-style-rules.md`, and the bodies, after the frontmatter, of `spec-create`, `spec-plan` and `spec-merge`.
  - **Priority examples:** "merge it" about a merge request triggering a fold-in is High; `updated:` moving on any confirmation in one file and only on a clean check in another is Medium.
