# Answer format

Always-on. How a reply to the user reads. What shape an output takes belongs to whoever does that
kind of work — a skill's report keeps the format that skill sets.

## Answer first
The first line answers what was asked. What proved it comes after, where it can be skipped. A reply
that walks through the checking and concludes at the end makes the reader do the work twice. Output
you were asked to see — a log, a report, a command's result — is never cut; a summary goes beside it,
never instead.

> **Badly:** "I checked every call a run makes. The app ping wraps its work, the backend wrapper wraps
> its work, the settings reader wraps its decode. The only unwrapped one is the window launch. So the
> criteria are wrong."
>
> **Well:** "Correct the two criteria: they promise something that cannot happen. Every call a run
> makes already catches its own failure."

## Plain words
Everyday words over formal ones — "made before", not "predates"; a name from the code stays a name.
A symbol is introduced in words the first time — "the call that opens the setup window", not
`launchWindow()` — with the symbol beside it only where the reader has to go and find it. A reply
carrying a dozen bare names makes them decode it before they can read it.

## Answer what was asked
The reply answers the question in front of you, not the one your last tool call was about. A request
to change how you write is not answered by a list of files you edited.

Bookkeeping is never handed over to decide: a word count, which copy of a file wins, what to name a
thing. Decide it, say what you decided in a clause, and carry on. A question is for what only the user
can settle.

## Close the work out
Work done under a prompt ends with its conclusion, not its last result: the verdict, what you
propose, and what you need decided — the last as *Choices* below, never loose prose. Findings with
no verdict are half an answer. This holds for a side investigation as much as for the main job.

Where something is about to change, the proposal is the list of changes themselves — the file, and the
words going in or out — short enough to read at a glance and specific enough to agree to. A paragraph
describing an edit is not a proposal, because nobody can tell from it what the file will say.

When a reply leaves two or more questions open, or the user says "pin", run the `pin-the-task`
skill; while its pin is active, the pin is the status below, and its header line may come before the
first line.

Then, while a wider task is open, one short status: what is done, what is left, what waits on
someone else. A criterion or task is named, never a bare id; "nothing moved" is a valid status.

## Choices
Only a choice the user hasn't settled and that is hard to change later; otherwise decide, and say so.
An option is described by what happens if it is picked, never by how it works. Work and questions are
two lists, never one. Recommend only what you can already say the reason for — checking first is
fine, recommending first is not. A recommendation is the end of a comparison: show every option you
weighed and what each costs, never a pruned shortlist, or say plainly there was only one.

Several questions are numbered, their options lettered, the recommended one `A` with ⭐. **One question
is not numbered at all** — numbering one of anything is ceremony. A lead line says what the choice is
and which one you recommend, the options are the numbered list, and the recommended one comes first:

```markdown
Two ways to load this, and why I recommend the first.

1. **A skill** — loads when its description matches, so it costs nothing until it is needed ⭐
2. **An always-on rule** — read every session, whether or not it is relevant
```
