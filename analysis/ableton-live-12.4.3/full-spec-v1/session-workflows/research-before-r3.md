---
id: RES-SESSION-VIEW-WORKFLOWS
type: research
status: current
updated: 2026-10-19
access: analysis
revision: 2
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

The behavior owner contains29 requirements/40 finite proposed cases. These are
partial documentary contracts, not28 closed gestures or a complete chapter.
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

The [author seal](../../analysis/ableton-live-12.4.3/full-spec-v1/session-workflows/manifest-author-r2.json)
pins this source routing, cases, tools and canonical snapshots. Separate semantic
review, target-version evidence and eventual calibrated outcomes remain pending.
No profile/family is complete; no release or compatibility approval is implied.

## Revision2 ownership correction

Independent Session review SV-REVIEW-001 found overlapping general metadata
semantics in SessionREQ004 and ClipViewREQ004/005. SessionREQ004 now owns only
Session entrypoints/selection dispatch and routes shared metadata behavior to
[Clip View](../specs/clip-view-workflows.md). The SV-004 action and SV-B015 source
remain unchanged; its documentary expectation is narrowed to the entrypoint.
All target oracles remain null/U. The exact12-payload prior revision and its seal
are retained under archive-r1; revision2 awaits focused independent re-review.
