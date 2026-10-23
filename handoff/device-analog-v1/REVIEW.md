# Independent review disposition

Release: device-analog-v1, reviewed and locally released 2026-10-19.

Reviewer: Codex analyst/handoff-review agent `collision_recovery`, separately
assigned from the author. The reviewer did not author this candidate and will
not implement it. The reviewer owns the clarifications and review metadata below.

## Scope

Approval is limited to the explicit finite clauses of REQ-DEVICE-ANALOG-001,
004 to 008, 011 to 017 and 023 in [the contract](spec.md). The 38 groups contain
42 evaluations, supplied by 40 distinct retained captures and nine generated
silent signals. No general synthesis, mapping, allocation, controller,
automation or original-application integration contract is approved.

## Independent checks

- Exact evidence identity: the retained source inventory and capture hashes
  matched, including both executable slice identities and numerical parameter
  tables. No original code was run during review.
- Every 203-component vector, its names/order and binary32 values, note-event
  list, block size, rate, silent-input history and captured frame count matched
  the retained capture records and scripts. The control vectors keep random
  noise, pitch errors, vibrato, both LFOs and glide inactive. Their oscillators
  use the three non-random shapes. Two block variants reuse a base capture
  only where the retained comparison records bit identity.
- Expanding each mono capture into two identical channels reproduced its
  original captured stereo sample digest exactly. This was checked against
  the stereo digest, without assuming that mono implies identical channels.
  No sample rescaling, conversion or resampling was introduced.
- Measurement eligibility: all 24 stationary windows satisfy the required
  length and period count. The 21 frequency windows lie at or above 100 Hz.
  All 601 selected harmonic amplitudes per channel were independently
  reselected using a complex-exponential least-squares basis; that selection
  agrees with the tool's real sine/cosine basis. Counts, the first-40 cap and
  frozen windows agree with the contract. Low-frequency checks and omitted
  modes remain excluded rather than receiving a pass.
- The full executable comparison algorithm was read. It measures exact
  nonzero onset, optional voice end, 59 onset windows per channel, fixed RMS
  envelope eligibility, specified steady frequencies and harmonic/DC values.
  No candidate-dependent time alignment, gain normalization or eligibility
  selection is allowed. Missing/unmeasurable results fail.
- The author's analytic calibration was inspected. Three additional
  independently chosen analytic signals recovered frequency, fundamental/
  third-harmonic amplitude and DC, with maximum relative frequency error
  below 6.4e-10 and amplitude/DC errors below 1e-8. These tests verify the
  signal estimator only. Library-perturbation evidence motivates the finite
  project metric; it establishes no arm64 or arbitrary-input error bound.
- The full 42-output self comparison passed with 7,528 checks. Every per-channel
  silence, +2% overall-gain and +2% late-gain mutation was rejected (252 tests).
  Seven malformed, non-finite or missing-output checks were rejected. Exact
  payload hashes/sizes, local links, source-exclusion scan and an isolated
  package's comparator CLI were checked. The exported package requires only
  its own files and the stated installed numerical libraries.

## Findings

| ID | Finding | Resolution |
| --- | --- | --- |
| ANR-01 | The partial timing clause said first “audible” frame, while the executable criterion is the first sample unequal to exact zero. | Corrected to first nonzero frame; no numerical expectation changed. |
| ANR-02 | Event channel numbering was present numerically but its base was implicit. | Contract now specifies zero-based channels 0–15, using 0 in these evaluations; captured event bytes are unchanged. |
| ANR-03 | Candidate status prose needed to agree after review. | README, role instructions, contract, cases status and manifest now consistently identify the reviewed local release. A fresh restricted implementation workspace remains required. |

## Disposition

**Approved with the listed clarifications**, only for the finite inputs and
measurements in this package. The project metric is accepted for those finite
comparisons. Unmeasured properties and excluded inputs remain unknown.

Reference outputs came from earlier extracted x86_64 original-code execution
with substituted libraries. Neither the whole application nor an arm64 device
was run, and no independent candidate application has been compared. A metric
self-test proves comparison behavior, not application compatibility or clean
workspace isolation. This disposition authorizes no external publication;
external distribution and provision of a restricted implementation workspace remain separate steps.
