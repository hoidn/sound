---
id: RESEARCH-DEVICE-COLLISION-DSP
type: research
status: draft
updated: 2026-10-22
access: analysis
target: Ableton Live 12 Suite 12.4.3 Collision.bundle, x86_64 slice
---

# Collision audio by extracted execution (T1.2)

**Question.** Why did Collision produce silence with the constructor parameter table, and what
instrument behavior can the unfinished extracted-execution packet establish?

**Answer (X, partial).** The silence is explained: the constructor disables both resonators.
The shipped Defaults preset enables resonator 1, and a C4 note then peaks at 0.110951.
The retained packet establishes the bundle's event grid, measured voice limits, modal pitch and
decay behavior, mallet response, level controls, resonator routing and several noise settings.
It does not establish Live's actual host protocol, a stable noise acceptance metric, complete
modal amplitudes, controller/LFO behavior or parameter automation.

The draft contract is [SPEC-DEVICE-COLLISION](../specs/device-collision.md). Both pages are
analyst material, unreleased and unsuitable as direct clean implementation inputs.

## Evidence and recovery

The original packet is [t12-collision-v1](../../analysis/ableton-live-12.4.3/r2/t12-collision-v1/manifest.json),
created 2026-10-18. This recovery on 2026-10-19 did **not** regenerate captures or run original code.
The [read-only audit](../../analysis/ableton-live-12.4.3/r2/t12-collision-v1/recovery_audit.py)
and its [result](../../analysis/ableton-live-12.4.3/r2/t12-collision-v1/results/recovery-audit.json)
check:

- all 103 original manifest payload hashes and byte counts;
- the full executable, both slices, the N6 conversion table, the Corpus mode tables, the
  Defaults preset, all 33 shipped preset/preview pairs and the loader binary;
- all five harness files against `t12-device-dsp-v1/harness`;
- 41 WAV/script pairs against the result registries: 32 in `results/collision.json` and nine in
  `results/noise.json`; stereo IEEE binary32, stated frame counts and rates, finite samples,
  all 139 parameters sent once in index order, and warm-up/process lengths matching the registry.

These checks establish integrity of the original bytes **through the recovery mapping below**,
not blanket agreement at current paths or compatibility. The original manifest is unchanged. The additive
[recovery inventory](../../analysis/ableton-live-12.4.3/r2/t12-collision-v1/recovery-manifest.json)
binds the audit script and result; it does not replace the original manifest.

### Concurrent-edit incident and recovered originals

The first audit passed all 103 payloads at their original paths. A repeated audit then found
two mismatches: `run_collision.py` gained logging and an `extras` probe, and
`results/collision.json` gained an `extras` section. Neither was edited or executed by this
recovery worker. No writer was identified. The changed bytes are preserved as
`recovery/incident-run_collision.py` and `recovery/incident-collision.json`; their new execution
claims have unknown provenance and are excluded from this draft.

Removing **only** the added script fragments and JSON section produced exact matches to the
original manifest's hashes and byte counts. Those recovered bytes were written to distinct
paths; current concurrent work was not overwritten:

| Original logical locator used below | Verified original bytes | SHA-256 |
| --- | --- | --- |
| `run_collision.py` | [recovery/originals/run_collision.py](../../analysis/ableton-live-12.4.3/r2/t12-collision-v1/recovery/originals/run_collision.py) | `f48e866f7307bf3b71336d70b48cd1e0d822112660ef8276d21300084f9cd8e1` |
| `results/collision.json` | [recovery/originals/collision.json](../../analysis/ableton-live-12.4.3/r2/t12-collision-v1/recovery/originals/collision.json) | `16019047fcc55c4d88e2c88a2ab3ef3f3def67215303bad0e1aee1e905db52db` |

Every logical reference to these two files in this page and the draft spec means the recovered
original path above. The recovery audit verifies that mapping and reports the two current-path
mismatches separately. Initial audit bytes are preserved in `recovery/initial-recovery-audit.json`.
The recovery inventory binds both incident copies, both recovered originals, initial audit and
inventory, and the revised audit/result. It records the restoration method. This is a recovered
original evidence view, not approval of the concurrent additions or an unmodified current tree.

### Target and substitutions

Observed (`manifest.json`, `external_inputs`):

| Artifact | Identity |
| --- | --- |
| Collision executable | SHA-256 `797e903cf3c147c6ee3d57054aaaa07988bd68999b153e82703bcf6aa550fcbd` |
| x86_64 slice | Offset 16,384; 367,488 bytes; SHA-256 `69f7edfdc7954fe5019045cd77afd9807a17ed1d142aa35d02a81c88b3623b21` |
| arm64 slice | Offset 393,216; 332,496 bytes; SHA-256 `2bc497cd849eb4412f04b40c84f18486305417f64b30519cab2278d9a1f105f7` |
| Retained-loader identity | `/var/tmp/sound-analysis/t12-collision/xdev`; SHA-256 `8d004008c588dc3edda9e98f6f7fe2271ef11a157b0585ad620b15f01914178b` |

The executable remains external at the path in the manifest. The harness is byte-identical to
the [T1.2 loader](device-dsp-extracted.md#harness). It substitutes glibc 2.39 libm, a Park–Miller
`rand`, fixed `time`, C locale and the libc++ stream shim. The manifest records gcc 13.3,
Python 3.13.9, NumPy 2.3.1, SciPy 1.16.0 and GStreamer 1.24.2. Per-render imported-call counts
are in the reference registries. No arm64 code was executed.

### What is retained

- `col.py`: 139 host values, constructor and preset parameter sets, stored-value conversion;
- `run_collision.py`: timing, pitch, modal fits, mallet, velocity, levels, note-off, voices,
  pitch envelope and waveguide probes; `results/collision.json` holds their measurements;
- `model.py` and `fit.py`: analyst-side static model and modal estimator, **not** independent
  application code; the model imports `corpus-dsp-v1/tables.py`;
- `run_noise.py` and `results/noise.json`: eight-seed ensembles, noise envelope/filter probes;
- `previews.py` and `results/previews.json`: shipped-preview comparisons of position mappings;
- `libm_sensitivity.py`, `results/libm_sensitivity.json`, `fma_scan.py` and `results/fma_scan.txt`;
- `raw/*.script` and `raw/*.wav`: exact inputs and stereo reference renders.

Sweeps, seed members 1–7, perturbed renders, decoded previews and comparison renders are
outside the retained packet under `/var/tmp/sound-analysis/t12-collision/`. Results survive in
JSON, but these scratch files are not covered by the original manifest. Their absence from the
packet limits independent remeasurement of those comparisons.

## Protocol and constructor silence

`run_collision.py:run`, `col.py:script` and each retained script specify:

1. fresh instance, then sample rate 44,100 or 48,000 Hz;
2. all 139 host values in index order;
3. warm-up with no events: 11,264 frames at 44.1 kHz or 12,288 at 48 kHz, in 512-frame blocks;
4. notes at frames counted from the first frame **after** warm-up;
5. silent input, input flag 0, transport not playing, position 0, 120 BPM;
6. processing in 512-frame blocks, except named partition variants; `time=0` except seed variants.

The loader queues events after warm-up; its `process` command starts its event-frame counter at
zero each time. The device's control-grid phase persists. Both warm-ups are integral multiples
of its period, so render frame 0 is also a grid point. WAVs omit warm-up output.

**X** (`root_cause`). Constructor host values give peak 4.00008 × 10⁻²². Both resonators are off.
The Defaults preset differs at exactly one binary32 host value, `Resonator1/OnOff`; enabling it
gives peak 0.110951, first frame above 10⁻¹² at 4,136 for an event at 4,096. The other stored
preset difference, PerNotePitchBendRange, is not sent through this table. This closes the
specific silence question in [Q-025](../questions.md#q-025-device-host-protocol-and-device-audio-acceptance).
It does not explain the earlier no-host-values, unwarmed engine-patch render's large output;
that different setup was not repeated here.

**X** (`protocol`). Re-runs, blocks of 64, 256 and 2,048, flush-to-zero/denormals-are-zero and the
tested reset sequence reproduce the preset render bit-for-bit. Blocks of 333 move the note by
44 frames; compensating that shift leaves at most 9.31 × 10⁻¹⁰ difference, not bit identity.
Omitting warm-up changes this preset render by only 7.88 × 10⁻²⁷, but Volume 0.25 applied at
creation starts at gain 1 and has settled by frame 44 (`levels.volume_start`). Warm-up remains
part of the fixture protocol. Changing the rate after sending parameters changes a Q render
by 9.76 × 10⁻⁵ relative RMS; rate-change identity is not established.

## Parameter mapping and positions

**S** ([N6](device-tables-native.md#collision-collision-139-entries-0138-no-second-outputs)).
There are 139 values, indices 0–138. Note-off decay is sent as 1 − stored value. Legacy integer
fields, target lookup tables and mode-8 target amounts follow N6. `col.stored_to_host` implements
that derivation; its use in a render does not independently prove Live's value path.

**S** (arm64 wrapper `0x13ba0`; helper corpus
`/var/tmp/sound-analysis/helpers/Collision/corpus/decomp/chunks/`, function code SHA-256
`5d79e0ac8fd11e61f370155aee13f3b95a8da4f87f09e4b5f1f4ed084b8fe2ff`). Normalized values use
controller `128v` below/equal 0.5, `126v + 1` above. Ranged values use
`127(v − lo)/(hi − lo)`. The packet's X fits distinguish floor quantization for exponential
parameters, floor with the special midpoint for material/inharmonicity/brightness, and
`floor(c + 0.4)` with the special midpoint for positions and mallet-noise mix. See
`model.U`, `K1`, `FL`, `TR` and `collision.json` `mallet`/`resonator`. These are analyst-side
explanations; retained renders define the limited behavioral expectations.

**Inferred, strengthened, not closed.** Position values are passed unchanged in the fixtures.
The shipped-preview comparison tests unchanged 0..1 against an additional `2v − 1` mapping:

- 33 previews; 29 separate the listening hypotheses by at least 0.5 dB;
- unchanged values fit listening-channel differences better in all 29; median error
  0.0629 dB versus 3.7386 dB, but worst unchanged error is 6.7084 dB;
- hit-position spectral patterns favor unchanged values in 19 presets, bipolar values in
  seven; the rest do not differ by more than the script's 0.1 dB threshold;
- 174 of 210 selected peaks lie within five cents, with median absolute difference zero.

The comparisons use lossy shipped previews with unknown generation protocol and optimize over
three velocities. They support the unchanged listening hypothesis but are not a capture of
Live's parameter calls. Hit mapping remains less discriminating. These observations do not
resolve Corpus's separate position question or N6's two StartTranspose range mismatches and
resonator-2 type-6 mismatch.

## Event timing, pitch and voices

**X** (`timing`, 380 events). Let `P = floor(fs/1000)`, `g = P floor(f/P)`, and
`b = B floor(f/B)`, where `f` is an event frame and `B` the uniform host block size. The first
changed output frame is `g` when `g ≥ b`, otherwise `g + P`. This is the changed frame itself;
Analog and Tension have a further one-frame offset. All 336 note-ons (44.1 kHz at B = 512, 64,
333; 48 kHz at B = 512) and 44 note-offs (44.1 kHz, host note-off decay 0.5) match. An event
can act before its timestamp. Arbitrary nonuniform partitions and Live's grid phase are unknown.

**X** (`pitch`, 34 cases). The nominal pitch is `261.62 A(p)` Hz, where
`p = KeyToTranspose(key − 60)/12 + Transpose/12 + FineTranspose/1200`, and `A` is the
engine's approximate power of two. With `n=floor(x)` and `t=(x−n) ln 2`,
`A(x)=2ⁿ[1+t+t²(0.5+0.200064t)]`. Measured pole frequencies differ through coefficient
rounding: C4 261.62391 Hz at 44.1 kHz, 261.61277 at 48 kHz; A4 440.33104 and 440.33945 Hz.
All 34 readings are within 0.67 of the frequency bound defined in the draft's metric, including
notes 24–108, transpose ±48, fine tune ±50 and keyboard amounts −1, 0, 0.5, 2. These are
modal String probes, not a uniform tuning claim for Pipe and Tube.

**X** (`voices`). Polyphony indices 0–8 leave 1, 2, 4, 6, 8, 10, 12, 14 or 16 notes sounding
after 24 sequential held notes. The surviving notes are the most recent ones. In the one-voice
test, key 67 replaces key 60 at frame 11,000 (event 11,025); subtracting the second-note-only
render leaves at most 6.24 × 10⁻⁶ over the next 4,096 frames, versus 0.0752 just before.
This supports oldest-note stealing for this sequence, not all retrigger/released-voice policies.

## Resonators, mallet and levels

### Modal results

**S, X** (`resonator`, 37 settings; `model.CollisionModel`). Beam, Marimba, String, Membrane and
Plate share the [Corpus modal family](corpus-dsp-static.md). Quality caps are 4, 16, 30 and
70 modes before the 5fs/12 frequency cutoff. The model describes their ratios, inharmonicity,
decay, material, brightness and position weighting. The 37 settings vary type, rate, quality,
decay, material, inharmonicity, brightness, ratio, hit/listening points, pitch, stiffness and
the selected resonator. They are not a full parameter cross product.

Across resolved modes with model weight at least 0.01, largest frequency residual is 3.385
frequency bounds, largest per-frame log-radius residual 4.897 × 2⁻²⁵, and largest normalized
complex-amplitude residual 0.02568. The fitted common gain is estimated separately per channel;
these figures do **not** prove the absolute gain model. Closely spaced modes, modes below the
weight threshold, and fits more than 10⁻⁴ away from the predicted frequency are excluded.
`ratio_3_0.75` resolves **zero** modes in both channels. It is retained but ungraded; no broad
"model matches all modes" conclusion follows from this packet.

**S** (arm64 modal processor `0x2809c`, code SHA-256
`1905b6fb202f23d819c33d242cce51083e5185b9e6aaed5cab14edfca226cf59`). The static processor
supports the approximate power-of-two pitch law, ±pitch clamp, cubic inharmonicity,
frequency cutoff and note-off-dependent decay. Full static-to-render equivalence is not proven.

### Mallet and velocity

**S, X** (`mallet`; arm64 mallet processor `0x38edc`, code SHA-256
`844d4c2aaabc2cdccc5ccb372689b7da1ac0c009e2f13a688839ad42a456807b`). The deterministic mallet
is an impulse shaped by a second-order low-pass. Volume follows 0.001 to 1 exponentially;
stiffness follows 2 to 5,000 Hz exponentially, clamped to 10–20,000 Hz. Exponential controls
use floor(controller). The model's deterministic response fits measured modal amplitude ratios,
with the exclusions above. The normalized amplitude is not itself an output waveform.

The mallet pulse is multiplied by a blend of a constant and filtered random noise. The noise
share is `(atan(a)/π + 0.5)³`, where `a` is the quantized −4..4 amount. Shares for host NoiseAmount
0, 0.25, 0.5, 0.75, 1 are 0.0004742, 0.0032809, 0.125, 0.61718, 0.78383. Thus host value 0
does **not** remove randomness. The packet's "Q" parameter set means PRESET with that value 0,
not a deterministic exciter. Its two-clock difference is 2.473 × 10⁻⁴ relative RMS.

**X** (`velocity`). With zero modulation amounts, velocities 1, 64, 127 reproduce velocity 100
bit-for-bit. Mallet VelToVolume follows the fitted gain law
`gain_db ≈ 20 log10(2) × 0.96856686 × amount × (velocity−64)/63`, maximum residual 0.00702 dB
on the tested amounts −2.5, 1, 2.5, 5. KeyToVolume follows the same fitted factor with
`(key−60)/12` replacing velocity source. VelToStiffness changes corner frequency; its measured
octave shifts differ from that factor, so it is defined only by the retained high-velocity
fixture and measurements, not by reusing the volume formula.

### Levels and routing

**X** (`levels`). Output Volume 0 is silent; relative to the preset, values 0.25, 0.5, 1 give
−17.92572, −6.02077, +6.02043 dB. Resonator Volume 0.25, 0.5, 1 give −11.90495, 0, +12.04120 dB
relative to 0.5. Sampled gain residuals are below 4.7 × 10⁻⁸ except muted paths with only tiny
residual noise. Pan holds the near-side channel at unity; at −0.5 the right is −6.02060 dB,
at +0.5 the left is −6.08926 dB. The slight asymmetry is retained; an equal-power law would
not describe these measurements.

**X** (`root_cause.topology`, `levels.coupling`). Order 1 routes exciters to both resonators;
either can sound alone. Order 0 requires resonator 1 to excite resonator 2: resonator 2 alone
is effectively silent. With resonator 1 muted, its pan and pickup swap have no effect on the
serial resonator-2 output. The serial output equals the sum of the two separately muted
parts within 1.87 × 10⁻⁸ in the measured case. Parallel output differs from the sum of separate
fresh-instance renders by 6.97 × 10⁻⁵; the packet does not establish exact additive identity
across fresh instances, which draw different random streams.

## Note-off, pitch envelope and waveguides

**X** (`noteoff`). Default stored DecayOnNoteOff 0 sends host 1: note-off does not alter the
render at all. In the String, Quality 0, Decay 0.75 probe, fitted held T60 is about 5.738 s;
host values 0, 0.1, 0.25, 0.5, 0.75, 0.9, 1 give post-off T60 0.04267, 0.04748, 0.13370,
0.75388, 2.42403, 4.15801, 5.73441 s. These are fitted pole decay times, not envelope cutoff
times. General laws for very short tails remain ungraded.

**X, partial** (`pitch_env`). StartTranspose 1, StartTime 0.5 gives approximately +6.54,
+4.55, +1.41 and +0.0024 semitones at 10, 20, 50 and 100 ms (20 ms FFT windows beginning
at those times). Negative and half amounts and times 0.25/0.75 were also measured. No exact
trajectory law is established. The retained `penv_1_0.5` fixture supports that sampled path only.

**X** (`waveguides`). Pipe/Tube C4 fundamentals at 44.1 kHz are 251.09609/241.36376 Hz;
at 48 kHz 251.27072/241.68681 Hz. Channels are identical in these probes. Radius and opening
change pitch: Pipe radius 1 gives 258.33884 Hz, opening 0.3 gives 234.44411 Hz; Tube radius 0
gives a short-lived spectral peak at 173.47582 Hz. These are selected results, not a full
waveguide pitch/decay law. Only the default 44.1 kHz Pipe and Tube renders are retained.

## Noise and comparison limits

**X** (`noise.json`). Nine settings were rendered with eight fixed clock seeds; member 0 is
retained. Noise exciter on/off, filter types LP/HP/BP/LP+HP, an ADSR setting, sustain 1 and
mallet NoiseColor/Amount changes all produce distinct retained outputs. Selected envelope and
filter sweeps are summarized in the JSON. They measure resonator output, not isolated filter
transfer functions: the denominator is an open-low-pass noise-driven Pipe render and the
harmonic sampling uses nominal 65.4 Hz spacing. Exact filter orders/corners and ADSR laws are
not established by those summaries.

The split-half spectrum maximum is 0.0354 dB for the preset, but 4.758–7.899 dB for the noise
exciter settings and 6.26 dB for the two high-mallet-noise cases. Envelope split-half median
reaches 4.655 dB and the 90th percentile 8.185 dB. Eight seeds are therefore insufficient to
justify a uniform tight noise comparator. The spectrum routine averages frame levels in dB
within each member, then power-averages those member levels; it is not the power mean of all
frame spectra. Empty FFT bands at low frequencies reach its −300 dB floor and are uninformative.
The nine noise fixtures remain ungraded pending a suitable estimator and stability study.

**X** (`libm_sensitivity.json`). Eight settings were rerendered with inexact libm results moved
one ulp up/down. Over the first 256 frames, relative RMS changes reach 0.001087; over long
modal renders they reach 0.09072. Mode shifts reach 0.671 of the frequency bound. Pipe's whole
window reaches 0.000611. Hence long modal waveform identity is unsuitable as a general metric.

**S** (`fma_scan.txt`). arm64 has 324 fused instructions in 78 functions, including 67 in the
modal processor and 27 in the mallet processor; x86_64 has no VEX FMA instructions or fma
imports. **Inferred:** arm64 rounding may have comparable sensitivity, but no arm64 comparison
establishes a bound. The draft's metric is provisional, restricted to measured fixtures and
resolved modes, and still needs acceptance under ADR 0004.

## Reproduction and remaining gaps

The original manifest records `sh run.sh` as regeneration command. **Do not run it unchanged
under the current 256-CalcA-calls-per-process limit.** `run_collision.py:pitch` includes
131,072-frame low-pitch probes plus warm-up: 278 calls at block size 512. The 41 retained
fixture scripts themselves use at most 109 calls. A bounded new probe must count every
process call, including warm-up, and retain a new result revision. Original captures must
not be overwritten merely to relabel this historical command.

Read-only audit reproduction, from the packet directory:

```sh
python3 -I recovery_audit.py > /var/tmp/collision-recovery-audit.json
```

Open: Live-side call ordering/grid phase and event frame base; stopping on activity flag;
position rescale and N6 range mismatches; absolute modal gain, unresolved/closely spaced modes
and Membrane ratio 0.75; noise statistical metric; LFO/controller/MPE/retrigger behavior;
automation and smoothing; rate changes, persistence, undo and malformed input; arm64 numerical
differences. These remain partial T1 coverage. No application or original-versus-candidate
comparison exists.


## 2026-10-20 Collision family route map — pending review

The [bounded route map](../../analysis/ableton-live-12.4.3/full-spec-v1/family-collision-routes-v1/structure.md)
indexes the current 18 requirement contexts, all 50 draft cases and all 139 host indices.
Its 84 local predicate/context rows (38 X, 10 S, 36 without a complete established route
or oracle) are an author inventory, not a frozen whole-family denominator or new grades.
The 41 retained original renders remain distinct from the two locally released finite
comparisons in [device-collision-v1](../../handoff/device-collision-v1/README.md).
Only constructor effective silence and the exact Pipe output have that release's
approved metrics; modal/noise/Tube and the remaining owner contexts are not promoted.

The map preserves all 103 original payloads through the existing two-path recovery
mapping. Current `run_collision.py` and `results/collision.json` extras remain excluded;
no capture, model, estimator, comparator, old audit or harness was replayed. The
resonators-off constructor and productive Defaults-enabled path stay separate. Generic
integration I-07/I-08 does not bind an actual Collision instance, stored parameter
emission, event grid, host output or render delivery. A1/A2, unresolved modal components,
noise stability, target ARM numerics, automation and lifecycle limits remain open.
The older unreleased language above records draft provenance; the finite release and
its review govern only their stated two cases. Parent seal and independent map review
are pending; this addition makes no normative or release change.


## Collision family-map approval — 2026-10-20

The [independent review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/family-collision-routes-v1-review.json)
approves the bounded map, manifest SHA256
`f1d5ea694e8bf9fe751a7b9384bcc5841580e0645a48cd994564024e6fe0f09c`;
review SHA256 `e2fd6b508531e7270c552db8d7bfee0bd74fb7dbdf55b2e8d7673d798f83b842`.
The pending-review section is author history. All 84 local rows, 50 draft rows,
139 indices, 41 historical scripts/renders and two released comparisons remain
separate units; no completed profile, grade or whole-product denominator.
The bounded review checks two recovered originals, selected providers, all41
script metadata/5,699 binary32 values and two vectors/278 components. It does
not replay the full103/recovery/release/audio byte loops; earlier broad audit
results are carried under their limits. Unknown current extras supply no evidence.
Actual instance/event/output, A1 positions/Type6, modal/noise/ARM/lifecycle and
oracle gaps remain U. DCL014 and nine noise fixtures stay ungraded. No original,
model, comparator or audio ran; no normative clause/case/release changes.


## Collision whole12 enable-history actual approval — 2026-10-21

The [whole twelve-history packet](../../analysis/ableton-live-12.4.3/full-spec-v1/batch-collision-resonator-enable-histories-v1/manifest.json) (59 payloads /2,704,695 bytes; manifest SHA-256 `06896e58bf5fd69a499b03ab4af82cefb5ac940df54f636df76017c879907f0b`) [passed independent actual review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/collision-resonator-enable-histories-v1-review.json) with no blockers (56,450 bytes; SHA-256 `e899873b4bd4335aedc83013739fd8875d9d465db32d6daa929e70601131d086`). Root adopts its bounded observations by citation under design12, without reviewing the same raw observations again. The sole nonblocking qualification is POSIX0664 on all60 files: their fixed byte identities are verified, not OS write protection.

The complete finite class is initial Resonator1/OnOff index25 in{0,1} ×sent value in{none,0,1} ×held/queued-note-off context: eight post-segment setters and four matched no-setter controls. All139 ordered initial values are fixed except25, and Resonator2 index58 stays0. A fresh recorded instance receives rate44,100, all values,11,264 warm-up frames, then note60/velocity100 at4097 (off7168 only in the note-off context),8,192 frames, optional setter25,4,096 more frames and destroy, with512-frame blocks throughout. No reset or recreation occurs at the boundary.

The inert driver confirms each process command resets local event coordinate done to0 while the event queue persists. Warm-up precedes queueing. Both4097 and7168 are strictly outside the second[0,4096) segment, so no selected event replays; no new event-clear or cumulative clock model was introduced. “Released” names the queued note-off history, not a measured envelope phase. This synthetic protocol does not establish Live's event origin/grid/A2.

All12 once-only children exited0 with empty stderr, no timeout/TRAP/FAULT/C++ failure or retry at05:04:18.529–18.920 UTC. Each has46 CalcA calls:22 warm-up,16 first segment,8 second. The whole batch has552 CalcA/2,264 direct exports; nested calls remain unknown. Each capture is188,416 bytes including warm-up, totaling2,260,992 raw bytes/565,248 binary32 sample words. All34 recorded before/after identities agree; post-child checks have no separate per-child custody receipt or continuous monitoring. All18 frozen input payloads and the exact11,658-byte pre-call manifest serialization remain retained. The reviewer freshly checked owned payloads/baseline/inert drivers/current owner; image/runtime/provider identity is recorded collector custody, not freshly reopened by review.

All eight matched warm-up/first-segment prefixes are byte-identical. Four repeated-state setter suffixes equal their no-setter controls; four changed-state suffixes differ. OFF→ON maximum differences are6.614593209903703e-20 (held) and6.467745745179208e-20 (queued off), so these supply no audible effect, productive note, exact silence threshold or general activation claim. ON→OFF maximum difference is0.0558696985244751 in both contexts, without a smoothing/envelope/timeconstant law. Enabled versus disabled controls have finite peak contrast0.11095097661018372 versus4.000078885370357e-22; no physical threshold is derived. All pre-call predictions remain NULL. Equal/tiny captures are retained, not omitted.

The reviewer read complete227/123/104-line new sources before data-only checks, all12 scripts/argv/statuses/raw words, all1,668 initial/eight sent binary32 projections, every import log and all eight relations. Nine owned retained controls/eight independent negatives passed; stored author ten-input/four-analyzer results remain separately attributed. All129 declarations agree (96 Linux/seven data/26 trap), with58/59 actually counted Linux names per child, union59. The collector permits declared Linux bindings rather than an exact name whitelist; counts are not complete nested/global/provider tracing. Checks generally occur at child end and cannot intercept earlier within-child commands. Raw/JSON close/hash has no explicit fsync; normal children do not validate timeout/failure/escaped-descendant/crash durability.

The approved finite observations may enter owner R2 directly; extra wording/mapping/preservation requires its bounded review. General active automation, A1/A2/public receiver/output, reset/rate/persistence/lifecycle, physical calibration, ARM/Apple and portable exact-waveform behavior remain U. The two currently released criteria remain unchanged. Main indirect inventory stays25,071 baseline +24 conditional =25,095 of268,015; frozen family inventory stays691 X /1,076 S /3,857 none with Analog199 X predecessor scope. Whole-product coverage remains OPEN.


## Collision owner r2 finite adoption — 2026-10-21

The [R2 owner packet](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-collision-r2-finite-v1/manifest.json) (seven payloads /172,694 bytes; manifest SHA-256 `6465a85ab18d580816c8d294a00154ca260276f962b6a37e3a675c9abf981489`) adopts DCL-051–062: twelve new exact histories, four controls/eight setters, with eight pair relations kept separate. [Added-wording/preservation review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/collision-owner-r2-added-wording-review.json) (3,439 bytes; SHA-256 `bc0e7f51e99844c723e9e05ce4299a04cb2f6d5a67a99430fdb1798b3ca08986`) inherits the approved actual review without repeating it.

Root read all added scope/REQ017/catalog/provenance/revision text and the complete142-line checker before its data-only invocation; all11 negative controls passed. All18 old requirement bodies remain exact prefixes; the other17 whole bodies, all50 old rows/IDs, the proposed metric and open-question sections remain exact. An independent minimal-delta reversal reconstructs the full31,187-byte R1 predecessor. The owner now has18 requirements/62 IDs; DCL-048's general U stays unchanged, and pair relations are not additional cases.

Each new case retains exact139 words, event coordinates, all three process segments, the boundary and immutable observation pointers. Strict second-segment event exclusion and tiny OFF→ON differences remain explicit. Historical predictions and new portable candidate comparators/grades stay NULL. Raw hashes are provenance, not candidate waveform criteria; no tolerance, physical calibration, deterministic/no-effect/smoothing, public A1/A2 or ARM law is added. Actual0664 byte-sealing, child-end checks/import/runtime/no-fsync/failure-path limits are inherited. The two released criteria remain separate from draft proposed metrics, with no new fixture/release or release re-audit. Old R1 source pins are historical as-of evidence, not gates against R2. Unsupported required behavior keeps coverage OPEN.

## Standing-class eligibility after finite adoption — 2026-10-21

The [adopted twelve-history class](#collision-whole12-enable-history-actual-approval--2026-10-21)
covers its complete selected initial-OnOff × sent-value × held/queued-off
contexts. The [retained input inventory](../../analysis/ableton-live-12.4.3/full-spec-v1/family-collision-routes-v1/input-sets.json)
keeps all 41 scripts, including the five named modal types, Pipe/Tube and both
serial/parallel coupling contexts. Those existing members are not missing
merely because the family still has 38 mapped X routes, and replaying them does
not establish general type, timing or parameter laws.

The same inventory explicitly leaves DCL-014 and DCL-033–041 ungraded. DCL-014
has no resolved modal comparison; the nine retained noise fixtures have no
accepted noise comparator under REQ-015. The `summary_only_sets` are historical
navigation, not assured current scripts or legal new input recipes. The
`future_batch` warning retains the distinction between the bounded 41 scripts
and old regeneration paths that can exceed the current 256-CalcA limit.

No further complete missing class with an exact admitted input/history was
identified in this bounded assessment. A NULL waveform prior or portable
comparator alone does not prohibit a finite observation capture; existing
ungraded fixtures do not become missing inputs merely because their comparator
is unresolved. No new metric or calibration is selected here. The 139 control
domains and their interactions have no proven finite equivalence partition;
this is not proof that every possible class is exhausted. A1/A2,
actual public receivers/output, lifecycle and physical/ARM uncertainty remain
open. No raw audio, original source behavior, providers, runtime or comparator
was replayed, and no new batch, tolerance or grade was selected.


## Fixed preset history native kind3 eligibility — 2026-10-21

**Metadata-only; no capture selected.** The [compact complete eligibility report](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/collision-kind3-host-domain-eligibility.json),120,032bytes/SHA-256`706b599ba68670b8faa1139f64f192c270d2a14b18cdfdd0f653f0389d05c5d9`, enumerates all20 nonvirtual native-kind3 domains/105(index,value) aliases at ONE already retained `preset_c4` history. All20 baseline words are exact legal integers within the native declared ranges. Full139-word vector dedup gives86 unique vectors:20 baseline aliases collapse to one retained baseline, leaving85 single-word vectors missing in the bounded exact-history cut. No continuous139-control partition, crossproduct or arbitrary sampling is implied. These are input inventory units, not required predicates, application coverage, candidate grades or ordinary Live admission.

The [baseline input script](../../analysis/ableton-live-12.4.3/r2/t12-collision-v1/raw/preset_c4.script) is2,045bytes/SHA-256`3b17f74d5f2b6500635628d48db81decdf5bf28ec1f5b18ba63bc3ab2a0e383b`; its139 initial words in index order0–138 hash to`1a61d31521973c8eaa9167ca184704b787cda790d43db0c82a459d28caf0d0bc`. It creates the existing instance, sets rate44100/all139values/zeroinputflag0, renders11264 warm-up frames BEFORE queueing note60/on4096/status90/velocity100 and off26146/status80/velocity0, then renders44100frames in512blocks/last68 and destroys. Repeated zero-input/flag commands and queue-after-warm ordering are retained exactly. Each candidate changes one host word only. The existing unmodified Collision xdev path has recorded SHA-256`8d004008c588dc3edda9e98f6f7fe2271ef11a157b0585ad620b15f01914178b`; bundle/slice/method/environment identities are inherited metadata, not freshly acquired. This model uses109CalcA/251selected exports per prospective child;85 would retain37,647,520stereo bytes including warmup/9,265CalcA/21,335selectedexports, with nested/constructor/library work unbounded by that count. No run is selected here.

All41 retained script identities match the original Collision manifest and the reviewed family input inventory. Exact parameter words/order and complete call/event/process histories yield only `preset_c4` itself;40 scripts have different histories. The two released evaluation input declarations also have different render durations. The [approved whole12 review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/collision-resonator-enable-histories-v1-review.json),56,450bytes/SHA-256`e899873b4bd4335aedc83013739fd8875d9d465db32d6daa929e70601131d086`, has initial0/1 index25 vectors overlapping parameter-wise, but its queue4097/off7168 and8192+4096 post-warm segments differ from this complete history. None of its twelve histories is an additional exact intersection; parameter-vector-only matching would incorrectly replay or inherit them. Only approved input/protocol projections were consulted, without actualpacket/raw/audio/numeric-results/estimator/model/provider/native/runtime replay. A prior routing dump exposed existing release-metric fields; they were not evaluated or used as new numeric evidence. Old source-executed-version/public binding remains unknown, and this bounded41+2+12 comparison is not universal absence.

The declaration authority is H4 `out/param_tables.json` (113,135bytes/SHA-256`c6335d8b9d8436d9ee4fcc6a5d85274704dd30907700240de77c9db98c4947a7`), verified against its retained H4 manifest. Eleven virtual-kind3 indices102/104/116/118/121/123/125/127/129/135/137 are excluded; other kinds/continuouscontrols are not widened into this class. Resonator1 Type26 has native0..6, while Resonator2 Type59 has native0..5. N6's stored-emitted0..6 for Resonator2 is distinct metadata, not permission to extend the selected native range or infer a clamp/ABI/Live conversion. ResonatorOrder91 includes both0/1; serial/parallel coupling remains separately qualified. Resonator2 is off in the baseline, as are LFOs/noise, so many type/sync/gate changes are dormant; no productive effect, activation, symmetry, physical modal/noise metric or general equality law is assumed.

The complete compact105-alias catalog is specified by each inclusive domain below: every baseline cell is one of20 aliases for the same retained vector, and every other listed value is a prospective missing single-word vector. All85 fresh waveform priors, portable expected/comparator and grades remain NULL.

| Host index | Stored navigation name | Native inclusive range | Baseline alias | Missing values |
| --- | --- | --- | --- | --- |
| 0 | Mallet/OnOff | 0–1 | 1 | 0 |
| 11 | Noise/OnOff | 0–1 | 0 | 1 |
| 15 | Noise/FilterType | 0–3 | 0 | 1,2,3 |
| 25 | Resonator1/OnOff | 0–1 | 1 | 0 |
| 26 | Resonator1/Type | 0–6 | 0 | 1,2,3,4,5,6 |
| 27 | Resonator1/Quality | 0–3 | 2 | 0,1,3 |
| 58 | Resonator2/OnOff | 0–1 | 0 | 1 |
| 59 | Resonator2/Type | 0–5 | 0 | 1,2,3,4,5 |
| 60 | Resonator2/Quality | 0–3 | 2 | 0,1,3 |
| 91 | ResonatorOrder | 0–1 | 0 | 1 |
| 92 | Lfo1/OnOff | 0–1 | 0 | 1 |
| 93 | Lfo1/Type | 0–6 | 0 | 1,2,3,4,5,6 |
| 94 | Lfo1/Retrigger | 0–1 | 1 | 0 |
| 95 | Lfo1/Sync | 0–1 | 0 | 1 |
| 97 | Lfo1/SyncRate | 0–21 | 4 | 0,1,2,3,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21 |
| 106 | Lfo2/OnOff | 0–1 | 0 | 1 |
| 107 | Lfo2/Type | 0–6 | 0 | 1,2,3,4,5,6 |
| 108 | Lfo2/Retrigger | 0–1 | 1 | 0 |
| 109 | Lfo2/Sync | 0–1 | 0 | 1 |
| 111 | Lfo2/SyncRate | 0–21 | 4 | 0,1,2,3,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21 |

This newly identified declared finite class supersedes no earlier global claim: the prior assessment explicitly lacked a concrete missing whole class and did not prove all classes drained. NULL priors alone do not ban capture; DCL-014 and noise/physical/modal/ARM/public comparator uncertainties remain U. A future Root selection can use the existing139-word standing factory/model with full inputs/custody/first-fault policy, without new objects/tools/provider/FP treatment or calibration. No original calls, behavioral IDs, owner/release/site or shared routing changes are selected here. Required unsupported behavior staysU/productOPEN.


## Whole native integer-domain capture selected — 2026-10-21

Root selected the complete [fixed-preset native kind3 class](#fixed-preset-history-native-kind3-eligibility--2026-10-21):20 nonvirtual domains/105 aliases/86 full histories, with85 fresh single-word variants and one historical-input baseline. The [pre-call freeze](../../analysis/ableton-live-12.4.3/full-spec-v1/batch-collision-kind3-host-domains-v1/pre-call-manifest.json),27,691bytes/SHA-256 `34ee0dee377897b5b3924e8ce5637aa886e101c61cec628e06adfe1fefec2608`, binds all102 initial files including every new recording/check/assembly/freeze/parent-launch source,85 scripts,139-word input catalog and copied unchanged method sources before any call. Input/synthetic controls cover all domains, max5 versus max6, virtual exclusion, complete-history identity, no baseline replay or invented approval, NULL criteria and literal opaque Rate returns.

The retained `preset_c4` baseline is input/history metadata ONLY unless a separate exact actual approval is identified; it is not presented as an approved capture or assigned any new PID, receipt, metric or oracle. The prior approved whole12 supplies the existing model/protocol only because its complete event/process histories differ. The selected85 calls preserve warm11264 BEFORE queue/on4096key60vel100/off26146vel0/render44100/block512last68/default model/time/FP/providers, varying one host word without a crossproduct. Native59 stays0..5; eleven virtual domains are excluded.

Execution is once per selected child, first detected fault stops later children, no retry or extension. All finite silent, quiet, noisy, dormant and channel dispositions are retained with waveform priors/portable criteria/grades NULL; no new productive-effect, modal/noise metric, calibration, general host/Live/public/ARM law is assumed. Auto is sole actual/source peer after the final seal; Root is citation-only for all new actual/source/code/raw/results. This selection/status paragraph is not actual approval, an owner revision, a release, a coverage grade or product closure. Required unsupported behavior remains U and whole-Live coverage OPEN.


### Partial capture sealed for sole review

The [frozen actual packet](../../analysis/ableton-live-12.4.3/full-spec-v1/batch-collision-kind3-host-domains-v1/manifest.json),26,541bytes/SHA-256 `b1ac0121bd80341377ed0b4b194969c2d4ba86a5a7f92b288fdbeb50f13ff6ab`, retains159payloads and the entire105-alias86-history catalog. Execution stopped after16 attempted children:15 collector-recorded, then index58=1 exited0/full output but failed the frozen CalcA return/flag guard. The other69 selected plans were never launched. No original retry or guard correction occurred. All16 raw/stdout/stderr sets, failed phases/error, PID/UTC/argv and custody remain retained; the [partial-status note](../../analysis/ableton-live-12.4.3/full-spec-v1/batch-collision-kind3-host-domains-v1/PARTIAL-STATUS.md) distinguishes recorded status from independent approval and explains the historical RUNNING label left by post-child parse failure.

The post-capture readback is JSON bookkeeping only, explicitly not pre-call capture code or new numeric/semantic proof. Auto's one sole actual/source review covers all attempted bytes and literal failed-guard fields; Root remains citation-only. This is a partial investigation, not a completed85-result class or approved output. The historical baseline remains input-only, priors/portable criteria/grades NULL, required U and product OPEN. No continuation or successor is selected by this status filing.

## Native kind3 partial actual adoption and unlaunched continuation — 2026-10-21

[Auto’s sole actual/source review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/collision-kind3-host-domains-v1-partial-review.json),3,087,748bytes/SHA-256 `011fa84e0d430dfe31df3111ed1958a8c37789b6d3e13c633fb84e5cad616adc`, approves **15 bounded finite observations and partial-failure retention**, not completion of the85-input batch. The [partial manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/batch-collision-kind3-host-domains-v1/manifest.json),26,541bytes/SHA-256 `b1ac0121bd80341377ed0b4b194969c2d4ba86a5a7f92b288fdbeb50f13ff6ab`, seals159 payloads/10,810,983bytes;160files0444. Root adopts the approved summary by citation only, with no new actual/code/source/raw/result reads or numeric re-review. All105aliases/86histories retain one historical-input-only baseline,15approved fresh points, one guard-rejected discovery and69 unlaunched members. Baseline has no assumed approved output/PID/receipt/metric or replay.

The first15 approved outputs are finite/nonzero,12 have unequal channel words and all15 have nonzero warmup;13 fresh hashes are descriptive only. They contain3,765 selected exports/1,635CalcA/6,643,680stereo bytes. The16th i058-v01 exits0 with empty stderr/destroy/CXXfail0/full442,912-byte audio, but24 render blocks (indices13–36) log return1/flag1, violating frozen ret0. Its warmup is22×(ret0,flag0); render groups are8×(0,0),5×(0,1),24×(1,1),50×(0,1). Return1’s native success/failure semantics remain UNKNOWN. The guard remains FAIL, the child’s stale RUNNING status and outer exit1/AssertionError remain history; the16th is not approved success, waveform criterion or new grade. All16 raw captures total7,086,592bytes. No retry, status fitting, frozen repair or guard relaxation occurs.

The peer fully read six new sources/all85 scripts/139-word projections/all16 logs/audio and all105alias86history joins;23 independent negatives/opaque-Rate/guard-FAIL/audio boundaries pass. Owned partial-check PASS covers15 parsed successes plus16 retained file identities, not failed-child acceptance. All112 common-initial identities match15 child-after arrays plus the failure endpoint (1,792 pairs), not per-child-before/continuous provider/OSexec/build/fenv/ABI attestation. All capture/parent code was pre-call-bound in102files; separate post-capture JSON readback was not pre-call-bound and does not repair the recorder or constitute actual approval. Raw/log close/hash/JSONfsync/cleanup/after-wait limits, native Res2 type0..5 versus N6 stored0..6, dormant controls/noise/physical/public/ARM/metric U and NULL priors/portable criteria/grades remain.

**Later Root selection, after that sole partial review:** capture ONLY the exact69 `approved_summary.unlaunched_ids` once in one separate continuation packet. Inherit15 approved observations, the failed i058-v01 discovery and historical baseline by reference; never retry/replay any of those16 or baseline. Keep the SAME existing139-word preset model, warm11264 BEFORE queue, on4096/off26146/render44100/block512/last68/default time/FP and SAME ret0/flag0or1 guard. Planned maxima17,319 selected exports/7,521CalcA/30,560,928stereo bytes; first detected anomaly stops future children, no automatic extension or retry. No new model/object/provider/patch/tool/calibration or extra gate. Mix authors/Auto solely reviews, Root citation-only for all new actual payloads. The review’s no-continuation-selected field describes its freeze; this later selection changes neither that report nor the original failure. No owner/IDs selected yet; continuation cannot silently turn the failed16th into success or complete all85 successful observations. Required U / OPEN.


## Never-launched native integer inputs selected — 2026-10-21

Root selects ONLY the69 IDs in [Auto's sole partial review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/collision-kind3-host-domains-v1-partial-review.json) `/approved_summary/unlaunched_ids`. The [new pre-call freeze](../../analysis/ableton-live-12.4.3/full-spec-v1/batch-collision-kind3-unlaunched-continuation-v1/pre-call-manifest.json),24,715bytes/SHA-256 `c35df49445db13eb4e958240862dc5c436d40f9dddfaad0b92f19015d3b1425d`, binds all87 newinitialfiles including capture/check/assembly/freeze/parentcode,69 scripts/full105alias86historycatalog/inputs/context before any new call. The15 approved observations, failed index58=1 and historical input-only baseline are references only, never retried or replayed. The previous ret1×24 render blocks remain guardFAIL with native return semantics U.

The native log-parser function is byte-identical to the preceding frozen predicate: CalcA ret0/flags0or1. No guard relaxation or ret1 reinterpretation is selected. Same preset139words/warm11264-before-queue/on4096/off26146/render44100/block512last68/default model/time/FP/providers hold. Twenty-nine input and23 synthetic protocol negatives include failed-case replay, approved-control replay, baseline approval fabrication and ret1 rejection; nine opaqueRate and six audio controls pass. Initial mutable metadata assembly rejected a too-strict exactCLEAR review-field assertion before inputs/calls; the prefix-match correction is recorded before freeze, not an original retry.

The69 once-only children have planned17,319 selected exports/7,521CalcA/30,560,928stereo bytes, nested/initializer work unknown. First detected anomaly stops later children with allpartialbytes retained; no automatic extension or repair. All fresh priors/portable criteria/grades remain NULL, finite silence/noise/dormant/channel/warmup dispositions retained without a new effect/calibration/public/ARM law. Auto is sole newactual/sourcepeer afterseal, Root citation-only all new payloads. The complete catalog preserves15approved+1failed+69selected+1input-only baseline; this continuation cannot make all85originalplans successful. Selection is not actual approval or an owner/release/grade/site change; requiredU/whole-LiveOPEN persists.


### Never-launched continuation sealed, sole review pending

The [continuation final manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/batch-collision-kind3-unlaunched-continuation-v1/manifest.json),49,715bytes/SHA-256 `763c3a9dd799495a3b470d78a4b07e6df0b36163cec5adc93eadbcad20a68b28`, seals300payloads/37,974,034bytes/301read-onlyfiles with exacttree/hashes checked. Recorder metadata reports all69 once-only children exit0 without timeout/retry/error at14:08:06.588985–14:08:22.300375UTC,17,319 selected exports/7,521CalcA/30,560,928stereo bytes. The97 common initial custody entries match each69 child-after endpoint (6,693pairs), not per-child before snapshots or continuous provider/OSexec/build/entryFP proof.

Author verification is recorded-JSON bookkeeping and hash custody only, not independent actual/source/raw/audio interpretation. Auto is activated as sole actual/source peer; Root remains citation-only. The original15 approved observations and failed index58=1 remain inherited references without new calls; baseline remains historical input-only. The continuation's69 completed collector records do not repair the prior ret1 guard failure or make85 successful captures. All priors/portable criteria/grades NULL and requiredU/whole-LiveOPEN remain. No new owner or successor is selected by sealing.

## Native kind3 unlaunched continuation actual adoption — 2026-10-21

[Auto’s sole continuation actual/source review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/collision-kind3-unlaunched-continuation-v1-review.json),10,775,075bytes/SHA-256 `a8a1556b079394d72b09d0539ab4ffdf479a8f0223c5b14970c9e7bd12a4a87a`, approves all69 new once-only observations from the original unlaunched-ID set. The [final manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/batch-collision-kind3-unlaunched-continuation-v1/manifest.json),49,715bytes/SHA-256 `763c3a9dd799495a3b470d78a4b07e6df0b36163cec5adc93eadbcad20a68b28`, seals300payloads/37,974,034bytes;301files0444. Root adopts by citation only, no new actual/code/source/raw/result reads or numeric proof. The complete105alias/86history catalog now retains84 approved observations (15prior+69new), one earlier guard-rejected discovery and one historical-input-only baseline; this is not85 approved successes.

All69oncechildren exit0/empty stderr/no timeout/fault/error/retry at14:08:06.589–22.300UTC. They contain17,319 selected direct exports/7,521CalcA/30,560,928stereo bytes, all finite/nonzero with unequal channel words and nonzero warmup. Two fresh hashes are finite-context identities, not inactive-control/noise/Res2, deterministic, productive-effect or public/ARM laws. Owned29input/23synthetic/23actual/nine opaqueRate/six audio controls and29 independent negatives plus guard-ret1/flag2 rejection/INT_MIN,0,INT_MAX Rate/audio boundaries pass. All97 common-initial identities match69 child-after arrays (6,693pairs), not per-child-before/continuous runtime/provider/OSexec/FP attestations. All87pre-call payloads remain exact. The new parser function digest is checked; its inherited old guard identity is qualified rather than a fresh old-source/body audit. No first15, failedi058-v01 or baseline is replayed.

The frozen old ret0/flag01 guard remains unchanged. Earlier24returns1 in i058-v01 remain a guard failure with UNKNOWN native return semantics, stale RUNNING child status/outerexit1/partial phases and separately unbound post-capture JSON readback; none is repaired by this continuation. Baseline remains historical input only, no assumed approved X/PID/receipt/metrics/oracle. Existing139-word preset/warm-before-queue/time/FP/model, raw close/hash/JSONfsync/cleanup/import-vs-use/native59max5/source/default/public/ARM/physical/noise/metric limits and NULLpriors/portable criteria/grades persist.

Mix authors one combined R3 annex from the two sole-approved summaries:84 new DCL-063–146 IDs, one guard-failed U discovery and input-only baseline retained separately. Arrangement solely reviews new wording/mapping/preservation after its CorpusR11 proposal freeze; Root is citation-only for all new R3 proposal payloads from reassignment before any read. No ID credited until R3 application, no actual/source/raw/numeric redo, new metric/calibration/general law/release/site or product closure. Required U / OPEN.

## Collision owner R3 finite kind3 annex adoption — 2026-10-21

[Arrangement’s sole new-owner review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/collision-owner-r3-kind3-finite-v1-review.json),6,954,572bytes/SHA256 `8a3b3df046644949d1fa1074a0efa693e5010bd67c65bc4f8b95485ebc967c47`, approves the [R3 proposal](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-collision-r3-kind3-finite-v1/manifest.json),3,377bytes/SHA256 `327c40f8969367cfaf1f1fa65e7e9813d1dbceb9240ad5b59e06473acbf7a398`,ninepayloads/5,968,909bytes. Root applies the complete delta/target embedded in that sole peer report, remaining citation-only for ALLnewR3proposal and actual/code/source/raw/result payloads from reassignment before anyread. Applied [canonical R3](../specs/device-collision.md) is45,211bytes/SHA256 `d616266d87a39ad8ac8f7cb1076fabfd35ba96fbe77565035e960ef9b8079ae8`.

R3 adds84 DCL-063–146 IDs from the two sole actual summaries:15partial+69continuation. Full105aliases86histories retain the failedi058-v01 as unnumbered guardFAIL/U/no approvedsuccess/no nativeRet1law, plus one unnumbered historical-input-only baseline/noX/DCL002criterion/PIDreceiptmetrics/oracle. This is not85success. OnlyREQ002append/annex/revision changes;17otherwhole requirements/old002prefix/ALL62oldrows62IDs(50R1+12R2)/R2twelveobjects8relations/oldAcceptance/metricsnoisephysicalU/tolerances/history/released2cases2evaluations8inventory exact/fullreverse. Earlierouterexit1/staleRUNNING/failurephases/unboundpostcaptureJSONreadback/asof69unlaunched remain with their own dates; unchangedret0flag01guard never reinterpretsreturn1. Twenty-nineauthorcontrols/16independentpromotion/preservationnegatives pass. No actual/source/raw/numeric redo, general effect/noise/inactive/publicARM/calibrationlaw, criterion/grade/release/site or closure. Priors/portablecriteria/gradesNULL/newappFalse;146navigationIDs are not passes or denominator. RequiredU/OPEN.


## Remaining independent no-setter MIDI-byte axes eligibility — 2026-10-21

**Input metadata only; no capture or case IDs selected.** The Collision portion of [the complete remaining-axis input catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/electric-collision-remaining-midi-input-eligibility.json), 2,976,649 bytes / SHA-256 `6e6e6b49a9d95d8511234208525fc8497201d0f2de445051f29c8afc41140f42` uses the independently approved DCL-054 / `initial1-no-setter-released` control. It does **not** invent approval for the kind3 class's historical-input-only preset baseline. The [whole12 sole review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/collision-resonator-enable-histories-v1-review.json), SHA-256 `e899873b4bd4335aedc83013739fd8875d9d465db32d6daa929e70601131d086`, and the separately approved R2 owner catalog retain all139 ordered original tokens/words and the exact input protocol. This assessment uses their INPUT/identity paths only, without re-reviewing observations.

| Independent axis | Complete values | Other event fields fixed | Missing histories |
| --- | --- | --- | --- |
| Note Off key only | 0–127 | On key60 | 127 |
| Note On channel nibble only | 0–15 | Off channel0 | 15 |
| Note Off channel nibble only | 0–15 | On channel0 | 15 |

The160 aliases deduplicate to158 complete histories, with three baseline aliases sharing DCL-054 and157 missing histories. The fixed139-word vector hashes to `1a61d31521973c8eaa9167ca184704b787cda790d43db0c82a459d28caf0d0bc`; initial Resonator1 index25=1 and no boundary setter. Rate44100 and all139 setters precede inputflag0/zero input/warm11264; queue On4097/status90/key60/velocity100 and Off7168/status80/key60/velocity0, process8192 then4096 with512-frame blocks, then destroy. The exact baseline script is2040 bytes / SHA-256 `48a15b4f1483c5e92d9c940ae9469aaeecd3309ecf672851e9f298dc0111a2bc`. No timing, segmentation, warmup or parameter changes are proposed. The persistent queue and process-local clock remain unchanged: both events are strictly outside the second segment's[0,4096), so neither replays there. The label “released” means queued Note Off history, not a new envelope-state claim.

The approved12 input projections intersect only at this no-setter control. Existing metadata for41 old scripts, two released inputs and the kind3 class has different event/process/setter histories; no old Collision script, source behavior, raw output, metric, provider or original execution was reopened. Other Collision MIDI axes are not declared complete by this three-axis assessment. The supplied finite fields identify an admitted native-event recipe, not public ingress, current receiver, matching/dispatch or general channel/release law. Baseline criteria/PID/receipt/metrics never transfer; fresh waveform priors/portable expected/comparator/grades remain NULL. Full history, including both packed events, parameters, three process requests, queue placement, FP and environment, participates in dedup.

The shared assessment's21 metadata negatives pass. If separately selected,157 children contain29,516 selected direct exports /7,222 CalcA /29,581,312 raw stereo bytes; initializers/nested work remain separate/unknown. The complete lifecycle planning allowance is94,593,024 bytes: exact raw bytes plus12MiB logs/receipts,10MiB code/input/catalog/custody metadata,20MiB sole actual review and20MiB owner proposal/review. The combined Electric/Collision allowance is291,683,200 bytes, not an enforced cap or reservation; existing file-size limits admit a larger worst case, and concurrent work consumes workspace headroom. Root chooses accounting/placement only at later selection; no cleanup, storage arrangement or capture follows here. All old source/default/FP/provider/OSexec/0664 sealing/fsync/cleanup qualifications, general MIDI/public/ARM/physical unknowns and released criteria remain unchanged. Required unsupported behavior stays U / whole-Live OPEN.

## DCL054 independent Off-key and channel bytes selected — 2026-10-21

Root selects the [complete frozen pre-call class](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/batch-collision-independent-midi-bytes-v1/pre-call-manifest.json),28,977bytes/SHA256 `a69fcb758bcc8ad663d40b2d71cf3e479a34295bd6cd800a1b75a301241955bb`:179payloads/6,084,740bytes. The existing r2-large link resolves the new0700directory to `/var/tmp/sound-analysis/full-spec-v1/batch-collision-independent-midi-bytes-v1`, without newlinks/evidencemoves/deletion/install.160aliases158WHOLEhistories contain157fresh and threebaselinealiasesONE inheritedDCL054 INPUT reference; no oldPIDreceiptoutputmetrics/criterion replay/transfer. Independent OffkeyONLY0..127/fixedOn60; OnchannelONLY0..15/fixedOff80; OffchannelONLY0..15/fixedOn90. No crossproduct/newevent/timing/hostupdate/receiver/model/tool/patch/provider/calibration.

Same139orderedwords/vector1a61…0d0bc/exactoriginal2040Bbaseline48a15b4f…1a2bc, create/rate44100/allsetters/inflag0zero/warm11264 BEFOREqueueOn4097v100/Off7168v0/process8192then4096/block512/no boundarysetter. Existingprocess-relativeeventclock/queue unchanged; secondsegment[0,4096) excludes4097/7168/no eventreplay. This is the approvedwhole12no-settermodel, NOTkind3baseline/failureretry. Allnewsourceparent/analysis/checker/initialassembler/context/scripts/model/env pre-call-bound.23input/14protocol/fivePRECALLparent negatives/tworesourceboundaries/threeopaqueRate/threeedges/sixunsignedshape groups pass before calls.

157sequentialonce/20sCPUwall/core0/4MiBfiles/DEVNULL/newgroups/firstfaultstop/noretry/fullrawlogs/PIDUTC/argv/importbindings-vs-used/flags/cxx/beforeaftercustody;29,516selectedexports7,222CalcA29,581,312rawstereoB, initializer/nestedcountsseparate.8,695,947,264bytes free versus94,593,024Bnormalfull-lifecyclebudget+128MiBheadroom/extra352MiBconcurrentbatch allowance; unreserved prechildremainingraw+48MiBmetadata+128MiBguard. MixSOLEactual/sourcepeer afterTensionreview/finalseal; Rootcitation-only ALLnewactual/code/source/raw/results. Old0664/source/default/FP/provider/OSexec/fsync/cleanup limitations keep oldscope/no retrorepair. Keepzero/nonfinite/failure/U, NULLpriors/portablecriteria/grade/newappFalse; no unmatchedrelease/publicARMlaw/newmetric/fit/calibration/ownerIDs/closure.

## Independent no-setter MIDI-byte batch selected — 2026-10-21

Root selects the [DCL054 no-setter class](#remaining-independent-no-setter-midi-byte-axes-eligibility--2026-10-21):160aliases/158completehistories/157fresh, OffkeyONLY/fixedOn60, OnchannelONLY/fixedOff80 and OffchannelONLY/fixedOn90. Three baseline aliases inherit ONE approved DCL054 INPUTreference without replay/newPIDreceiptmetrics/criterion. This uses the approved whole12 control, not the kind3 historical-input-only baseline or its failed input. Arrangement authors; Mix is sole actual/source peer after final seal and its prior Tension review. Root remains citation-only for ALL new Collision actual/code/source/raw/results from assignment before any read.

All139 original tokens/1a61…0d0bc vector, exact2040B/48a15b4f…1a2bc baseline, rate44100/setters/inputflag0/zero/warm11264 BEFOREqueue, On4097/90/60/100 and Off7168/80/60/0, process8192then4096 at512/no boundarysetter remain. The existing queue/local clock model leaves both events outside the second segment; no second-segment event replay or new timing interpretation is introduced. No extra event, host crossproduct, receiver construction, model/tool/provider/patch or calibration. The NEWpacket uses existing analyst storage at `r2-large/full-spec-v1/batch-collision-independent-midi-bytes-v1`;94,593,024B normal lifecycle estimate plus128MiBheadroom/concurrent allowance/resource guards must fit. All new code/parent/analysis/checker/initialassembler/context/scripts bind before once157, with meaningful controls/first-fault stop/no retry/partial retention. Older0664/source/default/FP/provider/OSexec/fsync/cleanup limits remain with their own scopes. No owner/IDs/portable criterion/grade/general unmatched-key/release/publicARM law is selected; required U / OPEN.

The selected DCL054 residual-byte class is now [author-sealed for Mix's sole actual/source review](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/batch-collision-independent-midi-bytes-v1/manifest.json),108,220bytes/SHA256 `7cadb9f1efac68d0b851053deddb9abbd27e828365d96ea90ae4a15b30673f1c`:658payloads/46,285,330bytes/all659files0444/directory0700. All157plannedcaptures completed once; full158history160alias catalog and ONE inherited DCL054 INPUT reference retained. Owned authorcheck4,943,420bytes/SHA256 `ce45553f4eab1c1a28231e69172b38fb4e4693489bf8d8db9922cf04bee169c9` passes; sealed safechecker output is byte-exact. Pending independent actual admission, with no owner IDs/criteria/grade or general unmatched-release/channel law; Root remains citation-only for all new actual/code/source/raw/results.

## Independent no-setter MIDI-byte actual adoption — 2026-10-21

[Mix’s sole actual/source review](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/collision-independent-midi-bytes-v1-review.json),4,225,681bytes/SHA256 `7ba3cc8262e08d20d411210d976d4e67aea4caa8004e0df0359e6386758c799c`, approves157fresh/full160aliases158completehistories/one inherited DCL054 INPUTreference shared by three aliases. [Final manifest](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/batch-collision-independent-midi-bytes-v1/manifest.json),108,220bytes/SHA256 `7cadb9f1efac68d0b851053deddb9abbd27e828365d96ea90ae4a15b30673f1c`, seals658payloads/46,285,330bytes/all659files0444/directly in the existing analyst store. Root adopts by citation only, with no new actual/code/source/raw/result read or numeric proof replay.

The reviewer fully read all5newsource files/README/assessment/authoring history before the packet-only checker, then independently checked all157scripts/139originaldecimal-f64 words/logs/receipts/29,581,312rawbytes/custody/parents/precall/tree and full history/alias joins. Twenty-two independent negative controls/6unsigned groups pass, plus23input/14syntheticprotocol/5preparent/2resource boundaries/3Rate/3edges/6unsigned/14retained/4postparent owned controls. The first independent control pass stopped because a hardcoded warmup RLE literal did not mutate the actual log. The unsealed reviewer test was corrected to remove the exact retained warmup line; no frozen guard, packet, original call or retry changed.

All157oncechildren exit0/emptyerr/no timeout/error/retry at15:00:15.091498–15:00:23.854698UTC/outer1445891.29,516selectedexports7,222CalcA/0loggedinitializers/nestedunknown. All157 outputs are finite/nonzero in both channels with unequal words and ONEfreshwhole-filehash. This is a local descriptive identity, not an old-baseline audio comparison or a general no-effect/inactivity/ignored-event/key/channel/release law. New129name/binding/slot import records (96linux26trap7data), seven export declarations and initializer list match across all157fresh children;59counted used-code names are Linux-bound. The old policy supplied counts, not invented exact historical addresses; declarations do not establish provider/global-data absence.

Ten whole-source endpoint pairs and2,355per-child15pairs match, without continuous provider/nativeFP/OSexec proof. Success paths request log/audio/JSON/JSONL FDfsync, not directory/crash durability or old-gap repair. Recorded available bytes cover remaining raw plus48MiBmetadata128MiBheadroom;94,593,024B lifecycle planning is unreserved/not a quota. Post-child/parent-loss/escaped-process cleanup limits remain. Historical assembler/flattened slice metadata/pre-output KeyError remain disclosed, with final code completed before pre-call seal; no new native header, source/default/build or model proof follows.

The approved DCL054 input keeps139tokens/1a61…0d0bc, warm11264 BEFOREqueue4097/7168, process8192then4096/block512/no setter and no second-segment replay. Three baseline aliases inherit INPUTapproval only/no replay/PIDreceiptmetrics/criterion/modal-budget transfer. This is a different history from the kind3 partial packet; its failedi058-v01/unknownRet1/outerexit1/staleRUNNING/unboundpostJSONreadback/input-only baseline stay unchanged and ungraded. Newret0/flag01guard is unchanged. Priors/portable criteria/gradesNULL/newappFalse, no general matching/release/velocity0/publicARM/physical/calibration law; requiredU/whole-LiveOPEN.

Arrangement authors ONE R4annex157DCL147–303 from this sole-approved summary. Root is sole NEW wording/mapping/preservation peer for R4, while remaining citation-only for all actual payloads and old R3proposal payloads. The new owner checker must use only current canonical owner, newMixapproved summary and priorR3sole-peer embedded mapping/preservation; no old R3catalog/code/raw/provider/fixture reads. No IDs credited until application; currentR3/146navigationIDs/62oldrows/criteria/releases remain.

## DCL054 remaining five MIDI-axis input eligibility — 2026-10-21

**Input metadata only; no capture selected.** The [complete catalog and embedded computation](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/collision-dcl054-five-midi-axis-eligibility.json),4,424,964bytes/SHA256 `c33b6beb2dee3b66cab6fcbca7a034b83eb014c21c0f649b9d5f07d7848263c7`, computes528aliases/524WHOLEhistories at the already approved DCL-054 no-setter recipe. Independent axes:OnkeyONLY0..127/fixedOff60; matchingBOTHkeys0..127; Onvelocity0..127; matchingBOTHchannelnibbles0..15; Offvelocity0..127. Five baseline aliases (60/60/100/0/0) share ONE DCL054 approved INPUT reference. The other523 histories are missing in this bounded input cut, not globally absent. No parameter/event/timing/process crossproduct.

The computation uses ONLY older [input eligibility](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/electric-collision-remaining-midi-input-eligibility.json),2,976,649bytes/SHA256 `6e6e6b49a9d95d8511234208525fc8497201d0f2de445051f29c8afc41140f42`, its approved12 and old41/released2/kind3 input projections, old approved DCL054 input provenance, and the exact2040-byte baseline script48a15b4f…1a2bc. New Collision157 actual/code/raw/results/approval is NOT used as proof or a source. Each member retains original139decimal/binary32/binary64 identities, complete event/process/FP/environment history hash, both packed16events and full generated original-script UTF8 size/hash.14 input corruption controls pass, with zero original calls or audio/numeric/sourcebehavior/provider reads.

Exactly ONE of the12 approved input histories joins: DCL054/initial1-no-setter-released. The other11 differ in initial vector, missingOff or boundarysetter. All41 old scripts differ in firstOn coordinate/process history; the predecessor's occasional `exact-domain-history` classification refers to parameter-vector identity and does NOT establish whole-history equality. Released2 inputs and the kind3 recipe also differ (On4096 or0/Off26146/process44100 versus4097/7168/8192+4096). Kind3's historical baseline stays INPUT-only, not an approved output criterion. The prior three residual axes' INPUT metadata intersects this new class only at the same baseline; no new actual approval is credited. No baseline replay/newPIDreceiptmetrics/outputcriterion/modalbudgettransfer is proposed.

If separately selected,523 children through unchanged whole12xdev/model/context would contain98,324 selected direct exports/24,058CalcA/98,541,568full-stereo bytes, with initializer/nested native counts separate. The normal full-lifecycle capture+author+peer-report estimate is320MiB plus128MiBheadroom; rootstore had8,375,558,144bytes free as of this metadata snapshot. These are unreserved estimates requiring fresh pre-call/per-child resource guards if selected, not execution authorization or aggregate hard-output proof. No cleanup/move/link/install, newmodel/tool/patch/provider/calibration/criteria/grade/IDs is selected. Samewarm11264BEFOREqueue4097/7168→8192+4096/noSetter/no2ndsegmentreplay/exact139tokens remain mandatory; no velocity0/unmatchedrelease/pitch/channel/noeffect/publicARMlaw/f0/fit/newmetric/tolerance inference. Oldsource/default/FP/provider/OSexec/fsync/0664/cleanup limits retain scope; requiredunsupportedU/OPEN.

## Collision owner R4 independent MIDI annex adoption — 2026-10-21

[Root’s sole new-owner review](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/collision-owner-r4-independent-midi-finite-v1-review.json), 7,748,367 bytes, SHA256 `90e42ccdfc61efb032e947633dbb9dcf25921d23f5425ec4e3fbedae9f2859fe`, approves wording, IDs, mapping and preservation only. The [manifest](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-collision-r4-independent-midi-finite-v1/manifest.json), 3,725 bytes, SHA256 `e4084ed440ad48a45a810f02db97bb58f0d4332b3f839a887cb4028574170808`, records nine payloads / 6,419,491 bytes. Root applied the exact 53,159-byte canonical target, SHA256 `bd9b95cd5cdf128c1b3813eb559563117f6992ff89685792674268fcb7eda7a5`.

R4 adds 157 DCL-147–303 IDs, full 160 aliases / 158 whole histories and one inherited DCL-054 INPUT reference shared by three aliases. Only REQ004, its annex and revision change; seventeen other whole requirements including all R3 REQ002, the old REQ004 prefix, 146 old IDs / 62 rows, R2/R3 objects and eight relations, criteria and release scope (two cases / two evaluations / eight inventory entries) remain exact. The sole owner checker reads exactly current canonical owner, new Mix actual-review summary and prior Arr R3 peer embedded mapping/preservation. No old R3 proposal/catalog/code/actual/source/raw/provider/release manifest or fixture was read. Old pins are inherited reviewed facts, not fresh custody proof.

Thirty author and twenty-one independent peer negatives pass. Root corrected its unsealed metadata filename assertion from check-results.json to author-checks.json before sealing; no evidence, canonical delta or original call changed. The old kind3 failed i058-v01 guard FAIL/U, unknown Ret1, input-only baseline, 84 rather than 85 successes, outer exit1/stale RUNNING and unbound JSON readback remain unchanged. This is the different DCL-054 no-setter history; no retry or repair. One fresh hash is descriptive only. All new portable criteria/grades remain NULL and application proof false; required behavior U / product OPEN.

## DCL054 five remaining MIDI axes selected — 2026-10-21

Root read the preceding canonical INPUT-only assessment and its complete frozen metadata summary (4,424,964 bytes / SHA256 `c33b6beb2dee3b66cab6fcbca7a034b83eb014c21c0f649b9d5f07d7848263c7`). Root selects 523 missing histories / full528 aliases524 histories under the unchanged admitted DCL054 no-setter model: On-key-only, matching both keys, On velocity, matching both channel nibbles, Off velocity. Five aliases share ONE inherited DCL054 INPUT reference; no baseline replay or PID/receipt/metric/criterion transfer. These differ from the prior157 residual axes and are selected individually without a crossproduct.

Mix authors one frozen `batch-collision-dcl054-five-midi-axes-v1` packet after Corpus R14 sealing. Auto is its SOLE actual/source peer after Electric R8 sealing. Root is citation-only for ALL new actual/code/source/raw/results before any reads. This is an execution selection under the standing harness authorization, not another preflight/readiness/root gate. All new parent/recorder/checker/input context must be final before once-only calls; safe synthetic controls and full sole actual/source review remain required. The existing store and current model are mandatory; no native patch, new construction/tool/provider/emulation/calibration/metric/window/tolerance is selected.

Preserve the original139 decimal/f64 words, warm11264 BEFORE queue4097/7168 then process8192+4096 at512, no setter and no replay of events in the second segment. Pre-parent and pre-child resource guards must admit full remaining output and metadata/headroom; planning320MiB full lifecycle plus128MiB concurrent headroom is unreserved, not a hard quota. Stop on first fault/resource limit, retain partials and do not retry. If this cannot fit the unchanged route, file the exact blocker. No new IDs, criteria/grades or release follow from selection; prior failure/history/limits remain unchanged, required U / product OPEN.


## DCL054 five-axis pre-call freeze — 2026-10-21

The selected whole class is [pre-call frozen](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/batch-collision-dcl054-five-midi-axes-v1/pre-call-manifest.json), 93,322 bytes / SHA256 `79cc35eb396e8d05feab40ccf4e0d0ce9f8c8ef11bdfad3944b3883a9a96a102`:546payloads/19,734,412bytes, including every new parent/recorder/checker/data/initial-assembler/freezer file and all523 scripts. The existing r2-large path resolves to `/var/tmp/sound-analysis/full-spec-v1/batch-collision-dcl054-five-midi-axes-v1`; no new link, evidence move or cleanup. Full528 aliases524 whole histories retain ONE inherited DCL054 INPUT reference/five baseline aliases, no baseline replay or PID/receipt/metric/criterion transfer.

Mix's data-only controls pass:25 input/15 protocol/5 parent negatives, two resource boundaries, three opaque Rate positives, five event edges and six unsigned shape/bit groups. No original calls preceded this seal. The resource snapshot is8,225,914,880bytes free against unreserved320MiB lifecycle+128MiB headroom planning; pre-child guards cover all remaining raw plus96MiB metadata and128MiB headroom, with a320MiB packet soft stop and possible launched-child overshoot. This records the already selected capture, not another gate or hard quota.

The exact139original-token/f64 recipe, warm-before-queue/no-setter/4097+7168→8192+4096 history and unchanged ret0/flag0or1 guard remain. Once523/first-fault stop/no retry; all quiet/edge/partial data stay retained. Auto is the sole actual/source peer after final seal; Root is citation-only all new actual/code/source/raw/results. Fresh priors/portable criteria/gradesNULL/new application proofFalse; no new owner IDs or public/ARM/physical law. Required unsupported U / product OPEN.


The five-axis capture is now [author-sealed for Auto's sole actual/source review](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/batch-collision-dcl054-five-midi-axes-v1/manifest.json),368,826bytes/SHA256 `71d6fd90c7cae04f76fbd5aaa8e55c90b71b7a4b76cf2da0fc854f2a2fd230b6`:2,123payloads/137,110,925bytes/all2,124files0444/exacttree-hash check passes. Once523children completed15:54:33.693666–15:55:18.680400UTC/outer1455702 with recorder exit0/errorNULL/no retry,98,324selectedexports/24,058CalcA/98,541,568rawbytes/0loggedinitializers; nested counts unknown. Author checks only receipt/counter/frozen-input bookkeeping after capture, without reopening actual audio/stdout/stderr for self-review. Complete524history528alias catalog includes the five shared baseline INPUT aliases, without new baseline evidence. Auto receives the full source/packet for one independent review; Root remains citation-only. This is pending actual admission, with no owner IDs, waveform criterion, grade, public/ARM or general matching/release/channel law.

## DCL054 five MIDI-axis actual adoption — 2026-10-21

[Auto’s sole actual/source review](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/collision-dcl054-five-midi-axes-v1-review.json),35,092,417bytes/SHA256 `0dd108e1ea1bc56fbf06250243f5319dabb5e20c1072113c259b489d8d142d9f`, approves523fresh/full528aliases524whole histories/one DCL054 INPUT-only reference shared by five aliases. The [manifest](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/batch-collision-dcl054-five-midi-axes-v1/manifest.json),368,826bytes/SHA256 `71d6fd90c7cae04f76fbd5aaa8e55c90b71b7a4b76cf2da0fc854f2a2fd230b6`, seals2,123payloads/137,110,925bytes/2,124files0444. Root adopts by citation only, with no new actual/code/source/raw/result or numeric-proof read.

The sole reviewer read all six new source files before the safe check and independently checked523scripts/logs/receipts/98,541,568rawbytes/both lanes/all528aliases524histories/original139decimal-f64 words/model/input/parents/precall/custody/resources. Fourteen independent protocol negatives, seven unsigned groups and three opaque-Rate positives pass; owned25input/15protocol/5parent/2resource plus14retained/4parent controls pass. All523once-only children15:54:33.693666–15:55:18.680400UTC exit0/no fault/retry,98,324selected exports/24,058CalcA/zero logged initializers/nestedunknown. All523outputs finite/nonzero in both channels,522word-unequal/oneequal and181freshhashes are descriptive only. Literal Rate1 remains opaque. No general event admission, pitch, velocity0, channel, release, productive-effect or public/ARM law follows.

Eleven whole-source pairs plus7,845actual per-child15before/afterpairs match, not common-initial-only custody. New log/audio/JSON FD-fsync requests do not establish directory/crash durability or repair old0664/default/FP/OS-exec/source/cleanup gaps. Existing139word/noSetter/warm11264 BEFOREqueue4097/7168→8192+4096/512/no second-segment event replay remains fixed; first-fault/resource/partial/no-retry guard scope stays bounded. Old kind3 i058-v01 guardFAIL/U/unknownRet1/input-onlybaseline/outerexit1staleRUNNING/unboundJSON readback remains unchanged; this is a different DCL054 history.

Arr authors R5 after its remaining-control INPUT assessment seals. Root is sole NEW wording/IDs/mapping/preservation peer while staying citation-only ALL new actual payloads and old R3 proposals. The new owner checker may read only current canonical R4, this Auto approved summary and Root’s R4 peer embedded mapping/preservation; no old R3catalog/code/provider/release manifest/fixture reads. Preserve17otherwhole including entire R3REQ002/old004R4prefix/303oldIDs62rows/R2–R4objects/eightrelations/criteria/releases2cases2evaluations8inventory/history/fullreverse. No IDs until application; new portablecriteria/gradesNULL/applicationFalse/no general calibration/public/ARM law/requiredU/productOPEN.

## Collision owner R5 five-axis annex adoption — 2026-10-21

[Root’s sole new-owner review](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/collision-owner-r5-dcl054-five-midi-axes-finite-v1-review.json),8,717,117bytes/SHA256 `b96f42d58cd27d50715af7d0569d879b0af83569cde25c15226b56b60c148c90`, approves wording, IDs, mapping and preservation only. The [manifest](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-collision-r5-dcl054-five-midi-axes-finite-v1/manifest.json),3,841bytes/SHA256 `54d33c64971578d79c082d7da7ef993fb8421f290cab9da3672db46aca896b61`, seals ten payloads/7,532,771bytes. Applied canonical target:61,492bytes/SHA256 `87c2c05ab7c302672f29f326f2167122c77508589273cd3fc211a99fc1b76cb0`.

R5 adds523 DCL-304–826 IDs/full528aliases524histories/one DCL054 INPUT-only reference shared by five aliases. Root read all new checker/README/delta/authoring history/historical stage source before the safe --check; stage-owner.py was never executed/imported. Thirty-one owned and twenty-three independent mapping/preservation/wording negatives pass. An initial guessed assessment.json filename was absent; corrected to manifest-listed authoring-history.json before any check, with no evidence/canonical/original-call changes. Slim per-ID case references resolve to complete catalog rows rather than duplicating native observations.

Exactly current R4 canonical, Auto’s new sole actual-review summary and Root’s R4 peer embedded mapping/preservation supply external authority. Root remains citation-only for ALL actual/code/source/raw/results and old R3 proposal payloads; no old catalog/provider/release manifest or fixture was reopened. Earlier object/release pins are inherited reviewed facts, not fresh custody. Seventeen other whole requirements including all R3 REQ002, old R4 REQ004 prefix,303oldIDs62rows/R2–R4objects/eightrelations/old Acceptance/criteria/U and release2cases2evaluations8inventory remain exact, with full reversal.

The prior kind3 failed i058-v01/unknownRet1/guardFAIL/U/unnumbered INPUT-only baseline/84not85successes/outerexit1/staleRUNNING/unbound readback remain unchanged. New523 histories retain no-setter/warm-before-queue/no second-segment replay,11source+7845per-child15pairs/newFDfsyncrequests/522unequal1equal/181hashes as descriptive bounded facts only. New waveform expectations/portablecriteria/gradesNULL/applicationFalse, no general MIDI/velocity0/release/channel/public/ARM/calibration law or closure. The826navigationIDs are not passes or product denominator units.

## Complete Mallet controller input class selected — 2026-10-21

Root selects the complete two-axis class in Arrangement's [INPUT catalog](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/collision-mallet-controller-cells-input-eligibility.json): 1,752,231 bytes, SHA256 `3b0be2a9b905852d8a2dc8aa0937f992efc5f4b0e0762831955dfde7265a4ae4`. Current R5 REQ008 explicitly gives Mallet Volume and Stiffness the floored U controller mapping. H4/N6 metadata identifies host indices 1 and 4, each nonvirtual native 0..1 with identity Live conversion. For each axis, the catalog supplies all 128 representatives `repr(n/127)`, with every other original preset word fixed. Rational checks of the supplied binary32 words visit all 128 declared labels; they enumerate INPUTS, without proving native arithmetic, within-cell equivalence, physical response or a general control law.

Both original host values are exactly 0.5, which is absent from the representative grid even at binary32 precision. Thus all 256 histories are distinct and missing in the bounded INPUT cut, with no inherited baseline. The prior kind3 assessment's retained 41-history classifications identify only preset_c4 as sharing this nonparameter history; its two values remain 0.5. The other forty differ, including named stiffness histories with key48/On0/render32768. Those classifications and pins are inherited INPUT metadata, not a new source/raw/numeric audit. The approved twelve enable histories, released inputs and later DCL054 MIDI classes have different event or process histories. This is bounded input intersection, not global absence, parameter-vector-only equality, a new PID/receipt/metric/output/criterion or a repair of old data.

Fourteen author INPUT corruption controls pass. Root reconstructed all 256 full scripts from the original input declaration and checked all 139 decimal/f64/f32 words, hashes and rational labels. Its first runtime metadata validator expected word lists where the retained fields correctly use concatenated little-endian hex strings; it stopped before document edits or original calls. The sealed failure remains and v2 corrects only Root's representation expectation, without changing input/evidence bytes. No actual/source/code/raw/results, native output, estimator, provider or old R3 owner proposal was opened or replayed. The old failed kind3 index58=1, input-only baseline, 84-not-85 count and every associated qualification remain unchanged; this class changes only host1 or4 and does not retry that failure. Noise/physical/modal comparators, A1/A2, public delivery and ARM/FP/source uncertainty remain U.

Auto authors one `batch-collision-mallet-controller-cells-v1` after sealing Playback4. Arrangement is the sole actual/source reviewer after its Electric124 review, disclosing INPUT authorship and having no capture/control authorship. Root remains citation-only for all new Collision actual/source/code/raw/results. The whole class executes once under the unchanged preset_c4/139-setter model: original decimal tokens except one host, rate44100, zero input/flag0, warm11264 BEFORE queued On4096/key60/velocity100 and Off26146/key60/velocity0, then render44100/block512/destroy, TIME0 and the existing FP/provider/native loader. DCL054's timing or no-setter history must not replace this one.

All new collector, parent, assembler, checker, analysis, finalizer, scripts and context freeze before calls. One frozen packet receives one actual/source review; author post-capture bookkeeping stays metadata-only. Fresh parent and pre-child guards must admit complete remaining output, metadata/final allowance and headroom. First detected fault/resource limit stops later children, retaining partials without retry or guard relaxation. Prospective totals are 256 children, 64,256 selected direct exports, 27,904 CalcA calls and 113,385,472 raw stereo bytes; initializer and nested work remain separate. The 512 MiB full-lifecycle estimate plus 128 MiB headroom is unreserved and does not prevent concurrent-writer, escaped-child or within-child overshoot. No new tool/build/model/provider/FP treatment, native construction, calibration, fit, metric or threshold is selected. New priors, portable criteria and grades remain NULL; application admission is false. Selection adds no owner IDs, release or closure; required behavior without evidence remains U and product coverage OPEN.


## Mallet controller capture author status — 2026-10-21

Auto froze [all selected inputs and source versions](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/batch-collision-mallet-controller-cells-v1/pre-call-manifest.json) before any selected call: pre-call manifest 45,014 bytes, SHA256 `0f330482c87d27879bf68b3e13f1af6b71ab26f084a5183b129f2b7a9e28375e`. It binds the complete 256-script catalog, exact initial authoring history, parent, capture/check/finalizer code and fixed context. All 128 Mallet Volume and all 128 Stiffness representatives are fresh; neither axis inherits the literal 0.5 baseline. The original 139-setter preset, warm-up-before-queue order, existing model and failure guards remain fixed. Arrangement is the sole actual/source peer after final seal, disclosing INPUT authorship only. Author capture/bookkeeping is not independent approval, portable criteria, new cases or public/ARM/calibration proof. Root remains citation-only for every new actual/code/raw/result payload; shared routing and owner admission are separate.

## Mallet controller partial packet awaiting sole review — 2026-10-21

The author reports125attempts:124recorded, one frozen protocol AssertionError at MCI-001-124 (Volume representative124), and131never launched. The failed child exited0 with empty stderr and full-length raw output; these are author-reported metadata pending Arrangement's sole source/actual review, not an admitted protocol, metric or pass. No retry, continuation or guard change is selected. The [partial manifest](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/batch-collision-mallet-controller-cells-v1/manifest.json),108,939bytes/SHA256 `a0b530c04a6017a32fa95483920803212a6b3b53846c487e20f21419fd9c21cc`, seals662payloads/65,251,534bytes/all663files0444. Root remains citation-only for all new actual/source/code/raw/results.

A separate metadata-only finalizer error requested recorded_raw_bytes while the checker emitted raw_bytes. Frozen source and already-written bookkeeping remain unchanged; an additive JSON-only sealer is explicitly post-capture, not pre-call-bound. The exception was tool-returned, without a standalone original stderr file; retained assembly history must not be presented as that missing original receipt. The external [assembly qualification](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/collision-mallet-controller-partial-assembly-qualification.json),4006bytes/SHA256 `818d4906174d1f6f9ed10760686b406c070060e05f29784288ceb45158879681`, records metadata-only missing/mismatch controls; it changes no frozen packet or native classification. The sole review will assess recording, failed guard, durability and additive sealing separately. Failed/unattempted histories remain U, with no IDs/expectations/grades; no actual admission or closure is made here.

## Mallet controller partial actual adoption — 2026-10-21

[Arrangement's sole actual/source review](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/collision-mallet-controller-cells-v1-review.json), 24,096,318 bytes, SHA256 `9968349497c41a6f1ba9c7d20a1e5c150088abf4fc3949890497b75b5d12d814`, approves **124 finite observations, one guard-FAIL/U discovery and retention of 131 unattempted U histories**. The full 256-history/two-axis catalog remains incomplete. The [partial manifest](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/batch-collision-mallet-controller-cells-v1/manifest.json), 108,939 bytes, SHA256 `a0b530c04a6017a32fa95483920803212a6b3b53846c487e20f21419fd9c21cc`, seals 662 payloads/65,251,534 bytes/all 663 files readonly. Auto authored capture/control; Arrangement solely reviewed it, disclosing earlier INPUT authorship. Root adopts the approved summary by citation only; this filing performs no actual/source/raw/numeric proof review.

The batch attempted 125 children once and stopped at MCI-001-124, Mallet Volume host1 representative124/127. That child exited zero with empty stderr and full-length output, but its ninth render block at frame4096 logs `ret=1,flag=1`; the unchanged ret0 predicate rejects it. Native return meaning, ABI and cause remain unknown. Its finite raw diagnostic is not an accepted waveform, metric, expectation or success. The other 131 histories were never launched, including all 128 Stiffness representatives. No failed input or literal0.5 baseline is replayed, and no retry, continuation, guard relaxation or new return policy is selected here.

The 124 accepted outputs are finite and nonzero in both lanes, all channel-word-unequal, with nonzero warm-up and 124 distinct hashes: descriptive facts only. Their accepted counts are 31,124 selected direct exports and 13,516 CalcA calls, with zero logged initializers and nested work unknown. All 125 attempted raw files total 55,364,000 bytes; failed-child work is separate from accepted counts. Rate1 remains opaque. The reviewer checked all 256 input/disposition joins and all 125 logs/raws, including the failed child omitted by the owned acceptance checker. Independent protocol, resource, unsigned-word and packaging controls pass.

Seven whole-batch source pairs and **2,250 actual per-child before/after pairs** (eighteen per attempt) match. These endpoints do not establish continuous loaded-provider, FP, OS-exec or historical source/default/environment equivalence. Accepted audio/log/JSON FD-fsync requests retain their limits; the failed guard skips its later raw FD-fsync branch, leaving failed audio close/hash custody only. The separate finalizer key mismatch and additive post-capture JSON-only sealer remain explicit: that sealer was not pre-call-bound, and no standalone original traceback file is invented. Correct packaging does not repair the failed native guard.

R6 is staged, not adopted; this actual adoption adds no owner IDs, criteria, grades or release. All fresh priors/native waveform expectations/portable criteria/grades remain NULL and application proof false. No native quantizer, within-cell, productive-effect, noise/physical/modal, public/ARM or calibration law follows. Earlier kind3 i058-v01 failure and its distinct history, input-only baseline and 84-not-85 qualification remain unchanged. Earlier selection/as-of paragraphs remain historical; required unsupported behavior stays U and product coverage OPEN.

## Collision owner R6 partial Mallet annex adoption — 2026-10-21

Root's [sole NEW wording/IDs/mapping/preservation review](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/collision-owner-r6-partial-mallet-cells-finite-v1-review.json),7282950bytes/SHA256 `933315601abb09e3212eaf6ba836b198c00b7dc2456da29771c9fb83be397bb3`, approves and applies exactly69525bytes/SHA256 `b1b397febffffe1a99ae084a780a0bd3a564b6112baad7d79171d11e2063cbb9`. The [manifest](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-collision-r6-partial-mallet-cells-finite-v1/manifest.json),2435bytes/SHA256 `2e73223e668bef8a0e5370acc23f68103769664853b3121739fd9e60957b3b39`, seals9payloads6914713bytes/all10files0444/private0700/exacttree.

ONLY124 DCL827–950 map accepted Volume representatives0–123; all256dispositions remain complete, failedVolume124U and131unlaunchedU unnumbered/no accepted metric/expectation/grade. All18wholeREQ/826oldIDs62rows/R2–R5objects/eightrelations/criteria/U/history/releases2cases2eval8inventory remain exact, with fullreverse. New native-waveform expectations/portablecriteria/gradesNULL/appFalse. Nonzero warmups, failedret1 unknownABI/cause/rejection/skippedfailedrawfsync/diagnostic-only raw, additivepostcaptureNOTprebound packaging/finalizerfieldmismatch/no standalone originalstderr and oldkind3failure84not85 remain qualified. No continuation/guardchange/retry/quantizer or within-cell law.

Root FULLread new80linechecker/191linehistoricalstager/README/delta/history INERT before ONLYsafecheck/NEVERstager.27owned29Rootnegative controlsPASS; allnewmapping/wording/preservation independently checked using exactly currentR5+ArrangementapprovedpartialREPORT+RootR5ownerREPORTembeddedmetadata. Root remains citation-only actual/source/code/raw/numeric/provider/oldR3proposal/catalog/fixtures, with no proof replay or absent-object reconstruction. The safecheck equals author-validation's nested check_output; Root's initial unsealed wrapper-comparison assumption stopped before approval and was corrected after key inspection, with no evidence change.950navigationIDs are not passes or a product denominator; no release/implementation/closure.

## Whole never-launched Stiffness class selected — 2026-10-21

Root selects ALL128 MalletStiffness host4 representatives `repr(n/127)` in the [1240938-byte INPUT composition](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/collision-unlaunched-stiffness128-input-eligibility.json),SHA256 `4712b845206b2c0481cc909bcb397d5c484872f6b6215c8eb72b4b9d3834ec47`, composed with the [5501-byte control qualification](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/collision-unlaunched-stiffness128-input-control-qualification.json),SHA256 `7746cc2bafadf23ae5df75c5592336a646ec95c716956e068a27665bac8f9243`. Sole-approved partial REPORT metadata explicitly maps all128 to unattemptedU/noPIDreceiptmetrics; this is a complete separate axis, not the failedVolume history or an automatic Volume-tail continuation. OriginalfailedVolume124U/threeunlaunchedVolume125–127U/124approvedVolume observations remain exact/asof, with no replay or guard relaxation.

All139 original decimal/f64/f32 words excepthost4, script bytes/history hashes/custody-context INPUT references remain exact. Host1Volume remains literal0.5, which is absent from the n/127grid; there is no inherited baseline output. Root reconstructed all128vectors/scripts/rationalbinary32INPUTlabels and soleREPORTunlaunched joins. Originalfourteen mutation checks verified changed metadata only, not rejection passes; their frozen bytes remain, while the external qualifier supplies14 actual rejection controls/fulloriginalINPUTbijection/NULLfuture/noPID/no failedVolume policy. Initial writer else126SyntaxError occurred atcompile before reads/artifact/nativecalls and was corrected before freezing; no original or INPUT change.

Mix authors ONE `batch-collision-unlaunched-stiffness-v1` after selectedCorpus13; Arrangement SOLEactual/sourcepeer afterElectric7/Root remains citation-only ALL newCollisionactual/source/code/raw/results. Existing139setter factory/rate44100/zeroInputflag0/warm11264 BEFOREqueuedOn4096/60/100 Off26146/60/0/render44100/block512/last68/destroy, C/TIME0/LIBM-unset/admittedFP model unchanged. CalcAret0/flag01/cxx0 and ALLotherguards remain; no opaque policy adopted, failedinputretried, newconstruction/tool/build/provider/patch/model/FPtreatment/calibration/metric/criterion or noise domain.

Prospective32128selectedexports13952CalcA56692736rawstereoB/expectedinitializerDATAempty/loggedworkseparate/nestedU.2GiBfull lifecycle+128MiBheadroomunreserved plans for128×8MiBmaxstdoutstderr/raw/futureownerreview allowances; parent/perchildfresh complete remainingraw/logmetadata/final268435456B/headroom guards, allnewsourceparentassemblercheckerfinalizer/scriptscontext precallbound, once-only/firstfaultstop/fullpartials/no retry. Future correctmetadatafinalizer is prebound, not retroactive oldKeyError/additivesealer repair. Notquota/concurrentwriter/escapedchild/withinchildovershoot guarantee. Olderret1diagnostic/skippedrawfsync/additivepostcapturepackaging/oldkind3failure/sourceFPABIproviderOSexec scopes remain. NewpriorsnativewaveformexpectationsportablecriteriaGradeNULL/appFalse/no IDs or grades/releases/closure/requiredU/productOPEN.


## Whole Stiffness128 actual adoption — 2026-10-22

[Arrangement's sole actual/source review](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/collision-unlaunched-stiffness-v1-review.json),13,128,862 bytes/SHA256 `c438ddd5dec075e868a00d35025ad6233a0d02838cedc351b9c73f7ec7ea2c7d`, approves all128 finite Stiffness observations/CLEAR/no findings or corrections. The [actual manifest](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/batch-collision-unlaunched-stiffness-v1/manifest.json),88,261 bytes/SHA256 `60294dfefa001e6880c5cdb4b6c1956908ae886d0ca56d7b3829109e16237fae`, records534payloads/65,487,417bytes/all535files0444/private root0700. Mix authored capture/control; Arrangement disclosed earlier INPUT/partial-review roles without authoring this capture. Root adopts by citation only; this filing reopens no actual/source/code/raw/numeric/provider proof.

Every host4 `repr(n/127)` representative, n0–127, retains all139 original decimal/f64/f32 words otherwise unchanged, Volume literal0.5 and warm11264 BEFORE queuedOn4096/Off26146 then render44100/block512/last68. All128 were previously unlaunched INPUT histories, not a retry of failed Volume124 or three unlaunched Volume125–127. The old R6 full256 AS-OF dispositions remain unchanged:124approved Volume, one failedU,131then-unlaunchedU. New Stiffness approval does not mean256successes, repair the failure, fabricate a baseline output or authorize any remaining Volume capture/guard relaxation.

All128 new outputs are finite/nonzero in both lanes/channel-word-unequal;102hashes/59usedLinux names are descriptive only. Accepted work is32,128selected exports/13,952CalcA/56,692,736raw stereo bytes/zero logged initializers; nested startup/provider calls stay unknown and Rate is opaque. Current129import declarations (96Linux/26trap/7data) and seven raw exports match the first current capture, without inventing a historical exact whitelist or continuous provider binding. Twenty-five independent negatives, three opaque-Rate positives and unsigned-word boundary controls pass. Original fourteen INPUT mutations established change only; the external qualifier supplies actual rejection checks for that metadata alone, preserving the original frozen authority.

2,304actual per-child18before/after pairs plus two source pairs are endpoints, not nativeFP/provider/ABI/OSexec/source-version continuity. Successful child raw/log/JSON FDfsync requests retain their branch scope; outer files have no explicit FDfsync and no directory/crash guarantee follows. The2GiB+128MiB unreserved full-lifecycle/resource contract is not a quota or protection from concurrent writers/escaped children/within-child overshoot. Older ret1/skippedfailedrawfsync/additive-not-prebound packaging/oldkind3 failure and default/FP/provider qualifications remain historical. No native quantizer/within-cell/physical/noise/productivity/publicARM/calibration law, portable criterion or grade is admitted; application proof false and all priors/native-waveform expectations/portable criteria/grades NULL. R7 owner adoption is separate and is not made by this actual filing; no IDs, release or closure are added here. Required U/product OPEN persists.


## Collision owner R7 Stiffness annex adoption — 2026-10-22

Root applied the exact74,566-byte target/SHA256 `222a13643a51042c7d16631922069c6a3e869d0a7a3b46968877334961fb0e66` approved by [Mix's sole new-owner wording/IDs/mapping/preservation review](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/collision-owner-r7-stiffness-cells-finite-v1-review.json),12,203,979 bytes/SHA256 `404de0e86f21a32ae434c9d67b8eb68536c114b928a7b2f9cdea3288bd122bfd`. The [owner manifest](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-collision-r7-stiffness-cells-finite-v1/manifest.json),2,215 bytes/SHA256 `29249dea83fc4252c312d2845a54e25ba78fc2b3745e88df2c53f145acea29a6`, records11payloads/11,580,215bytes/all12files0444/root0700/private0700ancestors. Its intendedRoot-peer labels are historical: Mix was the sole assigned reviewer, and Root applied only the approved embedded target/delta by citation. This filing reads REPORT metadata only, not R7 proposal payloads or actual/source/code/raw/numeric/provider proof.

128new DCL-951–1078 map the whole128fresh Stiffness histories, with no optional current256 overlay. R6's full256 AS-OF disposition view remains exact:124approved Volume, failedVolume124U and131then-unlaunchedU. The new128Stiffness observations neither rewrite that history nor replay failedVolume124 or the three Volume125–127 inputs; those four remain U. No complete256-success, baseline output/PID/metric/criterion transfer, guard relaxation or opaque-return policy follows.

Annex/revision only preserves all18whole requirements/950oldIDs62rows/R2–R6objects/eight relations/criteriaU/history/releases2cases2evaluations8inventory/fullreverse. Twenty-six owned and twenty independent owner negatives pass. REQ008 is context only, without new quantizer/within-cell/physical/noise/publicARM/calibration law. Prior kind3ret1/84-not85/input-only baseline and failed-Mallet/additive-not-prebound packaging/skippedfailedrawfsync/sourceFPproviderOSexec/resource qualifications retain their original scopes. Fresh priors/native-waveform expectations/portable criteria/grades NULL/application false;1,078 navigation IDs are not passes or a product denominator. No release, site credit or closure; required U remains OPEN.

### Complete unattempted Volume suffix selected — 2026-10-23

Select **batch-collision-unlaunched-volume-tail-v1**, Mix capture/control author/Arrangement sole NEW actual-source-code-raw peer after final seal/Root citation-only before all new payloads. The exact INPUT/disposition/model/runtime authority is the [sole-approved original partial REPORT](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/collision-mallet-controller-cells-v1-review.json),24096318bytes/SHA256 `9968349497c41a6f1ba9c7d20a1e5c150088abf4fc3949890497b75b5d12d814`, used only as approved INPUT/shared-model metadata, without oldsource/raw/numeric/provider proof replay. Bind **all three** original never-launched Volume125–127 histories/aliases/full139ordered decimal/f64/f32words/scripts/contexts unchanged. Exclude all launched Volume0–124, failedVolume124 and all128Stiffness observations. Retain original warm11264 BEFORE queuedOn4096/Off26146/render44100block512last68 and exact other defaults from approved metadata, not guessed reconstruction.

STRICT CalcAret0/flag0or1/everyotherprotocol/frame/input/output/unsignedfinite/trap/custody/status/timeout/resource/cleanup guard remains unchanged; D08/D09/design13 opaque policies do not transfer. Any whole-class grammar/context gap prevents calls; no arbitrary subset/patch. All new controls/parent/collector/checker/assembler/finalizer/catalog/context/scripts must be fully inert-read and pre-call-bound. Capture each once sequentially; firstfault stops later children, retaining accepted/failed/unattempted distinctly without retry or guard relaxation. Original helper/module/compiler/provider/model/build/FP/construction changes are excluded. Explicit supplied environment/default premises do not establish historical equivalence/actualFP/provider/OSexec/source-build/public behavior.

Retain full old512MiBlifecycle+128MiBheadroom=671088640byte floor plus268435456concurrent allowance and any larger complete remainingraw/worst8MiBstdoutstderr/futuremetadata/finalreview-owner allowance before parent and each child. No evidence move/delete/split/reduced floor. Estimates are unreserved, with within-child/concurrent-writer/escaped-child limits explicit. Preserve all raw/log/status/argv/env/PIDUTC/custody/resource/fsync/cleanup and original R6ASOF/failedret1/skippedfailedrawfsync/oldfinalizerfieldmismatch/additivepostcapture qualification. Author bookkeeping is metadata-only; one final sole actual/source review, no added readiness gate. No new case credit before approval/owneradoption; all new priors/expectations/comparators/gradesNULL/applicationfalse. RequiredU/productOPEN/O0 unchanged.

#### Complete Volume suffix pre-call binding — 2026-10-23

Author reports all new methods/controls/parent/context and exactthree scripts frozen before originals in the [pre-call manifest](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/batch-collision-unlaunched-volume-tail-v1/pre-call-manifest.json),3844bytes/SHA256 `83686ebfb17e6462bafabd74278c89900ac8e4f01d2017c38f42f8ddeb9a2dd5`. Actual packet basename supersedes the earlier descriptive selected basename; same new scope/store, no evidence relocation/refreeze/gate. Exact MCI-001-125/126/127/fixedStiffness0.5/139words/source-script contexts derive from approved INPUT metadata. Planned totals327CalcA/753directexports/1328736rawbytes are not yet observed work. Supplied C/TIME0/LIBM-unset/unchanged149624byte model context and historical-source/provider/FP limits remain explicit. Author’s own prior recorder/control code was used only as inert authoring pattern; no old capture/check/raw proof rerun or original DSP/helper/source follow. Root remains citation-only; one sole final actual/source review follows once-only strict capture, no new gate or case credit here.

#### Volume suffix author partial; sole actual review pending — 2026-10-23

Author reports the new once-only batch stopped at its first child MCI-001-125 with a frozen protocol AssertionError: zero accepted protocols,126/127 never launched, no retry/guard repair. [Final partial manifest](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/batch-collision-unlaunched-volume-tail-v1/manifest.json),5487bytes/SHA256 `0f0d3dbc0eff8b9d7770489f3f8a244432a705a7230de9b4a420247abb3fbbe4`, seals32payloads811665bytes/all33files0444/private0700.442912diagnostic raw bytes,29per-child identitypairs+oneREPORTpair, parent/precall/outertool receipts and metadata-only partial bookkeeping are retained. These are author metadata pending Arrangement’s sole full-source/actual review, not protocol acceptance, literal-return adjudication, numeric proof, criteria or case credit. Root remains citation-only. OldfailedVolume124/allolder Volume/Stiffness/strictguards/ASOF unchanged; no automatic continuation, opaque-policy extension or newguard selected. CurrentR7/1078nav/23138draft additions/requiredU/productOPEN/O0 unchanged.

## Complete Volume suffix sole partial review adopted — 2026-10-23

[Arrangement’s sole actual/source review](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/collision-unlaunched-volume-tail-v1-review.json),610749bytes/SHA256 `27d6230039bf224d19b4f5878fffa35cfee92421bec2d50b45849f819e0051d7`, approves retained failure/disposition/custody classification only, CLEAR/no blocking findings/corrections. **Zero approved native observations/new IDs.** MCI-001-125 is guardFAIL/U;126/127 remain unlaunchedU. Oldfailed124/Volume0–123/Stiffness128 and fullR6ASOF remain immutable. No retry, automatic continuation, guard/policy extension or owner admission is selected.

The sole review checks all three INPUT/disposition joins, complete new code, failed protocol and diagnostic raw. The once-launched child3810386 exited0/empty stderr/full442912byte raw; strict rejection is renderblock9/start4096 with literalret1/flag1, the other108CalcAreturns literal0. This is the configured guard’s rejection, not evidence of native ABI/domain/error/cause/activity meaning.55364frames include11264warm+44100render; diagnostic raw finite/unequal/nonzero55364frames per lane is not an accepted metric/expectation/pass. The failed branch skipped raw-FDfsync; diagnostic shape does not repair that durability gap.

Full671088640floor+268435456concurrent+largerremaining requirements, oneREPORTpair/29actualperchildidentitypairs, all33frozenfiles and ownedpartialcheck/11independentcontrols passed. Mutable reviewer ordinal-rebase/whitespace mistakes were corrected only in reviewer code and retained; no frozen/native/input repair. Nonblocking **CVT-RV-Q01** records leaf/attemptdirectories0775 behind private0700root/files0444; this qualifies privacy without silently changing modes. Fullall3catalog/dispositions/oldASOF/resource/source/FP/provider/OSexec/parent/crash limits remain in soleREPORT. Root adopts scalar summary/pins only, without any second raw/log/protocol/numeric/source proof review. CurrentR7/1078nav/23138draft additions/releases/requiredU/productOPEN/O0 unchanged.
