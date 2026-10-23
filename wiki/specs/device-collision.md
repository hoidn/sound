---
id: SPEC-DEVICE-COLLISION
type: spec
status: draft
updated: 2026-10-21
access: analysis
revision: 7
target: Ableton Live 12 Suite 12.4.3 / macOS; reference renders from the Collision.bundle x86_64 slice
---

# Collision instrument: signal behavior and reference renders

## Scope

Feature FEAT-DEVICES, T1 device audio ([ADR 0004](../decisions/adr-0004-target-scope-t1.md)).
The user task is to render a track containing Collision from note events and parameter values.
This partial draft specifies the retained instrument outputs and selected timing, pitch,
resonator, mallet, level, note-off and voice behavior at 44.1 and 48 kHz.

Parameter storage, domains and absent-field defaults belong to
[SPEC-BUNDLED-DEVICE-PARAMETERS](bundled-device-parameters.md). Track routing and event delivery
belong to playback and mix-graph specifications. This draft does not replace those contracts.

Every requirement is a **proposed contract**. Evidence is extracted execution of the original
x86_64 device code, static parameter mapping and shipped presets. No whole Live run or
candidate comparison was performed. This is not a compatibility pass or released implementation
input. Canonical evidence is [Collision DSP](../research/device-collision-dsp.md).

Apart from the twelve exact supplied-host Resonator1 enable histories under 017,
excluded or explicitly unresolved: statistical grading of high-noise settings; complete
mode amplitudes; the position rescale; LFOs, controllers, MPE, retrigger, general dynamic
parameter changes, rate changes, persistence/undo, malformed input and CPU/latency behavior.

## Evidence labels and assumptions

| Label | Meaning |
| --- | --- |
| D | Directly present in identified shipped files |
| S | Static derivation, without a Live run |
| S-cond | Static derivation conditional on a named assumption |
| X | Extracted x86_64 original-code execution for the specified calls and substitutions; does not establish that Live makes those calls |
| U | No settled expectation or comparator; ungraded |

| ID | Assumption | Affected clauses |
| --- | --- | --- |
| A1 | Stored HitX, ListeningXL and ListeningXR pass to the bundle unchanged, as N6 traces. Shipped previews support this most strongly for listening, but do not observe Live's calls | 002, 007; every fixture interpreted as a stored-value scenario |
| A2 | The device receives the sample-rate, warm-up, parameter, event, transport and input-flag protocol of 001 | All audio expectations; Live's event base, block partition, grid phase and activity handling remain unknown |
| A3 | The proposed fixture metrics below are accepted for the bounded T1 scope | Candidate acceptance; currently unresolved under Q-025 |

U clauses block the behavior they name. They do not invalidate a retained X observation in its
stated harness protocol. Proposed comparisons below are not executed or accepted comparisons.

## Requirements

### REQ-DEVICE-COLLISION-001 — retained render protocol

- **X.** A reference render starts with a fresh instance, sets 44,100 or 48,000 Hz, sends all
  139 host values in index order, and processes silent input with flag 0 and transport
  {not playing, position 0, 120 BPM}. It warms up for 11,264 or 12,288 frames respectively in
  512-frame blocks, then renders the event sequence. Event frame 0 and WAV frame 0 are the
  first frame after warm-up. Control-grid phase persists and the warm-up spans whole periods.
- **X.** Outputs are stereo binary32 with the stated frame count. Rerunning the preset,
  using blocks of 64, 256 or 2,048 frames, setting flush-to-zero/denormals-are-zero, and the
  tested reset sequence leave it bit-identical. Block 333 shifts the first note by one period;
  compensating that shift leaves 9.31 × 10⁻¹⁰ maximum difference.
- **X.** The clock seed affects the mallet even at NoiseAmount 0. The fixtures fix the clock
  at 0. A candidate need not reproduce the substituted generator's samples, provided the
  applicable accepted metric accounts for this randomness.
- **U.** Live's complete host protocol and arm64 output differences. T1 effect: expectations
  are conditional on A2 and are not general Live or arm64 equivalence.

### REQ-DEVICE-COLLISION-002 — parameter sets and conversion

- **S.** The 139 host indices correspond to N6's Collision table, with no second outputs.
  Note-off decay is sent as 1 − stored value; legacy integer fields use N6's rounding/truncation;
  LFO targets use their lookup tables, and target amounts scale by 0.125 for target 4 or 9.
- **D, S.** The constructor parameter set disables both resonators. The shipped Defaults
  preset changes the sent Resonator1/OnOff value to 1. At binary32 precision it changes no
  other sent value. Its stored PerNotePitchBendRange difference is not sent by this table.
- **S-cond (A1).** Position values pass unchanged. This contract defines host-value fixtures
  independently of whether A1 is accepted for stored-value input.
- **U.** N6's two VelToStartTranspose range mismatches and resonator-2 Type 6 mismatch are
  not exercised here. Their stored-value audio behavior remains excluded from T1 acceptance.

**X, finite supplied-host integer observations (revision 3).** The [complete catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-collision-r3-kind3-finite-v1/cases86.json)
adds DCL-063–146 for84 approved once-only host-input observations, covering
20 nonvirtual native-kind3 domains at the exact preset history below.
They do not validate general stored-value conversion, ordinary Live emission,
parameter effects or public A1/A2/ARM behavior. Native index59 retains max5;
N6's stored/emitted Type6 mismatch and all existing U remain unresolved.
The failed index58=1 history and input-only baseline receive no success case.
Fresh waveform priors, portable expected/comparator and grades remain NULL.

### REQ-DEVICE-COLLISION-003 — enabled resonators and order

- **X.** With constructor parameters, C4 produces only a residual of at most 4.01 × 10⁻²².
  With the Defaults preset it sounds (reference peak 0.110951).
- **X.** For order 1, either resonator can sound independently. At identical settings,
  resonator 2 alone reproduces resonator 1 alone bit-for-bit in the measured case.
- **X.** For order 0, resonator 2 alone is effectively silent. Resonator 1 excites resonator 2
  even when resonator 1's audible Volume is 0; changing resonator 1's pan or swapping its
  pickups then does not change the resonator-2 output in the tested case.
- **X.** The serial combined output equals its separately muted components within
  1.87 × 10⁻⁸ for that same-instance-setup comparison. Parallel fresh-instance sums differ
  by up to 6.97 × 10⁻⁵. Exact additive identity across fresh instances is not required.

### REQ-DEVICE-COLLISION-004 — note event timing

- **X.** At fixed host block size B, let P = floor(fs/1000), g = P floor(f/P), and
  b = B floor(f/B). An event at frame f first changes the output at g if g ≥ b, otherwise
  g + P. There is no further one-frame offset. The grid starts at render frame 0 under 001.
- **X.** This rule covers 336 note-ons at 44.1 kHz (B = 512, 64, 333) and 48 kHz (B = 512),
  and 44 note-offs at 44.1 kHz (B = 512, host DecayOnNoteOff 0.5). Changed frame means a
  difference from the corresponding no-event/held-note reference, not an audible threshold.
- **U.** Nonuniform partitions, simultaneous event ordering, fractional event time and
  Live's grid phase. T1 effect: only the specified partitions/events have timing expectations.

- **X finite supplied independent MIDI-byte observations; U portable acceptance
  (revision 4).** [DCL-147–303](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-collision-r4-independent-midi-finite-v1/new-cases157.json) add157 once-only
  histories in the exact DCL-054 no-setter recipe:127 Off-key-only values,
  15 On-channel-only values and15 Off-channel-only values. The opposite key
  or channel stays fixed; no crossproduct or timing change. Three baseline
  aliases inherit ONE DCL-054 INPUT reference without replay/new PID/receipt/
  metric/criterion transfer. These supplied-byte observations do not extend
  the older004 timing rule or establish unmatched-note release, channel/voice
  handling, internal admission or Live/ARM law. Fresh waveform priors/new
  expectations, portable expected/comparator/grade remain NULL; new application
  predicate proofs remain false. All older criteria and general U retain scope.

- **X finite supplied DCL054 MIDI-axis observations; U portable acceptance
  (revision 5).** [DCL-304–826](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-collision-r5-dcl054-five-midi-axes-finite-v1/new-cases523.json) add523 once-only
  histories:127 On-key-only,127 matching-key,127 On-velocity,15 matching-channel
  and127 Off-velocity inputs. These five independent axes retain the fixed
  no-setter DCL-054 recipe; there is no crossproduct, timing or state change.
  Five baseline aliases share ONE inherited DCL-054 INPUT reference without
  replay, fresh PID/receipt/metric/output or criterion transfer. No new general
  event matching, velocity-zero, note-off, channel/voice, timing, productive
  effect, public/ARM or physical law follows. New waveform priors/expectations
  and portable expected/comparator/grade remain NULL; new application-predicate
  proofs remain false. All prior criteria and general U retain scope.

### REQ-DEVICE-COLLISION-005 — modal pitch

- **S, X.** Nominal modal pitch is 261.62 A(p) Hz, with
  p = KeyToTranspose(key − 60)/12 + Transpose/12 + FineTranspose/1200.
  For n = floor(x), t = (x − n) ln 2,
  A(x) = 2ⁿ[1 + t + t²(0.5 + 0.200064t)]. Pole frequencies also depend on binary32 rounding.
- **X.** String Quality 0 gives C4 261.62391/261.61277 Hz and A4 440.33104/440.33945 Hz at
  44.1/48 kHz. The 34 measured cases span keys 24–108, transpose ±48, fine tune ±50 and
  KeyToTranspose −1, 0, 0.5, 2; frequency-bound residuals are below 0.67.
- **U.** Unmeasured extreme combinations and pitch clamps. Pipe and Tube use 014 instead.

### REQ-DEVICE-COLLISION-006 — modal resonator outputs

- **S, X.** Beam, Marimba, String, Membrane and Plate have the modal families represented by
  the reference fixtures. Quality caps are 4, 16, 30 and 70 modes, with higher-frequency
  modes excluded at 5fs/12. Inharmonicity, material, decay, brightness and ratio change their
  poles and relative levels as the retained renders show.
- **X, bounded.** The 37-setting study estimates only sufficiently strong, separated modes.
  It supports the fixture pole comparisons below; it does not establish every mode, an exact
  full waveform or an absolute gain formula.
- **U.** The estimator resolves no modes for Membrane Ratio 0.75 (DCL-014). Its render is
  retained but has no acceptance criterion. Closely spaced, weak and excluded modes are also
  ungraded. T1 effect: these modal portions remain incomplete.

### REQ-DEVICE-COLLISION-007 — hit and listening positions

- **X.** Host HitX 0, 0.25, 1 and host ListeningXL/ListeningXR 0/0.5 produce the retained
  spectral and channel-weight changes. They do not move the resolved modal poles beyond the
  metric's frequency bounds.
- **S-cond (A1).** The same fixtures apply to those stored positions if unchanged conversion
  is accepted. The shipped-preview evidence favors unchanged listening positions over an
  additional bipolar conversion in all 29 discriminating previews.
- **U.** The full Live-side mapping and untested position combinations remain open. Preview
  generation settings are unknown; hit evidence is mixed (19 versus seven presets).

### REQ-DEVICE-COLLISION-008 — mallet excitation

- **S, X.** Mallet Volume spans an exponential 0.001..1 and Stiffness an exponential
  2..5,000 Hz, with frequency clamped to 10..20,000 Hz. Normalized controller is 128v for
  v ≤ 0.5, otherwise 126v + 1; these exponential controls take its floor. Selected
  stiffness and volume changes have the retained response.
- **S, X.** The pulse is shaped by a second-order low-pass and multiplied by a blend of a
  constant and filtered noise. The noise share is (atan(a)/π + 0.5)³ for its quantized −4..4
  amount. Host NoiseAmount 0 still gives share 0.0004742; 0.5 gives 0.125; 1 gives 0.78383.
- **U.** Complete NoiseColor/velocity/key modulation laws and an exact portable pulse
  waveform. High-noise settings wait for 015's comparator.

### REQ-DEVICE-COLLISION-009 — measured velocity and key response

- **X.** With zero modulation amounts, velocities 1, 64, 127 and 100 give identical output.
- **X, fitted.** For Mallet VelToVolume amounts −2.5, 1, 2.5 and 5, the measured gain relative
  to zero amount is 20 log10(2) × 0.96856686 × amount × (velocity − 64)/63 dB, within 0.00702 dB.
  KeyToVolume uses the same fitted factor with (key − 60)/12 for the sampled keys 36, 48,
  72, 84 and amounts ±1. These fits do not establish arbitrary continuous-value equality.
- **X, partial.** VelToStiffness 2.5 at velocity 127 gives the retained DCL-025 response.
  The general stiffness modulation law is unknown; the volume fit must not be reused for it.

### REQ-DEVICE-COLLISION-010 — output level and pan

- **X.** Measured settled gain changes are:

  | Control | Host value | Gain relative to reference |
  | --- | --- | --- |
  | Volume (reference preset 0.7047892213) | 0 / 0.25 / 0.5 / 1 | silent / −17.92572 / −6.02077 / +6.02043 dB |
  | Resonator Volume (reference 0.5) | 0.25 / 0.5 / 1 | −11.90495 / 0 / +12.04120 dB |
  | Pan | −0.5 | left unchanged; right −6.02060 dB |
  | Pan | +0.5 | right unchanged; left −6.08926 dB |

- **X.** Pan endpoints mute the opposite channel to the tiny residual floor. A newly created
  instance with Volume 0.25 starts with the initial unity gain and reaches the settled gain
  by frame 44 in the measured 44.1 kHz case. Fixture warm-up avoids this transient.
- **U.** Full gain interpolation and dynamic smoothing remain unspecified.

### REQ-DEVICE-COLLISION-011 — note-off decay

- **X.** At stored DecayOnNoteOff 0 (host 1), releasing a note does not change the tested
  render relative to holding it. For String Quality 0, Decay 0.75, held T60 is about 5.738 s.
  Host note-off decay 0, 0.1, 0.25, 0.5, 0.75, 0.9, 1 gives fitted post-off T60
  0.04267, 0.04748, 0.13370, 0.75388, 2.42403, 4.15801, 5.73441 s.
- **U.** A general law for all types, decay settings and very short tails. T1 acceptance is
  restricted to these measurements and retained DCL-028.

### REQ-DEVICE-COLLISION-012 — voices and stealing

- **X.** Polyphony indices 0–8 allow respectively 1, 2, 4, 6, 8, 10, 12, 14, 16 sounding
  voices in the 24-sequential-held-note test. The most recent notes survive.
- **X.** With one voice, C4 then G4 at frame 11,025 replaces C4 at grid frame 11,000. The
  residual against G4-only is at most 6.24 × 10⁻⁶ over the next 4,096 frames.
- **U.** Repeated keys, released-voice preference, retrigger modes and other stealing sequences.

### REQ-DEVICE-COLLISION-013 — sampled pitch envelope

- **X, partial.** For String Quality 0, Decay 1, StartTranspose 1, StartTime 0.5, the
  20 ms spectral windows beginning 10, 20, 50, 100 ms after onset give approximately +6.54,
  +4.55, +1.41, +0.0024 semitones relative to 261.62 Hz. DCL-030 retains this trajectory.
- **U.** Exact trajectory law, unmeasured times, key/velocity amounts and N6's range mismatch.

### REQ-DEVICE-COLLISION-014 — selected Pipe and Tube output

- **X.** At C4 with Decay 1 and the Q parameter set, Pipe/Tube fundamentals are
  251.09609/241.36376 Hz at 44.1 kHz and 251.27072/241.68681 Hz at 48 kHz. Both channels
  are identical in these probes. DCL-031/032 retain the 44.1 kHz outputs.
- **X, partial.** Pipe radius 1 gives 258.33884 Hz; opening 0.3 gives 234.44411 Hz. Tube
  radius 0 gives a short-lived spectral peak at 173.47582 Hz, not an established steady pole.
- **U.** Full pitch/decay laws, other parameter combinations and arm64 waveform tolerance.

### REQ-DEVICE-COLLISION-015 — noise fixtures are ungraded

- **X.** Nine seed-ensemble cases retain one seed each and ensemble summaries: preset,
  mallet Amount 1 and Color 0, noise-only LP/HP/BP/LP+HP, ADSR and Sustain 1. Noise
  Volume and velocity have sampled gain measurements in the analyst evidence.
- **U.** Their statistical acceptance metric. Four-versus-four-seed spectra differ by up to
  7.899 dB, and envelope differences have 90th percentile up to 8.185 dB. Neither a single
  retained seed nor these unstable summaries defines a tight portable noise requirement.
  DCL-033–041 are ungraded. T1 noise coverage remains partial.

### REQ-DEVICE-COLLISION-016 — modulation and other MIDI behavior

- **U.** LFO shapes/routing/sync, pitch bend, CC, pressure, MPE, retrigger and release-velocity
  effects. The static parameter table establishes available controls, not their audio result.
  No acceptance case for these paths is graded in this revision.

### REQ-DEVICE-COLLISION-017 — parameter and sample-rate transitions

- **X.** Setting 44.1 then 48 kHz after parameters differs from the direct-48-kHz Q render
  by 9.76 × 10⁻⁵ relative RMS. No general rate-change identity is required.
- **U.** Active-note automation timing, smoothing, reset during a note, rate changes during
  sounding and transport-dependent behavior. Fixed-parameter fixtures do not cover these.

- **X, finite supplied-host histories.** The [revision 2 catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-collision-r2-finite-v1/case-catalog.json)
  retains all twelve DCL-051–062 histories for Resonator1/OnOff (host index 25),
  with resonator 2 disabled at index 58. It includes eight Boolean initial/sent
  transitions across held/note-off histories and four matched no-setter controls.
  Every case uses its exact 139-value prefix and the protocol below. All eight
  pre-change prefixes match their controls. Repeated-setter suffixes match in the
  four selected histories; the four changed-state suffixes differ. OFF→ON maximum
  absolute differences are only about 6.6 × 10⁻²⁰: this does not establish audibility,
  a new note or a productive post-setter effect. ON→OFF differences and repeated-setter
  equalities are also finite observations, not general mode/no-effect/smoothing laws.
  The retained raw hashes identify evidence; they are not a portable candidate
  waveform criterion. No new calibration/tolerance is defined. General automation
  timing, Live A1/A2, reset/rate behavior and Apple/arm64 results remain unknown.

### REQ-DEVICE-COLLISION-018 — persistence, errors and teardown boundaries

- **X, limited.** Fixture scripts create and destroy a fresh device and finish rendering finite
  outputs. This is not a complete teardown/error-path contract.
- **U.** Device state round trips, undo/redo, cancellation, malformed/NaN/out-of-domain event
  and parameter inputs, invalid rates, concurrent use and fault recovery. These are omitted
  from graded cases because this packet has no retained expectations for them. UI, file
  format and real-time performance have no acceptance claim here.

## Proposed comparison metric

This proposal applies only to the fixed-parameter fixtures below; A3 remains open. No comparison
has run. Thresholds are not a global proof for unmeasured settings or arm64.

| Quantity | Comparator | Proposed bound |
| --- | --- | --- |
| Event frame | Difference from matching no-event/held-note render | Exact grid rule for the tested cases |
| Effectively silent constructor | Peak absolute sample | ≤ 10⁻¹⁸ |
| Modal frequency | Same estimator, same resolved modes in reference and candidate | Relative error ≤ 4F(f,fs), F = 3 × 2⁻²⁵/(2πf/fs)² + 2⁻²³ |
| Modal decay | Per-frame natural-log pole radius | Absolute difference ≤ 8 × 2⁻²⁵ |
| Modal complex amplitude | Same fit and note-relative origin; compare to reference without fitting away candidate gain | Relative difference ≤ 0.05 on graded modes |
| Modal onset | First 256 frames after reference onset, stereo relative RMS | ≤ 0.005 |
| Waveguide fixtures | Frequency and whole-window stereo relative RMS | Frequency ≤ 4F; relative RMS ≤ 0.003 (provisional; Pipe libm calibration only) |
| Pitch-envelope fixture | Same 20 ms spectral-window method at 10, 20, 50, 100 ms | Each within 0.2 semitone of reference; plus onset metric |
| Sampled gains | Least-squares settled gain relative to matching reference control | 0.02 dB; mute paths use 10⁻¹⁸ peak |
| Random/noise cases | No accepted comparator | U |

Modal comparisons use the already resolved reference-mode rows marked weight ≥ 0.01 in
`results/collision.json`; unmeasured modes do not acquire a pass. A fixture with no resolved
modes is U. Comparing normalized model amplitudes alone cannot test candidate absolute level.

Calibration: one-ulp libm variants reach 0.001087 onset relative RMS, 0.09072 over long modal
windows, 0.671 frequency bounds and 0.000611 whole-window Pipe relative RMS. Resolved static
model residuals reach 3.385 frequency bounds, 4.897 log-radius bounds and 0.02568 normalized
amplitude. The proposed bounds cover those observed residuals, but Tube, seed and arm64
calibration are incomplete. A release review must decide the permitted fixture scope and
accept the metric; noise stays U rather than receiving an enlarged tolerance.

## Acceptance cases

The packet [manifest](../../analysis/ableton-live-12.4.3/r2/t12-collision-v1/manifest.json)
owns full hashes, and `raw/<fixture>.script` owns exact calls. WAVs are stereo IEEE binary32.
Each table hash is a locator prefix of the full SHA-256, not a separate digest.
Two logical source/result paths were concurrently edited after the initial audit; all references
here to `run_collision.py` and `results/collision.json` use the exact-hash recovered originals
in the research page's [mapping](../research/device-collision-dsp.md#concurrent-edit-incident-and-recovered-originals).
The concurrent `extras` section is excluded. Retained WAV/script pairs are unchanged.

Parameter sets: **PRESET** is all 139 host values derived from the shipped Defaults preset;
**Q** is PRESET with host Mallet/NoiseAmount 0 (still slightly random). **CTOR** is the sent
constructor values. Unless a row says otherwise, fixtures use Q, C4 velocity 100 on frame 0,
held, 32,768 frames at 44.1 kHz after 001's warm-up. Changes below are **host values**. A
stored-value interpretation is conditional on 002 and A1. Scripts resolve any omitted detail.

Kinds: P positive, B boundary, T timing, U ungraded. “Audio” denotes a **proposed** comparison
using the applicable metric lines; it is not an observed candidate pass.

| Case ID | Requirement | Kind | Setup (Q plus host changes unless stated) | Expected comparison | Fixture, WAV SHA-256 prefix |
| --- | --- | --- | --- | --- | --- |
| DCL-001 | 001, 002, 003 | B | CTOR; C4 on 4,096, off 26,146; 22,050 frames | Peak ≤ 10⁻¹⁸ | `ctor_c4`; `775d38f661412aed` |
| DCL-002 | 001, 002, 003 | P | PRESET; C4 on 4,096, off 26,146; 44,100 frames | Audio; onset 4,136; peak 0.110951 | `preset_c4`; `d57ce2f393d218d1` |
| DCL-003 | 005, 006 | P | Resonator1/Quality 3; Resonator1/Decay 0.75 | Audio, resolved modes | `mode_beam_high`; `3386a94e34d9a17e` |
| DCL-004 | 006 | P | Resonator1/Type 1; Resonator1/Quality 3; Resonator1/Decay 0.75 | Audio, resolved modes | `mode_marimba_high`; `ed3381658b03cba5` |
| DCL-005 | 005, 006 | P | Resonator1/Type 2; Resonator1/Quality 3; Resonator1/Decay 0.75 | Audio, resolved modes | `mode_string_high`; `ebc98f66d48430ac` |
| DCL-006 | 006 | P | Resonator1/Type 3; Resonator1/Quality 3; Resonator1/Decay 0.75 | Audio, resolved modes only | `mode_membrane_high`; `bcc3f4292f3420bc` |
| DCL-007 | 006 | P | Resonator1/Type 4; Resonator1/Quality 3; Resonator1/Decay 0.75 | Audio, resolved modes only | `mode_plate_high`; `3f11308fdb9d2ea4` |
| DCL-008 | 001, 005, 006 | P | Resonator1/Quality 3; Resonator1/Decay 0.75; 48,000 Hz | Audio at 48 kHz | `mode_beam_48`; `0e94d91071cef1d2` |
| DCL-009 | 006 | B | Resonator1/Type 2; Resonator1/Quality 1; Resonator1/Decay 0.25 | Audio, resolved modes | `decay_0.25`; `51411db9fef67f84` |
| DCL-010 | 006 | B | Resonator1/Type 2; Resonator1/Quality 1; Resonator1/Decay 0.75; Resonator1/Damp -1 | Audio, resolved modes | `material_-1`; `80433981e1413a6b` |
| DCL-011 | 006 | B | Resonator1/Type 2; Resonator1/Quality 1; Resonator1/Decay 0.75; Resonator1/Damp 1 | Audio, resolved modes | `material_1`; `3233563212296e4e` |
| DCL-012 | 006 | P | Resonator1/Type 2; Resonator1/Quality 1; Resonator1/Decay 0.75; Resonator1/Inharmonics 0.5 | Audio, resolved modes | `inharm_0.5`; `832649f355d82924` |
| DCL-013 | 006 | B | Resonator1/Type 2; Resonator1/Quality 1; Resonator1/Decay 0.75; Resonator1/AmpFreq 1 | Audio, resolved modes | `bright_1`; `298554e8923adae3` |
| DCL-014 | 006 | U | Resonator1/Type 3; Resonator1/Quality 1; Resonator1/Decay 0.75; Resonator1/Ratio 0.75 | U: zero modes resolved | `ratio_3_0.75`; `4073560c607324ef` |
| DCL-015 | 006 | P | Resonator1/Type 4; Resonator1/Quality 1; Resonator1/Decay 0.75; Resonator1/Ratio 0.75 | Audio, resolved modes | `ratio_4_0.75`; `073b8ada9d9cc94e` |
| DCL-016 | 007 | B | Resonator1/Type 2; Resonator1/Quality 1; Resonator1/Decay 0.75; Resonator1/HitX 0 | Audio, resolved modes | `hit_0`; `0b4c465c5bd6c075` |
| DCL-017 | 007 | P | Resonator1/Type 2; Resonator1/Quality 1; Resonator1/Decay 0.75; Resonator1/HitX 0.25 | Audio, resolved modes | `hit_0.25`; `cab5f3fff74b9c0a` |
| DCL-018 | 007 | B | Resonator1/Type 2; Resonator1/Quality 1; Resonator1/Decay 0.75; Resonator1/HitX 1 | Audio, resolved modes | `hit_1`; `eaab61ddebcfcde1` |
| DCL-019 | 007 | P | Resonator1/Type 2; Resonator1/Quality 1; Resonator1/Decay 0.75; Resonator1/ListeningXL 0; Resonator1/ListeningXR 0.5 | Audio, both channels | `listen_L0_R0.5`; `1486ad0eb4d5f4e8` |
| DCL-020 | 003, 005, 006 | P | Resonator1/OnOff 0; Resonator2/OnOff 1; Resonator2/Type 1; Resonator2/Transpose 7; Resonator2/Decay 0.75; ResonatorOrder 1 | Audio, resolved res2 modes | `res2_marimba_tr7`; `a886a12cfc79e6af` |
| DCL-021 | 008 | P | Mallet/Stiffness 0.15; Resonator1/Type 2; Resonator1/Decay 0.75; key 48 vel 100 on 0 | Audio, resolved modes | `stiff_0.15`; `3ffce9ade23f761d` |
| DCL-022 | 008 | B | Mallet/Stiffness 1; Resonator1/Type 2; Resonator1/Decay 0.75; key 48 vel 100 on 0 | Audio, resolved modes | `stiff_1`; `ef3fd41471451279` |
| DCL-023 | 009 | B | Mallet/VelToVolume 2.5; key 60 vel 1 on 0; 16,384 frames | Audio, velocity/key gain fit | `vel_2.5_1`; `ef24df205320a7ac` |
| DCL-024 | 009 | B | Mallet/VelToVolume 2.5; key 60 vel 127 on 0; 16,384 frames | Audio, velocity/key gain fit | `vel_2.5_127`; `26e824eb1fcf5baa` |
| DCL-025 | 009 | P | Mallet/VelToStiffness 2.5; Resonator1/Type 2; Resonator1/Decay 0.75; key 48 vel 127 on 0 | Audio only; general stiffness law U | `vstiff_2.5_127`; `4be2ec455fe8cf56` |
| DCL-026 | 003 | P | Resonator2/OnOff 1; Resonator2/Type 1; Resonator2/Transpose 7; ResonatorOrder 1 | Audio; no exact fresh-instance sum | `coupling_parallel`; `0553bfd405266792` |
| DCL-027 | 003 | P | Resonator2/OnOff 1; Resonator2/Type 1; Resonator2/Transpose 7 | Audio | `coupling_serial`; `475899a63f5e2465` |
| DCL-028 | 004, 011 | P, T | Resonator1/Type 2; Resonator1/Quality 0; Resonator1/Decay 0.75; Resonator1/DecayOnNoteOff 0.5; off 11025; 43,793 frames | Audio; post-off fitted T60 0.75388 s | `no_0.5`; `c9b6a9f022f9bc15` |
| DCL-029 | 004, 012 | P, T | Resonator1/Type 2; Resonator1/Quality 0; Resonator1/Decay 0.75; Polyphony 0; key 67 vel 100 on 11025; 22,050 frames | Audio; takeover at 11,000 | `steal_both`; `9eff0c2c802ec0fc` |
| DCL-030 | 013 | P | Resonator1/Type 2; Resonator1/Quality 0; Resonator1/StartTranspose 1; Resonator1/Decay 1 | Pitch-envelope and onset metrics | `penv_1_0.5`; `e5d20a6e05f576d5` |
| DCL-031 | 014 | P | Resonator1/Type 5; Resonator1/Decay 1 | Waveguide metric, 251.09609 Hz | `wg_pipe`; `2297f2923e68a8f6` |
| DCL-032 | 014 | P | Resonator1/Type 6; Resonator1/Decay 1 | Waveguide metric, 241.36376 Hz; calibration provisional | `wg_tube`; `5a4a3c3454a931a8` |
| DCL-033 | 015 | U | Mallet/NoiseAmount 0.5 | U: noise comparator unresolved | `noise_preset_s0`; `09b496c383bae5cb` |
| DCL-034 | 015 | U | Mallet/NoiseAmount 1 | U: noise comparator unresolved | `noise_mallet_amount1_s0`; `ec1b5d66b4eb1294` |
| DCL-035 | 015 | U | Mallet/NoiseAmount 1; Mallet/NoiseColor 0 | U: noise comparator unresolved | `noise_mallet_color0_s0`; `9465e1147adb8e07` |
| DCL-036 | 015 | U | Mallet/OnOff 0; Mallet/NoiseAmount 0.5; Noise/OnOff 1; off 13230 | U: noise comparator unresolved | `noise_exc_default_s0`; `9d84cb9e62cc696f` |
| DCL-037 | 015 | U | Mallet/OnOff 0; Mallet/NoiseAmount 0.5; Noise/OnOff 1; Noise/FilterType 1; off 13230 | U: noise comparator unresolved | `noise_exc_hp_s0`; `513dce85c8381a88` |
| DCL-038 | 015 | U | Mallet/OnOff 0; Mallet/NoiseAmount 0.5; Noise/OnOff 1; Noise/FilterType 2; Noise/Q 0.5; off 13230 | U: noise comparator unresolved | `noise_exc_bp_s0`; `0838c0d4622d66e0` |
| DCL-039 | 015 | U | Mallet/OnOff 0; Mallet/NoiseAmount 0.5; Noise/OnOff 1; Noise/FilterType 3; off 13230 | U: noise comparator unresolved | `noise_exc_lphp_s0`; `2cafdbd6464b42b4` |
| DCL-040 | 015 | U | Mallet/OnOff 0; Mallet/NoiseAmount 0.5; Noise/OnOff 1; Noise/Attack 0.5; Noise/Decay 0.5; Noise/Sustain 0.5; Noise/Release 0.5; off 13230; 44,100 frames | U: noise comparator unresolved | `noise_exc_adsr_s0`; `ba66d793dfe51066` |
| DCL-041 | 015 | U | Mallet/OnOff 0; Mallet/NoiseAmount 0.5; Noise/OnOff 1; Noise/Sustain 1; off 13230 | U: noise comparator unresolved | `noise_exc_sustain1_s0`; `1bf86a6c55057862` |

### Value checks and open cases

These cases use retained measurement rows rather than separate WAV fixtures. Input definitions
and exact sampled values are in the cited script function and result section; no new capture
or candidate execution is implied.

| Case ID | Requirement | Kind | Setup and expected result | Evidence |
| --- | --- | --- | --- | --- |
| DCL-042 | 004 | T, B | 336 note-ons and 44 note-offs at the four rate/block combinations; all changed frames follow 004 exactly | `run_collision.py:timing`; `collision.json:timing` |
| DCL-043 | 012 | P, B | 24 held notes 48, 50, …, 94, every 2,000 frames; all nine Polyphony indices leave 012's listed voice counts and most recent notes | `run_collision.py:voices`; `collision.json:voices.polyphony` (counts in 012) |
| DCL-044 | 003 | P, B | Both orders × resonator-enable combinations 00/10/01/11; order 0 with only res2 is silent; order 1 lets either sound; identical single-resonator settings match | `run_collision.py:root_cause`; `collision.json:root_cause.topology` |
| DCL-045 | 009, 010 | P, B | Sampled velocity/key and Volume/resonator-Volume/pan settings meet their measured gain tables and fits | `run_collision.py:velocity,levels`; corresponding JSON sections |
| DCL-046 | 011 | P, B | Default note-off equals held output exactly; host decay sweep gives 011's post-off fitted T60, within 1% for host ≥ 0.25 (shorter-tail tolerance U) | `run_collision.py:noteoff`; `collision.json:noteoff` |
| DCL-047 | 016 | U | LFO, CC, pressure, pitch bend, MPE, retrigger and release velocity | No graded expectation |
| DCL-048 | 017 | U | Active-note automation, arbitrary partitions, reset/rate/transport changes | No graded expectation |
| DCL-049 | 018 | U | Persistence, undo, malformed input, cancellation and fault/teardown paths | No graded expectation |
| DCL-050 | 002, 007 | U | Full Live position mapping and N6 mismatches, including res2 Type 6 | Preview support is partial; no traced-call expectation |

### Revision 2 finite same-instance enable histories

The [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-collision-r2-finite-v1/case-catalog.json) defines DCL-051–062 as twelve new finite reference
histories under 017, including all four matched control histories. Their inputs
are new; they do not regrade an old capture. All 50 prior rows/IDs remain exact,
including DCL-048's general U. This revision has 18 requirements and 62 case IDs.
The eight `COLLISION-ENABLE-PAIR-001–008` relations compare named cases and are not
eight additional cases, grades or an atomic behavior denominator.

Each case creates an instance, sets 44,100 Hz and sends all 139 ordered preset
host words, changing only initial index 25; index 58 remains 0. It processes
11,264 silent warm-up frames before queuing C4/100 at frame 4,097. The note-off
history additionally sends note-off at 7,168; “released” names this message history,
not an established envelope phase or cutoff. The first segment processes 8,192
frames, followed by the named setter or no setter and a 4,096-frame segment.
All blocks are 512 frames, with silent input, input flag 0 and stopped transport
at position 0/120 BPM. The original instance persists until destruction.

The recorded driver's event counter restarts at zero on each process command.
Both event coordinates are inside the first [0,8192) interval and strictly outside
the second [0,4096) interval, so neither event is replayed. Warm-up precedes event
queueing and cannot receive these events. The retained output includes all 23,552
frames (warm-up and both segments); the device state/grid is not reset between
segments. This is the supplied experimental protocol, not a public Live clock law
or a required candidate API.

| Case ID | Requirement | Kind | Exact input history | Expected comparison |
| --- | --- | --- | --- | --- |
| DCL-051 | 017 | Finite control | Initial25=0; no setter; held; `initial0-no-setter-held` | Retained finite observation X; portable candidate comparator U |
| DCL-052 | 017 | Finite control | Initial25=0; no setter; released; `initial0-no-setter-released` | Retained finite observation X; portable candidate comparator U |
| DCL-053 | 017 | Finite control | Initial25=1; no setter; held; `initial1-no-setter-held` | Retained finite observation X; portable candidate comparator U |
| DCL-054 | 017 | Finite control | Initial25=1; no setter; released; `initial1-no-setter-released` | Retained finite observation X; portable candidate comparator U |
| DCL-055 | 017 | Finite transition | Initial25=0; send 0; held; `initial0-send0-held` | Retained finite observation X; portable candidate comparator U |
| DCL-056 | 017 | Finite transition | Initial25=0; send 0; released; `initial0-send0-released` | Retained finite observation X; portable candidate comparator U |
| DCL-057 | 017 | Finite transition | Initial25=0; send 1; held; `initial0-send1-held` | Retained finite observation X; portable candidate comparator U |
| DCL-058 | 017 | Finite transition | Initial25=0; send 1; released; `initial0-send1-released` | Retained finite observation X; portable candidate comparator U |
| DCL-059 | 017 | Finite transition | Initial25=1; send 0; held; `initial1-send0-held` | Retained finite observation X; portable candidate comparator U |
| DCL-060 | 017 | Finite transition | Initial25=1; send 0; released; `initial1-send0-released` | Retained finite observation X; portable candidate comparator U |
| DCL-061 | 017 | Finite transition | Initial25=1; send 1; held; `initial1-send1-held` | Retained finite observation X; portable candidate comparator U |
| DCL-062 | 017 | Finite transition | Initial25=1; send 1; released; `initial1-send1-released` | Retained finite observation X; portable candidate comparator U |

The catalog retains every exact parameter token/binary32 word, script/input/capture
pointer, per-segment peak/RMS/channel summary and all eight pair relations. Enabled
pre-change controls peak at about 0.110951, versus about 4.00008 × 10⁻²² for their
disabled controls. This productive finite contrast is not a new silence threshold
or physical calibration. All pre-change matched prefixes are byte-identical; the
relation data preserve the four changed and four equal suffixes, including every
tiny OFF→ON difference. All pre-run predictions in the immutable capture remain
null. New portable candidate comparators and candidate grades remain null: neither
raw SHA equality nor an invented tolerance is an acceptance rule for these cases.
The proposed metric above is unchanged and is not extended to these histories.
The published device-collision-v1 retains only its two accepted criteria.

The actual evidence is the [whole12 batch](../../analysis/ableton-live-12.4.3/full-spec-v1/batch-collision-resonator-enable-histories-v1/manifest.json)
(SHA-256 `06896e58bf5fd69a499b03ab4af82cefb5ac940df54f636df76017c879907f0b`),
approved by its [independent actual review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/collision-resonator-enable-histories-v1-review.json)
(SHA-256 `e899873b4bd4335aedc83013739fd8875d9d465db32d6daa929e70601131d086`).
This adoption inherits that review and checks only added wording, preservation and
mechanical mapping. The actual packet is byte-sealed with files at mode 0664,
not OS-enforced read-only. The capture's grouped end-of-child checks, selected runtime
pins/import counts and ordinary-close/hash without explicit fsync retain their
limits. No original is rerun, no general deterministic/no-effect/automation law is
created, and all broader U clauses stay open. Neutral fixtures and any later
handoff are separate work; existing releases are unchanged.

### Revision 3 finite native integer host observations

The [86-history catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-collision-r3-kind3-finite-v1/cases86.json) and [105-alias joins](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-collision-r3-kind3-finite-v1/joins105.json) enumerate all20 nonvirtual
native-kind3 domains,105 index/value aliases and86 complete histories.
Twenty baseline aliases share one retained input; each other history changes
one host word only. No continuous-control partition, virtual domain,
parameter/event crossproduct or arbitrary first-N sampling is implied.
Resonator1 Type26 has native0..6; Resonator2 Type59 has native0..5.
N6's different stored/emitted0..6 metadata does not widen this native class,
repair a conversion or prove actual Live input admission.

Exactly84 histories receive new observation IDs DCL-063–146 in index/value
order. The first15 observations are inherited from the [sole partial approval](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/collision-kind3-host-domains-v1-partial-review.json),
SHA256 `011fa84e0d430dfe31df3111ed1958a8c37789b6d3e13c633fb84e5cad616adc`;
the other69 are inherited from the [sole continuation approval](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/collision-kind3-unlaunched-continuation-v1-review.json),
SHA256 `a8a1556b079394d72b09d0539ab4ffdf479a8f0223c5b14970c9e7bd12a4a87a`.
This owner joins those approved summaries only; it does not repeat actual,
source, raw, audio or numeric review. All full input words/tokens/bit patterns,
event coordinates, script/output/receipt identities and exact summary pointers
remain in the catalog. Raw hashes are provenance, not candidate criteria.
All fresh waveform priors, portable expected/comparator and grades stay NULL;
new application-predicate proofs remain false. No metric, fit, f0, window,
tolerance or physical/calibrated modal/noise expectation is introduced.

Every selected history uses all139 ordered preset host words, zero input and
input flag0, a fresh existing instance at44100Hz, stopped transport0/0/120,
clock0 and the recorded unchanged FP/provider model. It warms11264frames in
512blocks BEFORE queueing On4096/status90/key60/velocity100 and
Off26146/status80/key60/velocity0, then renders44100frames in512blocks/last68
before destruction. The complete output includes warmup. The baseline words
hash to `1a61d31521973c8eaa9167ca184704b787cda790d43db0c82a459d28caf0d0bc`.
These are driver coordinates and recorded-model histories, not Live timing,
ordinary constructor/default, current receiver or target-entry register proof.
Noise/LFO/second-resonator settings can be dormant, and both order values
remain explicit; no productive-effect, inactive-control, symmetry, equality,
repeatability, voice, smoothing or deterministic waveform law follows.

Two catalog entries remain deliberately unnumbered. `i058-v01` is the
original16th attempt: exit0/full retained audio, but24 render blocks return1
with flag1 and fail the frozen CalcAret0/flag0-or1 guard. Its success status,
native return meaning and any portable expectation remain U. The original
outer exit1, error/partial phases and stale RUNNING child label are preserved;
the recorded exit/end explain that historical label, not a running process.
The added post-capture JSON readback was NOT pre-call-bound and does not repair
the recorder. The continuation never reran this failed history or the first15;
it ran only the69 previously unlaunched IDs with the byte-identical guard.
Thus84 approved observations do not mean all85 planned new histories succeeded.

The other unnumbered entry is the historical `preset_c4` input-only baseline.
It has no approved X observation in these summaries, no newly inferred old-case
criterion, no new PID/receipt/metrics or waveform oracle, and no baseline replay.
The older twelve enable histories have different event/process histories and
provide model/protocol context only, not extra exact input intersections.
All prior observations keep their exact scope.

Both batches bind their capture/parent code and initial inputs before calls;
the partial packet's later JSON readback retains its separate post-capture
status. Source hashes and common initial-to-child-after custody are not
OSexec/build, continuous loaded-provider, source-executed-version, ABI or
native-entry FP attestation. Binding declarations stay distinct from counted
code use; selected direct exports exclude unknown nested/initializer work.
Rate's signed integer is opaque, not sample-clock/success semantics. Raw
stdout/stderr/audio close-and-hash has no explicit raw-FDfsync proof;
JSON fsync is not directory/crash durability. Post-child guards cannot retract
earlier queued calls; escaped descendants and uncatchable termination retain
their cleanup limits. No original retry or failed-guard relaxation is adopted.

Only REQ002 gains a bounded host-input qualification. The17 other whole
requirements, old002 prefix, all50 original rows plus12 revision2 rows/62 IDs,
all twelve R2 history objects/eight separate relations, old comparison metric,
noise/physical/state/error/timing/history/U/tolerances and released two cases/
two evaluations stay exact. This revision has146 navigation IDs, never passes
or an application outcome denominator. Existing releases are unchanged;
unsupported required behavior stays U and whole-Live coverage OPEN.

### Revision 4 finite DCL054 independent Off-key and channel observations

The [158-history/160-alias catalog](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-collision-r4-independent-midi-finite-v1/cases158.json) retains three complete,
independent typed axes:Off-key-only0..127 fixes On key60; On-channel-only0..15
fixes Off status80; Off-channel-only0..15 fixes On status90. No matching changes
or crossproduct is invented. DCL-147–303 label157 fresh observations (127+15+15
nonbaseline values). Three baseline aliases (Offkey60/Onchannel0/Offchannel0)
share ONE inherited DCL-054 INPUT reference, the approved
`initial1-no-setter-released` history. It receives no new ID, original call,
PID, receipt, output, metric, expectation or criterion. Full-history dedup,
not parameter-only collapse, preserves all158 histories. [All160 joins](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-collision-r4-independent-midi-finite-v1/joins160.json)
retain original139 decimal/binary64/binary32 words, complete events and
packed16 records for new histories, and exact input/output/provenance pointers.

Only Mix's [sole actual/source approval](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/collision-independent-midi-bytes-v1-review.json),
SHA256 `7ba3cc8262e08d20d411210d976d4e67aea4caa8004e0df0359e6386758c799c`,
supplies these finite observations. The owner maps that approved summary
without actual/source/raw/audio/numeric re-review. Older R3 mappings and
preservation come ONLY from the [approved R3 owner peer report](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/collision-owner-r3-kind3-finite-v1-review.json),
SHA256 `8a3b3df046644949d1fa1074a0efa693e5010bd67c65bc4f8b95485ebc967c47`,
with embedded complete mapping/preservation and exact target. No old R3
proposal, actual/source/code, released fixture or provider is reopened.
Old R2 object/8relation/release pins are inherited reviewed facts here, not
fresh file-custody claims. Complete canonical R3 remains exact to that target.

The common139 ordered setter words have SHA256
`1a61d31521973c8eaa9167ca184704b787cda790d43db0c82a459d28caf0d0bc`.
The exact original2040-byte baseline script has SHA256
`48a15b4f1483c5e92d9c940ae9469aaeecd3309ecf672851e9f298dc0111a2bc`.
Original decimal tokens and binary64 parsing remain alongside binary32 words.
Initial host25 is1 and host58 is0. Each unchanged recorded instance uses
create/rate44100/all139setters/inflag0/zero input, then warm11264frames/block512
BEFORE queueing On4097/status90/key60/velocity100 and Off7168/status80/key60/
velocity0, then process8192 and4096 at512, then destroy. There is NO boundary
setter. Only the selected Off-key or one status low nibble changes. The old
process-local queue model is unchanged:the second segment's[0,4096) excludes
4097/7168, so neither queued event is replayed there. This is a source/test
coordinate premise, not a new Live event-base or internal admission proof.
No new event type, host update, timing segmentation, receiver/constructor
model, native patch, provider, tool, calibration or original-control replay.

All157 new outputs are finite and nonzero in BOTH channels; none has identical
channel words. The fresh captures share one hash, descriptive only. No old
baseline audio is replayed or compared. Finite hash equality supplies no
unmatched-key/channel release, ignored-Off, latching, voice, timing, inactivity,
productive-control, mechanism, physical accuracy or general no-effect law.
All fresh waveform priors/new expectations, portable expected/comparator/
grade remain NULL; native artifact hashes are evidence references, not portable
candidate waveform criteria. No f0, fitting, estimator, metric, window,
tolerance, modal budget or physical calibration is added. No public/ARM proof
or extension of004's older timing partitions follows.

THIS157 batch uses the approved DCL-054 no-setter input history, DIFFERENT
from R3's kind3 history. It does not retry or repair failed `i058-v01`:
that old record stays unnumbered guardFAIL/U discovery with native Ret1
meaning unknown, not an approved success/waveform criterion. R3 still has
84 approved observations (15partial+69continuation), not85 successes.
Its old kind3 baseline remains unnumbered INPUT-only without approved X,
PID/receipt/metric/oracle or assumed DCL-002 criterion. Old partial outerexit1,
staleRUNNING, failed phases, unbound postcapture JSON readback and historical
as-of69unlaunched qualification stay exact; later continuation never replays
that failed child or the first15. No old budget or timing criterion transfers.

All new capture/parent/data/checker/initial-materializer code was pre-call-bound
for THIS157 batch; the materializer is a historical initial stage, not a final
regenerator. Existing source/default/LinuxFP/time/provider/OSexec scopes remain
unproved beyond their recorded model. Old0664/close-and-hash/noexplicitfsync
limits remain old facts, not repaired by new0444 files/0700directory or FDfsync
requests. New JSON/JSONL/log/audio FDfsync is not directory/crash/power-loss
durability. SamePID and per-child endpoint identities are not continuous
loaded-provider/entryFP/ABI/build/OSexec proof. Post-child protocol checks
cannot retract earlier within-child calls; group/direct-child cleanup does
not exhaust parent-loss/escaped-process paths.129 import declarations
(96Linux,26trap,7data) stay distinct from counted code use. New raw export/
initializer declarations were compared across fresh children under the fixed
bundle/loader; no historical target whitelist was fabricated.188 selected
direct exports/46CalcA per child and0 logged initializers leave nested/all-native
calls unknown. Rate's signed integer remains opaque/public meaning unknown.

Only bounded REQ-004 wording is appended. All17 other whole requirements,
including ENTIRE REQ-002 R3, old004 prefix,146 prior IDs/62 old rows,
allR2/R3 objects and eightrelations, old Acceptance prefix, original NULLs/
generalU/criteria/tolerances/state/error/history/noisephysicalmetricunknowns,
and released2cases/2evaluations/8inventory entries remain exact, with full
reversal. The resulting303 navigation IDs are not passes or application-outcome
units. New application-predicate proofs remain false; no release, grade,
portable criterion, publicA1A2/ARM law, calibration or whole-product closure.

### Revision 5 finite DCL054 five remaining MIDI axes

The [complete catalog](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-collision-r5-dcl054-five-midi-axes-finite-v1/cases524.json) contains528 aliases /524 WHOLE histories,
with523 new navigation IDs DCL-304–826. The independent supplied axes are:
On key0–127 with Off key60 fixed; matching On+Off keys0–127; On velocity0–127;
matching On+Off channel nibbles0–15; and Off velocity0–127. Only the named
axis changes, with no crossproduct or added event/state/timing/host change.
Five baseline aliases (Onkey60/matchingkeys60/Onvelocity100/matchingchannels0/
Offvelocity0) share ONE DCL-054 `initial1-no-setter-released` INPUT reference,
without a new ID, replay, PID, receipt, output, metric, expectation or criterion.
The [523 finite case references](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-collision-r5-dcl054-five-midi-axes-finite-v1/new-cases523.json) join exact catalog rows,
not copied portable oracles. [All528 joins](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-collision-r5-dcl054-five-midi-axes-finite-v1/joins528.json) retain complete event histories,
original139 decimal tokens/parsedbinary64/binary32 words, packed16-byte events,
and exact approved-summary point/history pointers. Whole-history dedup never
collapses records just because parameter words or output hashes agree.

Only Auto's [sole actual/source approval](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/collision-dcl054-five-midi-axes-v1-review.json),
SHA256 `0dd108e1ea1bc56fbf06250243f5319dabb5e20c1072113c259b489d8d142d9f`,
supplies the new observations. This owner maps its approved summary ONLY;
no actual/source/raw/audio/numeric re-review occurs. Root's
[approved R4 owner report](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/collision-owner-r4-independent-midi-finite-v1-review.json),
SHA256 `90e42ccdfc61efb032e947633dbb9dcf25921d23f5425ec4e3fbedae9f2859fe`,
supplies all older R2–R4 object/relation/release preservation facts and exact
R4 target. No old R3 proposal/catalog/code, actual/source/raw, provider or
released manifest/fixture is reopened. Earlier preservation/release pins are
inherited reviewed metadata, not fresh custody of those older files.

The common139 ordered setter words retain binary32 hash
`1a61d31521973c8eaa9167ca184704b787cda790d43db0c82a459d28caf0d0bc`;
original decimal/binary64 identities remain separately recorded, not replaced
by rounded owner values. Initial host25=1 and host58=0. The unchanged recorded
instance uses create/rate44100/all139setters/inflag0/zero input; warm11264frames
at512 BEFORE queueing On4097/status90/key60/velocity100 and Off7168/status80/
key60/velocity0; then process8192 and4096 at512 and destroy, no boundarysetter.
Only the selected byte(s) change; matching keys/channels explicitly change BOTH
matching fields, unlike the earlier R4 independent Off-key/channel histories.
The admitted process-local queue model remains unchanged:secondsegment
[0,4096) excludes4097/7168, so neither event is replayed there. Those supplied
coordinates/default stopped0/0/120/TIME0/per-entryFP assumptions are not new
native event-origin, actual receiver/ABI, Live timebase or emission proof.
No new constructor, native patch, provider, tool, build, emulation, FP treatment,
reset, warmup order, segmentation or calibration is introduced.

All523 approved fresh captures are finite and nonzero in both channels;
522 have unequal channel words and ONE has equal channel words. The181 fresh
hashes and first-nonzero/phase summaries are descriptive only, without mechanism,
voice allocation, channel matching, velocity response, audibility, productive
control, ignored-Off, general no-effect or deterministic waveform claims.
In particular, supplied Onvelocity0 or Offvelocity0 does not prove a general
note-on/note-off equivalence or release law. The inherited baseline output is
not replayed or compared; no old criterion/modal budget transfers. Every new
case carries the common review-qualification pointer; waveform priors/new
expectations, portable expected/comparator/grade remain NULL and new application
proof remains false. No new f0, fit, estimator, metric/window/tolerance,
physical calibration, public A1/A2/ARM law or criterion is added.

The new batch remains the DCL-054 no-setter history, not R3's kind3 history.
Failed `i058-v01` remains unnumbered guardFAIL/U discovery with native Ret1
meaning unknown, not a success or waveform criterion. The old kind3 baseline
remains unnumbered INPUT-only with no approved X/PID/receipt/metric/oracle or
assumed DCL-002 criterion. R3 has84 approved observations, not85 successes;
old partial outerexit1/staleRUNNING/failure phases/unbound postcapture JSON
readback and its as-of69unlaunched qualification remain exact. Neither R4's
157 nor this523 batch retries or repairs that old failure or old criteria.

For THIS523 batch, all capture/parent/analysis/checker/initial-assembler source
was pre-call-bound. The historical materializer is not a final regenerator.
Eleven whole-source pairs and15 before/after endpoint identities per child
(7,845 pairs) match as reported; they are not continuous loaded-provider,
interpreter/build/nativeFP/ABI/OSexec or semantic receiver attestation. New
raw/log/audio/JSON FDfsync requests are separate from directory/crash/powerloss
durability and do not repair old0664/closehash/noexplicitfsync/default/source
limits. Resource320MiB+128MiBheadroom planning/remaining-output guards/soft
current-child overshoot are no reservation, hard aggregate quota or external-
writer/unmodeled-file guarantee. Post-child failures cannot retract earlier
within-child calls; selected group/directchild cleanup does not cover all
escaped/native/parent-loss paths, and normal runs do not validate fault paths.
129 declarations (96Linux/26trap/7data) differ from57or59 counted code names;
uncounted declarations/data do not prove provider/global-data absence.
188 selected direct exports/46CalcA per child and0 logged initializers leave
nested/all-native counts unknown. Rate's signed integer remains opaque.

Only bounded REQ-004 wording is appended. All17 other whole requirements,
including ENTIRE REQ-002 R3 and old004 R4 prefix,303 prior IDs/62 old rows,
all R2–R4 objects/eight relations, old Acceptance prefix/NULL history/generalU/
criteria/tolerances/state/error/noisephysicalmetricunknowns and released
2cases/2evaluations/8inventory remain byteexact, with full R4 reversal. The826
navigation IDs are not passes or application-outcome denominator units.
No new release/grade/site/portable criterion or whole-product closure follows;
required unsupported U remains OPEN.

### Revision 6 partial Mallet controller observations

**Analyst draft; finite extracted observations, portable acceptance U.**
The [R6 catalog](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-collision-r6-partial-mallet-cells-finite-v1/mapping.json)
assigns DCL-827–950 ONLY to 124 accepted native observations: Mallet Volume
host1 representatives0–123 with token `repr(n/127)`. These reference REQ-008's
Mallet context; all18 requirement bodies, including that entire proposed
formula/metric scope, remain unchanged. The annex does not independently
validate their formulas or endorse every existing parent-case assertion.
All256 supplied histories remain mapped:124 approved, ONE failed/unknown
125th history, and131 never launched/unknown. No ID, native-waveform
expectation, metric or grade is assigned to those latter132 histories.
This is not a completed256-member capture or a whole-device pass.

The sole actual/source authority is [Arrangement's partial review](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/collision-mallet-controller-cells-v1-review.json),
24,096,318bytes/SHA256 `9968349497c41a6f1ba9c7d20a1e5c150088abf4fc3949890497b75b5d12d814`.
Only its approved summary supplies observations and original input/result
references. Every new case points to the full input and common qualification;
all fresh priors/new native-waveform expectations/portable expected/comparator/
grade remain NULL, with new application proof false. No old capture, raw,
source, numeric result, provider, old owner proposal/catalog or fixture is
replayed by this owner proposal. Root's R5 sole owner review supplies inherited
mapping/preservation only, not new custody or actual-proof review.

The complete INPUT class is128 independent representatives on host1 Volume
and128 on host4 Stiffness, without a crossproduct. The original preset's
literal0.5 on each is absent from the n/127 grid; same-floor-cell membership
is not exact token/binary64/binary32/history identity. No baseline output,
PID, receipt, metric, expected waveform or criterion is inherited. All139
original decimal words/binary64/binary32 conversions remain fixed except the
one named host. No new NoiseAmount domain or arbitrary139-control sweep is
introduced. Neither this class nor its incomplete capture proves quantizer,
within-cell, exponential-output, pulse/physical/noise or productive-effect laws.

Each supplied history is the existing unmodified factory/rate44100/all139
setters/zeroInputflag0 route: warm11264 at512 BEFORE queueing On4096/status90/
key60/velocity100 and Off26146/status80/key60/velocity0, then process44100 at512
(last68) and destroy. Stopped0/0/120, TIME0 and the admitted existing FP/model
context remain qualifications, not actual Live/current receiver/native ABI/
OSexec/provider/default/source-version proof. This is the preset_c4 full44100
history, not the later DCL0544097/7168→8192+4096/no-setter history. No new
construction, provider/tool/build/patch/emulation, timing, reset, segmentation,
parameter/event crossproduct or calibration is introduced.

All124 accepted captures are finite and nonzero in both channels, with unequal
channel words and124 distinct fresh hashes. Their warmup outputs are also
nonzero and are retained: zero input/inputflag0 is NOT a silence or inactivity
premise. These copied finite facts do not establish deterministic waveforms,
noise distribution, audibility, general effect/no-effect or public/ARM laws.
The131 unattempted inputs are Volume125–127 and all128 Stiffness members.
They retain their frozen NULL predictions and acquire no fabricated PID,
receipt, metric, native output expectation or acceptance result.

Failed `MCI-001-124` is Volume124/127, literal0.9763779527559056. It exited0
with empty stderr and a complete442912-byte raw file, but the frozen protocol
rejected it: warm22blocks(ret0,flag0), then render8(ret0,flag0), ONE(ret1,flag1)
starting at render4096, and78(ret0,flag1). The signed-long return projection's
meaning, formal ABI and cause remain U. Retained finite/unequal raw-word
properties are an UNACCEPTED diagnostic, not an accepted protocol, metric,
case expectation, clipping/error/success law or permission to relax the guard.
The process exit is not protocol approval. First detected fault stopped later
launches; earlier within-child calls cannot be retracted. No retry,
continuation or changed opaque-return policy is selected here.

For THIS partial packet, all eight capture/parent/analysis/checker/finalizer/
initial-authoring Python sources and all256scripts were pre-call-bound.
The frozen finalizer later raised metadata KeyError `recorded_raw_bytes`,
after author-bookkeeping.json but before assessment/manifest, because the
checker returns `raw_bytes`. Original code and failure remain immutable.
The additive JSON-only post-capture sealer and separate seven-control metadata
qualification are explicitly NOT pre-call-bound; they package metadata only
and do not repair or approve the original protocol failure. The finalizer
tool returned a traceback, but no separately redirected standalone stderr
file exists; none is invented. The original recorder's outerexit1 and first-
fault stderr remain retained separately from that packaging error.

Accepted124 raw/log/JSON FDs request fsync. Failed raw FDfsync and the accepted
unsigned-guard/metric branch were SKIPPED after the protocol assertion;
failed raw has close/hash custody only, with logs/JSON retaining their own
request scope. No directory/crash/power-loss durability or retroactive old
fsync repair follows. Seven whole-source pairs plus2,250 actual per-child18
before/after pairs span125 attempts; endpoint matches are not continuous
loaded-provider, transitive-library, interpreter/nativeFP/ABI or OSexec proof.
129 declarations(96Linux/26trap/7data), seven exports and59 counted Linux
code names remain distinct; no provider/global-data absence is inferred.
31,124 selected exports/13,516CalcA/0logged initializers count only124 accepted
protocols; nested/all-native counts remain unknown. Rate's integer is opaque.
512MiB lifecycle+128MiBheadroom/remaining-output resource guards are unreserved
estimates, not hard quotas or concurrent-writer/escaped-child guarantees.
Post-child/within-child soft overshoot and selected-group cleanup limits remain.

The old kind3 failed `i058-v01` stays unnumbered guardFAIL/U discovery with
unknown Ret1 meaning and an unnumbered INPUT-only baseline:84 approved
observations, not85 successes, no assumed DCL-002 oracle. Oldouterexit1,
staleRUNNING, unbound postcapture JSON readback/default/source/0664/durability
limits and their history remain unchanged. This new failure does not replay,
repair, regrade or give a return law to that different old history.

Only this annex and revision metadata are added. All18 whole requirement
bodies,826 old IDs/62 old rows/all R2–R5 objects/eight pair relations/old
Acceptance prefix/criteria/U/tolerances/noise physical metric unknowns/state/
error/history and released2cases/2evaluations/8inventory remain byteexact,
with full R5 reversal. Release facts are inherited reviewed metadata only;
no release manifest or fixture is reopened. The950 navigation IDs are not
passes, new application-outcome denominator units or whole-product closure.
Required unsupported U remains OPEN; no new release/site/portable criterion
or grade is added.

### Revision 7 finite Stiffness controller representatives

The [whole Stiffness mapping](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-collision-r7-stiffness-cells-finite-v1/mapping.json)
adds DCL-951–1078 for all128 newly approved supplied Stiffness histories.
REQ-008 is context only; all18 whole requirement bodies, including its
existing controller formulas, remain byte-exact without new validation of
those formulas or general physical/quantizer/within-cell/output/noise laws.
Each host4 token is the selected `repr(n/127)`, n0–127, with all139 original
decimal/binary64/binary32 parameter words otherwise unchanged. Volumehost1
remains literal0.5; that original0.5 is not an inherited controller-cell
representative. No baseline/PID/receipt/output/metric/criterion is replayed
or transferred; all128 histories have their own new once-only captures.

The sole actual/source authority is the [approved Stiffness128 review](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/collision-unlaunched-stiffness-v1-review.json),
13128862bytes/SHA256 `c438ddd5dec075e868a00d35025ad6233a0d02838cedc351b9c73f7ec7ea2c7d`.
Only its approved summary supplies INPUT, receipts, output references and
observations. Existing44100Hz/139setters/zeroInput/inflag0/TIME0/C/LIBM-unset
model remains exact: warm11264 BEFORE queueOn4096/key60/velocity100 and
Off26146/key60/velocity0, then render44100/block512/last68. These are literal
existing supplied command coordinates/order, not a generalized native event
clock or public Live path; no added events/timing/FP/model/construction.

The old R6 full256 disposition catalog remains an immutable AS-OF view:
124 approved Volume cases DCL-827–950, failed Volume124 U, and131 then-
unattempted U, including all128 Stiffness and Volume125–127. This annex's
128 new Stiffness cases do not rewrite that historical view. The failed
Volume124 guard rejection and three unlaunched Volume125–127 stay U with
no newIDs/expectations/grades; no retry, continuation or opaque-return
policy is adopted. No complete256-success claim or repaired old proof
follows. No new oldVolume PID/output/metric is fabricated. Oldkind3ret1/
84-not85/input-only baseline/outerexit1/staleRUNNING/unbound postcapture
readback, failedraw FDfsync skipped/diagnostic not accepted metric,
additive postcapture JSON sealer NOTprebound/finalizer mismatch/no standalone
finalizer stderr and old source/default/provider/FP gaps remain unchanged.

All128 fresh captures are finite and both-channel nonzero, with unequal
channels/102raw hashes/59usedLinux names descriptive only; warmup portions
are retained, with no new zero-warmup premise. All13952CalcA satisfy frozen
ret0/flag01/CXX0 guards.32128selected direct exports/zero logged initializer
lines leave nested native/provider calls and actual startup semantics U.
Current129 import declarations/96Linux26trap7data and seven raw exports
match the first current capture; this is not a fabricated historical exact
address whitelist. Used-code counters differ from binding declarations.
Rate signed projection is opaque, not a success/return ABI/absence law.

2304 actual per-child18before/after custody pairs plus two whole-source
pairs are endpoints, not continuous loaded-provider/nativeFP/register-entry/
ABI/OSexec attestation. Successful raw/log/JSON FDs request fsync; outer
redirects have no explicit FDfsync. No directory/crash/powerloss or oldgap
repair follows.2GiB lifecycle+128MiBheadroom/fullremainingraw/max8MiBfuture
logsmetadata/final256MiB guards are unreserved/soft, not quotas, concurrent-
writer/escaped-child/within-child-overshoot guarantees. Original INPUT14
mutation-only controls remain historical; the external qualifier replaces
ONLY INPUT_controls with actual rejection checks. No frozen repair occurs.

All new priors/native-waveform expectations/portable expected/comparator/
grade remain NULL; application predicate proof is false. No portable
waveform, calibration, productive effect, public Live/ARM/Apple law, metric
budget, release, site credit or completion follows. Only this annex and
revision metadata change. All950 prior navigation IDs/62old rows/allR2–R6
objects/eight relations/criteriaU/state/error/history/releases2cases2eval8
inventory objects remain exact with full reversal, including entire
REQ002R3 and REQ004R4–R5 text. Preservation uses only currentR6 and its sole
owner REPORT's embedded metadata; absent old bytes are not reconstructed.
The resulting1078 navigation IDs are not passes or a product denominator;
required unsupported U remains OPEN.

## Open questions and handoff

[Q-025](../questions.md#q-025-device-host-protocol-and-device-audio-acceptance) owns host protocol
and metric acceptance. The constructor-silence subquestion is answered by 002/003; whole-device
coverage stays partial. Additional Collision gaps are enumerated in 006–018, especially zero
resolved modes at Membrane Ratio 0.75 and the unstable noise metric.

A release would require an independent review of behavioral formulas and fixtures, accepted
comparators with their narrowed scope, reviewed removal of analyst material and a self-contained
handoff. No release or implementation is authorized by this draft.

## Analyst evidence appendix

Analysis-only. Do not copy recovered structures, scripts, models or helper-code locators into a
handoff. Canonical research: [Collision DSP](../research/device-collision-dsp.md). Original packet
`analysis/ableton-live-12.4.3/r2/t12-collision-v1/`; original executable and slice identities,
substitutions, recovery integrity checks and retention limits are recorded there.

| Clauses | Exact evidence locator |
| --- | --- |
| 001 | `collision.json:protocol`; `run_collision.py:run,protocol`; per-render process/import registry |
| 002 | `col.py:stored_to_host,CTOR,PRESET`; N6 `out/conversions.tsv`; Defaults preset in external inputs |
| 003 | `collision.json:root_cause,levels.coupling` |
| 004 | `collision.json:timing`; `run_collision.py:grid_rule,timing` |
| 005 | `collision.json:pitch` (34 rows); `model.py:A`; arm64 modal processor `0x2809c` |
| 006, 007 | `collision.json:resonator` (37 settings, per-channel measured/graded rows); `previews.json:summary,presets`; `model.py:CollisionModel` |
| 008 | `collision.json:mallet`; `model.py:mallet_response`; arm64 mallet `0x38edc` and wrapper `0x13ba0` |
| 009 | `collision.json:velocity`; note source arm64 `0x2faa0` (static support, not complete controller behavior) |
| 010 | `collision.json:levels` |
| 011 | `collision.json:noteoff` |
| 012 | `collision.json:voices` |
| 013 | `collision.json:pitch_env`; `run_collision.py:pitch_env` (20 ms FFT estimator) |
| 014 | `collision.json:waveguides` |
| 015 | `noise.json:ensembles,envelope,filter,noise_volume`; `run_noise.py:ensemble,band_levels` |
| Metric | `libm_sensitivity.json`; `fma_scan.txt`; modal fitting exclusions in `run_collision.py:modal` |
| Integrity | Original `manifest.json`; additive `recovery-manifest.json`, `results/recovery-audit.json` |

## Revision history

| Revision | Date | Change |
| --- | --- | --- |
| 1 | 2026-10-19 | Recovered original 2026-10-18 bytes without rerendering; two concurrently edited paths use exact-hash recovered originals. 18 requirements; 50 case IDs: 31 retained fixtures with proposed audio/value comparisons, five retained measurement checks (DCL-046 partly U), 14 ungraded cases. Noise and unresolved modes remain U; no accepted metric, release or compatibility pass |
| 2 | 2026-10-21 | Adopted the approved twelve supplied-host index25 enable histories as DCL-051–062, with eight named pair relations kept separate. REQ-017 gains finite observations only; its old U and DCL-048 remain, the other 17 bodies/all 50 old rows/proposed metric/open questions stay exact. Scope excludes general dynamic behavior while naming this finite exception. No new portable waveform criterion, calibration, public A2/ARM law or release. |
| 3 | 2026-10-21 | Add84 approved native-host observations DCL-063–146 from15 partial plus69 continuation summaries, full20domain105alias86history catalog. Append only bounded REQ002 qualification; retain failed index58=1 guardFAIL/U and historical input-only baseline without IDs/success/criteria. Preserve17otherwhole clauses/old002prefix/62IDs50+12rows/R2objects/metrics/U/release2 exact, full reversal. No general effects/publicARM law, portable criterion or application proof. |
| 4 | 2026-10-21 | Add157 finite DCL054 independent MIDI-byte observations DCL-147–303/full160aliases158histories/oneINPUTref3baselinealiases/no replaynewPIDmetricscriteriontransfer. AppendONLYboundedREQ004+annex; preserve17otherwhole inclENTIREREQ002R3/old004prefix/146priorIDs62rows/allR2R3objects8relations/oldcriteriaU/noisephysicalmetricunknowns/releases2cases2eval8inventory/history exact/fullreverse. Oldkind3failedi058-v01guardFAIL/U/input-onlybaseline/84not85/outerexit1staleRUNNING/unboundJSONreadback unchanged; THIS157differenthistory/NULLpriorsportablecriteria/grades/newappFalse/no generalpublicARMlaw. |
| 5 | 2026-10-21 | Add523 finite DCL054 five-axis observations DCL-304–826/full528aliases524WHOLEhistories/oneINPUTref5baselinealiases/no replaynewPIDmetricscriteriontransfer. AppendONLYboundedREQ004+annex; preserve17otherwhole inclENTIREREQ002R3/old004R4prefix/303priorIDs62rows/R2–R4objects8relations/criteriaU/releases2cases2eval8inventory/history exact/fullreverse. Oldfailedkind3Ret1guardFAIL/U/unnumberedinputbaseline/84not85/outerexit1staleRUNNING/unboundreadback stayunchanged; new523FDfsyncrequests/11source7845pairs/522unequal1equal181hashes descriptiveonly/NULLportablecriteria/appFalse/no generalMIDIpublicARMlaw. |
| 6 | 2026-10-21 | Add124 partial Mallet Volume observations DCL-827–950 from the sole approved partial summary; full256dispositions retain failedVolume124 and131unattempted U without IDs/expectations/grades. Annex/revision ONLY; all18wholeREQ/826oldIDs62rows/R2–R5objects8relations/criteria/history/releases2cases2eval8inventory exact/fullreverse. Nonzero warmups/failedret1 rejection/skippedfailedrawfsync/additivepostcaptureNOTprebound packaging/finalizer mismatch/no standalone stderr/oldkind3failure remain qualified; NULLportablecriteria/appFalse/no quantizer/within-cell/publicARM/calibration law or continuation. |
| 7 | 2026-10-21 | Add128 finite Stiffness observations DCL-951–1078/full128 fresh histories. Preserve R6full256ASOF dispositions/failedVolume124U+threeunlaunchedVolumeU/no retry or guard relaxation. Annex/revision ONLY/all18wholeREQ950oldIDs62rows/R2–R6objects8relations/criteriaU/history/releases2cases2eval8inventory/fullreverse exact; native-waveform/portable criteriaGradeNULL/appFalse/no physical/quantizer/publicARM/calibration law. |

Released locally 2026-10-19 as [device-collision-v1](../../handoff/device-collision-v1/README.md):
two cases only (DCL-001 and DCL-031), partial REQ-001/002/003/014. The
[handoff plan](device-collision-handoff-plan.md) records the independent finite
metric decision. Every other modal/noise/device scenario remains unreleased.
