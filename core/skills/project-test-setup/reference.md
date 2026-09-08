# Project Validate — questions and priorities

Every run asks every question below of every file or pair its check lists, so two runs look at the same
things. An answer that differs between files, or a file that doesn't answer where it should, is a finding.
A profile's own questions are in its `PROFILE.md`, under **Self-check**.

## Constitution

For each scenario, open the rules and skills its work reaches, and ask:

1. Does anything warn, fail, or ask for a test when work was confirmed by hand?
2. Does a change of mind mid-way stop the work, or add an approval, beyond what the rule for that work
   says?
3. Does any line argue for a test, check or gate, or defend not having one?

## Consistency

Ask of every pair on the list:

1. Who approves what, and what counts as approval?
2. What do done and red flag mean?
3. What is committed, and what does local mean?
4. What does each say is read, and when — for an agent, what its steps read?
5. Do both name the same file, field, section or order for the same thing — a skill's description
   against its own body included?

Of the loaders, also: does every rule have one line placing it, does every skill a line runs exist, and
is each skill run from one line only?

For a skill against the template: quoted triggers first, a **Not for**, the template's sections or a
reason for its own; for a code or docs skill, the precedence line `project-create-rule-or-skill`'s *Non-negotiables*
allows — a skill that only reads and reports carries none.

## Load

For every always-on rule, on-demand rule, and body of a skill a piece of work loads:

1. Does every session or task that loads it need all of it?
2. Is a passage said elsewhere that also loads — a skill step restating a rule, a file re-read that is
   already loaded, two files read where one or a diff would do?
3. Does a skill read a reference whole where its rule says to open one entry?

## Simplification

1. Would an agent act the same without this line, step, field or file?
2. Do two files or two skills do one job?
3. Does a step repeat its own skill's non-negotiables or description?

## Leftovers

Beyond the inventory's leads: does any builder block, installed or not, name something only this project
has?

## Priority, with examples

- **Critical** — a step that loses data, fakes a pass or a confirmation, or breaks a principle on ordinary
  work. *Example:* a step that deletes a folder of the user's without their yes.
- **High** — ordinary work does the wrong thing. *Example:* a rule no loader line places, so it never
  loads; or "review this" about a merge request triggering a skill for reviewing a rule.
- **Medium** — two files give different answers to a question above; or 250 or more words loaded where the
  work doesn't need them. *Example:* one commit format in the workflow rule and another in a skill.
- **Low** — a term used two ways, a repeat under 250 words, a wording slip, an example or a leftover.
  *Example:* "the human" where everything else says "the user".
