# Track mixer values in Live Set documents, release 2

**Reviewed local release.** Read [the contract](spec.md), [cases](cases.json),
[role instructions](AGENTS.md), [the manifest](manifest.json) and
[the review disposition](REVIEW.md). The stated partial scope, with the
narrowing recorded in the review, is approved as a contract for a fresh,
restricted implementation workspace. Such a workspace has not been provisioned
by this release.

The finite scope is how the decoded XML of one Live Set format version stores
each track's mixer values (volume, pan, pan mode, split-stereo pans, sends,
track switch and crossfade assignment), the main track's crossfader and the
set's crossfade curve: where each value is, which value it takes when the
document is opened, and the text or name the application gives to it. As
computed values at listed inputs, it also covers the volume and send fader
curves (fader position to gain and back), the pan-law gains and the levels of
the seven crossfade curves. Requirement IDs are retained with explicit partial
clauses. Requirements 010, 011, 012 and 015 (what is written on save, the gains
the audio path applies, and out-of-range values) are not released, and neither
is where or when the audio path applies the computed values. No application
source, shipped file or public dependency is included.

The package has 80 cases. The 37 cases carried from mixer-values-v1 each open
one independently authored fixture, a complete minimal Live Set. The 43 new
cases compute values from listed inputs and have no fixture. Carried
expectations are static-derived, and new ones come from extracted execution of
the original program's code, as defined in the contract. None is captured
reference behavior. The representation is a comparison convention, not an API
claimed to exist in Live and not a required architecture. No compatibility
claim is made. After publication the release is immutable; corrections require
a new revision.

## Supersession

This release supersedes mixer-values-v1, which stays
immutable. Its 37 case records are carried unchanged: the same IDs, inputs,
purposes, expectations, labels and comparators. Its fixtures are replaced. The
mixer-values-v1 fixtures are minimal documents that lack parts of a Live Set,
for example the list that holds one send setting per return track. Whether a
set without them opens is not established, and mixer-values-v1 relied on such
absence not changing a judged outcome. [The manifest](manifest.json) records
the relationship, the superseded manifest digest and each replaced fixture's
digest.

## Changes from mixer-values-v1

1. **Fixtures.** All 37 fixtures are rebuilt as complete Live Sets from one new
   template set ([fixture provenance](spec.md#fixture-provenance)). Each is the
   template set with exactly the changes its case had in mixer-values-v1, so
   every case edit, value text and expectation is unchanged. Every fixture
   changes in these ways:
   - track order MIDI, audio, return (was audio, MIDI, return); track Ids 1,
     2 and 3 (were 11, 12 and 13);
   - each track except the cue track gains `Name`, `Color`,
     `AutomationEnvelopes` (empty, except the main track's tempo and
     time-signature envelopes), `TrackGroupId` −1 (not on the main track) and
     `AudioOutputRouting`;
   - the MIDI and audio tracks gain session and freeze clip lists with two
     empty clip slots each; the MIDI, audio, return and main tracks gain an
     empty device list;
   - each mixer gains `On` as its first child; each value element with a
     `Manual` child gains an `AutomationTarget` and, as the contract states
     for each, a `MidiControllerRange` and a `ModulationTarget`; the main
     mixer gains `Tempo` (120) and `TimeSignature` (201) before `CrossFade`;
   - `LiveSet` gains `NextPointeeId` 67, `SendsPre` with one `false` item,
     two scenes, `Transport`, `GlobalQuantisation` 4 and `AutoQuantisation` 0;
   - indentation is one tab per level (was two spaces). The envelope, ASCII
     text, line-feed endings and final newline are unchanged.

   The manifest lists each fixture's case edits and its mixer-values-v1
   digest.
2. **Preconditions.** The statement that set content absent from a fixture
   must not by itself change a judged outcome is withdrawn. Every fixture has
   the template set's structure, and a document with another structure has no
   expectation.
3. **REQ-MIXER-VALUES-005, new partial clause.** The volume and send fader
   curves and both conversions between fader position and gain, as computed
   values at the listed inputs, and the exact round trip at seven curve
   points. Cases MIXER-VALUES-038 to 064.
4. **REQ-MIXER-VALUES-013, new partial clause.** The pan-law gains as
   computed values, for a pan-mode amount and a gain of 0 or 1, at the listed
   inputs. Cases MIXER-VALUES-065 to 073.
5. **REQ-MIXER-VALUES-014, new partial clause.** The levels of the seven
   crossfade curves at seven positions, as computed values. Cases
   MIXER-VALUES-074 to 080. REQ-MIXER-VALUES-009 now points to it for the
   curve levels.
6. **REQ-MIXER-VALUES-008.** The `On`/`Off` rule is unchanged and is now also
   supported by extracted execution. MIXER-VALUES-001 and 030 keep their
   records and the static-derived label.
7. **Provenance.** The extracted-execution label is new and carried by every
   new case. Its definition names what ran and what did not. Assumptions for
   it are stated, among them an accuracy assumption for the exact round trip.
8. **Representation.** A new action, `compute`, with a function, its inputs
   and a comparison per function. The `open` representation is unchanged.
9. **Comparison obligation.** Each fixture is now the set to open. The
   computed values have no observation channel in the original application.
10. **Exclusions.** REQ-MIXER-VALUES-005, 013 and 014 move from unreleased to
    partial, and their remainders are listed. Added: documents whose
    structure differs from the template set; computed inputs other than those
    listed; the meaning of `SendPreBool`; where and when the audio path
    applies the computed gains; whether a set with another structure opens.
11. **Unchanged.** Every other clause, case record and expectation of
    mixer-values-v1.
