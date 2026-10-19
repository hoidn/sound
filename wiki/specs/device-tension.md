---
id: SPEC-DEVICE-TENSION
type: spec
status: draft
updated: 2026-10-18
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3 / macOS; reference renders from the Tension.bundle x86_64 slice
---

# Tension instrument: signal behavior and reference renders

## Scope

Feature FEAT-DEVICES, T1 device audio ([ADR 0004](../decisions/adr-0004-target-scope-t1.md)).
User task: a MIDI track holds the bundled Tension instrument, and the offline render of that
track's notes must sound as Live's would. This draft specifies:

- the output Tension produces for note events and a set of stored parameter values, at 44.1 kHz
  and 48 kHz;
- the reference renders that define that output for T1, and the protocol that made them;
- the comparison metric a candidate render must meet;
- a signal description of each section: excitator, string, damper, termination, pickup, Body,
  filter, output level, pitch, velocity and voices.

How the parameters are stored, with their domains and defaults, is
[SPEC-BUNDLED-DEVICE-PARAMETERS](bundled-device-parameters.md). Where the instrument sits in the
track's signal flow, and when notes reach it, belong to the playback and mix-graph specs.

Excluded:

- a signal description of the modulation sources: vibrato, LFO, filter envelope, portamento and
  unison (REQ-015 makes them render-defined only);
- the random features (KeyboardError above 0; VibratoError above 0 with vibrato on), LFO Sync, and
  the MPE inputs (channel pressure, slide, per-note pitch bend), mod wheel and sustain pedal (REQ-015, U);
- mono-mode note priority and legato (REQ-014, U);
- display text, enumeration labels, CPU load and latency reporting.

Every requirement is a **proposed contract**. Nothing was run against Live, and under
[ADR 0003](../decisions/adr-0003-no-reference-execution.md) nothing will be. The audio evidence is
extracted execution of the shipped x86_64 Tension code. The Live-side parameter path is a static
derivation. Canonical evidence: [Tension DSP](../research/device-tension-dsp.md).

## Evidence labels

| Label | Meaning |
| --- | --- |
| D | Documented in shipped bytes: the schema, the shipped presets and the bundle's export table |
| S | Static derivation from the 12.4.3 executables; not an observed run |
| S-cond | A static derivation that holds only under the named assumption |
| X | Extracted execution: the shipped x86_64 Tension slice was run on the stated calls in the harness of [ADR 0003](../decisions/adr-0003-no-reference-execution.md#extracted-execution-of-original-code). It shows what the device code computes for those calls. It does not show that Live makes the same calls. The arm64 release slice is matched only by a static count (appendix) |
| U | Unknown; no expected result, and not graded |

Only D, S and X clauses, and S-cond clauses whose assumption is accepted, may enter a release.
A U clause blocks the behavior it names. Each blocking U clause states its effect on T1.

## Assumptions

| ID | Assumption | What rests on it |
| --- | --- | --- |
| A1 | The device sees the protocol of REQ-001: the sample rate set before the parameters; all 129 host values sent; note events as 16-byte records with frames relative to the host block; transport not playing; input flag 0. Live's call order and conversions are static (S). The event frame base, the transport and flag values and Live's block partition are unknown ([Q-025](../questions.md#q-025-device-host-protocol-and-device-audio-acceptance)) | REQ-001, REQ-003, every case |
| A2 | Host blocks start at the render's first frame and are 512 frames long. The device's note timing depends on the block partition (REQ-003), and Live's partition is unknown | REQ-003 exact frames; all cases |

## Requirements

### REQ-DEVICE-TENSION-001 — reference renders define the output

- **X.** For T1, Tension's output for note events and a set of host values is the reference
  render made with this protocol:
  1. a new instance is created;
  2. the sample rate is set (44,100 or 48,000 Hz);
  3. the 129 host values of REQ-002 are sent, in index order;
  4. processing starts at the first frame, in host blocks of 512 frames, with silent input buffers
     and input flag 0;
  5. note events are delivered in the block that contains their frame, with the frame relative to
     that block's start;
  6. the transport is not playing (position 0, 120 BPM).

  The output is two channels, one frame for each processed frame. In every render both channels
  are bit-identical. The reference renders are retained as mono 32-bit float WAV with their
  scripts and SHA-256 (cases below). For a parameter set without a case, the reference is a new
  render made with this protocol.
- **X.** With constant parameters the output does not depend on:
  - the host block size, 64, 256 or 512 frames, except through event placement (REQ-003);
  - flush-to-zero and denormals-are-zero;
  - the clock value from which the device seeds its random generator, except for the settings
    of REQ-015.

  Re-running a case gives a bit-identical render.
- **S, X.** Live creates the instance, sets the current rate and sends the parameter values
  ([N5](../research/device-parameter-mapping-native.md#how-live-loads-a-bundle)). It may run a
  reset sequence: 1,024 frames of processing, a device reset, then index 0 again. Before a note,
  that sequence leaves the output bit-identical, with or without the index-0 resend (X).
  Setting 44.1 kHz and then 48 kHz differs from 48 kHz directly by at most 1.8 × 10⁻⁷ (rel RMS
  4.4 × 10⁻⁷), inside the metric.
- **D, U.** Which values a newly inserted Tension starts with is U
  ([REQ-BUNDLED-DEVICE-PARAMETERS-009](bundled-device-parameters.md#req-bundled-device-parameters-009--values-of-a-newly-inserted-device)).
  DTN-001 renders the constructor defaults and DTN-003 the shipped Defaults preset. A Live Set
  stores every value, so T1 sets do not depend on it.
- **U.** When Live runs the reset sequence, its block partition, the event frame base, and the
  transport and flag values it passes. Effect on T1: none for the audio of a held parameter set.
  Note timing depends on the block partition (REQ-003, A2).

### REQ-DEVICE-TENSION-002 — from stored values to host values

- **S** ([N6](../research/device-tables-native.md#tension-stringstudio-130-entries-0129-25-second-outputs-1-unused)).
  Live sends indices 0 to 129 except 2, in the N6 order. Each stored value is first clamped to its
  domain (SPEC-BUNDLED-DEVICE-PARAMETERS). Then:
  - **Polyphony** v: max(v − 1, 0) on index 0, and 1 on index 7 if v > 0.5, else 0;
  - **PitchBendRange** v / 12;
  - **Octave** v + 3; **Transpose** v + 12;
  - **KeyboardUnison**, **LFOSync** and **BodyType**: v + 1 when their toggle
    (KeyboardUnisonToggle, LFOSyncToggle, BodyToggle) is on, else 0;
  - **PortamentoProportional**: 1 when off, 0 when on;
  - **FilterType** t: ⌊t/2⌋ on index 91 and t mod 2 on index 92;
  - the **23 bipolar amounts** (`*KbdMod`, `*VelMod`, `*LFOMod`, `*EnvMod`, and the Geo modulations):
    |v| on their index and 1 on the next index if v < 0, else 0;
  - **integer-stepped Floats** (PitchBendRange, Octave, Transpose, LFOSync): rounded to the
    nearest 1/32768, then truncated toward zero, before the steps above;
  - **all others** pass unchanged, including index 121 (48, not stored) and the pressure and slide
    targets and ranges.

  N6's value for each default is reproduced for all 101 indices that state one (X harness check).
- **X.** For the 0..1 host values of most controls, the device forms c = 128v for v ≤ 0.5 and
  126v + 1 above. Then:
  - **Stepped:** these use ⌊c⌋, so each has 128 steps. Two values in one step render
    bit-identically:
    - ExcitatorParameterX, ExcitatorStiffness, ExcitatorVelocity and ExcitatorDamping, with
      their key and velocity amounts;
    - DamperMass, DamperStiffness and DamperDamping, with their key amounts;
    - StringDamping, StringDecay, StringDecayRatio and StringInharmonicity, with their key
      amounts;
    - TerminationFingerStiffness, TerminationFingerForce (with its amounts) and
      TerminationFretStiffness;
    - BodyDecay, BodyHighCut, BodyLowCut and BodyMix.

    The steps begin exactly at k/128 below 0.5, and within one binary32 ulp of (k − 1)/126 above.
  - **Continuous:** KeyboardFineTune, KeyboardStretch, KeyboardError, VibratoDelay,
    PortamentoTime, FilterCutoffFrequency and FilterQFactor (with their key and envelope amounts)
    and BodyLevel use c unrounded.
- **X.** GeoExcitatorPosition, GeoDamperPosition and PickupPosition select one of a set of
  discrete points, which narrow toward 1. The number of points depends on the note: over the 129
  host values k/128 there are 34, 36 and 35 distinct renders at note 60, and 95, 87 and 98 at
  note 36. Two values that select the same point render bit-identically.
- **U.** Which controls the remaining host values feed, other than as REQ-004 to 015 state.

### REQ-DEVICE-TENSION-003 — note events and timing

- **X.** The device acts on note events on a control grid of P = ⌊fs/1000⌋ frames: 44 at
  44.1 kHz and 48 at 48 kHz, counted from the first processed frame. An event at frame f takes
  effect at the start g of the grid period that contains f. If g lies in an earlier host block
  than f, the event takes effect at g + P instead. An event renders bit-identically to the same
  event placed at its effective frame. Tested on 560 note-ons (44.1 kHz blocks of 512, 64 and
  333; 48 kHz) and 500 note-offs.
- **X.** From the effective frame of a note-on, the first non-zero output frame follows after a
  fixed delay:

  | ExcitatorType | Velocity 1 | 64 | 100 | 127 |
  | --- | --- | --- | --- | --- |
  | 0 | 13 | 13 | — | 14 |
  | 1 and 2 | 17 | 17 | — | 18 |
  | 3 (default), 44.1 kHz | 32 | 32 | 33 | 33 |
  | 3, 48 kHz | — | — | 36 | — |

  The pickup adds 37 frames (case DTN-021).
- **X.** From the effective frame of a note-off, the first output frame that differs from the
  held note follows after 78 frames for types 3 and 1, 14 for type 0, 66 with the damper on and
  gated, and 85 for type 3 at 48 kHz.
- **X.** A note-on with velocity 0 acts as a note-off. Without events the output is exactly zero.
  With ExcitatorToggle off, a note gives exactly zero output.
- **S-cond (A2).** Exact frames hold for host blocks of 512 from the render start. Effect on T1:
  with another block partition an event can move by one grid period (1 ms). T1's sample-exact
  note timing for Tension therefore needs the block partition fixed, by Live's (unknown) or by a
  render convention.

### REQ-DEVICE-TENSION-004 — pitch

- **X.** A note's first partial lies within 0.05 cent below 440·2^((n − 69)/12) Hz for notes 24
  to 72 at 44.1 kHz; C4 at 48 kHz is also 0.04 cent below. It is 0.12 cent below at note 84 and
  0.64 cent below at note 96. At note 108 no partial was resolved.
- **X.** Octave and Transpose shift the note in semitones. Whole octaves give the shifted note's
  frequency exactly. Other shifts are slightly sharp, as the 2ˣ approximation A of
  [SPEC-DEVICE-CORPUS REQ-006](device-corpus.md#req-device-corpus-006--pitch) predicts. For
  example, Transpose +7 is +1.15 cents sharp of equal temperament (A: +1.15).
- **X.** Pitch bend (status 0xE0) shifts by (value − 8,192)/8,192 × PitchBendRange semitones
  through the same approximation. At range 2, values 0, 4,096, 12,288 and 16,383 measure +1.17,
  +0.75, +0.02 and +0.09 cents from the exact shift (A: +1.17, +0.74, +0.01, +0.07). Value 16,383
  at range 12 measures +0.14 cents.
- **X.** KeyboardFineTune 0, 0.25, 0.75 and 1 shift by −49.58, −24.59, +25.20 and +50.00 cents.
- **X.** KeyboardStretch detunes in proportion to the distance from note 69:

  | Stretch | C2 | C4 | C6 |
  | --- | --- | --- | --- |
  | 0 | +26.40 | +7.20 | −11.89 |
  | 0.25 | +13.10 | +3.57 | −5.90 |
  | 0.5 (default) | 0 | 0 | 0 |
  | 1 | −26.17 | −7.13 | +12.00 |

  Values are cents relative to the same note at the default.

### REQ-DEVICE-TENSION-005 — string partials

- **X.** After the excitation ends, a note at constant parameters rings as a sum of exponentially
  decaying partials. Partial k lies near k·f₁·√((1 + Bk²)/(1 + B)). Each partial's frequency,
  decay rate and complex amplitude are measured with the estimator of the
  [Corpus metric](device-corpus.md#comparison-metric), applied per partial.
- **X.** Defaults, C4, 44.1 kHz (case DTN-001), held part:

  | k | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
  | --- | --- | --- | --- | --- | --- | --- | --- | --- |
  | Hz | 261.620 | 524.522 | 789.533 | 1056.900 | 1326.471 | 1597.919 | 1870.893 | 2134.901 |
  | T60, s | 5.552 | 3.642 | 2.301 | 1.510 | 1.044 | 0.757 | 0.571 | 0.448 |
  | Level, dB | 0 | −2.6 | −8.6 | −22.3 | −18.6 | −15.0 | −16.5 | −22.2 |

  At 48 kHz the upper partials differ (k = 2: 524.251 Hz), so a 48 kHz render is not a resampled
  44.1 kHz render.
- **X.** By note: at C2, B is 3.8 × 10⁻⁴ and T60 falls from 5.81 s (k = 1) to 4.49 s (k = 8). At
  C5, B is 1.9 × 10⁻³ and T60 is 2.83, 1.00 and 0.48 s for k = 1 to 3. At C6 the first partial's
  T60 is 0.62 s.
- **X.** StringDecay sets the overall decay. The first partial's T60 is 0.216, 1.194, 5.552 and
  17.56 s at 0.25, 0.5, 0.75 and 1.
- **X.** StringDamping sets how much faster the upper partials decay. At 1, k = 1 to 8 decay with
  T60 6.7 to 6.3 s. At 0 only a 258.5 Hz component with T60 0.05 s remains.
- **X.** StringInharmonicity sets B at C4: 5 × 10⁻⁶ at 0 (k = 2 at 523.244 Hz), 8.4 × 10⁻⁴ at 0.5,
  and 3.7 × 10⁻³ at 1 (k = 2 at 530.355 Hz). The first partial stays at 261.620 Hz.
- **X.** StringDecayRatio sets the decay after the note-off:

  | Ratio | 0 | 0.25 | 0.5 | 0.75 | 1 |
  | --- | --- | --- | --- | --- | --- |
  | Release T60, first partial | 32.98 s | 1.134 s | 0.205 s | 0.091 s | stops within 50 ms |

  The partial frequencies do not change at the note-off.
- **X.** The key amounts act relative to note 60. At note 60, StringDecayKbdMod ±1 and
  StringDampingKbdMod 1 render bit-identically to no amount; at notes 36 and 84 they change the
  decay.
- **X.** After the release the output becomes exactly zero, once the voice has fallen to about
  10⁻⁶ (largest magnitude in the last 10 ms of `defaults_44`: 6.0 × 10⁻⁷). Under the
  perturbations of the metric, the last non-zero frame moved by 0 or 44 frames. The voice-end
  rule is U and is graded only through the waveform comparator.

### REQ-DEVICE-TENSION-006 — excitators

- **X.** ExcitatorType selects how a note excites the string. Labels are U
  ([REQ-BUNDLED-DEVICE-PARAMETERS-014](bundled-device-parameters.md#req-bundled-device-parameters-014--enumeration-labels)).
  - **0, sustained excitation.** At C4 with the defaults the tone sustains while the key is held:
    held RMS 0.349, peak 1.47. Its strongest component is near 1,061 Hz, with weaker ones near
    272, 545 and 794 Hz; they do not form a harmonic series of 261.6 Hz. After the note-off the
    string decays as in REQ-005. The output is chaotic: per-operation rounding changes
    decorrelate it within 2,048 frames (metric).
  - **1, single strike.** Free decay; at C4 peak 0.683, partials 2 to 7 at −19 to −32 dB.
  - **2, repeated strike.** Peak 0.693; the first held partial at 275.7 Hz with T60 0.35 s; the
    voice ends earlier (last non-zero frame 38,675). Moderately sensitive (metric).
  - **3, the default.** REQ-005's table.
- **X.** ExcitatorToggle off silences the note (REQ-003).
- **X.** The excitator controls change the level and partial balance, not the partial
  frequencies or decays. Cases DTN-011 to 013:

  | Setting | Peak | Held RMS | Partial levels k = 1..4, dB |
  | --- | --- | --- | --- |
  | Defaults (type 3; X 0.75, Stiffness 0.5, Velocity 0.5, Damping 0.5) | 0.381 | 0.0951 | 0, −2.6, −8.6, −22.3 |
  | Type 3, ExcitatorParameterX 0 / 1 | 0.064 / 0.858 | 0.0082 / 0.218 | −2.7, 0, −3.0, −16.0 / 0, −2.7, −8.2, −22.1 |
  | Type 3, ExcitatorStiffness 0 | 0.0077 | 0.0022 | 0, −2.9, −8.7, −23.1 |
  | Type 3, ExcitatorDamping 0 | 0.186 | 0.052 | 0, −3.1, −9.1, −23.1 |
  | Type 1, ExcitatorParameterX 1 | 1.125 | 0.053 | 0, −10.5, −14.6, −15.3 |
  | Type 1, ExcitatorStiffness 1 | 0.789 | 0.181 | 0, −14.2, −10.8, −14.8 |
  | Type 1, ExcitatorDamping 1 | 0.969 | 0.315 | 0, −17.4, −17.0, −26.1 |
  | Type 0, ExcitatorParameterX 1 | 3.43 | 0.485 | chaotic |

- **X.** At the ends of their ranges some settings leave the string's normal range:
  - type 1 at ExcitatorVelocity 1 peaks at 3.9999, and type 3 at ExcitatorDamping 1 at 3.998;
  - type 1 at ExcitatorVelocity 0, and type 0 at ExcitatorParameterX 0.25 or ExcitatorVelocity 1,
    give exactly zero output.

  The candidate must reproduce these renders like any other.
- **X.** GeoExcitatorPosition shapes the partial levels like a strike point along the string. At 1
  the even partials are 23 to 28 dB down (the middle); at 0 the levels fall smoothly (k = 2 to 6
  at −0.8 to −11.3 dB); at 0.5 partial 4 is weakest.
- **U.** GeoExcitatorAbsolute and the Geo key and velocity amounts were not rendered. Effect on
  T1: graded only by on-demand renders under REQ-001.

### REQ-DEVICE-TENSION-007 — velocity

- **X.** With all velocity amounts at 0, velocity changes the level a little. Peak 0.3626, 0.3812
  and 0.3856 at velocities 1, 100 and 127.
- **X.** ExcitatorVelocityVelMod raises the excitation with velocity, from no change at velocity 1:
  a velocity-1 note renders bit-identically to the same note without the amount. At 0.5 the held
  RMS is 0.0914, 0.1254 and 0.1785 at velocities 1, 64 and 127. At 1, velocities 32 and 64 peak at
  3.11 and 3.84, and 100 and 127 give exactly zero output.
- **U.** The other velocity amounts were not rendered (on-demand renders only).

### REQ-DEVICE-TENSION-008 — damper

- **X.** DamperToggle on, not gated, damps the string while it is held. At C4 the held RMS is
  0.0056, against 0.0951 without the damper. Partials 6 to 8 remain, and partials 1 and 2 of the
  release are raised to 285.7 and 568.8 Hz.
- **X.** DamperGated on leaves the held part's partials as without the damper. At the note-off it
  produces a transient (peak 1.016, against the note's 0.381) and a fast release: partials at
  284.5, 569.9, 850.9 and 1,117.3 Hz with T60 0.078 to 0.050 s.
- **X.** GeoDamperPosition 0 (not gated) leaves partials from 263.35 Hz with T60 0.62 to 0.29 s.
  DamperVelocity has no effect when the damper is not gated. DamperMass 0 makes the output chaotic.

### REQ-DEVICE-TENSION-009 — termination

- **X.** TerminationToggle on lowers the pitch and shortens the decay. At C4 the first partial is
  259.810 Hz (−12.0 cents) with T60 4.78 s. With TerminationFingerForce 0 it is 245.224 Hz
  (−112 cents) with T60 1.82 s.

### REQ-DEVICE-TENSION-010 — pickup

- **X.** PickupToggle on changes the partial balance and level, not the frequencies or decays. At
  position 0.5: held RMS 0.1187, partial 2 strongest, partial 6 at −25.5 dB. At position 0: held
  RMS 0.0341, partials 6 and 7 at −3.3 and −3.6 dB. The first output frame is 37 frames later
  (REQ-003).

### REQ-DEVICE-TENSION-011 — Body

- **X.** The Body is off unless BodyToggle is on (index 114 is then BodyType + 1). Body on with
  BodyMix 0 renders bit-identically to Body off. The output stays mono. The Body leaves partial
  frequencies and held decays unchanged, except at BodyDecay 1. It colours the spectrum. The table
  gives third-octave levels over the held part of C4, Body minus Body off, at BodySize 2 unless
  stated:

  | Setting | 250 Hz | 500 | 1 k | 2 k | 4 k | Held RMS |
  | --- | --- | --- | --- | --- | --- | --- |
  | BodyType 0 | −4.4 | −1.6 | −2.1 | −1.6 | −3.4 | −3.3 dB |
  | BodyType 1 | −7.3 | −4.7 | −7.7 | −2.4 | −2.6 | −5.5 dB |
  | BodyType 2 | −7.8 | +1.8 | −7.3 | −8.5 | +5.6 | −2.2 dB |
  | BodyType 3 | −2.5 | −2.6 | −1.8 | −3.1 | −1.9 | −2.5 dB |
  | Type 0, BodySize 0 | −10.2 | −0.8 | −1.1 | −2.3 | −2.0 | −4.6 dB |
  | Type 0, BodySize 4 | −3.0 | −3.3 | −3.0 | −2.7 | −3.4 | −3.1 dB |
  | Type 0, BodyMix 1 | −16.7 | −13.5 | −8.9 | −9.2 | −13.4 | −15.4 dB |

- **X.** BodyDecay 1 adds a long Body ring: the release T60 of the first partial becomes 0.63 s,
  against 0.21 s.
- **U.** BodyLowCut and BodyHighCut, other than being stepped (REQ-002), and a closed-form Body
  response. Effect on T1: Body settings are graded only against renders (on demand for unrendered
  values).

### REQ-DEVICE-TENSION-012 — filter

- **X.** FilterToggle on inserts a filter that acts as a linear, time-invariant filter on the
  string's output. Changing the excitation by −8 and −22 dB changed the measured response by at
  most 0.092 dB and 0.0065 rad. The partial decays pass unchanged. Off (the constructor default)
  the output is unfiltered. The Defaults preset turns it on at type 1 and cutoff 1, where the
  response is within 3 dB to 20.1 kHz.
- **X.** Response at FilterCutoffFrequency 0.5 and FilterQFactor 0, as a ratio to the unfiltered
  output at harmonic frequencies:

  | Stored type | 65 Hz | 262 Hz | 1,047 Hz | 4,186 Hz | 12 kHz | Shape |
  | --- | --- | --- | --- | --- | --- | --- |
  | 0 | −2.0 | −10.3 | −22.0 | −35.2 | −52.4 dB | Low-pass, −3 dB at 81 Hz, about −6 dB per octave |
  | 1 | −0.4 | −5.1 | −24.1 | −59.4 | −102.9 dB | Low-pass, −3 dB at 187 Hz, −26 dB per octave at 4 to 8 kHz |
  | 2 | −24.2 | −20.4 | −20.0 | −21.0 | −26.7 dB | Band-pass, −20.0 dB at 851 Hz |
  | 3 | −48.3 | −40.7 | −40.0 | −41.9 | −53.4 dB | Band-pass, −40.0 dB at 851 Hz |
  | 4 | −2.1 | −11.2 | −26.8 | −7.0 | −1.0 dB | Notch, −48.1 dB at 851 Hz |
  | 5 | −4.2 | −22.3 | −53.5 | −14.1 | −2.1 dB | Notch, −96.2 dB at 851 Hz |
  | 6 | −46.3 | −30.4 | −18.0 | −6.7 | −1.0 dB | High-pass |
  | 7 | −88.9 | −45.4 | −16.2 | −2.3 | −0.2 dB | High-pass, steeper |
  | 8 | −10.8 | +22.0 | −9.3 | −18.8 | −33.9 dB | Peak +22.0 dB at 261 Hz |
  | 9 | −14.4 | +19.8 | −12.8 | −22.3 | −37.4 dB | Peak +19.8 dB at 261 Hz |

- **X.** Cutoff and resonance, type 1. The resonance peak frequency at FilterQFactor 1 grows by a
  factor of 2.16 to 2.28 per 0.125 of cutoff:

  | Cutoff | 0.375 | 0.5 | 0.625 | 0.75 | 0.875 | 1 |
  | --- | --- | --- | --- | --- | --- | --- |
  | −3 dB point at Q 0 | 77.7 Hz | 187.2 Hz | 428.8 Hz | 998.5 Hz | 2,600.8 Hz | 20,117 Hz |
  | Peak at Q 1 | 393 Hz, +28.4 dB | 851 Hz, +39.8 dB | 1,896 Hz, +41.4 dB | 4,250 Hz, +41.5 dB | 9,681 Hz, +41.6 dB | none below 20.9 kHz |

  Peaks are read at the nearest harmonic of 65.4 Hz. At cutoff 0.5 the peak is +0.23, +11.6, +25.7
  and +39.8 dB for Q 0.25, 0.5, 0.75 and 1.
- **U.** The filter's key, LFO and envelope amounts and the filter envelope (REQ-015), and a
  closed-form description of the types. Effect on T1: graded only against renders.

### REQ-DEVICE-TENSION-013 — output level

- **X.** BodyLevel (Volume) scales the whole output by g(v)/g(0.705), with g(v) = n², n = c/127,
  c = 128v for v ≤ 0.5 and 126v + 1 above, and n = 0.5 at c = 64. Ten values from 0 to 1 agree
  within 2.6 × 10⁻⁷. At 1 the factor is 1.99878 (+6.0 dB); at 0 the output is exactly zero. The
  level of the default note itself is REQ-005's render.

### REQ-DEVICE-TENSION-014 — voices

- **X.** Stored Polyphony 0 to 9 gives 1, 2, 4, 8, 12, 16, 20, 24, 28 and 32 voices. When more notes
  of different pitch sound than there are voices, the oldest is silenced. In mono, the stolen
  voice's output changes from the new note's effective frame. A repeated note-on of a pitch that
  is still sounding does not take another voice: with four voices, a C1 survives eight repeats of
  C5.
- **U.** Mono-mode priority (KeyboardPriority) and legato, the shape of a stolen voice's fade,
  KeyboardUnison and its detune and delay. Effect on T1: sets that rely on them are graded only
  against on-demand renders; stealing in polyphonic chords is graded by renders made under REQ-001.

### REQ-DEVICE-TENSION-015 — modulation sources and other inputs

- **X.** With VibratoError 0, Vibrato on is seed-independent. So are all five LFO shapes on the
  filter, and Unison on. They are deterministic and render-defined: a case is graded against a
  render made under REQ-001, without a signal description in this revision.
- **X, U.** KeyboardError above 0, and VibratoError above 0 with vibrato on, make the output depend
  on the clock seed. KeyboardError 1 detuned C4 by +11.3 cents at seed 0. Inferred: in Live the
  result differs between instances and sessions. Effect on T1: such sets are graded only as
  non-silent, bounded output.
- **U.** LFO Sync (tempo-synced rate), the filter envelope and portamento timing, and the MPE and
  controller inputs: channel pressure, slide, per-note pitch bend, mod wheel and sustain pedal.
  None was driven. Effect on T1: none for sets that only play notes; anything beyond notes is not
  verifiable.

## Timing and state

- **Units.** Frames at the stated rate; pitch in cents; levels in dB relative to the stated
  reference.
- **Latency.** None reported. The first audible frame follows the note's effective frame by
  REQ-003's excitator delay.
- **Persistent state.** None beyond the stored parameters. Ringing voices live only in a running
  instance.
- **Determinism.** Deterministic for a given parameter set, event list and block partition, except
  REQ-015's seed-dependent settings.

## Comparison metric

Proposed, pending acceptance as the T1 device-audio criterion of ADR 0004. Each case names its
class. A new parameter set takes its class from the perturbation spread of its own reference
render (method below): stable if the spread is at most a quarter of the stable tolerances, else
chaotic.

| Class | Comparator | Tolerance |
| --- | --- | --- |
| All | First non-zero frame | Exact |
| All | Exact silence where the case expects all-zero output | Exact |
| Stable | Waveform rel RMS from the first non-zero frame to the note-off frame | 3 × 10⁻³ |
| Stable | Waveform rel RMS from the note-off frame to the end | 10⁻² |
| Stable | Partials of the held part with level at least −60 dB re the strongest, measured in candidate and reference with the same estimator (appendix) | Frequency within 2 × 10⁻⁶ relative; per-frame log radius within 6 × 10⁻⁴ relative; complex amplitude within 5 × 10⁻⁴ of the strongest partial's |
| Repeated strike (type 2) | Waveform rel RMS from the first non-zero frame to the end | 5 × 10⁻³ |
| Chaotic (type 0; DamperMass 0) | Held-part RMS level | Within 3 dB |
| Chaotic | Peak magnitude | At most 4.0; non-zero while held |

Why these tolerances. The reference was re-rendered five ways: every inexact libm result one ulp
up, then one ulp down; and every SSE operation of the bundle rounded toward −∞, +∞ and zero. The
directed rounding stands in for the arm64 slice's 822 fused multiply-adds, which the x86_64 slice
does not have. Over 26 stable cases the worst differences were:

| Measure | Worst |
| --- | --- |
| Held part, rel RMS | 6.0 × 10⁻⁴ |
| After note-off, rel RMS | 2.3 × 10⁻³ |
| Partial frequency | 4.7 × 10⁻⁷ |
| Log radius | 1.4 × 10⁻⁴ |
| Complex amplitude | 1.1 × 10⁻⁴ |

The stable tolerances leave a margin of 4 to 5 over these. The repeated strike moved by
1.1 × 10⁻³. Type 0 and DamperMass 0 decorrelated completely (rel RMS up to 1.5), while their held
RMS level moved by at most 1.0 dB and their onset frame not at all. Unlike Corpus, the stable
Tension renders do not drift in phase over the render, so a waveform comparator can be used.

## Acceptance cases

Expectations are X renders of the original x86_64 code under REQ-001's protocol. None has been
run against Live, and under ADR 0003 none will be. Kinds: P positive, B boundary, T timing,
U not graded.

### Fixtures

Retained renders are 44,100 frames (48,000 at 48 kHz), mono 32-bit float WAV, from
[t12-tension-v1](../../analysis/ableton-live-12.4.3/r2/t12-tension-v1/manifest.json)
`raw/<render>.wav`. Each one's `.script` gives the exact calls. Unless stated, a case:

- starts from the constructor defaults (the "Default when absent" column of
  SPEC-BUNDLED-DEVICE-PARAMETERS) and changes only the stated stored values;
- plays C4 (note 60) at velocity 100, on at frame 4,096 and off at frame 26,146 (28,096 at 48 kHz);
- is graded as stable.

"Bright C2" means ExcitatorType 1, ExcitatorStiffness 1, StringDamping 1, StringDecay 1,
StringInharmonicity 0, note 36.

### Render cases

| Case ID | Requirement | Kind | Setup | Expected result / comparator | Reference render (WAV SHA-256) |
| --- | --- | --- | --- | --- | --- |
| DTN-001 | 001, 005 | P | Defaults, 44.1 kHz | Stable metric; partials as REQ-005's table | `defaults_44` (`75e5447da8309f70…`) |
| DTN-002 | 001, 005 | P | Defaults, 48 kHz | Stable metric | `defaults_48` (`870152dd916c94f7…`) |
| DTN-003 | 001 | P | The Defaults preset `Defaults/Instruments/Tension.adv` | Stable metric; first partial T60 17.6 s | `preset_defaults` (`cebfd43714ded5b9…`) |
| DTN-004 | 004, 005 | P | Notes 36, 48, 72, 84 | Stable metric; first partials 65.405, 130.810, 523.237, 1046.432 Hz | `note_36` (`742ee3e8…`), `note_48` (`ee7ce843…`), `note_72` (`3a7a41a3…`), `note_84` (`56642556…`) |
| DTN-005 | 007 | P | Velocity 1 and 127 | Stable metric; peaks 0.3626, 0.3856 | `vel_1` (`a15cdc11…`), `vel_127` (`5afe4e03…`) |
| DTN-006 | 007 | P | ExcitatorVelocityVelMod 0.5; velocity 1, 64, 127 | Stable metric; velocity 1 identical to `vel_1` | `velmod_1` (`a15cdc11…`), `velmod_64` (`f4d16cef…`), `velmod_127` (`ce6e7c07…`) |
| DTN-007 | 006 | P | ExcitatorType 1 | Stable metric | `exc_hammer` (`d02582f851d9e08a…`) |
| DTN-008 | 006 | P | ExcitatorType 2 | Repeated-strike metric | `exc_bounce` (`e38b402aa0707eb0…`) |
| DTN-009 | 006 | P | ExcitatorType 0 | Chaotic metric: held RMS 0.349 within 3 dB | `exc_bow` (`43c10cb0882b188c…`) |
| DTN-010 | 006 | P | ExcitatorType 0, ExcitatorParameterX 1 | Chaotic metric: held RMS 0.485 | `bow_x1` (`1e26138a13d875fe…`) |
| DTN-011 | 006 | P, B | ExcitatorParameterX 0 and 1; ExcitatorStiffness 0; ExcitatorDamping 0 | Stable metric | `plk_x0` (`989a8675…`), `plk_x1` (`99657b6a…`), `plk_stiff0` (`ff63558b…`), `plk_damp0` (`9dbdaaa0…`) |
| DTN-012 | 006 | P | ExcitatorType 1 with ExcitatorParameterX 1, ExcitatorStiffness 1 or ExcitatorDamping 1 | Stable metric | `ham_x1` (`1027234b…`), `ham_stiff1` (`6d770dfc…`), `ham_damp1` (`ef896eff…`) |
| DTN-013 | 006 | P, B | GeoExcitatorPosition 0 and 1 | Stable metric; at 1 even partials 23 to 28 dB down | `pos_0` (`bbe0ff86…`), `pos_1` (`c5024fb1…`) |
| DTN-014 | 005 | P, B | StringDecay 0.25 and 1; StringDamping 0 and 1 | Stable metric; first-partial T60 0.216 and 17.56 s | `str_decay_0.25` (`9203fabe…`), `str_decay_1` (`a942483c…`), `str_damp_0` (`f26bb5d2…`), `str_damp_1` (`df4490d6…`) |
| DTN-015 | 005 | P, B | StringDecayRatio 0 and 1 | Stable metric; release T60 33.0 s; ratio 1 last non-zero frame 30,562 (within 44) | `str_ratio_0` (`1d3604cd…`), `str_ratio_1` (`f3cba201…`) |
| DTN-016 | 005 | P, B | StringInharmonicity 0 and 1 | Stable metric; k = 2 at 523.244 and 530.355 Hz | `str_inharm_0` (`b595413c…`), `str_inharm_1` (`8346553e…`) |
| DTN-017 | 008 | P | DamperToggle on; also with DamperGated on; also with GeoDamperPosition 0 | Stable metric | `damper_on` (`8e294dc4…`), `damper_gated` (`ff6b0168…`), `damper_pos_0` (`b2f4524d…`) |
| DTN-018 | 008 | P | DamperToggle on, DamperMass 0 | Chaotic metric: held RMS 0.0771 | `damper_mass_0` (`0289eee4bc18cfaf…`) |
| DTN-019 | 009 | P | TerminationToggle on; also with TerminationFingerForce 0 | Stable metric; first partial 259.810 and 245.224 Hz | `term_on` (`46482e3a…`), `term_force_0` (`1e24a3ee…`) |
| DTN-020 | 010 | P | PickupToggle on; also with PickupPosition 0 | Stable metric | `pickup_on` (`452ac841…`), `pickup_pos_0` (`d47162d7…`) |
| DTN-021 | 003, 010 | T | DTN-020 at position 0.5 | First non-zero frame 4,206 (37 after the defaults' 4,169) | `pickup_on` |
| DTN-022 | 011 | P | BodyToggle on, BodyType 0 to 3 | Stable metric | `body_type_0` (`e8ce986e…`), `body_type_1` (`4279c00d…`), `body_type_2` (`4b627010…`), `body_type_3` (`c6a5735a…`) |
| DTN-023 | 011 | P, B | Body on, type 0: BodySize 0 and 4; BodyDecay 1; BodyMix 1 | Stable metric | `body_size_0` (`0701537a…`), `body_size_4` (`132c77a3…`), `body_decay_1` (`61a32f01…`), `body_mix_1` (`77191fdb…`) |
| DTN-024 | 012 | P | Bright C2, filter off; and FilterToggle on with FilterType 0 to 9 | Stable metric | `filt_base` (`35d6f840…`), `filt_t0` … `filt_t9` (manifest) |
| DTN-025 | 012 | P, B | Bright C2, FilterType 1: cutoff 0.25 and 0.75; FilterQFactor 0.5 and 1 | Stable metric; Q 1 peak +39.8 dB near 851 Hz | `filt_t1_c0.25` (`551a03e9…`), `filt_t1_c0.75` (`7af25788…`), `filt_t1_q0.5` (`6600fe3e…`), `filt_t1_q1` (`5dc4b0d5…`) |
| DTN-026 | 001 | P | Shipped presets Steel Basic Guitar, Clav Clicky, Nice Harp (`Core Library/Devices/Instruments/Tension/…`) | Stable metric | `preset_steel_guitar` (`9be7c825…`), `preset_clav_clicky` (`6b9f80e4…`), `preset_nice_harp` (`7ef901ce…`) |
| DTN-027 | 001, 006 | P | Shipped preset Cello Strings | Chaotic metric: held RMS 0.1291 | `preset_cello` (`f13a88d6835c1872…`) |

### Check cases

These are graded by exact frames or values from `results/checks.json`; their renders are not
retained and are regenerated by the run.

| Case ID | Requirement | Kind | Setup | Expected result |
| --- | --- | --- | --- | --- |
| DTN-028 | 003 | T | One note-on at frames 1,000 to 1,198 (step 2) and 3,060 to 3,099, blocks 512, 64, 333; also 48 kHz | First non-zero frame = effective frame (grid rule) + 33 (44.1 kHz) or + 36 (48 kHz); identical to the event placed at its effective frame |
| DTN-029 | 003 | T | Note at 1,024, note-off at 4,000 to 4,198 (step 2); types 3, 1, 0; damper gated; 48 kHz | First changed frame = effective frame + 78, 78, 14, 66, 85 |
| DTN-030 | 003 | P | Note-on velocity 0 instead of note-off | Bit-identical to the note-off render |
| DTN-031 | 003, 006, 007 | B | No events; ExcitatorToggle off; ExcitatorVelocityVelMod 1 at velocity 127; ExcitatorType 1 at ExcitatorVelocity 0 | Output exactly zero |
| DTN-032 | 004 | P | Notes 24 to 96 by octaves; Octave ±1, ±3; Transpose +7, −12; FineTune 0, 0.25, 0.75, 1; Stretch 0, 0.25, 1 at notes 36, 60, 84; pitch bend 0, 4,096, 12,288, 16,383 at range 2 and 16,383 at range 12 | First-partial frequencies of REQ-004 within 0.02 cent |
| DTN-033 | 013 | P | BodyLevel 0, 1/128, 0.1, 0.25, 0.5, 0.6, 0.75, 0.9, 1 | Output = defaults × REQ-013's factor within 10⁻⁶ relative; 0 gives exact zero |
| DTN-034 | 014 | P | C1, then 0 to 33 notes of other pitches 441 frames apart, Polyphony 0 to 9 (StringDecay 1, StringDecayRatio 0) | C1 silenced when the number of later notes equals the voice count of REQ-014 |
| DTN-035 | 014 | P | Polyphony 2: C1, then 3, 4 or 8 repeats of C5 | C1 level at least 0.99 of C1 alone |
| DTN-036 | 001 | P | DTN-001 in blocks of 64 and 256; with flush-to-zero and denormals-are-zero; with clock values 1,760,000,000 and 12,345; preceded by the reset sequence | Bit-identical to DTN-001 |
| DTN-037 | 001 | P | 44.1 kHz then 48 kHz, then DTN-002's events | Stable metric against DTN-002 |
| DTN-038 | 002 | P | ExcitatorVelocity host 0.25 against 0.253 (one step); 0.5 against the next lower binary32 value | Bit-identical; different |
| DTN-039 | 011 | P | Body on, BodyMix 0 | Bit-identical to DTN-001 |
| DTN-040 | 015 | U | KeyboardError above 0; VibratoError above 0 with vibrato on | Not graded: seed-dependent. Non-silent, bounded output only |
| DTN-041 | 015 | U | LFO Sync on; channel pressure, slide or per-note pitch bend; mod wheel; sustain pedal | Not graded (REQ-015) |
| DTN-042 | 014 | U | Polyphony 0 with KeyboardPriority 1 or 2, or overlapping legato notes | Not graded (REQ-014) |

## Open questions

Proposed for [questions](../questions.md) (not edited by this draft):

- **Block partition (A2).** Tension, like Analog, places events on a 1 ms grid relative to host
  blocks. T1 needs Live's partition, or a render convention that fixes it.
- **Live-side protocol (A1).** The event frame base, the transport and flag values, and when the
  reset sequence runs ([Q-025](../questions.md#q-025-device-host-protocol-and-device-audio-acceptance)).
- **Modulation sources (REQ-015).** Signal descriptions of vibrato, LFO, filter envelope,
  portamento and unison would let a candidate be built from this spec rather than from renders.
- **Chaotic settings.** The sustained excitator (type 0) and DamperMass 0 can be graded only
  statistically. Is that acceptable for T1?
- **libm.** Apple's libm against glibc for the functions the device calls. The metric assumes that
  they differ by at most one ulp on inexact results.

## Analyst evidence appendix

Analysis-only. Do not copy into a handoff. Canonical evidence:
[Tension DSP](../research/device-tension-dsp.md). Retained run
`analysis/ableton-live-12.4.3/r2/t12-tension-v1/`, harness `harness/xdev*.c` (copy of
t12-device-dsp-v1 with `xdev_bind.c` changed), built to `/var/tmp/sound-analysis/t12-tension/xdev`.
Slice: `Tension.bundle/Contents/MacOS/Tension` (SHA-256 `db7eb728…077c6f`), x86_64 at offset
16,384, 501,392 bytes, SHA-256 `63dd07171e76e20427045cc0269e124d67e94e6cddb42cab82c77cec7e6ed05d`.

| Clause | Evidence |
| --- | --- |
| 001 | `results/checks.json` `determinism`; exports `0x17690` (create), `0x17780` (rate), `0x178a0` (`CalcA`), `0x17bb0` (parameter), `0x17c30` (reset), x86_64 |
| 002 | N6 `out/conversions.tsv` (rows `StringStudio`), `tension.py` self-check; `checks.json` `quantization` (67 kind-0 indices at 0.25, 0.253 and 0.25 − ulp; index 48 boundaries; position scans); H4 `out/param_tables.json` kinds |
| 003 | `checks.json` `timing` |
| 004 | `checks.json` `pitch`; A(x) predictions in the research page |
| 005 | `results/measure.json` `held`, `release` (fit.py estimator, `measure.modes`); `checks.json` `string_curves` |
| 006, 007 | `measure.json`; `checks.json` `extremes`; engine text naming bow, hammer and plectrum parameters (arm64 string `0x55698`) |
| 008 to 011 | `measure.json`, including `body_minus_dry_third_octave_db` |
| 012 | `measure.json` `filter`; `checks.json` `filter_linearity`, `filter_maps` |
| 013, 014 | `checks.json` `level`, `polyphony` |
| 015 | `checks.json` `determinism` seed checks, `pitch` `KeyboardError_1_seed0` |
| Metric | `results/sensitivity.json` (31 cases × 5 perturbations; `_summary`); `results/fma_scan.txt` (arm64 822 fused in 109 functions, x86_64 0); estimator `fit.py`, `measure.modal_compare` |
| arm64 equivalence | Not executed. Differences expected from the fused operations and Apple's libm builds; bounded by the directed-rounding study (inferred) |

## Revision and handoff

| Revision | Date | Change |
| --- | --- | --- |
| 1 | 2026-10-18 | First draft from packet t12-tension-v1. 15 requirements: 13 X (001, 003 to 014), 002 S with X clauses, 015 X with U parts. U parts in 001, 002, 005, 006, 007, 011, 012, 014 and 015; one S-cond clause (003, A2). 42 cases: 27 graded by retained X renders, 12 check cases graded by exact values, 3 not graded (DTN-040 to 042) |

Not released. A first release could carry REQ-001 to 014 and the X parts of 015, cases DTN-001 to
039 and the reference renders as fixtures. It needs the metric accepted for ADR 0004, a decision
on A2 (the block partition), and a reviewer's check that the tables are behavior statements, not
recovered code.
