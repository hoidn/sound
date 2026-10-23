# Electric: finite reference-output contract

This reviewed local release defines finite partial clauses of SPEC-DEVICE-ELECTRIC
revision 2. Expected outputs came from extracted execution of original x86_64
device code with substituted Linux mathematical libraries. Neither the whole
application nor arm64 device code was run. The accepted tolerances are finite project criteria, not measured arm64
error bounds; see the [review](REVIEW.md).

## Inputs and protocol

[cases.json](cases.json) enumerates 117 evaluations. Each starts from a fresh
device state, sets its sample rate, applies all 33 named comparison-domain
parameters in `parameter_order`, then processes `warm_up_frames` of silent
input without events in blocks of 512. Discard that output. Frame 0 of the
comparison output follows warm-up; it is a block start and control-grid point.

Process the evaluation's generated zero signal for exactly `frames` frames in
512-frame blocks, with a shorter final block if needed. Input is absent;
transport is stopped, position 0, tempo 120 BPM. Deliver `events` in listed
order at their explicit comparison-frame timestamps. Event channel is 1 and
velocities are integer bytes. Apply each `during_processing` parameter action
before processing the block beginning at its frame; these actions do not
restart the block partition or event-frame count. Only these enumerated action
histories have expectations. The original clock seed was fixed at 0.

The numerical parameter vectors are explicit comparison inputs, not a claimed
application API, file representation, stored-value mapping or required design.
Interpret each decimal as its nearest binary32 value. Names identify controls;
the comparison-domain PerNotePitchBendRange is fixed at 48 in these vectors.
Do not rescale a value from a presumed physical unit. No unlisted vector or
interpolation between listed settings is specified.

Produce one mono little-endian binary32 value per output frame, without a
header. This comparison releases only the retained mono signal; stereo layout is
not graded. Do not align, resample, normalize gain or fit
away phase or delay.

## Partial requirements

Every clause below is limited to the listed vectors, events, histories and
graded measurement elements. Case requirement lists define the exact mapping.

| Requirement | Approved finite scope |
| --- | --- |
| REQ-DEVICE-ELECTRIC-001 | Finite reference outputs under this protocol; no original-application call-sequence claim |
| REQ-DEVICE-ELECTRIC-005 | Outputs of the enumerated polyphony/stealing sequences only; no general allocator or voice-count formula |
| REQ-DEVICE-ELECTRIC-006 | Listed pitch-related vectors and note keys only |
| REQ-DEVICE-ELECTRIC-007 | Listed integer velocities only |
| REQ-DEVICE-ELECTRIC-008 | Listed mallet vectors, restricted to stable graded elements |
| REQ-DEVICE-ELECTRIC-009 | Listed fork vectors only |
| REQ-DEVICE-ELECTRIC-010 | Listed damper vectors, excluding random-level equality |
| REQ-DEVICE-ELECTRIC-011 | Listed pickup vectors only |
| REQ-DEVICE-ELECTRIC-012 | Listed output-level vectors including exact silence; no general gain formula |
| REQ-DEVICE-ELECTRIC-014 | The three explicitly enumerated parameter-change histories only |
| REQ-DEVICE-ELECTRIC-015 | Enumerated outputs at 48 kHz only; no other rates |

Requirements 002, 003, 004, 013 and 016 remain unreleased. Measured first-onset
windows are comparison checks under 001, not a general event-timing law under
004. No recovered synthesis equations or general internal structure is specified.

## Numerical measurements

[compare.py](compare.py) defines the executable measurement procedure. It uses
Python, NumPy and SciPy already present in the analysis environment. All
measurement arithmetic is binary64 after reading binary32 samples. Reject
missing, truncated, oversized or non-finite outputs and any missing required
measurement. A missing observation fails. Every applicable listed check must
pass. Frozen masks in `metric.graded` select the only graded elements; do not
select different elements from candidate audio.

**Silence.** The silent evaluation requires every sample exactly zero. It has
no logarithmic or relative-energy comparison.

**Onset.** Require the first sample unequal to zero inside the inclusive
`onset_min_frame`–`onset_max_frame` range. Samples before that are zero by this
definition. The maximum range is three frames, frozen from the reference's
relationship to the nominal event grid. Cases outside that range use the
reference frame exactly. This permits no global time alignment.

**Envelope.** Starting at frame 0, divide into consecutive windows of
`floor(sample_rate/100)` frames, discard an incomplete final window, and
compute `20 log10(sqrt(mean(samples²)) + 1e-30)`. Compare each selected window
to `expected_measurements.envelope_db` with absolute error no larger than
`metric.tolerances.env` dB.

**Bands.** For every `band_start_frames` entry take exactly 4096 samples,
multiply by NumPy's symmetric Hann window and compute a 4096-point real FFT.
For each `band_centres_hz` value c sum squared magnitudes of bins in
`[c*2^(-1/6), c*2^(1/6))`, then compute `10 log10(power + 1e-30)`.
Compare only listed window/band pairs within `metric.tolerances.bands` dB.
The values are unnormalized FFT-power levels, not calibrated acoustic levels.

**Partials.** Only evaluations with a nonempty `metric.partials` list grade
partials. Freeze all centers and measurement boundaries from the reference.
For harmonic k, mix output frames `[0, partial_stop_frame)` down by
`exp(-i*2π*k*fundamental_center_hz*n/sample_rate)`. Low-pass causally using
`scipy.signal.firwin`, Hamming window, scale true, cutoff
`min(20, fundamental_center_hz/4)` Hz and length
`min(4001, floor(3.3*sample_rate/cutoff) bitwise-OR 1)`.
Fit straight lines to unwrapped phase and log magnitude on frames
`partial_start_frame + filter_length` through `partial_stop_frame - 1`;
correct their frame coordinates by `(filter_length-1)/2`. Require at least
filter_length fitted samples and positive magnitude throughout.

Frequency is the center plus phase slope times sample_rate/(2π). Amplitude
is twice the fitted exponential magnitude extrapolated to partial_start_frame,
expressed as `20 log10(amplitude + 1e-30)`. Decay is log-magnitude slope times
sample_rate times 20/ln(10), in dB/s. Compare to the frozen reference estimates:

- selected amplitudes within `tolerances.amp` dB;
- selected decays within `tolerances.decay` dB/s;
- selected frequencies within relative error `4*(3*2^-25/theta² + 2^-23)`,
  where theta = 2π*fundamental_center_hz/sample_rate.

No fitted candidate gain, phase correction or frequency recentering is allowed.
Expected measurements are independently recomputed from the included reference
bytes using this same executable procedure; they are not rounded display text.

## Metric provenance and exclusions

Masks and per-evaluation tolerances were retained from six original-code
variants: four other clock seeds and one-ulp upward/downward perturbations of
inexact mathematical-library results. Loudness eligibility was within 40 dB
of the loudest envelope window and within 30 dB of the strongest band or
partial. A level/decay element remains eligible only if no variant changes
it by more than 1.5 dB / 2 dB/s. Tolerance is twice the largest eligible
deviation, with floors 0.05 dB envelope, 0.1 dB bands/amplitudes and 0.1 dB/s
decay. Those masks are frozen, not recalibrated against a candidate.

Three retained settings with less than half of their loud envelope windows
stable are excluded. Random waveform and random-component level are excluded:
the second-seed reference audio needed for a portable two-render comparison
is not included. Omitted windows, bands and partials remain ungraded. A pass
does not establish equality of all audio content, arbitrary tails, complete
phase behavior or a general sound-equivalence claim.

Also excluded: unlisted settings or histories, stored-value conversion,
project loading/saving, device placement, the application audio chain, the
general timing/voice-allocation/gain laws of the parent, controllers, MPE,
pitch bend, pedal, UI, latency/CPU reporting and real-time scheduling.

Implementation may use this reviewed release only inside a restricted workspace.
