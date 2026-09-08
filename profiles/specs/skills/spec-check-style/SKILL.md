---
name: spec-check-style
description: Use when asked to "review this spec", "check the spec for style issues", "is this spec well written", or when the user accepts spec-merge's offer of --fix on the specs a change touched — reviews existing specs against spec-style-rules.md and reports findings, or with --fix applies the high-confidence ones. Not for writing or changing a spec (spec-create), checking structure and drift (spec-rebuild-overviews), or reviewing the spec setup as a whole (project-test-setup).
---

# Spec Review

`spec-style-rules.md` is applied while a spec is written; nothing re-checks it afterwards, and `spec-rebuild-overviews`
checks structure, never prose. This skill is that second read.

## Non-negotiables

- **Only two triggers:** a direct request, or the user's yes to `spec-merge`'s offer of `--fix`. Never sweep `.specs/**`
  unprompted; when a request names no spec, ask which.
- **Without `--fix`, report only.** With it, apply the high-confidence findings; judgement calls stay
  flagged for the user.
- **Verify against code** before calling a Decision, a guarantee or a citation wrong — open the file.
- **A checked criterion's proof — a test, or `Source: Manual` with its description — is never a
  finding**, and never stripped: that turns a verified criterion back into an unverified one.
- **A finding names its place, the rule it breaks and the fix.** "This is bloated" alone isn't one.

## Before reviewing

Read `.agents/profiles/specs/rules/on-demand/spec-style-rules.md` fresh — the checklist is the rule. Open this skill's
`reference.md` entry for a rule only when the checklist doesn't settle a finding. Run `spec-rebuild-overviews`, and take what it reports
about decisions — a missing **Instead of**, one recorded twice — as the starting list.

## Reviewing

Read each spec whole, then section by section in order, against every rule in the checklist. Where each
section most often goes wrong:

| Section | Check hardest |
|---|---|
| Acceptance criteria | *Guarantee, not implementation*; *Sub-bullet per field*; three "And"s that are two criteria |
| Constraints | *Obligation, not description* — a dependency edge, a gotcha or a behaviour isn't one |
| Public surface | *Point, don't repeat* — a symbol inventory; a stub on a leaf module |
| Decisions | *What was rejected*; *One owner per decision*; doc comment or spec (`spec-builder-rules.md`'s *Where a decision lives*) |
| Pitfalls, References | *Point, don't repeat* — a file map, restated behaviour, a summary of the target |
| Change history | *One row, one sentence* — no rows for prose edits |
| Anywhere | *The delete test*, *Plain words, no filler*, *Prose over ceremony*, *Every chapter earns its place* |

Tag each finding:
- **High-confidence** — one fact stated at two exact locations, a Decision with no **Instead of**, a
  Change history row with no behaviour in it, a missing sub-bullet, a stubbed section.
- **Judgement call** — whether a Pitfall is really non-obvious, whether a decision is file-scoped, whether
  an AC is really two.

## With `--fix`

Apply the high-confidence findings. Then run `spec-rebuild-overviews`. A style pass changes no behaviour: no Change
history row, and `updated:` stays.

## Report

Per spec, then per section, most serious first: each finding with its tag, the rule and the fix — never
what is already fine. Close with one line: specs reviewed, findings, how many high-confidence, and any
source files edited.
