---
id: RESEARCH-TRANSPORT-TRANSITIONS-NATIVE
type: research
status: draft
updated: 2026-10-17
access: analysis
target: Ableton Live 12 Suite 12.4.3 arm64
---

# Transport transitions in native Live (S3)

**Question.** From a stopped document, what does a Start request followed by a
Stop request change in Live's transport state? How do a repeated Start, a Stop
while stopped and loop toggling behave?

**Answer (static, draft).** The indirect call at `0x101a4ac58` in the shared
helper `0x101a4abd8` is resolved. It is `OSendThreadMessage::Finish`
(`0x101ab7898`), which queues an `OSetPlayingCommand` thread message for the
engine. Start and Stop do not write a playing flag directly. They post requests,
and the engine then reports its state back to the interface. The derived
transition table is [below](#transition-table). Effective timing, the position
after Stop, and which external controls reach each entry point need runtime
evidence. They are collected in the [escalation record](#adr-0002-escalation-record).

This page continues the [native transport study](native-transport-study.md#default-profile-comparison-and-shared-helper)
(T1 cases), which stopped at this helper. Evidence:
[n3-transitions-v1](../../analysis/ableton-live-12.4.3/r2/n3-transitions-v1/manifest.json).
It holds two dossier results (`n3-0001`, `n3-0002`), exact corpus records for
every cited function, slice reads with RTTI names, the ATransport member table, the
symbol-match table, notes per round, and a script that reproduces the extracts.
Nothing was executed. No result on this page is an observed runtime behavior.

## Method

- **Target.** The Live arm64 slice (SHA-256 `3a99ceea…383cfad`, base `0x100000000`)
  and the completed whole-program corpus and indexes (418,417 functions). Material
  branches were checked against disassembly in dossiers n3-0001 and n3-0002.
- **Symbol donor.** The [Engine bundle](x86-only-bundles.md#consequence-for-analysis-a-named-copy-of-lives-engine-code)
  x86_64 corpus names the `OEngine` methods that Live leaves unnamed. The donor
  bundle is a ReWire device build of the same engine. Matches rest on shared
  message-descriptor strings, identical field offsets, call shape and address
  adjacency. The full table is in [symbol-matches.tsv](../../analysis/ableton-live-12.4.3/r2/n3-transitions-v1/symbol-matches.tsv).
  An engine name applied to a Live address is **inferred**, with the confidence
  stated there.
- **Not used.** Live's own x86_64 analysis (`helpers/Live_x86_64/summary.json`
  was absent during this packet), REA, and any runtime execution.
- **Budget.** Four rounds: dossier round n3-0001, then three rounds over the
  corpus, with dossier round n3-0002 confirming disassembly. The [notes](../../analysis/ableton-live-12.4.3/r2/n3-transitions-v1/notes.md)
  record what each round resolved and what it left open.

## Findings

### 1. The indirect call and its consumer

**Observed:**

- `0x101a4abd8` builds a stack object through `0x101ab7348`. The arguments are
  descriptor `0x106f55ea8`, from-thread `w1`, to-thread `0x10100` and method 0.
  The helper appends `x0` (8 bytes) and `w2`, `w3`, `w4` (1 byte each), calls
  `[[sp]+0x10]` with `blr x8` at `0x101a4ac58`, and then calls `0x101ab786c`.
- `0x101ab7348` stores `0x106756188` into the object's first word. The slice word
  before it is typeinfo `0x1067562d8`, whose name string is `18OSendThreadMessage`.
  Slot `+0x10` holds **`0x101ab7898`**; slots `+0` and `+8` hold `0x101ab786c` and
  `0x101ab787c` ([binary-reads.json](../../analysis/ableton-live-12.4.3/r2/n3-transitions-v1/binary-reads.json)).
  The symbol-named `vtables` index does not contain this vtable.
- `0x101ab7898` passes the message and both thread ids to `0x101aaca84`. It does
  so only when construction did not fall back to the static dummy `0x106f56460`.
- Initialiser `0x101a8effc` sets descriptor `0x106f55ea8` to `{-1, "OSetPlayingCommand"}`.
  Registration `0x101a50bd4` binds that name to handler `0x101a524b8` with members
  `Engine`, `Playing`, `ByUser` and `AllowCountIn` (string `0x105bb0a42`).
  `0x101a4abd8` is the only function in the corpus that uses the descriptor.
- The handler reads the pointer and three booleans and calls `0x101a4ac8c`.

**Inferred** (high confidence matches): `0x101a4abd8` is `OEngine::SendRequestForSetPlaying(TId, bool, bool, bool)`,
`0x101ab7898` is `OSendThreadMessage::Finish` and `0x101a524b8` is
`OEngineController::SOnSetPlayingCommand`. `0x10100` names the audio (engine)
thread and `0x100500` the main thread. In the donor, the engine-to-interface
message `RootUnit.NotifyPlaying` is sent from `0x10100` (or the current audio
thread) to `0x100500`. **Unknown:** how the queue send (`0x101aaca84`) orders,
drops or delivers messages. A message is silently discarded when the queue pool
has no slot (the dummy-buffer path); the conditions for that are unknown.

### 2. Engine-side handling of a Playing request

**Observed** in `0x101a4ac8c` and `0x101a4adec` (disassembly in n3-0002) and
`0x101a4af58`. The labels are the donor's names:

| Step | Condition | Effect |
| --- | --- | --- |
| Host override | Engine bytes `+0x8e0`/`+0x8e1` not both set, and the play (`0x106e2b638`) or stop (`0x106e2b628`) callback differs from its default lambda | The request goes to that callback; nothing below runs |
| Stop (`Playing=0`) | Otherwise | `SetPlaying(false, ByUser)` (`0x101a4adec`); `ByUser` is passed through in `x2` |
| Start (`Playing=1`) | `AllowCountIn` set, deferred-play object at `+0x9b0` present, and its slot 0 returns true | Return; playing is not set |
| Start | Otherwise | Slot `0x10` of the `+0x9b0` object if present; domain manager `SetPlaying(true)` (`0x101a4af58`); stop counter `0x106f55d24` := 0 |
| Domain manager `SetPlaying(v)` | Byte `+0x60` differs from `v` | Send `RootUnit.NotifyPlaying` (unit id, `v`) to `0x100500`; write `+0x60`; call `0x101a54364` for each domain |
| `SetPlaying(false, ByUser=1)` | — | If the last stamped stop was 3,501 ms or more ago (`cmp #0xdad`), counter := 0. Then counter += 1 and stamp. When counter = 3, call the callbacks at `0x106e2b6b0`/`6b8`/`6c0`, set counter := 0 and return. Otherwise call `0x106e2b6c8`, then `0x106e2b6d0` |
| `SetPlaying(false, ByUser=0)` | — | Counter := 0; then the same two callbacks |
| `SetPlaying(true, ·)` | — | Counter := 0 |

**Inferred** from the donor: the three callbacks on the third stop are the
"MIDI panic" set (`sMidiPanicCallbacks` first), and the two otherwise are the
"all notes off" set (`sAllNotesOffCallbacks` first). Which functions Live
installs there, and what they emit, is **unknown**.

**Observed:** the engine reports back through `TransportEngineStateChanged`
(descriptor `0x106f55d00`), sent by `0x101a3d6d8` from `0x101a3d638` and the
periodic `0x101a3d7d0`. The members are UnitId, Playing (the scheduler status byte
`+0x68`), BeatTime, CountInPosition, IsSongPositionJump, IsAtSongLoopJump and Stamp.
`0x101a3d638` sends when the scheduler's playing byte or beat time differs from
its last status. It sets IsSongPositionJump when the beat time changed.

### 3. Interface side: ATransport

**Observed:**

- ATransport member offsets come from reflection registration `0x10275dccc`
  (80 names, [atransport-members.json](../../analysis/ableton-live-12.4.3/r2/n3-transitions-v1/atransport-members.json)).
- Code uses the pointer at descriptor offset + 8. Constructor `0x102760d88` stores
  each wrapper's vtable at the descriptor offset and registers callbacks on the +8
  pointer.
- The relevant pointers are `+0x5a8` `mpStart`, `+0x698` `mpStop`, `+0x240`
  `mpCurrentTime`, `+0x228` `mpLoopOn`, `+0x60` `mpLoopIsSongStart`, `+0x1c8`
  `mpLoopStart`, `+0x5c0` `mpGlobalRecord`, `+0x5d8` `mpSessionRecord` and `+0xb0`
  `mpIsTempoFollowerInControl`.
- `+0x788` is an unreflected `ARemoteableBool`. `+0x8b0` is a byte initialised
  to 1, `+0x8c8` a pointer initialised to 0 and `+0x968` a double initialised to
  `DBL_MAX`.
- The constructor registers wrapper `0x102770a58` (Mach-O symbol
  `CallMemberFunc<&ATransport::OnStart>`) as the change callback of `mpStart` and
  names that control "Play". It registers `0x102770a64` (`OnStop`) on `mpStop`
  and names it "Stop". `mpLoopOn` gets an empty callback and the name "Toggle loop".
- `ARemoteableBool`'s set slot `0x248` (`0x1015645e4`) calls the controller at
  `+0x68`. `mpStart` keeps the default controller `0x10156a5f8`, which writes and
  notifies only when the value changes.

**Start body `0x10276a7b0`.** The OnStart wrapper and `0x102767a70`/`0x102767a7c`
call it with (1, 1); the toggles `0x10276b2a0`/`0x10276b370` call it with (0, 0).
Observed:

1. It always calls slot `0x998` of the object returned by `0x10267619c`. That
   effect is unknown.
2. It continues only if byte `+0x8b0` = 1, and only if the engine's byte `+0x960`
   (inferred `ExternSyncOn`, through `0x101a48488`) is clear.
3. If the first argument is set, it computes a start time with `0x102769868`:
   - ATransport `+0x50`, which OnLoopIsSongStart (`0x1027686f4`) sets to the
     `mpLoopStart` value while `mpLoopIsSongStart` is on;
   - else `+0x70`;
   - else a song value from `0x1026de350`, or 0.0 when that is `DBL_MAX`.

   The result is wrapped as a `TStartBeatTime` (`0x101a4c224`). Selector
   `0x101a4c2dc` uses the quantized downbeat only when a flag computed from the
   song's tracks is set and the time is not the loop-start value. Inferred from
   the donor name: the flag means a session clip is playing in the visible session.

   If the first argument is clear, it uses `+0x968` when that is set, and skips
   the jump otherwise.
4. It posts the jump with `0x101a4b1d0` (inferred `SendRequestForSetBeatTime`,
   message `OEngine.ScheduleBeatTimeJump`), then
   `SendRequestForSetPlaying(engine, 0x100500, Playing=1, ByUser=0, AllowCountIn=second argument)`.
5. If `mpStart` is now true, a further interface block runs (`0x101557e04` …
   `0x1017906e8`). Its effect is unknown.

**Stop body `0x102767b70`** (reached from the OnStop wrapper, the toggles and
`0x1027684bc`). Observed:

1. If extern sync is clear, it posts `SetPlaying(engine, 0x100500, Playing=0, ByUser=1, AllowCountIn=0)`.
2. If `+0x788` is false, and the engine pointer at `+0x8c8` is null or its byte
   `+0x9b8` is clear (inferred `IsCountInRunning`), it tail-calls
   `mpCurrentTime` slot `0x248` with `d0 = 0.0` (`br x1` at `0x102767c98`).
   ACurrentTime overrides that slot (`0x10276d80c` → `0x10276d814`). When stopped,
   the override forwards the value to a song-level setter `0x10270087c`, which was
   not traced.
3. If `+0x788` is true, it calls slot `0x998` when extern sync is clear. If
   `mpIsTempoFollowerInControl` and `mpGlobalRecord` are both true, it tail-calls
   `mpIsTempoFollowerInControl` slot `0x248` with `w1 = 0` (`br x2` at `0x102767c60`).

These are the two computed transfers that blocked the earlier selected-profile
export; both are now resolved to virtual slots on named members.

**Reflection `0x10276c538`.** Called only by `TransportEngineStateChanged`
handler `0x1026baa70`. Observed:

- Stores Stamp at `+0x970`.
- On Playing = 0 while `+0x788` was set and IsSongPositionJump is clear, sets
  `mpSessionRecord` to false, guarding `+0x8b1` around the write.
- On Playing = 1 while `+0x788` was clear, clears `+0x968` if set and calls two
  song functions (`0x1026925fc`, `0x102695718`).
- Stores BeatTime at `+0x950`, and CountInPosition (if negative) or BeatTime at
  `+0x958`.
- On a change of playing state or a position jump (unless `+0x900` is set):
  fires `mpSongPositionJumpBang` on a jump, updates `mpCurrentTime` and the count-in
  values through `0x10276a4f0`, and updates `mpFollow`.
- Finally writes `+0x788` := Playing, then `mpStart` := Playing with `+0x8b0`
  cleared. OnStart therefore runs its step 1 and tail but posts no requests.

**Inferred:** `+0x788` is the interface's copy of engine playing state, and
`mpStart` is the Play control's value. Both change only when the engine reports,
not when Start or Stop is requested.

### 4. Loop toggling

**Observed:**

- `ALoopOn` (RTTI `7ALoopOn`, vtable `0x106803d50`) overrides set slot `0x248`
  with `0x10276e79c`. When the owner's engine is reachable, that function posts
  `OSetLoopOnCommand` (`0x101a4a3b4`; members Engine, LoopOn). It does not write
  the local value.
- The handler `0x101a522c8` applies the same host-callback test as Playing. It
  then calls `0x101a4a4d4` (inferred `OEngineDomainManager::SetLoopOn`), which:
  - changes engine byte `+0x61` only when it differs;
  - calls `0x101ab3594` (inferred `OScheduler::SetLoop`) for each domain with the
    stored loop start and length;
  - calls `0x101a547f0` when a scheduler's loop byte changed.
- No code path above reads the loop flag when handling Start, Stop or Playing,
  and `0x101a4a4d4` does not read or write `+0x60`. Loop affects Start only
  through `mpLoopIsSongStart` (start time = loop start).

**Unknown:** how the interface `LoopOn` value is updated after the request, and
how a loop change moves the playback position while playing.

The x86_64 build corroborates these readings, including both Stop transfers (`0x1028a0584`,
`0x1028a05db`); in both builds, when `+0x900` = 1 the reflection writes `+0x788` through a separate
function and returns without writing `mpStart`
([Live x86_64 paths](x86-live-paths.md#transport-cross-check-with-arm64)).

## Transition table

Preconditions for rows T-01 to T-08:

- a loaded set with a reachable engine;
- extern sync off (engine `+0x960` clear);
- default host play, stop and loop callbacks;
- no deferred-play (count-in) object accepting the start;
- ATransport `+0x8b0` = 1 (an interface-originated request).

"Static-derived" means derived from code paths without execution; it is not an
observation. "Request" means a posted thread message. The engine and interface
columns describe effects after the engine handles the message and after the
interface handles `TransportEngineStateChanged`.

| ID | From state | Action and entry | Requests posted (order of posting) | Engine state | Interface state | Label |
| --- | --- | --- | --- | --- | --- | --- |
| T-01 | Stopped | Start via `mpStart` false→true (OnStart, args 1,1) | Jump to start time t*, then Playing=1, ByUser=0, AllowCountIn=1 | Playing byte 0→1; `RootUnit.NotifyPlaying`(1); stop counter 0 | After report: `+0x788`=1, `mpStart`=1 (no new OnStart requests); pending `+0x968` cleared; `mpCurrentTime`←reported BeatTime | Static-derived. t* rule static-derived; the effective start position and latency are unknown |
| T-02 | Playing (`+0x788`=1) | Stop via `mpStop` (OnStop) | Playing=0, ByUser=1, AllowCountIn=0 | Playing byte 1→0; NotifyPlaying(0); stop counter +1; all-notes-off callbacks (panic set on the third stop within 3.5 s) | Immediately: tempo follower control off if it and Arrangement Record (`mpGlobalRecord`) are both on. After report: `+0x788`=0, `mpStart`=0, `mpSessionRecord`=off unless the report flags a position jump | Static-derived. Callback effects and the position after stop are unknown |
| T-03 | Stopped (`+0x788`=0) | Stop again | Playing=0, ByUser=1, AllowCountIn=0 | Playing byte unchanged; no NotifyPlaying; stop counter +1; all-notes-off or panic callbacks as in T-02 | `mpCurrentTime` set to 0.0, unless the engine at `+0x8c8` reports a running count-in; forwarded to song setter `0x10270087c` | Static-derived up to the 0.0 write; the displayed or stored position after it is unknown |
| T-04a | Playing | Start via `mpStart` when it is already true | None (default controller: value unchanged, no notification) | Unchanged | Unchanged | Static-derived; that the Play control takes this path is unknown |
| T-04b | Playing | Start via direct callers `0x102767a70`/`0x102767a7c` (args 1,1) | Jump to t*, then Playing=1 | Playing byte unchanged (no NotifyPlaying); stop counter 0; deferred-play slot `0x10` | Any position jump is reflected by a later report | Static-derived for requests; the effect of a jump while playing is unknown |
| T-05 | Stopped | Start then Stop before the engine reports | Jump, Playing=1, then Playing=0 (ByUser=1) | Inferred: 0→1→0 if the queue is FIFO | Stop sees `+0x788`=0, so it also takes the T-03 position write (0.0) | Unknown: queue ordering and report timing |
| T-06 | Any | Third user Stop, each within 3,500 ms of the previous one | As T-02/T-03 | Panic callbacks instead of all-notes-off; counter reset to 0 | As T-02/T-03 | Static-derived; callback effects unknown |
| T-07 | Stopped or playing | Loop toggle through `ALoopOn` set | `OSetLoopOnCommand`(v) only | Loop byte := v if different; scheduler SetLoop per domain; playing byte untouched | Local LoopOn not written by the set override; how it is updated is unknown | Static-derived for the request and engine flag; position effect unknown |
| T-08 | Stopped, loop-is-song-start on | Start (args 1,1) | Jump to `mpLoopStart` value (unquantized), then Playing=1 | As T-01 | As T-01 | Static-derived |
| T-09 | Any, extern sync on | Start or Stop | None | Unchanged | Stop's T-03 branch still sets `mpCurrentTime` to 0.0; Stop's slot `0x998` call is skipped | Static-derived; outside the first contract |
| T-10 | Any | Host callbacks installed | Requests posted | Diverted to the host callbacks | — | Static-derived; outside the first contract (ReWire/host) |
| T-11 | Stopped | Start with a deferred-play object that accepts | As T-01 | Playing not set by this request | — | Static-derived; count-in is outside the first contract |
| T-12 | Pending request | Close document | — | — | — | Unknown (not traced) |
| T-13 | After T-01/T-02 | Save | — | — | `+0x788` is not in the reflected member table (inferred: not persisted); `CurrentTime` and `LoopOn` are reflected members | Unknown for the saved values |

Undo participation was not examined: unknown. T1-A–F map to T-01/T-02, T-04/T-03,
T-05, T-07/T-08, T-13 and T-12.

## ADR 0002 escalation record

**Remaining runtime question.** For the default preconditions above, what does
the user observe after Play, Stop, Stop, and after a Play then Stop within one
audio buffer? Specifically, the song position display and the saved
`CurrentTime`, and whether the Play control and `is_playing` lag the request.

**Existing evidence.** This page: the request and reflection paths, T-01 to T-08.

**Why runtime.** The position after Stop depends on scheduler internals
(`0x101a54364` and below) and the untraced song setter `0x10270087c`. Report
timing depends on the audio thread. Static tracing would need many more
functions for a value one capture shows directly.

**Minimal scenario** (macOS host, Live 12.4.3):

- default set, extern sync, Link and count-in off, Arrangement Record off;
- move the insert marker to bar 5 (beat 16);
- press Play, wait 2 s, press Stop, wait 1 s, press Stop;
- separately, Play then Stop within 50 ms;
- separately, enable Loop and "loop is song start" (if exposed in the
  interface), then press Play.

**Discriminating observations.**

- Position display and LOM `current_song_time` after each step. T-03 predicts
  0.0 after the second Stop.
- LOM `is_playing` sampled every 10 ms around each press, to measure the
  reflection lag.
- Saved `CurrentTime` after the final step.
- Start position with loop-is-song-start: T-08 predicts the loop start.

**Stop condition.** One capture per scenario. If the second Stop does not
return to 0.0, record the observed value and reopen T-03 statically at
`0x10270087c`; do not iterate further at runtime.

## Unknowns and limits

- Static evidence only. A call edge is not proof of execution.
- Engine names on Live addresses are matches, not symbols. Medium-confidence
  matches (`ExternSyncOn`, `IsCountInRunning`) rest on offsets and adjacency.
- Which external controls (transport Play button, Space bar, LOM
  `start_playing`/`stop_playing`, MIDI-mapped Play) set `mpStart`, call
  `0x102767a70`/`0x102767a7c` or use the toggles is not established.
- Untraced:
  - the slot `0x998` call;
  - Start's tail block;
  - `0x101aaca84` queue semantics;
  - `0x101a54364` and the Live scheduler;
  - `0x10270087c`, `0x10276b47c`;
  - writers of ATransport `+0x70` and `+0x8c8`;
  - writers of the host-callback and panic/all-notes-off globals.
- The `mpStart` false transition caused by a report calls OnStart with
  `+0x8b0` cleared. What OnStart does when a control writes `mpStart` = false
  directly was not examined.
- Cost note: each `str:` dossier query took about 4–6 minutes on Live. The
  corpus `strings.jsonl` index answers the same question offline.
