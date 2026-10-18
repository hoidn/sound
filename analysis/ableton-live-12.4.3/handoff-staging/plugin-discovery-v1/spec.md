# Plug-in discovery folders and candidates, release 1

Target: Ableton Live 12 Suite 12.4.3 (2026-07-07_e3d8be4d07), macOS, Apple
silicon (arm64). Feature: FEAT-HOSTING, discovery part. Parent specification
identity: SPEC-PLUGIN-DISCOVERY revision 1. Release: plugin-discovery-v1. Only
the clauses explicitly included below are in scope. No other clause of a listed
requirement is implicitly approved. This document is self-contained.

**Status: reviewed local release.** A separate review approved the clauses
below with the clarifications recorded in [the review disposition](REVIEW.md).

## What the contract means

A user installs VST3 and VST2 plug-ins as bundles in the usual folders or in a
custom folder, and the application finds them. This contract describes which
folders are searched for each format under which settings, and which entries in
those folders the application examines as possible plug-in modules. It covers:

- the two system folders and the custom folder of each format, and the two
  switches that add them;
- which entries under a VST3 folder are candidates;
- which entries under a VST2 folder are candidates;
- that bundles named `*.clap` are not VST3 or VST2 candidates.

It does not specify what examining a candidate finds, whether or how a plug-in
is listed, the order of examination, what later scans do, or what the user sees
during a scan.

All rules and expected results are **static-derived**: they were derived for
the target build without running it. None is an observed execution of the
original application, and none was run against a candidate. No compatibility
result is established. The original application remains the authority for a
later comparison. A few derived steps rest on assumptions that were not traced
to the end: that the VST2 system folders are the two locations given in
REQ-PLUGIN-DISCOVERY-002; that each format's two on/off settings are the
switches described there and can be set independently; that listing a readable
folder returns every entry in it, so that readable subfolders are searched at
any depth; and that, in a tree without symbolic links, an entry is judged by
its own stored name. The comparison obligation below covers them.

## Terms

| Term | Meaning |
| --- | --- |
| Format | VST3 or VST2 |
| `~` | The home folder of the macOS user account that runs the application |
| Folder | A location searched for one format, given as an absolute path |
| Entry | A directory or plain file below a folder, at any depth. A folder is not an entry of itself |
| Name | The last component of an entry's path |
| Extension | The part of a name from its last period to the end. `A.b.vst3` has the extension `.vst3`; `B.vst3.bak` has `.bak`; a name without a period has none |
| Examine | Try to load an entry as a plug-in module of the format, to find out which plug-ins it holds. The attempt may fail; a plain file, for example, cannot be loaded |
| Candidate | An entry that a scan examines as a module of a given format |
| Scan | One discovery run, from its start until every candidate has been handled |
| Clean start | No discovery results are stored from any earlier scan |
| System-folder switch | The on/off setting of a format that adds its two system folders |
| Custom-folder switch | The on/off setting of a format that adds its custom folder |
| Custom folder | The one folder chosen by the user for a format, or none |

This release identifies the switches by role. It does not specify which
preference control sets each one, their labels or their defaults.

## Scenario descriptions

Each case's input is a scenario description, a JSON file in `fixtures/` with
these members:

| Member | Content |
| --- | --- |
| `settings` | For each of `vst3` and `vst2`: `system_folders_switch` (true or false), `custom_folder_switch` (true or false) and `custom_folder` (an absolute path, or null when none is set) |
| `entries` | A list of objects with `path`, `type` (`directory` or `file`) and optionally `mode` with the value `"000"` |
| `absent` | Paths that do not exist |

The tree is built as follows:

- A path that starts with `~/` is below the home folder. Every other path is
  absolute.
- Every ancestor of a listed entry that is not itself listed is an ordinary
  directory. Files are empty. The user who runs the application can read and
  search every directory and read every file.
- A directory with `mode` `"000"` has all permissions removed after every entry
  listed below it exists. Only directories whose names do not end in `.vst3`
  or `.vst` (in any letter case) carry a mode.
- Nothing else exists below any folder that the case's settings search. Such a
  folder that is neither listed, nor an ancestor of a listed entry, nor in
  `absent` is either absent or empty; the expected result is the same either
  way.
- Directories are empty placeholders. A directory with a name such as
  `A.vst3` stands for a bundle only through its name. No fixture contains a
  plug-in, an executable or any other file content.

## Outcomes and comparison convention

Each case in [cases.json](cases.json) gives one scenario description and the
expected candidates of each format:

| Label | Value |
| --- | --- |
| `vst3_candidates` | The sorted paths of the entries examined as VST3 modules |
| `vst2_candidates` | The sorted paths of the entries examined as VST2 modules |

Paths are written in the description's form: `~/...` below the home folder,
otherwise absolute.

Comparison rules:

- For each format, the set of candidate paths compares exactly. Order is not
  compared.
- How many times a candidate is examined, what examination finds, whether any
  plug-in is listed and under which name, and any message or progress
  information are not compared.
- Each case is independent. It starts from a clean start with its settings in
  place and covers one scan. No timing applies.
- A candidate adapter may build the tree under a test root, provided it maps
  every path of the description consistently and reports candidates in the
  description's form.

This is a **project comparison representation**, not an API claimed to exist
in Live and not a required design. A candidate adapter may translate its own
result into these labels. The fixture set is not an executable harness for the
original application.

## Selected requirement clauses

Each clause below is included only as stated.

### REQ-PLUGIN-DISCOVERY-001: formats (partial)

1. A bundle whose name ends in `.clap` is not a VST3 or VST2 candidate, in any
   folder. A folder intended for CLAP plug-ins is not searched
   (REQ-PLUGIN-DISCOVERY-002 clause 6). A directory named `*.clap` inside a
   VST3 or VST2 folder is searched like any other directory that is not a
   candidate (REQ-PLUGIN-DISCOVERY-004 and 005).

### REQ-PLUGIN-DISCOVERY-002: searched folders (partial)

1. Each format has two independent switches: a system-folder switch and a
   custom-folder switch. The switches of one format do not affect the other
   format.
2. The VST3 system folders are `~/Library/Audio/Plug-Ins/VST3` and
   `/Library/Audio/Plug-Ins/VST3`. They are searched when the VST3
   system-folder switch is on.
3. The VST2 system folders are `~/Library/Audio/Plug-Ins/VST` and
   `/Library/Audio/Plug-Ins/VST`. They are searched when the VST2
   system-folder switch is on.
4. A format's custom folder is searched when its custom-folder switch is on
   and a custom folder is set, in addition to the system folders if their
   switch is on. With the switch off, a set custom folder is not searched.
   With the switch on and no custom folder set, no custom folder is searched.
5. When both switches of a format are off, that format has no candidates.
6. No other folder is searched for VST3 or VST2 candidates. For example,
   `~/Library/Audio/Plug-Ins` itself, its `Components` and `CLAP` subfolders,
   the same subfolders of `/Library/Audio/Plug-Ins`, and a folder that is not
   the format's custom folder are not searched.
7. A searched folder that does not exist contributes no candidate, and the
   other folders are still searched.

The order in which folders are searched is not specified.

### REQ-PLUGIN-DISCOVERY-004: VST3 candidates (partial)

1. Under each VST3 folder, at any depth, every entry whose extension is exactly
   `.vst3` is a candidate. The match is case-sensitive: `G.VST3` and
   `Mixed.Vst3` are not candidates. `Multi.Dot.vst3` and `Space Name.vst3` are
   candidates; `Backup.vst3.bak` and `Suffix.vst3x` are not.
2. Directories and plain files both qualify. An empty plain file named
   `J.vst3` is a candidate.
3. A candidate is not searched inside, so an entry nested in a candidate is
   not a candidate.
4. Every other directory is searched, whatever its name, including names
   ending in `.vst`, `.component`, `.clap` or `.vst3.bak`.

### REQ-PLUGIN-DISCOVERY-005: VST2 candidates (partial)

1. Under each VST2 folder, at any depth, a directory whose extension is
   `.vst` in any ASCII letter case (`.vst`, `.VST`, `.Vst`, `.vSt`) is a
   candidate. `Two.Dots.vst` is a candidate; `Old.vst.bak`, `Inst.vsti` and
   `N.vst3` are not.
2. A candidate is not searched inside. Every other directory is searched,
   including one whose extension is `.vst3`.
3. A plain file is never a VST2 candidate, even one named `M.vst`.
4. A directory that cannot be read is skipped: nothing below it is a
   candidate. The search continues with the other directories and folders.
   This applies equally to a VST2 system folder that cannot be read.

## Exclusions and deferred obligations

These inputs have **no expectation** in this release:

- symbolic links, anywhere in a tree or in a folder path, and entries other
  than directories and plain files;
- names or folder paths with characters other than ASCII letters, digits,
  space, hyphen, underscore, period and the path separator, including a comma;
  names that begin with a period;
- custom folders that are not absolute paths or that end with a separator,
  and folder paths that name a plain file;
- paths longer than 255 bytes once `~` is expanded;
- permissions other than those of the description form: normal access, or
  mode `000` on a directory as allowed there;
- in a VST3 folder, any directory that cannot be read, including the folder
  itself; a permission change on any entry whose name ends in `.vst3` or
  `.vst` in any letter case;
- two folders of one format that are equal or nested, such as a custom folder
  at or below a system folder of its format;
- more than 50 candidates of one format;
- a home folder other than the account's own, for example a different `HOME`
  environment value, and a folder whose stored letter case differs from the
  paths in this release;
- a tree that changes while a scan runs.

Excluded behavior:

- the order of examination, including any order between the formats and
  between folders (REQ-PLUGIN-DISCOVERY-003, unreleased);
- what a candidate contributes: whether it is listed, its names, instrument or
  effect, code signatures and entry points (REQ-PLUGIN-DISCOVERY-006 and 007,
  unreleased);
- later scans: unchanged, changed, removed and returning modules, Rescan and
  its reset variant, and quitting during a scan (REQ-PLUGIN-DISCOVERY-008 to
  010 and 016, unreleased);
- progress information and how it is presented (REQ-PLUGIN-DISCOVERY-011,
  unreleased);
- modules that crash or hang, more than 50 new modules, and duplicate bundles
  or class identifiers (REQ-PLUGIN-DISCOVERY-012 to 015, unreleased);
- from REQ-PLUGIN-DISCOVERY-001: Audio Unit discovery, process isolation and
  survival of a crashing module, and the activation of plug-in sources in the
  preferences;
- from REQ-PLUGIN-DISCOVERY-002: control labels and defaults, the effect of
  changing a switch or a custom folder, when scans start, and custom folders
  whose path contains a comma;
- from REQ-PLUGIN-DISCOVERY-004 and 005: symbolic links, unreadable
  subfolders in VST3 folders, and whether the folder structure below a VST2
  folder is presented to the user.

Before claiming reference compatibility, a separately designed bounded probe
must run these cases, or a justified equivalent set, against the original. It
must pin the original and candidate builds and the scenario descriptions,
retain independent observations, and report mismatches. Five obligations are
specific to this release:

1. The probe first establishes which preference control sets each switch role.
   Each case starts from a clean start with its settings in place before the
   tree exists. How a scan is started, and how a clean start is reached, are
   not specified here.
2. To make examination observable, the probe replaces every directory in the
   tree whose name contains a period by a bundle that records each time it is
   loaded. Each bundle keeps the entries the description lists below that
   directory, adds no entry whose name ends in `.vst3` or `.vst` in any letter
   case, loads without crashing or blocking, and carries no invalid code
   signature. Directories without a period in their names stay ordinary
   directories. Such bundles are not part of this release.
3. The observation is the set of recorded loads from the creation of the tree
   until no further examination occurs. A load is attributed to the format
   whose searched folder contains the entry; in every case, the searched
   folders of at most one format contain any given entry. A load of an entry
   that no searched folder contains, as in PLUGIN-DISCOVERY-016 and 035, is a
   mismatch unless another method shows that it was not an examination as a
   VST3 or VST2 module.
4. A recorded load cannot show whether a plain file was examined. For entries
   that are plain files the observation is inconclusive unless another method
   shows whether the application examined them. In this release that applies
   to `J.vst3` in PLUGIN-DISCOVERY-021 and to all of PLUGIN-DISCOVERY-028.
5. Directories with mode `000` are created by the user who runs the
   application, and the application runs without elevated privileges.

Candidate-only success proves agreement with this contract, not with the
running original.

## Fixture provenance

All 35 scenario descriptions were authored for this release. Each is ASCII
JSON with line-feed line endings. Settings default to both system-folder
switches on, both custom-folder switches off and no custom folder set; each
case changes only what its purpose states. Paths use the standard macOS
plug-in folder locations, `/Users/Shared` for custom folders, and invented
names.

No fixture contains a plug-in, an executable, bundle content, shipped file
content or assets. Expected results are newly authored static-derived
behavioral data. No public source or dependency is approved or included.
Review status is recorded in [the manifest](manifest.json) and
[the review disposition](REVIEW.md).
