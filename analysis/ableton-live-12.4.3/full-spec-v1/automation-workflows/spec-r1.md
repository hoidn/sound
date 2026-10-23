---
id: SPEC-AUTOMATION-WORKFLOWS
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3; Version 12 documentary applicability U
---

# Automation recording, editing and clip-envelope workflows

## Scope and provenance

This partial F-04/F-09 draft owns documentary automation record/overwrite,
override/re-enable presentation, lane/editor gestures and local clip-envelope
workflows. [Research](../research/automation-workflows.md) retains source contexts;
the [coverage design](../research/full-live-specification-design.md) governs closure.
It does not close the whole feature or supply a released implementation input.

**D12** means text in two retained official Version 12 chapters, captured
2026-10-19. Every new runtime clause has **exact-12.4.3 applicability U**. All
target expected/comparison fields are null, all grades U and all cases unexecuted.
Visible-control documentary predicates are proposals only. Signal, timing,
recorded-event and wholly unknown probes have null documentary expectations and
comparators; their source claim is retained separately. No UI case closes a
compound timing/audio clause, and no source wording supplies numerical tolerances.

## Existing authorities and exclusions

[Automation envelopes r5](automation-envelopes.md) retains stored containers,
targets/events, load/save checks and its logic evaluator. In particular,
[REQ-AUTOMATION-ENVELOPES-013](automation-envelopes.md#req-automation-envelopes-013--editing-override-recording-and-undo)
remains unknown: this manual packet does not settle its runtime, recorded point/Id,
override persistence, Undo, stored transforms or LockEnvelope meaning. The public
Lock Envelopes command is not a proof of that stored field's meaning.
[automation-envelopes-v2](../../handoff/automation-envelopes-v2/README.md) remains an
unchanged 21-case partial storage release; its exclusions and conditional clauses
are not broadened. No original evaluator or comparator is executed here.

[Mix graph](mix-graph.md) owns its finite playback envelope selection, point-list
evaluation, ramps and units, preserving untraced owners/conversions and A3/A6/A8
conditions. Logic evaluation, engine playback and a visible value are distinct.
Session clip timebase/start/loop/Warp and composed manual/modulation behavior remain
unproven. [Mixer values](mixer-values.md) retains fader, send and pan domains and
coefficients. No user-interface percentage is imported as stored normalization.

[Arrangement editing](arrangement-editing.md) retains clip edits, Back to Arrangement
and REQ032 lock-on movement. The new lock entry point below does not duplicate
that law or settle its lock-off/partial-selection gaps. [Recording](recording-comping.md)
retains note/audio record, count-in, punch and Session performance recording;
this page owns only its automation-specific eligibility and envelope roles.
[Session](session-view-workflows.md), [Clip View](clip-view-workflows.md),
[launch](clip-launch.md), [playback](playback-core.md) and
[transport](transport-state.md) keep their selection, source ownership, launch,
loop and clock contracts. Re-Enable Automation is distinct from Back to Arrangement.

[Keyboard/navigation](keyboard-navigation.md) retains focus and keyboard breakpoint
operations. [MIDI user mapping](midi-user-mapping.md), [MPE](mpe-workflows.md) and
[tuning](tuning-systems.md) retain their bounded input/transform contracts. Ordinary
audio sample transposition is not MPE per-note expression. [Warp markers](warp-markers.md)
retains finite marker/time conversion; Linked envelope editing supplies no new
warp kernel. [Racks](device-racks.md), [project/media](project-media-workflows.md),
[media files](media-file-workflows.md), [export](audio-video-export.md),
[Bounce/Freeze](bounce-freeze-workflows.md) and [Set structure](live-set-structure.md)
retain common device/preset/commit/file and storage behavior. Sample replacement
remains with Clip View REQ041; the chapter's all-settings description is not an
unqualified new Warp-marker preservation law.

## Preconditions and observation

Use the [future fixtures](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/fixtures.json),
not guessed constructor states. Record accepted target and values, track/clip/view,
actual playback ownership, explicit arm/record/transport, focus/mapping, envelope
kind/link/local region, grid/zoom and source/route before-state. Each named gesture,
platform entry point and first-pass/overwrite branch needs its own retained result.
Only actually offered controls/formats may be used. Missing prerequisites remain U.

Audio/no-effect probes require active changing automation or modulation, enabled
eligible target/section, nonzero base/depth/amount/gain/send, nonempty source,
nonmuted output/wet return and a separately retained positive baseline. Correct
receiver Monitor/arm/clip state is explicit. A silent source, inactive envelope,
zero send or absent controller cannot prove exclusion/no-effect. Recording probes
also require positive admitted movement, Automation Arm/appropriate record and
explicit running transport, with a paired working pass before a negative gate.

Envelope points, automation/modulation indicators, lane layout, arming and audible
output are separate observables. Templates/examples do not supply signal fixtures,
point-thinning, interpolation, scaling, normalization, MIDI bytes, envelope-time
equations, RNG, rate invariants, CPU performance, atomicity or error messages.
Figures and linked help/PDF bytes have not been inspected.

## Requirements

## Automation

### REQ-AUTO-WF-001 — Automation and modulation indicators

**D12/target-U.** An automated control has a theme-dependent colored indicator, typically red; blue denotes modulation. Session automation is available as a clip envelope, while Arrangement automation is displayed in track lanes.

Evidence/context: [automation:B003](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json), [automation:B004](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json).

### REQ-AUTO-WF-002 — Session automation recording eligibility

**D12/target-U.** Session clip automation recording uses Automation Arm, eligible armed tracks and Session Record. Record Session automation in: All Tracks permits recording into all playing Session clips regardless of track arm, including automation overdub without recording MIDI notes.

Evidence/context: [automation:B008](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json), [automation:B009](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json), [automation:B010](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json).

### REQ-AUTO-WF-003 — Session recording stop controls

**D12/target-U.** Session Record can stop automation recording while playback continues; Stop ends transport and recording. Recorded clip automation is viewed/edited in the Envelope Editor.

Evidence/context: [automation:B011](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json), [automation:B012](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json).

### REQ-AUTO-WF-004 — Session transfer and performance recording

**D12/target-U.** Session-to-Arrangement recording stores parameter changes as track automation, not Session clip automation, and can record tempo changes. Copying automated Session clips to Arrangement also copies automation as track automation; Session performance recording includes existing clip automation alongside live parameter changes.

Evidence/context: [automation:B007](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json), [automation:B013](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json).

### REQ-AUTO-WF-005 — Arrangement automation recording

**D12/target-U.** With Automation Arm enabled, Arrangement automation recording applies to all tracks. Arrangement Record is described as starting transport/recording by default and records tempo, mixer and device adjustments into track lanes; this is no unconditional transport-start guarantee.

Evidence/context: [automation:B015](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json), [automation:B016](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json), [automation:B018](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json).

### REQ-AUTO-WF-006 — Arrangement recording stop controls

**D12/target-U.** Arrangement Record can stop recording while playback continues; the adjacent Stop button ends both transport and recording.

Evidence/context: [automation:B017](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json).

### REQ-AUTO-WF-007 — Overwrite and Session touch/latch contexts

**D12/target-U.** Adjusting an already automated parameter during recording replaces its recorded adjustments. For Session overwrite, mouse release returns to prior automation, whereas MIDI knobs/faders hold the new setting until clip/loop end. A first Session automation pass uses the hold behavior regardless of input method. No overwrite interval or controller protocol law is supplied.

Evidence/context: [automation:B020](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json), [automation:B021](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json).

### REQ-AUTO-WF-008 — Manual override presentation

**D12/target-U.** With recording off, manually changing an automated parameter overrides its automation, turns its automation indicator gray and activates Re-Enable Automation. This is distinct from overwriting recorded data.

Evidence/context: [automation:B023](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json), [automation:B024](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json), [automation:B025](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json).

### REQ-AUTO-WF-009 — Global and per-parameter re-enable

**D12/target-U.** The Control Bar Re-Enable Automation button restores all overridden automation; a parameter context-menu command restores only that parameter. The active button indicates at least one overridden automated parameter.

Evidence/context: [automation:B026](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json), [automation:B027](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json).

### REQ-AUTO-WF-010 — Session relaunch re-enable role

**D12/target-U.** Relaunching a Session clip that contains automation is another documented way to re-enable overridden automation. This does not identify every affected target, launch boundary or Arrangement-return transition.

Evidence/context: [automation:B027](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json).

### REQ-AUTO-WF-011 — Session envelope selection

**D12/target-U.** The Session Envelope Editor Automation toggle and Device/Control choosers select a target envelope; device/mixer and MIDI Ctrl entries are described. Automated controls/devices have indicators; an unautomated selected control appears as a dashed line at its current value. Actual entries depend on clip type.

Evidence/context: [automation:B031](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json), [automation:B032](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json), [automation:B033](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json).

### REQ-AUTO-WF-012 — Session adjusted-envelope filter

**D12/target-U.** Show Adjusted Envelopes Only combines Session Device/Control choices into an Automated Control chooser; Show All Envelopes restores the full choices. An unautomated envelope already displayed remains displayed when filtering is enabled.

Evidence/context: [automation:B034](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json), [automation:B035](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json), [automation:B036](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json).

### REQ-AUTO-WF-013 — Stacked Session control focus

**D12/target-U.** With Envelope Editor open and Clip/Device Views stacked, clicking a track device or mixer control displays its envelope, including unautomated controls. Adjusted-only filtering prevents newly opening an unautomated envelope this way.

Evidence/context: [automation:B036](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json).

### REQ-AUTO-WF-014 — Arrangement Automation Mode and choosers

**D12/target-U.** Automation Mode button or A opens main track automation lanes. Device/Automation Control select envelopes; None hides the envelope and empties the control chooser. Automated entries have indicators and an untouched selected parameter is dashed.

Evidence/context: [automation:B038](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json), [automation:B039](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json), [automation:B040](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json), [automation:B041](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json).

### REQ-AUTO-WF-015 — Arrangement filters and focus commands

**D12/target-U.** Show Automated Parameters Only combines the Arrangement choosers; Show All Parameters restores them. In Automation Mode, clicking a control or its Show Automation/Show Automation in New Lane commands selects its envelope. With automated-only filtering, untouched controls cannot newly open and those menu options are disabled/unavailable; an already displayed untouched envelope remains.

Evidence/context: [automation:B042](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json), [automation:B043](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json), [automation:B044](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json).

### REQ-AUTO-WF-016 — Add lane and main-lane None

**D12/target-U.** Add Automation Lane moves the main envelope into an additional lane and sets main Device to None. Selecting a new main target permits another lane; Add is absent while None is selected.

Evidence/context: [automation:B045](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json).

### REQ-AUTO-WF-017 — Additional lane visibility and order

**D12/target-U.** A main-lane toggle hides/shows additional lanes; when main Device is None, hiding promotes the top additional lane to main. Additional lanes can be reordered by drag; arrows navigate lanes or show/hide from main context.

Evidence/context: [automation:B046](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json), [automation:B047](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json), [automation:B048](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json).

### REQ-AUTO-WF-018 — Existing lane focus and duplicate limit

**D12/target-U.** Choosing a parameter already in an additional lane focuses that lane. Ctrl-click Windows/Option-click macOS on Add creates a duplicate of the main envelope, with up to two such duplicates documented.

Evidence/context: [automation:B049](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json).

### REQ-AUTO-WF-019 — All lanes and lane removal

**D12/target-U.** Alt Windows/Cmd macOS Add or Add Lane for Each Automated Envelope adds lanes for automated parameters. Remove applies to selected additional lanes; modified Remove also removes lanes below. Main-lane Add and additional-lane Remove are available in the corresponding header menus.

Evidence/context: [automation:B050](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json), [automation:B051](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json), [automation:B054](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json), [automation:B055](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json), [automation:B056](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json).

### REQ-AUTO-WF-020 — Breakpoint insertion

**D12/target-U.** Clicking a selected control’s dashed envelope line inserts a breakpoint and makes it solid. Click-drag sets the new point value, Shift refines the adjustment, and double-click away from the line inserts there. Hover values and Add Value context entry support a chosen displayed value.

Evidence/context: [automation:B059](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json), [automation:B061](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json), [automation:B063](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json).

### REQ-AUTO-WF-021 — Breakpoint grid and display

**D12/target-U.** Inserted/moved breakpoints snap to grid, with Alt Windows/Cmd macOS bypass. Hover/drag exposes point values; segment hover/drag shows the closest breakpoint’s value. Shift horizontal drag constrains the horizontal axis and Shift vertical drag refines value adjustment.

Evidence/context: [automation:B062](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json), [automation:B063](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json), [automation:B080](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json), [automation:B087](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json).

### REQ-AUTO-WF-022 — Discrete envelope presentation

**D12/target-U.** Discrete controls such as toggles/radio choices display stepped rather than diagonal automation and permit only the square inserted shape.

Evidence/context: [automation:B064](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json), [automation:B074](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json).

### REQ-AUTO-WF-023 — Draw Mode and snapping

**D12/target-U.** Draw Mode is toggled through Options, Control Bar or B; holding B temporarily enables it when off. Drawing creates grid-width steps by default; grid size and Snap to Grid or Alt Windows/Cmd macOS bypass alter drawing alignment.

Evidence/context: [automation:B067](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json), [automation:B068](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json), [automation:B069](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json).

### REQ-AUTO-WF-024 — Shape insertion extent

**D12/target-U.** Context-menu automation shapes can be inserted at a marker or time selection; selection width determines horizontal extent and parameter range the vertical extent, while no selection uses current grid width. Source text names sine, triangle, sawtooth, inverse sawtooth, square, ramps and ADSR.

Evidence/context: [automation:B071](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json), [automation:B072](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json).

### REQ-AUTO-WF-025 — Waveform and ramp surroundings

**D12/target-U.** Inserted waveforms retain their shape irrespective of surrounding values, whereas ramps depend on values on either side of the insertion selection. Exact ramp coefficients, clipping and boundary events are unknown.

Evidence/context: [automation:B073](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json).

### REQ-AUTO-WF-026 — Breakpoint deletion and selection

**D12/target-U.** Points can be dragged; clicking a breakpoint deletes it and joins its neighbors by a new segment. Background drag selects multiple points, whose point drag moves the selection and whose context Delete removes selected points.

Evidence/context: [automation:B079](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json), [automation:B081](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json), [automation:B082](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json).

### REQ-AUTO-WF-027 — Segment movement and selection edges

**D12/target-U.** Dragging near a segment moves it; Shift-click/hold then releasing Shift is an alternative selection gesture. Moving a segment inside a time selection inserts points at the edges, and moving it outside inserts further edge points. Fine vertical and constrained horizontal drags are documented.

Evidence/context: [automation:B083](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json), [automation:B084](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json).

### REQ-AUTO-WF-028 — Drop overwrites and drag preview

**D12/target-U.** Dropping a dragged point/segment onto existing breakpoints overwrites them; while dragging before drop, existing parts are not permanently overwritten. This says nothing about Escape rollback or transaction atomicity.

Evidence/context: [automation:B085](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json).

### REQ-AUTO-WF-029 — Diagonal curve gesture

**D12/target-U.** Alt Windows/Option macOS segment drag adds a curve only to diagonal segments; modified double-click changes curved to straight. Numeric curve controls and runtime interpolation remain with the finite envelope/mix owners.

Evidence/context: [automation:B086](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json).

### REQ-AUTO-WF-030 — Exact value editing

**D12/target-U.** Edit Value on a point/segment accepts a typed value. With multiple selected points, the edited point takes that value and the others move relatively. Admission, saturation and error grammar are unknown.

Evidence/context: [automation:B088](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json).

### REQ-AUTO-WF-031 — Stretch and skew handles

**D12/target-U.** Time-selection handles transform the selected envelope: top/bottom centers stretch vertically, side centers horizontally and corners skew. Outline snaps with horizontal bypass; Shift refines vertical stretch and Alt Windows/Option macOS mirrors opposite handles. Dragging over outside points removes them.

Evidence/context: [automation:B091](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json), [automation:B092](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json), [automation:B093](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json), [automation:B094](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json), [automation:B095](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json).

### REQ-AUTO-WF-032 — Simplify Envelope command

**D12/target-U.** Simplify Envelope on a selected segment reduces unnecessary breakpoints using straight/curved segments. The source supplies no error tolerance, optimum algorithm or guaranteed reduction for every input.

Evidence/context: [automation:B097](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json).

### REQ-AUTO-WF-033 — Delete Automation parameter action

**D12/target-U.** Parameter Delete Automation context action or Ctrl-Backspace Windows/Cmd-Delete macOS deletes that parameter’s automation, removes its indicator and returns the value to its default. This does not identify a numeric default or general clip-editor shortcut dispatch.

Evidence/context: [automation:B099](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json).

### REQ-AUTO-WF-034 — Clear command scopes

**D12/target-U.** Clear Envelope removes selected-parameter envelope; lane-header Clear All Envelopes of… removes automated envelopes for the selected device; Clear All Envelopes removes automation throughout the Set. Partial removal uses point/segment editing instead.

Evidence/context: [automation:B100](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json), [automation:B101](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json), [automation:B102](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json), [automation:B103](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json), [automation:B104](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json).

### REQ-AUTO-WF-035 — Tempo envelope and mapped range

**D12/target-U.** Tempo can be recorded during Arrangement recording or edited in Main’s Mixer/Song Tempo lane. Tempo Minimum/Maximum Range controls set its displayed BPM range and also the value range of a MIDI controller assigned to tempo. Numeric mapping, global tempo precedence and clock response remain separate.

Evidence/context: [automation:B107](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json), [automation:B108](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json), [automation:B109](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json).

### REQ-AUTO-WF-036 — Lock Envelopes entry point

**D12/target-U.** Lock Envelopes is available through its toggle or Options menu. Arrangement REQ-ARRANGEMENT-032 retains the lock-on clip-move contract; the source’s broader lock-off move statement does not close that owner’s partial-selection and transformation unknowns.

Evidence/context: [automation:B111](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json).

### REQ-AUTO-WF-037 — Envelope Edit commands and target transfer

**D12/target-U.** Cut, Copy, Duplicate and Delete on an automation-lane time selection affect only selected envelope portions rather than clip content or other portions; multi-lane selections apply to the included envelopes. Segments can be copied across time and parameter targets, without a conversion rule for unrelated controls.

Evidence/context: [automation:B113](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json), [automation:B114](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json).

## Clip envelopes

### REQ-AUTO-WF-038 — Clip-type chooser vocabulary

**D12/target-U.** Clip Envelopes tab has Device and Control choosers; audio clips expose Clip sample controls, track effects and mixer, while MIDI clips expose MIDI Ctrl, track devices and mixer. Altered envelopes have adjacent indicators and an adjusted-only filter.

Evidence/context: [clip-envelopes:B004](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-clip-envelopes-blocks.json), [clip-envelopes:B005](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-clip-envelopes-blocks.json), [clip-envelopes:B006](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-clip-envelopes-blocks.json), [clip-envelopes:B007](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-clip-envelopes-blocks.json), [clip-envelopes:B008](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-clip-envelopes-blocks.json).

### REQ-AUTO-WF-039 — Session versus Arrangement envelope kinds

**D12/target-U.** Session clips offer Automation/Modulation toggles; Arrangement Clip View exposes modulation only and track automation uses lanes. Automation specifies a control’s absolute value while modulation influences its current/automated value. Both kinds can coexist, with separate indicators and knob position/ring presentation; no universal combiner formula follows.

Evidence/context: [clip-envelopes:B009](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-clip-envelopes-blocks.json), [clip-envelopes:B010](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-clip-envelopes-blocks.json), [clip-envelopes:B038](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-clip-envelopes-blocks.json), [clip-envelopes:B040](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-clip-envelopes-blocks.json), [clip-envelopes:B041](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-clip-envelopes-blocks.json).

### REQ-AUTO-WF-040 — Clear clip envelope entry

**D12/target-U.** Clear Envelope in the Clip View envelope context menu resets the selected clip envelope to its default. Exact default values and the source’s shortcut-to-menu wording remain unresolved; parameter Delete Automation is a distinct context.

Evidence/context: [clip-envelopes:B011](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-clip-envelopes-blocks.json).

### REQ-AUTO-WF-041 — MIDI Envelope Auto-Reset option

**D12/target-U.** MIDI Envelope Auto-Reset is offered through Options or the Sample Editor context menu and is described as resetting certain MIDI control messages at new clip start. Which messages/values, delivery time and persistence are unknown.

Evidence/context: [clip-envelopes:B012](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-clip-envelopes-blocks.json).

### REQ-AUTO-WF-042 — Non-destructive sample modulation

**D12/target-U.** Clip-envelope modulation is non-destructive to the referenced sample on disk; clips can reuse one sample with different envelopes. Render/resample/consolidate are separate ways to commit audio, owned by their workflow pages.

Evidence/context: [clip-envelopes:B017](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-clip-envelopes-blocks.json), [clip-envelopes:B018](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-clip-envelopes-blocks.json).

### REQ-AUTO-WF-043 — Audio transposition envelope context

**D12/target-U.** The audio Clip/Transposition workflow uses Warp on and supports Draw Mode or fine breakpoint edits. The source describes additive influence bounded by the Transpose range and Warp-mode/granularity-dependent response; no frequency law, warp kernel, smoothing or numeric event conversion is added.

Evidence/context: [clip-envelopes:B020](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-clip-envelopes-blocks.json), [clip-envelopes:B021](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-clip-envelopes-blocks.json), [clip-envelopes:B022](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-clip-envelopes-blocks.json), [clip-envelopes:B023](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-clip-envelopes-blocks.json), [clip-envelopes:B025](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-clip-envelopes-blocks.json).

### REQ-AUTO-WF-044 — Audio Clip Gain modulation role

**D12/target-U.** Clip/Gain envelope can shape sample level. Its influence is relative to Clip Gain, can attenuate to silence and cannot exceed that absolute setting; this documentary role supplies no calibrated gain-domain formula.

Evidence/context: [clip-envelopes:B027](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-clip-envelopes-blocks.json), [clip-envelopes:B028](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-clip-envelopes-blocks.json).

### REQ-AUTO-WF-045 — Sample Offset eligibility

**D12/target-U.** Clip/Sample Offset modulation is available only in Beats Warp Mode and is edited as a clip envelope. The chapter’s beat-scrambling examples do not establish random, resampling or analytic cut-and-splice behavior.

Evidence/context: [clip-envelopes:B030](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-clip-envelopes-blocks.json), [clip-envelopes:B031](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-clip-envelopes-blocks.json).

### REQ-AUTO-WF-046 — Track volume stage and indicator

**D12/target-U.** Clip Gain and Track Volume are distinct envelope targets; Track Volume modulation affects the mixer’s post-effect gain stage and a dot below its slider indicates the modulated setting. No stored-unit or signal multiplier law is restated.

Evidence/context: [clip-envelopes:B043](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-clip-envelopes-blocks.json), [clip-envelopes:B044](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-clip-envelopes-blocks.json).

### REQ-AUTO-WF-047 — Send modulation ceiling role

**D12/target-U.** Send modulation is relative to the Send control: it cannot open the send beyond the knob and can reduce it to minus infinity. This does not extend finite send coefficients or define event conversion.

Evidence/context: [clip-envelopes:B045](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-clip-envelopes-blocks.json).

### REQ-AUTO-WF-048 — Pan modulation contextual range

**D12/target-U.** Pan modulation range depends on the base knob: center permits the full stereo span, movement toward an edge reduces available influence, and full left is described as no-effect. This is not a pan law or formula for every mode.

Evidence/context: [clip-envelopes:B047](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-clip-envelopes-blocks.json).

### REQ-AUTO-WF-049 — Device modulation relative role

**D12/target-U.** Clip modulation acts on devices in that clip’s track and changes controls relative to their current setting rather than defining preset values. Per-device eligible targets and combination arithmetic require their owners/evidence.

Evidence/context: [clip-envelopes:B049](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-clip-envelopes-blocks.json).

### REQ-AUTO-WF-050 — MIDI controller envelope editing

**D12/target-U.** MIDI Ctrl/Control selects listed controller envelopes for creation/editing with steps or points, including imported/recorded data indicated by adjacent LEDs. Most controller numbers through 119 are described as supported; this is not every number or a MIDI codec. Receiver conventions may differ from names such as Pitch Bend or Pan.

Evidence/context: [clip-envelopes:B051](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-clip-envelopes-blocks.json), [clip-envelopes:B052](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-clip-envelopes-blocks.json), [clip-envelopes:B053](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-clip-envelopes-blocks.json).

### REQ-AUTO-WF-051 — Envelope-local region controls

**D12/target-U.** Unlinking gives the selected envelope its own local region/loop controls and colored loop braces. Its Loop switch is independent of the sample’s Loop switch, allowing a one-shot envelope while the sample continues looping.

Evidence/context: [clip-envelopes:B056](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-clip-envelopes-blocks.json), [clip-envelopes:B059](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-clip-envelopes-blocks.json), [clip-envelopes:B060](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-clip-envelopes-blocks.json).

### REQ-AUTO-WF-052 — Independent envelope lengths and start markers

**D12/target-U.** Each unlinked envelope can have its own loop length, extended by braces or numeric controls, including non-bar-aligned lengths. Its start marker identifies where envelope playback begins on clip start; start/end and braces obey the zoom-adaptive grid. No clip-time equation or sample-rounded extent follows.

Evidence/context: [clip-envelopes:B067](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-clip-envelopes-blocks.json), [clip-envelopes:B068](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-clip-envelopes-blocks.json), [clip-envelopes:B069](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-clip-envelopes-blocks.json), [clip-envelopes:B070](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-clip-envelopes-blocks.json), [clip-envelopes:B071](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-clip-envelopes-blocks.json).

### REQ-AUTO-WF-053 — Local-loop rhythmic role

**D12/target-U.** Local envelope loops may be shorter or longer than source playback and can be shaped with handles/shapes. The source describes tempo-relative repetition and grid-hidden independent endpoints; it does not specify clock arithmetic, rate limits or a free-running oscillator implementation.

Evidence/context: [clip-envelopes:B073](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-clip-envelopes-blocks.json), [clip-envelopes:B075](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-clip-envelopes-blocks.json), [clip-envelopes:B076](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-clip-envelopes-blocks.json).

### REQ-AUTO-WF-054 — Linked envelope Warp interaction

**D12/target-U.** In Linked mode, moving a clip Warp Marker lengthens/shortens its envelope accordingly, and Warp Markers can be adjusted within the envelope editor. Exact marker/envelope transformation and interpolation stay unknown or with the finite Warp owner.

Evidence/context: [clip-envelopes:B078](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-clip-envelopes-blocks.json).

## Unknown obligations

### REQ-AUTO-WF-U-RUNTIME — Runtime, timebase and finite-law boundary

**U/target-U.** Editing/recording/override/re-enable/runtime outcomes of REQ-AUTOMATION-ENVELOPES-013 remain U. Point generation/Ids, stored transforms/LockEnvelope meaning, modulation normalization, clip timebase/start/loop/Warp, scheduler/ramp alignment and untraced mix-graph owners are not settled by this packet.

Evidence/context: [automation:B020](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json), [automation:B021](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json), [automation:B027](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json), [clip-envelopes:B038](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-clip-envelopes-blocks.json), [clip-envelopes:B078](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-clip-envelopes-blocks.json).

### REQ-AUTO-WF-U-SOURCE — Unresolved source contexts

**U/target-U.** Clip Clear Envelope shortcut wording, parameter Delete Automation shortcut dispatch, and sample-replacement all-settings wording versus the existing equal-length Warp-marker predicate need context/build evidence. MIDI auto-reset message set/values and exact copy-across-domain conversions are unknown.

Evidence/context: [automation:B099](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json), [automation:B114](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json), [clip-envelopes:B011](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-clip-envelopes-blocks.json), [clip-envelopes:B012](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-clip-envelopes-blocks.json), [clip-envelopes:B036](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-clip-envelopes-blocks.json).

### REQ-AUTO-WF-U-MAPPING — Mapping and automation ownership

**U/target-U.** Controller delivery/takeover, key or MIDI mapping versus automation/override/recording, MPE/controller identity, tempo mapping ranges versus normalization and simultaneous input precedence have no new runtime law.

Evidence/context: [automation:B021](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json), [automation:B109](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation-blocks.json), [clip-envelopes:B053](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-clip-envelopes-blocks.json).

### REQ-AUTO-WF-U-BOUNDARY — Unspecified edit and record boundaries

**U/target-U.** Empty selections/lanes/clip slots, ineligible targets, equal-time points, endpoints, negative or extreme text/ranges, multi-clip/group/return/Main combinations and crossing/collapsed transforms have no general refusal/repair law.

Evidence: unsupported outcome; ungraded investigation obligation.

### REQ-AUTO-WF-U-STATE — History, persistence and cancellation

**U/target-U.** Undo/redo grouping, gesture cancellation, override/arming/filter/selection persistence, save/reopen/duplicate/transfer and automation edit ownership are unknown beyond visible documentary roles. No rollback or event serialization is inferred.

Evidence: unsupported outcome; ungraded investigation obligation.

### REQ-AUTO-WF-U-CLOCK — Transport, rates and engine transitions

**U/target-U.** Stop/start/seek/loop/tempo/meter/sync changes during record/edit/re-enable, rate/block changes, engine restart and concurrent processing retain unknown event ordering, phase and audio results.

Evidence: unsupported outcome; ungraded investigation obligation.

### REQ-AUTO-WF-U-LOSS — Source and target loss

**U/target-U.** Device/parameter/track/clip/media/controller disappearance during active envelopes or pending edits, unavailable ports and malformed admitted documents have no new diagnostics, recovery or silence oracle.

Evidence: unsupported outcome; ungraded investigation obligation.

### REQ-AUTO-WF-U-TEARDOWN — Teardown and concurrent workflows

**U/target-U.** Closing/replacing Set, quitting, losing engine/controller connection or concurrently editing/removing targets while recording or transforming has no established completion, cleanup or transaction outcome.

Evidence: unsupported outcome; ungraded investigation obligation.

## Finite case index

The [76 cases](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/cases.json) map exactly to the
[62 requirements](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/requirements.json): 54 D12
and eight U. 44 cases have only visible documentary
predicates; 32 have null documentary oracles.
All target oracles are null/U and all cases unexecuted. This is partial coverage;
the index does not claim every target/gesture combination, platform or lifecycle
branch is closed. Each case carries exact finite action, fixture gates, source
locators and a separate source_claim field, including signal/timing cases.

| Case | Requirement | Kind | Action focus |
| --- | --- | --- | --- |
| AW-001 | REQ-AUTO-WF-001 | state | Automation and modulation indicators |
| AW-002 | REQ-AUTO-WF-002 | state | Session automation recording eligibility |
| AW-003 | REQ-AUTO-WF-003 | state | Session recording stop controls |
| AW-004 | REQ-AUTO-WF-004 | state | Session transfer and performance recording |
| AW-005 | REQ-AUTO-WF-005 | state | Arrangement automation recording |
| AW-006 | REQ-AUTO-WF-006 | state | Arrangement recording stop controls |
| AW-007 | REQ-AUTO-WF-007 | timing | Overwrite and Session touch/latch contexts |
| AW-008 | REQ-AUTO-WF-008 | state | Manual override presentation |
| AW-009 | REQ-AUTO-WF-009 | state | Global and per-parameter re-enable |
| AW-010 | REQ-AUTO-WF-010 | timing | Session relaunch re-enable role |
| AW-011 | REQ-AUTO-WF-011 | state | Session envelope selection |
| AW-012 | REQ-AUTO-WF-012 | state | Session adjusted-envelope filter |
| AW-013 | REQ-AUTO-WF-013 | state | Stacked Session control focus |
| AW-014 | REQ-AUTO-WF-014 | state | Arrangement Automation Mode and choosers |
| AW-015 | REQ-AUTO-WF-015 | state | Arrangement filters and focus commands |
| AW-016 | REQ-AUTO-WF-016 | state | Add lane and main-lane None |
| AW-017 | REQ-AUTO-WF-017 | state | Additional lane visibility and order |
| AW-018 | REQ-AUTO-WF-018 | state | Existing lane focus and duplicate limit |
| AW-019 | REQ-AUTO-WF-019 | state | All lanes and lane removal |
| AW-020 | REQ-AUTO-WF-020 | state | Breakpoint insertion |
| AW-021 | REQ-AUTO-WF-021 | state | Breakpoint grid and display |
| AW-022 | REQ-AUTO-WF-022 | state | Discrete envelope presentation |
| AW-023 | REQ-AUTO-WF-023 | state | Draw Mode and snapping |
| AW-024 | REQ-AUTO-WF-024 | state | Shape insertion extent |
| AW-025 | REQ-AUTO-WF-025 | state | Waveform and ramp surroundings |
| AW-026 | REQ-AUTO-WF-026 | state | Breakpoint deletion and selection |
| AW-027 | REQ-AUTO-WF-027 | state | Segment movement and selection edges |
| AW-028 | REQ-AUTO-WF-028 | state | Drop overwrites and drag preview |
| AW-029 | REQ-AUTO-WF-029 | state | Diagonal curve gesture |
| AW-030 | REQ-AUTO-WF-030 | state | Exact value editing |
| AW-031 | REQ-AUTO-WF-031 | state | Stretch and skew handles |
| AW-032 | REQ-AUTO-WF-032 | state | Simplify Envelope command |
| AW-033 | REQ-AUTO-WF-033 | state | Delete Automation parameter action |
| AW-034 | REQ-AUTO-WF-034 | state | Clear command scopes |
| AW-035 | REQ-AUTO-WF-035 | control | Tempo envelope and mapped range |
| AW-036 | REQ-AUTO-WF-036 | state | Lock Envelopes entry point |
| AW-037 | REQ-AUTO-WF-037 | state | Envelope Edit commands and target transfer |
| AW-038 | REQ-AUTO-WF-038 | state | Clip-type chooser vocabulary |
| AW-039 | REQ-AUTO-WF-039 | state | Session versus Arrangement envelope kinds |
| AW-040 | REQ-AUTO-WF-040 | state | Clear clip envelope entry |
| AW-041 | REQ-AUTO-WF-041 | control | MIDI Envelope Auto-Reset option |
| AW-042 | REQ-AUTO-WF-042 | signal | Non-destructive sample modulation |
| AW-043 | REQ-AUTO-WF-043 | signal | Audio transposition envelope context |
| AW-044 | REQ-AUTO-WF-044 | signal | Audio Clip Gain modulation role |
| AW-045 | REQ-AUTO-WF-045 | state | Sample Offset eligibility |
| AW-046 | REQ-AUTO-WF-046 | control | Track volume stage and indicator |
| AW-047 | REQ-AUTO-WF-047 | signal | Send modulation ceiling role |
| AW-048 | REQ-AUTO-WF-048 | signal | Pan modulation contextual range |
| AW-049 | REQ-AUTO-WF-049 | signal | Device modulation relative role |
| AW-050 | REQ-AUTO-WF-050 | control | MIDI controller envelope editing |
| AW-051 | REQ-AUTO-WF-051 | state | Envelope-local region controls |
| AW-052 | REQ-AUTO-WF-052 | timing | Independent envelope lengths and start markers |
| AW-053 | REQ-AUTO-WF-053 | timing | Local-loop rhythmic role |
| AW-054 | REQ-AUTO-WF-054 | state | Linked envelope Warp interaction |
| AW-U-RECORD-EVENTS | REQ-AUTO-WF-U-RUNTIME | recording | Record events |
| AW-U-VALUE-RETURN | REQ-AUTO-WF-U-RUNTIME | timing | Value return |
| AW-U-ARRANGEMENT-RETURN | REQ-AUTO-WF-U-RUNTIME | transport | Arrangement return |
| AW-U-CLEAR-SHORTCUT | REQ-AUTO-WF-U-SOURCE | boundary | Clear shortcut |
| AW-U-REPLACEMENT | REQ-AUTO-WF-U-SOURCE | source-loss | Replacement |
| AW-U-MIDI-AUTO-RESET | REQ-AUTO-WF-U-SOURCE | midi-output | Midi auto reset |
| AW-U-MAPPED-OVERWRITE | REQ-AUTO-WF-U-MAPPING | mapping | Mapped overwrite |
| AW-U-TEMPO-RANGE | REQ-AUTO-WF-U-MAPPING | mapping | Tempo range |
| AW-U-INACTIVE-CONTROLS | REQ-AUTO-WF-U-BOUNDARY | negative | Inactive controls |
| AW-U-EMPTY-AND-EDGES | REQ-AUTO-WF-U-BOUNDARY | boundary | Empty and edges |
| AW-U-TRANSFORM-LIMITS | REQ-AUTO-WF-U-BOUNDARY | boundary | Transform limits |
| AW-U-TARGET-CONTEXTS | REQ-AUTO-WF-U-BOUNDARY | boundary | Target contexts |
| AW-U-UNDO-REDO | REQ-AUTO-WF-U-STATE | undo | Undo redo |
| AW-U-CANCEL | REQ-AUTO-WF-U-STATE | cancel | Cancel |
| AW-U-SAVE-REOPEN | REQ-AUTO-WF-U-STATE | persistence | Save reopen |
| AW-U-TRANSPORT-LOOP | REQ-AUTO-WF-U-CLOCK | transport | Transport loop |
| AW-U-RATE-ENGINE | REQ-AUTO-WF-U-CLOCK | sample-rate | Rate engine |
| AW-U-TARGET-REMOVAL | REQ-AUTO-WF-U-LOSS | source-loss | Target removal |
| AW-U-SOURCE-CONTROLLER-LOSS | REQ-AUTO-WF-U-LOSS | source-loss | Source controller loss |
| AW-U-MALFORMED | REQ-AUTO-WF-U-LOSS | malformed | Malformed |
| AW-U-CLOSE-ACTIVE | REQ-AUTO-WF-U-TEARDOWN | teardown | Close active |
| AW-U-CONCURRENT-EDIT | REQ-AUTO-WF-U-TEARDOWN | concurrency | Concurrent edit |

## Unresolved contexts and closure

[Research source questions](../research/automation-workflows.md#source-context-questions)
preserve the deletion shortcut and replacement contexts. They remain U rather than
globalized UI or marker laws. MIDI Auto-Reset names no complete message set or
reset values. Theme colors and slightly different chooser wording do not prove
exact label aliases or build parity. Example pitch/gain/offset/fade/LFO anecdotes
remain source context rather than waveform recipes or numerical engine laws.

Recording/overwrite point production, input ownership, return-to-automation timing,
envelope/clip-time conversion, automation/modulation combination, undo/cancel,
save/reopen, controller/target/media loss, transport/rate changes and teardown need
bounded evidence. The [whole-product applicability question](../questions.md#q-027-whole-product-specification-evidence-and-version-coverage)
remains open. No original/native/extracted-original, candidate, controller,
hardware, codec or audio/MIDI runtime is run for this draft.

## Analyst evidence appendix

[Sources](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/sources.json) pin URLs/final URLs, UTC capture, major edition,
immutable HTML sizes/SHA256. [Authority pins](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/existing-authority-pins.json)
retain ten existing canonical identities and three immutable automation release
identities unchanged. [Counts](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/counts.json), [manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manifest-author-r1.json)
and the read-only [validator](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/validate.py) freeze the packet.

| Source | Retained scope | Text view |
| --- | --- | --- |
| D12-AUTOMATION | §26.1–26.9.3, 114 numbered chapter blocks, HTML280–832 | [Automation](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-automation.txt) |
| D12-CLIP-ENVELOPES | §27.1–27.5.5, 78 numbered chapter blocks, HTML280–460 | [Clip envelopes](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/manual-clip-envelopes.txt) |

Exact block records preserve original HTML lines, anchors and heading context.
No figures, linked tutorials, native data or private formats supply new laws.
Shared indexes, coverage, questions and log integration belong to the root analyst.
