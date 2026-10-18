---
id: RESEARCH-WARP-MARKERS
type: research
status: draft
updated: 2026-10-17
access: analysis
target: Ableton Live 12 Suite 12.4.3 arm64
---

# Warp markers and warp settings

Packet S8 (FEAT-WARP). Question: how does an audio clip store its warp markers
and warp settings, and how does Live 12.4.3 interpret them on load? The static
half reads the shipped schemas and documents. The native half traces the
reader, the enumerations and the marker helpers in the arm64 image. Nothing was
executed. "Load fails" means the traced code raises an error; what the user sees
was not traced. The time-stretching algorithms are out of scope; audio output
needs measured comparison (PRB-S8-11).

The value parsing, number text and generic loader come from
[transport-state native](transport-state-native.md), and the container from
[document container native](document-container-native.md). They are not repeated here.

## Evidence

Source: [SRC-ABLETON-12-4-3](sources/ableton-live-12.4.3.md), bundle
`/home/ollie/Ableton Live 12 Suite.app` (read-only). Image
`analysis/ableton-live-12.4.3/derived/Live.arm64`, SHA-256 `3a99ceea…d1c383cfad`,
Ghidra 12.1.4. Retained run: [s8-warp-v1](../../analysis/ableton-live-12.4.3/r2/s8-warp-v1/manifest.json).
`sh run.sh` (Python 3.13.9, `python3 -I`) regenerates every derived file; two
consecutive runs gave byte-identical output.

| File | Content |
| --- | --- |
| [static-survey.json](../../analysis/ableton-live-12.4.3/r2/s8-warp-v1/static-survey.json) | 203 schemas: field evolution, holders, field order. 4,005 documents: distributions, ranges, `checks`, `notable` |
| [audioclip-warp-records.jsonl](../../analysis/ableton-live-12.4.3/r2/s8-warp-v1/audioclip-warp-records.jsonl) | One line per shipped AudioClip (2,878): settings, markers, sample reference, loop fields |
| [inputs-documents.tsv](../../analysis/ableton-live-12.4.3/r2/s8-warp-v1/inputs-documents.tsv) | SHA-256 and path of the 4,005 `.als`, `.alc`, `.adv` and `.adg` files read |
| [notes.md](../../analysis/ableton-live-12.4.3/r2/s8-warp-v1/notes.md) | Round-by-round native findings with addresses, ✓ marks and negative results |
| `results/s8-0001` … `s8-0003` | Unchanged query-server results with request text: 23 dossiers with disassembly |
| [corpus-excerpts.jsonl](../../analysis/ableton-live-12.4.3/r2/s8-warp-v1/corpus-excerpts.jsonl) | The 71 C1 records relied on, with chunk, offset and line SHA-256 |
| `registrations.txt`, `getter-constants.txt`, `vtable-reads.txt`, `strings-lookup.txt`, `symbols-warp.txt` | Member registrations, decoded range constants, vtable slots and tables, string and symbol lookups |
| [probe-batch.json](../../analysis/ableton-live-12.4.3/r2/s8-warp-v1/probe-batch.json) | Phase 4 probe records PRB-S8-01 to 11 |

Inputs: 26 `.als`, 350 `.alc`, 2,557 `.adv` and 1,072 `.adg`; 4,005 AppleDouble
companions skipped. One `.adv` (`Misc/MidiPreHear.adv`, binary) did not parse. The
shipped documents were written by 12.4d1 or 12.1d1, not by 12.4.3. Native budget:
three rounds of 8, 8 and 7 dossiers. ✓ marks a branch or constant checked in
dossier disassembly; the rest is C1 pseudocode.

## Where warp state lives

**Observed** in `12.0_12402` (latest schema):

| Holder | Warp fields (class) |
| --- | --- |
| `AudioClip` | `IsWarped` (RemoteableBool), `SampleRef`, `Onsets`, `WarpMode` (RemoteableEnum), `GranularityTones`, `GranularityTexture`, `FluctuationTexture` (UserFloat), `TransientResolution`, `TransientLoopMode` (RemoteableEnum), `TransientEnvelope`, `ComplexProFormants`, `ComplexProEnvelope` (UserFloat), `Sync`, `HiQ`, `Fade`, `PitchCoarse`, `PitchFine`, `SampleVolume`, `WarpMarkers` (RemoteableList), `SavedWarpMarkersForStretched` (RemoteableList), `MarkersGenerated`, `IsSongTempoLeader` |
| `SampleWarpProperties` (field of `MultiSamplePart`, used by Simpler and Sampler) | `WarpMarkers`, `WarpMode`, the same eight mode settings, `IsWarped`, `Onsets`, `TimeSignature`, `BeatGrid` |
| `WarpMarker` | `SecTime`, `BeatTime` (Double) |
| `SampleRef` | `FileRef`, `LastModDate`, `SourceContext`, `SampleUsageHint`, `DefaultDuration` (Int), `DefaultSampleRate` (Int), `SamplesToAutoWarp` (RemoteableEnum) |
| `Loop` (clip) | `LoopStart`, `LoopEnd`, `StartRelative`, `LoopOn`, `OutMarker`, `HiddenLoopStart`, `HiddenLoopEnd` |

`MidiClip` also has `IsWarped`. No schema has a `FluxTexture` field: the stored
name is `FluctuationTexture`; "Flux" appears only in the modulation target
`FluxModulationTarget` and the engine callback `OnFluxModulation`.

**Evolution (observed, ordered by file name):** `WarpMarker` is (`SecTime`,
`BeatTime`, Double) in all 203 schemas. All `AudioClip` warp fields above keep
their class from `8.1_220` to `12.0_12402`, except `IsSongTempoLeader` (from
`12.0_12002`). `SampleWarpProperties` exists from `9.5_305`; its
`HasCustomWarpMarkers` existed only in `9.5_305`–`9.5_319`. `SampleRef/SamplesToAutoWarp`
exists from `12.0_12119`. Translator `0x1014919c4` uses the strings `WarpMarkers`,
`WarpMarker`, `SecTime` and `BeatTime`; it was not traced.

**Shape (observed and native).** A marker list is written as
`<WarpMarkers><WarpMarker Id="10" SecTime="0" BeatTime="0" />…</WarpMarkers>`. The
registration `0x10260fdd8` gives `mSecTime` (+0x50) and `mBeatTime` (+0x58) type −4
with flag 4 ✓, the flag that the [transport-state native](transport-state-native.md#names-order-and-attributes-come-from-the-member-registry)
writer emits as attributes. `Id` is the list-item id: unique within each shipped
list, but not ascending in 18 lists. `DefaultDuration` and `DefaultSampleRate` have
flags 0 ✓ (`0x102875ec0`) and are child elements.

## What the shipped documents hold

**Observed** ([static-survey.json](../../analysis/ableton-live-12.4.3/r2/s8-warp-v1/static-survey.json)
`checks`, `distributions`). There are 14,494 marker lists: 2,878 in AudioClips (14
`.als` files; 2,679 of them in `Sample Reference.als`) and 11,616 in
SampleWarpProperties (388 files). The AudioClip results are therefore dominated by
one reference set.

| Check | AudioClip | SampleWarpProperties |
| --- | --- | --- |
| Marker count | 2 markers: 2,667 (2,479 unwarped, 188 warped); 3: 197; 4: 4; 5: 1; 12: 9. Never 0 or 1 | 0: 4,244 (all unwarped); 2: 6,141; 3: 1,231 |
| `SecTime` and `BeatTime` strictly increasing (lists of ≥2) | 2,878 / 2,878 | 7,372 / 7,372 |
| Last marker exactly 1/32 beat after the previous one | 2,869 / 2,878 (others 1/16 or 1/64 beat) | 7,313 / 7,372 |
| Tempo of the last segment equals the previous segment (≥3 markers) | 189 / 211 | 1,227 / 1,231 |
| First marker at (0, 0) | 2,820 / 2,878 | 7,299 / 7,372 |
| Every segment tempo within 5–999 BPM | 2,878 / 2,878 | 7,372 / 7,372 |
| Negative values | `SecTime` never; `BeatTime` in 5 markers | none |

Across both holders, 44,058 of 44,058 `SecTime`/`BeatTime` texts match the native
Double writer rule ([REQ-TRANSPORT-STATE-011](../specs/transport-state.md#req-transport-state-011--number-text-on-save)),
and 22,029 of 22,029 `BeatTime` values lie on the 1/3,843,840-beat grid.

**Settings.** Every AudioClip carries the constructor defaults (below):
`GranularityTones` 30, `GranularityTexture` 65, `FluctuationTexture` 25,
`TransientResolution` 6, `TransientLoopMode` 2, `TransientEnvelope` 100,
`ComplexProFormants` 100, `ComplexProEnvelope` 128. SampleWarpProperties vary
within the constructor ranges: Tones 12–80.0625, Texture 2–132.5, Fluctuation
0–100, TransientEnvelope 0–100, Formants 0–100, ComplexProEnvelope 8–128,
TransientResolution {6, 4, 3}, TransientLoopMode {2, 1, 0}. `WarpMode` values:
unwarped AudioClips all 0; warped AudioClips 0 (291), 4 (92), 3 (10), 6 (6);
SampleWarpProperties also 1 and 2. No shipped document uses 5 (REX). `MarkersGenerated`
is true in 2,764 and false in 114 AudioClips. `SavedWarpMarkersForStretched` is empty
except in 3 AudioClips (64 markers each). `SamplesToAutoWarp` is 0 except in 4
SampleWarpProperties (1). Sample rates: 44,100, 96,000, 48,000, 22,000, 22,050.

**Units (observed, interpretation inferred).** Let *L* = `DefaultDuration` /
`DefaultSampleRate`.

- Unwarped AudioClips (2,479): `LoopEnd` = `HiddenLoopEnd` = *L* in 2,479 of 2,479.
  `OutMarker` = *L* in 1,866, = *L* × set tempo / 60 in 432, and neither in 181.
  Inferred: an unwarped clip's loop fields are in seconds of sample time and
  `DefaultDuration` is in sample frames. The unit of `OutMarker` in unwarped clips
  is unknown.
- Warped AudioClips (399): extrapolating the last segment to *L* gives `OutMarker`
  in 292 (within 10⁻⁶ beat), `HiddenLoopEnd` in 284 and `LoopEnd` in 244.
  Extrapolating the first segment back to 0 s gives `HiddenLoopStart` in 330.
  Inferred: warped clip region fields are in beats, `SecTime` is seconds from the
  sample start and `BeatTime` is clip beats.

## How the reader treats markers and settings

**Load path (static-derived).** The AudioClip, AWarpMarker and ASampleWarpProperties
vtables use the generic loader `0x101487310`; AudioClip and AWarpMarker also use the
generic writer `0x101486cdc`
([vtable-reads.txt](../../analysis/ableton-live-12.4.3/r2/s8-warp-v1/vtable-reads.txt)).
As in [transport-state native](transport-state-native.md#how-a-set-reaches-the-transport-objects),
base values are stored directly with no setter, clamp or range check. The
consequences:

- **Missing attribute or element.** The AWarpMarker constructor `0x1026105ec` sets
  `SecTime` and `BeatTime` to DBL_MAX ✓; the writer spells that `Invalid`. A missing
  warp setting keeps its constructor default (table below).
- **Out-of-range values.** No range check runs on load for `WarpMode`, the two
  transient enums or the UserFloat settings. The ARemoteableEnum setter's range check
  is not on the load path. What a stored `WarpMode` of 7 or −1 does afterwards is
  unknown (PRB-S8-05).
- **No quantisation on load.** The `BeatTime` setter `0x1026101b4` ✓ rounds to the
  nearest 1/3,843,840 beat, half away from zero. The loader does not call it. Edit
  paths round, so Live-written beats sit on that grid; `SecTime` is never rounded.
- **Ordering.** No sort or order check was found on load. Later code assumes
  ascending order: onset linking `0x1027b7cf0` walks markers and onsets together, and
  marker lookup by beat `0x1027c79d0` scans until it passes the target.

**Minimum count.** The AudioClip post-load hook `0x1027c1c7c` ✓ (vtable
`0x10680bea0` slot +0xd0) tests the list with `0x10156da34` ✓ (count == 0). An empty
list raises `Empty warp marker array.` through `0x101488e64` ✓ and the
document-corrupt error `0x10148229c`. A non-empty list links each marker to its owner
and to a coinciding onset. ASampleWarpProperties' hook `0x10288538c` ✓ has no such
check, which matches the 4,244 shipped empty lists. A one-marker AudioClip passes
this check; what it then does is unknown (PRB-S8-02). Whether the post-load hook runs
on every set load is the same open question as in transport-state native.

## The shadow marker

**Observed native, confirmed:** the last list element is the "shadow marker".

- `0x1026102c0` ✓ returns true for the list's last element.
- The API refuses to delete or move it: `The shadow marker can't be deleted.`
  (`0x1033bfa68` ✓) and `The shadow marker can't be moved.` (`0x1033bfb94` ✓).
- `0x102612464` ✓ appends it at `BeatTime = q(last.BeatTime + 1/32)` and
  `SecTime = last.SecTime + (60 / tempo) × 1/32`, where *tempo* is a BPM argument.
- `0x102610bc4` ✓ (scale beats about the first marker) re-places it 1/32 beat
  after the previous marker. `0x1027d304c` and `0x102610fb0` (C1) rebuild it with
  the previous segment's slope.
- The flip model `FWarpMarkerContainer` holds `mWarpMarkers` and `mTempoAfterLastMarker`,
  with the assertion `Constraints::kMinSegmentBpm <= tempoAfterLastMarker() <= Constraints::kMaxSegmentBpm`.

**Inferred:** the stored list is the visible markers followed by one shadow marker
1/32 beat later, whose segment encodes the tempo after the last visible marker. It
usually equals the last visible segment's tempo (189 of 211 shipped AudioClips with
≥3 markers) but is stored independently. Example: the Patience Suite Demo
(SHA-256 `3f1c0f92…0952b`) clip "Vocal Main" has markers (0 s, 0) and
(0.0112275449101796407 s, 0.03125): one visible marker and a shadow at exactly
167.0 BPM. Extrapolating to *L* = 2,138,444 / 48,000 s gives 124.000051 beats; the
stored `OutMarker` is 124.00005151098901. Nine shipped AudioClips and 59
SampleWarpProperties use spacings of 1/16 or 1/64 beat instead. No load-time
normalisation was found (PRB-S8-07).

## From sample time to beat time

**Observed native:**

- Segment tempo `0x10261093c` ✓: (*b*₂ − *b*₁) / (*s*₂ − *s*₁) × 60 BPM, and −60 when
  *s*₂ ≤ *s*₁. `0x102610910` gives the same in beats per second (−1 when degenerate).
- The "Segment BPM" value for a marker uses the segment ending at it, or the
  segment starting at it for the first marker (`0x1027c28dc`, C1).
- After inserting a marker while recording, `0x1027c724c` ✓ deletes the previous
  marker when its seconds lie within 0.001 s of the straight line through its
  neighbours.
- Edit limits: `0x1027afd40` ✓ bounds a marker's beat relative to a neighbour so that
  the segment stays within 5–999 BPM. The API add function `0x1033bf42c` ✓ enforces
  these limits ("Segment length out of range."). It also requires
  0 ≤ sample time ≤ sample length and a beat no lower than the left neighbour and no
  higher than the right one (unless the right one is the shadow). The clip must be
  warped.

**Inferred (not traced to a conversion routine):** beat time is piecewise linear in
sample time. Between adjacent markers *i*, *i*+1:
*b* = *b*ᵢ + (*s* − *s*ᵢ)(*b*ᵢ₊₁ − *b*ᵢ)/(*s*ᵢ₊₁ − *s*ᵢ). Before the first marker the
first segment's slope applies, and after the last marker the shadow segment's slope
applies. Support: constant per-segment tempo, the collinearity test, the shadow
construction and the shipped extrapolation checks. The routine behind the API's
`sample_to_beat_time` and the engine's playback mapping were not located
(`0x103abc6e8` did not decompile). PRB-S8-08 measures it.

## Enumerations and setting domains

**Observed native ✓** (`0x1026a9ef8`, `0x1027b279c`, `0x1027b29e8`, `0x1026aa13c`;
defaults from the constructor `0x1027b0e40` and `getter-constants.txt`):

| Field | Codes and labels | Default |
| --- | --- | --- |
| `WarpMode` (stored list) | 0 Beats, 1 Tones, 2 Texture, 3 Re-Pitch, 4 Complex, 5 REX, 6 Complex Pro | Preference index mapped by table `0x105889f90` (0, 1, 2, 3, 4, 6) when a preferences object exists (`0x101849958`), else 0 |
| Display chooser (`DisplayWarpMode`, runtime only) | Beats, Tones, Texture, Re-Pitch, Complex, Complex Pro (no REX); short twin ends "Pro". 4- and 5-entry variants exist (`0x1026a9a08`, `0x1026a9820`); their selection was not traced | — |
| `TransientResolution` | 0 1 Bar, 1 1/2, 2 1/4, 3 1/8, 4 1/16, 5 1/32, 6 Transients | 6 |
| `TransientLoopMode` | 0 LoopOs, 1 LoopFwd, 2 LoopAlt; paired in the string table with Off, Loop Forward, Loop Back-and-Forth (inferred display labels) | 2 |

| UserFloat (UI label) | Constructor (min, max, default) |
| --- | --- |
| `GranularityTones` ("Granularity Tones") | 12, 100, 30 |
| `GranularityTexture` ("Granularity Texture") | 2, 263, 65 |
| `FluctuationTexture` ("Fluctuation Texture") | 0, 100, 25 |
| `TransientEnvelope` | 0, **1.0**, 100; its curve object gets 0–100 |
| `ComplexProFormants` ("Complex Pro spectral envelope factor") | 0, 100, 100 |
| `ComplexProEnvelope` ("Complex Pro spectral envelope order") | 8, 256, 128; integer-step curve |
| `RightTempo` (runtime only, not in documents) | 5, 999, 120 |

ASampleWarpProperties' constructor `0x102883578` (C1) uses the same getters and
defaults; its `IsWarped` default is false. The API setter `0x1033bded8` accepts only
modes from `0x1033be004`: {5} for REX-type samples and another list otherwise
("Invalid warp mode").

**Inferred from names only:** Beats uses the three transient settings, Tones uses
`GranularityTones`, Texture uses `GranularityTexture` and `FluctuationTexture`, and
Complex Pro uses the two `ComplexPro*` settings. The engine classes are
`OWarperBeats`, `OWarperTones`, `OWarperTexture`, `OWarperRePitch`, `OWarperElastique`,
`OWarperRex` and `OWarperUnWarped`. Which one serves Complex and Complex Pro, and what
the settings do to audio, were not traced.

## Candidate requirements for SPEC-WARP-MARKERS

Proposed. Feature FEAT-WARP, with FEAT-PERSISTENCE. "Shipped" means 12.4d1/12.1d1
content in the 12.4.3 bundle. "Static-derived" means traced in 12.4.3 code, not
observed running.

| ID | Statement | Evidence | Strength |
| --- | --- | --- | --- |
| WM-01 | Warp state is stored per AudioClip and per MultiSamplePart `SampleWarpProperties`, with the field set and classes above; the mode-texture field is `FluctuationTexture` | Schema 203/203 | Observed |
| WM-02 | `WarpMarkers` holds `<WarpMarker Id SecTime BeatTime/>` items with attribute values; `SecTime` is seconds from the sample start, `BeatTime` is clip beats | Registration ✓; documents; unit checks | Representation observed; units inferred |
| WM-03 | Marker values are written with the Double fixed-precision rule; DBL_MAX is written `Invalid`; Live-edited `BeatTime` lies on a 1/3,843,840-beat grid; `SecTime` is not rounded | 44,058/44,058; 22,029/22,029; setters ✓ | Static-derived; observed in shipped |
| WM-04 | `WarpMarker` and the AudioClip warp fields are unchanged from `8.1_220` to `12.0_12402`; `SampleWarpProperties` from `9.5_305`; `SamplesToAutoWarp` from `12.0_12119` | Schema evolution | Observed |
| WM-05 | Shipped marker lists are strictly increasing in `SecTime` and `BeatTime`; editing keeps beats non-decreasing; load-time handling of other orders is unknown | 10,250/10,250 lists; API ✓ | Observed and static; load unknown |
| WM-06 | Shipped AudioClips have ≥2 markers (warped or not); SampleWarpProperties may have 0 | Counts | Observed |
| WM-07 | An AudioClip with an empty `WarpMarkers` list fails to load (document-corrupt error, `Empty warp marker array.`); SampleWarpProperties have no such check | `0x1027c1c7c` ✓, `0x10288538c` ✓ | Static-derived; user-visible outcome unknown |
| WM-08 | The last marker is a shadow marker that Live places 1/32 beat after the last visible marker; its segment sets the tempo after that marker; the API cannot move or delete it | Native ✓; 2,869/2,878 and 7,313/7,372 | Static-derived and observed; other spacings are accepted in shipped files |
| WM-09 | Beat time is piecewise linear in sample time between markers, extended before the first marker with the first segment's slope and after the last with the shadow segment's slope; segment tempo = Δbeat / Δsec × 60 | `0x10261093c` ✓, `0x1027c724c` ✓, extrapolation 292/399 and 330/399 | Inferred; playback unverified |
| WM-10 | Missing `SecTime`/`BeatTime` load as DBL_MAX; missing settings keep the constructor defaults | `0x1026105ec` ✓, `0x1027b0e40` ✓ | Static-derived; effect unknown |
| WM-11 | Edits keep every segment tempo within 5–999 BPM and sample times within [0, sample length]; no load-time check was found | `0x1027afd40` ✓, `0x1033bf42c` ✓; shipped 100% | Static-derived (edit path) |
| WM-12 | `WarpMode` codes are 0 Beats, 1 Tones, 2 Texture, 3 Re-Pitch, 4 Complex, 5 REX, 6 Complex Pro; the user chooser omits REX; the default follows the preference map (0–4, 6) or 0 | `0x1026a9ef8` ✓, `0x1026aa13c` ✓, table | Static-derived |
| WM-13 | Out-of-range enum and setting values are stored on load without a check | Generic loader | Static-derived; downstream effect unknown |
| WM-14 | Setting codes, labels, ranges and defaults are as in the tables above | Constructor ✓, getters | Static-derived; TransientEnvelope max anomaly unresolved |
| WM-15 | `DefaultDuration` is sample frames and `DefaultSampleRate` Hz; unwarped clip loop fields are seconds; warped clip region fields are beats | 2,479/2,479; 292/399 | Inferred; unwarped `OutMarker` unit unknown |
| WM-16 | Audio output per warp mode is not specified here; compatibility needs measured comparison | — | Unknown |

Statically derived fixture expectations (document values only): Patience Suite Demo
"Vocal Main" → shadow tempo 167.0 BPM and `OutMarker` ≈ extrapolated sample end;
`Sample Reference.als` (SHA-256 `19d32f0f…3ce1`) → 2,479 unwarped clips whose
`LoopEnd` equals the sample length in seconds. Full hashes are in `inputs-documents.tsv`.

## Phase 4 probes

Each record in [probe-batch.json](../../analysis/ableton-live-12.4.3/r2/s8-warp-v1/probe-batch.json)
gives the question, the evidence, why static tracing is not enough, the minimal input,
the discriminating observation and a stop condition.

| Probe | Settles |
| --- | --- |
| PRB-S8-01 | Empty AudioClip marker list: error text and whether the set opens |
| PRB-S8-02 | A single-marker AudioClip: tempo, display and re-save |
| PRB-S8-03 | Out-of-order, inverted and equal-time markers |
| PRB-S8-04 | Missing `BeatTime` and `BeatTime="Invalid"` |
| PRB-S8-05 | `WarpMode` 5 on a WAV, 7 and −1 |
| PRB-S8-06 | Out-of-range settings, clamped or kept; the TransientEnvelope range |
| PRB-S8-07 | Shadow spacing other than 1/32 beat, kept or normalised |
| PRB-S8-08 | Rendered click times against the piecewise-linear prediction, inside and outside the markers |
| PRB-S8-09 | Units of unwarped `LoopEnd` and `OutMarker` |
| PRB-S8-10 | Defaults when settings are absent, and the Default Warp Mode preference |
| PRB-S8-11 | Per-mode renders kept for later candidate comparison |

Update 2026-10-17 from the [SPEC-WARP-MARKERS](../specs/warp-markers.md) draft (queries d7-0001 and
d7-0002, retained in `analysis/ableton-live-12.4.3/r2/d7-warp-v1/`): the conversion behind the
scripting interface's sample-to-beat and beat-to-sample calls is piecewise linear over the stored
marker list, extends the first segment before the first marker and the shadow segment from the
last visible marker on, and does not clamp. The mapping used for playback remains unknown
(PRB-S8-08).

## Unknowns

- The user-visible outcome of the empty-list error, and whether the post-load hook
  runs for every set load.
- Load behaviour for unordered, duplicate-time or single-marker lists, and for
  `Invalid` positions.
- The conversion routine itself (API and engine); the playback mapping is inferred.
- Effects of out-of-range `WarpMode` and setting values; whether any later setter
  clamps them; the TransientEnvelope range (0–1 in the remoteable, 0–100 in its curve
  and in shipped values).
- The meaning of `MarkersGenerated`, `SavedWarpMarkersForStretched`, `SamplesToAutoWarp`
  and `IsSongTempoLeader`; how the runtime members `DisplayWarpMode` and `RightTempo`
  are kept out of documents.
- The unit of `OutMarker` in unwarped clips (432 shipped values fit beats at the set tempo).
- Which engine warper serves Complex and Complex Pro, and every algorithmic detail.
- Migration of pre-`9.5_305` sampler warp data (translator `0x1014919c4`).

## Limitations

Static evidence only. A traced throw or store does not prove the path runs for a
given file. The AudioClip sample is dominated by `Sample Reference.als`, and no shipped
file is a 12.4.3 save. `FUN_` names are generated. Branches without ✓ come from C1
pseudocode. The schema order is by file name, not proven migration order.
