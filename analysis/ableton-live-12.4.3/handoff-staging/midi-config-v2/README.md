# MIDI configuration interpretation release 2

**Reviewed local release.** Read [the contract](spec.md), [cases](cases.json),
[role instructions](AGENTS.md), [the manifest](manifest.json) and
[the review disposition](REVIEW.md). The stated partial scope, narrowed as
recorded in the review, is approved as a contract for a fresh, restricted
implementation workspace. Such a workspace has not been provisioned by this
release.

The finite scope is how a user configuration file is interpreted: which
assignments are enabled, their MIDI addresses, the device, mixer, transport and
drum-pad targets they name, map-mode labels, button kinds and the device
parameter bank span. Existing requirement IDs are retained with explicit
partial clauses. Requirements 001 and 004 and every runtime effect remain
unreleased. No application source, shipped file or public dependency is
included.

This release supersedes midi-config-v1 as a strict superset.
Its 54 cases keep their IDs, fixture bytes and logical expectations in a wider
representation; 55 cases are new, for 109 in total. The spec lists the changes.

All expected outputs are static-derived and unexecuted, not captured reference
behavior. The representation is a comparison convention, not an API claimed to
exist in Live or a required architecture. No compatibility claim is made.
After publication the release is immutable; corrections require a new revision.
