---
id: RESEARCH-HELPER-LAUNCH-LIVE-SIDE
type: research
status: draft
updated: 2026-10-17
access: analysis
target: Ableton Live 12 Suite 12.4.3 arm64
---

# Helper launch and supervision: the Live side (packet N4)

**Question.** For each helper (plug-in scanner, index, Push 3, web connector,
add-ons, swapper), how does arm64 Live start it, with which arguments and
environment, under which conditions, how does it handle the helper's messages,
exit, crash or restart, and which side binds each nanomsg channel? Which MultiF0
copy does arm64 Live use? The helper-side halves are in
[plug-in scanner](plugin-scanner-static.md), [browser index](browser-index-static.md),
[Push 3 helper](push3-helper-static.md) and
[web connector, add-ons, swapper](web-addons-swapper-static.md); MultiF0 is in
[x86_64-only bundles](x86-only-bundles.md). Questions: Q-013 to Q-016 in
[questions](../questions.md).

Everything here is a static derivation from `Live.arm64` (SHA-256
`3a99ceea…383cfad`). Nothing was executed; Live cannot run on this host. A call
edge or string does not show that a path runs. Function names such as
`TProcessController::LaunchWithArguments` come from RTTI, `std::function` type
strings and exported template symbols; they are evidence, not proof. ReWire
install strings exist only in the x86_64 slice, whose analysis had not finished;
they are left to a later pass.

## Evidence

[n4-helper-contracts-v1](../../analysis/ableton-live-12.4.3/r2/n4-helper-contracts-v1/manifest.json):
query results `results/n4-0001`–`n4-0006` (46 function dossiers with
disassembly), corpus pseudocode of 70 further cited functions in `corpus-code/`,
string-to-function tables `anchor-string-refs*.txt` from the C2 strings index,
the small read-only scripts used, and `notes.md` (round log, derived tables,
negative results). `manifest.json` lists a SHA-256 for every file. Function
addresses are entries in the arm64 image; string addresses are image VAs.

## Shared mechanism (all helpers except the web connector)

**Observed.**

- Launch goes through `TProcessController::LaunchWithArguments(path,
  vector<TString> argv, unique_ptr<INanoMsgSocket>, TWindowStyle,
  TPriorityClass)` at `0x1025da348` (lambda type names at vtables `0x1067e3688`,
  `0x1067e3718`). Callers: scanner `0x103179e68`, index `0x1002b4b14`, add-ons
  `0x102966254`, Push 3 `0x1038f0914`, Push 2 display `0x1025dee98`.
- Each launch builds a `TProcessObserver` whose states are exposed to Python as
  `Push2ProcessState` (`0x1039fa2a4`): 0 initialized, 1 launching, 2 running,
  3 connected, 4 died, 5 terminated, 6 killed, 7 wait_for_termination,
  8 defunct_process_wait_for_termination, 9 defunct_process_terminated,
  10 defunct_process_killed.
- The transition table is built in `0x1025db270` (call `0x1025e6af0(from, to,
  trigger)`; confirmed in n4-0002 disassembly at `0x1025db3e0`–`0x1025db52c`).
  Event names are the table at `0x1067e3ea8`.

| From | Event or timeout | To |
| --- | --- | --- |
| initialized | KLaunched | launching |
| launching | KProcessObservedRunning | running |
| launching | KGotSync | connected |
| launching | KShutdownRequested | wait_for_termination |
| launching | 20000 ms | died |
| running | KGotSync | connected |
| running | KProcessNotObservedRunning | died |
| running | KShutdownRequested | wait_for_termination |
| running | 60000 ms | killed |
| connected | KProcessNotObservedRunning | died |
| connected | KShutdownRequested | wait_for_termination |
| connected | KProcessDefunct | defunct_process_wait_for_termination |
| wait_for_termination | KProcessNotObservedRunning | terminated |
| wait_for_termination | 5000 ms | killed |
| defunct_process_wait_for_termination | KProcessNotObservedRunning | defunct_process_terminated |
| defunct_process_wait_for_termination | 5000 ms | defunct_process_killed |

- `TProcessController::OnTimer` runs every 1000 (`0x1025d94cc` passes 1000 to the
  timer service) and, per observer, raises KProcessObservedRunning or
  KProcessNotObservedRunning from a process-alive query and adds 1000 to the
  elapsed count used by the timeouts (`0x1025d9d14`). Observers in states 4, 5,
  6, 9 or 10 are removed.
- On a state change (`0x1025dcc88`, n4-0002): a KShutdownRequested transition
  sends one byte `0x02`; entering connected sends `0x01`; entering
  defunct_process_wait_for_termination sends `0x02`; entering killed or
  defunct_process_killed calls the process object's slot `+0x38` and drops it;
  entering a final state closes the socket. Then the owner's listener receives
  the new state.
- Control messages are one byte (`0x100e170d0`). Shared IPC code uses `0x00` as
  sync ("IPC: Failed to send sync signal to other site.", `0x1015a40d0`), `0x01`,
  `0x02` and `0x03` (`0x1015a4198`, `0x1015a4280`, `0x1015a420c`). User data is
  `0x04` followed by the payload (`0x100e17004`). Named events are framed as
  little-endian `u32 topic_length`, `u32 payload_length`, topic bytes, payload
  bytes (`0x104a04cd8` via `TNanoMsgIPCChannel` send `0x1015a3518`), and are sent
  only while the observer is connected (`0x1025ddb28`).
- Socket roles. Live's socket is either
  `ableton::nanomsg::NanoMsgSocket<NanoMsgApi, ServerTrait<NanoMsgApi>>` (vtable
  `0x1065928b0`) whose open slot `0x10027a130` calls the bind wrapper
  `0x1009032d8`, or the `ClientTrait` variant (vtable `0x106787a18`) whose open
  slot `0x1022c4120` calls the connect wrapper `0x1009032cc`. The two wrappers
  reach nanomsg's endpoint creator with bind flag 1 (`0x1049b2ed8`) and 0
  (`0x1049b30f4`), checked in the raw instructions. The protocol constant is 16
  (`0x1055d3960`).
- Addresses are built by `0x1002725dc`: `ipc://` + temporary-directory path +
  channel name, or `inproc://` + name.
- Random channel IDs come from `0x1014412dc(id, 7)`: one 32-bit random value,
  converted to text and cut to 7 characters.
- Helper executables resolve through `0x1011e8540(dir, name)`, with
  (`PluginScanner`, `Ableton Plugin Scanner`), (`Index`, `Ableton Index`),
  (`AddOns`, `Ableton AddOns`), (`WebConnector`, `Ableton Web Connector`) and
  `Ableton Swapper`.

**Inferred.**

- Protocol 16 is `NN_PAIR`, as on the helper side.
- `0x01` is the acknowledgement and `0x02` the shutdown request; this matches the
  helpers' six-alternative variant (alternative = byte + 1: ack 2, shutdown 3,
  user data 5) described in [Push 3 helper](push3-helper-static.md#launch-and-process-model).
- Receiving `0x00` from the helper raises KGotSync, so a helper is connected once
  it has sent its sync and Live has answered `0x01`.
- The executables resolve to `Contents/App-Resources/Extensions/<dir>/<name>`,
  the bundle layout recorded on the helper pages.
- Both sides use the same temporary directory because the child inherits
  `TMPDIR`. No explicit environment setup was found in any launch path.
- A helper that has connected and then hangs is not killed by this table:
  connected has no timeout. Only a shutdown request starts the 5 s kill timer.

**Unknown.** What the process slot `+0x38` does (SIGKILL is assumed); the text
form of the random ID (hex is assumed); the timer unit (milliseconds is assumed
from the 1000 increments).

## Plug-in scanner

Addition 2026-10-17 from the [SPEC-PLUGIN-DISCOVERY](../specs/plugin-discovery.md)
draft check: the VST2 system folders are `~/Library/Audio/Plug-Ins/VST` and
`/Library/Audio/Plug-Ins/VST`.

Mediator `TPluginScannerMediator` (anonymous namespace; listener lambda RTTI
referenced from `0x10317c884`).

**Argument table (Observed, `0x103179e68`, n4-0001).**

| Order | Argument | Value and condition |
| --- | --- | --- |
| 1–2 | `--db` | `Live-plugins-1.db` in the database folder (`0x1015ed930`, stored by `0x1002cbaf8`, read through app slot `+0xa60`) |
| 3–4 | `--cid` | 7-character random ID; Live binds `ipc://<tmp><id>` |
| per format | `--vst2` / `--vst3` / `--au` | Key 8 → `--vst2`, 16 → `--vst3`, 4 and 32 → `--au` (table `0x1068d88f0`, rotate test confirmed at `0x10317a100`). Value: `ID=PATH` items joined with `,` |
| optional | `--reset`, `all` | Only when the request's reset flag is set (`ldrb [x,#0xcc]`, `0x10317a6dc`). Live never sends `vst2` or `vst3` |
| optional | `--limit=N` | Only when a debug option is present; N is its first argument, default 50, sent if ≥ 1 (`0x10317a7cc`) |
| last 2 | `--lang`, code | Current UI language (`0x1015041e0`) |

Window style 1, priority class 0. Log line `Plugins: start scanner process`.

**Folders and domain IDs (Observed).** VST3 (`0x1031c0f28`, `0x1031c0144`):
`user` = home + `Library/Audio/Plug-Ins/VST3`, `local` =
`/Library/Audio/Plug-Ins/VST3`, `custom` = the custom folder. VST2
(`0x1031b8e5c`, `0x1031b7f94`): `user` and `local` from a path service with
selectors 2 and 3, `custom`. The builders `0x1031c0d2c` and `0x1031b8c68` add
the system pair and the custom entry each behind a separate Boolean preference.
Inferred: those are `Vst3UseSystemFolders`/`Vst3UseCustomFolder` and the VST2
pair. A VST3 command line would look like
`--vst3 user=/Users/<u>/Library/Audio/Plug-Ins/VST3,local=/Library/Audio/Plug-Ins/VST3`.

**Launch conditions (Observed).**

- `APluginSettingsPreferencesModel::OnRescanPlugins` (`0x10035e3fc`) reads the
  modifier mask and requests a rescan with reset when bit 2 is held
  (`0x1012946e8`, `0x101294398`). Inferred: Option/Alt-click on Rescan.
- The plug-in manager (`0x103169978`, logs `PluginManager: Scan start`) loops over
  format handlers. A handler with an out-of-process descriptor (VST2 and VST3:
  slot returns `this+0x30`, `0x1031b7820`, `0x1031bf9c8`) contributes its
  domains; a handler without one is scanned in-process through its own slot.
- `0x103179994` ignores a request while a scan runs, stores the reset flag,
  creates a process controller named `plugin-scanner`, registers the listener and
  launches.

**Messages (Observed, `0x10317bcf0`).** On connected, Live creates the channel
`live->plugin-scanner` and registers `scan` (plain payload), `update` (JSON keys
`total`, `current`) and `current-plugin` (key `name`). `scan` = `done` sets
result 1, `interrupted` 2, anything else 0 (`0x10317c810`). Inferred: `update`
and `current-plugin` drive the status text through `0x10317ad9c`.

**Lifecycle (Observed, n4-0001 at `0x10317c068`).**

| State | Result | Action |
| --- | --- | --- |
| died | 2 (`interrupted`) | Log `finished a chunk of work.  Continue`; clear reset flag; relaunch |
| died | 0 (no or unknown result) | Log `stopped prematurely.  Restart`; clear reset flag; relaunch |
| died | 1 (`done`) | Log `stopped`; finish (`0x10317c634`) |
| terminated, killed | any | Finish |

No restart counter exists in this path. Inferred: a scanner that always dies
before reporting relaunches without limit; the helper's own crash bookkeeping
(`unconfirmed` → `on-retry` → `disabled`) is what ends a crash loop. A plug-in
that hangs after the helper connected is not timed out by Live.

**Unknown.** Which handler owns keys 4 and 32, and whether either ever has an
out-of-process descriptor (if so, the scanner would reject `--au`); the exact
VST2 folders behind selectors 2 and 3; the folder behind the database path
service; the debug-option name for `--limit`.

## Index

**Argument table (Observed, `0x1002b4b14`, n4-0003).**

| Argument | Value |
| --- | --- |
| argv[1] | Path of a JSON options file `com.ableton.index.<id>.txt` in the folder from path service slot `+0x78` (`0x1002b5da4` builds the one-element argv) |

Options written by `0x10163abe4`: `db-path` (from app slot `+0xa58`),
`ipc-channel` (the 7-character ID; Live binds), `usage-data_file`,
`fileref-map-path` (`0x1002e957c`), `parent-pid` (`getpid()`), `log-traces`
and `os-events-flags` (debug-option strings), `profile-log` (debug option
present), `db-stats-trigger` and `db-stale-factor` (`0x10122ed30`,
`0x10122ed88`; the same values configure Live's own database), `sound-analyzer`
(`0x100237fe8`), `auto-keywords` (`0x10326fa58`) and `features`. Priority class
from a debug option, default 2. Inferred: the helper maps a bare argument to
`options-file` (its parser passes the name `options-file` to the shared parse
routine `0x1001b2b18` in the helper).

**Conditions (Observed).** Init step `StartIndex` is added unless run mode is 2
(`0x1002cc484`). `ALiveApp::StartAppIndex` (`0x1002cab2c`) proceeds only without
the no-UI flag, when app slot `+0x718` is true, without a debug option, and in
run mode 0. Inferred: slot `+0x718` is "first instance".

**Messages and lifecycle (Observed, `0x1002b56c4`).** Connected: log
`Indexer: connected`, channel `live->indexer`, handler `done`, then
`0x10023894c` is called with "launch count > 1" (Inferred: a restart flag for
the browser side). Died while not stopping: if
the launch count is at most 100 (`cmp w8,#0x64`, `0x1002b5a30`) log
`stopped prematurely [n]. Restart` and relaunch, else `Giving up`. Terminated or
killed: `Indexer: killed`, clear the channel. A deliberate stop clears the
count.

**Unknown.** The database file prefix, folder and version written (callers of
`{}-files-{}.db` builder `0x103f1aff4`); `usage-data_file` source; the `features`
list; how Live consumes the helper's events.

## Add-ons

**Argument table (Observed, `0x102966254`, n4-0003).** One argument
`--cid=<7-character ID>` (format `L"--cid={}"`); Live binds. Window style 1,
priority class from a debug option, default 2.

**Conditions (Observed).** Init step `AddOns` is added unless run mode is 1 or 2
or either of two debug options is present (`0x1002cc484`). The process starts on
demand: `0x1029627a0` creates a controller named `addons` and launches it when a
hub request arrives and it is not running (callers `0x102962ea8` and six
others). `ALiveApp::StartAppAddOns` (`0x1002cacf0`) calls a hub slot with the
value 600000; its meaning is unknown.

**Lifecycle (Observed, `0x1029668e8`).** Connected: `AddOns: connected`, channel
`live->addons`, handler `done`. Died with the stopping flag: `process stopped`.
Died otherwise: restart while the launch count is at most 10
(`cmp w8,#0xa`, `0x102966bd0`), else `Giving up` and the hub is told the channel
is gone. Terminated or killed: `AddOns: killed`, reset the count. Stop requests
(`0x102962a04`, `0x102962a54`, `0x102962a9c`) send KShutdownRequested.

## Web connector

The web connector does not use `TProcessController`; it is started as a plain
subprocess (`0x1012479e4`, `0x101247d40`) with its own socket.

**Argument table (Observed, `0x1008eb988`, n4-0004).**

| Order | Argument |
| --- | --- |
| executable | `WebConnector/Ableton Web Connector` |
| 1 | `<resources>/Python/scripts/ableton_ping.pyc` (`.py` if the `.pyc` is missing and run mode is not 2; development builds use `../../AppWebConnector/Resources`) |
| 2 | `web_connector_args_<pid>.txt` in the folder from path service slot `+0x70` |
| 3–4 | `--crashpad-fd`, n, only when a descriptor is passed; `StartWebConnector` passes −1, so not sent |

The JSON file holds `pid`, `session_id`, `ipc_channel_id` (`wc` + 7 characters;
Live opens a server socket on it before writing the file, channel
`webconnector->live`), `version`, `platform` = `mac`, `architecture`,
`wordsize` = `64`, `app_base_path`, `app_exe_path`, `wait_for_confirmation`
(true when an update-controller setting equals 1), `autoupdates_dir_base_path`, `aip_usage_data_dir`,
`services_endpoint`, `live_variant`, `crash_detection_file`, `commands`,
`logging` (`file_path`, `log_level` default `info`), `swapper_exe`,
`directory_connection` (debug option), `skip_vcredist_update` (debug option),
`usage_report_prefix` and `swapper_sentinel_file`.

**Conditions (Observed).**

- Start: the init step `StartWebConnector` is always added. `0x1008eb988` returns
  with `WC start disabled` unless an application object's virtual slot `+0x720`
  is true or one of three debug options is present.
- `commands`: `upload_event_logs` when `0x10189ee9c` allows (run mode 0, no debug
  option, and a preference when `0x1011c4750` returns 4).
  `check_for_auto_updates` when `0x101a4517c` is false, auto-update is enabled
  (`0x1017ec96c`: debug override, else slot `+0x720` or an option, then the
  preference), and the volume holding the application bundle (executable folder
  + `../..`, `0x1008f000c`) has more than 3 GiB available
  (`cmp x20,#0xc0000001`, `0x1008ec36c`; Inferred: the compared field is
  `space_info.available`). Otherwise Live logs
  `Too little disk space for potential Live update` and records the usage event
  `no_sufficient_space_for_auto_update`.
- A 60 s timer started beside it (`0x101447d84(60000, …)`) writes usage data; it
  does not restart the connector.

**Messages (Observed).** Handlers registered in `0x1008e7b74`:
`update_available` → state 1 when confirmation is required, else 2
(`0x1008f365c`); `vcredist_needs_install` → 3; `update_ready_to_apply` → 5;
`update_failed` → 6 (`0x1008e81f0`). Live sends `continue` (then state 2 or 4,
`0x1008e8114`, `0x1008e8450`) and `cancel` (`0x1008e852c`). Inferred from the
nearby text keys: state 1 is the "update available" dialog with Continue, Remind
Me Later and Preferences buttons; 2 is downloading; 5 is ready; 6 is the error.

**Unknown.** What slot `+0x720` tests; any restart policy (none found); the
values of `session_id`, `architecture` and `live_variant`.

## Swapper

**Observed.**

- Live never launches the swapper; it passes `swapper_exe` to the web connector.
- `swapper_sentinel_file` is filled only from a debug option; otherwise it is
  empty (`0x1008eb988` around the key at `0x105b1b87a`).
- At startup `0x1002ea094` always asks for running processes named
  `Ableton Swapper` (`0x1011e88b8`, confirmed at `0x1002ea554` in n4-0004). If
  one exists, `0x1002fe740` shows "There is an automatic update of Live
  currently in progress. Press OK to close this dialog and then wait a few
  moments before trying to restart Live again." (`0x10178ae84`) and exits
  through `0x1011a68f8` with code 42 (`Aborting with error code: `). In run
  mode 1, or when any of six debug options is present, a no-dialog flag is set
  first (`0x1011b5360`) and Live exits with 42 without the dialog.

**Unknown.** Any Live-side read of the sentinel file (none found).

## Push 3

**Argument table (Observed, `0x1038f0d4c`, n4-0005).**

| Argument | Condition |
| --- | --- |
| `--parent-process-id=<getpid()>` | Always |
| `--log-level=<value>` | Always; debug option value, else `info` |
| `--python-log-filters=<value>` | Debug option present |
| `--dont-log-to-console` or `--show-developer-window` | Developer-mode test and two debug options; the default branch sends `--dont-log-to-console` |
| `--faceless` | Debug option present (`0x1002ca298`) |
| `--emulator`, `--emulator-device=ah05` | Debug option present; the second if its value is `ah05` |
| `--crashpad-fd=<n>` | Never from this caller (−1) |
| `--language=<code>` | Always |

Executable: built from the running executable's folder, `Helpers` and
`Push3.app` (Inferred: `Contents/Helpers/Push3.app`); development builds use
another path. The channel is the fixed name
`push-flip-api-ipc-channel` (`KPushIpcChannelName`, `0x106a3e1b0`), and Live
binds `ipc://<tmp>push-flip-api-ipc-channel` (`0x1038f0914`). With a further
debug option Live only binds and waits for an already running app
(`0x1002ca4b8`, `0x1038f2160`).

**Channel roles (Observed).**

| Channel | Live | Helper (from the H5 page) |
| --- | --- | --- |
| `push-flip-api-ipc-channel` | binds (server socket, `0x1038f0914`) | connects |
| `push-to-live-midi-ipc-channel` | binds (`0x1022e8330`, `TPushMidiForwarder`) | connects |
| `live-to-push-midi-ipc-channel` | connects (client socket, `0x1022b927c`, `APushMidiOutDevice`) | binds |

**Conditions and lifecycle (Observed).**

- `TPushClientConnection::OnMidiDevicesChanged` (`0x1039b79fc`) starts the
  launcher when a presence flag (`+0x94` of a MIDI-side object) is set and the
  connection is enabled; when the flag clears (and no debug option), it sends a
  shutdown request (`0x1038f0838`).
- Before the first launch the launcher may kill processes with the same
  executable name (`KillLingeringProcesses`, `0x1025db018`, from `0x1038f08c4`).
- `TPushClientConnection::OnPushProcessStateChanged` (`0x1039b7ad4`): on died,
  defunct_process_terminated or defunct_process_killed, unless stopping, it arms
  a one-shot timer with 1500 (`mov w1,#0x5dc`, `0x1039b7b08`) whose callback
  relaunches (`0x1038fd748`). Killed and terminated do not restart. No counter.
- A missing executable logs `{}  not found`; a failed launch logs
  `Failed to start {}`.

**Inferred.** Push 3 presence is what sets `+0x94`. The release helper's parser
does not define `--show-developer-window` or `--emulator`
([Push 3 helper](push3-helper-static.md#launch-and-process-model)), so these only
reach development builds; the page's earlier guess that they serve another
target is superseded.

**Unknown.** Who writes `+0x94`; the flip document protocol; real-time shared
memory setup.

## MultiF0 (Q-013, arm64 only)

**Observed (`0x10307ae94`, n4-0006).** Without a debug option, Live creates the
built-in implementation and logs `Audio2Midi: Use builtin MultiF0 lib`. With the
option, `0x10307a630` takes a path from a second option or defaults to
`<resources>/Misc/MultiF0/Mac/libmultif0_64.dylib`, logs
`MultiF0: No MultiF0 library found at …` if absent, and `0x10307aa68` loads it
and requires `mf0p_GetApiRevision` = 10.

**Inferred.** arm64 Live uses the built-in copy by default; the shipped x86_64
dylib can only be selected by a developer option, and an arm64 process could not
load it. The x86_64 slice also defaults to the built-in copy ([Live x86_64 paths](x86-live-paths.md#multif0)). **Unknown:** the
callers of `0x10307c060` (no direct callers).

## Remaining unknowns

- Debug-option names: options are looked up by 32-byte digests
  (`0x1011aeb80`); simple hashes of known names did not match.
- AU discovery path and storage (key 4/32 handlers).
- What `process+0x38`, app slot `+0x718`, `+0x720` and run modes 1 and 2 mean.
- Index database prefix, folder and version; consumption of index events.
- Wire format received from helpers beyond the shared framing (parse side not
  traced).
- ReWire install and Engine alias: resolved as unreachable in 12.4.3 ([Live x86_64 paths](x86-live-paths.md#rewire)).

## Phase 4 probe records

All need the macOS reference host. Batch them under
[ADR 0002](../decisions/adr-0002-static-first-analysis.md); none is a gate.

| ID | Question | Minimal input and capture | Discriminating observation | Stop |
| --- | --- | --- | --- | --- |
| PRB-N4-01 | Scanner argv for Rescan and modifier-Rescan | `ps -axww -o pid,ppid,args` during each | `--vst3 user=…,local=…`; `--reset all` only with the modifier; no `--au` | One capture per kind |
| PRB-N4-02 | Scanner relaunch on crash and on limit | Test plug-in that crashes on load; 60 new test modules | Log `stopped prematurely.  Restart` vs `finished a chunk of work.  Continue`; launch count | Scan reaches `done` |
| PRB-N4-03 | Index options file | Copy `com.ableton.index.*.txt` at launch | Key set and values above, `db-path` folder and name | One capture |
| PRB-N4-04 | Restart caps | `kill -9` the index (or add-ons) helper repeatedly | Restarts stop after 100 (index) and 10 (add-ons) launches with `Giving up` | Cap reached once |
| PRB-N4-05 | Observer timeouts | Replace a helper by a stub that never sends sync; and one that ignores shutdown | Killed about 60 s after launch; killed about 5 s after shutdown request | Three repeats |
| PRB-N4-06 | Web connector commands | Copy `web_connector_args_<pid>.txt` with auto-update on/off and with < 3 GiB free | `check_for_auto_updates` present only with > 3 GiB and the setting on | Four combinations |
| PRB-N4-07 | Swapper-running guard | Start Live while a process named `Ableton Swapper` exists | Dialog text above; exit status 42 | One capture |
| PRB-N4-08 | Push 3 sockets and restart | `lsof -U` for Live and Push3; `kill -9` Push3 | Live listens on flip and push-to-live; Push3 relaunched about 1.5 s later | Three repeats |
| PRB-N4-09 | MultiF0 selection | Convert Harmony on arm64 Live with logging | `Audio2Midi: Use builtin MultiF0 lib` | One capture |
