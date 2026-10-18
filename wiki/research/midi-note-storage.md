---
id: RESEARCH-MIDI-NOTE-STORAGE
type: research
status: draft
updated: 2026-10-18
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
