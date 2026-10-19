# MIDI configuration interpretation and value transforms — release 4

Target: Ableton Live 12 Suite 12.4.3 (2026-07-07_e3d8be4d07), macOS.
Feature: FEAT-MIDI-USER-MAPPING. Parent specification identity:
SPEC-MIDI-USER-MAPPING revision 5. Release: midi-config-v4, which
supersedes midi-config-v3 ([README](README.md#supersession)). Only the
clauses explicitly included below are in scope. No other clause of a listed
requirement is implicitly approved. This document is self-contained.

**Status: reviewed local release.** A separate review approved the clauses
below, recorded in [the review disposition](REVIEW.md). The clauses carried
from midi-config-v3 keep the narrowing of the earlier releases' reviews.
Implementation requires a fresh, restricted implementation workspace.

## What the contract means

A user supplies a text file named `UserConfiguration.txt` that assigns MIDI
messages to device, mixer, transport and drum-pad controls. This contract
describes how that file is **interpreted**: which assignments are enabled, the
MIDI address of each (message type, number, channel), the user target it
names, its map-mode label (continuous controls) or button kind (buttons), and
the device parameter bank span. For continuous controls it also specifies the
[value transforms](#value-transforms): the parameter value that each incoming
Control Change message produces in each map mode, including
[takeover](#takeover). It does not specify what a button or pad does with a
message, audio results, feedback, or when a configuration takes effect.

Every expected result carries one of two provenance labels:

- **Static-derived**: derived from evidence about the pinned build, reviewed
  before sanitization. Cases MIDI-CONFIG-001 to 127 carry it.
- **Extracted execution**: the original program's own code that turns a
  received Control Change message into a parameter value ran on the case's
  messages: the handling of each message and of 14-bit halves, the value
  computation and takeover. It ran on a Linux x86_64 host, from the program's
  x86_64 build, with glibc in place of the macOS system libraries. The
  substituted functions only provide memory and initialization services; none
  computes a value. The takeover choice was set through the program's own
  preference code. The run itself supplied the target parameter, which
  returned the value last set on it, and the previous data value on each
  controller number. Two parts of that code did not run: a notification
  that Pick-Up gives after it has decided a value, and the route that
  applies a value later instead of at once; the run applied each value at
  once. Cases MIDI-CONFIG-128 to 161 carry it.

In every case the interpreted assignments are static-derived. So are the
rules that say which earlier data value counts as previous, which preference
entry selects each takeover choice, and that the crossfader's exemption from
takeover does not cover its 14-bit pairs (MIDI-CONFIG-150). The value cases
rest on three stated assumptions:

- the macOS arm64 build computes the extracted-execution values as the x86_64
  build does, except that it rounds once where the x86_64 build rounds twice
  when it forms the target value of an absolute message. The results then
  differ by at most one binary32 unit in the last place of max(|*min*|,
  |*max*|), and not at all when the smaller of *min* and *max* is 0. τ covers
  that difference. Cases MIDI-CONFIG-128 to 161 depend on this;
- the application gives this code the parameter's range, kind and stepping,
  its current value and the previous data values as this contract states
  them, and the parameter keeps the value set on it. Every value case depends
  on this, as the [preconditions](#value-transforms) require;
- the three preference entries display as None, Pick-Up and Value Scaling.
  Their wording was not read. Only the labels used in a reference comparison
  depend on this.

None is an observed run of the original application. No compatibility
result is established; the original application remains the authority for a
later comparison.

## Preconditions and bounded input grammar

Each fixture is a complete ASCII text file with LF line endings and a final
newline. Within the scope of this release, every line is one of:

- a section header `[Name]` starting in column 1;
- an option line `Key: value` or `Key = value` starting in column 1, with a
  single `:` or `=` delimiter; spaces around the key and the value are not
  part of either, and the value may be empty;
- a full-line comment starting in column 1 with `#` or `;`;
- a blank line.

Supported section names are exactly `Globals`, `DeviceControls`,
`MixerControls` and `TransportControls`, plus an optional `[DEFAULT]` section.
Any supported section may be absent. Assignments in one fixture have distinct
MIDI addresses. All interpretations assume a selected, active profile, existing
targets, correct input routing and no competing mapping or owner. Discovery and
activation remain outside the contract. Inputs listed under
[exclusions](#exclusions-and-deferred-obligations) have no expectation.

## Value interpretation

**Integer text.** After trimming, a value is integer text when it is an
optional `+` or `-` followed by ASCII decimal digits, in which an underscore
may appear only singly between two digits. Leading zeros are allowed.
Examples: `+20` is 20, `0021` is 21, `1_0` is 10. Any other value is a
**conversion failure**, including an empty value, `abc`, `0x14`, `20.0` and
`20 ; fader` (text after the number is part of the value).

**Number fields.** A CC number or pad note field enables its assignment when it
is integer text with a value from 0 through 127. A missing key, `-1`, any other
out-of-range integer, or a conversion failure disables it. A disabled assignment
is absent from the expected output.

**Channel fields.** A channel field is valid when it is integer text with a
value from 0 through 15.

**Boolean text.** For `MixerButtonsToggle`, the values `1`, `yes`, `true`, `on`
are true and `0`, `no`, `false`, `off` are false, in any letter case.

## Interpreted keys and targets

*N* is 1–8 for mixer strips (one bank of 8 tracks) and 1–16 for encoders and
pads. Keys are interpreted only in the section shown. The same spelling in
another section is a different key or is ignored. Any key not listed here is
ignored and does not disable other assignments.

| Section | Number key | Channel source | Target label | Kind |
| --- | --- | --- | --- | --- |
| `Globals` | `Pad`*N*`Note` (note) | `Pad`*N*`Channel`, see [pads](#pads) | `drum-pad:`*N* | none |
| `DeviceControls` | `Encoder`*N* | `EncoderChannel`*N* or global | `device-parameter:`*K* | map mode from `EncoderMapMode` |
| `DeviceControls` | `Bank`*N*`Button`, *N* 1–8 | global | `device-bank:`*K* | momentary |
| `DeviceControls` | `NextBankButton`, `PrevBankButton` | global | `device-bank-next`, `device-bank-previous` | momentary |
| `DeviceControls` | `LockButton`, `OnOffButton` | global | `device-lock`, `device-on-off` | momentary |
| `MixerControls` | `VolumeSlider`*N* | `Slider`*N*`Channel` or global | `track-volume:`*N* | map mode from `VolumeMapMode` |
| `MixerControls` | `Send1Knob`*N*, `Send2Knob`*N* | global | `track-send-a:`*N*, `track-send-b:`*N* | map mode from `SendsMapMode` |
| `MixerControls` | `TrackMuteButton`*N*, `TrackSoloButton`*N*, `TrackSelectButton`*N*, `TrackArmButton`*N* | global | `track-mute:`*N*, `track-solo:`*N*, `track-select:`*N*, `track-arm:`*N* | mixer button kind |
| `MixerControls` | `NextBankButton`, `PrevBankButton` | global | `mixer-bank-next`, `mixer-bank-previous` | mixer button kind |
| `MixerControls` | `MasterVolumeSlider` | `MasterSliderChannel` or global | `master-volume` | map mode from `VolumeMapMode` |
| `MixerControls` | `CueVolumeSlider` | `CueSliderChannel` or global | `cue-volume` | map mode from `VolumeMapMode` |
| `MixerControls` | `CrossfaderSlider` | `CrossfaderSliderChannel` or global | `crossfader` | map mode from `CrossfaderMapMode` |
| `TransportControls` | `StopButton`, `PlayButton` | global | `transport-stop`, `transport-play` | momentary |
| `TransportControls` | `RecButton`, `SessionRecButton`, `OverButton` | global | `arrangement-record`, `session-record`, `arrangement-overdub` | momentary |
| `TransportControls` | `MetroButton`, `LoopButton` | global | `metronome`, `arrangement-loop` | momentary |
| `TransportControls` | `RwdButton`, `FfwdButton` | global | `rewind`, `fast-forward` | momentary |
| `TransportControls` | `PunchInButton`, `PunchOutButton` | global | `punch-in`, `punch-out` | momentary |
| `TransportControls` | `NudgeUpButton`, `NudgeDownButton`, `TapTempoButton` | global | `nudge-up`, `nudge-down`, `tap-tempo` | momentary |

Target meanings: Drum Rack visible pad *N*; device parameter control position
*K* of the selected device; direct device-bank selector position *K*; next and
previous device parameter bank; lock controls to the selected device; Device
Activator; strip *N* track volume, Send A, Send B, mute, solo, selection and
arm; next and previous bank of 8 mixer tracks; master volume; cue/preview
volume; crossfader; Stop, Play, Arrangement Record, Session Record, Arrangement
Overdub, Metronome, Arrangement Loop, rewind, fast-forward, Punch-In,
Punch-Out, Phase Nudge Up/Down and Tap Tempo. `FwdButton` is not a key.

## Selected requirement clauses

**REQ-MIDI-USER-002 — partial: number enablement.** Every number key in the
table follows the number-field rule. Pad notes use the same rule for integer
text. All CC keys address Control Change messages; pad keys address Note
messages. Noninteger pad notes are excluded.

**REQ-MIDI-USER-003 — partial: channels.** The **effective global channel** is
`GlobalChannel` when that key is valid in `Globals`. A missing `Globals`
section, missing key, out-of-range integer or conversion failure gives 0.
A control with its own channel key uses that channel when it is valid and
otherwise the effective global channel. Every other CC control uses the
effective global channel; invented keys such as `LockButtonChannel` are
ignored. A valid explicit channel works even when `GlobalChannel` is invalid.
Channel rules never enable a disabled number. Pads follow [their own
rule](#pads).

**REQ-MIDI-USER-005 — partial: map-mode labels.** The map-mode keys accept
exactly these case-sensitive tokens: `Absolute`, `Absolute14Bit`,
`LinearSignedBit`, `LinearSignedBit2`, `LinearTwoCompliment`,
`LinearBinaryOffset`, `AccelSignedBit`, `AccelSignedBit2`,
`AccelTwoCompliment`, `AccelBinaryOffset` (`Compliment` is the literal
spelling). A missing map-mode key gives `Absolute`. Each continuous control
takes the label of the key in the table. When that label is `Absolute14Bit`
and the control's CC number is 96–127, the label is `Absolute` instead;
numbers 0–95 keep `Absolute14Bit`. The label states the configured mode; its
effect on parameter values is given under [value transforms](#value-transforms).

**REQ-MIDI-USER-006 — partial: pad identity.** Enabled pad *N* names visible
pad *N* of the documented 4×4 layout: pads 1–4 form the top row and 13–16 the
bottom row, left to right. Pad playback is not specified.

**REQ-MIDI-USER-007 — partial: encoder compaction and bank span.** Enabled
encoders take parameter positions *K* = 1, 2, … in ascending slot number;
disabled slots are skipped. `device_parameter_banks` is null with no enabled
encoder, 1 with 1–8 enabled encoders and 2 with 9–16, regardless of which slot
numbers are used. Which parameter of a device occupies a position is excluded.

**REQ-MIDI-USER-008 — partial: device button targets.** Enabled
`Bank`*N*`Button` keys take selector positions *K* = 1, 2, … in ascending *N*,
skipping disabled slots; for example, a lone `Bank8Button` is position 1. The
navigation, lock and activator keys name the targets in the table. All device
buttons are momentary on the effective global channel. Which bank a selector
or navigation input chooses, wrapping, lock and activator effects are excluded.

**REQ-MIDI-USER-009 — partial: strip and mixer-bank targets.** Each enabled
strip key names its strip *N* target; mixer bank keys name the mixer bank
targets. A `Send2Knob`*N* assignment is in scope only when `Send1Knob`*N* is
also enabled. Which track a strip addresses is excluded.

**REQ-MIDI-USER-010 — partial: master, cue and crossfader.** The three keys
name their targets with the channel rules above. `VolumeMapMode` applies to
master and cue volume as well as track volume; `CrossfaderMapMode` applies to
the crossfader. Their values follow the [value transforms](#value-transforms),
including the crossfader's takeover exemption. Audio results are excluded.

**REQ-MIDI-USER-011 — partial: mixer button kind.** Mixer strip buttons and
mixer bank buttons are `momentary` when `MixerButtonsToggle` is present with a
false Boolean value, and `toggle` when it is true or absent. The kind is a
configuration label; how either kind responds to data values is excluded.

**REQ-MIDI-USER-012 — partial: transport targets.** The 14 transport keys name
the targets in the table. All are momentary on the effective global channel.
Transport effects and timing are excluded.

**REQ-MIDI-USER-013 — partial: lexical rules.** Option names match in any
ASCII letter case; section names match exactly, so `[mixercontrols]` is not
`MixerControls`. `:` and `=` are equivalent delimiters. Full-line comments and
blank lines are ignored, but text after a value is part of the value. Values
and keys are trimmed. A key in `[DEFAULT]` counts as present in each supported
section that appears in the file and does not define that key itself. Unknown
keys and keys in the wrong section are ignored.

### Pads

Pads are read only from `Globals`; without that section there are no pads.
For an enabled pad note, the pad channel is `Pad`*N*`Channel` when valid. When
that key is missing or `-1`, the pad uses `GlobalChannel` if `GlobalChannel`
is valid; otherwise the pad is disabled. Any other integer channel disables the
pad. Unlike ordinary controls, pads do not fall back to channel 0. When a pad
note is not enabled, its channel text has no effect.

## Value transforms

**REQ-MIDI-USER-005 — partial: value transforms.** An enabled continuous
control turns incoming Control Change messages into values of its target
parameter. Continuous controls are the keys whose kind in the
[table](#interpreted-keys-and-targets) is a map mode: encoders, track volume,
send knobs, master volume, cue volume and the crossfader. Each uses the
channel, number and map-mode label of its interpreted assignment.

**Messages.** A message is three bytes: hexadecimal B0 plus the channel *c*
(a Control Change on channel 0–15), the controller number *n* and the data
value *v* (0–127). Cases write them in hexadecimal, so `B0 14 40` is channel 0,
number 20, data value 64. A control acts only on messages with its channel and
number; an `Absolute14Bit` control also acts on number *n* + 32 on its
channel. Each message produces at most one new value, applied once and without
smoothing.

**Target parameter.** The target is a parameter with a minimum *min*, a
maximum *max*, a current value, a kind (continuous, on/off, enumerated or
other) and a stepped property: a stepped parameter takes only whole-number
values. The maximum may be below the minimum, a *reversed range*; *lo* and
*hi* are the smaller and the larger of *min* and *max*. This release requires
*min* ≠ *max*, a current value in [*lo*, *hi*], an integer *min*, *max* and
current value for a stepped parameter, and a parameter that keeps exactly the
value last set on it. A target value computed by the rules below for a stepped
parameter is rounded to the nearest integer, with halves away from zero; a
Value Scaling move ([takeover](#takeover)) is the one value that is not
rounded. On/off parameters have no expectation. Which application parameter a
target is, and its kind, range and stepping, are not specified.

**Target value.** A data value *x* gives the target value *min* + (*max* −
*min*) × *x*/127, rounded if the parameter is stepped. This holds for either
range order. *x* is a message's data value, or for a 14-bit pair the fraction
given below.

**Absolute.** Data value *v* sets *min* + (*max* − *min*) × *v*/127, the
target value of *v*, subject to [takeover](#takeover).

**Absolute14Bit.** Number *n* carries the most significant seven bits (MSB)
and number *n* + 32 the least significant seven bits (LSB), on the same
channel. The label rule above keeps *n* at 95 or below. A received half is held
until the other half arrives, in either order. A newer half replaces a held
half of the same kind, and a lone half changes nothing. When both halves are
held, the value becomes *min* + (*max* − *min*) × (128 × MSB + LSB)/16383,
subject to takeover, and both held halves are discarded. That is the target
value of *x* = (128 × MSB + LSB)/129.

**Relative modes.** The eight other modes decode data value *v* into a signed
step *d*:

| Mode | *d* for data value *v* |
| --- | --- |
| `LinearSignedBit` | v ≤ 64: +v; v ≥ 65: −(v − 64) |
| `LinearSignedBit2` | v ≤ 64: −v; v ≥ 65: +(v − 64) |
| `LinearTwoCompliment` | v ≤ 64: +v; v ≥ 65: v − 128 |
| `LinearBinaryOffset` | v − 64 |
| `AccelSignedBit` | v ≤ 64: +A(v); v ≥ 65: −A(v − 64) |
| `AccelSignedBit2` | v ≤ 64: −B(v); v ≥ 65: +B(v − 64) |
| `AccelTwoCompliment` | v ≤ 65: +B(v); v ≥ 66: −B(128 − v) |
| `AccelBinaryOffset` | v ≥ 64: +B(v − 64); v ≤ 63: −B(64 − v) |

A(*k*) is 1, 2, 3, 4, 5, 8, 10, 20, 50 for *k* = 1 to 9, and 20 for any other
*k*, including 0. B(*k*) is 1, 2, 3, 4, 5, 8, 20, 50 for *k* = 1 to 8, and 50
for any other *k*, including 0. Hence `AccelSignedBit` 10 to 64 gives +20,
`AccelBinaryOffset` 64 gives +50 and `AccelTwoCompliment` 65 gives +50.

A parameter that is not stepped becomes current + (*max* − *min*) × *d*/256,
clamped to [*lo*, *hi*]. A stepped parameter moves one unit per message, toward
*max* when *d* > 0 and toward *min* otherwise, so a decoded 0 moves it toward
*min*. With *min* < *max* that is +1 and −1; with a reversed range it is −1
when *d* > 0 and +1 otherwise. The result is clamped to [*lo*, *hi*].

### Takeover

Live's preferences offer one application-wide takeover setting with three
entries. This contract names the choices they select, in the order offered:
`none`, `pick-up` and `value-scaling`. Which entry selects which choice is
static-derived from the order in which the entries are built and the position
each one sends. Their displayed wording was not read; it is believed to be
None, Pick-Up and Value Scaling (a stated assumption). The default choice is
not known, so every value case names its choice.

Takeover acts only on *absolute target values*: the target value of an
`Absolute` message, or of a completed `Absolute14Bit` pair, for a continuous
parameter. Three groups of values apply directly under every choice: values of
the eight relative modes; values for a parameter of kind enumerated or other;
and `Absolute` values of the crossfader. A completed `Absolute14Bit` pair of
the crossfader is subject to takeover like any other control's pair. Under
`none`, every value given by the rules above applies.

**Previous data values.** The input keeps, for each channel and controller
number, the last data value received there. The record is empty when the input
opens. Every message on the input counts, whether or not an assignment uses
it, and within this release nothing else empties the record. For an
`Absolute` message, the previous data value is the one recorded on its channel
and number before it, if any. For a completed pair, let *m* be the data value
received on number *n* before the held MSB, and *l* the one received on *n* +
32 before the held LSB, on the same channel. Either is missing when nothing
preceded that half since the input opened. The pair's previous data value is
(128 × *m* + *l*)/129 when both exist; −1/129 when neither exists; −128 +
*l*/129 when only *l* exists; and, when only *m* exists, −1/129 for an odd *m*
and −1 for an even *m*. A pair therefore always has a previous data value,
including the first pair after the input opens.

**Pick-Up and Value Scaling.** Let *n* be an absolute target value subject to
takeover under `pick-up` or `value-scaling`, *c* the current value, *w* =
(*hi* − *lo*)/64, and *p* the target value of the previous data value, formed
like *n*, including rounding for a stepped parameter. *p* may lie outside
[*lo*, *hi*]. The new value is given by the first of these rules that applies:

1. *c*, for an `Absolute` message without a previous data value, or when *p*
   is exactly −129;
2. *n*, when |*p* − *c*| ≤ (*hi* − *lo*)/256;
3. under `pick-up`: *n* when *c* lies in [min(*n*, *p*) − *w*, max(*n*, *p*) +
   *w*], and *c* otherwise;
4. under `value-scaling`: *n* when |*n* − *c*| ≤ *w*; *c* when *p* = *n*; and
   otherwise a *move* by the travelled fraction of the remaining distance:
   *c* + (*hi* − *c*)(*n* − *p*)/(*hi* − *p*) when *n* > *p*, and
   *c* − (*c* − *lo*)(*p* − *n*)/(*p* − *lo*) when *n* < *p*. A move is not
   rounded, even for a stepped parameter.

Every bound is inclusive. The new value is clamped to [*lo*, *hi*]. The rules
hold for either range order: *lo*, *hi* and *w* use the sorted bounds, while
*n* and *p* are ordinary target values.

### Master, cue and crossfader values

**REQ-MIDI-USER-010 — partial: master, cue and crossfader values.** Master
volume, cue volume and the crossfader take values by these rules with their
map modes. Master and cue volume are subject to takeover like the other
controls; the crossfader's `Absolute` values are exempt, and its completed
`Absolute14Bit` pairs are not.

### Starting state, order and precision

**Starting state and order.** A value case starts with the configuration
active and the MIDI input just opened: nothing has been received on it, so
the record of previous data values is empty, no 14-bit half is held, and the
parameter is at its initial value. Only the case's messages arrive on that
input. They arrive one at a time, in order, and each is applied before the
next arrives.

**Precision.** The rules are stated in exact arithmetic. The original computes
in IEEE 754 single precision (binary32), and values are compared within the
tolerance τ given under [value cases](#value-cases). τ covers the rounding of
one message. Over relative messages in a row on a parameter that is not
stepped, that rounding can add up, so a value reached by *k* relative
messages in a row is compared within *k* × τ. Three kinds of result can lie
farther from the exact rules than that, so outside the cases that state them
they have no expectation:

- A takeover comparison or test whose two sides lie within 8τ of each other:
  *c* and a window bound, |*p* − *c*| and (*hi* − *lo*)/256, |*n* − *c*| and
  *w*, *p* and −129, or *p* and *n*, except *p* = *n* for one and the same
  data value. Rounding can decide it either way. Cases MIDI-CONFIG-149 and
  152 to 161 place a test exactly on its bound or one binary32 step beyond
  it; their expected values hold.
- A target value *n* or *p* of a stepped parameter whose exact value lies
  within 8τ of a half-integer. Rounding can give either adjacent whole
  number. No case has one.
- A Value Scaling move. The travelled fraction can magnify rounding far beyond
  τ. The moves in cases MIDI-CONFIG-129, 133, 137, 138, 143 to 145, 153, 155
  and 161, all with a smaller bound of 0, lie within τ of the exact rule;
  their expected values hold. None of them is on a stepped parameter. A
  stepped parameter takes only whole-number values, so its value after a
  move has no expectation.

After such a result, the later values of the same sequence have no
expectation either.

## Acceptance representation and comparison

[cases.json](cases.json) gives each input and its complete expected output:
`assignments` (a set) and `device_parameter_banks`. Every assignment has:

| Field | Meaning |
| --- | --- |
| `section` | Section name from the table |
| `control` | Canonical key spelling from the table, whatever case the file used |
| `target` | Target label from the table |
| `message_type` | `control-change`, or `note` for pads |
| `number` | Integer 0–127 |
| `channel` | Effective integer channel 0–15 |
| `map_mode` | Continuous controls only: one of the ten tokens |
| `button_kind` | Buttons only: `momentary` or `toggle` |

Pads carry neither `map_mode` nor `button_kind`. This is a **project comparison
representation**, not an API claimed to exist in Live or a required design. A
candidate adapter may translate its own result into these labels. Compare exact
sets over all fields with no missing or extra assignment; order has no meaning.
`device_parameter_banks` compares exactly. Each case starts from fresh input.
Logical interpretation has no timing tolerance, and silence after a short wait
does not prove an assignment is disabled. The fixture set is not an executable
harness for the original application.

### Value cases

Cases MIDI-CONFIG-110 to 161 are value cases. Their fixture is interpreted and
compared like any other case, and each adds a `stimulus`:

| Field | Meaning |
| --- | --- |
| `takeover` | `none`, `pick-up` or `value-scaling`; or `any`: the expected values hold under every takeover choice |
| `parameter` | The target label and its description: `kind`, `stepped`, `min`, `max` and `initial_value`. The initial value is a binary32 number; the decimal given, read as a double-precision number, is exactly that number |
| `messages` | Three-byte Control Change messages in hexadecimal, in the order they arrive |

`expected.values` gives the parameter value after each message, on the
parameter's own scale, including after messages that leave it unchanged,
rounded to nine decimal places. For the static-derived cases 110 to 127 they
are exact results; for the extracted-execution cases 128 to 161 they are that
execution's binary32 results. Compare each value within

τ = max(1e-6, 2⁻²² × max(|*min*|, |*max*|)),

absolute, with the case's *min* and *max*. τ is 1e-6 for cases 110 to 127,
the tolerance midi-config-v3 stated; each new case's comparator gives its τ.
τ covers the original's rounding of one message and the one difference
between its two builds (see [provenance](#what-the-contract-means)). The
[precision](#starting-state-order-and-precision) rules say where it does not:
after relative messages in a row, near a bound, near a half-integer on a
stepped parameter and for Value Scaling moves. Each step of the relative
cases is exact in single precision, so τ holds for each of their values.
Every value case uses number 20 on channel 0, and the `Absolute14Bit` cases
also send number 52. A candidate adapter may supply a test parameter with the
given description at the target and feed the messages to the interpreted
assignment.

## Exclusions and deferred obligations

These inputs have **no expectation** in this release: duplicate sections;
duplicate option names after case folding; text before the first section
header; option lines without a delimiter; indented or continuation lines; `%`
in any value; non-ASCII bytes, CR line endings, or ASCII control characters
other than the LF line ending, including tabs; a noninteger pad note, or a
noninteger pad channel for an enabled pad note; integer text longer than 640
characters in a pad note, or in a pad channel for an enabled pad note; a
`MixerButtonsToggle` value that is not a listed Boolean; any
`InvertMuteButtonFeedback` key; a map-mode value that is not exactly one of the
ten tokens, including case variants; two enabled assignments with the same MIDI
address; and `Send2Knob`*N* enabled while `Send1Knob`*N* is not.

Value behavior also has **no expectation** for: on/off target parameters in
any map mode; a target parameter whose *min* equals its *max*; a stepped
parameter with a non-integer *min*, *max* or current value; a current value
outside [*lo*, *hi*]; a parameter that changes a value after it is set; the
results near a bound, the stepped target values near a half-integer and the
Value Scaling moves described under
[precision](#starting-state-order-and-precision), outside the cases listed
there, and the later values of their sequences; another enabled assignment on
number *n* + 32 and the channel of an `Absolute14Bit` control with number *n*;
other MIDI input during a value case, including running status; and anything
else that empties the record of previous data values, such as another control
surface on the same input.

Excluded behavior: how the application reports or recovers from inputs that
fail to load; profile discovery, naming, activation and reload; value behavior
outside the [value transforms](#value-transforms), including the default
takeover choice, the displayed wording of the choices, any notification or
display while takeover holds a value, and on/off parameter values; when a
value is applied, and the ordering, coalescing and deferral of messages sent
back to back; displayed values; which
application parameter a target is, and its kind, range and stepping; what any
button does with a data value, including toggling, held
seeking, nudge and tap timing; bank navigation, bank contents, lock and
activator effects; which tracks strips address; arm, solo and select
interactions; pad playback and note lifetime; MIDI feedback and mute feedback
inversion; collisions and competing mappings; UI presentation; persistence,
undo and automation; latency, cancellation, disconnect and teardown with held
controls. The interpretation has no specified asynchronous lifecycle, so those
cases are deferred, not passed.

Before claiming reference compatibility, run a separately designed bounded
probe for these cases or a justified equivalent set. Pin the original and
candidate builds and fixture bytes, retain independent observations and report
mismatches. Candidate-only success proves agreement with this contract, not
with the running original.

A reference comparison of value cases must also: select each case's choice by
its entry's position (first `none`, second `pick-up`, third `value-scaling`)
and record the entry's displayed wording, believed to be None, Pick-Up or
Value Scaling; record the choice used for `any` cases, since the exemptions
are exercised only under `pick-up` or `value-scaling`; use a target whose
parameter matches the description, set to its initial value, except that the
crossfader's range cannot be chosen: if it reports another range,
MIDI-CONFIG-126 expects *min* + (*max* − *min*) × *v*/127 for the same data
values, and MIDI-CONFIG-150 starts from and expects *min* + (*max* − *min*) ×
*x* for each stated value *x*; if the crossfader is stepped or on/off, those
cases do not apply; open the input immediately before the case; and read each
value only after its message has been applied, by a bounded completion method
and never from the display. Silence after a wait is not evidence that a value
is unchanged.

## Changes from midi-config-v3

The change list and the supersession record are in
[the README](README.md#changes-from-midi-config-v3) and
[the manifest](manifest.json). No midi-config-v3 case, fixture or expected
value is changed.

## Earlier changes: midi-config-v3 from midi-config-v2

1. REQ-MIDI-USER-005 gains the value transforms: `Absolute`, `Absolute14Bit`
   pairing, the eight relative decode tables and step rules, rounding on
   stepped parameters, the takeover choice `none` and the values exempt from
   takeover.
2. REQ-MIDI-USER-010 gains master, cue and crossfader values, with the
   crossfader's `Absolute` values exempt from takeover.
3. The midi-config-v2 exclusion of numeric transforms, 14-bit pairing, relative
   arithmetic, pickup and takeover narrows to the value exclusions listed in
   the contract.
4. Value cases add a `stimulus` (takeover, parameter, messages) and
   `expected.values`. The other case fields are unchanged.
5. Cases MIDI-CONFIG-110 to 127 are new value cases.
6. Every midi-config-v2 clause, case and fixture is carried unchanged, and
   nothing in midi-config-v2 is contradicted. The sentences that left value
   behavior unspecified, in the contract summary, REQ-MIDI-USER-005,
   REQ-MIDI-USER-010 and the exclusions, now point to the new section.

## Earlier changes: midi-config-v2 from midi-config-v1

1. Scope widened from three mixer controls to every number key in the table,
   16 pads, map-mode labels, button kinds and the device parameter bank span.
   Requirements 005–009, 011 and 012 gain partial clauses; 002, 003, 010 and
   013 are widened. Requirements 001 and 004 remain unreleased.
2. Representation: `section`, `map_mode`, `button_kind`,
   `device_parameter_banks` and `message_type: note` are added.
3. The 54 midi-config-v1 cases keep their IDs, fixture bytes and logical
   expectations. They gain `section: MixerControls`, `map_mode: Absolute`
   and `device_parameter_banks: null`, and now also list REQ-MIDI-USER-005.
4. Cases MIDI-CONFIG-055 to 109 are new.
5. Nothing in midi-config-v1 is contradicted. Its bounded grammar is widened by
   the lexical rules above.

## Fixture provenance

All fixtures were independently authored for these cases using public
configuration field names and simple values. They contain no shipped file
content, program code or assets. Expected JSON is newly authored behavioral
data, labeled per case as static-derived or extracted execution. No public
source or dependency is approved or included. The MIDI byte sequences and
parameter descriptions of the value cases are also authored for these cases.
Review status is recorded in [the manifest](manifest.json).
