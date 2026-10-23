---
id: SPEC-MIXING-WORKFLOWS
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3
---

# Mixer interactions and group presentation

Partial F-08/F-09 contracts for additional mixer UI/selection/group/remote
entrypoints from the retained Mixing chapter. D12 is current Version12 publication
text only; all exact12.4.3 outcomes remain U. No original function/application,
UI/audio/MIDI/API/Max/hardware/candidate operation or source example ran.

[Mix graph](mix-graph.md) and [mixer values](mixer-values.md) own finite signal,
values/units/curves/storage laws. [Routing](routing-monitoring-latency.md) owns
routing/cue/send taps/meters/track-delay policy; [recording](recording-comping.md)
owns arm/monitor/record gates; [Session](session-view-workflows.md) owns group
slots/scenes. [Keyboard](keyboard-navigation.md), [remote](remote-control-workflows.md),
[Clip View](clip-view-workflows.md), [automation](automation-workflows.md),
[racks](device-racks.md), [projects](project-media-workflows.md) and
[engine](engine-resource-workflows.md) retain detailed focus/mapping/metadata/
processing/persistence/lifecycle laws. No duplicate algorithm or unqualified
signal law is introduced by these entrypoints.

## Documentary requirements

### REQ-MIXING-WORKFLOW-001 — Mixer visibility and components

**D12/target-U.** Mixer controls are available from Session and Arrangement; the bottom-right mixer control shows/hides the section, with its adjacent menu controlling component visibility. Arrangement also offers Track Controls. No geometry, accessibility order or persistence law is supplied.

Evidence: `mixing:B003` HTML280, `mixing:B004` HTML302, `mixing:B005` HTML324, `mixing:B006` HTML346, `mixing:B007` HTML358; [retained source](#analysis-only-evidence).

### REQ-MIXING-WORKFLOW-002 — Resizable meter presentation

**D12/target-U.** Increasing mixer height reveals tick marks, numeric volume and resettable peak-level indicators; increased track width adds a decibel scale. These are presentation roles, with no pixel thresholds, calibrated detector or reset duration.

Evidence: `mixing:B016` HTML408, `mixing:B017` HTML408; [retained source](#analysis-only-evidence).

### REQ-MIXING-WORKFLOW-003 — Selected mixer controls move together

**D12/target-U.** With multiple tracks selected, editing one mixer control edits that control for the selected tracks. The source describes preserving existing knob/slider differences; coordinates/units, clamping, boundary interactions and exact transformations remain unknown. Existing mixer values own numeric laws.

Evidence: `mixing:B010` HTML386, `mixing:B011` HTML386, `mixing:B012` HTML386, `mixing:B033` HTML428; [retained source](#analysis-only-evidence).

### REQ-MIXING-WORKFLOW-004 — Pan mode menu and reset gestures

**D12/target-U.** Pan context menu chooses Stereo versus Split Stereo presentation; Split offers independent left/right controls. Double-clicking Pan or clicking its triangle in the Session/Arrangement mixer resets to the described default. Numeric defaults, ramps and stereo processing remain with mixer values.

Evidence: `mixing:B011` HTML386; [retained source](#analysis-only-evidence).

### REQ-MIXING-WORKFLOW-005 — Exclusive and multiselected Solo controls

**D12/target-U.** Solo supports selected-track sets. Outside that multi-selection context, ordinary exclusivity is bypassed by Ctrl on Windows/Cmd on Mac or disabled Exclusive Solo preference. S invokes the solo shortcut in an eligible focus context owned by keyboard/remote control. Arbitrary routed graph muting remains separately owned.

Evidence: `mixing:B013` HTML386; [retained source](#analysis-only-evidence).

### REQ-MIXING-WORKFLOW-006 — Nonadjacent track move context

**D12/target-U.** Adjacent/nonadjacent selection is described with Shift/Ctrl-click. Dragging nonadjacent tracks collapses them together at drop; Ctrl+arrow moves without collapsing. This paragraph does not qualify Ctrl by platform, so no Cmd substitution or complete focus/ordering grammar is inferred.

Evidence: `mixing:B031` HTML428, `mixing:B032` HTML428; [retained source](#analysis-only-evidence).

### REQ-MIXING-WORKFLOW-007 — Track numbering names

**D12/target-U.** A leading # produces an automatically updated track number when moved; extra # characters add leading zeros. Prefix parsing beyond this example, numbering basis, interaction with renaming/history and exact rendered text remain unknown.

Evidence: `mixing:B029` HTML428, `mixing:B030` HTML428; [retained source](#analysis-only-evidence).

### REQ-MIXING-WORKFLOW-008 — Clip drag to a new track

**D12/target-U.** Dragging one or multiple existing clips into empty space right of Session tracks or below Arrangement tracks creates a new track carrying those clips and the original track devices. This does not establish device-copy state, mappings, media bytes, source ownership or processing equivalence.

Evidence: `mixing:B027` HTML408; [retained source](#analysis-only-evidence).

### REQ-MIXING-WORKFLOW-009 — Group creation and nesting

**D12/target-U.** Group Tracks combines selected audio/MIDI tracks, including existing groups nested in a new group. Groups have mixer controls and can host audio effects but cannot contain clips. Group routing is owned by routing-monitoring; Session group slots remain their own owner.

Evidence: `mixing:B037` HTML428, `mixing:B038` HTML428, `mixing:B039` HTML428; [retained source](#analysis-only-evidence).

### REQ-MIXING-WORKFLOW-010 — Group folding and Arrangement overview

**D12/target-U.** Unfold Group shows/hides contained tracks; Arrangement groups show an overview of contained clips. Hidden tracks are not inferred inactive, and overview graphics are not playable group clips or timing/audio proof.

Evidence: `mixing:B040` HTML428, `mixing:B042` HTML440; [retained source](#analysis-only-evidence).

### REQ-MIXING-WORKFLOW-011 — Group movement, deletion and ungrouping

**D12/target-U.** Tracks may be dragged into/out of a group. Deleting a group deletes its contents; Ungroup Tracks restores individual tracks. Exact nested deletion/selection, Undo/media deletion and rerouting are not supplied.

Evidence: `mixing:B041` HTML440; [retained source](#analysis-only-evidence).

### REQ-MIXING-WORKFLOW-012 — Group color applies to active view clips

**D12/target-U.** Assign Track Color to Grouped Tracks and Clips applies group color to contained tracks and clips. In Session it affects Session clips; in Arrangement it affects Arrangement clips. Nested/selected subsets and palette equality remain unresolved.

Evidence: `mixing:B044` HTML460, `mixing:B045` HTML460; [retained source](#analysis-only-evidence).

### REQ-MIXING-WORKFLOW-013 — Group descendant solo indicator

**D12/target-U.** A group Solo button appears half colored when a child track or nested group is soloed. The source supplies no exact RGB/pixel measure or complete status precedence.

Evidence: `mixing:B046` HTML460; [retained source](#analysis-only-evidence).

### REQ-MIXING-WORKFLOW-014 — Return Send enable entrypoints

**D12/target-U.** Return Send knobs are documented disabled by default, with Enable Send/Enable All Sends in their context menu. This is a control admission description; no identity with stored EnabledByUser or active-bit derivation, feedback stability or audible send is established.

Evidence: `mixing:B053` HTML484; [retained source](#analysis-only-evidence).

### REQ-MIXING-WORKFLOW-015 — Crossfader visibility and curve choice

**D12/target-U.** Crossfader visibility is offered via Mixer Controls or the mixer-control menu; its context menu offers seven curves. The uninspected chart is not a numerical curve source. Existing mixer values retain names/codes/curve functions and assignment laws.

Evidence: `mixing:B058` HTML484, `mixing:B059` HTML500, `mixing:B060` HTML512; [retained source](#analysis-only-evidence).

### REQ-MIXING-WORKFLOW-016 — Crossfader mapping gesture contexts

**D12/target-U.** The main slider and absolute left/right positions are separately assignable. The source describes a key assigned to any of left/center/right fields toggling absolute endpoints and two-field held-key press/release snap-back. Focus, repeat, overlapping input and restoration order remain unknown.

Evidence: `mixing:B061` HTML532, `mixing:B062` HTML532, `mixing:B063` HTML532; [retained source](#analysis-only-evidence).

### REQ-MIXING-WORKFLOW-017 — Crossfader automation entrypoints

**D12/target-U.** Crossfader gestures can be recorded into Arrangement; track assignment edits use Mixer then X-Fade Assign in envelope choosers. This adds the editing entrypoint, not automation timebase, override, persistence or audio coefficients.

Evidence: `mixing:B069` HTML548; [retained source](#analysis-only-evidence).

### REQ-MIXING-WORKFLOW-018 — Solo in Place and return-solo contexts

**D12/target-U.** Solo in Place is offered in Solo context menu and as an Options default. Soloed clip tracks can leave returns audible in that context; return solo mutes other main outputs while preserving arriving sends. Routing exceptions in the source and existing finite assumptions prevent an all-graph solo law.

Evidence: `mixing:B071` HTML548, `mixing:B072` HTML548; [retained source](#analysis-only-evidence).

### REQ-MIXING-WORKFLOW-U-MULTI — Multi-control units, name/order and focus

**U/target-U.** Relative multi-edit units/clamping, mixed pan modes, prefix numbering grammar, drag/device state and Ctrl/platform/focus histories remain unknown.

### REQ-MIXING-WORKFLOW-U-GROUP — Group scope and source contexts

**U/target-U.** Group slot launch/stop context in Mixing B043 versus existing Session group-slot owner, nesting/media/Undo/move/ungroup and color/solo precedence remain unknown.

### REQ-MIXING-WORKFLOW-U-ARM — Arm preference and implicit-arm context

**U/target-U.** Mixing B014 documents Exclusive Arm and new/empty MIDI instrument implicit arm; recording REQ001 retains preference/implicit-arm U. Preserve this new source context without silently revising that sealed owner.

### REQ-MIXING-WORKFLOW-U-CROSSFADE — Curve and remote gesture context

**U/target-U.** B066/067 describes unattenuated half ranges without naming a curve; existing finite seven-curve functions differ. Keep source/curve context U and do not replace numeric laws. Keyboard held-input and automation histories remain unknown.

### REQ-MIXING-WORKFLOW-U-LIFECYCLE — Build, state and processing lifecycle

**U/target-U.** Exact12.4.3 controls/defaults, malformed inputs, permissions/source loss, cancellation, undo/persistence, event ordering, active audio/MIDI/rate changes and teardown remain required unknowns.

## Cases and unresolved source contexts

[33 proposals](../../analysis/ableton-live-12.4.3/full-spec-v1/mixing-workflows/cases.json)
cover18 documentary roles and15 U histories across23 requirements. Visible role
comparators do not grade numeric differences, naming grammar, pixels, meter
calibration, audio/MIDI or timing. All transforms/signal and U documentary
expectations/comparators remain null; every target expectation/comparison is
null/U/unexecuted. [Setups](../../analysis/ableton-live-12.4.3/full-spec-v1/mixing-workflows/fixtures.json)
require independent valid controls and positive active source/path where relevant.
No track/group/file was deleted or modified during this documentary work.

Mixing B066/067 half-range prose cannot override seven finite curve functions.
B014 new implicit-arm/preference context is retained for the recording owner,
not silently published over its U clause. B043 group slot context stays with the
Session owner. B053 control enablement does not establish ALS EnabledByUser or
engine send-active identity. These contexts and all new lifecycle branches remain U.

## Analysis-only evidence

Official [Version12 Mixing](https://www.ableton.com/en/live-manual/12/mixing/),
original captureUTC2026-10-19T21:33:28.556179+00:00,276916bytes,SHA-256
`255923c650a256ea0c663e83351e3ac0d8f14ba8dfe12706825754b2066de02e`.
[Exact retained HTML](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-12-mixing-2026-10-19.html)
is reused unchanged. [Source identity](../../analysis/ableton-live-12.4.3/full-spec-v1/mixing-workflows/source.json)
keeps its original gap-capture scope label as history, not a recapture or authority
for all chapter claims. [All94 blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/mixing-workflows/source-blocks.json)
retain HTML lines/anchors; root read every block, with figures/chart uninspected.
[Research](../research/mixing-workflows.md) owns routing/context interpretation.
[Author seal](../../analysis/ableton-live-12.4.3/full-spec-v1/mixing-workflows/manifest-author-r1.json)
freezes only this partial scope for independent review.
