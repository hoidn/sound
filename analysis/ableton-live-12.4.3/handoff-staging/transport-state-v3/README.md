# Transport state in Live Set documents, release 3

**Reviewed local release.** Read [the contract](spec.md), [cases](cases.json),
[role instructions](AGENTS.md), [the manifest](manifest.json) and
[the review disposition](REVIEW.md). The stated partial scope, with the
clarifications recorded in the review, is approved as a contract for a fresh,
restricted implementation workspace. Such a workspace has not been provisioned
by this release.

The finite scope is the same as in transport-state-v2. It covers how the decoded
XML of one Live Set format version stores six values: the arrangement loop
switch, loop start, loop length, playback position, tempo and time-signature
code. For each it states where the value is, which text is accepted or refused
when a document is opened, what missing, duplicated and unknown items do, and
the exact text written on save. Existing requirement IDs are retained with
explicit partial clauses. Requirements 009 and 012 and every runtime effect
remain unreleased. No application source, shipped file or public dependency is
included.

The 33 cases use independently authored minimal XML fixtures. Each expected
output is labeled static-derived or extracted execution, as defined in the
contract. None is captured reference behavior. The representation is a
comparison convention, not an API claimed to exist in Live or a required
architecture. No compatibility claim is made. After publication the release is
immutable; corrections require a new revision.

## Supersession

This release supersedes transport-state-v2, which stays immutable. Its
clauses, case records and expectations are carried unchanged, but its fixtures
must not be used to judge any case: the documents expected to open cannot, and
the refused ones do not isolate the text they test (change 1).
All 33 cases keep their IDs and records, and every fixture changes (change 2).
[The manifest](manifest.json) records the relationship, the superseded
manifest digest and the fixture changes.

## Changes from transport-state-v2

1. **Defect corrected: the fixtures had no track.** Opening a Live Set checks
   its track list, and a set whose `Tracks` element is absent or holds no audio,
   MIDI or group track is not opened (static-derived). No transport-state-v2 fixture
   has a `Tracks` element. So the 23 cases that expect a document to open
   (TS-001 to 003, 006, 008, 011 to 014, 016, 020 to 022, 024 to 028, 030, 032,
   034, 036 and 037) could not hold for those files. The 10 cases that expect a
   refusal (TS-004, 005, 007, 009, 010, 015, 029, 031, 033 and 035) were refused
   for that reason as well as for the text they test, so they did not isolate
   it. transport-state-v2 stated that the absence of other Live Set content must
   not by itself change a judged outcome; for the track list that was wrong.
   The 18 transport-state-v1 fixtures, which transport-state-v2 carried byte for
   byte, have the same defect.
2. **Fixture change, all 33 fixtures.** Each of `fixtures/TS-001.xml` to
   `TS-016.xml`, `TS-020.xml` to `TS-022.xml` and `TS-024.xml` to `TS-037.xml`
   is the transport-state-v2 file of the same name with 21 lines inserted
   directly after the `<LiveSet>` start tag. The lines are the `Tracks` element
   shown in [the preconditions](spec.md#document-scope-and-preconditions): one
   MIDI track with fixed values and empty session and freeze clip lists. No
   line of a transport-state-v2 fixture is changed, removed or reordered. The
   fixtures remain ASCII with LF endings and no tabs.
3. **Expectations re-checked; none changed.** With the track, each of the 23
   documents opens and reads the same transport values as before, and the saved
   values judged are unaffected: the track is a separate part of the document
   and none of the judged paths lies inside it. Each of the 10 refused
   documents differs from the unchanged document of TS-022, which opens, only in
   the tested `Transport` child or `Manual` element.
4. **Preconditions and exclusions.** The precondition on missing content now
   names the track list. A document whose `Tracks` element is absent or holds no
   audio or MIDI track, and track content other than the fixtures' one MIDI
   track, are added to the inputs with no expectation.
5. **Parent revision.** The parent is SPEC-TRANSPORT-STATE revision 4.
   Revision 4 states the clarifications recorded in the transport-state-v2
   review, which that release already carries: the REQ-011 band without
   expectation, the logarithm-accuracy assumption, and the library dependence
   of reading `-0` and of the save text. It settles no clause beyond
   transport-state-v2, so no clause or case is added.
6. **Unchanged.** Every requirement clause, case record, expectation,
   provenance label, stated assumption and other exclusion of
   transport-state-v2 is carried unchanged.
