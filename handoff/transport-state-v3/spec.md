# Transport state in Live Set documents — release 3

Target: Ableton Live 12 Suite 12.4.3 (2026-07-07_e3d8be4d07), macOS.
Features: FEAT-TRANSPORT with FEAT-PERSISTENCE. Parent specification identity:
SPEC-TRANSPORT-STATE revision 4. Release: transport-state-v3, which supersedes
transport-state-v2 with corrected fixtures ([README](README.md#supersession)).
Only the clauses explicitly included below are in scope. No other clause of a
listed requirement is implicitly approved. This document is self-contained.

**Status: reviewed local release.** A separate review approved the clauses
below with the clarifications recorded in [the review disposition](REVIEW.md).
Implementation requires a fresh, restricted implementation workspace.

## What the contract means

A Live Set document stores the song's arrangement loop switch, loop start, loop
length, playback position, tempo and time signature. For one document format
version, this contract describes where those values are stored, which value text
is accepted when a document is opened, what a missing, duplicated or unknown
item does, and the text written for the values when a document is saved. It does
not describe playback, timing, editing after opening, undo, the user interface,
or how a refused document is reported.

Every expected result carries one of two provenance labels:

- **Static-derived**: derived from evidence reviewed before sanitization.
- **Extracted execution**: the original program's own code that reads the value
  text was run on the case's text and, where a saved text is judged, its code
  that writes the value text was run on the value read. It ran on a Linux x86_64
  host, from the program's x86_64 build, with glibc in place of the macOS system
  libraries. The macOS arm64 build is inferred to give the same result.

Locating the value, opening the document and saving it are static-derived in
every case. The extracted-execution cases rest on four stated assumptions:

- the macOS arm64 build converts these texts and values as the x86_64 build does;
- on save, the base-10 logarithm the program computes is within 3/4 of a
  binary64 gap of the exact value wherever its last bit decides k in REQ-011,
  outside the values excluded there. TS-024 to TS-027, whose logarithms lie 0.02
  to 0.17 gaps from an integer, need only an error below 0.8 of a gap;
- the decimal reading in TS-024 to TS-028, TS-034 and TS-035 follows the
  C-standard number grammar and gives the nearest binary64 value, keeping the
  sign of `-0`, as the glibc run did;
- the fixed-point text on save is exact, rounds exact decimal ties to even and
  keeps the sign of negative zero, as the glibc run did. No case lies on a tie.

None is an observed run of the original application. No compatibility
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
- Every fixture's `LiveSet` element starts with this track list, one MIDI track
  whose session and freeze clip lists are empty:

  ```xml
  <Tracks>
    <MidiTrack Id="1">
      <Name>
        <EffectiveName Value="1-MIDI" />
        <UserName Value="" />
      </Name>
      <Color Value="15" />
      <TrackGroupId Value="-1" />
      <DeviceChain>
        <AudioOutputRouting>
          <Target Value="AudioOut/Main" />
        </AudioOutputRouting>
        <MainSequencer>
          <ClipSlotList />
        </MainSequencer>
        <FreezeSequencer>
          <ClipSlotList />
        </FreezeSequencer>
      </DeviceChain>
    </MidiTrack>
  </Tracks>
  ```

  A Live Set whose `Tracks` element is absent or holds no audio, MIDI or group
  track is not opened (static-derived). That rule, and every other rule for
  tracks, is not part of this release. The track is present only so that the
  documents can open; its values are fixed and not interpreted, and no case
  judges it.
- A full Live Set contains much more than the fixtures (more tracks, devices,
  clips, scenes, automation and other state). That content is outside this
  release. Apart from the track list above, its absence from a fixture must not
  by itself change a judged outcome.
- Expectations exist only for values in these ranges: loop start and position
  from 0 to below 1,000,000; loop length from 1 to below 1,000,000; tempo from
  20 to 999; time-signature codes from 0 to 494. Negative zero counts as zero
  for these ranges. The upper loop and position bound is a scope limit of this
  release, not a claim about the original.

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
- Text of exactly 17 characters, `#` followed by 16 hexadecimal digits (`0`–`9`,
  `A`–`F`, `a`–`f`), reads as the binary64 value with those bits, the first digit
  most significant: `#4012000000000000` reads as 4.5. Other text that starts with
  `#` has no decimal prefix and is refused.
- Text without such a prefix is refused, for example `abc`, `- 4.5` or the empty
  string. ` +4.5 ` reads as 4.5, and `-0` reads as negative zero.

### REQ-TRANSPORT-STATE-005 — partial: tempo text on load

`Tempo/Manual` text is read by the REQ-004 rule, except for the `#` form. For
tempo that form has exactly 9 characters, `#` followed by 8 hexadecimal digits, and
reads as the binary32 value with those bits: `#42f00000` reads as 120. The binary64
result of a decimal prefix is then rounded to the nearest binary32 value, ties to
even, which is the tempo. `93.3333333` reads as 93.33333587646484375.

### REQ-TRANSPORT-STATE-006 — partial: time-signature code text on load

- Split the text into its leading spaces (U+0020), at most one `+` directly after
  them, a body, and its trailing spaces (U+0020). The text is accepted as a
  decimal integer when all five conditions hold. Otherwise it is refused.
  1. Every byte is ASCII.
  2. The body is an optional `-` followed by one or more ASCII digits, at most 63
     characters in all.
  3. A `+` is not followed by `-`.
  4. There are no trailing spaces when there are leading spaces or a `+`.
  5. The value lies from −2147483648 to 2147483647.
- Accepted examples: `201`, ` 201`, `+201`, ` +201`, `201 `, `00201`, `-0`, and
  63 characters `0…0201` followed by a space.
- Refused examples: ` 201 `, ` +201 `, `+201 `, `- 201`, `+-201`, `--201`, `-`,
  `2147483648`, `201.0`, `2e2`, `0x10`, `abc`, the empty text, and `-` followed by
  63 digits.
- An accepted code outside 0 to 494 has no expectation (see the preconditions).

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
defines the meaning of a stored code only. No case exercises it, because whether
a stored code other than 201 takes effect, and saving an edited time signature,
are excluded below. TS-030 judges only that a document with code 0 opens.

### REQ-TRANSPORT-STATE-011 — partial: number text on save

- Booleans are written `true` or `false`. Integers are written as plain decimal.
- Let P be 17 for the binary64 values and 9 for tempo. Tempo is first converted
  exactly to binary64. Positive zero is written `0`, and negative zero `-0`. For
  any other value x:
  1. let L be the binary64 value nearest to log10|x|. Let k be the smallest
     integer not below L when L ≥ 0, and the largest integer not above L when
     L < 0;
  2. write x in fixed-point notation with max(0, P − k) digits after the decimal
     point, rounded from its exact binary value to nearest, ties to even;
  3. if the text contains `.`, remove trailing `0` characters and then a
     trailing `.`.
- Step 1 uses the rounded logarithm L. It gives a different k from the exact
  logarithm only when L is an integer and log10|x| is not. In that case:
  - a binary64 value just above a power of ten 10ⁿ with n ≥ 1 gets one more digit
    after the point than the exact logarithm would give;
  - a binary64 value just below 10⁻ⁿ with n ≥ 1 gets one fewer. The binary64
    value nearest to 10⁻ⁿ can itself lie below 10⁻ⁿ.

  For example, 1000.0000000000001 → `1000.00000000000011` (the exact logarithm
  would give `1000.0000000000001`) and 0.000001 → `0.00000099999999999999995`.
  Tempo values are never affected.
- Values whose log10|x| is not an integer but lies between 1/4 and 3/4 of a
  binary64 gap from one have no expectation, because the last bit of L is not
  established there ([exclusions](#exclusions-and-deferred-obligations)).
- Examples: 120 → `120`; 8 → `8`; 4.5 → `4.5`; tempo read from `121.2` →
  `121.199997`; tempo read from `93.3333333` → `93.3333359`; binary64 0.3 →
  `0.299999999999999989`; binary64 3.3 → `3.2999999999999998`;
  100.00000000000001 → `100.000000000000014`; 0.09999999999999999 →
  `0.099999999999999992`.

## Acceptance representation and comparison

[cases.json](cases.json) lists 33 cases. Each has an input fixture, an action
(`open`, or `open-save`: open, then save without other changes), an
`expectation_provenance` label (see [What the contract means](#what-the-contract-means))
and an expected result with these parts:

| Field | Meaning |
| --- | --- |
| `outcome` | `opens` or `refused` |
| `state` | Values read when the document opens; only listed keys are judged: `loop_on` (Boolean), `loop_start`, `loop_length`, `current_time` (binary64) and `tempo` (binary32) |
| `saved.values` | Path to exact `Value` text in the saved document. The element occurs exactly once at that path, has no child elements and has no attribute other than `Value` |
| `saved.absent` | Paths that must not occur in the saved document |
| `saved.transport_order` | When true, the saved `Transport` children obey the REQ-002 order and contain the four required children exactly once |

Numbers in `state` are JSON numbers and compare exactly as binary64 values. A
tempo is compared after its exact conversion to binary64. Because equality does
not distinguish negative zero, TS-028 judges the sign only through its saved
text. Saved documents are compared as parsed XML: element names, nesting and
attribute text, never bytes, whitespace, indentation or attribute quoting. Anything a case does not list is
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
tempo `Manual` has no value. For TS-009, TS-010, TS-029, TS-031 and TS-033 the
time-signature event holds `201`, so that only `Manual` holds the refused text.
Every scene has its tempo and time-signature overrides disabled; the application
uses its factory default set, not a user template; and the host locale uses `.`
as the decimal separator. The observation channel is chosen by the validation analyst. A
channel that rounds must be compared at its rounding. None of this has been run.

## Exclusions and deferred obligations

Requirements not released: **REQ-TRANSPORT-STATE-009** (numbers outside the
ranges above, and the loop end derived on load) and **REQ-TRANSPORT-STATE-012**
(precedence between `Manual`, its automation and enabled scene values).

Inputs with **no expectation** in this release:

- loop, position or tempo text whose remainder, after leading spaces and an
  optional sign, starts with `0x` or `0X`, or with `inf` or `nan` in any letter
  case; the text `Invalid`; leading whitespace other than U+0020;
- values outside the ranges in the preconditions, non-finite values and the
  largest finite values;
- saved binary64 values x whose log10|x| is not an integer but lies, from the
  nearest integer n, between 1/4 and 3/4 of the gap between n and the adjacent
  binary64 value on the side of log10|x|; the last bit of L is not established
  there;
- accepted time-signature codes outside 0 to 494;
- a missing `TimeSignature/Manual` element or value; a missing `Transport`,
  `Tempo`, `TimeSignature`, `Mixer`, `DeviceChain` or `MainTrack` element;
- a `Tracks` element that is absent or holds no `AudioTrack` or `MidiTrack`;
  track content other than the fixtures' one MIDI track;
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

Cases of the parent draft not released here: TS-017 to TS-019 (out-of-range
values) and TS-023 (withdrawn: editing the time signature after opening).

Before claiming reference compatibility, run a separately designed bounded
probe for these cases or a justified equivalent set. Pin the original and
candidate builds and fixture bytes, retain independent observations and report
mismatches. Candidate-only success proves agreement with this contract, not
with the running original.

## Fixture provenance

All 33 fixtures are minimal XML documents independently authored for these
cases. Each is the transport-state-v2 fixture of the same name with the track
list of [the preconditions](#document-scope-and-preconditions) inserted directly
after the `<LiveSet>` start tag; no other line differs. They use public document
element names and simple values and contain no shipped file content, program
code or assets. The six `Transport` children outside the release carry fixed
values (`PhaseNudgeTempo` 10, `MetronomeTickDuration` 0, the others `false`)
only to give the element its usual shape; they are not interpreted. The same
holds for the track's values (Id 1, name `1-MIDI`, colour 15, no group, output
to the main track). Expected results are newly authored behavioral data, labeled
per case as static-derived or extracted execution. No public source or
dependency is approved or included. Review status is recorded in
[the manifest](manifest.json) and [the review disposition](REVIEW.md).
