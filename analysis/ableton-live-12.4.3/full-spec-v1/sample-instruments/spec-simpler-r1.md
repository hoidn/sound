---
id: SPEC-DEVICE-SIMPLER
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3
---

# Simpler sample-instrument behavior

## Scope and evidence rules

Owns `SURF-DEVICE-SIMPLER` in [the product inventory](../research/full-live-coverage-inventory.md).
This is a **partial draft**, not a released contract or a complete instrument family.
Requirements marked **D** describe the captured current Live 12 manual; **U** identifies
an unresolved outcome. Every D clause has **U exact 12.4.3 applicability**. Installed
schema/preset presence corroborates device identity and storage vocabulary only.
No application, original function or candidate was executed.

Canonical analysis and source pins: [sample instruments](../research/sample-instruments.md).
Generic chain/rack editing belongs to [device racks](device-racks.md), media/dependencies
to [project/media workflows](project-media-workflows.md), Set structure to
[live-set structure](live-set-structure.md), marker storage to [warp markers](warp-markers.md),
and automation ownership to [automation envelopes](automation-envelopes.md).
These links assign ownership; they do not resolve an interaction automatically.

## Requirements

### REQ-SIMPLER-001 — Load and replace sample (D)

Dropping a sample from the browser loads it. Dropping an audio clip from Session or Arrangement uses its start/end or loop-bounded region and retains its Warp Markers and warp settings. Dragging another sample or using sample Hot-Swap replaces the loaded sample. The precedence when clip start/end and loop bounds disagree is unknown.

Evidence: [manual §31.11](https://www.ableton.com/en/live-manual/12/live-instrument-reference/#simpler); exact retained HTML anchor/line in the [heading map](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manual-headings.json).

### REQ-SIMPLER-002 — Playback mode selection (D)

Expose Classic, One-Shot and Slicing modes. Classic is the documented initial mode with polyphonic playback and ADSR/looping; One-Shot is monophonic and has no looping; Slicing selects sample regions chromatically without modifying the original file. User defaults may replace initial settings.

Evidence: [manual §31.11.1](https://www.ableton.com/en/live-manual/12/live-instrument-reference/#playback-modes); exact retained HTML anchor/line in the [heading map](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manual-headings.json).

### REQ-SIMPLER-003 — Classic region and percentage controls (D)

In Classic, absolute flags delimit the available region. Start and Length are percentages of that region. Length 50% selects half its duration. The Loop amount is active only while Loop is enabled. The precise Start/Length constraint and clamp rule at the region end remains unknown.

Evidence: [manual §31.11.1.1](https://www.ableton.com/en/live-manual/12/live-instrument-reference/#classic-playback-mode); exact retained HTML anchor/line in the [heading map](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manual-headings.json).

### REQ-SIMPLER-004 — Classic looping, snap and fades (D)

Loop enables repeated playback while a note is held. Snap moves region/loop markers to zero crossings using the left channel of stereo samples; it does not guarantee a click-free right channel. Fade crossfades loop endpoints. The title-bar option selects constant-power (documented default) or linear loop fades; Fade is unavailable with Warp enabled (context-menu-options-for-simpler). Exact crossfade coefficients are unknown.

Evidence: [manual §31.11.1.1](https://www.ableton.com/en/live-manual/12/live-instrument-reference/#classic-playback-mode); exact retained HTML anchor/line in the [heading map](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manual-headings.json).

### REQ-SIMPLER-005 — Voice limits and repeated pitch (D)

Voices sets the simultaneous voice limit. When exceeded, the oldest voices are removed in favor of new voices. With Retrig enabled a sustaining copy of the same note is cut on its next trigger; with Retrig disabled same-note voices can overlap. A useful audible retrigger comparison requires Voices>1 and a long release. Exact stealing fade/tie ordering is unknown.

Evidence: [manual §31.11.1.1](https://www.ableton.com/en/live-manual/12/live-instrument-reference/#classic-playback-mode); exact retained HTML anchor/line in the [heading map](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manual-headings.json).

### REQ-SIMPLER-006 — One-Shot Trigger, Gate and fade (D)

One-Shot uses absolute region flags, has no Loop/Length/Voices controls and is always monophonic. Trigger plays the sample after note release. Gate begins Fade Out at note release and reaches silence after its configured duration. In Trigger, Fade Out is placed before the sample-region end. Fade In starts at note onset. Endpoint rounding and fade curves are unknown.

Evidence: [manual §31.11.1.2](https://www.ableton.com/en/live-manual/12/live-instrument-reference/#one-shot-playback-mode); exact retained HTML anchor/line in the [heading map](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manual-headings.json).

### REQ-SIMPLER-007 — Automatic and manual slice creation (D)

Slice By Transient places slices according to detected transients; raising Sensitivity increases detected slices up to 64. Beat uses the selected beat division. Region divides the available region into equal durations. Manual adds no automatic slices; double-click within the region creates one. Exact detection thresholds and musical-boundary rounding remain unknown.

Evidence: [manual §31.11.1.3](https://www.ableton.com/en/live-manual/12/live-instrument-reference/#slicing-playback-mode); exact retained HTML anchor/line in the [heading map](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manual-headings.json).

### REQ-SIMPLER-008 — Editing slice markers (D)

Automatic slice lines are blue and manually created lines white. Double-click an existing slice to delete; drag to move; double-click between slices to insert. In Transient mode Alt/Option-click toggles manual/automatic identity; manual slices survive Sensitivity changes. Marker collision and out-of-region movement rules remain unknown.

Evidence: [manual §31.11.1.3](https://www.ableton.com/en/live-manual/12/live-instrument-reference/#slicing-playback-mode); exact retained HTML anchor/line in the [heading map](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manual-headings.json).

### REQ-SIMPLER-009 — Slice playback and fade extent (D)

Mono permits one slice; Poly allows multiple slices and exposes Classic Voices/Retrig behavior; Thru is monophonic and continues from the triggered slice through the rest of the region. Trigger/Gate behaves as in One-Shot. Mono/Poly fades span an individual slice; Thru fades span from the selected slice to region end. The lowest mapped note and overflow note behavior are not established here.

Evidence: [manual §31.11.1.3](https://www.ableton.com/en/live-manual/12/live-instrument-reference/#slicing-playback-mode); exact retained HTML anchor/line in the [heading map](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manual-headings.json).

### REQ-SIMPLER-010 — Warp mode interaction (D)

With Warp off, note pitch changes playback speed. Warp on follows Set tempo independently of the played pitch. Warp as sets a chosen musical duration. The ÷2 command doubles playback speed and ×2 halves it, as documented. Warp modes/marker storage belong to warp-markers.md; this clause provides no resampling, stretch or transient DSP oracle.

Evidence: [manual §31.11.2](https://www.ableton.com/en/live-manual/12/live-instrument-reference/#warp-controls); exact retained HTML anchor/line in the [heading map](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manual-headings.json).

### REQ-SIMPLER-011 — Filter control availability (D)

Expose low-pass, high-pass, band-pass, notch and Morph with 12/24 dB slopes. Clean and OSR support every filter type; MS2/SMP/PRD are documented for low-pass/high-pass. Drive is present for low-pass/high-pass/band-pass with non-Clean circuits. Morph traverses low-pass → band-pass → high-pass → notch → low-pass and has context-menu snap choices. Cutoff accepts velocity, key, envelope and LFO modulation. Transfer functions and circuit nonlinearities are unknown.

Evidence: [manual §31.11.3](https://www.ableton.com/en/live-manual/12/live-instrument-reference/#filter-1); exact retained HTML anchor/line in the [heading map](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manual-headings.json).

### REQ-SIMPLER-012 — Envelopes (D)

Amplitude, filter and pitch have ADSR controls, editable by values or graph handles. Attack reaches peak, Decay reaches Sustain, and note release begins Release toward zero. Pitch/filter envelope amounts govern their influence. Amplitude Loop/Trigger restarts after Decay when held, returning from sustain to initial over Time; Beat/Sync repeats after Rate. Precise envelope curves, clock alignment and mode-switch continuity remain unknown.

Evidence: [manual §31.11.4](https://www.ableton.com/en/live-manual/12/live-instrument-reference/#envelopes-2); exact retained HTML anchor/line in the [heading map](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manual-headings.json).

### REQ-SIMPLER-013 — Per-voice LFO (D)

LFO offers sine, square, triangle, descending/ascending saw and random; rate is 0.01–30 Hz or tempo divisions. Attack fades its depth in. Retrigger resets each new note to Offset; Offset has no effect while retrigger is off. Key scales rate by note pitch, with zero giving equal rate across voices. Destinations are Volume/Pitch/Pan/Filter. Random distribution and exact phase/sample math are unknown.

Evidence: [manual §31.11.5](https://www.ableton.com/en/live-manual/12/live-instrument-reference/#lfo); exact retained HTML anchor/line in the [heading map](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manual-headings.json).

### REQ-SIMPLER-014 — Gain, output and stereo spread (D)

Sample Gain precedes the output Volume stage after the filter; these are separate controls. Output Volume accepts velocity and LFO modulation. Pan accepts random and LFO modulation. Spread creates two detuned voices per note, one left and one right; its on/off decision is taken at Note On. Changing Spread later does not change whether that held note acquired the paired voices. Exact detune/pan/gain laws are unknown.

Evidence: [manual §31.11.6](https://www.ableton.com/en/live-manual/12/live-instrument-reference/#global-parameters-1); exact retained HTML anchor/line in the [heading map](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manual-headings.json).

### REQ-SIMPLER-015 — Pitch reference, transpose and glide (D)

Without tuning or additional pitch modulation, C3 plays the sample at original pitch. Transpose spans ±48 semitones, Detune ±50 cents, and pitch bend sensitivity is documented as ±5 semitones. Glide is monophonic; Portamento is polyphonic; Time controls transition duration from the prior note pitch to the new one. MPE/tuning interactions and the exact glide trajectory are unknown.

Evidence: [manual §31.11.6](https://www.ableton.com/en/live-manual/12/live-instrument-reference/#global-parameters-1); exact retained HTML anchor/line in the [heading map](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manual-headings.json).

### REQ-SIMPLER-016 — Non-destructive crop and reverse (D)

Crop retains only the Start/End-bounded sample region in a new copy. Reverse also creates a processed copy. The original sample bytes are preserved. Generated names, directories, repeated operation deduplication and failure atomicity are unknown; media ownership belongs to project-media-workflows.md.

Evidence: [manual §31.11.7](https://www.ableton.com/en/live-manual/12/live-instrument-reference/#context-menu-options-for-simpler); exact retained HTML anchor/line in the [heading map](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manual-headings.json).

### REQ-SIMPLER-017 — Convert to Sampler and slice to racks (D)

Simpler → Sampler converts the preset. Sampler has no Simpler warp/slice functionality, so conversion of those modes carries no sound-equivalence promise. In Slicing, Slice to Drum Rack replaces this Simpler with a rack containing one pad per current slice. Slice to New MIDI Track instead adds a rack track and a clip playing slices in order. Generic rack/track/clip rules remain with device-racks.md and live-set-structure.md.

Evidence: [manual §31.11.7](https://www.ableton.com/en/live-manual/12/live-instrument-reference/#context-menu-options-for-simpler); exact retained HTML anchor/line in the [heading map](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manual-headings.json).

### REQ-SIMPLER-018 — Sample management and normalization (D)

Manage Sample opens the File Manager for the sample; Show in Browser selects it there. Show in Finder/Explorer reveals the backing folder but is unavailable for official Ableton Pack samples. Normalize Volumes adjusts sample gain so the peak uses available headroom; exact peak scanning, gain rounding and silent-file handling remain unknown.

Evidence: [manual §31.11.7](https://www.ableton.com/en/live-manual/12/live-instrument-reference/#context-menu-options-for-simpler); exact retained HTML anchor/line in the [heading map](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manual-headings.json).

### REQ-SIMPLER-019 — Persistence and dependent media (U)

Exact save/reopen restoration of device modes, layer/slot assignments, markers, modulation, voice options and external media references is unknown. Stored fields in shipped content do not prove writer coverage, crash recovery or reload equivalence. Generic Set/media container behavior remains with live-set-structure.md and project-media-workflows.md.

Evidence: [lifecycle evidence gaps](../research/sample-instruments.md#unresolved-interactions); exact retained HTML anchor/line in the [heading map](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manual-headings.json).

### REQ-SIMPLER-020 — Undo and redo (U)

Undo grouping, restoration of device/sample settings, marker/layer edits, generated files, conversion and routing changes are unknown. No promise of file deletion or resurrection is derived from a non-destructive operation.

Evidence: [lifecycle evidence gaps](../research/sample-instruments.md#unresolved-interactions); exact retained HTML anchor/line in the [heading map](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manual-headings.json).

### REQ-SIMPLER-021 — Malformed or unavailable sample failure (U)

Acceptance of corrupt/truncated/unsupported audio, zero-length or missing samples, dependency resolution, out-of-range imported controls and failed allocation is unknown. No silence/no-crash or atomic rollback promise is invented.

Evidence: [lifecycle evidence gaps](../research/sample-instruments.md#unresolved-interactions); exact retained HTML anchor/line in the [heading map](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manual-headings.json).

### REQ-SIMPLER-022 — Cancellation and voice teardown (U)

Cancel during sample replacement/import/conversion and remove or bypass while held notes play: resource cleanup, voice tail, pending-note handling and state restoration are unknown. Sample-rate changes, transport stop/restart and device reset have no established output oracle here.

Evidence: [lifecycle evidence gaps](../research/sample-instruments.md#unresolved-interactions); exact retained HTML anchor/line in the [heading map](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manual-headings.json).

### REQ-SIMPLER-023 — DSP, scheduling and modulation fidelity (U)

Interpolation, filter/warp/stretch/saturation equations, gain/pan curves, modulation sums, random sequences, denormal/overload handling and sample-accurate note/control order are unknown. No numeric audio-error tolerance, performance bound or exact12.4.3 parity follows from manual descriptions.

Evidence: [lifecycle evidence gaps](../research/sample-instruments.md#unresolved-interactions); exact retained HTML anchor/line in the [heading map](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manual-headings.json).

## Timing, state and comparison rules

Use fresh device state for each scenario; explicitly pin edition, mode, source hashes,
engine/sample rate, tuning, note duration and routing. MIDI note names use the manual’s
C3 convention; no numeric-note alias is inferred. Time/frequency/cent/semitone units
are those named in each clause. “Before/after” describes causal order, without an
invented audio-block latency. Endpoints and values are exact displayed choices;
float/audio comparisons require a separately supported tolerance. No sample-exact
DSP or timing oracle is supplied.

[Fixture definitions](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/fixtures.json)
pin three synthetic stereo PCM files with separated source bands. Their hashes and
known segment order identify test inputs, never Live output. `state` means compare
named visible states/counts/values exactly; `source-identity` distinguishes loaded
layers/regions, refusing ambiguous observations; `presence` tests only the named
continuation/termination or independence predicate, never waveform equality.
`unknown` records an observation without a pass/fail oracle. Cases with unavailable
third-party/official-Pack input stay unexecuted. All cases are plans and have not run.

## Acceptance cases

The [frozen case index](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/cases.json)
also retains requirement, source anchor, fixture and execution status per case.
All D expectations remain version-uncertain for the pinned target; all U cases are ungraded.

| Case | Requirement | Kind | Setup and action | Expected result / comparator |
| --- | --- | --- | --- | --- |
| SIMPLER-001 | REQ-SIMPLER-001 | positive | Audio clip uses segmented.wav with bounds 1–3 seconds and two manually adjusted Warp Markers. Drop clip into empty Simpler. | Loaded region follows the clip bounds; the two edited markers and warp settings are retained. / state |
| SIMPLER-002 | REQ-SIMPLER-001 | positive | Simpler contains segmented.wav. Replace it with layer-b.wav by drag. | Loaded sample becomes layer-b.wav; which other settings reset is unknown. / state |
| SIMPLER-003 | REQ-SIMPLER-002 | positive | Factory-initialized device, no user default. Inspect modes and switch Classic → One-Shot → Slicing. | All three modes selectable; One-Shot omits loop controls; Slicing shows slice controls. / state |
| SIMPLER-004 | REQ-SIMPLER-003 | boundary | Classic with segmented.wav; absolute flags at 1 and 3 seconds. Set Start=0%, Length=50%. | Selected duration is 1 second within the flagged region. / state |
| SIMPLER-005 | REQ-SIMPLER-003 | negative | Same region, Loop disabled. Inspect Loop amount control. | Loop amount is inactive. / state |
| SIMPLER-006 | REQ-SIMPLER-004 | positive | Classic, segmented.wav, Loop enabled, region 1–2 seconds, long sustain. Hold note longer than region. | Region repeats while held; loop-wrap numerical timing is ungraded. / source-identity |
| SIMPLER-007 | REQ-SIMPLER-004 | negative | Same setup, Warp enabled. Inspect Fade. | Loop Fade parameter is unavailable. / state |
| SIMPLER-008 | REQ-SIMPLER-005 | boundary | Classic, Voices=2, long held samples, distinguishable pitches C3/E3/G3. Play C3, then E3, then G3. | The oldest C3 voice is dropped; E3 and G3 remain. / source-identity |
| SIMPLER-009 | REQ-SIMPLER-005 | positive | Voices=8, long release. Repeat C3 with Retrig on, then repeat in fresh setup with it off. | On cuts the preceding same-note voice; off permits overlap. / presence |
| SIMPLER-010 | REQ-SIMPLER-006 | negative | One-Shot Trigger; full 4-second segmented.wav; no fades. Release the note after 0.25 seconds. | Playback continues after release before reaching region end. / presence |
| SIMPLER-011 | REQ-SIMPLER-006 | positive | Same sample, Gate, Fade Out=0.1 seconds. Release at 0.25 seconds. | The fade begins on release and reaches silence after its configured duration; sample precision ungraded. / presence |
| SIMPLER-012 | REQ-SIMPLER-007 | positive | Slicing, segmented.wav, full 4-second region. Choose Region and Regions=4. | Four equal-duration regions divide the selected audio. / state |
| SIMPLER-013 | REQ-SIMPLER-007 | negative | Fresh sample with no manually added slices. Choose Manual. | No automatic slices are placed; the implicit playable start-region convention remains unknown. / state |
| SIMPLER-014 | REQ-SIMPLER-008 | positive | Transient mode with an automatic slice. Alt/Option-click it to manual, change Sensitivity. | The manual marker stays; its manual identity is shown. / state |
| SIMPLER-015 | REQ-SIMPLER-008 | positive | Two known markers. Insert between them, move the new marker, then double-click it. | Count grows by one; marker position follows the move; deletion restores prior count. / state |
| SIMPLER-016 | REQ-SIMPLER-009 | positive | Four-region sample; identify the input key mapped to second slice without assuming its note number. Trigger second slice in Mono, then in Thru. | Mono ends at that slice boundary; Thru continues through following regions. / source-identity |
| SIMPLER-017 | REQ-SIMPLER-009 | positive | Slicing Poly. Inspect Voices and Retrig; trigger two mapped slices together. | Both controls available; simultaneous slices allowed. / presence |
| SIMPLER-018 | REQ-SIMPLER-010 | positive | Neutral pitch, Warp as 2 bars at 120 BPM, full 4-second sample. Choose ÷2 then reset and choose ×2. | ÷2 doubles speed and ×2 halves speed relative to that setup; exact interpolation ungraded. / source-identity |
| SIMPLER-019 | REQ-SIMPLER-011 | positive | Loaded sample; filter enabled. Choose low-pass Clean, then low-pass OSR, then Morph. | Clean has no Drive; OSR low-pass has Drive; Morph control and named snap choices are available. / state |
| SIMPLER-020 | REQ-SIMPLER-012 | positive | Classic, long sample, amplitude envelope visible. Change Attack numerically, then drag the attack handle. | Numeric and graphical values reflect the same envelope control; exact drag quantization unknown. / state |
| SIMPLER-021 | REQ-SIMPLER-013 | boundary | LFO enabled, free rate. Set rate to 0.01 then 30 Hz; inspect waveform/destination options. | Endpoints and six documented waves selectable; four named destinations present. / state |
| SIMPLER-022 | REQ-SIMPLER-013 | negative | LFO retrigger disabled. Change Offset while comparing repeated held-note setup. | Offset has no effect under disabled retrigger; audio precision ungraded. / presence |
| SIMPLER-023 | REQ-SIMPLER-014 | positive | Loaded sample. Change sample Gain, inspect output Volume; then set independent Volume. | Both controls remain independently adjustable; no gain curve asserted. / state |
| SIMPLER-024 | REQ-SIMPLER-014 | positive | Neutral mono sample, Spread=0 at first Note On. Set Spread nonzero while held; trigger a new note. | The first note does not acquire spread; the new note uses spread. / source-identity |
| SIMPLER-025 | REQ-SIMPLER-015 | boundary | Neutral pitch, no tuning, no Warp, layer-b.wav. Play C3; inspect Transpose and Detune endpoints. | C3 preserves source pitch; ±48-semitone and ±50-cent endpoints are available. / source-identity |
| SIMPLER-026 | REQ-SIMPLER-016 | positive | segmented.wav original hash retained; flags 1–3 seconds. Crop; inspect generated audio and original hash. | A cropped copy contains the selected region; original bytes unchanged. / state |
| SIMPLER-027 | REQ-SIMPLER-016 | positive | segmented.wav original hash retained. Reverse. | A copy is reversed; original bytes unchanged. / source-identity |
| SIMPLER-028 | REQ-SIMPLER-017 | positive | Slicing with four known slices. Run Slice to Drum Rack. | Current device replaced by Drum Rack; four pads own the four slices. / state |
| SIMPLER-029 | REQ-SIMPLER-017 | positive | Fresh same setup. Run Slice to New MIDI Track. | A new rack track and ordered-slice clip are added; original Simpler remains. / state |
| SIMPLER-030 | REQ-SIMPLER-018 | negative | Sample from an official Ableton Pack; control platform macOS. Inspect sample context menu. | Show in Finder command unavailable; Manage Sample and Show in Browser remain documented routes. / state |
| SIMPLER-031 | REQ-SIMPLER-019 | persistence | Simpler configured with all applicable sample assignments and nondefault controls; retain original hashes. Save Set/preset, close and reopen with media available; repeat after moving one dependency. | Unknown — collect observations; no graded expected outcome. / unknown |
| SIMPLER-032 | REQ-SIMPLER-020 | undo | Simpler with documented sample state snapshot. Perform one sample/layer/marker edit as applicable, undo, redo; record control state and source-file hashes. | Unknown — collect observations; no graded expected outcome. / unknown |
| SIMPLER-033 | REQ-SIMPLER-021 | malformed/failure | Simpler loaded with valid segmented.wav; retain complete state snapshot. Try truncated WAV, empty file and deleted dependency separately; also inspect a zero-width sample/zone region where applicable. | Unknown — collect observations; no graded expected outcome. / unknown |
| SIMPLER-034 | REQ-SIMPLER-022 | cancellation/teardown | Simpler with an actively held long sample and original dependency hashes retained. In separate runs cancel a load, remove device during sustain, stop/restart transport and change engine sample rate; record outputs and media state. | Unknown — collect observations; no graded expected outcome. / unknown |
| SIMPLER-035 | REQ-SIMPLER-023 | audio/timing | Simpler with retained fixtures, explicit 48kHz engine and event schedule. Render documented modes, repeat under different block/rate/event alignments and compare retained outputs only after an original-derived oracle exists. | Unknown — collect observations; no graded expected outcome. / unknown |

Negative/boundary cases are included where a documented constraint supports an oracle.
Malformed, cancellation, teardown, persistence and undo cases are present but ungraded.
Unsupported controls, note-zero semantics, edge ties and resource exhaustion cannot
receive a pass from this packet. No case kind is treated as covered merely by naming it.

## Open questions and analyst evidence appendix

See [unresolved interactions](../research/sample-instruments.md#unresolved-interactions)
for exact-build parity, audio/timing, media, lifecycle and routing gaps. These are
required unknown outcomes, not authorized exclusions from full Live coverage.
The [source manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/sources.json)
pins current manual bytes/date/URL and original shipped schema/presets. The manual
heading map links each D clause to its retained section. Static field names impose
no candidate layout, enum value or processing architecture.

## Revision and handoff

Revision 1, 2026-10-19: bounded documented behavior plus explicit unresolved cases.
Independent review is required. No handoff or candidate compatibility result exists.
