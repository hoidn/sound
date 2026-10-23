---
id: RESEARCH-ENGINE-RESOURCE-WORKFLOWS
type: research
status: current
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3; current Version 12 documentary parity unknown
specs: SPEC-ENGINE-RESOURCE-WORKFLOWS
---

# Engine resource and fact-sheet evidence

## Question and provenance

The [canonical draft](../specs/engine-resource-workflows.md) adds public resource
control roles and ungraded audio/MIDI fact-sheet comparison obligations to the
[coverage plan](full-live-specification-plan.md) F-09. The
[coverage design](full-live-specification-design.md) governs partial closure.
Existing finite laws and immutable releases are not broadened. No original,
native, extracted function, candidate, audio/MIDI/hardware, network, load stress,
measurement or installation was executed for this packet.

Root retained two official fact-sheet pages and a byte-identical reuse of the
resources chapter before authoring. Preserve original sources/catalogs and all
195 derived blocks: FACT1 has88, FACT2 has51 and RES has56. The
[initial12-input pins](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/initial-input-pins.json)
record their unchanged identities. The
[original fact catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/sources.json),
[resources record](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/resources-source.json)
and [combined ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/sources-all.json)
retain their original file/capture_utc fields and distinct source IDs. Current
Version12 web prose has no exact12.4.3 or immutable publication revision guarantee.
Figures and linked help/PDF bytes were not inspected.

- D12-AUDIO-FACT-SHEET: [manual-audio-fact-sheet-2026-10-19.html](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/manual-audio-fact-sheet-2026-10-19.html), 259761 bytes, SHA256 `2c7cb127aae9505f42f0bc19bf9541ea419af4153f263b412cea0e4776df1159`, captured `2026-10-19T22:07:10.436513+00:00`; [official chapter](https://www.ableton.com/en/live-manual/12/audio-fact-sheet/).
- D12-MIDI-FACT-SHEET: [manual-midi-fact-sheet-2026-10-19.html](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/manual-midi-fact-sheet-2026-10-19.html), 252758 bytes, SHA256 `c324af2b58be0e8d2584a41a4e4f9a4e7a6fbfc1a93739f0d8f6b14ab5257b58`, captured `2026-10-19T22:07:10.389862+00:00`; [official chapter](https://www.ableton.com/en/live-manual/12/midi-fact-sheet/).
- D12-RESOURCES: [manual-12-resources-2026-10-19.html](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/manual-12-resources-2026-10-19.html), 258140 bytes, SHA256 `9d875319b2562a484f2de7b859d2a4d1bb3f3ef426605bc33c93a30609f75f23`, captured `2026-10-19T21:48:31.965101+00:00`; [official chapter](https://www.ableton.com/en/live-manual/12/computer-audio-resources-and-strategies/).

Resources SHA9d875319…75f23 is the exact existing Bounce/Freeze resource capture;
its original HTML path and resources-12-capture.json metadata are independently
pinned, not replaced by a current recapture. The existing Session chapter parser
is pinned and inspected before pure extraction; capture main is never executed.
Local copies/derivatives do not establish a second capture date or source version.

## Public resource controls

RES-B012–B016 supports CPU menu routes, Average/Current/off, combined shaded
presentation, Meter Text Shows and shared CPU-warning options. RES-B024/B025
supports mixer Performance Impact entry routes and six left-to-right rectangles.
RES-B018/B019 distinguishes explicit Input/Output Config from automatically
turning off unused channels. RES-B053–B056 names Disk and conditional CPU labels,
without supplying a trigger/hold/reset threshold, false-positive behavior or
capacity test. Potential dropouts are not guaranteed for every indicated value.

Q-ER-001 preserves RES-B011 audio-processing-only versus RES-B013 total-current
wording. The source buffer-time ratio, 50% example, OS scheduling/thread priorities,
core/cache/temperature and inactive-device/tail-processing narrative remain
context. They are not a new meter calibration, private architecture, idle-shutdown
observable assertion, workload clock or stress/performance oracle. Six bars do
not map to percentages or guaranteed cost ordering. Source stress advice and
likely-stable wording do not authorize or prove a load investigation.

## Audio fact-sheet comparisons and existing owners

FACT1-B007/B008's neutral list is explicitly contextual and incomplete (B088).
Its publisher testing/methodology claims are not project outputs. No neutral
classification proves a comparison once other gain/effect/fade/Warp operations
are active, and non-neutral prose is not a valid every-input inequality test:
silence, degenerate/identity controls and matching paths need explicit treatment.

- B011–B019: retain matching-rate/no-other-processing undithered render and
  unstretched/untransposed internal-playback conditions. Same/higher depth
  cancellation and lower-depth distortion statements have no input/output
  assets or metric. Export/playback/Clip View remain the owners.
- B021–B025/B056/B077: mode/identity-tempo, tempo-return/automation and groove
  claims provide no DSP, phase, history, quality or waveform equality oracle.
  Warp/groove owners retain their existing roles. Complex never-neutral wording
  is not made into a promise of differing samples for every source.
- B027/B028:64-bit single-point summing,32-bit internal and multi-node narrative
  are research context. Existing mix/rack/coefficient/unit/assumption owners
  remain canonical; no precision architecture or reassociation law is prescribed.
- B030/B032/B033/B067/B069: external A/D-depth and internal processed/unprocessed
  record conditions require actual accepted formats, sources and calibrated
  paths. No recording codec, gain math, ADC or file identity is supplied.
- B035–B040: retain Freeze depth/tail/automation/snapshot/Warp/Beats/randomness
  descriptions as U context under the sealed Bounce/Freeze owner. Its two-cycle
  role stays there. Q-ER-003 keeps the Arrangement1.1.1 snapshot's exact parameter,
  automation and source-version context open; no assumption about current
  Session clip automation or a fixed seed is adopted. New headers and repeated
  output need independent files/signals.
- B042/B043: bypass identity and retained latency require Q-ER-004 alignment and
  device context. No original device, waveform, tail or latency fixture is
  present; generic host/device and compensation owners retain their contracts.
- B045: routing comparison must match the selected tap and independently active
  receiver, not a different stage in the original chain. Existing routing/mix
  and Impulse owners remain canonical.
- B047–B051: splitting already-neutral clips and publisher cancellation claims
  provide no sample endpoint/interpolation result. Q-ER-002 preserves unwarped
  loop-on test wording versus current Clip View unwarped-loop unavailability;
  unsupported setup stays an unmet prerequisite.
- B058/B060/B062/B064/B065/B071/B073/B075: SRC/transposition, SoX, per-sample
  volume update, bit depth/dither, Consolidate normalization/compensating clip
  gain, fades and pan descriptions do not mint second operation/numeric laws.
  Source private library/precision/scheduling explanations stay contextual;
  existing export/automation/Arrangement/mixer owners and all their ungraded
  audio/header/transaction gaps remain unchanged.

Recommended high-rate/depth/hardware/32bit practices (B080–B086) are advice,
not new acceptance or spending recommendations. No universal quality metric,
required bit architecture or reference sampling environment follows.

## MIDI fact-sheet scope

FACT2-B006–B012 defines ideal recording/playback/playthrough and latency/jitter
terms, then explicitly explains the practical limits. It provides no zero-jitter
or perfect-response target promise. B017–B020's timestamp/buffer/driver scheduling
explanations remain context, not clock conversion, sample arithmetic, MME or
candidate-thread design. Q-ER-005 keeps B019/B045's monitored/direct-hardware
recording narrative distinct from current recording/routing Monitor gates and
Keep Monitoring Latency options. Actual source/controller/output and current
option contexts are prerequisites, not inferred from a device object name.

B021's incoming-MIDI continuation through audio dropouts is a scoped documentary
claim with null timing/event-loss output. It does not guarantee no audio distortion,
perfect event timing or recovery duration. B023–B026's serial transport, hardware
scan and driver timestamp uncertainty require actual accepted interfaces/clocks;
no apparatus is supplied or simulated.

B029–B040 reports the publisher's anonymous A/B/C apparatus and36 historical
configurations at roughly50% CPU across OS/rate/buffer conditions, with results
spanning approximately±1 to±11ms. Preserve the exact table in retained blocks;
it is not a current12.4.3 test, named current hardware inventory, project result,
measurement-error calibration or target tolerance. The source zero-latency
splitter/converter description does not establish a zero-delay available fixture.
No table row, majority range or no-noticeable-issues recommendation is converted
to acceptable jitter, a percentile or hardware-performance proof.

## Packet and remaining evidence

[28 requirements](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/requirements.json)
contain13D12 controls/source roles and15U obligations.
[50 future cases](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/cases.json)
contain10visible documentary predicates and40null documentary oracles; all target
outcomes are null/U/unexecuted. The
[fixture definitions](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/fixtures.json)
require accepted nonempty inputs/format, active nonzero processing/automation,
correct receiver record/monitor state, nonmuted wet return/output and matched
calibrated positive baseline before no-effect/exclusion probes. No media,
load/clock/controller/driver fixture or output is provided. Source labels/meter
presence/file headers alone cannot close signal or numeric requirements.

Undo/cancel/save, source/output/storage loss, unsupported/malformed controls,
transport/automation/rate/engine changes, concurrency and teardown remain U.
The [authority/reuse/parser pins](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/existing-authority-pins.json)
retain18exact identities, including existing canonicals and original resource
capture metadata. The [manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/manifest-author-r1.json)
seals every source/payload and canonical snapshot. The
[validator](../../analysis/ableton-live-12.4.3/full-spec-v1/engine-resources/validate.py)
is read-only, emits stdout and never rewrites frozen reports. It checks all195
blocks/line views, source/reuse/initial/authority pins, JSON/case coverage/nulls,
snapshots/links, browser ID equality and authored whitespace. Independent semantic
review remains required; no whole-engine or product compatibility follows.
[Q-027](../questions.md#q-027-whole-product-specification-evidence-and-version-coverage)
retains exact-version coverage. Root owns shared catalog/coverage/question/log work.
