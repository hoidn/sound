---
id: RESEARCH-DEVICE-PARAMETER-MAPPING-NATIVE
type: research
status: draft
updated: 2026-10-17
access: analysis
target: Ableton Live 12 Suite 12.4.3 arm64
---

# Device bundles: Live-side loading and parameter mapping (static)

Packet N5 of [roadmap revision 2](native-decompilation-roadmap.md#revision-2-proposal--2026-10-17),
for FEAT-DEVICES and [Q-006](../questions.md#q-006-native-analysis-and-resource-decoding). It is the
Live side of the boundary described in [device bundles (static)](device-bundles-static.md).
Bounded question: how does Live 12.4.3 load the seven device bundles and drive them? Static evidence
only. Nothing was executed, and Live cannot run on this host. Signal processing is out of scope. A call
edge or decompiled line is not proof of runtime behavior.

## Evidence

Retained run: [n5-device-mapping-v1](../../analysis/ableton-live-12.4.3/r2/n5-device-mapping-v1/manifest.json)
(`notes.md` there has the function map, the four dossier rounds and every command).

- Live `Live.arm64` (SHA-256 `3a99ceea…d1c383cfad`, image base 0x100000000): 32 function dossiers from
  the read-only query server in `results/n5-0001`…`n5-0004`, unchanged. Other cited decompiled functions
  from the C1 corpus are copied into `out/live_corpus_excerpts.jsonl` (76 records). Pointer words and
  typeinfo names were read from the image bytes.
- Corpus bundle (`Corpus.bundle`, arm64 slice at offset 278,528): helper-corpus records in
  `out/corpus_bundle_excerpts.jsonl`; vtable, class names and a table read from the slice in
  `out/corpus_bundle_facts.json`.
- Stored ranges and default-preset values from H4 `out/param_table.tsv`; bundle index tables from H4
  `out/param_tables.json`.

| Output | Content |
| --- | --- |
| `extract_mapping.py` → `out/live_index_map.tsv`, `out/live_index_summary.json` | For Amp, Cabinet, Electric and Corpus: the parameter vector in index order, parsed from the decompiled builders, with H4's bundle kind and range beside each row |
| `conversions.py` → `out/conversions.tsv`, `out/corpus_parameters.tsv`, `out/corpus_priority.tsv` | 82 rows: stored name, domain, labels, constructor default, internal range, mapping mode, value passed for the default, Corpus bundle rule, source call. Asserts that the index order matches `live_index_map.tsv`, and that every domain equals the stored modal range. `corpus_priority.tsv` follows six Corpus parameters from stored value to engine value |
| `excerpts.py` → `out/*excerpts.jsonl`, `out/corpus_bundle_facts.json` | Cited code and bundle facts |

Addresses are unslid vmaddrs. Bundle addresses are arm64-slice vmaddrs.

## How Live loads a bundle

**Observed.**

- Each device class has a module getter that names its bundle: Amp `0x1030b54ec` ("Amp"), Cabinet
  `0x1030ca554`, Collision `0x1030df330`, Corpus `0x1030e6104`, Electric `0x1030ec8d0`, Tension
  `0x103196dcc`, Analog `0x1031b1368`. Each calls `0x103196ec0`, which returns the existing module of
  that name or creates one. Modules are kept in one global list, so all instances of a device share a
  module.
- `0x1031983d4` builds the path `<dir>/Devices/Mac/<Name>.bundle`. `Devices` and `Mac` are inline
  short strings, and `.bundle` is the literal at `0x105c8c4a0`. It passes the path to `0x103e9728c`, a
  path test that takes an error code. Only when that test succeeds does it post the message
  `OThirdPartyDeviceFactory.Create(Handle, Path)` (descriptor `0x107027d98`).
- The handler `0x102fbdf34` constructs the loader (`0x102fbe07c`) and calls `0x102f998c4` (dossier
  n5-0001). That function:
  1. creates a CFURL and a CFBundle;
  2. calls `CFBundleLoadExecutable` unless the bundle is already loaded;
  3. on load failure, clears all entry pointers (`0x102fbe248`), releases the bundle and keeps no handle;
  4. on success, queries `GetPlugInfoU` (`0x102fbe49c`) and resolves the other six names with
     `CFBundleGetFunctionPointerForName`. The CFString constants at `0x106ba17e8`…`0x106ba18a8` hold the
     C strings `0x105bdd69e`…`0x105bdd6ef`.
- `0x102fbe25c` creates an instance. If the bundle is not loaded it retries loading first. It then
  requires all seven pointers to be non-null and `GetPlugInfoU` selector 3 to be non-zero. It calls
  `CreateInstanceU()` and does **not** test the result for NULL (disassembly `0x102fbe2c4`–`0x102fbe348`).
  It wraps the handle with the `CalcA` and `SetParameterA` pointers and calls `SetSampleRateU(handle, rate)`
  with the current rate; the wrapper's initial rate is 44,100.
- `SetSampleRateU`, `SetParameterA` and `ResetA` are called through `0x102fbe580`, `0x102fbec58` and
  `0x102fbe650`. Each sets the FPCR flush-to-zero bit for the call and restores the floating-point
  environment afterwards.
- A load-status message `AThirdPartyDeviceModule.LoadPluginStatus(DeviceModuleId, Status)` is handled by
  `0x103198c80`. When the status is false, the handler builds a notice from the localized key
  `AThirdPartyDeviceModule` / `sErrorTextPluginLoadFailed` (`0x10319bd08`).

**Inferred.** `<dir>` is the application resources directory. A missing bundle leaves the device
without an engine instance, and the user sees the `sErrorTextPluginLoadFailed` text. The sender of the
status message, the text itself and the device's state after failure were not traced.

## How Live uses `GetPlugInfoU`

Observed (`0x102fbe49c`, loader defaults in `0x102fbe07c`). Live queries selectors 1, 2, 3 and 5 with
size 8, then 4 and 6 with size 4. It keeps an answer only when the call returns non-zero; otherwise the
default stays.

| Selector | Loader field (default) | Live use | Bundle answers (H4) |
| --- | --- | --- | --- |
| 1 | +0x70 (1) | No reader found | 1 for all |
| 2 | +0x78 (1) | No reader found | 1 for all |
| 3 | +0x80 (0) | Must be non-zero before an instance is created. A value of 2 makes the warm-up (`0x102fbff98`) clear the input buffers first | Effects 2, instruments 1 |
| 4 | +0x84 (0; stored as non-zero → 1) | Non-zero creates a second engine instance (`0x102fbf644`). Parameter values go to both instances (`0x102fbfe54`) | Amp, Cabinet 1; others 0 |
| 5 | +0x88 (1,024) | Read through the instance virtual `0x102fcc390`. The warm-up processes 1,024 frames in blocks of at most this size | Amp, Cabinet 32,767; others 512 |
| 6 | +0x90 (1) | Enables the reset sequence in `0x102fbf220`: warm-up calls, then `ResetA`, then the latest index-0 value is sent again. It also enables batched parameter flushing when more than 10 values are pending (`0x102fbf19c`, `0x102fbf340`) | Amp, Cabinet 0; others 1 |

Inferred: selector 4 means "mono engine, run one per channel" (dual mono), which matches the H4
hypothesis. The roles of selectors 1 and 2 on the Live side are unknown.

## From a stored parameter to `SetParameterA`

**Observed structure.**

- Every device class has a virtual at slot +0x5a0 that returns a vector of 0x38-byte entries. Builders:
  Amp `0x1030b5220`, Cabinet `0x1030ca45c`, Electric `0x1030ebe78`, Corpus `0x1030e54e8`. Dossiers place
  these at vtable 0x1068c2718 (Cabinet), 0x1068c3d80 (Corpus) and 0x1068c4bb8 (Electric), each + 0x5a0.
  The nested builders for Collision (`0x1030debd0`), Tension (`0x103193b1c`) and Analog (`0x1031ad110`)
  were not extracted.
- `0x10319cb10` walks the vector. **The entry's position is the `SetParameterA` index**, and an empty
  entry still uses up an index. For each entry it creates:
  - a parameter unit;
  - an `AConvertQuantingInt` stage, but only when the parameter's user converter is an
    `ALegacyQuantingIntUserFloatConverter` (`0x10319c95c`; cast target typeinfo `0x106680fb8`);
  - a mapping module chosen by the entry's mode.
- Each module emits `{index, value}` to `OThirdPartyDeviceProcessor::OnParameter` (`0x102fccd28`).
  `OnParameter` ignores indices above 255 and keeps the latest value per index. The flush `0x102fbfe54`
  then calls `SetParameterA(handle, index, value)`.

Mapping modes, with the module and what it emits (Observed in the processor `OnValue` functions):

| Mode | Module | Emits |
| --- | --- | --- |
| 0 | `AIndexedFloatModule` | v unchanged |
| 1 | `AAasModulationPolarizerModule` | \|v\|, and a sign flag on a second output |
| 2 | `AAasToggleMappingModule` | v + 1 when the toggle is above 0.5, else 0 |
| 3 | `AAasFilterTypeModule` | int(v) >> 1, and int(v) & 1 |
| 4 | `AAasBoolInverterModule` | 1 if v ≤ 0.5, else 0 |
| 5 | `AAasToToggleMappingModule` | max(v − 1, 0), and v > 0.5 |
| 6 | `AAasMultiplyOffsetModule` | offset + multiplier · v |
| 7 | `AThirdPartyIntegerMappingModule` | float(table[int v]), with no bounds check |
| 8 | `ACollisionScaledModeModule` | v × 0.125 when the mode is 4 or 9, else v |

**Value model** (Observed in the constructors and converter code; dossiers n5-0002 to n5-0004):

- A float parameter is initialized by `0x1026f0bcc(p1, p2, default, …, userConverter, …)`. It sets the
  internal range [p1, p2]. The default is stored as both the current value and `mpManual` (member names
  from `0x1026f0390`).
- The user converter maps the stored (user) value to internal:
  - `ALinearUserFloatConverter(c0, c1)`: linear from [c0, c1] to [p1, p2], then clamp (`0x1015758bc`);
  - `ALog10UserFloatConverter(c0, c1)`: log10(u/c0)/log10(c1/c0), then clamp. u ≤ 0 or NaN gives p1
    (`0x1015763e0`);
  - `AQuantizingUserFloatConverter`: clamp only;
  - `ALegacyQuantingIntUserFloatConverter`: linear, then clamp.
- `MidiControllerRange` Min and Max are set from p1 and p2 through the inverse mapping (`0x1025856a0`).
  That is why the stored range equals the user domain [c0, c1].
- `ConvertQuantingInt` (`0x101bb9f34`) maps internal to user, rounds to the nearest 1/32768 (`frinta`),
  then truncates toward zero (`fcvtzs`).

**Inferred, strongly supported:** the stored document value is the user value, and the value passed to
`SetParameterA` is the internal value. Three independent checks agree:

- Amp stores Bass as 0..10 with internal range 0..1, and the Softube engine clamps every parameter to
  [0, 1].
- The Electric bundle declares exactly the internal ranges 0..30, 0..24 and 0..48.
- The Corpus bundle's setter converts Live's internal domains −48..48, −50..50, 0..360, 0.5..9 and −1..1
  explicitly (next section).

The unit that turns the current value into the emitted value was not traced end to end.

## Mapping tables

All 82 rows are in `out/conversions.tsv`. For every row, the domain in Live's constructor equals the
stored modal range found in shipped content (asserted).

### Electric (`LoungeLizard`): complete, 33 indices

All 33 entries use mode 0. Indices 0–29 follow the schema order of the stored names, skipping
`PerNotePitchBendRange`, `KeyboardTranspose` and `KeyboardStretch`; index 23 is `PickupModel`. Index 30
is `KeyboardTranspose`, 31 is `KeyboardStretch`, and 32 is the unstored `DummyPerNotePitchBendRange`.

| Index | Stored parameter | Stored domain | Constructor default | Value passed |
| --- | --- | --- | --- | --- |
| 0 | `Polyphony` | enum 0..30, labels "2"…"32" (`Voices`) | 30 | index |
| 1 | `PitchBendRange` | 0..1 | 1 | identity, clamp |
| 2 | `Volume` | 0..1 | 0.7047892 | identity, clamp |
| 3 | `KeyboardFineTune` (`Detune`) | 0..1 | 0.5 | identity, clamp |
| 4–22 | `MalletStiffness` … `PickupDistance`, in schema order | 0..1 | 0.5 | identity, clamp |
| 23 | `PickupModel` | enum 0..1, labels R, W | 0 | index |
| 24–29 | `PickupAmpIn`, `PickupAmpOut`, `PickupAmpKeyboardScaling`, `DamperTone`, `DamperAmount`, `DamperBalance` | 0..1 | 0.5 | identity, clamp |
| 30 | `KeyboardTranspose` (`Semitone`, displayed with −12 st offset) | 0..24 | 12 | clamp, round to 1/32768, truncate |
| 31 | `KeyboardStretch` | 0..1 | 0.5 | identity, clamp |
| 32 | (none; runtime `DummyPerNotePitchBendRange`) | 0..48 | 48 | clamp |
| — | `PerNotePitchBendRange` | 0..48 | 0 | not passed to the bundle |

Cross-check: 33 Live entries and 33 bundle entries. The three non-unit bundle ranges sit at indices 0,
30 and 32, as above. The bundle's only integer-kind entry, index 23, is the enumeration `PickupModel`.
The constructor defaults equal the `Defaults/Instruments/Electric.adv` values, except `PickupAmpIn` and
`PickupAmpOut` (code 0.5, preset 0.42).

### Corpus: complete, 38 indices

Bundle rule (Observed, helper corpus). The constructor `0xc40c` installs the vtable `0x2cb88`
(`CorpusWrapper`, deriving from `WrapperTemplate<CorpusSynth,37>`). `_SetParameterA` dispatches to slot 0,
`0xd75c`, which accepts indices up to 37 and special-cases 18 of them. Other indices go to the base
setter `0x50c0`, which accepts only indices below 37. The base setter has two rules:

- **I** (integer kind 3): int(min(v, max)).
- **U** (other kinds): min(v, 1), then 128v when the result is ≤ 0.5, else 126v + 1.

The bundle passes the resulting 0..127 value, or the integer, to the engine.

| Index | Stored parameter | Stored domain (labels) | Default | Live conversion (value passed) | Bundle rule |
| --- | --- | --- | --- | --- | --- |
| 0 | `ResonanceType` | 0..6 (Beam, Marimba, String, Membrane, Plate, Pipe, Tube) | 0 | index | int table [1,2,3,4,5,7,6][int v] if int v < 7, else 0 |
| 1 | `Decay` | 0..1 | 0.5 | identity, clamp | U |
| 2 | `FreqDamping` (`Material`) | −1..1 | 0 | identity, clamp | v < 0 ? 63.5v + 63.5 : 63v + 64 |
| 3 | `Inharmonics` | −1..1 | 0 | identity, clamp | as 2 |
| 4 | `Ratio` | 0..1 | 0.5 | identity, clamp | U |
| 5 | `Radius` | 0..1 | 0.5 | identity, clamp | 1 − v ≤ 0.5 ? 127(1 − v) : 127 − 126v |
| 6 | `Frequency` (`Tune`) | 0..1 | 0.5 | identity, clamp | U |
| 7 | `Transpose` | −48..48 | 0 | clamp, round to 1/32768, truncate | int(int v + 48) |
| 8 | `FineTranspose` | −50..50 | 0 | clamp, round to 1/32768, truncate | 63.5 + 1.27v |
| 9 | `Detune` (`Spread`) | −1..1 | 0 | identity, clamp | as 2 |
| 10 | `PitchBendRange` | 0..24 | 5 | clamp, round to 1/32768, truncate | I (max 24) |
| 11 | `AmpFreq` (`Brightness`) | −1..1 | 0 | identity, clamp | as 2 |
| 12 | `MidiPitch` (`MIDI Frequency`) | bool | false | 0 or 1 | U |
| 13 | `MidiGate` (`Note Off`) | bool | false | 0 or 1 | U |
| 14 | `ExcitationX` (`Hit`) | 0..1 | 0.5 | identity, clamp | 64 + 31.5v |
| 15 | `ListeningXL` | 0..1 | 0.1 | identity, clamp | 64 + 31.5v |
| 16 | `ListeningXR` | 0..1 | 0.9 | identity, clamp | 64 + 31.5v |
| 17 | `LfoOnOff` | bool | false | 0 or 1 | I (max 1) |
| 18 | `LfoType` | 0..6 (Sine, Square, Triangle, SawUp, SawDown, Sample & Hold, Random Ramp) | 0 | index | I (max 6) |
| 19 | `LfoSync` | 0..1 (Free, Sync) | 0 | index | U |
| 20 | `LfoRate` | 0..1 | 0.5 | identity, clamp | U |
| 21 | `LfoSyncRate` | 0..21 (22 rates) | 4 | clamp, round to 1/32768, truncate | I (max 21) |
| 22 | `LfoStereoMode` | 0..1 (Phase, Spin) | 0 | index | integer: v ≠ 0 → 0, else 1 |
| 23 | `LfoSpin` | 0..0.5 | 0 | identity, clamp | v ≤ 0.5 ? 127v : 126v + 1 |
| 24 | `LfoPhase` | 0..360 | 180 | identity, clamp | v < 180 ? 0.35277778v : 0.35v + 1 |
| 25 | `LfoOffset` | 0..360 | 0 | identity, clamp | as 24 |
| 26 | `LfoAmount` | 0..1 | 0 | identity, clamp | U |
| 27 | `FilterOn` | bool | false | 0 or 1 | I (max 1) |
| 28 | `FilterMidFreq` | 50..18000 Hz | 1000 | log10(s/50)/log10(360), clamped to 0..1 (1000 Hz → 0.50895) | U |
| 29 | `FilterBandWidth` | 0.5..9 | 4 | identity, clamp | 14.941176v − 7.470588 |
| 30 | `Drive` (`Gain`) | 0..1 | 0.5 | identity, clamp | U |
| 31 | `StereoWidth` (`Width`) | 0..1 | 1 | identity, clamp | U |
| 32 | `DryWet` | 0..1 | 0.5 | identity, clamp | U |
| 33 | `ResonatorQuality` | 0..3 (Eco, Low, Med, High) | 2 | index | I (max 3) |
| 34 | `DecayOnNoteOff` (`Note Off Decay`) | 0..1 | 0 | identity, clamp, then 1 − v (mode 6; multiplier −1, offset 1) | U |
| 35 | `TubeOpening` (`Opening`) | 0..1 | 1 | identity, clamp | U |
| 36 | `Bleed` | 0..1 | 0 | identity, clamp | U |
| 37 | `MidiMode` | 0..1 (Last, Low) | 0 | index | not forwarded (the base setter accepts only indices below 37) |

Cross-checks (Observed):

- The seven integer-kind bundle entries (0, 10, 17, 18, 21, 27, 33) fall exactly on Live's enum, bool
  and integer parameters.
- Every special case in `0xd75c` matches the internal domain of the parameter Live places at that index.
- The −1..1 rules sit on the four bipolar parameters; +48 is applied at `Transpose`; ±50 → 0..127 at
  `FineTranspose`; degrees at `LfoPhase`/`LfoOffset`; 0.5..9 at `FilterBandWidth`.

Inferred: Live itself handles MIDI mode. `ACorpusUnit` (`0x1031a0358`) wires a `MonophoneMode` module,
and the engine never receives index 37.

Reported by another session and confirmed here: indices 14–16 map as 64 + 31.5v. Reported and **not**
verified: "index 6 is a fixed pitch, linear −4..4 octaves around 261.62 Hz; the stored `Frequency` does
not reach the resonator directly". Live does pass the stored `Frequency` (identity) at index 6, through
the base U rule. The constant 261.62 occurs in the engine function `0x23670`, whose connection to index 6
was not traced.

### Corpus cross-check with the bundle-side trace

[Corpus DSP (static)](corpus-dsp-static.md#host-parameters) maps each host index to an engine target. It
inferred the Live name for each index from what the target does. This packet derives the same 37
index → name pairs (0–36) from Live's own vector and member registration. That confirms its inferred
names, including `FreqDamping` (display `Material`), `Drive` (`Gain`) and `Bleed`.

One correction. Live does call index 37 (`MidiMode`). The wrapper `0xd75c` stores the value; the base
setter `0x50c0` then rejects the index. So "never sent" should read "sent but ignored".

`out/corpus_priority.tsv` chains three pieces for the six priority parameters:

- Live's conversion (this page);
- the wrapper rule (read here);
- the engine driver from [`report-chain.md`](../../analysis/ableton-live-12.4.3/r2/corpus-dsp-v1/report-chain.md)
  and [`report-resonator.md`](../../analysis/ableton-live-12.4.3/r2/corpus-dsp-v1/report-resonator.md),
  which are another session's evidence and were not re-verified.

All values are static derivations.

| Stored parameter → index | Live conversion (Observed constructor; vector mode 0 confirmed in disassembly n5-0002) | Wrapper → controller *c* | Engine (other session) | Derived examples |
| --- | --- | --- | --- | --- |
| `Frequency` → 6 | identity, clamp 0..1 (`FUN_103197830`: s0 = 0, s1 = 1.0, read from instruction bytes at `0x1031978cc`–`0x1031978e8`) | U | Modulator fixed pitch −4…+4 octaves around 261.62 Hz, float | 0 → 16.35 Hz; 0.5 → 261.62 Hz; 1 → 4186 Hz |
| `Radius` → 5 | identity, clamp 0..1 | inverted: v ≥ 0.5 ? 127(1 − v) : 127 − 126v | tube radius 0.005·80^(trunc *c*/127) | 0 → 0.4; 0.5 → 0.044; 1 → 0.005 |
| `ExcitationX` → 14 | identity, clamp 0..1 | 64 + 31.5v | exci_x 0.05…0.95 linear, truncated *c* | 0 → 0.5; 1 → 0.72 |
| `ListeningXL` → 15, `ListeningXR` → 16 | identity, clamp 0..1 | 64 + 31.5v | list x 0.01…0.99 linear, truncated *c*; the right instance swaps L and R | defaults 0.1 → 0.527, 0.9 → 0.720 |
| `FilterMidFreq` → 28 | log10(s/50)/log10(360), clamped to 0..1 (`ALog10UserFloatConverter`) | U | 50·360^(*c*/127) Hz; float assumed | 50 → 50; 1000 → ≈1023; 18000 → 18000 |

`Frequency`, `Radius` and `FilterMidFreq` agree with the bundle-side reading:

- `Frequency` 0.5 gives 261.62 Hz, which matches that page's self-test.
- `Radius` is inverted, as its CD-C07 says.
- `FilterMidFreq` arrives normalized, as that page required. The asymmetric U rule moves 1000 Hz to
  about 1023 Hz.

**Contradiction (open): the three position parameters.** Live's side was checked:

- The internal range is 0..1 (instruction bytes).
- The vector mode is 0, with no remapping module (disassembly).
- No user converter rescales the value.

On that chain, `ExcitationX`, `ListeningXL` and `ListeningXR` reach only controller 64…95.5. That is
the half of the engine range from the centre to about 0.72. The wrapper's `64 + 31.5v` fits a bipolar
−1…1 input, and the other session's port assumes Live maps 0..1 to −1..1. **The Live-side evidence
stops at the float parameter unit** (`AFloatParameterUnit`, created by `0x10319c4dc`), whose emitted
value was inferred rather than traced.

A blanket bipolar rescale in that unit would contradict Amp and Electric:

- Amp: the Softube engine clamps to [0, 1].
- Electric: the bundle declares ranges 0..24 and 0..48.

A rescale specific to these parameters was not found. P4-N5-01 settles it: log the value passed at
index 14 for stored `ExcitationX` 0 and 1, expecting 0/1 on this chain or −1/1 on the port's
assumption.

### Amp: complete, 7 indices; Cabinet: complete, 3 indices

| Device | Index | Stored parameter | Domain (labels) | Default | Value passed |
| --- | --- | --- | --- | --- | --- |
| Amp | 0 | `AmpType` | 0..6 (Clean, Boost, Blues, Rock, Lead, Heavy, Bass) | 2 | table [4,5,0,1,2,3,6][index] (mode 7) |
| Amp | 1–6 | `Bass`, `Middle`, `Treble`, `Presence`, `Gain` (`Input Gain`), `Volume` | 0..10 | 5, 5, 5, 5, 5, 9 | stored/10, clamped to 0..1 |
| Amp | — | `DualMono` | bool | false | not passed to the bundle |
| Amp | — | `DryWet` | 0..1 | 1 | not passed to the bundle |
| Cabinet | 0 | `CabinetType` | 0..4 (1x12, 2x12, 4x12, 4x10, 4x10 Bass) | 0 | index |
| Cabinet | 1 | `MicrophoneTypeSwitch` | bool (Dynamic, Condenser) | false | 0 or 1 |
| Cabinet | 2 | `MicrophonePosition` | 0..2 (Near On-Axis, Near Off-Axis, Far) | 0 | index |
| Cabinet | — | `DualMono`, `DryWet` | bool; 0..1 | false; 1 | not passed to the bundle |

Cross-check: the bundle side (H4) does the following.

- Index 0 selects a model by (uint)(v + 0.5).
- Index n ≥ 1 sets engine parameter n − 1.
- Cabinet maps index 2 to int(v) × 0.5.

The Live order matches this. The processor has `OnDualMono` and `OnDryWet` handlers (`0x102fccddc`,
`0x102fccdf4`); what feeds them was not traced. The Softube model order is unknown, so the model behind
each `AmpType` label is unknown. Live's table entry is known for each.

## Load handling and defaults

- **Out-of-range stored values.** Observed in the converters: the value passed to the bundle is clamped
  into the internal range. NaN passes through the linear clamp, but not the log10 converter. Unknown:
  whether the stored value is clamped, rejected or kept on load and then re-saved. The document reader
  was not traced.
- **Enumerations.** No clamp was traced on the Live side. The Amp table lookup has no bounds check
  (`0x102faadb8`). The Corpus bundle guards `ResonanceType` (< 7, else engine type 0).
- **Missing parameters.** Observed: the constructor defaults in the tables above, including Amp
  (`AmpType` Blues, tone controls 5, `Volume` 9, `DualMono` off, `DryWet` 1), Cabinet (1x12, Dynamic,
  Near On-Axis, `DualMono` off, `DryWet` 1) and Corpus. Inferred: an element absent from a document
  keeps the constructor default. Whether `Defaults/<Product>.adv` is applied to new instances is unknown.

## Candidate requirements for per-device parameter storage specs

Proposed. These cover stored representation, domains, defaults and load handling, in observable terms.
Index tables and module names are internal structure. They stay in this analyst page and do not belong
in a handoff.

| Candidate | Statement | Evidence | Strength |
| --- | --- | --- | --- |
| DEV-M01 | Stored values of the seven devices' float parameters are in the user domain listed per parameter. For Amp, Cabinet, Electric and Corpus those domains are the 82 rows of `out/conversions.tsv` | Constructor arguments equal the shipped modal ranges in 82 of 82 rows | Observed |
| DEV-M02 | Amp `Bass`…`Volume` are stored on 0..10 and act as one tenth of that on a 0..1 control. Corpus `FilterMidFreq` is stored in Hz (50..18000) on a logarithmic control; `LfoPhase`/`LfoOffset` in degrees; `Transpose`/`FineTranspose` in semitones/cents as integers | Converters and constructor arguments | Observed representation; effect on sound out of scope |
| DEV-M03 | Integer-stepped float parameters (Electric `KeyboardTranspose`; Corpus `Transpose`, `FineTranspose`, `PitchBendRange`, `LfoSyncRate`) take effect as the stored value rounded to the nearest 1/32768, then truncated toward zero: stored −3.7 acts as −3, and 11.99999 as 12 | `0x101bb9f34` disassembly | Observed arithmetic; the chain into it is Inferred |
| DEV-M04 | New instances without a preset start from the constructor defaults listed above (Amp, Cabinet, Corpus, Electric) | Constructor arguments | Observed values; use when the Defaults preset is absent is Inferred; P4-N5-03 |
| DEV-M05 | Enumeration labels are as listed: Amp, Cabinet, Electric `Polyphony` 2…32 voices and `PickupModel` R/W, and the Corpus enumerations | Label lists in the constructors | Observed strings; localization unknown |
| DEV-M06 | A stored value outside its domain does not drive the device outside the domain: processing uses the value clamped to the domain | Converter clamps | Inferred; P4-H4-02 and P4-N5-01 |
| DEV-M07 | Electric `PerNotePitchBendRange` is stored but does not reach the engine. The engine always receives 48 semitones through a runtime-only parameter | Electric vector and constructor | Observed structure; per-note bend scaling in Live is Inferred |
| DEV-M08 | Amp and Cabinet `DualMono` and `DryWet` are host features. Live runs two engine instances for these mono engines | Selector 4 path, parameter vectors, processor handlers | Observed structure; feeding of `DryWet`/`DualMono` is Inferred |
| DEV-M09 | Corpus `DecayOnNoteOff` acts inverted (1 − v), and Corpus `MidiMode` is not handled by the engine | Vector entry mode 6; bundle index bound | Observed |
| DEV-M10 | When a device's engine cannot be loaded, Live posts a load-failure notice (`sErrorTextPluginLoadFailed`) | `0x103198c80` | Inferred; the text and the device state are unknown |

## Unknowns

- Analog, Tension and Collision index tables (nested builders using modes 1–5 and 8).
- The document reader: clamping, rejection or keeping of out-of-range and malformed values, and
  behavior for missing or extra elements.
- Whether `Defaults/<Product>.adv` is read when a device is created.
- The Live-side roles of `GetPlugInfoU` selectors 1 and 2, the `CalcA` arguments `a5`–`a7`, and the use
  of `flagOut`.
- What feeds `OnDualMono` and `OnDryWet`. The sender and text of the load-failure notice.
- The Softube model order behind Amp's model table.
- The Corpus engine's meaning of index 6, and of the other 0..127 values.

## Phase 4 probe records

Per [ADR 0002](../decisions/adr-0002-static-first-analysis.md). Run on the macOS reference host, batched
with P4-H4-01 to 05. Inputs are copies. Tool availability, including a debugger able to attach to
Live, must be established first.

| Probe | Question | Static evidence so far | Minimal input | Discriminating observation | Stop when |
| --- | --- | --- | --- | --- | --- |
| P4-N5-01 SetParameterA trace | Is the passed value the internal value, with the index order above? Do the Corpus positions arrive as 0..1 or −1..1? | Tables above; value chain Inferred; open position contradiction | Breakpoint or trace on each bundle's `_SetParameterA` (Amp `0x3490`, Electric `0xc2b8`, Corpus `0x4f40` arm64); load one shipped preset per device, plus Corpus copies with `ExcitationX` 0 and 1 | Logged (index, value): Amp `Bass` 5 → (1, 0.5); Electric `KeyboardTranspose` 12 → (30, 12); Corpus `FilterMidFreq` 1000 → (28, ≈0.509); Corpus `ExcitationX` 0/1 → (14, 0/1) on this chain or (14, −1/1); index 37 arrives and is ignored | Three values per device match, or any mismatch is recorded |
| P4-N5-02 Instance count | Do Amp and Cabinet create two engine instances, and the others one? | Selector 4 path | Breakpoint on `_CreateInstanceU`; insert each device once | Hit count per insert | All seven counted |
| P4-N5-03 Defaults source | Does a fresh Electric take `PickupAmpIn` 0.42 (Defaults preset) or 0.5 (constructor)? | Code 0.5 vs preset 0.42 | Empty set; insert Electric; save | Saved `PickupAmpIn` | One save inspected; refines P4-H4-03 |
| P4-N5-04 Missing bundle | What does the user see when a bundle is absent? | `sErrorTextPluginLoadFailed` path | Only if a disposable application copy with a removed `Corpus.bundle` can be run without breaking code signing; otherwise skip | Notice text; device state; save output | Observed once or recorded as infeasible |

## Limitations

- Derived from decompiler text, checked against disassembly only where the dossiers cite it. The four
  rounds are listed in `notes.md`.
- `extract_mapping.py` parses decompiled text with regular expressions, and handles only flat builders.
- The bundle-side Corpus semantics end at the 0..127 value passed to the engine.
- No organization is attributed to any binary.
