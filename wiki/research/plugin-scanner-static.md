---
id: RESEARCH-PLUGIN-SCANNER-STATIC
type: research
status: draft
updated: 2026-10-17
access: analysis
target: Ableton Live 12 Suite 12.4.3
---

# Plug-in scanner: static evidence (packet H1)

**Question.** What externally observable behavior does Live's plug-in scanner
helper implement? This covers how it is invoked, which formats and folders it
scans, what it writes and reports, and how it treats crashes, hangs, invalid
plug-ins and duplicates. The question is bounded by the
[helper analysis](ableton-package-structure.md#helper-executables-analyzed--2026-10-17)
of `App-Resources/Extensions/PluginScanner/Ableton Plugin Scanner` and by FEAT-HOSTING in the
[feature map](../specs/feature-map.md).

**Answer (static, draft).**

- The helper is a command-line program. Live passes it:
  - a database path;
  - an optional IPC channel ID;
  - comma-separated `ID=PATH` scan roots for VST3 and VST2;
  - an optional reset scope, language and per-session limit.
- It scans **VST3, then VST2**. No Audio Unit or CLAP scanning code or option
  was found in it.
- Results go into an SQLite database. It has three tables: modules (one per
  bundle), plug-ins (one per class or shell entry) and domains (scan roots).
- Each module and plug-in has a scan state: `unconfirmed`, `ok`, `disabled`,
  `not-a-plugin` or `on-retry`.
- A module is loaded again only when it is new, or when its fingerprint changed,
  or when its state is `unconfirmed`. For both formats the fingerprint is the
  size and modification time of the bundle executable.
- Crash containment is by state:
  1. A module that kills the process stays `unconfirmed`.
  2. The next session marks one such module `on-retry`.
  3. The session after that marks it `disabled`.
- Progress goes to Live as `update`, `current-plugin` and `scan` messages over
  a nanomsg channel.
- The helper stops itself after a per-session module limit (default 50). It
  also stops when Live's channel goes away or the helper is orphaned.
- No hang timeout was found in the scan path.

Everything here is a static derivation from Ghidra 12.1.4 pseudocode, the
helper's data and strings. Nothing was executed. Live cannot run on this host.

## Evidence

All evidence is in [h1-plugin-scanner-v1](../../analysis/ableton-live-12.4.3/r2/h1-plugin-scanner-v1/manifest.json).
`run.sh` regenerates everything except the hand-written `keys.txt` and
`probe-batch.json`. The manifest lists the SHA-256 of every file.

| Input | Identity |
| --- | --- |
| Universal scanner `App-Resources/Extensions/PluginScanner/Ableton Plugin Scanner` | SHA-256 `59c196af…dbbfc`, 28,574,080 bytes |
| arm64 slice (offset 14,991,360), the analyzed program | SHA-256 `6ce847b0f56d842d638ca638546636ecdba66f5942fa668f4d2d3403f2a97ad6`, 36,879 functions |
| x86_64 slice (offset 16,384) | SHA-256 `293a284b…6726`; strings only |
| C1 corpus | 36,873 of 36,879 decompiled; 6 failures, 5 of them timeouts. One timeout is the database-open function `0x1005a30f8` |
| Live universal executable, strings only | SHA-256 `52289af6…a35ef`, the [pinned build](sources/ableton-live-12.4.3.md) |

Files:

- `options.json`: the option blocks of both slices.
- `tables.json`: enum name tables and watchdog constants.
- `sql.json`: 48 plug-in table SQL statements.
- `vtables.json`: vtables named from RTTI, by `macho_vtables.py`.
- `functions.tsv` and `pseudocode/`: 54 functions with corpus state, code hash and assigned role.
- `string-refs.tsv`: string to referencing function, from C2 `strings.jsonl`.
- `live-anchors.json`: Live strings, with slice and offset.
- `app-resources.json`: plug-in mentions in the lesson texts.
- `probe-batch.json`: the runtime probes.

Caveats:

- The binary is stripped. Class names come from RTTI type strings and gmock
  method-name strings. Method roles are inferred by matching argument counts
  to those name lists.
- The image links a large slice of Live's library: the browser file database,
  preset metadata, curl, OpenSSL, SQLite, gtest and gmock. A string in the
  binary is not evidence that the scanner uses it.
- Ghidra drops exception handlers, so catch paths are inferred.
- Addresses are arm64 image addresses unless stated otherwise.

Live side: argv, domain IDs, the reset mapping and the relaunch policy are in
[helper launch, Live side](helper-launch-live-side.md#plug-in-scanner).

## Invocation

**Observed.** `entry` `0x1001308e0` registers these boost::program_options
options under the caption `PluginScanner options`. The strings are at
`0x100a1067b`–`0x100a107dd`; the x86_64 slice has the same set.

| Option | Value type in code | Help text |
| --- | --- | --- |
| `--help`, `-h` | flag | `this help` |
| `--cid` | string | `communication channel id` |
| `--db`, `-d` | string | `path to database` |
| `--vst3` | string | `paths to scan for vst3 plugins` |
| `--vst2` | string | `paths to scan for vst2 plugins` |
| `--reset` | string | `reset plugin data before scanning. Possible values: 'all', 'vst2', 'vst3'` |
| `--lang`, `-l` | string | `language to use; defaults to 'EN'` |
| `--limit`, `-N` | int, default 50 (`0x32`) | `limit to check N candidates in one session` |
| `--verbose`, `-v` | bool | `verbose output` |

**Observed control flow in `entry`.**

1. It sets application identities ("Ableton", "PluginScanner", "12.4.3",
   "1.0") and ("Ableton", "Live", "12.4.3", "12.0").
2. With `--help`, or with neither `--vst3` nor `--vst2`, it prints the options
   and returns 1.
3. With no `--db` or an empty one, it logs `No database path` and returns 1.
4. It logs `Init: check for <limit> plugin modules per architecture maximum`.
5. With `--cid`, it builds an IPC run context (`TRunContext`). Without it, it
   uses `TNullRunContext`, whose alive check returns 1 and orphan check
   returns 0. Inferred: the scanner also runs standalone, without messages.
6. It opens the database at the `--db` path. On failure it logs
   `Error opening plugin scan database: <message>` and returns 1.
7. It scans VST3 if the parsed `--vst3` list is non-empty, then VST2 if the
   `--vst2` list is non-empty. The VST2 scan runs even when the VST3 scan was
   interrupted.
8. It sends `scan` = `done` only if every scan that ran returned success,
   otherwise `scan` = `interrupted`. It returns 0.

**Observed: scan-root syntax.** `--vst2` and `--vst3` take a single string,
parsed by `0x1001332fc`. The string is split on `,`. Each item is split at its
first `=` (`0x100137810`) into a pair: the part after `=` is the path, the part
before it is a domain ID string. An item without `=` gives the ID with an empty
path.

Inferred consequences:

- A path containing `,` cannot be passed.
- An ID with no path empties that domain: nothing is enumerated, so its stored
  modules are removed (see Database).
- What the domain IDs mean, and which IDs Live sends, is unknown.

**Observed: reset.** `0x100133b9c` returns true when `--reset` equals `all`
or the format name (`vst3` or `vst2`).

**Observed: Live side.**

- Strings in both Live slices, at arm64 slice offset `0x5be57e4` and nearby:
  - process name `Ableton Plugin Scanner`;
  - arguments `--db`, `--cid`, `--reset`, `all`, `--au`, `--vst2`, `--vst3`;
  - channel names `plugin-scanner` and `live->plugin-scanner`;
  - log lines `Plugins: start scanner process`, `Plugins: scanner process stopped prematurely.  Restart`, `Plugins: scanner process finished a chunk of work.  Continue` and `Plugins: scanner process stopped`.
- Live's preferences model has the keys `UseAUv2`, `UseAUv3`,
  `VstUseSystemFolders`, `VstUseCustomFolder`, `Vst3UseSystemFolders` and
  `Vst3UseCustomFolder`, at offset `0x5ab40ad`.
- Live has the strings `/Library/Audio/Plug-Ins/VST3` and
  `Library/Audio/Plug-Ins/VST3`, at offset `0x5be7c92`.
- The scanner contains no plug-in folder path.

Inferred: Live chooses the folders, and the scanner scans only what it is
given. The scanner does not register `--au`. Inferred: with boost defaults, an
unregistered option is a parse error, which takes the error path and returns 1.
So if Live passes `--au`, that call cannot reach a scan. Whether Live ever
passes it is unknown (PRB-H1-01).

## Formats, enumeration and loading

Corrections 2026-10-17 from the [SPEC-PLUGIN-DISCOVERY](../specs/plugin-discovery.md)
draft check: the VST2 `.vst` match ignores letter case (the VST3 `.vst3` match is
case-sensitive), and the crash-state update runs once per format pass, so with both
formats searched a crashed module is disabled within the next session rather than
the one after; the outcome (never examined again) is unchanged.

| Aspect | VST3 | VST2 |
| --- | --- | --- |
| Candidate walk | `0x1005e8cb4`: recursive iterator (options value 5, meaning unresolved). Each entry is canonicalized; a directory seen before is not descended again; a `.vst3` entry is a candidate and is not descended into. Candidates are a set of canonical paths per domain. Failures log `Can't resolve path:` and `Reading directory failed:` | `0x1005aad10`: breadth-first walk with a visited-folder set. A directory named `*.vst` (exact 4-byte `.vst` suffix) is a candidate. Other directories are queued with a relative path. Plain files are ignored. Failures log `VST2: Failed to scan folder:` |
| Stored relative path | empty | relative path of the bundle under its root (`plugin_domains.relpath`). Inferred: it feeds folder-structured VST2 browsing |
| Load | `0x100146ae4`: bundle `bundleEntry`, `GetPluginFactory`, `bundleExit`, with specific error strings | `0x100145d24`: `SecStaticCodeCreateWithPath` + `SecStaticCodeCheckValidity` with flags 9 (`0x10075325c`). Unsigned (`-67062`) continues; any other failure logs `VST2: Code signature verification failed for … with error …` and fails with `plugin has an invalid signature`. Entry point `main_macho`, then `VSTPluginMain`; name from `CFBundleName` |
| Plug-ins kept | factory classes with category exactly `Audio Module Class` | every entry the module reports, including shell sub-plug-ins |
| Instrument versus effect | flag 1 if a subcategory token equals `Instrument` (`0x100145768`), else 2 | flag 1 if a per-entry byte is set, else 2. Inferred: the synth flag |
| Fingerprint | `0x1001458a4`, via the VST3 adapter slot `0x100138a34`: `hex(st_size):hex(st_mtime seconds)` of the bundle's main executable | the same function, via the VST2 adapter slot `0x1001384a8` (vtable `0x100b43ab8`) |
| Host identity offered | not traced | host callback `0x100140cb8`: version 2400, vendor string `Ableton`, product `Live`, vendor version, current shell ID, canDo `shellCategory` answered non-zero, language from `--lang` |

Observed: the scanner contains no VST3 `moduleinfo.json` reader. VST3 class data
comes from loading the module. Also observed: `TVst3MetainfoParser` and the
`*vst3*` matcher in `0x1005eafd0` belong to `.vstpreset` metadata reading, not
to scanning.

## Per-session algorithm (one format)

This is a static derivation from `0x1005e9fd8` (VST3) and `0x1005aca28` (VST2).
The VST2 path has the same structure with architecture 2.

1. Log `<FMT>: start scanning plugins`. For each root, log
   `<FMT>: scanning plugins in <path> (<id>)`, enumerate candidates grouped by
   domain, and send `update` with `total` = candidates found so far and
   `current` = 0.
2. Call `UpdateUnconfirmedPluginsAndModulesState(processor)`. This is
   `0x1005a8258`, one transaction:
   1. plug-ins `on-retry` → `disabled`;
   2. one `unconfirmed` plug-in → `on-retry`;
   3. modules `on-retry` with no plug-in rows → `disabled`;
   4. one `unconfirmed` module with no plug-in rows → `on-retry`;
   5. modules `unconfirmed` or `on-retry` whose plug-ins are all `disabled` or `not-a-plugin` → `disabled`.
3. If reset applies, call `ResetScanData(arch, processor, domains)`
   (`0x1005a87f0`). It deletes those domains' rows for the architecture, then
   orphaned modules and plug-ins. Architecture 0 clears all three tables.
4. For each domain, read the stored modules (`ModulesScanData`, `0x1005a8e20`).
   - A stored module whose path is no longer a candidate is removed
     (`RemoveModules`).
   - A candidate whose current fingerprint equals the stored one, with stored
     state ≠ `unconfirmed`, is **skipped**.
5. For each remaining candidate:
   1. Ask the adapter's run state (`0x100138504`):
      - 1 (stop): Live's channel is gone or the helper is orphaned. Log
        `stopped scanning plugins` and return success.
      - 2 (limit): the limit is smaller than the number of modules confirmed
        this session. Log `interrupted scanning plugins` and return failure.
   2. Otherwise check the module, then send `update` with `current` + 1.
6. Log `<FMT>: finished scanning plugins` and return success.

**Module check** (`0x1005e91fc` VST3, `0x1005aba10` VST2):

1. Log `check plugin at path`. Compute the fingerprint; on failure log a warning.
2. Call `AddModuleCandidate(path, arch, processor, domain, fingerprint, relpath)`
   (`0x1005a4318`). A new module is inserted as `unconfirmed`.
3. For a module already stored, log `plugin already scanned. Retry` (stored
   state 0 or 4) or `… Rescan` (other states). Then `PrepareModuleForRescan`
   sets the new fingerprint and state 0, and returns the existing plug-in rows.
4. Send `current-plugin`, then load the module.
   - If loading fails: `not a plugin`, `RejectModule(state 3)`.
   - Otherwise, for each plug-in: report it, log `found` (with ` [retry]` for
     an existing plug-in in state 0 or 4) followed by the metadata fields.
     Then `ConfirmPlugin` (state 1, with device ID, name, vendor, version,
     SDK version, flags and subcategories) and `SetPluginEnabled(1)`.
   - Finally `ConfirmModule`, and the session count is incremented.

**Inferred crash consequences.** A module that kills the scanner stays
`unconfirmed`.

- If Live starts another session, that module becomes `on-retry`. It is then
  skipped, because its fingerprint is unchanged and its state is nonzero.
- In the session after that it becomes `disabled`.
- A disabled module is checked again only when its fingerprint changes, or after
  a reset. Then it shows `Rescan`, or `Retry` if its state was `on-retry`.

The name `on-retry` suggests a retry that this derivation does not find. The
derivation may miss Live-side handling (PRB-H1-02).

**Inferred limit boundary.** The check happens before each candidate. The count
grows only on confirmation and has its own counter per format. With `--limit 50`
that allows up to 51 confirmed modules per format per session. Live's
`finished a chunk of work.  Continue` string fits a restart after `interrupted`.

## Database

Observed tables, created by `0x1005e62d8`:

- `plugin_modules(module_id AUTOINCREMENT, path, arch, processor, scanstate, fingerprint)`
- `plugins(plugin_id AUTOINCREMENT, module_id, dev_identifier, name, vendor, version, sdk_version, flags, scanstate, subcategories, enabled)`
- `plugin_domains(id TEXT, module_id, relpath, enabled)`

`sql.json` holds every statement.

| Enum | Values | Source |
| --- | --- | --- |
| Architecture (`arch`) | 0 unknown, 1 AU, 2 vst2, 3 vst3 | name table `0x100b6eb50` |
| Scan state | 0 unconfirmed, 1 ok, 2 disabled, 3 not-a-plugin, 4 on-retry | `0x100b6eb70` via `0x10059b7a8` |
| Processor (bit mask) | 1 x86_64, 2 arm64; this slice always uses 2 (`0x1005aa7cc`) | `0x10059b7d0` |

**Observed.**

- The default name `Live-plugins-{}.db` is formatted with the integer 1
  (`0x1005a2b84`). The scanner itself opens whatever `--db` names.
- Older migrations add `fingerprint`, `relpath`, `sdk_version`, `flags`,
  `subcategories` and `processor`. The `processor` step also empties all three
  tables (`0x10024a1b4`). These migrations sit in the browser file-database
  migration chain (`0x10023459c`, `0x100234e8c`). Inferred: the plug-in tables
  once lived in that database.
- `0x1005a717c` writes CSV dumps of the three tables to `PluginScanDb.txt`, but
  no caller or pointer to it was found.
- The device-identifier vocabulary (`device:vst:`, `device:vst3:`, `instr`,
  `audiofx`, `midifx`; bit masks 8 for VST and 16 for VST3) is shared Live code
  (`0x100688b28`, `0x100689c1c`). The exact `dev_identifier` text was not
  derived.
- A normalization regex for vendor names (`0x1005aa7d4`) has no caller in the
  scanner.

## Messages, logging and supervision

**Observed.**

- The IPC address (`0x10013da2c`) is `ipc://` + `temp_directory_path()` + cid,
  concatenated as strings. An `inproc://` + cid form also exists.
- The channel is a `TControlledProcessIPCChannel` named `plugin-scanner->live`,
  over an `NNanoMsgIPCChannel::IIPCSocket`. Setup failure logs
  `Scanner: Failed to set up IPC channel.`, with ` Process orphaned.` when that
  applies.

Messages sent:

| Topic | Payload | Function |
| --- | --- | --- |
| `update` | JSON object `total`, `current` (compact rapidjson writer, `0x1002983cc` with pretty = 0) | `0x10013e06c` |
| `current-plugin` | JSON object `name`, with the value `<FMT>: <name>` plus an optional ` [<x>]` | `0x10013e284`, `0x100138588` |
| `scan` | plain `done` or `interrupted` | `0x1001308e0` |

The wire framing of topic plus payload, and which side binds, are unknown.

**Supervision.**

- The orphan check (`0x1001806e4`) uses `sysctl(KERN_PROC_PID)` and reads the
  field at kinfo_proc offset 0x230. Inferred: that is `e_ppid`, and the check
  is parent PID == 1. It is throttled to half of the first watchdog constant.
- `TLiveProcessWatchDog` lambda `0x10013f4fc` clears the channel-alive flag.
- The shared helper watchdog (`0x100149888`) has messages including
  `Shutting down because live didn't ack in time`.
- Constants at `0x1009a8ff0`: 5000, 20000, 20000, 1000, 2000, 4000. Inferred:
  milliseconds. Their mapping to states is unknown.

**Logging.**

- spdlog with pattern `%l: %v` and logger `plugscan`. Progress is logged at
  info, fingerprint problems at warn, load and signature failures at error.
- `--verbose` changes console logging.
- `PluginScanner.txt` is read as a config file (`0x10019a9d8`) with
  `log.level` (debug, info, warn, error, off) and `log.categories`. Its folder
  comes from a runtime path service (`0x1001c5f40`), unresolved.

## Shipped resources

Observed:

- The built-in lessons (`app-resources.json`) say only that third-party VST
  and Audio Units (Mac only) plug-ins complement built-in devices. They say
  plug-in support may need activating in the **Plug-In Sources** section of the
  Plug-Ins preferences
  (`1-Live Basics Category/4-Playing Software Instruments Lessons/LessonsEN.txt`
  lines 113 and 116, SHA-256 `0834f8fc…`).
- No other App-Resources text describes scanning. Max's own `vstscan`
  documentation is Max's, not Live's.

## Candidate requirements for SPEC-PLUGIN-DISCOVERY

Each is Proposed and statically derived. "Probe" means runtime confirmation is
needed before release. Internal wire and database formats are excluded unless a
row says otherwise.

| ID | Statement | Evidence | Status |
| --- | --- | --- | --- |
| PD-01 | Plug-in modules are loaded for discovery in a separate process, so a crashing module cannot terminate the host | Separate executable; Live restart strings | Static; probe PRB-H1-02 |
| PD-02 | VST3 and VST2 are discovered from host-configured roots. VST3 candidates are `*.vst3` entries found recursively, without descending into bundles. VST2 candidates are `*.vst` directories found breadth-first. Canonical paths are deduplicated and folder cycles ignored | `0x1005e8cb4`, `0x1005aad10` | Static |
| PD-03 | Unreadable folders or paths are logged and skipped. The scan continues | same | Static |
| PD-04 | A VST3 module contributes one plug-in per `Audio Module Class` factory class. It is an instrument when a subcategory is `Instrument`, otherwise an effect | `0x1005e91fc`, `0x100145768` | Static |
| PD-05 | A VST2 module whose code signature is present but invalid is not loaded. Unsigned modules are loaded | `0x100145d24`, `0x10075325c` | Static; probe optional |
| PD-06 | During VST2 discovery the host identifies itself as VST 2400, vendor "Ableton", product "Live". It answers the `shellCategory` canDo and reports the configured language. Shell sub-plug-ins are enumerated | `0x100140cb8` | Static |
| PD-07 | A module whose fingerprint (executable size and modification time) is unchanged and whose state is settled is not loaded again | `0x1005e9fd8`, `0x1005aca28`, `0x1001458a4` | Static; probe PRB-H1-05 |
| PD-08 | A module that disappears from its root is removed with its plug-ins | `RemoveModules`, orphan deletes | Static |
| PD-09 | A module that cannot be loaded is recorded as not a plug-in and not listed | `RejectModule(3)` | Static |
| PD-10 | A module that crashed discovery is excluded, and then disabled in a later session, until its fingerprint changes or data is reset | `0x1005a8258` plus the skip rule | Static derivation; **probe PRB-H1-02 before release** |
| PD-11 | A reset (all, or one format) discards stored discovery data for the given roots before scanning | `0x100133b9c`, `0x1005a87f0` | Static; UI mapping by PRB-H1-01 |
| PD-12 | Discovery proceeds in sessions of at most limit + 1 newly confirmed modules per format (default limit 50). The host restarts the helper until all candidates are processed | `0x100138504`, Live strings | Static; probe PRB-H1-04 |
| PD-13 | Progress is visible as total and current candidate counts and the current plug-in name | message builders | Static; UI rendering unknown |
| PD-14 | AU discovery is not performed by this helper | absence of code or option; arch enum includes AU | Static absence; probe PRB-H1-06 |

## Unknowns

- **Folders.** Which folders and domain IDs Live passes, how the Plug-In Sources
  toggles map to arguments, and whether a modifier on Rescan maps to `--reset`.
- **Audio Units.** Where Audio Units are scanned. Whether `--au` is ever sent.
- **Timeouts.** Any scan timeout or kill policy. The meaning of the watchdog
  constants.
- **IPC.** Wire framing and socket roles. Inbound messages from Live.
- **Database files.** The database folder and lifetime. The folder for
  `PluginScanner.txt`. What the database-open function `0x1005a30f8` does, such
  as journal mode, version checks and migration. It failed to decompile.
- **Identifiers.** The `dev_identifier` format. How VST2 names, vendors and
  shell IDs are read.
- **Duplicates.** How the browser presents duplicate class IDs across modules.
  The scanner does no class-ID deduplication.
- **Code signing.** Whether VST3 modules get a code-signature check. None was
  found.
- **Exit codes.** Exit codes on uncaught exceptions. Exception handlers are not
  in the pseudocode.

## Live-side questions for the main Live project

Anchors are Live arm64 strings.

1. **Arguments.** Callers of `Plugins: start scanner process` and `--cid`:
   - how argv is built (`SystemPluginScanPaths`, `CustomPluginScanPaths`);
   - the domain IDs;
   - when `--reset all|vst2|vst3` and `--au` are passed.
2. **Supervision.** `TPluginScannerMediator::ProcessStateChangedListener`:
   - the restart policy behind `stopped prematurely.  Restart` and `finished a chunk of work.  Continue`;
   - any timeout or kill.
3. **Preferences.** `APluginSettingsPreferencesModel`: `OnRescanPlugins`,
   `OnPluginRescanTypeChanged` and `OnPluginScanningChanged`, and their
   preference keys.
4. **Database consumption.** How Live reads the database:
   - `PluginsScanData`: whether it filters `scanstate = 1` and `enabled`;
   - how `disabled` and `on-retry` entries are shown;
   - where `SetPluginEnabled` and `SetDomainEnabled` come from in the UI.
5. **Audio Units.** The discovery path and its storage for `UseAUv2` and `UseAUv3`.

## Phase 4 probe batch

`probe-batch.json` holds eight records. Each has the question, the existing
evidence, why static evidence is insufficient, the minimal input, the
discriminating observation and the stopping condition. All need the macOS host
and test plug-ins built from public SDK samples.

| ID | Question |
| --- | --- |
| PRB-H1-01 | Exact argv per Plug-In Sources configuration and Rescan kind; `--au` |
| PRB-H1-02 | Crash: launches, scanstate sequence, listing |
| PRB-H1-03 | Hang: timeout, signal, resulting state |
| PRB-H1-04 | More than 50 new modules: modules per session |
| PRB-H1-05 | Fingerprint change, including a disabled module |
| PRB-H1-06 | Audio Unit discovery location and storage |
| PRB-H1-07 | Database and log-configuration locations |
| PRB-H1-08 | Duplicate bundles and duplicate class IDs |

## Limitations

- Function roles rest on RTTI and gmock name lists, argument counts and string
  references. No symbols or source were available.
- The pseudocode omits exception paths.
- The VST2 module-check internals (`createPluginInfo`, shell enumeration) and
  the VST3 load errors were read only for control flow.
- The x86_64 slice was compared by strings only.
