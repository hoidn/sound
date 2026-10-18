---
id: PLAN-BROWSER-INDEX-HANDOFF
type: research
status: current
updated: 2026-10-18
access: analysis
target: Ableton Live 12 Suite 12.4.3 / macOS
---

# Browser index handoff: candidate and review plan

## Review outcome

Released 2026-10-18 as [browser-index-v1](../../handoff/browser-index-v1/README.md),
approved with narrowing by a separate review agent
([review record](../../handoff/browser-index-v1/REVIEW.md)); manifest SHA-256
`c47068980e7a10440f059acde5797b5760a2f18478ab97869c19340ead7225a5`. The review
cut the 28 staged cases below to 26.

The reviewer made three changes:
- **RVB-01:** cases 016 (`sub/b.wav`) and 017 (folder `kit`) are removed. A
  user folder's sidecar binds by name only to files directly inside that
  folder, so subfolder items and folders get no tags. REQ-005 clause 1 and
  REQ-003 clause 2 are narrowed to match.
- **RVB-02:** whether Live rewrites a sidecar after reading it is excluded.
- **RVB-03:** absence from a view is not an observation, and a case whose item
  is not shown or offered is inconclusive.

The reviewer also confirmed the numeric colour rule: only the low 32 bits are
kept, so `03` gives label 3 and `4294967298` gives label 2.

The draft spec needs three fixes. REQ-005 must bind direct files only, which
makes r1 cases BI-040 and BI-041 wrong. REQ-006's "other numeric entries are
ignored" is too broad. The draft must also add that entries naming no file are
dropped and the sidecar is marked changed.

Applied in revision 2 (2026-10-18); rejected: F7 (a candidate narrowing, not a draft error) and RVB-05, RVB-08, RVB-09 and RVB-10 (release status, evidence identity, accepted assumptions and fixtures; no draft text depends on them).

## Decision and boundary

Stage a finite candidate, browser-index-v1, from
[SPEC-BROWSER-INDEX revision 1](browser-index.md). The candidate follows the
pattern and gates of the [ALS container plan](als-container-handoff-plan.md)
and the [release workflow](../workflows.md#release-a-handoff). Its scope is the
static-derived part of REQ-BROWSER-INDEX-001 and 003 to 008: content kind by
extension, the user-folder tag sidecar as read and as written, and the sidecar
file names for the user's tags on Core Library and built-in content. Under
[ADR 0002](../decisions/adr-0002-static-first-analysis.md#specification-and-verification-boundary),
every expectation is a static derivation; nothing was executed.

The spec's revision note asks for three things before a handoff: the corpus
reads retained, PRB-BI-01 (listing) and PRB-H2-04 (write location and timing).
The reads are retained (finding F1). This candidate does not resolve the two
probes. It excludes every outcome that depends on them, as the revision note
allows: listing of any file, write timing, the `<n>` folder, nested items and
merging into an existing sidecar. Review gate 1 must accept or reject that
narrowing.

This page is the analyst-side plan and traceability record, not an
implementation input. The candidate is **unreviewed and unpublished**. No
reference or candidate execution has run, and no compatibility is claimed.
Open question: [Q-014](../questions.md#q-014-browser-index-behavior).

## Scope

| Requirement | Included | Excluded remainder |
| --- | --- | --- |
| 001 | Kind of a file from its lowercase extension, for the 84 extensions in the table (13 kinds and none) | Whether any file is listed (PRB-BI-01); upper case, no extension, unregistered extensions and `.ablx`; folder kinds and plug-ins; named content sets; sidebar categories (PRB-BI-02) |
| 002 | None | All of it: no location configuration is constructible without the unknown UI (PRB-BI-02, PRB-H2-05) |
| 003 | Parent-name test inside F; F's sidecar with the user-folder name is read | Other names in the sidecar folder (BI-022), a sidecar folder below F (BI-023), letter case (BI-024), the override folder branch, sidecar folder visibility, user folders inside the User Library |
| 004 | Folder-resource form of the fixtures; `xmp` properties ignored; not well-formed gives no tags or labels; the written header | `win`/`linux` platform (BI-032), xpacket (BI-033), other resources, unknown properties, document-level tags, alternative RDF forms, any message |
| 005 | `filePath` relative to F with `/`, file or folder at any depth; an entry naming nothing does not affect others | Case-insensitive matching (BI-043), `..` and absolute paths (BI-044); tags of items inside a tagged folder |
| 006 | Keywords entries give tags; colour entries exactly `1` to `7` give labels; `0`, `8` and empty ignored; written encoding | Other colour texts (BI-052; finding F3), tag levels other than 2 or 3 and duplicates (BI-054), `hideKeywords` (BI-055), empty keyword entries |
| 007 | New user-folder sidecar for an item directly in F: name, location, header and item entry; override file names for the Core Library and built-in content, with the folder depth but not the folder name | Timing (PRB-H2-04), `<n>`, override content and reading, existing sidecars (BI-062), nested items (BI-063), read-only volumes (BI-066), quit (BI-067), missing User Library, removal of emptied sidecars (finding F5) |
| 008 | A folder copied with its sidecar folder keeps its tags on another installation | Rebuild after an edit (BI-070), data kept only in the index |
| 009–013 | None | Previews (PRB-BI-05), change handling, missing and moved items, unsupported files, the index and its rebuild |

The 28 release cases comprise 18 of the 24 static-derived r1 cases, narrowed
where stated, plus 10 new cases. Each new case exercises a static-derived r1
clause that had no case. The six other static-derived r1 cases are excluded
with their requirements: BI-080 to 083 (REQ-009, whose observable effect
depends on PRB-BI-05) and BI-100 and BI-103 (REQ-011, change handling). All 28
unknown r1 cases are excluded.

| r1 case | Release case | Change |
| --- | --- | --- |
| BI-001, 002, 003 | 001, 002, 003 | Kind only; "listed" and "none listed" dropped (PRB-BI-01) |
| (table rows) | 004 to 011 | New: every remaining extension of the table appears in exactly one case. BI-004's file set is covered by kind only; BI-004 itself (listing) stays excluded |
| BI-020, 021 | 012, 013 | "the `.xmp` is not listed" dropped: it rests on the kind-filter assumption of REQ-001 (finding F6) |
| BI-030, 031 | 014, 015 | 015: no tags and no labels only; other effects excluded |
| BI-040, 041, 042 | 016, 017, 018 | 017: `k.wav` and display dropped (inheritance unknown). 018: "no entry or error for `gone.wav`" dropped |
| BI-050, 051, 053 | 019, 020, 022 | 022: grouping dropped |
| (REQ-006 bounds) | 021 | New: labels 1 and 7 |
| BI-060, 061 | 023, 024 | Timing, "nothing else in F changes", `assetId` and `contentHash` dropped (finding F4); an absent file is inconclusive |
| (REQ-006/007 writer) | 025 | New: tags and two labels written together |
| BI-064, 065 | 026, 027 | File name and folder depth only; `<n>`, content and timing excluded |
| BI-071 | 028 | Unchanged |

Comparison labels are `content_kind`, `tags`, `labels` and a sidecar data
model: dc and ablFR document properties plus the multiset of item entries,
absent equal to an empty Bag, ignoring `xmp` properties, `assetId` and
`contentHash`. The kind labels are project labels that paraphrase the r1
table; none is a name the program uses.

## Findings while staging

Proposed corrections for a spec revision 2; this page does not edit the spec.

- **F1 (stale text).** The appendix says the corpus reads marked † are "Not
  retained" and should be kept before review, and the revision note lists that
  as a prerequisite. They are retained in
  [d2-browser-index-v1](../../analysis/ableton-live-12.4.3/r2/d2-browser-index-v1/README.md)
  (manifest digests re-checked 2026-10-18), as the research page already says.
- **F2 (strengthening).** REQ-007 calls `mac` for a new sidecar's
  `ablFR:platform` inferred. It is static-derived: the new-sidecar
  constructor `0x1006e4394` passes resource 1 and platform 2 to `0x1006f07c8`,
  whose header writer `0x1006f09d8` indexes the platform table `0x100dbd698`
  = [`win`, `mac`, `linux`] at platform − 1. The format table `0x100dbd650`
  is [`""`, folder, factory-pack, plugin-device, app-builtin], indexed by the
  resource kind itself.
- **F3 (overbroad).** REQ-006 says other numeric colour entries are ignored.
  `0x1006ed324` converts with `std::stoul(…, base 10)` without checking the
  end and keeps the low 32 bits before the 1-to-7 test, so `03`, ` 3` and
  `3x` give label 3 and `4294967298` gives label 2. A non-numeric value throws;
  its effect is untraced (BI-052). The candidate grades only `0` to `8` and
  empty.
- **F4 (overbroad).** BI-060 expects the written file to equal Fixture A with
  the new tag, and "nothing else in F changes". The item writer `0x1006ef218`
  writes `assetId` and `contentHash` under a condition on the item's asset
  identity whose meaning is untraced, so a new entry may carry them. Only the
  sidecar write was read, so other files in F are not established. The
  candidate's data model ignores those two fields and judges only the sidecar.
- **F5 (missing behavior).** The file writer `0x1006cce78` removes a sidecar
  whose document has become empty, and then its sidecar folder if that is
  empty (`Remove empty Metadata file`). It creates the parent folders before
  writing, and skips paths that `0x1006e71c8` classifies. None of this is in
  REQ-007. Not released: the emptiness test `0x1006e1ae4` is untraced.
- **F6 (label).** BI-020 and BI-021 are labelled static-derived with only
  REQ-003's assumption, but their "`.xmp` is not listed" part also rests on
  REQ-001's kind-filter assumption (PRB-BI-01).
- **F7 (candidate narrowing, not a spec error).** REQ-003's parent-name test
  also accepts files whose parent is the User Library override folder, which
  is not named `Ableton Folder Info`; the spec says so. The candidate therefore
  states the negative clause for files inside F only and excludes user folders
  inside the User Library.
- **F8 (resolvable unknowns).** The keyword reader `0x1006ed554` skips empty
  entries and inserts the rest into a set, so duplicates collapse. The folder
  writer `0x1006d03b8` keys a new entry by the leaf name of the item's path
  (`0x10075f5c0`), and writes tags of the folder itself at document level. These
  bear on BI-054 and BI-063 but are not released.
- **F9.** Proposed r2 case rows: the 10 new cases (BROWSER-INDEX-004 to 011,
  021 and 025), whose sources are in `traceability.json`.

[Q-014](../questions.md#q-014-browser-index-behavior) still lists "how XMP
sidecar names are derived" under Gap although its D2 progress line resolves it.

## Deliverables

- Payload: [browser-index-v1/README.md](../../analysis/ableton-live-12.4.3/handoff-staging/browser-index-v1/README.md),
  `AGENTS.md`, `spec.md` (behavioral contract and comparison convention),
  `cases.json` (28 cases), `fixtures/` (30 files in 15 case folders) and a
  draft `manifest.json` (`release_status: candidate-unreviewed`, review
  pending). The manifest lists 34 payload files; with itself the package has
  35. Draft manifest SHA-256:
  `5d821ca7aef3799acb992f502264617eedf243ac56fc8cc31ed7e22121606328`. Review
  edits will change it.
- Analyst side, never shipped: `browser-index-v1-analysis/` with
  [build_bi.py](../../analysis/ableton-live-12.4.3/handoff-staging/browser-index-v1-analysis/build_bi.py)
  (fixtures, cases, manifest, seal and verify),
  [crosscheck_bi.py](../../analysis/ableton-live-12.4.3/handoff-staging/browser-index-v1-analysis/crosscheck_bi.py)
  (models and mutation probe),
  [trace_bi.py](../../analysis/ableton-live-12.4.3/handoff-staging/browser-index-v1-analysis/trace_bi.py),
  [traceability.json](../../analysis/ableton-live-12.4.3/handoff-staging/browser-index-v1-analysis/traceability.json),
  [author-validation.json](../../analysis/ableton-live-12.4.3/handoff-staging/browser-index-v1-analysis/author-validation.json)
  and `kept/corpus-addendum.jsonl`.

## Evidence traceability

Evidence is the [H2 run](../../analysis/ableton-live-12.4.3/r2/h2-index-v1/manifest.json)
(helper arm64 slice `3390bd4b…a289b62`, C1 run `858745e5…6cf8c1f`), the
retained D2 reads (`cited-functions.jsonl`, SHA-256 `b3cd0db5…a654`) and a
kept addendum of five further corpus records copied unchanged for this
candidate (`kept/corpus-addendum.jsonl`, SHA-256 `d0d2905d…8485`: `0x10013f420`,
`0x1006cce78`, `0x1006e1ad0`, `0x1006e4394`, `0x1006f07c8`). Each locator below
was re-read on 2026-10-18. Per-case locators are in `traceability.json`; the
payload contains none of them.

| Release cases | Kept evidence | Inferred links |
| --- | --- | --- |
| 001–011 | Registry `file-type-registry.tsv` (80 rows, 85 extensions); kind map `0x10016b758`, evaluated for every code by compiling its pseudocode; bit names `0x10016b3e8` | I2 |
| 012, 013, 028 | Gate `0x1006e6d40` (leaf of parent equals the `Ableton Folder Info` constant, else parent equals `0x1006e5d68`); reader `0x1006d2624` (gate first; resource-kind 1 branch takes R as the sidecar's grandparent and applies items only when R is indexed); single caller `0x10013f420` | I1 |
| 014, 015 | Reader parse `0x1006e4778` and its error branch (`Error reading xmp file: `, empty result); reader reads only ablFR item fields | I1 |
| 016–018 | Item read `0x1006ee124`; shipped resolution counts (7,084 of 7,085; all 85 built-in entries are folders) | I1, I3, I4 |
| 019–022 | Colours read `0x1006ed324`; keywords `0x1006ed554` | I1 |
| 023–025 | Folder writer `0x1006d03b8`; path `0x1006e637c` mode 1; new document `0x1006e4394` → `0x1006f07c8` → `0x1006f09d8` with tables decoded by `read_ptrs.py` on the pinned slice; item writer `0x1006ef218`; colours write `0x1006edbbc`; file writer `0x1006cce78` | I7 |
| 026 | `0x1006e5f48` (name under `0x1006e5d68`), writer `0x1006cf838`; namespace `uuid5(nil, "factory-pack")`; Core Library sidecar `packUniqueId` `www.ableton.com/0`; 159 of 160 Legacy Pack Data names recomputed | I5, I6, I7 |
| 027 | `0x1006e67dc` (`uuid5(uuid5(nil, "app-resource"), "builtin")`) | I5, I7 |

| Link | Inference not established by kept evidence | Affects |
| --- | --- | --- |
| I1 | The indexer passes each file of a location's sidecar folder to the reader. Only the reader and its queue-pop caller are read | Every read case |
| I2 | A file's type, and so its kind, comes from its lowercase extension through the registered extension list; the lookup is not kept | 001–011 |
| I3 | An entry naming no indexed item is skipped without affecting others (apply step `0x1006dbf98` untraced; the shipped built-in sidecar has one such entry) | 018 |
| I4 | Assigned tags are observable per item, without inheritance from the folder | 016, 017 |
| I5 | The override base folder is the User Library (config accessor untraced; the refusal message names it) | 026, 027 |
| I6 | The pack identifier given to the name construction is the pack sidecar's `packUniqueId` | 026 and the general rule |
| I7 | UUID text is lowercase with hyphens (formatter `0x100616d44` not kept; every shipped sidecar name is) | 023–027 |

## Fixture construction and sanitization

`build_bi.py build` writes every fixture. WAV files are 60-byte PCM files
(one channel, 44,100 Hz, 16 bit, eight zero samples). Sidecars come from one
template written for this release, with one-space indentation, no XML
declaration and no packet wrapper; the base sidecar is byte-identical to r1's
Fixture A. Each sidecar case changes what its purpose states. The write cases carry an
`expected-sidecar.xmp` generated from the expected data model. The
classification cases have no fixture files. No shipped file is read by
`build`.

The payload names three sidecar file names, one namespace UUID and the Core
Library's pack identifier. All four values are file names or document text of
the installed product. It names RFC 9562 only to identify the UUID version.
The tag texts reuse r1's examples, some of which are also factory tag names.

## Mechanical checks performed

`build_bi.py seal` (CPython 3.13.9 `-I`, gcc 13.3.0) wrote the author
validation:

- The read and write models agree with all 15 folder-case expectations, and
  each `expected-sidecar.xmp` parses to its case's data model. The compiled
  kind map agrees with every row of the release table; cases 001 to 011 cover
  each of the 84 extensions exactly once; `.ablx` is the only registered
  extension unknown to the kind map. All four sidecar names were recomputed.
  The models share the static evidence and are not an oracle.
- The mutation probe altered ten expectations (labels, sidecar location,
  truncation, unresolved and nested entries, written platform and labels, two
  kinds, a non-exact colour text); the models rejected all ten.
- Fixtures were inspected: every WAV header, UTF-8 and LF endings, and
  well-formedness of every sidecar except the truncated one.
- Hashes and sizes of the 34 listed files match. The inventory equals the
  directory, there are no symlinks and all case inputs exist.
- The sanitization deny-list covers analyst paths, addresses, internal names
  and program kind names, recovered messages, probe, finding and r1 case IDs,
  tool names, absolute paths and construction strings. Its only hit is
  "decompil" in the forbidden-inputs list of `AGENTS.md`, worded as in the
  released packages. A probe copy with planted terms was flagged.
- In an export copy in the session scratch directory, `verify` matched all 34
  hashes and resolved all 6 Markdown links inside the package. An independent
  recheck matched as well, and the copy is byte-identical to staging.
- Evidence identity: the registry digest matches the H2 manifest, the D2 files
  match the D2 manifest, and the helper slice matches `3390bd4b…a289b62`.

Not checked: any reference or candidate execution, and any proof of I1 to I7.

## Review gates still required

1. **Scope review**, in a separate context. Check every included clause and
   all 28 expectations against the locators, I1 to I7 and F1 to F8. Decide
   whether the REQ-001 kind table stays in scope without any listing claim and
   with an observation channel still to be designed, or is removed. Decide
   whether the override names (026, 027) stay with the folder name and content
   excluded. Accept or reject the 10 new cases and the narrowing that replaces
   PRB-BI-01 and PRB-H2-04.
2. **Quality and sanitization review**: behavioral completeness, the data-model
   comparator (absent equals empty Bag; `assetId` and `contentHash` ignored),
   exclusions in both contract and manifest, and no internal structure or
   analyst link. Confirm that describing the name rule through RFC 9562 is
   acceptable without listing it as an approved source.
3. **Evidence identity**: re-check the H2 and D2 manifests, the addendum hash
   and the helper slice before release.
4. **Fixture and sharing review** of the 30 authored fixtures, the tag texts,
   the three file names, the namespace UUID and the Core Library identifier.
5. **Finalize**: add `REVIEW.md`; set the manifest review fields,
   `release_status` and `release_date`; re-run `seal`; verify an isolated
   export; record the manifest hash in the handoff catalog.
6. **Publish** only after approval. Copy the package unchanged to
   `handoff/browser-index-v1/`. Then update the catalog, spec status,
   coverage, indexes, questions and log. This page still needs an entry in the
   [spec index](index.md).
7. An isolated implementation workspace remains unprovisioned.

## Current disposition

Staged on 2026-10-18 as an unreviewed candidate: 28 cases, partial
REQ-BROWSER-INDEX-001 and 003 to 008, with 002 and 009 to 013 unreleased. It
is not published, and no handoff exists for SPEC-BROWSER-INDEX.
