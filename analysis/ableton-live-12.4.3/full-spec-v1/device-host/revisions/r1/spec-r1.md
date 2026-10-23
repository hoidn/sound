---
id: SPEC-BUNDLED-DEVICE-HOSTING
type: spec
status: draft
updated: 2026-10-19
access: analysis
target: Ableton Live 12 Suite 12.4.3 macOS arm64
revision: 1
---

# Bundled-device hosting: finite processing boundary

## Scope and evidence conditions

This draft covers Analog, Tension, Collision, Electric, Corpus, Amp and Cabinet.
It specifies a finite **logical device boundary**: prepared audio/event/context
inputs and delivered control/state changes. This boundary allows comparison of
host behavior while treating device processing as a separately specified operation.
It does not require the original ABI, functions, memory layout, call count,
capability selectors or processor scheduling architecture. A mechanism having no
established audible or boundary effect is analysis only, never a compatibility
requirement. Whole-application audio equivalence does not follow from satisfying
these conditional boundary cases.

Stored parameters/defaults and name/value conversion belong to
[bundled-device parameters](bundled-device-parameters.md). Audio belongs to the
individual [Corpus](device-corpus.md), [Electric](device-electric.md),
[Tension](device-tension.md), [Analog](device-analog.md) and
[Collision](device-collision.md) contracts; Amp/Cabinet audio remains unresolved.
Common chain/rack editing belongs to [device racks](device-racks.md).

Evidence: **S** is statically derived for the pinned macOS arm64 build; **U** is
unresolved and ungraded. No case below has run against Live or a candidate.
The draft contains 12 requirements: seven conditional S boundary requirements
and five U requirements. The 26 cases comprise 14 conditional S cases and 12 U
cases. All remain proposed until independent review and release.

Conditions applying to S requirements:

- **A1:** The named device is successfully initialized and the corresponding
  processing path is selected. Existing parameter mappings apply. Engine output
  is supplied as a named input to host-mix cases; this is a contract decomposition,
  not permission to replace original evidence with an invented audio oracle.
- **A2:** Events have reached this logical host boundary in timestamp order. Their
  coordinates are given explicitly; conversion from clip/MIDI timestamps into
  those coordinates remains U. Split vectors use a positive frame count that is
  an exact multiple of the known 512-frame maximum and contain at most 2,048
  events in a subblock. They do not assert arbitrary host block sizes.
- **A3:** Transport vectors already supply the copied numeric position and tempo.
  The position unit and complete scheduler mapping remain U. Vectors avoid loop
  crossings and tempo changes inside the outer request.
- **A4:** A normal parameter delivery point is reached without the grouped-change
  path; fewer than 256 distinct controls are pending. UI automation scheduling
  and the audible block in which it arrives remain U.

## Named inputs and outputs

`Left`, `Right` and `AudioPresent` identify separate binary32 audio channels and
whether both channels are supplied. A buffer filled with zeros is present audio.
`WetLeft`/`WetRight` are the separately evaluated device result; `OutputLeft`/
`OutputRight` are the host mix. `DualMono` and settled `DryWet` apply only to Amp
and Cabinet's host mix. The Corpus control of the same name belongs to its own DSP.

`FrameCount`, `Events` (coordinate plus logical MIDI action), `Playing`, `Position`,
`Tempo` and integer-Hz `SampleRate` describe the processing request. `Prepared`
values are logical inputs presented to device processing. `PendingControls` and
`RateChange` describe control delivery and state changes. These names impose no
candidate interface or allocation design.

## Requirements

### REQ-BUNDLED-DEVICE-HOSTING-001 — Stereo effect input (S, A1)

For Corpus and the selected stereo effect path, when both audio channels are
present, prepared channels equal their respective input channels. When either
channel is absent, both prepared channels are zero. Input presence is distinct
from nonzero sample content. Instrument processing does not consume these stereo
audio inputs on this path; note synthesis expectations remain with each device.

### REQ-BUNDLED-DEVICE-HOSTING-002 — Amp/Cabinet channel mode (S, A1)

With DualMono enabled, the wet operation receives Left and Right independently.
With DualMono disabled, its mono input is `(Left + Right)/2` and its result serves
both wet channels. When either input is absent, prepared wet inputs are zero.
Dry samples retain their original stereo channels. No exact Amp/Cabinet wet audio
is asserted by this requirement.

### REQ-BUNDLED-DEVICE-HOSTING-003 — Settled host DryWet (S, A1)

For Amp and Cabinet at settled d in [0,1], let wet gain be `sin(d*pi/2)` and dry
gain be `sqrt(1-wet_gain^2)`. Each output channel combines its dry sample with its
wet sample using those gains. Endpoint d=0 is dry, d=1 is wet; d=0.5 gives equal
weights `sqrt(0.5)`. This is the steady mathematical gain law; sample-exact floating
rounding and the transition after changing d are ungraded (REQ-012).

### REQ-BUNDLED-DEVICE-HOSTING-004 — Pending-control replacement (S, A1/A4)

Repeated pending updates to one mapped control replace its previous pending value.
A delivery presents each distinct control's final value in first-arrival order;
subsequent delivery without new updates presents no updates. A secondary channel
processor, when required by channel mode, receives the same control values.
No rule about UI gesture/automation sampling times or intermediate audible values
is inferred. The canonical parameter spec supplies domains and conversions.

### REQ-BUNDLED-DEVICE-HOSTING-005 — Event coordinate preservation (S, A1/A2)

When a 1,024-frame logical request is partitioned into two 512-frame ranges,
ordered event coordinates in [0,1024) are assigned to the containing half-open
range, with that range's start subtracted. An event at 512 belongs to the second
range at coordinate 0; 511 stays in the first. This defines preservation of the
supplied coordinate, not its alignment with a real sample or the engine's control
grid. A candidate may use any partition yielding the same logical delivery and
specified device result; this requirement does not mandate two native calls.

### REQ-BUNDLED-DEVICE-HOSTING-006 — Transport within a split request (S, A1–A3)

At a subrange starting f frames into the request, the supplied context preserves
Tempo and Playing. When Playing is zero, Position is unchanged. When nonzero,
Position advances by `Tempo*f/(SampleRate*60)` before any loop adjustment. The
finite vectors exclude looping; loop crossings are ungraded under REQ-012.

### REQ-BUNDLED-DEVICE-HOSTING-007 — Rate-change event invalidation (S, A1)

On an accepted host rate-change notification with an existing processor, the
prepared processing state uses the new integer-Hz rate and its pending event queue
is cleared. Events already queued before that notification are not delivered by
that queue afterward. This says nothing about notes re-created upstream, sustained
voice behavior, external input re-sends or the audio produced during reset.

### REQ-BUNDLED-DEVICE-HOSTING-008 — Reset output and initialization history (U)

The sound/state after ordinary reset, grouped parameter changes, new insertion or
sample-rate change is unresolved beyond REQ-007. In particular, a finite extracted
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

## Acceptance cases

All S cases compare the named logical boundary values; they are statically
supported expectations, not retained executions. Audio-mix numeric comparisons
use absolute tolerance 1e-6 for the finite values below; this proposed tolerance
is only for arithmetic boundary vectors, not a device DSP metric. Control/event
comparators are exact. Context comparisons use absolute tolerance 1e-12 on these
binary64 vectors. U cases explicitly have no pass criterion.

| Case | Req suffix | Kind | Concrete input/action | Expected output/comparator |
| --- | --- | --- | --- | --- |
| BDH-001 | 001 | P/S | Corpus, present Left=[1,-1], Right=[0.25,-0.25] | Prepared channels equal each respective input; present=true |
| BDH-002 | 001 | B/S | Corpus, both channels present and [0,0] | Prepared zeros; present=true |
| BDH-003 | 001 | N/S | Corpus, Left=[1,1], Right absent | Both prepared channels [0,0]; present=false |
| BDH-004 | 002 | P/S | Amp/Cabinet DualMono=true; L=[1,-1], R=[0.25,-0.25] | Independent wet inputs [1,-1] and [0.25,-0.25] |
| BDH-005 | 002 | P/S | Same with DualMono=false | Mono wet input [0.625,-0.625], same wet result for both channels |
| BDH-006 | 002 | B/S | DualMono=false; L=[1], R=[-1] | Wet input [0]; original dry inputs retained as [1],[-1] |
| BDH-007 | 003 | B/S | Settled d=0; dry L=0.5,R=-0.25; wet L=0.125,R=0.75 | Output L=0.5,R=-0.25 within finite arithmetic tolerance |
| BDH-008 | 003 | B/S | Same samples, settled d=1 | Output L=0.125,R=0.75 within finite arithmetic tolerance |
| BDH-009 | 003 | P/S | Same samples, settled d=0.5 | Output L=0.625/sqrt(2),R=0.5/sqrt(2) |
| BDH-010 | 004 | P/S | Pending A=0.1, B=0.2, A=0.3; normal delivery | A=0.3 then B=0.2, once each; same values for any secondary processor |
| BDH-011 | 004 | B/S | Immediately deliver again with no new control | Empty control delivery |
| BDH-012 | 005 | B/S | N=1024,max=512; ordered note actions at coordinates 0,511,512,1023 | First range coordinates [0,511]; second [0,511]; note payload/order unchanged |
| BDH-013 | 006 | P/B/S | fs=48000,N=1024; Position=4,Tempo=120; substart=512; Playing=1 then 0; no loop | Playing case Position=4+8/375; stopped case=4; tempo and playing preserved |
| BDH-014 | 007 | P/S | Existing engine, queue note-on pitch60 at coordinate100; rate notification 44100→48000 before delivery | New processing rate 48000; that queue delivers no note-on |
| BDH-015 | 008 | U | Corpus Tube selected; excite and reset while sounding; compare fresh and ordinary-reset cases | Ungraded: Live-output reset/tail and initialization history unknown |
| BDH-016 | 008 | U | Analog held C4; change 44100→48000 | Ungraded: rate/reset sound and voice continuity; BDH-014 only grades queue invalidation |
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

S cases include positive, negative-presence and boundary inputs. Malformed,
cancellation and teardown cases are retained U because the source cannot establish
their observable outcomes. Save/reopen/undo and device on/off editing are delegated
to their canonical owners; their interaction with active processing remains open
here. Instrument DSP and resampling quality have independent acceptance contracts.

## Analyst evidence appendix

Remove this appendix when preparing any clean handoff. Canonical evidence is
[device-host protocol](../research/device-host-protocol.md) and the retained
[packet manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/device-host/manifest.json).
All record locators below are `live-records.jsonl` from that packet, pinned to
Live.arm64 SHA-256 `3a99ceeabce62ccd069b6b55d99d186c9bdf8a6b80a7e3350dd0f9d1c383cfad`.

| Requirement | Original function / retained record | Evidence limitation |
| --- | --- | --- |
| 001 | 0x102fc070c / 37; 0x102fc0e2c / 39 | Selected path only; no always-process guarantee |
| 002 | 0x102fc0294 / 35; 0x102fc04dc / 36; 0x102fccddc / 48 | Amp/Cabinet wet DSP unavailable |
| 003 | 0x101df082c / 7 | Settled gain law only; proposed finite tolerance, no render |
| 004 | 0x102fccd28 / 45; 0x102fbfe54 / 32; 0x102fc0a38 / 38 | A4 excludes grouped changes and full capacity |
| 005 | 0x102fbe964 / 15; 0x102fcc390 / 40; N5/H4 maximum512 | Stack-probe decompile, ordered finite multiples only |
| 006 | 0x102fcce00 / 50; 0x102fbe964 / 15 | Numeric context supplied; scheduler source units not independently established |
| 007 | 0x102fbfd80 / 31; 0x102fccd24 / 44 | Existing instance and explicit notification only |
| 008 | 0x102fbf220 / 20; 0x102fbff98 / 33; ordinary reset / 26,42 | Dispatch uses four warmups; ordinary reset none; output remains U |
| 009 | 0x102fbe830 / 14; 0x102fc0e2c / 39; CalcMain / 43 | Return-type recovery, readiness and scheduler gaps |
| 010 | N5 loading/error canon | No new output/error trace |
| 011 | 0x102fccc48 / 41; 0x102fbf70c / 24; 0x102f999fc / 8 | Resource cleanup is not UI/audio equivalence |
| 012 | Records 15,28,38,43,50; N5/N6 and device DSP canon | Required unknowns retained, not omitted |

## Revision record

| Revision | Date | Change |
| --- | --- | --- |
| 1 | 2026-10-19 | Finite conditional host boundary: 12 requirements, 26 cases (14 S,12 U); 51 unchanged static records; no implementation or compatibility result |
