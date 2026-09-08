# testing

How tests get written here: unit tests in isolation, integration tests across real components, and
manual test plans for the proof no automated test can reach — a real device, a tag push, a registry.

- **Take what you want.** Nothing here depends on anything else here; delete the skills you do not
  use.
- **Stack-agnostic.** Each skill states its principles for any language, and keeps a concrete
  template for one framework in its `reference.md` — copy the shape, translate the annotations.
- **The `test-writer` agent** writes tests from the code's behaviour in its own context, reading
  whichever of these skills are installed; delete `agents/` to write tests in the main conversation.
- **To remove it:** delete this folder and run `project-sync-profiles-and-skills`.
