# Tension: finite reference-output contract

This reviewed local release specifies finite partial clauses of SPEC-DEVICE-TENSION
revision 2. Reference audio came from extracted execution of original x86_64
device code with substituted Linux libraries. The whole application and arm64
device were not executed. Tolerances are reviewed fixed-scope project criteria,
not measured arm64 error bounds.
See [the review disposition](REVIEW.md).

## Inputs and protocol

[cases.json](cases.json) defines 27 finite evaluations. Start each with a fresh
device state, set its sample rate and apply every named comparison-domain
parameter once in `parameter_order`. Interpret JSON decimals as their nearest
binary32 values. Process the generated zero input for exactly `frames` frames
in 512-frame blocks (short final block allowed), without a warm-up. Input is
absent; transport is stopped, position 0, tempo 120 BPM. Deliver the listed
channel-1 note events at their comparison-frame timestamps and in list order.
All parameters remain constant. The original clock seed was fixed at 0. Input
absence is the comparison convention for supplying no external audio, not a required application interface.

Each vector contains 129 components. These are comparison inputs, not stored
values, a claimed application API or a required design. Components with suffix
`.Negative`, `.Enabled` or `.SlopeFlag` are independent named components of
this finite comparison vector. They are supplied explicitly; do not reconstruct
them from a presumed signed, physical or stored scale. PerNotePitchBendRange
is a comparison-domain value, fixed at 48 here. No unlisted vectors or
interpolation between them have an expectation.

Produce exactly one mono little-endian binary32 sample per output frame,
without a header. Both original channels were identical; only their shared
mono signal is released. Do not align time, resample, normalize gain or fit
away a phase shift. Note timestamps describe this comparison protocol; they
do not claim the application's event delivery or grid phase.

## Partial requirements

All clauses below are limited to enumerated inputs and measured properties.
Each case carries its exact requirement list.

| Requirement | Approved finite scope |
| --- | --- |
| REQ-DEVICE-TENSION-001 | Fixed-protocol outputs and numerical comparisons |
| REQ-DEVICE-TENSION-004 | Listed note-key vectors only; no general tuning formula |
| REQ-DEVICE-TENSION-005 | Listed ringing string outputs, measured partials and decay windows |
| REQ-DEVICE-TENSION-006 | Listed plectrum, hammer, position and repeated-strike outputs; sustained bow excluded |
| REQ-DEVICE-TENSION-007 | Listed velocity vectors only |
| REQ-DEVICE-TENSION-008 | The two stable damper vectors; zero-mass chaotic output excluded |
| REQ-DEVICE-TENSION-009 | Listed termination vector only |
| REQ-DEVICE-TENSION-010 | Listed pickup vector only |
| REQ-DEVICE-TENSION-011 | Listed body vectors only |
| REQ-DEVICE-TENSION-012 | Listed filter vectors only |

Requirements 002, 003, 013, 014 and 015 remain unreleased. No general
stored-value conversion, timing, gain, allocation, modulation or synthesis
formula is specified by this release.

## Measurement criterion

[compare.py](compare.py) is executable signal measurement only. It requires
Python, NumPy and SciPy. Read binary32 samples and widen to binary64 for all
measurements. Missing, truncated, oversized or non-finite files fail. Required
measurements that are absent or unmeasurable also fail. No missing observation
can be reported as a pass. Audio arrays and waveform windows must be nonempty
and finite, and stable cases require their complete nonempty partial lists.

**Onset.** The first sample unequal to zero must equal `metric.onset_frame`
exactly. Thus every earlier sample must be zero. This criterion does not allow
a candidate-dependent analysis window.

**Waveform.** For each `[start, stop, tolerance, label]` in
`metric.waveform_windows`, using the half-open frame interval, require
`sqrt(sum((candidate-reference)^2)/sum(reference^2)) <= tolerance`.
A zero reference denominator fails. Stable cases grade the held window
`[reference onset, note-off timestamp)` at 0.003 and the release window
`[note-off timestamp, end)` at 0.01. The repeated-strike evaluation grades
the whole `[reference onset, end)` at 0.005 instead.

**Stable partials.** The cases freeze centers, cutoff, analysis window and
amplitude normalizer from the reference study. Candidate audio never changes
which modes are eligible. For each listed center, mix frames `[0, stop)` down
by `exp(-i*2π*center*n/sample_rate)`, where `[start, stop]` is
`metric.partial_window`. Causally low-pass with a Hamming FIR from
`scipy.signal.firwin`, scale true, cutoff `metric.partial_cutoff_hz` and length
`min(4001, floor(3.3*sample_rate/cutoff) bitwise-OR 1)`.

Fit straight lines to unwrapped phase and log magnitude over frames
`start + filter_length` through `stop - 1`, correcting frame coordinates by
the delay `(filter_length-1)/2`. At least filter_length samples must remain;
zero magnitude or non-finite estimates fail. Frequency is center plus phase
slope times sample_rate/(2π). Per-frame natural-log radius is log-magnitude
slope. Complex amplitude is twice the fitted exponential extrapolated to
frame start, including the fitted phase.

Measure candidate and included reference identically, and require for every
listed partial:

- relative frequency error at most 0.000002;
- relative per-frame log-radius error at most 0.0006; a zero reference radius fails;
- complex-amplitude difference divided by `metric.amplitude_normalizer` at most 0.0005.

The normalizer is the strongest reference partial magnitude from the retained
eligibility study. Only partials at or above −60 dB relative to that strongest
partial are listed. No candidate amplitude normalization or phase fitting is
permitted. The repeated-strike case grades no partials, since its perturbation
spread does not support the stable-partial criterion. Omitted modes remain
ungraded; they do not acquire a compatibility pass.

## Calibration and exclusions

All 27 cases have retained per-setting sensitivity results. The perturbed audio
is not retained, so those historical measurements cannot be independently
recomputed from this payload. The 26 stable settings were tested with inexact library results moved one ulp up/down and
SSE arithmetic rounded downward, upward and toward zero. Largest deviations
were held waveform 0.00059511, release waveform 0.00229178, relative frequency
0.00000046698, relative log radius 0.00014159 and normalized complex amplitude
0.00011119. All onset frames were unchanged. The repeated-strike whole-waveform
spread reached 0.00114477. The approved finite bounds retain a margin over these
observed substituted-library/rounding variants; they do not prove arm64 equivalence.

Four chaotic retained settings are excluded: sustained bow, its position
variant, zero damper mass and the cello control vector. The other 37 retained
outputs without per-setting sensitivity studies are excluded from this first
release. No loose RMS/peak statistical criterion is substituted for them.
New settings require their own reviewed evidence and criterion.

Also excluded: unlisted inputs/rates/histories, parameter automation, project
files and stored-value mapping, loading/saving, device placement, application
audio-chain integration, voices and stealing, LFO/modulation, controllers,
MPE, pitch bend, pedal, UI, real-time timing, latency and CPU reporting. A pass
covers only listed protocol-conditioned audio properties. It does not establish
general sound equivalence beyond the declared comparisons.
