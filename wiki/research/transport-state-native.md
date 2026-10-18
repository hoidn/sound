---
id: RESEARCH-TRANSPORT-STATE-NATIVE
type: research
status: draft
updated: 2026-10-17
access: analysis
target: Ableton Live 12 Suite 12.4.3 arm64
---

# Transport-state fields: native reader and writer

Packet S1, native half (N1), from [roadmap revision 2](native-decompilation-roadmap.md#revision-2-proposal--2026-10-17).
It continues [transport-state static](transport-state-static.md) and works on
[Q-012](../questions.md#q-012-transport-state-load-and-save-semantics).
Question: for song tempo (`Tempo/Manual`), time signature (`TimeSignature/Manual`),
`LoopOn`, `LoopStart`, `LoopLength` and `CurrentTime`, what does the 12.4.3
document reader do with a missing, malformed, duplicated or out-of-range value?
Which defaults and clamps apply, and what does the writer emit? Everything here
is static. Nothing was executed. Where this page says "load fails", it means that
the traced code throws; what the user sees has not been traced.

The resulting draft contract is [SPEC-TRANSPORT-STATE](../specs/transport-state.md).
The [reader walkthrough](learning/walkthroughs/transport-state-reader.md) follows one
field through the code.

## Evidence

Image: `analysis/ableton-live-12.4.3/derived/Live.arm64`, SHA-256
`3a99ceea…d1c383cfad`, image base `0x100000000`, Ghidra 12.1.4. Retained run:
[n1-transport-state-v1](../../analysis/ableton-live-12.4.3/r2/n1-transport-state-v1/manifest.json).

| File | Content |
| --- | --- |
| [notes.md](../../analysis/ableton-live-12.4.3/r2/n1-transport-state-v1/notes.md) | Round-by-round findings with every address, plus negative results |
| `results/n1-0001` … `n1-0008` | Unchanged query-server results with request text: 34 function dossiers (with disassembly) and 41 reference reports |
| [corpus-excerpts.jsonl](../../analysis/ableton-live-12.4.3/r2/n1-transport-state-v1/corpus-excerpts.jsonl) | The 95 C1 corpus pseudocode records relied on, each with chunk name, byte offset and line SHA-256 |
| [vtable-reads.txt](../../analysis/ableton-live-12.4.3/r2/n1-transport-state-v1/vtable-reads.txt) | Six vtables and three constant groups read from the image by `read_ptrs.py` |
| [number-format-check.txt](../../analysis/ableton-live-12.4.3/r2/n1-transport-state-v1/number-format-check.txt) | Output of `check_number_format.py` against the shipped sets and clips |
| [registry-order-check.txt](../../analysis/ableton-live-12.4.3/r2/n1-transport-state-v1/registry-order-check.txt) | Output of `check_registry_order.py`: persistent `ATransport` registrations against the `12.0_12402` Transport field order |
| [probe-batch.json](../../analysis/ableton-live-12.4.3/r2/n1-transport-state-v1/probe-batch.json) | Phase 4 probe records PRB-N1-01–08 |

The query budget was four rounds: n1-0002 and n1-0004 (8 dossiers each), n1-0006
and n1-0007 together (9, one over the per-round budget, all taken only to confirm
disassembly), and n1-0008 (8). The C1/C2 corpus finished during round 2. After that,
pseudocode and call or string lookups came from the corpus
(`corpus_lookup.py`), and server dossiers were used to confirm material branches
against disassembly. No `str:` scan was issued.

## How a set reaches the transport objects

**Observed** in pseudocode and confirmed in disassembly where marked (✓):

1. The XML parser builds a tree of document nodes typed by the class schema.
   The start-element handler `0x1015299e0` looks up each child name among the
   parent class's fields (`0x10152ac0c`). `0x10152adb0` then branches on the
   field's type. A base-type field (`Type=-4`) written as an element must carry
   a `Value` attribute: `0x10152b45c` throws `Required attribute '$1' missing`
   through `0x10152d54c`. A compound field opens a node, and its attributes go
   through `0x10152b77c`.
2. Attribute text is converted by `0x10152bfb8` according to the field's base type
   ✓ (n1-0006). Any conversion failure throws.
3. At the end of an element, the child is added to its compound parent. The add
   slot `0x101472624` raises `Class {} already has member {}` when the name is
   already present ✓ (n1-0007).
4. Each object reads its node through virtual slot `+0x140`. For `ALoopOn`,
   `ALoopStart`, `ATimeableSongTempo` and `ARemoteableKeyMidi` the slot holds the
   generic loader `0x101487310` ([vtable-reads](../../analysis/ableton-live-12.4.3/r2/n1-transport-state-v1/vtable-reads.txt)).
   The loader walks **the members present in the node**. It skips names the class
   does not know and members whose descriptor flag bit 0 is set. A type mismatch
   is an error. Compound members recurse. A base-type value is stored straight
   into the object field at the descriptor offset ✓ (n1-0008: `tbnz w8,#0x0` at
   `0x1014873f8`; store at `0x101487364`). No setter, controller or range check
   runs on that store.
5. After a member is loaded, its slot `+0xd0` post-load hook runs when the load
   context flag at `+0x2c` is set. For `ATransport` that hook is `0x10276c6f4` ✓.
   It sets `LoopEnd = LoopStart + LoopLength` (`fadd` at `0x10276c738`) and does
   not clamp anything.

**Inferred:** the top-level load creates the root object through its factory and
then applies the loader. That entry point was not traced here. The container
packet traced the post-parse decision `0x1015289c8`: a stored parse error becomes
the corrupt-document error `0x10148229c`. It infers that exceptions thrown inside
Expat callbacks are caught and stored, but the catch site was not kept
([document container native](document-container-native.md#how-a-refusal-becomes-an-error)).

### Names, order and attributes come from the member registry

**Observed:** `0x10275dccc` registers 80 `ATransport` members through `0x10147e954`.
The registration strips the `mp` prefix (pointer members) or the `m` prefix (value
members). The descriptor built by `0x101480c2c` stores a type at `+0x70` and flags
at `+0x74`. Every runtime-only member (`LoopEnd`, `SongLength`, `Start`, `Stop` …)
is registered with flags 3. The others are exactly the 33 schema fields of
`Transport` in `12.0_12402`, registered in schema order (`check_registry_order.py`:
33 of 80 registrations, identical order). The remoteable base classes
register their value as `mValue`, with type -4 and flag 4: `ARemoteableBool` at
`+0x60` (`0x101564330`), `ARemoteableDouble` and `ARemoteableFloat` at `+0x58`, and
`ARemoteableEnum` at `+0xd8`. The class registry `0x1027744a4` makes `ALoopOn` an
`ARemoteableBool`, and `ALoopStart`, `ALoopLength` and `ACurrentTime`
`ARemoteableDouble`s. Song tempo's `Manual` is an `ARemoteableFloat` (`0x1026f0390`).
Time signature's `Manual` belongs to `ATimeableEnum`.

The writer `0x101486cdc` (slot `+0x138`) first writes flag-4 members as attributes
(`0x10152205c`). It then writes members whose `flags & 6 == 0` as child elements in
registration order. A compound member is skipped when its slot `+0x148` returns
true. For a plain compound that slot returns 0. `ARemoteableKeyMidi` overrides it
(`0x10260dde0`) with a predicate over its mapping fields.

**Inferred:** this explains the shapes observed in the static half. The value of a
field such as `LoopOn` is an attribute (`<LoopOn Value="false" />`) because flag 4
is set. `LomId` is a child element because its flags are 0. Every shipped document
omits the 23 `*KeyMidi` children because that predicate reports them unassigned.
This resolves the "mapping rule is unknown" note on the static page. The
"unassigned" meaning of the KeyMidi predicate is not verified.

## Lexical acceptance on load

**Observed** in `0x10152bfb8` (bool and float branches ✓ n1-0006) and `0x1002fd908` (✓ n1-0006):

| Base type (fields) | Accepted | Rejected (throws) |
| --- | --- | --- |
| Bool (`LoopOn/@Value`) | exactly `true` or `1` gives true; exactly `false` or `0` gives false | anything else, including `TRUE`, `True`, `""`, ` true`, `yes` |
| Double (`LoopStart`, `LoopLength`, `CurrentTime`) | `Invalid` gives the largest double; a 17-character `#` plus 16 hex digits gives raw IEEE bits; otherwise C `strtod`, accepted when at least one character is consumed, so trailing text is ignored and leading whitespace, exponents, hex floats, `inf` and `nan` are accepted | text with no numeric prefix, such as `""` or `abc` |
| Float (`Tempo/Manual/@Value`) | as Double, but `#` plus 8 hex digits, `Invalid` gives the largest float, and the parsed double is rounded to float32 (`fcvt s0,d0`) | as Double |
| Int (`TimeSignature/Manual/@Value`) | ASCII decimal; leading spaces and an explicit `+` are skipped, but trailing spaces are kept whenever a leading space or `+` was present (see [document container native](document-container-native.md)); `+-` is rejected; the `-` sign is passed to an untraced converter; fewer than 64 characters after the skipped prefix. Corrected 2026-10-17 from "after trimming spaces, optional sign"; see [SPEC-TRANSPORT-STATE](../specs/transport-state.md) r2 | `201.0`, `2e2`, `0x10`, `""`, non-ASCII bytes |

The float32 rounding answers the static page's question: tempo is held as float32
after load. **Unknown:** whether `strtod` follows the user's locale on macOS (for
example a decimal comma). Expat itself rejects a duplicated attribute as malformed
XML.

## Missing, duplicated and unknown items

- **Missing element or `Value` attribute (static-derived).** The loader visits only
  members present in the node, so a missing child or missing `Value` attribute
  leaves the field at the value the constructor set. Defaults:
  - The `ATransport` constructor `0x102760d88` sets `LoopOn` false
    (`0x102762eb8`), `LoopStart` 8.0 (`0x102762f0c`), `LoopLength` 16.0
    (`0x102762f20`), `CurrentTime` 0.0 (`0x102762778`) and `LoopEnd` 24.0 ✓ (n1-0008).
  - The `AMainTrackDevice` constructor `0x1025788b8` calls `0x1026f4d98`, which
    passes min 20.0, max 999.0 and default 120.0 to `0x1026f0bcc` ("Song Tempo").
    That stores 120.0 into `Manual` through `0x101568960` ✓ (constants at
    `0x1026f4e20`–`0x1026f4e34`).
  - **Unknown:** the time-signature default. `LTimeableTimeSignature` init
    `0x1026f7420` sets code 201 (4/4) through `0x101567bfc`, but it is a
    logic-layer object and its order relative to the load was not established.
    This also leaves open whether a loaded non-4/4 `Manual` survives.
  - The `ARemoteableDouble` constructor stores DBL_MAX (written as `Invalid`)
    before the owner's constructor overrides it. A Double field without an owner
    default would therefore round-trip as `Invalid`. None of the four transport
    Double fields is in that state.
- **Duplicated child element (static-derived).** The add slot raises
  `Class {} already has member {}` with the `sErrorDocumentCorruptWhileReading`
  key (`0x10148229c`, key registered in `0x10148e4cc`).
- **Unknown child element of a compound (static-derived).** The element and its
  subtree are skipped. A report record (`Unexpected node`, `0x101453aac`) is built,
  not thrown, under one condition: the reader is in versioned mode (flag `+0xc8`,
  set per root class as described in
  [document container native](document-container-native.md)) and the document's
  `SchemaChangeCount` (`+0x40`) equals the ChangeCount of the schema object chosen
  for the document (`+0xb0`, through `0x1015147cc`). An unknown element in list or
  root position goes through `0x10152a570` instead and raises `Unknown class`;
  the container packet traced that path.
- **Unknown attribute (static-derived, condition partial).** `0x10152b77c` throws
  `Unknown attribute '$1'` only under that same versioned, equal-change-count
  condition. Otherwise the attribute is ignored. For shipped 12.4d1 content the
  condition is false: SchemaChangeCount is 1, while the `12.0_12402` schema file
  says ChangeCount 5. Whether the in-memory schema matches the file, and the value
  a 12.4.3 save writes (`0x101485240`), are unknown.
- **`Member "{}" of Class {} is missing`** is raised by the node accessors
  `0x101472284` and `0x101472750` (node vtable `0x106672eb8` slots `+0x58`/`+0xc0`).
  Their callers are version translators. That message is therefore a migration
  error, not the fate of a missing field in a current-version set.

## Range handling

- **Observed:** the `Value … out of range for '` message belongs to the
  `ARemoteableEnum` setter `0x10156675c`. That setter logs and keeps the old value
  when the index is outside its entry list (`tbnz w1,#31` and `cmp`/`b.le` at
  `0x101566774`–`0x10156678c`). The loader does not call it: it stores the enum
  index at `+0xd8` directly.
- **Observed:** `ATransport::LoopStartController` (`0x102770bac`) applies
  `max(0, v)` and `LoopLengthController` (`0x102770c0c`) applies `max(1, v)`. Both
  act on controlled value changes, not on the loader's direct store. The ATransport
  post-load hook adds no clamp.
- **Inferred:** a well-formed but out-of-range number does not make the load fail.
  This covers negative `LoopStart`, `LoopLength` below 1, negative `CurrentTime`,
  tempo outside 20–999 and a time-signature code outside 0–494. The values the
  program then uses and displays, and what a later save writes, are **unknown**
  (PRB-N1-03, PRB-N1-06). Where 20 and 999 are enforced is unknown too. They reach
  the MIDI controller range setup `0x1025856a0`, not the `Manual` value. The
  `Tempo out of range` callers (`0x10391362c` and three others) were not examined.
- `ARemoteableDouble`'s post-load hook `0x10156580c` quantizes to 1/3,843,840 only
  when its flag at `+0x70` is set. The constructor clears that flag, and nothing
  that was read sets it for the loop fields.

## Time-signature code

**Observed** ✓ (n1-0008): `0x101abea70` maps (numerator n, denominator d) to
`n − 1 + 99·log2(d)` when n ≥ 1 and d ∈ {1, 2, 4, 8, 16}, otherwise INT_MIN.
`0x1026e10a8` builds the 495-entry list: denominator exponents 0–4 by numerators
1–99. This confirms hypothesis H-TS from the static page natively. Valid codes are
0–494, 4/4 is 201, and the shipped maximum `MidiControllerRange` value 494 is 99/16.
The translator `0x10149c404` builds the same code from the older `Transport/Signature*`
values (formula hidden in pseudocode; not re-derived).

## What `-63072000` is

**Observed:** the 16 bytes at `0x1055dba00` are the pair (−63,072,000.0,
1.7976931348623155e308). The `AListAutomation` and `ACuePoint` initialisers copy
them into global time-range variables. The translator `0x101492afc` moves an
unautomated parameter's single event from time 0.0 to −63,072,000.
**Inferred:** −63,072,000 beats is the lower end of the automation time range, and
a one-event envelope at that time encodes an unautomated value. Whether 12.4.3
prefers that event or `Manual` when they disagree is **unknown** (PRB-N1-04/05).

## Writer number format

**Observed** (`0x101520c70`, `0x101520dbc`, and the formatters `0x101431584` and
`0x101431788` ✓ n1-0007):

- A non-finite value is written as `#` plus uppercase hex bits (8 digits for Float,
  16 for Double). The largest finite value is written as `Invalid`.
- Otherwise the program takes k = ⌈log10|x|⌉, or ⌊log10|x|⌋ when log10|x| < 0, and
  formats with `%.*lf` (`0x105b8f6c9`) at precision max(0, 9 − k) for Float or
  max(0, 17 − k) for Double. Zero uses precision 8 or 16. Trailing `0`s and a
  trailing `.` are then removed.
- Bool is written `true`/`false`; Int as plain decimal.

**Corroborated** (`check_number_format.py`): the rule reproduces all 376 shipped
values of each of `LoopStart`, `LoopLength`, `CurrentTime` and `Tempo/Manual`, and
149,716 of 149,716 `FloatEvent` values. Of those, 4,803 are values below 1 where
`%.9g` gives different text (for example `0.5500000119`). This corrects
[T-09](transport-state-static.md#candidate-requirements-for-spec-transport-state):
the writer is not "at most 9 or 17 significant digits". A Float below 1 gets up to
10 or more decimals. The shipped files were written by 12.4d1 and 12.1d1. This
binary's own formatter is the 12.4.3 evidence, which makes the rule a static
derivation for 12.4.3.

## Phase 4 probes

Static tracing cannot settle the items below. Each record in
[probe-batch.json](../../analysis/ableton-live-12.4.3/r2/n1-transport-state-v1/probe-batch.json)
gives the question, the minimal input (edits to the shipped 12.0_12402
`Recording Audio.als`, SHA-256 `af57ff8f…c043`), the discriminating observation and
a stop condition.

| Probe | Settles |
| --- | --- |
| PRB-N1-01 | Bool tokens `1`, `0`, `TRUE`, empty: opens or error, and the loop state |
| PRB-N1-02 | Missing element or attribute gives 8/16/120 (and not a template value) |
| PRB-N1-03 | Effective and re-saved values for negative or small loop values, negative position, tempo 5 and 2000 |
| PRB-N1-04 | Time signature: `Manual` versus envelope; whether a loaded 6/8 survives |
| PRB-N1-05 | Tempo: `Manual` versus envelope; an enabled scene tempo at load |
| PRB-N1-06 | Time-signature codes 495, −1 and `201.0` |
| PRB-N1-07 | A real 12.4.3 save: number text, child order, KeyMidi omission, envelopes, SchemaChangeCount |
| PRB-N1-08 | Duplicate child, unknown child and unknown attribute outcomes |

## Remaining unknowns

- The user-visible outcome of a read error: dialog text, whether the previous set
  stays open. This is shared with the container packet.
- `Manual` versus envelope versus scene precedence, and whether the time-signature
  logic layer overwrites a loaded value.
- Effective clamping of out-of-range values after load, and where tempo 20–999 is
  enforced.
- Whether 12.4.3 always writes the one-event tempo and time-signature envelopes.
- `strtod` locale behaviour; the exact KeyMidi omission predicate.

## Limitations

Static evidence only. A store or a throw in code does not prove that the path runs
for a given file. The top-level load and its exception handling were not traced.
Ghidra `FUN_` names are generated. Demangled names come from the symbol table and
are evidence, not proof. The corpus pseudocode was cross-checked against dossier
disassembly only for the branches marked ✓. Shipped documents are 12.4d1/12.1d1
writes, not 12.4.3 saves.
