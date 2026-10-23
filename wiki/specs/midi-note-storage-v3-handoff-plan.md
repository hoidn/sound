---
id: PLAN-MIDI-NOTE-STORAGE-V3-HANDOFF
type: research
status: superseded
updated: 2026-10-20
access: analysis
target: Ableton Live 12 Suite 12.4.3 / macOS arm64
---

# Third MIDI note storage handoff: six local group comparisons

Current catalog disposition2026-10-20: v3 is superseded by [v4](midi-note-storage-v4-handoff-plan.md#current-local-publication--2026-10-20). Its payload and the dated publication records below remain unchanged.

## Review outcome and current disposition

Released locally2026-10-20 as [midi-note-storage-v3](../../handoff/midi-note-storage-v3/README.md),
manifest SHA256 `fa281c37472e13a6ba840499687e90928654c9862582fa5bd4d04f4436da7c2c`. All83 payloads/217,952bytes plus manifest match the
[sealed final tree](../../analysis/ableton-live-12.4.3/handoff-staging/midi-note-storage-v3-final/manifest.json) exactly;
[copy receipt](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/midi-note-storage-v3-local-copy-receipt.json).
The [independent content review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/midi-note-storage-v3-handoff-review.json)
found one stale supersession metadata block, H01; the
[separate r2 correction review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/midi-note-storage-v3-r2-final-seal-review.json)
closed it. The [external final exact-tree seal](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/midi-note-storage-v3-final-exact-tree-review.json),
SHA256 `af2536c413fe1359541ca1f6963c6f85723ed05d35b8a5f81aef50e50ea7d2a4`, approves exact local copying.
All original/r2/final staging trees remain immutable. No future seal hash was
embedded into its own payload; the catalog records actual publication.

V3 supersedes v2 with all72 prior case objects/fixtures and13 prior partial
requirement bodies exact. Six local group comparisons add partialREQ015,
for78 cases/14 partial clauses. Four local refusals/two nonrefusals retain A1
and supplied-counter premises. Final Save, whole-load repair, missing-note
effects, public lifecycle and original/candidate compatibility remain U.
No new original run, candidate execution or grade occurred. Full pre-release
[lint v60](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/documentation-lint-2026-10-20-v60-pre-midi3.json) passed;
[Destination/catalog and15changed-page checks](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/midi-note-storage-v3-publication-incremental-check.json) passed:83new payloads/all84destination files exact,35releases/19current/16superseded, no new links/errors. The staging
and pending-gate wording below is historical, not the current disposition.

## Original staging record (history)

The candidate is staged, unreviewed and unpublished. Nothing was written into
`handoff/`; the current [v2 release](../../handoff/midi-note-storage-v2/README.md)
remains unchanged. [Candidate payload](../../analysis/ableton-live-12.4.3/handoff-staging/midi-note-storage-v3/README.md),
[manifest](../../analysis/ableton-live-12.4.3/handoff-staging/midi-note-storage-v3/manifest.json),
[author checks](../../analysis/ableton-live-12.4.3/handoff-staging/midi-note-storage-v3-analysis/author-validation.json)
and [analyst traceability](../../analysis/ableton-live-12.4.3/handoff-staging/midi-note-storage-v3-analysis/traceability.json)
are ready for an independent handoff review under the
[release workflow](../workflows.md#release-a-handoff).

## Selection and provenance

Select only the six existing MNS-054 to MNS-059 cases from the independently
reviewed [r5 canonical owner](midi-note-storage.md#req-midi-note-storage-015--probability-groups).
The [owner review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/midi-probability-groups-owner-r5-review.json)
and [adoption](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/midi-probability-groups-owner-r5-adoption.json)
approve a bounded static refinement, following the
[conditional source review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/depth-midi-probability-groups-v1-review.json).
That approval is not handoff approval or executed reference behavior.

The reviewed canonical prefix is 63,380 bytes, SHA-256
`0f9cfe15d7af8043f604af2377c1c0ad7d5c6352968d6fd5b6e2b6c32caae11b`.
Its later additive disposition is not copied into the candidate.
All 72 v2 case objects, 72 gzip fixture bytes and 13 released partial
requirement bodies are carried exactly. The five earlier extracted-execution
cases retain their labels and numerical clauses; no original code reruns.

## Added scope

| Cases | Exact input difference | Contracted comparison |
| --- | --- | --- |
| MNS-054 | GroupId 0, group NextId 1 | Local refusal |
| MNS-055 | GroupId 5, group NextId 1 | Local refusal |
| MNS-056 | GroupIds 2 then 1, group NextId 3 | Local refusal |
| MNS-057 | GroupIds 1 then 1, group NextId 2 | Local refusal |
| MNS-058 | GroupId 1, notes 1 and 2, group NextId 2 | Local admission only |
| MNS-059 | GroupId 1, missing note 99, group NextId 2 | Local admission only; later effects unknown |

Each group supplies type 0 and probability 1. MNS-054 to 058 name notes 1 and
2 in each group. The conditional input representation uses a `GroupId` child,
nested `NoteId` attributes, and group-list `Id` values distinct from GroupId.
No enum label or playback meaning is released. All six authored full Set
fixtures replace only Notes in the v2 MNS-001 carrier with the
[reviewed concrete fragments](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-midi-probability-groups-v1/case-proposals.json).
The existing freeze slot and scene repair and all carrier bytes outside Notes
remain exact. This is authored content, not a shipped Set.

The six additions use `validate-notes` and `local_reader_outcome` as a project
comparison projection of the supplied data. It specifies neither a public
Live validation API nor an implementation pipeline. Implementations may
validate anywhere. The observation assumes ordinary Set-read validation is
enabled (A1) and compares the supplied group counter at that point. A public
Set-open result cannot establish that local observation or its counter premise.
The legacy `loads`/`refused` public-open comparison remains confined to the
72 unchanged records. No new public load/save success is asserted.

## Exclusions retained

Final saved group text/default omission, complete-load counter repair, later
missing-note effects, public error presentation and lifecycle, unsupported
group enum values, playback semantics and actual original/candidate execution
remain unknown. Requirements 011, 012 and 017 remain unreleased; REQ-015 is
selected only for the six exact local inputs. No new requirement or case ID.

## Validation and remaining release gate

The [data-only checker](../../analysis/ableton-live-12.4.3/handoff-staging/midi-note-storage-v3-analysis/build.py)
checks predecessor preservation, exact Notes transplants, gzip members,
input pins, payload hashes, links, limited sanitization and exact carried
clauses. Only the inspected existing schema/structure helper is imported;
no native collector, execution builder or original binary runs. The six new
fixtures have no target-schema deviations, structural refusals or structural
unknown shapes under those bounded helpers. This validates authored data,
not native behavior. The unchanged deliberately malformed MNS-012 is not
reparsed or repaired.

Independent review must inspect semantics, sanitization, the local/public
boundary and the A1/supplied-counter qualification. If approved, a separate
final seal and local publication may supersede v2; record that approval in
the exported review record and manifest first. Current handoff counts,
coverage grades and compatibility status do not change at staging.
