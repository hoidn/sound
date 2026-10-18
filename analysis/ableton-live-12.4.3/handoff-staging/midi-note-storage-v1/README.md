# MIDI clip note storage in Live Sets, release 1

**Reviewed local release.** Read [the contract](spec.md),
[the cases](cases.json), [the role instructions](AGENTS.md),
[the manifest](manifest.json) and [the review disposition](REVIEW.md). The
stated partial scope, narrowed as recorded in the review, is approved as a
contract for a fresh, restricted implementation workspace. Such a workspace
has not been provisioned by this release.

The finite scope is how a Live Set stores the notes of a MIDI clip: the note
structure, which note text is accepted or refused when the set is opened, the
defaults and limits applied on opening, the time grid, note identifiers and
the clip's next identifier, per-note expression lists, and the attribute
order, omission and number text written on save. Requirement IDs are retained
with explicit partial clauses. Requirements 011, 012, 015 and 017 (the MIDI
key range, key track and list ids, probability groups, and how a refusal is
presented) are not released. No application source, shipped file or public
dependency is included.

The package has 67 cases, each with one independently authored gzip Live Set
fixture. A `loads` case means that no rule in this release refuses the
document; it does not mean that every part of the set opens as in a full set.

All expected results are static-derived and unexecuted. They are not captured
reference behavior. The representation is a comparison convention, not an API
claimed to exist in Live and not a required architecture. No compatibility
claim is made. After publication the release is immutable; corrections
require a new revision.
