# MIDI clip note storage in Live Sets, release 2

**Reviewed local release.** Read [the contract](spec.md),
[the cases](cases.json), [the role instructions](AGENTS.md),
[the manifest](manifest.json) and [the review disposition](REVIEW.md). The
stated partial scope, with the clarifications recorded in the review, is
approved as a contract for a fresh, restricted implementation workspace.
Such a workspace has not been provisioned by this release.

The finite scope is the same as in midi-note-storage-v1. It covers how a Live
Set stores the notes of a MIDI clip: the note structure, which note text is
accepted or refused when the set is opened, the defaults and limits applied on
opening, the time grid, note identifiers and the clip's next identifier,
per-note expression lists, and the attribute order, omission and number text
written on save. New in this release are negative zero, the time grid next to
halfway points and the value limits at their binary32 bounds. Requirement IDs
are retained with explicit partial clauses. Requirements 011, 012, 015 and 017
(the MIDI key range, key track and list ids, probability groups, and how a
refusal is presented) are not released. No application source, shipped file
or public dependency is included.

The package has 72 cases, each with one independently authored gzip Live Set
fixture. A `loads` case means that no rule in this release refuses the
document; it does not mean that every part of the set opens as in a full set.

Each expected result is labeled static-derived or extracted execution, as
defined in the contract. None is captured reference behavior. The
representation is a comparison convention, not an API claimed to exist in Live
and not a required architecture. No compatibility claim is made. After
publication the release is immutable; corrections require a new revision.

## Supersession

This release supersedes midi-note-storage-v1. midi-note-storage-v1 stays
immutable, and its clauses and expectations remain valid, but its fixtures
must not be used: they lack Live Set structure that the target needs to open a
set (change 1). All 67 of its cases keep their IDs and case records. Each
fixture is rebuilt with the two additions of change 1 and nothing else. Five
cases are new, for 72 in total. [The manifest](manifest.json) records the
relationship and the superseded manifest digest.

## Changes from midi-note-storage-v1

1. **Fixtures rebuilt.** Every fixture gains exactly two elements. Inside the
   MIDI track's `DeviceChain`, after `MainSequencer`, a `FreezeSequencer`
   whose `ClipSlotList` holds one empty slot. After `Tracks`, a `Scenes` list
   holding one scene. Live Set structure is outside this release. Under the
   target's structure rules, a set whose MIDI track has a session slot but no
   matching freeze slot is not opened. The midi-note-storage-v1 fixtures would
   therefore be refused although 51 of their cases expect `loads`, and its 16
   refused cases would not isolate the rule they test. Without one scene per
   session slot, whether the set opens is not established. No other element,
   attribute or value changes. MNS-012, whose repeated attribute makes the XML
   not well-formed, gets the same additions, so that repeat is its only
   defect.
2. **Negative zero** (REQ-002, 005, 006, 007 and 016). The text `-0` reads as
   negative zero. A `Velocity` of −0 becomes 1, while an `OffVelocity` or
   `Probability` of −0 is kept. A `Time` or `Duration` of −0 is stored as
   positive zero, and a `Time` that rounds to zero from below is stored as
   negative zero. Negative zero is saved as `-0`. REQ-007 now says that a
   note whose `Duration` is positive zero saves unchanged; a `Duration` of −0
   is saved as `0`. REQ-006's statement that values on the grid are
   unchanged now excepts negative zero. The midi-note-storage-v1 exclusion of
   negative zero is narrowed: it remains only for `VelocityDeviation`, an
   event's `TimeOffset` and `Value`, and the curve controls. MNS-023 (from the
   parent draft), MNS-073 and MNS-074 are new.
3. **Time grid next to halfway points** (REQ-006). The stated binary64 formula,
   not exact rounding, defines the stored value next to a halfway point.
   MNS-072 is new.
4. **Limits at the binary32 bounds** (REQ-005). A `Velocity` one binary32 step
   above 127 or below 1 is limited. MNS-075 is new.
5. **Provenance.** The extracted-execution label is new, and the five new
   cases carry it. The carried cases keep their records and the static-derived
   label. The contract states the assumptions the new label rests on. The
   general assumption on number text now also names ties to even on save,
   which REQ-016 already stated, and MNS-072, which depends on the
   nearest-value reading of its text.
6. **Unchanged.** Every other clause, case and expectation of
   midi-note-storage-v1 is carried unchanged.
