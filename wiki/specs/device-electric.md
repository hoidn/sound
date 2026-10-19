---
id: SPEC-DEVICE-ELECTRIC
type: spec
status: draft
updated: 2026-10-18
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3 / macOS; reference renders from the Electric.bundle x86_64 slice
---

# Electric instrument: signal behavior and reference renders

## Scope

Feature FEAT-DEVICES, T1 device audio ([ADR 0004](../decisions/adr-0004-target-scope-t1.md)).
User task: a MIDI track holds the bundled Electric instrument. Its clip notes play, and the offline
render of that track must sound as Live's would. This draft specifies:

- the mono output Electric produces for timed note events and a set of stored parameter values,
  at 44.1 kHz and 48 kHz;
- note timing, voice allocation and the voice limit, and the response to pitch and velocity;
- the mallet, fork, damper and pickup sections, and the output stage;
- what happens when parameter values change during a render;
- the reference renders that define the output for T1, and the comparison metric.

How the parameters are stored, with their domains and defaults, is
[SPEC-BUNDLED-DEVICE-PARAMETERS](bundled-device-parameters.md). Which note events a clip sends,
and on which sample, is [SPEC-PLAYBACK-CORE](playback-core.md). Where the instrument's output
enters the mixer is [SPEC-MIX-GRAPH](mix-graph.md).

Excluded from T1, with behavior recorded where it was observed (REQ-016):

- pitch bend, sustain pedal, other controllers, aftertouch, MPE and per-note pitch bend;
- sample rates other than 44.1 and 48 kHz;
- display text and CPU load.

Every requirement is a **proposed contract**. Nothing was run against Live, and under
[ADR 0003](../decisions/adr-0003-no-reference-execution.md) nothing will be. The audio evidence
is extracted execution of the shipped x86_64 Electric code. The Live-side parameter path is a
static derivation. Canonical evidence: [Electric DSP](../research/device-electric-dsp.md).

## Evidence labels

| Label | Meaning |
| --- | --- |
| D | Documented in shipped bytes: the schema, the shipped presets and the bundle's export table |
| S | Static derivation from the 12.4.3 executables; not an observed run |
| S-cond | A static derivation that holds only under the named assumption |
| X | Extracted execution: the shipped x86_64 Electric slice ran on the stated calls in the harness of [ADR 0003](../decisions/adr-0003-no-reference-execution.md#extracted-execution-of-original-code). It shows what the device code computes for those calls. It does not show that Live makes them. The arm64 release slice is matched only by static comparison (appendix) |
| U | Unknown; no expected result, and not graded |

Only D, S and X clauses, and S-cond clauses whose assumption is accepted, may enter a release.
A U clause blocks the behavior it names, and each blocking U clause states its effect on T1.

## Terms

- **fs** is the sample rate. **P** = ⌊fs/1000⌋ is the control period: 44 frames at 44.1 kHz and
  48 at 48 kHz.
- **Render frame 0** is the first frame after the protocol's warm-up (REQ-001). It is a host-block
  start and a control-grid point.
- **Grid point g′ of an event at frame f.** Let b be the first frame of the host block that holds
  f, and g = P·⌊f/P⌋. Then g′ = g if g ≥ b, and g′ = g + P otherwise.
- **n(v), the controller scale of a host value v in 0..1.** Let c = 128v for v ≤ 0.5 and
  c = 126v + 1 otherwise. Then n = 0.5 when c = 64, and n = c/127 otherwise.

## Assumptions

| ID | Assumption | What rests on it |
| --- | --- | --- |
| A1 | Live sends each stored value as REQ-002's host value. The index order and conversions are N5's static reading (S); the chain from stored value to the call is inferred | REQ-002; every case for stored values |
| A2 | Live drives the device like the reference protocol. It creates the instance, sets the rate, sends all 33 values, and processes continuously in host blocks of 512 frames. Event frames are 0-based offsets within the block. Before the first note, the instance has processed a whole number of control periods, at least 4,400 frames at 44.1 kHz. Live's call order is static (S). The frame base, block sizes, grid phase and any pause in processing are unknown | REQ-001, REQ-004, REQ-014; every case |

## Requirements

### REQ-DEVICE-ELECTRIC-001 — reference renders define the output

- **X.** For T1, Electric's output for a list of timed note events and a set of host values is the
  reference render made with this protocol:
  1. a new instance is created;
  2. the sample rate is set (44,100 or 48,000 Hz);
  3. all 33 host values of REQ-002 are sent, in index order;
  4. the device processes a warm-up with no events: 11,264 frames at 44.1 kHz and 12,288 at
     48 kHz. That is 256 control periods and a whole number of 512-frame blocks. Its output is
     exactly zero and is discarded;
  5. the events follow at frames counted from render frame 0, in host blocks of 512 frames, with
     silent input and the input flag 0;
  6. the transport is not playing (position 0, 120 BPM).

  Both output channels are identical in every render, so references are mono binary32. They are
  retained with their scripts and SHA-256 (cases below).
- **X.** The output does not depend on any of these, bit for bit:
  - the host block size, when the events fall on the same grid points (64, 256, 333, 512 and
    2,048 tested);
  - flush-to-zero and denormals-are-zero;
  - the transport values;
  - the input buffer content and the input flag.

  A re-run gives a bit-identical render.
- **X.** Live's reset sequence leaves the envelope within 0.001 dB and the harmonic amplitudes
  within 0.01 dB of the case without it. The sequence is a device reset after the warm-up, then
  the Polyphony value again.
- **S, U.** Live creates the instance, sets the rate and sends the values (S,
  [N5](../research/device-parameter-mapping-native.md#how-live-loads-a-bundle)). Unknown: when Live
  runs the reset sequence; which block sizes and event frame base it uses; and whether it stops
  calling the device while the device reports it may stop. The device first reports this about
  3 s after creation or after the last note-off (X). **Effect on T1:** the timing rule of REQ-004 is defined relative to
  the device's own grid. A2 places that grid; Live's grid phase is not established.

### REQ-DEVICE-ELECTRIC-002 — from stored values to host values

- **S** ([N5](../research/device-parameter-mapping-native.md#electric-loungelizard-complete-33-indices)).
  Live sends 33 host values. Indices 0 to 31 correspond to the stored parameters in N5's order,
  from 0 Polyphony to 31 KeyboardStretch; index 30 is KeyboardTranspose. Each stored value is
  first clamped to its domain (SPEC-BUNDLED-DEVICE-PARAMETERS). Then:
  - **Polyphony and PickupModel** pass as their index;
  - **KeyboardTranspose** passes as the stored value rounded to the nearest 1/32768, then truncated
    toward zero;
  - **index 32** is always 48;
  - **every other parameter** passes unchanged, as binary32.
- **S.** `PerNotePitchBendRange` is stored but not sent.
- **S-cond (A1).** A stored Live Set value acts as the host value above.
- **D, U.** A new Electric either starts from the constructor values or loads the Defaults
  preset, which differs only in PickupAmpIn and PickupAmpOut (0.42 against 0.5). Which one applies
  is SPEC-BUNDLED-DEVICE-PARAMETERS REQ-009 U. **Effect on T1:** none for Live Sets, which store
  their values. Both starting points are rendered (DEL-001, DEL-005).

### REQ-DEVICE-ELECTRIC-003 — controller scale and steps

- **X.** Host values in 0..1 act through n(v): Volume, PickupAmpOut and PickupAmpKeyboardScaling
  follow exact laws in n(v) or c (REQ-012). n(0.5) = 0.5, n(0.25) = 0.25197, n(0.75) = 0.75197.
- **X.** PickupSymmetry and PickupDistance act in 128 steps, ⌊c⌋: host values 0.25 and 0.2525
  render bit-identically. The 11 other controls tested change the output for the same difference.

### REQ-DEVICE-ELECTRIC-004 — note events and timing

- **X.** A note-on is a status byte 0x90 to 0x9F. The channel has no effect: channels 1, 2 and 16
  render bit-identically. A note-on with velocity 0 renders bit-identically to a note-off.
- **X.** For a note-on at frame f, every frame before g′ + P is exactly 0. The note's first
  non-zero sample is at g′ + P. This holds for all 318 note-ons tested: blocks of 512, 64 and 333
  frames at 44.1 kHz, and 512 at 48 kHz. It also holds for 118 of the 119 sounding reference cases.
  In the remaining case, the E-Piano MKII Hollow preset, the attack starts below binary32
  resolution and the first non-zero sample is at g′ + P + 2.
- **X.** A note-off (0x80 to 0x8F, or a note-on with velocity 0) changes the output from frame g′
  on (201 of 201 tested). Release velocity has no effect: 127 renders bit-identically to 0. A
  note-off for a key that is not sounding changes nothing.
- **X.** All 128 keys sound. A key may sound several times at once (REQ-005).
- **S-cond (A2).** With render frame 0 a grid point and blocks of 512, the onset of a note-on at
  render frame f is P·⌊f/P⌋ + P. One period is added when that grid point lies before the start of
  f's block.
- **U.** Live's grid phase and event frame base. **Effect on T1:**
  - A one-based frame base would move the onset by one period for events at frames f with
    (f + 1) a multiple of P.
  - A different grid phase moves onsets by 0 to P − 1 frames relative to song time.
  - Note positions in a T1 render are sample-exact only under A2.

### REQ-DEVICE-ELECTRIC-005 — voices and polyphony

- **X.** Polyphony index p (labels `2` … `32`) allows p + 2 voices at once. This was tested for
  all 31 values with p + 2 and p + 3 staggered held notes. This settles the meaning of the
  labels: SPEC-BUNDLED-DEVICE-PARAMETERS REQ-014 holds them as U.
- **X.** A note-on that needs a voice when all are in use takes one in this order:
  - a released voice that is still sounding, before any held one;
  - otherwise the oldest held voice, not the lowest note.

  The stolen voice fades out linearly over one control period, scaled by about 1 − (k + 1)/P at
  frame g′ + k for k = 0 … P − 1, where g′ is that of the new note-on. It is silent from g′ + P on.
- **X.** Each note-on starts a new voice, even on a key that is already sounding. Two strikes of
  one key equal the sum of two single strikes within −64 dB, the noise floor. A note-off releases
  every voice of its key.
- **X.** Changing Polyphony while notes sound changes the output from the next grid point on. The
  sounding notes then fall away (−43 dB against −18 dB unchanged, 20 ms to 280 ms after the
  change).

### REQ-DEVICE-ELECTRIC-006 — pitch

- **X.** At the defaults (KeyboardTranspose 12, KeyboardFineTune 0.5, KeyboardStretch 0.5), A4
  (note 69) sounds at 440.329 Hz and C4 (note 60) at 261.621 Hz. From note 60 up, the deviation
  from equal temperament on A = 440 Hz repeats by pitch class, within 0.06 cents:

  | C | C♯ | D | D♯ | E | F | F♯ | G | G♯ | A | A♯ | B |
  | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
  | −0.04 | −0.04 | 0.03 | 0.16 | 0.35 | 0.61 | 0.86 | 1.10 | 1.27 | 1.29 | 1.12 | 0.70 |

  Notes 48 to 59 are within 0.23 cents of this pattern, and notes 21 to 47 lie between −1.8 and
  +2.8 cents. The measured fundamental of each note from 21 to 108 is retained. Notes below 21 are
  graded only by their reference renders.
- **X.** All partials are harmonics of the fundamental (REQ-011).
- **X.** KeyboardTranspose t transposes by t − 12 semitones (t = 0 and 24: −1,200.0 and
  +1,200.0 cents). The pitch-class pattern follows the sounding note.
- **X.** KeyboardFineTune v shifts every note by (v − 0.5)·100 cents: −49.6, −24.8, +25.0 and
  +50.0 cents at v = 0, 0.25, 0.75 and 1 (C4 and C6; C2 within 0.8 cents).
- **X.** KeyboardStretch v shifts every note by about (0.5 − v)·14.4 cents: +7.0 to +7.5 cents at
  v = 0 and −6.8 to −7.2 cents at v = 1, for notes 39 to 105. No stretch that grows with distance
  from a reference note was found.
- **X.** A change of these three parameters retunes sounding notes from g′ + P on (REQ-014).
- **X.** 48 kHz agrees with 44.1 kHz within 0.12 cents from note 57 up. Lower notes differ by up to
  one binary32 ulp bound (4.7 cents at A0), which the metric allows.

### REQ-DEVICE-ELECTRIC-007 — velocity response

- **X.** At the defaults, velocity raises both the level and the brightness. The loudest 10 ms
  frame of C4 is −36.6, −30.3, −23.2, −15.9, −15.0 and −9.9 dBFS at velocities 1, 32, 64, 96, 100
  and 127.
- **X.** MalletForceVelocity sets how much velocity raises the strike force:
  - at 0 (with MalletStiffnessVelocity 0) the sustain is −38.4 dB at every velocity;
  - at 1, velocity 127 gives +11.1 dB.
- **X.** MalletStiffnessVelocity sets how much velocity raises the mallet stiffness. A stiffer
  strike is quieter at these settings, so at 1 the sustain falls from −38.4 dB at velocity 1 to
  −60.9 dB at 127 (with MalletForceVelocity 0).
- **X.** Velocity 1 sounds the same at every sensitivity setting.

### REQ-DEVICE-ELECTRIC-008 — mallet section

Measured on C4, velocity 100, at host values 0, 0.25, 0.5, 0.75 and 1. Sustain is the RMS from
50 ms to the note-off. Renders at 0 and 1 are retained (DEL-006, 007).

- **X.** MalletStiffness is not monotonic. The sustain is −68.2, −35.3, −16.6, −23.1 and −40.6 dB,
  and the attack brightens at the top: the centroid of the first 20 ms is 1.9 kHz at 1.
- **X.** MalletForceStrength raises the level and the upper harmonics. The sustain goes from
  −50.3 to −8.7 dB, and harmonic 4 from −126 to −14 dB.
- **X.** MalletNoisePitch, MalletNoiseDecay and MalletNoiseAmount shape a transient in the attack
  and leave the sustain within 0.1 dB. At MalletNoiseAmount 1 the peak is 1.28, against 0.30.
- **X.** MalletStiffnessKeyboard, MalletForceKeyboard and MalletNoiseKeyboardScaling have no effect
  at note 60. Away from note 60 the effect grows, with the sign of v − 0.5. For example,
  MalletForceKeyboard 1 gives a peak of 3.94 at note 84 and 0.019 at note 36 (DEL-013).
- **U.** Values between the sampled points. **Effect on T1:** such values are graded only by
  further reference renders made under REQ-001 (see Revision and handoff).

### REQ-DEVICE-ELECTRIC-009 — fork section

- **X.** ForkToneBarDecay sets the decay of the sustained tone: harmonic 2 decays at −123, −35,
  −10.2, −3.2 and −1.0 dB/s at host values 0 to 1. ForkToneBarVolume sets its level, from −37.1
  to +0.3 dB sustain, brighter as it rises.
- **X.** ForkTineVolume, ForkTineDecay, ForkTineColor and ForkTineKeyboardScaling act on the
  attack transient. At ForkTineVolume 1 the peak is 0.37 and the attack centroid 715 Hz. At C4,
  with the default ForkTineVolume, the others change the sustain and harmonics by less than 0.1 dB.
- **X.** ForkReleaseTime sets the release. The time from the note-off until the level is 60 dB
  below the level before it:

  | ForkReleaseTime | 0 | 0.25 | 0.5 | 0.75 | 1 |
  | --- | --- | --- | --- | --- | --- |
  | C2 (note 36) | 0.09 s | 0.21 s | 0.50 s | 1.15 s | 2.68 s |
  | C4 (note 60) | 0.02 s | 0.05 s | 0.13 s | 0.30 s | 0.71 s |
  | C6 (note 84) | 0.02 s | 0.02 s | 0.04 s | 0.09 s | 0.20 s |

- **U.** Values between the sampled points, as in REQ-008.

### REQ-DEVICE-ELECTRIC-010 — damper section

- **X.** DamperAmount mainly sets the level of the random component of REQ-013. At C4 that level is
  −59.9, −41.6 and −25.0 dB re the note at host values 0, 0.5 and 1. The deterministic sustain
  changes by at most 1.6 dB.
- **X.** DamperBalance moves the random component from the held note to the release. At 1 it is
  −76 dB during the note and is heard after the note-off. DamperTone changes its color and
  changes the sustain by at most 0.2 dB.
- **X.** All three take effect for a sounding note from its note-off on (REQ-014).

### REQ-DEVICE-ELECTRIC-011 — pickup section

- **X.** The pickup forms harmonics of the fundamental. All partials are harmonics, and every
  harmonic frequency moves with the fundamental.
- **X.** PickupSymmetry trades the fundamental for the second harmonic: at 0, harmonic 1 is
  −82.6 dB and harmonic 2 −12.2 dB; at 1, harmonic 1 is −11.8 dB and harmonic 2 −40.6 dB.
- **X.** PickupDistance: a nearer pickup is louder and brighter. The sustain goes from −12.9 to
  −26.2 dB from 0 to 1, and harmonic 5 from −18.1 to −91.7 dB.
- **X.** PickupAmpIn drives the pickup amplifier, from −34.6 to −1.9 dB sustain, brighter as it
  rises.
- **X.** PickupModel W (1) differs from R (0) in level and harmonic balance: the loudest frame is
  −20.3 dB against −15.0 dB (DEL-009).
- **U.** PickupSymmetry, PickupDistance and PickupAmpIn values between the sampled points, as in
  REQ-008.

### REQ-DEVICE-ELECTRIC-012 — output stage

- **X.** **Volume** v scales the output by n(v)², relative to v = 1, within 1.5 × 10⁻⁷ at 23 values.
  v = 0 is silent. The default 0.7047892 gives n = 1/√2, exactly −6.02 dB below v = 1.
- **X.** **PickupAmpOut** v scales the output by 15(c − 64)/64 dB relative to v = 0.5, within
  3 × 10⁻⁶ dB at 17 values. The range is −15 dB just above 0 to +14.77 dB at 1. v = 0 is silent.
- **X.** **PickupAmpKeyboardScaling** v scales the output of note k by 2^((n(v) − 0.5)(k − 60)/4).
  At v = 0 that is +18.06 dB at note 36 and −27.09 dB at note 96; at v = 0.5 there is no effect.
- **X.** These three are pure gains: the waveform is otherwise unchanged.
- **X.** The output is limited to −4.0 … +4.0. A hot setting holds 7,045 frames at exactly +4.0
  and 7,070 at −4.0. Both output channels are identical.

### REQ-DEVICE-ELECTRIC-013 — random component

- **X.** Every note carries a random component, generated per frame while a voice sounds. Its
  generator is seeded from the clock once, when the instance is created. Renders with other clock
  values differ from the note's first frame on.
- **X.** Its level is 20 log₁₀ RMS((x_a − x_b)/√2)/RMS(x_a) over the note, for two renders that
  differ only in the seed. It is −41.6 dB at the defaults (range −43.2 to −38.6 dB over four
  seeds). Over the cases it ranges from −76 to −3 dB, and each case states its value.
- **X, U.** Inferred: in Live the realization differs between instances and sessions. No render
  can fix it. **Effect on T1:** the random waveform is not graded. Only its level is graded,
  where the reference's four seeds agree within 6 dB. The deterministic measures exclude
  elements that the seed moves (metric).

### REQ-DEVICE-ELECTRIC-014 — parameter changes over time

The values below are for a host value set between blocks while a note sounds; g′ is the grid
point of the block's first frame.

- **X.** These parameters change a sounding note:

  | Parameter | First changed frame |
  | --- | --- |
  | Volume, Polyphony (REQ-005) | g′ |
  | PickupModel | g′ + 1 |
  | KeyboardFineTune, KeyboardTranspose, KeyboardStretch | g′ + P |
- **X.** ForkReleaseTime, the fork tine and tone-bar volumes, ForkTineKeyboardScaling,
  ForkTineColor, the mallet noise parameters and the damper parameters also act at the note-off.
  A change while the note is held changes the output only from the note-off's g′ on.
- **X.** The other parameters are taken at note-on, and a change does not affect sounding notes.
  They are the mallet stiffness and force values, ForkTineDecay, ForkToneBarDecay,
  PickupSymmetry, PickupDistance, PickupAmpIn, PickupAmpOut and PickupAmpKeyboardScaling.
  PitchBendRange has no effect without pitch bend; its timing with bend was not run.
- **X.** Volume moves linearly from the old gain to the new one over exactly 4,000 frames from g′,
  at both rates. At frame g′ + k the gain ratio is 1 + (r − 1)(k + 1)/4000, where r is the ratio
  of the new gain to the old one.
- **X.** MalletForceVelocity moves to a new value over about 98 control periods. A note struck
  meanwhile uses an intermediate value; notes from 4,312 frames (44.1 kHz) or 4,704 frames
  (48 kHz) after the change use the new one. Every other note-on parameter applies to a note
  512 frames after the change.
- **X.** After creation, MalletForceVelocity ramps from the engine's built-in value to the sent
  value. A note at creation sounds 14.9 dB louder than a settled note. REQ-001's warm-up removes
  this.
- **U.** In Live, on which block boundary an automated value arrives. **Effect on T1:** automation
  of the immediate parameters can be early or late by up to one Live block plus one period.
  Note-on and note-off parameters are graded only for notes after the change.

### REQ-DEVICE-ELECTRIC-015 — sample rates

- **X.** At 48 kHz:
  - timing scales by P = 48 (REQ-004);
  - the Volume ramp stays 4,000 frames;
  - the pitch agrees within REQ-006;
  - the harmonic levels of C4 agree with 44.1 kHz within 0.01 dB.
- **X.** A rate change on a running instance gives the output of a new instance at that rate,
  within 0.001 dB in envelope and 0.01 ulp bound in frequency.
- **U.** Other rates. **Effect on T1:** renders at rates other than 44.1 or 48 kHz are not graded.

### REQ-DEVICE-ELECTRIC-016 — other MIDI input (outside T1)

- **X.** Pitch bend shifts sounding notes by ±12r semitones at full deflection, where r is the
  PitchBendRange host value. At r = 0.25, 0.5 and 1, A4 bends to 523.24, 622.29 and 880.66 Hz.
- **X.** Controller 64 at 127 holds released notes until it returns to 0.
- **U.** Other controllers, aftertouch, MPE and per-note pitch bend. **Effect on T1:** none. T1
  clips carry notes only.

## Timing and state

- **Units.** Frames at the stated rate; frame 0 is render frame 0 (REQ-001).
- **Latency.** A note-on's sound starts one control period after its grid point (REQ-004).
- **Persistent state.** None beyond the stored parameters.
- **Determinism.** The deterministic part is bit-for-bit repeatable for a given protocol and event
  list. The random component depends on the clock (REQ-013).

## Comparison metric

Proposed, pending acceptance as the T1 device-audio criterion of ADR 0004. A sample-by-sample
comparison is not usable, for three reasons:

- the random component differs per instance;
- one-ulp libm changes move the pitch by about two thirds of a binary32 ulp bound, so the phase
  drifts;
- the arm64 slice has 171 fused multiply-adds that the x86_64 slice lacks.

A candidate render passes a case when every line below holds. The measures are computed the same
way on the candidate and on the reference render. The estimator is in the appendix.

| Measure | Definition | Graded elements | Tolerance |
| --- | --- | --- | --- |
| Timing | Every frame before the first note's g′ + P is exactly 0 | Each case's first note | Exact. The first non-zero frame is the reference's, except where the reference itself starts within 3 frames after g′ + P |
| Envelope | 20 log₁₀ RMS of consecutive 10 ms frames (fs/100) from frame 0 | Frames within 40 dB of the loudest frame | The case's `env` tolerance |
| Bands | Third-octave levels, 50 Hz to 16 kHz, of 4096-frame Hann windows at the case's start frames | Bands within 30 dB of the window's strongest band | The case's `bands` tolerance |
| Partials (single-note cases) | Harmonics k = 1 … 8 below fs/2 − 200 Hz at k·f0 over [onset + 30 ms, note-off): amplitude at the window start, decay rate, frequency | Harmonics within 30 dB of the strongest | Amplitude: the case's `amp`. Decay: the case's `decay`. Frequency within 4·b(f0), with b(f0) = 3·2⁻²⁵/θ² + 2⁻²³ and θ = 2πf0/fs |
| Random level | REQ-013's level, from two candidate renders that differ only in the noise seed | Cases whose four reference seeds span 6 dB or less (94 of 119) | Within 6 dB of the reference mean |

Per-case tolerances come from six variant renders of the original:

- four other clock values, about 37 days apart;
- every inexact libm result moved one ulp up, and one ulp down.

An element is graded only when no variant moves it by more than 1.5 dB (2 dB/s for decay). Such
elements are dominated by the random component or lie near a null. Each tolerance is twice the
largest variant deviation over the graded elements, with floors of 0.05 dB (envelope), 0.1 dB
(bands and amplitude) and 0.1 dB/s (decay).

Over the 120 cases, the median tolerances are 0.22 dB (envelope), 0.46 dB (bands), 0.43 dB
(amplitude) and 0.15 dB/s (decay). The largest is 2.96 dB.

Harmonic frequencies moved by at most 0.78 b(f0) in any variant. The exception is PickupSymmetry
0 at 2.66, whose harmonic 1 lies near −83 dB. The frequency tolerance therefore leaves a margin of
five, or 1.5 in that case.

Four cases leave most loud envelope frames ungraded: their deterministic part lies under the
random component. They are MalletStiffness 0, MalletStiffnessKeyboard 1 at notes 36 and 84, and
the A0 tail. Each case's graded element lists and tolerances are fixture data
(`results/cases.json` `graded`, `tolerances`).

## Acceptance cases

Expectations are X renders of the original x86_64 code under REQ-001's protocol. None has been
run against Live, and under ADR 0003 none will be. Kinds: P positive, B boundary, T timing,
U not graded.

### Fixtures

All renders come from [t12-electric-v1](../../analysis/ableton-live-12.4.3/r2/t12-electric-v1/manifest.json)
`raw/<case>.wav`: mono IEEE binary32, after the warm-up. Each `<case>.script` gives the exact
calls. `results/cases.json` gives each render's SHA-256, host values, events, measures, graded
elements, tolerances and random level.

"Defaults" means the constructor values (REQ-002). A single-note case plays C4 (note 60) at
velocity 100 from frame 0, releases it at 13,230 (0.3 s) and lasts 22,050 frames, unless stated
otherwise. It measures bands at 0, fs/10 and the note-off. Each case states only its changes in
stored values.

The preset phrase is:

- note 48 at velocity 100 from 0 to 17,640;
- notes 64, 67 and 72 at velocity 80 from 22,050 to 39,690;
- a length of 52,920 frames.

### Cases

| Case ID | Requirement | Kind | Setup | Expected result / comparator | Reference render |
| --- | --- | --- | --- | --- | --- |
| DEL-001 | 001, 004, 006, 011 | P, T | Defaults; C4 held to 22,050; 44,100 frames | Metric. Onset 44; f0 261.621 Hz; harmonics 1 to 4 at −26.4, −12.5, −26.9, −29.0 dB; random level −41.6 dB | `defaults_c4` |
| DEL-002 | 015 | P, T | DEL-001 at 48 kHz (held to 24,000) | Metric. Onset 48; f0 261.610 Hz; harmonics within 0.01 dB of DEL-001 | `defaults_c4_48` |
| DEL-003 | 006 | P, B | Defaults; notes 21, 36, 48, 72, 84, 96, 108 | Metric. f0 27.523, 65.407, 130.814, 523.236, 1046.473, 2092.958, 4185.919 Hz | `key_21` … `key_108` (7) |
| DEL-004 | 007 | P, B | Defaults; C4 at velocity 1, 32, 64, 96, 127 | Metric. Loudest 10 ms frame −36.6, −30.3, −23.2, −15.9, −9.9 dBFS | `vel_1` … `vel_127` (5) |
| DEL-005 | 002 | P | Defaults preset (PickupAmpIn, PickupAmpOut 0.42) | Metric | `preset_defaults_c4` |
| DEL-006 | 008 | P, B | Each of MalletStiffness, MalletStiffnessKeyboard, MalletStiffnessVelocity, MalletForceStrength, MalletForceKeyboard, MalletForceVelocity at 0 and 1 | Metric; levels as REQ-008 | `p04_0` … `p09_1` (12) |
| DEL-007 | 008 | P, B | MalletNoisePitch, Decay, Amount, KeyboardScaling at 0 and 1 | Metric | `p10_0` … `p13_1` (8) |
| DEL-008 | 009 | P, B | ForkReleaseTime, ForkTineDecay, ForkTineVolume, ForkTineKeyboardScaling, ForkTineColor, ForkToneBarDecay, ForkToneBarVolume at 0 and 1 | Metric | `p14_0` … `p20_1` (14) |
| DEL-009 | 011, 012 | P, B | PickupSymmetry, PickupDistance, PickupAmpIn, PickupAmpKeyboardScaling at 0 and 1; PickupAmpOut at 1; PickupModel W | Metric | `p21_*`, `p22_*`, `p24_*`, `p25_1`, `p26_*`, `p23_1` (10) |
| DEL-010 | 012 | B | PickupAmpOut 0 | Every frame exactly 0 | `p25_0` |
| DEL-011 | 010, 013 | P, B | DamperTone, DamperAmount, DamperBalance at 0 and 1 | Metric; random level −59.9 dB at DamperAmount 0, −25.0 dB at 1 | `p27_0` … `p29_1` (6) |
| DEL-012 | 006 | P, B | KeyboardFineTune 0 and 1; KeyboardTranspose 0 and 24; KeyboardStretch 0 and 1 | Metric. f0 254.231, 269.288, 130.815, 523.236, 262.713, 260.535 Hz | `p03_*`, `p30_0`, `p30_24`, `p31_*` (6) |
| DEL-013 | 008, 009, 012 | P, B | MalletStiffnessKeyboard, MalletForceKeyboard, MalletNoiseKeyboardScaling, ForkTineKeyboardScaling, PickupAmpKeyboardScaling at 0 and 1, at notes 36 and 84 | Metric | `p05_*_key36` … `p26_*_key84` (20) |
| DEL-014 | 012 | P | Volume 1 and 0.25 | Metric; the gain law itself is DEL-027 | `p02_1`, `p02_0.25` |
| DEL-015 | 001, 002 | P | The 17 shipped Electric presets, preset phrase, 44.1 kHz | Metric | `preset_<name>` (17) |
| DEL-016 | 015 | P | Wurli Classic Piano and E-Piano MKI Simple, preset phrase at 48 kHz | Metric | `preset_*_48` (2) |
| DEL-017 | 005 | P | Polyphony 0; C4, E4, G4 on at 0, 2,205, 4,410; all off at 22,050; 26,460 frames | Metric. C4 is stolen: absent from g′ + 44 = 4,444 on | `poly_2_steal` |
| DEL-018 | 005 | P | Polyphony 0; C4 on at 0; E4 on at 2,205 and off at 4,410; G4 on at 6,615 | Metric. The released E4 is stolen and C4 is kept | `poly_2_released_first` |
| DEL-019 | 005 | P | Polyphony 0; C4 at 0 and again at 2,205; E4 at 4,410 | Metric. The first C4 strike is stolen | `poly_2_repeat` |
| DEL-020 | 005 | P | Defaults (32 voices); notes 36 to 68, one every 300 frames; all off at 30,870; 44,100 frames | Metric. Note 36 is stolen when note 68 starts | `poly_32_steal` |
| DEL-021 | 014 | T, P | DEL-001 shape (off at 17,640); Volume set to 0.35 before the block at 8,192 | Metric. Linear gain ramp from 8,228 over 4,000 frames | `auto_volume` |
| DEL-022 | 014 | T, P | KeyboardFineTune set to 1.0 before the block at 8,192 | Metric. Retuned from 8,272 on | `auto_finetune` |
| DEL-023 | 014 | T, P | MalletForceVelocity set to 1.0 at frame 0; C4 at 2,048 | Metric. Intermediate force; onset 2,112 | `auto_forcevel` |
| DEL-024 | 004 | T | Note-on and note-off at the frames of `probes_events.json` `timing`: 318 note-ons and 201 note-offs, blocks of 512, 64 and 333 at 44.1 kHz and 512 at 48 kHz, frames counted from creation | Each first non-zero frame and first changed frame equals REQ-004's rule | X rule; renders not retained |
| DEL-025 | 005 | P | For each Polyphony index p, p + 2 and p + 3 staggered notes, with and without the first | The first note sounds with p + 2 notes and is absent with p + 3 | X; `voices.limit` |
| DEL-026 | 004 | P | Velocity-0 note-on; release velocity 127; channels 2 and 16; note-off of another key | Each identical to its counterpart in the candidate's own renders | X (bit-identical in the original) |
| DEL-027 | 012 | P | Volume at 23 values; PickupAmpOut at 17 values; PickupAmpKeyboardScaling at 0, 0.25, 0.75, 1 at notes 36 to 96 | Gain ratios of REQ-012 within 10⁻⁴ dB | X; `gains`, `laws` |
| DEL-028 | 001 | P | DEL-001 in host blocks of 64, 256, 333, 2,048; transport playing at 90 BPM; input a 440 Hz sine | Identical to the candidate's DEL-001 render | X (bit-identical in the original) |
| DEL-029 | 013 | U | Any case | The random waveform: not graded. Its level is graded under the metric | — |
| DEL-030 | 004 | U | Live's grid phase or a one-based frame base | Not graded (REQ-004 U) | — |
| DEL-031 | 016 | U | Pitch bend, controller 64, MPE | Not graded in T1; the X values of REQ-016 are informative | — |
| DEL-032 | 008–011 | U | Stored values not among the cases | Graded only by further reference renders under REQ-001 | — |

## Open questions

Proposed for [questions](../questions.md) (not edited by this draft):

- **Q-025, protocol.** The same Live-side unknowns as Corpus: event frame base, block sizes and
  reset timing. Two more matter for Electric:
  - the grid phase at render start;
  - whether Live stops processing while the device reports it may. That would move the grid.
- **Q-025, metric.** The per-case variant-derived tolerances and the 6 dB random-level band need
  acceptance for ADR 0004.
- **Intermediate values.** Electric has no closed form except the laws of REQ-006 and REQ-012.
  Verification sets with other values need reference renders from the analyst harness.
- **Polyphony labels.** SPEC-BUNDLED-DEVICE-PARAMETERS REQ-014 can cite REQ-005 for their meaning.

## Analyst evidence appendix

Analysis-only. Do not copy into a handoff. Canonical evidence:
[Electric DSP](../research/device-electric-dsp.md).

- Retained run: `analysis/ableton-live-12.4.3/r2/t12-electric-v1/`, harness `harness/xdev*.c`,
  built to `/var/tmp/sound-analysis/t12-electric/xdev`.
- Slice: `Electric.bundle/Contents/MacOS/Electric` (SHA-256 `bb0d404b…5ef95`). The x86_64 slice is
  at offset 16,384, 267,648 bytes, SHA-256
  `f121bb8d66ec1f3d8e9cb830e8081b25922cece6011cc12857c78180cd89dd32`.

| Clause | Evidence |
| --- | --- |
| 001 protocol, invariances | `el.py`; `results/probes_params.json` `protocol`; exports `0xc030`, `0xc120`, `0xc240`, `0xc550`, `0xc5d0` (x86_64) |
| 002 | N5 `out/conversions.tsv` (LoungeLizard rows); `el.host_values`; presets read by `el.read_preset` |
| 003, 012 | `probes_params.json` `gains`, `laws` (sample ratios, `quantized_0.25_vs_0.2525_identical`) |
| 004 | `probes_events.json` `timing`, `messages`; the first non-zero frame in `cases.json` |
| 005 | `probes_events.json` `voices`; `probes_params.json` `protocol.polyphony_to_*` |
| 006 | `probes_events.json` `tuning` (`defaults_44`, `cents_re_defaults`) |
| 007 | `probes_events.json` `velocity`; `cases.json` `vel_*` |
| 008–011 | `probes_params.json` `sweeps`, `release_60db_s_by_note_and_fork_release_time`; `cases.json` |
| 013 | `cases.json` `noise_level_db`; `srand`, `time` and `rand` counts in `imports` |
| 014 | `probes_params.json` `latch_during_note`, `change_before_next_note`, `ramps`, `laws.forcevel_note_rms_re_settled`, `start_up_*` |
| 015 | `cases.json` `defaults_c4_48`; `protocol.rate_44100_then_48000_vs_48000` |
| 016 | `probes_events.json` `messages.pitch_bend_f0_hz`, `cc64` |
| Metric | `measure.py` (estimator `fit.py`: demodulation, linear-phase FIR, fit of phase and log magnitude); `cases.json` `variant_max_deviation_on_graded`; `results/fma_scan.txt` |
| arm64 equivalence | Static: 171 fused multiply-adds in 63 arm64 functions; none in x86_64; Apple's libm not compared. Not executed |

## Revision and handoff

| Revision | Date | Change |
| --- | --- | --- |
| 1 | 2026-10-18 | First draft (packet t12-electric-v1). 16 requirements: 1 S with an S-cond clause and a D/U part (002); 15 with X clauses, of which 001, 004, 008, 009, 011 and 013–016 have U parts and 004 an S-cond clause. 32 cases: 28 graded (23 by retained renders, 5 by X rules or laws), 4 not graded (DEL-029 to 032) |

Not released. A first release could carry these parts:

- REQ-001, 003 to 007, 012 and 015;
- the X parts of 008 to 011, 013, 014 and 016;
- cases DEL-001 to 028, with the 120 renders and `cases.json` as fixtures.

It needs the metric accepted for ADR 0004, A2 accepted or replaced by a traced protocol, and a
reviewer's check that the clauses describe behavior rather than recovered code. Stored values
other than the cases need on-demand reference renders. That is a validation-analyst task.
