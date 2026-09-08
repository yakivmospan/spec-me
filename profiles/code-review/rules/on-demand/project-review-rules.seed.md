# Review rules

What a review of this repository judges against, and where its evidence comes from. These are this
project's answers; the method is not here.

<!--
  FILLING THIS IN (SETUP.md, or by hand later). This form arrives with the `code-review` profile and
  is answered where it sits: the questions below only have answers where reviews run through
  `code-change-review`. Deleting the profile's folder takes this with it, and the next sync removes
  its line from `LOADER.md`.

  Every value here is specific to one repository, and a wrong one is worse than a missing one: a
  reviewer that trusts the wrong requirement source reports a scope gap that does not exist.

  Evidence, per section:
    Forge     — the git remote, and which CLI is installed. Name the project path a CLI needs.
    Sources   — the tracker in the branch names and commit subjects; any wiki or design space the
                README or the tickets link to. Ask which pages are mandatory for which areas.
    Reach     — ask the user which modules ship ahead of the code that will call them, and what
                gates them. This is the question nobody writes down, and it decides severity.
    Docs      — the language and framework documentation a guideline claim must cite.
    Closing   — the commands that end a review, from `.specs/02-tech.md`, and anything a working
                copy needs before it can build.

  Delete any section this project genuinely has nothing for. An empty heading teaches nothing.
-->

## Where the work is reviewed

| | |
|---|---|
| Forge | {{merge requests or pull requests, and the project path a CLI needs}} |
| Tool | {{the CLI that reads and posts, and anything it cannot do}} |
| Ticket | {{how a ticket id is derived, usually from the branch name}} |

## Requirement sources, in order

{{Numbered, most authoritative first. For each: what it is, and when it is mandatory rather than
optional. Name the pages that must be read together where one alone has been misleading. Say where
`.specs/` sits in the order, and that a spec disagreeing with the code is itself a finding.}}

{{Where criteria for a story can live in another repository, say so and say what the disposition is:
Missing here, a note on the story, never a defect.}}

## Reachability in this repository

{{Which modules or packages ship ahead of their wiring, and the exact chain to follow before calling
a defect Required: registration, construction, injection, call site, and the flag guarding it. Name
the type or file where those flags live. Say that inertness expires and what re-validates it.}}

{{Delete this section only if nothing here ships ahead of its callers.}}

## Documents to fetch for a guideline claim

{{The minimum set of official documents, as URLs, that a guideline claim must cite. Never quoted from
memory.}}

## Performance claims

{{The performance dimension that actually bites in this project, and how to measure it. Everything
else needs a measured number or it stays out of the request.}}

## Closing a review

{{The commands that close a review, and a pointer to the rule that says which of them CI gates. Say
what a fresh working copy needs before it can build, and that a missing one of those is a setup error
rather than a finding.}}
