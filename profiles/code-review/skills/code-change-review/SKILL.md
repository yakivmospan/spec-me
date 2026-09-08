---
name: code-change-review
description: >-
  Use when asked to "review this merge request", "review PR 123", "go through the comments on my MR",
  "address the review feedback", or to review a branch before any request exists — runs the change
  through business, technical and security lanes, reports findings as Required / Must to have /
  Cosmetic with `path:line` evidence, and works incoming comments one thread at a time. Every write
  to a forge, tracker or the author's code is gated behind an explicit ask. Not for tidying code as
  it is written, checking a spec against its code, or reviewing a rule or skill.
---

# code-change-review

Reviews one change end to end and posts only the comments the user picked. Two halves: did it deliver
what was asked, and is the code correct, tested and safe.

**The project's rules and the surrounding file come first — read what `AGENTS.md` loads for this
work, if you haven't.** They are what the technical lane judges style and structure against.

## Three modes, one standard

- **Request mode:** a merge or pull request exists. Findings live in the conversation; no file
  deliverable.
- **Local mode:** the branch has no request yet. Same lanes, same evidence bar, judged against the
  target branch. `reference.md` has the freeze, the loop and the verdicts. Never open a request just
  to review local code.
- **Response mode:** the request already carries someone else's comments. Work them one thread at a
  time, each through the same three gates, each ending in a reply that says what you did and why.
  The one mode that may change the author's code, per fix and per approval. `reference.md` has the
  loop and the reply contract.

Reads of the forge, the tracker, the source and documentation are authorized in every mode.
Validation runs in an isolated copy, never in the author's checkout.

## Gate 0: no external write without asking. Ever.

- Reads need no approval.
- ANY write — a comment, a reply, a resolve, an approval, a label, a merge, a tracker transition —
  requires an explicit ask first, showing the exact body and anchor of every item, and posting only
  what the user selects. Never post then ask; rewording something posted earlier counts.

## Review manifest, captured before any code is judged

- **Request mode:** project and request id, source and target branches, the base, start and head
  revisions from the request's own diff refs, the pipeline revision and status, and any dirty paths
  excluded from the verdict. Judge against those refs, never the current target branch or a dirty
  checkout.
- **Local mode:** repository, target branch, immutable base, head, and a reproducible snapshot including
  staged, unstaged and new files. Absent request or pipeline metadata is
  `NOT CREATED`, never fabricated.
- **Both:** the ticket and its last-updated time, the version of every requirement document that
  applies, the dependency versions, and **every source that could not be retrieved**. A passing test
  suite is a lead, never a substitute for reading the code and the requirements.

**The main session fetches the sources; a lane has no tracker or wiki access and reads only what
the manifest carries.** Fetch each document once and pass its content in the lane's prompt. Where
the project names no source, ask once; none at all is valid, and the business lane reports scope as
unverifiable rather than inventing criteria.

## Lanes

The three lanes cover the whole diff in context, not only the files a plan named or the last fix. On
a small change the main session runs all three itself; otherwise run `code-reviewer-business`,
`code-reviewer-technical` and `code-reviewer-security` in parallel, read-only, each with the manifest. A local
review always uses a reviewer that did not author the candidate. The main session verifies
load-bearing anchors, removes duplicates and owns the verdict.

## Categories, and the three gates that come first

- **Required** — blocks the merge: a broken build or failing pipeline job, a real defect with a
  concrete failure path, or a scope gap against the ticket or its requirement documents.
- **Must to have** — should land but does not block: threading and dispatcher choices, performance and
  log volume, architecture and module boundaries, missing tests for new logic.
- **Cosmetic** — style, naming, formatting, doc wording. Never blocks.

One category per finding, never a range. Severity comes from impact, not effort.

Before anything may be Required, in this order:

1. **Pre-existing?** Diff the offending lines against the immutable base, never the dirty tree. Already
   there, and the finding's title starts with `[pre-existing]`, it can never be Required here, and the
   disposition is a follow-up. Say so in the first sentence, for scope gaps as much as defects.
2. **Reachable?** A defect the shipped build cannot execute is never Required, however real.
   Follow the whole chain on the target branch: who constructs it, who injects it, who calls it, **and
   the capability or feature flag guarding that call site**. Say it as a release risk instead, and name
   what will make it reachable. **Unreachable expires:** when a build is cut, re-validate every defect
   deferred as inert.
3. **Proven?** An INFERRED finding can never be Required. **PROVEN is the exact code or document
   read this session, or something you ran; INFERRED is anything you reasoned to without doing
   either.** A conclusive read is proof, which is why a Required comment may say "I read this rather
   than running it". Where the read leaves a step unproven, downgrade it or prove it — the cheapest
   proof is a probe test that asserts the buggy behaviour and passes. Red-then-green is only needed
   for a code suggestion you post.

## What gets posted

Only what affects the functionality a user experiences, plus a real scope gap. Diagnostics, test gaps,
doc wording and style stay in the report unless asked. When in doubt, fewer threads: each is an
implicit demand for a reply.

## Comment contract

One finding per comment. Every part below that has something to say, and no more:

```markdown
**Required:** one line saying what goes wrong, as the harm, not the mechanism.

- **What happens:** the case in plain prose, three or four sentences. **No `path:line` and no internal
  names here:** someone who has not opened the code follows the story, or it has not been told.
- **Why now:** only where the change is what makes this reachable. What used to catch it, and what
  removed that.
- **Where to look:** a `path:line` for each step of the story, gathered here rather than scattered
  through it, and how you know: "I read this rather than running it", or "I ran a probe and it ended
  READY".
- **Source:** the ticket with a link, or the spec with its file and date. Both when they disagree.
- **Possible fix:** the smallest change. **Possible improvement:** where nothing is broken.
```

- Open every posted comment with `> 🤖 **Self AI Review**`, a block quote on a line of its own.
  Below it the category prefix is the only heading. No praise boilerplate, no severity rationale:
  both live in the report.
- Friendly and direct: first person for what you did, second person for what the author decides.
  Whoever uses the product is "the user", never "you", and their actions are named as the events they
  are ("user switched"), never narrated as instructions. "Possible" softens the remedy, never the
  finding.
- **Every part stands alone.** The headline and each bullet are read as separate units, so a pronoun
  or a "that question" reaching back into another one arrives with nothing to point at. Name the thing
  again where it is used.
- **Write for someone who has not read the code.** A state, an enum or a flag by its own name says
  nothing to them: say what it means. Give every verb the actor it belongs to, and open with the harm
  rather than with what the code failed to do.
- **Shorter is never the goal, clearer is.** Cut what repeats, what the thread already holds, and what
  the reader can see for themselves. Never cut what they need to follow it: a trimmed comment that no
  longer makes sense costs more than the long one did.
- No em dash or en dash anywhere in a posted comment. Commas, colons or parentheses instead.
- 100% certain only: code read this session, or a document fetched this session. Anything softer stays
  in the report. Phrase non-deterministic behaviour honestly: "can be delivered twice", never "always".
- **Source names the document, never a bare criterion id:** a spec can override a criterion on
  purpose. `reference.md` works one through.

## Code suggestions

Only with red-then-green, run through the project's own runner in an isolated copy. Without it, give
the remedy in prose and name the missing validation; a snippet labelled "example" is not an exemption.
Where a Required or Must-to-have fix is small and self-contained, prefer a suggestion block over prose.
`reference.md` has the full contract.

## Workflow

1. **Gather, read-only.** The diff in context; the ticket, its criteria and sibling tickets that might
   overlap; the requirement documents the project names; the baseline files at the target revision. In
   request mode also the existing threads and the pipeline.
2. **Business lane.** One row per scope item and per criterion: Done, Partial, Missing or Beyond
   scope, each with evidence. Name every overlap with another ticket.
3. **Technical lane**, in this order: correctness and concurrency (walk every mutation site before
   claiming a race or its absence); architecture and module boundaries; tests against criteria,
   separating what is asserted from what merely executes; performance; algorithm; readability.
4. **Security lane, never folded into correctness.** Its own pass over authorization, surfaces that
   cross a process or network boundary and the validation on them, secrets in logs and artifacts,
   storage, trust boundaries, supply-chain changes, unsafe defaults and resource exhaustion. Trace
   only reachable paths; never invent a vulnerability.
5. **Ground every guideline claim in a document fetched this session** at the repository's dependency
   version, linking the section, not a homepage. Never quote one from memory.
6. **Report in chat.** Verdict and two or three lines of rationale, the scope matrix, an index table
   of findings (id, category, one line, anchor, PROVEN or INFERRED), then each finding's evidence and
   its ready-to-paste comment body. Close with what was checked and cleared.
7. **Approval gate.** Present the exact bodies and anchors and ask which to post. Default: Required yes, Must to have yes unless the change is time-critical, Cosmetic no.
8. **Post, then verify.** Inline threads on the diff line, at most one top-level note. Re-list them
   afterwards and show the final anchor table. Report outcomes faithfully, partial failures included.
   Then tick `Self AI Reviewed` in the request's description, naming the lanes and their models.

## Close-out checklist

- [ ] Every posted comment: provenance line, category prefix, dash-free, evidenced, link where due.
- [ ] Every finding in the report with its category, anchor and verbatim comment body.
- [ ] Nothing written to the forge or the tracker without an explicit selection this session.
- [ ] Final comment state re-listed and shown to the user.
- [ ] All three lanes covered, the clean ones recorded, the manifest stated.
- [ ] Every posted suggestion carries its executed red-then-green proof, or it was not posted.
