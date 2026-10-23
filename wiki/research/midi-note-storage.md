---
id: RESEARCH-MIDI-NOTE-STORAGE
type: research
status: draft
updated: 2026-10-23
access: analysis
target: Ableton Live 12 Suite 12.4.3 arm64
---

# MIDI note storage in clips

Packet S7 for FEAT-MIDI. Question: how does a MIDI clip store its notes, and how does
12.4.3 read them back? The static half covers schemas and shipped documents: the note
structure, value domains, time units, ordering and schema evolution. The native half covers
the reader (missing attributes, defaults, out-of-range values, duplicate NoteIds, overlapping
notes) and the writer (grouping, order, omission, number text). Nothing was executed.
"Load fails" means the traced code throws the corrupt-document error; what the user then
sees is the subject of [document container native](document-container-native.md#how-a-refusal-becomes-an-error)
and was not traced here. The generic loader, member registry and number formatter are described in
[transport-state native](transport-state-native.md) and are only referenced here.

## Evidence

Source: [SRC-ABLETON-12-4-3](sources/ableton-live-12.4.3.md), bundle
`/home/ollie/Ableton Live 12 Suite.app` (read-only). Image `analysis/ableton-live-12.4.3/derived/Live.arm64`,
SHA-256 `3a99ceea…d1c383cfad`, image base `0x100000000`, Ghidra 12.1.4. Retained run:
[s7-midi-notes-v1](../../analysis/ableton-live-12.4.3/r2/s7-midi-notes-v1/manifest.json) (SHA-256 of every file).

| File | Content |
| --- | --- |
| [s7_static.py](../../analysis/ableton-live-12.4.3/r2/s7-midi-notes-v1/s7_static.py), `run.sh` | Static survey; `sh run.sh` regenerates the two outputs below byte-identically (Python 3.13.9, `python3 -I`) |
| [static-survey.json](../../analysis/ableton-live-12.4.3/r2/s7-midi-notes-v1/static-survey.json) | Schema evolution segments for 9 classes over 203 versions; per-writer attribute shapes, value statistics, ordering, identity, grid and number-format checks, examples |
| [inputs-documents.tsv](../../analysis/ableton-live-12.4.3/r2/s7-midi-notes-v1/inputs-documents.tsv) | SHA-256, size, kind and path of 595 documents (26 `.als`, 350 `.alc`, 219 `.agr` of which 103 AB1E binaries were not parsed) |
| [notes.md](../../analysis/ableton-live-12.4.3/r2/s7-midi-notes-v1/notes.md) | Round-by-round findings with every address, negative results |
| `results/s7-0001` … `s7-0004` | Unchanged query-server results with request text: 32 function dossiers with disassembly |
| [corpus-excerpts.jsonl](../../analysis/ableton-live-12.4.3/r2/s7-midi-notes-v1/corpus-excerpts.jsonl) | The 81 C1 pseudocode records relied on, with chunk, offset and line SHA-256 |
| [vtable-reads.txt](../../analysis/ableton-live-12.4.3/r2/s7-midi-notes-v1/vtable-reads.txt), [string-lookups.txt](../../analysis/ableton-live-12.4.3/r2/s7-midi-notes-v1/string-lookups.txt) | Eleven vtables and three constant groups read from the image; string-index lookups |
| [probe-batch.json](../../analysis/ableton-live-12.4.3/r2/s7-midi-notes-v1/probe-batch.json) | Phase 4 probe records PRB-S7-01–10 |

Budget: four rounds of 8 dossiers (s7-0001 to s7-0004). Pseudocode came from the corpus;
dossiers confirmed material branches against disassembly (marked ✓). No `str:` query was issued.

## Document shape

**Observed** in `12.0_12402.txt` and in every shipped 12.4d1 clip:

```xml
<MidiClip …>
  …
  <Notes>                                   <!-- class MidiNotes -->
    <KeyTracks>
      <KeyTrack Id="0">
        <Notes>                             <!-- RemoteableArray, ArrayTranslator MidiNoteEvent -->
          <MidiNoteEvent Time="0" Duration="0.25" Velocity="85" OffVelocity="64" NoteId="1" />
          …
        </Notes>
        <MidiKey Value="36" />
      </KeyTrack>
      …
    </KeyTracks>
    <PerNoteEventStore><EventLists>
      <PerNoteEventList Id="108" NoteId="38" CC="-1"><Events>
        <PerNoteEvent TimeOffset="0.377140567765567758" Value="0" CurveControl1X="0" … />
      </Events></PerNoteEventList>
    </EventLists></PerNoteEventStore>
    <NoteProbabilityGroups />
    <ProbabilityGroupIdGenerator><NextId Value="1" /></ProbabilityGroupIdGenerator>
    <NoteIdGenerator><NextId Value="39" /></NoteIdGenerator>
  </Notes>
  …
</MidiClip>
```

Notes are grouped by pitch: one `KeyTrack` per MIDI key, holding that key's notes. The note
fields are attributes of `MidiNoteEvent`; `MidiKey` and `NextId` are child elements with a `Value`
attribute. The field `MidiClip.Notes` has class `MidiNotes` in all 203 schema versions, and
`KeyTrack` is `{Notes, MidiKey}` in all 203.

### Schema evolution

**Observed** (`schema.segments`; version order is by file name, so isolated 8.x gaps may be ordering
artifacts, as noted in [S2](document-container-static.md#schema-directory-and-version-cross-check)):

| Class | Versions | Fields (Class · Type) |
| --- | --- | --- |
| `MidiNoteEvent` | 8.1_220–10.0_370 (80) | Time Double, Duration Double, Velocity Float, OffVelocity Float, IsEnabled Bool (all −4) |
| | 10.0_371–10.0_377 (6) | + NoteId Int64 |
| | 11.0_402–11.0_406 (5) | + Probability Float, before IsEnabled |
| | 11.0_407–12.0_12402 (112) | + VelocityDeviation Float, after Velocity |
| `MidiNotes` | 8.x | KeyTracks (`UndoWatch` RemoteableBool in 8.1_220–222 and 8.2_260–264 only) |
| | 10.0_373 / 10.0_376 | + PerNoteEventStore / + NoteIdGenerator |
| | 12.0_12001 / 12.0_12005 | + NoteProbabilityGroups / + ProbabilityGroupIdGenerator (before NoteIdGenerator) |
| `NoteIdGenerator` | 10.0_376; 10.0_377–12.0_12402 | NextId Int64 −4; then NextId RemoteableInt64 0 |
| `PerNoteEvent` | 10.0_373–11.0_419; 11.0_420; 11.0_421– | TimeOffset, CCNumber, Value; CCNumber removed; + CurveControl1X/1Y/2X/2Y Double |
| `PerNoteEventList` | 10.0_373–11.0_419; 11.0_420– | Events (ArrayTranslator PerNoteEvent), NoteId Int64; + CC Int |
| `NoteProbabilityGroup` | 12.0_12001; 12.0_12005– | GroupType RemoteableEnum, Notes (ArrayTranslator NoteId), Probability RemoteableFloat; + GroupId Int64 |

## Values in shipped documents

**Observed** over 1,368 clips with notes (901 in `.als`, 351 in `.alc`, 116 in plain-XML `.agr`):
235,756 notes, 14,981 KeyTracks (267 empty), 23,306 per-note lists, 271,549 per-note events and
no probability group. The `.als`/`.alc` clips were written by 12.4d1 (1,251) and 12.1d1 (1, the
default set); grooves by Live 10.1.6 to 11.3.12. None is a 12.4.3 save.

| Field | Observed values |
| --- | --- |
| `Time` | −2.6015651015651016e-07 (330 notes, exactly −1/3,843,840) to 352; 20,983 integer texts |
| `Duration` | 0 (4 notes, Chuck Sutton demo) to 80 |
| `Velocity` | 1 to 127; 168,085 non-integral (for example `80.578949`) |
| `OffVelocity` | integers 0 to 127; `0` 163,418, `64` 71,299 |
| `VelocityDeviation` | 12.4d1: only `3` (8 notes); older writers: `0` |
| `Probability` | 12.4d1: 0.3333332241 to 0.8333332539, never `1`; older writers: `1` |
| `IsEnabled` | 12.4d1: only `false` (40,910); older writers: `true` |
| `NoteId` | 1 to 6,035; unique within every clip; no 0 |
| `MidiKey` | 20 to 127; unique within every clip |
| `NextId` | greater than the largest NoteId in all 1,354 clips with notes (equal to max+1 in 1,014); `1` or `32` in 14 empty clips |
| `PerNoteEventList` | attributes `Id NoteId CC`; CC −1 (8,367), −2 (7,211), 74 (7,728); every NoteId names a note of the clip; no repeated (NoteId, CC) |
| `PerNoteEvent` | TimeOffset 0 to 66.66, never above the note's Duration; Value 0–127 for CC −1 and 74, −1706.5625 to 3165.60645 for CC −2; curve controls 0–1 and never `0.5` |

**Checks** (`documents.checks`):

- Attribute order equals schema order in every note except 570 notes in Live 10.1.6 grooves,
  which list the attributes alphabetically.
- 12.4d1 never writes `VelocityDeviation="0"`, `Probability="1"` or `IsEnabled="true"`. Every
  older writer writes all of them.
- KeyTracks are in ascending `MidiKey` order in 1,368 of 1,368 clips. Their `Id`s are in ascending
  order in only 719.
- Within a KeyTrack, `Time` never decreases and never repeats. 261 notes start before the previous
  note on the same key ends (same-key overlap).
- Every `Time`, `Duration` and `TimeOffset` is a multiple of 1/3,843,840 as computed by the native
  quantizer below.
- All 2,054,618 Double and Float note and per-note texts match the fixed-precision writer rule from
  [transport-state native](transport-state-native.md#writer-number-format); 182,251 of them differ from `%.17g`.

**Inferred:** `Time` and `Duration` are in quarter-note beats relative to the clip's own time line,
the coordinate of `Loop/LoopStart` and `LoopEnd`. Example: `909 Core Kit House 127 bpm.alc` is a
4/4 clip looping 0 to 8 with notes from 0 to 7.5. 45,068 notes start before LoopStart and 52,740 at
or after LoopEnd, so notes outside the loop are stored too.

## How the reader loads notes

**Observed** in pseudocode and confirmed in disassembly where marked ✓:

1. `AMidiNoteEvent` is a document class whose registration `0x1028e26c0` lists `Time` … `NoteId`
   in schema order. Each is a base-type member with flag 4, which makes it an XML attribute ✓.
   `AKeyTrack` (`0x1028ab80c`) registers `Notes` as a RemoteableArray whose translator is the
   `AMidiNoteEvent` descriptor, element size 48 bytes, and `MidiKey` as an Int child element.
2. The array loader `0x101560424` ✓ creates **one** `AMidiNoteEvent` before the loop over child
   elements and reuses it for every note of that KeyTrack. A child of another class throws
   `Class mismatch for array member` (corrupt).
3. For each note `0x101487284` ✓ calls the reset slot `+0xc8`, the generic loader, then the
   post-load slot `+0xd0`. The reset `0x1028e2fcc` ✓ sets only VelocityDeviation 0,
   Probability 1 and IsEnabled true. The generic loader stores only the attributes present
   ([transport-state native](transport-state-native.md#how-a-set-reaches-the-transport-objects)),
   so attribute order does not matter.
4. Post-load `0x1028e2c80` ✓: a Duration below 0 or equal to DBL_MAX becomes 0. Velocity is
   clamped to 1…127, OffVelocity to 0…127 and Probability to 0…1. NaN survives every clamp, and
   Time, VelocityDeviation and NoteId are not checked. This runs only when the load context flag
   `+0x2c` is set. **Inferred** set for document loads: eleven context constructors set it, and only two
   binary-stream paths clear it. Corrected 2026-10-18: see [Corrections](#corrections).
5. The copy into the in-memory note `0x1028e2e24` ✓ rounds Time and Duration half away from
   zero to the nearest multiple of 1/3,843,840 beat. Four sentinels are left unchanged:
   ±1.7976931348623155e308, DBL_MAX and +∞.
6. After its members load, the clip's `AMidiNotes` post-load `0x1028f5864` ✓:
   - rebuilds the 128-slot key-to-KeyTrack map;
   - collects all non-zero NoteIds of all KeyTracks and sorts them;
   - throws `Note IDs are not unique` on any repeat (logged, rate-limited, with up to 10 ids);
   - raises `NextId` to max(NextId, largest id + 1) by unsigned comparison, or to at least 1 when
     there are no ids ✓;
   - removes per-note lists whose NoteId names no note;
   - gives every NoteId-0 note the current NextId and increments it, in KeyTrack list order, then
     note order ✓;
   - validates probability groups (below).

### Missing, malformed and duplicate items

| Input | Static-derived outcome |
| --- | --- |
| `VelocityDeviation`, `Probability` or `IsEnabled` absent | 0, 1, true |
| `Time`, `Duration`, `Velocity`, `OffVelocity` or `NoteId` absent on a note that is not the first of its KeyTrack | Value of the previous note in the same KeyTrack (reused object, no reset) |
| The same, absent on the first note of a KeyTrack | Time DBL_MAX (sentinel, not quantized); Duration 0; Velocity and OffVelocity 127 (FLT_MAX clamped); NoteId 0 (assigned on load) |
| NoteId absent from every note (as in documents older than 10.0_371) | All 0, then numbered from NextId on load |
| NoteId absent after a non-zero NoteId, or two notes with the same non-zero NoteId anywhere in the clip | Load fails (`Note IDs are not unique`) |
| Velocity 0 / 300, OffVelocity −5 / 200, Probability 1.5 / −1, Duration −2 | 1 / 127, 0 / 127, 1 / 0, 0; load continues |
| Off-grid Time or Duration | Rounded to the 1/3,843,840 grid |
| NoteId text `1.0`, `0x10`, empty, 64 or more characters, overflow | Load fails (`Unexpected value for int64 node`, `0x101533e14` ✓). Leading or trailing spaces and one `+` are accepted |
| IsEnabled `1` / `0` | true / false; other tokens fail ([transport-state native](transport-state-native.md#lexical-acceptance-on-load)) |
| Duplicate attribute | Malformed XML (Expat) |
| Unknown attribute | Presumably ignored unless the versioned, equal-change-count condition of [transport-state native](transport-state-native.md#missing-duplicated-and-unknown-items) holds; not traced for array items |
| `MidiKey` outside 0…127, absent (constructor −1), or two KeyTracks with the same key | **Unknown.** The map store has no range check (`str x23,[x19,w0,SXTW #3]` in `0x1028f5f74` ✓; `0x1028f5420` ✓), so an out-of-range key writes outside the 128-slot table. With a repeated key, the later KeyTrack takes the map slot; both stay in the list and are saved |
| Notes of a KeyTrack out of time order; overlapping notes on one key | Loaded in document order; no sort was found after load. Overlaps are accepted (shipped). Later re-sorting is **unknown** |

## Per-note expression (MPE)

**Observed:** each `PerNoteEventList` binds one note (`NoteId`) and one controller (`CC`) to a
breakpoint list. Its events carry `TimeOffset` (Double), `Value` (Float) and four Bézier controls
(Double). The `APerNoteEvent` constructor `0x1025c77fc` ✓ sets TimeOffset DBL_MAX, Value 0 and each
control 0.5. Its reset `0x1025c7b04` ✓ restores only the four controls, and its omit predicate
`0x1025c7b10` ✓ skips a control equal to 0.5 on save. TimeOffset is quantized like note Time
(`0x1025c7a0c` ✓).

On load (all ✓):

- The list post-load `0x10292b730` skips lists whose CC is outside −2…128 or invalid.
  Otherwise it:
  - drops events whose TimeOffset is still DBL_MAX;
  - clamps Value to −8192…8191 for CC −2 and to 0…127 for any other CC;
  - stable-sorts the events by TimeOffset.
- The store post-load `0x10292cd70` erases lists with NoteId 0, a CC outside −2…128, or a CC that
  fails `0x1011afdac`. Valid CCs are every value except 0, 32 and 120…128. A repeated
  (NoteId, CC) pair throws
  `Multiple sets of per-note controller change events with the same note ID and CC number`.
- Lists whose NoteId names no note are removed afterwards by `0x1028f64d0`.

**Inferred:** CC −2 is per-note pitch bend in 14-bit units; −1 is per-note pressure; 74 is slide.
This rests only on the clamp ranges, the shipped values and MPE convention.

## Probability groups

**Observed** ✓ `0x1028f5640`: when `NoteProbabilityGroups` is not empty, each group's `GroupId`
must be non-zero, larger than the previous group's, and below `ProbabilityGroupIdGenerator/NextId`.
Otherwise the load fails with `Note-group ids are corrupt.`. Each listed NoteId is mapped to its
group without checking that the note exists. No shipped document contains a group, so the group XML
shape is known only from the schema.

## Writer

**Observed:**

- The generic compound writer emits flag-4 members as attributes in registration (schema) order. It
  skips a member when the class's slot `+0x150` returns true.
- `AMidiNoteEvent`'s predicate `0x1028e2fe4` ✓ omits VelocityDeviation when it equals 0.0,
  Probability when it equals 1.0, and IsEnabled when true. It always writes Time, Duration,
  Velocity, OffVelocity and NoteId.
- The array writer `0x101560258` ✓ emits notes in in-memory array order. Its copy-out
  `0x1028e2f90` ✓ does not quantize.
- The list writer `0x101468408` emits KeyTracks and per-note lists in list order, each with its
  stored `Id`.
- Number text uses the formatters of
  [transport-state native](transport-state-native.md#writer-number-format): Double `0x101520dbc`,
  Float `0x101520c70`, Int64 plain decimal, Bool `true`/`false` (`0x10152205c` ✓).

**Corroborated:** the omission rule matches every 12.4d1 note, and the number rule matches every
shipped value. One example is `Time="0.359923670079920099"`, 18 decimals for a value below 1. The rule is a
static derivation for 12.4.3, because the shipped files were written by 12.4d1.

## Candidate requirements for SPEC-MIDI-NOTE-STORAGE

Proposed. Feature FEAT-MIDI with FEAT-PERSISTENCE. "Shipped" means bundle content written by
12.4d1/12.1d1 or older, not a 12.4.3 save. "Static-derived" means derived from traced code, not
observed execution.

| ID | Statement | Evidence | Strength |
| --- | --- | --- | --- |
| MN-01 | A MIDI clip's notes are `MidiClip/Notes` with children `KeyTracks`, `PerNoteEventStore`, `NoteProbabilityGroups`, `ProbabilityGroupIdGenerator`, `NoteIdGenerator` in that order (12.0_12005 and later) | Schema; 1,252/1,252 12.x clips; registration `0x1028f3afc` | Observed |
| MN-02 | Notes are grouped by pitch: one `KeyTrack Id=…` per key with `Notes` then `MidiKey Value` (0–127); no two KeyTracks of a clip share a key | 14,981 KeyTracks; registration `0x1028ab80c` | Observed (shipped); out-of-range handling unknown (MN-16) |
| MN-03 | Each note is `MidiNoteEvent` with attributes Time, Duration (Double), Velocity, VelocityDeviation, OffVelocity, Probability (Float), IsEnabled (Bool), NoteId (Int64) | Schema 11.0_407+; registration ✓ | Observed |
| MN-04 | A save writes the attributes in that order and omits VelocityDeviation = 0, Probability = 1 and IsEnabled = true; Time, Duration, Velocity, OffVelocity, NoteId are always written | `0x1028e2fe4` ✓, writer; 12.4d1 notes without counterexample | Static-derived for 12.4.3; corroborated |
| MN-05 | A load accepts the attributes in any order; an absent VelocityDeviation, Probability or IsEnabled means 0, 1, true | `0x1028e2fcc` ✓; Live 10.1.6 alphabetical grooves | Static-derived |
| MN-06 | Time and Duration are clip-relative positions and lengths in quarter-note beats; notes may lie outside the loop region | Loop extents, 909 example | Inferred |
| MN-07 | Velocity is a real number 1–127 (fractions allowed), OffVelocity 0–127, Probability 0–1; muted notes are IsEnabled false | Value census; clamps | Observed domains; muted meaning inferred |
| MN-08 | Load rounds Time and Duration (and per-note TimeOffset) half away from zero to the nearest multiple of 1/3,843,840 beat, except the four sentinels | `0x1028e2e24`, `0x1025c7a0c` ✓; all shipped values on grid | Static-derived |
| MN-09 | Load clamps Velocity to 1–127, OffVelocity to 0–127, Probability to 0–1, and a negative Duration to 0; NaN, Time and VelocityDeviation are not clamped | `0x1028e2c80` ✓ | Static-derived; depends on the inferred context flag |
| MN-10 | A well-formed out-of-range note value does not make the load fail | Same | Static-derived |
| MN-11 | Number text follows the transport-state writer rule (REQ-TRANSPORT-STATE-011); NoteId and NextId plain decimal | `0x10152205c` ✓; 2,054,618 shipped values | Static-derived; corroborated |
| MN-12 | An absent Time, Duration, Velocity, OffVelocity or NoteId repeats the previous note of the same KeyTrack; on the first note it gives Time DBL_MAX, Duration 0, velocities 127, NoteId 0 | `0x101560424`, `0x1028e2fcc`, ctor ✓ | Static-derived; candidate for explicit exclusion as malformed input |
| MN-13 | Non-zero NoteIds must be unique across the whole clip; a repeat makes the load fail | `0x1028f5864`, `0x1028f6154` ✓ | Static-derived |
| MN-14 | NoteId 0 (or absent everywhere) is assigned from NextId on load, in KeyTrack list order then note order | `0x1028f6664`, `0x1028db9b8` ✓ | Static-derived |
| MN-15 | After load NextId = max(stored NextId, largest NoteId + 1), compared unsigned; a save writes it | `0x102920db4` ✓; shipped NextId > max in 1,354/1,354 | Static-derived; corroborated |
| MN-16 | MidiKey outside 0–127, a missing MidiKey or a repeated key: reference outcome unknown; the reference performs an unchecked table store | `0x1028f5f74`, `0x1028f5420` ✓ | Unknown (PRB-S7-05) |
| MN-17 | Saved KeyTracks are in ascending key order and notes in ascending Time order without ties; same-key overlaps are representable | 1,368/1,368 clips; 261 overlaps; array and list writers | Observed (shipped); ordering on load and save of unsorted input unknown |
| MN-18 | KeyTrack and PerNoteEventList `Id`s are unique per clip and need not follow key order | Shipped | Observed; semantics unknown |
| MN-19 | Per-note expression is a list per (NoteId, CC) with events (TimeOffset relative to note start, Value, optional curve controls defaulting to 0.5, omitted when 0.5); CC −2 range −8192…8191, other CCs 0…127 | Schema, `0x1025c7b10`, `0x1011afc18/2c` ✓; shipped | Observed shape; static-derived defaults and ranges; TimeOffset origin inferred |
| MN-20 | Load drops per-note lists with NoteId 0, invalid CC (0, 32, 120–128, outside −2…128) or no matching note, drops events lacking TimeOffset, clamps Value, stable-sorts events, and fails on a repeated (NoteId, CC) | `0x10292cd70`, `0x10292b730`, `0x1028f64d0` ✓ | Static-derived |
| MN-21 | Probability groups need non-zero, strictly increasing GroupIds below the group NextId, or the load fails | `0x1028f5640` ✓ | Static-derived; no shipped instance |
| MN-22 | The note fields arrived by version: NoteId 10.0_371, Probability 11.0_402, VelocityDeviation 11.0_407, per-note store 10.0_373, CC per list 11.0_420, curves 11.0_421, groups 12.0_12001/12005 | 203 schemas | Observed (schema); translation of older documents not traced |
| MN-23 | Lexical forms: Bool `true`/`1`/`false`/`0`; Int64 as described above; Double and Float as in transport-state native | `0x10152bfb8`, `0x101533e14` ✓ | Static-derived |
| MN-24 | Every child of `KeyTrack/Notes` must be a `MidiNoteEvent`, or the load fails | `0x101560424` ✓ | Static-derived |

Static fixture expectations (document values only, no behaviour):

- `909 Core Kit House 127 bpm.alc` (SHA-256 `79c6ed2f…a901ff59`): 41 notes and KeyTrack 36 first.
  Its first note is `Time="0" Duration="0.25" Velocity="85" OffVelocity="64" NoteId="1"`.
- `Chuck Sutton - Patience (Live 12 Intro Demo).als` (`f78a98f5…fdaea6`): zero-length notes,
  `Time` −1/3,843,840, same-key overlaps and all three CCs.
- `2 Step Accent 16ths.agr` (`138c7787…5f2e32`): alphabetical attribute order.

Full hashes are in `inputs-documents.tsv`.

## Phase 4 probes

Records with inputs, discriminating observations and stop conditions are in
[probe-batch.json](../../analysis/ableton-live-12.4.3/r2/s7-midi-notes-v1/probe-batch.json).
Fixture: `909 Core Kit House 127 bpm.alc`, edited.

| Probe | Settles |
| --- | --- |
| PRB-S7-01 | Inheritance of absent note attributes (MN-12) |
| PRB-S7-02 | Absent or duplicate NoteId: load failure versus renumbering (MN-13, MN-14) |
| PRB-S7-03 | Out-of-range clamps on load and save (MN-09, MN-10) |
| PRB-S7-04 | Grid rounding and its text: `0.123456789` → `0.123456751581751581`, `-0.0000002` → `-0.000000260156510156510156` (MN-08) |
| PRB-S7-05 | MidiKey out of range, absent, repeated; run in a disposable session (MN-16) |
| PRB-S7-06 | Unsorted notes and same-key overlaps on load, playback and save (MN-17) |
| PRB-S7-07 | Per-note list and event clean-up and the duplicate-pair failure (MN-19, MN-20) |
| PRB-S7-08 | Probability-group id failures and group XML (MN-21) |
| PRB-S7-09 | A real 12.4.3 save of muted, probability, deviation, release-velocity and MPE notes (MN-04, MN-11, MN-15, MN-17, MN-18) |
| PRB-S7-10 | NextId below, above and negative (MN-15) |

## Unknowns

- The user-visible outcome of each "load fails" path (shared with the container packet).
- The effect of MidiKey outside 0–127, of a missing MidiKey and of a repeated key. The reference's
  unchecked store suggests undefined behaviour.
- Whether notes or KeyTracks are re-sorted after load, and how overlapping same-key notes play.
- What a note at Time DBL_MAX (absent Time on the first note) or with Duration 0 does in editing and
  playback.
- The global flag (`DAT_106f54e20`+0x350) that removes empty KeyTracks on load.
- The meaning of KeyTrack and PerNoteEventList `Id`s, and how the reader handles repeats.
- The meaning of CC −1/−2, `GroupType` and VelocityDeviation's range; the time unit natively.
- Translation of pre-12 note layouts (UndoWatch, CCNumber per event, NextId as Int64), and AB1E
  binary grooves (memcpy path in `0x101560424`).
- Whether 12.4.3 writes exactly what 12.4d1 wrote (PRB-S7-09).

## Extracted execution results (X2, 2026-10-18)

**Question.** Under [ADR 0003](../decisions/adr-0003-no-reference-execution.md#extracted-execution-of-original-code),
do the shipped x86_64 functions behind the note value limits (PRB-S7-03) and the time grid and its
saved text (PRB-S7-04) compute what [SPEC-MIDI-NOTE-STORAGE](../specs/midi-note-storage.md) states,
and does a pure function guard the `MidiKey` range (Q-018)?

**Answer (X, with the paths still static).** Yes for the limits and the grid: every result agrees
with the spec's rules, bit for bit. Negative zero, previously unknown, is now settled. No range
guard exists. Evidence:
[x2-notes-launch-v1](../../analysis/ableton-live-12.4.3/r2/x2-notes-launch-v1/manifest.json),
regenerated by `sh run.sh` (about 25 s). The method follows
[extracted execution](extracted-execution.md) (X1). The loader is a copy of
[tools/xexec](../../tools/xexec/xexec.c), `xexec_x2.c`, with one added command, `poke`, which
writes a pointer into a harness buffer. Results are in `results/notes.json` and the summary in
`summary.txt`.

**Functions and matching** (`addresses.json`):

| Role | x86_64 | arm64 | How matched |
| --- | --- | --- | --- |
| Post-load value limits | `0x102a2a7f0` | `0x1028e2c80` | Slot +0xd0 of the AMidiNoteEvent vtable (x86 `0x106d6ab58`, stored by the ctor `0x102a2a660`; arm64 `0x1068256e0`) |
| Copy into the in-memory note, with grid rounding | `0x102a2a9b0` | `0x1028e2e24` | Slot +0 of the translator vtable (x86 `0x106d6ad10`, arm64 `0x106825898`) |
| Per-note event copy, with grid rounding | `0x1026ede60` | `0x1025c7a0c` | Slot +0 of the APerNoteEvent translator vtable `0x106d24b48`; registration `0x1026ed900` |
| Member registration (offsets) | `0x102a2a250` | `0x1028e26c0` | Names mTime +0x30, mDuration +0x38, mVelocity +0x40, mVelocityDeviation +0x44, mOffVelocity +0x48, mProbability +0x4c, mIsEnabled +0x50, mNoteId +0x58 |
| Double and Float member writers (static) | `0x10150f7a0`, `0x10150f6a0` | `0x101520dbc`, `0x101520c70` | Sole references to `#%16.16llX` and `#%8.8X`; they call the P = 17 and P = 9 formatters run in X1 |
| `MidiKey` getter | `0x1029ed3b0` | `0x1028aca40` | Called by the key-map rebuild `0x102a40980` (arm64 `0x1028f5f74`), the first callee of the AMidiNotes post-load `0x102a40180` (arm64 `0x1028f5864`, the sole function that references `Note IDs are not unique` in each slice) |

**Setup.** Each note is a 0x60-byte buffer with the fields at the registered offsets. The run calls the
limits with it, then the copy with the translator subobject (note + 0x28) and a 0x30-byte output.
This follows the load order of REQ-005, then REQ-006. Events use the same layout, at +0x30 to +0x58.
The writers are called as in X1 on the held values. The harness passes the binary64 or binary32 value
of each document text; the text parse itself is not run. No import is called by the limits, the grid
or the getter.

**Results (X).**

- **Limits.** 128 vectors, including every value of MNS-014 to 025. The rules of REQ-005 hold exactly
  at the bounds. Binary32 127.00000762939453 becomes 127, 0.99999994 becomes 1, and −5 OffVelocity
  becomes +0. Negative zero: Velocity −0 becomes 1, OffVelocity and Probability −0 stay −0, and
  Duration −0 stays −0 (the grid then makes it +0). Excluded values: NaN is kept by every rule;
  ±∞ Velocity, OffVelocity and Probability are limited; Duration −∞ becomes 0, and +∞ is kept.
- **Grid.** The REQ-006 binary64 formula equals X for all 128 notes and 9 TimeOffsets, bit for bit.
  That includes the sentinels, ±∞, NaN and 70 values within three binary64 steps of a halfway point.
  Exact halves-away rounding differs from X for 12 of those 70. For example, 1.3007825507825505e-07,
  one step below the binary64 value nearest h/2, is stored as h, where exact rounding gives 0. Time or
  Duration −0 becomes +0; −0.0000001 becomes −0; `Invalid` (DBL_MAX) is not rounded.
- **Text.** The spec examples hold: `0.123456751581751581`, `0.333333333333333315`,
  `-0.000000260156510156510156`, `0.000000260156510156510156`, `80.578949`, `33.2999992`. Negative
  zero is written `-0` by both formatters.
- **MidiKey.** The getter returns 128, 129, −1 and −5 unchanged.

**Static comparison** (`slice-compare.txt`). The limits use `minss`/`minps` with compare masks on x86,
and `fcsel`, `fcmlt`, `fcmgt`, `bit` and `bic` on arm64. The results are the same for every input
class, NaN included: `minss` returns its second operand when unordered. The x86 Ghidra pseudocode of
`0x102a2a7f0` shows NaN changed, as the arm64 pseudocode did; the disassembly governs. The grid
sequence is the same in both slices. arm64's `fmadd` adds the exact product (±h)·0.5, so it rounds
like x86's `mulsd` then `addsd`. The sentinels and constants are equal.

**Q-018 range guard (S, both slices).** Both key-map stores index the 128-slot map at this + 0x28 with
the sign-extended key and no bound check: x86 `0x102a40980` (`cltq`; `mov %r13,(%rbx,%rax,8)`) and
`0x102a3fce0`, arm64 `0x1028f5f74` and `0x1028f5420`. Key 128 writes this + 0x428. Key 129 writes
this + 0x430, the KeyTrack list pointer that the same post-load reads next. −1 writes this + 0x20
and −5 the vtable pointer. The getter adds no check, and the loader stores the Int directly (N1). The
route named by Q-018 is exhausted: out-of-range keys corrupt the notes object, so they stay excluded.

**Limits.** X shows what these functions compute for these inputs. That the load reaches them in
this order with the context flag set is the static A1 of the spec. That the save writes the held
value through these formatters is static (the copy-out `0x102a2aaf0` copies; the member writers
branch only for non-finite values and DBL_MAX). The writers use glibc `log10` and `vsnprintf`, as
in X1. The arm64 equivalence is a static inference.

## Corrections

Dated notes. The text above is kept as written. The evidence is the midi-note-storage-v1
review directory:
[review-checks.txt](../../analysis/ableton-live-12.4.3/handoff-staging/midi-note-storage-v1-analysis/review/review-checks.txt)
and
[corpus-excerpts.jsonl](../../analysis/ableton-live-12.4.3/handoff-staging/midi-note-storage-v1-analysis/review/corpus-excerpts.jsonl)
("review excerpts").

- **2026-10-18, load-context flag (review RVN-01).** Reader step 4, MN-09 and the Limitations
  call the flag `+0x2c` inferred and tie it to the note clamps only. It gates every post-load
  slot `+0xd0`. That covers the note clamps `0x1028e2c80`, the `AMidiNotes` post-load
  `0x1028f5864` (NoteId check, NextId raise, orphan removal, zero-id numbering, groups), the
  store `0x10292cd70` and the list `0x10292b730`. The reviewer established statically that the
  flag is set when a Live Set is read. Every context constructor stores 1. The only clear,
  `0x1015192b8`, is reached from the undo-history streams `0x101546518` and `0x101547ef4`. The
  general XML reader `0x101484108` builds a fresh context through `0x101478258` and
  `0x10151e0d8` (review-checks section 2). Residual: an inlined clear elsewhere is not
  excluded. A clip-file read was not traced separately.
- **2026-10-18, per-note list boundary step (review RVN-02).** The per-note expression
  section omits one load step. After the orphan removal, `0x1028f5864` passes each note's
  NoteId and Duration to `0x10292c960` (`0x1028f5bec`–`0x1028f5c0c`, retained S7
  disassembly). That function calls `0x10292b9ec` on each list of that NoteId and then
  removes lists left with no events. `0x10292b9ec` leaves a list unchanged when it has
  events, its first TimeOffset is above 0 and its last is below the Duration. Otherwise it
  adjusts the list through a call whose semantics were not traced. The step was found in
  query round d4-0001, which was not retained. The review re-established it from the review
  excerpts (chunk-02023, offsets 170246 and 201797, code hashes equal to the d4-0001 files)
  and an image decode (review-checks section 3).
- **2026-10-18, extracted execution (X2).** The reader step 4 and the missing-items table say
  NaN survives the clamps. X agrees, and the x86 pseudocode's contrary reading is wrong too.
  The unknowns list keeps the MidiKey effect unknown. X2 traced the stores in both slices and
  found no guard, so the effect is memory corruption of the notes object and stays excluded
  (see [X2 results](#extracted-execution-results-x2-2026-10-18)). Negative zero is no longer
  unknown: it is kept, rounded or written as stated there.
- **2026-10-18, NoteId text (spec r1 MN-23; plan F7).** In the missing and malformed items
  table, trailing spaces are accepted only when no space or `+` precedes the digits; spaces
  on both sides are unknown. "Overflow" means a value above 9,223,372,036,854,775,807. The
  conversion `0x101524d8c` is signed 64-bit (review excerpts, chunk-00813 offset 61888), and
  the 63-character limit counts leading zeros.

## Limitations

Static evidence only. A traced store or throw does not prove that the path runs for a given file.
The top-level load, its catch and undo or editor behaviour were not traced. The post-load clamps
depend on an inferred context flag (corrected 2026-10-18: see [Corrections](#corrections)).
Ghidra `FUN_` names are generated. Demangled names come from the symbol table and are
evidence, not proof. Pseudocode was checked against disassembly only where marked ✓. Shipped
documents are not 12.4.3 saves, and 103 binary grooves were not parsed. Document text and
recovered strings are treated as data.

## Family route map — pending independent review, 2026-10-20 20:37 UTC

The analyst [MIDI note-storage family packet](../../analysis/ableton-live-12.4.3/full-spec-v1/family-midi-note-routes-v1/structure.md)
cuts SPEC-MIDI-NOTE-STORAGE revision 4 from approved integration packet 1b,
I-01/I-02/I-06/I-10, and the approved playback family map. Its
[ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/family-midi-note-routes-v1/route-ledger.json)
enumerates 88 required predicates: 12 X routes, 52 S routes and 24 with no
established route. These are bounded route inventory counts, not grades,
coverage percentages or a frozen whole-product denominator. All 75 case IDs
are unchanged; 17 auxiliary clauses and 12 excluded/unresolved scope records
remain separate. REQ-011 defines no required outcome for unsafe, missing or
duplicate MidiKeys, so its getter/stores are auxiliary and it contributes no
required predicate. The six group-shape cases remain blocked.

The packet retains A1 as established statically for Live Set post-read checks,
A2 for every saved comparison and A3 for inferred per-field parser binding.
Generic loading/writing does not prove the public Save/catch lifecycle or
loaded-note-to-active-player delivery. Expression boundary adjustment through
virtual `+0x308`, group XML/save shape, list-Id preservation, unsorted/overlap
persistence and the empty-KeyTrack gate remain explicit gaps. Covered negative
zero parsing cites the retained transport/parser and v2 review evidence;
X2 note-limit/grid buffers alone did not parse the text.

Four unexecuted finite batch candidates reference 161 historical result rows
through six exact raw command rows, with retained inputs, setup and gdb-script
identities. These rows are neither outcomes nor call counts and do not authorize
new object construction. The
[author check](../../analysis/ableton-live-12.4.3/full-spec-v1/family-midi-note-routes-v1/author-check.json)
checks documentary integrity, source/case identities and the unchanged research
prefix. Root owns the seal, one independent structure review and shared atlas,
index, plan, coverage and log changes. No original/provider/harness/decoder
execution, normative change or new behavior grade occurred.


### Family route review adopted — 2026-10-20

The [frozen MIDI storage map](../../analysis/ableton-live-12.4.3/full-spec-v1/family-midi-note-routes-v1/manifest.json)
[passed independent review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/family-midi-note-routes-v1-review.json)
with no finding. Its 88 required predicates (12 X / 52 S / 24 without an
established route) remain inventory, not grades. The review checked all 17
requirements, 71 parent-clause dispositions, 75 case identities and 52 source
rows. REQ-011's undefined unsafe inputs have no required reference outcome;
getter/stores remain auxiliary. Six group-shape cases stay blocked and envelope
adjustment virtual +0x308 remains unresolved. Admission-only MNS-036/070 does
not establish their saved result. Actual public Save, error recovery and active
player delivery remain unjoined. No normative clause, case or release changed.


## Probability-group source-depth batch — 2026-10-20 (pending review)

Following the approved family map, one [source batch](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-midi-probability-groups-v1/README.md)
addresses all five REQ-015 questions and all six shape-blocked MNS-054–059
cases. It retains 39 exact C1 records/86,545 C bytes from 16 approved-input
chunks, five inherited conditional class-table rows and 70 native call-index
rows. GroupId's child flag and NoteId's attribute flag support concrete proposed
XML; ordered enum labels associate 0/1 with PlayAll/PlayOne without proving
playback meaning. Generic list/array/class writer links remain conditional.

The batch explicitly rejects expanded C beyond the native callback/registration
bodies: the four-byte wrapper tail-jumps to the 176-byte notifier, and the
244-byte registration body is distinct from the actual AMidiNotes post-load
record. Local NoteId-to-group map insertion is not proof of active behavior,
final saved text, public load/save or absence of all group-counter repair.
Six complete Notes-fragment proposals materialize existing case setups, but
current r4 cases remain shape-blocked until separate owner adoption/review.
The old statement that shape was known only from schema is now historical;
this new evidence is pending independent review and grants no normative change,
original execution, behavior grade, new case ID or release.


## Group source approval and r5 owner refinement — 2026-10-20

The [independent source review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/depth-midi-probability-groups-v1-review.json)
approves the conditional evidence/proposal batch, manifest SHA256
`ff7497c86f2979399cea18f90b7a3741df1894191ce73b56c0011f882f48bcdb`;
review SHA256 `facf6bdf5cb017f8d964b8f8928992df186397074506a6c6ebfb43810dc16600`.
It supports the GroupId child/NoteId attribute shape, 0/1 internal label association,
bounded map registration and six concrete Notes fragments. Pending-source-review
prose above is author history. It proves no public Save, later missing-note effect,
unsupported enum admission or whole-load group-counter repair.

The separate [r5 owner refinement](../../analysis/ableton-live-12.4.3/full-spec-v1/midi-probability-groups-owner-r5/README.md)
is **pending independent owner review**. It adopts those conditional shapes in
REQ-015/Fragment G and the six existing 054–059 cases as four refusal/two
admission-only expectations. All 16 other bodies/69 other rows and all17/75 IDs
are preserved. Saved group state and later effects remain U; no original or
candidate ran, and current v2/72 released cases remain unchanged. The r4 family
map stays frozen; the refinement's route delta supplies qualified current context
without inventing a new whole-family denominator or application grade.


## Group r5 owner approval — 2026-10-20

The [separate owner review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/midi-probability-groups-owner-r5-review.json)
approves the [six-case refinement](../../analysis/ableton-live-12.4.3/full-spec-v1/midi-probability-groups-owner-r5/README.md).
Root [adopted](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/midi-probability-groups-owner-r5-adoption.json)
the exact reviewed draft with an additive current disposition, preserving all
reviewed bytes. Earlier pending-owner text is author history. All six former
shape-blocked cases now have concrete conditional static reader expectations;
only admission/refusal is assessed. Final Save, later missing-note behavior,
unsupported enum meaning and whole-load repair stay U. The r4 map is historical
under the qualified route delta, not a new r5 outcome denominator. Current v2's
72 released cases remain unchanged; no application or candidate ran.


## Current partial release v3 — 2026-10-20

[MIDI note storage v3](../../handoff/midi-note-storage-v3/README.md) is now the current local partial release,
superseding v2 with72 case objects/fixtures carried exactly plus six conditional
local group comparisons. Its14 partial requirement bodies include bounded REQ015;
011/012/017 remain unreleased. [Review and publication record](../specs/midi-note-storage-v3-handoff-plan.md#review-outcome-and-current-disposition)
pins content/correction/final exact-tree approval and manifest `fa281c37472e13a6ba840499687e90928654c9862582fa5bd4d04f4436da7c2c`.
Earlier current-v2 statements above record the as-of owner-adoption history;
this dated release disposition governs. No original/candidate execution,
compatibility grade or new public load/save/later-effect/counter-repair result.
All 75 draft IDs and the historical r4 family-map inventory remain unchanged.

## Remaining MIDI storage unknowns: one source batch — 2026-10-20

**Source/proposals only; independent review pending.** The
[remaining-U packet](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-midi-storage-remaining-u-v1/README.md)
follows the reviewed MIDI family map, r5 group source/owner refinement and
midi-note-storage-v3 publication. It addresses all eight remaining U case IDs
(MNS-011,024,034,035,037,038,053,060) together, plus final group Save, later
missing-note effects and whole-load counter repair. These eleven bounded
questions add no case IDs, required-outcome denominator, adopted expectation,
behavior grade, owner revision or release.

The selected Int64 wrapper/converter supports the existing local mixed-space
refusal reading, while public error/remaining state stays unknown. `Invalid`
Time is not ordinary grid rounding, but final note retention/text remains
unjoined to Save. Negative counters stay excluded, and sorting a collected
NoteId vector is not proof that the notes are sorted. MNS-037 keeps **zero
required safe-refusal outcomes**; no guard or defined reference outcome is
manufactured for unsafe, missing or duplicate MidiKeys.

For MNS-038, the constructor/KeyTrack descriptor and inherited RemoteableList
+140 wrapper conditionally reach the generic list loader's explicit duplicate
parsed-Id refusal. This is a new local source proposal, not an adopted public
load outcome; saved Id identity/meaning and empty-KeyTrack flag ownership
remain unknown. For MNS-053, the receiver frontier narrows to conditional
APerNoteAutomationAdapter vptr1067decd8, whose +308 slot reaches a four-byte
thunk 1025c6068→312-byte body 1025c606c. Its +2e8/+398 targets 10256314c/1025654e8,
transaction helpers and underlying event-array effects remain untraced. All
four existing boundary variants remain U. Retained indirect sites 1025c6110/1025c6148
stay unresolved; main resolution inventory receives zero credit.

[Exact source locators](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-midi-storage-remaining-u-v1/source-locators.json)
reuse 25 already retained records without copying them again, and retain six
needed existing C1 projections once from two approved hash-pinned chunks.
Twenty-five exact C spans, two inherited class-row projections, eight existing
call rows and two unresolved indirect rows preserve version/body/chunk/byte
provenance. The thunk's expanded C is not a second implementation. The older
group callback/registration body boundaries remain in force.

MNS-060 still needs the shared ALS009 public catch/presentation/rollback
receiver. Group writer shape and local registration are not final Save or
later playback/listener effects, and note-counter repair is not group-counter
repair across a whole load. A1, A2/A3, supplied-counter and valid class/receiver
premises remain distinct. All broader existing exclusions remain unchanged.

[Data-only integrity checks](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-midi-storage-remaining-u-v1/author-check.json)
include eight negative controls against omitted questions, unsafe-key oracle
creation, local-to-public promotion and body/slot/span corruption. No original,
provider/native/binary/decoder/harness/model/comparator/module/fixture/build
execution or old-script import occurs. Only targeted retained source/index
lookups and stdlib integrity checks were used. Any later owner reconciliation
must separately review the whole proposal batch; this packet changes none.


## Remaining-U source batch review approval — 2026-10-20

Root read the complete [independent source/proposal review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/depth-midi-storage-remaining-u-v1-review.json), SHA256 `bd3052e837d596467e221313f46190caba54d55d30b7230406b40b6d57ac24c8`. It approves [manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-midi-storage-remaining-u-v1/manifest.json) `6b5b0f4a9a7ba99af6d23ea546bdf496a4bd86bdda990cc9e6589eac441a83f0`,9payloads/93,941bytes as bounded retained-source facts/proposals only. All eight existing U cases and three retained group gaps were assessed together. The local mixed-space parser and duplicate-list-Id refusal proposals retain field/class/ordinary-reader premises; they do not establish public Open, catch, remaining state or Save.

MNS053 now has a qualified adapter constructor/vptr/thunk/body frontier, but all four expression variants stay U. Two native sites remain unresolved, adding zero indirect-resolution credit. Unsafe MNS037 still has zero required safe-refusal outcomes. Group final Save, later missing-note effects and whole-load counter ordering remain U. The reviewer used independent read-only assertions rather than the supplied checker's final frozen-file write; nine payloads/23pins/31source records/25spans/class/call rows and six independent negatives were checked. No original/native/provider/binary/decoder/harness/model/comparator/fixture/build or inherited module execution occurred.

The preceding unreviewed section is author history. Root separately selected one r6 owner reconciliation across this whole eleven-question batch; source approval itself changes no expectation, case, grade or release. Existing public U cases must remain qualified; any local comparison needs its own explicit scope.


## Four expression-boundary variants: range-operation source frontier — 2026-10-20

Pending independent source review: Root selected [both conditional range-operation bodies](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-midi-expression-boundaries-v1/README.md) from the approved remaining-U frontier in one bounded source batch across all four MNS053 variants. Exact retained C1 entries10256314c/1025654e8 contain4,966UTF8Cbytes/166lines;836/320native body bytes are retained metadata, not fresh instruction coverage. Forward/backward comparison strictness, indexed mutation requests and count-like traversal are visible in source. Actual list/provider/callback identity, indexed mutation10156da64, first-call interval global values, transaction effects and resulting event arrays remain unknown. No encountered callee/slot/global was followed; all four variants retain null expected/actual, adding zero indirect-site or grade credit.

The [owned read-only checks](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-midi-expression-boundaries-v1/author-check.json) pass selected source/pin/span integrity and five false-promotion controls. One wrapper-format assumption failed before writes and was corrected directly against the existing record field, with disclosure in findings; no frozen adapter. No original/native/provider/decoder/harness/model/comparator/fixture/build or inherited-module execution occurred. This source packet is separate from r6 owner review and changes no requirement, case or release.


## R6 owner adopted; v4 staging selected — 2026-10-20

Root read the [separate r6 owner review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/midi-storage-remaining-u-owner-r6-review.json), SHA256 `492476f9376b1f2ff2e8f558b30d3fedae4bca828136e3d717a2aa15a7d8ab84`, and [adopted](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/midi-storage-remaining-u-owner-r6-root-adoption.json) its exact72,839-byte reviewed prefix. Only002/012/014bodies change; all75oldrows/14otherbodies/allXclauses/eightpublicUrows remain exact.076/077 are separate conditional local-reader comparison projections, not public Open/rollback/Save or a mandated native API/pipeline.77draft IDs are navigation, not an outcome denominator. Twelve false-promotion controls and40local links passed; the review's initially reported54-link chat count was corrected to its recorded40without rewriting evidence.

V4 staging is separately selected:78v3case objects/78existinggzip fixtures carried byte-exact, plus exactlytwo local comparisons via explicit data-only edits over the existing authored MNS001fixture. No new carrier generation is needed. Existing14requirement bodies stay exact; the002local supplement and newpartial012yield15partial IDs. Content review, exact-tree approval and full prerelease lint must precede local publication. V3 remains current; no original/candidate or compatibility grade follows. The concurrent expression source packet remains a separate review/adoption and supplies no new r6 outcome.


## Expression range-operation source review approval — 2026-10-20

Root read the complete [separate source review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/depth-midi-expression-boundaries-v1-review.json), SHA256 `60f16989eebef6be56fe17a0b153b3f04ae6fe9109598b605473cd1f0f779595`, and adopted only its bounded frontier. Eight payloads/27,524bytes/two C1records/4,966Cbytes/seven exactspans and five false-promotion controls were verified;17watched paths unchanged. Native836/320-byte extents are retained metadata, not fresh instruction coverage. Conditional comparison strictness is supported as C syntax; inferred list/count roles, underlying provider/index mutation/callbacks/interval globals/transaction effects do not become resulting event-array laws. Allfour MNS053variants remainU; no indirect-site credit, owner/case/criterion/release change or successor follows. The preceding pending source section is author history, distinct from the already approved r6 owner and v4 staging.


## V4 local partial release — 2026-10-20

[MIDI v4 publication](../specs/midi-note-storage-v4-handoff-plan.md#current-local-publication--2026-10-20)
is complete after independent content approval, separate final exact-tree seal
and full prerelease lint.83payloads/223,995bytes plus24,458-byte manifest copied
exactly; all84destination files verified.78oldcaseobjects/78gzip/14oldbodies exact,
two local comparisons reuse existing authored MNS001with explicit Notes edits.
No new fixture, original/candidate execution, compatibility grade or publicU
resolution. V3 is immutable/superseded; v4 is current. Allfour053variants and
group final Save/later effects/counter order remainU.36releases/19current/17superseded
are catalog units, not outcomes. The pending/current-v3 statements above retain
their dated histories. No implementation or restricted-workspace update selected.

## Standing whole-class selection assessment — 2026-10-21

The approved [12-X family map](../../analysis/ableton-live-12.4.3/full-spec-v1/family-midi-note-routes-v1/manifest.json),2,866bytes/SHA-256 `96547699ca57189013abd582f7c0657a87ce540459dfc7481716cd9caff49a95`, currently identifies existing128note-limit/copy/grid vectors, nine offset-grid inputs,22text-number inputs and two typed negative-zero parser inputs. The bounded selection assessment consulted retained map/input metadata and current R6/v4 dispositions, without replaying oldraw/source behavior or originals. No mapped whole unrun standing class was found. This is a current eligibility result, not proof that further legal classes cannot exist.

Remaining MNS-053/public mutation/provider/Save/transaction/sorted-ID joins require a legal receiver/state or a separate evidence route; another arbitrary scalar sweep would not close them. Existing finite refinements/releasev4 remain exact. No new original run/model/tool/source frontier or owner/case/release/grade/site is selected. Frozen691X/1,076S/3,857none/main25,071+24=25,095of268,015/bundlesseparate/requiredUproductOPEN.


## All-four MNS-053 frontier metadata selected — 2026-10-23

The [approved expression-boundaries source report](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/depth-midi-expression-boundaries-v1-review.json),5293bytes/SHA256 `60f16989eebef6be56fe17a0b153b3f04ae6fe9109598b605473cd1f0f779595`, `/semantic_assessment`, supplies one coherent remaining metadata question across **allfour MNS-053variants**. CanonicalEvidence binds this study to Live.arm64/3a99…cfad, not an inferred same-number x86function. Currentr6/v4refinements, publicOpen/Save/mutation/provider/transaction/sorted-ID gaps, allcaseIDs/criteria/releases and null expected/actual values stayexact.

Select ONE **depth-midi-MNS053-frontier-metadata-v1**:recover exact declared range topology/HEADER_STATUSmetadata for the two already reviewed source bodies0x10256314c/0x1025654e8(retained native counts836/320bytes, not instruction coverage); census exactARMalias/export/C1declarations for the two newly named direct-callee keys0x10156da64/0x10156d4c8; classify the two interval-global keys0x105847020/0x105847028through inherited approved mapmetadata, with contents/accesswidth/objectextentUunless explicitly admitted. Carry unresolved provider predicates **slot offsets**+0x3c8/+0x3d8/+0x250asoffsets, never absolute addresses. Unnamed transaction-helper/current receiver/list/provider/callback and resulting-event-array questions remainU; no arbitrary scalar sweep or convenient single-variant subset.

A finite whitelist may first inspect approved oldmanifestnames/pins and the retained two C1records' HEADER_STATUS/ranges only, with C/code/optext opaque. This is topology reuse, not a second source-semantic review. CorrectARMauthority only; no numeric lookup in a different architecture. External rows must be excluded before hexadecimal parsing and ordinals count only nonexternalrows. New meaningful actual-shaped external/malformed/ordinal/overlap/opaque-invariance controls and fully read/prebound new methods/PREPythoneligibility precede one census. No oldhelper/checker/fixture/decoder/proof replay, source-body/native/image/header/vtable/pointee/runtime/model/provider/guest/QMP/UI/media/profile/AUZ or opaque-scope action.

Tension_review_finish authors; tension_owner_finish solely reviews after its separate Automationv2authoring, never its own packet; RootCITEONLY. Preserve minimum7893696512bytes or larger full6039814144currentconcurrent plus12MiBremaining-parent/output/log/512MiBfinal/128MiBheadroom allowances from the first point, without trimming, deletion or Analog59subset. Onefinalfreeze/sole report with SAFEunderstanding/completequestionunion/qualified geometry/lineage/limits/history, no new preparation/review gate or automatic acquisition retry/body follow. This metadata selection changes no case, criterion, grade, site, O, release or whole-product completion.


## MNS-053 preparation stopped before acquisition — 2026-10-23

The selected all-four-variant packet remains **unbound/unsealed preparation**, not acquired metadata or approved evidence. Its [retained resource stop](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/depth-midi-MNS053-frontier-metadata-v1/resource-stop-PREACQUISITION.json),770bytes/SHA256 `ca4cd02b3533e3454007c704c7f3b844500cbf99e9c2d620b600ebed27951931`, records3313270784available bytes against7893696512required, full6039814144concurrent unchanged, at2026-10-23T16:24:29UTC. The prebinding builder failed its capacity assertion before writing a binding. Because the next shell command was not conditional, controls.py then launched and failed opening missing prebinding.json before any method import, owned fixture/control, interpreter eligibility check or original-source operation. Both preparation failures remain retained; do not call this zero command launches or passing controls.

No original metadata census/parent read, binding/control result or sole review exists. All four MNS-053 variants and the unnamed joins remainU; no r6/v4case/criterion/release change. Hold further preparation and acquisition until actual capacity satisfies the unchanged full contract. Do not lower budgets, trim the class, delete retained evidence or substitute an Analog59 subset. This environmental stop is not metadata-route exhaustion or whole-product progress.


## All-four metadata preparation resumed after capacity change — 2026-10-23

The user says “proceed” after cleanup changed actualcapacity. Explicitly resume fresh fullbudget admission/newbinding, followed only by the **first unused owned controls and first once-only original metadata census** in the already-selected allfourMNS053packet. Preserve the failed prebindingbuilder and subsequent unconditionalcontrolslaunch/missing-binding trace,770byte resource-stop record and zero fixture/import/source outcome; no completed proof prefix or oldhelper/checker is replayed. Original unbound methods must be fully read/control/prebound and PREPython312-I-Beligible before firstuse.

Same complete question/architecture/offset predicates/zero contentsemantics/full6039814144concurrent+lifecycle/7893696512minimum-or-larger/fullhistory/firstfault rules remain. Tension_review authors, tension_owner solelyreviews afterfreeze and its independentAutomationauthoringboundary; RootCITEONLY. Later soleAnalog59review is a differentpacket, never an own-source review. No Source/native fact, publicMNS053expectation, case/criterion/release or evidencegrade changes at resumption; wholeLiveOPEN and Claudeguesthold unchanged.


## All-four frontier metadata adopted — 2026-10-23

The [sole metadata review](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/midi-MNS053-frontier-metadata-v1-review.json),70392bytes/SHA256 `c624a64a30ad32a49963f74916292dd26849803501a1eb21fb42c928ac7fdcdc`, approves only qualified metadata across **MNS-053(a)–(d)**. [Manifest](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/depth-midi-MNS053-frontier-metadata-v1/manifest.json),5348bytes/SHA256 `534f1700d7a63d2415af94ea22ce81b1b39625465ef580aa61792f1adcc31262`, seals33payloads223621bytes/all34files0444/private0700 unchanged. Root verified the sole-report pin and read only its whitelisted approvedSAFE/understanding/wholeunion/geometry/global-slot/lineage/limits/history/checker/tree projections, no original C/native/parent/proof/helper replay.

All six approved groups are at `/approved_understanding_METADATA/groups`:

| Group | Qualified metadata understanding |
| --- | --- |
| MNSMETA01 | The complete question is all four canonical MNS-053 variants(a)-(d), not one example. Each retains null expected/actual and unknown public Open/Save, resulting event array, mutation, callback/provider and lifecycle joins. Current owner r6 and local partial release v4 remain unchanged; no new standalone case IDs or released outcomes are created. |
| MNSMETA02 | HEADER_STATUS/range topology reuse, with old C/code/optext excluded, locates the two already source-reviewed declarations as separate single ranges:836B[0x10256314c,0x102563490) and320B[0x1025654e8,0x102565628), both in inherited ARM64 __TEXT/__text mapping. Prior source comparison/strictness syntax is inherited solely from the approved5293B review; it is not rederived here. Native instruction coverage remains zero. The836B record retains global-symbol-overlap and subroutine-does-not-return decompiler warnings. These warnings are metadata, not newly established runtime nonreturn, complete CFG, ABI or whole object laws. |
| MNSMETA03 | Both new direct-callee keys have exact unique nonexternal ARM aliases and exact C1 declarations:16B[0x10156da64,0x10156da74) and8B[0x10156d4c8,0x10156d4d0). Nonexternal ordinals83625/83608 select lines26/9 of the same chunk00836. No source expressions or native bodies were selected, so indexed mutation, traversal, event-array behavior and callback semantics remain unknown. The16B record warns that the jumptable at0x10156da70 could not be recovered and that an indirect jump was treated as a call. That is a decompiler warning locator only; it does not resolve an actual site/target or certify whole runtime implementation extent. |
| MNSMETA04 | The complete four-declaration topology is four disjoint ranges/1180 declared native bytes/295 prospective four-byte rows. Bounded overlap against inherited240 selected native ranges is zero; global novelty, ownership, cold/exception/all-exit extent and actual ABI remain unknown. This is a whole future metadata nomination, not selected native/C content or a completed behavior profile. |
| MNSMETA05 | The two interval-global keys0x105847020 and0x105847028 map to inherited __TEXT/__const file points92565536 and92565544. Their contents, access widths and whole object extents remain unknown. Eight-byte spacing is not evidence for reading eight bytes, a double interpretation, a complete interval object or a zero value. |
| MNSMETA06 | Provider+0x3c8/+0x3d8/+0x250 remain three slot-offset predicates with unknown actual site PCs, receiver/vptr/provider and target binding. They are not absolute addresses and were never queried as index keys. Unnamed transaction helpers/current receiver/list/callback identities and public resulting event arrays remain unknown; no automatic callee/body/global/pointee follow, source-runtime replay or numeric sweep is selected. |

The complete four declared ranges are836B `[10256314c,102563490)`/fileoffset39203148;320B `[1025654e8,102565628)`/39212264;16B `[10156da64,10156da74)`/22469220;8B `[10156d4c8,10156d4d0)`/22467784, all inheritedARM64`__TEXT/__text`. Fourdisjointfragments total1180bytes/295**prospective**rows, zero boundedprior240nativeoverlap; globalnovelty/ownership/runtimeCFG/ABI stayU. The newcallee sizes are16+8, not an assumed equal-size pair. OldC1hash/countfields aredeclaredmetadata/not recomputed Csemantics. The836Bnonreturn/globaloverlap and16Bunrecoveredjumptable/indirect-jump-as-call warnings remainwarnings, not runtimefacts or indirectresolution. No body/nativecontent was selected or read.

The globalpoints `105847020`/`105847028` maptofilepoints92565536/92565544 in`__TEXT/__const`, with widths/contents/objectextentsU; eightbytespacing proves no eightbyte access or doublevalue. Provider`+3c8/+3d8/+250` remainoffsetpredicates, notaddresses/sitePCs. Unnamedtransaction/currentreceiver/list/provider/callback, finalarrays/mutation/sortedIDs/Open/Save/lifecycle remainU/null. Currentownerr6/localreleasev4/oldcases/criteria/expectations/fixtures stayexact; no standaloneIDs wereinvented for the fourexistingvariants.

Freshcustody covers threephysicalparents122426303bytes:6014byte oldsource-rows parent with C/code/optextopaque,122340555bytealiases and79734byte C1parent. Actualnonexternalordinals83625/83608 locate newrecords atchunk00836lines26/9; aliases420470total/418417eligible/2053external skippedbeforeparse. Four endpoints/size/hash matching is boundedcustody, not continuousstability/ancestorhistory/snapshot/crashdurability. Inheritedmap/image/header/oldSourcecomparison semantics were not reacquired/reviewed. SourceC/native/MachOheader/vtable/slot/global/pointeesemanticbytes selected:zero.

Five newmethods199lines/firsteligible20ownednegatives/oneoncecensus/oneauthorsafecheck passed. Solepeer ranonlythatneweligiblecheckeronce/217bytestdout exact/emptyerr plus tenindependentmetadatanegatives; all34filesunchanged. The checker reads a fixedPythonidentity inadditiontopacket and reexecutes onlynew ownedmetadatamethods/controls, notoldSource/decoder/helper/nativeproof. OwnPython312-I-B/sourceeligibility and effectiveparentCPU60/AS1GiB/FSIZE12MiB/NOFILE256/STACK8MiB were recordedPREsource; nochild/tool waslaunched, no wallwatchdog/transitiveruntime identity claim.

Thirteenadmittedresume resourcepoints hadminimumstorefree13693661184 versus unchangedneed7893696512/full6039814144concurrentFROMRESUMESTART/tenunchanged12MiBunits+metadataoutput/final/headroom. **These are store-filesystem points**, notseparateroot/physicalRAM measurements, quota orcontinuouscapacity. Earlier770bytecapacitystop and768byte missing-bindingstderr remainexact. That unconditionalfailedcontrolsprocess is failedorchestrationhistory, notcleanfirstfault; it stoppedbeforemethodimport/Pythoneligibility/actualfixtures/Source. Freshresume admitted FIRSTunusedcontrols andFIRSToncecensus, no failedprefix relabelled or oldproofreplay. Prior146checker-textdisplayexception remainscite-only history. No automaticbody/global/provider/pointee successor or case/grade/site/O/release/wholeclosure credit.


## Whole four-declaration native question selected — 2026-10-23

After sole metadata approval, explicitly select ONE **depth-midi-MNS053-four-declarations-native-v1** for allfour admitted ARMdeclarations:836B `[10256314c,102563490)`/fileoffset39203148;320B `[1025654e8,102565628)`/39212264;16B `[10156da64,10156da74)`/22469220;8B `[10156d4c8,10156d4d0)`/22467784. Wholeunion **1180newnativebytes/fourseparateexactpreads/295prospectiverows**, no convenientvariant subset. One preferred149711904byte ARMimageROFD/fresh3a99…cfadwholehash; inheritedapprovedgeometry/map only. No oldC1/alias/source-rows/bodysemanticproof, MachOheader/vtable/slot/global/pointee/string/neighbor/field contents or callee-body follow. The two globalpoints have no admitted accesswidth; eightbytespacing still grants no read.

Authority is the [70392byte approved metadata report](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/midi-MNS053-frontier-metadata-v1-review.json),SHA256 `c624a64a30ad32a49963f74916292dd26849803501a1eb21fb42c928ac7fdcdc`, its whitelisted declaredgeometry/wholequestion/Source-lineage/limits/history. Carry oldSourcecomparisonsemantics and both decompilerwarningclasses bycitation; nativecode must establish any NEWlocal instruction/branch/site understanding, never turn a warninglocation/nonreturnlabel into proof. FormalABI/currentreceiver/provider, completeCFG/all-exits/objectextents/FPnumericlaws/publicoutcomes remainU unlessnewscope evidence actuallysupports a narrowly qualified local claim.

O137authors afteritsclosedAnalog59authoringboundary; tension_review solelyreviews frozenNEWnative/code/understanding afteritsclosedClipauthoring/Analog59sole-reviewboundary. RootCITEONLY. O137's separateAutoV3sole-review role takesplaceonlyataclosedMNSauthoringboundary, neverinterrupting Source/decoder/checkerprefixes and neverreviewingthisownMNSnativepacket. AllfourexistingMNS053(a)–(d)/r6/v4/IDs/criteria/releases/nullpublicexpectations remainexact.

Fullyread/control/prebindNEWmethods/PREPython312-I-B/pinnedRizinidentity and prospectiveparent-to-child CPU/AS/FSIZE/NOFILE/STACK/COREcompatibility beforeFIRSTuse. Use byte-count `pDj LEN(raw)` ononlyownbuffers, no ESIL/emu/analysis/originalcode invocation. Necessary NEWownedfixtures include one whole836bytefixedword case to test fullbytecoverage past the observed256byteboundary; preserve exactrawtooloutput and formatter/type/ptr qualifications. No oldtoys/helper/checker/fixture/proofprefix replay, automaticretry/tweak or alternativedecoder. StopfirstfaultandcheckeveryresultbeforelaterSource/toolstep; retainwholepartialifanyunitfails.

From START retain full6039814144currentconcurrent plus allparent/fourbody/twoownedtoy/output/log/final/headroom allowances, minimum7893696512or largercompletecontract at everyrequiredstep; no actual-size/budget/scopecut/deletion/Analog59subset. Onefinalfreeze/solepeer/directSAFEallgroups/entirecalls-sites-fields-return-nominationunion/allgeometry/lineage/qualifiedlimits/history. Newunreadtarget/site/field/objectquestions are nominationsonly, no automaticfollow. No originalfunction/application/Xaudio/reference/runtime/model/provider/FP/opaque, VM/guest/QMP/UI/media/profile/AUZ action (Claudehold), case/grade/site/O/release/productclosure credit.


### Native sole reviewer scheduling amendment — 2026-10-23

Tension_review confirmed its queuedMNS4nativepayload/method/checker review had notbegun, with only activationmetadata received while itsAnalog59review remainedactive. Root reassigned **one sole MNS4nativepeer to tension_owner after itsAutoV3finalfreeze/closedauthoringboundary**; tension_review's unbegunqueuednative review was withdrawn. O137remains nativeauthor. Frozenauthorselection naming the earlier reviewer isasof schedulehistory. OldMNSmetadatareview and newnativeproof remain distinct; no ownpacketreview, interruptedSource/checkerprefix, second actualreview, Rootgate or Source/behavioral expansion follows.


## All-four declaration native review adopted — 2026-10-23

The [sole native review](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/mns053-native-peer-work/midi-MNS053-four-declarations-native-v1-review.json), **261,055 bytes**, SHA256 `8345810a780c3e086d7910fb8edd392a0f47360ef2bcfcbd7a9eb4aa463b17a4`, approves the selected static cohort and conditional local annotations, with the bootstrap evidence limit below. Its `/approved_SAFE_scalar`, `/approved_understanding`, `/approved_complete_question_union`, `/approved_all4_geometry_METADATA`, `/approved_source_lineage_METADATA`, `/approved_image_custody_METADATA`, `/approved_limits`, `/approved_PRE_chronology_qualification`, `/approved_history` and resource/history projections are the adoption authority. The [frozen native manifest](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/depth-midi-MNS053-four-declarations-native-v1/manifest.json), 8,412 bytes/SHA256 `c918d8b74111bbb08841ae5d5716c4cb65e4bc42a14814b582e4c0ec4fd7af1e`, seals 58 payloads/1,357,520 bytes; all 59 files remained unchanged. No original source, image, index, tool, decoder, old checker or proof was replayed for this documentary adoption.

The author retained **1,180 native bytes in four separate preads and 295 guarded four-byte rows**, covering the complete admitted class:

| ARM64 declared range, end exclusive | Bytes | File offset | Guarded rows |
| --- | ---: | ---: | ---: |
| `[0x10256314c,0x102563490)` | 836 | 39,203,148 | 209 |
| `[0x1025654e8,0x102565628)` | 320 | 39,212,264 | 80 |
| `[0x10156da64,0x10156da74)` | 16 | 22,469,220 | 4 |
| `[0x10156d4c8,0x10156d4d0)` | 8 | 22,467,784 | 2 |

All four use the inherited ARM64 `__TEXT/__text` mapping. Declared extents and zero bounded overlap against the inherited 240-range catalogue do not prove global novelty, ownership, complete cold/exception/all-exit extent or an ABI. The earlier metadata sections remain records of their original zero-content scope; this separate native study supplies the new instruction observations. Source comparison semantics and the old C1/header/map authorities remain accepted by citation, without a second source-semantic review.

All twelve conditional groups from `/approved_understanding` are adopted here. These describe visible local instructions under valid memory, reached paths, ordinary outside-call returns and any required register preservation; they do not establish legal runtime receiver state or public outcomes.

| Approved group | Conditional native understanding |
| --- | --- |
| 1 | All four selected ARM declarations are retained as 1,180 bytes/295 guarded rows. All existing MNS-053(a)–(d), owner r6/release v4, IDs, criteria and null public expected/actual values remain unchanged. Open/Save, resulting arrays, sorted IDs, mutation and lifecycle outcomes remain unknown. |
| 2 | In `0x10256314c`, sites `0x102563168`–`0x10256318c` save entry X2/X1/X0 in X19/X20/X21 and pass X0=SP+0x40 and X1=saved entry X0 to direct BL `0x102415e20`. Later roles and the helper-initialized local aggregate remain unknown. Saved-register survival across outside calls is a condition, not an established formal ABI. |
| 3 | Both larger declarations repeatedly load receiver/vptr carriers and use slot displacements 0x60 and 0x20 through X8, then dereference returned storage at +8 and load D registers at +0x50. The inventory locates these carriers; current provider classes, event formats, legal receiver state and callback semantics remain unknown. |
| 4 | The 836-byte body uses two FABD operations, FCMP and B.PL for a direction split; later flag-byte CMPs choose FCMP branches LE/GE, LT/LE, PL/LS and LS/MI on the two legs. Only literal operands, condition codes and destinations are claimed. No FP evaluation, NaN/order law, threshold, interval-inclusion rule or portable numeric model follows. FABD's raw `type=null` remains unchanged. |
| 5 | The BLs at `0x102563354` and `0x1025633bc` to the selected 16-byte helper receive X0 loaded from saved entry receiver+0x58, X1=SP+0x28 and X2 from W22/X22. Forward advance steps increment W22; reverse steps decrement it, seeded from W0 minus 1 on that leg. These narrow argument/cursor/count delivery; actual container mutation and final arrays remain unknown. |
| 6 | The reverse leg at `0x102563370`–`0x102563398` loads a Q0-sized, unread 16-byte window at preferred address `0x1055d9680`, stores Q0 at SP+0x10 and stores the low two bytes of W8=1 at SP+0xe. A runtime slot+0x398 call receives X0=saved entry receiver, X1=SP+0x10 and X2=SP+0xe. The initializer and passed addresses are visible; literal contents, pointee objects, provider meaning and resulting state remain unknown. STRH's raw `type=null` is retained. |
| 7 | The 320-byte entry loads a D-register pair from entry X1, materializes comparison inputs with MOV/MOVK/FMOV transfers and uses FCMP/FCCMP plus B.EQ for a separate dispatch leg. That leg loads runtime slot+0x250, BLRs, restores its frame and tail-branches to selected `0x10156d4c8`. Constant bits remain opaque; no FP/numeric outcome, current target, returned value or public interval rule is established. FCCMP's raw `type=null` remains unchanged. |
| 8 | In the 320-byte body's other leg, first flag byte equal to 1 selects runtime slot+0x3c8; otherwise it selects +0x3d8. Both set X8=SP+8 before BLR; +0x3c8 also clears W1. The new PCs locate transfer carriers without resolving targets or assigning a formal hidden-result ABI. W21 starts at zero, increments on reached advance steps and is copied through X21 to X0 before the ordinary RET; this is a local register counter, not a proved public event count. |
| 9 | All four rows of `0x10156da64` copy entry X1 to X3 and entry X0 to X1, load X4/X0 from entry X0+0x128/+0x130 and BR through X4. X2 is locally unchanged. This carrier/site observation comes from the new native rows, not the inherited jumptable warning. Current pair contents, target, provider and formal ABI remain unknown. |
| 10 | `0x10156d4c8` adds 0x70 to X0 and tail-branches to unread `0x1014670e8`. It establishes neither a local RET nor returned identity. The outside declaration and content remain unselected. |
| 11 | The 836-byte body passes SP+0x40 to cleanup BL `0x102415ebc`, then compares a saved value with a freshly dereferenced ADRP/LDR-derived carrier. Its ordinary path restores the frame and RETs without subsequently normalizing X0, leaving the cleanup-call return in that visible register. A mismatch reaches the separate final BL `0x1054d56b4` at the declared end. Neither this BL nor the historical warning proves runtime nonreturn, exception or fallthrough behavior. |
| 12 | Original global points `0x105847020`/`0x105847028` remain unread, with access widths, values and object extents unknown. New native-only nominations are an 8-byte conditional access at `0x1064f8818` and a 16-byte Q0 access at `0x1055d9680`. These are access windows, not whole-object prefixes, current values or automatic data acquisitions. The three old slot predicates remain ASOF; separately located native load/transfer carriers retain unknown actual targets. |

The complete current frontier is retained at `/approved_complete_question_union`: **4 outside destinations, 20 unresolved indirect sites, 73 bounded numeric candidates, 136 lexical load/store rows, 6 explicit access classes and 2 visible RET rows**. The outside destination keys are `0x1014670e8`, `0x102415e20`, `0x102415ebc` and `0x1054d56b4`; none is followed. The 20 indirect sites retain unknown actual targets. The 73 candidates include scalar/displacement/unsigned-wrapped formatter values, pages and slot offsets; numerical map containment, including PAGEZERO membership, does not promote them to runtime addresses or objects. The memory-row total is **lexical**, not 136 established field widths, complete memory effects or runtime accesses.

The six explicit access classes comprise two unread static windows, three runtime slot-offset carriers and one receiver-relative pair delivery. The static nominations total **24 bytes**, `0x1064f8818`/8 bytes (`__DATA_CONST/__got`, file offset 105,875,480) and `0x1055d9680`/16 bytes (`__TEXT/__const`, file offset 90,019,456). No field contents were acquired. New PCs locate +0x3c8 at load/transfer `0x102565540`/`0x10256554c`, +0x3d8 at `0x1025655f0`/`0x1025655f8`, and +0x250 at `0x1025655d0`/`0x1025655d4`; these remain runtime displacements, not absolute address queries or resolved targets. The pair delivery at `0x10156da6c`/`0x10156da70` has a conditional 16-byte access at entry X0+0x128, with the first eight-byte carrier delivered to X4/BR and the next to X0; its current binding and whole object extent remain unknown. Original global points and the earlier three metadata predicates stay unchanged as their ASOF records. No current provider, receiver, transaction/list/callback identity, resulting arrays or public variant is closed.

### Native custody, bootstrap qualification and retained history

The author used one read-only FD for the 149,711,904-byte standalone ARM64 image, whole SHA256 `3a99ceeabce62ccd069b6b55d99d186c9bdf8a6b80a7e3350dd0f9d1c383cfad`, and the four exact preads above. Before/after path/FD identities matched. Whole-file hashing physically contacts unselected bytes, including the header; only the four native ranges were retained for this study. This does not prove current universal-parent derivation, an atomic snapshot, continuous stability, ancestor-path history or runtime load addresses. Old source/alias/C1/index/header/map proofs and prior Source semantics were inherited, not reacquired or recertified.

Eight new methods/232 lines were read and prebound. The pinned Rizin 0.9.1 static formatter ran only on new owned buffers: two new fixtures and four selected body buffers, **six once-only children, all exit 0/empty stderr**. The 836-byte fixture checks all 209 rows, including the word at byte 256 and final word 832–835; one fixture is not a general decoder guarantee. The short BL/B/RET fixture uses a known standard literal sequence at a new fake address, without replaying an old fixture artifact. Fifteen author pre-use negatives and twelve final retained negatives passed. Passive ESIL strings were data; no emulator, numeric evaluation or original native execution was performed. Raw `type`, `ptr`, `val` and formatter qualifications remain intact.

**Bootstrap evidence limit:** the prebinding writer asserted the 8,020,928-byte Python executable hash but retained only a declaration/boolean for that pre-module check. A separate detailed shell hash/stat/four-endpoint receipt **before first new module evaluation was not retained**. The first detailed `eligible()` receipt is `controls.json/PRE`, after pure module definitions, before actual pure controls, toys and original image use. Later receipts do not establish or retroactively approve earlier bootstrap eligibility. The accepted scope retains that unknown; neither frozen bytes nor history were repaired. Python 3.12 isolated/source dependencies were used, while standard-library and other transitive runtime identities remain unproved. This qualification is explicit at `/approved_PRE_chronology_qualification`.

The resource record has 29 distinct full-bound points: minimum root/store account-available **14,294,315,008 bytes**, required **7,893,696,512 bytes**, and minimum MemAvailable **94,465,011,712 bytes**. Full **6,039,814,144-byte concurrency from START**, twenty unchanged 12-MiB parent units, complete native/metadata/code/six-child-output allowances, 512-MiB final allowance and 128-MiB headroom were preserved without scope/budget cuts. These are unreserved endpoint measurements, not continuous capacity, quota or guest-readiness proof. Requested child limits were CPU 20 seconds, AS 1 GiB, FSIZE 4 MiB, NOFILE 256, STACK 8 MiB and CORE 0, with prospective parent-hard-limit compatibility and a preexec assertion. Child wall timeout was 20 seconds with bounded group cleanup. Parent CPU/AS/FSIZE were unbounded; no parent wall watchdog, independent in-child syscall trace or escaped-descendant guarantee was established. Child maxrss is cumulative. Raw files/JSON receipts were fsynced; formatter stdout/stderr used ordinary close, and directory crash durability remains unproved. See `/approved_limits`, `/approved_resources` and `/approved_resource_qualification`.

The sole peer ran only the eligible frozen-packet safe checker once: 232-byte stdout matched the author's bytes exactly, stderr was empty, and all 59 frozen files stayed unchanged. Its first read-only summary projection used a wrong key and produced a truncated display/KeyError; a later peer audit stopped on a list-versus-dict TypeError after its finite 295-row/branch arithmetic prefix. Fourteen new negatives and that prefix are inferred from the sequential traceback; no intermediate result file was written. The failure source/binding/567-byte traceback remain retained. A new adapter completed only the unused suffix, with three new shape/count negatives and the one still-unused checker; it did not rerun the completed prefix or any original/tool/decoder action. These limits are direct in `/peer_history` and `/sole_safe_checker`, not relabelled clean first-fault orchestration.

The old metadata packet's 770-byte low-capacity stop, subsequent unconditional controls launch/missing-binding failure, and later explicit first-unused-controls/first-census resumption remain history as adopted above. The native author corrected an unsealed prose spelling before the single inspector use; no source/method/row/control acquisition was replayed. The inherited 836-byte global-overlap/nonreturn warnings and 16-byte unrecovered-jumptable/indirect-jump-as-call warnings remain exact warnings. New visible RET and a separate final BL do not establish whole CFG, runtime return/nonreturn, exception behavior, formal ABI, object ownership or global extent, and do not invalidate the historical warnings.

This adoption selects **no successor or new source work**. All four MNS-053(a)–(d), current r6/v4, IDs, criteria, releases, fixtures and null public expected/actual values remain unchanged; Open/Save, mutation, final arrays, sorted IDs, lifecycle and provider joins remain unknown. There is no global-novelty, behavioral/native-grade, resolved-site, case, O, release or whole-Live completion credit. No FP model/evaluation, provider/model expansion, original application/runtime/audio/X experiment, opaque-scope change or guest/QMP/UI/media/profile/AUZ action occurred; Claude's exclusive guest hold remains in force.


### Shared file-window nomination reconciled by approved metadata — 2026-10-23

The native24Bstatic-access nomination remainsasof its Sourcecohort, but the16Bwindow1055d9680 is now known to coincide exactly with a separately approved ClipFILEBITS capture on the same3a99ARMimage/fileoffset90019456. [Cross-cohortreconciliation](program-structure.md#cross-cohort-static-reference-reconciliation--2026-10-23) carries its rawhex/SHA bycitation for this NEWreferenceassociation, without anotherimage/windowread or FP/currentmemory/objectlaw. The other8Bcell1064f8818 remainsunread and issharedwith AutoV3'sfive-cellnomination. Originaltwointervalglobalpoints stillhavewidth/value/extentU; there isno publicMNS053expectation, Sourceproofreplay or automaticfollow.


## Complete four-body dependency metadata class selected — 2026-10-23

Select one **depth-midi-MNS053-four-body-dependency-metadata-v1** after the current independent author/reviewer boundaries. Its authority is the [sole four-body native report](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/mns053-native-peer-work/midi-MNS053-four-declarations-native-v1-review.json),261055bytes/SHA256 `8345810a780c3e086d7910fb8edd392a0f47360ef2bcfcbd7a9eb4aa463b17a4`, approved SAFE understanding, complete question union, geometry, lineage, limits, history and resource projections only. Underlying four-body source, native bytes, decoder, fixtures and proof stay by citation. All four MNS-053 variants, r6/v4 criteria and public Open/Save/event-array/mutation/lifecycle questions remain unchanged unknown.

Account for the entire four-destination/twenty-site/73-candidate/six-access-class frontier. Exact ARM alias/C1 declaration and HEADER_STATUS metadata are selected for `1014670e8`, `102415e20` and `102415ebc`; bounded predecessor topology is permitted only if exact lookup fails. The fourth destination, `1054d56b4`, already has a12-byte declaration in Analog59 `/approved_dependency_nomination_METADATA/all_known242_ranges_METADATA`: carry it by citation, with no old C1 or native reread. Look up function/name/in-thunk/flow/resolved-target metadata for all twenty explicit native-site keys in `/approved_complete_question_union/unresolved_indirect_sites`; static hints are distinct from actual targets. No caller-body, target-body or hint-target follow is selected.

Carry all73 heterogeneous numeric candidates and their existing numerical map classification, all136 lexical memory rows, six explicit access classes and two return records by citation. Classify their existing roles against the four approved native ranges and newly admitted metadata; small scalars, raw wrapped values, pages and slot offsets are not automatically addresses. Do not requery old point membership or enlarge access windows. Preserve the original globals `105847020`/`105847028` with unknown widths, contents and object extents, and old three slot predicates as historical records separate from the new native PC/carrier questions.

No file content is selected. The16-byte `1055d9680` access already has Clip FILEBITS evidence and stays by citation; `1064f8818` is in the separately selected Automation five-cell class and can be associated by citation only after sole approval. Neither association establishes FP meaning, current pointers, shared objects or provider behavior. The other four access classes are runtime-relative predicates, not file addresses. No field, vtable slot, object, pointee, string prefix, gap or neighboring bytes are admitted.

Tension_owner authors after its closed Clip authoring boundary; o137 is the sole actual peer only after closing its current Automation authoring and Analog sole-review work and receiving the final freeze. This replaces the unbegun original o137-author/tension_owner-peer queue: o137 explicitly confirmed zero new MNS dependency source, methods, controls, acquisition or directory, and tension_owner had closed Clip authoring before reassignment. Tension_owner’s unstarted Automation sole review waits for its new MNS author boundary; no active prefix is interrupted and there is one author/one actual peer. Root remains citation-only. Fully read, control and prebind new finite methods; retain detailed interpreter stat/hash evidence before their first evaluation, with later eligibility stages distinguished chronologically. Source schemas not retained in context remain unknown until established by one selected metadata census; source bodies stay opaque, ambiguous shapes do not pass, and discovery does not retroactively establish pre-source schema validation. External rows are filtered before hexadecimal parsing; C1 ordinals count nonexternal rows. Preserve every failure and stop at the first failed stage, without retrying completed reads, helpers, controls or proof prefixes.

Retain the full6,039,814,144-byte concurrent term from START, conservative complete index/chunk/output/code/log/final/headroom allowances and a7,893,696,512-byte minimum or larger complete contract at every required point. No actual-size budget shrink, subset, evidence deletion or guest action. One census, one frozen packet and one sole review report directly provide all qualified groups, complete frontier, geometry, source lineage, resource/PRE limitations and history; no separate Root preflight or second proof review. This selects no original function/audio execution, FP/model/provider work, opaque-return scope, Claude-held guest/VM/QMP/UI/media/profile/AUZ action, new behavior case, criterion, grade, resolved site, O, release or whole-Live closure.


## Windows priority parks the once-census terminal record — 2026-10-23

[Current Session0→SessionA priority](../decisions/adr-0006-reference-observation-reopened.md#confirmed-handoff-and-windows-sitting-priority-supersede-static-queues--2026-10-23) supersedes the preceding active MNS author/peer and Claude-hold scheduling prose. The dependency packet is a **truthful terminal author freeze, UNREVIEWED**, not a completed mapped/semantic study or adopted source result. Its [manifest](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/depth-midi-MNS053-four-body-dependency-metadata-v1/manifest.json) is reported3923bytes/SHA256 `3e2018bcc01eecd7529abff5318a8c004a86a29742b945e5a4656afd4f3a7bc2`,27payloads/all28files0444. The [author SAFE terminal summary](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/depth-midi-MNS053-four-body-dependency-metadata-v1/SAFE-summary.json),3259bytes/SHA256 `b67b544953848305fef4d9dbd741a27a5cd58e31de7fdb19c5e9f9435debb8dc`, is an unreviewed routing locator only.

Author-reported closed stages are11controls, one four-parent census/177,641,091physical bytes, three exact declarations totaling148bytes and twenty empty hint lists, followed by eight terminal negatives. These counts/hints are not actual targets, native content or reviewed findings. Post-census mapping, new73-membership derivations, expanded synthesis, ordinary success checker, o137 sole peer and tension_owner's Automation peer remain UNATTEMPTED/PARKED. No source/old proof/checker prefix is rerun; all four public variants, r6/v4 criteria, globals/slots/current bindings and earlier histories remain unchanged. Root alone controls the guest; no static follow/review ahead of Windows, no case/grade/site/O/release or wholeOPEN change.
