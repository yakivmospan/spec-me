# Specs

What this codebase guarantees, written down so any person or agent can rely on it and keep it true.
Plain Markdown: no tool, skill or script is needed to read a spec or to change one.

A spec reads as short documentation of the code as built: what it does on purpose (Behaviour), and
what plain docs lose — what was turned down and why (Decisions), and what is still undecided (Open
questions). Where the code has docs of its own — a README, doc comments, an `ARCHITECTURE.md` — the
spec points there instead of repeating them; where it has none, Behaviour is its documentation. What
the code will do is a change's plan, never a spec.

## What's here

```
.specs/
├── README.md             this file
├── 00-product.md         what the product is, who it's for, what it does — pointing at each feature's spec — and what it won't do
├── 01-architecture.md    modules and the boundaries between them
├── 02-tech.md            stack, commands, testing conventions
├── feature/              one spec per feature, nested freely
├── contract/             behaviour that spans several modules
├── changes/              planned work — one folder per change, holding its plan
└── INDEX.md  DECISIONS.md  OPEN-QUESTIONS.md    generated overviews — optional, never committed;
                                                 when one looks stale, the specs win
```

Every Markdown file here, outside `changes/`, is a spec. What a spec draws on without being one — research, a log, legal
notes — lives outside `.specs/`, and the spec points at it under References.

## Find the spec for a file

- **By `owns`:** a spec lists the code it describes under `owns:` in its frontmatter. Search for a
  glob that matches the file; the most specific match owns it.
- **No match** is normal: much of the code may have no spec yet.
- **Check `changes/` too:** a plan there that names the spec among those it touches says what is
  about to change.

## Read a spec

Frontmatter:

- **Always:** `id` — unique and dot-namespaced, like `feature.logger`; `title`; and `parent` — the
  id of the spec above it.
- **Optional:** `owns` — the code it describes, its tests included, `[]` or left out when it owns none; `related`; `ticket`;
  and `updated` — the day it was last confirmed against the code.

Sections, each present only when it has something real:

- **Intent** — what it guarantees to the rest of the system, not how — and, for a feature that carries
  part of a contract, which contract.
- **Behaviour** — one line per rule the code follows on purpose: the edge cases, failures, ordering and
  callers a reader could get wrong, not the happy path anyone expects. Code that differs from a line is
  a conflict to raise, never to settle quietly; behaviour not listed isn't promised. The tests are the
  proof, found through `owns`. A rule the code breaks, or something it does that nobody chose — a
  likely bug — is not a Behaviour line: the gap goes under Pitfalls, and the fix under Future plans,
  or an Open question when it's unclear the fix is wanted.

  ```markdown
  - A dropped upload is retried once, then reported as failed.
  - Only the signed-in account's uploads are sent; another account's stay queued.
  ```
- **Decisions** — a choice, and what it ruled out under *Instead of*. Don't bring back a rejected
  option without saying so. Revising one: edit it in place; the overturned choice joins *Instead of*,
  with what was learned, and Change history gets a row. A long list is grouped under the same bold labels as Behaviour.
- **Open questions** — undecided, each a bold question with an *Action*. Never settle one by guessing;
  ask. Once answered, delete it: the answer lives on as a Decision, a doc comment or the code.
- **Future plans** — wanted, but not now: a bold title with optional *Why*, *Not yet because* and *Take
  up when*. Not a guarantee, and it may point at a kept plan in `changes/`; it goes when the work
  that builds it lands.
- **Pitfalls** — what a reader would get wrong; **References** — pointers; **Change history** — a table with one row
  per change in documented behaviour or requirements, or a revised Decision: the ticket, one sentence
  and the date.

A contract spec (`contract.*`) owns no code. It has an **Intent** and **Behaviour** like a feature — the
rules that hold across its modules — and adds **Source** — where it came from — and **Implementation** —
which features and modules take part, and their role. A feature taking part names the contract in its
Intent.

## Change what a spec guarantees

- **Shaping, the default:** build, try, adjust, repeat. Each spec the work moves is edited in place as
  you go — Behaviour to what's built, a Decision for an option tried and dropped, one Change history
  row (its ticket, or "No ticket") and `updated:` for the work.
- **Planning, when asked:** work worth thinking through first gets a plan, below. Specs still follow
  the code as it's built; you can reshape the plan, and fold in, at any point.
- **Not sure which way?** Ask whether the code is already right: if it is, the spec is corrected in
  place, or written from the code; if not, the code follows the spec.
- **Keeping it honest:** code or tests moved or deleted → update `owns`; something a spec records as
  broken or pending fixed → correct every line that describes it.

1. **Open a change** — a folder `.specs/changes/<branch-name>/` holding one file,
   `implementation-plan.md`; a second change on the same branch adds what it's about:
   `<branch-name>-<topic>/`. Folders may nest to group one story's tickets; each one holding a plan is
   a change of its own.
2. **Write the plan**, starting with `status: draft` in its frontmatter:
   - **`## Requirements`:** why, in a sentence or two, then what must hold once it's built — plain
     lines grouped by topic, never a log of spec edits. Anything undecided is an Open question here.
     It ends with one line naming the specs it touches.
   - **`## Findings`**, when there are any: how things really behave, learned while doing the work,
     each dated, with where. When the change is folded in, what still holds goes into the specs.
   - **`## Design`:** how, with each option not taken as `- **Not {option}:** {why}`, and each new or
     changed call between packages or layers as a signature with the class that owns it. A new module,
     boundary or library: say so before touching build files.
   - **`## Tasks`:** checkboxes in the order they run, each an instruction with its number inside the
     bold title — `- [ ] **3. …**`, so every viewer shows the number. An optional `- Check:` line under
     it names a test, or what to try by hand. A check needing a real push, pipeline or device is a
     task of its own.
   - **When needed:** `## Not in this change`.
3. **Approve** — the user's OK on the plan sets `status: approved`; asking to build a draft is that OK.
   Only the user sets it back to `draft`, to rethink.
4. **Build** — tasks in order, re-reading the plan before each one. A task only a person can check
   waits for them, and what they saw goes on its Check line. As each task lands, the specs it moved
   are updated in place — Behaviour, Intent, `owns`, a Decision, `updated:`, and once per change a
   Change history row; a new spec is written when its first piece lands. One blocked by an Open
   question waits; build what isn't blocked.
5. **Fold in** — when the user says it's done, or asks to save what's built so far. The specs already
   say what's built; anything they missed is added, and a `Not` line someone reading only the code
   would propose again becomes a Decision. What isn't built: if the user hasn't said, one question —
   "The rest — into Future plans, or keep the plan for later?" Into Future plans, the folder goes;
   kept, the plan is cut to what isn't built and what it waits on, and each spec it touches gets a
   Future plan pointing at it.
- **Abandoning a change:** on the user's yes, delete the folder. Code and spec edits already made stay
  unless the user asks to undo them.

### Reshaping the plan

Any time: edit, add, reorder or delete pending tasks; rewrite Requirements and Design to what's true
now — a dropped approach becomes a `Not` line saying what was learned. Shaping what's built — trying it
and adjusting — changes the code and the specs directly, with no new task. Work reaching another
module: say so, and ask whether it joins this plan or gets its own.

## Why another spec format?

Same idea. Less paper.

| Per change | OpenSpec | Kiro | Ours |
|---|:---:|:---:|:---:|
| Files to write | 3 | 3 | **1**, the plan — and none when shaping |
| Approval gates | 1 | 3 | **1**, and none when shaping |
| Files left behind after merge | 3, archived | 3, forever | **0** |

| | OpenSpec | Kiro | Ours | + Simpler because | − Costs us |
|---|---|---|---|---|---|
| **A change** | delta blocks + `proposal.md` + `tasks.md` | permanent `requirements.md` + `design.md` + `tasks.md` | one plan: requirements, design, tasks | specs never move | requirements are plain lines, not a diff of the spec |
| **After it lands** | change archived | docs kept forever | the plan goes; its decisions stay in the specs | one place to read | rationale lost unless written into a Decision |
| **Approval** | 1 gate | 3 gates, in sequence | one OK on the plan | nothing to sequence | design not gated — flaws caught mid-build |
| **Cross-module work** | no concept | no concept | `contract` spec | tickets land independently | one more spec kind |
| **What it guarantees** | requirements, each with WHEN/THEN scenarios | user stories with EARS acceptance criteria | one plain line per rule, tests as proof | nothing to keep in step with the tests | no rule-to-test link in the spec |

**Why ours:** one merged spec beats a pile of documents — OpenSpec's archived proposals nobody
reopens, or Kiro's per-feature files that keep growing and can drift from what's actually true. A
curated Decision lives right next to the guarantee it explains. The real risk is skipping that
write-up, not the missing archive — the original is still in `git log` either way.

**Why it's easy to adopt:** no required tooling, and partial coverage is normal, not an error. A team
new to spec-driven work can write one spec file and go, no CLI or three-gate flow to learn first. A
big existing project gains specs one module at a time, confirmed from the code that's already
there — no big-bang migration.

### A hybrid, on purpose

- **The plan leads:** what's agreed goes into the plan, and the code is built to it — and reshaped as
  it's tried.
- **The spec follows:** it documents what the code does on purpose, and keeps what docs lose — why,
  what was turned down, what's still open. Where the code has docs of its own, the spec points there.
- **When they disagree,** the code settles what the system does today; what it should do is the
  user's call — shaped straight away, or planned first.

The pure version — criteria as the source of truth the code must always follow — kept turning into
this one anyway: criteria reworded to match the code once it was built.

### Behaviour, not acceptance criteria

Acceptance criteria — a numbered Given/When/Then each, with its tests listed as proof — look rigorous
and work badly in practice. The agent writes them, they get approved unread, they are reworded to match
the code once it's built, and their test lists go stale with every rename. The approval that counts
happens in chat and in the plan. So a spec lists **Behaviour** instead: one plain line per rule the
code follows on purpose.

| | Acceptance criteria | Behaviour |
|---|---|---|
| One rule | 6–15 lines: id, Given/When/Then, checkbox, proof | 1–2 lines |
| Its proof | test names copied into the spec | the tests themselves, found through `owns` |
| A test renamed | the spec goes stale | nothing to update |
| Folding in a change | each criterion confirmed or dropped | done when you say so |
| A rule the code's own docs already state | written again | pointed at |
| Behaviour nobody chose | written up as a criterion | a Pitfall, with an Open question |
| A Decision revised | dated `Replaced` lines retelling each version | the old choice joins *Instead of*; a Change history row dates it |

- **What we gain:** a spec you read in a minute, grouped by topic, that doubles as the feature's
  documentation; nothing to keep in step with the tests or the docs; less for an agent to read before
  every task; no bookkeeping — no ids, checkboxes or proof lists.
- **What stays the same:** a listed rule is on purpose, so code that differs is raised, never settled
  quietly; behaviour not listed isn't promised; a person's word is enough — a line needs no test;
  Decisions and Open questions still keep the why and the undecided.
- **What we lose:** the link from a rule to the test that proves it — the tests under `owns` are
  searched instead; a ready checklist to tick a change off against — the plan's tasks and their
  Check lines do that; criteria to hand another team — written on demand from the lines and the
  tests, in minutes.

### Converting out

Not locked in — same Markdown shape everywhere: frontmatter, named sections, one-line behaviour rules.

- **Specs → OpenSpec/Kiro baseline:** rename + reformat; each Behaviour line becomes a requirement
  with one scenario. Minutes.
- **Open change → delta or design+tasks:** split the plan. Minutes.
- **Spec → permanent design doc:** doesn't exist — write it, don't convert it.
