# Warp markers and warp settings, release 2

Target: Ableton Live 12 Suite 12.4.3 (2026-07-07_e3d8be4d07), macOS, Apple
silicon (arm64). Features: FEAT-WARP with FEAT-PERSISTENCE. Parent
specification identity: SPEC-WARP-MARKERS revision 4. Release: warp-markers-v2,
which supersedes warp-markers-v1 ([README](README.md#supersession)). Only the
clauses explicitly included below are in scope. No other clause of a listed
requirement is implicitly approved. This document is self-contained.

**Status: reviewed local release**, approved with listed narrowing. A separate
review approved the clauses below, narrowed as recorded in
[the review disposition](REVIEW.md).

## What the contract means

An audio clip in a Live Set can be warped: warp markers pair a time in its
sample with a position in beats. For one document format version, this
contract describes:

- where warp markers and warp settings are stored in a decoded Live Set, and how
  their text is read when a document is opened;
- the default of a warp setting that the document does not give;
- the meaning of the stored warp mode codes, and the stored transient codes and
  their defaults;
- the values that the scripting interface's two conversions between sample
  time and beat time return for a warped clip right after opening;
- which edits of warp markers through the scripting interface are refused, and
  which are accepted.

It does not describe what is saved, how a clip plays or sounds, the marker list
after an accepted edit, editing in the user interface, how a refused document
is reported, devices and the sample parts of a Sampler or Simpler, or the
structure rules that decide whether a Live Set opens.

### Provenance

Every expected result carries one of three labels:

- **Static-derived**: derived for the target build without running it, from
  evidence reviewed before sanitization.
- **Extracted execution**: the deciding binary64 values of the case were
  computed by the original program's own x86_64 code for this case's inputs.
  The deciding values are the conversion result, or the rounded beat and the
  beat bounds that decide the outcome. For a conversion, that code computed
  the step between seconds and beats. The division of a position in frames by
  the sample rate, and the multiplication of a result by it, are
  static-derived; for every case with this label they are exact. The grid
  rounding ran in another part of the original program that rounds a beat
  with the same operations as the add and the marker lookup (static-derived).
  The code ran on a Linux x86_64 host, outside the application, with the
  host's C library in place of the macOS system libraries. The macOS arm64
  build is inferred to compute the same values. Opening, the comparisons of
  the deciding values, the call's other checks and the sample rate are
  static-derived.
- **Computed by extracted-execution rules**: computed for this case's inputs
  with the binary64 operation sequences of REQ-WARP-MARKERS-008, 015 and 016.
  Extracted execution confirmed those sequences on other inputs; this input was
  not run. Everything else is static-derived.

None is an observed run of the original application, and none was run against
a candidate. No compatibility result is established. The original application
remains the authority for a later comparison.

### Stated assumptions

Some derived steps rest on assumptions that were not traced to the end. The
[manifest](manifest.json) lists the cases that depend on each, and the
comparison obligation below covers them:

1. the base set opens in the target build; its structure follows static-derived
   rules, and its device lists are empty;
2. marker times are held as binary64 values read by REQ-WARP-MARKERS-002
   clause 2;
3. the sample length that `add_warp_marker` compares with is the duration of
   the clip's sample;
4. the sample rate that both conversions use is the rate of the clip's sample;
5. an add or remove whose checks all pass raises no further error;
6. the marker lookup of REQ-WARP-MARKERS-015 clause 7 behaves as stated;
7. the macOS arm64 build computes the conversions, the grid rounding and the
   beat bounds with the same binary64 operations as the x86_64 build;
8. a conversion made right after opening uses the marker list held after
   opening.

## Document scope and preconditions

- The input is the decoded XML of a Live Set: well-formed XML 1.0 in UTF-8
  whose root element is `Ableton` with exactly the attributes
  `MajorVersion="5"`, `MinorVersion="12.0_12402"` and `SchemaChangeCount="1"`,
  and whose first child is `LiveSet`. Every fixture uses this envelope. The
  compressed file container, other root elements and attributes, other format
  versions and their upgrade are outside this release.
- **Base set.** Every fixture is one complete Live Set, the base set, with the
  one change that its case purpose states. The base set holds a MIDI track, an
  audio track and a return track, the main and cue tracks, two scenes, the
  transport and the set-level values. The MIDI track holds a MIDI clip of two
  notes. Every device list is empty. The audio track's first clip slot holds
  the clip; its second slot is empty. Each audio and MIDI track has two clip
  slots and two empty freeze slots, and each track mixer has one send. The
  base set's structure is static-derived to open in the target build (stated assumption
  1). The rules that decide whether a Live Set opens are outside this release.
  This release relies only on the base set opening, and no case judges the
  base set's other content.
- Paths are relative to `/Ableton/LiveSet`. The **clip** of a case is the only
  `AudioClip` element, at
  `Tracks/AudioTrack/DeviceChain/MainSequencer/ClipSlotList/ClipSlot/ClipSlot/Value/AudioClip`.
  Besides the children of REQ-WARP-MARKERS-001 clause 1, it holds its region,
  name, colour, launch and time-signature children, and a sample reference
  `SampleRef` between `IsWarped` and `WarpMode`.
- The **base list** is the clip's marker list in the base set: three visible
  markers (0 s, beat 0), (1 s, beat 2), (2 s, beat 3) and a shadow marker
  (2.015625 s, beat 3.03125), 1/32 beat after the last visible marker. Its
  segment tempi are 120, 60 and 120 BPM.
- The **text** of a value is its attribute value after standard XML
  attribute-value decoding.
- **Opens** means the document is read without refusal. **Refused** means the
  document is not opened. How a refusal is reported, and what is open
  afterwards, are excluded.
- **Held after opening** means the values the clip holds once the document
  has been read. A change that the application then makes by
  itself, such as automatic warping or sample analysis, is outside this
  release. Whether the original makes such a change when a set is opened is not
  established; the comparison obligation says how a comparison detects one.
  Scripting calls are made on the values held after opening.
- **The clip's sample** is the WAV fixture named by each case's `sample`
  field, `fixtures/sample.wav`: mono, 16-bit PCM, 8,000 Hz, 24,000 frames, so
  3 seconds long, all samples zero. The clip's sample reference names it by the
  path `sample.wav`, relative to the document's folder, and stores its length
  in frames (`DefaultDuration` 24000) and its rate (`DefaultSampleRate` 8000),
  which equal the file's. Keep the WAV in the folder of the documents. How a
  document refers to and finds its sample is outside this release. No
  expectation of an `open` case depends on the sample.
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
| Grid rounding | The rounding of REQ-WARP-MARKERS-016 clause 1 |
| Binary64 arithmetic | IEEE 754 binary64; each operation is rounded to the nearest value, ties to even, unless it is stated as fused |
| Fused multiply-add | F(a, b, c) = a × b + c computed with a single rounding, the fused multiply-add operation of IEEE 754 |
| Segment tempo | For markers (s₁, b₁) and (s₂, b₂) with s₁ ≠ s₂: (b₂ − b₁) / (s₂ − s₁) × 60, in BPM; used to describe cases |
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
2. Not released: how a Sampler or Simpler sample stores its warp state.
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

### REQ-WARP-MARKERS-007: the shadow marker (partial)

1. The last marker of an audio clip's marker list is the shadow marker.
2. The scripting interface refuses to remove or move the shadow marker
   (REQ-WARP-MARKERS-015 clause 7), and never treats it as the right
   neighbour of a new marker (clause 3).
3. In the conversions of REQ-WARP-MARKERS-008, the segment from the last
   visible marker to the shadow marker applies to every position at or after
   the last visible marker.
4. Opening keeps the shadow marker as the document gives it, whatever its
   spacing from the marker before it: for example 1/16 beat, where the base
   list has 1/32 beat.

### REQ-WARP-MARKERS-008: scripting conversion between sample time and beat time (partial)

1. `sample_to_beat_time` and `beat_to_sample_time`, called on an audio clip
   that is not warped, raise an error. The call is refused with reason
   `not-warped`.
2. On a warped clip, let the marker list be (s₀, b₀) … (sₙ₋₁, bₙ₋₁) in list
   order, with sᵢ the `SecTime` and bᵢ the `BeatTime` of marker i and n ≥ 2. Let
   R be the sample rate of the clip's sample in Hz. All arithmetic is binary64.
   `sample_to_beat_time(t)` takes a position t in sample frames and computes
   x = t / R. It selects segment k: the largest index from 0 to n − 2 with
   sₖ ≤ x, or 0 when x < s₀. With u = (x − sₖ) / (sₖ₊₁ − sₖ), it returns
   F(u, bₖ₊₁, F(−u, bₖ, bₖ)), which is bₖ + u × (bₖ₊₁ − bₖ) evaluated with two
   fused multiply-adds.
3. `beat_to_sample_time(b)` selects k in the same way over b₀ … bₙ₋₂. With
   u = (b − bₖ) / (bₖ₊₁ − bₖ), it computes x = F(u, sₖ₊₁, F(−u, sₖ, sₖ)) and
   returns x × R, a position in sample frames.
4. The result is linear inside each segment. Before the first marker the first
   segment is extended, and at or after the last visible marker the segment to
   the shadow marker is extended (REQ-WARP-MARKERS-007 clause 3). Results are
   not limited to the sample or to the range of the markers. For the base list
   and R = 8,000, `sample_to_beat_time(20000)` returns 4 and
   `beat_to_sample_time(2.5)` returns 12000.
5. These values apply to a call made right after opening, on the marker list
   held after opening. A result after an edit of the clip is not part of this
   release.

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
seconds; q is compared with the `BeatTime` values. The checks run in the order
of clauses 1 to 5, and the first that fails refuses the call.

1. The add is refused with reason `not-warped` when the clip is not warped.
2. The add is refused with reason `sample-time-out-of-range` when p is below 0
   or above the length of the clip's sample in seconds.
3. The new marker's position is before the first visible marker whose
   `SecTime` is greater than p, or before the shadow marker if no visible
   marker's is. Its **left neighbour** is the marker before that position; when
   p is below the first marker's `SecTime` it has none. Its **right
   neighbour** is the marker at that position, unless that marker is the shadow
   marker, in which case it has none.
4. The add is refused with reason `beat-below-left-neighbour` when q, as given,
   is below the left neighbour's beat, and with reason
   `beat-above-right-neighbour` when q, as given, is above the right
   neighbour's beat. These two checks use q before grid rounding. A missing
   neighbour has no check.
5. q is then grid-rounded, giving q′. For each neighbour (sₙ, bₙ), let
   d = p − sₙ and compute, each operation rounded separately,
   a = bₙ + d × f₅ and c = bₙ + d × f₉₉₉, where f₅ and f₉₉₉ are the binary64
   values nearest to 5/60 and 999/60. The add is refused with reason
   `segment-tempo-out-of-range` unless min(a, c) ≤ q′ ≤ max(a, c). No bound
   applies toward a missing neighbour: none toward the shadow marker, and none
   to the left when p is below the first marker's `SecTime`.
   For d ≠ 0 this is, up to binary64 rounding next to the limits, the condition
   that the segment tempo between (p, q′) and the neighbour lies within 5 to
   999 BPM inclusive. When p equals the left neighbour's `SecTime`, both bounds
   toward it equal its beat, so only a q′ equal to that beat passes. For
   example, toward the neighbour (1 s, beat 2) the bounds are
   2.0416666666666665 and 10.325 at p = 1.5 s, and 2 and 2 at p = 1 s.
6. Otherwise the add is accepted: the call raises no error. The marker list
   after an accepted add is not part of this release.
7. `remove_warp_marker` and `move_warp_marker` are given a beat q (and the move
   a second argument). q is grid-rounded and the first marker whose beat equals
   the rounded value is looked up. The call is refused with reason
   `no-such-marker` when no marker has that beat, and with reason
   `shadow-marker` when that marker is the shadow marker.
8. Neither `remove_warp_marker` nor `move_warp_marker` checks whether the clip
   is warped. Otherwise a remove is accepted, also on a list of two markers.
   The marker list after an accepted remove is not part of this release. An
   accepted move has no expectation.

### REQ-WARP-MARKERS-016: beat grid (partial)

1. Grid rounding of a binary64 beat b is computed in binary64, each operation
   rounded separately: s is 1 when b ≥ 0 and −1 otherwise; h is the binary64
   value nearest to 1/3,843,840, which is 2.6015651015651016e−07;
   y = |b + s × (h × 0.5)| × 3,843,840; the result is s × ⌊y⌋ / 3,843,840.
   This is the nearest point of the beat grid, with values halfway between two
   grid points rounded away from zero, except within about 3 × 10⁻⁹ of a grid
   step from a halfway point. For example, 2.0000001 gives 2 and 2.001 gives
   2.0010000416250415. The binary64 value nearest to the halfway point between
   2 and the next grid point, 2.0000001300782553, and the value one binary64
   step below it, 2.000000130078255, both give 2.00000026015651, although the
   second lies below the halfway point. Two steps below,
   2.0000001300782544 gives 2.
2. The add of REQ-WARP-MARKERS-015 clause 5 and the lookup of clause 7
   grid-round the beat they are given.
3. Opening a document does not round (REQ-WARP-MARKERS-002 clause 4).

### Combined failures

Every case breaks at most one rule, with one exception: an `add_warp_marker`
call is refused for the first check of REQ-WARP-MARKERS-015 clauses 1 to 5 that
fails, whatever the later checks would give (the calls of WARP-MARKERS-023 to
027 also lie outside the beat bounds). Any other document or call that breaks
more than one rule of this release has no expectation.

## Acceptance representation and comparison

[cases.json](cases.json) lists 63 cases. The identifier WARP-MARKERS-018 is
not used: that case of warp-markers-v1 is withdrawn
([README](README.md#supersession)). Each has an input fixture, the clip's
sample, an action and an expected result. The action is `open` (open the
document) or `open-call` (open it, then make the one scripting call in the
case's `call` field on the clip, before any other edit).

| Field | Meaning |
| --- | --- |
| `outcome` | For `open`: `opens` or `refused`. For `open-call`: `accepted` (the call raises no error) or `refused` (it raises an error) |
| `state` | Values held after opening, for listed keys only, under `AudioClip` (the clip). Each key is a child element name of REQ-WARP-MARKERS-001. `IsWarped` is a Boolean, codes and settings are numbers, and `WarpMarkers` is the marker list as `[SecTime, BeatTime]` pairs in list order |
| `value` | For an accepted conversion call: the number it returns, a beat for `sample_to_beat_time` and a position in sample frames for `beat_to_sample_time` |
| `refusal_reason` | For a refused call: `not-warped`, `sample-time-out-of-range`, `beat-below-left-neighbour`, `beat-above-right-neighbour`, `segment-tempo-out-of-range`, `no-such-marker` or `shadow-marker`, as defined in the clauses above |
| `expectation_provenance` | One of the three labels of [Provenance](#provenance) |

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
- `value` compares within 1e-9 beat for `sample_to_beat_time` and within 1e-6
  sample frame for `beat_to_sample_time`. Each expected value is the exact
  binary64 result of REQ-WARP-MARKERS-008.
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

Each fixture is a complete Live Set, so a later comparison against the original
application uses the fixtures as they are. For each case the validation analyst
saves the fixture's bytes under a file name ending in `.als`, in a folder that
also holds `sample.wav`. The WAV's modification time is set to the clip's
stored `LastModDate`, 1,760,000,000 seconds after 1970-01-01 UTC. The set is
opened in a fresh application state with factory preferences. An `open-call`
case makes its one call on the clip after opening, through the control-surface
or Max for Live scripting interface, before any other edit. Each observation or
call is made right after opening, before playback or any other action.

If the original does not open `fixtures/base.xml`, stated assumption 1 has
failed. Every case of this release is then inconclusive, and the difference is
reported for analysis.

WARP-MARKERS-001 and 002 also show whether the original changes a clip by
itself after reading it. If their held values differ from the fixture's, the
difference is reported for analysis, and the other `state`, `value` and
`open-call` comparisons of this release are inconclusive until it is resolved.
The analyst may then repeat the comparison with the clip's children outside
REQ-WARP-MARKERS-001 clause 1 set as the application saves them for a clip of
the WAV fixture.

The observation channel for held values and returned values is chosen by the
validation analyst. A channel that rounds or converts must be compared at its
rounding. A graded `refusal_reason` observation must show which condition the
original reports, without comparing wording; if its error does not distinguish
them, that comparison is inconclusive. None of this has been run.

Before claiming reference compatibility, a separately designed bounded probe
must run these cases, or a justified equivalent set, against the original. It
must pin the original and candidate builds and the fixture bytes, retain
independent observations, and report mismatches. Candidate-only success proves
agreement with this contract, not with the running original.

## Exclusions and deferred obligations

Requirements not released: **REQ-WARP-MARKERS-004** (empty marker lists),
**REQ-WARP-MARKERS-005** (one-marker, out-of-order and equal-time audio clip
marker lists), **REQ-WARP-MARKERS-006** (missing or `Invalid` marker times),
**REQ-WARP-MARKERS-009** (playback) and **REQ-WARP-MARKERS-014** (codes and
settings outside their codes or ranges on load). Clause 2 of
REQ-WARP-MARKERS-001 is not released.

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
  Every fixture carries 100; the held `TransientEnvelope` value is not judged;
- children of `AudioClip` other than those the fixtures carry, a child order
  other than the fixtures', and repeated children;
- any change to the fixtures' context: the document outside the clip's
  children of REQ-WARP-MARKERS-001 clause 1, including the clip's sample
  reference, and the WAV file; any device in a device list, including a
  Sampler or Simpler and its sample parts (every device list of the fixtures
  is empty);
- scripting arguments that are not finite or whose magnitude is 1,000,000 or
  more; a move on a list of fewer than three markers;
- any other envelope, format version, compressed container or document kind.

Excluded behavior:

- everything written on save, including the marker, code and setting text;
- an empty marker list, in an audio clip or in a sample part, and what the
  user sees for any refused document;
- the value used, shown and saved for a code or setting outside its list or
  range; the range and default of `TransientEnvelope`;
- conversion results after any edit of the clip, and conversions on clips that
  are not audio clips;
- playback: which sample position plays at a given beat, whether a clip that
  is not warped uses its warp markers, and arrangement clips; the audio output
  of every warp mode and setting;
- the warp mode a new or loaded clip gets when `WarpMode` is absent, and any
  default warp mode preference;
- Sampler and Simpler sample parts: how they store warp state, their marker
  lists, codes, settings and defaults; any device in a device list;
- where and when the application creates or re-places the shadow marker, and
  the values it gives it; the marker list after an accepted add or remove; the
  limits of `move_warp_marker` and the result of an accepted move; setting the
  warp mode through the scripting interface; scripting calls on clips that are
  not audio clips;
- what the user interface shows for markers, codes, labels and settings;
  interactive marker edits, automatic warping, recording and undo;
- any change the application makes by itself after reading the document, such
  as automatic warping or sample analysis;
- the structure rules that decide whether a Live Set opens, and how a document
  refers to and finds its sample;
- progress, cancellation and timing.

## Fixture provenance

All 20 XML fixtures were authored for this project from one base set: the
envelope above; the tracks, scenes and set-level values described in
[Document scope and preconditions](#document-scope-and-preconditions), with
invented names, colours, identifiers and values; and the clip, whose ten value
children of REQ-WARP-MARKERS-001 clause 1 hold invented values and whose marker
list is the base list. Each fixture is the base set, or the base set with the
one change that its case purpose states. Every device list is empty.
Text is ASCII with line-feed line endings, tab indentation and a final newline.
The WAV fixture is generated silence.

No fixture contains shipped file content, shipped audio, program code or
assets. Expected outcomes are newly authored behavioral data, labelled by
provenance. No public source or dependency is approved or included. Review
status is recorded in [the manifest](manifest.json) and
[the review disposition](REVIEW.md).
