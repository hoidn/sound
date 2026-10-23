# Manual citation crosswalk, revision 4: first four-packet cohort

This is an additive navigation/audit artifact. It joins retained documentary
citations to the original manual TOC; it does not establish behavioral coverage,
whole-clause support, target applicability or completed topics. The
[existing F01–F10 plan](../../../../../wiki/research/full-live-specification-plan.md)
remains the sole work selector. There is no new queue or passed percentage.

The finite cohort is exactly these independently reviewed author R1 packets:

| Packet | Requirements | Cases | Source blocks | Independent review |
| --- | ---: | ---: | ---: | --- |
| video-workflows | 18 (16 D12/2 U) | 28 | 39 | [Partial review](../../reviews/video-workflows-review.json) |
| synchronization | 26 (24 D12/2 U) | 36 | 54 | [Partial review](../../reviews/synchronization-workflows-review.json) |
| settings-learning | 21 (19 D12/2 U) | 30 | 70 | [Partial review](../../reviews/settings-learning-workflows-review.json) |
| stem-separation | 18 (15 D12/3 U) | 29 | 32 | [Partial review](../../reviews/stem-separation-review.json) |

Totals are83 requirements (74 D12/9 U),123 cases and195 source blocks. This195
is only the four listed chapters, not the separate engine packet. Other packets,
released contracts, devices and controller inventories are outside this cohort.
Their absence here does not mean they lack evidence or an owner.

## Exact join and retained limits

[Inputs](inputs.json) pins72 existing files: the four complete author payload
sets and manifests, independent reviews, matching canonical spec/research pages,
the packets' external parser dependency, and the original TOC/HTML/manifest.
Reviewed manifest identities, source capture UTC/bytes/hashes and exact source
block anchors/HTML lines are retained. No original product or source validator
was rerun; no source prose was reclassified or independently re-reviewed here.

For each D12 requirement evidence record, the join key is literally its
`source.json.url + "#" + evidence.anchor`, compared with the original TOC URL.
The evidence block must have exactly that anchor and HTML line. There is no URL
normalization, title similarity, section-parent inference or automatic alias.
Every citation links its requirement catalog/JSON position, exact block/catalog/
source identity and all cases referencing that requirement, including each case's
kind, catalog/JSON position and original null/U/unexecuted target-oracle status.
Documentary-oracle null flags describe the existing cases; they are not new
acceptance criteria or claims that visible-control proposals were executed.

- [Topic citations](topic-citations.json) retains all880 original topic rows in
  original order, including708 leaves across43 chapters. Original fields remain
  exact discovery-time data, including their `specification` and `complete` fields.
  New fields explicitly keep full semantic coverage/completion unknown and target
  applicability U. A citation status only means a partial reviewed draft cites
  that exact source anchor; it supplies no complete topic or leaf disposition.
- There are111 matched requirement/evidence citations on27 topics:22 leaves and5
  nonleaves. The other853 topics remain visible without a citation in this cohort.
  These are citation counts, not counts of fully supported clauses or topics.
- [Unmatched citations](unmatched-citations.json) retains8 evidence references at
  three exact URLs absent from the original TOC: video `movies-with-partial-tracks`,
  video `warp-markers`, and synchronization `midi-timecode-options`. They are not
  attached to nearby/parent headings. No post-target, typo or alias disposition
  is inferred; the retained source and unmatched URL remain reviewable.
- [Unbacked requirements](unbacked-requirements.json) retains all9 U requirements
  without evidence and all their referencing cases. `source:null` means no source
  was invented for those clauses; the chapter capture is not borrowed as proof.
- 69 requirements have at least one matching citation,5 have only unmatched
  citations, and9 lack evidence. Video requirement013 has both matched and
  unmatched citations, so the unmatched ledger is not disjoint from matched
  requirements. The union reconciles all83 requirement IDs and123 case IDs.

[Summary](summary.json) retains the separate counts and explicitly claims zero
complete topics. Current Version12 documentation remains version-uncertain for
12.4.3; reviewed documentary clauses do not make compatibility results.
Welcome, Concepts, Credits, missing-owner topics and all other source rows remain
in the unchanged original denominator. The prior routing companion is not
overwritten, and no canonical inventory/wiki/shared files are edited.

## Reproduce without mutation

Inspect [derive.py](derive.py), then run:

```sh
python3 -B analysis/ableton-live-12.4.3/full-spec-v1/inventory-revisions/r4-citation-crosswalk/derive.py --check
```

`--check` verifies pinned input/manifest/source/review/canonical identities,
evidence locators, exact URL joins, ID/case unions, null target oracles, all880
original rows, deterministic output bytes and untracked-aware whitespace. It
writes nothing. Omitting the flag is an author-only first-creation operation;
it refuses to run once [manifest.json](manifest.json) exists. Revisions require a
new artifact rather than rewriting frozen bytes. The manifest freezes the seven
payloads for separate independent audit review, not behavioral release.
