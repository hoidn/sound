# Tension: supplied-device call chain and observable route inventory

Authored 2026-10-20; pending root seal and one independent structure review.
Analyst-only. Owner is [SPEC-DEVICE-TENSION revision 2](../../../../wiki/specs/device-tension.md),
15 requirements and 42 draft case IDs. The separately enumerated
[27 released finite evaluations](released-evaluations.json) are fixed inputs and
measurements from [device-tension-v1](../../../../handoff/device-tension-v1/manifest.json).
No specification, case, release, expectation, grade or U changed.

## Integration cut and method

The amended [plan revision 4](../../../../wiki/research/full-live-specification-plan.md#revision-4--analyst-depth-throughput-2026-10-20)
selects integration before component grading. This cut pins approved integration 1b
manifest `7dddd59650ca3395d10e1b3c8aded3cda01d66b522dda4973a08f32e7bfb8f83`,
[mix](../family-mix-routes-v1/structure.md) manifest
`c4ad95bef8e44db6c01c654f471347c6d666305894a104f3f5e3bff3d06fdab9`
and [playback](../family-playback-routes-v1/structure.md) manifest
`d69a45b394e6f1143a0efbaee61634aa5330ece0e1afe6c3d87a61d2304dc981`,
with their independent approvals. Packet1a component resolution is inherited at
`392a738005f7d776dca96d7c78220cb94091081ef7086ec45b9397afccbe438b`.
Exact selected source/driver/result/script identities are in [pins.json](pins.json).
Predecessor manifests retain their source universes; no spec snapshot is copied.

I-05/I-06 supplies scheduler/parameter context; I-07/I-08 supplies constructed
track-output ports and processor wrappers. Neither identifies the actual Tension
instance supplying a track's buffers. Playback's due-event virtual+0x10 dispatch
has no bound Tension event receiver. Mix's unit InL/R→TrackOut+0x428 construction
has no bound Tension instance output. Main/send wrapper receiver, actual bus
ownership, callback order and host/export delivery remain UNKNOWN. A type name,
component-table slot or similar buffer shape cannot close these joins.

No new traversal or indirect resolution occurred. Inherited mix search used three
levels per direction, top 1000 destination-hub pruning except explicit seeds,
80-node/200-edge bounds per direction/level; unexpanded final frontiers, pruned
helpers and 15 considered-function unresolved indirect associations remain.
Playback's retained 121 unresolved associations and terminal frontiers also remain;
these are local search units, not a full Tension or application census. Packet1a's
25,071 baseline resolved indirect sites and 24 conditional class-slot additions are
separate inventory units. Its OSend receiver proof cannot transfer to Tension.
No binary read, original/candidate/provider/harness/decoder execution or install
occurred here. Checks only parse retained text/JSON, hash selected files and inspect
finite scripts with Python stdlib. No WAV decoding or unchanged release replay.

## State, data and call boundaries

[Source map](source-map.json) gives nine component edges, 16 selected unchanged
host-source record locators (original chunk/line, record/code identities and retained
line), route bases and exact text spans. Observed-static means the retained code
contains the expression, not that Live invoked it; inferred names retain their
source qualifications. Historical extracted execution remains X only for supplied
calls. Source addresses in Live.arm64 use image base 0x100000000; the Tension export
addresses below are bundle x86_64 slice-relative and must not be mixed.

| Boundary | State/data owner and retained basis | Limit |
| --- | --- | --- |
| Stored parameter→host value | N6 StringStudio 130-entry vector, indices 0..129 except2; `tension.py:51–92`; REQ002 domain clamp, toggles, polarizers and conversions | Static relation; actual loaded parameter/automation/provider receiver unjoined. |
| Pending values→engine | Host records 45/32, `OnParameter`→`0x102fbfe54`; latest index values and first-seen order; cached index0 | Generic primary/secondary instance queue. Actual Tension receiver and edit scheduling unknown. |
| Scheduler→events | Records28/13/15; readiness/On filtering, logical-event conversion, ordered subblock translation | Origin0/1, upstream ordering/rounding, receiver and arbitrary request sizes unknown. Does not prove public sample placement. |
| Scheduler→transport | Records50/15 copy playing/position/tempo/loop state and conditionally advance split position | Producer unit and loop boundary unknown; stopped position0/120BPM is an explicitly supplied harness context. |
| Script→device exports | `tension.py:110–120`, `harness/xdev.c:32–91,98–148`; create0x17690→rate0x17780→parameter0x17bb0→CalcA0x178a0→destroy | Historical loader with substituted imports and original instance construction. This is outside the standing self-contained function call model for a new run; mapping grants no run authorization. |
| Device→retained signal | `run_tension.py:29–39`, runs registry; historical stereo binary32 bit identity→mono float WAV | Reviewed trace connects27 fixed outputs to frozen release samples/metrics; this map checks metadata/scripts without decoding or re-rendering them. |
| Device→track/main/export | I-07/I-08 construction and wrappers, integration MIX-E06/07–09 | UNKNOWN actual Tension instance/buffer receiver, dispatch, bus/output owner and delivery. No public waveform credit. |
| Reset/rate/teardown | Host records31/26/18/20/33/24, reviewed [protocol correction](../../../../wiki/research/device-host-protocol.md#initialization-reset-sample-rate-and-teardown) | Ordinary Reset/NewRate has no warm-up; ResetAndDispatch invokes four 1,024-frame helpers (4,096 total), then reset/index0 restoration. Historical Tension 1,024-frame test is only that finite sequence. Application continuity/removal/failure behavior unknown. |
| Readiness/activity→processing | Host records38/39/43/14; queue/grouped-change, activity and output-reference handling | Generic intermediate transformations are auxiliary, not added required outcomes. Exact stop/restart/tails and errors remain unknown. |

A1 supplies rate-before-parameters,129 values,16-byte events with block-relative
frames, stopped transport and input flag 0. A2 supplies 512-frame host blocks counted
from the first render frame. Existing static host analysis narrows transformations,
but does not establish these as Live's actual values for the selected instance.
Control-grid timing depends on partition; another partition can move an event by
one grid period. Units are frames at stated rate, cents and relative dB. Ringing
voices belong to a running instance; parameters are persistent state. Exact voice
end, lifecycle sound/continuity and new-device defaults remain qualified/unknown.

The retained bundle identity is x86_64 slice SHA256
`63dd07171e76e20427045cc0269e124d67e94e6cddb42cab82c77cec7e6ed05d`,
offset 16,384, length 501,392, in whole bundle
`db7eb728dc8567d14faadaa170829decab6511d068f2e69d9f4aeb272f077c6f`.
Import bindings substitute Linux library operations, deterministic clock/PRNG,
C++/locale/runtime support; `xdev_bind.c` documents them. Its perturbation helper
leaves integer-valued libm results unchanged. Loader/build/binding/initialization
steps are dependencies, not extra public requirements or standing-run approvals.

## Required predicates, finite evaluations and calibration

The [ledger](route-ledger.json) enumerates 93 required predicates from all 15 owners:
71 X-route, 12 S-route, 10 no-established-route. These bounded route counts are
**not grades, coverage, a frozen whole-product denominator or completeness proof**.
U rows retain unknown expected outputs. Twelve unresolved enumeration gaps are
separate. Compound predicates split where their observable relation differs;
tables define relations over input sets, not an outcome for each number. Two
explicit repeated cross-references (excitation-off silence and pickup delay) count
once. Helper-only host, loader and metric implementation leaves remain auxiliary.
The 42 unchanged DTN case IDs are navigation, not independent outcome units.

Each row has its exact owner span/digest/context, original evidence label, retained
route basis, missing joins and candidate batch set. Owner X labels remain X even
where this map records only a static conversion-check route; route classification
and source evidence label are different. Broader draft signal laws are not
silently promoted into the finite release. [Candidate sets](candidate-batches.json)
index the 68 named existing render inputs, named check sets, 31 sensitivity settings
and static mapping classes without numeric padding. They are inventories, not new
execution instructions. Unlisted continuous parameters/histories and unrendered
Geo/velocity/Body/filter/modulation/controller/mono behaviors remain unresolved.

The 27 release evaluations are a distinct finite unit set: 26 stable, one repeated
strike. Each points to its exact case/evaluation/metric, source script, retained
run/measurement/calibration and reference digest. The index copies no parameter
vector, event list, case body or metric snapshot. Zero input, all 129 binary32
comparison components/order, rate, length, 512 partition and zero warm-up are fixed.
Stable onset/windows/eligible partial centers, cutoff/window and strongest-reference
amplitude normalization are frozen. Missing/unmeasurable required partials fail
under the existing comparator. Repeated strike grades the waveform only.

Four chaotic settings and 37 uncalibrated settings are excluded. Draft chaotic
RMS/peak criteria supply no released statistical substitute, and bounded/non-silent
random-setting prose grants no accepted compatibility result. Seed-dependent
session differences are inferred. The five perturbations measure x86_64 numerical
sensitivity; arm64's 822 fused operations in 109 functions versus x86_64's zero do not
establish an arm64 or Apple-libm bound. No actual Live, arm64 or candidate output
was run or graded by this map.

## Author checks and handoff boundary

Run `python3 analysis/ableton-live-12.4.3/full-spec-v1/family-tension-routes-v1/author-check.py`
from the repository root. [Author results](author-check.json) record selected pin,
span, source-record, exact finite script/vector/trace and distinct-unit checks plus
negative controls. [Focused lint](lint-result.json) covers this packet and additive
canonical research links/prefix preservation. These checks are documentary and
structural; they do not validate DSP, ARM equivalence, public scheduling or audio.
The DamperVelocity ungated no-effect statement retains owner X provenance, but
its exact vector/result is not independently joined in the selected checks. Its X
route denotes the supplied device calculation, with that receipt gap explicit.
The mutable plan hash is an author-time selection identity, not a future freshness
gate; only exact selected inputs are replayed.

Root owns the seal, independent review, atlas/index/coverage/plan/log integration.
