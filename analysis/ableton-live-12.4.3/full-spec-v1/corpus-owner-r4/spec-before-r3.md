---
id: SPEC-DEVICE-CORPUS
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 3
target: Ableton Live 12 Suite 12.4.3 / macOS; reference renders from the Corpus.bundle x86_64 slice
---

# Corpus audio effect: signal behavior and reference renders

## Scope

Feature FEAT-DEVICES, T1 device audio ([ADR 0004](../decisions/adr-0004-target-scope-t1.md)).
User task: a track holds the bundled Corpus effect, and the offline render of that track
must sound as Live's would. This draft specifies:

- the output Corpus produces for a stereo input and a set of stored parameter values, at
  44.1 kHz and 48 kHz;
- the reference renders that define that output for T1, and the protocol that made them;
- the comparison metric a candidate render must meet.

How the parameters are stored, with their domains and defaults, is
[SPEC-BUNDLED-DEVICE-PARAMETERS](bundled-device-parameters.md). Where Corpus sits in the
track's signal flow belongs to the mix-graph and playback specs.

Excluded:

- the MIDI side-chain features: MidiPitch, MidiGate, Transpose, FineTranspose,
  PitchBendRange, DecayOnNoteOff, MidiMode and the side-chain routing fields (REQ-013, U);
- LFO Sync and the random LFO shapes as exact waveforms (REQ-011);
- parameter automation during a render beyond the timing rules of REQ-012;
- display text, CPU load and latency reporting.

Every requirement is a **proposed contract**. Nothing was run against Live, and under
[ADR 0003](../decisions/adr-0003-no-reference-execution.md) nothing will be. The audio
evidence is extracted execution of the shipped x86_64 Corpus code. The Live-side
parameter path is a static derivation. Canonical evidence:
[device DSP by extracted execution](../research/device-dsp-extracted.md).

## Evidence labels

| Label | Meaning |
| --- | --- |
| D | Documented in shipped bytes: the schema, the shipped presets and the bundle's export table |
| S | Static derivation from the 12.4.3 executables; not an observed run |
| S-cond | A static derivation that holds only under the named assumption (A1 below) |
| X | Extracted execution: the shipped x86_64 Corpus slice was run on the stated inputs in the harness of [ADR 0003](../decisions/adr-0003-no-reference-execution.md#extracted-execution-of-original-code). It shows what the device code computes for those calls. It does not show that Live makes the same calls. The arm64 release slice is matched only by static comparison (appendix) |
| U | Unknown; no expected result, and not graded |

Only D, S and X clauses, and S-cond clauses whose assumption is accepted, may enter a release.
A U clause blocks the behavior it names. Each blocking U clause states its effect on T1.

## Assumptions

| ID | Assumption | What rests on it |
| --- | --- | --- |
| A1 | Live passes the stored ExcitationX, ListeningXL and ListeningXR values (0..1) to the device unchanged, as its float parameter unit is traced to do for every other identity-mapped Corpus parameter. Static readings conflict: the device would cover its full position range only for inputs of −1..1 (REQ-BUNDLED-DEVICE-PARAMETERS-015). Static route: trace the value that unit emits | REQ-002, REQ-008; cases DCO-013, 014 and 028 for stored values |
| A2 | The device sees the protocol of REQ-001. That is: the sample rate is set before the parameters; all 38 values are sent; transport not playing; input flagged as present. Live's call order is static (S); the transport and flag values Live passes are unknown | REQ-001, every case |

## Requirements

### REQ-DEVICE-CORPUS-001 — reference renders define the output

- **X.** For T1, Corpus's output for an input and a set of host values is the reference render
  made with this protocol:
  1. a new instance is created;
  2. the sample rate is set (44,100 or 48,000 Hz);
  3. all 38 host values of REQ-002 are sent, in index order;
  4. processing starts at the first frame, in host blocks of 512 frames;
  5. the input is stereo binary32, flagged as present;
  6. the transport is not playing (position 0, 120 BPM).

  The reference renders are retained with their inputs and SHA-256 (cases below). The
  output is stereo binary32, one output frame for each input frame.
- **X.** With constant parameters the output does not depend on these choices:
  - the host block size (64, 256, 333, 512 and 2,048 frames tested);
  - flush-to-zero and denormals-are-zero;
  - the clock value with which the device seeds its random generator, except for the random
    LFO shapes (REQ-011).

  Re-running a case gives a bit-identical render.
- **S, X.** Live creates the instance, sets the current sample rate and sends the parameter values
  ([N5](../research/device-parameter-mapping-native.md#how-live-loads-a-bundle)). It may also run
  a reset sequence: 1,024 frames of silent input, a device reset, then the ResonanceType value
  again. That sequence leaves the output of a later input unchanged within 4.6 × 10⁻²⁰ (X, default
  and Tube settings).
- **U.** When Live runs the reset sequence, which host block sizes it uses, and which
  transport and input-flag values it passes. Effect on T1: none for constant parameters
  (block-size invariance, X). The timing of parameter changes under REQ-012 depends on Live's
  block boundaries.

### REQ-DEVICE-CORPUS-002 — from stored values to host values

- **S** ([N5](../research/device-parameter-mapping-native.md#corpus-complete-38-indices)). Live
  sends 38 host values. Index i corresponds to the stored parameter in the order of the N5 table
  (0 ResonanceType … 37 MidiMode). Each stored value is first clamped to its domain
  (SPEC-BUNDLED-DEVICE-PARAMETERS). Then:
  - **Enumerations and Booleans** pass as the index or as 0/1. These are ResonanceType,
    ResonatorQuality, LfoType, LfoSync, LfoStereoMode, FilterOn, LfoOnOff, MidiPitch, MidiGate and
    MidiMode.
  - **FilterMidFreq** in Hz passes as log₁₀(f/50)/log₁₀(360). 1000 Hz gives binary32 0.5089499354362488.
  - **DecayOnNoteOff** passes as 1 − v.
  - **Transpose, FineTranspose, PitchBendRange and LfoSyncRate** pass as the stored value rounded
    to the nearest 1/32768, then truncated toward zero.
  - **All others** pass unchanged.
- **X.** MidiMode (index 37) has no effect on the output (bit-identical with 1 and 0).
- **S-cond (A1).** ExcitationX, ListeningXL and ListeningXR pass unchanged.
- **U.** Whether A1 holds. Effect on T1: renders are defined for host position values. A stored
  position other than the default can be tied to a render only under A1. Without A1, sets that
  change these three parameters from their defaults are not verifiable.

### REQ-DEVICE-CORPUS-003 — controller values

The device turns each host value v into a controller value c between 0 and 127 (X; the
formulas are confirmed by the agreement of REQ-004 to 010):

| Rule | Host values | c |
| --- | --- | --- |
| U | 0..1 (values above 1 act as 1) | 128v if v ≤ 0.5, else 126v + 1 |
| B | −1..1 | 63.5v + 63.5 if v < 0, else 63v + 64 |
| P | positions | 64 + 31.5v |
| I | Radius | 127(1 − v) if 1 − v ≤ 0.5, else 126(1 − v) + 1 |

- **X.** The resonator controls take ⌊c⌋, so each has 128 steps. These controls are Decay,
  FreqDamping, Inharmonics, Ratio, Radius, AmpFreq, ExcitationX, ListeningXL, ListeningXR,
  TubeOpening and Bleed. Two host values with the same ⌊c⌋ give the same output: Decay 0.503
  renders bit-identically to Decay 0.5. The other controls use c unrounded.
- **Definitions (X).** Curves used below, with n = 0.5 when c = 64 and n = c/127 otherwise:
  - lin(c; lo, hi) = lo + n·(hi − lo);
  - exp(c; lo, hi) = lo·(hi/lo)^(c/127), which has no midpoint case.

### REQ-DEVICE-CORPUS-004 — dry and wet mix, drive, width and level

- **X.** DryWet: with a = U(DryWet)/127, the dry gain is P(0.25 − a/4) and the wet gain P(a/4).
  Here P(t) = t·(10.392633 − 31.177902t + 20.785267t²). DryWet 0 passes the input at
  0.974309 (−0.226 dB). DryWet 1 removes the dry signal.
- **X.** Drive multiplies the wet signal, before the band filter and the resonator, by
  exp(U(Drive); 0.17783, 5.6234),
  which is −15 to +15 dB with no saturation. The default 0.5 gives +0.12 dB.
- **X.** StereoWidth w mixes the two resonator outputs:
  - left = (½ + ½w)·left resonator + (½ − ½w)·right resonator;
  - right is the same with the sides exchanged.

  It acts on the wet part only.
- **X.** The left resonator is fed by the left wet input and the right resonator by the right.
  Output = dry gain × input + width mix of the resonators, on each channel. An impulse on the
  left input alone leaves the right output at the floor (≤ 2 × 10⁻²⁰) when StereoWidth is 1, and
  the left output bit-identical to the stereo case. The output carries an added floor of about
  10⁻²² that does not depend on the input.
- **X.** Sine steady-state gains match these rules and REQ-005 to 008 within 2.2 × 10⁻⁴ dB and
  0.06° (cases DCO-016).

### REQ-DEVICE-CORPUS-005 — modal resonance types, modes and quality

- **X.** ResonanceType 0 to 4 (Beam, Marimba, String, Membrane, Plate) are modal. For constant
  parameters, each resonator is a sum of independent two-pole resonances (modes), plus one weak
  bleed resonance (REQ-007). Mode k's nominal angular frequency is
  w_k = 2π·261.62·A(p)·r_k·A(i·log₂ r_k) rad/s. Here:
  - p is the pitch in octaves (REQ-006);
  - i is the inharmonicity (REQ-007);
  - A is the 2ˣ approximation of REQ-006;
  - r_k is the mode's ratio.
- **X.** Ratios r_k, k = 0, 1, …:
  - **Beam:** (β_k/4.730)², with β = 4.730, 7.853, 10.996, then (k + 1.5)π: 1, 2.756, 5.404, 8.933,
    13.34, ….
  - **Marimba:** (β_k/4.730)², with β = 4.730, 9.413, 15.450, 20.710, 24.580, then
    (1.4142k + 2.1213)π: 1, 3.960, 10.67, 19.17, 27.00, ….
  - **String:** k + 1.
  - **Membrane and Plate,** with R = exp(⌊U(Ratio)⌋; 1, 20) and N modes:
    - Let M = ⌊√(R·N)⌋ and Q = ⌊√(N/R)⌋; each is increased by 1 when its successor squared
      equals its argument.
    - Every pair (m, n) with 1 ≤ m ≤ M + 1 and 1 ≤ n ≤ Q + 1, listed m-major, gives a ratio.
      Membrane: √(m² + (Rn)²)/√(1 + R²). Plate: (m² + (Rn)²)/(1 + R²).
    - The pairs are sorted by ratio, stably, and the first N are kept.
- **X.** ResonatorQuality 0 to 3 (Eco, Low, Med, High) allows at most N = 4, 16, 30 or 70 modes.
  The first mode with w_k ≥ (5π/6)·fs (frequency at or above 5/12 of the sample rate) and all
  later modes are absent. For example, Beam at High has 12 modes at 44.1 kHz, the highest at
  18,033 Hz.
- **X.** For constant parameters, each channel's resonator output for input x has this transfer
  function, with z⁻¹ a one-frame delay:

  H(z) = 3000·[Σ_k c_k·E_k(h)·E_k(l)·(1 − z⁻²)/(1 + a1_k z⁻¹ + a2_k z⁻²) + bleed term]

  The terms, with fs the sample rate:
  - θ_k = w_k/fs;
  - α_k = (π/(π − θ_k))·sin θ_k·d_k/w_k, with d_k from REQ-007;
  - a1_k = −2 cos θ_k/(1 + α_k);
  - a2_k = (1 − α_k)/(1 + α_k);
  - c_k = α_k·1.01097·t_k/(2d_k(1 + α_k)), with the brightness tilt t_k from REQ-007;
  - E_k(h) and E_k(l) are the mode's weights at the strike point h and the pickup point l
    (REQ-008).

  The frequency and decay of each mode are those of the poles of its denominator. A mode with
  E_k(h)·E_k(l) = 0 is absent.

### REQ-DEVICE-CORPUS-006 — pitch

- **X.** Frequency v sets the pitch p = lin(U(v); −4, 4) octaves relative to 261.62 Hz.
  Frequency 0.5 gives 261.62 Hz (render 261.624 Hz, String).
- **X.** Detune d = lin(B(Detune); −1/12, 1/12) octave raises the left resonator by d and lowers
  the right by d. Detune 0.5 gives 269.346 Hz left and 254.176 Hz right.
- **X.** Octaves become frequency ratios by
  A(x) = 2^⌊x⌋·(1 + t + t²·(0.5 + 0.200064t)), with t = (x − ⌊x⌋)·ln 2. A is exact at whole
  octaves and up to about 1 cent sharp between them. Frequency 0.5625 gives 377.341 Hz
  (exact 2ᵖ would give 377.122 Hz).
- **X.** The pitch is limited to −5 to +67/12 octaves, LFO included.

### REQ-DEVICE-CORPUS-007 — decay, material, brightness, inharmonicity and bleed

- **X.** Decay T = exp(⌊U(Decay)⌋; 0.05, 35) s. FreqDamping (material) m = lin(⌊B(v)⌋; −1, 1).
  With L_k = log₂ r_k:
  - e_k = (5 − L_k)·min(m, 1) for m ≥ 0;
  - e_k = −max(m, −1)·L_k for m < 0;
  - d_k = 8·A(e_k)/T.
- **X.** Inharmonics i = lin(⌊B(v)⌋; −1, 1), and it enters as i³ limited to −1..1.
- **X.** AmpFreq (brightness) b = lin(⌊B(v)⌋; −1, 1) gives the tilt t_k = A((L_k − 2)·b).
- **X.** Bleed adds a resonance at the last mode's angle θ_K, but only when no mode was dropped
  under REQ-005:
  - its damping is α_H = 32·(π/(π − θ_K))·sin θ_K·d_K/w_K;
  - its numerator is b_H·g·(1 − z⁻¹)², with b_H = ((1 + cos θ_K)/2)·1.01097·t_K/((1 + α_H)·w_K)
    and g = exp(⌊U(Bleed)⌋; 0.01, 1), so its minimum is 0.01, not 0;
  - its denominator has the form of REQ-005, with α_H.
- **X.** Measured at 44.1 kHz, String, FreqDamping 0: the 261.6 Hz mode falls by 60 dB in
  0.2223 s at Decay 0.25, 1.1585 s at 0.5 and 5.736 s at 0.75. Higher modes fall slightly faster.
  FreqDamping −1 shortens the higher modes (the second mode 0.5727 s at Decay 0.5). FreqDamping
  +1 shortens the lower ones.

### REQ-DEVICE-CORPUS-008 — strike and pickup positions

- **X.** The strike point is h = lin(⌊P(ExcitationX)⌋; 0.05, 0.95), limited to 0.02..0.98. The
  left resonator's pickup is l = lin(⌊P(ListeningXL)⌋; 0.01, 0.99). The right resonator's is the
  same with ListeningXR. Each channel has one pickup.
- **X.** For Beam, Marimba and String, mode k's weight at a point u is a linear interpolation
  on a coarse grid:
  - G = N + 2 points;
  - T_k(j) = sin(π(k + 1)j/(N + 1)) for j = 0 … N + 1;
  - q = u·(G − 1), j = min(⌊q⌋, G − 2), f = q − j;
  - E_k(u) = ½·(T_k(j) + f·(T_k(j + 1) − T_k(j))).
- **X.** For Membrane and Plate the weight of mode (m, n) is a bilinear interpolation:
  - G = ⌊√N⌋ + 3;
  - the grid values are sin(πmi/(G − 1))·sin(πnj/(G − 1));
  - the point is (u, 0.44375);
  - the result is halved.
- **X.** ExcitationX 0 strikes the centre, and the even harmonics of a String are absent (−119 dB
  or lower). Host values −1 to 1 reach strike points 0.277 to 0.723. Host values 0 to 1 reach
  0.5 to 0.723. Each channel follows only its own pickup value; the other channel is unchanged
  within 4.1 × 10⁻²¹.
- **S.** A change of a pickup value moves linearly to the new point over 4,000 frames (200 steps
  of 20 frames). This was not rendered.
- **S-cond (A1).** For stored values, ExcitationX and the pickups are the host values above.

### REQ-DEVICE-CORPUS-009 — Pipe and Tube

- **X.** ResonanceType 5 (Pipe) and 6 (Tube) are waveguide resonances, without the modes of
  REQ-005. At the default Radius and Opening:
  - Pipe has strong second and third harmonics;
  - Tube's even harmonics are at least 68 dB below its fundamental, and its third is −16 dB;
  - both output channels are identical (Detune 0, LFO off).
- **S.** ResonatorQuality, FreqDamping, Inharmonics, AmpFreq, the positions and Bleed have no
  effect on Pipe and Tube. This was not rendered.
- **X.** Fundamentals at Frequency 0.5, Decay 1:

  | Setting | 44.1 kHz | 48 kHz |
  | --- | --- | --- |
  | Pipe, Radius 0.5, Opening 1 | 251.096 Hz | 251.271 Hz |
  | Tube, Radius 0.5 | 241.364 Hz | 241.687 Hz |
  | Pipe, Radius 1 | 258.339 Hz | — |
  | Pipe, Opening 0.3 | 234.444 Hz | — |
  | Tube, Radius 0 | 173.067 Hz | — |

  Both types lie below the nominal 261.62 Hz, by more as Radius decreases.
- **U.** A closed-form description of the Pipe and Tube waveforms, and Radius and Opening values
  other than those rendered. Effect on T1: Pipe and Tube are graded only against the cases'
  reference renders (DCO-018). The appendix has a static description, which a later revision
  may state as behavior.

### REQ-DEVICE-CORPUS-010 — band filter

- **X.** FilterOn inserts a band filter in the wet path, after Drive and before the resonator.
  It is a second-order low-pass at f·A(bw/2) followed by a second-order high-pass at f/A(bw/2):
  - both are RBJ cookbook forms with Q 0.707;
  - both corner frequencies are limited to 50..18,000 Hz;
  - f = exp(U(v₂₈); 50, 18000) Hz and bw = lin(c; 0.5, 9) octaves, where c = 14.941176v₂₉ − 7.470588
    is used directly as the controller.

  Off, the wet signal passes unchanged.
- **X.** Cases DCO-019 (defaults; 200 Hz with bandwidth 1) agree with this description within
  6 × 10⁻⁵ rel RMS and 0.004 dB per third octave.
- **S.** Coefficient changes ramp over 30 frames. Switching on or off fades over ⌊fs/100⌋ frames.
  The ramps were not rendered.

### REQ-DEVICE-CORPUS-011 — LFO

- **X.** With LfoOnOff on and LfoSync Free, the LFO adds to both resonators' pitch:
  - amount·S(φ) octaves, with amount = lin(U(LfoAmount); 0, 1);
  - S(φ) = 6.094263φ + 6.094263φ² − 85.31969φ³ + 121.88526φ⁴ − 48.754105φ⁵ for the Sine shape;
  - the phase φ advances by rate/fs per frame, from 0 at the first processed frame, with
    rate = exp(U(LfoRate); 0.01, 10) Hz;
  - in Phase mode (LfoStereoMode 0) the right channel's phase is φ + lin(Deg(LfoPhase); 0, 1),
    where Deg(v) = 127v/360 for v < 180 and 0.35v + 1 otherwise.

  The resonators read the pitch every 200 frames and hold it in between. Case DCO-020: rate
  2.539 Hz, ±0.302 octave, right channel half a cycle later, within 0.1 Hz of this rule.
- **S.** The shape list: Square (−1 then +1), Triangle, Ramp Up, Ramp Down, Sample & Hold (phase
  at twice the rate) and Random Ramp. Spin mode runs the right channel at rate·(1 + spin). These
  were not rendered.
- **X, U.** Sample & Hold and Random Ramp draw from a generator that the device seeds from the
  clock each time it builds its engine: at creation and at every sample-rate change. Their
  output depends on that seed (X). Inferred: in Live it differs between instances and sessions.
  Effect on T1: these two shapes are graded only as non-silent, bounded output; no exact
  render is expected.
- **U.** LfoSync on (tempo-synced rate and phase reset at transport start). The transport values
  Live passes are unknown. Effect on T1: synced LFO settings are not verifiable.

### REQ-DEVICE-CORPUS-012 — behavior over time

- **X.** After creation the output remains at its approximately 10⁻²² numerical floor for
  100 frames (not bitwise zero). From frame 100 the dry and wet gains
  rise linearly over 100 frames to their values (DryWet 0: 0.009743 at frame 100, 0.974309 from
  frame 199).
- **S.** A parameter value sent between host blocks takes effect at the next block. Changes then
  ramp:
  - Drive and StereoWidth over 10 ms;
  - Frequency, Detune, FineTranspose and LfoAmount over 1 ms;
  - DryWet gains toward new values over 100 frames, retargeted every 100 frames;
  - pickups over 4,000 frames;
  - the other resonator values step at the next coefficient update, which comes at most every
    200 frames.
- **X.** Changing the sample rate rebuilds the device and restores its state with six significant
  digits. The output then differs from a device created at that rate by at most 1.2 × 10⁻⁶
  (rel RMS 3.3 × 10⁻⁵). This is inside the metric.
- **X.** A device reset alone turns a Tube into a Pipe until ResonanceType is sent again. Live
  sends it again after every reset (S, REQ-001), so this is not audible.
- **S.** The device reports that it may stop processing after fs/10 frames whose magnitude is at
  most 10⁻⁵ on both channels.

### REQ-DEVICE-CORPUS-013 — MIDI side-chain features

- **U.** These were not rendered:
  - the effect of MIDI notes, pitch bend and sustain received through Corpus's side-chain input;
  - MidiPitch (pitch from the note), MidiGate (gate from held notes) and DecayOnNoteOff (decay
    while the gate is closed);
  - Transpose, FineTranspose and PitchBendRange (active only with MidiPitch);
  - MidiMode (Live-side note priority).

  The bundle's note handling and Live's routing of side-chain MIDI are untraced. Effect on T1:
  sets that route MIDI to Corpus, or that turn MidiPitch or MidiGate on, are not verifiable.
- **X.** With MidiPitch and MidiGate off, these parameters do not change the output. Transpose 12,
  FineTranspose 50, PitchBendRange 24, DecayOnNoteOff 1 (host 0) and MidiMode 1 together render
  bit-identically to the defaults.

## Timing and state

- **Units.** Frames at the stated sample rate. Pitch in octaves relative to 261.62 Hz.
- **Latency.** None. An input impulse at frame n gives its dry part and the first resonator
  output at frame n (X).
- **Persistent state.** None beyond the stored parameters. The device's ringing state lives only
  in a running instance.
- **Determinism.** Deterministic for a given input, parameter set and history (REQ-001, 012),
  except the random LFO shapes (REQ-011).

## Comparison metric

Proposed as a general T1 device-audio criterion of ADR 0004. The finite
use of this criterion is separately bounded by the
[handoff plan](device-corpus-handoff-plan.md#review-outcome--2026-10-19); approval
of that finite package does not approve unlisted modes or scenarios. A candidate render
of a case passes when it meets every line that applies, measured on the case's frames after
any start-up ramp.

| Signal | Comparator | Tolerance |
| --- | --- | --- |
| Modal types, impulse input | Each mode with weight at least 10⁻³ of the strongest, measured in candidate and reference with the same demodulation estimator (appendix). A mode is graded only if the estimate from the reference render is within 10⁻⁴ of its REQ-005 pole frequency; closely spaced or heavily damped modes are not resolved | Frequency within 4 binary32 ulp bounds. The bound is 3·2⁻²⁵/θ² + 2⁻²³ relative, with θ = 2πf/fs. At 44.1 kHz the tolerance is 4.0 × 10⁻³ at 66 Hz and 2.6 × 10⁻⁴ at 262 Hz. Per-frame log radius ρ within 8·2⁻²⁵/\|ρ\| relative. Complex amplitude within 5 × 10⁻³ |
| Modal types, impulse input | Waveform, the 256 frames from the impulse | Rel RMS within 2 × 10⁻³ |
| Steady-state sine | Complex gain fitted over the last 8,192 frames | 0.01 dB and 0.5° |
| Noise | Third-octave band levels, 80 Hz to 16 kHz, from frame 8,192 | 0.01 dB |
| Pipe, Tube, filter, dry path | Waveform after the impulse or after frame 8,192 | Rel RMS within 10⁻⁴ |
| LFO pitch | Instantaneous fundamental, averaged over 200 frames | 0.2 Hz at 261.62 Hz |
| Timing | Start-up silence and ramps | Exact frames |

Why not a sample-by-sample maximum error. The device's coefficients are binary32. One ulp
in each denominator coefficient moves a low mode's frequency by up to 3·2⁻²⁵/θ² relative.
Over a long ring that grows into a large phase error, although the sound does not change.
The original is itself sensitive at that scale:

- one-ulp changes of the substituted libm results move a 66 Hz mode by 6.8 × 10⁻⁴ and change
  the waveform by 4 % after 0.28 s;
- the arm64 release slice has 232 fused multiply-adds that the x86_64 slice lacks.

The largest differences between the reference renders and REQ-005 to 008 are 1.0 ulp bound in
frequency, 2.04 in log radius and 2.8 × 10⁻⁴ in amplitude, against which the tolerances leave a
margin of four or more. Membrane is the exception, at 1.19, 4.4 and 2.3 × 10⁻³: its closely
spaced modes limit the estimator, and the margin there is about two. On paths that do not
resonate the effects are 10⁻⁵ or smaller, so a waveform tolerance can be used there.

## Acceptance cases

Expectations are X renders of the original x86_64 code under REQ-001's protocol. None has been
run against Live, and under ADR 0003 none will be. Kinds: P positive, B boundary, T timing,
U not graded.

### Fixtures

All renders are 16,384 frames, stereo binary32, interleaved, with block 512, from
[t12-device-dsp-v1](../../analysis/ableton-live-12.4.3/r2/t12-device-dsp-v1/manifest.json)
`raw/corpus/<render>.f32`. Each one's `.script` gives the exact calls.

| Input | File | SHA-256 |
| --- | --- | --- |
| I1 unit impulse at frame 4,096, both channels (44.1 and 48 kHz) | `inputs/impulse44.f32` | `03a7d8daa68e7954…` |
| I2 sine 0.25·sin(2πfn/fs), f = 261.62, 400, 1000, 3000 Hz | `inputs/sine<f>_44.f32`, `sine1000_48.f32` | in `results/corpus_runs.json` |
| I3 white noise, RMS 0.1, seed 1214 | `inputs/noise44.f32` | `6805d44a29f0db85…` |
| I4 constant 0.5 | `inputs/dc44.f32` | `0288e3482c14fa82…` |

"Defaults" means the 38 host values that Live sends for a new Corpus (REQ-002). Each case
states only its changes in host values. "Probe" means DryWet 1, so that only the resonators are
heard.

### Cases

| Case ID | Requirement | Kind | Setup | Expected result / comparator | Reference render (SHA-256) |
| --- | --- | --- | --- | --- | --- |
| DCO-001 | 001, 004–008 | P | Defaults (Beam, Med), I1, 44.1 kHz | Modal metric. 12 modes: 261.617, 721.141, 1413.897, 2337.079 Hz, … | `defaults_44` (`2264a81b565341a9…`) |
| DCO-002 | same | P | Defaults, I1, 48 kHz | As DCO-001; first mode 261.620 Hz | `defaults_48` (`6f0c3c5755159b57…`) |
| DCO-003 | 005 | P | Probe; Beam, High, Decay 1 | 12 modes as DCO-001 | `mode_beam_44` (`0bfe85cbffe2dead…`) |
| DCO-004 | 005 | P | Probe; Marimba, High, Decay 1 | 8 modes: 261.624, 1036.107, 2791.294, 5015.438 Hz, … | `mode_marimba_44` (`9d5bf9671f8ae56e…`) |
| DCO-005 | 005 | P | Probe; String, High, Decay 1 | 70 modes at 261.624·(k + 1) Hz, within the metric | `mode_string_44` (`0dae8b9ca0f8361d…`) |
| DCO-006 | 005 | P | Probe; Membrane, High, Decay 1 (R = 4.524) | 261.621, 306.498, 340.950 Hz, …; graded on resolved modes | `mode_membrane_44` (`0e09e31e5bdb8978…`) |
| DCO-007 | 005 | P | Probe; Plate, High, Decay 1 | 261.624, 298.165, 359.070 Hz, … | `mode_plate_44` (`0bba47a8201f4294…`) |
| DCO-008 | 005 | P | DCO-003 and DCO-005 at 48 kHz | Modal metric | `mode_beam_48` (`2754ccc144af54fa…`), `mode_string_48` (`55a2719cc96ad35c…`) |
| DCO-009 | 006 | P, B | Probe; String, Eco, Decay 1; Frequency 0.25, 0.5625, 0.75, 1 | Fundamentals 66.167, 377.341, 1057.964, 4185.921 Hz | `pitch_0.25` (`4892f2c8…`), `pitch_0.5625` (`74421814…`), `pitch_0.75` (`93487532…`), `pitch_1` (`b36ea666…`) |
| DCO-010 | 006 | P | Probe; String, Eco, Decay 1; Detune 0.5 | Left 269.346 Hz, right 254.176 Hz | `detune_0.5` (`9bf6418bb89af344…`) |
| DCO-011 | 007 | P | Probe; String, Low; Decay 0.25, 0.5, 0.75; also 0.5 at 48 kHz | 261.6 Hz mode loses 60 dB in 0.2223, 1.1585, 5.736 s (1.1595 s at 48 kHz) | `decay_0.25` (`2b15b588…`), `decay_0.5` (`28b5578a…`), `decay_0.75` (`09cac9e2…`), `decay_0.5_48` (`11ca4e19…`) |
| DCO-012 | 007 | P | Probe; String, Low, Decay 0.5; FreqDamping −1, −0.5, 0.5, 1 | Modal metric; second mode 0.5727 s at −1 | `tone_-1` (`58893202…`), `tone_-0.5` (`4880eb0a…`), `tone_0.5` (`a5809e79…`), `tone_1` (`9a99604a…`) |
| DCO-013 | 008 | P, B | Probe; String, Low, Decay 1; ExcitationX −1, −0.5, 0, 0.5, 1 | Modal metric; at 0, harmonics 2, 4, 6, 8 at least 100 dB below the fundamental | `hit_-1` (`6e45645b…`), `hit_-0.5` (`edd753e4…`), `hit_0` (`402448e0…`), `hit_0.5` (`0ba4838b…`), `hit_1` (`eeea8682…`) |
| DCO-014 | 008 | P | As DCO-013 at ExcitationX 1; ListeningXL 0, 0.5, 1; ListeningXR 0, 0.5, 1 | Modal metric on the changed channel; the other channel within 10⁻²⁰ of the ListeningXL 0 (or XR 0) render | `listenL_*`, `listenR_*` (six renders) |
| DCO-015 | 005, 007 | P | Probe; String, Low, Decay 1; Inharmonics ±0.5; AmpFreq ±1. Membrane, Low; Ratio 0.2, 0.8. String, Eco; Bleed 1 | Modal metric; Inharmonics 0.5 second mode 569.454 Hz, −0.5 477.094 Hz | `inharm_*`, `bright_*`, `ratio_*`, `bleed_1` (seven renders) |
| DCO-016 | 004 | P | Defaults with Decay 0.1; I2 at 261.62, 400, 1000, 3000 Hz; 1000 Hz at 48 kHz; Drive 0 and 1; DryWet 0.25 | Sine metric. Left gain at 1000 Hz −1.3295 dB, −4.699°; Drive 1 −0.3036 dB, −23.819° | `sine_*`, `drive_0`, `drive_1`, `drywet_0.25` (eight renders) |
| DCO-017 | 004, 005 | P | Defaults with Decay 0.1; I3 | Noise metric | `noise_44` (`f8b95bc7163a5076…`) |
| DCO-018 | 009 | P | Probe; Pipe and Tube at Decay 1, 44.1 and 48 kHz; Pipe with Radius 0, Radius 1, Opening 0.3; Tube with Radius 0 | Waveform rel RMS within 10⁻⁴; fundamentals as REQ-009 | `wg_*` (eight renders) |
| DCO-019 | 010 | P | Defaults with Decay 0.1, FilterOn; also FilterMidFreq 200 Hz and FilterBandWidth 1; I3 | Waveform rel RMS within 10⁻⁴ from frame 8,192; noise metric | `filter_on` (`45261a14…`), `filter_200_bw1` (`10a645af…`) |
| DCO-020 | 011 | P | Probe; String, Low, Decay 1; LFO on, Sine, rate 0.8, amount 0.3 | LFO metric: rate 2.539 Hz, ±0.302 octave, right half a cycle later | `lfo_sine` (`fadb3e890a943e63…`) |
| DCO-021 | 012 | T | Defaults with DryWet 0; I4 | Frames 0–99 have the numerical floor. Gain rises linearly from about 0.009743 at frame 100 to 0.974309 at 199; with input 0.5 the first output is about 0.00487155 | `startup_dry` (`93469eb93211f0e0…`) |
| DCO-022 | 001 | P | DCO-001 in host blocks of 64, 256, 333 and 2,048 frames | Identical to DCO-001 within the metric | DCO-001 |
| DCO-023 | 001, 012 | P | New instance; set 44.1 kHz, then 48 kHz, then apply all default parameters and I1 | Within the metric of DCO-002. This is the retained `defaults_48_via_44` variant, not the after-parameters rate change | DCO-002; exact-output equivalence retained in `corpus_runs.json` |
| DCO-024 | 001, 012 | P | DCO-001 and the 44.1 kHz Tube of DCO-018, each preceded by 1,024 silent frames, a reset and ResonanceType again | Within the metric of the case without them | DCO-001, `wg_tube_44` |
| DCO-025 | 011 | U | LFO Sample & Hold | Not graded: seeded from the clock (REQ-011). Non-silent, bounded output only | `lfo_sah` (one seed, not an expectation) |
| DCO-026 | 013 | U | MidiPitch or MidiGate on; MIDI to the side-chain | Not graded (REQ-013) | — |
| DCO-027 | 011 | U | LfoSync on, transport playing | Not graded (REQ-011) | — |
| DCO-028 | 002, 008 | U | A Live Set storing ExcitationX 0 | Graded only if A1 is accepted: as DCO-013 at host 0 | `hit_0` |

## Open questions

Proposed for [questions](../questions.md) (not edited by this draft):

- **A1, position range.** This is the open Q of REQ-BUNDLED-DEVICE-PARAMETERS-015. Both readings now
  have X consequences: host 0..1 reaches strike points 0.5–0.723, and −1..1 reaches 0.277–0.723.
- **Live-side protocol.** The event frame base (Corpus subtracts one from non-zero frames), the
  transport and input-flag values, the block sizes, and when the reset sequence runs.
- **MIDI side-chain path (REQ-013).** It needs both a bundle trace (event to note) and a Live
  trace (side-chain routing).
- **Pipe and Tube (REQ-009).** Restate the static waveguide description as behavior, or keep these
  render-only.
- **libm.** Apple's libm against glibc for the functions the device calls. The metric assumes
  that they differ by at most one ulp.

## Analyst evidence appendix

Analysis-only. Do not copy into a handoff. Canonical evidence:
[device DSP by extracted execution](../research/device-dsp-extracted.md) and
[Corpus DSP (static)](../research/corpus-dsp-static.md). Retained run
`analysis/ableton-live-12.4.3/r2/t12-device-dsp-v1/`, harness `harness/xdev*.c`, built to
`/var/tmp/sound-analysis/t12-xdev/xdev`. Slice: `Corpus.bundle/Contents/MacOS/Corpus`
(SHA-256 `2164ec08…3ef422`), x86_64 at offset 16,384, 250,352 bytes, SHA-256
`03be50fae8abee39dcaafec743d82ab4c908d548977354528aa1b8dd3919b00d`.

| Clause | Evidence |
| --- | --- |
| 001 protocol, invariances | `results/corpus_runs.json` `determinism` (25 checks); exports `0x23b0`, `0x2490`, `0x29c0`, `0x2d60`, `0x2d80` (x86_64) |
| 002 | N5 `out/conversions.tsv` (Corpus rows, asserted equal to the harness defaults by `run_corpus.py check_defaults`) |
| 003–008 | `model.py` (static model; binary32 coefficients) against renders, `results/corpus_model.json` `modes`, `impulse_response`, `sine`, `noise`, `even_mode_null`; report sections 0–4 of `corpus-dsp-v1/report-resonator.md` and sections 0–3 of `report-chain.md` |
| 009 | `results/corpus_port.json` `wg_*` (port within 1.9 × 10⁻⁵; `harmonic_levels_db_re_f0`, `channels_identical`); waveguide `0x23670` (arm64) in the resonator report §5 (two 2,048-frame lines, 5-tap Lagrange reads, reflection filter from Radius and Opening, loss exp(−4/(T·261.62·2ᵖ)), 30 Hz DC blocker, Tube inverted) |
| 010 | `filter_on`, `filter_200_bw1` against the port; report-chain §3 filter |
| 011 | `results/corpus_model.json` `lfo`; seed checks `lfo_sah_seed1760000000`; `srand(time(0))` at `0x199c0` (x86_64), called from engine build `0x1d2e0` |
| 012 | `startup`; rate-history and reset variants; report-chain §0–2 |
| Metric | `results/libm_sensitivity.json`; `results/fma_scan.txt` (arm64 232 fused, x86_64 0); estimator `fit.py` (demodulation, Hamming FIR, cutoff min(100 Hz, 0.4 × the gap to the nearest significant mode)) |
| arm64 equivalence | Static: same constants and structure (the C1 corpus readings of the reports); differences limited to fused multiply-adds (count above) and Apple's libm builds. Not executed |

## Revision and handoff

| Revision | Date | Change |
| --- | --- | --- |
| 1 | 2026-10-18 | First draft from the T1.2 feasibility gate (packet t12-device-dsp-v1). 13 requirements: 9 X with S origins (001, 003–008, 010, 012), 1 S with an X clause, an S-cond clause and a U part (002), 3 X with U parts (009, 011, 013). 28 cases: 24 graded by X renders, 4 not graded (DCO-025 to 028; DCO-028 graded only under A1) |
| 2 | 2026-10-19 | Pilot-staging precision corrections against retained corpus_runs.json and raw/startup_dry.f32: FilterMidFreq 1000 Hz corresponds to host binary32 0.5089499354362488; startup frames 0–99 have the numerical floor, not exact zero. No general metric approval or case expectation beyond those clarifications. 13 requirements and 28 cases unchanged. |
| 3 | 2026-10-19 | Independent review distinguishes DCO-023's before-parameters rate sequence from the earlier after-parameters scenario; the latter remains excluded from device-corpus-v1 because its changed output is not retained in the payload. DCO-021 states gain separately from output for its 0.5 input. The reviewed finite metric does not approve the broader draft formulas or unlisted scenarios. |

The finite pilot is recorded under the [handoff plan](device-corpus-handoff-plan.md).
It is reviewed and published locally as device-corpus-v1.
The reviewed snapshot pins this revision 3, including the listed review
clarifications. Only finite clauses of REQ-001 and 004 to 012 are
approved, in 24 groups and 68 evaluations. General equations, REQ-002, REQ-003
and REQ-013 are not released. A1 and Live integration remain unaccepted.

DCO-023 deliberately uses `defaults_48_via_44`: both rate calls precede all
parameters. The distinct `defaults_48_rate_after_params` scenario reports
max error 1.2e-6 and relative RMS 3.3e-5 in the retained determinism summary,
but its changed output is not a payload reference. That scenario is excluded
from the finite release; the two histories are not silently equated.

Released locally 2026-10-19 as [device-corpus-v1](../../handoff/device-corpus-v1/README.md):
24 groups/68 finite evaluations, partial REQ-001 and 004–012. Stored mapping,
general synthesis laws, omitted modes and Live/arm64 integration remain excluded.
See [handoff plan](device-corpus-handoff-plan.md#local-publication).
