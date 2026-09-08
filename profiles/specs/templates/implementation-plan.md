<!--
  Optional — only when the work needs a design or is worth splitting. Shape and change rules:
  `.agents/profiles/specs/rules/on-demand/spec-change-rules.md`'s *Implementation plan*. Delete any heading with
  nothing real under it; Design and Tasks stay.

  A list of several named things (jobs, config blocks, modules), each carrying more than one fact,
  reads better as one bold label per item with its facts as sub-bullets than as a single dense line
  of inline code — the same rhythm Decisions use for Instead of/Because. The same goes for a Task
  that packs a file path, more than one change, and criterion tags into one line: pull each fact onto
  its own bold-labeled sub-bullet instead of blurring them together.

  Tasks and checkpoints: spec-change-rules' *Implementation plan*.
-->

# Implementation plan — {{CHANGE_TITLE}}

## Design
{{How the spec files become true — a sentence for a small change; sub-headings such as ### Flow,
### Interfaces or ### State for a big one, with Mermaid for diagrams.}}
- **Not {{the option not taken}}:** {{why not}}

## Tasks
1. [ ] **{{a short, bolded instruction}}** [AC-{{N}}]
   - **{{File}}:** {{the file it touches}}
   - **{{Add}}:** {{one change, when there's more than one to list}}
   - Check: `{{test name}}` in `{{TestFile.kt}}`
2. [ ] **{{a task that closes no criterion}}**
3. [ ] **Add {{the thing}}**, per Design's *{{section}}*. [AC-{{N}}]
4. [ ] **Verify {{the thing}} for real** — {{what a person does: push a tag, open the MR, run it on
   a device}}.
   - Check: {{what they should see}}

## Not in this change
- {{what a reader would expect here and won't find}}
