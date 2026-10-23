---
id: SPEC-DELAY-REVERB-DEVICES
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 2
target: Ableton Live 12 Suite 12.4.3; Live 12 documentary behavior, exact-build applicability unknown
---

# Delay, Echo, Filter Delay, Grain Delay, Reverb, Hybrid Reverb and Resonators

## Scope, authority and ownership

This partial FEAT-DEVICES draft owns seven individual profiles in the
[full product inventory](../research/full-live-coverage-inventory.md). Each has a
stable individual REQ-DR prefix. It describes documented controls, signal-path
roles, freeze/input admission, modulation and tails; it establishes no complete
device DSP or exact-build compatibility. It is an analyst draft, not a released
implementation input. The [coverage design](../research/full-live-specification-design.md)
governs evidence/case closure; the [research owner](../research/delay-reverb-devices.md)
interprets its retained sources.

[Device chains/racks](device-racks.md) owns insertion, common bypass, grouping,
presets and rack-chain tail gating. [Mix graph](mix-graph.md) owns its bounded
track composition, [automation envelopes](automation-envelopes.md) its stored
and evaluated envelope subset, and [Live Set structure](live-set-structure.md)
its document-reader scope. None establishes these seven devices' smoothing,
latency, automation eligibility or buffer lifetime. [Project/media workflows](project-media-workflows.md)
and [media files](media-file-workflows.md) own their existing media operations;
Hybrid Reverb-specific IR selection/import/list state is here. [Tuning systems](tuning-systems.md)
owns Set-level tuning; Resonators-specific controls are here. The seven bundled
instrument/effect [host draft](bundled-device-hosting.md) does not include these
seven profiles. Shared naming gives no cross-device DSP equivalence.

**D12** means the official Version 12 manual captured 2026-10-19, with **exact
12.4.3 applicability U for every runtime clause**. **Dpkg** means a checked
installed-file observation only. **U** means unknown and ungraded. There is no
S/X evidence or original/candidate execution in this packet. The source catalog
pins original manual-capture identity as well as reused bytes; matching schema
names and preset fields cannot turn D12 into an exact-build runtime assertion.

## Inputs, state and acceptance boundaries

Use an isolated active device and a valid editable test-owned Set; explicitly
select named settings, routing, channel mode, gain, timing and context. Do not
substitute shipped preset values for constructor defaults. Reset state between
trials. No automation, macro or mapping is active unless the case calls for it.
Track/monitor/main routing must deliver the source to the tested device, and
output gains must be nonzero and unmuted. Fixture choices of 120 BPM, 48 kHz,
16-second capture and 0.125 peak are authored setups, not product limits.

The retained [fixtures](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/fixtures.json)
define F0 isolation, F1 pulses/freeze signatures, F2 distinguishable stereo and
multiband tones, F3 changing envelope/donor, F4 nonidentity IRs, F5 tuning contexts
and F6 test-owned malformed/missing assets. These are declarative definitions;
no PCM/ALS/IR reference files or executable acceptance harness are supplied.
Inputs/output controls are in their stated display units; timing uses ms/seconds
or beat divisions, pitch semitones/scale degrees/note indices/cents as applicable,
frequency Hz, level dB/percent where documented. No universal normalized storage
mapping follows.

Before an audio effect/no-effect, freeze-admission, channel exclusion, inactive
control or zero-amount comparison, retain an active route, nonzero relevant
stimulus and nonzero wet output from the tested path, plus baseline and an
input-admitting/effect-on positive control. Isolate other paths with public
routing/mix/level controls when they can mask the observation. Filter modulation
needs an enabled filter, nonzero depth and excited pass/cut bands; envelope
modulation needs a changing envelope. Failed setup gates are inconclusive.
Numeric silence, equality or pitch tolerances remain U; these controls do not
create a calibrated audio comparator.

Observable state includes selected controls/modes, visible labels/disabled
controls, IR content/reference/User list, tuning/scale context and captured
stereo output. Buffer/grain/random state and tail persistence are independently
unknown. Freeze semantics differ by device: Delay rejects new input; Reverb
Cut controls admission and Flat controls frozen shelving; Hybrid Reverb Freeze In
admits input into the frozen algorithm engine. Do not substitute one for another.

Documentary cases compare only explicitly stated UI/control/routing predicates
against the cited source. Dpkg cases compare gzip/XML file facts. No sample-exact
output, delay rounding, oscillator phase, grain/window/RNG law, convolution
normalization, feedback saturation, tail cutoff, resampling kernel, mix equation,
smoothing period, filter transfer or acceptable tolerance is invented. All
149 cases have `exact_target_expected: null` and remain unexecuted. The 65 U
cases also have `expected: null`; they are evidence obligations, never passes.

## Requirements

Every D12 requirement below retains exact 12.4.3 applicability U. B-number
citations name exact retained blocks, with original HTML lines and heading
anchors available in the source packet. U requirements have no supported
runtime expectation. Package field observations stay in the research packet.

## Delay

### REQ-DR-DELAY-001 — Time and tempo-synchronized divisions

**D12.** Delay has separate left/right delay lines. Sync selects sixteenth-note divisions; selection 4 denotes four sixteenths, one quarter note. Offset shortens timing at negative values and extends it at positive values. Time mode offers 1.00 ms to 5.00 s. These are documented units/range, not sample rounding or tempo-change rules.

Evidence: [delay:B002](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-delay-blocks.json), [delay:B003](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-delay-blocks.json), [delay:B004](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-delay-blocks.json), [delay:B005](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-delay-blocks.json).

### REQ-DR-DELAY-002 — Stereo Link and independent offsets

**D12.** With Stereo Link on, changing one delay time applies to both channels, but each Offset remains independently adjustable. Linking initial unequal values, unlink restoration and simultaneous edits are unresolved.

Evidence: [delay:B006](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-delay-blocks.json).

### REQ-DR-DELAY-003 — Feedback paths

**D12.** Feedback returns each channel output to its own delay input; with Ping Pong off the documented feedback loops do not feed the opposite channel. Feedback gain law, runaway limit and saturation remain U.

Evidence: [delay:B007](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-delay-blocks.json).

### REQ-DR-DELAY-004 — Freeze admission and buffer cycling

**D12.** Freeze endlessly cycles the audio already in the buffer and ignores new input until deactivated. This does not establish a capture length, crossfade, exact periodic output or buffer persistence across save/reset.

Evidence: [delay:B008](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-delay-blocks.json).

### REQ-DR-DELAY-005 — Input band-pass filter

**D12.** The switchable band-pass filter precedes the delay signal. The display X-axis and Freq slider adjust center frequency; Y-axis and Width slider adjust bandwidth. Its transfer function is U.

Evidence: [delay:B009](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-delay-blocks.json).

### REQ-DR-DELAY-006 — Modulation targets and section visibility

**D12.** An LFO modulates delay time and filter frequency through separate Delay and Filter depth sliders. LFO Controls expands the collapsed section; the documented initial display is collapsed. The timing smoothing mode can change the sonic result of modulation. No default values or oscillator phase are established for the pinned build.

Evidence: [delay:B010](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-delay-blocks.json), [delay:B011](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-delay-blocks.json), [delay:B012](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-delay-blocks.json), [delay:B019](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-delay-blocks.json).

### REQ-DR-DELAY-007 — LFO modes, shapes and Morph

**D12.** Rate offers Rate, Time, Synced, Triplet, Dotted and Sixteenth modes. Wave offers Sine, Triangle, Ramp Up, Ramp Down, Square, S&H and Wander, with Morph shaping the selected wave. During playback the LED flashes with current LFO rate. Random distributions and phase resets are U.

Evidence: [delay:B013](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-delay-blocks.json), [delay:B014](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-delay-blocks.json).

### REQ-DR-DELAY-008 — Timing transitions

**D12.** Repitch produces a pitch change when delay time changes; Fade crossfades old/new times; Jump changes time immediately and can click during an existing decay. Repitch is the manual-described initial mode, with exact-build defaults U. No smoothing duration or requirement to click is inferred.

Evidence: [delay:B015](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-delay-blocks.json), [delay:B016](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-delay-blocks.json), [delay:B017](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-delay-blocks.json), [delay:B018](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-delay-blocks.json).

### REQ-DR-DELAY-009 — Ping Pong

**D12.** Ping Pong makes the delay signal alternate between left and right channels. Input summing, initial side, stereo normalization and interaction with Link are U.

Evidence: [delay:B020](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-delay-blocks.json).

### REQ-DR-DELAY-010 — Dry/Wet

**D12.** Dry/Wet balances dry and processed audio; 100% is documented for a return so that only processed signal is output. No bit-exact dry bypass, latency or mix equation follows.

Evidence: [delay:B021](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-delay-blocks.json).

### REQ-DR-DELAY-011 — Hi-Quality context option

**D12.** Hi-Quality is available through the device context/Show Options menu. It improves delay interpolation in Repitch/Fade and applies tape-style timing smoothing in Repitch. Numerical interpolation, cost and behavior in Jump are U.

Evidence: [delay:B022](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-delay-blocks.json), [delay:B023](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-delay-blocks.json), [delay:B024](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-delay-blocks.json).

### REQ-DR-DELAY-012 — Equal-Loudness context option

**D12.** Dry/Wet - Equal-Loudness changes between linear and equal-loudness output behavior; enabled 50/50 is described as equally loud for most signals. This qualitative statement is not an equal-power coefficient formula or loudness guarantee for correlated signals.

Evidence: [delay:B023](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-delay-blocks.json), [delay:B025](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-delay-blocks.json).

### REQ-DR-DELAY-013 — Effective audio, timing and edge behavior

**U.** Effective audio output, numeric gain/mix/filter/delay laws, sample-rate and block dependence, latency/compensation, silence floor, modulation phase, transition timing, feedback stability and tail completion remain unresolved. Randomness where applicable has no specified seed, distribution or repeatability. No source-derived parameter name/preset proves these outcomes.

### REQ-DR-DELAY-014 — Automation, persistence and lifecycle

**U.** Parameter automation/mapping eligibility, control ownership, state transition granularity, undo/redo grouping, saved/preset/tail/random-state persistence, malformed input handling, cancellation atomicity, missing dependencies and device/Set/audio-engine teardown are unresolved. Common editing/storage owners apply only within their published scopes; these device-specific outcomes are not inferred from generic actions.

## Echo

### REQ-DR-ECHO-001 — Channel modes

**D12.** Echo provides Stereo, Ping Pong and Mid/Side. Mid/Side replaces the Left/Right delay controls with Mid/Side controls. No matrix normalization or sample-level stereo trajectory is specified.

Evidence: [echo:B002](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-echo-blocks.json), [echo:B003](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-echo-blocks.json), [echo:B004](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-echo-blocks.json).

### REQ-DR-ECHO-002 — Delay units and Sync Mode

**D12.** Delay time is in beat divisions with Sync on and milliseconds with Sync off. Notes, Triplet, Dotted and 16th are selectable Sync Modes; changing Sync Mode affects sound only while Sync is on.

Evidence: [echo:B004](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-echo-blocks.json), [echo:B005](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-echo-blocks.json).

### REQ-DR-ECHO-003 — Stereo Link and offsets

**D12.** Stereo Link propagates time, Sync-switch and Sync-Mode edits to both delay lines; Offset remains independent per line. The initial value chosen on linking is U.

Evidence: [echo:B006](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-echo-blocks.json), [echo:B007](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-echo-blocks.json).

### REQ-DR-ECHO-004 — Input gain and dry distortion

**D12.** Input adjusts gain applied to the dry signal; D applies distortion to it. The distortion curve, clipping threshold and gain location beyond this description remain U.

Evidence: [echo:B008](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-echo-blocks.json).

### REQ-DR-ECHO-005 — Feedback and inversion

**D12.** Feedback returns each channel output to delay inputs; Ø inverts output before feeding it back. This documents sign inversion, not a full gain/stability law or parity of the first repeat.

Evidence: [echo:B009](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-echo-blocks.json).

### REQ-DR-ECHO-006 — Echo Tunnel

**D12.** Echo Tunnel displays repeats progressing outside to center; spacing denotes repeat interval, white dots form a fixed eighth-note reference. Dragging the display edits delay times.

Evidence: [echo:B010](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-echo-blocks.json), [echo:B011](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-echo-blocks.json), [echo:B012](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-echo-blocks.json).

### REQ-DR-ECHO-007 — Filters and display

**D12.** Filter enables high-pass and low-pass filtering; each has cutoff and resonance. The triangle shows/hides the Filter Display, whose points also edit filters. Transfer functions, ordering beyond the manual and transition behavior are U.

Evidence: [echo:B013](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-echo-blocks.json), [echo:B014](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-echo-blocks.json).

### REQ-DR-ECHO-008 — LFO wave, rate and phase

**D12.** The Modulation tab offers sine, triangle, saw up, saw down, square and noise. Sync selects beat-based Rate versus Freq in Hz. Display dragging edits frequency; Phase offsets left/right waveforms and 180 degrees denotes opposed phase. Exact wave shapes/noise law are U.

Evidence: [echo:B015](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-echo-blocks.json), [echo:B016](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-echo-blocks.json), [echo:B017](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-echo-blocks.json), [echo:B018](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-echo-blocks.json), [echo:B019](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-echo-blocks.json).

### REQ-DR-ECHO-009 — Modulation targets and x4

**D12.** Mod Delay targets delay time, Modulation x4 multiplies delay-modulation depth by four, and Mod Filter targets the filter. This does not establish a time-domain equation after clipping or smoothing.

Evidence: [echo:B020](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-echo-blocks.json), [echo:B021](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-echo-blocks.json).

### REQ-DR-ECHO-010 — Envelope versus LFO source

**D12.** Env Mix blends the LFO and envelope follower: 0% selects LFO only and 100% envelope only. Envelope detection, attack/release and blending law are U.

Evidence: [echo:B016](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-echo-blocks.json), [echo:B022](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-echo-blocks.json).

### REQ-DR-ECHO-011 — Input gate and wet ducking

**D12.** Gate operates at the input and mutes components below Threshold; Release sets closing time after a drop below threshold. Ducking reduces wet signal while input exceeds its Threshold, with Release after it drops. Equality, detector curve, attenuation amount, sidechain topology and exact timing are U.

Evidence: [echo:B024](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-echo-blocks.json), [echo:B025](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-echo-blocks.json), [echo:B026](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-echo-blocks.json).

### REQ-DR-ECHO-012 — Noise and Wobble

**D12.** Noise adds vintage-character noise with Amount and Morph. Wobble adds irregular delay-time modulation with Amount and Morph. Random processes, seed, spectral law and restart continuity are U.

Evidence: [echo:B027](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-echo-blocks.json), [echo:B028](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-echo-blocks.json).

### REQ-DR-ECHO-013 — Repitch versus crossfade

**D12.** Repitch on produces pitch variation when delay time changes; off crossfades old/new times. No fade duration, resampling kernel or state reset is specified.

Evidence: [echo:B029](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-echo-blocks.json).

### REQ-DR-ECHO-014 — Idle shutdown exception

**U.** Any application-observable consequence of the documented idle shutdown and Noise+Gate exception remains unknown. No shutdown indicator, CPU criterion, tail cutoff or internal processing mechanism is required; the manual statement is research context only.

Evidence: [echo:B030](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-echo-blocks.json).

### REQ-DR-ECHO-015 — Reverb placement and decay

**D12.** Reverb adjusts added reverberation; Location offers pre delay, post delay and within feedback. Decay lengthens/shortens reverb tail; its kernel and numerical tail are U.

Evidence: [echo:B032](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-echo-blocks.json).

### REQ-DR-ECHO-016 — Stereo width, output and mix

**D12.** Stereo acts on wet width: 0% is mono, above 100% is widened. Output changes processed gain. Dry/Wet balances dry/processed signals and 100% is intended for returns. Equal-Loudness is a Dry/Wet context option; its 50/50 loudness statement applies to most signals and establishes no coefficients.

Evidence: [echo:B033](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-echo-blocks.json), [echo:B034](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-echo-blocks.json).

### REQ-DR-ECHO-017 — Effective audio, timing and edge behavior

**U.** Effective audio output, numeric gain/mix/filter/delay laws, sample-rate and block dependence, latency/compensation, silence floor, modulation phase, transition timing, feedback stability and tail completion remain unresolved. Randomness where applicable has no specified seed, distribution or repeatability. No source-derived parameter name/preset proves these outcomes.

### REQ-DR-ECHO-018 — Automation, persistence and lifecycle

**U.** Parameter automation/mapping eligibility, control ownership, state transition granularity, undo/redo grouping, saved/preset/tail/random-state persistence, malformed input handling, cancellation atomicity, missing dependencies and device/Set/audio-engine teardown are unresolved. Common editing/storage owners apply only within their published scopes; these device-specific outcomes are not inferred from generic actions.

## Filter Delay

### REQ-DR-FILTER-DELAY-001 — Three delay inputs and output panning

**D12.** Three independently enabled delay lines have input selections left, left+right and right respectively. Each output normally uses its source channel; its Pan can override output placement. Input summing/normalization, disabled-line tail and pan law remain U.

Evidence: [filter-delay:B002](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-filter-delay-blocks.json), [filter-delay:B003](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-filter-delay-blocks.json).

### REQ-DR-FILTER-DELAY-002 — Filters and feedback routing

**D12.** Linked low/high-pass filtering precedes each delay and is also in its feedback path. Each filter has its own switch. X adjusts band frequency and Y bandwidth. A filter bypass is distinct from disabling its entire line.

Evidence: [filter-delay:B002](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-filter-delay-blocks.json), [filter-delay:B004](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-filter-delay-blocks.json).

### REQ-DR-FILTER-DELAY-003 — Sync and fractional timing

**D12.** Sync expresses time as sixteenth divisions; 4 denotes a quarter note. Percentage adjustment shortens/extends delay fractions in Sync. A displayed number does not define fractional-sample conversion.

Evidence: [filter-delay:B005](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-filter-delay-blocks.json).

### REQ-DR-FILTER-DELAY-004 — Milliseconds editing

**D12.** Sync off uses milliseconds. Delay Time can be edited by vertical drag or typed value. Accepted numerical range, out-of-range parsing, precision and smoothing remain U.

Evidence: [filter-delay:B006](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-filter-delay-blocks.json).

### REQ-DR-FILTER-DELAY-005 — Feedback

**D12.** Each Feedback control sets returned output amount. Very high values may produce runaway oscillation; the manual gives no safe maximum, limiter, exact gain or guaranteed finite tail.

Evidence: [filter-delay:B007](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-filter-delay-blocks.json).

### REQ-DR-FILTER-DELAY-006 — Line levels and Dry

**D12.** Each delay has a volume control offering up to +6 dB. Dry adjusts unprocessed level; minimum is documented for return use. These are independent levels, not a Dry/Wet ratio.

Evidence: [filter-delay:B008](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-filter-delay-blocks.json), [filter-delay:B009](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-filter-delay-blocks.json).

### REQ-DR-FILTER-DELAY-007 — Effective audio, timing and edge behavior

**U.** Effective audio output, numeric gain/mix/filter/delay laws, sample-rate and block dependence, latency/compensation, silence floor, modulation phase, transition timing, feedback stability and tail completion remain unresolved. Randomness where applicable has no specified seed, distribution or repeatability. No source-derived parameter name/preset proves these outcomes.

### REQ-DR-FILTER-DELAY-008 — Automation, persistence and lifecycle

**U.** Parameter automation/mapping eligibility, control ownership, state transition granularity, undo/redo grouping, saved/preset/tail/random-state persistence, malformed input handling, cancellation atomicity, missing dependencies and device/Set/audio-engine teardown are unresolved. Common editing/storage owners apply only within their published scopes; these device-specific outcomes are not inferred from generic actions.

## Grain Delay

### REQ-DR-GRAIN-DELAY-001 — Grains and Frequency

**D12.** Grain Delay divides input into individually delayed grains that may change pitch. Frequency determines grain size/duration and changes how Pitch and Spray sound. Exact grain schedule/window/overlap and Frequency-to-duration law are U.

Evidence: [grain-delay:B002](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-grain-delay-blocks.json), [grain-delay:B008](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-grain-delay-blocks.json).

### REQ-DR-GRAIN-DELAY-002 — X/Y assignments

**D12.** Parameter rows assign X below the display and Y at its left. Delay Time can be assigned to X; Dry/Wet can be assigned to Y. Pointer mapping and assignment persistence remain U.

Evidence: [grain-delay:B003](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-grain-delay-blocks.json), [grain-delay:B006](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-grain-delay-blocks.json), [grain-delay:B012](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-grain-delay-blocks.json).

### REQ-DR-GRAIN-DELAY-003 — Synchronized delay and milliseconds

**D12.** Sync selects sixteenth divisions with 4 equal to a quarter note and percentage timing adjustment. Sync off selects milliseconds, editable by vertical drag or typing. Randomized grain timing does not establish exact output onset at this nominal delay.

Evidence: [grain-delay:B004](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-grain-delay-blocks.json), [grain-delay:B005](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-grain-delay-blocks.json).

### REQ-DR-GRAIN-DELAY-004 — Spray random delay

**D12.** Spray adds random delay changes; low/high descriptions indicate temporal smearing through disruption of source rhythm. No distribution, maximum offset, seed, replay identity or monotonic audio metric is established.

Evidence: [grain-delay:B007](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-grain-delay-blocks.json).

### REQ-DR-GRAIN-DELAY-005 — Pitch and Random Pitch

**D12.** Pitch transposes grains; Random Pitch varies individual-grain pitches and interacts with Pitch. The pitch-shift method, random distribution, tuning precision and no-op bit identity are U.

Evidence: [grain-delay:B009](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-grain-delay-blocks.json), [grain-delay:B010](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-grain-delay-blocks.json).

### REQ-DR-GRAIN-DELAY-006 — Feedback and dry/wet

**D12.** Feedback returns output to the delay input; high values may run away without a documented bound. Dry/wet balances dry and processed audio and can be assigned to Y. The mix law and random-state behavior in feedback are U.

Evidence: [grain-delay:B011](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-grain-delay-blocks.json), [grain-delay:B012](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-grain-delay-blocks.json).

### REQ-DR-GRAIN-DELAY-007 — Effective audio, timing and edge behavior

**U.** Effective audio output, numeric gain/mix/filter/delay laws, sample-rate and block dependence, latency/compensation, silence floor, modulation phase, transition timing, feedback stability and tail completion remain unresolved. Randomness where applicable has no specified seed, distribution or repeatability. No source-derived parameter name/preset proves these outcomes.

### REQ-DR-GRAIN-DELAY-008 — Automation, persistence and lifecycle

**U.** Parameter automation/mapping eligibility, control ownership, state transition granularity, undo/redo grouping, saved/preset/tail/random-state persistence, malformed input handling, cancellation atomicity, missing dependencies and device/Set/audio-engine teardown are unresolved. Common editing/storage owners apply only within their published scopes; these device-specific outcomes are not inferred from generic actions.

## Reverb

### REQ-DR-REVERB-001 — Input filters

**D12.** Input first passes through individually switchable low/high cut filters. X controls band center, Y bandwidth; sliders offer the same controls. Cutoff laws, slope and bypass transition are U.

Evidence: [reverb:B006](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-reverb-blocks.json).

### REQ-DR-REVERB-002 — Early reflections and Spin

**D12.** Early reflections precede the diffuse tail. Spin modulates early reflections with Amount and Rate and can be disabled. Large rates may cause Doppler shifts/panning; no trajectory or threshold is specified.

Evidence: [reverb:B008](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-reverb-blocks.json), [reverb:B009](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-reverb-blocks.json).

### REQ-DR-REVERB-003 — Shape

**D12.** At smaller Shape values early reflections decay more gradually and diffuse onset is sooner, increasing overlap. Larger values yield quicker reflection decay and later diffuse onset. No continuous mapping or exact onset/decay metric follows.

Evidence: [reverb:B010](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-reverb-blocks.json).

### REQ-DR-REVERB-004 — Diffuse tail and shelving

**D12.** The Diffusion Network generates the tail. Independent high/low shelving filters shape frequency-dependent decay and can be turned off. Filter transfer, decay multipliers and frequency equality are U.

Evidence: [reverb:B012](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-reverb-blocks.json), [reverb:B013](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-reverb-blocks.json).

### REQ-DR-REVERB-005 — Diffusion and Scale

**D12.** Diffusion and Scale control tail density/coarseness, with pronounced coloration at extremely small room Size. No delay-line topology or parameter law is established.

Evidence: [reverb:B014](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-reverb-blocks.json).

### REQ-DR-REVERB-006 — Chorus

**D12.** Chorus modulates the diffusion with Amount and Rate and has an independent disable switch. Exact oscillator phases, waves and reset state are U.

Evidence: [reverb:B016](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-reverb-blocks.json).

### REQ-DR-REVERB-007 — Predelay

**D12.** Predelay is in milliseconds before the first early reflection. The manual describes 1-25 ms as typical natural-room choices; this is not its allowed range or rounding rule.

Evidence: [reverb:B018](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-reverb-blocks.json).

### REQ-DR-REVERB-008 — Size and Smooth

**D12.** Size controls virtual room volume. Smooth None changes diffusion delay times immediately; Slow/Fast update them over a period. Exact periods, interpolation and transition ordering are U.

Evidence: [reverb:B019](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-reverb-blocks.json), [reverb:B020](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-reverb-blocks.json).

### REQ-DR-REVERB-009 — Decay definition

**D12.** Decay denotes time for tail amplitude to fall to 1/1000 of its initial amplitude (-60 dB). This defines the documented quantity, not a calibrated output crossing in a multiband/modulated signal, finite tail termination or a numerical exponential.

Evidence: [reverb:B021](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-reverb-blocks.json).

### REQ-DR-REVERB-010 — Freeze, Flat and Cut

**D12.** Freeze sustains the diffuse response almost endlessly. With Freeze on, Flat bypasses high/low shelves; Flat off permits energy loss in attenuated bands according to shelf state. Cut prevents new input contributing to frozen reverberation; Cut off admits it. No exact infinite tail or bypass law outside Freeze follows.

Evidence: [reverb:B022](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-reverb-blocks.json).

### REQ-DR-REVERB-011 — Stereo, Density and output

**D12.** Stereo lowest setting mixes output to mono; 120 degrees describes independent reverberant channels. Density trades quality/performance, with Sparse and High named endpoints. Reflect and Diffuse independently scale their components; Dry/Wet balances overall dry/wet. No coefficient matrix, CPU count or mix law is specified.

Evidence: [reverb:B023](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-reverb-blocks.json), [reverb:B024](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-reverb-blocks.json), [reverb:B026](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-reverb-blocks.json).

### REQ-DR-REVERB-012 — Effective audio, timing and edge behavior

**U.** Effective audio output, numeric gain/mix/filter/delay laws, sample-rate and block dependence, latency/compensation, silence floor, modulation phase, transition timing, feedback stability and tail completion remain unresolved. Randomness where applicable has no specified seed, distribution or repeatability. No source-derived parameter name/preset proves these outcomes.

### REQ-DR-REVERB-013 — Automation, persistence and lifecycle

**U.** Parameter automation/mapping eligibility, control ownership, state transition granularity, undo/redo grouping, saved/preset/tail/random-state persistence, malformed input handling, cancellation atomicity, missing dependencies and device/Set/audio-engine teardown are unresolved. Common editing/storage owners apply only within their published scopes; these device-specific outcomes are not inferred from generic actions.

## Hybrid Reverb

### REQ-DR-HYBRID-REVERB-001 — Wet send and predelay

**D12.** Send changes gain feeding reverb while leaving dry signal unaffected. Predelay offers time/beat-synced units; each mode has an independent Feedback setting. These are distinct from the algorithm additional Delay. Timing units, feedback persistence across mode toggles and sample conversion need separate evidence.

Evidence: [hybrid-reverb:B007](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-hybrid-reverb-blocks.json), [hybrid-reverb:B010](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-hybrid-reverb-blocks.json), [hybrid-reverb:B011](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-hybrid-reverb-blocks.json), [hybrid-reverb:B012](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-hybrid-reverb-blocks.json).

### REQ-DR-HYBRID-REVERB-002 — Serial routing

**D12.** Serial sends convolution output into the algorithm engine. The convolution stays active; Blend 100/0 gives convolution-only output, while 0/100 gives algorithmic output fed by convolution. It is not raw-input algorithm-only at the second endpoint. The interpolation law is U.

Evidence: [hybrid-reverb:B013](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-hybrid-reverb-blocks.json), [hybrid-reverb:B014](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-hybrid-reverb-blocks.json), [hybrid-reverb:B019](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-hybrid-reverb-blocks.json).

### REQ-DR-HYBRID-REVERB-003 — Parallel routing

**D12.** Parallel keeps convolution and algorithm engines separate. Blend 100/0 gives pure convolution and 0/100 pure algorithmic output. Exact summation/gain law is U.

Evidence: [hybrid-reverb:B015](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-hybrid-reverb-blocks.json), [hybrid-reverb:B019](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-hybrid-reverb-blocks.json).

### REQ-DR-HYBRID-REVERB-004 — Single-engine routing and disabled controls

**D12.** Algorithm uses only the algorithm engine; Convolution only convolution. Unused-engine controls are grayed out. Blend has no effect in either single-engine route. Stored hidden values, CPU behavior and sample-identical no-op output are U.

Evidence: [hybrid-reverb:B016](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-hybrid-reverb-blocks.json), [hybrid-reverb:B017](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-hybrid-reverb-blocks.json), [hybrid-reverb:B018](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-hybrid-reverb-blocks.json), [hybrid-reverb:B019](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-hybrid-reverb-blocks.json).

### REQ-DR-HYBRID-REVERB-005 — IR selection and display

**D12.** Category and IR selectors choose impulses; arrows advance continuously across category boundaries. Waveform reflects Attack/Decay/Size changes. Ten documented categories are Early Reflections, Real Places, Chambers and Large Rooms, Made for Drums, Halls, Plates, Springs, Bigger Spaces, Textures and User. Exact installed IR list/version is U.

Evidence: [hybrid-reverb:B021](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-hybrid-reverb-blocks.json), [hybrid-reverb:B022](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-hybrid-reverb-blocks.json), [hybrid-reverb:B023](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-hybrid-reverb-blocks.json).

### REQ-DR-HYBRID-REVERB-006 — User IR import and removal

**D12.** Dropping an audio file on the waveform adds it as an IR; audio siblings in its folder are also added. Remove the device and add it again: previously added User samples no longer appear in User until added again. This does not define saved-Set restoration, supported codec set, recursion, file sorting or cleanup of source bytes.

Evidence: [hybrid-reverb:B003](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-hybrid-reverb-blocks.json), [hybrid-reverb:B024](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-hybrid-reverb-blocks.json).

### REQ-DR-HYBRID-REVERB-007 — Convolution envelope

**D12.** Attack/Decay control the IR amplitude envelope attack/decay times; Size controls relative IR size. Exact envelope, resampling, normalization, latency and stereo-channel convolution are U.

Evidence: [hybrid-reverb:B025](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-hybrid-reverb-blocks.json).

### REQ-DR-HYBRID-REVERB-008 — Algorithms and common controls

**D12.** Algorithms are Dark Hall, Quartz, Shimmer, Tides and Prism, with controls changing by selection. All have Decay, Size, Delay and Freeze. Decay denotes approximate time to -60 dB, Size virtual room size and Delay an additional algorithmic predelay in milliseconds. No exact kernel, sample delay or tolerance is established.

Evidence: [hybrid-reverb:B027](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-hybrid-reverb-blocks.json), [hybrid-reverb:B028](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-hybrid-reverb-blocks.json), [hybrid-reverb:B029](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-hybrid-reverb-blocks.json), [hybrid-reverb:B030](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-hybrid-reverb-blocks.json).

### REQ-DR-HYBRID-REVERB-009 — Freeze versus Freeze In

**D12.** Freeze blocks input to the algorithmic engine and sets decay to infinite for sustained output. Freeze In adds new input to frozen reverberation. This contract is algorithmic; it does not establish freezing convolution output, state persistence or numerical infinite duration.

Evidence: [hybrid-reverb:B031](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-hybrid-reverb-blocks.json).

### REQ-DR-HYBRID-REVERB-010 — Dark Hall controls

**D12.** Dark Hall provides Damping for high-frequency filtering, Mod for tail movement, Shape from small/resonant toward large/diffused, Bass X low-tail crossover and Bass Mult low-tail decay scaling. Long decay with tiny Size can give gong-like resonance; no guaranteed timbre or crossover law follows.

Evidence: [hybrid-reverb:B034](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-hybrid-reverb-blocks.json), [hybrid-reverb:B036](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-hybrid-reverb-blocks.json), [hybrid-reverb:B037](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-hybrid-reverb-blocks.json), [hybrid-reverb:B038](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-hybrid-reverb-blocks.json), [hybrid-reverb:B039](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-hybrid-reverb-blocks.json), [hybrid-reverb:B040](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-hybrid-reverb-blocks.json), [hybrid-reverb:B041](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-hybrid-reverb-blocks.json).

### REQ-DR-HYBRID-REVERB-011 — Quartz controls

**D12.** Quartz provides Damping (high filtering), Lo Damp (low filtering), Mod (tail movement), Diffusion (sparse to dense) and Distance (closer/denser to farther/more-spaced reflections). No monotonic waveform statistic or exact reflection schedule is specified.

Evidence: [hybrid-reverb:B043](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-hybrid-reverb-blocks.json), [hybrid-reverb:B045](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-hybrid-reverb-blocks.json), [hybrid-reverb:B046](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-hybrid-reverb-blocks.json), [hybrid-reverb:B047](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-hybrid-reverb-blocks.json), [hybrid-reverb:B048](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-hybrid-reverb-blocks.json), [hybrid-reverb:B049](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-hybrid-reverb-blocks.json).

### REQ-DR-HYBRID-REVERB-012 — Shimmer controls and zero amount

**D12.** Shimmer includes Damping, Mod, Diffusion, Pitch in semitones and Shimmer amount. Pitch-shifted feedback creates rising/falling tails; Shimmer=0% applies no pitch shifting and increasing amount makes pitched signal more present. Size affects spacing of echoes on percussive material. No resampling, diffusion threshold kernel or feedback stability law is specified.

Evidence: [hybrid-reverb:B051](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-hybrid-reverb-blocks.json), [hybrid-reverb:B053](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-hybrid-reverb-blocks.json), [hybrid-reverb:B054](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-hybrid-reverb-blocks.json), [hybrid-reverb:B055](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-hybrid-reverb-blocks.json), [hybrid-reverb:B056](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-hybrid-reverb-blocks.json), [hybrid-reverb:B057](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-hybrid-reverb-blocks.json), [hybrid-reverb:B058](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-hybrid-reverb-blocks.json).

### REQ-DR-HYBRID-REVERB-013 — Tides modulation

**D12.** Tides modulates output spectrum with a multiband filter. Damping controls high filtering; Tide controls texture intensity; Wave morphs noise (0%) to sine (50%) to square (100%); Phase=180 degrees opposes left/right modulation; Rate uses beat divisions with Triplet/16th/Dotted variations. Random spectra and phase/timing precision are U.

Evidence: [hybrid-reverb:B060](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-hybrid-reverb-blocks.json), [hybrid-reverb:B062](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-hybrid-reverb-blocks.json), [hybrid-reverb:B063](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-hybrid-reverb-blocks.json), [hybrid-reverb:B064](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-hybrid-reverb-blocks.json), [hybrid-reverb:B065](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-hybrid-reverb-blocks.json), [hybrid-reverb:B066](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-hybrid-reverb-blocks.json).

### REQ-DR-HYBRID-REVERB-014 — Prism band decay controls

**D12.** Prism is described as based on spectrally flat velvet noise. Low Mult and High Mult scale respective tail-band decays; X over sets the band boundary. Noise process, crossover filters, gain normalization and exact decay curves are U.

Evidence: [hybrid-reverb:B068](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-hybrid-reverb-blocks.json), [hybrid-reverb:B070](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-hybrid-reverb-blocks.json), [hybrid-reverb:B071](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-hybrid-reverb-blocks.json), [hybrid-reverb:B072](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-hybrid-reverb-blocks.json).

### REQ-DR-HYBRID-REVERB-015 — EQ placement and enable

**D12.** EQ has its own tab and toggle. The documented usual position follows both engines; Pre Algo places it before the algorithm engine regardless of selected reverb routing. This text does not resolve every Convolution-only inactive-algorithm topology or changing-tail transition.

Evidence: [hybrid-reverb:B075](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-hybrid-reverb-blocks.json), [hybrid-reverb:B076](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-hybrid-reverb-blocks.json).

### REQ-DR-HYBRID-REVERB-016 — EQ bands

**D12.** Four EQ bands include low/high bands switchable between pass filters and shelves, with 6 to 96 dB/octave slope range in pass modes; two middle peak bands cover the frequency range. Exact band domains, slope menu steps, cutoff/Q and digital transfer functions are U.

Evidence: [hybrid-reverb:B077](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-hybrid-reverb-blocks.json).

### REQ-DR-HYBRID-REVERB-017 — Wet width and Dry/Wet

**D12.** Stereo controls wet width with mono at 0% and widening above 100%; Dry/Wet balances processed/dry audio and 100% is documented for return use. No mono matrix, pan gain or mixing formula is established.

Evidence: [hybrid-reverb:B080](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-hybrid-reverb-blocks.json), [hybrid-reverb:B083](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-hybrid-reverb-blocks.json).

### REQ-DR-HYBRID-REVERB-018 — Vintage

**D12.** Vintage increasingly emulates lower sample rates/bit depths, with four presets Subtle, Old, Older and Extreme. No actual sample rates, bit depths, noise shaping or exact distortion is established.

Evidence: [hybrid-reverb:B081](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-hybrid-reverb-blocks.json).

### REQ-DR-HYBRID-REVERB-019 — Bass Mono

**D12.** Bass Mono converts frequencies below 180 Hz of the described output signal to mono. The source does not settle dry-path participation, crossover transition/filter slopes, equality at 180 Hz or channel summation coefficients.

Evidence: [hybrid-reverb:B082](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-hybrid-reverb-blocks.json).

### REQ-DR-HYBRID-REVERB-020 — Effective audio, timing and edge behavior

**U.** Effective audio output, numeric gain/mix/filter/delay laws, sample-rate and block dependence, latency/compensation, silence floor, modulation phase, transition timing, feedback stability and tail completion remain unresolved. Randomness where applicable has no specified seed, distribution or repeatability. No source-derived parameter name/preset proves these outcomes.

### REQ-DR-HYBRID-REVERB-021 — Automation, persistence and lifecycle

**U.** Parameter automation/mapping eligibility, control ownership, state transition granularity, undo/redo grouping, saved/preset/tail/random-state persistence, malformed input handling, cancellation atomicity, missing dependencies and device/Set/audio-engine teardown are unresolved. Common editing/storage owners apply only within their published scopes; these device-specific outcomes are not inferred from generic actions.

## Resonators

### REQ-DR-RESONATORS-001 — Five resonators and mode

**D12.** Five parallel resonators add tonal character. Mode A and B select distinct resonance modes; descriptions of realistic/low-pitched effects establish no modal kernel or numerical equivalence.

Evidence: [resonators:B002](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-resonators-blocks.json), [resonators:B004](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-resonators-blocks.json).

### REQ-DR-RESONATORS-002 — Input filter

**D12.** Input filtering precedes resonators, with low-pass, band-pass, high-pass and notch types, and Frequency controlling selected filter frequency. Filter order, slope and switching tails are U.

Evidence: [resonators:B003](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-resonators-blocks.json).

### REQ-DR-RESONATORS-003 — Decay, Const and Color

**D12.** Decay changes resonator sustain; normal pitch-dependent decay lasts longer at lower notes. Const selects pitch-independent decay; Color controls brightness. Exact time definition, frequency law, equality and spectrum are U.

Evidence: [resonators:B005](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-resonators-blocks.json), [resonators:B006](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-resonators-blocks.json).

### REQ-DR-RESONATORS-004 — Channel assignments

**D12.** Resonator I receives left+right, II/IV left only, III/V right only. Summation scaling and the output stereo matrix are U.

Evidence: [resonators:B007](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-resonators-blocks.json).

### REQ-DR-RESONATORS-005 — Root tuning and context

**D12.** Without scale awareness/tuning, I sets root and others follow musical intervals. With scale awareness, I is relative to active clip scale in octave 2; others relative to I. With tuning active, I uses an absolute tuning-defined pitch and others relative to it. Exact tuning precedence, no-active-clip fallback and changes during a tail remain U.

Evidence: [resonators:B008](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-resonators-blocks.json), [resonators:B009](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-resonators-blocks.json).

### REQ-DR-RESONATORS-006 — Note, Fine and relative ranges

**D12.** Default Note is semitones C-1 to C5; scale awareness changes to scale degrees, tuning to note indices. Fine I edits cents. II-V transpose relative to I by ±24 semitones or ±21 scale degrees and have individual Fine controls. Note-label ranges do not establish internal numbering, quantization or frequency calculation.

Evidence: [resonators:B009](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-resonators-blocks.json), [resonators:B011](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-resonators-blocks.json).

### REQ-DR-RESONATORS-007 — Independent enable and gain

**D12.** Every resonator has On/Off and Gain. Turning I off leaves others active; a disabled resonator is described as consuming no CPU, but this is not an application CPU benchmark or silence/tail oracle.

Evidence: [resonators:B010](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-resonators-blocks.json).

### REQ-DR-RESONATORS-008 — Wet width, gain and balance

**D12.** Width acts only on wet output and at 0% blends II-V to mono. Gain adjusts resonated level unless Dry/Wet=0%. Dry/Wet balances paths. No claim is made that I stereo mapping is determined by the II-V statement.

Evidence: [resonators:B012](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manual-resonators-blocks.json).

### REQ-DR-RESONATORS-009 — Effective audio, timing and edge behavior

**U.** Effective audio output, numeric gain/mix/filter/delay laws, sample-rate and block dependence, latency/compensation, silence floor, modulation phase, transition timing, feedback stability and tail completion remain unresolved. Randomness where applicable has no specified seed, distribution or repeatability. No source-derived parameter name/preset proves these outcomes.

### REQ-DR-RESONATORS-010 — Automation, persistence and lifecycle

**U.** Parameter automation/mapping eligibility, control ownership, state transition granularity, undo/redo grouping, saved/preset/tail/random-state persistence, malformed input handling, cancellation atomicity, missing dependencies and device/Set/audio-engine teardown are unresolved. Common editing/storage owners apply only within their published scopes; these device-specific outcomes are not inferred from generic actions.

## Acceptance cases

The [full case definitions](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/cases.json)
are part of this draft: each stable ID names setup, action, input fixture,
requirement, documentary or unknown expectation, comparison rule, evidence
locator and execution state. The following index maps every case to its
individual requirement; use the JSON action/expected fields for the complete
finite scenario. The [requirements index](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/requirements.json)
is a derived machine-readable copy of the clauses above. Canonical wording
remains this page; the author snapshot pins the reviewed wording.

Every device has positive, negative or inactive-path, boundary, automation,
persistence, undo, malformed, cancellation, teardown, sample-rate and sidechain
case definitions. Missing/rejected sidechain availability is U: the absence of
an external-sidechain section proves no interface outcome. Echo's internal
Ducking/envelope follower is not an external-routing protocol. Where no
operation/endpoint is offered, record that observation as U rather than silently
skipping it. Rare/high-feedback or long/frozen tails remain open obligations;
a finite capture cannot establish an infinite or complete tail.

| Device | Requirements | D12 clauses | U clauses | Cases | D12 / Dpkg / U cases |
| --- | --- | --- | --- | --- | --- |
| Delay | 14 | 12 | 2 | 22 | 12 / 1 / 9 |
| Echo | 18 | 15 | 3 | 26 | 15 / 1 / 10 |
| Filter Delay | 8 | 6 | 2 | 16 | 6 / 1 / 9 |
| Grain Delay | 8 | 6 | 2 | 17 | 6 / 1 / 10 |
| Reverb | 13 | 11 | 2 | 21 | 11 / 1 / 9 |
| Hybrid Reverb | 21 | 19 | 2 | 29 | 19 / 1 / 9 |
| Resonators | 10 | 8 | 2 | 18 | 8 / 1 / 9 |

Total: **92 requirements (77 D12, 15 U), 149 case definitions (77 D12, seven Dpkg, 65 U)**. No exact-build behavior is graded.

### Delay case index

| Case ID | Requirement | Kind | Scenario | Evidence grade |
| --- | --- | --- | --- | --- |
| DR-DELAY-001 | REQ-DR-DELAY-001 | boundary | Time and tempo-synchronized divisions | D12; exact build U |
| DR-DELAY-002 | REQ-DR-DELAY-002 | positive | Stereo Link and independent offsets | D12; exact build U |
| DR-DELAY-003 | REQ-DR-DELAY-003 | positive | Feedback paths | D12; exact build U |
| DR-DELAY-004 | REQ-DR-DELAY-004 | negative | Freeze admission and buffer cycling | D12; exact build U |
| DR-DELAY-005 | REQ-DR-DELAY-005 | positive | Input band-pass filter | D12; exact build U |
| DR-DELAY-006 | REQ-DR-DELAY-006 | positive | Modulation targets and section visibility | D12; exact build U |
| DR-DELAY-007 | REQ-DR-DELAY-007 | positive | LFO modes, shapes and Morph | D12; exact build U |
| DR-DELAY-008 | REQ-DR-DELAY-008 | positive | Timing transitions | D12; exact build U |
| DR-DELAY-009 | REQ-DR-DELAY-009 | positive | Ping Pong | D12; exact build U |
| DR-DELAY-010 | REQ-DR-DELAY-010 | positive | Dry/Wet | D12; exact build U |
| DR-DELAY-011 | REQ-DR-DELAY-011 | positive | Hi-Quality context option | D12; exact build U |
| DR-DELAY-012 | REQ-DR-DELAY-012 | positive | Equal-Loudness context option | D12; exact build U |
| DR-DELAY-013 | REQ-DR-DELAY-013 | sample-rate | Sample-rate and timing boundary | U; exact build U |
| DR-DELAY-014 | REQ-DR-DELAY-013 | boundary | Silence and tail boundary | U; exact build U |
| DR-DELAY-015 | REQ-DR-DELAY-013 | sidechain | External sidechain admission | U; exact build U |
| DR-DELAY-016 | REQ-DR-DELAY-014 | automation | Automation and ownership | U; exact build U |
| DR-DELAY-017 | REQ-DR-DELAY-014 | persistence | Set and preset persistence | U; exact build U |
| DR-DELAY-018 | REQ-DR-DELAY-014 | undo | Undo and redo | U; exact build U |
| DR-DELAY-019 | REQ-DR-DELAY-014 | malformed | Malformed and missing input | U; exact build U |
| DR-DELAY-020 | REQ-DR-DELAY-014 | cancel | Cancel and interrupted gesture | U; exact build U |
| DR-DELAY-021 | REQ-DR-DELAY-014 | teardown | Removal, bypass and teardown | U; exact build U |
| DR-DELAY-022 | REQ-DR-DELAY-014 | package | Retained installed profile | Dpkg; exact build U |

### Echo case index

| Case ID | Requirement | Kind | Scenario | Evidence grade |
| --- | --- | --- | --- | --- |
| DR-ECHO-001 | REQ-DR-ECHO-001 | positive | Channel modes | D12; exact build U |
| DR-ECHO-002 | REQ-DR-ECHO-002 | negative | Delay units and Sync Mode | D12; exact build U |
| DR-ECHO-003 | REQ-DR-ECHO-003 | positive | Stereo Link and offsets | D12; exact build U |
| DR-ECHO-004 | REQ-DR-ECHO-004 | positive | Input gain and dry distortion | D12; exact build U |
| DR-ECHO-005 | REQ-DR-ECHO-005 | positive | Feedback and inversion | D12; exact build U |
| DR-ECHO-006 | REQ-DR-ECHO-006 | positive | Echo Tunnel | D12; exact build U |
| DR-ECHO-007 | REQ-DR-ECHO-007 | positive | Filters and display | D12; exact build U |
| DR-ECHO-008 | REQ-DR-ECHO-008 | positive | LFO wave, rate and phase | D12; exact build U |
| DR-ECHO-009 | REQ-DR-ECHO-009 | positive | Modulation targets and x4 | D12; exact build U |
| DR-ECHO-010 | REQ-DR-ECHO-010 | boundary | Envelope versus LFO source | D12; exact build U |
| DR-ECHO-011 | REQ-DR-ECHO-011 | positive | Input gate and wet ducking | D12; exact build U |
| DR-ECHO-012 | REQ-DR-ECHO-012 | positive | Noise and Wobble | D12; exact build U |
| DR-ECHO-013 | REQ-DR-ECHO-013 | positive | Repitch versus crossfade | D12; exact build U |
| DR-ECHO-014 | REQ-DR-ECHO-014 | boundary | Idle shutdown exception | U; exact build U |
| DR-ECHO-015 | REQ-DR-ECHO-015 | positive | Reverb placement and decay | D12; exact build U |
| DR-ECHO-016 | REQ-DR-ECHO-016 | boundary | Stereo width, output and mix | D12; exact build U |
| DR-ECHO-017 | REQ-DR-ECHO-017 | sample-rate | Sample-rate and timing boundary | U; exact build U |
| DR-ECHO-018 | REQ-DR-ECHO-017 | boundary | Silence and tail boundary | U; exact build U |
| DR-ECHO-019 | REQ-DR-ECHO-017 | sidechain | External sidechain admission | U; exact build U |
| DR-ECHO-020 | REQ-DR-ECHO-018 | automation | Automation and ownership | U; exact build U |
| DR-ECHO-021 | REQ-DR-ECHO-018 | persistence | Set and preset persistence | U; exact build U |
| DR-ECHO-022 | REQ-DR-ECHO-018 | undo | Undo and redo | U; exact build U |
| DR-ECHO-023 | REQ-DR-ECHO-018 | malformed | Malformed and missing input | U; exact build U |
| DR-ECHO-024 | REQ-DR-ECHO-018 | cancel | Cancel and interrupted gesture | U; exact build U |
| DR-ECHO-025 | REQ-DR-ECHO-018 | teardown | Removal, bypass and teardown | U; exact build U |
| DR-ECHO-026 | REQ-DR-ECHO-018 | package | Retained installed profile | Dpkg; exact build U |

### Filter Delay case index

| Case ID | Requirement | Kind | Scenario | Evidence grade |
| --- | --- | --- | --- | --- |
| DR-FILTER-DELAY-001 | REQ-DR-FILTER-DELAY-001 | negative | Three delay inputs and output panning | D12; exact build U |
| DR-FILTER-DELAY-002 | REQ-DR-FILTER-DELAY-002 | positive | Filters and feedback routing | D12; exact build U |
| DR-FILTER-DELAY-003 | REQ-DR-FILTER-DELAY-003 | boundary | Sync and fractional timing | D12; exact build U |
| DR-FILTER-DELAY-004 | REQ-DR-FILTER-DELAY-004 | positive | Milliseconds editing | D12; exact build U |
| DR-FILTER-DELAY-005 | REQ-DR-FILTER-DELAY-005 | positive | Feedback | D12; exact build U |
| DR-FILTER-DELAY-006 | REQ-DR-FILTER-DELAY-006 | boundary | Line levels and Dry | D12; exact build U |
| DR-FILTER-DELAY-007 | REQ-DR-FILTER-DELAY-007 | sample-rate | Sample-rate and timing boundary | U; exact build U |
| DR-FILTER-DELAY-008 | REQ-DR-FILTER-DELAY-007 | boundary | Silence and tail boundary | U; exact build U |
| DR-FILTER-DELAY-009 | REQ-DR-FILTER-DELAY-007 | sidechain | External sidechain admission | U; exact build U |
| DR-FILTER-DELAY-010 | REQ-DR-FILTER-DELAY-008 | automation | Automation and ownership | U; exact build U |
| DR-FILTER-DELAY-011 | REQ-DR-FILTER-DELAY-008 | persistence | Set and preset persistence | U; exact build U |
| DR-FILTER-DELAY-012 | REQ-DR-FILTER-DELAY-008 | undo | Undo and redo | U; exact build U |
| DR-FILTER-DELAY-013 | REQ-DR-FILTER-DELAY-008 | malformed | Malformed and missing input | U; exact build U |
| DR-FILTER-DELAY-014 | REQ-DR-FILTER-DELAY-008 | cancel | Cancel and interrupted gesture | U; exact build U |
| DR-FILTER-DELAY-015 | REQ-DR-FILTER-DELAY-008 | teardown | Removal, bypass and teardown | U; exact build U |
| DR-FILTER-DELAY-016 | REQ-DR-FILTER-DELAY-008 | package | Retained installed profile | Dpkg; exact build U |

### Grain Delay case index

| Case ID | Requirement | Kind | Scenario | Evidence grade |
| --- | --- | --- | --- | --- |
| DR-GRAIN-DELAY-001 | REQ-DR-GRAIN-DELAY-001 | positive | Grains and Frequency | D12; exact build U |
| DR-GRAIN-DELAY-002 | REQ-DR-GRAIN-DELAY-002 | positive | X/Y assignments | D12; exact build U |
| DR-GRAIN-DELAY-003 | REQ-DR-GRAIN-DELAY-003 | boundary | Synchronized delay and milliseconds | D12; exact build U |
| DR-GRAIN-DELAY-004 | REQ-DR-GRAIN-DELAY-004 | positive | Spray random delay | D12; exact build U |
| DR-GRAIN-DELAY-005 | REQ-DR-GRAIN-DELAY-005 | positive | Pitch and Random Pitch | D12; exact build U |
| DR-GRAIN-DELAY-006 | REQ-DR-GRAIN-DELAY-006 | positive | Feedback and dry/wet | D12; exact build U |
| DR-GRAIN-DELAY-007 | REQ-DR-GRAIN-DELAY-007 | sample-rate | Sample-rate and timing boundary | U; exact build U |
| DR-GRAIN-DELAY-008 | REQ-DR-GRAIN-DELAY-007 | boundary | Silence and tail boundary | U; exact build U |
| DR-GRAIN-DELAY-009 | REQ-DR-GRAIN-DELAY-007 | negative | Zero random-control boundary | U; exact build U |
| DR-GRAIN-DELAY-010 | REQ-DR-GRAIN-DELAY-007 | sidechain | External sidechain admission | U; exact build U |
| DR-GRAIN-DELAY-011 | REQ-DR-GRAIN-DELAY-008 | automation | Automation and ownership | U; exact build U |
| DR-GRAIN-DELAY-012 | REQ-DR-GRAIN-DELAY-008 | persistence | Set and preset persistence | U; exact build U |
| DR-GRAIN-DELAY-013 | REQ-DR-GRAIN-DELAY-008 | undo | Undo and redo | U; exact build U |
| DR-GRAIN-DELAY-014 | REQ-DR-GRAIN-DELAY-008 | malformed | Malformed and missing input | U; exact build U |
| DR-GRAIN-DELAY-015 | REQ-DR-GRAIN-DELAY-008 | cancel | Cancel and interrupted gesture | U; exact build U |
| DR-GRAIN-DELAY-016 | REQ-DR-GRAIN-DELAY-008 | teardown | Removal, bypass and teardown | U; exact build U |
| DR-GRAIN-DELAY-017 | REQ-DR-GRAIN-DELAY-008 | package | Retained installed profile | Dpkg; exact build U |

### Reverb case index

| Case ID | Requirement | Kind | Scenario | Evidence grade |
| --- | --- | --- | --- | --- |
| DR-REVERB-001 | REQ-DR-REVERB-001 | positive | Input filters | D12; exact build U |
| DR-REVERB-002 | REQ-DR-REVERB-002 | positive | Early reflections and Spin | D12; exact build U |
| DR-REVERB-003 | REQ-DR-REVERB-003 | positive | Shape | D12; exact build U |
| DR-REVERB-004 | REQ-DR-REVERB-004 | positive | Diffuse tail and shelving | D12; exact build U |
| DR-REVERB-005 | REQ-DR-REVERB-005 | positive | Diffusion and Scale | D12; exact build U |
| DR-REVERB-006 | REQ-DR-REVERB-006 | positive | Chorus | D12; exact build U |
| DR-REVERB-007 | REQ-DR-REVERB-007 | boundary | Predelay | D12; exact build U |
| DR-REVERB-008 | REQ-DR-REVERB-008 | positive | Size and Smooth | D12; exact build U |
| DR-REVERB-009 | REQ-DR-REVERB-009 | positive | Decay definition | D12; exact build U |
| DR-REVERB-010 | REQ-DR-REVERB-010 | negative | Freeze, Flat and Cut | D12; exact build U |
| DR-REVERB-011 | REQ-DR-REVERB-011 | boundary | Stereo, Density and output | D12; exact build U |
| DR-REVERB-012 | REQ-DR-REVERB-012 | sample-rate | Sample-rate and timing boundary | U; exact build U |
| DR-REVERB-013 | REQ-DR-REVERB-012 | boundary | Silence and tail boundary | U; exact build U |
| DR-REVERB-014 | REQ-DR-REVERB-012 | sidechain | External sidechain admission | U; exact build U |
| DR-REVERB-015 | REQ-DR-REVERB-013 | automation | Automation and ownership | U; exact build U |
| DR-REVERB-016 | REQ-DR-REVERB-013 | persistence | Set and preset persistence | U; exact build U |
| DR-REVERB-017 | REQ-DR-REVERB-013 | undo | Undo and redo | U; exact build U |
| DR-REVERB-018 | REQ-DR-REVERB-013 | malformed | Malformed and missing input | U; exact build U |
| DR-REVERB-019 | REQ-DR-REVERB-013 | cancel | Cancel and interrupted gesture | U; exact build U |
| DR-REVERB-020 | REQ-DR-REVERB-013 | teardown | Removal, bypass and teardown | U; exact build U |
| DR-REVERB-021 | REQ-DR-REVERB-013 | package | Retained installed profile | Dpkg; exact build U |

### Hybrid Reverb case index

| Case ID | Requirement | Kind | Scenario | Evidence grade |
| --- | --- | --- | --- | --- |
| DR-HYBRID-REVERB-001 | REQ-DR-HYBRID-REVERB-001 | positive | Wet send and predelay | D12; exact build U |
| DR-HYBRID-REVERB-002 | REQ-DR-HYBRID-REVERB-002 | boundary | Serial routing | D12; exact build U |
| DR-HYBRID-REVERB-003 | REQ-DR-HYBRID-REVERB-003 | boundary | Parallel routing | D12; exact build U |
| DR-HYBRID-REVERB-004 | REQ-DR-HYBRID-REVERB-004 | negative | Single-engine routing and disabled controls | D12; exact build U |
| DR-HYBRID-REVERB-005 | REQ-DR-HYBRID-REVERB-005 | boundary | IR selection and display | D12; exact build U |
| DR-HYBRID-REVERB-006 | REQ-DR-HYBRID-REVERB-006 | positive | User IR import and removal | D12; exact build U |
| DR-HYBRID-REVERB-007 | REQ-DR-HYBRID-REVERB-007 | positive | Convolution envelope | D12; exact build U |
| DR-HYBRID-REVERB-008 | REQ-DR-HYBRID-REVERB-008 | positive | Algorithms and common controls | D12; exact build U |
| DR-HYBRID-REVERB-009 | REQ-DR-HYBRID-REVERB-009 | positive | Freeze versus Freeze In | D12; exact build U |
| DR-HYBRID-REVERB-010 | REQ-DR-HYBRID-REVERB-010 | positive | Dark Hall controls | D12; exact build U |
| DR-HYBRID-REVERB-011 | REQ-DR-HYBRID-REVERB-011 | positive | Quartz controls | D12; exact build U |
| DR-HYBRID-REVERB-012 | REQ-DR-HYBRID-REVERB-012 | negative | Shimmer controls and zero amount | D12; exact build U |
| DR-HYBRID-REVERB-013 | REQ-DR-HYBRID-REVERB-013 | boundary | Tides modulation | D12; exact build U |
| DR-HYBRID-REVERB-014 | REQ-DR-HYBRID-REVERB-014 | positive | Prism band decay controls | D12; exact build U |
| DR-HYBRID-REVERB-015 | REQ-DR-HYBRID-REVERB-015 | positive | EQ placement and enable | D12; exact build U |
| DR-HYBRID-REVERB-016 | REQ-DR-HYBRID-REVERB-016 | boundary | EQ bands | D12; exact build U |
| DR-HYBRID-REVERB-017 | REQ-DR-HYBRID-REVERB-017 | boundary | Wet width and Dry/Wet | D12; exact build U |
| DR-HYBRID-REVERB-018 | REQ-DR-HYBRID-REVERB-018 | positive | Vintage | D12; exact build U |
| DR-HYBRID-REVERB-019 | REQ-DR-HYBRID-REVERB-019 | positive | Bass Mono | D12; exact build U |
| DR-HYBRID-REVERB-020 | REQ-DR-HYBRID-REVERB-020 | sample-rate | Sample-rate and timing boundary | U; exact build U |
| DR-HYBRID-REVERB-021 | REQ-DR-HYBRID-REVERB-020 | boundary | Silence and tail boundary | U; exact build U |
| DR-HYBRID-REVERB-022 | REQ-DR-HYBRID-REVERB-020 | sidechain | External sidechain admission | U; exact build U |
| DR-HYBRID-REVERB-023 | REQ-DR-HYBRID-REVERB-021 | automation | Automation and ownership | U; exact build U |
| DR-HYBRID-REVERB-024 | REQ-DR-HYBRID-REVERB-021 | persistence | Set and preset persistence | U; exact build U |
| DR-HYBRID-REVERB-025 | REQ-DR-HYBRID-REVERB-021 | undo | Undo and redo | U; exact build U |
| DR-HYBRID-REVERB-026 | REQ-DR-HYBRID-REVERB-021 | malformed | Malformed and missing input | U; exact build U |
| DR-HYBRID-REVERB-027 | REQ-DR-HYBRID-REVERB-021 | cancel | Cancel and interrupted gesture | U; exact build U |
| DR-HYBRID-REVERB-028 | REQ-DR-HYBRID-REVERB-021 | teardown | Removal, bypass and teardown | U; exact build U |
| DR-HYBRID-REVERB-029 | REQ-DR-HYBRID-REVERB-021 | package | Retained installed profile | Dpkg; exact build U |

### Resonators case index

| Case ID | Requirement | Kind | Scenario | Evidence grade |
| --- | --- | --- | --- | --- |
| DR-RESONATORS-001 | REQ-DR-RESONATORS-001 | positive | Five resonators and mode | D12; exact build U |
| DR-RESONATORS-002 | REQ-DR-RESONATORS-002 | positive | Input filter | D12; exact build U |
| DR-RESONATORS-003 | REQ-DR-RESONATORS-003 | positive | Decay, Const and Color | D12; exact build U |
| DR-RESONATORS-004 | REQ-DR-RESONATORS-004 | positive | Channel assignments | D12; exact build U |
| DR-RESONATORS-005 | REQ-DR-RESONATORS-005 | positive | Root tuning and context | D12; exact build U |
| DR-RESONATORS-006 | REQ-DR-RESONATORS-006 | boundary | Note, Fine and relative ranges | D12; exact build U |
| DR-RESONATORS-007 | REQ-DR-RESONATORS-007 | positive | Independent enable and gain | D12; exact build U |
| DR-RESONATORS-008 | REQ-DR-RESONATORS-008 | negative | Wet width, gain and balance | D12; exact build U |
| DR-RESONATORS-009 | REQ-DR-RESONATORS-009 | sample-rate | Sample-rate and timing boundary | U; exact build U |
| DR-RESONATORS-010 | REQ-DR-RESONATORS-009 | boundary | Silence and tail boundary | U; exact build U |
| DR-RESONATORS-011 | REQ-DR-RESONATORS-009 | sidechain | External sidechain admission | U; exact build U |
| DR-RESONATORS-012 | REQ-DR-RESONATORS-010 | automation | Automation and ownership | U; exact build U |
| DR-RESONATORS-013 | REQ-DR-RESONATORS-010 | persistence | Set and preset persistence | U; exact build U |
| DR-RESONATORS-014 | REQ-DR-RESONATORS-010 | undo | Undo and redo | U; exact build U |
| DR-RESONATORS-015 | REQ-DR-RESONATORS-010 | malformed | Malformed and missing input | U; exact build U |
| DR-RESONATORS-016 | REQ-DR-RESONATORS-010 | cancel | Cancel and interrupted gesture | U; exact build U |
| DR-RESONATORS-017 | REQ-DR-RESONATORS-010 | teardown | Removal, bypass and teardown | U; exact build U |
| DR-RESONATORS-018 | REQ-DR-RESONATORS-010 | package | Retained installed profile | Dpkg; exact build U |

## Errors, timing, persistence and interactions

The last two requirements per device retain its unresolved numeric/runtime and
lifecycle outcomes. There is no assumed acceptance/clamp rule for malformed
numeric text, out-of-range values, corrupt presets, absent IRs, interrupted
load/save, unsupported codecs, permissions or engine loss. No transaction
atomicity, generic Esc rollback, undo grouping, teardown silence, feedback
limiter or durable buffer/random-state guarantee is claimed.

Automation cases target a control only when its UI actually offers that target;
the existing envelope law does not prove this device consumes it at the same
sample/clock granularity. Tempo-synchronized nominal delay does not establish
the result of transport stop/start, seek, loop, tempo automation or a live
sample-rate change. Sample-rate cases explicitly retain 44.1/48/96 kHz and
64/512-frame observations as unknown. Real-time/offline differences, disabled
processing CPU behavior and rack-tail interactions remain open.

Hybrid Reverb IR import User-list reset on remove/reinsert is a documentary
clause, not a promise that a saved Set loses or restores its IR. Saved media
reference and transient category list are separate state. Resonators tuning
units do not define frequency calculations or override the Set-level tuning
owner. Missing input, inactive engines and silent paths cannot be used to
approve a no-effect contract without the fixture gates above.

## Analyst-only evidence appendix

The [source catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/sources.json)
retains the official [Live 12 audio-effect chapter](https://www.ableton.com/en/live-manual/12/live-audio-effect-reference/)
URL/capture date, original audio-utilities capture identity and external pins.
Reused HTML SHA-256 is `9cb15cb3d80bda4771e5add2c2b74f5c57d73ee8850e198acf7cf8a51dfd1299`;
shipped `12.0_12402.txt` SHA-256 is
`b7c9d4c767d8ca9b346ce7d517265446bbacd6de366cc058e155613789d0f299`.
The seven bounded preset copies and their historical Creator attributes only
establish installed-byte field/profile observations. They are not exact-build
saved outputs or constructor/default/audio proof.

The [author manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/manifest-author-r2.json)
pins canonical page snapshots, source extracts, declarative cases/fixtures and
validation. This is an author freeze for independent analyst review, not a
handoff, independent approval or compatibility result. Retain source/case
versions when correcting it. Revision 2 addresses DR-REVIEW-001 by retaining
Echo idle shutdown as an ungraded application probe. The exact revision 1 seal and
all 32 payloads are preserved in [archive-r1](../../analysis/ableton-live-12.4.3/full-spec-v1/delay-reverb/archive-r1/manifest-author-r1.json).
No original program/function, emulator, hardware
or candidate was run; no tool installation, publication or commit was made.
