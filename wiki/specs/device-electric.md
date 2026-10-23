---
id: SPEC-DEVICE-ELECTRIC
type: spec
status: draft
updated: 2026-10-23
access: analysis
revision: 16
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

**X, finite supplied-host scope (revision 4).** The [25-point transpose catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-electric-r4-transpose-finite-v1/cases25.json)
records exact host integers 0–24 at index 30, with all other 32 host words fixed.
The 22 new cases DEL-CS-009–030 cover integers 1–11 and 13–23; 0, 12 and 24
reference existing DEL-CS-002, 001 and 003. These are supplied host words, not
new observations of stored/UI values or their rounding, actual A1 dispatch,
current receiver identity or the Defaults-preset insertion choice. The prior
stored 11.99999/12 alias remains the R3 author-conversion fact only.

**X, finite supplied-host observations (revision 7).** The [R7 host catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-electric-r7-host-midi-finite-v1/host-catalog58.json)
adds DEL-CS-285–315 for 31 supplied host vectors: Polyphony index 0 at 0–29 and
PickupModel index 23 at 1, only in the fixed P1 history below. All 58 declared
aliases join 56 full vectors, including the 25 prior Transpose references.
This single-note class does not newly validate stored/UI conversion, actual
A1 delivery, current receiver identity, Polyphony labels, p + 2 voice capacity,
stealing or general control effects. The existing clauses retain their scope.

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

**X, finite note-key observations (revision 5).** [DEL-CS-031–157 and the inherited key-60 reference](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-electric-r5-note-keys-finite-v1/cases128.json)
retain the complete 128-value typed note-key catalog only in the fixed 33-word
P1 history below. Both matching note-on/off keys vary; no other state changes.
The 127 fresh outputs are finite and nonzero. These observations do not newly
validate the broader note-range, channel, event-timing or onset laws above.
REQ-006 remains pitch context, not a newly measured or fitted frequency law.

**X, finite note-on velocity observations (revision 6).** [DEL-CS-158–284 and the inherited velocity-100 reference](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-electric-r6-velocity-finite-v1/cases128.json)
retain all 128 typed note-on velocity bytes only in the fixed 33-word P1/key-60
history below. Only note-on data2 varies. The 127 fresh outputs are finite;
velocity0 is silent in this initially unvoiced history. This observation does
not independently establish equivalence to a note-off in an existing voice.
The broader event/channel/timing and velocity-zero dispatch laws above are
not newly validated; REQ-006 remains unchanged, with no newly measured
parameter-dependent velocity curve, pitch formula or calibrated response.

**X, finite matching-channel and note-off byte observations (revision 7).**
[DEL-CS-316–457 and the inherited P1 baseline](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-electric-r7-host-midi-finite-v1/midi-catalog144.json)
retain two independent typed axes: matching channel nibbles 0–15 in both status
bytes, and note-off velocity bytes 0–127 with the baseline channel. Their 144
aliases join 143 complete histories; both zero aliases reference one old
DEL-CS-001/P1 control. These fixed histories do not newly establish the general
channel, release-velocity, velocity-zero dispatch, event-timing or public laws
above. Parameter-vector equality alone does not identify an event history.

**X, finite independent On/Off key and channel observations (revision 8).**
[DEL-CS-458–741](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-electric-r8-independent-midi-finite-v1/new-cases284.json)
add 284 supplied histories at the unchanged 33-word P1 context. They vary
one On key, Off key, On channel nibble or Off channel nibble at a time;
the other event's corresponding byte stays at its baseline. One inherited
DEL-CS-001/P1 INPUT reference serves four baseline aliases without replay,
fresh receipt/PID/metrics or criterion transfer. These finite observations
do not newly validate the broader channel, unmatched-key, release, timing,
voice, velocity-zero dispatch or public laws above. New waveform priors,
portable expected/comparator/grade remain NULL; new application-predicate
proofs remain false.

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

**X, finite transpose captures (revision 3).** DEL-CS-001 to 003 retain the
approved original outputs for the exact supplied host vectors with
KeyboardTranspose 12, 0 and 24. Each has finite binary32 output, identical
channels, a numerically zero warm-up and first non-zero render frame 44, under
the recorded protocol below. The author conversion of stored 11.99999 and 12
gives the same host 12 input, so both aliases name DEL-CS-001. This conversion
is the existing author-side mapping; it does not establish A1's actual Live
dispatch. These captures add no pitch estimate, retuning law or portable exact
waveform criterion. Their input words, full capture identities and expectations
are in the [finite fixtures](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-electric-r3-finite-v1/cases.json).

**X, finite transpose observations (revision 4).** [DEL-CS-009–030](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-electric-r4-transpose-finite-v1/cases25.json)
adopt the 22 approved fresh captures under the exact P1 history below, completing
its 25-point supplied integer catalog with three inherited R3 references. Every
fresh capture is finite, has byte-identical channels and a zero warmup, and first
becomes nonzero at render frame 44. The 22 fresh output hashes are distinct.
These native observations add no f0 measurement, semitone-rule validation, pitch
curve, retuning trajectory, physical calibration or portable waveform criterion.
The existing broader pitch clauses are not newly validated by this annex.

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

**X, finite pickup pairs (revision 3).** DEL-CS-004 is the baseline for the
four complete settings in DEL-CS-005 to 008: PickupSymmetry or PickupDistance
at host 0.25 or 0.2525, with every other indexed value fixed. All five captures
are finite, have identical channels and a numerically zero warm-up, and first
become non-zero at render frame 44. Under this one fixed protocol and seed,
DEL-CS-005 and 006 have identical retained render bytes; so do DEL-CS-007 and
008. These two finite original relations do not extend the general controller
law, prove no effect at other inputs or establish smoothing or determinism.
Intermediate values and an accepted compatibility metric for these new captures
remain outside the finite evidence. Full inputs and the two pair relations are
in the [finite fixtures](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-electric-r3-finite-v1/cases.json).

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

Proposed as the general T1 device-audio criterion of ADR 0004. The finite metric
of [device-electric-v2](../../handoff/device-electric-v2/README.md) is accepted
only for its listed inputs and frozen measurement eligibility; broader criteria
below remain proposed. A sample-by-sample
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

### Finite control seams — revision 3

These eight new X case IDs directly adopt the [independently approved batch](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/electric-control-seams-v1-review.json).
The [owner packet](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-electric-r3-finite-v1/README.md)
maps every approved capture and pair relation to its exact input and retained
output identity. The 32 earlier rows remain unchanged, including DEL-029 to
032. No new original or candidate run, audio measurement or observation review
was performed for this adoption.

Common supplied protocol: original x86_64 Electric instance, 44,100 Hz, all 33
binary32 values sent in order, 512-frame blocks, silent input and input flag 0,
stopped transport at position 0 and 120 BPM. Constructor defaults use Volume
word `0x3f346d11`, pickup amps 0.5 and runtime index 32 = 48. The synthetic
11,264-frame warm-up precedes render frame 0; the clock substitution is 0, with
the existing inferred Park–Miller PRNG, glibc libm and C-locale/libc++ shim.
Neither the Defaults preset's 0.42 insertion choice nor current Live control
delivery is selected. Input word records are supplied host data, not child
register or FP-state traces.

| Case ID | Req | Supplied change from constructor defaults | Retained history |
| --- | --- | --- | --- |
| DEL-CS-001 | 006 | Host KeyboardTranspose 12; stored aliases 11.99999 and 12; P1 baseline | C4/velocity 100 on at 0, off at 22,050; 44,100 render frames |
| DEL-CS-002 | 006 | Host KeyboardTranspose 0; stored alias 0 | Same P1 history |
| DEL-CS-003 | 006 | Host KeyboardTranspose 24; stored alias 24 | Same P1 history |
| DEL-CS-004 | 011 | No change; P2 baseline | C4/velocity 100 on at 0, off at 8,820; 13,230 render frames |
| DEL-CS-005 | 011 | Host PickupSymmetry 0.25 | Same P2 history |
| DEL-CS-006 | 011 | Host PickupSymmetry 0.2525 | Same P2 history; finite render bytes equal DEL-CS-005 |
| DEL-CS-007 | 011 | Host PickupDistance 0.25 | Same P2 history |
| DEL-CS-008 | 011 | Host PickupDistance 0.2525 | Same P2 history; finite render bytes equal DEL-CS-007 |

Every case's observed expectation is finite output, channels equal word for
word, numerical-zero warm-up and first non-zero render frame 44. Capture hashes
identify the original evidence; they do not prescribe a candidate waveform
hash. The two pair relations are observations of these fixed original captures,
not a portable exact-waveform acceptance test. The longer P1 baseline and
shorter P2 baseline are separate histories. P1's four stored aliases produce
three distinct supplied host scripts, so no fourth native observation is
invented. No inactive or equal result was removed.

The current 117 released evaluations, three unstable exclusions and their
frozen measurement eligibility and tolerances remain unchanged. These new
finite facts add no calibration rule, random-waveform grade, ARM/Apple bound,
actual A1/A2 binding or public audio result. General metric proposals and the
unknown behaviors above retain their existing scope.

### Finite host-transpose integer catalog — revision 4

The [R4 catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-electric-r4-transpose-finite-v1/cases25.json) adopts 22 new finite **X native observations**,
DEL-CS-009–030, from the [sole actual/source approval](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/electric-transpose-integers-v1-review.json)
SHA256 `16783862180b314900c96762538313167874751f2fa68c5a867fdcbbf60a8e56`.
IDs follow ascending fresh host integers 1–11, 13–23. The whole 25-point catalog
retains host 0, 12 and 24 as references to DEL-CS-002, DEL-CS-001 and DEL-CS-003,
respectively; no duplicate case, fresh control, receipt, PID, UTC or old metric is
invented. All 40 earlier case IDs/rows, eight R3 case objects and two R3 pair relations
remain exact. The resulting 62 navigation IDs are not outcomes, grades or passes.

Each evaluation supplies the exact 33 ordered binary32 host words: Volume is
`0x3f346d11`, index 32 is 48, and only index 30 takes its catalog integer. The
recorded P1 context is 44,100 Hz, zero input and flag 0, stopped transport at
position 0 and 120 BPM, an 11,264-frame warmup followed by one 44,100-frame render
in 512-frame blocks (last render block 68 frames). The cumulative event queue has
note-on at total frame 11,264 (render frame 0), status 0x90, key 60, velocity 100;
note-off is total frame 33,314 (render frame 22,050), status 0x80, key 60, velocity 0.
The exact scripts, 33-word vectors, input history, provenance and raw output hashes
are joined to the approved summary for every point.

All 22 fresh captures contain 55,364 finite stereo frames including warmup, with
identical left/right channel words. Their warmup samples are positive zero and
the first nonzero render frame is 44. The catalog gives per-channel whole, warmup
and render peak/RMS/mean/nonzero observations; these are descriptive binary64
summaries, not calibrated tolerances. Three inherited controls retain only their
already approved observations and historical output/render hashes; missing old
numeric metrics or fresh process data are not synthesized. Distinct fresh hashes
are finite facts about these inputs, not evidence of a pitch formula or mechanism.

Original fresh waveform-prior NULLs remain history. Portable expected outputs,
comparators and candidate grades stay NULL. The recorded unchanged x86 harness,
Linux providers, explicit clock substitution 0 and inherited MXCSR behavior define
this context, not clock/seed stability, child register/FP-state proof or an Apple
host equivalence. The approving review's endpoint/interpreter/provider, process
cleanup and regular-file fsync limits remain part of each observation. No original
or portable candidate hash criterion, f0 estimate, physical tuning calibration,
retuning/history law, current stored-value/receiver binding, public A1/A2 or ARM
execution is admitted. ADR 0003's arm64 inference caveat applies.

The proposed general comparison metric, all old tolerances, U/state/error/history
clauses, DEL-029's random-waveform exclusion, three unstable exclusions and the
117 released evaluations remain unchanged. This is an analyst draft, with no new
release, candidate result or whole-product closure. Added wording, mapping and
preservation are the sole owner-review scope; the approved actual observations
are inherited by citation without another source/raw/result review.

### Finite typed note-key catalog — revision 5

The [R5 catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-electric-r5-note-keys-finite-v1/cases128.json) adds 127 finite **X native observations**,
DEL-CS-031–157, from the [sole actual/source approval](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/electric-note-keys-v1-review.json)
SHA256 `b0582f43026e386012d4f52ab9dd023db8ad21effdfd2c6e9e8e050a5652fffc`.
IDs follow ascending fresh keys 0–59 and 61–127. The full 128-point catalog keeps
key 60 only as the inherited DEL-CS-001 / P1 / ELECTRIC-AUDIO-004 reference,
through approved ETI-12. Both stored aliases 11.99999 and 12 remain attached to
that one host-input control. No duplicate ID, fresh control, receipt, PID, UTC or
missing historical metric is invented. All 40 earlier table rows, 62 IDs, eight
R3 case objects, two pair relations and the complete R4 25-point catalog remain
exact. The resulting 189 navigation IDs are not outcomes, grades or passes.

Only the key bytes in both matching events vary. Every point supplies the same
33 ordered binary32 host words: Volume `0x3f346d11`, KeyboardTranspose 12 and
index 32 equal to 48. The P1 context is 44,100 Hz, silent input and flag 0,
stopped transport at position 0 and 120 BPM, an 11,264-frame warmup followed by
44,100 render frames in 512-frame blocks (last render block 68). The queued
note-on is total frame 11,264 (render frame 0), status 0x90 and velocity 100;
the matching note-off is total frame 33,314 (render frame 22,050), status 0x80
and velocity 0. Destruction follows that single warmup/render history. All 256
packed 16-byte event records, supplied parameter tokens/bits and exact input,
output and receipt pointers are retained in the catalog. Existing factory,
clock-0 and unperturbed shim/MXCSR context are unchanged, not a new seed or
receiver model.

Every fresh capture has 55,364 finite stereo frames including warmup, with
byte-identical channels and nonzero render samples. The warmups are
**numerically zero**; this permits signed zero and is not a new positive-zero
byte assertion. All 127 fresh whole-output hashes are distinct. Native hashes
and exact copied output summaries become analysis-side finite native
expectations; they identify original observations, not a portable candidate
waveform criterion. No onset estimate, f0 measurement, pitch/range formula,
retuning law, fit, new metric/window, tolerance or physical calibration follows.
The historical key-60 reference retains only its approved facts; earlier
transpose-capture onset or positive-zero facts are not extended to the fresh
note-key class.

The bounded historical input intersection remains explicit. The old all-128-key
tuning history rendered 17,640 frames with its off event at that exclusive
render end. The old edge keys 0/127 and base-key 69 used 22,050 frames with off
at 13,230. Other released note-key fixtures have that shorter history too.
They are not the current P1 history. This is a scoped declaration/metadata join,
not a universal absence claim, new historical audio comparison or replay.
Retained declaration pins do not independently attest the original source
version or execution.

All original fresh waveform-prior NULLs remain immutable. Portable expected
outputs, comparators and candidate grades remain NULL. The approving review's
154 common whole-batch-before identity records are compared with each of 127
child-after arrays (19,558 recorded pairs); these are not independent
per-child-before snapshots. Recorded endpoints and interpreter strings do not
attest continuous loaded-provider, OS execution, transitive dependency or actual
child register/fenv/FP state. Rate returned the opaque integer 1; no success or
sample-clock semantics is assigned. The logs contain no initializer entries; this does not bound all nested native
or initialization calls. Import declarations and counted code-stub use
remain distinct, without proof of implicit data/provider absence.

Recorder/launcher JSON records request file flush/fsync; raw stdout/stderr/audio
FDs were closed and hashed without explicit FD fsync. Directory/power-loss
persistence is not proved. First detected post-child fault would stop later
children, but queued calls inside that child may already have executed; cleanup
branches do not prove every termination/escaped-process/IO path. No retry follows.
These method and retention limits remain attached to every observation.

No general note-range, onset, velocity/channel, deterministic waveform, current
stored-value/receiver, public Live A1/A2 clock/audio/state/lifecycle or ARM/Apple
law is admitted. ADR 0003's arm64 inference caveat applies. All previous
requirement bodies retain their exact text (REQ-004 only gains the finite
qualification), along with old U/error/history, metric/tolerance scope,
DEL-029's random-waveform exclusion, the three unstable exclusions and 117
released evaluations. R4's unchanged-body/count statements describe that
revision. No new release, candidate result, site or whole-product closure
follows. The new owner review covers only wording, mapping, IDs and preservation;
approved observations are inherited by citation without actual/source/raw or
numeric re-review.

### Finite P1 note-on velocity catalog — revision 6

The [complete 128-point catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-electric-r6-velocity-finite-v1/cases128.json)
and [point joins](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-electric-r6-velocity-finite-v1/joins128.json)
add 127 draft IDs DEL-CS-158–284 in ascending byte order excluding 100. Byte 100
keeps DEL-CS-001/P1/ELECTRIC-AUDIO-004/ETI-12 and stored aliases 11.99999/12;
it has no new ID, original call, PID, receipt or fabricated metric.
The [sole actual/source review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/electric-velocity-bytes-v1-review.json)
is the approved observation authority. This owner annex inherits that summary
without actual/source/raw or numeric re-review. It does not release any case.

The shared input is exactly all 33 ordered P1 host words, native x86_64 output
at 44,100 Hz, 11,264 warm-up frames followed by 44,100 render frames, blocks 512 with
last render block 68, zero audio/flag0 and stopped transport 0,0,120. Both event
keys stay 60; note-on at absolute 11,264 varies only its velocity byte 0–127;
note-off at 33,314 retains velocity 0. All other parameters and history stay
fixed. The catalog retains full token/binary32/reconstructed-binary64 input
metadata, packed events, source case, receipt and native output identities.
The reconstruction is not an entry-register, parser or floating-state trace.

All fresh outputs are finite and channel-word-equal; their warmups are
**numerically zero**, not a new positive-zero byte assertion for all warmups.
Fresh byte 0 has zero render samples; the other 126 fresh inputs are nonzero.
Silence is retained rather than rejected or fitted. Native expected entries
copy only the approved output identity and finite observation summary.
Original fresh waveform priors remain NULL. Portable expected outputs,
comparators and candidate grades remain NULL for every new case. No common
waveform tolerance or candidate pass follows from these observations.

The review records 154 common whole-batch-before identities compared with each
of 127 child-after arrays (19,558 endpoint pairs), not independent per-child-before
or continuous loaded-provider identity. Rate returned the opaque integer 1;
its success/sample-clock semantics remain unknown. No initializer entry was
logged, while nested/internal calls are not fully counted. Import bindings
and counted use are separate. Parent launcher/recorder/scripts were file-bound
before calls; retained PID/argv/time and file identities are not OSexec proof.
Raw audio/log files close/hash without explicit FDfsync; JSON fsync is not a
power-loss/directory guarantee. Existing ABI, FP/library, cleanup, source-origin
and receiver/model qualifications remain, under ADR 0003.

The older 63 FV/SV-by-velocity inputs have shorter render/off histories, as
qualified by the approved summary's selected input declarations. This is not
universal historical absence or a repaired original executed-source binding.
REQ-006 stays unchanged: this fixed P1 velocity catalog supplies no new
parameter-dependent curve, frequency/onset/range law, fitting, f0 estimator,
new metric/window/tolerance/calibration, actual public/current-parameter,
clock/lifecycle or Apple/ARM/candidate waveform equivalence. All required-U
and existing metric exclusions remain. No new release, candidate result,
site or whole-product closure is implied; coverage remains OPEN.

### Revision 7 finite supplied-host and MIDI histories

The [173 new cases](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-electric-r7-host-midi-finite-v1/cases173.json) add finite **X native observations** in one revision.
The [host catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-electric-r7-host-midi-finite-v1/host-catalog58.json) retains all 58 aliases and 56 complete vectors:
31 fresh observations receive DEL-CS-285–315 in recorded host-index/value order
(Polyphony 0–29, then PickupModel 1). The other 25 vectors reference the existing
R3/R4 Transpose cases, including the common P1 baseline, with no duplicate ID,
original call, fresh PID, receipt or metric. This is one note, not a new test of
p + 2 voice capacity, stealing or label meaning.

The [MIDI catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-electric-r7-host-midi-finite-v1/midi-catalog144.json) retains all 144 aliases and 143 complete histories.
DEL-CS-316–330 cover matching zero-based channel nibbles 1–15, changing both
note-on/off status low nibbles together. DEL-CS-331–457 cover note-off data2
bytes 1–127, with status bytes 0x90/0x80 unchanged. These are independent axes,
not their crossproduct. Both zero aliases reference the same inherited
DEL-CS-001 / P1 / ETI-12 / ELECTRIC-AUDIO-004 baseline through approved
velocity 100. Stored aliases 11.99999 and 12 stay attached to that one control.
The [complete joins](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-electric-r7-host-midi-finite-v1/joins173.json) keep parameter-vector identity distinct from
complete event/process/FP-context history. All 143 MIDI histories share one
parameter vector, while their event histories differ. Across both catalogs,
the shared baseline is one reference, not another native capture or case.

Only the two approved summaries provide observation authority: the
[sole host-domain review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/electric-finite-host-domains-v1-review.json),
SHA256 `aeba458a8dcd448048abbe18cd51fa5e166d80530a3be736755c04efc8dab530`,
and the [sole MIDI-axis review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/electric-midi-axes-v1-review.json),
SHA256 `f50281e51a0a8c4b2507e469512870ebd7dd207587b4d09a6c4a1244b6ae45f3`.
This owner adoption uses their complete approved input/provenance/output
summaries without actual/source/raw or numeric re-review. It adds no original
execution, model, provider, tool, construction or candidate result.

Each history supplies all 33 ordered binary32 P1 host words, including Volume
`0x3f346d11`, KeyboardTranspose 12 and index 32 equal to 48, except the selected
host-word change in the host catalog. The MIDI catalog leaves every host word
fixed and varies only its selected event bytes. The common protocol is
44,100 Hz, 11,264 warm-up frames then 44,100 render frames, 512-frame blocks
(last render block 68), silent input and flag 0, stopped transport 0/0/120,
clock substitution 0 and the existing unperturbed MXCSR/library treatment.
Note-on is absolute frame 11,264 (render frame 0), key 60, velocity 100;
note-off is absolute frame 33,314 (render frame 22,050), key 60, baseline
velocity 0. Full host tokens, binary32/reconstructed-binary64 projections,
events, packed 16-byte records and process histories remain joined. These
reconstructions are not child-register, parser or floating-state traces.

All 31 host captures are finite, nonzero and equal between channel words,
with two distinct fresh whole-output hashes. All 142 MIDI captures are finite,
nonzero and equal between channel words. Their one fresh whole-output hash
matches the already approved baseline hash metadata; old baseline audio was
not reopened. These are finite native identities in the recorded contexts,
not a general channel or release-velocity invariance, inactive-control,
repeat/seed stability, timing, mechanism, voice or deterministic waveform law.
Warm-ups are **numerically zero**, permitting either sign; this is not a new
positive-zero-byte assertion. Native expectations copy only approved output
identities and summaries. Original fresh waveform priors, portable expected
outputs, comparators and candidate grades remain NULL. No new f0 estimate,
metric, window, fit, tolerance, physical calibration or pitch law follows.

The old 120-script input intersection and the shorter channel/release Boolean
recipes remain bounded input metadata. They do not repair historical executed
source/version binding, recreate receipts, extend an old Boolean to this
history, or prove universal historical absence. Inherited Transpose and P1
references retain only their prior approved observations and qualifications;
no missing old metric, timestamp or PID is invented. Exact owner/research pins
in the actual packets are nongating as-of context, not runtime binding proof.

The host review records 59 common whole-batch initial identities compared with
31 child-after arrays (1,829 pairs); the MIDI review records 169 initial
identities compared with 142 child-after arrays (23,998 pairs). These are not
independent per-child-before or continuous loaded-provider/interpreter/OS
execution/register/fenv attestations. Parent and capture code were file-bound
before calls. MIDI author bookkeeping was not independent actual approval;
the sole peer separately verified every retained raw/log/audio member. Rate
returned the opaque integer 1, with no success/sample-clock meaning. No
initializer entries were logged; selected direct exports and CalcA counts do
not bound nested native, constructor or library work. Import declarations
and counted code use remain distinct and do not prove provider/data absence.

Raw logs/audio closed and hashed without explicit FD fsync; JSON regular-file
flush/fsync does not prove directory or crash durability. First detected
post-child failures stop later children, while queued calls inside that child
may already have executed. Catchable group cleanup is not proof for all
termination, escaped-descendant or transitive dependency paths. No original
retry or repair follows. The host packet's mutable input-metadata KeyError
was corrected before freeze/calls and is retained as authoring history.

All 316 old navigation IDs, 40 table rows, eight R3 objects/two pairs and full
R4/R5/R6 catalogs remain exact. Only bounded REQ-002 and REQ-004 qualifications
are appended; their old prefixes, the other 14 whole clauses, old acceptance
annexes, timing/state/error/U/history, tolerances, DEL-029 random-waveform and
three unstable exclusions, and released 117 evaluations / 129 objects remain
unchanged. The resulting 489 navigation IDs are not grades or passes. ADR
0003's arm64 inference caveat applies. No new public A1/A2, current stored-value
or receiver binding, MIDI/channel/release/voice/clock/lifecycle law, Apple/ARM
or candidate waveform equivalence, release, site or whole-product closure is
admitted; coverage remains OPEN. Earlier revision counts describe those
revisions. The sole new owner review covers wording, mapping, IDs and
preservation, inheriting actual proof only by the two approved summaries.

### Revision 8 finite independent On/Off key and channel observations

The [complete catalog](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-electric-r8-independent-midi-finite-v1/cases285.json)
retains 288 aliases / 285 complete histories. DEL-CS-458–741 are 284 fresh
observations: On key 0–127 except 60 with Off key 60 fixed; Off key 0–127
except 60 with On key 60 fixed; On channel nibble 0–15 except 0 with Off
status 0x80 fixed; and Off channel nibble 0–15 except 0 with On status 0x90
fixed. One old DEL-CS-001 / ELECTRIC-AUDIO-004 / P1 INPUT reference serves
four baseline aliases, without a new ID, replay, PID, receipt, output,
metric, expectation or criterion. [All 288 joins](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-electric-r8-independent-midi-finite-v1/joins288.json)
preserve WHOLE histories and two packed 16-byte events. Parameter-vector
equality alone does not identify a history. No paired key/channel changes,
additional events, host-state crossproducts, reset or new timing are added.

Only [Arrangement's sole actual/source review](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/electric-independent-midi-bytes-v1-review.json),
SHA-256 `338e2dd88385ea586f42da79a0c69ba037385626c14a3d29bc799f829a95e528`,
supplies the observations. This owner maps that approved summary without
actual/source/raw/audio/numeric re-review. The author recorded the batch;
its actual review was independent. Root reviews only this new owner wording,
mapping, IDs and preservation. No second actual review or old control replay.

The 33 original decimal tokens, reconstructed binary64 and binary32 words
remain fixed at P1, including index 32=48. The vector hash remains
`9ef2b39d47ca833730a9bbfd9d26e3bdc08a847df0ead035bd14d948bc35a43a`.
Both events are queued BEFORE the unchanged warmup/render recipe: On
11264/status 0x90/key 60/velocity 100; Off 33314/status 0x80/key 60/velocity 0;
then warm 11264 and render 44100 at rate 44100, block 512, final block 68,
zero audio/input flag 0. Only the selected byte varies. The retained stopped
transport 0/0/120, TIME0, per-entry MXCSR1f80 and unperturbed existing
bindings are recorded-model premises, not proof of native FP/ABI, Live
clock coordinates or public current receiver. No construction, tool, patch,
provider, FP treatment or physical calibration is introduced.

All 284 approved fresh outputs are finite, nonzero and channel-word-equal;
128 fresh hashes are descriptive only. THIS batch's warmup words are all
positive zero, independently checked in the approved summary; earlier
numeric-warmup-zero qualifications are unchanged. Hashes/unsigned word
summaries are native finite references, not portable waveform criteria.
No unmatched-key handling, channel matching, release/voice semantics,
productive control, deterministic waveform, f0, estimator, fit, metric,
window, tolerance, calibration or public/ARM law follows. Old Boolean,
default, executed-source/version and input-binding gaps remain scoped.
All fresh priors/new waveform expectations, portable expected/comparator/
grade stay NULL. Required U and the broader S/history remain open.

All new capture/parent/analysis/checker/initial assembler code was pinned
before THIS capture; the staged owner materializer is historical, not a
regenerator. This does not repair earlier source/preparation/checker/default
or OSexec/FP qualifications. One COMMON set of 314 initial identities is
compared to each of 284 child-after snapshots: 89,176 pairs, NOT separate
per-child before snapshots or continuous interpreter/provider/mapping/FP
proof. Parent and recorder have distinct PIDs; source-level argv/endpoints
are not independent OSexec attestation. Raw/stdout/stderr FDs were closed/
hash checked without explicit FD fsync; JSON requests fsync, without
crash/powerloss/directory durability. Post-child guards cannot retract
within-child earlier calls. Cleanup of selected groups/direct children
does not exhaust escaped/uncatchable/parent-loss/native paths and was not
failure-tested. Soft resource limits/floors/conditional overshoot are not
OS quotas, reservations or guarantees against unmodeled/external writers.
The existing r2-large storage route proves no relocatability.

133 declared bindings (100 Linux, 26 trap, seven data) differ from counted
use: 64 Linux code names per child; neither proves provider/global absence.
Each child has 145 selected direct exports / 109 CalcA. There are zero
logged initializers; all nested/native call counts remain unknown. Rate's
signed integer remains opaque, not a sample-clock or success/type law.

Only REQ-004 gains a bounded append. All 15 other whole bodies, including
ENTIRE R7 REQ-002, old REQ-004 prefix, 40 original rows / 489 prior navigation
IDs, R3–R7 objects/catalogs, criteria/tolerances/U/state/error/history and
released 117 evaluations / 129 inventory objects remain exact, with full
R7 reversal. Earlier catalog preservation is inherited from the approved
R7 owner report; its documented old-catalog DATA read-scope exception is
not repeated or erased. No older proposal/code/actual/raw/provider/release
fixture is opened for this owner. The resulting 773 navigation IDs are not
passes, application outcomes, site credit, release or whole-product closure.

### Revision 9 finite pickup controller representatives

The [complete catalog](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-electric-r9-pickup-controller-cells-finite-v1/cases256.json) and
[joins](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-electric-r9-pickup-controller-cells-finite-v1/joins256.json) add 256 finite **X native observations**,
DEL-CS-742–997: PickupSymmetry host index 21 at n/127 for n=0–127,
then PickupDistance host index 22 at the same 128 representatives. Each axis
changes one original host token independently; there is no crossproduct.
All 256 aliases identify distinct complete histories and all are fresh.
The original literal 0.5 is not any n/127 representative, so there is no
inherited baseline, replay, duplicate reference, old PID/receipt/metric or
output-criterion transfer. Controller-cell names are INPUT metadata, not
newly observed UI values or a native quantizer. REQ-011 supplies navigation
context only; all sixteen existing requirement bodies remain exact.

Only the [sole actual/source review](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/electric-pickup-controller-cells-v1-review.json),
SHA256 `52a51498304fadca95d82b9938e33f80622b1237b329ba506dad01e98b61e0d6`,
supplies these observations. This annex maps its complete approved summary;
there is no new original execution or actual/source/raw/audio/numeric review.
The exact 33 original decimal tokens and reconstructed binary64/binary32
words are retained, with only index 21 or 22 varied. The original P1 context
has key 60, velocity 100, index 32=48, rate 44100, zero input/flag 0 and
stopped transport 0/0/120. BOTH events are queued BEFORE warmup: On at
11264/status 0x90/key 60/velocity 100, Off at 33314/status 0x80/key 60/velocity 0;
then warm 11264 and render 44100 in 512-frame blocks, final render block 68.
TIME0, the existing per-entry MXCSR1f80 and unperturbed Linux bindings are
recorded-model premises, without a new construction, tool, build, patch,
provider, FP treatment, seed, timing or physical calibration. Reconstructed
words are not child-entry parser/register/fenv or current receiver proof.

All 256 approved captures have 55,364 finite, channel-word-equal stereo
frames, including warmup, and nonzero render samples. There are 255 distinct
whole-output hashes. THIS packet's warmup words are all positive zero and
its first nonzero render sample is 44 in both lanes. These are descriptive
finite capture facts only; older numeric-zero qualifications stay unchanged.
Hash references identify retained native bytes, not a native waveform
expectation, portable waveform criterion, onset or general warmup law.
All fresh priors, native/new waveform expectations, portable expected
outputs, comparators and candidate grades remain NULL; application admission
is false. No productive pickup effect, within-cell equality, control-step or
quantizer law, frequency/transfer formula, f0, fit, metric/window, tolerance,
calibration, deterministic waveform, public Live route or Apple/ARM law follows.

The approving review's EPC-RV-Q01 remains explicit: frozen resource-budget
line items total 537,030,912 bytes, exceeding the declared 536,870,912-byte
normal estimate by 160,000 bytes. This arithmetic discrepancy is not repaired.
Literal 512MiB packet/resource guards and the recorded free-space endpoints
passed with ample space. The lifecycle estimate and 128MiB headroom were
unreserved, without quota, concurrent-writer or escaped-process guarantees;
conditional soft overshoot remains possible. No resource/capture retry follows.

One COMMON set of 286 initial identities (10 runtime records plus 276 frozen
files) is compared with each of 256 child-after snapshots: 73,216 pairs,
NOT separate per-child-before snapshots or continuous loaded-provider,
interpreter, mapping, OSexec or FP-state attestation. All capture, parent,
checker, finalizer, initial assembler, inputs and scripts were pre-call-bound;
the retained initial assembler/fragment are historical stages, not final
regenerators. Their isolated-import and meaningful f64-negative corrections
occurred before freeze/calls, not as frozen repair or original retry. Old
executed-source/default/checker/preparation/binding gaps remain qualified.

Raw stdout/stderr/audio FDs were closed and hashed without explicit FD fsync;
JSON receipts requested fsync, without directory/crash/power-loss durability.
First detected post-child failures stop later children but cannot retract
within-child earlier calls. Selected process-group/direct-child cleanup does
not exhaust parent loss, uncatchable termination, escaped descendants or
transitive library paths. The existing r2-large placement is not relocatability.
There are 133 declared bindings (100 Linux, 26 trap, seven data), distinct from
64 counted Linux code names per child; neither proves provider/global absence.
Rate's integer 1 remains opaque. Selected counts are 145 direct exports and
109 CalcA per child; zero logged initializers does not bound nested/native
or initialization work. ADR 0003's arm64 inference caveat applies.

All 773 previous navigation IDs, 40 table rows, R3–R8 objects/catalogs and
pairs, old acceptance annexes, requirement/metric/tolerance/U/state/error/history
text, DEL-029 random-waveform and three unstable exclusions, and released
117 evaluations / 129 inventory objects remain unchanged with full R8 reversal.
Earlier revision counts describe those revisions. Prior preservation comes
only from the approved R8 owner report's embedded mapping and preservation;
the documented R7 old-catalog DATA read-scope exception is retained and not
repeated. No old proposal/catalog/code/provider/fixture or actual proof is
opened for this owner. The resulting 1,029 navigation IDs are not passes,
portable criteria, candidate outcomes or a product denominator. Root reviews
only new wording, mapping, IDs and preservation. No new release, site credit,
public/current-receiver/A1/A2/clock/lifecycle or whole-product closure follows.

### Revision 10 finite Polyphony load and omission observations

The [complete catalog](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-electric-r10-load-omission-finite-v1/cases124.json) and
[joins](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-electric-r10-load-omission-finite-v1/joins124.json) add 124 finite **X native observations**,
DEL-CS-998–1121, linked to REQ-005. For each supplied Polyphony index
p = 0–30, two nominal note loads n = p + 2 and p + 3 each have a full
history and a history omitting only the first note: 31 × 2 × 2 = 124
histories and 62 same-end pairs. Polyphony index 31 is unselected. These are
the source-declared 31 comparisons already described in the draft, with new
retained captures and precise input/output references. They are not all 32
settings, never-run or globally new inputs, new voice counts, stealing or
residual criteria, or repaired historical raw/executed-source evidence.

Every case supplies all 33 original decimal host words except index 0 = p
and index 28 = positive zero. At 44,100 Hz, the queue receives note-ons
at absolute frames 11,264 + 1,024k, key 40 + k, velocity 100; the omission
history drops only k = 0. Both histories queue events **before** the
11,264-frame warm-up, then render 1,024n + 8,820 frames in blocks of 512
(last render block 116). The end is identical within each pair. There are
no note-offs or resets. Zero audio input/flag 0, stopped transport 0/0/120,
TIME 0, unperturbed libm and the existing per-entry MXCSR model remain the
recorded supplied protocol, not Live's public parameter/event receiver.

The [sole approved actual/source review](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/electric-polyphony-load-omission-v1-review.json)
is the only observation authority for this annex. It records all 124 fresh
once-only histories as finite, with equal stereo words and nonzero render
portions; their warm-ups contain positive-zero bytes. All 62 pairs have
identical warm-up bytes and different render bytes. These are descriptive
references for those exact pairs, not a test that identifies a voice, proves
a first note absent, fits a residual, establishes a voice-capacity/stealing
law or admits a new tolerance. The 94 output hashes identify retained bytes
only. All 124 fresh priors, native waveform expectations, portable expected
values, comparators and grades remain **NULL**; new application proof is
false. No old output or criterion transfers into these observations.

This capture records 19 actual before/after custody pairs per child (2,356
total), plus three whole-batch authority endpoints. That scope is not
continuous loaded-provider or FP-state attestation. Its prebound raw, log,
JSON and JSONL file-descriptor fsync requests do not establish directory or
crash durability and do not repair earlier Electric raw/log NOFDfsync.
Source/version association, historical env-None/defaults, actual OS exec,
FP/ABI/provider continuity and cleanup limits stay qualified in the approved
summary. The INPUT scope qualification retains the incidental unexecuted
adjacent residual-call expression; no estimator or residual result was used.
Prior EPC-RV-Q01 (537,030,912-byte line items versus 536,870,912 declared;
160,000-byte discrepancy), prior common-initial custody qualifications and
the R7 old-catalog DATA read-scope exception remain unchanged. No new public,
ARM, calibration, general warm-up/onset, capacity or numerical law follows.

All 16 whole requirement bodies, 1,029 prior navigation IDs, 40 old rows,
R3–R9 objects, existing criteria/U/state/error/history and the released
117 evaluations/129 inventory objects are preserved. Earlier revision counts
remain historical. The resulting 1,153 navigation IDs are finite observation
navigation, not passes, portable criteria or a product denominator. Root's
review covers only this new wording, mapping, IDs and preservation. No
actual/source/raw/numeric proof is repeated; no release or site closure follows.

### Revision 11 finite declared rate/block protocol observations

The [seven-history mapping](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-electric-r11-seven-protocols-finite-v1/mapping.json)
adds DEL-CS-1122–1128 only from seven newly approved supplied histories and
eight source aliases. `pr_ref` and `rerun` name ONE history/capture. This is
not the P1 context, an inherited baseline or a never-run/global novelty
claim. REQ-001 and REQ-015 are context only: their entire existing bodies
and all parent assertions remain unchanged, without endorsement or new
validation here. No old120 output/PID/receipt/metric/criterion transfer or
source-executed-version/default/history bridge is repaired.

The sole actual/source authority is the [approved Electric seven-history
review](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/electric-rate-block-protocol-v1-review.json),
632177 bytes/SHA256 `0824ef9e85c1f9d4bf2fbd892e817fbe9c3181808b54c660c0fea0334cd5cc77`.
Only its approved summary supplies all 33 original decimal tokens and
binary64/binary32 words, scripts, whole-history identities, receipt/output
references and observations. First five histories queue On11264/Off24494
BEFORE warm11264 plus render22050 at 44100 Hz, with block512/64/256/333/2048
respectively. Direct48000 queues On12288/Off26688 BEFORE warm12288 plus
render24000 at block512. The transition creates/rates44100, sends all33
setters, processes11264 at512 WITHOUT queued events, then rates48000,
queues On23552/Off37952 and processes36288 at512. Literal absolute event
coordinates/command order remain exact; no generalized native clock,
render-relative equivalence, rate/block invariance or capacity law follows.

Existing149688-byte xdev/bundle/slice/model only, zero input/inflag0,
C/TIME0/LIBM-unset, no added MXCSR/transport/reset or new receiver/provider/
model/tool/FP treatment. Historical envNone/default/source-to-executed-version,
provider/FP/OSexec associations remain unknown. Rate signed integer
projections are opaque; zero logged initializer lines is not proof of all
native startup absence. All1000 CalcA satisfy the frozen ret0/flag01 guards;
1253 selected direct exports exclude unknown nested/provider/native calls.

Seven finite stereo captures, all both-channel nonzero and word-equal,
three raw hashes and 70 used Linux names are descriptive only. Import
binding declarations differ from used-code counters. No portable waveform,
general rate/block, pitch/onset/productivity, voice capacity, current public
Live/ARM/Apple, physical or calibration law is admitted. All new priors,
native-waveform expectations, portable expected/comparator and grades remain
NULL; application predicate proof is false. No fitting, thresholds, old
metric budget transfer or release criteria are introduced.

133 actual per-child19 before/after custody pairs plus two whole-source
pairs are endpoints, not continuous loaded-provider/nativeFP/register-entry/
ABI/OSexec attestation. Successful child raw/log/JSON file descriptors request
fsync; parent outer files have no explicit FDfsync. No directory/crash/
powerloss guarantee or earlier raw-FDfsync repair follows.128MiB lifecycle
plus128MiB headroom and full remaining-output/metadata guards are unreserved,
not quotas, external-writer/escaped-child/within-child-overshoot guarantees.
No retries or automatic continuation are authorized by this owner annex.

Only this annex and revision metadata change. All16 whole requirements,
1153 prior navigation IDs/40 original rows/all R3–R10 objects/criteria/U/
state/error/history, EPCQ01/common-custody/old FDfsync/R7 preservation-read
exception and releases117 evaluations/129 inventory objects remain exact
with full reversal. Preservation inherits only current R10 and its sole
owner REPORT's embedded approved metadata; absent old bytes are not
reconstructed and old proposals/catalogs/fixtures are not reopened.
The resulting1160 navigation IDs are not passes or a whole-product
denominator. No new release/grade/site/application proof or closure;
required unsupported U remains OPEN.

### Revision 12 finite declared protocol observations and retained unknowns

[DEL-CS-1129–1132 and the complete 17-history disposition catalog](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-electric-r12-protocol-partial-finite-v1/mapping.json)
admit exactly four finite **X native observations**: `reset_sequence`,
`reset_only`, `transport_playing_90bpm` and `ftz`, in that source order.
The only observation authority is the [sole approved partial actual/source
review](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/electric-declared-protocol-remainder-v1-partial-review.json),
889098 bytes/SHA256 `f3edc51acf0db886e38a1657cecf43d3e96848f4aebcba53e47017a97498b305`.
The mapping copies its approved summary only; no original capture, source,
raw audio or numerical proof is reviewed again for this owner. REQ-001 is
context only. All 16 existing requirement bodies remain unchanged and are
not newly validated. The new annex does not endorse a general reset,
transport, FTZ, stopping, state, FP or public behavior law.

These are source-declared supplied histories, not P1 baseline reuse or a
never-run/global-novelty claim. Each accepted history creates/rates 44100,
sends all 33 original decimal/binary64/binary32 words, queues On11264 and
Off24494 for key60/velocity100 and off0 **before** a 11264-frame warm-up,
then renders22050 at block512 (last34), with zero audio input/flag0.
The reset sequence literally sends `param 0 30.0` then `reset` after warm-up;
`reset_only` sends only `reset` there. Sorting full source command tuples
produces this order; it is not the reversed prose order in an older claim.
The transport history sends `transport 1 16.0 90.0` after warm-up. The FTZ
history sends `mxcsr 0x9fc0` before input/processing. These are supplied
command bytes, not attestation of native register/FP state or Live dispatch.
C/TIME0/LIBM-unset and the admitted149688-byte xdev/bundle/slice model are
recorded context; historical envNone, compiled-source association, defaults,
loaded-provider/OSexec/current receiver, A1/A2, FP and ARM remain qualified.

Only the four approved outputs are admitted: finite, both-channel nonzero
and stereo-word-equal, with positive-zero warm-up bytes. Their two raw hashes
and the six descriptive pair relations remain finite byte references only:
reset_sequence/reset_only match, transport_playing_90bpm/ftz match, and the
four other pairs differ. There is no portable equality criterion, causal
control comparison, reset/transport/FTZ invariance, fitted metric or new
calibration/tolerance. Fresh waveform priors, native waveform expectations,
portable expected/comparator and grades remain **NULL**; new application
predicate proof is false. No old baseline/PID/output/metric/criterion transfers.
The accepted scope records411 selected direct exports and264 CalcA; zero
logged initializers does not bound initialization, nested or all native work.
Rate signed integers remain opaque. Binding declarations differ from counted
positive Linux CODE uses and do not prove provider/dependency completeness.

`activity_note` remains **guard FAIL/U**, with no new ID, accepted output,
protocol metric, expected waveform, comparator or grade. Its child exited0
and returned full diagnostic raw bytes, but the frozen ret0 guard rejected
one literal CalcA return1/flag1 at block8, absolute frames3584–4096. All862
CalcA had already completed, including854 later calls in that child, before
the parent detected the guard failure and stopped later children. Return1's
native meaning and cause remain unknown. Finite diagnostic bytes do not
convert it into an accepted observation or repair the frozen guard.
`activity_empty` and all eleven startup histories remain **unattempted/U**,
without new IDs, PIDs, receipts, outputs or criteria. The complete mapping
preserves all17 dispositions as four accepted, one failed/U and12 unattempted/U;
it is not a completed17-success class. No retry, continuation, guard change
or transfer of Tension's separately scoped opaque-return policy is selected.

The report's100 actual per-child before/after identity pairs across five
attempts, plus two whole-source endpoint pairs, are not continuous source,
input-read, provider, FP, ABI or OSexec attestation. Successful child raw/log/
JSON descriptors request fsync; failed raw skips that branch, and parent
outer redirects have no explicit FDfsync. No directory/power-loss durability
or repair of earlier fsync gaps follows. Full8513-byte driver source was
read for command admission, not compilation/vendor ABI proof. Copied521/557
bounds describe the old rate-only profile, not the862-call activity history.
Frozen pre-call/old-draft selection labels stay historical as-of metadata.
Resource checks are unreserved floors, not quotas, within-child stop,
escaped-descendant, external-writer or parent-watchdog guarantees. All sole
review qualifications remain explicit in the mapping.

Only this annex and revision metadata change. All1160 previous navigation
IDs,40 old rows,16 whole requirements, R3–R11 objects/catalogs/pairs,
criteria/tolerances/U/state/error/history, EPCQ01/common-custody/FDfsync and
R7 preservation-read exceptions, and released117 evaluations/129 inventory
objects remain exact with full reversal. Preservation inherits current R11
and its sole owner REPORT's embedded metadata only; no old proposal,
catalog, provider, fixture, release proof or actual is reopened. The resulting
1164 navigation IDs are not passes, portable criteria or a product denominator.
No new release, grade, site, public/ARM law or product closure follows.
Required unsupported behavior stays U/OPEN.

### Revision 13 finite activity-empty observation and later partial snapshot

[DEL-CS-1133 and the complete later twelve-history mapping](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-electric-r13-activity-empty-finite-v1/mapping.json)
admit **one finite X native observation**, `activity_empty`, only from the
[sole approved later partial review](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/electric-declared-protocol-unlaunched12-v1-partial-review.json),
318644 bytes/SHA256 `add1375a0575e5a4585f2538ace052d4a3685df581baeac3c7d2c4fc960ae446`.
The observation authority is that REPORT summary only. This owner repeats no
actual/source/raw/numeric proof. REQ-001 is context only and all 16 existing
requirement bodies remain unchanged, without new validation or endorsement.

The history supplies all 33 original decimal/binary64/binary32 host words,
create/rate44100, no events and no warm-up, zero audio input/flag0, then
441000 frames in block512 (last168), under the existing149688-byte xdev/
bundle/slice model, C/TIME0/LIBM-unset and unperturbed default entry-FP context.
No new receiver, initialization, FP, provider, reset or transport treatment is
introduced. The exact captured441000-frame stereo output consists entirely
of positive-zero words. This is an exact finite quiet observation, not a
criterion for general inactivity, initial state, silence, activity flags or
public behavior. Its recorded process sequence is262 ret0/flag1 blocks then
600 ret0/flag0 blocks; the flags have no newly assigned semantics. The accepted
counts are898 selected direct exports/862 CalcA and3528000 raw stereo bytes;
zero logged initializers does not bound startup or nested/all native work.
Rate1 remains an opaque signed integer. Native waveform priors/expectations,
portable expected/comparator and grade remain **NULL**; new application
predicate proof is false. No old baseline/PID/output/metric/criterion transfers.

The later packet's `startup_0` is **guard FAIL/U**, without a new ID, accepted
protocol metric, expected waveform or criterion. The child exited0/full raw,
but the unchanged ret0 guard rejected literal return1/flag1 in blocks8 and9
(frames3584–4096 and4096–4608). All26 CalcA finished before parent rejection,
including18 calls after the first bad block and17 after the second. Its finite
diagnostic raw bytes do not admit an observation or establish native return
meaning, ABI, cause, success, activity, startup or event-delivery law. The ten
remaining startup histories remain **unattempted/U in that packet's snapshot**,
without IDs, outputs, PIDs, receipts, metrics or criteria. No retry, guard repair
or transfer of Tension's separately scoped opaque-return policy follows.

These are **dated packet snapshots**, not a global current never-run or
no-continuation assertion. R12's earlier seventeen-history catalog remains
exactly four accepted/failed `activity_note`/twelve then-unattempted. This later
twelve-history packet separately records one accepted/failed `startup_0`/ten
unattempted. It does not rewrite the earlier as-of metadata, replay its five
attempted histories, repair either failed guard, or claim all17 succeeded.
Any later selection or disposition belongs to its own approved evidence and
canonical research; neither frozen snapshot asserts a permanent capture ban.
Source-declared startup Off-at-end and historical INPUT/source admission are
not new proof of event delivery, current Live binding or whole-history novelty.

The sole report records36 actual ordered per-child before/after custody pairs
(18 each) plus one whole-batch authority pair. These are endpoints, not native
FP, continuous loaded-provider, input-read, OSexec or compiled-source attestation.
133 binding declarations differ from counted Linux CODE uses and do not prove
all transitive/global/data/native dependencies. Accepted raw readFDfsync was
requested; failed startup raw skipped that branch, while both child logs and
JSON request fsync. Parent outer FDs have no explicit fsync. Directory/crash/
power-loss durability, cleanup and earlier raw-FDfsync gaps are not repaired.
Resource floors are fresh but unreserved, not quotas, external-writer,
within-child-stop/overshoot, escaped-descendant or parent-watchdog guarantees.
Historical assembler/selection labels and source/envNone/default/ABI/provider/
FP/public A1/A2/ARM qualifications retain their exact scope in the mapping.

Only this annex and revision metadata change. All1164 prior navigation IDs,
40 old rows,16 whole requirements, R3–R12 objects/catalogs/pairs/criteria/U/
state/error/history, EPCQ01/common-custody/FDfsync/R7 preservation-read exceptions,
and released117 evaluations/129 inventory objects remain exact with full
reversal. Preservation uses current R12 plus its sole owner REPORT embedded
metadata only; old proposals/catalogs/providers/fixtures are not reopened.
The resulting1165 navigation IDs are not passes, portable criteria or a product
denominator. No activity/startup/reset/transport/FTZ/numerical/public/ARM law,
fit, calibration, new tolerance, grade, site, release or product closure follows.
Required unsupported behavior remains U/OPEN.

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
| 2 | 2026-10-19 | Stage a finite protocol-conditioned candidate with 117 retained outputs, explicit binary32 comparison vectors, frozen reference measurement windows/masks and executable numerical comparisons. Exclude three unstable-envelope settings and random-component level; no general laws, stored-value mapping or Live integration released. Parent requirement/case IDs unchanged. |
| 3 | 2026-10-21 | Directly adopt all eight independently approved finite control-seam captures under REQ-006 and 011: three distinct transpose inputs with all four stored aliases, and four pickup settings plus their separate-history baseline and two finite pair equalities. Add DEL-CS-001 to 008 and exact analysis-side fixtures. Preserve all other 14 requirement bodies, all 32 old case rows, general metrics/U and the immutable 117-evaluation release. No portable exact waveform, calibration, smoothing, public or ARM claim. |
| 4 | 2026-10-21 | Add 22 finite supplied transpose captures DEL-CS-009–030 and three inherited R3 references, completing the 25-point P1 integer catalog. Qualify REQ-002/006 without new pitch, dispatch, calibration or portable law. Preserve 14 other whole bodies, both old prefixes, 40 prior rows/IDs, eight R3 objects/two pairs and released scope; portable expected/comparator/grade NULL. |
| 5 | 2026-10-21 | Add 127 finite typed note-key observations DEL-CS-031–157 and inherited key60 DEL-CS-001/P1/ELECTRIC-AUDIO-004 aliases, completing the 128-point P1 catalog. Append only REQ-004 finite qualification; REQ-006 stays unchanged pitch context. Preserve 15 other whole bodies, old004 prefix, 40 rows/62 IDs, R3 eight objects/two pairs, R4 whole25 catalog, tolerances/U/history and117 released evaluations. Portable expected/comparator/grade NULL; no general pitch/range/onset/public/ARM/calibration law. |
| 6 | 2026-10-21 | Add 127 finite P1 note-on velocity observations DEL-CS-158–284 and inherited100 reference, completing the 128-byte catalog. Append only bounded REQ-004 qualification; REQ-006 stays unchanged. Preserve 15 other whole bodies/old004prefix, 40 rows/189 IDs, R3 eight objects/two pairs/R4 whole25/R5 whole128, oldacceptance/tolerances/U/history and 117 released evaluations. Fresh priors/portablecriteria/gradesNULL; no general velocity-zero dispatch/curve/public/ARM/calibration law. |
| 7 | 2026-10-21 | Add one combined 173-observation annex: 31 supplied host vectors DEL-CS-285–315 and 142 matching-channel/note-off-byte histories DEL-CS-316–457. Full 58-alias/56-vector and 144-alias/143-history catalogs deduplicate inherited Transpose/P1 references by complete history. Append only REQ-002/004 finite qualifications; preserve 14 other whole bodies, old prefixes, 40 rows/316 prior IDs, R3–R6 objects/catalogs, criteria/U/state/history and released 117 evaluations/129 objects. Portable expected/comparator/grade NULL; no general/public/ARM/calibration law. |
| 8 | 2026-10-21 | Add 284 finite independent On/Off key/channel observations DEL-CS-458–741; full 288-alias/285-history catalog, one inherited P1 INPUT reference/four aliases without replay or criterion transfer. Append only REQ-004; preserve 15 other whole bodies, old prefix, 40 rows/489 prior IDs, R3–R7 objects/history/criteria and released 117 evaluations/129 objects, with full reversal. NULL portable criteria/grades; no general unmatched-release/public/ARM/calibration law. |
| 9 | 2026-10-21 | Add 256 finite pickup controller observations DEL-CS-742–997; full 256 aliases/256 fresh histories, no 0.5 baseline inheritance. Annex and revision only; preserve all 16 whole requirement bodies, 773 prior IDs, 40 rows, R3–R8 objects, criteria/U/history and releases 117 evaluations/129 inventory objects, with full reversal. All waveform expectations, portable criteria and grades NULL; retain EPC-RV-Q01 budget discrepancy and common 286 initial/73,216 after-pair qualification. No general pickup, within-cell, quantizer, productivity, public/ARM or calibration law. |
| 10 | 2026-10-21 | Add 124 finite source-declared Polyphony p0–30 load/first-omission observations DEL-CS-998–1121, full 124 histories/62 same-end pairs. Annex/revision only; preserve all 16 whole requirements, 1,029 prior IDs, 40 rows, R3–R9 objects, criteria/history and releases 117 evaluations/129 inventory objects, with full reversal. All waveform expectations/portable criteria/grades NULL; no capacity, stealing, residual, public/ARM or calibration law. New FDfsync requests do not repair old NOFDfsync; all prior qualifications retained. |
| 11 | 2026-10-21 | Add seven finite declared rate/block observations DEL-CS-1122–1128/full7histories8aliases, pr_ref/rerun one fresh history/not P1 or inherited baseline. Annex/revision ONLY/all16wholeREQ/1153oldIDs40rows/R3–R10objects/criteriaU/history/releases117eval129inventory exact/fullreverse; literal queue/warm/rate order/native priorsportablecriteriaGradeNULL/appFalse/no general invariance/publicARM/calibration law. |
| 12 | 2026-10-22 | Add only four approved finite declared-protocol observations DEL-CS-1129–1132/full17 dispositions; failed activity_note and12 unattempted stay U without IDs or criteria. Annex/revision only; preserve16wholeREQ/1160oldIDs40rows/R3–R11objects/releases117eval129inventory/fullreverse. NULL waveform priors/portable criteria/grades; no reset/transport/FTZ/public/FP law or guard repair. |
| 13 | 2026-10-22 | Add only quiet finite activity_empty DEL-CS-1133/full later12 snapshot; failedstartup_0 and10unattempted remain U/no IDs or criteria. Preserve earlier17snapshot/16wholeREQ/1164oldIDs40rows/R3–R12objects/releases117eval129inventory/fullreverse; annex/revision only, NULL criteria/grades/no activity/startup/publicFP/ARM law or guard repair. |
| 14 | 2026-10-23 | Add10 finite exact startup observations DEL-CS-1134–1143 under user-adopted15 signed64 opaque returns/all other guards unchanged. Preserve16wholeREQ/1165oldIDs40rows/R3–R13objects/both17+12ASOF/failedU/releases117eval129inventory/fullreverse; no return/flag/startup/publicARM law or portable criterion. |
| 15 | 2026-10-23 | Add3 finite supplied dynamic-Polyphony histories DEL-CS-1144–1146; strictret0flag01/no15transfer/segmentation-confounded byte comparisons only. Preserve16wholeREQ/1175oldIDs40rows/R3–R14objects/both17+12ASOF/failedU/opaque10policyRLE/releases117eval129inventory/fullreverse; no soleparameter/voice/publicARM law or portable criterion. |
| 16 | 2026-10-23 | Add only two current-provided owned sine flag observations DEL-CS-1147/1148; original missing NumPy artifact/both old gapsU unchanged. Annex/revision only; preserve16wholeREQ/1178oldIDs40rows/R3-R15objects/both17+12ASOF/failedU/opaque10/R15Poly3/releases117eval129inventory/fullreverse. STRICTret0flag01/no opaque transfer; NULL waveform/portable criteria/grades/appFalse, no general input-flag/equality/publicARM law. |

The [finite handoff plan](device-electric-handoff-plan.md) records the reviewed first
release to enumerated output portions of REQ-001, 005 to 012, 014 and 015. It defines
comparison-domain vectors rather than accepting A1 or A2 as claims about Live. Three settings
with too few stable envelope windows and the random-component-level comparator are excluded.
Windows, band edges, harmonic centers, masks and full-precision reference measurements are
explicit in the candidate. The measurement code does not synthesize the device.

Independent review accepted the finite project metric for the released scope. The
broader draft formulas and checks, all unlisted values, stored-value mapping and Live
integration remain outside that candidate. Existing source captures are preserved.

Released locally 2026-10-19 as [device-electric-v1](../../handoff/device-electric-v1/README.md):
117 finite mono outputs, partial REQ-001, 005–012, 014 and 015 only.
[Review and exclusions](device-electric-handoff-plan.md#review-outcome) keep
random/unstable portions, phase/polarity and original application integration
ungraded; this is not whole-device completion.

Current release: [device-electric-v2](../../handoff/device-electric-v2/README.md),
which supersedes v1 by correcting one permission sentence. Its 117 finite
evaluations and numerical payload are unchanged; v1 remains immutable.

Revision 3's added finite control-seam facts remain an analyst draft and are
not released implementation inputs. A later neutral handoff requires ordinary
release review, with an explicitly supported comparison scope. The already
approved batch observations need no second review; added owner wording and
fixture mapping require their own bounded review. No release bytes are changed.

## Internal helper qualification — 2026-10-21

[The three whole internal helpers](../research/device-electric-dsp.md#electric-internal-initializers-adoption--2026-10-21) preserve full-width native resize, saved descriptor-base, partial cell initialization, FP and tail/nonreturn qualifications. Fixed caller windows do not establish current-child/producer identity or runtime/provider/public meaning. No callable X admission or behavioral case/grade/release/site is added; required U/product OPEN.

## R14 finite startup observations under revision15 — 2026-10-23

DEL-CS-1134–1143 add only ten native observation-only supplied startup histories
under REQ-001, from the
[sole approved summary](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/electric-startup-unlaunched10-opaque-v1-review.json)
(2,610,753B; SHA256 `c203996b433b180198b3f69ecfa6793dc4f8a7d4815db33705ba780a9c39fc95`).
The [owner mapping](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-electric-r14-startup-opaque-finite-v1/mapping.json)
retains all ten inputs, approved observations, receipt pointers, both old as-of
snapshots and the exact remaining-set INPUT binding.

- DEL-CS-1134: `startup_1024`.
- DEL-CS-1135: `startup_2048`.
- DEL-CS-1136: `startup_3072`.
- DEL-CS-1137: `startup_4096`.
- DEL-CS-1138: `startup_4224`.
- DEL-CS-1139: `startup_4352`.
- DEL-CS-1140: `startup_4400`.
- DEL-CS-1141: `startup_4480`.
- DEL-CS-1142: `startup_5000`.
- DEL-CS-1143: `startup_11264`.

These are precisely the formerly unlaunched startup1024/2048/3072/4096/4224/
4352/4400/4480/5000/11264 members. Both old failed activity_note and startup_0
remain U, unreplayed and unaccepted under their frozen strict guards. The
original17 and later12 snapshots remain exact historical as-of dispositions;
this separate ten-history approval does not rewrite their unattempted fields or
repair prior source, receipts, flags, raw fsync or guard failures. All earlier
native-launched/accepted members, rate/Polyphony/sine/baseline aliases are excluded;
no old output, PID, receipt, metric, oracle or criterion is transferred.

All33 original decimal/binary64/binary32 words, queued On/Off bytes and command
order are explicit. Only the literal startup On frame and corresponding process
end differ between these histories. Off equals that exact process end; public
Off delivery or exclusion is not established. No added warmup, reset, process,
event, MXCSR, provider, model or native construction is introduced. The unchanged
149688B model, C/TIME0/LIBM-unset/default-entry FP context and inherited source/
executed-version/receiver/provider/public qualifications remain bounded premises.

User-adopted revision15 changes ONLY this new packet's CalcA return admission:
retain every signed64 integer projection in exact RLE/order, without a zero or
0/1 domain, native ABI, success/error/benignness or flag meaning. Flag0or1 and all
other exit/stderr/trap/fault/CXX/initializer/import-binding-versus-counted-use/
input/parameter/event/frame/shape/both-channel-finite/custody/resource/timeout/
cleanup guards remain unchanged. All348 actual projections happen to be literal0
with flag1 in these ten; that descriptive fact does not narrow the opaque policy
or repair old ret1 failures. No design13 policy transfer or general flag law.

All ten approved outputs are finite, nonzero in BOTH channels and stereo-word
equal, with ten raw hashes and64 counted Linux CODE names. These are descriptive
local facts only, not a startup/onset/voice/Offdelivery/symmetry/within-cell/public/
ARM law. Every new waveform prior/native expectation/portable expected/comparator/
grade is NULL; new application predicate proof is false. No new f0, window,
metric, tolerance, fit, calibration or portable criterion is selected.

708 selected exports/348 CalcA/zero logged initializers leave nested/all-native
counts unknown.133 declared bindings(100Linux/26trap/7data) are not all loaded or
transitive dependencies; counted use is positive logger scope. Rate1 is opaque.
370 actual per-child37 before/after endpoint pairs plus two REPORT pairs match;
endpoint/parent receipts are not continuous mapping, source certification,
provider, input-register, FP-state or OSexec attestation. Raw/log/JSON file-fsync
requests do not establish directory/crash durability; outer redirects have no
explicit FDfsync. Complete fresh1GiB+128MiB floors and full remaining raw/future
capped-log/metadata/final-review-owner/headroom guards are unreserved, not quotas
or concurrent-writer/current-child-overshoot/escaped-child guarantees. Existing
20s child wall/CPU, core0/file4MiB/DEVNULL/newgroup/cleanup limits remain.

The initial mutable DATA assembler incorrectly removed final LF and failed
before scripts or native calls. Its source/failure record is retained; corrected
pre-call assembly preserves exact approved LF-terminated bytes and all ten
binding identities. This is not an original retry or historical repair. The new
owned generic file-identity check accepts legitimate zero-byte stderr while
complete runtime sizes stay exact/positive. The separate frozen Corpus10 checker
FAIL remains unchanged; no retroactive PASS or cross-family evidence repair.

Only annex and revision/date metadata change. All16 whole requirements,1,165 old
navigation IDs,40 old rows,R3–R13 objects,old Acceptance/annex/navigation/U/criteria/
tolerances/state/history and both17/12 snapshots remain exact.117 release
evaluations/129 manifest inventory entries are unchanged. Full reversal restores
R13. The resulting1,175 navigation IDs are not passes or a product denominator;
unsupported required behavior stays U and whole-Live coverage OPEN. No owner
grade, release, site, public/native contract or portable criterion is admitted.

## R15 finite declared dynamic-Polyphony observations — 2026-10-23

DEL-CS-1144–1146 add three observation-only supplied histories under REQ-001:
DEL-CS-1144 `poly_base`, DEL-CS-1145 `poly_0.0`, DEL-CS-1146 `poly_29.0`.
The [sole approved summary](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/electric-declared-dynamic-polyphony-v1-review.json)
(866,215B; SHA256 `4e5514fe01865acce985ea3229cf96754ef36017ea0ee1f57e4d47d5894cb553`)
and [owner mapping](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-electric-r15-dynamic-polyphony-finite-v1/mapping.json)
retain every exact input, approved observation, receipt and descriptive pair.
This complete three-invocation source class is distinct from the adopted124
load/omission histories. No old output/PID/receipt/metric/criterion is transferred.
Bounded INPUT intersections are not global absence, exhaustion or never-run proof.

All33 original decimal/f64/f32 words and literal command order remain. One On
at11264/key60/velocity100 queues BEFORE11264 warm frames; there is no Off. The
reference then processes20480. Each changed history instead processes8192,
writes host0=0.0 or29.0 at absolute19456, then processes12288. These exact scripts
supply both a parameter write and a different process segmentation. The two
changed full outputs are byte-equal and both differ from the reference, but the
segmentation confound prevents sole-parameter causality. No ignored-parameter,
no-effect, setter-delivery, voice-count, stealing, capacity, clear/release or
process-invariance law follows; neither comparison is a new portable criterion.

All three captures are finite, nonzero in BOTH lanes and stereo-word-equal, with
two raw hashes and64 counted Linux CODE names. Their11264-frame warm prefixes
are both-lane positive-zero words in these exact captures only, not a general
warmup/initialization/FP law. All186 logged CalcA projections are0 with flag1,
under the unchanged STRICT ret0/flag0or1 guard. User-adopted revision15 and
Tension13 opaque-return admission do NOT apply here. Those observations do not
establish native ABI, return meaning or a success/flag domain. The earlier R14
ten-startup opaque policy and its exact RLE remain unchanged in their own scope.

All new waveform priors/native expectations/portable expected/comparators/grades
remain NULL; new application predicate proof is false. No f0, metric, window,
tolerance, fit, calibration, physical/public/ARM or musical effect law is added.
The inherited8513B grammar and unchanged149688B model are metadata premises, not
source-to-compiled-version/current-receiver/provider/FP/input-register/OSexec
certification. Explicit C/TIME0/LIBM-unset/import logging/default-entryFP remains
a supplied current context, not historical ambient equivalence. No Off, reset,
MXCSR, transport, provider, model, construction or artifact generation is added.
Sine0/1 remain a separate incomplete INPUT class with unmet artifact identities;
no source/artifact follow-up or generation is selected by this annex.

Literal timed SetParameter contributes one extra selected export to each changed
history:98+99+99=296 selected exports/186 CalcA/zero logged initializers. The
older36-overhead294 projection omitted those two writes; it is not an actual
counter. Nested/all-native counts remain unknown.133 binding declarations
(100Linux/26trap/7data) and counted positive use do not prove complete provider/
global/data/transitive dependency absence. Rate's signed integer remains opaque.
90 actual per-child30 endpoint pairs plus three REPORT pairs match; endpoint
and parent receipts are not continuous mapping/provider/FP/OSexec proof. Raw/log/
JSON fsync requests do not establish directory/crash durability; outer redirects
have no explicit FDfsync. Fresh1GiB+128MiB floors and remaining-output/future-log/
metadata/final-review-owner guards are unreserved, not quotas or protections
against concurrent writers, current-child overshoot or escaped children. Existing
20s child CPU/wall/core0/FSIZE4MiB/DEVNULL/newgroup/cleanup limits remain.

The mutable DATA else99 syntax failure was corrected by one space before freeze
and before guard/native execution; source identity/error history remains. It is
not an original retry or frozen repair. First-fault/no-retry and full partial
retention remain. All16 whole requirements,1,175 old IDs,40 rows,R3–R14 objects,
old Acceptance/annex/navigation/U/criteria/tolerances/state/history, both17/12
frozen snapshots,failedactivity_note/startup0U and accepted opaque-ten policy/RLE
are exact.117 release evaluations/129 manifest inventory entries are unchanged.
Only this annex and revision metadata change; full reversal restores R14.
The resulting1,178 navigation IDs are not passes or a product denominator;
unsupported required behavior stays U and whole-Live coverage OPEN. No grade,
release, site, implementation input or general public/ARM law is admitted.

## R16 finite current-provided owned sine flag observations — 2026-10-23

DEL-CS-1147 (`sine_0`, input flag0) and DEL-CS-1148 (`sine_1`, input flag1)
are two observation-only current-provided histories under REQ-001. The
[sole approved summary](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/electric-owned-sine-input-flags-v1-review.json)
(452,066B; SHA256 `bc97e9bb524ba03c1844e1d885e47a52f35074b7f6c2d69ce009c94f41cde7f6`)
and [complete two-point mapping](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-electric-r16-owned-sine-pair-finite-v1/mapping.json)
retain exact scripts, supplied contexts, generation provenance, point digests,
receipt pointers, observations and qualifications. These are new supplied-input
observations, without historical case, PID, output, metric or criterion transfer.

Both use the same new owned33314-frame/266512-byte stereo little-endian binary32
input (SHA256 `dafee8ccf9d61104d90f4ababeb747863da0df8e7fcb0bc1858a7fcce5ec94d8`).
Its pinned owned generator declares binary64 operation order using current
math.pi,440.0,frame index and44100.0, one math.sin call, amplitude0.5, one
binary32 pack and duplicated lane bytes per frame. This records new INPUT
construction only. It does not establish original NumPy rounding/construction,
missing-original bytes, reproducibility across FP/libm/platform/interpreter
contexts or an output oracle. The original missing pr_sine artifact and BOTH
historical sine gaps remain U and unchanged. The earlier missing-file result,
old R15 incomplete/unselected statements and all prior snapshots remain exact
as-of records; this separately selected supplied route does not repair them.

All33 original decimal/binary64/binary32 words remain exact. Both On at11264,
key60/velocity100 and Off at24494,key60/velocity0 queue BEFORE11264 warm frames;
22050 render frames follow, at44100Hz/block512(last34). The full33314 output
frames include the warm phase. Input flag0 versus1 is the only supplied script
difference. No extra event/reset/transport/MXCSR command, native model, provider,
construction or driver change is introduced. Current explicit C/TIME0/LIBM-unset/
import logging/default-entryFP and unchanged149688B model remain qualified
premises, not historical ambient/current receiver/source-to-executed/provider/
FP/input-register/OSexec or public/ARM equivalence.

Both outputs are finite, nonzero in BOTH lanes and stereo-word-equal, with22006
nonzero words per lane and no negative-zero words in these exact captures.
Their complete output bytes and hashes are equal (one raw hash). This pair
comparison is descriptive ONLY: no general input-flag/no-effect/input-ignore,
waveform equality, voice, physical, ABI, public/ARM, calibration or application
law or portable criterion follows. Every fresh waveform prior/native waveform
expectation/portable expected/comparator/grade remains NULL; new application
predicate proof is false. No residual, f0, fit, metric, window or tolerance is
added or transferred from an older case or released handoff.

Both histories retain STRICT CalcA return0/flag0or1 and every other collector
guard; D08/D09/design13/15 opaque policies do NOT transfer. The132 actual CalcA
projections are all0 with flag1, without native return/flag meaning or domain
proof.204 selected exports and zero logged initializers leave nested/all-native
work unknown.133 declared bindings(100Linux/26trap/7data) and positive counted
Linux use do not establish complete provider/data/transitive dependency absence.
Rate1 remains an opaque integer. All exit/stderr/trap/fault/CXX/initializer/
binding/input/parameter/event/frame/shape/both-channel-finite/custody/resource/
timeout/cleanup guards remain. First-fault/no-retry/full partial retention stays.

All eight generation/capture/control/finalizer sources were pinned BEFORE the
one owned generation; the exact artifact, both scripts and all code were bound
again BEFORE both once-only native children. The sole peer checked the owned
generation AST/order inertly without regenerating samples, then all retained
input/output words, protocols and custody.74 actual per-child37 before/after
endpoint pairs and three REPORT pairs agree. Such endpoints and parent receipts
do not prove continuous mapping, source certification, FP/provider state or
OSexec. Successful log/JSON/raw file-fsync requests are not directory/crash
durability; outer redirects have no explicit FDfsync. Fresh1GiB+128MiB floors
PLUS268435456 concurrent allowance, and larger complete remaining raw/future
8MiB-log/1MiB-metadata-per-child/final64MiB/headroom guards, are unreserved,
non-atomic soft bounds, not quota/current-child-overshoot/escaped-child promises.
Child20s CPU/wall/core0/FSIZE4MiB/DEVNULL/newgroup/cleanup remain; parent has no
external watchdog. Original source/runtime and generation reproducibility gaps
remain explicit. There was no original missing-path retry or frozen repair.

Only this annex and revision metadata change. All16 whole requirements,1178
prior navigation IDs,40 literal rows,R3-R15 objects,old Acceptance/navigation/
U/criteria/tolerances/state/history,both17+12 as-of snapshots,failedactivity_note/
startup0U,old sine gaps,R14 opaque-ten policy/RLE and R15 strict dynamic-Polyphony
observations remain exact.117 release evaluations/129 inventory entries remain
unchanged by inherited approved metadata, without fixture or manifest reproof.
Full reversal restores R15. The resulting1180 navigation IDs are observation
navigation, not passes or a product denominator. Required unknowns keep
whole-Live coverage OPEN; no release, grade, site or implementation input follows.
