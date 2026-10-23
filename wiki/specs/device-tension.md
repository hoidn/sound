---
id: SPEC-DEVICE-TENSION
type: spec
status: draft
updated: 2026-10-23
access: analysis
revision: 17
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

**X, finite supplied native-host observations (revision 7).** The [kind-3 catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-tension-r7-kind3-finite-v1/cases117.json)
retains DTN-291–396 for 106 fresh one-host-word inputs and eleven historical
input references, covering all 164 aliases of 48 nonvirtual declared integer
domains as 117 unique vectors. These are supplied x86 native-host observations,
not validation of Live's stored-to-host conversions, current values or public
parameter path above. Host index 91 value 5 is explicitly an auxiliary native-
host boundary, not an ordinary Live/stored emitted value or application predicate.
Sign1 at zero magnitude, dormant LFO and inactive gates remain qualified; no
productive-effect, dispatch or general DSP law is inferred from equality.

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

**X, finite velocity-0 scope (revision 5).** [DTN-043](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-tension-r5-velocity-finite-v1/cases128.json) retains the
positive-zero output of the supplied default C4 history with note-on velocity 0.
That finite capture does not independently establish general velocity-0 dispatch,
held-voice note-off equivalence, arbitrary event history or Live's timing. The
existing timing clauses are not newly validated by the velocity annex.

**X, finite default note-key observations (revision 6).** The [128-point key catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-tension-r6-note-keys-finite-v1/cases128.json)
adopts DTN-168–290 for 123 fresh supplied note-key histories; keys 36, 48, 60,
72 and 84 remain inherited references. Both matching note-on/off key bytes vary
in the fixed constructor-default 129-word history below. All fresh outputs are
finite; keys 2 and 3 contain only positive zero and remain explicit observations.
No general note range, onset, dispatch, pitch formula, f0, alias/clamp mechanism,
velocity law or Live event timing is newly validated. REQ-004 is unchanged pitch
context; REQ-007 remains unchanged velocity context.

**X, finite supplied MIDI-axis observations (revision 8).** The [complete catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-tension-r8-midi-axes-finite-v1/cases143.json)
adds DTN-397–538 for 142 once-only histories:15 matching channel-nibble values
and127 Note-Off velocity bytes, varied independently in the fixed defaults44
history below. The shared DTN-001 baseline is inherited without replay. These
are supplied event-byte observations, not a newly established public channel,
velocity, release, held-voice, dispatch, timing or pitch law. Existing clauses
and U retain their scope; portable expected/comparator/grade remain NULL.

**X, finite supplied independent MIDI-byte observations (revision 9).** The
[complete catalog](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-tension-r9-independent-midi-finite-v1/cases285.json) adds DTN-539–822 for284 once-only
histories:127 On-key-only,127 Off-key-only,15 On-channel-only and15 Off-channel-only
members of the fixed defaults44 fixture. Each axis changes one supplied byte,
leaving the opposite key/channel unchanged. Four baseline aliases inherit ONE
DTN-001 INPUT reference without replay, new PID/receipt/metric or criterion
transfer. These observations do not establish unmatched-note/channel meaning,
release/gating/voice behavior, timing, pitch or public Live/ARM law. General U
and old clauses/criteria retain their scopes; all new waveform priors and
expectations, portable expected/comparator/grade remain NULL. New application
predicate proofs remain false.

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

**X, finite default velocity-byte observations (revision 5).** The [128-point catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-tension-r5-velocity-finite-v1/cases128.json)
adopts DTN-043–167 for 125 approved fresh inputs and retains velocities 1, 100
and 127 as existing DTN-005 / DTN-001 references. These exact supplied default
129-word C4 histories provide finite native word/size/channel/zero observations.
They add no fitted velocity curve, gain law, f0 estimate, waveform comparator,
stability class or physical calibration. Other velocity amounts remain U. The
annex's parent-launch custody and durability qualifications apply to every case.

### REQ-DEVICE-TENSION-008 — damper

- **X.** DamperToggle on, not gated, damps the string while it is held. At C4 the held RMS is
  0.0056, against 0.0951 without the damper. Partials 6 to 8 remain, and partials 1 and 2 of the
  release are raised to 285.7 and 568.8 Hz.
- **X.** DamperGated on leaves the held part's partials as without the damper. At the note-off it
  produces a transient (peak 1.016, against the note's 0.381) and a fast release: partials at
  284.5, 569.9, 850.9 and 1,117.3 Hz with T60 0.078 to 0.050 s.
- **X.** GeoDamperPosition 0 (not gated) leaves partials from 263.35 Hz with T60 0.62 to 0.29 s.
  DamperMass 0 makes the output chaotic.
- **U, evidence qualification (revision 3).** The historical revision-2 assertion
  that DamperVelocity has no effect when ungated has no independently joined
  exact input/result in the retained eleven check sets (TNR-067). Their
  sections-on quantization context does not settle that ungated behavior.
  The required behavior remains open; it is not a new no-effect expectation.

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

Proposed as the general T1 device-audio criterion of ADR 0004. The finite metric
of [device-tension-v1](../../handoff/device-tension-v1/README.md) is accepted
only for its listed inputs and frozen measurement eligibility; broader criteria
below remain proposed. Existing case class labels do not automatically classify new
parameter sets. For a newly studied parameter set, the proposed numerical margin
compares the maximum deviation from its same-setting unperturbed control, over
the five stated perturbations, with one quarter of each stable tolerance.
This is the reference-to-variant method below, not a measured pairwise spread.
Meeting that margin records only the result for the captured inputs; failing it
leaves eligibility unresolved and supplies no chaotic or statistical substitute.

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

These historical check expectations come from `results/checks.json`. Its
reported values and exact source-defined finite selectors are now linked by
the revision-3 annex below. Raw check execution receipts and renders were not
retained in the immutable packet; this revision performs no regeneration.
The table preserves earlier draft expectations, not newly approved exact-input
fixtures or numerical compatibility criteria. Missing execution/input bridges
stay U where required, and the released 27-evaluation metric remains separate.

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

### Finite default velocity-byte catalog — revision 5

The [R5 catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-tension-r5-velocity-finite-v1/cases128.json) adds 125 finite **X native observations**,
DTN-043–167, from the [sole actual/source approval](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/tension-velocity-bytes-v1-review.json)
SHA256 `98340a93c054964cc8ffbefc80c93dfe20585c4ff7a9482c711dd43744c6127e`.
IDs follow ascending fresh velocity bytes 0, 2–99 and 101–126. The complete
128-point catalog retains velocities 1 and 127 as references to DTN-005 and
velocity 100 as a reference to DTN-001. No duplicate ID, new historical receipt,
PID, UTC, audio decode or missing stereo/mono provenance is fabricated. The
42 earlier rows/IDs and retained R3/R4 owner objects remain exact; the resulting
167 navigation IDs are not compatibility grades or outcome counts.

Each evaluation supplies the same 129 ordered binary32 host words (indices
0–129 except 2) recorded in the approved summary. The fixed context is C4/key 60,
44,100 Hz, 44,100 frames, 512-frame blocks (last block 68), no warmup, zero input
and flag 0, stopped transport at position 0 and 120 BPM. Note-on is frame 4,096,
status 0x90, selected integer velocity; note-off is frame 26,146, status 0x80,
key 60, velocity 0. The recorded unperturbed x86 harness/provider environment
uses its existing fixed clock 0 and MXCSR context; this is not public A1/A2,
clock stability, native entry-register or floating-point-state proof.

All 125 fresh captures contain 44,100 finite stereo frames with bit-identical
channels. Velocity 0 is exactly positive zero in both channels; all other fresh
velocities are nonzero. The catalog retains every native output hash and exact
finite word summary, plus each input script and receipt/provenance reference.
These are observations at the supplied inputs, not a general zero-note or
velocity-response law. Native identities become finite expectations with
extracted-execution provenance; waveform priors, portable expected outputs,
comparators and candidate grades stay NULL. No f0 analysis, waveform measurement
method, fitting, metric, calibration, stability class or tolerance is added.

**Parent-launch custody qualification.** The child recorder, scripts, method
and context were bound by the pre-call record and independently reviewed.
The parent launch source was **not pre-call file-bound**. Its pre-execution
placement is author-reported/session tool source, without independent file-pin
or OS-execution attestation. The retained parent transcription/receipt agrees
structurally with the recorder argv, PID, UTC and environment; that agreement
does not close the custody gap. Thus the old README's broad all-code freeze
claim is qualified here. This limits parent execution provenance; the approving
review still admits the bounded child observations. No retroactive pin, frozen
source repair or original retry has occurred.

**Durability qualification.** The recorder's results JSON was explicitly
fsynced. The outer receipt and raw stdout/stderr/audio had no explicit file-
descriptor fsync; an all-JSON, directory or power-loss durability guarantee is
not established. The old broad README wording does not supersede this limit.
Recorded endpoint/provider identities and retrospective child failure checks
also do not prove continuous runtime binding, every interrupted/parent-loss
path or within-child interception. The exact qualification is retained verbatim
in the catalog from the sole review.

The entire 37-setting R4 sensitivity annex, its estimator/window and proposed-
margin qualifications, the earlier retained-report/input gaps, REQ-008's ungated
DamperVelocity U, other velocity amounts, all old state/error/history clauses,
metrics and tolerances remain unchanged. R4's statements about unchanged bodies
and no new IDs describe R4 itself. Its 31 margin matches and six unresolved rows
are not new calibration decisions for these velocity inputs. The 27 released
evaluations and four chaotic/37 uncalibrated exclusions stay separate and
unchanged. No ARM/Apple bound, public behavior, candidate result, release or
whole-product closure follows; ADR 0003's arm64 inference caveat applies.
Only new wording, ID mapping and preservation require the owner review; the
approved observations are inherited without reopening actual source or raw data.

### Finite default note-key catalog — revision 6

The [R6 catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-tension-r6-note-keys-finite-v1/cases128.json) adds 123 finite **X native observations**,
DTN-168–290, from [Root's sole actual/source approval](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/tension-note-keys-v1-review.json)
SHA256 `537ab1e99b8e7a7a50bbefb09453135508316c7f442521aaf09b89dc25597c06`.
IDs follow ascending fresh keys 0–35, 37–47, 49–59, 61–71, 73–83 and 85–127.
The full 128-point catalog retains key 60 as DTN-001 (`defaults_44`) and keys
36/48/72/84 as DTN-004 (`note_36`, `note_48`, `note_72`, `note_84`). These are
five exact historical input/metadata references, not new IDs or replayed controls.
Their missing fresh PID, receipt, UTC and descriptive metrics stay missing.
All 167 earlier IDs, 42 table rows, retained R3/R4 maps and complete R5 128-point
velocity catalog remain exact. The resulting 290 navigation IDs are not grades,
outcomes or compatibility passes.

Only the two matching key tokens vary. All 129 ordered binary32 host values
(indices 0–129 excluding 2) remain fixed, 516 bytes with vector SHA256
`e00185698bafd4531b3562012e001afa759556d27405928685f07bf2f5c97eb8`.
The context is 44,100 Hz, 44,100 frames, 512-frame blocks (last block 68), no
warmup, zero input and flag 0, stopped transport at position 0 and 120 BPM.
Note-on is frame 4,096, status 0x90, selected key and velocity 100. Note-off is
frame 26,146, status 0x80, matching key and velocity 0. The supplied event rows,
available packed 16-byte records, exact scripts and native output/provenance
references are copied from the approved summary. No new event type, reset,
segmentation, receiver model or state crossproduct is added.

Each fresh capture contains 44,100 finite stereo frames with byte-identical
channels. Keys 2 and 3 contain only positive-zero words; all 121 other fresh
keys are nonzero. There are 122 distinct fresh output hashes. Equality of the
two zero captures is descriptive only; no alias, clamp, pitch or physical
mechanism is inferred. Native output identities and unsigned finite/channel/
nonzero/negative-zero summaries become finite native expectations. Original
fresh waveform priors, portable expected outputs, comparators and candidate
grades remain NULL. No audio estimator, onset measurement, f0, fit, new metric,
window, tolerance, stability class or physical calibration is added. Existing
pitch, velocity, partial and generic comparison proposals are not newly
validated or made applicable to every new key by this annex.

The five historical joins use recorded exact vector/event/render contexts and
full script declarations. Their output identities and mono/stereo metadata are
inherited, not freshly decoded or measured. Other old pitch-40,000-frame and
no-off histories differ; incomplete histories imply no universal absence claim.
The inherited cases keep their earlier assertions as history, not new proof of
all parent-case metrics, partials or frequencies.

All new note-key capture code, including the parent launcher, was pre-call
file-bound. The approving review checks the source-level same-PID exec, planned
argv/environment and seal records. This differs from the R5 velocity capture's
historical parent-launch file-binding gap: that older gap and its durability
limits remain unchanged and are not retroactively repaired. For the note-key
batch, sixteen before/after runtime/local/script endpoint records per child
(1,968 pairs) and fifteen whole-batch source pairs agree; this is not continuous
provider/build/interpreter/OS-exec or child register/fenv/FP-state attestation.
The existing seven-export ABI, per-call MXCSR1f80, clock0 and substituted Linux
math/CXX behavior remain conditional harness-model context, not public Live,
Apple or ARM binding. Import declarations remain distinct from counted use;
26,937 selected direct exports, 10,701 CalcA calls and 123 separately logged
initializer entries do not bound nested/all-native calls. Rate returns and
flags remain opaque observations. Regular raw/log/JSON/launch file fsync was
requested, without directory or crash/power-loss durability proof. Detection
follows child completion; escaped descendants, uncatchable parent termination
and every cleanup path remain untested. No retry occurred.

All prior requirement text is retained, with REQ-003 only gaining this finite
qualification. REQ-007 stays whole-byte-exact, along with the older velocity
annex's parent and fsync limitations. All R4 37-setting sensitivity/window/
proposed-margin qualifications, six unresolved margin settings, four chaotic
exclusions, ungated DamperVelocity U, other U/state/error/history, tolerances
and 27 released evaluations remain unchanged. No ARM/Apple bound, general
pitch/key or public A1/A2 law, portable candidate criterion, release, site,
candidate result or whole-product closure follows. ADR 0003's arm64 caveat
applies. Only the new wording, mapping, IDs and preservation need the owner
review; the approved actual/source/raw/numeric proof is inherited without replay.

### Finite nonvirtual kind-3 native-host catalog — revision 7

The [117-vector catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-tension-r7-kind3-finite-v1/cases117.json)
and [164-alias joins](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-tension-r7-kind3-finite-v1/joins164.json)
retain 106 finite **X native observations**, DTN-291–396, from
[Root's sole actual/source approval](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/tension-kind3-host-domains-v1-review.json)
SHA256 `b050d049b20fdaab1692f3e4cd9faeb50fe74f9f7a7c70cc5b7c34ae7eafee55`.
IDs follow ascending fresh unique-vector order. All 290 earlier IDs and 42 table
rows remain exact. Aliases and case IDs are navigation units, not outcomes,
application coverage, candidate passes or accepted release criteria.

The retained native table declares 54 kind-3 rows. Excluding virtual indices
0,7,122,124,126,128 leaves 48 domains, each enumerated over every integer from 0
to its exact declared maximum. All baseline values are integral and in-range.
There are 164 logical domain/value aliases but only 117 unique whole vectors:
the constructor-default vector is one shared historical reference with 48
baseline aliases; ten other exact historical inputs and 106 fresh inputs make
the remainder. No baseline is replayed and no state crossproduct is added.
Only one host word differs per nonbaseline vector. The 129-word index order
(0–129 except 2), other 128 words, key60/velocity100, rate44100, 44100 frames,
block512/last68, zero input/flag0,
no warmup, stopped0,0,120 and on4096/off26146/status90/80/offvelocity0 remain
fixed. Supplied tokens/binary32 words, exact input/output identities, native
unsigned descriptors and available event/provenance records are retained in
the approved summary and catalog.

The eleven historical input references are `defaults_44` (DTN-001),
`exc_hammer` (DTN-007), `exc_bounce` (DTN-008), `exc_bow` (DTN-009),
`damper_on` (DTN-017), `pickup_on` (DTN-020), `term_on` (DTN-019), and
`body_type_0` through `body_type_3` (DTN-022). They retain exact input-script
and old-manifest WAV metadata only, without new IDs, PID, receipt, metrics,
old audio decode or replay. Baseline collapse does not fabricate 48 captures.
Their parent-case frequency, stability, onset, partial or comparison assertions
are not newly proved. Pickup-37-frame and ungated DamperVelocity remain on their
separate evidence/unknown scopes.

Every fresh output is finite with byte-identical channels. Only TK3-U045
(host36=0) consists entirely of positive-zero words; the other 105 fresh vectors are nonzero.
There are 36 distinct fresh hashes. These are recorded finite identities and
unsigned finite/channel/nonzero/negative-zero descriptors, with no onset/f0
estimator, fit, new metric/window/tolerance, stability or physical calibration.
Native expected entries copy only approved observations. Original fresh waveform
priors, portable expected outputs, comparators and candidate grades remain NULL.
No arbitrary parameter behavior, inactive-domain law, alias/clamp mechanism or
productive DSP conclusion follows from silent or equal captures.

Host91=5 remains an **auxiliary native-host boundary**: its declared native
0..5 range is distinct from N6's ordinary stored FilterType0..9 mapping to
host91=0..4 plus remainder92. Its new ID has no application-predicate mapping.
The other 105 fresh IDs are also finite native-host observations rather than
proof of ordinary Live emission or current receiver delivery. Sign1 with zero
magnitude, unison/toggle folding, inactive modules and LFO shapes with the LFO
off are not claimed to be productive or ordinary public stored states. Live's
conversion/current-value/ABI/public A1/A2 and ARM/Apple joins remain unknown.

Three fresh members, host6=2,13=1 and36=0, have earlier source-declared recipe
relations but lacked complete changed-vector/process/raw bridges. This current
capture does not retroactively repair those historical U bridges, seed,
polyphony or velocity claims. The input-only68-script census and retained
recipe comparisons establish bounded intersections, not universal absence of
other histories or fresh historical execution provenance.

All new domain capture code including the parent launcher was pre-call file-
bound. Sixteen per-child runtime/local/script before/after records (1,696 pairs)
and sixteen whole-batch source pairs agree. Same-PID/source/argv/environment/seal
records are not independent OS-exec/interpreter/provider/build-from-source or
child register/fenv attestation. Existing clock0, per-call MXCSR1f80 and Linux
math/CXX substitutions remain the admitted harness model, not Apple/ARM or Live
binding. Import declarations are distinct from counted code use; 23,214 selected
direct exports,9,222 CalcA and106 logged initializer260c0 entries do not bound
all nested native calls. Rate returns/flags remain opaque observations. File
fsync requests do not prove directory/crash/power-loss durability; post-child
checks cannot undo queued calls, and parent-loss/escaped-descendant/all cleanup
paths remain unexhausted. The retained initial assembler is not a final
regenerator; the pre-freeze INDICES restoration involved no original retry.

The old velocity parent-launch file-binding/fsync gap is unchanged. R6 key and
R7 domain launcher bindings are separate and do not repair it. All fourteen
other whole requirement bodies, old REQ-002 prefix, R3/R4 maps, complete R5/R6
catalogs and old Acceptance text remain exact, including the 37-setting
sensitivity/window/margin qualifications and six unresolved margin settings.
All U/state/error/history, four chaotic exclusions, metric/tolerance proposals
and 27 released evaluations / 35 release inventory entries remain unchanged.
No release, site, portable candidate criterion, general DSP/public/ARM law or
whole-product closure follows. ADR0003's arm64 caveat applies. Only new wording,
IDs, mapping and preservation require this owner review; actual/source/raw/
numeric proof is inherited from the sole approval without replay.

### Revision 8 finite matching-channel and Note-Off-byte observations

The [143-history/144-alias catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-tension-r8-midi-axes-finite-v1/cases143.json) retains two independent
whole typed axes, not a crossproduct:matching status channel nibbles0..15 and
Note-Off data2 bytes0..127. Channel0 and Off velocity0 are two aliases to ONE
DTN-001/defaults44 control inherited from the approved Root note-key summary.
It receives no new ID, PID, receipt, metrics or original call. The15 new
matching-channel histories receive DTN-397–411; the127 new Off-velocity
histories receive DTN-412–538. Fullhistory dedup is essential:all129-word
parameter vectors are identical while the143 complete event histories differ.
The catalog and [joins](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-tension-r8-midi-axes-finite-v1/joins144.json) retain full event coordinates,
input/output identities and exact approved-summary pointers for EVERY case.

Only Root's [sole actual/source approval](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/tension-midi-axes-v1-review.json),
SHA256 `148ffd51bb2e33c32a615665c286996b31c43becd5e27d8444e95c492a2fdb4d`,
supplies these observations. This owner mapping does not repeat source, raw,
audio or numeric proof. It proposes no expectation before observation, metric,
f0, fit, window, calibration, tolerance, stable/chaotic class or portable method.
All original fresh waveform priors and portable expected/comparator/grade
remain NULL. Native hashes and word summaries characterize finite retained
outputs; they are not portable candidate waveform acceptance criteria.

The common constructor-default vector is129 ordered binary32 words at host
indices0..129 except2,516bytes/SHA256
`e00185698bafd4531b3562012e001afa759556d27405928685f07bf2f5c97eb8`.
Each recorded instance uses rate44100/render44100frames/block512/last68,
no warm-up, zero input/flag0, stopped transport0/0/120, key60, on at4096 with
velocity100 and off at26146 with baseline velocity0. The channel axis changes
BOTH statuses to90|n and80|n only; the independent Off-velocity axis leaves
statuses90/80 fixed and changes only Off data2. No CC, sustain, unmatched
channel, new event type, timing segmentation, later parameter update or state
crossproduct is introduced. These are supplied host/test coordinates and
recorded-model defaults, not proved Live scheduling or target-entry FP state.

All142 fresh outputs are finite, nonzero and have identical channel words.
Their one fresh hash matches the approved inherited baseline METADATA; no old
audio was opened or control replayed. This is descriptive finite equality,
not proof of general channel filtering, Off-velocity independence, ignored
MIDI, note-off admission, existing-voice equivalence, inactivity, mechanism,
public legality, physical accuracy, current receiver or ARM/Apple behavior.
The old general timing and velocity clauses are not newly validated here.

All new capture code INCLUDING the parent launcher was pre-call-bound for
THIS batch. It does not repair the older velocity parent-launch gap or older
source-version/execution associations. SamePID/source/hash receipts do not
attest OSexec/build/continuous loaded providers/entry FP/ABI. Import142
declarations (109Linux,26trap,7data) stay separate from counted code use;
selected direct exports and initializer260c0 are separate from unbounded
nested native work. Rate's observed signed integer has unknown public or
sample-clock meaning. This collector requested fsync for JSON/JSONL and
regularstdout/stderr FDs plus the retained audio read FD after child completion;
that is not directory/crash/power-loss durability proof. Earlier packets keep
their own fsync limits. Post-child checks cannot retract earlier within-child
calls; cleanup does not prove every escaped-descendant/uncatchable-parent path.

Only bounded REQ-003 wording is appended. All14 other whole requirements,
including REQ-002 and general pitch004/velocity007/ungated DamperVelocity008 U,
old003 prefix,42 historical rows/396 prior IDs, R3–R7 objects/catalogs,
all37 sensitivity rows/31-versus6 qualification, originalNULLs/state/error/history,
comparison tolerances and released27 evaluations/35inventory entries remain
exact. The resulting538 navigation IDs are not passes or an application
outcome denominator. New application-predicate proofs remain false; no owner
application/publicA1A2/ARM grade, release or whole-product closure follows.

### Revision 9 finite independent On/Off key and channel observations

The [285-history/288-alias catalog](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-tension-r9-independent-midi-finite-v1/cases285.json) retains four complete,
independent typed axes at the same parameter vector:On-key-only0..127 fixes
Off key60; Off-key-only0..127 fixes On key60; On-channel-only0..15 fixes Off
status80; Off-channel-only0..15 fixes On status90. No crossproduct or matching
change is invented. DTN-539–822 label284 fresh observations:127+127+15+15
nonbaseline values. Four baseline aliases (Onkey60/Offkey60/Onchannel0/
Offchannel0) share ONE inherited DTN-001 INPUT reference. It receives no new
ID, original call, PID, receipt, output, metric, expectation or criterion.
Full-history dedup is essential:the129-word parameter vector is common while
285 complete event histories differ. [All288 joins](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-tension-r9-independent-midi-finite-v1/joins288.json)
preserve every event/packed16 record and original decimal/binary64/binary32
input identity and exact approved-summary pointer; the inherited baseline
keeps its approved input projection without a new raw/metric reconstruction.

Only Mix's [sole actual/source approval](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/tension-independent-midi-bytes-v1-review.json),
SHA256 `a49bf2e423c7df89bcb142bef1f35548340a664885ac3496a375952b5b11feb9`,
supplies these finite observations. This owner maps its approved summary
without actual/source/raw/audio/numeric re-review. Native output identities
and copied word summaries are descriptive references, not portable candidate
waveform criteria. No f0, estimator, window, metric, fit, tolerance, physical
calibration, new stable/chaotic class or portable method is proposed. Fresh
waveform priors/new expectations, portable expected/comparator/grade remain
NULL. No old baseline criterion or modal budget transfers to the284 cases.

The constructor-default context keeps129 ordered setter words at host
indices0..129 except2,516bytes/SHA256
`e00185698bafd4531b3562012e001afa759556d27405928685f07bf2f5c97eb8`.
Original decimal tokens and their binary64 parsing are retained alongside
binary32 words. Each instance uses rate44100/render44100frames/block512/last68,
no warm-up, zero input/flag0, stopped transport0/0/120, baseline On4096/status90/
key60/velocity100 and Off26146/status80/key60/velocity0. Only one selected
On-key/Off-key/On-status-low-nibble/Off-status-low-nibble changes per history.
The opposite key or channel stays fixed. No CC, sustain, extra event, timing
segmentation, reset, host update, constructor model, patch or provider change.
These are supplied test coordinates/recorded-model defaults; internal/public
event admission, current receiver and Live frame base remain unproved.

The approved summary retains all284 captures as finite with identical channel
words;282 have nonzero samples in both channels. TENSION-BYTE-002 and003
(the On-key-only2/3 histories) are numerically zero and remain in the catalog.
There are127 fresh hashes, descriptive only. No old baseline audio is replayed
or compared. Quiet outcomes, equal words or hashes do not prove ignored Off,
unmatched-note release semantics, channel matching, latching, inactivity,
productive controls, pitch/voice mechanism, physical accuracy, current public
binding or ARM/Apple equivalence. Old general MIDI/pitch/velocity/lifecycle
assertions and named63/Damper unknowns are not newly validated by this class.

All new capture/data/parent/checker/initial-materializer code was pre-call-bound
for THIS batch. Its initial materializer is a historical first stage, not a
final regenerator. That does not repair the old velocity parent-launch/fsync
gap, source-version associations, or other earlier proof limits. SamePID and
before/after endpoint hashes do not attest OSexec/build/continuous providers/
entry FP/ABI.142 declared imports (109Linux,26trap,7data) remain distinct
from counted code use.219 selected direct exports/87 CalcA per child plus
initializer260c0 logged separately leave nested/all-native counts unknown.
Rate's signed integer remains opaque, not a public success/sample-clock law.
New JSON/JSONL/log/audio FDfsync requests do not prove directory/crash/power-loss
durability or repair older scopes. Post-child checks cannot retract earlier
within-child calls; group/direct-child cleanup does not cover all parent-loss
or escaped-process paths. Existing r2-large lexical/resolved storage and
pre-child resource guards are custody limits, not application behavior.

Only bounded REQ-003 wording is appended. All14 other whole requirements,
including ENTIRE REQ-002 R7 native-host qualification, old003 R8 prefix,
42 original rows/538 prior IDs, allR3–R8 objects/catalogs, all37 sensitivity
rows/31-versus6 qualification, auxiliary nativehost91=5 admission limit,
original NULLs/generalU/criteria/tolerances/state/error/history, and released
27evaluations/35inventory entries remain exact, with full reversal. The
resulting822 navigation IDs are not passes or application-outcome units.
New application-predicate proofs remain false; no release, portable criterion,
publicA1A2/ARM grade, calibration or whole-product closure follows.

### Revision 10 partial supplied stepped-controller observations

This annex maps ONLY [Root's sole partial actual/source approval](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/tension-stepped-controller-cells-v1-review.json),
183,968,010 bytes/SHA256 `b456eb66f7b7df7496f7989b9d951b55227c845d9e8b65d985d7cd80ea7a9086`.
[DTN-823–2210](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-tension-r10-partial-stepped-cells-finite-v1/new-cases1388.json) are1388 approved finite native
observations. The [complete catalog](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-tension-r10-partial-stepped-cells-finite-v1/catalog5350.json) retains5350
WHOLE histories/5364 aliases: ONE qualified defaults44 DTN001/TK3 baseline
with15 aliases,1388 approved fresh observations,ONE failed U history and3960
unattempted U histories. These are not5349 completed or accepted captures.
The [full joins](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-tension-r10-partial-stepped-cells-finite-v1/joins5364.json) preserve original decimal/f64/f32
words, complete history identities and exact approved-summary pointers.
No actual/source/raw/audio/numeric or old-proposal/provider proof is repeated.

All15 existing requirement bodies remain exact. REQ-002 supplies the existing
stepped-input context only; this annex adds no quantizer, within-cell,
continuous-domain, productive-effect, physical/calibration or public/ARM law.
Eighteen primary128-member axes and twelve signed255-member axes use paired
abs(value) at the magnitude index and sign(value<0) at the next index. Zero
has one sign; no independent magnitude-sign crossproduct or negative-zero
sign1-at-zero class is added. The parameter model is unchanged, without
activation of excitator, damper, body, gate or previously inactive branches.
The inherited baseline is INPUT only, without replay, new case ID, PID,
receipt, metrics or criterion transfer. Source-only recipes lacking an old
execution bridge remain historical U, not retroactively repaired by this class.

The first-fault contract stopped after1389 once-only children:1388 protocol-valid
observations and TENSION-STEP-U1389 failed U at host48 ExcitatorVelocity,
representative116/127, literal0.9133858267716536. Its ninth CalcA block,
starting4096 in the recorded process coordinates, returned1; all other
recorded returns were0/flag1. Exit0/empty stderr/no timeout do NOT establish
protocol success. It has NO accepted protocol, metric, case ID, native
expectation or grade. Root's retained finite unsigned diagnostic is not an
accepted metric or waveform criterion. The return ABI, cause and meaning
remain unknown. All3960 later planned histories were unlaunched, unnumbered
and ungraded. No guard relaxation, retry, continuation or state substitution
is authorized or represented by this annex.

The1388 approved outputs are finite and channel-word-equal;1381 are nonzero
in BOTH channels and all seven quiet observations remain represented.800fresh
hashes and76 used Linux code-import names are descriptive only. They do not
establish same output across cells, deterministic waveform laws, inactivity,
physical behavior, stable/chaotic classes, calibration or absence of a provider.
Every new prior/waveform expectation/native expected/portable expected,
comparator and grade remains NULL; new application-predicate proof is false.
Native output references are observations, not portable candidate criteria.
No f0, fit, metric, tolerance, window, modal budget or general law is added.

All129 ordered original decimal/f64 setter words/130-slot range with index2
omitted remain; On4096/velocity100, Off26146/velocity0,44100Hz/44100frames/
block512/final68, no warmup, zero input/inflag0, stopped0/0/120/TIME0 and
unperturbed entryFP/existing model are fixed. Minimal C locale differs from
old kind3 C.UTF-8; source/executed-version/defaulttimeFP/environment/old
velocity-parent/sensitivity/calibration limits retain their own scope.
New parent binding never repairs the old velocity-parent gap. No new event,
rate/block/reset/timing/host-state crossproduct, model/tool/build/patch/provider
or receiver construction is supplied. Same-PID/source endpoint custody is
not continuous OSexec/interpreter/nativeFP/ABI/loaded-provider attestation.

Eight source endpoint pairs and22,224 actual per-child sixteen-pair checks
span all1389 attempts. Parent resource guard code was prebound and called,
but separate returned parent resource values were NOT retained; recorded
child remaining-output floors are distinct.4GiB lifecycle+128MiB headroom,
131072 future-metadata bytes per child and512MiB final reserve are unreserved,
not quotas/worst-case/external-writer/escaped-child guarantees. Post-child
checks do not retract within-child calls; group cleanup is not exhaustive.
Successful1388 raw/log/JSON FDfsync requests remain qualified. Failed raw
fsync was SKIPPED by the protocol guard before that branch: close/hash only;
its stdout/stderr/JSON requests remain. No directory/crash/powerloss proof
or historical FDfsync/source/parent repair follows. Bindings declared differ
from counted code use; valid-protocol303972 exports/120756 CalcA/1388 logged
260c0 initializers do not count all failed-child, nested or native calls.

Only this annex and revision metadata change. All15 requirements,822 prior
navigation IDs/42 old case rows, R3–R9 objects/catalogs,37-setting sensitivity
31 proposed margins/six unknowns, auxiliary91=5 native-host-only qualification,
quiet002/003, old velocity-parent gap, criteria U/state/history and releases
27 evaluations/35 inventory entries remain exact through the pinned Auto R9
embedded mapping/preservation, with full reversal. Older absent object bytes
are not reconstructed or claimed freshly audited. Resulting2210 navigation
IDs are not application passes or an outcome denominator; no new release,
site, grade or whole-product closure. Required unsupported U stays OPEN.

## Retained report reconciliation — revision 3

The [independently reviewed retained batch](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/tension-retained-checks-v1-review.json)
joins every field of the original report to its source-defined finite context.
The [owner annex](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-tension-r3-retained-v1/README.md)
links all eleven sets together. Their 239 report projections are navigation
entries, not new case IDs, native calls, exact-input fixtures, grades or a
coverage denominator. All 42 existing case rows are preserved.

| Retained check set | Finite reported relation or quantity |
| --- | --- |
| determinism | Named block, seed, FTZ/DAZ, reset, rate, silence and Body comparisons |
| timing | Complete selected note-on/off frame groups, effective-frame comparisons and travel-delay table |
| quantization | All 67 kind-0 controls, five boundary pairs and six complete 129-value position scans |
| pitch | Selected notes, octave/transpose/fine/stretch/bend settings and unresolved high-note measurement |
| level | Ten BodyLevel settings against the retained defaults; gain, spread and separately identified author prediction |
| polyphony | First reported capacity crossing, three repeated-note ratios and one mono-steal frame |
| filter_linearity | Six finite response comparisons at the stated harmonic matching/window limits |
| extremes | All ten selected finite peak/silence observations, including inactive results |
| string_curves | Selected held/release/key-amount measurements and equalities, preserving unresolved partials |
| filter_maps | All selected cutoff/Q harmonic-response measurements and unresolved crossings |
| corpus_crosscheck | Three retained Corpus input histories across three library variants; no modal-calibration transfer |

The [finite selectors](../../analysis/ableton-live-12.4.3/full-spec-v1/batch-tension-retained-checks-v1/input-selectors.json)
and [reported observations](../../analysis/ableton-live-12.4.3/full-spec-v1/batch-tension-retained-checks-v1/observations.json)
carry inherited historical X attribution. This is approval of retained report
and source joins, not a new audit of original execution. Per-child PID, argv,
status, stdout/stderr, import use, FP/clock custody and changed indexed-input
bridges are absent. Exact fixture/native admission stays U wherever those
bridges are required. Present volatile scratch files do not repair that history;
none was read, hashed, decoded or replayed for this reconciliation.

Finite reported Booleans retain only their exact source context. Quantization
`none` means equality of three captures in that context, not global inactivity
or ungated DamperVelocity behavior. Its third value is the immediate lower
binary32 neighbor of 0.25 (`0x3e7fffff`), not the driver's shorthand “minus
10⁻⁶.” Numerical quantities stay descriptive: ideal pitch and predicted gain
are author reference values, not native outputs; unresolved measurements and
missing comparison values remain NULL. No new fit, tolerance or physical
calibration follows.

The broad map pointer to `timing` does not provide the pickup's 37-frame
comparison, and the pointer to `extremes` does not provide a paired velocity-1
VelMod comparison. Those earlier render claims retain their separate DTN-021
and DTN-006 evidence references; this report supplies no new coverage for them.
The [explicit frontiers](../../analysis/ableton-live-12.4.3/full-spec-v1/batch-tension-retained-checks-v1/open-frontiers.json)
also keep the ungated DamperVelocity input/result gap open.

Synthetic A1/A2 state, fixed/alternate clock seeds and substituted libraries
remain the original context. The finite 1,024-frame reset prefix does not
establish the host's separate four-helper sequence. The 27 released finite
evaluations (26 stable and one repeated strike), four chaotic exclusions and
37 uncalibrated settings are unchanged. No random-waveform metric, ARM/Apple
bound, actual Live receiver, public timing or audio behavior is added.

### Revision 11 finite rate/block protocol observations

The [four-case mapping](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-tension-r11-four-protocols-finite-v1/mapping.json)
adds DTN-2211–2214 only for the four newly approved supplied histories:
44100 Hz/blocks256 and333, direct48000 Hz/block512, and create/rate44100,
all129 original setters, then rate48000/block512. REQ-001 is context for
these finite observations; its entire existing body remains unchanged.
All new priors/native-waveform expectations/portable expected/comparator/
grade are NULL; application proof is false. These are original model output
references, not portable criteria or general sample-rate/block invariance,
pitch/onset/productivity/capacity, current Live/ARM/Apple or physical laws.

The sole actual/source authority is [Auto's approved four-history review](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/tension-four-unlaunched-protocol-v1-review.json),
547683bytes/SHA256 `8b19f0c40e4d6ab4d7df400c68472b45ccf9987497931284a9074172e7eacce9`.
Only its approved summary supplies INPUT/receipt/output/protocol references.
All four literal129-word decimal/binary64/binary32 vectors, omission of
host2, original parameter order, rate order and absolute supplied event
coordinates remain exact. Direct44.1k uses44100frames/On4096/Off26146;
48k histories use48000frames/On4096/Off28096. No warmup or injected MXCSR/
transport commands, reset, crossproduct or new event/construction is added.
C.UTF-8/TIME0/LIBM-unset and the existing155680-byte xdev/native model are
supplied context; historicalenv/default/source-executed-version/FP/provider/
OSexec equivalence remains qualified. Rate1 is an opaque integer projection.

The original six-history/seven-alias catalog remains mapped. Old44100/512
baseline/twoaliases is qualified INPUT only: no newID/PID/receipt/output/
metric/criterion transfer or replay. The old block64 attempt remains
FROZEN GUARD-FAIL/U, with no newID/expectation/metric/grade; its empty-init
assertion was false, not repaired or replayed. The four formerly unlaunched
histories now have distinct new once-only captures. Future model DATA
expects exactly ONE initializer260c0 from already approved matching-model
metadata; all494CalcA still satisfy ret0/flag1 and every other guard remains.
This does NOT adopt proposed design13, relax the opaque-return guard, retry
the earlier stepped failure or execute/regrade its3960unlaunched histories.
Those earlier failed/unattempted U records and R10's full5350 dispositions
remain unchanged; no output comparison to either oldfailed64 or baseline
is performed. No return ABI/success/error/void/clipping/cause law follows.

1023selected direct exports/494CalcA/four separate logged initializers count
only this four-child protocol; all nested native/provider calls remain U.
76 actual per-child19before/after custody pairs plus two whole-source pairs
are endpoints, not continuous loaded-provider/nativeFP/register-entry/ABI/
OSexec attestation. Accepted raw/log/JSON file descriptors request fsync;
outer FDs are not explicitly fsynced. No directory/crash/powerloss or earlier-
gap durability repair follows.128MiB lifecycle+128MiBheadroom/fullremaining
resource guards are unreserved/soft, not quotas or concurrent-writer/
escaped-process/within-child overshoot guarantees. Untested SIGTERM/cleanup/
uncaught-parent-loss/transitive-library/source associations retain scope.

Only this annex and revision metadata change. All15 whole requirement
bodies,2210prior navigation IDs/42old rows/R3–R10objects,37-setting sensitivity
with31proposed margins/sixunknowns, quiet002/003/aux91=5/oldvelocityparentgap,
criteria/U/state/error/history and released27evaluations/35inventory objects
remain exact with full reversal. Preservation uses currentR10 and its sole
owner REPORT's embedded mapping/preservation metadata; absent oldobjects
are not reconstructed, and no release fixture/catalog is reopened.
The resulting2214 navigation IDs are not passes or a product denominator.
No actual/source/code/raw/numeric/provider/oldproposal/fixture proof repeats
in this owner revision. No new release, grade, site credit or closure;
required unsupported U remains OPEN.

## Revision 12 finite supplied stepped-controller suffix observations

The [sole actual/source review](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/tension-stepped-unlaunched-opaque-returns-v1-review.json)
approves exactly 3,960 fresh supplied-host histories `TENSION-STEP-U1390`–`U5349`.
The [complete owner catalog](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-tension-r12-opaque-stepped-suffix-finite-v1/mapping.json)
assigns **DTN2215–DTN6174**, one new observation ID per approved history, with all
3,960 aliases, exact original decimal tokens/binary64/binary32 words, complete
scripts and receipt/output pointers. REQ-002 is the supplied-input context;
all fifteen requirement bodies remain unchanged. These are native x86 extracted
observations, with no new application-predicate proof or portable acceptance rule.

Each history retains the recorded 129 host setters at indices 0, 1 and 3–129
(host 2 omitted), the selected magnitude/sign pairing, On at 4,096 and Off at
26,146 for key 60, 44,100 frames at 44,100 Hz in 512-frame blocks (last 68),
silent input/flag 0 and no warmup. The C/TIME0/LIBM-unset/default-FP and stopped
transport context, unchanged admitted xdev/bundle/model, source-version and
provider qualifications remain those in the approved report. No new event,
parameter crossproduct, reset, FP treatment or receiver construction was added.
The 867,240 selected exports, 344,520 CalcA projections and 3,960 separately
logged initializer entries are supplied-harness accounting; nested calls remain U.

For this new suffix only, the user-adopted design13 collector records every CalcA
return as an **opaque signed64 integer**, preserving exact RLE and order. All
other frozen guards remain: exit/stderr/trap/fault, import declarations/use,
exactly one initializer 0x260c0, parameter/event/frame/raw shape, process flags
0 or 1, CXX failbits, both-channel finiteness, custody, timeout, cleanup and
resources. The literal 343,063 zeros and 1,457 ones (73 histories containing a 1)
do not establish a general 0/1 return domain, native ABI, cause, success/error,
void/arbitrary-value, clipping or activation meaning. Every recorded process
flag is 1; that does not establish a general flag law. Signed64 endpoint
acceptance is synthetic collector testing, not an original return observation.

All 3,960 outputs are finite and stereo-word-equal. **Thirteen histories are
quiet and 3,947 are nonzero**; the 889 raw hashes are descriptive only. Quiet
histories remain in the catalog without substitution, exclusion or new grade.
No waveform, residual, f0, estimator, modal, calibration, determinism,
productivity, effect/no-effect, general velocity, public Live or ARM law follows.
All fresh waveform priors, native waveform expectations, portable expected
values/comparators and grades remain NULL, and new application proof is false.
No tolerance, criterion, release, main-image-site or coverage closure is added.

The full **5,350-history / 5,364-alias OLD ASOF** catalog is preserved separately:
1,388 previously approved, the qualified U0255 INPUT-only baseline, the frozen
failed U1389 and the then-unattempted 3,960 suffix. The new approval does not
rewrite those historical dispositions, repair U1389, or replay/invent baseline,
failed or prior accepted PID, receipt, output metric or criterion evidence.
Older parent/fsync/source/FP/provider gaps retain their old scopes. All previous
objects, sensitivity37 (31 proposed margins and six U), quiet002/003,
auxiliary host91=5, U/history/criteria and releases remain unchanged.

Fresh endpoint custody comprises 75,240 per-child before/after pairs and one
whole INPUT-authority pair. Endpoint hashes, same-PID exec expectations and
reported interpreter/source identities are not continuous loaded-provider,
input-read, OS-exec, ABI or FP-register attestation. The 4GiB lifecycle plus
128MiB headroom and remaining-output/final-metadata guards are unreserved
estimates, not a quota or worst-case allocation/overshoot guarantee. Accepted
logs/raw/JSON reached FD-fsync requests; outer redirects have no explicit FD
fsync, and no directory/power-loss durability or old-gap repair follows. Full
report limits remain binding. Frozen D07-unrecorded prose is an as-of label:
local Windows VM is now chosen, readiness remains open and no O evidence follows.

## Revision 13 finite declared quantization partial observations

The [sole recorder2 actual/source review](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/tension-declared-quantization-recorder2-v1-partial-review.json)
approves **209 finite observations**, assigned **DTN6175–DTN6383** in the
[complete owner mapping](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-tension-r13-declared-quantization-partial-finite-v1/mapping.json).
These comprise the 201 declared active-context triples and eight host-48
boundary recipes, in approved source order. The full **981 literal histories /
985 recipe aliases** remain a partial as-of snapshot: 209 approved histories
and aliases, failed `TQI-B4-point` U, and **771 unattempted histories / 775
aliases U**. Only the 209 approved histories receive new IDs. No accepted
metric, waveform expectation, portable criterion or grade is assigned to the
failed or unattempted members. These are historically declared recipes with
new retained captures, not a global never-run claim or repaired old result.

Every catalog member retains all 129 original decimal, binary64 and binary32
setter words at indices 0, 1 and 3–129 (host 2 omitted), its complete literal
script and supplied-context history hash. The 201 active recipes retain the
ten source-declared context changes, key 72/velocity 90, On1024/Off7000 and
12000 frames; the host-48 recipes retain On4096/Off26146 and 8192 frames.
That late Off is not clipped or moved into the render. Literal 0.253 remains
distinct from a promoted binary32 value, and actual binary32 predecessors are
preserved. The 774 position aliases / 770 distinct scripts stay unattempted;
the four exact duplicate aliases create no extra calls or cases. Rate44100,
block512, zero input/flag0, no warmup/reset/new MXCSR or transport commands,
C.UTF-8/TIME0/LIBM-unset and the unchanged admitted model/default-entry FP
remain the supplied premises. Legacy environment, source/executed-version,
provider, construction, public receiver and OS-exec bridges remain qualified
or unknown. The script hash is not a legacy native-history identity.

Recorder2 corrects only an owned identity-record schema mismatch after the
original packet's zero-native preparation failure. Applicable lexical path,
resolved path, byte count and hash comparisons remain intact; nine recorded
real compatibility checks and 54 field negatives are bookkeeping controls,
not OS-exec or continuously loaded-provider proof. The original all-981-U
prelaunch snapshot stays immutable. This recorder2 used **strict CalcA return
zero / flags 0 or 1**, with every other guard unchanged. User-adopted design13
remains confined to the separate 3960-history suffix; no opaque-return policy
is transferred to this class.

First-fault stopping retained failed `TQI-B4-point` U and stopped all later
launches. Its exit zero, legal flags and retained raw bytes do not admit it;
failed returns remain unaccepted diagnostics without a native ABI, cause,
success/error, clipping, activity or boundary meaning. There was no native
retry, failed replay, continuation or guard relaxation. Failed raw-FD fsync
was skipped by the pre-existing guard branch. This annex supplies no failed
output metric or full-class success claim.

The 209 approved outputs are finite, both channels nonzero and stereo-word-
equal, with 100 distinct raw hashes: descriptive finite observations only.
Their 32540 selected exports, 4952 CalcA calls and 209 separately logged
initializer entries are accepted-only accounting; nested native calls remain
unknown. Full-class prospective counts are not actual completion counts.
All new waveform priors, native waveform expectations, portable expected
values/comparators and grades remain NULL; application proof is false. There
is no new quantizer, within-cell equivalence, productivity, stability, f0,
modal/physical calibration, fitted metric, public Live or ARM law, tolerance,
release, main-image site or coverage closure.

The sole review retains 3780 per-child endpoint pairs (18 per attempted child)
and three whole REPORT pairs, not continuous loaded-provider, input-read,
FP-register, compiled-source or OS-exec attestation. The full 4GiB lifecycle
plus 128MiB headroom and complete remaining-output/future-metadata/final-floor
guards are unreserved estimates, not a quota or worst-case overshoot bound.
Accepted raw and child log/JSON FD-fsync requests do not establish directory,
crash or power-loss durability; outer redirects lack explicit FD fsync. Older
parent, source, FP and fsync gaps are not repaired.

All fifteen whole requirements, 42 old case rows, 6174 prior navigation IDs,
R3–R12 objects, sensitivity37/31 proposed margins versus six U, auxiliary
host91=5, quiet002/003, old velocity parent gap, criteria/U/history and the
27 released evaluations / 35-object inventory stay exact. The separate
5350-history / 5364-alias OLD ASOF still records its 1388 accepted, failed
U1389, qualified U0255 INPUT baseline and then-unattempted 3960 suffix; the
R12 approval does not rewrite that snapshot. Failed64 and original zero-native
snapshots remain U in their own scopes. TQI-RV-Q01 still identifies the old
TENSION-BYTE-060 field as a prior MIDI INPUT-class match, not a TQI script
intersection or old executed-source bridge. Preservation inherits only the
prior sole owner REPORT's embedded metadata and reverses exactly to R12;
no old proposal, fixture, provider, actual/source/raw or numeric proof is
reopened. Resulting 6383 navigation IDs are not passes or a product denominator.
Unsupported required behavior remains U and whole-Live coverage OPEN.

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
| arm64 equivalence | Not executed. The library/directed-rounding study measures sensitivity of the x86_64 renders; it does not establish a bound on arm64 or Apple's library results |

## Revision and handoff

| Revision | Date | Change |
| --- | --- | --- |
| 13 | 2026-10-22 | Add only 209 finite declared quantization observations, DTN6175–6383, within the full 981-history / 985-alias snapshot. Failed TQI-B4-point and 771 unattempted histories / 775 aliases stay U without IDs or accepted metrics. Annex and revision only: all 15 whole requirements, 6174 old IDs, 42 rows, R3–R12 objects, criteria/U/history and releases (27 evaluations / 35 objects) remain exact with full reversal. Strict return-zero / flags 0 or 1 remains unchanged; no opaque-policy transfer. Original zero-native and 5350-history / 5364-alias OLD ASOF snapshots stay exact. New native waveform expectations, portable criteria and grades remain NULL; application proof false. No quantizer, public/ARM or calibration law. |
| 14 | 2026-10-23 | Add771 finite supplied-history observations DTN-6384–7154/full775aliases under user-adopted15 signed64 opaque returns/all other guards unchanged. Annex+revision only/all15wholeREQ/6383oldIDs42rows/R3–R13objects/981985OLDASOF/failedTQI-B4-pointU/5350OLDASOF5364/releases27eval35inventory/fullreverse; no quantizer/return/flag/publicARM law or portable criterion. |
| 1 | 2026-10-18 | First draft from packet t12-tension-v1. 15 requirements: 13 X (001, 003 to 014), 002 S with X clauses, 015 X with U parts. U parts in 001, 002, 005, 006, 007, 011, 012, 014 and 015; one S-cond clause (003, A2). 42 cases: 27 graded by retained X renders, 12 check cases graded by exact values, 3 not graded (DTN-040 to 042) |
| 2 | 2026-10-19 | Stage 27 finite protocol-conditioned outputs (26 stable, one repeated strike), restricted to settings with retained per-setting sensitivity studies. Freeze measurement windows, mode centers and reference amplitude normalization. Exclude four chaotic settings and 37 outputs without per-setting calibration. Clarify that directed-rounding sensitivity is not an arm64 bound. Parent requirement/case IDs unchanged. |
| 3 | 2026-10-21 | Reconcile the approved whole-eleven-set retained report with exact source selectors and explicit custody/input limits. Preserve all 42 case rows and add no fixture IDs or calibration criteria. Qualify ungated DamperVelocity as U without an exact joined input/result; keep pickup-37-frame and velocity-1 claims on their separate prior render evidence rather than broad report pointers. The 239 report projections remain navigation only; 27 released evaluations and four chaotic/37 uncalibrated exclusions are unchanged. |
| 5 | 2026-10-21 | Add 125 finite default velocity-byte observations DTN-043–167 and three inherited references/full 128-point catalog. Append bounded REQ-003/007 qualifications; preserve 13 other whole bodies, both old prefixes, 42 rows/IDs, R3/R4 objects and 37-setting sensitivity annex, U/metrics/tolerances and 27 released evaluations. Parent launch source not pre-call file-bound; outer receipt/raw fsync unproved. Portable expected/comparator/grade NULL. |
| 6 | 2026-10-21 | Add 123 finite default note-key observations DTN-168–290 and five inherited references/full 128-point catalog. Append only REQ-003 finite qualification; preserve 14 other whole bodies including REQ-004/007, old003 prefix, 42 rows/167 IDs, all R3/R4/R5 objects and sensitivity/velocity qualifications, U/metrics/tolerances and27 released evaluations. New note-key launcher pre-call bound does not repair older velocity launcher gap. Portable expected/comparator/grade NULL; no general key/pitch/public/ARM/calibration law. |
| 7 | 2026-10-21 | Add106 finite native-host observations DTN-291–396 and11 historical input references/full117-vector164-alias catalog of48 nonvirtual kind3 domains. Append only REQ-002 bounded qualification; host91=5 auxiliary/nonapplication, other emission/current/public joins unproved. Preserve14 other whole bodies/old002prefix,42rows290IDs,R3–R6maps/catalogs,oldannexes/U/tolerances/release27+35. Older velocity launch gap remains; freshpriors/portablecriteria/gradesNULL, no general DSP/calibration/publicARM law. |
| 8 | 2026-10-21 | Add142 finite MIDI-axis observations DTN-397–538,15 matchingchannels plus127 Offbytes, full143history144alias catalog/sharedDTN001 baseline inherited without replay. Append ONLY bounded REQ003 qualification; preserve14otherwholebodies/002/old003prefix/42rows396IDs/R3–R7 objects/criteria/U/history/release27+35 exact, full reversal. Native finite equality supplies no portable comparator/public/ARM/general law/calibration or new application proof. |
| 9 | 2026-10-21 | Add284 finite independent On/Off key/channel observations DTN-539–822/full288alias285WHOLEhistory catalog, oneDTN001INPUTref/fourbaselinealiases/no replay/newmetrics/criteriontransfer. AppendONLYboundedREQ003; preserve14otherwhole inclENTIREREQ002R7/old003R8prefix/42rows538IDs/allR3–R8objects/criteriaU/history/auxiliary91=5/velocityparentgap/releases27eval35inventory exact/fullreverse. Quiet002003/finitewordfacts descriptiveonly, NULLpriorsportablecriteria/grades/newappFalse/no unmatchedrelease/publicARM/calibrationlaw. |
| 10 | 2026-10-21 | AddONLY1388 finite partial stepped observations DTN-823–2210/full5350histories5364aliases, ONE INPUTbaseline15aliases/onefailedU3960unattemptedU NOIDs/expectations/grades. Annex+revisionONLY/all15REQexact/822oldIDs42rows/R3–R9objects/37sensitivity31vs6/aux91=5/quiet002003/oldparentgap/releases27eval35inventory/criteriaU/fullreverse; failedexit0notpass/no retry/continuation/guardrelaxation/nativecause/publicARM/calibrationlaw. |
| 11 | 2026-10-21 | Add4finite rate/block observations DTN-2211–2214/full6hist7aliases; oldfailed64U/baselineINPUTonly and R10failed+3960U unchanged/no retry. Annex/revision ONLY/all15wholeREQ2210oldIDs42rows/R3–R10objects/criteria/history/releases27eval35inventory/fullreverse exact. Future initializerDATAone260c0 only/ret0flag01allguardsunchanged/NOdesign13adoption; nativewaveformexpectationsportablecriteriaGradeNULL/appFalse. |

The [finite handoff plan](device-tension-handoff-plan.md) records the released
enumerated output portions of REQ-001 and 004 to 012 for 27 retained, calibrated settings.
It uses explicit comparison-domain inputs without accepting A1/A2 as claims about Live.
Chaotic settings receive no statistical substitute, and uncalibrated settings stay outside
the candidate. The broader formulas, checks, timing, voices, modulation and stored-value
mapping in this draft remain unreleased. Independent review accepted only that finite metric and sanitized fixture scope,
with explicit nonempty, finite, shape and required-measurement guards in the
comparator. The finite package is published locally; restricted workspace provisioning
remains a prerequisite for implementation. The reviewed scope and limits are in
the linked plan.

Released locally 2026-10-19 as [device-tension-v1](../../handoff/device-tension-v1/README.md):
27 calibrated finite output evaluations only. Four chaotic settings and 37
uncalibrated outputs are excluded. See the [handoff plan](device-tension-handoff-plan.md#local-publication).

Revision 3's retained-report annex remains an analyst draft, not released
implementation input. It does not rewrite any release or approve the earlier
unreleased check tolerances. New owner qualifications require bounded owner
review; the approved report joins and released finite metric need no repeated
review. Missing required evidence remains open.

## Tension guarded getter qualification — 2026-10-21

[The twelve-byte table/getter review](../research/device-tension-dsp.md#tension-guarded-table-and-own78-word-adoption--2026-10-21) establishes four guarded arithmetic branch nominations and raw own+0x78 nominee 0x3ddc only. Saved N, packed return and current child remain distinct; absence of a producer classification is not proof of absent allocation or mutation. Runtime/class/ABI/public/named63/Damper behavior stays U. No cases, grades, releases or main-image sites are added; frozen 691 X / 1,076 S / 3,857 none and main 25,071+24=25,095 of 268,015 remain unchanged, with bundle sites separate. Coverage remains OPEN.

## Whole getter qualification — 2026-10-21

[The complete nominated getter](../research/device-tension-dsp.md#tension-own78-getter-body-adoption--2026-10-21) conditionally returns32 with no local memory access or call. It proves neither actual own+0x78 invocation nor a public return meaning, child identity or general behavior. Saved/current receiver distinctions remain. No cases, grades, releases or main-image sites are added; required U/product OPEN.

## Finite sensitivity evidence qualification — proposed revision 4

The [222-child batch](../../analysis/ableton-live-12.4.3/full-spec-v1/batch-tension-uncalibrated-sensitivity-v1/manifest.json)
passed its [sole actual/source review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/tension-uncalibrated-sensitivity-v1-review.json)
for bounded finite observations. It retains a fresh unperturbed control and the
five stated perturbations for each of 37 settings without a prior per-setting
sensitivity study. All captures use 44,100 Hz, 44,100 frames and 512-frame host blocks.
Each input retains the exact prior 129-component parameter vector and full
original event and command script, with only the historical MXCSR command
insertion in rounding variants. All 37 fresh controls match the prior
raw-output hashes; both channels of all 222 captures are finite and identical.
The complete 444 channel comparisons retain the prior estimator windows recorded
under the historical `held/window` key, together with the prior partial centers,
floors and normalization. These are zero-based full-render estimator parameters,
using the same coordinates as the supplied MIDI events. The retained method
initially requests reference onset plus 2,048 through note-off. Its threshold
can shorten the end, and it clamps the start with
`max(0, min(requested_start, end - 4096))`. For `str_damp_0`, the stored interval
`[3903,7999)` consequently starts before the supplied note-on at 4096
(note-off 26146); this is not a different event-coordinate convention.
`fit.track` applies its own FIR tap-settling selection and group-delay
correction. The `held` label does not guarantee that the stored interval lies
wholly inside a physically held or settled phase. Retaining these frozen
parameters neither re-centers or re-fits them nor validates generic physical,
calibration or candidate-measurement assumptions. These are finite x86 extracted
observations under the recorded substituted libraries, not ARM or Apple bounds,
physical calibration, actual Live A1/A2 behavior or a general signal law.

The [37-row mapping](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-tension-r4-sensitivity-v1/adoption-map.json)
joins each existing case and primary requirement to all inputs and complete
metric records. The table below compares the maximum deviation from the fresh
same-setting control over all five perturbations and both channels with the
existing proposed quarter-tolerance margins: held 7.5 × 10⁻⁴, release
2.5 × 10⁻³, frequency 5 × 10⁻⁷, log radius 1.5 × 10⁻⁴ and complex amplitude
1.25 × 10⁻⁴. This arithmetic introduces no tolerance or acceptance criterion.
A recorded numerical margin is not an accepted stable class or release
eligibility. A margin not met leaves eligibility unresolved; it does not
classify a setting as physically chaotic or admit a statistical substitute.

| Setting | Existing case | Primary REQ | Held rel RMS | Release rel RMS | Frequency rel | Log radius rel | Complex amplitude rel | Proposed numerical margin |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `body_mix_1` | DTN-023 | 011 | 3.16792297039e-05 | 0.0001886992214 | 9.54400225517e-10 | 2.53576877691e-05 | 1.64068318376e-06 | meets proposed numerical margin for captured class |
| `body_size_0` | DTN-023 | 011 | 1.72042995077e-05 | 0.000228142705639 | 5.51389156556e-09 | 2.5704146881e-05 | 2.02267110993e-06 | meets proposed numerical margin for captured class |
| `body_size_4` | DTN-023 | 011 | 7.24388038135e-06 | 0.000225213772094 | 1.8249159961e-09 | 2.53676958839e-05 | 1.34735185402e-06 | meets proposed numerical margin for captured class |
| `body_type_0` | DTN-022 | 011 | 8.93329856094e-06 | 0.000226543316603 | 9.06080210861e-10 | 2.53752367343e-05 | 1.42505549537e-06 | meets proposed numerical margin for captured class |
| `body_type_3` | DTN-022 | 011 | 8.23195038731e-06 | 0.000219864889304 | 1.7211694292e-09 | 2.5412033491e-05 | 1.39427389939e-06 | meets proposed numerical margin for captured class |
| `damper_pos_0` | DTN-017 | 008 | 1.46964671213e-06 | 0.000231178145997 | 6.40431607746e-09 | 2.34694075418e-06 | 1.123242032e-06 | meets proposed numerical margin for captured class |
| `filt_base` | DTN-024 | 012 | 0.000571366834323 | 0.00115036719389 | 3.4996817766e-07 | 3.91661282597e-05 | 2.06117816507e-05 | meets proposed numerical margin for captured class |
| `filt_t0` | DTN-024 | 012 | 8.29853774531e-05 | 0.000323280009547 | 3.55767362348e-07 | 9.99452832855e-05 | 1.41398163451e-05 | meets proposed numerical margin for captured class |
| `filt_t1` | DTN-024 | 012 | 8.91113437483e-05 | 0.000328003471282 | 3.54537418201e-07 | 9.28639427088e-05 | 1.62922619783e-05 | meets proposed numerical margin for captured class |
| `filt_t1_c0.25` | DTN-025 | 012 | 7.14892811914e-05 | 0.000299549658195 | 3.62518961627e-07 | 0.000321521467201 | 3.6858145941e-05 | margin not met; eligibility unresolved |
| `filt_t1_c0.75` | DTN-025 | 012 | 0.00018065505458 | 0.00045965320057 | 3.50087274392e-07 | 4.05387024629e-05 | 1.86970367181e-05 | meets proposed numerical margin for captured class |
| `filt_t1_q0.5` | DTN-025 | 012 | 0.000289802262399 | 0.000651986105032 | 3.50148550377e-07 | 4.13510972502e-05 | 5.50159633815e-05 | meets proposed numerical margin for captured class |
| `filt_t2` | DTN-024 | 012 | 0.000539021289181 | 0.00110850106493 | 3.5060551673e-07 | 4.62470269791e-05 | 2.41516656765e-05 | meets proposed numerical margin for captured class |
| `filt_t3` | DTN-024 | 012 | 0.000525680330308 | 0.00109135845221 | 3.50517228798e-07 | 4.70154317416e-05 | 2.83467316006e-05 | meets proposed numerical margin for captured class |
| `filt_t4` | DTN-024 | 012 | 0.000645930055719 | 0.00125222275856 | 3.57425346986e-07 | 0.000451569127593 | 1.41966159901e-05 | margin not met; eligibility unresolved |
| `filt_t5` | DTN-024 | 012 | 0.000713985397331 | 0.00135134589842 | 3.69968419234e-07 | 0.000544374811749 | 2.69183029284e-05 | margin not met; eligibility unresolved |
| `filt_t6` | DTN-024 | 012 | 0.00356088511348 | 0.00708128675605 | 3.53510992257e-07 | 4.72811886004e-05 | 0.000100355587732 | margin not met; eligibility unresolved |
| `filt_t7` | DTN-024 | 012 | 0.00327490093718 | 0.00651507574043 | 5.05372568571e-07 | 0.000461960087759 | 0.000125137644663 | margin not met; eligibility unresolved |
| `filt_t9` | DTN-024 | 012 | 0.000250853946956 | 0.000503448685803 | 3.82944453148e-07 | 0.000807291275269 | 0.000135659396905 | margin not met; eligibility unresolved |
| `ham_damp1` | DTN-012 | 006 | 7.54040373117e-06 | 0.000223777850329 | 3.06932790295e-09 | 2.51378163241e-05 | 1.55148758203e-06 | meets proposed numerical margin for captured class |
| `ham_stiff1` | DTN-012 | 006 | 7.37418100412e-06 | 0.000224264890228 | 1.62382729485e-09 | 2.51905608197e-05 | 1.58952657288e-06 | meets proposed numerical margin for captured class |
| `note_48` | DTN-004 | 004/005 | 9.6287975316e-05 | 0.00019352035191 | 2.36902208073e-07 | 1.40070917725e-05 | 1.06283556597e-05 | meets proposed numerical margin for captured class |
| `note_72` | DTN-004 | 004/005 | 0.000219464454886 | 0.000742142485477 | 3.53220086735e-07 | 2.50315842816e-05 | 4.52993588718e-05 | meets proposed numerical margin for captured class |
| `pickup_pos_0` | DTN-020 | 010 | 6.23312350891e-06 | 0.000224787599721 | 6.95429824837e-10 | 2.52798462228e-05 | 1.40276483933e-06 | meets proposed numerical margin for captured class |
| `plk_damp0` | DTN-011 | 006 | 7.24241665542e-06 | 0.000227931294558 | 6.62182086941e-10 | 2.53411341757e-05 | 1.24844214787e-06 | meets proposed numerical margin for captured class |
| `plk_stiff0` | DTN-011 | 006 | 7.26002790368e-06 | 0.000226927345411 | 2.08763217824e-09 | 2.53855631056e-05 | 1.23752830692e-06 | meets proposed numerical margin for captured class |
| `plk_x0` | DTN-011 | 006 | 6.88324148584e-06 | 0.000222895551692 | 9.67229074611e-10 | 2.53053649322e-05 | 2.195148421e-06 | meets proposed numerical margin for captured class |
| `pos_0` | DTN-013 | 006 | 6.48275479571e-06 | 0.000227632570189 | 1.09623221611e-09 | 2.54065648557e-05 | 1.24407474796e-06 | meets proposed numerical margin for captured class |
| `str_damp_0` | DTN-014 | 005 | 7.39931908442e-07 | 0.000228002043784 | 2.81631651333e-09 | 2.43397921595e-07 | 8.19548003039e-07 | meets proposed numerical margin for captured class |
| `str_damp_1` | DTN-014 | 005 | 7.77993518902e-06 | 0.000230473077241 | 2.93968183129e-10 | 3.06521430029e-05 | 1.21928074388e-06 | meets proposed numerical margin for captured class |
| `str_decay_0.25` | DTN-014 | 005 | 1.09599433464e-06 | 1.69598405099e-05 | 1.7123433782e-09 | 1.04988106786e-06 | 1.7319368105e-06 | meets proposed numerical margin for captured class |
| `str_inharm_0` | DTN-016 | 005 | 6.73369847066e-06 | 0.000222429244787 | 3.6834342243e-09 | 2.52064044046e-05 | 1.618814244e-06 | meets proposed numerical margin for captured class |
| `str_ratio_0` | DTN-015 | 005 | 7.14608192821e-06 | 0.00246223796686 | 1.40746925226e-09 | 2.53889066326e-05 | 1.22726577282e-06 | meets proposed numerical margin for captured class |
| `term_force_0` | DTN-019 | 009 | 6.63890674682e-06 | 0.000198623074314 | 3.41087151856e-08 | 7.50021799045e-06 | 3.1846670612e-06 | meets proposed numerical margin for captured class |
| `vel_1` | DTN-005 | 007 | 7.12366386544e-06 | 0.000226196311616 | 1.2066577737e-09 | 2.54084477624e-05 | 1.25156599421e-06 | meets proposed numerical margin for captured class |
| `velmod_1` | DTN-006 | 007 | 7.12366386544e-06 | 0.000226196311616 | 1.2066577737e-09 | 2.54084477624e-05 | 1.25156599421e-06 | meets proposed numerical margin for captured class |
| `velmod_64` | DTN-006 | 007 | 7.34308507271e-06 | 0.000221754445022 | 1.20305854168e-09 | 2.53661640042e-05 | 1.50648348014e-06 | meets proposed numerical margin for captured class |

The 31 rows meeting the proposed margins and six unresolved rows are all
retained. The unresolved rows are `filt_t1_c0.25`, `filt_t4`, `filt_t5`,
`filt_t6`, `filt_t7` and `filt_t9`. Even the full proposed stable tolerances
are exceeded by held deviation for `filt_t6` and `filt_t7`, and log-radius
deviation for `filt_t9`; no threshold is raised and no result is rounded into
eligibility. The linked JSON retains full values and every maximum's variant,
channel and exact record pointer; displayed numbers are descriptive.

The unchanged “Stable metric” labels in parent rows DTN-024 and DTN-025 are
pre-existing draft proposals. This annex does not endorse their applicability
to `filt_t1_c0.25`, `filt_t4`, `filt_t5`, `filt_t6`, `filt_t7` or `filt_t9`,
or validate all other parent-case assertions. Stable-metric eligibility for
these six remains unresolved; no chaotic or statistical comparator substitutes
for that decision. Their complete records and all 42 historical case rows
remain intact.

This supplies the missing per-setting five-way evidence for the captured
inputs, subject to the sole actual review's custody and method limits. It
does not supply untested pairwise spreads, general parameter/rate behavior,
new calibration decisions, public receiver or output joins. The old baseline
format reconstruction does not fabricate missing historical execution receipts.
MXCSR variants begin after parameter setting and apply to processing and
teardown; the libm variants act from loading and initialization. They are not
identical whole-program perturbation scopes. The libm wrapper selects results
with `r != rint(r)` (or its float form); this does not prove that every
mathematically inexact result or every library operation is covered.

All 15 requirement bodies and 42 existing case rows and IDs remain unchanged.
REQ-008's ungated DamperVelocity remains U; `damper_pos_0` is not that missing
parameter comparison. `pickup_pos_0` remains DTN-020 and supplies no new
DTN-021 position-0.5/37-frame evidence. Old NULLs, check-custody qualifications,
all other U and broad proposed criteria remain. The 27 released finite
evaluations and four chaotic exclusions are unchanged. All 37 settings in
this annex remain outside the published handoff; no release, new case ID,
statistical substitute or implementation input is admitted here.

## R14 finite remaining declared-quantization observations — 2026-10-23

DTN-6384–7154 add771 native observation-only histories/775 recipe aliases under
REQ-001 from the
[sole approved summary](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/tension-declared-quantization-unlaunched771-opaque-v1-review.json)
(47,574,803B; SHA256 `20f0f9a66a43af36d4b09f2e9c94fa3ce44aa656cb6b35531ca6b4f5ba765b09`).
The [owner mapping](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-tension-r14-declared-quantization-opaque-finite-v1/mapping.json)
retains all771 exact inputs,775 aliases, new signed64/RLE projections, receipt
pointers, policy and full old981/985 as-of dispositions. IDs follow the sole
approved point order: DTN-6384 is TQI-B4-lower; DTN-6385–7154 are the770 supplied
position histories. Duplicate aliases do not receive duplicate observation IDs.

Every previously native-launched member is excluded, including failed
TQI-B4-point. The first new lower input is a different exact supplied history,
not a replay, substitute or retrospective acceptance of that failed point.
Original zero-native981U and the later strict981histories/985aliases snapshot
remain exact old scope:209 approved/one failed/771unattempted. These separate
new771 observations supplement that snapshot without rewriting its unattempted
fields. Old5350OLD-ASOF/5364aliases,1388 accepted/failedU1389/baseU0255/failed64,
prior R12/R13 objects and original source/parent/fsync/history gaps remain intact.
No old PID, output, receipt, metric, oracle or criterion transfers or repairs.

All129 original ordered decimal/f64/f32 words and exact source scripts/events
are retained; no setter is supplied for index2. Each uses8192frames/44100Hz/
block512/zero input/flag0/no warmup. Late Off timestamps remain literal, without
clipping or recentering; public event delivery/exclusion is not established.
C.UTF-8/TIME0/LIBM-unset/default-entryFP is a supplied current context, not
historical environment/source-to-executed-version/current-receiver/provider/
input-register/FP/OSexec equivalence. Source lower/point/upper and position labels
are INPUT recipes, not recovered native quantizer or within-cell boundaries.
No reset, transport, MXCSR, producer, provider, model, build or construction is
introduced. The old supplied_context ret0 guard label remains exact input-hash
metadata only; the separate new collector policy governs this packet. A supplied
history hash does not establish native history equivalence across policies.

User-adopted revision15 changes ONLY this new CalcA return admission to logged
signed64 integer projections with exact ordered run lengths/values/flags, without
requiring zero or0/1 or assigning a native ABI/domain/void/benignness/success/error/
cause/flag meaning. Flag0or1 and all other exit/stderr/trap/fault/CXX/initializer/
import-binding-versus-counted-use/parameter/event/order/frame/shape/both-channel-
finite/custody/timeout/resource/cleanup guards remain unchanged. No design13
scope transfer, generalized return policy or changed frozen strict guard follows.
Literal new counts12,328 zero+eight one/all12,336 flags1 are descriptive only.
The eight ones occur in the new TQI-B4-lower second eight-block run, not in a
replayed failed point, with no causal, parameter-equivalence or return-meaning
inference and no restriction of the opaque policy to the observed values.

All771 approved outputs are finite, nonzero in BOTH channels and stereo-word
equal;382 hashes and76 counted Linux CODE names are descriptive, not musical,
physical, effect, symmetry, quantizer, within-cell or public/ARM laws. All new
waveform priors/native expectations/portable expected/comparators/grades remain
NULL; new application predicate proof is false. Existing criteria/windows/metrics/
tolerances are unchanged; no fit, f0, new metric/window or calibration is selected.

114,108 selected exports/12,336 CalcA exclude771 separately logged260c0
initializers; nested/all-native counts stay unknown.142 declared bindings
(109Linux/26trap/7data) and counted use do not prove absence of other global/data/
transitive/provider dependencies. Rate integers remain opaque.13,878 actual
per-child18 endpoint pairs plus two whole REPORT pairs match; endpoints and
source-level same-PID receipts are not continuous mapping/provider/FP/input-read/
OSexec or compiled-source proof. Raw/log/JSON fsync requests do not establish
directory/crash durability; outer redirects have no explicit FDfsync, and new
requests do not repair older skipped-fsync/parent gaps. Fresh4GiB+128MiB parent
floor and remaining raw/future metadata/final-review-owner/headroom guards are
unreserved estimates, not quotas or external-writer/current-child-overshoot/
escaped-child guarantees. Child20s CPU/wall/core0/FSIZE4MiB/DEVNULL/newgroup and
cleanup-source limits remain; all new children exited, so cleanup was unused.

Only this annex and revision/date metadata change. All15 whole requirements,
6,383 prior IDs,42 old rows,R3–R13 objects,old Acceptance/annex/navigation/U/
criteria/tolerances/state/history and37 sensitivity settings(31margins/sixU),
quiet002/003,auxiliary91=5,old velocity-parent gap and all prior as-of scopes stay
exact.27 released evaluations/35 inventory entries are unchanged. Full reversal
restores R13. The resulting7,154 navigation IDs are not passes or a product
denominator; unsupported required behavior stays U and whole-Live coverage OPEN.
No new portable criterion, grade, site, release, implementation input, observedO
or general native/public/ARM law is admitted.
## R15 finite five-group supplied timing observations — 2026-10-23

**Analyst draft: 1087 additional native observations only.** DTN-7155 through DTN-8241
join the exact sole-approved TIMING-0001–1087 order, one navigation ID per
approved history and alias, through the [complete compact owner mapping](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-tension-r15-declared-timing-finite-v1/mapping.json).
REQ-003 is navigation context only. The resulting 8,241 navigation IDs are
not passes, a family denominator or a general timing requirement admission.

The only new observation authority is the [independent five-group review](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/tension-declared-timing-five-groups-v1-review.json),
145,056,541 bytes / SHA256 `51d4b483abf929c9fd06cf90cbc62e06b46980766c608e0ca42cad7b8de0cba4`.
Each new case retains its exact REPORT JSON pointer and canonical SHA256
of the complete approved point, with original whole supplied INPUT/script
hashes, alias/group and necessary scalar references. The 1,209,831 actual
custody pairs remain in that canonical REPORT rather than being duplicated
in owner objects. This is a new wording/mapping/preservation composition,
with no second actual/source/raw/numeric/provider or release-fixture proof review.

All five declared groups are retained: 560 ON-primary, five OFF-held-control,
500 OFF-sweep, ten velocity0-ON and twelve excitator-type/velocity histories.
The exact 1087 aliases, source order, literal defaults/omissions, full 129
original decimal/f64/f32 parameter words, absolute events, script arguments,
frames and current supplied contexts remain linked without clipping,
recentring, parameter-only deduplication or silent normalization. Index2 has
no setter. There are 572 supplied 4096-frame histories and 515 supplied 8192-frame
histories; both use the recorded block 512 geometry. No warmup or new event
construction, reset, transport, MXCSR, model, provider, build or FP treatment
is added. Predicted-grid and source-ys-truthiness-conditional groups remain
symbolic/excluded; this annex adds no arbitrary grid or continuous crossproduct.

This class uses STRICT CalcA return0/flag0or1 and every other existing guard.
All 21,356 captured CalcA returns are literal0 and their flags literal1. Those
facts satisfy the selected parser, without establishing native ABI, domain,
success/error, cause, activity or flag meaning. User-adopted D08/D09 and the
older design13 opaque-return policies do not transfer to these histories.
Rate integers remain opaque. All 1,087 accepted outputs are finite, nonzero
in BOTH lanes and stereo-word-equal; 61 hashes and 79 counted used-Linux CODE
names are descriptive references only. No onset, Off, grid, zero-velocity,
Damper, gate, excitator, equality, waveform, pitch, capacity, stability,
quantizer, physical or public/ARM law, new metric/window/tolerance, fit,
f0 or calibration follows. Every fresh prior/native waveform expectation,
portable expected/comparator and grade remains NULL; application proof is false.

The supplied context is minimal C.UTF-8/TIME0/LIBM-unset/default-entryFP,
zero audio/input flag0/no warmup and the unchanged admitted Tension model.
Source env=None/ambient historical execution, original executed-source,
current receiver, loaded provider, actual FP/input registers, native ABI,
OS execution and public behavior equivalence remain unknown. The exact
1087 current contexts do not validate the historical source producer or
repair any source/default/environment bridge.

164,840 selected direct exports and21,356 CalcA exclude 1,087 separately
logged 260c0 initializers; nested/all-native work remains U. The 142 declared
bindings (109Linux/26trap/7data) are distinct from counted CODE use, without
absence claims for uncounted/data/global/transitive dependencies. Custody
is 1,113 applicable file identities before/after EACH child, 1,209,831 pairs,
plus five REPORT-authority pairs. This is not a common-initial-only count,
continuous loaded mapping/provider/FP state, OSexec or compiled-source proof.
Successful raw/log/JSON FDfsync requests do not establish directory/crash
durability; outer redirect FDfsync is not explicit and older skipped-fsync
or parent gaps are not repaired.

Full resource guards retain the 4GiB+128MiB floor and recompute the larger
complete remaining raw/worst stdout-stderr/future metadata/final-review-owner/
headroom requirement, including a 268,435,456-byte concurrent allowance; the retained larger initial requirement
is10,252,910,592 bytes. These are unreserved estimates, not quotas, reservations
or external-writer/current-child-overshoot guarantees. Child CPU/wall 20s,
core0/FSIZE4MiB/DEVNULL/newgroup and cleanup-source limits remain; the parent
has resource guards but no wall watchdog. Exited recorded children do not
prove absence of unobserved or escaped descendants.

The prior 981 exact-script cut has zero matches; older 68 and R4–R12 process
44100/48000 geometry differs from new 4096/8192. These are bounded INPUT
comparisons, not global never-run or historical execution equivalence.
No old PID, output, receipt, metric or criterion is transferred. Prior
981 histories/985 aliases original-zero-native and strict ASOF snapshots,
failed TQI-B4-point, original failed U1389/baseU0255/failed64,
5350OLD-ASOF/5364aliases, older accepted/unattempted labels and D08 suffix
remain exact separate histories, without replay, substitution, new grade,
repaired guard or retrospective acceptance. The earlier R14 13,878-pair
custody scope remains that older packet's scope, not the new count.

Only this annex and the revision number change; the date is already2026-10-23.
All 15 whole requirements, 7,154 prior navigation IDs, 42 literal rows,
R3–R14 objects, old Acceptance/annex/navigation/criteria/U/state/history,
37 sensitivity settings (31 margins/six U), quiet 002/003, auxiliary 91=5,
old velocity-parent gap and all previous ASOF/release/return-policy scopes
remain byte-exact. The immutable release retains 27 evaluations/35 inventory
entries. Full reversal restores the exact 120,807-byte R14 baseline.
No new portable criterion, grade, site, release, implementation input,
observed O or whole-product closure is admitted. Required unsupported
behavior remains U and whole-Live coverage OPEN.

## R16 finite current-supplied remaining-check observations — 2026-10-23

This annex records **737 accepted finite observations**, navigated by **DTN-8242–DTN-8978**, from the sole-approved [partial current-supplied report](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/tension-remaining-checks-current-supplied-v1-partial-review.json) (87,377,774 bytes; SHA256 `57deae2defadad8c9613f15f556131fb824a2b6b5abae24134fa24c59fb00cc5`). The compact mapping in the [R16 owner proposal](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-tension-r16-remaining-checks-partial-finite-v1/mapping.json) joins every new ID to its exact approved report point, canonical point digest, input identity and aliases. These IDs add navigation for supplied-context observations; they add no portable waveform expectation, comparator, grade or application-predicate proof. All fifteen existing requirement bodies remain exact.

| Approved source method | New observations |
| --- | ---: |
| `determinism` | 19 |
| `pitch` | 33 |
| `level` | 9 |
| `polyphony` | 675 |
| `extremes` | 1 |

The capture's complete disposition remains **762 histories / 779 aliases**: 737 accepted histories (754 aliases), **TRCS-0738 failed/U**, and **TRCS-0739–TRCS-0762 unattempted/U**. Its 842 SOURCE slots separately retain twelve prior SCRIPT references and 51 whole dependency/FP gaps. The mapping includes all these dispositions; only accepted histories receive new IDs. Prior SCRIPT matches transfer no current-context PID, output, metric or criterion. The complete 5350 OLD-ASOF / 5364-alias snapshot remains historical and unchanged; later launched statuses remain separate. Subsequent candidate INPUT studies do not repair this capture's 51-gap ASOF record. This is a partial observation annex, not completion or global exhaustion.

The approved collector required **CalcA return zero and flags 0 or 1**, with all other guards retained. No opaque-return policy, D08, D09 or design 13 scope transfers here. It stopped at the first fault without retry. TRCS-0738 returned exit zero with empty stderr, but 49 consecutive CalcA return-one blocks starting at frame 4096 failed that strict guard. Its full 352800-byte diagnostic raw data is retained **without accepted-observation metric, expected waveform or case ID**. Native return ABI, meaning and cause remain unknown. The failed branch skipped raw FD fsync; stale RUNNING metadata with child end fields and outer exit 1 remain preserved. The remaining 24 histories were never launched in this packet; no continuation is selected by this annex.

The accepted observations include **four quiet histories** (TRCS-0017, TRCS-0018, TRCS-0053 and TRCS-0737) and **733 nonzero in both lanes**. All 737 had finite, word-equal stereo lanes; 305 distinct raw hashes and 76 counted Linux code names are descriptive only. They establish no productive-effect, voice/stealing, timing, pitch, event/reset, public Live or ARM law. All fresh waveform priors, native expectations, portable expectations/comparators and grades remain NULL; new application-predicate proof remains false.

The supplied C.UTF-8/TIME0 profile includes explicit clock overrides and no LIBM override. It differs from historical env=None and old LANG=C; entry FP remains an unmeasured model premise. The 737 logged 0x260c0 initializers are separate from 130646 selected exports and 33359 CalcA calls; nested calls remain unknown. Accepted raw FD fsync requests and log/JSON FD fsync requests do not establish directory/crash durability; outer redirected FDs lack explicit fsync. The 738 attempted children retain 803 endpoint identity pairs each (592614 total); endpoints do not establish continuous runtime/provider use, compiled-source identity, ABI or OS-exec attestation. Child 20-second CPU/wall, core-zero and 4 MiB file guards do not imply a parent watchdog or containment of normally exiting escaped descendants. Resource floors and future allowances remain unreserved, with external writers and overshoot limits retained in the approved metadata.

The original INPUT DATA tuple/list checker failure and additive post-materialization qualification remain historical ASOF; this later actual-check result repairs neither. The live checkpoint JSON read race, additive postcapture monitor and reviewer-only pair-assertion corrections remain disclosed, with no frozen/native change or retry. Full qualified limits and all old U/state/history/criteria, quiet 002/003, auxiliary 91=5, older velocity-parent gap, strict quantization snapshots, failed points, FTZ gaps and scoped return policies remain exact. The 27 release evaluations/35 inventory entries are preserved metadata, with no release-fixture review.

The baseline for this append is the current 127150-byte R15 owner, SHA256 `c96e99ab416c90f9e2cd4bd2e590e2a804dce99363e91e665b3d2cb16fde749e`. It is exactly the historical sole-approved 127151-byte target minus the recorded one final LF. R16 preserves that correction, all 8241 prior navigation IDs, 42 literal rows, all prior text except the revision field, and one terminal LF. Required unsupported behavior remains U and whole-Live coverage OPEN.

## R17 finite current-provided BRIGHT observations — 2026-10-23

This annex adds **13 finite X observations**, **DTN-8979–DTN-8991**, from the
[sole-approved current-provided partial report](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/tension-candidate-provided41-current-supplied-v1-partial-review.json),
5,134,462 bytes / SHA256 `280a7943a4de028004a291d0c9e390a65de7a9f193d1c0835ad10f54472faf4a`.
The [complete R17 mapping](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-tension-r17-candidate-provided29-partial-finite-v1/mapping.json)
joins TCPB-002–TCPB-014 to their approved CASE/INPUT identities and 23 aliases.
Raw hashes are reference identities, not waveform expectations or portable
comparators. The receipt reference is the retained report record in results.jsonl,
not an invented separate receipt file. Root reviews only this new wording, ID
mapping and preservation; underlying actual/source/code/log/raw/numerical proof
is inherited from the sole review without replay.

All **41 provided aliases / 30 bound histories** remain represented: the 29
selected BRIGHT histories cover 40 aliases, and TCPB-001/defaults48 remains one
supporting reference with no replay or PID/output/metric/criterion transfer.
The partial run attempted 14 children once: 13 approved / 23 aliases,
**TCPB-015 failed U** / TCP41-022 alias, and **TCPB-016–TCPB-030 unattempted U** /
16 aliases. Only approved histories receive new IDs. Complete literal 129-word
arrays, scripts, events, frame/rate/block/default/omission order, supplied contexts,
original provided DATA and SOURCE alias relations remain in the mapping.
These are bounded supplied histories, not native uniqueness, global never-run,
a repair of the original 41/842/51-gap ASOF studies or product denominators.

Every accepted CalcA return projection is zero and its flag is one, satisfying
the unchanged strict return-zero / flags0or1 guards. Failed TCPB-015 has correct
process geometry and legal flags, but 58 consecutive return-one blocks starting
at zero-based block11/frame5632 reject that strict guard (RLE11zero/58one/18zero,
all flags1). Its exit0/empty stderr/no-timeout and finite word-equal diagnostic
352800-byte raw are not an accepted observation, expected waveform, metric or
case. Failed raw FDfsync was skipped. Return ABI, meaning, domain and cause stay
unknown; no retry, automatic continuation, policy repair or D08/D09/design13/15/16
opaque-return transfer follows. The unadopted D10 proposal remains parked.

The 13 approved histories account for 2,847 selected exports, 1,131 CalcA and
4,586,400 raw bytes, with 13 separately logged 0x260c0 initializers and unknown
nested work. All are finite, nonzero in both lanes and stereo-word-equal;
13 hashes and 76 counted Linux CODE names are descriptive only. They establish
no filter, BRIGHT, voice, output, productivity, physical/public Live/ARM law,
calibration, metric, tolerance or general behavior. Fresh priors, native waveform
expectations, portable expected/comparator/grade stay NULL; new application proof
is false. All 142 import declarations remain distinct from counted use.

The same admitted model and C.UTF-8/TIME0/LIBM-unset/default-entry-FP premise
remain qualified; no new model, provider, FP treatment or construction. Current
candidate import/physical SOURCE/executed-version, old envNone/default/context
and public equivalence remain unknown. Ten inherited missing-SCRIPT rows retain
NULL/U bridges and exact identity/role/provenance, without guessed scripts or
discarded records. Original reader KeyError/prebinding/code/trace remain;
additive V2 was prebound before the one complete binding target. Earlier DATA
serialization/reviewer corrections, 5350OLD/5364 aliases, quant981/985, timing1087,
prior738, all earlier failed/FTZ/cross-device/source gaps and scoped policies
remain their separate ASOF histories, without retrospective acceptance.

Custody retains 84 identity pairs for each of 14 attempts, 1,176 pairs total,
and two REPORT source pairs. These are discrete endpoints, not continuous
provider/FP/OSexec/source-to-compiled/ABI attestation. The identity helper follows
paths; final no-symlink files do not prove ancestor or continuous identity.
Accepted raw FDfsync progress follows recorded control flow/request, without a
separate syscall receipt; log/JSON requests and outer redirected FDs do not prove
directory/crash durability. Child20sCPU/wall/core0/4MiB/newgroup/DEVNULL limits do
not imply a parent watchdog or escaped-descendant containment. The full
4,697,620,480-byte minimum plus larger complete raw/future-log/metadata/final/
headroom/concurrent lifecycle allowances remains unreserved, not a quota or
external-writer/within-child/finalization-overshoot guarantee.

The author agent-capacity interruption is POST-capture coordination history,
not a native fault or prebound evidence; original sealed bytes were not amended.
Sole review continuation packaged the completed audit without rerunning capture,
owned checker, numerical audit or old proof. Only this annex and revision scalar
change. All15 whole requirements,42 literal rows,8,978 prior IDs/R3–R16 objects,
U/criteria/state/history, old ASOF gaps and immutable27release evaluations/35
inventory entries remain exact. Full reversal restores the 132327-byte R16
baseline, SHA256 `7e42d5a715d7634a94c4e09915b62f5374f17b60411859de2b490a2117e49fea`,
and one terminal LF. Current8,991 navigation IDs are not passes or a compatibility
percentage. No release, application grade or whole-product closure follows;
required unsupported behavior stays U and whole-Live coverage OPEN.
