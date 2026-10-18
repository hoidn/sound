# N6 device tables v1: analyst notes

Packet N6 (FEAT-DEVICES, Q-006). Live 12.4.3 `Live.arm64` (SHA-256 `3a99ceea…d1c383cfad`, image base
0x100000000). Static only; nothing was executed. Pages: `wiki/research/device-tables-native.md`,
`wiki/specs/bundled-device-parameters.md`. Extends N5 (`../n5-device-mapping-v1`) to the three nested
builders N5 left open: Analog (`UltraAnalog`), Tension (`StringStudio`), Collision (`Collision`).

## Sources and tools

- C1 corpus and C2 indexes under `/var/tmp/sound-analysis/corpus/`, read through the unmodified
  `../n1-transport-state-v1/corpus_lookup.py` (cache in the session scratchpad via `N1_CACHE`). Cited
  records retained in `out/live_corpus_excerpts.jsonl` (71 records, chunk, offset and line SHA-256).
- Dossiers from the shared read-only R2FunctionDossier server, copied unchanged to `results/n6-000{1,2,3}/`.
- `analysis/ableton-live-12.4.3/derived/Live.arm64` for 8-byte constants, the mode-7 byte tables, UTF-16
  names held as data, and vtable/typeinfo words (chained-fixup rebase decoded as in N1 `read_ptrs.py`).
- H4 outputs `../h4-devices-v1/out/{param_table.tsv,param_tables.json,inputs.jsonl,occurrences.jsonl}`;
  N5 `../n5-device-mapping-v1/conversions.py` (its `sent()` and `SPEC` rows, imported, not modified);
  N1 `../n1-transport-state-v1/check_number_format.py` (its `fmt`, imported, not modified).
- Shipped documents under the read-only bundle (`number_text_check.py` re-checks each SHA-256 against H4).

Commands (cwd = this directory, `python3 -I`, Python 3.13 standard library; `N1_CACHE` set):

```
python3 -I extract_nested.py out ../h4-devices-v1/out ../../derived/Live.arm64        # live_index_map.tsv, live_index_summary.json, registration_classes.json
python3 -I constructors.py out ../h4-devices-v1/out ../../derived/Live.arm64 results  # constructors.tsv, constructors_summary.json, nonparam_fields.tsv
python3 -I conversions_nested.py out ../h4-devices-v1/out                              # conversions.tsv, crosscheck.json
python3 -I asm_order_check.py out results                                              # asm_order_check.txt
python3 -I loader_slots.py out ../../derived/Live.arm64                                # loader_slots.txt
python3 -I number_text_check.py out ../h4-devices-v1/out "<app>/Contents/App-Resources" # number_text_check.json
python3 -I spec_tables.py out ../h4-devices-v1/out                                     # spec_tables.md, spec_defaults.tsv
python3 -I ../n1-transport-state-v1/corpus_lookup.py excerpt out/live_corpus_excerpts.jsonl <71 entries>
python3 -I make_manifest.py . "<app>" ../../derived/Live.arm64
```

## Method

1. **Index order.** The +0x5a0 builders push one 0x38-byte entry per `SetParameterA` index (N5). Each
   push has an inline fast path and an out-of-line emplace call; Ghidra interleaves them with gotos.
   `extract_nested.py` compiles the decompiled text to a flat jump list and executes it twice: every
   capacity test true (fast) and every test false (slow). Sub-builders are followed with the sub-object.
   Both runs give the same member sequence and mode words (asserted) for all 472 entries.
2. **Names.** `FUN_10147e954(&class, -1, -1, slot, L"mpName", …)` registers members; the getter assigned
   just before gives the value class or the sub-object class. Array members use `FUN_10147eacc` (total,
   stride) → `Envelope.0/1`. Base classes come from `FUN_10147e7c4(&class, L"Name", n, &base)` in the
   static initialisers 0x1030f1c08, 0x10319bd08, 0x1031c639c. `mpQ` (Collision Noise) is a data UTF-16
   string read from the image.
3. **Virtual getters.** Analog pushes `(*(obj)+0x1e8)(obj)` once per signal chain. The vtable of
   `AUltraAnalogSignalChain1` (address point 0x1068dcb38) has 0x1031b6254 at +0x1e8, chain 2 (0x1068dcd40)
   0x1031b670c; both return `*(this+0x508)`, slot 0x500 (`FilterToFilter2` / `FilterControllee`).
4. **Collision modulation targets.** `FUN_1030cb434(target, vec, source)` was read in full and modelled by
   hand: source 0 → Target mode 0; otherwise Target mode 7 with the table of k in 0..17 whose byte
   `0x1068c5398 + 0x28k + source` has bit 0 clear; then Amount mode 8. LFO 1 passes 1, LFO 2 passes 2.
5. **Constructors.** `constructors.py` walks each device constructor and the sub-object constructors it
   calls (control flow executed with the chain/resonator index constant; static-init guards taken once).
   Set-up helper semantics (internal range, converter, default argument) are in `SETUP`, read from:
   0x103192720 → 0x103197830 (0..1, `ALinearUserFloatConverter(0,1)` unless arg 8 overrides),
   0x103192974 → 0x103197e1c (−1..1), 0x103192a6c (−1..1, fixed default 0.5 — n6-0003 disassembly
   `fmov s2,0x3f000000`), 0x1030cb214 (−5..5), 0x1030cdf18 (−2..2), 0x1026f0b58 (lo, hi, default,
   converter argument), 0x10319285c/0x1031980a4 (bool), 0x1026ef060/0x1026ef0dc (enum; default in w1),
   0x101564728 (plain bool: `ToggleDummy`, `IsChain2`). Converters: 0x101575868 linear, 0x101577e1c
   legacy-quanting int, 0x101578050 quantizing, 0x101576354 log10.
6. **Disassembly checks.** For every set-up call in the 12 dossier-covered constructors, s0/s1/s2 (floats)
   or w1/w2 (bool/enum defaults) are re-read from the disassembly: 412 of 426 calls checked, 0 mismatches.
   The 14 unchecked are the fixed-default 0x103192a6c (checked once in its own dossier) and four
   chain-dependent booleans (`iVar8 == 0`, chain index 0 or 1, from the top constructor's
   `FUN_1031a7d8c(chain, 0|1, …)`). `asm_order_check.py`: the slow-path emplace calls of the three top
   builders, in address order, equal the interpreter's sequence (20, 130 and 37 entries); four sub-builders
   match as sequences with the first entry's slow block placed last; three match as offset sets.
7. **Computed arguments (`OVERRIDES`).** Collision LFO SyncRate: range `0..FUN_1020ef18c()-1` and default
   `FUN_1020ee0f4()`; both callees return constants (0x16, 4) → internal 0..21, legacy-int, default 4.

## Rounds

| Round | Request | Functions | Resolution | Next |
| --- | --- | --- | --- | --- |
| 1 | n6-0001 | 0x1030cac68 ModTarget, 0x1030ccacc Lfo, 0x1030cf96c Mallet, 0x1030d1d80 Noise, 0x1030d6708 Resonator, 0x1030dc3cc Collision, 0x103189a7c Tension, 0x1031a3acc Analog constructors | Float and integer defaults confirmed in disassembly | Signal-chain constructors, builder order |
| 2 | n6-0002 | 0x1031a7d8c chain, 0x1031b4554 envelope, 0x1031b625c / 0x1031b6714 chain-specific, builders 0x1030debd0, 0x103193b1c, 0x1031ad110, 0x1031adde8 | Top-builder order confirmed; chain defaults | Remaining sub-builders |
| 3 | n6-0003 | 0x1030d0098, 0x1030d2eb0, 0x1030d8ebc, 0x1030ce134, 0x1031b5104, 0x1030cb434, 0x103192a6c, 0x1030cb214 | Sub-builder order; fixed 0.5 default; −5..5 helper | Stopped: questions answered; round 4 unused |

## Findings beyond the tables

- **Empty entries.** All 31 Analog and 25 of 26 Tension empty entries receive a second output: index + 1
  after a mode-1 (ModulationPolarizer: sign flag) or mode-3 (FilterType: low bit) entry, or the index in
  the high word of a mode-5 entry (Polyphony → index 7). Tension index 2 is unused; the bundle has no
  index 2 (H4's "one gap").
- **Non-parameter fields** (`out/nonparam_fields.tsv`): constructors set `*RelativePosition` to
  0xC0000000 (−1073741824), Analog `SelectedFinger` 7, Tension and Collision `CurrentTab` 0, Collision
  `ResonatorNumber` 1/2, `*On` flags 0. Matches H4's shipped values (DEV-C09).
- **Loader.** `ATimeableFloat`, `ATimeableEnum`, `ATimeableBool` and every device and sub-object class have
  the N1 generic member loader 0x101487310 at +0x140 (`out/loader_slots.txt`). The Timeable post-load hook
  0x1026fc4cc (→ 0x1026fd6f4, 0x1026fd7d4) updates automation/modulation links and has no range test.
- **Value text.** 114,000+ Float `Manual`/range texts in 599 shipped documents reproduce the N1 32-bit
  writer rule; every Enum is plain decimal, every Bool `true`/`false` (`out/number_text_check.json`).
- **Bundle cross-check** (`out/crosscheck.json`): Analog 197 exact + 6 within, Tension 124 + 5 + 1 gap,
  Collision 81 + 54 + 1 unrecovered (H4 row 28) + 3 mismatches: Resonator1/2 `VelToStartTranspose`
  (Live −5..5, bundle kind 1 −1..1) and Resonator2 `Type` (Live 0..6, bundle kind 3 0..5).
- **Collision positions.** `HitX`, `ListeningXL`, `ListeningXR` (both resonators) are sent as 0..1 with
  mode 0, and the bundle entries are kind 1 −2..2 (→ 0..127): on this chain they reach 63.5..95.25 only.
  Same shape as the open Corpus position contradiction (P4-N5-01).

## Contradictions and limits

- The interpreter is a pattern executor for this decompiler output, not a C front end. Unrecognised
  statements that touch the vector raise; none remained.
- `FUN_1030cb434` and the two virtual getters are modelled by hand (read in full; cited above).
- Defaults: the constructor values are Observed; whether a device created while loading a document
  starts from them, or from a Defaults preset first, is not traced (N1: the top-level factory path
  was not traced). Display names in `constructors.tsv` are partly unresolved (`pcVar7`, `?` prefixes);
  they are not used by the pages.
- Enumeration labels for the three devices were not extracted (label tables are built at run time).
