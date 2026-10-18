---
id: RESEARCH-DEVICE-TABLES-NATIVE
type: research
status: draft
updated: 2026-10-17
access: analysis
target: Ableton Live 12 Suite 12.4.3 arm64
---

# Analog, Tension and Collision: parameter index and conversion tables (static)

Packet N6 for FEAT-DEVICES and [Q-006](../questions.md#q-006-native-analysis-and-resource-decoding).
It completes the Live-side tables that [device parameter mapping](device-parameter-mapping-native.md)
(N5) left open because their builders are nested. Bounded question: for Analog (`UltraAnalog`),
Tension (`StringStudio`) and Collision (`Collision`), which stored parameter goes to which
`SetParameterA` index, with which conversion, and what are the constructor defaults? Static evidence
only; nothing was executed and Live cannot run on this host. A decompiled line or call edge is not
proof of runtime behavior. The storage contract built on this page is the draft
[SPEC-BUNDLED-DEVICE-PARAMETERS](../specs/bundled-device-parameters.md).

## Evidence

Retained run: [n6-device-tables-v1](../../analysis/ableton-live-12.4.3/r2/n6-device-tables-v1/manifest.json)
(`notes.md` there has the method, the function map, the three dossier rounds and every command).
Live `Live.arm64` SHA-256 `3a99ceea…d1c383cfad`, image base 0x100000000; 24 dossiers in
`results/n6-0001` to `n6-0003`, unchanged; 71 cited C1 records in `out/live_corpus_excerpts.jsonl`.
Stored ranges and bundle tables come from H4 ([device bundles](device-bundles-static.md)).

| Output | Content |
| --- | --- |
| `extract_nested.py` → `out/live_index_map.tsv`, `live_index_summary.json`, `registration_classes.json` | 472 vector entries in index order with member path, mapping mode and its operands, stored range, bundle kind and range |
| `constructors.py` → `out/constructors.tsv`, `constructors_summary.json`, `nonparam_fields.tsv` | One row per configured member: set-up helper, internal range, user converter, default; non-parameter field values |
| `conversions_nested.py` → `out/conversions.tsv`, `crosscheck.json` | 475 rows (472 entries and 3 unvectored `PerNotePitchBendRange`): stored domain, converter, default, Defaults-preset value, mode, emitted range, value sent for the default, bundle cross-check |
| `asm_order_check.py`, `loader_slots.py`, `number_text_check.py` → `out/*.txt`, `*.json` | Disassembly order check, loader vtable slots, stored value text check |
| `spec_tables.py` → `out/spec_tables.md`, `spec_defaults.tsv` | The 502 stored parameters of all seven devices with class, domain and default, for the spec |

## Method and checks

**Observed.**

- The three builders at vtable +0x5a0 (Analog `0x1031ad110`, Tension `0x103193b1c`, Collision
  `0x1030debd0`) call seven sub-builders. Every push has an inline path and an emplace call. The
  decompiled text was executed twice, with all capacity tests true and with all false, following
  sub-builders into their sub-objects. Both runs give the same 472 entries, members and mode words.
- In the dossier disassembly, the emplace calls of the three top builders, in address order, equal the
  derived sequences (20, 130 and 37 entries). Four sub-builders match as sequences (their first entry's
  slow block is placed last). Three match as sets of member offsets (`out/asm_order_check.txt`).
- Member names come from the class registrations (`0x10147e954`), with base classes from the static
  class definitions (`0x10147e7c4`) and the `Envelope.0/1` array (`0x10147eacc`). Every stored
  parameter except `PerNotePitchBendRange` is carried by the vectors; nothing else stored is missing.
- Two Analog entries come from a virtual getter (+0x1e8). The vtables of `AUltraAnalogSignalChain1`
  and `2` (address points `0x1068dcb38`, `0x1068dcd40`) hold `0x1031b6254` and `0x1031b670c` there;
  both return slot 0x500, which is `FilterToFilter2` in chain 1 and `FilterControllee` in chain 2.
- Constructor defaults: 412 of 426 set-up calls had their float (s0–s2) or integer (w1/w2) arguments
  re-read from disassembly with no mismatch. The rest are a fixed-default helper (`0x103192a6c`:
  −1..1, default 0.5, checked in its own dossier) and four chain-dependent booleans.
- For every stored parameter of the three devices, the user domain of Live's converter equals the
  modal stored range H4 found in shipped content (417 of 417, asserted).

**Inferred.** The two hand models (Collision modulation targets, the virtual getters) are faithful;
both were read in full and are cited in `notes.md`.

## The three tables

Modes are the mapping modules of N5's table (0 identity, 1 polarizer, 2 toggle mapping, 3 filter type,
4 bool inverter, 5 to-toggle, 6 multiply-offset, 7 integer table, 8 Collision scaled). Unless a row
says otherwise, entries use mode 0 and Live's internal range equals the stored domain: 0..1 linear,
−1..1 linear, enumeration index or Boolean 0/1.

**Second outputs (Observed).** Every empty entry receives a second output: the next index after a
mode-1 entry (the sign of a bipolar amount) or a mode-3 entry (the filter-type low bit), or the
index named by a mode-5 entry (Polyphony's flag goes to index 7). The only exception is Tension
index 2, which nothing writes and which the bundle lacks: H4's "one gap".

### Analog (`UltraAnalog`): 203 entries, 31 second outputs

| Indices | Parameters |
| --- | --- |
| 0–27 | `Polyphony`, `PitchBendRange`, `Volume`, `Octave`, `Transpose`, `KeyboardFineTune`, `KeyboardUnison` (6) + flag (7), `KeyboardPriority` … `KeyboardError`, `Vibrato*` (13–19), `Portamento*` (20–23), `Noise*` (24–27) |
| 28–86, 111–169 | `SignalChain1`, `SignalChain2`: oscillator, filter (with `FilterToFilter2` / `FilterControllee` at 56 / 139), amplifier and LFO, in that order |
| 87–110, 170–193 | `Envelope.0` and `Envelope.1` of each chain; each starts with the unstored `ToggleDummy` (constant 1) |
| 194 | unstored `DummyPerNotePitchBendRange` (0..48, default 48) |
| 195–202 | `ChannelPressureTarget1/2`, `ChannelPressureAmount1/2`, `MpeCC74Target1/2`, `MpeCC74Amount1/2`, interleaved |

| Parameter (both chains where named) | Stored domain | Live conversion → value on the index |
| --- | --- | --- |
| `Polyphony` | 0..9 | mode 5: max(v − 1, 0) → 0..8 at index 0; v > 0.5 → index 7 |
| `Octave`, `OscillatorOct` | −3..3, integer steps | legacy-int, mode 6: v + 3 → 0..6 |
| `Transpose`, `OscillatorSemi` | −12..12, integer steps | legacy-int, mode 6: v + 12 → 0..24 |
| `KeyboardUnison` with `KeyboardUnisonToggle` | 0..1 | mode 2: v + 1 when the toggle is on, else 0 → 0..2 |
| `LFOSync` with `LFOSyncToggle` | 0..23, integer steps | legacy-int, mode 2 → 0..24 |
| `NoiseBalance`, `OscillatorBalance` | 0..1 | mode 6: 1 − v |
| `FilterType` | 0..9 | mode 3: v >> 1 → 0..4; v & 1 → next index |
| 28 bipolar amounts (`OscillatorEnvAmount`, `Filter*Mod`, `Amplifier*Mod`, …) | −1..1 | mode 1: \|v\| → 0..1; sign flag → next index |
| `ChannelPressureAmount1/2`, `MpeCC74Amount1/2` | −1..1, default 0.5 | identity; bundle clamps to −10..10 |

Cross-check (Observed against H4's bundle table): 197 entries exact, 6 within the bundle range
(`FilterType` emits 0..4 into 0..5; the four amounts into −10..10), no mismatch. H4's "XML has
32 × −1..1 … the bundle has none" is explained: Live sends those as magnitude and sign.

### Tension (`StringStudio`): 130 entries (0–129), 25 second outputs, 1 unused

| Indices | Parameters |
| --- | --- |
| 0–23 | `Polyphony` (flag at 7), `PitchBendRange` (2 unused), `Octave`, `Transpose`, `Keyboard*`, `Vibrato*`, `Portamento*` |
| 24–83 | `GeoExcitator*`, `GeoDamper*`, `Excitator*`, `Pickup*`, `Damper*`, `String*`, `Termination*` |
| 84–120 | `LFO*`, `Filter*`, `FilterEnvelope*`, `Body*` |
| 121 | unstored `DummyPerNotePitchBendRange` |
| 122–129 | `ChannelPressureTarget/Range1/2`, `SlideTarget/Range1/2` |

| Parameter | Stored domain | Live conversion → value on the index |
| --- | --- | --- |
| `PitchBendRange` | 0..12, integer steps | legacy-int, mode 6: v / 12 → 0..1 |
| `Polyphony`, `Octave`, `Transpose`, `KeyboardUnison`, `LFOSync` | as Analog | as Analog |
| `PortamentoProportional` | Bool | mode 4: inverted |
| `BodyType` with `BodyToggle` | 0..3 | mode 2 → 0..4 |
| `FilterType` | 0..9 | mode 3 |
| 23 bipolar `*KbdMod`, `*VelMod`, `*LFOMod`, `*EnvMod` | −1..1 | mode 1 |
| `ChannelPressureRange1/2`, `SlideRange1/2` | −1..1, default 0.5 | identity; bundle −10..10 |

Cross-check: 124 exact, 5 within, the unused index 2 matches the bundle gap.

### Collision (`Collision`): 139 entries (0–138), no second outputs

| Indices | Parameters |
| --- | --- |
| 0–10, 11–24 | `Mallet/*`, `Noise/*` (`Noise/Q` at 20) |
| 25–57, 58–90 | `Resonator1/*`, `Resonator2/*` |
| 91 | `ResonatorOrder` |
| 92–105, 106–119 | `Lfo1/*`, `Lfo2/*`, each ending with `Target1/2` (`Target`, `Amount`) |
| 120–138 | `PitchBendRange`, `PitchBendTarget1`, `ModWheelTarget1/2`, `ChannelPressureTarget1/2`, `Polyphony`, `Retrigger`, `Volume`, unstored `DummyPerNotePitchBendRange` (134), `MpeCC74Target1/2` |

| Parameter | Stored domain | Live conversion → value on the index |
| --- | --- | --- |
| `Vel*` amounts | −5..5 (`Noise/VelToFreq` −8..8) | identity (Live range = stored range) |
| `Key*` amounts | −2..2 (`KeyToPan` −1..1) | identity |
| `Resonator*/DecayOnNoteOff` | 0..1 | mode 6: 1 − v |
| `Resonator*/Transpose`, `FineTranspose`, `Lfo*/SyncRate`, `PitchBendRange` | −48..48, −50..50, 0..21, 0..24, integer steps | legacy-int |
| `Lfo1/Target*/Target` | 0..16 | mode 7, table 0–14, 16, 17 (skips 15) |
| `Lfo2/Target*/Target` | 0..16 | mode 7, table 0–16 (skips 17) |
| all `*/Amount` of modulation targets | −5..5, default 2.5 | mode 8: v, or v × 0.125 when the target value is 4 or 9 |

The LFO tables come from bytes `0x1068c5398 + 0x28k + n` (k = 0..17, n = LFO number), read from
the image; a byte with bit 0 clear keeps k. The other targets use 0..17 directly.

Cross-check: 81 exact, 54 within (Live's ±5 and ±2 amounts inside the bundle's −10..10 clamp; see
positions below), 1 unrecovered (H4 index 28 lost an argument), 3 mismatches:

- `Resonator1/VelToStartTranspose`, `Resonator2/VelToStartTranspose` (indices 32, 65): Live −5..5,
  bundle kind 1 −1..1. Static reading: stored values beyond ±1 have the same effect as ±1. Shipped
  content stays within 0..3.75.
- `Resonator2/Type` (59): Live 0..6, bundle kind 3 0..5, while `Resonator1/Type` is 0..6 on both
  sides. Static reading: type 6 on resonator 2 acts as 5. Shipped content stores 6 there.

**Positions (Observed, contradiction kept open).** `Resonator*/HitX`, `ListeningXL` and
`ListeningXR` go out as 0..1 with mode 0, and the bundle entries are kind 1 with range −2..2, which
rescales to 0..127. On this chain the full stored range reaches 63.5–95.25 only. Corpus shows the same
shape (64 + 31.5v; N5). Two devices with the same pattern make an unmodelled Live-side rescale more
likely than an engine that uses a quarter of its range, but nothing found in the code supports either.
P4-N5-01 and P4-N6-01 settle it.

## Defaults and non-parameter fields

- **Constructor defaults (Observed).** All 417 stored parameters of the three devices have one
  constructor value (`out/spec_defaults.tsv`; the spec lists them). Chain-dependent: Analog chain 1
  starts with oscillator and amplifier on, chain 2 with both off.
- **Defaults presets differ (Observed).** 24 Analog, 9 Tension and 2 Collision stored values in
  `Core Library/Defaults/Instruments/*.adv` differ from the constructor values, for example Analog
  `SignalChain2/OscillatorToggle` (preset true, constructor false), Tension `StringDecay` (1 vs
  0.75), Collision `Resonator1/OnOff` (true vs false) and `PerNotePitchBendRange` (48 vs 0 for all
  three). Which one a new instance gets is P4-H4-03 / P4-N5-03.
- **Non-parameter fields (Observed, `out/nonparam_fields.tsv`).** The constructors set every
  `*RelativePosition` to −1073741824, Analog `SelectedFinger` to 7, Tension and Collision `CurrentTab` to
  0, Collision `ResonatorNumber` to 1 and 2, and the `*On` MPE flags to 0. These equal H4's shipped
  values, so DEV-C09's values are now also constructor values for these three devices.
- **Runtime-only members.** `ToggleDummy`, `IsChain2` and `DummyPerNotePitchBendRange` are registered
  but absent from the schema; they are not stored.

## Load handling

- **Observed** (`out/loader_slots.txt`): `ATimeableFloat`, `ATimeableEnum`, `ATimeableBool` and every
  device and sub-object class here use the generic member loader `0x101487310` at +0x140, the one N1
  read: it visits the members present, skips unknown names and stores base-type values without a range
  check ([transport-state native](transport-state-native.md#range-handling)). The Timeable post-load hook
  `0x1026fc4cc` (→ `0x1026fd6f4`, `0x1026fd7d4`) maintains automation and modulation links and has no
  range test. Enumerations store the index directly, as N1 found for `ARemoteableEnum`.
- **Observed** (`out/number_text_check.json`): in the 599 shipped documents with these devices, all
  114,570 Float `Manual` and range texts of the seven devices equal the N1 32-bit writer rule, all
  6,771 Enum texts are plain decimal integers and all 7,515 Bool texts are `true` or `false`. The device
  envelope's `On` parameter is included in the Bool count.
- **Inferred:** a device read from a document is constructed with the values above and then receives
  only the members present, stored without range checks. The document-level create path for device list
  items was not traced; the S6 packet traced the generic create-then-load sequence for automation
  ([automation envelopes](automation-envelopes.md#native-reading-defaults-and-load-checks)). What Live then
  displays, sends and re-saves for an out-of-range value is unknown (P4-H4-02); the converters clamp
  what reaches the engine (N5).

## Corrections to earlier pages

- [Device bundles](device-bundles-static.md#where-the-parameter-model-lives), table row Analog and
  Tension "Differ: XML has … −1..1 …; the bundle has none": Live sends bipolar amounts as magnitude plus
  a sign flag on the next index. Row Collision "Mostly differ": the ±5/±2 amounts fit the bundle's
  −10..10 clamp; three real mismatches remain (above).
- [Device parameter mapping](device-parameter-mapping-native.md#unknowns), first bullet: resolved here.

## Unknowns

- Enumeration labels for Analog, Tension and Collision (label tables are built at run time and were not
  decoded); the meaning of each mode-7 target number.
- The effect of the three Collision mismatches and of the position ranges (P4-N6-01, P4-N5-01).
- The document create path for device list items, and the display, use and re-save of out-of-range
  stored values (P4-H4-02).
- Which defaults a newly inserted device gets (P4-H4-03, P4-N5-03).

## Phase 4 probe records

Per [ADR 0002](../decisions/adr-0002-static-first-analysis.md); batched with P4-H4-01 to 05 and
P4-N5-01 to 04 on the macOS reference host. Inputs are copies of shipped files.

| Probe | Question | Static evidence so far | Minimal input | Discriminating observation | Stop when |
| --- | --- | --- | --- | --- | --- |
| P4-N6-01 Collision index trace | Do the three mismatches and the positions behave as derived? | Index table and bundle ranges above | Breakpoint on Collision `_SetParameterA` (arm64 `0x12a1c`); copies of `Defaults/Instruments/Collision.adv` with `Resonator1/HitX` 0 and 1, `Resonator1/VelToStartTranspose` 3, `Resonator2/Type` 6 | Logged (index, value): (51, 0/1) on this chain or (51, −1/1); (32, 3) arrives unclamped; (59, 6) arrives | Each value logged once |

## Limitations

- The index tables rest on a pattern interpreter for this decompiler's output, checked against
  disassembly as described. Two parts are hand models.
- Analog and Tension display names are only partly resolved in `constructors.tsv`; they are not used.
- No organization is attributed to any binary.
