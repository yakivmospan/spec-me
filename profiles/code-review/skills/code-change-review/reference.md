# code-change-review reference

What a run needs beyond `SKILL.md`: the local and response modes, the code-suggestion contract, and
the mechanics of each forge.

## Local mode: reviewing before the request exists

Not a reduced checklist. All three lanes, the same evidence bar, the same comment voice. A passing
criteria check alone is not completion.

### Freeze the candidate

Record repository, target branch, immutable base, head, changed paths, excluded pre-existing dirty
paths, dependency and build configuration, and the versions of every requirement source. Preserve a
reproducible snapshot: an isolated checkout of the head plus the complete candidate, staged, unstaged
and new files included. Do not stage into the user's index, commit, omit untracked files, or copy
secrets into review artifacts.

Review and test in an isolated worktree or copy. Secrets a build needs may be referenced, never
printed or archived with the evidence. Excluded user edits must not influence the tests. Do not race
the review against a moving checkout: compare the candidate identity before and after the checks, and
again before reporting. If it changed, discard the verdict and review the new candidate. A commit
revision alone cannot identify uncommitted work.

### Rounds

1. Run each lane with a fresh agent every round, never by resuming one that already saw this
   candidate. Give each a self-contained, evidence-only prompt: snapshot location and identity,
   immutable base, the raw requirement sources, the criteria, the exclusions. Give intent and raw
   evidence, never the implementer's "done" conclusion. Review the full diff first; supply prior
   findings only afterwards, for closure checks.
2. All three lanes apply at every size. Size changes parallelism, not coverage. Reviewers never fix
   the candidate and never post.
3. The main session verifies load-bearing claims and removes duplicates. Record stable ids with
   category, PROVEN or INFERRED, evidence, trigger, remedy and disposition. Refuting a finding needs
   evidence; "the plan approved it" and "the tests passed" are not refutations.
4. Proven Required and Must-to-have defects, and the regression tests that guard them, go back as a
   precise fix list. Anything needing new scope, a design decision, a dependency or unrelated files
   goes to the user as a decision before any edit.
5. After fixes: targeted red/green tests, re-check every criterion for the changed behaviour and its
   regressions, freeze the new candidate, run a fresh full review. Close an earlier finding only
   against current code. A fix followed only by a criteria check cannot close the loop.
6. Keep `Review loop: iteration k/3` visible in the report. Three rounds by default; a restart or a
   snapshot change does not reset it. At the cap, record what is unresolved and ask for an extra
   round, a replan, a manual takeover, or acceptance with named gaps. Never loop indefinitely, and
   never call a capped run clean.

### Verdicts

- `PASS` — all lanes covered, no unresolved Required or Must-to-have finding, every criterion
  verified, final checks green on the same candidate. Cosmetic items may remain, explicitly deferred.
- `ACCEPTED WITH GAPS` — the user accepted named unresolved findings, failed checks or criteria gaps.
  Carry the impact and the owner into the request description. Never reported as a clean PASS.
- `BLOCKED` — anything else: an unresolved finding, missing evidence, or an exhausted loop.

Deferring a Must-to-have item produces `ACCEPTED WITH GAPS`, not `PASS`. Any source, test, dependency
or formatting edit after the review returns through this loop. Before a commit, compare the content
again; afterwards verify the committed content equals what was reviewed, since hooks can change it.

## Response mode: working the comments on your own request

Someone has reviewed your change and you are answering them. This is the one place this skill may
edit the code it reviewed, and it still edits nothing until you pick the fix.

### Before the first thread

List every discussion at the current head and record that head. A comment describes the code as it
stood when it was written: a rebase, a later commit or another thread's fix may already have moved
the line or closed the point. Re-read what each thread points at before judging it.

A thread marked resolved is a claim, not evidence. Re-check it against the current head, and say
which head you checked and whether the code changed.

### Two ways through the threads

Pick one before the first thread and say which, because they differ in what the request looks like to
everyone else while you work.

**One thread at a time.** Fix it, commit, push, reply with the real revision, resolve, then open the
next. The code and the threads agree at every moment, so a reviewer reading the request mid-flight is
never misled, and each commit carries one finding and can be reverted on its own. It costs a push and
a pipeline run per thread. Take this when other people are watching the request, when the findings are
independent, or when one fix is big enough to deserve its own review.

**Every fix first, then every reply.** Work all the threads, commit one per finding at the end, push
once, then reply and resolve in a single pass. Fewer pushes, one pipeline. Take this when the findings
overlap enough that fixing one changes what you would say about another, or when nobody is reading the
request yet. The cost is real: the threads sit stale while you work, and several fixes ride in an
uncommitted tree where a mistake is harder to unpick.

Either way **the reply still goes last, after its fix exists and is pushed**, and the steps inside a
thread do not change. What changes is only how many threads are open at once.

**A fix often closes a thread it was not aimed at.** Say so on that thread in its own reply and let it
be resolved there; a finding that quietly disappears from the request teaches the reviewer nothing.

**Every push moves the head** and invalidates the anchors you have not used yet, so re-anchor what is
left afterwards: once per thread in the first flow, once at the end in the second.

### Per thread

1. **Explain it before acting on it.** In chat, in plain words: what the reviewer is saying, what the
   code actually does at head, and whether they are right. Quote the line, never your memory of it.
2. **Triage through the three gates**, exactly as for a finding you raise. Pre-existing, unreachable
   or unproven changes what the thread is owed, never whether you answer it.
3. **Classify it, and say which:**
   - **Agreed** — a real problem in this change. Fix it here.
   - **Agreed, not here** — real, but pre-existing, out of scope, or it needs a decision. It becomes
     a ticket or a document change, not an edit.
   - **Already fixed** — head no longer has it. Name the commit.
   - **Disputed** — the code is right. Evidence, not opinion: the document that settles it, or a
     probe that ran.
   - **Yours to decide** — it turns on intent the code cannot settle. Ask, never guess.
4. **Resolve it.** Any of the three below, in this order, and one thread can need all three:
   - **Code.** Only after the user picks the fix. The smallest change that closes the point, one
     commit per thread so the reviewer can follow it, and red-then-green through the project's own
     runner where behaviour changes. Never push.
   - **Documents.** A scope gap, a criterion the code now contradicts, a stale spec, a follow-up:
     draft the ticket body or the spec edit and show it. Filing or editing either is a write and
     waits for the ask, so drafting the two together costs nothing and answers a reviewer who asked
     "is this written down anywhere".
   - **Reply.** What you did and why, posted last, once the fix exists.
5. **Then decide the resolve, per thread.** Resolve what you fixed, and what you closed with
   evidence the reviewer can check. **Never resolve a thread you disputed:** it is their comment and
   theirs to close, and resolving it yourself ends a conversation you just started. Resolving is a
   write like any other.

**Verify a fix with the commands the pipeline gates on, not the broadest task that resembles them.**
A project whose pipeline lints one module will not warn you about the module you broke if you run the
lint covering all eleven and skim the result. The project's own rules usually say which jobs gate a
request and which modules they cover: read that before deciding what counts as green.

**Read that output whole.** Filtering it for the files you expect to be affected only confirms what
you already believe, and a real finding in a file you were not thinking about scrolls past inside an
exit code you have already explained to yourself. Search it for the failure, never for a filename.

### The reply contract

The same voice as a finding: friendly, first person for what you did, no em dash or en dash. Shorter,
because the thread already holds the finding, never at the cost of clarity. **Never give the finding a
part of its own.** The comment is two lines above your reply and they wrote it, so summarising it back
is filler that pushes the part they are waiting for down the page. Saying what a change replaced is not
restating it: that "was" is what a reviewer compares against. Leave out a part with nothing to say. A
reply carries no `🤖` opener, since it already sits under the comment that has one, and a second mark
would put two emoji in one reply.

```markdown
**Fixed in [`abc1234`](link to the commit):** one line saying what changed.

**What I did:**

- **A label for the change.** What it was, what it is now, why, and a `path:line` where there is one.
- **Another label.** One bullet per change, every change in the list.

**Source:** the ticket or the spec with a link, where a document decides it.

👍
```

One change is a sentence after `**What I did:**`, not a list of one. Several are labelled bullets, each
carrying what it was, what it is now and why: without the "was" there is nothing to compare, and a
reviewer cannot tell a fix from a rewrite.

**`What I did instead:` where the first line says you have not fixed it.** One word, and it stops the
bullets reading as the fix they are standing in for. Everything you did belongs in that list, including
a ticket you raised: it is usually the main thing you did, and it is the one people forget to list.

**A ticket you raised yourself is never the `Source`.** Source is the document that decides the point.
A ticket asks, so it is the outcome, and the first line already links it.

The first line carries the outcome, never agreement: `Fixed in`, `Moved to PROJ-1234`,
`Already fixed in`, `Not changing this`, or a plain question where the call is theirs.

**A commit in a posted comment is a link, never a bare hash.** Someone reading the thread should reach
the diff from it without going to look for it, and a hash alone makes them search. Backticks are
usually what breaks this: a forge that turns a bare sha into a reference leaves one inside a code span
alone. So wrap the link around the code span rather than the other way round, and the reference stays
monospace and becomes clickable. The same goes for a ticket: `Moved to PROJ-1234` is a link too.

**No written thank you. One emoji instead, on its own line at the end.** A sentence of thanks on
every thread becomes a signature: a reviewer reading ten of them sees the formula before they see the
answer, and any phrase short enough not to grate is one you would end up repeating. An emoji says the
same thing, carries no false warmth, and costs a line nobody has to read twice.

👍 by default, 🎯 where they found something that would have shipped, ✅ where the fix is already in
and nothing is left on your side. 🎯 wins where both fit: it says something about their review, and ✅
only about your queue. One emoji, never a row of them, and never one inside a sentence.
Nothing at all on a thread you disputed, where 👍 reads as agreement you do not have.

#### Agreeing

> Why is this list built once in `init`? A setting the user changes later never reaches the screen.

```markdown
**Fixed in `a3f21c8`:** the list follows the repository now instead of being read once.

**What I did:** `CartViewModel.kt:64` collects the repository flow instead of reading it once, and
  two tests in `CartViewModelTest.kt` cover a value changing while the screen is open.

👍
```

No Source line, because nothing here turns on a document.

#### Disagreeing

> AC4 says checkout resumes where the shopper left. This restarts the whole flow.

```markdown
**Not changing this:** the flow re-runs from the top on purpose, and you are only asked what is
still missing.

**What I did:** nothing here. I read `CheckoutFlow.kt:112` rather than running it: the flow does
  restart, then skips every answer we already hold, so from the shopper's side it does pick up where
  they left off.
**Source:** [PROJ-218](…) AC4 promises a resume. Our [contract spec](…) Decision (2025-03-14) and
  the [design doc](…) (Draft, 2025-02-20) both say the flow is never resumed from a saved step, and
  they are the later word. Happy to take it back to the ticket if you think the spec has it wrong.
```

That thread stays open afterwards: it is the reviewer's to close, and it ends with no emoji either,
because a 👍 under a paragraph explaining why they were wrong reads as agreement. The offer to take
it back to the ticket is the friendly part here, and it is doing real work.

#### Moved to a ticket, badly and well

> This can run with the fraud check skipped entirely.

Badly:

```markdown
**Moved to PROJ-1234:** we are asking that first, before closing the path that skips it.

- **What you found:** a cancelled run keeps its saved answers, so the next attempt reports `Passed`
  and reaches `CONFIRMED` without the check running. The flag that stopped that is gone in this MR.
- **What I did:** three changes, none of which closes that path on purpose. The legacy caller is
  deleted, so nothing keeps a shared answer any more: the request, the flag, the `isTrusted` state and
  the dialog all go. The two calls are reversed in `Checkout.kt:160`, so the fraud service is asked
  first and the card is saved only once it says yes, which means a refused order never has a card
  stored against it. And a test covers it.
- **Source:** PROJ-1234 asks whether the check is worth keeping.

👍
```

Well:

```markdown
**Moved to [PROJ-1234](link):** I have not fixed this, because the check it skips may not be needed at
all.

**What I did instead:**

- **Asked whether we need the check at all.** It is left over from a closed beta and runs once per
  checkout, so if we drop it there is nothing to fix.
- **Removed the duplicate.** A second screen asked the fraud service the same question and stored the
  answer for the whole account. That, the shared setting and the dialog it showed are deleted.
- **Swapped the order.** We used to save the shopper's card first and ask the fraud service second.
  Now we ask first and save the card only if it says yes, so a refused order never has a card saved
  against it.
- **Added a test** that fails if the order is swapped back.

👍
```

Seven faults, and not one of them is length:

- the outcome line names nothing: "that" and "the path that skips it" point at words in the author's head;
- `Passed`, `CONFIRMED` and `isTrusted` are internal names, and "the flag" and "the legacy caller" are things
  only someone who wrote the change can see;
- `What you found` hands the reviewer their own comment back;
- the changes are one paragraph, so none can be found at a glance and none is set against what it
  replaced;
- `Source` points at a ticket the author raised, which asks rather than decides, and repeats a link the
  first line already carries;
- raising that ticket, the main thing done, is missing from the list;
- the test is a trailing clause, so the one thing stopping the change being undone is the easiest to
  miss.

The good version is barely shorter. It is clearer because every name is the thing it means, every
change is labelled and set against what it replaced, and nothing is said twice.

### Close-out

Re-list the threads and show the final table: thread, classification, what changed, reply posted,
resolved or still open. Threads left open on a dispute are a normal outcome, not a failure. Say what
is now uncommitted in the author's checkout, and never push it yourself.

## A finding, badly and well

The same finding, written twice. Badly:

```markdown
**Required:** an account whose checkout was cancelled at the retry screen reaches `CONFIRMED` on its
next Pay and places the order, with the fraud check never having run for it.

- **What happens:** you enter the card and the address, and both are saved right away
  (`Checkout.kt:99`), before anything is sent. The payment then fails, for any reason. You are left on
  the retry screen. Now switch account, or let the process die. Nothing clears the saved answers,
  because `clearAll` runs only on `Closed`, `Dismissed` or `WindowGone` (`Checkout.kt:166`), and a
  cancelled run reaches none of them. When that account presses Pay again, `Validator` finds nothing
  missing and answers `Passed` (`Validator.kt:43`), so the run places the order and reports
  `CONFIRMED` (`OrderState.kt:220`) without entering `Checkout` at all.
- **Where to look:** `Checkout.kt:153`. I read this rather than running it. At the base revision this
  was covered: the check wrote `isTrusted`, whose stored default is `false`, and the guard refused on
  it. This change removes the write and both readers.
```

Well:

```markdown
**Required:** when checkout is interrupted we never ask the fraud service about the order, so we can
place an order it would have refused.

- **What happens:** during checkout we ask the fraud service whether this order may go through, and we
  ask that nowhere else. The shopper's card and address are saved immediately, so if checkout is
  interrupted (account switched, or the app killed) they stay behind. Next time Pay is pressed there
  is nothing left to ask, so checkout is skipped and the fraud question goes with it. The order is
  placed, and the account is marked trusted for good: every later order from it goes through the
  quick path, which never asks again.
- **Why now:** an account-wide setting used to catch this. The check wrote it, it defaulted to no, and
  orders were refused unless it said yes. This change removes that setting and both of its readers,
  which is the point of the change, but nothing replaces what it was catching.
- **Where to look:** `Checkout.kt:153`, and the comment above it saying an account is trusted only
  through a run that got past the check. I read this rather than running it. The answers are saved at
  `Checkout.kt:99` and nothing clears them on a cancelled run; the next run finds nothing missing at
  `Validator.kt:43` and goes straight to a placed order at `OrderState.kt:220`.
```

Four faults, and the bad one is not much longer:

- the headline opens with the mechanism and three internal names, so the harm arrives last, after the
  reader has already had to decode `CONFIRMED`;
- the story is threaded with six file references, so it is decoded rather than read; moving them all
  into **Where to look** costs nothing and the prose becomes prose;
- the fact that makes this *this change's* problem sits mid-paragraph under a navigational label,
  where nobody looks for an argument. It is its own part, **Why now**;
- the shopper's actions are narrated as instructions to the reviewer ("you enter", "now switch account"),
  which asks them to act out the bug instead of being told it.

The good version also says something the bad one missed: that the skip is permanent for that account,
not a single session. Writing the story as a story is what made the gap visible.

## Writing the Source line

The part that goes wrong. A criterion id alone is not a source, because documents override each other.

Worked example. PROJ-218 AC4 promises "checkout resumes from the step at which the shopper left".
The design doc (Draft, 2025-02-20) and the in-repo contract Decision (2025-03-14) both say the
opposite: the flow re-runs from the top and is "never resumed from a saved step". The code follows the
spec, and for almost every leaving point that still meets AC4, because saved answers are skipped and
the shopper is only asked what is missing. One path does not: closing the failed-payment dialog drops
every answer, so the next attempt starts over.

"Violates AC4" would be wrong there, twice over: the spec overrode AC4's mechanism on purpose, and the
mechanism is not what fails. The finding exists only where following the spec also breaks what the
ticket promised the shopper. So the Source line carries both documents with their dates, says which
the code follows, and leaves the decision with an owner:

> **Source:** [PROJ-218](…) AC4 says checkout "resumes from the step at which the shopper left".
> Our [contract spec](…) Decision (2025-03-14) and the [design doc](…) (Draft, 2025-02-20) say the
> flow re-runs from the top. The code follows the spec, which satisfies AC4 everywhere except this path.

## Proving a finding

A probe is the cheap proof: a test written against the unfixed candidate that **asserts the buggy
behaviour**. If it passes, the bug is real and the finding is PROVEN — no patch, no fix, no
red-then-green. Delete the probe afterwards; it is evidence, not a test the project keeps. Where a
finding claims an existing test cannot fail, prove it the other way: mutate the production line that
test covers and run only that test. Red means the test does cover it and the claim is wrong.

The bar below is higher because it governs code you put in front of the author, not a finding you
report.

## Code suggestions: the full contract

1. Match the reviewed revision, the agreed behaviour, the file's conventions, its dependencies and the
   surrounding contracts. Prepare the patch in an isolated copy; never touch the author's tree.
2. Add or extend a meaningful test that exercises the behaviour. Watch it fail for the expected reason
   on the uncorrected candidate, apply the patch, watch it pass. A compile or setup failure is not
   behavioural red evidence. For a test-only suggestion, prove the test detects a relevant production
   mutation and passes on the intended implementation.
3. Run it through the project's own runner together with the relevant existing tests. Record the
   candidate identity, the patch, the test name, the commands and the observed red and green results.
   Static reasoning, a citation, a cached pass or a toy reimplementation is not proof.
4. If the tests cannot run or the result is inconclusive, omit the code, keep the finding, and state
   the limitation.
5. Use the forge's own suggestion block only for a verified, self-contained replacement of the exact
   anchored lines, revalidating the range and the diff refs before posting. A multi-file change goes in
   complete path-labelled blocks, and only when that combined patch passed the same proof.

**Where a Required or Must-to-have fix is small and self-contained, prefer a suggestion block.** The
proof does not change: the patch still passes points 1 to 3 before it is posted. What changes is the
shape a proven remedy takes, since a two-line fix the author applies in one click costs them less than
the same fix described in a paragraph they have to retype. Prose stays the right form for a fix that
spans files, needs a decision, or is one of several ways to solve the problem.

Any change to the patch or the candidate invalidates the proof until it is revalidated.

**The benefit has to be proven too, not only the patch.** Red-then-green proves the code works, never
that the finding is worth fixing. For any finding justified only by performance, allocations, log
volume or tidiness: measure the benefit or do not post it. A green suite is evidence the patch is
safe, never evidence it helps. If the comment has to admit the benefit cannot be measured here, that
sentence is the signal to leave it in the report. Never push a restructuring onto code the author has
already said is about to be replaced, so read the existing threads first. Assume the author takes the
shape and drops the constraint, and name in the comment what the change must not alter: ordering,
synchrony, threading, lifecycle.

**Another reviewer's numbers are data, not truth.** Reproduce a measurement with the project's own
tooling before building a finding on it. When two reviewers' numbers disagree, settle it before the
author acts on either.

## The Self AI Review mark

Every posted comment opens with one provenance line, above the category prefix:

> 🤖 **Self AI Review**

**A block quote on a line of its own.** The grey bar down the left is what does the work: it sets the
mark apart at a glance without it reading as the comment's first sentence. Not a heading, which would
outshout the finding under it, and not a bare bold line, which runs into the text below. The finding
is the part anyone has to act on, so the mark stays the quieter of the two.

The request's description carries a box saying the same thing once, ticked only after the threads are
posted and re-listed:

```markdown
- [x] **Self AI Reviewed**: business, technical and security lanes on <model> at <effort>,
  orchestrated by <model>. <n> threads posted: <n> Required, <n> Must to have.
```

**The box counts what was posted, never what was held back.** A reader can open every thread it
refers to. Naming findings that are not on the request tells them something exists that they cannot
read, which invites a question the box cannot answer and turns a coverage mark into a teaser.

**The mark is for the people reviewing after you.** It says a machine has already walked the whole
diff through the three lanes and the three gates, so a human reviewer does not have to repeat that
pass and can spend their time on what no lane can judge: whether this is the right change, whether the
design will hold, and whether the product decision behind it is the one the team wants.

It is a claim about coverage and nothing else. It never says the change is correct, and it never makes
a second reviewer optional. A reviewer who disagrees with a lane is right until the lane's evidence
says otherwise, and the lanes post evidence precisely so that argument can happen.

**Name the models, because that is what makes the mark worth anything.** A reader who knows which
model ran, at what effort, can weigh the findings and decide how much to lean on them; a ticked box
with no models named is decoration. Say it honestly when a lane was skipped, when a source could not
be retrieved, or when the main session ran the lanes itself on a small change, since a reader will
otherwise assume all three ran apart.

Also worth carrying into the request: one reference link where a claim leans on platform behaviour or
a written guideline.

## Forge mechanics

### GitLab

- Check `glab auth status` first. The GitLab MCP note tool cannot position comments; use `glab api`.
- Post a thread: `POST projects/:id/merge_requests/:iid/discussions` with `--input payload.json`, the
  payload being `{"body": ..., "position": {"position_type": "text", "base_sha": ..., "head_sha": ...,
  "start_sha": ..., "old_path": ..., "new_path": ..., "new_line": N}}`, the revisions taken from the
  request's `diff_refs`.
- **`glab api --method POST ... --input file.json` fails with HTTP 415, "The provided content-type ''
  is not supported", unless you also pass `--header "Content-Type: application/json"`.** Always pass
  it.
- Line numbers: prefer the raw file at head
  (`repository/files/<url-encoded path>/raw?ref=<sha>`); from a diff alone, reconstruct the numbering
  and validate it in both directions against the hunk headers. Anchor mid-block on added lines so an
  off-by-one still lands inside the same block.
- Write bodies as JSON files and post with `--input`; never inline shell-escaped strings.
- Verify every write by re-listing (`GET .../notes`), never by exit code: the CLI can exit non-zero on
  an empty 204, and a 404 on DELETE usually means the note was already gone.
- Resolving (`PUT .../discussions/:id?resolved=true`) can be refused where posting is allowed. After
  any attempt, re-list with `GET .../discussions` and report the real per-thread `resolved` value. When
  it is refused, print the exact one-line command for the user to run, then re-verify by listing.
- Update a comment with `PUT .../notes/:id`, keeping the anchor; rewording re-passes the comment
  contract.
- **Commit links.** A bare sha is a GitLab commit reference and links itself, but one inside backticks
  is not, which is why a hash in a code span renders dead. Post the link wrapped around the code span,
  pointing at `<web_url>/-/commit/<sha>`, with `web_url` taken from `GET projects/:id`.
- Reply in an existing thread with `POST .../discussions/:id/notes`, which needs no position: the
  thread already carries the anchor. Read the whole thread first, since a later note can withdraw
  what the first one asked for.
- **Suggestion blocks.** A fenced block opened with `suggestion:-N+M` replaces the commented line plus
  N lines above and M below, so a single line is `suggestion:-0+0`. The body is the replacement text,
  not a diff. Validate the range against the raw file at head before posting: an off-by-one here does
  not fail, it silently replaces the wrong lines. Suggestions may span several files, and the author
  can "Add suggestion to batch" and apply them in one commit, which is why several small ones cost
  them less than one prose comment asking for the same edits.
