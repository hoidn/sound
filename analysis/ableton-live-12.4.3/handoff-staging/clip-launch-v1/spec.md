# Clip launch settings in Live Set documents, release 1

Target: Ableton Live 12 Suite 12.4.3 (2026-07-07_e3d8be4d07), macOS, Apple
silicon (arm64). Features: FEAT-SESSION with FEAT-PERSISTENCE. Parent
specification identity: SPEC-CLIP-LAUNCH revision 1. Release: clip-launch-v1.
Only the clauses explicitly included below are in scope. No other clause of a
listed requirement is implicitly approved. This document is self-contained.

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

It does not describe launching. That includes when a launched clip starts, the
grid length that a quantization value stands for, how quantization places a
launch on the grid, and what launch modes, legato, velocity amount and follow
actions do during playback. It also does not describe the user interface,
editing after opening, the scripting interface, undo, or how a refused
document is reported.

All rules and expected results are **static-derived**: they were derived for
the target build without running it. None is an observed execution of the
original application, and none was run against a candidate. No compatibility
result is established. The original application remains the authority for a
later comparison. Some derived steps rest on behavior that was not traced to
the end:

- an item absent from a clip or a follow action keeps the value that a new
  clip or follow action starts with, and a value that is present and inside
  the ranges of the preconditions is kept as read;
- the opening corrections run for every clip read from a document, after any
  conversion;
- the rescaled chance values are kept as computed;
- before an older document's values are read, it is converted by every
  conversion step whose number is above the suffix number of its MinorVersion,
  in increasing order.

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
- A full Live Set contains much more than the fixtures, such as clip notes,
  loop settings, devices, mixer and transport state. That content is outside
  this release. Its absence from a fixture must not by itself change a judged
  outcome.
- Every clip in an input has `LaunchMode` and `LaunchQuantisation`, and
  `LiveSet` has `GlobalQuantisation` and `AutoQuantisation`.
- Expectations exist only for values in these ranges:

| Item | Range |
| --- | --- |
| `GlobalQuantisation` | 0 to 13 |
| `AutoQuantisation` | 0 to 8 |
| `VelocityAmount` | 0 to 1 |
| `FollowChanceA`, `FollowChanceB` | 0 to 100 |
| `JumpIndexA`, `JumpIndexB` | −1 to 8,388,608 |
| `LoopIterations` | 1 to 1,073,741,823 |
| `FollowTime` | 0 to below 1,000,000 |
| `LaunchMode`, `LaunchQuantisation`, `FollowActionA`, `FollowActionB` | the values of REQ-CLIP-LAUNCH-004, 005 and 007; other values only as REQ-CLIP-LAUNCH-011 states |

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
Which setting, time signature and grid a launch uses is excluded.

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

A `LaunchMode`, `LaunchQuantisation`, `FollowActionA` or `FollowActionB`
value outside the values of REQ-CLIP-LAUNCH-004, 005 and 007 does not refuse
the document when its text is an accepted integer. Nothing else about such a
value is part of this release: the value then held, displayed or written, and
any effect on launching, are excluded.

### REQ-CLIP-LAUNCH-012 — partial: follow-chance rescaling on opening

After a clip's follow action is read, let A and B be its `FollowChanceA` and
`FollowChanceB` values (binary32):

1. If A = 0 and B = 0, `FollowChanceA` becomes 100, `FollowChanceB` stays 0 and
   `FollowActionEnabled` becomes off.
2. Otherwise, with every operation in binary32 arithmetic rounded to nearest,
   ties to even: s = (A + B) ÷ 100 and q = A ÷ s. `FollowChanceA` becomes q
   rounded to an integer, with halves rounded away from zero, and
   `FollowChanceB` becomes 100 − `FollowChanceA`. `FollowActionEnabled` is
   unchanged.

Examples: 30 and 30 give 50 and 50 (q is 49.999996); 1 and 2 give 33 and 67;
1 and 7 give 13 and 87 (q is exactly 12.5); 0 and 50 give 0 and 100; 0.25 and
0.75 give 25 and 75; 100 and 0 are unchanged.

### REQ-CLIP-LAUNCH-013 — partial: follow-time rounding on opening

After a clip's follow action is read, `FollowTime` becomes the multiple of
1/3,843,840 nearest to its value, with halves rounded away from zero. The
result is the binary64 value nearest to m ÷ 3,843,840 for that multiple m.
3,843,840 is 2⁸·3·5·7·11·13. Examples: 2.0000001 gives 2; 3.0000002 gives
11,531,521 ÷ 3,843,840 (about 3.00000026); 1e-8 gives 0; 1.3333333 gives 4/3.
A value within 10⁻⁹ of a point halfway between two multiples has no
expectation.

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

## Acceptance representation and comparison

[cases.json](cases.json) lists 50 cases. Each has an input fixture, an action
(`open`, or `open-save`: open, then save without other changes) and an expected
result with these parts:

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
exact conversion to binary64. Saved documents are compared as parsed XML:
element names, nesting and attribute text, never bytes, whitespace,
indentation or attribute quoting. Anything a case does not list is not judged,
including other children of a clip, the saved envelope and every set-level or
scene item in a saved document. A refused case has no `values` or `saved`
part.

This is a **project comparison representation**, not an API claimed to exist
in Live and not a required design. A candidate adapter may translate its own
result into these labels. Each case starts from its fixture alone. Reading and
writing have no timing tolerance, cancellation step or teardown in this scope,
so those case kinds are omitted.

## Reference comparison obligation (not executed)

A comparison against the original application needs a full Live Set for each
case. The validation analyst builds it from an otherwise unchanged set saved
with the fixture's MinorVersion, whose root carries the fixture's
`MajorVersion`, `MinorVersion` and `SchemaChangeCount` values, and stores it
in the target's usual Live Set container:

- the set has a clip at each named clip location that the fixture uses, of the
  same kind. That clip's launch elements, and in `11.0_405` fixtures its direct
  children `FollowTime`, `FollowActionA`, `FollowActionB`, `FollowChanceA` and
  `FollowChanceB`, are replaced by the fixture's, in the fixture's order and
  number, and removed where the fixture has none;
- where the fixture has scenes, the set's first scene `FollowAction` is
  replaced by the fixture's, or removed where the fixture's first scene has
  none;
- `GlobalQuantisation` and `AutoQuantisation` are replaced by the fixture's.

Any set saved by the target build can serve for `12.0_12402`. The target's
factory default set is saved at `12.0_12117` and can serve there. For
`11.0_405` the analyst needs an authentic set saved by an earlier Live version
that writes that format version; none is included, and none ships with the
target. A value must be observed for the clip or scene at the named location.
The observation channel is chosen by the validation analyst; a channel that
rounds must be compared at its rounding. Notices shown when an older document
is opened or saved are not compared. None of this has been run.

## Exclusions and deferred obligations

Requirements not released: **REQ-CLIP-LAUNCH-008** (initial set values, and a
set without `GlobalQuantisation` or `AutoQuantisation`),
**REQ-CLIP-LAUNCH-010** (the initial launch mode and launch quantization of a
new clip, and a clip without `LaunchMode` or `LaunchQuantisation`),
**REQ-CLIP-LAUNCH-015** (the grid length that a quantization value stands for
with a given time signature; it has no observable outside launching) and
**REQ-CLIP-LAUNCH-016 to 023** (which grid a launch uses, the launch boundary,
launches without a grid, launching with the transport stopped, Gate, Toggle
and Repeat, Legato, velocity amount and follow-action execution).

Inputs with **no expectation** in this release:

- a clip without `LaunchMode` or `LaunchQuantisation`; a `LiveSet` without
  `GlobalQuantisation` or `AutoQuantisation`;
- an item of the item table without a `Value` attribute, with another
  attribute or with child elements;
- values outside the ranges in the preconditions, apart from the
  REQ-CLIP-LAUNCH-011 clause; non-finite values and negative zero;
- `FollowTime` within 10⁻⁹ of a point halfway between two multiples of
  1/3,843,840;
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
  scenes;
- in `12.0_12117` documents: a scene `FollowAction` without all ten items;
- any other envelope, format version, compressed container or document kind;
- documents that break more than one refusal rule.

Excluded behavior:

- launching: when a launched clip starts, the grid length of a quantization
  value, grid placement, the time signature a launch uses, launches without a
  grid or with the transport stopped, Gate, Toggle and Repeat press and release
  behavior, Legato, velocity scaling, follow-action timing, loop iterations,
  jump indices and chance selection;
- displayed text, including whether the user interface shows exactly the
  labels above and where each form of the follow-action labels is shown;
- the value held, displayed or written for an out-of-range launch mode,
  launch quantization or follow action;
- the text written for numbers and Booleans, and whether a written number with
  more than six significant digits reads back exactly; layout and indentation;
  the save container and envelope; what is written for set-level items and
  scenes;
- the initial launch mode and launch quantization of a new clip and the
  related preferences; initial set values; File > New; recording, drawing or
  dropping a clip;
- conversion steps other than 406, 417, 421 and 12203, the conversion of a
  clip that has both forms, and documents older than `11.0_405`;
- the scripting interface (Live API): names, properties and assignment of
  values;
- the effect of record quantization; scene follow actions other than their
  conversion; the key and MIDI assignment of the global quantization;
- editing after opening, undo, and the text and presentation of refusals.

Before claiming reference compatibility, run a separately designed bounded
probe for these cases or a justified equivalent set. Pin the original and
candidate builds and the fixture bytes, retain independent observations and
report mismatches. Candidate-only success proves agreement with this contract,
not with the running original.

## Fixture provenance

All 50 fixtures are minimal XML documents authored for these cases from a
template written for this release. The template has the declaration, the root
with the three attributes of the preconditions, and a `LiveSet` holding one
MIDI track whose first clip slot holds a MIDI clip, followed by
`GlobalQuantisation` 4 and `AutoQuantisation` 0. The clip holds only its
launch elements, with the values of a new follow action, launch mode 0, launch
quantization 0, `Legato` off and `VelocityAmount` 0. Each fixture is the
template or the template with the changes its purpose states: an audio track
or an arrangement clip in place of the session MIDI clip, a scene, or the
older clip form of `11.0_405`, in which the five follow-action items are
direct children of the clip. `Id` and `Time` attribute values are invented.
Text is ASCII with line-feed line endings, two-space indentation and a final
newline.

No fixture contains shipped file content, program code or assets. Expected
results are newly authored static-derived behavioral data. No public source or
dependency is approved or included. Review status is recorded in
[the manifest](manifest.json) and [the review disposition](REVIEW.md).
