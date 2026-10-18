# N5 device mapping v1: analyst notes

Packet N5 (FEAT-DEVICES, Q-006). Live 12.4.3 `Live.arm64` (SHA-256 `3a99ceea…d1c383cfad`, image
base 0x100000000). Static only; nothing was executed. Page:
`wiki/research/device-parameter-mapping-native.md`.

## Sources and tools

- Dossiers from the read-only R2FunctionDossier server, copied unchanged to `results/n5-000{1..4}/`
  (each has `request.txt`, `queries.json`, `manifest.json`).
- C1 corpus and C2 indexes under `/var/tmp/sound-analysis/corpus/` (read through the existing
  `analysis/ableton-live-12.4.3/r2/n1-transport-state-v1/corpus_lookup.py`, cache redirected with
  `N1_CACHE`). Pointer words read with `analysis/ableton-live-12.4.3/r2/n1-transport-state-v1/read_ptrs.py`
  on `analysis/ableton-live-12.4.3/derived/Live.arm64`. Neither script was modified.
- Corpus helper corpus `/var/tmp/sound-analysis/helpers/Corpus/corpus/` and the bundle's arm64 slice.
- H4 outputs `../h4-devices-v1/out/param_table.tsv`, `param_tables.json`.

Commands (cwd = this directory, `python3 -I`, Python 3.13 standard library):

```
python3 -I extract_mapping.py out ../h4-devices-v1/out      # out/live_index_map.tsv, live_index_summary.json
python3 -I conversions.py out ../h4-devices-v1/out          # out/conversions.tsv, corpus_parameters.tsv (asserts)
python3 -I excerpts.py out "<app>/Contents/App-Resources/Devices/Mac/Corpus.bundle/Contents/MacOS/Corpus"
```

## Rounds

| Round | Request | Functions | Resolution | Next query |
| --- | --- | --- | --- | --- |
| 1 | n5-0001 | 0x102f998c4 loader, 0x102fbe25c instance, 0x102fbe49c GetPlugInfo, 0x102fbf644 dual instance, 0x1031983d4 path, 0x1030ebe78 Electric vector, 0x103192720 float setup, 0x102fbdf34 factory | Loader branches confirmed in disassembly (load failure clears pointers and releases the bundle; CreateInstanceU result not tested). Electric vector sits at vtable 0x1068c4bb8 + 0x5a0 | Who consumes slot +0x5a0; value domain |
| 2 | n5-0002 | 0x103197a6c Amp float setup, 0x1026f0bcc timeable init, 0x103192974 bipolar, 0x10319cb10 parameter-unit builder, 0x1030e54e8 Corpus vector, 0x1030ca45c Cabinet vector, 0x102fbec58 SetParameterA call, 0x102fbfe54 pending flush | Float args confirmed: Amp passes internal (0,1), default 5.0, `ALinearUserFloatConverter(0,10)`. Corpus vector at 0x1068c3d80 + 0x5a0, Cabinet at 0x1068c2718 + 0x5a0 | Corpus constructor arguments |
| 3 | n5-0003 | 0x10319c95c converter insertion, 0x1030e277c / 0x1030e3830 / 0x1030e4c94 / 0x1030e12c8 Corpus inits, 0x1030b4934 Amp ctor, 0x1030c9c90 Cabinet ctor, 0x1030e9578 Electric ctor | Every float argument used in `conversions.py` checked against the `fmov`/`movi`/`scvtf` before the call | Converter and quantizer arithmetic |
| 4 | n5-0004 | 0x101bb9f34 ConvertQuantingInt, 0x1015758bc / 0x101577e70 / 0x1015763e0 converters, 0x102fccd28 OnParameter, 0x10294de10 MultiplyOffset setter, 0x102faadb8 IntegerMapping, 0x1030e7f80 Electric registration | ConvertQuantingInt rounds with `frinta` to 1/32768 before `fcvtzs` (the decompiler's `(long)` cast hid this). Setter stores index, multiplier, offset in message order | Stopped: four rounds used |

## Function map (Live)

Loader and instance (audio side): factory message `OThirdPartyDeviceFactory.Create(Handle, Path)` registered by
0x102fbdeb4, handler 0x102fbdf34 → 0x102fbe07c (defaults: +0x70=1, +0x78=1, +0x80=0, +0x84=0, +0x88=0x400,
+0x90=1) → 0x102f998c4 (CFBundle load, `GetPlugInfoU` via 0x102fbe49c, six names via
`CFBundleGetFunctionPointerForName`; CFString constants 0x106ba17e8…0x106ba18a8 point at the C strings
0x105bdd69e…0x105bdd6ef). 0x102fbe248 clears entry pointers. 0x102fbe25c creates an instance;
0x102fbf644 a second one when +0x84 ≠ 0. 0x102fbe580 = SetSampleRateU, 0x102fbec58 = SetParameterA,
0x102fbe650 = ResetA, each under FPCR.FZ. Instance vfunc 0x102fcc390 returns +0x88.

Main side: module getters by name (Amp 0x1030b54ec, Cabinet 0x1030ca554, Collision 0x1030df330, Corpus
0x1030e6104, Electric 0x1030ec8d0, Tension 0x103196dcc, Analog 0x1031b1368) → 0x103196ec0 find-or-create
in the list at 0x107027f28 → 0x1031983d4 builds `<dir>/Devices/Mac/<Name>.bundle` (inline SSO strings
"Devices", "Mac", literal ".bundle"), tests it with 0x103e9728c and posts the factory message
(descriptor 0x107027d98). Load status message `AThirdPartyDeviceModule.LoadPluginStatus(DeviceModuleId,
Status)` (0x103198c00 → handler 0x103198c80) uses text key `AThirdPartyDeviceModule`/
`sErrorTextPluginLoadFailed` (0x10319bd08). The sender of that message was not traced.

Parameter path: device vfunc +0x5a0 (Amp 0x1030b5220, Cabinet 0x1030ca45c, Electric 0x1030ebe78, Corpus
0x1030e54e8; Collision 0x1030debd0, Tension 0x103193b1c, Analog 0x1031ad110 are nested and not extracted)
→ 0x10319cb10 builds per entry: parameter unit (0x10319c4dc), optional `AConvertQuantingInt`
(0x10319c95c, when the user converter casts to `ALegacyQuantingIntUserFloatConverter`, typeinfo
0x106680fb8), mapping module by entry mode → processor payload {index, value} → OnParameter
0x102fccd28 (index ≤ 255) → pending table → 0x102fbfe54 → 0x102fbec58.

Mode → module (constructor follows `SNewCompound<…>`; registrations in 0x10295fec8): 0 AIndexedFloatModule
"Indexer" (0x101e504ec: value unchanged), 1 AAasModulationPolarizer (|v| and sign), 2 AAasToggleMapping,
3 AAasFilterType (v>>1, v&1), 4 AAasBoolInverter, 5 AAasToToggleMapping, 6 AAasMultiplyOffset
(offset + multiplier·v; message `Handle, Index, Multiplier, Offset` 0x102fa7bf0), 7
AThirdPartyIntegerMapping "MappedIndexer" (float(table[int v]), no bounds check, 0x102faadb8), 8
ACollisionScaledMode. Mode constants: `0x1055d1ec0` = 6, `0x1055d1ed0` = 7 (bytes read from the image).

Value model: `FUN_1026f0bcc(p1, p2, default, timeable, device, userConverter, display, name, flags)` stores
p1, p2 as the internal range of `mpCurrent` (+0x80/+0x84), the default as its value and as `mpManual`
(0x101568960), and the user converter at +0x78. Member names from 0x1026f0390 (`mpCurrent` 0x228,
`mpManual` 0x240, `mpMidiControllerRange` 0x210). Converters (typeinfo names read from the image):
`ALinearUserFloatConverter` (vtable 0x1066807e0; user→internal 0x1015758bc linear + clamp),
`ALegacyQuantingIntUserFloatConverter` (0x106680c18; 0x101577e70 same; internal→user 0x101577ec0 truncates),
`AQuantizingUserFloatConverter` (0x106680c90; clamp only), `ALog10UserFloatConverter` (0x106680948;
0x1015763e0: u ≤ 0 → min, else log10(u/c0)/log10(c1/c0) clamped). MIDI controller range Min/Max are
set from p1/p2 through internal→user (0x1025856a0, 0x101574564), which is why the stored
`MidiControllerRange` equals the user domain.

## Corpus bundle side (helper corpus)

`CreateInstanceU` 0x46e4 → ctor 0xc40c stores vtable 0x2cb88 (`13CorpusWrapper`, base
`WrapperTemplate<CorpusSynth,37>` 0x2c090). `_SetParameterA` 0x4f40 calls slot 0 = 0xd75c (override),
which handles indices ≤ 37, special-cases 0, 2, 3, 5, 7, 8, 9, 11, 14–16, 22–25, 29, and passes the rest to
the base 0x50c0 (indices < 37 only: kind 3 → int(min(v, max)), else min(v, 1) then 128v or 126v+1). The
ResonanceType table at 0x2a450 is 1, 2, 3, 4, 5, 7, 6. All in `out/corpus_bundle_excerpts.jsonl` and
`out/corpus_bundle_facts.json`.

Coordinator hints (from another session): "indices 14–16 mapped 64 + 31.5·v" — confirmed in 0xd75c cases
0xe–0x10. "Index 6 is a fixed pitch, linear −4..4 octaves around 261.62 Hz" and "stored Frequency does not
reach the resonator directly" — not verified: index 6 takes the base path (min(v,1) → 0..127 → engine
module param 4 per H4); the constant 261.62 occurs in engine function 0x23670, whose link to index 6 was not
traced. Live does send stored `Frequency` (identity, clamped 0..1) at index 6.

## Contradictions and corrections

- H4 classified Corpus bundle entries 2, 3, 7, 8, 9, 11, 23–25, 29 as kind 0 [0, 1] and concluded the
  stored ranges −48..48, −50..50, 0..360, 0.5..9, −1..1 are "XML-only". The real setter is the CorpusWrapper
  override, which converts exactly those domains. H4's statement needs qualifying.
- H4 found 37 Corpus bundle entries (0–36); Live builds 38. Index 37 (`MidiMode`) passes the override's
  bound but is ignored by the base path. `ACorpusUnit` wires a `MonophoneMode` module (0x1031a0358), so MIDI
  mode is probably handled in Live (Inferred).
- Electric: `PerNotePitchBendRange` (stored) is not in the vector; index 32 carries the unstored
  `DummyPerNotePitchBendRange` (default 48). H4's "PerNotePitchBendRange matches index 32" is a range match
  only.

## Not done

Analog, Tension and Collision tables (nested builders using modes 1–5 and 8). XML read path (clamping,
missing elements). Who sends OnDualMono/OnDryWet. Meaning of `GetPlugInfoU` selectors 1 and 2 on the Live
side. Whether `Defaults/<Product>.adv` is read.

## Cross-check with corpus-dsp-static (coordinator request, after round 4)

- `wiki/research/corpus-dsp-static.md` and `../corpus-dsp-v1/report-{chain,resonator}.md` (another session)
  give the bundle host map. Its inferred names for hosts 0–36 equal Live's vector order here.
  Correction: Live sends index 37 (`MidiMode`); the bundle ignores it.
- No dossier round was left, so `FUN_103197830`'s float arguments were checked from raw instruction words
  in `Live.arm64`: `0x1031978cc` `2f00e400` movi d0,#0; `0x1031978d0` `1e2e1001` fmov s1,#1.0;
  `0x1031978e0` `1e204102` fmov s2,s8; `0x1031978e8` bl `0x1026f0b58`. Internal range 0..1 for every
  `FUN_103192720` parameter, including `ExcitationX`, `ListeningXL/XR`, `Radius`, `Frequency`.
- Corpus vector entries for members 0x448/0x460/0x478/0x310/0x2e0/0x5b0 store entry[2] = `fneg(movi 0)` =
  0x8000000000000000 (mode 0) and entry[3] = FLT_MAX pair (n5-0002 disassembly).
- `out/corpus_priority.tsv` chains Live conversion → wrapper rule → engine driver (engine drivers copied
  from the other session, unverified). Open contradiction: the positions reach controller 64…95.5 only.
