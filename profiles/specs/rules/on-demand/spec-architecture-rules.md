# Architecture rules

| Rule | Detail |
|---|---|
| Read first | `.specs/01-architecture.md`, `.specs/02-tech.md` (its Technical constraints and Development approach often bound the option space), and every spec whose `owns` glob overlaps the blast radius, plus the actual code — existing patterns outrank general best practice. |
| A proposal needs | For a real choice, at least two approaches with concrete tradeoffs (migration cost, testability, blast radius); with one obvious way, say so. Either way, which specs would change, by id. |
| Boundaries, and changes to them | Which module may depend on which, and why, is `.specs/01-architecture.md`'s Boundaries section — read it there. A new module dependency that doesn't fit it is a boundary change: flag it and wait for the user's yes before adding. |
| Recording a decision | In the narrowest spec whose scope covers it — `01-architecture.md` only when no narrower one does — per spec-style-rules' *One owner per decision*, *What was rejected* and *Revising, not replacing*. Inside an open change, as spec-change-rules' *Implementation plan* says. Outside a change, a new module or moved boundary goes into `01-architecture.md` alongside the code, with a Change history row and `updated:` (spec-format-rules' *Change history*). |
