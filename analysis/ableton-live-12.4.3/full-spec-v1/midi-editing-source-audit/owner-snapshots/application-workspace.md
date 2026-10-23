---
id: SPEC-APPLICATION-WORKSPACE
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3
---

# Shared workspace controls and feedback

This partial F-08 contract adds Control Bar grouping/global scale-selection,
Status Bar feedback, paired-window view switching and track-title view entry
predicates. The [coverage design](../research/full-live-specification-design.md)
governs closure; [research](../research/application-workspace.md) owns sources and
owner routing. It is not a complete UI, layout, scale or source-chapter contract.

**D12/target-U:** current Version12 documentary roles only. All exact12.4.3
expected/comparison fields remain null/U/unexecuted. No UI, original function,
audio/MIDI/API, update/network, hardware or candidate ran. Figures were not
inspected. Timing/signal outputs are source_claim only, not graded oracles.

## Canonical owners

[Keyboard navigation](keyboard-navigation.md) owns focus/traversal, Tab preference,
single-window switching and platform shortcuts; this adds only paired-window
swap. [Clip View](clip-view-workflows.md) owns stacking and perclip properties;
[MIDI editing](midi-editing-tools.md) owns note/scale/folding values and operations.
This adds global selection/default context and Status Bar presentation only.
[Tuning](tuning-systems.md), [native MIDI effects](native-midi-effects.md),
[modulation](modulation-pitch-loop-devices.md) and [synthesis](synthesis-instruments.md)
retain actual scale-aware device/tuning roles, not a new pitch conversion here.

[Transport](transport-state.md), [launch](session-launch-workflows.md),
[recording](recording-comping.md), [automation](automation-workflows.md),
[Arrangement](arrangement-editing.md), [routing](routing-monitoring-latency.md),
[device hosting](bundled-device-hosting.md), [Browser](browser-workflows.md),
[projects](project-media-workflows.md), [media](media-file-workflows.md),
[export](audio-video-export.md), [settings](settings-learning-workflows.md),
[engine/resource](engine-resource-workflows.md) and [delivery](delivery-recovery-workflows.md)
retain their detailed controls/operations. Control Bar grouping and overview
examples neither duplicate their laws nor close the other Concepts sections.

## Requirements

Use [future owned setups](../../analysis/ableton-live-12.4.3/full-spec-v1/live-concepts/fixtures.json)
with explicit selection/preferences/focus/feature availability and positive
active source/output where relevant. Compound branches require individual
evidence; no single UI observation closes an error, output or lifecycle branch.

### REQ-WORKSPACE-CONTROL-001 — Control Bar grouping

**D12/target-U.** The chapter groups Control Bar roles into nine named sections: Browser Options; Tempo Settings and Metronome; Scale Settings; Follow and Arrangement Position; Transport Controls; Automation and Capture MIDI; Arrangement Loop Settings; MIDI and CPU Settings; View Selector. This is a documentary grouping, not pixel/order/visibility geometry or a new definition of the domain controls.

Evidence: `CONCEPT-B004`, `CONCEPT-B005`, `CONCEPT-B006`, `CONCEPT-B007`, `CONCEPT-B008`, `CONCEPT-B009`, `CONCEPT-B010`, `CONCEPT-B011`, `CONCEPT-B012`, `CONCEPT-B013`, `CONCEPT-B014`; [exact routes](#analysis-only-evidence).

### REQ-WORKSPACE-CONTROL-002 — Shared scale selection and future clips

**D12/target-U.** Control Bar scale controls reflect the selected clip and offer Scale Mode, Root Note and Scale Name. With no clip selected, chosen scale settings apply to subsequently created clips. This adds the global selection/default context to Clip View properties; accepted scale lists, data codec, preference scope and numerical pitch transforms remain with existing owners or unknown.

Evidence: `CONCEPT-B008`, `CONCEPT-B074`, `CONCEPT-B075`, `CONCEPT-B076`; [exact routes](#analysis-only-evidence).

### REQ-WORKSPACE-CONTROL-003 — Scale controls with multiple clips

**D12/target-U.** Control Bar Scale controls can turn Scale Mode on/off or set the same scale for multiple selected clips. Mixed audio/MIDI selections, incompatible tuning, empty-slot versus existing-clip propagation and merge/display precedence remain unknown. This does not redefine perclip Scale or a device retuning law.

Evidence: `CONCEPT-B076`; [exact routes](#analysis-only-evidence).

### REQ-WORKSPACE-CONTROL-004 — Status messages and update context

**D12/target-U.** Status Bar can display error information and available-release updates, the latter in the documented Automatic Updates enabled context. Error wording, severity, retention, availability checks, update protocol/consent and whether other notifications appear are unknown; delivery owns update operations.

Evidence: `CONCEPT-B016`; [exact routes](#analysis-only-evidence).

### REQ-WORKSPACE-CONTROL-005 — Selected-note Status Bar details

**D12/target-U.** With a selected MIDI Note Editor note, Status Bar provides its location, pitch, velocity and probability details. Numeric encoding, pitch naming, formatting, rounding, multi-selection aggregation and update deadlines remain unknown; note values/editing remain MIDI-owner contracts.

Evidence: `CONCEPT-B017`; [exact routes](#analysis-only-evidence).

### REQ-WORKSPACE-CONTROL-006 — Insert-marker hover feedback

**D12/target-U.** Hovering an actually offered insert marker in the documented Session/Arrangement context displays its location in Status Bar. Which Session/editor marker is intended, exact location grammar/precision, hidden-marker handling and focus/hover timing remain unknown; no marker coordinate formula is inferred.

Evidence: `CONCEPT-B017`; [exact routes](#analysis-only-evidence).

### REQ-WORKSPACE-CONTROL-007 — Two-window view swap

**D12/target-U.** With two Live windows and Use Tab Key to Navigate disabled, Tab swaps Session and Arrangement between the windows. Existing keyboard-navigation owns the one-window Tab switch, preference-conditioned focus traversal and platform view shortcuts; this adds only the paired-window swap context.

Evidence: `CONCEPT-B034`; [exact routes](#analysis-only-evidence).

### REQ-WORKSPACE-CONTROL-008 — View switching versus playing state

**D12/target-U.** The chapter describes Session/Arrangement view switching during playback/recording as a UI change that does not change the currently playing clips. It does not specify sample continuity, a no-glitch deadline, record event ordering or arbitrary UI-command independence; transport/launch/record owners retain those laws.

Evidence: `CONCEPT-B035`, `CONCEPT-B036`; [exact routes](#analysis-only-evidence).

### REQ-WORKSPACE-CONTROL-009 — Track-title Device View entry

**D12/target-U.** Double-clicking a track title opens Device View for its device chain. This adds an entry gesture, not device insertion/classification/routing or clip/device stack behavior. Generic device focus remains with keyboard-navigation and stacking/Clip View selection with Clip View.

Evidence: `CONCEPT-B063`; [exact routes](#analysis-only-evidence).

### REQ-WORKSPACE-CONTROL-U-SCALE — Scale propagation and folding contexts

**U/target-U.** Global no-selection/future-clip/empty-slot propagation, mixed-selection state, Fold to Scale exceptions, scale-aware device/MIDI-tool conversion and tuning interactions remain unresolved beyond linked owners.

### REQ-WORKSPACE-CONTROL-U-FEEDBACK — Status and control feedback limits

**U/target-U.** Error/update, marker/note field grammar, multi-selection/hidden/focus contexts, warnings and inaccessible or unavailable controls have no complete feedback oracle.

### REQ-WORKSPACE-CONTROL-U-WINDOWS — Workspace layout and window outcomes

**U/target-U.** Window creation/closure, selected-view conflicts, minimization, displays/scaling, unavailable shortcuts, focus restoration and layout persistence remain required unknowns.

### REQ-WORKSPACE-CONTROL-U-LIFECYCLE — Workspace failures and lifecycle

**U/target-U.** Undo/redo/cancel, invalid/unsupported settings, object/media/device loss, audio-rate/engine/transport changes, concurrent controls and teardown remain unknown.

## Source-context questions

**WORKSPACE-U-SCALE-HISTORY:** CONCEPT-B008 mentions subsequently created clips
or selected slots; B075 explicitly describes no-selection/future creation. This
does not establish that selecting any existing clip overwrites its scale.

**WORKSPACE-U-FOLD:** B077 describes only scale rows, while REQ-MIDI-EDIT-017
retains an out-of-scale-note visibility exception. Preserve overview/detailed
contexts; the existing owner remains authoritative for its partial scope.

**WORKSPACE-U-MARKER:** B017's Session/Arrangement insert-marker context needs
an actually offered marker/editor and coordinate-system match. No synthetic
marker, exact location grammar or absent-control rejection is inferred.

## Finite acceptance proposals

[23 cases](../../analysis/ableton-live-12.4.3/full-spec-v1/live-concepts/cases.json)
cover9D12roles/14operational U probes for13requirements (9D12/4U). Eight
documentary visible-control/state proposals have named role expectations;
the timing case and all14U cases have null documentary outputs/comparators.
All23target outputs/comparisons are null/U/unexecuted; setups are future,
not retained UI/media or compatibility results.

## Analysis-only evidence

Official [current Version12 Concepts](https://www.ableton.com/en/live-manual/12/live-concepts/), captureUTC
2026-10-19T22:23:42.054730+00:00, 306807bytes, SHA-256 `611eeb0d7ffa1cb63aacd5bafbfbb3e60803836f4ca02f0e4aabb017fb7cf5c9`;
[exact HTML](../../analysis/ableton-live-12.4.3/full-spec-v1/live-concepts/manual-live-concepts-2026-10-19.html).
[125 blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-concepts/source-blocks.json)
retain anchors/HTML lines; figures uninspected and patch applicability unknown.
The parser is pinned in dependencies.json. An earlier distinct Concepts capture
remains preserved in the Arrangement packet; it is not this byte identity and
is not silently replaced. [Requirements](../../analysis/ableton-live-12.4.3/full-spec-v1/live-concepts/requirements.json)
and [author seal](../../analysis/ableton-live-12.4.3/full-spec-v1/live-concepts/manifest-author-r1.json)
freeze only the new predicates. Other chapter material is routed, not declared
specified completely or nonbehavioral from its overview title.
