---
name: docs-incode
description: Use after any code change that adds, edits or removes a comment, and before reporting code work done — writing a new function, class or file while implementing a ticket counts, not only an explicit request. Also on "add a comment", "add KDoc", "document this function", "is this comment needed", "these comments are too long", "remove the region markers". Covers KDoc, Javadoc, docstrings, inline comments and region markers, keeping each to what the code alone can't say: a contract, a non-obvious why, a warning. Not for READMEs or ARCHITECTURE.md, specs, or the code itself.
---

# Docs In-Code

A comment states only what the name, type and code can't. What most often goes wrong is a comment
that restates the code — or, once edited, keeps a condition and loses the behaviour.

## Non-negotiables

- **The project's rules and the surrounding file come first — read what `AGENTS.md` loads for this work, if you haven't.**
- **A comment earns its place** — a contract, a non-obvious *why*, or a warning. Otherwise none.
- **A comment changes with its code** — one made untrue is fixed in the same change.
- **No region markers** — never added, not even while working; removed from code being changed.

## Writing a comment

1. **Delete test** — *would the reader lose real information without this line?* No: delete it. Editing
   an existing comment, test only the sentence you add.
2. **One line if one line does it.**
3. **Plain words** — everyday words over formal ones: "made before", not "predates"; "use", not
   "utilise". A symbol's own name stays.
4. **Behaviour before condition** — say what the member does, then when it no-ops, throws or returns
   empty; never the condition alone.
5. **Doc comments on public API state what callers can rely on**, never how it's built or what it
   hides. `@param`, `@return`, `@throws` only when the name and type don't say it.
6. **Link the symbols you name** — `[Symbol]` in KDoc, the doc tool's form elsewhere, first mention per
   comment. Plain text where no link form exists or the symbol can't resolve.
7. **Shape by width** — fits on one line at the width the surrounding comments wrap at: open and close
   on that line. Doesn't fit: the text starts on the next line, each line with its marker, the close on
   its own line. Never open on the first line and then wrap.
8. **Inline comments** follow the same test — a *why*, a workaround, a guarded edge case; never a
   narration of the next line. A test's Given/When/Then markers are structure a project asks for, not
   narration.

## Reviewing comments

One line per finding: `**defect|risk|clarity** — file:line — what's wrong. Fix: the change.` An untrue
comment is a risk; one failing the delete test is clarity. Asked only to review, report and stop.

## When the plan stops fitting

- **The comment is explaining a bad name or tangled code** — say so; renaming or restructuring is a
  code change, not a comment.
- **The behaviour a comment should state isn't clear from the code** — ask, rather than guess a contract.

## Report

Comments added, changed or deleted, and why; members left without one because nothing passed the
delete test; review findings; anything left because the code needs to change instead.
