---
id: RESEARCH-BROWSER-INDEX-STATIC
type: research
status: draft
updated: 2026-10-17
access: analysis
target: Ableton Live 12 Suite 12.4.3
---

# Browser index helper: static evidence

Packet H2 of [roadmap revision 2](native-decompilation-roadmap.md#revision-2-proposal--2026-10-17),
outside-in from the `Ableton Index` helper and the shipped browser metadata. It
serves FEAT-UI (browser) and FEAT-PERSISTENCE (media references, tag sidecars).
Everything here is static. No Ableton code was executed, and Live cannot run on
this host. Pseudocode, function names and call edges come from Ghidra. They show
code structure, not runtime behavior. A `FUN_` name is Ghidra's label.

## Evidence identity

| Item | Identity |
| --- | --- |
| Helper | `Contents/App-Resources/Extensions/Index/Ableton Index`, universal SHA-256 `f989be02…45138`. Its arm64 slice is 16,602,976 bytes, SHA-256 `3390bd4b030c74080540d025b7688c8612d63a1abc89ea8f36162f2b9a289b62` ([helper manifest](../../analysis/ableton-live-12.4.3/r2/helpers-v1/manifest.json)) |
| C1 corpus | 43,737 eligible functions: 32,717 `exported`, 11,011 `exported-with-warnings`, 9 `failed` (7 timeouts), 0 pending |
| C2 indexes | 46,005 strings and 209,593 direct call edges; strings SHA-256 `95733c86…4ac6`; full list in the evidence manifest |
| Shipped database | `Contents/App-Resources/Database/filerefmap.db`, 9,412,608 bytes, SHA-256 `97b29374…67897`, the same file as REA evidence `ev_8d5e74b0…77b57` ([execution ledger](native-phase-execution.md#rea-analyzer-dependencies--2026-10-17)) |
| Live cross-check | Byte grep of `Live.arm64` `3a99ceea…383cfad` for 14 protocol tokens. Only presence is shown; cross-references were not resolved |
| Evidence | [`analysis/ableton-live-12.4.3/r2/h2-index-v1/`](../../analysis/ableton-live-12.4.3/r2/h2-index-v1/manifest.json) holds `run.sh`, seven scripts, `out/`, 35 key-function pseudocode files in `out/code/`, `probe-batch.json` and a SHA-256 manifest |

Function addresses below are entries in this slice. String addresses are the
defined-string addresses in `out/strings-*.tsv`.

## Process role and communication with Live

**Observed.**

- Command-line options at `0x100131790`, under the heading `AppIndex options`:
  - `slave,l`: "Slave mode";
  - `standalone,s`: "Stand-alone mode";
  - `os-notifications,t`: "Test OS notifications";
  - `libconfig,L`: "Path to library configuration file";
  - `dump-config-files`;
  - `options-file`: "File containing additional options".
- `entry` (`0x1001308e0`) picks controlled mode (`0x100132970`) by default and
  when `slave` is given. `standalone` picks command mode (`0x100133f90`), and
  `os-notifications` picks an OS-event test mode (`0x100135614`).
- It prints `ERROR: Invalid option file`, `ERROR: Reading option file` or
  `ERROR: No valid database path defined` and exits for those conditions. In the
  controlled branch it can also print `ERROR: No valid IPC channel defined`.
- The options file supplies these keys, read at `0x100673f10` and written at
  `0x100674318` (strings `0x100c59f99`–`0x100c5a030`): `db-path`, `ipc-channel`,
  `usage-data_file`, `fileref-map-path`, `parent-pid`, `log-traces`,
  `profile-log`, `os-events-flags`, `db-stats-trigger`, `db-stale-factor`,
  `sound-analyzer`, `auto-keywords` and `features`.
- Controlled mode does the following:
  - logs `IPC Channel`, `DB`, `Parent pid`, `Usage data file`, `Os Event Flags`
    and `Filerefmap` (`0x10014ddfc`);
  - opens the file-reference map read-only (`0x1005284c4` with mode 1);
  - builds an `ipc://` address from a path prefix (returned by
    `thunk_FUN_100711bb8`) plus the channel name, or an `inproc://` address
    (`0x10014e584`);
  - registers a channel named `index->live` (`0x100c1d398`).
- If the channel fails, it logs `Scanner: Failed to set up IPC channel.` and adds
  ` Process orphaned.` (`0x100c1d384`) when `FUN_10019fd6c` returns non-zero.
  That function is inferred, not shown, to be a parent-process check. It stops on
  `Shutdown request from Live` (`0x100150ab8`).
- The RTTI names include `TNanoMsgIPCChannel`, `TJsonIPCEvent<…>`,
  `TLiveObserverImpl` and `TDbIPCChannelImpl`. The last one is backed by an
  SQLite table `messages(id, sender, receiver, event_type, payload)` (`0x100c55df6`).
- Live-to-index command names, a table at `0x10016a6f8` with 25 entries (strings
  `0x100d240a8`–`0x100d243f4`): `ConfigureLibrary`, `StartDetection`,
  `SetFoldersNotScanned`, `EnableAutoUpdate`, `IncreaseUseCount`, `SetUseCount`,
  `RegisterFile`, `BindMetadata`, `BindCloudManagerData`, `SetColor`,
  `SetColors`, `ApplyKeywordChange`, `AssignUserKeywords`, `DeleteUserKeyword`,
  `RenameUserKeyword`, `SetContentSourceInfo`, `HandleFileOperation`,
  `ObserveNewFile`, `ReimportMetadataForPack`, `ReimportMetadataForPlugin`,
  `RebindSafeUserData`, `SetEnableSoundAnalyzer`, `UpdatePacks`,
  `UpdateUnavailablePacks` and `SetDeviceFolderVisibility`.
- Index-to-Live event names (strings `0x100d23e7e`–`0x100d24068`):
  - `FinishedActivity`, with keys `EventId`, `NeedsRefresh`, `UpdatedLocations`
    and `RefreshCategories`;
  - `ReportFileColorSetFirstTime` and `ReportFileColorChange`;
  - `ReportKeywordsChanged` and `ReportKeywordAssignmentsChanged`;
  - `ReportObservedFile`, `ReportActivity` and `ReportSoundAnalysisStatus`;
  - `SetDeviceFolderVisibilityDone`, `ConfigureLibraryFinished`,
    `UpdateMaxUseCount` and `ReportRegisterFileDone`.
- `Live.arm64` contains `Ableton Index`, `live->index`, `ipc-channel` (8 times),
  `db-path`, `fileref-map-path`, `parent-pid`, `usage-data_file`,
  `os-events-flags`, `db-stale-factor`, `sound-analyzer`, `auto-keywords`,
  `{}-files-{}.db` and `Library.cfg` ([grep](../../analysis/ableton-live-12.4.3/r2/h2-index-v1/out/live-arm64-index-strings.txt)).
  It also contains the database strings `Database is at version`,
  `database corrupted; must be` and `ableton database schema vr. 1.0`.

**Inferred.**

- Live starts the helper as a child process in controlled mode and writes its
  options file.
- The two processes exchange JSON-encoded named events over a nanomsg IPC socket.
- The helper writes the browser database. Live also opens it, as the "secondary
  instance" named in `Could not repair corrupted database in secondary instance`
  (`0x10023a384`).

**Unknown.** The spawn site, the argv, the option values, the socket directory,
the restart policy and the payload schemas beyond the key names.

## What is indexed

**Observed.**

- Library configuration keys (`0x100153650` reads them and `0x100131a44` writes
  them for `Library.cfg`): `builtin-folders`, `factory-packs`, `user-library`,
  `user-folders`, `current-project`, `managed-folders`,
  `places-only-managed-folders`, `legacy-packs`, `cloud-manager-folder` and
  `abl-factory-library`.
- The `places` table has `folder_kind`. A temporary view maps synthetic roots to
  kinds: `<plugins>` 10, unavailable places 13, `<keywords>` 14 and `<packs>` 15.
- The file-type registry at `0x10029bb10` (`FileTypes.cpp`) has 80
  registrations. Each has a four-character code, a description, extensions and a
  macOS type. They are recovered in
  [file-type-registry.tsv](../../analysis/ableton-live-12.4.3/r2/h2-index-v1/out/file-type-registry.tsv).
  The registrations cover the following:
  - Live documents: `.als`, `.alc`, `.adv`, `.adg`, `.agr`, `.amxd`, `.alp`,
    `.ablbundle` and `.ablpresetbundle`;
  - audio: `.wav`, `.aif`/`.aiff`, `.flac`, `.mp3`, `.m4a`, `.ogg`, `.wv`, `.bwf`
    and `.rf64`;
  - REX: `.rex`, `.rcy` and `.rx2`;
  - MIDI: `.mid` and `.midi`;
  - plugin presets: `.fxp`, `.fxb`, `.aupreset` and `.vstpreset`;
  - tunings: `.ascl` and `.scl`;
  - images, video, `.xmp`, `.asd`, and the folder kinds `fldr`, `pfld`, `dfld`,
    `lfld`, `back` and `tmpl`.
- The `files.file_kind` bitmask names are decoded at `0x10016b3e8`, bit 0 first:
  `others`, `clips`, `other-audio`, `groove`, `max-patches`, `live-presets`,
  `video`, `rex-files`, `device-folders`, `other-folders`, `images`,
  `restricted-encoded-audio`, `restricted-direct-show-audio`,
  `restricted-direct-show-m4a-audio`, `plugin-presets` and `plugins`.
  Named sets include `browser-default` = `0x7CFF`, `audio` = `0x38C4`,
  `all-folders` = `0x300` and `all` = `0xFFFF`.
- Plugins are indexed as files of type `plug`, together with tables
  `plugin_modules`, `plugin_domains` and `plugins` (`0x100c59742`).

**Inferred.** The registry is shared product code (`products/live/Live/CreamOs`),
so registration does not prove that every type is indexed or shown. The
`file_kind` sets look like the browser's content filters.

**Unknown.** The mapping from type to kind (`TFileDatabase::MapFileTypeToFileKind`
is only referenced) and the set of visible kinds per browser view.

## What is extracted and stored

**Observed.**

- Metadata key vocabulary (`0x10016f458`):
  - sample origin: `abl-factory-sample`, `abl-imported-sample` and
    `abl-recording-sample`;
  - descriptive: `album`, `annotation`, `artist`, `author`, `genre` and `year`;
  - keywords: `keyword`, `user-keyword`, `auto-keyword`, `implicit-keyword` and
    `keyword-hide-flag`;
  - devices: `device-id`, `cont-device-id`, `device-name`, `device-path`,
    `device-type`, `device-folder` and `device-folder-equivalent`;
  - packs: `pack-unique-id`, `pack-version`, `pack-display-name`,
    `pack-download-url`, `pack-download-size` and `pack-installation-size`;
  - content: `content-hash`, `content-source`, `asset-id`, `cloud-hash-id` and
    `cloud-song-id`;
  - folder flags: `folder-hidden-in-browse`, `is-protected-folder` and
    `is-templates-folder`;
  - XMP links: `xmp-file-id` and `xmp-file-type`;
  - others, including the `patch-*` and `source-*` keys and `limitations`.
- A migration maps text keys to four-character codes such as `albm`, `arts`,
  `genr`, `UKey` and `AKey`.
- `files` holds per-file `mod_date`, `file_size`, `colors`, `use_count`,
  `scanner_version`, `md_version`, `device_type/arch/id`, `edit_source`,
  `edit_date`, `fe_version` and `flags`.
- The index binary contains a full Live document reader. Function `0x1004ca3b4`
  references 203 class names (`InstrumentSimpler`, `DrumGroupDevice`, `FileRef`
  and others). It also has its own schema-version checks
  (`Unsupported MajorVersion (`, `Live: Finding schema file failed:`).
- Sound similarity:
  - `fe_values(file_id, data BLOB, hash)` and `fe_values_record`;
  - the options `sound-analyzer` and `auto-keywords`;
  - feature-file checks at `0x10017e380`, for example `Sound similarity feature
    file is outdated` and `SoundAnalyzerVersion`;
  - `Ableton Pack: Binding Sound Similarity Features to Database for:`.

**Inferred.**

- The helper parses Live documents to extract the devices used and the referenced
  samples. This is suggested by the `ReferencedSamples` key, the `file_devices`
  table and the document classes.
- Packs ship precomputed similarity features as `Features.json`, which is present
  in Core Library `Ableton Folder Info`.

**Unknown.**

- Which audio properties, if any, are extracted (no sample-rate or duration
  metadata key exists).
- The feature algorithm and its model inputs.
- What `auto-keywords` produces.

## Index storage and versioning

**Observed.**

- File name format `{}-files-{}.db` (`0x100c5e123`, built in `0x10073559c`).
- `TFileDatabase` vtable at `0x100d92710`, recovered from constructor
  `0x100265ac4` and confirmed by typeinfo `0x100d93278` at vtable−8 (raw-file
  decode in `out/tfiledatabase-vtable.tsv`). Slot +0x30 resolves through a thunk
  to `0x100735594`, which returns `0x300c` (12300).
- The version check `0x10023344c` compares `version` and `platform` from table
  `version` with that value and with platform 2. The outcomes are:
  - equal: open;
  - stored lower: upgrade through a translator, then `ANALYZE`;
  - stored higher, other platform, or no table: `Need to recreate`.
- 64 `SDatabaseVersionTranslators` lambda type names exist (`E_`, then `E0_` to
  `E62_`; strings from `0x100bab634`), each a `std::function` taking a
  `TFileDatabase*`.
- Files whose names start with `{}-files-` are scanned and the version after the
  last `-` is parsed (`0x10023af84`). A selected older file is copied through
  `temp.db` (`0x10023b614`). The selection rule was not traced.
- The current schema is one string at `0x100c274f0`, created by `0x100266b70`
  through vtable slot +0x48. Its tables are `files`, `ancestors`, `metadata`,
  `metadata_values`, `places`, `vfolders`, `vfolder_patterns`, `keywords`,
  `fe_values`, `fe_values_record`, `devices` and `file_devices`, plus a virtual
  `search_aggregation USING fts4 (sys, tags, tokenize=AbletonTokenizer,
  prefix="2,4,6")`.
- 386 application SQL strings are inventoried in
  [sql-strings.jsonl](../../analysis/ableton-live-12.4.3/r2/h2-index-v1/out/sql-strings.jsonl),
  with per-table columns in `sql-summary.json`.
- Pragmas: `page_size = 4096`, journal mode PERSIST, DELETE, WAL or OFF,
  configurable `synchronous`, and a schema dump format
  `ableton database schema vr. 1.0`.

**Inferred.**

- The on-disk file is `<db-path dir>/<prefix>-files-12300.db`. The prefix is
  probably the product name supplied by Live.
- The index is a rebuildable cache. A version or platform mismatch discards it
  rather than failing.
- Data that lives only in the database is lost on recreate. That would include
  use counts and colors, unless re-imported.

**Unknown.**

- The actual prefix and directory, and whether 12300 is the value written for
  12.4.3. This is probe PRB-H2-02.
- The semantics of the tokenizer.

## Incremental update and rescan

**Observed.**

- Scan reasons logged:
  - `Live` (with an Event ID and an all-folders flag);
  - `OS Events, Folders:`;
  - `Explicit, All Folders?: true`;
  - `Reenabled auto-update`.
- The work queue runs change detection, then extraction, then updating, then XMP
  import, then removal. Cleanup and `GarbageCollectAggregatedData` follow
  (`0x100140bac`, `0x100140680`, `DoSomeWork` and `WorkOn*`).
- macOS file-event streams are set up per directory. The log includes
  `OsEvents: Volume mounted/unmounted` and `OsEvents: Path has gone`.
- `Folders to be scanned fully, since they don't support OSEvents:`
  (`0x100c1ca96`) and `Unavailable folders:` are logged.
- Per-file queries read `mod_date`, `file_size` and `name`. Folder queries also
  read the `mod_date` of the folder's `Ableton Folder Info/Properties.cfg`
  (`0x100c350b1`). Their use for change detection is inferred.
- Each file has `scanner_version`. A migration resets it to 0 for `als-`, `alc-`,
  `agr-`, `adv-` and `adg-` files that have no metadata, which forces
  re-extraction. Plugins get the same reset (`file_type = str2fourcc('plug')`).

**Inferred.** Updates are incremental through file-system events where the volume
supports them, and full scans elsewhere. Extraction reruns when the extractor
version changes.

**Unknown.** Debounce timing, ordering guarantees, what `db-stale-factor` and the
dead-file statistics govern, and when Live requests a scan.

## Missing, moved, corrupt and unsupported files

**Observed.**

- `Index: Observed File is gone:`.
- Deletion of a file row together with its descendants
  (`DELETE FROM files WHERE file_id IN (SELECT :fileid UNION … ancestors …)`).
- Unavailable places are kept in `unavail_places`. The commands
  `UpdateUnavailablePacks` and `RelocateFolder` and the `RebindSafeUserData` path
  exist.
- Database corruption is detected and an indicator file is written
  (`0x1002301ac`). The message `Failed to write corrupted database indicator file.
  Database will not be rebuilt on next start-up.` exists. The
  load path attempts to delete both the indicator and the database file; its
  failure messages are `Could not delete corrupted database indicator` and `Could
  not delete corrupted database file` (`0x10023a970`).
- The text identifiers `sErrorDatabaseCorrupt`, `sErrorCorruptedDatabaseInfo` and
  `sErrorCantCreateIndex` exist.
- Document and audio errors: `corrupt_document`, `audio_decoding_failed`,
  `Error reading xmp file:` and `Importing XMP from builtin content at least
  partially failed:`.

**Inferred.** A corrupt index is rebuilt on the next start. Vanished files are
removed from the index rather than shown as missing.

**Unknown.** User-visible messages and their timing, whether tags or colors
survive a move, and how unsupported or undecodable files appear in the browser.

## Persisted browser metadata outside the database

**Observed in shipped content** ([shipped-inventory.json](../../analysis/ableton-live-12.4.3/r2/h2-index-v1/out/shipped-inventory.json)):

- There are 179 `Ableton Folder Info` directories, 94 under Builtin and 85 under
  Core Library. They hold:
  - 2,563 `.ogg` previews and 2,563 `.asd` companions;
  - 176 `Properties.cfg`, one each of `Metadata.cfg`, `VirtualFolders.cfg`,
    `FallbackLocations.cfg` and `FirstTimeStart.cfg`;
  - 162 `.xmp` and 20 `.amxd`;
  - four JSON files, including `Features.json`.
- Every preview sits at `Ableton Folder Info/Previews/<item path>.ogg`. The item
  exists at `<item path>` in the folder that contains `Ableton Folder Info` in
  2,563 of 2,563 cases.
- `Properties.cfg` is text with an `Ableton#04I` or `Ableton#05I` header (2 with a
  UTF-8 BOM) and one `FolderConfigData { Type Name = value; }` block. Observed
  fields:
  - `IsProtected`, `DeviceId`, `DeviceEquivalentId` and
    `FolderHiddenInBrowseGroups`;
  - `IsTemplatesFolder`, `IsBuiltinContentFolder` and `ContentKinds`;
  - pack identity fields (`PackUniqueID`, `PackDisplayName`, `PackVendor`,
    `PackMajorVersion`/`MinorVersion`/`Revision` and `MinSoftwareProductId`).
- `Metadata.cfg` is binary (`ab1e5678…`). `VirtualFolders.cfg` and
  `FallbackLocations.cfg` are `Ableton` XML documents.
- XMP tag sidecars, 162 files:
  - Format: an XMP packet with
    `ablFR = https://ns.ableton.com/xmp/fs-resources/1.0/`, `dc:format`,
    `ablFR:resource`, `ablFR:platform` (`mac` in all 162), optional
    `ablFR:packUniqueId`/`packVersion`, and `ablFR:items` (a Bag of
    `{ablFR:filePath, ablFR:keywords Bag}`). One file has `ablFR:hideKeywords`.
  - Names: every file name is a version-5 (name-based) UUID.
  - Resources: one `app-builtin` (Builtin), one Core Library pack and 160 packs
    under `Builtin/Legacy Pack Data`.
  - Items: 66,312 in total. Item paths resolve relative to the folder containing
    `Ableton Folder Info`: 84 of 85 in Builtin (the one miss is
    `Devices/Audio Effects/Auto Pan`, while the folder is `Auto Pan-Tremolo`),
    7,000 of 7,000 in Core Library, and 0 of 59,227 for legacy packs (not
    installed).
  - Keywords: `|`-separated paths of depth 2 (61,790) or 3 (42,060). The 10
    top-level segments are Drums, Sounds, Type, Character, Key, Genres, Clips,
    Devices, Grooves and Tunings.

**Observed in the helper.**

- The same vocabulary appears in the helper: resources `folder`, `pack`, `plugin`
  and `app-builtin`; `dc:format` values `application/vnd.ableton.folder`,
  `.factory-pack`, `.plugin-device` and `.app-builtin`; and fields `deviceId`,
  `contentHash`, `hideKeywords`, `packUniqueId`, `packVersion`, `filePath` and
  `items` (strings `0x100c5c4bb`–`0x100c5c6b2`).
- Sidecar names match `c55d131f-2661-5add-aece-29afb7099dfa([-_][a-zA-Z0-9-_]+)?.xmp`
  and the `b20da5c2-…` analogue (`0x1006e71c8`). The two base names are the
  shipped Core Library and Builtin sidecars. Boost's name-based UUID SHA-1 code is
  present.
- Writer messages: `Writing folder metadata done.`, `Writing factory pack metadata
  done.`, `Writing plugin metadata done.` and `No UserLibrary.  Can't write factory
  pack metadata`. Items pending export carry `flags | 32`.

**Inferred.**

- User tag edits are exported to XMP sidecars, so tags survive a database rebuild
  and travel with folders.
- Edits to factory-pack tags are written under the User Library, not into the
  pack.
- Legacy pack sidecars let tags apply when those packs are installed.

**Unknown.** The namespace and name used for the UUIDv5 file names (standard
namespaces with obvious names did not match), the exact target path for user
edits, and when the export runs. These are covered by PRB-H2-04.

## Shipped `filerefmap.db`

**Observed.**

- Schema:
  - `sample_mapping(src_type int, src_packid, src_ref, dst_type int, dst_packid
    nullable, dst_ref)`, with a unique key on the source triple;
  - `pack_names(packid, packname)`;
  - `meta_info(key, value)`, one row with key `build_revision` and a 5-character
    value;
  - `sqlite_stat1` and `sqlite_stat2`.
- Row counts: 37,617 / 81 / 1. `user_version` 0, page size 4096.
- Distributions:
  - source types: 2 has 35,610 rows and an empty pack id; 5 has 2,005; 7 has 2;
  - destination types: 5 has 37,583; 7 has 34, with an empty pack id;
  - pack ids: 9 distinct sources and 80 distinct destinations, 72 of them listed
    in `pack_names`;
  - references are all relative, mostly `.aif`, with `.wav` and 63 `.amxd`.
- The helper's own create statement (`0x100c4cde9`, in `0x1005284c4`) differs: it
  declares `dst_packid … NOT NULL`, an index named `sample_mapping_KEY`, a
  `pack_names` primary key and no `meta_info`. The helper only creates it when
  the file is missing and the open is not read-only. Controlled mode opens it
  read-only.
- Queries: `SELECT dst_type, dst_packid, dst_ref FROM sample_mapping WHERE
  src_type=… AND src_packid=… AND src_ref=…` and `SELECT packname FROM pack_names
  WHERE packid=…`.

**Inferred.**

- The table redirects sample references from older or legacy content locations to
  current pack locations.
- The type values plausibly reuse the document `FileRef` path-type enumeration.
  The shipped `Sample Reference.als` uses `RelativePathType` 5 in 5,358 FileRefs.
  This mapping is not established.

**Unknown.** Which component consults the map during document load, and what a
miss does. These are covered by PRB-H2-07.

## Candidate requirements for a future SPEC-BROWSER-INDEX

These are proposals for review. They describe externally observable files and
behavior, not the helper process. A reimplementation needs no helper process,
nanomsg channel or `files` database layout unless a compatibility decision
requires one.

| Candidate | Statement | Evidence | Status |
| --- | --- | --- | --- |
| BI-C01 | Read tag sidecars `Ableton Folder Info/*.xmp` in the `ablFR` format above. Item `filePath` is relative to the folder containing `Ableton Folder Info`, and keywords are `|`-separated hierarchical tags | 162 shipped files parse; 7,084 of 7,085 installed items resolve; helper vocabulary | Static; read side supportable |
| BI-C02 | Treat tags with the 10 shipped top-level categories as the factory tag tree; depths 2–3 occur | Shipped keyword statistics | Static; UI grouping unknown |
| BI-C03 | Show `Ableton Folder Info/Previews/<item>.ogg` as the preview of `<item>` | 2,563 of 2,563 correspondences; `Previews` string | Static convention; playback behavior unknown |
| BI-C04 | Apply `Properties.cfg` fields: `FolderHiddenInBrowseGroups` hides a folder from browse groups; `IsProtected`, `IsTemplatesFolder` and the device ids classify folders | 176 files; matching metadata keys and visibility-flag SQL | Inferred effects |
| BI-C05 | Recognize the 80 registered extensions with their type identities; default browser content excludes device and other folders (`0x7CFF`) | Registry and bitmask decode | Inferred; per-view visibility unknown |
| BI-C06 | Locations comprise built-in content, factory packs, the User Library, user folders, the current project, managed folders and legacy packs; places that cannot be reached are remembered as unavailable | Library.cfg keys; `unavail_places` | Static; UI unknown |
| BI-C07 | Additions, deletions and renames in indexed folders appear without restart. Volumes without file-event support are rescanned fully | OsEvents strings and task phases | Needs PRB-H2-03 |
| BI-C08 | User tag edits persist in XMP sidecars and survive index rebuilds | Export and writer strings | Needs PRB-H2-04 |
| BI-C09 | A corrupt or incompatible index is discarded and rebuilt; a corrupt one is rebuilt at the next start | Version outcomes, indicator strings | Needs PRB-H2-06 |
| BI-C10 | A reference matching a `filerefmap.db` source triple resolves to its destination | Schema and query | Needs PRB-H2-07 |
| BI-C11 | The index records per-file color and use count, settable from the UI | Columns and commands `SetColor(s)`, `IncreaseUseCount` | Persistence location unknown |
| BI-C12 | Search matches tags and system text with prefix indexing | FTS4 `(sys, tags)`, `prefix="2,4,6"` | Matching rules unknown |

## Live-side questions (main Live project)

1. Which code spawns `Ableton Index`, with which argv, when, and with what restart
   policy after `Process orphaned` or a crash?
2. Where does Live write the options file and `Library.cfg`? Which values does it
   use for `db-path`, `ipc-channel`, `usage-data_file` and the file-name prefix?
3. Which browser queries does Live run against the shared database: search over
   `search_aggregation`, tag filters, `file_kind` masks? How do `FinishedActivity`
   `NeedsRefresh` and `RefreshCategories` drive the UI?
4. Does Live itself read `filerefmap.db`, for example during document load? Which
   component uses `sample_mapping`?
5. Which user preferences map to `sound-analyzer`, `auto-keywords`,
   `os-events-flags` and `EnableAutoUpdate`?

These need cross-references to the strings listed in `out/live-arm64-index-strings.txt`,
resolved in the saved Live project.

## Phase 4 probe batch

[probe-batch.json](../../analysis/ableton-live-12.4.3/r2/h2-index-v1/probe-batch.json)
holds 9 records. Each lists the question, the existing evidence, why static
evidence is insufficient, the minimal input, the discriminating observation and
the stopping condition, under [ADR 0002](../decisions/adr-0002-static-first-analysis.md).

| ID | Question |
| --- | --- |
| PRB-H2-01 | Launch: argv and options-file keys |
| PRB-H2-02 | Database file name, directory and recorded version and platform |
| PRB-H2-03 | Add, rename and delete latency in a user folder |
| PRB-H2-04 | Where tag edits are persisted |
| PRB-H2-05 | Moved, deleted and unmounted files; tag and color retention |
| PRB-H2-06 | Corrupt, newer-version and foreign-platform database handling |
| PRB-H2-07 | Use of `filerefmap.db` when a set loads |
| PRB-H2-08 | When sound-similarity data is computed |
| PRB-H2-09 | Presentation of unsupported and corrupt media |

## Method notes and limits

- The completion signal was misleading. `decomp.time` is created by
  `/usr/bin/time -o` when the job starts, so its existence did not mean the job
  had finished. This packet waited for a non-empty `decomp.time` (exit 0, 3:27
  wall) before using the indexes.
- One read-only dossier run on four typeinfo addresses returned no incoming
  references. Ghidra recorded no data references to typeinfo here. The vtable was
  therefore located from a constructor and decoded from the raw slice with
  `read_ptrs.py`, which assumes plain or chained-rebase pointers. The decoded
  slots matched the expected typeinfo and the creation-path calls.
- The option and command tables were read from pseudocode, so argument order
  inside `FUN_` helpers is inferred.
- Shipped-file statistics count structure only. No tag lists or pack contents
  are reproduced beyond the 10 top-level category names and the single unresolved
  Builtin item.
