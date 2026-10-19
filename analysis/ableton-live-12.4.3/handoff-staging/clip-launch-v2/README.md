# Clip launch settings in Live Set documents, release 2

**Reviewed local release.** Read [the contract](spec.md), [the cases](cases.json),
[the role instructions](AGENTS.md), [the manifest](manifest.json) and
[the review disposition](REVIEW.md). The stated partial scope, with the
narrowing recorded in the review, is approved as a contract for a fresh,
restricted implementation workspace. Such a workspace has not been provisioned
by this release.

The finite scope is how the decoded XML of a Live Set stores each clip's launch
settings and the set's global and record quantization: where each value is,
what each value means and how it is labeled, which text is accepted or refused
when a document is opened, what missing and repeated items do, the
follow-chance and follow-time corrections made on opening, the conversion of
follow actions in two older format versions, and what is written on save. New
in this release is a value contract for the quantization grid: the grid length
of each quantization value, the grid a clip's setting denotes, the rounding of
a beat to the beat lattice and the grid boundary at or after it. These are
functions of explicit inputs, not launch timing. Requirement IDs
are retained with explicit partial clauses. Requirements 008, 010 and 019 to
023, launch timing and every other effect on launching or playback remain
unreleased. No application source, shipped file or public dependency is
included.

The 100 cases use 62 independently authored fixtures, each a complete minimal
Live Set, and one generated sample. Each expected output is labeled
static-derived or extracted execution, as defined in the contract. None is
captured reference behavior. The representation is a comparison convention,
not an API claimed to exist in Live or a required architecture. No
compatibility claim is made. After publication the release is immutable;
corrections require a new revision.

## Supersession

This release supersedes clip-launch-v1. Opening a Live Set checks its
structure, and a set whose tracks have clip slots but no matching freeze slots
is refused. 49 of the 50 clip-launch-v1 fixtures have that defect, although
their cases expect most of them to open; the cases that expect a refusal are
refused for that defect as well as for the reason they test. clip-launch-v1
stays immutable and its clauses stay correct for its scope, but its fixtures
are not valid Live Sets and must not be used to judge its expectations. Its 50
cases keep their IDs and case records unchanged here; only their fixtures are
rebuilt. 50 cases are new, for 100 in total. [The manifest](manifest.json)
records the relationship and the superseded manifest digest.

## Changes from clip-launch-v1

1. **Fixtures.** Every fixture is a complete minimal Live Set. The fixture
   changes are listed [below](#fixture-changes).
2. **Precondition.** clip-launch-v1 said that the absence of other set content
   from a fixture must not by itself change a judged outcome. That does not
   hold for set structure, so the statement is replaced: each fixture holds the
   structure a set needs to open, and a refusal case changes exactly one item.
3. **REQ-CLIP-LAUNCH-012.** Chances outside 0 to 100 now have expectations
   within the stated ranges: they are rescaled by the same rule, and each
   result is limited to 0 to 100. clip-launch-v1 assumed that the rescaled
   values are kept as computed; that is now part of the rule. Negative zero
   counts as zero in the both-zero test. CLIP-LAUNCH-051 to 059 are new.
4. **REQ-CLIP-LAUNCH-013.** The rounding is stated as a binary64 formula. More
   than 10⁻⁹ from a halfway point it gives the same result as clip-launch-v1's
   rule; nearer to such a point, where clip-launch-v1 gave no expectation, the
   formula decides. That exclusion is removed. CLIP-LAUNCH-060 to 062 are new.
5. **REQ-CLIP-LAUNCH-015 to 018** are released as a value contract only: the
   grid length of each value, the grid a clip's setting denotes (a clip value
   of −99 counts as Global), the rounded beat and the boundary, including a
   triplet case in which the boundary is the next grid line, and the boundary
   with no grid. They define values, not launch timing: the boundary is not
   stated to be the beat at which a launched clip starts, and which global
   value and time signatures a launch uses is excluded. CLIP-LAUNCH-063 to 100
   are new.
6. **REQ-CLIP-LAUNCH-011.** Follow chances outside 0 to 100 now follow
   REQ-CLIP-LAUNCH-012, and the −99 rule of REQ-CLIP-LAUNCH-016 is named. The
   value held for other out-of-range values stays excluded. A follow time
   outside 0 to below 1,000,000 has no expectation, not even that the document
   opens.
7. **Provenance.** The extracted-execution label is new. Every new case carries
   it; the contract states the assumptions it rests on. Carried records keep
   the static-derived label.
8. **Exclusions.** Narrowed: chances in the wider ranges, negative zero as a
   follow chance, follow times near a halfway point, and `11.0_405` scenes in
   the fixtures' form. Added: launch timing, reading the clip and song time
   signatures, follow times outside 0 to below 1,000,000, and the fixtures'
   other content.
9. **Unchanged.** Every other clause of clip-launch-v1, and every carried case
   record, is unchanged.

## Fixture changes

Every clip-launch-v1 fixture is replaced. Each new fixture of CLIP-LAUNCH-001
to 050 is the template set described in the
[fixture provenance](spec.md#fixture-provenance), in the case's format version,
with the change from a new clip that the clip-launch-v1 fixture made. In every
carried fixture the envelope, `GlobalQuantisation`, `AutoQuantisation`, every
launch element and follow-action item of each clip that clip-launch-v1 had, the
old-form follow items of `11.0_405` clips and the first scene's follow action
are identical to clip-launch-v1. The changes, all made so that the set opens,
are:

1. **All 50.** Added: `NextPointeeId`; for every track its name, colour,
   group Id −1, output, mixer with its automation and modulation targets, send
   and an empty device chain; on the MIDI track a volume automation envelope;
   an audio track and a return track; `HasStop` on each session slot; a second
   session slot on each player track and, on each, a freeze sequencer with as
   many empty slots as session slots; in each clip its start, end,
   loop, name, colour, time signature, clip envelopes, warp state and notes or
   sample reference and warp markers; the main track, cue track, send-pre item,
   transport and `CrossfadeCurve`; the sample file `Samples/T11-tone.wav`. Text
   is now tab-indented (clip-launch-v1: two spaces).
2. **Clips added.** The session audio clip, at the values of a new clip, is
   added in every fixture except CLIP-LAUNCH-004. The session MIDI clip, at the
   values of a new clip, is added in CLIP-LAUNCH-004, whose changed clip is the
   audio clip, and in CLIP-LAUNCH-005, whose changed clip is the arrangement
   clip.
3. **CLIP-LAUNCH-005.** The arrangement clip has the template's MIDI clip form
   and lies in the MIDI track's main sequencer, after its session slots.
4. **Scenes.** CLIP-LAUNCH-001 to 040 gain two scenes. CLIP-LAUNCH-046 to 050
   keep the first scene's follow action and gain a second scene and the
   first scene's name, colour, tempo and time-signature items; in
   CLIP-LAUNCH-048 the first scene still has no follow action.
5. **CLIP-LAUNCH-041 to 045 (`11.0_405`).** The template in that version's
   form: the main track is `MasterTrack`, two name-only scenes are items of
   `SceneNames`, colours are `ColorIndex`, and the added audio clip also uses
   the old clip form, with follow items 4, 0, 0, 1 and 0. Elements that
   version does not define are absent.
6. **CLIP-LAUNCH-046 to 049 (`12.0_12117`).** The template in that version's
   form, without the elements that version does not define.
