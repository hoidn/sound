---
id: RESEARCH-MIDI-USER-MAPPING
type: research
status: current
updated: 2026-10-21
access: analysis
target: Ableton Live 12 Suite 12.4.3
---

# MIDI user mapping investigation

Question: which observable configuration and assignment rules can be derived
from the shipped user-controller documents and their bytecode paths before
investigating native MIDI arithmetic? The [source record](sources/midi-user-mapping-12.4.3.md)
pins nineteen retained files and the static decoder. The resulting behavioral
contract lives only in the [draft spec](../specs/midi-user-mapping.md); this page
owns the evidence interpretation and remaining investigation boundaries.

## Evidence and conclusions

The [parser findings](../../analysis/ableton-live-12.4.3/midi-user-mapping-v1/parser-findings.json)
(PARSE-01–10) and [mapping findings](../../analysis/ableton-live-12.4.3/midi-user-mapping-v1/bytecode-mapping-findings.json)
(BC-01–10) contain exact module, function, source-line and bytecode-offset
locators. All findings are static derivations conditional on the traced path.
They are not observed reference executions.

| Investigation | Result and consequence | Evidence |
| --- | --- | --- |
| Numeric parsing | Ordinary controls use disable/fallback rules; pad parsing has a separate direct-integer path and can raise rather than disable. Template comments alone cannot specify malformed input. | PARSE-01/02/08, BC-01 |
| Mode tokens | Unknown present tokens follow a different representation path from an absent mode. A safe Absolute fallback is not established. Native numeric transforms remain unknown. | PARSE-03/04/09 |
| Configuration syntax | Retained parser code establishes normalized option names, strict duplicate rejection and Boolean lexical rules; host error recovery is outside this trace. | PARSE-05/06/07 |
| Sparse controls and banks | Filtering and retained matrix ordering close the relevant width/order dependency. Counts and compacted order matter, not only numbered labels. | BC-02/03 and matrix supplemental capture |
| Bank navigation | Next-only and Next-plus-Previous follow different branches; extrapolating one navigation case to all configurations would be wrong. | BC-04 |
| Button input | Momentary/toggle and repeated-value behavior depends on control type; a universal rising-edge rule would be wrong. Native target-property side effects remain unresolved. | BC-05/06/07/09/10 |
| Held seeking | Static code nominates a task-based progression, but scheduler cadence and time-unit interpretation are insufficient for a real-time contract. | BC-08 |
| Internal profile naming | A source function transforms a name, but this does not establish discovery timing or the displayed surface list. | PARSE-10 |

The bank matrix dependency was initially a gap and was closed by an additional
bounded static capture. This demonstrates the intended investigation loop:
trace a dependency that changes the answer, without broad analysis of the main
native executable or launching Live.

## Contract and validation boundary

The [case matrix](../../analysis/ableton-live-12.4.3/midi-user-mapping-v1/acceptance-cases.json)
is a structured plan, not an executable harness. Expectations identify their
documentary/static provenance; unresolved cases cannot pass. Every case remains
unexecuted. No app implementation exists. A subsequent
[finite configuration handoff](../../handoff/midi-config-v1/README.md) releases
only four partial clauses with a separate 54-case fixture set; the broader
draft and its matrix remain unreleased.

Questions [Q-008–Q-010](../questions.md#q-008-midi-profile-parsing-and-host-errors)
retain host errors, numerical modes, timing/feedback and lifecycle gaps.
Continue with a targeted static dependency only when it blocks the chosen
contract. A runtime probe requires its own bounded question under
[ADR 0002](../decisions/adr-0002-static-first-analysis.md).

Separate author, evidence review and quality review are used for this draft.
The [scope recheck](../../analysis/ableton-live-12.4.3/midi-user-mapping-v1/scope-recheck.json)
and [quality review](../../analysis/ableton-live-12.4.3/midi-user-mapping-v1/quality-review.json)
approved the bounded draft after two scope corrections. They assess draft
quality, not clean handoff suitability or empirical compatibility.


## 2026-10-20 MIDI-user family routes — pending review

The [family route map](../../analysis/ableton-live-12.4.3/full-spec-v1/family-midi-user-routes-v1/structure.md)
reconciles current SPEC-MIDI-USER-MAPPING revision6 with the immutable
[midi-config-v4 finite release](../../handoff/midi-config-v4/README.md), retained
S4/N7/X2 sources and reviewed integration I-04/I-05 context. The older findings
and v1-only wording above retain their historical scope; numeric modes/takeover
now have the later source and finite-X evidence in
[native transform research](midi-transforms-native.md#extracted-execution-results-x2-2026-10-18).
That does not supply a running application profile, MIDI ingress, actual parameter
receiver, notification or public feedback path.

The route ledger is a bounded predicate/context inventory, not the13 requirement
IDs,56MT rows or161 released case objects as an outcome denominator. All four
on/off S-cond MT rows remain unreleased. X2 supplied parameter details/history,
simulated accessors/current value/setter and skipped Pick-Up notification; the
deferred path did not run. Preference default/wording, pad translation, actual
bank/track state, malformed-host recovery, precision exclusions, persistence and
held-control teardown remain qualified. All old cases/expectations/grades stay
unchanged; no original, provider, decoder, model, comparator or harness ran for
this map. Parent seal and independent review are pending; no new normative or
release scope is adopted.


## Family route review approval — 2026-10-20

The [independent family-map review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/family-midi-user-routes-v1-review.json)
approves bounded structure only. Manifest SHA256 `9e2b1a4916e58d05420aaea4d663d23da4f9d56aceef3b5c09f61252c9f79f59`;
review SHA256 `53c34080242ef66b0b0c075e7cda70126d4ee93a98d7af2f8ce73e7e0688d97d`.
The94contexts (19X/31S/44without complete route/oracle),161releaseobjects and56MTrows
are separate inventory/input units. All11frozen payloads and selected30providers/
84spans/13pointers verified;15negative checks passed. Actual X2 row43 supports
notification interception and PC jump; it does not establish real dispatch,
details construction, current parameter, setter, deferred or public delivery.
Four on/off MTrows remain unreleased; currentr6 precision and sequence exclusions
remain exact. Prior numerical/bytecode/native derivations are inherited, not
rerun. No new original/candidate execution, norm/case/release/grade, denominator
or whole-family completion follows. Root separately selects any later batch.

## Complete relative-byte class batch selection — 2026-10-21

The approved family map's MU-OUT-026/REQ-MIDI-USER-005 has a concrete unchanged, unpatched direct-call route for **eight relative modes ×128 legal CC bytes**, at the already supplied UNIT state: current0.5, range[0,1], nonstepped, sensitivity1, reversed0. This is one complete finite input class, not all19X contexts or a general parameter/ingress contract.

The existing X1 driver `run_pilot.py:219–225` and X2 `run_x2.py:507–523` supply initializer0x101bc1360 followed by value function0x101bb27b0, a16-byte input record `{float(byte),FLT_MAX,int(mode),1.0f}`, packed binary32 range and low-XMM0 binary32 result. No receiver, GDB interception, accessor/setter/notification simulation or new construction model is required by this selected route.

Of1,024logical observations,18exact direct-function results are inherited from pinned X1 `results/midi.json` and their existing evidence: mode1 byte1; mode2 bytes65/70; mode3 bytes1/8; mode4 bytes0/1/7; mode6 bytes1/64; mode7 bytes0/64/65/127; mode8 bytes1/65; mode9 bytes1/64. They are not re-executed or given fabricated historical process receipts. The selected new batch is **1,006 target evaluations plus eight initializers in eight sequential mode processes**, at most128calls/127buffers per process, below256limits. Complete1,024row provenance must distinguish historical from fresh inputs/results.

Mix authors one frozen input/code/source/image/harness/stub/environment/recording packet, Root is sole independent actual/source peer after final seal. Existing20s child bound, full stdout/stderr/memory/raw result lanes/PID/UTC/argv/exit/timeout/import/custody records and one-attempt/first-anomaly stop apply. No retry, fallback, model/tool/stub edit, old computation replay, new range/state axes, oracle fitting or silent nonfinite normalization. No runtime result is admitted until review. Actual ingress/parameter binding, receiver accumulation, pairing, takeover boundaries, deferred delivery, lifecycle and ARM/public behavior remain unresolved. No case/grade/release/site credit from selection; frozen691 X/1,076 S/3,857 none and main25,071+24=25,095 of268,015 unchanged; required U/product OPEN.

## Relative-byte batch review disposition — 2026-10-21

The [canonical native numerical adoption](midi-transforms-native.md#midi-relative-byte-whole-class-adoption--2026-10-21) records Root's sole approval of 1,006 fresh observations and 18 inherited joins at fixed UNIT state. The selected finite class is complete; actual ingress/receiver/public behavior and the other family X contexts remain qualified. That approval selected Mix's R7 delta and Auto's sole new-wording/mapping/IDs/preservation review. The later R7 adoption below supersedes that pending owner status; existing releases are unchanged.

## MIDI-user owner R7 finite annex adoption — 2026-10-21

The [canonical R7 draft](../specs/midi-user-mapping.md) is adopted after [Auto's sole composed-owner review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/midi-user-r7-owner-v2-review.json),52,085 bytes/SHA-256 `bd48ca3dbd273891836ce718f286ab7fb2cc823e126ddd0cf95d521aecb3a858`, with no blockers/corrections and final source window CLEAR. Root adopts by citation, without repeating the owner or actual review. The review pins [base proposal](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-midi-user-r7-relative-bytes-v1/manifest.json),3,367-byte manifest/SHA-256 `281c8916fe772f555e8a569e52fed05529ddf75c7d8e647594db3250d53b8aa6`, plus [Root's two-sentence overlay](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-midi-user-r7-wording-amendment-v2/manifest.json),903bytes/SHA-256 `a2732ecf608eac30e6a719bb22f48e698d85547f1e8ed99c3a7fdfe9ce866e76`. All14payloads/2,961,389bytes remain read-only. Exact composed owner:74,585bytes/SHA-256 `e2321ad10bc5ae8d56219f909cead0c0487b1347fc8197b52838e55007c328ae`; base-only74,510-byte text is historical intermediate.

R7 adds **MUR-REL-0001…MUR-REL-1006** under REQ-005, one per fresh point in the approved [fixed-UNIT class](midi-transforms-native.md#midi-relative-byte-whole-class-adoption--2026-10-21). The complete1,024-point catalog retains18 inherited observations without new IDs or fabricated fresh receipts. Auto checked every case/catalog/input/output/pointer join against Root's approved summary, without opening actual packet/source/raw. Twenty author and22independent owner/overlay controls pass; full eight-step reverse restores R6. The original five acceptance sets are expressly pre-existing, followed by the finite annex; each evaluation supplies current0.5 rather than implying a new process per case.

All12 other requirement bodies,56old MT rows,161released objects, general S law, precision/state/error/open-question/U clauses remain exact. Mode-name binding is inherited, not observed UI selection. Native x86 lowbinary32 results are finite expectations only; portable expected output and comparator remain NULL. Actual MIDI ingress/parameter receiver/current-value setter/accumulation/pairing/takeover/deferred/lifecycle/public/ARM gaps stay U. The family's19X contexts are not all completed by one input class. No release, application grade or indirect site. Current owner adoptions total **3,890 new finite draft IDs**, not a required-outcome denominator or pass count. Frozen691X/1,076S/3,857none; main25,071+24=25,095of268,015, bundles separate; requiredU/productOPEN.
