---
id: PLAN-DEVICE-ELECTRIC-HANDOFF
type: research
status: current
updated: 2026-10-22
access: analysis
target: Ableton Live 12 Suite 12.4.3 / macOS arm64; retained x86_64 extracted renders
---

# Electric finite audio handoff candidate

Released locally on 2026-10-19 as
[device-electric-v1](../../handoff/device-electric-v1/README.md), from
[SPEC-DEVICE-ELECTRIC revision 2](device-electric.md), approved for its finite
117 mono outputs by a separate candidate-review context.
No original device code was executed during staging. No Live integration or
arm64 execution is claimed.

## Finite scope

The payload holds 117 case/evaluation pairs, each with a complete 33-name
binary32 comparison-domain vector, explicit ordered note events, zero input,
sample rate, 512-frame block partition, warm-up and any parameter-change history.
Exact mono binary32 reference samples are copied from retained generated-note
renders without changing sample bytes. Measurement code is independently
authored signal analysis only, with no device synthesis or recovered DSP code.

Only finite output portions of REQ-001, 005 to 012, 014 and 015 are proposed.
REQ-002, 003, 004, 013 and 016 remain unreleased, as do general formulas and
unlisted combinations. First-onset windows are finite comparisons, not a release
of the general event timing law. There is no stored-value or original-API claim.

Exclude original cases `p04_0`, `p05_1_key36`, `p05_1_key84`: fewer than half of
their loud envelope windows survived the original variant eligibility threshold.
Other cases grade only the masks frozen in the retained results, not every window,
band, partial or tail. The random waveform and random-component level are excluded;
additional seed audio was not retained. No statistical tolerance was enlarged to
admit them. The exact-silence case stays exact rather than using logarithmic floors.

The proposed comparison fixes every frame boundary, band edge, harmonic center,
FIR length/window, phase/log-magnitude fit, reference value and mask. Four clock
variants and two one-ulp library variants established the retained eligibility
and tolerance values. This is evidence for a finite project criterion, not a
measured bound on arm64 or a whole-application compatibility result.

## Evidence and provenance

Source [t12-electric-v1 manifest](../../analysis/ableton-live-12.4.3/r2/t12-electric-v1/manifest.json):
all 262 listed payload hashes and byte counts match. Staging also checks the
external executable and both slices, numerical-name table, Defaults preset and
every preset source listed there. For every included output, the 33 initial
parameter values, note timestamps (subtracting warm-up) and total process length
are checked against its retained script and result record. No source capture,
manifest or published payload was edited.

The [analyst companion](../../analysis/ableton-live-12.4.3/handoff-staging/device-electric-v1-analysis/traceability.json)
keeps source case names, WAV/script hashes, exact raw-output hashes, metric source
locators and exclusions. `source-inventory.json` preserves the original inventory
and identities. `build.py` performs the read-only audits and copies exact data;
`seal.py` inventories the current candidate; `validate.py` checks the package and
comparison behavior. `environment.json` records numerical-library versions.

## Author validation

Commands, from the repository root:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 -I analysis/ableton-live-12.4.3/handoff-staging/device-electric-v1-analysis/build.py
python3 -I analysis/ableton-live-12.4.3/handoff-staging/device-electric-v1-analysis/seal.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 -I analysis/ableton-live-12.4.3/handoff-staging/device-electric-v1-analysis/validate.py
```

Author checks passed: all 117 self comparisons (9,423 measurements), 351
silence/gain/early-impulse mutations, seven missing/invalid-length/non-finite
file checks, payload hashes/sizes, source-exclusion scan, local links and a
standalone copy outside the analyst checkout. The isolated comparator CLI
passes against its own reference directory using only the exported package
and installed numerical libraries. These are author checks, not independent
review, original execution, application compatibility or proof of access isolation.

Results: `author-validation.json` and `isolated-self-comparison.json` in the
analyst companion. A gain mutation doubles sounding output (+6.02 dB); silence
evaluations instead receive a nonzero sample. Thus silence does not masquerade
as a successful gain mutation of an unchanged zero signal.

## Original review gate (author staging record)

At staging, independent review was required to verify scope, reference sharing/provenance, numerical
measurements, calibration limits, source exclusion and the isolated package.
Unmeasured portions could not be inferred to pass. The original candidate was
`staged-unreviewed` with pending reviewer disposition. The outcomes below record
subsequent review and publication; no implementation workspace was provisioned.

## Review outcome

[Approved with finite scope](../../handoff/device-electric-v1/REVIEW.md),
then released as a byte-identical reviewed package. Independent checks verified
3,861 parameter values, all events/history/sample bytes, 7,908 calibrated
envelope/band values and 1,284 partial values (maximum difference 1.81e-11),
plus comparator boundaries and exclusions. Coordinator reran the final validation:
117 self comparisons / 9,423 measurements, 351 mutations, seven invalid files
and isolated CLI passed. Final manifest:
`1f4e84947bf1ffa9fd605f73381a9778ad8ab4af1b6f9e14662458d606e0dd4f`.
Polarity and complete waveform/phase equality remain ungraded, as do omitted
random/unstable portions. The staging steps above are historical preparation.

## Editorial supersession: Electric v2

[device-electric-v2](../../handoff/device-electric-v2/README.md) supersedes v1
on 2026-10-19 solely to correct the contradictory final permission sentence
introduced by the coordinator during v1 metadata promotion. V1 stays immutable.
The separate reviewer verified all 129 predecessor payload hashes/sizes: 126
files unchanged; only README, spec and review differ, plus manifest metadata.
All numerical code, cases, inputs, outputs, thresholds and exclusions are
identical. Three representative isolated comparisons pass. The coordinator
reran the retained editorial review check before publication. Current manifest:
`c53a829a459bba8a32311b3f537adc54607e2d05c0b2182ed007012b34591273`.
The [review](../../handoff/device-electric-v2/REVIEW.md) accepts only this
editorial supersession and inherits the unchanged finite numerical review.

## Unreleased R4 transpose observation annex — 2026-10-21

[Canonical R4](device-electric.md) includes the [reviewed 22-observation transpose annex](../research/device-electric-dsp.md#electric-owner-r4-transpose-annex-adoption--2026-10-21), plus three inherited references. All prior rows/R3 objects/pair relations and released 117 evaluations remain exact. Portable waveform comparators/grades remain NULL; no new release or candidate comparison is selected.

## Unreleased R5 observation annex — 2026-10-21

[CanonicalR5](device-electric.md) adopts the [sole-reviewed finiteannex](../research/device-electric-dsp.md#electric-owner-r5-note-key-annex-adoption--2026-10-21):127newkey observations/full128catalog; v2remains117evaluations. Priorclauses/objects/criteria and broaderUremainexact. Portablecriteria/gradesNULL; no newrelease or candidatecomparison selected.

## Unreleased R6 velocity observation annex — 2026-10-21

[Canonical R6](device-electric.md) adopts the [reviewed127-observation velocity annex](../research/device-electric-dsp.md#electric-owner-r6-velocity-annex-adoption--2026-10-21), with100 inherited by reference and all prior clauses/objects/criteria retained. Portable expected outputs/comparators/grades remain NULL; no zero-note dispatch or general velocity law is newly validated. Current v2 remains117 evaluations; no new release or candidate comparison is selected.

## Unreleased R7 finite MIDI observation annex — 2026-10-21

The [canonical draft](device-electric.md) applies the [sole-reviewed R7 annex](../research/device-electric-dsp.md#electric-owner-r7-combined-host-and-midi-annex-adoption--2026-10-21). These fixed native observations add no portable candidate criterion, general MIDI/public/ARM law or new release. Old criteria/U/history and immutable release scope remain exact; no candidate comparison selected.

## Unreleased R8 finite observation annex — 2026-10-21

The [canonical draft](device-electric.md) applies the [sole-reviewed R8 annex](../research/device-electric-dsp.md#electric-owner-r8-independent-midi-annex-adoption--2026-10-21). New fixed native observations carry NULL portable criteria/grades and no application proof. Earlier criteria, unknowns, objects, history and immutable release scope remain preserved. No new release or candidate comparison is selected.

## Unreleased R9 observation annex — 2026-10-21

The [canonical draft](device-electric.md) applies the [sole-reviewed annex](../research/device-electric-dsp.md#electric-owner-r9-pickup-controller-annex-adoption--2026-10-21), adding 256 draft navigation IDs with NULL new portable criteria and grades. All prior whole requirements, cases, objects, criteria, unknowns, history and immutable release scope remain exact. The linked adoption owns the input, custody and method limitations. No new release or candidate comparison is selected.

## Unreleased R10 load and omission observation annex — 2026-10-21

The [canonical draft](device-electric.md) applies the [sole-reviewed R10 annex](../research/device-electric-dsp.md#electric-owner-r10-load-and-omission-annex-adoption--2026-10-21):124new navigation IDs/full124histories62pairs. Earlier whole clauses, objects, criteria, unknowns, history and immutable v2scope remain exact. Pair differences establish no capacity/stealing/residual criterion; new portable criteria and grades are NULL. New FDfsync requests retain their separate scope. No new release or candidate comparison is selected.

## Unreleased R11 finite observation adoption — 2026-10-22

The [R11 draft](device-electric.md) and [canonical adoption](../research/device-electric-dsp.md#electric-owner-r11-seven-protocol-annex-adoption--2026-10-22) add 7 finite observation IDs. Earlier whole requirements, objects, criteria, unknowns, history and immutable releases remain exact. New portable expectations/comparators/grades are NULL; no release, candidate conformance or whole-product closure follows.
