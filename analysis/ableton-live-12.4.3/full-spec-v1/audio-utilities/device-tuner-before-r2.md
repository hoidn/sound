---
id: SPEC-DEVICE-TUNER
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3
---

# Tuner device

This is the canonical partial contract for `SURF-DEVICE-TUNER` under
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
their T1 device subset does not prove Tuner save/reopen. [Automation](automation-envelopes.md)
owns its envelope representation/evaluation clauses, not untraced device scheduling.
[Mix graph](mix-graph.md) owns track routing/mixing. [Mixer values](mixer-values.md)
describes track faders; it does not supply this device's gain, pan or smoothing law.
The current-manual source does not settle platform differences, keyboard access,
permissions, recovery, latency or transport coupling beyond explicit clauses.

## Requirements

### REQ-DEVICE-TUNER-001 — measurement input and transparent output

**D12.** Analyze incoming monophonic pitch and its distance from the nearest semitone. Tuner is a measurement device and does not alter the incoming audio. Clean monophonic signals are the intended input; polyphonic, noisy or harmonically rich inputs may give inaccurate results. No error or polyphonic-detection fallback is promised.

Evidence: `tuner:B02–B03`; [source locators](#analysis-only-evidence).

### REQ-DEVICE-TUNER-002 — view switching and tuning color

**D12.** The lower-left view buttons switch between Classic and Histogram views. Both use green for in tune and red for out of tune. Detection/green thresholds, hysteresis, intermediate colors and hold time are U.

Evidence: `tuner:B05`; [source locators](#analysis-only-evidence).

### REQ-DEVICE-TUNER-003 — Classic display

**D12.** Classic View shows a colored ball along a curve, the nearest detected note name in the center, and side arrows indicating whether tuning must move up or down. Exact note/octave spelling, pixels, ball displacement law and arrow thresholds are U.

Evidence: `tuner:B07`; [source locators](#analysis-only-evidence).

### REQ-DEVICE-TUNER-004 — Target Mode direction

**D12.** Target Mode has a central outline for desired pitch. The signal is in tune when the ball lies exactly within the outline; a sharp signal appears to its right, a flat signal to its left. This describes display semantics, not a quantified accepted cents band.

Evidence: `tuner:B08`; [source locators](#analysis-only-evidence).

### REQ-DEVICE-TUNER-005 — Strobe Mode

**D12.** Strobe Mode replaces the curve with a rotating light band. Rightward rotation means sharp; leftward means flat; a greater detuning makes the band move faster. Rotation speed, reference tolerance and freeze behavior are U.

Evidence: `tuner:B09`; [source locators](#analysis-only-evidence).

### REQ-DEVICE-TUNER-006 — Hertz and cents readout

**D12.** A switch selects incoming absolute frequency in Hz or distance from target in cents, and is visible in both Classic and Histogram views. Exact rounding, displayed precision, cents conversion, note-boundary tie handling and octave labeling are U.

Evidence: `tuner:B10, B14`; [source locators](#analysis-only-evidence).

### REQ-DEVICE-TUNER-007 — Histogram

**D12.** Histogram shows pitch over time and note names on its right scale. Horizontal gray lines indicate in-tune note centers; sharp notes lie above their lines and flat notes below. History length, vertical units, update cadence and handling of missing detections are U.

Evidence: `tuner:B12`; [source locators](#analysis-only-evidence).

### REQ-DEVICE-TUNER-008 — Histogram navigation and Auto

**D12.** Dragging vertically scrolls pitches; dragging horizontally zooms. Auto centers the display on incoming pitch. Auto/manual precedence, zoom limits and view-state retention are U.

Evidence: `tuner:B13`; [source locators](#analysis-only-evidence).

### REQ-DEVICE-TUNER-009 — note spelling menu

**D12.** Right-clicking anywhere within the view exposes three spelling choices: sharps, flats, or sharps and flats. Spelling changes labels; no pitch-processing change is documented. Exact key- or tuning-system-dependent enharmonic selection is U.

Evidence: `tuner:B16–B19`; [source locators](#analysis-only-evidence).

### REQ-DEVICE-TUNER-010 — reference pitch

**D12.** Reference changes the tuning reference used to analyze input; documented default is 440 Hz with an adjustable domain 410–480 Hz. Exact increment, text parsing, runtime default corroboration, reference convention under nonstandard tuning systems and output indication tolerances are U.

Evidence: `tuner:B21`; [source locators](#analysis-only-evidence).

### REQ-DEVICE-TUNER-011 — target persisted fields

**Dpkg.** The retained Tuner schema and Guitar Recording template show tuning frequency, view/readout/strobe state, histogram state, accidental spelling and IgnoreTuningSystem. The historical template stores TuningFreq/Manual=440. This is a saved example, not a 12.4.3 constructor/default or tuning-system behavioral contract.

Evidence: `PKG-SCHEMA:Tuner; package-values.json device=Tuner`; [source locators](#analysis-only-evidence).

### REQ-DEVICE-TUNER-012 — unresolved detection and lifecycle

**U.** Exact 12.4.3 applicability of every D12 clause remains U. Pitch algorithm, supported frequency/level/sample-rate range, confidence, silence/noise/polypitch fallback, latency, channel combination, transients, tuning-system interaction, persistence, automation, undo, cancellation, invalid files and teardown are unknown. No zero-cent or note-accuracy tolerance is invented.

Evidence: `No outcome evidence`; [source locators](#analysis-only-evidence).

## Acceptance cases

These finite scenarios have retained parameters in the
[case packet](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/tuner-cases.json) and [signal definitions](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/fixture-signals.json).
A D12 case compares only its stated documented relation or UI state; it supplies
no sample/pixel/cents/time tolerance and cannot grade exact-target compatibility.
Dpkg cases compare exact retained XML values only. Cases marked U have no
expected outcome. Named neutral settings mean other switches off, normal stereo
channel mode, Gain displayed 0 dB, Balance centered and Width displayed 100%,
where those controls exist; this setup is a proposed probe configuration, not a
factory default or proven transparent processing chain. No UI image was inspected.

| Case | Requirements | Kind; setup and action | Expected / criterion | Evidence |
| --- | --- | --- | --- | --- |
| DTU-001 | 001 | positive: SIG-440; Tuner enabled. Capture audio before/after Tuner | Incoming audio is unaltered according to manual; bit identity, delay compensation and numerical tolerance require target evidence. | D12: `tuner:B03` |
| DTU-002 | 001, 003, 010 | positive: SIG-440; reference 440 Hz, standard tuning. Select Classic View | Display represents detected monophonic pitch and nearest semitone; A note class is the intended documentary case. Octave label, measured Hz and green threshold U. | D12: `tuner:B02, B07, B21` |
| DTU-003 | 002 | positive: Classic View visible. Click Histogram then Classic view buttons | Views switch; each supports the documented tuning color semantics. | D12: `tuner:B05` |
| DTU-004 | 004 | positive: SIG-SHARP; reference 440 Hz, standard tuning. Use Classic Target Mode | Detected sharp signal appears to right of target; precise position and cent tolerance U. | D12: `tuner:B08` |
| DTU-005 | 004 | positive: SIG-FLAT; reference 440 Hz, standard tuning. Use Classic Target Mode | Detected flat signal appears to left of target; precise position U. | D12: `tuner:B08` |
| DTU-006 | 005 | positive: SIG-SHARP. Select Strobe Mode | Curve becomes a band moving right for a detected sharp pitch. | D12: `tuner:B09` |
| DTU-007 | 005 | positive: SIG-FLAT. Select Strobe Mode | Band moves left for a detected flat pitch. | D12: `tuner:B09` |
| DTU-008 | 005 | boundary: SIG-SHARP then SIG-SHARP-WIDE. Observe same note target in Strobe Mode | Greater detuning makes motion faster; no numerical rate/latency threshold. | D12: `tuner:B09` |
| DTU-009 | 006 | positive: Classic View; SIG-440. Toggle Hertz/Cents | Readout changes between frequency Hz and distance from target cents. Numerical rounding U. | D12: `tuner:B10` |
| DTU-010 | 006 | positive: Histogram View; SIG-440. Toggle Hertz/Cents | Same unit choice is available in Histogram View. | D12: `tuner:B14` |
| DTU-011 | 007 | positive: Histogram View; SIG-SHARP then SIG-FLAT. Observe detected traces | Sharp trace is above its note-center line; flat trace below. Time/history precision U. | D12: `tuner:B12` |
| DTU-012 | 008 | positive: Histogram Auto off. Drag up/down, then horizontally | Vertical drag scrolls pitches; horizontal drag zooms. Extents U. | D12: `tuner:B13` |
| DTU-013 | 008 | positive: Histogram View; SIG-440 then SIG-880. Enable Auto | Display adjusts to center the incoming pitch. Center tolerance and speed U. | D12: `tuner:B13` |
| DTU-014 | 009 | positive: View display with detected accidental note. Right-click view; select each spelling option | Menu offers sharps, flats, combined sharps/flats; labels reflect chosen notation. Exact glyph sequence U. | D12: `tuner:B16–B19` |
| DTU-015 | 010 | boundary: Reference control available. Set 410, 440 and 480 Hz | All three reference values are within documented domain. Detection calibration at each setting U. | D12: `tuner:B21` |
| DTU-016 | 011 | file observation: Retained Guitar Recording.als. Decode Tuner XML | TuningFreq/Manual=440, ViewMode=0, StrobeMode=false, DisplayPitchInHz=false, HistogramFollowsPitch=true, IgnoreTuningSystem=false. No enum semantics asserted. | Dpkg: `package/Tuner/Guitar Recording.als:.//Tuner` |
| DTU-017 | 012 | negative: SIG-POLY. Analyze two simultaneous independent tones | Unknown; no oracle, do not grade. | U: `tuner:B03 (only accuracy warning)` |
| DTU-018 | 012 | negative: SIG-SILENCE then SIG-NOISE. Observe no-pitch state and history | Unknown; no oracle, do not grade. | U: `U` |
| DTU-019 | 012 | boundary: SIG-TIE. Sweep across a half-semitone boundary | Unknown; no oracle, do not grade. | U: `U` |
| DTU-020 | 012 | boundary: Reference 410 Hz then 480 Hz. Attempt 409.9 and 480.1 Hz through keyboard/text | Unknown; no oracle, do not grade. | U: `U` |
| DTU-021 | 012 | malformed: Reference text editor. Enter NaN, inf and abc; submit | Unknown; no oracle, do not grade. | U: `U` |
| DTU-022 | 012 | error: Copy of saved Tuner template. Remove TuningFreq; use invalid ViewMode and reference −1 | Unknown; no oracle, do not grade. | U: `U` |
| DTU-023 | 012 | cancel: Reference edit active. Type 442 then Escape; dismiss spelling context menu with Escape | Unknown; no oracle, do not grade. | U: `U` |
| DTU-024 | 012 | undo: Reference 440; Classic view. Change reference and view; Undo/Redo | Unknown; no oracle, do not grade. | U: `U` |
| DTU-025 | 012 | persistence: Nondefault reference, strobe, units, histogram and spelling. Save/reopen Set; inspect each setting and history retention | Unknown; no oracle, do not grade. | U: `U` |
| DTU-026 | 012 | teardown: Tuner analyzes audio. Delete/reinsert; suspend audio engine; remove input source | Unknown; no oracle, do not grade. | U: `U` |
| DTU-027 | 012 | timing: SIG-440 begins at frame 4800. Measure first detection at rates 44100, 48000, 96000 and blocks 64,512 | Unknown; no oracle, do not grade. | U: `U` |
| DTU-028 | 012 | tuning system: SIG-440; nondefault Set tuning system. Toggle IgnoreTuningSystem in an evidence-supported UI route if found; compare reference/notes | Unknown; no oracle, do not grade. | U: `U` |
| DTU-029 | 012 | automation: Reference pitch automation where exposed. Automate 440→442, override then re-enable | Unknown; no oracle, do not grade. | U: `U` |
| DTU-030 | 012 | channel: Left-only and right-only monophonic inputs, then opposite-polarity stereo. Observe pitch detection and through audio | Unknown; no oracle, do not grade. | U: `U` |
| DTU-031 | 012 | boundary: SIG-LEVEL-SWEEP and SIG-FREQ-SWEEP. Measure detection limits, confidence and in-tune color threshold | Unknown; no oracle, do not grade. | U: `U` |
| DTU-032 | 012 | numeric: SIG-440 and SIG-SHARP. Record measured frequency/cents at every displayed precision | Unknown; no oracle, do not grade. | U: `U` |

Counts: 12 requirements; 32 scenarios: 15 D12
(documentary relationships, exact-target U), 1 Dpkg (stored-file
observations only), 16 U (ungraded). Zero target application executions,
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

## Analysis-only evidence

Source `D12-AUDIO-EFFECTS`: [official current manual](https://www.ableton.com/en/live-manual/12/live-audio-effect-reference/#tuner),
captured 2026-10-19 as [retained HTML](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/manual-audio-effects-2026-10-19.html).
[Block locators](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/manual-tuner-blocks.json) retain h2/h3 anchors, paragraph
kind, exact HTML line and text; [readable extract](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/manual-tuner.txt).
`tuner:Bnn` points to that numbered block; ranges are inclusive.
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
| 1 | 2026-10-19 | First bounded F-06 Tuner contract; documentary/file-only evidence and finite ungraded lifecycle/numerical probes |
