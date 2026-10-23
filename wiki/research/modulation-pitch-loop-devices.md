---
id: RES-MODULATION-PITCH-LOOP-DEVICES
type: research
status: current
updated: 2026-10-19
access: analysis
revision: 4
target: Ableton Live 12 Suite 12.4.3
---

# Modulation, pitch, spectral and looping: retained documentary evidence

## Ownership and method

The [individual-device draft](../specs/modulation-pitch-loop-devices.md) owns
observable contracts for ten current F-06 devices. This page owns documentary
interpretation, source limitations and the spectral alias correction. It follows
[coverage design](full-live-specification-design.md) and the
[execution plan](full-live-specification-plan.md). It does not supersede the
rack, host, MPE, tuning or recording owners linked in the specification.

The [capture program](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/capture.py)
uses Python standard-library HTML parsing, gzip/XML preset reading and SHA-256.
It reuses the exact audio-utilities HTML, reads ten selected shipped presets,
the latest schema and preexisting discovery inventories, and audits only the
two spectral preset folders for the discovered alias discrepancy. No tooling
was installed. No native binary, original function, Live instance, emulation,
hardware or candidate was run. No implementation context was created.

## Source identities and observations

The [source ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/sources.json)
records external paths, sizes, hashes, official URL, capture date and retained
local preset copies. The manual's original identity is D12-AUDIO-EFFECTS in the
audio-utilities packet; it is not relabeled a fresh capture. Its SHA-256 is
`9cb15cb3d80bda4771e5add2c2b74f5c57d73ee8850e198acf7cf8a51dfd1299`.
The latest retained schema SHA-256 is
`b7c9d4c767d8ca9b346ce7d517265446bbacd6de366cc058e155613789d0f299`.
Both are external pinned dependencies rather than copied raw history.
The canonical spec appendix gives exact per-device manual sections and links
to 332 extracted heading/paragraph/list blocks with their HTML line locators.

**Observed Dpkg:** all ten chosen preset XML roots carry
`MinorVersion="12.0_12402"`, `Creator="Ableton Live 12.4d1"`, Revision
`42bc084cd8152e4fb737ef3fefd04b2bea5320e7`.
Their presence in the 12.4.3 package does not make 12.4d1 its runtime identity or
these stored values constructor defaults. One example per class is sufficient
for field-presence corroboration only; full legal domains and semantics are U.

## Spectral discovery-association correction

**Observed Dpkg:** the immutable initial discovery inventory associated Spectral
Resonator with `Spectral`/line 7423 and a preset physically stored in Spectral
Time's folder, and Spectral Time with `Transmute`/line 8118 and a preset in
Spectral Resonator's folder. The
[bounded folder ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/spectral-folder-observations.json)
retains exact paths, sizes and hashes for all 28 `.adv`-suffixed files in those
two folders. Fourteen names beginning `._` are excluded sidecars, not fourteen
additional product presets. The remaining eight Spectral Resonator presets all
have root `/Ableton/Transmute`; the remaining six Spectral Time presets all have
root `/Ableton/Spectral`. No non-sidecar preset parse failed.

**Observed vocabulary:** checked `Transmute` schema/preset fields include
`MidiPitch`, `PartialFrequencies`, `Global_NumHarmonics`; checked `Spectral`
fields include `Freezer`, `Delay`, `ProcessingOrder`.
[Exact class fields](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/schema-fields.json)
and [example root/fields](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/package-values.json)
retain the actual flattened field spellings. The manual Resonator sections
29.36.1–29.36.5 discuss MIDI/partials/harmonics, and Time sections 29.37.1–29.37.4
discuss Freezer/Delay/order. This supports the corrected **artifact association**
Resonator→Transmute and Time→Spectral. It does not establish runtime equivalence,
DSP semantics, exposure of every field, or a public serialized API. The frozen
inventory and original preset bytes remain unchanged. The independently reviewed
[companion inventory revision](../../analysis/ableton-live-12.4.3/full-spec-v1/inventory-revisions/r2-spectral-aliases/devices-r2.json)
and its [review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/inventory-spectral-alias-review.json)
now own the corrected discovery routing. This packet retains the original
inventory ID in historical source records rather than hiding it; the
[association reconciliation](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/association-reconciliation.json)
explicitly maps those crossed spectral IDs to the checked physical preset
identity. Neither retained R1 label is a current device association.

## Documentary distinctions that affect cases

The spec's source-mapped requirements remain canonical; these are evidence
interpretation notes, not competing control specifications.

- Auto Pan-Tremolo §29.3's channel-LFO descriptions concern modulation. Equal LFO
  values do not mean equal output samples from arbitrary stereo input. Random
  Phase Offset wording and beat-mode availability do not establish extra
  free-running control eligibility.
- Auto Shift §29.4.1.1's no-MIDI sound statement must be tested on its processed
  path, with Dry/Wet full wet and prior latch/release history excluded. It is
  not assigned to Shifter or Spectral Resonator by similarity. Voice Count,
  MIDI On and MIDI panel visibility have distinct roles.
- Chorus-Ensemble §29.8 disables Feedback and Dry/Wet in Vibrato; that is a
  control eligibility proposal. It supplies no independent audio invariance
  comparator when a disabled control is manipulated.
- Phaser-Flanger §29.29 explicitly requires Env Fol enabled and nonzero amount;
  negative Amount reverses envelope phase. Random-waveform Duty Cycle/no-effect
  testing still needs active nonzero modulation and an audible positive baseline.
- Shifter §29.35.1 calls the Delay free slider Hertz. Its preset field spelling
  `Delay_TimeSeconds` does not authorize silently correcting the UI unit or
  inventing a conversion. §29.35.2 describes Random S&H Width in LFO terms,
  which supplies no exact stereo audio law.
- Spectral Resonator §29.36.1 makes MIDI Gate always active in Poly and Glide
  Mono-only; §29.36.3's Chorus Mod Rate zero exception still concerns active
  amplitude modulation. Quantize needs explicit scale/tuning/chromatic context.
- Spectral Time §29.37 initially describes Freezer feeding Delay, while
  §29.37.4 supplies both orders. The specific order control prevents an
  unconditional Freezer-first contract. §29.37.1 requires Freeze enabled in
  both trigger modes, and its X-Fade sentence mixes ms/percentage language;
  no exact conversion or fade coefficient is specified. Section-local and
  global Dry/Wet remain distinct.
- Vocoder §29.42's Sens endpoints control unvoiced detection/generator activity,
  not guaranteed audible noise at zero Unvoiced level. External carrier and
  modulator paths require separate positive baselines. Filterbank mode names
  do not supply filter coefficients or channel downmix weights.
- Beat Repeat §29.5 distinguishes automatic Chance/Interval/Offset/Gate from
  manual Repeat and separates three output modes. Endpoint no-repeat proposals
  require Repeat off, a valid nonzero repeat path and Chance 100 positive trial.
- Looper §29.25 distinguishes its own recording, overdub Undo, monitoring and
  tempo ownership from track recording/global Undo. Reverse changes existing
  and newly overdubbed material differently. No retained audio proves those
  time-domain outputs or supplies a resampler/clock oracle.

## Unknowns and retained checks

The preserved R2 catalog has 96 D12 clauses plus ten U lifecycle obligations and 186 cases:
55 control/state documentary proposals, 41 ungraded audio obligations and 90
device-specific U lifecycle cases. Every exact-target expected outcome is null,
every target grade U, and every case unexecuted. Boundary/automation/transport/
persistence/undo/malformed/cancel/teardown/sample-rate questions remain required
for every device. Figures, CPU performance, MPE codecs, voice stealing, onset
thresholds, latency, FFT/filter/resampler/gain/fade laws, random distributions,
state migration and crash recovery were not established.

The historical R2 [validator](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/validate-r2.py)
checks source pins and manual-line/block reproduction, schema locators,
folder-root evidence, all requirement references, distinct device ownership,
null unknowns, per-device lifecycle coverage, metadata, page-relative links and
whitespace including untracked files. Its
[author result](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/validation-author-r2.json)
is a packet integrity check, not a behavioral pass. The
[manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/manifest-author-r2.json)
freezes all payload bytes and canonical spec/research snapshots for a separate
analyst review. Shared index, question, coverage and append-only log integration
is coordinated outside this owned packet.

## Revision 2 discoverability correction

The existing 10 U lifecycle requirements now use requirement headings so the
existing requirements browser discovers all 106 IDs. Their IDs, U classification,
body text, 106 requirement records and 186 case records are unchanged. The
[original r1 seal and payloads](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/archive-r1/manifest-author-r1.json)
remain byte-for-byte preserved. The [narrow response](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/response-author-r2.json)
and [revision tool](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/revise-r2.py)
record this presentation-only change. Earlier independent semantic review retains
its prior partial scope; no runtime, whole-profile or compatibility claim expands.

## Revision 3 selected source-action adoption

AS-OF AUTHOR FREEZE: independent owner review pending; current disposition is routed by shared indexes. The independently [approved full retained-source audit](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/modulation-pitch-loop-source-audit-review.json) compared all 332 selected contexts, 106 bodies and 186 original case records. Its 22 research proposal groups are not complete device specifications. R3 selects a bounded finite action history from each group, preserving all prior predicates and objects. The [adoption ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/adoption-r4.json) records exact source pointers and unresolved subsets.

Current routing is 106 unchanged requirements and [208 cases](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/cases-r3.json): the original 186 plus 22 null documentary/actual future histories. The [actual-status overlay](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/actual-overlay-r4.json) explicitly keeps all 208 actual expected/comparison values null, target U and unexecuted. Old documentary control/state/signal fields remain historical proposals, not observed results. All 107 prior recursive files, original seals and R2 providers remain exact in place; no duplicate whole archive or identical requirement catalog is added.

Actual entry/reset histories extend mode-specific Auto Pan controls; Auto Shift displays, MIDI/latch/modulation/pitch/vibrato contexts; Chorus Rate dial/display gestures; Phaser display/envelope controls; Shifter tuning/modulation/Drive; Spectral Resonator MIDI/scale/display/optional combined routes; Spectral Time menu/capture/order; Vocoder carrier/band/recipe gestures; Beat Repeat ending/variation; and Looper Clear/record/import/processing histories. Existing productive Blend/Duty Cycle/Chorus Rate-zero/Auto Shift correction-off/Looper halves/local Undo/both Insert-Looper taps remain true subsets. Inspecting a control does not operate it; a completed conversion or enabled route does not prove received notes/output.

All future audio steps require genuinely recognized NONEMPTY source and independently productive active wet/control/output paths first. EACH route and BOTH channels/notes/modulators/buffers/voices must be productive before suppression, loss or ordering; captures/Clear require observed nonzero content. Incompatible common defaults are explicitly replaced by each history's Quantizer MIDI Off, Internal, Mono, Repeat Off or latch/release context. UI-only steps need no hardware/audio. Unsupported fixtures/receivers, unavailable mapping hardware, Link peer behavior, individual unison contributions, safe limiter-positive observations and voice allocation remain U or pending. No forced clipping/stress, arbitrary file/MPE acceptance, exact silence, capacity guarantee, random noncoincidence, timing, pitch or gain formula is introduced.

The source remains exact Version 12 HTML, date-only 2026-10-19 with UTC unknown; target 12.4.3 is U. All raw Hertz, X-Fade ambiguity, Frz>Dly/Dly>Frz and historical modern/Legacy/spectral association qualifications remain unchanged. Neither the audit nor R3 inspected image pixels/linked destinations or executed original/vendor/native/UI/audio/MIDI/hardware/network/candidate code.

[The finite consumer ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/consumer-history-r3.json) records 13 exact old-hash JSON occurrences in six frozen files, including one external direct canonical-spec pin. These consumers and old validators/reports remain as-of historical inputs; none was edited or replayed, and no automatic adapter is added. New validation uses only [own immutable inputs](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/inputs-r3.json), [exact delta](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/delta-r3.json), the [current checker](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/check-r4.py) and [R3 seal](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/manifest-author-r4.json). Independent owner review follows author freeze. No behavior/full-family/compatibility completion is claimed.

## Revision 4 pointer-only correction

AS-OF AUTHOR FREEZE: independent owner review pending; shared indexes route current disposition. R4 corrects 230 navigation fields only: 208 actual-overlay and 22 adoption-ledger case pointers now dereference the top-level case list as `/i`, rather than the invalid `/cases/i`. All 208 case objects, 106 requirement objects/bodies, source/action fields and documentary/actual oracles remain unchanged from R3. The sealed R3 packet and its inadequate pointer check remain exact historical evidence; its passing result is not pointer-validation proof.

The [correction record](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/pointer-correction-r4.json), [exact page delta](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/delta-r4.json), [current checker](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/check-r4.py) and [current author seal](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/manifest-author-r4.json) bind the effective correction. The checker actually dereferences each of the 230 pointers against `cases-r3.json` and checks its case ID. It rejects a jointly restored invalid prefix, wrong valid index, missing/duplicate references and out-of-range index. No old main/replay or case behavior is executed or changed; all target/actual outcomes remain null/U/unexecuted and completeness remains zero.


## Modulation, pitch and looping family route map — 2026-10-20

Pending independent structure review: the [bounded family map](../../analysis/ableton-live-12.4.3/full-spec-v1/family-modulation-pitch-loop-routes-v1/structure.md)
extends approved I05–I08 and Mix/Automation context across all ten current
profiles. The [R4 owner review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/modulation-pitch-loop-owner-r4-review.json)
approves a partial successor and230pointer-only corrections; prior pending
author-freeze prose remains history. Current106whole-clause bundles/208cases,
186old exact objects and all actual null/U overlays remain unchanged.

The [route ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/family-modulation-pitch-loop-routes-v1/route-ledger.json)
records106whole-clause bundles, all no-established-route/actualU. They are not
atomic outcomes;96D12/10U source annotations label those SAME106units, not96
additional outcomes. Ten auxiliary retained-file S facts stay outside106 and
cannot satisfy runtime/lifecycleU. Required unsupported behavior remainsU and
family/product coverageOPEN; there is no documentary-complete fallback.

Metadata retention followed Root's exact coherent32primary class scope across
ten model/processor/module frontiers and two typed curve-helper candidates.
Twenty large tables retain leading3 construction/lifetime slots; twelve small
tables retain whole exported prefixes, not complete native tables/classes or
processing callbacks.704DATArows retain102selected of1770exported-prefix slots,
67stores,133aliases/133memberships and160one-hop outgoing plus27unresolved
indirect rows from122named seeds. Eleven UI/display/timer-name entries remain
metadata but their outgoing rows are unselected; corresponding required UI and
lifecycle outcomes remainU. No incoming/transitive/callee expansion occurred.
Curve helpers may visualize only; no LFO/pitch/math/audio leaf follows from names.

All106fullclauses and208fullcaseactions/control/limit contexts were freshly read.
Fresh332rawspan/geometry and418case-source joins do not renew the inherited full
332-block source audit. Corrected Resonator→Transmute and Time→Spectral remain
artifact associations only; failedR3 pointers and separate Legacy profiles stay
historical/separate. EACH/BOTH productive NONEMPTY/NONZERO guards, explicit
MIDI/Mono/latch/RepeatOff overrides, genuine captures/Clear baselines, Shifter's
literal Hertz, SpectralTime's mixed X-Fade/both orders, Looper localUndo/both
InsertLooper taps and all numerical/runtime/lifecycle gaps remain qualified.
No C body/native/provider/decoder/original/harness/model/comparator/fixture was
run or selected. Root owns final seal/review and shared routing integration;
no grade, owner/spec/case/release or automatic successor is authorized.


## Modulation family route review approval — 2026-10-20

The immediately preceding pending-review paragraph is the exact dated author proposal,now qualified by this later approval. Root read/adopted the complete [independent review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/family-modulation-pitch-loop-routes-v1-review.json),32,459bytes/SHA25636378e40412cc29fac99944e49ad7b0931f1a5f938b39edd1a6c3b4c9eba7d83,with no findings. A truncated middle was separately reread in full. [Manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/family-modulation-pitch-loop-routes-v1/manifest.json),SHA2564f42965236b9b26b71fa24134dec6170b3e305ddc56682da48b41a132700390e,binds23payloads/1,765,052bytes. All106wholeclause bodies/subconditions and208complete action/control/limit histories were freshly reviewed;186oldobjects/230correctedpointerjoins/208batchactions/148adoptiontexts/39pins/704selectedrawmetadata/43negativecontrols passed. Full332source semantics remain inherited;332geometries/418caseblock/148adoptionjoins are mechanical.

All106requiredwholeclause bundles remainnone/U(0S/0X);96D12+10U annotate SAME106,not202contexts. TenfileS assertions are auxiliary outside;all208applicationactualresults staynull/U. Spectralcrossed historical IDs andcorrectedcurrentartifact IDs/reconciliation pointers/hashes remainseparate,bothswapcontrols reject. Pre-freeze auxiliarylabel correction is disclosed,no owner/source rewrite. Thirty-two tables/102of1770slots/67stores/133aliases133memberships/122outgoingseeds/160direct27emptyindirect retain boundedmetadata scope;elevenUI-methodgroup outgoing exclusions do not discard requiredUI/lifecycle behavior.

Source/currentcase productive EACH/BOTH/nonempty/nonzero,explicit MIDI/Mono/Quantizer/latch/RepeatOff,capturedcontent/Clear,ShifterHertz,SpectralTimeorders/mixedunits,carrierchannels/Chancepositive/localUndo/taps remainqualified. Typedcurvehelper updates may visualize only,no math/audio leaf. No body/native/original/provider run,site/grade/norm/case/release/publicroute/automatic successor orfamily/productclosure. RequiredunsupportedU keepscoverageOPEN. Entire15,924byte priorresearchprefix includingdate plus2,824byteproposal append remainexact;frozen pendingflags andasofcanonicalchecks retain historicalscope afterthisapproval.


## 2026-10-21 — Complete selected122 source frontier (pending independent review)

PROPOSAL ONLY. Root may append a reviewed disposition to the canonical research page after independent review. This file does not edit that page or adopt claims.

The bounded [whole122 source packet](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-modulation-whole122-source-frontier-v1/README.md) extends the approved Modulation/Pitch/Loop map's entire122 outgoing-seed frontier. All133 parent aliases/memberships and the complete11 UI/display/timer seed exclusions remain explicit. Root separately approved source reading after the complete metadata census; no firstN or processing-name subset was taken.

The122 exact raw records were retained once (437,740bytes) and all360,530 C UTF-8 bytes/9,041lines read, with20 warned records/31literal warnings and47four-byte native extents/false thunk flags preserved.44of those47 have>11C lines; three return-like projections have10/10/11. All12 large Vocoder variants were read losslessly using a full base plus every changed and exactshared span; all target C is reconstructible and no representative-only omission occurred.

The source shows control/scheduling, buffer/history processing, coefficient/indexed algebraic updates, and callback/transaction projections. Whole Looper CalcImport/CalcRecording C projections are helper-free under declared lexical patterns; the indexed Vocoder cube and scalar exp2f update are concrete source prospects. Their native extent/ABI/executable counterpart, legal object/buffer/index/rate/history state, FP/library behavior, supplied legal inputs and calibrated oracle remain unproved. The typed AutoPan2/Chorus2 curve wrappers expose only unresolved virtual forwarding, not curve math. Save/import callbacks and copied result cells do not establish successful durable operations.

No complete callable math X leaf, execution-ready batch, public binding, new native-site credit, original/model/harness execution, or automatic successor is established. Actual current control/provider→same callback/processor and result→host output, clocks/ordering/load/lifecycle and public effects remain unknown. No encountered helper/global/table/callee/native/provider was followed;12chunk/alias custody remains inherited without replay.

All106 required whole-clause bundles and208 actual records retain U/no established exact-target routes.96D12 plus10unknown annotations label the SAME106, with10file-S auxiliary predicates outside. Full332 documentary semantics and owner/case actions are inherited rather than newly audited.25,095native sites/268,015inventory denominator, requirements, cases, grades and releases are unchanged. Unsupported required behavior keeps coverage OPEN; no documentary fallback. Root seals/reviews/adopts separately.


## Modulation whole122 source review approval — 2026-10-20

Root read and adopts the full [independent source review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/modulation-whole122-source-v1-review.json),
63,095 bytes, SHA256
`2e4ba1199ec0dcc6257317bf1d5066eb41513561392d053108bfddebf9c06c1e`,
with no blocking findings. The [manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-modulation-whole122-source-frontier-v1/manifest.json)
seals 24 payloads / 1,574,875 bytes. The exact pending proposal above remains
history, qualified by this approval and M122-REVIEW-NOTE-001: ordinal24's unused
second declared argument is **void\***, not a declared scalar. Its native ABI
and actual payload type remain unknown. Frozen assessment bytes are preserved.

All 122 bodies / 360,530 C bytes / 9,041 lines, 31 warnings in 20 records,
9 whole claims, 8 OPEN frontiers and 6 NOT READY prospect classes were reviewed.
All 12 Vocoder variants were losslessly read and independently reconstructed,
including every changed and exact shared span; stereo/carrier diagnostic
copy/scaling differences remain distinct. The 33 author and 17 independent
negative controls passed. Eight metadata-stage files / 320,807 bytes remain exact.
Original alias and twelve-chunk custody remain inherited without replay.

Forty-seven four-byte native extent records include 44 expanded projections
longer than eleven C lines. Whole Looper CalcImport/CalcRecording projections
contain no calls under the declared lexical patterns, but native implementations,
legal buffers/counts/history/aliasing, ABI and numeric interpretation remain
unknown. Fixed64word copies establish no host block size. Indexed Vocoder cube,
exp2f/coefficient/rate expressions retain index/domain/receiver/library-FP gaps.
Return-only Init/Reset fragments establish no global inactivity. AutoPan2/Chorus2
typed-curve wrappers forward unresolved virtual+0x1e8 through distinct linked
fields, with no recovered curve formula or public LFO identity. Transaction,
path, cancellation, refcount and result-cell projections prove no durable
import/export, Undo/rollback, file format or successful public operation.

The 740 declared lexical occurrences (374 FUN, 169 global, 130 library/builtin,
67 indirect-expression lines) are navigation under explicit token patterns,
not an exhaustive native-call inventory. None was followed. All 106 whole
clauses / 208 actual-U records, same-unit 96D12+10U annotations and ten auxiliary
file-S predicates retain their separate scopes. No complete callable math/X leaf,
ready batch, native-site credit, current control/processor/audio route, case,
grade, release, closure or automatic successor follows. Required unsupported
stays U and whole-product coverage OPEN.
