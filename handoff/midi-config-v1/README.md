# MIDI configuration assignment release 1

**Reviewed local release.** Read [the contract](spec.md), [cases](cases.json),
[role instructions](AGENTS.md) and [review disposition](REVIEW.md). The stated
partial scope is approved as a contract for a fresh, restricted implementation
workspace. Such a workspace has not been provisioned by this release. No passing
reference comparison is claimed.

The finite scope is interpreting master-volume, cue-volume and crossfader CC
assignments in a user configuration. Existing requirement IDs are retained with
explicit partial clauses. The broader MIDI feature is not released by this
release. No application source, original fixture or public dependency is
included.

All expected outputs are reviewed static-derived expectations, not
captured reference behavior. The small text fixtures were independently authored
for these cases. The normalized assignment representation is a comparison
convention; it is not an API claimed to exist in Live or a required implementation
architecture. [The manifest](manifest.json) records exact contents and completed
review. This release is immutable; corrections require a new reviewed revision.
