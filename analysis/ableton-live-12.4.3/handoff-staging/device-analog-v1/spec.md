# Analog: finite reference-output contract

This reviewed local release retains only finite portions of SPEC-DEVICE-ANALOG
revision 1. The expected samples were captured from original x86_64 device code
with substituted Linux libraries. Neither the original application nor arm64 device
code was executed. Correspondence to Ableton Live 12 Suite 12.4.3 arm64 is
inferred, not an observed compatibility result.

## Comparison inputs and protocol

Each evaluation in [cases.json](cases.json) specifies all 203 named comparison-domain
values, their application order, sample rate, block size, silent input and note
list. The labels are project comparison labels. A `.secondary` label denotes a
second component of that named comparison control; `Enabled` denotes a fixed
comparison switch. These are not original internal identifiers, stored XML values,
a claimed application API or a required candidate structure. The exact JSON
binary32 values are authoritative; do not replace them with rounded defaults or
apply a presumed stored-to-control conversion. No unlisted vector has an expectation.

For each evaluation:

1. Begin with a fresh instrument state. Set the sample rate.
2. Apply every vector value once, in `parameter_order`. Round each JSON decimal
   to binary32 before applying it. All values remain constant during processing.
3. Process the given silent stereo input from frame 0 in the stated block size;
   the final block may be shorter. The input-presence flag is false. Transport
   is stopped at position 0, tempo 120 BPM.
4. Deliver the note events in listed order. Frames are absolute zero-based frames
   since processing began. Deliver an event in the host block that contains it,
   with within-block offset `frame - block_start`. Preserve order for equal frames.
   `note_on`/`note_off`, channel, key and velocity are the listed comparison inputs.
   Channel numbers are zero-based (0 to 15); these evaluations use channel 0.
5. Produce exactly the stated number of output frames. Write left then right as
   little-endian IEEE-754 binary32 values, no header. Do not align, normalize,
   resample or mix channels before comparing.

The instrument's 1 ms control grid is part of its observed output, not an
adapter adjustment to event delivery. The test convention does not accept the
open assumption that Live itself uses this frame base, grid phase, vector mapping
or block protocol. Loading/saving sets and integration with a playing MIDI clip
or mixer are excluded.

## Partial requirements

Only exact vectors, events, protocol histories and measurement windows in this
package have expectations. General formulas and unknown portions of the parent
are excluded.

| Requirement | Finite scope |
| --- | --- |
| REQ-DEVICE-ANALOG-001 | Fixed protocol and listed reference outputs, including the two supported block-size variants in case 045 |
| REQ-DEVICE-ANALOG-004 | Captured event responses: first nonzero frame, selected onset windows and final voice end where the reference ends before the file boundary |
| REQ-DEVICE-ANALOG-005 | Listed chord, stealing and mono-key sequences, only their measured onset/envelope/timing outputs; no general allocation or mono-dip formula |
| REQ-DEVICE-ANALOG-006 | Listed pitch/detune/transpose inputs, only eligible frozen steady frequency/harmonic measurements and short onset windows |
| REQ-DEVICE-ANALOG-007 | Listed sine, saw and rectangle vectors, only the first 40 harmonics at most and the defined temporal windows |
| REQ-DEVICE-ANALOG-008 | The two listed Sub/Sync reference outputs under the same finite metrics; no general synthesis method |
| REQ-DEVICE-ANALOG-011 | The listed two-chain routing vector, with measured outputs only |
| REQ-DEVICE-ANALOG-012 | The ten fixed filter-type vectors, including render-only Notch4/formant outputs; no general transfer or closed-form filter model |
| REQ-DEVICE-ANALOG-013 | The listed filter-envelope, keyboard-tracking and two-chain vectors, only measured outputs; no general modulation law |
| REQ-DEVICE-ANALOG-014 | The two listed drive vectors, with fixed output measurements only |
| REQ-DEVICE-ANALOG-015 | The listed maximum-level output vector |
| REQ-DEVICE-ANALOG-016 | The listed amplitude-envelope vectors and their measured windows/tails; no segment recursion or envelope implementation |
| REQ-DEVICE-ANALOG-017 | The listed integer-velocity sequences and attack vector |
| REQ-DEVICE-ANALOG-023 | The two exact 48 kHz vectors/events, only their finite measured output; no other sample-rate behavior |

Requirements 002, 003, 009, 010, 018 to 022 are unreleased. Random noise and pitch
errors, unvalidated LFO/pitch-envelope/vibrato trajectories, glide, unison,
unrendered envelope modes, controllers, pressure, MPE and automation are excluded.
There is no statistical grading. Unresolved closed forms do not become approved
merely because a deterministic fixture exists.

## Reviewed finite measurement criterion

The independent review accepts this criterion only for the finite comparisons below. The retained
one-ulp library perturbation study supports using short waveform, envelope and
steady-frequency comparisons rather than long sample equality. It does not
measure arm64 errors or prove that these tolerances cover all implementations.
A missing or unmeasurable required observation fails. Other output properties
remain unknown, not passes. [compare.py](compare.py) defines the executable arithmetic.

All measurements widen the binary32 samples to binary64. Reject wrong lengths,
non-finite values, zero energy denominators, silent required windows, non-finite
fits and missing files. Compare left and right independently. References are
stored as stereo; both captured channels were bit-identical. No independent
phase alignment or gain normalization is allowed.

**Timing.** `first_nonzero` freezes the reference's first sample different from
exact zero. The candidate's first nonzero frame must equal it. If `last_nonzero`
is supplied, the candidate's final nonzero frame must be within one frame of it.
A null final frame means the voice did not end inside the capture, so no voice-end
claim is made. This does not separately grade every note-off's first changed frame.

**Onsets.** Each frozen `[start, stop]` onset window includes start and excludes
stop. Its first frame follows the device's observed event grid, and it contains
2,048 frames unless truncated at the capture boundary. Per channel compute
`sqrt(sum((candidate-reference)^2)/sum(reference^2))`; it must be at most 0.005.
The windows include existing voices during polyphonic and mono-key changes.

**Envelope.** Starting at file frame 0, divide output into consecutive windows
of `floor(sample_rate/100)` frames (441 or 480). Discard any incomplete final
window. Compute RMS per window. Grade only windows whose reference RMS is at
least 0.001 times its greatest window RMS: exactly 60 dB down in amplitude. Each
candidate/reference RMS ratio must lie within 0.05 dB. Ungraded low-level windows
are not evidence of silence, except where the first/final-frame check applies.

**Steady windows.** The frozen windows begin 100 ms after a single note-on and end
at the capture boundary. The author retained only windows at least 0.2 s and 25
reference periods long. Multi-note, time-varying or unselected windows have no
steady-frequency/harmonic claim. Centers, counts and selected harmonic numbers
are frozen in the cases; eligibility is never recomputed from candidate data.

Frequency estimation mixes down at the given center, applies a causal Hamming
FIR designed with `scipy.signal.firwin` (scale true), cutoff
`min(20 Hz, center/4)` and length
`min(4001, floor(3.3*rate/cutoff) bitwise-OR 1)`. Discard the first filter-length
frames, correct times by the FIR group delay `(filter_length-1)/2` and linearly fit the unwrapped
complex phase. Add `phase_slope * rate/(2π)` to center. Apply the same operation to
the candidate and reference; relative frequency error must be at most 1e-5.
Frequency checks below 100 Hz are omitted because they lie outside the cited
pitch calibration. A zero/failed estimate is a failure, never a skipped mode.

For harmonic amplitudes, fit all cos/sin pairs at integer multiples of the fixed
reference center plus a constant column, by least squares on the window. The
amplitude is the hypotenuse of that harmonic's coefficients. Fit at most the first
40 harmonics below Nyquist. Among those, grade the frozen harmonics whose reference
amplitude is at least 0.01 times the strongest fitted harmonic (40 dB down).
Each amplitude ratio must lie within 0.05 dB. The fitted DC difference must be at
most 0.001 times the peak absolute reference sample in that same window. Harmonics
above this finite cap are excluded; this is not a full spectral comparison.

## Coverage limits

Only the listed sample inputs and output measurements are released. No stored
parameter mapping, constructor/default insertion, real-time or Live-chain timing,
file loading, UI or whole-application behavior is approved. All parameters are
constant during each render. General device equations, random/statistical
components, unselected modulation trajectories and unlisted histories are excluded.
No pass proves arbitrary-input sound equivalence, general spectrum equality or
arm64 execution. Unmeasured properties remain unknown.
