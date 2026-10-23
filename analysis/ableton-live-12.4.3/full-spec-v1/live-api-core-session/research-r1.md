---
id: RESEARCH-LIVE-API-CORE-SESSION
type: research
status: draft
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3; public LOM index 12.4.5 applicability U
---

# Public LOM core and Session member mapping

## Evidence and method

The [canonical draft](../specs/live-api-core-session.md) maps 226 direct
declarations, not complete classes. Reused unchanged immutable [R1 inventory
manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/max-api/manifest-inventory-r1.json)
SHA67e24da58fb1d91d8c55659c65eb0779a3c3e8cc2424ddcf07915032d8637a73.
No recapture or mutable source-family canonical pin. All65 R1 payload hashes
are checked. Ten exact class sources retain original URL, UTC, bytes and SHA
in [sources](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/sources.json); HTML remains at its immutable
original location. The source index says Live12.4.5, not target12.4.3. Source
paragraphs/headers/access declarations were read as data. No scripts/examples,
API/Max/native/original/candidate, hardware or patch were executed.

All 659 retained class blocks are
present in [source blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json) and text with
HTML line/column locations. The original pinned article-only extractor checks
these against exact HTML bytes; sidebar/reference links do not add declarations.
Member spans start at the exact h3 and stop before the next h2/h3. Class context
is retained through B0002 and canonical path B0004. Type/access comes from the heading/access
paragraph; manual argument names/order/type and explicit result annotations
come from each actual member description. Unannotated signatures stay null;
the original function paragraph is preserved so the ledger is auditable.
Copied publisher prose supplies source_claim, never a numerical/API oracle.

## Denominator and remaining work

Global inventory45entries/588direct declarations remains unchanged. Selected
ten entries226members are mapped to226D-current-public clauses and finite
member cases; 8U requirements retain cross-cutting gaps. Remaining outside
family35entries/362members are unmapped here. Every226member has explicit U
flags and complete:false; target-applicable/complete member and class counts
are zero. Inherited/root/alias members are not flattened or assumed absent.
Full per-member branches/errors/argument/result grammars and lifecycle remain
required; mapping every source heading does not complete behavior.

## Source context questions

| Local question | Exact source context | Retained unknown |
| --- | --- | --- |
| Q-LCS-001 | Application.View B0014, B0022, B0028 | available_main_views/scroll use Arranger but zoom uses Arrangement. Empty view-name typography also differs. No alias/empty quoting normalization. |
| Q-LCS-002 | ClipSlot B0030/B0033/B0039 | is_playing/recording predicates and status2 description overlaps status1 by saying playing or recording. Preserve wording; no numeric status precedence inferred. |
| Q-LCS-003 | Track B0148; ClipSlot B0044/B0046 | MIDI-create paragraph refers to ClipSlot.create_clip for audio in Session. Preserve apparent cross-reference wording issue; do not adopt MIDI function as audio creator. |
| Q-LCS-004 | Track B0016; Song B0018; bridge owner | devices includes mixer prose and master_track API name cannot overwrite installed device topology or Main storage/native names; aliases and reflection closure U. |
| Q-LCS-005 | Song.View B0014/B0015/B0018; Track B0078 | Push3-only modulation context and Push implicit arm are not generic or Push1/2 capability. Actual firmware/hardware and API target availability U. |
| Q-LCS-006 | Track B0096/B0160; Song B0024 | future fix language, insert_device since12.3 and groove since11 do not establish exact12.4.3 semantics; chronology/current-source conflict U. |
| Q-LCS-007 | Track B0146/B0148; TakeLane B0015/B0017; ClipSlot B0045 | Prints versus throws, audio path/platform wording, insertion into take-lane versus Arrangement, range/length/error distinctions remain context-specific; no universal exception or rollback protocol. |
| Q-LCS-008 | Application.View B0024; unannotated function headings/access-only members | show_view only lists view_name. Missing behavior/type/optionality/return prose remains missing, not filled from names or memory. |
| Q-LCS-009 | Song B0055/B0103/B0133/B0167/B0170; Scene B0026–B0038; Track meter blocks | Source numeric enums/ranges/sentinels/meter words do not overwrite finite stored/native values or supply wire/message/signal/timing comparators. |

## Review and freeze

[Requirements](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/requirements.json), [cases](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json),
[typed member ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json), [denominator](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/denominator.json),
[future prerequisites](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/fixtures.json) and [counts](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/counts.json)
are sealed with both canonical snapshots. Twenty-three canonical owner pins
plus browser-parser pin keep ownership visible; seven immutable inventory pins
avoid mutable source-family revision changes. The validator checks all65original
R1 payloads, ten source/block identities, member spans/signatures/IDs, exact
browser requirement equality, links, whitespace and snapshots without writes.
Independent review pending; no semantic/runtime or complete-API approval.
