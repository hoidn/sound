---
id: SPEC-SESSION-VIEW-WORKFLOWS
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3
---

# Session View grid, scenes and presentation

This partial F-04/F-08 draft owns Session grid/scene gestures, selection,
metadata, scene assignment controls, Track Status and cross-view scene workflows.
[Coverage design](../research/full-live-specification-design.md) governs closure;
[research](../research/session-view-workflows.md) owns source interpretation.
It is not a complete Session specification or a released implementation input.

**D12/target-U:** the retained official Version12 chapter supplies documentary
behavior, not observed Live12.4.3 outcomes. Every target expectation/comparison
is null, every target grade U and every case unexecuted. U never passes. Named
choices and visible state proposals have documentary comparators only; no audio,
clock, numeric grammar, pixel, hidden-buffer or candidate architecture is imposed.

[Clip launch](clip-launch.md) owns launch modes, quantization, Legato, velocity
and Follow Actions; [playback](playback-core.md) and [transport](transport-state.md)
own finite timing computations. This draft does not resolve their unknowns.
[Arrangement](arrangement-editing.md) REQ020/021 owns Session override and Back
to Arrangement; REQ009/010 owns consolidation signal/destination. [Recording](recording-comping.md)
REQ031 owns Session performance recording, including the retained scene-name
qualifier; scene-field recording without that qualifier remains U.
[Set structure](live-set-structure.md) owns storage/scene identities, which are
distinct from position-based UI numbers. [MIDI mapping](midi-user-mapping.md),
[keyboard navigation](keyboard-navigation.md), [media](media-file-workflows.md)
and [Clip View](clip-view-workflows.md) retain their bounded owners. A link does
not establish composed behavior, focus precedence or version applicability.

## Requirements and finite cases

Use the [future fixture](../../analysis/ableton-live-12.4.3/full-spec-v1/session-workflows/fixtures.json)
with per-case mode/preference/focus overrides, reset histories and independently
confirmed active/nonzero output before any no-effect or continuity claim.
The [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/session-workflows/cases.json)
retains full finite actions and documentary expectations; the table is an index,
not evidence of exhaustive mode coverage. Compound requirements need additional
per-branch cases before coverage closure. Migration/media inputs are future
prerequisites, not existing captured fixtures or measured outputs.

### REQ-SESSION-VIEW-001 — Clip launch gestures

**D12/target-U.** The triangular clip button requests playback; selecting a clip by name then Enter also launches it, and arrows move to neighboring clips. Grid position does not prescribe playback order. Launch mode/quantization arithmetic remains owned by SPEC-CLIP-LAUNCH and SPEC-PLAYBACK-CORE.

Evidence: `SV-B008`, `SV-B012`; [source blocks](#analysis-only-evidence).

### REQ-SESSION-VIEW-002 — Clip stop and deactivate contexts

**D12/target-U.** Square Clip Stop controls exist in slots and Track Status. Pressing 0 on selected Session clips deactivates those clips. Stopping a Session clip leaves global Play highlighted and song position advancing. Reactivation/toggle policy is not stated here.

Evidence: `SV-B009`, `SV-B010`, `SV-B013`; [source blocks](#analysis-only-evidence).

### REQ-SESSION-VIEW-003 — Global double Stop

**D12/target-U.** Pressing the Control Bar Stop button twice stops playback of the whole Set and returns Arrangement Position to 1.1.1. Single-stop/continue arithmetic remains in transport/playback contracts.

Evidence: `SV-B014`; [source blocks](#analysis-only-evidence).

### REQ-SESSION-VIEW-004 — Session clip metadata

**D12/target-U.** Edit/menu-context Rename handles clips and multiple selected clips; Edit Info Text supplies clip annotation and context color palette supplies custom clip color. Text grammar, maximum lengths and multi-selection value conflicts are unknown.

Evidence: `SV-B015`; [source blocks](#analysis-only-evidence).

### REQ-SESSION-VIEW-005 — Grid selection and moving

**D12/target-U.** Drag/drop moves clips in the grid. Shift or platform Ctrl/Cmd supports multi-clip selection before dragging; dragging from an empty slot can rubber-band select. The introductory paragraph names Ctrl without a platform qualifier; platform-specific modifier interpretation remains uncertain outside the explicitly qualified grid paragraph.

Evidence: `SV-B016`, `SV-B054`; [source blocks](#analysis-only-evidence).

### REQ-SESSION-VIEW-006 — Group slots

**D12/target-U.** A group slot is shaded when contained tracks have at least one clip in that scene, using the left-most clip color. Its launch control launches the corresponding clips; a group slot with no corresponding clips has a stop control. Clicking a group slot selects the referred clips.

Evidence: `SV-B017`; [source blocks](#analysis-only-evidence).

### REQ-SESSION-VIEW-007 — Track clip exclusivity

**D12/target-U.** A Session track plays only one clip at a time; alternative material belongs in that track's column. Voice tails, instruments and routed audio are not an extra clip playback instance.

Evidence: `SV-B019`; [source blocks](#analysis-only-evidence).

### REQ-SESSION-VIEW-008 — Track width gestures

**D12/target-U.** Drag title-bar edges to resize Session tracks; Alt on Windows or Option on Mac while resizing one track resizes all Session tracks. Narrow presentation retains clip launch and essential track controls; minimum size and exact pixel layout are unknown.

Evidence: `SV-B020`; [source blocks](#analysis-only-evidence).

### REQ-SESSION-VIEW-009 — Track-header deactivation

**D12/target-U.** With a Session track header selected, 0 deactivates that track. This context differs from selected-clip deactivation; the manual does not specify an activation toggle or selection precedence with a text editor focused.

Evidence: `SV-B021`; [source blocks](#analysis-only-evidence).

### REQ-SESSION-VIEW-010 — Scene launch and cancellation

**D12/target-U.** A Scene Launch control in the Main-track column launches the clips in its row together. Cancel Scene Launch in the Main-track context menu cancels a previously triggered scene launch. Exact cancellation deadline and already-committed launch behavior are unknown.

Evidence: `SV-B022`; [source blocks](#analysis-only-evidence).

### REQ-SESSION-VIEW-011 — Next-scene selection preference

**D12/target-U.** After a scene launch the scene below is selected as the next to launch unless Select Next Scene on Launch in Launch Settings is Off. Last-scene wrap/creation, empty scenes and concurrent selection edits are unknown.

Evidence: `SV-B023`; [source blocks](#analysis-only-evidence).

### REQ-SESSION-VIEW-012 — Scene metadata commands

**D12/target-U.** Scene Rename is available in Edit/context menus and Tab can advance through successive scene renames. Edit Info Text supplies annotation; a context palette supplies color. Scene View title context also offers Rename/color for one or multiple selected scenes. Multi-scene naming transformation and platform/focus preferences remain unknown.

Evidence: `SV-B024`, `SV-B044`; [source blocks](#analysis-only-evidence).

### REQ-SESSION-VIEW-013 — Scene ordering and position numbers

**D12/target-U.** Scene drag/drop reorders rows. Shift-click selects adjacent scenes; Ctrl-click selects nonadjacent scenes in the retained text. Dragging nonadjacent scenes collapses them together; Ctrl+Up/Down moves them without collapsing. Scene numbers reflect current row position rather than stable identity. OS modifier substitution and boundary behavior are unknown.

Evidence: `SV-B025`, `SV-B026`; [source blocks](#analysis-only-evidence).

### REQ-SESSION-VIEW-014 — Scene tempo/meter editing

**D12/target-U.** Dragging the Main-title left edge reveals scene tempo/meter controls, documented hidden by default. Values can be dragged or typed then Enter, and edited in Scene View. Launching a scene with assigned values adjusts project tempo/meter. This is a Version12 documentary claim; target storage and scheduler behavior remain separate.

Evidence: `SV-B028`, `SV-B029`, `SV-B030`, `SV-B031`; [source blocks](#analysis-only-evidence).

### REQ-SESSION-VIEW-015 — Scene documented numeric domain

**D12/target-U.** The captured manual permits scene tempo20-999 BPM and meter numerator1-99 with denominator1,2,4,8,16. These are documentary UI domains, not a replacement for SPEC-TRANSPORT-STATE's narrower evidence on numeric storage, parsing or scheduling.

Evidence: `SV-B032`; [source blocks](#analysis-only-evidence).

### REQ-SESSION-VIEW-016 — Disable/reset scene assignments

**D12/target-U.** An enabled scene tempo/meter control can be disabled and reset with Return to Default or Delete; double-click disables it. The reset stored numeric value and retention on double-click are not supplied.

Evidence: `SV-B033`; [source blocks](#analysis-only-evidence).

### REQ-SESSION-VIEW-017 — Scene keyboard traversal

**D12/target-U.** Left/right arrows navigate from selected slots/scenes to tempo/meter controls. Within scene name/tempo/meter editing, Tab/Shift-Tab advances/reverses controls and crosses to the next/previous scene at row ends. Enter on a selected tempo/meter control first selects the scene; a second Enter launches it. Keyboard accessibility preference/context interactions remain unproven.

Evidence: `SV-B034`, `SV-B035`; [source blocks](#analysis-only-evidence).

### REQ-SESSION-VIEW-018 — Scene assignment indicator

**D12/target-U.** A scene with assigned tempo and/or meter change has a colored Scene Launch button. The captured text supplies no exact color, contrast, accessibility label or mapping from scene custom color.

Evidence: `SV-B036`; [source blocks](#analysis-only-evidence).

### REQ-SESSION-VIEW-019 — Pre-Live11 scene-name migration

**D12/target-U.** For Sets made before Live11 with tempo/meter in scene names, the manual describes carrying those values into scene controls on opening newer Live and widening Main to expose them. Exact legacy grammar, build boundary, malformed-name handling and migration round trips remain unknown.

Evidence: `SV-B037`; [source blocks](#analysis-only-evidence).

### REQ-SESSION-VIEW-020 — Scene View selection context

**D12/target-U.** Selecting one/multiple scenes, clicking a scene tempo/meter control, or clicking Main title opens Scene View. Its top edits tempo/meter; lower controls expose scene Follow Actions, whose execution belongs to the launch owner. For one selected scene its title shows name/number/color if assigned; multiple scenes show selection count.

Evidence: `SV-B039`, `SV-B040`, `SV-B041`, `SV-B042`, `SV-B043`; [source blocks](#analysis-only-evidence).

### REQ-SESSION-VIEW-021 — Track Status presentation

**D12/target-U.** Looping clips show a pie chart with right-side loop length in beats and left-side number of played loops. A playing group shows a pie without numbers. One-shots show progress and remaining minutes:seconds. Monitored audio/MIDI show microphone/keyboard icons; Arrangement playback shows a miniature Arrangement. Overlapping status precedence and update rounding are unknown.

Evidence: `SV-B046`, `SV-B047`, `SV-B048`, `SV-B049`, `SV-B050`; [source blocks](#analysis-only-evidence).

### REQ-SESSION-VIEW-022 — Multi-file import layout

**D12/target-U.** Browser import or recording can populate Session. Multiple raw audio/MIDI files default to one Session column; Ctrl on Windows or Cmd on Mac before drop spreads them over tracks. This multi-track drop shortcut does not apply to Live Clips with embedded devices. Media decoding and recording remain in their owners.

Evidence: `SV-B052`, `SV-B053`; [source blocks](#analysis-only-evidence).

### REQ-SESSION-VIEW-023 — Select on Launch preference

**D12/target-U.** Clip launch normally selects the clip for Clip View. Turning off Select on Launch in Launch Settings lets the current view/focus remain when clips or scenes launch. This preference is separate from Select Next Scene on Launch.

Evidence: `SV-B056`; [source blocks](#analysis-only-evidence).

### REQ-SESSION-VIEW-024 — Stop-button editing

**D12/target-U.** Edit Add/Remove Stop Button adds/removes grid Clip Stop controls. Removing an empty row/track stop control permits scene launch without affecting that track. Launch scheduling and empty armed-slot recording policy remain owned by launch/recording contracts.

Evidence: `SV-B058`; [source blocks](#analysis-only-evidence).

### REQ-SESSION-VIEW-025 — Insert Scene

**D12/target-U.** Create Insert Scene inserts an empty scene below the current selection. Multi-selection anchor, selection after insert and scene count limits are unknown.

Evidence: `SV-B060`, `SV-B061`; [source blocks](#analysis-only-evidence).

### REQ-SESSION-VIEW-026 — Capture and Insert Scene

**D12/target-U.** Create Capture and Insert Scene inserts below current selection, copies currently running clips into it and launches it. The manual claims no audible interruption; this packet supplies no signal comparator or timing tolerance for that claim. Scene capture is distinct from Capture MIDI and Arrangement Record.

Evidence: `SV-B060`, `SV-B062`; [source blocks](#analysis-only-evidence).

### REQ-SESSION-VIEW-027 — Cross-view clip transfer

**D12/target-U.** Copy/paste and drag permit Session/Arrangement clip transfer, including across separate windows. Arrangement-to-Session paste attempts matching top-to-bottom temporal ordering. Exact tiling, overlaps, metadata transfer and operation atomicity are unknown. Keyboard Second Window controls retain their OS-specific documented modifiers.

Evidence: `SV-B075`, `SV-B076`; [source blocks](#analysis-only-evidence).

### REQ-SESSION-VIEW-028 — Consolidate Time to New Scene

**D12/target-U.** Arrangement Create/context Consolidate Time to New Scene makes one new clip per selected track from the selected time and places them in a new Session scene below prior selected scene. Audio tracks containing at least one selected clip generate new samples. The signal/destination contract for audio consolidation stays in REQ-ARRANGEMENT-010; exact silence-only, MIDI merge and file-failure behavior remain unknown.

Evidence: `SV-B077`; [source blocks](#analysis-only-evidence).

### REQ-SESSION-VIEW-029 — Lifecycle and boundary outcomes

**U/target-U.** Required operational outcomes below remain unknown; documentary gestures and XML structure do not establish them.

| Case | Requirement | Kind / finite action |
| --- | --- | --- |
| SV-001 | REQ-SESSION-VIEW-001 | documented-control: Select owned clip A by name, press Enter, navigate to B with arrows and separately click B's triangular launch control. |
| SV-002 | REQ-SESSION-VIEW-002 | documented-state: With a playing Session clip and global transport, stop it using each square control in separate reset trials; separately select one then two clips and press 0. |
| SV-003 | REQ-SESSION-VIEW-003 | documented-state: Start a disposable Set away from 1.1.1, then press Control Bar Stop twice. |
| SV-004 | REQ-SESSION-VIEW-004 | documented-control: Rename selected clips A/B using Edit and context commands in separate trials; add owned info text and choose an admitted color. |
| SV-005 | REQ-SESSION-VIEW-005 | documented-control: In the five-scene grid select adjacent and nonadjacent clips, then drag them; separately rubber-band from a known empty slot. |
| SV-006 | REQ-SESSION-VIEW-006 | documented-control: Prepare Group G with differently colored clips on two child tracks in scene A, a single child clip in B and no child clips in C; inspect and click each group slot. |
| SV-007 | REQ-SESSION-VIEW-007 | signal-obligation: Use two nonempty distinguishable Session clips in one track; request B while A is playing and separately use another track as a control. |
| SV-008 | REQ-SESSION-VIEW-008 | documented-control: Resize one title edge normally, reset, then resize with the documented OS modifier. |
| SV-009 | REQ-SESSION-VIEW-009 | documented-state: Select a known active track header with no text edit in progress and press 0; use selected-clip context in a separate reset trial. |
| SV-010 | REQ-SESSION-VIEW-010 | documented-control: Set explicit nonzero global quantization and request scene B while transport runs; independently confirm a pending launch before invoking Cancel Scene Launch. If no pending launch can be confirmed, retain U. |
| SV-011 | REQ-SESSION-VIEW-011 | documented-state: With scenes A-E, select B then launch it under preference On; reset and repeat Off with a deliberately different prior selection. |
| SV-012 | REQ-SESSION-VIEW-012 | documented-control: Rename B then advance with Tab using a valid scene-name editing focus; separately annotate/color B and invoke Scene View title context on B/D. |
| SV-013 | REQ-SESSION-VIEW-013 | documented-state: Use five uniquely named scenes A-E. Select B/D; drag them to a distinct interior destination. Reset and move B/D by the stated Ctrl+arrow gesture. Record order and displayed numbers. |
| SV-014 | REQ-SESSION-VIEW-014 | documented-state: Reveal controls in a test-owned fresh Set; assign B tempo120 and meter3/4 by typing, then change via drag in a separate trial; launch B with both assignments explicitly enabled. |
| SV-015 | REQ-SESSION-VIEW-015 | documented-control: Enter20 and999 BPM in separate scenes, then meter1/1 and99/16; enumerate stated denominators with an interior numerator. |
| SV-016 | REQ-SESSION-VIEW-016 | documented-state: Begin with B tempo137/meter3/4 assigned and enabled; independently reset using Return to Default, Delete and double-click in separate restored trials. |
| SV-017 | REQ-SESSION-VIEW-017 | documented-control: With main-window Tab focus navigation enabled where required, select B tempo control; press Enter once then again. Separately edit B name and traverse controls/neighbor scenes using Tab/Shift-Tab. |
| SV-018 | REQ-SESSION-VIEW-018 | documented-control: Use distinct B tempo-only, C meter-only and D both assigned, alongside A with neither assigned; inspect launch controls. |
| SV-019 | REQ-SESSION-VIEW-019 | documented-state: Use a separately identified future owned pre-Live11 Set with known scene-name tempo/meter values; open a disposable copy. No suitable historical fixture is retained by this packet. |
| SV-020 | REQ-SESSION-VIEW-020 | documented-control: Open Scene View via each named context using B and B/D selections; inspect title and both control regions. |
| SV-021 | REQ-SESSION-VIEW-021 | documented-control: Use separate reset looping, one-shot, monitored-audio, monitored-MIDI, group-playing and Arrangement-playing fixtures; inspect Track Status with independently confirmed activity. |
| SV-022 | REQ-SESSION-VIEW-022 | documented-control: Use two independently valid owned raw audio files and separately two MIDI files; drop normally and with the OS modifier into empty slots. Repeat with two independently valid Live Clips. |
| SV-023 | REQ-SESSION-VIEW-023 | documented-state: Focus a return-track device panel; launch B clip and scene in separate trials with Select on Launch Off, then restore the same setup with On for clip launch. |
| SV-024 | REQ-SESSION-VIEW-024 | signal-obligation: Play a nonempty clip on track A; remove the stop control from empty A/sceneC and launch C; compare restored-stop setup in a separate reset trial. |
| SV-025 | REQ-SESSION-VIEW-025 | documented-state: Select single interior scene B in A-E and invoke Create Insert Scene. |
| SV-026 | REQ-SESSION-VIEW-026 | documented-state: Run distinct nonempty clips on A/B tracks, select scene C then invoke Capture and Insert Scene. Capture visible row/content/launch state and audio separately after a paired positive output baseline. |
| SV-027 | REQ-SESSION-VIEW-027 | documented-control: Use two owned clips with separated Arrangement times; copy/paste into empty Session region. Separately drag through view selectors and between enabled main/second windows. |
| SV-028 | REQ-SESSION-VIEW-028 | documented-state: Select owned Arrangement material on audio A and MIDI B over one interior bar; select Session scene C as destination anchor; invoke Consolidate Time to New Scene and inspect scene/clip/file references. |
| SV-U-BOUNDARY | REQ-SESSION-VIEW-029 | boundary: Enter tempo19.999/1000, numerator0/100 and denominator3; press traversal/move commands at first/last scene; try empty selection and duplicate names. |
| SV-U-MALFORMED | REQ-SESSION-VIEW-029 | malformed: On disposable copies open truncated/invalid media or invalid scene/slot saved state; import a claimed MIDI file with invalid contents. |
| SV-U-UNDO | REQ-SESSION-VIEW-029 | undo: Rename B, move B/D and insert a captured scene; Undo/Redo each action separately and inspect order, metadata and active playback. |
| SV-U-CANCEL | REQ-SESSION-VIEW-029 | cancel: Begin multi-file drop/scene rename or pending launch and cancel before completion; repeat after independently observed commit in a separate copy. |
| SV-U-PERSISTENCE | REQ-SESSION-VIEW-029 | persistence: Save/reopen owned Set with reordered/renamed/color scenes, nondefault widths, removed stop buttons and tempo/meter fields; inspect all values and view selection. |
| SV-U-SOURCE-LOSS | REQ-SESSION-VIEW-029 | source-loss: Remove an imported audio source or externally referenced clip asset from an owned copy, then launch/capture/transfer and inspect diagnostics/recovery. |
| SV-U-TRANSPORT | REQ-SESSION-VIEW-029 | transport: Run then stop/seek/restart with a pending scene, assigned tempo/meter and active clip; compare no-grid/global-grid/clip-grid configurations separately. |
| SV-U-AUTOMATION | REQ-SESSION-VIEW-029 | automation: Launch scene tempo/meter changes with active Arrangement automation and manually overridden controls; observe ownership without assuming precedence. |
| SV-U-TEARDOWN | REQ-SESSION-VIEW-029 | teardown: During pending scene launch and active nonempty clips remove source track/group/scene in separate copies, then close/reopen Set. |
| SV-U-RATE | REQ-SESSION-VIEW-029 | rate: With active clips and status display, request44.1/48kHz and64/256-frame settings in separate running/stopped trials; no clock/driver capability inferred. |
| SV-U-FOCUS | REQ-SESSION-VIEW-029 | focus: Repeat 0/Enter/Tab/arrow gestures in clip-name edit, scene-name edit, tempo field, plug-in window and main window with Tab preference On/Off; record target/context. |
| SV-U-AUDIO | REQ-SESSION-VIEW-029 | audio: Record paired active-output baselines and scene-capture/stop/reorder transitions with owned distinct signals; interruption, crossfade, tails, scheduling and tolerance remain unknown. |

Counts:29 requirements (28 D12/1 U),40 proposed cases (28 documentary/signal
proposals and12 operational U probes). Two of the28 are signal obligations with
null documentary comparator; all40 target outcomes/comparisons remain null/U.
No original code, audio, candidate, hardware or whole application was executed.

## Unclosed outcomes

Exact-build applicability, complete per-gesture branches, field parsing/ranges,
selection/focus conflicts, OS modifier differences, launch/cancel deadlines,
last-scene boundaries, nested groups, capture continuity, transfer/consolidation
files, malformed inputs, undo/redo, persistence, source loss, automation ownership,
sample-rate/driver changes and teardown remain required unknowns. The current
chapter's scene-name recording wording is retained by the recording owner;
dedicated scene fields do not silently supersede that condition. Follow Action
execution and complete clip launch behavior remain with the launch owner.

## Analysis-only evidence

- [Retained chapter](../../analysis/ableton-live-12.4.3/full-spec-v1/recording/manual-12-session-view-2026-10-19.html),
  official [Version12 Session View](https://www.ableton.com/en/live-manual/12/session-view/),
  capture2026-10-19T19:53:59.135059+00:00,267328bytes,
  SHA-256 `16e29141f823e298d5fa7fee3b993861f6c38415f8432cd00ac89789e9470a31`.
- [77 exact HTML blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/session-workflows/source-blocks.json)
  retain heading context/line/text; [line view](../../analysis/ableton-live-12.4.3/full-spec-v1/session-workflows/source-blocks.txt)
  is derived navigation, not replacement source. Figures were not separately inspected.
- [Requirement/evidence catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/session-workflows/requirements.json)
  and [author manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/session-workflows/manifest-author-r1.json)
  freeze the review scope. Revision1 is an author draft awaiting independent review.
  No existing release is expanded and no application compatibility result is claimed.
