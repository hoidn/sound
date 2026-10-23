---
id: SPEC-VIDEO-WORKFLOWS
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 1
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

## Requirements

Use the [finite future setup](../../analysis/ableton-live-12.4.3/full-spec-v1/video-workflows/fixtures.json)
and reset histories/configuration per case. Independently confirm visible video
and active nonzero audio before any black/silence/continuity assertion. Nominal
MOV extension, zero send, absent stream, hidden window or failed decoder cannot
establish the tested behavior. All compound clauses remain partial until their
individual branches, source outcomes and required case kinds are closed.

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

### REQ-VIDEO-WORKFLOW-U-MEDIA — Media/codec and numerical outputs

**U/target-U.** Decode, source/container/codec/frame-rate/marker/timecode/track-gap handling, missing streams, frame selection, audio output and resource limits remain required unknowns.

### REQ-VIDEO-WORKFLOW-U-LIFECYCLE — Lifecycle, state and failure outcomes

**U/target-U.** Undo/cancel/save/source-loss, editing/tempo/transport ordering, window/display recovery, concurrency and teardown remain required unknowns.

## Finite acceptance proposals

The [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/video-workflows/cases.json)
contains full finite actions, source references and documentary proposals; the
table is an index. There are18requirements (16 D12/2 U) and28cases:16 documented
proposals plus12operational U probes. Two signal/two timing proposals have null
documentary comparators; every target expectation/comparison is null and grade U.

| Case | Requirement | Kind / action |
| --- | --- | --- |
| VID-001 | REQ-VIDEO-WORKFLOW-001 | control: Use a separately validated owned .mov with nonempty video/audio and import from Browser into an Arrangement audio track. Identify codec/streams independently; an unsupported fixture leaves U. |
| VID-002 | REQ-VIDEO-WORKFLOW-002 | control: On separately reset copies import the same known movie into Arrangement and Session; inspect clip type/view eligibility. Establish audible/visible positive input controls before observing the Session limitation. |
| VID-003 | REQ-VIDEO-WORKFLOW-003 | control: Compare known video clip title with a plain audio clip in Arrangement at an admitted view scale. |
| VID-004 | REQ-VIDEO-WORKFLOW-004 | control: With owned movie long enough for an interior region, trim left and right edges in separate copies, retaining source identity and displayed region. |
| VID-005 | REQ-VIDEO-WORKFLOW-005 | state: In separate owned copies run Consolidate, Reverse and Crop in their supported Arrangement/Clip View contexts on the same video asset; inspect resulting clip media role and independently hash the original movie before/after. |
| VID-006 | REQ-VIDEO-WORKFLOW-006 | control: Open an Arrangement movie, move Video Window, toggle its View command, and place Live's main window under it. Do not infer OS-wide topmost behavior. |
| VID-007 | REQ-VIDEO-WORKFLOW-007 | state: Resize/move the window, close/hide and open a video again in the same session; separately open another owned Set/movie after recording the prior geometry. |
| VID-008 | REQ-VIDEO-WORKFLOW-008 | control: With identified source dimensions, double-click Video Window, then perform the documented platform-modified double-click in a separate controlled trial. Use second monitor only if independently available. |
| VID-009 | REQ-VIDEO-WORKFLOW-009 | signal: Use future owned .mov with independently indexed nonempty video/audio before and after a video-only gap and separate audio-only gap. Confirm valid positive playback on both sides before inspecting gaps. |
| VID-010 | REQ-VIDEO-WORKFLOW-010 | control: With movie in Arrangement, inspect Leader availability with Warp off/on, then explicitly select Leader and a separate audio follower. Do not rely on defaults. |
| VID-011 | REQ-VIDEO-WORKFLOW-011 | timing: Use two overlapping owned warped Arrangement movie/audio clips flagged Leader, with independently distinguishable valid tempo maps; place them in different track order and repeat with one not playing. |
| VID-012 | REQ-VIDEO-WORKFLOW-012 | signal: Retain active positive video output and a separately confirmed different active leader; change its tempo map while movie is nonleader and record output for future analysis. |
| VID-013 | REQ-VIDEO-WORKFLOW-013 | timing: On an owned movie with independently indexed distinguishable frames, drag a video Warp Marker between two interior positions with window visible; record marker and frame feedback. |
| VID-014 | REQ-VIDEO-WORKFLOW-014 | control: Use future owned movie with independently verified embedded named markers at two interior times; import and inspect cue presentation before setting Warp Markers. |
| VID-015 | REQ-VIDEO-WORKFLOW-015 | state: Use owned movie with known two-second pre-roll and distinct action onset; place at1.1.1, open Clip View and move Start to that onset in a disposable copy. |
| VID-016 | REQ-VIDEO-WORKFLOW-016 | state: After the pre-roll working-region setup and adding owned music, move all composition later by the known omitted interval; select video alone, reveal its left pre-roll and inspect intended selection before invoking the existing export workflow. |
| VID-U-FORMAT | REQ-VIDEO-WORKFLOW-U-MEDIA | format: Import unsupported/invalid extension, truncated .mov, valid container with unsupported stream codec and audio-only/video-only file in separate disposable trials. |
| VID-U-BOUNDARY | REQ-VIDEO-WORKFLOW-U-MEDIA | boundary: Move region/markers to source start/end, just outside bounds and adjacent to partial-stream gap; enter zero/negative/extreme positions without assuming clamp/reject policy. |
| VID-U-AUDIO-VIDEO | REQ-VIDEO-WORKFLOW-U-MEDIA | audio-video: Capture active nonmuted positive audio/video baselines, then inspect known gaps, nonleader warping, frame/sample synchronization and processing transitions; no tolerance exists. |
| VID-U-MARKERS | REQ-VIDEO-WORKFLOW-U-MEDIA | markers: Use duplicate/non-ASCII/large-count embedded markers and two distinct frame rates; observe text/order/time without presupposing a QuickTime marker codec. |
| VID-U-RATE | REQ-VIDEO-WORKFLOW-U-MEDIA | rate: Use separately validated24/25/30fps/VFR inputs where accepted, request44.1/48kHz audio rates and window resizes; retain decoder/driver settings and no timing guarantee. |
| VID-U-UNDO | REQ-VIDEO-WORKFLOW-U-LIFECYCLE | undo: Trim, Reverse/Crop into audio-only clip and change leader; Undo/Redo separately, inspecting media role, source files and visible state. |
| VID-U-CANCEL | REQ-VIDEO-WORKFLOW-U-LIFECYCLE | cancel: Cancel an offered import/progress/processing dialog before commit; dismiss window gesture separately. Cancellation availability and partial-output cleanup are unknown. |
| VID-U-PERSISTENCE | REQ-VIDEO-WORKFLOW-U-LIFECYCLE | persistence: Save/reopen a Set with trimmed movies, leader flags/markers and window geometry; reopen another Set and restart application in separate trials. |
| VID-U-SOURCE-LOSS | REQ-VIDEO-WORKFLOW-U-LIFECYCLE | source-loss: On owned copy rename/remove movie source, reopen and relink; repeat while pending frame feedback, without modifying retained originals. |
| VID-U-TRANSPORT | REQ-VIDEO-WORKFLOW-U-LIFECYCLE | transport: Stop/seek/restart across gap, clip end and active-leader boundary; change tempo/automation concurrently in separate trials. Record ordering without inventing deadlines. |
| VID-U-DISPLAY | REQ-VIDEO-WORKFLOW-U-LIFECYCLE | display: Move Video Window to an independently available second monitor, disconnect/change scale in future supported setup and reopen video; record fallback, focus and accessibility. |
| VID-U-TEARDOWN | REQ-VIDEO-WORKFLOW-U-LIFECYCLE | teardown: Close/remove video clip, track, Set and application during active video and separate pending import/editor action; observe prompts, resources and retained files. |

## Analysis-only evidence

- Official [Version12 video chapter](https://www.ableton.com/en/live-manual/12/working-with-video/),
  captured2026-10-19T21:36:14.636455+00:00, 251482bytes, SHA-256
  `76c940973456cf47c91157e308345544f058d0e98a9fa3f92ad6b88efc8a238a`; [exact HTML](../../analysis/ableton-live-12.4.3/full-spec-v1/video-workflows/manual-video-2026-10-19.html).
- [39 paragraph/heading/list locators](../../analysis/ableton-live-12.4.3/full-spec-v1/video-workflows/source-blocks.json)
  retain exact section anchors/HTML lines; [text view](../../analysis/ableton-live-12.4.3/full-spec-v1/video-workflows/source-blocks.txt)
  is navigation only. The imported existing analyst parser is pinned in dependencies.json.
- [Requirement catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/video-workflows/requirements.json)
  and [author seal](../../analysis/ableton-live-12.4.3/full-spec-v1/video-workflows/manifest-author-r1.json)
  freeze the partial draft for independent review. No prior release is expanded.

No domain/codec enumeration, performance promise, CPU/decoder/thread architecture,
memory law, synchronization limit or complete platform support follows from this
manual. All error/cancel/undo/persistence/source-loss/rate/teardown, missing-stream,
frame/timecode and image/audio numerical outcomes remain required unknowns.
