# Analog v2: retained parameter-change history correction

Author-complete, pending independent review. This bounded successor addresses **ANRMAP-001** only. Frozen [v1](../family-analog-routes-v1/manifest.json) manifest SHA`7eb26d849e950f329d2dd94494f67389e6bf530f106461c7f6ca1a35986ce9fa` and its [final blocking review](../reviews/family-analog-routes-v1-review.json) SHA`1046e9cf911970e96aff9fa5fe9dd2ac2617c690e95f4f609f5d11eca45b0f19` are pinned. V1 is wholly preserved. Source records, owner/spec snapshots and the241-predicate ledger are not copied or re-derived.

The correction is that the legacy two-process parameter-change history **delivers its queued note twice**. AttackTime17734 remains an exact retained historical result; it does not establish an uninterrupted-held-sustain delay. No original rerun, changed expected value, case, release or grade is involved.

## Source and history proof

[history-correction.json](history-correction.json) records exact source-span hashes and retained-result pointers. [source-pins.json](source-pins.json) pins13 selected predecessor/review/method/result/qualified-owner files rather than replaying the old corpus or release.

| Retained source span | Established source fact |
| --- | --- |
| T12 `measure.py`715–729, especially719–723 | Eight existing control tuples; one queued note at4400; change and baseline each process13312frames twice in512frame blocks. Change adds one parameter command between intervals. Both persist the same instance and share the event history. |
| T12 `an.py`104–110 | The event command is queued once before the process sequence. No new event command is required for the later delivery. |
| T12 `harness/xdev.c`55–88 | `events`/`nevents` are global; every `process()` call initializes local`done=0`, scans the persistent queue using local coordinates and passes matching events to CalcA. The queue is not consumed. |
| T12 `harness/xdev.c`118–148 | Create occurs once; event commands append to the queue; both process commands use the same instance. No supported event-clear command exists in this driver. |
| T12 `results/protocol.json#/parameter_changes` | Eight unchanged first-different-frame scalars from those paired histories. The historical author label “attack time (held note)” does not override the actual driver input history. |

In process1, the queued frame4400 note is delivered by the callback starting4096 with offset304. Process2 begins at cumulative13312 and resets the local scan counter. The same queued frame4400 therefore enters the callback starting **17408**, again at offset **304**; its cumulative queued timestamp is **17712**. These are integer source-history coordinates. No exact device/audio effect at17712 is inferred: internal control-grid/state qualifications remain.

The seven earlier first-change values13332/13340/13376/13390 precede the second event callback17408. They retain their narrower finite first-change support under the supplied shared two-process history. They do not establish later ramps, arbitrary held/settled histories, actual Live automation timing or ARM equivalence. AttackTime's retained first difference17734 occurs after the repeated-note callback/timestamp, so interpreting it as an uninterrupted held-sustain response or smoothing latency is unsupported.

## Overlay contract and preserved units

[route-ledger.json](route-ledger.json) is an explicit overlay on the pinned v1 ledger. Resolve it by loading that exact base, applying `row_updates[id].set`, adding the one named history context and merging the named auxiliary protocol qualification. Only AN-OUT-222–231 receive history/context/join qualifiers; their IDs, observable-predicate text, requirement/source spans, route classifications, owner-basis labels and case/input links are unchanged. The other231 rows remain exact. The common method history is qualified without claiming the older missing generic context definition was a proof.

AN222–228 link the same seven early retained values and their finite scope. AN229 links the same17734 but explicitly rejects the uninterrupted-held interpretation. AN230's post-change ramps and AN231's other timing/latching remain U with investigative local X routes and no trajectory oracle. AN232 actual Live arrival remains unknown and untouched. Root has added the separate current-owner stale qualification, pinned as-of SHA`a63ceb8be20b5c24a7b3270ead540f45f79ee2eb01032d7f17516913c4ccd993` with [receipt](../reviews/analog-owner-anrmap001-stale-qualification.json) SHA`300ec5c63a9a9d005960380c14e2056301addf1e3cd279281d7d8e67d68d50e2`. Its23requirement bodies and39case table rows covering47IDs remain unchanged. This packet preserves the old full-owner identity historically, locates unchanged affected spans by exact text hash after the metadata shift, and never gates current owner bytes against that old identity or validates the stale “during sustain” wording.

[batch-inputs.json](batch-inputs.json) overlays only the inherited PROTOCOL group's history/meaning and parked P2's qualification. The203-index P2 universe is not an executable selected history or the next prepared batch. Existing13312 history cannot be reused as an uninterrupted-held template. Other selectors, including P1/P3, remain inherited historical/unselected data. This packet supplies no new history, inputs, waveform expectation, trajectory measurement, calibration or event-clear verb. Root may select one whole eight-control batch after correction review and applicable setup requirements; none is prepared or run here.

All decomposition units remain unchanged:241predicates,199X/30S/12no-established-route,128owner spans,64source entries,18call-index rows,90original source-pin units,37localU with investigativeX, and all241public bindings at no-established-route. The203controls/171stored parameters/31secondary outputs,38groups/42finite evaluations and helper/source dependencies remain separate from predicates and grades. Generic I07/I08 does not bind an actual Analog instance/output. A1/A2, fractional velocity, clock/seed/library/ARM, reset/rate/activity/lifecycle and public automation/output gaps remain inherited exactly. Existing release parameter-change/automation exclusions are unchanged; other single-process captures are not implicated.

## Author integrity and scope

Run only `python3 analysis/ableton-live-12.4.3/full-spec-v1/family-analog-routes-v2/author-check.py`. [Its result](author-check.json) verifies the exact v1/review pins, selected source spans and retained eight tuples/results, integer history coordinates, the10-row/PROTOCOL/P2 patch boundary, unchanged inventory/U/public bindings, affected owner spans and canonical-prefix preservation. Meaningful negative fixtures reject an uninterrupted-held label/claim for this repeated history, a false callback/timestamp, altered result and changed predicate. No retained module, study, model, comparator or harness is imported or run.

Only a dated correction is appended to canonical Analog DSP research, preserving its full earlier body including v1's historical section. Root owns shared catalogs/atlas, current-owner qualification, seal and independent review. No source snapshot, full prior universe replay, original/provider/decoder/harness/measurement/model/comparator/candidate execution, installation, normative/case/release change, new expectation or grade occurs here.
