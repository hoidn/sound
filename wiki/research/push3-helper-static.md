---
id: RESEARCH-PUSH3-HELPER-STATIC
type: research
status: draft
updated: 2026-10-17
access: analysis
target: Ableton Live 12 Suite 12.4.3
---

# Push 3 helper: role and external interfaces (static)

Packet H5 of [roadmap revision 2](native-decompilation-roadmap.md#revision-2-proposal--2026-10-17),
for FEAT-ECOSYSTEM. Bounded question: what the Push 3 helper does and which
interfaces it exposes to the hardware, to Live and to the network. This is static
evidence only: nothing was executed, and Live cannot run on this host. A static
call edge or string is not proof of runtime behavior.

Evidence: [h5-push3-v1](../../analysis/ableton-live-12.4.3/r2/h5-push3-v1/)
(`manifest.json` holds a SHA-256 for every file). Run `python3 -I extract.py out` and
`python3.11 -I pyc_summary.py > out/pyc-summary.txt`. `out/checks.txt` records 12
self-checks; all passed. Retained pseudocode is in `out/functions/<entry>.c`.
Sources:

- the Ghidra 12.1.4 bulk corpus and indexes of the helper's arm64 slice (method in
  [corpus tooling](r2-corpus-tooling.md));
- the Push3.app bundle;
- string offsets in `derived/Live.arm64`;
- the Push2DisplayProcess indexes in `r2/c-tooling-v1`, for comparison.

Addresses below are static arm64 virtual addresses in the helper slice unless marked
otherwise.

## Identity

| Item | Observed value |
| --- | --- |
| Bundle | `Contents/Helpers/Push3.app`, 2,028 files without AppleDouble files |
| Bundle ID | `com.ableton.Push3`, executable `Push3`, version `1.0` (`Info.plist`); `LSBackgroundOnly` true; minimum macOS 11; SDK macosx15.5 |
| Executable | Universal x86_64/arm64, SHA-256 `32e6f87b…ae22be`; arm64 slice at offset 42,811,392, 39,286,192 bytes, SHA-256 `8a2b77c9…c079b7ec` |
| Signature binding | The app's `Contents/_CodeSignature/CodeResources` entry for `Helpers/Push3.app` has cdhash `VNyrEHFP+L62Oj9OQNB8ZU4nAO8=`. That equals the x86_64 slice CodeDirectory hash. Requirement: `identifier "com.ableton.Push3"`, team `MWR434WD94` |
| Build | Version string `12.4.3` (`0x101838b89`); commit string `e3d8be4d07c71dbd4de9e4183bf90652f680375b` (`0x10183b505`), which matches the pinned build tag `2026-07-07_e3d8be4d07`; bytecode `co_filename` prefix `output/Live/mac_universal_64_static/Release/Push3.app` |
| Corpus | 104,161 eligible functions: 104,120 decompiled and 41 failed. The binary is stripped, so names come from RTTI strings and Ghidra analysis |

**Inferred:** the helper is built from the same source tree and commit as Live 12.4.3.

## Role

- **Observed:** the helper is a native C++ application. It statically links CPython 3.11
  (pyc magic 3495), pybind11, Skia with HarfBuzz, nanomsg, a data-model library named
  `flip` (`modules/flip/...`, `flip::Message`, `flip::BackEndBinary`), SQLite, OpenSSL,
  libcurl/cpr, boost.asio and spdlog. The evidence is source-path and RTTI strings plus
  the absence of matching dylib imports. It dynamically loads only `@rpath/libusb-1.0.dylib` (bundled) and
  system frameworks: CoreMIDI, CoreAudio, AudioToolbox, Security, CoreText,
  SystemConfiguration, AppKit, Foundation and CoreFoundation (`out/macho.json`,
  `out/imports.json`). It does not link Qt. One rpath, `@loader_path/../../../../Qt/lib`,
  points at Live's Qt.
- **Observed:** the constructor of `ableton::push3::Application` takes a `FlipClient`,
  a `ScriptHost`, a `screen::Screen*` and a `dbus::IPush3DBusServer*` (RTTI string
  `0x101571874`). `runMainLoop<RealMidiIo, display::UsbDisplay>` takes the screen, a
  `process_control::ControlledProcessSocket<Watchdog>*` and the `FlipClient`
  (`0x101570b54`). A separate `MidiHub<RealMidiIo>` exists (`0x1015711a6`).
- **Observed:** `ScriptHost` runs a Python control-surface package named `Push2` that is
  shipped inside the helper (`Resources/python/Push2`, 237 entries). It is passed the
  literal `"Push2"` (string `0x10183769b`, referenced at `0x10017d39c` in FUN_10017cfa0). That package is not Live's MIDI
  Remote Script of the same name: 90 file names are shared, no shared `.pyc` is
  byte-identical, and 12 Live entries are absent (`out/bundle.json`).
- **Observed:** the Python `Live` API is served by `live_model`, Python wrappers over
  flip objects (`live_model/model.pyc` names `LiveFlip`, `_flip_object`,
  `FlipSignalConnection`). The embedded modules are `BrowserBackend`, `UsbInterface`,
  `WifiConnector`, `Screen`, `WebService`, `SoftwareUpdater` and `MidiRemoteScript`
  (FUN_1002313d8).
- **Inferred:** the helper is the Push application itself. It runs the Push script,
  renders the display and drives the hardware, and treats Live as a remote document
  server. For Push 2 the split is different: Live runs the script and the display
  process only renders (see the comparison below). The same code base also carries
  standalone-device features: D-Bus, Wi-Fi, a local web service, Linux syslog and
  avahi, and `.swu` software updates. Which of these are active on macOS is unknown.

## Launch and process model

**Command line** (`entry` at `0x1001bdfa0`; boost::program_options group `Push 3
options`):

| Option | Help text or default (observed) |
| --- | --- |
| `log-file` | Default `Push3.log` in the preferences folder |
| `log-level` | Default `info` |
| `dont-log-to-console` | Boolean switch |
| `log-to-syslog` | "linux-only feature" |
| `parent-process-id` | "Default is 0 and disables checking" |
| `screenshot-filename` | "write a PNG of the screen every 300ms" |
| `faceless` | Boolean switch, no help text |
| `no-parent` | Boolean switch, no help text |
| `python-log-filters` | Default `!Push2.push2_model,live_model.model` |
| `webservice-id-file` | "used by the web service for unique identification by the Live integration" |
| `update-server-url` | Default `https://hardware-updates.ableton.com` |
| `crashpad-fd` | Default −1 |
| `language` | Default `EN`; `KR` and `ZH` select the CJK Noto font, anything else Japanese |

**Live side, strings only.** These are in `derived/Live.arm64`, SHA-256
`3a99ceea…`, at the file offsets listed in `out/live-strings.json`:

- launch arguments: `--log-level=`, `--python-log-filters=`, `--show-developer-window`,
  `--dont-log-to-console`, `--faceless`, `--emulator`, `--emulator-device=ah05`,
  `push-app-launching`, `inproc://`, `--parent-process-id=` and `Helpers`, contiguous
  at file offsets `0x5c08e16`–`0x5c08ef7` (`Helpers` at `0x5c08ef0`);
- the three channel names below and `Live.0.0.316` (`0x5cac862`);
- `FlipMessageStreamSocket send …` messages.

**Inferred:** Live starts the helper from `Contents/Helpers` with
`--parent-process-id=<Live pid>`. The helper's parser defines neither
`--show-developer-window` nor `--emulator*`, so those strings serve another target.
Which one is unknown.

**Startup** (FUN_10017cfa0):

1. Sleep for a duration of `0x3b9aca00` (inferred 1 s).
2. Search CoreMIDI for the hardware. "No Push hardware found" is thrown as
   `std::runtime_error`.
3. Create the `UsbDisplay`, with its Push 3 flag set when the hardware type is 1.
4. Open MIDI, the flip socket and the `ScriptHost`, then enter the main loop.

**Watchdog** (`process_control::Watchdog`; table built in FUN_1006678a0, names in
FUN_100668c58 and FUN_100668d74). Timeouts are read from `0x1015c09a0` as six u32
values: 5000, 20000, 20000, 1000, 2000 and 4000. The main loop advances the watchdog
by 500 every 500,000 accumulated microseconds, so the units are inferred to be ms.

| From | Event (id) | To | Timeout to kShutdown (ms) |
| --- | --- | --- | --- |
| kLaunched (0) | kReceiverThreadStarted (0) → kWaitForUsb (1); kUsbDeviceOpen (3) → kWaitForReceiverThread (2) | | 20000 ("neither background thread started nor USB device connected") |
| kWaitForUsb (1) | kUsbDeviceOpen (3) | kSendFirstSync (3) | 20000 ("USB device wasn't connected in time") |
| kWaitForReceiverThread (2) | kReceiverThreadStarted (0) | kSendFirstSync (3) | 20000 ("background thread not started in time") |
| kSendFirstSync (3) | kAckReceived (2) | kRunning (6) | After 1000 ms, kSendSecondSync (4) |
| kSendSecondSync (4) | kAckReceived (2) | kRunning (6) | After 2000 ms, kSendThirdSync (5) |
| kSendThirdSync (5) | kAckReceived (2) | kRunning (6) | 4000 ("live didn't ack in time") |
| kRunning (6) | kLiveStillRunning (1) | kRunning (6) | 5000 |

kProcessDefunct (4) moves kLaunched and the three sync states to kShutdown (7), and
kRunning to kDefunct (8).

- **Observed:** each time the main loop accumulates 500,000 µs, FUN_100668408 raises
  kLiveStillRunning, unless a nonzero parent pid fails `kill(pid, 0)` (FUN_10066df0c).
  The liveness test is therefore process existence, not responsiveness.
- **Observed:** the sync signal is a one-byte message `0x00` sent on the flip socket
  (FUN_10017ff30 → FUN_1006677a8). If sending fails, the log says "Failed to send
  sync signal to parent process. Shutting down."
- **Observed:** received process-control messages are parsed into a six-alternative
  variant. The named types are `AckMessage`, `ShutdownMessage`,
  `ProcessDefunctMessage` and `UserDataMessage`. Alternative 2 raises kAckReceived,
  alternative 3 invokes the shutdown callback, and alternative 5 carries user data
  (dispatchers `0x100180864`, `0x100180878`, `0x1001808a4`).
- **Unknown:** the byte values of the received messages.
- **Inferred:** with a parent pid, the helper exits about 5 s after Live disappears.
  It also exits if Live does not acknowledge the sync within 7 s of the first sync.
- **Unknown:** the effect of `--faceless` and `--no-parent`. They are read only in the
  main-loop exit test together with a `UsbDisplay` flag (`+0x17c`). A separate field
  that gates the hardware search (`+0x46`) is never set by the parser.

## Interface to the hardware

**USB** (shared `push-usb-interface` library):

| Fact | Observed value | Location |
| --- | --- | --- |
| Vendor ID | `0x2982` | FUN_1013e5b58 |
| Push 2 match | idProduct `0x1967`, bDeviceClass `0x00`; logged as "rev" value `0x41` | FUN_1013e5b58 |
| Push 3 match | idProduct `0x1969`, bDeviceClass `0xEF`; "rev" value `0x42` | FUN_1013e5b58 |
| Selection | Caller argument 0 selects Push 2 and 1 selects Push 3; claims interface 0; logs "Push display USB device opened" | FUN_1013e5b58 |
| Hotplug | `libusb_hotplug_register_callback(ctx 0, event 1, flags 0, 0x2982, 0x1969, class −1, …)` | FUN_1013ebf50 |
| Bulk OUT | Endpoint `0x01`, bulk, 1000 ms timeout, synchronous and asynchronous | FUN_1013eff5c, FUN_1013f00c8 |
| Bulk IN | Endpoint `0x81`; synchronous 1000 ms; asynchronous 512-byte buffer, no timeout | FUN_1013f0008, FUN_1013f0ae4 |
| Display frame | 16-byte header `ff cc aa 88` plus 12 zero bytes (`0x101809960`), then a payload of `0x50000` = 327,680 bytes on the OUT endpoint | FUN_1013ec2f8, FUN_1013ec734 |
| Frame pacing | The next rendered frame is received with a timeout argument of 1,800,000,000 (inferred ns, so 1.8 s); the frame-rate estimate is smoothed with factors 0.2 and 0.1 | FUN_1002776a4 |
| System info | 16-byte request `f8 f8 13 13 0a 00 …`. The response is 40 bytes with magic `0xFFF000FE` and version 1, and logs engineering run, flash lock, compute module, battery, serial number, uptime and firmware package version | FUN_1013e70cc, FUN_1013ed848 |
| Firmware | Python enum `FirmwareType` has `xmos`, `pmc`, `xy_sensor`, `apc` and `imagery`; Python exposes `firmware_info`, `start_update` and `engineering_run`. The RTTI classes `push_usb::detail::{Xmos,Pmc,Apc,XYSensor,Imagery,StartupImage,DataPartitionFirmware}Update` and `FlashFirmwarePackageVersionCommunication` also exist | FUN_1002353d0; RTTI strings |

**Inferred:** 327,680 = 160 × 2,048. That is consistent with a 960 × 160 display at 2 bytes
per pixel plus line padding. **Unknown:** the pixel format and whether the payload is
masked. The publicly known Push 2 XOR pattern does not occur as a repeated 8-byte
constant in the slice.

**Bundled firmware** (paths under `Resources/python/Push2/firmware/`; hashes in
`out/bundle.json`): `push2/app_push2_stable_1.0.71.upgrade`, and in `push3/push3_fw_1.5.4/`
the files `push3_xmos_fw_1.0.91.upgrade`, `push3_pmc_fw_1.20.pmc`, `push3_apc_fw_1.9.apc`,
`push3_xy_fw_0.13.bl2` and `push3_imagery_0.7.bin`. The formats were not analyzed.

**MIDI to the hardware:**

- **Observed:** FUN_1002867e0 creates the CoreMIDI client "Push 3 port search". It
  compares each source's and destination's `kMIDIPropertyModel` with `Ableton Push 2`
  and `Ableton Push 3`.
- **Observed:** RtMidi opens the found ports through clients "RtMidi Input Client" and
  "RtMidi Output Client". The port names given are `Ableton Internal Input` and
  `Ableton Internal Output` (FUN_10017eabc, FUN_1001cbfec).
- **Inferred:** under RtMidi semantics those are the helper's own port names, not
  device port names.
- **Unknown:** whether the virtual-endpoint imports (`MIDISourceCreate`,
  `MIDIDestinationCreate`) are reached. They have no direct callers.
- **Observed sysex constants** (`Push2/sysex.pyc`, SHA-256 `e1b75304…`):
  - `MANUFACTURER_ID (0,33,29)`;
  - `MESSAGE_START = F0 + MANUFACTURER_ID + (1,1)`;
  - identity product bytes Push 2 `(103,50,2,0)` and Push 3 `(105,50,3,0)`;
  - message IDs: mode switch 10, pad velocity curve 32, set pad parameter 38, set
    audio controls 55, get audio controls 56, power command 57, get power state 58,
    set RGB LED 59, get host mode 62, get firmware update results 66 and get pad
    velocity curve 67.

## Interfaces to Live

| Channel | Transport | Helper role | Evidence |
| --- | --- | --- | --- |
| `push-flip-api-ipc-channel` | nanomsg, `ipc://` + `temp_directory_path()` + name | Connects (vtable `0x101bcf110` slot `0x38` → FUN_100181150 → `nn_connect`) | FUN_10017f084, FUN_100180a80 |
| `push-to-live-midi-ipc-channel` | Same | Connects (same class) | FUN_100220998 |
| `live-to-push-midi-ipc-channel` | Same | Binds (vtable `0x101bd4098` slot `0x38` → FUN_10022142c → `nn_bind`) | FUN_100220f38 |
| Real-time data | Named shared-memory segment; the name is a client id supplied at runtime; it holds a named object `RTSync`; permissions `0644` | Opens; that the segment already exists is inferred | FUN_1013f1be0, FUN_1013f1ca4 |
| Live browser database | SQLite file `<shared user dir>/Ableton/Live Database/Live-files-12300.db` (`{}-files-{}.db`, `0x300c`) | Opens; read-only use is inferred | FUN_1001ccc6c, FUN_10063e970 |

- **Observed:** the bind/connect distinction rests on nanomsg's `create_ep` bind flag:
  0 in `0x100a20064` and 1 in `0x100a1fe48`.
- **Observed:** all three sockets use protocol value 16 (`0x101570410`).
- **Inferred:** value 16 is `NN_PAIR`. Push2DisplayProcess logs "Opening IPC pair
  socket".
- **Observed:** a push-to-live message is the raw MIDI bytes of one message followed by
  8 bytes of a caller-supplied value (FUN_10022cb04). The message variant covers note,
  aftertouch, CC, program change, channel pressure, pitch bend, MTC, song
  position/select, tune request, SysEx and realtime `F8/FA/FB/FC/FF`.
- **Inferred:** the 8-byte value is a timestamp.
- **Observed (flip API):** the helper and Live both contain the model string
  `Live.0.0.316`. The helper names 369 flip messages across 35 model classes
  (`out/flip-messages.tsv`). The largest classes are Song with 76,
  BrowserServices 66, Track 30, Clip 21 and ExtensionHost 19.
- **Observed:** service-level messages include:
  - `MidiServices.push_is_ready` and `RealTimeServices.request_mapping`/`mapping_response`;
  - `AudioServices.try_setup_audio_device_for_push`;
  - `LicenseServices.authorize_call` and `Root.refresh_token`;
  - `M4lServices.grab_control`/`send_midi`;
  - `ExtensionHost.show_modal_web_view_call`.
- **Inferred:** the process-control `UserDataMessage` on the same socket carries flip
  traffic, so Live is the flip document server.

**Wire format:** **Unknown.** The flip wire encoding and the mapping from the six
variant alternatives to byte values were not traced.

## Network interfaces

These facts are observed in the binary. Whether each one is active in tethered mode
on macOS is unknown.

- **Updates:** `https://hardware-updates.ableton.com` and the path `{}/api/v1/update/{}/`.
  Channels are `push3-dev`, `push3-release`, `push3-12-public-beta`,
  `push3-12-private-beta` and `push3-12-release`, chosen by regular expressions
  over the version (FUN_1001b015c). Update files are `update.swu` and
  `combo-update.swu`.
- **Service discovery:** UDP multicast `224.76.78.75`. Port bytes `0xad51` are stored
  into the socket address (FUN_1002ad94c).
- **Local web service:** sources under `WebService/html`; `/api/v1/challenge` and
  `/api/v1/challenge-response`; the `Ableton-Challenge-Response-Token` cookie; a
  `sessions` SQLite table; and a `webservice.db`/`webservice.id` pair.
- **Cloud authentication:** OIDC (`auth_client::OidcClient`) and `local.transfer`.
- **Crash reporting:** the `sentry-sdk 1.32.0` Python package.

**Inferred:** the stored port bytes decode to port 20909 in network order. From
outside knowledge, not checked here: Ableton Link uses the same multicast address
with a different port.

## Display rendering

- **Observed:** rendering is native, using Skia with HarfBuzz text
  (`font_rendering::SkiaAndHarfbuzzFont`, `TypefaceRegistry`).
- **Observed:** the scene graph uses `screen::SceneNode` plugins. They include
  activity, breadcrumb, browser contents, count-in, MIDI clip, real-time image,
  real-time waveform and recording waveform.
- **Observed:** assets are 10 `.otf` fonts and 663 PNG images under `Resources/assets`.
- **Observed:** Python drives the content through the `Screen` module, with
  `update_display` and `screen_id_to_string`.
- **Observed:** there is no QML in the helper.

## Comparison with the Push 2 display process

| Aspect | Push3 helper | Push2DisplayProcess |
| --- | --- | --- |
| Bundle ID | `com.ableton.Push3` | `com.ableton.Push2DisplayProcess` |
| UI technology | Skia/HarfBuzz scene graph, no Qt | Qt 5 QtQuick/QML, 153 `.qml` files |
| Control script | Runs its own embedded `Push2` Python package through CPython 3.11 | None; Live runs `MIDI Remote Scripts/Push2` |
| MIDI to hardware | CoreMIDI through RtMidi | No CoreMIDI imports |
| USB display | Shared `push_usb::DisplayUsbCommunication`; same VID/PID/class code | Same shared code (match at Push2 FUN_1001bbd74) |
| IPC to Live | Three named nanomsg channels plus flip, real-time shared memory and a process-control watchdog | One nanomsg pair socket; options `push2-ipc-channel` (default `push2ipc`) and Live-side `--push2-parent-process-id=` |
| Model | flip document `Live.0.0.316`, 369 messages | Not examined here; Live hosts the script |
| Extra | Firmware and OS update, web service, D-Bus mock, Wi-Fi, service discovery, Live database reader | None observed |

## Facts that could support a future specification

Candidates only. Any FEAT-ECOSYSTEM Push spec needs a scope decision (Q-005) and
review first.

- Hardware identification: USB `0x2982:0x1969` with class `0xEF` (Push 3) and
  `0x2982:0x1967` with class `0x00` (Push 2); MIDI model names `Ableton Push 2` and
  `Ableton Push 3`; sysex identity bytes.
- Display transport: interface 0, bulk OUT `0x01`, a 16-byte header, then a
  327,680-byte payload. Pixel encoding still has to be established.
- Helper lifecycle as externally observable process behavior: launch arguments,
  log file `Push3.log`, and shutdown timing after Live exits or fails to acknowledge.
  The timing is unverified.
- Live's dependency surface for a Push 3 integration: a document-sync API
  (flip `Live.0.0.316`), MIDI forwarding channels, and real-time playhead/waveform data.

These are interface constants of Ableton hardware and protocols. Whether a
clean-room product should implement the original Push integration at all is a
scope decision, not an analysis result.

## Unknowns

- The display pixel format and masking; the frame rate.
- The flip wire format, and the byte values of the process-control messages.
- Whether `faceless`, `no-parent`, the web service, Wi-Fi, D-Bus, service
  discovery and software updates are active on macOS.
- What the `ah05` hardware type is. It is the third `HardwareType` value after
  `push2` and `push3` (FUN_100239a64), and Live passes `--emulator-device=ah05`.
- The firmware file formats, and when flashing is triggered.
- The open mechanism and layout of the real-time segment. Reachable imports are
  `open`, `ftruncate`, `fchmod`, `mmap`, `shmdt` and process-shared mutexes, which
  suggests a file-backed mapping; that is inferred.
- Whether the helper also serves Push 2 in practice: its code accepts `0x1967`, but
  hotplug is registered for `0x1969` only.

## Live-side questions (need the main Live project)

1. Which function builds the helper argument vector, and under what condition? Anchor:
   the strings at file offset `0x5c08e16` onward.
2. Does Live bind `push-flip-api-ipc-channel` and `push-to-live-midi-ipc-channel` and
   connect `live-to-push-midi-ipc-channel`?
3. Which bytes encode Ack, Shutdown, ProcessDefunct and UserData, and what does Live
   do on the helper's `0x00` sync?
4. How does Live serve the flip document (`FlipMessageStreamSocket`)? Which of the 369
   messages does it implement?
5. Who creates the real-time segment, and how is the client id chosen
   (`RealTimeServices.request_mapping`)?
6. Which executable receives `--emulator`, `--emulator-device=ah05` and
   `--show-developer-window`?
7. Does Live choose between Push2DisplayProcess and the Push3 helper by hardware type?

## Phase 4 probe records

All of these need the macOS reference host, a Push 3 and, for P5-06, a Push 2.
Hardware availability is not established. Batch them under
[ADR 0002](../decisions/adr-0002-static-first-analysis.md).

| ID | Question | Input and capture | Discriminating observation | Stop |
| --- | --- | --- | --- | --- |
| P5-01 | Does Live launch the helper, and with which arguments? | Start Live with Push 3 in Control mode; `ps -axo pid,ppid,args` | `Helpers/Push3.app/.../Push3` child with `--parent-process-id=<Live pid>` | One capture each with and without Push 3 |
| P5-02 | Socket roles and paths | `lsof -U -a -p <pid>` for both processes; list `$TMPDIR` | Listener of each of the three channel names | All three attributed |
| P5-03 | Watchdog timing | (a) `kill -9 <Live pid>`; (b) `kill -STOP <Live pid>` for 30 s; time the helper's exit and read `Push3.log` | Static prediction: (a) exit after about 5 s; (b) no exit, because `kill(pid, 0)` still succeeds | Three repeats of each |
| P5-04 | Behavior without hardware | Launch path with Push 3 unplugged and replugged | No launch, "No Push hardware found", or a hotplug wait | Each case once |
| P5-05 | Display frame encoding | USB capture of the bulk OUT endpoint | Header and payload sizes; frame rate; pixel/mask pattern on a known screen | 10 s capture |
| P5-06 | Push 2 path | Connect Push 2 instead | Which display process runs | One capture |
| P5-07 | Network activity in Control mode | `tcpdump` on `224.76.78.75` and the update host | Packets present or absent | 5-minute capture |
| P5-08 | MIDI path | Live MIDI preferences plus `lsof`/MIDI Monitor | Whether pads reach Live through CoreMIDI or the push-to-live channel | One pad press per path |
| P5-09 | Real-time segment | `vmmap`/`lsof` on the helper | Backing file or shared-memory name | One capture |

## Gaps and next step

The smallest next step is Live-side question 2. Use the Live corpus string index to
find the references to the three channel strings, then trace whether `nn_bind` or
`nn_connect` follows. That needs the main Live project, which is outside this packet.
