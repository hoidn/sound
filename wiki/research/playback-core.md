---
id: RESEARCH-PLAYBACK-CORE
type: research
status: draft
updated: 2026-10-21
access: analysis
target: Ableton Live 12 Suite 12.4.3 (Live arm64 and x86_64 slices; x86_64 Live Engine as named donor)
---

# Playback core: clock, transport, launch, clip playback (T1.3)

**Question.** For the offline render of [ADR 0004](../decisions/adr-0004-target-scope-t1.md)
(target T1), what does 12.4.3 do, in output samples at a stated sample rate, for transport
Play, Stop, Continue, the song loop and tempo; for a session clip launch under global
quantization; for MIDI clip notes; for an audio clip with warping off; and for stopping clips?
Is the launch arithmetic of [SPEC-CLIP-LAUNCH](../specs/clip-launch.md) the one the scheduler
uses (that spec's assumption A1)?

**Answer (static and extracted execution, draft).** The engine is sample-accurate and its
timing is pure arithmetic over a per-tempo anchor, so most of the timing questions have exact
answers:

- **Clock.** Samples per beat is (rate ÷ tempo) × 60 in binary64 with the binary32 song
  tempo. A beat event fires on the first sample at or after its beat. One exception cannot be
  settled. When the exact position is a whole number of samples and the binary64 product
  exceeds it, Live sometimes fires one sample later. That depends on an engine sample counter
  that a render cannot observe.
- **Transport.** Play starts on its start beat at the first rendered sample. Stop freezes the
  position and Continue resumes from it. The song loop jumps on the loop-end sample. A tempo
  change while playing waits for the next 1/16-note line.
- **Launch.** A1 is settled for the Trigger fire path: a clip-slot press reaches the X2
  boundary arithmetic with no explicit time. The near-boundary offset, which earlier pages
  called run-time only, is the audio crossfade length (0 for MIDI). It is reproduced by
  extracted execution.
- **MIDI clips.** The clip position, per-key note lists and pass windows are settled. Notes that
  span the start or the loop start are not started.
- **Audio clips, warping off.** The read step, start frame, gain, mono handling and the three
  interpolation kernels are settled by X. An unwarped session clip plays its region once.
  Fades are settled in shape only, and resampling only as reference kernels.
- **Stopping.** Stop presses use the global grid and the same boundary rule; transport Stop keeps
  the playing clips assigned.

The behavioral contract is [SPEC-PLAYBACK-CORE](../specs/playback-core.md) revision 2.

Evidence: [t13-playback-v1](../../analysis/ableton-live-12.4.3/r2/t13-playback-v1/manifest.json).
- **Area subdirectories.** `transport/`, `launch/`, `midi/`, `audio/` and `stop/` each hold
  their scripts, raw runs (`raw/` or `raw-runs.jsonl`), results, corpus excerpts
  (`excerpts.jsonl` or `corpus-excerpts.jsonl`), disassembly extracts and a matching table.
- **`end/`.** Holds the X run of the unwarped clip end for the shipped one-shots.
- **Top level.** `plus_one_check.py` and `plus_one_check.json` classify the one-sample
  deviations. `run.sh` regenerates everything, and `lookup.py` is the corpus reader.

Nothing was run against Live.

## Method

- **Donor names.** The x86_64 Live Engine bundle (SHA-256 `028df12e…5843de`, base 0) is a ReWire
  device build of the engine with 75,348 named functions
  ([x86_64-only bundles](x86-only-bundles.md#consequence-for-analysis-a-named-copy-of-lives-engine-code)).
  Its scheduler, fire manager, clip players and warper classes carry their C++ names.
- **Matching to Live x86_64.** Within each engine region, the Engine functions sit in Live
  x86_64 (SHA-256 `1bae9a97…be999b0`) at one constant address delta. The deltas are
  `0x1019cf360` for the scheduler and fire-manager region and `0x1019cf280` to `0x1019cf350`
  for the note players and clip position.
  - All 39 scheduler and engine-domain pairs cited were compared instruction by instruction and
    are identical modulo addresses (`transport/matching-eng-x86.txt`).
  - In the MIDI region, 322 of 323 functions match with 12 of 12 same-size neighbours
    (`midi/match-eng-x86.tsv`).
  - Live-side functions (interface and document classes) are not in the Engine. They were
    found through the symbolized `CallMemberFunc<…>` wrappers, message descriptors and vtable
    slots of Live x86_64.
- **Matching to Live arm64** (SHA-256 `3a99ceea…d1c383cfad`). Through named wrappers, call order,
  shared constants (LCG constants, the 4 ms fade default and its debug-option hash, the lattice
  constants) and message descriptors. Each subdirectory's `matching.tsv` records how. Where a
  function was found only in x86_64, the claim is marked "x86_64 only" below and in the spec.
- **Extracted execution** ([ADR 0003](../decisions/adr-0003-no-reference-execution.md#extracted-execution-of-original-code)).
  The transport, launch, midi and audio areas each have a copy of
  [tools/xexec](../../tools/xexec/xexec.c) that adds only `poke`. The stop and end runs use the
  unchanged loader. Each loader is built outside the tree to
  `/var/tmp/sound-analysis/xexec-t13-<area>/xexec`. Live
  x86_64 functions were called with hand-built objects whose fields come from the static
  reading; the reading and every stub are recorded beside each run. No process exceeded 256 calls.
- **Not used.** Ghidra (no new analysis), the arm64 slice under emulation, any Live process, and
  published Ableton documentation, of which none is retained in `raw/`.

## Findings

Labels: S = static derivation, both Live slices unless "x86_64 only" is stated; X = extracted
execution of the Live x86_64 function; U = unknown. "Lattice" means rounding to the
1/3,843,840-beat grid of REQ-CLIP-LAUNCH-013.

### 1. Clock: beats to samples

- **S.** The scheduler holds an anchor (sample n_a, beat b_a). Samples per beat are
  spb = (SR ÷ T) × 60.0 and beats per sample 1.0 ÷ spb, both binary64. SR is the integer engine
  rate and T the binary32 tempo. `OScheduler::DoSetTempo` is Engine `0x10c2e0`, x86_64
  `0x101adb640`, arm64 `0x101ab2d50`; the constants 60.0 and 1.0 are Engine `0x15caf58` and
  `0x15bac48`. The running beat at sample n is b_a + (n − n_a) × bps.
- **S.** A beat event's time is first rounded to the lattice (`ScheduleAbsoluteBeatEvent`, Engine
  `0x10a400`, x86_64 `0x101ad9760`, arm64 `0x101ab10ec`). Events at one beat are ordered by
  priority. The event fires at sample ⌈fl(fl(fl(b − b_a) × spb) + n_a)⌉ (`ProcessNextEvents`,
  Engine `0x10f540`, x86_64 `0x101ade8a0`, arm64 `0x101ab5cec`; `TStatus::PredictedLongSampleTime`,
  x86_64 `0x101ad8a30`). During the event the current beat reads exactly b. arm64 forms the same
  value with one `fmadd` and `fcvtps`.
- **X.** 1,216 placements in `transport/results/fire.json` cover rates 44.1, 48 and 96 kHz,
  tempos 20, 90, 93.33333587646484, 120, 121.2 (binary32), 128, 140 and 999, anchors n_a of 0,
  2²⁰ and 2³¹ + 12,345, and anchor beats 0 and 3.5. All equal the model and
  `PredictedLongSampleTime`. A further 4,000 calls in `transport/results/sweep.json` agree.
  The spb values that the real `DoSetTempo` stores equal (SR ÷ T) × 60 bit for bit.
- **Derived (X model).** Let P be the least integer at or above the exact rational
  (b − b_a)·SR·60 ÷ T, with b and b_a taken as their lattice rationals. Over 240,000 swept
  placements (40,000 cases × 6 anchor counters, `plus_one_check.json`):
  - every placement whose exact value is not an integer (182,046) is P;
  - of the 57,954 whose exact value is an integer, 2,753 are P + 1, at anchor counters 0 to 2²⁵,
    and none at 2³⁰ or above;
  - no other deviation occurs.

  The deciding quantity is q, the product of the two binary64 operands fl(b − b_a) and spb,
  rounded to binary64, compared with the integer P:
  - **q ≤ P.** All 51,414 such integer cases give P on both slices for every counter. A larger
    counter only coarsens the rounding, so this holds in general.
  - **q > P.** The result is P or P + 1: x86_64 gives P + 1 in 2,753 of 6,540 cases, arm64 in
    2,798.

  Examples:
  - At 48 kHz and 90 BPM, spb is 32000.000000000004, so q exceeds P at every whole beat. Beat 1
    lands at 32,001 with n_a = 0 and at 32,000 with n_a = 2²⁰.
  - At 44.1 kHz and 90 BPM, spb is exactly 29,400. The triplet beat 8/3 has fl(8/3) below 8/3,
    so q < 78,400 and the launch at B = 8/3 is exactly 78,400.
  - At 44.1 kHz and 120 BPM, beat 10/3 has fl(10/3) above 10/3. Yet q rounds to exactly 73,500,
    so the event is at 73,500 for every counter.

  Of the 64 common pairs of rate (44.1, 48, 88.2, 96 kHz) and tempo (60 to 180 BPM), 26 have an
  inexact spb (`transport/results/summary-sweep.txt`).
- **U.** n_a is the engine's absolute sample counter, which starts when the audio engine
  starts, not at Play. Which of P and P + 1 Live gives at an integer position is therefore not
  determined by the set and the action script.
- **arm64.** The fused form differs from x86_64 by +1 in at most 33 of 40,000 cases, at
  n_a = 2²⁰ (`summary-sweep.txt`). That is inside the same P / P + 1 class.
- **S.** Buffer size does not move events relative to an anchor. `OEngineDomain::CalcAudio`
  splits each buffer at every event countdown.

### 2. Tempo

- **S.** The tempo path is "Song Tempo" → TempoNudge processor → scheduler `OnTempo` (Engine
  `0x10f370`, x86_64 `0x101ade6d0`, arm64 `0x101ab5b70`). The value is clamped to 20–999, then
  multiplied by the tempo modulation (1.0 here) and clamped to 5–999 (constants 999.0f and 5.0f
  at Engine `0x15bf2c8`, `0x15bab88`). The graph builder was matched in arm64 at the processor
  level only.
- **S.** While stopped, a new tempo applies at once. While playing, it waits for the next
  multiple of 1/4 beat. It applies at once when the current beat is already on such a line in
  binary32: the tempo quantizer is Engine `0x8a30a0`, x86_64 `0x1021d0620`, arm64 `0x1020f1db4`.
- **X.** At that line `DoSetTempo` re-anchors at (that sample, that beat) with the new spb.
  Example: at 48 kHz, 120 BPM changing to 90 BPM at beat 1 (sample 24,000) puts beat 2 at
  sample 56,000 in the run (`transport/results/tempo_change.json`). That position is in the
  P / P + 1 class, so another engine counter could give 56,001.
- **T1 relevance.** ADR 0004 lists tempo among the transport behaviors, so a render script may
  change it. Tempo automation and scene tempo are not traced here.

### 3. Play, Stop and Continue

- **S.** Play from stopped (Live arm64 `0x10276a7b0`, x86_64 counterpart in
  `transport/excerpts.jsonl`) sends SetBeatTime(t\*) and then SetPlaying(true). The engine
  rounds t\* to the lattice and raises a negative value to 0. The anchor becomes (current
  sample, t\*). The first played sample is beat t\*, and an event at t\* fires on it (X,
  `transport/results/fire.json`).
- **S.** t\* is chosen in this order:
  1. the loop start when "loop is song start" is on;
  2. the insert marker (ATransport +0x70, written by OnMoveInsertMarkerToPlayheadPosition);
  3. the earlier end of the arrangement selection (x86_64 `0x10280fcc0`);
  4. 0.

  When a session clip is playing and Session View is visible, and t\* is not the loop start,
  playback starts at the bar line at or before t\* (lattice helper mode 2).
- **U.** Which of these states holds after a set is opened: the insert marker and selection
  are interface state, and whether the loaded `CurrentTime` sets the marker was not traced.
  Also untraced: the bar-floor helper (x86_64 `0x102814eb0`) and the Session-visible condition.
- **S.** A count-in happens only when the start would begin recording
  (`OFireManager::MustCountInOnSongStart`), which is outside T1.
- **X.** Stop applies at once: the song beat stays at the beat of the stop sample. Continue (no
  jump) re-anchors at (resume sample, that beat). Example at 48 kHz and 140 BPM: Stop after
  30,000 samples gives beat 1.4583333333333335. After a 5,000-sample gap, playback resumes
  there and reaches 2.916666666666667 30,000 samples later (`transport/results/stop_resume.json`).
- **U.** The second Stop's write of 0.0 to the current time
  ([T-03](transport-transitions-native.md#transition-table)) was not traced further.

### 4. Song loop

- **S.** `SetLoop` (Engine `0x10cb20`, x86_64 `0x101adbe80`, arm64 `0x101ab3594`) schedules a
  start brace (priority 13) at the loop start and an end brace (priority 5) at start + length.
  The end brace is scheduled only while the current beat is before it. At the end brace, with
  the loop on, the scheduler jumps to the loop start and flags IsAtSongLoopJump
  (`ProcessLoopBracePassed`, x86_64 `0x101aded30`, arm64 `0x101ab60c8`).
- **S.** The engine limits the loop start to at least 0 and the loop length to at least 1 beat
  (`OEngineDomainManager::SetLoopStart` and `SetLoopLength`, Live x86_64 identical).
- **X** (`transport/results/loop.json`). Each jump re-anchors, so each pass is placed afresh by
  the clock rule:
  - 48 kHz, 120 BPM, loop [4, 8), Play from 4: jumps at 96,000, 192,000, 288,000 and 384,000;
  - 48 kHz, 140 BPM: jumps every 82,286 samples;
  - 44.1 kHz, 140 BPM, Play from 0: no jump at the start brace (75,600), then jumps at 151,200,
    226,800 and 302,400;
  - a loop of 10/3 beats from 2 at 48 kHz, 120 BPM: 128,000, 208,000 and 288,000;
  - Play from 10 with loop [4, 8) never jumps.
- **S, x86_64 and arm64.** A playing session clip is not moved by the jump.
  `OAsyncTrack::OnSongPositionJumped` (x86_64 `0x101b06500`, arm64 `0x101adb6b0`) shifts the
  clip's fire time by the jump. The later event beats therefore shift by minus
  (loop end − loop start) and are placed from the new anchor. Their samples can
  differ by one from an independent placement that ignores the jump: the two
  anchors round their placements separately. The released loop cases agree under
  both readings; see the [review outcome](../specs/playback-core-handoff-plan.md#review-outcome--2026-10-19).

### 5. Launching a clip

**A1, settled for the Trigger fire path (S).**

- **The command carries no time.** `OFireClipCommand` (registered by Engine `0x14ee00`, x86_64
  `0x101b1e150`, arm64 `0x101af22f4`) has no time member. Its members are Engine, TrackIndex,
  AutomationIndex, Quantized, NoteType, OClipFireParams (StartType, StartValue, ScrubAmount,
  RecordLength, QuantizationOverride, ForceLegato, track, IsStartValueUnfolded), FireVelocity
  and FireTransposition.
- **The song fire passes no time either.** `OFireManager::FireClip` (Engine `0x14d520`, x86_64
  `0x101b1c870`, arm64 `0x101af0cbc`) passes DBL_MAX as the requested time.
- **What a clip-slot press sends.** The clip slot's fire method is AClipSlot vtable slot +0x258
  (x86_64 `0x10257bf70`, arm64 `0x10245c72c`); Python `ClipSlot.fire()` also uses it. It sends
  Quantized 1, StartType 0, no quantization override, fire velocity 1.0 and no legato.
- **Where explicit times come from.** Only follow actions, refires, loop scheduling and scenes,
  the other callers of `PrepareClipFire`.
- **The slot test.** In `CalcLaunchQuantization` (Engine `0x12a9f0`, x86_64 `0x101af9d50`, arm64
  `0x101acffa4`), +0x38 is IsSlotAutomation and +0x20 ≥ 2 is "the slot holds a clip". The grid
  is then the slot's `QuantisationTime` from `OSlotFireData`. That is the clip grid of
  REQ-CLIP-LAUNCH-016 when it is not negative. For Global (−1.0), with no explicit time, the
  grid is the global quantization on the song's current signature. Quantized 0 gives no grid.
- **Bounded remainders (U).** Which interface gestures reach slot +0x258, and that the loaded
  `GlobalQuantisation` is posted to the engine when the set opens
  (`LSongUnit::OnGlobalQuantizationChanged`).

**Boundary, offset and activation** (`OAsyncClipFireManager::PrepareClipFire`, Engine `0x12ab50`,
x86_64 `0x101af9eb0`, arm64 `0x101ad0130`).

- **S.** The press time t is the lattice-rounded current beat. B is the X2 boundary of
  REQ-CLIP-LAUNCH-017.
- **X, path S.** The offset o is a pre-delay asked of the track's clip player
  (`RequestedPredelaySongBeatForClip`, Engine `0x12c1a0`, x86_64 `0x101afb500`, arm64
  `0x101ad1418`):
  - **MIDI.** MIDI clip and note players return 0 (`OAutomationPlayer` slot +0x48, x86_64
    `0x101b119a0`, arm64 `0x101ae6134`).
  - **Audio.** `OAudioClip::SCrossfadeDurBeat` (Engine `0x9a45d0`, x86_64 `0x102278eb0`, arm64
    `0x102188f34`, no fused operation) gives o as the smaller of two values over the old and the
    new clip:
    - half the clip's loop region (an unwarped clip's region is in seconds, converted at
      tempo ÷ 60);
    - 4 ms × tempo ÷ 60 (`OAudioClipFadeTime::SInitInstance`, x86_64 `0x10227c780`, arm64
      `0x10218c488`: 4.0 unless a debug option is set).
  - **When o is 0.** It applies only when both clips are session clips with Fade on. It is 0
    when either has Fade off, and when no clip was playing.
  - **X.** All 16 cases of `launch/run_launch.txt` match this model. Examples: 0.006 beat at
    90 BPM, 0.008 at 120 BPM, 0.00375 for a 5 ms unwarped loop.
- **S.** The "track condition" of the earlier reading is
  `SongWasPlayingBeforeCurrentSample` (x86_64 `0x101af9bb0`, arm64 `0x101acfe68`). It is true when
  the transport plays and the current sample differs from the sample at which playback last
  started (+0x3b0, written by `OnSongPlayingSwitched`, Engine `0x12db80`).
- **S.** If B − t < o, the song was already playing and the grid is not 0, B becomes B + grid.
  Otherwise o is reduced to B − t.
- **S.** The fire record holds B and E = lattice(B − o). The clip's start maps to song beat B.
  The fire event is a beat event at E, placed by the clock rule. If E ≤ t and the song was
  already playing, the launch is applied at the request sample itself. The track's previous clip
  is replaced in the same activation (`OAsyncClipFireManager::Fire`, x86_64 `0x101afb6e0`, arm64
  `0x101ad15e8`).
- **S.** With no grid, B = lattice(t) and o becomes 0, so the clip starts at the request sample.
- **S.** A launch while stopped makes the engine set the song position to the stored start beat:
  its downbeat unless it is a locator (Engine `FireClip`). The engine computes B from that
  position, then requests play. With a start beat of 0 and the clip on the grid, the clip
  starts on the first played sample.
- **Cases** (`launch/samples.txt`). Launch samples for the CLC grid cases at 90 BPM:
  - At 44.1 kHz spb is exactly 29,400: CLC-031 (B = 8) is 235,200, and CLC-041 (B = 8/3) is 78,400.
  - At 48 kHz the same launches are 256,000 or 256,001 by the clock rule's +1 class.
  - Audio at 100 BPM, Fade on:
    - a first clip launches at 230,400 (48 kHz);
    - a replacing clip's event is at 230,208, with the clip start at 230,400;
    - a press at 7.995 moves to B = 12, with the event at 345,408.

### 6. Stopping clips

- **S, both slices.** The press reaches the engine with no explicit time:
  - **Track Clip Stop.** `ATrackDevice::OnStop` (x86_64 `0x10285cce0`, arm64 `0x102728b88`)
    calls track vtable slot +0x3d8 (x86_64 `0x102842c50`, arm64 `0x1027104dc`). That slot sends
    `OFireClipCommand` with AutomationIndex −2, Quantized 1, no override and no time.
  - **Empty slot.** Pressing an empty slot's button (AClipSlot slot +0x258) is a stop only when
    the slot's HasStopSlot flag is set.
  - **Stop All Clips.** The main track's slot +0x3d8 (x86_64 `0x10269d2d0`, arm64 `0x1025770bc`)
    sends `OFireSceneCommand`(−2). `FireScene` (x86_64 `0x101b1cff0`, arm64 `0x101af1358`) then
    fires −2 on every player track.
- **S.** A stop uses the global quantization on the song's current signature, even when the
  playing clip has its own launch quantization. The grid is 0 (immediate stop) when the
  transport is not playing, when the track is already stopped, or when playback started on the
  current sample.
- **S, X for the arithmetic.** The boundary and the near-boundary rule are those of launching:
  - **MIDI tracks.** o is 0.
  - **Audio tracks with Fade on.** o is the crossfade length of the playing clip.
  - **When it applies.** The stop applies at E = lattice(B − o). It applies at once when E ≤ t.
  - **Pending launches.** A stop takes the track's single pending-fire slot, so it replaces a
    pending launch.
  - **X results** (`stop/results/stop.json`, 10 boundary cases): 5.3 at 1 Bar → 8; 10/3 at
    1/4T → 4; 1.3 at 1/16 → 1.5; no grid → t.
- **S, x86_64 and arm64 for the end test.** An unlooped clip ends at its launch beat + (loop end
  − loop start): `SIsPastEndOfUnloopedSlotClip`, x86_64 `0x101b17510`, arm64 `0x101aeb668`, X
  inclusive. An unwarped unlooped clip ends on the first sample at or after its length in
  seconds (`OUnwarpedClipTimeEvent::SBeatTimeForClipTime`, x86_64 `0x101b6c540`, arm64
  `0x101b36d14`, X). The end is rounded up to a whole sample and nudged down by half a lattice
  step. A 2.0 s clip launched at beat 8 at 90 BPM lasts 96,000 samples at 48 kHz. A clip can
  also last one sample more than its frame count; see finding 8.
- **S, Engine and x86_64, arm64 for the jump handler.** Transport Stop posts only
  SetPlaying(false). The engine does not clear a track's playing slot on stop, so playing clips
  stay assigned and sound again at the next Play. If the song position is changed while
  stopped, each assigned clip is re-based on the new position (`OnSongPositionJumped` branch,
  x86_64 `0x101b06500`, arm64 `0x101adb6b0`).
- **U.** What Live installs in the all-notes-off and panic callbacks; and whether a stop pending
  at a transport stop or a position jump survives (rescheduled, not analyzed).

### 7. MIDI clip playback

- **D, S.** The clip writer (x86_64 `0x10257ecd0`, arm64 `0x10245f420`) sends the engine four
  values:
  - start S = lattice(LoopStart + StartRelative) when IsWarped (all 1,252 shipped MidiClips are);
  - loop start Ls and loop end Le, from `Loop/LoopStart` and `Loop/LoopEnd`;
  - looped, from `LoopOn`.

  `OutMarker`, `HiddenLoopStart/End` and `CurrentStart/End` do not enter session playback
  (`ALoop` registry, x86_64 `0x102691be0`, arm64 `0x10256b7e4`). All 376 shipped unlooped
  MidiClips have StartRelative 0.
- **X.** Clip position (`OClip::SCalcCurrentPos`, x86_64 `0x101b12870` and core `0x101b14fd0`;
  arm64 `0x101ae6f54`, `0x101ae9360`). 234 inputs × 3 functions are bit-equal to a binary64
  model (`midi/results/clip-position.json`). At song beat B + d the clip time is
  p = lattice(S + d):
  - **Looped.** Once p ≥ Le it is folded into [Ls, Le) by fmod, and a result equal to Le becomes Ls.
  - **Unlooped.** The clip has ended once p ≥ Le.
  - **Start outside the loop.** S < Ls plays through to Ls. S > Le folds into the loop (start
    3.5 with loop 1–3 starts at clip time 1.5).
- **S.** Pass 1 runs from B to W₁ = lattice(B + Le − S). Each later pass k starts at W_k and
  lasts Le − Ls (`SetupRecurringLoopEvents`, x86_64 `0x101b13460`, arm64 `0x101ae7984`). Event
  times are lattice(base + t), with base B − S in pass 1 and W_k − Ls afterwards (x86_64 only).
- **X.** The per-key event list comes from builder x86_64 `0x102a13f20`, arm64 `0x1028cf5c0`:
  12 cases in `midi/results/note-events.json`. Under gdb the pool allocator is replaced by
  malloc, the capability flag is poked and the group lookup is stubbed. Each list holds:
  - one monophonic player per key that has notes, shared by the track's clips;
  - a leading note-off at −10,000,000;
  - per enabled note in stored order: a note-on at Time with the stored binary32 velocity, then
    a note-off at lattice(Time + Duration) with OffVelocity;
  - for a zero-length note, a note-off one lattice step later.

  Notes are skipped or dropped in three cases:
  - disabled notes are skipped;
  - a note with the same Time as the previously emitted note on the key is dropped;
  - a zero-length note followed by a note at the same Time is dropped.

  Overlapping notes on one key give an unsorted time list.
- **S, x86_64 only.** Activation origins decode to the same 18 names in Engine and Live x86_64.
  Chasing (starting a note already under way) happens only for scrub, song start, song position
  (when chasing is on) and update origins, within a Live-supplied range. So a note that spans S
  at launch, or spans Ls at a loop wrap, is not sounded.
- **S, x86_64 only.** At one beat, events are ordered by priority: per-note expression 0,
  note-off 1, loop and clip-end events 7, note-on 14 (table x86_64 `0x105db2460`). A note-off
  exactly at Le is sent before the wrap with its own OffVelocity. A note-on exactly at Le never
  plays.
- **Cut notes (S, x86_64 only, except retrigger S both).**
  - **At the wrap.** A note held across Le is cut at the wrap. Its velocity is 64, or the
    OffVelocity of the last note-off before Ls.
  - **Retrigger.** A note-on for a key still sounding is preceded at the same sample by a
    note-off of velocity 64.
  - **Unlooped end.** Every held note gets velocity 64 at B + (Le − Ls).
  - **Stop.** A stop button, transport Stop or deactivation sends velocity 64 to held notes.
  - **Relaunch.** Launching another clip cuts held notes. The exception is a held note on a key
    where the new clip is itself inside a note at its start: that note keeps sounding.
- **S, x86_64 only.** The note-on velocity is v × (1 − a × (1 − f)), clamped to 1–127
  (`OMidiClipAttributeProcessor::HandleNoteOn`, x86_64 `0x101b78010`). a is the clip's
  VelocityAmount and f the fire velocity, so with a = 0 the stored velocity passes through.
  That this processor is in the note path is assumed.
- **S, both slices.** VelocityDeviation and Probability apply only when an application
  capability byte is set (x86_64 `0x1014f9cc0`; set for product codes 0 and 3). X with the flag
  clear: deviation 0 and probability 1. With it set, the deviation is clamped so v + deviation
  stays in 1–127, and the velocity is drawn uniformly from a per-player linear congruential
  generator (constants `0x19660d`, `0x3c6ef35f`). Probability ≤ 0 never plays, 1 always plays,
  and any other value is a random draw.
- **U.** Which product code 12.4.3 Suite runs as, and so whether the flag is set.
- **S.** With GrooveId −1 no groove is passed and note times are unchanged.
- **S, x86_64 only for later points.** Per-note expression initial values (TimeOffset ≤ 0) are
  rounded half away from zero and sent with the note-on; later points become timed events.
- **Cases** (`midi/results/cases.json`). Fixture B1 "Slide" has key 51, eight 0.25-beat notes
  at 0, 0.5 … 3.5, velocity 100 and loop 0–4. Launched at B = 4 at 48 kHz and 120 BPM, the
  note-ons are at 96,000 + 12,000k and the note-offs at 102,000 + 12,000k; pass 2 starts at
  192,000. At 44.1 kHz and 110 BPM (spb inexact, positions not integers) the first note-on is at
  96,219.

### 8. Audio clip playback with warping off

Engine names reach Live x86_64 here by byte similarity: 70 to 100 % equal bytes at the same
size (`audio/matching.tsv`). Each arm64 counterpart named below was found separately. A clause
without one is x86_64 only.

- **S.** The interface sends `WarperUnWarped.Parameter.Create` (x86_64 `0x102904c10`, arm64
  `0x1027cade8`; member writer x86_64 `0x1029048e0`, arm64 `0x1027cab44`). It carries
  Transposition, Volume, VelocityAmount, InterpolationType, and the loop start and end in
  seconds.
- **The playback chain (x86_64).** In the engine, `OWarperUnWarped::StartClipNote` and
  `StartFileSmpl` start an `OFadingPlayerBrain` voice. `OPlayerEndEvent::PlaySample` then calls
  a per-sample `OFadingPlayer::CalcPri…` kernel, and `OAudioNoteEnvelopeProcessor` applies the
  clip fades.
- **D, S.** An unwarped clip's `LoopStart`, `LoopEnd` and `StartRelative` are seconds of file
  time. In all 2,479 shipped unwarped clips, LoopEnd × DefaultSampleRate = DefaultDuration
  (`audio/shipped-unwarped-clips.jsonl`). All 2,479 have `LoopOn` false.
- **X, path S.**
  - **Transposition.** t = PitchCoarse + 0.01 × PitchFine in binary32, limited to ±48.
  - **Read step.** The step per output sample is binary32 powf(binary32 2^(1/12), t) ×
    file rate ÷ engine rate, held in 32.32 fixed point rounded to nearest.
  - **Function.** `OWarperProcessor::SSemitonesToInc`, x86_64 `0x10236f1f0`, arm64 `0x10225a2bc`,
    no fused operation. 78 of 78 runs equal the model.
  - **Examples.** A 44.1 kHz file at 48 kHz: 0.91875, fixed 3,946,001,203. +12 semitones: step
    `0x200001400`, slightly above 2. −12 semitones: 0.4999997317790985.
- **S.**
  - **First frame.** trunc(file rate × loop start), plus the truncated product of any samples
    already elapsed since the clip start and the step (`StartFileSmpl`, x86_64 `0x1023706b0`,
    arm64 `0x10225b4e8`).
  - **Fraction.** The fraction starts at 0, and is forced to 0 whenever the step is exactly 1.
  - **Accumulation.** Output k reads position p₀ + k × step, accumulated exactly in fixed point.
  - **Quantization.** Positions are quantized to 2⁻²⁴ frame (`SQuantizePosFileSmpl`, x86_64
    `0x10235b910`, X 8 of 8).
- **S, x86_64; X for the kernels.**
  - **Choice.** The Live side picks the interpolation type (x86_64 `0x1028f76a0`, arm64
    `0x1027bd748`). HiQ off gives linear interpolation. HiQ on gives a 16-tap Kaiser-windowed
    sinc (β = 5π, cutoff 0.95, 257 phases, linear between phases; the table built by
    `NFirInterpolation::SInitO` matches that formula within 9.9e-8).
  - **High steps.** Above a step of 1.125, HiQ uses the FIR twice per output and then an
    8th-order allpass half-band decimator (FIR2X).
  - **Direct copy.** A step of exactly 1 with fraction 0 copies frames under both settings.
  - **Cubic.** Cubic interpolation needs `ASong` slot +0x368, whose base class returns false.
  - **X results** (`audio/summary.txt`). The None, linear, cubic and 16-bit kernels are bit-equal
    to their models in every run. The FIR agrees with a binary64 model within 6e-8, and its X
    outputs are the reference.
  - **arm64.** Linear fuses one operation and cubic four, so arm64 differs at rounding level.
- **X, path S.** The clip gain `SampleVolume` is stored as linear gain. It is sent through the
  −70 to +24 dB control mapping (`OVuMeterMath::SControlLevel`, x86_64 `0x101aed490`). The
  round trip equals binary32(SampleVolume) within 1.2e-7 relative, exactly for 18 of 32 values.
  The gain is limited to 3.1622776e-4 to 15.848933, so SampleVolume 0 plays at −70 dB, not
  silence. The kernel multiplies each interpolated value by gain × ramp. With VelocityAmount 0
  the gain is unchanged.
- **S, X.**
  - **Mono files.** A mono file gives identical left and right outputs (R = L in every run).
  - **16-bit sources.** None and linear outputs are bit-identical whether frames are held as
    16-bit or float chunks. The FIR outputs differ between the two by up to 4.9e-4.
  - **U.** Which chunk type a 16-bit file gets (static route: the caller of
    `OChunkedSample::Init`).
- **S, x86_64; arm64 for the fade ramp** (`OAudioNoteEnvelopeProcessor::ScheduleFade` and
  `UpdateGainRamp`, arm64 `0x10218fc08`, `0x10218fe24`; seven fused operations).
  - **Fade-in.** With Fade on, the clip fades in over min(4 ms, half the region). The gain follows
    3x² − 2x³, evaluated at control points at most 32 samples apart with linear ramps between,
    starting from 0.
  - **Clip change.** A new clip cuts the old voice short over min(new fade, 4 ms).
  - **Fade off.** No envelope fade; the gain is 1 at once.
- **S, x86_64.** Past the last frame the read position stays on it. With Fade on, that frame's
  value is held and ramped linearly to 0 over about 4 ms of file frames. With Fade off the
  output is silence.
- **S.** The step does not depend on tempo. An unwarped clip's end is scheduled in seconds and
  rescheduled on a tempo change (`OUnwarpedClipTimeEvent::OnTempoChanged`, x86_64 `0x101b6ceb0`).
- **S, both slices for the scheduling branch.** `OAsyncTrack::ScheduleLoopOrUnloopedClipEnd`
  (Engine `0x136c20`, x86_64 `0x101b05f80`, arm64 `0x101adb0b8`) branches on the clip's warp
  flag:
  - **Unwarped.** It schedules only the unwarped end event, at the start plus the clip's
    `LoopLengthInSecs` (OAudioClip vtable slot +0x18), whatever the loop switch. The event's
    callback (read in x86_64) is `OAsyncTrack::OnUnloopedClipEnd`, which fires the stop
    slot (−2).
  - **Warped.** Only a warped clip reaches the recurring loop events.

  An unwarped session clip therefore plays its region once and stops. This is consistent with
  the shipped data, where no unwarped clip has LoopOn true. With transposition, the region
  length in seconds is divided by the pitch ratio.
- **X.** The end beat comes from `SBeatTimeForClipTime` (x86_64 `0x101b6c540`, arm64
  `0x101b36d14`). It rounds the clip length up to a whole engine sample in beats and subtracts
  half a lattice step. Runs with the shipped clip lengths (`end/results.json`):

  | Clip, at 120 BPM | 48 kHz | 44.1 kHz |
  | --- | --- | --- |
  | Rim 3k Sharp (19,913 frames at 48 kHz) | 19,914 samples, from 96,000 to 115,914 | 18,296 |
  | Rim DMX Vinyl (3,386 frames at 44.1 kHz) | 3,686 | 3,386 |

  The 48 kHz figure for Rim 3k Sharp is one more than the frame count because binary64
  0.4148541666666667 × 48,000 is 19,913.000000000004.
- **U.**
  - Fade gains as exact sample values (the envelope processor was not run).
  - Chunk padding at the file start, the file end and chunk edges, which affects about the first
    and last 8 FIR outputs.
  - Decoder scaling for 24-bit, 32-bit, AIFF and compressed files.
  - `StartRelative` ≠ 0 and launches that start late into the clip.
  - Files with more than two channels.
  - Clip gain or pitch changed during playback, and VelocityAmount > 0.
  - Absent `HiQ` or `Fade` elements.
  - What the crossfade sounds like between E and B on a clip change.
- **Resampling quality.** Settled only as reference kernels. The interpolators are specified by
  their X behavior (linear, the windowed sinc and FIR2X), not by a quality metric. Their
  frequency response and FIR2X group delay are characterized only by the retained renders.
- **Cases** (`audio/results/shipped.json`, first 96 outputs of each render, with hex). Fixture
  `Core Library/Ableton Folder Info/Sample Reference.als` (SHA-256 `19d32f0f…8b43ce1`) has
  `Rim 3k Sharp.wav` (48 kHz mono 16-bit, `6ef0441c…4d338f`) and `Rim DMX Vinyl.wav`
  (44.1 kHz mono 16-bit, `1802f16a…bbd6`) as unwarped session clips with HiQ on and Fade off.
  At 48 kHz the first is a bit-exact copy, int16 ÷ 32,768 on both channels.

## Matching table (key functions)

| Role | Engine | Live x86_64 | Live arm64 |
| --- | --- | --- | --- |
| `TStatus::PredictedLongSampleTime` | `0x1096d0` | `0x101ad8a30` | `0x101ab05cc` |
| `OScheduler::DoSetTempo` | `0x10c2e0` | `0x101adb640` | `0x101ab2d50` |
| `OScheduler::SetPlaying` / `SetBeatTime` | `0x10cff0` / `0x10d640` | `0x101adc350` / `0x101adc9a0` | `0x101ab3a4c` / `0x101ab4038` |
| `OScheduler::ProcessNextEvents` | `0x10f540` | `0x101ade8a0` | `0x101ab5cec` |
| `OScheduler::SetLoop` / `ProcessLoopBracePassed` | `0x10cb20` / `0x10f9d0` | `0x101adbe80` / `0x101aded30` | `0x101ab3594` / `0x101ab60c8` |
| Tempo quantizer | `0x8a30a0` | `0x1021d0620` | `0x1020f1db4` |
| `OFireManager::FireClip` | `0x14d520` | `0x101b1c870` | `0x101af0cbc` |
| `OAsyncClipFireManager::CalcLaunchQuantization` | `0x12a9f0` | `0x101af9d50` | `0x101acffa4` |
| `OAsyncClipFireManager::PrepareClipFire` | `0x12ab50` | `0x101af9eb0` | `0x101ad0130` |
| `OAsyncClipFireManager::RequestedPredelaySongBeatForClip` | `0x12c1a0` | `0x101afb500` | `0x101ad1418` |
| `OAudioClip::SCrossfadeDurBeat` | `0x9a45d0` | `0x102278eb0` | `0x102188f34` |
| `OClip::SCalcCurrentPos` | `0x143520` | `0x101b12870` | `0x101ae6f54` |
| `OMidiNoteAutomationPlayer::Process` | `0x1b0150` | `0x101b7f3d0` | `0x101b48da8` |
| `OClipTimeable::SIsPastEndOfUnloopedSlotClip` | `0x1481c0` | `0x101b17510` | `0x101aeb668` |
| `OAsyncTrack::OnSongPositionJumped` | `0x1371a0` | `0x101b06500` | `0x101adb6b0` |

The full tables, with how each pair was matched, are the `matching*.tsv` and
`matching-eng-x86.txt` files of each subdirectory.

## Corrections to existing pages

Applied on 2026-10-18:

- SPEC-CLIP-LAUNCH r4: REQ-017 to 019 and the tolerance;
- SPEC-WARP-MARKERS r4: REQ-009 and WM-15;
- transport transitions: a dated correction to T-01.

The other items below are not yet applied (SPEC-CLIP-LAUNCH REQ-022, SPEC-TRANSPORT-STATE,
SPEC-MIDI-NOTE-STORAGE, the extracted-execution triage and the x86_64-only bundles page).

- **[Clip launch](clip-launch.md) and [SPEC-CLIP-LAUNCH](../specs/clip-launch.md) r3, REQ-017.**
  - The offset objects are not "found through the song's track list" or "a per-song engine
    object". They are the track's clip player and the track's clip timeable.
  - The offset is not "settleable only at run time": it is 0 for MIDI and the audio crossfade
    length (X).
  - The "track condition" is the song-already-playing test.
  - B + g needs g ≠ 0.
  - The clip activates at B − o; its start still maps to B.
- **SPEC-CLIP-LAUNCH REQ-018.** The delay of an unquantized launch is zero once the request is
  handled.
- **SPEC-CLIP-LAUNCH REQ-019.** The note "the grid computation can return no grid when the song
  is not playing" applies to stop requests and empty-slot presses, not to clip launches.
- **SPEC-CLIP-LAUNCH, timing and state.** The ±1/64-beat tolerance (375 samples at 48 kHz,
  120 BPM) is coarser than ADR 0004's sample-exact timing dimension. Grid cases can be graded to
  the sample.
- **SPEC-CLIP-LAUNCH REQ-022.** It says the velocity-amount code is "not located". It is located
  (x86_64 only) and its formula is above.
- **[Transport transitions](transport-transitions-native.md) T-01.** The effective start
  position is no longer unknown: the first sample is beat t\*. ATransport +0x70 is the insert
  marker, and the "song value" is the arrangement selection start.
- **[SPEC-TRANSPORT-STATE](../specs/transport-state.md).**
  - "Tempo in BPM (inferred)" is now S.
  - REQ-009's open effective values are partly answered by the engine limits: loop start ≥ 0,
    length ≥ 1.
- **[Extracted execution](extracted-execution.md#candidates-settleable-by-extracted-execution).**
  It lists timing among the probes not settleable by X. The scheduler arithmetic is settleable
  with a hand-built scheduler status.
- **[SPEC-MIDI-NOTE-STORAGE](../specs/midi-note-storage.md) REQ-007.** "IsEnabled false is
  muted" and "Probability is a play chance" are U there and now S. REQ-010's overlap question
  is partly answered (finding 7).
- **[x86_64-only bundles](x86-only-bundles.md).** "Equivalence between the compiles is not
  established" now has strong static support for the regions above.
- **[SPEC-WARP-MARKERS](../specs/warp-markers.md) REQ-009 and [warp markers](warp-markers.md).**
  The claim that no static caller connects the conversion cores to playback is wrong. x86_64
  `0x101b6f970` and `0x101b6fa60` are the Engine's `OWarpMarkerList::BeatToSampleTime` and
  `SampleToBeatTime` (96.3 % equal bytes). They are called by `OWarperBase::PlayPosFileSmpl`,
  `OWarperBase::StartSample`, `OWarpData::FileBeatToFileSmpl` and the `OWarperBeats` grain
  functions. REQ-009's "Inferred" clause can become S, for x86_64. Candidate WM-15 ("unwarped
  loop fields are seconds") is S, not inferred.
- **SPEC-CLIP-LAUNCH REQ-022, audio clips.** For audio clips the velocity amount is applied in
  `OWarperBase::PreparePlayingProperties` (x86_64 `0x10235ca20`) through
  `OModulation::ModulateUnipolarSingleIntensity`.

## Unknowns and their effect on T1

- **The +1 class** (finding 1). At an integer exact position where the rounded binary64 product
  q exceeds it, Live gives P or P + 1, so T1 must accept either there. Where q ≤ P the position
  is exact.
  Choosing rates and tempos with an exact spb keeps whole-beat positions exact: 120 BPM at 48 kHz,
  or 90 BPM at 44.1 kHz.
- **Play's start beat after opening a set** (finding 3). Render scripts must state the start
  beat or start from 0 with the loop off.
- **Delivery time of unquantized requests.** Play, Stop, a no-grid launch, an immediate stop and
  a tempo change while stopped take effect when the engine handles the message. The render
  script defines that sample.
- **MIDI.**
  - Same-key overlapping notes are excluded: 261 shipped notes overlap their predecessor, and the
    binary search over an unsorted list is undefined.
  - The capability flag is not identified, so probability strictly between 0 and 1, non-zero
    velocity deviation and probability groups are excluded.
  - Per-note expression ramps, the fire velocity when VelocityAmount ≠ 0, and the chase range
    are U.
- **Stopping.** The all-notes-off callbacks and pending stops across a jump are U.
- **Audio.**
  - Exact fade gains are U, so Fade-on renders are graded within a tolerance or excluded.
  - The FIR outputs of 16-bit files depend on the untraced chunk type (up to 4.9e-4).
  - Formats other than 16-bit PCM WAV, audio `StartRelative` ≠ 0, LoopOn true on an unwarped clip,
    files with more than two channels, and gain or pitch changes during playback are excluded.
  - arm64 fused operations and Apple's `powf` keep interpolated outputs from being bit-exact
    against the release slice. The reviewed linear comparator uses an absolute
    bound of two binary32 units in the last place of the largest source-frame
    magnitude read by the window; a relative bound on the output fails near
    cancellation. FIR output retains the proposed 1e-6 absolute bound.
  - With Fade off and the region extending through the file, silence past the
    final frame cannot establish the clip's scheduled end sample. The end-beat
    extraction is retained, but grading the end sample needs another observable
    (handoff plan F7).

## Limits

- Static evidence describes code, not a run of Live. Engine names on Live addresses are matches,
  strongly supported where instruction streams are identical, otherwise as recorded per pair.
- X results bind to the x86_64 slice with glibc in place of Apple's libraries.
  - **Timing functions.** They called only `memcpy`, `bzero` and the exact `fmod`.
  - **Audio runs.** They called glibc's `powf`, `exp`, `sinf` and `exp10f`, so the read step,
    the FIR table and the gain mapping bind to glibc's results.
  - **arm64.** Equivalence is inferred from the static comparison. The known differences are
    the fused placement in finding 1 and the fused interpolation and fade operations in finding 8.
- Hand-built objects carry the field values the static reading assigns. A wrong field reading
  would change an X result's meaning, not its arithmetic.
- No retained Ableton documentation exists in `raw/`. Nothing here is labelled documented except
  shipped schemas and sets.

## Bounded playback route inventory — 2026-10-20

**Authored; pending independent structure review.** The
[playback family structure packet](../../analysis/ableton-live-12.4.3/full-spec-v1/family-playback-routes-v1/structure.md)
cuts the approved integration packet’s I-03–I-06 into the current
SPEC-PLAYBACK-CORE revision 2 requirements 001–023. Its
[bounded route ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/family-playback-routes-v1/route-ledger.json)
enumerates 243 semantic outcomes after collapsing eight repeated cross-references:
43 X-route, 69 S-route, 131 no-established-route. Counts describe this authored
inventory, not grades, application evidence, a completed family or a frozen
whole-product denominator. Existing requirements, cases, releases, U parts,
A1–A5 and cross-architecture/clock/receiver assumptions remain unchanged.

**Observed-static/inferred/unknown remain separate.** Exact retained function,
call-index PC/byte/row and C-line locators support guarded producer/packet,
consumer/state, same-local launch preparation/activation and local scheduler/
MIDI/audio relationships. Public admission, asynchronous command delivery/order,
actual scheduler events, active player/provider identity, MIDI-to-instrument and
audio-parameters-to-voice/output remain unjoined. ARM StartFileSmpl is a file-start
position calculation, not proved voice activation. An available internal X leaf
does not close an emitted-note, gesture, host or clip-audio outcome.

The packet pins predecessor manifest
`7dddd59650ca3395d10e1b3c8aded3cda01d66b522dda4973a08f32e7bfb8f83`
and selected T13/X2/release evidence without copying normative snapshots. It
retains 703 historical input/result rows as auxiliary batch enumeration, including
explicit unresolved actual-receiver/host input sets. These are not call or
required-outcome counts. No new provider, runtime, harness, decoder, installation,
original-function call or candidate work occurred. Root owns the freeze, separate
structure review, atlas/catalog/coverage/log updates and subsequent batch selection.


### Family route review adopted — 2026-10-20

The [frozen playback family map](../../analysis/ableton-live-12.4.3/full-spec-v1/family-playback-routes-v1/manifest.json)
[passed independent review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/family-playback-routes-v1-review.json)
with no findings. All 23 owner requirements and the 243 bounded predicates were
reviewed; eight cross-references remain collapsed and 703 historical result/input
rows remain auxiliary. Its 43 X / 69 S / 131 no-established-route inventory
changes no grades. Public receiver, clock/callback, event/audio delivery and
F6/F7/F8/F9 limits remain explicit. The map selects no original calls or public
output expectations; clip-launch mapping proceeds from the reviewed context.


## Playback whole117 scalar quantization actual approval — 2026-10-21

Root adopts the [whole117 actual batch](../../analysis/ableton-live-12.4.3/full-spec-v1/batch-playback-standing-leaves-v1/manifest.json), SHA256 `e0086f7249ecf7a121991affebc2966d6525177d3cb788327a5aab4b4b8b8646`, by its [independent actual review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/playback-standing-leaves-v1-review.json), SHA256 `275e720fd33c6992463d7f807b8d9d527bce206b7c4b812a4a63775aa1431a7f`. The 243 payloads total 10,028,789 bytes. Each of 117 original children made one supplied-double call to the existing x86 scalar helper `0x10235b910`; the selected result is the complete saved binary64 XMM0 word. Eight historical exact controls agree; 109 pre-call expectations remain NULL in the frozen capture and can become new finite owner expectations under design12.

The closed class retains signed node/half-threshold neighbors around all seven historical lattice magnitudes, zero/quantum/subnormal/minimum-normal, precision and finite scaling/overflow frontiers, infinities and the selected canonical positive/negative quiet NaNs. It is not the infinite lattice or all NaN payloads; no signaling NaN was selected. There are 107 finite and ten nonfinite results: eight infinities, including six from finite inputs, and two canonical signed quiet-NaN words. Twelve returned words are signed zeros. These are local observations, not application faults or legal file/sentinel admission.

All children exited zero with empty stderr and no timeout/TRAP/FAULT/counted-import use/retry. The reviewer read the complete 192-line collector, 87-line analyzer and 93-line checker before data checks, then verified all 117 input words/tokens/strtod results, 234 raw files, call projections, controls and 22 recorded custody identities. Eleven independent negative controls and seven fresh safe host-parser controls passed. Each process lists 1,796 trap/85 Linux/one Linux-data bindings; zero counted use is not proof of absent providers or global-data access. Existing helper ABI/native semantics and the built loader are inherited, not fresh native-body or loaded-provider proof.

JSON records are explicitly fsynced; raw stdout/stderr are closed and hashed without explicit raw-file fsync. No crash/power-loss durability, child input-register/FP-state trace, native arithmetic cause or fitted mathematical replacement is established. Scope is only the supplied scalar function. Clip voices, file admission, public timebase, audio delivery, ARM/Apple equivalence, A1–A5/F6/F7 and builder/kernel/gain joins remain open. Current owner revision3 adoption will pin this approved observation review without repeating it; release review remains separate. Unsupported required behavior stays U and coverage OPEN.


## Playback owner r3 finite adoption — 2026-10-21

The [R3 owner packet](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-playback-r3-finite-v1/manifest.json), SHA256 `03701f9ddf119cee9be0bb62632ae8f98e7a2ae089a275eb3f07a569d0ffa437`, adopts 109 new finite scalar cases PBC-097–205 and retains eight known-oracle agreements as supporting controls. Ten payloads total 242,938 bytes. Root's [added-wording/mapping review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/playback-owner-r3-added-wording-review.json), SHA256 `c3bf0a3ef962ce4a05b3d79656ffc3e6bd7d0330c88a1d587c91f69b069c47be`, reuses the approved actual observations, without reviewing them again. The 122-line data-only checker passed ten negative controls, all109 mappings/eight agreements, 22 unchanged requirement bodies/68 old rows and exact reversal to the 61,890-byte R2 predecessor. Current draft has 177 case IDs, not new outcome-denominator units.

REQ-017 now limits the finite-grid reading to supplied scalar observations: signed zero, six finite inputs returning infinity and canonical signed quiet NaNs do not establish an arbitrary-binary64 finite-grid, native arithmetic cause, FP-state guarantee or portable ARM/Apple bound. Original NULL expectations remain unchanged in the frozen batch; H cases use separate scalar setup and do not inherit timing/audio/file comparators. Public clip/sentinel/Open/audio input admission, A1–A5/F6/F7 and receiver/builder/gain/kernel joins stay open. All 92 released objects remain unchanged. Owner edit followed closure of the peer source-pin window; prior mutable R2 identities remain as-of evidence, not future gates. Neutral fixtures and ordinary release review remain required; unsupported required behavior stays U/OPEN.

## Standing-class eligibility after finite adoption — 2026-10-21

The [117-point batch and R3 adoption](#playback-owner-r3-finite-adoption--2026-10-21)
record every member of their selected supplied-one-double quantization class. This does not
exhaust the standing Playback routes. The `whole_classes` of the `playback` entry
in the retained
[eligibility assessment](../../analysis/ableton-live-12.4.3/full-spec-v1/batch-high-X-eligibility-v1/eligibility.json)
separate 413 historical clock, launch,
position, stop and dependency rows, plus 86 scalar increment/quantization rows,
from 204 builder/gain/kernel rows outside that unpatched scalar class. These are
input-navigation rows, not new observations, callable totals or outcomes.

The [map input inventory](../../analysis/ableton-live-12.4.3/full-spec-v1/family-playback-routes-v1/batch-inputs.json)
retains the existing supplied-state classes. Its `enumeration_gaps` names only
PBC-007's start-beat −2 as a concrete unrun vector, with rate/setup still
unspecified; that lone vector is not a selected whole class. The three-scalar
increment and supplied clock/loop/stop routes are not declared unavailable, but
this assessment identifies no additional complete, missing input partition in
the reviewed inventory. Replaying the historical 499 potentially eligible rows
would not itself settle a new required predicate.

Allocator-intercepted MIDI builder/audio gain and constructed kernel/FIR states
remain separate from receiver-free arithmetic. Public clock and player delivery,
A1–A5, F6 positive-predelay activation and F7 silent-end discrimination remain
open. No new raw/source/runtime evidence or execution was acquired for this
selection assessment. Its conditional lack of a concrete next class is not
proof that all classes are exhausted or Playback/product coverage is complete.


## Post-adoption standing input assessment — 2026-10-21

The [Corpus-first/playback input assessment](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/corpus-playback-next-standing-input-eligibility.json),528,975 bytes/SHA-256 `9f202e2e8ba59344f2cf2b8abb44fb902497802becea09a251605503aacd04e5`, carries the prior standing-class conclusion without replaying observations: the selected117 quantization class is fully observed/adopted, while413 historical supplied-state/clock rows and86 scalar increment/quantization rows remain input navigation, not a new missing class. The existing three-binary64 increment and supplied clock/loop/stop models are not globally unavailable. A next selection needs one complete exact input-bit/branch/typed partition and its existing ABI/state/stub setup; the lone named PBC007 startbeat−2 still has no selected rate/setup. No new such matrix was frozen here.

The allocator-intercepted builder/gain and constructed kernel/FIR paths remain distinct from the admitted unpatched scalar class. Public delivery, A1–A5, positive-predelay activation and silent-end discrimination remain U; neither replaying499 historical rows nor a scalar result settles those joins. Corpus's proposed128-cell Decay input class is the higher-priority concrete route, pending separate Root selection. No original/sourcebehavior/raw/audio/numeric metric replay, model/tool/provider acquisition, new capture/ID/criterion or global exhaustion claim follows.

## Integer semitone and retained-rate class selected — 2026-10-21

Root’s [INPUT-only matrix](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/playback-integer-semitone-rate-input-eligibility.json),715,435bytes/SHA256 `31342332ca3aabfb37a6f3e3b37ad5b722edc0d697274c9e199cea1bf2f2f5fc`, freezes a concrete finite next class: all97 integer semitones−48..48 crossed with the six rate pairs already in the retained `run_inc` declaration:48000/48000,44100/48000,48000/44100,96000/48000,22050/44100,44100/44100. The582 distinct three-binary64 input tuples contain528 new argument tuples and54 historical argument-only matches. Input tokens are exact `d:` hexadecimal values; thirteen meaningful input negatives pass, with zero original calls or output/formula evaluation.

**Whole histories are not argument tuples.** The old78 increment calls shared a process; the proposed582 each use a fresh single-call child. Fifty-four argument intersections are support/navigation, not whole-history equality or old PID/receipt/metric/output/criterion transfer. None may be silently removed by argument-only deduplication. All582 result-bit priors remain NULL, without a powf/ratio evaluator, old result review, fitted formula or portable criterion. This is a complete bounded supplied-helper matrix, not all fine-pitch/rates/loaded clips or a native clamp/rounding/general increment law.

Root selects ONE `batch-playback-integer-semitone-rates-v1` under the standing model. Mix authors after Collision523 final seal; Auto is SOLE actual/source peer after its Collision523 review. Root is citation-only for ALL new playback actual/code/source/raw/results before any reads. Root authored the INPUT enumeration only, never the capture/analysis/control/checker code. One frozen packet receives one independent actual review; no prep/readiness/root-review chain is created.

Use only the existing74792-byte `/var/tmp/sound-analysis/xexec-t13-audio/xexec`, inherited SHA256 `f7fdae69a26d930a4326a2a3eecce271ddf406a1c3ce364e87451dca0c4c13aa`, and existing Live x86 slice identified in the old approved quantization manifest. These identities are inherited metadata here, not fresh loader/image/provider proof. The selected function is `0x10236f1f0`, three binary64 `d:` arguments via the existing XMM0/1/2 bridge, one selected direct call per child, full saved XMM0 output word, no receiver/integer arguments/initializers/setup. The ordinary driver/source declarations were read but not imported or run. Do not import historical Runner (which can build), execute run_x.py, rebuild/install, patch native code, intercept allocators, construct objects, initialize gain/kernel paths or introduce provider/FP treatment. Existing strtod's temporary float cast remains qualified; all selected integer/rate inputs are exactly binary32 representable, which does not trace native entry FP state or ABI.

All new recorder/parent/analysis/checker/initial-assembler source, exact argv/scripts/context bind before calls. Record all registers/raw/import declarations and counted use, host token-to-bit checks, parents/custody and resource outcomes; counted nested work remains separate from582 selected exports. Planning192MiB lifecycle plus128MiB concurrent headroom includes repeated import logs/receipts/author and peer reports; it is unreserved/not a quota. Fresh parent/pre-child remaining-output admission, strict output shape, first-fault stop/no retry/partial retention remain required. If unchanged route cannot fit, stop/file its exact blocker. Prior source/default/FP/provider/OS-exec/cleanup/durability qualifications persist. No IDs/criteria/grades/release/public or ARM/Apple law/whole-product closure follow from selection; public clock/file/player/A1–A5/predelay/silent-end remain U.


## Integer semitone/rate pre-call freeze — 2026-10-21

The selected [whole582 single-call input packet is frozen](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/batch-playback-integer-semitone-rates-v1/pre-call-manifest.json),3,017bytes/SHA256 `e64000779adb7df8fab0bc428038f4e929fb0bff715a5bbd9b6f4ef600952230`:15payloads including every new assembler/recorder/parent/data/checker/freezer, exact input matrix, parser checks and unchanged method-source copies. Existing r2-large resolves to `/var/tmp/sound-analysis/full-spec-v1/batch-playback-integer-semitone-rates-v1`; no new link/storage move/cleanup. All582 are fresh histories, including54 historical argument-only supporting controls; no old PID/receipt/metric/output/criterion inheritance or multicall-history equivalence. ALL priors/portable criteria/grades remain NULL.

Before calls,17input/15protocol/5parent negatives, tworesourceboundaries/six returned-word positives pass; all1,746 original d:hex tokens match whole-token libcstrtod binary64 words. Temporary float cast/native input registers/FPstate remain untraced. Existing xexec/T13 source is retained as data, never built/imported/run as an old helper. Only receiver-free0x10236f1f0/threebinary64/onecall/no setup is selected. Allfour raw carriers and complete imports/positive counted Linux-code uses remain; nonfinite return words are retained discovery, not silently normalized or rejected.

Capture is once582/20sCPUwall/core0/1MiBfile/DEVNULL/newgroups/firstfaultstop/noretry. Seven runtime/image/tool/cache/interpreter plus five new code/input identities use ONE common initial endpoint→each-child-after, explicitly NOT per-child-before custody. Fresh pre-parent and per-child guards retain unreserved192MiB lifecycle+128MiBheadroom/remaining stdout allowance+64MiBmetadata; possible launched-child overshoot/concurrent consumption remains. FDfsync requests are not directory/crash or OSexec/FP/provider proof. AutoSOLEactual/sourcepeer after finalseal; Rootcitation-only ALLnewactual/code/source/raw/results/INPUTmatrixauthor only. No IDs, criteria, public/ARM/audio/clock/filebinding law or whole-product closure; unsupportedU/OPEN.


The full582 class is now [author-sealed for Auto's sole actual/source review](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/batch-playback-integer-semitone-rates-v1/manifest.json),193,818bytes/SHA256 `bbbdb872f8063d2f2b0ad4e05a97feb20870a2d5b8443766c821972d967ee5f0`:1,187payloads/127,393,172bytes/all1,188files0444/exacttreehashPASS. Once582children completed16:04:07.493290–16:06:18.791216UTC/outer1458813/recorderexit0/errorNULL/no retry;582selecteddirectcalls/0selectedinitializers/nestedunknown. Wholeclass includes54argument-only supporting controls, with no oldwholehistory/PIDmetriccriterioninheritance. Sevenruntime+fivecode ONEcommoninitial→eachafter6,984pairs, notperchildbefore. Author receipt/frozen-input bookkeeping passes without own actual stdout/carrier/formula reanalysis; Auto independently reviews allnewsource/raw/results. Root remains citation-only. ALLpriors/portablecriteria/gradesNULL, no owner IDs or public/ARM/file/audio/clock/general increment law; requiredU/OPEN.

## Integer semitone/rate actual adoption — 2026-10-21

[Auto’s sole actual/source review](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/playback-integer-semitone-rates-v1-review.json),4,549,979bytes/SHA256 `c1e4fae9d02a733440d31f5f3ba9a069ee1152964cd0cd60992a3ca8fcd5f1de`, approves the full582 fresh single-call histories. The [manifest](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/batch-playback-integer-semitone-rates-v1/manifest.json),193,818bytes/SHA256 `bbbdb872f8063d2f2b0ad4e05a97feb20870a2d5b8443766c821972d967ee5f0`, seals1,187payloads/127,393,172bytes/1,188files0444. Root adopts by citation ONLY, without reading any new actual/code/source/raw/result payload or repeating numeric proof.

The reviewer read all six new source files/README/assessment/history before the packet-only safe check, then independently checked all582stdout/stderr/receipts/four64-bit carriers,1,746 complete strtod tokens and exact input bits/binary32 representability,582matrix members,precall/parents/resources and custody. Fifteen independent protocol negatives plus seven unsigned-word positives (including raw signaling-NaN words without float decoding) pass, with owned17input/15protocol/5parent/2resource/6word/11retained controls. All582once-only children completed16:04:07.493290–16:06:18.791216UTC/all0/no fault/retry,582selected direct calls/zero selected initializers/nested original/provider calls unknown.47,995,008stdout bytes are retained. All582saved XMM0 words are positive finite normal values,485unique words descriptive only; each counted _powf once. Current1,882declarations comprise85Linux/one data/1,796trap, distinct from counted use and no provider/global-data absence proof.

Twelve COMMON initial identities join each582after endpoint (6,984pairs), NOT per-child before snapshots; six whole-source endpoint pairs are separate. Same loader/slice/three exact d:hex arguments/function0x10236f1f0/no receiver/constructor/init/patch/build/provider/FP treatment remain. Loader strtod’s temporary float cast, native FP/ABI/OS-exec/provider/cleanup/durability/resource guard limits retain scope. Ordinary source/argv endpoints do not prove input-register state or continuous loaded-provider identity.

All582 frozen result priors remain NULL; no powf/ratio formula/model/fit or old increment raw/source-behavior review occurred. Fifty-four old argument-only intersections are not inherited whole histories: old78calls shared a process, these use fresh single-call children. They carry no old PID/receipt/metric/output/criterion transfer or historical replay credit. The full582 newly observed histories may enter R4 as finite supplied-helper cases, while the54relationship and528novel argument tuples remain explicit. Only the saved XMM0 word has the selected observation meaning; other returned registers remain raw carriers. Portable criteria/grades remain NULL/applicationFalse/no public clip/frame/read-step/clock/ARM law, A1–A5/F6/F7 or completion proof.

Arr authors R4 after its priority INPUT assessment seals; Root is sole NEW wording/IDs/mapping/preservation peer while remaining citation-only ALL new actual payloads. Append only bounded REQ017/annex/revision, preserve22otherwhole/old017R3prefix/177oldnavigationIDs68legacyrows/R3objects/old NULL/signed-zero/infinity/NaN qualifications/criteria/release92cases/history/fullreverse. Use current canonical, this new approved summary and prior R3 peer embedded metadata only; absent older individual bytes are not reconstructed or re-audited. No IDs until application, no new release/portable grade or whole-product closure; required U/OPEN.


## Playback owner R4 integer semitone and rate annex adoption — 2026-10-21

[Auto's sole new-owner review](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/playback-owner-r4-integer-semitone-rates-finite-v1-review.json),3,876,369bytes/SHA256 `f9257844d94896382ffb7427a83605fd1adfc3a9197242f0c9d8254327658da3`, approves the new wording, IDs, mapping and preservation. The [manifest](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-playback-r4-integer-semitone-rates-finite-v1/manifest.json),4,261bytes/SHA256 `d6f7dda855370b76b221b25654f07b55eb757bfcafe28ac7006aa04645373e0e`, lists11payloads/3,445,510bytes. Mix applied ONLY the report's complete embedded four-fragment delta and exact75,822-byte target, SHA256 `348a58b89415e912e0f6cf09508bae7c8f7b3950da6f0d27a1dd2765e503c30e`, after exact composition and full reversal to68,222-byte R3. No proposal payload, actual/source/raw/numeric/formula, old catalog/provider or release-fixture proof was reopened; manifest listing/counts alone are metadata.

Arrangement authored R4; Auto was assigned SOLE new-owner wording/mapping/IDs/preservation peer BEFORE any Root new-proposal read. Frozen intended-Root labels remain historical and are superseded by that assignment. Root and this application inherit Auto's embedded approval by citation, without a second owner/actual review. Auto's32owned and25independent negative controls pass; its earlier582actual approval is inherited, not repeated.

R4 adds582 PBC-206–787 IDs/full582fresh single-call histories:97integersemitones−48..48×six retained file/engine-rate pairs. Native expectations copy exact approved SAVED XMM0 binary64 little-endian words; the other three raw carriers have no assigned return meaning. All582frozenpriors remain NULL, portable expected/comparator/grade NULL and new application proof false. Fifty-four historical argument projections are ARG-only supporting references, not old whole-history/PID/receipt/metric/oracle/criterion transfer;528triples are novel in that bounded argument cut. No formula/powf/ratio evaluation, fit, pitch calibration or general semitone/rate/clamp/rounding/publicclip/audio/file/clock/ARM law is inferred.

Only bounded REQ017 is appended, plus its finite annex and revision record. The22otherwhole requirements/old017R3prefix,177oldnavigationIDs/68oldrows/109R3case links/eight known agreements/oldAcceptance and protected sections remain exact, with full reversal. The priorR3owner review lacks individual catalog bytes: only its embedded approved scope/owner pin/counts are inherited, with no invented catalog reconstruction. All92releasedobjects stay unchanged as inherited reviewed scope, not a fresh fixture audit. Old signedzero/sixfinite-inputInf/canonical±qNaN/NULLhistory and A1–A5/F6positivepredelay/F7silentend/currentpublic/ARM gaps keep their scopes. The759draftIDs are navigation, not passes or a whole-product denominator.

Temporaryfloatcast/1746hoststrtod words do not attest native input registers/FPstate. Current1,882declarations (1,796trap/85Linux/oneLinux-data) differ from counted `_powf` once per selected call;485positive-finite words are descriptive only. Six source endpoints and ONEcommon12initial→582after snapshots/6,984pairs are NOT per-child-before or continuous provider/ABI/OSexec/source-version proof. FDfsync/resource/cleanup and initial-materializer qualifications remain unchanged; no old-gap repair. No new release, candidate conformance, grade/site or product closure. Required unsupportedU/OPEN.

The [focused application delta](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/playback-r4-owner-adoption-incremental-check.json) checks only sole-review/manifest metadata, the exact applied target and affected docs/browser. Prior CorpusR15 checkpoint carries as-of9,519 without proof replay; this adoption brings cumulative additions to10,101draftIDs. Analog193 and Corpus890 actual adoptions/later owners are excluded from this delta and routed separately by Root.


## Shipped unwarped file-rate INPUT class — 2026-10-21

The [sealed INPUT-only catalog](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/playback-shipped-unwarped-rate-input-eligibility.json),1,731,262 bytes/SHA256 `cb7a6fbca5a68067e41fb566ff10129f8a0300b5aab2f1e35c6f578afd15dc9b`, covers all2,479 retained shipped-unwarped metadata rows and exact source-row locators. All have literal PitchCoarse=`0`/PitchFine=`0`. Distinct DefaultSampleRate values/counts are44,100(2,058),96,000(288),48,000(130),22,000(2),22,050(1). Crossing this COMPLETE retained five-value source class with BOTH engine rates declared in the owner's Definitions (44,100/48,000), at supplied semitones+0, gives10 distinct three-binary64 helper INPUT histories. It is not all possible UI/engine rates, a fine-pitch grid or a whole-product denominator. No referenced sets/audio files are opened.

Six exact+0 entries of the approved582 single-call catalog qualify as historical INPUT references: identical d:hex tokens/three f64 words, target0x10236f1f0, fresh-process/no-init/no-object/one-call history, fixed environment and unchanged loader/slice/runtime-expected metadata. No old PID, receipt, output, metric, oracle or criterion transfers. Their old78 argument-only multi-call references are not used as whole-history joins. Future custody/current runtime equivalence remains a required recorded condition, not acquired or inferred here. The four missing pairs in this bounded whole source class are(96000,44100),(22000,44100),(22000,48000),(22050,48000), file rate first. All exact d:hex tokens/f64 words and six qualified INPUT pointers are retained, with NULL new priors/native expectations/portable criteria/grades/application proof false. No pow/ratio/output/native/provider evaluation or original call occurred.

The retained schema's `/classes/AudioClip/fields/44` and45 identify BOTH PitchCoarse and PitchFine as UserFloat, not Int. Combined with all-zero retained values, this supplies NO complete101-cent/all-fine partition or integer-step/public admission law. General Fine and A3 remain U; selecting an arbitrary fine grid would not complete that domain. Thirteen meaningful INPUT corruptions and full-rate/source-row/context-intersection assertions pass. If separately selected, the four missing members would use the already-admitted audio xexec74792-byte/no-initializer/no-receiver/three-double/one-call fresh-child model only, with first-anomaly stop/no retry and no new source/tool/patch/provider/object/calibration.16MiB lifecycle+128MiB headroom is unreserved planning only. No capture/owner IDs/release/grade/site or compatibility/closure is selected; required U/product OPEN.

## Shipped unwarped file-rate class selected — 2026-10-21

Root selects the complete [retained rate INPUT class](#shipped-unwarped-file-rate-input-class--2026-10-21), pinned by the [1,731,262-byte INPUT catalog](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/playback-shipped-unwarped-rate-input-eligibility.json)/SHA256 `cb7a6fbca5a68067e41fb566ff10129f8a0300b5aab2f1e35c6f578afd15dc9b`: five file sample rates found in all2479retained unwarped-clip records, crossed with the two engine rates already named in the owner's Definitions. Every retained record has literal PitchCoarse=0/PitchFine=0. The ten supplied native-input histories use semitones positive zero and all pairs of file rates44100/48000/96000/22000/22050 with engine44100/48000. Six match approved582 INPUT metadata under the same declared fresh single-call context and remain references only; they receive no replay, new PID, receipt, metrics, native output or criterion. The four missing pairs are96000/44100,22000/44100,22000/48000 and22050/48000. The old78 shared-child argument-only projections are not used as whole-history references.

Arrangement authored this INPUT catalog and retained all2479row locators/line hashes. Thirteen meaningful INPUT controls pass; Root reconstructed all ten three-binary64 words and exact d:hex call tokens. Root's first metadata validator wrongly expected numeric0 rather than the correct literal string+0; it failed before documentation edits or original calls. Its sealed failure remains, and v2 corrects only that field-type assertion, without changing input/evidence bytes. The existing report's shared context/env/target/runtime declarations qualify the six INPUT references, without a new binary/provider read, runtime equivalence proof or output transfer. Fresh capture custody must still establish its own endpoints. No pow, ratio, expected output or native arithmetic was evaluated to choose inputs. The retained schema summary types PitchCoarse/PitchFine as UserFloat, and the observed zero-only inventory gives no complete101-cent/all-fine-pitch partition. That domain, A3/public clip/file/audio admission, general rates and ARM/Apple/FP equivalence remain U; this class is the bounded retained dataset, not a product denominator.

Auto authors ONE `batch-playback-shipped-unwarped-rates-v1` after sealing Electric124. Mix is SOLE actual/source peer after its Corpus3586 final seal; Root remains citation-only for all new Playback actual/source/code/raw/results before any read. Four once-only children each make one selected original call to0x10236f1f0 using the unchanged74792-byte audio xexec/Live163716848 model: three d:hex arguments in XMM0/1/2, no initializer, receiver, integer argument, original construction, patch, tool/build/model/provider/stub or FP change. The saved XMM0 word is the sole proposed native expectation carrier; the other three raw words remain unassigned. There is one frozen packet and one actual/source review, without preparation/readiness/Root gate chains.

All new capture/control/parent/assembler/analysis/checker/finalizer source, exact scripts/context and future artifact guards freeze BEFORE calls. Author post-capture bookkeeping remains metadata-only. Planning16MiB full lifecycle plus128MiB headroom is unreserved; fresh guards admit complete remaining stdout/stderr/receipt/metadata/final allowance and headroom. First detected fault/resource limit stops later children; retain partials, do not retry or relax guards. No old baseline/native-output replay, f0/metric/fit/calibration/tolerance or new portable criterion is selected. Priors, portable expected/comparator/grade remain NULL/appFalse. No new owner ID, release, candidate comparison or closure follows from selection; requiredU/productOPEN.


## Shipped unwarped rate capture author status — 2026-10-21

Auto froze the complete four-missing/six-INPUT-reference packet before any selected call: [pre-call manifest](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/batch-playback-shipped-unwarped-rates-v1/pre-call-manifest.json), 2,339 bytes, SHA256 `78c541c6ccbd6c09e2501bc988f7f7baecacf766c7bad51791af48d484e101aa`, binding all 13 initial payloads (1,881,905 bytes), including the parent, recorder, checker, finalizer, exact initial authoring sources, immutable INPUT authority, context and ten-point catalog. The unchanged selected helper receives four once-only fresh single-call histories; six old points remain INPUT-only references without replay or output/criterion transfer. Mix is the sole independent actual/source peer after final seal; Root is citation-only for all new actual code and results. Capture and author bookkeeping are not independent approval, case admission, portable criteria or public/ARM proof.

## Shipped unwarped rate actual adoption — 2026-10-21

[Mix's sole actual/source review](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/playback-shipped-unwarped-rates-v1-review.json), 2,551,036 bytes, SHA256 `6607fb750a4a9dd68648a5d1f1702f8078e55b09b00b538aae2b6b5bc4679fb5`, approves the four fresh local observations in the ten-history catalog. The [packet manifest](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/batch-playback-shipped-unwarped-rates-v1/manifest.json), 5,012 bytes, SHA256 `803367dca790f43fc62ae9aba6b25ec57aa4224e2ca000b8bacc08ffa3f030a3`, lists 28 payloads/2,781,492 bytes; all 29 files remain readonly. This adoption uses only the approved report summary, with no actual/source/raw/numeric proof replay. Auto authored capture/control source, Mix was the sole peer, and Root remains citation-only for those new payloads.

Four once-only children captured file/engine-rate pairs 22000/44100, 22000/48000, 22050/48000 and 96000/44100, each with supplied semitones positive zero and one receiver-free three-double call. They exited zero without a recorded fault or retry. All four saved XMM0 words are positive normal finite values and distinct; each logs one counted `_powf` use. These are descriptive observations, without a ratio evaluator or fitted law. The six other catalog entries remain qualified INPUT-only references to the earlier 582 class, with no old output, PID, receipt, metric or criterion transfer. Other raw carriers remain unassigned.

The peer read all eight new Python sources and checked all four logs, sixteen raw carriers, twelve host argument words, the complete catalog and readonly tree. Thirty-one independent negative controls and eight unsigned-word positives pass. Seven runtime identities plus thirteen pre-call payload identities form **one common initial snapshot followed by four after-child snapshots: 80 matching pairs**, not per-child-before or continuous custody. Host `strtod` bookkeeping does not attest child entry registers, temporary-float-cast FP flags or native fenv. File-fsync requests do not establish directory/crash durability, OS exec or loaded-provider continuity; cleanup and inherited source-version limits remain.

No owner IDs or release are admitted here. Fresh priors, native expectations, portable expected/comparator and grades remain NULL; application proof is false. General fine-pitch/rate, current clip/file/audio/clock admission, A1–A5/F6/F7 and ARM/Apple behavior remain unresolved. The earlier selection and author-status paragraphs remain historical as-of records. Required unsupported behavior stays U and product coverage OPEN.

## Playback owner R5 shipped-rate annex adoption — 2026-10-21

Root's [sole NEW wording/IDs/mapping/preservation review](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/playback-owner-r5-shipped-unwarped-rates-finite-v1-review.json),4041361bytes/SHA256 `3da7e77dfd793ec52e64789f892df34be45d118f6bb89b8b6c408e216feed8ab`, approves and applies exactly80268bytes/SHA256 `767541e4ab1a4e9da180355c65ee4a5b17797672be89302311d6264ad77e4b92`. The [manifest](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/owner-playback-r5-shipped-unwarped-rates-finite-v1/manifest.json),2595bytes/SHA256 `f209e3e7fe73f1c3794a372b13c8493791feeb4803ab8d24b0c33fdecc719291`, seals12payloads3479015bytes/all13files0444/private0700/exacttree.

Four PBC788–791 map only the sole-approved fresh SAVEDXMM0 observations; full10history catalog retains six INPUT-only references/no newPIDreceiptoutputmetriccriteriontransfer/existingR4IDs navigationonly. Other3rawcarrier semantics remain unassigned. All23wholeREQ/759oldIDs68rows/R3R4objects/criteria/U/history/92releasedobjects remain exact/fullreverse; absentR3individualcatalog metadata is not reconstructed. New priors/portablecriteria/gradesNULL/appFalse; no formula/rate-domain/finepitch/publicclip/ARM law or oldproof repair.

Root FULLread newchecker/historicalstager/README/delta/history INERT before ONLYsafecheck/NEVERstager.26owned28Rootnegative controlsPASS; exactly currentR4+Mixapproved4REPORT+AutoR4ownerREPORTembeddedmetadata. No actual/source/raw/numeric/provider/oldR4proposal/catalog/fixtures proof replay, and no embeddedactualmethodsource copied. The80commoninitial→after custody pairs are NOTperchildbefore; FP/OSexec/provider/source/FDfsync/resource/cleanup qualifications remain.763navigationIDs are not passes/productdenominator; no release/implementation/closure.


## Remaining scalar INPUT class assessment — 2026-10-21

The retained 86 scalar navigation rows are exactly **78 increment inputs plus eight quantization inputs**, not 86 newly missing observations. The [map INPUT inventory](../../analysis/ableton-live-12.4.3/full-spec-v1/family-playback-routes-v1/batch-inputs.json), 375,615 bytes/SHA256 `4e8915af2d8e33d4a81aab293b2ff95a5a3da6d353dafc50c9b1f96b785d2442`, `/batches/4/rows`, separates them from the same batch's 32 gain, 150 kernel and ten shipped-render navigation rows. The 413 clock/state rows retain their earlier supplied-state/setup limits; they are not added to this receiver-free scalar class.

The exact retained [driver INPUT declarations](../../analysis/ableton-live-12.4.3/r2/t13-playback-v1/audio/run_x.py), 16,646 bytes/SHA256 `3d469c231aa4c045a91c476e3cf0219e2669005a387d6539936689ee5a5f3c61`, lines43–49, enumerate semitones `0,1,-1,12,-12,0.5,-0.25,7,24,48,-48,0.01,3.3` at all six declared rate pairs: 48000/48000,44100/48000,48000/44100,96000/48000,22050/44100,44100/44100. That exact span is 388 bytes/SHA256 `a25d6cef549b2459b315254b95d71b580f448965cf87534a6d293484f2d323f7`. INPUT-only binary64/tuple checks find 54 argument intersections with the [already adopted integer582 matrix](#integer-semitonerate-actual-adoption--2026-10-21); the other 24 are the four already recorded fractional semitone values at those six pairs. They do not become new required behavior merely by assigning fresh single-call process histories. Old shared-process calls and the newer single-call histories remain distinct, with no PID, receipt, output or criterion transfer.

Lines64–67 declare the eight quantization inputs (196-byte span/SHA256 `60f60ad065e97c32715997fe0457151a1ce0d85b65bc380fc08c7e716c0e3c7b`). All eight exact binary64 input words already occur in the [117-input catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/batch-playback-standing-leaves-v1/inputs.json), 50,056 bytes/SHA256 `451c5f9a51fd2e1c44a48464ef26385aa53b006f0351b688a0d464f876478757`. That catalog already names its complete bounded anchor/half-step/lattice/representation-boundary neighborhoods. The separately adopted shipped-rate class is also accounted. No old result, formula, comparator, numeric estimator or native-source behavior was reevaluated for these INPUT joins.

The existing unchanged scalar route remains available: `0x10236f1f0` accepts three binary64 `d:hex` arguments, while `0x10235b910` accepts one, through the admitted 74,792-byte audio xexec and pinned Live x86 slice. Neither needs a receiver, buffer, initializer, integer argument or new stub; the inherited loader/image identities and bridge limits are in the [integer INPUT authority](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/playback-integer-semitone-rate-input-eligibility.json). These are retained setup metadata, not fresh executable/provider/entry-register or FP-state proof. All 78 declared increment arguments and eight quantization seed arguments have finite binary64 storage; this says nothing about unselected output behavior or public input admission.

This bounded read identifies **no additional complete missing scalar boundary matrix**. The missing bridge is a source-owned exact input partition with justified boundaries/endpoints and fixed rate/setup context, beyond the already accounted classes; a legal ABI alone does not supply that partition. UserFloat fields and all-zero retained fine-pitch metadata still do not declare an integer-cent or other complete fine domain. No arbitrary fractional grid, clipped slice, parameter crossproduct or replay of the 86 historical rows is proposed. This is not a global exhaustion claim or a ban on future scalar discovery with NULL priors. Public delivery, A1–A5/F6/F7, ARM/Apple behavior and required unsupported predicates remain U; coverage stays OPEN. No capture, new artifact gate, IDs, owner change or shared routing edit follows.
