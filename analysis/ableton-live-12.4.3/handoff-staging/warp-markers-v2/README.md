# Warp markers and warp settings, release 2

**Reviewed local release.** Read [the contract](spec.md),
[the cases](cases.json), [the role instructions](AGENTS.md),
[the manifest](manifest.json) and [the review disposition](REVIEW.md). The
stated partial scope, narrowed as recorded in the review, is approved as a
contract for a fresh, restricted implementation workspace. Such a workspace
has not been provisioned by this release.

The finite scope is how a decoded Live Set stores the warp markers and warp
settings of an audio clip: where they are, how their text is read when a
document is opened, the defaults of absent settings and the stored codes. It
also covers what the scripting interface's conversions between sample time and
beat time return for a warped clip, and which edits of warp markers through the
scripting interface are refused or accepted, including the exact binary64
arithmetic at the edges of the edit limits and of the beat grid. Requirement
IDs are retained with explicit partial clauses. Requirements 004, 005, 006, 009
and 014 are not released. Nothing that is saved, played or heard is graded,
and no device is part of the release.

The package has 63 cases over 20 XML documents and one generated WAV file of
three seconds of silence. Every document is the same complete Live Set with
one change.

Each expected outcome is labelled static-derived, extracted execution or
computed by extracted-execution rules, as defined in the contract. None is
captured reference behavior. The outcome representation is a comparison
convention, not an API claimed to exist in Live and not a required
architecture. No compatibility claim is made. After publication the release is
immutable; corrections require a new revision.

## Supersession

This release supersedes warp-markers-v1, which stays immutable. Do not use the
warp-markers-v1 fixtures: the target build checks the structure of every Live
Set it opens, and it would refuse 17 of the 18 warp-markers-v1 documents,
although 35 of their cases expect them to open (change 1). Case
WARP-MARKERS-018 is withdrawn and has no expectation (change 11); do not use it
either. For every other case and clause of warp-markers-v1, both releases give
the same expectations. Its other 37 case records are carried unchanged, with
the same IDs and fixture names, and 26 cases are new, for 63 in total.
[The manifest](manifest.json) records the relationship and the superseded
manifest digest.

## Changes from warp-markers-v1

1. **Fixtures are complete Live Sets.** Each warp-markers-v1 document held
   only the clip, or only the sample part, inside a single track. The target
   build refuses a set in which a track with clip slots has no matching freeze
   slots, so it would refuse all 17 clip documents. Every document is now the
   base set of [the contract](spec.md#document-scope-and-preconditions) with
   the same single change as in warp-markers-v1. The changes common to every
   document are these:
   - the freeze slots that the structure check requires: one empty freeze slot
     for each clip slot of the audio and MIDI tracks;
   - the rest of the base set: a MIDI track with a two-note MIDI clip, a
     return track, one send per track mixer, the main and cue tracks, two
     scenes, the transport, the set-level values and the automation target
     identifiers. Every device list is empty. The audio track's identifier is
     now 2 (it was 0) and its second clip slot is empty;
   - in the clip: its region, name, colour, launch and time-signature children,
     and a sample reference to `sample.wav` between `IsWarped` and `WarpMode`.
     The ten value children of REQ-WARP-MARKERS-001 clause 1, the marker list
     and the marker identifiers keep their warp-markers-v1 values and order;
   - tab indentation in place of two spaces.

   Per document:

   | Document | Change from the base set | Cases |
   | --- | --- | --- |
   | `base.xml` | None | 001, 022 to 037, 039 to 045, 048 to 050, 052 to 060 |
   | `not-warped.xml` | `IsWarped` false, as in warp-markers-v1 | 002, 019 to 021, 038, 062 |
   | `sectime-exponent.xml` | Second marker `SecTime="1.0e0"`, as in warp-markers-v1 | 003 |
   | `sectime-leading-space.xml` | Second marker `SecTime=" 1"`, as in warp-markers-v1 | 004 |
   | `beattime-off-grid.xml` | Second marker `BeatTime="2.0000001"`, as in warp-markers-v1 | 005 |
   | `beattime-trailing-text.xml` | Second marker `BeatTime="2junk"`, as in warp-markers-v1 | 006 |
   | `sectime-no-number.xml` | Second marker `SecTime="abc"`, as in warp-markers-v1 | 007 |
   | `beattime-empty.xml` | Second marker `BeatTime=""`, as in warp-markers-v1 | 008 |
   | `settings-absent.xml` | Seven setting elements removed, as in warp-markers-v1 | 009 |
   | `settings-no-value.xml` | Seven setting elements without `Value`, as in warp-markers-v1 | 010 |
   | `transient-resolution-0.xml` | `TransientResolution` 0, as in warp-markers-v1 | 011 |
   | `transient-loop-mode-0.xml` | `TransientLoopMode` 0, as in warp-markers-v1 | 012 |
   | `warp-mode-0.xml` to `warp-mode-3.xml`, `warp-mode-6.xml` | `WarpMode` 0, 1, 2, 3 or 6, as in warp-markers-v1 | 013 to 017 |
   | `first-marker-later.xml` (new) | First marker (0.5 s, beat 1) | 046, 047, 061 |
   | `two-markers.xml` (new) | Two markers: (0 s, beat 0) and (0.0112275449101796407 s, beat 0.03125) | 051, 063 |
   | `shadow-sixteenth.xml` (new) | Shadow marker (2.03125 s, beat 3.0625), 1/16 beat after the last visible marker | 064 |

   `sample.wav` is byte-identical to warp-markers-v1's.
2. **Refusal cases isolate their rule.** WARP-MARKERS-007 and 008 still expect
   a refusal. Their warp-markers-v1 documents were also refused for their
   structure, so the cases did not show that the number text alone refuses
   the document. Now it is the only cause.
3. **Beat bounds of an add (REQ-WARP-MARKERS-015 clause 5).** The 5 to 999 BPM
   tempo rule is replaced by the binary64 beat bounds toward each neighbour.
   Within warp-markers-v1's scope the two give the same outcome. The
   exclusions next to a tempo limit (0.001 BPM) and next to a neighbour's
   sample time (0.0005 s) are withdrawn. WARP-MARKERS-052 to 055, 059 and 060
   are new.
4. **Grid rounding (REQ-WARP-MARKERS-016 clause 1)** is stated as its binary64
   operation sequence. Within warp-markers-v1's scope it gives the same result.
   The exclusion next to a rounding tie (0.001 grid step) is withdrawn.
   WARP-MARKERS-056 to 058 are new.
5. **Conversion values (REQ-WARP-MARKERS-008 clauses 2 to 5)** of
   `sample_to_beat_time` and `beat_to_sample_time` on a warped clip are
   released, for a call right after opening. WARP-MARKERS-039 to 051 are new.
6. **Shadow marker (REQ-WARP-MARKERS-007 clauses 3 and 4).** Its segment
   extends the conversions past the last visible marker, and opening keeps a
   spacing other than 1/32 beat. WARP-MARKERS-064 is new.
7. **Edit clauses (REQ-WARP-MARKERS-015 clauses 3, 4 and 8).** An add whose
   sample time is below the first marker's has no left neighbour; that
   exclusion is withdrawn (WARP-MARKERS-061). `move_warp_marker`, like the
   remove, does not check whether the clip is warped (WARP-MARKERS-062). A
   remove on a list of two markers is accepted; that exclusion is withdrawn
   for the remove and kept for the move (WARP-MARKERS-063).
8. **REQ-WARP-MARKERS-009** stays unreleased, as in warp-markers-v1: no case
   of this release can observe playback.
9. **Provenance and assumptions.** The labels extracted execution and computed
   by extracted-execution rules are new; 22 new cases carry one of them. The
   carried records keep the static-derived label. The stated assumptions now
   also cover the base set opening, the sample rate, the marker list a
   conversion uses and the arm64 build.
10. **Exclusions.** The fixtures' context, the structure rules that decide
    whether a Live Set opens, how a document finds its sample, devices and
    the sample parts of a Sampler or Simpler are newly excluded. Conversion
    values, the cases named in changes 3, 4 and 7, and the three uncertainty
    bands are no longer excluded.
11. **Withdrawn.** WARP-MARKERS-018, and with it REQ-WARP-MARKERS-001 clause 2
    and REQ-WARP-MARKERS-004. Its document needs a Simpler in the MIDI track's
    device list, and whether the target build accepts a device there is not
    established. `simpler-empty-markers.xml` is removed, and no fixture holds a
    device.
12. **Unchanged.** Every other clause, the 37 carried case records and the WAV
    are as in warp-markers-v1.
