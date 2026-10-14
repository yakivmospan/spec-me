---
name: docs-incode
description: Use after any code change that adds, edits or removes a comment, and before reporting code work done — writing a new function, class or file while implementing a ticket counts, not only an explicit request. Also on "add a comment", "add KDoc", "document this function", "is this comment needed", "these comments are too long", "remove the region markers". Covers KDoc, Javadoc, docstrings, inline comments and region markers, keeping each to what the code alone can't say: a contract, a non-obvious why, a warning. Not for READMEs or ARCHITECTURE.md, specs, or the code itself.
---

# Docs In-Code

A comment states only what the name, type and code can't. What most often goes wrong is a comment
that restates the code — or, once edited, keeps a condition and loses the behaviour.

## Non-negotiables

- **The project's rules and the surrounding file come first — read what `AGENTS.md` loads for this work, if you haven't.**
- **A comment earns its place** — a contract, a non-obvious *why*, or a warning. Otherwise none, and
  none is the default: a private member whose name and body say it all gets no comment, and a *why*
  the code already states — an argument named `userWaiting = true` — is not a why to write.
- **Every name a comment uses is a link** — a state, a type, a member or a constant appears as
  `[ServiceState.READY]` at its first mention in each comment, never as bare `READY`, however often
  the file writes it bare; a bare first mention is a defect. Before reporting, grep the comment lines
  you wrote for a capitalised word outside brackets.
- **A comment changes with its code** — one made untrue is fixed in the same change.
- **No region markers** — never added, not even while working; removed from code being changed.

## Before starting

Write one line: who reads this member, and which words they see. A public member's reader sees the
public surface — states, dialogs, results, the types in the signature — and nothing the class coined
for its insides. A private member's reader sees this file. The comment uses those words only.

## Writing a comment

1. **Delete test** — *would the reader lose real information without this line?* No: delete it. Editing
   an existing comment, test only the sentence you add.
2. **One line if one line does it.**
3. **Plain words, for a reader who knows nothing but this file** — everyday words over formal ones:
   "made before", not "predates"; "use", not "utilise". A symbol's own name stays. Whole sentences
   that name who does what ("the service never shows this dialog", not "no run shows one"), and no
   shorthand from the work that wrote it — a term coined while building, a word the code doesn't
   define. A state, an event, a flag or another class named in a comment is said in words — what it
   means and what it causes — and linked (step 6), never dropped in by its bare name: "the service's
   state goes to [ServiceState.BLOCKED], which stops the assistant", not "BLOCKED is reported". The
   reader is a person opening the file cold, not an agent with half the project in its context. **Test:** read it aloud to someone who has never opened the
   project; anything they'd ask "what is that?" or "where does that happen?" about, or would have to
   read twice, is rewritten.
4. **Behaviour before condition** — say what the member does, then when it no-ops, throws or returns
   empty; never the condition alone.
5. **Doc comments on public API state what callers can rely on**, never how it's built, what it
   hides, or who calls it today: "verifies again as a conversation opens" on a method any caller may
   use describes one caller and misleads the next. They use only words a caller sees — states,
   dialogs, results — never a word the class coined for its insides, however often the file uses it:
   "without starting a run" means nothing outside the class; "with no setup dialog, staying READY"
   does. `@param`, `@return`, `@throws` only when the name and type don't say it.
6. **Link the symbols you name** — `[Symbol]` in KDoc, the doc tool's form elsewhere, first mention per
   comment. Plain text where no link form exists or the symbol can't resolve.
7. **Shape by width** — fits on one line at the width the surrounding comments wrap at: open and close
   on that line. Doesn't fit: the text starts on the next line, each line with its marker, the close on
   its own line. Never open on the first line and then wrap.
8. **Inline comments** follow the same test — a *why*, a workaround, a guarded edge case; never a
   narration of the next line. A test's Given/When/Then markers are structure a project asks for, not
   narration.
9. **A fresh reader before reporting** — a fresh agent, where the tool has them, gets this skill and
   every comment the change adds or edits, and reviews them; fix what it finds. Without one, say the
   pass was your own: a writer passes their own comments.

## Examples

Each pair: the comment as written, then as the steps above make it. They show what a miss looks
like, so the step is recognised in a comment they don't cover; they are not patterns to match.

- **A bare state (steps 3, 6).** `/** Whether the requirements are met; when not, BLOCKED is reported. */`
  → `/** Checks the requirements again and returns whether all are met. When one is missing, the
  service's state goes to [ServiceState.BLOCKED], which stops the assistant. */`
- **The caller instead of the contract (steps 3, 5).** `/** The voice assistant asks it as a
  conversation opens. */` → `/** Checks that the service may still run: its own permissions, and the
  two apps it needs reachable. */`
- **A why the code already says (step 1).** `/** The driver just started a conversation, so an app that
  doesn't answer gets the quick retries Enable gets. */` on a private function whose body passes
  `userWaiting = true` → deleted. Rewording it in plain words was the wrong fix: the argument says it.
- **Its one caller today (step 5).** `/** Verifies the requirements again as a conversation opens. */`
  on a public method of a state manager → `/** Verifies the requirements again with no setup dialog,
  staying READY meanwhile. */`: what it does for any caller, in words a caller sees, not where the
  first caller sits and not the class's own word for its insides ("a run").
- **A public call, in full.** What a doc that passes every step reads like, on a state manager's
  method: `/** Verifies the requirements again with no dialog, staying [State.READY] meanwhile. When
  they are no longer met, calls [onRequirementsNotMet], so the caller can end what it is doing, and
  then moves the state to [State.BLOCKED], which stops the assistant. It never passes through
  [State.INITIALIZING], which would stop the assistant too. Calls that overlap share one verification,
  with the [onRequirementsNotMet] of the call that started it. Starts nothing while the state is not
  READY; a call then only waits for a verification already under way. */` — behaviour, then each
  state named and linked with what it causes, then the edge cases, in words any caller sees.
- **A condition alone (step 4).** `/** Only while READY. */` → `/** Starts the wake word; does nothing
  while the service is not ready, since nothing may listen then. */`
- **Narration (steps 1, 8).** `// reset the counter` above `count = 0` → deleted.

## Reviewing comments

Every comment goes through every step of *Writing a comment*, not only whether it's true — a true
comment can still restate another class, run long, or explain how it's built. One line per finding:
`**defect|risk|clarity** — file:line — what's wrong. Fix: the change.` An untrue comment is a risk;
one failing the delete test is clarity. Asked only to review, report and stop.

## When the plan stops fitting

- **The comment is explaining a bad name or tangled code** — say so; renaming or restructuring is a
  code change, not a comment.
- **The behaviour a comment should state isn't clear from the code** — ask, rather than guess a contract.

## Report

Comments added, changed or deleted, and why; members left without one because nothing passed the
delete test; review findings; anything left because the code needs to change instead.
