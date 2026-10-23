---
id: PLAN-DEVICE-ANALOG-HANDOFF
type: research
status: draft
updated: 2026-10-22
access: analysis
target: Ableton Live 12 Suite 12.4.3 / macOS arm64; retained x86_64 device outputs
---

# Analog reviewed finite audio handoff

The reviewed local release was staged from [SPEC-DEVICE-ANALOG](device-analog.md),
using retained deterministic outputs and explicit comparison-domain vectors/events.
No original code was executed during staging or review. No recovered DSP or synthesis code
may enter the payload. A1/A2 remain open for Live integration; this package defines
only fixed device-level input/output comparisons.

## Staging plan

1. Verify the retained manifest, render hashes, exact captured vectors and events.
2. Copy deterministic outputs with no numerical alteration; reproduce silent input
   signals. Define fixed onset, envelope and eligible steady-harmonic windows.
3. Exclude random/statistical, unvalidated modulation trajectories, glide, unison
   and unrendered cases; omit unresolvable steady measurements explicitly.
4. Validate identity, missing/size/nonfinite rejection, per-channel silence/gain
   mutants and an isolated CLI export. Keep source hashes and coverage limits.
5. Stop candidate writes for separate review. No shared documentation, publication,
   application implementation, installation or commit is authorized here.

## Candidate scope

The candidate covers 38 groups, ANALOG-AUDIO-001 to 045 with explicit gaps,
and 42 evaluations. It carries draft DAN-001 to 011, 013 to 032, 037 to 042
and 045. Forty distinct retained WAV captures supply the samples; the two
block-size variants reuse the corresponding three-note chord reference.
Nine silent stereo inputs are generated, one per required capture length.

Excluded rather than silently graded:

- DAN-012: random/statistical noise; no distribution or spectral bound is invented.
- DAN-033 to 036: LFO, pitch-envelope and vibrato trajectories; their estimator
  windows/tolerances have not been independently calibrated for this candidate.
- DAN-043, 044, 046 and 047: glide, unison, unrendered envelope/LFO modes and
  other MIDI input.
- Parameter changes, general synthesis formulas, arbitrary input sets, Live
  integration and the stored-to-control mapping (A1/A2 remain open).

Only finite portions of REQ-001, 004 to 008, 011 to 017 and 023 are released.
The reference vectors have 203 independently named comparison components;
secondary flags and fixed envelope switches are project labels, without original
numeric indices or a claimed device API. They are not XML values. The original
capture's parameter order and rounded binary32 values are retained exactly.

The metric grades every channel's first nonzero frame, a final voice end only
when it falls inside the capture, selected 2,048-frame onset windows and 10 ms
RMS envelope windows above a fixed 60 dB threshold. It also freezes 24 stationary
windows: 21 frequency checks and 601 selected harmonic amplitudes per channel.
The frequency check is omitted below 100 Hz; three retained low-frequency windows
keep only harmonic/DC checks. No steady window is asserted for multi-note or
unselected time-varying output. Harmonic grading is narrowed to at most the first
40 harmonics below Nyquist, not the parent's open-ended spectrum criterion.

The original's short-waveform/envelope/library sensitivity observations motivate
the reviewed finite thresholds. They do not measure arm64 error or guarantee arbitrary
input compatibility. Independent review accepted the project metric only for the finite
comparisons. It supplies no general or arm64 tolerance bound. No draft precision error was found, so Analog stays revision 1.

## Evidence and provenance

Source run: [t12-analog-v1 manifest](../../analysis/ableton-live-12.4.3/r2/t12-analog-v1/manifest.json),
SHA-256 `88c406aa51a7609516bf332cc859ca4731d1cabbda03d418734e7438a5bdc40e`.
The source manifest and every listed retained artifact are checked before staging.
External N6 vector-table digests are checked against the source manifest too.
No original executable is copied or run.

The public reference files are little-endian stereo binary32. Every source WAV
was mono because the two original captured channels were bit-identical. Duplicating
that single channel reproduces the capture's retained **stereo f32 SHA-256** exactly;
there is no sample conversion, resampling, quantization or alteration. Container
bytes are omitted, and both the WAV and sample-byte hashes remain in private
traceability. All event lists and 203-component vectors are checked against the
retained per-render scripts. Input silence is reproduced as exact zero bytes.

The analyst companion
[device-analog-v1-analysis](../../analysis/ableton-live-12.4.3/handoff-staging/device-analog-v1-analysis/source-inventory.json)
contains 89 exact source paths/hashes/sizes in `source-inventory.json`, per-case
source/omission records in `traceability.json`, `build.py` for the numerical fixtures
and measurement eligibility, `compare_payload.py` for independent measurement only,
and `validate.py` for integrity/source/self/mutant/export checks. No recovered
instrument DSP, synthesis model or binary data structure is included in the payload.
Markdown was authored directly; the manifest seals its exact bytes.

## Validation

The author checks verify the exact manifest inventory, payload links, no symlinks/
bytecode/unlisted files, a deny scan for addresses/recovered identifiers/private paths,
all 137 retained manifest hashes, all external N6 table digests and 89 source-inventory
hashes. Every one of 42 vectors/event lists/sample captures is checked against its
retained script and stereo sample digest; all nine silence signals are regenerated.

The complete measurement tool also passes eight analytic-tone calibrations at both
rates (130.8, 261.6, 795.77 and 2118.569 Hz centers): maximum relative frequency
error 3.42e-9, harmonic amplitude and DC errors below 1e-8. This verifies measurement
arithmetic, not device compatibility or an arm64 error bound. See
[metric-calibration.json](../../analysis/ableton-live-12.4.3/handoff-staging/device-analog-v1-analysis/metric-calibration.json).

Final validation, 2026-10-19:

- All 42 self-comparisons pass, totaling 7,528 measurements. Per-channel silence,
  overall gain +2% and late-only gain +2% mutations are all rejected: 252 checks.
  Seven missing, wrong-length and non-finite output checks are rejected.
- The final isolated export runs the payload CLI with no analyst siblings:
  exit 0, all 42 evaluations pass. Its exact inventory contains no generated
  bytecode or other unlisted bytes. The export path is retained in the report.
- All 57 payload files have verified hashes/sizes. Total bytes excluding manifest:
  17,672,765. Manifest SHA-256:
  `b98157cd4cc77661f0755002318d8019789a51790138668ff721a50376f6e231`.
- Python 3.13.9, NumPy 2.3.1, SciPy 1.16.0, little-endian Linux. No tooling was
  installed and no original code was executed. `git diff --check` is clean.
- Selected vectors all have NoiseToggle, KeyboardError, VibratoToggle,
  VibratoError, both LFO toggles and PortamentoToggle off. Oscillator waveforms
  are 0, 1 or 2; random/statistical components are inactive, rather than assumed
  deterministic because of a fixed seed.

Retained report:
[author-validation.json](../../analysis/ableton-live-12.4.3/handoff-staging/device-analog-v1-analysis/author-validation.json).
All results are finite integrity and measurement checks. Whole-application
execution, arm64 execution and implementation compatibility remain unestablished.

## Independent review disposition

Independent review approved the finite contract with two clarifications: exact
first nonzero frame rather than “audible” onset, and explicit zero-based note
channels. Release metadata now consistently identifies a reviewed local release,
dated 2026-10-19. See the staged [REVIEW.md](../../analysis/ableton-live-12.4.3/handoff-staging/device-analog-v1/REVIEW.md).

The reviewer independently verified source identities, all vectors/events and
raw stereo sample hashes, 24 stationary windows, 21 frequency checks and 601
selected harmonics per channel using a separate complex least-squares basis.
Three additional analytic estimator checks passed. The comparator, all 42
reference files (40 distinct captures) and all nine input signals are byte-identical
to the original candidate. The entire cases object is identical except its top-level status.
The original manifest and exact comparison record are retained in
[review-promotion-invariance.json](../../analysis/ableton-live-12.4.3/handoff-staging/device-analog-v1-analysis/review-promotion-invariance.json).
The final prose was reread after metadata promotion.

No implementation workspace has been provisioned. Copying the reviewed release,
shared index/coverage/questions/log updates and commits remain outside this
worker's scope. These checks are not application compatibility proof.

## Reviewed local publication — 2026-10-19

Independent reviewer `collision_recovery` approved the finite metric and scope,
with exact-nonzero onset and zero-based event-channel clarifications. Every
203-component vector/history and source identity was checked. Independent
complex-exponential least squares confirmed all 601 harmonic masks; three
additional analytic signals checked frequency, harmonic amplitude and DC.
The final seal contains 57 payload files, 17,672,765 bytes excluding manifest:
`b98157cd4cc77661f0755002318d8019789a51790138668ff721a50376f6e231`.

Final 42 self-comparisons/7,528 measurements, 252 mutations, seven invalid files
and isolated export passed after status promotion. Numerical case objects,
comparison code and signal/reference bytes were preserved across final prose
and metadata edits. The earlier candidate pin above is historical, not the
published pin. See the immutable [review](../../handoff/device-analog-v1/REVIEW.md).
Noise, uncalibrated modulation, glide/unison and general protocol remain excluded.
No application implementation or arm64 execution was performed.

## Unreleased R4 velocity observation annex — 2026-10-21

[Canonical R4](device-analog.md) now includes the [reviewed velocity annex](../research/device-analog-dsp.md#analog-owner-r4-velocity-annex-adoption--2026-10-21): 127 native-observation IDs, one inherited control and NULL portable comparators/grades. Existing v1 remains 38 groups / 42 evaluations. No new release or candidate comparison is selected; prior release bytes and broader U remain unchanged.

## Unreleased R5 note-key observation annex — 2026-10-21

[Canonical R5](device-analog.md) includes the [reviewed 127-case note-key annex](../research/device-analog-dsp.md#analog-owner-r5-note-key-annex-adoption--2026-10-21), with inherited key60 and all prior criteria/rows/R3/R4 objects preserved. Portable waveform comparators/grades remain NULL; the high-key hash coincidence supplies no pitch/clamp law. Current v1 remains 38 groups / 42 evaluations; no new release or candidate comparison is selected.

## Unreleased R6 channel observation annex — 2026-10-21

[Canonical R6](device-analog.md) includes the [reviewed fifteen-channel annex](../research/device-analog-dsp.md#analog-owner-r6-channel-annex-adoption--2026-10-21), with inherited channel0 and all prior clauses/rows/R3/R4/R5 objects/criteria preserved. Portable comparators/grades remain NULL. Current v1 remains38groups/42evaluations; no new release or candidate comparison is selected.

## Unreleased R7 observation annex — 2026-10-21

[CanonicalR7](device-analog.md) adopts the [sole-reviewed finiteannex](../research/device-analog-dsp.md#analog-owner-r7-release-velocity-annex-adoption--2026-10-21):127newrelease-velocity observations/full128catalog; v1remains38groups/42evaluations. Priorclauses/objects/criteria and broaderUremainexact. Portablecriteria/gradesNULL; no newrelease or candidatecomparison selected.

## Unreleased R8 finite host observation annex — 2026-10-21

The [canonical draft](device-analog.md) applies the [sole-reviewed R8 annex](../research/device-analog-dsp.md#analog-owner-r8-combined-host-annex-adoption--2026-10-21). New observation navigation does not supply portable candidate criteria or close public/ARM/history unknowns. Existing immutable release, criteria and scope remain exact; no new release or candidate comparison selected.

## Unreleased R9 independent MIDI observation annex — 2026-10-21

The [canonical draft](device-analog.md) applies the [sole-reviewed R9 annex](../research/device-analog-dsp.md#analog-owner-r9-independent-midi-annex-adoption--2026-10-21). The284 new finite observations add no portable criterion, application proof or release. All earlier clauses/rows/catalogs/criteria/history and immutable v1 scope remain exact; candidate comparison remains unselected.

## Unreleased R10 converted virtual-enum observation annex — 2026-10-21

The [canonical draft](device-analog.md) applies the [sole-reviewed R10 annex](../research/device-analog-dsp.md#analog-owner-r10-converted-virtual-enum-annex-adoption--2026-10-21),193finite observations/full198aliases194histories/one qualified INPUT reference5aliases. All23whole requirement bodies/old rows/objects/criteria/U/history/releases remain exact; only annex/revision change. Mandatory erratum/all amounts0.5/coupledPoly/fourtarget axes do not prove MPE dormancy/no-effect/productivity/voicecapacity. New portablecriteria/gradesNULL/appFalse; no new release or candidate comparison selected.

## Unreleased R11 secondary protocol observation annex — 2026-10-21

The [canonical draft](device-analog.md) applies the [sole-reviewed R11 annex](../research/device-analog-dsp.md#analog-owner-r11-secondary-protocol-annex-adoption--2026-10-21), adding five draft observations with the complete six-history/seven-alias mapping. Prior whole requirements, objects, criteria, unknowns, error history and immutable v1 scope remain exact. The baseline is INPUT-only and new portable criteria/grades are NULL; there is no general rate/block invariance or new release/candidate comparison. The linked adoption owns the context, custody and method qualifications.

## Unreleased R12 finite observation adoption — 2026-10-22

The [R12 draft](device-analog.md) and [canonical adoption](../research/device-analog-dsp.md#analog-owner-r12-partial-multi-note-annex-adoption--2026-10-22) add 4 finite observation IDs. Earlier whole requirements, objects, criteria, unknowns, history and immutable releases remain exact. New portable expectations/comparators/grades are NULL; no release, candidate conformance or whole-product closure follows.

## Unreleased R13 four-control observation annex — 2026-10-22

[Current R13](device-analog.md) adds four DAN1190–1193 with two raw-byte/hash DIFFER comparisons, descriptive only. All23wholeREQ/oldobjects/72literalrows/criteriaU/history and immutable v1 scope38groups42evaluations remain exact. New priors/native waveform expectations/portable criteria/grades NULL/appFalse; no residual, capacity/release law or new release.
