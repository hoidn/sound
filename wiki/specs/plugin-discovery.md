---
id: SPEC-PLUGIN-DISCOVERY
type: spec
status: draft
updated: 2026-10-18
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3 / macOS
---

# Plug-in discovery (VST3 and VST2)

## Scope

Feature FEAT-HOSTING in the [feature map](feature-map.md), discovery part only.
User task: install third-party plug-ins in the usual or a custom folder, let the
application find them, and see them listed as instruments or effects. Later scans
should reflect added, changed and removed plug-ins without re-examining everything.
This draft specifies:

- which folders are searched, and in what order;
- which bundles count as plug-in modules, and what each module contributes;
- how unchanged, changed, removed and failing modules are treated across scans;
- what Rescan and the modifier Rescan do.

Every clause is a **proposed contract**. Each is documented, supported by a static
derivation, or explicitly unknown. Nothing was run against Live.
[ADR 0002](../decisions/adr-0002-static-first-analysis.md) permits a static-first
draft. Target: 12.4.3 on macOS. The arm64 build was analyzed; the x86_64 build was
compared by strings only.

Excluded:

- Audio Unit discovery (unknown, REQ-001);
- plug-in instantiation, editors, parameters, state, latency and the device lifecycle;
- how Live Sets refer to plug-ins;
- the location and format of the application's private discovery cache and of its
  internal process interfaces;
- Windows.

## Evidence labels

| Label | Meaning |
| --- | --- |
| D | Documented in text shipped with the application |
| S | Static derivation from the 12.4.3 executables; not an observed run |
| U | Unknown; no expected result. PRB IDs name the Phase 4 probe that would settle it |

Only D and S clauses may enter a release. U clauses block the behavior they name.

Terms used below:

- A **folder** is a search root.
- A **module** is one bundle found under a folder.
- A **plug-in** is one listed entry contributed by a module.
- **Examining** a module means loading its executable to enumerate its plug-ins.
- **Listed** means the plug-in appears in the application's plug-in browser.
- A **scan** is one discovery run, from its start until all candidates are handled.

## Requirements

### REQ-PLUGIN-DISCOVERY-001 — formats and isolation

- **D.** Third-party plug-ins in VST and Audio Units (Mac only) formats complement
  the built-in devices. Plug-in support may have to be activated in the Plug-In
  Sources section of the Plug-Ins preferences.
- **S.** VST3 and VST2 modules are examined in a process separate from the
  application. A module that crashes while it is examined does not terminate the
  application.
- **S.** Bundles with the extension `.clap` are not discovered, in any folder.
- **U.** Where, when and how Audio Units (v2 and v3) are discovered and listed:
  PRB-H1-06.

### REQ-PLUGIN-DISCOVERY-002 — searched folders

- **S.** Each format has two independent source switches. One adds the format's
  pair of system folders; the other adds the custom folder.
- **S.** VST3 system folders, in this order: `~/Library/Audio/Plug-Ins/VST3`,
  then `/Library/Audio/Plug-Ins/VST3`.
- **S.** VST2 system folders, in this order: `~/Library/Audio/Plug-Ins/VST`, then
  `/Library/Audio/Plug-Ins/VST`. A VST2 system folder that does not exist
  contributes nothing.
- **S.** With its switch on and a custom folder set, the format's custom folder is
  searched after the system folders. If both switches of a format are off, no
  module of that format is examined.
- **U.** Which labelled control is which switch. Inferred labels: "Use VST3/VST2
  Plug-In System Folders" and "... Custom Folder". Also unknown: the defaults on
  first launch, and whether turning a switch off hides that source's plug-ins at
  once: PRB-H1-01, PRB-N4-01.
- **U.** A custom folder path that contains a comma. The derivation predicts that
  nothing is found there: PRB-N4-01.

### REQ-PLUGIN-DISCOVERY-003 — order of examination

- **S.** In a scan, all VST3 candidates are handled before any VST2 candidate.
- **S.** VST2 handling does not depend on the outcome of the VST3 part.
- **U.** The order within a format, both between folders and within one folder.
  The derivation gives no defined order. Implementations are not graded on it.

### REQ-PLUGIN-DISCOVERY-004 — VST3 candidates

- **S.** Under each VST3 folder, at any depth, every entry whose name ends in
  `.vst3` is a candidate. The match is exact and case-sensitive: `X.VST3` is not
  a candidate. Directories and plain files both qualify.
- **S.** A candidate is not searched inside, so a `.vst3` nested in another
  `.vst3` is not a candidate.
- **S.** Within one folder, a directory reached twice (same resolved location) is
  searched once. Paths that resolve to the same location count as one candidate.
- **U.** Whether symbolic links to directories are followed, and whether an
  unreadable subfolder ends the search of the rest of that folder. No probe has
  been filed; propose adding both to the PRB-H1-08 session.

### REQ-PLUGIN-DISCOVERY-005 — VST2 candidates

- **S.** Under each VST2 folder, folders are searched level by level:
  - a directory whose name ends in `.vst`, in any letter case (`.vst`, `.VST`), is
    a candidate and is not searched inside;
  - every other directory is searched, including one named `*.vst3`;
  - plain files are ignored, even ones named `*.vst`.
- **S.** Each resolved folder is searched once. A folder that cannot be read is
  skipped, and the search continues with the remaining folders.
- **U.** Whether the folder structure below a VST2 folder is presented to the user.
  Inferred: it feeds folder-structured browsing. No probe has been filed.

### REQ-PLUGIN-DISCOVERY-006 — what a VST3 module contributes

- **S.** The module is examined. Each factory class with category exactly
  `Audio Module Class` becomes one listed plug-in. Other classes, such as
  controller classes, are not listed.
- **S.** A module that loads but has no such class contributes no plug-in.
- **S.** A module that cannot be loaded, or that has no plug-in factory, contributes
  no plug-in.
- **S.** Neither of these two kinds of module is examined again until REQ-008 or
  REQ-010 applies.
- **S.** A plug-in is an instrument when one of its subcategory entries is exactly
  `Instrument` (case-sensitive, any position in the `|`-separated list). Otherwise
  it is an effect.
- **D.** Instrument plug-ins are distinguished in the browser by piano keys in the
  lower half of their icon.
- **U.** Whether VST3 code signatures are checked. None was found.

### REQ-PLUGIN-DISCOVERY-007 — what a VST2 module contributes

- **S.** Before loading, the bundle's code signature is validated across all
  architectures and nested code:
  - an unsigned bundle is examined;
  - a bundle whose signature is present but invalid is not loaded and contributes
    no plug-in.
- **S.** The entry point `main_macho` is used if present, otherwise
  `VSTPluginMain`. A bundle with neither contributes no plug-in.
- **S.** Every plug-in the module reports is listed, including each sub-plug-in of a
  shell plug-in.
- **S.** While the module is examined, the host answers these requests:
  - version: 2400;
  - vendor string: `Ableton`;
  - product string: `Live`;
  - can-do `shellCategory`: non-zero; every other can-do string: 0;
  - current shell ID: the ID of the sub-plug-in being enumerated;
  - any request other than these, vendor version and language: 0.
- **U.** The vendor-version and language values. Also how a VST2 plug-in is
  classified as an instrument; inferred: from the plug-in's synth flag.

### REQ-PLUGIN-DISCOVERY-008 — persistence and change detection

- **S.** Discovery results persist across scans and application restarts.
- **S.** A module whose examination completed is not examined again while two
  properties of its main executable are unchanged: its size, and its modification
  time in whole seconds. The main executable is the one the bundle's Info.plist
  names.
- **S.** Changing other bundle files (Info.plist without renaming the executable,
  resources) or the bundle directory's own timestamp does not cause a new
  examination.
- **S.** A change in either property causes one new examination at the next scan.
  The module's previous plug-ins are replaced by the result: a removed class is no
  longer listed and an added class is listed.
- **U.** Confirmation of the above, and a change within the same second:
  PRB-H1-05.

### REQ-PLUGIN-DISCOVERY-009 — removed modules and unavailable folders

- **S.** A module no longer found under its folder at the next scan is forgotten,
  and its plug-ins are no longer listed.
- **S.** The same applies to every module of a searched folder that is missing or
  unreadable when the scan runs, for example a custom folder on an unmounted
  volume. When the folder returns, its modules are examined again as new.
- **U.** How plug-ins of a source whose switch was turned off are treated
  (REQ-002), and the effect on sets that use a forgotten plug-in.

### REQ-PLUGIN-DISCOVERY-010 — Rescan and reset rescan

- **S.** Rescan in the Plug-Ins preferences starts a scan. That scan examines only
  modules that are new, changed (REQ-008), or whose earlier examination did not
  complete.
- **S.** A Rescan requested while a scan is running is ignored, including its reset
  variant.
- **S.** Rescan with a modifier key held starts a reset scan. Before searching, all
  stored discovery results for the folders being searched are discarded, for both
  formats. Every module found is then examined, whatever its earlier outcome.
  Results for folders not being searched are kept.
- **U.** Which modifier key (inferred: Option), and whether the control's label
  changes while the key is held: PRB-N4-01. When scans start without Rescan, for
  example at application start or on a switch or custom-folder change:
  PRB-H1-01, PRB-N4-01.

### REQ-PLUGIN-DISCOVERY-011 — progress and scan states

- **S (content).** During a scan, the application has the following progress
  information for the format being handled:
  - the number of candidates found;
  - the number handled so far, counting skipped unchanged modules;
  - the name of the module being examined, prefixed by its format, such as
    `VST3: Name`.

  A scan ends either complete or interrupted.
- **U.** Where and how the user sees this: status text, any animation of the
  Rescan control, the end state. No probe has been filed; propose a screen capture
  during PRB-H1-04.

### REQ-PLUGIN-DISCOVERY-012 — crashing module

- **U.** PRB-H1-02 and PRB-N4-02, then PRB-H1-05. Only REQ-001's survival clause
  applies until those run.
- The static derivation, which is not a requirement:
  - the application relaunches discovery without user action and without a retry
    limit;
  - the crashing module contributes no plug-in;
  - it is not examined again until REQ-008 or REQ-010 applies;
  - all other modules are discovered normally.

  If the derivation is wrong, discovery could crash repeatedly.

### REQ-PLUGIN-DISCOVERY-013 — hanging module

- **U.** No time limit on examining a module was found, so a module that never
  returns may stall discovery indefinitely. Settled by PRB-H1-03 and PRB-N4-05.

### REQ-PLUGIN-DISCOVERY-014 — many new modules

- **U.** Whether one scan with more than 50 new modules lists all of them without
  further user action. Settled by PRB-H1-04 and PRB-N4-02.
- The derivation splits discovery into batches of at most 51 newly examined modules
  per format, restarted automatically. Batching is not a requirement.

### REQ-PLUGIN-DISCOVERY-015 — duplicates

- **U.** Two cases are unresolved: the same bundle present in two folders, and two
  modules declaring the same plug-in class ID. Unknown: whether each appears once or
  twice, and which one is used. Settled by PRB-H1-08.

### REQ-PLUGIN-DISCOVERY-016 — quitting during a scan

- **S.** If the application quits during a scan, discovery does not run to
  completion.
- **S.** At the next scan, modules whose examination completed before the quit are
  not examined again, and the remaining ones are examined.
- **U.** How long examination continues after the quit. No probe has been filed.

## Timing and state

- **Units.** The only time quantity is the modification time used by REQ-008, in
  whole seconds.
- **Ordering.** VST3 before VST2 (REQ-003). Order within a format is undefined and
  not compared.
- **Persistent state.** For each module of each searched folder: whether its
  examination completed and with what result, the executable size and modification
  time at that examination, and its plug-ins.
- **Out of scope.** Undo does not apply. The cache location (PRB-H1-07) and format
  are out of scope.
- **Cancellation.** No user control to cancel a scan was found. A repeated Rescan is
  ignored (REQ-010). Teardown is REQ-016.
- **Nondeterminism.** Which module is in progress when the application quits.
  Batch boundaries (REQ-014, U).
- **Interactions.**
  - The plug-in browser list (FEAT-UI) consumes the results.
  - Instantiating a listed plug-in is FEAT-HOSTING lifecycle, not specified here.
  - Live Sets that reference missing plug-ins belong to FEAT-PERSISTENCE.

## Acceptance cases

**Fixtures.**

- **V3(name).** A VST3 bundle `<name>.vst3` built from the public VST3 SDK, with
  executable `Contents/MacOS/<name>`. It has one processor class (category
  `Audio Module Class`, subcategories `Fx`) and its controller class. Class IDs
  are unique per bundle. A load-time initializer appends `<name>` to a fixed load
  log, so every load is counted.
- **V2(name).** A VST2 bundle `<name>.vst` (directory with Info.plist and
  `Contents/MacOS/<name>`). It exports `VSTPluginMain`, is an effect, is unsigned,
  and has the same load log.
- **V2Q.** A V2 that also writes the host's answers to its version, vendor,
  product, can-do (`shellCategory`, `sendVstEvents`) and sample-rate requests.
- **Clean start.** No previous discovery results (for the reference, a new macOS
  user or its cache removed; location: PRB-H1-07). All plug-in folders are empty
  except as stated. VST3 and VST2 system switches are on, custom switches off,
  unless stated. The load log is cleared before the measured action.

"Rescan" means the preference action; "reset rescan" is REQ-010's modifier variant.
Expectations are static derivations or documented; none has been run.

Case kinds:

| Kind | Meaning |
| --- | --- |
| P | Positive |
| N | Negative |
| B | Boundary |
| M | Malformed |
| T | Teardown |
| C | Cancellation |
| U | Unresolved; not graded |

| Case ID | Requirement | Kind | Setup/action | Expected result/comparator | Fixture |
| --- | --- | --- | --- | --- | --- |
| PD-001 | 002, 006 | P | Clean start; `~/Library/Audio/Plug-Ins/VST3/A.vst3`, `/Library/Audio/Plug-Ins/VST3/B.vst3`; Rescan | A and B listed as effects; log A once, B once | V3 |
| PD-002 | 002 | N | As PD-001 with both VST3 switches off; Rescan | A, B not loaded and not listed | V3 |
| PD-003 | 002 | P | Clean start, VST3 system off, custom on at `/Users/Shared/PDC` holding `C.vst3`, plus A as in PD-001; Rescan | C listed; A not loaded | V3 |
| PD-004 | 002 | U | Custom folder `/Users/Shared/pd,c` holding `C.vst3`; Rescan | Unresolved (derivation: C not found) | V3 |
| PD-005 | 002 | P | `~/Library/Audio/Plug-Ins/VST/D.vst`, `/Library/Audio/Plug-Ins/VST/E.vst`; Rescan | D and E listed | V2 |
| PD-006 | 002 | B | `~/Library/Audio/Plug-Ins/VST` absent; `/Library/Audio/Plug-Ins/VST/E.vst`; Rescan | E listed; scan completes | V2 |
| PD-007 | 003 | P | Clean start; A as in PD-001 and D as in PD-005; Rescan | Log has A before D | V3, V2 |
| PD-008 | 004 | P | `~/Library/Audio/Plug-Ins/VST3/Vendor/Sub/F.vst3`; Rescan | F listed | V3 |
| PD-009 | 004 | N | `~/Library/Audio/Plug-Ins/VST3/G.VST3` (valid bundle); Rescan | G not loaded, not listed | V3 |
| PD-010 | 004 | B | `H.vst3` in the user VST3 folder with a valid `I.vst3` inside `H.vst3/Contents/Resources/`; Rescan | H listed; I not loaded | V3 |
| PD-011 | 004 | M | Empty plain file `~/Library/Audio/Plug-Ins/VST3/J.vst3`, plus A; Rescan | J not listed; A listed; scan completes | V3 |
| PD-012 | 005 | P | `~/Library/Audio/Plug-Ins/VST/Vendor/K.vst`; Rescan | K listed | V2 |
| PD-013 | 005 | B | `~/Library/Audio/Plug-Ins/VST/L.VST` (valid bundle); Rescan | L listed | V2 |
| PD-014 | 005 | M | Plain file `~/Library/Audio/Plug-Ins/VST/M.vst`; Rescan | M not loaded, not listed | none |
| PD-015 | 005 | B | `N.vst3` (valid VST3) placed only in `~/Library/Audio/Plug-Ins/VST`; Rescan | N not loaded, not listed | V3 |
| PD-016 | 005 | B | `~/Library/Audio/Plug-Ins/VST/Locked/` (mode 000) and `.../VST/Open/O.vst`; Rescan | O listed; scan completes | V2 |
| PD-017 | 006 | P | `P.vst3` with two processor classes, subcategories `Instrument\|Synth` and `Fx\|Delay`, plus controllers; Rescan | Exactly two plug-ins from P; the first shown as instrument (piano-key icon), the second as effect | V3 variant |
| PD-018 | 006 | B | `Q.vst3` with processor subcategories `Fx\|Instrument`; `R.vst3` with `instrument`; Rescan | Q instrument; R effect | V3 variant |
| PD-019 | 006 | M | `S.vst3` whose executable exports no plug-in factory; Rescan, then Rescan again | Not listed; log S exactly once over both scans | V3 variant |
| PD-020 | 006 | B | `T.vst3` with only a controller class; Rescan twice | No plug-in from T; log T once | V3 variant |
| PD-021 | 007 | P | `U.vst` unsigned in the user VST folder; Rescan | U listed | V2 |
| PD-022 | 007 | P | `V.vst` ad-hoc signed (`codesign -s -`), unmodified; Rescan | V listed | V2 |
| PD-023 | 007 | N | `W.vst` ad-hoc signed, then one byte of its executable changed; Rescan | W not loaded, not listed | V2 |
| PD-024 | 007 | P | `X.vst` shell plug-in reporting three sub-plug-ins; Rescan | Three plug-ins from X listed | V2 shell variant |
| PD-025 | 007 | P | `Y.vst` in the user VST folder; Rescan | Recorded: version 2400; vendor `Ableton`; product `Live`; `shellCategory` non-zero; `sendVstEvents` 0; sample rate 0 | V2Q |
| PD-026 | 007 | B | `Z1.vst` exporting only `main_macho`; `Z2.vst` exporting neither entry point; Rescan | Z1 listed; Z2 not listed | V2 variants |
| PD-027 | 008 | P | After PD-001, Rescan; then quit, relaunch, Rescan | No load-log entries; A and B still listed | V3 |
| PD-028 | 008 | P | After PD-001, `touch A.vst3/Contents/MacOS/A`; Rescan | Log A once; A listed | V3 |
| PD-029 | 008 | N | After PD-001, `touch` A's `Contents/Info.plist` and the `A.vst3` directory; Rescan | No load | V3 |
| PD-030 | 008 | P | After PD-001, replace A's executable with a build adding a second processor class; Rescan; then with a build lacking the original class; Rescan | After the first: both classes listed. After the second: original class not listed | V3 variants |
| PD-031 | 009 | P | After PD-001, delete `B.vst3`; Rescan | B not listed | V3 |
| PD-032 | 009 | B | Custom folder as in PD-003; rename the folder away; Rescan; rename back; Rescan | After the first: C not listed. After the second: log C once; C listed | V3 |
| PD-033 | 010 | P | After PD-019 and PD-027; reset rescan | Every module in the searched folders loaded once, including S; listing as before | V3 |
| PD-034 | 010 | C | Clean start; 30 V3 variants each sleeping 1 s on load; Rescan; click Rescan again after 5 s | Each module loaded exactly once; no second scan | V3 variant |
| PD-035 | 011 | U | During PD-034, record what the user sees | Unresolved; record text and location | as PD-034 |
| PD-036 | 001 | N | `K1.vst3` whose factory calls `abort()`, plus A; Rescan | The application keeps running | V3 variant |
| PD-037 | 012 | U | Continue PD-036; Rescan twice more | Unresolved (derivation: A listed; K1 loaded once in total, never listed) | V3 variant |
| PD-038 | 013 | U | `H1.vst3` whose factory blocks forever; Rescan; wait 15 min | Unresolved | V3 variant |
| PD-039 | 014 | U | Clean start; 60 distinct V3 bundles; one Rescan | Unresolved (derivation: all 60 listed without further action) | V3 |
| PD-040 | 015 | U | A copied into both VST3 system folders; separately, two bundles with the same class ID; Rescan | Unresolved | V3 |
| PD-041 | 001 | N | A valid `.clap` bundle in `~/Library/Audio/Plug-Ins/CLAP` and in the user VST3 folder; Rescan | Not listed | CLAP sample |
| PD-042 | 016 | T | Clean start; the 30 sleeping V3 variants of PD-034; quit the application 10 s into the scan; relaunch; Rescan | Modules logged before the quit are not logged again; each other module logged once | V3 variant |

Comparators:

- "Listed" means the plug-in name appears in the plug-in browser after the scan
  ends.
- Load counts come from the fixtures' load log, compared exactly.
- Instrument versus effect is judged by the browser icon (REQ-006 D clause).

Cases marked U must not be graded. Malformed coverage is the M cases: broken
bundles, files posing as bundles and invalid signatures. Cancellation is limited to
the ignored repeat Rescan (PD-034), because no cancel control is known.

## Open questions

[Q-016](../questions.md#q-016-plug-in-discovery-live-side-contract) holds the open
items:

- Audio Unit discovery;
- scan triggers and source-switch effects;
- the crash, hang and batch behavior (REQ-012 to 014);
- duplicates;
- the presentation of progress;
- VST2 classification, vendor version and language;
- symbolic links and unreadable subfolders in VST3 folders.

The probes are in the
[H1 probe batch](../../analysis/ableton-live-12.4.3/r2/h1-plugin-scanner-v1/probe-batch.json)
(PRB-H1-01–08) and in [helper launch](../research/helper-launch-live-side.md#phase-4-probe-records)
(PRB-N4-01, 02, 05). Both are merged into the
[Phase 4 batch](../research/phase4-probe-batch.md). The REQ-004, 005, 011 and 016
unknowns have no probe yet; additions are proposed in those requirements.

## Analyst evidence appendix

Analysis-only. Do not copy into a handoff. The canonical evidence is in
[plug-in scanner](../research/plugin-scanner-static.md) and
[helper launch, Live side](../research/helper-launch-live-side.md#plug-in-scanner).

**Retained runs.**

- `analysis/ableton-live-12.4.3/r2/h1-plugin-scanner-v1/`. Scanner arm64 slice
  SHA-256 `6ce847b0…a97ad6`; "pc" below means its `pseudocode/<entry>.c`.
- `analysis/ableton-live-12.4.3/r2/n4-helper-contracts-v1/`. Live arm64 SHA-256
  `3a99ceea…383cfad`. Result `n4-0001` and `corpus-code/`.

**Reading this pass.** Every S clause was rechecked by reading the cited
pseudocode. No query-server rounds were used. Four functions were read for the
first time from the C1 corpora, which are not retained in the repository:

| Function | Corpus chunk | Code SHA-256 |
| --- | --- | --- |
| Live `0x1030ad96c` | `chunk-02343` | `8d034202…` |
| Live `0x1030adbbc` | `chunk-02343` | `95d65a93…` |
| Live `0x10317ad9c` | `chunk-02395` | `cd20f10a…` |
| Scanner `0x1006ad5c8` → `0x1006b4f14`, `0x100679138` | helper corpus | — |

| Requirement | Evidence | Strength |
| --- | --- | --- |
| 001 | Lessons `1-Live Basics Category/4-Playing Software Instruments Lessons/LessonsEN.txt` lines 113, 116 (SHA-256 `0834f8fc…`, via `app-resources.json`); separate executable launched by Live `0x103179e68` (n4-0001); module loading for discovery is in that executable (pc `0x100146ae4`, `0x100145d24`); C2 strings index: no string containing `.clap` in Live arm64, no CLAP option in the scanner (`options.json`) | D; S; CLAP by static absence |
| 002 | VST3 `0x1031c0f28` (`user` = home + `Library/Audio/Plug-Ins/VST3` at `0x105be7c71`, `local` = `/Library/Audio/Plug-Ins/VST3` at `0x105be7c92`), custom `0x1031c0144` (non-empty only), switches `0x1031c0d2c`; VST2 `0x1031b8e5c`: `0x1030ad96c` selector 2 → `FSFindFolder(kUserDomain 0xffff8005, 'aplg')`, 3 → `kLocalDomain 0xffff8003`, + `VST`, empty path unless the existence check `0x103e970a4` passes (new this pass); switches `0x1031b8c68`; preference keys `Vst3UseSystemFolders` etc. at slice offset `0x5ab40ad`; label string `Use VST2 Plug-In System Folders` at `0x105b02974` (single reference `0x100782730`, role unknown); comma split pc `0x1001332fc` vs Live join (n4-0001) | S; switch-to-label mapping inferred |
| 003 | pc `0x1001308e0` (VST3 driver, then VST2 driver regardless of VST3 result); per-format candidate map ordered by folder ID, per-folder hash set (pc `0x1005e9fd8`) | S; within-format order U (map comparator unread; would give `custom`, `local`, `user`) |
| 004 | pc `0x1005e8cb4`: recursive iterator option 5, visited set of canonical directories, extension compare `0x100679138` (component-wise `memcmp`) against `.vst3`, recursion disabled on a match | S; option 5 and status-type 3 semantics (boost-like?) unresolved |
| 005 | pc `0x1005aad10`: FIFO queue, visited set, `FUN_1006ad5c8` lowercases the extension (`0x1006b4f14` is a Unicode lower-case map) before the 4-byte `.vst` compare, files ignored, folder error logs `Failed to scan folder` and continues the queue | S (case-insensitivity new this pass) |
| 006 | pc `0x1005e91fc` (`Audio Module Class` compare, length 0x12; reject state 3; confirm), `0x100145768` (exact 10-byte `Instrument` token), skip rule pc `0x1005e9fd8` (equal fingerprint and stored state ≠ 0); lessons line 118 | S; D |
| 007 | pc `0x100145d24`, `0x10075325c` (flags 9, `-67062` = unsigned accepted), entry points `main_macho` → `VSTPluginMain`; host callback pc `0x100140cb8` (opcode 1 → 0x960, 32 `Ableton`, 33 `Live`, 37 `shellCategory` → 10, 2 shell ID, 34 vendor version, 38 language, default 0) | S; synth flag inferred |
| 008 | Fingerprint `0x1001458a4` (`CFBundleCopyExecutableURL`, size and seconds mtime); skip pc `0x1005e9fd8`; Rescan branch `0x1005a55c8` deletes the module's plug-in rows (Retry branch keeps them), sets new fingerprint and state 0 | S; probe PRB-H1-05 |
| 009 | pc `0x1005e9fd8` (stored path not a candidate → `RemoveModules` `0x1005a9534`); empty or failed enumeration gives zero candidates; Live adds custom without an existence check (`0x1031c0144`) | S |
| 010 | `OnRescanPlugins` `0x10035e3fc` and identical `0x100345b2c` → `0x10316a4c0` (the only direct callers) with reset = modifier mask bit value 2 (`0x1012946e8`, `0x101294398`); busy check `0x103179994`; `--reset all` only (n4-0001 `0x10317a6dc`); `ResetScanData` `0x1005a87f0` per passed domain plus orphans; reset flag cleared before relaunch (`0x10317bcf0`) | S; key identity and other triggers U |
| 011 | `update` and `current-plugin` builders pc `0x10013e06c`, `0x10013e284`, `0x100138588`; Live stores name/current/total `0x10317ad9c` and notifies a listener only; `scan` = `done` or `interrupted` (pc `0x1001308e0`); UI strings `mpRescanAnim`, `mpRescanState` | S content; presentation U |
| 012 | `0x1005a8258`; Live died branch `0x10317bcf0` without a counter | U (see contradiction) |
| 013 | No timeout in the scan path; observer table (helper launch page) has no connected-state timeout | U |
| 014 | Run state pc `0x100138504` (2 when limit < count), count `0x100138578` incremented only after a confirmed module, per-format adapter (`0x100133aa0`, `0x100134018`) | U |
| 015 | Per-folder canonical dedup only; `AddModuleCandidate` keyed by path and folder | U |
| 016 | Run state 1 (channel gone or orphaned) checked before each candidate (`0x100138504`, `0x1001806e4` throttled); completed modules persist as REQ-008 | S; timing U |

**Contradiction with the research page.** The state-update transaction
`0x1005a8258` runs at the start of every format pass (VST3 `0x1005e9fd8`, VST2
`0x1005aca28`). Its statements filter by processor only, not by format. So when both
formats are searched, a module left unconfirmed by a crash becomes on-retry in the
first pass of the next session and disabled in the second pass of that session. The
research page's "the session after that" holds only when one format is searched.
The externally predicted outcome (never examined again) is the same. Two further
details limit the derivation:

- each pass moves at most one module, chosen with `LIMIT 1` and no order;
- a module that has plug-in rows is not moved.

**Other derived details, not in the body.**

- A reset scan interrupted in the VST3 part restarts without reset, so VST2 results
  are then not reset.
- Live never sends `--reset vst2|vst3` or, without a debug option, `--limit`.

**Dropped from the body as internal:**

- helper name and argv;
- folder IDs `user`, `local`, `custom`;
- message topics, framing and socket roles;
- database name and schema; scan-state names;
- log lines and `PluginScanner.txt`.

## Revision and handoff

| Revision | Date | Change |
| --- | --- | --- |
| 1 | 2026-10-17 | First draft from the H1 scanner and N4 Live-side evidence: 16 requirements (2 D and S with U parts, 10 S with U parts, 4 U only) and 42 unexecuted cases (36 graded, 6 unresolved) |

Before the 2026-10-18 review, a handoff candidate could carry:

- the D and S clauses of REQ-001 to 011 and 016;
- the graded cases.

REQ-012 to 015 and every U clause stay out until their probes run.

Released 2026-10-18: [plugin-discovery-v1](../../handoff/plugin-discovery-v1/README.md), 35 cases, approved with clarifications by a separate review agent (partial REQ-001, 002, 004, 005 only; 003, 006 to 016 unreleased). The review findings to apply in the next revision are on the [handoff plan](plugin-discovery-handoff-plan.md#review-outcome). This revision's text is unchanged.
