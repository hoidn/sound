# Playback core: transport, launch timing and clip playback, release 1

Target: Ableton Live 12 Suite 12.4.3 (2026-07-07_e3d8be4d07), macOS, arm64 and
x86_64 builds. Features: FEAT-TRANSPORT and FEAT-SESSION, with FEAT-MIDI and
FEAT-AUDIO. Parent specification identity: SPEC-PLAYBACK-CORE revision 1.
Release: playback-core-v1. Only the clauses explicitly included below are in
scope. No other clause of a listed requirement is implicitly approved. This
document is self-contained.

**Status: reviewed handoff**, approved with the clarifications in
[the review disposition](REVIEW.md). Application implementation requires a
fresh restricted workspace.

## What the contract means

A user opens a Live Set, then plays it and launches its session clips. This
contract describes, for an offline render of that session at a stated sample
rate, the parts of the output that come before the tracks' devices and mixer:

- the song clock: how song beats map to render samples, Play from a stated
  start beat, Stop, Continue and the song loop;
- on which render sample a session clip launched with its launch button starts,
  in Trigger launch mode, under launch quantization;
- which note-on and note-off events a playing MIDI clip sends into its track's
  device chain, with which velocity and on which render sample;
- which file positions an audio clip with warping off reads for each output
  sample, and the values it produces with direct copy or linear interpolation.

It does not describe instrument or effect audio, the mixer, sends, automation,
tempo changes, clip stop buttons, crossfades between audio clips, fades, the
user interface, recording, the arrangement or undo.

Every expected result carries one of two provenance labels:

- **Extracted-execution arithmetic**: the arithmetic that gives the listed
  sample or value (clock, placement, Stop and Continue, song loop, launch
  boundary, clip position, note events, read step, interpolation, gain) is the
  arithmetic that the original program's x86_64 code computed when it was run
  on stated inputs, on a Linux x86_64 host with glibc in place of the macOS
  system libraries. That playback reaches that code with the case's values is
  derived statically. The macOS arm64 build is inferred to give the same
  results.
- **Static-derived**: derived from static evidence about the target build
  without running it.

None is an observed run of the original application, and none was run against
a candidate. No compatibility result is established. The original application
remains the authority for a later comparison. The results rest on the
[stated assumptions](#stated-assumptions).

## Render conventions and observables

A render is defined by a Live Set file, the WAV files it references, a sample
rate SR in Hz and a script of actions. These conventions define the test
vehicle. They describe no behavior of the original application, which has no
offline render of this kind.

- **Render sample.** Render sample 0 is the first sample processed after the
  script's first Play, or after its first launch while the transport is
  stopped. Indices count up from there without gaps, also while the transport
  is stopped.
- **Request sample.** Each action names the render sample `at` on which it is
  handled. Actions on one sample are handled in script order. When the original
  application handles a user action relative to its audio buffer is not part of
  this contract.
- **Actions.** `play` with `start_beat` (Play from stopped); `stop` (transport
  Stop); `continue` (play without a position change); `launch` of track 1,
  slot 1: a press of that clip slot's launch button. A `launch` with
  `transport` `stopped` and `start_beat` is a launch while stopped.
- **Settled start.** A render starts from a settled state: every ramp that the
  loaded state starts has finished before render sample 0.
- **Note events.** For a MIDI track: the note-on and note-off events that its
  session clip sends into the track's device chain. Each has a render sample,
  a type, a MIDI key and a velocity (a binary32 value, not rounded to an
  integer). Events on one sample have an order.
- **Clip signal.** For an audio track: its session clip's output before the
  track's devices and mixer, one value per render sample on the left and the
  right channel.

## Document scope and preconditions

- Every input is a Live Set: a gzip file (header `1F 8B 08 00 00 00 00 00 02 13`,
  one member) holding XML 1.0 in UTF-8 whose root element is `Ableton` with
  `MajorVersion="5"`, `MinorVersion="12.0_12402"` and `SchemaChangeCount="1"`,
  and whose first child is `LiveSet`. Every fixture is a complete set that
  opens; a candidate that refuses one fails its cases.
- Each set has exactly one track, an audio or a MIDI track, the first item of
  `LiveSet/Tracks`; one scene; one clip, in the track's first session slot; no
  devices, no return track and no automation beyond the one-event tempo and
  time-signature envelopes. Follow actions are off.
- Paths are relative to `/Ableton/LiveSet`. Values are the `Value` attribute of
  the named element unless stated. `clip` is
  `Tracks/*[1]/DeviceChain/MainSequencer/ClipSlotList/ClipSlot[1]/ClipSlot/Value/*[1]`.

| Value | Element |
| --- | --- |
| Song tempo T, BPM | `MainTrack/DeviceChain/Mixer/Tempo/Manual` (the tempo envelope's one event holds the same value) |
| Song time signature | `MainTrack/DeviceChain/Mixer/TimeSignature/Manual`, a code: 200 is 3/4, 201 is 4/4, 202 is 5/4, 302 is 6/8, 303 is 7/8 |
| Global launch quantization | `GlobalQuantisation` |
| Song loop switch, start and length (beats) | `Transport/LoopOn`, `Transport/LoopStart`, `Transport/LoopLength` |
| Clip launch quantization | `clip/LaunchQuantisation` (`clip/LaunchMode` is 0, Trigger) |
| Clip time signature | `clip/TimeSignature/TimeSignatures/RemoteableTimeSignature[1]`, `Numerator` and `Denominator` |
| Clip loop start, loop end, start offset, loop switch | `clip/Loop/LoopStart`, `LoopEnd`, `StartRelative`, `LoopOn` |
| Notes of a MIDI clip | `clip/Notes/KeyTracks/KeyTrack[1]/Notes/MidiNoteEvent`: attributes `Time`, `Duration`, `Velocity`, `VelocityDeviation`, `OffVelocity`, `Probability`, `IsEnabled`; the key is `KeyTrack[1]/MidiKey` |
| Audio clip settings | `clip/IsWarped`, `HiQ`, `Fade`, `PitchCoarse`, `PitchFine`, `SampleVolume` |
| Audio file | `clip/SampleRef/FileRef/RelativePath`, relative to the folder of the set (`RelativePathType` 1); its rate and length are `SampleRef/DefaultSampleRate` and `DefaultDuration` |

- Every number is written so that its text is exactly the value meant: the
  tempos are exact binary32 values, and note times and lengths are exact
  multiples of 1/3,843,840 beat (some written as the nearest binary64 value,
  such as `1.3333333333333333` for 4/3). Expectations assume a host locale whose
  decimal separator is `.`.
- Every MIDI clip has `IsWarped` true, `VelocityAmount` 0, `GrooveId` −1, one key
  and notes with `VelocityDeviation` 0 and `Probability` 1, none overlapping
  another. Every audio clip has `IsWarped` false, `Fade` false, `LoopOn` false,
  `StartRelative` 0, `PitchFine` 0 and refers to a 16-bit PCM mono WAV file
  whose rate and frame count equal the stored values; its `LoopEnd` (0.01 s)
  times the file rate is the frame count.

## Terms

| Term | Meaning |
| --- | --- |
| Lattice, L(x) | Rounding to a multiple of 1/3,843,840 beat, halves away from zero, by the binary64 formula s × (⌊\|x + s × h/2\| × 3,843,840⌋ ÷ 3,843,840), with h the binary64 value of 1/3,843,840 and s the sign of x. A lattice beat is a value L returns, taken as the exact multiple of 1/3,843,840 it stands for |
| T | The song tempo in BPM as a binary32 value (REQ-PLAYBACK-CORE-003) |
| spb, bps | Samples per beat (SR ÷ T) × 60 and beats per sample 1 ÷ spb, each operation in binary64 |
| Anchor | A pair (render sample n_a, song beat b_a) from which song time is counted |
| P(b) | For lattice beat b and anchor (n_a, b_a): n_a plus the least integer at or above the exact value of (b − b_a) × SR × 60 ÷ T, with b as its lattice multiple and b_a as its exact binary64 value |
| Transport playing | Between a Play (or a launch while stopped) or a Continue and the next Stop |
| Press beat t | The song beat at the request sample of a launch, rounded by L |
| Pass | One run of a MIDI clip through its loop region |

## Stated assumptions

These are supported by the evidence but not established. A case lists the ones
it depends on. If one fails, the clauses that use it have no expectation.

- **AS-1.** The macOS arm64 build follows the rules that were run on, or
  derived only from, the x86_64 build: the clock and launch arithmetic, the
  order of note events at one beat, the song beat of a note in a clip's first
  pass, which notes start or are cut in a pass, the velocity path, the read
  step, the interpolation (within the stated tolerance) and the silence past
  a file's end.
- **AS-2.** An audio clip's stored `IsWarped`, `HiQ`, `Fade`, `SampleVolume`,
  `PitchCoarse` and `PitchFine` are the values its playback uses, and a
  session clip never starts in a crossfade.
- **AS-3.** While a set is open, the global launch quantization in effect is
  the stored `GlobalQuantisation`.
- **AS-4.** In a set whose time signature never changes, launch grid lines lie
  at whole multiples of the grid length from song beat 0.
- **AS-5.** For a transposition other than 0, and for the clip gain, the macOS
  C library gives the same binary32 power and decibel-to-gain values as the
  x86_64 runs got from glibc. The cases state the read step and the gain they
  use.

## Selected requirement clauses

Each clause is included only as stated. Labels: **X** extracted-execution
arithmetic with a static-derived path; **S** static-derived.

### REQ-PLAYBACK-CORE-001

The song clock (partial).

1. **X.** spb = (SR ÷ T) × 60 and bps = 1 ÷ spb in binary64. At 48,000 Hz spb
   is 24,000 at 120 BPM, 32,000.000000000004 at 90 BPM and 20,571.42857142857
   at 140 BPM; at 44,100 Hz it is 29,400 at 90 BPM and 22,050 at 120 BPM.
2. **S, X.** The song beat at render sample n is b_a + (n − n_a) × bps in
   binary64, from the anchor in effect. Play, Continue and a song-loop jump set
   a new anchor (REQ-PLAYBACK-CORE-004 to 006). Song time is never accumulated
   sample by sample.
3. **S.** Results do not depend on the size of the buffers in which a render
   is processed.

### REQ-PLAYBACK-CORE-002

Placing an event on a render sample (partial). Applies to note events, a
clip's loop wraps and end, launches and song-loop jumps.

1. **S.** An event's beat is first rounded by L.
2. **X.** An event at lattice beat b, with anchor (n_a, b_a), takes effect on
   render sample P(b) when the exact value of (b − b_a) × SR × 60 ÷ T is not an
   integer, and when it is an integer and the binary64 product of the binary64
   difference b − b_a and spb does not exceed it. Otherwise it takes effect on
   P(b) or on P(b) + 1. Which of the two occurs is not specified: it depends on
   a sample counter that neither the set nor the script determines. Such events
   list both samples, and either is correct. Examples at 48,000 Hz: at 120 BPM
   every case position is exact; at 90 BPM a whole beat b falls on 32,000 × b or
   32,000 × b + 1; at 140 BPM beat 1 falls on 20,572.
3. **S (AS-1).** Events at the same beat are handled in this order: note-off,
   then a clip's loop wrap or end, then note-on.

### REQ-PLAYBACK-CORE-003

Tempo (partial).

1. **S.** The song tempo is used as the binary32 value of the stored tempo.
   The cases store tempos that are exact binary32 values, among them
   121.1999969482421875 (the binary32 value nearest 121.2) and
   93.33333587646484375 (nearest 280/3).

### REQ-PLAYBACK-CORE-004

Play from stopped (partial).

1. **S, X.** Play with start beat t\* rounds t\* by L and raises a negative
   value to 0. Song beat t\* plays on render sample 0, an event at t\* takes
   effect on render sample 0, and the anchor is (0, t\*).
2. The script states t\*. Which start beat the original application uses for
   its own Play control after opening a set is outside this release.

### REQ-PLAYBACK-CORE-005

Stop and Continue (partial).

1. **X.** Stop handled at request sample R ends playback there. The song beat
   stays at the beat of sample R, and no later sample advances it.
2. **X.** Continue handled at R′ resumes from that beat, with anchor
   (R′, that beat). Example at 48,000 Hz and 140 BPM from beat 0: Stop at
   30,000 holds beat 1.4583333333333335; after Continue at 35,000, beat 3 is
   at 35,000 + 31,715 = 66,715.

### REQ-PLAYBACK-CORE-006

The song loop (partial). Applies while the transport plays with
`Transport/LoopOn` true, start s ≥ 0 and stored length ℓ.

1. **S.** The loop length is used as at least 1 beat. The loop end is
   e = L(s + max(ℓ, 1)).
2. **S, X.** When the song beat reaches e, song time jumps to s on that
   sample: the jump sample is the placement of e (REQ-PLAYBACK-CORE-002) from
   the anchor in effect, and the anchor becomes (jump sample, s). The loop
   start itself causes no jump, and a Play at or after e never jumps.
   Examples: 48,000 Hz, 120 BPM, loop 4 to 8, Play from 4: jumps at 96,000,
   192,000, 288,000 and 384,000; at 140 BPM every 82,286 samples; 44,100 Hz,
   140 BPM, Play from 0: no jump at beat 4 (75,600), then jumps at 151,200,
   226,800 and 302,400; loop 2 to 2 + 10/3 at 48,000 Hz and 120 BPM: 128,000,
   208,000 and 288,000; Play from 10 with loop 4 to 8: no jump.
3. **S.** A session clip that is playing is not moved by a jump: each later
   event of the clip is at its beat minus (e − s), from the new anchor. In every
   case of this release that gives the same samples as placing the event as if
   song time had not jumped.

### REQ-PLAYBACK-CORE-007

Launch request and grid (partial).

1. **S.** A press on a session clip slot's launch button is a quantized
   launch with no explicit time, fire velocity 1, no legato and no quantization
   override. The script's `launch` is this press.
2. **S (AS-3).** The grid is chosen as follows:
   - clip `LaunchQuantisation` k from 2 to 14: global value k − 1 with the
     clip's own time signature;
   - k = 0 (Global): the set's `GlobalQuantisation` with the song's time
     signature;
   - k = 1 (None), or Global with `GlobalQuantisation` 0 (None): no grid.
3. **X.** Grid lengths of global values 1 to 13, with
   bar = L(4 × n ÷ d) beats for time signature n/d, in binary64:

| Global value | Setting | Grid (beats) |
| --- | --- | --- |
| 1 | 8 Bars | 8 × bar |
| 2 | 4 Bars | 4 × bar |
| 3 | 2 Bars | 2 × bar |
| 4 | 1 Bar | bar |
| 5 | 1/2 | 2 |
| 6 | 1/2T | the binary64 value nearest 4/3 |
| 7 | 1/4 | 1 |
| 8 | 1/4T | the binary64 value nearest 2/3 |
| 9 | 1/8 | 0.5 |
| 10 | 1/8T | the binary64 value nearest 1/3 |
| 11 | 1/16 | 0.25 |
| 12 | 1/16T | the binary64 value nearest 1/6 |
| 13 | 1/32 | 0.125 |

The note values do not depend on the time signature: 1/2 is 2 beats in 6/8.
These lengths and the boundary arithmetic of REQ-PLAYBACK-CORE-008 are stated
here so that the release is self-contained.

### REQ-PLAYBACK-CORE-008

Launch boundary and pre-delay (partial). For a launch with grid g > 0 handled
at request sample R while the transport plays:

1. **X, path S.** The press beat is t. The launch boundary is
   B = L(⌈t ÷ g⌉ × g), every operation in binary64 with g from the table
   (AS-4). For bar grids and the note values 2, 1, 1/2, 1/4 and 1/8, B is the
   first grid line at or after t. For a triplet grid it is not always: a press
   exactly on a triplet line can give the next line (1/4T with t exactly 10/3
   gives B = 4).
2. **X, path S.** The track supplies a pre-delay of 0 on a MIDI track, and on
   an audio track on which no clip is playing (AS-2). A launch in this release
   therefore never moves to B + g.

### REQ-PLAYBACK-CORE-009

Launch activation (partial).

1. **S.** With pre-delay 0 the launch takes effect at B, and the clip's start
   plays at song beat B.

### REQ-PLAYBACK-CORE-010

Launch without a grid, and launch while stopped (partial).

1. **S.** With no grid, B = t: the clip's start plays at the press beat. Its
   notes are then placed as in REQ-PLAYBACK-CORE-011 and 002.
2. **S.** A launch while the transport is stopped, with start beat 0, sets the
   song position to 0, computes B from it and starts the transport. The clip's
   start plays at render sample 0 whatever its grid.

### REQ-PLAYBACK-CORE-011

MIDI clip region and position (partial). Applies to a session `MidiClip` with
`IsWarped` true.

1. **S.** Its playback depends on the start S = L(`LoopStart` + `StartRelative`),
   the loop start Ls = `LoopStart`, the loop end Le = `LoopEnd` and `LoopOn`.
   `OutMarker`, `HiddenLoopStart`, `HiddenLoopEnd`, `CurrentStart` and
   `CurrentEnd` do not affect it.
2. **X.** For a clip whose start plays at song beat B, the clip time at song
   beat B + d is L(S + d). A looped clip folds it into [Ls, Le). An unlooped
   clip ends when the clip time reaches Le.
3. **S (AS-1).** A looped clip's first pass runs from B to W₁ = L(B + Le − S);
   pass k + 1 runs from W_k to W_{k+1} = L(W_k + Le − Ls). A note at clip time c
   sounds at song beat L(B − S + c) in the first pass and at L(W_k − Ls + c) in
   pass k + 1. An unlooped clip has one pass, which ends at L(B + Le − S).

### REQ-PLAYBACK-CORE-012

MIDI note events (partial).

1. **X, path S.** For each enabled note in a pass, the clip sends a note-on at
   the song beat of its `Time` with its `Velocity` (binary32, not rounded: 63.5
   is sent as 63.5), and a note-off at the song beat of L(`Time` + `Duration`)
   with its `OffVelocity`. Each is placed by REQ-PLAYBACK-CORE-002 from the song
   anchor.
2. **X.** A zero-length note's note-off is one lattice step (1/3,843,840 beat)
   after its note-on.
3. **X.** A note with `IsEnabled` false sends nothing.

### REQ-PLAYBACK-CORE-013

Which notes sound in a pass (partial). **S (AS-1).**

1. A note starts only if its note-on lies inside the pass: at or after the
   pass's start (clip time S in the first pass, Ls later) and before Le. A note
   already under way at S when the clip starts is not started.
2. A note-on exactly at Le never plays.
3. A note-off exactly at Le is sent, with its own `OffVelocity`, before the
   wrap.

### REQ-PLAYBACK-CORE-014

Note-offs from wraps and ends (partial). **S (AS-1).**

1. With Ls = 0, a note still sounding when a pass reaches Le is cut at the wrap
   with velocity 64, before the next pass's note-ons.
2. A note still sounding when an unlooped clip ends gets a note-off with
   velocity 64 on the clip's end sample.

### REQ-PLAYBACK-CORE-015

Velocity and timing of notes (partial).

1. **S.** With `VelocityAmount` 0, `VelocityDeviation` 0, `Probability` 1 and
   `GrooveId` −1, the velocity sent is the stored velocity, every enabled note
   plays and note times are not changed.

### REQ-PLAYBACK-CORE-017

Unwarped audio clip: start, read step and read position (partial). Applies to
a session `AudioClip` with `IsWarped` false (AS-2).

1. **S.** `LoopStart`, `LoopEnd` and `StartRelative` are seconds of file time.
2. **X.** The transposition is t = `PitchCoarse` + 0.01 × `PitchFine` in
   binary32, limited to −48 to +48.
3. **X (AS-5 for t other than 0).** The read step is the binary32 power of
   the binary32 value of 2^(1/12) raised to t, times file rate ÷ SR in binary64.
   It is held in 32.32 fixed point as F = ⌊step × 2³² + 0.5⌋. Values in the
   cases: 4,294,967,296 (step exactly 1); 3,946,001,203 (44.1 kHz file at
   48,000 Hz); 4,674,794,336 (48 kHz file at 44,100 Hz); 8,589,939,712
   (+12 semitones, 48 kHz file at 48,000 Hz).
4. **S.** The first frame f₀ is the integer part of the binary64 product of the
   file rate and `LoopStart`, with fraction 0. Output k of the clip reads the
   fixed-point position p_k = f₀ × 2³² + k × F, accumulated exactly: frame
   i = ⌊p_k ÷ 2³²⌋ and fraction r = p_k mod 2³². `LoopStart` 0.00251 s of a
   48 kHz file gives frame 120 with fraction 0.
5. **S.** With pre-delay 0, output 0 of the clip is on the render sample on
   which its launch takes effect.

### REQ-PLAYBACK-CORE-018

Unwarped audio clip: interpolation (partial).

1. **X.** When F is exactly 2³², output k is frame f₀ + k, whatever `HiQ` says.
2. **X (AS-1).** With `HiQ` false and any other F, output k is linear
   interpolation in binary32: with f the binary32 value of r × 2⁻³² and x_i the
   frame values, the output is the binary32 sum of the binary32 products
   (1 − f) × x_i and f × x_{i+1}, where 1 − f is also binary32.

### REQ-PLAYBACK-CORE-019

Unwarped audio clip: gain, channels and sample format (partial).

1. **X (AS-5).** The clip gain g is `SampleVolume` as a linear factor. It is
   used within 1.2e-7 relative of its binary32 value and limited to
   3.1622776e-4 (−70 dB) to 15.848933 (+24 dB). `SampleVolume` 0 plays at
   −70 dB, not silence. Each output is the binary32 product of the interpolated
   value and g. Values in the cases:

| `SampleVolume` text | g |
| --- | --- |
| `1` | 1 |
| `0.5011872336272722` | 0.5011872053146362 |
| `0` | 0.0003162277571391314 |
| `10` | 9.999999046325684 |
| `20` | 15.848933219909668 |

2. **S, X.** A mono file plays identically on the left and the right channel.
3. **S.** A 16-bit PCM frame is read as its signed value ÷ 32,768.

### REQ-PLAYBACK-CORE-020

Unwarped audio clip: fade off and the file end (partial). **S (AS-1, AS-2).**

1. With `Fade` false there is no fade: the gain is g from the first output.
2. Past the file's last frame the output is silence.

## Excluded behavior and inputs

Requirements not released: REQ-PLAYBACK-CORE-016 (per-note expression),
REQ-PLAYBACK-CORE-021 (an unwarped clip's end sample and its independence of
tempo; with `Fade` false its end is not visible in the clip signal),
REQ-PLAYBACK-CORE-022 (clip stop buttons, Stop All Clips, empty-slot presses
and quantized stops) and REQ-PLAYBACK-CORE-023 (clips after a transport Stop
and a new Play).

Parts of the included requirements without an expectation:

- which start beat the original's own Play control uses after opening, what its
  transport controls do, and which gestures other than the launch button reach
  the launch path;
- which of P(b) and P(b) + 1 occurs where both are listed;
- tempo changes; the tempo limits; a second Stop; Play after Stop; Stop or
  Continue while a clip plays;
- the song loop switched or changed during playback; a loop start below 0; a
  launch whose boundary is at or after the loop end; any event on the beat of
  a jump; a launch on the beat of a note event;
- the launch sample and the audio during a crossfade between audio clips
  (pre-delay above 0); a launch on a track whose clip is playing;
- note chasing; extra messages at a transport Stop; retriggered notes; the cut
  velocity when the loop does not start at 0;
- notes overlapping another note of the same key, two notes at one time on a
  key, a zero-length note followed by a note at the same time, and probability
  groups; `VelocityAmount`, `VelocityDeviation` or `Probability` other than 0,
  0 and 1; MIDI clips with `IsWarped` false;
- `LaunchQuantisation` outside 0 to 14 and `GlobalQuantisation` outside 0 to
  13; launch modes other than Trigger; legato;
- audio clips with `Fade` true, `HiQ` true with a step other than exactly 1,
  `StartRelative` other than 0, `LoopOn` true, warping on, `PitchFine` other
  than 0 or a transposition other than 0 and 12; files other than 16-bit PCM
  mono WAV; a region shorter than the frames that remain after the first frame;
  fade values; the interpolated outputs next to the file's last frame;
- set content other than the fixtures' form (see the preconditions).

## Cases and comparison

Each case in [cases.json](cases.json) gives a fixture, its sample files, the
sample rate, the script, the expected result, informative values, the
provenance label and the stated assumptions it depends on.

- **Set.** The set must open (`outcome` `opens`).
- **Note events.** The note events of track 1 whose render sample lies in the
  window [from, to) must form exactly the listed sequence: the same number, in
  the same order. Each event's render sample must be one of its listed
  `samples`; where two are listed, either is correct. Type, key and velocity
  compare exactly; a binary32 velocity compares after exact widening.
- **Clip signal.** At every listed render sample, the left and the right
  channel must each equal the listed value within the window's tolerance:
  `exact` (bit-exact), `relative` (|a − e| ≤ value × |e|; used with a gain other
  than 1) or `absolute` (|a − e| ≤ value; used for linear interpolation, two
  binary32 units in the last place of the largest frame magnitude the window
  reads). Samples outside the windows are not compared.
- `informative` values (samples per beat, press beat, grid, boundary, song-loop
  jump samples, read step, first frame, gain) help to understand a case and are
  not compared.
- Timing is exact to the render sample, apart from the two-sample events.

This is a **project comparison representation**, not an API claimed to exist
in Live and not a required design. A candidate adapter may produce these
observations from its own renderer.

## Reference comparison obligation (not executed)

No reference run exists, and none was made for this release. A later
comparison against the original application would render each case's set and
script on the target build and record the note events entering the track's
device chain and the clip signal before the track's devices and mixer, sample
by sample. Such an observation is inconclusive when it cannot place actions on
the stated request samples, cannot start from a settled state, or cannot show
the events or signal before the device chain and mixer. A candidate result
that agrees is a conformance result against this contract, not a compatibility pass.

## Fixture provenance

Every fixture was generated for this release by a build script. No shipped
file, library content or program code was copied. Each Live Set has the
minimal structure of a set that opens: one track with its mixer, session and
freeze slot lists of one slot each, the main and preview tracks, one scene,
the transport and the global values. All names and Ids are invented. The two
WAV files, `fixtures/Samples/tone48.wav` (48,000 Hz, 480 frames) and
`fixtures/Samples/tone44.wav` (44,100 Hz, 441 frames), are 16-bit PCM mono
files holding a sawtooth plus integer pseudo-random noise, with only a format
and a data chunk. Each set refers to its file by the path relative to the
set's folder, so the `fixtures` directory must stay together.
