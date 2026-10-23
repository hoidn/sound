---
id: PLAN-DEVICE-COLLISION-HANDOFF
type: research
status: current
updated: 2026-10-22
access: analysis
target: Ableton Live 12 Suite 12.4.3 / macOS; retained x86_64 extracted outputs
---

# Collision finite audio handoff candidate

The two-case [device-collision-v1](../../handoff/device-collision-v1/README.md) was released locally on 2026-10-19 under
[SPEC-DEVICE-COLLISION](device-collision.md) revision 1. It covers the constructor
silence boundary and one calibrated Pipe render. It is approved only for that finite scope by a separate candidate-review context. It does not complete Collision, all
five devices or T1 audio. The original application and arm64 were not executed,
and no candidate renderer exists in this work.

## Scope and selection

| Cases | Partial requirements | Proposed acceptance |
| --- | --- | --- |
| DCL-001 → DEVICE-COLLISION-001 | REQ-DEVICE-COLLISION-001, 002, 003 | Exact retained constructor vector/events, 22,050 stereo frames at 44.1 kHz; peak ≤ 10⁻¹⁸ |
| DCL-031 → DEVICE-COLLISION-002 | REQ-DEVICE-COLLISION-001, 014 | Exact retained Pipe vector/events, 32,768 stereo frames at 44.1 kHz; whole-window joint stereo relative RMS ≤ 0.003 |

The [clean payload](../../analysis/ableton-live-12.4.3/handoff-staging/device-collision-v1/README.md)
contains all 139 named binary32 parameter values per case, exact event records,
fixed 512-frame partitions and 11,264-frame warm-up, reference output data,
measurement-only comparator, contract, scoped instructions and manifest.
RIFF IEEE-float data chunks were copied verbatim to headerless f32 files with
recorded hashes. No recovered code, synthesis algorithm or internal identifiers
are included in that payload. Independent semantic review subsequently approved
this finite package (outcome below). Stored-value conversion and original host
integration remain excluded.

[Collision research](../research/device-collision-dsp.md#evidence-and-recovery)
owns evidence provenance and the two-path concurrent-edit recovery. Packaging
verified all 103 original payload hashes through that mapping; no current or
recovered original bytes were modified. Only recovered-original `collision.json`
was read, excluding unknown-provenance extras. The
[analyst companion](../../analysis/ableton-live-12.4.3/handoff-staging/device-collision-v1-analysis/README.md)
records exact source/output digests, mapping, private reproduction scripts and
calibration locators. It must not be exported to an implementer.

## Metric decision proposed for review

Pipe's exact retained setup has prior whole-window stereo relative RMS library
perturbation measurements 0.0005140501236040379 and 0.0006108612471224301.
The proposed 0.003 bound uses that same full `[0, 32768)` window and does not
fit away gain or alignment. The disabled-resonator capture peaks around
4 × 10⁻²²; its proposed absolute 10⁻¹⁸ boundary accepts effective silence.
The original measurements are retained in `results/libm_sensitivity.json:pipe`
and `results/collision.json:root_cause`, using the recovery mapping above.
Perturbed audio is not retained; arm64 and arbitrary-seed bounds are unknown.

Every other case is deferred. In particular modal complex-amplitude/log-radius
portability calibration is missing; the candidate cannot substitute static model
residuals for that experiment. Zero-resolved-mode DCL-014, noise, Tube and pitch
envelope are ungraded here. No mode rows or frequency-only comparator are used;
no empty mode selection can become a pass. General event-grid, pitch, gain,
voice, modulation, parameter-transition, persistence, malformed-device-input,
UI and real-time contracts remain outside this candidate.

## Author verification

The [retained author report](../../analysis/ableton-live-12.4.3/handoff-staging/device-collision-v1-analysis/author-validation.json)
records both reference self-comparisons passing, audible Pipe silence and ×2 gain
mutations failing, and every-case malformed/NaN/±infinity/wrong-length rejection.
DCL-001 valid silence and ×2 inaudible residual correctly pass its absolute peak
criterion; introduced audible output fails. Missing candidate files fail via the
CLI. Both CLI self-comparisons pass from a copied export without analyst siblings,
using only Python's standard library. Exact inventory, hashes, local payload links
and source-token exclusion checks passed. These results validate measurement
plumbing only, not original-versus-candidate compatibility or enforceable
implementation isolation.

Focused lint covers this plan's frontmatter/local links and staged payload
links/inventory. The parent coordinator owns the shared index, coverage, questions
and append-only log updates. Full repository lint and publication are deferred
to the separate review/release stage; no source regeneration, install, commit or
publication occurred during staging.

## Review outcome

Approved with finite scope and released locally on 2026-10-19; see the
[review](../../handoff/device-collision-v1/REVIEW.md). The coordinator, separate
from both authors, independently rechecked 278 binary32 values, both event and
processing sequences, lossless WAV data extraction, metric boundaries, malformed
output controls, source exclusion and isolated CLI behavior. Final manifest:
`c1ea731dcee088f9c6a64d786ddf2d36ad84a7799aba0af59b961dfb024d7da2`.
The candidate instructions and proposed metric discussion above record staging;
only the released contract governs the two accepted cases. No other Collision
case or compatibility dimension gained a pass.

## Unreleased R3 finite observation annex — 2026-10-21

The [canonicaldraft](device-collision.md) applies the [sole-reviewed R3 annex](../research/device-collision-dsp.md#collision-owner-r3-finite-kind3-annex-adoption--2026-10-21). Fixed native observations add no portable candidate criterion, general public/ARM/calibration law or release. All prior criteria/U/history and immutable release scopes remain exact; candidate comparison remains unselected.

## Unreleased R4 independent MIDI observation annex — 2026-10-21

The [canonical draft](device-collision.md) applies the [sole-reviewed R4 annex](../research/device-collision-dsp.md#collision-owner-r4-independent-midi-annex-adoption--2026-10-21). New fixed observations carry NULL portable criteria and no application proof. All earlier criteria, unknowns, history and immutable release scope remain exact. No new release or candidate comparison is selected.

## Unreleased R5 five-axis observation annex — 2026-10-21

The [canonical draft](device-collision.md) applies the [sole-reviewed R5 annex](../research/device-collision-dsp.md#collision-owner-r5-five-axis-annex-adoption--2026-10-21),523 finite native observations/full528aliases524histories. New portable criteria/grades remain NULL with no application proof; prior unknowns, failures, criteria, objects, history and immutable release scope remain exact. No new release or candidate comparison is selected.

## Unreleased finite owner adoption — 2026-10-21

CollisionR6 partialannex adds124IDs; failed1U131unlaunchedU remain unnumbered/noexpectationsgrades; oldclausescriteriahistory/releases exact/portablecriteriaNULL/no continuation. No new release selected.

## Unreleased R7 finite observation adoption — 2026-10-22

The [R7 draft](device-collision.md) and [canonical adoption](../research/device-collision-dsp.md#collision-owner-r7-stiffness-annex-adoption--2026-10-22) add 128 finite observation IDs. Earlier whole requirements, objects, criteria, unknowns, history and immutable releases remain exact. New portable expectations/comparators/grades are NULL; no release, candidate conformance or whole-product closure follows.
