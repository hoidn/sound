---
id: RESEARCH-DEVICE-BUNDLES-STATIC
type: research
status: draft
updated: 2026-10-17
access: analysis
target: Ableton Live 12 Suite 12.4.3
---

# Native device bundles: interface and parameters (static)

Packet H4 of [roadmap revision 2](native-decompilation-roadmap.md#revision-2-proposal--2026-10-17),
for FEAT-DEVICES. Bounded question: what is the boundary between Live and the seven
bundles under `Contents/App-Resources/Devices/Mac/`, and which parameters does each
device expose? This is static evidence only. Nothing was executed, and Live cannot run
on this host. Signal processing is out of scope; a static call edge, string or
pseudocode line is not proof of runtime behavior.

## Evidence

Retained run: [h4-devices-v1](../../analysis/ableton-live-12.4.3/r2/h4-devices-v1/manifest.json)
(Python 3.13.9 standard library, `python3 -I`; the manifest lists every command and the
SHA-256 of every script and output). `python3 -I checks.py out <Devices/Mac>` re-derives
16 claims from this page into `out/checks.txt`; all pass. Sources:

- Source [SRC-ABLETON-12-4-3](sources/ableton-live-12.4.3.md): the local bundle
  `/home/ollie/Ableton Live 12 Suite.app` (`Contents/Info.plist` SHA-256 `9b804aa1…ffda29b6d`).
  The seven bundle directories, schema `Schema/12.0_12402.txt` and all 203 schema files,
  and 3,634 gzip documents (2,187 `.adv`, 1,071 `.adg`, 350 `.alc`, 26 `.als`) under
  `Core Library/` and `Builtin/`. Path, size and SHA-256 of every scanned document are
  in `out/inputs.jsonl`.
- Each bundle's arm64 slice in its own Ghidra 12.1.4 project, with the complete C1
  corpus (every eligible function exported; 0 failed, 0 pending, verified with
  `tools/r2_corpus.py`) and C2 indexes, under `/var/tmp/sound-analysis/helpers/<slug>/`.
  The functions cited below are copied unchanged into `out/entry_points.jsonl`.
- Byte-level string presence in `analysis/ableton-live-12.4.3/derived/Live.arm64`
  (SHA-256 `3a99ceea…d1c383cfad`). The Live Ghidra project was not opened.

| Output | Content |
| --- | --- |
| `out/bundles.json`, `out/bundle_strings.jsonl` | Info.plist, CodeResources, every slice's load commands, export trie, symbol table, imports and code-signature identity; every arm64 `__cstring` string with vmaddr |
| `out/schema_devices.json` | Shared device envelope, flattened device fields of `12.0_12402`, field history across 203 schemas |
| `out/occurrences.jsonl`, `out/params.json`, `out/fields.json`, `out/envelopes.json`, `out/scan.json` | One row per device occurrence; per-parameter value distributions; non-parameter fields; envelope matching; scan totals |
| `out/param_table.tsv`, `out/param_summary.json` | One row per device parameter: class, kinds, observed min/max, modal stored range, mapping and target counts, shipped default |
| `out/param_tables.json` | Bundle-side parameter index tables recovered from pseudocode, each row with its source line, and a range comparison with the documents |
| `out/entry_points.jsonl`, `out/entry_compare.json` | Cited pseudocode records; normalized-hash families of the seven entry points |
| `out/live_strings.json` | Interface anchors and every parameter name in the Live image (C string and UTF-16LE counts) |
| `out/corpus_resonance.json` | Shipped documents for each Corpus `ResonanceType` value; the Live string run around `Beam` |

Addresses in bundles are arm64-slice vmaddrs (image base 0, as Ghidra shows them).
Addresses in Live are unslid vmaddrs of `Live.arm64`; thin-file offsets are in
`out/live_strings.json`.

## Identity

Observed (`out/bundles.json`). Every executable is universal x86_64 + arm64, built for
macOS 11.0. Each executable's SHA-256 equals its `hash2` entry in the application's
`Contents/_CodeSignature/CodeResources`. The seven inner `_CodeSignature/CodeResources`
files are byte-identical and list no files.

| Bundle | Info.plist identity | Executable (SHA-256) | arm64 slice (offset, bytes, SHA-256) | Mach-O type; dylibs | Signature identifier; team; CD flags |
| --- | --- | --- | --- | --- | --- |
| `Amp.bundle` | `com.softube.Amplifier` 1.2.3; GetInfo "(c) 2021 Softube" | `Amplifier` `ffc0ead3…fde8bb` | 1,982,464; 1,738,608; `74bfecc8…9ca751` | `MH_DYLIB`, install name `build/arm64/Amp_unstripped.dylib`; 12 incl. Cocoa, Security, libz | `com.softube.Amplifier`; `MWR434WD94`; `0x0` |
| `Cabinet.bundle` | `com.softube.Cabinet` 1.2.3; same GetInfo | `Cabinet` `5b886e31…a09b61` | 2,555,904; 1,841,728; `04813553…4d9447` | `MH_DYLIB`, `build/arm64/Cab_unstripped.dylib`; same 12 | `com.softube.Cabinet`; `MWR434WD94`; `0x0` |
| `Analog.bundle` | `com.ableton.analog` 1.0 | `Analog` `dddb93e7…8c3d4b` | 524,288; 432,640; `211bd67c…2f09ab` | `MH_BUNDLE`; libc++, libSystem | `com.ableton.analog`; `5R73KCYJ3T`; `0x10000` |
| `Tension.bundle` | `com.ableton.tension` 1.0 | `Tension` `db7eb728…077c6f` | 524,288; 449,696; `640700be…b424be` | `MH_BUNDLE`; libc++, libSystem | `com.ableton.tension`; `5R73KCYJ3T`; `0x10000` |
| `Collision.bundle` | `com.ableton.collision` 1.0 | `Collision` `797e903c…50fcbd` | 393,216; 332,496; `2bc497cd…f105f7` | `MH_BUNDLE`; libc++, libSystem | `com.ableton.collision`; `5R73KCYJ3T`; `0x10000` |
| `Electric.bundle` | `com.ableton.electric` 1.0 | `Electric` `bb0d404b…85ef95` | 294,912; 265,920; `fcf490a0…6de8db` | `MH_BUNDLE`; libc++, libSystem | `com.ableton.electric`; `5R73KCYJ3T`; `0x10000` |
| `Corpus.bundle` | `com.ableton.corpus` 1.0 | `Corpus` `2164ec08…3ef422` | 278,528; 248,624; `29df4582…ad9fe8` | `MH_BUNDLE`; libc++, libSystem | `com.ableton.corpus`; `5R73KCYJ3T`; `0x10000` |

`MWR434WD94` is also the team that the [Push 3 helper page](push3-helper-static.md#identity)
records for `com.ableton.Push3`. This page does not attribute either team ID to an organization.

**Document element for each bundle.** Observed: the shipped default presets
`Core Library/Defaults/Instruments/{Analog,Collision,Tension,Electric}.adv` have the root
children `UltraAnalog`, `Collision`, `StringStudio` and `LoungeLizard`. Every `.adv` under
`Core Library/Devices/Audio Effects/{Amp,Cabinet,Corpus}/` has the root child `Amp`,
`Cabinet` or `Corpus`. Each of the seven element names occurs exactly once as a C string
in Live (`UltraAnalog` `0x105b9ac34`, `LoungeLizard` `0x105b9ac22`, `Collision`
`0x105b9ac40`, `Corpus` `0x105b9ac4a`, `StringStudio` `0x105b6c516`, `Amp` `0x105beb70c`,
`Cabinet` `0x105beb744`). Inferred: the mapping from element to bundle follows the
product names. No code reference has been traced yet.

## The interface Live calls

**Observed: one shared C interface.** Every slice of all seven executables exports the
same seven C symbols. In the five `com.ableton.*` arm64 slices these are the only
exports. The Softube arm64 dylibs export 1,243 (Amp) and 1,123 (Cabinet) symbols in
total, mostly C++. Live's image
holds each name exactly once, as adjacent `__TEXT,__cstring` strings (`GetPlugInfoU`
`0x105bdd69e`, `CreateInstanceU` `0x105bdd6ab`, `DestroyInstanceU` `0x105bdd6bb`,
`SetSampleRateU` `0x105bdd6cc`, `CalcA` `0x105bdd6db`, `SetParameterA` `0x105bdd6e1`,
`ResetA` `0x105bdd6ef`). Live does not contain `Amp.bundle` or the other bundle file
names, but it does contain `Devices` (`0x105be6880`), `Mac` (`0x105be6878`) and `.bundle`
(`0x105c8c4a0`). Inferred, not established: Live builds the bundle path at run time and
resolves the seven entry points by name.

Entry addresses (arm64):

| Bundle | CreateInstanceU | DestroyInstanceU | SetSampleRateU | GetPlugInfoU | CalcA | SetParameterA | ResetA |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Amp | `0x3100` | `0x32a0` | `0x3340` | `0x337c` | `0x340c` | `0x3490` | `0x35ac` |
| Cabinet | `0x2c84` | `0x2e24` | `0x2ec4` | `0x2f00` | `0x2f90` | `0x3014` | `0x317c` |
| Analog | `0x17044` | `0x170e8` | `0x17160` | `0x171f8` | `0x172c4` | `0x1760c` | `0x176a4` |
| Tension | `0x12fc8` | `0x1306c` | `0x130e4` | `0x1317c` | `0x13248` | `0x13590` | `0x13628` |
| Collision | `0x12454` | `0x124f8` | `0x12570` | `0x12608` | `0x126d4` | `0x12a1c` | `0x12ab4` |
| Electric | `0xbcf0` | `0xbd94` | `0xbe0c` | `0xbea4` | `0xbf70` | `0xc2b8` | `0xc350` |
| Corpus | `0x46e4` | `0x4798` | `0x47b4` | `0x4c20` | `0x4cb8` | `0x4f40` | `0x4f54` |

**Three implementations behind one interface.** Observed (`out/entry_compare.json`):
the pseudocode of each entry point, with addresses and generated names masked, falls
into three groups:

- Softube: Amp and Cabinet. They differ only in `SetParameterA`.
- TassmanSynthWrapper family: Analog, Tension, Collision and Electric are identical in all
  seven entry points. The family is named after the string `TassmanSynthWrapper::…`
  (Analog `0x5620f`).
- Corpus: a separate wrapper.

Statically derived roles. These are labeled inferences from pseudocode. Argument roles
come from use, not from symbols.

| Entry | Observed in pseudocode | Inferred role |
| --- | --- | --- |
| `CreateInstanceU()` | Returns a heap object. **Softube:** returns NULL unless `CFBundleGetIdentifier(CFBundleGetMainBundle())` equals `com.ableton.live` (CFString data `0x160508` → `0x159468` in Amp); registers the instance in a global list. **TassmanSynthWrapper:** queries the new object with selector `0x15` and, on failure, prints `Error creating device: Ableton devices must implement kCanStopProcessing.` (Analog `0x55e68`) and returns NULL. **Corpus:** sets the C locale while it constructs | Instance factory. The Softube binaries refuse any host but Live |
| `DestroyInstanceU(inst)` | Frees the instance; NULL is ignored or logged | Instance teardown |
| `SetSampleRateU(inst, rate)` | TassmanSynthWrapper: the integer rate is converted to `float` and passed to vtable `+0x50`. Corpus: stores `rate / 10` as a sample counter and reinitializes. Softube: vtable `+0x10`, `+0x20` | Sample-rate change; integer Hz |
| `GetPlugInfoU(selector, out, size)` | A switch on selectors 1–6, each guarded by `size` 8 or 4; any other selector returns 0 (table below) | Static capability query |
| `CalcA(inst, frames, outL, outR, a5, a6, a7, flagOut)` | TassmanSynthWrapper passes `a5`/`a6` and a local buffer (initialized with capacity `0x400`) to a helper, reads three fields of `a7`, and processes in place: input pointers are the output pointers unless selector 3 is 1. It writes `*flagOut = (query(0x14) == 0)`. Softube writes `*flagOut = engine->vtbl[0x1c0]() ^ 1`. Corpus counts down `rate / 10` samples whose magnitude is at most `1e-5` before clearing `*flagOut` | Audio/event block process. `flagOut` reports whether the device may stop being processed. The meaning of `a5`–`a7` is unknown |
| `SetParameterA(inst, index, value)` | TassmanSynthWrapper: tail call to vtable `+0x38`, which leads to `TassmanSynthWrapper::SetParameter` (Analog `0x18640`): it range-checks `index`, clamps `value` by entry kind and forwards to the engine. Softube: index 0 selects a model by `(uint)(value + 0.5)`, and index *n* ≥ 1 sets engine parameter *n*−1 (Cabinet maps index 2 to `int(value) * 0.5`). Corpus: tail call to vtable `+0x0` | Parameter set by integer index and float value |
| `ResetA(inst)` | One vtable call | State reset |

`GetPlugInfoU` values (Observed). For the TassmanSynthWrapper family the values come from
`__DATA,__data` initial words, such as Analog `0x5c2e8` = 1 and `0x5c2e0` = 1, and from
`__DATA,__common` (zero at load) for selector 4. No direct write to these words was found
in the pseudocode.

| Selector (size) | Amp, Cabinet | Analog, Tension, Collision, Electric | Corpus |
| --- | --- | --- | --- |
| 1 (8) | 1 | 1 | 1 |
| 2 (8) | 1 | 1 (initial data) | 1 |
| 3 (8) | 2 | 1 (initial data) | 2 |
| 4 (4) | 1 | 0 (`__common`) | 0 |
| 5 (8) | 32,767 | 512 | 512 |
| 6 (4) | 0 | 1 | 1 |

Inferred hypotheses, to be settled from Live's caller:

- Selector 3 is 2 for the three audio effects and 1 for the four instruments. In
  `CalcA` the value 1 means no audio input is passed, so selector 3 is plausibly the
  audio-input role.
- Selector 4 makes both outputs alias one buffer in `CalcA`. Plausibly it marks a mono
  processor; Amp and Cabinet return 1 and carry a Live-side `DualMono` parameter.
- Selector 5 is plausibly the maximum number of frames per call.
- Selector 6 matches the `kCanStopProcessing` requirement.

## Where the parameter model lives

**Observed: Live owns names, document structure and stored domains.**

- The schema (`12.0_12402`) declares every device class and field.
- All 502 parameter leaf names found in shipped documents occur in the Live image as
  UTF-16LE (502/502), and 237 also as C strings (`out/live_strings.json`).
- The bundles contain parameter names only where their own engines use the same words:
  Softube `Bass`…`Volume`, `MicrophoneType` and `MicrophonePosition`, and Corpus's
  module names `DryWet` and `StereoWidth`. The four TassmanSynthWrapper bundles contain
  none of their XML parameter names as exact strings.
- The interface carries no names, only an integer index and a float.
- Presence counts include unrelated uses of common words; no reference was traced.

**Bundle-side tables (Observed from pseudocode, `out/param_tables.json`).**

- **Softube.** Each model constructor (for example Amp `CSoftubeAmp_AC30Cleann44a` at
  `0x49a90`, Cabinet `CSoftubeAmp_1x12n44a` at `0x4d1c4`) declares its parameters with
  `CSoftubeParameter::SetAll(default, id, name, label, type, steps, …)` (`0x2ca78`).
  - Amp declares `Bass`, `Middle`, `Treble`, `Presence`, `Gain`, `Volume`: type 0
    (continuous), 100 steps, default 0.5. IDs `cA01`…`cA06`.
  - Cabinet declares `MicrophoneType` (type 1, 2 steps, default 0.0) and
    `MicrophonePosition` (type 1, 3 steps, default 0.5).
  - `CSoftubeEngine::SetParamFloatValue` (`0x2431c`) quantizes stepped parameters and
    clamps every value to [0, 1].
  - Model classes exist for 7 amps (`AC30Clean`, `AC30Crunchy`, `DualRectHeavy`,
    `DualRectLead`, `Plexi`, `SilverTwin`, `SimmsWattsBass`) and 5 cabinets (`1x12`,
    `2x12`, `4x10`, `4x10Bass`, `4x12`), each built separately for 44.1, 48, 88.2, 96,
    176.4 and 192 kHz. The string `WARNING: Sample rate not supported` is at Amp
    `0x1596af`.
  - Inferred: `AmpType` 0–6 and `CabinetType` 0–4 select a model. Live keeps `DualMono`
    and `DryWet`, because the engine has no such parameters.
- **TassmanSynthWrapper and Corpus.** A per-instance array of 28-byte ParamLink entries
  holds the engine module, module parameter, initialized flag, virtual flag, kind,
  min, max and last value. Setters write entries; for example Analog's builder at
  `0x18d8` and its setters at `0x179a4`, `0x17aa8`, `0x17c44` and `0x17d58`. Corpus
  writes entries inline in `0xc40c`. `SetParameter` (Analog `0x18640`) clamps the value
  by kind:
  - kind 0: clamp to [0, 1];
  - kind 1: clamp to [min, max], then rescale to 0–127;
  - kind 2: clamp to [min, max];
  - kind 3: clamp to [0, max] and truncate to int.

  The index tables below are static derivations from decompiler text. One Collision row
  (index 28) lost an argument in decompilation and has no range.

| Bundle | Index entries | Kind 0 / 1 / 2 / 3 | Virtual | XML parameters | Non-[0,1] ranges, bundle vs XML |
| --- | --- | --- | --- | --- | --- |
| Analog | 203 (0–202) | 104 / 0 / 8 / 91 | 10 | 171 | Differ: XML has 32 × `-1..1`, 3 × `-12..12`, 3 × `-3..3`; the bundle has none of these |
| Tension | 129 (0–129, one gap) | 67 / 0 / 8 / 54 | 10 | 107 | Differ: XML 27 × `-1..1` |
| Collision | 139 (0–138) | 34 / 25 / 49 / 31 | 22 | 139 | Mostly differ: bundle 46 × `-10..10`; XML 30 × `-5..5`, 15 × `-2..2` |
| Electric | 33 (0–32) | 27 / 1 / 4 / 1 | 1 | 33 | **Identical** multisets: `0..24`, `0..30`, `0..48` |
| Corpus | 37 (0–36) | 30 / 0 / 0 / 7 | 0 | 38 | Integer ranges match (`0..3`, `0..6` × 2, `0..21`, `0..24`). XML-only: `50..18000`, `0.5..9`, `-48..48`, `-50..50`, `0..360` × 2, `0..0.5`, `-1..1` × 4 |

Inferred: Live keeps its own per-parameter mapping from the stored value to (bundle
index, bundle value). Electric's index order is not the XML order:
`PerNotePitchBendRange` (0..48, added in schema `11.0_11300`) matches index 32, the last
entry. For Analog, Tension, Collision and Corpus, many stored domains are display
domains, such as Hz, semitones, degrees and bipolar −1..1, that Live must convert before
`SetParameterA`. The index mapping and the conversions are Live-side and unknown.

The bundles also contain engine-internal value formatters (Analog `0x1c280`: units `Hz`,
`dB`, `ms`, `s`, `BPM`, `%`) and enumeration labels such as Corpus's LFO waveforms and
`1/16`-style sync rates. Whether these are reachable from the seven exports was not
traced, and whether Live displays these strings is unknown.

## Parameter inventory in shipped documents

Observed (`out/scan.json`, `out/param_summary.json`): 599 of the 3,634 scanned documents
contain at least one of the seven devices, giving 1,064 occurrences. There were no parse
errors, and every byte match of a device tag was a real occurrence.

| Element (product) | Occurrences: `.adv` / `.adg` / `.alc` / `.als` | Parameters (Float / Enum / Bool) | Shipped default preset |
| --- | --- | --- | --- |
| `Amp` (Amp) | 263: 12 / 54 / 188 / 9 | 9 (7 / 1 / 1) | none |
| `Cabinet` (Cabinet) | 257: 11 / 51 / 185 / 10 | 5 (1 / 2 / 2) | none |
| `UltraAnalog` (Analog) | 98: 59 / 24 / 8 / 7 | 171 (119 / 24 / 28) | `Defaults/Instruments/Analog.adv` |
| `StringStudio` (Tension) | 146: 108 / 22 / 8 / 8 | 107 (78 / 13 / 16) | `Defaults/Instruments/Tension.adv` |
| `Collision` (Collision) | 50: 34 / 13 / 3 / 0 | 139 (108 / 22 / 9) | `Defaults/Instruments/Collision.adv` |
| `LoungeLizard` (Electric) | 214: 18 / 10 / 184 / 2 | 33 (31 / 2 / 0) | `Defaults/Instruments/Electric.adv` |
| `Corpus` (Corpus) | 36: 26 / 9 / 1 / 0 | 38 (28 / 6 / 4) | none |

Every occurrence uses MinorVersion `12.0_12402`. The full per-parameter inventory is
`out/param_table.tsv` (502 rows). Its columns are class, value kinds, observed min/max,
distinct count, modal stored range, occurrences with a different range, values outside
the range, mapped count, automation and modulation target counts, and the default-preset
value.

**Placement (Observed).**

- In `.adv` the device element is the root's child.
- In `.adg` it sits in `…/AbletonDevicePreset/Device`.
- In `.als`/`.alc` it is a child of a `Devices` list, nested two to four `Devices`
  levels deep.

**Envelope and field order (Observed).**

- Each device element starts with the 21 fields of the shared device envelope that all
  97 device-like classes in `12.0_12402` share: `LomId` … `ViewData`,
  `OverwriteProtectionNumber`.
- The device-specific fields follow, in schema order.
- All occurrences of a device carry an identical parameter path list (one path set per
  device), and every Timeable field the schema declares occurs.

**Parameter wrappers (Observed, schema class plus documents).**

| Class | Children in schema order | Stored value | Range child |
| --- | --- | --- | --- |
| `TimeableFloat` (372 parameters) | `LomId`, optional `KeyMidi`, `Manual`, `MidiControllerRange`, `AutomationTarget`, `ModulationTarget` | Decimal text; 309 parameters mix integer-looking (`5`) and fractional (`4.44444466`) text | `Min`/`Max` |
| `TimeableEnum` (70) | `LomId`, optional `KeyMidi`, `Manual`, `AutomationTarget`, `MidiControllerRange` | Decimal integer | `Min`/`Max` (0..N) |
| `TimeableBool` (60) | `LomId`, optional `KeyMidi`, `Manual`, `AutomationTarget`, `MidiCCOnOffThresholds` | `true`/`false` | Always `64..127` when unmapped |

**Value domains (Observed).**

- For each parameter the stored range, when no `KeyMidi` is present, is one modal
  `Min..Max`. All 502 parameters show the modal range in almost every occurrence; 13
  parameters have a few occurrences with a narrower range.
- No stored `Manual` value lies outside its parameter's modal range.
- 25 of the 70 enumerations never reach their range maximum in shipped content.
- Inferred: the modal range is the parameter's declared range. That is consistent with
  Electric's bundle ranges. Labels and units for the values are absent from the documents.

**Automation and modulation targets (Observed).**

- `AutomationTarget` is present on every parameter, and `ModulationTarget` on every
  `TimeableFloat` and on no other class. Each target holds `LockEnvelope`.
- Every target `Id` is `0` in `.adv`/`.adg` (37,794 parameter instances) and nonzero in
  `.als`/`.alc` (13,618).
- In all 215 sets and clips, nonzero target IDs are unique per document.
- None of the 3,553 envelopes in those documents (2,961 in `.als`, 592 in `.alc`) points
  at a parameter of these devices.
- Inferred: target IDs are assigned per document when a device is placed in a set or
  clip. Shipped content gives no example of automating these devices.

**Mappings (Observed).** `KeyMidi` appears on 1,672 parameter instances. These are only
inside racks and sets (137 `.adg`, 210 `.alc` and 27 `.als` occurrences; 0 of 268
standalone `.adv`). Every one has `Channel` 16; `NoteOrController` runs from 0 to 10. A
mapped parameter's `MidiControllerRange` is often a narrower sub-range, for example Amp
`Gain` `1.484375..10`. Inferred: `Channel` 16 with `NoteOrController` *n* is a binding to
rack macro *n*, and its range is the mapping range.

**Non-parameter fields (Observed, `out/fields.json`).**

- `*RelativePosition` is always `-1073741824`, except one Tension `OctaveRelativePosition`
  (`0`) and one Tension `TransposeRelativePosition` (`-90`).
- UltraAnalog `SelectedFinger` is `7`.
- Tension and Collision `CurrentTab` is `0`, except one Collision occurrence with `3`.
- Corpus `SideChain/RoutedInput/Routable` is always `MidiIn/None`, `No Output`, MPE
  channels 1–15, zone type 0.
- Amp, Cabinet and Electric have no such fields.

**Amp and Cabinet (complete).** Observed min and max are over all occurrences. The
engine column comes from the bundle.

| Parameter | Class | Stored range | Observed min–max (distinct) | Mapped | Bundle engine side |
| --- | --- | --- | --- | --- | --- |
| Amp `AmpType` | Enum | 0..6 | 0–6 (7) | 4 | Model select (index 0); 7 models |
| Amp `Bass`, `Middle`, `Treble`, `Presence` | Float | 0..10 | 0–10 (45–47) | 25–29 | Engine params 1–4; normalized, default 0.5 |
| Amp `Gain` | Float | 0..10 | 1.2598–9 (53) | 36 | Engine param 5 |
| Amp `Volume` | Float | 0..10 | 2.9365–10 (42) | 23 | Engine param 6 |
| Amp `DualMono` | Bool | 64..127 | both (2) | 0 | Not an engine parameter |
| Amp `DryWet` | Float | 0..1 | 0–1 (28) | 31 | Not an engine parameter |
| Cabinet `CabinetType` | Enum | 0..4 | 0–4 (5) | 7 | Model select (index 0); 5 cabinets |
| Cabinet `MicrophoneTypeSwitch` | Bool | 64..127 | both (2) | 6 | `MicrophoneType`, 2 steps, default 0 |
| Cabinet `MicrophonePosition` | Enum | 0..2 | 0–2 (3) | 2 | `MicrophonePosition`, 3 steps, default 0.5; index 2 maps 0, 1, 2 to 0, 0.5, 1 |
| Cabinet `DualMono` | Bool | 64..127 | both (2) | 0 | Not an engine parameter |
| Cabinet `DryWet` | Float | 0..1 | 0–1 (19) | 19 | Not an engine parameter |

Inferred, not established: Live sends Amp's 0..10 values divided by 10, and the
correspondence between Live parameters and Softube indices is the one shown.

**Corpus `ResonanceType` labels (`out/corpus_resonance.json`).**

- Observed: `Core Library/Devices/Audio Effects/Corpus/Pipe Resonator.adv` (SHA-256
  `d402e8f8…eff184`) stores `ResonanceType` 5. `Tubular Pan.adv` in the same folder
  (`c24d7dae…36418a`) stores 6. The 36 occurrences use all seven values 0–6; the JSON
  lists the documents for each value.
- Observed: Live's `__TEXT,__cstring` holds the adjacent strings `Res `, `Beam`
  (`0x105be2dac`), `Marimba`, `Membrane`, `Plate`, `Pipe`, ` Type`. They sit among
  filter and envelope labels. `String` and `Tube` are not in this run; identical
  strings are pooled, so they may be stored elsewhere.
- Inferred: the order Beam, Marimba, String, Membrane, Plate, Pipe, Tube for values
  0–6. The preset names support only 5 = Pipe and 6 = Tube. The string run is not shown
  to belong to Corpus rather than Collision, and no code reference was traced.
- A [learning demo](learning/demos/corpus-resonator.md) drives a labelled textbook
  modal-resonator stand-in with the shipped Corpus parameters. Its sound is not recovered
  code and is not evidence of Corpus's behavior.

**Schema history (Observed, `out/schema_devices.json`).** `UltraAnalog`, `StringStudio`,
`Collision`, `LoungeLizard` and `Corpus` are declared in the oldest shipped schema,
`8.1_220`. `Amp` and `Cabinet` first appear in `8.1_226`. Device-specific changes since
then (files ordered by family, then translator number):

- MPE fields added in `11.0_11300`/`12.0_12001` for UltraAnalog (9), StringStudio (9),
  Collision (5, replacing 3 `…On` fields) and LoungeLizard (`PerNotePitchBendRange`).
- Collision `CurrentTab` added in `11.0_413`.
- Corpus side-chain MPE fields added in `11.0_436` and `12.0_12119`.
- UltraAnalog `SignalChain2/FilterSlave` renamed `FilterControllee` in `12.0_12004`.
- `DeviceTags` and `LastSelectedModulationIndex` appear and disappear in 8.x–9.0.

`12.0_12000` lacks the MPE fields that `11.0_11300` has, so this ordering is not a
release chronology.

## Candidate requirements for per-device parameter specs

Proposed. These cover only the preset load/save representation and the parameter
domains. "Shipped" means present in 12.4.3 content, not observed being loaded or saved
by 12.4.3.

| Candidate | Statement | Evidence | Strength |
| --- | --- | --- | --- |
| DEV-C01 | The seven devices are stored as elements `Amp`, `Cabinet`, `UltraAnalog`, `StringStudio`, `Collision`, `LoungeLizard`, `Corpus`. They are the root child in `.adv`, inside `AbletonDevicePreset/Device` in `.adg`, and inside `Devices` lists in `.als`/`.alc` | 1,064 occurrences | Observed for shipped content |
| DEV-C02 | Each device element is the 21-field device envelope followed by the device-specific fields of schema `12.0_12402` in schema order. Writers emit every field | One path set per device; schema | Observed; reader tolerance of missing fields is unknown |
| DEV-C03 | Parameters use the three Timeable wrappers with the child orders above. Bool ranges are `MidiCCOnOffThresholds` `64..127` | 502 parameters | Observed |
| DEV-C04 | Readers accept `TimeableFloat` `Manual` as integer-looking or fractional decimal text, Enum as integers, Bool as `true`/`false` | Value kinds | Observed |
| DEV-C05 | Each parameter's domain is its stored unmapped `MidiControllerRange`, per `out/param_table.tsv`; shipped values never exceed it | 502 rows, 0 outside | Observed domain. Clamping or rejection on load is unknown |
| DEV-C06 | Preset files (`.adv`/`.adg`) write `AutomationTarget`/`ModulationTarget` `Id="0"`. Set and clip files write nonzero IDs, unique within the document | 37,794 / 13,618 instances; 215 documents | Observed for shipped content; the save rule is inferred |
| DEV-C07 | A rack macro binding is stored on the target parameter as `KeyMidi` (`Channel` 16, `NoteOrController` = macro index) plus a `MidiControllerRange` mapping sub-range | 1,672 instances | Representation observed; meaning inferred |
| DEV-C08 | New instances of Analog, Tension, Collision and Electric take their values from `Core Library/Defaults/Instruments/<Product>.adv`. Defaults for Amp, Cabinet and Corpus are unknown | Default-preset values in `param_table.tsv` | Inferred; Phase 4 |
| DEV-C09 | Non-parameter fields round-trip: `*RelativePosition` sentinel `-1073741824`, `SelectedFinger`, `CurrentTab`, Corpus side-chain routing | `out/fields.json` | Observed values; semantics unknown |
| DEV-C10 | Amp `AmpType` has 7 values and Cabinet `CabinetType` 5. Cabinet `MicrophonePosition` has 3 values and `MicrophoneTypeSwitch` 2 | Ranges, plus the bundle model and step tables | Observed counts; labels unknown |

## Unknowns

- The Live-side map from each stored parameter to (bundle index, value conversion) for
  all seven devices. Without it the stored domains above cannot be tied to engine
  behavior.
- Labels, units and display strings for enumerations and continuous parameters. The
  documents hold only numbers; Live's UTF-16 strings and `Languages.alp` were not decoded.
- Live's built-in defaults where no default preset ships (Amp, Cabinet, Corpus), and
  whether Defaults presets are consulted at all.
- Load behavior for values outside the range, missing parameters, extra elements or
  malformed text; whether `KeyMidi` with a channel other than 16 is used for these devices.
- What `GetPlugInfoU` selectors 1, 2, 4 and 5 mean, and the roles of `CalcA` arguments `a5`–`a7`.
- How `DualMono` and `DryWet` are realized for Amp and Cabinet.
- Sample-rate behavior outside the six Softube model rates.

## Questions for the main Live project

Each question starts from the Live anchors above, through references in the saved
LiveR2 project:

1. Who references the seven entry-point strings (`0x105bdd69e`–`0x105bdd6ef`)? That
   gives the loader, the bundle path composition (`Devices`, `Mac`, `.bundle`), and the
   failure handling when a bundle or symbol is missing or `CreateInstanceU` returns NULL.
2. Which `GetPlugInfoU` selectors does Live query, and what does it do with each answer:
   input role, mono, maximum block size, stop capability?
3. For each device class, where is the parameter-to-index table, and what conversion
   is applied before `SetParameterA`? Start from the class-name strings and the
   per-device parameter names, which are UTF-16 in Live.
4. Where are `DualMono` (`0x105be6a58`) and `DryWet` implemented for Amp and Cabinet?
   Are two instances created for dual mono?
5. How does Live call `CalcA`: frame counts, the event payload in `a5`/`a6`, the
   structure in `a7`, and what it does with `flagOut`?
6. Is `Core Library/Defaults/<kind>/<Product>.adv` read when a device is created?

## Phase 4 probe records

Each probe follows [ADR 0002](../decisions/adr-0002-static-first-analysis.md). Each one
runs on the macOS reference host with retained captures, and all are batched with the
other Phase 4 probes. Inputs are copies, never edited shipped files. Tool availability
must be established first.

| Probe | Question | Static evidence so far | Minimal input | Discriminating observation | Stop when |
| --- | --- | --- | --- | --- | --- |
| P4-H4-01 Save round-trip | What does 12.4.3 write when it saves each device? | DEV-C01–C09 come from shipped content only | Insert each device fresh; also load each default or shipped preset; save as `.adv`, and save a set holding all seven | XML diff against the inputs: field order, value text, IDs, ranges, envelope | Seven presets and one set saved and diffed |
| P4-H4-02 Out-of-domain load | Does load clamp, reject or keep out-of-range values? | DEV-C05 | Copies of one Amp and one Analog preset with `Manual` above max, below min, non-numeric and missing; an enum index past its maximum | The value shown after load and after re-save; any error dialog | Each case observed once |
| P4-H4-03 Built-in defaults | What values does a fresh Amp, Cabinet or Corpus have, and does editing `Defaults/*.adv` change a fresh Analog? | No default preset for three devices | Empty set; insert each device; save | Saved `Manual` values | Values recorded for all seven |
| P4-H4-04 Display domains | Which labels and units belong to each stored domain? | Units appear only as engine strings | A control-surface or Max for Live script dumping each parameter's name, min, max, quantization, value items and string for value, if the API is confirmed present in 12.4.3 | Parameter table per device | All seven tables captured |
| P4-H4-05 Unsupported sample rate | What do Amp and Cabinet do at a rate without a model (for example 32 kHz)? | Six model rates; `Sample rate not supported` | Set the audio device rate; insert Amp | Output signal present or absent; any message | One rate observed |

## Signal behavior needing measured comparison later

Not specified here: the DSP of all seven devices, Softube model selection by sample
rate, Live-side `DryWet` and `DualMono`, polyphony and voice allocation, MPE response,
stop-processing and tail behavior (`flagOut`), and the `CalcA` output-scaling branch in
the TassmanSynthWrapper family. Each needs measured original-versus-candidate audio
with declared tolerances under FEAT-AUDIO.

## Limitations

- Only shipped content was scanned. Max-for-Live `.amxd` devices and `Max/` presets are
  outside this scope.
- Pseudocode came from Ghidra's default analysis. Argument roles and tables are derived
  from decompiler text, and one row lost an argument.
- Signature identities were parsed from code-signature blobs; the signatures were not
  verified cryptographically.
- No organization is attributed to a team ID.
- The x86_64 slices were compared only by their exports. They export the same seven
  entry points and differ only in a few C++ typeinfo symbols.
