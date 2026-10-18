# Track mixer values in Live Set documents, release 1

**Reviewed local release.** Read [the contract](spec.md),
[the cases](cases.json), [the role instructions](AGENTS.md),
[the manifest](manifest.json) and [the review disposition](REVIEW.md). The
stated partial scope, with the corrections recorded in the review, is approved
as a contract for a fresh, restricted implementation workspace. Such a
workspace has not been provisioned by this release.

The finite scope is how the decoded XML of one Live Set format version stores
each track's mixer values (volume, pan, pan mode, split-stereo pans, sends,
track switch and crossfade assignment), the main track's crossfader and the
set's crossfade curve: where each value is, which value it takes when the
document is opened, and the text or name the application gives to it.
Requirement IDs are retained with explicit partial clauses. Requirements 005
and 010 to 015 (fader curves, what is written on save, the effect on audio and
out-of-range values) are not released. No application source, shipped file or
public dependency is included.

The package has 37 cases, each with one independently authored fixture. All
expected values, texts and names are static-derived and unexecuted. They are
not captured reference behavior. The representation is a comparison
convention, not an API claimed to exist in Live and not a required
architecture. No compatibility claim is made. After publication the release is
immutable; corrections require a new revision.
