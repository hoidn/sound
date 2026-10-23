---
id: SPEC-DEVICE-SAMPLER
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 3
target: Ableton Live 12 Suite 12.4.3
---

# Sampler sample-instrument behavior

## Scope and evidence rules

Owns `SURF-DEVICE-SAMPLER` in [the product inventory](../research/full-live-coverage-inventory.md).
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

### REQ-SAMPLER-001 — Multisample layers and focus (D)

Zone toggles a separate editor above Device View; Key/Vel/Sel select its range editor. Every contained sample is listed as a layer. Selecting a layer exposes it in the Sample tab. With Auto Select enabled, all layers eligible for the arriving note through key, velocity and selector zones are selected for that note duration. Simultaneous selection/ending-note tie behavior is unknown.

Evidence: [manual §31.10.5](https://www.ableton.com/en/live-manual/12/live-instrument-reference/#the-zone-tab) (retained HTML line 1554); exact retained source locators in the [heading map](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manual-headings.json).

### REQ-SAMPLER-002 — Key and velocity eligibility (D)

Each layer responds only within its key zone and Note On velocity zone. Newly imported key zones cover the full MIDI note range. Velocity zones span 1–127. The manual inconsistently describes full key coverage as “127” while naming C-2–G8; do not derive a 127-versus-128 endpoint rule from that wording. Zone-edge inclusivity and fade weighting are not independently resolved. See also velocity-zones.

Evidence: [manual §31.10.5.3](https://www.ableton.com/en/live-manual/12/live-instrument-reference/#key-zones) (retained HTML line 1700); [manual §31.10.5.4](https://www.ableton.com/en/live-manual/12/live-instrument-reference/#velocity-zones) (retained HTML line 1722); exact retained source locators in the [heading map](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manual-headings.json).

### REQ-SAMPLER-003 — Sample selector latch (D)

Each layer also has a 0–127 sample-select zone. A layer is eligible only if that zone overlaps the current selector. The selector affects availability at trigger time: moving it while a sample plays does not switch that playing voice to a different sample. Selector fade and exact boundary inclusivity are unknown.

Evidence: [manual §31.10.5.5](https://www.ableton.com/en/live-manual/12/live-instrument-reference/#sample-select-zones) (retained HTML line 1744); exact retained source locators in the [heading map](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manual-headings.json).

### REQ-SAMPLER-004 — Zone fades and edits (D)

Zone edges resize ranges, zone bodies move them and upper corners set fades. Lin/Pow switches all zone fades between linear and constant-power modes. Range normalization on overlapping/crossed/zero-width edges, the exact gain law and endpoint rounding remain unknown; names alone do not prove sin/cos coefficients.

Evidence: [manual §31.10.5](https://www.ableton.com/en/live-manual/12/live-instrument-reference/#the-zone-tab) (retained HTML line 1554); exact retained source locators in the [heading map](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manual-headings.json).

### REQ-SAMPLER-005 — Layer management and range distribution (D)

Layer menu supports Delete, Duplicate, Rename and sorting by name/key/velocity/selector in both directions. Select All With Same Range uses the currently active editor. Distribute Ranges Equally spans C-2–G8; Around Root Key allocates ranges around differing roots without overlaps, distributing equal-root layers evenly. Exact division remainder/tie rules are unknown.

Evidence: [manual §31.10.5.2](https://www.ableton.com/en/live-manual/12/live-instrument-reference/#the-sample-layer-list) (retained HTML line 1678); exact retained source locators in the [heading map](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manual-headings.json).

### REQ-SAMPLER-006 — Round Robin modes (D)

With RR enabled, layers sharing the same key zone cycle by mode. Forward goes top→bottom and wraps; Backward bottom→top and wraps. Other excludes an immediate repeat; Random permits repeats. Reset Interval restarts at its chosen musical interval: Forward from top, Backward from bottom, and Other/Random from the sample first played. These are current manual clauses only; target applicability and interactions with unequal velocity/selector ranges, one eligible layer and stopped transport remain unknown.

Evidence: [manual §31.10.5.1](https://www.ableton.com/en/live-manual/12/live-instrument-reference/#round-robin-sample-playback) (retained HTML line 1598); exact retained source locators in the [heading map](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manual-headings.json).

### REQ-SAMPLER-007 — Per-layer sample controls (D)

Sample tab values generally apply to selected layer. Root Key sets its reference note; sample Detune spans ±50 cents; Volume ranges from attenuation to +24 dB; Pan controls that sample. Reverse and RAM/interpolation are explicitly global exceptions. Sample chooser changes edited layer. Exact root mapping under tuning is unknown.

Evidence: [manual §31.10.6](https://www.ableton.com/en/live-manual/12/live-instrument-reference/#the-sample-tab) (retained HTML line 1782); exact retained source locators in the [heading map](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manual-headings.json).

### REQ-SAMPLER-008 — Reverse and display-only controls (D)

Global Reverse plays from Sample End backwards through any active sustain loop toward Sample Start without generating a new file. Snap uses left-channel zero crossings for sample/loop points and does not ensure right-channel continuity. Vertical Zoom changes display only. B/M/L/R chooses displayed channels, without specifying any output-channel processing.

Evidence: [manual §31.10.6](https://www.ableton.com/en/live-manual/12/live-instrument-reference/#the-sample-tab) (retained HTML line 1782); exact retained source locators in the [heading map](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manual-headings.json).

### REQ-SAMPLER-009 — Sample extent, sustain loop and Link (D)

Sample Start/End bound playback. Without an enabled loop, Sample End terminates playback even if the volume envelope continues; active sustain/release-loop behavior is the controlling exception, as specified here and in REQ-SAMPLER-010. With no sustain loop, playback ends at Sample End or completion of envelope release. Forward sustain loops return Loop End→Loop Start; back-and-forth loops reverse at both ends. With release mode Off they keep looping during volume-envelope release. Link makes effective Sample Start equal Loop Start, disabling but retaining the original Sample Start value for restoration when Link is disabled. Values can display samples or min:sec:ms.

Evidence: [manual §31.10.6.1](https://www.ableton.com/en/live-manual/12/live-instrument-reference/#sample-playback) (retained HTML line 1800); exact retained source locators in the [heading map](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manual-headings.json).

### REQ-SAMPLER-010 — Release modes and loop crossfades (D)

Release modes require active sustain looping. Release Enabled proceeds linearly toward Sample End on envelope release. Release Loop mode goes to Sample End then jumps to Release Loop start; back-and-forth release reverses between those points until the volume envelope ends. Crossfade is independently available for sustain/release loops with constant-power default or title-menu linear selection; loop Detune adjusts their pitch. Exact transition at a note-off coincident with a loop edge is unknown.

Evidence: [manual §31.10.6.1](https://www.ableton.com/en/live-manual/12/live-instrument-reference/#sample-playback) (retained HTML line 1800); exact retained source locators in the [heading map](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manual-headings.json).

### REQ-SAMPLER-011 — Envelope stages and repetition (D)

Attack moves Initial→Peak; Decay Peak→Sustain; Release moves toward End on Note Off. Zero slope is linear; positive slopes move faster at the beginning, negative slopes faster at the end. Loop restarts after Decay, Beat/Sync after a musical Repeat interval; Sync aligns to song time. Trigger ignores Note Off. Velocity scales segments, not Beat/Sync beat-time. Exact curves/clock rounding remain unknown.

Evidence: [manual §31.10.6.1](https://www.ableton.com/en/live-manual/12/live-instrument-reference/#sample-playback) (retained HTML line 1800); exact retained source locators in the [heading map](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manual-headings.json).

### REQ-SAMPLER-012 — Interpolation and RAM (D)

Interpolation is global, offering Normal, Good and Best quality. RAM is global and loads the entire multisample into RAM when enabled. Quality names provide no filter kernel or numeric fidelity contract. Allocation failure, streaming transition and memory-budget outcomes remain unknown.

Evidence: [manual §31.10.6.1](https://www.ableton.com/en/live-manual/12/live-instrument-reference/#sample-playback) (retained HTML line 1800); exact retained source locators in the [heading map](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manual-headings.json).

### REQ-SAMPLER-013 — Modulation oscillator (D)

Each voice has an FM/AM modulation oscillator; its signal is not directly audible as an independent sound source. It has 21 waveform choices, modulation amount and velocity amount, plus an envelope. Fixed enables frequency Freq×Multi independent of input pitch; with Fixed off, Coarse/Fine are used. Exact waveforms, FM scaling and AM law remain unknown.

Evidence: [manual §31.10.7.1](https://www.ableton.com/en/live-manual/12/live-instrument-reference/#the-modulation-oscillator-osc) (retained HTML line 1888); exact retained source locators in the [heading map](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manual-headings.json).

### REQ-SAMPLER-014 — Pitch envelope, zone shift and glide (D)

Pitch envelope affects sample and enabled modulation oscillator; Amount sets influence in semitones. Global Transpose/Detune act in semitones/cents. Key Zone Shift changes selection of sample layers while retaining played pitch. Spread creates two detuned voices per note. Glide is mono and Portamento poly, with Time defining transition duration. Pitch paths under alternate tuning and exact portamento law are unknown.

Evidence: [manual §31.10.7.2](https://www.ableton.com/en/live-manual/12/live-instrument-reference/#the-pitch-envelope) (retained HTML line 1888); exact retained source locators in the [heading map](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manual-headings.json).

### REQ-SAMPLER-015 — Filter and waveshaper routing (D)

Filter provides low-pass/high-pass/band-pass/notch/Morph,12/24 dB and circuit choices with the same documented availability as Simpler REQ-SIMPLER-011. Its own filter envelope requires enable and nonzero Amount. Shaper offers Soft/Hard/Sine/4bit; the routing control selects shaper→filter or filter→shaper. Transfer functions and oversampling are unknown.

Evidence: [manual §31.10.8.1](https://www.ableton.com/en/live-manual/12/live-instrument-reference/#the-filter) (retained HTML line 1906); exact retained source locators in the [heading map](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manual-headings.json).

### REQ-SAMPLER-016 — Global articulation and voice control (D)

Volume envelope articulates the instrument; Time globally scales all envelope lengths and Time<Key varies that scaling by note pitch. Global Pan and random pan act across samples. Voices allows up to32 simultaneous voices. Retrigger reuses already-playing same-note voices instead of adding them. Voice stealing order, smoothing and any counting interaction with Spread remain unknown.

Evidence: [manual §31.10.8.2](https://www.ableton.com/en/live-manual/12/live-instrument-reference/#the-volume-envelope-and-global-controls) (retained HTML line 1906); exact retained source locators in the [heading map](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manual-headings.json).

### REQ-SAMPLER-017 — Auxiliary envelope and LFO routing (D)

An auxiliary loopable envelope has A/B destinations and independent amounts; the manual describes29 destinations. Three LFOs expose sine/square/triangle/down-saw/up-saw/sample-and-hold,0.01–30 Hz or beat-time from1/64 note to8 bars. Retrig resets at note onset; Offset sets phase. LFO1 has Volume/Pan/Filter/Pitch amounts; LFO2/3 have A/B destinations and Phase/Spin stereo modes. Phase keeps channel rates equal; Spin can make right run up to50% faster. Exact destination enumeration and random sequences remain unknown.

Evidence: [manual §31.10.9](https://www.ableton.com/en/live-manual/12/live-instrument-reference/#the-modulation-tab) (retained HTML line 1906); exact retained source locators in the [heading map](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manual-headings.json).

### REQ-SAMPLER-018 — MIDI modulation assignments (D)

Key, Note On velocity, Release Velocity, Aftertouch, Mod Wheel, Foot Controller and Pitch Bend can each target A/B destinations with amounts. Pitch Bend Range spans0–24 semitones. The manual mentions14-bit pitch-wheel input; MIDI decoding is a separate owner. MPE assignment, destination clamps, simultaneous-source combination and note-off velocity handling beyond these assignments are unknown.

Evidence: [manual §31.10.10](https://www.ableton.com/en/live-manual/12/live-instrument-reference/#the-midi-tab) (retained HTML line 1924); exact retained source locators in the [heading map](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manual-headings.json).

### REQ-SAMPLER-019 — Import, preset actions and conversion (D)

The documented import list includes REX (Standard/Suite), ACID Loops and Soundtrack Loops. Drop from browser imports into User Library/Sampler/Imports, possibly as an Instrument Rack with multiple Samplers. ACID/Soundtrack tags are not accessible. Title menu can save current state as default and convert Sampler→Simpler. Exact supported versions, library decoding, migration and conversion loss remain unknown; project/media and racks retain generic ownership.

Evidence: [manual §31.10.11](https://www.ableton.com/en/live-manual/12/live-instrument-reference/#importing-third-party-multisamples) (retained HTML line 1942); [manual §31.10.3](https://www.ableton.com/en/live-manual/12/live-instrument-reference/#title-bar-options) (retained HTML line 1518); exact retained source locators in the [heading map](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manual-headings.json).

### REQ-SAMPLER-020 — Persistence and dependent media (U)

Exact save/reopen restoration of device modes, layer/slot assignments, markers, modulation, voice options and external media references is unknown. Stored fields in shipped content do not prove writer coverage, crash recovery or reload equivalence. Generic Set/media container behavior remains with live-set-structure.md and project-media-workflows.md.

Evidence: [lifecycle evidence gaps](../research/sample-instruments.md#unresolved-interactions); exact retained source locators in the [heading map](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manual-headings.json).

### REQ-SAMPLER-021 — Undo and redo (U)

Undo grouping, restoration of device/sample settings, marker/layer edits, generated files, conversion and routing changes are unknown. No promise of file deletion or resurrection is derived from a non-destructive operation.

Evidence: [lifecycle evidence gaps](../research/sample-instruments.md#unresolved-interactions); exact retained source locators in the [heading map](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manual-headings.json).

### REQ-SAMPLER-022 — Malformed or unavailable sample failure (U)

Acceptance of corrupt/truncated/unsupported audio, zero-length or missing samples, dependency resolution, out-of-range imported controls and failed allocation is unknown. No silence/no-crash or atomic rollback promise is invented.

Evidence: [lifecycle evidence gaps](../research/sample-instruments.md#unresolved-interactions); exact retained source locators in the [heading map](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manual-headings.json).

### REQ-SAMPLER-023 — Cancellation and voice teardown (U)

Cancel during sample replacement/import/conversion and remove or bypass while held notes play: resource cleanup, voice tail, pending-note handling and state restoration are unknown. Sample-rate changes, transport stop/restart and device reset have no established output oracle here.

Evidence: [lifecycle evidence gaps](../research/sample-instruments.md#unresolved-interactions); exact retained source locators in the [heading map](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manual-headings.json).

### REQ-SAMPLER-024 — DSP, scheduling and modulation fidelity (U)

Interpolation, filter/warp/stretch/saturation equations, gain/pan curves, modulation sums, random sequences, denormal/overload handling and sample-accurate note/control order are unknown. No numeric audio-error tolerance, performance bound or exact12.4.3 parity follows from manual descriptions.

Evidence: [lifecycle evidence gaps](../research/sample-instruments.md#unresolved-interactions); exact retained source locators in the [heading map](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manual-headings.json).

### REQ-SAMPLER-025 — Title, view and credits controls (D)

Group places Sampler in a new Instrument Rack. Fold leaves its title bar visible; double-clicking that bar unfolds it. Unchecking Show Preset Name replaces the title with Sampler. Hovering a sample layer or zone displays relevant sample information in the Status Bar; Small/Medium/Large changes Zone Editor zoom. Clicking the Sampler image in the MIDI tab starts scrolling credits. Exact title precedence, focus, zoom geometry and credit timing/content are unknown. Control-surface locking remains a separately conditioned, unadopted source-audit proposal.

Evidence: [reviewed retained source audit](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments-source-audit/README-r2.md) and exact block pointers in the [R3 cases](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/cases-r3.json). Exact 12.4.3 applicability remains U.

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
also retains requirement, every supporting source anchor/section/HTML line, fixture and execution status per case.
All D expectations remain version-uncertain for the pinned target; all U cases are ungraded.

| Case | Requirement | Kind | Setup and action | Expected result / comparator |
| --- | --- | --- | --- | --- |
| SAMPLER-001 | REQ-SAMPLER-001 | positive | Two layers with identical full key/velocity/selector ranges and RR off; Auto Select on. Play a note, then select either layer manually after release. | Both eligible layers selected during the note; manual selection exposes that layer in Sample tab. / state |
| SAMPLER-002 | REQ-SAMPLER-002 | negative | RR off; one layer key range C3–B3, velocity range 40–90. Play C2 at velocity64, then C3 at velocity20. | Neither input triggers the layer. / presence |
| SAMPLER-003 | REQ-SAMPLER-002 | positive | Same range, velocity64. Play E3. | Layer is eligible and plays. / source-identity |
| SAMPLER-004 | REQ-SAMPLER-003 | negative | A uses selector0–30, B uses90–127; selector15; hold A. Move selector to110; then trigger new note. | Held voice remains A; next eligible voice uses B. / source-identity |
| SAMPLER-005 | REQ-SAMPLER-004 | positive | Two adjoining key zones. Add edge fades and switch Lin to Pow. | Fade extents are represented; fade-mode choice changes globally, with exact audio law ungraded. / state |
| SAMPLER-006 | REQ-SAMPLER-005 | positive | Three named layers; two share key range but not velocity range. Select one of those two; Select All With Same Range in Key, then Velocity. | Key selects both key-matching layers; Velocity selects only velocity-range matches. / state |
| SAMPLER-007 | REQ-SAMPLER-005 | positive | Two selected layers. Duplicate one, rename copy, then delete it. | One added layer receives chosen name; deletion restores original layer count. / state |
| SAMPLER-008 | REQ-SAMPLER-006 | positive | Three layers A/B/C share all ranges, no fades, RR Forward, cycle freshly initialized. Trigger four successive notes before any reset boundary. | Identity order A,B,C,A. / source-identity |
| SAMPLER-009 | REQ-SAMPLER-006 | positive | Same setup with Backward and freshly initialized cycle. Trigger four notes. | Identity order C,B,A,C. / source-identity |
| SAMPLER-010 | REQ-SAMPLER-006 | negative | Three equally eligible layers, Other mode. Trigger 20 notes, record source identity. | No neighboring pair repeats; no random-frequency or seed claim. / source-identity |
| SAMPLER-011 | REQ-SAMPLER-007 | positive | Two layers with distinct names; no modulation. Select A, set Detune +25 cents; select B. | B exposes its own detune; sample chooser and editor follow the selected layer. / state |
| SAMPLER-012 | REQ-SAMPLER-008 | positive | Two layers, original file hashes retained. Enable Reverse. | Multisample reverses playback; no reversed copy is generated; original hashes stay unchanged. / source-identity |
| SAMPLER-013 | REQ-SAMPLER-008 | negative | One held layer. Change Vertical Zoom. | Waveform height changes; the control has no audio effect. / presence |
| SAMPLER-014 | REQ-SAMPLER-009 | positive | segmented.wav, Sample Start=0, sustain Loop Start=1 seconds. Enable Link, then disable Link. | Effective start becomes1 seconds while enabled; original0 seconds setting is recalled after disabling. / state |
| SAMPLER-015 | REQ-SAMPLER-009 | positive | Sustain loop1–2 seconds, release mode Off, long release. Hold beyond2 seconds then release. | Sustain region continues looping through envelope release. / source-identity |
| SAMPLER-016 | REQ-SAMPLER-010 | positive | Sustain loop1–2 seconds; sample end4 seconds; release loop start3 seconds; long envelope release. Release a note in Release Loop mode. | Playback reaches4 seconds then loops between3 and4 seconds until envelope completion. / source-identity |
| SAMPLER-017 | REQ-SAMPLER-010 | negative | Sustain loop inactive. Inspect Release Mode availability. | Release mode cannot be enabled without a sustain loop. / state |
| SAMPLER-018 | REQ-SAMPLER-011 | positive | Volume envelope, no loop, slope controls visible. Set attack slope0 then positive then negative. | Display shows linear, faster-start and slower-start shapes respectively; numeric curve equation ungraded. / state |
| SAMPLER-019 | REQ-SAMPLER-011 | negative | Envelope Trigger mode, sufficiently long sample. Send Note Off early in the envelope. | Trigger envelope ignores Note Off; sample end still independently bounds playback. / presence |
| SAMPLER-020 | REQ-SAMPLER-012 | positive | Two-layer multisample. Inspect Interpol choices and RAM control. | Normal/Good/Best are available; RAM is a global control rather than one per layer. / state |
| SAMPLER-021 | REQ-SAMPLER-013 | positive | Loaded sample; Osc enabled. Toggle Fixed on/off. | Fixed exposes Freq/Multi; non-fixed exposes Coarse/Fine. / state |
| SAMPLER-022 | REQ-SAMPLER-013 | negative | No sample loaded; oscillator enabled. Send notes. | Oscillator provides no directly audible standalone oscillator output. / presence |
| SAMPLER-023 | REQ-SAMPLER-014 | positive | A and B have different root/key zones and different timbre. Apply Key Zone Shift so the played note selects the other layer. | Layer selection changes while played pitch is retained. / source-identity |
| SAMPLER-024 | REQ-SAMPLER-015 | positive | Filter/Global tab. Inspect shaper modes and toggle direction. | Four named modes present; routing indicator alternates the two ordered paths. / state |
| SAMPLER-025 | REQ-SAMPLER-015 | negative | Override neutral fixture defaults: layer-c.wav (880 Hz) at its root pitch, held 3-second notes; enable main filter, Clean low-pass, 24 dB, cutoff 440 Hz, minimum resonance; no other modulation. Enable F. Env, minimum Initial/Sustain, maximum Peak, nonlooping envelope and Amount=0. Positive control: set filter-envelope Amount to a nonzero positive offered depth and compare Attack 10 ms versus 1000 ms; require a discernible envelope-dependent level/tone change, increasing depth within its offered range if necessary. Restore Amount=0, then repeat the same envelope edits. | The positive control establishes an active filter and envelope route on a source above cutoff. With Amount=0, envelope edits add no cutoff-driven change while the main filter remains enabled. If the active-path control cannot be resolved, record unknown; no transfer function or numeric audio threshold asserted. / presence |
| SAMPLER-026 | REQ-SAMPLER-016 | boundary | Filter/Global tab, long release. Set Voices to32 and enable Retrigger. | 32 is an available voice limit; repeating a playing pitch retriggers instead of adding a new same-note voice. / presence |
| SAMPLER-027 | REQ-SAMPLER-017 | boundary | Modulation tab. Inspect three LFO switches, rate endpoints and LFO2 stereo modes. | Three LFOs, documented0.01/30 Hz endpoints and Phase/Spin modes present. / state |
| SAMPLER-028 | REQ-SAMPLER-018 | boundary | MIDI tab. Inspect seven sources and two destination/amount slots each; set bend range0 and24. | Named sources each expose A/B;0 and24-semitone bend ranges selectable. / state |
| SAMPLER-029 | REQ-SAMPLER-019 | positive | Valid compatible REX file and Suite edition; file itself not supplied by this packet. Drop from browser into Set. | Import creates preset under User Library/Sampler/Imports; internal conversion fidelity ungraded. / state |
| SAMPLER-030 | REQ-SAMPLER-019 | positive | Sampler with one loaded layer. Inspect title context menu. | Save as Default Preset and Sampler → Simpler are available; state-equivalence result unknown. / state |
| SAMPLER-031 | REQ-SAMPLER-020 | persistence | Sampler configured with all applicable sample assignments and nondefault controls; retain original hashes. Save Set/preset, close and reopen with media available; repeat after moving one dependency. | Unknown — collect observations; no graded expected outcome. / unknown |
| SAMPLER-032 | REQ-SAMPLER-021 | undo | Sampler with documented sample state snapshot. Perform one sample/layer/marker edit as applicable, undo, redo; record control state and source-file hashes. | Unknown — collect observations; no graded expected outcome. / unknown |
| SAMPLER-033 | REQ-SAMPLER-022 | malformed/failure | Sampler loaded with valid segmented.wav; retain complete state snapshot. Try truncated WAV, empty file and deleted dependency separately; also inspect a zero-width sample/zone region where applicable. | Unknown — collect observations; no graded expected outcome. / unknown |
| SAMPLER-034 | REQ-SAMPLER-023 | cancellation/teardown | Sampler with an actively held long sample and original dependency hashes retained. In separate runs cancel a load, remove device during sustain, stop/restart transport and change engine sample rate; record outputs and media state. | Unknown — collect observations; no graded expected outcome. / unknown |
| SAMPLER-035 | REQ-SAMPLER-024 | audio/timing | Sampler with retained fixtures, explicit 48kHz engine and event schedule. Render documented modes, repeat under different block/rate/event alignments and compare retained outputs only after an original-derived oracle exists. | Unknown — collect observations; no graded expected outcome. / unknown |

The unlooped Sample End termination subclause of REQ-SAMPLER-009 is outside this finite case selection; the retained sustain/release-loop cases remain selected. A future bounded unlooped-end case is still required.

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

Revision 2, 2026-10-19: qualified Sampler loop-end behavior, active modulation controls and exact cross-section evidence locators. Revision 1 remains archived with its original manifest and payloads.
Independent review is required. No handoff or candidate compatibility result exists.

## Bounded revision 3 histories

The [R3 packet](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/README-r3.md) preserves all 88 original case objects and all 61 original requirement bodies. The [current case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/cases-r3.json) adds concrete selected reset histories, with [explicit current prerequisites and actual-result overlay](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/fixtures-r3.json). Original table entries above are the retained R2 subset.

- **SAMPLER-036**, REQ-SAMPLER-025: From independent resets invoke Group; invoke Fold and double-click the remaining title bar to unfold; uncheck Show Preset Name; hover a layer then a zone and inspect Status Bar; select Small, Medium and Large Zone Editor zoom independently. Do not simulate Lock to Control Surface without admitted configured supported hardware. Documented role: Group wraps in an Instrument Rack; Fold/unfold, title replacement, Status Bar and three zoom roles follow the new clause. No title-precedence/default or pixel/focus law; hardware lock is outside this case.
- **SAMPLER-037**, REQ-SAMPLER-007: Actually open the Sample chooser and select B, then reopen and select A. Record the selected edited layer each time, and change Detune only on that layer. Separately select a layer directly and inspect its corresponding display. Preserve old SAMPLER-011 as direct A/B selection plus Detune and expected chooser display, never chooser invocation. Documented role: Chooser changes edited layer; generally layer-specific values concern the selected layer. Reverse/RAM/interpolation exceptions remain global. No sound-equivalence or root/tuning law.
- **SAMPLER-038**, REQ-SAMPLER-009: Set an earlier Sample End within the productive region, trigger and hold beyond it. Reset to the longer Sample End and repeat the matched note. Observe source termination separately from the continuing volume-envelope setting; do not apply this unlooped predicate to enabled sustain/release loops. Documented role: Without enabled loops Sample End terminates playback even while the volume envelope continues. Source silence, shorter envelope or inactive output cannot establish termination; loop exceptions retain their separate predicates.
- **SAMPLER-039**, REQ-SAMPLER-010: In separate resets select back-and-forth sustain, then enabled release loop and back-and-forth release. Actually change sustain and release crossfade and Detune separately on their active loops. Select each title-bar constant-power/linear fade option only with an independently productive nonzero loop fade. Reset before disabling each demonstrated loop path. Documented role: Named sustain/release branches and controls concern their active loops; no invented icon label, fade coefficient, loop endpoint law or unconditional Sample End truncation.
- **SAMPLER-040**, REQ-SAMPLER-025: Click the Sampler image on the right of the MIDI tab and inspect whether scrolling credits begin. Do not infer a playback duration, exact names or movie codec. Documented role: The image is an entrypoint to scrolling credits; this adopts no MIDI codec, 14-bit scaling or numeric timing law.
- **SAMPLER-041**, REQ-SAMPLER-016: With Retrigger OFF play a note, release into its productive long tail, then trigger the same note again. Reset with the same admitted inputs and Retrigger ON and repeat actual notes. Merely setting Voices32 or enabling Retrigger as in old026 is not this two-history action. Documented role: Retrigger controls same-note overlap versus interruption as documented. No borrowed oldest-voice selection, tail coefficients or event-tie ordering.
- **SAMPLER-042**, REQ-SAMPLER-013: In independent resets actually select FM and AM and vary oscillator Type, Volume and VolVel. Exercise envelope, Fixed with Freq/Multi and non-Fixed Coarse/Fine in their appropriate contexts. Admit BOTH compared pitches/velocities first. Only after the active sample/modulation positive compare the retained empty-source negative. Documented role: Oscillator modulates the loaded sample and is not standalone audio. Named control roles are documented, not an FM/AM equation, tuning formula or guaranteed audible change for arbitrary input.

Every new documentary expected/comparison pair is null/U; the separate documented role is not a numeric or executed oracle. All 102 current actual pairs remain null/U/unexecuted. Each new case retains full specific and common prerequisites in the catalog; unavailable or ambiguous positives remain U. Independent R3 semantic review is pending; no complete profile or exact-target result is claimed.
