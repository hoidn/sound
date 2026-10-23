# Review disposition

Release: device-corpus-v1, 2026-10-19.

Reviewer: Codex independent handoff-review agent, in a separate review context.
The reviewer did not author the candidate and will not implement the application.
This review covers scope, source fidelity, the numerical comparison procedure,
sharing suitability, sanitization and a package export outside the checkout.
Publication remains the coordinator's action.

## Scope approved

Approval is limited to the finite clauses of REQ-DEVICE-CORPUS-001 and
REQ-DEVICE-CORPUS-004 to 012 in [the contract](spec.md): 24 groups and 68
evaluations. Requirements 002, 003 and 013 remain unreleased. No general
synthesis formula, stored-value mapping or application integration is approved.
The named parameter vectors are explicit project comparison inputs, with the
order and exact binary32 values stated; they impose no candidate architecture.

The fixed protocol is accepted as a test convention. No assumption that Live
uses it in general is accepted. Stored position conversion remains unresolved;
position cases operate directly on their named comparison-domain values.
Neither the original application nor the arm64 executable was run. Reference
outputs are previous extracted execution of the x86_64 device with substituted
Linux libraries. Their correspondence with arm64 remains inferred.

## Independent checks performed

- All 68 vectors, parameter orders, input signals, rates, frame counts, reference
  bytes and history actions agree with the retained source evidence. The seven
  block/rate/reset variants are supported by their retained comparison results.
  Every reference hash is full length and equals its source output's digest.
- All 287 files in the source manifest were re-hashed, as were the Corpus
  bundle and its x86_64 image. They agree with their recorded identities.
  Source inventory entries were also checked. The parent draft at staging is
  retained separately so later draft corrections do not erase its exact bytes.
- The 1,427 listed mode/channel/evaluation occurrences and all 174 omitted
  occurrences reproduce the retained eligibility decisions and cutoff values.
  Every graded channel has a nonempty frozen mode list. An independent linear
  fit parameterization refits all 1,427 graded occurrences from the output
  samples. Its largest frequency difference from the retained estimate is
  below 6e-11 Hz, and its largest per-frame log-radius difference is below
  6e-15. Omitted or unresolved modes are never promoted to passes.
- The measurement code was read in full against the written procedure. It
  analyzes samples only and contains no device synthesis. Synthetic probes
  exercise accepted and rejected waveform errors, sine gain and phase errors,
  noise-band errors, LFO frequency shifts, startup timing, modal frequency
  bounds and log-radius bounds. A separately computed modal fit also agrees
  with the tool's complex amplitude. Non-finite or unmeasurable results fail.
- The existing validation suite was rerun: all 68 self-comparisons pass, with
  4,601 measurements. It rejects all 272 per-channel silence or wrong-output
  mutations and seven missing, invalid-length or non-finite files. These are
  comparator checks, not executions of a candidate application.
- A byte-identical export outside the checkout runs the complete command-line
  comparator without analyst siblings: exit 0 and all 68 evaluations pass.
  All inventory hashes, sizes and local Markdown links resolve within the
  package. No symlink or extra executable is present.
- All 82 payload files before this review were examined by type. Inputs are
  generated numerical signals; reference files are headerless numerical output
  captures. No shipped music or project document, original executable,
  recovered program code, private path, internal identifier or evidence-to-case
  mapping entered the package. The only executable is the newly authored
  measurement tool. Its NumPy and SciPy dependencies are explicit.

## Findings and rulings

| ID | Finding | Disposition |
| --- | --- | --- |
| RCO-01 | The broader draft's rate-history case described a change after parameters were applied. This package instead sets 44.1 kHz then 48 kHz before applying all parameters. | The package's explicit before-parameters history is upheld and the mutable draft corrected. The distinct after-parameters scenario is excluded; its changed output is not a payload reference. |
| RCO-02 | The source has a numerical floor before startup, and its 0.5 constant input makes output half the stated gain. | The candidate's 1e-18 floor criterion and exact onset at frame 100 are accepted as a project measurement convention. The draft now distinguishes gain from output. No claim of exact zero is approved. |
| RCO-03 | Only resolved, frozen modal estimates and a short impulse window are graded. The LFO metric measures pitch without constraining its gain. | These are accepted coverage limits. Neither complete long-term spectral equality nor LFO gain is approved. All omissions stay explicit. |
| RCO-04 | The metric's tolerances are proposed engineering acceptance criteria, rather than measured arm64 error bounds. | Accepted solely for the enumerated finite comparisons. The factor four on the frequency bound, absolute log-radius bound and complex-amplitude normalization are explicit and executable. No broader metric approval follows. |
| RCO-05 | Entry points and metadata labelled the package unreviewed. | This record added; review status and date finalized, entry points corrected and inventory resealed. |

## Disposition

**Approved with listed clarifications** for these 24 groups and 68 evaluations.
All audio fixtures, vectors, histories and measurement thresholds are unchanged.
The finite metric is accepted under the project's offline device comparison
convention. A pass is conformance to those measurements, not general sound
equivalence, Live integration or an arm64 compatibility pass.

A fresh restricted implementation workspace remains required. This local review
does not authorize external publication or tooling installation. Preserve the
published payload unchanged; corrections require a new reviewed release.
