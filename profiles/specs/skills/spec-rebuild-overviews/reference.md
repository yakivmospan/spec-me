# Spec Sync — messages

What each message usually means, and its fix. Look a message up here when a report shows it. Drift fails
`--check`; a warning never does.

## Drift

| Message | What it usually means | Fix |
|---|---|---|
| `no frontmatter block`, or `frontmatter missing required key(s)` | a Markdown file under `.specs/` that isn't a spec, or a spec missing `id`/`title` | add the frontmatter, move the file out of `.specs/`, or — for a manual test plan — name it `<spec>.manual-test-plan.md` |
| `duplicate id` | copy-paste from a template without editing `id`, or a new spec in a change reusing an existing id | rename one; ids are unique |
| `multiple root specs`, or `no root spec` | a `parent:` left empty or set to `null` by mistake | give every spec but `product` a parent |
| `parent '<id>' is not a known spec id` | parent renamed or deleted | repoint `parent`, or reparent to `architecture` |
| `related '<id>' is not a known spec id` | a spec was renamed, or the reference was written for a spec that never got created | repoint it, or drop it |
| `parent chain forms a cycle` | two specs point at each other | break the cycle at whichever is conceptually the child |
| `owns '<glob>' matches nothing on disk` | code was moved or deleted, spec was not updated | update `owns`, or delete the spec if the feature is gone — the user's call |
| `ambiguous ownership` | two globs of equal specificity claim the same files | narrow one of them; a file has exactly one owner |
| `has no \`id:\`` | a spec file missing its frontmatter | give it the id — the spec's own for a moved one, a new one for a new spec |
| `.specs/… is still there` | the spec was copied into the change instead of moved, or restored at its place since | `git mv` it: keep the edited file in the change, bring any edit only the one in `.specs/` has into it, then delete the one in `.specs/` |
| `lands at …, which is not under feature/ or contract/, or a root spec` | a spec file name spelling the wrong path, e.g. `specs.features.x.md` | rename it after the path it lands at |

## Warnings

| Message | What it usually means | Fix |
|---|---|---|
| `` no status — add `status: merged` `` | a spec outside `changes/` with no status | add `status: merged` |
| `` is `draft` but sits outside changes/ `` (or `approved`) | a spec in progress written straight into `.specs/` | move it into a change as `specs.<path>.md`, or set `status: merged` if it already describes the code |
| `` no status — add `status: draft` `` | a change spec file with no `status:` | add `status: draft`, or `approved` once agreed |
| `` is `merged` but still in a change `` | a change finished but not merged | merge it with `spec-merge` |
| `unknown status` | a typo, or a value from another process | use `draft` or `approved` in a change, `merged` outside one |
| `no spec files yet` | a folder with an `implementation-plan.md` but no `specs.<path>.md` — not a change yet | add the spec files, or leave it while the change is being shaped |
| `has no \`title:\``, or `has no \`parent:\`` | a change spec file with incomplete frontmatter | add it before merging |
| `both hold .specs/…` | two open changes each holding the same spec, moved or new | fold one in first, then move it into the other |
| `has no \`Instead of\`` | a Decision naming nothing it rejected — usually a Behaviour rule or a scope note | add what it ruled out, or move it to Behaviour |
| `same decision in two specs` | one choice written in two specs | keep it in the narrower spec, and link from the other |
