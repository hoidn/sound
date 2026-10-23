---
id: PLAN-MIDI-NOTE-STORAGE-V4-HANDOFF
type: research
status: current
updated: 2026-10-20
access: analysis
target: Ableton Live 12 Suite 12.4.3 / macOS arm64
---

# Fourth MIDI note storage handoff: two local reader comparisons

## Current local publication — 2026-10-20

[MIDI note storage v4](../../handoff/midi-note-storage-v4/README.md) is locally
released, superseding v3. Manifest `1d0cc553a37d95e25b66dad0f5048af8fc79349d9663b184228fac1d0ab24800`,24,458bytes/83payloads223,995bytes/all84files exact.
[Content approval](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/midi-note-storage-v4-content-review.json)
and the separate [final exact-tree seal](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/midi-note-storage-v4-final-exact-tree-review.json)
approve the staged finite content and metadata successor respectively.
[Full prerelease lint v61](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/documentation-lint-2026-10-20-v61-pre-midi4.json)
passed262pages/35preexistingreleases/2,216payloads/1,306HEADimmutable files.
[Exact copy receipt](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/midi-note-storage-v4-local-copy-receipt.json)
records the destination verification before catalog adoption; the catalog now
records actual publication. Original candidate/final/analyst stages remain
immutable. Publication metadata was not rewritten after sealing.

All78oldobjects/78gzip/14oldbodies are exact; two local projections add no
public load/catch/rollback/save result.80cases/15partialIDs are package units,
not a complete family or compatibility fraction. No original/candidate
execution, restricted-workspace synchronization or implementation occurred.
The following staging disposition is dated author history, superseded here.

## Staging disposition — historical

**Staged candidate; independent handoff review pending; unpublished.** The current
[midi-note-storage-v3](../../handoff/midi-note-storage-v3/README.md) release remains
immutable. This task creates no release directory or catalog change. The
[candidate payload](../../analysis/ableton-live-12.4.3/handoff-staging/midi-note-storage-v4/README.md),
[manifest](../../analysis/ableton-live-12.4.3/handoff-staging/midi-note-storage-v4/manifest.json),
[author check](../../analysis/ableton-live-12.4.3/handoff-staging/midi-note-storage-v4-analysis/author-validation.json)
and [analyst traceability](../../analysis/ableton-live-12.4.3/handoff-staging/midi-note-storage-v4-analysis/traceability.json)
are for a separate review under the [release workflow](../workflows.md#release-a-handoff).

Independent content approval, an external exact-tree seal and coordinator full
prerelease lint precede any local publication. The final attestation stays outside
the payload. Supporting source/owner approvals are not handoff approval. A future
metadata successor must preserve all cases, fixture bytes and selected clauses.

## Selection and provenance

Select only the approved r6 local comparisons MNS-076/077 from the
[canonical MIDI draft](midi-note-storage.md#r6-owner-approval--2026-10-20).
The [independent owner review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/midi-storage-remaining-u-owner-r6-review.json),
SHA256 `492476f9376b1f2ff2e8f558b30d3fedae4bca828136e3d717a2aa15a7d8ab84`,
and [root adoption](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/midi-storage-remaining-u-owner-r6-root-adoption.json)
approve the exact 72,839-byte owner prefix, SHA256
`593e10be4054180173c09d8c7fd30bbf84535877dccb9c4de34133f27dec2d73`.
The current 74,118-byte as-of draft includes the additive approval disposition,
SHA256 `62ef96d4cf57a60f93358a5a3be24a5a74ab4d751ffd101cc22220da0c70cd9a`.
Both identities are pinned without copying a spec snapshot.

The [approved remaining-U source review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/depth-midi-storage-remaining-u-v1-review.json)
supports the local parser/list rules. Its bounded source packet is pinned in
[analyst inputs](../../analysis/ableton-live-12.4.3/handoff-staging/midi-note-storage-v4-analysis/pins.json).
The concurrently authored expression-source frontier is not ingested here.
No expression boundary result, source structure or internal native identifier
enters the exported contract.

## Exact scope and inputs

V4 carries all 78 v3 case objects, all 78 gzip fixture files and all 14 selected
requirement bodies verbatim. It adds exactly two local case objects and one new
partial requirement ID, 012. The 002 mixed-space rule is a separate supplement so
its old body and public no-expectation table remain exact. There are 80 case
records, 78 fixture files and 15 partial requirement IDs; these are package units,
not a full-family outcome denominator or compatibility fraction.

| Case | Existing authored input | Exact decoded Notes edit | Comparison |
| --- | --- | --- | --- |
| MNS-076 | v3 MNS-001 fixture | n3 NoteId becomes U+0020, digit 7, U+0020 | Conditional local reader refused |
| MNS-077 | v3 MNS-001 fixture | Both KeyTrack Id attributes become 5 | Conditional local reader refused |

Each new record names `fixtures/MNS-001.als` and has an explicit `input_projection`
over its decoded `MidiClip/Notes`. Relative element paths and one-based indices
identify the exact attribute edits. No new fixture, full Set carrier, compression,
shipped-content transplant or binary generation is necessary. Data-only checks
verify that one NoteId attribute or two Id attributes change and all other input
content remains unchanged. They compute no reader expectation.

Both cases use `validate-notes` and only `local_reader_outcome=refused`. These
are project comparison labels over domain input, not a required public validation
API, native invocation, reader entry point or implementation pipeline. An independent
implementation may validate anywhere suitable. The sanitized clause omits internal
construction ordering; it contracts only bounded local refusal.

Conditional current field/list associations, the ordinary reader context and A3
integer-field binding remain premises. A1 governs the inherited post-read group
checks; it does not gate the new read-phase refusals or prove public lifecycle.
A2 is the separate same-state Save assumption and supplies no saved result here.

## Preserved unknowns and boundaries

Original public MNS-011/038 remain unreleased; no new public Open/refusal,
catch, UI, loaded state, rollback, saved Id identity or Id meaning is judged.
All four MNS-053 expression variants remain unknown. Group final Save, later
missing-note effects, whole-load counter mutation/ordering and unsupported
enum/playback meanings remain unknown. Unsafe MNS-037 keeps zero required
safe-refusal outcomes. Negative-counter and other input exclusions remain.
The 72 legacy public comparisons, six carried local group comparisons and
all extracted-execution clauses retain their exact content and limitations.

## Checks and remaining gate

The new [read-only stdlib checker](../../analysis/ableton-live-12.4.3/handoff-staging/midi-note-storage-v4-analysis/check.py)
checks exact predecessor payloads, all carried object/fixture/body bytes, gzip
member/CRC/size integrity, both input projections, source/owner pins, isolated
package links, sanitization, candidate inventory and meaningful negative controls.
The deliberately malformed carried MNS-012 XML is not reparsed or repaired.
Predecessor schema/structure review is inherited through exact fixture bytes;
no old builder, collector, schema helper or other script is imported or run.

Only stdlib file/JSON/gzip/XML input-data operations occur. No original or
candidate program, native/provider/binary/decoder/harness/model/comparator/build
execution, reference behavior observation or new compatibility grade occurs.
The analyst sibling is outside the package and must never be copied as a handoff.
The coordinator owns shared index/log routing and full prerelease lint.


## Postpublication check — 2026-10-20

[Destination/catalog and16changed-page checks](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/midi-note-storage-v4-publication-incremental-check.json)
passed at23:06UTC:83newpayloads/all84destination files exact,36releases/19current/
17superseded,r6reviewedprefix/logprefix preserved,no newlinks/differrors. Older
check reports retain their as-of scopes; this is not a runtime compatibility pass.
