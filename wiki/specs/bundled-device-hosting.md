---
id: SPEC-BUNDLED-DEVICE-HOSTING
type: spec
status: draft
updated: 2026-10-22
access: analysis
target: Ableton Live 12 Suite 12.4.3 macOS arm64
revision: 2
---

# Bundled-device hosting: observable gaps and conditional mixing

## Scope and evidence conditions

This draft tracks the application behavior of Analog, Tension, Collision,
Electric, Corpus, Amp and Cabinet. The retained native source proves several
internal component transformations. It does not establish an independently
observable application boundary for their prepared buffers, queue order, event
partitioning, transport context or queue clearing. Those findings belong to
[non-normative research model checks](../research/device-host-protocol.md#non-normative-component-model-checks).
They impose no candidate interface, decomposition, call order or instrumentation
and are excluded from application compatibility coverage.

One conditional output-composition law is supported: settled Amp/Cabinet host
DryWet with wet output supplied as an explicit dependency. Its synthetic arithmetic
vectors are analyst checks, not captured device output or full-device audio closure.
All other application requirements below remain U. No original or candidate ran.

Stored parameters/defaults and name/value conversion belong to
[bundled-device parameters](bundled-device-parameters.md). Audio belongs to the
individual [Corpus](device-corpus.md), [Electric](device-electric.md),
[Tension](device-tension.md), [Analog](device-analog.md) and
[Collision](device-collision.md) contracts; Amp/Cabinet audio remains unresolved.
Common chain/rack editing belongs to [device racks](device-racks.md).

Evidence: **S** is statically derived for the pinned macOS arm64 build; **U** is
an unresolved application outcome and is ungraded. The draft contains **12
requirements: one conditional S composition law and 11 U requirements**. Its 26
case entries contain **three conditional S arithmetic cases and 23 U application
cases**. Eleven of the U entries additionally link to supported, non-normative
static component model checks. These 11 checks do not count as covered application
requirements or compatibility passes. Independent review and release remain
separate gates.

**C1, conditional composition only:** the selected Amp/Cabinet host-mix path is
successfully initialized, d is settled in [0,1], original dry Left/Right and wet
Left/Right are supplied explicitly, and the steady mathematical law is evaluated.
These inputs are a project decomposition for checking the algebra. C1 does not
establish the selection/scheduling path, a public wet-output observation point,
Amp/Cabinet DSP, floating rounding or an application audio oracle. Corpus's own
DryWet control belongs to its separate DSP contract.

For the conditional law, `OutputLeft` and `OutputRight` denote the mixed channels.
Other analysis input names appearing in the linked model checks identify recovered
internal component values; they define no required candidate interface. Former
r1 assumptions A1–A4 did not make those internal values application-observable and
are withdrawn as compatibility preconditions.

## Requirements

### REQ-BUNDLED-DEVICE-HOSTING-001 — Stereo effect input (U)

Application audio behavior for supplied stereo, silent and absent inputs remains
ungraded. The source's copy/zero and input-presence transformations are supported
internal findings; no composed device-output comparator establishes their audible
or other application-observable effect. The research model checks BDH-001–003
retain those finite derivations without imposing a prepared-buffer interface.

### REQ-BUNDLED-DEVICE-HOSTING-002 — Amp/Cabinet channel mode (U)

The application's audio response to DualMono changes and missing input remains
ungraded. Independent versus averaged wet-input preparation is supported internal
research, but the wet DSP and a composed output oracle are unavailable. Model
checks BDH-004–006 do not require a candidate to expose independent wet operations,
mono buffers or the original decomposition.

### REQ-BUNDLED-DEVICE-HOSTING-003 — Settled host DryWet (conditional S, C1)

For Amp and Cabinet at settled d in [0,1], let wet gain be `sin(d*pi/2)` and dry
gain be `sqrt(1-wet_gain^2)`. Each output channel combines its dry sample with its
wet sample using those gains. Endpoint d=0 is dry, d=1 is wet; d=0.5 gives equal
weights `sqrt(0.5)`. This is the steady mathematical gain law; sample-exact floating
rounding and the transition after changing d are ungraded (REQ-012).

### REQ-BUNDLED-DEVICE-HOSTING-004 — Control-change delivery (U)

The audio/behavior produced by repeated control changes and their timing remains
unresolved. Recovered pending-control coalescing, first-arrival order and delivery
count do not establish an application-observable UI/automation interval or a
required candidate queue. Model checks BDH-010/011 retain the source transformation;
a candidate must not fail solely because its equivalent output uses another order,
count or control-update mechanism. Parameter domains/conversions retain their
canonical owner.

### REQ-BUNDLED-DEVICE-HOSTING-005 — Event timing across processing ranges (U)

The application note/event timeline across processing ranges remains unresolved.
The internal coordinate-rebasing model BDH-012 is supported for its finite ordered
vector; timestamp origin, actual scheduler partition and composed audible timing
are not established. No block partition, native call count or intermediate event
coordinate is a compatibility requirement.

### REQ-BUNDLED-DEVICE-HOSTING-006 — Transport-dependent processing (U)

The audible behavior driven by transport position/tempo within processing ranges
remains unresolved. Model BDH-013 preserves the supported numeric subblock formula,
but scheduler context units, loop crossings and an external audio comparator are
unproved. A candidate need not expose the original subrange context or reproduce
its internal update trace.

### REQ-BUNDLED-DEVICE-HOSTING-007 — Rate-change note continuity (U)

The application note/audio response to a rate-change notification remains
unresolved. The source clears one internal pending-event queue and updates rate,
as retained in model BDH-014. Upstream note re-creation, held-voice continuity,
external input re-sends and reset output are not established. Absence in that
particular queue is not a required application observation or compatibility test.

### REQ-BUNDLED-DEVICE-HOSTING-008 — Reset output and initialization history (U)

The sound/state after ordinary reset, grouped parameter changes, new insertion or
sample-rate change is unresolved, including REQ-007 note continuity. A finite extracted
render using a chosen warm-up sequence does not prove Live uses it at insertion.
Keep the selected patch, held/released notes, resonator choice, control values and
rate in each reset comparison. Whether the resulting output is silent or retains
a particular tail must remain ungraded without a supported oracle.

### REQ-BUNDLED-DEVICE-HOSTING-009 — Activity and restart (U)

The exact host decision to suspend an idle device, resume it for audio/note/control
input and preserve tails is unresolved. Input presence, event/control arrivals,
previous output activity, smoothing and readiness all participate in the observed
path. Activity zero alone is insufficient evidence of immediate suspension.

### REQ-BUNDLED-DEVICE-HOSTING-010 — Load and processing errors (U)

Failure observables remain unresolved: missing bundle, failed executable load,
missing entry, null creation result, unsupported rate, processing failure and
crash. Notice wording, output/mute/bypass behavior, retries and recoverability need
supported outcomes before grading. Existing parameter-file rejection cases remain
owned by the parameter contract.

### REQ-BUNDLED-DEVICE-HOSTING-011 — Exit, cancellation and removal (U)

Static resource release does not establish the user-visible audio, pending-event,
undo or save behavior when a device is deleted or a load is cancelled. These
observables and the timing of teardown remain unresolved. Persistence/undo belongs
to the common device/rack contract; this draft owns only its processing boundary.

### REQ-BUNDLED-DEVICE-HOSTING-012 — Scheduler and remaining boundary inputs (U)

Unknowns include event frame base, real block sizes and residual frames, malformed
or unordered/out-of-range events, event overflow, velocity rounding, Corpus MIDI
side-chain/MPE, scheduler transport units and loop crossings, sample-exact DryWet
transitions, automation timing and grouped-change audio interruption. They cannot
be converted into compatibility passes by using a convenient harness default.

## Cases and non-normative model references

Only BDH-007–009 check the conditional composition law. Their wet samples are
synthetic analyst vectors and their proposed absolute arithmetic tolerance is
1e-6. They do not grade Amp/Cabinet output or settle any application audio case.
All other 23 entries are U application cases with no pass criterion. BDH-001–006
and BDH-010–014 also identify static model checks retained in research; their
intermediate comparators are non-normative and excluded from compatibility coverage.

| Case | Req suffix | Kind | Concrete input/action | Expected output/comparator |
| --- | --- | --- | --- | --- |
| BDH-001 | 001 | P/U | Analysis input retained in linked model BDH-001; corresponding application input/output comparator unresolved | Ungraded application behavior; non-normative component model only, excluded from compatibility coverage |
| BDH-002 | 001 | B/U | Analysis input retained in linked model BDH-002; corresponding application input/output comparator unresolved | Ungraded application behavior; non-normative component model only, excluded from compatibility coverage |
| BDH-003 | 001 | N/U | Analysis input retained in linked model BDH-003; corresponding application input/output comparator unresolved | Ungraded application behavior; non-normative component model only, excluded from compatibility coverage |
| BDH-004 | 002 | P/U | Analysis input retained in linked model BDH-004; corresponding application input/output comparator unresolved | Ungraded application behavior; non-normative component model only, excluded from compatibility coverage |
| BDH-005 | 002 | P/U | Analysis input retained in linked model BDH-005; corresponding application input/output comparator unresolved | Ungraded application behavior; non-normative component model only, excluded from compatibility coverage |
| BDH-006 | 002 | B/U | Analysis input retained in linked model BDH-006; corresponding application input/output comparator unresolved | Ungraded application behavior; non-normative component model only, excluded from compatibility coverage |
| BDH-007 | 003 | B/S/conditional | Synthetic analyst vector: Settled d=0; dry L=0.5,R=-0.25; wet L=0.125,R=0.75 | Output L=0.5,R=-0.25 within finite arithmetic tolerance; conditional algebra only, no device/application audio pass |
| BDH-008 | 003 | B/S/conditional | Synthetic analyst vector: Same samples, settled d=1 | Output L=0.125,R=0.75 within finite arithmetic tolerance; conditional algebra only, no device/application audio pass |
| BDH-009 | 003 | P/S/conditional | Synthetic analyst vector: Same samples, settled d=0.5 | Output L=0.625/sqrt(2),R=0.5/sqrt(2); conditional algebra only, no device/application audio pass |
| BDH-010 | 004 | P/U | Analysis input retained in linked model BDH-010; corresponding application input/output comparator unresolved | Ungraded application behavior; non-normative component model only, excluded from compatibility coverage |
| BDH-011 | 004 | B/U | Analysis input retained in linked model BDH-011; corresponding application input/output comparator unresolved | Ungraded application behavior; non-normative component model only, excluded from compatibility coverage |
| BDH-012 | 005 | B/U | Analysis input retained in linked model BDH-012; corresponding application input/output comparator unresolved | Ungraded application behavior; non-normative component model only, excluded from compatibility coverage |
| BDH-013 | 006 | P/B/U | Analysis input retained in linked model BDH-013; corresponding application input/output comparator unresolved | Ungraded application behavior; non-normative component model only, excluded from compatibility coverage |
| BDH-014 | 007 | P/U | Analysis input retained in linked model BDH-014; corresponding application input/output comparator unresolved | Ungraded application behavior; non-normative component model only, excluded from compatibility coverage |
| BDH-015 | 008 | U | Corpus Tube selected; excite and reset while sounding; compare fresh and ordinary-reset cases | Ungraded: Live-output reset/tail and initialization history unknown |
| BDH-016 | 008 | U | Analog held C4; change 44100→48000 | Ungraded: rate/reset sound and voice continuity; BDH-014 is a non-normative internal queue model, not application evidence |
| BDH-017 | 008,012 | U | Change 11 distinct mapped controls while a note sounds; compare same final values set one at a time | Ungraded: grouped-change fade/reset timing and audio |
| BDH-018 | 009 | U | Release Electric C4; return activity=0, wait, send note-on | Ungraded: exact host suspend/restart, first sounding frame and tail |
| BDH-019 | 010 | N/U | Missing bundle, missing entry, or null create result, tested separately | Ungraded: notice, output, retry and recovery |
| BDH-020 | 010 | N/U | Request 32000 Hz for Amp/Cabinet; separately inject process failure | Ungraded: unsupported rate/error behavior; no emulation authorized |
| BDH-021 | 011 | T/C/U | Begin note/load then delete/cancel device; undo/reopen separately | Ungraded: audible tail, cancellation, undo and persistence |
| BDH-022 | 012 | B/U | Note at clip/sample start, then coordinates 0 and 1 in matching host captures | Ungraded: timestamp base and device grid alignment |
| BDH-023 | 012 | B/U | N=513 and N=333 with maximum512; compare contiguous expected timeline | Ungraded: real scheduler partition and residual frames |
| BDH-024 | 012 | M/B/U | Reverse event order; negative or >=N coordinate; 2049 events in one subrange; 4097 arrivals | Ungraded: externally reachable validation/overflow behavior |
| BDH-025 | 012 | P/U | Tempo120 loop crossing; automate d=0→1; fractional velocity100.5; test separately | Ungraded: transport loop law, transition audio and velocity rounding |
| BDH-026 | 012 | P/U | Corpus MIDI side-chain note while transport runs; repeat with MPE expression | Ungraded: routing, event transformation and audible timing |

The three conditional S cases cover settled arithmetic boundaries/midpoint only.
Positive/negative-presence and internal timing/control vectors remain model-only.
Malformed, cancellation and teardown cases are retained U because the source cannot establish
their observable outcomes. Save/reopen/undo and device on/off editing are delegated
to their canonical owners; their interaction with active processing remains open
here. Instrument DSP and resampling quality have independent acceptance contracts.

## Analyst evidence appendix

**Native evidence qualification (2026-10-22).** The [sole-approved host instruction study](../research/device-host-protocol.md#three-method-host-native-contract-adopted--2026-10-22) distinguishes low32 callback-return projection from the separate activity pointer and preserves distinct capability-query returns. REQ-006/BDH-013's old numeric model remains non-normative; its association to native P+30 bytes/rate identity/FP state is unjoined. Do not treat it as a native expected-position oracle. Public requirements, all23applicationU cases and the old model artifacts remain unchanged; no x86-bundle return/guard or audible law follows.

Remove this appendix when preparing any clean handoff. Canonical evidence is
[device-host protocol](../research/device-host-protocol.md) and the retained
[revision 2 packet manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/device-host/manifest.json).
All record locators below are `live-records.jsonl` from that packet, pinned to
Live.arm64 SHA-256 `3a99ceeabce62ccd069b6b55d99d186c9bdf8a6b80a7e3350dd0f9d1c383cfad`.

| Requirement | Original function / retained record | Application claim limitation |
| --- | --- | --- |
| 001 | 0x102fc070c / 37; 0x102fc0e2c / 39 | Internal preparation only; application output U |
| 002 | 0x102fc0294 / 35; 0x102fc04dc / 36; 0x102fccddc / 48 | Amp/Cabinet wet DSP unavailable |
| 003 | 0x101df082c / 7 | Settled gain law only; proposed finite tolerance, no render |
| 004 | 0x102fccd28 / 45; 0x102fbfe54 / 32; 0x102fc0a38 / 38 | Internal queue ordering only; application timing/output U |
| 005 | 0x102fbe964 / 15; 0x102fcc390 / 40; N5/H4 maximum512 | Non-normative internal model; external note timeline U |
| 006 | 0x102fcce00 / 50; 0x102fbe964 / 15 | Non-normative numeric model; external transport effect U |
| 007 | 0x102fbfd80 / 31; 0x102fccd24 / 44 | One queue clears; application note/audio continuity U |
| 008 | 0x102fbf220 / 20; 0x102fbff98 / 33; ordinary reset / 26,42 | Dispatch uses four warmups; ordinary reset none; output remains U |
| 009 | 0x102fbe830 / 14; 0x102fc0e2c / 39; CalcMain / 43 | Return-type recovery, readiness and scheduler gaps |
| 010 | N5 loading/error canon | No new output/error trace |
| 011 | 0x102fccc48 / 41; 0x102fbf70c / 24; 0x102f999fc / 8 | Resource cleanup is not UI/audio equivalence |
| 012 | Records 15,28,38,43,50; N5/N6 and device DSP canon | Required unknowns retained, not omitted |

## Revision record

| Revision | Date | Change |
| --- | --- | --- |
| 1 | 2026-10-19 | Finite conditional host boundary: 12 requirements, 26 cases (14 S,12 U); 51 unchanged static records; no implementation or compatibility result |
| 2 | 2026-10-19 | Applies BDH-REVIEW-001/002: 12 requirements (1 conditional S,11 U); 26 cases (3 conditional S arithmetic,23 U application); 11 internal model checks excluded from compatibility coverage; exact r1 seal/payloads and all 51 source records preserved |
