---
id: RESEARCH-TRANSPORT-STATE-NATIVE
type: research
status: draft
updated: 2026-10-21
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
is static except the [extracted-execution results](#extracted-execution-results-x2-2026-10-18)
added on 2026-10-18, which ran the x86_64 counterparts of the reader's text
conversion, the writer and the meter functions. Where this page says "load fails", it means that
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
| Int (`TimeSignature/Manual/@Value`) | ASCII decimal; leading spaces and an explicit `+` are skipped, but trailing spaces are kept whenever a leading space or `+` was present (see [document container native](document-container-native.md)); `+-` is rejected; the `-` sign is passed to an untraced converter; fewer than 64 characters after the skipped prefix. Corrected 2026-10-17 from "after trimming spaces, optional sign"; see [SPEC-TRANSPORT-STATE](../specs/transport-state.md) r2. Settled 2026-10-18 by [X2](#integer-and-number-text-c): the converter is `from_chars`, which takes one optional `-` and no spaces | `201.0`, `2e2`, `0x10`, `""`, non-ASCII bytes |

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
selects the envelope value, and under which owner state, remains partly **unknown**
(PRB-N1-04/05). The retained
[v3 review checks](../../analysis/ableton-live-12.4.3/handoff-staging/transport-state-v3-analysis/review/review-checks.txt)
add a conditional static result (2026-10-19 reconciliation): the set-open validation
`0x1026fc558` checks slot +0x200 for an envelope, slot +0x290 for enablement,
and owner +0x2b8 bit 0 clear; if the envelope-derived value differs from `Manual`
by at least 1e-12 (`0x102777640`), it sets `Manual` through `0x10156e6ec`.
For song tempo, +0x200 is `0x1026f90d4` (envelope lookup) and +0x290 is
`0x1026f9240` (true). No envelope means no replacement. The owner flag's meaning
and the choice of envelope value were not interpreted, so this does not establish
an unconditional first-event precedence or any scene/meter rule. See
[REQ-TRANSPORT-STATE-012](../specs/transport-state.md#req-transport-state-012--precedence-between-stored-tempo-and-meter-sources).

## Writer number format

**Observed** (`0x101520c70`, `0x101520dbc`, and the formatters `0x101431584` and
`0x101431788` ✓ n1-0007):

- A non-finite value is written as `#` plus uppercase hex bits (8 digits for Float,
  16 for Double). The largest finite value is written as `Invalid`.
- Otherwise the program takes k = ⌈log10|x|⌉, or ⌊log10|x|⌋ when log10|x| < 0, and
  formats with `%.*lf` (`0x105b8f6c9`) at precision max(0, 9 − k) for Float or
  max(0, 17 − k) for Double. Zero uses precision 8 or 16. Trailing `0`s and a
  trailing `.` are then removed.
- Correction 2026-10-18 ([X2](#number-text-on-save-a-b)): "log10|x|" here is the
  binary64 result of the library `log10`, not the exact logarithm. Next to powers of
  ten the two give different k.
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

## Extracted execution results (X2, 2026-10-18)

**Question.** Four clauses of [SPEC-TRANSPORT-STATE](../specs/transport-state.md)
r2 could be settled by running the original x86_64 code. They are (a) REQ-011's k
next to powers of ten, (b) negative zero on save, (c) the REQ-006 integer spellings
and whether the number reader treats them the same way, and (d) the REQ-010 meter
codes and texts (PRB-N1-06). The method follows
[ADR 0003](../decisions/adr-0003-no-reference-execution.md#extracted-execution-of-original-code)
and the [X1 pilot](extracted-execution.md).

**Answer.**

| Target | Outcome | Label |
| --- | --- | --- |
| (a) REQ-011 k | k comes from the binary64 `log10` result L. This differs from r2 (exact logarithm) for 825 of 6,539 swept 64-bit values; no 32-bit value is affected | X; L's last bit near half a spacing U |
| (b) Negative zero | Both writers write `-0`; `-0` loads as −0 | X |
| (c) REQ-006 | Exact rule: ASCII; body `-`? digits, at most 63 characters; no `+-`; no trailing spaces after leading spaces or `+`; int32 range. ` +201 ` (TS-010) is refused, and `-0`, `-201` are accepted | X |
| (c) Number text | Not the same as the integer reader: `strtod` skips leading white space, takes a sign and ignores trailing text. The `Invalid` and `#` checks and the binary32 rounding are original code | X; grammar on glibc `strtod` |
| (d) REQ-010 | Encoder and decoder agree with the formula; the 495 value texts are `n/d` | X; display surface and out-of-range meaning U |

Evidence: [x2-transport-v1](../../analysis/ableton-live-12.4.3/r2/x2-transport-v1/manifest.json),
regenerated by `sh run.sh` (about 15 s). It contains:

- `results/writer.json`, `parse.json` and `meter.json`, byte-stable across reruns;
- `raw/runs.jsonl`, with the argv, stdout, stderr and gdb script of all 412 processes;
- `addresses.json`, with every function, how it was matched and its corpus record SHA-256;
- `imports.txt`, `x86-disasm.txt` and `summary.txt`, and the scripts.

### Method

- **Slice and loader.** The slice is the X1 slice (`1bae9a97…be999b0`). The loader is a
  copy of [tools/xexec](../../tools/xexec/xexec.c) in the evidence directory, with
  three changes. `_strtod` is bound to glibc `strtod`; the process never calls
  `setlocale`, so the locale is C. A `mk` command builds a buffer without passing it.
  A `ptrs:` argument builds a buffer of pointers, so one buffer can point to another.
  The built loader is `/var/tmp/sound-analysis/xexec/xexec-x2-transport`.
- **Substituted libraries.** glibc 2.39 replaces Apple's `log10`, `vsnprintf_l` (under
  the C locale) and `strtod`. The integer path runs only original code, `from_chars`
  included.
- **Reader setup.** The converter `0x10151b630` takes a node and a (pointer, length)
  text. It asks the node's vtable slot +0x28 for the base type and reads it with
  `0x1011ec760` (`return *p`).
  - The fake node is {`0x106a4b178`, pointer to the type id}. At `0x106a4b178` + 0x28
    the slice holds `0x103c2c670`, a `mov rax,[rdi+8]` getter, so no code is stubbed.
  - `SetValue<T>` is reached by tail jumps through the stubs `0x105a4d446` (bool),
    `0x105a4d44c` (double), `0x105a4d452` (float) and `0x105a4d458` (int). gdb stops
    there, prints the value register and returns, so the value holder is never built.
  - A refusal shows as the trap on `___cxa_allocate_exception`. The throw itself, and
    the catch, did not run.
- **Writer setup.** The writers `0x10150f6a0` (float) and `0x10150f7a0` (double)
  take the value and a stream. The stream's fake vtable sends slot +0x30 (a Live
  string) and slot +0x38 (a C string) to two unrelated entries, where gdb prints the
  text and returns. The sweep calls the formatters `0x10142b6c0` and `0x10142b980`
  directly, 100 values per process.
- **Meter setup.** The encoder, decoder and list builder are pure apart from
  allocation and the list's static guard. They were called directly.

### Function matching

| Role | x86_64 | arm64 | How matched |
| --- | --- | --- | --- |
| Float / double attribute writer | `0x10150f6a0` / `0x10150f7a0` | `0x101520c70` / `0x101520dbc` | Sole references to `#%8.8X` / `#%16.16llX`; same branches |
| Number text P = 9 / 17 | `0x10142b6c0` / `0x10142b980` | `0x101431584` / `0x101431788` | X1 |
| Attribute text converter | `0x10151b630` | `0x10152bfb8` | 5th of the 10 call sites of the int parser in each slice; same type switch (0x10–0x19), same `true`/`false`/`0`, `Invalid`, `#hex` and `strtod` structure |
| Int parser, `from_chars` | `0x100375650`, `0x100375790` | `0x1002fd908`, `0x1002fda78` | X1 |
| Meter encoder | `0x101ae7a40` | `0x101abea70` | n > 0, d − 1 < 16, popcount(d) = 1, 99·log2(d) + n − 1, else INT_MIN; called by the time-signature init `0x102829920` (arm64 `0x1026f7420`) |
| Meter decoder | `0x101ae7a00` | `0x101abea38` | The two functions with both `code % 99` and `code / 99` next to the encoder |
| Meter list, entry text | `0x102812bf0`, `0x1028127e0` | `0x1026e10a8`, `0x1026e0c6c` | Callee of the time-signature init; loops 5 × 99; text is int, `/`, int |

### Number text on save (a, b)

- **Sweep.** The sweep covers each binary64 value within ±40 steps of the double
  nearest 10ⁿ, for n = −30 to 22 and ten larger |n|. It adds every binary32 value
  within ±8 steps of each power of ten from 1e−45 to 1e38, the sign mirrors of some,
  and tie probes: 6,539 values. Each X text was compared with three models of
  REQ-011:
  - "glibc": k from glibc's `log10`. It agrees with X for 6,539 of 6,539, as it must,
    because X called the same `log10`.
  - "cr": k from the correctly rounded binary64 log10, computed in 80-digit decimal.
    It agrees with X for 6,528. The 11 others lie 0.495 to 0.556 spacings from an
    integer, where glibc's `log10` is not correctly rounded. It is not correctly
    rounded at 108 inputs in all; 97 of them do not change the text.
  - "exact": k from the exact logarithm, as r2 is worded. It agrees with X for 5,714.
    The 825 others are all binary64 values just above 10ⁿ (n = 1 to 15) or just below
    10⁻ⁿ, whose exact logarithm lies within 0.56 spacings of the integer.
  The binary32 values lie at least 22,008 binary64 spacings from an integer, apart
  from exact powers of ten, so the 32-bit text never depends on L's rounding.
- **Examples.** The doubles nearest 1e−6 and 1e−14 lie below those powers, so the
  nearest double to 10⁻ⁿ is itself affected: 0.000001 → `0.00000099999999999999995`,
  1e−14 → `0.00000000000001`. Further examples are in REQ-011.
- **Whole writer.** Through the attribute writers:

  | Value | Double field | Float field |
  | --- | --- | --- |
  | +0 / −0 | `0` / `-0` | `0` / `-0` |
  | Largest finite | `Invalid` | `Invalid` |
  | Most negative finite | its 309 digits | `-340282346638528859811704183484516925440` |
  | +∞ / −∞ | `#7FF0000000000000` / `#FFF0000000000000` | `#7F800000` / `#FF800000` |
  | NaN / −NaN | `#7FF8000000000000` / `#FFF8000000000000` | `#7FC00000` / `#FFC00000` |

  The 16 case values (4.5, 0.3, 121.2, 93.3333333 and the new REQ-011 cases) give the
  texts in the spec.
- **Ties.** Exact decimal ties round to even under glibc: 1 + 2⁻¹⁷ →
  `1.0000076293945312`, tempo 120.0078125 → `120.007812`.
- **Static arm64 comparison** (n1-0007 dossiers, corpus records in `addresses.json`).
  Both slices skip to precision 8 or 16 on `x == 0`, which is true for −0, so the
  sign reaches `%.*lf`. Both choose floor or ceiling by L < 0 (`fcsel …,mi` against
  `cmpltsd`) and truncate (`fcvtzs` / `cvttsd2si`). The writers test finiteness, then
  equality with the positive largest value, in the same order. There is no fused or
  extended-precision step. Possible slice differences are only Apple's `log10` and
  `vsnprintf_l` builds.

### Integer and number text (c)

- **Integer reader.** The parser and the converter ran on 72 texts and agreed on
  every one. The rule in REQ-006 r3 reproduces all 72.
  - The window passed to `from_chars` is text[start, start + min(len − start, len − t)],
    where start is after the leading spaces and `+` and t counts the trailing spaces.
    With leading spaces or `+`, it keeps at least one trailing space, and
    `from_chars` stops there.
  - `from_chars` takes one optional `-`, digits, and int32 range. The 63-character
    limit counts the `-`.
  - Arm64 computes the same window (`csel` at `0x1002fd9a4`) and limit (`cmp x11,#0x3f`).
- **Number reader** (types 0x12, 0x17; 133 texts).
  - Original code, no library involved: the converter compares `Invalid` by length 7
    and content. It accepts `#` and 8 or 16 hex digits of either case (mask
    `0x3f0000003f` in both slices) and swaps them to most-significant-first. Any
    other text goes to `strtod`, and the converter refuses it when nothing is
    consumed. The binary32 result is `cvtsd2ss` (arm64 `fcvt s0,d0`), so
    `3.4028236e38` and `1e39` become +∞.
  - The rest is glibc's `strtod` grammar. It accepts leading spaces, tabs and line
    feeds, a sign, trailing text, hex floats, `inf`, `infinity` and `nan`, so ` 4.5 `
    and ` +4.5 ` load 4.5. It refuses `- 4.5`, `+-4.5`, `--4.5`, `+` and `-`.
  - The number reader therefore does not refuse the padded and signed-padded
    spellings that the integer reader refuses.
- **Booleans** (13 texts) agree with REQ-003.

### Meter codes and texts (d)

- **Encoder.** For all 495 valid pairs, the code is (n − 1) + 99·log2(d). Of 160
  other pairs, a denominator outside {1, 2, 4, 8, 16}, or n ≤ 0, gives INT_MIN. A
  numerator above 99 is not checked: 100/4 gives 297, the code of 1/8, and
  2147483647/2 wraps.
- **Decoder.** For c ≥ 0 it gives (c mod 99 + 1, 1 << (⌊c/99⌋ mod 32)), so 495 gives
  1/32 and 3069 gives a denominator of INT_MIN. For c < 0 it gives (INT_MIN, INT_MIN).
  On 0–494 it inverts the encoder.
- **List.** The list builder fills a vector of 495 entries (capacity 512) whose entry
  c is `n/d` for decode(c).
- **Slices.** The arm64 encoder (n1-0008 disassembly) uses `cnt`/`uaddlv` for the
  popcount, `clz` and an integer `madd`. The decoder and list builder agree in the
  corpus pseudocode. All of it is integer arithmetic.
- **Not shown.** Whether a loaded code outside 0–494 ever reaches the decoder, and
  which UI shows the list texts. PRB-N1-06 stays U for the effective meter.

### Limits

- **Scope.** X shows what these x86_64 functions compute with this setup. The open
  and save paths, the catch of a refusal and the UI are static or unknown.
- **Slices and libraries.** arm64 equivalence is inferred from the comparisons
  above. The library-dependent results are the last bit of `log10` near half a
  spacing, exact ties, and the `strtod` grammar for signs, white space and special
  forms.
- **Missing counts.** Processes that end at the exception trap print no
  import-usage lines, so the counts in `parse.json` cover accepted texts only.
- **Loader limit.** At most 256 calls per process (`rets[256]` in the loader); the
  script stays below it.

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
| PRB-N1-06 | Time-signature codes 495, −1 and `201.0`. Parser outcomes, encoder, decoder and list texts settled by X2; the effective meter stays open |
| PRB-N1-07 | A real 12.4.3 save: number text, child order, KeyMidi omission, envelopes, SchemaChangeCount |
| PRB-N1-08 | Duplicate child, unknown child and unknown attribute outcomes |

## Shared integer-converter lead, reconciled 2026-10-19

The retained [note-storage review excerpts](../../analysis/ableton-live-12.4.3/handoff-staging/midi-note-storage-v1-analysis/review/corpus-excerpts.jsonl)
contain int32 converter `0x1002fda78` (chunk-00132 offset 138125), which accepts
a leading `-`. The retained N1 `corpus-excerpts.jsonl` record for `0x1002fd908`
(chunk-00132 offset 135671) calls that exact converter. Thus note storage's Int
fields (`MidiKey`, `CC`, list `Id`) and transport REQ-006 share the int32 parser
and converter. NoteId/NextId use a separate signed-int64 converter
`0x101524d8c` (review chunk-00813 offset 61888); its width and limits must not
be imported into the transport rule. Transport REQ-006 already settled the
int32 `-` spellings by X2 (`parse.json`, original x86 parser `0x100375650` and
converter `0x100375790`), so the lead adds traceability, not a new unknown.

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


## Pending review: persistence family routes — 2026-10-20

The [transport family structure proposal](../../analysis/ableton-live-12.4.3/full-spec-v1/family-transport-routes-v1/structure.md)
cuts this owner from approved integration packet1b, boundaries I-01, I-02 and
I-10. Its [route ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/family-transport-routes-v1/route-ledger.json)
references all twelve revision5 requirements and separates existing X leaf
conversion/format/meter routes, conditional S document paths, and predicates
with no established route. The local inventory is108predicate/context rows
(30 X,44 S,34 no-established-route), pending independent structure review.
These are route inventory units, not a frozen required-outcome denominator,
completed behavior count or grade. Required predicates share a row when they
name the same outcome; helper computations and numeric instances are inputs
or dependencies, not additional outcomes.

[Exact predecessor and source pins](../../analysis/ableton-live-12.4.3/full-spec-v1/family-transport-routes-v1/pins.json)
and the [input-set navigation](../../analysis/ableton-live-12.4.3/full-spec-v1/family-transport-routes-v1/input-sets.json)
reuse N1/S1/X1/X2/currentv3 evidence without replay. Stored fields versus active
song state, actual Save receiver and file lifecycle, malformed-error recovery,
range effects and general precedence remain separate missing joins. Number-text
library/rounding assumptions, the undecided band, older shipped-writer versions,
and all existing S/X/U qualifications remain unchanged. No requirement, case,
release or normative expectation changes; no original execution, provider,
harness, decoder or numerical run occurred for this map. Root owns the atlas,
independent review and any later batch selection.


### Family route review adopted — 2026-10-20

The [frozen transport family map](../../analysis/ableton-live-12.4.3/full-spec-v1/family-transport-routes-v1/manifest.json)
[passed independent review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/family-transport-routes-v1-review.json)
with no findings. The 108 bounded predicate/context rows cover the stated
current-owner distinctions; 30 X / 44 S / 34 no-established-route remain route
inventory, not grades. The review checked 19 relationships, five missing public
bridges and the selected source/release identities. Typed member stores and
number formatting do not establish active engine state, public Save/reopen,
error recovery or general envelope/template precedence. Existing case/U and
Apple-library/logarithm qualifications remain unchanged. Document structure and
ALS-container mapping proceeds next; no original execution was selected here.


## Transport whole316 typed-bit actual approval — 2026-10-21

The [whole316 packet](../../analysis/ableton-live-12.4.3/full-spec-v1/batch-transport-standing-leaves-v1/manifest.json) (30 payloads / 2,267,445 bytes; manifest SHA-256 `fcf5328bcfb2c2c160cf33bccb7627a29703c2cea539188bbe826bacab8c4236`) [passed independent review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/transport-standing-leaves-v1-review.json) with no findings (30,554 bytes; SHA-256 `2cdd28a03e473553e3cc8a0807dfaf5e4541ad623ec5d7368caa25e985507fb7`). Root adopts that bounded review by citation under design12; the same observations receive no second review.

The finite class is158 exponent-all-ones IEEE words in upper/lower hex strings: each sign and width, with fraction0, every one-hot fraction bit and all fraction bits set. This gives316 distinct typed strings,313 new and three exact historical members. All316 intercepted SetValue argument words match REQ004/005's declared bit oracle; all50 sign-extended float HITs are masked to the selected low32 bits. These are integer-bit observations, including infinity/quiet-bit-clear/quiet-bit-set layouts, with no floating-value decode, signaling-exception, arithmetic, quieting or FP-state law. They do not cover all NaN payloads or IEEE words.

Eight existing-model GDB groups contain316 conversions plus eight recorded empty-string initializers (324 direct entries), with26/55 calls and100/216 owned buffers per float/double group. All eight debugger exits are0 with separate normal-inferior-exit records; the inferior OS wait status was not separately collected. Four existing GDB return stubs skip the original SetValue bodies. This establishes supplied-model typed argument delivery, not real node storage, public Transport field admission, Open/Save, effective range, writer formatting or Apple/ARM equivalence.

The reviewer checked the complete30-payload tree, all source/input/script/raw-bit joins,31 recorded before/after custody identities, twelve independent negative controls and the new data-only checker after full source reading. Each group declares1,882 bindings (1,795 trap /86 Linux /one Linux-data); the five actually counted allocation/guard/atexit names and2/2/1/1/1 counts agree. Zero counted strtod/libm use is not provider/global-data absence. All eight stderr files retain the same80-byte GDB index-cache warning. The stdout libthread_db identity is after-only, not a before pin or complete provider trace.

Structural/status/import/custody checks occur after each group, so later within-group calls can precede detection; the collector stops subsequent groups on raised errors. Its import guard checks binding class, not an exact five-name whitelist; the reviewer independently checked the captured names/counts. Oracle mismatches would be retained rather than automatically fatal. The sole attempts required no retry or original fault recovery. JSON/raw files are closed and hashed without explicit fsync; byte sealing (observed POSIX0664) is not OS write protection or crash durability. Existing model/ABI/source-to-loader premises are inherited, not independently reconstructed here.

Review approval clears the source-pin window for the next owner revision.313 finite new cases may be admitted directly while keeping three historical strings as supporting controls. No public, ARM, formatter, storage, calibration, native-site or whole-product credit follows. Required unsupported behavior stays U/OPEN. Frozen inventory remains691X /1,076S /3,857none across32 heterogeneous cuts (Analog199X predecessor scope); indirect25,071baseline +24conditional =25,095of268,015.


## Transport owner r6 finite adoption — 2026-10-21

The [R6 owner packet](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-transport-typed-hex-finite-v1/manifest.json) (seven payloads /825,548 bytes; manifest SHA-256 `82782168fdf1baad59323329217659e20f5aeec080d4556e3a29efa6e31c1c6d`) directly adopts313 finite converter cases TS-038–350 and three historical input controls from the approved316 observations. [Added-wording/preservation review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/transport-owner-r6-added-wording-review.json) (3,168 bytes; SHA-256 `9bdcc53b61b96ccb9f14241fe2765d913357361e340363ebb583646c8e1fb018`) inherits the actual review without repeating it.

The complete194-line owned checker was read before Root's invocation and passed15 negative controls. All12 prior requirement bodies remain exact prefixes, the other ten whole bodies and all37 legacy rows remain exact. Independent minimal-delta reversal reconstructs the full34,329-byte R5 predecessor. TS-023 stays withdrawn:350 IDs include that withdrawal,349 are nonwithdrawn, and three supporting controls are separate. These counts are navigation, not a required-outcome denominator.

The new catalog keeps exact ASCII, integer words including payload/sign bits, raw sign-extension provenance and immutable input/result pointers; experimental type IDs are evidence locators, not a candidate API. Pure conversion bit comparison is separate from the legacy F0/public load/save comparators. Original SetValue bodies remain skipped. Public field/storage/range admission, formatter, FP state, ARM/Apple and application outcomes remain U; all old unknowns and logarithm/library qualifications remain. No new neutral fixture or release is supplied, and current v3's33 records remain unchanged. R5 mutable-source pins are historical as-of evidence, not future gates against R6. Unsupported required behavior keeps coverage OPEN.

## Standing-class eligibility after finite adoption — 2026-10-21

The [316-string batch and R6 adoption](#transport-owner-r6-finite-adoption--2026-10-21)
cover the selected exponent-all-ones typed-word class: 313 new finite converter
cases and three historical members. This does not exhaust strings or IEEE
payloads, and it does not observe the SetValue bodies that the existing model
skips. The [map input inventory](../../analysis/ableton-live-12.4.3/full-spec-v1/family-transport-routes-v1/input-sets.json)
also retains 495 distinct valid meter pairs/codes, historical formatter/parser
sets and their separate setup qualifications. These existing observations are
not a new unrun enum class merely because 30 route rows carry X.

The concrete remaining `sets.missing-five-fields`, `sets.range-contexts` and
`sets.precedence-contexts` concern compatible constructed owners, field
precedence, scene/envelope state and actual loaded/displayed/saved values.
Their receiver/state prerequisites are not supplied by another typed-string
sweep. The meter-list allocator/guard model and intercepted scalar conversion
are separate scopes; neither proves public field admission or writer delivery.

The reviewed metadata supplies no additional complete, missing standing class
for selection here. That conditional result is not an exhaustive statement
about all strings, ranges, locales or state histories. Public storage/range,
Open/Save, formatter/library and Apple/ARM joins remain unknown. This assessment
read canonical conclusions and retained input metadata only; it ran no original,
parser, writer, model, comparator or tool and added no coverage or grade.
