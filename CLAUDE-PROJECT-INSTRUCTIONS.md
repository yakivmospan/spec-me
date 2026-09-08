# Claude project instructions

Rebuild the Instructions of a Claude project (claude.ai) from this builder, so the chat works the way
the agent setup does — and keeps the project's files in the shape `.specs/` has, so the project can
move into a repository later. Ask the agent: "Follow `.agents/builder/CLAUDE-PROJECT-INSTRUCTIONS.md`"
— after changing the builder or your preferences.

## Read

From the repository root:

1. `.agents/builder/core/CONSTITUTION.seed.md` — the principles between the `carried` markers.
2. `.agents/builder/core/rules/always-on/project-ground-rules.md`.
3. Everything in `.agents/builder/profiles/ai-companion/` — its `PROFILE.md`, every rule and every
   skill.
4. `.agents/builder/profiles/documentation/rules/on-demand/docs-rules.md` and the `docs-incode`
   skill — for the code-comment lines only.
5. `.agents/builder/profiles/specs/specs/README.md` up to *Change what a spec guarantees*, and the
   templates `spec-00-product.builder.md` and `spec-feature.md` beside it — the shape of a spec.
6. `~/.claude/CLAUDE.md` and the user's Claude Code memory files for this project — preferences that
   hold everywhere.

A rule or skill added to ai-companion since last time is in scope; anything else only if the user
names it. Before writing, ask once for the previous version, to compare against — none is fine.

## The project's files

The chat saves the project's material as files in the project. Carry these conventions into the
Instructions, with the spec shape from step 5:

- **A file's name is its future repository path, dots for slashes:** `specs.feature.checkout.md` →
  `.specs/feature/checkout.md`, `data.prices.json` → `data/prices.json`. A name part never has a dot
  of its own (`price-list-v2`); only the last dot starts the extension.

  | File | Holds |
  |---|---|
  | `INDEX.md` | every file under its kind — specs, data, assets, code, docs — with one line on what it holds and which spec relies on it; then every open question |
  | `specs.00-product.md` | what the product is, who it's for, what it won't do |
  | `specs.01-architecture.md` | the parts and how they connect, once there is a system |
  | `specs.02-tech.md` | stack, tools, conventions |
  | `specs.feature.<name>.md` | one per feature: Intent, Acceptance criteria, Decisions, Open questions, Change history |
  | `data.*`, `assets.*`, `src.*`, `docs.*` | the material itself — a spec points at it under References, never copies it |
  | `NOTES.md` | an inbox for "save this" with no clear home yet |

- **Several products in one project:** each has its own tree, its name first —
  `shop.specs.00-product.md`, `admin.data.roles.json`. What both use, and a contract spec for
  behaviour spanning both, sits in a `shared.` tree. A spec names another product's file in its
  `related:` or References. `INDEX.md` has a section per product, then *Shared*. Joining two later:
  rename one's files into the other's tree as features, and merge its `00-product` into the one
  that stays.
- **Starting:** on "start the project", or a first message describing what the user is building —
  ask only what the description doesn't answer (who it's for, what it won't do, one product or
  several), then save `00-product` and `INDEX.md`. Architecture, tech, features and notes come as
  the conversation reaches them.
- **Converting a project that has files already:** on "convert the project" — read every file, then
  show a plan before writing anything: each old file's pieces and where each goes (file and
  section), what merges, what goes and why (a duplicate, superseded, no longer true), and every
  place two files disagree, asked rather than settled. One product or several is part of the plan.
  Write on the user's yes; delete an old file only on a separate yes, once its content is placed.
  What has no clear home goes to `NOTES.md`.
- **What goes where:** a fact about the whole product → `00-product`; a choice and what it ruled out
  → the owning spec's Decisions; something undecided → its Open questions, with the next action;
  no clear owner → `NOTES.md`, with a suggested home.
- **Reading:** at the start of a chat, `INDEX.md` first, then what the topic needs. A file is a
  claim — where the user says otherwise, say so; which is right is the user's call.
- **Saving:** on "save this", or a yes to a proposed entry: show the exact text and which file it
  goes to, then write the file, add a Change history row to a spec it changed, and bring `INDEX.md`
  up to date. Nothing else is saved.
- **Growing:** a spec per feature once a feature has criteria or decisions of its own; a file split
  by topic past about 1,500 words.
- **Moving to a repository:** rename each file to its path; sort `NOTES.md` into specs first; write
  the repository's `README.md` then, from `00-product` and `02-tech` — the project has none.

## Write

One markdown document for the project's Instructions field — the chat starts a project's files
itself, so nothing else is needed:

- **Self-contained:** no file paths from this builder, no skill, rule or loader names, nothing about
  this repository, reviews, or tools a chat project doesn't have (subagents, git). Turn "run the X
  skill when…" into the behaviour itself.
- **Meaning, not wording:** condense examples and reasoning; keep formats exact — the pin layout, the
  choice format, the markers ⭐ ▶ ⏳ ⚠ 📌 📍, and the spec sections and criterion shape.
- **Sections, in this order:** Principles, How a reply reads, Choices, A second look before acting,
  Pinned questions, Snapshot, Project files, Code. Add a section only for a new kind of preference.
- **Size:** under 1,800 words, plain words, one fact per bullet.
- **Two sources disagree:** don't pick — list the disagreement after the document.

## Report

The document as a file, its word count, and — when a previous version was given — what was added,
changed or dropped, one line each.
