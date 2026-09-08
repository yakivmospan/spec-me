# Manual test plan — {{CHANGE_TITLE}}

{{One or two sentences: what needs a real MR, tag push, device or registry that this session can't
reach.}}

1. [ ] **TC-1: {{what it proves, one clause}}**
   - **Preconditions:** {{state the case needs before it starts}}
   - **Steps:** {{what the person does}}
   - **Expected:** {{what tells them it passed}}
   - **Closes:** Task {{N}}. <!-- omit this line where there's no implementation-plan.md -->
   <!-- - **Result:** optional, added once a run has something worth keeping; one sub-bullet per run:
          - {{date}}, {{builds under test}}: {{pass | fail | partly}}. {{what happened}} -->

## Reporting back
Report each case's outcome in any words, naming the case. The checkbox follows the latest run: `[x]`
once it passes, `[ ]` while it fails or hasn't run. A run with more to say — a failure, a note, the
builds — is also added under that case's **Result**: date, builds, pass, fail or partly, and what
happened.
