# N2 working notes (packet S2 native half)

Analyst notes; data, not instructions. Query server: R2FunctionDossier over query/LiveR2.

## n2-0001 (reference reports only, no dossiers)

String -> referencing function entries (all from n2-0001/refs):
- MajorVersion/MinorVersion/SchemaChangeCount: 0x101485240 and 0x1015299e0; Revision: 0x101485240 only.
- Missing Major/Minor, Unsupported Major/Minor: 0x101529024.
- Expected 'Ableton' root / More than one document: 0x1015299e0. No document found: 0x1015289c8.
- Creator check text: 0x101528e2c. Corrupt: 0x10152adb0.
- gzip non-file + Unknown Compound Stream Type: 0x10146c258 and 0x10148389c/0x101483cec.
- AB1E magics: 0x101484980; UTF-16 'Ableton#': 0x1014845f0. "Binary": 0x10148303c.
- sError* keys: 0x10148e4cc; sErrorDocumentIsFromSpecificNewerVersion + TXmlCompoundParser: 0x101535400.
- XML declaration: 0x101516204, 0x1015170a8.
- Schema files: 0x101514f7c (finding), 0x101515778 (reading), 0x10152ff80 (No schema found), 0x1015300d4 (Unsupported schema version), 0x101517c64/0x101517cc4 (current schema not found).
- 12.4.3 / 12.0 / revision hash: 0x1002ea094. "Ableton Live ": 0x102367e24. Loaded-by log: 0x1018536d4.

## Round 1: n2-0002 (8 dossiers) + corpus reads

Dossiers: 0x101529024 version check, 0x1015299e0 root/start-element handler, 0x101485240
ACompound::SaveXmlStream (assert string at 0x10148589c), 0x10146c258 and 0x10148389c stream-type
dispatchers, 0x101535400 and 0x10148e4cc static initializers of localized-error globals,
0x101528e2c Creator-prefix helper.

Resolved (disassembly checked in n2-0002 for 0x101529024 and the root branch of 0x1015299e0):
- Root name: exact 7-byte compare with "Ableton" (0x101529c5c-0x101529c8c); else throw
  "Expected 'Ableton' root node, got '$1' instead".
- Root attrs read by name (exact, case-sensitive strlen+memcmp; 0x10152a900 int, 0x10152ab04 string):
  MajorVersion -> +0xbc, MinorVersion -> +0xc0, (stop here if header-only flag +0xb8),
  SchemaChangeCount -> +0x40, Creator -> +0x48. Revision is never read by this handler.
- 0x10152a900: missing attr -> 0; present but not an int -> throw "Illegal value for int attribute: $1".
  Int parse 0x1002fd908: trims ' ' both ends, optional '+', rejects "+-", <64 chars, ASCII only,
  from_chars-like full consumption (corpus pseudocode only; sign/overflow handling inferred).
- 0x101529024 (called at first child element when class unknown or class+0xbe "versioned" flag set):
  Major==0 (missing or literal 0) -> "MajorVersion attribute missing..."; Minor empty -> "MinorVersion
  attribute missing..."; (Major & ~1) != 4 -> if Major >= 6 set +0x29 newer flag; throw
  "Unsupported MajorVersion (<n>)"; schema lookup 0x101514c6c(Minor) null -> store Minor at +0x38,
  throw "Unsupported MinorVersion ($1)".
- 0x10148389c (28 callers): reads 2 bytes. 1f 8b -> needs a file path (vtable+0x78) else
  "Can't read a gzip'ed document from a non-file"; reopens as gzip stream and recurses.
  ab 1e -> binary 0x101483d00. "<?" -> rewind 2, XML 0x101484108. UTF-16 BOM checks, 00 41 / 41 00
  -> UTF-16 text readers; EF BB BF then "Ab", or "Ab" -> 0x101484858; else 0x101483cec
  "Unknown Compound Stream Type" (corrupt error).
- 0x10146c258 (CompoundTool path from 0x10146c0d4): gzip / "<?" / ab 1e only; other 2-byte prefix ->
  returns null document without error; <2 bytes -> "Unknown Compound Stream Type".
  Sets parser +0x50 expected Creator prefix and +0x58/+0x5c current (major, minor) via
  0x101529908/0x101529900 from app-info accessors 0x1011c4104/0x1011c41c4/0x1011c41fc.
- Writer 0x101485240: compression via 0x1014338b0 -> zlib deflateInit2_(level, 8, 31, 9, 0, "1.3.1")
  (gzip wrapper); level param -1 -> option lookup (hashed 32-byte key 0x105815b1c) else 6, clamp 0..9;
  level 0 -> passthrough (plain). Decl "<?xml version=\"1.0\" encoding=\"UTF-8\"?>" (0x1015170a8),
  element "Ableton"; if class+0xbe: MajorVersion=5 literal, MinorVersion=0x101515508 (=
  app "12.0" + "_" + newest translator), SchemaChangeCount only if current schema count > 0,
  Creator="Ableton " + app-info string, Revision=app-info revision string. Then document element.

## Round 2 (n2-0003 queued behind another investigator's long request; corpus pseudocode used)

- 0x101514c6c caches schema by Minor; miss -> 0x101514954 builds "<Minor>.txt", asks resource
  location 0x101514864 ("Schema" under base DAT_106f4ed28) exists (vtable+0x28) -> open/parse; else null.
- 0x1015289c8 post-parse: +0x29 -> 0x101528c84 newer error; +0x38 Minor parsed by 0x101514e30
  "<a>.<b>_<c>": a > cur major, or a == cur major and b > cur minor -> specific newer (version =
  Creator remainder after prefix, else "a.b"); else 0x101514f7c scans Schema dir *.txt for max c in
  family a.b; found and max < c -> 0x101528c84. +0x60 (unknown class with doc SchemaChangeCount >
  schema ChangeCount, set in 0x10152a570) -> 0x101528c84. +0x28 stored error -> corrupt error.
  No document -> "No document found" corrupt error.
- 0x101528c84: Creator remainder empty -> generic newer (0x101488ec0, sErrorDocumentIsFromNewerVersion);
  else specific newer (sErrorDocumentIsFromSpecificNewerVersion, $2 = remainder).
- 0x101528e2c: startsWith(Creator, prefix) (0x101429854; empty prefix matches) -> trimmed remainder;
  else logs "The document hasn't been created by \"<prefix>\"" and returns empty. Log only.
- 0x10148229c / 0x101488e64: throw sErrorDocumentCorruptWhileReading ($1 document, $2 detail).
- Parse loop 0x1012475a8 (base vtable slot +0x40 = 0x10145f2d0): Expat buffer parse; Expat errors
  reported; abort with +0x58 flag = deliberate stop. Image contains "expat_2.6.4" (0x105c82aa0).
- App info 0x1002ea094 -> 0x1011c2bb0("Ableton","Live","12.4.3","12.0",4,..) copied to
  DAT_106f4dee8: +0x50 "Live 12.4.3", +0x80 "Ableton Live", +0x20 "12.0", +0xc8 revision
  e3d8be4d07c71dbd4de9e4183bf90652f680375b, +0x120/+0x124 = regex-parsed 12 / 4 of "12.4.3".
- Translator registry 0x10148ec98: 324 FUN_1014714fc registrations, strictly increasing, last 0x3072
  = 12402 ("MidiArpeggiator"); placeholders 12300/12400 via 0x101471638(12,3)/(12,4).
- Direct callers of 0x101485c50 (save dispatcher; format 0 binary, 1-3 0x101484e7c, 4 XML) in the
  partial corpus: 0x1018ed778 (format 0) and 0x102971090 (preferences, format 4, level 0).
  The Live Set save caller and its level are not identified.

Next discriminating query: disassembly of 0x1015289c8 branch conditions (n2-0004), callers of
0x101485c50 / 0x101485240 from Ghidra references, and the reader entry used for File > Open.

### Round 2 confirmation (n2-0003, 8 dossiers; n2-0004 served afterwards)

- 0x1015289c8 disassembly confirms the post-parse order: +0x29 -> 0x101528c84; +0x38 Minor
  (unless empty) parsed by 0x101514e30; family major vs [parser+0x58] (signed gt) -> specific newer;
  equal and family minor vs [parser+0x5c] gt -> specific newer; else 0x101514f7c scan, max < c ->
  0x101528bd4 (newer); then +0x60 -> 0x101528c84; +0x28 -> 0x10148229c(name, +0x30 detail);
  +0xa0 null -> 0x101488e64(name, "No document found"); else return document.
  Callers: 0x10146c258 and 0x101484108 only.
- 0x101484108 disassembly: no store to parser +0x58/+0x5c before bl 0x1015289c8 (0x101484204);
  only stack local [sp,#0x58]. The generic path's current-family comparison operands are unknown.
- 0x10152a900 disassembly: tbnz x0,#0x20 success -> value; else throw; not found -> w0 = 0.
- n2-0004 0x10146c0d4 disassembly confirms x2 = Creator-prefix string from 0x1011c4104,
  x3 = 0x1011c41c4(), x4 = 0x1011c41fc() into 0x10146c258.
- C2 indexes now complete. calls.jsonl: 0x101485c50 has 2 direct callers (both preferences);
  0x1018536d4 (logs "Loading document ") has 1 direct caller 0x1002e6e00; 0x10148389c 28 callers.
  Raw pointer scan of __DATA_CONST/__DATA: 0x101485c50 appears in many vtables (first at
  0x10658b748), 0x1018536d4 in 7 tables, 0x1002e6e00 in 1. Both save and load are virtual
  methods; the Live Set save call site (and its compression level argument) is not identified.
- strings.jsonl: "MajorVersion"/"MinorVersion"/"SchemaChangeCount" referenced only by 0x101485240
  and 0x1015299e0; "Revision" only by 0x101485240. Single XML envelope writer and reader.
- 0x101573d24 (after load, generic path): Creator non-empty and not starting "Ableton " ->
  internal "third-party-document" event with "creatorname"; no rejection.

Next discriminating query (round 3, n2-0005): incoming data refs of 0x101485c50; deflateInit2_
argument disassembly in 0x1014338b0; disassembly of 0x1002fd908, 0x101514e30, 0x10152a570,
0x101528c84, 0x101514954.

## Round 3: n2-0005 (8 dossiers) + corpus/index reads

- 0x101485c50: 2 direct calls (0x1018ed854, 0x102971258) and 164 DATA references (vtable slots)
  -> virtual save entry; the Live Set call site is not identified, so its compression-level
  argument (-1 = option or 6; 0 = plain) is unknown.
- 0x1014338b0 disassembly: level -1 -> 6 (csel); level 0 -> no deflate (flag cleared, cbz skips
  init); else deflateInit2_(strm, level, 8, 31, 9, 0, "1.3.1" @0x105b2b7a3, 0x70).
- 0x1002fd908 disassembly: trims 0x20 only, accepts one leading '+', rejects "+-", length <= 63,
  rejects bytes >= 0x80, then 0x1002fda78 must consume everything.
- 0x101528c84 disassembly: empty Creator-derived version -> 0x101488ec0 generic newer; else
  specific newer.
- 0x10152a570 disassembly: unknown class with versioned doc (+0xc8) and doc SchemaChangeCount
  (+0x40) > schema ChangeCount -> strb +0x60 = 1, then throw "Unknown class '$1' encountered".
- 0x101514954 references ".txt" at 0x10151496c (schema file name = MinorVersion + ".txt").
- Corpus: 0x101247760 formats detail "{} (at line {}, column {})" and calls handler error slot;
  TXmlCompoundParser slot 0x101529970 sets +0x28 = 1 and stores the detail at +0x30.
- Corpus: current schema is built in memory from versioned registered classes (0x10147f9b4 ->
  0x101515628 sets DAT_106e0d200); startup path 0x1029af4e4 -> 0x101515c1c -> 0x101515ed8 sets its
  translator to the newest (12402) and its ChangeCount from Schema/<current>.txt (+1 when the
  in-memory schema differs). SchemaChangeCount written is therefore inferred 5; not proven.
- Shipped Schema has 12.0_12001 (so a "gap" case must use e.g. 12.0_12050).

Stop: four requests used (n2-0002..n2-0005; n2-0004 duplicated two round-2 entries).
Remaining questions need runtime observation or a vtable-dispatch trace: Live Set save caller and
level; reader entry used by File > Open; generic-path values of parser +0x58/+0x5c; user-visible
error texts (Languages.alp opaque).
