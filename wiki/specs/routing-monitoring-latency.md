---
id: SPEC-ROUTING-MONITORING-LATENCY
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 2
target: Ableton Live 12 Suite 12.4.3; Version 12 documentary behavior with target applicability unknown
---

# Track routing, monitoring and latency controls

## Scope and authority

This partial FEAT-AUDIO/F-09 analyst draft owns general track audio/MIDI routing,
source taps, submix/group/return/Main/cue route selection, monitor-control context
and latency-option policy. [Coverage design](../research/full-live-specification-design.md)
governs closure; [research](../research/routing-monitoring-latency.md) owns source
interpretation. No original program/function, hardware or candidate was executed.
It is not a complete engine contract, handoff or compatibility report.

**D12** means a claim in the retained official Version 12 manual. All runtime
clauses have exact-12.4.3 applicability **U**. Every case has target `expected`
and `comparison` null, grade U and `executed:false`. Visible documentary control
or state predicates are proposals only. Signal, latency, hardware, lifecycle
and unprovided fixture outcomes have null documentary oracles too. Source
adjectives, UI meters, port names, a compensation switch and reported delay
values cannot establish calibrated delivered audio/MIDI or real-time capacity.


Revision 2 preserves all 40 historical requirement records and all 69 prior case
IDs/fields except RML-009's explicit right-click action refinement. It adds only
REQ-RML-036/RML-070 for the named blue Monitor In Activator indicator with I/O
hidden. **AS-OF AUTHOR FREEZE:** independent R2 review is pending. Current review
and adoption disposition belongs to the [spec index](index.md), rather than this
historical author-freeze status. No whole-owner semantic renewal is claimed.

## Existing canonical owners

- [Recording/comping](recording-comping.md), especially REQ001/002, owns ordinary
  arming and Off/Auto/In gating, including selected-track Monitor dispatch.
  Those laws are linked here rather than copied. Recording file format,
  transitions, takes and media remain there. A reset default is a distinct
  context from initial armed monitoring or a saved/custom track default.
- [Mix graph](mix-graph.md) and [mixer values](mixer-values.md) retain their finite
  coefficients, send stages, ramps and bounded summing/mute/solo contracts.
  Their existing scope excludes general monitoring, groups, cue, track delay,
  latency-reporting devices and physical-device output. Their exclusions are
  still required product behavior, not grounds to narrow this packet’s target.
- [Playback](playback-core.md), [transport](transport-state.md),
  [clip launch](clip-launch.md) and [automation](automation-envelopes.md) retain
  finite clocks, event/clip scheduling and envelope laws. No new compensation
  arithmetic, block scheduler or graph architecture is introduced here.
- [External hardware devices](external-hardware-devices.md) owns External
  Instrument/External Audio Effect selectors, return/gain and Hardware Latency.
  General Track Delay and global compensation are different controls.
  [Plug-in hosting](plugin-hosting.md), [bundled hosting](bundled-device-hosting.md),
  [racks](device-racks.md) and [Impulse](device-impulse.md) own their specific
  ports/chains/processing; arbitrary multi-output plug-ins are not proven.
- [Export](audio-video-export.md) owns render scope and real-time/offline
  decisions; [media](media-file-workflows.md), [browser](browser-workflows.md),
  [MIDI mapping](midi-user-mapping.md) and [Set structure](live-set-structure.md)
  retain their existing operations. Computer-keyboard notes, sync/resync
  protocols and control surfaces are discovery context, not specified here.

## Inputs, positive controls and unresolved outputs

Use the [fixtures](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/fixtures-r2.json):
owned distinguishable audio/MIDI sources, explicitly selected active paths and
accepted controls in disposable Sets. Actual input bytes, qualifying instruments,
effects, auxiliary outputs, sidechains, driver/interface ports and measured
latencies are unproven prerequisites. No test file, fake host, hardware loopback
or numerical response was created. Never infer a routed result from a meter
alone, a silent source, zero send, muted return, inactive instrument, dry-only
path, absent cue output or unsupported plug-in.

Before an exclusion/no-effect test independently retain nonzero source and
return/output, relevant processing, accepted nonzero gain/send/wet contribution
and matched positive control. Reset unrelated routes, mapping, automation,
solo/mute, note history and active clips. Independent Main/Cue and source/effect/
receiver paths must be identifiable. A failed gate remains inconclusive.
Fixtures’ 440/997 Hz, beat/note choices, rates and block sizes are analyst
setups, not device limits, product defaults or tolerance definitions.

## Requirements

### REQ-RML-001 — I/O visibility

**D12/target-U.** Track I/O controls can be shown or hidden in Session and Arrangement using the mixer View controls or the documented platform shortcut.

Evidence: [routing:B002](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json), [routing:B003](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json).

### REQ-RML-002 — Input and output types

**D12/target-U.** Audio From and MIDI From select their respective track input types. Tracks output audio except MIDI tracks without an instrument, which output MIDI; return inputs come from sends.

Evidence: [routing:B004](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json), [routing:B005](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json), [routing:B007](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json).

### REQ-RML-003 — Type and channel hierarchy

**D12/target-U.** The upper routing chooser selects a source/destination category; the lower chooser supplies its available channel or sub-selection.

Evidence: [routing:B008](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json).

### REQ-RML-004 — Selected-track routing edits

**D12/target-U.** External audio input/output chooser changes and MIDI input chooser changes apply to the selected tracks described by the chapter.

Evidence: [routing:B019](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json), [routing:B026](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json).

### REQ-RML-005 — Monitoring path and existing gating owner

**D12/target-U.** Monitoring passes selected input through the track device chain to its output. Off/Auto/In gating, arm interaction and selected-track Monitor dispatch are owned by REQ-RECORDING-COMPING-002; ordinary arming belongs to REQ-RECORDING-COMPING-001. No competing monitor-default rule is introduced here.

Owners: [recording-comping.md](recording-comping.md#req-recording-comping-001--input-and-arm-selection), [recording-comping.md](recording-comping.md#req-recording-comping-002--input-monitoring).

Evidence: [routing:B010](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json), [routing:B011](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json), [routing:B012](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json), [routing:B013](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json), [routing:B014](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json), [routing:B016](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json).

### REQ-RML-006 — Monitor reset context

**D12/target-U.** With I/O expanded, the documented Monitor reset command restores Off for audio and Auto for MIDI. This is a reset-context statement, not a universal new-track/custom-default/armed-track default.

Evidence: [routing:B017](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json).

### REQ-RML-007 — Recorded monitoring-latency option

**D12/target-U.** In/Auto monitoring documents an enabled-by-default option to keep monitoring latency in recorded material, with manual switching through those Monitor controls. This establishes an option and context, not a timestamp correction formula or global constructor default.

Evidence: [routing:B015](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json).

### REQ-RML-008 — External audio availability and configuration

**D12/target-U.** Ext. In selects interface input channels; Audio Settings and channel configuration determine available mono/stereo inputs/outputs. Configure opens that settings route.

Evidence: [routing:B019](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json), [routing:B020](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json).

### REQ-RML-009 — Device-associated channel names

**D12/target-U.** Renaming configured audio channels changes their chooser names; names are associated with the audio device. Tab advances between names in the configuration dialog.

Evidence: [routing:B021](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json).

### REQ-RML-010 — Input activity and overload role

**D12/target-U.** External audio input entries expose activity/overload meters; MIDI input channel entries expose activity meters. Their calibration, red threshold, detector/window, hold and refresh timing are not established here.

Evidence: [routing:B019](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json), [routing:B026](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json).

### REQ-RML-011 — External MIDI port and channel selection

**D12/target-U.** MIDI From can select one external port or All Ins, and one channel or All Channels; the All choices describe merged inputs. No merge ordering or duplicate-event policy is supplied.

Evidence: [routing:B026](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json).

### REQ-RML-012 — MIDI port role switches

**D12/target-U.** The MIDI settings distinguish Track for note/CC traffic, Sync for clock/timecode use and Remote for controller mapping/feedback. These roles do not establish sync protocol, arbitrary hardware support or mapping takeover behavior.

Owners: [midi-user-mapping.md](midi-user-mapping.md).

Evidence: [routing:B028](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json), [routing:B030](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json), [routing:B031](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json), [routing:B032](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json), [routing:B035](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json), [routing:B045](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json), [routing:B046](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json), [routing:B047](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json).

### REQ-RML-013 — External MIDI destination

**D12/target-U.** A MIDI-output track selects a destination port and output channel through its To chooser pair. External Instrument is an alternative device-owned round-trip route, not the same controls.

Owners: [external-hardware-devices.md](external-hardware-devices.md).

Evidence: [routing:B056](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json), [routing:B057](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json).

### REQ-RML-014 — MIDI indicator classification

**D12/target-U.** Control-Bar MIDI indicators distinguish sync, remote and track traffic and incoming/outgoing direction. Sync indicators have an external-sync-source visibility condition; mapped remote messages are described as consumed before MIDI tracks.

Evidence: [routing:B060](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json), [routing:B061](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json), [routing:B062](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json), [routing:B063](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json), [routing:B064](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json), [routing:B065](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json).

### REQ-RML-015 — Output-to-track and many-to-one routing

**D12/target-U.** A track may choose another compatible receiver as output without changing that receiver’s own I/O settings; multiple senders can address that receiver. Source/destination signal types must be compatible.

Evidence: [routing:B071](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json), [routing:B072](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json), [routing:B074](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json).

### REQ-RML-016 — Input-from-track and one-to-many routing

**D12/target-U.** Selecting a compatible source as another track’s input taps it without otherwise changing the source’s routing; more receivers can tap that source.

Evidence: [routing:B073](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json), [routing:B075](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json).

### REQ-RML-017 — Audio source tap selections

**D12/target-U.** Audio From another track offers Pre FX, Post FX and Post Mixer: before devices, after devices/before mixer and after mixer respectively. Finite device/mixer calculations remain with their owners.

Owners: [mix-graph.md](mix-graph.md), [mixer-values.md](mixer-values.md).

Evidence: [routing:B077](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json), [routing:B078](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json), [routing:B079](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json), [routing:B080](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json), [routing:B081](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json).

### REQ-RML-018 — Solo interaction for tapped tracks

**D12/target-U.** The chapter distinguishes hearing a source when its receiving track is soloed at Pre FX/Post FX versus Post Mixer, and separately describes solo behavior for output-to-track many-to-one routing. No universal solo law for arbitrary graphs is inferred.

Owners: [mix-graph.md](mix-graph.md).

Evidence: [routing:B074](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json), [routing:B079](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json), [routing:B080](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json), [routing:B081](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json).

### REQ-RML-019 — Rack-chain tap exposure

**D12/target-U.** Routing choices can expose Instrument/Effect Rack chain Pre FX/Post FX/Post Mixer and Drum Rack return-chain points, with documented chain-point solo behavior. Rack chain processing and drum return ownership remain with SPEC-DEVICE-RACKS.

Owners: [device-racks.md](device-racks.md).

Evidence: [routing:B083](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json), [routing:B084](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json), [routing:B085](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json), [routing:B086](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json), [routing:B087](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json).

### REQ-RML-020 — MIDI source tap before instrument

**D12/target-U.** When one MIDI track takes MIDI from another, the chapter describes tapping after MIDI effects and before the source instrument, permitting layered receivers even when the source track ultimately outputs audio.

Evidence: [routing:B124](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json), [routing:B125](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json).

### REQ-RML-021 — Track In versus direct instrument destination

**D12/target-U.** A MIDI sender targeting an instrument-hosting track can address Track In or the offered instrument directly. Direct instrument targeting bypasses the receiving track’s recording/monitoring stage in the chapter’s example.

Evidence: [routing:B102](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json), [routing:B103](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json).

### REQ-RML-022 — No Input instrument-container context

**D12/target-U.** In the documented instrument-container setup, selecting MIDI No Input hides its Arm control; it does not make its routed instrument output immune to the host track’s Activator.

Evidence: [routing:B104](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json).

### REQ-RML-023 — Qualified auxiliary and sidechain choices

**D12/target-U.** Multi-output instruments and sidechain-capable devices may expose named routing destinations/sources. Availability is device-specific: Impulse’s automatic removal of a tapped slot from its own mix must not be generalized to arbitrary plug-ins.

Owners: [device-impulse.md](device-impulse.md), [plugin-hosting.md](plugin-hosting.md), [external-hardware-devices.md](external-hardware-devices.md).

Evidence: [routing:B106](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json), [routing:B107](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json), [routing:B109](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json), [routing:B110](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json), [routing:B120](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json), [routing:B121](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json), [routing:B122](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json).

### REQ-RML-024 — Post-effects recording topology

**D12/target-U.** The chapter uses a monitored processing track and separate recording receivers taking Post FX, or Post Mixer when its level/pan is wanted. Recording transitions/media semantics belong to SPEC-RECORDING-COMPING.

Owners: [recording-comping.md](recording-comping.md).

Evidence: [routing:B091](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json), [routing:B092](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json), [routing:B093](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json), [routing:B095](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json), [routing:B096](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json).

### REQ-RML-025 — Submix and Sends Only choices

**D12/target-U.** Multiple track outputs can feed a submix track that outputs to Main. Sends Only with a nonzero selected send uses its corresponding return as submixer; this describes routing roles, not a send-gain law.

Owners: [mix-graph.md](mix-graph.md), [mixer-values.md](mixer-values.md).

Evidence: [routing:B098](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json), [routing:B100](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json).

### REQ-RML-026 — Grouping preserves custom output exception

**D12/target-U.** Grouping retargets Main-routed children to the group; existing custom destinations are retained.

Evidence: [routing:B099](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json), [mixing:B039](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-mixing-blocks.json).

### REQ-RML-027 — Return and Main roles

**D12/target-U.** Returns combine sent audio; Main is the usual final destination. Neither plays clips.

Evidence: [routing:B005](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json), [mixing:B048](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-mixing-blocks.json), [mixing:B051](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-mixing-blocks.json), [mixing:B055](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-mixing-blocks.json).

### REQ-RML-028 — Per-return send tap controls

**D12/target-U.** Pre/Post is per return; the finite send-stage law remains in SPEC-MIX-GRAPH.

Owners: [mix-graph.md](mix-graph.md).

Evidence: [mixing:B054](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-mixing-blocks.json).

### REQ-RML-029 — Cue output and mode controls

**D12/target-U.** Cue requires distinct Main/Cue destinations on a qualifying multi-output interface; Cue mode replaces Solo controls and offers Cue Volume.

Evidence: [mixing:B074](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-mixing-blocks.json), [mixing:B075](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-mixing-blocks.json), [mixing:B076](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-mixing-blocks.json), [mixing:B077](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-mixing-blocks.json), [mixing:B078](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-mixing-blocks.json), [mixing:B079](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-mixing-blocks.json).

### REQ-RML-030 — Cue versus Main admission

**D12/target-U.** Cue routes the selected track to Cue Out while its Activator still controls Main admission; browser preview also uses configured cue output.

Owners: [browser-workflows.md](browser-workflows.md).

Evidence: [mixing:B078](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-mixing-blocks.json), [mixing:B080](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-mixing-blocks.json).

### REQ-RML-031 — Main resampling route

**D12/target-U.** An audio track’s Resampling input takes Main. During resampling its own output is suppressed from the recording; recording and media storage outcomes retain their existing owners.

Owners: [recording-comping.md](recording-comping.md), [media-file-workflows.md](media-file-workflows.md).

Evidence: [routing:B067](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json), [routing:B068](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json), [routing:B069](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json).

### REQ-RML-032 — Delay Compensation switch and scope

**D12/target-U.** Options exposes Delay Compensation, documented on by default for built-in devices and plug-ins including returns. The synchronization goal supplies no measured alignment, device-reporting contract or scheduling algorithm.

Evidence: [compensation:B002](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-compensation-blocks.json), [compensation:B003](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-compensation-blocks.json).

### REQ-RML-033 — Reduced Latency When Monitoring policy

**D12/target-U.** Reduced Latency When Monitoring is available with Delay Compensation on and changes compensation for input-monitored tracks while other compensated paths can remain different. Lowest-latency/in-sync language is an uncalibrated goal, not a zero-latency or alignment oracle.

Evidence: [compensation:B004](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-compensation-blocks.json).

### REQ-RML-034 — Track Delay control distinction

**D12/target-U.** Track Delay offers sample/ms units and is unavailable with Delay Compensation off. It is distinct from automatic compensation and device-owned Hardware Latency controls.

Owners: [external-hardware-devices.md](external-hardware-devices.md).

Evidence: [compensation:B006](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-compensation-blocks.json), [mixing:B082](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-mixing-blocks.json), [mixing:B083](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-mixing-blocks.json), [mixing:B084](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-mixing-blocks.json), [mixing:B085](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-mixing-blocks.json), [mixing:B087](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-mixing-blocks.json).

### REQ-RML-035 — Track-meter context

**D12/target-U.** Track meters describe peak/RMS output, or input while monitoring; no detector calibration follows.

Evidence: [mixing:B009](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-mixing-blocks.json).

### REQ-RML-U-SIGNAL — General routed-signal outcomes

**U/target-U.** Exact audio/MIDI routing matrices, mono/stereo conversion coefficients, tap/solo/mute leakage, sums, duplicate delivery, sidechain admission, return feedback and onset/tail identity remain unknown outside linked finite owners. No all-graph equivalence is inferred.

Evidence: [routing:B023](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json), [routing:B024](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json).

### REQ-RML-U-LATENCY — Latency, clocks and real-time calibration

**U/target-U.** No latency arithmetic, graph maximum/difference calculation, driver/buffer/device-reporting law, clock phase/jitter, compensation accuracy, zero-latency deadline, CPU bound or calibration tolerance is established. Tempo-synced effects after delay and large-delay sluggishness are documented caveats only.

Evidence: [compensation:B002](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-compensation-blocks.json), [compensation:B004](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-compensation-blocks.json), [compensation:B005](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-compensation-blocks.json), [compensation:B006](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-compensation-blocks.json), [compensation:B007](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-compensation-blocks.json).

### REQ-RML-U-STATE — Routing persistence and identity

**U/target-U.** Saved port/source/channel/monitor/cue/group identities, renaming/reordering/missing-source repair, user/custom defaults, preference loading and old-version migration remain unknown. General document readers do not establish these routing transitions.

### REQ-RML-U-LIFECYCLE — Routing transactions and teardown

**U/target-U.** Automation/mapping eligibility and ownership, undo grouping, cancellation commit points, source loss/reconnection, malformed fields, graph-cycle handling, simultaneous edits, engine/rate changes and device/track/Set teardown remain required unknowns.

### REQ-RML-U-HARDWARE — Hardware and driver prerequisites

**U/target-U.** Actual port/driver/interface/hardware availability, supported channel counts/rates, delivery feedback, permission/refusal behavior, hotplug identity and independent source/return calibration are unknown on this analyst host. Hardware absence does not remove the required scope.

### REQ-RML-036 — Monitor In Activator indicator

**D12/target-U.** With Monitor In selected, the source describes a blue track Activator indicator that remains recognizable when the In/Out section is hidden. This is a named categorical color/control role only, not an RGB value, theme/contrast guarantee, Off/Auto color law, disabled-Activator behavior, activation/audio gate or transition-time rule.

Owners: [recording-comping.md](recording-comping.md#req-recording-comping-002--input-monitoring).

Evidence: [routing:B013](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json), HTML314 in the original Routing capture, Version12/exact12.4.3 U. The [complete bounded source reconciliation](../../analysis/ableton-live-12.4.3/full-spec-v1/monitoring-source-reconciliation/README.md) preserves the exact raw selection and limitations.

## Finite case catalog

The retained [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/cases-r2.json) owns full setup/actions, documentary
expectations and comparison limits. The [requirement index](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/requirements-r2.json)
is derived from the canonical clauses above. This table is navigation only;
one compound clause does not establish exhaustive branch coverage.

**41 requirements (36 D12, 5 U), 70 cases: 34 documentary control/state proposals and 36 cases with null documentary oracles. All target outcomes are null/U/unexecuted.**

| Case | Requirement | Kind | Scenario | Documentary oracle |
| --- | --- | --- | --- | --- |
| RML-001 | REQ-RML-001 | control | Both-view visibility | visible control/state only |
| RML-002 | REQ-RML-002 | control | Typed choices | visible control/state only |
| RML-003 | REQ-RML-003 | control | Dependent channel choices | visible control/state only |
| RML-004 | REQ-RML-004 | state | Multiple selected audio tracks | visible control/state only |
| RML-005 | REQ-RML-004 | state | Multiple selected MIDI inputs | visible control/state only |
| RML-006 | REQ-RML-005 | signal | Monitor and clip discrimination | U / null |
| RML-007 | REQ-RML-005 | state | Monitor selection and recording independence | visible control/state only |
| RML-008 | REQ-RML-006 | boundary | Reset scope | visible control/state only |
| RML-009 | REQ-RML-007 | control | Keep-latency control | visible control/state only |
| RML-010 | REQ-RML-007 | signal | Recorded timing boundary | U / null |
| RML-011 | REQ-RML-008 | control | Enabled channel inventory | visible control/state only |
| RML-012 | REQ-RML-009 | state | Rename one configured channel | visible control/state only |
| RML-013 | REQ-RML-010 | control | Visible meter roles | visible control/state only |
| RML-014 | REQ-RML-011 | control | Port and channel choices | visible control/state only |
| RML-015 | REQ-RML-011 | signal | Merged and selected MIDI streams | U / null |
| RML-016 | REQ-RML-012 | control | Separate port roles | visible control/state only |
| RML-017 | REQ-RML-012 | signal | Track versus mapped message delivery | U / null |
| RML-018 | REQ-RML-013 | control | MIDI To port and channel | visible control/state only |
| RML-019 | REQ-RML-014 | control | Indicator directions and categories | visible control/state only |
| RML-020 | REQ-RML-014 | signal | Consumed remote messages | U / null |
| RML-021 | REQ-RML-015 | control | Compatible output target list | visible control/state only |
| RML-022 | REQ-RML-015 | signal | Many-to-one delivery | U / null |
| RML-023 | REQ-RML-016 | state | Compatible input target list | visible control/state only |
| RML-024 | REQ-RML-016 | signal | One-to-many delivery | U / null |
| RML-025 | REQ-RML-017 | control | Three audio tap choices | visible control/state only |
| RML-026 | REQ-RML-017 | signal | Device and mixer perturbations at taps | U / null |
| RML-027 | REQ-RML-018 | signal | Tap and receiver solo contexts | U / null |
| RML-028 | REQ-RML-019 | control | Named chain tap choices | visible control/state only |
| RML-029 | REQ-RML-019 | signal | Chain tap isolation | U / null |
| RML-030 | REQ-RML-020 | control | MIDI tap list | visible control/state only |
| RML-031 | REQ-RML-020 | signal | MIDI before source instrument | U / null |
| RML-032 | REQ-RML-021 | control | Track and instrument destination choices | visible control/state only |
| RML-033 | REQ-RML-021 | signal | Direct instrument with receiver monitoring variations | U / null |
| RML-034 | REQ-RML-022 | state | No Input Arm presentation | visible control/state only |
| RML-035 | REQ-RML-022 | signal | Container activation boundary | U / null |
| RML-036 | REQ-RML-023 | control | Qualified port availability | visible control/state only |
| RML-037 | REQ-RML-023 | signal | Auxiliary and sidechain contribution | U / null |
| RML-038 | REQ-RML-024 | control | Processing and recording receiver routes | visible control/state only |
| RML-039 | REQ-RML-024 | signal | Recorded tap contribution | U / null |
| RML-040 | REQ-RML-025 | control | Sends Only choice | visible control/state only |
| RML-041 | REQ-RML-025 | signal | Sends Only with active return | U / null |
| RML-042 | REQ-RML-026 | state | Main versus custom child routing | visible control/state only |
| RML-043 | REQ-RML-027 | control | Return and Main presentation | visible control/state only |
| RML-044 | REQ-RML-028 | control | Return tap option | visible control/state only |
| RML-045 | REQ-RML-028 | signal | Tap and separate monitor destination | U / null |
| RML-046 | REQ-RML-029 | control | Cue setup choices | visible control/state only |
| RML-047 | REQ-RML-030 | signal | Cue and Main discrimination | U / null |
| RML-048 | REQ-RML-031 | control | Resampling selector | visible control/state only |
| RML-049 | REQ-RML-031 | signal | Resampling self-contribution boundary | U / null |
| RML-050 | REQ-RML-032 | control | Compensation control | visible control/state only |
| RML-051 | REQ-RML-032 | signal | Compensation composition | U / null |
| RML-052 | REQ-RML-033 | control | Reduced-latency option eligibility | visible control/state only |
| RML-053 | REQ-RML-033 | signal | Input monitoring versus return latency | U / null |
| RML-054 | REQ-RML-034 | boundary | Track Delay units and availability | visible control/state only |
| RML-055 | REQ-RML-034 | signal | Track Delay and clock-dependent effects | U / null |
| RML-056 | REQ-RML-035 | signal | Input versus output meter context | U / null |
| RML-057 | REQ-RML-U-SIGNAL | signal | Unresolved mono/stereo matrix | U / null |
| RML-058 | REQ-RML-U-LATENCY | sample-rate | Rate, blocks and latency calibration | U / null |
| RML-059 | REQ-RML-U-LATENCY | transport | Transport and synchronized routes | U / null |
| RML-060 | REQ-RML-U-STATE | persistence | Save, reopen and missing route identity | U / null |
| RML-061 | REQ-RML-U-STATE | boundary | Monitor default contexts | U / null |
| RML-062 | REQ-RML-U-LIFECYCLE | automation | Routing automation and control ownership | U / null |
| RML-063 | REQ-RML-U-LIFECYCLE | undo | Undo and redo of route changes | U / null |
| RML-064 | REQ-RML-U-LIFECYCLE | malformed | Malformed route or numeric values | U / null |
| RML-065 | REQ-RML-U-LIFECYCLE | cancel | Routing chooser cancellation | U / null |
| RML-066 | REQ-RML-U-LIFECYCLE | source-loss | Source loss and reconnection | U / null |
| RML-067 | REQ-RML-U-LIFECYCLE | boundary | Feedback and cycle admission | U / null |
| RML-068 | REQ-RML-U-LIFECYCLE | teardown | Removal and engine teardown | U / null |
| RML-069 | REQ-RML-U-HARDWARE | recovery | Unavailable or refused configuration | U / null |

| RML-070 | REQ-RML-036 | control | Monitor In indicator with hidden I/O | visible control/state only |

[Finite R2 contexts](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/finite-contexts-r2.json)
keep In/Auto right-click and option off/on histories separate. RML-070 uses
separate audio/MIDI resets: independently verify actual Monitor In and a genuinely
visible blue In Activator indicator with I/O shown before hiding the same I/O;
observe that same track/control, restore I/O and independently verify actual In.
Missing indicator or failed visible positive baseline is U, never a passing
absence test. Color alone is not Monitor-state or audio-output proof. Theme,
other-mode/disabled-Activator color, transition timing and every signal outcome
remain unknown. Existing source/receiver positive path gates still apply.

RML-006 already retains the full arm/clip/mode matrix; RML-007 already exercises
selected Monitor dispatch; RML-008 already invokes both reset entries. No duplicate
cases or false missing-context claim is added. The original contracts/default
limits, Off-mode option availability unknowns and compensation/latency controls
remain unchanged. This increment does not adopt a new gate, initial state,
recording outcome, timing rule or stored-field/control-composition identity.

## Errors, timing and state boundaries

Source loss, malformed references/fields, simultaneous route changes, cycles,
cancel/undo/redo, persistence/migration, automation ownership, tempo/transport,
rate/driver refusal and teardown remain required unknowns. There is no assumed
last-note release, tail persistence, silence, rollback, clamp, repair, output
continuity, cleanup deadline, fixed latency or maximum CPU bound.

The monitor reset Off/audio and Auto/MIDI statement does not resolve the existing
recording owner’s contextual default question. Labels for the keep-monitoring-
latency option vary within the prose; no exact target caption is required.
“Lowest possible latency”, synchronization and interface-quality advice supply
no zero-latency, subtraction formula or calibration oracle. A tempo-synced effect
after a delay-causing device may need separate clock-context investigation.
Main, cue, return and monitor mixes are separate observed paths, not assumed
identical signals. General routing does not expand any published finite release.

## Analyst-only source appendix and freeze

The [source ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/sources.json)
pins original recording/racks capture identities plus the bounded mixing capture.
The routing chapter SHA-256 is
`1a9c9c842c7a2d04b59794ee12d959f7fad15e3b67f41622109ea14e06e4b9b9`;
compensation source chapter SHA-256 is
`6a783fde3de24178e1b1d4b8431ada1a1691a1c8f16a633f909bac347e72cd82`.
The [block extracts](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json)
retain HTML lines and heading context. Figures and linked help/FAQ/tutorials
were not separately inspected; their contents are not evidence here.

The historical [R1 author manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manifest-author-r1.json)
and all 19 original files remain byte-identical at their original paths. The
[R2 manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manifest-author-r2.json)
adds versioned catalogs/fixtures/current snapshots, [exact delta](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/delta-r2.json),
[immutable input pins](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/inputs-r2.json)
and [consumer impact](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/consumer-impact-r2.json).
The [approved source-only reconciliation review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/monitoring-source-reconciliation-review.json)
is evidence for the two proposals; it does not self-approve this owner successor.

The [current read-only validator](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/validate-r2.py)
checks this revision's immutable inputs, precise delta, source contexts,
prerequisites, snapshots and identifiers. It does not run the historical R1
validator against current pages, or execute vendor code, UI, hardware or network.
Old validators/reports remain as-of their revisions. Additive advancement alone
does not require historical adapters; any later concrete dependency or release
gate is a separately scoped root task. No frozen consumer or shared file is
edited here. **AS-OF AUTHOR FREEZE:** R2 awaits independent review; consult the
[spec index](index.md) for current disposition. A packet self-check is neither
semantic approval, release nor candidate compatibility. No topic is complete.
