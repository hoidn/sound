# Corpus 006-01: alias and uncertainty controls

**Bounded numerical investigation, independent review pending as of author
freeze. No calibrated capture-frequency interval or grading criterion.**

This additive packet follows the independently reviewed
[first investigation](../depth-corpus-modal-observability/README.md) and its
[review](../reviews/corpus-modal-observability-review.json). It analyzes only
the existing 006-01 Membrane capture and the candidate near 279.2923 Hz. Earlier
packets, sources, releases and all 174 ungraded observations stay unchanged.
The [retained results](results.json) include every new fit and failed control;
the single [new script](diagnose.py) imports installed mathematical tooling only.

## What is newly supported

The first packet's raw strides 4/8/16 cannot distinguish 279.2923 Hz from
11304.2923 Hz. This packet checks **full-rate data**, **coprime raw strides 5/7**
and **measured low-pass filtering before stride 8**. Together they strongly
disfavor the proposed pure-high-frequency-alias explanation for this capture's
candidate. This is stronger evidence of a low-band component, not a proof of
physical mode identity, an exact frequency, or a validated frequency estimator.

| New evidence | Left | Right |
| --- | ---: | ---: |
| Full-rate Hann peak amplitude in probe ±3 Hz | 0.0015753 | 0.0093456 |
| Largest Hann peak amplitude in the three common-alias ±3-Hz bands | 2.87e-10 | 3.49e-10 |
| Coprime raw rank 100/120 candidate range across two disjoint windows | 279.2921751–279.2937502 Hz | 279.2921490–279.2924157 Hz |
| Low-pass/stride-8 rank 100/120 candidates | 279.2922442 / 279.2923997 Hz | 279.2923856 / 279.2923711 Hz |

Full-rate projection/FFT uses raw frames 4160–16383 at 44,100 Hz, separately
for both channels. The record's 12,288 post-impulse samples in each channel
are nonzero. All common positive-frequency aliases below Nyquist are retained:
279.2923, 10745.7077, 11304.2923 and 21770.7077 Hz. Hann FFT zero-padding supplies
a finer display grid, **not additional observation time or precision**. The
unwindowed joint sinusoid projection has substantial multimode residual and
finite-window cross-leakage; its nonzero high-band coefficients are not exact
high-frequency component amplitudes. No band is declared zero.

The 24 raw coprime fits use both channels, strides 5/7, ranks 80/100/120 and
disjoint intervals [4160,10240) and [10304,16384). Hankel heights 410/293 give
approximately matched raw apertures of 2050/2051 samples. Rank-80 failures are
retained: the left first-window candidates reach 279.4910/279.4970 Hz. There is
no automatic rule selecting a rank because its answer is near the probe.

The offline analysis filter is an 801-tap Kaiser-8.6 FIR low-pass at 1800 Hz.
Its measured magnitude is 0.99999683 at the probe and approximately
4.85e-7/9.01e-7/8.10e-7 at the other three aliases. Filtering is causal with
zero initial analysis state; selected output starts 1602 samples after the
recorded impulse, beyond the full 801-tap transient. Its group delay is 400
raw samples. These choices belong to this analysis, not a required device
filter, latency, sampling algorithm or application behavior.

A mathematical high-frequency-only fixture confirms both facts: at raw
strides 4/8/16 the 11304.2923-Hz tone aliases to the probe, whereas at strides
5/7 its principal frequencies are 2484.2923/1295.7077 Hz. After the analysis
filter, measured gain matches the independently evaluated FIR response. This
fixture tests the analysis mechanism; it is not reference-device execution.

## What still blocks uncertainty or a criterion

All 28 capture fits report candidate multiplicity, selected candidate, local
left/right eigenvector condition, full eigenbasis condition, shift residual,
singular-boundary values and a hypothetical rounding-cell perturbation bound.
The nearest-probe record is an **explicit post-fit label**, not independent
mode identification. Missing or duplicate candidates would remain visible;
no acceptance decision is attached to the label.

At raw rank 100 the target's local eigenvalue condition is roughly 1.07–1.08,
but full-eigenbasis condition reaches approximately 659. At rank 120 the basis
condition reaches approximately 45,030 and weak singular gaps remain. The
target-local condition only describes sensitivity of an already constructed
shift matrix. It does not bound truncation bias, wrong signal order,
nonstationarity, nuisance leakage or the complete data-to-frequency procedure.

The hypothetical half-ULP calculation uses the larger adjacent binary32
spacing divided by two at every captured value. Hankel entries reuse samples;
the Frobenius norm of the matrix of these entry bounds is a conservative
matrix-norm upper bound **under that artificial rounding-cell assumption**.
For filtered data the entry bounds are propagated through absolute FIR taps.
No independence/noise distribution is assumed, and the captured binary32
numbers themselves remain exact retained data. Some rank-120 bound/gap ratios
exceed 1; filtered right rank 120 reaches approximately 7.54. Even a smaller
ratio is not itself a frequency error bound or proof of the chosen signal rank.

Ten full-window stride-5/rank-100 records include two unperturbed baselines and
eight finite perturbations: ±half-ULP with alternating signs and probe-phase
signs, independently per channel. Small shifts under those directions do
**not** exhaust the rounding box, calibrate actual noise, yield a worst-case
frequency bound or define a confidence interval.

The decisive negative control is an abstract six-tone, unequal-decay,
binary32-quantized mixture with a close neighbor and a high alias. It is
explicitly **not a Corpus implementation or realistic noise model**. Underfit
rank 10 returns 279.5757492 Hz for its known 279.2923-Hz component: about
0.2834492 Hz error despite local condition approximately 1.01 and relative
shift residual approximately 8.93e-6. Correct order 12 nearly recovers the
known tones; overfit 80/100/120 retains weak gaps despite small candidate error.
Thus neither favorable local condition, small residual, agreement of some
variants nor finite perturbation spread suffices to calibrate the real capture.

The remaining dependency is a separately justified **signal-order/model-error
and data-to-frequency uncertainty procedure**, with explicit candidate identity,
window/rank selection and nuisance bounds. Existing data may support a future
criterion after that work and independent review. This packet deliberately
records `calibrated_capture_frequency_uncertainty`, `confidence_interval`,
`criterion_or_tolerance` and `compatibility_result` as null. It adds no required
outcome numerator, no eligible mode, no graded observation or target law.
All 174 omissions retain their prior status; this is not an original, candidate,
x86-provider or arm64 result.

## Reproduce the new calculations only

Inspect the single new script, then run:

```sh
OPENBLAS_NUM_THREADS=1 python3 -B analysis/ableton-live-12.4.3/full-spec-v1/depth-corpus-modal-calibration/diagnose.py --check
```

It reads immutable pins, regenerates the 28 fits, ten finite-sensitivity records,
full-rate/filter results and mathematical controls, checks the seal and five
rejection fixtures, and writes nothing. With no argument it prints results to
stdout. Unsupported `--write` is refused before numerical imports. Its numeric
JSON reproduction allowance is not capture uncertainty or a target tolerance.
No old estimator/model/comparator/author function, script main or native source
is imported or run. No source fetch, install, UI, playback, hardware, account,
configuration, release/canonical/shared edit, A1 trace or other capture analysis
occurs here. Only the new analysis script and this packet's files are authored.
