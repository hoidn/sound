# Transport state in Live Set documents, release 1

**Staged candidate, not reviewed, not released.** Read [the contract](spec.md),
[cases](cases.json), [role instructions](AGENTS.md) and [the manifest](manifest.json).
This package is not an implementation input until a separate review approves
it and it is published. Even then, implementation requires a fresh, restricted
implementation workspace, which this package does not provision.

The finite scope is how the decoded XML of one Live Set format version stores
the arrangement loop switch, loop start, loop length, playback position, tempo
and time-signature code: where each value is, which text is accepted or refused
when a document is opened, what missing, duplicated and unknown items do, and
the exact text written on save. Existing requirement IDs are retained with
explicit partial clauses. Requirements 009 and 012 and every runtime effect
remain unreleased. No application source, shipped file or public dependency is
included.

The 18 cases use independently authored minimal XML fixtures. All expected
outputs are static-derived and unexecuted, not captured reference behavior. The
representation is a comparison convention, not an API claimed to exist in Live
or a required architecture. No compatibility claim is made.
