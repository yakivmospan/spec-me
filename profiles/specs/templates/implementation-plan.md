---
status: draft
---

<!--
  A change is this one file: what will be done. Specs stay in `.specs/` and are updated in place as
  each task lands. Shape and change rules: `.agents/profiles/specs/rules/on-demand/spec-change-rules.md`.
  Delete any heading with nothing real under it; Requirements and Tasks stay.

  A list of several named things (jobs, config blocks, modules), each carrying more than one fact,
  reads better as one bold label per item with its facts as sub-bullets than as a single dense line
  of inline code — the same rhythm Decisions use for Instead of/Because. The same goes for a Task
  that packs a file path and more than one change into one line: pull each fact onto
  its own bold-labeled sub-bullet instead of blurring them together.
-->

# Implementation plan — {{CHANGE_TITLE}}

## Requirements
{{Why this work, in a sentence or two.}}

**{{A topic, as the user would name it}}**
- {{what must hold once it's built — a rule, an edge case, a failure path}}

**Open questions**
- **{{undecided}}** — **Action:** {{who decides what}}

Specs it touches: `{{feature.x}}`, `{{contract.y}}`

## Findings
- **{{what was found}}** ({{date}}, {{where — on a device, in a log, from another team}}): {{what
  really happens}}

## Design
<!-- A small change: Overview and Alternatives considered, nothing else. A bigger one, or a plan in
     stages (one ### per stage): the #### parts below, each kept only when it has something real.
     Written for someone joining cold: why and what before how. -->

#### Context
{{Which Requirements topic this builds — the goals are there, the non-goals under Not in this change
— then what the code does today and any outside fact the design rests on: an interface someone else
ships, a measured limit. Two to five lines.}}

#### Overview
{{One paragraph: which piece does what, where it lives, and the existing pattern it follows.}}

New pieces are green, changed ones yellow, deleted ones red.

```mermaid
flowchart LR
    subgraph moduleA["{{module}}"]
        A[{{Caller}}] --> B[{{NewPiece}}]
    end
    subgraph moduleB["{{module}}"]
        C[{{Existing}}]
    end
    B --> C
    classDef new fill:#d4f7d4,stroke:#2e7d32
    classDef changed fill:#fff4c2,stroke:#b8860b
    classDef deleted fill:#f8d4d4,stroke:#c62828,stroke-dasharray:4
    class B new
```

#### Scenarios
**{{The main path, in the user's words}}**
1. {{what the user does}}
2. {{what each piece does, in order, named}}
3. {{what the user sees at the end}}

**{{Another path}}** — {{how it differs from the main one, in a line or two}}

#### Detailed design
**`{{Piece}}`** — {{module}}, {{new / changed}}
- **Responsibility:** {{one sentence}}
- **Interface:**
  ```{{language}}
  // each new or changed call between packages or layers, as a signature
  ```
- **Behaviour:** {{a few lines, or pseudo-code where the logic isn't obvious; a table where it maps
  one answer to another}}
- **Failures:** {{what can go wrong and what it answers}}

#### Cross-cutting
- **Threading:** {{}}
- **Compatibility:** {{old versions, other apps, modules and build}}
- **Testing:** {{where the tests are listed}}

#### What changes
| | Where | What | Why not an existing piece |
|---|---|---|---|
| Added | {{module, package}} | {{new class, object or function}} | {{the existing piece that could hold it, and why it can't}} |
| Changed | | | |
| Deleted | | | |
| Reused | | | |

#### Alternatives considered
- **Not {{the option not taken}}:** {{why not, in a line}}

## Tasks
- [ ] **1. {{a short, bolded instruction}}**
  - **{{File}}:** {{the file it touches}}
  - **{{Add}}:** {{one change, when there's more than one to list}}
  - Check: `{{test name}}` in `{{TestFile.kt}}`
- [ ] **2. {{a task with nothing to check on its own}}**
- [ ] **3. Add {{the thing}}**, per Design's *{{section}}*.
- [ ] **4. Verify {{the thing}} for real** — {{what a person does: push a tag, open the MR, run it on
  a device}}.
  - Check: {{what they should see}}

## Not in this change
- {{what a reader would expect here and won't find}}
