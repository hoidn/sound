---
id: RESEARCH-LIVE-API-CLIP-SAMPLE
type: research
status: current
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3; current public API applicability U
---

# Clip and Simpler sample API evidence

The [canonical draft](../specs/live-api-clip-sample.md) is the first bounded
member-family reconciliation of the [reviewed53-source API inventory](sources/cycling74-live-api.md).
All379 text blocks of the selected five reference bodies were read: Clip214,
Clip.View20, Sample84, SimplerDevice55, SimplerDevice.View6. Raw retained HTML was
reparsed only for source/locator verification; no reference code was executed.
No recapture, figure, external help, patch, JavaScript or example inspection/run.

## Source identities and scope

[Sources](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-clip-sample/sources.json) preserves original URL/final URL, capture UTC, bytes,
SHA256, version and original retained paths; these are reused bytes, not new captures.
[Source blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-clip-sample/source-blocks.json) is an exact subset of inventory R1 blocks.
[External pins](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-clip-sample/external-pins.json) pins inventory R1 metadata/manifest,
original members/entries, all53-source index/blocks, selected raw pages/parser,
independent inventory/bridge review identity and existing owner/release manifests.
The validator verifies all53 retained source hashes but semantic reading was the
five selected references only. Source/index current12.4.5 is not target12.4.3.

## Documentary reconciliation

All131 direct members have a particular source-backed role and proposed case:
Clip77, Clip.View6, Sample28, SimplerDevice19, SimplerDevice.View1. No source entry
or direct member disappears from its denominator. All131 target outcomes and
all five profiles remain unresolved/partial; no member or class is complete.
Generic Device/Device.View inheritance is explicitly pending, not an invented
flattened API. A member being linked to an existing owner is not semantic proof.
All dictionary fields, public range/index/default notes and types remain exact
source data in member bodies; paraphrased clauses limit their authority to source
roles. Published numeric/message/event/signal/timing claims are never documentary
or target test oracles here. No sample tolerance or result comparator is invented.

## Source-context questions

- Q-LCS-001: Clip position lists get/observe while its prose describes setting
  loop position/preserving loop length. Preserve both; no new set capability.
- Q-LCS-002: Clip is_playing lists get/set without observe, despite the reporting
  role. Simpler playing_position_enabled lists get/observe, despite its name.
  Do not invent toggle/set/observer capabilities by analogy.
- Q-LCS-003: Sample gain_display_string is a function returning list of symbols;
  Clip gain_display_string is a get-only symbol property. Sample sample_rate is
  int; Clip sample_rate is float. Preserve declared differences, not native coercion.
- Q-LCS-004: Clip and Sample Warp mode lists differ at REX; Sample warp_markers
  does not repeat Clip's sample_time/beat_time schema. Existing finite Warp enums,
  marker edits/conversions/shadow rules remain their owner's evidence, not replaced.
- Q-LCS-005: Sample marker and slice function integer units/bounds are not stated
  by their member bodies. Slices property explicitly uses sample frames; do not
  silently transfer that unit to every integer signature or Clip beat marker.
- Q-LCS-006: Clip start_time's Session wording reports the currently playing clip
  on the track regardless of queried clip, unlike a simple per-object start cache.
  Context and negative positions require explicit fixtures and remain target-U.
- Q-LCS-007: Note dictionary APIs retain required/optional fields, valid-ID
  preconditions, field-selection forms and distinct missing-ID wording. Deselect's
  reference to replace_selected_notes does not add an undeclared member or restore
  older signatures. No storage-ID/API-ID identity, RNG or atomicity is inferred.
- Q-LCS-008: Omitted units/arguments/returns and Clip.View grid enum stay unknown.
  Source access prose is not a complete refusal or error protocol. Return snippets
  in the ledger include full mixed paragraphs for faithful context, not parsed ABI.
- Q-LCS-009: Warp deferral/sequence warning describes possible externally noticed
  ordering surprises only, not threads, event loops, latency or internal design.
  Sample warping does not inherit this warning as a guaranteed behavior.
- Q-LCS-010: Simpler can_warp flags need independent available-feature baselines;
  mode, multisample, voice, retrigger, crop/reverse/replacement and sample lifecycle
  supply no algorithm, media transaction, voice allocator or signal prediction.
- Q-LCS-011: Inherited Device and Device.View members/canonical reachability await
  generic member-family work; five profiles are not full inherited member coverage.
- Q-LCS-012: Exact target applicability, malformed/refusal, read-only/observe,
  deleted/missing IDs, dictionaries, region equality, tuning/dependencies,
  cancel/undo/persistence/reorder/transport/rate/teardown all remain U. A failed or
  unavailable prerequisite cannot pass a proposed negative case.

Root owns integration into shared catalogs/questions/coverage/log. This packet
contains no implementation, release, reference execution or compatibility result.
