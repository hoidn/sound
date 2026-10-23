---
id: RESEARCH-NATIVE-MIDI-EFFECTS
type: research
status: current
updated: 2026-10-19
access: analysis
revision: 3
target: Ableton Live 12 Suite 12.4.3
---

# Native MIDI effects evidence

This page supports the canonical [native MIDI effects draft](../specs/native-midi-effects.md)
for Arpeggiator, CC Control, Chord, Note Length, Pitch, Random, Scale and Velocity.
It is an F-06 partial packet under the [full coverage design](full-live-specification-design.md).
These effects process live MIDI; the [MIDI editor/tools page](midi-editing-tools.md)
owns clip rewriting, and [user mapping](midi-user-mapping.md) owns controller
mapping. No observed audio or runtime behavior is claimed here.

## Source identities and retention

Packet root:
[full-spec-v1/native-midi-effects](../../analysis/ableton-live-12.4.3/full-spec-v1/native-midi-effects/).

| Source ID | Exact source and locator | Observed scope and limit |
| --- | --- | --- |
| SRC-NATIVE-MIDI-MANUAL-20261019 | [Official current Live 12 chapter](https://www.ableton.com/en/live-manual/12/live-midi-effect-reference/); [HTML](../../analysis/ableton-live-12.4.3/full-spec-v1/native-midi-effects/manual-12-midi-effects-2026-10-19.html), capture 2026-10-19; 265,958 bytes; SHA-256 `33739cb549d6577624acd91466dafeafe8faaeea03044ac358043233015603a9` | Eight named sections, retained numbered text0003–0142; current Version12, no 12.4.3 publication pin. Text describes behavior (D12); exact build U. Images not inspected |
| SRC-NATIVE-MIDI-SCHEMA-12402 | Retained [schema excerpts](../../analysis/ableton-live-12.4.3/full-spec-v1/native-midi-effects/schema-excerpts.json); parent [12.0_12402.txt](../../analysis/ableton-live-12.4.3/full-spec-v1/inventory/12.0_12402.txt), SHA-256 `b7c9d4c767d8ca9b346ce7d517265446bbacd6de366cc058e155613789d0f299` | Eight exact class blocks with original line numbers; stored vocabulary, not load acceptance, defaults, limits or DSP |
| SRC-NATIVE-MIDI-PRESETS-1243 | Seven retained compressed `.adv` files and decompressed `.xml`; [source paths and hashes](../../analysis/ableton-live-12.4.3/full-spec-v1/native-midi-effects/shipped-presets.json); [literal observations](../../analysis/ableton-live-12.4.3/full-spec-v1/native-midi-effects/preset-observations.json) | Product-shipped historical presets declare Creator 12.4d1/MinorVersion 12.0_12402, not freshly saved 12.4.3 state. No CC Control example in inventory. No preset executed |
| SRC-NATIVE-MIDI-ALIASES-ARM64 | Existing arm64 [retained selected symbol rows](../../analysis/ableton-live-12.4.3/full-spec-v1/native-midi-effects/native-presence.json), external source `/var/tmp/sound-analysis/corpus/indexes/aliases.jsonl`; source and line SHA-256 inside packet | At most three Reset/Exit/OnOn aliases per processor; 15 rows. Presence establishes bounded follow-up anchors only; no function body/call graph/runtime law |

[Source metadata](../../analysis/ableton-live-12.4.3/full-spec-v1/native-midi-effects/source.json)
retains the manual URL/date/hash/heading anchors. The [inventory](full-live-coverage-inventory.md)
pins installed product identity and original preset choices. The extractor reads
those retained inventory records, verifies the seven source digests, copies their
original bytes, decompresses XML as data and reads only eight schema blocks.
No original code, bytecode, patch or host was executed; no tooling was installed.

## Observations and implications

The following are **Observed stored fields**, not behavior deductions. Full
original declarations and source line bounds are in the schema packet.

| Device / schema lines | Exact stored surface | Supported implication and boundary |
| --- | --- | --- |
| Arpeggiator 4208–4259 | Mode, PatternOffset, RepeatCount, SyncState, SyncedRate, FreeRate, Gate, Retrigger, Hold, transposition and velocity fields; four compatibility-mode Booleans | Rate/hold/retrigger surfaces corroborated. Compatibility flags make inferred modern behavior for older presets especially unsafe; no flag meaning inferred |
| CC Control 4284–4348 | ModWheel, PitchBend, Pressure, CustomBoolName/Target/Value; 12 indexed custom names, targets and values | Event families/custom controls have storage. No CC wire-range, Send or Learn ordering established |
| Chord 4349–4405 | Six shifts, separate degree shifts, velocities and chances; Strum/Tension/Crescendo; duplicate-strum and per-note-event flags | Current manual's additional Chord controls have installed schema counterparts; no strum schedule or probability distribution established |
| Note Length 4862–4893 | Mode, Latch, SyncState, SyncedLength, TimeLength, Gate, Balance, DecayTime, DecayKeyScale | Latch/dynamic controls present. No mode enum decoding or note-off matching proven |
| Pitch 4901–4939 | Pitch, PitchScaleDegrees, Lowest, Range, RangeMode, UseCurrentScale, StepWidth and mapping keys | Degree/range/step surfaces present. No range inclusion, Fold law or overflow handling proven |
| Random 4940–4968 | Chance, Choices, Scale, Sign, Alternate, UseCurrentScale | Stored field named Scale is not independently proven to encode current Interval labels/range; cycle math remains unsupported |
| Scale 4973–5020 | Base, InternalScale, Transpose, Fold, Lowest, Range, Mapping.0..11 | Twelve mappings stored despite manual's13×13 display description. No extra13th pitch class inferred |
| Velocity 5107–5138 | Drive, Compand, Random, Mode, Operation, MaxOut, MinOut, Range, Lowest | Control surfaces present; neither mode codes nor curve arithmetic established |

Examples of literal values: `Pitch/+12.adv` stores Pitch 12, Lowest 0, Range 127;
`Scale/8-Tone Spanish.adv` stores Range 128 and 12 mapping fields; Note Length's
`16th Notes.adv` stores SyncedLength 5, TimeLength 10000, Gate 100. These do **not**
prove common Range units, a UI division decoder or the active setting behind a
preset name. `Arpeggiator/Bach 16th.adv` stores PatternOffset −1 and RepeatCount 0;
no “−1 means first” or “0 means infinite” law is asserted. The Chord sample has
multiple zero shifts: these do not prove which zero-shift slots are enabled.
The preset case is only byte-level corroboration of parameters, not a behavioral
acceptance oracle.

The retained native names include Arpeggiator Reset/Exit/OnOn, NoteLength
Reset/Exit/OnOn, Random Reset/OnOn and analogous activation hooks. These name
anchors make bypass/reset questions concrete but do not settle held-note output,
random reseeding or the user's actions that reach a reset. No native-law S grade
is justified from this packet.

## Documentary contracts and unresolved readings

The draft assigns 27 stable requirements and 146 concrete cases: 54 documentary
partial predicates and 92 U cases. Every case is unexecuted and all 146 exact-build
grades are U. Cases001–066 cover device behavior; the 80 `-L01`..`-L10` cases
individually cover automation, pitch/overlap boundary, malformed input,
cancellation, undo, bypass, reset/transport, save/reopen, teardown and non-note
forwarding for every device. [Counts](../../analysis/ableton-live-12.4.3/full-spec-v1/native-midi-effects/case-counts.json)
separate positive 75, boundary 24, cancellation 9, negative 13, teardown 9,
malformed 8 and undo 8. Counts are authored scenario counts, never executed results
or evidence that eight profiles are complete.

Three source ambiguities must remain visible:

1. **Random Alt (text0105–0106).** Choices12/Interval1 is said to cycle C3 through
   C4, suggesting13 positions including the original, whereas Choices2/Interval2
   is said to alternate C3/D3, only2 positions. These are retained in NME-050/051
   with null oracles; no generalized cycle cardinality is approved. D12 Alt's
   Chance0 passthrough and cyclic-order statement remain separable clauses.
2. **Arpeggiator Hold (0025).** Repeat-until-another-key wording coexists with
   adding pitches and toggling them out. NME-010 grades only continuation after
   release without another key; NME-014 leaves replacement/addition when all keys
   are up unknown.
3. **Note Off latch (0084).** The all-keys/pedal-released plus new-note-off wording
   does not supply an unambiguous multi-note transition. NME-038 grades only
   disabled controls; NME-039 probes note/pedal ordering without an invented
   output schedule.

Other material uncertainties: no known channel forwarding, changed-parameter
held-note policy, clamp at MIDI0/127, random seed/distribution, exact rate or
sample placement, unsupported/malformed-input handling, automation event priority,
undo/cancel grouping, save/load emissions or teardown cleanup. S-presence does
not narrow these U cases. Target fidelity remains open even for clear manual
clauses. The draft's prospective acceptance predicates are not observations.

## Capture and validation record

The first capture attempt successfully retained the HTML but stopped when it
encountered CC Control's null preset example. No source bytes were lost. The
extractor was corrected to preserve the existing HTML and record the absent
example explicitly; the resumed capture completed with eight schema classes
and seven preset sources. An initial schema-block endpoint selector included
following classes; it was corrected to stop at each exact closing class tag
before author freeze. These were packet-construction failures, not Live results.

[validate.py](../../analysis/ableton-live-12.4.3/full-spec-v1/native-midi-effects/validate.py)
checks raw and derived source correspondence, seven preset source hashes/XML,
eight exact schema blocks, numbered text locators, case-ID uniqueness,27 declared
requirement references,146 case grade/oracle coherence, all per-device lifecycle
case kinds, relative links/frontmatter and frozen payload hashes. Its retained
[validation result](../../analysis/ableton-live-12.4.3/full-spec-v1/native-midi-effects/validation.json)
reports actual checks. Hashes and a lint pass establish packet integrity only.
Root owns shared indexes, coverage, questions and append-only log integration.
The frozen author manifest is review input; a separate review must assess semantic
support before any reviewed-contract or release claim.

## Revision 2 review corrections

The [independent revision 1 review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/native-midi-effects-review.json)
requested changes to NME-NL-L01/L05: their Note On Latch setup disabled Length,
which they attempted to edit. M0084 supports that finding. Revision 2 uses
Latch off, Free Length200ms, Gate100%, with Length enabled and an output note
still sounding. Both event outcomes remain U. Lower-priority findings were also
corrected: NME-043/044/045 use a positive accepted UI Range value with unit/end
semantics U; NME-064 compares only output membership in60..127, keeping the
unresolved random-modulation baseline and displacement U. No transfer formula
was added. Counts remain27 requirements,146 cases,54 D12 partial predicates,
92 U and146 exact-build U/unexecuted.

The exact revision 1 manifest and all30 payloads were verified and archived
before edits in [author-r1-snapshot.tar.gz](../../analysis/ableton-live-12.4.3/full-spec-v1/native-midi-effects/author-r1-snapshot.tar.gz),
SHA-256 `c6967748a7b453dd5d8b4bb336faf42fe417bb3d1bd129e801f5a9e9a0b9864a`.
The original manifest remains unchanged; its historical path entries resolve
against that archive. The [revision 2 manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/native-midi-effects/manifest-author-r2.json)
pins current payloads, the archive and the original seal.
[Correction dispositions](../../analysis/ableton-live-12.4.3/full-spec-v1/native-midi-effects/review-corrections-r2.json)
name all three findings. The validator verifies archive contents against the
original seal, checks the corrected case setups/predicate and checks current
payload pins. Source capture bytes are unchanged. Revision 2 is ready for
focused independent review; no runtime or compatibility result follows.

## Revision 3 approved source-audit subsets

The [full retained-source audit](../../analysis/ableton-live-12.4.3/full-spec-v1/native-midi-effects-source-audit/README.md)
and [independent review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/native-midi-effects-source-audit-review.json)
support a bounded successor, not complete native MIDI behavior. All 112 chapter
blocks, 19 literal resource roles, 27 clauses and 146 actual future actions were
read. Images/destinations, surrounding owner families and runtime remain outside
this read. The current [R3 README](../../analysis/ableton-live-12.4.3/full-spec-v1/native-midi-effects/README-r3.md)
routes catalogs, preservation, exact delta and read-only validation.

All 32 old packet files, both seals, opaque R1 archive and all 146 case objects
remain byte/object exact. Prior wiki bytes are retained in spec-before-r3.md and
research-before-r3.md within the packet. The original revision-2 review-pending
text above records its author-freeze context; the retained final independent
review approved its narrow correction. Current R3 is pending independent review.
No old tool or archive extraction was needed for this successor.

R3 keeps 27 IDs, appends only clause008's per-Shift LED role and adds 30
source-claimed control/history proposals (176 total, 54 old D12 / 122 U).
All new documentary and all actual oracles are null; no new finite numerical
law is approved. The explicit R3 overlay qualifies future event branches with
independent genuinely productive NONEMPTY output and both received identities
before absence/order/merge; UI-only entries need no hardware. Old records are
not silently edited by that overlay. Random Alt, all-up Hold, Note Off Latch,
Pitch Range units/upper endpoint, Scale 13×13 context and Velocity displacement
remain open; source prose does not supply private mechanisms or target proof.

The [literal consumer-hash census](../../analysis/ableton-live-12.4.3/full-spec-v1/native-midi-effects/consumers-asof-r3.json)
retains historical/as-of dependency locations and exact snapshot providers.
Consumers are unchanged; no adapter/replay or current semantic approval follows.

## Bounded native MIDI family routes — 2026-10-20

Pending independent structure review: [family-native-midi-effects-routes-v1](../../analysis/ableton-live-12.4.3/full-spec-v1/family-native-midi-effects-routes-v1/structure.md) extends approved component/integration I04/I05/I07/I08 and playback/automation context for all eight processors. Current owner r3 has 27 requirements/176 unchanged scenarios, not the old 146 baseline. The ledger enumerates 309 observable/context rows, all without an established behavioral route in the selected DATA-only scope. Counts are inventory only, not grades, native absence, scope exclusion or a frozen product denominator; all actual/public input→same processor→outgoing event bindings remain unknown.

Censused, capped selections retain 165 lexical owner/membership/alias anchors, eight exact literal RTTI/table candidates, 49 prefix slots/35 targets, 27 literal store candidates and 212 fixed-set call rows. These units remain separate; template/reset/control names, table prefixes and store quotes are navigation, not behavioral/receiver proof. All full processor/control bodies remain unselected with explicit entry/PC/null-provider frontiers; no new traversal or indirect credit follows. Source D12 remains current Live 12 with 12.4.3 parity U. The map preserves Random/Hold/NoteOff-latch ambiguities, Range128/127 and enum/CC-order unknowns, enabled LatchOFF Note Length controls, and the R3 NONEMPTY/BOTH productive-event overlay for all 176 future cases. No original/provider/native/decoder/harness/model/comparator/fixture/build execution occurred. Root owns seal/shared routing and separate review; no owner, case, expected value, grade or release changes here.


## Native MIDI family-map approval — 2026-10-20

Root read/adopted the complete [independent structure review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/family-native-midi-effects-routes-v1-review.json), SHA256 `b7febe64dc55e09faff4e4022ad45426ebe5ca0582f2dd6f4ff7ec888d9ad95d`. Manifest `b28419e4e09997ac8c2a1cb7890ad2d3536879b6e2903471b1fa9dea2f9f430b`,13payloads/1,123,381bytes is approved as bounded structure only.309behavioral/context rows(91D12/218U) have no established behavioral route within the selected data-only scope; this is neither native absence nor impossibility. All27clauses/176scenarios/54D12-versus122U documentary labels and all actualU outcomes remain unchanged.

The reviewer verified750selected raw metadata/call rows,165membership-alias source triples,eight class/RTTI/prefix/store/control associations,212fixed call-row tags,309TSV/JSON pairs,33selectedpins/fourfoundationmanifests and13negative controls.165lexical/template owner rows are not165classes;49table-prefix slots/35targets/27store quotes remain separate. No body was read or new site resolved. Prior112-block semantic audit remains inherited; source-line labels are retained provenance, not a fresh full-index line census. At-most50 wording versus NME064membership-only displacement, NONEMPTY/BOTH, enabledLength/LatchOFF, Range/Alt/CC/held/RNG uncertainties remain qualified.

The pending section above is author history. Root separately selected one whole-eight-effects construction/activation/reset/registration source batch using a fixed class/store/control seed set and metadata-first size caps. Newly selected retained C1 bodies are data only; no encountered callee/global/slot expansion, original/model/comparator/fixture or provider execution follows automatically. This map approval changes no requirement, case, release or grade.

## Native MIDI initialization source batch — 2026-10-20

Pending independent source review: [depth-native-midi-effects-initialization-v1](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-native-midi-effects-initialization-v1/structure.md) retains one fixed whole-eight-effects batch selected from the approved family map: 27 literal-store candidate entries, 35 distinct prefix targets and 18 named lifecycle wrapper rows collapse to 74 unique records. The metadata-first census passed all caps (118,189 C bytes; maximum327 lines/record); 15 approved C1 chunk pins and exact raw/line/byte/C/native-range locators precede full selected-body reading. No callee/global/slot expansion or original/native/provider/decoder/harness/model/comparator/fixture/build execution occurred.

Conditional source-local relationships include constructor/table and callback/context stores, raw activation predicates, scheduled-carrier registration/removal requests, tracked-entry handling and payload-helper→stored-callback paths. Expanded four-byte constructor/control projections, false thunk metadata and unrecovered arguments are explicitly qualified. Shared payload/base/output helpers, callback/parameter receiver identity and actual public host/event transport remain unknown; raw indices, flags, recurrence/constants and names establish no UI units, seed/order/gate/lifecycle law. These are auxiliary investigative S relationships, not public outcome closure or grades. The approved309-row map remains as-of and unmodified; all27requirements/176scenarios and allactualU remain unchanged. The packet preserves NONEMPTY/BOTH and the prior Range/Alt/held/NoteOff-latch/CC-order/RNG/Velocity displacement unknowns. Root owns seal, shared routing and separate review.


## Native MIDI initialization source review approval — 2026-10-20

Root read/adopted the complete [independent initialization-source review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/depth-native-midi-effects-initialization-v1-review.json), SHA256 `68cf5164d9f345b897980413fd1b88efe77027c7343c0c642914595622e2bc76`. It approves manifest `c2ca756a12345d70e6ca55e484fbdac1d948a0e9f9aa25329c9223b5bf6ad106`,15payloads/646,126bytes and74fixed source records as bounded conditional source relationships. All16pins/15approved chunks,74raw/body/state locators,75claim spans and28claims were checked; the read-only checker rejected14negative controls. The17,736-byte research prefix remained exact. Fresh semantic reading covers69complete projections/3,560lines, including all59claim-evidence entries; five other constructor projections received declaration-name-only equivalence review against separately selected/read records. This is not a fresh literal74-body semantic reread.

Arpeggiator/Note Length scheduler-registration/removal descriptions are inferred source-role shorthand: helper semantics and success remain unknown. CC carrier context changes are not actual control delivery. Chord/Pitch payload/callback relationships do not supply wire/public modes, MPE or active-note lifecycle. Random/Scale/Velocity arithmetic remains conditional source expressions with unread base/output helpers and unknown parameter binding. Four-byte expanded Arp Reset/OnOn and CC Exit projections are not native operations attributed to those entries; retained tail targets101c15a18/101c136d4/101c1d948 remain unread/unselected. Raw OnOn flag writes establish no public bypass/flush law.

The309historical route rows,27requirements/176case objects and all actual/public outcomesU remain unchanged. Four hundred syntactic C frontier occurrences are not new native sites, resolved indirect calls or outcomes. No owner/case/release/grade/original execution follows. Root separately selected a metadata-first whole-eight event-processing/value-transformation frontier from existing class-qualified symbols: at most64records/196,608Cbytes/1,500lines each. No body materialization until that fixed census is reviewed; no encountered callee/global/native/provider or original execution is selected. The pending source append above retains its author-time meaning.

## Native MIDI event-processing frontier — 2026-10-20

Pending independent source review: [depth-native-midi-effects-processing-v1](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-native-midi-effects-processing-v1/structure.md) extends the approved family/initialization contexts across all eight effects. Root approved a fixed17entry metadata census before new C reading (50,962Cbytes/1,748lines/max327; six approved1achunks). Fourteen approved event-associated records remain referenced in place, and only three new class-qualified Arpeggiator/CCControl/NoteLength event-wrapper rows were retained once (6,203Cbytes/195lines). No new creation/lifecycle round or callee/global/slot expansion occurred.

The new source shows conditional raw-discriminator dispatch, stored callback requests and a CC indexed-value/flag/helper path. Arpeggiator and NoteLength wrappers have4Bnativeextents with expanded C despite false thunk flags; delegated targets remain unselected/unread and no expanded operations are attributed to those4Bbodies. Ten warning-bearing records remain conditional projections, with no total/native flow or failure law. Whole-eight assessment finds no established complete callable X leaf or public delivery route in this bounded set. Six auxiliary arithmetic/predicate fragments are source-local seams, not separately exported callable leaves, expected values or execution permission; receiver/helper/callback and x86entry/ABI/setup binding gaps remain explicit.

The approved309-row inventory and all27requirements/176scenarios/allactualU remain unchanged. Public same-instance event/control delivery, NONEMPTY/BOTH, active-note/held/pedal/NoteOff-latch, Range/enum/Alt/RNG/CC-order/Velocity displacement, gate/clock/lifecycle/save and ARM/Apple limits persist. No original/native/provider/decoder/harness/model/comparator/fixture/build or old author import executed. Root owns seal/shared adoption and independent review; no grade, case or release change follows.


## Native MIDI processing source review approval — 2026-10-20

Root read/adopted the complete [independent processing-source review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/depth-native-midi-effects-processing-v1-review.json), SHA256 `d76615503ff559a95a7a356de4b4fd348aff8ef7ebaced5c0e6f46818ba07649`. Manifest `beebb64c3159b9ae276b4963a65a7b888dba6af4a7965dd83c7881e8bf9c077b` binds17payloads/234,383bytes. The fixed17-entry whole-eight frontier reuses14approved raw records in place and retains exactly three new records once:6,203Cbytes/195lines. Thirteen pins/six approved chunks/all17record identities/nine claims/six fragment spans/17aliases/three old call slices and16negative controls passed;41paths/37slices and the21,857-byte research prefix stayed exact.

Fresh semantic reading covers all three new projections, all nine claims, six exact fragment windows and eight device assessments. Fourteen prior whole-body semantics remain inherited at the initialization review's scope, with fresh identity/warning checks; they are not claimed as fourteen fresh complete semantic rereads. Arpeggiator and Note Length wrappers have4-byte native extents but larger delegated C projections; their targets101c17300/101f4827c remain unread. CC's callback and101c1e7fc helper dependencies remain unresolved. All ten warning-bearing records retain jump-recovery, indirect-as-call and no-return qualifications, preventing total native-flow, unchanged forwarding or failure laws.

Raw event discriminators, local comparisons/recurrences/cache writes and callback requests remain source expressions with unknown event schema, parameter/current-value units, actual receiver, helper success, transport clock, output and lifecycle joins. The six arithmetic/predicate fragments are auxiliary and noncallable in this scope. No complete callable X leaf or public route is established within the fixed set; this is not proof of native infeasibility or absence. All309historical route rows,27requirements/176case objects and all actual/publicU remain unchanged. Zero new native sites, grades, normative clauses/cases/releases or automatic source successor follow. Earlier pending prose is author history; current selections belong to the plan.
