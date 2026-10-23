---
id: SPEC-ENGINE-RESOURCE-WORKFLOWS
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3; current Version 12 documentary applicability unknown
---

# Engine resource controls and audio/MIDI comparison obligations

## Scope and evidence boundary

This partial F-09/FEAT-AUDIO/FEAT-MIDI analyst draft owns CPU/impact/overload
control roles and scoped MIDI monitoring/dropout source claims. It also records
ungraded fact-sheet comparison obligations, routed to existing operation owners.
[Research](../research/engine-resource-workflows.md) retains exact sources and
context questions; the [coverage design](../research/full-live-specification-design.md)
governs closure. It is not an engine architecture, numerical DSP or benchmark
specification, complete product family or released implementation input.

**D12** means a documented public observable role in the retained current
Version 12 manual. Every option, described default and behavior has exact
**12.4.3 applicability U**. **U** means no supported outcome/comparator is retained.
All target `expected`/`comparison` fields are null, grades U and cases unexecuted.
Signal/timing/file/numeric, cancellation and all other U cases also have null
documentary oracles. Their `source_claim` retains source context only. A source
claim or case count is not measured target behavior or closed compound coverage.

No original/native/extracted function, candidate, renderer, hardware/interface,
load stress, network or install was executed. Figures, private model/scheduling,
linked help and PDF bytes were not inspected. Source narratives about precision,
bit depth, resampling library, process/thread/core choices, per-sample updates and
MIDI scheduling are research context, never required candidate mechanisms.

## Existing owners and comparison routing

- [Playback](playback-core.md), [mix graph](mix-graph.md) and [mixer values](mixer-values.md)
  keep finite sample/event selection, graph/coefficient/ramp/unit laws and their
  assumptions. [Warp storage](warp-markers.md), [Warp workflows](warping-workflows.md),
  [groove](groove-workflows.md) and [automation](automation-workflows.md) retain
  their existing finite and ungraded output boundaries. No fact-sheet prose
  extends a released comparator, precision rule, timebase or neutrality result.
- [Export](audio-video-export.md), [recording](recording-comping.md),
  [routing/monitoring](routing-monitoring-latency.md), [settings](settings-learning-workflows.md)
  and [MIDI mapping](midi-user-mapping.md) retain command/format/port/monitor/arm,
  latency-option and control contracts. A buffer-dependent monitoring narrative
  is not a new clock/compensation formula or replacement for Monitor gates.
- [Arrangement](arrangement-editing.md), [Clip View](clip-view-workflows.md),
  [projects](project-media-workflows.md) and [media](media-file-workflows.md) retain
  split/fade/consolidate/region/file operations and their unknowns. Fact-sheet
  normalization/metadata/loop examples create questions, not second laws.
- [Bounce/Freeze](bounce-freeze-workflows.md) remains sealed and owns freeze files,
  loops, tails, editing and commit behavior. Additional audio-fact descriptions
  remain U here; its existing two-cycle role is referenced, not copied or changed.
  [Racks](device-racks.md), [bundled hosting](bundled-device-hosting.md),
  [plug-ins](plugin-hosting.md) and device-specific owners retain bypass/processing.

A neutral/non-neutral classification is conditional on source, operation and
surrounding processing. It does not justify bit identity from a header, blanket
acceptance of any format, a mandatory precision architecture or output inequality
for every input. Silence, zero amounts, already processed material and unmatched
source taps cannot establish the intended comparison. Publisher test results
are not this project's original-side captures or target tolerances.

## Future setup and observables

[Fixtures](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/fixtures.json)
are definitions only: no audio/MIDI/ALS/record/render/freeze result, actual accepted
interface/clock/load trace or calibrated baseline is supplied. Retain exact build,
platform, visible options/theme, source format/identity, actual accepted controls,
record/monitor/arm/transport, active automation/effect, output path and driver
configuration before every trial. Target defaults are never inferred from a fresh
unknown profile. Existing independently retained issue traces are prerequisites
for overload cases; this packet performs no stress or exhaustion investigation.

Before signal/no-effect/exclusion tests independently establish nonempty eligible
source/valid format, active processing, admitted nonzero amount/base/gain/send,
nonmuted wet return/output, correct receiver Monitor/arm/clip state and a matched
calibrated positive source/return/output baseline. Recording additionally requires
eligible arm/record and actual running transport. Confirm direct/dry and tapped
stages before isolation. A failed baseline, muted return, absent port, inactive
control, silent source or unavailable overload trace stays inconclusive.

Inspect menu/state/indicator roles separately from delivered audio/events, sample
and file metadata, timing/jitter and CPU/disk cost. A visible percentage, six bars
or mode label does not calibrate processing time, OS utilization or capacity.
Each command/default/branch needs separately retained evidence; no control case
closes a compound signal, timing, lifecycle or target clause.

## Requirements

### REQ-ER-001 — CPU meter menu

**D12/target-U.** The Control Bar CPU meter menu opens via its triangle or meter context click. Menu choices are public control roles; no numeric measurement or scheduler behavior is established.

Evidence/context: [RES-B012](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/resources-blocks.json).

### REQ-ER-002 — Average Current and off choices

**D12/target-U.** The CPU meter can display Average, Current (peak), or be switched off. Average is documented enabled by default; this is a current-chapter default, not observed target factory state. What exact load each mode measures remains an open source-context question.

Evidence/context: [RES-B011](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/resources-blocks.json), [RES-B012](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/resources-blocks.json), [RES-B013](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/resources-blocks.json).

### REQ-ER-003 — Combined meter presentation

**D12/target-U.** With Average and Current both enabled, both appear in the menu; the meter uses lighter/darker theme-dependent shades to distinguish the two. No fixed RGB, pixel, numeric averaging window or OS-total meaning is implied.

Evidence/context: [RES-B014](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/resources-blocks.json).

### REQ-ER-004 — Meter Text Shows selection

**D12/target-U.** Only one of the Average/Current percentage values is shown as meter text at a time; Meter Text Shows selects which. Numeric percentage and refresh timing are ungraded.

Evidence/context: [RES-B015](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/resources-blocks.json).

### REQ-ER-005 — Shared CPU warning controls

**D12/target-U.** Warn on Current CPU Overload in the CPU menu and CPU Overload Indicator in the Overload context menu share state. Enabling one enables the other; warnings are documented off by default, with exact-target default and thresholds unknown.

Evidence/context: [RES-B016](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/resources-blocks.json), [RES-B055](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/resources-blocks.json).

### REQ-ER-006 — Performance Impact visibility

**D12/target-U.** Mixer Performance Impact indicators can be enabled via Show/Hide Mixer Config or View Mixer Controls. This specifies public visibility entry points, not CPU calibration.

Evidence/context: [RES-B024](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/resources-blocks.json).

### REQ-ER-007 — Six-part track impact display

**D12/target-U.** Each track Performance Impact indicator has six rectangles lighting left to right for relative track impact. Level boundaries, detector, timing and track-to-track cost ratios are unknown.

Evidence/context: [RES-B025](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/resources-blocks.json).

### REQ-ER-008 — Unused I/O selection context

**D12/target-U.** Input/Output Config settings let users disable unused channels; the source says unused channels are not automatically disabled. Availability of actual channels retains the routing/settings owner, and no glitch or performance outcome follows.

Evidence/context: [RES-B018](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/resources-blocks.json), [RES-B019](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/resources-blocks.json).

Existing owners: [routing-monitoring-latency](routing-monitoring-latency.md), [settings-learning-workflows](settings-learning-workflows.md).

### REQ-ER-009 — Disk overload indicator role

**D12/target-U.** The Control Bar Overload indicator presents Disk for a disk read/write load issue. Exact trigger, detector, hold/reset behavior and processing capacity are unknown.

Evidence/context: [RES-B053](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/resources-blocks.json), [RES-B054](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/resources-blocks.json).

### REQ-ER-010 — CPU overload warning role

**D12/target-U.** With CPU warnings enabled, the Overload indicator presents CPU for processor overload. Indicator appearance does not define a current-load threshold, sample deadline or audio dropout result.

Evidence/context: [RES-B053](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/resources-blocks.json), [RES-B055](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/resources-blocks.json).

### REQ-ER-011 — Overload audio caveat

**D12/target-U.** The source describes disk/CPU load issues as potentially causing playback/recording dropouts or crackles. This is a conditional caveat, not guaranteed failure at a displayed value or a real-time capacity promise.

Evidence/context: [RES-B004](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/resources-blocks.json), [RES-B047](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/resources-blocks.json), [RES-B056](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/resources-blocks.json).

Ungraded source context: Disk and CPU load issues can cause audible dropouts/crackles; no detection or failure threshold is supplied.

### REQ-ER-012 — MIDI monitoring context

**D12/target-U.** The MIDI fact sheet distinguishes recording while hearing a direct hardware device from playthrough and describes monitoring-related added latency to record what is heard. Existing recording/routing owners keep Monitor/arm gates and latency options; no timestamp correction, buffer arithmetic or universal mode policy is added.

Evidence/context: [FACT2-B016](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-MIDI-FACT-SHEET-blocks.json), [FACT2-B018](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-MIDI-FACT-SHEET-blocks.json), [FACT2-B019](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-MIDI-FACT-SHEET-blocks.json), [FACT2-B045](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-MIDI-FACT-SHEET-blocks.json).

Ungraded source context: The chapter describes added monitoring latency for MIDI playthrough/recording and recommends monitoring off for direct-hardware listening or device-generated MIDI; exact target interaction with current monitoring options is unknown.

Existing owners: [recording-comping](recording-comping.md), [routing-monitoring-latency](routing-monitoring-latency.md), [external-hardware-devices](external-hardware-devices.md).

### REQ-ER-013 — MIDI reception during audio dropout

**D12/target-U.** The MIDI fact sheet says incoming MIDI reception/recording should continue through high-load audio dropouts, while playthrough may have timing errors/distortion and later playback should recover. This supplies no loss bound, timing accuracy or required recovery deadline.

Evidence/context: [FACT2-B021](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-MIDI-FACT-SHEET-blocks.json).

Ungraded source context: Publisher prose describes continuing incoming MIDI recording during audio dropouts and accurate later playback after recovery; no retained target event trace or output exists.

Existing owners: [recording-comping](recording-comping.md), [playback-core](playback-core.md).

### REQ-ER-U-CPU — CPU numeric and source-context outcomes

**U/target-U.** RES-B011 audio-processing-only wording and RES-B013 total-current wording do not settle Current scope. Ratio formula, averaging/current windows, numeric thresholds, sample-cost, OS CPU, thread/core scheduling and CPU/disk capacity remain unknown.

Evidence/context: [RES-B009](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/resources-blocks.json), [RES-B010](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/resources-blocks.json), [RES-B011](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/resources-blocks.json), [RES-B013](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/resources-blocks.json), [RES-B021](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/resources-blocks.json), [RES-B022](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/resources-blocks.json), [RES-B023](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/resources-blocks.json), [RES-B048](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/resources-blocks.json).

Ungraded source context: The source explains a processing-buffer-time ratio and gives an example, audio-only scope and total-current wording; these are not a calibrated numeric or scheduling oracle.

### REQ-ER-U-RENDER — Conditional undithered render comparison

**U/target-U.** Undithered render neutrality/bit-depth comparisons require independently retained finite inputs, explicit matching rates and no other processing under the existing export owner. No phase-cancellation, distortion minimum, dither or file oracle is supplied here.

Evidence/context: [FACT1-B007](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-AUDIO-FACT-SHEET-blocks.json), [FACT1-B008](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-AUDIO-FACT-SHEET-blocks.json), [FACT1-B011](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-AUDIO-FACT-SHEET-blocks.json), [FACT1-B012](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-AUDIO-FACT-SHEET-blocks.json), [FACT1-B013](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-AUDIO-FACT-SHEET-blocks.json), [FACT1-B014](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-AUDIO-FACT-SHEET-blocks.json), [FACT1-B015](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-AUDIO-FACT-SHEET-blocks.json), [FACT1-B016](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-AUDIO-FACT-SHEET-blocks.json), [FACT1-B017](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-AUDIO-FACT-SHEET-blocks.json).

Ungraded source context: The publisher reports cancellation for unprocessed matched-rate rendering to same/higher bit depth and minimal distortion for lower depth under its methodology; no source test data or target results are retained.

Existing owners: [audio-video-export](audio-video-export.md).

### REQ-ER-U-PLAYBACK — Matched-rate playback comparison

**U/target-U.** Unstretched same-rate untransposed playback comparison stays with playback/Clip View owners and excludes the hardware output stage. No broadened reconstruction identity, sample rounding, format or tolerance is established.

Evidence/context: [FACT1-B018](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-AUDIO-FACT-SHEET-blocks.json), [FACT1-B019](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-AUDIO-FACT-SHEET-blocks.json).

Ungraded source context: The fact sheet describes neutral playback for unstretched matching-rate untransposed files before audio hardware, verified by publisher cancellation tests.

Existing owners: [playback-core](playback-core.md), [clip-view-workflows](clip-view-workflows.md).

### REQ-ER-U-WARP — Conditional Warp and groove comparison

**U/target-U.** Identity-tempo Warp, tempo return/automation, mode and groove comparisons retain Warp/groove owners. No universal neutrality/non-neutral inequality for all inputs or DSP algorithm is inferred.

Evidence/context: [FACT1-B021](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-AUDIO-FACT-SHEET-blocks.json), [FACT1-B022](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-AUDIO-FACT-SHEET-blocks.json), [FACT1-B023](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-AUDIO-FACT-SHEET-blocks.json), [FACT1-B024](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-AUDIO-FACT-SHEET-blocks.json), [FACT1-B025](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-AUDIO-FACT-SHEET-blocks.json), [FACT1-B056](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-AUDIO-FACT-SHEET-blocks.json), [FACT1-B077](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-AUDIO-FACT-SHEET-blocks.json).

Ungraded source context: The publisher describes unstretched Beats/Tones/Texture/Re-Pitch neutrality, mode/tempo-automation caveats and non-neutral Complex/groove processing. Silence, identity settings and other conditions cannot prove a universal difference.

Existing owners: [warping-workflows](warping-workflows.md), [warp-markers](warp-markers.md), [groove-workflows](groove-workflows.md).

### REQ-ER-U-SUM — Mix-point comparison

**U/target-U.** Single/multiple mix-point numerical comparison retains mix/rack owners. Source 64-bit summing and 32-bit internal explanations are research context, not required candidate architecture, precision or associativity.

Evidence/context: [FACT1-B027](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-AUDIO-FACT-SHEET-blocks.json), [FACT1-B028](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-AUDIO-FACT-SHEET-blocks.json).

Ungraded source context: Publisher phase-cancellation tests describe single-point summing; its precision/architecture narrative and possible multi-point differences supply no new numeric tolerance or target output.

Existing owners: [mix-graph](mix-graph.md), [device-racks](device-racks.md).

### REQ-ER-U-RECORD — External and internal recording comparison

**U/target-U.** Bit-depth-conditioned external/internal recording neutrality stays with recording/routing/export owners. Actual A/D/source representation, accepted format, stage and retained results are required; no new recording codec, capacity or bit-exactness rule follows.

Evidence/context: [FACT1-B030](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-AUDIO-FACT-SHEET-blocks.json), [FACT1-B032](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-AUDIO-FACT-SHEET-blocks.json), [FACT1-B033](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-AUDIO-FACT-SHEET-blocks.json), [FACT1-B067](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-AUDIO-FACT-SHEET-blocks.json), [FACT1-B069](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-AUDIO-FACT-SHEET-blocks.json).

Ungraded source context: The fact sheet conditions external recording on source-converter depth and internal recording on 32-bit or unprocessed matching lower depth; it does not supply target capture files or hardware calibration.

Existing owners: [recording-comping](recording-comping.md), [routing-monitoring-latency](routing-monitoring-latency.md), [audio-video-export](audio-video-export.md).

### REQ-ER-U-FREEZE — Additional Freeze fact-sheet contexts

**U/target-U.** Freeze comparison and generated-file inspection retain the sealed Bounce/Freeze owner. The additional source descriptions of 32-bit files, Arrangement automation, Session values at Arrangement1.1.1, Beats/Warp and fixed random realization remain unverified context, not new target laws. The existing two-cycle role is not duplicated here.

Evidence/context: [FACT1-B035](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-AUDIO-FACT-SHEET-blocks.json), [FACT1-B036](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-AUDIO-FACT-SHEET-blocks.json), [FACT1-B037](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-AUDIO-FACT-SHEET-blocks.json), [FACT1-B038](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-AUDIO-FACT-SHEET-blocks.json), [FACT1-B039](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-AUDIO-FACT-SHEET-blocks.json), [FACT1-B040](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-AUDIO-FACT-SHEET-blocks.json), [RES-B027](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/resources-blocks.json), [RES-B040](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/resources-blocks.json), [RES-B041](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/resources-blocks.json), [RES-B042](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/resources-blocks.json).

Ungraded source context: Audio fact-sheet Freeze descriptions include file depth, tails/transport, Arrangement versus Session automation snapshot, Warp/Beats playback and rendered randomness. Their exact version/control/automation context needs evidence; existing frozen contracts remain unchanged.

Existing owners: [bounce-freeze-workflows](bounce-freeze-workflows.md).

### REQ-ER-U-BYPASS — Bypass comparison and latency context

**U/target-U.** Bypass comparison retains common device/host and compensation owners. Source identity and retained-device-delay wording do not establish zero-latency equality, universal bypass tails, reactivation or a new graph/DSP law.

Evidence/context: [FACT1-B042](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-AUDIO-FACT-SHEET-blocks.json), [FACT1-B043](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-AUDIO-FACT-SHEET-blocks.json).

Ungraded source context: The source describes bypassed signal identity but delay retention for delay-requiring devices; cancellation/alignment context and actual output are not retained.

Existing owners: [bundled-device-hosting](bundled-device-hosting.md), [plugin-hosting](plugin-hosting.md), [routing-monitoring-latency](routing-monitoring-latency.md).

### REQ-ER-U-ROUTING — Routing source-tap comparison

**U/target-U.** Routing neutrality comparison uses the selected source tap and destination under the existing routing/mix/Impulse owners. Pre/post-processing taps must not be compared against a different source-stage output as if identical.

Evidence/context: [FACT1-B045](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-AUDIO-FACT-SHEET-blocks.json).

Ungraded source context: The fact sheet calls routing neutral while warning source taps can precede processing/mixer or individual instrument outputs; this is no universal end-to-end identity law.

Existing owners: [routing-monitoring-latency](routing-monitoring-latency.md), [mix-graph](mix-graph.md), [device-impulse](device-impulse.md).

### REQ-ER-U-SPLIT — Split comparison

**U/target-U.** Already-neutral clip split comparison retains Arrangement/Clip View/playback owners. Source unwarped-loop examples, seamless/sample-accurate prose and cancellation reports do not override current loop eligibility or provide a boundary/sample oracle.

Evidence/context: [FACT1-B047](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-AUDIO-FACT-SHEET-blocks.json), [FACT1-B048](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-AUDIO-FACT-SHEET-blocks.json), [FACT1-B049](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-AUDIO-FACT-SHEET-blocks.json), [FACT1-B050](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-AUDIO-FACT-SHEET-blocks.json), [FACT1-B051](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-AUDIO-FACT-SHEET-blocks.json).

Ungraded source context: The publisher describes neutral splits and tests including loop-on/off unstretched/unwarped cases. Current Clip View unwarped-loop eligibility is a distinct source context requiring reconciliation, not silent owner expansion.

Existing owners: [arrangement-editing](arrangement-editing.md), [clip-view-workflows](clip-view-workflows.md), [playback-core](playback-core.md).

### REQ-ER-U-CONSOLIDATE — Consolidation file and normalization context

**U/target-U.** Consolidation stays Arrangement-owned. Source normalization/compensating clip-level and configured rate/depth descriptions remain unverified file/signal context, not new output-header or normalization laws in this packet.

Evidence/context: [FACT1-B071](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-AUDIO-FACT-SHEET-blocks.json).

Ungraded source context: The fact sheet says consolidation creates normalized configured-rate/depth files with adjusted clip volume; no generated file, field transform, normalization algorithm or numerical playback equality is supplied.

Existing owners: [arrangement-editing](arrangement-editing.md), [project-media-workflows](project-media-workflows.md).

### REQ-ER-U-PROCESSING — Processing comparison families

**U/target-U.** SRC/transposition, volume automation, dither, fades, panning and grooves stay with existing owners. Non-neutral classifications identify comparison dimensions, not a proof every input/output differs, a new metric, per-sample update law, required library or architecture.

Evidence/context: [FACT1-B053](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-AUDIO-FACT-SHEET-blocks.json), [FACT1-B058](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-AUDIO-FACT-SHEET-blocks.json), [FACT1-B060](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-AUDIO-FACT-SHEET-blocks.json), [FACT1-B062](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-AUDIO-FACT-SHEET-blocks.json), [FACT1-B064](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-AUDIO-FACT-SHEET-blocks.json), [FACT1-B065](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-AUDIO-FACT-SHEET-blocks.json), [FACT1-B073](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-AUDIO-FACT-SHEET-blocks.json), [FACT1-B075](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-AUDIO-FACT-SHEET-blocks.json), [FACT1-B077](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-AUDIO-FACT-SHEET-blocks.json).

Ungraded source context: Source descriptions include SoX, internal depth, per-sample volume updates, pan curves and fade/SRC/dither/groove neutrality classifications; existing finite numeric owners and their assumptions remain unchanged.

Existing owners: [audio-video-export](audio-video-export.md), [warping-workflows](warping-workflows.md), [automation-workflows](automation-workflows.md), [arrangement-editing](arrangement-editing.md), [mixer-values](mixer-values.md), [groove-workflows](groove-workflows.md).

### REQ-ER-U-MIDI — MIDI timing and publisher-report comparison

**U/target-U.** MIDI timing, monitoring/driver scheduling, serial transport, hardware scan and high-load recording comparisons require known accepted actual sources and clocks. Ideal-system and anonymous A/B/C historical tests provide no zero-jitter promise, target tolerance or current hardware proof.

Evidence/context: [FACT2-B006](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-MIDI-FACT-SHEET-blocks.json), [FACT2-B007](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-MIDI-FACT-SHEET-blocks.json), [FACT2-B008](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-MIDI-FACT-SHEET-blocks.json), [FACT2-B010](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-MIDI-FACT-SHEET-blocks.json), [FACT2-B011](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-MIDI-FACT-SHEET-blocks.json), [FACT2-B012](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-MIDI-FACT-SHEET-blocks.json), [FACT2-B017](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-MIDI-FACT-SHEET-blocks.json), [FACT2-B019](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-MIDI-FACT-SHEET-blocks.json), [FACT2-B020](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-MIDI-FACT-SHEET-blocks.json), [FACT2-B023](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-MIDI-FACT-SHEET-blocks.json), [FACT2-B024](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-MIDI-FACT-SHEET-blocks.json), [FACT2-B026](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-MIDI-FACT-SHEET-blocks.json), [FACT2-B029](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-MIDI-FACT-SHEET-blocks.json), [FACT2-B030](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-MIDI-FACT-SHEET-blocks.json), [FACT2-B032](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-MIDI-FACT-SHEET-blocks.json), [FACT2-B033](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-MIDI-FACT-SHEET-blocks.json), [FACT2-B034](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-MIDI-FACT-SHEET-blocks.json), [FACT2-B036](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-MIDI-FACT-SHEET-blocks.json), [FACT2-B037](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-MIDI-FACT-SHEET-blocks.json), [FACT2-B038](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-MIDI-FACT-SHEET-blocks.json), [FACT2-B040](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-MIDI-FACT-SHEET-blocks.json).

Ungraded source context: The publisher describes timestamps, monitoring latency, MME scheduling and an anonymous36-configuration A/B/C report with roughly ±1 through ±11ms observations. These are historical reported configurations, not project measurements or acceptance bounds.

Existing owners: [recording-comping](recording-comping.md), [playback-core](playback-core.md), [routing-monitoring-latency](routing-monitoring-latency.md), [midi-user-mapping](midi-user-mapping.md).

### REQ-ER-U-STATE — Control and engine lifecycle

**U/target-U.** Undo/cancel, persistence/restart, transport/record/automation interactions, rate/block/output changes, unsupported controls, malformed admitted inputs, concurrent engine operations and teardown remain unknown.

Evidence/context: [RES-B012](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/resources-blocks.json), [RES-B016](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/resources-blocks.json), [RES-B018](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/resources-blocks.json), [RES-B053](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/resources-blocks.json), [FACT2-B021](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-MIDI-FACT-SHEET-blocks.json).

### REQ-ER-U-LOSS — Resource and source failure

**U/target-U.** Source/device/port/disk loss, sustained load, memory/CPU/storage limits, overload trigger/recovery/cleanup, dropped MIDI/audio and fallback have no calibrated detector, timeout, silence, event-loss or repair oracle.

Evidence/context: [RES-B004](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/resources-blocks.json), [RES-B010](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/resources-blocks.json), [RES-B018](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/resources-blocks.json), [RES-B019](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/resources-blocks.json), [RES-B022](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/resources-blocks.json), [RES-B023](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/resources-blocks.json), [RES-B047](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/resources-blocks.json), [RES-B048](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/resources-blocks.json), [RES-B056](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/resources-blocks.json), [FACT2-B021](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-MIDI-FACT-SHEET-blocks.json), [FACT2-B026](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-MIDI-FACT-SHEET-blocks.json).

## Source-context questions

- **Q-ER-001:** RES-B011 says CPU meter audio-processing only, while RES-B013 calls
  Current total current CPU usage. Preserve both without equating Current to OS
  total or inventing windows/ratio calibration.
- **Q-ER-002:** FACT1-B049 includes splitting unwarped clips with Loop on, while
  Clip View REQ011 makes unwarped looping unavailable. The fact-sheet test context
  and current UI context are not silently reconciled; only actually offered
  prerequisites can be used, with exact-target outcome U.
- **Q-ER-003:** FACT1-B038's Session parameter snapshot at Arrangement1.1.1 needs
  exact automation/parameter/source-version context. It neither replaces current
  Session recording/override roles nor updates sealed Freeze behavior.
- **Q-ER-004:** FACT1-B042 combines bypass identity with retained device delay.
  Alignment, latency-bearing device and comparison context are unprovided;
  no zero-lag identity or dropout/tail behavior is inferred.
- **Q-ER-005:** FACT2-B019/B045 monitoring prose must be reconciled with current
  recording/routing latency options and hardware-direct versus playthrough setup.
  Monitor/arm gating and timestamps remain existing-owner/U boundaries.

## Acceptance cases

[50 proposed cases](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/cases.json)
cover 28 requirements: 13 D12 controls/source roles and 15 U obligations. Ten
cases have visible documentary predicates; 40 have null documentary oracles.
All 50 target outcomes are null/U/unexecuted. Fact-sheet tests use source_claim
only; no original result, numerical acceptance rule or new operation law is added.

| Case | Requirement | Kind | Focus | Documentary criterion |
| --- | --- | --- | --- | --- |
| ER-001 | REQ-ER-001 | control | CPU menu entry | visible named role only |
| ER-002 | REQ-ER-002 | control | Average Current and off | visible named role only |
| ER-003 | REQ-ER-003 | control | Combined display | visible named role only |
| ER-004 | REQ-ER-004 | control | Text source selection | visible named role only |
| ER-005 | REQ-ER-005 | state | Shared warnings off and on | visible named role only |
| ER-006 | REQ-ER-006 | control | Track impact visibility | visible named role only |
| ER-007 | REQ-ER-007 | control | Six rectangles relative display | visible named role only |
| ER-008 | REQ-ER-008 | state | Unused configured channels | visible named role only |
| ER-009 | REQ-ER-009 | state | Disk indicator role | visible named role only |
| ER-010 | REQ-ER-010 | state | CPU warning role | visible named role only |
| ER-011 | REQ-ER-011 | signal | Overload and delivered audio | U / null; source context only |
| ER-012 | REQ-ER-012 | timing | Monitored MIDI recording context | U / null; source context only |
| ER-013 | REQ-ER-013 | timing | MIDI during audio dropout | U / null; source context only |
| ER-014 | REQ-ER-U-CPU | numeric | CPU mode source context | U / null; source context only |
| ER-015 | REQ-ER-U-RENDER | file | Undithered same and higher depth | U / null; source context only |
| ER-016 | REQ-ER-U-RENDER | signal | Lower depth and dither context | U / null; source context only |
| ER-017 | REQ-ER-U-PLAYBACK | signal | Matching-rate source playback | U / null; source context only |
| ER-018 | REQ-ER-U-WARP | signal | Identity tempo Warp modes | U / null; source context only |
| ER-019 | REQ-ER-U-WARP | transport | Tempo return and automation | U / null; source context only |
| ER-020 | REQ-ER-U-WARP | signal | Groove neutrality context | U / null; source context only |
| ER-021 | REQ-ER-U-SUM | signal | Single and multiple mix points | U / null; source context only |
| ER-022 | REQ-ER-U-RECORD | file | External recording depth | U / null; source context only |
| ER-023 | REQ-ER-U-RECORD | file | Internal recording depth | U / null; source context only |
| ER-024 | REQ-ER-U-FREEZE | file | Freeze file depth context | U / null; source context only |
| ER-025 | REQ-ER-U-FREEZE | automation | Freeze automation snapshot context | U / null; source context only |
| ER-026 | REQ-ER-U-FREEZE | transport | Frozen tail stop context | U / null; source context only |
| ER-027 | REQ-ER-U-FREEZE | signal | Frozen mode and random realization | U / null; source context only |
| ER-028 | REQ-ER-U-BYPASS | signal | Bypass neutral source context | U / null; source context only |
| ER-029 | REQ-ER-U-ROUTING | signal | Routing matching tap | U / null; source context only |
| ER-030 | REQ-ER-U-SPLIT | signal | Split already neutral context | U / null; source context only |
| ER-031 | REQ-ER-U-CONSOLIDATE | file | Consolidated normalization context | U / null; source context only |
| ER-032 | REQ-ER-U-PROCESSING | signal | SRC and transpose comparisons | U / null; source context only |
| ER-033 | REQ-ER-U-PROCESSING | signal | Volume automation and gain | U / null; source context only |
| ER-034 | REQ-ER-U-PROCESSING | signal | Fades pan and dither families | U / null; source context only |
| ER-035 | REQ-ER-U-MIDI | timing | Incoming timing comparison context | U / null; source context only |
| ER-036 | REQ-ER-U-MIDI | timing | Outgoing MIDI and serial context | U / null; source context only |
| ER-037 | REQ-ER-U-MIDI | timing | Repeatability hardware buffer context | U / null; source context only |
| ER-038 | REQ-ER-U-STATE | boundary | Off disabled and unavailable options | U / null; source context only |
| ER-039 | REQ-ER-U-STATE | undo | Control undo redo | U / null; source context only |
| ER-040 | REQ-ER-U-STATE | cancel | Cancellation and menu dismissal | U / null; source context only |
| ER-041 | REQ-ER-U-STATE | persistence | Save restart and control retention | U / null; source context only |
| ER-042 | REQ-ER-U-STATE | transport | Transport and recording transitions | U / null; source context only |
| ER-043 | REQ-ER-U-STATE | sample-rate | Rate block engine transitions | U / null; source context only |
| ER-044 | REQ-ER-U-STATE | automation | Mapping and resource option ownership | U / null; source context only |
| ER-045 | REQ-ER-U-STATE | malformed | Malformed admitted settings | U / null; source context only |
| ER-046 | REQ-ER-U-STATE | teardown | Close while engine context active | U / null; source context only |
| ER-047 | REQ-ER-U-STATE | concurrency | Concurrent resource changes | U / null; source context only |
| ER-048 | REQ-ER-U-LOSS | source-loss | Input output or media loss | U / null; source context only |
| ER-049 | REQ-ER-U-LOSS | error | Disk and resource failures | U / null; source context only |
| ER-050 | REQ-ER-U-LOSS | recovery | Overload recovery context | U / null; source context only |

## Open obligations

[Q-027](../questions.md#q-027-whole-product-specification-evidence-and-version-coverage)
retains source-version/build applicability. No exact neutral render, reconstructed
waveform, per-mode response, file codec/depth/rate, ADC/driver correction, dropout,
jitter distribution, numerical CPU ratio or performance threshold is established.
Anonymous A/B/C and 36 historical MIDI configurations do not identify available
hardware, a zero-latency measurement apparatus or a current target tolerance.
Source ideal-system language supplies no zero-jitter promise.

Actual stimuli, accepted formats/ports/drivers, nonzero calibrated paths and
independent event/audio/load observations remain prerequisites. Undo/cancel,
save/restart, transport/automation/rate/engine transitions, source/device/disk
loss, malformed controls, concurrent operation and teardown remain U. Only
actually offered controls or independently understood formats may be used.
No hidden codec/schema, fake host, stress test or engine implementation is implied.

## Analyst evidence appendix

The original [fact capture catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/sources.json),
[resource provenance](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/resources-source.json)
and [combined source ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/sources-all.json)
remain unchanged. The reused resources bytes and original Bounce/Freeze capture
metadata are pinned in place. Source IDs/prefixes remain distinct; normalized
blocks retain exact HTML lines/anchors and never replace source bytes.

| Source | Retained blocks | Scope |
| --- | --- | --- |
| D12-AUDIO-FACT-SHEET | [FACT1-B001–B088](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-AUDIO-FACT-SHEET-blocks.json), HTML280 | §39 conditional audio comparison claims and publisher reports |
| D12-MIDI-FACT-SHEET | [FACT2-B001–B051](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/D12-MIDI-FACT-SHEET-blocks.json), HTML280–320 | §40 timing/monitoring/dropout context and historical report |
| D12-RESOURCES | [RES-B001–B056](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/resources-blocks.json), HTML280–390 | §38 public resource controls plus existing Freeze source context |

[Initial input pins](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/initial-input-pins.json),
[authority/reuse/parser pins](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/existing-authority-pins.json),
[counts](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/counts.json) and
[frozen manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/manifest-author-r1.json)
identify this review packet. The validator is read-only and emits stdout only;
no frozen report is created or rewritten on replay. Independent semantic review
is required; author integrity checks are not behavior or compatibility evidence.
