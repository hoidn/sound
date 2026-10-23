# Corpus: finite reference-output contract, draft release 3

This unreviewed draft proposes finite portions of SPEC-DEVICE-CORPUS revision5.
The finite method has separate approval; the proposed parent revision and
handoff extension still await independent approval;
[the review status](REVIEW.md) is pending. Earlier v2 expectations are retained.
All expected audio derives from extracted execution of original
x86_64 device code under a fixed protocol, with Linux mathematical libraries.
Correspondence with the target Ableton Live 12 Suite 12.4.3 arm64 build is inferred
from static work; the application and arm64 device were never executed.

## Input and protocol

Every evaluation in [cases.json](cases.json) specifies an exact stereo input,
38 named comparison-domain parameter values, a sample rate and a block size.
These named numerical vectors are comparison inputs, not a claimed original API,
file representation or required architecture. Values are exactly the binary32
numbers represented by the JSON decimals. Do not replace them with rounded
printed defaults or convert them from a presumed physical scale. For example,
FilterMidFreq values in these vectors are normalized comparison inputs, not Hz.
Only the enumerated vectors have expectations; no interpolation is released.

For each evaluation:

1. Begin with a fresh device state. If `before_parameters` is empty, set the
   evaluation's sample rate.
2. Otherwise the `before_parameters` actions supply the complete initial sample-rate
   sequence, in order. Its final rate is the evaluation's sample rate.
3. Apply all parameter values in the given `parameter_order`, once each.
4. Apply any `after_parameters` actions, in order.
5. Process the supplied signal from frame 0, in `block_frames` chunks (the last
   chunk may be shorter). Input is present on both channels. No MIDI events are
   supplied except the exact events specified for group025 below. The comparison
   transport is stopped, position 0, tempo 120 BPM.
6. Produce exactly 16,384 frames. Output one binary32 value for left and then
   right, little endian, no header. Neither align nor resample the output.

`set_sample_rate` changes the comparison sample rate. `process_silence` processes
that many zero input frames with the stated block size; discard their output
before processing the supplied signal. `reset` clears device state by the
comparison reset operation. `set_parameter` applies the stated named value.
These history actions describe test inputs, not an implementation interface.
Cases 023 and 024 exercise rate history and reset; all other parameters remain
constant. Case 022 varies the host block size. No real-time timing is specified.

## Held-note inputs: group025 only

Evaluations025-01 (parent DCO-030) and025-02 (DCO-031) use the complete38-value
vectors and ordered event lists in cases.json. MidiPitch is1, MidiGate and LFO
are0. Both have one note_on at absolute host/test coordinate1537, channel0,
velocity100; only key60 versus72 differs. Channels are zero-based. Deliver in
the containing block starting1536 with local offset1, preserving listed order.
No extra adapter-minus-one correction, scheduling quantization or alignment is
permitted. This convention does not prove Live's event origin or require an
internal candidate event representation. No note_off, other event, reset,
warm-up or later parameter change is supplied; the note is held until the
finite capture ends. Destruction/release after that boundary is not compared.

These use the same generated stereo impulse at4096,44100Hz,16384frames/block512,
stopped transport0/0/120 and present input. The captured reference environment
uses round-to-nearest-even with denormals enabled and fixed clock-derived seed;
this does not impose candidate architecture or establish floating-mode/clock
invariance. All unlisted MIDI inputs and histories remain excluded.

## Partial requirements

Requirement numbers retain their parent identifiers. Each clause applies only
to the exact inputs and measurement windows of its listed cases.

| Requirement | Finite partial clause |
| --- | --- |
| REQ-DEVICE-CORPUS-001 | The protocol above and listed outputs; case022 block variants, case024 warm-up/reset variants, and only the two explicit group025 event inputs |
| REQ-DEVICE-CORPUS-004 | The dry/wet, drive and default stereo output represented in cases 001, 002, 016, 017 and 021; no general gain formula |
| REQ-DEVICE-CORPUS-005 | Modal output of cases 001–008, 015 and 017, only measured modes and impulse windows; no full mode enumeration or synthesis formula |
| REQ-DEVICE-CORPUS-006 | The listed pitch and detune vectors in cases 009 and 010, only measured modes and impulse windows |
| REQ-DEVICE-CORPUS-007 | The listed decay, material, inharmonicity, brightness, ratio and bleed vectors in cases 011, 012 and 015 |
| REQ-DEVICE-CORPUS-008 | Host position and pickup comparison vectors in cases 013 and 014; no claim about stored document position controls |
| REQ-DEVICE-CORPUS-009 | The eight Pipe/Tube reference outputs in case 018, at the supplied radii, opening and rates; no general waveguide model |
| REQ-DEVICE-CORPUS-010 | The two fixed filter vectors in case 019; changes during processing and coefficient ramps excluded |
| REQ-DEVICE-CORPUS-011 | The Free-running Sine trajectory in020-01 and the single finite Ramp Up waveform in020-02 (parent DCO-029), each only its stated measurement window; no general LFO law, random shapes or Sync |
| REQ-DEVICE-CORPUS-012 | Startup gain in case 021, rate history in case 023 and warm-up/reset in case 024; other automation and timing excluded |
| REQ-DEVICE-CORPUS-013 | Proposed only the exact held-note60/72 finite outputs in025-01/02 and their stated measurements; all general MIDI behavior and Live side-chain routing excluded |

Requirements002 (stored-to-comparison mapping) and003 (controller formulas) are
unreleased. Requirement013 is proposed only for the bounded subset above. The full parameter equations and general
claims of the parent are not part of these finite partial clauses.

## Measurement criterion

This is a reviewed project criterion for the enumerated finite comparisons. It accounts for plausible
floating-point differences without asserting that any tolerance is a measured
arm64 error bound. The reference itself was produced with substituted libraries.
A candidate must meet every applicable check independently for left and right.
No time alignment, gain normalization, channel mixing or fitted phase shift is
permitted. [compare.py](compare.py) defines the numerical details below and the
finite JSON mode centers specify exactly which modes are graded.

All arithmetic in measurement uses binary64. Read samples as binary32 then widen.
Reject non-finite samples or estimates, absent or unmeasurable required modes,
zero energy denominators and invalid output lengths. A missing observation fails.

**Relative RMS.** For the stated frames, compute
`sqrt(sum((candidate-reference)^2)/sum(reference^2))` per channel.

**Modal impulse outputs.** Compare frames 4096 through 4351 with relative RMS
at most 0.002. For every listed center and cutoff, mix each full output down by
`exp(-i 2π center n / sample_rate)`, low-pass with a Hamming FIR designed by
`scipy.signal.firwin` (scale true), length
`min(4001, floor(3.3*sample_rate/cutoff) bitwise-OR 1)`. Use causal filtering.
Fit straight lines to unwrapped phase and log magnitude on frames
`4096 + filter_length` through 16383, with times corrected by the FIR delay
`(filter_length-1)/2`. The frequency is center plus phase slope times rate/(2π);
the per-frame log radius is the log-magnitude slope. Complex amplitude is twice
the fitted complex exponential extrapolated to frame 4096.

Apply these limits against the identically measured reference:

- frequency error at most `reference_frequency * 4 * (3*2^-25/theta^2 + 2^-23)`,
  where `theta = 2π*reference_frequency/sample_rate`;
- absolute per-frame log-radius error at most `8*2^-25`;
- `abs(candidate_complex_amplitude/reference_complex_amplitude - 1)` at most 0.005.

For the preceding modal cases, eligibility is frozen in the cases. Centers came from static pole estimates;
only reference modes whose resolved frequency estimate is within 1e-4 relative
of that center are retained. Each cutoff is min(100 Hz, 0.4 times the nearest
significant-mode gap). The omission of other modes is a coverage limit. It must
not be interpreted as those modes passing or as permission for arbitrary added
long-term energy. This finite metric does not establish complete spectral equality.
Group025 uses the case-specific eligibility decision stated below.

**Sine.** On frames 8192 through 16383, fit sin and cos at the exact supplied
frequency by least squares, independently in each output. Form complex gain as
sin coefficient plus i times cos coefficient. Candidate/reference gain must differ
by at most 0.01 dB in magnitude and 0.5 degrees in phase, with wrapped phase.

**Noise.** On frames 8192 through 16383, apply NumPy's symmetric Hann window and
an 8192-point real FFT. Band lower edges are `1000*2^(j/3)` for j=-11…12;
upper edges are lower times `2^(1/3)`. Include bins at the lower edge and exclude
those at the upper edge. Sum squared magnitudes per band; require each candidate/
reference ratio to lie within 0.01 dB. Every band needs at least four bins and
positive energy. This fixes the approximate 80 Hz–16 kHz lower-edge range.

**Pipe and Tube.** Compare all frames 4096 through 16383 with relative RMS at
most 0.0001. **Filter.** Compare frames 8192 through 16383 with that same limit
and the noise-band checks.

**LFO.** Mix down at 261.62 Hz, then causally low-pass with an 801-tap Hamming
FIR, cutoff 80 Hz. For t=5296,6296,…,15296, inspect filtered frames t+300 through
t+500 inclusive. Average the 200 consecutive unwrapped phase differences and
convert to frequency. Candidate/reference estimates must differ by at most 0.2 Hz.
This does not grade the LFO's amplitude or all of its spectrum.

**Finite Ramp Up (020-02, parent DCO-029).** This evaluation was added in release2.
It uses the Sine evaluation020-01 input/protocol and all38 comparison values,
except LfoType is3 instead of0. Compare every frame4096through16383inclusive
independently for each channel. Require full-file finite samples and positive
reference AND candidate energy on that interval. Use binary64 subtraction and
products, `math.fsum` for the two energy sums and squared-error sum, then
`math.sqrt(error_energy/reference_energy)`. Both computed channel errors must
be inclusively at most0.01, with no epsilon. The tool checks the exact nominal
Ramp reference SHA-256. The older modal, Sine-trajectory and startup metrics do
not additionally apply to this evaluation.

The1%budget is an explicit finite engineering acceptance choice, permitting at
most1e-4 error energy/reference energy per channel. Two coherent math-import
substitution observations fall below it, but do not form an architecture error
bound, a guarantee for arbitrary mixed math errors, or a measured original
application tolerance. Aggregate RMS can admit concentrated, onset or late-tail
defects. Finite differences in frames0through4095 are outside this metric;
nonfinite samples anywhere still fail. No full-cycle/absence-of-phase-wrap,
Sync/Spin/random, stored mapping, original Live delivery or candidate claim
follows. The supplied reference is a finite output capture, not LFO sample data.
The reference environment uses round-to-nearest-even with denormals enabled;
this is not a required candidate architecture. No block-size, repeatability,
clock, reset, rate or floating-mode invariance is established for020-02.

**Startup.** The original has a numerical floor of about 1e-22, not bitwise
silence. Frames 0–99 must stay at or below 1e-18 absolute on each channel, and
frame 100 must exceed that floor. Compare the rising gain on frames 100–199 and
the settled gain on frames 199–16383 separately with relative RMS at most 0.0001.
The onset/ramp frame boundaries are exact. The floor threshold is a reviewed
project comparison convention; the reference is not asserted to output zeros.

## Case-specific held-note criterion

Only the modal measurement branch applies to025-01/02: the first256 frames
4096through4351 inclusive and every frozen point on both channels. All points
have cutoff100Hz, giving1455-tap FIRs and fits on5551through16383 inclusive,
with727-frame delay correction and complex amplitude extrapolated to4096.
The frequency, per-frame log-radius and complex-amplitude limits above are
unchanged. No startup, Sine-trajectory, Ramp or other general signal-class
comparison additionally applies. Full-file exact length and finite samples
are mandatory; required modes must be measurable with finite nonzero amplitude
and reference denominators. Both channels must have positive post4096 energy;
a missing or zero active signal cannot yield the required measurable modes.

Frames0through4095 have format/finiteness validation only. There is no prefix
waveform budget, silence/floor, energy, phase, onset, event-time or startup
accuracy claim. Finite prefix corruption can pass. No phase/gain correction,
centering adjustment, failed-point removal, alternate scoring window or wider
threshold is permitted. All expected mode values are measured from the exact
reference, not equated to a navigation center or inferred note-frequency law.

025-01 copies all32 points of evaluation013-04 exactly. Its reference bytes
from4096onward equal that earlier reference; full files differ. All FIR input
support for the fixed fitted segment is inside that identical region. That
case alone cannot reject ignoring the note or MidiPitch: the earlier fixed-pitch
output satisfies every scored sample and descriptor.

025-02 proposes an explicit POST-OBSERVATION finite engineering eligibility
exception for this case only, instead of the earlier recovered-pole condition.
The16 navigation centers/channel and100Hz cutoff were fixed before reference
calibration. After observing the reference diagnostics, the first15 points per
channel were selected without refitting:30points total. Both mode16 estimates
are omitted because full/half-window estimates were materially sensitive. This
was a disclosed engineering choice after reference observation and before any
candidate result, not a predeclared subset or automatic stability criterion.
The full32-point evidence remains retained. These2new omitted observations are
ungraded, separate from the unchanged historical174omissions. The total initial
256-frame waveform still includes the omitted component; omission does not
prove absence or permit arbitrary added energy.

The unchanged numerical budgets are proposed here as finite project engineering
limits, not a recovered vendor tolerance, transferred native4ULP guarantee,
inaudibility claim, Apple/arm64 bound or mathematical-library error envelope.
Conditional pole estimates and the reference/control evidence do not prove
actual native coefficients, p1 state, source binding or physical note accuracy.
Observed significant regular-mode gaps support100Hz within that inspected list;
complete nearest-significant-gap, hidden-spectrum and estimator-uncertainty
proof remain absent. Half-window sensitivity is descriptive, not a new scoring
threshold. The wrong-note60 control is strongly rejected by the selected025-02
measurements, but shared harmonics mean frequency-only checks can pass; it is
not a universal note classifier. A reference-self pass is not a candidate grade.

## Exclusions and limits

Only the enumerated inputs, protocols and measurements have expectations.
Excluded are project loading/saving, default insertion behavior, stored-to-device
position conversion, device placement or the Live audio chain, UI text, automation
beyond the explicit history actions, all MIDI side-chain behavior except the
two exact held-note inputs, random LFO shapes, Sync,
all unlisted vectors/rates/signals/histories, reporting/CPU behavior and real-time
scheduling. This package accepts no assumption that the original application uses
this protocol in every circumstance. Unmeasured modes and output properties
remain unknown. No whole-application or arm64 compatibility pass can be inferred.


## Historical changes from release1 to release2

Carries all24 existing groups and68 evaluations, histories, values, signals,
references and measurement rules unchanged. Adds only020-02 within group020,
mapped to parent DCO-029, and its dedicated finite waveform metric. Release2
has24groups/69evaluations,69reference files containing62distinct byte streams,
and nine generated input signals. Release1 remains immutable. This strict finite
extension does not complete any device profile or whole behavioral family.

## Proposed changes from release2

Preserve all69 previous evaluation objects,78 physical input/reference fixtures
and the measurement code byte-for-byte. Add only group025 with two evaluations,
mapped to parent DCO-030/031, and two retained reference files. Draft release3
has25groups/71evaluations,71reference files containing64distinct byte streams,
and nine generated inputs. Prior releases remain immutable. This does not
approve general MIDI behavior, source binding, stored mapping/A1, Live routing,
arm64, note-off/gate/sustain/bend/priority/velocity/channels/boundaries, invariance,
complete spectra, all omitted modes or a complete profile. No candidate ran.
