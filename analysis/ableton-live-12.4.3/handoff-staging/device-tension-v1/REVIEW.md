# Review disposition

Package: device-tension-v1. Date: 2026-10-19.
Reviewer: a handoff-review context separate from the Tension candidate author.
The reviewer will not implement this contract.

**Approved with finite scope.** Accept only the
27 enumerated comparisons: 26 stable settings and one repeated-strike output.
Partial requirements 001 and 004 through 012 carry only the cases' exact
protocol-conditioned outputs and listed measurements. Every other setting,
requirement clause and unmeasured mode remains outside this approval.

## Independent checks

- Verified all 161 original evidence payloads, external source identities and
  both executable slices without executing original device code.
- Matched each full 129-component binary32 vector, its order, note events,
  rate, zero input, absent-input convention, single processing interval,
  512-frame blocks and zero warm-up to its retained input record.
- Matched all mono reference bytes to their IEEE-float WAV data chunks.
  Duplicating each mono sample to stereo also reproduced the recorded digest
  of its original output, confirming the identical-channel reduction.
- Checked every selected setting's five retained sensitivity variants against
  the exact frozen eligibility, centers, cutoff, windows and strongest-reference
  amplitude normalization. Stable maximum errors are 0.000595103 held waveform,
  0.002291776 release waveform, 4.669726e-7 relative frequency, 0.000141588
  relative log radius and 0.000111182 normalized complex amplitude. All are
  within the approved 0.003, 0.01, 2e-6, 6e-4 and 5e-4 limits. Every onset is
  unchanged. Repeated-strike whole-window error 0.001144768 is below 0.005;
  no partial measurements are approved for that case.
- Independently exercised each numerical boundary with generated test signals
  at 90% and 110% of its bound, including the three waveform limits and three
  partial limits. The relevant checks accept the lower and reject the upper.
  Added and tested explicit guards for empty/nonfinite/mismatched mono arrays,
  invalid waveform windows and empty required stable-partial lists.
- Rechecked all reference self-comparisons, every-case silence, doubled-gain
  and early-impulse mutations, malformed/nonfinite/length/missing files,
  exact inventory and hashes, payload links, no symlinks, source exclusion
  and the comparator CLI from an export without analyst siblings.

The comparison code measures signals only. Public control/document names and
independently named numerical components identify finite comparison inputs;
they prescribe no application API or internal implementation. No executable,
recovered synthesis algorithm, original source, private path, analysis transcript
or original musical recording is part of the payload. The synthetic-note output
captures are accepted as behavioral fixture outputs for this local handoff.

## Corrections and limits

The reviewer added measurement input and nonvacuity guards; no audio, vector,
event, selected partial, window or tolerance changed. The original proposal's
numerical criteria are accepted only as fixed-scope project criteria.

The five-variant calibration is retained as measurements; its perturbed audio
is not retained for independent recomputation. It is an x86_64 sensitivity
study, not an arm64 error bound. Four chaotic settings and 37 outputs without
per-setting calibration stay excluded. No broad statistical substitute was
accepted. No original application, arm64 or independent candidate renderer ran.
Self-comparison and synthetic measurement tests establish tool behavior only.
This partial package does not complete Tension, all five devices or T1.

Use this release only in a restricted implementation workspace. Preserve its
bytes; corrections need a new reviewed release.
