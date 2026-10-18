# S5 clip launch: analyst notes

Image `analysis/ableton-live-12.4.3/derived/Live.arm64`, SHA-256 `3a99ceea…d1c383cfad`, base
`0x100000000`. Pseudocode from the C1 corpus (`corpus-excerpts.jsonl`, 69 records with chunk,
offset and line SHA-256); disassembly from the query server (`results/s5-000N/`). "✓ s5-000N" marks
a branch read in that round's disassembly. Static only; nothing was executed.

## Pre-round corpus work (no server queries)

- Label strings in the strings index led to four static label lists built under `__cxa_guard`:
  `0x102438b44` (Trigger, Gate, Toggle, Repeat), `0x102438d00` (Global, None, 8 Bars … 1/32; 15),
  `0x102503ea0` (No Action, Stop, Play Again, Previous, Next, First, Last, Any, Other, Jump) and its
  short twin inside `0x102505724` (Again for Play Again). The 14-entry song list and the 9-entry
  record-quantization list are built inside `0x10266f738`.
- UTF-16 member names gave the registries: `0x102435a28` (AClip), `0x1025037a4` (AFollowAction),
  `0x10266c21c` (ASong), `0x1026a292c` (ASongPrefData, class name from `0x1026b987c`) and
  `0x10285d098` (a sample-data class with LaunchMode/LaunchQuantisation/VelocityAmount; not followed).
- `0x102436fc4` initialises AClip; `0x102505030` initialises AFollowAction; `0x10266f738` (caller
  `0x10287a300`) initialises ASong (callbacks named `ASong::InKeyController`, `ASong::ScaleController`).
- Symbolised callbacks: `AClip::UpdateEngineForLaunchParameters` wrapper `0x1024467ac`,
  `LSong::SongQuantisationTime` wrapper `0x1026ac9b8` (tail-jumps to `0x1026787f0`),
  `LSongUnit::OnGlobalQuantizationChanged` wrapper `0x1026cc7a4`.
- `0x101aaae44` (callers listed by the calls index: 29 sites) maps a song-quantization index and a
  (numerator, denominator) pair to a grid length in beats.
- Python binding registrations: `0x103abc6e8` (Clip; corpus decompile timed out) and `0x103ba8520`
  (Song).
- Translators registered in `0x10148ec98`: `0x101493140` (0x11, Clip/AudioClip/MidiClip; also 0x16,
  SampleData), `0x10149491c` (0x29, Song…), `0x1014b6d14` (0x196), `0x1014b82d8` (0x1a1),
  `0x1014b8b00` (0x1a5), `0x1014bb048` (0x2ee8), `0x1014c04d0` (0x2fab, Scene).
- Negative: `0x1022f1ff4` matched the 1/6-1/8-1/3 constant search but is a ruler-step chooser
  (seconds/frames), unrelated. `0x101ec84c8`…`0x101ecfbb4` call the grid function with the Looper's
  own quantization (`OLooperProcessor::OnLaunchQuantizationEnum` lies beside them); excluded.

## Round 1 — s5-0001 (8 dossiers)

`0x101aaae44`, `0x102442998`, `0x102436fc4`, `0x102505030`, `0x102505724`, `0x10266f738`,
`0x101ad0130`, `0x1011be6c8`. Resolved:

- Grid function ✓: `sub w8,w1,#1; cmp w8,#0xc; b.hi` default 0.0; jump table bytes at
  `0x105846ef8` = 00 7a 37 61 2f a4 aa 76 ae 33 ac 2b 31 (read with `read_ptrs.py`), targets
  `0x101aaae68 + 4*b`. bar = 4·n/d rounded to 1/3,843,840 unless it equals one of the sentinels at
  `0x1055d9680` (−1.7976931348623155e308, +1.7976931348623155e308, DBL_MAX, +inf). 1→8·bar, 2→4·bar,
  3→2·bar, 4→bar, 5→2, 6→4/3, 7→1, 8→2/3, 9→1/2, 10→1/3, 11→1/4, 12→1/6, 13→1/8.
- Clip grid `0x102442998` ✓: reads LaunchQuantisation at `[clip,#0x258]`; non-zero → grid(clip time
  signature from `[clip,#0x1d8]`, value−1); zero → `0x10268ce9c(song)` (song grid) when a song is
  passed, else −1.0.
- Floor/ceil helper `0x1011be6c8(t, g, anchor, mode)` ✓: mode 0 `frinta`, 1 `frintp` (ceil),
  2 `frintm` (floor); other modes or g = 0 skip the step; result rounded to 1/3,843,840. The corpus
  pseudocode shows a truncating cast for all modes; the disassembly corrects it.
- AClip init ✓: Legato `[#0x68]` false, Ram `[#0x80]` false, Disabled `[#0x148]` false;
  VelocityAmount `[#0x3b8]` UserFloat (s0 0.0, s1 1.0, s2 0.0) with converter (0, 1, 0.01, 0.001);
  LaunchMode `[#0x270]` and LaunchQuantisation `[#0x258]` initial values come from
  `0x1026ab2ec`/`0x1026ab2f4` on the `0x102676cf0` object when `0x101849958` is non-null, else 0;
  labels `0x10700a120`/`0x10700a138`; callback `0x106534a58` (UpdateEngineForLaunchParameters).
- AFollowAction init ✓: FollowTime `[#0x78]` 4.0 then `0x101565624(…,1,1)` (sets the +0x70 quantize
  flag); IsLinked `[#0x90]` true; LoopIterations `[#0xa8]` value 1, packed bounds 0x3fffffff00000001;
  `0x102505724` for A (s0 100.0, w2 4) and B (s0 0.0, w2 0); FollowActionEnabled `[#0x120]` false.
- `0x102505724` ✓: enum init with long and short labels; chance UserFloat (0, 100, default arg);
  jump index UserFloat (−1.0, 8388608.0, 1.0); chance controller `0x10652b4d8`.
- ASong init ✓: SmpteFormat `[#0x328]` 0 (6 labels), GlobalQuantisation `[#0x388]` 4 (14 labels
  `0x10700c740`), AutoQuantisation `[#0x3c0]` 0 (9 labels `0x10700c758`). Label order read from
  string-reference order (`strrefs.py`).
- Fire computation `0x101ad0130` ✓ (`0x101ad06cc`–`0x101ad0924`): d12 = `0x101acffa4(...)`;
  d3 = engine song time `[song,#0x70]` rounded; d11 = requested time unless it is DBL_MAX, then d3;
  if d12 > 0, d11 = `0x101abf294(d11, d12, song+0x38, 1)`; later (unless skipped) d9 =
  `0x101ad1418(...)`, d8 = d11 − d3; if d9 > d8: if `0x101acfe68` and d12 ≠ 0 then d11 += d12 else
  d9 = d8.

## Round 2 — s5-0002 (8 dossiers)

`0x102438d00`, `0x101abf294`, `0x101acffa4`, `0x10245efa0`, `0x1014b8b00`, `0x101493140`,
`0x101567bfc`, `0x103abc6e8` (decompile timeout; disassembly complete). Resolved:

- Clip label order ✓ (pseudocode had lost four arguments).
- `0x101abf294` ✓: anchor = `fmaxnm([ts,#8], 0)`, tail-call `0x1011be6c8`.
- `0x101acffa4` ✓: returns 0.0 when quantization is off (w1 = 0) or, in the immediate-check path,
  when the song is not playing, the slot is −2 or the track condition matches; an override index
  ≤ 13 (`cmp w6,#0xd; b.ls`) uses grid(song signature at `+0x38`, index); otherwise the slot's
  precomputed grid at `[[slot,#0x50],#0x50]` when ≥ 0, else (flag set) grid(song signature, engine
  global value from `0x101b0e1c0`).
- `0x10245efa0` ✓: builds `OSlotFireData.Create`; sends Legato `[clip,#0x68]` only when vtable
  `+0x300` returns non-zero, follow-action data (`0x10250416c`), launch mode (`0x10243f7f8`, value of
  `[clip,#0x270]`) and `0x102442998(clip, 0)` (so Global is sent as −1.0).
- `0x1014b8b00` ✓ (translator 0x1a5): IsLinked := true and FollowActionA := 4 iff
  FollowActionEnabled false, A = 0, B = 0 and FollowTime = 4.0; otherwise IsLinked := false.
- `0x101493140` ✓ (translator 0x11): LaunchQuantisation < 11 remapped through the int table at
  `0x105815e9c` = 0,1,2,3,4,5,6,8,10,12,14; ≥ 11 raises `Enum value out of range`.
- `0x101567bfc` ✓: enum init stores value at +0xd8 and +0xdc, labels at +0x90/+0x98.
- `0x103abc6e8` ✓: Python `LaunchMode` trigger 0, gate 1, toggle 2, repeat 3;
  `ClipLaunchQuantization` q_global 0 … q_thirtysecond 14; `GridQuantization` names g_8_bars …
  (values not needed). Property getters `0x103ac1e94` (launch_mode → `[clip,#0x270]`), `0x103ac1ed0`
  (launch_quantization → `[clip,#0x258]`).

## Round 3 — s5-0003 (8 dossiers)

`0x1025044b4`, `0x1026787f0`, `0x103ba8520`, `0x10250416c`, `0x1014b82d8`, `0x1026e3698`,
`0x101acfe68`, `0x1014b6d14`. Resolved:

- AFollowAction post-load `0x1025044b4` ✓: A = B = 0 → ChanceA := 100 through slot `+0x280` and
  FollowActionEnabled := false; else ChanceA := `frinta`(A / ((A+B)/100)), ChanceB := 100 − ChanceA.
  The corpus pseudocode shows a truncating cast; the disassembly shows round-to-nearest.
- `0x1026787f0` ✓: song grid = grid(time signature via `0x1026e3698`, `[[x19,#8],#0x388]`).
- `0x1026e3698` ✓: (numerator, denominator) = (`fcvtzs` of `+0x78` value, `fcvtzs` of `+0x90` value).
- `0x103ba8520` ✓: Python `Song.Quantization` q_no_q 0 … q_thirtytwoth 13 (spellings as in binary:
  q_eight, q_sixtenth, q_thirtytwoth); `RecordingQuantization` rec_q_no_q 0 … rec_q_thirtysecond 8.
- `0x10250416c` ✓: sends FollowTime, LoopIterations only when IsLinked (else 0x80000000), A, B,
  chances and jump indices (converted to int).
- `0x1014b82d8` ✓ (translator 0x1a1): when FollowActionEnabled is absent, Enabled :=
  (A ≠ 0 ∧ ChanceA ≠ 0) ∨ (B ≠ 0 ∧ ChanceB ≠ 0).
- `0x101acfe68` ✓: true iff engine song byte `+0x68` = 1 and `[song,#0x98]` ≠ `[track,#0x3b0]`.
- `0x1014b6d14` ✓ (translator 0x196): moves FollowTime (default 1.0 if absent), FollowActionA/B,
  FollowChanceA (default 1.0) and FollowChanceB (default 0) from the clip into a new FollowAction.

## Round 4 — s5-0004 (8 dossiers)

`0x1033bbe98`, `0x1033bc00c`, `0x1015743b0`, `0x10157432c`, `0x10155afc8`, `0x1014c04d0`,
`0x1026cc7a4`, `0x101ad1418`. Resolved:

- API setters ✓: launch mode `cmp w1,#4; b.cs` throws `Invalid launch mode`; launch quantization
  `cmp w1,#0xf; b.cs` throws `Invalid launch quantization`. Velocity amount setter `0x1033bc1a4`
  (pseudocode only) checks against the float's bounds and throws `Clip velocity amount … is out of range`.
- UserFloat init ✓: `stp s0,s1,[x0,#0x80]; str s2,[x0,#0x88]` then sets the value to s2; the
  bound getters `0x1015748cc`/`0x1015748e8` read +0x80/+0x84 (pseudocode). Hence VelocityAmount
  (0, 1, 0), chance (0, 100, default), jump index (−1, 8388608, 1).
- `0x10155afc8` ✓: RangedRemoteableInt stores w1 at +0x78 and the packed pair at +0x7c.
- `0x1014c04d0` (translator 0x2fab, Scene; pseudocode read, disassembly retained): creates a default
  FollowAction (4.0, 1, 0, 0, 100, 0, false, 1, 1, IsLinked true) when absent; otherwise IsLinked :=
  (¬Enabled ∧ FollowTime = 4 ∧ A = 4 ∧ B = 0 ∧ ChanceA = 100 ∧ ChanceB = 0).
- `0x1026cc7a4`: on change, posts the GlobalQuantisation value to the engine (`0x101a9c534`).
- `0x101ad1418`: the offset d9 comes from a virtual call (`+0x48` on `0x101acff34()` or `+0x18` on
  `[track+0xa0]` with the float at `[song,#0x1c]`). Not resolved; recorded as unknown.

## Static checks run

- `check_registry_order.py`: 28 persistent AClip registrations equal AudioClip and MidiClip fields
  after `Time`; 10 AFollowAction registrations equal FollowAction; ASong launch members are in
  LiveSet order.
- Vtables (`read_ptrs.py`): AClip base vtable `0x1067b6cc0` and AFollowAction `0x1067c8830` hold the
  generic loader `0x101487310` at +0x140 and writer `0x101486cdc` at +0x138; post-load +0xd0 is
  `0x102441a30` and `0x1025044b4` respectively.

## Open

Launch-mode semantics inside `0x101ad0130`; the offset d9; the meaning of `[song,#0x98]` versus
`[track,#0x3b0]`; stopped-transport launch; legato and velocity application in the engine; scene
JumpIndex 0 in shipped sets versus constructor default 1.
