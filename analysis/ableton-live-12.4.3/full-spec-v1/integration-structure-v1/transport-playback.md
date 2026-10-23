# Transport, quantized launch, and playback boundaries

Status: unsealed contribution to the single T1 integration packet. The approved
component-resolution manifest is `392a738005f7d776dca96d7c78220cb94091081ef7086ec45b9397afccbe438b`.
This is a static structure investigation, not a runtime ordering or audio-output
proof. The transport seed set separates message producers, a message consumer,
event dispatch, and playback data preparation rather than assuming they form one
continuous call chain.

## Selection and evidence

`transport-seeds.json` contains six forward entries and five backward sinks, all
exact internal ARM64 C1 function entries. `transport-seed-evidence.json` records
canonical nominations, alias line/byte locators, complete source-row identities,
metadata and warnings. `transport-source-records.json` retains the eleven freshly
read complete C projections (44,155 C bytes). Its `/records/i/record/code` line
numbers below are one-based lines within the retained code string, not native
instruction PCs. Source projection and prior canonical matching identify roles
conditionally; neither names nor field offsets establish current receiver types.

| Boundary | Observed source facts | Interpretation and open bridge |
| --- | --- | --- |
| Transport request producer `10276a7b0` | Record8 C55 calls `101a4b1d0`; C69 calls `101a4abd8` after state/engine/external-sync guards. | Canonical Start body requests beat-time and playing changes. Calls appearing in C order do not prove asynchronous delivery order, buffer position, or actual start. |
| Engine command consumer `101a524b8` | Record0 C10–16 deserializes one word and three byte locals, then directly calls `101a4ac8c`. | Canonical descriptor evidence associates these with Engine/Playing/ByUser/AllowCountIn. The sender-to-queue-to-this-consumer connection remains a separate descriptor/delivery boundary. |
| Clip-slot request `10245c72c` | Record6 C8–10 obtains a virtual result and `10273aed0` result, then forwards those and literals to `102710290`. | Canonical matching calls this AClipSlot fire. Decompiled argument positions do not independently prove native floating-register arguments or a launch grid. |
| Clip activation `101ad15e8` | Record2 branches on request fields, reads scheduler context through `101ab4558`, manipulates several containers, and dispatches virtual slots18/10 on one branch (C102–104). | Canonical Fire role is an inferred engine owner. Request admission, actual class of those virtual receivers, and delivery to MIDI/audio owners remain conditional. |
| Scheduler `101ab5cec` | Record1 removes entries from lists at owner+1d0/+1c0 and invokes entry virtual+10 (C101/C172); it computes a next limit and calls `101ab086c`. | Canonical sample/beat queues and clock context explain two time domains. Actual event implementation targets and host audio callback ordering are unresolved. |
| MIDI preparation `1028cf5c0` | Record10 allocates separate eight-byte time and 28-byte event arrays; writes record kinds0/1/2, iterates note-associated data, and sets output count. Full C includes recovered floating-return artifacts and nonreturn warnings. | Canonical per-key event-list builder, not proof of MIDI admission or delivery into an instrument. Matching producer/consumer data layouts alone would not establish a live connection. |
| MIDI consumer `101b48da8` | Record4 checks scheduler-context byte68; selects 28-byte records, handles kinds1/2 and other modes, and calls `101b492e4` on guarded branches (C108/C183). | Canonical MidiNoteAutomationPlayer Process role. Callback/function-pointer dispatch and final device/event route remain unresolved. |
| Float automation sender `1026f1e4c` | Record7 builds parallel time/value arrays, constructs `101ab7348` message (C43), adds count and two pointers (C45–47), then invokes message virtual+10 (C48). | Canonical FloatAutomation.Create boundary. The engine-side point-list consumer, exact provider ownership, clip timebase, and downstream parameter application are not supplied by this local sender. |
| Audio parameter writer `1027cab44` | Record9 serializes several virtual-return values, combines pitch-like values, calls interpolation chooser `1027bd748`, and serializes marker-derived integer data. | Canonical unwarped parameter writer; virtual-value sources and serialized values require matching receiver/descriptor premises. This is not sample rendering. |
| File-start-position calculation `10225b4e8` | Record5 computes a timing/position expression on one branch and delegates to `10224865c` on the other. | T13 audio matching.tsv labels this OWarperUnWarped::StartFileSmpl by formula. The name denotes calculation of a starting sample position here; this body does not establish OFadingPlayerBrain voice activation. |
| Clip end/repeat split `101adb0b8` | Record3 branches on clip byte+0b, uses scheduler context, calls `101a41050` in one path and `101ae7984` in another (C58). | Canonical source maps this to unwarped seconds versus warped beat scheduling. The real beat-to-sample Warp DSP path is still unknown; no interpolation algorithm follows from this split. |

## Retained message-registration associations

Static registration supplies useful structure even when queue behavior is unknown.
`transport-message-associations.json` pins five exact retained rows (path, line,
byte offset, row hash, function/code identity) and distinguishes inherited
semantics from the twenty complete source projections freshly read here.

* **SetPlaying:** the freshly read sender uses descriptor `106f55ea8`. Retained
  N3 initializer `101a8effc` names it OSetPlayingCommand; registration `101a50bd4`
  associates that name and Engine/Playing/ByUser/AllowCountIn members with handler
  `101a524b8`, whose full C was read here. The initializer/registration are exact
  N3 `live-functions.jsonl` rows31/28. This supports an **inferred registered
  message association** between the two owners, not an invented direct call or
  demonstrated queue delivery. It carries the original symbol-donor/architecture
  matching limits as well as the conditional OSend receiver proof.
* **Clip fire:** T13 `launch/matching.tsv` lines2/21/22 associates request producer
  `102710290` with sender thunk/body `102754ff0/102754ff8`, descriptor `10700d040`,
  and matched ARM registration `101af22f4`. Exact retained sender records are
  `launch/corpus-excerpts.jsonl` rows98/99; named Engine registration `14ee00` is
  row43. Its matched members include quantization and clip-fire settings, without
  a time member. This is an **inherited cross-build message association**; it does
  not newly establish an ARM handler-to-`101af0cbc` call or runtime admission.
* **Automation:** the fresh ARM sender constructs descriptor `106e522b0` and sends
  count/time/value arrays. T14 associates its point-list format with named Engine
  OFloatAutomation. That format relationship remains **inferred**; the Live x86
  cache address in the old notes is not the ARM descriptor address, and this
  contribution has not established an exact ARM descriptor-to-handler join.

The broad voice-start chain in playback research is explicitly an x86_64 claim.
The ARM StartFileSmpl association is specifically the first-frame calculation.
This contribution preserves that distinction and does not change the existing
value oracles, canonical spec, or release.

## Classification and unresolved connections

An **observed-static** edge means an exact retained call-site reference, or an
explicit expression in a retained C projection. An **inferred** boundary owner
uses the cited canonical/T13 correspondence and its prerequisites. An **unknown**
bridge lacks the receiver, descriptor, state identity, or runtime scheduling
connection needed to compose two observations.

The twenty-four packet1a OSend class-slot additions remain conditional. A caller
must reach the proved constructor, preserve the same object/address point across
opaque calls under the recorded ABI and noninterference premises, and dispatch
the selected slot at the exact PC. Their implementation target is not an
unconditional runtime target. Unresolved virtual event dispatch is retained as
unknown rather than treated as a disconnected endpoint.

Current explicit gaps are public gesture→request admission; command queue
ordering/delivery→engine consumer; actual scheduler-event classes; quantized
activation→the selected MIDI/audio/automation receiver instances; MIDI list→device
or instrument; automation list→active provider and parameter application; audio
parameter message→voice activation→render/host buffer; and clock/warp-marker data→
actual warped resampling. No observed sound, application outcome, or family
coverage is credited here.

## Boundary composition after source review

Nine further complete C projections are retained in
`transport-boundary-source-records.json`. Combined fresh semantic read scope is
20 functions / 78,694 C bytes; this is not a whole playback-engine read. Native
argument recovery remains conditional. In particular `101a4ac8c` has two
unrecovered-jumptable / indirect-jump-as-call warnings; launch preparation has
floating-return recovery artifacts and a globals-overlap warning.

| Transfer | Exact retained connection | State/data and limit |
| --- | --- | --- |
| Transport request → command packet | Start calls sender at `10276a8e8`; sender constructs with descriptor literal `106f55ea8`, writes a word plus three byte-like arguments and invokes slot10. | The descriptor and serialization support a control-message boundary; the exact packet1a conditional target at sender PC `101a4ac58` is `101ab7898`, subject to all receiver/vptr/opaque-call premises. The registered-handler association below is inherited/inferred; actual queue delivery and order remain unknown. |
| Command consumer → engine state | Handler `101a524b8@101a524f8→101a4ac8c`; guarded `101a4ac8c@101a4ad70→101a4af58`. | Boundary record1 has early-return callback branches; under its other guards it passes receiver+30 to the engine-state function. Record2 writes byte+60 only when changed, optionally sends a state message, then calls `101a54364` for enumerated domain results (`101a4b020`). Domain→scheduler control is not freshly read or proven here. |
| Clip request → producer-side launch settings | `10245c72c@10245c7a8→102710290`; latter directly forwards its assembled local settings to `102754ff0` (boundary record8 C122). | Producer-side virtual clip/song queries and request fields are observed; final sender and engine command admission are still a missing bridge. No direct UI→Fire edge is claimed. |
| Engine Fire request → prepare → activation | `101af0cbc@101af0e4c→101b0dc14`; `101b0dc14` uses local `auStack_140` as preparation output and later as argument to `101ad15e8` (record7 C44, C93/C107). | This provides a same-local-record source connection across the two calls, under their guards and ordinary call/alias premises. It is not merely equal field offsets in separate objects. The Fire-manager function also conditionally calls the already-read playing controller (`101af0eac`), connecting launch request and transport-control owners without proving realtime ordering. |
| Preparation → quantization/clock | `101ad0130` directly calls `101acffa4` (record5 C389); it reads scheduler context+70, calls `101abf294` under positive recovered quantization value (C429), and calls predelay helper `101ad1418` (C488). | The result record explicitly stores two doubles at output+20/+28 (C623/C624). Canonical T13 identifies launch time and earlier event time. This map retains that inference and floating-return caveat; it does not adopt a new timing formula or tolerance. Quantization function has active/stopped/selection branches, not a universal fixed grid. |
| End/repeat scheduling → event helper | `101adb0b8@101adb178→101ae7984`. | The already-read branch separates clock/clip conditions; actual scheduling-target implementation and audio Warp conversion remain unknown. |
| MIDI Process → event-construction helper | Two exact direct calls to `101b492e4` are indexed from `101b48da8`. | Recovered record-kind selection and a downstream helper call are observed. That helper body and final instrument/host event delivery are not read in this scope. |

The six additional direct-call pairs above (seven native PC rows) are retained in
`transport-boundary-edges.json`, including exact index byte/row hashes and C
line citations. They attach semantics to already-selected functions; they do not
silently add a fourth graph-traversal wave. A repeated callee's C lines are not
independently disambiguated to individual native PCs by this source lookup.

## Traversal checkpoint and finite omissions

The initial depth1 invocation failed before creating a graph file because the
shared helper consumed an obsolete overlay field. `transport-trace-attempt1.json`
retains that failure. The corrected helper SHA is
`d1fa658bc2e74449034348b34c79eead0e8487f04f118282dd44d8e6a4dc7c24`.
Its current source was read before execution. Depth1, depth2 and depth3 completed,
with the first two frontiers reviewed before proceeding; each output is preserved
separately along with `transport-frontier-depthN-review.json`.

| Wave | Forward edges / new nodes / hub-pruned rows | Backward edges / new nodes / hub-pruned rows |
| --- | --- | --- |
| 1 | 50 / 39 / 59 | 18 / 15 / 0 |
| 2 | 53 / 37 / 68 | 28 / 23 / 0 |
| 3 | 32 / 24 / 33 | 22 / 19 / 0 |

All waves have zero edge-budget and node-budget omissions. Hub pruning remains a
real omission: message constructors, serializers, memory helpers and shared
context accessors are not absent simply because the finite graph excludes them.
All hub-pruned rows remain in the trace artifacts. The 24/19 terminal frontiers
are retained but not expanded. The final trace retains 121 unknown indirect sites
from its considered functions; this is not an exhaustive count for terminal
frontier functions or the application. External metadata keys keep a separate
address domain. No forward/backward intersection was found within these finite
neighborhoods; that is not proof of runtime separation or absence of a route.

Traversal stops at depth3 and the selected twenty-source-function budget. No new
provider, decoder, original execution, harness, installation, or family map was
used. The selected integration structure remains partial, with all the explicit
public/async/receiver/render/Warp bridges above unresolved.
