---
id: SPEC-DEVICE-COLLISION-RELEASE-V1
type: spec
status: released
updated: 2026-10-19
access: handoff
revision: 1
target: Ableton Live 12 Suite 12.4.3 / macOS; retained x86_64 output captures
---

# Collision: two bounded output contracts

Reviewed partial scope of SPEC-DEVICE-COLLISION revision 1, FEAT-DEVICES. Only
DEVICE-COLLISION-001 and DEVICE-COLLISION-002 are included. Requirements below are approved only for the finite comparison scope. Original x86_64 device execution produced the retained
outputs previously; no whole application, arm64 or independent candidate has
been executed for this contract.

## Inputs and state

For each case create a fresh instrument, set the rate to 44,100 Hz and apply all
139 named comparison-domain parameter values in listed order. `cases.json` owns
all exact values; there are no omitted defaults. Values are binary32: the
little-endian four-byte `binary32_hex` field is authoritative, with its exact
numeric value also shown. Names are descriptive control labels, not a required
API, serialized field name or prescribed internal structure. A candidate may
represent them as it chooses. The reserved per note pitch bend entry is fixed
input data with no behavioral claim.

These values are in the device comparison domain, not saved-project values or
UI knob positions. In particular the note-off decay values are already inverted
relative to saved values. Position values are the listed values without another
rescale. No contract for that conversion from saved projects is released here.
The Pipe case sets resonator 1 enabled, type 5 (Pipe), decay 1 and mallet noise
amount 0; the disabled-resonator case disables both resonators. Even mallet noise
amount 0 has small residual randomness. References use a fixed zero clock seed;
reproducing a particular random-generator algorithm is not required.

Both cases start with silent stereo audio input and input availability 0
(the comparison convention meaning no external audio is supplied), transport
stopped, position 0 beats and tempo 120 BPM. Warm up for 11,264 frames in blocks of 512,
with no events, discarding its output. Then render the declared frame count in
512-frame blocks with a final shorter block as needed. Render frame 0 follows
warm-up; control state persists across that boundary. Continue processing the
entire declared length. Keep parameters,
transport and input constant. Destroy the instance after rendering.

Each event lists an integer frame relative to render frame 0, MIDI status byte,
key and velocity. The status byte includes channel 1. Events are supplied at
their listed timestamps; their audible effect is judged only by the output
metric. DEVICE-COLLISION-001 schedules C4 velocity 100 on frame 4,096 and note-off on 26,146,
beyond its 22,050-frame output, so that note-off is never reached. DEVICE-COLLISION-002 has
C4 velocity 100 on frame 0, held throughout its 32,768-frame output. No other
events occur. No particular teardown result is claimed beyond finishing each
finite output.

## Outputs and measurement

Output is stereo interleaved IEEE binary32 little-endian audio with exactly the
case's frame count. No metadata header, normalization, alignment, gain fit,
channel swapping or leading/trailing cropping is permitted. The comparison
window is fixed at `[0, frames)` for both cases. All samples must be finite,
and both output files must exist and be nonempty for the overall comparison to pass.

| Case | Partial requirements | Metric and approved maximum |
| --- | --- | --- |
| DEVICE-COLLISION-001 | REQ-DEVICE-COLLISION-001, 002, 003 | Maximum absolute sample over both channels and all 22,050 frames ≤ 10⁻¹⁸ |
| DEVICE-COLLISION-002 | REQ-DEVICE-COLLISION-001, 014 | Stereo relative RMS over all 32,768 frames ≤ 0.003 |

For DEVICE-COLLISION-002 compute `sqrt(sum((candidate-reference)^2)/sum(reference^2))`
over all 65,536 scalar samples in binary64 arithmetic with accurately summed
terms. The denominator must be finite and positive; the result must be finite.
The comparator checks the reference byte digest before measurement. It rejects
invalid data rather than producing an empty or vacuous pass. DEVICE-COLLISION-001 is an
absolute silence boundary: zero or scaling its inaudible residual remains a
valid pass, while introduced output above the peak limit fails.

`compare.py` is the exact independent measurement procedure. It checks both
cases and reports every error; the overall result requires two passing results.
No modal estimator, mode selection or frequency-only test is used. Thus there
are no unresolved mode rows that can silently disappear from this package's
acceptance checks.

## Evidence and tolerance limits

The disabled-resonator capture has peak approximately 4 × 10⁻²². The approved
10⁻¹⁸ bound intentionally accepts effectively silent implementations.

For the exact Pipe setup and window, earlier two-sided one-ulp perturbations of
inexact mathematical library results produced stereo relative RMS 0.0005140501
and 0.0006108613. The approved 0.003 bound covers those observations. Perturbed
audio is not in this package; calibration is a retained measurement summary.
The reference audio itself is fully retained and hashed. Calibration does not
establish an arm64 bound, arbitrary random seeds, arbitrary compiler arithmetic
or whole-application behavior. The metric is an approved finite project acceptance
criterion, not proof of those unmeasured dimensions.

## Exclusions and unknowns

No other draft acceptance case is included. Modal outputs, unresolved/weak/close modes,
Membrane ratio 0.75, Tube, pitch envelope, noise-exciter settings and statistical
noise acceptance remain deferred. Modal decay and complex-amplitude portability
calibration is incomplete; those cases receive no pass from these checks.
There is no separately accepted Pipe frequency measurement, general synthesis
formula, event-grid rule or arbitrary-note/rate/parameter guarantee.

Also excluded: saved-value conversion and position mapping, original application
call ordering and integration, LFO/controllers/MPE, retrigger and stealing,
active parameter transitions, automation, rate changes, persistence, undo,
malformed/out-of-domain device inputs, cancellation, concurrency, faults, UI,
file formats, latency, CPU and real-time scheduling. Comparator malformed-file
checks specify this measurement tool, not original device error behavior.
No five-device or T1 completion follows from this finite pilot.
