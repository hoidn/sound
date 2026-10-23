---
id: PLAN-DEVICE-TENSION-HANDOFF
type: research
status: current
updated: 2026-10-22
access: analysis
target: Ableton Live 12 Suite 12.4.3 / macOS arm64; retained x86_64 extracted renders
---

# Tension finite audio handoff candidate

Released locally on 2026-10-19 as
[device-tension-v1](../../handoff/device-tension-v1/README.md), from
[SPEC-DEVICE-TENSION revision 2](device-tension.md). Independent review accepted
only its 27 fixed-protocol outputs and stated measurements. No original code
ran during staging; the package establishes neither Live integration nor
arm64 execution. The sections below retain the author and review record;
[Local publication](#local-publication) records the current disposition.

## Scope and narrowing

The payload contains 27 finite cases/evaluations: 26 stable settings and the
repeated-strike setting. Every selected setting has a retained five-variant
numerical-sensitivity study. Of 68 retained outputs, four chaotic settings and
37 settings without their own retained calibration are excluded.

Each evaluation includes all 129 named comparison-domain components, parameter
order, exact binary32 values, generated note events, zero input, sample rate,
512-frame partition and zero warm-up. Reference sample bytes are copied exactly
from the retained mono WAV data chunks. No project/preset bytes, original
device executable or recovered synthesis code is included. Named numerical
components are finite comparison inputs, not a stored format or required API.

Partial output scopes: REQ-001 and 004 to 012. REQ-002, 003, 013, 014 and 015
remain unreleased. No general tuning, timing, allocator, gain or modulation law
is carried. Bow, bow-position variant, zero damper mass and cello are excluded;
their broad RMS/peak statistical proposal is not accepted by this candidate.

The waveform criterion fixes held/release windows at the reference onset and
event timestamp; candidate timing cannot move those windows. Stable partial
centers, FIR cutoff/window and amplitude normalizer are frozen from the
retained eligibility study. Missing or unmeasurable required partials fail.
Only the repeated-strike waveform is graded; its unstable partial estimates
are excluded. Omitted modes and all unlisted inputs retain no pass claim.

The directed-rounding and one-ulp library studies demonstrate sensitivity of
x86_64 reference outputs, not a guaranteed arm64 error bound. Draft revision 2
corrects that overly strong appendix wording. The accepted metric remains a
fixed-scope project criterion.

## Provenance

All 161 payload hashes/sizes in the
[retained manifest](../../analysis/ableton-live-12.4.3/r2/t12-tension-v1/manifest.json)
were checked, together with every listed external source and both executable
slices. For each selected output, retained script events and the single process
length match the run registry. The script supplies the entire parameter vector;
the numerical-name table supplies comparison labels, including separately
named sign/enable/slope components. No original source or published release was
modified.

The [analyst companion](../../analysis/ableton-live-12.4.3/handoff-staging/device-tension-v1-analysis/traceability.json)
records every source case, WAV and script digest, raw-reference digest,
measurement locator, calibration maxima and exclusion. `source-inventory.json`
keeps the complete source inventory/identities. `environment.json` records the
numeric environment. `build.py` copies and audits retained bytes; `seal.py`
inventories the reviewed package; `validate.py` tests comparison behavior and
an isolated export. None executes the original device.

## Validation and next step

Verify the reviewed package from the repository root:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 -I analysis/ableton-live-12.4.3/handoff-staging/device-tension-v1-analysis/validate.py
```

Rebuilding with `build.py` recreates unreviewed author data and requires review
again before resealing; do not replace reviewed bytes solely to change labels.

The validator records all self-comparison checks, every-case silence, doubled
gain and early-impulse mutants, invalid-length/non-finite/missing output rejection,
payload inventory, restricted-source scan, local links and a separate exported
copy's comparator CLI against its reference directory. Results belong in
`author-validation.json` and `isolated-self-comparison.json` in the analyst
companion. They are author checks, not independent review or compatibility.

Author validation passed for all 27 self comparisons (806 measurements),
81 altered outputs and seven invalid/missing file checks, including the
isolated export. Initial author candidate manifest SHA-256:
`d8c4cb87e188ce677435b83ed4bed7e64dfd68b77d32c08e4d6686bbf69aaecf`.

## Independent review outcome

A handoff reviewer separate from the Tension candidate author accepted only the
27 finite comparisons, source sharing and exclusion, fixed measurement windows,
calibration limits and the standalone package. The
[clean review record](../../analysis/ableton-live-12.4.3/handoff-staging/device-tension-v1/REVIEW.md)
owns the disposition. The
[independent reviewer evidence](../../analysis/ableton-live-12.4.3/handoff-staging/device-tension-v1-analysis/reviewer-validation.json)
records 161 original payload hashes, all listed external identities and both
slices, 135 per-setting calibration variants, exact binary32 input/event/protocol
checks and mono-to-original-stereo digest equality. Perturbed audio remains
unretained; the historical calibration summaries cannot be independently
recomputed from this package.

The reviewer added explicit nonempty/mono-shape/finite-array checks, valid
waveform windows and a nonempty stable-partial requirement to the measurement
comparator. Nine malformed direct-input/requirement cases fail. Independent
generated-tone checks at 90% and 110% exercise all three partial limits and
all three waveform limits; the relevant check accepts below and rejects above.
No vector, event, reference sample, selected mode, window or tolerance changed.
Observable document/control names remain labels for explicit comparison-domain
components; their spelling does not prescribe an original API or implementation.

The revised comparator passed all 27 self-comparisons (806 measurements),
81 mutants and seven malformed/missing-file controls after the guard changes.
Subsequent payload edits clarified prose and review metadata only. Independent
final inventory, source exclusion and isolated export checks cover the final
reseal. Reviewed staging manifest SHA-256:
`5c42bd304d14e2d2ac6eba02c8ee3dfe704c1977bbd19c500ede759529833fe4`.

Publication is transferred to the coordinator. Local publication, shared catalog/index/coverage/log updates and
implementation isolation remain the coordinator's separate responsibilities.
The broader Tension draft, 41 excluded outputs, general behavior and arm64
correspondence remain unreleased or unknown.


## Prepared release finalization

The parent authorized metadata-only preparation for exact-byte local publication.
The approved staging manifest and case file are retained privately. Manifest
release status/date and the case file's top-level status are promoted to
`released` / `2026-10-19`; clean prose describes the reviewed local release.
This preparation does not publish it.

The [finalization check](../../analysis/ableton-live-12.4.3/handoff-staging/device-tension-v1-analysis/finalization-validation.json)
proves all 27 case/evaluation objects identical to the approved snapshot, and
byte identity for the comparator plus all 29 reference/signal files. The sole
case-file change is its top-level status. Final inventory, hashes and links pass,
and all four final clean Markdown documents were reread. Numerical tests were
not repeated because code, inputs, audio and criteria are unchanged.

Prepared release manifest SHA-256:
`02f9a0166bd6538ecfca0dcbebaad79b2397b14c75ca8a6608b5de618a1ffa3d`.
At this preparation checkpoint, copying and publication remained the
coordinator's next action. The completed publication is recorded below.

## Local publication

Released locally on 2026-10-19 as
[device-tension-v1](../../handoff/device-tension-v1/README.md), a byte-identical
copy of the separately reviewed final package. Manifest:
`02f9a0166bd6538ecfca0dcbebaad79b2397b14c75ca8a6608b5de618a1ffa3d`.
The coordinator reran `finalize_check.py`: case objects and all numerical
code/reference/signal files match the approved snapshot; only status/prose
metadata changed after the full 806-measurement and mutation/export checks.
The current release remains limited to 27 finite comparisons.

## Later analyst draft R4 — 2026-10-21

The [whole37 sensitivity observations and R4 annex](../research/device-tension-dsp.md#tension-owner-r4-sensitivity-annex-adoption--2026-10-21) are now reviewed and adopted on the analyst side. “Without their own retained calibration” above records the release-time exclusion; the new study does not itself accept calibration or a candidate comparator. Thirty-one proposed-margin annotations and six unresolved settings, including qualified historical estimator windows, remain outside device-tension-v1. Its 27 evaluations, four chaotic exclusions and immutable bytes are unchanged. No new release is selected.

## Unreleased R5 velocity observation annex — 2026-10-21

[Canonical R5](device-tension.md) includes the [reviewed 125-observation velocity annex](../research/device-tension-dsp.md#tension-owner-r5-velocity-annex-adoption--2026-10-21), plus three inherited references. The parent-launch pre-call custody gap and outer/raw fsync limits remain explicit; portable criteria/grades stay NULL. Old rows/R3/R4 objects and 37-setting sensitivity annex remain exact. Current v1 remains 27 calibrated evaluations; no new release or candidate comparison is selected.

## Unreleased R6 note-key observation annex — 2026-10-21

[Canonical R6](device-tension.md) adopts the [reviewed123-observation key annex](../research/device-tension-dsp.md#tension-owner-r6-note-key-annex-adoption--2026-10-21), retaining five inherited references and all old clauses/objects/criteria. The earlier velocity launch/fsync gaps remain explicit; portable criteria/grades stay NULL. Current v1 remains27 evaluations. No new release or candidate comparison is selected.

## Unreleased corrected R7 native-host observation annex — 2026-10-21

[Canonical R7](device-tension.md) applies the [sole-reviewed corrected composition](../research/device-tension-dsp.md#tension-owner-r7-native-host-annex-adoption--2026-10-21),106 new observation IDs /11 historical input references. The original uncorrected proposal remains frozen; only the external wording erratum plus reviewed composition is approved. Auxiliary host91=5 and all public-predicate claims stay ungraded, portable criteria/grades NULL; prior clauses/objects/criteria and v1's27 evaluations remain exact. No release/candidate comparison selected.

## Unreleased R8 finite MIDI observation annex — 2026-10-21

The [canonical draft](device-tension.md) applies the [sole-reviewed R8 annex](../research/device-tension-dsp.md#tension-owner-r8-midi-axis-annex-adoption--2026-10-21). These fixed native observations add no portable candidate criterion, general MIDI/public/ARM law or new release. Old criteria/U/history and immutable release scope remain exact; no candidate comparison selected.

## Unreleased R9 independent MIDI observation annex — 2026-10-21

The [canonical draft](device-tension.md) applies the [sole-reviewed R9 annex](../research/device-tension-dsp.md#tension-owner-r9-independent-midi-annex-adoption--2026-10-21). New fixed observations carry NULL portable criteria and no application proof. All earlier criteria, unknowns, history and immutable release scope remain exact. No new release or candidate comparison is selected.

## Unreleased R10 PARTIAL stepped observation annex — 2026-10-21

The [canonical draft](device-tension.md) applies the [sole-reviewed R10 annex](../research/device-tension-dsp.md#tension-owner-r10-partial-stepped-annex-adoption--2026-10-21):ONLY1388finite observations/full5350histories5364aliases/onequalifiedINPUTbaseline15aliases. Failed1/3960unattempted remainU withNOIDs/expectations/criteria/grades; completefalse. All15whole requirements/old cases/objects/criteria/history/releases exact. Failedrawfsyncskipped/parentresourcevaluesabsent/newportablecriteriaGradeNULL/appFalse. No retry/continuation/guardrelaxation/newrelease or candidate comparison is selected by this annex.

## Unreleased R11 finite observation adoption — 2026-10-22

The [R11 draft](device-tension.md) and [canonical adoption](../research/device-tension-dsp.md#tension-owner-r11-four-protocol-annex-adoption--2026-10-22) add 4 finite observation IDs. Earlier whole requirements, objects, criteria, unknowns, history and immutable releases remain exact. New portable expectations/comparators/grades are NULL; no release, candidate conformance or whole-product closure follows.

## Unreleased R12 opaque-return suffix annex — 2026-10-22

[Current R12](device-tension.md) adds3960finite native observations DTN2215–6174 after sole actual and sole new-owner composition reviews. All15whole requirements/old42rows/R3–R11objects/criteriaU/history and immutablev1scope27evaluations35inventory remain exact. New priors/native waveform expectations/portable criteria/grades NULL/appFalse;13quiet retained, no ABI/return-meaning/general0/1domain/publicARM/calibration law. No new release selected.
