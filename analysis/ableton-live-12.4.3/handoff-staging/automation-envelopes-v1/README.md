# Automation envelopes in Live Set documents, release 1

**Reviewed local release.** Read [the contract](spec.md),
[the cases](cases.json), [the role instructions](AGENTS.md),
[the manifest](manifest.json) and [the review disposition](REVIEW.md). The
stated partial scope, narrowed as recorded in the review, is approved as a
contract for a fresh, restricted implementation workspace. Such a workspace
has not been provisioned by this release.

The finite scope is how the decoded XML of one Live Set format version stores
track and clip automation envelopes: where envelopes are stored and how each
names its parameter, the event elements and their value kinds, the envelopes
that make a document refused when it is opened, how curve controls are kept and
written, and the text read and written for event numbers. Requirement IDs are
retained with explicit partial clauses. Requirements 004 (event Ids), 010 and
011 (the value an envelope supplies at a time) and 013 (editing, override,
recording, undo and the precedence of a parameter's own value over its
envelope) are not released. Envelope values at any time, clip envelope timing
and malformed or dangling envelopes have no expectation. No application source,
shipped file or public dependency is included.

The 21 cases use independently authored minimal XML fixtures. All expected
results are static-derived and unexecuted. They are not captured reference
behavior. The representation is a comparison convention, not an API claimed to
exist in Live and not a required architecture. No compatibility claim is made.
Preserve this release unchanged; corrections require a new revision.
