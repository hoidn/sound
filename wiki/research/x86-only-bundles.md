---
id: RESEARCH-X86-ONLY-BUNDLES
type: research
status: draft
updated: 2026-10-17
access: analysis
target: Ableton Live 12 Suite 12.4.3
---

# x86_64-only bundles: Live Engine, ReWire and MultiF0

**Question.** Three native components in the 12.4.3 bundle have no usable arm64
code: `Resources/Ableton Live Engine.bundle`, `Resources/ReWire-Mach-O/ReWire.bundle`
and `App-Resources/Misc/MultiF0/Mac/libmultif0_64.dylib`. What are they, who loads
them and when, and what follows for a native arm64 Live?

**Answer (static, draft).**

- The Live Engine bundle is Live's audio engine built as a **ReWire device**. A
  ReWire mixer application can load it into its own process while Live's
  interface runs as the ReWire panel application.
- `ReWire.bundle` is Propellerhead's ReWire system library 1.8.7.
- MultiF0 is an IRCAM polyphonic pitch and note estimator built on SuperVP. It is
  the dynamically loaded alternative to a MultiF0 copy built into Live for Convert
  Harmony/Melody to New MIDI Track.
- Native arm64 Live contains none of the strings that locate, install or open the
  Engine or ReWire bundles. Superseded 2026-10-17: the earlier inference that ReWire
  works when Live runs as x86_64 is wrong. `SIsReWireDeviceEnabled` and
  `SIsReWireHostEnabled` return 0 in the Engine and in Live x86_64, so `_RWDEFOpenDevice`
  always returns 5 and the install chain is unreachable; see [Live x86_64 paths](x86-live-paths.md).
- Native arm64 Live keeps the MultiF0 loader code but cannot load the x86_64-only
  dylib. Inferred: it uses the built-in copy.

Evidence: [h3-x86-bundles-v1](../../analysis/ableton-live-12.4.3/r2/h3-x86-bundles-v1/manifest.json).
It holds the scripts, Mach-O tables, string tables, byte scans of `Contents/MacOS/Live`,
extracted pseudocode and two read-only dossiers. Rerunning `run.sh` gave
byte-identical files. Nothing was executed. Pseudocode is Ghidra 12.1.4 output.
Addresses are image virtual addresses unless they are called file offsets.

## Identities

All observed. The source is the [Mach-O tables](../../analysis/ableton-live-12.4.3/r2/h3-x86-bundles-v1/macho/)
written by `macho_inspect.py`. All three components are signed with team ID `MWR434WD94`,
the same team ID as Live.

| Item | Live Engine bundle | ReWire.bundle | libmultif0_64.dylib |
| --- | --- | --- | --- |
| Info.plist | `com.ableton.live-engine`, `BNDL`, executable `Ableton Live Engine`, version `12.4.3 (2026-07-07_e3d8be4d07)` (identical to Live), SDK macosx15.5; no principal class, `CFBundleSupportedPlatforms` or `LSMinimumSystemVersion` | `se.propellerheads.rewire.library`, `BNDL`, signature `ReWi`, version `1.8.7 build 145`, platforms `MacOSX`, SDK macosx10.13, ©1999–2018 Propellerhead; no principal class | None (bare dylib) |
| File SHA-256 | `827e28bb…f50d6d9` (42,354,928 B) | `17b01f9e…f7883e2e` (1,004,656 B) | `b7d1f42e…53c0283f` (4,758,224 B) |
| Slices | x86_64 `028df12e…5843de` (42.3 MB) and arm64 `8c92c768…e37e784` (35,056 B) | i386 `6c8c042f…17dbd1c` and x86_64 `e6417803…f3dbd12` | x86_64 only |
| Type and minimum OS | `MH_BUNDLE`, `LC_BUILD_VERSION` macOS 11.0 on both slices | `MH_BUNDLE`, `LC_VERSION_MIN_MACOSX` 10.7 | `MH_DYLIB`, install name `/Volumes/jas-dev/ircam-a2n/master_multif0/build_64/lib/Release/libmultif0_64.dylib`, current version 0.0.16; no minimum-OS load command |
| Signature | Identifier `com.ableton.live-engine`, hardened runtime (flags `0x10000`), no entitlements | Identifier `se.propellerheads.rewire.library`, flags `0x0` | Identifier `libmultif0_64`, flags `0x0` |
| Entry points | No `LC_MAIN`. 51,073 export-trie entries, which equals `nextdefsym`, including `_RWDEF*`, `_RWM*`, `_RWP*` and `_InitNow` | 68 exports per slice: `RWM*Imp`, `RWM2*Imp`, `RWP*Imp`, `RWD*Imp`, `TopHat*Imp`, `RWIsReWireMixerAppRunningImp` | 12 exports: `mf0p_*` |
| Linked libraries | Foundation, AppKit (x86_64 only), CoreFoundation, Security, Carbon, Cocoa, CoreServices, CoreText, Accelerate, AudioToolbox, AVFoundation, CoreAudioKit, AudioUnit, libc++, libobjc, libSystem; `@loader_path/` rpath | Carbon, IOKit, ApplicationServices, CoreFoundation, CoreServices, libc++, libSystem; imports include `shm_open`, `mmap`, `bootstrap_register`/`bootstrap_look_up`, `CFBundleLoadExecutable`, `FSFindFolder`, `FSNewAlias` | Accelerate/vecLib/LAPACK/BLAS, Carbon, CoreServices, CoreFoundation, **libstdc++.6** and **libgcc_s.1**, libSystem |

Both bundles' `_CodeSignature/CodeResources` files are byte-identical (SHA-256 `6686de10…5aee629e9b`)
and list no resource files.

## Live Engine bundle: a ReWire device build of the engine

**arm64 slice. Observed:**

- `__TEXT,__text` at `0x828` has size 0, and the 14,376 bytes of `__TEXT` after the load commands are zero.
- The export trie (8 bytes) and the function-start table are empty.
- The only symbol is the undefined `dyld_stub_binder`.
- Ghidra discovered 0 functions. The [stub dossier](../../analysis/ableton-live-12.4.3/r2/h3-x86-bundles-v1/dossier/engine-arm64-stub/queries.json)
  finds no function, symbol or incoming reference at `0x828`. `str:dyld_stub_binder`
  resolves to `0x4024` in `__LINKEDIT`, which only symbol-table data at `0x4010` references.

So nothing can be disassembled or decompiled: the arm64 slice contains no code.
**Inferred:** a native arm64 process can map the slice, but it finds no `RWDEF*`
entry points in it. **Unknown:** why the slice exists. A build that compiles the
target for both architectures with every source excluded on arm64 would explain
it, but no evidence shows this.

**ReWire device entry points. Observed** in the x86_64 corpus, which has 75,348
functions and none pending:

- `_RWDEFOpenDevice` (`0x3ae20`) returns 5 unless `OEngineReWireData::SIsReWireDeviceEnabled`
  is true and there is at least one output channel. It then calls
  `OReWireMemoryInitializer::Open` (`0x3ab70`), which runs `OceanEngineInitO`,
  `OceanSongInitO`, `OceanProcessorInitO`, `OceanMidiInitO`, `OceanMidiSyncInitO`,
  `OceanSampleInitO` and `OceanPluginInitO`, registers request callbacks and returns 1.
- `_RWDEFIdle` (`0x3b120`) creates an `OEngine` (`OEngine::SNew`, audio and idle
  activation) when shared-memory slot 0 appears, and tears it down when the slot
  disappears.
- `_RWDEFIsPanelAppLaunched` (`0x3b380`) and `_RWDEFIsCloseOK` (`0x3b0c0`) test
  that slot. `_RWDEFLaunchPanelApp` and `_RWDEFQuitPanelApp` only return 1.
- `_RWDEFDriveAudio` (`0x3b3e0`) does three things:
  - synchronizes `OEngine::SetBeatTime` and `SetPlaying` to the host position,
    divided by the constant 15360.0 read at `0x15bb428`;
  - renders into the host buffers;
  - clears the buffers when no engine is attached.

**Device name. Observed:** `OEngineReWireData::DetermineReWireDeviceName` (`0xe71a0`)
is called only from the `OEngineReWireData` constructor, and only when the stored
name is empty. It writes the bytes `[Disabled]` (immediates at `0xe7292`/`0xe72a0`)
followed by `Ableton Live` (`0x16bd296`), or by `Ableton Live (Reason)` (`0x16bd280`)
when a debug option is set. `_RWDEFGetDeviceNameAndVersion` copies that name.

**Process boundary. Observed:**

- `OSharedMemory::SInit<false>` (`0x112150`) maps a shared block and checks
  `0x61626c65`, a version word of 13 and `AVersionInformation::AppAndVersionString`.
  It then waits up to 3,000 ms for the peer.
- On timeout it logs `OSharedMemory: ReWire handshake timed out.` (`0x16be371`) and
  falls back to private `malloc` memory.
- A named mutex `/ableton.live.omessage-factory` (`0x16bd656`) guards message
  allocation.

**Inferred:**

1. The mixer loads the bundle and calls `RWDEF*`.
2. The Ocean engine then runs inside the mixer's process.
3. Live's interface process acts as the panel application and exchanges state and
   messages with that engine through shared memory.

This is consistent with ReWire's mixer/device/panel roles but is not runtime-proven.

**Other engine behavior. Observed:** `SUseEngineCodeGeneration` (`0x750e0`) returns
`ableton::system::runningOnNativeArch()`, which reads `sysctl.proc_translated`.
A debug option can override it. Inferred: the engine turns off its code-generation
path under Rosetta.

**Contents. Observed:**

- Typed classes cover the transport, scheduler, clips, warping (`OWarperElastique`,
  `OWarperBeats`), built-in device processors (Operator, Simpler/Sampler, EQ Eight,
  Glue, Looper and others), recording, Link, VST2/VST3/AU hosting (`OVstPlugin`,
  `OVst3Plugin`, `OAuPlugin`) and Max devices (`OMxDeviceProcessor`).
- GoogleTest code is linked in.

So the bundle is the engine itself, not a plug-in bridge or a Rosetta helper.

### Consequence for analysis: a named copy of Live's engine code

**Observed** in [engine-vs-live-exports.json](../../analysis/ableton-live-12.4.3/r2/h3-x86-bundles-v1/macho/engine-vs-live-exports.json)
and the byte scans:

- The Engine exports 297 `OEngine` methods by name, including `OEngine::SetPlaying(bool,bool)`,
  `SetBeatTime(double)`, `RequestForSetPlaying`, `ScheduleDelayedBeatTimeJump` and
  `TStartBeatTime::Downbeat`. Live exports none of them in either slice, and neither
  slice contains the mangled names `OEngine10SetPlaying`, `OEngine11SetBeatTime` or
  `OEngine8BeatTime`.
- Both Live slices still contain the same engine classes and logging strings:
  typeinfo `7OEngine` and `12OFireManager`, `OEngine.Decouple`,
  `TransportEngineStateChanged` and `products/live/Live/OceanEngine/Src/OMessage.cpp`.
- Export names in common with the Engine: 29,843 in Live x86_64 and 21,636 in Live arm64.

**Inferred:** the Engine's x86_64 corpus is a named, fully decompiled compile of
the engine-side code that is anonymous in Live. It is a candidate symbol donor.
For example, a string such as `OEngine.Decouple` can be followed from a named
Engine function to the unnamed Live function that uses the same string. This bears
directly on S3 (transport transitions). Equivalence between the compiles is not
established. The Engine corpus can also be browsed through
[the helper catalog](../../analysis/ableton-live-12.4.3/browse/r2/r2-index.html).

arm64 MultiF0 selection (built in unless a developer option selects the dylib)
is in [helper launch, Live side](helper-launch-live-side.md#multif0-q-013-arm64-only).

## ReWire.bundle, MakeAlias and the install path

**Observed:**

- `ReWire.bundle` carries Propellerhead build paths
  (`/Users/buildmac/Jenkins/workspace/JBuildComponentMac/Projects/ReWire/…`),
  `NSReWireIPC` shared-memory and FIFO classes, and `NSSmuggler` bundle loaders.
- It also carries the string `RWPRegisterDevice: Device is a file (only bundled devices are supported)`.
- `Resources/MakeAlias` is an x86_64-only `MH_EXECUTE` (SHA-256 `b4e4c40d…dd1b673ed`,
  macOS 10.13). Its usage line is `Usage: %s originalFile aliasDir aliasName`, and
  it calls `FSNewAlias`.

**Observed in Live x86_64 only** (file offsets in [live-install-and-mf0.json](../../analysis/ableton-live-12.4.3/r2/h3-x86-bundles-v1/needles/live-install-and-mf0.json)
and [live-bundle-names.json](../../analysis/ableton-live-12.4.3/r2/h3-x86-bundles-v1/needles/live-bundle-names.json);
virtual address = file offset + `0x100000000`):

- A contiguous `__cstring` run at `0x10612f16f`–`0x10612f39a`:
  - `InstallPropellerheadDlls: `, `kLocalDomain`, `kUserDomain`;
  - `… is either missing or not up to date, will install`;
  - `/Propellerhead Software/ReWire`, `/bin/rm`, `/usr/bin/ditto`;
  - `Ableton Live Engine.bundle`, `InstallPropellerheadDlls: 'Ableton Live Engine.bundle' not found`;
  - `Ableton Live Engine`, `Ableton Live Engine_64`;
  - `InstallPropellerheadDlls: 'MakeAlias' not found`, `SDeleteAlias: ran helper tool: '/bin/rm' `.
- Near `LReWireHost` (`0x10612e9c2`):
  - `ReWire-Mach-O` and `ReWire.bundle`;
  - error keys `sErrorCantInstallReWireDll`, `sErrorCantInstallRexDll`,
    `sErrorCantInstallReWireEngine`, `sDialogInstalledReWireEngine`,
    `sErrorAuthorizationCancelled` and `sErrorAuthorizationFailed`.
- `RWPRegisterReWireDeviceImp` and the other `RWP*Imp` names.

None of `Ableton Live Engine`, `ReWire-Mach-O`, `ReWire.bundle`, `Propellerhead Software`,
`InstallPropellerheadDlls` or `RWPRegisterReWireDevice` occurs anywhere in the
Live arm64 slice. The arm64 slice still contains ReWire interface classes and
`----- Running as ReWire Device -----` (`0x105bc1a38`).

**Observed** in the ReWire SDK code linked into the Engine. Live x86_64 carries the
same four search names at file offsets `0x5f9e5d0`–`0x5f9e620`; Live arm64 carries
none ([live-rewire-sdk-loader.json](../../analysis/ableton-live-12.4.3/r2/h3-x86-bundles-v1/needles/live-rewire-sdk-loader.json)):

- `_ReWireLoadReWireSharedLibrary` (`0xb6fa70`) tries `ReWire Debugging.bundle`,
  then `ReWire Testing.bundle`, then `ReWire.bundle`.
- `FUN_00b6fbf0` resolves each name under `FSFindFolder(0xffff8003, 'asup')`
  and then `FSFindFolder(0xffff8004, 'asup')`, followed by `Propellerhead Software/ReWire/`.
- The loaded bundle is accepted only if `CFBundleGetVersionNumber() & 0xff800000 == 0x01800000`.

**Inferred** (domain constants and NumVersion layout from Apple's Carbon
conventions, not from the bundle): the search covers the local domain, then the
network domain, `Application Support`, and requires ReWire major version 1 with
minor version 8 or later. The shipped 1.8.7 qualifies. The resulting chain is:

1. x86_64 Live copies `ReWire.bundle` from `Resources/ReWire-Mach-O` into
   `…/Application Support/Propellerhead Software/ReWire/` with `ditto`, possibly
   after asking for authorization.
2. It places an alias to `Ableton Live Engine.bundle` there with `MakeAlias`.
3. Mixer applications then find Live's engine through the ReWire library.
4. Live itself, as a ReWire mixer, loads devices such as Reason through the same library.

The shipped `ReWire.bundle` is not loaded from inside Live's bundle.

## MultiF0: polyphonic pitch and note estimation

**Observed** in the dylib (string addresses are image VAs):

- `ircam-a2n` in the install name.
- SuperVP strings: `supervp` (`0x4268cd`), version `2.99.45` (`0x4268f0`),
  `SVPmain` and `audiosculpt-bugs@ircam.fr`.
- Multiple-F0 option formats such as `fm%f,fM%f,F%f,sn%f,smooth%d,M%f,E%f,cgn%f%s`
  (`0x424a88`), `writeNoteToText` (`0x423f78`) and `writeF0ToText` (`0x423fb0`).
- Its signal-processing imports are Accelerate vDSP FFT routines plus BLAS/LAPACK.
  It links no CoreAudio, AudioToolbox or CoreMIDI.

Exported API, observed in the complete corpus (1,896 functions: 1,077 exported,
814 with warnings, 5 failed; [pseudocode](../../analysis/ableton-live-12.4.3/r2/h3-x86-bundles-v1/pseudocode/multif0/)):

| Export | Observed behavior |
| --- | --- |
| `mf0p_GetApiRevision` `0x193ca0` | Returns 10 |
| `mf0p_GetMajorVersionNumber` / `Minor` / `GetRevisionNumber` | Return 0 / 0 / 16 |
| `mf0p_GetDefaultParameters` `0x193de0` | Fills 64 bytes: ints 0, 1; floats 40, 3140, 6, 0.093, 15, 23, 1.3, 19, 20, 0.001, 0.1, 0.01, 3; int 8 |
| `mf0p_RunMultiF0OnAudio` `0x1956d0` | Takes three arguments, the third an optional string; builds an analysis object and worker, starts it, busy-waits on a flag at worker `+0xcd`; returns a handle |
| `mf0p_GetProgress`, `mf0p_GetStatus` (`handle[3]+0xbc`), `mf0p_CancelProcess` | Progress, status and cancellation on the handle |
| `mf0p_GetMultiF0Result` `0x194050` | Returns `{records, count}`; each 32-byte record has three 4-byte fields, a count, an array pointer at `+0x10` and a value divided by an analysis-wide float |
| `mf0p_FreeMultiF0Result`, `mf0p_FreeHandle` | Free result arrays; cancel if still running, then free the handle |

**Inferred:** this is offline audio-to-note transcription that yields note events
with per-note trajectories. The field meanings are **unknown**. That 40 and 3140
are the F0 search bounds in Hz is a guess consistent with the `fm`/`fM` options.

**Observed in both Live slices:**

- `Misc/MultiF0/Mac/libmultif0_64.dylib`, all nine `mf0p_` names Live resolves,
  `API revision does not match. Loaded $1, expected $2.` and
  `MultiF0: No MultiF0 library found at `.
- `Audio2Midi: Use dynamic loaded MultiF0 lib` / `Audio2Midi: Use builtin MultiF0 lib`
  (arm64 VAs `0x105be168d`/`0x105be16b8`).
- `TBuiltinMultiF0InterfaceImpl` and `TDynamicMultiF0InterfaceImpl`.
- `third-party/MultiF0/src/matmtl/…`, which shows MultiF0 source compiled into Live.
- The menu strings `Create>Convert Harmony|Melody|Drums to New MIDI Track`.

**Inferred:** Convert Harmony and Convert Melody use MultiF0. Native arm64 Live
must use the built-in copy because it cannot load an x86_64 dylib. **Unknown:**

- which implementation x86_64 Live selects by default (the two `Audio2Midi:`
  strings look like debug-option labels);
- whether Convert Drums uses MultiF0;
- whether the two copies produce identical results;
- whether a libstdc++-linked x86_64 dylib still loads on current macOS.

## What follows for a native arm64 Live

| Component | Features it may serve | Native arm64 consequence |
| --- | --- | --- |
| Live Engine bundle | ReWire device mode: Live's engine inside another host's process (FEAT-ECOSYSTEM, FEAT-AUDIO) | Inferred unavailable: the slice is empty and arm64 Live has no install or locate strings |
| ReWire.bundle and MakeAlias | ReWire mixer mode (hosting Reason and similar devices) and the device install | Inferred unavailable: ReWire has no arm64 code, and arm64 Live lacks the SDK loader names |
| MultiF0 dylib | Convert Harmony/Melody to New MIDI Track (FEAT-WARP/FEAT-MIDI boundary, audio analysis) | Feature retained through the built-in copy (inferred); the dylib is an alternative implementation |

For the reimplementation, the following items are proposed:

- Treat ReWire as out of scope unless [Q-001](../questions.md#q-001-compatibility-targets)
  requires Rosetta-mode parity.
- The document schema still declares `MidiTrack/ReWireDeviceMidiTargetId` (`Int`,
  `Type="-4"`) in `Schema/12.0_12402.txt` line 5089 (SHA-256 `b7c9d4c7…0f299`);
  `9.5_315.txt` line 2957 has `ReWireSlaveMidiTargetId`. A compatible loader
  probably has to tolerate or preserve this field (FEAT-PERSISTENCE).
- Audio-to-MIDI conversion is a separate, analysis-heavy feature. Its observable
  contract (note output for given audio) needs reference captures, not this library's internals.

## Questions that need the main Live project

1. The callers of the x86_64 install strings (`0x10612f16f`–`0x10612f39a`, `0x10612ea01`):
   - when does `InstallPropellerheadDlls` run (startup, preference, first ReWire use)?
   - which domain does it choose?
   - which alias name, `Ableton Live Engine` or `Ableton Live Engine_64`, is created?
2. Whether x86_64 Live ever loads the Engine bundle into its own process, or only
   registers it for mixers.
3. The condition behind `OEngineReWireData::SIsReWireDeviceEnabled`. What replaces
   the `[Disabled]` device name once Live attaches?
4. The callers of `0x105be168d`/`0x105be16b8` and of `MultiF0: No MultiF0 library found at `
   in each slice: the default implementation, the fallback order and the user-visible error.
5. Whether arm64 Live's ReWire classes (`AppHasReWireDevices`, `FakeReWireHostProblems`)
   are reachable, and what they show.
6. Matching named Engine functions to Live arm64 functions through shared strings,
   as a naming aid for S3.

## Unknowns and limits

- This is static analysis only. No mixer, Rosetta or Live process was observed.
  Presence of a string is not a code reference.
- Whether ReWire is still offered to users in 12.4.3 is not established here.
  Release notes and the manual were not captured. One shipped lesson,
  `Builtin Lessons/3-Hardware Setup Category/3-Connecting MIDI Controllers Lessons/LessonsJA.txt`,
  still cites a manual chapter titled with ReWire.
- The localized text for `sDialogInstalledReWireEngine` and the related keys is not
  located. `App-Resources/Languages.alp` was not decoded.
- MultiF0 pseudocode chunks 5 and 6 were read before the decompile finished. They
  were committed, and their hashes were unchanged afterwards. The MultiF0 Ghidra
  project was not opened.
