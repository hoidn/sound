---
id: PLAN-ALS-CONTAINER-HANDOFF
type: research
status: current
updated: 2026-10-17
access: analysis
target: Ableton Live 12 Suite 12.4.3 / macOS
---

# Container and version envelope handoff: candidate and review plan

## Decision and boundary

Stage a finite candidate, als-container-v1, from
[SPEC-ALS-CONTAINER revision 1](als-container.md). The candidate follows the
pattern and gates of the [midi-config-v2 plan](midi-config-v2-handoff-plan.md)
and the [release workflow](../workflows.md#release-a-handoff). The scope is the
static-derived part of REQ-ALS-CONTAINER-001 to 006 that holds on both reader
entries described in the [native research](../research/document-container-native.md#reader-entry-points-and-stream-detection).
Under [ADR 0002](../decisions/adr-0002-static-first-analysis.md#specification-and-verification-boundary),
every expectation is a static derivation; nothing was executed.

The spec's revision note asks for PRB-N2-03 and PRB-N2-05 before a handoff.
This candidate does not resolve them. It excludes every outcome that depends on
them: refusal presentation, and outcomes that differ between the two reader
entries. Review gate 1 must accept or reject that narrowing.

This page is the analyst-side plan and traceability record, not an
implementation input. The candidate is **unreviewed and unpublished**. No
reference or candidate execution has run, and no compatibility is claimed.

## Scope

Outcomes are `envelope-accepted` (no rule in the release refuses the file; it
does not mean the set opens) or `refused` with class `corrupt-document`,
`newer-version` or `unspecified`. Detail kinds and message texts are never
graded.

| Requirement | Included | Excluded remainder |
| --- | --- | --- |
| 001 | First-byte container decision; gzip content classified again; refusal (class unspecified) for whitespace, `<` + non-`?`, BOM + `<`, fewer than two bytes; not well-formed XML refused as corrupt | Stream-type class (entry-dependent; PRB-N2-05); command-level handling of plain XML (PRB-N2-02); gzip flags, truncation, multiple members (PRB-N2-07); non-file gzip source; legacy and UTF-16 starts |
| 002 | Exact `Ableton` root; root without a child refused | Second child; document element other than `LiveSet` |
| 003 | Exact case-sensitive names in any order; integer rule (verified forms only); MajorVersion table; MinorVersion absent or empty refused | ` 5 `, `+5 `, ` +5 ` (N2-014; converter untraced); `-`, leading zeros, overflow; MajorVersion 4 whole-set load (PRB-N2-06); document kinds that skip checks; detail of N2-015/016 |
| 004 | MajorVersion ≥ 6; schema name above its family's largest translator in S | Newer family such as `13.0_13000` (N2-020; PRB-N2-05); version text (PRB-N2-04); the general precedence clause (finding F1) |
| 005 | Names in S pass; letters-only value refused | Gaps such as `12.0_12050` (N2-018; PRB-N2-05); other non-schema values (finding F4); conversion of older documents |
| 006 | Creator and Revision free and optional; SchemaChangeCount optional but integer; other attributes ignored | Unknown-element rule against the schema's ChangeCount; non-refusing Creator effects |
| 007–009 | None | Save container and envelope (PRB-N2-01/02), presentation and state (PRB-N2-03/04) |

The 35 release cases comprise all 23 static-derived r1 cases, re-authored and
narrowed where stated, plus 12 new cases. Each new case exercises a
static-derived r1 clause that had no case. The four unknown r1 cases (N2-014,
N2-018, N2-020, N2-027) are excluded. Combined failures have no expectation.

## Findings while staging

Proposed corrections for a spec revision 2; this page does not edit the spec.

- **F1.** REQ-004's clause "a newer-version condition takes precedence over a
  corrupt-document condition found in the same document" is overbroad.
  Reading stops at the first refusal. Newer-version wins only when its
  condition is recorded together with the refusal: MajorVersion ≥ 6, or the
  MinorVersion stored by check 4. A root-level refusal stops reading first,
  and so does an earlier version check. Examples: `MajorVersion="6"` with
  `SchemaChangeCount="x"`, or with `MinorVersion=""`, derive to
  corrupt-document (order in `0x1015299e0`
  and `0x101529024`; `0x1015289c8` reads only `+0x29` and `+0x38`).
- **F2.** REQ-003 says the checks run at the document element. The two
  illegal-integer refusals run at the root, before it (`0x1015299e0` calls
  `0x10152a900` for MajorVersion and SchemaChangeCount).
- **F3.** The r1 fixtures N2-002 to N2-020 and N2-022 to N2-026 are
  uncompressed. Their reference relevance therefore depends on PRB-N2-02. The
  candidate stores envelope cases in gzip with the 25 shipped sets' header
  form.
- **F4.** "A value not of the form `<a>.<b>_<c>` is refused" is broader than
  the evidence. The lookup only tests whether `<MinorVersion>.txt` exists in
  the schema directory (`0x101514954`). Path-like values, or names of other
  `.txt` files there, are not established as refused. The local copy's
  `Schema` directory also holds 203 AppleDouble `._*.txt` companions, which
  are probably a copy artifact. The candidate narrows to letters-only values.
- **F5.** For an unrecognized start, the general entry's error body
  `0x101483cec` is untraced. If it returned, the dispatcher would throw the
  gzip non-file error (`0x101483b94`), so refusal holds either way. The
  version-aware entry returns no document. The class is therefore left
  `unspecified`.
- **F6.** Proposed r2 case rows: the 12 new cases (ALS-CONTAINER-006, 007, 011,
  017 to 021, 032 to 035), whose sources are listed in `traceability.json`.

## Deliverables

- Payload: [als-container-v1/README.md](../../analysis/ableton-live-12.4.3/handoff-staging/als-container-v1/README.md),
  `AGENTS.md`, `spec.md` (behavioral contract and comparison convention),
  `cases.json` (35 cases), `fixtures/` (35 files) and a draft `manifest.json`
  (`release_status: candidate-unreviewed`, review pending). The manifest lists
  39 payload files; with itself the package has 40. Draft manifest SHA-256:
  `62da834b6b385d2a985896c20f69800d3311ff9f9daaf26462d1216e6c2fb9a7`. Review
  edits will change it.
- Analyst side, never shipped: `als-container-v1-analysis/` with
  [build_als.py](../../analysis/ableton-live-12.4.3/handoff-staging/als-container-v1-analysis/build_als.py)
  (fixtures, cases, manifest, cross-check model, seal and verify),
  [traceability.json](../../analysis/ableton-live-12.4.3/handoff-staging/als-container-v1-analysis/traceability.json)
  and [author-validation.json](../../analysis/ableton-live-12.4.3/handoff-staging/als-container-v1-analysis/author-validation.json).

## Evidence traceability

Evidence is the [N2 run](../../analysis/ableton-live-12.4.3/r2/n2-container-v1/manifest.json)
(manifest SHA-256 `8faab9dccf6a…`, `Live.arm64` `3a99ceea…d1c383cfad`) and the
[S2 schema table](../../analysis/ableton-live-12.4.3/r2/s2-static-v1/out/schemas.json).
Each locator below was re-read on 2026-10-17 before inclusion. Per-case
locators are in `traceability.json`; the payload contains none of them.

| Release cases | r1 source | Kept evidence | Inferred links |
| --- | --- | --- | --- |
| 001, 002 | N2-001, N2-002, narrowed to envelope-accepted | n2-0002 `0x10148389c` disassembly, `0x10146c258.c`; checks below | I6 (001) |
| 003–005 | N2-003 to 005, class dropped | `0x10148389c` 0x1014838cc–0x101483b90; `0x10146c258.c`; corpus `0x10143354c`, `0x101433570`; image-probe BOM | none |
| 006, 007 | REQ-001 clauses, new | as above; gzip branch 0x1014838e4–0x10148396c | I6 (006) |
| 008 | N2-026, gzip and minimal | corpus `0x1012475a8` (final buffer), `0x101247828`, `0x101247760`, `0x101529970`; n2-0003 `0x1015289c8` step 4; corpus `0x10148229c`; `0x10148e4cc.c` | I6 |
| 009, 010 | N2-006, 007 | n2-0002 `0x1015299e0` 0x101529c5c–0x101529c8c | I1, I6 |
| 011 | REQ-002 no-document clause, new | `0x1015289c8.c` step 5; corpus `0x101488e64` | I6 |
| 012–015, 020, 022, 023 | N2-008 to 011, 015, 016; name clause, new | n2-0003 `0x10152a900.c`, `0x10152ab04.c`; n2-0002 `0x101529024` 0x101529038–0x101529130; `0x10147fdbc.c`; writer `0x101485240.c` | I1, I2, I6; I3 (013–015); I4 (022) |
| 016–019, 021 | N2-012 narrowed; spelling and order clauses, new | n2-0005 `0x1002fd908` full disassembly; `0x10152a900.c`; `0x101529024` | I3, I6 |
| 024, 025 | N2-013, 019 | `0x101529024` (signed ≥ 6 sets `+0x29`); `0x1015289c8`; n2-0005 `0x101514e30.c`, `0x101528c84.c`; corpus `0x101514f7c`; schemas.json 12.0 max 12402 | I1, I2, I6; I5 (025) |
| 026, 027 | N2-017; N2-021 with FLG 0 | n2-0003 `0x101514c6c.c`; n2-0005 `0x101514954.c`, `0x101514e30.c`; schemas.json | I5, I6; I1, I2 (026) |
| 028–030 | N2-022 to 024, narrowed | `0x1015299e0.c` (four names read); n2-0001 `refs/0x105b91713.json`; `0x101528e2c.c`; corpus `0x101573d24` | I6 |
| 031–035 | N2-025; integer clauses, new | n2-0005 `0x1002fd908` disassembly; `0x10152a900.c` | I1, I6; I3 (031) |

| Link | Inference not established by kept evidence | Affects |
| --- | --- | --- |
| I1 | An exception from the start-element handler is caught at the callback boundary, and the parse stops with the stored message. The post-parse decision then runs. The catch site is untraced. `0x1012475a8`'s abort handling and the flags set before each throw support it | Refusal class only, never the refusal |
| I2 | `LiveSet`'s class carries the versioned flag that gates the version check. The writer emits versions only for flagged classes, and every shipped set carries them | Refusals raised by the version check |
| I3 | Converter `0x1002fda78` is a base-10 whole-string integer conversion | Accepted integer forms; letter values |
| I4 | A missing MinorVersion may be a null shared empty string; the lookup is assumed null-safe | Case 022 |
| I5 | The lookup and the family scan both use the shipped `Contents/App-Resources/Schema` | Cases 025, 027 |
| I6 | The gzip stream object `0x10146208c` inflates a standard single member with the header used by all 25 shipped `.als` | Every gzip case |

## Fixture construction and sanitization

`build_als.py build` writes every fixture from a four-line template written for
this release. The template has the declaration, a root with
`MajorVersion="5" MinorVersion="12.0_12402" SchemaChangeCount="1"
Creator="Ableton Live 12.4.3"` and an invented Revision, `<LiveSet />` and the
end tag. Each case changes one property of the template. No shipped file is
read. The gzip fixtures use the header `1F 8B 08 00 00000000 02 13`, the form
of all 25 shipped sets ([documents.jsonl](../../analysis/ableton-live-12.4.3/r2/s2-static-v1/out/documents.jsonl)),
followed by raw deflate at level 9 and the CRC-32 and length trailer
(CPython 3.11.13, zlib 1.3.1). The payload names only the S facts the cases
use: `12.0_12402` and `12.0_12117` are in S, and family 12.0 ends at 12402. It
contains no schema content.

## Mechanical checks performed

`build_als.py seal` (CPython 3.11.13 `-I`, Expat 2.6.3) wrote the author
validation:

- The cross-check model agrees with all 35 expectations. It restates the
  released rules over the real 203 shipped schema names. Probes confirmed that
  it rejects excluded inputs (`12.0_12050`, `13.0_13000`, ` +5 `, `-1`, an
  FNAME header). It shares the static evidence and is not an oracle.
- Fixtures were inspected: root start tag, first bytes, line counts, LF
  endings, and the gzip header and trailer.
- Hashes and sizes of the 39 listed files match. The inventory equals the
  directory, and all case inputs exist.
- The sanitization deny-list covers analyst paths, addresses, internal names,
  recovered message strings, probe and case IDs, tool names, absolute paths
  and derivation terms. Its only hit is "decompil" in the forbidden-inputs
  list of `AGENTS.md`, the same wording as the released packages. A probe
  copy with planted terms was flagged.
- In the export copy `/var/tmp/sound-analysis/scratch/stage-als/als-container-v1/`,
  `verify` matched all 39 hashes and resolved all 7 Markdown links inside the
  package. An independent recheck matched as well, and the copy is
  byte-identical to staging.

Not checked: any reference or candidate execution, and any proof of I1 to I6.

## Review gates still required

1. **Scope review**, in a separate context. Check every included clause and
   all 35 expectations against the locators. Check I1 to I6 and F1 to F5, and
   decide whether refusal classes resting on I1 stay graded or narrow to
   `unspecified`. Accept or reject the 12 new cases and the narrowing that
   replaces PRB-N2-03 and PRB-N2-05.
2. **Quality and sanitization review**: behavioral completeness and the
   comparison convention, with exclusions in both spec and manifest. Confirm
   no internal structure or analyst link and no claim beyond static derivation.
   Confirm that naming S facts without schema content is acceptable.
3. **Evidence identity**: the N2 manifest and image hashes matched on
   2026-10-17; re-check before release.
4. **Fixture and sharing review** of the 35 authored fixtures, including the
   product name in `Creator` and the invented Revision.
5. **Decision**: whether a later revision supplies the full list of S names as
   approved data. This candidate does not.
6. **Finalize**: add `REVIEW.md`; set the manifest review fields,
   `release_status` and `release_date`; re-run `seal`; verify an isolated
   export; record the manifest hash in the handoff catalog.
7. **Publish** only after approval. Copy the package unchanged to
   `handoff/als-container-v1/`. Then update the catalog, spec status,
   coverage, indexes and log.
8. An isolated implementation workspace remains unprovisioned.

## Current disposition

Staged on 2026-10-17 as an unreviewed candidate: 35 cases, partial
REQ-ALS-CONTAINER-001 to 006, with 007 to 009 unreleased. It is not published,
and no handoff exists for SPEC-ALS-CONTAINER.
