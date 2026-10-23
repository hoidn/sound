---
id: SPEC-BUNDLED-DEVICE-WORKFLOWS
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3; Live 12 documentary applicability unresolved
---

# Broader workflows for seven bundled devices

## Scope, provenance and ownership

This partial F-06 draft owns previously unowned documented presentation,
control eligibility, copy/routing gestures, envelope/glide/unison modes and
MIDI/MPE destination workflows for Analog, Collision, Corpus, Electric, Tension,
Amp and Cabinet. [Coverage design](../research/full-live-specification-design.md)
governs closure; [research](../research/bundled-device-workflows.md) owns source
interpretation. No complete device, released handoff or compatibility is claimed.

D12 is the retained official Version 12 manual; **every new runtime clause is
exact-12.4.3 U**, including controls of devices with existing finite X evidence.
All case target expectations/comparisons are null, all grades U and all cases
unexecuted. Documentary control/state predicates compare visible options or
exposed values only. Signal/lifecycle cases have null documentary oracles.
Models and public signal-role descriptions mandate no private circuit, kernel,
voice architecture, host identity or platform emulation.

The [bundled parameter owner](bundled-device-parameters.md) retains exact storage,
parameter paths/domains/defaults and reviewed label mappings. This page never
assigns stored numeric indices, derives engine units or replaces its malformed-
reader clauses. [Bundled hosting](bundled-device-hosting.md) owns its conditional
Amp/Cabinet composition; supplied wet audio is still an explicit dependency.
The [individual audio owners](#existing-finite-authorities) retain every finite
DSP/vector law, measurement and scope condition. A matching control name or a
manual paragraph does not extend a finite release to another mode or controller.

[Device racks](device-racks.md) owns common insertion, presets, rack copy/mixing;
[MPE](mpe-workflows.md), [tuning](tuning-systems.md),
[automation](automation-envelopes.md), [routing](routing-monitoring-latency.md),
[playback](playback-core.md) and [Set structure](live-set-structure.md) keep their
bounded owners. Links do not prove the composition or fill their unknowns.

## Existing finite authorities

| Device | Current authoritative scope | Immutable finite release |
| --- | --- | --- |
| Analog | [Analog](device-analog.md), especially REQ021/023 open modes/controllers; existing wave/filter/envelope/priority formulas remain there | [device-analog-v1](../../handoff/device-analog-v1/README.md), 38 groups / 42 evaluations only |
| Collision | [Collision](device-collision.md), especially REQ016–018; enabled resonators, order, note/voice and finite outputs remain there | [device-collision-v1](../../handoff/device-collision-v1/README.md), two cases only |
| Corpus | [Corpus](device-corpus.md), especially REQ011–013 sync/MIDI/dynamic boundaries; constant-parameter mix/models remain there | [device-corpus-v1](../../handoff/device-corpus-v1/README.md), 24 groups / 68 evaluations only |
| Electric | [Electric](device-electric.md), especially REQ016 per-note/controller gap; pitch/Stretch/global bend/voices/component laws remain there | [device-electric-v2](../../handoff/device-electric-v2/README.md), 117 evaluations only |
| Tension | [Tension](device-tension.md), especially REQ014/015 modulation/priority/MPE gaps; component/voice and retained render-defined laws remain there | [device-tension-v1](../../handoff/device-tension-v1/README.md), 27 cases only |
| Amp / Cabinet | [Parameters](bundled-device-parameters.md) and [host composition](bundled-device-hosting.md); no new wet DSP is provided | No finite Amp/Cabinet audio release; original execution route remains blocked |

These snapshots and release manifests are pinned by the new author packet as
unchanged authority references. Their extracted original evidence is neither a
run of Live nor evidence for arbitrary app interaction. No comparator or device
binary from those releases is executed for this work.

## Inputs and positive controls

The [fixtures](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/fixtures.json)
are future finite setups only. Retain accepted visible controls, actual source/
controller routing, enabled sections, nonzero output/wet contribution and an
independently known positive baseline before no-effect/zero/ineligible tests.
Collision needs active excitation and an enabled audible resonator; Tension
needs a productive exciter/string combination. Corpus must distinguish prior
resonance from new excitation. Amp/Cabinet require an independently qualified
wet path, which is not available or proven by this packet. Absence/silence/zero
or an inactive path remains inconclusive rather than passing a control claim.

Amp/Cabinet audio execution is blocked. No fake Live identity, CoreFoundation/
Objective-C host, native probe, original function, emulator, installation or
candidate is created or run. A future fixture requirement is not evidence that
such a route works. Hardware/controller/codec availability is likewise unknown.

## Individual requirements

## Analog

### REQ-BDW-AN-001 — Panel selection

**D12/target-U.** Selecting a shell section changes its detail display; Noise has no separate detail display. The Global MPE switch reveals Pressure, Slide and NotePB controls. This specifies presentation, not synthesis structure.

Evidence: [analog:B007](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-analog-blocks.json), [analog:B022](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-analog-blocks.json), [analog:B072](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-analog-blocks.json).

### REQ-BDW-AN-002 — Shape and LFO control eligibility

**D12/target-U.** Pulse Width is editable for the rectangular oscillator shape; oscillator Width-LFO and Pitch-LFO modulation controls require their corresponding LFO enabled. The existing oscillator laws are not restated.

Evidence: [analog:B012](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-analog-blocks.json), [analog:B014](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-analog-blocks.json).

### REQ-BDW-AN-003 — Quick Routing and preserved edits

**D12/target-U.** Quick Routing selects four layouts: upper-left gives each oscillator its own filter/amplifier; upper-right sends each oscillator to both filters; lower-left sends both to Filter 1/Amp 1 only; lower-right sends both through Filter 1 into Filter 2/Amp 2. The gesture preserves oscillator level, tuning and waveform edits. Exact signal coefficients remain with the Analog owner.

Evidence: [analog:B064](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-analog-blocks.json), [analog:B065](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-analog-blocks.json).

### REQ-BDW-AN-004 — Filter Follow control context

**D12/target-U.** Filter 2 Follow changes its cutoff control to an offset from Filter 1, including the documented following of Filter 1 cutoff modulation. Exact tracking and modulation arithmetic remain U here.

Evidence: [analog:B027](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-analog-blocks.json).

### REQ-BDW-AN-005 — Envelope modes beyond finite renders

**D12/target-U.** Envelope Legato reuses the current envelope position for overlapping notes; Free skips sustain. Loop offers Off, AD-R, ADR-R and ADS-R; Free in AD-R/ADR-R treats notes as held, while ADS-R repeats attack/release at key release. These documentary mode roles do not supply curves, timing or a target reset law.

Evidence: [analog:B043](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-analog-blocks.json), [analog:B044](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-analog-blocks.json), [analog:B045](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-analog-blocks.json), [analog:B046](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-analog-blocks.json), [analog:B047](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-analog-blocks.json), [analog:B048](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-analog-blocks.json).

### REQ-BDW-AN-006 — LFO timing and shape controls

**D12/target-U.** Each LFO offers Hz/sync rate, Delay/Attack and Retrig/Offset. Width is editable for triangle/rectangle and disabled for sine/noise. Existing free-running waveform laws are not expanded by these UI and sync descriptions.

Evidence: [analog:B051](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-analog-blocks.json), [analog:B052](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-analog-blocks.json), [analog:B053](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-analog-blocks.json), [analog:B054](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-analog-blocks.json).

### REQ-BDW-AN-007 — Vibrato activation and wheel amount

**D12/target-U.** Vibrato activation exposes its additional controls; Amt < MW is relative to the shell Vibrato Amount. Error describes per-voice random variation without a distribution or reproducibility rule.

Evidence: [analog:B058](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-analog-blocks.json), [analog:B059](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-analog-blocks.json).

### REQ-BDW-AN-008 — Unison workflow

**D12/target-U.** Uni enables additional Unison Voices/Delay controls and Detune variation. These are stacked-voice controls, distinct from keyboard polyphony; no voice-budget formula or delayed-onset tolerance is added.

Evidence: [analog:B060](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-analog-blocks.json), [analog:B061](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-analog-blocks.json).

### REQ-BDW-AN-009 — Glide workflow

**D12/target-U.** Gli exposes Glide Mode; Legato limits slides to overlapping notes. Const and Prop distinguish interval-independent versus interval-dependent glide time, without an interpolation or first-note law.

Evidence: [analog:B062](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-analog-blocks.json), [analog:B063](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-analog-blocks.json).

### REQ-BDW-AN-010 — MPE destinations and bend controls

**D12/target-U.** Pressure and Slide each offer two destinations with individual amounts and input-activity LEDs. Note PB sets per-note bend range, separately from global PB Range. Destinations/domains/codecs not established by this text remain U.

Evidence: [analog:B067](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-analog-blocks.json), [analog:B073](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-analog-blocks.json), [analog:B074](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-analog-blocks.json), [analog:B075](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-analog-blocks.json), [analog:B076](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-analog-blocks.json).

### REQ-BDW-AN-U-SIGNAL — Unresolved broader signal and expression results

**U/target-U.** Exact broader output, MPE/controller/tuning response, modulation/voice/loop/glide phase and transitions, numerical domains, timing and random laws remain unknown outside the explicitly linked finite contracts. D12 does not expand any released vector or infer a new parameter codec.

### REQ-BDW-AN-U-LIFECYCLE — Required workflow lifecycle and error outcomes

**U/target-U.** Automation/mapping ownership, persistence and migration, malformed/out-of-domain edits or files, undo grouping, cancellation, transport/rate/engine changes, source loss, running tails and teardown remain required unknowns. Public controls and stored fields supply no transaction, recovery or host architecture.

## Collision

### REQ-BDW-CL-001 — Tabs and presentation

**D12/target-U.** Resonator, LFO and MIDI/MPE tabs expose their corresponding controls, alongside global voice/retrigger/structure/output controls. The existing resonator-order and finite voice laws remain with the Collision owner.

Evidence: [collision:B006](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-collision-blocks.json), [collision:B007](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-collision-blocks.json), [collision:B008](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-collision-blocks.json).

### REQ-BDW-CL-002 — Resonator-dependent eligibility

**D12/target-U.** Object selection updates the X-Y visualization. Pipe/Tube omit Quality and replace Material with Radius; their Brightness/Inharm/Hit/listening controls are not used. Ratio is for Membrane/Plate and Opening for Pipe. These are visible eligibility/role statements, not new modal or waveguide laws.

Evidence: [collision:B038](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-collision-blocks.json), [collision:B039](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-collision-blocks.json), [collision:B041](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-collision-blocks.json), [collision:B044](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-collision-blocks.json), [collision:B046](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-collision-blocks.json), [collision:B047](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-collision-blocks.json), [collision:B048](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-collision-blocks.json), [collision:B049](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-collision-blocks.json), [collision:B050](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-collision-blocks.json), [collision:B052](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-collision-blocks.json).

### REQ-BDW-CL-003 — Resonator copy buttons

**D12/target-U.** Each resonator has a directional copy button that copies its settings to the other resonator. This establishes exposed value copying, not an atomic transaction, tail copy or private-state cloning.

Evidence: [collision:B040](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-collision-blocks.json).

### REQ-BDW-CL-004 — LFO destinations and retrigger controls

**D12/target-U.** The two LFOs can target parameters and each other; each has two destination amounts relative to overall Amount. Rate supports Hz/sync; Offset sets the retrigger start phase. No lookup, scaling formula, random law or clock boundary is inferred.

Evidence: [collision:B062](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-collision-blocks.json), [collision:B063](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-collision-blocks.json), [collision:B064](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-collision-blocks.json), [collision:B065](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-collision-blocks.json), [collision:B066](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-collision-blocks.json).

### REQ-BDW-CL-005 — MIDI and MPE mapping destinations

**D12/target-U.** Pitch bend/per-note bend, wheel, pressure and slide can each map to two destinations with independent amounts; Key/Vel controls supply additional parameter modulation. No message codec, destination list or response law is invented.

Evidence: [collision:B068](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-collision-blocks.json), [collision:B069](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-collision-blocks.json).

### REQ-BDW-CL-006 — Repeated-note Retrig workflow

**D12/target-U.** Global Retrig is documented to retrigger an already-playing note rather than add a voice. Duplicate-note pairing, release velocity and target allocation remain U and do not expand the existing finite voice contract.

Evidence: [collision:B073](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-collision-blocks.json).

### REQ-BDW-CL-U-SIGNAL — Unresolved broader signal and expression results

**U/target-U.** Exact broader output, MPE/controller/tuning response, modulation/voice/loop/glide phase and transitions, numerical domains, timing and random laws remain unknown outside the explicitly linked finite contracts. D12 does not expand any released vector or infer a new parameter codec.

### REQ-BDW-CL-U-LIFECYCLE — Required workflow lifecycle and error outcomes

**U/target-U.** Automation/mapping ownership, persistence and migration, malformed/out-of-domain edits or files, undo grouping, cancellation, transport/rate/engine changes, source loss, running tails and teardown remain required unknowns. Public controls and stored fields supply no transaction, recovery or host architecture.

## Corpus

### REQ-BDW-CO-001 — Model-dependent control presentation

**D12/target-U.** Model selection changes control eligibility: Pipe/Tube use Radius instead of Material and omit Quality/Bright/Inharm/Hit/listening/Bleed roles; Opening is Pipe-only and Ratio Membrane/Plate-only. Existing numerical model/position laws remain authoritative elsewhere.

Evidence: [corpus:B012](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-corpus-blocks.json), [corpus:B014](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-corpus-blocks.json), [corpus:B015](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-corpus-blocks.json), [corpus:B017](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-corpus-blocks.json), [corpus:B018](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-corpus-blocks.json), [corpus:B019](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-corpus-blocks.json), [corpus:B020](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-corpus-blocks.json), [corpus:B021](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-corpus-blocks.json), [corpus:B023](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-corpus-blocks.json), [corpus:B041](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-corpus-blocks.json).

### REQ-BDW-CO-002 — Sidechain access and MIDI source

**D12/target-U.** The title-bar toggle opens MIDI sidechain controls and indicates active sidechain use. MIDI From selects a source track and tap point; Frequency and Off Decay enable distinct modulation roles.

Evidence: [corpus:B045](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-corpus-blocks.json), [corpus:B046](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-corpus-blocks.json).

### REQ-BDW-CO-003 — Frequency mode and note priority

**D12/target-U.** Frequency-enabled sidechain follows MIDI note tuning with Last/Low priority for held notes and coarse/fine offsets plus PB Range. With Frequency off, Tune controls Hertz and a note/cents readout is shown. This adds documentary controls/roles, not a note-frequency or priority scheduling formula.

Evidence: [corpus:B024](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-corpus-blocks.json), [corpus:B025](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-corpus-blocks.json), [corpus:B047](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-corpus-blocks.json), [corpus:B048](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-corpus-blocks.json).

### REQ-BDW-CO-004 — Off Decay admission

**D12/target-U.** Off Decay makes MIDI Note Off reduce resonance according to its amount; the endpoints are described as ignoring Note Off versus muting it. No numeric decay, immediate deadline, sustain-pedal or held-note aggregation policy is established for the target.

Evidence: [corpus:B049](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-corpus-blocks.json).

### REQ-BDW-CO-005 — Synchronized LFO and stereo eligibility

**D12/target-U.** Sync exposes Offset; Spin is available only in Hz mode, where Phase/Spin can be selected. For noise waveforms Phase/Spin are described as ineffective; this is not random-sample identity or a new free-running waveform formula.

Evidence: [corpus:B029](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-corpus-blocks.json), [corpus:B033](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-corpus-blocks.json), [corpus:B034](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-corpus-blocks.json), [corpus:B035](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-corpus-blocks.json), [corpus:B036](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-corpus-blocks.json).

### REQ-BDW-CO-006 — Dry/Wet and running resonance

**D12/target-U.** The manual describes Dry/Wet as changing admission of new input without cutting resonances already sounding. This dynamic documentary statement does not replace the existing constant-parameter mix law or establish a tail-preservation tolerance.

Evidence: [corpus:B043](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-corpus-blocks.json).

### REQ-BDW-CO-007 — Limiter indication

**D12/target-U.** A LED next to Gain is documented as indicating automatic limiting at excessive level. No threshold, curve, ceiling, clipping rule or real-time performance oracle follows.

Evidence: [corpus:B042](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-corpus-blocks.json).

### REQ-BDW-CO-U-SIGNAL — Unresolved broader signal and expression results

**U/target-U.** Exact broader output, MPE/controller/tuning response, modulation/voice/loop/glide phase and transitions, numerical domains, timing and random laws remain unknown outside the explicitly linked finite contracts. D12 does not expand any released vector or infer a new parameter codec.

### REQ-BDW-CO-U-LIFECYCLE — Required workflow lifecycle and error outcomes

**U/target-U.** Automation/mapping ownership, persistence and migration, malformed/out-of-domain edits or files, undo grouping, cancellation, transport/rate/engine changes, source loss, running tails and teardown remain required unknowns. Public controls and stored fields supply no transaction, recovery or host architecture.

## Electric

### REQ-BDW-EL-001 — Section selection

**D12/target-U.** Clicking the Hammer, Fork and Damper/Pickup sections or their icons reveals their associated controls; Global has performance controls. The existing physical-component and pitch/voice laws are not repeated.

Evidence: [electric:B006](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-electric-blocks.json), [electric:B007](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-electric-blocks.json).

### REQ-BDW-EL-002 — Global versus per-note bend range

**D12/target-U.** Pitch Bend and Note PB address global and MPE per-note pitch-bend ranges separately. Existing extracted global-bend results do not establish per-note bend handling or these UI transitions.

Evidence: [electric:B036](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-electric-blocks.json).

### REQ-BDW-EL-U-SIGNAL — Unresolved broader signal and expression results

**U/target-U.** Exact broader output, MPE/controller/tuning response, modulation/voice/loop/glide phase and transitions, numerical domains, timing and random laws remain unknown outside the explicitly linked finite contracts. D12 does not expand any released vector or infer a new parameter codec.

### REQ-BDW-EL-U-LIFECYCLE — Required workflow lifecycle and error outcomes

**U/target-U.** Automation/mapping ownership, persistence and migration, malformed/out-of-domain edits or files, undo grouping, cancellation, transport/rate/engine changes, source loss, running tails and teardown remain required unknowns. Public controls and stored fields supply no transaction, recovery or host architecture.

## Tension

### REQ-BDW-TE-001 — Tabs, section toggles and shared Volume

**D12/target-U.** String and Filter/Global tabs expose their named sections; all sections except String and Keyboard have independent enables. The overall Volume is accessible from both tabs. No CPU saving or independent duplicate Volume parameter is required.

Evidence: [tension:B006](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-tension-blocks.json), [tension:B074](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-tension-blocks.json), [tension:B076](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-tension-blocks.json), [tension:B106](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-tension-blocks.json).

### REQ-BDW-TE-002 — Exciter-dependent controls

**D12/target-U.** The first exciter controls depend on selected type: Bow Force/Friction, Hammer variants Mass/Stiffness and Plectrum Protrusion/Stiffness. Damping is unavailable for Bow. Existing exciter models/ranges remain with their owners.

Evidence: [tension:B013](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-tension-blocks.json), [tension:B014](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-tension-blocks.json), [tension:B019](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-tension-blocks.json), [tension:B020](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-tension-blocks.json), [tension:B021](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-tension-blocks.json), [tension:B022](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-tension-blocks.json), [tension:B023](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-tension-blocks.json), [tension:B024](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-tension-blocks.json), [tension:B025](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-tension-blocks.json), [tension:B026](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-tension-blocks.json), [tension:B027](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-tension-blocks.json), [tension:B028](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-tension-blocks.json).

### REQ-BDW-TE-003 — Damper Gated and Velocity eligibility

**D12/target-U.** Damper Velocity is effective/enabled in the documented Gated context; Gated off leaves the damper applied and Velocity has no stated effect. The finite damper/decay law is not redefined.

Evidence: [tension:B042](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-tension-blocks.json).

### REQ-BDW-TE-004 — Filter modulation subsection gates

**D12/target-U.** Filter, Filter Envelope and Filter LFO have independent switches. The LFO/Env modulation sliders have no effect unless their corresponding subsections are enabled. No filter coefficient or modulation scaling law is added.

Evidence: [tension:B078](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-tension-blocks.json), [tension:B080](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-tension-blocks.json), [tension:B081](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-tension-blocks.json), [tension:B086](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-tension-blocks.json).

### REQ-BDW-TE-005 — Filter LFO sync and onset controls

**D12/target-U.** The filter LFO offers Hz/sync rate and Delay/Attack onset controls. Random choices are described but provide no seed, distribution or new waveform comparator.

Evidence: [tension:B087](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-tension-blocks.json), [tension:B088](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-tension-blocks.json), [tension:B089](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-tension-blocks.json).

### REQ-BDW-TE-006 — Vibrato wheel and Error controls

**D12/target-U.** Vibrato has an enable, Delay/Attack and Rate/Amount controls; wheel depth is relative to Amount and Error adds unspecified variation. Existing finite render-defined modulation does not cover these controller interactions.

Evidence: [tension:B054](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-tension-blocks.json), [tension:B055](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-tension-blocks.json), [tension:B056](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-tension-blocks.json), [tension:B057](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-tension-blocks.json), [tension:B058](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-tension-blocks.json).

### REQ-BDW-TE-007 — MPE destinations, indicators and bend ranges

**D12/target-U.** Pressure and Slide each have two destination/amount slots; pressure/slide/note-bend activity LEDs indicate input. Global Pitch Bend and Note PB ranges are distinct. MPE destination domains, codec and audio remain unknown.

Evidence: [tension:B090](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-tension-blocks.json), [tension:B091](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-tension-blocks.json), [tension:B092](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-tension-blocks.json).

### REQ-BDW-TE-008 — Portamento and Legato workflow

**D12/target-U.** Portamento enable/Time and Legato select note-slide context; Prop makes time interval-dependent while off is constant-time. This documentary role does not provide first-note behavior, a curve or a timing tolerance.

Evidence: [tension:B099](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-tension-blocks.json), [tension:B100](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-tension-blocks.json), [tension:B101](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-tension-blocks.json), [tension:B102](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-tension-blocks.json).

### REQ-BDW-TE-009 — Unison workflow

**D12/target-U.** Unison enables stacked-voice Voices, Detune and Delay controls, distinct from Keyboard polyphony. No stacked-voice allocation budget or onset/detune formula is specified here.

Evidence: [tension:B103](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-tension-blocks.json), [tension:B104](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-tension-blocks.json), [tension:B105](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-tension-blocks.json).

### REQ-BDW-TE-U-SIGNAL — Unresolved broader signal and expression results

**U/target-U.** Exact broader output, MPE/controller/tuning response, modulation/voice/loop/glide phase and transitions, numerical domains, timing and random laws remain unknown outside the explicitly linked finite contracts. D12 does not expand any released vector or infer a new parameter codec.

### REQ-BDW-TE-U-LIFECYCLE — Required workflow lifecycle and error outcomes

**U/target-U.** Automation/mapping ownership, persistence and migration, malformed/out-of-domain edits or files, undo grouping, cancellation, transport/rate/engine changes, source loss, running tails and teardown remain required unknowns. Public controls and stored fields supply no transaction, recovery or host architecture.

## Amp

### REQ-BDW-AM-001 — Consistent controls across models

**D12/target-U.** Selecting the already cataloged amp models uses a common set of controls. Model names/indices remain in the bundled-parameter owner; model changes do not establish parameter preservation, a reset policy or an emulated circuit design.

Evidence: [amp:B003](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-amp-blocks.json), [amp:B011](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-amp-blocks.json).

### REQ-BDW-AM-002 — Gain, Volume and tonal interactions

**D12/target-U.** Gain is the principal distortion control while Volume addresses output; EQ controls interact and Presence is model-dependent. These are documented control roles, not independent gain stages, transfer curves, coefficients or a private circuit requirement.

Evidence: [amp:B012](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-amp-blocks.json), [amp:B013](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-amp-blocks.json), [amp:B014](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-amp-blocks.json), [amp:B022](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-amp-blocks.json).

### REQ-BDW-AM-003 — Output processing selector

**D12/target-U.** Output selects mono or Dual processing. The CPU multiplier in the prose is context only; channel mapping and performance criteria are unknown. Labels/domains stay with the parameter owner.

Evidence: [amp:B015](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-amp-blocks.json).

### REQ-BDW-AM-004 — Separate and companion placement

**D12/target-U.** Amp and Cabinet may be used independently; the manual recommends Cabinet after Amp for the companion setup. This is an optional workflow, not automatic insertion or a required guitar-only input.

Evidence: [amp:B020](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-amp-blocks.json), [amp:B024](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-amp-blocks.json).

### REQ-BDW-AM-U-SIGNAL — Unresolved broader signal and expression results

**U/target-U.** Exact broader output, MPE/controller/tuning response, modulation/voice/loop/glide phase and transitions, numerical domains, timing and random laws remain unknown outside the explicitly linked finite contracts. D12 does not expand any released vector or infer a new parameter codec.

### REQ-BDW-AM-U-LIFECYCLE — Required workflow lifecycle and error outcomes

**U/target-U.** Automation/mapping ownership, persistence and migration, malformed/out-of-domain edits or files, undo grouping, cancellation, transport/rate/engine changes, source loss, running tails and teardown remain required unknowns. Public controls and stored fields supply no transaction, recovery or host architecture.

## Cabinet

### REQ-BDW-CA-001 — Speaker and microphone controls

**D12/target-U.** Speaker selects cabinet configuration, Microphone its virtual placement, and the separate mic-type switch the microphone kind. Exact label/index mapping remains in the corrected bundled-parameter owner; tonal adjectives supply no response metric.

Evidence: [cabinet:B003](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-cabinet-blocks.json), [cabinet:B004](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-cabinet-blocks.json), [cabinet:B005](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-cabinet-blocks.json).

### REQ-BDW-CA-002 — Output selector and host mix boundary

**D12/target-U.** Output selects mono or Dual processing; Dry/Wet is a mix control whose finite conditional host composition is owned elsewhere. No new channel formula, wet signal, CPU multiplier or host architecture is inferred.

Evidence: [cabinet:B006](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-cabinet-blocks.json), [cabinet:B007](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-cabinet-blocks.json).

### REQ-BDW-CA-003 — Multiple-microphone rack workflow

**D12/target-U.** The documented multiple-mic workflow duplicates Cabinet-containing rack chains, changes microphone placement/type per chain and balances chain volumes. Rack duplication/mixing remains with SPEC-DEVICE-RACKS and does not imply a new Cabinet signal law.

Evidence: [cabinet:B013](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-cabinet-blocks.json), [cabinet:B014](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-cabinet-blocks.json), [cabinet:B015](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-cabinet-blocks.json), [cabinet:B016](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-cabinet-blocks.json), [cabinet:B017](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-cabinet-blocks.json), [cabinet:B018](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-cabinet-blocks.json).

### REQ-BDW-CA-U-SIGNAL — Unresolved broader signal and expression results

**U/target-U.** Exact broader output, MPE/controller/tuning response, modulation/voice/loop/glide phase and transitions, numerical domains, timing and random laws remain unknown outside the explicitly linked finite contracts. D12 does not expand any released vector or infer a new parameter codec.

### REQ-BDW-CA-U-LIFECYCLE — Required workflow lifecycle and error outcomes

**U/target-U.** Automation/mapping ownership, persistence and migration, malformed/out-of-domain edits or files, undo grouping, cancellation, transport/rate/engine changes, source loss, running tails and teardown remain required unknowns. Public controls and stored fields supply no transaction, recovery or host architecture.

## Case catalog and coverage limits

The [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/cases.json) owns full actions and oracles; the
[requirement index](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/requirements.json) is derived from the clauses above.
Every profile retains finite positive, negative, boundary, automation,
persistence, undo, malformed, cancel, transport, rate, teardown and expression/
tuning probes. A compound documentary clause still needs branch-specific
expansion before complete coverage. All target and unsupported oracles stay null.

| Device | D12 / U requirements | Cases |
| --- | --- | --- |
| Analog | 10 / 2 | 21 |
| Collision | 6 / 2 | 17 |
| Corpus | 7 / 2 | 18 |
| Electric | 2 / 2 | 13 |
| Tension | 9 / 2 | 20 |
| Amp | 4 / 2 | 15 |
| Cabinet | 3 / 2 | 14 |

Total: **55 requirements (41 D12, 14 U), 118 unexecuted cases; 33 visible documentary control/state proposals and 85 null documentary oracles.** No target is graded.

| Case | Requirement | Kind | Documentary oracle |
| --- | --- | --- | --- |
| BDW-AN-001 | REQ-BDW-AN-001 | documented-state | visible controls/state only |
| BDW-AN-002 | REQ-BDW-AN-002 | documented-control | visible controls/state only |
| BDW-AN-003 | REQ-BDW-AN-003 | documented-state | visible controls/state only |
| BDW-AN-004 | REQ-BDW-AN-004 | documented-control | visible controls/state only |
| BDW-AN-005 | REQ-BDW-AN-005 | signal-obligation | U / null |
| BDW-AN-006 | REQ-BDW-AN-006 | documented-control | visible controls/state only |
| BDW-AN-007 | REQ-BDW-AN-007 | documented-control | visible controls/state only |
| BDW-AN-008 | REQ-BDW-AN-008 | documented-control | visible controls/state only |
| BDW-AN-009 | REQ-BDW-AN-009 | signal-obligation | U / null |
| BDW-AN-010 | REQ-BDW-AN-010 | documented-control | visible controls/state only |
| BDW-CL-001 | REQ-BDW-CL-001 | documented-control | visible controls/state only |
| BDW-CL-002 | REQ-BDW-CL-002 | documented-control | visible controls/state only |
| BDW-CL-003 | REQ-BDW-CL-003 | documented-state | visible controls/state only |
| BDW-CL-004 | REQ-BDW-CL-004 | documented-control | visible controls/state only |
| BDW-CL-005 | REQ-BDW-CL-005 | documented-control | visible controls/state only |
| BDW-CL-006 | REQ-BDW-CL-006 | signal-obligation | U / null |
| BDW-CO-001 | REQ-BDW-CO-001 | documented-control | visible controls/state only |
| BDW-CO-002 | REQ-BDW-CO-002 | documented-control | visible controls/state only |
| BDW-CO-003 | REQ-BDW-CO-003 | documented-control | visible controls/state only |
| BDW-CO-004 | REQ-BDW-CO-004 | signal-obligation | U / null |
| BDW-CO-005 | REQ-BDW-CO-005 | documented-control | visible controls/state only |
| BDW-CO-006 | REQ-BDW-CO-006 | signal-obligation | U / null |
| BDW-CO-007 | REQ-BDW-CO-007 | signal-obligation | U / null |
| BDW-EL-001 | REQ-BDW-EL-001 | documented-state | visible controls/state only |
| BDW-EL-002 | REQ-BDW-EL-002 | documented-control | visible controls/state only |
| BDW-TE-001 | REQ-BDW-TE-001 | documented-state | visible controls/state only |
| BDW-TE-002 | REQ-BDW-TE-002 | documented-control | visible controls/state only |
| BDW-TE-003 | REQ-BDW-TE-003 | documented-control | visible controls/state only |
| BDW-TE-004 | REQ-BDW-TE-004 | documented-control | visible controls/state only |
| BDW-TE-005 | REQ-BDW-TE-005 | documented-control | visible controls/state only |
| BDW-TE-006 | REQ-BDW-TE-006 | documented-control | visible controls/state only |
| BDW-TE-007 | REQ-BDW-TE-007 | documented-control | visible controls/state only |
| BDW-TE-008 | REQ-BDW-TE-008 | signal-obligation | U / null |
| BDW-TE-009 | REQ-BDW-TE-009 | documented-control | visible controls/state only |
| BDW-AM-001 | REQ-BDW-AM-001 | documented-control | visible controls/state only |
| BDW-AM-002 | REQ-BDW-AM-002 | signal-obligation | U / null |
| BDW-AM-003 | REQ-BDW-AM-003 | documented-control | visible controls/state only |
| BDW-AM-004 | REQ-BDW-AM-004 | documented-state | visible controls/state only |
| BDW-CA-001 | REQ-BDW-CA-001 | documented-control | visible controls/state only |
| BDW-CA-002 | REQ-BDW-CA-002 | documented-control | visible controls/state only |
| BDW-CA-003 | REQ-BDW-CA-003 | documented-state | visible controls/state only |
| BDW-AN-U-NEGATIVE | REQ-BDW-AN-U-SIGNAL | negative | U / null |
| BDW-AN-U-BOUNDARY | REQ-BDW-AN-U-SIGNAL | boundary | U / null |
| BDW-AN-U-AUTOMATION | REQ-BDW-AN-U-LIFECYCLE | automation | U / null |
| BDW-AN-U-PERSISTENCE | REQ-BDW-AN-U-LIFECYCLE | persistence | U / null |
| BDW-AN-U-UNDO | REQ-BDW-AN-U-LIFECYCLE | undo | U / null |
| BDW-AN-U-MALFORMED | REQ-BDW-AN-U-LIFECYCLE | malformed | U / null |
| BDW-AN-U-CANCEL | REQ-BDW-AN-U-LIFECYCLE | cancel | U / null |
| BDW-AN-U-TRANSPORT | REQ-BDW-AN-U-LIFECYCLE | transport | U / null |
| BDW-AN-U-RATE | REQ-BDW-AN-U-LIFECYCLE | sample-rate | U / null |
| BDW-AN-U-TEARDOWN | REQ-BDW-AN-U-LIFECYCLE | teardown | U / null |
| BDW-AN-U-MPE-TUNING | REQ-BDW-AN-U-SIGNAL | mpe-tuning | U / null |
| BDW-CL-U-NEGATIVE | REQ-BDW-CL-U-SIGNAL | negative | U / null |
| BDW-CL-U-BOUNDARY | REQ-BDW-CL-U-SIGNAL | boundary | U / null |
| BDW-CL-U-AUTOMATION | REQ-BDW-CL-U-LIFECYCLE | automation | U / null |
| BDW-CL-U-PERSISTENCE | REQ-BDW-CL-U-LIFECYCLE | persistence | U / null |
| BDW-CL-U-UNDO | REQ-BDW-CL-U-LIFECYCLE | undo | U / null |
| BDW-CL-U-MALFORMED | REQ-BDW-CL-U-LIFECYCLE | malformed | U / null |
| BDW-CL-U-CANCEL | REQ-BDW-CL-U-LIFECYCLE | cancel | U / null |
| BDW-CL-U-TRANSPORT | REQ-BDW-CL-U-LIFECYCLE | transport | U / null |
| BDW-CL-U-RATE | REQ-BDW-CL-U-LIFECYCLE | sample-rate | U / null |
| BDW-CL-U-TEARDOWN | REQ-BDW-CL-U-LIFECYCLE | teardown | U / null |
| BDW-CL-U-MPE-TUNING | REQ-BDW-CL-U-SIGNAL | mpe-tuning | U / null |
| BDW-CO-U-NEGATIVE | REQ-BDW-CO-U-SIGNAL | negative | U / null |
| BDW-CO-U-BOUNDARY | REQ-BDW-CO-U-SIGNAL | boundary | U / null |
| BDW-CO-U-AUTOMATION | REQ-BDW-CO-U-LIFECYCLE | automation | U / null |
| BDW-CO-U-PERSISTENCE | REQ-BDW-CO-U-LIFECYCLE | persistence | U / null |
| BDW-CO-U-UNDO | REQ-BDW-CO-U-LIFECYCLE | undo | U / null |
| BDW-CO-U-MALFORMED | REQ-BDW-CO-U-LIFECYCLE | malformed | U / null |
| BDW-CO-U-CANCEL | REQ-BDW-CO-U-LIFECYCLE | cancel | U / null |
| BDW-CO-U-TRANSPORT | REQ-BDW-CO-U-LIFECYCLE | transport | U / null |
| BDW-CO-U-RATE | REQ-BDW-CO-U-LIFECYCLE | sample-rate | U / null |
| BDW-CO-U-TEARDOWN | REQ-BDW-CO-U-LIFECYCLE | teardown | U / null |
| BDW-CO-U-MPE-TUNING | REQ-BDW-CO-U-SIGNAL | mpe-tuning | U / null |
| BDW-EL-U-NEGATIVE | REQ-BDW-EL-U-SIGNAL | negative | U / null |
| BDW-EL-U-BOUNDARY | REQ-BDW-EL-U-SIGNAL | boundary | U / null |
| BDW-EL-U-AUTOMATION | REQ-BDW-EL-U-LIFECYCLE | automation | U / null |
| BDW-EL-U-PERSISTENCE | REQ-BDW-EL-U-LIFECYCLE | persistence | U / null |
| BDW-EL-U-UNDO | REQ-BDW-EL-U-LIFECYCLE | undo | U / null |
| BDW-EL-U-MALFORMED | REQ-BDW-EL-U-LIFECYCLE | malformed | U / null |
| BDW-EL-U-CANCEL | REQ-BDW-EL-U-LIFECYCLE | cancel | U / null |
| BDW-EL-U-TRANSPORT | REQ-BDW-EL-U-LIFECYCLE | transport | U / null |
| BDW-EL-U-RATE | REQ-BDW-EL-U-LIFECYCLE | sample-rate | U / null |
| BDW-EL-U-TEARDOWN | REQ-BDW-EL-U-LIFECYCLE | teardown | U / null |
| BDW-EL-U-MPE-TUNING | REQ-BDW-EL-U-SIGNAL | mpe-tuning | U / null |
| BDW-TE-U-NEGATIVE | REQ-BDW-TE-U-SIGNAL | negative | U / null |
| BDW-TE-U-BOUNDARY | REQ-BDW-TE-U-SIGNAL | boundary | U / null |
| BDW-TE-U-AUTOMATION | REQ-BDW-TE-U-LIFECYCLE | automation | U / null |
| BDW-TE-U-PERSISTENCE | REQ-BDW-TE-U-LIFECYCLE | persistence | U / null |
| BDW-TE-U-UNDO | REQ-BDW-TE-U-LIFECYCLE | undo | U / null |
| BDW-TE-U-MALFORMED | REQ-BDW-TE-U-LIFECYCLE | malformed | U / null |
| BDW-TE-U-CANCEL | REQ-BDW-TE-U-LIFECYCLE | cancel | U / null |
| BDW-TE-U-TRANSPORT | REQ-BDW-TE-U-LIFECYCLE | transport | U / null |
| BDW-TE-U-RATE | REQ-BDW-TE-U-LIFECYCLE | sample-rate | U / null |
| BDW-TE-U-TEARDOWN | REQ-BDW-TE-U-LIFECYCLE | teardown | U / null |
| BDW-TE-U-MPE-TUNING | REQ-BDW-TE-U-SIGNAL | mpe-tuning | U / null |
| BDW-AM-U-NEGATIVE | REQ-BDW-AM-U-SIGNAL | negative | U / null |
| BDW-AM-U-BOUNDARY | REQ-BDW-AM-U-SIGNAL | boundary | U / null |
| BDW-AM-U-AUTOMATION | REQ-BDW-AM-U-LIFECYCLE | automation | U / null |
| BDW-AM-U-PERSISTENCE | REQ-BDW-AM-U-LIFECYCLE | persistence | U / null |
| BDW-AM-U-UNDO | REQ-BDW-AM-U-LIFECYCLE | undo | U / null |
| BDW-AM-U-MALFORMED | REQ-BDW-AM-U-LIFECYCLE | malformed | U / null |
| BDW-AM-U-CANCEL | REQ-BDW-AM-U-LIFECYCLE | cancel | U / null |
| BDW-AM-U-TRANSPORT | REQ-BDW-AM-U-LIFECYCLE | transport | U / null |
| BDW-AM-U-RATE | REQ-BDW-AM-U-LIFECYCLE | sample-rate | U / null |
| BDW-AM-U-TEARDOWN | REQ-BDW-AM-U-LIFECYCLE | teardown | U / null |
| BDW-AM-U-MPE-TUNING | REQ-BDW-AM-U-SIGNAL | mpe-tuning | U / null |
| BDW-CA-U-NEGATIVE | REQ-BDW-CA-U-SIGNAL | negative | U / null |
| BDW-CA-U-BOUNDARY | REQ-BDW-CA-U-SIGNAL | boundary | U / null |
| BDW-CA-U-AUTOMATION | REQ-BDW-CA-U-LIFECYCLE | automation | U / null |
| BDW-CA-U-PERSISTENCE | REQ-BDW-CA-U-LIFECYCLE | persistence | U / null |
| BDW-CA-U-UNDO | REQ-BDW-CA-U-LIFECYCLE | undo | U / null |
| BDW-CA-U-MALFORMED | REQ-BDW-CA-U-LIFECYCLE | malformed | U / null |
| BDW-CA-U-CANCEL | REQ-BDW-CA-U-LIFECYCLE | cancel | U / null |
| BDW-CA-U-TRANSPORT | REQ-BDW-CA-U-LIFECYCLE | transport | U / null |
| BDW-CA-U-RATE | REQ-BDW-CA-U-LIFECYCLE | sample-rate | U / null |
| BDW-CA-U-TEARDOWN | REQ-BDW-CA-U-LIFECYCLE | teardown | U / null |
| BDW-CA-U-MPE-TUNING | REQ-BDW-CA-U-SIGNAL | mpe-tuning | U / null |

## State, errors and timing

Default loading, exposed-to-stored domains, MIDI/MPE codecs, tuning composition,
parameter ownership, automation/clock/rate transitions, first/last-note handling,
copy/route transaction boundaries, tail/random-state persistence, malformed UI
or presets, cancellation, undo and teardown remain required unknowns beyond
existing owners’ exact scopes. This page supplies no clamp/reject/repair policy,
zero-latency deadline, voice budget, output continuity or CPU threshold.

Source physical-model descriptions and arithmetic-like adjectives are not new
DSP formulas. Numeric domains and mode indices must use the existing parameter
owner, not the manual’s visual labels. Earlier finite X clauses are not weakened,
relabelled or extended. Manual/extracted-context differences retain both sources
and stay unresolved; the research page records the relevant cautions.

## Analyst-only evidence and freeze

The [source ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/sources.json)
reuses the official instrument/effect chapters and their original capture
identities. The [author manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manifest-author-r1.json)
pins source extracts, catalogs, fixtures, existing-authority pins, canonical
snapshots and [validation](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/validation-author-r1.json).
All normative requirement IDs are proper headings and must be discovered as
exactly the catalog set by the existing requirements browser. This author
freeze awaits independent analyst review; it is not a release or compatibility
result. Shared catalog/log integration belongs to root.
