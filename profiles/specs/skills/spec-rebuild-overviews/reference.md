# Spec Sync — messages

What each message usually means, and its fix. Look a message up here when a report shows it. Drift fails
`--check`; a warning never does.

## Drift

| Message | What it usually means | Fix |
|---|---|---|
| `no frontmatter block`, or `frontmatter missing required key(s)` | a Markdown file under `.specs/` that isn't a spec, or a spec missing `id`/`title` | add the frontmatter, move the file out of `.specs/`, or — for a manual test plan — name it `<spec>.manual-test-plan.md` |
| `duplicate id` | copy-paste from a template without editing `id` | rename one; ids are unique |
| `multiple root specs`, or `no root spec` | a `parent:` left empty or set to `null` by mistake | give every spec but `product` a parent |
| `parent '<id>' is not a known spec id` | parent renamed or deleted | repoint `parent`, or reparent to `architecture` |
| `related '<id>' is not a known spec id` | a spec was renamed, or the reference was written for a spec that never got created | repoint it, or drop it |
| `parent chain forms a cycle` | two specs point at each other | break the cycle at whichever is conceptually the child |
| `owns '<glob>' matches nothing on disk` | code was moved or deleted, spec was not updated | update `owns`, or delete the spec if the feature is gone — the user's call |
| `ambiguous ownership` | two globs of equal specificity claim the same files | narrow one of them; a file has exactly one owner |

## Warnings

| Message | What it usually means | Fix |
|---|---|---|
| `` `status` is no longer used — delete the line `` | a spec written under the old process, when specs carried a status | delete the `status:` line |
| `specs no longer move into a change` | a `specs.<path>.md` left in a change folder from the old process | move it back to `.specs/<path>`, keeping its edits |
| `` no status — add `status: draft` `` | an `implementation-plan.md` with no `status:` in its frontmatter; read as draft | add `status: draft`, or `approved` once agreed |
| `unknown status` | a plan's `status:` is a typo or a value from another process; read as draft | use `draft` or `approved` |
| `has no \`Instead of\`` | a Decision naming nothing it rejected — usually a Behaviour rule or a scope note | add what it ruled out, or move it to Behaviour |
| `same decision in two specs` | one choice written in two specs | keep it in the narrower spec, and link from the other |
