# Transport state in Live Set documents — release 1

Target: Ableton Live 12 Suite 12.4.3 (2026-07-07_e3d8be4d07), macOS.
Features: FEAT-TRANSPORT with FEAT-PERSISTENCE. Parent specification identity:
SPEC-TRANSPORT-STATE revision 1. Release: transport-state-v1. Only the clauses
explicitly included below are in scope. No other clause of a listed requirement
is implicitly approved. This document is self-contained.

**Status: reviewed local release.** A separate review approved the clauses
below with the narrowing recorded in [the review disposition](REVIEW.md).
Implementation requires a fresh, restricted implementation workspace.

## What the contract means

A Live Set document stores the song's arrangement loop switch, loop start, loop
length, playback position, tempo and time signature. For one document format
version, this contract describes where those values are stored, which value text
is accepted when a document is opened, what a missing, duplicated or unknown
item does, and the text written for the values when a document is saved. It does
not describe playback, timing, editing after opening, undo, the user interface,
or how a refused document is reported.

All rules and expected results are **static-derived** from evidence reviewed
before sanitization. None is an observed reference execution. No compatibility
result is established; the original application remains the authority for a
later comparison.

## Document scope and preconditions

- The input is the decoded XML of a Live Set: well-formed XML 1.0 in UTF-8
  whose root element is `Ableton` with exactly the attributes
  `MajorVersion="5"`, `MinorVersion="12.0_12402"` and `SchemaChangeCount="1"`,
  and whose first child is `LiveSet`. Every fixture uses this envelope. The
  compressed file container, other root elements and attributes, other format
  versions and their upgrade are outside this release.
- The **text** of a value is its attribute value after standard XML
  attribute-value decoding.
- Paths are relative to `/Ableton/LiveSet`.
- **Opens** means the document is read without refusal. **Refused** means the
  document is not opened. How a refusal is reported, and what is open
  afterwards, are excluded.
- Numbers use `.` as the decimal separator. Expectations assume a host locale
  whose decimal separator is `.`; locale-dependent behavior is excluded.
- A full Live Set contains much more than the fixtures (tracks, devices, scenes,
  automation and other state). That content is outside this release. Its absence
  from a fixture must not by itself change a judged outcome.
- Expectations exist only for values in these ranges: loop start and position
  from 0 to below 1,000,000; loop length from 1 to below 1,000,000; tempo from
  20 to 999; time-signature codes from 0 to 494. The upper loop and position
  bound is a scope limit of this release, not a claim about the original.

## Selected requirement clauses

### REQ-TRANSPORT-STATE-001 — partial: value locations and types

| Value | Element (attribute `Value`) | Value type |
| --- | --- | --- |
| Arrangement loop switch | `Transport/LoopOn` | Boolean |
| Loop start | `Transport/LoopStart` | IEEE 754 binary64 |
| Loop length | `Transport/LoopLength` | IEEE 754 binary64 |
| Playback position | `Transport/CurrentTime` | IEEE 754 binary64 |
| Song tempo | `MainTrack/DeviceChain/Mixer/Tempo/Manual` | IEEE 754 binary32 |
| Time-signature code | `MainTrack/DeviceChain/Mixer/TimeSignature/Manual` | integer, see [REQ-010](#req-transport-state-010--partial-time-signature-code) |

Elements with the same names elsewhere in a document, for example in clips,
scenes, instruments and grooves, are different values. Only these paths carry
the song's transport state. The units of the loop, position and tempo values
are not part of this release.

### REQ-TRANSPORT-STATE-002 — partial: element shape and order on save

- The four `Transport` elements above and both `Manual` elements are written as
  empty elements whose only attribute is `Value`, for example
  `<LoopOn Value="false" />`.
- A saved `Transport` element contains `LoopOn`, `LoopStart`, `LoopLength` and
  `CurrentTime` exactly once each.
- The children of a saved `Transport` element appear in the following relative
  order. A child that is not written is skipped.
  1. `PhaseNudgeTempo`, `LoopOn`, `LoopStart`, `LoopLength`, `LoopIsSongStart`,
     `CurrentTime`, `PunchIn`, `PunchOut`, `MetronomeTickDuration`;
  2. the key and MIDI assignment children `DrawButtonKeyMidi`, `FollowKeyMidi`,
     `PhaseNudgeUpKeyMidi`, `PhaseNudgeDownKeyMidi`, `TapTempoKeyMidi`,
     `LoopOnKeyMidi`, `StartKeyMidi`, `StopKeyMidi`, `RecordKeyMidi`,
     `SessionRecordKeyMidi`, `PrepareSceneForNewRecordingKeyMidi`,
     `ArrangementOverdubKeyMidi`, `AutomationArmKeyMidi`,
     `BackToArrangementKeyMidi`, `ReEnableAutomationKeyMidi`, `PunshInKeyMidi`,
     `PunshOutKeyMidi`, `MetronomOnKeyMidi`, `MidiPrelistenKeyMidi`,
     `TriggerCaptureKeyMidi`, `FollowActionEnabledKeyMidi`,
     `IsTempoFollowerInControlKeyMidi`, `ResyncExternalHardwareKeyMidi`
     (`Punsh` and `Metronom` are the literal spellings);
  3. `DrawMode`.

These 33 names are the **known** `Transport` children. Whether any of the other
29 known children is written is not part of this release.

### REQ-TRANSPORT-STATE-003 — loop switch text on load

- `LoopOn` text `true` or `1` gives loop on; `false` or `0` gives loop off.
  Matching is exact and case-sensitive, with no trimming.
- Any other text is refused, including `TRUE`, `True`, the empty string and
  ` true`.

### REQ-TRANSPORT-STATE-004 — partial: loop and position number text on load

Applies to `LoopStart`, `LoopLength` and `CurrentTime`.

- Leading space characters (U+0020) are skipped. The value is then read from
  the longest prefix of the remaining text that forms a decimal number: an
  optional `+` or `-`; digits with an optional `.` and fraction digits, at least
  one digit in total; and an optional exponent of `e` or `E`, an optional sign
  and at least one digit. An exponent marker without digits is not part of the
  prefix. Text after the prefix is ignored, so `4.5abc` reads as 4.5.
- The value is the binary64 number nearest to the decimal prefix, ties to even.
- Text without such a prefix is refused, for example `abc` or the empty string.

### REQ-TRANSPORT-STATE-005 — partial: tempo text on load

`Tempo/Manual` text is read by the REQ-004 rule. The binary64 result is then
rounded to the nearest binary32 value, ties to even, which is the tempo.
`93.3333333` reads as 93.33333587646484375.

### REQ-TRANSPORT-STATE-006 — partial: time-signature code text on load

- Accepted, as a decimal integer: ASCII digits preceded by any number of spaces
  and at most one `+`, in that order, with nothing after the digits (`201`,
  ` 201`, `+201`, ` +201`); or ASCII digits followed only by spaces (`201 `).
- Refused: text that is empty or only spaces; text with any byte outside ASCII;
  text in which, after leading spaces and one leading `+`, the rest is empty,
  starts with `-` after that `+`, contains a character other than an ASCII digit
  (apart from a single leading `-` and trailing spaces), or, when the text does
  not end in a space, is longer than 63 characters.
  Examples: `201.0`, `2e2`, `0x10`, `abc`.

### REQ-TRANSPORT-STATE-007 — partial: missing values

- A missing `LoopOn`, `LoopStart`, `LoopLength` or `CurrentTime` element, or one
  without a `Value` attribute, reads as loop off, start 8, length 16 and
  position 0 respectively.
- A missing `Tempo/Manual` element, or one without a `Value` attribute, reads as
  tempo 120.
- None of these is refused.

### REQ-TRANSPORT-STATE-008 — partial: duplicated and unknown items

- Two `Transport` children with the same known name that does not end in
  `KeyMidi`, or two `Manual` children of
  `Tempo` or of `TimeSignature`, are refused. A repeated attribute makes the XML
  not well-formed, which is refused.
- A child element of `Transport` whose name is not a known child is skipped
  together with its content. The document opens, and a later save does not
  write that element.

### REQ-TRANSPORT-STATE-010 — partial: time-signature code

The code for numerator n and denominator d is `(n − 1) + 99 × log2(d)`, with n
from 1 to 99 and d in {1, 2, 4, 8, 16}. Valid codes are 0 to 494. Examples:
4/4 is 201, 6/8 is 302, 7/8 is 303, 1/1 is 0 and 99/16 is 494. This clause
defines the meaning of a stored code only. No case exercises it, because opening
a document with a code other than 201 and saving an edited time signature are
excluded below.

### REQ-TRANSPORT-STATE-011 — partial: number text on save

- Booleans are written `true` or `false`. Integers are written as plain decimal.
- Let P be 17 for the binary64 values and 9 for tempo. Positive zero is written
  `0`. For any other value x:
  1. let k be the smallest integer not below log10|x| when |x| ≥ 1, and the
     largest integer not above log10|x| when |x| < 1;
  2. write x in fixed-point notation with max(0, P − k) digits after the decimal
     point, rounded from its exact binary value to nearest, ties to even (tempo
     is first converted exactly to binary64);
  3. if the text contains `.`, remove trailing `0` characters and then a
     trailing `.`.
- Examples: 120 → `120`; 8 → `8`; 4.5 → `4.5`; tempo read from `121.2` →
  `121.199997`; tempo read from `93.3333333` → `93.3333359`; binary64 0.3 →
  `0.299999999999999989`; binary64 3.3 → `3.2999999999999998`.

## Acceptance representation and comparison

[cases.json](cases.json) lists 18 cases. Each has an input fixture, an action
(`open`, or `open-save`: open, then save without other changes) and an expected
result with these parts:

| Field | Meaning |
| --- | --- |
| `outcome` | `opens` or `refused` |
| `state` | Values read when the document opens; only listed keys are judged: `loop_on` (Boolean), `loop_start`, `loop_length`, `current_time` (binary64) and `tempo` (binary32) |
| `saved.values` | Path to exact `Value` text in the saved document. The element occurs exactly once at that path, has no child elements and has no attribute other than `Value` |
| `saved.absent` | Paths that must not occur in the saved document |
| `saved.transport_order` | When true, the saved `Transport` children obey the REQ-002 order and contain the four required children exactly once |

Numbers in `state` are JSON numbers and compare exactly as binary64 values. A
tempo is compared after its exact conversion to binary64. Saved documents are
compared as parsed XML: element names, nesting and attribute text, never bytes,
whitespace, indentation or attribute quoting. Anything a case does not list is
not judged, including other elements, automation and the presence of other
known `Transport` children. A refused case has no `state` or `saved` part.

This is a **project comparison representation**, not an API claimed to exist in
Live or a required design. A candidate adapter may translate its own result into
these labels. Each case starts from its fixture alone. Reading and writing have
no timing tolerance, cancellation step or teardown within this scope, so those
case kinds are omitted.

## Reference comparison obligation (not executed)

A later comparison against the original application needs a full Live Set per
case. The validation analyst builds it from an otherwise unchanged set of the
same format version, whose root carries the fixture's `MajorVersion`,
`MinorVersion` and `SchemaChangeCount` values, by replacing its `Transport`
element with the fixture's and each `Manual` child of `Tempo` and
`TimeSignature` with the fixture's (removing it where the fixture has none). In
that set, the tempo and time-signature automation of the main track holds a
single event equal to the fixture's `Manual` text, or `120` when the fixture's
tempo `Manual` has no value; for TS-009 the time-signature event holds `201`,
so that only `Manual` holds the refused text. Every scene has its tempo and
time-signature overrides disabled; the application uses its factory default
set, not a user template; and the host locale uses `.` as the decimal
separator. The observation channel is chosen by the validation analyst. A
channel that rounds must be compared at its rounding. None of this has been run.

## Exclusions and deferred obligations

Requirements not released: **REQ-TRANSPORT-STATE-009** (numbers outside the
ranges above, and the loop end derived on load) and **REQ-TRANSPORT-STATE-012**
(precedence between `Manual`, its automation and enabled scene values).

Inputs with **no expectation** in this release:

- loop, position or tempo text whose remainder, after leading spaces and an
  optional sign, starts with `0x` or `0X`, or with `inf` or `nan` in any letter
  case; the text `Invalid`; text starting with `#`; leading whitespace other than
  U+0020;
- values outside the ranges in the preconditions, non-finite values, the largest
  finite values and negative zero; saved values whose base-10 logarithm lies
  within 1e-12 of an integer without being an exact power of ten;
- time-signature text with spaces both before and after the digits, or with a
  `+` and trailing spaces (for example ` +201 `); text with a `-` sign; text
  longer than 63 characters that ends in a space;
- a missing `TimeSignature/Manual` element or value; a missing `Transport`,
  `Tempo`, `TimeSignature`, `Mixer`, `DeviceChain` or `MainTrack` element;
- an unknown attribute on any element this release reads; repeated unknown
  children;
- `LoopIsSongStart` with any text other than `false` (every fixture sets
  `false`); any `*KeyMidi` child in the input;
- a tempo or time-signature automation event or scene value that disagrees with
  `Manual`;
- any other envelope, format version, compressed container or document kind.

Excluded behavior: which effective tempo and time signature apply after opening;
whether a stored time-signature code other than 201 takes effect; editing after
opening, including through the user interface, remote control or MIDI; whether
the automation of tempo and time signature is written; whether any other known
`Transport` child is written; byte layout of saved documents; playback, timing,
Link and external sync; undo; the text and presentation of refusals.

Cases of the parent draft not released here: TS-010 (a code with spaces on both
sides), TS-017 to TS-019 (out-of-range values) and TS-023 (editing the time
signature after opening).

Before claiming reference compatibility, run a separately designed bounded
probe for these cases or a justified equivalent set. Pin the original and
candidate builds and fixture bytes, retain independent observations and report
mismatches. Candidate-only success proves agreement with this contract, not
with the running original.

## Fixture provenance

All fixtures are minimal XML documents independently authored for these cases.
They use public document element names and simple values and contain no shipped
file content, program code or assets. The six `Transport` children outside the
release carry fixed values (`PhaseNudgeTempo` 10, `MetronomeTickDuration` 0,
the others `false`) only to give the element its usual shape; they are not
interpreted. Expected results are newly authored static-derived behavioral data.
No public source or dependency is approved or included. Review status is
recorded in [the manifest](manifest.json) and
[the review disposition](REVIEW.md).
