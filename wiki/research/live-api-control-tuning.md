---
id: RESEARCH-LIVE-API-CONTROL-TUNING
type: research
status: current
updated: 2026-10-19
access: analysis
revision: 2
target: Ableton Live 12 Suite 12.4.3; current public API applicability U
---

# Public API control and tuning source contexts

The [partial draft](../specs/live-api-control-tuning.md) follows the
[coverage design](full-live-specification-design.md) and [plan](full-live-specification-plan.md).
Root read every retained block for ControlSurface, DeviceIO, Groove, GroovePool,
TuningSystem and this_device. Sources are unchanged reviewed R1 captures;
no recapture, example execution or API/hardware/application/candidate operation.

## Denominator and provenance

Six exact entries expose28 direct declarations: ControlSurface10,DeviceIO5,
Groove6,GroovePool1,TuningSystem6,this_device0. All28 receive a source-specific
partial documentary contract and action; none is semantically complete. The zero-
member root gets a distinct context contract. Four U groups add12 probes, giving
33 requirements/41 cases, all actual documentary/target outputs/comparators null.
The source index states12.4.5, not target12.4.3; published since-version labels
are retained as source claims without proving this runtime or complete support.

[Sources](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-control-tuning/sources.json),
[blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-control-tuning/source-blocks.json),
[direct-member ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-control-tuning/member-ledger.json),
[requirements](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-control-tuning/requirements.json)
and [cases](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-control-tuning/cases.json)
retain exact locators and action linkage. Owner pins preserve the existing
bridge/remote/Push/routing/rack/groove/tuning/MIDI/notes context. No finite law,
released payload or reference source is revised by adding this packet.

## Source-context questions

- LAC-U-CONTROL: ControlSurface B0002 explicitly distinguishes root-path order
  from Application listing. B0029–0030 timeout annotation int versus prose float
  lacks a unit. Script requests versus realtime track forwarding and ownership/
  disconnect cleanup remain context-dependent; no protocol or timing tolerance.
- LAC-U-ROUTING: DeviceIO dictionaries name display_name/identifier and availability
  wrapper keys, but do not define serialization, stable identity, bus cardinality,
  stale/type-channel fallback or real audio routing. Printed bool1 none-default is
  not a complete current-selection or persistence law.
- LAC-U-GROOVE: six primitive declarations are printed under Children; retain
  category and capabilities without assuming object navigation. Amount units,
  ranges, RNG/quantization/timing/velocity algorithms and pool mutation remain U.
- LAC-U-TUNING: dictionary keys, ordering, range/reference conventions and no-system
  behavior remain missing. A single-element dictionary of cents array is not a
  supplied schema or frequency conversion; existing scale/tuning owners retain laws.

The this_device reference uses a Device root description plus ordinary canonical
path example. No restriction to top-level tracks, inherited member closure or
identity lifetime follows. The broader bridge root-omission question remains open.

## Author freeze and checks

[Author manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-control-tuning/manifest-author-r2.json)
pins source catalogs/blocks, per-member data/actions/ledger, owner/inventory pins,
author script, read-only validator and exact spec/research snapshots. Validation
reproduces source sections from unchanged inventory data, checks original R1
payload hashes, exact28-member set/33 browser IDs/41 null cases, links and whitespace.
A pass establishes author integrity only; independent semantic review is required.

## Preserved R1 and focused correction

The [initial independent review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/live-api-control-tuning-review.json)
required LAC-REVIEW-001/002: restrict the explicit-request caveat to engine channel
messages and state that matching surface order is not guaranteed. R1 payloads,
manifest and freeze remain byte-exact in archive-r1. R2 changes only those two
contract/source-claim phrases and successor metadata/snapshots; cases/actions,
counts, source bytes and all null outcomes remain unchanged. Independent focused
review is pending; no behavioral or target completion follows from the correction.
