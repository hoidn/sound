# Warp markers and warp settings, release 1

Target: Ableton Live 12 Suite 12.4.3 (2026-07-07_e3d8be4d07), macOS, Apple
silicon (arm64). Features: FEAT-WARP with FEAT-PERSISTENCE. Parent
specification identity: SPEC-WARP-MARKERS revision 1. Release: warp-markers-v1.
Only the clauses explicitly included below are in scope. No other clause of a
listed requirement is implicitly approved. This document is self-contained.

**Status: reviewed local release**, approved with listed narrowing. The review
record is [REVIEW.md](REVIEW.md).

## What the contract means

An audio clip in a Live Set can be warped: warp markers pair a time in its
sample with a position in beats. Each sample of a Simpler carries a marker list
of the same kind. For one document format version, this contract describes:

- where warp markers and warp settings are stored in a decoded Live Set, and how
  their text is read when a document is opened;
- the default of a warp setting that the document does not give;
- the meaning of the stored warp mode codes, and the stored transient codes and
  their defaults;
- which edits of warp markers through the scripting interface are refused, and
  which are accepted.

It does not describe what is saved, how a warped clip plays or sounds, the
conversion between sample time and beat time, the marker list after an
accepted edit, editing in the user interface, or how a refused document is
reported.

All rules and expected results are **static-derived**: they were derived for
the target build without running it. None is an observed execution of the
original application, and none was run against a candidate. No compatibility
result is established. The original application remains the authority for a
later comparison. A few derived steps rest on assumptions that were not traced
to the end: that marker times are held as binary64 values; that the sample
length used by `add_warp_marker` is the duration of the clip's sample; that an
add or remove whose checks all pass raises no further error; and that the
marker lookup of REQ-WARP-MARKERS-015 clause 7 behaves as stated. The comparison
obligation below covers them.

## Document scope and preconditions

- The input is the decoded XML of a Live Set: well-formed XML 1.0 in UTF-8
  whose root element is `Ableton` with exactly the attributes
  `MajorVersion="5"`, `MinorVersion="12.0_12402"` and `SchemaChangeCount="1"`,
  and whose first child is `LiveSet`. Every fixture uses this envelope. The
  compressed file container, other root elements and attributes, other format
  versions and their upgrade are outside this release.
- Paths are relative to `/Ableton/LiveSet`. The **clip** of a case is the
  `AudioClip` element at
  `Tracks/AudioTrack/DeviceChain/MainSequencer/ClipSlotList/ClipSlot/ClipSlot/Value/AudioClip`.
  The **sample part** of a case is the `SampleWarpProperties` element at
  `Tracks/MidiTrack/DeviceChain/DeviceChain/Devices/OriginalSimpler/Player/MultiSampleMap/SampleParts/MultiSamplePart/SampleWarpProperties`.
  Each fixture holds exactly one of the two.
- The **text** of a value is its attribute value after standard XML
  attribute-value decoding.
- **Opens** means the document is read without refusal. **Refused** means the
  document is not opened. How a refusal is reported, and what is open
  afterwards, are excluded.
- **Held after opening** means the values the clip or sample part holds once
  the document has been read. A change that the application then makes by
  itself, such as automatic warping or sample analysis, is outside this
  release. Whether the original makes such a change when a set is opened is not
  established; the comparison obligation says how a comparison detects one.
  Scripting calls are made on the values held after opening.
- **The clip's sample** is the WAV fixture named by each case's `sample`
  field, `fixtures/sample.wav`: mono, 16-bit PCM, 8,000 Hz, 24,000
  frames, so 3 seconds long, all samples zero. How a document refers to its
  sample is outside this release, and the fixtures carry no sample reference.
  No expectation of an `open` case depends on the sample.
- A full Live Set contains much more than the fixtures (other clip properties,
  devices, the transport and other state). That content is outside this
  release. Its absence from a fixture must not by itself change a judged
  outcome.
- Numbers use `.` as the decimal separator. Expectations assume a host locale
  whose decimal separator is `.`.

## Terms

| Term | Meaning |
| --- | --- |
| Marker | A `WarpMarker` element, taken as the pair (SecTime, BeatTime) of its two values |
| Marker list | The markers inside one `WarpMarkers` element, in document order |
| Shadow marker | The last marker of an audio clip's marker list |
| Visible markers | The markers of an audio clip's list other than the shadow marker |
| Beat grid | The multiples of 1/3,843,840 beat |
| Grid rounding | Rounding a beat to the nearest multiple of 1/3,843,840 beat, with values exactly halfway rounded away from zero |
| Segment tempo | For markers (s₁, b₁) and (s₂, b₂) with s₁ ≠ s₂: (b₂ − b₁) / (s₂ − s₁) × 60, in BPM |
| Scripting interface | The clip functions Live offers to control-surface scripts and Max for Live: `sample_to_beat_time`, `beat_to_sample_time`, `add_warp_marker`, `remove_warp_marker` and `move_warp_marker` |

## Selected requirement clauses

Each clause below is included only as stated.

### REQ-WARP-MARKERS-001: where warp state is stored (partial)

1. An audio clip stores its warp state in these children of `AudioClip`:
   `IsWarped` (Boolean), `WarpMode`, `TransientResolution` and
   `TransientLoopMode` (integer codes), `GranularityTones`,
   `GranularityTexture`, `FluctuationTexture`, `TransientEnvelope`,
   `ComplexProFormants` and `ComplexProEnvelope` (numbers), and `WarpMarkers`.
   Each of these children other than `WarpMarkers` is an empty element with one
   `Value` attribute, for example `<WarpMode Value="4" />`.
2. A Sampler or Simpler sample stores a marker list of the same form, a
   `WarpMode`, the same eight settings and an `IsWarped` in
   `SampleWarpProperties`, a child of each `MultiSamplePart`.
3. The texture fluctuation setting is named `FluctuationTexture`.
4. `IsWarped` text `true` means the clip is warped and `false` that it is not.

### REQ-WARP-MARKERS-002: marker element and number text on load (partial)

1. `WarpMarkers` contains `WarpMarker` elements, each with the attributes `Id`,
   `SecTime` and `BeatTime`, for example
   `<WarpMarker Id="10" SecTime="0" BeatTime="0" />`. `SecTime` and `BeatTime`
   are attributes, not child elements. Each holds an IEEE 754 binary64 value.
2. `SecTime` and `BeatTime` text is read as follows. Leading space characters
   (U+0020) are skipped. The value is then read from the longest prefix of the
   remaining text that forms a decimal number: an optional `+` or `-`; digits
   with an optional `.` and fraction digits, at least one digit in total; and an
   optional exponent of `e` or `E`, an optional sign and at least one digit. An
   exponent marker without digits is not part of the prefix. Text after the
   prefix is ignored, so `2junk` reads as 2. The value is the binary64 number
   nearest to the decimal prefix, ties to even.
3. Text without such a prefix refuses the document, for example `abc` or the
   empty string.
4. A value is held as read, without rounding, clamping or a range check. In
   particular a `BeatTime` is not moved to the beat grid: `2.0000001` is held
   as the binary64 number nearest to 2.0000001.
5. No case judges `Id`.

### REQ-WARP-MARKERS-003: well-formed audio clip marker lists on load (partial)

1. An audio clip marker list of at least two markers that is strictly
   increasing in both `SecTime` and `BeatTime` opens. Each marker holds its
   values as read by REQ-WARP-MARKERS-002, and the list keeps document order.

### REQ-WARP-MARKERS-004: empty marker list of a sample part (partial)

1. An empty `WarpMarkers` element (`<WarpMarkers />`) in
   `SampleWarpProperties` does not refuse the document. The sample part's
   marker list is empty after opening.

### REQ-WARP-MARKERS-007: the shadow marker (partial)

1. The last marker of an audio clip's marker list is the shadow marker.
2. The scripting interface refuses to remove or move the shadow marker
   (REQ-WARP-MARKERS-015 clause 7), and never treats it as the right
   neighbour of a new marker (clause 3).

### REQ-WARP-MARKERS-008: scripting conversion on a clip that is not warped (partial)

1. `sample_to_beat_time` and `beat_to_sample_time`, called on an audio clip
   that is not warped, raise an error. The call is refused with reason
   `not-warped`.

### REQ-WARP-MARKERS-010: absent warp settings (partial)

1. In an audio clip, a `GranularityTones`, `GranularityTexture`,
   `FluctuationTexture`, `TransientResolution`, `TransientLoopMode`,
   `ComplexProFormants` or `ComplexProEnvelope` element that is absent, or that
   is present without a `Value` attribute, gives the value 30, 65, 25, 6, 2,
   100 or 128 respectively. Neither form refuses the document.

### REQ-WARP-MARKERS-011: warp mode codes (partial)

1. `WarpMode` codes 0 to 4 and 6 are the six modes of the warp mode chooser:
   0 Beats, 1 Tones, 2 Texture, 3 Re-Pitch, 4 Complex, 6 Complex Pro. Code 5 is
   not one of them and is outside this release.
2. An audio clip `WarpMode` of 0, 1, 2, 3, 4 or 6 is held as stored after
   opening. What the user interface shows is not judged.

### REQ-WARP-MARKERS-012: transient resolution and transient loop mode codes (partial)

1. `TransientResolution` codes are 0 to 6. Default 6.
2. `TransientLoopMode` codes are 0, 1 and 2. Default 2.
   The labels of both code lists are not part of this release.
3. A code within these lists is held as stored after opening.

### REQ-WARP-MARKERS-013: setting ranges and defaults (partial)

| Element | Minimum | Maximum | Default |
| --- | --- | --- | --- |
| `GranularityTones` | 12 | 100 | 30 |
| `GranularityTexture` | 2 | 263 | 65 |
| `FluctuationTexture` | 0 | 100 | 25 |
| `ComplexProFormants` | 0 | 100 | 100 |
| `ComplexProEnvelope` | 8 | 256 | 128 |

1. An integer value within its range is held as stored after opening.
2. `TransientEnvelope` is not part of this clause: its range, default and
   value are not released.

### REQ-WARP-MARKERS-015: marker edits through the scripting interface (partial)

`add_warp_marker` is given a sample time p and a beat q. p is compared with the
`SecTime` values of the clip's list and with the length of the clip's sample in
seconds; q is compared with the `BeatTime` values.

1. The add is refused with reason `not-warped` when the clip is not warped.
2. The add is refused with reason `sample-time-out-of-range` when p is below 0
   or above the length of the clip's sample in seconds.
3. The new marker's position is before the first visible marker whose
   `SecTime` is greater than p, or before the shadow marker if no visible
   marker's is. Its **left neighbour** is the marker before that position. Its
   **right neighbour** is the marker at that position, unless that marker is
   the shadow marker, in which case it has none.
4. The add is refused with reason `beat-below-left-neighbour` when q, as given,
   is below the left neighbour's beat, and with reason
   `beat-above-right-neighbour` when q, as given, is above the right
   neighbour's beat. These two checks use q before grid rounding.
5. q is then grid-rounded. The add is refused with reason
   `segment-tempo-out-of-range` when the segment tempo between the new marker
   (p, rounded q) and its left neighbour, or between it and its right
   neighbour, lies outside 5 to 999 BPM. No limit applies toward the shadow
   marker.
6. Otherwise the add is accepted: the call raises no error. The marker list
   after an accepted add is not part of this release.
7. `remove_warp_marker` and `move_warp_marker` are given a beat q (and the move
   a second argument). q is grid-rounded and the marker whose beat equals the
   rounded value is looked up. The call is refused with reason `no-such-marker`
   when no marker has that beat, and with reason `shadow-marker` when that
   marker is the shadow marker.
8. Otherwise a remove is accepted, whether or not the clip is warped. The
   marker list after an accepted remove is not part of this release. An
   accepted move has no expectation.

### REQ-WARP-MARKERS-016: beat grid (partial)

1. The add of REQ-WARP-MARKERS-015 clause 5 and the lookup of clause 7
   grid-round the beat they are given.
2. Opening a document does not round (REQ-WARP-MARKERS-002 clause 4).

### Combined failures

Every case breaks at most one rule. A document or call that breaks more than
one rule of this release has no expectation.

## Acceptance representation and comparison

[cases.json](cases.json) lists 38 cases. Each has an input fixture, the clip's
sample, an action and an expected result. The action is `open` (open the
document) or `open-call` (open it, then make the one scripting call in the
case's `call` field on the clip, before any other edit).

| Field | Meaning |
| --- | --- |
| `outcome` | For `open`: `opens` or `refused`. For `open-call`: `accepted` (the call raises no error) or `refused` (it raises an error) |
| `state` | Values held after opening, for listed keys only, under `AudioClip` (the clip) or `SampleWarpProperties` (the sample part). Each key is a child element name of REQ-WARP-MARKERS-001. `IsWarped` is a Boolean, codes and settings are numbers, and `WarpMarkers` is the marker list as `[SecTime, BeatTime]` pairs in list order |
| `refusal_reason` | For a refused call: `not-warped`, `sample-time-out-of-range`, `beat-below-left-neighbour`, `beat-above-right-neighbour`, `segment-tempo-out-of-range`, `no-such-marker` or `shadow-marker`, as defined in the clauses above |

The `call` field names the function and its arguments: `sample_frames` for
`sample_to_beat_time` (a time in sample frames), `beat` for
`beat_to_sample_time`, `remove_warp_marker` and `move_warp_marker`,
`sample_time_seconds` and `beat` for `add_warp_marker`, and `distance` for the
second argument of `move_warp_marker`. Arguments are binary64 numbers. How the
scripting interface receives its arguments is outside this release.

Comparison rules:

- `outcome` compares exactly.
- Numbers in `state` are JSON numbers and compare exactly as binary64 values.
  A `WarpMarkers` value compares as a whole list: the same length and every
  pair equal, in order. Keys a case does not list are not judged.
- `refusal_reason` compares exactly. Error text and error type are not
  compared.
- An `open-call` case relies on the document opening; that is not judged
  separately. Each case starts from its fixture alone in a fresh state.

This is a **project comparison representation**, not an API claimed to exist
in Live and not a required design. A candidate adapter may translate its own
result into these labels. Opening and the scripting calls in scope have no
cancellable step, resource or timing tolerance, so cancellation, teardown and
timing cases are omitted.

## Reference comparison obligation (not executed)

A later comparison against the original application needs a full Live Set per
case. For a clip case, the validation analyst builds it from a set of the same
format version, whose root carries the fixture's `MajorVersion`,
`MinorVersion` and `SchemaChangeCount` values, with one audio track whose first
clip slot holds a clip of the WAV fixture created and saved by the
application. In that clip, each child of REQ-WARP-MARKERS-001 clause 1 is
replaced by the fixture's, and removed where the fixture has none. Every other
child, among them the sample reference and `MarkersGenerated`, keeps the value
the application saved. For the sample-part case, a MIDI
track holds one Simpler whose sample is the WAV fixture, and the children of its
sample part's `SampleWarpProperties` named in REQ-WARP-MARKERS-001 clause 2 are
replaced in the same way. The set is opened in a fresh application state with
factory preferences. An `open-call` case makes its one call on that clip after
opening, through the control-surface or Max for Live scripting interface,
before any other edit. Each observation or call is made right after opening,
before playback or any other action.

WARP-MARKERS-001 and 002 also show whether the original changes a clip by
itself after reading it. If their held values differ from the fixture's, the
difference is reported for analysis, and the other `state` and `open-call`
comparisons of this release are inconclusive until it is resolved.

The observation channel for held values is chosen by the validation analyst.
A channel that rounds or converts must be compared at its rounding. A graded
`refusal_reason` observation must show which condition the original reports,
without comparing wording; if its error does not distinguish them, that
comparison is inconclusive. None of this has been run.

Before claiming reference compatibility, a separately designed bounded probe
must run these cases, or a justified equivalent set, against the original. It
must pin the original and candidate builds and the fixture bytes, retain
independent observations, and report mismatches. Candidate-only success proves
agreement with this contract, not with the running original.

## Exclusions and deferred obligations

Requirements not released: **REQ-WARP-MARKERS-005** (one-marker, out-of-order
and equal-time audio clip marker lists), **REQ-WARP-MARKERS-006** (missing or
`Invalid` marker times), **REQ-WARP-MARKERS-009** (which sample position plays
at a given beat) and **REQ-WARP-MARKERS-014** (codes and settings outside their
codes or ranges on load).

Inputs with **no expectation** in this release:

- `SecTime` or `BeatTime` text whose remainder, after leading spaces and an
  optional sign, starts with `0x` or `0X`, or with `inf` or `nan` in any letter
  case; the text `Invalid`; text starting with `#`; leading whitespace other
  than U+0020; a `WarpMarker` without `SecTime` or `BeatTime`; values outside
  −1,000,000 to 1,000,000 (a scope limit of this release, not a claim about the
  original);
- marker `Id` values that are missing, repeated or not decimal integers;
  content inside `WarpMarker`; children of `WarpMarkers` other than
  `WarpMarker`;
- an audio clip marker list with fewer than two markers, including an empty
  one, or not strictly increasing in both `SecTime` and `BeatTime`;
- code and setting text other than plain decimal digits; codes outside the
  lists of REQ-WARP-MARKERS-011 clause 2 and 012; settings outside their
  ranges or not integers; `IsWarped` text other than `true` or `false`; a
  missing `IsWarped` or `WarpMode`; a `TransientEnvelope` value other than 100.
  Every fixture carries 100, the value of every shipped audio clip; the held
  `TransientEnvelope` value is not judged;
- children of `AudioClip` or `SampleWarpProperties` other than those of
  REQ-WARP-MARKERS-001, a child order other than the fixtures', and repeated
  children;
- scripting arguments that are not finite or whose magnitude is 1,000,000 or
  more; an add whose p, within the sample, is below the first marker's
  `SecTime` or less than 0.0005 s from a neighbour's `SecTime`; a segment tempo
  within 0.001 BPM of 5 or 999; a beat within 0.001 grid step of a value
  exactly halfway between two grid points; a remove or move on a list of fewer
  than three markers;
- any other envelope, format version, compressed container or document kind.

Excluded behavior:

- everything written on save, including the marker, code and setting text;
- an audio clip whose marker list is empty, and what the user sees for any
  refused document;
- the value used, shown and saved for a code or setting outside its list or
  range; the range and default of `TransientEnvelope`;
- the values returned by `sample_to_beat_time` and `beat_to_sample_time` for a
  warped clip; which sample position plays at a given beat; the audio output of
  every warp mode and setting;
- the warp mode a new or loaded clip or sample part gets when `WarpMode` is
  absent, and any default warp mode preference; defaults of sample-part
  settings;
- where and when the application creates or re-places the shadow marker; the
  marker list after an accepted add or remove; the limits of
  `move_warp_marker` and the result of an accepted move; setting the warp mode
  through the scripting interface; scripting calls on clips that are not audio
  clips;
- what the user interface shows for markers, codes, labels and settings;
  interactive marker edits, automatic warping, recording and undo;
- any change the application makes by itself after reading the document, such
  as automatic warping or sample analysis;
- progress, cancellation and timing.

## Fixture provenance

All 18 XML fixtures were authored for this release from one template written
for it: the envelope above and the clip path with the ten value children of
REQ-WARP-MARKERS-001 clause 1 holding invented values, and a marker list of
three visible markers and a shadow marker. Each clip fixture is the
template, or the template with the one change that its case purpose states.
The sample-part fixture is a Simpler path whose `SampleWarpProperties` holds an
empty marker list, `WarpMode` 0, `IsWarped` false, `TransientEnvelope` 100 and
the setting values of REQ-WARP-MARKERS-010. Text is ASCII with line-feed line
endings, two-space indentation and a final newline. The WAV fixture is
generated silence.

No fixture contains shipped file content, shipped audio, program code or
assets. Expected outcomes are newly authored static-derived behavioral data.
No public source or dependency is approved or included. Review status is
recorded in [the manifest](manifest.json) and [the review record](REVIEW.md).
