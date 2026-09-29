# Write summary — shapes by kind

## Open questions — `templates/questions-summary.md`

- **Title and date:** `# <Product> <topic> — open questions`, then `Updated YYYY-MM-DD`.
- **Opening:** two to four sentences — what the topic is and where it is heading, with its tracker
  ticket; that these questions need answers from outside the team; and, by number, the ones whose missing
  or negative answer breaks something a user already has. One that only holds back planned work isn't
  among them.
- **Groups:** a heading per owner, named as the reader's team (`Settings app team`), or teams together
  (`Backend team and product owner`). The group holding a blocking question first; then each team,
  followed by the joint groups it leads, most questions first — `Backend team and product owner` with two
  before `Backend team and platform owner` with one; a product-owner-only group last. One numbering runs
  across all groups, so a question can point at another ("question 4").
- **Each question:** a direct question in bold; how it works today; the one thing asked, addressed to the
  reader ("Please tell us", "Please confirm") — several only when the reader must act on each; then, only
  where today's behaviour doesn't already make it clear, what changes with each answer and what we do
  until then, a value we use meanwhile included. Keep only facts the reader needs to answer, never ones
  they own. Three or more facts or asks become bullets with a bold lead-in; options are bullets, never
  numbered.

## Cases a team must handle — a table under the question that asks for it

- **Rows:** from the specs' criteria and the code, one per situation, not per value. Go through: an
  account switch, a restart, boot, an interrupted step, and each dependency before and during use — each
  that applies gets a row, or is left out knowingly. Situations share a row only when they have the same
  cause; a situation naming either of two values (microphone or location) is one row.
- **Groups:** today; planned — any ticket will report it, a follow-up one included; reserved — in an API,
  and nobody has planned to report it. Today's rows show the value now and after the planned work;
  planned rows show the value after it.
- **Closing note:** go row by row, and name every row the fix asked for doesn't cover, because something
  outside the reader's reach — another app, the backend, a list — must change first.

## Decisions

- **Title and date:** `# <Product> <topic> — decisions`, then `Updated YYYY-MM-DD`.
- **Each decision:** what was decided, in one sentence; what it ruled out, and why; what it means for
  the reader — what they can rely on, or have to do. A decision replaced since goes in only when the
  reader built on the old one, saying what changed.
- **Groups:** by what the reader works on, not by spec.

## How it works today, or anything else the user names

- **Title and date** as above, with the kind in the title.
- **Sections** that follow the reader's questions, not the code's structure: what happens, when, what
  they see, what they can do. A table where a set of cases or values repeats the same shape.
