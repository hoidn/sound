---
id: SPEC-WARPING-WORKFLOWS
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3; current Version 12 documentary behavior with applicability unknown
---

# Warp editing and playback workflows

## Scope and evidence boundary

This partial F-04/FEAT-WARP analyst contract owns interactive Warp/transient
editing, automatic-warp command roles, sample-load policy controls, audio-clip
tempo/leader controls and mode-control roles. The retained Version 12 chapter
is dated by capture, not by an asserted patch. **Every D12 clause, command,
gesture, option and described default has exact-12.4.3 applicability U.**
[Research](../research/warping-workflows.md) records source interpretation/gaps.
No original application/function, candidate, decoder, hardware or native probe
was run. This draft is not a released handoff or complete Warp family.

D12 means directly documented in the retained current major-version manual.
U means no supported outcome. All cases have target `expected`/`comparison`
null, grade U, `executed:false`. Signal, timing, automatically generated result
and lifecycle documentary expectations/comparators are also null: their
`source_claim` records what the chapter says, not a measurable oracle. Control
cases grade only named visible documentary state and remain target-U. No DSP,
detector, stretch, RNG, interpolation, clock, quality or tolerance is inferred
from recommendations, marketing language or private mechanism descriptions.

## Existing canonical owners

- [Warp markers](warp-markers.md) retains all existing serialization, numeric
  mapping, shadow/grid, enum/range/default and scripting-edit contracts and their
  assumptions. No interactive gesture is assumed to use scripting bounds or
  rounding. No finite extracted-function fixture proves an automatic map or
  stretched playback result. Published releases and the canonical page remain
  unchanged.
- [Clip View](clip-view-workflows.md), especially REQ018/028/031/045, owns the
  Warp switch's basic playback roles, Quantize panel availability, editor Follow
  and Clip Update Rate. Generic regions, loop enablement, focus, crop/reverse,
  gain/pitch and editor UI remain there. This page adds interactive commands
  and control roles without recopying those finite or general operations.
- [Video](video-workflows.md), especially REQ010–014, retains video prerequisites,
  the documented bottom-most currently playing leader selection context and
  marker-to-frame feedback. This chapter corroborates its active-leader rule;
  it does not supply a separate hierarchy/boundary/scheduler law. This page owns
  audio Arrangement Lead/Follow controls and generated automation presentation.
- [Transport](transport-state.md), [playback](playback-core.md),
  [automation](automation-envelopes.md), [Session](session-view-workflows.md) and
  [launch](clip-launch.md) retain stored tempo, finite time/event mapping,
  envelope and scene/clip scheduling. Tap/nudge controls and leader UI below do
  not extend those numerical contracts or define a complete tempo precedence.
- [Media](media-file-workflows.md) owns import/cache/analysis/ASD/default settings;
  [projects](project-media-workflows.md) owns references/collection/save. Saving
  markers with an owned sample uses those owners; only the ordinary Auto-Warp
  exception/manual command distinction is added here. Conflicting/narrower
  readiness and format wording stays unresolved rather than replacing an owner.
- [Groove](groove-workflows.md) owns assignment/application/Commit marker results;
  [audio-to-MIDI](audio-to-midi.md) owns slicing/conversion and transient influence.
  [MPE](mpe-workflows.md), [tuning](tuning-systems.md) and [MIDI editing](midi-editing-tools.md)
  retain their data/processing. Direct audio Quantize here does not define their
  operations. [Mapping](midi-user-mapping.md) retains mapping/takeover protocol.
  [Routing](routing-monitoring-latency.md), [export](audio-video-export.md) and
  [Bounce/Freeze](bounce-freeze-workflows.md) retain output and commit workflows.

## Preconditions and observables

The [future fixtures](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/fixtures.json)
provide finite setup definitions, not media/ALS/ASD, marker ground truth, hardware
or captured outputs. Retain accepted sample class, exact source/beat/downbeat
identity, source versus region/display length, focus, selected markers/time,
Warp/Loop/mode, tempo/meter, preferences and saved markers/analysis context.
Short/long classification and a true detected transient are prerequisites to
cases that name them, not assumptions justified by an arbitrary duration or peak.

Before signal or no-effect/exclusion observations establish independently
nonempty eligible source, accepted path/control, Warp on/correct mode, enabled
processing and relevant admitted nonzero amount/stretch/transposition. Retain
nonmuted source and wet return/output, actual receiver Monitor/arm/clip context,
and a matched independent positive baseline. Confirm direct/dry/return paths
before isolation. A failed gate, absent interface, wrong mode, zero amount,
silent source or unavailable operation remains inconclusive. UI and meters alone
do not establish rendered output, detector correctness or alignment.

Inspect controls, selection/membership, real/pseudo/transient markers, waveform
versus marker movement, generated versus editable automation and resulting source
references separately. No count of cases or one control observation closes a
compound clause. Each named gesture/source/default context needs retained evidence;
all branches below are future and target-U. Marker/BPM results, numeric ranges,
amount/tie rules, samples and lifecycle outcomes stay explicitly ungraded.

## Requirements

### REQ-WFW-001 — Tempo field controls

**D12/target-U.** Control Bar tempo exposes coarse BPM and fine hundredths of BPM controls which can be key/MIDI mapped separately. Numeric storage, ranges, interpolation and mapping protocol retain existing owners.

Evidence: [WFW:B006](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B007](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json).

Existing owners: [transport-state](transport-state.md), [automation-envelopes](automation-envelopes.md), [midi-user-mapping](midi-user-mapping.md).

### REQ-WFW-002 — Tap Tempo inputs

**D12/target-U.** Tap Tempo accepts mouse clicks, a key assigned through Key Map Mode, or a MIDI note/controller assigned through MIDI Map Mode. Tap estimation, dispatch latency and accuracy remain ungraded.

Evidence: [WFW:B010](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B011](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B012](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B013](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B014](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B015](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B016](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B017](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B018](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B019](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json).

Existing owners: [midi-user-mapping](midi-user-mapping.md).

### REQ-WFW-003 — Tap-start option

**D12/target-U.** Start Playback with Tap Tempo in Record, Warp & Launch Settings enables tap-triggered playback; the source describes four taps in 4/4. No estimator, interval tolerance, other-meter count or Link alignment oracle is established.

Evidence: [WFW:B020](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B021](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json).

### REQ-WFW-004 — Phase Nudge controls

**D12/target-U.** Phase Nudge Up/Down can temporarily speed or slow playback and can be key/MIDI mapped. Rate, duration, recovery curve, phase and external synchronization are unknown.

Evidence: [WFW:B023](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json).

Existing owners: [transport-state](transport-state.md), [midi-user-mapping](midi-user-mapping.md).

### REQ-WFW-005 — Audio clip Lead and Follow

**D12/target-U.** Warped audio clips are documented as followers by default; Arrangement clips can select Lead through Audio Utilities Lead/Follow. This is documentary context, not an exact-target constructor default or Session eligibility rule.

Evidence: [WFW:B025](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json).

Existing owners: [video-workflows](video-workflows.md).

### REQ-WFW-006 — Leader role and disabled tempo field

**D12/target-U.** For an active tempo leader, clip Warp Markers determine Set tempo and the Control Bar tempo field is deactivated. The source describes leader playback as if unwarped; no time-map, DSP or sample equality follows.

Evidence: [WFW:B026](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json).

Existing owners: [warp-markers](warp-markers.md), [transport-state](transport-state.md).

### REQ-WFW-007 — Leader-generated automation presentation

**D12/target-U.** Tempo automation tracking leader/Set tempo changes appears in Main and is not editable; rearranging leader clips moves the corresponding automation. Exact points, ownership boundaries and scheduling remain unknown.

Evidence: [WFW:B028](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json).

Existing owners: [automation-envelopes](automation-envelopes.md).

### REQ-WFW-008 — Unfollow Tempo Automation

**D12/target-U.** Unfollow Tempo Automation in the tempo field context menu makes all leader clips followers and makes the Main tempo automation editable. Envelope point identity, numerical values and Undo are unknown.

Evidence: [WFW:B028](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json).

### REQ-WFW-009 — External sync toggle eligibility

**D12/target-U.** With EXT enabled, the Lead/Follow toggle is deactivated. Accepted external source, protocol, activation timing and fallback remain unknown.

Evidence: [WFW:B030](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json).

### REQ-WFW-010 — Leader versus audio Tempo Follower

**D12/target-U.** Clip-leader tempo automation is documented to override tempo from an audio input synchronized through Tempo Follower. This does not establish all tempo-source precedence or real-time alignment.

Evidence: [WFW:B029](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json).

### REQ-WFW-011 — Short-sample load policy controls

**D12/target-U.** Record, Warp & Launch Settings offers Loop/Warp Short Samples: Unwarped One Shot, Warped One Shot, Warped Loop and Auto. The first is unwarped; the second warped using Default Warp Mode without looping; the third warped/looped. Auto chooses a policy and is documented as selected by default. Classification threshold and Auto choice remain unknown.

Evidence: [WFW:B038](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B039](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B040](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B041](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B042](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B043](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json).

### REQ-WFW-012 — Long-sample load policy

**D12/target-U.** Auto-Warp Long Samples is documented enabled by default. Enabled requests automatic warping on load; disabled loads long samples unwarped. The source claims a first-beat-per-bar marker policy, without establishing analysis or exact marker results for any supplied sample.

Evidence: [WFW:B038](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B044](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json).

### REQ-WFW-013 — Default Warp Mode preference

**D12/target-U.** Default Warp Mode selects the mode applied when samples are warped; this chapter describes Beats as the initial default. This documentary default does not settle missing-field load behavior, preference precedence or exact-target factory state.

Evidence: [WFW:B045](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json).

Existing owners: [warp-markers](warp-markers.md).

### REQ-WFW-014 — Insert an interactive Warp Marker

**D12/target-U.** In the Sample Editor upper half, double-click adds a Warp Marker; Ctrl+I (Windows)/Cmd+I (macOS) places one at the insert marker. Selection-driven insertion has its separate documented context below. Numeric marker validation, identity and scripting limits are not imported.

Evidence: [WFW:B050](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B051](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json).

### REQ-WFW-015 — Move interactive markers

**D12/target-U.** Warp Markers can be dragged or moved with arrow keys to change their timeline placement. Step size, snapping, bounds, rounding and audio output are unknown here.

Evidence: [WFW:B051](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json).

### REQ-WFW-016 — Shift waveform under a marker

**D12/target-U.** With a Warp Marker selected, Shift-drag moves the waveform beneath the marker to adjust the audio starting point under it. Exact coordinate transformation and collateral marker changes are unknown.

Evidence: [WFW:B052](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B085](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B086](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json).

### REQ-WFW-017 — Delete interactive Warp Markers

**D12/target-U.** Double-click deletes a Warp Marker; selecting its corresponding time and pressing Backspace (Windows)/Delete (macOS) is another documented route. Last/protected markers, deduplication and exact resulting list remain unknown.

Evidence: [WFW:B053](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json).

### REQ-WFW-018 — Transient presentation and editing

**D12/target-U.** Detected transients appear as small gray markers. Create menu and Ctrl+Shift+I (Windows)/Cmd+Shift+I (macOS) create transients; Ctrl+Shift+Backspace (Windows)/Cmd+Shift+Delete (macOS) deletes them. Detection output and numerical positions remain unknown.

Evidence: [WFW:B056](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B057](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B058](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json).

Existing owners: [audio-to-midi](audio-to-midi.md).

### REQ-WFW-019 — Reset manually created transients

**D12/target-U.** Sample Editor Reset Transients removes all manually created transients. The source does not establish restoration of moved/deleted automatically detected transients or exact redetection results.

Evidence: [WFW:B058](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json).

### REQ-WFW-020 — Selection-based Warp Marker insertion

**D12/target-U.** Insert Warp Markers in Create or Ctrl+I (Windows)/Cmd+I (macOS) creates markers for selected-area transients. For a selected area containing no transients, the source describes markers at selection start and end. Numerical endpoint, count/deduplication and detector outcomes remain unknown.

Evidence: [WFW:B059](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json).

### REQ-WFW-021 — Pseudo-marker conversion

**D12/target-U.** Hovering a transient shows a gray pseudo-Warp Marker; double-click or drag converts it to a real Warp Marker. The source says clip tempo changes if no Warp Markers follow the new one, without a numerical tempo oracle.

Evidence: [WFW:B060](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json).

### REQ-WFW-022 — Pseudo-marker adjacent anchors

**D12/target-U.** Ctrl (Windows)/Cmd (macOS) while creating a real marker from a pseudo-marker also creates Warp Markers at adjacent transients. First/last transient, duplicates and exact resulting lists remain unknown.

Evidence: [WFW:B060](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json).

### REQ-WFW-023 — Move transient via pseudo-marker

**D12/target-U.** Shift-dragging a pseudo-marker moves the transient to a new Sample Editor location. This is distinct from moving waveform under a selected real Warp Marker.

Evidence: [WFW:B060](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json).

### REQ-WFW-024 — Saved markers and Auto-Warp

**D12/target-U.** A sample saved with Warp Markers is unaffected by ordinary Auto-Warp; manual Warp From context commands remain available. Saving default clip settings and their media scope remain with the media owner. Exact identity/ASD precedence and corruption outcomes remain unknown.

Evidence: [WFW:B062](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B063](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json).

Existing owners: [media-file-workflows](media-file-workflows.md).

### REQ-WFW-025 — Clip BPM and Arrangement edge adjustment

**D12/target-U.** Audio Utilities BPM shows estimated sample tempo, permits direct known-BPM input and Shift-drag fine adjustment. Shift-drag from an Arrangement clip edge stretches or compresses its tempo. Accepted range, increment, anchors and timing arithmetic are unknown.

Evidence: [WFW:B068](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json).

### REQ-WFW-026 — Double and halve clip tempo

**D12/target-U.** The clip tempo ×2 and ÷2 buttons double or halve estimated tempo for correction. Limits, repeated-operation rounding and resulting marker/sample mapping remain unknown.

Evidence: [WFW:B069](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json).

### REQ-WFW-027 — Set 1.1.1 Here contexts

**D12/target-U.** For an uneven short-loop example, moving the insert marker to the downbeat and Set 1.1.1 Here places a Warp Marker there; in the long-sample correction example the command moves the start marker to that downbeat. Preserve these source contexts without asserting a complete region/marker transform.

Evidence: [WFW:B076](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B077](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B085](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B087](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B088](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json).

### REQ-WFW-028 — Same-length multi-clip marker editing

**D12/target-U.** For multiple clips of the same length, adding or adjusting Warp Markers in one applies the changes to all selected clips. Length equality definition, mixed Warp/region states, deletion and unequal-length behavior remain unknown.

Evidence: [WFW:B079](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json).

### REQ-WFW-029 — Warp Sample as command

**D12/target-U.** For a seamlessly edited loop, Warp Sample as in Sample Editor context menu displays a suggested loop length fitting Set tempo. Suggested length and generated markers are ungraded.

Evidence: [WFW:B089](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json).

### REQ-WFW-030 — Warp Selection as command

**D12/target-U.** Warp Selection as operates on selected sample time; the source describes assumed loop length, loop start/end markers and warping to fill the loop. Algorithm choice, exact markers, bounds and audio are ungraded.

Evidence: [WFW:B090](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json).

### REQ-WFW-031 — Move multiple Warp Markers

**D12/target-U.** Ctrl (Windows)/Cmd (macOS) selects multiple Warp Markers for moving together. Anchor, spacing, snapping, coordinate and refusal laws remain unknown.

Evidence: [WFW:B091](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json).

### REQ-WFW-032 — Warp From Here scope

**D12/target-U.** Warp From Here context commands reset markers to the right of the chosen grid division/marker while leaving left-side markers unchanged. The basic command requests Auto-Warp to the right and adds a marker at the specified grid point if none is selected. Exact generated list and selected-point ownership remain unknown.

Evidence: [WFW:B092](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B093](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json).

### REQ-WFW-033 — Warp From Here Start At baseline

**D12/target-U.** Warp From Here (Start At …) uses Set tempo as the Auto-Warp baseline. The described preparation turns Warp off, taps the source tempo, re-enables Warp and invokes the command. Estimation and generated marker outcomes remain unknown.

Evidence: [WFW:B094](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json).

### REQ-WFW-034 — Warp From Here Straight

**D12/target-U.** Warp From Here (Straight) is intended for material without tempo variation; the source describes one starting marker based on estimated original BPM. This is a source claim, not a graded automatic marker count or position for unprovided media.

Evidence: [WFW:B095](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json).

### REQ-WFW-035 — Warp BPM From Here

**D12/target-U.** Warp … BPM From Here assumes source tempo equals Set tempo and describes a single starting marker. Known BPM may be entered in Control Bar before invoking it; exact resulting map and boundary handling remain unknown.

Evidence: [WFW:B096](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json).

### REQ-WFW-036 — Quantize command focus

**D12/target-U.** With Sample Editor focused, Edit Quantize or Ctrl+U (Windows)/Cmd+U (macOS) uses current Quantize settings. Clip View owns the Quantize panel availability and grid/Amount controls.

Evidence: [WFW:B103](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json).

Existing owners: [clip-view-workflows](clip-view-workflows.md).

### REQ-WFW-037 — Audio quantization role

**D12/target-U.** The source describes moving a nearest transient to a closest grid line; current or specific/triplet grid and Amount affect Warp Marker movement. Selection, ties, Amount equation, marker generation and exact output remain unknown. Groove application/commit remains groove-owned.

Evidence: [WFW:B102](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B104](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json).

Existing owners: [groove-workflows](groove-workflows.md).

### REQ-WFW-038 — Beats Preserve control

**D12/target-U.** Beats mode exposes Preserve with Transients or grid divisions to choose segment divisions. Actual segmentation, transient preservation, grains, crossfades, values and output quality are ungraded; stored enums/settings remain Warp-marker-owned.

Evidence: [WFW:B109](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B110](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json).

Existing owners: [warp-markers](warp-markers.md).

### REQ-WFW-039 — Beats Transient Loop modes

**D12/target-U.** Transient Loop Mode offers Loop Off, Loop Forward and Loop Back-and-Forth. The source describes segment stop/silence, forward looping and alternating direction respectively; zero-crossing choice, endpoints, loops and delivered audio remain unknown.

Evidence: [WFW:B111](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B112](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B113](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B114](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json).

Existing owners: [warp-markers](warp-markers.md).

### REQ-WFW-040 — Transient Envelope role

**D12/target-U.** Transient Envelope controls segment fades; the source describes no fade at 100 and quicker decay at 0. No numeric gain envelope, time constant, normalization, detector or click-quality criterion follows. Existing stored range/default uncertainty remains unchanged.

Evidence: [WFW:B115](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json).

Existing owners: [warp-markers](warp-markers.md).

### REQ-WFW-041 — Tones Grain Size role

**D12/target-U.** Tones exposes Grain Size for approximate average grain size, described as affected by pitch clarity. Suggested material and grain size are guidance, not a pitch detector, DSP, noise or quality guarantee.

Evidence: [WFW:B117](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B118](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json).

### REQ-WFW-042 — Texture controls

**D12/target-U.** Texture exposes Grain Size and Fluctuation; the former is described independently of tonal characteristics, the latter as increasing processing randomness. No RNG, seed, distribution, correlation, grain process or monotonic statistical oracle is established.

Evidence: [WFW:B120](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B121](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B122](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json).

### REQ-WFW-043 — Re-Pitch control and signal role

**D12/target-U.** Re-Pitch changes playback rate and pitch with tempo; its sample transposition controls are deactivated. The doubled-rate/octave source example is descriptive, not a new rate-conversion or sample-accuracy contract.

Evidence: [WFW:B124](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B125](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json).

Existing owners: [warp-markers](warp-markers.md), [playback-core](playback-core.md).

### REQ-WFW-044 — Complex Pro Formants and Envelope

**D12/target-U.** Complex Pro exposes Formants and Envelope. The source describes formant preservation at 100% with transposition and no Formants effect without transposition; Envelope changes tonal character. Exact response, defaults/ranges and byte values retain existing storage owner or remain unknown; no quality/CPU guarantee is inferred.

Evidence: [WFW:B127](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B128](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B129](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B130](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B131](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json).

Existing owners: [warp-markers](warp-markers.md).

### REQ-WFW-U-AUTO — Detection and automatically generated markers

**U/target-U.** Short/long classification, initial BPM/markers, downbeat accuracy, transient detection and exact output of every Auto-Warp/Warp From/Selection/Sample command require evidence. Short-loop and odd-loop examples do not provide universal estimators or correct marker positions.

Evidence: [WFW:B038](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B044](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B048](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B056](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B065](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B067](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B071](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B072](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B073](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B075](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B081](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B083](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json).

### REQ-WFW-U-DSP — Warp audio and randomness

**U/target-U.** Per-mode audio/pitch/time behavior, Formants/Envelope/Transient settings, zero-crossing/grain behavior, resampling, tail/phase continuity, determinism and comparison tolerances remain unknown. Manual material/quality recommendations and internal explanations are not required implementation mechanisms.

Evidence: [WFW:B003](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B106](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B109](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B112](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B113](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B114](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B115](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B118](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B121](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B122](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B124](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B129](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B130](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B131](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json).

### REQ-WFW-U-EDIT — Interactive limits and quantization boundaries

**U/target-U.** Interactive marker/region limits, protected/shadow edits, duplicate/order/selection transforms, near/equal boundaries, unequal multi-clips, quantization ties and Amount rounding remain unknown. Existing scripting limits do not establish interactive behavior.

Evidence: [WFW:B051](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B053](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B059](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B060](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B079](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B091](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B099](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B102](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B104](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json).

Existing owners: [warp-markers](warp-markers.md).

### REQ-WFW-U-TIMING — Tempo and transport interactions

**U/target-U.** Tap estimation/start schedule, nudge curves, leader handoffs and tempo/automation/scene/external-source precedence, live edit dispatch and clip-update timing remain unknown beyond documented controls. The existing video owner retains its documented active-leader selection context.

Evidence: [WFW:B019](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B020](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B021](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B023](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B027](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B028](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B029](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B030](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B054](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json).

Existing owners: [video-workflows](video-workflows.md), [transport-state](transport-state.md), [clip-view-workflows](clip-view-workflows.md).

### REQ-WFW-U-STATE — State and lifecycle

**U/target-U.** Marker/default/analysis interactions on save/reopen/migration, undo/redo, cancel, automation during edits, source/device loss, rate/engine changes, errors and teardown have no complete oracle. Existing finite storage/reader/ASD contracts retain their scope.

Evidence: no supported outcome retained; ungraded obligation.

Existing owners: [warp-markers](warp-markers.md), [media-file-workflows](media-file-workflows.md), [project-media-workflows](project-media-workflows.md).

### REQ-WFW-U-IMPORT — Import source differences

**U/target-U.** This chapter first-import readiness and Import Audio File format/destination text is retained context, not a complete codec or readiness law. Its all-first-import wording versus media owner long-analysis wording, accepted AAC/Ogg variants, platform scope and destination interactions require separate reconciliation.

Evidence: [WFW:B047](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json), [WFW:B048](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json).

Existing owners: [media-file-workflows](media-file-workflows.md).

## Acceptance cases

All 88 cases are unexecuted and target-U/null. Forty-one have documentary visible
control/state predicates; 47 have null documentary oracles. All signal/timing,
automatic-analysis and operational cases use `source_claim` only, never a filled
numerical oracle. Full setup/actions, source routes and limits are retained in
[cases.json](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/cases.json).
This table indexes finite proposals and does not close all command/branch coverage.

| Case | Requirement | Kind | Focus | Documentary criterion |
| --- | --- | --- | --- | --- |
| WFW-001 | REQ-WFW-001 | control | Coarse and fine tempo controls | visible named state only |
| WFW-002 | REQ-WFW-002 | control | Tap input mapping | visible named state only |
| WFW-003 | REQ-WFW-003 | control | Tap-start option | visible named state only |
| WFW-004 | REQ-WFW-004 | control | Nudge controls | visible named state only |
| WFW-005 | REQ-WFW-005 | control | Arrangement audio Lead Follow | visible named state only |
| WFW-006 | REQ-WFW-006 | control | Leader disables tempo field | visible named state only |
| WFW-007 | REQ-WFW-007 | state | Generated tempo automation | visible named state only |
| WFW-008 | REQ-WFW-008 | state | Unfollow automation state | visible named state only |
| WFW-009 | REQ-WFW-009 | boundary | EXT toggle eligibility | visible named state only |
| WFW-010 | REQ-WFW-010 | timing | Clip leader versus Tempo Follower | U / null; source claim only |
| WFW-011 | REQ-WFW-011 | control | Short policy selection | visible named state only |
| WFW-012 | REQ-WFW-012 | control | Long policy selection | visible named state only |
| WFW-013 | REQ-WFW-013 | control | Default Warp Mode selection | visible named state only |
| WFW-014 | REQ-WFW-014 | state | Manual insertion routes | visible named state only |
| WFW-015 | REQ-WFW-015 | state | Drag and arrow movement | visible named state only |
| WFW-016 | REQ-WFW-016 | state | Shift waveform under marker | visible named state only |
| WFW-017 | REQ-WFW-017 | state | Marker deletion routes | visible named state only |
| WFW-018 | REQ-WFW-018 | state | Transient create delete | visible named state only |
| WFW-019 | REQ-WFW-019 | state | Reset manual transients | visible named state only |
| WFW-020 | REQ-WFW-020 | control | Selection insertion command | visible named state only |
| WFW-021 | REQ-WFW-021 | state | Pseudo-marker conversion | visible named state only |
| WFW-022 | REQ-WFW-022 | analysis | Adjacent anchors modifier | U / null; source claim only |
| WFW-023 | REQ-WFW-023 | state | Shift pseudo-marker | visible named state only |
| WFW-024 | REQ-WFW-024 | control | Manual Warp after saved markers | visible named state only |
| WFW-025 | REQ-WFW-025 | control | Clip BPM edit controls | visible named state only |
| WFW-026 | REQ-WFW-026 | control | Tempo double and halve | visible named state only |
| WFW-027 | REQ-WFW-027 | state | Set origin source contexts | visible named state only |
| WFW-028 | REQ-WFW-028 | state | Equal-length multi-clip edits | visible named state only |
| WFW-029 | REQ-WFW-029 | control | Warp Sample as suggestion | visible named state only |
| WFW-030 | REQ-WFW-030 | control | Warp Selection as entry | visible named state only |
| WFW-031 | REQ-WFW-031 | state | Multi-marker move | visible named state only |
| WFW-032 | REQ-WFW-032 | state | Warp From right-side scope | visible named state only |
| WFW-033 | REQ-WFW-033 | control | Start At baseline controls | visible named state only |
| WFW-034 | REQ-WFW-034 | control | Straight command | visible named state only |
| WFW-035 | REQ-WFW-035 | control | BPM From Here command | visible named state only |
| WFW-036 | REQ-WFW-036 | control | Quantize focus entry | visible named state only |
| WFW-037 | REQ-WFW-037 | timing | Quantize displacement | U / null; source claim only |
| WFW-038 | REQ-WFW-038 | control | Beats Preserve choices | visible named state only |
| WFW-039 | REQ-WFW-039 | control | Transient Loop choices | visible named state only |
| WFW-040 | REQ-WFW-040 | control | Transient Envelope control | visible named state only |
| WFW-041 | REQ-WFW-041 | control | Tones Grain Size control | visible named state only |
| WFW-042 | REQ-WFW-042 | control | Texture controls | visible named state only |
| WFW-043 | REQ-WFW-043 | boundary | Re-Pitch disables transposition | visible named state only |
| WFW-044 | REQ-WFW-044 | control | Complex Pro controls | visible named state only |
| WFW-045 | REQ-WFW-002 | timing | Tap estimate and history | U / null; source claim only |
| WFW-046 | REQ-WFW-003 | timing | Four tap start context | U / null; source claim only |
| WFW-047 | REQ-WFW-004 | timing | Nudge playback | U / null; source claim only |
| WFW-048 | REQ-WFW-006 | timing | Leader playback role | U / null; source claim only |
| WFW-049 | REQ-WFW-011 | analysis | Auto short decision | U / null; source claim only |
| WFW-050 | REQ-WFW-012 | analysis | Long generated markers | U / null; source claim only |
| WFW-051 | REQ-WFW-020 | analysis | Selection transients result | U / null; source claim only |
| WFW-052 | REQ-WFW-020 | analysis | No-transient selection | U / null; source claim only |
| WFW-053 | REQ-WFW-021 | timing | Pseudo-marker tempo change | U / null; source claim only |
| WFW-054 | REQ-WFW-024 | analysis | Saved marker Auto-Warp priority | U / null; source claim only |
| WFW-055 | REQ-WFW-025 | timing | Arrangement edge stretch | U / null; source claim only |
| WFW-056 | REQ-WFW-030 | analysis | Selection generated loop | U / null; source claim only |
| WFW-057 | REQ-WFW-032 | analysis | Warp From without selected marker | U / null; source claim only |
| WFW-058 | REQ-WFW-033 | analysis | Start At generated map | U / null; source claim only |
| WFW-059 | REQ-WFW-034 | analysis | Straight generated map | U / null; source claim only |
| WFW-060 | REQ-WFW-035 | analysis | BPM From Here result | U / null; source claim only |
| WFW-061 | REQ-WFW-038 | signal | Preserve audio | U / null; source claim only |
| WFW-062 | REQ-WFW-039 | signal | Transient Loop audio | U / null; source claim only |
| WFW-063 | REQ-WFW-040 | signal | Transient Envelope audio | U / null; source claim only |
| WFW-064 | REQ-WFW-041 | signal | Tones source roles | U / null; source claim only |
| WFW-065 | REQ-WFW-042 | signal | Texture repeated output | U / null; source claim only |
| WFW-066 | REQ-WFW-043 | signal | Re-Pitch source example | U / null; source claim only |
| WFW-067 | REQ-WFW-044 | signal | Formants with and without transpose | U / null; source claim only |
| WFW-068 | REQ-WFW-044 | signal | Complex Envelope audio | U / null; source claim only |
| WFW-069 | REQ-WFW-U-AUTO | analysis | Classification and estimates | U / null; source claim only |
| WFW-070 | REQ-WFW-U-AUTO | analysis | Repeated analysis contexts | U / null; source claim only |
| WFW-071 | REQ-WFW-U-DSP | signal | All mode repeatability | U / null; source claim only |
| WFW-072 | REQ-WFW-U-EDIT | boundary | Marker limits | U / null; source claim only |
| WFW-073 | REQ-WFW-U-EDIT | boundary | Mixed multi-clips | U / null; source claim only |
| WFW-074 | REQ-WFW-U-EDIT | boundary | Quantize boundary Amount | U / null; source claim only |
| WFW-075 | REQ-WFW-U-TIMING | timing | Multiple leader context | U / null; source claim only |
| WFW-076 | REQ-WFW-U-TIMING | transport | Live editing transport | U / null; source claim only |
| WFW-077 | REQ-WFW-U-TIMING | timing | Tempo source changes | U / null; source claim only |
| WFW-078 | REQ-WFW-U-STATE | undo | Undo redo operations | U / null; source claim only |
| WFW-079 | REQ-WFW-U-STATE | cancel | Cancel and dismiss | U / null; source claim only |
| WFW-080 | REQ-WFW-U-STATE | persistence | Save reopen defaults | U / null; source claim only |
| WFW-081 | REQ-WFW-U-STATE | automation | Live automation edits | U / null; source claim only |
| WFW-082 | REQ-WFW-U-STATE | source-loss | Source loss | U / null; source claim only |
| WFW-083 | REQ-WFW-U-STATE | sample-rate | Rate and engine change | U / null; source claim only |
| WFW-084 | REQ-WFW-U-STATE | malformed | Malformed admitted input | U / null; source claim only |
| WFW-085 | REQ-WFW-U-STATE | recovery | Output device loss | U / null; source claim only |
| WFW-086 | REQ-WFW-U-STATE | teardown | Close while active | U / null; source claim only |
| WFW-087 | REQ-WFW-U-IMPORT | analysis | Import wording and readiness | U / null; source claim only |
| WFW-088 | REQ-WFW-U-STATE | error | Writable media and analysis failure | U / null; source claim only |

## Open obligations

[Q-021](../questions.md#q-021-warp-playback-mapping-and-load-handling) retains Warp
mapping/load gaps; [Q-027](../questions.md#q-027-whole-product-specification-evidence-and-version-coverage)
retains current-manual/exact-build applicability. Automatic classification,
transients/initial marker placement, suggested lengths, Warp From generation,
quantization ties/Amount and interactive bounds require independently retained
inputs/results. No internal grain/zero-crossing/RNG narrative supplies a required
algorithm. Source pitch/quality/accuracy examples are not metric definitions.

Tap/nudge, active leader boundaries, source precedence, generated tempo map and
live edits have no numerical or dispatch oracle. Short/long Set 1.1.1 Here
contexts and import readiness/format wording remain separately represented.
Undo/redo, cancellation, persistence/default/ASD identity, source or destination
loss, errors, automation, rate/engine changes, recovery and teardown stay U.
Attempts require offered controls or independently understood formats; no
malformed state encoding, fake host, hardware acquisition or runtime is implied.

## Analyst evidence appendix

The [source ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/sources.json)
pins official URL/final URL, capture UTC, major version, size and SHA256.
[131 blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual-blocks.json)
retain HTML lines, section anchors/numbers and heading contexts; the
[line view](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manual.txt)
is normalized derived text, not a second source. Figures, PDFs and linked
help/tutorials were not separately inspected.

| Source scope | Exact anchors and retained blocks |
| --- | --- |
| §9.1 tempo | #setting-the-tempo through #clip-tempo-followers-and-leaders; WFW:B005–B030, HTML280–364 |
| §9.2 load and markers | #warping through #saving-warp-markers-with-a-sample-file; WFW:B031–B063, HTML364–428 |
| §9.2 short and long editing | #warping-short-samples through #quantizing-audio; WFW:B064–B104, HTML428–592 |
| §9.3 mode controls | #warp-modes through #complex-and-complex-pro-mode; WFW:B105–B131, HTML592–622 |

[Counts](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/counts.json)
and [frozen manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/warping-workflows/manifest-author-r1.json)
identify the bounded review packet. The read-only validator checks integrity,
references, snapshots, local links/anchors, exact browser ID equality and authored
whitespace. It never writes reports after the seal. Author validation is not
independent semantic review or a compatibility result.
