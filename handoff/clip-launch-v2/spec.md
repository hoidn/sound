# Clip launch settings in Live Set documents, release 2

Target: Ableton Live 12 Suite 12.4.3 (2026-07-07_e3d8be4d07), macOS, Apple
silicon (arm64). Features: FEAT-SESSION with FEAT-PERSISTENCE and
FEAT-TRANSPORT. Parent specification identity: SPEC-CLIP-LAUNCH revision 4.
Release: clip-launch-v2, which supersedes clip-launch-v1
([README](README.md#supersession)). Only the clauses explicitly included below
are in scope. No other clause of a listed requirement is implicitly approved.
This document is self-contained.

**Status: reviewed local release.** A separate review approved the clauses
below with the narrowing recorded in [the review disposition](REVIEW.md).
Implementation requires a fresh, restricted implementation workspace.

## What the contract means

A Live Set stores launch settings for each clip: launch mode, launch
quantization, legato, velocity amount and a follow action. For the whole set it
stores a global launch quantization and a record quantization. For the decoded
XML of a Live Set, this contract describes:

- where these values are stored and what type each value has;
- what each stored value means and how it is labeled;
- which value text is accepted or refused when a document is opened, and the
  effect of a missing or repeated item;
- two corrections made when a document is opened, follow-chance rescaling and
  follow-time rounding;
- how follow actions in documents of two older format versions are converted;
- what form and values these items have when the document is saved.

It also states four **value functions**, as a value contract
(REQ-CLIP-LAUNCH-015 to 018): the grid length a quantization value stands for
in a given time signature, the grid that a clip's stored setting denotes, a
beat rounded to the beat lattice, and the grid boundary at or after a beat.
They are functions of explicit inputs and nothing more. They are not launch
timing: this release does not say which inputs a launch supplies, whether or
how a launch uses the results, or at which beat or sample a launched clip
starts.

It does not describe launching. That includes when a launched clip starts, the
sample at which a launch takes effect, which beat, anchor and grid a launch
uses at run time, launches with the transport stopped, and what launch modes,
legato, velocity amount and follow actions do during playback. Launch timing
belongs to a separate playback release (SPEC-PLAYBACK-CORE), which is not part
of this package. This contract also does not describe the user interface,
editing after opening, the scripting interface, undo, or how a refused document
is reported.

Every expected result carries one of two provenance labels:

- **Static-derived**: derived for the target build, without running it, from
  evidence reviewed before sanitization.
- **Extracted execution**: the original program's own code for the computation
  was run on the case's inputs: the follow-chance correction with its limit,
  the follow-time rounding, the grid length, the reading of a stored launch
  quantization value, the beat rounding and the boundary. It ran on a Linux
  x86_64 host, from the program's x86_64 build; these computations call no
  system library. The macOS arm64 build is inferred to give the same results.

In every case, reading the value text, locating the values, opening and saving
the document are static-derived. In the value cases, the selection of a clip's
grid (REQ-CLIP-LAUNCH-016) and the boundary with no grid (REQ-CLIP-LAUNCH-018)
are static-derived; [cases.json](cases.json) names the basis of each computed
result. In the both-zero branch of REQ-CLIP-LAUNCH-012 the change of
`FollowActionEnabled` is static-derived.

None of these is an observed execution of the original application, and none
was run against a candidate. No compatibility result is established. The
original application remains the authority for a later comparison. Some
derived steps rest on behavior that was not traced to the end:

- an item absent from a clip or a follow action keeps the value that a new
  clip or follow action starts with; a value that is present and inside the
  ranges of the preconditions is kept as read, apart from the opening
  corrections; a follow chance outside 0 to 100 is kept as read until the
  follow-chance correction;
- the opening corrections run for every clip read from a document, after any
  conversion;
- before an older document's values are read, it is converted by every
  conversion step whose number is above the suffix number of its MinorVersion,
  in increasing order;
- the macOS arm64 build computes the extracted-execution values as the x86_64
  build does;
- converting the other content of a fixture (tracks, mixers, notes, the sample
  reference and scenes) from `12.0_12117` or `11.0_405` does not refuse the
  document.

The [reference comparison obligation](#reference-comparison-obligation-not-executed)
covers them.

## Document scope and preconditions

- The input is the decoded XML of a Live Set: well-formed XML 1.0 in UTF-8. Its
  root element is `Ableton` with exactly the attributes `MajorVersion="5"` and
  `SchemaChangeCount="1"` and a `MinorVersion` of `12.0_12402`, `12.0_12117`
  or `11.0_405`. Its first child is `LiveSet`. The compressed file container,
  other envelopes and other format versions are outside this release.
- A MinorVersion has the form `<a>.<b>_<c>`; c is its **suffix number** (12402,
  12117 or 405 here).
- The **text** of a value is its attribute value after standard XML
  attribute-value decoding.
- Paths are relative to `/Ableton/LiveSet`. `X[1]` is the first child element
  named `X`. These locations are named:

| Name | Path |
| --- | --- |
| session MIDI clip | `Tracks/MidiTrack[1]/DeviceChain/MainSequencer/ClipSlotList/ClipSlot[1]/ClipSlot/Value/MidiClip` |
| session audio clip | `Tracks/AudioTrack[1]/DeviceChain/MainSequencer/ClipSlotList/ClipSlot[1]/ClipSlot/Value/AudioClip` |
| arrangement MIDI clip | `Tracks/MidiTrack[1]/DeviceChain/MainSequencer/ClipTimeable/ArrangerAutomation/Events/MidiClip[1]` |
| first scene | `Scenes/Scene[1]` |

- **Opens** means the document is read without refusal. **Refused** means the
  document is not opened. How a refusal is reported, and what is open
  afterwards, are excluded.
- Numbers use `.` as the decimal separator. Expectations assume a host locale
  whose decimal separator is `.`; locale-dependent behavior is excluded.
- Every fixture is a **complete minimal Live Set** ([Fixture provenance](#fixture-provenance)).
  Besides the launch values it holds the tracks, mixers, session and freeze
  clip slots, scenes, clip content, a sample reference and the other structure
  that opening a Live Set requires. That content is there so that the set
  opens. It is not judged and is outside this release. A case that expects a
  refusal changes exactly one item, and that item is the only reason for the
  refusal.
- The audio clip of every fixture references the sample
  `fixtures/Samples/T11-tone.wav` by a path relative to the set. Open a fixture
  from the `fixtures` folder, or copy it together with that `Samples` folder.
- Every clip in an input has `LaunchMode` and `LaunchQuantisation`, and
  `LiveSet` has `GlobalQuantisation` and `AutoQuantisation`.
- Expectations exist only for values in these ranges:

| Item | Range |
| --- | --- |
| `GlobalQuantisation` | 0 to 13 |
| `AutoQuantisation` | 0 to 8 |
| `VelocityAmount` | 0 to 1 |
| `FollowChanceA`, `FollowChanceB` | both 0 to 100; or both −100 to 200 with \|A + B\| ≥ 1, the sum taken in binary32 arithmetic |
| `JumpIndexA`, `JumpIndexB` | −1 to 8,388,608 |
| `LoopIterations` | 1 to 1,073,741,823 |
| `FollowTime` | 0 to below 1,000,000 |
| `LaunchMode`, `LaunchQuantisation`, `FollowActionA`, `FollowActionB` | the values of REQ-CLIP-LAUNCH-004, 005 and 007; other values only as REQ-CLIP-LAUNCH-011 states |

- Negative zero has an expectation only as a follow chance (REQ-CLIP-LAUNCH-012).

## Stored items and value types

Each item is an element whose attribute `Value` holds the value text, except
`FollowAction`, which is an element holding other items.

| Item | Parent | Value type |
| --- | --- | --- |
| `LaunchMode` | clip | integer (REQ-CLIP-LAUNCH-004) |
| `LaunchQuantisation` | clip | integer (REQ-CLIP-LAUNCH-005) |
| `Legato` | clip | Boolean |
| `VelocityAmount` | clip | IEEE 754 binary32 |
| `FollowAction` | clip or scene | holds the ten items below |
| `FollowTime` | `FollowAction` | IEEE 754 binary64 |
| `IsLinked` | `FollowAction` | Boolean |
| `LoopIterations` | `FollowAction` | integer |
| `FollowActionA`, `FollowActionB` | `FollowAction` | integer (REQ-CLIP-LAUNCH-007) |
| `FollowChanceA`, `FollowChanceB` | `FollowAction` | IEEE 754 binary32 |
| `JumpIndexA`, `JumpIndexB` | `FollowAction` | IEEE 754 binary32 |
| `FollowActionEnabled` | `FollowAction` | Boolean |
| `GlobalQuantisation` | `LiveSet` | integer (REQ-CLIP-LAUNCH-005) |
| `AutoQuantisation` | `LiveSet` | integer (REQ-CLIP-LAUNCH-006) |

In this release a **clip** is an element at one of the three named clip
locations. `LaunchMode`, `LaunchQuantisation`, `Legato`, `VelocityAmount` and
`FollowAction` are its **launch elements**.

## Reading rules for value text

**Boolean.** `true` or `1` gives on (true); `false` or `0` gives off (false).
Matching is exact and case-sensitive, with no trimming. Any other text is
refused, including `TRUE`, `True`, `yes`, the empty string and ` true`.

**Integer.**

- Accepted as a decimal integer: one to nine ASCII digits, preceded by any
  number of U+0020 spaces and at most one `+`, in that order, with nothing
  after the digits (`5`, ` 5`, `+5`, ` +5`); or ASCII digits followed only by
  spaces (`5 `).
- Refused: text that is empty or only spaces; text with any byte outside ASCII;
  text in which, after leading spaces and one leading `+`, the rest is empty,
  starts with `-` after that `+`, or contains a character other than an ASCII
  digit (apart from a single leading `-` and trailing spaces); and text longer
  than 63 characters that does not end in a space. Examples: `2.0`, `2e0`,
  `0x2`, `abc`.

**binary64.**

- Leading space characters (U+0020) are skipped. The value is then read from
  the longest prefix of the remaining text that forms a decimal number: an
  optional `+` or `-`; digits with an optional `.` and fraction digits, at
  least one digit in total; and an optional exponent of `e` or `E`, an optional
  sign and at least one digit. An exponent marker without digits is not part
  of the prefix. Text after the prefix is ignored, so `4.5abc` reads as 4.5.
- The value is the binary64 number nearest to the decimal prefix, ties to
  even.
- Text without such a prefix is refused, for example `abc` or the empty string.

**binary32.** The text is read by the binary64 rule. The result is then rounded
to the nearest binary32 value, ties to even. `0.3` reads as
0.300000011920928955078125.

Text that these rules refuse, in any item of the table above that a document
contains, refuses the document.

## Selected requirement clauses

### REQ-CLIP-LAUNCH-001 — partial: clip launch elements

1. A clip at each named clip location (session MIDI clip, session audio clip,
   arrangement MIDI clip) stores its launch settings in its launch elements,
   which are direct children of the clip element, with the types above.
2. `Legato` and `VelocityAmount` also name items elsewhere, for example in
   instrument envelopes and in grooves. Elements with these names that are not
   direct children of a clip are different values.
3. Values are read with the reading rules above. Refused text refuses the
   document.
4. Two direct children of one clip with the same launch-element name refuse
   the document.
5. On save, each launch element of a clip is written once as a direct child of
   the clip element. `LaunchMode`, `LaunchQuantisation`, `Legato` and
   `VelocityAmount` are written as empty elements whose only attribute is
   `Value`. `FollowAction` is written as REQ-CLIP-LAUNCH-002 states. Among the
   clip's children the five appear in the relative order `LaunchMode`,
   `LaunchQuantisation`, `Legato`, `VelocityAmount`, `FollowAction`. Other
   children of the clip may lie between them.
6. A written Boolean, or a written number whose value has at most six
   significant decimal digits, read back with the reading rules above, gives
   the value held. For other numbers this is not part of this release, and
   neither is the exact text written for numbers and Booleans.

### REQ-CLIP-LAUNCH-002 — partial: follow-action element

1. A clip's `FollowAction` holds the ten items of the table above. Each has a
   `Value` attribute and is read with the reading rules.
2. On save, a clip's `FollowAction` is written with exactly these ten
   children, in the order `FollowTime`, `IsLinked`, `LoopIterations`,
   `FollowActionA`, `FollowActionB`, `FollowChanceA`, `FollowChanceB`,
   `JumpIndexA`, `JumpIndexB`, `FollowActionEnabled`. Each is an empty element
   whose only attribute is `Value`, and its value reads back as in
   REQ-CLIP-LAUNCH-001.
3. A scene holds a `FollowAction` of the same form. Scenes are in this release
   only for their conversion (REQ-CLIP-LAUNCH-014).

### REQ-CLIP-LAUNCH-003 — partial: set quantization items

`LiveSet` holds the global launch quantization in `GlobalQuantisation` and the
record quantization in `AutoQuantisation`, both integers read with the integer
rule. Refused text refuses the document. What is written for them on save is
not part of this release.

### REQ-CLIP-LAUNCH-004 — launch mode values

`LaunchMode`: 0 Trigger, 1 Gate, 2 Toggle, 3 Repeat.

### REQ-CLIP-LAUNCH-005 — partial: launch quantization values

| Clip `LaunchQuantisation` | `GlobalQuantisation` | Label |
| --- | --- | --- |
| 0 | — | Global |
| 1 | 0 | None |
| 2 | 1 | 8 Bars |
| 3 | 2 | 4 Bars |
| 4 | 3 | 2 Bars |
| 5 | 4 | 1 Bar |
| 6 | 5 | 1/2 |
| 7 | 6 | 1/2T |
| 8 | 7 | 1/4 |
| 9 | 8 | 1/4T |
| 10 | 9 | 1/8 |
| 11 | 10 | 1/8T |
| 12 | 11 | 1/16 |
| 13 | 12 | 1/16T |
| 14 | 13 | 1/32 |

A clip value k from 1 to 14 denotes the same setting as global value k − 1,
with the same label. Clip value 0 (Global) denotes the set's global setting.
The grid length a setting stands for is REQ-CLIP-LAUNCH-015 and 016. Which
setting, time signature and grid a launch uses is excluded.

### REQ-CLIP-LAUNCH-006 — partial: record quantization values

`AutoQuantisation`: 0 None, 1 1/4, 2 1/8, 3 1/8T, 4 1/8 + 1/8T, 5 1/16,
6 1/16T, 7 1/16 + 1/16T, 8 1/32. Its effect on recording is excluded.

### REQ-CLIP-LAUNCH-007 — partial: follow-action values

`FollowActionA` and `FollowActionB`: 0 No Action, 1 Stop, 2 Play Again,
3 Previous, 4 Next, 5 First, 6 Last, 7 Any, 8 Other, 9 Jump. A short form of
the labels differs only in "Again" for 2.

Labels in REQ-CLIP-LAUNCH-004 to 007 identify the meaning of each value. No
case grades displayed text.

### REQ-CLIP-LAUNCH-009 — partial: initial values and missing clip items

1. A new clip starts with `Legato` off and `VelocityAmount` 0. A new follow
   action starts with `FollowTime` 4, `IsLinked` on, `LoopIterations` 1,
   `FollowActionA` 4 (Next), `FollowActionB` 0 (No Action), `FollowChanceA`
   100, `FollowChanceB` 0, `JumpIndexA` and `JumpIndexB` 1, and
   `FollowActionEnabled` off.
2. A clip without `Legato`, `VelocityAmount` or `FollowAction`, or whose
   `FollowAction` lacks some of its ten items, opens with these values for the
   missing items. The opening corrections then apply. A later save writes the
   missing items with these values.

### REQ-CLIP-LAUNCH-011 — partial: out-of-range values

1. A `LaunchMode`, `LaunchQuantisation`, `FollowActionA` or `FollowActionB`
   value outside the values of REQ-CLIP-LAUNCH-004, 005 and 007 does not
   refuse the document when its text is an accepted integer. The value then
   held, displayed or written, and any effect on launching, are excluded.
2. A follow chance outside 0 to 100, inside the ranges of the preconditions,
   does not refuse the document. It is rescaled and limited by
   REQ-CLIP-LAUNCH-012.
3. In the value function of REQ-CLIP-LAUNCH-016, a clip value of −99 counts as
   0 (Global).

### REQ-CLIP-LAUNCH-012 — partial: follow-chance rescaling on opening

After a clip's follow action is read, let A and B be its `FollowChanceA` and
`FollowChanceB` values (binary32):

1. If A = 0 and B = 0, `FollowChanceA` becomes 100, `FollowChanceB` stays 0 and
   `FollowActionEnabled` becomes off. Negative zero counts as zero here.
2. Otherwise, with every operation in binary32 arithmetic rounded to nearest,
   ties to even: s = (A + B) ÷ 100 and q = A ÷ s. Let a be q rounded to an
   integer, with halves rounded away from zero, and b = 100 − a.
   `FollowChanceA` becomes a and `FollowChanceB` becomes b, each limited to 0
   to 100: a value below 0 becomes 0 and a value above 100 becomes 100.
   `FollowActionEnabled` is unchanged.

Examples: 30 and 30 give 50 and 50 (q is 49.999996); 1 and 2 give 33 and 67;
1 and 7 give 13 and 87 (q is exactly 12.5); 3 and 5 give 38 and 62 (q is
37.5); 5 and 3 give 63 and 37; 1 and 199 give 1 and 99 (q is 0.5); 0 and 50
give 0 and 100; 0.25 and 0.75 give 25 and 75; 99.5 and 0.5 give 100 and 0;
100 and 0 are unchanged. Outside 0 to 100: 150 and 50 give 75 and 25; −10 and
50 give 0 and 100 (a is −25 and b is 125 before the limit); 150 and −50 give
100 and 0; −10 and −10 give 50 and 50.

### REQ-CLIP-LAUNCH-013 — partial: follow-time rounding on opening

After a clip's follow action is read, its `FollowTime` x (0 ≤ x < 1,000,000)
becomes L(x), computed in binary64 arithmetic with every operation rounded to
nearest, ties to even. With h the binary64 value nearest to 1/3,843,840:

1. t₁ = x + h × 0.5;
2. t₂ = t₁ × 3,843,840;
3. m = ⌊t₂⌋, the largest integer not above t₂;
4. L(x) = m ÷ 3,843,840.

3,843,840 is 2⁸·3·5·7·11·13. When x is more than 10⁻⁹ from every point
halfway between two multiples of 1/3,843,840, L(x) is the binary64 value
nearest to the multiple nearest to x; this is the rule of clip-launch-v1, which
gave no expectation within 10⁻⁹ of such a point. Nearer to a halfway point the
formula decides: 1.3007825507825505e-07, one binary64 step below the binary64
value nearest to h ÷ 2, gives h (2.6015651015651016e-07), where exact rounding
gives 0. Examples: 2.0000001 gives 2; 3.0000002 gives 11,531,521 ÷ 3,843,840
(about 3.00000026); 1e-8 gives 0; 1.3333333 gives 4/3;
3.902347652347652e-07 gives 5.203130203130203e-07;
100000.00000143086 gives 100000.00000156094.

### REQ-CLIP-LAUNCH-014 — partial: conversion of older documents

1. Opening a document whose MinorVersion has suffix number c converts it,
   before its values are read, by each conversion step below whose number is
   above c, in increasing order. The reading rules, the initial values of
   REQ-CLIP-LAUNCH-009 and the corrections of REQ-CLIP-LAUNCH-012 and 013 then
   apply to the converted document. Conditions below compare values read with
   the reading rules.

| Step | Applies to | Effect |
| --- | --- | --- |
| 406 | each clip | The clip's direct children `FollowTime`, `FollowActionA`, `FollowActionB`, `FollowChanceA` and `FollowChanceB` move, with their values, into a new `FollowAction` child of the clip. A missing `FollowTime` becomes 1 |
| 417 | each follow action without `FollowActionEnabled` | `FollowActionEnabled` is added: on when (A ≠ 0 and `FollowChanceA` ≠ 0) or (B ≠ 0 and `FollowChanceB` ≠ 0), where A and B are `FollowActionA` and `FollowActionB`; off otherwise |
| 421 | each follow action | `IsLinked` is added: on, with `FollowActionA` set to 4 (Next), when `FollowActionEnabled` is off, A = 0, B = 0 and `FollowTime` = 4; off otherwise |
| 12203 | each scene | A scene without `FollowAction` gets one with `FollowTime` 4, `LoopIterations` 1, A 0, B 0, chances 100 and 0, `FollowActionEnabled` off, jump indices 1 and `IsLinked` on. In a scene with `FollowAction`, `IsLinked` becomes on when `FollowActionEnabled` is off, `FollowTime` = 4, A = 4, B = 0, `FollowChanceA` = 100 and `FollowChanceB` = 0, and off otherwise, replacing any earlier `IsLinked` |

2. Hence, of these steps, a `11.0_405` document passes through 406, 417, 421
   and 12203; a `12.0_12117` document through 12203 only; a `12.0_12402`
   document through none. Older documents also pass through other conversion
   steps. Those are excluded, and none of them changes an item that this
   release describes.
3. Items still missing after conversion, such as `LoopIterations` and the jump
   indices of a converted clip, take the initial values of
   REQ-CLIP-LAUNCH-009.
4. Example: a `11.0_405` clip with follow time 4, actions 0 and 0 and chances
   1 and 0 opens with `FollowTime` 4, `IsLinked` on, `FollowActionA` 4,
   `FollowActionB` 0, chances 100 and 0 and `FollowActionEnabled` off.

## Quantization grid values (value contract)

REQ-CLIP-LAUNCH-015 to 018 define values as functions of explicit arguments.
In a Live Set the arguments correspond to these quantities:

- q: a value on the scale of `GlobalQuantisation` (REQ-CLIP-LAUNCH-005);
- clip value: a value on the scale of a clip's `LaunchQuantisation`; global
  value: a value on the scale of the set's `GlobalQuantisation`;
- the clip's time signature: the clip's own time signature, stored in the
  clip's `TimeSignature` element; the song's time signature;
- beat: a position in beats (quarter notes); grid: a grid length in
  beats; anchor: a beat from which grid lines are counted.

How these arguments are obtained when a clip is launched, including which
global value and which clip and song time signatures a launch uses and how
they are read, and whether and how a launch uses the results, are not part of
this release. In particular, the boundary B is not stated to be the beat at
which a launched clip starts or takes effect; that belongs to a separate
playback release. Every result is a binary64 number. A grid of 0 means no
grid.

### REQ-CLIP-LAUNCH-015 — grid length

For an integer q with |q| < 1,000,000 and a time signature n/d with n from 1
to 99 and d one of 1, 2, 4, 8 and 16, let bar = 4 × n ÷ d beats (exact for
these signatures). The grid length G(q, n/d) is:

| q | Setting | G (beats) |
| --- | --- | --- |
| 1 | 8 Bars | 8 × bar |
| 2 | 4 Bars | 4 × bar |
| 3 | 2 Bars | 2 × bar |
| 4 | 1 Bar | bar |
| 5 | 1/2 | 2 |
| 6 | 1/2T | the binary64 value nearest 4/3 |
| 7 | 1/4 | 1 |
| 8 | 1/4T | the binary64 value nearest 2/3 |
| 9 | 1/8 | 0.5 |
| 10 | 1/8T | the binary64 value nearest 1/3 |
| 11 | 1/16 | 0.25 |
| 12 | 1/16T | the binary64 value nearest 1/6 |
| 13 | 1/32 | 0.125 |
| any other | None or out of range | 0 (no grid) |

The note settings (5 to 13) do not depend on the time signature: 1/2 is 2
beats in 6/8. Examples: 1 Bar is 3 beats in 3/4 and 6/8 and 3.5 beats in 7/8;
8 Bars is 198 beats in 99/16.

### REQ-CLIP-LAUNCH-016 — partial: the grid a clip's setting denotes

Given a clip value k (|k| < 1,000,000), a global value Q from 0 to 13, the
clip's time signature n_c/d_c and the song's time signature n_s/d_s (each as in
REQ-CLIP-LAUNCH-015):

1. A clip value of −99 counts as 0. Every other clip value counts as itself.
2. If the clip value counts as 0 (Global), the grid is G(Q, n_s/d_s): the
   global value in the song's time signature.
3. Otherwise the grid is G(k − 1, n_c/d_c): the clip's own setting in the
   clip's own time signature. So clip value 1 (None), clip values of 15 or
   more, and negative clip values other than −99 give no grid.

Examples: clip value 5 (1 Bar) in a clip in 6/8 gives 3, whatever the song's
time signature; clip value 0 in a clip in 6/8 with global value 4 in a 4/4 song
gives 4; clip value 8 (1/4) gives 1 whatever the global value.

These clauses state what a stored setting denotes for the given arguments.
That a launch uses the set's stored `GlobalQuantisation`, the song's time
signature at some moment or the clip's time signature is not part of this
release.

### REQ-CLIP-LAUNCH-017 — partial: beat rounding and boundary

Given a beat t (0 ≤ t < 1,000,000), a grid g > 0 that is a grid length of
REQ-CLIP-LAUNCH-015 and an anchor a with a > −1,000,000 and max(0, a) ≤ L(t),
where L is the rounding of REQ-CLIP-LAUNCH-013:

1. The **rounded beat** is p = L(t). Examples: 3.99 gives 3.990000104062604;
   4 − 10⁻⁹ and 4 + 10⁻⁹ give 4; 0.13 gives 0.12999994796869796; 4 plus one
   lattice step (4.000000260156511) is kept.
2. With a′ = max(0, a), the **boundary** is
   B = L(a′ + ⌈(p − a′) ÷ g⌉ × g), every operation in binary64 arithmetic
   rounded to nearest, ties to even; ⌈y⌉ is the smallest integer not below y.
   A negative anchor therefore counts as 0.
3. Examples with anchor 0: 1 Bar in 4/4 (g = 4) and t = 5.3 give 8; t = 4
   gives 4; t = 3.99 gives 4; t = 4.000000260156511 gives 8. With g = 1/3 and
   t = 0.4, B is the binary64 value nearest 2/3. With anchor 8, g = 3 and t =
   9, B is 11.
4. For the triplet grids (the binary64 values nearest 4/3, 2/3, 1/3 and 1/6),
   B is not always p when p lies exactly on a grid line: (p − a′) ÷ g can
   exceed the whole number of lines by one rounding step, and B is then the
   next line. With g nearest 2/3 and t the binary64 value nearest 10/3, B is 4;
   with g nearest 2/3 and t nearest 4/3, B is p.
5. For the grid lengths of q = 5 to 13 with anchor 0, a beat one lattice step
   (1/3,843,840) before or after any of their grid lines up to beat 64 gives
   the first line at or after the beat.

### REQ-CLIP-LAUNCH-018 — partial: boundary with no grid

With g = 0 (no grid) and t as in REQ-CLIP-LAUNCH-017, the boundary is the
rounded beat: B = p = L(t). The anchor plays no part.

## Acceptance representation and comparison

[cases.json](cases.json) lists 100 cases: 62 document cases, 50 of them
carried from clip-launch-v1, and 38 value cases. Each case has an
`expectation_provenance` label ([What the contract means](#what-the-contract-means)).

A **document case** has an input fixture, an action (`open`, or `open-save`:
open, then save without other changes) and an expected result with these
parts:

| Field | Meaning |
| --- | --- |
| `outcome` | `opens` or `refused` |
| `values` | Path to the value held after the document has opened. Only listed paths are judged |
| `saved.values` | Path to a value. In the saved document the element occurs exactly once at that path, has no child elements and has no attribute other than `Value`, and its `Value` text read with the reading rules gives this value |
| `saved.absent` | Paths that must not occur in the saved document |
| `saved.clip_order` | A clip path. In the saved document that clip's five launch elements each occur once in the relative order of REQ-CLIP-LAUNCH-001, and its `FollowAction` has exactly the ten children of REQ-CLIP-LAUNCH-002 in that order |

`saved.values` lists only Booleans and numbers with at most six significant
decimal digits (REQ-CLIP-LAUNCH-001 clause 6).

The value type of a path is the type of its last element name in the item
table. Booleans are JSON `true` and `false`; integers and binary64 values are
JSON numbers that compare exactly; binary32 values are compared after their
exact conversion to binary64. Equality does not distinguish negative zero.
Saved documents are compared as parsed XML: element names, nesting and
attribute text, never bytes, whitespace, indentation or attribute quoting.
Anything a case does not list is not judged, including other children of a
clip, the other content of the fixture, the saved envelope and every set-level
or scene item in a saved document. A refused case has no `values` or `saved`
part.

A **value case** has no input fixture and the action `compute`. Its expected
result is a list of computations, each with a `function`, its `arguments`, the
expected `result` and the `basis` of that result:

| Function | Arguments | Result |
| --- | --- | --- |
| `grid-length` | `q`, `time_signature` [n, d] | `grid`: G(q, n/d) of REQ-CLIP-LAUNCH-015 |
| `clip-grid` | `clip_value`, `global_value`, `clip_time_signature` [n, d], `song_time_signature` [n, d] | `grid` of REQ-CLIP-LAUNCH-016 |
| `grid-boundary` | `beat`, `grid`, `anchor` | `rounded_beat` p and `boundary` B of REQ-CLIP-LAUNCH-017 and 018 |

Each computation is judged alone, from its arguments. Where a case chains two
computations, the later one's `grid` argument repeats the earlier result.
Results are JSON numbers compared exactly as binary64 values.

This is a **project comparison representation**, not an API claimed to exist
in Live and not a required design. A candidate adapter may translate its own
result into these labels. Each case starts from its fixture alone, or from its
arguments alone. Reading, writing and computing have no timing tolerance,
cancellation step or teardown in this scope, so those case kinds are omitted.

## Reference comparison obligation (not executed)

**Document cases.** Each fixture is a complete Live Set. A comparison against
the original application opens it as it is, from the `fixtures` folder with its
`Samples` folder, either as plain XML or encoded in the target's usual Live Set
container. For `11.0_405`, the fixtures are authored in that format version's
form; an authentic set saved by an earlier Live version that writes that
version is still needed to confirm the conversion of its launch elements and of
its other content. None is included, and none ships with the target. The
target's factory default set is saved at `12.0_12117` and can serve to confirm
that version's form. A value must be observed for the clip or scene at the
named location. The observation channel is chosen by the validation analyst;
a channel that rounds must be compared at its rounding. Notices shown when an
older document is opened or saved are not compared.

**Value cases.** The original application shows these values only through
launch timing, which a separate playback release will specify and compare.
A value case is not a launch case, and agreement with the value cases shows
nothing about launching. Their expectations come from the original program's
own code, run on the case's arguments, and are otherwise static-derived, not
taken from a run of the application.

None of this has been run.

## Exclusions and deferred obligations

Requirements not released: **REQ-CLIP-LAUNCH-008** (initial set values, and a
set without `GlobalQuantisation` or `AutoQuantisation`),
**REQ-CLIP-LAUNCH-010** (the initial launch mode and launch quantization of a
new clip, and a clip without `LaunchMode` or `LaunchQuantisation`) and
**REQ-CLIP-LAUNCH-019 to 023** (launching with the transport stopped, Gate,
Toggle and Repeat, Legato, velocity amount and follow-action execution).
REQ-CLIP-LAUNCH-015 to 018 are released only as the value functions above.

Inputs with **no expectation** in this release:

- a clip without `LaunchMode` or `LaunchQuantisation`; a `LiveSet` without
  `GlobalQuantisation` or `AutoQuantisation`;
- an item of the item table without a `Value` attribute, with another
  attribute or with child elements;
- values outside the ranges in the preconditions, apart from the
  REQ-CLIP-LAUNCH-011 clause on launch mode, launch quantization and follow
  action values; non-finite values; negative zero, except as a follow chance;
- number text whose remainder, after leading spaces and an optional sign,
  starts with `0x` or `0X`, or with `inf` or `nan` in any letter case; the text
  `Invalid`; text starting with `#`; leading whitespace other than U+0020;
- integer text with spaces both before and after the digits, with a `+` and
  trailing spaces, with a `-` sign, or with ten or more digits within 63
  characters;
- repeated or unknown children of `FollowAction`; unknown children or
  attributes of a clip element;
- clips other than at the named locations, including clips in take lanes and
  the groove pool, and more than one clip at a named location;
- in `11.0_405` documents: a clip that already has `FollowAction`; a clip
  without `FollowActionA`, `FollowActionB`, `FollowChanceA` or
  `FollowChanceB`, or with a `FollowActionEnabled` or `IsLinked` child;
  scenes other than in the fixtures' form (an item of the old scene list
  `SceneNames` holding only its name);
- in `12.0_12117` documents: a scene `FollowAction` without all ten items;
- a Live Set that lacks the structure a set needs to open, and documents that
  break more than one refusal rule;
- any other envelope, format version, compressed container or document kind;
- value-function arguments outside the ranges stated in REQ-CLIP-LAUNCH-015 to
  018.

Excluded behavior:

- launch timing: when a launched clip starts, the sample at which a launch
  takes effect, which beat, anchor, global value, time signatures and grid a
  launch uses at run time, whether a launch starts at the boundary of
  REQ-CLIP-LAUNCH-017, any delay before the boundary and any move to the next
  grid line, launches with the transport stopped, and the anchor after a
  time-signature change;
- Gate, Toggle and Repeat press and release behavior, Legato, velocity scaling,
  follow-action timing, loop iterations, jump indices and chance selection;
- displayed text, including whether the user interface shows exactly the
  labels above and where each form of the follow-action labels is shown;
- the value held, displayed or written for an out-of-range launch mode,
  launch quantization or follow action; for a follow time outside 0 to below
  1,000,000, whether the document opens and the value then held;
- the text written for numbers and Booleans, and whether a written number with
  more than six significant digits reads back exactly; layout and indentation;
  the save container and envelope; what is written for set-level items and
  scenes;
- the initial launch mode and launch quantization of a new clip and the
  related preferences; initial set values; File > New; recording, drawing or
  dropping a clip;
- conversion steps other than 406, 417, 421 and 12203, the conversion of a
  clip that has both forms, documents older than `11.0_405`, and the
  conversion of the fixtures' other content;
- reading the clip and song time signatures, and clips with several
  time-signature entries;
- the scripting interface (Live API): names, properties and assignment of
  values;
- the effect of record quantization; scene follow actions other than their
  conversion; the key and MIDI assignment of the global quantization;
- the fixtures' other content (tracks, mixers, notes, the sample, automation
  and scenes): it is not judged;
- editing after opening, undo, and the text and presentation of refusals.

Cases of the parent draft not released here: its cases for a clip without
`LaunchMode` and `LaunchQuantisation`, for the scripting interface, for a set
without `GlobalQuantisation` and `AutoQuantisation`, for a follow time below 0,
for the anchor after a time-signature change and for a launch with the
transport stopped. Its launch-timing cases are not released. Some value cases
use the same beats and grids as arguments; they state the value functions
only, not when or at which sample a launch takes effect.

Before claiming reference compatibility, run a separately designed bounded
probe for these cases or a justified equivalent set. Pin the original and
candidate builds and the fixture bytes, retain independent observations and
report mismatches. Candidate-only success proves agreement with this contract,
not with the running original.

## Fixture provenance

All 62 fixtures are complete minimal Live Sets authored for these cases from
one template written for the project. No fixture contains shipped file
content, program code or assets. The template set, at `12.0_12402`, holds:

- `NextPointeeId` 69, and 66 automation and modulation targets with Ids 1 to
  66;
- a MIDI track (`Id` 1, named `Lead`), an audio track (`Id` 2, `2-Audio`) and a
  return track (`Id` 3, `A-Return`), each with output to the main track, a
  mixer at new-mixer values and one send; the two player tracks have two
  session slots and two empty freeze slots each, and empty device chains; the
  MIDI track has a volume automation envelope with two events;
- in the MIDI track's first slot the MIDI clip `Two Notes` (4 beats, looped,
  4/4, two notes of key 60); in the audio track's first slot the audio clip
  `Tone` (2 beats, looped, unwarped, two warp markers), which references
  `Samples/T11-tone.wav` relative to the set;
- a main track with tempo 120 and time signature 4/4 and their one-event
  automation, a cue track, one send-pre item, two scenes, transport values,
  `GlobalQuantisation` 4, `AutoQuantisation` 0 and `CrossfadeCurve` 2.

Both clips hold the launch elements at the values of a new clip: launch mode 0,
launch quantization 0, `Legato` off, `VelocityAmount` 0 and the follow action
of REQ-CLIP-LAUNCH-009. Each fixture is the template, or the template with the
changes its purpose states; the fixture of CLIP-LAUNCH-005 adds an arrangement
MIDI clip of the same form to the MIDI track. The `12.0_12117` fixtures are the
template in that version's form, without the elements that version does not
define. The `11.0_405` fixtures are the template in that version's form: the
main track is `MasterTrack`, the scenes are items of `SceneNames` holding only
their name, track and clip colours are `ColorIndex`, both clips use the old
clip form, in which the five follow-action items are direct children of the
clip with the values 4, 0, 0, 1 and 0, and elements that version does not
define are absent. `Id` and `Time` attribute values, names and colours are
invented. Text is ASCII with line-feed line endings, tab indentation and a
final newline.

The sample is generated for the project: 1 s of a 441 Hz sine at amplitude
8,192, 44,100 Hz, 16-bit, two channels, as a PCM WAV file of 176,444 bytes.

Expected results are newly authored behavioral data. No public source or
dependency is approved or included. Review status is recorded in
[the manifest](manifest.json) and [the review disposition](REVIEW.md).
