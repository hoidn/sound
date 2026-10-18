---
id: SPEC-MIDI-NOTE-STORAGE
type: spec
status: draft
revision: 1
updated: 2026-10-18
access: analysis
target: Ableton Live 12 Suite 12.4.3 / macOS
---

# MIDI clip note storage

## Scope

Feature FEAT-MIDI, with FEAT-PERSISTENCE, in the [feature map](feature-map.md).
User task: open a document containing a MIDI clip and save it again. This draft specifies
how the clip's notes are stored in the document and how they are read and written:

- the note structure;
- attribute types, text and defaults;
- normalization on load (clamping and the time grid);
- note identifiers;
- per-note expression lists and probability groups;
- the order and number text a save writes.

Every requirement is a **proposed contract**. Each clause is documented by shipped files,
supported by a static derivation, or explicitly unknown. Nothing was run against Live.
[ADR 0002](../decisions/adr-0002-static-first-analysis.md) permits a static-first draft.
The target is documents with `MinorVersion="12.0_12402"`. The gzip and XML envelope belongs
to [SPEC-ALS-CONTAINER](als-container.md). Value text follows
[SPEC-TRANSPORT-STATE](transport-state.md) REQ-003, 004, 005 and 011. Both are dependencies.
All examples are fragments of decoded XML.

## Evidence labels

| Label | Meaning |
| --- | --- |
| D | Documented: present in the shipped schema for `12.0_12402` or in shipped documents. Those documents were written by 12.4d1 or older, not by 12.4.3 |
| S | Static derivation from the 12.4.3 executable; not an observed run |
| U | Unknown; no expected result. PRB IDs name the Phase 4 probe that would settle it |

Only D and S clauses may enter a release. U clauses block the behavior they name.

Static clauses rest on two stated assumptions:

| ID | Assumption | Affects |
| --- | --- | --- |
| A1 | The per-item normalization step of the document reader (REQ-005) runs when a Live Set or clip file is loaded. This is inferred, not traced | REQ-005 |
| A2 | The acceptance procedure, which places a loaded clip file into a set and saves the set, does not itself change the notes, their ids or the clip's next id. This is not traced; PRB-S7-09 checks it | Every case that compares saved values |

**Refused** means that the document reader stops with a read error of the corrupt-document
class. That is the class of SPEC-ALS-CONTAINER; for a duplicate attribute it is the XML
class. What the user then sees, and what stays loaded, is U (REQ-017).

## Exclusions

These inputs and behaviors have no requirement in this revision. They are not graded, and
fixtures avoid them.

- **Missing note attributes.** A `MidiNoteEvent` that omits Time, Duration, Velocity,
  OffVelocity or NoteId is malformed input. The reference's static outcome depends on the
  notes read before it in the same key, and is recorded in the appendix only. One exception
  is specified: NoteId absent from **every** note of the clip (REQ-009). The same exclusion
  applies to a `PerNoteEvent` that omits TimeOffset or Value.
- **Key range and duplicate keys** (REQ-011). These are excluded because the reference's
  handling may corrupt memory.
- **Non-finite and special values.** NaN or infinite note and event values, and the
  unrounded time values of REQ-006, are excluded beyond the clauses stated there.
- **Negative ids.** Negative NoteId, NextId and GroupId values (REQ-008, 009, 015).
- **Other document content.** Older document versions and their translation, binary groove
  files, and unknown attributes or child elements in the note structures.
- **Behavior beyond load and save.** Editing, playback, recording, undo, the meaning of
  per-note expression, and every other `MidiClip` field. Loop and launch fields belong to
  the planned SPEC-CLIP-LAUNCH.

## Requirements

### REQ-MIDI-NOTE-STORAGE-001 — note container structure

- **D.** A MIDI clip's notes are the `Notes` child of `MidiClip`. Its children are, in this
  order: `KeyTracks`, `PerNoteEventStore`, `NoteProbabilityGroups`,
  `ProbabilityGroupIdGenerator` and `NoteIdGenerator`. Each generator holds one `NextId`
  element with a `Value` attribute.
- **D.** `KeyTracks` holds `KeyTrack` elements. Each has an `Id` attribute and the children
  `Notes` and then `MidiKey`. `Notes` holds the notes of one MIDI key as `MidiNoteEvent`
  elements. `MidiKey` has a `Value` attribute.
- **D.** Notes are grouped by pitch. In shipped clips no two KeyTracks share a key, and every
  key lies in 20 to 127.
- **S.** A save writes this structure in this order.
- **S.** Every child element of `KeyTrack/Notes` must be a `MidiNoteEvent`. Any other element
  there makes the document refused.
- **U.** A missing structural child, such as no `NoteIdGenerator` or a KeyTrack without
  `Notes` (see Exclusions).

### REQ-MIDI-NOTE-STORAGE-002 — note attributes and their text on load

- **D.** A `MidiNoteEvent` has these attributes:

  | Attribute | Type |
  | --- | --- |
  | `Time`, `Duration` | 64-bit floating point |
  | `Velocity`, `VelocityDeviation`, `OffVelocity`, `Probability` | 32-bit floating point |
  | `IsEnabled` | Boolean |
  | `NoteId` | 64-bit signed integer |

- **S.** Attributes are accepted in any order.
- **S.** Value text follows SPEC-TRANSPORT-STATE:
  - 64-bit values follow REQ-TRANSPORT-STATE-004;
  - 32-bit values follow the 32-bit form of REQ-TRANSPORT-STATE-005;
  - `IsEnabled` follows REQ-TRANSPORT-STATE-003: exactly `true` or `1` for true, and `false`
    or `0` for false. Any other text makes the document refused.
- **S.** Integer text (`NoteId`, both `NextId` values and the group id of REQ-015) is accepted
  in these forms only:
  - ASCII decimal digits after any number of U+0020 spaces and then at most one `+`
    (`7`, ` 7`, `+7`, ` +7`);
  - digits followed only by spaces, when nothing precedes the digits (`7 `).

  After the leading spaces and sign, the part up to the last digit must be at most 63
  characters. The value must fit in 64 bits.
- **S.** Any other integer text makes the document refused. This includes an empty or
  all-space value, `7.0`, `0x10`, `+-7`, a non-ASCII byte and an overflowing number.
- **S.** A repeated attribute is malformed XML, and the document is refused.
- **U.** These integer spellings are unknown:
  - spaces on both sides of the digits, or a `+` with trailing spaces (` 7 `, `+7 `).
    The static reading is refused;
  - a `-` sign (see Exclusions).

### REQ-MIDI-NOTE-STORAGE-003 — optional note attributes

- **S.** On load, each note that omits `VelocityDeviation` gets 0. One that omits
  `Probability` gets 1, and one that omits `IsEnabled` gets true. Each note is defaulted
  independently of the notes before it.
- Excluded: omitting any other attribute (see Exclusions; REQ-009 has one exception).

### REQ-MIDI-NOTE-STORAGE-004 — note attributes on save

- **S.** Each note is written as one `MidiNoteEvent` with its attributes in this order:
  `Time`, `Duration`, `Velocity`, `VelocityDeviation`, `OffVelocity`, `Probability`,
  `IsEnabled`, `NoteId`.
- **S.** `Time`, `Duration`, `Velocity`, `OffVelocity` and `NoteId` are always written.
  `VelocityDeviation` is omitted when it is 0, `Probability` when it is 1, and `IsEnabled`
  when it is true.
- **D.** Every note written by 12.4d1 agrees with this rule. Older writers wrote all eight
  attributes. Live 10.1.6 grooves list them alphabetically.

### REQ-MIDI-NOTE-STORAGE-005 — value normalization on load

- **S (A1).** After a note's attributes are read:
  - `Velocity` below 1 becomes 1, and above 127 becomes 127;
  - `OffVelocity` below 0 becomes 0, and above 127 becomes 127;
  - `Probability` below 0 becomes 0, and above 1 becomes 1;
  - a `Duration` below 0, or equal to the largest finite 64-bit value, becomes 0.

  These values do not make the document refused.
- **S.** `Time`, `VelocityDeviation` and `NoteId` are not range-checked. A negative `Time` is
  kept.
- **S.** A fractional `Velocity` is kept, for example 80.578949.
- Excluded: NaN and infinite values (the rules above do not change NaN).

### REQ-MIDI-NOTE-STORAGE-006 — time grid

- **S.** On load, each note's `Time` and `Duration` (after REQ-005) and each per-note event's
  `TimeOffset` are rounded to a grid of 1/3,843,840 beat, half away from zero. In binary64
  arithmetic, with each operation rounded:
  - let h = 2.6015651015651016e-07 (the binary64 value of 1/3,843,840);
  - let s = +1 when x ≥ 0 (including −0), else −1;
  - the stored value is s × (⌊|x + s × h/2| × 3,843,840⌋ / 3,843,840).
- **S.** These values are not rounded: ±1.7976931348623155e308, the largest finite value
  1.7976931348623157e308 (text `Invalid`), and +∞.
- **S.** Values already on the grid are unchanged. Every shipped value is on the grid.
- **S.** Examples:

  | Input | Stored and saved |
  | --- | --- |
  | 0.123456789 | `0.123456751581751581` |
  | 0.3333333333 | `0.333333333333333315` |
  | −0.0000002 | `-0.000000260156510156510156` (−1/3,843,840) |
  | 0.00000013 | `0` |
  | 0.000000131 | `0.000000260156510156510156` |

- **U.** The saved text of a value that rounds to negative zero, such as −0.0000001.
  REQ-TRANSPORT-STATE-011 leaves negative zero unknown.
- **U.** What a note whose time was not rounded does after load, including whether it is
  kept.

### REQ-MIDI-NOTE-STORAGE-007 — time coordinates and value domains

- **D.** In shipped documents:
  - `Time` runs from −1/3,843,840 to 352, and `Duration` from 0 to 80;
  - `Velocity` runs from 1 to 127, often fractional;
  - `OffVelocity` takes integers 0 to 127, and `Probability` values 0 to 1;
  - 12.4d1 wrote `IsEnabled` only as `false`, and `VelocityDeviation` only as `3`;
  - notes before the clip's loop start and at or after its loop end are stored.
- **S.** A note outside the clip's loop region, and a note with `Duration` 0, load and save
  unchanged.
- **U.** These meanings are inferred and not established:
  - that `Time` and `Duration` are quarter-note beats on the clip's own time line, the
    coordinate of the clip loop fields;
  - that `IsEnabled` false is a muted note;
  - that `Probability` is a play chance;
  - the range of `VelocityDeviation`.

### REQ-MIDI-NOTE-STORAGE-008 — NoteId uniqueness

- **S.** Within one clip, across all its KeyTracks, each non-zero `NoteId` must be unique.
  A repeat makes the document refused.
- **S.** `NoteId` 0 may occur on any number of notes (REQ-009).
- Excluded: negative NoteIds, which the reference compares as unsigned values.

### REQ-MIDI-NOTE-STORAGE-009 — NoteId assignment and next id

- **S.** After the notes load, the clip's next id N becomes the larger of:
  - the stored `NoteIdGenerator/NextId`;
  - the largest non-zero NoteId plus 1, or 1 when no note has a non-zero NoteId.
- **S.** Then each note with NoteId 0 receives N, and N increases by 1 after each. Notes are
  taken KeyTrack by KeyTrack, and within a KeyTrack in document order. For a clip whose
  KeyTracks are in ascending key order, KeyTracks are taken in ascending key order.
- **S.** A save writes every note's NoteId and the final N as `NoteIdGenerator/NextId`.
- **S.** When `NoteId` is absent from every note of the clip, every note counts as NoteId 0
  and is numbered as above.
- **U.** The next id when `NoteIdGenerator` is missing, and the order for KeyTracks that are
  not in ascending key order (REQ-010).
- Excluded: a negative next id. The reference compares it as unsigned (PRB-S7-10).

### REQ-MIDI-NOTE-STORAGE-010 — note and KeyTrack order

- **S.** Take a clip whose KeyTracks are in ascending key order and whose notes in each
  KeyTrack are in strictly ascending `Time` order after rounding. Load and save keep both
  orders. No load step reorders notes or KeyTracks.
- **S.** Notes of one key that overlap in time, or that share a `Time`, do not make the
  document refused.
- **D.** Every shipped clip has ascending key order and strictly ascending times within each
  key. 261 shipped notes start before the previous note on the same key ends.
- **U.** These outcomes are unknown (PRB-S7-06):
  - whether notes or KeyTracks stored out of order are re-sorted before a later save;
  - whether overlapping notes are kept, trimmed or merged after load, and how they play.

### REQ-MIDI-NOTE-STORAGE-011 — MIDI key range and duplicate keys

- **U, excluded.** Three inputs are unknown and excluded:
  - a `MidiKey` value outside 0 to 127;
  - a KeyTrack without `MidiKey`;
  - two KeyTracks with the same key.

  The reference handles them without a range or duplicate check, so the outcome may be
  memory corruption rather than defined behavior. No reference outcome may be treated as
  required. See [Q-018](../questions.md#q-018-midi-note-key-range-and-ordering-after-load)
  and PRB-S7-05, which runs in a disposable session.

### REQ-MIDI-NOTE-STORAGE-012 — list ids and empty KeyTracks

- **D.** Shipped KeyTrack `Id`s are unique within a clip and need not follow key order. They
  are ascending in 719 of 1,368 clips. Per-note lists also carry an `Id`.
- **S.** A save writes an `Id` attribute on each KeyTrack and each per-note list.
- **U.** These are unknown (PRB-S7-09):
  - the meaning of these Ids;
  - whether loaded Ids are written back unchanged;
  - how repeated Ids are read;
  - whether an empty KeyTrack is kept or removed on load. The reference removes empty
    KeyTracks under a condition that was not traced. 12.4d1 saves contain 267 empty
    KeyTracks.

### REQ-MIDI-NOTE-STORAGE-013 — per-note expression structure

- **D.** `PerNoteEventStore/EventLists` holds `PerNoteEventList` elements.
  - Each list has the attributes `Id`, `NoteId` and `CC`, and an `Events` child holding
    `PerNoteEvent` elements.
  - An event has `TimeOffset` (64-bit) and `Value` (32-bit). It may also have
    `CurveControl1X`, `CurveControl1Y`, `CurveControl2X` and `CurveControl2Y` (64-bit).
  - Shipped `CC` values are −2, −1 and 74.
- **S.** An omitted curve control loads as 0.5, independently for each event.
- **S.** On save, a curve control equal to 0.5 is omitted. `TimeOffset` and `Value` are always
  written. `TimeOffset` is rounded on load (REQ-006).
- **U.** These meanings are inferred:
  - that `TimeOffset` is measured from the note's start;
  - that CC −2 is per-note pitch bend in 14-bit units, −1 is per-note pressure and 74 is
    slide.
- Excluded: omitted `TimeOffset` or `Value` (see Exclusions).

### REQ-MIDI-NOTE-STORAGE-014 — per-note expression validation on load

- **S.** A per-note list is removed, and the document is not refused, when:
  - its `NoteId` is 0;
  - its `CC` is outside −2 to 128, or is 0, 32 or 120 to 128 (the kept CCs are −2, −1, 1 to
    31 and 33 to 119);
  - its `NoteId` names no non-zero NoteId stored on a note of the clip. A list naming an id
    that a note only receives through REQ-009 is removed.
- **S.** Two lists that share `NoteId` and `CC`, and that both pass the `NoteId` 0 and `CC`
  rules, make the document refused. This holds even when that NoteId names no note.
- **S.** Within each list that passes the `CC` rule:
  - an event whose `TimeOffset` is the largest finite value (text `Invalid`) is dropped;
  - `Value` is limited to −8192 to 8191 when `CC` is −2, and to 0 to 127 otherwise;
  - events are sorted by ascending `TimeOffset`. Events with equal offsets keep their
    document order.
- **S.** A list left without events is removed, including one stored with an empty `Events`.
- **S.** A list whose events all lie strictly after offset 0 and strictly before the note's
  `Duration` (after rounding) is otherwise unchanged.
- **U.** Lists with an event at or before offset 0, or at or after the note's `Duration`. The
  reference adjusts such lists in a way that was not traced, and may remove or re-sample
  events outside the note. Whether such a list ends up empty, and so removed, follows from
  that adjustment. Shipped lists often start at offset 0, so this gap matters (proposed
  PRB-S7-07 variants).

### REQ-MIDI-NOTE-STORAGE-015 — probability groups

- **D.** The schema defines `NoteProbabilityGroups` as a list of groups. Each group has a
  group type, a list of note ids, a probability and a 64-bit `GroupId`. The group generator
  holds `NextId`. No shipped document contains a group.
- **S.** When the clip has at least one group, the groups are checked in document order. Each
  `GroupId` must be greater than 0 and greater than the previous group's id. Each must also
  be below the group generator's `NextId`, compared as unsigned values. Otherwise the
  document is refused.
- **S.** A group's note ids are not checked against the clip's notes. A group naming a missing
  note does not make the document refused.
- **U.** These are unknown (PRB-S7-08):
  - the XML shape of a group, including whether `GroupId` is an attribute;
  - the group type values;
  - what a group naming a missing note does after load;
  - the saved group text;
  - whether the group generator's `NextId` is raised on load.

  The cases for this requirement are blocked until the group shape is known.

### REQ-MIDI-NOTE-STORAGE-016 — number and Boolean text on save

- **S.** Values are written as held after REQ-005 and REQ-006. The writer does not round
  again.
- **S.** Number text follows REQ-TRANSPORT-STATE-011:
  - `Time`, `Duration`, `TimeOffset` and the curve controls use the 64-bit rule;
  - `Velocity`, `VelocityDeviation`, `OffVelocity`, `Probability` and `Value` use the 32-bit
    rule;
  - `NoteId`, `NextId`, `CC`, `Id` and `GroupId` are plain decimal integers;
  - `IsEnabled` is written `false` (true is omitted, REQ-004).
- **D.** All 2,054,618 shipped note and event numbers agree with this rule, for example
  `Time="0.359923670079920099"`.
- Examples:

  | Value | Saved text |
  | --- | --- |
  | Time 0.1 | `0.100000000000000006` |
  | Velocity 33.3 | `33.2999992` |
  | Velocity 80.578949 | `80.578949` |
  | Curve control 0.2 | `0.200000000000000011` |

- **U.** Negative zero, as in REQ-006.

### REQ-MIDI-NOTE-STORAGE-017 — refusal presentation

- **S.** The refusals of REQ-001, 002, 008, 014 and 015 are raised as corrupt-document read
  errors that carry a detail text.
- **U.** What the user sees is unknown, including whether the detail is shown, as for
  REQ-ALS-CONTAINER-009. It is also unknown whether the whole set or clip file is rejected or
  only the clip is dropped, and what remains loaded (PRB-S7-02).

## Timing and state

- **Units.** Times are binary64 values on a grid of 1/3,843,840 (REQ-006). The beat unit is
  inferred (REQ-007).
- **Order of load effects.** Clauses that interact apply in this order:
  1. per note: defaults (REQ-003), then the attribute values, then the limits (REQ-005),
     then rounding (REQ-006);
  2. per event list: event drop, value limits and sort (REQ-014);
  3. list removal by NoteId 0 or CC, and the duplicate-pair refusal (REQ-014);
  4. the NoteId uniqueness check (REQ-008), then the next-id raise (REQ-009);
  5. removal of lists naming no note, then of empty lists (REQ-014);
  6. assignment of NoteId 0 notes (REQ-009);
  7. the group check (REQ-015).

  Cases MNS-046 and MNS-052 depend on this order.
- **Persistent state.** The note fields, the per-note lists, the groups and both `NextId`
  values. Editing, playback and undo are out of scope.
- **Determinism.** Load and save are deterministic for a given document, so saved attribute
  text can be compared exactly.

## Acceptance cases

**Base B0.** The shipped clip file
`Core Library/MIDI Clips/Drums/Drum Machines/909 Core Kit House 127 bpm.alc`
(SHA-256 `79c6ed2f5a46d8ce139e2dae5261285c6894d196e289835f455906e4a901ff59`,
`MinorVersion="12.0_12402"`, written by 12.4d1). It contains one MIDI clip whose loop runs
from 0 to 8.

**Construction.** Decode B0, replace the clip's `MidiClip/Notes` element with the case
fragment, and re-encode as gzip.

**Procedure.** This is the common procedure of the S7 probe batch:

1. Start with fresh preferences.
2. Drag the file into an empty MIDI track.
3. Save as a new set.
4. Compare the clip's `Notes` element in the saved set.

**Comparators.** Attribute values are compared as exact text. KeyTrack and list `Id` values
are not compared (REQ-012). Assumption A2 applies to every saved comparison.

**Fragment F0.** Its notes are called n1, n2 (key 36) and n3 (key 38):

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

**Fragment F1.** F0 with `<EventLists />` replaced by one list L1 on n1, whose events are
called e1 and e2:

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

**Fragment G.** The probability-group cases replace F0's `<NoteProbabilityGroups />`. The
group shape is unknown, so they are marked "blocked" until PRB-S7-08 records one.

**Case kinds.** P positive, N negative (refused), B boundary, M missing input, S save text,
U unresolved. All expected results are static derivations or shipped-document facts; none
has been run. Unless stated otherwise, the other values are unchanged from F0 or F1.

| Case ID | Requirement | Kind | Setup (edit of F0 or F1) | Expected result | Fixture |
| --- | --- | --- | --- | --- | --- |
| MNS-001 | 001, 004, 010, 016 | S | F0 unchanged | Loads. The saved `Notes` equals F0 apart from Ids: KeyTracks 36 then 38, the same note order and attribute text, `NextId` 4 | B0+F0 |
| MNS-002 | 003, 004 | P | n1 adds `VelocityDeviation="0" Probability="1" IsEnabled="true"` | Saved n1 has none of these three attributes | B0+F0 |
| MNS-003 | 004, 016 | S | n1 adds `VelocityDeviation="3" Probability="0.5" IsEnabled="false"` | Saved n1 is exactly `Time="0" Duration="0.25" Velocity="85" VelocityDeviation="3" OffVelocity="64" Probability="0.5" IsEnabled="false" NoteId="1"` | B0+F0 |
| MNS-004 | 002, 003 | B | n1 written as `<MidiNoteEvent Duration="0.25" IsEnabled="false" NoteId="1" OffVelocity="64" Probability="0.5" Time="0" Velocity="85" VelocityDeviation="3" />` | Saved n1 as in MNS-003 | B0+F0 |
| MNS-005 | 002, 004 | P | n1 `IsEnabled="0"`, n2 `IsEnabled="1"` | Saved n1 has `IsEnabled="false"`; saved n2 has no `IsEnabled` | B0+F0 |
| MNS-006 | 002 | N | n1 `IsEnabled="TRUE"` | Refused | B0+F0 |
| MNS-007 | 002 | N | n3 `NoteId="3.0"` | Refused | B0+F0 |
| MNS-008 | 002 | N | n3 `NoteId="0x3"` | Refused | B0+F0 |
| MNS-009 | 002 | N | n3 `NoteId=""` | Refused | B0+F0 |
| MNS-010 | 002, 009 | B | n3 `NoteId=" +7"` | Loads; saved n3 `NoteId="7"`; `NextId` 8 | B0+F0 |
| MNS-011 | 002 | U | n3 `NoteId=" 7 "` | Unresolved; the static reading is refused | B0+F0 |
| MNS-012 | 002 | N | n1 has `Velocity="85"` twice | Refused (malformed XML) | B0+F0 |
| MNS-013 | 001 | N | `<Foo />` after n2 inside key 36's `Notes` | Refused | B0+F0 |
| MNS-014 | 005, 016 | B | n1 `Velocity="0"`, n2 `Velocity="300"`, n3 `Velocity="0.5"` | Loads; saved Velocity `1`, `127`, `1` | B0+F0 |
| MNS-015 | 005 | B | n1 `OffVelocity="-5"`, n2 `OffVelocity="200"` | Saved OffVelocity `0`, `127` | B0+F0 |
| MNS-016 | 005, 004 | B | n1 `Probability="1.5"`, n2 `Probability="-1"` | Saved n1 has no `Probability`; n2 has `Probability="0"` | B0+F0 |
| MNS-017 | 005 | B | n1 `Duration="-2"`, n2 `Duration="Invalid"` | Saved `Duration="0"` for both | B0+F0 |
| MNS-018 | 005, 007 | B | n1 `Time="-3" VelocityDeviation="-500"` | Saved n1 `Time="-3"` and `VelocityDeviation="-500"` | B0+F0 |
| MNS-019 | 005, 016 | P | n1 `Velocity="80.578949"`, n2 `Velocity="33.3"` | Saved Velocity `80.578949`, `33.2999992` | B0+F0 |
| MNS-020 | 006, 016 | B | n1 `Time="0.123456789" Duration="0.3333333333"` | Saved n1 `Time="0.123456751581751581" Duration="0.333333333333333315"` | B0+F0 |
| MNS-021 | 006 | B | n1 `Time="-0.0000002"` | Saved n1 `Time="-0.000000260156510156510156"` | B0+F0 |
| MNS-022 | 006 | B | n1 `Time="0.00000013"`, n3 `Duration="0.000000131"` | Saved n1 `Time="0"`; n3 `Duration="0.000000260156510156510156"` | B0+F0 |
| MNS-023 | 006 | U | n1 `Time="-0.0000001"` | Rounds to negative zero; saved text unresolved | B0+F0 |
| MNS-024 | 006 | U | n2 `Time="Invalid"` | Not rounded; whether n2 is kept and its saved text unresolved | B0+F0 |
| MNS-025 | 007 | P | n2 `Time="20"` (outside the loop), n3 `Duration="0"` | Saved n2 `Time="20"`; n3 `Duration="0"` | B0+F0 |
| MNS-026 | 008 | N | n3 `NoteId="2"` (repeat in another key) | Refused | B0+F0 |
| MNS-027 | 008 | N | n2 `NoteId="1"` (repeat in the same key) | Refused | B0+F0 |
| MNS-028 | 009 | P | n2 `NoteId="0"` | Saved n2 `NoteId="4"`; `NextId` 5 | B0+F0 |
| MNS-029 | 009 | P | n1, n2 and n3 `NoteId="0"` | Saved NoteIds 4, 5, 6 for n1, n2, n3; `NextId` 7 | B0+F0 |
| MNS-030 | 009 | M | `NoteId` removed from n1, n2 and n3 | As MNS-029 | B0+F0 |
| MNS-031 | 009 | B | `NoteIdGenerator/NextId` `Value="1"` | Saved `NextId` 4 | B0+F0 |
| MNS-032 | 009 | B | `NoteIdGenerator/NextId` `Value="100"` | Saved `NextId` 100 | B0+F0 |
| MNS-033 | 009 | B | n1 to n3 `NoteId="0"`, `NextId` `Value="100"` | Saved NoteIds 100, 101, 102; `NextId` 103 | B0+F0 |
| MNS-034 | 009 | U | `NoteIdGenerator/NextId` `Value="-5"` | Unresolved (PRB-S7-10) | B0+F0 |
| MNS-035 | 010 | U | Key 36 lists n2 before n1 | Saved order unresolved (PRB-S7-06) | B0+F0 |
| MNS-036 | 010 | B | n1 `Duration="2"`, overlapping n2 | Loads (not refused); saved n1 and n2 unresolved (PRB-S7-06) | B0+F0 |
| MNS-037 | 011 | U | Key 38's MidiKey (a) `128`, (b) `-1`, (c) removed; (d) both KeyTracks `36` | Not graded; excluded; disposable session only (PRB-S7-05) | B0+F0 |
| MNS-038 | 012 | U | Both KeyTracks `Id="5"` | Load outcome and saved Ids unresolved | B0+F0 |
| MNS-039 | 013, 014, 016 | S | F1 unchanged | Loads; saved L1 with e1 `TimeOffset="0.0625" Value="100"` and e2 `TimeOffset="0.125" Value="-200"`, no curve attributes | B0+F1 |
| MNS-040 | 013, 016 | S | e1 adds `CurveControl1X="0.5" CurveControl1Y="0.2"` | Saved e1 has no `CurveControl1X` and has `CurveControl1Y="0.200000000000000011"` | B0+F1 |
| MNS-041 | 014 | N | Add a second list `NoteId="1" CC="-2"` with one event at 0.0625 | Refused | B0+F1 |
| MNS-042 | 014 | P | Add a list `NoteId="1" CC="74"` with one event `TimeOffset="0.0625" Value="64"` | Both lists saved | B0+F1 |
| MNS-043 | 014 | B | L1 `CC` set to (a) `0`, (b) `32`, (c) `120`, (d) `128`, (e) `129`, (f) `-3` | Loads; L1 not saved | B0+F1 |
| MNS-044 | 014 | B | L1 `CC` set to (a) `1`, (b) `119`, (c) `-1` | Loads; L1 saved with e1 `Value="100"` and e2 `Value="0"` | B0+F1 |
| MNS-045 | 014 | B | L1 `NoteId` set to (a) `0`, (b) `99` | Loads; L1 not saved | B0+F1 |
| MNS-046 | 014 | B | L1 `NoteId="99"`, plus a second list `NoteId="99" CC="-2"` | Refused (duplicate pair, although NoteId 99 names no note) | B0+F1 |
| MNS-047 | 014 | B | e1 `Value="9000"`, e2 `Value="-9000"` | Saved Value `8191`, `-8192` | B0+F1 |
| MNS-048 | 014 | B | L1 `CC="74"`, e1 `Value="200"`, e2 `Value="-1"` | Saved Value `127`, `0` | B0+F1 |
| MNS-049 | 014 | B | (a) e2 listed before e1; (b) a third event `TimeOffset="0.0625" Value="5"` after e2 | (a) saved e1, e2; (b) saved e1, the third event, then e2 | B0+F1 |
| MNS-050 | 014 | B | L1 `<Events />` | Loads; L1 not saved | B0+F1 |
| MNS-051 | 014 | B | (a) e2 `TimeOffset="Invalid"`; (b) e1 and e2 `TimeOffset="Invalid"` | (a) L1 saved with e1 only; (b) L1 not saved | B0+F1 |
| MNS-052 | 014, 009 | B | n2 `NoteId="0"`; add a list `NoteId="4" CC="-2"` with one event `TimeOffset="0.0625" Value="1"` | Loads; n2 saved with `NoteId="4"`; the added list not saved | B0+F1 |
| MNS-053 | 014 | U | (a) e1 `TimeOffset="0"`; (b) e2 `TimeOffset="0.25"` (equal to n1's Duration); (c) e2 `TimeOffset="0.5"`; (d) e1 `TimeOffset="-0.1"` | Unresolved (proposed PRB-S7-07 variants) | B0+F1 |
| MNS-054 | 015 | N | G: one group, `GroupId` 0, notes 1 and 2; group `NextId` 1 | Refused (blocked) | B0+F0+G |
| MNS-055 | 015 | N | G: one group, `GroupId` 5; group `NextId` 1 | Refused (blocked) | B0+F0+G |
| MNS-056 | 015 | N | G: two groups, `GroupId` 2 then 1; group `NextId` 3 | Refused (blocked) | B0+F0+G |
| MNS-057 | 015 | N | G: two groups, `GroupId` 1 then 1; group `NextId` 2 | Refused (blocked) | B0+F0+G |
| MNS-058 | 015 | P | G: one group, `GroupId` 1, notes 1 and 2; group `NextId` 2 | Loads (blocked); saved group text unresolved | B0+F0+G |
| MNS-059 | 015 | B | G: one group, `GroupId` 1, naming note 99; group `NextId` 2 | Loads (not refused; blocked); later effect unresolved | B0+F0+G |
| MNS-060 | 017 | U | MNS-026 | User-visible outcome unresolved (PRB-S7-02) | B0+F0 |

Cases marked unresolved or blocked must not be graded as passes. The omitted case kinds:

- **Cancellation and teardown.** Reading and writing notes has no cancellable step or resource
  in this scope.
- **Older versions.** Documents in older versions are excluded.

## Open questions

- [Q-018](../questions.md#q-018-midi-note-key-range-and-ordering-after-load) covers
  REQ-011, re-sorting after load (REQ-010), and list Ids and empty KeyTracks (REQ-012).
- **Refusal presentation** (REQ-017) is shared with REQ-ALS-CONTAINER-009.
- **New in this revision:** the adjustment of per-note lists with events at or outside the
  note's span (REQ-014, MNS-053). PRB-S7-07 needs the four MNS-053 variants added.
- **Probability groups:** the group XML shape and saved text (REQ-015, PRB-S7-08).
- **Negative values and other spellings:** negative ids and next ids, negative zero, and the
  integer spellings of REQ-002.
- **Assumptions:** A1 (PRB-S7-03 tests it) and A2 (PRB-S7-09).

The [probe batch](../../analysis/ableton-live-12.4.3/r2/s7-midi-notes-v1/probe-batch.json)
(PRB-S7-01 to 10) gives an input, a discriminating observation and a stop condition for each
probe. Its PRB-S7-02 variant B expectation needs the correction noted in the appendix.

## Analyst evidence appendix

Analysis-only. Do not copy into a handoff. The canonical evidence is
[MIDI note storage](../research/midi-note-storage.md), with retained run
`analysis/ableton-live-12.4.3/r2/s7-midi-notes-v1/` (dossier results s7-0001 to s7-0004,
`corpus-excerpts.jsonl`, `vtable-reads.txt`, `static-survey.json`). The image is
`Live.arm64`, SHA-256 `3a99ceea…d1c383cfad`, base `0x100000000`. ✓ marks a branch this
author re-read in the dossier disassembly while drafting.

Drafting added one query round, **d4-0001**, with dossiers `0x10292b9ec` and `0x10292c960`.
It sits in `/var/tmp/sound-analysis/query-spool-2/results/d4-0001/` and is not yet copied
into the retained run. File hashes:

| File | SHA-256 prefix |
| --- | --- |
| `0x10292b9ec.json` | `313210f3…` |
| `0x10292b9ec.c` | `98be02fc…` |
| `0x10292c960.json` | `306f1071…` |
| `0x10292c960.c` | `33cdeee5…` |
| `queries.json` | `535d6a5d…` |

| Requirement | Evidence (function entry, result) | Strength |
| --- | --- | --- |
| 001 | Schema `12.0_12402` and 1,252 12.x clips (`static-survey.json` `schema.segments`, `midinotes_child_orders`). MidiNotes registration `0x1028f3afc`; KeyTrack registration `0x1028ab80c`, `0x1028ab9f4` (s7-0004). Array loader `0x101560424` ✓ (s7-0001): `Class mismatch for array member` leads to the corrupt throw `0x10148229c` | D; save order S via the generic writer (n1) |
| 002 | Registration `0x1028e26c0` (s7-0004), flag 4. Text conversion `0x10152bfb8` (n1-0006). Int64 parser `0x101533e14` ✓ (s7-0004): leading-space scan, trailing-space count, optional `+`, converted length `min(len − start, end)` (the same computation as the transport-state integer parser, RV1-01), `< 0x40`, `+-` check, ASCII check, then a whole-span conversion `0x101524d8c`. Its failure is `Unexpected value for int64 node` | S; both-sides spaces and `-` U |
| 003 | Reset slot `+0xc8` = `0x1028e2fcc` ✓ (s7-0002) sets only VelocityDeviation 0, Probability 1, IsEnabled 1. Per-item sequence `0x101487284` ✓ (s7-0001) | S |
| 004 | Omit predicate `0x1028e2fe4` ✓ (s7-0001). Generic writer `0x101486cdc` (n1-0008). Array writer `0x101560258` (s7-0003). Copy-out `0x1028e2f90` (s7-0004) copies every field, so no state carries between written notes. Shipped: 12.4d1 attribute sets and `veldev_present_equal_0` / `probability_present_equal_1` only in older writers | S; corroborated |
| 005 | Post-load `0x1028e2c80` ✓ (s7-0001, disassembly). Duration: `fcmp d0,#0.0; fccmp d0,DBL_MAX,#4,pl; b.ne`, so a negative value or DBL_MAX is zeroed and NaN is kept. Velocity: `fcsel gt` then `fcsel mi`, NaN kept. OffVelocity and Probability: vector `fcmlt`/`fcmgt`/`bit`/`bic` against `0x105896fa8` = (127.0, 1.0). The Ghidra pseudocode wrongly shows NaN zeroed for Duration and set to 1 for Velocity; the disassembly governs. The flag `+0x2c` is inferred set for documents (A1) | S (A1) |
| 006 | Quantizer `0x1028e2e24` ✓ (s7-0001): `fcsel ge` sign, `fmadd` with h × 0.5, `fabs`, `fmul` by 3843840, `frintm`, `fdiv`, `fmul` sign. Sentinels `0x1055d9680` = (−1.7976931348623155e308, 1.7976931348623155e308, DBL_MAX, +inf) (`vtable-reads.txt`). Event quantizer `0x1025c7a0c` (s7-0003). Examples recomputed with a scratch script (not retained) and equal to PRB-S7-04 | S |
| 007 | `static-survey.json` `documents.checks`: `time_negative` 330, `time_before_loopstart` 45,068, `time_at_or_after_loopend` 52,740, `duration_nonpositive` 4 | D; meanings U |
| 008 | MidiNotes post-load `0x1028f5864` ✓ (s7-0001). Id collection `0x1028f6154` (s7-0002) skips 0 and sorts as unsigned 64-bit. Adjacent-equal scan, log `Note IDs are not unique in {}: {}{}`, throw `Note IDs are not unique` | S |
| 009 | Next-id raise `0x102920db4` (s7-0002): `max` by unsigned compare, argument 1 when there are no ids. Zero-id pass `0x1028f6664` (s7-0002) walks the KeyTrack list, then the array. Id allocation `0x1028db9b8` (s7-0003). The all-absent case needs only the constructor value 0 (`0x1028e2af4` ✓) and a reset that does not touch NoteId; it does not depend on the inheritance mechanism | S |
| 010 | No sort found after load (generic post-load `0x101486fa8` on KeyTrack and array). `documents.checks`: `keytracks_sorted_by_key` 1,368, `order_time_decreasing` 0, `order_time_equal` 0, `overlap_same_key` 261 | S (negative result) / D / U |
| 011 | Key-map store without a range check: `str x23,[x19,w0,SXTW #3]` in `0x1028f5f74` (s7-0003) and `0x1028f5420` (s7-0004). The map has 128 slots; the constructor sets MidiKey −1 | U, excluded |
| 012 | List writer `0x101468408` (pseudocode) writes the stored id. The reader's handling of `Id` was not traced. Empty-KeyTrack removal at the start of `0x1028f5864` is gated by global `DAT_106f54e20`+0x350 and `0x10185138c` | D / S / U |
| 013 | Event constructor `0x1025c77fc`, reset `0x1025c7b04`, omit predicate `0x1025c7b10` (s7-0004) | D / S |
| 014 | List post-load `0x10292b730` ✓ (s7-0002): `CC + 2 > 0x82` skip, `0x1011afdac`, DBL_MAX drop, clamp `0x1011afc18`/`0x1011afc2c` (−8192/8191 for −2, else 0/127), stable sort `0x1029307b8`. Store post-load `0x10292cd70` ✓ (s7-0002): erase when NoteId is 0 or CC is out of range or invalid; a (NoteId, CC) set size different from the list count throws `Multiple sets of per-note controller change events with the same note ID and CC number`. Orphans `0x1028f64d0` (s7-0003) use the pre-assignment id list. **New (d4-0001 ✓):** in `0x1028f5864` at `0x1028f5bec`–`0x1028f5c0c`, each note's NoteId and Duration go to `0x10292c960`. That function calls `0x10292b9ec` for each list of that NoteId, then removes lists whose event count is 0 (`0x10292caa4`, `0x10292cb58`). `0x10292b9ec` returns early when the list is empty, or when the first offset is > 0 (`fcmp; b.le`) and the last is < Duration (`b.mi`). Otherwise it builds an envelope (`0x1025c442c`, `0x1025c4708`) and calls vtable `+0x308` with the ranges [−1.7976931348623155e308, 0.0] (`0x105847020`, read with `read_consts.py`) and [rounded Duration, 1.7976931348623155e308]. That call's semantics were not traced. In the Chuck Sutton Intro demo, 3,204 of 5,491 non-empty lists start at an offset ≤ 0 and 1,012 end at or after the note's Duration (ad-hoc count, not retained) | S; boundary adjustment U |
| 015 | Group check `0x1028f5640` ✓ (s7-0002): id 0 or id ≤ previous (signed, starting at 0) fails. `0x102920ecc` (corpus) is `id < NextId` unsigned. Registration `0x1028f5770` (corpus) does not check the note. The failure throws `Note-group ids are corrupt.` | S; shape U |
| 016 | `0x10152205c` ✓ (s7-0001): Double `0x101520dbc`, Float `0x101520c70`, Int64 plain, Bool. Rule in REQ-TRANSPORT-STATE-011. `documents.checks` `fmt_ok` 2,054,618 | S; corroborated |
| 017 | Throws through `0x101488e64` and `0x10148229c`; the top-level catch was not traced | S / U |

**Excluded inheritance (static reading, not a requirement).** The array loader creates one
note object per KeyTrack and reuses it. The reset touches only three fields. So an omitted
Time, Duration, Velocity, OffVelocity or NoteId repeats the previous note of the same
KeyTrack, after that note's limits but before rounding. On the first note the omitted values
come from the constructor `0x1028e2af4` ✓: Time DBL_MAX (not rounded), Duration 0 (DBL_MAX,
then limited), Velocity and OffVelocity 127 (FLT_MAX, then limited) and NoteId 0. A NoteId
omitted after a non-zero id therefore duplicates it and makes the document refused. Per-note
events behave the same way: one object per list, and a reset of the curve controls only.
PRB-S7-01 and PRB-S7-02 test this reading.

**Corrections to the source packet:**

- **MN-23.** The research says "leading or trailing spaces … are accepted". Trailing spaces
  are accepted only with no leading space or `+`; spaces on both sides are U (REQ-002).
- **MN-20.** It says events "lacking TimeOffset" are dropped. Only an event whose TimeOffset
  is DBL_MAX is dropped, which for an omitted value is only the first event. The excluded
  inheritance applies to the others.
- **New step.** Neither MN-19 nor MN-20 records the boundary adjustment and empty-list
  removal (d4-0001).
- **PRB-S7-02 variant B.** It expects "NoteIds 1..n". With every NoteId removed from the 909
  file, whose `NextId` is 59, the static result is 59 to 99 in KeyTrack document order
  (keys 36, 38, 39, 44, 45, 46), then note order, with `NextId` 100.
- **PRB-S7-07.** It should add the MNS-053 variants.

**Dropped or downgraded from MN-01 to MN-24:**

- **MN-06** and MN-07's mute meaning become U.
- **MN-12** becomes an exclusion, apart from the all-absent NoteId case.
- **MN-16** is U and excluded.
- **MN-17** is S for sorted input only.
- **MN-18:** the meaning and preservation of Ids are U.
- **MN-19:** the TimeOffset origin is U.
- **MN-21:** the cases are blocked by the group shape.
- **MN-22** (version history) is not a requirement, because older documents are excluded.

## Revision and handoff

| Revision | Date | Change |
| --- | --- | --- |
| 1 | 2026-10-17 | First draft from packet S7 (MN-01 to MN-24) plus one verification round (d4-0001). 17 requirements: 4 without unknown parts (003, 004, 005, 008), 12 with D or S clauses and unknown parts, 1 unknown and excluded (011). 60 unexecuted cases: 45 gradable (MNS-036 in part), 6 blocked by the group shape, 9 unresolved |

Before the 2026-10-18 review, a first release candidate could
contain the gradable cases of REQ-002 to 009, REQ-014 and REQ-016, under assumptions A1
and A2.

Released 2026-10-18: [midi-note-storage-v1](../../handoff/midi-note-storage-v1/README.md), 67 cases, approved with narrowing by a separate review agent (partial REQ-001 to 010, 013, 014, 016 only; 011, 012, 015, 017 unreleased). The review findings to apply in the next revision are on the [handoff plan](midi-note-storage-handoff-plan.md#review-outcome). This revision's text is unchanged.
