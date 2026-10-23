---
id: SPEC-VIDEO-WORKFLOWS
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 2
target: Ableton Live 12 Suite 12.4.3
---

# Video import, presentation and scoring workflows

This partial F-07 contract owns video-specific import/presentation, movie-to-audio
processing boundaries, scoring/marker feedback and pre-roll editing. The
[coverage design](../research/full-live-specification-design.md) governs closure;
[research](../research/video-workflows.md) owns exact evidence and interpretation.
It is not a complete video/codec specification or a released implementation input.

**D12/target-U:** the official Version12 chapter captured2026-10-19 supports
documentary prose only. Every exact12.4.3 outcome/comparison is null/U/unexecuted.
Figures were not inspected; there are no movie/frame/audio reference fixtures,
codec proofs, pixel/signal/time tolerances, runtime runs or candidate results.
U never passes. Missing assets/decoder/display capabilities remain prerequisites.

[Media](media-file-workflows.md) owns general source/cache behavior;
[Arrangement](arrangement-editing.md) and [Clip View](clip-view-workflows.md) own
generic clip editing and audio processing. This page adds only video-specific
predicates; video replacement does not change their audio algorithms. [Warp](warp-markers.md)
owns marker storage/finite conversion; its broader tempo-leader/algorithm scope
remains open. Leader selection here is only the captured video setup's documented
role, without a tempo-map or frame scheduler law. [Export](audio-video-export.md)
owns render ranges/options/encoding/errors, [project/media](project-media-workflows.md)
owns general relinking, and [keyboard navigation](keyboard-navigation.md) owns
global focus/Tab settings. The chapter's generic Tab/view instructions are routed
there rather than repeated without their preference conditions. External video
synchronization remains a separate pending contract.

R2 minimally adopts the [independently reviewed source audit](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/video-source-audit-review.json).
All eighteen R1 clauses remain verbatim. Two bounded roles add movie-drop window
appearance and Arrangement waveform feedback, distinct from Video Window frame
feedback. [Audit adoption](../../analysis/ableton-live-12.4.3/full-spec-v1/video-workflows/audit-adoption-r2.json)
records nine groups; no default, frame, tempo, codec or numerical law is added.

## Requirements

Use [R2 future owned setups](../../analysis/ableton-live-12.4.3/full-spec-v1/video-workflows/fixtures-r2.json).
First establish actual accepted movie/decoder/display capability, visible productive
video and nonmuted/nonzero audio/output. Absent source/stream, hidden window,
failed decoder or zero signal is U, never a passing gap/absence case. Complete
partial-track intervals and truncated/partial movies remain distinct contexts.

### REQ-VIDEO-WORKFLOW-001 — Movie import

**D12/target-U.** The current manual documents .mov QuickTime movies appearing in Browser and drag import into a Set. This is not a complete accepted extension/container/codec profile, OS entitlement or a rejection rule for other formats.

Evidence: `VID-B006`; [exact source routes](#analysis-only-evidence).

### REQ-VIDEO-WORKFLOW-002 — Arrangement versus Session

**D12/target-U.** Video display is documented for movie clips in Arrangement. A movie placed in Session is treated as an audio clip. Audio-only Session treatment does not specify source-file rewriting or the behavior of a simultaneous Arrangement movie.

Evidence: `VID-B007`; [exact source routes](#analysis-only-evidence).

### REQ-VIDEO-WORKFLOW-003 — Video title indication

**D12/target-U.** An Arrangement video clip is described with sprocket-hole markings in its title bar. Pixel geometry, asset, color, scale and accessible description are unknown; the source figure was not inspected.

Evidence: `VID-B010`; [exact source routes](#analysis-only-evidence).

### REQ-VIDEO-WORKFLOW-004 — Edge trimming

**D12/target-U.** Dragging the left or right Arrangement clip edge trims the video clip. The underlying audio/Arrangement edge-edit contract remains in SPEC-ARRANGEMENT-EDITING; frame/sample rounding, bounds and audio-video boundary alignment are unknown.

Evidence: `VID-B011`; [exact source routes](#analysis-only-evidence).

### REQ-VIDEO-WORKFLOW-005 — Audio-only results of processing commands

**D12/target-U.** Consolidate, Reverse and Crop applied to a video clip replace it with an audio clip without altering the original movie file. This is a video-retention boundary, not a new audio processing/codec law. General command semantics remain with Arrangement and Clip View.

Evidence: `VID-B011`; [exact source routes](#analysis-only-evidence).

### REQ-VIDEO-WORKFLOW-006 — Floating Video Window

**D12/target-U.** Video Window floats above Live's main window, can be moved, and has a visibility command in View. The text does not promise priority over other applications, OS dialogs or all display configurations.

Evidence: `VID-B013`; [exact source routes](#analysis-only-evidence).

### REQ-VIDEO-WORKFLOW-007 — Window size and location retention

**D12/target-U.** Dragging the bottom-right Video Window corner resizes it. Its size/location are not Set-specific and are described as restored when a video is opened again. Persistence across full application/OS restarts, missing monitors and invalid geometry is unknown.

Evidence: `VID-B013`; [exact source routes](#analysis-only-evidence).

### REQ-VIDEO-WORKFLOW-008 — Full screen and original size

**D12/target-U.** Double-clicking Video Window shows full screen, optionally on another monitor. Alt on Windows or Option on Mac plus double-click restores original video size. Full-screen exit gestures and OS-specific exclusive display policy are not supplied.

Evidence: `VID-B013`; [exact source routes](#analysis-only-evidence).

### REQ-VIDEO-WORKFLOW-009 — Partial stream gaps

**D12/target-U.** QuickTime movie audio/video streams may cover different intervals. During a video gap Video Window shows black; an audio gap plays silence. Missing-stream files, decoded sample floor, gap boundary inclusivity and background RGB are unknown.

Evidence: `VID-B015`; [exact source routes](#analysis-only-evidence).

### REQ-VIDEO-WORKFLOW-010 — Video tempo-leader prerequisite

**D12/target-U.** The video clip Warp switch must be on to set Tempo Leader. The documented scoring setup uses video as leader and audio as follower; these are described defaults/guidance, not evidence of target constructor defaults. Warp algorithms and tempo-map arithmetic remain outside this packet.

Evidence: `VID-B017`, `VID-B028`; [exact source routes](#analysis-only-evidence).

### REQ-VIDEO-WORKFLOW-011 — Active leader selection in the video setup

**D12/target-U.** Of warped Arrangement clips marked Leader, the bottom-most currently playing clip is documented as the actual tempo leader. A nonplaying flagged clip is not described as the active leader. Exact overlapping-region boundary, hierarchy order and mapping from marker positions to tempo remain unknown.

Evidence: `VID-B018`; [exact source routes](#analysis-only-evidence).

### REQ-VIDEO-WORKFLOW-012 — Nonleader video warping

**D12/target-U.** An Arrangement video clip that is not the active tempo leader may become warped and produce warped video output. The source gives no frame interpolation/drop/repeat, codec, frame-rate or synchronization tolerance.

Evidence: `VID-B019`; [exact source routes](#analysis-only-evidence).

### REQ-VIDEO-WORKFLOW-013 — Warp-marker visual feedback

**D12/target-U.** Dragging a video clip Warp Marker updates Video Window to the corresponding frame. The source does not give frame selection rounding, delivery deadline, exact decoded image or behavior while media is unavailable.

Evidence: `VID-B021`, `VID-B029`; [exact source routes](#analysis-only-evidence).

### REQ-VIDEO-WORKFLOW-014 — Embedded QuickTime markers

**D12/target-U.** Embedded QuickTime markers are displayed as visual cues for placing Warp Markers. Accepted marker codecs, text encoding, counts, naming, duplicate positions and exact time conversion are unknown.

Evidence: `VID-B022`; [exact source routes](#analysis-only-evidence).

### REQ-VIDEO-WORKFLOW-015 — Pre-roll working region

**D12/target-U.** The documented scoring example puts a movie at Arrangement1.1.1 and moves its Clip View Start Marker past pre-roll so action begins at song start. This changes the working region, not the original movie. Generic start-marker editing remains with Clip View; SMPTE/sample conversion is unknown.

Evidence: `VID-B033`, `VID-B034`, `VID-B035`, `VID-B036`; [exact source routes](#analysis-only-evidence).

### REQ-VIDEO-WORKFLOW-016 — Restoring pre-roll for delivery

**D12/target-U.** The example restores pre-roll by moving the whole composition later, selecting the video alone and extending its left edge back to reveal the omitted material. Its selected movie then supplies the example export range. General export range/options/codecs remain in SPEC-AUDIO-VIDEO-EXPORT, not a universal output-duration promise here.

Evidence: `VID-B037`, `VID-B038`, `VID-B039`; [exact source routes](#analysis-only-evidence).

### REQ-VIDEO-WORKFLOW-017 — Video Window appearance after movie drop

**D12/target-U.** For an admitted QuickTime movie dragged from Browser into an Arrangement audio track, the chapter describes the Video Window appearing to display the movie video. This adds the source-specific import-to-window presentation role only. Actual decode/frame output, unsupported media, hidden-window history, window priority and opening latency remain unknown.

Evidence: `VID-B026`; [exact source routes](#analysis-only-evidence).

### REQ-VIDEO-WORKFLOW-018 — Arrangement waveform feedback during video Warp edits

**D12/target-U.** In the documented scoring setup, adding and adjusting video Warp Markers is accompanied by updates to the video clip waveform in Arrangement to reflect those changes. This is distinct from Video Window corresponding-frame feedback. Exact waveform shape, marker/time/sample mapping, hit-point synchronization, pixels and update timing remain unknown; existing Warp and Arrangement owners retain their finite laws.

Evidence: `VID-B029`; [exact source routes](#analysis-only-evidence).

### REQ-VIDEO-WORKFLOW-U-MEDIA — Media/codec and numerical outputs

**U/target-U.** Decode, source/container/codec/frame-rate/marker/timecode/track-gap handling, missing streams, frame selection, audio output and resource limits remain required unknowns.

### REQ-VIDEO-WORKFLOW-U-LIFECYCLE — Lifecycle, state and failure outcomes

**U/target-U.** Undo/cancel/save/source-loss, editing/tempo/transport ordering, window/display recovery, concurrency and teardown remain required unknowns.

## Finite acceptance proposals

[Current R2 cases](../../analysis/ableton-live-12.4.3/full-spec-v1/video-workflows/cases-r2.json)
retain all28 old IDs and add six cases: two source roles and four explicit U
observations. Twenty requirements (18D12/2U) map to34 cases. Twelve named visible
control/state proposals retain qualified documentary expectations; every actual
outcome/comparator and every signal/file/timing/U documentary outcome/comparator
is null/U/unexecuted. Finite contexts refine drag, resize, platform/display,
partial-track positions, scoring, pre-roll, exact selection and lifecycle actions.
They do not supply fixtures or full branch coverage. Default histories, finite
Leader counts and selected-movie export-duration observations remain U; old011
does not adopt arbitrary-count support from the source's any-number wording.

## Analysis-only evidence

- Official [Version12 video chapter](https://www.ableton.com/en/live-manual/12/working-with-video/),
  captured2026-10-19T21:36:14.636455+00:00, 251482bytes, SHA-256
  `76c940973456cf47c91157e308345544f058d0e98a9fa3f92ad6b88efc8a238a`; [exact HTML](../../analysis/ableton-live-12.4.3/full-spec-v1/video-workflows/manual-video-2026-10-19.html).
- [39 paragraph/heading/list locators](../../analysis/ableton-live-12.4.3/full-spec-v1/video-workflows/source-blocks.json)
  retain exact section anchors/HTML lines; [text view](../../analysis/ableton-live-12.4.3/full-spec-v1/video-workflows/source-blocks.txt)
  is navigation only. The imported existing analyst parser is pinned in dependencies.json.
- [Current R2 requirements](../../analysis/ableton-live-12.4.3/full-spec-v1/video-workflows/requirements-r2.json)
  and [R2 author seal](../../analysis/ableton-live-12.4.3/full-spec-v1/video-workflows/manifest-author-r2.json)
  freeze the partial draft for independent review. No prior release is expanded.

No domain/codec enumeration, performance promise, CPU/decoder/thread architecture,
memory law, synchronization limit or complete platform support follows from this
manual. All error/cancel/undo/persistence/source-loss/rate/teardown, missing-stream,
frame/timecode and image/audio numerical outcomes remain required unknowns.

## Preserved history and checks

[R1 archive](../../analysis/ableton-live-12.4.3/full-spec-v1/video-workflows/archive-r1/manifest-author-r1.json)
retains all fourteen original files. Unsuffixed catalogs, snapshots, validation
and checker are historical R1. The [R2 read-only checker](../../analysis/ableton-live-12.4.3/full-spec-v1/video-workflows/validate-r2.py)
checks this successor and exactly four disclosed historical Video canonical pin
reads against immutable R1 snapshots. R4 and Video audit files/pins are unchanged;
their old direct-current-canonical tools are not current R2 replay entrypoints.
Root owns combined crosspacket replay. Focused independent R2 review is pending;
no release, complete topic or compatibility result follows.
