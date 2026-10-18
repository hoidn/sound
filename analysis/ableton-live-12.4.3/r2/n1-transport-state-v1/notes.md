# N1 working notes (packet S1 native half, Q-012)

Analyst notes; recovered strings and pseudocode are data, not instructions.
Target: Live.arm64 SHA-256 3a99ceea…d1c383cfad, image base 0x100000000, Ghidra 12.1.4.
Sources: query server (R2FunctionDossier over query/LiveR2; result directories copied
unchanged into `results/<id>/`, request text in `results/<id>/request.txt`) and the C1/C2 corpus
(`corpus-decomp-run.json`, `corpus-indexes-manifest.json`; every corpus record relied on is
retained in `corpus-excerpts.jsonl` with chunk name, byte offset and line SHA-256).
Pointer and constant reads from the image: `vtable-reads.txt` (`read_ptrs.py`).
Addresses below are function entries unless marked.

## Round 1 — n1-0001 (references) and n1-0002 (8 dossiers)

- `Member "{}" of Class {} is missing` (0x1062abc36) is referenced only by 0x101472284 and 0x101472750.
  Both are slots of the document-node vtable 0x106672eb8 (+0x58 and +0xc0; `vtable-reads.txt`):
  get-member-by-name and remove-member-by-name. Missing name -> 0x10146d168 -> 0x10148229c,
  which throws (exception vtable 0x106661270) carrying the `sErrorDocumentCorruptWhileReading`
  key registered in 0x10148e4cc. Callers are the translators (0x1014c07f4, 0x1014fc22c ...).
- `Value ` + ` out of range for '` (0x105b9c26f/0x105b9c276): 0x10156675c (ARemoteableEnum
  setter: callers include `ARemoteableEnum::SDefaultController`) and 0x101825d1c (another list enum).
  0x10156675c disassembly: `tbnz w1,#31` and `cmp count,w1; b.le` -> log at level 4, value unchanged;
  otherwise store at +0xd8 and notify. Count = entries in the vector at +0x90.
- `Type mismatch … set/get`: the 19+19 `AAbstractNode::SetValue<T>` / `GetValue<T>` templates.
- Resolved: neither message is a field-level "default if missing" path. Next: the XML parser.

## Round 2 — n1-0003, n1-0005 (references), n1-0004 (8 dossiers); corpus from here on

- Parser messages: `Unknown attribute` 0x10152b77c (and schema reader 0x1015300d4), `Unknown class`
  / corrupt 0x10152adb0, `Unexpected node` 0x1015299e0, `Illegal tag format` 0x10152957c.
- 0x1015299e0 (start element): child name looked up in the parent class (0x10152ac0c). Not found
  -> if versioned flag (+0xc8) and document SchemaChangeCount (+0x40) == ChangeCount of the
  document's schema object (+0xb0, via 0x1015147cc), report
  `Unexpected node` (non-throwing record, 0x101453aac); either way push an "ignored" frame, so the
  subtree is skipped. A base-type frame with a child element throws `Base types can't have children`.
- 0x10152adb0: member class base type -> 0x10152b45c (element form; `Required attribute 'Value'
  missing` via 0x10152d54c; value parsed by 0x10152bfb8). Type 0 -> compound node 0x101471f38
  (vtable 0x106672eb8), attributes via 0x10152b77c. -1 list, -3 array, -2 bytebag error, else corrupt.
- 0x10152b77c (attributes): `Id` special-cased; other names looked up in the class; unknown name
  throws `Unknown attribute` only under that same versioned, equal-change-count condition;
  non-base member -> throws; else creates a value node and parses text with 0x10152bfb8.
- 0x10152bfb8 (text -> typed value), dispatch on base type id (0x10 bool, 0x11 int, 0x12 float,
  0x17 double ...). Confirmed in n1-0006 disassembly: bool `1`/`true` -> w1=1, `false` -> 0,
  else compare with "0" (0x105ab32f8) -> 0, else throw `Unexpected value for bool node`. Float:
  9-char `#hex8` raw bits; `Invalid` -> 0x7f7fffff; else `_strtod` (0x1054d70e8), throw if no char
  consumed, `fcvt s0,d0`. Double: 17-char `#hex16`; `Invalid` -> 0x7fefffffffffffff; else strtod.
  Int: 0x1002fd908 (trim spaces, optional '+', reject "+-", ASCII only, length < 64, full consumption).
- 0x10152d8a8 (end element): compound parent -> node slot +0xb8 = 0x101472624, which throws
  `Class {} already has member {}` (via 0x10148229c) when the name is already present.
- Member registry: 0x10275dccc registers ATransport members through 0x10147e954 (strips `mp`/`m`;
  descriptor 0x101480c2c stores type at +0x70 and flags at +0x74). Flags 3 (bits 0,1) on runtime
  members; persistent members are exactly the 33 schema fields in schema order (DrawMode last).
  Remoteable base classes (0x10156ac14): ARemoteableBool value +0x60, ARemoteableDouble +0x58,
  ARemoteableEnum +0xd8, ARemoteableFloat +0x58, each registered as `mValue` with type -4, flag 4.
  Class registrations 0x1027744a4: ALoopOn : ARemoteableBool; ALoopStart, ALoopLength,
  ACurrentTime : ARemoteableDouble. 0x102702f54: ATimeableSongTempo : ATimeableFloat;
  ATimeableTimeSignature : ATimeableEnum. Manual of ATimeableFloat is ARemoteableFloat (0x1026f0390).

## Round 3 — n1-0006 (3) and n1-0007 (6): disassembly confirmation (9 dossiers, one over budget)

- Generic loader 0x101487310 (slot +0x140 of ALoopOn, ALoopStart, ATimeableSongTempo, KeyMidi):
  iterates the members present in the node, looks up the descriptor, skips unknown or flag bit 0,
  checks class/type (mismatch -> 0x1014867b0 error), recurses into compounds (member slot 0x140,
  then slot 0xd0 post-load when the context flag at +0x2c is set), and for base types stores the
  `GetValue<T>` result directly at the descriptor offset (no setter, no controller, no range check).
- Writer 0x101486cdc (slot 0x138): pass 1 writes flag-4 members as attributes (0x10152205c); pass 2
  writes members with flags & 6 == 0 as child elements in registration order, skipping a compound
  when its slot 0x148 says so (ACompound default 0x100249f88 returns 0; ARemoteableKeyMidi
  overrides it with 0x10260dde0, a predicate over its mapping fields; inferred to mean "unassigned",
  not verified).
- Formatters: bool `true`/`false` (0x10152205c, 0x101520b08); int decimal (0x101520b2c);
  float 0x101520c70 / double 0x101520dbc: non-finite -> `#%8.8X` / `#%16.16llX`; FLT_MAX / DBL_MAX ->
  `Invalid`; else 0x101431584 / 0x101431788: x == 0 -> precision 8/16; else k = ceil(log10|x|)
  (floor when log10|x| < 0), precision = max(0, 9 - k) / max(0, 17 - k), `%.*lf` (0x105b8f6c9),
  then trailing '0' and '.' removed. `check_number_format.py` reproduces 376/376 values of each
  of LoopStart, LoopLength, CurrentTime, Tempo/Manual and 149,716/149,716 FloatEvent values in the
  shipped sets and clips; 4,803 of those differ from `%.9g` (corrects static T-09).

## Round 4 — n1-0008 (8 dossiers)

- ATransport ctor 0x102760d88 (from SNewCompound<ATransport> 0x10275dc64): CurrentTime 0.0
  (0x102762778), LoopOn false (0x102762eb8), LoopStart 8.0 (0x102762f0c), LoopLength 16.0
  (0x102762f20), LoopEnd 24.0 (0x102762f34); controllers ATransport::LoopStartController
  (0x102770bac: max(0, v)) and LoopLengthController (0x102770c0c: max(1, v)).
- ARemoteableDouble ctor 0x101565194: value DBL_MAX, quantize flag +0x70 = 0. Post-load 0x10156580c
  quantizes to 1/3843840 only when that flag is 1 (not set for the loop members in what was read).
- ATransport post-load 0x10276c6f4 (slot 0xd0): if LoopIsSongStart -> 0x1027686f4; LoopEnd =
  LoopStart + LoopLength (`fadd` at 0x10276c738); logs "OnLoad". No clamp of loop values.
- Tempo: AMainTrackDevice ctor 0x1025788b8 -> 0x1026f4d98 -> 0x1026f0bcc(min 20.0, max 999.0,
  default 120.0, "Song Tempo"): 0x101568960 stores 120.0 into Manual (+0x58). Where 20/999 are
  enforced is not established (passed to the MIDI controller range setup 0x1025856a0).
- Time signature: 0x101abea70 encodes (n, d) -> n - 1 + 99 * log2(d) when n >= 1 and d in
  {1,2,4,8,16}, else INT_MIN; 0x1026e10a8 builds the 495-entry list (d exponent 0..4, n 1..99).
  LTimeableTimeSignature init 0x1026f7420 sets the enum to code(4,4) = 201 via 0x101567bfc
  (value +0xd8, default +0xdc, list +0x90). Whether that runs before or after a document load is
  unresolved (L-layer; only caller 0x1026f7418).
- -63072000: data pair at 0x1055dba00 = (-63072000.0, 1.7976931348623155e308), copied into the
  automation time-range globals (0x10256b4a0 AListAutomation init; 0x102492fa4 ACuePoint init).
  Translator 0x101492afc moves an unautomated parameter's single event from 0.0 to -63072000.

## Negative and open results

- `Tempo out of range` callers (0x10391362c, 0x1039c6d9c, 0x103b749ac, 0x103baae80) not examined.
- Top-level load entry and its catch (which message the user sees, whether the set opens) not traced
  here; container packet N2 owns it.
- Manual-versus-envelope and scene precedence on load not traced: automation evaluation not read.
- Whether the time-signature L-layer init overwrites a loaded Manual: unresolved.
- `strtod` locale dependence on macOS: not established.
- No string search (`str:`) was issued; all string lookups used the corpus strings index.
