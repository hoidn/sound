# MIDI clip note storage in Live Sets, release 1

Target: Ableton Live 12 Suite 12.4.3 (2026-07-07_e3d8be4d07), macOS, Apple
silicon (arm64). Features: FEAT-MIDI with FEAT-PERSISTENCE. Parent
specification identity: SPEC-MIDI-NOTE-STORAGE revision 1. Release:
midi-note-storage-v1. Only the clauses explicitly included below are in scope.
No other clause of a listed requirement is implicitly approved. This document
is self-contained.

**Status: reviewed local release.** A separate review approved the clauses
below with the narrowing recorded in [the review disposition](REVIEW.md).

## What the contract means

A user opens a Live Set that contains a MIDI clip, and saves it again. This
contract describes how the clip's notes are stored in the document, which
note text is accepted or refused when the set is opened, what changes on
opening, and what is written on saving. It covers:

- the structure that holds a clip's notes;
- note attributes: their types, accepted text, defaults and refusals;
- limits applied to note values, and the time grid, on opening;
- note identifiers and the clip's next identifier;
- per-note expression lists: their structure, validation, limits and order;
- attribute order, omission and number text on saving.

It does not cover what the user sees after a refusal or what then remains
open, probability groups, the meaning of the stored values (time units,
muting, chance, expression), or editing, playback, recording and undo.

All rules and expected results are **static-derived**: they were derived for
the target build without running it. None is an observed execution of the
original application, and none was run against a candidate. No compatibility
result is established. The original application remains the authority for a
later comparison. Some derived steps rest on assumptions that were not traced
to the end:

- that a refusal raised while the notes are read stops the reading of the
  document (see [the outcomes](#outcomes-and-comparison-convention));
- that opening a set and saving it without other changes changes the notes
  only as these rules state;
- that decimal number text is read and written with exact, correctly rounded
  conversions.

The [reference comparison obligation](#reference-comparison-obligation-not-executed)
covers them.

## Document scope and preconditions

- The input is a Live Set file in the fixtures' form (see
  [fixture provenance](#fixture-provenance)): a gzip file whose decompressed
  content is UTF-8 XML with the root `Ableton` carrying exactly
  `MajorVersion="5"`, `MinorVersion="12.0_12402"`, `SchemaChangeCount="1"`,
  `Creator="Ableton Live 12.4.3"` and the fixtures' `Revision`. Other
  containers, envelopes, format versions and document kinds, including clip
  files, are outside this release.
- The set has one MIDI track, whose first session clip is the case's MIDI
  clip, at `/Ableton/LiveSet/Tracks/MidiTrack/DeviceChain/MainSequencer/ClipSlotList/ClipSlot/ClipSlot/Value/MidiClip`.
  The **notes element** is the `Notes` child of that `MidiClip`. Paths below
  are relative to the notes element.
- A full Live Set contains much more than the fixtures: devices, mixer,
  scenes, other clip settings and other state. That content is outside this
  release, and its absence from a fixture must not by itself change a judged
  outcome. The clip's `Loop` element sets a loop from 0 to 8. This release
  does not interpret it, except that MNS-025 places a note outside that loop.
- The **text** of a value is its attribute value after standard XML
  attribute-value decoding.
- Number text uses `.` as the decimal separator. Expectations assume a host
  locale whose decimal separator is `.`; locale-dependent behavior is
  excluded.

## Terms

| Term | Meaning |
| --- | --- |
| Note | A `MidiNoteEvent` element |
| Key track | A `KeyTrack` element: the notes of one MIDI key |
| Per-note list | A `PerNoteEventList` element: the events of one note for one controller number `CC` |
| Event | A `PerNoteEvent` element |
| Next id | The `Value` of `NoteIdGenerator/NextId` |
| binary64, binary32 | IEEE 754 double and single precision |
| Largest finite value | 1.7976931348623157e308, the largest finite binary64 value |
| Refuse | A rule of this release rejects the document while it is read (see the outcomes) |

## Base notes

Every fixture holds the base notes below, or the base list, with the one
change that the case's purpose states. The notes are called n1 and n2 (key 36) and
n3 (key 38):

```xml
<Notes>
	<KeyTracks>
		<KeyTrack Id="0">
			<Notes>
				<MidiNoteEvent Time="0" Duration="0.25" Velocity="85" OffVelocity="64" NoteId="1" />
				<MidiNoteEvent Time="1" Duration="0.25" Velocity="85" OffVelocity="64" NoteId="2" />
			</Notes>
			<MidiKey Value="36" />
		</KeyTrack>
		<KeyTrack Id="1">
			<Notes>
				<MidiNoteEvent Time="0.5" Duration="0.25" Velocity="100" OffVelocity="64" NoteId="3" />
			</Notes>
			<MidiKey Value="38" />
		</KeyTrack>
	</KeyTracks>
	<PerNoteEventStore>
		<EventLists />
	</PerNoteEventStore>
	<NoteProbabilityGroups />
	<ProbabilityGroupIdGenerator>
		<NextId Value="1" />
	</ProbabilityGroupIdGenerator>
	<NoteIdGenerator>
		<NextId Value="4" />
	</NoteIdGenerator>
</Notes>
```

The **base list** fixtures replace `<EventLists />` with one per-note list L1
on n1, whose events are called e1 and e2:

```xml
<EventLists>
	<PerNoteEventList Id="0" NoteId="1" CC="-2">
		<Events>
			<PerNoteEvent TimeOffset="0.0625" Value="100" />
			<PerNoteEvent TimeOffset="0.125" Value="-200" />
		</Events>
	</PerNoteEventList>
</EventLists>
```

An added list takes the next unused list `Id` (1, then 2). An added event
with no stated value has `Value="1"`.

## Selected requirement clauses

Each clause below is included only as stated.

### REQ-MIDI-NOTE-STORAGE-001 — partial: note structure

1. The notes element has these children, in this order: `KeyTracks`,
   `PerNoteEventStore`, `NoteProbabilityGroups`,
   `ProbabilityGroupIdGenerator` and `NoteIdGenerator`. Each of the two
   generators holds one `NextId` element with a `Value` attribute.
2. `KeyTracks` holds key tracks. Each has an `Id` attribute and the children
   `Notes` and then `MidiKey`. That `Notes` element holds the notes of one
   key, and `MidiKey` has a `Value` attribute, the key.
3. Every child element of `KeyTrack/Notes` must be a `MidiNoteEvent`. Any
   other element there refuses the document.
4. A save writes this structure in this order.

### REQ-MIDI-NOTE-STORAGE-002 — partial: note attributes and their text

1. A note has these attributes:

   | Attribute | Type |
   | --- | --- |
   | `Time`, `Duration` | binary64 |
   | `Velocity`, `VelocityDeviation`, `OffVelocity`, `Probability` | binary32 |
   | `IsEnabled` | Boolean |
   | `NoteId` | 64-bit signed integer |

2. Attributes are accepted in any order. A repeated attribute makes the XML
   not well-formed, which refuses the document.
3. **Number text.** A binary64 value is read as follows. Leading U+0020 space
   characters are skipped. The value is then read from the longest prefix of
   the remaining text that forms a decimal number: an optional `+` or `-`;
   digits with an optional `.` and fraction digits, at least one digit in
   total; and an optional exponent of `e` or `E`, an optional sign and at
   least one digit. Text after the prefix is ignored, so ` 0.5abc` reads as
   0.5. The value is the binary64 number nearest to the prefix, ties to even.
   Text without such a prefix, such as `abc` or the empty string, refuses the
   document. The text `Invalid` reads as the largest finite value;
   expectations exist for it only in `Duration` and in an event's
   `TimeOffset`.
4. A binary32 value is read by the same rule and then rounded to the nearest
   binary32 value, ties to even. `33.3` reads as 33.299999237060546875.
5. **Boolean text.** `IsEnabled` text `true` or `1` is true, and `false` or
   `0` is false. Matching is exact and case-sensitive, with no trimming. Any
   other text, including `TRUE`, refuses the document.
6. **Integer text** of a note's `NoteId` and of the next id:

   | Text | Result |
   | --- | --- |
   | ASCII digits after any number of U+0020 spaces and then at most one `+`: `7`, ` 7`, `+7`, ` +7` | the integer |
   | ASCII digits followed only by U+0020 spaces, with nothing before the digits: `7 ` | the integer |
   | digits with spaces both before and after them, or a `+`, digits and trailing spaces: ` 7 `, `+7 ` | no expectation |
   | a `-` sign that does not directly follow a `+` | no expectation |
   | any other text | refused |

   An accepted integer has at most 63 digits and a value of at most
   9,223,372,036,854,775,807; otherwise it is refused. Examples of refused
   text: the empty string, three spaces, `3.0`, `0x3`, `+-3`, `３` (a
   fullwidth digit, outside ASCII), 64 digits, and `9223372036854775808`.
   Expectations exist only for accepted values from 0 to 1,000,000.
7. Expectations for `MidiKey`, `CC`, a list's `NoteId` and the `Id`
   attributes exist only for plain decimal text: `0`, or digits without a
   leading zero, with a leading `-` only in `CC`.

### REQ-MIDI-NOTE-STORAGE-003 — optional note attributes

1. A note that omits `VelocityDeviation` reads it as 0. One that omits
   `Probability` reads it as 1, and one that omits `IsEnabled` reads it as
   true. Each note is defaulted independently of the notes before it.
2. A note that omits any other attribute has no expectation, except for the
   case in REQ-MIDI-NOTE-STORAGE-009 clause 4.

### REQ-MIDI-NOTE-STORAGE-004 — note attributes on save

1. Each note is written as one `MidiNoteEvent` whose attributes appear in
   this order: `Time`, `Duration`, `Velocity`, `VelocityDeviation`,
   `OffVelocity`, `Probability`, `IsEnabled`, `NoteId`. An omitted attribute
   is skipped.
2. `Time`, `Duration`, `Velocity`, `OffVelocity` and `NoteId` are always
   written. `VelocityDeviation` is omitted when it is 0, `Probability` when it
   is 1, and `IsEnabled` when it is true.

### REQ-MIDI-NOTE-STORAGE-005 — partial: value limits on opening

1. After a note's attributes are read:
   - `Velocity` below 1 becomes 1, and above 127 becomes 127;
   - `OffVelocity` below 0 becomes 0, and above 127 becomes 127;
   - `Probability` below 0 becomes 0, and above 1 becomes 1;
   - `Duration` below 0, or equal to the largest finite value, becomes 0.

   A value set to 0 by these rules is positive zero. None of these values
   refuses the document.
2. `Time`, `VelocityDeviation` and `NoteId` are not limited. A negative `Time`
   is kept. A fractional `Velocity` within the limits is kept.

### REQ-MIDI-NOTE-STORAGE-006 — partial: time grid

1. On opening, each note's `Time` and `Duration` (after
   REQ-MIDI-NOTE-STORAGE-005) and each event's `TimeOffset` are rounded to a
   multiple of 1/3,843,840, half away from zero. In binary64 arithmetic, with
   each operation rounded to nearest:
   - let h = 2.6015651015651016e-07, the binary64 value nearest to
     1/3,843,840;
   - let s = +1 when x ≥ 0, else −1;
   - the stored value is s × (⌊|x + s × h/2| × 3,843,840⌋ / 3,843,840).
2. The largest finite value is left unchanged by this rule.
3. Values already on the grid are unchanged.
4. Examples:

   | Input | Stored and saved text |
   | --- | --- |
   | 0.123456789 | `0.123456751581751581` |
   | 0.3333333333 | `0.333333333333333315` |
   | −0.0000002 | `-0.000000260156510156510156` (−1/3,843,840) |
   | 0.00000013 | `0` |
   | 0.000000131 | `0.000000260156510156510156` |

### REQ-MIDI-NOTE-STORAGE-007 — partial: notes outside the loop

A note outside the clip's loop region, and a note with `Duration` 0, load and
save unchanged.

### REQ-MIDI-NOTE-STORAGE-008 — NoteId uniqueness

1. Within the clip, across all its key tracks, each non-zero `NoteId` must be
   unique. A repeat refuses the document.
2. `NoteId` 0 may occur on any number of notes (REQ-MIDI-NOTE-STORAGE-009).

### REQ-MIDI-NOTE-STORAGE-009 — partial: NoteId assignment and next id

1. After the notes are read, the clip's next id N becomes the larger of the
   stored next id and the largest non-zero `NoteId` plus 1, or 1 when no note
   has a non-zero `NoteId`.
2. Each note with `NoteId` 0 then receives N, and N increases by 1 after each.
   For key tracks stored in ascending key order, the key tracks are taken in
   that order, and the notes of each key track in document order. The order
   for other key tracks is not part of this release.
3. A save writes every note's `NoteId`, and the final N as the next id.
4. When `NoteId` is absent from every note of the clip, every note counts as
   `NoteId` 0 and is numbered as above.

### REQ-MIDI-NOTE-STORAGE-010 — partial: note and key track order

1. Take a clip whose key tracks are in ascending key order and whose notes in
   each key track are in strictly ascending `Time` order after rounding, with
   no note starting before the previous note of its key ends. A save keeps
   both orders.
2. Notes of one key that overlap in time, or that share a `Time`, do not
   refuse the document. What a save writes for them is not part of this
   release.

### REQ-MIDI-NOTE-STORAGE-013 — partial: per-note list structure

1. `PerNoteEventStore` has one child, `EventLists`, which holds per-note
   lists. Each list has the attributes `Id`, `NoteId` and `CC`, and one child
   `Events` holding its events.
2. An event has `TimeOffset` (binary64) and `Value` (binary32). It may also
   have `CurveControl1X`, `CurveControl1Y`, `CurveControl2X` and
   `CurveControl2Y` (binary64). Their text follows
   REQ-MIDI-NOTE-STORAGE-002 clauses 3 and 4.
3. An omitted curve control reads as 0.5, independently for each event.
4. On save, a curve control equal to 0.5 is omitted. `TimeOffset` and `Value`
   are always written.

### REQ-MIDI-NOTE-STORAGE-014 — partial: per-note list validation on opening

1. A list is removed, and the document is not refused, when:
   - its `NoteId` is 0;
   - its `CC` is outside −2 to 128, or is 0, 32 or 120 to 128 (the kept
     values are −2, −1, 1 to 31 and 33 to 119);
   - its `NoteId` equals no non-zero `NoteId` stored on a note of the clip. An
     id that a note only receives on opening (REQ-MIDI-NOTE-STORAGE-009) does
     not count.
2. Two lists with the same `NoteId` and `CC`, neither of them removed by the
   `NoteId` 0 or `CC` rule, refuse the document. This holds even when no note
   has that `NoteId`.
3. Within each list that the `CC` rule keeps:
   - an event whose `TimeOffset` is the largest finite value (text `Invalid`)
     is dropped;
   - `Value` is limited to −8192 to 8191 when `CC` is −2, and to 0 to 127
     otherwise;
   - events are sorted by ascending `TimeOffset`. Events with equal offsets
     keep their document order.
4. A list left without events is removed, including one stored with an empty
   `Events` element.
5. A kept list whose events all lie strictly after offset 0 and strictly
   before the `Duration` of its note (both after rounding) is otherwise
   unchanged.

### REQ-MIDI-NOTE-STORAGE-016 — partial: number and Boolean text on save

1. Values are written as held after REQ-MIDI-NOTE-STORAGE-005, 006 and 014.
   They are not rounded again.
2. `NoteId`, the next id, `CC` and `MidiKey` are written as plain decimal
   integers. `IsEnabled` false is written `false`.
3. Let P be 17 for the binary64 attributes (`Time`, `Duration`, `TimeOffset`
   and the curve controls) and 9 for the binary32 attributes (`Velocity`,
   `VelocityDeviation`, `OffVelocity`, `Probability` and `Value`). Positive
   zero is written `0`. For any other value x:
   1. let k be the smallest integer not below log10|x| when |x| ≥ 1, and the
      largest integer not above log10|x| when |x| < 1;
   2. write x in fixed-point notation with max(0, P − k) digits after the
      decimal point, rounded from its exact binary value to nearest, ties to
      even (a binary32 value is first converted exactly to binary64);
   3. if the text contains `.`, remove trailing `0` characters and then a
      trailing `.`.
4. Examples:

   | Value | Saved text |
   | --- | --- |
   | `Velocity` read from `33.3` | `33.2999992` |
   | `Velocity` read from `80.578949` | `80.578949` |
   | curve control read from `0.2` | `0.200000000000000011` |
   | `Value` 8191, −8192 | `8191`, `-8192` |

### Combined failures

Every case breaks at most one refusal rule. A document that breaks more than
one refusal rule of this release has no expectation.

## Outcomes and comparison convention

[cases.json](cases.json) lists 67 cases. Each has one input fixture, an
action and an expected result. The action is `open`, or `open-save`: open the
set, then save it as a new set without other changes. The expected result
has these parts:

| Field | Meaning |
| --- | --- |
| `outcome` | `loads`: no rule of this release refuses the document. `refused`: a rule of this release refuses the document while it is read |
| `saved_notes` | `open-save` only: the expected saved notes element |

`saved_notes` has three parts:

| Part | Meaning |
| --- | --- |
| `key_tracks` | The key tracks in saved order. Each gives `midi_key`, the `MidiKey` value text, and `notes`, the notes in saved order. Each note maps every attribute name to its exact text |
| `event_lists` | The per-note lists. Each gives `NoteId` and `CC` text and `events`, the events in saved order. Each event maps every attribute name to its exact text |
| `note_id_next` | The exact next id text |

Comparison rules:

- `outcome` compares exactly.
- For `refused`, what the application shows, its wording, and what remains
  open after the refusal are not compared. Nothing remaining open and the set
  remaining open without the case's clip both match.
- The saved document is compared as parsed XML: element names, nesting and
  attribute text, never bytes, whitespace, indentation or attribute quoting.
  The saved notes element must:
  1. have exactly the five children of REQ-MIDI-NOTE-STORAGE-001, in order;
  2. hold in `KeyTracks` exactly the listed key tracks, in the listed order.
     Each has the children `Notes` and then `MidiKey`, whose `Value` equals
     `midi_key`. Its `Notes` holds exactly the listed notes in the listed
     order. Each note has exactly the listed attributes, with exactly the
     listed text, in the order of REQ-MIDI-NOTE-STORAGE-004;
  3. hold in `PerNoteEventStore` one `EventLists` with exactly the listed
     lists, each matched by its `NoteId` and `CC`. Their order is not
     compared. Each list has one `Events` child holding exactly the listed
     events in the listed order. Each event has exactly the listed attributes
     with exactly the listed text, in any attribute order;
  4. hold in `NoteIdGenerator` one `NextId` whose `Value` equals
     `note_id_next`.
- Not compared: the `Id` attributes of key tracks and lists, the content of
  `NoteProbabilityGroups`, the `Value` of
  `ProbabilityGroupIdGenerator/NextId`, and everything outside the notes
  element.
- An `open` case with outcome `loads` judges only the outcome.
- Each case is independent and starts from its fixture alone. Reading and
  writing have no timing tolerance, cancellation step or teardown within this
  scope, so those case kinds are omitted.

Each case also carries its `kind` (positive, negative, boundary, missing or
save), the requirement IDs it exercises, its `expectation_provenance`, and
`reference_execution` and `candidate_execution`, both `not-run`.

This is a **project comparison representation**, not an API claimed to exist
in Live and not a required design. A candidate adapter may translate its own
result into these labels. The fixture set is not an executable harness for
the original application.

## Reference comparison obligation (not executed)

A later comparison against the original application needs a full Live Set per
case. The validation analyst builds it from a set saved by the target build,
whose root carries the fixture's `MajorVersion`, `MinorVersion` and
`SchemaChangeCount` values and which has one MIDI track whose first session
clip is a MIDI clip looping from 0 to 8. The fixture's notes element replaces
that clip's notes element. The application uses its factory default set, not
a user template, and the host locale uses `.` as the decimal separator. The
set is opened, then saved as a new set without other changes, and the saved
clip's notes element is compared.

A `refused` observation matches when the original reports the set as damaged,
does not open it, or opens it without the case's clip. A set that opens with
the case's clip holding notes is a mismatch. A set that opens with the case's
clip present but holding no notes is inconclusive. The observation channel is
chosen by the validation analyst. None of this has been run.

Before claiming reference compatibility, a separately designed bounded probe
must run these cases, or a justified equivalent set, against the original. It
must pin the original and candidate builds and the fixture bytes, retain
independent observations, and report mismatches. Candidate-only success
proves agreement with this contract, not with the running original.

## Exclusions and deferred obligations

Requirements not released:

- **REQ-MIDI-NOTE-STORAGE-011**: the MIDI key range and repeated keys;
- **REQ-MIDI-NOTE-STORAGE-012**: the key track and list `Id` values on save,
  and whether empty key tracks are kept;
- **REQ-MIDI-NOTE-STORAGE-015**: probability groups;
- **REQ-MIDI-NOTE-STORAGE-017**: how a refusal is presented and what remains
  open.

These inputs have **no expectation** in this release:

- a note without `Time`, `Duration`, `Velocity` or `OffVelocity`; `NoteId`
  absent from some but not all notes; an event without `TimeOffset` or
  `Value`;
- a `MidiKey` value outside 0 to 127, a key track without `MidiKey`, two key
  tracks with the same key, key tracks not in ascending key order, a key
  track without notes, and repeated key track or list `Id` values;
- notes of one key that are not in strictly ascending `Time` after rounding,
  or that overlap, beyond the outcome in REQ-MIDI-NOTE-STORAGE-010 clause 2;
- a list that REQ-MIDI-NOTE-STORAGE-014 clauses 1 and 4 do not remove and
  that, after the drop of clause 3, has an event at or before offset 0, or at
  or after its note's `Duration`;
- number text starting with `#`; text whose remainder, after leading spaces
  and an optional sign, starts with `0x`, `0X`, `inf` or `nan` in any letter
  case; leading whitespace other than U+0020; `Invalid` in any attribute other
  than `Duration` and `TimeOffset`; values whose magnitude is 1,000,000 or
  more, other than `Invalid`; non-finite values; negative zero, whether read
  (`-0`) or produced by rounding (`-0.0000001`); saved values whose base-10
  logarithm lies within 1e-12 of an integer without being an exact power of
  ten;
- integer text marked "no expectation" in REQ-MIDI-NOTE-STORAGE-002 clause 6,
  including negative `NoteId` and next id values; accepted integer values
  above 1,000,000; `MidiKey`, `CC`, list `NoteId` and `Id` text other than
  plain decimal;
- a missing structural element, such as no `NoteIdGenerator` or a key track
  without `Notes`; unknown attributes or child elements in the note
  structures; a `NoteProbabilityGroups` element with content;
- documents that break more than one refusal rule;
- other containers, envelopes, format versions and document kinds.

Excluded behavior:

- what is shown after a refusal, and what remains open;
- probability groups, and the saved `ProbabilityGroupIdGenerator/NextId`;
- re-sorting, trimming or merging of unsorted or overlapping notes, and the
  adjustment of per-note lists that reach the edges of their note;
- the meaning of the values: time units, muting, chance, expression
  controllers;
- editing, playback, recording and undo; the rest of the clip and the set.

Cases of the parent draft not released: MNS-011 (integer text with spaces on
both sides), MNS-023 (a value that rounds to negative zero), MNS-024 (`Time`
of `Invalid`), MNS-034 (a negative next id), MNS-035 (notes out of order),
MNS-037 (key values outside 0 to 127, a missing key, repeated keys), MNS-038
(repeated key track `Id`s), MNS-053 (events at or outside the note's span),
MNS-054 to MNS-059 (probability groups) and MNS-060 (refusal presentation).
MNS-036 is released for its outcome only. MNS-043, 044, 045, 049 and 051 are
split into one case per variant, with a letter suffix. MNS-061 to MNS-071 are
new cases for released clauses that had none.

## Fixture provenance

All 67 fixtures were authored for this release from a carrier Live Set written
for it. The carrier is the declaration, the root `Ableton` with the attributes
listed under the preconditions and an invented forty-digit hexadecimal
`Revision`, and the elements on the path to the clip: `LiveSet`, `Tracks`,
`MidiTrack Id="1"`, `DeviceChain`, `MainSequencer`, `ClipSlotList`,
`ClipSlot Id="0"`, `ClipSlot`, `Value` and `MidiClip Id="0" Time="0"`. The
clip holds a `Loop` element with `LoopStart` 0, `LoopEnd` 8 and `LoopOn`
true, then the notes element. Each fixture is the carrier holding the base
notes, or the base list, with the one change that its purpose states. Text is
UTF-8 with line-feed line endings and tab indentation.

Each fixture is a single-member gzip file. The 10-byte header is
`1F 8B 08 00 00 00 00 00 02 13`: deflate, no optional header fields, zero
modification time, maximum-compression marker and operating-system byte 19.
The header is followed by raw deflate data at maximum compression and the
CRC-32 and length trailer. Nothing follows the trailer.

No fixture contains shipped file content, program code or assets. Element and
attribute names are the public names of the document format. Expected results
are newly authored static-derived behavioral data. No public source or
dependency is approved or included. Review status is recorded in
[the manifest](manifest.json) and
[the review disposition](REVIEW.md).
