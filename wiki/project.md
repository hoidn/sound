---
id: PROJECT-OVERVIEW
type: overview
status: active
updated: 2026-10-23
access: neutral
---

# Project scope and status

The project is establishing an evidence-based process for an independent
desktop application covering Ableton Live workflows. The user requested a
persistent LLM-maintained wiki including specification and implementation
documentation. Whole-app coverage is the planning scope; completion of the
documentation structure is not completion of the application.

## Current state

| Area | State |
| --- | --- |
| Documentation routing and schema | Established in this workspace |
| Reference target | Ableton Live 12 Suite 12.4.3; identity pinned and arm64 slices re-derived on the current host; the earlier static evidence tree is absent here (see research index) |
| Analysis workstation | Linux host provisioned 2026-10-17 with Ghidra 12.1.4, JDK 21 and REA 6.5.0; Push2 smoke test reproduced prior counts; persistent Live project at `/var/tmp/sound-analysis`, analysis running (see [execution ledger](research/native-phase-execution.md#linux-workstation-provisioning--2026-10-17)) |
| Research | Retained native corpora, method guides and reviewed recovery tooling; [bounded component and integration maps](research/program-structure.md#t1-scenario-integration-map--2026-10-20) now support family route work; unresolved source/runtime joins remain explicit |
| Behavioral specifications | Partial draft contracts spanning T1 and broader device/workflow/UI scope; 36 partial releases, 19 current (see [spec index](specs/index.md)) |
| Implementation | No application code; architecture choices remain proposals |
| Verification | No retained original-versus-candidate compatibility results |
| Clean implementation workspace | Provisioned 2026-10-19: sparse worktree `~/Documents/sound-impl` (branch `impl`); this checkout contains analyst material |
| Published handoffs | 36 releases, 19 current; see the [catalog](../handoff/index.md) for scope, supersession and the corrected fixture defect. All cases are unexecuted against Live |

## Current phase

Current execution (2026-10-23 UTC) is recorded in the [plan checkpoint](research/full-live-specification-plan.md#current-execution-checkpoint): **24,051 draft case additions**, not passes, with36partial releases/19current and main25,095of268,015 indirect sites. [The user confirms Claude's handoff](decisions/adr-0006-reference-observation-reopened.md#confirmed-handoff-and-windows-sitting-priority-supersede-static-queues--2026-10-23): Root alone controls the offline/no-NIC Windows guest, prioritizing **Session0 then all nine SessionA records** over further zero-case S work and static peer queues. Workers provide host-only support/docs. Claude reports authorized-offline Live12.4.3/build2026-07-07_e3d8be4d07/hash92e7943d…e0539, Windows11Pro26300/26H2/unactivated observer profile and44.1kHz ich9HDA audio; actual resumed guest identities/capabilities/results remain UNVERIFIED. The203924 authorization-session crash is separate setup history. Earlier process1588360 vanished before the first key; Root ran the supplied existing-disk script once offline, without duplicate boot/reinstall/revert, and reports newPID1590872. Earlier signed-build/copy/hardware-code/capacity/hold captures remain ASOF. No key/media/AUZ/credentials request is added. Analog57 is author-partial-frozen; Clip9, Automation frontier and MNS once-census terminal records are frozen UNREVIEWED with static peers parked/unbegun. One sole NEW sitting-evidence/code review follows freeze, inheriting approved INPUT/source proofs. ReviewedO remains0, unsupported required behavior stays unknown and wholeLiveOPEN.

On 2026-10-19 the user expanded the analyst target to the entire Live product
surface under [ADR 0005](decisions/adr-0005-full-live-specification-coverage.md).
The [full specification plan](research/full-live-specification-plan.md) is the
current work selector. Its amended
[revision 4](research/full-live-specification-plan.md#revision-4--analyst-depth-throughput-2026-10-20)
(2026-10-20, user direction) selects symbol-based component recovery and
class-level indirect-call resolution, then the T1 integration map, family maps
and batch extracted execution. The restricted implementation worktree (T1.6)
is provisioned at `~/Documents/sound-impl` and idle; T1.7 is deferred until
whole-product specification closure or explicit user resequencing.
The inventory baseline is independently checked.
Reviewed partial contracts now
span editing/recording, MIDI/racks, host classification, browser/projects/export
and selected devices. Further device, media and UI/control packets are being
authored, corrected and reviewed; current assignments and dispositions belong
to the plan. Whole-product coverage remains incomplete; existing partial
releases do not change that status. T1 remains the first bounded candidate target,
with T1.6 provisioning recorded in plan revision 3; candidate implementation
and conformance evidence remain separate work.

On 2026-10-20 the user directed that the specification is completed before T1
is implemented and that depth starts from call chains across components.
[Plan revision 4](research/full-live-specification-plan.md#revision-4--analyst-depth-throughput-2026-10-20),
[design revision 11](research/full-live-specification-design.md#revision-11--structure-packets-batch-evidence-and-harness-authorization--2026-10-20)
and [roadmap revision 5](research/native-decompilation-roadmap.md#revision-5--depth-throughput-alignment-2026-10-20)
put component/indirect-call recovery, a reviewed cross-component integration
map and family call-chain maps ahead of case grading, batch extracted execution
under a standing harness authorization, run harness sessions in parallel and
defer T1.7. The user confirmed on2026-10-20 that required behavior without
supporting evidence keeps coverage open; [ADR0005](decisions/adr-0005-full-live-specification-coverage.md#completion-rule-confirmation--2026-10-20)
owns this closure rule. A documentary inventory of unknowns does not satisfy it.
On 2026-10-21 the plan's [second amendment](research/full-live-specification-plan.md#second-amendment--batch-adoption-authorization-scope-and-x-count-ordering-2026-10-21),
[design revision 12](research/full-live-specification-design.md#revision-12--review-once-batch-adoption-and-authorization-scope--2026-10-21)
and the [roadmap amendment](research/native-decompilation-roadmap.md#revision-5-amendment--yield-ordered-depth-and-one-review-per-standing-packet-2026-10-21)
responded to the first ledger totals: batch review approval admits observations
into owners' revisions, standing packets carry one review, depth is ordered by
ledger X count, and checkpoints state the totals. Most enumerated predicates have
no evidence route under ADR 0003 and stay U under the confirmed closure rule.
Later on 2026-10-21 the user reopened that restriction:
[ADR 0006](decisions/adr-0006-reference-observation-reopened.md) authorizes
whole-application observation (evidence label O) once a reference host is
recorded; [plan revision 5](research/full-live-specification-plan.md#revision-5--reference-observation-route-2026-10-21)
and [design revision 14](research/full-live-specification-design.md#revision-14--reference-observation-evidence--2026-10-21)
add the route, the observation packet and the host decision D-07. D-07 now
selects local Windows virtualization; the [current checkpoint](research/full-live-specification-plan.md#current-execution-checkpoint) records the confirmed handoff and Root-only Session0→SessionA priority. Earlier guest/signedLive/copy/hardwarecode captures remain ASOF; the reported final authorized profile must be reconciled and actual capability/results retained. Windows activation/key is not required. Whole-application observations await the full guest/build/authorization/capture/copy record.


The user authorized the analyst-side [roadmap](research/native-decompilation-roadmap.md):
systematic main Live decompilation, browsable function exports, an accessible
method guide and evolving program-structure atlas, native behavior studies and
a first reviewed handoff. The [execution plan](research/native-phase-execution.md)
records actual progress and resource limits. Current implementation and
verification states remain unchanged. A [revision 2 proposal](research/native-decompilation-roadmap.md#revision-2-proposal--2026-10-17)
for restarting on the Linux workstation was adopted on 2026-10-17 and is executing.
On 2026-10-18 [ADR 0004](decisions/adr-0004-target-scope-t1.md) set the first completion
target, T1, and [roadmap revision 3](research/native-decompilation-roadmap.md#revision-3--t1-completion-plan-2026-10-18)
plans its gaps.

## Milestones

1. Record the reference build, artifact digests, environment, and package inventory.
2. Establish the whole-app feature matrix and explicit compatibility dimensions.
3. Derive bounded behavioral specifications from static evidence; resolve only
   material gaps with targeted reference probes under [ADR 0002](decisions/adr-0002-static-first-analysis.md).
   Whole-application observation is O-pending under [ADR 0006](decisions/adr-0006-reference-observation-reopened.md) until the selected local Windows guest profile is ready; static/extracted author and reviewer queues are parked behind the current Windows sitting priority. Unsupported required behavior stays unknown.
4. Release the first reviewed behavioral specification and fixture package.
5. Provision an isolated implementation workspace and build a candidate.
6. Compare reference and candidate; revise specifications and implementation
   through reviewed handoffs until the declared cases meet their criteria.
   Current comparison obligations follow immutable released expectations. Future releases may add O evidence after guest readiness and a reviewed observation packet; candidate work remains deferred.

The proposed first integrated scenario is two audio tracks, quantized clip
launching, recording into Arrangement, editing, save/reopen, and audio export.
It is a proposed milestone, not a requirement already validated against Live.

## Decisions still to make

- Compatibility targets and tolerances for behavior, audio, files, UI, and timing.
- Implementation platform and dependency/license choices.
- Priority and scope of devices, Warp, Max for Live, Push, and project interchange.
- Durable artifact storage and enforced analyst/implementer access boundaries.

Use [the routing table](../AGENTS.md) to choose the next task. Implementation-only
contexts proceed through the [handoff index](../handoff/index.md) and
[implementation index](implementation/index.md).


The [current checkpoint](research/full-live-specification-plan.md#current-execution-checkpoint) applies design12 to owner adoption and finishes the already-frozen metadata/Legacy reviews, then parks their no-X depth. A schema-aware census corrected the first amendment totals/order; its independently approved 691 X / 1,076 S / 3,857 none are heterogeneous inventories, with Analog199X qualified as predecessor context. Indirect resolution remains25,071baseline plus24conditional =25,095of268,015. Neither count establishes whole-product completion.


## Earlier research update snapshots — ASOF, superseded for scheduling

The update paragraphs below preserve their recorded adoption/selection/resource/ownership states. Current work is selected only by [Current phase](#current-phase) and the plan checkpoint; older Claude-hold/S-next language is historical.

An earlier design12 adoption snapshot recorded these owner updates: [Automation R6](research/automation-envelopes.md#automation-owner-r6-finite-adoption--2026-10-21), [Mixer R7](research/mixer-values.md#mixer-owner-r7-regular-node-annex-adoption--2026-10-21), [Analog R8](research/device-analog-dsp.md#analog-owner-r8-combined-host-annex-adoption--2026-10-21), [Electric R7](research/device-electric-dsp.md#electric-owner-r7-combined-host-and-midi-annex-adoption--2026-10-21), [Tension R8](research/device-tension-dsp.md#tension-owner-r8-midi-axis-annex-adoption--2026-10-21), [Playback R3](research/playback-core.md#playback-owner-r3-finite-adoption--2026-10-21) [Transport R6](research/transport-state-native.md#transport-owner-r6-finite-adoption--2026-10-21) and [Collision R3](research/device-collision-dsp.md#collision-owner-r3-finite-kind3-annex-adoption--2026-10-21). [MIDI-user R7](research/midi-user-mapping.md#midi-user-owner-r7-finite-annex-adoption--2026-10-21) is also adopted. [Mix R3](research/mix-graph.md#mix-owner-r3-finite-annex-adoption--2026-10-21) is also adopted. [LiveSet R3](research/live-set-structure.md#live-set-owner-r3-finite-crc-annex-adoption--2026-10-21) is also adopted. [Corpus R13](research/corpus-dsp-static.md#corpus-owner-r13-residual-midi-annex-adoption--2026-10-21) is also adopted. That snapshot added 7,733 finite draft case IDs and qualify unsupported report/input bridges; case counts are not whole-product coverage. Existing releases stay unchanged. Analog's [constructor-helper source review](research/device-analog-dsp.md#analog-constructor-helper-source-adoption--2026-10-21) is adopted. Its [whole receiver operand frontier](research/device-analog-dsp.md#analog-whole-receiver-native-adoption--2026-10-21) is adopted with carrier/runtime joins still open. [Electric's inner-word/dyld witness is adopted](research/device-electric-dsp.md#electric-inner-word-and-dyld-witness-adoption--2026-10-21), with runtime/R/D/public joins and argv/test qualifications open; [Tension's whole-helper/export cut is adopted](research/device-tension-dsp.md#tension-helperexport-frontier-adoption--2026-10-21), with B=P conditional and currenttable/P/O/D/I/probe/named/public joins unknown. [Analog's52-byte thunk/outer-word successor is adopted](research/device-analog-dsp.md#analog-thunk-and-outer-word-adoption--2026-10-21): localA=priorP/Q/B is conditional, [four construction helpers and the override-word nomination are also adopted](research/device-analog-dsp.md#analog-construction-helpers-and-override-word-adoption--2026-10-21), with V/J/Z/interior/callback/runtime/public joins open. Collision's twelve supplied state histories are adopted into R2; the [current queue](research/full-live-specification-plan.md#current-execution-checkpoint) owns their exact scopes. No new runtime model follows. Unsupported required behavior remains U/OPEN. Frozen route inventory remains691X/1,076S/3,857none (mixed units, Analog199X predecessor scope), and indirect resolution remains25,071baseline +24conditional =25,095of268,015.


[Electric's owned-stream analysis](research/device-electric-dsp.md#electric-encoded-site-association-adoption--2026-10-21) now establishes six positive encoded rebase-site associations. Two streams remain incomplete at declared arithmetic limits; runtime targets and required behavior remain U. Primary Apple dyld source research is selected before any revised method. This adds no case, grade, release or main-image site credit; frozen691 X/1,076 S/3,857 none and main25,071+24=25,095 of268,015 remain unchanged, bundle sites separate/product OPEN.


[Analog's whole initialization/override review](research/device-analog-dsp.md#analog-initialization-and-override-adoption--2026-10-21) supports one conditional local member assignment. Runtime/class/public joins remain unknown. The next selected static cut is134 data bytes; it adds no behavioral grade or whole-product closure.


The [primary Apple dyld source study](research/sources/apple-macho-format.md#primary-classic-dyld-implementation--2026-10-21) is approved as source/method evidence. A separately frozen Electric data-method revision is selected; applicability to Live's actual loader and all resulting runtime behavior remain unknown. Required coverage stays open.


[Analog's producer-word and guarded-table data](research/device-analog-dsp.md#analog-producer-word-and-guarded-table-adoption--2026-10-21) is approved: all126 guarded entries and a raw producer nomination, without runtime target or public behavior proof. The next step is retained function metadata, with required coverage still open.


[Electric's complete encoded-site method v2](research/device-electric-dsp.md#electric-complete-encoded-site-method-v2-adoption--2026-10-21), [Analog's whole producer nominee](research/device-analog-dsp.md#analog-whole-producer-nominee-adoption--2026-10-21) and [Tension's current dispatch](research/device-tension-dsp.md#tension-current-dispatch-adoption--2026-10-21) are approved within their stated static/data scopes. Diagnostic cursor and pair-count qualifications are retained. Their next bounded source/native reads remain analyst work; runtime/class/public behavior and required coverage stay U/OPEN. No behavioral cases, grades, releases or main-image site credit are added.


[Tension's complete50/58 wrapper pair](research/device-tension-dsp.md#tension-outer-rate-and-reset-nominees-adoption--2026-10-21) is approved, adding conditional operand positions rather than public behavior. Its40-byte inner-word cut and Analog's combined thunk/constructor nominee are in progress; Electric's six inner bodies have one independent reviewer. Runtime/class/public joins keep product coverage open.


[Electric's six inner bodies](research/device-electric-dsp.md#electric-whole-inner-six-adoption--2026-10-21) and [Tension's five raw word nominations](research/device-tension-dsp.md#tension-five-inner-word-nominations-adoption--2026-10-21) are approved, preserving reloaded-child and current-table uncertainty. Analog's combined constructor nominee is under independent review. These static findings add no behavior grade, released contract or main-image site; required product coverage stays open.


[Analog's combined producer constructor](research/device-analog-dsp.md#analog-producer-constructor-adoption--2026-10-21) is approved as conditional local carrier/store evidence. The [base-carrier helper](research/device-analog-dsp.md#analog-base-carrier-helper-adoption--2026-10-21) now supports their equality conditionally at normal return; allocation/class/current-vptr/public behavior remain unproved. Required coverage remains open.


[Electric's12-byte data study](research/device-electric-dsp.md#electric-producer-word-and-guarded-table-adoption--2026-10-21) is approved: four guarded entries and one raw producer nomination, without runtime/class/public behavior proof. Exact function metadata is next; required coverage remains open.


[Tension's whole inner-five review](research/device-tension-dsp.md#tension-whole-inner-five-adoption--2026-10-21) is approved, preserving saved/current child, cast and packed-payload distinctions. Electric's producer nomination reuses already-approved bodies without another capture. Further bounded helper/data work remains analyst-only; required coverage stays open, without new cases, grades, releases or main-image sites.

[Tension's guarded table/getter word](research/device-tension-dsp.md#tension-guarded-table-and-own78-word-adoption--2026-10-21) is approved as bounded static evidence. The raw getter nominee remains conditional, with saved/current receiver and public behavior gaps open. Parallel helper studies and their one-review assignments are maintained in the current plan; these studies add no behavioral cases or compatibility results.

[Analog's whole interior-state helper](research/device-analog-dsp.md#analog-interior-state-helper-adoption--2026-10-21) passed its sole independent review. Conditional return and direct stores narrow the local construction path; unread callees still prevent a whole-helper preservation or public behavior claim. Coverage remains open.

[Electric's three internal helpers](research/device-electric-dsp.md#electric-internal-initializers-adoption--2026-10-21) and [Tension's constant getter](research/device-tension-dsp.md#tension-own78-getter-body-adoption--2026-10-21) are approved within their static scopes. Current receiver/provider/public joins remain unknown. The next Tension selection assessment asks whether the existing unchanged harness can support the37 uncalibrated settings; it authorizes no execution or calibration result by itself.

[Analog's three stateful helpers](research/device-analog-dsp.md#analog-opaque-three-helpers-adoption--2026-10-21) remain approved with no currently admitted pure-function successor. [Tension's whole37 sensitivity and R4 annex](research/device-tension-dsp.md#tension-owner-r4-sensitivity-annex-adoption--2026-10-21) are now adopted:31 proposed-margin matches/six unresolved, no calibration/class or new IDs. [MIDI's whole relative-byte class](research/midi-transforms-native.md#midi-relative-byte-whole-class-adoption--2026-10-21) is approved at fixed UNIT state (1,006 fresh observations/18 inherited); [R7 owner is adopted](research/midi-user-mapping.md#midi-user-owner-r7-finite-annex-adoption--2026-10-21) with1,006new finite IDs and portable comparators NULL. The plan owns current assignments; no grade, release or whole-product closure follows.

The [Analog 128-value velocity catalog](research/device-analog-dsp.md#whole-velocity-byte-actual-adoption--2026-10-21) and [Corpus five-shape finite catalog](research/corpus-dsp-static.md#deterministic-free-lfo-continuation-adoption--2026-10-21) are independently approved. Their R4/R8 owner annexes are now adopted, adding 127/3 observation IDs with portable criteria NULL. Electric's complete 25-integer transpose class is sealed with 22 new captures and three inherited controls, under sole actual review. Analog's next full note-key class is selected: 127 fresh keys and inherited 60 at fixed velocity 100, without changing its recorded host model. These are bounded supplied-host observations with NULL portable comparators; required unknowns and whole-Live coverage remain OPEN. The [current checkpoint](research/full-live-specification-plan.md#current-execution-checkpoint) owns assignments and selection state.

[Electric's whole 25-integer transpose catalog](research/device-electric-dsp.md#whole-transpose-integer-actual-adoption--2026-10-21) is approved by its sole actual/source peer. Root adopts by citation and the next R4 finite annex is drafting. Current adopted ID total remains 5,124 until that owner review. Analog's complete note-key class and Tension's complete velocity-byte class are selected under their existing host models, with NULL portable criteria and no automatic successor.

[Analog's complete note-key actual catalog](research/device-analog-dsp.md#whole-note-key-actual-adoption--2026-10-21) is now approved by its sole peer; Root adopts by citation and the next R5 annex is selected from that summary. The channel class remains a separate selected packet. Current owner additions remain 5,124 until new owner review/adoption; exact output coincidences introduce no general pitch/channel law or portable criterion.

[Analog channel16](research/device-analog-dsp.md#whole-channel-nibble-actual-adoption--2026-10-21) and [Tension velocity128](research/device-tension-dsp.md#whole-velocity-byte-actual-adoption--2026-10-21) actual catalogs are independently approved. Tension retains an explicit missing pre-call parent-launch file pin and limited fsync scope; it does not pass full execution-provenance custody. Next owner annexes use approved summaries only, with portable comparators NULL. Current adopted additions remain 5,124 until those owner reviews/adoptions.

[Analog R5](research/device-analog-dsp.md#analog-owner-r5-note-key-annex-adoption--2026-10-21) is applied after its sole wording/ID/mapping/preservation review, adding 127 note-key observations and bringing cumulative added draft IDs to 5,251. The next channel annex authors on this base. Electric R4's sole owner peer is now Arrangement; reassignment preceded any Root proposal-payload read, so Root remains citation-only. Tension R5 remains drafting with its parent-launch custody qualification. Existing releases and required U / product OPEN are unchanged.

[Electric R4](research/device-electric-dsp.md#electric-owner-r4-transpose-annex-adoption--2026-10-21) and [Tension R5](research/device-tension-dsp.md#tension-owner-r5-velocity-annex-adoption--2026-10-21) are applied, adding 22/125 native-observation IDs. Cumulative added draft IDs are now 5,398, never passes or a product denominator. Tension retains its parent-launch custody gap; all portable comparators/grades stay NULL. Analog channel R6 drafts on R5; Electric key and Analog release-velocity captures are selected under existing models. Existing releases, main/bundle inventories and required U / product OPEN are unchanged.

[Analog R6](research/device-analog-dsp.md#analog-owner-r6-channel-annex-adoption--2026-10-21) is applied by its sole peer's review citation, adding fifteen channel observations; cumulative added draft IDs are 5,413. [Electric key128 actual](research/device-electric-dsp.md#whole-p1-note-key-actual-adoption--2026-10-21) is approved and its R5 annex authors from the summary. Analog release-velocity review and Tension key capture continue under existing models. Portable criteria/grades remain NULL; existing releases and required U / product OPEN are unchanged.

[AnalogR7](research/device-analog-dsp.md#analog-owner-r7-release-velocity-annex-adoption--2026-10-21) and [ElectricR5](research/device-electric-dsp.md#electric-owner-r5-note-key-annex-adoption--2026-10-21) are applied by sole owner-review citations;127new IDs each bring cumulativeadded draft IDs to5,667. [Tensionkeyactual](research/device-tension-dsp.md#whole-note-key-actual-adoption--2026-10-21) approves123fresh/fiveinherited for nextR6authoring. AnalogwholeTranspose25 is selected under the existing model, with Auto soleactualpeer and Rootcitation-only. Priors/portablecriteria/gradesNULL; no productcoverage denominator/pass/release/site or closure. RequiredU/productOPEN unchanged.

[Tension R6](research/device-tension-dsp.md#tension-owner-r6-note-key-annex-adoption--2026-10-21) is applied after the sole review of new wording/mapping/preservation. It adds123 key observation IDs; cumulative added draft IDs are5,790. Analog transpose and Electric velocity captures proceed under the recorded models with separate independent peers. Complete finite host-domain metadata assessments seek larger eligible sweeps without changing runtime authorization. Portable criteria/grades remain NULL and required U / whole-Live coverage OPEN.

[Analog transpose](research/device-analog-dsp.md#whole-transpose-actual-adoption--2026-10-21) and [Electric velocity](research/device-electric-dsp.md#whole-p1-velocity-actual-adoption--2026-10-21) actuals passed their sole reviews; next owners remain pending, so added draft IDs stay5,790. Complete native host-domain sweeps are now selected for Analog208, Tension106 and [Corpus57](research/corpus-dsp-static.md#whole-native-integer-domain-batch-selection--2026-10-21), using unchanged recorded models and historical references without replay. None establishes public behavior, calibration, a portable criterion or product closure. Required U / coverage OPEN.

[Tension whole host-domain actual](research/device-tension-dsp.md#whole-native-host-domain-actual-adoption--2026-10-21) passed sole independent review:106 fresh observations /11 historical references /164 aliases. Arrangement is drafting R7; no new IDs are credited yet, so cumulative added draft IDs stay5,790. Analog208 awaits sole review, Corpus57 authors, and ElectricR6 wording review is queued. All native/public/history qualifications remain; required U / whole-Live coverage OPEN.

[Electric R6](research/device-electric-dsp.md#electric-owner-r6-velocity-annex-adoption--2026-10-21) is applied by its sole owner-review citation, adding127 velocity observation IDs. Cumulative added draft IDs are5,917, never passes or a whole-product denominator. Its31-vector host-domain sweep is selected; Tension106 actual is approved for R7 authoring, Analog208 awaits review and Corpus57 awaits its qualified final packet/review. Native/public/history unknowns and NULL portable criteria persist; whole-Live coverage OPEN.

[Corpus57 actual](research/corpus-dsp-static.md#whole-native-integer-domain-actual-adoption--2026-10-21) passed sole review with a retained checker qualification: the original frozen checker fails its no-op control; a separately labeled post-capture data-only correction passes, with capture/input/raw bytes unchanged and no original retry. R9 authoring adds no IDs yet. TensionR7's sole owner peer is now Mix, before any Root proposal read, with one external wording erratum under review. Added draft IDs remain5,917; native/public/history/portable unknowns keep whole-Live coverage OPEN.

[Corrected Tension R7](research/device-tension-dsp.md#tension-owner-r7-native-host-annex-adoption--2026-10-21) is applied after Mix's sole review, preserving the original proposal plus its one-sentence external erratum. It adds106 native observation IDs, including an explicitly auxiliary boundary; cumulative added draft IDs6,023 are not application proofs or a product denominator. [Analog208 actual](research/device-analog-dsp.md#whole-kind3-native-host-actual-adoption--2026-10-21) is approved for the combined R8; Corpus R9 authors from its qualified57 summary, Electric31 waits sole review. All portable criteria/grades remain NULL and required U / whole-Live OPEN.

[Corrected Corpus R9](research/corpus-dsp-static.md#corpus-owner-r9-native-integer-annex-adoption--2026-10-21) and [combined Analog R8](research/device-analog-dsp.md#analog-owner-r8-combined-host-annex-adoption--2026-10-21) are applied after their sole owner reviews:57+232 new observation IDs, cumulative6,312 added draft IDs, never passes or a product denominator. [Electric31 actual](research/device-electric-dsp.md#whole-finite-host-domain-actual-adoption--2026-10-21) is approved; next Electric/Tension142-history MIDI batches are selected under unchanged models. Frozen691X/1,076S/3,857none and25,095of268,015 main indirect sites unchanged; unsupported required U/whole-Live OPEN, releases unchanged.

[Tension’s full MIDI-axis actual approval](research/device-tension-dsp.md#whole-midi-axis-actual-adoption--2026-10-21) admits142 fresh histories/one inherited baseline for R8 authoring; no extra IDs yet. [Corpus’s complete finite converted-host class](research/corpus-dsp-static.md#complete-finite-stored-host-domain-eligibility-and-selection--2026-10-21) selects201 missing inputs from277aliases/264vectors/63inherited references under the unchanged I1 model. Current added draft IDs6,312; ledger691X/1,076S/3,857none and25,095of268,015 main sites unchanged, not completion fractions. Required unsupported U / whole-Live OPEN, no release/calibration/candidate claim.

[Electric R7](research/device-electric-dsp.md#electric-owner-r7-combined-host-and-midi-annex-adoption--2026-10-21) and [Tension R8](research/device-tension-dsp.md#tension-owner-r8-midi-axis-annex-adoption--2026-10-21) are applied after their sole owner reviews,173+142 new observation IDs. Cumulative added draft IDs6,627, never passes or product denominator. Old criteria/releases and all broader U remain; Corpus201/Collision85 batches are selected under unchanged models. Ledger691X/1,076S/3,857none and25,095of268,015 main sites unchanged, no release/calibration/public/ARM/candidate or whole-product closure.

[Corpus’s complete finite stored-host actual approval](research/corpus-dsp-static.md#complete-finite-stored-host-actual-adoption--2026-10-21) admits201 new observations/63qualified inherited references across277aliases/264vectors. R10 authoring adds no IDs yet; current cumulative added draft IDs remain6,627. Collision’s selected85-input batch stopped with an unreviewed partial packet; no retry or continuation selected. Unsupported required U/whole-Live OPEN; ledger691X/1,076S/3,857none and25,095of268,015 main sites/releases unchanged.

[Corpus R10](research/corpus-dsp-static.md#corpus-owner-r10-complete-finite-host-annex-adoption--2026-10-21) is applied,201 new observation IDs; cumulative added draft IDs6,828, never passes or product denominator. [Collision partial approval/continuation](research/device-collision-dsp.md#native-kind3-partial-actual-adoption-and-unlaunched-continuation--2026-10-21) admits15 finite observations while preserving one guard failure/U semantics; ONLY69 previously unlaunched inputs are selected, no retry/guard revision. Corpus’s held-note268 class is selected separately. Ledger691X/1,076S/3,857none/main25,095of268,015/releases unchanged; required U/whole-Live OPEN.

[Corpus held-note268](research/corpus-dsp-static.md#held-note-midi-axis-actual-adoption--2026-10-21) and [Collision continuation69](research/device-collision-dsp.md#native-kind3-unlaunched-continuation-actual-adoption--2026-10-21) passed sole independent reviews. R11/R3 authoring adds no IDs yet; current cumulative added draft IDs6,828. Collision has84 approved observations/one failed-return U discovery/one historical-input-only baseline, not85success. Original history/NULLportablecriteria/publicARM/required U remain, whole-Live OPEN; ledger691X/1,076S/3,857none/main25,095of268,015/releases unchanged.

[CorpusR11](research/corpus-dsp-static.md#corpus-owner-r11-held-on-midi-annex-adoption--2026-10-21) and [CollisionR3](research/device-collision-dsp.md#collision-owner-r3-finite-kind3-annex-adoption--2026-10-21) applied aftersoleownerreviews,268+84newdraftIDs; cumulative7,180, notpasses/denominator. Collision84approved+failedguardU+input-onlybaseline, not85success. Originalcriteria/releases/history/U exact. [DCO032eligibility](research/corpus-dsp-static.md#dco032-pre-impulse-note-off-midi-axis-eligibility--2026-10-21) selects396missing underexistingmodel; no newcriterion/model/tool/calibration/publicARMlaw/grade/release/site. Ledger691X/1076S/3857none/main25095of268015 unchanged; requiredU/whole-LiveOPEN.

[CorpusDCO032396actual](research/corpus-dsp-static.md#dco032-whole-midi-axis-actual-adoption--2026-10-21) passedsoleRootreview; R12drafting addsnoIDsyet/current7,180. ResidualCorpus157 and Analog284 areselected underexistingmodels/soleactualreview; laterlargepackets reuse [existinganalyststore](research/native-analysis-recovery.md#existing-analyst-store-reuse-for-finite-batches--2026-10-21), no oldevidencemove/newsymlink/install/model. Electric284/Collision157/Tension284 remain metadataeligibilityonly. Ledger691X/1076S/3857none/main25095of268015/releases unchanged; NULLnewportablecriteria/grades/requiredU/whole-LiveOPEN.

[CorpusR12](research/corpus-dsp-static.md#corpus-owner-r12-two-event-midi-annex-adoption--2026-10-21) applies396newIDs/currentcumulative7,576, notpasses/denominator;12otherwhole/562oldIDs/22objects/criteriaU/releasesexact. [Tension284selection](research/device-tension-dsp.md#independent-note-and-channel-byte-batch-selected--2026-10-21) joinsCorpus157/Analog284 underexistingmodels/existinganalyststorewherebudgeted, RootcitationonlynewTensionactualbeforeanyread/Mixsolepeer; no newownerIDsyet. Ledger691X1076S3857none/main25095of268015/releases unchanged; requiredU/OPEN.

[Corpusresidual157actual](research/corpus-dsp-static.md#dco032-residual-midi-axis-actual-adoption--2026-10-21) passedsoleRootreview/full160aliases158histories/oneinheritedDCO032INPUTref; R13drafting addsnoIDsyet/current7,576. Recordedresourceguards untriggered, fullsource/data/protocol checks bounded/nativeonly; no oldcriteria/metric/calibration/generalMIDI/publicARMlaw transfer. Analog284/Tension284 selected viaexistingstore; Electric284/Collision157metadataonly. Ledger691X1076S3857none/main25095of268015/releasesunchanged/requiredU/OPEN.

[CorpusR13](research/corpus-dsp-static.md#corpus-owner-r13-residual-midi-annex-adoption--2026-10-21) applies157IDs/currentcumulative7,733, notpasses/denominator. Matching-keyCorpus127 isselected/queued; Electric284 and Collision157 join Analog284/Tension284 underexistingmodels/existinganalyststore/fullresourcebudgets/oneactualpeer. Rootcitationonlynewdeviceactuals beforeanyread; no baseline replay/newcriteria. Ledger691X1076S3857none/main25095of268015/releasesunchanged/requiredU/OPEN.

[Analog284](research/device-analog-dsp.md#independent-midi-byte-actual-adoption--2026-10-21) and [Tension284](research/device-tension-dsp.md#independent-midi-byte-actual-adoption--2026-10-21) passed their sole independent actual/source reviews. R9owner revisions are queued/drafting under separate new-wording/mapping/preservation reviews; Root citation-only newactual/proposalpayloads beforeanyread. QuietTension002003/commonAnalogcustody/rawNOFDfsync versusTensionperchild/FDfsyncrequests/oldsourceparentlimits retained. No IDsyet/current7,733/notpasses/denominator; ledger691X1076S3857none/main25095of268015/releases/requiredU/OPEN unchanged.

[Collision157actual](research/device-collision-dsp.md#independent-no-setter-midi-byte-actual-adoption--2026-10-21) passedsoleMixreview/full160aliases158histories/oneDCL054INPUTref. ArrR4author/Rootsolenewownerpeer; RootcitationonlyactualandoldR3proposalscope/approvedembeddedpreservation only. No IDsyet/current7,733, notpasses/denominator; oldkind3failure and unknownRet1/input-onlybaseline unchanged. Ledger691X1076S3857none/main25095of268015/releases/requiredU/OPEN unchanged.

[Tension R9](research/device-tension-dsp.md#tension-owner-r9-independent-midi-annex-adoption--2026-10-21) and [Collision R4](research/device-collision-dsp.md#collision-owner-r4-independent-midi-annex-adoption--2026-10-21) are applied after sole new-owner reviews, adding284+157 draft IDs. Current cumulative additions: **8,174**, not passes or a product denominator. [Corpus127 actual](research/corpus-dsp-static.md#dco032-matching-key-actual-adoption--2026-10-21) and [Electric284 actual](research/device-electric-dsp.md#independent-midi-byte-actual-adoption--2026-10-21) are sole-approved and enter R14/R8 drafting without a second actual review. Analog R9 remains pending. Exact scopes and limits are canonical in those pages; frozen691X/1076S/3857none, main25095of268015, releases and requiredU/productOPEN remain unchanged.

[Analog R9](research/device-analog-dsp.md#analog-owner-r9-independent-midi-annex-adoption--2026-10-21) is applied after Arr’s sole new-wording/mapping/preservation review, by exact embedded target citation only. It adds284 draft IDs, bringing cumulative additions to **8,458**, not passes or a product denominator. Corpus R14 and Electric R8 remain in drafting; Collision523 is selected under its existing model. Frozen691X1076S3857none/main25095of268015/releases/requiredU/productOPEN remain unchanged.

[Corpus R14](research/corpus-dsp-static.md#corpus-owner-r14-matching-key-annex-adoption--2026-10-21) and [Electric R8](research/device-electric-dsp.md#electric-owner-r8-independent-midi-annex-adoption--2026-10-21) are applied after sole new-wording/mapping/preservation reviews, adding127+284draftIDs. Cumulative additions: **8,869**, not passes or a product denominator. Collision523 remains selected/pending sole actual approval. All old criteria/releases/history stay preserved; frozen691X1076S3857none/main25095of268015/requiredU/productOPEN remain unchanged.

[Corpus Decay controller representatives](research/corpus-dsp-static.md#decay-controller-cell-standing-batch-selected--2026-10-21) select127fresh/full128cells/one DCO020 INPUT reference through the existing no-event I1 model. Arr authors one packet/Root solely reviews actual/source; no baseline replay or newnative/model/tool/calibration. The bounded [playback assessment](research/playback-core.md#post-adoption-standing-input-assessment--2026-10-21) leaves scalar boundary work eligible with exact matrix/setup still needed. Current8,869 added draft IDs/ledger691X1076S3857none/main25095of268015/releases/requiredU/productOPEN unchanged.

[Playback’s integer-semitone/rate matrix](research/playback-core.md#integer-semitone-and-retained-rate-class-selected--2026-10-21) selects582 fresh single-call histories through the existing three-binary64 scalar helper. The54 historical argument matches are not whole-history equivalences; all new result priors remain NULL. Mix authors after Collision523 seal/Auto solely reviews actual/source after Collision523 review; Root citation-only all new actual payloads. No new model/build/patch/provider/criterion/grade/IDs. Current8,869 draft additions/frozen691X1076S3857none/main25095of268015/releases/requiredU/productOPEN unchanged.

[Corpus Decay127](research/corpus-dsp-static.md#decay-controller-cell-actual-adoption--2026-10-21) and [Collision523](research/device-collision-dsp.md#dcl054-five-midi-axis-actual-adoption--2026-10-21) passed their sole actual/source reviews. R15/R5 drafting adds no IDs yet; cumulative8,869draft additions/notpasses/denominator unchanged. Root remains citation-only all new Collision actual payloads, with separate NEW owner review scoped to wording/mapping/preservation. Playback582 continues selected; ledger691X1076S3857none/main25095of268015/releases/requiredU/productOPEN unchanged.

[Corpus’s seven remaining resonator-control partitions](research/corpus-dsp-static.md#seven-resonator-control-classes-selected-together--2026-10-21) are selected together:890fresh/full896aliases891histories/one qualified INPUT reference6aliases. Auto authors after Playback582 review/Root solely reviews actual/source. Bipolar/inverted/unipolar input distinctions and Ratio baseline nonrepresentability remain; three A1 position controls excluded. Existing model/resource guards only/no new criteria or IDs. Current8,869draft additions/frozen691X1076S3857none/main25095of268015/releases/requiredU/productOPEN unchanged.

[Collision R5](research/device-collision-dsp.md#collision-owner-r5-five-axis-annex-adoption--2026-10-21) is applied after its sole new-owner review, adding523draftIDs/current cumulative **9,392**, not passes/denominator. [Playback582 actual](research/playback-core.md#integer-semitonerate-actual-adoption--2026-10-21) is sole-approved and enters R4 drafting;54oldargument matches are not whole-history equivalences or old-output transfer. Corpus R15 pending/Corpus890 selected; ledger691X1076S3857none/main25095of268015/releases/requiredU/productOPEN unchanged.

[Corpus R15](research/corpus-dsp-static.md#corpus-owner-r15-decay-annex-adoption--2026-10-21) is applied after its sole new-wording/mapping/preservation review, adding127draftIDs/current cumulative **9,519**, not passes/denominator. REQ007 finite observations preserve all other bodies, old criteria/history/releases and qualified INPUT-only baseline;003cell formula is no new quantizer law. Playback R4 pending/Corpus890 selected; ledger691X1076S3857none/main25095of268015/releases/requiredU/productOPEN unchanged.

[Analog’s converted virtual-enum class](research/device-analog-dsp.md#converted-virtual-enum193-standing-batch-selected--2026-10-21) selects193fresh/full198aliases194histories/one INPUT reference5aliases using the immutable v1+mandatory prose erratum. Exact amount values remain0.5; no dormancy/MPE/voice-capacity claim. Mix authors/Auto solely reviews actual-source/Root citation-only new actual payloads. Existing model/resource guards only/no criteria or IDs; current9,519draft additions/ledger691X1076S3857none/main25095of268015/releases/requiredU/productOPEN unchanged.


[Playback R4](research/playback-core.md#playback-owner-r4-integer-semitone-and-rate-annex-adoption--2026-10-21) is applied by exact sole-review target citation only:582new PBC-206–787 IDs/759PlaybacknavigationIDs/current cumulative **10,101**draft additions, not passes or a product denominator. Auto solely reviewed NEW wording/mapping/IDs/preservation before any Root proposal read; intendedRoot labels stay historical. Only017append/annex/revision;22otherwhole/old017R3prefix/177oldIDs68rows/R3scope/criteriaU/releases92 exact/fullreverse. NativeSAVEDXMM0 expectations/54ARG-onlysupports/no oldwholehistorytransfer; portablecriteria/gradesNULL/newappFalse/no formula/publicARM law. Prior numeric/status paragraphs retain their as-of adoption snapshots; [current checkpoint](research/full-live-specification-plan.md#current-execution-checkpoint) owns current queue. Analog193/Corpus890actual adoptions excluded from this metadata delta for Root's next routing. Frozen691X1076S3857none/main25071+24=25095of268015/releases/requiredU/productOPEN unchanged.

[Corpus890](research/corpus-dsp-static.md#seven-resonator-control-actual-adoption--2026-10-21) and [Analog193](research/device-analog-dsp.md#converted-virtual-enum-actual-adoption--2026-10-21) passed their sole actual/source reviews and enter the next owner revisions directly. R16/R10 wording/mapping/preservation remains separate; no IDs yet/current10,101draft additions/notpasses. Root citation-only Analog actuals and R10proposal; exacterratum/amount0.5 preserved/noquantizer/MPEcapacity law. Ledger691X1076S3857none/main25095of268015/releases/requiredU/productOPEN unchanged.

[Electric pickup256](research/device-electric-dsp.md#complete-pickup-cell256-standing-batch-selected--2026-10-21) selects the complete two128cell INPUT class/256fresh histories under the existing model. Mix author/Auto sole actual peer/Root citation-only all new actuals. Original0.5isnotn/127/no inherited history, no nativequantizer/within-cell law. Current10,101draftIDs/notpasses/frozen691X1076S3857none/main25095of268015/releases/requiredU/productOPEN unchanged.

[Tension stepped5349](research/device-tension-dsp.md#complete-stepped-control5349-standing-batch-selected--2026-10-21) selects the complete30-axis INPUT class/full5364aliases5350histories/one qualified baseline15aliases. Arr authors afterCorpusR16seal/Root sole actual-source peer under the existing model;4GiB+128MiB unreserved lifecycle/freshguard planning. No new IDs/criteria/current10,101draft additions/notpasses; ledger691X1076S3857none/main25095of268015/releases/requiredU/productOPEN unchanged.

[Corpus R16](research/corpus-dsp-static.md#corpus-owner-r16-seven-resonator-annex-adoption--2026-10-21) and [Analog R10](research/device-analog-dsp.md#analog-owner-r10-converted-virtual-enum-annex-adoption--2026-10-21) are applied after sole NEW wording/mapping/preservation reviews:890+193draftIDs/current cumulative **11,184**, not passes/denominator. Existing clauses/criteria/history/releases and qualified INPUT references remain exact; no actual proof redo. Rootcitation-only Analog actuals/R10proposal. Electric256/Tension5349 remain selected; ledger691X1076S3857none/main25095of268015/releases/requiredU/productOPEN unchanged.

[Corpus native-HOST position189](research/corpus-dsp-static.md#bounded-native-host-position189-class-selected--2026-10-21) selects64P-cell representatives per supplied host−1..1 axis,192aliases190histories189fresh/oneINPUTref3aliases. Stored/UI A1 remainsU/no128cell/physical/generalposition law; old890/R16exclusions retain scope. Auto author/Root sole actual-source peer; existingmodel/no IDs yet. Current11,184draft additions/notpasses/ledger691X1076S3857none/main25095of268015/releases/requiredU/productOPEN unchanged.

[Tensionpartial1388](research/device-tension-dsp.md#stepped-control-partial-actual-adoption--2026-10-21), [Corpus189](research/corpus-dsp-static.md#native-host-position189-actual-adoption--2026-10-21) and [Electric256](research/device-electric-dsp.md#pickup-controller256-actual-adoption--2026-10-21) passed their sole actual/source reviews for exactly those observations. Tensionfailed1/3960unlaunched remainU/no retry; Electric budget discrepancy retained. Separate NEWowner reviews pending/no newIDs/current11,184draft additions/notpasses. RootactualElectric/R17proposalCITEONLY; CorpusA1U. Ledger691X1076S3857none/main25095of268015/releases/requiredU/productOPEN unchanged.

[Tension R10](research/device-tension-dsp.md#tension-owner-r10-partial-stepped-annex-adoption--2026-10-21) addsONLY1388draftIDs/current cumulative **12,572**, not passes/denominator. Failed1/3960never-runU remainunnumbered/completefalse; all15oldREQ/criteria/history/releases exact. The [proposed return-recording design](research/full-live-specification-design.md#revision-13-proposal--opaque-return-recording-for-unattempted-tension-histories-2026-10-21) is NOTadopted, pending userdecision/no changedcollector or newcall authorized. Currentownerreviewscontinue/691X1076S3857none/main25095of268015/releases/requiredU/productOPEN unchanged.

[Electric R9](research/device-electric-dsp.md#electric-owner-r9-pickup-controller-annex-adoption--2026-10-21) and [Corpus R17](research/corpus-dsp-static.md#corpus-owner-r17-native-host-position-annex-adoption--2026-10-21) are applied after sole new-owner reviews, adding256+189 draft IDs; cumulative additions **13,017**, not passes or a product denominator. Prior clauses, objects, criteria, history and releases remain exact. [Analog’s five protocol comparisons](research/device-analog-dsp.md#secondary-protocol-device-harness-source-bounds--2026-10-21) are assigned under the unchanged standing model; actual success remains unreviewed. Tension design13 is still proposed only/pending user decision. Frozen691X/1076S/3857none, main25095of268015, releases36/19/17 and requiredU/productOPEN remain unchanged.

[Corpus’s internal controller neighborhoods](research/corpus-dsp-static.md#internal-controller-boundary-neighborhoods-selected--2026-10-21) select3586 missing histories from1197 rational transitions/3591aliases3587histories/one qualified INPUT reference5aliases, under the unchanged no-event I1 model. Mix authors and Root solely reviews actual/source after freeze. Inputs are not native boundary/within-cell/public-ARM proof. No newIDs: cumulative13,017draft additions/notpasses; ledger691X1076S3857none/main25095of268015/releases/requiredU/productOPEN unchanged. Analog5 actuals await sole review; Tension design13 remains proposed/userpending.

[Analog’s five protocol observations](research/device-analog-dsp.md#secondary-protocol-five-actual-adoption--2026-10-21) passed sole actual/source review and enter R11 drafting; no new IDs yet/current13,017draft additions. Full6histories7aliases/baselineINPUTonly; no old-output comparison or general rate/block law. Root remains citation-only actuals and ALLnewR11proposals; Auto authors/Arrangement solely reviews new owner wording/mapping/preservation. Corpus3586 selected; Tensiondesign13 pending. Ledger691X1076S3857none/main25095of268015/releases/requiredU/productOPEN unchanged.

[Electric’s retained124-history polyphony comparison](research/device-electric-dsp.md#whole-retained-polyphony-load-comparison-selected--2026-10-21) is selected as a whole: p0–30/two loads/full+omit-first/62same-end pairs. Auto authors/Arrangement solely reviews actual-source; Root citation-only. It is historically declared, with new retained captures and explicit old per-history bridge limits, not a never-run or general capacity claim. No newIDs/current13,017draft additions/notpasses. AnalogR11pending/Corpus3586selected/Tensiondesign13pending; ledger691X1076S3857none/main25095of268015/releases/requiredU/productOPEN unchanged.

[Analog R11](research/device-analog-dsp.md#analog-owner-r11-secondary-protocol-annex-adoption--2026-10-21) is applied by exact sole-review target citation, adding five draft IDs; cumulative additions **13,022**, not passes or a product denominator. All prior whole clauses, objects, criteria, error history, MPE erratum and releases remain exact; no rate/block invariance law. Electric124/Corpus3586 actual work continues; Tension design13 remains proposed/userpending. Ledger691X1076S3857none/main25095of268015/releases36/19/17/requiredU/productOPEN unchanged.

[Playback’s retained unwarped-rate class](research/playback-core.md#shipped-unwarped-file-rate-class-selected--2026-10-21) selects four missing histories in the complete ten-pair INPUT set, with six qualified INPUT-only references. Auto authors/Mix solely reviews actual-source; Root citation-only. The zero-only source inventory and UserFloat metadata establish no complete fine-pitch domain or public clip admission. No IDs/current13,022draft additions/notpasses; other selected work and Tensiondesign13pending/ledger691X1076S3857none/main25095of268015/releases/requiredU/productOPEN unchanged.

[Collision’s complete Mallet controller class](research/device-collision-dsp.md#complete-mallet-controller-input-class-selected--2026-10-21) selects 256 missing histories across two declared 128-step controls. Auto authors and Arrangement solely reviews actual/source; Root is citation-only. Old kind3 failure, input-only baseline, criteria and broader unknowns stay unchanged. No new IDs: current13,022 draft additions, not passes. Other selected batches continue; Tension design13 remains pending. Ledger691X1076S3857none/main25095of268015/releases/requiredU/productOPEN unchanged.

[Electric’s124 retained polyphony histories](research/device-electric-dsp.md#retained-polyphony-comparison-actual-adoption--2026-10-21) passed their sole actual/source review and enter R10 drafting. Pair differences supply no capacity or stealing law, portable criterion or old-history repair. Root remains actual citation-only; the new owner review covers wording/mapping/preservation. No IDs yet: current13,022draft additions/notpasses. Other selected work continues; Tensiondesign13 remains pending. Ledger691X1076S3857none/main25095of268015/releases/requiredU/productOPEN unchanged.

[ElectricR10](research/device-electric-dsp.md#electric-owner-r10-load-and-omission-annex-adoption--2026-10-21) is applied after sole new-owner review, adding124 draft IDs/current **13,146**, not passes. [Tension’s separate protocol class](research/device-tension-dsp.md#declared-rate-and-block-protocol-class-selected--2026-10-21) selects five gaps under the original guard; design13 remains pending for3960 only. [Collision’s partial packet](research/device-collision-dsp.md#mallet-controller-partial-packet-awaiting-sole-review--2026-10-21) awaits sole review/failed1+131unlaunchedU/no continuation. Earlier clauses/criteria/history/releases and ledger691X1076S3857none/main25095of268015/requiredU/productOPEN unchanged.

[Analog’s whole14 INPUT selection](research/device-analog-dsp.md#declared-multi-note-fourteen-history-class-selected--2026-10-21) precedes [Tension’s four never-launched protocol histories](research/device-tension-dsp.md#four-never-launched-protocol-histories-selected--2026-10-21). The latter corrects future initializer DATA from already approved model metadata while keeping ret0/flag01/allotherguards; failed64U/no retry and pendingdesign13for3960 remain separate. Sole-approved [Playback4](research/playback-core.md#shipped-unwarped-rate-actual-adoption--2026-10-21), [Collision124partial](research/device-collision-dsp.md#mallet-controller-partial-actual-adoption--2026-10-21) and [Tensionpartial](research/device-tension-dsp.md#rate-and-block-protocol-partial-actual-adoption--2026-10-21) enter canonical research without proof replay. Owner revisions pending/current13,146draftIDs/notpasses; ledger691X1076S3857none/main25095of268015/releases36/19/17/requiredU/productOPEN unchanged.

[CollisionR6](research/device-collision-dsp.md#collision-owner-r6-partial-mallet-annex-adoption--2026-10-21) and [PlaybackR5](research/playback-core.md#playback-owner-r5-shipped-rate-annex-adoption--2026-10-21) apply128new draft IDs/current **13,274**, not passes. [Corpus3586actual](research/corpus-dsp-static.md#internal-boundary-neighborhood-actual-adoption--2026-10-21) is solely approved/R18ArrangementauthorAutoNEWownerpeer/RootproposalCITEONLY; no second actual review/nativequantizerlaw/IDs yet. WholeAnalog14andfournever-launchedTension remain selected with originalguards/correctfutureinitializerDATAonly; failedU/no retry/pending3960design13 unchanged. Ledger691X1076S3857none/main25095of268015/releases36/19/17/requiredU/productOPEN remain.

Next finite unchanged-model selections: [Electric7](research/device-electric-dsp.md#seven-history-rate-and-block-protocol-class-selected--2026-10-21) then [Corpus13](research/corpus-dsp-static.md#declared-thirteen-history-rate-and-block-protocol-class-selected--2026-10-21), afterTension4. Analog14authorpartial4recorded/failed1U9unlaunchedawaitssolepeer; no retry/guardchange. Current13,274draftIDs/notpasses/ledger691X1076S3857none/main25095of268015/releases36/19/17/requiredU/productOPEN unchanged.

[Analogpartialsoleadoption](research/device-analog-dsp.md#declared-multi-note-partial-actual-adoption--2026-10-21) admitsfourp00–03; failedp04U9unlaunchedU/noactualreleasecontrolcomparison/R12drafting. [WholeStiffness128selection](research/device-collision-dsp.md#whole-never-launched-stiffness-class-selected--2026-10-21) followsCorpus13 underunchangedguards/model; oldfailedVolume+threeVolume-tailU untouched. Current13,274draftIDs/notpasses/ledger691X1076S3857none/main25095of268015/releases36/19/17/requiredU/productOPEN unchanged.

[CorpusR18adopted](research/corpus-dsp-static.md#corpus-owner-r18-controller-boundary-annex-adoption--2026-10-21) adds3586draftIDs/current **16,860**, not passes. Sole-approved [Tension4](research/device-tension-dsp.md#four-never-launched-protocol-actual-adoption--2026-10-21) and [Electric7](research/device-electric-dsp.md#seven-history-protocol-actual-adoption--2026-10-21) awaitowneradoption/no proofredo; failedU/no retry/pending3960design13/ledger691X1076S3857none/main25095of268015/releases36/19/17/requiredU/productOPEN unchanged.

## Device owner adoption and next standing packet — 2026-10-22

The [current checkpoint](research/full-live-specification-plan.md#current-execution-checkpoint) records Analog R12 (+4), Tension R11 (+4), Electric R11 (+7), Corpus R19 (+13) and Collision R7 (+128): **156 new draft IDs; 17,016 cumulative additions**. Each owner preserves earlier whole requirements, objects, unknown criteria/history and immutable releases. Sole actual approvals were adopted without another source/raw/numeric proof review; the owner peers reviewed new wording, mapping, IDs and preservation only. No new grade or release is claimed.

[Analog's complete four-history release/control class](research/device-analog-dsp.md#whole-four-history-releasecontrol-class-selected--2026-10-22) is selected with unchanged guards. [Tension's approved execution steps](research/full-live-specification-plan.md#execution-steps--exact-3960-unlaunched-tension-histories-2026-10-22) retain the full4GiB+128MiB storage floor; fresh capacity now admits selection, with every parent/child resource guard retained. The [Playback86 INPUT assessment](research/playback-core.md#remaining-scalar-input-class-assessment--2026-10-21) supplies no additional justified whole-history class in its bounded inventory.

The frozen pre-O census remains691X/1076S/3857none; the revision5 route interpretation is691X/1076S/3857O-pending/0none, with zero observed O. These heterogeneous inventories are not a coverage denominator. D-07 is unrecorded; no O host/tool provisioning or execution is selected. Main indirect25095of268015, releases36/19current/17superseded, required unsupported U and whole-product OPEN remain unchanged.

## Analog R13 adopted; five-count remainder selected — 2026-10-22

[Four-control actual and R13 adoption](research/device-analog-dsp.md#four-releasecontrol-actual-and-r13-owner-adoption--2026-10-22) adds four draft IDs, bringing cumulative additions to **17,020**. The two pair differences are descriptive raw bytes/hashes only; earlier whole requirements, objects, criteria/U/history and releases remain exact. [All five unattempted count histories](research/device-analog-dsp.md#whole-five-count-unlaunched-remainder-selected--2026-10-22) are selected with unchanged Analog ret0/flag01; no failed p04/acceptedcount/releasefour replay or Tension-only return-policy transfer. Auto authors; Arrangement solely reviews actual/source; Root citation-only. Tension's independently selected3960packet continues under adopted13/allotherguards. No new grade/release/coverage denominator; requiredU/productOPEN/D07unrecorded/Oinert remain.

## D-07 local Windows guest selected; observations pending — 2026-10-22

The [user's D-07 choice](decisions/adr-0006-reference-observation-reopened.md#windows-guest-profile-selected--2026-10-22) selects a local Windows VM; they will provide the authorized Live12.4.3 installer and can run the required sudo step. Bounded setup is selected, without a guest boot or observed Live result. Exact guest/license/build/installer hashes, usable acceleration, isolation and evidence copy remain open. Package/provider mutations wait for active X captures/source-window checks. Windows/VM evidence is a separate profile; pinned macOS/arm64 equivalence is not assumed. The3857conditional O units remain pending/U/zeroobserved, and whole-product coverage remains OPEN. Earlier unrecorded-host statements are as-of history.

## Analog count partial and Windows preparation — 2026-10-22

The [sole-reviewed Analog count partial](research/device-analog-dsp.md#five-count-remainder-partial-actual-adoption--2026-10-22) records0accepted/p05guardFAIL/fourunattemptedU, no retry/newIDs/guardchange. Current17020draft additions andR13remain unchanged. Tension3960 is still active under its separately approved opaque-return policy. [Windows Session0+A inputs](research/phase4-probe-batch.md#windows-first-sitting-input-packet-prepared--2026-10-22) are prepared21INPUT/zeroobservations; first authoring failure was retained and plain-XML envelope corrected in a new packet. D07selects localWindows11Pro; package downloads are verified, KVM reboot deferred by user, guest/build/installer/license/graphics/copy readiness open. No guest boot/Ograde/coverage closure.

## Local Windows VM preparation retained — 2026-10-22

The [VM/transfer preparation](research/full-live-specification-plan.md#prepared-transfer-media-and-current-stop-points--2026-10-22) records private QEMU tool checks, the sparse guest disk/private firmware state and read-only21INPUT/separate empty export images. No global package/provider/cache mutation, guest boot or observed Live result occurred. Microsoft's ISO request returnedHTTP403; user media and their later KVM reboot remain needed. Host choice is decided; guest/build/license/Liveinstaller/graphics/copy readiness is open. Tension3960 capture is sealed and under its sole actual/source review, with no owner IDs credited before approval; current draft additions remain17020/requiredU/productOPEN.

## Tension3960 sole actual approval — 2026-10-22

[All3960 new suffix observations](research/device-tension-dsp.md#exact-3960-opaque-return-actual-adoption--2026-10-22) are approved by the sole actual/source reviewer, under user-adopted opaque-return recording with every other guard unchanged. Quiet13/nonzero3947/889hashes and literal0/1 return projections remain descriptive, without a general domain/ABI/meaning/criterion. Old5350as-of dispositions/failedU1389/INPUTbaseline/accepted histories remain exact and unreplayed. Mix authors R12; Arrangement solely reviews NEW wording/IDs/mapping/preservation; Root applies by citation only. Current17020draft additions stay unchanged until owner adoption. No new grade/release/Oresult/product closure.

## Tension R12 adopted — 2026-10-22

[Tension R12](research/device-tension-dsp.md#tension-owner-r12-opaque-suffix-annex-adoption--2026-10-22) adds3960finite observation IDs, bringing cumulative draft additions to **20,980**. All15whole requirements/old42rows/objects/criteriaU/history/releases/full5350OLD-ASOF5364aliases remain exact.13quiet/3947nonzero/889hashes and signed64 return projections stay descriptive, not a domain/ABI/meaning/calibration/publicARM law. Root applied the sole owner's embedded approved target/delta by citation without proposal payload or actual proof rereview; no new release/grade or product closure. [The selected static locator cut](research/device-analog-dsp.md#selected-float-unit-constructor-locator-cut--2026-10-22) continues toward the unresolved parameter-emission join. VM setup is staged; user media and reboot will come later. RequiredU/whole-LiveOPEN/zeroobservedO remain.

## Immediate-caller native adoption and CalcA scalar selection — 2026-10-22

The [sole-reviewed Automation caller contract](research/automation-envelopes.md#immediate-m-caller-native-contract-adopted--2026-10-22) narrows local delivery/branch premises across3,009selected bytes without a new case, grade or public/cross-slice law. [CalcA's complete33byte scalar union](research/device-analog-dsp.md#whole-calca-direct-scalar-union-added-before-review--2026-10-22) joins its metadata+784B native packet before the sole final review; GOT/pointees, zero-fill and strings remain excluded. Current20,980draft additions, releases36/19current/17superseded, main25095of268015, zeroobservedO and requiredU/productOPEN remain. User will supply the Windows ISO/authorized Live installer after their deferred reboot; VM readiness remains open. The [current checkpoint](research/full-live-specification-plan.md#current-execution-checkpoint) owns selection; earlier dated selection snapshots are historical.

## Executed-x86 CalcA static adoption — 2026-10-22

The [sole-approved combined study](research/device-analog-dsp.md#executed-x86-calca-metadatanativescalar-adoption--2026-10-22) narrows conditional local register/pointer delivery across4041selected content bytes. Formal return ABI/meaning/benignness, old failure cause, current runtime/public/ARM behavior and all-exits proof remain unknown. Strictguards/failedandunattemptedU/currentR13 unchanged; no new IDs, grade, release or site. Whole-product coverage stays OPEN. The [selected host-processing cohort](research/device-host-protocol.md#whole-three-method-host-native-cohort-selected--2026-10-22) continues independently; no automatic CalcA dependency or capture follow-up.


[Analog expanded native study](research/device-analog-dsp.md#expanded49-native-study-adopted-local-chains-and-complete-frontier--2026-10-23) is adopted as conditional local-chain evidence, including one selected two-body receiver-return clarification. Runtime/class/public behavior and required coverage remain open. The [atlas](research/program-structure.md#analog-factory-dependency-chain-progress--2026-10-23) routes to the next complete dependency metadata cohort; no behavioral cases, grades, releases or main-image site credit are added. Claude retains guest-operation ownership.


[Complete Analog locator metadata](research/device-analog-dsp.md#complete64-locator-metadata-adopted-66-declarations-and-qualified-hint--2026-10-23) is adopted; the next complete native cohort is selected with gap/current-binding limits. [Session0 capability-method sources](research/phase4-probe-batch.md#session0-capability-methods-primary-source-followup-adopted--2026-10-23) qualify future CPU/audio/video/MIDI checks without measuring readiness or changing Claude guest ownership. Current behavioral-case/release/indirect-site totals and whole-product OPEN status are unchanged.


[Owned Session0 calibration inputs](research/phase4-probe-batch.md#owned-audio-and-midi-calibration-inputs-adopted--2026-10-23) are prepared and reviewed for future route checks. They establish file bytes only; guest acceptance/audio/capture/MIDI delivery remain unmeasured. No guest/profile/media/tool action or coverage grade follows, and Claude retains guest ownership.


[Complete66native findings](research/device-analog-dsp.md#complete66-native-study-adopted-27-qualified-groups-and-cache-history--2026-10-23) are adopted with qualified local return/output/record paths, a retained failed peer cache inspection and runtime/public unknowns. A combined metadata/known-dispatch successor is selected under one sole review. This adds no behavioral case, release or resolved-site credit; guest ownership and whole-Live OPEN status remain unchanged.


The [current checkpoint](research/full-live-specification-plan.md#current-execution-checkpoint) now records the combined Analog frontier/dispatch adoption and next complete67 native selection. Official Windows tool archives and a new unattached calibration/tool image have host-side approval; installed versions, signatures and guest capabilities remain unknown. Claude retains exclusive guest operations pending its completion report; reviewed O remains zero and whole-product coverage remains open.


The [21prepared SessionA inputs now have sole independent INPUT/code approval](research/phase4-probe-batch.md#sessiona-prepared-input-sole-review-adopted--2026-10-23). Their source/edit preservation is established for the exact packet; actual guest acceptance and Live outcomes remain unknown, with guest operations still held.


The [current plan checkpoint](research/full-live-specification-plan.md#current-execution-checkpoint) now records sole-reviewed Analog67 findings and the next combined59 static cohort, plus qualified Windows MIDI source/callback methods. These advance bounded analysis and observation preparation; actual targets/public behavior and guest capabilities remain unknown, with no new case/site/O/release credit or whole-product completion.


[The static-route scope assessment](research/full-live-coverage-inventory.md#frozen-s-route-scope-assessment-and-new-metadata-questions--2026-10-23) now accounts for the full1076S inventory, preserving all counts and unknowns. New bounded metadata questions can proceed independently while Analog’s whole59cohort waits for capacity; guest operations remain held for Claude. These planning conclusions add no public-behavior or compatibility credit.


The [currentcheckpoint](research/full-live-specification-plan.md#current-execution-checkpoint) records sole-approved Automation/AClipmetadata and their next complete native questions, preserving prior failed/classifier histories and all runtime/public gaps. Planning and declarations add no case/grade/O/release credit; whole-Live coverage remainsopen, Analog59awaitscapacity and guest operations remainwithClaude.


[Latest analyst checkpoint](research/full-live-specification-plan.md#current-execution-checkpoint):AClipwholehook conditional static findings adopted; Automationnativev2unreviewedpartial and MNSpre-acquisition preparation retained without coverage credit. [Shared root/store is capacity-held](research/native-analysis-recovery.md#shared-filesystem-capacity-stop--2026-10-23), so all new captures/diagnostics/checker-seals wait for space under unchanged full contracts. Claude exclusively owns guestoperations pending completion report; Root makes no VM change. Whole-Live coverage remainsopen.


[Currentanalystwork](research/full-live-specification-plan.md#current-execution-checkpoint) now includes adoptedAutomationv2truthfulpartial and MNSfour-variantmetadata, resumedwholeAnalog59authoring and explicitly selectedwholeClipdependency/raw32Bfield cohort. These partialstatic records preservepublic/runtimeunknowns and addno behavioralcase/site/O/releasecredit. Claudeexclusiveguesthold persists; wholeLiveOPEN.


[Lateststaticcheckpoint](research/full-live-specification-plan.md#current-execution-checkpoint) adopts Analog59, AutoV3retainedrecovery/semantics, Clipfrontier32B and MNS4native through their solepeers. All public/FP/currentprovider/runtime joins and proceduralqualifications remainexplicit. [Boundedsharingreconciliation](research/program-structure.md#cross-cohort-static-reference-reconciliation--2026-10-23) prevents duplicate Sourcebyte reads. No behaviorcase/grade/site/O/release/closure gain isclaimed; Claudeexclusiveguesthold unchanged.


## Current Windows sitting route — 2026-10-23

[The confirmed handoff and current priority](decisions/adr-0006-reference-observation-reopened.md#confirmed-handoff-and-windows-sitting-priority-supersede-static-queues--2026-10-23) supersede the preceding ASOF update snapshots: Root alone controls the offline/no-NIC guest for Session0 then SessionA; source-only workers provide host support/docs and static author/peer queues remain parked. Reported authorized Live/Windows/audio must be reconciled; current capability/results remain UNVERIFIED, reviewedO0 and wholeLiveOPEN. No new source proof, guest result, case/grade/site/release or automatic static continuation follows from this route.


[Plan revision6](research/full-live-specification-plan.md#revision-6--paired-observation-and-static-analysis-2026-10-23), amended by user direction, now runs Session0/SessionA with three concurrent O/S/X workers on the same four areas. Tension_owner alone drives the offline guest; tension_review performs static analysis and o137 extracted execution on the host. Root coordinates. Results keep separate routes and reviews; the earlier prohibition on parallel relevant static work is superseded. The first actual SessionA case is underway; reviewedO remains0 and whole-Live coverage remainsopen.
