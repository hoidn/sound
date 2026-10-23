# Manual citation crosswalk R6: second bounded cohort

Navigation/audit only. This adds no behavioral coverage, applicability, semantic
support or completed topic. The [existing F01–F10 plan](../../../../../wiki/research/full-live-specification-plan.md)
remains the sole work selector. R4 is pinned intact, not merged or replaced.

| Reviewed packet | Requirements D12/U | Cases | Source blocks |
| --- | ---: | ---: | ---: |
| Push1/2 workflows | 53/12 | 77 | 706 |
| Engine/resources | 13/15 | 50 | 195 |
| Browser content/services | 50/6 | 71 | 274 |
| Application workspace | 9/4 | 23 | 125 |

The cohort has162 requirements (125D12/37U),221 cases and1300 packet-scoped
source blocks in eight retained source records. The195 engine blocks differ
from R4's195-block first cohort. Other packets, APIs/releases, Push3 Standalone,
controller profiles and online-service compatibility are outside this cohort.

[Inputs](inputs.json) pins148 existing files: original TOC/HTML/manifest, all
R4 payloads/seal and its navigation review, four current reviewed author manifests,
all their payloads, independent reviews, matching canonical snapshots, raw source
bytes and existing external inputs. Source URL/version/UTC/hash metadata is retained
without recapture or identity substitution. Browser's older Concepts capture and
the newer workspace capture remain distinct despite sharing a chapter URL.
No source validators, source claims, product, service or candidate were rerun.

## Literal join and explicit gaps

[Topic citations](topic-citations.json) preserves all880 original rows/IDs/order,
708 leaves and43 chapters, including original discovery metadata. Its new fields
keep full semantic coverage/completion unknown and target applicability U.
Only literal source `url + "#" + block.anchor` matches join an original TOC URL.
No URL normalization, title matching, parent/heading inference or aliases apply.
A match means a partial reviewed draft cites that anchor, not leaf completion,
whole-clause support, a tested output, or a new owner/work queue.

There are290 matched requirement/source citations on62 topics (55leaves/7nonleaves).
Of those citations192 belong to D12 requirements;98 are explicitly **U source
context**, from15 engine requirements. D12 requirements cite36topics/31leaves;
33topics/30leaves have U context, and26topics have only U context. These are audit
counts, never partial/complete behavioral-coverage counts. The other818 original
topics remain visible without a citation in this cohort. Zero topics are complete.

[Unmatched citations](unmatched-citations.json) retains376 references:

- All330 cited Push blocks have direct `anchor:null`. Their original
  `heading_context` ancestors remain context only; none is inherited or joined.
- Another46 Browser references have nonnull direct anchors at14 exact URLs absent
  from the original TOC. The summary lists every URL; no parent, typo, alias or
  newer-version disposition is guessed.

77requirements have exact matches;63 have only unmatched references; three of
the matched requirements also have unmatched references. [Unbacked requirements](unbacked-requirements.json)
retains22 U clauses without source references. No chapter is borrowed as their
proof. The union reconciles all162 requirements and all221 referencing cases.

[Case index](case-index.json) separately retains every case's packet-qualified
ID/catalog/JSON pointer, kind, original provenance-field presence/value, requirement
pointers, original evidence/reference pointers and source identities. All851 case
source references remain explicit (475exact matches/330null anchors/46unmatched
URLs); none introduces a block outside its linked requirements.59cases have no
source references. Existing documentary roles/null flags remain exact:69cases have
nonnull documentary proposals and152 have null documentary expectations. Every
target expected/comparison remains null, grade U and executed:false. These flags
are publication data, never fresh acceptance criteria or observed product results.

## Read-only reproduction

Inspect [derive.py](derive.py), then run:

```sh
python3 -B analysis/ableton-live-12.4.3/full-spec-v1/inventory-revisions/r6-citation-crosswalk/derive.py --check
```

It verifies148 input pins/review identities/source bytes, original880-row identity,
all clause/case/block IDs and pointers, literal joins/null-anchor boundaries,
source-capture distinction, retained provenance/oracle flags, deterministic outputs,
manifest and untracked-aware whitespace. It writes nothing. Omitting `--check`
is first-author creation only and refuses once the manifest exists. A revision
requires a new artifact. Independent navigation review remains required.
