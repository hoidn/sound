---
id: RES-SESSION-VIEW-WORKFLOWS
type: research
status: current
updated: 2026-10-19
access: analysis
revision: 3
target: Ableton Live 12 Suite 12.4.3
---

# Session grid and scene workflow evidence

This is the evidence owner for [Session workflow contracts](../specs/session-view-workflows.md)
under the [full specification plan](full-live-specification-plan.md). It reuses
the exact official Session chapter retained in the recording packet; no new
network capture, original execution or binary investigation was performed.

## Source and extraction

[Source metadata](../../analysis/ableton-live-12.4.3/full-spec-v1/session-workflows/source.json)
retains original URL/capture UTC,267328bytes and SHA-256
`16e29141f823e298d5fa7fee3b993861f6c38415f8432cd00ac89789e9470a31`.
The [extractor](../../analysis/ableton-live-12.4.3/full-spec-v1/session-workflows/capture.py)
reads only the chapter_content HTML element, producing77 paragraph/list/heading
blocks with exact HTML lines and heading anchors. It asserts the source digest,
chapter start/end and refuses changed derived-artifact overwrites. Figures and
image-based glyphs were not inspected. The cross-view source paragraph loses
two inline icon glyphs in text extraction; its other named copy/paste and separate
window gestures remain readable. No icon appearance or hit target is inferred.

## Scope and interpretation

The current R3 behavior owner contains30 requirements/57 finite proposed cases.
Its29 prior requirement records and40 prior case records remain verbatim. These
are partial documentary contracts, not complete gestures or a closed chapter.
All target outcomes are null/U/unexecuted. In particular:

- Scene controls' documented20-999BPM and meter domains do not replace the target
  storage/transport owner's traced numeric contracts. Text acceptance, clamping,
  clock rounding and timing remain U.
- Scene row numbers change with position; storage item identities are separate.
- Select Next Scene on Launch and Select on Launch are distinct settings. Current
  chapter defaults are documentation, not observed constructor preferences.
- The chapter's scene reorder paragraph names Ctrl without an OS qualifier; other
  import/selection paragraphs explicitly name Ctrl/Cmd. OS equivalence is unproven.
- General keyboard preferences and local edit traversal require explicit focus
  setup; shortcut labels alone do not prove dispatch priority.
- Capture and Insert Scene claims uninterrupted audio, but no signal/time
  comparator is supplied. Copied clips and visible launch state are separate.
- Session-to-Arrangement recording and override clauses remain in their existing
  canonicals. Retained scene-name tempo/meter recording language is not silently
  widened to all scene-field changes; exact-build applicability remains U.
- Follow Actions, clip launch scheduler, media decode and consolidation audio
  retain existing owners. No API, DSP, thread, buffer or candidate design follows
  from UI prose, file bytes or these cross-links.

## Packet and next evidence

[Finite future setups](../../analysis/ableton-live-12.4.3/full-spec-v1/session-workflows/fixtures.json)
name five scenes, audio/MIDI/group tracks, empty slots and independently valid
nonempty media/clips. Assets and a pre-Live11 migration Set are not yet retained;
no case may pass without its prerequisites. Twelve operational probes keep
boundary/malformed/undo/cancel/save/source-loss/transport/automation/teardown/rate/
focus/audio obligations open. Compound clauses need separate per-branch cases.

The [author seal](../../analysis/ableton-live-12.4.3/full-spec-v1/session-workflows/manifest-author-r3.json)
pins the current source routing, cases, tools and snapshots. Target-version
evidence and eventual calibrated outcomes remain unknown; separate review status
is explicitly as of the author freeze below.
No profile/family is complete; no release or compatibility approval is implied.

## Revision2 ownership correction

Independent Session review SV-REVIEW-001 found overlapping general metadata
semantics in SessionREQ004 and ClipViewREQ004/005. SessionREQ004 now owns only
Session entrypoints/selection dispatch and routes shared metadata behavior to
[Clip View](../specs/clip-view-workflows.md). The SV-004 action and SV-B015 source
remain unchanged; its documentary expectation is narrowed to the entrypoint.
All target oracles remain null/U. The exact12-payload prior revision and its seal
are retained under archive-r1. The retained
[final R2 review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/session-view-workflows-review-final.json)
approved its corrected partial scope; no later completeness is inferred.


## R3 retained-source audit adoption

The [full retained Session audit](../../analysis/ableton-live-12.4.3/full-spec-v1/session-grid-source-audit/README.md)
and its [separate partial review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/session-grid-source-audit-review.json)
read77 source blocks/142 facets versus29 clauses/40 actual actions, plus59 literal
resource records. That full retained-text accounting is not whole-source/product
closure; pixels and link destinations were not inspected. Current authoring read
all17 proposals, actual local contracts/actions and their selected external
predicates; it reuses exact immutable audit source/context providers. No capture.

One new source-supported clause names scene Cut/Copy/Paste/Duplicate Edit command
entrypoints (`SV-B060`), with no content-copy/clipboard-format/insertion law.
All29 old requirements and40 old case records are exact;15 source-backed cases
and2 U probes are appended. The current totals are30 clauses/57 cases,43 D12
source contexts/14 U probes,38 named-control documentary predicates/19 null
comparators; every actual expected/comparison is null/U/unexecuted.

The [disposition ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/session-workflows/audit-adoption-r3.json)
links all17 groups to exact new case pointers. G01-09/G11/G12/G15/G16 receive
bounded local contexts: nonsequential requests, explicit menu/selection/resize/
scene launch and setter gestures, assigned-color history, numeric-status
observations without numeric oracles, Stop-button Edit dispatch, scene Edit
commands, transfer/window entrypoints and positive consolidation eligibility.
Existing metadata, renameTab, move distinctions, launch-cancel, parameter and
productive stop cases remain represented subsets; no field or algorithm law is
changed. G10 Arrangement multi-file drop stays external-owner-pending; G13 named
clip-property recording stays pending with Recording/Automation/Clip View.
Actual AW004/005/006 changing-envelope/live-parameter/record-stop trials and
RecordingRC073/074/079 launch/return/scene-name histories are not declared missing.

G14 adds an ungraded Arrangement ClipStop/StopAll probe with actual nonempty
playing Arrangement/output prerequisites. Literal B074 wording is preserved,
not corrected from memory. G17 observes a bounded copied clip-field context;
no all-fields or unshared-source/file/device law follows. Both remain U-only.
Existing MixingR2 `MXW-U-GROUP-SLOT` `/45` already has genuinely playing child,
populated/empty and selection branches; its exact frozen source/context is
reused, not reauthored. SessionB017 and MixingB043 remain unresolved contexts.

A fresh known visibility/history precedes default/hidden inspection; explicit
modes/assignments precede launches; selected/playing/requested identities stay
separate. Positive admitted controls and genuine active/nonzero baselines precede
suppression/stop/no-effect/empty trials; missing/failed prerequisites remain U.
Counter/time, numeric assignment, consolidation files and unresolved stop/copy
contexts have null documentary comparators. No timing/audio/codec/RNG/pixel,
constructor, modifier alias, text grammar or updated finite launch/transport law.

[Exact delta](../../analysis/ableton-live-12.4.3/full-spec-v1/session-workflows/delta-r3.json),
[old-file preservation](../../analysis/ableton-live-12.4.3/full-spec-v1/session-workflows/prior-files-r3.json)
and [historical consumer inventory](../../analysis/ableton-live-12.4.3/full-spec-v1/session-workflows/consumer-impact-r3.json)
retain33 old files in place, including R1/R2 seals/reports/archive and exact-before
canonical snapshots.33 qualified old-hash occurrences across27 frozen consumer
files include archives/reviews/as-of providers, not27 active dependencies. No old
consumer/checker/adapter is run or changed. Current R3 checks own immutable
sources, exact append delta, pointers/nulls/prerequisites, snapshots and Browser
IDs. The old checks remain as-of their revisions; no blanket-green or new
historical resolver is required. All sources/providers remain immutable.

**AS-OF AUTHOR FREEZE:** R3 independent owner review is pending. Current
disposition routes via the [spec index](../specs/index.md) and independent review.
This author previously reviewed the source audit and authored adjacent workflows;
that does not self-approve this owner increment. Root supplies separate review
and all shared integration. No source/application/original/vendor/native/input/
audio/MIDI/hardware/network/installation/candidate operation was executed.
