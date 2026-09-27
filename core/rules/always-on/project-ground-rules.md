# Ground rules

Always-on.

| Rule | Detail |
|---|---|
| KISS, always | Code, docs, explanations: the simplest thing that meets the actual requirement — no speculative flexibility, no premature abstraction, no restating the obvious. |
| No guessing | A fact, convention, command or requirement that isn't written down or visible in the code: say "I don't know", name the missing input and ask — never fill the gap with ecosystem defaults. |
| Code first | Before you state, plan on or write down any claim about the code or how the system works today — its behaviour, structure, names, commands, config — check it in the code, before you say it and before you take it back. A spec, doc, comment, changelog, ticket or old test is a claim to check, never the answer, and it may be stale or incomplete. Two that differ — or a file and the code reading it — are a conflict: say so and what each expects; which side is wrong is the user's call, and a warning that they differ doesn't settle it. Something is a bug only once you have seen it fail yourself. The code settles what the system does, not what it should do. |
| Scope | One feature or module per change; touching a second needs a stated reason first. Adding anything beyond what was asked: check the project's stated non-goals first, where it has them. |
