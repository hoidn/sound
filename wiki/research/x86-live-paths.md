---
id: RESEARCH-X86-LIVE-PATHS
type: research
status: draft
updated: 2026-10-17
access: analysis
target: Ableton Live 12 Suite 12.4.3 x86_64
---

# Live x86_64: ReWire install, MultiF0 selection and a transport cross-check (packet N8)

**Question.** [Q-013](../questions.md#q-013-x86_64-only-rewire-and-multif0-paths)
asks when Live installs ReWire and which alias it creates, whether 12.4.3 still
offers ReWire, which MultiF0 copy the x86_64 build uses by default, whether
Convert Drums uses MultiF0, what MultiF0's result fields mean, and why the Engine
bundle has an empty arm64 slice. A second question: does the x86_64 build agree
with the arm64 readings in [transport transitions](transport-transitions-native.md),
especially the two computed transfers in Stop?

**Answer (static, draft).**

- The install code is complete but **switched off**. It runs only from one
  virtual method of `LReWireHost`, called while a song agent is constructed. That
  method first tests a predicate that is compiled as `return 0`. The same holds
  for opening Live as a ReWire mixer. The Engine bundle's own device and host
  predicates also return 0, so its `_RWDEFOpenDevice` always refuses.
  Inferred: 12.4.3 offers no working ReWire mode on either architecture.
- If the code were enabled, it would copy `ReWire.bundle` into
  `Application Support/Propellerhead Software/ReWire/` in the local and the user
  domain, then create the alias **`Ableton Live Engine_64`** there with `MakeAlias`.
  It also deletes an item named `Ableton Live Engine` from `Application Support`.
- x86_64 Live chooses MultiF0 exactly as arm64 Live does: it uses the built-in copy
  unless the same developer option, with a byte-identical key, is set.
- Convert Drums does not use MultiF0. Harmony (type 0) and Melody (type 1) build
  `TMultiF0Task`; Drums (type 2) builds `TDtmTask`.
- Live's reading of a MultiF0 record gives the fields a meaning: start, end,
  frequency in Hz (converted to a MIDI pitch), a frequency trajectory and an
  amplitude-like value that sets velocity.
- The x86_64 transport code matches the arm64 readings, including both Stop
  transfers. One reflection branch is missing from the arm64 page.

Evidence: [n8-x86-paths-v1](../../analysis/ableton-live-12.4.3/r2/n8-x86-paths-v1/manifest.json).
It holds two dossier results (`results/n8-0001`, `results/n8-0002`, eight queries
each), corpus pseudocode for 74 cited functions, `binary-reads.txt`
(vtables, RTTI, keys and constants), `objdump.txt` (raw-byte disassembly), the
anchor table, scripts and [notes](../../analysis/ableton-live-12.4.3/r2/n8-x86-paths-v1/notes.md)
with the round log. Nothing was executed. A call edge is not proof that a path
runs at runtime.

## Method

- **Target.** Live x86_64 slice, SHA-256 `1bae9a97…be999b0`, image base
  `0x100000000`. The whole program is decompiled (414,791 functions, 0 pending)
  and indexed (strings index SHA-256 `26336158…`). The read-only Ghidra project
  was opened twice through route step 4 of [query route](r2-query-route.md).
  Addresses are image VAs.
- **Comparison.** Live arm64 (`3a99ceea…383cfad`), the Engine x86_64 slice
  (`028df12e…5843de`, named symbols) and the MultiF0 dylib corpus.
- **Budget.** Four rounds: corpus, dossier n8-0001, corpus, dossier n8-0002.
  Every material branch below was checked in dossier disassembly and against
  GNU objdump output of the raw bytes.

## ReWire

### The install chain

**Observed** (`0x1024b0300`, `0x1024b0650`, `0x1024b0d30`; dossiers n8-0001 and
n8-0002; `objdump.txt`):

1. `0x1024b0300` calls `0x1024b0650` with domain `0xffff8003`, then with
   `0xffff8005`, and continues only when both succeed. It then calls `0x1024b0d30`
   with the same two domains. The log labels these domains `kLocalDomain` and
   `kUserDomain`.
2. `0x1024b0650` reads the version of the shipped `Resources/ReWire-Mach-O/ReWire.bundle`
   (`CFBundleGetVersionNumber`). It then looks for
   `<domain Application Support>/Propellerhead Software/ReWire/ReWire.bundle`
   (`FSFindFolder(domain,'asup')`). If that copy is at least as new, it logs
   `… is already installed and up to date, no action required` and returns success.
   Otherwise it runs `/bin/rm -rf <…/ReWire/ReWire.bundle>`, then
   `/usr/bin/ditto <Resources/ReWire-Mach-O> <…/Propellerhead Software/ReWire>`.
3. `0x1024b0d30` resolves `Ableton Live Engine.bundle` in Live's resources. It runs
   `/bin/rm -f "<Application Support>/Ableton Live Engine"`. The path is built
   from the bare Application Support folder (`rcx` = `rbp-0x14f0` at `0x1024b0e5e`),
   not from the ReWire folder. It then checks
   `<…/Propellerhead Software/ReWire>/Ableton Live Engine_64`. If that alias
   resolves to the shipped Engine bundle, it logs "already installed" and returns
   success. Otherwise it sets the "installed" flag and runs
   `Resources/MakeAlias <Engine bundle path> <…/ReWire> "Ableton Live Engine_64"`.
4. Every tool runs through `0x101180aa0`. That function first tries fork and exec.
   If the status is non-zero and interaction is allowed (`0x101198610`), it retries
   with `AuthorizationExecuteWithPrivileges`. The result is 0 for success, 1 for
   failure and 2 for `errAuthorizationCanceled` (`-0xea66`). Status 1 shows
   `sErrorAuthorizationFailed` and status 2 shows `sErrorAuthorizationCancelled`
   (keys bound to `LReWireHost` in `0x1024b96f0`).
5. If any step fails, `0x1024b0300` shows `sErrorCantInstallReWireDll` (library
   step) or `sErrorCantInstallReWireEngine` (alias step), unless an authorization
   error was already shown. When both alias steps succeed and one of them
   installed something, it shows `sDialogInstalledReWireEngine`.

The localized texts of these keys were not decoded.

### When it would run, and why it does not

**Observed:**

- The only call to `0x1024b0300` is at `0x1024b50b0` in `0x1024b5060`. The dossier
  shows no other code or data reference except `__LINKEDIT` symbol data.
- `0x1024b5060` is slot `0x190` of the `LReWireHost` vtable (`0x106cea210`, typeinfo
  `11LReWireHost` → `11AReWireHost` → `9ACompound`). Its only stored pointer is that
  slot (`0x106cea3a0`).
- The song-agent constructor `0x1027c81e0` logs `LSongAgent: Begin Constructing`.
  It creates the host (`0x1024b6190`), stores it at `this+0xe8` and calls
  `[rcx+0x190]` on it at `0x1027c85c8`. `r15` = `this+0xe8` is not reassigned
  between `0x1027c8437` and the call.
- `0x1024b5060` begins with these branches (dossier disassembly):
  - `call 0x101ab6780; test al,al; je` skips the install;
  - then a developer-option test (key at `0x105de826c`) and `0x101198610`;
  - then `call 0x101ab68f0; test al,al; je` skips `ReWire: ReWireHost Open`, the
    `SRWMOpen` path and the ReWire SDK loader `0x105421ae0` (search names
    `ReWire Debugging.bundle`, `ReWire Testing.bundle`, `ReWire.bundle`).
- `0x101ab6780` and `0x101ab68f0` are both `push rbp; mov rbp,rsp; xor eax,eax;
  pop rbp; ret`.
- In the named Engine, `OEngineReWireData::SIsReWireDeviceEnabled` (`0xe73f0`) and
  `SIsReWireHostEnabled` (`0xe7560`) have the same bytes. The 0x180 bytes starting
  at each device predicate agree in 361 places, and the differences are rel32
  displacements. The host predicate is `+0x170` from the device predicate in both
  binaries.
- `_RWDEFOpenDevice` (`0x3ae20`) calls `0xe73f0`, loads 5 into the return
  register and returns it when the result is 0.
- The other path to the ReWire library, panel-side `0x1024b5e50` → `0x101b2e930`
  → `0x1054224a0` (`RWPOpenImp` and the other `RWP*Imp` names), has no caller and
  no stored pointer.
- arm64 `LReWireHost` slots `0x190`–`0x1a8` are `ret`, `return 1`, `ret`,
  `return 0` (`0x10239f0c4`…`0x10239f0d4`). The x86 slots hold the install/open
  method, two methods that test the open flag `+0x30`, and the device count (`+0x40`).

**Inferred.**

- `0x101ab6780` is Live's copy of `SIsReWireDeviceEnabled` and `0x101ab68f0` is
  its copy of `SIsReWireHostEnabled`. Confidence is high: identical bytes,
  identical spacing and the same neighbour (`IsReWireDeviceNameAnAbletonOne`
  at `+0x10`).
- If the predicates were enabled, the install would run each time a song agent is
  constructed, before the host is opened.
- As built, 12.4.3 x86_64 Live does none of the following:
  - install `ReWire.bundle` or the Engine alias;
  - open a ReWire host, so devices such as Reason are not hosted;
  - load the ReWire library.
- A mixer that finds an Engine alias left by an older Live install loads that
  older bundle, not this one. A mixer that loads this Engine bundle gets error 5
  from `_RWDEFOpenDevice`.
- arm64 Live's matching `LReWireHost` methods are empty, so nothing there opens
  or installs ReWire either.
- Therefore 12.4.3 offers no working ReWire mode on either architecture. This
  replaces the earlier inference that ReWire works under Rosetta.

**Unknown.**

- What the user sees: whether menus, preferences or I/O choosers still show
  ReWire entries. Strings such as `sDialogRunningAsReWireDevice` and
  `AudioIn/ReWire.` remain in the binary.
- Release notes and the manual were not captured.
- The text behind the error keys.

### The Engine bundle's arm64 slice

**Unknown, unchanged.** No new evidence explains why the slice exists. The new
facts only show that the x86_64 Engine refuses device mode too
(`SIsReWireDeviceEnabled` = 0). Inferred (low confidence): the bundle target is
still built for both architectures with no functioning code. Nothing in Live
x86_64 refers to the Engine except the alias step above: the only uses of the
`Ableton Live Engine*` strings are in `0x1024b0d30`. Inferred: Live never loads
the Engine into its own process.

## MultiF0

### Selection in x86_64 Live

**Observed** (`0x1031d6b30`, dossier n8-0001):

- `0x101188890` looks up a 32-byte key at `0x105e2c7b8`. `test dl,1; jz 0x1031d6ba1`
  leads to the built-in implementation (vtable `0x106e02768`, RTTI
  `TBuiltinMultiF0InterfaceImpl`) and the log line
  `Audio2Midi: Use builtin MultiF0 lib`.
- Only when the option is found does it call the path resolver `0x1031d6330`.
  The resolver uses a second option or defaults to `Misc/MultiF0/Mac/libmultif0_64.dylib`,
  and logs `MultiF0: No MultiF0 library found at …` when the file is missing. The
  loader `0x1031d67b0` then logs `Audio2Midi: Use dynamic loaded MultiF0 lib`,
  resolves nine `mf0p_*` symbols and throws unless `mf0p_GetApiRevision` returns 10.
- The 32-byte key is byte-identical to arm64's key at `0x1058c29f8`. The option
  table is consulted only when flag `0x1073bb210` is 1. Only `0x101187200`
  writes that flag; that function was not traced.

**Inferred.** The x86_64 default is the same as arm64's: built-in unless the
developer option is set. This closes the open item on
[helper launch](helper-launch-live-side.md#multif0-q-013-arm64-only). Whether the
libstdc++-linked dylib still loads on current macOS stays **unknown**.

**Two copies.** Observed: the built-in `GetApiRevision` (`0x1054eac40`) returns 10.
The built-in default parameters (`0x1054eac80`) are ints 0, 1; floats 40, 3140,
6, 0.093, 15, 23, 1.3, 19, 20, 0.001, 0.1, 0.01, 3; and int 8. These match the
dylib's `mf0p_GetDefaultParameters` values. Whether the two copies produce
identical results is **unknown**.

### Convert Drums

**Observed:**

- The `AudioToMidiType` enum (`0x103ca34b0`) has `harmony_to_midi` = 0,
  `melody_to_midi` = 1 and `drums_to_midi` = 2.
- The callbacks `OnConvertHarmonyToNewMidiTrack`, `…Melody…` and `…Drums…` of
  `LArrangerControlManager`, `AAudioClipTimelineEditor` and `LSlotManager` load
  `esi` = 0, 1 and 2 respectively. Each one tail-jumps to a converter that reaches
  `0x103171b40`.
- `0x103171b40` calls the task factory `0x1031712f0`.
- In the factory (dossier n8-0001), outside the mock run mode, `cmp r15d,1; ja`
  creates `TDtmTask` (`0x1031a5c70`) for type 2 or higher. Types 0 and 1 create
  `TMultiF0Task` (`0x1031d7d40`).
- The task's log label comes from `H2M`/`M2M`/`D2M` (`0x106e00090`).
- `TAudioToMidiTask` has exactly three subclasses: `TDtmTask`, `TMultiF0Task` and
  `TMockAudioToMidiTask`.
- `TMultiF0Task`'s vtable slot `0x48` (`0x1031d7d70`) returns a string only for
  types 0 and 1.

**Inferred.**

- Convert Drums uses a separate analysis, `TDtmAnalysis` ("DTM"), not MultiF0.
- The algorithm type passes through the variant visitor in `0x103171b40` unchanged.
  That was not traced instruction by instruction.
- arm64 contains the same labels and the `TDtmTask` symbol text. Inferred: the
  same split applies there.

### Meaning of the result fields

**Observed** in `0x1031d7420`, which converts one 32-byte record into Live's
note structure (dossier n8-0002 and `objdump.txt`). Here *f* is the float at
`+8`, *p* = 12·log2(*f*/440) + 69 (`0x103173c30`), and *a* is the float at `+0x1c`.

| Offset | Use in Live |
| --- | --- |
| `+0x00`, `+0x04` (float) | Copied to the note's first two doubles. The drum analysis's result getter `0x1031abcd0` (reached from `0x1031ac1a0`, a `TDtmAnalysis` vtable slot) fills the same two slots with a start and start + length |
| `+0x08` (float) | Kept as a double. The note's integer pitch is *p* rounded half away from zero (`roundsd` truncate of *p* + copysign(0.49999999999999994, *p*)) |
| `+0x10` (pointer), `+0x18` (int count) | Array of *count* 8-byte (float *x*, float *y*) points. Each becomes the pair (*x*, *y* − *f*) |
| `+0x1c` (float) | Velocity (float) = 1 + 126·*a*·(0.5 + *p*/254), computed with two `fma` calls |

For Melody (default-parameter int[1] = 0), the analysis object's `+0x30` is set,
and that clears note byte `+0x20` on every note. For Harmony, int[1] = 1
(`0x1031d7e10`).

**Inferred:**

- `+0` and `+4` are the note's start and end times, not a start and a duration.
- `+8` is the fundamental frequency in Hz.
- The points are a pitch trajectory, stored as deviation from *f*.
- `+0x1c` is a normalized amplitude.
- Default-parameter int[1] is a polyphony switch.

**Unknown:**

- the time unit of `+0`/`+4` (seconds is likely, not shown);
- how the float velocity is rounded or clamped later;
- the meaning of note byte `+0x20`;
- the meaning of the other parameters.

## Transport cross-check with arm64

The function-by-function table is in the
[notes](../../analysis/ableton-live-12.4.3/r2/n8-x86-paths-v1/notes.md#transport-cross-check-table).
The x86_64 build has Mach-O symbols for the two member callbacks:
`CallMemberFunc<&ATransport::OnStart>` (`0x1028a9aa0`, calls `0x1028a3500(this,1,1)`)
and `…OnStop` (`0x1028a9ac0`, calls `0x1028a0460`).

**Observed, agreeing with arm64:**

- **Stop body** `0x1028a0460`:
  - if extern sync is clear, it posts `SetPlaying(engine, 0x100500, 0, 1, 0)`
    (`0x101a6f1f0`);
  - if `+0x788` is false and either `+0x8c8` is null or `0x101a6f1b0` is false,
    it executes `jmp rax` at **`0x1028a0584`**. The target is `[[this+0x240]]+0x248`
    with `xmm0` = 0.0: `mpCurrentTime` slot `0x248` with 0.0;
  - if `+0x788` is true, it calls slot `0x998` when extern sync is clear. If `+0xb0`
    and `+0x5c0` are both true, it executes `jmp rax` at **`0x1028a05db`** to
    `[[this+0xb0]]+0x248` with `esi` = 0: `mpIsTempoFollowerInControl` set false.

  These are the same members, offsets and slots as arm64 `br x1` `0x102767c98`
  and `br x2` `0x102767c60`.
- **Start body** `0x1028a3500`:
  - it always calls slot `0x998`;
  - it continues only if `+0x8b0` = 1 and extern sync is clear;
  - with the first argument set, it posts a jump to the computed start time.
    With it clear, it posts a jump to `+0x968` unless that is `DBL_MAX`;
  - it then posts `SetPlaying(engine, 0x100500, 1, 0, AllowCountIn = second argument)`;
  - the tail block runs when `mpStart` (`+0x5a8`) is true.

  Direct callers `0x1028a0300`/`0x1028a0320` pass (1,1). Toggles `0x1028a4080`/`0x1028a4160`
  pass (0,0) after the same `+0x8c8`, `+0xf0` and `+0x788` tests.
- **Message path.** `0x101a6f1f0` builds a message from thread `0x100500` to thread
  `0x10100` and calls slot `+0x10` of the vtable at `0x106c98f18` (RTTI
  `18OSendThreadMessage`). That slot, `0x101ae06b0`, queues the message unless the
  buffer is the static dummy `0x1073e8050`.
- **Engine side.** The handler for `OSetPlayingCommand` is `0x101a76fc0` → `0x101a6f290`
  (members `Engine`, `Playing`, `ByUser`, `AllowCountIn`). It applies the same
  host-callback test and count-in test. `SetPlaying(false)` (`0x101a6f3c0`)
  resets the stop counter after 3,501 ms (`cmp $0xdad` at `0x101a6f43a`), runs the
  three panic callbacks on the third stop (`cmpl $3` at `0x101a6f45d`) and otherwise
  runs the two all-notes-off callbacks.
- **Reflection** `0x1028a54b0` (from `0x1027e75a0`) stores Stamp at `+0x970`,
  clears `mpSessionRecord` on a reported stop without a position jump, clears `+0x968`
  on a reported start, and stores BeatTime and
  CountInPosition at `+0x950`/`+0x958`. It finally writes `+0x788` and then
  `mpStart` with `+0x8b0` cleared.

**Observed, missing from the arm64 page (both builds).** When byte `+0x900` = 1,
the reflection writes `+0x788` through a separate function (x86 `0x101554650`,
arm64 `0x1015646f4`) and returns without writing `mpStart`.

**Differences.** These are compilation differences, not behavior differences:

- the extern-sync helper takes the engine pointer in x86 (`0x101a6c470`);
- x86 reaches the Stop body through a wrapper `0x1028a0450` with 17 call edges,
  while arm64 has 23 direct call edges to the body;
- the global callback slots are spaced differently.

**Conclusion.** The x86_64 build corroborates T-01 to T-11 of the arm64
transition table, including both Stop computed transfers. Agreement between two
compiles of the same source is still static evidence. It does not replace the
[escalation record](transport-transitions-native.md#adr-0002-escalation-record).

## Probe records (runtime only)

All need the macOS reference host. Live x86_64 runs under Rosetta ("Open using
Rosetta"). Batch these with the [Phase 4 probe batch](phase4-probe-batch.md)
under [ADR 0002](../decisions/adr-0002-static-first-analysis.md). None is a gate.

| ID | Question | Minimal input and capture | Discriminating observation | Stop |
| --- | --- | --- | --- | --- |
| PRB-N8-01 | Does Live x86_64 install ReWire or the Engine alias? | Clean user account; start Live under Rosetta, create a new Set, quit; list `/Library/…/Propellerhead Software/ReWire` and `~/Library/…/Propellerhead Software/ReWire`; search `Log.txt` | Static prediction: no new files, no `InstallPropellerheadDlls` or `ReWire: ReWireHost Open` lines, no authorization prompt | One capture |
| PRB-N8-02 | Is ReWire visible to users? | Same session: Preferences, track input/output choosers, Help menu | Any ReWire entry. Static prediction: no hosted devices | One capture |
| PRB-N8-03 | MultiF0 default under Rosetta | Convert Harmony on a short audio clip, with logging | `Audio2Midi: Use builtin MultiF0 lib`; no `dynamic loaded` line | One capture |
| PRB-N8-04 | Convert Drums engine | Convert Drums on a drum loop on both architectures | No `Audio2Midi:` MultiF0 line; task label `D2M` if logged | One capture each |
| PRB-N8-05 | Result-field meaning | Convert Melody on a 1 s, 440 Hz sine starting at 1 s (fixture at known level), then the same sine an octave up | Note pitch 69 (then 81); note start and end match the tone; velocity rises with level and with pitch | Two clips |

## Unknowns and limits

- Static evidence only. No mixer, Rosetta or Live process was observed.
- Not traced: `0x101187200` (when developer options are active); the variant
  visitor in `0x103171b40`; `TDtmAnalysis`; how notes are converted to clip beats.
- The raw-read scripts assume VA = file offset + base. That does not hold for
  `__LINKEDIT`, but no cited read lies there.
- Name matches between the Engine and Live (`SIsReWire*Enabled`) are inferred
  from bytes and layout, not from symbols in Live.
