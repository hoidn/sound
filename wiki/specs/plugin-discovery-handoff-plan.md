---
id: PLAN-PLUGIN-DISCOVERY-HANDOFF
type: research
status: current
updated: 2026-10-18
access: analysis
target: Ableton Live 12 Suite 12.4.3 / macOS
---

# Plug-in discovery handoff: candidate and review plan

## Review outcome

Released 2026-10-18 as [plugin-discovery-v1](../../handoff/plugin-discovery-v1/README.md),
approved with three clarifications and no narrowing by a separate review agent
([review record](../../handoff/plugin-discovery-v1/REVIEW.md)); manifest SHA-256
`9c3c739b0cf624d793a18bff6c36f5677934863af4da6be61dcd4a55555f6113`; 35 cases.
None of F1 to F5 reaches a released case: folders compare as unordered sets, no
case has more than four candidates of one format or mixes formats, links and
names starting with a period are excluded, and the missing-folder rule holds for
all six folders. On Q-016: Live chooses the folders from its switches and the
scanner examines each candidate by loading it, so a bundle that records its own
load makes a directory candidate observable. Plain files cannot record a load.
`J.vst3` in case 021 and all of case 028 therefore cannot yet be compared with
Live, and the comparison obligation names them. Clarifications: RVP-01
attributes loads outside every searched folder (cases 016 and 035); RVP-02
replaces the "VST3 before VST2" wording with neutral wording; RVP-04 names the
plain-file cases. For revision 2 of the spec: adopt F1 to F7 and record the
plain-file observation gap under Q-016. The VST2 folder listing does return
hidden entries, so F5's only open point is how the extension of a name starting
with a period is taken.

## Decision and boundary

Stage a finite candidate, plugin-discovery-v1, from
[SPEC-PLUGIN-DISCOVERY revision 1](plugin-discovery.md). The candidate follows
the pattern and gates of the [als-container plan](als-container-handoff-plan.md)
and the [release workflow](../workflows.md#release-a-handoff). Under
[ADR 0002](../decisions/adr-0002-static-first-analysis.md#specification-and-verification-boundary),
every expectation is a static derivation; nothing was executed.

The Live-side discovery contract is open
([Q-016](../questions.md#q-016-plug-in-discovery-live-side-contract)). Crash,
hang and batch-limit behavior is unknown, and so are scan triggers, source-switch
effects, duplicates, progress presentation and VST3 link and unreadable-subfolder
handling. The candidate therefore carries only the folder and candidate-selection
clauses: which folders each setting adds, and which entries in them are examined.
Every case's expected result is a pair of candidate sets, one per format. Whether
a candidate is then listed, and as what, is not graded. Each excluded behavior is
either an unreleased requirement or a named remainder below.

What remains is a usable contract: a candidate implementation can build its
folder search from it and test it against 35 exact expectations. It is not too
thin to release. Review gate 1 must accept or reject that judgment.

This page is the analyst-side plan and traceability record, not an
implementation input. The candidate is **unreviewed and unpublished**. No
reference or candidate execution has run, and no compatibility is claimed.

## Scope

| Requirement | Included | Excluded remainder |
| --- | --- | --- |
| 001 | `.clap` bundles are not VST3 or VST2 candidates in any folder | D clause (formats, Plug-In Sources activation); process isolation and crash survival (runtime); Audio Units (U) |
| 002 | Two independent switches per format; VST3 and VST2 system folders as a set; custom folder only with its switch on and a folder set; both off gives no candidates; no other folder; a missing folder contributes nothing | Folder order (finding F1); control labels, defaults, effect of changing a switch, scan triggers (U); comma paths (U) |
| 003 | None | Whole requirement: examination order (finding F2) |
| 004 | Exact case-sensitive `.vst3` extension at any depth; directories and plain files; candidates not searched inside; every other directory searched | Resolved-location clause (finding F3); links and unreadable subfolders (U); names that are only an extension (finding F5) |
| 005 | `.vst` in any ASCII letter case, directories only, at any depth; not searched inside; `*.vst3` directories searched; plain files never; unreadable directories skipped, search continues | "Level by level" (finding F6); resolved-folder clause (links excluded); folder-structure presentation (U) |
| 006, 007 | None | What a module contributes; needs loadable plug-in binaries |
| 008–010, 016 | None | Persistence, change detection, removal, Rescan, quitting: runtime across scans |
| 011 | None | Progress content and presentation (U) |
| 012–015 | None | Unknown-only requirements (crash, hang, many modules, duplicates) |

Inputs without an expectation, in both the contract and the manifest: symbolic
links; names outside ASCII letters, digits, space, hyphen, underscore and
period, or beginning with a period; non-absolute custom folders and folder paths
naming a plain file; paths over 255 bytes; permissions other than the
description form; unreadable directories in VST3 folders and permission changes
on bundle-named entries; equal or nested folders of one format (duplicates,
REQ-015); more than 50 candidates of one format (keeps every case inside one
session limit, REQ-014); a home folder other than the account's own; trees that
change during a scan.

The 35 release cases comprise 15 re-authored r1 cases and 20 new ones. Each new
case exercises a static-derived r1 clause that had no case.

### Case disposition

| r1 case | Release case | Change |
| --- | --- | --- |
| PD-001, 002, 003 | 001, 002, 003 | Candidates only; listing as effects and load counts dropped |
| PD-005, 006 | 009, 010 | Candidates only; "scan completes" not graded |
| PD-008, 009, 010 | 017, 019, 020 | Candidates only |
| PD-011 | 021 | Narrowed: J is a candidate. "J not listed, A listed" is REQ-006 |
| PD-012, 013, 014, 015 | 024, 026, 028, 029 | Candidates only |
| PD-016 | 033 | `Q.vst` added inside the locked folder (finding F7) |
| PD-041 | 035 | Candidates only; `/Library/Audio/Plug-Ins/CLAP` and the VST2 folder added |
| PD-004 | Not released | U (comma path) |
| PD-007 | Not released | REQ-003 (finding F2) |
| PD-017–026 | Not released | REQ-006, 007 |
| PD-027–034, 042 | Not released | REQ-008 to 010, 016 |
| PD-036 | Not released | Crash survival is runtime |
| PD-035, 037–040 | Not released | U |

New cases: 004–008, 011–016, 018, 022, 023, 025, 027, 030–032 and 034.

## Findings while staging

Proposed corrections for a spec revision 2. This page does not edit the spec.

- **F1. REQ-002 folder order contradicts REQ-003 and the appendix.** REQ-002
  says the system folders are searched "in this order" and the custom folder
  "after the system folders". REQ-003 marks the order within a format U, and the
  appendix row 003 says the candidate map is ordered by folder ID, which would
  give custom, local, user: the reverse. The stated order is at most the
  argument order (n4-0001). Proposed: drop the order words from REQ-002.
- **F2. REQ-003 clause 1 depends on REQ-014 (U).** The VST2 pass runs even when
  the VST3 pass stopped at the session limit (`0x1001308e0`), and Live
  relaunches after `interrupted` (n4-0001). With more than 51 new VST3 modules,
  VST2 modules are therefore examined before the remaining VST3 modules.
  Clause 2 depends on crash handling (REQ-012, U). Proposed: limit clause 1 to
  one session or relabel it U.
- **F3. REQ-004 and 005 test the resolved entry, not its name.** Both
  walks take the extension from the resolved path (`0x1005e8cb4`,
  `0x1005aad10`). For a link, the target's name decides, and two links to one
  bundle give one candidate. "Every entry whose name ends in" is imprecise
  for links. The release excludes links.
- **F4. Missing folders are stated for VST2 system folders only.** A missing
  VST3 system folder, or a missing custom folder of either format, also
  contributes nothing. Its path is passed and enumeration yields nothing
  (`0x1005e8cb4` listing error ends that root; `0x1005aad10` open failure skips
  it). The VST2 system check is an is-directory test (`0x103e89910`), so a
  VST2 system path that is a plain file also contributes nothing. Proposed: state
  the rule for all folders. The release's REQ-002 clause 7 does so for missing
  folders (cases 007, 008, 014).
- **F5. Names that are only an extension are unresolved.** The extension
  helper `0x1006c4724` has a leading-period branch that the decompiler renders
  unreachable. Whether `.vst3` or `.vst` is a candidate is therefore not
  established, yet the spec's wording would include it. Whether the VST2 folder
  lister returns hidden entries is untraced. Proposed: mark names beginning
  with a period U. The release excludes them.
- **F6. "Level by level" in REQ-005 is traversal structure.** It describes
  an order that REQ-003 leaves undefined and no case grades. Proposed: drop it
  from the body.
- **F7. PD-016 cannot show that an unreadable folder's content is skipped.**
  Its locked folder is empty. Release case 033 adds `Q.vst` inside. Proposed:
  adopt it in r2, together with the 20 new cases, whose sources are in
  `traceability.json`.

No other spec error was found. REQ-002's VST3 user folder uses the home folder
reported by the system (`0x103e9e3d8`), which agrees with `~`.

## Evidence traceability

Evidence is the [H1 run](../../analysis/ableton-live-12.4.3/r2/h1-plugin-scanner-v1/manifest.json)
(manifest SHA-256 `bc605ee8…c98007`; scanner arm64 slice
`6ce847b0…a97ad6`) and the
[N4 run](../../analysis/ableton-live-12.4.3/r2/n4-helper-contracts-v1/manifest.json)
(manifest SHA-256 `99706973…81500f`; `Live.arm64` `3a99ceea…383cfad`). Ten
functions come from the C1 corpora, which are not retained in the repository.
They are listed with their code SHA-256 in `traceability.json`: Live
`0x1030ad96c`, `0x1030adbbc`, `0x103e970a4`, `0x103e89910` and `0x103e9e3d8`,
and scanner `0x1006c4724`, `0x100679138`, `0x1006ad5c8`, `0x10066f1e4` and
`0x10066f240`. Each locator was re-read on 2026-10-18 before inclusion.
Per-case and per-clause locators are in `traceability.json`; the payload
contains none of them.

| Release cases | Kept evidence | Inferred links |
| --- | --- | --- |
| 001–008, 015, 016 | VST3 folders `0x1031c0f28` (home + `Library/Audio/Plug-Ins/VST3`, `/Library/Audio/Plug-Ins/VST3`); switches `0x1031c0d2c`; custom `0x1031c0144` (non-empty only, no existence check); per-format argv items `user`, `local`, `custom` only (n4-0001); scanner runs only the formats given (`0x1001308e0`) | I2; I3, I5 where candidates are found |
| 009–016 | VST2 folders `0x1031b8e5c` → `0x1030ad96c` selectors 2 and 3 → `0x1030adbbc` (`aplg` + `VST`, is-directory check, else empty); switches `0x1031b8c68`; custom `0x1031b7f94` | I1, I2, I4 |
| 017–023 | `0x1005e8cb4` (per root; resolved path; descent disabled on a `.vst3` match or a repeated directory; files and directories inserted; listing error ends the root); `0x1006c4724`, `0x100679138` (exact extension) | I3, I5 |
| 024–034 | `0x1005aad10` (folder list with visited set; directories only; extension lowered per code point by `0x1006ad5c8` and compared with `.vst` at length 4; other directories queued; open failure skips and continues); `0x103e89910` for 034 | I1 (system folders), I4, I5 |
| 035 | As above; no CLAP option (`options.json`); no string containing `.clap` in Live arm64 (C2 `strings.jsonl` `eca20374…`) | I1, I3, I4 |
| all | `0x1005e9fd8`, `0x1005aca28` (no stored module: every candidate checked); `0x100138504` (limit 50, so up to 51 per format per session) | none |

| Link | Inference not established by kept evidence | Affects |
| --- | --- | --- |
| I1 | The folder service with type `aplg` returns `~/Library/Audio/Plug-Ins` for the user domain and `/Library/Audio/Plug-Ins` for the local domain (public API semantics; the returned path is not traced) | VST2 system folders |
| I2 | The two Booleans of each format are the user's system-folder and custom-folder switches, and can be set independently. Gating is observed; the mapping to `Vst3UseSystemFolders` and the other keys, and to labelled controls, is inferred | Every case through its settings |
| I3 | The VST3 recursive listing (option value 5, meaning unresolved) yields every entry of every readable non-candidate directory at any depth | VST3 depth and nesting cases |
| I4 | The VST2 folder lister yields every entry of a readable folder and fails to open a mode-000 folder; the observed failure path then continues | VST2 cases, especially 033 and 034 |
| I5 | Without links, an entry's resolved path equals its path, so the tested name is the stored name, letter case included | Every case with candidates |

## Fixture construction and sanitization

`build_pd.py build` writes the 35 scenario descriptions from the case table.
Each holds the settings per format, an `entries` list of empty placeholder
directories and empty files (optionally mode `000` on a directory), and an
`absent` list. The default settings turn both system-folder switches on and both
custom-folder switches off, with no custom folder. Each case changes only what
its purpose states. Paths use the standard macOS plug-in folders, `/Users/Shared`
for custom folders and invented names; the longest entry path is 62 bytes. No
plug-in, executable, bundle content or shipped file is read or written. The
contract names no internal identifier, folder ID, process, argument or storage
detail.

The comparison obligation tells a later probe how to make examination
observable. It replaces every period-named directory with a bundle that records
its own loads. Plain-file entries remain inconclusive. Those bundles are not
part of the release.

## Deliverables

- Payload: [plugin-discovery-v1/README.md](../../analysis/ableton-live-12.4.3/handoff-staging/plugin-discovery-v1/README.md),
  `AGENTS.md`, `spec.md` (behavioral contract and comparison convention),
  `cases.json` (35 cases), `fixtures/` (35 JSON descriptions) and a draft
  `manifest.json` (`release_status: candidate-unreviewed`, review pending). The
  manifest lists 39 payload files; with itself the package has 40. Draft
  manifest SHA-256:
  `b908dac604ed0a6dc4ad4596303a2e9878cff0c5667895807db83870c05f33e8`. Review
  edits will change it.
- Analyst side, never shipped: `plugin-discovery-v1-analysis/` with
  [build_pd.py](../../analysis/ableton-live-12.4.3/handoff-staging/plugin-discovery-v1-analysis/build_pd.py)
  (case table, fixtures, manifest, cross-check model, exclusion probes, seal and
  verify),
  [mutate_pd.py](../../analysis/ableton-live-12.4.3/handoff-staging/plugin-discovery-v1-analysis/mutate_pd.py)
  (rule-mutation check),
  [traceability.json](../../analysis/ableton-live-12.4.3/handoff-staging/plugin-discovery-v1-analysis/traceability.json)
  (every case and released clause to its r1 source, evidence and inferences)
  and [author-validation.json](../../analysis/ableton-live-12.4.3/handoff-staging/plugin-discovery-v1-analysis/author-validation.json).

## Mechanical checks performed

`build_pd.py seal` (CPython 3.11.13 `-I -B`) wrote the author validation:

- The cross-check model agrees with all 35 expectations. It restates the
  released rules over each description. It rejected all nine probes of
  excluded inputs instead of giving them an expectation: a link, a comma path,
  a leading period, a non-ASCII name, a custom folder inside a system folder,
  an unreadable VST3 directory, a mode on a bundle-named entry, 51 candidates
  and a relative custom folder. It shares the static evidence and is not an
  oracle.
- `mutate_pd.py` flipped 14 rules one at a time, for example VST3 matching
  without regard to case, VST2 accepting plain files, unreadable folders read,
  the custom folder searched without its switch, and `~/Library/Audio/Plug-Ins`
  searched. Each flip changed the result of at least one case.
- All 35 fixtures are distinct, ASCII JSON with LF endings and no tabs.
- Hashes and sizes of the 39 listed files match. The inventory equals the
  directory, all case inputs exist, and there are no links.
- The deny list covers analyst paths, addresses, internal names, folder IDs,
  argument names, storage and state terms, recovered messages, probe, question,
  inference and finding IDs, tool names, traversal-structure terms and absolute
  analyst paths. Its only allowed hit is "decompil" in the forbidden-inputs list
  of `AGENTS.md`, as in the released packages. A copy with planted terms was
  flagged.
- In the export copy
  `/tmp/claude-1000/-home-ollie-Documents-sound/5c433942-c5e3-420d-833a-756602393383/scratchpad/export/plugin-discovery-v1/`,
  `verify` matched all 39 hashes and resolved all 6 Markdown links inside the
  package. `sha256sum -c` against the manifest matched as well, and the copy is
  byte-identical to staging. That copy is session scratch and is not retained.
- H1 (68 files) and N4 (190 files) manifests were re-hashed on 2026-10-18 with
  no mismatch. `Live.arm64` and the scanner slice match their recorded
  digests.

Not checked: any reference or candidate execution, any proof of I1 to I5, and
whether the preference controls can produce every settings combination used.

## Review gates still required

1. **Scope review**, in a separate context. Check every included clause and
   all 35 expectations against the locators. Check I1 to I5 and F1 to F7.
   Accept or reject the 20 new cases, the decision that the folder and
   candidate subset is useful on its own, and the candidate-set representation
   in place of listing.
2. **Quality and sanitization review**: behavioral completeness, exclusions in
   both spec and manifest, no internal structure or analyst link, and no claim
   beyond static derivation. Confirm that the switch roles, defined without
   labels, and the bundle-replacement obligation are intelligible without
   analyst access.
3. **Evidence identity**: the H1 and N4 manifests and image hashes matched on
   2026-10-18; re-check before release.
4. **Fixture and sharing review** of the 35 descriptions, including the
   standard folder paths and `/Users/Shared`.
5. **Finalize**: add `REVIEW.md`; set the manifest review fields,
   `release_status` and `release_date`; re-run `seal`; verify an isolated
   export; record the manifest hash in the handoff catalog.
6. **Publish** only after approval. Copy the package unchanged to
   `handoff/plugin-discovery-v1/`. Then update the catalog, spec status,
   coverage, indexes, questions and log.
7. An isolated implementation workspace remains unprovisioned.

## Current disposition

Staged on 2026-10-18 as an unreviewed candidate: 35 cases, partial
REQ-PLUGIN-DISCOVERY-001, 002, 004 and 005. REQ-PLUGIN-DISCOVERY-003 and 006 to
016 are unreleased. The candidate is not published, and no handoff exists for
SPEC-PLUGIN-DISCOVERY. This page has no index entry yet; the coordinator adds it
together with the log entry.
