---
id: RES-DISTORTION-DEVICES
type: research
status: current
updated: 2026-10-19
access: analysis
revision: 4
target: Ableton Live 12 Suite 12.4.3; current official Version 12 manual
---

# Distortion device evidence

## Scope and route

This packet supports the [distortion draft](../specs/distortion-devices.md) for
nine separate device profiles: Drum Buss, Dynamic Tube, modern Erosion,
Overdrive, Pedal, current Redux, Roar, Saturator and Vinyl Distortion. The
[full inventory](full-live-coverage-inventory.md) supplies profile identities;
[coverage design](full-live-specification-design.md) defines partial versus
complete, and the [execution plan](full-live-specification-plan.md) owns status.
Root owns shared indexes, coverage, questions and append-only log integration.
The draft owns behavioral wording; this page owns source interpretation/limits.

## Source identities and observed evidence

**Observed, documentary.** Reused D12-AUDIO-EFFECTS from the existing
[manual source record](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/sources.json),
not a fresh fetch. Original URL is the official
[Version 12 audio-effect reference](https://www.ableton.com/en/live-manual/12/live-audio-effect-reference/),
captured 2026-10-19; no exact 12.4.3 publication is established. Exact reused
HTML SHA-256 is `9cb15cb3d80bda4771e5add2c2b74f5c57d73ee8850e198acf7cf8a51dfd1299`
(588328 bytes). The packet's [source manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/distortion/sources.json)
pins this external retained file and its original identity. Separate extraction
files preserve 216 paragraphs/headings/list items with HTML start-line and stable
B locators; all text is validated against the pinned HTML.

**Observed, package bytes.** Installed latest schema 12.0_12402 is reused from the
inventory, SHA-256 `b7c9d4c767d8ca9b346ce7d517265446bbacd6de366cc058e155613789d0f299`
(441285 bytes). Nine complete class field records are retained in
[schema-fields.json](../../analysis/ableton-live-12.4.3/full-spec-v1/distortion/schema-fields.json).
Exactly one inventoried preset per device was copied and hash-checked against
its inventory example, retaining all bytes and historical Creator 12.4d1.
[Package values](../../analysis/ableton-live-12.4.3/full-spec-v1/distortion/package-values.json)
retain /Ableton/class, root attributes and exact field XML. This proves presence
and one represented configuration, not loading, defaults, GUI domains or DSP.

| Profile | Schema and start line | Manual blocks | Bounded preset |
| --- | --- | --- | --- |
| Drum Buss | DrumBuss at line 1873 | drum-buss:B001–B024, §29.12 | Bonzo on the Dials.adv |
| Dynamic Tube | Tube at line 8203 | dynamic-tube:B001–B009, §29.13 | Broken Tube.adv |
| Erosion | Erosion2 2377 | erosion:B001–B007, §29.17 | Dusty Mids.adv |
| Overdrive | Overdrive at line 5913 | overdrive:B001–B007, §29.27 | Distort.adv |
| Pedal | Pedal at line 5942 | pedal:B001–B036, §29.28 | Bass Guitar Front of Stage.adv |
| Redux | Redux2 6321 | redux:B001–B015, §29.30 | Chiptune Filter.adv |
| Roar | Roar at line 6568 | roar:B001–B081, §29.33 | Roar.adv |
| Saturator | Saturator at line 6878 | saturator:B001–B029, §29.34 | Saturator.adv |
| Vinyl Distortion | Vinyl at line 8495 | vinyl-distortion:B001–B008, §29.41 | Awfull.adv |

## Interpretation and limits

**Documented, not executed.** The manual supplies named modes, control gestures,
signal order and qualitative interaction descriptions. The draft separates
main Drive from Saturator Waveshaper Drive; global gain from wet-only output;
Dynamic Tube's zero-Envelope follower gate; Erosion's sine-only disabled width;
Drum Buss's Decay at zero versus nonzero Boom; and Overdrive/Pedal zero drive
from a bypass guarantee. Each requirement maps exact retained blocks in
[requirements.json](../../analysis/ableton-live-12.4.3/full-spec-v1/distortion/requirements.json).

Roar adds routing/stage/filter/shaper modes, LFO/noise/follower modulation,
feedback/gate/compression, external audio and MIDI-note sidechains. No private
schema enum index is converted into a public mode identity. The manual's claim
that MIDI sidechain inactivates Feedback Mode/Amount is preserved as D12 rather
than corrected by intuition. Current Erosion explicitly says pre-12.4 Sets load
Erosion Legacy (erosion:B007). That is a documented version boundary, not a
retained old-Set loading test. Erosion2 and legacy Erosion remain separate.
Current Redux does not establish Redux Legacy semantics or migration.

**Unknown.** Exact 12.4.3 applicability of current-manual statements; nonlinear
transfer equations, oscillator/PRNG/random correlations, jitter/degradation,
quantization rounding, clipping thresholds, saturation gain normalization,
oversampling kernels/factors, filter coefficients/phase, envelope timing,
modulation summation/clipping, feedback stability and all calibrated audio,
CPU or latency tolerances. Schema-only fields such as Roar HiQuality or Redux
EcoProcessing do not establish visible controls or processing law. No file or
GUI malformed-input policy, undo grouping, cancellation restoration, save/reopen
preservation, reset or teardown response is inferred from storage presence.

The finite audio experiments are all U. Any effect/no-effect comparison requires
independently established source, active path, nonzero effective control or
modulation amount, nonmuted processed output and control-sensitive positive
baselines; other paths must be isolated. This is particularly necessary for
Erosion width, Dynamic Tube follower timing, Saturator Waveshaper zero influence,
Roar filter/feedback/matrix and Vinyl crackle versus harmonic paths. A setting
alone does not prove activation. Failed or missing prerequisites produce U,
never a pass. Silence and digital-zero input are not assumed to disable a
noise generator, tail, feedback or DC path.

## Finite cases and reproducibility

The preserved R2 catalog contains **67 requirements and 190 case entries**: 18 Dpkg source
assertions, 29 D12 documented UI/state criteria and 143 U outcomes with null
expected values. Counts are authored coverage only; no original/candidate case
has run. All nine profiles include positive, negative, boundary, automation,
persistence, undo, malformed, cancellation, transport, rate/block and teardown
cases. Device-specific sound interactions remain independently ungraded. The
proposed signals are deterministic analytic test inputs, not original output
captures or calibrated validators.

Historical R2 capture/validation commands (as-of only; not rerun against this successor):

```sh
python3 analysis/ableton-live-12.4.3/full-spec-v1/distortion/capture.py
python3 analysis/ableton-live-12.4.3/full-spec-v1/distortion/validate.py
```

Capture verifies existing retained bytes rather than silently replacing them.
The historical R2 [author freeze](../../analysis/ableton-live-12.4.3/full-spec-v1/distortion/manifest-author-r2.json)
contains payload hashes, external source pins, canonical spec/research snapshots,
case/source records and [validation report](../../analysis/ableton-live-12.4.3/full-spec-v1/distortion/validation-author-r2.json).
Frozen files must remain unchanged; corrections require a new manifest revision.
Separate review is required before any reviewed-contract claim or release.
No tooling installation, executable/bytecode/binary analysis, original-code probe,
reference application run, candidate change, publication or commit occurred.
The Amp/Cabinet unavailable-emulation route remains outside this packet.

## Review corrections, revision 2

The independent [revision 1 review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/distortion-review.json)
identified two Erosion fixture conditions. DST-EROSION-003 now selects and verifies
accepted Noise Blend=100% with enabled Filter Width before the positive modifier-Y
gesture. The disabled sine-only gesture is separately observed in DST-EROSION-005
with a null U oracle. This follows erosion:B003–B005 without asserting that an
inactive width can be changed. DST-EROSION-006 now uses S1's first second only:
1 second, 500 Hz, peak 0.1, identical channels with initial phase 0. Its width-
sensitive positive baseline, active modulation and nonmuted processed-path
requirements remain; its expected result is still null U.

The exact revision 1 seal and all 38 payloads were retained in
[archive-r1](../../analysis/ableton-live-12.4.3/full-spec-v1/distortion/archive-r1/manifest-author-r1.json)
before mutable edits. The root revision 1 manifest is unchanged; its historical
payload resolution is the archive. The revision 2 manifest freezes corrected
canonicals/cases and [response](../../analysis/ableton-live-12.4.3/full-spec-v1/distortion/review-response-r2.json),
with source and proposed signal invariance checks. Requirement/case/provenance
counts remained 67/190 and 29 D12/18 Dpkg/143 U. At that original author freeze, focused independent re-review was
still required; exact-build, audio, lifecycle and complete-profile limits remain.

## Full selected-source audit and focused association correction

The [full216-block source audit](../../analysis/ableton-live-12.4.3/full-spec-v1/distortion-source-audit/README.md)
received an [independent full review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/distortion-source-audit-review.json)
requiring DSA-REVIEW-001. The [minimal additive R2](../../analysis/ableton-live-12.4.3/full-spec-v1/distortion-source-audit/README-r2.md)
then passed [focused independent review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/distortion-source-audit-r2-review.json).
Roar007/030 actually select all nine filter types, toggle Pre and require
productive filter/nonlinear baselines. Neither explicitly changes gain-stage
Filter Frequency; this remains documented but unexercised/U with a bounded future
action in existing G06. Analysis/feedback Frequency are separate controls.

Four literal replacements correct two logical fields in each catalog, preserving
all original six audit files and83owner/history files. The historical README and
old judgments remain frozen. All215other assessments/nineother groups,67clauses,
190cases and fixtures/source/null outcomes are exact. Ten bounded audit-only groups,
six questions and48literal resources are not atomic coverage or adoption. One
sealed README total-versus-unchanged denominator ambiguity is qualified by the
review; no cosmetic packet revision. No owner behavior, quantitative law, runtime,
exact-build compatibility or complete profile was established.

## Owner revision 3 bounded action adoption (research page revision 4)

AS-OF AUTHOR FREEZE: independent owner review pending; current disposition is routed by shared indexes. Root's reviewed source-audit metadata was already research revision 3; its exact 10548-byte page is preserved in [research-before-owner-r3.md](../../analysis/ableton-live-12.4.3/full-spec-v1/distortion/research-before-owner-r3.md), rather than assuming it equals the earlier R2 research snapshot. Owner packet revision 3 uses research page revision 4 and spec page revision 3. No prior metadata/provider or source-audit bytes are overwritten.

The approved [corrected source audit R2](../../analysis/ableton-live-12.4.3/full-spec-v1/distortion-source-audit/README-r2.md) and [focused review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/distortion-source-audit-r2-review.json) support ten selected finite actual-action histories. [The current catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/distortion/cases-r3.json) retains 190 original objects and adds ten U records: 200 current cases, including the unchanged 29 D12/18 historical file-only Dpkg/143 U originals plus ten new U histories. All 67 requirement IDs/bodies remain exact. [The actual overlay](../../analysis/ableton-live-12.4.3/full-spec-v1/distortion/actual-overlay-r3.json) keeps every current actual expected/comparison null/U/unexecuted; legacy documentary/source fields are not actual results.

Selected actions add Bass Meter observation/qualified low-path Decay history; Erosion carrier display roles with corrected Width/S1 prerequisites; Overdrive slider-box and productive return histories; optional Pedal kick/Fizzle/chain entries; actual Roar Parallel Blend modulation; actual gain-stage Filter Frequency plus eligible Resonance/Peak Gain/Morph; actual Matrix cell/global slider/activity entries; Roar manual-control-positive then MIDI sidechain eligibility context; Saturator Color slider alternatives; and Vinyl double-click/type Freq entry for both models. [The source/case ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/distortion/adoption-r3.json) records only selected subsets. Other Pedal/Roar recipes, lifecycle/capacity/source-loss combinations and all unproved DSP remain pending. Dynamic Tube/Redux true existing cases are preserved without invented generic additions.

Crucially, actual Roar Filter Frequency operation is not inferred from a filter-sensitive baseline, source text, or the distinct analysis/feedback Frequency controls. EACH chosen filter/control AND nonlinear Shaper must independently work before Pre/loss/order. EACH source/control/route and BOTH relevant channels/stages/modulators/voices/targets need genuine productive nonzero output before absence; dry and wet paths need separate positives when compared. Gate/input-removal/tail observations require genuine sustaining feedback first. Flags/names/S0 never prove noise or tail absence. UI-only gestures need no sound/hardware. All new documentary and actual expected/comparison fields stay null; no optional recipe promises an aesthetic result for every input.

The source remains exact588328-byte current Version12 HTML, captured date-only2026-10-19 with UTC unknown, target12.4.3U. Modern/Legacy, Erosion enabled-modifier/first1sS1, Roar both inactive Feedback controls, Listen replacement and zero-envelope/waveshaper path qualifications remain intact. No numeric DSP/RNG/clock/default/CPU/quality/formula/codec/file law or exact sound identity is added. No source pixels/destinations, preset/schema decode, original/vendor/native/UI/audio/MIDI/hardware/network/install/candidate or product-file operation occurs.

[The finite consumer census](../../analysis/ableton-live-12.4.3/full-spec-v1/distortion/consumer-history-r3.json) retains five exact current-before-canonical hash occurrences across four frozen JSON files, including one external direct spec pin; current research revision3 had no such consumer. All remain as-of, not future live gates. No automatic replay/adapter or consumer edit is added. [Immutable inputs](../../analysis/ableton-live-12.4.3/full-spec-v1/distortion/inputs-r3.json), [exact delta](../../analysis/ableton-live-12.4.3/full-spec-v1/distortion/delta-r3.json), [current checker](../../analysis/ableton-live-12.4.3/full-spec-v1/distortion/check-r3.py) and [author seal](../../analysis/ableton-live-12.4.3/full-spec-v1/distortion/manifest-author-r3.json) freeze this bounded successor for independent owner review; no full-family or compatibility closure follows.
