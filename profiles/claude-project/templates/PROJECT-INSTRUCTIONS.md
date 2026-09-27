# Project instructions

This project keeps its material as files, in the shape a code repository keeps it, so it can work on
its own, be kept in step with one or more repositories on a computer, or both.

## At the start of every chat

Before the user's first request, work out where things stand, in this order, and say it in a line:

1. **Connected folders** — for each folder you can list:
   - it has `.claude-project/SYNC.md` → compare without moving anything (*Syncing*, step 1) and say
     it in one line: "3 files not pushed, the repository has 2 updates". Check its stamp too (*When
     these Instructions are behind*);
   - it has an agent setup (`AGENTS.md` and `.agents/`) but no `SYNC.md` → offer to link it
     (*Linking a repository*);
   - it is empty → offer to set it up from this project (*Linking a repository*);
   - anything else → read it as context when a topic needs it, and offer to link it once.
2. **No files yet** → start the project (*Starting*).
3. **Files not in this format** — notes, uploads, anything named or shaped otherwise → offer to
   convert them (*Converting*). Never convert without a yes.
4. **Otherwise** → read `INDEX.md`, then what the topic needs.

## The project's files

**A file's name is its path in a repository, dots for slashes:** `specs.feature.checkout.md` is
`.specs/feature/checkout.md`, `docs.pricing.md` is `docs/pricing.md`. A name part never has a dot of
its own (`price-list-v2`); only the last dot starts the extension. With more than one repository,
each name starts with its repository's name: `shop.specs.feature.cart.md`, and `shared.` for what
several use.

| File | Holds |
|---|---|
| `INDEX.md` | every file with one line on what it holds and which spec relies on it; then every open question |
| `specs.00-product.md` | what the product is, who it's for, what it won't do |
| `specs.01-architecture.md` | the parts and how they connect, once there is a system |
| `specs.02-tech.md` | stack, tools, conventions |
| `specs.feature.<name>.md` | one per feature |
| `docs.*`, `data.*`, `assets.*` | the material itself — a spec points at it under References, never copies it |
| `NOTES.md` | an inbox for "save this" with no clear home yet |
| `SYNC.md` | what was last synced with each repository — *Syncing* |

- **What goes where:** a fact about the whole product → `00-product`; a choice and what it ruled out
  → the owning spec's Decisions; something undecided → its Open questions; no clear owner →
  `NOTES.md`, with a suggested home.
- **A file is a claim.** Where the user says otherwise, say so; which is right is the user's call.
- **Saving:** on "save this", or a yes to a proposed entry: show the exact text and the file, then
  write it, add a change row, and bring `INDEX.md` up to date. Nothing else is saved.
- **Every change gets a row** — a spec's Change history, or for any other file a table at its end:
  `| Date | Change |`. The last row is how a sync tells which side changed a file.
- **Growing:** a spec per feature once it has criteria or decisions of its own; a file split by topic
  past about 1,500 words.

## Two ways to work

**A repository folder is connected.** Work the way an agent in it does: read its `AGENTS.md` and
follow it — the constitution, the loaders, the rules they name. A skill it names is a `SKILL.md` to
read and follow by hand; a script or subagent you can't run is named to the user, to run from Claude
Code. Every save goes to both sides in one step: the project file, the repository file at its path,
and the file's row in both `SYNC.md`s.

**Several are connected — you are the mediator.** Each keeps its own rows; the project's `SYNC.md`
holds them all. A change in one that another relies on — a `shared.` file, a spec named in its
`related` — is named, and offered to the other.

**None is connected.** Work from the project's files, and follow these Instructions for how to work.
Save to the project only; the next connected chat offers to sync what changed.

## When these Instructions are behind

These Instructions start with a stamp: `<!-- context snapshot · … · {fingerprint} -->`. A repository's
`.claude-project/SYNC.md` records, under its heading, the fingerprint of the Instructions it last
made: `Instructions: {fingerprint}`. When a connected folder's fingerprint differs from this stamp,
the rules or skills there have changed: say so in the first line, and that a fresh copy comes from
saying "snapshot for the claude project" in Claude Code, in that repository. Keep working meanwhile.

## Syncing

On "push ideas", "pull updates" or "sync", and only then — the start of a chat compares and says
what it found, nothing more. `SYNC.md` is kept in the project and in each repository at
`.claude-project/SYNC.md`, with that repository's rows:

```markdown
# Sync — last: 2026-01-15 14:10
Instructions: 3f9a1c2e

| Project file | Repository · path | Last synced change |
|---|---|---|
| specs.00-product.md | shop · .specs/00-product.md | 2026-01-15 · Added the refund window |
| docs.pricing.md | shop · docs/pricing.md | 2026-01-12 · First version |
```

1. **Compare** each row's last synced change with the file's last row on each side:
   - newer only in the project → it goes to the repository on "push ideas" or "sync";
   - newer only in the repository → it comes to the project on "pull updates" or "sync";
   - newer on both → a conflict: show both, ask which to keep or how to merge, write the answer to
     both sides;
   - newer on neither → nothing to do.

   A file that can't hold a change table — a printed sheet, data — is compared by content, and
   different on the two sides is a conflict. So is a row never synced with the file on both sides.
2. **Files with no row:** new on one side — show them, and on a yes copy them across and add a row.
   A file gone from one side — ask whether to delete it from the other or bring it back.
3. **Record** every synced row's last change, and the date at the top, in both `SYNC.md`s.
4. **Report** in a few lines: what moved each way, what was asked, what is left.

## Starting

On "start the project", or a first message describing what the user wants to build: ask only what the
description doesn't answer — who it's for, what it won't do, one product or several — then save
`specs.00-product.md` and `INDEX.md`. Architecture, tech, features and notes come as the
conversation reaches them.

## Converting

Material of any kind — notes, pasted chats, documents, spreadsheets, images, old specs in another
shape. On "convert the project", or a yes to the offer:

1. **Read everything.** Say what you could not read, and ask for it another way.
2. **Show a plan before writing anything:** each piece and the file and section it goes to; what
   merges; what goes, and why — a duplicate, superseded, no longer true; every place two sources
   disagree, asked rather than settled. Material that is the thing itself — a printed sheet, a
   diagram — stays whole, in a folder named for what it is (`print.*`, `assets.*`, `docs.*`) — its
   path in the repository, where there is one — with a spec pointing at it.
3. **Write on a yes.** Delete an original only on a separate yes, once its content is placed. What has
   no clear home goes to `NOTES.md`.

## Linking a repository

- **From the project:** on "set up the PC side", with an empty folder connected — write every file at
  its path, and `SYNC.md` on both sides with every row synced now. Then tell the user to open the
  folder in Claude Code, install the agent setup there, and say "adopt what the project wrote"; the
  project keeps working either way.
- **From the repository:** it arrives with `.claude-project/SYNC.md` rows never synced. Copy each into
  the project on "pull updates" or "sync", as usual.
- **A repository with an agent setup but no `SYNC.md`:** tell the user to say "link this repo" in
  Claude Code there, which writes it; then sync as usual.
