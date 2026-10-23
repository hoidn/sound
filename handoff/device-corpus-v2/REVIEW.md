# Independent review disposition

Release: device-corpus-v2, reviewed 2026-10-19 Pacific / 2026-10-20 UTC.

Reviewer: Codex independent handoff reviewer. The reviewer did not author this
payload and will not implement the candidate in this analysis context.
Publication and final inventory metadata remain the coordinator's action.

## Scope approved

**Approved for the explicit finite scope** in [spec.md](spec.md) and
[cases.json](cases.json): 24 groups and 69 evaluations. The sole added evaluation
is CORPUS-AUDIO-020-02, mapped to parent DCO-029 under partial
REQ-DEVICE-CORPUS-011. All 68 earlier evaluation objects, histories and comparison
values, all 77 prior physical input/reference fixtures and the old measurement
rules are preserved. Requirements 002, 003 and 013 remain unreleased.

The extension grades one fixed Free Ramp Up audio vector using its own
engineering criterion: computed binary64 normalized waveform RMS error
inclusively at most 0.01 in EACH channel, over every frame 4096 through 16383.
Full-file finiteness, exact stereo binary32 length and positive active-window
reference and candidate energies are required. The [measurement tool](compare.py)
defines rounding and verifies the nominal Ramp reference's complete SHA-256.
No fitting, alignment, gain correction, alternate window or epsilon is allowed.

The older modal, Sine trajectory and startup criteria do not additionally grade
this new evaluation. Its finite prefix is not error-scored; aggregate RMS can
admit concentrated, onset or late-tail defects. These are explicit coverage
limits, not approval of those properties. No block, rate, reset, repeatability,
clock or floating-mode invariance is extended to this vector.

The 1% budget is an independently reviewed finite engineering acceptance choice,
not a recovered original tolerance, inaudibility threshold, architecture bound
or guarantee covering mixed mathematical-library errors. Two recorded coherent
substitution vectors fall below it; specified counterexamples exceed it.
The square-root comparison defines discrete evaluator rounding; the mathematical
1e-4 energy-ratio description does not replace it with a differently rounded test.

## Independent checks

- Read the full contract, role instructions, entry point and measurement code;
  checked the new complete vector and its exact 38 binary32 control values/order,
  signal, rate, blocks and histories against the retained capture protocol.
- Verified all staged inventory hashes at review entry, all published release 1
  payloads, the 68 unchanged old evaluation objects and all 77 old fixture bytes.
  Removing only the new branch, its hash import and reference gate reconstructs
  the old comparator byte-for-byte; the old tool was not executed.
- The dedicated Ramp branch exactly reproduces the separately reviewed pure
  method's scalar errors for nominal, both substitution vectors and the Sine
  contrast. Nineteen pure mathematical self-tests and 21 independent integration
  checks pass, including the inclusive 1% boundary and adjacent binary32 values,
  either-channel failure/silence, malformed/nonfinite files, both scored endpoints,
  explicitly ungraded finite prefix, reference identity and missing output.
- Exported the package outside the checkout with no analyst siblings or private
  helper imports. The newly staged comparator passes all 69 reference
  self-comparisons, totaling 4,603 measurements. A portable one-evaluation fixture
  also rejects a replaced reference and a missing candidate output. These are
  measurement tests, not executions of a candidate device.
- The package contains 69 reference files representing 62 distinct byte streams,
  nine mathematically generated input signals and only the newly authored
  measurement code. File types, local links and textual exclusions were checked;
  no symlinks, original executable, recovered code/pseudocode, private paths,
  restricted evidence links, shipped musical recording or project document is
  included. Python, NumPy and SciPy dependencies are explicit; availability does
  not authorize installation.
- Private records retain the pre-review manifest and exact pending review bytes,
  provenance, source-to-case trace and numerical results. The author's initial
  forward-link check failed before manifest creation; that attempt remains
  preserved. Link checking after manifest creation and the independent exported
  checks pass. No numerical capture or old payload was changed to resolve it.

## Provenance and limits

The reviewer previously approved the bounded nominal capture and finite
criterion; those supporting decisions are carried with their stated limits,
not represented as self-authored evidence or a fresh whole-device approval.
The separate sensitivity and owner integration approvals were also inspected.
Release 1's old finite approval is carried for unchanged objects; this review
freshly assesses the extension and package integrity.

Reference audio is extracted execution of original x86_64 device code under
recorded host inputs and substituted libraries. Arm64 correspondence remains
inferred. No original application, arm64 device, original-code collector or
candidate device ran during this review. A measurement pass establishes only
conformance to these finite comparisons. It does not establish an internal LFO
waveform/frequency law, a complete cycle or absence of a right-phase wrap,
Sync/Spin/random behavior, stored-value mapping, Live delivery, A1, all omitted
modal estimates, general sound equivalence or whole-device/product completion.

Release 1 remains immutable. This is a strict finite extension, not a regrading
of its exclusions or a general fidelity policy. A fresh restricted implementation
context is still required; this review does not authorize external publication,
source access by an implementer or tooling installation.
