# Review disposition

Release: browser-index-v1, 2026-10-18.

Reviewer: separate review agent (Claude Opus 5.5) launched by the coordinator
in its own handoff-review context. It did not author this candidate and will
not implement it. The one reviewer performed the scope and evidence, quality
and sanitization, evidence-identity and fixture-sharing checks. Publication
metadata outside this package is left to the coordinator.

## Scope and checks

Approval covers only the explicit partial clauses of REQ-BROWSER-INDEX-001
and 003 to 008 in [the contract](spec.md), narrowed as listed below.
REQ-BROWSER-INDEX-002 and 009 to 013 remain unreleased. The candidate had 28
cases; this release has 26.

- At least one expectation per released requirement, and every case whose
  support looked weakest, was re-derived from the reviewed static evidence for
  the pinned build: the extension table, the sidecar folder name, the reading
  of a user folder's sidecar and how its entries bind to items, the tag and
  colour readers, the new-sidecar header, the item and colour writers, and
  the four sidecar names. The author's cross-check was not relied on.
- The content kind of all 84 extensions in the table was re-derived from the
  reviewer's own transcription of the kind rule and the registered extension
  list. All 84 agree with cases 001 to 011, and each appears in exactly one
  case.
- How the entries of a user folder's sidecar bind to items was traced further
  than the kept evidence. It is narrower than the candidate stated (RVB-01).
- The colour entry rule was re-derived from the kept evidence and the pinned
  build's machine code (RVB-06).
- The written-sidecar comparison was checked against what the writer can add
  to a new sidecar (RVB-07).
- No case depends on whether the browser lists a file or on when a sidecar is
  written. Expectations are kinds, tags, labels and the content and name of a
  written file. A missing observation or a missing file is inconclusive
  (RVB-03).
- Sanitization was checked by the reviewer's own scan of every payload file.
  None contains source code, recovered program text or messages, internal
  identifiers, addresses, analyst paths, private evidence links, planning
  identifiers or per-case evidence fields. The only flagged word is in the
  forbidden-inputs list of `AGENTS.md`, worded as in the released packages.
- Every fixture was read. The WAV files are identical 60-byte PCM files with
  eight zero samples. Each sidecar is the release template with exactly the
  change its case states. Every sidecar except the truncated one is
  well-formed. Text is ASCII with LF endings.
- Exclusions appear in both the contract and the manifest and agree. Every
  expectation is labelled static-derived, with reference and candidate
  execution not run. No compatibility is claimed.
- In a copy outside the analyst checkout, every Markdown link resolves inside
  the package, every case input exists, and every listed hash and size
  matches.

## Scope rulings

- REQ-001 kind table: kept in scope. It makes no listing claim, and designing
  the channel for observing kinds is left to the probe. Absence from a view is
  not an observation of `none` (RVB-03).
- Factory and built-in file names (cases 026 and 027): kept. The folder
  between `Ableton Folder Info` and the file, and the file's content, stay
  excluded. Each name was recomputed. For factory packs, the general rule
  reproduces the names of 159 of the 160 factory pack sidecars shipped with
  the application.
- The 10 new cases (004 to 011, 021 and 025) each exercise a static-derived
  clause that had no case. All 10 are accepted.
- The candidate excludes the outcomes that depend on listing and on write
  timing, in place of the two planned reference observations. This is
  accepted for a static-derived release. Both observations remain required
  before any compatibility claim.

## Findings

| ID | Severity | Finding | Resolution |
| --- | --- | --- | --- |
| RVB-01 | High | REQ-005 clause 1 let an entry name a file or a folder at any depth below F. Case 016 expected a tag on `sub/b.wav` from an entry with that path, and case 017 expected one on the folder `kit`. The reviewer's static check of the pinned build shows that a user folder's sidecar applies only to the files directly inside that folder, matched by name. Folders and items in subfolders are not matched. Matching at any depth is used only for factory pack sidecars, which this release does not cover. The evidence points to no tags in both cases. | Narrowed. Cases 016 and 017 are removed and their identifiers are not reused. Clause 1 now covers an entry that is exactly the name of a file directly inside F, and REQ-003 clause 2 says the same. Entries that contain `/` or name a folder, and the tags of items in subfolders, are excluded in the contract and the manifest. A later revision may release both cases as negative cases. |
| RVB-02 | Low | The same check shows that an entry naming no file is never applied. The application then treats the sidecar as changed, without that entry. Whether it rewrites the file is untraced. | Narrowed. Whether the application rewrites a sidecar after reading it is now excluded behavior. The assumption that such an entry does not affect other entries is now supported by evidence and is removed from the assumption list. Case 018 is unchanged. |
| RVB-03 | Low | The comparison obligations suggest a browser view as the observation channel. They did not say that absence from a view is not an observation of `none` or of an empty tag set. The edit cases also assume the item is offered for editing. | Clarified. A file absent from a view is not an observation of `none` or of an empty set. An item the original does not present, or does not offer for the edit, makes that comparison or case inconclusive. No expectation changed. |
| RVB-04 | Editorial | Cases 026 and 027 expected no sidecar to be written inside the named content, but no comparison rule covered it. | Added to the comparison rules and the two comparators: no sidecar file inside the Core Library or the built-in content is created or changed. |
| RVB-05 | Editorial | README, AGENTS, contract, cases and manifest described an unreviewed candidate. | Status set to reviewed local release. This record is added and linked, the manifest review fields are filled, and the inventory was re-hashed by the reviewer. |
| RVB-06 | Info | Colour entries. An empty entry is skipped. Any other entry is converted as an unsigned decimal number with no check of the end of the text, and only the low 32 bits are kept. Label n is given when that value is 1 to 7. So `03` gives label 3, and `4294967298` (2^32 + 2) gives label 2. `0` and `8` are ignored. Non-numeric or overlong text causes an error whose effect is untraced. | Confirms the author's finding. Only entries that are exactly `1` to `7`, `0`, `8` or empty are graded, and all other colour text stays excluded. Cases 019 to 021 were re-derived and agree. |
| RVB-07 | Info | Written sidecars. A new user-folder sidecar starts with the three document properties of REQ-007. The entry is keyed by the item's name, and colour labels are written as `1` to `7` in ascending order. The writer may also add `ablFR:assetId` and `ablFR:contentHash`, empty bags and the informational `xmp` properties, in its own serialization. | Accepted. The data model leaves those additions out and treats an absent property as an empty bag, and `expected-sidecar.xmp` is an example, not a byte-for-byte target. Cases 023 to 025 agree. |
| RVB-08 | Info | Evidence identity and recomputation. | The pinned build version, the analyzed program slice, the evidence runs with every file they list, and the kept records were re-hashed on 2026-10-18; all matched the recorded digests. Every kept record matches its source record. All four sidecar names were recomputed. The program step that writes the user's tags for built-in content was found, and it uses the stated name. |
| RVB-09 | Info | Remaining stated assumptions. | Accepted as stated in the contract: sidecars are read when F is indexed and applied to its indexed files; the kind follows from the lowercase extension; tags are those assigned to the item itself; factory and built-in sidecars are written below the User Library, with the factory name computed from the pack's own identifier; names are lowercase hexadecimal. No expectation was invented. |
| RVB-10 | Info | Fixtures and sharing. | Acceptable. There are 26 fixture files, all authored for this release. None contains shipped content. The sidecar template differs from shipped sidecars in serialization. The tag texts are short common words, and some also occur as factory tags. The sidecar names, the namespace identifier and the Core Library's pack identifier are factual values. RFC 9562 is named only to identify the UUID version, and the cases give every name literally, so it is not listed as an approved source. |
| RVB-11 | Info | Proposals for a later revision. | Not released: negative cases for entries with `/` and entries naming a folder; colour text with leading zeros, spaces, signs or more than 32 bits; whether a sidecar is rewritten after reading. |

## Disposition

**Approved with listed narrowing** (RVB-01 and RVB-02), only for the explicit
partial clauses in the contract. The release has 26 cases. All expected
results remain static-derived. Neither reference nor candidate application
cases have run, and no compatibility pass is claimed. Candidate-only checks
cannot replace independent reference observations. An isolated
implementation workspace remains a prerequisite.

This disposition concerns the local reviewed-handoff workflow; it does not
authorize external publication. Preserve this release unchanged.
