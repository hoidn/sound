---
id: SPEC-MIXING-WORKFLOWS
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 2
target: Ableton Live 12 Suite 12.4.3
---

# Mixer interactions and group presentation

Partial F-08/F-09 contracts for mixer UI/selection/group/remote and track-title
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

This revision preserves all 23 R1 requirements verbatim and adds eight bounded
control/display entry roles. Its 50 future cases include eight action refinements,
17 additions and all 33 original IDs. No runtime or full Mixing closure is claimed.

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

### REQ-MIXING-WORKFLOW-019 — Create-menu track entry points

**D12/target-U.** The Create menu offers new audio and MIDI tracks. The documented audio shortcut is CtrlT on Windows/CmdT on Mac; MIDI is CtrlShiftT/CmdShiftT. This specifies admitted track-creation entries only; Browser content admission, constructor state, counts, focus precedence and signal behavior remain separately owned or unknown.

Evidence: `mixing:B025` HTML408; [retained source](#analysis-only-evidence).

### REQ-MIXING-WORKFLOW-020 — Track-title edit entry points

**D12/target-U.** Clicking a track title selects its track for Edit commands. Rename is offered there, including CtrlR on Windows/CmdR on Mac followed by Tab between titles in a rename series. Edit Info Text is offered in Edit and track context menus. Edit Delete is a track-removal entry; it does not imply source-file deletion. Generic keyboard/text editing, naming grammar, modal interception and history remain with their owners or unknown.

Evidence: `mixing:B029` HTML428, `mixing:B030` HTML428, `mixing:B035` HTML428; [retained source](#analysis-only-evidence).

### REQ-MIXING-WORKFLOW-021 — Track-title edge resize

**D12/target-U.** Dragging a track title bar edge changes track width in Session or track height in Arrangement. This is distinct from resizing mixer meters; no pixel threshold, minimum/maximum, snapping, persistence or accessibility order is specified.

Evidence: `mixing:B031` HTML428; [retained source](#analysis-only-evidence).

### REQ-MIXING-WORKFLOW-022 — Track-title Places save entry

**D12/target-U.** Dragging a track title to a supported Places folder is documented to save it as a new Set and offer a name to type or confirm with Enter. Sample collection remains controlled by the existing Project Media019 preference contract. This adds the track-title entry and naming role only, with no file bytes, copy algorithm, transaction, persistence or source-deletion law.

Evidence: `mixing:B034` HTML428; [retained source](#analysis-only-evidence).

### REQ-MIXING-WORKFLOW-023 — Optional overlevel display role

**D12/target-U.** The mixer chapter describes optional visual overlevel feedback for track signals. Only that display role is retained here. Its numerical threshold, meter calibration/detector, clipping, headroom, internal sample format and external/file results are not supplied as new laws.

Evidence: `mixing:B018` HTML408, `mixing:B019` HTML408, `mixing:B020` HTML408, `mixing:B021` HTML408, `mixing:B022` HTML408; [retained source](#analysis-only-evidence).

### REQ-MIXING-WORKFLOW-024 — Return visibility and creation entries

**D12/target-U.** Return Tracks is offered in View → Mixer Controls for showing/hiding returns; Create → Insert Return Track offers a new return. Existing return/Main routing and no-clip roles remain with Routing027. This adds the entry points, not a resource-count, Main constructor, sum or device law.

Evidence: `mixing:B050` HTML472, `mixing:B056` HTML484; [retained source](#analysis-only-evidence).

### REQ-MIXING-WORKFLOW-025 — Exclusive Arm preference entry

**D12/target-U.** The mixer source identifies an Exclusive Arm option in Record, Warp & Launch Settings. This clause retains its selectable preference role only. Ordinary/modifier/multiselected arm remains Recording001; preference-dependent exclusivity and new/empty MIDI instrument implicit arm remain explicit U probes under the existing Mixing arm unknown.

Evidence: `mixing:B014` HTML386; [retained source](#analysis-only-evidence).

### REQ-MIXING-WORKFLOW-026 — Track Options menu entries

**D12/target-U.** Track Delay is exposed through Track Options in View → Mixer Controls, the bottom-right Mixer Config menu, and View → Arrangement Track Controls. These are separate visibility entries. Routing034 owns units and the documented unavailable state with Delay Compensation off; no delay conversion, timing or compensation arithmetic is added.

Evidence: `mixing:B082` HTML562, `mixing:B083` HTML562, `mixing:B084` HTML580, `mixing:B085` HTML590, `mixing:B087` HTML590; [retained source](#analysis-only-evidence).

## Cases and unknown outcomes

The current [50 cases](../../analysis/ableton-live-12.4.3/full-spec-v1/mixing-workflows/cases-r2.json)
cover 31 requirements. [Finite contexts](../../analysis/ableton-live-12.4.3/full-spec-v1/mixing-workflows/finite-contexts-r2.json)
name the refined/new gestures, view/platform/preference populations and separate
positive histories; they are future proposals, not executions. The original
33 IDs remain, with eight setup/action refinements only. Every original
source_claim, documentary expectation/comparator, target oracle and execution
flag remains unchanged. There are 21 named visible documentary roles and
29 null documentary outcomes; all 50 actual expectations/comparisons are null,
target U and unexecuted. Signal, transform, file, timing and unknown outcomes
are never inferred from a control label or a successful integrity check.

[Current prerequisites](../../analysis/ableton-live-12.4.3/full-spec-v1/mixing-workflows/fixtures-r2.json)
require independently valid owned backed-up disposable state, admitted exact
controls/focus/platform and genuinely productive operation before any absence
comparison. A mapped key must actually change the admitted value independently
before a two-key held sequence; stopping requires genuinely playing nonempty
child clips. Implicit-arm trials require genuinely unarmed new/empty eligible
MIDI tracks and an actually accepted compatible instrument on matched positive
resets. Solo comparisons need working nonzero clip/return/send paths, respective
outputs and admitted noncenter pan. Missing, silent, muted, dry-only, unavailable
or unsupported contexts remain U, never a successful negative result. No future
file/deletion/recording/control proposal is an operation performed here.

MXW-012 preserves the known member track, both distinct clip populations and a
nonmember control across reset active views. MXW-006 preserves nonadjacent A/C
drag versus admitted Ctrl-arrow, adding explicit adjacent Shift/nonadjacent Ctrl
selection without a Cmd alias. MXW-008 retains one clip; MXW-027 separately uses
two clips from the same known source track in each view. Generic malformed,
boundary, save/Undo/cancel/source-loss/teardown histories remain U; the new held-key
Undo history has no source-backed restoration law. The old generic U templates
do not establish every control's lifecycle or engine/rate behavior.

## Source contexts and owner boundaries

Q046 remains open. The new Exclusive Arm clause specifies only the preference
control; implicit/exclusive arm outcomes remain under the existing arm unknown,
without changing Recording001. Mixing B043 populated-slot wording and Session006
empty-slot stop context remain separate. New group stop/folder probes supply
productive child/receiver histories but no routing/stop/timing law. B066/067
unnamed half-range prose cannot choose a curve or override the seven finite
functions. Enable Send admission is not ALS EnabledByUser/engine-active identity.

[Browser010](browser-workflows.md) retains loading into an already selected track;
new-track Browser admission remains a separate U probe. [Project Media019](project-media-workflows.md)
retains collection choices and copy/reference behavior: this page adds only the
track-title Places entry/naming role. Generic text/focus/keyboard commands remain
with [keyboard navigation](keyboard-navigation.md). Monitoring/record gates,
selected Monitor behavior and default contexts remain with [routing](routing-monitoring-latency.md)
and [recording](recording-comping.md); recommendation-only software-instrument/effect
versus acoustic/external-monitor histories do not impose a mandatory setting or
claim the existing monitor matrix is missing. Routing034/054 remains the owner of
Track Delay units and observable compensation-OFF unavailability; the new clause
adds separate menu entries, not compensation arithmetic. Headroom32bit/CPU advice,
source adjectives and uninspected charts add no algorithm, threshold or guarantee.

## Analysis-only evidence

The exact retained current Version12 Mixing chapter is identified by
[source.json](../../analysis/ableton-live-12.4.3/full-spec-v1/mixing-workflows/source.json):
URL `https://www.ableton.com/en/live-manual/12/mixing/`, capture
`2026-10-19T21:33:28.556179+00:00`, 276916 bytes, SHA256
`255923c650a256ea0c663e83351e3ac0d8f14ba8dfe12706825754b2066de02e`.
Its original bounded-gap scope metadata remains historical and unchanged.
[94 source blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/mixing-workflows/source-blocks.json)
retain exact lines/literal anchors and heading context; a paragraph's null anchor
is not replaced by its ancestor. All text was read; 21 image pixels/chart and
14 linked destinations remain uninspected. Publication Version12 is not exact
12.4.3 behavior proof. The [approved full retained-source audit](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/mixing-source-audit-review.json)
identifies gaps; this separately reviewable successor adopts only the bounded
roles/actions recorded in [17 group dispositions](../../analysis/ableton-live-12.4.3/full-spec-v1/mixing-workflows/audit-adoption-r2.json).
Fourteen groups receive local role/action subsets; M09/M10/M17 receive only U
cross-owner/recommendation histories. No group is fully closed.

[Requirements](../../analysis/ableton-live-12.4.3/full-spec-v1/mixing-workflows/requirements-r2.json),
[delta](../../analysis/ableton-live-12.4.3/full-spec-v1/mixing-workflows/delta-r2.json),
[immutable inputs](../../analysis/ableton-live-12.4.3/full-spec-v1/mixing-workflows/inputs-r2.json),
[consumer impact](../../analysis/ableton-live-12.4.3/full-spec-v1/mixing-workflows/consumer-impact-r2.json)
and [R2 manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/mixing-workflows/manifest-author-r2.json)
retain history and checks. Root owns downstream historical replay. No frozen
consumer or original R1 byte was edited, and this packet does not rerun the
historical R1 validator against changed canonicals. Independent R2 review is
required; the author does not approve this successor.

## Revision history

| Revision | Scope |
| --- | --- |
| 1 | Historical 23 requirements/33 cases, independently reviewed as partial; all source and payload bytes remain at original paths. |
| 2 | 31 requirements/50 cases; eight old action-only refinements and 17 additions from the full retained audit, with finite positive histories and remaining U contexts. Independent review pending. |
