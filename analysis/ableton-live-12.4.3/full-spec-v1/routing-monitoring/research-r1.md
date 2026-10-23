---
id: RES-ROUTING-MONITORING-LATENCY
type: research
status: current
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3; documentary applicability unresolved
---

# General routing, monitoring and latency policy evidence

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
The one new mixing fetch used standard-library HTTPS; no tooling was installed.

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

The [draft](../specs/routing-monitoring-latency.md) has **40 requirements: 35 D12
and five U**. The [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/cases.json)
has **69 unexecuted definitions: 33 visible documentary control/state proposals
and 36 with null documentary expected/comparison fields**. All 69 target expected/
comparison values are null, all target grades U. No signal or timing case has an
invented output oracle; packet assertions are not compatibility passes.

The [fixtures](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/fixtures.json)
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

## Author freeze and validation

The [manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manifest-author-r1.json)
pins sources/extracts, requirement/case/fixture data, both canonical snapshots,
capture/validation code and the retained
[validation result](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/validation-author-r1.json).
Run the [validator](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/validate.py)
with Python 3 using -B to avoid bytecode artifacts. It checks source/capture
identity, exact block derivations, identifiers/evidence/counts/nulls, required
case kinds, ownership links/anchors, snapshots, payload hashes and authored
untracked-aware whitespace. Independent source/scope review is a separate gate.

No Live, original function, candidate, hardware/MIDI/audio or latency experiment
ran. No tooling was installed, release published or commit made. This packet is
an author-frozen partial draft for independent review, not a completed F-09 or
whole routing family. Root owns shared indexes, coverage, questions, execution
plan and append-only project log integration.
