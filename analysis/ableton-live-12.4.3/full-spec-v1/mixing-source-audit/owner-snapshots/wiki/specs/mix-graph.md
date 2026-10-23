---
id: SPEC-MIX-GRAPH
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 2
target: Ableton Live 12 Suite 12.4.3 / macOS
---

# Mix graph and automation in playback

## Scope

Feature FEAT-AUDIO, with FEAT-AUTOMATION, in the [feature map](feature-map.md). Target T1
([ADR 0004](../decisions/adr-0004-target-scope-t1.md)): render the main output of a Live Set
offline from a script of transport and launch actions. This draft specifies how the
per-track signals become that output:

- the order in which a track's signal passes its device chain and its mixer stage;
- where sends tap, and how `LiveSet/SendsPre` chooses pre- or post-fader;
- how return tracks and the main track sum their inputs;
- how the gains already defined in [SPEC-MIXER-VALUES](mixer-values.md) r3 combine with
  each other and with the on switches:
  - volume curve, crossfade factor and silence floor;
  - pan law;
  - send curve;
- mute (`Speaker`) and solo (`SoloSink`, `LiveSet/SoloInPlace`, `LiveSet/SoloOrPflSavedValue`);
- when gains change: per sample, through linear ramps of stated sample lengths;
- automation during playback:
  - which envelope drives a parameter;
  - how the song position selects its value;
  - how often values are applied;
  - in which units.

**Inputs and outputs.**

- **Input.** Each audio or MIDI track's source signal is specified elsewhere: clip playback
  and instruments in SPEC-PLAYBACK-CORE (T1.3), devices in the device specs (T1.2).
- **Output.** The main track's output signal.

Every requirement is a **proposed contract**. Its support is one of these, or it is
explicitly unknown:

- a static derivation from the 12.4.3 program;
- extracted execution of the shipped x86_64 code;
- shipped bytes.

No original-versus-candidate render exists or will exist
([ADR 0003](../decisions/adr-0003-no-reference-execution.md)). Whole-mix results are spec
conformance, not measured compatibility (ADR 0004). Target: documents with
`MinorVersion="12.0_12402"`. Document examples are fragments of the decoded XML.

**Excluded input.** These have no requirement and no case:

- **Tracks and routing:**
  - group tracks and tracks inside a group;
  - any `AudioOutputRouting` target other than `AudioOut/Main` for an audio, MIDI or return
    track;
  - input monitoring;
  - a non-zero `TrackDelay`;
  - freeze.
- **Devices:** racks; devices that report latency.
- **Outputs:** the cue (`PreHearTrack`) output and its sharing of physical channels.
- **Returns:** more than 12 return tracks.
- **Automation:** clip envelopes of session clips (their time base is unknown, REQ-012).

**Excluded behavior.**

- Recording, editing commands, undo, manual changes during a render, automation override and
  re-enable.
- Real-time scheduling and latency, and the audio-device stage after the main track.

## Evidence labels

| Label | Meaning |
| --- | --- |
| D | Documented in shipped bytes: the 12.4.3 schema or the shipped Live Sets |
| S | Static derivation from the 12.4.3 program; not an observed run. An assumption is named beside the clause when one is needed |
| S-cond | Static derivation that holds under one of the Q-019 conditions A3 to A5 below, which a static trace could settle. An S clause may also name an assumption (A1, A2, A6 to A8) |
| X | Extracted execution: the shipped x86_64 function computed the stated values in the harness of [ADR 0003](../decisions/adr-0003-no-reference-execution.md#extracted-execution-of-original-code), packet [t14-mix-v1](../../analysis/ableton-live-12.4.3/r2/t14-mix-v1/manifest.json). X shows what the function computes, not that Live reaches it for a document. The release slice is arm64; equivalence is checked statically (appendix) |
| U | Unknown; no expected result, or a static reading that must not be graded. Each U clause says how it limits T1 |

Only D, S, S-cond and X clauses may enter a release, and an S-cond clause only together
with its condition. U clauses block the behavior they name.

**Terms.**

- *Mixer stage*: a track's mixer device (`<Track>/DeviceChain/Mixer`,
  REQ-MIXER-VALUES-001) acting on audio.
- *Position*: a fader position in [0, 1].
- *Curve 1* and *curve 0*: the volume and send fader curves of REQ-MIXER-VALUES-005,
  position → gain.
- *Floor*: a gain at or below 0.0003199999919 becomes 0 (REQ-MIXER-VALUES-011).
- *Matrix*: four gains (L→L, L→R, R→L, R→R). Output L = L→L·in L + R→L·in R, and output
  R = L→R·in L + R→R·in R.
- *I*: the identity matrix (1, 0, 0, 1).
- A *ramp* to a target over n samples changes a gain linearly, sample by sample.
- *Fade time*: 75 samples (REQ-010).

## Assumptions

| ID | Assumption | What rests on it |
| --- | --- | --- |
| A1 | **Decided for T1 by [ADR 0004](../decisions/adr-0004-target-scope-t1.md#render-conventions), not Live behavior.** A render starts from a settled state. Every ramp that the loaded state starts has finished before the first rendered sample: switch fades, crossfade-assign ramps and the first matrix values. In Live a set is loaded before playback starts, and these ramps last 75 samples or 2 ms | REQ-011; every render case |
| A2 | A loaded `SoloSink` true has the effect of pressing the track's Solo button, under the loaded `SoloInPlace`. A loaded `SoloOrPflSavedValue` sets the Solo/Cue switch. Untraced: the load notification of the solo observer and the copy of the saved switch value. Static route: the post-load notification path (notes-solo.txt) | REQ-008; MG-024 to MG-027 |
| A3 | For a loaded track envelope on a Float parameter, the envelope's conversion provider is that parameter's automation target. The value conversion is then the parameter's own. Static route: the owner at `AListAutomation`+0x130 (notes-q019.txt 1d). Engine consistency supports it: the volume input of the crossfade stage takes a position | REQ-015; MG-035 |
| A4 | For sends above the exact stored minimum that reach a playing return, the send level reaches the send matrix through a level-conversion node of the send curve, with the floor. Static route: the connection of that node to the port `Send<k>` (notes-q019.txt 3c) | REQ-005 send gain; every R case with a send above its minimum |
| A5 | Audio, MIDI and return tracks take the crossfade wiring branch. The branch is chosen by a track virtual method that was not resolved. With crossfade assign None both branches give the same gain | REQ-003 for A or B assignments; MG-028 |
| A6 | Track-mixer Float parameters use the default automation settings: data step (range)/1000, a minimum ramp of 200 samples and no smoothing. No override was found for them | REQ-014; MG-035 |
| A7 | A send whose holder has `EnabledByUser` true, on a T1 graph (all outputs to Main), is active (a_k = 1). The engine bit is the holder's derived active state (`mpActive`); its derivation was not traced. The shipped defaults are true for audio and MIDI tracks | REQ-005; cases with a nonzero send reaching a playing return (MG-020 to 022, 024, 026 to 028, 030, 036); not MG-023 |
| A8 | After load every track's automation index is the arrangement. A session launch on a track sets it to the clip's slot, and the end or stop of that clip sets it to none; only Back to Arrangement, which is not a T1 action, restores the arrangement. Return and main tracks have no clip slots, so their arrangement envelopes always drive. Static: the index values and their setters (engine `OAsyncTrack`, notes-automation.txt §3); inferred: the initial value and the stop transition | REQ-012, 016; MG-032 to MG-037 |

## Requirements

### REQ-MIX-GRAPH-001 — T1 graph

- **S.** Each audio, MIDI and return track and the main track has exactly one mixer stage,
  the mixer of REQ-MIXER-VALUES-001. An audio or MIDI track's signal path is: source →
  device chain in device order → mixer stage. The mixer stage has one main output and one
  send output per return track.
- **D.** In the T1 fixture every audio, MIDI and return track has
  `AudioOutputRouting/Target` `AudioOut/Main`. The main track's own output target (for
  example `AudioOut/External/S0`) does not change the rendered signal.
- **S.** Send k of a track feeds the k-th return track. `SendPreBool` k of `LiveSet/SendsPre`
  belongs to the same return. Both follow list order. The set can have at most 12 returns:
  a thirteenth `SendPreBool` raises an error in the code that reads them. Holder-`Id` gaps
  and a holder count that differs from the return count stay U (REQ-MIXER-VALUES-003). T1
  effect: such sets are excluded.
- **S.** The render output is the main track's main output (REQ-006).

### REQ-MIX-GRAPH-002 — order inside the mixer stage

- **S.** Let x be the device chain's output (two channels), sample by sample. The mixer
  stage forms the main output y = M_main · x and, for each send k, the send output
  s_k = M_k · x. Each sample applies the matrices current for that sample (REQ-009).
- **S.** No other gain acts between the device chain and these products. The volume, the
  crossfade factor, the pan law and the on switch all act through M_main (REQ-003 and 004).
  Each send acts through its own M_k (REQ-005).
- **S.** A return track's x is the sum of the send outputs addressed to it, after its own
  device chain. The main track's x is the sum of the main outputs of all tracks and returns
  routed to Main, after the main's device chain (REQ-006).

### REQ-MIX-GRAPH-003 — volume gain

- **S-cond (A5 when assign is A or B; A3 for automated volume).** Let p be the volume
  position: the stored gain mapped by the volume curve's gain → position conversion and
  clamped to [0, 1]. The volume gain v is computed as follows:
  - Assign None, or curves 0–5: v = floor(curve1(p) × c). Here c is the track's crossfade
    factor of REQ-MIXER-VALUES-014, and c = 1 with assign None.
  - Transition (curve 6): v = floor(curve1(p × c)).
  - Every result at or below 0.0003199999919 is 0.
- **X.** The conversions and curves are those of REQ-MIXER-VALUES-005 and 014. A stored gain
  does not generally return unchanged through position and back; REQ-MIXER-VALUES-005
  records the seven tested exact curve points and the counterexamples. Keep both
  conversions in the computation above.
- **Conditional derivation; load outcome U (REQ-MIXER-VALUES-015).** If an out-of-range volume survives opening unchanged:
  - A stored volume above 1.99526238 plays at 1.99526238 (+6 dB).
  - A stored volume below 0.0003162277571, including 0 and negative values, is silent.
  - The silence threshold applies to the computed gain, not directly to the stored
    volume; there is no general round-trip error bound near that threshold.

  These are conversion consequences only. Whether opening preserves an out-of-range
  value is unknown, so they do not settle rendering from such a document.
- **S.** The main track's volume follows the same rule. The main's `CrossFadeState` is `1`
  (None) in the fixture and in every shipped set (REQ-MIXER-VALUES-009), so its c is 1.
- **U.** The main track with crossfade assign A or B, or with `Speaker` false. T1 effect:
  sets with either are excluded.

### REQ-MIX-GRAPH-004 — main matrix

- **X.** M_main = MainOn × P(w, pan, splitL, splitR, v). P is the pan-law matrix of
  REQ-MIXER-VALUES-013 with the volume gain v of REQ-003 as its gain input. MainOn is the
  on value of REQ-007 and 008 (0 or 1, or between them during a fade).
- **S.** w is the stored `PanMode` code used as the pan-mode amount: 0 Stereo, 1 Split
  Stereo. A change of `PanMode` ramps w linearly over the fade time. This settles the
  "pan mode to w" unknown of REQ-MIXER-VALUES-013.

### REQ-MIX-GRAPH-005 — sends, pre and post

- **X.** For a track outside any group, send k's matrix is
  M_k = g_k · SendsOn · a_k · (q_k · P + (1 − q_k) · I).
  - g_k is the send gain.
  - SendsOn is the track's sends-on value (REQ-007, 008).
  - a_k is 1 when send k is active and 0 otherwise.
  - q_k is 1 for post-fader and 0 for pre-fader.
  - P is the track's pan-law matrix with the volume gain (REQ-004), without MainOn.
- **X.** Consequences:
  - A **pre-fader** send carries g_k · x: no pan, no volume, no crossfade factor and no
    volume floor.
  - A **post-fader** send carries g_k · P · x.
  - Neither depends on MainOn: SendsOn alone switches all sends of a track.
- **S.** q_k = 0 (pre-fader) when the k-th `SendPreBool` of `LiveSet/SendsPre` has
  `Value="true"`, and 1 otherwise. One setting applies to every track's send k. A change
  ramps q_k linearly over the fade time.
- **S-cond (A4).** g_k = floor(curve0(r_k)), where r_k is the stored send gain mapped by the
  send curve's gain → position conversion, clamped to [0, 1]. A stored send at or below
  0.0003199999919 after conversion contributes nothing. At the exact stored minimum
  0.0003162277571, the position is 0 (X), so the send contributes nothing without
  A4 or A7. Claims for other stored values retain A4 and the conversion rounding.
- **S (A7).** a_k = 1 for a send whose holder has `EnabledByUser` true.
- **U.** a_k for a holder with `EnabledByUser` false. The engine bit is the holder's active
  state (`mpActive`), whose derivation from `EnabledByUser` and routing is not traced
  (REQ-MIXER-VALUES-003). T1 effect: graded renders require every such send to be at its
  minimum value (then g_k = 0). The shipped return-track sends satisfy this.
- **S.** s_k goes to the input of the k-th return track.

### REQ-MIX-GRAPH-006 — summing, returns and the main output

- **S.** Every destination input, at every sample, is the sum of the outputs addressed to
  it: send outputs into a return; main outputs of tracks and returns into the main track.
  The sum is formed once per sample before the destination's device chain runs.
- **S.** Each send output adds into the destination in binary64, and the destination
  converts the total to float32. Main outputs are float32.
- **U.** The order and intermediate precision of the main-bus sum. T1 effect: render
  comparisons use the tolerance under [Acceptance cases](#acceptance-cases), not exact
  sample values.
- **S.** A return track's own mixer stage (REQ-002 to 005) shapes its output to Main. A
  return's sends to returns follow REQ-005; at their minimum they contribute nothing.
- **S.** The main track has no sends (REQ-MIXER-VALUES-003). Its main output y is the
  render output, one float32 value per channel per sample.

### REQ-MIX-GRAPH-007 — mute

- **X.** With no track soloed (solo type 0), a track whose `Speaker` is false has MainOn = 0
  and SendsOn = 0. It contributes nothing to Main and nothing to any return, pre- or
  post-fader. With `Speaker` true both are 1.
- **S.** A change of `Speaker`, including a `BoolEvent` of its envelope, ramps MainOn and
  SendsOn linearly over the fade time, starting at the change's sample (REQ-009, 010).

### REQ-MIX-GRAPH-008 — solo

- **S (A2).** A track is soloed when its `Mixer/SoloSink` is true. Each track gets a solo
  type: 0 None, 1 Solo, 2 Following, 3 Muted, 4 Indirectly muted, 5 Muted for a return
  solo, 6 Pre-hear.
  - **Solo mode** (`SoloOrPflSavedValue` true), with at least one track soloed:
    - Soloed tracks are type 1.
    - Every other audio, MIDI and return track is type 3.
    - With `SoloInPlace` true and no return soloed, every return goes back to 0.
    - Tracks routed into a soloed track are type 2.
    - Tracks with an active send into a soloed return that were type 3 become type 5.
    - Non-return tracks fed by a soloed track become type 2.
    - The main track keeps 0.
  - **Cue mode** (`SoloOrPflSavedValue` false): soloed tracks are type 6 and every other
    track keeps 0.
  - **No solo:** every track is 0.
- **X.** The type and `Speaker` set the on values. With s = 1 for `Speaker` true and 0 for
  false:

  | Type | MainOn | SendsOn |
  | --- | --- | --- |
  | 0, 2, 6 | s | s |
  | 1 | 1 | 1 |
  | 3 | 0 | 0 |
  | 4 | s | 0 |
  | 5 | 0 | s |

  A soloed track therefore plays even when its `Speaker` is false.
- **S.** Consequences for T1 renders with one soloed audio or MIDI track:
  - `SoloInPlace` true: the soloed track plays and the other audio and MIDI tracks are
    silent. Returns play, so they carry only the soloed track's sends.
  - `SoloInPlace` false: the returns are silent too.
  - A soloed return: tracks with an active send to it lose their main output but keep their
    sends.
  - Cue mode: the main mix is the same as with no solo.
  - The exclusive-solo preference is not set content and has no effect on a loaded set.
- **S.** Changes ramp over the fade time (REQ-010).
- **U.** Solo of the main or pre-hear track, and solo with routing between tracks other than
  to Main (excluded by REQ-001). T1 effect: excluded.

### REQ-MIX-GRAPH-009 — when gains change

- **S.** Gains are applied per sample. There is no block-wise gain, and the buffer size has
  no effect on gains. A gain changes only at a scheduled sample, through a ramp event that
  carries a target and a length n in samples.
  - With n > 0 the gain moves linearly from its current value to the target over n samples.
  - With n = 0, or a step below 10⁻¹² per sample, it takes the target at once.
  - At a ramp's end the producer sends the exact target (switch fades) or the next ramp
    (automation, REQ-014).
- **S.** Within a ramp of n samples, d is (target − current)/n, rounded to float32, and the
  gain accumulates in float32:
  - A main-matrix entry used at the k-th sample (k = 1 … n) is current + k·d. The first
    sample already moves.
  - A send-matrix entry used at the k-th sample is current + (k − 1)·d.
- **X.** When an input of the pan law changes (w, pan, split pans, volume gain), each matrix
  entry ramps to its value at the end of the shortest running input ramp. The pan law is
  evaluated there at the inputs' interpolated values. Between such evaluations an entry is
  linear in time, so the pan law and the volume curve are applied piecewise-linearly. The
  volume curve and crossfade factor are evaluated in the same way: at each ramp end of their
  inputs, with the gain linear in between.
- **X.** Control values below 10⁻¹² in magnitude count as 0.

### REQ-MIX-GRAPH-010 — fade lengths

- **X.** The fade time is clamp(G, 10, 4096) samples with G = 75. It is a fixed number of
  samples at every sample rate.
- **S.** It applies to MainOn, SendsOn, the pre/post value q_k and the pan-mode amount w.
- **U.** A developer option can change G. T1 assumes it is absent.
- **S.** A change of crossfade assign ramps over 0.002 s × sample rate
  (REQ-MIXER-VALUES-014).
- **S.** Volume, pan, send and crossfader values ramp as their automation delivers them
  (REQ-014). Values that do not change during a render produce no ramp after the start
  (A1).

### REQ-MIX-GRAPH-011 — render start

- **Decided render convention (A1; ADR 0004).** At the first rendered sample every gain has its settled value for the
  loaded state and the start position.
  - Every on value, q_k and w already has its target.
  - Every automated parameter has the value of REQ-013 at the start position.
- **U.** What Live does in the first samples after a set is opened. T1 effect: none for the
  proposed definition; a reference comparison would not exist anyway (ADR 0003).

### REQ-MIX-GRAPH-012 — which automation drives a parameter

- **S (A8).** A track's arrangement envelopes (`<Track>/AutomationEnvelopes`) drive its
  parameters, the mixer's and its devices', as the song position moves while the track
  follows the arrangement. Every track follows it after load. Return and main tracks
  always follow it.
- **S (A8).** From the first session-clip launch on an audio or MIDI track, its arrangement
  envelopes are not applied for the rest of the render. While the launched clip plays, each
  parameter takes its `Manual` value unless the clip has a clip envelope for it. After the
  clip ends or stops, each parameter takes its `Manual` value.
- **S.** Consequence for T1: arrangement automation acts on return tracks, the main track,
  and audio or MIDI tracks before their first launch.
- **S, U.** Opening discards track envelopes on Pan, Speaker and CrossFadeState
  with fewer than two events (REQ-AUTOMATION-ENVELOPES-007). The one-event main-track
  tempo and time-signature envelopes are retained as the T11-MIN fixture shows; they
  are exempt from this exclusion. What other retained one-event arrangement
  envelopes apply remains U and is excluded from graded playback cases.
- **U.** The time base of a session clip's envelope (clip start, loop and warp), as in
  REQ-AUTOMATION-ENVELOPES-010. T1 effect: session clips with envelopes are excluded; the
  T1 target "automation applied during playback" is limited to arrangement envelopes under
  the rule above.

### REQ-MIX-GRAPH-013 — song position to envelope value

- **S.** Float playback uses a point list built from the envelope’s events in
  order (REQ-AUTOMATION-ENVELOPES-006). Bool/Enum lookup keeps event times and
  is specified only at or after its first event:
  - The first event's time becomes −10,000,000 beats, whatever it was. In every shipped
    envelope that event is the leading event at the lower bound (−63,072,000 beats,
    REQ-AUTOMATION-ENVELOPES-005). An envelope whose first event lies at another time (for
    example E4) therefore plays a ramp from −10⁷ beats to its second event.
  - Each segment that starts at an event with curve controls (REQ-AUTOMATION-ENVELOPES-008)
    becomes 16 straight pieces. The interior points lie at Bezier parameter s = 1/16 …
    15/16 of that event's cubic Bezier, with times in binary64 beats and values in float32.
- **X.** The point values are those of the original Bezier evaluator. For E9 (pan
  (0, −1) with controls 0.5/0/0.5/0 to (4, 1)) the 15 interior points start (0.352539,
  −0.999512) and end (3.647461, 0.647949). MG-031 gives all of them.
- **S; offset U.** At envelope time t′ the segment starts at the last point at or
  before t′. t′ is song beat t minus an automation offset, rounded to the
  1/3,843,840-beat grid. The offset is present but untraced even for arrangement
  envelopes (t14 `notes-automation.txt` §1b and §3; staging F6). No zero-offset
  or sample-timing claim is established. Computation cases take envelope time
  as input. At coincident points the later one applies (lookup mode 1).
- **X, under default settings with a nonzero data step (A6).** Within a segment
  from (t_a, v_a) to (t_b, v_b), the value at envelope time t is computed with
  durations in samples:
  - slope = float32(v_b − v_a) / ((t_b − t_a) · samples per beat), in binary64;
  - value = v_a + max(0, (t − t_a) · samples per beat) · slope, kept inside [v_a, v_b];
  - v_a = v_b gives a constant segment;
  - with no later point the value holds;
  - without a nonzero data step the segment value is held, rather than interpolated
    (mix-graph-v1 review RMG-01).
- **S.** Therefore what is played differs from REQ-AUTOMATION-ENVELOPES-010's E(t) in three
  ways. The curve cases (AEN-021, 022) and the leading-event ramp (AEN-018) do not describe
  playback:
  - A curved segment plays as the polyline. E9 at t = 1 and 3 gives −0.98246047 and
    0.01753953, not E(t) = −0.983523965 and 0.0164760482.
  - A ramp from the leading event starts at −10⁷ beats. E13 at t = 0 gives
    3.9999984·10⁻⁷, not 6.341957714539603·10⁻⁸.
  - At a step the later event applies.
- **S.** Bool and Enum envelopes apply the value of the current point, without interpolation
  (REQ-AUTOMATION-ENVELOPES-011, mode 1 at steps).

### REQ-MIX-GRAPH-014 — how often automated values are applied

- **S (A6).** While the transport plays, a Float parameter's value moves along its current
  segment through ramps of L samples:
  - for r = step / |slope| < 2³¹, L = clamp(trunc(r), 200, 65,536);
  - for r ≥ 2³¹, L = 200: the 32-bit truncating conversion overflows to
    −2³¹ before the clamps (staging F3, confirmed by x86 disassembly);
  - step is the parameter's engine-side range divided by 1000: 0.001 for volume and send
    (positions in [0, 1]); 0.002 for pan, inferred from its range −1 to 1;
  - slope is the segment slope per sample (REQ-013);
  - a flat segment sends no ramp;
  - the last ramp before a point is shortened to a whole number of samples that ends on the
    segment line; the value then holds until the point's sample, so it deviates from the line
    by at most one step;
  - a new segment starts at each point's sample.
- **S.** With the transport stopped, a value change takes effect at once (n = 0).
- **S.** For volume and send automation the curve and floor of REQ-003 and 005 are evaluated
  at each ramp end, and the gain is linear in between (REQ-009). Example: a volume segment
  from position 0.85 to 0.70 over 4 beats at 44,100 Hz and 120 BPM has slope
  −1.70068·10⁻⁶ per sample. That gives L = 587 samples, so the gain is piecewise linear in
  pieces of 587 samples.
- **U.** Smoothing settings other than the default (A6). T1 effect: none found for mixer
  parameters; device parameters follow their device specs.

### REQ-MIX-GRAPH-015 — units of automated values

- **S-cond (A3).** Volume and send envelope values are converted to fader positions (the
  gain → position conversion of REQ-MIXER-VALUES-005, clamped) before the point list is
  built. A volume envelope therefore interpolates linearly in fader position, not in gain.
  Pan, split-pan and crossfader values are used as stored (their conversion is the identity
  on their range).
- **S.** This contradicts assumption A1 of
  [SPEC-AUTOMATION-ENVELOPES](automation-envelopes.md) r3 ("every Float envelope value is in
  stored units") for Volume and Send targets. Pan, the target of all its value cases, is
  unaffected.

### REQ-MIX-GRAPH-016 — automated and manual values

- **S.** While an envelope drives a parameter (REQ-012), the engine uses the envelope's value
  in place of the stored `Manual` value. When the envelope stops driving it (for example at a
  session-clip launch), the parameter takes its `Manual` value.
- **U.** Automation override and re-enable, and what `LiveSet/AutomationMode` changes. T1
  effect: none for renders, which make no manual changes.

## Timing and state

- **Units.** Gains are linear amplitude; positions are 0 … 1; song time is in beats. Samples
  per beat = sample rate × 60 / tempo, as in SPEC-TRANSPORT-STATE.
- **Granularity.** Gains act per sample (REQ-009). The mapping of automation
  envelope time to a song sample remains untraced (REQ-013); value computations
  alone do not establish sample timing.
- **Constants.**
  - fade time 75 samples (REQ-010);
  - crossfade-assign ramp 2 ms;
  - automation ramps 200 to 65,536 samples (REQ-014);
  - floor 0.0003199999919;
  - envelope beat grid 1/3,843,840;
  - leading point −10⁷ beats.
- **Persistent state.** Only the stored fields named above. Solo types, on values and ramps
  are runtime state.
- **Determinism.** For a given document and script the output is deterministic up to the
  summation order of REQ-006.

## Acceptance cases

None of these cases has been run against Live, and none will be (ADR 0003).

- **Kinds.**
  - C: computation, one function's result; the expectation is X.
  - R: composed render expectation, from the requirements; static or X-derived, unmeasured.
  - U: unresolved, not graded.
- **Base document B0.** The shipped `Core Library/Lessons/Sets/Recording Audio.als`
  (SHA-256 `af57ff8f9eb1c2c51220ef6633a58838532350d53640df5f48dc01659023c043`), as in
  SPEC-MIXER-VALUES. It is decoded, changed only as stated, and re-encoded.
  - Mixers: A = `AudioTrack[@Id="0"]` (no devices, output `AudioOut/Main`); R =
    `ReturnTrack[@Id="2"]` (no devices, output `AudioOut/Main`); M = the main track (no
    devices).
  - As shipped: every volume `1`, pan `0`, `PanMode` `0`, `CrossFadeState` `1`, `Speaker`
    `true` and `SoloSink` `false`.
  - A's send to R and R's send to itself are `0.00031622799`; A's holder has `EnabledByUser`
    true and R's has false.
  - `SendsPre` holds one `SendPreBool Id="0" Value="false"`; `SoloInPlace` and
    `SoloOrPflSavedValue` are true.
- **Source.** An R case adds an audio clip to A's first clip slot (`ClipSlot Id="0"`) and
  launches it at beat 0 with the transport; its content and playback are SPEC-PLAYBACK-CORE's.
  x denotes the clip's signal at A's mixer-stage input, the same on both channels unless
  stated. An R case states the main output as a factor times x. Automation cases put their
  envelope on the main track M (targets Pan `337`, Volume `338`) or on R (Speaker `330`), whose
  arrangement envelopes drive while A's clip plays (A8). Rates: 44,100 Hz and 120 BPM. An
  automation case reads the value applied to the target at the stated beat through an adapter,
  as in the value comparator of SPEC-AUTOMATION-ENVELOPES.
- **Comparator (proposed, to be decided before grading).** The candidate's main output must
  be within 10⁻⁵ × max|x| of the stated factor times x, sample by sample, after any ramp has
  finished, under A1.
- **Precision.** C cases compare within 10⁻⁶ unless a tolerance is stated; values are given
  to about six significant digits.

| Case ID | Requirement | Kind | Setup/action | Expected result/comparator | Label |
| --- | --- | --- | --- | --- | --- |
| MG-001 | 005 | C | Send matrix, post-fader, matrix M = (0.9, 0.1, 0.2, 0.6), g 0.5, on, active | (0.45, 0.05, 0.1, 0.3) | X |
| MG-002 | 005 | C | As MG-001, pre-fader | (0.5, 0, 0, 0.5) | X |
| MG-003 | 005 | C | As MG-001 with q = 0.5 (mid-fade) | (0.475, 0.025, 0.05, 0.4) | X |
| MG-004 | 005, 007 | C | As MG-001 with SendsOn 0; separately a = 0; separately g = 0 | (0, 0, 0, 0) each | X |
| MG-005 | 005 | C | Post-fader, g 1, M = pan law of pan −0.5 at volume 0.5 (0.65328, 0, 0, 0.270598); then pre-fader | (0.65328, 0, 0, 0.270598); (1, 0, 0, 1) | X |
| MG-006 | 004 | C | Main matrix (0.9, 0.1, 0.2, 0.6) with MainOn 1, 0, 0.5 | the matrix; zeros; half the matrix | X |
| MG-007 | 007, 008 | C | On values for solo types 0 to 7 with `Speaker` true and false | The table of REQ-008; types outside 0–6 as 0 | X |
| MG-008 | 008 | Withdrawn | Internal solo predicates have no behavioral observable | No graded result. The old speaker-ignored claim for type 4 contradicted REQ-008: its main gate follows Speaker | Withdrawn (staging F1) |
| MG-009 | 010 | C | Fade time without a developer option | 75 samples | X |
| MG-010 | 009 | C | Control ramp from 0 to 1 over 4 samples, advanced one sample at a time | 0.25, 0.5, 0.75, 1, then 1 | X |
| MG-011 | 009 | C | Control ramp from 0 to 1·10⁻⁹ over 10,000 samples; value 5·10⁻¹³ | Jumps to 1·10⁻⁹ at once; reads as 0 | X |
| MG-012 | 009 | C | Pan law inputs w 0, pan 0, splits −1/+1, volume 1. Volume ramp to 0.5 over 100 samples at sample 0; pan ramp to −1 over 50 samples at sample 20 | After the first event: targets (0.5, 0, 0, 0.5) over 100. After the second: (0.919239, 0, 0, 6.5·10⁻⁶) over 50 | X |
| MG-020 | 002, 005, 006 | R | B0, A send `0.5011872053` | Main = 1.5011872·x on both channels | S-cond (A1, A4, A7); gains X |
| MG-021 | 005 | R | B0, A volume `0.5011872053`, A send `0.5011872053`, `SendPreBool` `true`; separately `false` | Pre: main = 1.0023744·x. Post: main = 0.7523758·x | S-cond (A1, A4, A7); gains X |
| MG-022 | 004, 005 | R | B0, A pan `-1`, A send `0.5011872053`, pre; separately post | Pre: main L = 1.9154008·x, main R = 0.5011972·x. Post: main L = 2.1229993·x, main R = 1.5011872·10⁻⁵·x | S-cond (A1, A4, A7); gains X |
| MG-023 | 007 | R | B0, A send `0.5011872053`, A `Speaker` `false` | Main = 0 (no direct and no return contribution) | S (A1); on values X |
| MG-024 | 008 | R | As MG-023 with A `SoloSink` `true` | Main = 1.5011872·x (soloed: speaker ignored; R plays, solo in place) | S (A1, A2, A7) |
| MG-025 | 008 | R | B0, A send `0.5011872053`, A `SoloSink` `true`, `SoloInPlace` `false` | Main = x (R muted) | S (A1, A2) |
| MG-026 | 008 | R | B0, A send `0.5011872053`, R `SoloSink` `true` | Main = 0.5011872·x (A type 5: no main output, send kept) | S (A1, A2, A7) |
| MG-027 | 008 | R | B0, A send `0.5011872053`, A `SoloSink` `true`, `SoloOrPflSavedValue` `false` | Main = 1.5011872·x (Cue mode: no muting) | S (A1, A2, A7) |
| MG-028 | 003, 005 | R | B0, A `CrossFadeState` `0` (A), crossfader `1`, A send `0.5011872053`, pre; separately post | Pre: main = 0.5011872·x (only through R). Post: main = 0 | S-cond (A1, A4, A5, A7); curve X |
| MG-029 | 003 | U | B0, A volume `2`; separately `0`; separately `-1` | Conditional conversion result: Main = 1.9952624·x; 0; 0 only if opening holds each out-of-range value unchanged; not graded from a document | U (load assumption; staging F2) |
| MG-030 | 003, 006 | R | B0, A send `0.5011872053`, M volume `0.5011872053` | Main = 0.7523758·x | S-cond (A1, A4, A7) |
| MG-031 | 013 | C | Curved segment of E9 ([automation fixtures](automation-envelopes.md#fixtures)): (0, −1) with controls 0.5/0/0.5/0 to (4, 1); the 15 interior polyline points | (0.352539, −0.999512), (0.664062, −0.996094), (0.94043, −0.986816), (1.1875, −0.96875), (1.411133, −0.938965), (1.617188, −0.894531), (1.811523, −0.83252), (2, −0.75), (2.188477, −0.644043), (2.382812, −0.511719), (2.588867, −0.350098), (2.8125, −0.15625), (3.05957, 0.072754), (3.335938, 0.339844), (3.647461, 0.647949), within 10⁻⁶ | X |
| MG-032 | 012, 013 | U | B0 + source + E9's events on M's pan (`PointeeId` 337); M's pan at beats 1, 2, 3 | −0.98246047, −0.75, 0.01753953 as segment values, not ramped sample values | U for song-time render (offset and A8); values X |
| MG-033 | 013 | U | B0 + source + E13's events on M's pan; M's pan at beat 0 | 3.9999984·10⁻⁷ as a segment value, not a ramped sample value | U for song-time render (offset and A8); value X |
| MG-034 | 013, 014 | U | B0 + source + E1's events on M's pan; M's pan at beats 5, 6, 7 | 0.25, 0.5, 0.75 | U for song-time render (offset and A8); values X |
| MG-035 | 014, 015 | U | B0 + source + M volume envelope (`PointeeId` 338) (L, `1`), (0, `1`), (4, `0.5011872053`) | M's fader position is linear from 0.85 at beat 0 to 0.70 at beat 4. M's gain is curve 1 of that position at every 587-sample ramp end from beat 0, linear in between. At beat 2 (sample 44,100) the position is 0.775 within 10⁻⁶ | S-cond (A3, A6, A8); curve X; song-time offset U |
| MG-036 | 007, 010 | U | B0 + source, A send `0.5011872053`, R `Speaker` envelope (`PointeeId` 330) `BoolEvent` (L, `true`), (4, `false`), (8, `true`) | Main = 1.5011872·x before sample 88,200. From sample 88,200 R's main gain falls linearly to 0 over 75 samples: main = (1 + 0.5011872·(1 − k/75))·x at the k-th sample, then x. From sample 176,400 it rises back over 75 samples | S (A1, A7, A8); fade X; song-time offset U |
| MG-037 | 012 | R | B0 + source + E1 on A's pan (`PointeeId` 323) | A's pan stays at `Manual` (0) at beats 5, 6, 7, because A's clip was launched at beat 0 | S (A8) |
| MG-038 | 001 | U | B0 with thirteen returns and a thirteenth `SendPreBool` | Unresolved (excluded) | U |
| MG-039 | 005 | U | B0, R send to itself `0.5011872053` with `EnabledByUser` false | Unresolved (a_k untraced) | U |
| MG-040 | 012 | U | B0, M pan envelope with only its leading event (L, 0.5), `Manual` 0 | Unresolved | U |
| MG-041 | 012 | U | B0 + a session clip on A with a clip envelope on A's pan | Unresolved (clip time base) | U |

**Notes on the cases.**

- **Composed gains.** The R cases compose the X gains of
  [SPEC-MIXER-VALUES](mixer-values.md) (fader curves and pan law) with the X matrices above.
- **Factors.** 1.5011872 = 1 + 0.5011872053; 0.7523758 = 0.5011872053 + 0.5011872053²;
  1.9154008 = 1.4142135 + 0.5011872. MG-022 post R = 10⁻⁵ × (1 + 0.5011872).
- **Excluded.** Cancellation and teardown kinds are omitted: a render has no cancellable
  step in this scope. Malformed input has no case: the document rules are SPEC-MIXER-VALUES
  and SPEC-AUTOMATION-ENVELOPES.
- **Count.** 34 case IDs: 1 withdrawn (MG-008), 12 X computations
  (MG-001 to 007, 009 to 012, 031), 11 conditional composed renders
  (MG-020 to 028, 030, 037), and 10 unresolved (MG-029, 032 to 036,
  038 to 041). Nonzero sends reaching a playing return need A4/A7;
  automation renders retain the untraced offset and A8 conditions.

## Open questions

[Q-019](../questions.md#q-019-mixer-volume-and-send-values-sent-to-the-engine) is settled
statically by this packet, with the conditions A3 and A4 and two more:

- the wiring branch (A5);
- the arm64 comparison of the envelope and send-graph paths.

The unknowns that limit T1 are these:

- **Solo on load (A2).** It is untraced; every solo render rests on it.
- **The send-active bit (REQ-005).** Graded sends with `EnabledByUser` false must be at their
  minimum.
- **The session-clip envelope time base (REQ-012).** T1 automation is limited to arrangement
  envelopes on return and main tracks and on audio or MIDI tracks before their first launch.
- **The send-active rule and the automation index (A7, A8).** Every send case and every
  automation case rests on them.
- **The single-event envelope (REQ-012).**
- **The main-bus summation order (REQ-006).** Renders are compared within a tolerance.
- **Main with crossfade assign, `Speaker` false or solo (REQ-003, 008).** Excluded.
- **The developer option on the fade time (REQ-010).**

## Analyst evidence appendix

Analysis-only. Do not copy into a handoff. Canonical research:
[mix graph](../research/mix-graph.md). Retained packet
`analysis/ableton-live-12.4.3/r2/t14-mix-v1/`:

- notes: `notes-mix.txt`, `notes-solo.txt`, `notes-automation.txt`, `notes-q019.txt`;
- excerpts: `excerpts-*.jsonl`;
- X runs: `results/mix.json`, `raw/runs.jsonl`;
- matches: `addresses.json`, `match-engine.txt`;
- scan: `fma-scan.txt`.

Addresses are named engine functions (x86_64 `Ableton Live Engine`, image base 0), Live
x86_64 (base `0x100000000`) and arm64. "pc" means pseudocode only; ✓ means confirmed in
objdump.

| Requirement | Evidence | Strength |
| --- | --- | --- |
| 001 | Track-out unit builder Live x86 `0x102866450` (arm64 `0x102731438`, pc); `SendsPre` mask `0x1027bde00` (pc, 12-bit `bitset`); shipped routing B0 lines 84, 531 | S, D |
| 002 | `OTrackOutProcessor` ports (engine SEnable `0x175550`); `OTrackOutVolumeProcessor` ports (`0x171b50`, handlers resolved with `engine_ptrs.py`); builder wiring (pc) | S |
| 003 | Q-019 notes 1a–1c (✓ `0x10284f013`, `0x102683d70`), 2a (✓ `0x102853727`), 2b; crossfade recompute engine `0x14a570` = Live `0x101b198c0`; floor `0x39a7c5ac`; X2 curves | S-cond; X for curves |
| 004 | `TVolumeSwitch::Calc` `0x101b40cf0` (X); panner recompute `0x101b27860` → `TVolumePanner::Calc` `0x101b719e0` (X); `PanMode` → `PanModeRamp` → `PanModeAmount` (pc) | X, S |
| 005 | `TSendVolumes::Calc` `0x101b40d30` (X, 12 cases; body read in objdump ✓, notes-q019.txt 3e); 13-input layout from the handlers (pc); constructor defaults `0x172af0` (pc); pre/post splitter engine `0x171250` (pc); send converter kind 0 (✓ `0x102788389`) and level node (✓ `0x1026f8ccd`) | X, S, S-cond |
| 006 | Send output accumulation ✓ `0x101b4c400` (`addsd` into the destination); track input `0x1702e0` (pc); main outputs are float32 fields ✓ `0x101b4d870` | S; order U |
| 007 | Switch word `0x101b3fdc0`/`0x101b3ff50` and splitter `0x101b401c0` (X, all types and words) | X, S |
| 008 | Logic `0x10284d180`, `0x10284c580`, `0x10285cf50` (pc; notes-solo.txt §3); predicates `0x101ae9e90`/`eb0`/`ed0` (X) | S (A2), X |
| 009 | Per-sample functions ✓ `0x101b4d870` (main: add, then multiply) and ✓ `0x101b4c400` (send: multiply, then add); ramp handlers engine `0x176c00`, `0x177cd0` (pc); `ORampInterpolator` `0x101b2b970`, `0x101b2bae0`, `0x101b2ba30`, `0x101b2ba80` (X) | S, X |
| 010 | `STrackFadeTime` `0x101b0ee70` after `0x101b0ecb0` (X: 75); `OMakeRampProcessor` engine `0x157890`/`0x157930` (pc); builder ramp nodes (pc) | X, S |
| 012 | Engine `OAsyncValueTimeable::ActivateAutomation` `0x13d800` (Live `0x101b0cb60`, pc), automation index (notes-automation.txt §3) | S |
| 013 | Point list `0x102823cb0` (✓ loop; ✓ `0x102823d84` stores −1e7 from `0x105dae938` into the first time unconditionally); Bezier `0x1011f1610` (X, 15 points); lookup engine `0x141110`, grid `0x15bdfe0` (pc); `OFloatAutomationSegment::Init` `0x101b1f400` (X) | S, X |
| 014 | Default settings hook `0x10282b410` (✓ N 1000, 200, 0); ramp length engine `0x16a240` (✓); `SendRamp` `0x169c00` (pc) | S (A6) |
| 015 | Iterator `0x102518360` (✓), provider cast `0x102687e00`, `AFloatAutomationTarget` slot +8 `0x10281abe0` (pc) | S-cond (A3) |
| 016 | `ActivateManualValue` (engine vtable slot 0x38 → `0x13de60`, pc) | S |

**Slice comparison** (`fma-scan.txt`). Most compared functions have no fused operation in
either slice: `TSendVolumes::Calc` (arm64 `0x101b10efc`), `SetRamp` (`0x101aff3a0`), the panner
recompute (`0x101afb494`) and the send recompute (`0x101b18bb4`). Two fuse on arm64:

- **SGroupedVolumes** (`0x101b3b720`) fuses four multiply-adds. With the identity group
  matrix every product is exact, so ungrouped tracks are unaffected.
- **Extrapolate** (`0x101aff494`) fuses one binary64 multiply-add before rounding to float32.

The arm64 per-sample track-output functions (`0x101b1c114`, `0x101b1afbc`) were not compared.
If they fuse input × gain + input × gain, an output sample can differ in its last float32
bit. That is inside the proposed comparator.

**Corrections to existing pages found by this packet.** They were applied on 2026-10-18 in SPEC-AUTOMATION-ENVELOPES r4 and SPEC-MIXER-VALUES r4, and in a dated note on the [mixer values](../research/mixer-values.md) research page:

- **SPEC-AUTOMATION-ENVELOPES r3.**
  - A1 is wrong for Volume and Send targets (REQ-015).
  - REQ-010 and its curve and leading-event cases describe the logic-side evaluator, not
    playback (REQ-013).
  - A2's drive is now static (REQ-012, 013).
- **x2-mixer-v1 `addresses.json`.** It names arm64 `0x101ac3c94` position → gain. That
  function is gain → position; `0x101ac3bac` is position → gain.
- **SPEC-MIXER-VALUES r3.** These clauses can be narrowed:
  - REQ-011's condition (REQ-003 here);
  - REQ-012 (REQ-005);
  - REQ-013's two U clauses (REQ-004, 009, 010);
  - REQ-015's rendering part for volume (REQ-003).

## Revision and handoff

| Revision | Date | Change |
| --- | --- | --- |
| 1 | 2026-10-18 | First draft (T1.4). 16 requirements: X clauses in 003, 004, 005, 007, 008, 009, 010 and 013; S-cond clauses in 003, 005 and 015; U clauses in 001, 003, 005, 006, 008, 010, 011, 012, 014 and 016; 011 is a proposed definition; 002 is S only. Assumptions A1 to A8. Q-019 settled statically with conditions. 34 cases: 13 C (X), 17 R (composed, unmeasured), 4 U |
| 2 | 2026-10-19 | Correct REQ-003’s exact-round-trip claim and direct stored-value silence threshold using mixer-values-v2 review RVM2-01. Keep both fader conversions. Apply staging F1–F6 and review RMG-01 to 03: MG-008 withdrawn, MG-029 ungraded; 32-bit ramp overflow, data-step condition, untraced automation offset, one-event tempo/meter exception, A4/A7 scope. Other case IDs preserved; song-time automation render cases MG-032 to 036 are ungraded. 34 IDs: 12 X, 11 conditional renders, 10 U, 1 withdrawn. |

Current release: [mix-graph-v1](../../handoff/mix-graph-v1/README.md),
28 cases approved with narrowing (review RMG-01 to 03). Its automation
computations take envelope time as input under default settings; no song-time
offset or automation-drive expectation is released.
