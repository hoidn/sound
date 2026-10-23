---
id: RESEARCH-DEVICE-AUDIO-UTILITIES
type: research
status: current
updated: 2026-10-19
access: analysis
revision: 2
target: Ableton Live 12 Suite 12.4.3
---

# Utility, Tuner and Spectrum evidence

F-06 now has separate canonical behavioral owners for
[Utility](../specs/device-utility.md), [Tuner](../specs/device-tuner.md) and
[Spectrum](../specs/device-spectrum.md). This page owns evidence synthesis,
source identity and limits. The device specs own the contracts. No device is
complete and no application, original function or candidate was executed.

**D12 exact-target U:** the current official Version 12 manual is documentary
support for the described interface/behavior, not proof of 12.4.3 applicability.
The installed schema and historical presets establish target-package fields and
saved values; they do not promote manual DSP or display clauses to S or X.
There is no numerical audio, pitch, display or timing compatibility oracle here.

## Captures and exact locators

`D12-AUDIO-EFFECTS` is the official
[Live Audio Effect Reference](https://www.ableton.com/en/live-manual/12/live-audio-effect-reference/),
captured 2026-10-19, page title Version 12, no exact publication/build revision.
[Retained HTML](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/manual-audio-effects-2026-10-19.html)
is 588,328 bytes, SHA-256
`9cb15cb3d80bda4771e5add2c2b74f5c57d73ee8850e198acf7cf8a51dfd1299`.
The [source manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/sources.json)
records exact URL/path, date, SHA-256 and size for all 24 sources: HTML, schema,
10 Utility presets, 11 Spectrum presets and the Guitar Recording template.
The [capture extractor](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/capture.py)
uses Python standard-library HTTP/HTML/gzip/XML handling and refuses changed
capture overwrites; it runs no original code. Figures were not inspected.

| Source section | Exact retained locator | What it supports |
| --- | --- | --- |
| `#utility`, h2 29.40 | HTML line 2218; [14 blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/manual-utility-blocks.json), `utility:B01–B14` | Documentary control relationships and stated domains; no kernel, precision or smoothing |
| `#tuner`, h2 29.39 | HTML line 2134; [21 blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/manual-tuner-blocks.json), `tuner:B01–B21` | Documentary monophonic analysis, transparent signal, views/reference/readout; no detection algorithm/tolerance |
| Tuner h3 anchors | `#view-switches` line 2146, `#classic-view` line 2158, `#histogram-view` line 2182, `#note-spellings` line 2194, `#reference-slider` line 2206 | Stable h3 routing in captured HTML; paragraph blocks retain separate start lines |
| `#spectrum`, h2 29.38 | HTML line 2108; [11 blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/manual-spectrum-blocks.json), `spectrum:B01–B11` | Documentary analysis/display controls and transparent signal; no FFT, latency, window or dB calibration |
| `PKG-SCHEMA` | [Latest shipped schema](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/12.0_12402.txt): `SpectrumAnalyzer` lines 7476–7510; `StereoGain` 7515–7553; `Tuner` 8236–8267 | Stored field declarations; no constructor defaults, permitted ranges or runtime behavior |

The copied schema is 441,285 bytes, SHA-256
`b7c9d4c767d8ca9b346ce7d517265446bbacd6de366cc058e155613789d0f299`.
Its source is the inventory's retained exact copy of installed
`Contents/App-Resources/Schema/12.0_12402.txt`. The inventory's
[device aliases](../../analysis/ableton-live-12.4.3/full-spec-v1/inventory/devices.json)
map Utility→StereoGain, Tuner→Tuner, Spectrum→SpectrumAnalyzer by named preset/template
roots plus package directories. The new packet retains the actual compressed
file bytes as well as [parsed values](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/package-values.json).

## Observed target-package state

All 22 retained documents identify Creator `Ableton Live 12.4d1`,
`MinorVersion="12.0_12402"`, revision
`42bc084cd8152e4fb737ef3fefd04b2bea5320e7`. They are historical content shipped
inside 12.4.3, not saves observed from the target application. Parsing succeeded
for all 22; each has one occurrence of the intended device class.

[Schema fields](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/schema-fields.json)
retain full class declarations and line numbers. The following selection separates
saved vocabulary from behavioral meaning:

| Device | Exact stored observations | Limit |
| --- | --- | --- |
| Utility | `PhaseInvertL/R`, `ChannelMode`, `StereoWidth`, `MidSideBalance`, `MidSideBalanceOn`, `Mono`, `BassMono`, `BassMonoAudition`, `BassMonoFrequency`, `Balance`, `Gain`, `LegacyGain`, `Mute`, `DcFilter`, `LegacyMode` | Field types include timeable versus remoteable, but do not prove automation UI, live interpolation or coupling |
| Utility presets | `Bass Mono.adv`: BassMono=true, frequency=120, Gain=1. `Left.adv`: ChannelMode=0; `Right.adv`: 2. `Phase Invert.adv`: both phase flags true. `Mid Only.adv`/`Sides Only.adv`: MidSideBalanceOn=true, MidSideBalance=0/2 respectively | Filename/value association is observed; enum map, normalization and actual sound are not |
| Utility historical state | All ten have LegacyMode=false. Difference.adv has Gain=2.61015725 and LegacyGain=8.33333302; other selected presets often have Gain=1 and LegacyGain=0 | No conversion law or migration branch is inferred from these paired values |
| Tuner template | ViewMode=0, TuningFreq/Manual=440, DisplayPitchInHz=false, StrobeMode=false, HistogramCenterNote=0, HistogramNoteRange=3.5, HistogramFollowsPitch=true, AccidentalSpelling=0, IgnoreTuningSystem=false | A saved 440 example corroborates vocabulary, not the documented default constructor or tuning-system behavior |
| Spectrum presets | All eleven have Window=3, AnalyzeOn=true, ChannelMode=2, AutoScaleY=true, ShowMax=true. Length codes seen: 0,1,2,3; ScaleXMode: 0,1,2; NumAverages: 1,2,3,4,6,8; MinRefreshTime: 40,80,100,198,200 | Observed values are not legal domains, units, Block counts, channel enum mapping or timing measurements |
| Spectrum hidden vocabulary | Window, AnalyzeOn and the full retained range/analysis fields appear in the schema | The manual does not establish a user-selectable window control or what Window=3 means |

## Evidence discipline and interactions

[Track mixer values](mixer-values.md) and [mix graph](mix-graph.md) are canonical
for their track/engine scopes. No traced caller path connects their fader curves,
silence floor, pan matrix or ramps to Utility's StereoGain control in this packet.
Reusing their mathematics would therefore invent device signal behavior. The
three new contracts explicitly leave gain/pan/mono normalization, filter response,
control ordering and smoothing unknown.

For Tuner, the manual supplies orientation and readout meaning. It does not give
pitch estimator, note-boundary ties, frequency/amplitude validity range, silence
state, confidence, cent/color thresholds, Hz rounding or acquisition latency.
The target's IgnoreTuningSystem field creates a concrete unresolved interaction
with Set tuning; its name alone supplies no semantics.

For Spectrum, Block/Avg/Refresh descriptions do not prove an FFT implementation,
window family, overlap, zero padding, amplitude normalization, effective latency
or averaging in linear magnitude versus power versus dB. Both-channel combination
and peak-history persistence/reset event details remain unknown. Window=3 is
specifically not a recovered window law.

The [device/rack draft](../specs/device-racks.md) owns generic host actions;
[Set structure](../specs/live-set-structure.md) owns its narrower T1 structure.
Neither makes these devices part of its released device subset. Save/reopen,
malformed state, undo/redo, cancellation, transport, automation, source/device
failure and teardown receive finite U cases in each device packet. Platform
accessibility/permissions remain cross-feature gaps; no figure inspection, binary
search or broad native analysis was performed solely to expand documentation.

## Packet and review boundary

| Device | Requirements | D12 cases, target U | Dpkg file-only cases | U cases | Total |
| --- | ---: | ---: | ---: | ---: | ---: |
| Utility | 15 | 22 | 3 | 12 | 37 |
| Tuner | 12 | 15 | 1 | 16 | 32 |
| Spectrum | 14 | 19 | 2 | 13 | 34 |
| Total | 41 | 56 | 6 | 41 | 103 |

[Finite signal definitions](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/fixture-signals.json)
are analyst probe parameters, not generated audio or reference outputs.
[Utility cases](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/utility-cases.json),
[Tuner cases](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/tuner-cases.json)
and [Spectrum cases](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/spectrum-cases.json)
retain requirement IDs, setup/actions/parameters, stated oracle or null, provenance,
comparison scope and unexecuted status. A D12 case is documentary only; a Dpkg
case can confirm retained file contents, never application acceptance or sound.

The [frozen author manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/manifest-author-r1.json)
pins source/spec/research/fixture bytes for independent review. Root owns shared
index, inventory routing, coverage, questions and append-only log integration.
This packet is a partial draft submitted for independent review; a review cannot
turn unknown numerical/lifecycle behavior into supported behavior.

## Revision 2 source-audit adoption

The independently approved full selected-section audit assessed 46 blocks and 101 qualified judgments, not the complete Audio Effects chapter or all device behavior. [Current R2 catalogs](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/cases-r2.json) preserve all 103 R1 cases verbatim and append nine bounded histories: four Utility, three Tuner, two Spectrum. Current totals: 41 requirement IDs, 112 cases (63 D12 documentary, six historical Dpkg file-only, 43 U); every application outcome remains target U/unexecuted. The original tables/counts above describe R1. No file grade is reexecuted.

Only Utility 005 and 013 append source qualifiers: continuous 0-to-100M controller context, and relevant low/DC content PLUS nonlinear processing AFTER Utility as a necessary, not sufficient, sonic condition. No exact DSP, interpolation, detector, FFT/window-3, color threshold, pixel, CPU or timing law follows. The [nine-group ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/delta-r2.json) maps actual guarded actions and retained subsets. All nine new documentary/actual expected and comparison fields are null; their source claims do not grade outcomes.

Both Width AND Mid/Side must be genuinely productive before Left/Right no-function contrasts; sustained NONZERO downstream tails precede Mute; DC requires known low/DC plus productive downstream nonlinear processing, without promised audibility. Tuner colors in BOTH views, Classic arrows and in-tune Target require genuinely accepted monophonic contexts, not inferred frequency truth. Independent positive detection precedes unsupported-input absence/negative histories. Spectrum requires actual manual Range AND zoom before Auto, and genuinely visible maximum history before each clear/restart contrast. Both units/views and both display routes remain preserved. Song-restart route and Max double-click interaction stay U.

Selected S06 FAQ states as of Live 12.1 that Tuner's reference follows selected tuning. This remains a separately guarded U probe: IgnoreTuningSystem has a UI action only IF independently found; TUN-015 is external MPE-receiver configuration and gives no Tuner result. The three audit questions, full lifecycle/algorithm gaps and exact 12.4.3 applicability remain open. Source date-only capture has unknown UTC; images and destinations were not inspected.

[Preservation and historical consumer inventory](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/consumer-history-r2.json) retains old exact canonical providers and qualified pointers. They are as-of contexts, not mutable live gates; old validators/reviews remain historical and were not replayed. [R2 manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/manifest-author-r2.json) seals current owner evidence/delta. AS-OF AUTHOR FREEZE: independent review pending; current disposition is routed through the shared research/spec indexes. No runtime execution, coverage completion or handoff release.
