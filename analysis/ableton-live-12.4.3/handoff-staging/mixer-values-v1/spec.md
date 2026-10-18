# Track mixer values in Live Set documents, release 1

Target: Ableton Live 12 Suite 12.4.3 (2026-07-07_e3d8be4d07), macOS, Apple
silicon (arm64). Features: FEAT-AUDIO with FEAT-PERSISTENCE. Parent
specification identity: SPEC-MIXER-VALUES revision 1. Release:
mixer-values-v1. Only the clauses explicitly included below are in scope. No
other clause of a listed requirement is implicitly approved. This document is
self-contained.

**Status: reviewed local release.** A separate review approved the clauses
below with the corrections recorded in [the review disposition](REVIEW.md).

## What the contract means

Every track of a Live Set has a mixer: volume, pan, pan mode, a left and a
right split-stereo pan, one send per return track, a track switch and a
crossfade assignment. The main track also has the crossfader, and the set has
a crossfade curve. For one document format version, this contract describes:

- where each of these values is stored, for each track type;
- which value it takes when the document is opened;
- the value text of volumes and sends (decibels), of pans, and of the track
  switch;
- the names of the pan mode, crossfade assignment and crossfade curve codes.

It does not describe what the values do to audio, what is written on save,
fader positions, editing, or which part of the user interface shows which text.

All rules and expected results are **static-derived**: they were derived for
the target build without running it. None is an observed execution of the
original application, and none was run against a candidate. No compatibility
result is established. The original application remains the authority for a
later comparison. A few derived steps rest on assumptions that were not traced
to the end: that a mixer value written as a plain decimal number is read as
the nearest binary32 number, as other binary32 values of a document are; that
the name of a code is its entry in the lists below; and that some part of the
user interface shows the value texts below, computed from the value as read.
The application's base-10 logarithm may also differ from the correctly rounded
result in the last binary32 digit, so inputs near a text boundary have no
expectation. The comparison obligation below covers these points.

## Document scope and preconditions

- The input is the decoded XML of a Live Set: well-formed XML 1.0 in UTF-8
  whose root element is `Ableton` with exactly the attributes
  `MajorVersion="5"`, `MinorVersion="12.0_12402"` and `SchemaChangeCount="1"`,
  and whose first child is `LiveSet`. Every fixture uses this envelope. The
  compressed file container, other root elements and attributes, other format
  versions and their upgrade are outside this release.
- The **text** of a value is its attribute value after standard XML
  attribute-value decoding. Paths are relative to `/Ableton/LiveSet`.
- **Opens** means the document is read without refusal. No case in this
  release expects a refusal.
- Numbers use `.` as the decimal separator. Expectations assume a host locale
  whose decimal separator is `.`; locale-dependent behavior is excluded.
- A full Live Set contains much more than the fixtures: devices, clips, scenes,
  the transport, and further mixer children such as controller ranges,
  automation targets and view state. That content is outside this release. Its
  absence from a fixture must not by itself change a judged outcome.
- **binary32** is IEEE 754 single precision. A binary32 value is compared
  after its exact conversion to binary64.

### Value text in documents

Expectations exist only for these spellings:

| Kind | Accepted text | Value read |
| --- | --- | --- |
| Number | an optional `-`, one or more ASCII digits, then optionally `.` and one or more ASCII digits | the binary32 number nearest to the decimal number |
| Boolean | `true` or `false` | true or false |
| Code | one or more ASCII digits | the decimal integer |

Every number in the fixtures lies well away from a point halfway between two
binary32 numbers, so it does not matter whether the decimal is rounded to
binary32 directly or through binary64 first.

## Mixers in the fixtures

Every fixture has exactly one audio track, one MIDI track and one return track,
in that order inside `Tracks`, plus the main and the cue track. The cases name
the mixers as follows:

| Name | Mixer element |
| --- | --- |
| `audio` | `Tracks/AudioTrack/DeviceChain/Mixer` |
| `midi` | `Tracks/MidiTrack/DeviceChain/Mixer` |
| `return` | `Tracks/ReturnTrack/DeviceChain/Mixer` |
| `main` | `MainTrack/DeviceChain/Mixer` |
| `cue` | `PreHearTrack/DeviceChain/Mixer` (the cue track) |
| `set` | `LiveSet` itself, for the crossfade curve |

## Selected requirement clauses

### REQ-MIXER-VALUES-001 — partial: mixer location and values per track type

- Every audio track (`AudioTrack`), MIDI track (`MidiTrack`), group track
  (`GroupTrack`) and return track (`ReturnTrack`), the main track
  (`MainTrack`) and the cue track (`PreHearTrack`) stores one mixer at
  `<track element>/DeviceChain/Mixer`. No case exercises a group track.
- A mixer holds these value elements, in this relative order:

| Value | Element in the mixer | Text read | Kind |
| --- | --- | --- | --- |
| Sends | `Sends`, holding `TrackSendHolder` elements | `TrackSendHolder/Send/Manual/@Value` | number |
| Track switch | `Speaker` | `Manual/@Value` | Boolean |
| Solo sink | `SoloSink` | `@Value` | Boolean |
| Pan mode | `PanMode` | `@Value` | code |
| Pan | `Pan` | `Manual/@Value` | number |
| Left split pan | `SplitStereoPanL` | `Manual/@Value` | number |
| Right split pan | `SplitStereoPanR` | `Manual/@Value` | number |
| Volume | `Volume` | `Manual/@Value` | number |
| Crossfade assignment | `CrossFadeState` | `Manual/@Value` | code |

- The main mixer also holds the crossfader `CrossFade`, read from
  `CrossFade/Manual/@Value` (number), after these elements. The set's
  crossfade curve is read from `LiveSet/CrossfadeCurve/@Value` (code).
- The fixtures follow this order; documents with another order have no
  expectation. Elements with the same names elsewhere, for example in devices
  and clips, are different values.
- The rules of REQ-MIXER-VALUES-002 to 009 are the same for every track type.
  Only the sends (REQ-MIXER-VALUES-003) and the main-only crossfader differ.

### REQ-MIXER-VALUES-002 — partial: volume domain

`Volume/Manual` is a linear gain (1 is 0 dB), held as binary32. Expectations
exist only for values from 0.0003162277571 to 1.99526238 inclusive, the
binary32 values of these two texts. They lie within 0.000001 dB of −70 dB
and +6 dB. The upper one is one binary32 step above the binary32 number
nearest to 10^(6/20).

### REQ-MIXER-VALUES-003 — partial: sends

- The `Sends` element of an audio, MIDI, group or return mixer holds one
  `TrackSendHolder` per return track of the set. A return mixer holds a send to
  every return track, its own included. The main and cue mixers hold none
  (`<Sends />`) and have no sends, also when the set has return tracks.
- Expectations exist only for documents with exactly one return track. The
  single `TrackSendHolder`, with `Id="0"`, is the send to that return track.
- `Send/Manual` is a linear gain held as binary32. Expectations exist only for
  values from 0.0003162277571 (−70 dB) to 1 (0 dB) inclusive.
- The fixtures store `EnabledByUser` as `true` on the audio and MIDI mixers'
  sends and `false` on the return mixer's own send. Its meaning is not
  released, and the return mixer's own send is not judged.

### REQ-MIXER-VALUES-004 — partial: pan, split pans and pan mode

- `Pan/Manual`, `SplitStereoPanL/Manual` and `SplitStereoPanR/Manual` are held
  as binary32, from −1 (left) to 1 (right) inclusive.
- `PanMode/@Value` code 0 is named `Stereo` and code 1 `Split Stereo`.

### REQ-MIXER-VALUES-006 — partial: volume and send value text

Applies to volume and send values g in the ranges of REQ-MIXER-VALUES-002 and
003.

1. Let L be log10(g) rounded to binary32, and dB the product L × 20 rounded to
   binary32.
2. If dB ≤ −69.7, the text is `-inf dB`.
3. Otherwise, if dB × 1000 rounds to the integer 0 (that is, |dB| < 0.0005),
   the text is `0.0 dB`, without a minus sign.
4. Otherwise dB is written in fixed-point notation with three digits after the
   decimal point, rounded to nearest. Trailing `0` characters are removed while
   more than one digit follows the point. A space and `dB` are appended.

Examples: 1 → `0.0 dB`; 0.5011872053 → `-6.0 dB`; 0.5 → `-6.021 dB`;
0.25 → `-12.041 dB`; 0.30725 → `-10.25 dB`; 0.7367056608 → `-2.654 dB`;
1.5 → `3.522 dB`; 1.99526238 → `6.0 dB`; 0.99999 → `0.0 dB`;
0.0003311311302 (−69.6 dB) → `-69.6 dB`; 0.0003235936455 (−69.8 dB) →
`-inf dB`; 0.0003162277571 → `-inf dB`.

Values whose exact decibel value 20 × log10(g) lies within 0.00005 dB of −69.7,
of ±0.0005, or of a number halfway between two consecutive multiples of 0.001
have no expectation.

### REQ-MIXER-VALUES-007 — partial: pan value text

Applies to `Pan`, `SplitStereoPanL` and `SplitStereoPanR`. Let p be the
binary32 value.

- If −0.01 ≤ p ≤ 0.01, the text is `C`.
- Otherwise |p| × 50, computed exactly, is rounded to the nearest integer and
  written in decimal digits, followed by `L` when p < 0 or `R` when p > 0.
- The binary32 value counts, not the decimal text: `0.33` is read as
  0.3300000131…, 50 times that is 16.500000656…, and the text is `17R`.

Examples: −1 → `50L`; −0.6 → `30L`; −0.5 → `25L`; 0.2 → `10R`; 0.5 → `25R`;
1 → `50R`; 0.004999999888 → `C`; 0.01 → `C` (its binary32 value is below
0.01); 0.0101 → `1R`; −0.0101 → `1L`. The values −0.75, −0.25, 0.25 and 0.75,
for which |p| × 50 is exactly halfway between two integers, have no
expectation.

### REQ-MIXER-VALUES-008 — partial: track switch value text

- `Speaker/Manual` is a Boolean. Its value text is `On` for true and `Off` for
  false.
- The fixtures store `SoloSink` as `false`. Its meaning is not released.

### REQ-MIXER-VALUES-009 — partial: crossfade assignment, crossfader and crossfade curve

- `CrossFadeState/Manual` code 0 is named `A`, 1 `None` and 2 `B`.
- The crossfader is `MainTrack/DeviceChain/Mixer/CrossFade/Manual`, held as
  binary32 from −1 to 1 inclusive. Which end of the crossfader favors A or B is
  not released.
- `LiveSet/CrossfadeCurve/@Value` names the crossfade curve: 0 `Dipped`,
  1 `Intermediate`, 2 `Constant Power`, 3 `Slow Fade`, 4 `Slow Cut`,
  5 `Fast Cut`, 6 `Transition`. The shapes of the curves are not released.

## Acceptance representation and comparison

[cases.json](cases.json) lists 37 cases. Each has one input fixture, the
action `open` (open the document and change nothing) and an expected result
with these parts:

| Field | Meaning |
| --- | --- |
| `outcome` | `opens` |
| `values` | Map from `<mixer>/<element>` (mixer names as above; `set/CrossfadeCurve` for the set) to an object with `value` and, where defined, `text` or `name` |
| `send_counts` | Map from mixer name to its number of sends; present in the first case only |

The element names in `values` are `Volume`, `Pan`, `SplitStereoPanL`,
`SplitStereoPanR`, `PanMode`, `Speaker`, `CrossFadeState`, `CrossFade` (main
only), `Send` (the send to the set's single return track) and
`CrossfadeCurve`.

- `value` is a JSON number for a binary32 value and compares exactly after the
  binary32 value's conversion to binary64; a JSON Boolean for the track switch;
  a JSON integer for a code. All compare exactly.
- `text` is the value text of REQ-MIXER-VALUES-006, 007 or 008 and compares as
  an exact string.
- `name` is the name of a code (REQ-MIXER-VALUES-004 or 009) and compares as an
  exact string.
- `send_counts` compares exactly.
- Anything a case does not list is not judged, including the values of the
  return mixer's own send.

This is a **project comparison representation**, not an API claimed to exist
in Live and not a required design. A candidate adapter may translate its own
result into these labels. Each case starts from its fixture alone. Reading has
no timing tolerance, cancellation step or teardown within this scope, so those
case kinds are omitted.

## Reference comparison obligation (not executed)

A later comparison against the original application needs a full Live Set per
case. The validation analyst builds it from an otherwise unchanged set whose
root carries the fixture's `MajorVersion`, `MinorVersion` and
`SchemaChangeCount` values and which has exactly one audio track, one MIDI
track and one return track. In each of the five mixers, the analyst replaces
the value texts of REQ-MIXER-VALUES-001 (each `Manual` value, `PanMode`,
`SoloSink`, the send's `Manual` and its `EnabledByUser`) with the fixture's,
and replaces the set's `CrossfadeCurve` value. In that set no automation, clip
envelope, modulation or MIDI or key mapping targets a mixer value, and the host
locale uses `.` as the decimal separator. Each value is observed after opening,
before any control is touched.

- The observation channel for `value` is chosen by the validation analyst. A
  channel that rounds must be compared at its rounding.
- A `text` observation must come from a place where the application shows the
  value text in the forms of this release: with ` dB` and `-inf dB` for
  volumes and sends, with `C`, `L` or `R` for pans, and as `On` or `Off` for
  the track switch. An observation that
  shows another form, for example the digits without the unit, is
  inconclusive, not a mismatch.
- A `name` observation must come from a place that shows the name of the code,
  for example a list of the choices.

None of this has been run.

## Exclusions and deferred obligations

Requirements not released:

- **REQ-MIXER-VALUES-005** (volume and send fader curves, from fader position
  to gain and back): positions are not observable within this release, and the
  curve values depend on the platform in the last binary32 digit.
- **REQ-MIXER-VALUES-010** (number text on save): what a save by the target
  build writes for mixer values is not established.
- **REQ-MIXER-VALUES-011** (volume gain applied to audio and the silence
  limit): depends on an unresolved question about the value the audio path
  receives, and needs measurement.
- **REQ-MIXER-VALUES-012** (send gain applied to audio): unknown.
- **REQ-MIXER-VALUES-013** (pan law) and **REQ-MIXER-VALUES-014** (crossfade
  effect and its timing): audio output that needs measurement.
- **REQ-MIXER-VALUES-015** (out-of-range and alternative stored values):
  unknown.

Inputs with **no expectation** in this release:

- number text other than the spelling above, for example with an exponent, a
  `+` sign, spaces, other characters, or empty, and `inf`, `nan`, hexadecimal
  or `#` forms; a missing `Value` attribute; Boolean text other than `true`
  and `false`; code text other than ASCII digits;
- volumes outside 0.0003162277571 to 1.99526238; sends outside 0.0003162277571
  to 1; pans, split pans and the crossfader outside −1 to 1; pan mode codes
  other than 0 and 1; crossfade assignment codes other than 0 to 2; crossfade
  curve codes other than 0 to 6;
- volumes and sends within 0.00005 dB of a text boundary as stated in
  REQ-MIXER-VALUES-006; pans and split pans of −0.75, −0.25, 0.25 and 0.75;
- documents with no return track or more than one; a number of send holders
  other than one per return track; a holder `Id` other than `0`;
  `EnabledByUser` other than `true` on audio, MIDI and group mixers' sends and
  `false` on the return mixer's own send; `SoloSink` other than `false`;
- missing, duplicated or unknown mixer value elements, value elements in
  another order, a track without a mixer, and any element whose name ends in
  `KeyMidi` inside a mixer;
- automation, clip envelopes, modulation or MIDI or key mappings that target a
  mixer value;
- any other envelope, format version, compressed container or document kind.

Excluded behavior:

- what is written on save, including the text of mixer values and of their
  controller ranges;
- the effect of volume, sends, pan, pan mode, split pans, track switch,
  crossfader and crossfade assignment on audio, any silence limit, ramps and
  the shapes of the crossfade curves;
- what opening, showing or saving does with out-of-range values;
- fader positions, the curves between fader position and gain, and the mapping
  of controllers to mixer values;
- which part of the user interface shows which text, and whether any part
  shows the same value in another form, for example the digits without the
  unit or without `-inf`;
- editing after opening, including text entry, keys, mouse, remote control and
  MIDI; creating tracks, and the values of new mixers and new sends; undo;
- the meaning of `EnabledByUser` and `SoloSink`; whether the cue track's volume
  is the preview level; a text for the crossfader value.

Before claiming reference compatibility, a separately designed bounded probe
must run these cases, or a justified equivalent set, against the original. It
must pin the original and candidate builds and the fixture bytes, retain
independent observations, and report mismatches. Candidate-only success proves
agreement with this contract, not with the running original.

## Fixture provenance

All 37 fixtures were authored for this release from one template written for
it. The template has the envelope above, a `LiveSet` holding `Tracks` with an
audio track (`Id="11"`), a MIDI track (`Id="12"`) and a return track
(`Id="13"`), then `MainTrack`, `PreHearTrack` and `CrossfadeCurve` with code 2.
Each track holds only `DeviceChain/Mixer` with the value elements of
REQ-MIXER-VALUES-001 in their order. Template values: volumes `1`, pans `0`,
split pans `-1` and `1`, pan mode `0`, track switch `true`, `SoloSink`
`false`, crossfade assignment `1`, crossfader `0`, and sends `0.0003162277571`
with `EnabledByUser` as stated in REQ-MIXER-VALUES-003. Each fixture is the
template with the change its purpose states. Text is ASCII with line-feed line
endings, two-space indentation and a final newline.

No fixture contains shipped file content, program code or assets. Expected
results are newly authored static-derived behavioral data. No public source or
dependency is approved or included. Review status is recorded in
[the manifest](manifest.json) and [the review disposition](REVIEW.md).
