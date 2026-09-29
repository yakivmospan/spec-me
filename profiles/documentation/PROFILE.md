# documentation

Keeping documentation true as the code changes: comments and doc comments, and the READMEs that name
what a change renamed or added. Also how a write-up for other people reads.

- **Whole or not at all.** `docs-code-rules.md` is what runs the two skills in the middle of other work;
  without it they run only when asked by name or by a request that matches them.
- **To place it:** put `docs-code-rules.md` in the loader at the step where production code is written or
  changed — after a stack's code-style rule there, so its cleanup runs before the comments are fixed.
- **`docs-writeup-rules.md` stands alone:** how a document written for others reads. Put it in the
  loader at the step where such a document is written.
- **To remove it:** delete this folder, run `project-sync-profiles-and-skills`, and it drops the
  loader line.
