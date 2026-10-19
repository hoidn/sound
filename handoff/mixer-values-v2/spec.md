# Track mixer values in Live Set documents, release 2

Target: Ableton Live 12 Suite 12.4.3 (2026-07-07_e3d8be4d07), macOS, Apple
silicon (arm64). Features: FEAT-AUDIO with FEAT-PERSISTENCE. Parent
specification identity: SPEC-MIXER-VALUES revision 4. Release:
mixer-values-v2, which supersedes mixer-values-v1
([README](README.md#supersession)). Only the clauses explicitly included below
are in scope. No other clause of a listed requirement is implicitly approved.
This document is self-contained.

**Status: reviewed local release.** A separate review approved the clauses
below with the narrowing recorded in [the review disposition](REVIEW.md).
Implementation requires a fresh, restricted implementation workspace.

## What the contract means

Every track of a Live Set has a mixer: volume, pan, pan mode, a left and a
right split-stereo pan, one send per return track, a track switch and a
crossfade assignment. The main track also has the crossfader, and the set has
a crossfade curve. For one document format version, this contract describes:

- where each of these values is stored, for each track type;
- which value it takes when the document is opened;
- the value text of volumes and sends (decibels), of pans, and of the track
  switch;
- the names of the pan mode, crossfade assignment and crossfade curve codes;
- as **computed values** at listed inputs: the volume and send fader curves,
  from fader position to gain and back; the pan-law gains; and the levels of
  the seven crossfade curves.

It does not describe what the values do to audio: which gains the audio path
derives from the stored values, where and when it applies them, or what is
heard. It also does not describe what is written on save, the fader positions
shown, editing, or which part of the user interface shows which text.

Every expected result carries one of two provenance labels:

- **Static-derived**: derived for the target build from evidence reviewed
  before sanitization, without running it.
- **Extracted execution**: the original program's own code that computes the
  value was run on the case's inputs. It ran on a Linux x86_64 host, from the
  program's x86_64 build, with glibc in place of the macOS system libraries;
  the base-10 exponential and the cosine came from glibc. The macOS arm64
  build is inferred to give the same result within each case's comparison.
  For the fader curves, the code that builds both curves and the two
  conversions ran. For the pan law, the code that computes the four gains from
  its five inputs ran. For the crossfade curves, the code that gives each
  curve's level at a position ran. Nothing that supplies these inputs from a
  document, a control or the audio path ran, and nothing that applies the
  results to audio.

None is an observed execution of the original application, and none was run
against a candidate. No compatibility result is established.

### Stated assumptions

The static-derived steps rest on these assumptions, which were not traced to
the end:

- a mixer value written as a plain decimal number is read as the nearest
  binary32 number, as other binary32 values of a document are;
- the name of a code is its entry in the lists below;
- some part of the user interface shows the value texts below, computed from
  the value as read;
- the application's base-10 logarithm may differ from the correctly rounded
  result in the last binary32 digit, so inputs near a text boundary have no
  expectation.

The extracted-execution cases rest on these:

- the macOS arm64 build computes these values as the x86_64 build does,
  within each case's comparison. The arm64 build fuses some multiplications
  and additions. That can change the last binary32 digit of the Dipped and
  Intermediate crossfade levels, of the pan-law gains (only through binary64
  intermediate results) and of the three points next to the bottom of each
  fader curve. The comparisons below cover these; MIXER-VALUES-051 uses one of
  those points, and a one-step change of it moves the expected position by
  less than 0.00000001;
- the macOS base-10 exponential and cosine are within one binary32 step of
  glibc's at these inputs. The comparisons allow one step;
- the round-trip cases MIXER-VALUES-058 to 064 compare exactly. They assume
  that the macOS base-10 exponential gives each curve point they use as the
  binary32 value nearest to the exact result, as the glibc run did. Each exact
  result lies at least 0.16 of a binary32 step from a rounding midpoint, so an
  exponential that errs by less than 0.66 of a step gives the same points.

The comparison obligation below covers these points.

## Document scope and preconditions

- The input of an `open` case is the decoded XML of a Live Set: well-formed
  XML 1.0 in UTF-8 whose root element is `Ableton` with exactly the attributes
  `MajorVersion="5"`, `MinorVersion="12.0_12402"` and `SchemaChangeCount="1"`,
  and whose first child is `LiveSet`. Every fixture uses this envelope. The
  compressed file container, other root elements and attributes, other format
  versions and their upgrade are outside this release.
- Every fixture is a complete Live Set built from one template set
  ([Fixture provenance](#fixture-provenance)). The template set holds the
  parts that a set needs in order to open, as derived statically for the
  target build: tracks with names, colours, routing, empty clip slots, empty
  freeze slots and empty device lists, one send setting per return track,
  scenes, the transport and the crossfade curve. It holds no clips, no devices
  and no envelope on a mixer value.
  Expectations exist only for documents with that structure. Whether a set
  with another structure opens, and the rules that decide it, are outside
  this release.
- The **text** of a value is its attribute value after standard XML
  attribute-value decoding. Paths are relative to `/Ableton/LiveSet`.
- **Opens** means the document is read without refusal. No case in this
  release expects a refusal.
- Numbers use `.` as the decimal separator. Expectations assume a host locale
  whose decimal separator is `.`; locale-dependent behavior is excluded.
- **binary32** is IEEE 754 single precision and **binary64** double
  precision. A binary32 value is compared after its exact conversion to
  binary64. The two **neighbours** of a binary32 value are the next binary32
  values above and below it.
- A `compute` case has no document. Its inputs are binary32 values, given as
  JSON numbers equal to those values.

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

Every fixture has exactly one MIDI track, one audio track and one return
track, in that order inside `Tracks`, plus the main and the cue track. The
cases name the mixers as follows:

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
- In the fixtures every mixer also holds `On` before `Sends`. After `Manual`,
  each value element with a `Manual` child also holds an `AutomationTarget`;
  all but `Speaker` hold a `MidiControllerRange`, and all but `Speaker` and
  `CrossFadeState` a `ModulationTarget`. The main mixer holds `Tempo` and
  `TimeSignature` before `CrossFade`. All of these keep the template set's
  values. None is a mixer value of this release, and none is judged.
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
- The fixtures hold one `SendPreBool` item, `Id="0"` with value `false`, in
  `LiveSet/SendsPre` for the one return track. Its meaning is not released.

### REQ-MIXER-VALUES-004 — partial: pan, split pans and pan mode

- `Pan/Manual`, `SplitStereoPanL/Manual` and `SplitStereoPanR/Manual` are held
  as binary32, from −1 (left) to 1 (right) inclusive.
- `PanMode/@Value` code 0 is named `Stereo` and code 1 `Split Stereo`.

### REQ-MIXER-VALUES-005 — partial: volume and send fader curves (computed values)

A fader position is a binary32 value from 0 to 1. Each curve is a list of
101 points; point k (k = 0 to 100) belongs to position k/100.

- **Static-derived: the points.** The decibel values D[0] to D[100] of a curve
  with top value T (volume +6, send 0) and bottom value B = −70 are computed
  from the top down, every operation rounded to binary32, with 0.4, 0.04 and
  0.05 meaning their binary32 values. Let e_0 = T and e_i = e_(i−1) − 0.4 for
  i = 1 to 60. With s_60 = 0.4, let s_i = s_(i−1) + 0.04 and
  e_i = e_(i−1) − s_i for i = 61 to 96. Let a = s_96 + 0.04,
  e_97 = e_96 − a, b = (3a + (B − e_97)) / 6, e_98 = e_97 − (a − b),
  e_99 = e_98 + (b − (a − b)) and e_100 = B. Each e_i for i below 100 whose
  magnitude is below 0.0001 becomes 0 before the next value is computed from
  it. Then D[k] = e_(100−k), and the gain of point k is
  G[k] = the binary32 value nearest to 10^(binary32(D[k] × 0.05)).
  Consequences: on the volume curve 0 dB is position 0.85 and about −6 dB is
  position 0.7; on the send curve 0 dB is position 1 and about −6 dB is
  position 0.85.
The two conversion rules below are static-derived. The original program's
code for both was run by extracted execution at the inputs of the cases, and
every result agrees with the rules.

- **Position to gain.** For a position p: if p ≤ 0 the
  gain is G[0]; if p ≥ 1 it is G[100]. Otherwise let x = 100p, k = ⌊x⌋ and
  f = x − k, computed in binary64; f ≤ 2^−17 counts as 0 and f ≥ 1 − 2^−17 as
  1. The gain is the binary32 value nearest to (1 − f)·G[k] + f·G[k+1],
  evaluated in binary64.
- **Gain to position.** For a binary32 gain g: if
  g < G[0] the position is 0; if g ≥ G[100] it is 1. Otherwise, with k such
  that G[k] ≤ g < G[k+1], the position is (k + (g − G[k])/(G[k+1] − G[k]))/100
  as a binary32 value, within the comparison of the cases.
- **Round trip (extracted execution).** For the seven gains of
  MIXER-VALUES-058 to 064, each a point of its curve, converting the gain to a
  position and that position back to a gain gives the same binary32 gain
  exactly. This does not hold for every gain. On the volume curve, from the
  point at position 0.7 (about −6 dB) to the point at 0.85 (0 dB), there are
  about 8.4 million binary32 gains but only about 2.5 million binary32
  positions, so most gains in that range cannot return unchanged. Other gains
  have no round-trip expectation: neither an exact return nor a bound on the
  difference is released.
- Expectations exist only for the inputs of MIXER-VALUES-038 to 064. Which
  fader, control or audio path uses these conversions is not released, and
  positions are not stored in documents.

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
  false. This rule is static-derived, and the original program's code that
  gives the text was also run by extracted execution: true gives `On` and
  false gives `Off`. MIXER-VALUES-001 and 030 judge it and keep their
  static-derived label, because how the document's Boolean reaches that code
  was not run.
- The fixtures store `SoloSink` as `false`. Its meaning is not released.

### REQ-MIXER-VALUES-009 — partial: crossfade assignment, crossfader and crossfade curve

- `CrossFadeState/Manual` code 0 is named `A`, 1 `None` and 2 `B`.
- The crossfader is `MainTrack/DeviceChain/Mixer/CrossFade/Manual`, held as
  binary32 from −1 to 1 inclusive. Which end of the crossfader favors A or B is
  not released.
- `LiveSet/CrossfadeCurve/@Value` names the crossfade curve: 0 `Dipped`,
  1 `Intermediate`, 2 `Constant Power`, 3 `Slow Fade`, 4 `Slow Cut`,
  5 `Fast Cut`, 6 `Transition`. Their levels are released only as stated in
  REQ-MIXER-VALUES-014.

### REQ-MIXER-VALUES-013 — partial: pan-law gains (computed values)

- The pan law maps five binary32 inputs, a pan-mode
  amount w, the pan p, the left and right split pans sL and sR, and a gain v,
  to four binary32 gains named L→L, L→R, R→L and R→R. With
  θ(x) = (x + 1)·π/4:
  - L→L = v·(w·cos θ(sL) + (1 − w)·max(10^−5, √2·cos θ(p)));
  - L→R = v·w·sin θ(sL);
  - R→L = v·w·cos θ(sR);
  - R→R = v·(w·sin θ(sR) + (1 − w)·max(10^−5, √2·sin θ(p))).

  The names are labels for the four computed values. Which signal each gain
  scales, and whether, where and when the audio path applies the gains, are
  not released. The formula is static-derived. The original program's code
  for it was run by extracted execution at the inputs of the cases, and every
  result agrees with it within the comparison.
- Consequences: with w = 0, L→R and R→L are 0; at p = −1, L→L is √2
  (+3.01 dB) and R→R is 10^−5 (−100 dB), not 0. With w = 1 and split pans −1
  and 1, L→L and R→R are 1, and L→R and R→L are 0 within the comparison; with
  split pans 0 and 0 every gain is 0.7071068 (−3.01 dB). With v = 0 every gain
  is 0.
- In MIXER-VALUES-070 the original gives about 6·10^−17 for L→R and R→L,
  where the formula gives 0. The comparison's bound of 10^−12 absorbs this.
- Expectations exist only for the inputs of MIXER-VALUES-065 to 073, which
  have w and v each 0 or 1. Which w and v the audio path supplies for a track,
  including which w belongs to which `PanMode` code and any ramp between them,
  and the application of these gains to audio are not released.

### REQ-MIXER-VALUES-014 — partial: crossfade curve levels (computed values)

- **Extracted execution.** Each crossfade curve code c of
  REQ-MIXER-VALUES-009 gives a level T_c(x), a binary32 value, at each of the
  curve positions x = −1, −0.5, −0.25, 0, 0.25, 0.5 and 1. MIXER-VALUES-074
  to 080 list these levels. No level is released for any other position, and
  the listed levels do not define one, for example by interpolation.
- Consequences: every curve gives 1 at −1 and 0 at 1, and no level rises as x
  increases among the listed positions. At 0 the levels are: Dipped 0.5,
  Intermediate 0.5821068, Constant Power 0.7071068, and 1 for Slow Fade,
  Slow Cut, Fast Cut and Transition.
- Expectations exist only for the listed positions. Levels at other positions,
  how the crossfader value and a track's crossfade assignment give the curve
  position, and the application of the levels to audio are not released.

## Acceptance representation and comparison

[cases.json](cases.json) lists 80 cases. Each has an action, an
`expectation_provenance` label (see
[What the contract means](#what-the-contract-means)), a comparator and an
expected result.

**`open` cases** (MIXER-VALUES-001 to 037) have one input fixture: open the
document and change nothing. The expected result has these parts:

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

**`compute` cases** (MIXER-VALUES-038 to 080) have no fixture (`input` is
null). The `compute` field names the function and its inputs:

| `function` | Inputs | Expected | Comparison |
| --- | --- | --- | --- |
| `position-to-gain` | `curve` (`volume` or `send`), `position` | `gain` | the expected binary32 value or one of its two neighbours |
| `gain-to-position` | `curve`, `gain` | `position` | within 0.000001 of the expected value |
| `round-trip` | `curve`, `gain` | `gain`: the gain after converting `gain` to a position and back | exactly the expected binary32 value, which equals the input |
| `pan-law` | `w`, `pan`, `split_left`, `split_right`, `v` | `gains` with keys `L->L`, `L->R`, `R->L`, `R->R` | each gain: the expected binary32 value, one of its two neighbours, or within 10^−12 of it |
| `crossfade-level` | `curve` (a code of REQ-MIXER-VALUES-009), `positions` | `levels`: one `position` and `level` per listed position | each level as for `pan-law` |

This is a **project comparison representation**, not an API claimed to exist
in Live and not a required design. A candidate adapter may translate its own
result into these labels. Each `open` case starts from its fixture alone, and
each `compute` case from its inputs alone. Reading and computing have no timing
tolerance, cancellation step or teardown within this scope, so those case
kinds are omitted.

## Reference comparison obligation (not executed)

A later comparison of an `open` case against the original application opens
the case's fixture itself, encoded as the comparison requires (the compressed
container is outside this release), in a host whose locale uses `.` as the
decimal separator. Each value is observed after opening, before any control is
touched.

- The observation channel for `value` is chosen by the validation analyst. A
  channel that rounds must be compared at its rounding.
- A `text` observation must come from a place where the application shows the
  value text in the forms of this release: with ` dB` and `-inf dB` for
  volumes and sends, with `C`, `L` or `R` for pans, and as `On` or `Off` for
  the track switch. An observation that shows another form, for example the
  digits without the unit, is inconclusive, not a mismatch.
- A `name` observation must come from a place that shows the name of the code,
  for example a list of the choices.

The original application offers no observation of the `compute` values within
this release: fader positions, pan-law gains and crossfade levels are not
shown or stored as such. They can only be computed again with the original
program's code, as was done to obtain them. A candidate's own computation is
compared with the expected values.

None of this has been run.

## Exclusions and deferred obligations

Requirements not released:

- **REQ-MIXER-VALUES-010** (number text on save): what a save by the target
  build writes for mixer values is not established.
- **REQ-MIXER-VALUES-011** (volume gain applied to audio and the silence
  limit) and **REQ-MIXER-VALUES-012** (send gain applied to audio): which gain
  the audio path applies rests on conditions that are not established, and
  rendered audio is outside this release.
- **REQ-MIXER-VALUES-015** (out-of-range and alternative stored values):
  unknown.

Parts of released requirements that are not released: in REQ-MIXER-VALUES-005,
any binding of the curves to faders, controls or audio, inputs other than
those of the cases, and the round trip of other gains; in
REQ-MIXER-VALUES-013, the inputs the audio path supplies, ramps, other inputs,
which signal each gain scales, and the application to audio; in
REQ-MIXER-VALUES-014, levels at other positions, the crossfader and assignment
mapping, ramps and the application to audio.

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
- documents whose structure differs from the template set other than in the
  mixer value texts the cases change, including another number of tracks,
  scenes, clip slots, send holders or `SendsPre` items, a `SendPreBool` other
  than `false`, and added clips, devices or envelopes;
- computed inputs other than those of the cases: other positions and gains,
  other pan-law inputs (including w or v other than 0 and 1), other crossfade
  positions, and round trips of gains other than the seven listed;
- any other envelope, format version, compressed container or document kind.

Excluded behavior:

- what is written on save, including the text of mixer values and of their
  controller ranges;
- the gains the audio path derives from stored values, and where and when it
  applies them: the volume and send gains and any silence limit, which w and v
  feed the pan law, the crossfade factor of an assigned track, ramps, and
  rendered audio;
- what opening, showing or saving does with out-of-range values;
- the fader positions shown, and the mapping of faders and controllers to the
  conversions of REQ-MIXER-VALUES-005;
- which end of the crossfader favors A or B, and crossfade levels at other
  positions;
- which part of the user interface shows which text, and whether any part
  shows the same value in another form, for example the digits without the
  unit or without `-inf`;
- editing after opening, including text entry, keys, mouse, remote control and
  MIDI; creating tracks, and the values of new mixers and new sends; undo;
- the meaning of `EnabledByUser`, `SoloSink` and `SendPreBool`; whether the
  cue track's volume is the preview level; a text for the crossfader value;
- whether a set with another structure opens, and the rules that decide it.

Before claiming reference compatibility, a separately designed bounded probe
must run the `open` cases, or a justified equivalent set, against the original.
It must pin the original and candidate builds and the fixture bytes, retain
independent observations, and report mismatches. Candidate-only success proves
agreement with this contract, not with the running original.

## Fixture provenance

All 37 fixtures were authored for this release from one template set written
for it. The template set has the envelope above and, in `LiveSet`, in this
order:

- `NextPointeeId` 67. Every `AutomationTarget` and `ModulationTarget` in the
  set has an `Id` from 1 to 66, each used once.
- `Tracks`, holding:
  - `MidiTrack Id="1"`, named `Lead` (`EffectiveName` and `UserName`), colour 15;
  - `AudioTrack Id="2"`, with `EffectiveName` `2-Audio` and an empty
    `UserName`, colour 3;
  - `ReturnTrack Id="3"`, with `EffectiveName` `A-Return` and an empty
    `UserName`, colour 55.

  Each track holds `Name`, `Color`, an empty `AutomationEnvelopes/Envelopes`,
  `TrackGroupId` −1 and a `DeviceChain` with `AudioOutputRouting` to
  `AudioOut/Main`, the `Mixer`, and an empty device list
  (`DeviceChain/Devices`). The MIDI and audio tracks also hold, between the
  mixer and the device list, a `MainSequencer` and a `FreezeSequencer` whose
  `ClipSlotList`s each hold two empty clip slots (`Id` 0 and 1, with
  `HasStop` true).
- `MainTrack`, with `EffectiveName` `Main` and an empty `UserName`, colour 69,
  and two envelopes, each with one event at time −63072000: the tempo (120)
  and the time signature (code 201). Its `DeviceChain` holds `AudioOutputRouting` to `AudioOut/External/S0`,
  the main mixer and an empty device list.
- `PreHearTrack`, whose `DeviceChain` holds the cue mixer.
- `SendsPre` with one `SendPreBool` (`Id="0"`, `false`).
- `Scenes`, with two scenes (`Id` 0 and 1, named `Scene 1` and `Scene 2`,
  colour −1, tempo 120 and time signature 201, both disabled, and a follow
  action that is not enabled).
- `Transport` (loop off, loop start 0, loop length 8, position 0),
  `GlobalQuantisation` 4, `AutoQuantisation` 0 and `CrossfadeCurve` 2.

Mixer values in the template set: volumes `1`, pans `0`, split pans `-1` and
`1`, pan mode `0`, track switch `true`, `SoloSink` `false`, crossfade
assignment `1`, crossfader `0`, `On` `true`, and sends `0.0003162277571` with
`EnabledByUser` as stated in REQ-MIXER-VALUES-003. Volumes have the controller
range 0.0003162277571 to 1.99526238, sends 0.0003162277571 to 1, pans −1 to 1
and crossfade assignments 0 to 2; the main mixer's tempo is 120 and its time
signature code 201.

Each fixture is the template set with exactly the changes its purpose states:
the same changes as for the same case in mixer-values-v1. Text is ASCII with
line-feed line endings, one tab of indentation per level and a final newline.

No fixture contains shipped file content, program code or assets. Expected
results are newly authored behavioral data. No public source or dependency is
approved or included. Review status is recorded in
[the manifest](manifest.json) and [the review disposition](REVIEW.md).
