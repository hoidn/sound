# Mix graph, mixer gains and automation playback, release 1

Target: Ableton Live 12 Suite 12.4.3 (2026-07-07_e3d8be4d07), macOS, Apple
silicon (arm64). Features: FEAT-AUDIO with FEAT-AUTOMATION. Parent
specification identity: SPEC-MIX-GRAPH revision 1. Release: mix-graph-v1.
Only the clauses explicitly included below are in scope. No other clause of a
listed requirement is implicitly approved. This document is self-contained.

**Status: reviewed local release.** A separate review approved the clauses
below with the narrowing recorded in [the review disposition](REVIEW.md).
Implementation requires a fresh, restricted implementation workspace.

## What the contract means

In a Live Set, each audio, MIDI and return track passes its signal through its
device chain and then its mixer, and the main track sums what reaches it. The
project renders a Live Set's main output offline. For that render, this
contract describes:

- the order in which a track's signal passes its device chain and its mixer,
  where sends tap the signal, and how return tracks and the main track sum
  their inputs;
- how the volume, the pan law, the pan mode, pre- and post-fader sends, the
  track switch and the solo state combine into the gains applied to the
  signal;
- how and when gains change: per sample, through linear ramps, and the fade
  length of switches;
- how an automation envelope's events become the values it plays: the point
  list, curved segments, the value between points, and how often an automated
  value moves along its segment.

It does not describe which envelope drives a parameter during playback, the
units of automated values, solo as stored in a Live Set, the gain and activity
of sends above their minimum, crossfade assignments A and B, clip playback,
devices, recording, editing, or real-time behavior.

### Expectation provenance

Every case carries one of these labels:

- **Extracted execution.** The original program's own x86_64 code computed the
  expected values on the case's inputs. It ran in isolation on a Linux x86_64
  host, with the host's C library in place of the macOS system libraries. It is
  not a run of the application.
- **Static-derived.** Derived from evidence reviewed before sanitization.
  Three computation cases combine the two labels: the points and values are
  extracted execution, and the choice of segment is static-derived.
- **Composed render (spec conformance).** A render expectation composed from
  the rules of this contract and from gains computed by extracted execution.
  No render of the original application exists, and none will be made, to
  compare against. A candidate that meets these cases conforms to this
  contract. That is spec conformance, not measured compatibility with the
  original application.

None of these is an observed run of the original application. No
compatibility result is established.

### Stated assumptions

Some derived steps rest on assumptions that were not traced to the end:

1. The macOS arm64 build computes the extracted-execution values as the x86_64
   build does, within the stated tolerances. The pan law uses the platform's
   cosine, which may differ in the last binary32 digit.
2. A Live Set in which no mixer stores `SoloSink` as `true` has no soloed
   track.

### Render convention

A render starts from a settled state
([REQ-011](#req-mix-graph-011--partial-render-start)). This is a convention
the project decided for its offline render (project decision ADR 0004). It
states no behavior of the original application.

## Terms and preconditions

- Signals have two channels, L and R, one binary32 value per channel per
  sample. **binary32** and **binary64** are IEEE 754 single and double
  precision.
- A **matrix** is four gains (L→L, L→R, R→L, R→R). Applied to an input (L, R)
  it gives output L = L→L·L + R→L·R and output R = L→R·L + R→R·R.
  **I** is the identity matrix (1, 0, 0, 1). Expected matrices list the four
  gains in this order.
- A **ramp** to a target over n samples changes a value linearly, sample by
  sample ([REQ-009](#req-mix-graph-009--when-gains-change)). The **fade
  length** is 75 samples ([REQ-010](#req-mix-graph-010--partial-fade-lengths)).
- The **silence limit** is 0.0003199999919, the binary32 value nearest to
  0.00032.
- The **default automation settings** are the application's defaults for an
  automated value: a value step q of one thousandth of the parameter's value
  range, a minimum ramp of 200 samples and no smoothing. REQ-013's Float value
  and REQ-014 are stated for these settings. Which parameters use them, and so
  the value step of any parameter, is not released.
- The **stored minimum** of volumes and sends is 0.0003162277571 (−70 dB), and
  the stored maximum of volumes is 1.99526238 (+6 dB). Both are the binary32
  values of these texts.
- **Live Set documents.** A fixture is the decoded XML of a Live Set:
  well-formed XML 1.0 in UTF-8 whose root element is `Ableton` with exactly
  the attributes `MajorVersion="5"`, `MinorVersion="12.0_12402"` and
  `SchemaChangeCount="1"`, and whose first child is `LiveSet`. Every fixture is
  a complete minimal Live Set that opens. The compressed file container is
  outside this release. Paths are relative to `/Ableton/LiveSet`.
- A number text is read as the binary32 number nearest to its decimal value.
  Every number text in the fixtures is a plain decimal.

### Document values used by the render cases

Each track's mixer is `<track>/DeviceChain/Mixer`. The tracks are the items of
`Tracks` and the main track `MainTrack`.

| Value | Text read in the mixer | Meaning in this contract |
| --- | --- | --- |
| Volume | `Volume/Manual/@Value` | stored volume g, a linear gain (1 is 0 dB) |
| Pan | `Pan/Manual/@Value` | pan p, −1 (left) to 1 (right) |
| Split pans | `SplitStereoPanL/Manual/@Value`, `SplitStereoPanR/Manual/@Value` | sL and sR, −1 to 1 |
| Pan mode | `PanMode/@Value` | 0 Stereo, 1 Split Stereo |
| Track switch | `Speaker/Manual/@Value` | `true` on, `false` off |
| Solo | `SoloSink/@Value` | `false` in every fixture |
| Crossfade assignment | `CrossFadeState/Manual/@Value` | `1` (None) in every fixture |
| Send k | `Sends/TrackSendHolder[k]/Send/Manual/@Value` | stored send value, a linear gain |
| Pre or post | `LiveSet/SendsPre/SendPreBool[k]/@Value` | `true` pre-fader, `false` post-fader |
| Output | `<track>/DeviceChain/AudioOutputRouting/Target/@Value` | `AudioOut/Main` on every audio and return track |

Here `[k]` is the k-th item in document order, counted from 0.

## Selected requirement clauses

### REQ-MIX-GRAPH-001 — partial: the render graph

- Each audio, MIDI and return track and the main track has exactly one mixer
  stage, its mixer. An audio or MIDI track's signal passes from its source
  through the devices of its device chain, in device order, to its mixer
  stage. The mixer stage has one main output and one send output per return
  track.
- Send k of a track, its k-th `TrackSendHolder`, feeds the k-th return track:
  the k-th `ReturnTrack` item of `Tracks` in document order. The k-th
  `SendPreBool` of `LiveSet/SendsPre` belongs to the same return.
  Expectations exist only for sets with at most 12 return tracks.
- In scope, every audio, MIDI and return track outputs to the main track
  (`AudioOutputRouting/Target` is `AudioOut/Main`). The render output is the
  main track's main output
  ([REQ-006](#req-mix-graph-006--partial-summing-and-the-main-output)),
  whatever the main track's own output target.
- Expectations exist only for sets in which every mixer of an audio, MIDI or
  return track holds exactly one `TrackSendHolder` per return track and
  `SendsPre` holds exactly one `SendPreBool` per return track. Every render
  case has one return track.

### REQ-MIX-GRAPH-002 — order inside the mixer stage

- Let x be the device chain's output, two channels, sample by sample. The
  mixer stage forms the main output y = M_main·x and, for each send k, the send
  output s_k = M_k·x. Each sample uses the matrices current at that sample
  ([REQ-009](#req-mix-graph-009--when-gains-change)).
- No other gain acts between the device chain and these products. The volume,
  the pan law and the track switch act through M_main
  ([REQ-003](#req-mix-graph-003--partial-volume-gain) and
  [REQ-004](#req-mix-graph-004--partial-main-matrix-and-pan-law)). Each send
  acts through its own M_k
  ([REQ-005](#req-mix-graph-005--partial-sends-pre-and-post-fader)).
- A return track's x is the sum of the send outputs addressed to it, after its
  own device chain. The main track's x is the sum of the main outputs of all
  tracks and return tracks routed to it, after its own device chain.

### REQ-MIX-GRAPH-003 — partial: volume gain

Applies to a track or main track whose crossfade assignment is None
(`CrossFadeState/Manual` `1`) and whose volume no envelope drives.

- For a stored volume g from the stored minimum to the stored maximum, the
  volume gain is v = g, except that a v at or below the silence limit is
  replaced by exactly 0.
- Consequences: the stored minimum is silent, and so is any stored volume up
  to the silence limit. A stored volume above the limit is audible.
- v equals g exactly for 0.0003162277571, 0.5011872053, 1 and 1.99526238
  (extracted execution). For other stored values, v is not established to be
  bit-exact; the render tolerance covers any difference in the last binary32
  digit.
- The main track's volume follows the same rule. Every fixture stores the main
  track's crossfade assignment as None.

### REQ-MIX-GRAPH-004 — partial: main matrix and pan law

- M_main = m·P(w, p, sL, sR, v). Here m is the track's main gate
  ([REQ-007](#req-mix-graph-007--track-switch) and
  [REQ-008](#req-mix-graph-008--partial-gates-by-solo-category)), v the volume
  gain of REQ-003, and P the pan-law matrix below. The product m·P is
  extracted execution.
- **Pan law.** With θ(u) = (u + 1)·π/4, p the pan, sL and sR the split pans
  and w the split amount:
  - L→L = v·(w·cos θ(sL) + (1 − w)·max(10⁻⁵, √2·cos θ(p)))
  - L→R = v·w·sin θ(sL)
  - R→L = v·w·cos θ(sR)
  - R→R = v·(w·sin θ(sR) + (1 − w)·max(10⁻⁵, √2·sin θ(p)))

  It is evaluated in binary64, and each gain is rounded to binary32. Gains that
  are mathematically 0 may come out below 10⁻¹⁶. Examples with v = 1:
  Stereo (w = 0), pan 0: I; pan −1: (1.4142135, 0, 0, 0.00001); pan −0.5:
  (1.306563, 0, 0, 0.5411961). Split Stereo (w = 1) with split pans (−1, 1):
  I; with split pans (0, 0): 0.70710677 for all four gains. The formula is
  static-derived; extracted execution of the original code gave exactly the
  example gains.
- The split amount w is the stored `PanMode` code: 0 for Stereo, 1 for Split
  Stereo. A change of `PanMode` ramps w linearly over the fade length.

### REQ-MIX-GRAPH-005 — partial: sends, pre and post fader

- For a track outside any group, send k's matrix is
  M_k = g·e·a·(q·P + (1 − q)·I), where:
  - g is the send gain;
  - e is the track's send gate (REQ-007, 008);
  - a is 1 when the send is active and 0 when it is not;
  - q is the post amount: 1 post-fader, 0 pre-fader, between the two during a
    fade;
  - P is the track's pan-law matrix with its volume gain (REQ-004), without m.
- Consequences:
  - A pre-fader send carries g·x: no pan law, no volume and no silence limit.
  - A post-fader send carries g·P·x.
  - Neither depends on the main gate m. The send gate e alone switches all
    sends of a track.
- q is 0 (pre-fader) when the k-th `SendPreBool` has `Value="true"`, and 1
  (post-fader) when it has `Value="false"`. One setting applies to send k of
  every track. A change ramps q linearly over the fade length.
- A send whose stored value is exactly the stored minimum, 0.0003162277571,
  contributes nothing (g = 0), whatever a is.
- s_k goes to the input of the k-th return track.
- Not released: the send gain g of any other stored send value, and which
  sends are active.

### REQ-MIX-GRAPH-006 — partial: summing and the main output

- Every destination input, at every sample, is the sum of the outputs
  addressed to it: send outputs into a return track, and main outputs of
  tracks and return tracks into the main track. The sum is formed once per
  sample, before the destination's device chain runs.
- Send outputs add into the destination in binary64, and the destination
  converts the total to binary32. Main outputs are binary32. The order of the
  main sum is not released; render cases compare within a tolerance.
- A return track's own mixer stage (REQ-002 to 005) shapes its output to the
  main track. Its sends to return tracks follow REQ-005; at the stored minimum
  they contribute nothing.
- The main track has no sends. Its main output y is the render output, one
  binary32 value per channel per sample.

### REQ-MIX-GRAPH-007 — track switch

- With no track soloed, a track whose `Speaker/Manual` is `false` has main gate
  m = 0 and send gate e = 0. It contributes nothing to the main track and
  nothing to any return track, pre- or post-fader. With `true`, both gates are
  1. This applies to audio, MIDI and return tracks.
- A change of the track switch ramps m and e linearly over the fade length,
  starting at the change's sample.
- A main track whose track switch is off has no expectation.

### REQ-MIX-GRAPH-008 — partial: gates by solo category

- Each track is in one solo category. Its main gate m and send gate e follow
  from the category and from the track switch value s, which is 1 for on and 0
  for off (extracted execution):

  | Category | m | e |
  | --- | --- | --- |
  | unaffected, following a soloed track, cue solo | s | s |
  | soloed | 1 | 1 |
  | muted by solo | 0 | 0 |
  | indirectly muted by solo | s | 0 |
  | muted by a return-track solo | 0 | s |

  A soloed track therefore plays even when its track switch is off. The
  categories are labels of this rule; they imply no stored value and no
  required internal state.
- Which category a track is in is not released, with one exception: in a Live
  Set in which no mixer stores `SoloSink` as `true`, no track is soloed and
  every track is unaffected (stated assumption 2).
- A change of category ramps m and e over the fade length. The cue output is
  outside this release.

### REQ-MIX-GRAPH-009 — when gains change

- Gains are applied per sample. There is no block-wise gain, and the buffer
  size has no effect on gains. A gain changes only at a scheduled sample,
  through a ramp that carries a target and a length n in samples:
  - with n > 0 the gain moves linearly from its current value to the target
    over n samples;
  - with n = 0, or a step below 10⁻¹² per sample in magnitude, it takes the
    target at once;
  - at a ramp's end the gain has exactly the target (switch fades), or the next
    ramp starts (automation, REQ-014).
- Within a ramp of n samples, the step d is (target − current)/n rounded to
  binary32, and the gain accumulates in binary32:
  - a main-matrix gain used at the k-th sample of the ramp (k = 1 … n) is
    current + k·d, so the first sample already moves;
  - a send-matrix gain used at the k-th sample is current + (k − 1)·d.
- When an input of the pan law changes (w, p, sL, sR or v), each matrix gain
  ramps to its value at the end of the shortest running input ramp. The pan law
  is evaluated there, at the inputs' values at that sample. Between such
  evaluations a gain is linear in time, so the pan law is applied piecewise
  linearly. The volume gain is evaluated in the same way, at each ramp end of
  its input.
- A control value below 10⁻¹² in magnitude counts as 0.

### REQ-MIX-GRAPH-010 — partial: fade lengths

- The fade length is 75 samples, the same number of samples at every sample
  rate, with the application's default settings.
- It applies to the main gate m, the send gate e, the post amount q and the
  split amount w.
- Values that do not change during a render produce no ramp after its start
  (REQ-011).

### REQ-MIX-GRAPH-011 — partial: render start

- **Render convention.** At the first rendered sample, every gain has its
  settled value for the opened set: every main gate, send gate, post amount and
  split amount already has its target, and no ramp started by opening the set
  is still running.
- This is a convention of the project's offline render. What the original
  application does in the first samples after a set is opened is not released.

### REQ-MIX-GRAPH-013 — partial: envelope playback value

This clause defines the value an envelope plays at a given envelope time, as a
computation. Not released here: which envelope drives a parameter and when, the
mapping from song position to envelope time and the samples at which point
times take effect, the automation settings of any parameter, and the units in
which the values of any parameter's envelope are played. Values below are in
the envelope's own value units.

- **Point list.** The events of the envelope, in document order, give the
  points: times in binary64 beats, values in binary32.
  - In a Float envelope, the first event's time is replaced by −10,000,000
    beats, whatever it was. In documents the first event is the leading event
    at −63,072,000 beats.
  - A segment that starts at an event with a curve becomes 16 straight pieces.
    The curve controls are the event's `CurveControl1X` (x1),
    `CurveControl1Y` (y1), `CurveControl2X` (x2) and `CurveControl2Y` (y2); a
    missing control is 0.5, and four controls of 0.5 mean no curve. With
    Δt = tb − ta, Δv = vb − va, and the cubic Bézier curve
    P0 = (ta, va), P1 = (ta + x1·Δt, va + y1·Δv), P2 = (ta + x2·Δt, va + y2·Δv),
    P3 = (tb, vb), the 15 interior points lie at the Bézier parameter
    s = 1/16, 2/16, …, 15/16. They are computed in binary64, with times kept in
    binary64 and values rounded to binary32.
- **Lookup.** At envelope time t (in beats, first rounded to the nearest
  multiple of 1/3,843,840 beat, halves away from zero), the current segment
  starts at the last point whose time is at or before t. At two points with
  the same time, the later one applies.
- **Float value**, with the default automation settings. In a segment from
  (ta, va) to (tb, vb), with S samples per beat (sample rate × 60 / tempo):
  - slope = (vb − va, computed in binary32) / ((tb − ta)·S), in binary64, per
    sample;
  - value = va + max(0, (t − ta)·S)·slope, kept within the range of va and vb;
  - va = vb gives a constant segment;
  - after the last point the value holds;
  - other automation settings have no expectation.
- **Bool and Enum values.** At an envelope time at or after the first event's
  time, the value of the current point, without interpolation.

### REQ-MIX-GRAPH-014 — partial: how often an automated value moves

- With the default automation settings, while the transport plays, a Float
  value driven by an envelope moves along its current segment (REQ-013)
  through ramps of L samples. With slope s per sample and value step q, let
  r = q/|s| in binary64. Then
  L = max(200, min(65,536, trunc(r))). A flat segment (s = 0) sends no ramp.
  Expectations exist only for r below 2³¹.
- Each ramp moves the value by L·s. The last ramp before a point is shortened
  to the whole number of samples that ends on the segment line. The value then
  holds until the point's sample, so it deviates from the line by at most q. A
  new segment starts at each point's sample.
- With the transport stopped, a value change takes effect at once (n = 0).
- q is an input of this rule: one thousandth of the value range of the
  parameter the envelope drives. Which parameters use the default automation
  settings, and so the q of any parameter, is not released. Volume and send
  automation are not released.

## Acceptance representation and comparison

[cases.json](cases.json) lists 28 cases: 17 computation cases and 11 render
cases. Each case lists the requirements it exercises and carries an
`expectation_provenance` label
([provenance](#expectation-provenance)). This is a **project comparison
representation**, not an API claimed to exist in the original application and
not a required design. A candidate adapter may translate its own results into
these labels. Cancellation and teardown kinds are omitted: a render has no
cancellable step in this scope. Malformed documents have no case here.

### Computation cases

A computation case has no fixture (`input` is null). Its `computation` names
one rule of this contract, and its `evaluations` list `arguments` and the
`expected` result. A candidate adapter evaluates the rule on the arguments.
Numbers compare within the case's absolute `tolerance`; integers, Booleans and
labels compare exactly. Expected numbers are binary32 or binary64 values
written as JSON numbers.

| Computation | Arguments | Result | Rule |
| --- | --- | --- | --- |
| `send-matrix` | `gain` g, `send_gate` e, `active` a, `post` q, `pan_matrix` P | `matrix` M_k | REQ-005 |
| `main-matrix` | `main_gate` m, `pan_matrix` P | `matrix` m·P | REQ-004 |
| `gates` | `solo_category` (`unaffected`, `soloed`, `following`, `muted`, `indirectly-muted`, `return-solo-muted`, `cue`), `track_switch` (Boolean) | `main_gate`, `send_gate` | REQ-007, 008 |
| `fade-length` | none | `samples` | REQ-010 |
| `ramp-advance` | `start`, `target`, `length` n, `advances` | `values`: the ramp's value after each one-sample advance, 1 to `advances`; the value after k advances is the main-matrix gain at the k-th sample | REQ-009 |
| `ramp-start` | `start`, `target`, `length` | `value` right after the ramp is set, before any advance | REQ-009 |
| `pan-ramp` | `initial` pan-law inputs (`split_amount`, `pan`, `split_l`, `split_r`, `volume_gain`) and `changes`, each a ramp of one input starting at a `sample` | `after_changes`: after each change, the `matrix_target` to which every pan-law gain ramps, and the ramp `length` in samples | REQ-004, 009 |
| `polyline` | segment `start` and `end` points (time, value) and `controls` (x1, y1, x2, y2) | `points`: the 15 interior points (time, value) | REQ-013 |
| `playback-value` | `events` as (time, value) or (time, value, controls), `samples_per_beat`, `times` (envelope times) | `values` | REQ-013 |
| `discrete-value` | `events` as (time, value) with Boolean or integer values, `times` | `values` | REQ-013 |
| `ramp-length` | `step` q, `segment` (ta, va, tb, vb), `samples_per_beat`, `transport` (`playing` or `stopped`) | `length` L in samples; 0 means no ramp | REQ-014 |

Computation cases grade the rules on stated inputs. Some of these inputs, such
as send gains above the minimum, solo categories other than unaffected, ramps
and automation, do not occur in the render cases. The conditions under which a
Live Set produces them are not released.

### Render cases

A render case has a fixture Live Set (`input`) and a `render` record:

- `signals` maps a track name to a WAV file of the package. `A` is the first
  `AudioTrack` of the fixture (`Id="1"`), and `B` the second (`Id="2"`). The
  return track is named `R`.
- The adapter opens the fixture and places each signal at the named track's
  mixer-stage input, as that track's device-chain output; every fixture's
  device chains are empty. A track without a signal has no input. The fixtures
  hold no clips, so clip playback plays no part.
- It renders `frames` sample frames at `sample_rate` 44,100 Hz, with the
  transport playing from beat 0, starting from the settled state of REQ-011.
  The n-th main output frame corresponds to the n-th input frame.

`expected.main` gives each main output channel as coefficients of the input
channels, for example `{"L": {"A.L": 1.0}, "R": {"A.R": 1.0}}`. An empty map
means silence. For every frame n and channel c, the candidate's main output
y_c[n] must lie within `tolerance_factor` × X of the sum of each coefficient
times its input channel's sample n. `tolerance_factor` is 10⁻⁵, and X is the
largest magnitude of any input sample of the case (0.5 for both signals). The
tolerance absorbs the unreleased order of the main sum and differences in the
last binary32 digit. It does not separate a gain of 10⁻⁵ from silence.

## Reference comparison

No reference observation exists for any case. Computation-case expectations
come from extracted execution of the original code or from static reading. For
the render cases, no render of the original application exists or is planned,
so they remain spec conformance. Candidate-only success proves agreement with
this contract, not with the running original. Record candidate results with
the exact package and candidate hashes.

## Exclusions and deferred obligations

Requirements not released:

- **REQ-MIX-GRAPH-012** (which automation drives a parameter): the drive state
  after opening a set and after a session launch rests on an untraced step, and
  the time base of clip envelopes is unknown.
- **REQ-MIX-GRAPH-015** (units of automated values): whether volume and send
  envelope values are played as fader positions rests on an untraced step.
- **REQ-MIX-GRAPH-016** (automated against manual values): its only content is
  the drive state of REQ-012.

Inputs with **no expectation** in this release:

- group tracks and tracks inside a group; audio, MIDI or return tracks whose
  output is not `AudioOut/Main`; input monitoring; a track delay other than 0;
  frozen tracks;
- racks and devices that report latency; in render cases, any device or clip;
- more than 12 return tracks; send holders or `SendPreBool` items other than
  exactly one per return track; render sets with other than one return track;
- a crossfade assignment other than None on any track; a main track with its
  track switch off;
- any mixer that stores `SoloSink` as `true`; solo of the main or cue track;
- in render cases, a send stored above its minimum whose output can reach the
  main track, that is, its track's send gate is not 0 and its return track's
  main gate is not 0;
  any send with `EnabledByUser` `false` stored above its minimum;
- stored volumes outside the stored minimum to the stored maximum; sends
  outside 0.0003162277571 to 1; pans and split pans outside −1 to 1; `PanMode`
  other than 0 and 1;
- in render cases, automation envelopes on any mixer or device parameter, other
  than the main track's one-event tempo and time-signature envelopes whose
  single event equals the stored value (every fixture holds these two); clip
  envelopes;
- ramp-length inputs whose r is 2³¹ or more.

Excluded behavior:

- which envelope drives a parameter and when; the mapping from song position to
  envelope time and the samples at which point times take effect; automated
  against manual values;
- which parameters use the default automation settings, and the value step of
  any parameter;
- the units of automated values, including volume and send automation;
- the send gain of sends stored above their minimum, and which sends are
  active;
- which solo category a track is in when a Live Set stores a solo, and the cue
  output;
- the crossfade factor, and the ramp of a crossfade-assignment change;
- clip playback, instruments and device processing;
- recording, editing, undo, manual changes during a render, automation override
  and re-enable;
- real-time scheduling and latency, the audio-device stage after the main track,
  and what the original does in the first samples after a set is opened;
- a non-default fade-length setting, and the order of the main sum.

Draft cases not released: the render cases with a send above its minimum
reaching a playing return track, with a stored solo, with crossfade assignment
A, with out-of-range stored volumes, or with an envelope driving a parameter;
the draft's unresolved cases; and a draft case with no observable in this
release. Three draft render cases on automation are
carried as the computation cases MIX-GRAPH-013 to 015, without their claim
about which envelope drives a parameter.

## Fixture provenance

All 11 Live Set fixtures were authored for this release from one template,
built on the project's minimal Live Set rules. The template holds two audio
tracks `A` (`Id="1"`) and `B` (`Id="2"`) and a return track `R` (`Id="3"`), all
output to `AudioOut/Main`, with empty device chains and two empty session clip
lists; the main track, with tempo 120, time signature 4/4 and their one-event
envelopes; the cue track; one `SendPreBool` (`false`); two scenes; the
transport; and the global settings. Template mixer values: volumes `1`, pans
`0`, split pans `-1` and `1`, pan mode `0`, track switches `true`, `SoloSink`
`false`, crossfade assignment `1`, crossfader `0`, sends `0.0003162277571`
with `EnabledByUser` `true` on A and B and `false` on R's own send. Each
fixture is the template with the change its case's purpose states. Every
fixture was checked against the project's structure rules for Live Sets: it has
no element outside the format's schema and nothing that would stop it from
opening. Text is ASCII, tab-indented, with line-feed line endings and a final
newline.

The two signals are generated 16-bit PCM WAV files, two channels, 44,100 Hz,
64 frames. Sample n (0 to 63) is the integer below divided by 32,768:

| File | L | R |
| --- | --- | --- |
| `fixtures/signals/x-a.wav` | 1024·((n mod 32) − 16) | 2048·\|(n mod 16) − 8\| − 8192 |
| `fixtures/signals/x-b.wav` | 12000 when n mod 8 < 4, otherwise −12000 | 512·((5n mod 64) − 32) |

No fixture contains shipped file content, audio, program code or assets.
Expected results are newly authored behavioral data, labeled per case. No
public source or dependency is approved or included. Review status is recorded
in [the manifest](manifest.json) and [the review disposition](REVIEW.md).
