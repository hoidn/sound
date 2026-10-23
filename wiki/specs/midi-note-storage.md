---
id: SPEC-MIDI-NOTE-STORAGE
type: spec
status: draft
revision: 6
updated: 2026-10-20
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
supported by a static derivation, settled by extracted execution, or explicitly unknown. Nothing
was run against Live.
[ADR 0002](../decisions/adr-0002-static-first-analysis.md) permits a static-first draft. Under
[ADR 0003](../decisions/adr-0003-no-reference-execution.md) nothing will be run against Live:
no reference observation is available, so a U clause is settled only by a static route, by
extracted execution of the shipped x86_64 code, or stays U. Revision 3 adds the X results of
packet X2 for the value limits, the time grid and the saved number text (appendix).
The target is documents with `MinorVersion="12.0_12402"`. The gzip and XML envelope belongs
to [SPEC-ALS-CONTAINER](als-container.md). Value text follows
[SPEC-TRANSPORT-STATE](transport-state.md) REQ-003, 004, 005 and 011. Both are dependencies.
All examples are fragments of decoded XML.

## Evidence labels

| Label | Meaning |
| --- | --- |
| D | Documented: present in the shipped schema for `12.0_12402` or in shipped documents. Those documents were written by 12.4d1 or older, not by 12.4.3 |
| S | Static derivation from the 12.4.3 executable; not an observed run |
| X | Extracted execution: the shipped x86_64 function was run on the stated inputs in the harness of [ADR 0003](../decisions/adr-0003-no-reference-execution.md#extracted-execution-of-original-code). It shows what the function computes, not that Live reaches it with those inputs; the path is S and is stated. The arm64 release slice is matched by static comparison (appendix) |
| U | Unknown; no expected result. A PRB ID names the Phase 4 probe that would have settled it. No probe will run (ADR 0003); where a static route could still settle a clause, the clause names it |

Only D, S and X clauses may enter a release. U clauses block the behavior they name.

Static clauses rest on these assumptions. A1 is now established statically. A2 and A3 remain
stated assumptions, which the review accepted as such (RVN-11):

| ID | Assumption | Affects |
| --- | --- | --- |
| A1 | **Established statically** (review RVN-01). Every step applied after an item's text is read runs when a Live Set is opened: the value limits (REQ-005), the NoteId check, the next-id raise and numbering (REQ-008, 009), the per-note list rules (REQ-014) and the group check (REQ-015). One load-context flag gates them all. Every context constructor sets it, and only undo-history streams clear it. For a clip file the same survey applies, but that read path was not traced. The defaults (REQ-003) and the time grid (REQ-006) are not gated. Revision 1 called A1 inferred and tied it to REQ-005 only | REQ-005, 008, 009, 014, 015 |
| A2 | Opening the document and saving it without other changes does not itself change the notes, their ids or the clip's next id. This covers the draft's procedure (a loaded clip file placed into a set, then the set saved) and the release's (an authored set opened, then saved). Not traced. No reference observation is available (ADR 0003), and no static route short of tracing every path between load and save is known | Every case that compares saved values |
| A3 | `MidiKey`, `CC` and the `Id` attributes are read by the integer parser of Int fields, the parser of REQ-TRANSPORT-STATE-006. A per-note list's `NoteId` is read by the Int64 parser of REQ-002. Inferred from the schema types and the type dispatch of the text conversion; not traced per field | REQ-002 (other integer fields); every case, since each reads `MidiKey` |

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
  - 64-bit values follow REQ-TRANSPORT-STATE-004. The text `Invalid` reads as the largest
    finite value 1.7976931348623157e308; MNS-017 and MNS-051 rely on it;
  - 32-bit values follow the 32-bit form of REQ-TRANSPORT-STATE-005;
  - `IsEnabled` follows REQ-TRANSPORT-STATE-003: exactly `true` or `1` for true, and `false`
    or `0` for false. Any other text makes the document refused.
- **X (glibc text conversion; arm64 library behavior inferred).** In `Time`, `Duration`,
  `Velocity`, `OffVelocity` and `Probability`, `-0` reads as negative zero before REQ-005
  and REQ-006 normalize it. Negative zero in `VelocityDeviation`, a per-note event's
  `TimeOffset` or `Value`, and curve controls has no expectation in this draft.
- **S.** Integer text (`NoteId`, both `NextId` values and the group id of REQ-015) is accepted
  in these forms only:
  - ASCII decimal digits after any number of U+0020 spaces and then at most one `+`
    (`7`, ` 7`, `+7`, ` +7`);
  - digits followed only by spaces, when nothing precedes the digits (`7 `).

  After the leading spaces and sign, the part up to the last digit must be at most 63
  characters, counting leading zeros. The value must be at most 9,223,372,036,854,775,807,
  the largest signed 64-bit integer.
- **S.** Any other integer text makes the document refused. This includes an empty or
  all-space value, `7.0`, `0x10`, `+-7`, a non-ASCII byte, 64 digits and a value above the
  maximum, such as `9223372036854775808`.
- **S.** A repeated attribute is malformed XML, and the document is refused.
- **S (A3).** `MidiKey`, `CC` and the `Id` attributes of KeyTracks and per-note lists have the
  schema type `Int`. A per-note list's `NoteId` has the type `Int64`. Plain decimal text reads
  as its value: `0`, or ASCII digits without a leading zero. `CC` text may also start with one
  `-` (`-2`, `-1`, `-3`).
- **U.** These integer spellings are unknown:
  - spaces on both sides of the digits, or a `+` with trailing spaces (` 7 `, `+7 `).
    The static reading is refused;
  - a `-` sign (see Exclusions);
  - any other spelling of `MidiKey`, `CC`, a list's `NoteId` or an `Id`, such as spaces, a
    `+`, leading zeros, or a `-` outside `CC`.
- **S (conditional local reader).** For the existing n3 `NoteId=" 7 "` input of
  MNS-011, the selected Int64 reader refuses the value when invoked on that field's
  stored text. This is the bounded local comparison MNS-076, under the current
  field/parser and ordinary-reader premises (A3 where applicable). It does not settle
  MNS-011's public-load outcome, catch, remaining state or saved result. The U spelling
  list above retains that broader scope; no additional spelling case is adopted.

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

- **X (path S, A1 established).** After a note's attributes are read:
  - `Velocity` below 1 becomes 1, and above 127 becomes 127;
  - `OffVelocity` below 0 becomes 0, and above 127 becomes 127;
  - `Probability` below 0 becomes 0, and above 1 becomes 1;
  - a `Duration` below 0, or equal to the largest finite 64-bit value, becomes 0.

  A value set to 0 by these rules is positive zero. These values do not make the document
  refused (S). The limits are exact at the bounds: binary32 127.00000762939453 (text
  `127.00001`) becomes 127, and 0.9999999403953552 (text `0.99999994`) becomes 1.
- **X.** Negative zero: a `Velocity` of −0 becomes 1. An `OffVelocity` or `Probability` of −0 is
  kept as −0, and a `Duration` of −0 is kept by this step and becomes +0 in REQ-006.
- **X.** `Time`, `VelocityDeviation` and `NoteId` are not range-checked. A negative `Time` is
  kept.
- **X.** A fractional `Velocity` is kept, for example 80.578949.
- Excluded: NaN and infinite values. (X, for the record only: NaN is kept by every rule; an
  infinite `Velocity`, `OffVelocity` or `Probability` is limited like a finite value; a `Duration`
  of −∞ becomes 0 and one of +∞ is kept.)

### REQ-MIDI-NOTE-STORAGE-006 — time grid

- **X (path S).** On load, each note's `Time` and `Duration` (after REQ-005) and each per-note
  event's `TimeOffset` are rounded to a grid of 1/3,843,840 beat, half away from zero. In binary64
  arithmetic, with each operation rounded:
  - let h = 2.6015651015651016e-07 (the binary64 value of 1/3,843,840);
  - let s = +1 when x ≥ 0 (including −0), else −1;
  - the stored value is s × (⌊|x + s × h/2| × 3,843,840⌋ / 3,843,840).

  The formula, not exact rounding, defines the result next to a halfway point. A value one
  binary64 step below the nearest binary64 value to h/2, 1.3007825507825505e-07 (text
  `0.00000013007825507825505`), is stored as h; exact halves-away rounding would give 0.
  Of 70 values within three binary64 steps of a halfway point, 12 differ in this way (X).
- **X.** These values are not rounded: ±1.7976931348623155e308, the largest finite value
  1.7976931348623157e308 (text `Invalid`), and +∞.
- **X.** A `Time` or `Duration` of −0 is stored as +0. A value that rounds to zero from below,
  such as −0.0000001, is stored as −0.
- **S.** Values already on the grid are unchanged except negative zero; every other
  on-grid value run was unchanged (X). Every shipped value is on the grid.
- **X.** Examples:

  | Input | Stored and saved |
  | --- | --- |
  | 0.123456789 | `0.123456751581751581` |
  | 0.3333333333 | `0.333333333333333315` |
  | −0.0000002 | `-0.000000260156510156510156` (−1/3,843,840) |
  | 0.00000013 | `0` |
  | 0.000000131 | `0.000000260156510156510156` |
  | −0.0000001 | `-0` (negative zero, REQ-016) |
  | 0.00000013007825507825505 | `0.000000260156510156510156` |

- **U.** What a note whose time was not rounded does after load, including whether it is
  kept.

### REQ-MIDI-NOTE-STORAGE-007 — time coordinates and value domains

- **D.** In shipped documents:
  - `Time` runs from −1/3,843,840 to 352, and `Duration` from 0 to 80;
  - `Velocity` runs from 1 to 127, often fractional;
  - `OffVelocity` takes integers 0 to 127, and `Probability` values 0 to 1;
  - 12.4d1 wrote `IsEnabled` only as `false`, and `VelocityDeviation` only as `3`;
  - notes before the clip's loop start and at or after its loop end are stored.
- **S.** A note outside the clip's loop region, and a note with `Duration` positive zero,
  is retained on load and save, subject to REQ-005 and REQ-006. A `Duration` of negative
  zero becomes positive zero (REQ-006).
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
- **S.** Then each note with NoteId 0 receives N, and N increases by 1 after each. For a clip
  whose KeyTracks are stored in ascending key order, the KeyTracks are taken in that stored
  order, and the notes of each KeyTrack in document order.
- **S.** A save writes every note's NoteId and the final N as `NoteIdGenerator/NextId`.
- **S.** When `NoteId` is absent from every note of the clip, every note counts as NoteId 0
  and is numbered as above.
- **U.** The next id when `NoteIdGenerator` is missing, and the numbering order for KeyTracks
  not stored in ascending key order (REQ-010).
- Excluded: a negative next id, which the reference compares as unsigned.

### REQ-MIDI-NOTE-STORAGE-010 — note and KeyTrack order

- **S.** Take a clip whose KeyTracks are in ascending key order and whose notes in each
  KeyTrack are in strictly ascending `Time` order after rounding, with no note starting before
  the previous note of its key ends. Load and save keep both orders. No load step reorders
  notes or KeyTracks.
- **S.** Notes of one key that overlap in time, or that share a `Time`, do not make the
  document refused.
- **D.** Every shipped clip has ascending key order and strictly ascending times within each
  key. 261 shipped notes start before the previous note on the same key ends.
- **U.** These outcomes are unknown. No reference observation is available (ADR 0003). A
  static search of the paths after load for a sort could narrow the first:
  - whether notes or KeyTracks stored out of order are re-sorted before a later save;
  - whether overlapping notes are kept, trimmed or merged after load, and how they play.

### REQ-MIDI-NOTE-STORAGE-011 — MIDI key range and duplicate keys

- **U, excluded.** Three inputs are unknown and excluded:
  - a `MidiKey` value outside 0 to 127;
  - a KeyTrack without `MidiKey`;
  - two KeyTracks with the same key.

  The reference handles them without a range or duplicate check, so the outcome may be
  memory corruption rather than defined behavior. No reference outcome may be treated as
  required. See [Q-018](../questions.md#q-018-midi-note-key-range-and-ordering-after-load).
  No reference observation is available (ADR 0003).
- **S (both slices, X for the getter).** Revision 3 traced the route this clause named. The
  `MidiKey` getter returns the stored value unchanged (X: 128, 129, −1 and −5 are returned as
  stored). Both key-map stores in both slices then write at map slot 8 × key with a sign-extended
  index and no bound check. The 128-slot map ends just before the object's KeyTrack list
  pointer, so key 129 overwrites that pointer, and −5 the object's vtable pointer. No range
  guard exists on the load path, so the exclusion is permanent: these inputs have no defined
  reference behavior.

### REQ-MIDI-NOTE-STORAGE-012 — list ids and empty KeyTracks

- **D.** Shipped KeyTrack `Id`s are unique within a clip and need not follow key order. They
  are ascending in 719 of 1,368 clips. Per-note lists also carry an `Id`.
- **S.** A save writes an `Id` attribute on each KeyTrack and each per-note list.
- **U.** These are unknown. No reference observation is available (ADR 0003). The static
  routes are the reader's handling of `Id` and the gate of the empty-KeyTrack removal
  (appendix):
  - the meaning of these Ids;
  - whether loaded Ids are written back unchanged;
  - how repeated Ids are read;
  - whether an empty KeyTrack is kept or removed on load. The reference removes empty
    KeyTracks under a condition that was not traced. 12.4d1 saves contain 267 empty
    KeyTracks.
- **S (conditional local reader).** In the current registered KeyTrack-list class and
  ordinary generic-list reader context, two KeyTracks whose parsed `Id` is 5 cause a
  duplicate-id read refusal before the duplicate item is constructed or read. This
  reuses MNS-038's input in the separate local comparison MNS-077; A3 remains the
  integer-field premise. It establishes neither a public whole-Set/clip rejection nor
  Id meaning, saved Id preservation, rollback or the empty-KeyTrack condition. Those
  broader questions and the original MNS-038 expectation remain U.

### REQ-MIDI-NOTE-STORAGE-013 — per-note expression structure

- **D.** `PerNoteEventStore/EventLists` holds `PerNoteEventList` elements.
  - Each list has the attributes `Id`, `NoteId` and `CC`, and an `Events` child holding
    `PerNoteEvent` elements.
  - An event has `TimeOffset` (64-bit) and `Value` (32-bit). It may also have
    `CurveControl1X`, `CurveControl1Y`, `CurveControl2X` and `CurveControl2Y` (64-bit).
  - Shipped `CC` values are −2, −1 and 74.
- **S.** Event value text follows REQ-002: `TimeOffset` and the curve controls as 64-bit
  values, `Value` as a 32-bit value. A `TimeOffset` of `Invalid` reads as the largest finite
  value.
- **S.** An omitted curve control loads as 0.5, independently for each event.
- **S.** On save, a curve control equal to 0.5 is omitted. `TimeOffset` and `Value` are always
  written. `TimeOffset` is rounded on load (REQ-006).
- **U.** These meanings are inferred:
  - that `TimeOffset` is measured from the note's start;
  - that CC −2 is per-note pitch bend in 14-bit units, −1 is per-note pressure and 74 is
    slide.
- **U.** The saved order of per-note lists and the attribute order of a saved event. Neither
  is compared.
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
  that adjustment. Shipped lists often start at offset 0, so this gap matters. No reference
  observation is available (ADR 0003). The reviewed retained-source route now narrows
  the conditional adapter receiver, its boundary-call thunk and the following body
  (appendix). The downstream event-array operations and transaction effects remain
  untraced. All four MNS-053 variants remain U; this frontier refinement supplies no
  resulting event list or new resolved indirect-site credit.

### REQ-MIDI-NOTE-STORAGE-015 — probability groups

- **D.** The schema defines `NoteProbabilityGroups` as a list of groups. Each group has a
  group type, a list of note ids, a probability and a 64-bit `GroupId`. The group generator
  holds `NextId`. No shipped document in the retained survey contains a group.
- **S (registered-class route).** A group is a `NoteProbabilityGroup` list item with its
  own `Id` attribute. Its children, in order, are `GroupType`, `Notes`, `Probability` and
  `GroupId`. `GroupId` is a child with a `Value` attribute, not an attribute of the group.
  `GroupType` and `Probability` have `Value` attributes. The group's `Notes` array contains
  `NoteId` elements, each with a `NoteId` attribute holding the note's integer id.
  The group's list `Id` is distinct from `GroupId`. Fragment G supplies the concrete form.
  This is a conditional static derivation through the registered constructors and generic
  loader/writer/array translator, not an observed open/save or proof of final saved state.
- **S (code/label association).** The group enum associates indices 0 and 1 with the
  internal labels `PlayAll` and `PlayOne`, respectively. Construction selects 0 and
  probability 1. The cases use these constructor choices; this does not establish their
  playback meaning, UI names or admission of other enum values.
- **S.** When the clip has at least one group, the groups are checked in document order. Each
  `GroupId` must be greater than 0 and greater than the previous group's id. Each must also
  be below the group generator's `NextId`, compared as unsigned values. Otherwise the
  document is refused. This retains the established A1 load-context premise.
- **S.** A group's note ids are not checked against the clip's notes in the selected
  registration path. A group naming a missing note does not itself cause that path to
  refuse the document. Later listeners, playback and public lifecycle effects remain U.
- **U.** No reference observation is available (ADR 0003). These remain unknown:
  - what a group naming a missing note does after load;
  - the final saved group text, including default omission and normalized values;
  - whether the group generator's `NextId` is raised anywhere across the complete load path;
  - unsupported enum values and the playback meaning of the code/label associations.

  Revision 5 supplies a conditional group shape for all six existing group cases.
  Their reader admission/refusal expectations are static derivations under A1; saved
  group state, later effects and actual public/candidate execution are not graded.

### REQ-MIDI-NOTE-STORAGE-016 — number and Boolean text on save

- **S.** Values are written as held after REQ-005, REQ-006 and REQ-014. The writer does not
  round again.
- **S.** Number text follows REQ-TRANSPORT-STATE-011:
  - `Time`, `Duration`, `TimeOffset` and the curve controls use the 64-bit rule;
  - `Velocity`, `VelocityDeviation`, `OffVelocity`, `Probability` and `Value` use the 32-bit
    rule;
  - `NoteId`, `NextId`, `CC`, `Id` and `GroupId` are plain decimal integers;
  - `IsEnabled` is written `false` (true is omitted, REQ-004).
- **D.** All 2,054,618 shipped note and event numbers agree with this rule, for example
  `Time="0.359923670079920099"`.
- **X (path S).** Examples, from the writers run on the held values:

  | Value | Saved text |
  | --- | --- |
  | Time 0.1 | `0.100000000000000006` |
  | Velocity 33.3 | `33.2999992` |
  | Velocity 80.578949 | `80.578949` |
  | Curve control 0.2 | `0.200000000000000011` |
  | 64-bit or 32-bit −0 | `-0` |

- **S (both slices).** The largest finite 64-bit or 32-bit value is written `Invalid`, and a
  non-finite value as `#` with 16 or 8 hexadecimal digits, without the number rule.

### REQ-MIDI-NOTE-STORAGE-017 — refusal presentation

- **S.** The refusals of REQ-001, 002, 008, 014 and 015 are raised as corrupt-document read
  errors that carry a detail text.
- **U.** What the user sees is unknown, including whether the detail is shown, as for
  REQ-ALS-CONTAINER-009. It is also unknown whether the whole set or clip file is rejected or
  only the clip is dropped, and what remains loaded. No reference observation is available
  (ADR 0003). A static trace of the top-level catch, shared with REQ-ALS-CONTAINER-009, could
  settle part of it.

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

**Procedure.** This was the common procedure of the S7 probe batch. Under ADR 0003 it will
not be run; it defines what a saved comparison means:

1. Start with fresh preferences.
2. Drag the file into an empty MIDI track.
3. Save as a new set.
4. Compare the clip's `Notes` element in the saved set.

The release builds each case instead as an authored Live Set. Its one MIDI track has a first
session clip that loops from 0 to 8 and holds the case fragment. The set is opened and then
saved. Review RVN-12 accepted this because shipped content cannot travel. Under A2 the
expected results are the same for both constructions.

**Comparators.** Attribute values are compared as exact text. Not compared: KeyTrack and list
`Id` values (REQ-012), the content of `NoteProbabilityGroups` and the group generator's
`NextId` (REQ-015), and the order of per-note lists and of an event's attributes (REQ-013).
Assumption A2 applies to every saved comparison.

**Separate local comparisons (MNS-076/077).** Supply the decoded F0 `Notes` domain
input with the exact edits already authored in MNS-011/038. Compare only a
`local_reader_outcome` of `refused` for the conditional clause named in the row.
This field is a project comparison projection of the decoded Notes contract; it
requires no separate public validation API, native call or implementation pipeline.
An independent implementation may validate at any suitable point. No fixture is
created by this revision, and no public Open/Save procedure is run. These two rows
assess neither user-visible errors, whole-Set/clip rejection, loaded state, rollback
nor saved text. They do not change the original public U cases.

The current registered-class and ordinary-reader associations remain conditional;
A3 remains explicit. A1 concerns the post-read checks and supplies no public catch
or lifecycle proof for these read-phase refusals. A2 remains the separate same-state
Save assumption and supplies no saved result here. The old rows and released v3
retain their existing scopes.

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

**Fragment G.** The probability-group cases replace F0's `<NoteProbabilityGroups />` with
this registered-class shape. This is the positive MNS-058 group; the table changes GroupId,
order, note ids and group `NextId` for the other five cases. All use GroupType 0 and
Probability 1. List Ids are 0, then 1 when a second group is present, independently of
GroupId. The fully materialized [six Notes fragments](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-midi-probability-groups-v1/case-proposals.json)
preserve the same F0 notes and note counter. They are used under B0/F0, not as complete Sets.

```xml
<NoteProbabilityGroups>
  <NoteProbabilityGroup Id="0">
    <GroupType Value="0" />
    <Notes><NoteId NoteId="1" /><NoteId NoteId="2" /></Notes>
    <Probability Value="1" />
    <GroupId Value="1" />
  </NoteProbabilityGroup>
</NoteProbabilityGroups>
<ProbabilityGroupIdGenerator><NextId Value="2" /></ProbabilityGroupIdGenerator>
```

The 054–057 refusal cases use notes 1 and 2 in each group. MNS-059 alone names missing
note 99. Conditional static shape and local registration do not establish final Save,
missing-note playback effects or the absence of all group-counter repair.

**Case kinds.** P positive, N negative (refused), B boundary, M missing input, S save text,
U unresolved. Expected results are static derivations, shipped-document facts or, for the
value limits, the time grid and the number text, X results of the original x86_64 functions
(appendix, "Cases backed by X"). No case has been run against Live, and none will be
(ADR 0003). Unless stated otherwise, the other values are unchanged from F0 or F1.

| Case ID | Requirement | Kind | Setup (edit of F0 or F1) | Expected result | Fixture |
| --- | --- | --- | --- | --- | --- |
| MNS-001 | 001, 004, 010, 016 | S | F0 unchanged | Loads. The saved `Notes` equals F0 apart from Ids, `NoteProbabilityGroups` and the group generator: KeyTracks 36 then 38, the same note order and attribute text, `NextId` 4 | B0+F0 |
| MNS-002 | 003, 004 | P | n1 adds `VelocityDeviation="0" Probability="1" IsEnabled="true"` | Saved n1 has none of these three attributes | B0+F0 |
| MNS-003 | 003, 004, 016 | S | n1 adds `VelocityDeviation="3" Probability="0.5" IsEnabled="false"` | Saved n1 is exactly `Time="0" Duration="0.25" Velocity="85" VelocityDeviation="3" OffVelocity="64" Probability="0.5" IsEnabled="false" NoteId="1"`; saved n2 unchanged, with none of these three attributes | B0+F0 |
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
| MNS-017 | 002, 005 | B | n1 `Duration="-2"`, n2 `Duration="Invalid"` | Saved `Duration="0"` for both | B0+F0 |
| MNS-018 | 005, 007 | B | n1 `Time="-3" VelocityDeviation="-500"` | Saved n1 `Time="-3"` and `VelocityDeviation="-500"` | B0+F0 |
| MNS-019 | 005, 016 | P | n1 `Velocity="80.578949"`, n2 `Velocity="33.3"` | Saved Velocity `80.578949`, `33.2999992` | B0+F0 |
| MNS-020 | 006, 016 | B | n1 `Time="0.123456789" Duration="0.3333333333"` | Saved n1 `Time="0.123456751581751581" Duration="0.333333333333333315"` | B0+F0 |
| MNS-021 | 006 | B | n1 `Time="-0.0000002"` | Saved n1 `Time="-0.000000260156510156510156"` | B0+F0 |
| MNS-022 | 006 | B | n1 `Time="0.00000013"`, n3 `Duration="0.000000131"` | Saved n1 `Time="0"`; n3 `Duration="0.000000260156510156510156"` | B0+F0 |
| MNS-023 | 006, 016 | B | n1 `Time="-0.0000001"` | Saved n1 `Time="-0"` | B0+F0 |
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
| MNS-034 | 009 | U | `NoteIdGenerator/NextId` `Value="-5"` | Unresolved; a negative next id is excluded (REQ-009) | B0+F0 |
| MNS-035 | 010 | U | Key 36 lists n2 before n1 | Saved order unresolved; no reference observation (ADR 0003) | B0+F0 |
| MNS-036 | 010 | B | n1 `Duration="2"`, overlapping n2 | Loads (not refused); saved n1 and n2 unresolved; no reference observation (ADR 0003) | B0+F0 |
| MNS-037 | 011 | U | Key 38's MidiKey (a) `128`, (b) `-1`, (c) removed; (d) both KeyTracks `36` | Not graded; excluded; no reference observation (ADR 0003) | B0+F0 |
| MNS-038 | 012 | U | Both KeyTracks `Id="5"` | Load outcome and saved Ids unresolved | B0+F0 |
| MNS-039 | 013, 014, 016 | S | F1 unchanged | Loads; saved L1 with e1 `TimeOffset="0.0625" Value="100"` and e2 `TimeOffset="0.125" Value="-200"`, no curve attributes | B0+F1 |
| MNS-040 | 013, 016 | S | e1 adds `CurveControl1X="0.5" CurveControl1Y="0.2"` | Saved e1 has no `CurveControl1X` and has `CurveControl1Y="0.200000000000000011"` | B0+F1 |
| MNS-041 | 014 | N | Add a second list `NoteId="1" CC="-2"` with one event `TimeOffset="0.0625" Value="1"` | Refused | B0+F1 |
| MNS-042 | 014 | P | Add a list `NoteId="1" CC="74"` with one event `TimeOffset="0.0625" Value="64"` | Both lists saved | B0+F1 |
| MNS-043 | 014 | B | L1 `CC` set to (a) `0`, (b) `32`, (c) `120`, (d) `128`, (e) `129`, (f) `-3` | Loads; L1 not saved | B0+F1 |
| MNS-044 | 014 | B | L1 `CC` set to (a) `1`, (b) `119`, (c) `-1` | Loads; L1 saved with e1 `Value="100"` and e2 `Value="0"` | B0+F1 |
| MNS-045 | 014 | B | L1 `NoteId` set to (a) `0`, (b) `99` | Loads; L1 not saved | B0+F1 |
| MNS-046 | 014 | B | L1 `NoteId="99"`, plus a second list `NoteId="99" CC="-2"` with one event `TimeOffset="0.0625" Value="1"` | Refused (duplicate pair, although NoteId 99 names no note) | B0+F1 |
| MNS-047 | 014 | B | e1 `Value="9000"`, e2 `Value="-9000"` | Saved Value `8191`, `-8192` | B0+F1 |
| MNS-048 | 014 | B | L1 `CC="74"`, e1 `Value="200"`, e2 `Value="-1"` | Saved Value `127`, `0` | B0+F1 |
| MNS-049 | 014 | B | (a) e2 listed before e1; (b) a third event `TimeOffset="0.0625" Value="5"` after e2 | (a) saved e1, e2; (b) saved e1, the third event, then e2 | B0+F1 |
| MNS-050 | 014 | B | L1 `<Events />` | Loads; L1 not saved | B0+F1 |
| MNS-051 | 002, 014 | B | (a) e2 `TimeOffset="Invalid"`; (b) e1 and e2 `TimeOffset="Invalid"` | (a) L1 saved with e1 only; (b) L1 not saved | B0+F1 |
| MNS-052 | 014, 009 | B | n2 `NoteId="0"`; add a list `NoteId="4" CC="-2"` with one event `TimeOffset="0.0625" Value="1"` | Loads; n2 saved with `NoteId="4"`; the added list not saved | B0+F1 |
| MNS-053 | 014 | U | (a) e1 `TimeOffset="0"`; (b) e2 `TimeOffset="0.25"` (equal to n1's Duration); (c) e2 `TimeOffset="0.5"`; (d) e1 `TimeOffset="-0.1"` | Unresolved; no reference observation (ADR 0003); static route in REQ-014 | B0+F1 |
| MNS-054 | 015 | N | G: one group, `GroupId` 0, notes 1 and 2; group `NextId` 1 | Refused (S, A1) | B0+F0+G |
| MNS-055 | 015 | N | G: one group, `GroupId` 5; group `NextId` 1 | Refused (S, A1) | B0+F0+G |
| MNS-056 | 015 | N | G: two groups, `GroupId` 2 then 1; group `NextId` 3 | Refused (S, A1) | B0+F0+G |
| MNS-057 | 015 | N | G: two groups, `GroupId` 1 then 1; group `NextId` 2 | Refused (S, A1) | B0+F0+G |
| MNS-058 | 015 | P | G: one group, `GroupId` 1, notes 1 and 2; group `NextId` 2 | Loads (S, A1); saved group text U | B0+F0+G |
| MNS-059 | 015 | B | G: one group, `GroupId` 1, naming note 99; group `NextId` 2 | Loads (S, A1; no missing-note refusal); later effect U | B0+F0+G |
| MNS-060 | 017 | U | MNS-026 | User-visible outcome unresolved; no reference observation (ADR 0003) | B0+F0 |
| MNS-061 | 002 | P | n1 `NoteId=" 1"`, n2 `NoteId="+2"`, n3 `NoteId="3 "` | Loads; saved NoteIds `1`, `2`, `3`; `NextId` 4 | B0+F0 |
| MNS-062 | 002 | N | n3 `NoteId="+-3"` | Refused | B0+F0 |
| MNS-063 | 002 | N | n3 `NoteId` of three spaces | Refused | B0+F0 |
| MNS-064 | 002 | N | n3 `NoteId="３"` (U+FF13, a fullwidth digit) | Refused | B0+F0 |
| MNS-065 | 002 | N | n3 `NoteId` of 64 digits: 63 zeros, then `3` | Refused | B0+F0 |
| MNS-066 | 002 | N | n3 `NoteId="9223372036854775808"` (2^63) | Refused | B0+F0 |
| MNS-067 | 002, 016 | B | n3 `Time=" 0.5abc"` | Loads; saved n3 `Time="0.5"` | B0+F0 |
| MNS-068 | 002 | N | n1 `Velocity="abc"` | Refused | B0+F0 |
| MNS-069 | 006, 013, 016 | B | e1 `TimeOffset="0.123456789"` | Saved e1 `TimeOffset="0.123456751581751581"`, before e2 | B0+F1 |
| MNS-070 | 010 | B | n2 `Time="0"`, the same Time as n1 | Loads (not refused); saved n1 and n2 unresolved; no reference observation (ADR 0003) | B0+F0 |
| MNS-071 | 014 | B | L1 `CC` set to (a) `31`, (b) `33` | Loads; L1 saved with e1 `Value="100"` and e2 `Value="0"` | B0+F1 |
| MNS-072 | 002, 006, 016 | B | n1 `Time="0.00000013007825507825505"` (one binary64 step below the nearest value to h/2) | Saved n1 `Time="0.000000260156510156510156"` (exact halves-away rounding would give `0`) | B0+F0 |
| MNS-073 | 002, 004, 005, 016 | B | n1 `OffVelocity="-0"`, n2 `Probability="-0"` | Saved n1 `OffVelocity="-0"`; saved n2 `Probability="-0"` | B0+F0 |
| MNS-074 | 002, 005, 006, 016 | B | n1 `Velocity="-0"`, n2 `Duration="-0"`, n3 `Time="-0"` | Saved n1 `Velocity="1"`, n2 `Duration="0"`, n3 `Time="0"` | B0+F0 |
| MNS-075 | 002, 005, 016 | B | n1 `Velocity="127.00001"`, n2 `Velocity="0.99999994"` | Saved Velocity `127`, `1` | B0+F0 |
| MNS-076 | 002 | N | n3 `NoteId=" 7 "` (same edit as MNS-011; local comparison only) | Local reader refused (S, conditional field/ordinary-reader premises); public load and saved state U | F0 domain input; no new fixture |
| MNS-077 | 012 | N | Both KeyTracks `Id="5"` (same edit as MNS-038; local comparison only) | Local reader refused (S, conditional class/ordinary-reader premises, A3); public load and saved Ids U | F0 domain input; no new fixture |

Cases marked unresolved or blocked must not be graded as passes. The omitted case kinds:

- **Cancellation and teardown.** Reading and writing notes has no cancellable step or resource
  in this scope.
- **Older versions.** Documents in older versions are excluded.

## Open questions

- [Q-018](../questions.md#q-018-midi-note-key-range-and-ordering-after-load) covers
  REQ-011, re-sorting after load (REQ-010), and list Ids and empty KeyTracks (REQ-012).
- **Refusal presentation** (REQ-017) is shared with REQ-ALS-CONTAINER-009.
- **Per-note lists at the note's edges:** the untraced adjustment of lists with events at or
  outside the note's span (REQ-014, MNS-053).
- **Probability groups:** the group XML shape and saved text (REQ-015).
- **Negative values and other spellings:** negative ids and next ids, and the integer spellings
  of REQ-002. Negative zero is settled in revision 3 (REQ-005, 006, 016).
- **Assumptions:** A1 is established statically (review RVN-01). A2 and A3 remain stated
  assumptions.

No reference observation will settle any of these (ADR 0003). Each stays U unless the static
route named in its requirement settles it. The
[probe batch](../../analysis/ableton-live-12.4.3/r2/s7-midi-notes-v1/probe-batch.json)
(PRB-S7-01 to 10) will not run. It is kept as the record of what observation would have
settled, together with the appendix's corrections to PRB-S7-02 and PRB-S7-07.

## Analyst evidence appendix

Analysis-only. Do not copy into a handoff. The canonical evidence is
[MIDI note storage](../research/midi-note-storage.md), with retained run
`analysis/ableton-live-12.4.3/r2/s7-midi-notes-v1/` (dossier results s7-0001 to s7-0004,
`corpus-excerpts.jsonl`, `vtable-reads.txt`, `static-survey.json`). The image is
`Live.arm64`, SHA-256 `3a99ceea…d1c383cfad`, base `0x100000000`. ✓ marks a branch this
author re-read in the dossier disassembly while drafting.

Revision 2 also cites the evidence of the midi-note-storage-v1 review (2026-10-18, a separate
review agent):
[review-checks.txt](../../analysis/ableton-live-12.4.3/handoff-staging/midi-note-storage-v1-analysis/review/review-checks.txt),
whose sections follow the findings, and
[corpus-excerpts.jsonl](../../analysis/ableton-live-12.4.3/handoff-staging/midi-note-storage-v1-analysis/review/corpus-excerpts.jsonl),
29 corpus records with chunk, offset, line SHA-256 and code SHA-256. "Review excerpts" below
means that file.

Drafting added one query round, **d4-0001**, with dossiers `0x10292b9ec` and `0x10292c960`.
Its results stayed in `/var/tmp/sound-analysis/query-spool-2/results/d4-0001/` and were
**not retained**. The review re-hashed them, and all five matched the table below. It then
re-established both functions from retained records (RVN-02). The review excerpts hold the
corpus records of `0x10292b9ec` (chunk-02023, offset 170246) and `0x10292c960` (chunk-02023,
offset 201797), whose code SHA-256 equal the d4-0001 `.c` files. Revision 2 cites those
records, not d4-0001. The d4-0001 file hashes recorded in revision 1:

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
| 002 | Registration `0x1028e26c0` (s7-0004), flag 4. Text conversion `0x10152bfb8` (n1-0006). Int64 parser `0x101533e14` ✓ (s7-0004): leading-space scan, trailing-space count, optional `+`, converted length `min(len − start, end)` (the same computation as the transport-state integer parser, RV1-01), `< 0x40`, `+-` check, ASCII check, then a whole-span conversion `0x101524d8c`. Its failure is `Unexpected value for int64 node`. The conversion `0x101524d8c` (review excerpts, chunk-00813 offset 61888) is signed 64-bit: it skips leading zeros, accepts `-`, and fails with errc 0x22 above 9,223,372,036,854,775,807 (plan F7). `Invalid`: an exact seven-character compare, then DBL_MAX, at `0x10152c058`–`0x10152c088` (review-checks section 4, RVN-09). Int fields (type 0x11 in `0x10152bfb8`, plan F3) use the parser `0x1002fd908`. Its converter `0x1002fda78` (review excerpts, chunk-00132 offset 138125) accepts one leading `-` (RVN-11). REQ-TRANSPORT-STATE-006 r3/r5 settles `-` with X: its int32 path uses this same `0x1002fd908` → `0x1002fda78`, while NoteId uses the separate int64 converter `0x101524d8c` | S; both-sides spaces and `-` U; other integer fields S (A3) |
| 003 | Reset slot `+0xc8` = `0x1028e2fcc` ✓ (s7-0002) sets only VelocityDeviation 0, Probability 1, IsEnabled 1. Per-item sequence `0x101487284` ✓ (s7-0001) | S |
| 004 | Omit predicate `0x1028e2fe4` ✓ (s7-0001). Generic writer `0x101486cdc` (n1-0008). Array writer `0x101560258` (s7-0003). Copy-out `0x1028e2f90` (s7-0004) copies every field, so no state carries between written notes. Shipped: 12.4d1 attribute sets and `veldev_present_equal_0` / `probability_present_equal_1` only in older writers | S; corroborated |
| 005 | Post-load `0x1028e2c80` ✓ (s7-0001, disassembly). Duration: `fcmp d0,#0.0; fccmp d0,DBL_MAX,#4,pl; b.ne`, so a negative value or DBL_MAX is zeroed and NaN is kept. Velocity: `fcsel gt` then `fcsel mi`, NaN kept. OffVelocity and Probability: vector `fcmlt`/`fcmgt`/`bit`/`bic` against `0x105896fa8` = (127.0, 1.0). The Ghidra pseudocode wrongly shows NaN zeroed for Duration and set to 1 for Velocity; the disassembly governs. Every slot `+0xd0` post-load runs only when the load-context flag `+0x2c` is set. Review RVN-01 established that it is set for a Live Set read (review-checks section 2). The gate sites are `0x101487284`, `0x101487310`, `0x101486fe4` and `0x1014868c0`. Every context constructor stores 1. The only clear, `0x1015192b8`, is called from the undo-history streams `0x101546518` and `0x101547ef4`. The reader `0x101484108` builds its context through `0x101478258` and `0x10151e0d8`. Residual, accepted in review: an inlined clear elsewhere is not excluded | S (A1 established) |
| 006 | Quantizer `0x1028e2e24` ✓ (s7-0001): `fcsel ge` sign, `fmadd` with h × 0.5, `fabs`, `fmul` by 3843840, `frintm`, `fdiv`, `fmul` sign. Sentinels `0x1055d9680` = (−1.7976931348623155e308, 1.7976931348623155e308, DBL_MAX, +inf) (`vtable-reads.txt`). Event quantizer `0x1025c7a0c` (s7-0003). Examples recomputed with a scratch script (not retained) and equal to PRB-S7-04 | S |
| 007 | `static-survey.json` `documents.checks`: `time_negative` 330, `time_before_loopstart` 45,068, `time_at_or_after_loopend` 52,740, `duration_nonpositive` 4 | D; meanings U |
| 008 | MidiNotes post-load `0x1028f5864` ✓ (s7-0001). Id collection `0x1028f6154` (s7-0002) skips 0 and sorts as unsigned 64-bit. Adjacent-equal scan, log `Note IDs are not unique in {}: {}{}`, throw `Note IDs are not unique` | S |
| 009 | Next-id raise `0x102920db4` (s7-0002): `max` by unsigned compare, argument 1 when there are no ids. Zero-id pass `0x1028f6664` (s7-0002) walks the KeyTrack list, then the array. Id allocation `0x1028db9b8` (s7-0003). Because the pass follows the stored KeyTrack list, ascending key order holds only for KeyTracks stored that way (RVN-03). The all-absent case needs only the constructor value 0 (`0x1028e2af4` ✓) and a reset that does not touch NoteId; it does not depend on the inheritance mechanism | S |
| 010 | No sort found after load (generic post-load `0x101486fa8` on KeyTrack and array). `documents.checks`: `keytracks_sorted_by_key` 1,368, `order_time_decreasing` 0, `order_time_equal` 0, `overlap_same_key` 261 | S (negative result) / D / U |
| 011 | Key-map store without a range check: `str x23,[x19,w0,SXTW #3]` in `0x1028f5f74` (s7-0003) and `0x1028f5420` (s7-0004). The map has 128 slots; the constructor sets MidiKey −1 | U, excluded |
| 012 | List writer `0x101468408` (pseudocode) writes the stored id. The reader's handling of `Id` was not traced. Empty-KeyTrack removal at the start of `0x1028f5864` is gated by global `DAT_106f54e20`+0x350 and `0x10185138c` | D / S / U |
| 013 | Event constructor `0x1025c77fc`, reset `0x1025c7b04`, omit predicate `0x1025c7b10` (s7-0004) | D / S |
| 014 | List post-load `0x10292b730` ✓ (s7-0002): `CC + 2 > 0x82` skip, `0x1011afdac`, DBL_MAX drop, clamp `0x1011afc18`/`0x1011afc2c` (−8192/8191 for −2, else 0/127), stable sort `0x1029307b8`. Store post-load `0x10292cd70` ✓ (s7-0002): erase when NoteId is 0 or CC is out of range or invalid; a (NoteId, CC) set size different from the list count throws `Multiple sets of per-note controller change events with the same note ID and CC number`. Orphans `0x1028f64d0` (s7-0003) use the pre-assignment id list. **Boundary step** (found in d4-0001 ✓; re-established in review RVN-02): in `0x1028f5864` at `0x1028f5bec`–`0x1028f5c0c` (retained S7 disassembly), each note's NoteId (`0x1028da61c`) and Duration (`0x1028dea48`) go to `0x10292c960`. That function (review excerpts) calls `0x10292b9ec` for each list of that NoteId, then removes lists whose event count is 0 (`0x10292caa4`, `0x10292cb58`). `0x10292b9ec` (review excerpts; early return decoded from the image, review-checks section 3) returns early when the list is empty, or when the first offset is > 0 (`fcmp; b.le`) and the last is < Duration (`b.mi`). Otherwise it builds an envelope (`0x1025c442c`, `0x1025c4708`) and calls vtable `+0x308` with the ranges [−1.7976931348623155e308, 0.0] (`0x105847020`, read with `read_consts.py`) and [rounded Duration, 1.7976931348623155e308]. That call's semantics were not traced. In the Chuck Sutton Intro demo, 3,204 of 5,491 non-empty lists start at an offset ≤ 0 and 1,012 end at or after the note's Duration (ad-hoc count, not retained) | S; boundary adjustment U |
| 015 | Group check `0x1028f5640` ✓ (s7-0002): id 0 or id ≤ previous (signed, starting at 0) fails. `0x102920ecc` (corpus) is `id < NextId` unsigned. Registration `0x1028f5770` (corpus) does not check the note. The failure throws `Note-group ids are corrupt.` Shape/type follow the reviewed [group source batch](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-midi-probability-groups-v1/README.md): registrations `10292627c`/`102925eb4`, group constructor `102926720`, label builder `1029265f4`, enum initialization `101567bfc`, array/list/generic writers and five inherited conditional class tables. Expanded C beyond the 4/176/244-byte callback/registration bodies is excluded; separate post-load `1028f5864` owns validation. [Independent source review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/depth-midi-probability-groups-v1-review.json) approves conditional shape/proposals only | S; registered-class shape/type association, final save/later effects/counter repair U |
| 016 | `0x10152205c` ✓ (s7-0001): Double `0x101520dbc`, Float `0x101520c70`, Int64 plain, Bool. Rule in REQ-TRANSPORT-STATE-011. `documents.checks` `fmt_ok` 2,054,618 | S; corroborated |
| 017 | Throws through `0x101488e64` and `0x10148229c`; the top-level catch was not traced | S / U |

**Extracted execution (X2, revision 3).** Evidence:
[x2-notes-launch-v1](../../analysis/ableton-live-12.4.3/r2/x2-notes-launch-v1/manifest.json),
regenerated by `sh run.sh`: `results/notes.json` (every vector, with the spec formula and exact
rounding beside the X value), `inputs.json`, `raw/runs.jsonl`, `addresses.json` (matching),
`slice-compare.txt` (arm64 comparison), `imports.txt` and `summary.txt`. The slice is
`Live_x86_64.x86_64` (SHA-256 in the manifest). The research page has the method:
[MIDI note storage, X2 results](../research/midi-note-storage.md#extracted-execution-results-x2-2026-10-18).

| Requirement | x86_64 function run (arm64 counterpart) | Setup and result | Limits |
| --- | --- | --- | --- |
| 005 | Post-load limits `0x102a2a7f0` (`0x1028e2c80`): slot +0xd0 of vtable `0x106d6ab58` | Hand-built note objects at the registered offsets (registration `0x102a2a250`: Time +0x30 … NoteId +0x58); 58 vectors outside the near-tie set, including every MNS-014 to 025 value, the bounds, −0, ±∞, NaN and denormals | That the post-load slot runs for a Live Set read is A1 (S). The text parse of each value is not run; the harness passes the binary64 or binary32 value of the text |
| 006 | Translator slot +0 `0x102a2a9b0` (`0x1028e2e24`), event translator `0x1026ede60` (`0x1025c7a0c`) | Run on the object the limits left (order of REQ-005 then 006); 128 note vectors, including 70 within three binary64 steps of a halfway point, and 9 TimeOffsets. The REQ-006 formula equals X bit for bit for all 137; exact halves-away rounding differs for 12 near-tie values | The copy into the in-memory note is the step that rounds (S); slices equal (no FMA effect: `fmadd` adds an exact product) |
| 016 | Writer text P = 17 `0x10142b980` and P = 9 `0x10142b6c0` (X1 matches) | The held values of the MNS cases, 0.1, 0.2 and ±0; `-0` for −0 in both widths | That the member writers `0x10150f7a0` and `0x10150f6a0` (arm64 `0x101520dbc`, `0x101520c70`) reach these formatters for a finite value other than the largest is S. Substituted glibc `log10` and `vsnprintf` as in X1 |
| 011 | `MidiKey` getter `0x1029ed3b0` (`0x1028aca40`) | Returns the stored int for 36, 0, 127, 128, 129, −1, −5 and 2³¹ − 1 | The stores `0x102a40980` and `0x102a3fce0` (arm64 `0x1028f5f74`, `0x1028f5420`) are read statically only |

No import was called by the limits, grid or getter runs. The slice comparison found no
difference for any input class, including NaN (the x86 Ghidra pseudocode of `0x102a2a7f0` shows
NaN changed; its disassembly keeps NaN, as X does).

**Cases backed by X.** MNS-014 to 023, 025, 067, 069 and 072 to 075 take their saved values from
X runs of the limits, the grid rounding and the writers. Their path (read, post-load, copy,
writer) remains S, and every saved comparison still rests on A2.

**Excluded inheritance (static reading, not a requirement).** The array loader creates one
note object per KeyTrack and reuses it. The reset touches only three fields. So an omitted
Time, Duration, Velocity, OffVelocity or NoteId repeats the previous note of the same
KeyTrack, after that note's limits but before rounding. On the first note the omitted values
come from the constructor `0x1028e2af4` ✓: Time DBL_MAX (not rounded), Duration 0 (DBL_MAX,
then limited), Velocity and OffVelocity 127 (FLT_MAX, then limited) and NoteId 0. A NoteId
omitted after a non-zero id therefore duplicates it and makes the document refused. Per-note
events behave the same way: one object per list, and a reset of the curve controls only.
PRB-S7-01 and PRB-S7-02 would have tested this reading. Under ADR 0003 it stays a static
reading.

**Corrections to the source packet:**

- **MN-23.** The research says "leading or trailing spaces … are accepted". Trailing spaces
  are accepted only with no leading space or `+`; spaces on both sides are U (REQ-002). The
  value limit is signed (plan F7).
- **MN-20.** It says events "lacking TimeOffset" are dropped. Only an event whose TimeOffset
  is DBL_MAX is dropped, which for an omitted value is only the first event. The excluded
  inheritance applies to the others.
- **New step.** Neither MN-19 nor MN-20 records the boundary adjustment and empty-list
  removal (d4-0001, re-established in review RVN-02). A dated correction is now on the
  research page.
- **Context flag (review RVN-01).** The research calls the load-context flag inferred and
  ties it to the clamps only. It gates every post-read step of A1 and is established
  statically for a Live Set read. A dated correction is on the research page.
- **PRB-S7-02 variant B.** It expects "NoteIds 1..n". With every NoteId removed from the 909
  file, whose `NextId` is 59, the static result is 59 to 99 in KeyTrack document order
  (keys 36, 38, 39, 44, 45, 46), then note order, with `NextId` 100. Kept as record; the
  probe will not run (ADR 0003).
- **PRB-S7-07.** It should add the MNS-053 variants. Moot under ADR 0003.

**Dropped or downgraded from MN-01 to MN-24:**

- **MN-06** and MN-07's mute meaning become U.
- **MN-12** becomes an exclusion, apart from the all-absent NoteId case.
- **MN-16** is U and excluded.
- **MN-17** is S for sorted input only.
- **MN-18:** the meaning and preservation of Ids are U.
- **MN-19:** the TimeOffset origin is U.
- **MN-21:** the cases are blocked by the group shape.
- **MN-22** (version history) is not a requirement, because older documents are excluded.

### Revision 6 retained-source reconciliation

The [approved remaining-U source/proposal packet](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-midi-storage-remaining-u-v1/README.md),
manifest SHA256 `6b5b0f4a9a7ba99af6d23ea546bdf496a4bd86bdda990cc9e6589eac441a83f0`,
and its [independent review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/depth-midi-storage-remaining-u-v1-review.json),
SHA256 `bd3052e837d596467e221313f46190caba54d55d30b7230406b40b6d57ac24c8`,
supply the exact target/version/record/body/chunk/span identities in
[source-locators.json](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-midi-storage-remaining-u-v1/source-locators.json).
The earlier evidence table records its as-of r5 frontier; this subsection qualifies
002/012/014 without rewriting retained analysis or the immutable family map.

- **002 / MNS-076.** Retained Int64 wrapper `0x101533e14` and converter
  `0x101524d8c` require consumption of the selected span. For the exact stored
  space-7-space input, that span retains trailing space, supporting local refusal.
  No translated parser or reference function was executed; field/reader binding and
  public catch/state remain qualified.
- **012 / MNS-077.** `0x1028f4048` constructs the wrapper/list at owner +0x428/+0x430
  through `0x10156b17c`; descriptor `0x1028ab68c` and AKeyTrack registry `0x1028ab80c`
  reference `DAT_106e58710`. Inherited conditional ARemoteableList vptr
  `0x10667ec98`, slot +0x140, reaches `0x10156d7d8` then generic loader
  `0x1014674b4`. Its parsed-Id set check raises `Non-unique list ids` before
  constructing/reading the duplicate item. This is distinct from REQ-014's
  duplicate `(NoteId, CC)` rule. The writer's held Id and empty-list flag
  `DAT_106f54e20`+0x350 do not settle final saved identity or flag ownership.
- **014 / MNS-053.** Retained caller `0x10292b9ec` creates/initializes the adapter
  through `0x1025c442c` → `0x1025c4484` and `0x1025c4708`. Conditional
  APerNoteAutomationAdapter vptr `0x1067decd8`, slot +0x308, reaches the four-byte
  thunk `0x1025c6068` → 312-byte body `0x1025c606c`. Expanded thunk C is not a
  second implementation. The body dispatches +0x2e8/+0x398; conditional targets
  `0x10256314c`/`0x1025654e8`, event-array callbacks and transaction commit effects
  remain untraced. Native sites `0x1025c6110`/`0x1025c6148` remain unresolved;
  C-order association supplies zero new indirect-resolution credit.

The [r6 owner packet](../../analysis/ableton-live-12.4.3/full-spec-v1/midi-storage-remaining-u-owner-r6/README.md)
records all eight public U rows and three group gaps as one reconciliation,
with exact predecessor hashes and a reversible minimal delta. MNS-024 retention/text,
034 negative-counter exclusion, 035 eventual order and 060 public catch/state remain
unchanged. MNS-037 has zero required safe-refusal outcomes. All four 053 variants,
final group Save, later missing-note effects and whole-load group-counter ordering
remain U. A local note-counter raise is not group-counter repair. No result is
inferred for unsupported group enum values or playback meanings. All X clauses
and the broader exclusions remain unchanged. Source approval is separate from
pending independent owner review; no new original/candidate run or release.

## Revision and handoff

| Revision | Date | Change |
| --- | --- | --- |
| 1 | 2026-10-17 | First draft from packet S7 (MN-01 to MN-24) plus one verification round (d4-0001). 17 requirements: 4 without unknown parts (003, 004, 005, 008), 12 with D or S clauses and unknown parts, 1 unknown and excluded (011). 60 unexecuted cases: 45 gradable (MNS-036 in part), 6 blocked by the group shape, 9 unresolved |
| 2 | 2026-10-18 | Applies the staging and review findings of midi-note-storage-v1 ([plan](midi-note-storage-handoff-plan.md#review-outcome), [review](../../handoff/midi-note-storage-v1/REVIEW.md)) and ADR 0003. Applied: RVN-01 (A1 widened to every gated post-read step and established statically); RVN-02 and F10 (the REQ-014 boundary step cited from the review excerpts); RVN-03 (REQ-009 precondition: KeyTracks stored in ascending key order); RVN-04 and F2 (MNS-001 and the comparators no longer cover probability groups or the group `NextId`); RVN-09 and F4 (`Invalid` stated in REQ-002 and REQ-013; MNS-017 and MNS-051 list 002); RVN-11 (A2 restated for both constructions; A3 added); RVN-12 and F1 in part (the release's authored-set construction noted); F3 (plain decimal text for `MidiKey`, `CC`, list `NoteId` and `Id`); F5 (REQ-010 order clause excludes overlap); F6 (list order and event attribute order U and not compared); F7 (signed 64-bit limit; leading zeros counted); F8 (MNS-061 to MNS-071 added); F9 (MNS-003 judges n2 and lists 003); the plan's case disposition (unstated event `Value` 1 in MNS-041 and MNS-046); release alignment (positive zero in REQ-005; REQ-014 in REQ-016). Rejected: copying d4-0001 into the retained run, since the review excerpts carry identical code and this revision edits wiki pages only; F1's PRB-S7-09 extension, since no probe will run (ADR 0003). No change needed: RVN-05 to RVN-08 and RVN-10, which concern only the release package or confirm the draft. Probe wording replaced under ADR 0003. 17 requirements: 4 without unknown parts, 12 with D or S clauses and unknown parts, 1 unknown and excluded (011). 71 unexecuted cases: 56 gradable (MNS-036 and MNS-070 for the outcome only), 6 blocked by the group shape, 9 unresolved |
| 3 | 2026-10-18 | Extracted execution (packet X2, evidence label X added). REQ-005, 006 and 016 examples become X with an S path; the REQ-006 formula is confirmed bit for bit, including values next to halfway points, where it differs from exact rounding. Negative zero settled: REQ-006's and REQ-016's U clauses become X (`-0`), and REQ-005 states −0 for each value. REQ-011 stays excluded; its static route was traced in both slices and no range guard exists. Errors found: none in the clauses; the x86 pseudocode's NaN reading is wrong, as revision 1 found for arm64. MNS-023 becomes gradable (`-0`); MNS-072 to 075 added. 17 requirements: 5 without unknown parts (003, 004, 005, 008, 016), 11 with D, S or X clauses and unknown parts, 1 unknown and excluded (011). 75 unexecuted cases: 61 gradable (17 backed by X, 44 static or documented; MNS-036 and MNS-070 for the outcome only), 6 blocked by the group shape, 8 unresolved |
| 4 | 2026-10-19 | applies midi-note-storage-v2 F1 to F3 and RVN2-01 to 03, 07. REQ-002 states the negative-zero reading for the five covered note attributes; REQ-006 excepts negative zero from on-grid identity; REQ-007 names positive-zero duration and retains normalization. MNS-072 to 075 list REQ-002, and MNS-073 also REQ-004. Counts and expectations unchanged. |
| 5 | 2026-10-20 | One six-case probability-group refinement from the independently reviewed conditional source batch. REQ-015 and Fragment G now state GroupId child/NoteId attribute form, distinct list Id and 0/1 label association; all six existing group setups become concrete. Four refusals and two admission-only outcomes no longer depend on unknown shape. All 16 other requirement bodies and 69 other case rows are unchanged; 17 IDs/75 cases retained. Final group save, later missing-note effects, whole-load counter repair and unsupported enum/playback meanings remain U. No original/candidate execution or new release. Owner refinement pending independent review. |
| 6 | 2026-10-20 | One whole remaining-U reconciliation after approved source review: conditional local clauses for 002/012 and reader-only MNS-076/077 reuse 011/038 inputs; 014 narrows its source frontier only. All 75 prior rows, eight public U rows and 14 other requirement bodies are byte-identical. All 17 requirement IDs retained; 77 draft case IDs. Four expression variants/three group gaps/unsafe-key exclusion remain. No fixtures, original/candidate execution, public result, new release or whole-family denominator. Independent owner review pending. |

Before the 2026-10-18 review, a first release candidate could
contain the gradable cases of REQ-002 to 009, REQ-014 and REQ-016, under assumptions A1
and A2.

Released 2026-10-18: [midi-note-storage-v1](../../handoff/midi-note-storage-v1/README.md), 67 cases, approved with narrowing by a separate review agent (partial REQ-001 to 010, 013, 014, 016 only; 011, 012, 015, 017 unreleased). The review findings are on the [handoff plan](midi-note-storage-handoff-plan.md#review-outcome). Revision 2 applies them; the release stays pinned to revision 1.

Revision 3 adds X evidence and cases MNS-072 to 075, and makes MNS-023 gradable.
[midi-note-storage-v2](../../handoff/midi-note-storage-v2/README.md) released these partial
clauses on 2026-10-18 with 72 cases, superseding v1 and rebuilding its structurally invalid
fixtures. The [v2 review](../../handoff/midi-note-storage-v2/REVIEW.md) RVN2-01 to 03 and
RVN2-07 support revision 4's negative-zero wording and requirement references; no case
expectation changes. At revision 4 the draft had 17 requirements and 75 cases (61 gradable,
6 blocked by the group shape, 8 unresolved).


Revision 5 retains all 17 requirement IDs and 75 case IDs. There are now 67 statically or
locally X-derived reader/computation cases (17 backed by X, 50 S or D), including admission-only
036, 058, 059 and 070, and eight unresolved cases. No case was executed against Live or a
candidate. Saved group text and later missing-note effects remain ungraded within 058/059.
The current partial release remains midi-note-storage-v2 with 72 cases and excludes REQ-015.
This draft successor is **pending independent owner review**, separate from source approval.


### Current r5 disposition — 2026-10-20

The separate [independent owner review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/midi-probability-groups-owner-r5-review.json)
approves this bounded static refinement. Its reviewed 63,380-byte draft SHA256 is
`0f9cfe15d7af8043f604af2377c1c0ad7d5c6352968d6fd5b6e2b6c32caae11b`;
review SHA256 `3b929d49769bd1c3a482f54a1967407e94a65b6db6b58f1bb1f046402f06daef`.
Pending-review wording above records the author freeze; this disposition governs.
Four refusals and two local admission-only cases are approved under the selected
registered-class route/A1. This is neither a public lifecycle pass nor a Save,
later-effect, unsupported-enum or whole-load-counter-repair contract. All 17 IDs/
75 case IDs remain; no original/candidate execution or released payload changes.
Current midi-note-storage-v2 remains the released 72-case partial contract.


## Current partial release v3 — 2026-10-20

[MIDI note storage v3](../../handoff/midi-note-storage-v3/README.md) is now the current local partial release,
superseding v2 with72 case objects/fixtures carried exactly plus six conditional
local group comparisons. Its14 partial requirement bodies include bounded REQ015;
011/012/017 remain unreleased. [Review and publication record](midi-note-storage-v3-handoff-plan.md#review-outcome-and-current-disposition)
pins content/correction/final exact-tree approval and manifest `fa281c37472e13a6ba840499687e90928654c9862582fa5bd4d04f4436da7c2c`.
Earlier current-v2 statements above record the as-of owner-adoption history;
this dated release disposition governs. No original/candidate execution,
compatibility grade or new public load/save/later-effect/counter-repair result.
All 75 draft IDs and the historical r4 family-map inventory remain unchanged.


## Current r6 proposal — 2026-10-20

The [owner reconciliation packet](../../analysis/ableton-live-12.4.3/full-spec-v1/midi-storage-remaining-u-owner-r6/README.md)
is pending independent owner review. It adds only the two separately scoped local
reader refusals MNS-076/077 and the qualified expression source frontier. All 75 old
case rows, including all 8 public U rows, and 14 other requirement bodies are preserved
exactly. There are 77 draft case IDs; this is not a whole-family outcome denominator
or compatibility fraction. Earlier r5/current-v3 count statements are as-of history.
MIDI note storage v3 remains the current immutable 78-object partial release; no
r6 release or fixture staging is selected. Local refusal is not proof of the
public catch, displayed error, whole-Set/clip rejection, rollback or saved state.
The source review and this owner proposal grant no application or candidate pass.


## R6 owner approval — 2026-10-20

The [separate independent owner review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/midi-storage-remaining-u-owner-r6-review.json), SHA256 `492476f9376b1f2ff2e8f558b30d3fedae4bca828136e3d717a2aa15a7d8ab84`, approves the bounded r6 refinement. Root adopted its exact72,839-byte reviewed prefix/SHA256 `593e10be4054180173c09d8c7fd30bbf84535877dccb9c4de34133f27dec2d73`; the pending proposal above records the author freeze. All75previous case rows/14other bodies/allX clauses remain exact. Only002/012/014 bodies changed;076/077 are separate conditional local comparisons. Eight publicU rows, allfour053variants, final group Save/later effects/counter order and unsafe-key exclusion remain.77draft case IDs are navigation, not a frozen family denominator. No public/reference/candidate result or grade follows.

MIDI note storage v3 remains current/immutable. Root separately selected v4 staging to carry all78v3case objects and existingfixture bytes plus exactlytwo local comparisons; content review/exact-tree approval/full prerelease lint precede any publication. Concurrent expression-source frontier is unreviewed and was excluded from r6 owner approval. No normative/case/release content is changed by this approval append.


## Current partial release v4 — 2026-10-20

[MIDI note storage v4](../../handoff/midi-note-storage-v4/README.md) is locally
released after independent content/final-tree approval and full prerelease lint;
[publication record](midi-note-storage-v4-handoff-plan.md#current-local-publication--2026-10-20).
All78v3objects/78gzip fixtures/14oldbodies remain exact. Two separately scoped
local-reader comparisons use explicit Notes edits over existing authored MNS001;
80case records/78fixtures/15partialrequirement IDs. Only the bounded002supplement
and012localrefusal are added. V3 remains immutable/superseded; earlier current-v3
statements are as-of history. Original publicU/four053variants/groupgaps/unsafe
exclusion persist. No reference/candidate result, compatibility grade, full-family
denominator, implementation or restricted-workspace synchronization follows.
