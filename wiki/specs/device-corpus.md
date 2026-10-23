---
id: SPEC-DEVICE-CORPUS
type: spec
status: draft
updated: 2026-10-23
access: analysis
revision: 21
target: Ableton Live 12 Suite 12.4.3 / macOS; reference renders from the Corpus.bundle x86_64 slice
---

# Corpus audio effect: signal behavior and reference renders

**Revision 8 finite-observation scope — 2026-10-21:** DCO-034–036 add only
Square, Triangle and Ramp Down outputs at one fixed supplied-host fixture.
Their new waveform expectations and candidate/portable comparators remain NULL.
The 36 draft rows comprise 29 existing cases with criteria, three new native
observation-only cases and four existing U cases.
The R7 adoption and private-proposal paragraphs below retain their historical
as-of scope. The immutable current `device-corpus-v5` release's 73 evaluations
and all earlier finite criteria are unchanged; this annex is not a new release.

**Current owner disposition — 2026-10-20:** R7 is independently reviewed and adopted
into this canonical draft; [adoption record](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/corpus-owner-r7-adoption.json).
All private/proposed/pending adoption statements below retain their respective
author-freeze status; they do not describe the current owner disposition.
At adoption, v4 is the current release; DCO-033 is not released by this adoption.

**Private R7 proposal; not adopted or released.** R6 is a separately adopted
immutable provider. Earlier author-freeze/release statements below retain their
historical scope. R7 adds only DCO-033, an exact same-instance pickup update
under REQ-001/012. The finite method has separate independent actual-result approval; owner
review/adoption remain pending. No application or candidate grade is asserted.

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

- MIDI side-chain behavior beyond the three exact extracted host-input cases
  DCO-030, DCO-031 and DCO-032: general MidiPitch, MidiGate, Transpose, FineTranspose,
  PitchBendRange, DecayOnNoteOff, MidiMode and Live side-chain routing remain U
  (REQ-013). The cases define finite bundle outputs, not Live routing;
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
- **X; proposed finite engineering scope.** DCO-030 and DCO-031 use the complete
  38-value host vector and event fixture below: new instance, 44,100 Hz, parameters
  in index order, one held note-on at absolute host/test frame1537, then one
  16,384-frame process in blocks512 with I1 at4096. The only difference between
  those two histories is key60 versus72. MidiPitch=1 and MidiGate=0; LFO is off.
  Stopped transport is `{playing:0, position:0, tempo:120}` and is not advanced;
  input flag1, MXCSR0x1f80 and time seed0 characterize the reference calls.
  No reset, warm-up, note-off, bend, sustain, second note or parameter update
  occurs. The event has status0x90, channel0 and velocity100, and remains held
  through destruction. The canonical input coordinate is1537 (block1536/local1);
  do not subtract again in an adapter. Live's event base and actual delivery are U.
  No block-size, repeatability, rate/reset, clock, FTZ/DAZ, MXCSR, startup or other
  invariance below is extended to these two new vectors. Their dedicated modal
  comparisons alone apply; DCO-029's separate Ramp rule is unchanged.
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

- **X; proposed finite project criterion, DCO-033 only.** One fresh instance
  receives the complete 38-value Membrane host vector, I1 at 44,100 Hz,
  16,384 frames in 512-frame blocks. Process 8,192 frames, set host index15
  ListeningXL to exactly0.75, then process the remaining8,192 on the SAME
  instance/input stream. No reset, rate change, input restart or extra update
  occurs. The source fixture and dedicated four-check waveform rule below are
  the only expectation for this history; no new general protocol invariance.

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

- **X finite supplied-native-host observations; U portable acceptance.**
  DCO-037–093 retain 57 once-only outputs from the complete seven typed
  integer-domain catalog in the R9 annex. These are supplied host values at
  indices0,10,17,18,21,27,33 under one fixed input/history, not observed stored
  conversion, ordinary Live emission or acceptance of A1/A2. No general
  controller, LFO, seed, waveform or parameter-effect law follows. Every new
  case carries the annex's original-checker-failure/postcapture-DATA qualification.
  Pre-call waveform priors, new waveform expectations, portable expected
  results, comparators and grades remain NULL. All earlier mapping statements and unknowns retain their
  existing scope; no old audio budget transfers to these observations.

- **X finite supplied-host observations; U portable acceptance (revision 10).**
  [DCO-094–294](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-corpus-r10-complete-finite-hosts-v1/new-cases201.json) add201 once-only outputs from the
  complete14 finite host-domain axes in the annex. The63 prior vectors remain
  inherited references joined by full vector hash, not new catalog position.
  These inputs do not validate actual Live emission, clamp/rounding between
  supplied members, stored/UI conversion, A1/A2, productive effects or general
  pitch, MIDI-gate, shape or timing laws. All new priors and portable expected/
  comparator/grade remain NULL; existing general clauses and U retain scope.

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

- **X finite supplied Decay observations; U portable acceptance (revision 15).**
  [DCO-1243–1369](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-corpus-r15-decay-controller-cells-finite-v1/new-cases127.json) add 127 once-only no-event I1 histories,
  changing only host index1 (Decay) over the 127 new representatives in the
  complete 128-cell input catalog. Cell127 retains ONE qualified
  CFH-V002/CNI-V002/DCO020 INPUT reference, without replay, new PID/receipt/
  metrics or waveform criterion/modal-budget transfer. REQ-003's cell formula
  identifies these supplied inputs only; this adds no native quantizer,
  within-cell, general Decay, physical/calibration or public Live/ARM law.
  New waveform priors/expectations, portable expected/comparator/grade remain
  NULL; new application-predicate proofs remain false. Earlier criteria,
  modal budgets, required U and timing/state/history scopes are unchanged.

- **X finite supplied resonator-host observations; U portable acceptance (revision 16).**
  [DCO-1370–2259](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-corpus-r16-seven-resonator-cells-finite-v1/new-cases890.json) retain890 once-only no-event I1
  histories from seven independent supplied-host representative classes.
  This requirement's related inputs are qualified by the R16 annex and exact
  case mapping; no continuous-domain, within-cell, physical/calibration,
  productive-effect or public Live/ARM law is added. One qualified no-event
  baseline INPUT reference has six aliases, without replay, new PID/receipt/
  metrics or criterion transfer. All new waveform priors/expectations,
  portable expected/comparator/grade remain NULL; new application proofs
  remain false. Earlier general clauses, required U and budgets retain scope.

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

- **X finite supplied resonator-host observations; U portable acceptance (revision 16).**
  [DCO-1370–2259](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-corpus-r16-seven-resonator-cells-finite-v1/new-cases890.json) retain890 once-only no-event I1
  histories from seven independent supplied-host representative classes.
  This requirement's related inputs are qualified by the R16 annex and exact
  case mapping; no continuous-domain, within-cell, physical/calibration,
  productive-effect or public Live/ARM law is added. One qualified no-event
  baseline INPUT reference has six aliases, without replay, new PID/receipt/
  metrics or criterion transfer. All new waveform priors/expectations,
  portable expected/comparator/grade remain NULL; new application proofs
  remain false. Earlier general clauses, required U and budgets retain scope.

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
  are not graded as general waveforms. Ramp Up retains the single finite audio
  expectation DCO-029 below. Square, Triangle and Ramp Down now have only the
  supplied-host observations DCO-034–036, with new waveform expectations and
  comparators NULL; Spin and other Ramp Up vectors remain unrendered here.
- **X; proposed finite project criterion.** DCO-029 fixes one Free Ramp Up comparison
  input and its captured output, without recovering an internal LFO waveform law.
  It differs from DCO-020 only in host LfoType=3 instead of 0; all other host
  values and input/protocol remain fixed. Its per-channel waveform RMS criterion
  is stated separately below. This does not accept A1 or assert Live uses this
  host protocol. The [capture review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/corpus-lfo-ramp-up-review.json)
  supports only the declared extracted calls.
- **X observations; U acceptance criterion.** DCO-034–036 retain the three fixed
  Free-LFO host-input outputs in the finite annex below. Their native waveform
  priors, new waveform expectations and candidate/portable comparators remain
  NULL. They do not recover internal shape laws, add a Hz/RMS budget, extend
  REQ-001's invariance claims or transfer DCO-020/029's criteria. A1, actual Live
  delivery, ARM/Apple, clock and state/lifecycle uncertainties remain unchanged.
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

- **X; proposed finite engineering exception, DCO-033 only.** The fixed
  ListeningXL update above has a retained finite reference, not a transition
  model. Compare the productive baseline[4096,8192) and response[8192,16384)
  independently in both channels under the dedicated `pickup_step_waveform`
  rule. The actual history is a host parameter update during nonzero ringing;
  it does not establish the 4,000-frame movement, 200 steps, next-update timing,
  eight-frame latency, linearity or terminal target state. Those earlier S
  statements and every prior finite budget keep their existing scope.

### REQ-DEVICE-CORPUS-013 — MIDI side-chain features

- **X; proposed finite project criterion.** DCO-030 and DCO-031 retain their proposed
  finite event-bearing expectation: one held note60 or72 under REQ-001's exact
  fixture, compared to that captured output with the fixed modal lists below.
  This does not recover a general note-to-pitch, velocity, gate or event-timing law.
  DCO-030's scored bytes equal an older fixed-pitch render after4096: that case
  alone cannot detect ignoring MIDI. DCO-031 supplies a distinct finite output;
  its wrong-note60 rejection is a bounded control, not proof of every MIDI path.
- **X; proposed finite engineering exception.** DCO-032 adds only the exact
  note60 On1537/Off3073 history with host MidiPitch=1, MidiGate=1, host index34=+0
  and LFO off, using the complete fixture below. Compare its captured B output
  only with `noteoff_decay_zero_waveform`, not a modal or general gate rule.
  This is the third finite history; it proves no stored/UI conversion, actual
  Note Off admission, general decay law or Live route. The observed output flags
  do not prescribe silence, stopping or scheduling. Earlier behavior statements
  and DCO-030/031 comparisons remain unchanged.
- **U.** Beyond these three declared extracted histories, the general features remain unknown:
  - the effect of MIDI notes, pitch bend and sustain received through Corpus's side-chain input;
  - MidiPitch (pitch from the note), MidiGate (gate from held notes) and DecayOnNoteOff (decay
    while the gate is closed);
  - Transpose, FineTranspose and PitchBendRange (active only with MidiPitch);
  - MidiMode (Live-side note priority).

  Live's side-chain routing/event base, other histories and the full bundle-event
  admission/handling path remain unproved. Effect on T1: general sets routing MIDI
  to Corpus or enabling MidiPitch/MidiGate remain unverifiable beyond these exact
  three finite host-input cases. DCO-026 remains U and unchanged.
- **X.** With MidiPitch and MidiGate off, these parameters do not change the output. Transpose 12,
  FineTranspose 50, PitchBendRange 24, DecayOnNoteOff 1 (host 0) and MidiMode 1 together render
  bit-identically to the defaults.

- **X finite supplied held-On observations; U portable acceptance (revision 11).**
  [DCO-295–562](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-corpus-r11-held-note-midi-finite-v1/new-cases268.json) add268 once-only histories in the
  exact38-word held-note fixture below:126 keys,127 On velocities and15 On
  channel nibbles, varied independently. DCO-030/031 remain two inherited
  references without replay or transfer of their modal budgets. These new
  observations do not establish public MIDI routing, dispatch, velocity-0
  note-off equivalence, pitch/channel/velocity law, event timing, stored
  emission or Live/ARM binding. All new waveform priors/expectations,
  portable expected/comparator/grade remain NULL. The older clauses, criteria
  and general U keep their prior scope; no old budget applies to new cases.

- **X finite supplied two-event observations; U portable acceptance (revision 12).**
  [DCO-563–958](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-corpus-r12-dco032-midi-finite-v1/new-cases396.json) add396 once-only histories from the
  fixed DCO-032 input context:127 On keys,127 On velocities,15 matching
  On/Off channel nibbles and127 Off velocities, independently. On-key
  variation leaves Off key60 fixed. Four baseline aliases share ONE old
  DCO-032 INPUT reference without replay, new PID/receipt/metric or criterion
  transfer. These observations do not establish velocity0 dispatch, release,
  unmatched-key behavior, public MIDI routing or general Live/ARM law.
  All new waveform priors/expectations, portable expected/comparator/grade
  remain NULL; new application-predicate proofs remain false. General U and
  all older criteria retain their prior scope; no old modal budget transfers.

- **X finite supplied residual two-event observations; U portable acceptance (revision 13).**
  [DCO-959–1115](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-corpus-r13-dco032-residual-midi-finite-v1/new-cases157.json) add 157 once-only histories at the fixed DCO-032 context:
  127 Off keys with On key 60 fixed,15 On channel nibbles with Off status 80
  fixed and15 Off channel nibbles with On status 90 fixed, independently.
  Three baseline aliases share ONE old DCO-032 INPUT reference, without
  replay, new PID/receipt/metrics or transfer of its criterion. These are
  supplied-event observations, not matching-key/channel construction or a
  general release, voice, dispatch, current public receiver or Live/ARM law.
  All new waveform priors/expectations and portable expected/comparator/grade
  remain NULL; new application-predicate proofs remain false. All older
  clauses, criteria, general U and modal-budget scopes remain unchanged.

- **X finite supplied matching-key observations; U portable acceptance (revision 14).**
  [DCO-1116–1242](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-corpus-r14-dco032-matching-key-finite-v1/new-cases127.json) add 127 once-only histories at the fixed DCO-032 context:
  both existing On and Off keys change together over 0–127 except 60, without
  any other event-byte, timing, parameter or model change. The complete 128-key
  catalog retains ONE inherited DCO-032 INPUT reference at key60, without
  replay, new PID/receipt/metrics or criterion/modal-budget transfer. These
  are supplied-history observations, not a general matching-key, pitch, release,
  event-admission or public Live/ARM law. All new waveform priors/expectations,
  portable expected/comparator/grade remain NULL;
  new application-predicate proofs remain false. All older clauses, criteria,
  general U and modal-budget scopes remain unchanged.

## Timing and state

- **Units.** Frames at the stated sample rate. Pitch in octaves relative to 261.62 Hz.
- **Latency.** None. An input impulse at frame n gives its dry part and the first resonator
  output at frame n (X).
- **Persistent state.** None beyond the stored parameters. The device's ringing state lives only
  in a running instance.
- **Determinism.** Deterministic for a given input, parameter set and history (REQ-001, 012),
  except the random LFO shapes (REQ-011).

## R7 scope addition: one pickup-step metric

DCO-033 uses ONLY the dedicated fixed-window rule stated here. General startup,
modal, sine, LFO, filter/noise and earlier waveform rules do not add checks to
DCO-033. Conversely this new rule changes none of their earlier case scopes.
Decode exactly16,384 stereo frames of headerless little-endian binary32 data;
every full-file sample must be finite. The trusted step reference is131,072B,
SHA-256 `1336d90115bd24c058e556aa95e9140014d168dad7111dec64eb8edd1d977e73`.
An incorrect reference identity or invalid size/nonfinite data is unsatisfied.

There are FOUR independent checks: preL/preR over[4096,8192), postL/postR over
[8192,16384). In each region/channel, reference AND candidate energy must be
positive. Widen binary32 exactly to binary64; compute
`sqrt(math.fsum((candidate-reference)*(candidate-reference))/math.fsum(reference*reference))` with binary64
subtractions/products, `math.fsum`, division and `math.sqrt`. Each computed
binary64 error must be <=0.01, inclusive with NO epsilon. All four must pass;
no pooling windows/channels, fitting gain/phase/offset, alignment, interpolation,
frame deletion, onset shift or transition exclusion is allowed. Prefix[0,4096)
is finite-only. All response samples, including the first eight equal frames,
remain scored; no latency meaning is assigned to that finite observation.

This is a NEW1% per-window/per-channel aggregate waveform RMS engineering budget
for this exact dynamic history, selected after reference observation but before
candidate evidence. It is not transferred Ramp/NoteOff calibration, old0.0001
waveform applicability, native tolerance, calibrated uncertainty, inaudibility,
ULP/Apple/arm64/mixed-library bound or an all-candidate correctness guarantee.
The mathematical1e-4 normalized error-energy interpretation is explanatory;
the specified rounded square-root comparison controls acceptance.

Actual validation retained38 comparisons/all152 axis records. Ignoring the
step fails postL with E=0.8990030348930524; its other three checks match exactly.
Four isolated1.02 corruptions fail their own axis with errors near0.02 while
other three stay exact self matches. A concentrated last-right-sample error
PASSES at E=0.005000000371140732, and finite-prefix123 corruption PASSES.
Artificial1/512-sample splices and last512zeroing fail for these vectors; these
are waveform sensitivity observations, not physical latency/duration or tail
laws. Aggregate budgets can conceal local/concentrated or low-energy defects.
No per-sample/tail/silence/general right-invariance, A1 or modal-omission closure
follows. The complete actual sensitivity ledger is retained in the private R7
provenance; independent actual-method approval and owner adoption are separate.

## Comparison metric

Proposed as a general T1 device-audio criterion of ADR 0004. The finite
use of this criterion is separately bounded by the
[handoff plan](device-corpus-handoff-plan.md#review-outcome--2026-10-19); approval
of that finite package does not approve unlisted modes or scenarios. A candidate render
of a case passes when it meets every line that applies, measured on the case's frames after
any start-up ramp. **DCO-029, DCO-030, DCO-031 and DCO-032 have dedicated finite rows:**
only the specified row and validation for each applies. DCO-029 retains its Ramp
rule; DCO-030/031 use only the modal measurements and first256 post-impulse frames
specified below. DCO-032 uses only its dedicated post4096 waveform row. General
startup, timing, LFO, Ramp and other signal rows do not add checks to these three
MIDI cases. The older case scopes remain unchanged.

| Signal | Comparator | Tolerance |
| --- | --- | --- |
| Modal types, impulse input | Each mode with weight at least 10⁻³ of the strongest, measured in candidate and reference with the same demodulation estimator (appendix). A mode is graded only if the estimate from the reference render is within 10⁻⁴ of its REQ-005 pole frequency; closely spaced or heavily damped modes are not resolved | Frequency within 4 binary32 ulp bounds. The bound is 3·2⁻²⁵/θ² + 2⁻²³ relative, with θ = 2πf/fs. At 44.1 kHz the tolerance is 4.0 × 10⁻³ at 66 Hz and 2.6 × 10⁻⁴ at 262 Hz. Per-frame log radius ρ within 8·2⁻²⁵/\|ρ\| relative. Complex amplitude within 5 × 10⁻³ |
| Modal types, impulse input | Waveform, the 256 frames from the impulse | Rel RMS within 2 × 10⁻³ |
| Steady-state sine | Complex gain fitted over the last 8,192 frames | 0.01 dB and 0.5° |
| Noise | Third-octave band levels, 80 Hz to 16 kHz, from frame 8,192 | 0.01 dB |
| Pipe, Tube, filter, dry path | Waveform after the impulse or after frame 8,192 | Rel RMS within 10⁻⁴ |
| LFO pitch | Instantaneous fundamental, averaged over 200 frames | 0.2 Hz at 261.62 Hz |
| Timing | Start-up silence and ramps | Exact frames |
| DCO-029 only: Free Ramp Up, exact frozen input/protocol | Every frame4096–16383inclusive, each channel independently; no fitting, alignment or alternate windows | Relative waveform RMS ≤0.01; both channel energies positive and full-file samples finite |
| DCO-030 only: held note60, exact frozen input/protocol | Fixed32 mode points (16per channel) copied exactly from CORPUS-AUDIO-013-04; original modal estimator and first256 frames4096–4351 inclusive | Unchanged modal frequency/log-radius/complex-amplitude budgets and early waveform relative RMS≤0.002; full-file finite validation |
| DCO-031 only: held note72, exact frozen input/protocol | Fixed30 mode points (first15per channel), cutoff100Hz, from the retained calibration's fixed navigation list; first256 frames4096–4351 inclusive | Same unchanged modal budgets and early waveform relative RMS≤0.002; explicit post-observation finite engineering eligibility, not recovered pole eligibility |
| DCO-032 only: note60 On1537/Off3073, gate1, host34=+0, exact frozen input/protocol | `noteoff_decay_zero_waveform`: every frame4096–16383 inclusive, each channel independently; no fitting/alignment or alternate window | Relative waveform RMS≤0.01; positive scored reference/candidate energy in EACH channel, exact length/full-file finite; new finite engineering budget only |

For DCO-029, decode exactly16384stereo interleaved little-endian binary32 frames
and widen to binary64. For each channel compute
`sqrt(math.fsum((candidate-reference)^2)/math.fsum(reference^2))` on all
frames4096through16383inclusive. Subtraction/products, fsum, sqrt and inclusive
computed-binary64 comparison define rounding, with no acceptance epsilon. Both
reference and candidate must have positive energy per channel. Reject any
nonfinite sample anywhere or invalid length. No gain/phase/offset fitting,
channel mixing or time alignment is allowed. The [frozen engineering proposal](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-corpus-lfo-ramp-criterion/README.md)
contains the standalone evaluator and finite controls. Its [independent criterion
review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/corpus-lfo-ramp-criterion-review.json)
approves only this finite engineering method/budget; owner adoption and release
review are separate gates, not consequences of captured bytes alone.

This1%budget permits at most1e-4error energy/reference energy per channel. It is
an explicit finite engineering choice, not a recovered device tolerance,
inaudibility claim, Apple/arm64 error bound or worst-case mixed-libm guarantee.
The two [reviewed math-substitution captures](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/corpus-lfo-ramp-sensitivity-review.json)
have relative errors0.00635–0.00709; selected wrappers advance even exact results
toward ±infinity. Those observations and rejection controls do not establish a
portability envelope. Finite prefix differences before4096are outside this
metric; concentrated/onset/tail errors can fit its aggregate budget. DCO-029
does not grade startup, all phases, full cycles, absence of a right-channel
phase wrap, Sync, Spin, random shapes, stored mapping or actual Live delivery.

For DCO-030/031, decode exactly16384 stereo interleaved little-endian binary32
frames and widen to binary64. Reject bad length or any nonfinite sample anywhere;
reference and candidate must have positive post4096 energy independently on each
channel. Compare every frozen point on both channels and the early256-frame
waveform. Do not align, rescale, mix channels, recenter modes, remove failed fits
or substitute another window. An absent/unmeasurable/nonfinite mode or zero
amplitude denominator fails. Frames0–4095 have length/finiteness validation only:
no silence/floor, energy, phase, onset, event timing or startup accuracy is graded.
Finite corruption in that prefix can pass.

The unchanged modal procedure is the released v2 comparator's `modal` branch:
causal1455-tap scaled Hamming FIR at100Hz, global demodulation, group delay727,
fit frames5551–16383 inclusive (earliest contributing input4097), and amplitude
extrapolation to4096. The early waveform uses frames4096–4351 inclusive with
relative RMS≤0.002. For each listed mode, candidate and reference are measured
with exactly the same center and cutoff. Compare frequency with absolute bound
`reference_frequency*4*(3*2^-25/theta^2+2^-23)`,
`theta=2*pi*reference_frequency/44100`; per-frame log-radius absolute error
≤`8*2^-25`; complex amplitude ratio error≤0.005. These are unchanged finite
engineering budgets, not a new bound on native poles, original math-library
error or physical note accuracy. Expected mode values come from measuring the
frozen reference, not from the navigation centers or an inferred MIDI pitch law.

DCO-030 copies all32 points of released evaluation CORPUS-AUDIO-013-04. All
scored source samples are byte-identical after4096, so its existing measurement
eligibility transfers only on those samples; full files differ. This cannot by
itself reject an implementation ignoring this MIDI event.

DCO-031 is an **explicit post-observation engineering eligibility proposal**:
freeze the first15 navigation points per channel from the fixed16-point
calibration list, without refitting centers or changing any numeric budget.
This case-specific choice replaces the general modal row's recovered-pole
eligibility condition for this case only. Both mode16 observations are omitted
because their full/half estimates were window-sensitive; all32 original research
rows, including those two, remain retained. The omission was selected after
observation, not predeclared or an automated stability test. The retained
[method proposal](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-corpus-midi-modal-method/README.md)
and its proposed [independent criterion review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/corpus-midi-modal-method-review.json)
are separate gates before owner adoption. No p1 hypothesis, recovered actual
coefficient/pole, complete significant-gap, estimator uncertainty, general mode
eligibility, hidden-spectrum or newly resolved174-omission claim follows.
Omitting mode16 leaves that observation ungraded; it does not prove it absent.

Both cases retain only their exact vector/input/history and the fixed listed
measurements. There is no new render, candidate result or application grade in
this owner draft. A source route or a reference-self comparison is not such a grade.

For DCO-032 only, decode exactly16384 interleaved stereo little-endian binary32
frames and widen exactly to binary64. Reject invalid length or any nonfinite
sample anywhere; reference and candidate must each have positive scored energy
in EACH channel. The actual reference must have SHA-256
`a378ac6de6c04041a21aee501094be643fdb6615d3fc212ebbcc32afdf76d829`.
On ALL frames4096–16383 inclusive, independently for left and right, compute
`sqrt(math.fsum((candidate-reference)**2)/math.fsum(reference**2))`.
Binary64 subtraction/products, `math.fsum`, division and `math.sqrt`, then
inclusive computed-binary64 `E <= 0.01`, define rounding; no acceptance epsilon.
Both channel checks must pass. No fitting, alignment, rescaling, offset removal,
channel mixing, frame deletion, transient exclusion or alternate window occurs.
Frames0–4095 are validated only for length/finiteness; finite prefix corruption
can pass, and no prefix silence, floor, energy, onset or event timing is graded.

This is a NEW finite1% engineering budget for this one nonstationary B transient,
not transferred Ramp applicability/sensitivity, the older0.0001 waveform rule,
modal eligibility, a native tolerance, calibrated uncertainty, inaudibility,
Apple/arm64/ULP/mixed-libm bound or a guarantee for future correct candidates.
No B-specific sensitivity/repeatability calibration is claimed. The rounded
square-root comparison controls acceptance; the mathematical1e-4normalized
error-energy interpretation is explanatory only. The [criterion proposal](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-corpus-midi-noteoff-decay-zero-criterion-proposal/README.md)
has a separately [approved finite method review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/corpus-midi-noteoff-decay-zero-criterion-review.json).
That review does not adopt this owner or a release. Its three named wrong references have only ONE unique scored waveform; they do not supply
three independent contrasts or a universal wrong-output detector.

The aggregate budget can hide concentrated/onset/low-energy-tail defects.
Deliberately zeroing the entire last8192frames can pass this aggregate rule,
although B's retained later samples are nonzero. There is no tail cutoff,
per-sample/local-envelope/silence threshold, decay constant or output-flag check.
The full captured reference remains retained. No general MIDI/gate/decay law,
source/setter/registry closure, stored/UI conversion or Live delivery is adopted.
DCO-032 gains no repeatability, block/rate/reset/transport/clock/MXCSR/FTZ/DAZ,
seed/lifecycle or other invariance from older cases. Independent capture,
criterion, owner and later release review remain distinct gates; this private
proposal runs no original or candidate code and assigns no application grade.

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

The original DCO-001–028 renders are 16,384 frames, stereo binary32, interleaved, with block 512, from
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

DCO-029 uses the same generated I1 impulse at44100Hz and exact38host values of
DCO-020, except LfoType=3. Its new [frozen capture](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-corpus-lfo-ramp-up/README.md)
retains the complete script, input pin, stopped0/0/120transport, present-input
flag1, MXCSR0x1f80 and no reset/event history. Baseline Sine output exactly
matched the retained DCO-020 bytes before Ramp capture. The captured file is
`raw/ramp-up.f32`,131072bytes, SHA-256
`40b77412adfc4768bd18e76e5df330ecd536544c50553212ba3125a8de7982ec`.
Host decimals0.8and0.3 mean their binary32 values; no stored-value conversion is
implied. Sensitivity variants are supporting observations, not additional cases.
DCO-029 does not extend the earlier block-size, repeatability, rate/reset, clock,
FTZ/DAZ or MXCSR invariance observations to this new vector. Only the exact
declared call history has this finite expectation; no second nominal Ramp run
or original-application execution is claimed.

DCO-030/031 use the complete vector and exact event objects in the additive
[R5 case fixture](../../analysis/ableton-live-12.4.3/full-spec-v1/corpus-owner-r5/cases-additions.json).
All38 host binary32 values are explicit; the pair differs only at the event key,
60 versus72. Both use I1 at44100Hz,16384frames/block512 and the REQ-001 fixed
history. Their [reviewed capture](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-corpus-midi-pitch/README.md)
retains original scripts/raw/logs without replay. The two raw files are each
131072bytes: note60 SHA-256
`5866c6b9e4915336648da87bd92c38927cb3e532fe81ab38b5300664c7bb984f`,
note72 SHA-256
`f98b465f7186680830bc87c97f4a4096e1e53b2ad1b07aa5333ccccd6ea36ddc`.
The event interface is an externally declared test input, not a required internal
record representation or a recovered Live-side frame convention. No extra
adapter-minus-one correction is permitted. Full source/capture history remains
unchanged. The original four U cases and all29 earlier case rows remain exact.

DCO-032 uses the complete38-value HOST vector and exact event objects in the
[R6 case fixture](../../analysis/ableton-live-12.4.3/full-spec-v1/corpus-owner-r6/cases-additions.json).
It is the captured B history: MidiPitch12=1, MidiGate13=1, LFO17=0 and
host34=positive0, with note60/channel0/velocity100 On1537 and velocity64 Off3073.
The host/test coordinates are absolute: block1536/local1 and block3072/local1;
no extra adapter subtraction or claimed Live frame-base conversion. Use I1 at
44100Hz,16384frames/block512, fresh instance/rate then all38parameters in order,
stopped0/0/120, inputflag1, reference MXCSR0x1f80 and time0; no reset, warm-up,
second note, bend, sustain or additional update. Those reference environment
values do not mandate candidate internals or imply newly tested invariance.
The [reviewed capture](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-corpus-midi-noteoff-decay-zero/CAPTURE.md)
retains complete scripts/logs/raws; B is131072bytes with SHA-256
`a378ac6de6c04041a21aee501094be643fdb6615d3fc212ebbcc32afdf76d829`.
The observed B process flags21x(ret0,flag1)/11x(ret0,flag0) are not an expectation
or scheduling/silence/admission law. All31previous case rows and original fourU
cases are preserved; A1,174oldmodal omissions and both note72mode16 omissions
remain unaccepted/ungraded. No release evaluation ID is allocated by this draft.

DCO-033 uses the complete host fixture in the
[R7 case record](../../analysis/ableton-live-12.4.3/full-spec-v1/corpus-owner-r7/cases-additions.json).
It reuses every initial binary32 value/order of CORPUS-AUDIO-006-01, including
Membrane3/Quality3, MidiPitch0/MidiGate0/LFOoff, initialListeningXL
0.10000000149011612 and unchangedListeningXR0.8999999761581421. I1 is at4096;
the only later update is index15=0.75 after8,192 processed frames. Both process
segments contain16 blocks of512. The captured reference uses stopped0/0/120,
inputflag1 before every block, MXCSR0x1f80/time0, fresh instance and no events,
info, reset, warm-up, input restart, bend or other parameter change. Environment
facts characterize the reference, not candidate architecture/invariance.
Host/test boundary8192 is not Live scheduling or proved internal onset.

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
| DCO-029 | 001, 011 | P | Exact DCO-020 host/input/protocol, only LfoType=3 (Free Ramp Up); I1 at44100Hz,16384frames/block512 | Dedicated per-channel post4096waveform RMS ≤0.01 only; positive energies/full-file finite validation; finite engineering criterion, no Live/application grade | New `raw/ramp-up.f32` (`40b77412adfc4768bd18e76e5df330ecd536544c50553212ba3125a8de7982ec`) |
| DCO-030 | 001, 013 | P | Exact38-value R5 fixture, MidiPitch1/MidiGate0/LFOoff; one held note60 velocity100/channel0 at1537, I1 at44100Hz,16384frames/block512 | Dedicated fixed32-point modal/early-waveform criterion only; prefix finite-only; cannot alone reject ignored MIDI | Captured `raw/note60.f32` (`5866c6b9e4915336648da87bd92c38927cb3e532fe81ab38b5300664c7bb984f`) |
| DCO-031 | 001, 013 | P | Same complete vector/protocol as DCO-030, only event key72 | Dedicated fixed30-point modal/early-waveform criterion only; post-observation engineering eligibility; both mode16 observations ungraded | Captured `raw/note72.f32` (`f98b465f7186680830bc87c97f4a4096e1e53b2ad1b07aa5333ccccd6ea36ddc`) |
| DCO-032 | 001, 013 | P | Exact R6 HOST fixture: note60 On1537/Off3073, MidiPitch1/MidiGate1/LFOoff, host34=+0; I1 at44100Hz,16384frames/block512 | Dedicated `noteoff_decay_zero_waveform`, ALL post4096 per-channel relative RMS≤0.01; full-file finite/exact length, positive scored energies; prefix finite-only; new finite engineering budget | Captured B `raw/gate1-off.f32` (`a378ac6de6c04041a21aee501094be643fdb6615d3fc212ebbcc32afdf76d829`) |
| DCO-033 | 001, 012 | P | Exact initial006-01 host vector; SAME instance process8192/512, ListeningXL index15=0.75, process8192/512; I1 at4096/44100Hz, all other controls unchanged | Dedicated pickup_step_waveform: pre[4096,8192)/post[8192,16384), L/R separately, FOUR relative RMS errors<=0.01; exact reference/full finite/positive4R/Y; engineering budget only | Captured left-step `raw/left-step.f32` (`1336d90115bd24c058e556aa95e9140014d168dad7111dec64eb8edd1d977e73`) |

## Finite deterministic Free-LFO observation annex

The [five-member catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-corpus-r8-deterministic-free-lfo-v1/catalog.json)
contains Sine 0, Square 1, Triangle 2, Ramp Up 3 and Ramp Down 4. DCO-020 and
DCO-029 remain the existing Sine/Ramp Up cases, with no duplicate IDs or transfer
of their criteria. Sample & Hold 5 and Random Ramp 6 remain the separate
clock/seed-dependent U contexts of REQ-011; the five-member class does not mean
all seven shapes are deterministic.

DCO-034–036 use the same explicit 38 host binary32 values as DCO-020/029 except
LfoType at host index18 is respectively1,2,4. The exact bit vectors and input
joins are in the [three draft records](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-corpus-r8-deterministic-free-lfo-v1/new-cases.json).
Each fixture uses a fresh instance, rate argument44100, parameters in index
order, I1 stereo impulse at4096,16384 frames in512-frame blocks, input flag1,
stopped transport0/0/120, XDEV_TIME0/LIBM_ULP0 and MXCSR1f80. These are supplied
host/test coordinates and substitutions, not proved Live scheduling, stored
value conversion or actual sample-clock/FP-state observations.

| Case ID | Requirement | Kind | Setup | Observation / acceptance criterion | Reference identity |
| --- | --- | --- | --- | --- | --- |
| DCO-034 | 011 | U | Exact annex fixture, LfoType1 Square | X: retained finite stereo output; new waveform expectation and candidate/portable comparator NULL | `b82781c5d6ef5d23…`,131072B; approved partial Square |
| DCO-035 | 011 | U | Exact annex fixture, LfoType2 Triangle | X: retained finite stereo output; new waveform expectation and candidate/portable comparator NULL | `c1741a23aee40b79…`,131072B; approved continuation |
| DCO-036 | 011 | U | Exact annex fixture, LfoType4 Ramp Down | X: retained finite stereo output; new waveform expectation and candidate/portable comparator NULL | `20c4b33c88e6bce0…`,131072B; approved continuation |

The draft now has 36 rows: 29 existing cases with criteria, these three native
observation-only cases, and four existing U cases. The new rows carry X
observations with U acceptance criteria; they are not newly graded renders. Their pre-call native waveform priors remain NULL in the immutable
captures; no new expected waveform, tolerance, Hz/RMS budget, shape fitting or
portable comparator is selected here. No REQ-001 block/rate/reset/clock/FTZ/DAZ,
repeatability, state or lifecycle invariance extends to them. All old 33 rows,
finite objects, criteria and released73 evaluations remain unchanged.

Square's once-only capture exited0 and retained its full output before the
recorder's unsupported Rate-return0 assertion stopped that batch. Its false
completion phases, stale recorder child label and failed guard remain history;
its unused generator's stale tail-index assertion and author-reported assembly
history, without independent durable initial-generation proof, are preserved
in the [history qualifications](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-corpus-r8-deterministic-free-lfo-v1/history-qualification.json).
Only the two never-launched shapes were captured in the separately approved
continuation. Square was not retried. The continuation records Rate's literal
signed integer with unknown status/clock semantics, rather than requiring0 or
fitting1 as a success oracle.

The owner records use only Root's independently approved full-five summary,
with exact point/hash/output/provenance pointers. They do not re-review or
reopen actual audio, source, providers or original calls. A1, public binding,
ARM/Apple, errors/state/lifecycle, all174+2 modal omissions and parked96-byte
setup remain unchanged. This finite catalog is not a required-outcome
denominator, accepted waveform method, application grade or complete profile.

## Finite native integer-host observation annex — revision 9

The [complete catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-corpus-r9-native-integers-finite-v1/catalog.json) retains 69 logical index/value
aliases across seven native kind3 domains: host0=0..6,10=0..24,17=0..1,
18=0..6,21=0..21,27=0..1,33=0..3. Their whole 38-value vectors deduplicate
into63 distinct inputs:57 new DCO-037–093, five existing shape references and
one unnumbered qualified historical shape5 metadata reference. These units
are navigation/input coverage, not a required-outcome or application denominator.

The [57 new draft records](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-corpus-r9-native-integers-finite-v1/new-cases.json) carry X observations with
U acceptance criteria. Each full word vector, exact input/output identity,
receipt and sole-approved-summary pointer is retained; no waveform was predicted
before capture. Native output identities describe retained reference evidence,
not portable candidate waveform criteria. Portable expected/comparator/grade
remain NULL. The draft now has93 IDs:36 unchanged old rows plus57 new native
observation-only cases. The immutable release's73 evaluations are unchanged.

Each vector uses the common supplied-host/test history: fresh recorded instance,
rate argument44100, all38 host values in index order, I1 stereo impulse at4096,
16384 frames in512-frame blocks, input flag1, stopped transport0/0/120,
MXCSR1f80 and time0/libm perturbation0. No warm-up, MIDI event, reset, later
parameter change or new state crossproduct occurs. Domain membership and these
reference-environment inputs are not observed Live delivery, candidate internals,
entry FP-state continuity, Apple-libm/ARM bounds or source-version binding.
Inactive branches remain in the catalog; equal outputs do not establish a
parameter no-effect law, and random shapes do not become deterministic classes.

The five inherited references are shape0 DCO-020, shape1 DCO-034, shape2 DCO-035,
shape3 DCO-029 and shape4 DCO-036. They receive no duplicate IDs, new receipts,
PIDs or metrics, and keep their prior criteria unchanged. Shape5 is an
UNNUMBERED qualified historical input/output-metadata reference, not DCO-021
(the unchanged startup-dry case), a new expectation or a newly replayed capture.
Its old script omits explicit MXCSR/transport commands; the same recorded-default
model remains a qualified premise, not proof of current FP/source/entry binding.
The old Sample & Hold and clock-dependent U contexts remain unchanged.

**Common qualification for EVERY new case:** the original frozen checker FAIL
and its no-op `data_as_code` negative remain immutable history. The additive
postcapture DATA checker PASS is NOT pre-call-bound. All CAPTURE code including
the parent launcher was pre-call-bound; this does not mean all later analysis
code was. The [qualification record](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-corpus-r9-native-integers-finite-v1/qualification.json) pins the
retained failure/stderr, additive source and proof using the
[sole actual approval](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/corpus-native-integer-domains-v1-review.json).
The correction changed data-only validation after capture; it did not retry or
repair original calls, inputs, audio, capture code or the frozen failed route.
Recorder/parent JSON requested fsync; raw audio/stdout/stderr only close/hash,
with no directory/crash-durability proof. Observed rate return1 has unknown
status/sample-clock semantics. Declared imports and counted use remain distinct.

This owner annex maps approved observations only; it does not re-review actual
source/raw/numeric evidence. It adds no metric, fit, calibration, tolerance,
new stable/random class, physical accuracy, public binding, general native law,
ARM parity, candidate grade, release or closure. REQ-011 Sync/seed and general
shape unknowns, A1/A2, timing/state/lifecycle, modal174+2 omissions, parked96
setup and the old Square guard/phases/unused-generator qualifications remain
unchanged. All other12 requirement bodies, old36 rows, old R3–R8 objects and
all earlier finite criteria are preserved byte-for-byte.

## Complete finite host-domain observation annex — revision 10

The [whole catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-corpus-r10-complete-finite-hosts-v1/catalog264.json) retains277 typed aliases over14
finite axes, deduplicated to264 complete38-word vectors under ONE fixed I1
history. The201 new observations receive DCO-094–294 in retained vector order:
96 host7 values across−48..48 except0,100 host8 values across−50..50 except0,
and one changed member at each binary host12,13,19,22,37. The seven earlier
native integer axes remain in the full catalog, not newly replayed. This is
one-index coverage, not a parameter/state crossproduct or an arbitrary float
sweep. A declared finite stored-conversion axis establishes input materiality,
not proof of current stored emission, binding or an application predicate.

All63 prior vectors join by FULL vector hash to the old R9 catalog. They keep
five existing shape IDs plus57 R9 IDs and ONE UNNUMBERED qualified shape5
metadata reference. No old reference gets a new ID, original call, PID,
receipt or metric; shape5 does not become DCO-021 or a new expectation. New
7/8 axes change catalog positions, so old/new positional indices are not joins.
The [complete joins](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-corpus-r10-complete-finite-hosts-v1/joins277.json) bind every full vector and277aliases
to the exact approved summary and old owner records without duplicate cases.

Only [Root's sole actual/source approval](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/corpus-complete-finite-host-domains-v1-review.json),
SHA256 `976edbd7da21c765ab85ed76ff298b58410d2d8e0ff4cdce5ca07eb806cc89be`,
supplies new finite native identities and unsigned word summaries. This owner
work repeats no actual source/raw/audio/numeric proof. All201 are finite and
nonzero in BOTH channels; none has identical channel words and there are five
distinct fresh hashes. These descriptive identities/equalities are not a
pitch/effect/clamp/LFO/MIDI-gate/seed/inactivity/mechanism or deterministic
waveform law. Their pre-call waveform priors, new waveform expectations,
portable expected/comparator and grades remain NULL. Native output identities
are evidence locators, not a portable candidate comparison criterion.

The supplied context is the complete38-word DCO-020/029/I1 vector, except ONE
selected word. Exact words/tokens/f32/reconstructed-f64 projections and input
identity are in the catalog. I1 is the stereo impulse at4096,rate44100,
16384frames/block512/last512,inputflag1,no warm-up or events,time0/libm0.
Literal script order is MXCSR1f80 and stopped transport0/0/120 BEFORE
create/rate/ordered38parameters, matching the existing approved model.
Eligibility prose groups conceptual roles and does not override frozen
script order or prove Live's actual call order/FP-state/receiver/public ABI.
No new model, event type, timing segmentation, provider, build, patch, tool,
emulation or state crossproduct is introduced.

**New201 checker scope:** THIS capture/data/checker code INCLUDING its parent
launcher was fully pre-call-bound, and its retained data check PASSED. Do not
label these201 new captures as the earlier frozen-checker failure. **Old63
scope:** each inherited reference retains its OWN prior original checker
FAIL/no-op `data_as_code`, additive postcapture DATA PASS NOT pre-call-bound,
old source/default/FP/transport and shape5 qualifications exactly. New good
checking does not repair old proof or replace older metadata with fresh
receipts. The catalog carries both qualification scopes separately.

This new collector requested fsync for JSON/JSONL, regularstdout/stderr FDs
and retainedaudio readFD afterchild; that does not repair old close/hash/no-FD-
fsync limits or prove directory/crash/powerloss durability. Source/hash/samePID
records do not attest OSexec/build/continuous providers or target-entry FP/ABI.
Post-child detection cannot retract earlier within-child calls, and group/
direct-child cleanup does not prove every escaped-descendant/parent-loss path.
Import127 declarations(99Linux21trap7data) stay separate from counted code
use.73 selected direct exports and32 CalcA per child plus0 logged initializers
are not all-native-call counts. Rate's literal signed integer has unknown
public/status/sample-clock meaning. No fresh runtime law follows.

This adds201 navigation IDs:294 total, with all93 prior IDs and36 old table
rows unchanged. Only bounded REQ-002 wording is appended. All12 other whole
requirements, old002 prefix, R3–R9 objects/catalogs, R9 count-wording erratum,
all old criteria/U/timing/state/history, released27groups/73evaluations,
modal174+2 omissions, parked96 setup and oldSquare guard/phases/prepare
qualifications remain exact. No old budget transfers here. There is no new
metric, f0/fit/window/tolerance/calibration, physical accuracy, public/ARM
law, candidate grade, release or whole-product closure; new application
predicate proofs remain false. Required unsupported behavior remains U.

## Finite supplied held-On MIDI observation annex — revision 11

The [complete catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-corpus-r11-held-note-midi-finite-v1/catalog270.json) retains272 typed aliases and270
WHOLE histories. The268 new cases DCO-295–562 comprise126 note keys excluding
60/72,127 On velocities excluding100 and15 On channel nibbles excluding0.
The axes vary independently without a crossproduct. There is NOOff event;
only the On status nibble varies, not a matching On/Off pair. Three baseline
aliases share ONE old DCO-030/key60 history; key72 separately references
DCO-031. Both are inherited metadata only, with no new original call, ID,
PID, receipt or metric and NO old modal-budget/expectation transfer.

Only [Root's sole actual/source approval](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/corpus-held-note-midi-axes-v1-review.json),
SHA256 `8d35db17713bd840ac2322b050a030e36dc83f850ec05d177ce9cd41ff5d954d`,
supplies these finite observations. The owner maps that summary without
actual/source/raw/audio/numeric re-review. [All272 joins](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-corpus-r11-held-note-midi-finite-v1/joins272.json)
use complete history plus ORIGINAL decimal/parsed-binary64 identity, not
R10's no-event parameter hash, old catalog position or rounded owner f32 repr.
Every exact script/event/packed16/input/output/provenance pointer is retained.

This is a DIFFERENT held-note vector:38 ordered binary32 words have hash
`613d0f49d678f947d847f2a4d56767881c63f370f07f2a8fdd2a172d4875b8a1`;
original parameter tokens parse to binary64 bytes with hash
`1c0495901fdb45b2e3d8c47034fe9fa80fdabd375d2e945ec3a8e31d4fdf7863`.
MidiPitch12=1/MidiGate13=0/LFO17=0. The no-event R10 host class uses a
different vector and supplies no substitute for this context. Literal script
order is MXCSR1f80/stopped transport0,0,120 BEFOREcreate/rate44100/38ordered
parameters, ONE On at1537, inputflag1/I1 impulse at4096,16384frames/block512,
then destroy. Baseline status90/key60/velocity100 changes at ONLY the chosen
On byte. No warm-up, Off, reset, later note/update or timing segmentation.
Absolute host/test frame1537 is retained, without a new Live event-base or
adapter-minus-one conversion. The exact original I1 source path and byte
identity remain fixed; no new receiver/object model, patch, tool or provider.

All268 fresh captures are finite and nonzero in BOTH channels; none has
identical channel words and there are127 distinct fresh hashes. These are
descriptive native identities, not proof of a pitch curve, key clamp/alias,
channel filter, velocity response, mechanism, physical accuracy, general
MIDI dispatch or deterministic waveform law. Velocity0 remains an unknown
dispatch observation in this exact initially supplied history; there is no
new held-voice note-off equivalence claim. Fresh waveform priors and new
waveform expectations, portable expected/comparator/grade remain NULL.
Native artifact hashes do not become portable waveform criteria. No f0,
fit, window, new metric, tolerance, calibration or old modal budget is added.

The explicit minimal recorded environment keeps XDEV_TIME0 while
XDEV_LIBM_ULP is UNSET, matching that held-note treatment rather than
R10's explicit LIBM0 context. This does not assert equality with the old
whole ambient environment or target-entry FP/source/default/OSexec state.
All new capture/data/checker/parent code was pre-call-bound for THIS batch;
old proof gaps and earlier checker FAIL/additive postcapture DATA/default/
source/fsync qualifications remain with their own references, not repaired
or indiscriminately attached to these new captures. Requests to fsync new
JSON/JSONL/log/audio FDs do not prove directory/crash/powerloss durability.
Endpoint hashes/samePID records do not attest build, OSexec, continuous
loaded providers or native entry FP/ABI. Post-child checks cannot retract
prior within-child calls; group/direct-child cleanup leaves unexhausted
parent-loss/escaped-descendant paths. Import declarations remain distinct
from counted code use.73 selected exports/32 CalcA per child and0 logged
initializers leave nested/all-native calls unknown; Rate's signed integer
has unknown public/status/sample-clock meaning.

Only bounded REQ-013 wording is appended. All12 other whole requirements,
including the ENTIRE R10 REQ-002 append, old013 prefix,294 prior IDs/36 old
rows, allR3–R10 objects/catalogs, original NULLs/criteria/U/timing/state/history,
released27groups/73evaluations, modal174+2 omissions, parked96 setup and
oldSquare phases/guard/prepare qualifications remain exact. The resulting
562 navigation IDs are not passes or an application-outcome denominator.
New application-predicate proofs remain false; no public/ARM law, release,
candidate grade or whole-product closure follows. Required U remains open.

## Finite supplied DCO032 two-event MIDI observation annex — revision 12

The [complete catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-corpus-r12-dco032-midi-finite-v1/catalog397.json) retains400 aliases and397
WHOLE histories at one fixed parameter vector. DCO-563–958 are396 fresh
observations:127 On keys excluding60;127 On velocities excluding100;
15 matching On/Off channel nibbles excluding0;127 Off velocities excluding64.
Each axis varies independently, without a crossproduct. The On-key axis
changes ONLY the On key: Off remains key60, so most pairs deliberately use
different keys. The channel axis changes BOTH status nibbles together.
The four baseline aliases (Onkey60/Onvelocity100/channel0/Offvelocity64)
share ONE inherited DCO-032 INPUT approval. No new ID, original call, PID,
receipt, output, metric, expectation, criterion or modal budget is assigned
to that inherited member. [All400 joins](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-corpus-r12-dco032-midi-finite-v1/joins400.json) use complete
histories and original decimal/parsed-binary64 identity, not parameter-only
collapse, old catalog position or rounded neutral-owner values.

Only [Root's sole actual/source approval](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/corpus-dco032-midi-axes-v1-review.json),
SHA256 `c073663a31b3a20aadd01ac60b200b0ac8c3a55f1abc09ce791c2ea0ffd440f2`,
supplies these new finite observations. The owner maps its approved summary
without actual/source/raw/audio/numeric re-review. Every exact script,
two packed16-byte events, input/output, PID/receipt and provenance pointer
is retained for fresh histories. The baseline source script is735bytes,
SHA256 `2366eeac0a1f1e41a6b835fda19703e452d46002f14d45c48a0a2e6641b82fc3`;
its old sole-endpoint approval is used ONLY for the input reference here.
Missing members refer to the reviewed bounded input cut, not global absence.

The38 ordered binary32 words have hash
`351eb39550097c4d432e53db67460f1e50b35533e34841a90438ab2e31256060`;
original decimal tokens parse to binary64 bytes with hash
`1855a118565d354015e7ba29929bba2152a57f5a3507885ee1050e37b7ec8a6a`.
MidiPitch12=1/MidiGate13=1/LFO17=0/host34=positive zero. This differs from
R11's held-On vector613d0f49…875b8a1 with MidiGate13=0/host34=1/NOOff;
that class is not a substitute or inherited baseline for this one. Literal
script order is MXCSR1f80/stopped transport0,0,120 BEFORE create/rate44100/
38 ordered parameters, On1537/status90/key60/velocity100 and Off3073/status80/
key60/velocity64, inputflag1/I1 impulse4096, render16384frames/block512,
then destroy. Only the selected event byte(s) change. No warm-up, reset,
later note, host update or timing segmentation. Host/test coordinates do
not prove a Live frame origin, current event ingress or internal admission.
The original I1 source path and bytes remain fixed; no new receiver model,
build, patch, tool or provider was introduced.

All396 new captures are finite and nonzero in BOTH channels; none has
identical channel words, and129 distinct fresh hashes are descriptive only.
These facts do not prove general release semantics, velocity0 note-off
equivalence, productive event admission, key matching, channel filtering,
pitch/velocity response, deterministic waveform law or physical accuracy.
The supplied Onvelocity0 and all domain edges remain in the catalog without
an extra dispatch claim. All new waveform priors/expectations, portable
expected/comparator/grade stay NULL. Artifact hashes are native observation
references, not portable candidate waveform criteria. No f0, fit, metric,
window, tolerance, calibration or modal-budget transfer is added.

Minimal explicit environment retains XDEV_TIME0 and XDEV_LIBM_ULP UNSET,
not explicit LIBM0 or equality with the old whole ambient environment.
Source/default/entryFP/ABI/OSexec and loaded-provider continuity gaps remain.
All new capture/data/parent/checker/initial-materializer source was frozen
before calls for THIS batch; the materializer is a historical initial stage,
not a final regenerator. This does not repair old source/checker FAIL/additive
postcapture DATA/default/fsync or earlier parent-binding limitations, which
retain their own scopes. Requests to fsync new JSON/JSONL/log/audio FDs do
not prove directory/crash/powerloss durability. Per-child endpoint hashes
and samePID records do not attest OSexec/continuous runtime/provider/FP
state. Post-child protocol/import checks cannot retract earlier within-child
calls; group/direct-child cleanup does not exhaust parent-loss/escaped
process paths. Imports declared are distinct from code imports counted as
used.73 selected direct exports/32 CalcA per child and0 logged initializers
leave nested/all-native calls unknown. Rate's signed integer remains opaque,
without public/status/sample-clock meaning.

Only bounded REQ-013 wording is appended. All12 other whole requirements,
including ENTIRE R10 REQ-002, old013 R11 prefix,562 prior IDs/36 old rows,
allR3–R11 objects/catalogs, old NULL criteria/general U/timing/state/history,
released27groups/73evaluations, modal174+2 omissions, parked96 setup and
oldSquare phases/guard/prepare qualifications remain exact, with full reversal.
The resulting958 navigation IDs are not passes or an application-outcome
denominator. New application-predicate proofs remain false; no public/ARM
law, release, grade or whole-product closure follows. Required U stays open.

## Finite supplied DCO032 residual MIDI observation annex — revision 13

The [complete catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-corpus-r13-dco032-residual-midi-finite-v1/catalog158.json) retains 160 aliases and 158 WHOLE histories at
one fixed 38-word parameter vector. DCO-959–1115 are 157 fresh observations:
Off key 0–127 except 60, On channel 0–15 except 0 and Off channel 0–15 except 0.
Each axis varies independently without a crossproduct. Off-key variation
keeps On key 60 fixed; On-channel variation keeps Off status 80 fixed;
Off-channel variation keeps On status 90 fixed. They do not change paired
keys or channel nibbles together. The three baseline aliases share ONE
inherited DCO-032 INPUT approval, without replay, fresh PID/receipt/metrics,
new ID, output expectation, criterion or modal-budget transfer. The [160 joins](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-corpus-r13-dco032-residual-midi-finite-v1/joins160.json)
use complete event/process/FP/environment history, not parameter-only dedup.
All new histories are distinct from the R12 four-axis catalog.

Only [Root's sole actual/source approval](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/corpus-dco032-residual-midi-axes-v1-review.json),
SHA-256 `a728173fc59cf176177bd3882f1da8027718b838be5dd5be9f0dbd39077d363f`,
supplies these finite observations. This owner maps that approved summary
without actual/source/raw/audio/numeric re-review. Each fresh record retains
exact script, two packed16-byte events, input/output identity, PID/receipt,
protocol and provenance pointers. The old 735-byte baseline script remains
`2366eeac0a1f1e41a6b835fda19703e452d46002f14d45c48a0a2e6641b82fc3`;
it is an inherited input reference only. Bounded input intersections are
not global absence or proof of all MIDI histories.

The original 38 decimal tokens and binary32 vector remain
`351eb39550097c4d432e53db67460f1e50b35533e34841a90438ab2e31256060`;
parsed binary64 token bytes remain
`1855a118565d354015e7ba29929bba2152a57f5a3507885ee1050e37b7ec8a6a`.
MidiPitch12=1/MidiGate13=1/LFO17=0/host34=positive zero. Literal script order
is MXCSR1f80/stopped transport0/0/120 BEFORE create/rate44100/38 ordered
parameters, On1537/status 90/key 60/velocity100 and Off3073/status 80/key 60/
velocity64, inputflag1/I1 impulse4096, render16384frames/block512/destroy.
Only the named event byte changes. No warmup/reset/extra event/host update,
new timing segmentation, construction, tool, patch, build or provider.
The original I1 path and bytes remain fixed; synthetic coordinates do not
prove Live frame origin, event admission or a current public receiver.

All 157 approved outputs are finite/nonzero in both channels; none has
identical channel words, and two fresh output hashes are descriptive only.
These facts establish no key matching, channel filtering, voice release,
productive event admission, deterministic waveform or general MIDI law.
All new waveform priors/expectations, portable expected/comparator/grades
stay NULL; artifact hashes are native observation references, not portable
candidate waveform criteria. No f0, metric, fit, window, tolerance,
calibration, physical/ARM law or old modal-budget transfer is added.

Minimal environment retains XDEV_TIME0 and XDEV_LIBM_ULP UNSET, not explicit
LIBM0 or proof of the old whole ambient environment. Old source/default/
entryFP/ABI/OSexec and loaded-provider continuity gaps remain. All new
capture/data/checker/parent/initial-assembler source was pre-call-bound for
THIS batch; the assembler is historical materialization, not a final
regenerator. This does not repair earlier source/checker FAIL/additive
postcapture DATA/default/fsync or parent-binding history. Regular raw/log/
JSON/JSONL fsync requests do not prove directory/crash durability. Per-child
endpoints and samePID parent records do not attest OSexec, continuous
runtime/providers or native FP. Post-child protocol/import checks cannot
undo earlier within-child calls; group/direct-child cleanup does not exhaust
parent-loss/escaped-process paths. Declarations differ from counted use.
73 selected direct exports/32 CalcA per child and zero logged initializers
leave nested/all-native calls unknown; Rate's signed integer is opaque.
Resource guards were not triggered: before each call the recorded packet
was at most 27,861,012 bytes and free space at least 258,478,080 bytes.
Planning estimates are not filesystem reservations or general resource laws.

Only bounded REQ-013 wording is appended. All 12 other whole requirements,
including ENTIRE R10 REQ-002, old013 R12 prefix,958 prior IDs / 36 old rows,
all R3–R12 objects/catalogs, old NULL criteria/general U/timing/state/history,
released 27 groups / 73 evaluations, modal174+2 omissions, parked96 setup and old
Square phases/guard/prepare qualifications remain exact, with full reversal.
The resulting 1115 navigation IDs are not passes or an application-outcome
denominator. New application-predicate proofs remain false; no release,
grade, public/ARM law or whole-product closure follows. Required U stays open.

## Open questions

Proposed for [questions](../questions.md) (not edited by this draft):

- **A1, position range.** This is the open Q of REQ-BUNDLED-DEVICE-PARAMETERS-015. Both readings now
  have X consequences: host 0..1 reaches strike points 0.5–0.723, and −1..1 reaches 0.277–0.723.
- **Live-side protocol.** The event frame base (Corpus subtracts one from non-zero frames), the
  transport and input-flag values, the block sizes, and when the reset sequence runs.
- **MIDI side-chain path (REQ-013).** It needs both a bundle trace (event to note) and a Live
  trace (side-chain routing). The three finite extracted histories do not resolve the general
  route, all notes/gates or event timing; their engineering comparisons are case-specific.
- **Pipe and Tube (REQ-009).** Restate the static waveguide description as behavior, or keep these
  render-only.
- **libm.** Apple's libm against glibc for the functions the device calls. The older metric assumes
  that they differ by at most one ulp. DCO-029 instead makes an explicit finite
  engineering acceptance choice; its two coherent substitution observations do
  not prove that assumption or bound mixed per-call differences. DCO-032's
  separate1% engineering budget transfers none of that sensitivity evidence.

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
| 001/013 finite DCO-030/031 | [Capture review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/corpus-midi-pitch-review.json); note60 scored-byte identity with released013-04; all32 note72 research rows in the [proposed method packet](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-corpus-midi-modal-method/README.md). The R2 preflight approved readiness only, not criteria/eligibility; proposed method/owner reviews remain separate. No actual Live result or new original call |
| 013 finite DCO-032 | [Endpoint capture review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/corpus-midi-noteoff-decay-zero-capture-review.json) supports bounded X observations only; [criterion proposal](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-corpus-midi-noteoff-decay-zero-criterion-proposal/README.md) proposes its own1% waveform budget. Independent method/owner/release gates are separate. No new original/candidate execution or UI/source-binding closure |
| 001/012 finite DCO-033 | [Private R7 record](../../analysis/ableton-live-12.4.3/full-spec-v1/corpus-owner-r7/README.md) binds separately reviewed pickup capture, effective method/addendum and complete actual38comparison ledger. Source environment/protocol only; no smoothing/A1/Live/candidate or complete-profile claim. Actual-method/owner/adoption gates remain separate. |
| arm64 equivalence | Static: same constants and structure (the C1 corpus readings of the reports); differences limited to fused multiply-adds (count above) and Apple's libm builds. Not executed |

## Revision and handoff

| Revision | Date | Change |
| --- | --- | --- |
| 1 | 2026-10-18 | First draft from the T1.2 feasibility gate (packet t12-device-dsp-v1). 13 requirements: 9 X with S origins (001, 003–008, 010, 012), 1 S with an X clause, an S-cond clause and a U part (002), 3 X with U parts (009, 011, 013). 28 cases: 24 graded by X renders, 4 not graded (DCO-025 to 028; DCO-028 graded only under A1) |
| 2 | 2026-10-19 | Pilot-staging precision corrections against retained corpus_runs.json and raw/startup_dry.f32: FilterMidFreq 1000 Hz corresponds to host binary32 0.5089499354362488; startup frames 0–99 have the numerical floor, not exact zero. No general metric approval or case expectation beyond those clarifications. 13 requirements and 28 cases unchanged. |
| 3 | 2026-10-19 | Independent review distinguishes DCO-023's before-parameters rate sequence from the earlier after-parameters scenario; the latter remains excluded from device-corpus-v1 because its changed output is not retained in the payload. DCO-021 states gain separately from output for its 0.5 input. The reviewed finite metric does not approve the broader draft formulas or unlisted scenarios. |
| 4 | 2026-10-19 | Proposes one finite Free Ramp Up host-input audio case DCO-029 with its own explicit 1%per-channel waveform-RMS budget. All13requirement IDs/28earlier case rows, A1 and174modal omissions remain unchanged. Independent criterion/owner review and successor release are separate gates; no complete-profile or actual Live/candidate claim. |
| 5 | 2026-10-20 | Proposes two exact held-note host-input modal cases DCO-030/031, preserving all13IDs/29oldcase rows;31cases:27finite proposed expectations/fourU. REQ001/013 narrowed only to these histories. Note72 eligibility is an explicit post-observation first15perchannel engineering choice, both mode16 records retained/ungraded. Criterion, owner adoption and release remain separate; no candidate/application grade or complete profile. |
| 6 | 2026-10-20 | Private proposed DCO-032 only: exact note60 On1537/Off3073/gate1/host34=+0 B reference and independently reviewable1%post4096per-channel waveform budget. All13IDs/31oldrows/001–012bodies preserved;32cases28finite/fourU if approved. No new gate/decay/flag/UI law, invariance, grade or completion. |
| 7 | 2026-10-20 | Private proposed DCO-033 only: same-instance ListeningXL host step during productive ringing, exact four pre/post L/R1%waveform engineering checks.13IDs/32old rows and every old clause/budget retained;33cases29finite/fourU if approved. No smoothing duration, general right-invariance, A1, modal-omission or application grade. |
| 8 | 2026-10-21 | Add three observation-only draft rows DCO-034–036 for fixed Free Square/Triangle/Ramp Down host fixtures and a full five-shape catalog, inheriting Sine/Ramp Up without duplicate IDs. Correct only REQ-011's obsolete unrendered wording and add bounded X-observation/U-criterion scope; new waveform priors/expectations/comparators remain NULL. Preserve prior33rows/12otherwholeclauses/allfinitecriteria/73releasedevaluations, historical Square guard/unused-generator qualifications and all public/ARM/A1/modal omissions. No new tolerance, grade or release. |

| 9 | 2026-10-21 | Add57 supplied-native-host observation-only cases DCO-037–093 under bounded REQ-002 qualification, complete69alias/63vector catalog with five existing case references and one unnumbered qualified shape5 metadata reference. Preserve all36 prior IDs/36 old rows/criteria/73release evaluations and old U; original checker FAIL plus additive postcapture DATA PASS retained, capture parent prebound does not imply all analysis prebound. No new waveform comparator, tolerance, public/ARM/general law, grade or release. |
| 10 | 2026-10-21 | Add201 finite supplied-host observations DCO-094–294 from14axes/277aliases264vectors;63 prior vectors keep62oldcase references plusONEunnumberedshape5 metadata reference, joinedfullhash/no replay. AppendONLY boundedREQ002 qualification; preserve12otherwholeREQ/old002prefix/93priorIDs36rows/R3–R9objects/criteriaU/modal176parked96/releases27groups73eval exact/fullreverse. New201 THISfullypreboundcheckerPASS; old63ownFAIL/additiveDATA/default/source qualifications and fsync limits remain. No new portablecriterion/grade/publicARM/general law/calibration. |
| 11 | 2026-10-21 | Add268 finite held-On observations DCO-295–562/full272aliases270WHOLEhistories, with oldDCO030/031 references/no replay/modalbudgettransfer. AppendONLY boundedREQ013; preserve12otherwholeREQ inclentireR10REQ002/old013prefix/294priorIDs36rows/allR3–R10objects/criteriaU/releases27groups73eval/modal176parked96/history exact/fullreverse. Originaldecimal/f64 heldcontext and LIBM_ULPUNSET retained; NULLnewpriors/waveformexpectations/portablecriteria/grades/newappFalse, no generalMIDI/pitch/publicARM/calibration law. |
| 12 | 2026-10-21 | Add396 finite DCO032 two-event observations DCO-563–958/full400aliases397WHOLEhistories, fourbaselinealiasesONE inheritedINPUTreference/no replay/newmetrics/criterion transfer. AppendONLY boundedREQ013; preserve12otherwhole inclENTIRER10REQ002/old013R11prefix/562priorIDs36rows/allR3–R11objects/criteriaU/releases27groups73eval/modal176parked96/Squarehistory exact/fullreverse. Originaldecimal/f64/gate1/host34+0/LIBMUNSET/OnkeyONLYfixedOff60 distinctR11heldcontext; NULLnewpriors/portablecriteria/grades/newappFalse/no velocity0release/publicARM/calibration law. |
| 13 | 2026-10-21 | Add157 finite DCO032 residual observations DCO-959–1115/full 160 aliases / 158 WHOLE histories, three baseline aliases / ONE inherited INPUT reference/no replay/newmetrics/criterion transfer. Append ONLY boundedREQ013; preserve 12 other whole requirements incl ENTIRE R10 REQ002/old013 R12 prefix/958 prior IDs / 36 rows/all R3–R12 objects/criteriaU/releases27groups73eval/modal176parked96/Squarehistory exact/fullreverse. Original decimal/f64/gate1/host34+0/LIBM_UNSET/single Offkey or Onchannel or Offchannel unchanged; NULL new priors/portable criteria/grades/newappFalse, no unmatched-key/release/publicARM/calibration law. |
| 16 | 2026-10-21 | Add890 finite seven-resonator supplied-host observations DCO-1370–2259/full896aliases891histories/ONE INPUTref sixaliases; appendONLY boundedREQ007/009 plusannex. Preserve11otherwhole inclENTIREREQ003/R10REQ002/R14REQ013/old007R15+009prefixes/1369priorIDs36rows/allR3–R15objects/criteriaU/releases27g73e/history/fullreverse. Representative INPUT formulas not nativequantizer/within-cell/publicARM/calibration laws; newpriors/portablecriteria/gradesNULL/appFalse. |
| 17 | 2026-10-21 | Add189 native-HOST position observations DCO-2260–2448/full190histories192aliases/ONE U047 INPUTref3aliases. Annex+revision only/all13 whole requirements,2259 prior IDs/36oldcases40literalrows/R3–R16 objects/criteriaU/releases27g73e/fullreverse exact. HOST−1..1/64P64labels32–95 not 128/fullphysical/within-cell/publicUI law; A1U/newpriorsportablecriteriaGradeNULL/appFalse. |
| 18 | 2026-10-21 | Add3586 finite controller-neighborhood observations DCO-2449–6034/full3587histories3591aliases/1197INPUTtransitions/ONE INPUTref fivealiases. Annex+revision ONLY/all13wholeREQ/2448oldIDs36cases40rows/R3–R17objects/criteria/history/releases27g73e exact/fullreverse. Native U/B/I/P neighbor labels not quantizer/within-cell/output/physical/publicARM law; positionA1U/root0700-child0775/inputsource-vs-copy/oneauthority64548pairs qualified; allnewpriorsportablecriteriaGradeNULL/appFalse. |
| 19 | 2026-10-21 | Add13 finite supplied-model declared-protocol observations DCO-6035–6047/full13histories17aliases; fourRERUNaliases notrerun/no inheritedbaselineoutputs. Annex+revision ONLY/all13wholeREQ/6034oldIDs36cases40rows/R3–R18objects/criteria/history/releases27g73e exact/fullreverse. Original38words/threeINPUTs/literalrateorder/no injectedFPtransport; no protocol/nativequantizer/publicARMlaw/newcriteria; allpriorsportablecriteriaGradeNULL/appFalse. |
| 20 | 2026-10-23 | Add10 finite exact declared-variant observations DCO-6048–6057; full19catalog9rate INPUT-only. Annex+revision only/all13wholeREQ/6047priorIDs36objects40rows/R3–R19objects/criteriaU/releases27g73e/fullreverse. Frozen owned-checker FAIL explicitly retained; independent strict actual audit only/no repair/guardrelaxation/seed-FTZ-reset-publicARM law or portable criterion. |

**Historical R1–R3 release statements, retained as of those freezes.**

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


**Historical R4 author-freeze proposal, retained verbatim below.**

Revision4 preserves the revision3 finite release and its immutable payloads.
The [R4 successor record](../../analysis/ableton-live-12.4.3/full-spec-v1/corpus-owner-r4/README.md)
retains exact R3before/R4proposal snapshots and text deltas. A proposed v2
release maps canonical DCO-029 to CORPUS-AUDIO-020-02, appending one evaluation
to existing group020; this does not rename DCO-025–028 or create29release groups.
No successor is published merely by this draft.


## Historical R5 owner proposal (2026-10-20)

Device-corpus-v2 is now a separately released immutable provider; its69 finite
evaluations and every v1/v2 payload remain unchanged. This R5 draft proposes two
canonical cases only; no successor release IDs or evaluation grouping are assigned
here. DCO-030/031 do not rename DCO-025–028, and no new requirement ID is created.
The [R5 proposal record](../../analysis/ableton-live-12.4.3/full-spec-v1/corpus-owner-r5/README.md)
retains exact R4before/R5proposal text, literal deltas and complete finite inputs.
AS-OF AUTHOR DRAFT: the method packet/criterion review and this owner review are
pending. No canonical page is adopted or release published by this proposal.


## Proposed R6 owner successor (2026-10-20)

The separately adopted R5 and released device-corpus-v3 remain immutable history:
31canonical cases and71finite release evaluations, with no candidate grade.
This R6 private draft adds only DCO-032; it creates no requirement ID and assigns
no release evaluation/group ID. The [private R6 record](../../analysis/ableton-live-12.4.3/full-spec-v1/corpus-owner-r6/README.md)
retains exact R5before bytes, literal deltas, full finite inputs and separate
criterion-review binding. AS-OF AUTHOR FREEZE: the finite method has separate
independent approval; this owner review/adoption remains pending. No canonical/
shared page, comparator, release or candidate is changed by this proposal.
Current disposition is routed through the shared specification index after review.


## Proposed R7 owner successor (2026-10-20)

The separately adopted R6 and released device-corpus-v4 remain immutable:13IDs,
32canonical cases/72finite release evaluations. This private R7 proposal adds
ONLY DCO-033 under REQ-001/012; no requirement or release group/evaluation ID is
allocated. The [private R7 packet](../../analysis/ableton-live-12.4.3/full-spec-v1/corpus-owner-r7/README.md)
reuses the exact58,472B R6 before provider, preserves all32old case rows/013body,
and records exact insertions and source/method/provenance bindings. The effective
method design and actual finite validation have separate independent approval;
independent owner approval/adoption remain pending. No
canonical/shared page, release, comparator, staging or candidate is changed.
All174old modal omissions and both note72mode16 observations remain ungraded.


## Analyst evidence follow-up — 2026-10-20

The [reviewed x86 source exports](../research/corpus-dsp-static.md#constructor-body-guard-stop-and-retained-frontier--2026-10-20)
improve finite source navigation. They add no parameter/model-state mapping,
modal expectation, arm64 equivalence or accepted audio criterion. R7's clauses,
33cases, grades and released v5 expectations remain unchanged; subsequent
preparation is governed by the sole analyst plan.

## Finite supplied DCO032 matching-key observation annex — revision 14

The [complete catalog](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-corpus-r14-dco032-matching-key-finite-v1/catalog128.json) retains 128 aliases and 128 whole histories.
DCO-1116–1242 number 127 fresh observations in ascending key order, excluding
key60. This class changes both existing On and Off keys together, to the same
key 0–127. It is distinct from the earlier On-key-only and Off-key-only axes,
which hold the other key60 fixed. All other bytes, times, parameters and
process requests stay fixed; there is no crossproduct, extra event or new
construction. ONE inherited DCO-032 INPUT reference at key60 receives no new
ID, call, PID, receipt, metric, output expectation, criterion or modal budget.
[All 128 joins](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-corpus-r14-dco032-matching-key-finite-v1/joins128.json) use complete event/process/FP/environment history and original
decimal/parsed-binary64 identity, never parameter-vector-only deduplication.

Only [Root's sole actual/source approval](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/corpus-dco032-matching-keys-v1-review.json),
SHA256 `974b8d4defd727f3761136c051cd73bddb90ab25ed419e20781f9bbe780a0d62`,
supplies these observations. This annex maps its approved summary without
actual/source/raw/audio/numeric re-review. Fresh records retain their exact
script, two packed16-byte events, input/output identity, PID/receipt/protocol
and provenance pointers. The old 735-byte baseline script remains
`2366eeac0a1f1e41a6b835fda19703e452d46002f14d45c48a0a2e6641b82fc3`,
an inherited INPUT reference only. Bounded prior catalog intersections are
not proof that every other MIDI history is absent or exhausted.

The original 38 decimal tokens and binary32 vector remain
`351eb39550097c4d432e53db67460f1e50b35533e34841a90438ab2e31256060`;
parsed binary64 token bytes remain
`1855a118565d354015e7ba29929bba2152a57f5a3507885ee1050e37b7ec8a6a`.
MidiPitch12=1/MidiGate13=1/LFO17=0/host34=positivezero. Literal script order
is MXCSR1f80/stopped transport0/0/120 BEFORE create/rate44100/38 ordered
parameters, On1537/status90/key/velocity100 and Off3073/status80/samekey/
velocity64, inputflag1/I1 impulse4096, render16384frames/block512/destroy.
There is no warmup, reset, additional event, host update or segmentation.
The original I1 source path and bytes stay fixed. Supplied host coordinates
do not prove a Live frame origin, current receiver or actual event admission.
Minimal environment keeps XDEV_TIME0 and XDEV_LIBM_ULP UNSET, not explicit
LIBM0 or proof of the old whole ambient environment. Ordinary bookkeeping
uses existing Python3.12, explicitly different from the historical summary's
Python3.13 identity; original xdev, bundle/slice/provider model is unchanged.
This distinction does not repair old ambient/source/default/FP/ABI gaps.

All 127 approved fresh captures are finite/nonzero in both channels; none
has identical channel words and all 127 fresh hashes are distinct. These are
descriptive local artifact facts, not a general matching-key, pitch, release,
productive admission, velocity0, physical or deterministic waveform law.
All new waveform priors and waveform expectations remain NULL;
portable expected/comparator/grade remain NULL and
new application-predicate proofs remain false. Native artifact hashes are
observation references, not portable candidate waveform criteria. There is
no new metric, f0, window, fitting, tolerance, calibration or old modal-budget
transfer. Public Live/ARM/Apple behavior remains outside this finite scope.

All new capture/data/parent/checker/initial-assembler code was pre-call-bound
for THIS batch. The 154 common-initial identities match each 127 after
endpoint (19,558 pairs), NOT separate per-child-before attestation. Recorded
endpoint identities/parent PIDs do not prove OSexec, continuous loaded
providers or native entry FP state. JSON receipts are explicitly fsynced;
regular raw/log files are closed with no explicit raw-FD fsync. Neither
provides directory/crash/powerloss durability or repairs older source,
checker FAIL, additive DATA, parent-binding, default or fsync limitations.
Post-child checks cannot retract earlier within-child calls, and group/
direct-child cleanup does not exhaust parent-loss/escaped-descendant paths.
Declarations differ from counted code use.73 selected direct exports and
32 CalcA per child, with zero logged initializer entries separately counted,
leave nested/all-native work unknown; Rate's signed integer remains opaque.
Pre/post-child storage guards and lifecycle estimates are not quotas,
reservations, portable resource laws or permission to clean old evidence.

Only bounded REQ-013 wording is appended. All 12 other whole requirements,
including ENTIRE R10 REQ-002, old013 R13 prefix,1115 old IDs/36 old rows,
all earlier navigation/objects/catalogs and the old Acceptance prefix remain
exact, with full R13 reversal. Old criteria, general U, timing/state/history,
released 27 groups/73 evaluations, modal174+2 omissions, parked96 setup and
Square failed-guard/unused-prepare/phase qualifications remain unchanged.
The resulting 1242 navigation IDs are not passes or an application-outcome
denominator. No new candidate grade, release, site or whole-product closure
follows. Required U remains open.


## Finite supplied Decay controller-cell observation annex — revision 15

This annex admits only Root's independently approved supplied-host observations:
[sole actual/source review](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/corpus-decay-controller-cells-v1-review.json),
9,452,808 bytes / SHA256 `1fe8a02e7fd3b88816c35a9b7d05e77755b50a3190ea35feae2a819c97494553`.
The [127 new cases](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-corpus-r15-decay-controller-cells-finite-v1/new-cases127.json),
[complete128-cell catalog](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-corpus-r15-decay-controller-cells-finite-v1/catalog128.json) and
[approved input/provenance joins](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-corpus-r15-decay-controller-cells-finite-v1/joins128.json)
retain DCO-1243–1369 in cell order0–126; cell127 has no new case ID.
The [reversible owner delta](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-corpus-r15-decay-controller-cells-finite-v1/owner-delta.json)
and [preservation metadata](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-corpus-r15-decay-controller-cells-finite-v1/preservation.json)
define this narrow revision. Earlier rows and releases are unchanged.

These are 128 explicitly named input representatives, not a claim that all
continuous host values in each cell behave alike. REQ-003's formula and floor
rule are INPUT enumeration context only, not a newly measured quantizer law,
output oracle or portable acceptance criterion. Each new case retains its
exact original decimal token, binary64/binary32 words, complete38-word vector,
script identity and approved output/receipt references without numeric re-review.
Only host index1 varies from the qualified CFH-V002/CNI-V002/DCO020 no-event
I1 fixture. The inherited cell127 reference supplies no new PID, receipt,
metrics, output criterion or modal budget. Its original checker FAIL/additive
post-capture DATA, default/source/durability qualifications keep their scopes;
this revision does not repair them or fabricate a fresh baseline observation.

The literal supplied script sets MXCSR1f80 and transport0,0,120 BEFORE create,
then rate44100/all38 ordered original decimal arguments, inputflag1/original
I1 input, process16384 at512, destroy. There are no MIDI events, warmup,
rate/reset/state updates or parameter-history crossproducts. TIME0 and explicit
LIBM_ULP0 are retained, unlike the distinct DCO032 LIBM_UNSET context. New
bookkeeping uses system Python3.12 rather than historical3.13; unchanged native
model/tool identities do not imply a new ABI or public receiver proof.

Root's approved summary reports finite/nonzero outputs in both channels,
unequal channel words and127 distinct fresh hashes. These are local descriptive
facts, not decay-time/shape, f0, symmetry, inactivity or calibration laws, and
no old metric, tolerance, window or modal omission budget is transferred.
All127 waveform priors/expectations, portable expected/comparator/grade remain
NULL; new_application_predicate_proof is false. A1/current receiver/provider/
nativeFP/OSexec/ARM/public behavior and general required scopes remain U.

The approved record retains two source endpoint pairs and2,286 per-child
18-pair comparisons, not continuous provider/nativeFP/ABI or OSexec proof.
The same-PID parent bridge is ordinary recording; outer tool PID is absent
and rendered progress is truncated, with full owned records retained. New
raw/log/JSON FDfsync requests are not directory/crash/power-loss durability
or repair of historical gaps. Resource/remaining-output guards and unreserved
128MiB lifecycle+128MiB headroom estimates are not hard quotas or permission
to clean evidence; post-child guards cannot retract within-child calls.

Only bounded REQ-007 wording is appended. All12 other whole requirements,
including ENTIRE R10 REQ-002 and ENTIRE R14 REQ-013, old007 prefix,1242 prior
navigation IDs/36old rows, old Acceptance/annex/navigation and all prior objects
remain exact through Root R14 embedded metadata, with full reversal. Existing
27groups/73released evaluations, modal174+2 omissions, parked96 setup, Square
failed-guard/unused-prepare/phase history, U criteria and state/history remain.
The resulting1369 navigation IDs are not passes or an outcome denominator.
No new release, application grade, site or whole-product closure follows;
required unsupported behavior stays U / OPEN.


## Finite supplied seven-resonator representative observation annex — revision 16

Only [Root's sole actual/source approval](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/corpus-remaining-resonator-controller-cells-v1-review.json),
75,205,145 bytes / SHA256 `23ce8da8c5a9596d1511a64eb676bf89029fe4ba4015c7408bbe896a72891181`,
supplies these finite observations. The owner maps its approved summary only,
without actual/source/raw/audio/numeric or old-proposal/provider proof replay.
The [890 new cases](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-corpus-r16-seven-resonator-cells-finite-v1/new-cases890.json), [complete catalog](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-corpus-r16-seven-resonator-cells-finite-v1/catalog891.json)
and [896 alias joins](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-corpus-r16-seven-resonator-cells-finite-v1/joins896.json) retain exact original decimal,
binary64/binary32 words, whole script/history and approved output/receipt
references. DCO-1370–2259 are890 fresh IDs, not application passes.

Seven independent axes each contribute128 explicitly named INPUT representatives:
B: FreqDamping2, Inharmonics3 and AmpFreq11; U: Ratio4, TubeOpening35 and
Bleed36; inverted I: Radius5. This totals896 aliases/891 whole histories.
The three B axes preserve negative cell63 versus zero cell64; Radius uses
its inverted representative mapping, including half-value cell63. Ratio0.5
is not a named n/127 representative, so all128 Ratio histories are fresh;
same-cell membership cannot fabricate exact baseline inheritance. Six other
baseline aliases collapse to ONE CFH-V002/CNI-V002/DCO020 INPUT reference.
It supplies no new case ID, PID, receipt, metric, output criterion or modal
budget and is not replayed. The seven axes do not form a crossproduct.
REQ-003 formulas select INPUT representatives only, not newly established
native quantizer, within-cell equivalence or maximum-domain laws. Positions
14–16 remain excluded under unresolved A1; no position admission is added.

REQ-007's append maps FreqDamping, Inharmonics, AmpFreq and Bleed;
REQ-009's append maps Ratio, Radius and TubeOpening as supplied context,
without asserting a waveguide/shape admission or stronger physical formula.
All38 original decimal arguments/f64 words are fixed except the named host.
The no-event I1 context is distinct from DCO032 and held-On MIDI contexts.
Literal MXCSR1f80/stopped transport0,0,120 precede create/rate44100/all38
ordered setters, inputflag1/original I1 impulse4096, process16384/block512,
then destroy. No MIDI, warmup, reset, rate/update or segmented process.
TIME0 and EXPLICIT LIBM_ULP0 remain, unlike the DCO032 UNSET context.
No new receiver/model, native patch, tool/build/provider or FP treatment.

The approved summary reports890 finite outputs nonzero in BOTH channels,
zero stereo-bit-equal captures and509 distinct fresh hashes, descriptive only.
No f0, decay metric, shape/effect, symmetry, inactivity, physical accuracy,
fit, window, tolerance or calibration is inferred; no old modal budget transfers.
All fresh waveform priors and new waveform expectations, portable expected/
comparator/grade remain NULL; application-predicate proof false. Hashes reference
native observations, not portable candidate waveform acceptance criteria.
General A1/A2/current receiver/provider/nativeFP/OSexec/public/ARM scopes stay U.

Two source endpoint pairs and16,020 per-child eighteen-pair comparisons
retain their endpoint scope, not continuous provider/loaded interpreter/FP,
ABI or OSexec attestation. Python3.12 bookkeeping differs from historical3.13.
Same-PID parent recording is not OSexec proof; outer tool PID is absent and
rendered progress truncated, with full owned records retained. New regular
raw/log/JSON FDfsync requests do not prove directory/crash/powerloss durability
or repair earlier default/source/checker/FDfsync limitations. Inherited INPUT
keeps its own original checker FAIL/additive postcapture DATA/default/source
qualification; this new prebound checker PASS does not rewrite that history.
All new capture/parent/analysis/checker/initial-assembler sources were bound
before these calls; the initial assembler is a historical materializer.
512MiB lifecycle plus128MiB headroom remains unreserved; remaining-output,
post-child soft-overshoot and escaped-child/concurrent-writer limitations
remain. Counted code-import use differs from binding declarations;56 used
Linux names are not provider-absence proof.64,970 selected direct exports/
28,480 CalcA/zero logged initializers leave nested/all-native calls unknown.

Only bounded REQ-007 and REQ-009 wording plus this annex/revision changes.
Eleven other whole bodies, including ENTIRE REQ-003 INPUT formula, ENTIRE
R10 REQ-002, ENTIRE R14 REQ-013, old007 R15 and old009 prefixes,1369 prior
navigation IDs/36 old case rows, all R3–R15 objects/catalogs and old Acceptance
remain exact through the pinned Root R15 embedded mapping/preservation,
with full reversal. No absent prior objects are reconstructed or freshly
fully reaudited. All earlier criteria/U/state/history,27 release groups/
73 evaluations, modal174+2 omissions, parked96 setup and Square failed-guard/
prepare/phase history remain unchanged. Resulting2259 navigation IDs are not
passes or an outcome denominator; no release, grade, site or closure follows.

## Finite supplied native-HOST position observation annex — revision 17

This annex maps only the [sole-approved native-HOST position observations](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/corpus-native-host-position-cells-v1-review.json),
16,598,737 bytes, SHA256 `466601c8acdc7e27ac25d9be6261a544e67d031a24be0e5050173c9012fd5fed`.
It adds DCO-2260–2448: 189 native observation-only cases under the
REQ-008 position context. The [complete catalog](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-corpus-r17-native-host-position-cells-finite-v1/catalog.json),
[new case records](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-corpus-r17-native-host-position-cells-finite-v1/new-cases.json) and
[alias joins](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-corpus-r17-native-host-position-cells-finite-v1/joins.json)
retain all 190 whole histories and 192 aliases, exact original 38 decimal tokens,
binary32/binary64 words, script hashes, source-summary/receipt pointers and
observed native-output hashes. These hashes identify approved retained outputs;
they are not newly fitted or portable waveform criteria. All new waveform priors,
native waveform expectations, portable expected/comparator and grades remain NULL;
new application-predicate proof is false. This is not a new release.

The supplied domain is native HOST −1..1 only, independently for ExcitationX (index 14),
ListeningXL (index 15) and ListeningXR (index 16). P64 INPUT labels 32–95 enumerate 64 representatives per axis,
not 128, the entire native-float/physical domain or a newly proved quantizer.
The endpoint representatives are −1/+1; interior representatives follow the pinned
INPUT selection, retaining each original baseline token in its own cell.
There is no crossproduct and no within-cell equality, symmetry, productive-effect,
physical scale or public UI-emission law. A1 remains U: native HOST values are not
proved equivalent to stored/UI values or actual Live delivery. The R16 position exclusions
remain historical and scoped; its earlier 890-observation annex is not rewritten.

U047 is ONE historical INPUT-only reference shared by three aliases; it receives
no new case ID, replay, PID, receipt, output metric, approved waveform or criterion.
Its qualified U064/CFH-V002/CNI/DCO020 input lineage and old source/default/Square/
checkerFAIL/no-op/additive post-capture DATA/FP/provider/OS-exec/old-FD-fsync limits
keep their previous scopes. A matching input does not repair historical execution
attribution or grant the old baseline a fresh approved observation.

Each fresh history changes only one position host word; the shared baseline
leaves all words fixed. The exact 38-setter, no-event I1
fixture, rate 44100/render 16384/block 512/no warmup, input flag 1/TIME0/explicit LIBM0,
MXCSR and transport before create and original decimal/binary64 history remain
those in the approved summary. Python 3.12 bookkeeping does not establish an old
interpreter/source execution identity or a new native ABI. No event, timing,
reset, receiver, model, provider or floating-point treatment is added.

The sole actual reviewer reports all 189 fresh outputs finite/nonzero in both
channels, zero stereo-word-equal outputs and 189 hashes; 56 counted Linux names
are descriptive, not position/quantizer/activation/provider-absence laws.
One retained INPUT-authority pair and 3,402 actual before/after custody
pairs (18 per child) are distinct from continuous dependency, loaded-provider, FP, interpreter,
ABI or OS-exec proof. JSON/regular-FD fsync requests are not directory/crash or
power-loss durability. Resource estimates, remaining-output guards, after-wait
first-fault/queued-call/cleanup limits and every original partial/failure/source
qualification remain scoped. No original/native/source/raw/numeric/provider or
release-fixture proof is re-reviewed by this owner annex.

All 13 requirement bodies remain byte-exact, including the entire R10 REQ002,
R14 REQ013 and R16 REQ007/009 additions. All 2,259 prior navigation IDs, 36 old case
objects/all 40 literal rows, old Acceptance/annex/navigation and R3–R16 objects
are preserved through Root R16's embedded mapping/preservation, without absent
objects being reconstructed or freshly re-audited. Full reversal restores R16.
Existing criteria/U/state/history, 27 release groups/73 evaluations, modal176
omissions, parked96 setup and Square failed-guard/prepare/phase history remain
unchanged. Resulting 2,448 navigation IDs are not passes or an outcome denominator.
Required unsupported behavior remains U and whole-Live coverage OPEN; no grade,
site credit, public/ARM compatibility or calibration law follows.

## Finite supplied controller-neighborhood observations — revision 18

**Analyst draft; finite extracted observations, portable acceptance U.**
The [complete R18 mapping](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-corpus-r18-controller-boundaries-finite-v1/mapping.json)
adds ONLY DCO-2449–6034 for3,586 fresh supplied native-host observations,
with3,587 whole histories/3,591aliases/ONE qualified INPUT baseline shared by
five aliases. All13 whole requirement bodies remain exact. REQ-003 is a
navigation context for these supplied values, not a new endorsement of its
native arithmetic, boundary, within-cell or output claims. No existing parent
case criterion is transferred or automatically validated by this annex.

Root's [sole actual/source approval](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/corpus-controller-boundary-neighborhood-v1-review.json),
110,700,142bytes/SHA256 `beeea75a42f1df6d793353ca633d92fddfa19d163257a802821fdbc0edca6ec5`,
is the only observation authority. Each new case joins its exact whole input,
approved point/output references and this common qualification, with frozen
fresh priors/native-waveform expectations/portable expected/comparator/grade
NULL and new application proof false. The owner author and new owner peer do
not repeat actual/source/raw/numeric/native/provider or old owner proposal/
catalog/fixture proof. Prior R17's sole owner review supplies embedded mapping
and preservation only, without absent oldobjects being reconstructed.

The INPUT inventory is1,197 INTERNAL rational transition neighborhoods across
11 declared U/B/I/P axes: Decay1, FreqDamping2, Inharmonics3, Ratio4, Radius5,
AmpFreq11, ExcitationX14, ListeningXL15, ListeningXR16, TubeOpening35 and Bleed36.
Each neighborhood retains its nearest binary32 input and immediate predecessor
and successor, with original decimal/binary64 provenance and full38-word
history. U/B/I uses declared internal upper-cell labels1–126; P retains63
internal boundaries/64 labels32–95 at native HOST−1..1. These labels and
neighbor choices are INPUT arithmetic only, not recovered native quantizer
boundaries, maximal native domains, within-cell equality or physical laws.
The stated inverted-half discontinuity and bipolar-zero signed minsubnormal
neighbors stay present; no normalization, sign collapse or oracle fitting occurs.
Position A1/stored-to-HOST/UI emission remains U. R16's earlier exclusion of
position representatives and R17's HOST-only64-cell qualification remain
historical scopes, not retroactively changed128-cell or stored-route proof.

Every fresh history changes only ONE supplied host word. No parameter, event,
physical-mode or activation crossproduct is added; dormant/inactive settings
are retained without productive-effect or general ignored-control conclusions.
One qualified baseline `CORPUS-CONTROLLER-BOUNDARY-U0568` has five aliases and
NO new ID, replay, PID, receipt, metric, output expectation or criterion.
Its qualified U064/U047/Decay-cell127 INPUT references keep their own old
source/default/checkerFAIL/no-op/additivepostcaptureDATA/FP/provider/OSexec/
oldFDfsync/Square limits; equal INPUT does not repair old execution attribution
or transfer an old accepted waveform, calibration or modal budget.

The exact no-event I1 model is unchanged: original38decimal/binary64 values
except one selected host, MXCSR1f80 and stopped transport0/0/120 BEFOREcreate,
rate44100/all38setters/inputflag1/input impulse4096/render16384/block512/noWarm/
reset/update, TIME0 and explicit LIBM0. This is the DCO020/029 no-event context,
not DCO032 or the held-On MIDI fixture. The script passes the original retained
input SOURCE path; an owned copy is separately pinned, not substituted as an
asserted native read path. Matching source/copy endpoint identities are not
loaded-provider, interpreter/build/source-version/default/nativeFP/ABI or
OSexec proof. Python3.12 bookkeeping does not prove historical3.13 equivalence.
No constructor, tool/build/patch/provider/emulation or new FP treatment is added.

The sole actual reviewer reports all3,586 outputs finite and nonzero in both
channels, zero stereo-word-equal outputs,818 fresh hashes and56 counted Linux
code names. These are descriptive copied facts, not boundary, noise, symmetry,
activation/effect, deterministic-waveform or provider-absence laws. Retained
zero/subnormal/signed inputs and exact output references acquire no new f0,
fit, estimator, metric/window/tolerance, output-law or physical calibration.
No public/ARM compatibility or native quantizer/within-cell law follows.
261,778selectedexports/114,752CalcA/0logged initializers leave nested/all-native
counts unknown; Rate's signed integer projection remains opaque.

All current capture/parent/analysis/checker/initial-authoring source was
pre-call-bound as recorded; no future owner wording changes those original
inputs/predictions. One authority endpoint pair and64,548 actual per-child18
before/after pairs match, rather than common-initial-only custody. SamePID
parent-guard VALUES are retained, without continuous dependency/actual-read/
provider/FP/OSexec attestation. The packet ROOT directory was0700;3,589 child
directories were0775 behind that private root. Do NOT describe all child
directories as0700. File fsync requests on successful raw/log/JSON paths do
not imply directory/crash/power-loss durability or old-capture repair; outer
recorder stdout/stderr have no explicit FDfsync request. Unreserved2GiB
lifecycle+128MiBheadroom/fullremaining-output and metadata guards are estimates,
not hard quotas or external-writer/escaped-child/within-child/post-soft bounds.
First-fault/partial-retention/no-retry and selected-group cleanup limits remain.

Only this annex and revision metadata are added. All13 whole requirements,
2,448 prior IDs/36oldcase objects/40literal rows/all R3–R17 referenced objects/
old Acceptance/annex/navigation/criteria/U/tolerances/state/history remain
byteexact, including ENTIRE R10REQ002/R14REQ013/R16REQ007009 and R17position
qualifications.27releasegroups/73evaluations/modal176omissions/parked96setup/
Square failed-guard/prepare/phase history remain unchanged and unreleased
scope does not expand. Release/object preservation facts are inherited reviewed
metadata only, without old proposals/providers/fixtures being reopened.
Full reversal restores R17. Resulting6,034 navigation IDs are not passes or
application-outcome denominator units. Required unsupported behavior stays U
and whole-Live coverage OPEN; no grade, site, release or portable criterion.


## Revision 19 finite declared-protocol observations — 2026-10-21

This annex adds only DCO-6035–6047: thirteen once-only supplied-model render
observations in the approved thirteen-history/seventeen-alias catalog. Four
RERUN source aliases refer to the same four base histories; none is rerun or
assigned a second case. There is no inherited baseline output. The complete
catalog, original inputs, exact outputs and receipt references are in the
[owner mapping](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-corpus-r19-declared-protocol-finite-v1/mapping.json).
The sole actual approval is the
[Root review](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/corpus-declared-rate-block-protocol-v1-review.json),
1,204,374 bytes/SHA256
`263f6ddbc19508b29baf62891baf5d3c4342ccfa6c2d7dd6094848a8db1df567`.
Only that approved summary supplies these owner observations; no actual,
source, raw audio, numeric estimator, formula or old fixture is re-reviewed.

The four base histories are defaults44, defaults48, noise44 and LFO Sine.
The remaining nine preserve the exact source-declared block64/256/333/2048
default44 variants; default48 via44, default44 via48 and default48 with the
second rate call AFTER parameters; noise44/block128 and LFO Sine/block100.
All thirteen preserve their original38 decimal tokens and binary64/binary32
projections, including the retained host28 word, not a regenerated formula.
Literal create/pre-rate/38 setters/post-rate/inputflag1/original input path/
process16384/block/destroy order defines each history. No MXCSR or transport
verb, MIDI event, warmup, reset, clock/FTZ treatment, Numpy input regeneration,
constructor, tool/build/patch/provider or model change is introduced.

The three immutable inputs are the original impulse44, impulse48 and noise44
files. Original source paths remain in scripts; separately frozen owned copies
are additional custody only. Explicit C/TIME0/LIBM0 is the supplied current
model environment, not proof of the historical wrapper's merged os.environ,
source-to-executed-build, default, native sample clock, FP register/ABI or
loaded-provider equivalence. The source-locator qualification changes ONLY
two INPUT source pointers; its frozen original authority remains unchanged.
The pre-freeze synthetic binding-to-kind fixture correction changed no selected
input or original call and stays in the capture's authoring history.

The sole reviewer reports all13 outputs finite and nonzero in BOTH channels,
zero stereo-word-equal outputs, six fresh hashes and66 counted Linux code
names. These are descriptive local facts, not new block/rate invariance,
noise/LFO/quantizer/within-cell/physical/public/ARM laws or metrics. All new
waveform priors, native waveform expectations, portable expected values,
comparators and grades remain NULL; application proof is false. Existing
finite metrics/tolerances are neither transferred nor replaced, and no output
fit, calibration, new f0/window/metric or portable criterion is selected.

1,430 selected exports/894 CalcA/zero logged initializers leave nested/all-native
counts unknown. Rate's signed integer projection remains opaque. All new
capture/parent/assembler/checker/finalizer source and inputs were pre-call-bound.
260 actual per-child20 before/after custody pairs plus two authority endpoint
pairs match; these are not common-initial-only pairs, continuous actual-read,
OSexec, FP-state or provider proof. Successful raw/log/JSON file-fsync requests
do not establish directory/crash durability; outer stdout/stderr have no
explicit FDfsync request. Unreserved256MiB lifecycle+128MiB headroom and full
remaining-output/log/metadata/final guards are not quotas or guarantees against
concurrent writers, escaped children or within-child overshoot. First-fault,
partial-retention, no-retry and cleanup limitations remain.

Only this annex and revision metadata are added. All13 whole requirements,
6,034 prior navigation IDs,36 old case objects/40 literal rows, R3–R18 objects,
old Acceptance/annex/navigation/criteria/U/tolerances/state/history are exact.
27 release groups/73 evaluations, modal176 omissions, parked96 setup and Square
failed-guard/unused-prepare/phase history remain unchanged. Full reversal restores
R18. The resulting6,047 navigation IDs are not passes or a product denominator;
unsupported required behavior stays U and whole-Live coverage OPEN. No grade,
site, release, general protocol law or portable criterion is admitted.

## R20 finite remaining declared-variant observations — 2026-10-23

DCO-6048–6057 add ten native observation-only histories under REQ-001 from the
[sole approved summary](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/corpus-declared-remaining-variants10-v1-review.json)
(1,452,887B; SHA256 `87c1145856a7a2beb79f689d605261938bd8b49383dd168c4dd441f65c23cab3`).
The [owner mapping](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-corpus-r20-remaining-declared-variants-finite-v1/mapping.json)
retains every exact input, source group, receipt and approved observation pointer.
The full nineteen-declaration catalog keeps nine rate histories as INPUT references
only: no old PID, output, metric, oracle or criterion is transferred or replayed.

- DCO-6048: `defaults_44_ftz_daz`.
- DCO-6049: `noise_44_ftz_daz`.
- DCO-6050: `defaults_44_seed1760000000`.
- DCO-6051: `lfo_sine_seed1760000000`.
- DCO-6052: `lfo_sah_seed1760000000`.
- DCO-6053: `defaults_44_warmup_reset`.
- DCO-6054: `wg_tube_44_warmup_reset`.
- DCO-6055: `wg_tube_44_reset_only`.
- DCO-6056: `defaults_44_midi_params`.
- DCO-6057: `decay_0.5_same_step`.

All38 original decimal tokens and binary64/binary32 words, source paths and
literal command order remain explicit. Two histories append1,024 zero-input
warmup frames, reset and rewrite ResonanceType before opening the original input
and rendering16,384 frames; both warmup output prefixes are nonzero. Reset-only
has no added warmup. The five MIDI-labelled post-writes are ordered parameter
commands with NO MIDI events, and the Decay post-write is literal0.503, not a
recovered same-cell/output-equivalence law. Initial words are not silently merged
with later writes. Two exact scripts request MXCSR9fc0; three supply TIME1760000000
and the others TIME0. These are supplied histories, not FTZ/seed/reset/transport,
parameter-emission, quantizer, effect or public-law experiments.

All ten pass the independently reviewed strict ret0/flag0or1 protocol and full
both-channel finite checks. Eight fresh hashes, two stereo-word-equal captures
and57 counted Linux CODE names are descriptive only, not effect/symmetry or
invariance laws. Native waveform priors/expectations, portable expected values,
comparators and grades remain NULL; new application predicate proof is false.
Existing criteria, windows, metrics and tolerances are neither transferred nor
replaced. No fit, calibration, f0, physical, public or ARM criterion is admitted.

The frozen owned checker remains FAIL: its generic identity helper incorrectly
requires bytes>0 for legitimate empty stderr. CDRV10-RV-Q01 retains that defect;
a separate complete independent DATA audit supports these ten observations.
No original owned-checker PASS, repaired source, native retry or relaxed guard is
claimed. The unchanged8128B driver nine-verb grammar join is source-only admission, not
compiled-source certification, vendor long/void ABI, return meaning or actual
FP-register/provider/OSexec proof. Minimal C/LIBM-unset, absolute BIN and import
logging are explicit current context, distinct from historical unknown ambient
wrapper defaults. All earlier source/build/receiver/A1/U qualifications persist.

745 selected exports/324 CalcA/zero logged initializers leave nested/all-native
counts unknown. Rate integers stay opaque. 400 actual per-child40 endpoint pairs
plus three REPORT pairs match; endpoint equality is not continuous provider,
FP-state or actual-read attestation. Raw/log/JSON fsync requests do not establish
directory/crash durability; outer redirects have no explicit FDfsync. Complete
256MiB lifecycle+128MiB headroom floors and remaining-output/future-log/metadata/
review-owner guards are unreserved, not quotas or guarantees against concurrent
writers, escaped children or within-child overshoot. First-fault/no-retry and
cleanup limits remain. No design13 or revision15 policy transfers to this strict
Corpus capture; its frozen protocol remains unchanged.

Only this annex and revision metadata change. All13 whole requirements,6,047
prior navigation IDs,36 old case objects/40 literal rows, R3–R19 objects, old
Acceptance/annex/navigation/criteria/U/tolerances/state/history remain exact.
27 release groups/73 evaluations, modal176 omissions, parked96 setup and Square
failed-guard/unused-prepare/phase history are unchanged. Prior R19 leaf0775 behind
0700 ancestors retains its historical qualification. Full reversal restores R19.
The resulting6,057 navigation IDs are not passes or a product denominator;
unsupported required behavior stays U and whole-Live coverage OPEN. No new
release, grade, site, portable criterion or general reset/startup/FP law follows.
## R21 finite current-provided base-case observations — 2026-10-23

**Analyst draft: 59 additional finite observations only.** DCO-6058 through
DCO-6116 follow the exact sole-approved point order, with each source-slot
label/group/alias joined in the [complete compact owner mapping](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-corpus-r21-declared-base-cases-finite-v1/mapping.json).
REQ-001 is navigation context only. The resulting 6,116 navigation IDs are
not passes or a product denominator; no general source-to-device law is admitted.

The only new observation authority is the [independent base-case review](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/corpus-declared-base-cases-v1-review.json),
6,294,675 bytes / SHA256 `2764a41c36f01abd8b52ccedfda2d5b577eeb4de447b6fb8b20f9bcd24cc7f82`.
Each new owner object has its exact REPORT JSON pointer and canonical SHA256
of the complete approved point, original supplied INPUT/script hashes,
provided-input key/path/identity, label/group and necessary scalar references.
The actual protocol, source and raw proof remains in that sole REPORT;
this owner review checks new wording/mapping/preservation without a second
actual/source/raw/numeric/provider or release-fixture proof review.

All 64 source dispositions are retained: 59 approved current histories,
four supporting references and one whole filter 200 group gap. All 30 source
groups/16 loops and 63 complete INPUT templates remain distinct from native
success counts. `defaults_44`/`defaults_48`/`noise_44`/`lfo_sine` supporting references
were not replayed and receive no new owner ID, PID, receipt, output, metric
or criterion. Their old original-path scripts and qualified byte/context
matches do not prove native history equivalence to new private-copy paths.
Zero strict private-SCRIPT intersections is not new credit for a path-only
rebind. Filter 200's entire word/vector/template remains U/null; the known
default host 28 word is neither substituted nor recomputed. No dropped
member, arbitrary subset or parameter-only deduplication is introduced.

Each accepted history retains all 38 original ordered decimal/binary64/
binary32 words, literal rate/order/default/post fields, inflag 1, exact
approved private supplied-input path and 16384-frame/block 512 process.
There is no warmup, reset, event or injected transport/MXCSR command.
Input artifacts are provided bytes, not reconstructed NumPy/sine/noise/RNG
recipes or numerical formula equivalence. The thirteen private 0444 inputs,
including ten used logical keys, remain distinct from original 0664 candidates;
old qualified three hashes and ten current-only hashes do not certify
historical construction or current in-memory consumption. Equal `impulse44`/
`impulse48` hashes do not merge their path/key associations. Input lane
asymmetry and permissions are descriptive, not a DSP output acceptance law.

The exact admitted profile is Corpus 13 C/TIME0/EXPLICITLIBM0/noBIN with the
unchanged 149632-byte xdev/model. Corpus 10's TIME1760000000 or TIME0/LIBM-unset/
BIN contexts and source env=None/unknown historical ambient environment are
not merged. Source-to-current executable, original construction/defaults,
loaded provider, actual FP/input register, native ABI, OSexec, current receiver
and public behavior bridges remain U. Seven selected script verbs are within
the prior approved nine-verb grammar; retained method text is not compilation
or executed-source certification. No original producer/helper/module/NumPy,
artifact generation, provider/model/FP change or new construction follows.

All 59 outputs are finite and nonzero in BOTH lanes; nine are lane-word-equal
and fifty unequal, with 59 hashes and 68 counted used-Linux CODE names.
Those are descriptive finite references only, not activation/symmetry/noise/
physical/pitch/quantizer/within-cell/publicARM laws, waveform oracles, metric/
window/tolerance, fitting, f0 or calibration. All fresh waveform priors/native
expectations/portable expected/comparator/grades remain NULL; application
predicate proof is false. Existing criteria and releases stay unchanged.

STRICT CalcA return 0/flag 0 or 1 and every other existing guard remain unchanged.
All 1,888 observed CalcA returns are literal 0, with 1,864 flag-one and 24 flag-zero
projections. This satisfies the selected parser without defining a native
return ABI/domain, success/error, activity, cause or public flag law. Rate
integers remain opaque. D08/D09 and older opaque-return policies do not transfer.
4,307 selected direct exports/1,888 CalcA/7,733,248 raw stereo bytes and zero
logged initializers do not enumerate nested/all-native work. The 127 declared
bindings (99 Linux/21 trap/7 data) remain separate from counted CODE use and
uncounted/global/data/transitive dependencies.

Custody is 98 applicable identities before/after EACH of 59 children,
5,782 actual pairs (21 runtime/provided+77 prebound per child), plus two
binding/method authority pairs. Endpoint equality is not a common-initial-only
claim or continuous mapping/provider/FP/source-execution/OSexec proof.
Raw/log/JSON FDfsync requests along the accepted branch do not establish
directory/crash durability; outer redirect FDfsync is not explicit. Existing
failed/skipped-fsync/parent/source history is not repaired by these new requests.

The unreserved 715,522,048-byte lifecycle plus 134,217,728 headroom and
268,435,456 concurrent allowance retain a 1,118,175,232-byte fresh minimum,
with the earlier 402,653,184 floor preserved. Full remaining raw, future 8MiB
stdout/stderr + 1MiB metadata per child, frozen 16MiB and final 128MiB allowances
are recomputed; these are not quotas, reservations or external-writer/
within-child-overshoot/escaped-descendant guarantees. Child 20 s CPU/wall/core 0/
FSIZE4MiB/DEVNULL/newgroup and first-fault/fullpartial/no-retry/cleanup limits
remain; the parent has resource guards but no wall watchdog.

The bounded eight prior INPUT censuses cover 5,146 records. Available exact
scripts/hashes/shared-command roles establish only the stated bounded
intersections: no private-SCRIPT match, four old-path supporting references
and three other-clock projections. They do not prove global never-run,
complete old history absence or output/PID/criterion transfer. All earlier
7/19/10/13 source and partial-ASOF scopes remain immutable. In particular,
the old Corpus 10 owned checker FAIL at zero-byte stderr bookkeeping remains
recorded, separate from Arrangement's approved actual audit; this annex
neither claims that checker passed nor repairs/reruns it. The old R19 leaf 0775
behind private 0700 ancestors and Square failed-guard/unused-prepare/phase
history retain their own qualifications.

Only this annex and revision number change; the date is already 2026-10-23.
All 13 whole requirements, 6,057 prior navigation IDs, 36 old case objects/40
literal rows, R3–R20 objects, old Acceptance/annex/navigation/U/criteria/
tolerances/state/history remain byte-exact. All 27 release groups/73
evaluations, modal 176 omissions, parked 96 setup, A1/receiver/default/FP/
provider/public unknowns and all prior failed/gap records remain unchanged.
Full reversal restores the exact 145,831-byte R20 baseline. No new portable
criterion, grade, site, release, implementation input or O observation is
admitted. Required unsupported behavior remains U and whole-Live coverage OPEN.
