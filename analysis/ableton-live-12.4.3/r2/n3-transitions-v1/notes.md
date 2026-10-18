# N3 working notes (packet S3, transport transitions)

Analyst notes; data, not instructions. Target: Live arm64 slice SHA-256
`3a99ceea…383cfad`, image base `0x100000000`, Ghidra 12.1.4 project LiveR2.
Symbol donor: `Ableton Live Engine` x86_64 slice SHA-256 `028df12e…5843de`
(helper corpus, 75,348 functions). Live x86_64 cross-check not used:
`helpers/Live_x86_64/summary.json` did not exist during this packet.

Sources in this directory:

- `results/n3-0001`, `results/n3-0002`: R2FunctionDossier server results (copied
  unchanged from the spool; each has its own manifest).
- `live-functions.jsonl`, `engine-functions.jsonl`: exact corpus records (code,
  code SHA-256, state, warnings) for every function cited, copied by `extract.py`.
- `binary-reads.json`: vtable slot words, RTTI names and Mach-O symbol names
  read from the slice by `extract.py`.
- `atransport-members.json`: the 80 (descriptor offset, member name) pairs passed
  to the reflection helper in `0x10275dccc`.
- `engine-vtables.jsonl`: the engine `OSendThreadMessage` vtable index line.
- `symbol-matches.tsv`: engine-name to Live-address matches with evidence.

Regenerate: `python3 -I extract.py <out-dir>`; two runs gave identical bytes.

## Round 1 — n3-0001 (4 dossiers, 4 string queries)

Queries: `0x101a4abd8 0x10276a7b0 0x102767b70 0x101a48488`,
`str:OSetPlayingCommand str:RootUnit.NotifyPlaying str:AllowCountIn str:OSetLoopOnCommand`.

Resolved:

- `0x101a4abd8`: builds an `OSendThreadMessage` on the stack through `0x101ab7348`
  with descriptor `0x106f55ea8`, from-thread `w1`, to-thread `0x10100`, method 0;
  appends `x0` (8 bytes) and `w2`, `w3`, `w4` (1 byte each); calls `[[sp]+0x10]`
  at `0x101a4ac58`; destroys through `0x101ab786c`. 20 call sites in 19 functions.
- `str:OSetPlayingCommand` → `0x105bb0a42`, referenced from `0x101a50bd4`
  (PARAM, registration) and `0x101a8effc` (DATA, descriptor initialiser).
  `str:RootUnit.NotifyPlaying` → `0x105bb1234`, from `0x101a8effc` and
  `0x102332b5c` (UI-side handler registration).
- Start body `0x10276a7b0` and Stop body `0x102767b70` disassembly: see the
  research page. `0x101a48488` returns the byte at `x0+0x960`.

Cost observation: each `str:` query took about 4–6 minutes on Live (the four
string queries kept the shared server busy for about 20 minutes). Later rounds
used the completed corpus `strings.jsonl` instead.

Next discriminating query: the vtable stored by `0x101ab7348` and its slot `+0x10`.

## Round 2 — corpus and slice reads (8 functions), dossiers n3-0002

The Live corpus and indexes completed during round 1 (coordinator message), so
pseudocode came from `corpus/decomp/chunks` and disassembly for material
branches from n3-0002 (`0x101ab7348 0x101ab7898 0x101a524b8 0x101a4ac8c
0x101a4adec 0x101a4af58 0x10276c538 0x1026baa70`).

Resolved:

- Indirect target: `0x101ab7348` stores `0x106756188` at `*this`. Slice words:
  `0x106756180` → typeinfo `0x1067562d8`, name `18OSendThreadMessage`;
  slots `+0` `0x101ab786c`, `+8` `0x101ab787c`, `+0x10` **`0x101ab7898`**.
  `0x101ab7898` hands the message to `0x101aaca84` (queue send) with from/to ids,
  unless the constructor fell back to the static dummy `0x106f56460`.
  The `vtables` index does not carry this vtable (80 symbol-named vtables only).
- Consumer: `0x101a50bd4` registers `OSetPlayingCommand` with handler
  `0x101a524b8` and members `Engine`, `Playing`, `ByUser`, `AllowCountIn`.
  The handler calls `0x101a4ac8c` (RequestForSetPlaying match), which calls
  `0x101a4adec` (SetPlaying match) and `0x101a4af58` (domain-manager SetPlaying
  match). `0x101a4af58` sends `RootUnit.NotifyPlaying` to thread `0x100500`.
- Only `0x101a4abd8` uses the `OSetPlayingCommand` descriptor (whole-corpus scan).

Next discriminating query: what the UI side does with the engine's report.

## Round 3 — UI reflection and ATransport layout (corpus)

Resolved:

- `TransportEngineStateChanged` (descriptor `0x106f55d00`) is sent by
  `0x101a3d6d8` from `0x101a3d638`/`0x101a3d7d0` (OBeatTimeForwarderEvent
  matches) and handled by `0x1026baa70` (registered in `0x1026ba140` with
  members UnitId, Playing, BeatTime, CountInPosition, IsSongPositionJump,
  IsAtSongLoopJump, Stamp), which calls `0x10276c538`.
- `0x10276c538` writes the runtime bool at ATransport `+0x788` and `mpStart`
  to the reported Playing value, clearing byte `+0x8b0` around the `mpStart`
  write. Start's engine section requires `+0x8b0 == 1`.
- ATransport members from `0x10275dccc` (`atransport-members.json`); the
  pointer used by code is descriptor offset + 8 (constructor `0x102760d88`
  writes the wrapper vtable at the descriptor offset and registers callbacks on
  the +8 pointer). Used: `+0x240` mpCurrentTime, `+0x5a8` mpStart, `+0x5c0`
  mpGlobalRecord, `+0x5d8` mpSessionRecord, `+0x698` mpStop, `+0xb0`
  mpIsTempoFollowerInControl, `+0x228` mpLoopOn, `+0x60` mpLoopIsSongStart,
  `+0x1c8` mpLoopStart. `+0x788`, `+0x8b0`, `+0x8c8`, `+0x968` are unreflected.
- Constructor registrations: `mpStart` change callback = OnStart wrapper
  (`0x102770a58`, Mach-O symbol), name "Play"; `mpStop` callback = OnStop
  wrapper (`0x102770a64`), name "Stop"; `mpLoopOn` empty callback, name
  "Toggle loop".
- `ARemoteableBool` set slot `0x248` (`0x1015645e4`) calls the controller at
  `+0x68`; the default controller `0x10156a5f8` writes and notifies only when
  the value differs. `mpStart` keeps the default controller.

## Round 4 — loop and position setters (corpus)

Resolved:

- `ALoopOn` (vtable `0x106803d50`, RTTI `7ALoopOn`) overrides slot `0x248` with
  `0x10276e79c`, which only sends `OSetLoopOnCommand` (`0x101a4a3b4`) when an
  engine is reachable; handler `0x101a522c8` → `0x101a4a4d4` (domain-manager
  SetLoopOn match) → per-domain `0x101ab3594`.
- `ACurrentTime` (vtable `0x106803378`) overrides slot `0x248` with
  `0x10276d80c` → `0x10276d814`: if `+0x788` is set, `0x10276b47c`; otherwise a
  song-level setter `0x10270087c` with the value. Neither callee was traced.
- Start time `0x102769868`: `+0x50` (set from mpLoopStart by OnLoopIsSongStart
  `0x1027686f4` when mpLoopIsSongStart is on), else `+0x70`, else a song value
  `0x1026de350` (min of two song doubles; DBL_MAX → 0.0); then
  `TStartBeatTime` (`0x101a4c224`) and the playing-visible-session downbeat
  selector (`0x101a4c2dc`).

## Negative and open results

- The `vtables` index cannot resolve `0x101a4ac58`; constructor tracing did.
- Not traced: singleton slot `0x998` called first by Start (`0x10267619c`/
  `thunk_FUN_101849958`); Start's tail block when mpStart is true
  (`0x101557e04`, `0x101558118`, slot `0x738`, `0x1017906e8`); the queue
  send `0x101aaca84` and its ordering guarantee; `OScheduler` internals for
  Start/Stop position effects in Live (`0x101a54364` and below); who sets
  ATransport `+0x8c8` and `+0x70`; `0x10276b47c`, `0x10270087c`.
- Which external controls (Play button, Space bar, LOM, MIDI) reach
  `mpStart`, `0x102767a70`/`0x102767a7c` or the toggles `0x10276b2a0`,
  `0x10276b30c`, `0x10276b370` is not established.
- The callback globals tested by `0x101a4ac8c` (`0x106e2b628`, `0x106e2b638`)
  and the panic/all-notes-off callback globals (`0x106e2b6b0`–`0x106e2b6d0`)
  were not traced to their writers in Live.
