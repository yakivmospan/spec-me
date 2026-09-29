# Design quality

Read before proposing, comparing or reviewing a design: an approach, an architecture, where a
responsibility lives, how two parts talk to each other. The aim is the design a senior engineer who
knows this codebase would choose, and one that lasts: it fits the system's structure and the needs
already known. It never guesses at future ones — simple and lasting are the same thing here.

1. **Map before you propose.** Trace the flow end to end: where it starts, every layer it crosses,
   every place that uses its result, and what happens to work already in flight when it changes. List
   the pieces the codebase already has for this job — its interfaces, channels, extension points,
   dependency injection and conventions. An option that skips an existing piece says why. Done when you
   could draw the flow with its real class names without guessing.
2. **Design for the kind, not the one case, when a second case is known** — named in the ticket, a
   spec, or by the user. Otherwise build the one case, and put it where the next one plugs in without
   rework.
3. **Shared types stay general.** A type many callers use never carries one feature's data; the
   feature's meaning lives in the feature's own code.
4. **Wire the way the codebase wires.** Its dependency injection, not a new process-wide object. One
   part recognises another's outcome only by what that part says on purpose — a code, a type, or text
   it owns through a constant both share — never by free text or by digging into its reply's format.
   Where the codebase already recognises a similar outcome, do it the same way.
5. **Each concern lives with its owner.** A new responsibility gets a home of its own, never a room in
   a class that does something else.
6. **Recommend the lasting option by default.** Size decides only between options that fit the system
   equally well; "fewer files" never outweighs fitting it. When time forces a shortcut, name it as one,
   say what it costs later and where the proper way plugs in, and take it only when the user picks it.
7. **The same checks apply when reviewing** a design, a plan or code.
8. **Before sending a design, ask:** would a senior engineer who knows this codebase propose the same?
   If not, rethink before asking the user to choose.
