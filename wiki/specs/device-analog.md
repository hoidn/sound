---
id: SPEC-DEVICE-ANALOG
type: spec
status: draft (partial; finite extracted expectations adopted through R8; general mode, timing and public behavior U)
updated: 2026-10-23
evidence_status: partial (REQ-022 timing/trajectories U; bounded r2 correction approved)
access: analysis
revision: 15
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

Revision 3 adds only the explicitly listed finite extracted expectations in
[its case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-analog-r3-finite-v1/case-aliases.json):
eight paired parameter histories and twenty one-control envelope-mode inputs.
These are bounded exceptions to the unverified modes/history scope above, not
general laws or an extension of the released audio comparison metric.

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
  - 85 indices clamp to 0..max and act as an integer: enumerations, Booleans, Octave and Semi;
  - KeyboardDetune, KeyboardUnisonDelay, PitchBendRange, the DummyPerNotePitchBendRange and the
    MPE amounts act as floats in their range;
  - Polyphony and the MPE targets are handled separately.
- **X.** The curves are confirmed by the renders of REQ-006 to REQ-019. The c = 64 midpoint case of
  lin and sq applies where those requirements write n. Where a law is written with c/127 there is
  no midpoint case.

- **X, finite R8 qualification.** [DAN-472–703](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-analog-r8-kind3-transpose-finite-v1/cases232.json)
  retain 24 supplied Transpose integers and 208 further one-index native-kind3
  vectors only in the fixed 203-word P1 history below. All 338 declared
  index/value aliases join 254 full vectors, including inherited references;
  the Transpose vectors receive no duplicate IDs or captures. Index 99 = 0
  remains measurement-only auxiliary. These finite observations do not newly
  validate clamp or rounding behavior between integers, stored/UI conversion,
  a productive control, pitch formula, general event/state law or Live/ARM
  behavior. The general clauses above retain their existing evidence scope.

### REQ-DEVICE-ANALOG-004 — note events and timing

- **X.** Status 0x9n is a note-on and 0x8n a note-off. The channel n has no effect. A note-on with
  velocity 0 is a note-off. Release velocity has no effect. A note-off for a key that is not
  sounding changes nothing.
- **X.** An event at frame f takes effect at its grid point g′. The first output frame it can
  change is g′ + 1. A note-on therefore can sound up to P − 1 frames before its frame. The rule
  holds for 520 events: the 300 of the
  [T1.2 gate](../research/device-dsp-extracted.md#analog-results) (250 note-ons, 50 note-offs), and
  220 further note-ons and note-offs at both rates in blocks of 512, 64 and 333.
- **X.** Output before the first note is exactly 0. After every voice has ended it is exactly 0
  (REQ-016).
- **S-cond (A2).** With processing from the instance's creation in blocks of 512, a note-on at
  frame f first sounds at P·⌊f/P⌋ + 1. One period is added when that grid point lies before the
  start of f's block.
- **U.** Live's grid phase and event frame base, as for Electric. **Effect on T1:** onsets are
  sample-exact only under A2. A different phase moves onsets by 0 to P − 1 frames.

- **X, finite R4 qualification.** [DAN-076–202 and the inherited DAN-028/P1 reference](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-analog-r4-velocity-finite-v1/cases128.json)
  supply the complete 128-value numeric velocity-byte catalog only for the exact fixed
  203-value DAN028 setup and event history in the R4 annex. Velocity 0 produces only
  positive-zero samples in this supplied capture. This observation does not independently
  establish zero-velocity note-off dispatch, arbitrary prior-voice history, release-velocity
  semantics or Live's event timing; those broader clauses are not newly validated here.

- **X, finite R5 qualification.** [DAN-203–329 and inherited DAN-028/P1](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-analog-r5-note-keys-finite-v1/cases128.json)
  supply all128 typed note-key values only in the fixed203-word P1 context at velocity100
  described in the R5 annex. Both matching on/off keys vary; these finite observations
  do not newly validate REQ-006's frequency formula, a clamp/alias mechanism, general
  note-range/onset behavior or Live's event timing. REQ-006 is context, not a newly tested law.

- **X, finite R6 qualification.** [DAN-330–344 and inherited DAN-028/P1](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-analog-r6-channel-finite-v1/cases16.json)
  retain the complete 16-value matching note-on/off channel-nibble catalog only
  in the fixed 203-word P1 key-60/velocity-100 history below. Fifteen fresh output
  hashes match the inherited nibble-0 identity. This does not newly validate the
  broader channel statement above, arbitrary event/voice histories, actual Live
  channel dispatch, A1/A2, general determinism or ARM/Apple behavior.

- **X, finite R7 qualification.** [DAN-345–471 and inherited DAN-028/P1](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-analog-r7-release-velocity-finite-v1/cases128.json)
  retain all 128 typed note-off release-velocity bytes only in the fixed 203-word
  P1 history below. The 127 fresh output hashes match the inherited byte-64
  identity. This does not newly validate the broader release-velocity statement
  above, arbitrary voices or event histories, dispatch/timing, Live A1/A2,
  general determinism or ARM/Apple behavior.

- **X, finite supplied independent MIDI-byte observations (revision 9).**
  [DAN-704–987](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-analog-r9-independent-midi-finite-v1/new-cases284.json) add 284 once-only histories at the fixed P1 context:
  127 On keys with Off key 60 fixed, 127 Off keys with On key 60 fixed,
  15 On channel nibbles with Off status 80 fixed and 15 Off channel nibbles
  with On status 90 fixed. Each axis varies one supplied event byte only.
  Four baseline aliases share ONE inherited DAN-028 INPUT reference,
  without replay, fresh PID/receipt/metrics or transfer of its criterion.
  These observations do not newly validate the broader unmatched-note,
  channel, release, dispatch, timing or public Live/ARM laws above.
  New waveform priors/expectations and portable expected/comparator/grade
  stay NULL; new application-predicate proofs remain false.

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
- **X, U.** In mono, a change of the sounding key dips the output and restarts it: the peak falls to
  0.29 to 0.45 of its level within about 100 frames and recovers within about 300. A release that
  leaves the sounding key unchanged has no dip. The exact form is U. **Effect on T1:** mono key changes are graded only against DAN-040's reference with the
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
    excess e rises with frequency: for C4, +0.03 % at harmonic 2, +0.6 % at harmonic 10 (2.6 kHz)
    and +5.4 % at harmonic 30 (7.8 kHz).
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
  - its spectrum is flat and its amplitude distribution uniform (kurtosis 1.80). With Color 1, the
    default NoiseLevel and balance gain 1, its RMS at the output of the probe set is 0.375;
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
  free. The last non-zero frame after a note-off is g′ + ⌊L⌋ of the release, from any starting gain
  (DAN-001, DAN-028).
- **S.** The filter envelope is the same module as the amplifier envelope. Inferred: it follows the
  same law. Only its sustained level was rendered (REQ-013).
- **U.** General Envelope Loop, FreeRun and Legato semantics, combinations and lifecycle
  histories remain unknown. **X, finite.** DAN-056–075 adopt the twenty supplied one-control
  inputs and their exact finite observation records under the recorded factory protocol.
  All four envelopes are retained, including the sixteen inputs whose outputs equal the
  same-batch control. Equality is not inactivity, no-op or absence of an effect. These cases
  supply finite reference facts, not a general mode law or portable waveform criterion.
  **Effect on T1:** other non-default mode values/configurations/histories remain unverifiable.

### REQ-DEVICE-ANALOG-017 — velocity

- **X.** An envelope's AmpMod scales its gain by 2^((a/2)(v − 64)/63), where v is the note
  velocity and a = lin(0, 8). At AmpMod 0.5, velocity 127 gives ×4, 64 gives ×1 and 1 gives ×1/4.
- **X.** AttackMod scales the attack time by 2^(−(a/2)(v − 64)/63), with a = lin(0, 8).
- **X.** With both at 0 (table defaults) velocity has no effect on the output.
- **S-cond (A1).** Live's velocity, a binary32 that may be fractional
  (REQ-PLAYBACK-CORE-012), reaches the device as a 7-bit data byte.
- **U.** How Live rounds a fractional velocity to that byte. **Effect on T1:** graded cases use
  integer velocities.

- **X, finite R4 qualification of the default-modifier sentence above.** Its assertion that
  velocity has no effect must not be read as equality between zero and positive velocity
  bytes. In the [exact R4 catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-analog-r4-velocity-finite-v1/cases128.json), all eight AmpMod/AttackMod
  fields remain 0: the supplied velocity-0 capture contains only positive-zero samples,
  while the 126 fresh positive velocities and inherited velocity 100 share the approved
  historical output hash and descriptive metrics. These are fixed-input observations,
  not a productive velocity-response curve, a universal no-effect/zero-note rule, or a
  new proof of the AmpMod/AttackMod equations. Fractional-velocity/public binding, A1/A2,
  ARM/Apple behavior and portable calibration remain unresolved.

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
- **U.** General Envelope Loop, FreeRun and Legato behavior (REQ-016), beyond the explicitly
  supplied DAN-056–075 input histories and their finite extracted expectations.
- **Effect on T1:** general glide, unison and envelope-mode behavior remains unverifiable;
  the finite mode inputs of REQ-016 do not establish simultaneous modes, repeated/overlapping
  notes, Legato/FreeRun/reset/load lifecycle or arbitrary settings. DAN-043 and DAN-044
  remain retained but not graded.

### REQ-DEVICE-ANALOG-022 — parameter changes over time

- **U.** The first output change, smoothing and subsequent trajectory when a host value changes
  between blocks, including note-on latching, dependence on the prior note/control history,
  settling time and timing for other controls. **Effect on T1:** parameter-change and automation
  trajectories are not graded. No general first-change rule, 100 ms settling bound or portable
  trajectory tolerance is established. The finite release excludes parameter changes; its
  accepted stationary/onset/envelope criteria do not supply a post-change oracle.
- **U.** In Live, on which block boundary an automated value arrives (Q-025), and how the stored
  value, parameter unit and actual Analog instance receive and process it. **Effect on T1:** no
  host-arrival or automation-delay bound is adopted, and these Live timing outcomes are not
  graded. A1/A2 remain assumptions; extracted device differences do not bind the Live scheduler,
  receiver or output path.

  **Historical evidence qualification (ANRMAP-001).** The revision 1 table came from a retained
  two-process history whose persistent event queue delivered its note again in the second
  process request. AttackTime first-change 17,734 is a historical repeated-note result, not
  uninterrupted-sustain delay. The seven earlier first-change scalars retain only their exact
  finite supplied-history scope; neither that table nor its former 100 ms convention defines an
  acceptance rule here. The reversible revision delta retains the exact superseded wording.

  **X, finite observations adopted in revision 3.** DAN-048–055 adopt all eight paired
  no-replay histories already approved by the
  [independent actual-result review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/batch-analog-change-history-v1-actual-review.json),
  under design revision 12's batch-adoption rule. Each pair uses the exact 203-value setup,
  a note-on at 8,192, a boundary at 13,312 and process intervals 13,312 then 7,680 frames in
  512-frame blocks at 44,100 Hz. The old captured expectation-null/UNGRADED fields remain
  immutable history; these new owner cases adopt only the reviewed finite facts.

  Every pair's prechange prefix is byte-identical. Seven pairs first differ numerically
  20–68 frames after the supplied boundary; the AttackTime pair is byte-identical through
  frame 20,991, including the full 7,680-frame post-boundary interval. Exact per-control
  values and first-difference coordinates are in the finite case catalog below. A missing
  difference in that window is the finite expectation, not proof of latching or no effect.
  No envelope stage is established by a held key. The U clauses above continue to govern
  general first-change, smoothing, latching/history, settling and actual Live timing.
  These cases introduce no calibrated waveform/trajectory tolerance, portable latency,
  100 ms settling rule, ARM execution or Apple-library equivalence.

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

Proposed as the general T1 device-audio criterion of ADR 0004. The finite metric
of [device-analog-v1](../../handoff/device-analog-v1/README.md) is accepted
only for its listed inputs and frozen measurement eligibility; broader criteria
below remain proposed. A candidate render of a
case passes when it meets every line that applies.

| Signal | Comparator | Tolerance |
| --- | --- | --- |
| Timing | First non-zero frame of each note; first changed frame after each note-off; last non-zero frame of a voice | Exact; the voice end ±1 frame |
| Pitch | Frequency of a steady segment of at least 0.2 s and 25 periods, measured with the same estimator in candidate and reference | 10⁻⁵ relative (0.017 cent) |
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

This legacy fixture description applies to DAN-001–047. Revision 3 finite cases
below instead alias retained raw interleaved stereo binary32 captures and full scripts.

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
| DAN-010 | 006 | P, B | probe with release 0; keys 24, 69, 108 held 0.9 s each, 1 s apart | 32.6922, 440.1927, 4184.601 Hz | `bf489d48c55a9af3` |
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
| DAN-032 | 017 | P | probe; attack 0.4, AttackMod 0.5; velocity 127 | Attack lasts L = 1,390.4 frames: gain exactly 1 from frame 4,400 + 1,391 | `8ac5880a9623e55c` |
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

### Revision 3 finite extracted cases

These twenty-eight new case IDs are finite **X** expectations, admitted through
the two batch reviews under design revision 12, not a second review of the observations.
The [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-analog-r3-finite-v1/case-aliases.json)
gives each complete input-script/vector/history alias, exact reviewed observation fields,
raw-output hashes and independent review identity. All prior DAN-001–047 rows remain exact;
DAN-046's broader ungraded mode/LFO scope is not closed by these finite cases.

For DAN-048–055 (REQ-022), both baseline and changed scripts and outputs are retained.
The initial vector is the released ANALOG-AUDIO-013-01 vector with all 203 host values
in order. Note-on8192/key48/velocity100 is delivered once. At frame13,312 the baseline
re-sends its original value and the paired run sends the value listed below; processing
continues for7,680frames. No second note is delivered. Frame coordinates are zero-based;
+0 and −0 compare numerically equal, while the prechange prefix also requires byte identity.

| Case | Changed host index/control/value | Finite expected relation between pair | Source pair |
| --- | --- | --- | --- |
| DAN-048 | 52 SignalChain1/FilterCutoffFrequency → 0.6000000238418579 | First numeric difference 13376 (boundary +64); prechange bytes identical | CTRL-01 |
| DAN-049 | 45 SignalChain1/OscillatorLevel → 0.6000000238418579 | First numeric difference 13380 (boundary +68); prechange bytes identical | CTRL-02 |
| DAN-050 | 68 SignalChain1/AmplifierLevel → 0.6000000238418579 | First numeric difference 13380 (boundary +68); prechange bytes identical | CTRL-03 |
| DAN-051 | 2 Volume → 0.5 | First numeric difference 13332 (boundary +20); prechange bytes identical | CTRL-04 |
| DAN-052 | 71 SignalChain1/AmplifierPan → 0.0 | First numeric difference 13380 (boundary +68); prechange bytes identical | CTRL-05 |
| DAN-053 | 31 SignalChain1/OscillatorSemi → 19.0 | First numeric difference 13357 (boundary +45); prechange bytes identical | CTRL-06 |
| DAN-054 | 34 SignalChain1/OscillatorDetune → 0.6000000238418579 | First numeric difference 13357 (boundary +45); prechange bytes identical | CTRL-07 |
| DAN-055 | 105 SignalChain1/Envelope.1/AttackTime → 0.8999999761581421 | No numeric/byte difference through frame20,991; prechange bytes identical | CTRL-08 |

For DAN-056–075 (REQ-016/021), the full DAN028 script is preserved except exactly one
listed host value. Each capture uses all203values (index99=1), note-on4400/key60/velocity100,
note-off35270/velocity64, zero input/flag0, rate44100, stopped transport(position0/120BPM),
one44100-frame process request in512-frame blocks, then destroy. The fresh DAN028
capture is an explicit control alias CONTROL-DAN028-P1, not a new case or a regrading of
the old reference. All21captures have finite samples, positive per-channel RMS and
byte-identical channels in this supplied history.

| Case | Single host input change | Finite expected observation | Source capture |
| --- | --- | --- | --- |
| DAN-056 | 89 SignalChain1/Envelope.0/Loop = 1 | Byte-identical to control; last observed nonzero 40805 | mode-01-i89-v1 |
| DAN-057 | 89 SignalChain1/Envelope.0/Loop = 2 | Byte-identical to control; last observed nonzero 40805 | mode-02-i89-v2 |
| DAN-058 | 89 SignalChain1/Envelope.0/Loop = 3 | Byte-identical to control; last observed nonzero 40805 | mode-03-i89-v3 |
| DAN-059 | 90 SignalChain1/Envelope.0/FreeRun = 1 | Byte-identical to control; last observed nonzero 40805 | mode-04-i90-v1 |
| DAN-060 | 91 SignalChain1/Envelope.0/Legato = 1 | Byte-identical to control; last observed nonzero 40805 | mode-05-i91-v1 |
| DAN-061 | 101 SignalChain1/Envelope.1/Loop = 1 | First numeric difference vs control 15525; last observed nonzero 40805 | mode-06-i101-v1 |
| DAN-062 | 101 SignalChain1/Envelope.1/Loop = 2 | First numeric difference vs control 15525; last observed nonzero 40805 | mode-07-i101-v2 |
| DAN-063 | 101 SignalChain1/Envelope.1/Loop = 3 | First numeric difference vs control 35245; last observed nonzero 44099 (window censored) | mode-08-i101-v3 |
| DAN-064 | 102 SignalChain1/Envelope.1/FreeRun = 1 | First numeric difference vs control 15525; last observed nonzero 21085 | mode-09-i102-v1 |
| DAN-065 | 103 SignalChain1/Envelope.1/Legato = 1 | Byte-identical to control; last observed nonzero 40805 | mode-10-i103-v1 |
| DAN-066 | 172 SignalChain2/Envelope.0/Loop = 1 | Byte-identical to control; last observed nonzero 40805 | mode-11-i172-v1 |
| DAN-067 | 172 SignalChain2/Envelope.0/Loop = 2 | Byte-identical to control; last observed nonzero 40805 | mode-12-i172-v2 |
| DAN-068 | 172 SignalChain2/Envelope.0/Loop = 3 | Byte-identical to control; last observed nonzero 40805 | mode-13-i172-v3 |
| DAN-069 | 173 SignalChain2/Envelope.0/FreeRun = 1 | Byte-identical to control; last observed nonzero 40805 | mode-14-i173-v1 |
| DAN-070 | 174 SignalChain2/Envelope.0/Legato = 1 | Byte-identical to control; last observed nonzero 40805 | mode-15-i174-v1 |
| DAN-071 | 184 SignalChain2/Envelope.1/Loop = 1 | Byte-identical to control; last observed nonzero 40805 | mode-16-i184-v1 |
| DAN-072 | 184 SignalChain2/Envelope.1/Loop = 2 | Byte-identical to control; last observed nonzero 40805 | mode-17-i184-v2 |
| DAN-073 | 184 SignalChain2/Envelope.1/Loop = 3 | Byte-identical to control; last observed nonzero 40805 | mode-18-i184-v3 |
| DAN-074 | 185 SignalChain2/Envelope.1/FreeRun = 1 | Byte-identical to control; last observed nonzero 40805 | mode-19-i185-v1 |
| DAN-075 | 186 SignalChain2/Envelope.1/Legato = 1 | Byte-identical to control; last observed nonzero 40805 | mode-20-i186-v1 |

REQ-001's legacy repeat-run observations and the proposed general comparison chapter
do not add unmeasured oracles to these new cases. These records are raw stereo reference
data and finite observed relations, not a new portable waveform comparator. Descriptive RMS/peak/mean summaries in the catalog use
host binary64; they are not calibrated tolerances. The released onset/envelope/stationary
eligibility is not extended to these cases. Last observed nonzero at44,099 is capture-window
censored, not eventual tail duration or a voice-end bound. Differences between separate
fixed-input runs are not parameter-arrival, latching or host-latency measurements.
No seed/repeat-run determinism, simultaneous modes, general lifecycle, actual Live binding
or native ARM/Apple equivalence follows. ADR0003's arm64 inference caveat applies to
these extracted expectations; no candidate conformance result or new release is claimed.

### Revision 4 finite velocity-byte observations

The [R4 catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-analog-r4-velocity-finite-v1/cases128.json) adds 127 **X finite native observations**, DAN-076–202,
from the [sole independent actual/source review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/analog-velocity-bytes-v1-review.json)
SHA256 `8e62cca3b4de5efa1ebefb919f193cb90bdd45a0d4d1166f9ac42dc27374d71b`.
The full 128-point catalog includes velocity 100 solely as the existing DAN-028 /
CONTROL-DAN028-P1 historical reference, with no new ID or execution. The 127 new IDs
follow ascending fresh velocity order 0–99, 101–127. All 75 prior IDs, 67 table rows and
28 R3 finite case objects remain exact; these units are navigation, not outcome/pass totals.

Every evaluation supplies the catalog's same 203 ordered binary32 parameter words
(index 99 = 1), with all eight AmpMod/AttackMod fields 0. The recorded context is rate 44,100 Hz,
zero input and flag 0, no warmup, stopped transport (position 0, 120 BPM), a note-on at
frame 4,400 (status 0x90, key 60, selected integer velocity), and a note-off at frame
35,270 (status 0x80, key 60, velocity 64). One 44,100-frame process request uses
512-frame blocks (last block 68 frames), followed by destruction. Each fresh capture has
its own process and exact script/receipt/PID/time links; inherited velocity 100 has only historical
provenance. The shared vector/history and individual script/output pins are in the catalog.
A1/A2 remain assumptions about Live, not newly observed public receiver behavior.

The approving review retains each case's recorded Linux providers, typed raw/flag
carriers and endpoint-custody, floating-point, durability and process-cleanup limits.
Those observations supply no Apple-host or continuously attested runtime binding.

At velocity 0, both channels contain 44,100 positive-zero samples, with peak/RMS/mean 0 and
no first/last nonzero frame. Each of the 126 fresh positive-velocity captures is finite,
has byte-identical left/right channels and matches the inherited velocity-100 output SHA256
`c78d03bc527a8f0776cb84c5da401be9f49abf7b2b9bea9838ffcce0f6f56772`.
Their per-channel peak is 0.4791160523891449, RMS 0.1475852307858183,
mean 0.058815737467571426, with 36,405 numeric nonzero frames, first 4,401 and last 40,805.
These exact finite facts become native expectations with extracted-execution provenance.
Hash comparison uses approved historical metadata; no old-audio bytewise comparison or
fresh velocity-100 control is implied. No repeat/seed stability or general velocity law follows.

Original fresh waveform-prior NULLs remain immutable. Portable expected outputs,
comparators and candidate grades are NULL; descriptive binary64 metrics and native
hashes introduce no portable waveform criterion or accepted tolerance. The existing
comparison metric, timing/state/error/U clauses and released 38 groups / 42 evaluations remain
unchanged. No whole-Live execution, public mapping/dispatch, ARM/Apple equivalence,
physical calibration, new release or whole-product closure follows; ADR 0003's arm64
inference caveat applies. Review here concerns only added wording/mapping/preservation;
observations are inherited by citation and are not reviewed again.

### Revision 5 finite typed note-key observations

The [R5 catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-analog-r5-note-keys-finite-v1/cases128.json)
adds127 **X finite native observations**, DAN-203–329, from the
[sole independent actual/source review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/analog-note-keys-v1-review.json)
SHA256 `2c1d02a7f73b9ef4588fb43b061efeb7d82f395044254415fe5686646e71e37a`.
The128-point catalog includes key60 solely as the existing DAN-028 / CONTROL-DAN028-P1
reference, with no new ID, original replay or fresh receipt. New IDs follow ascending
fresh key order0–59,61–127. All202 prior IDs,67 prior table rows,28 R3 finite case objects,
the complete R4 velocity catalog and released38 groups/42 evaluations remain exact.
These navigation units are not behavior/pass totals.

Only BOTH matching note-on and note-off key bytes vary across0–127. Every evaluation
supplies the same203 ordered binary32 parameter words (index99=1), all eight
AmpMod/AttackMod fields0, rate44100Hz, zero input/flag0, no warmup and stopped
transport0/0/120. A note-on at4400 has status0x90/velocity100; note-off at35270 has
status0x80/velocity64. One44100-frame process request uses512-frame blocks (last68),
followed by destruction. The shared vector/history, exact event16-byte words and
individual script/output/receipt/PID/time references are in the catalog. Inherited key60
retains only approved historical provenance. A1/A2 remain Live-side assumptions.

The approved summary records every fresh capture finite in both channels, with
byte-identical left/right output and first nonzero frame4401 in this exact history.
Each case retains its own reviewed native output identity and per-channel descriptive
metrics as finite native expectations. Among127 fresh captures there are125 distinct
hashes: keys125/126/127 share hash
`47caef58ceb23dc37b0172d432320e39f8d8ae1b02d78a17b6fa4756d08f1a0f`.
This is descriptive equality of those captures, not a clamp, alias, periodicity or pitch
mechanism. No fresh hash matches the inherited key60 hash; old audio was not reread.
Neither an f0 estimate nor a general frequency/key-range/onset law was tested here.
REQ-004 is the finite mapping; REQ-006 remains unchanged pitch context only.

Historical335 pitch rows omit complete203word/event/render/phase information.
They supply no additional exact-context inherited joins or universal absence claim.
All original fresh waveform-prior NULLs remain immutable. Portable expected outputs,
comparators and candidate grades remain NULL. No new metric, model, fitting, tolerance,
physical calibration, general pitch/channel law, public Live A1/A2 behavior or Apple/ARM
compatibility is admitted. The sole actual review's recorded provider/import/typed-flag,
endpoint-custody, floating-point, durability and process-cleanup qualifications remain.
Hash identities and descriptive binary64 values are not portable waveform criteria.

All R4 requirement bytes remain exact prefixes (the other22 whole bodies are exact),
and existing U/state/error/history, comparison tolerances and release scope are unchanged.
This revision introduces no new original call or handoff release; required unsupported
behavior keeps whole-product coverage OPEN. Owner review concerns only new wording,
case mapping/IDs and preservation; approved observations are inherited by citation.

### Revision 6 finite matching channel-nibble observations

The [R6 catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-analog-r6-channel-finite-v1/cases16.json) adds 15 finite **X native observations**,
DAN-330–344, in ascending nibble order 1–15, from the
[sole actual/source approval](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/analog-channel-nibbles-v1-review.json)
SHA256 `9cf7ed07ada75e3d8064e8a9e75791ce17d3efd5debbeb89ac1535eb90ab9108`.
The complete 16-point catalog retains nibble 0 only as the existing DAN-028 /
CONTROL-DAN028-P1 reference, with no duplicate ID, fresh control, receipt, PID or
UTC. All 329 prior IDs, 67 table rows, 28 R3 objects and the complete 128-point
R4 velocity and R5 note-key catalogs remain exact. The resulting 344 navigation
IDs are not compatibility outcomes, grades or passes.

Only both matching status low nibbles vary: note-on `0x90 | n` and note-off
`0x80 | n`. The catalog records all 32 packed 16-byte event words. Key 60,
note-on velocity 100, note-off velocity 64 and all 203 ordered binary32 parameter
words (index 99 = 1, eight AmpMod/AttackMod fields 0) stay fixed. The P1 context
is 44,100 Hz, zero input and flag 0, no warmup, stopped transport at position 0
and 120 BPM, note-on at frame 4,400 and note-off at 35,270, one 44,100-frame
process request in 512-frame blocks (last block 68), followed by destruction.
No new event type, reset, segmentation or state crossproduct is inferred.

Every fresh capture is finite and nonzero, with byte-identical left/right
channels and first nonzero frame 4,401. Each matches the inherited nibble-0
output SHA256 `c78d03bc527a8f0776cb84c5da401be9f49abf7b2b9bea9838ffcce0f6f56772`
and its approved descriptive per-channel observations. Exact native identities,
input scripts and retained receipt/provenance links are in the catalog. These
finite facts become native expectations with extracted-execution provenance.
The comparison uses approved historical metadata; old nibble-0 audio was not
reopened, and no fresh paired baseline is implied. Equal hashes here establish
no general channel invariance, repeat/seed stability, pitch or mechanism law.

The historical channel-2 bare Boolean lacks a complete vector/event/render/
phase/provenance bridge and supplies no additional exact-context inherited
point or universal historical absence claim. Original fresh waveform priors,
portable expected outputs, comparators and candidate grades remain NULL.
Descriptive binary64 metrics and native hashes introduce no portable waveform
criterion, new metric, fit, f0 estimate, tolerance or physical calibration.

The approving review's recorded Linux providers, import-declaration versus code-
use distinction, typed-return/flag and host-parse limits, endpoint/interpreter/
floating-point custody, process-cleanup and regular-file fsync qualifications
remain part of each observation. No current receiver/table/class/ABI or public
Live A1/A2 channel path, Apple-host equivalence or ARM execution is proved;
ADR 0003's arm64 inference caveat applies. All other requirement bodies, the old
REQ-004 prefix, existing U/state/error/history, comparison tolerances and the
released 38 groups / 42 evaluations remain unchanged. R4/R5 statements about
unchanged bodies describe those revisions. No new release, candidate result or
whole-product closure follows. Only new wording/mapping/ID/preservation needs
the owner review; approved observations are inherited without actual replay.

### Revision 7 finite note-off release-velocity observations

The [R7 catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-analog-r7-release-velocity-finite-v1/cases128.json) adds 127 finite **X native observations**,
DAN-345–471, in ascending release-byte order 0–63 and 65–127, from the
[sole actual/source approval](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/analog-release-velocity-bytes-v1-review.json)
SHA256 `39514f4b22476e9fa4e32f3131785d138981e44c5ca8198652d996a718bf7c2e`.
The complete 128-point catalog retains byte 64 only as the existing DAN-028 /
CONTROL-DAN028-P1 reference, with no duplicate ID, fresh control, receipt, PID or
UTC. All 344 prior IDs, 67 table rows, 28 R3 objects, the complete 128-point R4
velocity and R5 note-key catalogs, and the 16-point R6 channel catalog remain
exact. The resulting 471 navigation IDs are not compatibility grades or passes.

Only note-off data2 varies. Status `0x80`, key 60 and frame 35,270 remain fixed;
note-on is at frame 4,400 with status `0x90`, key 60 and velocity 100. All 203
ordered binary32 parameter words (index 99 = 1, eight AmpMod/AttackMod fields 0)
remain fixed. The P1 context is 44,100 Hz, zero input and flag 0, no warmup,
stopped transport at position 0 and 120 BPM, one 44,100-frame process request
in 512-frame blocks (last block 68), followed by destruction. All 256 packed
16-byte event words and the 127 complete scripts are retained through the
approved summary. No event type, reset, segmentation or state crossproduct is
added.

Every fresh capture is finite and nonzero, with byte-identical left/right
channels, first nonzero frame 4,401 and last nonzero frame 40,805. Its output
SHA256 is `c78d03bc527a8f0776cb84c5da401be9f49abf7b2b9bea9838ffcce0f6f56772`,
matching the inherited byte-64 identity and approved descriptive observations.
Exact native output identities, both-channel descriptors and input/receipt
provenance are in the catalog. These finite results become native expectations
with extracted-execution provenance. The equality joins fresh hashes to
approved historical metadata; old byte-64 audio was not reopened or compared
bytewise, and no fresh paired baseline is implied. These facts establish no
general release/no-effect law, note dispatch, timing, repeat/seed stability,
pitch or mechanism.

The earlier release-127 bare Boolean lacks the complete vector/event/render/
phase/provenance bridge and supplies no additional exact-context inherited
point or universal historical absence claim. Original fresh waveform priors,
portable expected outputs, comparators and candidate grades remain NULL.
Descriptive binary64 metrics and native hashes introduce no portable waveform
criterion, new metric, fit, f0 estimate, tolerance or physical calibration.

All new capture code, including the parent launcher, was pre-call file-bound.
The approved same-PID, planned exec-argv/environment and pre-call-seal receipts
are source-level records, not independent OS execution/interpreter or child
floating-point attestation. Per-child runtime/local/script endpoint hashes and
whole-batch authority hashes do not establish continuous or transitive loaded
state. Import declarations remain distinct from counted code use; selected
direct exports and logged initializers do not bound nested native calls. Rate
return and activity flags retain their recorded values without public meaning.
Regular-file fsync was requested, without directory or crash-durability proof;
post-child failure detection, cleanup and escaped-descendant limits remain.

No current receiver/table/class/ABI or public Live A1/A2 release/timing path,
Apple-host equivalence or ARM execution is proved; ADR 0003's arm64 inference
caveat applies. The 22 other whole requirement bodies, old REQ-004 prefix,
existing U/state/error/history, comparison tolerances and released 38 groups /
42 evaluations remain unchanged. Earlier revision statements describe those
revisions. No new release, candidate result or whole-product closure follows.
Only added wording, mapping, IDs and preservation need the owner review;
approved observations are inherited without an actual/source/raw replay.

### Revision 8 finite supplied host-integer observations

The [R8 cases](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-analog-r8-kind3-transpose-finite-v1/cases232.json) add 232 finite **X native observations** in one revision.
The [whole 25-point Transpose catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-analog-r8-kind3-transpose-finite-v1/transpose-catalog25.json) assigns DAN-472–495 to the 24 fresh
host-index-4 values 0–11 and 13–24; host 12 references existing DAN-028/P1.
The [whole kind3 catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-analog-r8-kind3-transpose-finite-v1/kind3-catalog338.json) retains all 338 index/value aliases and 254 full
vectors from the 85 declared native integer domains. Its 208 further fresh
vectors receive DAN-496–703 in recorded index/value order. Its other vectors
reference the same 24 Transpose IDs, the existing DAN-028 baseline, 20 R3 mode
cases and DAN-029 (index 100 = 0). The 85 baseline aliases share one vector.
No alias creates an extra case, capture, PID, receipt or measurement. All 471
prior IDs, 67 table rows, 28 R3 objects and complete R4/R5/R6/R7 catalogs remain
exact. The resulting 703 navigation IDs are not compatibility grades or passes.

Observation authority is the [sole Transpose actual/source review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/analog-transpose-integers-v1-review.json)
SHA256 `18904de75c1234e0b274e76decee87ea78025a318b13dd56858df2c2588c60c1`
and [sole kind3 actual/source review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/analog-kind3-host-domains-v1-review.json)
SHA256 `58c868b77ce262b412fdd22a9d58049da2e28e9dcb76072796bd235213c4f7dd`.
Only those approved summaries supply new native identities, descriptors and
provenance; this owner adoption does not repeat actual/source/raw review.

Each capture changes one supplied native host word only. The other 202 ordered
binary32 words, including the fixed eight AmpMod/AttackMod fields 0 unless that
selected word is itself varied, remain at the recorded P1 values. The catalog
records every full vector and host token/f32/reconstructed-f64 projection.
Key 60, on-velocity 100 at frame 4,400, off-velocity 64 at frame 35,270, 44,100 Hz,
44,100 frames, 512-frame blocks (last 68), no warmup, zero input and flag 0,
stopped transport 0/0/120, clock 0 and existing unperturbed method remain fixed.
This is a one-index class, with no parameter, voice or event-state crossproduct.
Declared native integer ranges do not independently establish Live emission,
stored-value conversion, current parameter/receiver binding or public legality.

All 24 Transpose captures are finite, nonzero and equal between channels, with
24 distinct fresh hashes. All 208 further captures are finite and equal between
channels, with 42 distinct fresh hashes. Silent i028-v00 and i065-v00 are retained.
Index-99-zero i099-v00 remains explicitly **measurement-only auxiliary**, not
an admitted application predicate, portable criterion or calibration case. Exact
recorded native output hashes and per-channel word counts become finite native
expectations in their supplied contexts. They are no general invariance,
inactive-control, repeat/seed stability, mechanism, pitch or deterministic
waveform law. REQ-006's pitch formula and all event/timing claims remain exact
as previously written, without new validation here.

Every relevant join retains the Transpose review's historical label
qualification: its exact 80,667-byte owner pin identifies R7, although that
frozen packet's scalar revision 6 and R6 prose are stale. Those bytes are not
repaired and the discrepancy changes no input, model or finite result. The
kind3 packet's own R7 identity is retained separately. The 47 old script and
42 released-input projections are bounded input metadata, not a repeated old
audio/criterion audit or universal historical-absence proof; the earlier 335
source-version/executed-report association remains unknown. Inherited R3,
baseline, Transpose and DAN-029 references acquire no new receipts or metrics.

Original fresh waveform priors, portable expected outputs, comparators and
candidate grades remain NULL. Exact finite native identities introduce no new
metric, window, f0 estimate, fit, tolerance or physical calibration. Common
whole-batch initial-to-child-after custody is not per-child-before or continuous
loaded-provider/interpreter/OS execution/floating-point attestation. Import
declarations stay distinct from counted code use; selected exports and logged
initializers do not bound nested native work. Rate returns and activity flags
retain their recorded values without a public meaning. Raw logs/audio were
closed and hashed without explicit FD fsync; JSON regular-file fsync does not
prove directory or crash durability. Post-child detection, group cleanup and
escaped-descendant limits remain part of each observation.

Only the bounded REQ-003 qualification is appended. The 22 other whole bodies,
old REQ-003 prefix, every old acceptance annex, U/state/error/history, comparison
tolerances and released 38 groups / 42 evaluations remain unchanged. ADR 0003's
arm64 inference caveat applies. No public A1/A2, receiver/ABI, clock/audio,
Apple/ARM equivalence, new release, candidate result or whole-product closure
follows. Earlier revision count/preservation statements describe those revisions.
The sole new owner review covers added wording, IDs, joins and preservation.

### Revision 9 finite independent On/Off key and channel observations

The [complete catalog](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-analog-r9-independent-midi-finite-v1/cases285.json) retains 288 aliases / 285 WHOLE histories at one fixed
203-word P1 vector. DAN-704–987 are 284 fresh observations: On key 0–127
except 60 with Off key 60 fixed; Off key 0–127 except 60 with On key 60 fixed;
On channel 0–15 except 0 with Off status 80 fixed; Off channel 0–15 except 0
with On status 90 fixed. No paired key/channel changes, crossproducts,
extra events, timing segmentation, host update or state changes.
The four baseline aliases share ONE DAN-028 / CONTROL-DAN028-P1 INPUT
reference without a new ID, original call, PID, receipt, output, metric,
expectation or criterion. [All 288 joins](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-analog-r9-independent-midi-finite-v1/joins288.json) preserve complete histories,
two packed 16-byte events, original decimal/binary64/binary32 words and
exact approved-summary pointers; parameter-only dedup is invalid.

Only [Auto's sole actual/source review](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/analog-independent-midi-bytes-v1-review.json),
SHA-256 `5831d673770bc95169cffc2694ef5e6a77a0bd4dee3bf3b7336b1664b10a37e7`,
supplies these finite observations. This owner maps that approved summary
without actual/source/raw/audio/numeric re-review. Fresh output identities
and unsigned word summaries are descriptive native references; they are
not portable candidate waveform criteria. No old baseline audio is replayed
or compared, and no prior criterion or modal budget transfers to new cases.

All 203 original ordered decimal tokens and their parsed binary64/binary32
identities remain fixed. The vector hashes to
`18a94879168c2f73d621883d3a60b14de6f54a2b396fb8a0b11284c799926ed3`;
index 99=1 and all eight AmpMod/AttackMod words remain zero. The unchanged
P1 recipe uses rate 44100/render 44100/block 512/last 68, no warmup, zero input/
flag 0, baseline On 4400/status 90/key 60/velocity 100 and Off 35270/status 80/
key 60/velocity 64. Only the named event byte changes. Existing stopped
transport 0/0/120, TIME0, per-entry MXCSR1f80 and unperturbed bindings are
recorded-model context, not native FP/ABI or public current-receiver proof.
No new constructor model, tool, build, patch, provider, FP treatment or
calibration is introduced. Supplied coordinates do not prove Live timebase.

All 284 approved fresh outputs are finite, nonzero and channel-word-equal;
126 fresh hashes are descriptive only. Quiet/unequal outputs were permitted
by the frozen guard and were not omitted through output-driven selection.
These facts prove no unmatched-key handling, cross-channel matching,
release/gating/voice semantics, productive control, deterministic waveform,
physical accuracy or public/ARM law. The old shorter Boolean/input/source-
version/default qualification and bounded 47-script intersection remain
scoped metadata; no global absence or old-source execution attribution is
repaired. All fresh waveform priors/new expectations, portable expected/
comparator/grade stay NULL. No f0, estimator, metric, fit, window, tolerance,
calibration, velocity-zero dispatch or new application proof is added.

All new capture/parent/analysis/checker/initial-assembler source was file-
bound before calls for THIS batch. The materializer is historical, not a
final regenerator; this does not repair earlier preparation/checker/source/
default/FP/OSexec qualifications. One common set of 311 initial identities matches
each of 284 child-after snapshots (88,324 pairs), NOT separate per-child before
snapshots or continuous loaded-provider/interpreter/mapping/FP proof.
The parent and recorder have distinct PIDs; their recorded argv/endpoints
are not independent OSexec attestation. Native raw/stdout/stderr FDs were
closed/hash checked without explicit FDfsync; JSON receipts explicitly
requested fsync, without directory/crash/powerloss durability. An author
live checkpoint JSON read raced an ordinary in-progress truncate/write;
final closed JSON was checked, with no capture retry or record repair.
Post-child guards cannot retract earlier within-child calls. Cleanup of
selected groups/direct children does not exhaust parent-loss/escaped/native
process paths; normal runs do not validate failure paths. Resource floors,
soft packet bounds and conditional overshoot remain recording limits,
not OS quotas, reservations or unmodeled-file/external-writer guarantees.
The existing r2-large lexical/resolved storage adds no relocatability claim.

132 declared bindings (99 Linux/26 trap/7 data) differ from counted use: 64 Linux
code names per child. Neither proves provider/global-data absence. Each
child has 293 selected direct exports/87 CalcA plus initializer 314d0 logged
separately; nested/all-native call counts remain unknown. Rate's signed
integer remains opaque, not a public success/type/sample-clock law.

Only bounded REQ-004 wording is appended. All 22 other whole requirements,
including ENTIRE R8 REQ-003, old 004 R7 prefix, 67 original rows/703 prior IDs,
all R3–R8 objects/catalogs, auxiliary i099=0 measurement-only status, silent
gate observations, stale Transpose scalar-vs-exact-pin qualifications,
old NULL criteria/general U/tolerances/state/error/history and released
38 groups/42 evaluations remain unchanged, with full R8 reversal. The
resulting 987 navigation IDs are not passes or application-outcome units.
No release, portable criterion, public A1/A2/ARM grade, calibration, main-site
credit or whole-product closure follows. Required unsupported U stays open.

### Revision 10 finite converted Polyphony and virtual-target observations

The [complete catalog](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-analog-r10-converted-virtual-enums-finite-v1/cases194.json) adds 193 finite native observations,
DAN-988–1180, across 198 aliases / 194 WHOLE histories. [Case references](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-analog-r10-converted-virtual-enums-finite-v1/new-cases193.json)
and [all 198 joins](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-analog-r10-converted-virtual-enums-finite-v1/joins198.json) map each approved input to its recorded output.
One inherited DAN-028 / CONTROL-DAN028-P1 INPUT reference serves five aliases
without a new ID, original replay, PID, receipt, output, metric or criterion.
These are bounded supplied-input observations associated with REQ-002/003;
all existing requirement bodies remain unchanged. No broader conversion or
public binding claim is newly validated, and REQ-005 gains no voice law.

The five stored axes are Polyphony values 0–9 and four target domains 0–46.
Polyphony supplies host 0=max(v−1,0) and host 7=(v>0.5) JOINTLY, with no
independent 0/7 crossproduct. ChannelPressureTarget1/2 and MpeCC74Target1/2
independently change host 195/197/199/201. Thus six virtual host entries are
covered through five complete stored axes at the same P1 history, without
changing any other word or adding pressure, slide, CC74, reset, timing,
rate/block or state comparisons. The five extra rate/block points in the
INPUT assessment were not selected. Parameter-only identity is insufficient.

All four amount words at 196/198/200/202 remain exactly 0.5 in every one of
the 194 histories: binary32 `0000003f`, binary64 `000000000000e03f`.
[The sole actual review](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/analog-converted-virtual-enums-v1-review.json),
SHA256 `acbc34ff27bb1bad169e6f3eec655f5bea025098d8978f977e513855f33e407d`,
checks BOTH immutable INPUT v1 and mandatory erratum. Their single-field
composition is 3,893,689 bytes/SHA256
`99b9fa8b590f77601c2f79e4de7b04db731d67fc2cdc0651126a3124d1571408`.
The wrong v1 main-field and embedded-method zero-amount prose is historical,
explicitly superseded; no embedded materializer was executed. The original
catalog and script amounts were already 0.5. No dormancy, inactivity,
productive MPE dispatch or general no-effect law follows from this class.

All 203 original decimal tokens/reconstructed binary64/converted binary32
words remain exact except the selected coupled or individual host entries.
Index 99=1, no warmup, create/rate 44100/203 setters/On 4400 status 0x90 key 60
velocity 100/Off 35270 status 0x80 key 60 velocity 64/input flag 0/zero input/
process 44100 at 512 (final 68)/destroy remain the recorded P1 recipe. TIME0,
stopped transport 0,0,120 and existing per-entry MXCSR1f80 are inherited model
context, not traced native input registers/FP state, source/default provenance,
Live event-clock or public current receiver. No new constructor, provider,
patch, tool, original body/callee or stored-to-host experiment is introduced.

Only the approved summary supplies native observations; this owner performs
no actual/source/raw/audio/numeric proof re-review. All 193 fresh outputs
are finite, nonzero and channel-word-equal, with three distinct file hashes,
descriptive only. Each new native expected file identity is copied directly
from that summary for its exact supplied x86/Linux history; it is not a
portable waveform criterion or general deterministic/effect law. Frozen fresh
waveform priors stay NULL. New portable expected/comparator/grade remain
NULL; new application proof is false. No f0, fit, metric, window, tolerance,
physical calibration, voice capacity/stealing/labels, MPE/public/A1A2/ARM
law or repaired old 335 source-executed-version gap is implied.

The recorded initializer 314d0 entries (193) are separate from 56,549 selected
exports /16,791 CalcA; all nested/native call counts remain unknown. Rate's
literal 1 remains opaque. 132 declared bindings (99 Linux, 26 trap, seven data)
differ from 64 counted Linux code names per child; this proves no provider or
global-data absence. Eight whole-source endpoint pairs and 3,088 actual
per-child 16 before/after pairs are recorded equality only, not continuous
provider/interpreter/cache/native FP/ABI/source-origin or OSexec attestation.
The same-PID parent/precall/argv bridge remains source-level metadata.

All six new capture/parent/analysis/checker/initial-assembler sources were
pre-call bound according to the approved review. The initial materializer
is historical, not a final-directory regenerator. A checker count-substring
mistake was corrected while mutable before input checks/freeze/calls; no
native retry or frozen repair. New log/audio/JSON/JSONL FDfsync requests
prove no directory/crash/powerloss durability and repair no old gap. Resource
256 MiB lifecycle + 128 MiB headroom and remaining-output guards are unreserved,
not quotas or protections against current-child overshoot/concurrent writers.
Posthoc guards cannot retract prior within-child calls. Failure cleanup,
escaped/native paths and uncatchable parent loss were not tested by normal
success. Older source/default/FP/provider/0664/OSexec/fsync limits remain.

All 23 whole requirement bodies, including ENTIRE REQ-003/R8 and REQ-004/R9,
67 original rows/987 prior navigation IDs, R3–R9 objects/catalogs/old Acceptance
prefix, auxiliary i099=0 measurement-only/silent-gate/stale scalar qualifiers,
criteria/tolerances/U/state/error/history and released 38 groups/42 evaluations
remain exact, with full reversal to R9. The resulting 1,180 navigation IDs
are not passes or application-outcome units. No new release, grade, site
credit, physical calibration or whole-product closure follows. Required
unsupported U remains open.

### Revision 11 finite secondary rate and block histories

The [complete catalog](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-analog-r11-secondary-protocol-finite-v1/cases6.json) and
[joins](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-analog-r11-secondary-protocol-finite-v1/joins7.json) add five finite **X native observations**,
DAN-1181–1185: 48000 Hz/block 512, then 44100 Hz/blocks 64, 256, 333 and 2048.
The complete class contains six whole histories and seven aliases, not a
rate-by-block crossproduct. The 44100 Hz/block 512 baseline serves two
INPUT-only aliases with DAN-028 / CONTROL-DAN028-P1 navigation. It receives
no new ID, original call, PID, receipt, output, metric or criterion transfer.
Old baseline audio was not reopened or compared. REQ-001 and REQ-023 supply
protocol/rate navigation only; all twenty-three whole requirement bodies,
including their existing qualified broader X/S/U scope, remain exact.

Only the [sole actual/source review](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/analog-secondary-protocol-v1-review.json),
SHA256 `34aaab784bb5e7a3a9fd1635f1a2fd5bdc51a2db0fecddaaa39f016bbf057a12`,
supplies the five observations. This annex maps its complete approved summary
without a second actual/source/raw/audio/numeric review or new execution.
Every point supplies the same 203 original decimal tokens and reconstructed
binary64/binary32 P1 words, index 99=1 and the same eight zero modulation words.
On remains frame 4400/status 0x90/key 60/velocity 100; Off remains frame
35270/status 0x80/key 60/velocity 64. There is no warmup, reset, extra event,
new parameter/timing crossproduct or history substitution. All points process
exactly 44,100 frames, including the 48 kHz point: frames/events are NOT rescaled
and that point is not a 48,000-frame one-second history. Zero input/flag 0,
stopped transport 0/0/120, TIME0, unchanged per-entry MXCSR1f80 and existing
Linux/provider bindings remain recorded-model premises, without a new
construction, tool, build, patch, seed, FP treatment or calibration.

| New case | Rate | Block | CalcA | Final block | Selected direct exports |
| --- | --- | --- | --- | --- | --- |
| DAN-1181 | 48000 | 512 | 87 | 68 | 293 |
| DAN-1182 | 44100 | 64 | 690 | 4 | 896 |
| DAN-1183 | 44100 | 256 | 173 | 68 | 379 |
| DAN-1184 | 44100 | 333 | 133 | 144 | 339 |
| DAN-1185 | 44100 | 2048 | 22 | 1092 | 228 |

The block-64 capture's 690 CalcA records are retained positive finite evidence,
not a generic xexec 256-call cap or an unlimited-call claim. The unchanged
admitted device xdev is 149,608 bytes/SHA256
`3eec4ad1cfa0765c9e8267806cf02b7e664a07157043e3a170388cfa4d63cf14`;
its retained 8,128-byte source identity is
`2e550951a4c7eb669ecdf9fa50734b2227c0768cda0b62099e2e975bad9430a9`.
Source/model association is inherited, not independently rebuilt or proved as
the binary's exact executed source. Actual success is established only by the
approved retained logs, receipts and raw bytes under unchanged ret0/flag0-or-1,
cxx-failbits0, finite-output and custody guards. The whole five contain 2,135
selected direct exports, 1,105 CalcA and 1,764,000 raw stereo bytes. Five logged
0x314d0 initializers are separate; all nested/native totals remain unknown.

All five outputs are finite, nonzero and channel-word-equal, with three distinct
whole-output hashes. These are descriptive finite native references, not a new
rate/block/grid invariance, timing-scaling, pitch or deterministic waveform law.
No old baseline hash/output comparison or missing historical criterion is
invented. Fresh priors and native/new waveform expectations, portable expected
outputs, comparators and grades remain NULL; application admission is false.
No f0, fit, metric/window, tolerance, physical calibration, public Live route,
current receiver/clock/state or Apple/ARM equivalence follows. The existing
MPE prose erratum and its exact 0.5 amounts remain in their R10 scope, unchanged.

The selected packet omitted a direct context copy for its INPUT history hash;
the approving peer used the exact pinned INPUT authority projection
`/analog_selected_candidate/context` to recompute all six whole-history hashes.
That external projection is retained in the approved summary, without frozen
packet repair, embedded-method execution or old actual proof. The mandatory
MPE erratum does not change this context or protocol. Old executed-source,
335-input, default/preparation and source/version binding gaps remain qualified.

One COMMON initial set of 34 identities (10 runtime plus 24 frozen files) is
compared with each of five child-after arrays: 170 pairs, NOT fresh
per-child-before snapshots or continuous loaded-provider/interpreter/FP/OSexec
attestation. All six capture/checker/parent/initial assembler/finalizer sources
and inputs/scripts were pre-call-bound; the initial assembler/fragment are
historical stages, not final regenerators. Rate's signed integer 1 is opaque.
132 import declarations (99 Linux, 26 trap, seven data) differ from counted code
use; neither proves implicit provider/global absence. Entry registers/fenv and
transitive dependencies remain untraced. ADR 0003's arm64 inference caveat applies.

Raw stdout/stderr/audio FDs closed and hashed without explicit FD fsync; JSON
receipts request fsync without directory/crash/power-loss durability. First
post-child failures stop later children, not earlier queued calls within that
child. Selected-group cleanup does not exhaust parent loss, uncatchable or
escaped-descendant/native/IO paths. Unreserved 128MiB lifecycle plus 128MiB
headroom planning, full remaining-output/metadata guards and conditional soft
overshoot are not quotas or guarantees against external/unmodeled writers.
No retry or guard relaxation follows. The existing storage route is not a
relocatable protocol. Old source/FP/provider/OSexec/history limits stay attached.

All 1,180 previous IDs, 67 original table rows, R3–R10 objects/catalogs,
old acceptance annexes, all twenty-three whole clauses, metric/tolerances,
U/state/error/history and released 38 groups/42 evaluations remain exact,
with full reversal to R10. Preservation uses only the approved R10 owner
report's embedded mapping and baseline; no older proposal/catalog/code,
provider, fixture or actual proof is reopened or absent bytes reconstructed.
The resulting 1,185 navigation IDs are not passes or a product denominator.
Arrangement reviews only new wording, mapping, IDs and preservation; Root
remains citation-only new proposal payloads and actual observations. No
release, site credit, portable criterion/grade or whole-product closure follows.

### Revision 13 finite four-release-control observations

The [four-history mapping](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-analog-r13-four-release-controls-finite-v1/mapping.json)
adds only DAN-1190–1193 for the four newly approved supplied histories.
REQ-005 is context only: its whole existing body and all23 whole requirements
remain unchanged without new validation of parent voice-capacity, stealing,
release, activation, envelope, timing or physical assertions. Each original
release token0.6000000238/0.2 at storedPolyphony1 has full3 note-ons versus
exactev[:2] (first two, omitting the last scheduled note), with the SAME44100
end. Keys48/72/96 occur at4400/8800/22000, velocity100; there are no Off events.
No arbitrary event subset, timing/model crossproduct, warmup or reset is added.

The sole actual/source authority is the [approved four-control review](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/analog-four-unlaunched-release-controls-v1-review.json),
688112bytes/SHA256 `19b784963d1ac45db17888515748d03f0a8b2da2807bd992fc4abe74a782d222`.
Only its approved summary supplies original203 literal decimal/binary64/
binary32 words, scripts, histories, receipts/output references, protocol
and observations. The original probe's six differences from P1 at
hosts29/36/105/106/108/110 remain declared INPUT provenance; each new history
keeps its own supplied release token. Coupled host0=0/7=1 and host110 release
are exact, MPEamounts196/198/200/202 remain0.5; no activity/dormancy/productive
MPE inference follows. Existing149608-byte xdev/native model/C/TIME0/LIBM-
unset/rate44100/zeroInputflag0/process44100at512/last68/destroy, no warmup,
MXCSR/transport insertion or new receiver/provider/tool/model/FP treatment.

All four once-only captures passed unchanged ret0/flag01/CXX0/exit/stderr/
shape/finite/custody/resource guards.348CalcA/1172selected direct exports/
four logged initializer314d0 entries count separately; nested native/
provider work remains U. Rate signed projection is opaque, not a native
return-ABI/success/error/clipping/cause law. All four are finite/nonzeroBOTH/
stereoword-equal/two raw hashes/64usedLinux names, descriptive only. Each
full3-versus-prefix2 pair has DIFFERENT raw bytes/hashes at these supplied
histories. This is not a residual, estimator, threshold, fit, new metric,
waveform criterion, deterministic universal comparison or general capacity/
stealing/release/publicLive/ARM/Apple/physical/calibration law.

The full fourteen-history old AS-OF snapshot remains unchanged and separate
from these four new observations. R12's four approved count cases DAN-1186–
1189 stay exact; failedp04 and countp05–09 stay U without new IDs, expectations,
metrics or grades. The four release/control histories were unattempted in
that OLD snapshot; these new captures do not rewrite it. No failed count,
unlaunched count tail, accepted count, baseline or mono-priority history is
replayed/regraded/repaired and no guard relaxation, retry or automatic
continuation is authorized. Oldp04 TWOret1/flag1 projections, unaccepted raw
diagnostic/skippedfailedrawFDfsync and all source/default/envNone/FP/provider/
ABI/clock/OSexec gaps retain their earlier scope; no old output/PID/receipt/
metric/criterion transfers into these new cases.

76actual per-child19before/after custody pairs plus two source pairs are
endpoints, not continuous loaded-provider/nativeFP/register-entry/OSexec or
source-executed-version proof. Successful raw/log/JSON FDs request fsync;
outer files lack explicit FDfsync, no directory/crash/powerloss/old-gap
repair follows.128MiBfull lifecycle+128MiBheadroom/fullremainingraw+8MiBfuture
logsmetadata+64MiBfinal orremainingsoftbudget guards are unreserved/soft,
not quotas, concurrent-writer/escaped-child/within-child-overshoot or all
parent-loss/cleanup guarantees. Import declarations versus used counters
and initializer versus all nested work retain their exact qualified scopes.

Only this annex and revision metadata change. All1189 prior navigation IDs,
67 original acceptance rows plus five protocol navigation rows (72 literal
DAN rows), allR3–R12objects/criteriaU/state/error/history and releases38groups/
42evaluations remain exact/fullreverse. Prior object preservation uses only
currentR12 and its sole owner REPORT embedded metadata, never absent-byte
reconstruction or oldproposals/catalogs/fixtures. New priors/native-waveform
expectations/portable expected/comparator/grades remain NULL; application
predicate proof false. The resulting1193 navigation IDs are not passes or
a whole-product denominator. No release/site credit/grade/newapplication
proof or closure; required unsupported U remains OPEN.

### Revision 14 finite four-count observations under D09

**Analyst draft; four additional finite observations only.** The complete
[R14 mapping](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-analog-r14-count-opaque-finite-v1/mapping.json)
assigns DAN-1194–1197 to the separately approved p06–p09 histories. REQ-005
is navigation context only; these cases establish no general voice capacity,
stealing, MPE activation, parameter-delivery, return-meaning or public law.
The resulting 1,197 navigation IDs are not passes or a product denominator.

The sole observation authority is the [independent four-count review](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/analog-count-unlaunched4-opaque-v1-review.json),
983,811 bytes, SHA256 `b0178cac813c0480d65383a0af92f545957e4c5f68c4a7f3ac0dfd3832a39687`.
Its complete four approved points, exact inputs, source-case/receipt/output
references and literal ordered return/flag metadata are joined without a
second actual, source, raw, numeric or provider proof review. All fresh
waveform priors, native waveform expectations, portable expected values,
comparators and grades remain NULL; new application proof is false. Native
output hashes are descriptive references, not portable waveform criteria.

This is the exact user-adopted D09 suffix: only p06–p09 are new observations.
CalcA's logged signed64 projection is retained in order and canonical run
lengths as opaque DATA. The observed 638 zeros and 190 ones establish no
zero/one domain, native ABI, success/error, benignness or failure-cause law.
Likewise 24 flag-zero and 804 flag-one projections are literal observations,
not a public activity or flag-success law. The existing flag0or1 and every
other guard remain unchanged. D09 does not apply retrospectively to any
older record or automatically to other Analog histories or device families.

The original probe's 203 decimal/binary64/binary32 words and six P1
differences remain explicit. Polyphony stored 6–9 uses the declared joint
host-0/host-7 conversion; the four MPE amounts remain exactly 0.5. The
36 note-ons retain their original order at 4400 + 2200*i, keys 36–71 and
velocity 100, with no note-offs or warm-up. Rate is 44100, render end
105650, block 512 and final block 178. The admitted construction, event
types, model, providers and FP treatment are unchanged; no parameter
crossproduct or physical calibration is added.

All four approved outputs are finite, nonzero in both lanes and stereo-word
equal, with four hashes and 64 counted used-Linux code names. Those are
descriptive finite observations only, not new equality, productivity,
waveform, metric, residual, tolerance, pitch, capacity or numerical criteria.
The four account for 1,652 selected direct exports and 828 CalcA projections;
four logged initializer entries are separate and nested/all-native work is U.

Previously launched p00–p05 are excluded and were not replayed. Failed p04
and p05 remain U under their frozen strict guards, without reclassification,
new receipts, expectations or repair. The R12 fourteen-history and later
five-count partial snapshots remain unchanged ASOF metadata; their old
unattempted labels are not rewritten. This annex records the separate later
four-observation D09 result without claiming either old partial was complete.
Prior release/control observations and their byte-only comparisons also remain exact.

Custody is 30 before/after endpoint pairs per new child, 120 actual pairs in
all, plus three authority pairs. Endpoint agreement is not continuous loaded
provider, FP, source-to-compiled, ABI or OS-execution attestation. The minimal
supplied C/TIME0 environment is separate from old env=None/source/default
clock and version unknowns. Raw/log/JSON FD-fsync requests do not prove
crash or directory durability; outer-FD fsync is not explicit. Old failed
and skipped-fsync scopes are not repaired.
The unreserved full resource budgets, child limits, lack of a parent wall
watchdog and escaped-descendant/cleanup qualifications remain explicit.

Only this annex and revision metadata change. All 23 whole requirements,
1,193 prior navigation IDs, 67 acceptance rows plus five protocol navigation
rows (72 literal DAN rows), R3–R13 objects, criteria, tolerances, U, state,
error and history, all old fourteen/five ASOF records and the immutable
release's 38 groups/42 evaluations remain exact. Preservation uses the
current 119,503-byte R13 baseline, including its additive return-evidence
qualification; the historical 119,032-byte approved R13 target is not restored.
Full reversal restores that current baseline. No public/ARM, compatibility,
portable criterion, grade, release, O observation or whole-product closure follows.
Required unsupported behavior stays U and whole-Live coverage OPEN.

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

**Return evidence qualification (2026-10-22).** The [sole-reviewed executed-x86 CalcA study](../research/device-analog-dsp.md#executed-x86-calca-metadatanativescalar-adoption--2026-10-22) records conditional local return-carrier construction, separate optional-pointer delivery and remaining exit/runtime/ABI unknowns. It establishes no public return meaning or benignness and changes no guard, failed disposition, requirement, case or criterion. R13 remains unchanged.

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
| 1 | 2026-10-18 | First draft (T1.2, packet t12-analog-v1). 23 requirements: 17 with X closed forms or X tables (004 to 019 in part, 022); 002 S with S-cond and U parts; 001 X with U parts; 020, 021 and 023 largely U. 47 cases: 42 graded against retained reference renders, 1 graded statistically (DAN-012), 4 not graded (DAN-043, 044, 046, 047) |
| 2 | 2026-10-20 | ANRMAP-001 correction, pending independent review: REQ-022 removes unsupported sustain/first-change/settling/host-arrival grading claims. Whole eight-control no-replay results remain ungraded discovery. All 22 other requirement bodies and 39 case rows/47 IDs unchanged; device-analog-v1 unchanged. |
| 3 | 2026-10-21 | Adopt reviewed finite extracted observations directly under design12: eight paired no-replay histories (DAN-048–055) and all twenty first-order envelope-mode inputs (DAN-056–075), with fresh DAN028 as explicit control. General R2 timing/mode/lifecycle unknowns and all39old acceptance rows/47IDs preserved; no portable waveform criterion or release change. |
| 4 | 2026-10-21 | Add 127 finite native velocity-byte observations DAN-076–202 and one inherited DAN-028/P1 reference / full 128-point catalog; qualify REQ004/017 at fixed 203-value vector / all 8 modifiers 0. Old bodies retained as exact prefixes (21 other whole bodies), all 67 rows / 75 IDs / R3 objects / tolerances / released scope / U exact; portable comparators and grades NULL, no new general velocity, public, ARM or calibration law. |
| 5 | 2026-10-21 | Add127 finite typed note-key observations DAN-203–329 plus inherited key60 DAN028/P1 / complete128 catalog. Append only REQ004 finite qualification; REQ006 remains unchanged context, no f0 or general pitch/clamp/alias mechanism. All202 old IDs/67rows/R3objects/R4catalog/tolerances/U/state/history/releasedscope exact; portableexpected/comparator/gradeNULL. |
| 6 | 2026-10-21 | Add 15 finite matching channel-nibble observations DAN-330–344 and inherited nibble-0 DAN-028/P1 reference/full 16-point catalog. Append only REQ-004 finite qualification. Preserve 22 other whole bodies, old004 prefix, 329 IDs/67 rows, R3 objects/R4 and R5 catalogs, metrics/U/state/history and released scope. Portable expected/comparator/grade NULL; no general channel/public/ARM/calibration law. |
| 7 | 2026-10-21 | Add 127 finite note-off release-byte observations DAN-345–471 and inherited byte-64 DAN-028/P1 reference/full 128-point catalog. Append only REQ-004 finite qualification. Preserve 22 other whole bodies, old004 prefix, 344 IDs/67 rows, R3 objects/R4–R6 catalogs, metrics/U/state/history and released scope. Portable expected/comparator/grade NULL; no general release/dispatch/timing/public/ARM/calibration law. |
| 8 | 2026-10-21 | Add one combined 232-observation annex: 24 Transpose cases DAN-472–495 and 208 further native-kind3 vectors DAN-496–703, with full 25-point and 338-alias/254-vector reference catalogs. Append only REQ-003 finite qualification. Preserve 22 other whole bodies, old003 prefix, 471 prior IDs/67 rows, R3–R7 objects/catalogs, criteria/U/state/history and released scope. All portable expected/comparator/grade fields NULL; index99=0 remains measurement-only, no general/public/ARM/calibration law. |
| 9 | 2026-10-21 | Add 284 finite independent On/Off key/channel observations DAN-704–987, full 288-alias/285-WHOLE-history catalog with one inherited DAN-028 INPUT reference/four baseline aliases/no replay or criterion transfer. Append ONLY REQ-004 finite qualification; preserve 22 other whole bodies incl R8 REQ-003/old 004 R7 prefix/67 rows/703 old IDs/R3–R8 objects/auxiliary i099=0/silent gates/stale scalar qualifiers/criteria U/state/history/releases 38 groups/42 evaluations exact/full reverse. All NULL new priors/portable criteria/grades/new application proof false; no general unmatched-release/public/ARM/calibration law. |
| 10 | 2026-10-21 | Add 193 finite converted-input observations DAN-988–1180; full 198-alias/194-history catalog, one inherited DAN-028 INPUT reference/five aliases without replay or criterion transfer. Joint Polyphony 0/7 and four target axes only, exact 0.5 amounts under mandatory erratum; no dormancy/MPE/voice/general/public law. All 23 requirement bodies/67 rows/987 prior IDs/R3–R9 objects/criteria/history/releases 38 groups/42 evaluations exact/full reversal; portable criteria/grades NULL. |
| 11 | 2026-10-21 | Add five finite secondary rate/block observations DAN-1181–1185; full six histories/seven aliases, one baseline INPUT reference/two aliases without replay or criterion transfer. Keep 44,100 frames/events even at 48 kHz; block 64 has 690 CalcA/final 4. Annex/revision only: all 23 whole clauses, 1,180 prior IDs, 67 rows, R3–R10 objects/criteria/history/releases 38 groups/42 evaluations exact/full reversal. Preserve source-association/common170-pair/raw-no-fsync/NULL portable criteria limits; no new rate/block/grid/public/ARM law. |
| 12 | 2026-10-21 | Add four finite declared multi-note observations DAN-1186–1189; preserve all fourteen dispositions: four accepted, p04 guardFAIL U, nine unlaunched U. Annex/revision only; all23 whole requirements/1185 prior IDs/67 rows/R3–R11 objects/releases38 groups42 evaluations exact/full reversal. No actual pair, capacity, stealing, return-meaning, activation or public/ARM law; all priors/portable criteria/grades NULL, application false. |
| 13 | 2026-10-22 | Add only four finite release/control observations DAN-1190–1193/full4histories/two descriptive DIFFERbytehash pairs; full14oldASOF separate/unchanged/no failedp04 or counttail replay. Annex/revision ONLY/all23wholeREQ1189oldIDs67acceptance+5protocol=72literalrows/R3–R12objects/criteriaU/history/releases38groups42eval/fullreverse exact; NULL native-waveform/portablecriteriaGrade/appFalse/no capacity/release/publicARM/calibration law. |
| 14 | 2026-10-23 | Add only four D09 opaque-return observations DAN-1194–1197/p06–09; no failed p04/p05 replay or return/voice meaning. Annex/revision only; all23 whole REQ/1193 prior IDs/72 literal rows/R3–R13 objects/old14+5ASOF/criteria U/releases38 groups42 evaluations preserved/full reverse to current119503B R13 including additive return qualification. All new waveform priors/portable criteria/grades NULL/application false; no public/ARM/general capacity law. |
| 15 | 2026-10-23 | Add 161 finite current-supplied producer observations DAN-1198–1358 / 231 aliases. Retain all 469 contexts / 548 aliases / 556 slots / 23 groups: failed APCS-0162 U and 307 unattempted U, 14 references, seven FP/provider and eight whole SOURCE gaps. Annex/revision only; all 23 whole requirements, 72 rows, 1,197 old IDs, R3–R14 objects, old 14+5 ASOF, exact D09 four, U/criteria/history/releases 38 groups / 42 evaluations preserved with full reversal. Strict return 0 / flags 0 or 1; no opaque transfer. All nine omitted-input contexts / 16 aliases unattempted; native expectations/portable criteria/grades NULL, application false. |

Released locally on 2026-10-19: [device-analog-v1](../../handoff/device-analog-v1/README.md),
38 groups and 42 finite evaluations, after independent review. Only finite portions
of REQ-001, 004–008, 011–017 and 023 are released. The accepted metric uses frozen
onset/envelope/stationary eligibility and at most the first 40 eligible harmonics;
it does not release the parent's general formulas or open-ended spectrum criterion.
The [handoff plan](device-analog-handoff-plan.md) records the exact review and pin.

Random/statistical noise, uncalibrated modulation trajectories, glide, unison,
unrendered modes, parameter changes and Live-side protocol/mapping remain outside
that release. At that release the mutable parent was revision 1: review clarified the finite
contract's exact nonzero-onset test and zero-based channel numbering without
changing any captured values. Full behavior and arm64 equivalence remain unknown.


## Historical revision 1 evidence qualification — ANRMAP-001, 2026-10-20

The [independent family-map review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/family-analog-routes-v1-review.json)
found a retained-history error affecting REQ-022. Its old “during sustain”
AttackTime interpretation is **stale and unsupported**. The original table and
raw values remain history; they are not current proof of held-note latency.
The driver queues note-on4400 once, then runs two 13,312-frame process requests.
The harness reuses that queue with per-request coordinates, delivering the note
again in interval two: cumulative timestamp17,712 in callback17,408, offset304.
AttackTime first-change17,734 follows that callback and does not establish
uninterrupted-held-sustain behavior.

Seven other first-change values (13,332/13,340/13,376/13,390) precede the repeated
callback and retain only finite first-change support. They establish neither
later ramps nor a general 100ms settling bound. REQ-022's post-change/ramp and
actual host timing unknowns remain; the 100ms convention is not evidence that
arbitrary histories settle by then. No new expected value or behavior is adopted
by this stale notice. All 23 requirement bodies/47 case IDs (39 table rows) remain.
Current device-analog-v1 already excludes parameter changes and is unchanged.
A bounded family-map v2 provenance correction is being authored; no original/
candidate rerun or new metric is selected here.

## Revision 2 disposition — ANRMAP-001, 2026-10-20

At author freeze, revision 2 was **pending independent review**; the approval below now governs. Its REQ-022 supersedes revision 1's
parameter-change table and grading promises; it does not adopt new expected values, cases,
metrics or release scope. The historical revision 1 notice above is retained as written at its
stale-qualification stage: its “being authored” and unchanged-body statements describe that
stage, not current work. The bounded family-map v2 correction has since been approved, followed
by a frozen preparation/readiness gate, one whole eight-control execution and
[bounded actual-result review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/batch-analog-change-history-v1-actual-review.json).
All discoveries remain UNGRADED; the accepted finite device-analog-v1 release is unchanged.

The [revision 2 correction packet](../../analysis/ableton-live-12.4.3/full-spec-v1/analog-owner-r2-anrmap001/README.md)
pins that chain and the old owner 45184-byte identity, and preserves the exact superseded text
through a reversible minimal delta rather than a copied specification snapshot. All 23 REQ IDs,
the other 22 requirement bodies and all 39 acceptance rows covering 47 case IDs remain intact.
General smoothing/timing/other-control behavior, envelope-stage interpretation, ARM/Apple
behavior and Live control/receiver/output binding remain unknown. This correction supplies no
new original run, trajectory tolerance, portable latency metric or numerical acceptance case.


## Current r2 approval — 2026-10-20

The [independent owner review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/analog-owner-r2-anrmap001-review.json),
SHA256 `d621ac57b643ff3a7f0bb853cbb3ccb1e6faca26646900df67babec035157c66`,
approves the bounded ANRMAP-001 correction, manifest
`ecba81177c1efbc95d0e430b050ea3eb08f17b0bb8559f81fdf12ca285b4dcee`.
Pending-review wording in the author-frozen record is historical. Only REQ022
changes normatively; the other 22 requirement bodies, all 39 acceptance rows/47
case IDs and all 23 requirement IDs remain exact. Required parameter-change,
smoothing, settling, history and Live-timing outcomes remain U, with no new
portable oracle, metric, case or grade. The whole eight-control discovery is
ungraded. Device-analog-v1 and its 42 finite evaluations remain unchanged.

The [root metadata-adoption receipt](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/analog-owner-r2-root-adoption.json)
retains the exact reviewed owner identity and reversible status-only adoption
delta. Frozen predecessor maps and their 241-row inventory refer to revision 1;
they are not a newly derived r2 outcome denominator.


## Revision 3 finite observation adoption — 2026-10-21

The [R3 adoption packet](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-analog-r3-finite-v1/README.md)
pins the approved R2 predecessor, all23old body hashes and all39old acceptance-row hashes,
the two immutable batch manifests and independent batch reviews, and all28new case aliases.
The [eight-pair review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/batch-analog-change-history-v1-actual-review.json)
SHA256 `42883ae34c203ce530c203e9826520532aaffe4be81a58eb3d7b1c5aa9f73bbe`
and [whole P1 review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/batch-analog-envelope-modes-v1-review.json)
SHA256 `46402c9f899684c5e105301c522894b43f44ee8b52acb2c501251213c338250f`
admit the observations under design12 without a second observation review. R3's added
contract wording is a separate bounded owner-review scope.

The revision1/r2 disposition and approval notices above remain historical statements
of their own revisions. Their ungraded-discovery wording does not rewrite the new finite
R3 cases; original capture nulls/statuses remain exact. Only REQ016/021/022 change here;
the other20requirement bodies and all47old case IDs/39rows remain exact. The approved
R2 REQ022 withdrawal prefix remains byte-identical. General timing/settling, mode/lifecycle
and public behavior stay U; whole-product coverage stays open. Device-analog-v1 remains
immutable and no new handoff release or portable calibration is asserted.

## Interior-state helper qualification — 2026-10-21

[The whole interior-state review](../research/device-analog-dsp.md#analog-interior-state-helper-adoption--2026-10-21) establishes a conditional incoming-I return and 292 direct written bytes within a 696-byte bound. Its two inherited receiver bounds exclude Q's first word only for direct stores, under nonalias/nonwrap premises; eight opaque calls prevent a whole-helper preservation claim. No current class, runtime callback or public/default/math law follows. Cases, grades, releases and main-image sites are unchanged; required unsupported behavior stays U and coverage OPEN.

## Opaque-three eligibility qualification — 2026-10-21

[The whole three-helper review](../research/device-analog-dsp.md#analog-opaque-three-helpers-adoption--2026-10-21) retains direct state writes, opaque string/log-shaped calls and native FRINTZ/FP-store and mixed-precision distinctions. It supplies no receiver-free pure X batch, current-table preservation, exact numeric oracle or public behavior law. This is current missing admission, not an infeasibility claim or a ban on later legal finite discovery. Cases/grades/releases/sites stay unchanged; required U/product OPEN.

## Finite declared multi-note observations — revision 12

**Analyst draft; four observations admitted, ten histories remain U.**
The [complete R12 catalog](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-analog-r12-declared-multinote-partial-finite-v1/mapping.json)
assigns DAN-1186–1189 only to the four approved count histories p00–p03.
REQ-005 is navigation context, not a newly validated voice-capacity, stealing,
mono-priority, MPE activation or release law. The entire fourteen-history
source-declared class stays visible: p04 failed the frozen guard; p05–p09
and all four release/control histories were never launched. Those ten U
histories receive no IDs, accepted metrics, native expectations or grades.
No complete-class success or actual full/control pair comparison is claimed.

The sole observation authority is Arrangement's [independent partial review](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/analog-declared-multinote-v1-partial-review.json),
2,648,300 bytes, SHA256 `34a683877d016b55d09efb5cfe1fceedc835687e2fdce8ab0034ff639a093c61`.
Each new ID joins its exact input, approved point, native output reference and
copied unsigned/protocol metadata. Fresh waveform priors, native waveform
expectations, portable expected values, comparators and grades remain NULL;
new application proof is false. Native hashes are descriptive references,
not portable waveform criteria or new calibration. This owner revision does
not repeat actual/source/raw/numeric/provider proof or inherit old outputs.

These are the retained probe recipe's original 203 decimal/binary64/binary32
words, not the P1 vector. The six differences at indices 29, 36, 105, 106,
108 and 110 remain explicit in the inherited input qualification. The
mandatory corrected amounts at 196, 198, 200 and 202 remain 0.5; superseded
zero-amount prose was not executed and is not restored. Polyphony uses the
joint host-0/host-7 conversion; no independent Poly/MPE crossproduct is added.
The count inputs schedule 36 note-ons at frames 4400 + 2200*i, keys 36–71,
velocity 100, with no note-offs or warm-up, rate 44100, block 512 and end
105650 (last block 178). They are distinct whole event histories, not repeated
single-note finite-host samples. p00–p03 alone were accepted under the
unchanged admitted model and its ret0/flag0or1/CXX/shape/finite guards.

The source-declared release comparison uses exactly its two literal release
settings and full-three-note versus ev[:2] histories with the same end.
All four members are unattempted U: there is no accepted omission/control
output comparison or residual, tail, stealing or capacity inference.
Historical old-input nonintersection is bounded to the recorded cut, not a
claim that these inputs were never run. Old env=None, executed-source/default,
clock, FP and version bridges remain unknown; the current explicit supplied
environment does not establish historical equivalence.

Accepted p00–p03 outputs are copied as finite, nonzero in both lanes and
stereo-word-equal, with four hashes. These facts are descriptive only.
The failed p04 log retains two unaccepted ret1/flag1 projections at frames
59392 and 87552; its remaining ret0 projections, child exit0 and full raw
shape do not override the frozen rejection or explain the native return.
No return-error, clipping, ABI, activation or numerical-cause law is inferred.
The failed raw-FD fsync branch was skipped. Its diagnostics remain unaccepted;
no retry, guard relaxation, continuation or retroactive classification occurs.

The accepted four account for 1652 selected exports, 828 CalcA projections
and four separately logged initializer entries. Nested/all-native work remains
unknown. Rate's signed integer is opaque. Recorded custody is 19 actual
before/after endpoint pairs for each of five attempted children (95 pairs)
and two whole-batch source pairs, not continuous loaded-provider, actual-FP,
source-version or OSexec attestation. Successful child raw/log/JSON fsync
requests do not establish directory/crash durability; the failed raw path and
outer recorder have no such raw/outer FD request. Existing cleanup, within-child
first-detected-fault, unreserved resource and escaped-descendant limits remain.

Only this annex and revision metadata are added. All 23 whole requirements,
1185 prior navigation IDs, 67 acceptance rows plus five R11 protocol
navigation table rows (all 72 literal DAN rows), R3–R11 referenced objects, mandatory MPE
erratum, criteria, tolerances, U, state/error/history and the immutable release's
38 groups/42 evaluations remain exact. Prior preservation is inherited from
the approved R11 owner report's embedded metadata without reopening old
proposals, catalogs or fixtures. Full reversal restores R11. The resulting
1189 navigation IDs are not passes or a product-outcome denominator. Required
unsupported behavior stays U and whole-Live coverage OPEN; no new public/ARM,
physical compatibility, calibration, portable criterion, grade or release.

## Revision 15 finite current-supplied producer observations

This annex adds only 161 finite **X native observations**, **DAN-1198–1358**,
from the [sole-approved partial actual REPORT](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/analog-complete-producer-current-supplied-v1-partial-review.json),
84,865,091 bytes / SHA256 `f3f46e962d315bb708d5baf74216880c32dd31b6b63247d5bab419ea66889fa3`.
The [complete owner mapping](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-analog-r15-complete-producer-partial-finite-v1/mapping.json)
joins those cases to 231 SOURCE aliases and retains every other disposition.
Root reviews only this new wording, IDs, mapping and preservation; actual,
SOURCE, collector, raw/audio and numerical proof is inherited from the sole
review without reopening or rerunning underlying evidence.

The complete supplied class has 469 current contexts / 548 aliases derived
from 556 new SOURCE slots across all 23 groups. Inherited 183 shared arrays
and current 181 distinct ordered arrays are different DATA units, not native
uniqueness or product denominators. Fourteen prior INPUT references, one
conservative old 47-script reference/exclusion, seven unlaunched FP/provider
slots and eight original whole SOURCE gaps remain separate and unchanged.
The bounded 1,239 prior INPUT records and 22 exact-history bridge gaps do not
establish global absence, historical/current equivalence or 1,197 reconstructed
native histories. Every literal 203-word decimal/f64/f32 array, full script,
event/order/frame/rate/block/tail/default omission and supplied context is
retained in the approved mapping. No native law or new A1 emission follows.

Exactly 162 children were attempted once: 161 approved, APCS-0162 guardFAIL U
and 307 unattempted U. Accepted groups are oscillator 26, noise 21, filter 75,
voices 2, routing 22, drive 14 and output 1. The failed output history carries one
alias; unattempted histories carry 316 aliases. The sole peer verifies correct
failed process geometry and legal flags, but rejects its nonzero CalcA return
projection under the unchanged strict return 0 guard. Its finite diagnostic raw,
exit 0 and completed same-child calls are not an accepted observation, metric,
expectation, case or grade. Stale RUNNING with end fields, failure and partial
history remain exact. No return ABI/meaning/cause, retry, automatic continuation
or opaque-policy transfer is inferred. All prior p00–09, failed p04/p05 and
the exact D09 four remain unchanged and unreplayed.

All nine omitted-input contexts covering sixteen setter-tail aliases were
unattempted. Their literal omission remains; no input-zero command is inserted.
The conditional NULL-input byte-fill SOURCE premise is associated with the
same unchanged admitted model only. It is not an actual observation of those
tails, compiled-source/current consumption proof, explicit-input command/log
equivalence or a general default-input law. FTZ/provider variants stay U; source
envNone, literal TIME and import/table/executed-version/public associations
retain their recorded qualifications. Reset is absent from this supplied class;
an early chat-only assumption was corrected before native calls. Eight existing
command verbs and source geometry establish no unlimited process/completion law.

The accepted 161 account for 59,432 selected exports, 26,266 CalcA projections,
107,414,640 raw stereo bytes and 161 separately logged initializers; nested/all
native work stays unknown. All accepted renders are finite, BOTH nonzero and
stereo-word-equal; 144 raw hashes and 70 counted Linux names are descriptive
references only. All new waveform priors, native waveform expectations,
portable expected values/comparators and grades remain NULL; application proof
is false. Neither equality/nonzero/silence nor a waveform hash is a new guard,
portable criterion, productivity, capacity, release, causal or public/ARM law.
Strict CalcA return 0 / flags 0 or 1 and every other existing guard remain; D09 and
other opaque policies do not transfer. Rate is opaque; the frozen parser lacks
an explicit int64 range guard, while the sole peer checked the retained Rate
values within int64. No frozen repair or domain/meaning law follows.

The sole review checks 524 runtime/common-frozen before/after endpoint pairs
for each of 162 attempts (84,888 pairs), not continuous loaded-provider/FP,
OSexec or source-to-compiled attestation. Accepted raw fsync branch progress is
inferred from SOURCE/RECORDED state, without a separate syscall-receipt boolean;
failed raw skipped that branch. Log/JSON requests do not prove directory/crash
durability; outer recorder redirection has no explicit FDfsync. Child 20-second
CPU/wall, core-zero and file bounds do not imply a parent 20-second watchdog. Existing cleanup,
uncatchable/escaped-descendant, transitive-library, within-child detection and
overshoot limitations remain. The complete 6,991,975,856-byte fresh requirement
retains full remaining raw, 8MiB logs and 4MiB metadata per future child,
512MiB final/review/owner, 128MiB headroom and 256MiB concurrent allowance, retaining
the old Analog floor. It is an unreserved planning estimate, not quota or a
hard aggregate bound, with external writers/within-child/finalization limits.

Only this annex and revision metadata change. All 23 whole requirements,
72 literal rows, 1,197 old IDs, R3–R14 objects, criteria/U/state/history,
old 14+5 ASOF, mandatory MPE amount 0.5 qualification, old count/failure/D09
dispositions and immutable release 38 groups/42 evaluations remain exact.
Full reversal restores the exact 124,809-byte R14 owner. Navigation totals
1,358 IDs are not passes or whole-product coverage. Required unsupported
behavior remains U, whole-Live coverage OPEN; no new release or application grade.
