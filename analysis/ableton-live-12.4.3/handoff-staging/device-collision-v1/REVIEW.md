# Review disposition

Release: device-collision-v1, 2026-10-19.
Reviewer: coordinator in a handoff-review context separate from the candidate
and Collision draft authors. The reviewer will not implement this contract.

**Approved with finite scope.** Two output comparisons only: disabled-resonator
effective silence and the listed 44.1 kHz Pipe render. Partial requirements
001, 002, 003 and 014 have only the scope stated in the contract. All other
requirements and all other parameter/event/rate combinations remain unreleased.

## Independent checks

- Re-read the prior source calibration: the exact Pipe setup's two-sided
  mathematical-library perturbations give whole-window relative RMS
  0.0005140501 and 0.0006108613. Accept 0.003 for this fixed project comparison;
  it is not an arm64 or arbitrary-seed portability bound. The constructor's
  tiny residual supports the separate effective-silence criterion.
- Independently checked all 139 binary32 inputs per case against the retained
  capture scripts, their exact event sequences, 11,264-frame warm-up and
  fixed partitions. Both WAV data chunks equal the package reference bytes
  exactly, with their lengths, rate, channels and floating-point form checked.
- Independently checked comparator source and numeric boundaries: self
  comparisons pass; Pipe silence, channel mute, sign reversal and gain error
  above the 0.003 boundary fail. Gain error just below the boundary passes.
  For the constructor, zero is correctly accepted and audible injection fails.
- Verified payload hashes, sizes, exact inventory, links, no symlinks and
  source exclusion. The code is standard-library signal measurement only;
  no audio synthesis or recovered application algorithm is present. Control
  labels and exact vectors are comparison inputs, not an original API claim.
- An export copied outside the checkout passes its CLI comparisons without
  analyst files. Deleting one output causes a failing exit status and report.
  The author's additional malformed/nonfinite/size controls also pass review.

The original source packet has two concurrently changed paths. Separate
exact-hash recovered originals and unchanged WAV/script captures support this
release; the concurrent additions are excluded. The clean package depends on
neither analyst paths nor that incident's unreviewed bytes.

## Clarifications and exclusions

Draft case identifiers were replaced by release identifiers before approval.
Input availability and processing history are explicit comparison conventions,
not a prescribed application interface. A silence case cannot reject a change
that remains below its declared peak bound; tests correctly retain that result.

Modal outputs, noise, Tube and pitch-envelope coverage are deferred. Missing
calibration was not replaced with a wider arbitrary tolerance. This release
does not complete Collision, the five-device workstream or T1. No original
application, arm64 executable or independent candidate renderer ran. Passing
reference self-comparisons establish comparison plumbing only.

Preserve this reviewed local release unchanged; corrections need a new release.
