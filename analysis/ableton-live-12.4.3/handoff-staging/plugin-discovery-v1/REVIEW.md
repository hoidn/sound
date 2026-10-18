# Review disposition

Release: plugin-discovery-v1, 2026-10-18.

Reviewer: separate review agent (Claude Opus 5.5), launched by the coordinator
in its own handoff-review context. It did not author this candidate and will
not implement it. The one reviewer performed the scope and evidence, quality
and sanitization, evidence-identity, fixture-sharing and packaging checks.
Publication metadata outside this package is left to the coordinator.

## Scope and checks

Approval covers only the explicit partial clauses of REQ-PLUGIN-DISCOVERY-001,
002, 004 and 005 in [the contract](spec.md). REQ-PLUGIN-DISCOVERY-003 and 006
to 016 remain unreleased.

- Every included clause was checked against the reviewed static evidence for
  the pinned build: which folders each pair of switches adds, the custom folder
  being added only when set and switched on, the folder locations of both
  formats, the VST3 and VST2 tests on an entry's name, which entries are
  searched inside, and what happens to a folder that is missing or cannot be
  read. The author's cross-check was not relied on.
- All 35 expectations were re-derived by the reviewer's own restatement of the
  clauses, written from this contract alone. It agreed with all 35. The
  weakest-provenance cases were also traced to the evidence one by one: a
  missing VST2 system folder (PLUGIN-DISCOVERY-010, and the "absent or empty"
  rule that most VST3-only cases rely on), the unreadable directory and the
  unreadable system folder (033, 034), the folders outside the search (016),
  the plain file named `J.vst3` (021), the letter-case cases (019, 022, 026,
  027) and the CLAP bundles (035).
- The author proposed seven corrections to the draft contract. Each was
  confirmed, and none leaks into this package. Folder order is not graded: no
  clause states one and candidates compare as sets. No case depends on the
  limit on new modules per run or on handling of failing modules: no case has
  more than four candidates of a format or candidates of both formats, more
  than 50 candidates are excluded, and neither order nor examination count is
  compared. Candidate rules are worded on an entry's own name; the reviewer
  confirmed that, without symbolic links, the location the application tests
  is the entry's own path with its letter case unchanged, and links are
  excluded. A missing folder contributing nothing is stated for every folder,
  and the reviewer confirmed it for all six, including a missing VST2 system
  folder and a missing custom folder of either format; the other folders are
  still searched. Names that begin with a period, including `.vst3` and
  `.vst`, are excluded, and no fixture contains one. Wording about the
  structure of the search is absent. The unreadable folder in 033 now holds
  `Q.vst`.
- The author recorded five assumptions. The reviewer's own reading confirmed
  three for the description form: that listing a readable folder returns every
  entry except the folder's own self and parent references, that a folder
  which cannot be opened, including for lack of permission, is skipped while
  the other folders are still searched, and the unchanged-path point above.
  The other two are accepted as stated assumptions: the two VST2 system folder
  locations, which follow the documented locations of the system's per-user
  and computer-wide audio plug-in folders, and that each format's two settings
  are the switches described, which comparison obligation 1 establishes.
- The 20 cases new relative to the draft each exercise a static-derived draft
  clause that had no case. All 20 are accepted. The representation, a set of
  examined entries per format in place of a listing, is accepted. The folder
  and candidate subset is a usable contract on its own.
- Sanitization was checked by the reviewer's own scan of every payload file.
  No source code, recovered program text, internal identifiers or addresses,
  program structure, analyst paths, private evidence links, planning
  identifiers or per-case evidence fields are present. The only flagged word is
  in the forbidden-inputs list of `AGENTS.md`, worded as in the released
  packages. "Process isolation" appears only as excluded behavior.
- Every fixture was read and compared with its purpose. Each is the default
  settings with exactly the change its purpose states. All 35 are distinct,
  ASCII JSON with LF endings, without tabs. Every name uses the allowed
  characters, no path exceeds the length limit, modes appear only on
  directories whose names are not bundle names, and absent paths have no
  content.
- Exclusions appear in both the contract and the manifest and agree. Every
  expectation is labeled static-derived, with reference and candidate
  execution not run. No compatibility is claimed.
- In a copy outside the analyst checkout, every Markdown link and case input
  resolves inside the package and every listed hash and size matches.

## Observability ruling

The open question about how the application side chooses and starts discovery
was checked against the claim that the candidate set is observable. The
application decides both what is searched and what is examined: its settings
select the folders, and the entries it then examines are those the name rules
select there. Which component of the application does each step is internal
and is not graded. The parts of that question that bear on candidate
selection, the folders searched under each switch setting, are answered by the
reviewed evidence. What remains open is excluded here or only affects how a
later probe starts a scan: Audio Units, stored discovery results, identifiers,
duplicates, when scans start, the effect of changing a switch, hanging
modules, progress presentation, and links and unreadable subfolders in VST3
folders.

Examining a candidate means trying to load it, so a bundle that records its
own loads shows examination without any private storage. That holds for
directories. A plain file cannot record a load, and today only progress
counts or stored results, both still open, could show whether one was
examined. The claim therefore holds for directory entries. The plain-file
expectations stay graded as static-derived, and the comparison obligation now
names the affected cases (RVP-04).

## Findings

| ID | Severity | Finding | Resolution |
| --- | --- | --- | --- |
| RVP-01 | Low | Comparison obligation 3 attributed each recorded load to "the format of the folder that contains the entry". That is undefined for an entry outside every searched folder, which is what PLUGIN-DISCOVERY-016 and 035 test. | Clarified: a load is attributed to the format whose searched folder contains the entry; in every case at most one format's folders contain a given entry; a load of an entry no searched folder contains is a mismatch unless shown not to be a VST3 or VST2 examination. No expectation changed. |
| RVP-02 | Low | The manifest's behavior exclusion read "including VST3 before VST2". That restates an unreleased draft clause which holds only within one run of at most 50 new modules. | Reworded to the contract's neutral wording: any order between the formats and between folders. No case affected. |
| RVP-03 | Info | Observability of the candidate set, given the open application-side discovery question. | Ruled as described above: observable for directory entries; the open items are excluded or concern only how a probe starts a scan. |
| RVP-04 | Low | Plain-file candidacy has no established reference observation. Obligation 4 said so in general but did not name the cases. | Obligation 4 now names `J.vst3` in PLUGIN-DISCOVERY-021 and all of PLUGIN-DISCOVERY-028. Expectations unchanged and still graded for candidates. |
| RVP-05 | Info | The seven corrections the author proposed to the draft contract. | All confirmed; none leaks into the payload (see scope and checks). |
| RVP-06 | Info | Remaining assumptions. | Three confirmed by the reviewer's reading, two accepted as stated assumptions, as described above. No expectation invented or changed. |
| RVP-07 | Info | The 20 new cases, the candidate-set representation and the usefulness of the subset. | Accepted. |
| RVP-08 | Editorial | README, AGENTS, contract, cases and manifest described an unreviewed candidate. | Status set to reviewed local release. This record added and linked. Manifest review and status fields filled; inventory re-hashed by the reviewer. |
| RVP-09 | Info | Evidence identity. | The two pinned program images, both evidence runs with every file they list, and the code digests of the separately cited program parts were re-hashed on 2026-10-18. All matched the recorded digests. |
| RVP-10 | Info | Sharing: standard macOS plug-in folder paths, `/Users/Shared` and invented names. | Acceptable. No plug-in, vendor name, executable or shipped content is included. Changing permissions on system folders is a probe-side concern under comparison obligation 5. |

## Disposition

**Approved with listed clarifications** (RVP-01, RVP-02 and RVP-04), only for
the explicit partial clauses in the contract. No scope was narrowed. All
expected results remain static-derived. Neither reference nor candidate
application cases have run, and no compatibility pass is claimed.
Candidate-only checks cannot replace independent reference observations. An
isolated implementation workspace remains a prerequisite.

This disposition concerns the local reviewed-handoff workflow; it does not
authorize external publication. Preserve this release unchanged.
