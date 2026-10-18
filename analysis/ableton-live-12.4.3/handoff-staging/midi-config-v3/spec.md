# MIDI configuration interpretation and value transforms — release 3

Target: Ableton Live 12 Suite 12.4.3 (2026-07-07_e3d8be4d07), macOS.
Feature: FEAT-MIDI-USER-MAPPING. Parent specification identity:
SPEC-MIDI-USER-MAPPING revision 3. Release: midi-config-v3, which
supersedes midi-config-v2 as a strict superset. Only the
clauses explicitly included below are in scope. No other clause of a listed
requirement is implicitly approved. This document is self-contained.

**Status: reviewed local release.** A separate review approved the clauses
below, recorded in [the review disposition](REVIEW.md). The clauses carried
from midi-config-v2 keep the narrowing of that release's review.
Implementation requires a fresh, restricted implementation workspace.

## What the contract means

A user supplies a text file named `UserConfiguration.txt` that assigns MIDI
messages to device, mixer, transport and drum-pad controls. This contract
describes how that file is **interpreted**: which assignments are enabled, the
MIDI address of each (message type, number, channel), the user target it
names, its map-mode label (continuous controls) or button kind (buttons), and
the device parameter bank span. For continuous controls it also specifies the
[value transforms](#value-transforms): the parameter value that each incoming
Control Change message produces in each map mode. It does not specify what a
button or pad does with a message, audio results, feedback, or when a
configuration takes effect.

All rules and expected results are **static-derived** from evidence about the
pinned build, before sanitization. None is an observed reference execution. No
compatibility result is established; the original application remains the
authority for a later comparison.

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
values. This release requires *min* < *max*, a current value in [*min*,
*max*], an integer *min*, *max* and current value for a stepped parameter, and
a parameter that keeps exactly the value last set on it. A value set on a
stepped parameter is rounded to the nearest integer, with halves away from
zero. On/off parameters have no expectation. Which application parameter a
target is, and its kind, range and stepping, are not specified.

**Absolute.** Data value *v* sets *min* + (*max* − *min*) × *v*/127.

**Absolute14Bit.** Number *n* carries the most significant seven bits (MSB)
and number *n* + 32 the least significant seven bits (LSB), on the same
channel. The label rule above keeps *n* at 95 or below. A received half is held
until the other half arrives, in either order. A newer half replaces a held
half of the same kind, and a lone half changes nothing. When both halves are
held, the value becomes *min* + (*max* − *min*) × (128 × MSB + LSB)/16383, and
both held halves are discarded.

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

A parameter that is not stepped becomes clamp(current + (*max* − *min*) ×
*d*/256, *min*, *max*). A stepped parameter moves one unit per message: +1
when *d* > 0 and −1 otherwise, so a decoded 0 moves it down. The result is
clamped to [*min*, *max*].

**Takeover.** Live's preferences offer one application-wide takeover setting
with three choices. This release specifies one of them, called `none` here:
the choice under which takeover never acts. Under `none`, every value given by
the rules above applies. Under every choice, three groups of values also apply
directly: values of the eight relative modes; values for a parameter of kind
enumerated or other; and `Absolute` values of the crossfader. Under the other
two choices, any other value has no expectation. This includes `Absolute14Bit`
values of the crossfader, which are not exempt.

*Stated assumption.* `none` is believed to be the choice labelled None. That
correspondence is inferred from the order of the setting's choices and has not
been observed. Cases that name `none` depend on it; see the
[comparison obligations](#exclusions-and-deferred-obligations).

**REQ-MIDI-USER-010 — partial: master, cue and crossfader values.** Master
volume, cue volume and the crossfader take values by these rules with their
map modes. Master and cue volume are subject to takeover like the other
controls; the crossfader's `Absolute` values are exempt.

**Starting state and order.** A value case starts with the configuration
active and the MIDI input just opened: nothing has been received on it, no
14-bit half is held, and the parameter is at its initial value. Only the
case's messages arrive on that input. They arrive one at a time, in order,
and each is applied before the next arrives.

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

Cases MIDI-CONFIG-110 to 127 are value cases. Their fixture is interpreted and
compared like any other case, and each adds a `stimulus`:

| Field | Meaning |
| --- | --- |
| `takeover` | `none`, or `any`: the expected values hold under every takeover choice |
| `parameter` | The target label and its description: `kind`, `stepped`, `min`, `max` and `initial_value` |
| `messages` | Three-byte Control Change messages in hexadecimal, in the order they arrive |

`expected.values` gives the parameter value after each message, on the
parameter's own scale, including after messages that leave it unchanged.
Values are exact results rounded to nine decimal places; compare each within
an absolute tolerance of 1e-6. Every value case uses number 20 on channel 0,
and the `Absolute14Bit` cases also send number 52. A candidate adapter may
supply a test parameter with the given description at the target and feed the
messages to the interpreted assignment.

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
any map mode; a target parameter whose *min* is not below its *max*; a stepped
parameter with a non-integer *min*, *max* or current value; a current value
outside [*min*, *max*]; a parameter that changes a value after it is set;
under a takeover choice other than `none`, `Absolute` and `Absolute14Bit`
values for a continuous parameter, except `Absolute` values of the crossfader;
another enabled assignment on number *n* + 32 and the channel of an
`Absolute14Bit` control with number *n*; and other MIDI input during a value
case, including running status.

Excluded behavior: how the application reports or recovers from inputs that
fail to load; profile discovery, naming, activation and reload; value behavior
outside the [value transforms](#value-transforms), including Pick-Up and Value
Scaling, the labels of the takeover choices other than `none`, the default
choice and on/off parameter values; when a value is applied, and the ordering,
coalescing and deferral of messages sent back to back; displayed values; which
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

A reference comparison of value cases must also: confirm that the choice used
for `none` cases is the one under which takeover never acts, believed to be
None; record the choice used for `any` cases, since the exemptions are
exercised only under another choice; use a target whose parameter matches the
description, except that the crossfader's range cannot be chosen, so if it
reports another range the expected values are *min* + (*max* − *min*) ×
*v*/127 for the same data values, and if it is stepped or on/off the case does
not apply; open the input immediately before the case; and read each value
only after its message has been applied, by a bounded completion method and
never from the display. Silence after a wait is not evidence that a value is
unchanged.

## Changes from midi-config-v2

The change list and the supersession record are in
[the README](README.md#changes-from-midi-config-v2) and
[the manifest](manifest.json). No midi-config-v2 clause, case or fixture is
changed.

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
content, program code or assets. Expected JSON is newly authored
static-derived behavioral data. No public source or dependency is approved or
included. The MIDI byte sequences and parameter descriptions of the value
cases are also authored for this release. Review status is recorded in
[the manifest](manifest.json) and [the review disposition](REVIEW.md).
