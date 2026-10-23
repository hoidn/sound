---
id: SPEC-PLAYBACK-CORE
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 2
target: Ableton Live 12 Suite 12.4.3 / macOS
---

# Playback core: transport, launch timing and clip playback

## Review status

Revision 2 incorporates the independent playback-core-v1 review corrections.
The [handoff plan](playback-core-handoff-plan.md#review-outcome--2026-10-19)
records the approved finite scope and retained review evidence. The reviewed
snapshot is based on revision 1 with these corrections; the broader draft
remains unreleased outside that scope. Reference and candidate execution are
not-run. Staging approval is not catalog publication.

## Scope

Feature FEAT-TRANSPORT and FEAT-SESSION, with FEAT-MIDI and FEAT-AUDIO, in the
[feature map](feature-map.md). It serves workstream T1.3 of target T1
([ADR 0004](../decisions/adr-0004-target-scope-t1.md)). User task: from a Live Set and a script
of transport and launch actions, render the output offline, deterministically, at a stated
sample rate. This draft specifies the parts of that render that come before devices and the
mixer:

- the song clock: beats to samples, tempo, Play, Stop, Continue and the song loop;
- when a triggered session clip starts, in samples, under launch quantization;
- which note-on and note-off events a playing MIDI clip sends, and on which sample;
- which file samples an audio clip with warping off produces for each output sample;
- when a clip stops, for stop buttons, a replacing launch, transport Stop and the clip's end.

Timing is stated as render sample indices, the timing dimension of ADR 0004. Audio clip output
is stated as the clip's signal before the track's devices and mixer. Mixing, sends and
automation belong to the planned SPEC-MIX-GRAPH (T1.4), and instrument audio to the device
specs (T1.2).

Every requirement is a **proposed contract**. Each clause is supported by shipped bytes, by a
static derivation from the 12.4.3 program, or by extracted execution of the shipped x86_64
code, or it is explicitly unknown. Live was never run, and under
[ADR 0003](../decisions/adr-0003-no-reference-execution.md) it will not be. Static evidence
comes from both Live slices and from the x86_64 Live Engine bundle, whose function names were
matched to Live's own code (appendix). No published Ableton documentation is retained in
`raw/`, so no clause rests on it. Behavior that only documentation would show is U.

Dependencies:

- **[SPEC-CLIP-LAUNCH](clip-launch.md) r4**: launch values, the grid length (REQ-015) and the
  boundary arithmetic (REQ-017).
- **[SPEC-TRANSPORT-STATE](transport-state.md) r4**: the stored tempo, signature and loop values.
- **[SPEC-MIDI-NOTE-STORAGE](midi-note-storage.md) r3**: the stored notes, their limits and the
  1/3,843,840-beat time grid.
- **[SPEC-WARP-MARKERS](warp-markers.md) r4**: `IsWarped` and the warp fields.
- **[SPEC-ALS-CONTAINER](als-container.md)**: the document envelope.

Target: 12.4.3, documents with `MinorVersion="12.0_12402"`.

**Excluded** (no requirement; fixtures avoid them):

- Arrangement playback, recording, count-in and overdub.
- Launch modes other than Trigger, Legato, follow actions and scene launching (except Stop All
  Clips, REQ-022).
- Launches through the Live API with an explicit quantization or time.
- Warped audio clips; groove; tempo automation, scene tempo, Link, external sync and the tempo
  follower.
- Track delay and latency compensation (T1.4).
- MIDI controller input (midi-config).
- Undo.
- Real-time delivery of actions; see the definition of a request sample.

## Evidence labels

| Label | Meaning |
| --- | --- |
| D | Documented in shipped bytes: the schema files or the Live Sets in the 12.4.3 bundle, written by 12.4d1 or older. No published manual is retained, so no clause is D on documentation |
| S | Static derivation from the 12.4.3 program, in both Live slices unless the clause says otherwise; not an observed run |
| S-cond | Static derivation that rests on an assumption below, named beside the clause |
| X | Extracted execution: the shipped x86_64 function was run on the stated inputs in the harness of [ADR 0003](../decisions/adr-0003-no-reference-execution.md#extracted-execution-of-original-code). It shows what the function computes, not that Live reaches it with those inputs; the path is S and stated. The arm64 release slice is matched by static comparison |
| U | Unknown; no expected result, or only a static expectation that must not be graded. Each U that limits T1 says how |

Only D, S, S-cond and X clauses may enter a release. U clauses block the behavior they name.

## Definitions

These definitions make the render gradable. They describe how a render and its script are
read, not a behavior of Live.

- **Rate.** SR is the render's sample rate in Hz, an integer; cases use 48,000 and 44,100.
- **Render sample.** Render sample 0 is the first sample processed after the script's first
  Play (or first launch while stopped, REQ-010). Indices count up from there.
- **Request sample.** Every scripted action (Play, Stop, Continue, a launch, a stop button, a
  tempo change) names the render sample R at which the engine handles it. In Live, actions are
  messages to the audio thread, and when one is handled relative to the audio buffer is U.
  Clauses state results relative to R.
- **Lattice.** L(x) is the rounding of REQ-CLIP-LAUNCH-013 to the nearest multiple of
  1/3,843,840 beat, binary64 formula. A lattice beat is a value L returns, taken as the exact
  rational multiple it stands for.
- **Tempo.** T is the tempo in effect, as a binary32 value in BPM (REQ-003).
- **Position of a beat.** Given an anchor (render sample n_a, beat b_a) of REQ-001, the ideal
  position of lattice beat b is P(b) = n_a + the least integer at or above
  (b − b_a) × SR × 60 ÷ T. It is computed exactly, with b as its lattice rational and b_a as the
  exact value of the anchor beat.
- **Transport is playing.** Between a Play (or a launch while stopped) and the next Stop.

## Assumptions

Each assumption is supported by the evidence but not established. If one fails, the clauses
that name it become U.

| ID | Assumption | What rests on it |
| --- | --- | --- |
| A1 | Where a function was matched only in the x86_64 slice, arm64 implements the same logic. Support: Engine and Live x86_64 instruction streams are identical (scheduler, fire manager) or 70–100 % equal bytes at the same size (clip players, warper). arm64 counterparts of the neighbouring and calling functions match. The appendix lists the x86_64-only functions | Clauses marked S-cond (A1) |
| A2 | The clip attribute processor that applies the velocity amount lies on the path from a MIDI clip's note player to the instrument | REQ-015 |
| A3 | A session audio clip's `Fade`, `HiQ`, `IsWarped`, `SampleVolume`, `PitchCoarse` and `PitchFine` reach the engine as read, and a session clip is never "crossfading in". That flag belongs to arrangement clips | REQ-008, REQ-017 to REQ-021 |
| A4 | While a set is open, the engine's global quantization is the loaded `GlobalQuantisation` (posted by the song unit when it changes) | REQ-007, REQ-022 |
| A5 | A clip slot's stored `HasStop` sets the engine flag that makes an empty slot's button a stop button | REQ-022 |

## Requirements

### REQ-PLAYBACK-CORE-001 — the song clock

- **S.** The scheduler measures song time in beats against an anchor: a render sample n_a and
  the beat b_a playing there. Samples per beat are spb = (SR ÷ T) × 60 and beats per sample are
  1 ÷ spb, each operation in binary64.
- **S, X.** The song beat at render sample n is b_a + (n − n_a) × (1 ÷ spb) in binary64. The
  anchor changes at Play (REQ-004), Continue (REQ-005), a song-loop jump (REQ-006), a tempo
  change (REQ-003) and any other position jump. Positions are never accumulated sample by
  sample.
- **X.** The stored spb equals (SR ÷ T) × 60 bit for bit. At 48,000 Hz: 24,000 at 120 BPM,
  32,000.000000000004 at 90 BPM, 20,571.42857142857 at 140 BPM. At 44,100 Hz: 29,400 at 90 BPM,
  22,050 at 120 BPM.
- **S.** Results relative to an anchor do not depend on the engine buffer size: each buffer is
  split at every scheduled event.

### REQ-PLAYBACK-CORE-002 — placing an event on a sample

Applies to every event scheduled at a beat: notes, clip loop wraps and ends, launches, quantized
stops, song-loop braces and quantized tempo changes.

- **S.** The event beat is first rounded to the lattice. While the event is handled, the song
  beat reads exactly that lattice beat.
- **X** (1,216 X placements and a 240,000-placement sweep of the X-confirmed operation order).
  An event at lattice beat b takes effect on render sample P(b) in two cases:
  - when (b − b_a) × SR × 60 ÷ T is not an integer;
  - when it is an integer and the binary64 product of the binary64 beat difference and spb does
    not exceed that integer.

  Otherwise it takes effect on P(b) or on P(b) + 1. Examples at 48,000 Hz:
  - At 120 BPM with dyadic beats, every position is exact.
  - At 90 BPM, a whole beat b falls on 32,000·b or 32,000·b + 1.
  - At 140 BPM, beat 1 falls on 20,572.
- **U.** Which of P(b) and P(b) + 1 occurs in the remaining case. It depends on the engine's absolute
  sample count since the audio engine started, which neither the set nor the script
  determines. In the sweep, P + 1 occurred only for counts below 2³⁰. **T1 effect:** cases at
  such positions accept either value. Cases that need one exact value use rates and tempos with
  an exact spb (120 BPM at 48,000 Hz, 90 BPM at 44,100 Hz).
- **S.** Events that fall on the same beat are handled in priority order:
  - per-note expression, then note-off, then a clip's loop wrap or end, then note-on (S-cond
    (A1));
  - the song loop's end brace before its start brace.

  The order of a launch or stop event relative to note events at the same beat is U. Cases avoid
  that coincidence.

### REQ-PLAYBACK-CORE-003 — tempo

- **S.** The song tempo is used as a binary32 value, limited to 20 to 999 BPM; the tempo
  modulation is 1. A value outside the range plays at the nearer limit.
- **S.** A tempo change while the transport is stopped applies at once.
- **S.** A tempo change requested while playing applies at the first multiple of 1/4 beat at or
  after the song beat at the request sample. It applies at once when that beat, multiplied by 4
  in binary32, is a whole number.
- **X.** At that point the clock re-anchors: n_a is the sample where the change applies, b_a is
  the quarter-beat line, and T is the new tempo. Example: at 48,000 Hz, a change from 120 to
  90 BPM requested at beat 1 (render sample 24,000) puts beat 2 at 56,000 or 56,001 (REQ-002;
  the X run gave 56,000).
- **S.** Tempo changes during a render are T1-relevant: ADR 0004 lists tempo among the transport
  behaviors, and a script may change it. The beat positions of notes and launches follow the
  new tempo from the change on. Unwarped audio clips do not change speed (REQ-021).

### REQ-PLAYBACK-CORE-004 — Play from stopped

- **S, X.** Play with start beat t\* rounds t\* to the lattice and raises a negative value to 0.
  Song beat t\* plays at render sample 0, and an event at t\* takes effect on render sample 0.
  The anchor is (0, t\*).
- **S.** Live chooses t\* in this order: the loop start when "loop is song start" is on; the
  insert marker; the earlier end of the arrangement selection; 0. When a session clip is playing
  with Session View visible and t\* is not the loop start, playback starts at the bar line at or
  before t\*.
- **U.** Which of these holds after a set is opened. It is interface state, and whether the
  stored `CurrentTime` sets the insert marker was not traced. The bar-line rule's helper and its
  Session-visible condition are also untraced. **T1 effect:** a render script states t\*. Cases
  use t\* = 0 with the loop off and no clip playing.
- **S.** No count-in occurs unless starting would begin recording (excluded).

### REQ-PLAYBACK-CORE-005 — Stop and Continue

- **X.** Stop handled at request sample R ends playback there. The song beat stays at the beat
  of sample R (REQ-001), and no later sample advances it.
- **X.** Continue (play without a position change) handled at R′ resumes from that beat, with
  anchor (R′, that beat). Example at 48,000 Hz and 140 BPM, playing from beat 0:
  - Stop at 30,000 holds beat 1.4583333333333335;
  - Continue at 35,000 gives beat 2.916666666666667 at 65,000.
- **S.** A Play after a Stop is a Play with a start beat (REQ-004). If that changes the
  position, the clips are re-based (REQ-023).
- **U.** The position after a second Stop while stopped (a write of 0.0 was found, but not
  traced further). **T1 effect:** scripts do not use a second Stop.
- **U.** What the user's Stop, Continue and Play controls do beyond these requests (documented
  behavior not retained).

### REQ-PLAYBACK-CORE-006 — the song loop

Applies while the transport plays with the arrangement loop on (`Transport/LoopOn`,
`LoopStart`, `LoopLength`).

- **S.** The loop start is used as at least 0 and the loop length as at least 1 beat.
- **S, X.** When the song beat reaches loop start + loop length, song time jumps to the loop
  start on that sample. The end is placed by REQ-002, and each jump re-anchors the clock. A loop
  end at or before the song beat at Play, or before the loop was switched on, does not jump in
  that pass. Playing from at or after the loop end never loops.
- **X.** Examples:
  - 48,000 Hz, 120 BPM, loop 4 to 8, Play from 4: jumps at 96,000, 192,000, 288,000 and 384,000.
  - 48,000 Hz, 140 BPM, same loop: jumps every 82,286 samples.
  - 44,100 Hz, 140 BPM, Play from 0: no jump at beat 4 (75,600), then jumps at 151,200, 226,800
    and 302,400.
  - Loop 2 to 2 + 10/3 at 48,000 Hz, 120 BPM: jumps at 128,000, 208,000 and 288,000.
  - Play from 10 with loop 4 to 8: no jump.
- **S.** A jump does not restart a playing session clip. Later clip-event beats shift by
  minus (loop end − loop start) and are placed from the new anchor. Placing them
  independently as if no song jump had occurred can differ by one sample because
  each anchor rounds its own placement. The released loop cases give the same
  samples under both readings; that agreement is not a general identity (review F8
  in the [handoff plan](playback-core-handoff-plan.md#findings-while-staging)).

### REQ-PLAYBACK-CORE-007 — launch request and grid (settles SPEC-CLIP-LAUNCH A1)

- **S.** A press on a session clip's launch button sends the engine a quantized launch, as does
  the scripting call `ClipSlot.fire()` without arguments. The launch has no explicit time, fire
  velocity 1, no legato and no quantization override. Explicit times come only from follow
  actions, scenes and other paths outside T1.
- **S-cond (A4).** The grid is chosen as follows:
  - a clip `LaunchQuantisation` k ≥ 2 uses grid value k − 1 with the clip's own time signature
    (REQ-CLIP-LAUNCH-016);
  - Global (0, and a stored −99) uses the set's global quantization with the song's time
    signature in effect at the request;
  - None (clip value 1, or Global with global None) and out-of-range values give no grid.

  The grid length is REQ-CLIP-LAUNCH-015.
- **S.** This is the path that REQ-CLIP-LAUNCH-015 to 018 assumed (their A1). Which interface
  gestures besides the clip launch button and `ClipSlot.fire()` take it is U.

### REQ-PLAYBACK-CORE-008 — launch boundary and pre-delay

For a launch with grid g > 0, handled at request sample R while the transport plays:

- **X, path S.** The press beat t is the song beat at R rounded to the lattice. B is the
  boundary of REQ-CLIP-LAUNCH-017.
- **X, path S-cond (A3).** The track's player supplies a pre-delay o in beats:
  - **MIDI track.** o is 0.
  - **Audio track.** o is 0 unless a session audio clip is playing on the track and both it and
    the launched clip have `Fade` on. Then o is the smaller of the two clips' crossfade lengths.
  - **Crossfade length of a clip.** The smaller of half its region, LoopEnd − LoopStart in beats,
    and 4 ms in beats, 0.004 × T ÷ 60. For an unwarped clip the region is in seconds and counts
    as seconds × T ÷ 60.
  - **Examples.** 0.006 beat at 90 BPM, 0.008 at 120 BPM, 0.006666666666666667 at 100 BPM;
    0.00375 beat at 90 BPM for a 5 ms unwarped region.
- **S.** If B − t < o, the boundary moves to B + g. That happens only when the transport was
  already playing before sample R, that is, playback did not start at R. Otherwise, when
  B − t < o, o is reduced to B − t.
- **S.** So on a MIDI track a launch never moves to the next line, and a press exactly on a grid
  line launches on it (REQ-009).

### REQ-PLAYBACK-CORE-009 — launch activation and the replaced clip

- **S.** The launch takes effect at E = L(B − o), placed on a sample by REQ-002. When E is at or
  before t and the transport was already playing before R, it takes effect at R itself.
- **S.** The launched clip's position counts from song beat B: its start plays at B
  (REQ-011, REQ-017).
- **S.** The clip previously playing on the track is replaced at the sample where the launch
  takes effect. Its notes are ended (REQ-014), and its audio is cut short over the crossfade
  (REQ-020).
- **U.** The audio of either clip between E and B when o > 0. The immediate
  activation clause above has no independently graded observable in the released
  MIDI cases: o = 0, B ≥ t, and note events are placed from their beats.
  **T1 effect:** playback-core-v1 excludes nonzero pre-delay and crossfade
  activation until the clip output supplies an observable (handoff plan F6).

### REQ-PLAYBACK-CORE-010 — launch without a grid, and launch while stopped

- **S.** With no grid, B = L(t) and o = 0: activation occurs for the press beat.
  A first MIDI note is a beat event placed by REQ-002, so it may appear at R + 1
  after lattice rounding; it is not guaranteed to coincide with activation.
  The released no-grid cases put that first note at R.
- **S.** A launch while the transport is stopped first sets the song position, then computes B
  from that position and starts the transport (REQ-004). The position is the start beat if it is
  a locator, and otherwise the start beat's downbeat, the bar line at or before it. The downbeat
  helper is the one REQ-004 leaves untraced. With a start beat of 0, the launched clip starts at
  render sample 0, whatever its grid.
- **U.** Which notes are chased (started late) at such a start, and the order of notifications
  when the start beat is not on the grid. **T1 effect:** cases use start beat 0 and clips without
  a note spanning their start.

### REQ-PLAYBACK-CORE-011 — MIDI clip region and position

- **D, S.** A session MIDI clip's playback depends on four values:
  - start S = L(`Loop/LoopStart` + `Loop/StartRelative`);
  - loop start Ls = `Loop/LoopStart`;
  - loop end Le = `Loop/LoopEnd`;
  - looped, from `Loop/LoopOn`.

  `OutMarker`, `HiddenLoopStart`, `HiddenLoopEnd`, `CurrentStart` and `CurrentEnd` do not affect
  it. All 1,252 shipped MidiClips are warped (`IsWarped` true). A MIDI clip with `IsWarped` false
  is U.
- **X.** For a clip whose start plays at song beat B, the clip time at song beat B + d is
  L(S + d).
  - **Looped.** Once that reaches Le, it is folded into [Ls, Le): whole loop lengths Le − Ls are
    removed, with the remainder computed exactly and a result equal to Le read as Ls. It is then
    rounded to the lattice.
  - **Unlooped.** The clip ends when the clip time reaches Le.
  - **Start below the loop.** S < Ls plays through to Ls and then loops.
  - **Start above the loop.** S ≥ Le folds into the loop: start 3.5 with loop 1 to 3 begins at
    clip time 1.5.
  - **X results.** 234 inputs over three functions are bit-equal to these rules in binary64.
- **S.** A looped clip's first pass runs from B to W₁ = L(B + Le − S). Each later pass starts
  where the previous one ends and lasts Le − Ls: pass k + 1 runs from W_k to L(W_k + Le − Ls).
  A note at clip time c sounds at L(B − S + c) in the first pass (S-cond (A1)), and at
  L(W_k − Ls + c) in pass k + 1.

### REQ-PLAYBACK-CORE-012 — MIDI note events

- **S.** Each MIDI key that has notes plays through its own monophonic player, shared by the
  track's clips.
- **X, path S.** For each enabled note, in stored order, the key's player sends:
  - a note-on at its `Time` with its `Velocity` (binary32, unrounded: 63.5 is sent as 63.5);
  - a note-off at L(`Time` + `Duration`) with its `OffVelocity`.

  A zero-length note sends its note-off one lattice step after its note-on.
- **X.** Some notes are not sent:
  - a note with `IsEnabled` false;
  - a note whose `Time` equals the previously sent note's `Time` on the same key;
  - a zero-length note followed on the same key by a note at the same `Time`.
- **U.** Notes that overlap an earlier note on the same key. The player's event list is then out
  of time order, and its search over that list is undefined. 261 shipped notes do this.
  **T1 effect:** fixtures exclude same-key overlaps.
- **S.** A note-on sent while its key is still sounding (a retrigger) is preceded on the same
  sample by a note-off with velocity 64.

### REQ-PLAYBACK-CORE-013 — which notes sound in a pass

- **S-cond (A1).** A note starts only if its note-on falls inside the pass, at or after the
  pass's start beat and before its end. At a launch (REQ-009) or a loop wrap, a note already
  under way at S or at Ls is not started.
- **S-cond (A1).** A note-on exactly at Le never plays. A note-off exactly at Le is sent, with
  its own OffVelocity, before the wrap.
- **U.** Chasing of notes under way when the song starts or jumps, which happens only inside a
  range Live supplies. **T1 effect:** see REQ-010.

### REQ-PLAYBACK-CORE-014 — note-offs from cuts, stops and ends

Velocities are as sent to the instrument.

- **S-cond (A1).** A note still sounding at a loop wrap is cut at the wrap. Its velocity is 64
  when the clip's state at Ls is its start or a note-on at Ls. Otherwise it is the OffVelocity of
  the last note-off before Ls.
- **S-cond (A1).** When an unlooped clip ends (REQ-011), every note still sounding gets a
  note-off with velocity 64 on the clip's end sample.
- **S-cond (A1).** A clip stop (REQ-022), a transport Stop (REQ-005) or a replacing launch sends
  each note still sounding a note-off with velocity 64, at the stop or launch sample.
  - **Exception on a replacing launch.** A note keeps sounding when the new clip has a note on
    the same key in progress at its start.
- **U.** What the all-notes-off and panic callbacks that Live installs send in addition at
  transport Stop.

### REQ-PLAYBACK-CORE-015 — note velocity, deviation and probability

- **S-cond (A1, A2).** The note-on velocity sent to the instrument is v × (1 − a × (1 − f)),
  limited to 1 to 127. v is the stored velocity, a the clip's `VelocityAmount` and f the fire
  velocity (1 for a button press, REQ-007). With a = 0 the stored velocity is sent unchanged.
- **S, X.** `VelocityDeviation` and `Probability` take effect only when an application capability
  flag is set.
  - **Flag clear.** The deviation is 0 and the probability 1 (X).
  - **Flag set.** The deviation is limited so that v + deviation stays within 1 to 127, and the
    velocity is drawn uniformly from a per-player pseudo-random sequence. Probability ≤ 0 never
    plays, 1 always plays, and other values play at random. Probability groups also draw at
    random.
- **U.** Whether the flag is set for Live 12 Suite, and the random sequence's seed. **T1 effect:**
  fixtures use VelocityDeviation 0 and Probability 1 (or 0) with no groups, and VelocityAmount 0.
  The fixture clip "Velocity" of B1 has deviation 3 and is not used.
- **S.** With no groove (`GrooveId` −1) note times are unchanged.

### REQ-PLAYBACK-CORE-016 — per-note expression

- **S.** A note's per-note expression values at or before its start (`TimeOffset` ≤ 0) are
  rounded half away from zero and sent with its note-on.
- **S-cond (A1).** Later points are sent as timed events at L(note-on beat + `TimeOffset`).
- **U.** Values between points, and how the bundled instruments respond. **T1 effect:** timing
  only; audio belongs to the device specs.

### REQ-PLAYBACK-CORE-017 — unwarped audio clip: start, read step and read position

Applies to a session `AudioClip` with `IsWarped` false.

- **D, S.** `Loop/LoopStart`, `Loop/LoopEnd` and `Loop/StartRelative` are seconds of file time.
  In all 2,479 shipped unwarped clips, LoopEnd × `DefaultSampleRate` = `DefaultDuration`.
- **X, path S-cond (A3).** The transposition is t = `PitchCoarse` + 0.01 × `PitchFine` in
  binary32, limited to −48 to +48. The read step per output sample is the binary32 value of
  (binary32 2^(1/12)) raised to t, times file rate ÷ SR. It is held in 32.32 fixed point,
  rounded to the nearest.
  - **Examples.** A 44.1 kHz file at 48,000 Hz has step 0.91875 (fixed 3,946,001,203). +12
    semitones gives fixed `0x200001400`, slightly above 2. −12 semitones gives
    0.4999997317790985.
  - **X results.** 78 of 78 runs equal this rule.
- **S.** The first file frame is the integer part of file rate × LoopStart, with fraction 0. For
  LoopStart 0.1 s of a 48 kHz file that is frame 4,800; for 0.000015 s, frame 0. Output sample k
  of the clip reads file position first frame + k × step. The position is accumulated exactly in
  fixed point and quantized to 2⁻²⁴ frame (X).
- **S.** With pre-delay 0, output sample 0 of the clip is the sample where its launch takes
  effect (REQ-009).
- **U.** `StartRelative` ≠ 0, and a clip that starts later than its launch sample. **T1 effect:**
  fixtures use `StartRelative` 0.

### REQ-PLAYBACK-CORE-018 — unwarped audio clip: interpolation

- **S, X for the kernels.**
  - **Direct copy.** When the step is exactly 1, the output is the file's frames, unchanged
    apart from the clip gain (REQ-019), whatever `HiQ` says.
  - **HiQ off.** Linear interpolation between neighbouring frames.
  - **HiQ on.** A 16-tap Kaiser-windowed sinc interpolator (β = 5π, cutoff 0.95, 257 phases with
    linear interpolation between phases). When the step exceeds 1.125, the same filter runs at
    twice the rate and is followed by an 8th-order allpass half-band decimator.
  - **Cubic.** Not used for these clips.
- **X.** Outputs are the reference renders of the appendix. The direct, linear, cubic and 16-bit
  kernels are bit-equal to their stated models. The windowed sinc agrees with its binary64 model
  within 6e-8.
- **U.** For a 16-bit file, which internal sample type is used. The windowed-sinc output differs
  between the two by up to 4.9e-4; direct and linear outputs are identical. Also U: the padding at
  the file start, the file end and chunk edges, which affects about the first and last 8
  windowed-sinc outputs. **T1 effect:** HiQ-on resampled output is graded within 5e-4 absolute,
  away from the first and last 8 outputs, or not graded.
- **U.** Resampling quality as a measure (frequency response, aliasing, group delay). It is
  defined only by these kernels and their renders.
- **S-cond (A1).** arm64 fuses one operation in the linear kernel. **T1 effect:** interpolated
  linear outputs are graded with an absolute bound of 2 binary32 units in the
  last place of the largest source-frame magnitude read by the compared window.
  A bound relative to the output is unsafe near cancellation. Windowed-sinc
  outputs use 1e-6 absolute.

### REQ-PLAYBACK-CORE-019 — unwarped audio clip: gain, channels and sample format

- **X, path S-cond (A3).** The clip gain is `SampleVolume`, a linear factor. It is used within
  1.2e-7 relative of its binary32 value, and limited to 3.1622776e-4 (−70 dB) to 15.848933
  (+24 dB). `SampleVolume` 0 plays at −70 dB, not silence.
  - **Examples.** 0.5011872336 gives 0.5011872053146362; 10 gives 9.999999046325684; 20 gives
    15.848933219909668.
  - **Applied to.** Each interpolated value.
- **S, X.** A mono file plays identically on both channels.
- **S.** A 16-bit PCM file's frames are read as int16 ÷ 32,768.
- **U.** The scaling of 24-bit, 32-bit, AIFF and compressed files; files with more than two
  channels; gain or transposition changed during playback; `VelocityAmount` > 0. **T1 effect:**
  fixtures use 16-bit WAV, mono or stereo, with fixed values.

### REQ-PLAYBACK-CORE-020 — unwarped audio clip: fades and the file end

- **S-cond (A1, A3).** With `Fade` on:
  - the clip fades in from 0 over the smaller of 4 ms and half its region;
  - the gain follows 3x² − 2x³ of elapsed fraction x, evaluated at control points at most 32
    samples apart and ramped linearly between them;
  - a replacing launch cuts the old clip short over the smaller of the new clip's fade and 4 ms.

  With `Fade` off there is no fade: the gain is the clip gain from the first sample.
- **S-cond (A1).** Past the file's last frame the read position stays on that frame.
  - **Fade on.** Its value is held and ramped linearly to 0 over about 4 ms of file frames.
  - **Fade off.** The output is silence.
- **U.** The fade gains as exact sample values, and the fade-out at a stop. **T1 effect:**
  Fade-on outputs inside a fade are not graded sample by sample; fixtures use `Fade` off where
  output values are graded.

### REQ-PLAYBACK-CORE-021 — unwarped audio clip: tempo and end

- **S.** The read step does not depend on tempo. A tempo change does not change which file
  positions play.
- **S, X for the end beat.** An unwarped session clip plays its region once and stops,
  whatever `LoopOn` says. Its end is at the launch beat plus (LoopEnd − LoopStart) ÷ (the
  transposition ratio of REQ-017), in seconds converted at the tempo. That length is rounded up
  to a whole sample, then the end beat is lowered by half a lattice step and placed by REQ-002.
  A tempo change reschedules the end in seconds.
  - **Examples.** The shipped one-shot `Rim 3k Sharp.wav` (19,913 frames at 48 kHz, LoopEnd
    0.41485416666666669 s), launched at beat 4 at 120 BPM, plays 19,914 samples at 48,000 Hz:
    from 96,000 to 115,914, the last sample past the file's end. At 44,100 Hz it plays 18,296.
    `Rim DMX Vinyl.wav` (3,386 frames at 44.1 kHz) plays 3,686 samples at 48,000 Hz and 3,386 at
    44,100 Hz.
- **U (acceptance observable).** With `Fade` off and a region extending through
  the file, the silent output past the final frame does not reveal the clip's
  scheduled end. The end-beat calculation above is supported, but an exact
  end-sample acceptance case needs another observable, such as a subsequent
  launch whose timing depends on whether the clip remains active. PBC-061 and
  PBC-064 are not graded for the end sample, and REQ-021 is not released in
  playback-core-v1.
- **D.** No shipped unwarped clip has `LoopOn` true.
- **U.** Whether a stored `LoopOn` true on an unwarped clip has any other observable effect.
  **T1 effect:** fixtures use `LoopOn` false on unwarped clips.

### REQ-PLAYBACK-CORE-022 — stop buttons and quantized stop

- **S.** These are stop requests with no explicit time:
  - a track's Clip Stop button;
  - pressing an empty slot whose `HasStop` is true (S-cond (A5); with `HasStop` false the press
    does nothing);
  - Stop All Clips, which sends the request to every track.
- **S-cond (A4).** A stop uses the set's global quantization with the song's time signature,
  even when the playing clip has its own launch quantization.
- **S.** The stop is immediate, at the request sample, when any of these holds:
  - the transport is not playing;
  - the track has no clip playing;
  - the grid is None;
  - playback started on the request sample itself.

  A stop while the transport is stopped unassigns the track's clip, so the next Play does not
  restart it (REQ-023).
- **S, X for the arithmetic.** Otherwise the boundary, pre-delay and activation rules of REQ-008
  and REQ-009 apply, with these differences:
  - **MIDI track.** o is 0.
  - **Audio track.** o is the crossfade length of the playing clip if it has `Fade` on, else 0.
  - **When it applies.** The clip stops at E = L(B − o), placed by REQ-002, or at once when E is
    at or before t.
  - **X boundaries.** 5.3 at 1 Bar → 8; 9 at 2 Bars → 16; 2.1 at 1/4 → 3; 10/3 at 1/4T → 4; 4 in
    3/4 at 1 Bar → 6; 1.3 at 1/16 → 1.5.
- **S.** A track holds one pending launch or stop. A later request replaces it: a stop cancels a
  pending launch, and a launch replaces a pending stop.
- **S, X.** A warped unlooped clip (MIDI) ends by itself at its start beat + (Le − Ls). The test
  is inclusive.
- **U.** Whether a pending stop survives a transport Stop or a song position jump.

### REQ-PLAYBACK-CORE-023 — transport Stop and the playing clips

- **S.** A transport Stop does not unassign the playing clips. MIDI notes are ended (REQ-014).
  At the next Play the same clips play again.
- **S.** If the song position changes while stopped (Play with a new start beat, REQ-004), each
  assigned clip is re-based so that its start plays at the new position. A Continue keeps their
  positions.
- **U.** The exact first sample of each clip at such a restart, and chasing (REQ-013).
  **T1 effect:** cases grade only that the clip sounds again after Play, with start beat 0 and
  no note spanning the start.

## Timing and state

- **Units.** Song time and clip time in beats (quarter notes). Unwarped audio regions in
  seconds. Render positions in samples at SR.
- **Exactness.** Timing is sample-exact by REQ-002, with the P / P + 1 exception stated there.
  This replaces, for T1 grading, the ±1/64-beat tolerance proposed in SPEC-CLIP-LAUNCH.
- **Value tolerances.** These apply to audio values:
  - direct copies are bit-exact;
  - linear outputs use an absolute bound of 2 binary32 units in the last place of
    the largest source-frame magnitude read by the compared window;
  - windowed-sinc outputs within 1e-6 absolute (float source) or 5e-4 (16-bit source, REQ-018);
  - gains within 1.2e-7 relative.

  Tolerances are proposed, pending [Q-001](../questions.md#q-001-compatibility-targets).
- **Determinism.**
  - A render is deterministic for a given set, script and rate. The exceptions are REQ-002's
    P / P + 1 cases, and REQ-015 when its flag is set.
  - Buffer size does not change any result.
- **Persistent state.** Playback changes no stored field covered by the dependency specs.
- **Ordering.** Within a sample, events follow REQ-002's priorities. Requests are handled in
  script order at their request samples.
- **Cancellation.** A pending launch or stop is replaced by a later request on the same track
  (REQ-022).
- **Teardown.** Closing the set or ending the render is not specified.

## Acceptance cases

Expectations are X results of the original x86_64 functions or static derivations, as labelled.
None has been run against Live, and under ADR 0003 none will be. Kinds: P positive, B boundary,
G timing, A audio values, C cancellation, U unresolved (not graded).

Comparators:

- **Timing.** Every timing comparator is a render sample index, exact unless written "a or b"
  (REQ-002).
- **Audio.** Audio comparators apply to the clip's output before the track's devices and mixer.
- **Placements.** "Event at beat b" means any scheduled event at b, for example a note-on.
- **Common setup.** Unless stated: Play from start beat 0 with the arrangement loop off, nothing
  playing; and every launch is a launch-button press handled at the request sample of the
  stated song beat.

### Fixtures

Paths are relative to `Contents/App-Resources/` of the 12.4.3 bundle. A fixture is decoded,
changed only as stated, and re-encoded as gzip. A tempo edit sets the song tempo's `Manual`
value and its envelope event to the same value (REQ-TRANSPORT-STATE-012).

| ID | Shipped document | SHA-256 | Content used (D) |
| --- | --- | --- | --- |
| F1 | `Core Library/Lessons/Sets/Drums Lesson.als` (B1 of SPEC-CLIP-LAUNCH) | `66648e2054a014549df7681bc1fd52e35b9c575f771ba58b89ce7b6887ea630d` | 90 BPM, 4/4, global quantization 4 (1 Bar). Track 1 slot 1 MidiClip "Slide": key 51; eight enabled notes at clip times 0, 0.5 … 3.5, each 0.25 long, velocity 100, off velocity 64, deviation 0, probability 1; loop 0 to 4, LoopOn true, StartRelative 0; launch quantization 0; VelocityAmount 0; GrooveId −1 |
| F1-120 | F1 with tempo 120 | — | As F1 |
| F1-110 | F1 with tempo 110 | — | As F1 |
| F2 | `Core Library/Lessons/Sets/APC20 Demo.als` | `e54f00c53d9698343e37b88d8524d2776ae75533d2c5be673be667a65977c483` | 100 BPM, global quantization 4. Track 4 "4 Wavetable Pads" (audio) has session clips in slots 1 to 4, each `Wavetable Pads.wav` (44.1 kHz, 661,500 frames), Fade true. Edit for every case: slots 1 and 2 get `IsWarped` false, `LoopOn` false, `LoopStart` 0, `StartRelative` 0, `LoopEnd`, `OutMarker` and `HiddenLoopEnd` 10 (seconds) |
| F3 | `Core Library/Ableton Folder Info/Sample Reference.als` | `19d32f0fbdf84f6566a983be93d2ec4d08c69d9bd1cc2e7b3c88b66ed8b43ce1` | Tempo 121.199997, global quantization 4. Track 6 "6-Guitar Chord Jazz CMaj9" (audio, no devices) has two unwarped session clips, HiQ true, Fade false, LoopOn false, gain 1, launch quantization 0. Slot 102 holds `Samples/One Shots/Drums/Rim/Rim 3k Sharp.wav` (48 kHz mono 16-bit, 19,913 frames, SHA-256 `6ef0441cbf0d0b1961731f4012409f2fe44b2c25797e3edd78586100c04d338f`). Slot 129 holds `…/Rim DMX Vinyl.wav` (44.1 kHz mono 16-bit, 3,386 frames, `1802f16ae0692e4df42f63a05d1915d131359da74c5aa1d4127a4169b54abbd6`). Edit for every case: tempo 120 |

### Clock and transport cases

The draft tables name clock positions and jump samples, which are informative
arithmetic unless an output is scheduled there. In playback-core-v1, generated
probe clips make clock positions observable as note events; quantized presses
after a jump expose the looped song clock. A no-grid launch at a negative Play
start alone would not distinguish a clamped song clock, because its notes are
relative to that launch (handoff plan F9).

| Case ID | Requirement | Kind | Setup/action | Expected result/comparator | Provenance |
| --- | --- | --- | --- | --- | --- |
| PBC-001 | 001, 002, 004 | G | 48,000 Hz, 120 BPM | Events at beats 0, 0.25, 1, 4/3, 10/3, 4, 64: samples 0, 6,000, 24,000, 32,000, 80,000, 96,000, 1,536,000 | X |
| PBC-002 | 001, 002 | G | 48,000 Hz, 140 BPM | Beats 0.25, 1, 4, 7: 5,143, 20,572, 82,286, 144,000 | X |
| PBC-003 | 001, 002 | G | 44,100 Hz: 120 BPM; 128 BPM; binary32 121.2 BPM | 120: beat 0.25 → 5,513 and 10/3 → 73,500. 128: beat 1 → 20,672 and 1000 → 20,671,875. 121.2: beat 4 → 87,327 | X |
| PBC-004 | 001, 002, 003 | G | 48,000 Hz, tempo 93.33333587646484 (binary32 nearest 280/3; binary32 of 93.3333 is 93.33329772949219) | Beat 1 → 30,858; beat 7 → 216,000 | X |
| PBC-005 | 002 | B | 48,000 Hz, 90 BPM | Beat 1 → 32,000 or 32,001; beat 8 → 256,000 or 256,001; beat 8/3 → 85,334 | X (REQ-002 exception) |
| PBC-006 | 004 | G | 48,000 Hz, 140 BPM, start beat 3.5 | Sample 0 plays beat 3.5; beat 4.5 → 20,572; beat 19.5 → 329,143 | X |
| PBC-007 | 004 | B | Start beat −2 | Plays from beat 0 at sample 0 | S |
| PBC-008 | 005 | P | 48,000 Hz, 140 BPM; Stop at 30,000; Continue at 35,000 | Beat held after Stop: 1.4583333333333335. Beat at sample 65,000: 2.916666666666667. The next event at beat 3 is at 35,000 + 31,715 = 66,715 | X; the last value derived by REQ-001/002 from the X anchor |
| PBC-009 | 006 | G | 48,000 Hz, 120 BPM, loop 4 to 8 on, start beat 4 | Song beat returns to 4 at 96,000, 192,000, 288,000, 384,000 | X |
| PBC-010 | 006 | G | 48,000 Hz, 140 BPM, loop 4 to 8, start beat 4 | Jumps at 82,286, 164,572, 246,858, 329,144 | X |
| PBC-011 | 006 | G | 44,100 Hz, 140 BPM, loop 4 to 8, start beat 0 | No jump at 75,600; jumps at 151,200, 226,800, 302,400 | X |
| PBC-012 | 006 | G | 48,000 Hz, 120 BPM, loop start 2, length 10/3, start beat 0 | Jumps at 128,000, 208,000, 288,000 | X |
| PBC-013 | 006 | B | Loop 4 to 8, start beat 10 | No jump | X |
| PBC-014 | 003 | G | 48,000 Hz, 120 BPM; change to 90 BPM requested at beat 1 (sample 24,000) | Beat 2 at 56,000 or 56,001 | X (anchor), REQ-002 |
| PBC-015 | 003 | B | 48,000 Hz, 120 BPM; change to 90 BPM requested at beat 1.1 (sample 26,400) | Applies at beat 1.25 (sample 30,000); beat 2 at 30,000 + 24,000 = 54,000 or 54,001 | S, REQ-002 |
| PBC-016 | 006 | B | 48,000 Hz, 120 BPM; loop on with stored start 0 and length 0.5; start beat 0 | Loop length used as 1: song beat returns to 0 at 24,000, 48,000, 72,000 | S |

### Launch cases

F1 at 90 BPM, global 1 Bar, launches of "Slide" unless stated. "44.1" and "48" give the
activation sample at 44,100 and 48,000 Hz. PBC-023, PBC-061 and PBC-064 retain their IDs but have no graded expectation
after review. PBC-024 is instantiated at 44,100 Hz only.
The CLC IDs name the press and grid setup of the
SPEC-CLIP-LAUNCH grid case of that number, whose B is X.

| Case ID | Requirement | Kind | Setup/action | Expected result/comparator | Provenance |
| --- | --- | --- | --- | --- | --- |
| PBC-020 | 007–009 | G | Presses of CLC-031 to 040, 042, 044, 046, 048 to 051 and 062 (B a whole or dyadic beat) | 44.1: 29,400 × B exactly (CLC-031: 235,200; CLC-032: 470,400; CLC-046: 44,100; CLC-048: 7,350). 48: 32,000 × B or 32,000 × B + 1 | X (B), S (path), REQ-002 |
| PBC-021 | 007–009 | G | Presses of CLC-041, 043, 045, 047 (triplet B = 8/3, 4/3, 2/3, 1/3) | 44.1: 78,400, 39,200, 19,600, 9,800. 48: 85,334, 42,667, 21,334, 10,667 | X, S |
| PBC-022 | 008, 009 | B | Press of CLC-054 at t = 3.99 | 44.1: 117,600; 48: 128,000 or 128,001 | X, S |
| PBC-023 | 008, 009 | U | Slide already playing; launch Slide again by a press exactly at beat 8 (request sample 235,200 at 44.1) | Not graded: the relaunch coincides with its wrap and note events; their order relative to launch is U under REQ-002. An on-line press of an idle clip at beat 4 is covered in playback-core-v1 | U; prior S expectation withdrawn |
| PBC-024 | 008, 009 | B | Press of CLC-064 (1/4T, t exactly 10/3) | 44.1: 117,600 (B = 4). No integer request sample gives t exactly 10/3 at 90 BPM and 48 kHz, so the 48 kHz variant is not instantiated | X, S |
| PBC-025 | 007–009 | G | F1-120 at 48,000 Hz; press at t = 5.3 | 192,000 | X, S |
| PBC-026 | 010 | P | Slide set to launch quantization 1 (None); press at t = 5.3, request sample R | Activation at the press beat; the first note is placed from its lattice beat by REQ-002 and can be at R + 1. In the released cases it is at R | S |
| PBC-027 | 010 | P | Transport stopped, start beat 0; launch Slide | Transport starts; Slide's first note-on at render sample 0 | S |
| PBC-028 | 008, 009 | G | F2. Track 4 slot 1 launched by a press at t = 1 (no clip playing) | Starts at beat 4: 48: 115,200; 44.1: 105,840 | X (o = 0), S |
| PBC-029 | 008, 009 | G | F2. Slot 1 playing since beat 4; slot 2 launched by a press at t = 5.3 | Activation at E = 7.993333229270729: 48: 230,208; 44.1: 211,504. Slot 2's start counts from beat 8 | X, S |
| PBC-030 | 008, 009 | B | As PBC-029 with the press at t = 7.995, and separately exactly at beat 8 | B moves to 12; activation at 48: 345,408; 44.1: 317,344 | X, S |
| PBC-031 | 008 | B | As PBC-029 with slot 2's `Fade` false | Activation at beat 8: 48: 230,400; 44.1: 211,680 | X, S |
| PBC-032 | 008, 009 | U | As PBC-029 | Audio between activation and beat 8 unresolved (REQ-009) | U |

### MIDI clip cases

F1-120 at 48,000 Hz unless stated. Slide is launched by a press at beat 1, so B = 4, and is not
stopped unless stated. "On" and "off" are note-on and note-off of key 51; velocities are as sent.

| Case ID | Requirement | Kind | Setup/action | Expected result/comparator | Provenance |
| --- | --- | --- | --- | --- | --- |
| PBC-040 | 011–013 | G | Unedited | On (velocity 100) at 96,000 + 12,000k and off (velocity 64) at 102,000 + 12,000k for k = 0 … 7; pass 2 repeats from 192,000; no other events from Slide | X, S |
| PBC-041 | 011, 013 | B | `StartRelative` 0.125 | Note 0 not played in pass 1; first on at 105,000 (note 1); wrap at 189,000, where note 0 plays (on 189,000, off 195,000) | X, S-cond |
| PBC-042 | 012, 014 | B | Note at 3.5 lasts 1 beat | Off with velocity 64 at 192,000, then note 0's on at 192,000 | S-cond |
| PBC-043 | 012 | B | Note at 0.5 has duration 0 | On at 108,000; off at 108,001 | X, S |
| PBC-044 | 011, 014 | P | `LoopOn` false | One pass; last off at 186,000; Slide ends at 192,000; nothing after | X, S |
| PBC-045 | 011, 014 | B | `LoopOn` false; note at 3.5 lasts 1 beat | Off with velocity 64 at 192,000 (the clip's end) | S-cond |
| PBC-046 | 012 | N | Note at 1.0 has `IsEnabled` false | No on or off at 120,000 or 126,000; others as PBC-040 | X, S |
| PBC-047 | 012 | B | A ninth note added at clip time 4 (= Le), duration 0.25 | Never played | S-cond |
| PBC-048 | 014, 022 | P | Note at 0.5 has duration 0.4; global 1/16; stop button pressed at beat 4.6 | Off with velocity 64 at 114,000 (beat 4.75), not at 117,600 | X (B), S-cond |
| PBC-049 | 002, 011 | G | F1-110 at 44,100 Hz | First on at 96,219 (beat 4; spb 24,054.545454545456) | X |
| PBC-050 | 002 | B | F1 (90 BPM) at 48,000 Hz | First on at 128,000 or 128,001 | X, REQ-002 |
| PBC-051 | 015 | U | Slide with VelocityDeviation 10 | Not graded (REQ-015) | U |

### Audio clip cases

F3 at 48,000 Hz. A clip is launched by a press at beat 1, so it starts at beat 4, render
sample 96,000 (X, S). Values are the clip's output; x_k is the file's 16-bit frame k ÷ 32,768.

| Case ID | Requirement | Kind | Setup/action | Expected result/comparator | Provenance |
| --- | --- | --- | --- | --- | --- |
| PBC-060 | 017–019 | A | Slot 102 (48 kHz file, HiQ on) | Output 96,000 + k equals x_k on both channels for k = 0 … 19,912, bit-exact. First values: 0.000274658203125, 0.0008544921875, 0.00067138671875, −0.000213623046875. Output 115,913 is 0 | X (kernel, both HiQ settings), S |
| PBC-061 | 021 | U | As PBC-060 | Informative scheduled end: 115,914; at 44.1 kHz, 106,496. Not graded: past-file silence with Fade off cannot distinguish the clip end | X (end beat), S; end-sample observable U |
| PBC-062 | 017, 018 | A | Slot 129 (44.1 kHz file) with `HiQ` false | Output 96,000 + k reads position k × 3,946,001,203 ÷ 2³² frames. First values: 0.0, 0.055066678673028946, 0.20224608480930328, 0.3418603837490082, 0.41899415850639343, 0.45862865447998047 | X; arm64 within the absolute window bound of REQ-018 |
| PBC-063 | 018 | A | Slot 129, `HiQ` true | Outputs 96,008 onward within 5e-4 of the float-sample reference render (`audio/results/shipped.json`, which begins −0.000350424088537693, 0.0507950484752655, 0.19911181926727295); the first 8 outputs are not graded | X (both sample types), U (which one, and padding) |
| PBC-064 | 021 | U | Slot 129 | Informative scheduled end: 99,686. Not graded: past-file silence with Fade off cannot distinguish the clip end | X, S; end-sample observable U |
| PBC-065 | 017, 018 | A | Slot 102, `PitchCoarse` 12, `HiQ` false | Step fixed `0x200001400`. First values: 0.000274658203125, 0.0006713856710121036, −0.0016479495679959655, −0.0014343236107379198, 0.0009765676222741604, 0.002319333143532276 | X |
| PBC-066 | 019 | A | Slot 102, `SampleVolume` 0.5011872336; and separately 0, 10, 20 | Output = x_k × g in binary32, with g = 0.5011872053146362; 3.1622775713913143e-4; 9.999999046325684; 15.848933219909668 | X (gain), S |
| PBC-067 | 017 | B | Slot 102, `LoopStart` 0.1 (and `LoopEnd` unchanged) | Output 96,000 is frame 4,800 | S |
| PBC-068 | 021 | P | Slot 102; tempo changed to 90 at beat 4.25 (sample 102,000) | Outputs still equal x_k (unchanged read positions) | S |
| PBC-069 | 020 | U | Slot 102 with `Fade` true | Fade-in over 192 samples of shape 3x² − 2x³; values not graded | S (shape), U (values) |

### Stop cases

F1 at 44,100 Hz (exact) unless stated. Slide is playing, launched by a press at beat 1 under the
case's quantization settings, unless stated. "48" gives the value at 48,000 Hz where it
differs.

| Case ID | Requirement | Kind | Setup/action | Expected result/comparator | Provenance |
| --- | --- | --- | --- | --- | --- |
| PBC-080 | 022 | G | Track stop button at t = 5.3 (1 Bar) | Slide stops at 235,200 (48: 256,000 or 256,001) | X (B), S |
| PBC-081 | 022 | G | Global 2 Bars; stop at t = 9 | 470,400 | X, S |
| PBC-082 | 022 | G | Global 1/4; stop at t = 4.1 | 147,000 (beat 5) | X, S |
| PBC-083 | 022 | G | Song 3/4 (signature edit as SPEC-CLIP-LAUNCH fixtures); Slide launched by a press at beat 1 (B = 3); stop at t = 4 | 176,400 (beat 6) | X, S |
| PBC-084 | 022 | B | Slide's launch quantization 8 (1/4); global 1 Bar; stop at t = 5.3 | 235,200 (beat 8: the stop uses the global grid) | S, X |
| PBC-085 | 022 | B | Stop at t = 7.996 (MIDI) | 235,200 (no move to beat 12) | S, X |
| PBC-086 | 022 | B | Stop pressed exactly at beat 8 | At the request sample | S |
| PBC-087 | 022 | P | Global None; stop at request sample R | At R | S |
| PBC-088 | 022 | P | Stop All Clips at t = 5.3 | Slide stops at 235,200 | S, X |
| PBC-089 | 022 | C | Slide not playing; launch at t = 5.3 (pending for beat 8), then track stop at t = 6 | Stop at once; Slide does not start at beat 8 | S |
| PBC-090 | 022 | P | Slide `LoopOn` false, launched by a press at beat 1 | Ends by itself at 235,200 (beat 8) | X, S |
| PBC-091 | 022 | G | F2 at 48,000 Hz; slot 1 playing since beat 4; track stop at t = 5.3 | Stops at 230,208 (44.1: 211,504) | X, S |
| PBC-092 | 022 | B | As PBC-091 with the press at t = 7.995 | Stops at 345,408 (beat 12 − o) | X, S |
| PBC-093 | 022 | B | As PBC-091 with slot 1's `Fade` false | Stops at 230,400 | X, S |
| PBC-094 | 022 | N | F2; an empty slot (slot 5, `HasStop` true) pressed at t = 5.3 while slot 1 plays | As PBC-091 | S-cond (A5) |
| PBC-095 | 023, 005 | P | Transport Stop at beat 6; Play from start beat 0 | Slide sounds again after Play; first sample not graded | S, U |
| PBC-096 | 022, 023 | N | Transport Stop at beat 6; track stop button; Play from start beat 0 | Slide does not sound | S |

Omitted kinds:

- Malformed documents belong to the storage specs.
- Teardown is not specified.
- The U-only parts (REQ-009 crossfade audio, REQ-013 chasing, REQ-015 random draws, REQ-016
  values, REQ-020 fade values) have no graded cases.

## Open questions

Proposed for [Q-022](../questions.md) (playback core), with the clip-launch items updated in
[Q-017](../questions.md#q-017-clip-launch-timing-and-launch-modes):

- **The P / P + 1 class of REQ-002.** It depends on the engine's absolute sample counter. No
  static route settles it; T1 accepts either value.
- **Play's start beat after opening a set (REQ-004).** Static route: whether loading
  `CurrentTime` writes the insert marker, and the bar-line helper (x86_64 `0x102814eb0`).
- **The second Stop (REQ-005).** Static route: the song setter the Stop body reaches.
- **Delivery of actions relative to the audio buffer.** No static route; the render script
  defines the request sample.
- **MIDI.**
  - Same-key overlaps (REQ-012); no static route short of the undefined search.
  - The capability flag and seed (REQ-015). Static route: the writer of the flag.
  - Chasing ranges (REQ-013, REQ-023).
- **Audio.**
  - Crossfade content between E and B (REQ-009).
  - The 16-bit sample type. Static route: the caller of `OChunkedSample::Init`.
  - Chunk padding, other file formats and fade values (REQ-018 to 020).
  - Audio `StartRelative` ≠ 0 (REQ-017); MIDI offsets are covered by REQ-011.
  - An observable for the unwarped end sample with Fade off (REQ-021).
- **Stops.** The all-notes-off callbacks, and pending stops across a transport Stop or a jump
  (REQ-014, REQ-022).
- **Documentation not retained.** What the user's Play, Stop and Continue controls do and which
  gestures reach the launch path (REQ-004, 005, 007). Ableton's manual would show these. Each
  stays U until a retained source exists.

## Analyst evidence appendix

Analysis-only. Do not copy into a handoff. Canonical evidence:
[playback core research](../research/playback-core.md). Retained run:
[t13-playback-v1](../../analysis/ableton-live-12.4.3/r2/t13-playback-v1/manifest.json).

**Images.**

| Image | SHA-256 | Base |
| --- | --- | --- |
| Live x86_64 slice | `1bae9a97…be999b0` | `0x100000000` |
| Live arm64 slice | `3a99ceea…d1c383cfad` | `0x100000000` |
| x86_64 Live Engine (named) | `028df12e…5843de` | 0 |

**Corpus excerpts.** Each subdirectory keeps them as `excerpts.jsonl` or
`corpus-excerpts.jsonl`, with chunk, offset and line SHA-256: transport 131 records, launch 120,
midi 145, audio 188, stop 192.

| Requirement | Functions (Engine / Live x86_64 / Live arm64) | Evidence and strength |
| --- | --- | --- |
| 001, 002 | `DoSetTempo` `0x10c2e0` / `0x101adb640` / `0x101ab2d50`; `ProcessNextEvents` `0x10f540` / `0x101ade8a0` / `0x101ab5cec`; `TStatus::PredictedLongSampleTime` `0x1096d0` / `0x101ad8a30` / `0x101ab05cc`; `ScheduleAbsoluteBeatEvent` `0x10a400` / `0x101ad9760` / `0x101ab10ec` | Engine ↔ x86_64 identical modulo addresses (`transport/matching-eng-x86.txt`). X: `transport/results/fire.json` (1,216 rows), `sweep.json` (4,000 calls). Classification: `plus_one_check.json`. arm64 `fmadd` and `fcvtps` (`transport/disasm-arm64.txt`). Buffer splitting: `OEngineDomain::CalcAudio` (S) |
| 003 | `OnTempo` `0x10f370` / `0x101ade6d0` / `0x101ab5b70`; tempo quantizer `0x8a30a0` / `0x1021d0620` / `0x1020f1db4`; tempo graph x86_64 `0x102774df0` | S; X `transport/results/tempo_change.json`. arm64 graph builder not located |
| 004, 005 | `SetPlaying` `0x10cff0` / `0x101adc350` / `0x101ab3a4c`; `SetBeatTime` `0x10d640` / `0x101adc9a0` / `0x101ab4038`; Live Start body arm64 `0x10276a7b0`; selection start x86_64 `0x10280fcc0`; sync x86_64 `0x1028a21d0` | S; X `fire.json`, `stop_resume.json` |
| 006 | `SetLoop` `0x10cb20` / `0x101adbe80` / `0x101ab3594`; `ProcessLoopBracePassed` `0x10f9d0` / `0x101aded30` / `0x101ab60c8`; `OnSongPositionJumped` `0x1371a0` / `0x101b06500` / `0x101adb6b0` | S; X `transport/results/loop.json` |
| 007 | `OFireManager::SRegisterMessages` `0x14ee00` / `0x101b1e150` / `0x101af22f4`; `FireClip` `0x14d520` / `0x101b1c870` / `0x101af0cbc`; `CalcLaunchQuantization` `0x12a9f0` / `0x101af9d50` / `0x101acffa4`; AClipSlot slot +0x258 x86_64 `0x10257bf70`, arm64 `0x10245c72c`; `OSlotFireData.Create` sender x86_64 `0x10257e880`, arm64 `0x10245efa0` | S (`launch/matching.tsv`, `x86-fireclip-caller-tree.txt`) |
| 008, 009 | `PrepareClipFire` `0x12ab50` / `0x101af9eb0` / `0x101ad0130`; `RequestedPredelaySongBeatForClip` `0x12c1a0` / `0x101afb500` / `0x101ad1418`; `SCrossfadeDurBeat` `0x9a45d0` / `0x102278eb0` / `0x102188f34`; `OAudioClipFadeTime::SInitInstance` `0x9a7ea0` / `0x10227c780` / `0x10218c488`; `SongWasPlayingBeforeCurrentSample` `0x12a850` / `0x101af9bb0` / `0x101acfe68`; `OAsyncClipFireManager::Fire` `0x12c380` / `0x101afb6e0` / `0x101ad15e8` | X `launch/results.json` (16 of 16); cases `launch/samples.json` |
| 010 | `OFireManager::FireClip` (stopped branch) | S, Engine and both slices (`launch/matching.tsv`) |
| 011 | Clip writer x86_64 `0x10257ecd0`, arm64 `0x10245f420`; `ALoop` registry x86_64 `0x102691be0`, arm64 `0x10256b7e4`; `SCalcCurrentPos` `0x143520` / `0x101b12870` / `0x101ae6f54`; core `0x145c80` / `0x101b14fd0` / `0x101ae9360`; `SetupRecurringLoopEvents` `0x144110` / `0x101b13460` / `0x101ae7984` | X `midi/results/clip-position.json`; D `midi/scan-clip-loops.txt` |
| 012 | Builder x86_64 `0x102a13f20`, arm64 `0x1028cf5c0`; `SendNewNoteOn` `0x1afa60` / `0x101b7ece0` / `0x101b486ec` | X `midi/results/note-events.json` (12 cases; pool allocator replaced by malloc, flag poked, group lookup stubbed under gdb) |
| 013, 014 | `OMidiNoteAutomationPlayer::Process` `0x1b0150` / `0x101b7f3d0` / `0x101b48da8`; `ShouldChaseNoteEvent`, `ChaseNoteEvent`, `GenerateArtificialNoteOff` (both slices); `EventPriority` x86_64 `0x101b7e6c0` (table `0x105db2460`); `OnDeactivateAutomation` x86_64 `0x101b7fbc0` | S; S-cond for x86_64-only functions |
| 015 | `HandleNoteOn` `0x1a8d00` / `0x101b78010`; `ProbabilisticallySendNoteOn` `0x1b0a90` / `0x101b7fd10` / `0x101b49678`; `SendNoteOn` `0x1b0bd0` / `0x101b7fe50` / `0x101b497a8`; flag reader x86_64 `0x1014f9cc0` | S, X (builder runs with flag 0 and 1) |
| 017 | Live sender x86_64 `0x102904c10`, arm64 `0x1027cade8`; `SSemitonesToInc` `0xaa7290` / `0x10236f1f0` / `0x10225a2bc`; `StartFileSmpl` `0xaa8750` / `0x1023706b0` / `0x10225b4e8`; `SQuantizePosFileSmpl` `0xa92b50` / `0x10235b910` | X `audio/results/inc.json` (78), `quant.json` (8); D `audio/shipped-unwarped-clips.jsonl` |
| 018 | `CalcPri…` kernels (`audio/matching.tsv`); interpolation choice x86_64 `0x1028f76a0`, arm64 `0x1027bd748`; `NFirInterpolation::SInitO` `0x520260` / `0x101e95890` | X `audio/results/kernels.json`, `fir_formula.json`, `shipped.json`; arm64 fused-operation scan `audio/arm64-fp-kernels.txt` |
| 019 | Clip-gain mapping x86_64 `0x102683d10` to `0x102683da0`; `OVuMeterMath::SControlLevel` `0x11e130` / `0x101aed490` | X `audio/results/gain.json` |
| 020 | `ScheduleFade` `0x9ab830` / `0x102280110` / `0x10218fc08`; `UpdateGainRamp` `0x9aba80` / `0x102280360` / `0x10218fe24`; `CutShortOldNotes` `0x9adce0` / `0x1022825c0` | S; S-cond |
| 021 | `ScheduleLoopOrUnloopedClipEnd` `0x136c20` / `0x101b05f80` / `0x101adb0b8`; `SBeatTimeForClipTime` `0x19d230` / `0x101b6c540` / `0x101b36d14`; `OnUnloopedClipEnd` `0x137770` / `0x101b06ad0` / `0x101adbbf0`; `OAudioClip` vtable slot +0x18 = `LoopLengthInSecs` (Engine vtable `0x1781510`) | S; X `end/results.json` and `stop/results/stop.json` |
| 022 | `ATrackDevice::OnStop` x86_64 `0x10285cce0`, arm64 `0x102728b88`; track slot +0x3d8 x86_64 `0x102842c50`, arm64 `0x1027104dc`; main track x86_64 `0x10269d2d0`, arm64 `0x1025770bc`; `FireScene` `0x14dca0` / `0x101b1cff0` / `0x101af1358`; `SIsPastEndOfUnloopedSlotClip` `0x1481c0` / `0x101b17510` / `0x101aeb668` | S (`stop/matching.tsv`); X `stop/results/stop.json` |
| 023 | `OSequencer::SetSongPlaying`; `OnSongPositionJumped` stopped branch x86_64 `0x101b06500`, arm64 `0x101adb6b0` | S (Engine and both slices for the jump handler) |

**x86_64-only functions under A1.** These were matched to x86_64 only:

- `EventPriority`;
- `OnDeactivateAutomation`;
- the activation-origin table;
- `HandleNoteOn`;
- `OClipActionEvents` (priority 7);
- the `CalcPriT16…` and FIR2X kernels;
- `SQuantizePosFileSmpl`;
- `CutShortOldNotes`;
- `OPlayerEndEvent` and `OFadingPlayerBrain`.

**Harness.** Each subdirectory has a copy of `tools/xexec` that adds only `poke`. The copies
were built to `/var/tmp/sound-analysis/xexec-t13-{transport,launch,midi,audio}/xexec`. The
`stop/` and `end/` runs used the unchanged loader, built to `xexec-t13-stop` and `xexec-t13-end`.
Imports called, all bound to glibc:

- transport `memcpy`;
- MIDI `bzero` and `fmod`, which is exact in every IEEE library;
- audio `powf` (the read step), `exp` and `sinf` (the FIR table), `exp10f` (the gain mapping),
  and allocation and guard routines.

Apple's `powf`, `exp`, `sinf` and `exp10f` were not available. REQ-017 to 019 therefore bind to
glibc's results, which is one reason for their tolerances. No process exceeded 256 calls.

**Derived values.**

- Sample indices in the cases come from the X-confirmed placement rule with the anchor at render
  sample 0 and counter 0 (`launch/samples.json`, `stop/results/samples.json`,
  `midi/results/cases.json`, `end/results.json`). Each P / P + 1 case lists both values.
- PBC-008's beat-3 sample and PBC-015's values were derived by hand from REQ-001 and REQ-002.
- The F2 and F3 activation samples assume the clips' global quantization 1 Bar (REQ-CLIP-LAUNCH-015, X).

**Corrections to other pages.** These are listed on the
[research page](../research/playback-core.md#corrections-to-existing-pages): SPEC-CLIP-LAUNCH
REQ-017 to 019, 022 and its tolerance; transport transitions T-01; SPEC-TRANSPORT-STATE timing
and REQ-009; the extracted-execution triage; SPEC-MIDI-NOTE-STORAGE REQ-007 and 010; and
SPEC-WARP-MARKERS REQ-009.

## Revision and handoff

| Revision | Date | Change |
| --- | --- | --- |
| 1 | 2026-10-18 | First draft from packet T1.3. 23 requirements: 3 with D parts, all with S parts, 13 with S-cond parts, 15 with X parts, 19 with U parts (001, 003, 006 and 008 have none). A1 of SPEC-CLIP-LAUNCH settled for the Trigger fire path. 68 case IDs: 63 fully graded (8 accept P or P + 1 at 48,000 Hz: PBC-005, 014, 015, 020, 022, 024, 050, 080), 2 partly graded (PBC-063, 095), 3 not graded (PBC-032, 051, 069) |

| 2 | 2026-10-19 | Reconciles playback-core-v1 review: immediate E ≤ t activation lacks an independent observable; PBC-023 relaunch ordering and PBC-061/064 end samples ungraded; PBC-024 limited to 44.1 kHz; audio StartRelative remains open independently of the MIDI rule. 68 case IDs: 60 fully graded, 2 partly graded (063, 095), 6 ungraded (023, 032, 051, 061, 064, 069); seven rows accept P or P+1 at 48 kHz (005, 014, 015, 020, 022, 050, 080). The immutable release pins parent r1 and carries its reviewed corrections; this draft records them as r2. |

The released finite clauses and cases are identified below; all U-dependent
behavior remains outside the handoff.

The near-boundary and pre-delay clauses of REQ-008 replace SPEC-CLIP-LAUNCH REQ-017's
unknown clause. SPEC-CLIP-LAUNCH r5 and SPEC-WARP-MARKERS r5 apply the reviewed corrections
and point here.

Released locally 2026-10-19 as [playback-core-v1](../../handoff/playback-core-v1/README.md):
92 cases, partial REQ-001 to 015 and 017 to 020, approved with clarifications
by a separate reviewer. Requirements 016 and 021 to 023 remain unreleased.
