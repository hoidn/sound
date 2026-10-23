---
id: RES-ROUTING-MONITORING-LATENCY
type: research
status: current
updated: 2026-10-19
access: analysis
revision: 2
target: Ableton Live 12 Suite 12.4.3; documentary applicability unresolved
---

# General routing, monitoring and latency policy evidence

**AS-OF AUTHOR FREEZE:** this narrow R2 successor awaits independent review.
Current disposition is routed through the [spec index](../specs/index.md).
This historical author-freeze statement does not assert the later review state.

## Scope and canonical owner

The [canonical draft](../specs/routing-monitoring-latency.md) owns general
routing choices, track taps, monitor-control context, submix/group/return/Main/
cue roles and latency-option policy. This page interprets sources rather than
creating competing contracts. The [coverage design](full-live-specification-design.md)
and [execution plan](full-live-specification-plan.md) retain full F-09 obligations.
No original device/application/candidate execution or hardware test took place.

The draft links finite [mix graph](../specs/mix-graph.md),
[mixer values](../specs/mixer-values.md), [playback](../specs/playback-core.md),
[recording](../specs/recording-comping.md), [external hardware](../specs/external-hardware-devices.md),
[plug-in hosting](../specs/plugin-hosting.md), [racks](../specs/device-racks.md)
and [export](../specs/audio-video-export.md) boundaries. None establishes general
latency arithmetic by composition. Recording REQ001/002 remains the canonical
arm/Off/Auto/In owner; this packet adds route/control contexts without copying
that gate table. External-device selectors/Hardware Latency remain device-owned.

## Sources and exact retained identity

The [source ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/sources.json)
pins five records: three official manuals and the original recording/racks
capture catalogs. Reused source IDs, URLs and capture timestamps are preserved;
the new packet is not a new capture of those earlier bytes.

| Source | Capture identity | Bytes | SHA-256 |
| --- | --- | --- | --- |
| D12-routing-and-i-o | [Routing and I/O](https://www.ableton.com/en/live-manual/12/routing-and-i-o/), captured 2026-10-19T19:53:57.390800+00:00; [retained original](../../analysis/ableton-live-12.4.3/full-spec-v1/recording/manual-12-routing-and-i-o-2026-10-19.html) | 286397 | `1a9c9c842c7a2d04b59794ee12d959f7fad15e3b67f41622109ea14e06e4b9b9` |
| RACKS-MAN-DEVICES | [Working with instruments and effects](https://www.ableton.com/en/live-manual/12/working-with-instruments-and-effects/), captured 2026-10-19T20:01:52.371400+00:00; [retained original](../../analysis/ableton-live-12.4.3/full-spec-v1/racks/manual-devices-2026-10-19.html) | 302488 | `6a783fde3de24178e1b1d4b8431ada1a1691a1c8f16a633f909bac347e72cd82` |
| D12-MIXING | [Mixing](https://www.ableton.com/en/live-manual/12/mixing/), captured 2026-10-19T21:33:28.556179+00:00 for the cue/track-delay gap; [retained new bytes](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-12-mixing-2026-10-19.html) | 276916 | `255923c650a256ea0c663e83351e3ac0d8f14ba8dfe12706825754b2066de02e` |

All three declare Version 12 without exact 12.4.3 behavioral parity. No source
page, linked tutorial or source instruction expands task authorization. The
[capture tool](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/capture.py)
parses retained HTML only, with no network, native or runtime execution.
The historical R1 mixing fetch used standard-library HTTPS; R2 performs no source fetch or installation.

| Extract | Scope | Exact blocks |
| --- | --- | --- |
| [Routing](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-routing-blocks.json) | Complete chapter 17; includes discovery context not specified by this packet | routing:B001–B125, 125 blocks |
| [Compensation](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-compensation-blocks.json) | Only §23.3 Device Delay Compensation | compensation:B001–B007, seven blocks |
| [Mixing](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-mixing-blocks.json) | Chapter 18 retained as context; only bounded route/choice/visibility claims selected | mixing:B001–B094, 94 blocks |

There are **226 retained paragraph/list/heading blocks** with exact HTML line,
anchor and heading context. Extraction stops before the site’s manual navigation;
images, figure content, linked help/FAQ/tutorials and their implied capabilities
were not separately inspected. Source extraction is not application observation.
No schemas, presets, binaries or recovered internal structures were needed.

## Interpretation boundaries

Observed in routing:B012–B017: monitoring prose describes the common Auto case,
In/Off, a keep-monitoring-latency context option, multi-selection and reset
contexts. The reset has audio/MIDI-specific values while the common description
calls Auto the default. This does not settle a universal factory/custom/new-track
or loaded Set default. [Recording REQ002](../specs/recording-comping.md#req-recording-comping-002--input-monitoring)
already preserves that contextual uncertainty. The source also varies the
keep-monitoring-latency caption slightly. The draft states the control’s role
without imposing one exact target label or an unmeasured timestamp rule.

Observed in routing:B023–B024: mono recording format, stereo device-chain signals
and mono/stereo conversions have documentary descriptions. Their calibration,
precision and composition with existing mixer laws are not established by this
packet. The corresponding numeric/channel probe stays U rather than creating a
second finite mixer calculation or conflating recorded format with monitor output.

Observed in routing:B074–B087: output-to-track and input-from-track topologies
have different many-to-one/one-to-many and solo contexts. Named Pre FX/Post FX/
Post Mixer points describe public signal access, not private graph nodes.
Solo behavior at a tapped track and at a rack-chain tap is not one universal
all-graph rule. Cases isolate sources, receiver, device and mixer contributions;
no gain, silence floor, leak tolerance, graph-cycle or timing law follows.

Observed in routing:B103–B125: MIDI taps and direct instrument destinations have
contexts distinct from final audio output. Multi-output/sidechain examples need
qualifying devices; Impulse’s internal slot-removal behavior is not generic
plug-in behavior. [Impulse](../specs/device-impulse.md), the host/rack owners and
[external hardware](../specs/external-hardware-devices.md) retain device-specific
semantics. No plug-in API or fake host is required or proven by a menu name.

Observed in the newer bounded mixing context: grouping retains custom child
outputs, and cue uses independently selected output destinations. These
conditions narrow the setup for the draft’s corresponding cases. The broader
mixing chapter is discovery context, not a replacement for existing finite
mixer/crossfade/automation laws.

Observed in compensation:B002–B007: automatic compensation, its switch,
Reduced Latency When Monitoring, timing-sensitive effects after a delayed device
and Track Delay availability are described. “In sync,” “lowest possible latency,”
sluggishness and CPU advice provide no measured threshold or computation. No
maximum-path arithmetic, delay subtraction, note timestamp correction, reported-
latency callback, block cadence or internal compensation architecture is specified.
Switch visibility is observable; resulting alignment requires separate evidence.

Inference: the three chapters can provide useful control-policy and qualitative
routing questions, but they cannot prove that all combinations of track/return/
group/cue monitoring, hardware, devices and recording/rendering compose as stated
for the target build. Reported latency and an enabled option do not prove a
working nonzero source/return or correctly compensated samples.

## Requirements, fixtures and required unknowns

The [draft](../specs/routing-monitoring-latency.md) has **41 requirements: 36 D12
and five U**. The [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/cases-r2.json)
has **70 unexecuted definitions: 34 visible documentary control/state proposals
and 36 with null documentary expected/comparison fields**. All 70 target expected/
comparison values are null, all target grades U. No signal or timing case has an
invented output oracle; packet assertions are not compatibility passes.

The [fixtures](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/fixtures-r2.json)
are finite future setups, not retained WAV/MIDI/ALS files, calibrated plugin
responses or hardware loopbacks. They demand independently identified compatible
sources/destinations, active device/monitor/clip context, nonzero gain/send/wet/
return and matched positive controls. Cue requires independently working outputs;
latency requires separately established path/reporting/measurement context.
Hardware/interface availability on this analyst host remains unproven. Failed
prerequisites and absent controls remain inconclusive/U rather than a silent pass.

Required unknowns retain mono/stereo matrices, signal/event delivery, meter
calibration, all numerical latency/driver/buffer/jitter/performance, route identity
and saved-state migration, source loss/reconnection, feedback/cycles, malformed
state, cancellation, undo/redo, automation, transport, rate/engine changes and
teardown. Future cases must pin actual accepted routes, bytes and measurement
uncertainty before defining numerical/timing criteria. Missing hardware or a
finite owner’s scope exclusion does not remove these whole-product obligations.

## Narrow Monitoring adoption

The [complete bounded Monitoring reconciliation](../../analysis/ableton-live-12.4.3/full-spec-v1/monitoring-source-reconciliation/README.md)
and its [independent review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/monitoring-source-reconciliation-review.json)
read nine Monitoring blocks, seven compensation contexts and selected owner
clauses/actions. Their two source-only proposals are adopted as bounded subsets:
RML-009 explicitly right-clicks each In/Auto button before toggling the existing
option; REQ-RML-036/RML-070 adds the source's categorical blue In Activator role
even with I/O hidden. This owner increment reads those exact selected contexts,
not a new whole Routing/Recording/device chapter audit.

The new display case uses separate audio/MIDI resets, genuine visible In
indicator baseline with I/O shown, actual known In state independent of color,
then hide/observe/restore and verify In. Failed/invisible/missing prerequisites
remain U. This does not infer RGB/theme/contrast, other-mode or disabled-Activator
colors, activation/audio behavior or transition timing. Existing RML006 full
arm/clip/mode matrix, RML007 selected Monitor dispatch and RML008 both reset entries
are already represented; no duplicates or new missing-context claim is proposed.
The contextual defaults, Off-mode option availability, Aux/recording distinction,
label variants and source-only compensation/latency goals remain unchanged.

All 40 old requirement records and all 69 prior case IDs/fields except the single
RML009 setup/action field are preserved. Old documentary and actual oracles and
source routes are unchanged. The new case has only a named visible categorical
color-role comparator, all actual target outcomes null/U/unexecuted. No extra U
template, source adjective/numeric/RGB/phase/timestamp/default/composition law,
complete topic or runtime result is added.

## Author freeze and validation

The [historical R1 manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manifest-author-r1.json)
and all 19 prior files remain unchanged in place; no whole archive duplicate is
made. [Exact delta](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/delta-r2.json),
[current catalogs/contexts](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/finite-contexts-r2.json),
[immutable inputs](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/inputs-r2.json)
and the [R2 manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manifest-author-r2.json)
preserve review/source history and current canonical snapshots. The new
[read-only check](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/validate-r2.py)
validates the R2 source/delta/prerequisites/IDs/nulls without running the old
validator against changed canonicals. Integrity is separate from semantic review.

[Consumer inventory](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/consumer-impact-r2.json)
preserves 18 literal old-spec hash records, including archive and explicit
historical-policy copies; these are not 18 active current tools. As-of owner
snapshots stay historical. No direct research hashpin was found in that finite
JSON search. Existing old checks/reports remain as-of their revisions; unchanged
old predicates are preserved. An additive owner advance does not automatically
require adapters or replay. Root owns any separately justified concrete current
dependency, failed required check or release-gate investigation; none is performed
or repaired here, and no frozen consumer/shared file is edited.

No Live, original function, candidate, OS/UI, hardware/MIDI/audio, account,
network/capture, installation or latency experiment ran. Positive histories are
future prerequisites, not retained successful executions. **AS-OF AUTHOR FREEZE:**
R2 review is pending; use the [spec index](../specs/index.md) for current disposition.
This remains partial F-09 with all unknowns intact, not a released or complete
routing family. Root integrates shared indexes, coverage, questions and logs.
