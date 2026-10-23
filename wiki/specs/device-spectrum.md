---
id: SPEC-DEVICE-SPECTRUM
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 2
target: Ableton Live 12 Suite 12.4.3
---

# Spectrum device

This is the canonical partial contract for `SURF-DEVICE-SPECTRUM` under
FEAT-DEVICES / FEAT-AUDIO in the [feature map](feature-map.md), following
[ADR 0005](../decisions/adr-0005-full-live-specification-coverage.md).
Inputs, controls, observable outputs and state are specified below; numerical
algorithms and unsupported lifecycle outcomes remain explicit gaps.

**D12 exact-target U:** D12 means the captured current official Version 12 manual,
not an observation of Live 12.4.3. Every D12 clause's exact-build applicability
is U. Dpkg means direct observation of retained files shipped in the target
package; it grades only stored bytes/values. No S or X audio/display claim is
made. U has no oracle and must never pass. All application cases are unexecuted.
This page is an analyst draft, not a released implementation input or complete
device specification. [Research and source limits](../research/device-audio-utilities.md)
own evidence synthesis; this page owns behavior.

The [device-chain/rack contract](device-racks.md) owns generic insertion,
reordering, activation, preset actions and deletion. [Set structure](live-set-structure.md)
and [ALS container](als-container.md) own their stated container/structure scopes;
their T1 device subset does not prove Spectrum save/reopen. [Automation](automation-envelopes.md)
owns its envelope representation/evaluation clauses, not untraced device scheduling.
[Mix graph](mix-graph.md) owns track routing/mixing. [Mixer values](mixer-values.md)
describes track faders; it does not supply this device's gain, pan or smoothing law.
The current-manual source does not settle platform differences, keyboard access,
permissions, recovery, latency or transport coupling beyond explicit clauses.

## Requirements

### REQ-DEVICE-SPECTRUM-001 — analysis and transparent audio

**D12.** Spectrum performs real-time analysis of incoming audio; its graph has vertical dB and horizontal frequency/pitch axes. It is a measurement tool and does not alter incoming audio. Graph refresh timing and audio-through precision/latency are U.

Evidence: `spectrum:B02`; [source locators](#analysis-only-evidence).

### REQ-DEVICE-SPECTRUM-002 — Block measurement size

**D12.** Block chooses the number of samples analyzed per measurement. Larger settings improve accuracy and increase CPU demand according to the manual. The supported sample-count list, FFT size mapping, overlap, zero padding and accuracy/CPU bounds are U.

Evidence: `spectrum:B03`; [source locators](#analysis-only-evidence).

### REQ-DEVICE-SPECTRUM-003 — analysis channel

**D12.** Channel selects analysis of left, right or both. The channel-combination algorithm, stereo summation/normalization and cancellation behavior of Both are U. This setting is not documented as changing audio output.

Evidence: `spectrum:B04, B02`; [source locators](#analysis-only-evidence).

### REQ-DEVICE-SPECTRUM-004 — Refresh

**D12.** Refresh controls how often analysis occurs. Faster response trades greater CPU use for accuracy in the manual’s description. Exact domain, units, scheduling, update quantization, hidden-view behavior and wall-clock versus transport coupling are U.

Evidence: `spectrum:B05`; [source locators](#analysis-only-evidence).

### REQ-DEVICE-SPECTRUM-005 — Avg

**D12.** Avg selects how many sample blocks are averaged for each display update. At one, each block is shown; larger values smooth the display over time. The domain, accumulation method, reset/priming, decibel-versus-linear averaging and weighting/window are U.

Evidence: `spectrum:B06`; [source locators](#analysis-only-evidence).

### REQ-DEVICE-SPECTRUM-006 — Graph

**D12.** Graph switches between a single interpolated line and discrete frequency bins. Interpolation, bin positions, pixel rendering and amplitude calibration are U.

Evidence: `spectrum:B07`; [source locators](#analysis-only-evidence).

### REQ-DEVICE-SPECTRUM-007 — maximum trace and reset

**D12.** Peak levels are retained until the song restarts. Max toggles display of accumulated maximum amplitude; when Max is enabled, clicking the display resets the maximum. Whether Max off clears accumulation, reset scope, restart event definition and reset timing are U.

Evidence: `spectrum:B02, B08`; [source locators](#analysis-only-evidence).

### REQ-DEVICE-SPECTRUM-008 — horizontal scaling

**D12.** Scale X offers linear, logarithmic and semitone. Logarithmic and semitone use the same scaling, with top legends in Hz or note names respectively. Exact axis domain, note tuning reference, legend rounding and sample-rate-dependent limits are U.

Evidence: `spectrum:B09`; [source locators](#analysis-only-evidence).

### REQ-DEVICE-SPECTRUM-009 — pointer readout

**D12.** Hovering the display shows a box with amplitude, frequency and note name at pointer location. This is a location readout, not a documented peak-picking or pitch-detector result. Units/rounding, off-graph behavior and frequency-to-note tie rules are U.

Evidence: `spectrum:B10`; [source locators](#analysis-only-evidence).

### REQ-DEVICE-SPECTRUM-010 — manual range navigation

**D12.** Range/Auto selects manual or automatic dynamic range. In Range mode, amplitude-legending drags scroll vertically and zoom horizontally; Range sliders set minimum/maximum amplitude shown. Slider domain, allowed ordering, zoom limits and gestures outside the legending are U.

Evidence: `spectrum:B10`; [source locators](#analysis-only-evidence).

### REQ-DEVICE-SPECTRUM-011 — Auto range

**D12.** Auto scales the display to incoming level; Range sliders and zooming are disabled. Algorithm, margins, hysteresis, decay and retained manual range are U.

Evidence: `spectrum:B10`; [source locators](#analysis-only-evidence).

### REQ-DEVICE-SPECTRUM-012 — display location

**D12.** The title-bar button or double-click in the display toggles graph placement between device chain and Live’s main window. Geometry, focus/selection, keyboard accessibility and view/preset retention are U.

Evidence: `spectrum:B11`; [source locators](#analysis-only-evidence).

### REQ-DEVICE-SPECTRUM-013 — target stored analysis state

**Dpkg.** Latest schema and eleven shipped Spectrum presets contain range/axis, analysis, Length, Window, channel, averaging and refresh fields. Window=3 is an observed stored code in these presets, not a named window function, selectable UI control, FFT kernel or mathematical law. Preset labels do not prove block counts or enum meanings.

Evidence: `PKG-SCHEMA:SpectrumAnalyzer; package-values.json device=Spectrum`; [source locators](#analysis-only-evidence).

### REQ-DEVICE-SPECTRUM-014 — numerical and lifecycle gaps

**U.** Exact 12.4.3 applicability of every D12 clause is U. FFT/window/kernel, dB normalization/floor, sample rates, latency, displayed numerical tolerances, silence/nonfinite handling, persistence, automation availability, undo/redo, cancellation, malformed state, engine/device failure and teardown have no target outcomes here.

Evidence: `No outcome evidence`; [source locators](#analysis-only-evidence).

## Acceptance cases

These finite scenarios have retained parameters in the
[case packet](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/spectrum-cases.json) and [signal definitions](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/fixture-signals.json).
A D12 case compares only its stated documented relation or UI state; it supplies
no sample/pixel/cents/time tolerance and cannot grade exact-target compatibility.
Dpkg cases compare exact retained XML values only. Cases marked U have no
expected outcome. Named neutral settings mean other switches off, normal stereo
channel mode, Gain displayed 0 dB, Balance centered and Width displayed 100%,
where those controls exist; this setup is a proposed probe configuration, not a
factory default or proven transparent processing chain. No UI image was inspected.

| Case | Requirements | Kind; setup and action | Expected / criterion | Evidence |
| --- | --- | --- | --- | --- |
| DSP-001 | 001 | positive: SIG-STEREO; Spectrum enabled. Capture audio before/after; inspect graph axes | Documented signal is unaltered; graph axes are dB and frequency/pitch. Numerical audio equality/latency U. | D12: `spectrum:B02` |
| DSP-002 | 002 | positive: SIG-STEREO. Select smallest and largest offered Block options | Each option represents a sample count per measurement; larger option is documented as higher accuracy/cost. Exact counts and measured cost U. | D12: `spectrum:B03` |
| DSP-003 | 003 | positive: SIG-STEREO. Choose Left, Right, then Both | Analysis target follows chosen channel; Both combination and spectral levels U. | D12: `spectrum:B04` |
| DSP-004 | 004 | positive: SIG-STEREO. Choose two offered Refresh values | Refresh changes analysis frequency; exact units and observed cadence U. | D12: `spectrum:B05` |
| DSP-005 | 005 | boundary: SIG-BURST. Set Avg 1 | Each block is shown according to manual; precise timing and priming U. | D12: `spectrum:B06` |
| DSP-006 | 005 | positive: SIG-BURST. Compare Avg 1 with a larger offered value | Larger Avg smooths the display over time; averaging law and tolerance U. | D12: `spectrum:B06` |
| DSP-007 | 006 | positive: SIG-STEREO. Toggle Graph | View switches between interpolated line and discrete bins. | D12: `spectrum:B07` |
| DSP-008 | 007 | positive: SIG-BURST; Max enabled. Allow peak then lower input level | Accumulated maximum is shown and retained; calibration/decay law U. | D12: `spectrum:B02, B08` |
| DSP-009 | 007 | positive: A retained maximum; Max enabled. Click display | Maximum amplitude is reset; first post-reset measurement and sample timing U. | D12: `spectrum:B08` |
| DSP-010 | 007 | boundary: A retained maximum. Restart song | Peak retention ends on restart according to manual; exact restart gesture/event is ungraded. | D12: `spectrum:B02` |
| DSP-011 | 007 | positive: Max visible. Toggle Max off | Display of maximum is toggled off; accumulation retention U. | D12: `spectrum:B08` |
| DSP-012 | 008 | positive: SIG-STEREO. Cycle Linear, Logarithmic, Semitone Scale X | Three modes are offered; Logarithmic and Semitone share scaling, with Hz versus note legends. | D12: `spectrum:B09` |
| DSP-013 | 009 | positive: Graph visible. Hover a fixed interior location | Box reports amplitude, frequency and note at pointer location. Numerical rounding U. | D12: `spectrum:B10` |
| DSP-014 | 010 | positive: Range mode; graph visible. Drag amplitude legend vertically, then horizontally | Vertical motion scrolls amplitude; horizontal motion zooms. | D12: `spectrum:B10` |
| DSP-015 | 010 | positive: Range mode. Change minimum and maximum Range sliders | Displayed amplitude range follows sliders; valid ordering and numerical bounds U. | D12: `spectrum:B10` |
| DSP-016 | 011 | negative: Auto mode selected. Attempt Range-slider editing and amplitude zoom | Range sliders and zooming are disabled. | D12: `spectrum:B10` |
| DSP-017 | 011 | positive: SIG-LEVEL-STEP; Auto mode. Change input level | Display automatically scales with input level; margins/settling U. | D12: `spectrum:B10` |
| DSP-018 | 012 | positive: Display in device chain. Click title-bar display button twice | Display toggles to main window then device chain. | D12: `spectrum:B11` |
| DSP-019 | 012 | positive: Display in device chain. Double-click display twice | Display toggles between same two locations. Max-click interaction U. | D12: `spectrum:B11` |
| DSP-020 | 013 | file observation: Retained Accurate Fast.adv. Decode XML | Length=3, Window=3, ChannelMode=2, NumAverages=3, MinRefreshTime=40; no enum/kernel/units assertion. | Dpkg: `package/Spectrum/Accurate Fast.adv:.//SpectrumAnalyzer` |
| DSP-021 | 013 | file observation: Retained Spectrum.adv. Decode XML | Length=2, Window=3, NumAverages=1, MinRefreshTime=100, ScaleXMode=1; saved settings, not factory default proof. | Dpkg: `package/Spectrum/Spectrum.adv:.//SpectrumAnalyzer` |
| DSP-022 | 014 | negative: SIG-SILENCE. Inspect dB floor, automatic range and maxima | Unknown; no oracle, do not grade. | U: `U` |
| DSP-023 | 014 | boundary: SIG-IMPULSE and off-bin sine. Measure all offered Block sizes/refresh/Avg endpoints | Unknown; no oracle, do not grade. | U: `U` |
| DSP-024 | 014 | malformed: Copy of Spectrum preset. Set Length=99, Window=99, NumAverages=0 and MinRefreshTime=-1 separately | Unknown; no oracle, do not grade. | U: `U` |
| DSP-025 | 014 | error: Range editing. Enter inverted bounds, NaN and inf where editable | Unknown; no oracle, do not grade. | U: `U` |
| DSP-026 | 014 | cancel: Manual range text edit/menu active. Type change then Escape; dismiss context menu | Unknown; no oracle, do not grade. | U: `U` |
| DSP-027 | 014 | undo: Known graph, Avg and Range state. Change settings; Undo/Redo each | Unknown; no oracle, do not grade. | U: `U` |
| DSP-028 | 014 | persistence: Nondefault Block/Window/channel/range/Max/Avg/Refresh and expanded display. Save Set and preset; reopen; compare settings and peak history | Unknown; no oracle, do not grade. | U: `U` |
| DSP-029 | 014 | teardown: Streaming audio with expanded display. Delete Spectrum; Undo; disable/re-enable audio engine; close Set | Unknown; no oracle, do not grade. | U: `U` |
| DSP-030 | 014 | timing: SIG-BURST. Change sample rate/block size; stop/start/locate transport; hide device view | Unknown; no oracle, do not grade. | U: `U` |
| DSP-031 | 014 | numerical: SIG-440, SIG-IMPULSE and SIG-NOISE. Measure bin centers, normalization, window, FFT resolution and numerical output | Unknown; no oracle, do not grade. | U: `U` |
| DSP-032 | 014 | channel: SIG-ANTIPHASE. Compare Both with Left and Right analysis | Unknown; no oracle, do not grade. | U: `U` |
| DSP-033 | 014 | interaction: Max enabled; expanded Spectrum. Double-click display and compare maximum resets with single click | Unknown; no oracle, do not grade. | U: `U` |
| DSP-034 | 014 | automation: Spectrum with parameter mapping/automation lists. Enumerate exposed controls; automate any supported analysis control; cancel edit | Unknown; no oracle, do not grade. | U: `U` |

Historical R1 counts: 14 requirements; 34 scenarios: 19 D12
(documentary relationships, exact-target U), 2 Dpkg (stored-file
observations only), 13 U (ungraded). Zero target application executions,
zero target audio/display acceptance passes. Supported and unknown clauses may
coexist in a requirement; the labels do not promote its unknown parts.

Positive, negative, boundary, malformed/error, cancel, undo, persistence, timing
and teardown cases are explicit. File/device errors are distinct from valid audio
input outside an analyzer's intended signal class. No asynchronous cancelable
operation is documented for these controls; Escape/edit/menu cases remain U,
rather than inventing a new cancel workflow. State ownership on view change,
transport restart, preset replacement, Set close and engine suspension remains
unknown except the documentary clauses named above. Unknowns keep full-device
coverage open and are not exclusions from the whole-product target.

## Revision 2 bounded acceptance additions

The [current R2 catalogs](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/cases-r2.json) retain every original requirement and case record except the two explicitly appended Utility contract qualifiers. This page's original case table and historical counts describe R1. Current Spectrum: 14 requirements, 36 cases; 21 D12, 2 retained-file-only Dpkg and 13 U.

New cases add actual guarded histories rather than treating old endpoint, button or flag actions as broader evidence. Every new documentary and actual expected/comparison field is null; source claims are descriptions, not detector, signal, timing or numerical oracles. All application outcomes remain exact-target U and unexecuted. Six historical file grades across the family are preserved, not rerun or promoted to application evidence.

- `DSP-035` (UAS-G07): Genuinely usable NONZERO incoming analysis through an admitted active stream, not AnalyzeOn flags alone; independently reset manual/Auto histories. Explicitly select Range. Successfully operate BOTH minimum and maximum Range sliders and independently observe changed displayed range; drag amplitude legending vertically to scroll and horizontally to zoom and observe successful manual zoom. THEN select Auto and attempt those same Range sliders AND zoom. Separately change admitted nonzero incoming level under Auto and record ungraded scaling observations. Do not treat flags or mere control presence as productive manual history. Source: `spectrum:B10`.

- `DSP-036` (UAS-G08): Admitted active NONZERO analysis; Max enabled with a genuinely visible accumulated nonzero maximum independently observed BEFORE each clearing/visibility contrast. Create and actually observe retained maximum history, lower input, then click display with Max enabled. Rebuild and observe a fresh genuine maximum before a separately independently admitted song-restart event; if its UI route/event is not established keep that branch U, never substitute guessed transport stop/start. Rebuild visible history before toggling Max off; record visibility separately from unknown accumulation retention. Preserve DSP-033 single/double-click interaction as U and both DSP-018/019 display routes unchanged. Source: `spectrum:B02, B08; DSP-033 interaction U`.

[R2 delta and disposition](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/delta-r2.json) records all nine audit groups and remaining limits. AS-OF AUTHOR FREEZE: independent review pending; current disposition is routed through the [shared spec index](index.md). This is partial adoption, with zero complete device profiles.

## Analysis-only evidence

Source `D12-AUDIO-EFFECTS`: [official current manual](https://www.ableton.com/en/live-manual/12/live-audio-effect-reference/#spectrum),
captured 2026-10-19 as [retained HTML](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/manual-audio-effects-2026-10-19.html).
[Block locators](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/manual-spectrum-blocks.json) retain h2/h3 anchors, paragraph
kind, exact HTML line and text; [readable extract](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/manual-spectrum.txt).
`spectrum:Bnn` points to that numbered block; ranges are inclusive.
The source says Version 12, without a 12.4.3 publication pin.

`PKG-SCHEMA` is the [retained latest shipped schema](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/12.0_12402.txt);
[filtered fields](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/schema-fields.json) retain class start lines.
[Package values](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/package-values.json) retain XML locators, historical
Creator/revision, and exact values. [Source identity manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/sources.json)
pins URL/path, capture date, byte size and SHA-256 for the HTML, schema and each
shipped file. [Frozen author manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/manifest-author-r1.json) pins this
specification revision and packet for separate review. These are source/file
observations, not runtime validation, a read/write guarantee or host topology.

## Revision history

| Revision | Date | Change |
| --- | --- | --- |
| 1 | 2026-10-19 | First bounded F-06 Spectrum contract; documentary/file-only evidence and finite ungraded lifecycle/numerical probes |

| 2 | 2026-10-19 | Bounded source-audit qualifiers and guarded acceptance histories; original R1 cases preserved |
