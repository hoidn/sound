---
id: SPEC-DEVICE-ANALOG
type: spec
status: draft
updated: 2026-10-18
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3 / macOS; reference renders from the Analog.bundle x86_64 slice
---

# Analog instrument: signal behavior and reference renders

## Scope

Feature FEAT-DEVICES, T1 device audio ([ADR 0004](../decisions/adr-0004-target-scope-t1.md)).
User task: a MIDI track holds the bundled Analog instrument, and the offline render of its notes
must sound as Live's would. This draft specifies:

- the output Analog produces for timed note events and a set of stored parameter values, at
  44.1 kHz and 48 kHz;
- the reference renders that define that output for T1, and the protocol that made them;
- the comparison metric a candidate render must meet.

Storage of the 171 parameters (paths, domains, defaults) is
[SPEC-BUNDLED-DEVICE-PARAMETERS](bundled-device-parameters.md) r2. The note events a playing clip
sends, and when, are [SPEC-PLAYBACK-CORE](playback-core.md). Where the track's audio goes is
[SPEC-MIX-GRAPH](mix-graph.md).

Excluded, each with its effect stated in the requirement named:

- MIDI input other than note-on and note-off: pitch bend, controllers (mod wheel), channel
  pressure and MPE (REQ-023);
- glide, unison, the envelope loop, legato and free-run modes, and LFO sync (REQ-021);
- closed forms of the formant and 4-pole notch filters and of the random LFO shapes
  (REQ-012, REQ-018); these are graded only against reference renders;
- display text, CPU load and latency reporting.

Every requirement is a **proposed contract**. Nothing was run against Live, and under
[ADR 0003](../decisions/adr-0003-no-reference-execution.md) nothing will be. The audio evidence is
extracted execution of the shipped x86_64 Analog code. The Live-side parameter path is a static
derivation. Canonical evidence: [Analog DSP by extracted execution](../research/device-analog-dsp.md).
Formulas below describe the output signal. They are stated as behavior, and none is a
transcription of the device's code.

## Evidence labels

| Label | Meaning |
| --- | --- |
| D | Documented in shipped bytes: the schema, the shipped presets and the bundle's export table |
| S | Static derivation from the 12.4.3 executables; not an observed run |
| S-cond | A static derivation that holds only under the named assumption (A1, A2 below) |
| X | Extracted execution: the shipped x86_64 Analog slice was run on the stated inputs in the harness of [ADR 0003](../decisions/adr-0003-no-reference-execution.md#extracted-execution-of-original-code). It shows what the device code computes for those calls. It does not show that Live makes the same calls. The arm64 release slice is matched only by static comparison (appendix) |
| U | Unknown; no expected result, and not graded |

Only D, S and X clauses, and S-cond clauses whose assumption is accepted, may enter a release.
A U clause blocks the behavior it names. Each blocking U clause states its effect on T1.

## Terms

- **fs** is the sample rate. **P** = ⌊fs/1000⌋ is the control period: 44 frames at 44.1 kHz and
  48 at 48 kHz.
- **Grid point g′ of an event at frame f.** Let b be the first frame of the host block that holds
  f, and g = P·⌊f/P⌋. Then g′ = g if g ≥ b, and g′ = g + P otherwise. Frames are counted from the
  first frame the instance processed.
- **Host value v** is the value sent to the device for a parameter index (REQ-002).
- **Controller value c of a host value v in 0..1:** c = 128v for v ≤ 0.5, else 126v + 1, in binary32.
- **Curves of c**, used throughout. Each names its range lo..hi:
  - lin(lo, hi) = lo + n·(hi − lo), with n = 0.5 when c = 64 and n = c/127 otherwise.
  - exp(lo, hi) = lo·(hi/lo)^(c/127). exp0 is the same, except that c = 0 gives 0.
  - sq(lo, hi) = lo + n²·(hi − lo), with n as for lin. 4n² at c = 64 is therefore exactly 1.
  - "n" alone below means lin(0, 1).
- **A(x)**, the device's 2ˣ: A(x) = 2^⌊x⌋·(1 + t + t²(0.5 + 0.200064t)), with
  t = (x − ⌊x⌋)·ln 2, in binary32. A is exact at whole numbers and up to 1.34 cents high between.
- **S(φ)**, the device's quarter sine: S(φ) = 6.094263φ + 6.094263φ² − 85.31969φ³ + 121.88526φ⁴ −
  48.754105φ⁵, for 0 ≤ φ ≤ 1/4. S(1/8) = 0.718635.
- **Internal level** is the signal before the amplifier. A sine oscillator at level gain 1 and
  balance gain 1 has internal amplitude 0.6987.

## Assumptions

| ID | Assumption | What rests on it |
| --- | --- | --- |
| A1 | Live sends each stored value as REQ-002's host value. The index order and conversions are N6's static reading (S); the chain from stored value to the call is inferred | REQ-002; every case for stored values |
| A2 | Live drives the device like the reference protocol of REQ-001. It creates the instance, sets the rate, sends all 203 values and processes continuously in host blocks of 512 frames. Event frames are 0-based offsets within the block. Live's call order is static (S). The frame base, block sizes and grid phase are unknown | REQ-001, REQ-004; every case |

## Requirements

### REQ-DEVICE-ANALOG-001 — reference renders define the output

- **X.** For T1, Analog's output for a list of timed note events and a set of host values is the
  reference render made with this protocol:
  1. a new instance is created;
  2. the sample rate is set (44,100 or 48,000 Hz);
  3. all 203 host values of REQ-002 are sent, in index order;
  4. processing starts at the first frame, in host blocks of 512 frames, with silent input and the
     input flag 0;
  5. events are 16-byte records {frame, status, key, velocity} at absolute frames, delivered in the
     block that holds them;
  6. the transport is not playing (position 0, 120 BPM).

  Both output channels are identical in every reference render, so references are mono binary32
  (IEEE-float WAV). They are retained with their scripts and SHA-256 (cases below).
- **X.** The output does not depend on these, bit for bit:
  - the host block size, when the events fall on the same grid points (64, 256, 512 and 2,048
    tested; blocks of 333 move events by REQ-004's rule only);
  - flush-to-zero and denormals-are-zero;
  - the clock value that seeds the device's random generator, unless REQ-020 says otherwise;
  - a warm-up of 11,264 silent frames before the events. The output of the warm-up is exactly 0,
    and every later frame is bit-identical. This makes these references compatible with the
    warm-up protocol of [SPEC-DEVICE-ELECTRIC](device-electric.md).

  A re-run gives a bit-identical render.
- **S, U.** Live creates the instance, sets the rate and sends the values (S,
  [N5](../research/device-parameter-mapping-native.md#how-live-loads-a-bundle)). Unknown: when Live
  runs its reset sequence, which block sizes and event frame base it uses, and its grid phase.
  **Effect on T1:** note positions are sample-exact relative to the device's own grid only under A2.
- **X.** The device reports that it is sounding (its activity flag 1) for the first two host blocks
  after creation and while any voice sounds; otherwise 0. Whether Live stops calling the device on
  a 0 flag is U ([Q-025](../questions.md#q-025-device-host-protocol-and-device-audio-acceptance)).
  **Effect on T1:** none while notes sound.

### REQ-DEVICE-ANALOG-002 — from stored values to host values

- **S** ([N6](../research/device-tables-native.md#analog-ultraanalog-203-entries-31-second-outputs)).
  Live sends 203 host values. Index i corresponds to the stored parameter in N6's order (0
  Polyphony … 202 MpeCC74Amount2). Each stored value is first clamped to its domain
  (SPEC-BUNDLED-DEVICE-PARAMETERS). Then:
  - **Polyphony** sends max(v − 1, 0) on index 0, and 1 on index 7 when v > 0.5, else 0;
  - **Octave, OscillatorOct** send v + 3, and **Transpose, OscillatorSemi** send v + 12. All four are
    first rounded to the nearest 1/32768 and then truncated toward zero;
  - **NoiseBalance, OscillatorBalance** send 1 − v;
  - **FilterType** sends ⌊v⌋ >> 1 on its index and ⌊v⌋ & 1 on the next;
  - **the 28 bipolar amounts** (OscillatorEnvAmount, OscillatorLFOModPitch, OscillatorLFOModPW,
    Filter…Mod, Amplifier…Mod) send |v|, and 1 on the next index when v < 0, else 0;
  - **KeyboardUnison** sends v + 1 when KeyboardUnisonToggle is on, else 0. **LFOSync** does the
    same with its LFOSyncToggle, after the rounding above;
  - **the four ToggleDummy indices** (87, 99, 170, 182) send 1, and index 194 sends 48;
  - **Booleans** send 0 or 1, **enumerations** their index, and **every other parameter** the
    stored value, in binary32.
- **S.** `PerNotePitchBendRange` is stored but not sent.
- **S-cond (A1).** A stored Live Set value acts as the host value above.
- **D, U.** A new Analog either starts from the "Default when absent" values or loads the Defaults
  preset. They differ in 24 values, among them filter 1 on, oscillator 2 on and sustain 0.5
  (SPEC-BUNDLED-DEVICE-PARAMETERS REQ-009, U). **Effect on T1:** none for Live Sets, which store
  their values. Both starting points are rendered (DAN-001 to DAN-005). The preset is used as a
  parameter reference only.

### REQ-DEVICE-ANALOG-003 — controller values and curves

- **S, X.** Each host index acts in one of four ways (static map, appendix):
  - 104 indices clamp v to 0..1 and act through c and the curves of Terms;
  - 91 indices clamp to 0..max and act as an integer: enumerations, Booleans, Octave and Semi;
  - KeyboardDetune, KeyboardUnisonDelay, PitchBendRange, the DummyPerNotePitchBendRange and the
    MPE amounts act as floats in their range;
  - Polyphony and the MPE targets are handled separately.
- **X.** The curves are confirmed by the renders of REQ-006 to REQ-019. The c = 64 midpoint case of
  lin and sq applies where those requirements write n. Where a law is written with c/127 there is
  no midpoint case.

### REQ-DEVICE-ANALOG-004 — note events and timing

- **X.** Status 0x9n is a note-on and 0x8n a note-off. The channel n has no effect. A note-on with
  velocity 0 is a note-off. Release velocity has no effect. A note-off for a key that is not
  sounding changes nothing.
- **X.** An event at frame f takes effect at its grid point g′. The first output frame it can
  change is g′ + 1. A note-on therefore can sound up to P − 1 frames before its frame. The rule
  holds for 470 events: 250 note-ons from the
  [T1.2 gate](../research/device-dsp-extracted.md#analog-results), and 220 further note-ons and
  note-offs at both rates in blocks of 512, 64 and 333.
- **X.** Output before the first note is exactly 0. After every voice has ended it is exactly 0
  (REQ-016).
- **S-cond (A2).** With processing from the instance's creation in blocks of 512, a note-on at
  frame f first sounds at P·⌊f/P⌋ + 1. One period is added when that grid point lies before the
  start of f's block.
- **U.** Live's grid phase and event frame base, as for Electric. **Effect on T1:** onsets are
  sample-exact only under A2. A different phase moves onsets by 0 to P − 1 frames.

### REQ-DEVICE-ANALOG-005 — voices and polyphony

- **X.** Stored Polyphony 0 to 9 allows 1, 2, 4, 8, 12, 16, 20, 24, 28 or 32 voices. The default 3
  allows 8.
- **X.** A note-on beyond the limit takes the oldest voice. The stolen voice is silenced within
  about 2 ms, whatever its release time. The new note starts by REQ-004.
- **X.** With one voice (Polyphony 0) the held keys are remembered. KeyboardPriority chooses the
  key that sounds:
  - 0, highest held;
  - 1, lowest held;
  - 2, latest held (default). When it is released, the latest key still held sounds again.
- **X, U.** In mono, a key change while a key is held dips the output and restarts it: it falls to
  about 0.14 of its level within about 100 frames and recovers within about 300. The exact form
  is U. **Effect on T1:** mono key changes are graded only against DAN-040's reference with the
  envelope metric.

### REQ-DEVICE-ANALOG-006 — pitch

- **X.** A held key's oscillator frequency, with no modulation, is
  f = fs·A(p)/A(q), where:
  - p = ((key − 69)·s + 9 + Transpose + 12·Octave)/12 + fine;
  - s = lin(0.992, 1.008) of KeyboardStretch, acting only on the key's distance from 69;
  - fine = lin(−1/24, 1/24) octave of KeyboardFineTune;
  - q = L − 8.03136 − OscillatorOct − OscillatorSemi/12 − d;
  - L = log₂ fs, as binary32 (natural logarithm of fs times 1/ln 2);
  - d = ((c − 64)/64)²/4 octave for OscillatorDetune with c ≥ 64, and −((64 − c)/64)²/4 below.

  Octave, Transpose, OscillatorOct and OscillatorSemi are the integers of REQ-002.
- **X.** The renders agree with this within 5.4 × 10⁻⁶ in frequency (0.0093 cent) above 100 Hz,
  over 335 cases. The cases cover keys 24 to 108, every OscillatorOct and OscillatorSemi, Octave,
  Transpose, Detune, FineTune and Stretch sweeps, and both rates.
- **X.** Consequences:
  - C4 is 261.5371 Hz at 44.1 kHz and 261.4787 Hz at 48 kHz. A4 is 440.1927 Hz at 44.1 kHz.
  - The deviation from 12-TET follows the A(x) error over the octave from C, up to +1.34 cents at A,
    plus an offset of −0.585 cent at 44.1 kHz and −0.976 cent at 48 kHz.
  - Detune reaches −300.7 and +291.2 cents at its ends.
- **X, U.** KeyboardError adds a random offset per note, up to lin(0, 0.02) octave times a random
  factor (REQ-020). **Effect on T1:** sets with KeyboardError above 0 are graded for pitch only to
  ±lin(0, 0.02) octave.
- **U.** Pitch bend (REQ-023).

### REQ-DEVICE-ANALOG-007 — oscillator waveforms

Levels below are internal (Terms), at oscillator level gain 1 and balance gain 1.

- **X.** OscillatorWaveShape:
  - **0, sine:** fundamental amplitude 0.6987. Harmonics 2 to 6 lie at −37.9, −52.5, −54.4, −58.5
    and −62.4 dB re the fundamental, at every key tested.
  - **1, saw:** harmonic k has amplitude (1/(πk))·(1 + e), a sawtooth of ±0.5, band-limited. The
    excess e rises with frequency: +0.3 % at 523 Hz and +5.4 % at 7.8 kHz (C4, harmonics 2 and 30).
  - **2, rectangle:** a pulse of height 1, band-limited. Harmonic k is (2/(πk))·|sin(πkd)|·(1 + e)
    with the same kind of excess. Its duty is d = (c + 10)/274 of OscillatorPulseWidth: 3.65 % at
    0, 27.0 % at 0.5, 50 % at 1. Its mean is 0.8872d − 0.1818 (within 3 × 10⁻⁵).
  - **3, noise:** seed-dependent (REQ-020).
- **X.** PulseWidth has no effect on the sine and the saw.
- **X.** The waveform's phase at a note's start does not depend on the clock seed, so repeated
  renders are sample-identical.
- **X.** The waveform tables of DAN-006 to DAN-009 are the graded description. The band-limiting
  method is not specified. The metric grades harmonic amplitudes, not the method.

### REQ-DEVICE-ANALOG-008 — sub oscillator and sync

- **X.** OscillatorMode 0 (Sub):
  - a component one octave below the oscillator is added, at gain exp0(0.01, 1) of
    OscillatorSubAmount;
  - for the saw and the rectangle it is a square with the main waveform's amplitude: at amount 1
    its fundamental is 2/π of the internal level;
  - for the sine it is a sine;
  - amount 0 adds nothing.
- **X.** OscillatorMode 1 (Sync): the saw and the rectangle are hard-synced. They run at exp(1, 20)
  times the key frequency of SubAmount and restart every key period. Their strongest partial lies
  near that ratio (4.5 at amount 0.5). The sine is unaffected.
- **X.** The spectra of DAN-037 and DAN-038 are graded with the waveform metric. The exact shape of
  the synced waveform is defined by those renders only.

### REQ-DEVICE-ANALOG-009 — pitch envelope

- **X.** OscillatorEnvAmount and OscillatorEnvTime raise the pitch at each note-on by
  ±exp(0.01, 6) octaves, with the sign of the stored amount. The offset falls linearly to 0 over
  exp(0.01, 10) s. At amount 0.5 and time 0.5 the offset is 0.2512 octave, falling over 0.3249 s.
  Readings at fractions 0.05 to 0.95 of the time agree with the linear fall within the
  estimator's 1–2 ms lag.
- **U.** The fall's exact frame alignment. **Effect on T1:** graded with the pitch-trajectory
  metric only.

### REQ-DEVICE-ANALOG-010 — noise

- **X.** With NoiseToggle on, a noise source joins the oscillators:
  - its spectrum is flat and its amplitude distribution uniform (kurtosis 1.80). Its RMS is 0.375
    of full scale at NoiseLevel 1 and balance gain 1, at the output of the probe set;
  - NoiseColor is a one-pole low-pass y ← y + a(x − y), with a = min(1, 2πf/fs) and
    f = exp(20, 22,000) Hz of c. The renders agree within 0.16 dB (Color 0.1) and 0.02 dB from
    Color 0.4. Color 0.9 and above leave it unfiltered;
  - NoiseLevel and NoiseBalance act as the oscillator's level and balance (REQ-011).
- **X, U.** The noise sequence depends on the clock seed (REQ-020).

### REQ-DEVICE-ANALOG-011 — levels and routing into the filters

- **X.** OscillatorLevel and NoiseLevel are gains exp(0.01, 3). The default 0.8062 gives 1.0019.
- **X.** Balance (host value b = 1 − stored) sends gain S((1 − n)/4) to filter 1 and S(n/4) to
  filter 2, except exactly 1 and 0 at b = 0 and 0 and 1 at b = 1. Stored 0.5 gives 0.718635 to
  each. The levels agree with these laws within 10⁻⁴ dB.
- **X.** Each signal chain is: oscillator and noise into the filter, filter, amplifier. Chain 2
  renders bit-identically to chain 1 for the same settings. Each chain's amplifier sounds only when
  its AmplifierToggle is on.
- **X.** FilterToFilter2 adds filter 1's output, at gain 2(c/127)², to filter 2's input. There is no
  midpoint case: 0.5 gives 0.5079 and 1 gives 2. Amplifier 1 still receives filter 1's output.
- **X.** With a filter off, its input passes unchanged.

### REQ-DEVICE-ANALOG-012 — filter responses

- **X.** The cutoff of FilterCutoffFrequency is f_c = 30·(22,000/30)^(c/127) Hz, with no midpoint
  case: 0.5 gives 833.78 Hz. It is the same at 44.1 and 48 kHz. After modulation (REQ-013) it is
  limited to 20 Hz … 0.49·fs.
- **X.** FilterQFactor gives Q = exp(0.1, 120): 0.1 at 0, 3.562 at 0.5, 120 at 1.
- **X.** With g = tan(πf_c/fs), s = (1 − z⁻¹)/(g(1 + z⁻¹)) and D(Q) = s² + s/Q + 1, the filter's
  transfer function is:

  | Stored FilterType | Response | H(z) |
  | --- | --- | --- |
  | 0 | LP12 | 1/D(Q₂) |
  | 1 | LP24 | (1/D(Q₄))² |
  | 2 | BP6 | s/D(Q₂), peak gain Q₂ |
  | 3 | BP12 | (s/D(Q₂))² |
  | 4 | Notch2 | (s² + 1)/D(Q₂) |
  | 5 | Notch4 | U (below) |
  | 6 | HP12 | s²/D(Q₂) |
  | 7 | HP24 | (s²/D(Q₄))² |
  | 8, 9 | Formant6, Formant12 | U (below) |

  Here Q₂ = min(Q, 100) and Q₄ = min(√Q, 100). Fits of the renders give these coefficients to a
  relative residual of 1.8 × 10⁻⁷ for every 2-pole case (72 fits) and within 0.004 dB for LP24.
  For BP12 and for HP24's passband the agreement is within 0.12 dB.
- **X.** The filter is linear in the signal. The responses above hold at any level below the drive
  (REQ-014) and output (REQ-015) saturators.
- **U.** Notch4 at Q above about 1, and both formant types. Their responses are defined by the
  reference renders DAN-018, DAN-021 and DAN-022 only. **Effect on T1:** these types are graded only
  with the steady-state harmonic metric against those cases' settings. Other settings of these
  types are not verifiable.

### REQ-DEVICE-ANALOG-013 — filter modulation

All shifts add in octaves to log₂ f_c, or to log₂ Q, before the limits of REQ-012. A negative stored
amount inverts the shift.

- **X.** FilterKbdCutoffMod shifts the cutoff by 4n²·(key − 60)/12 octaves: 1 octave per octave at
  0.5, 2.26 at 0.75. FilterKbdQMod shifts log₂ Q the same way.
- **X.** FilterEnvCutoffMod shifts the cutoff by 16n⁴·e octaves, where e is the filter envelope's
  gain (REQ-016): 1 octave at 0.5, 5.11 at 0.75. FilterEnvQMod shifts log₂ Q by 4n²·e.
- **X.** FilterLFOCutoffMod shifts the cutoff by 4n²·l octaves, where l is the LFO's value
  (REQ-018). The shift was measured at amounts 0.25 and 0.5.
- **X.** FilterControllee on (filter 2 only) makes filter 2's cutoff that of filter 1 times
  A((c − 64)/32), where c is filter 2's own cutoff controller. At c = 127 the factor is exactly 4.
  When filter 1 is off, filter 2 goes to 20 Hz.
- **U.** FilterLFOQMod, and the combination of several modulations at once. These were not
  rendered. **Effect on T1:** sets that use them are graded only through the whole-render metric,
  with no closed form.

### REQ-DEVICE-ANALOG-014 — filter drive

- **X.** FilterDrive acts on the filter's input. Values 1 to 3 are symmetric, 4 to 6 asymmetric:

  | Stored | Input gain | Ceiling above | Ceiling below |
  | --- | --- | --- | --- |
  | 0 | 1 (no saturation) | — | — |
  | 1 / 4 | 1 | 8 / 4 | 8 / 8 |
  | 2 / 5 | √2 | 4 / 2 | 4 / 8 |
  | 3 / 6 | 2 | 2 / 1.3 | 2 / 8 |
- **X.** After the input gain, a signal u at internal level is unchanged for |u| ≤ 1. Above,
  |u| becomes L − (L − 1)/(1 + (|u| − 1)/(3(L − 1)))³, keeping its sign, where L is the ceiling for
  that sign. Fits of all six types agree within 6.4 × 10⁻⁵ at the output. Below the knee the drive
  is a pure gain: the default Drive 1 is linear at normal levels.

### REQ-DEVICE-ANALOG-015 — amplifier and output

- **X.** AmplifierLevel is a gain exp(0.01, 2). The default 0.869 gives 1.0045.
- **X.** AmplifierPan gives the left gain S((1 − n)/4) and the right gain S(n/4). At the centre both
  are 0.718635; at the ends 0.99984 and 0.
- **X.** Volume is a gain 2·n². The default 0.7048 gives 1.000.
- **X.** The output is out = 4·C(s/4), where s is the sum of the amplifiers' outputs and
  C(x) = x for |x| ≤ 0.7. Above, C(x) is ±(1 − 0.3/(1.1111112|x| + 0.22222221)³). |out| ≤ 4 × 10⁻⁹
  becomes exactly 0. The renders agree within 1.1 × 10⁻⁶ up to s = 3.86.
- **X.** At the probe set (table values, both chain-1 envelopes at sustain 1, sine) C4 peaks at
  0.36396: 0.7002 internal × level, balance, amplifier, pan and volume gains.
- **U.** AmplifierKbdAmpMod, AmplifierKbdPanMod and AmplifierEnvPanMod were not rendered.
  **Effect on T1:** sets that use them are not verifiable.

### REQ-DEVICE-ANALOG-016 — envelopes

Each chain has a filter envelope (Envelope.0) and an amplifier envelope (Envelope.1).

- **X.** Times are T = exp(0.005, 15) s for AttackTime, DecayTime and ReleaseTime, and
  exp(0.1, 1,000) s for SustainTime. SustainLevel is n.
- **X.** The gain e moves through segments, each from y₀ to y₁ over L = T·fs frames (L real,
  N = ⌊L⌋). Its steps 1 … N are computed in binary32:
  - ExponentialSlope off: y ← y + (y₁ − y₀)/N;
  - ExponentialSlope on (default): y ← y·(1 − k) + t·k, where k = 3.4906588/L and
    t = y₀ + 1.0313935·(y₁ − y₀).

  The frame after step N holds exactly y₁. The next segment's step 1 is the frame after that.
- **X.** The segments run as follows:
  1. a note-on's attack goes from 0 to 1, with step 1 at g′ + 1;
  2. the decay goes from 1 to the sustain level S;
  3. the sustain segment goes from S to 0 over SustainTime while the key is held;
  4. a note-off's release goes from the current gain to 0, with step 1 at g′ + 1.
- **X.** All 46 rendered cases agree with this within 2.4 × 10⁻⁷ for every segment, both slopes, and
  sustain times 0 to 1. The binary32 steps make long sustain times behave as follows. With
  ExponentialSlope off and SustainTime 1, the sustain does not fall. With it on, it falls by about
  0.26 % per second.
- **X.** A voice ends when its amplifier envelope reaches 0. Its output is then exactly 0, and it is
  free. The last non-zero frame after a note-off is g′ + ⌊L_release⌋ when the release starts at 1.
- **S.** The filter envelope is the same module as the amplifier envelope. Inferred: it follows the
  same law. Only its sustained level was rendered (REQ-013).
- **U.** Envelope Loop, FreeRun and Legato. They were not rendered. **Effect on T1:** sets with a
  non-default value are not verifiable.

### REQ-DEVICE-ANALOG-017 — velocity

- **X.** An envelope's AmpMod scales its gain by 2^((a/2)(v − 64)/63), where v is the note
  velocity and a = lin(0, 8). At AmpMod 0.5, velocity 127 gives ×4, 64 gives ×1 and 1 gives ×1/4.
- **X.** AttackMod scales the attack time by 2^(−(a/2)(v − 64)/63), with a = lin(0, 8).
- **X.** With both at 0 (table defaults) velocity has no effect on the output.
- **S-cond (A1).** Live's velocity, a binary32 that may be fractional
  (REQ-PLAYBACK-CORE-012), reaches the device as a 7-bit data byte.
- **U.** How Live rounds a fractional velocity to that byte. **Effect on T1:** graded cases use
  integer velocities.

### REQ-DEVICE-ANALOG-018 — LFOs

Each chain has one LFO. LFO 2 is taken as identical to LFO 1 (S, same module).

- **X.** LFOSpeed gives the rate exp(3, 1,000)/60 Hz, from 0.05 to 16.67 Hz. The LFO's phase runs
  from 0 at the instance's first processed frame. With LFOGateReset on it restarts at 0 at each
  note-on.
- **X.** LFOWaveShape (value l from −1 to 1):
  - **0, sine:** rises from 0 at phase 0;
  - **1:** starts at +1, falls linearly to −1 at phase PW, then rises to +1;
  - **2, square:** +1 for phase below PW, −1 above.

  PW is LFOPulseWidth's n.
- **X.** The LFO adds to its destinations:
  - pitch: 4n²·l octaves;
  - cutoff: 4n²·l octaves (REQ-013);
  - amplitude: a gain factor 1 + n·l, within 0.5 %;
  - pan: position 0.5 + n·l/2.

  These depths hold for OscillatorLFOModPitch, FilterLFOCutoffMod, AmplifierLFOAmpMod and
  AmplifierLFOPanMod.
- **X, U.** Shapes 3 and 4 are random-like but do not depend on the seed. They are defined by
  renders only and were not described. The pulse-width modulation of OscillatorLFOModPW swung the
  duty by ±0.011, ±0.063 and ±0.216 at amounts 0.25, 0.5 and 1. Its law is not identified. LFOPhase
  shifted the start by a quarter cycle at 0.25 and a half cycle at 0.5 with gate reset, and by a
  quarter cycle at 0.5 when free-running. Its law is not identified.
  **Effect on T1:** these settings are graded only against reference renders made for them.
- **U.** LFODelay, LFOFadeIn and LFOSync, which needs the transport values Live passes.
  **Effect on T1:** sets that use them are not verifiable.

### REQ-DEVICE-ANALOG-019 — vibrato

- **X.** With VibratoToggle on, the pitch is modulated by a sine:
  - rate lin(0.25, 10) Hz of VibratoSpeed;
  - depth ±exp(0.0002, 1/6) octave of VibratoAmount;
  - no vibrato for exp0(0.05, 5) s of VibratoDelay after the note-on;
  - then a rise to full depth over about the VibratoFadeIn time.
- **U.** The exact fade-in curve, and VibratoModWheel (needs controller input, REQ-023).
  **Effect on T1:** vibrato with fade-in is graded with the pitch-trajectory metric only.

### REQ-DEVICE-ANALOG-020 — random components

- **X.** These depend on the device's random generator, which the device seeds from the clock when
  it is built:
  - the noise source;
  - the oscillator's noise shape;
  - KeyboardError;
  - VibratoError.

  In this harness the generator is Park–Miller, which is inferred from Apple's libc lineage.
  Inferred: in Live these differ between instances and sessions.
- **X.** Everything else, the LFO random shapes included, is independent of the seed.
- **U.** The exact distributions. **Effect on T1:** these components are graded statistically
  only (metric), and no sample-exact render is expected.

### REQ-DEVICE-ANALOG-021 — glide, unison and envelope modes

- **U.** PortamentoToggle on. Glide occurs, but its curve and its first-note behavior were not
  resolved: the first note after creation appears to glide from an earlier pitch. Same for
  PortamentoMode and PortamentoLegato.
- **U.** KeyboardUnisonToggle with KeyboardUnison, KeyboardDetune and KeyboardUnisonDelay.
- **U.** Envelope Loop, FreeRun and Legato (REQ-016).
- **Effect on T1:** Live Sets that turn on glide or unison, or change these envelope modes, are not
  verifiable. DAN-043 and DAN-044 retain renders for a later revision; they are not graded.

### REQ-DEVICE-ANALOG-022 — parameter changes over time

- **X.** A host value set between blocks while a note sounds first changes the output at these
  frames, for a change at block start 13,312 (g′ = 13,332):

  | Parameter | First changed frame |
  | --- | --- |
  | Volume | g′ |
  | OscillatorSemi, OscillatorDetune | g′ + 8 |
  | FilterCutoffFrequency | g′ + P |
  | OscillatorLevel, AmplifierLevel, AmplifierPan | g′ + 58 |
  | Amplifier AttackTime, during sustain | g′ + 4,402 |
- **U.** The ramps that follow, and the timing for other parameters. **Effect on T1:** automation of
  Analog parameters is graded only after the change has settled, from 100 ms after it on. Within
  those 100 ms, and for parameters taken at note-on, nothing is graded.
- **U.** In Live, on which block boundary an automated value arrives (Q-025). **Effect on T1:** as
  for Electric, automation can be early or late by up to one Live block plus one period.

### REQ-DEVICE-ANALOG-023 — other MIDI input and sample rates

- **U.** Pitch bend (PitchBendRange), controllers (VibratoModWheel), channel pressure
  (ChannelPressureTarget/Amount) and MPE (MpeCC74…, per-note pitch bend). None was rendered.
  **Effect on T1:** none for clips that send only notes. These inputs are outside T1's note
  playback.
- **X.** At 48 kHz:
  - timing scales by P = 48;
  - pitch follows REQ-006;
  - envelope and filter laws hold, as tested in REQ-012 and REQ-016.
- **U.** Other rates, and a rate change on a running instance. **Effect on T1:** renders at rates
  other than 44.1 or 48 kHz are not graded.

## Timing and state

- **Units.** Frames at the stated sample rate. Pitch in octaves; cutoff in Hz.
- **Latency.** None beyond the control grid of REQ-004.
- **Persistent state.** None beyond the stored parameters. Voices, envelopes, LFO phases and filter
  states live only in a running instance.
- **Determinism.** Deterministic for a given host-value set, event list and grid, except the random
  components of REQ-020.

## Comparison metric

Proposed, pending acceptance as the T1 device-audio criterion of ADR 0004. A candidate render of a
case passes when it meets every line that applies.

| Signal | Comparator | Tolerance |
| --- | --- | --- |
| Timing | First non-zero frame of each note; first changed frame after each note-off; last non-zero frame of a voice | Exact; the voice end ±1 frame |
| Pitch | Frequency of a steady segment (≥ 0.2 s) | 10⁻⁵ relative (0.017 cent) |
| Pitch trajectory | Instantaneous frequency from zero crossings, averaged over 10 ms | 0.02 octave, or 1 % of the modulation depth if that is larger |
| Steady waveform | Amplitude of every harmonic within 40 dB of the strongest, over a steady segment, fitted at the reference frequency | 0.05 dB; mean (DC) within 10⁻³ of the peak |
| Onset waveform | The 2,048 frames from each note's first non-zero frame | Rel RMS 5 × 10⁻³ |
| Envelope | RMS in consecutive 10 ms windows, where the reference is within 60 dB of its peak | 0.05 dB |
| Random components (REQ-020) | RMS over 0.5 s and third-octave band levels 80 Hz to 16 kHz | 0.5 dB |

Why these. One-ulp changes of the substituted libm results move the renders by:

- 4.7 × 10⁻⁴ rel RMS over the first 2,048 frames after onset, and 1.8 × 10⁻³ over 8,192;
- at most 0.0075 dB in the 10 ms envelope;
- 1.2 × 10⁻⁶ in frequency.

The arm64 release slice has 814 fused multiply-adds that the x86_64 slice lacks. Inferred: they act
at the same scale. A sample-exact comparison over long windows would therefore fail on rounding
alone, and the tolerances leave a margin of seven to ten over the measured sensitivity. The models of
REQ-006 to REQ-016 meet these tolerances against the renders with margins of 10 or more.

## Acceptance cases

Expectations are X renders of the original x86_64 code under REQ-001's protocol. None has been run
against Live, and under ADR 0003 none will be. Kinds: P positive, B boundary, T timing, U not
graded.

### Fixtures

All renders are mono IEEE-float 32-bit WAV at the stated rate, made in host blocks of 512 frames.
They are in [t12-analog-v1](../../analysis/ableton-live-12.4.3/r2/t12-analog-v1/manifest.json)
`raw/<case>.wav`, and each `raw/<case>.script` gives the exact calls. Parameter sets:

- **table**: SPEC-BUNDLED-DEVICE-PARAMETERS "Default when absent" values;
- **preset**: the shipped Defaults-preset values;
- **probe**: table with SignalChain1 Envelope.0 and Envelope.1 SustainLevel 1 and the sine shape.

Each case lists only its stored-value changes. Notes are at 44.1 kHz unless stated. "C4 held"
means key 60, velocity 100, on at frame 4,400, not released.

### Cases

| Case ID | Requirement | Kind | Setup | Expected result / comparator | Reference render (SHA-256 of WAV) |
| --- | --- | --- | --- | --- | --- |
| DAN-001 | 001, 004, 006, 016 | P | table; C4 on 4,400, off 26,450 | All metric lines. First non-zero 4,401; saw at 261.5371 Hz; decay toward 0; last non-zero 54,026 | `314723861924b170` |
| DAN-002 | 001, 004, 006, 023 | P | table at 48 kHz; C4 on 4,800, off 28,800 | First non-zero 4,801; 261.4787 Hz; last non-zero 58,821 | `7837b416853eec55` |
| DAN-003 | 001, 002 | P | preset; C4 on 4,400, off 26,450 | Envelope, steady waveform, timing; last non-zero 48,491 | `be66eee57e5010d2` |
| DAN-004 | 001, 005, 017 | P | preset; keys 48, 55, 64 (velocities 100, 90, 110) on at 4,400, 8,800, 13,200, all off 26,450 | Envelope, onset, timing | `9991f5775dd4a833` |
| DAN-005 | 023 | P | DAN-004 at 48 kHz (frames ×48/44) | As DAN-004 | `5ee1afa5f5e07cd2` |
| DAN-006 | 007 | P | probe; C4 held | Sine, steady waveform metric; peak 0.36396 | `1fae06ba4e2b3e48` |
| DAN-007 | 007 | P | probe, shape 1; C4 held | Saw harmonics | `b770743b90f1632b` |
| DAN-008 | 007 | P | probe, shape 2; C4 held | Rectangle, duty 0.2701, mean 0.0300 at the output | `c7ee5f5c6210562b` |
| DAN-009 | 007 | B | probe, shape 2, PulseWidth 0 and 1 | Duty 0.0365 and 0.5 | `b9a5b46a92abeeed`, `8e77d0fd715a3488` |
| DAN-010 | 006 | P, B | probe; keys 24, 69, 108 for 0.3 s each | 32.6922, 440.1927, 4184.601 Hz | `c6ac6e5629560ddb` |
| DAN-011 | 006 | P | probe; (a) Octave 1, Transpose 7, FineTune 0.75; (b) OscOct −1, OscSemi −5, Detune 0.25; (c) key 96, Stretch 1 | 795.770, 93.7905, 2118.569 Hz | `89adb764abe00d4b`, `96be017dc1fdbbce`, `a05db78ec46abc57` |
| DAN-012 | 010, 020 | U, statistical | probe, oscillator off, noise on, balance 1; C4 held | Random metric only: RMS and third-octave levels. Not sample-graded | `3f3f29bd9f36dcbc` (one seed) |
| DAN-013 | 012 | P | probe, saw, key 48 held; filter 1 on, cutoff 0.5, Q 0.6 | Harmonics follow LP12 at 833.78 Hz, Q 7.198 | `b641a585759986ea` |
| DAN-014–020 | 012 | P | As DAN-013 with FilterType 1 to 7 | As REQ-012's table. Type 5 (DAN-018) graded against its render only | `d78047f4b20e2d2d`, `686fb99a98717fe1`, `8d64bcb21d10f8ab`, `f0d652566f8f56c5`, `ecde431316963aca`, `ba2fd86d345877a5`, `0aa015a18ee66aab` |
| DAN-021, 022 | 012 | P (render only) | As DAN-013 with FilterType 8 and 9 | Steady waveform metric against the render | `66dafc940ee1fb2a`, `c5b7dfeb70e8e3e7` |
| DAN-023 | 013, 016 | P | DAN-013 with LP24, cutoff 0.3, FilterEnvCutoffMod 0.75, filter decay 0.4, sustain 0 | Envelope and onset metrics | `0bb999b20839bbe4` |
| DAN-024 | 013 | P | DAN-013 with FilterKbdCutoffMod 0.5; keys 48 then 72 | Cutoff 416.9 then 1,667.6 Hz (±1 octave) | `f2e3d43bd5db8877` |
| DAN-025, 026 | 014 | P | probe, saw, key 36; filter 1 on (cutoff 0.8), OscLevel 1, AmpLevel 0.6; Drive 3 and 6 | Steady waveform metric | `0752392c2f271ed4`, `012ef825abcbafec` |
| DAN-027 | 015 | B | probe, saw, key 48; OscLevel 1, AmpLevel 1, Volume 1 | Output saturator; peak 3.507 | `889977e7d0fe41fe` |
| DAN-028 | 016 | P | probe, rectangle PW 1; amplifier A 0.4, D 0.4, S 0.5, R 0.4; C4 off at 35,270 | Envelope metric; last non-zero 40,805 | `7e7398a0de1c2910` |
| DAN-029 | 016 | P | DAN-028 with ExponentialSlope off | As DAN-028 | `7e449b74e9bb6617` |
| DAN-030 | 016 | P | probe, rectangle PW 1; decay 0.2, sustain 0.75, SustainTime 0.5; C4 held 1.4 s | Exponential fall over 10.369 s | `4afc1abf7873781a` |
| DAN-031 | 017 | P | probe; amplifier AmpMod 0.5; C4 at velocities 1, 64, 127 | Gains ¼, 1, 4 | `e30d5d47088de83e` |
| DAN-032 | 017 | P | probe; attack 0.4, AttackMod 0.5; velocity 127 | Attack ends after 1,391 frames | `8ac5880a9623e55c` |
| DAN-033 | 018 | P | probe, key 81; LFO 1 on, speed 0.75, pitch 0.25 | Pitch trajectory: 3.9454 Hz, ±0.254 octave, phase 0 at frame 0 | `82ec08b722fdbf93` |
| DAN-034 | 018 | P | DAN-033 with LFO square, PW 0.25 | +0.254 octave for a quarter cycle, −0.254 octave otherwise | `59515ccab3e365e6` |
| DAN-035 | 009 | P | probe, key 81; EnvAmount 0.5, EnvTime 0.5 | +0.2512 octave falling linearly over 0.3249 s | `4e02082cb1c1b8c3` |
| DAN-036 | 019 | P | probe, key 81; vibrato 0.75, delay 0.5, fade 0.5 | No vibrato for 0.509 s; then 5.125 Hz, ±0.0314 octave | `046b1dc915b635fc` |
| DAN-037 | 008 | P | probe, saw; Sub, amount 1 | Square one octave below | `d6cfb03c2db00b9b` |
| DAN-038 | 008 | P | probe, saw; Sync, amount 0.5 | Synced spectrum, peak near 4.5·f | `5da649f6867fc6fa` |
| DAN-039 | 005 | P | probe; Polyphony 1; keys 48, 72, 96 at 4,400, 8,800, 22,000 | Key 48 stolen at 22,001 | `1a3a8084cc84c63b` |
| DAN-040 | 005 | P | probe; Polyphony 0; keys 60, 67, 64 on, then 67 and 64 off | 261.54, 392.12, 329.59, 329.59, 261.54 Hz at 0.2 … 1.0 s; envelope metric through the key changes | `7fa400308538a0b3` |
| DAN-041 | 011, 013 | P | probe, saw, key 48; filter 1 LP12 (DAN-013) into filter 2 at 1; oscillator 2 (rectangle) into filter 2 HP12 at cutoff 0.4, following; amplifier 2 on | All metrics | `0e15783926ca8fac` |
| DAN-042 | 004 | T | probe; C4 on at frame 1,001, off at 3,011 | First non-zero 969; first changed frame after the note-off 2,993 | `33a5a38c382218b8` |
| DAN-043 | 021 | U | probe, mono, glide 0.75; keys 72 then 84 legato | Not graded | `44f6401fac590077` (retained) |
| DAN-044 | 021 | U | probe, saw; unison on, 4 voices, detune 0.5 | Not graded | `33625adeac2f6bdb` (retained) |
| DAN-045 | 001 | P | DAN-004 in host blocks of 64 and 2,048 | Bit-identical to DAN-004 | DAN-004 |
| DAN-046 | 016, 021 | U | Envelope Loop, FreeRun or Legato; LFO sync, delay, fade | Not graded | — |
| DAN-047 | 023 | U | Pitch bend, controllers, pressure, MPE | Not graded | — |

## Open questions

Proposed for [questions](../questions.md) (not edited by this draft):

- **Live-side protocol** (Q-025): grid phase and event frame base; Live's block sizes; the rounding
  of fractional velocities to the event byte; whether Live stops processing on a 0 activity flag;
  and on which block an automated value arrives.
- **Unresolved device behavior:**
  - glide and its first-note start;
  - unison;
  - envelope Loop, FreeRun and Legato;
  - the mono key-change dip;
  - LFO Phase, Delay, FadeIn, Sync and pulse-width laws, and the random LFO shapes;
  - the Notch4 and formant closed forms;
  - the keyboard and envelope pan modulation of the amplifier;
  - the ramps after parameter changes.

  Each has an X route with this harness.
- **arm64.** Whether the fused multiply-adds change the binary32 envelope steps that make long
  sustain times behave as REQ-016 states. It needs a static comparison of the segment step, or an
  approved arm64 emulator.
- **Metric.** Acceptance of the proposed metric for ADR 0004.

## Analyst evidence appendix

Analysis-only. Do not copy into a handoff. Canonical evidence:
[Analog DSP by extracted execution](../research/device-analog-dsp.md). Retained run
`analysis/ableton-live-12.4.3/r2/t12-analog-v1/`. Harness `harness/`, byte-identical to the T1.2
loader, built to `/var/tmp/sound-analysis/t12-analog/xdev`. Slice:
`Analog.bundle/Contents/MacOS/Analog` (SHA-256 `dddb93e7…8c3d4b`), x86_64 at offset 16,384,
500,880 bytes, SHA-256 `75c8d1cd8e10c7bcc2570c02c204d0860d725467353729eb1f2cef8594f2d113`.

| Clause | Evidence |
| --- | --- |
| 001 | `results/determinism.json`, `results/protocol.json` (warm-up, flag), `results/cases.json` DAN-045 |
| 002 | N6 `out/conversions.tsv` and `out/spec_defaults.tsv` (`an.host`, asserted 203 indices) |
| 003 | `results/static_map.json` (builder `0x18d8` arm64, curve declarations) |
| 004 | `results/timing.json` (220 events), `results/protocol.json`; the T1.2 `analog.json` `timing` |
| 005 | `results/voices.json`, `results/steal.json` |
| 006 | `results/pitch.json` (335 cases, `model.osc_freq`); arm64 VCO `0x35f80`, `0x37830`, `0x3760c` |
| 007, 008 | `results/osc.json`, `results/subsync.json` |
| 009 | `results/peg.json` |
| 010 | `results/noise.json` |
| 011 | `results/levels.json`, `results/routing.json` |
| 012 | `results/filter.json` (72 system-identification fits); arm64 coefficient functions `0x44f68` (2-pole, Q ≤ 100, f_c ≤ 0.49fs), `0x45388` (4-pole, √Q) |
| 013 | `results/mod.json`, `results/lfodest.json`, `results/routing.json` `follow` |
| 014 | `results/drive.json`; saturator family arm64 `0x42a20` |
| 015 | `results/levels.json`, `results/output.json`; arm64 `0x27530` |
| 016 | `results/env.json` (46 cases, `model.segment` in binary32); envelope ratio method `measure.env_curve` (host index 99 = 0 as a measurement device only) |
| 017 | `results/velocity.json` |
| 018 | `results/lfo.json`, `results/lfodest.json` |
| 019 | `results/vibrato.json` |
| 020 | seed comparisons in the research page; `results/noise.json` `seed` rows |
| 021 | `results/glide.json` (open); DAN-043, DAN-044 |
| 022 | `results/protocol.json` `parameter_changes` |
| Metric | `results/libm.json`; the onset and envelope calibration on the research page; `results/fma_scan.txt` (arm64 814 fused in 130 functions, x86_64 0) |

## Revision and handoff

| Revision | Date | Change |
| --- | --- | --- |
| 1 | 2026-10-18 | First draft (T1.2, packet t12-analog-v1). 23 requirements: 17 with X closed forms or X tables (004 to 019 in part, 022); 002 S with S-cond and U parts; 001 X with U parts; 020, 021 and 023 largely U. 47 cases: 41 graded against retained reference renders (one statistically), 6 not graded |

Not released. A first release could carry these with their cases and renders:

- REQ-001 and 003 to 019 without their U parts;
- REQ-002's S clauses.

It needs:

- the metric accepted for ADR 0004;
- a reviewer's check that the formulas are behavior statements, not recovered code;
- a decision on whether render-only definitions (formant, Notch4, sync waveform, random LFO
  shapes) are acceptable fixtures.

REQ-021 and 023 wait on further X work. The Live-side clauses wait on Q-025.
