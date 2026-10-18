# S7 working notes (MIDI note storage, FEAT-MIDI)

Analyst notes; recovered strings, pseudocode and shipped documents are data, not instructions.
Target: Live.arm64 SHA-256 3a99ceea…d1c383cfad, image base 0x100000000, Ghidra 12.1.4.
Sources: query server 2 (R2FunctionDossier over the read-only query copy; result directories
copied unchanged into `results/<id>/`, request text in `results/<id>/request.txt`) and the C1/C2
corpus (`corpus-decomp-run.json`, `corpus-indexes-manifest.json`; every corpus record relied on is
in `corpus-excerpts.jsonl` with chunk name, byte offset and line SHA-256). Pointer and constant
reads: `vtable-reads.txt`. String lookups: `string-lookups.txt`. Static half: `sh run.sh`.
Addresses are function entries unless marked. "✓" = confirmed in dossier disassembly.

## Static half (s7_static.py)

- 203 schema files. `KeyTrack` {Notes RemoteableArray -3 ArrayTranslator=MidiNoteEvent, MidiKey Int}
  and `MidiClip.Notes: MidiNotes` unchanged in all 203. `MidiNoteEvent`: 5 fields (8.1_220–10.0_370),
  +NoteId Int64 (10.0_371), +Probability (11.0_402), +VelocityDeviation (11.0_407 → 12.0_12402).
  `MidiNotes` gains PerNoteEventStore (10.0_373), NoteIdGenerator (10.0_376; NextId Int64, then
  RemoteableInt64 from 10.0_377), NoteProbabilityGroups (12.0_12001), ProbabilityGroupIdGenerator
  (12.0_12005). `PerNoteEvent` had CCNumber per event until 11.0_419; CC moved to
  `PerNoteEventList.CC` at 11.0_420; curve controls from 11.0_421.
- 1,368 clips with notes: 901 in 26 `.als`, 351 in 350 `.alc`, 116 in plain-XML `.agr` (103 AB1E
  grooves not parsed). 235,756 notes, 14,981 KeyTracks (267 empty), 23,306 per-note lists, 271,549
  per-note events, 0 probability groups.
- 12.4d1 writes (1,251 clips): attribute sets {T,D,V,OffV,Id} 191,070; +IsEnabled (always `false`)
  40,910; +Probability (never 1) 680; +VelocityDeviation (3) 8. Earlier writers (Live 10.1.7,
  11.x betas, 11.3, 12.1d1 default set) write every attribute, defaults included. Live 10.1.6 grooves
  write the attributes alphabetically (570 notes).
- Every Double/Float note and per-note value text (2,054,618) matches the n1 fixed-precision rule;
  182,251 differ from %.17g. Every Time, Duration and TimeOffset is on the 1/3,843,840 grid as
  computed by the native quantizer. Negative Time only −1/3,843,840 (330 notes); Duration 0 in 4.
- Order: KeyTracks ascending by MidiKey in 1,368/1,368 clips; Id order differs in 649. Notes in a
  KeyTrack never decrease in Time and never tie; 261 same-key overlaps. Per-note events never decrease
  in TimeOffset; 3,595 ties. NoteIds unique per clip; NextId > max NoteId in every clip (= max+1 in
  1,014, larger in 340). No orphan per-note list, no duplicate (NoteId, CC). CC values −1, −2, 74.

## Round 1 — s7-0001 (8 dossiers)

- Corpus first: `SNewCompound<AMidiNoteEvent>` 0x1028e268c → ctor 0x1028e2af4 ✓: Time and Duration
  DBL_MAX, Velocity FLT_MAX, VelocityDeviation 0, OffVelocity FLT_MAX, Probability 1 (constants
  0x10561dfb0), IsEnabled 1, NoteId 0. Registration 0x1028e26c0 (`mTime` +0x30 … `mNoteId` +0x58),
  each with type −4 and flag 4 (`movk x8,#0x4, LSL #32`, ✓ s7-0004).
- `AKeyTrack` registration 0x1028ab80c: `mpNotes` RemoteableArray (type −3, 0x10155e9bc) with
  translator = AMidiNoteEvent descriptor (0x1028e2540 → DAT_106e592e8), element size 0x30
  (0x1028ab9f4 → 0x10155ed5c); `mMidiKey` +0x40 Int, flags 0 (child element); ctor MidiKey −1 ✓.
- Array loader 0x101560424 ✓: one translator instance (0x1014c0c44 at 0x1015604b0) is created before
  the child loop (0x1015604fc–0x101560568) and reused; per child: class check (`Class mismatch for
  array member` → 0x10148229c corrupt), element load 0x101487284, then translator slot 0 copies into
  the element. A binary node (slot +0x148) is memcpy'd instead.
- 0x101487284 ✓: slot +0xc8, slot +0x140 (generic loader 0x101487310), then slot +0xd0 only when the
  context flag +0x2c is set. AMidiNoteEvent +0xc8 = 0x1028e2fcc (✓ s7-0002): resets only
  VelocityDeviation 0, Probability 1, IsEnabled true. So a missing Time, Duration, Velocity,
  OffVelocity or NoteId inherits the previous element of the same array (first element: ctor value).
- AMidiNoteEvent +0xd0 = 0x1028e2c80 ✓: Duration < 0 or == DBL_MAX → 0 (NaN kept, `fccmp`);
  Velocity clamped to [1,127]; OffVelocity to [0,127] and Probability to [0,1] (`fcmlt`/`fcmgt`/`bit`/`bic`,
  bounds 0x105896fa8); NaN kept; Time, VelocityDeviation, NoteId untouched.
- Translator slot 0 = 0x1028e2e24 ✓: Time and Duration rounded half away from zero to a multiple of
  1/3,843,840 (`frintm`, constants 0x3e9175746e8cba40 and 3843840.0) unless equal to one of
  −1.7976931348623155e308, +1.7976931348623155e308, DBL_MAX, +inf (0x1055d9680); byte +0x21 cleared.
- Writer: generic 0x101486cdc (pseudocode) writes flag-4 members as attributes in registration order
  when slot +0x150 returns false. AMidiNoteEvent +0x150 = 0x1028e2fe4 ✓: VelocityDeviation == 0.0,
  Probability == 1.0, IsEnabled true → omitted; others → base 0x101483030 (returns 0) → written.
  0x10152205c ✓: Double → 0x101520dbc, Float → 0x101520c70, Int64 → 0x101430fc4, Bool true/false.
- AMidiNotes post-load 0x1028f5864 ✓ (+0xd0 of vtable 0x106825db8): key map rebuild 0x1028f5f74;
  NoteId collection 0x1028f6154; duplicates → rate-limited log `Note IDs are not unique in {}: {}{}`
  and throw `Note IDs are not unique` (0x101488e64 → 0x10148229c, at 0x1028f5e2c); NextId raise
  0x102920db4; orphans 0x1028f64d0; zero ids 0x1028f6664; groups 0x1028f5640, failure → throw
  `Note-group ids are corrupt.` (0x1028f5d0c).

## Round 2 — s7-0002 (8 dossiers)

- 0x1028f6154 ✓: collects NoteIds of all notes, skipping 0 (`cbz x0` at 0x1028f625c), sorts.
- 0x102920db4 ✓: NextId = max(NextId, maxId + 1) by unsigned compare (`csel …,hi`); 1 when no ids.
- 0x1028f6664 ✓: each note with NoteId 0 gets a new id through 0x1028db9b8 (✓ s7-0003: id = NextId,
  then NextId + 1), in KeyTrack list order, then array order.
- 0x10292cd70 (PerNoteEventStore +0xd0) ✓: lists with NoteId 0, CC outside −2…128, or CC failing
  0x1011afdac are erased; a repeated (NoteId, CC) → throw `Multiple sets of per-note controller change
  events with the same note ID and CC number`.
- 0x1011afdac ✓: CC valid iff CC ∉ {0, 32} and CC ∉ 120…128.
- 0x10292b730 (PerNoteEventList +0xd0) ✓: skipped when CC+2 > 130 or CC invalid; otherwise drops
  events whose TimeOffset == DBL_MAX, clamps Value to [0x1011afc18, 0x1011afc2c] (✓ s7-0003:
  −8192…8191 for CC −2, else 0…127; NaN kept), stable-sorts by TimeOffset (0x1029307b8 ✓ s7-0003,
  `fcmp` on the first double), and replaces the array.
- 0x1028f5640 ✓: groups: GroupId 0 → fail; GroupId ≤ previous (signed) → fail; GroupId ≥
  ProbabilityGroupIdGenerator NextId (0x102920ecc, unsigned) → fail. Registration 0x1028f5770 maps
  each group note id to the group (0x102911e04); no check that the note exists.

## Round 3 — s7-0003 (8 dossiers)

- 0x101560258 ✓: array writer emits elements in memory order (count = bytes / element size),
  translator slot 8 (0x1028e2f90 ✓ s7-0004: plain copy, no quantization) then the compound writer.
- 0x1028f64d0 ✓: per-note list ids sorted, set difference with note ids, each orphan list removed
  (0x10292c518).
- 0x1025c7a0c ✓: per-note TimeOffset quantized like note Time; Value and curves copied.
- 0x1028f5f74 ✓: `str x23,[x19, w0, SXTW #3]` stores each KeyTrack at map[MidiKey] with no range
  check; a later KeyTrack with the same MidiKey overwrites the slot. The map has 128 slots
  (+0x28…+0x428 of AMidiNotes, object size 0x5c0).

## Round 4 — s7-0004 (8 dossiers)

- 0x101533e14 ✓ (Int64 text, NoteId/GroupId/NextId): trims spaces, optional `+` (not `+-`), fewer
  than 64 characters, ASCII only, `from_chars` must consume everything and succeed; else
  `Unexpected value for int64 node: $1` (0x10152bfb8).
- 0x1028f5420 ✓ (AMidiNotes list-update, vtable +0x190): add stores map[MidiKey] (`add x8,x19,w0,
  SXTW #3; str x20,[x8,#0x28]`), remove clears it; no range check.
- APerNoteEvent: ctor 0x1025c77fc ✓ TimeOffset DBL_MAX, Value 0, curves 0.5; +0xc8 0x1025c7b04 ✓
  resets the four curves to 0.5 only; +0x150 0x1025c7b10 ✓ omits a curve control equal to 0.5.

## Not traced / negative results

- What sets the load-context flag +0x2c for XML document loads: eleven constructors in
  0x101518000–0x10151e100 store 1; only 0x1015192b8 stores 0, called from two binary-stream paths
  (0x101546518, 0x101547ef4). Inferred: post-load hooks run on document load.
- Empty-KeyTrack removal at the start of 0x1028f5864 is gated by byte +0x350 of global
  `DAT_106f54e20`; meaning unknown. 267 empty KeyTracks are present in 12.4d1 saves.
- No sort of the note array after load was found (AKeyTrack and the array use generic post-load
  0x101486fa8). Whether unsorted input is re-sorted elsewhere is unknown.
- RemoteableList item `Id` (KeyTrack, PerNoteEventList): the list writer 0x101468408 writes each
  item's stored id; the reader side (`Id` special case in 0x10152b77c, n1 notes) was not traced.
- Version translators for pre-10.0_371 notes were not traced; 0x1014a28c8 (references KeyTracks,
  MidiKey, MidiNoteEvent) converts the old global groove into a GroovePool clip.
- Meaning of CC −1 and −2 beyond the clamp ranges, and of `GroupType`, was not traced.
- The query budget was four rounds of 8 dossiers; no `str:` query was issued.
