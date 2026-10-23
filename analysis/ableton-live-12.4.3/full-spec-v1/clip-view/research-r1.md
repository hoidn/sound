---
id: RES-CLIP-VIEW-WORKFLOWS
type: research
status: current
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3
---

# Shared Clip View and audio property evidence

## Scope and source selection

This partial F-04 analyst packet routes shared Clip View UI and unowned audio
properties to [the canonical draft](../specs/clip-view-workflows.md).
[Full coverage design](full-live-specification-design.md) governs closure.
The [inventory TOC](../../analysis/ableton-live-12.4.3/full-spec-v1/inventory/manual-toc.json)
selects the exact official `/en/live-manual/12/clip-view/` chapter URL; no prior
Clip View HTML capture was found in the active packets. The chapter was retained
once; no original program, external editor, hardware or candidate was run.

[Source metadata](../../analysis/ableton-live-12.4.3/full-spec-v1/clip-view/source.json) identifies official Version12 HTML,
capture UTC and URLs,306606 bytes, SHA-256
`30f156e6d83c8f4caf3fe9dcf55bb2b764dc42ed8cbd3847863a53747851bd80`.
No patch-level publication revision is available: all exact12.4.3 runtime
applicability remains U. The [180 block view](../../analysis/ableton-live-12.4.3/full-spec-v1/clip-view/manual-blocks.json)
retains paragraph text, source HTML lines and full numbered heading context.
The extractor stops at sidebar navigation, so unrelated TOC entries are not
miscounted as chapter behavior. HTML bytes are preserved; normalized text and
JSON are analyst navigation artifacts. Figures were not inspected separately.

## Canonical ownership and source interpretation

The canonical spec owns46 D12 requirements and8 required-U obligations, with62
finite unexecuted cases. Documentary visible-state proposals have explicit
comparators; timing/signal obligations and every exact-target oracle remain null.
No media fixture/reference render was fabricated. Future owned A/B/C media and
MIDI M must be retained independently before any action can be evaluated.

Shared clip selection, fields/panels, regions, looping/scrub gestures, multiclip
properties and audio-specific source actions are distinct from MIDI note/MPE
editing or global note/time serialization. The
[source-routing view](../../analysis/ableton-live-12.4.3/full-spec-v1/clip-view/source-routing.json) routes the chapter's
neighboring MIDI tools, groove and launch prose to their existing owners, not
to duplicated requirements. [MIDI editing](midi-editing-tools.md),
[MPE](mpe-tuning-grooves.md), [media](media-file-workflows.md) and
[clip launch](clip-launch.md) retain narrower evidence. Detailed Warp processing
and full Session/Follow Actions still require separate packets.

Specific predicates preserved in the draft/cases include audio Warp as Loop
eligibility; Session-only Fade toggle versus Arrangement envelopes; independent
clip/project meter; source-relative marker/region reversal versus unchanged
clip envelope time; equal-length source replacement/edit marker retention;
Temporary versus saved Project paths for new Crop/Reverse media; separate launch
quantization and Clip Update Rate; and mixed-value endpoint unification. These
are documentary relationships, not observed control law or DSP equivalence.

New source context requiring later reconciliation belongs to the MIDI owner:
CV:B126 §8.5.2 half-grid Humanize prose versus existing quarter-grid per direction
may concern total width versus one-sided displacement. CV:B122 Interval Size and
Add Interval button versus immediate-slider prose may depend on the gesture.
CV-U-MIDI-UTILITIES keeps both contexts open rather than declaring contradiction
or copying either as a new normative law. The source HTML at respective lines
720 and708 supplies exact current capture locators.

Clip meter display-only `CV:B059-B060` does not invalidate a distinct stored
follow-time normalization using clip meter in the launch owner. Scrub and Set
button prose does not establish that launch-grid rounding code runs for those
gestures. Hi-Q19-semitone/CPU claims are qualitative/conditional, not measurable
bounds. Fade0-4ms is documentary only; exact kernel stays with existing audio
owners and remains unproven outside their finite released scope.

## Remaining required evidence

Exact-build version parity, source/frame/time codecs, reverse/crop marker
arithmetic, scrub/region/update scheduling, gain/pitch/interpolation/fade audio,
program-message numbering/order, full shared-source/default/multi-selection
matrix, undo/persistence/cancel/malformed/error/teardown/resource behavior,
platform focus/accessibility and complete settings precedence remain U.
No absent original/candidate evidence is labelled pass or inapplicable.

## Freeze and review

[Manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/clip-view/manifest-author-r1.json) freezes exact payloads/canonical
snapshots plus the inventory TOC source. Run
`python3 analysis/ableton-live-12.4.3/full-spec-v1/clip-view/validate.py` for focused
hash, source locator, case, local link, metadata and untracked-aware whitespace
checks. [Validation](../../analysis/ableton-live-12.4.3/full-spec-v1/clip-view/validation-author-r1.json) does not establish
behavior. Root alone owns shared catalogs, coverage, questions, plan and log.
Separate semantic review is pending; no handoff or implementation scope is changed.
