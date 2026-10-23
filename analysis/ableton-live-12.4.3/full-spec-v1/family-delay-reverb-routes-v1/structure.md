# Delay/Reverb family: bounded route map — 2026-10-20

Pending independent structure review. This analyst packet covers the current
[R3 owner](../../../../wiki/specs/delay-reverb-devices.md): Delay, Echo, Filter
Delay, Grain Delay, Reverb, Hybrid Reverb and Resonators. Its 93 requirements
and 176 cases remain unchanged. The approved owner manifest is
`9856e7114ce60caef1f3873874b6e3f58381ea0201177dccb487f81417063330`;
the corrected full-source R2 manifest is
`9e75cb77bf07b6a3260405041a6e3209192dc04bef319cc431a0f1fb62abfc38`.
These predecessors are pinned, without copying spec or case snapshots.

The [ledger](route-ledger.json) has **562 bounded required predicate/context
units: 0 X-route, 0 S-route, 562 no-established-route**. Its 316 D12 and 246 U
annotations describe source roles, not compatibility grades. Seven auxiliary
historical file assertions have S routes; they are outside the required count
and cannot close the lifecycle requirements to which their cases are attached.
Requirement IDs, case rows, numeric examples, helper calls, slots and individual
wave/menu/input samples are not outcome denominators. The inventory is limited
to this pinned owner, not a frozen whole-product denominator.

The current decision keeps coverage open until evidence supports it. Every
unsupported application outcome remains U and the closure gate stays OPEN;
there is no documentary-complete fallback. No-established-route is a current
bounded evidence finding under ADR0003, not impossibility or an exclusion.

## Integration cut and state ownership

This extends approved 1a, manifest
`392a738005f7d776dca96d7c78220cb94091081ef7086ec45b9397afccbe438b`,
and 1b, manifest
`7dddd59650ca3395d10e1b3c8aded3cda01d66b522dda4973a08f32e7bfb8f83`,
through I07/I08 and the approved Mix/Automation family context. It does not
start a disconnected device graph. [Eight component edges](chain-edges.json)
carry observed-static or unknown labels and retain the missing joins.

| Boundary | Exact retained context | What remains unknown |
| --- | --- | --- |
| Chain to output unit | Integration builder `102731438`, C1482–1489/1898–1903; InL/R `+168/+170` to TrackOut `+428` | Actual seven effect instances, input/output receivers, active chain order and host callback |
| Construction to registration | Integration named-port helpers `102321f5c/102321e6c/102322044 → 102312ed0 → 102312604`; endpoint virtual `+40` | Reached endpoint class/method, lifecycle and audio consequence; no device table attached to an arbitrary slot |
| Stored controls to running effect | Current owner, seven schema records and package-value records; selected model/module/processor metadata | Constructor defaults, accepted target domains, current value/provider, UI gesture dispatch and actual engine consumption |
| Envelope to current parameter | Approved automation map separates stored values, E(t), ideal P(t), parameter conversion and ramped samples | A3 loaded owner/provider and units, A6 settings, A8 lane/session/index, song/clip timebase, offset, clock and actual dispatch |
| Effect output to main/host | Mix `101b1c114`/`101b1afbc`; builder C1907–2016 | Actual effect/TrackOut receiver, buses/return ownership, host buffer, summation and scheduling |
| Hybrid API/list to engines | Four selected PyHandle/push-model/list-vector tables, six literal-store candidates | Actual Hybrid processor, admitted IR loader/content, Convolution/Algorithm delivery and public availability |

The component baseline remains 25,071 nonempty reference sites of 268,015,
with 24 separately conditional additions, combined inventory 25,095. No new
indirect site resolution is credited. Inherited integration search bounds are
depth3, top1,000 hubs except seeds, 80 nodes/200 edges per direction/level;
there was no new traversal. Receiver proofs and scalar/automation helper X
results do not transfer into these device outcomes.

Document/schema state belongs to the established storage owners; current
device controls, IR lists/references, buffer/grain/tail/random state and actual
audio clock remain distinct candidate state domains here. Matching class or
field names supplies no runtime ownership, persistence or delivery proof.

## Metadata census and retained source frontiers

[Census](metadata-census.json) and [query source](metadata-query.py) preserve
the preliminary excess and the separately approved semantic scope. A naive
casefolded substring query found380 tables/8,123 exported-prefix slots, including
Chooser false hits. A case-sensitive candidate regex found132 primaries but
also admitted mangled templates; exact leading-length simple-name matching
gave100 primaries. None of these preliminary row universes was retained.

Root approved the coherent fixed scope before retention: **29 primary tables,
91 selected slots, 43 stores, 132 aliases plus132 memberships, 182 call rows
plus13 indirect rows**. There are130 lexical-owner and29 RTTI rows, for690
retained DATA records. All caps passed:32 tables/512 selected slots/128 stores/
512 aliases+memberships/512 call+indirect. The full exported prefixes contain
1,698 slots as a separate metadata count. Twenty large tables retain only
header/store context and the leading3 construction/lifetime prefix; nine small
tables retain their whole exported prefix. Neither policy claims complete
native table extent, render callbacks or native control flow.

The scope contains seven named processor tables (including FilterDelayAdd), six
model/loader pairs, five modules/units, Echo's curve helper and four Hybrid API/
list tables. Generic audio/MIDI compensation, Looper, Collision/Meld, broad
converters, Push renderers and UI view tables were not selected. Requirements
at those unjoined boundaries remain present and U. No native absence is
inferred from the selection or the lexical-owner parser's sparse naming.

[Associations](processor-associations.json) give every selected table/store,
alias, call and indirect-row locator per device. [Native data](native-data.jsonl)
records exact provider path, source line/byte, row length/hash and record.
Literal-store records additionally carry their inherited chunk/row/code-line/
code-hash/warnings. Those C bodies were not reopened. All newly selected C-body
locators are null; this packet neither reads nor decodes native code.

| Nominal frontier | Examples retained as metadata only | Limit |
| --- | --- | --- |
| Filter Delay | `101bd6ac4` OnDelayTimeInMs, `101bd6b4c` OnDelayTimeInNote, `101bd6cd0` OnFeedback; named Repitch/Fade/Jump wrappers `101bd6cfc…101bd6d28` | Wrapper names and index calls do not prove timing, feedback, control units or a callable leaf |
| Grain Delay | `101bec250` OnFreq, `101bec2ec` OnSpray, `101bec394` OnRandomPitch, `101bec498` CalcMain | Grain window, RNG, pitch, reset and actual receiver remain unproved |
| Resonators | `102164918` OnResDecay, `102164b90` OnScaleAndTuning, `102164d6c` CalcMainWithReset | No frequency/tuning/decay/channel law or current voice binding |
| Delay/Echo/Reverb | `102ad733c` FilterCoeffs, `102b2cf14` OnUpdateDelayTimes, `102b2d090` OnUpdateData, `102e027c0` FdnFilterCoeffs | Labels nominate source frontiers; bodies, effective coefficient use and actual control delivery unselected |
| Hybrid | PyHandle and push/list metadata | API/list names are not IR loading, engine construction, active controls or two productive audio branches |

The 13 indirect rows remain qualified index data; none gets a new receiver or
site-resolution credit. There is no established self-contained X leaf in this
selected data scope. Expected leaf yield motivated selection, not a promise
that names or source-table prefixes establish computation or public routes.

## Observable inventory and preserved limits

[Predicate units](predicate-units.tsv) split stated roles and distinct
mode/gesture/state contexts. Broad runtime and lifecycle clauses are separately
enumerated by their stated observable domains, with unresolved actual control/
domain enumeration explicit. Numeric/menu examples stay with their predicates.
Every required row has exact owner byte/line/hash context, requirement or
universal acceptance source, related case navigation, source annotation,
prerequisite/batch pointers and a concrete missing join. Internal metadata
steps remain auxiliary rather than enlarging this count.

[Case navigation](case-navigation.json) points to all176 full current objects
and hashes every field without copying their bodies.149 old objects are exact;
27 added histories and all176 actual overlays remain null/U/unexecuted.169
application probes stay separate from seven historical Dpkg checks.93 current
requirements retain92 exact predecessor objects plus one Hybrid tab/color
clause. All existing grade labels and nulls remain unchanged.

[Prerequisites](prerequisites.json) preserve the current owner and fixture
qualification, particularly:

- Actual X/Y drags and Freq/Width slider movements are separate from old Delay005
  Filter toggle/role inspection; DRA-REVIEW-001 remains resolved at that scope.
- EACH admitted control/source/channel/voice/engine must be independently
  NONEMPTY productive with NONZERO wet output before signal negatives. BOTH
  compared paths need independent identity. UI-only gestures need no audio.
- Echo014 internal idle/shutdown, eightseconds and Noise+Gate remain research
  context, without CPU indicator, mechanism, processing stop or tail-cutoff law.
- Delay Freeze, Reverb Freeze/Flat/Cut and Hybrid Freeze/FreezeIn remain distinct.
  Actual NONZERO tail and independent A/B admission positives precede exclusion.
- Hybrid requires valid recognized owned nonidentity IR with a genuine Convolution
  response, separately productive Algorithm and BOTH before combined modes.
  Serial Algorithm remains Convolution-fed. Public routing/Blend isolation cannot
  be replaced with hidden-buffer assumptions. G18 refines old006/007 only:
  User-list remove/reinsert is separate from saved reference/preset persistence.
- No source adjective, minus60 definition, typical-room example, phase label,
  seed/reset/control name, quality or CPU description supplies an audio tolerance,
  complete domain, allowed range, RNG law, default or host-arrival promise.
- Buffer/sample-rate/block/tempo/transport/seek/loop, feedback stability, tail
  completion, Undo/Redo, cancellation, malformed/load/missing-media and device/
  track/Set/engine lifetime remain unresolved. Library/FP/ARM equivalence is not
  inferred from the retained ARM metadata or prior unrelated X results.

[Read receipt](read-receipt.json) distinguishes fresh full canonical clauses,
current case actions/control/limit fields and fixture reading from inherited
full207-context source judgments. [Source geometry](source-geometry.json)
freshly checks207 raw spans/line/column/source hashes and60 current case reference
joins. This is custody/locator checking, not a renewed full semantic/resource/
pixel/destination audit. Current manual D12 is not exact-target native evidence.

## Batch readiness and review boundary

[Batch inputs](batch-inputs.json) compactly enumerate selected metadata entries,
store candidates/prefix targets and current176 input/action/setup pointers per
device. Applicable actual parameter domains, receiver/object graph, method ABI,
mode/state/time history, imports/stubs and a numerical oracle remain explicitly
unresolved. No new finite harness input vectors or original calls are invented.
No source/execution/preparation successor is selected by this map.

The owned [read-only checker](check.py) verifies pins, source spans, selected raw
row locators/projections, caps, decomposition/case accounting, null/grade guards,
source geometry and full preserved research prefix. Meaningful in-memory
negative controls check missing/duplicated/promoted outcomes, changed source/
case/nulls, helper padding, prefix slot substitution, pin corruption and unsafe
prerequisites. Mechanical PASS is not independent semantic review.

Root owns seal, one independent structure review and shared atlas/index/plan/
coverage/log updates. No requirement, case, release or shared page is edited.
No original/application/native/provider/decoder/harness/model/comparator/fixture/
build/install or old author-module execution occurs in this packet.
