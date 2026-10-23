---
id: SPEC-PUSH-CONTROLLER-WORKFLOWS
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3; Push 1 and Push 2 documentary applicability U
---

# Separate Push 1 and Push 2 documentary workflows

## Scope and evidence boundary

This partial F-08 draft gives separate text-supported profiles for Push 1 and
Push 2: setup, browser, drum/pitched/step layouts, record controls, device/mix,
automation, Session and preferences, plus selected Push 2 sample/Clip entrypoints.
[Research](../research/push-controller-workflows.md) retains interpretations and
source questions. [Coverage design](../research/full-live-specification-design.md)
governs closure. Neither profile is complete or a released implementation input.

**D12** means the retained official Version 12 chapter for that named model,
captured 2026-10-19. Every new clause has **exact-12.4.3 applicability U**, including
controls, modes, availability, default and firmware contexts. All target expected
and comparison fields are null, all grades U and all cases unexecuted. Only named
textual controls/display/selection/membership roles have documentary proposals.
Signal, timing, recording, MIDI, pad-role/numeric/model and protocol cases also
have null documentary expectations/comparators with source_claim retained separately.
No case closes a compound signal or physical-hardware clause.

Push 1 text is not Push 2 or Push 3 evidence. Broader Push 3 standalone/firmware,
all 149 controller-directory protocols, complete control references, pedal/pressure
calibration, user profiles and device-bank compatibility remain open. Figures,
inline glyphs and linked videos/help are not inspected. No physical pad placement,
button label or color palette is inferred from an image. Public pad counts and
examples are documentary context, not numeric pad/MIDI oracles.

## Canonical owners and prerequisites

[MIDI editing/tools](midi-editing-tools.md) retains note edits/quantization;
[recording](recording-comping.md) retains record, count-in, punch and Capture;
[Session](session-view-workflows.md), [Clip View](clip-view-workflows.md),
[Arrangement](arrangement-editing.md) and [launch](clip-launch.md) retain ordinary
selection/clip/scene/loop and recording eligibility. These new controller gestures
do not supply their event storage, note merging or scheduler equations.

[Automation storage/evaluation](automation-envelopes.md), especially REQ013,
retains unknown editing/runtime. [Automation workflows](automation-workflows.md)
owns generic record/override/re-enable and clip-envelope roles; controller buttons
do not establish numerical interpolation, event generation or override persistence.
[Routing/monitoring](routing-monitoring-latency.md) and [mixer values](mixer-values.md)
retain controls/coefficient and admitted signal-path conditions. [Racks](device-racks.md),
[Simpler](device-simpler.md), [conversion](audio-to-midi.md),
[Warp markers](warp-markers.md), [MPE](mpe-workflows.md) and [tuning](tuning-systems.md)
retain device, slicing, Warp, expression and scale/tuning computation. A named
Nudge or Warp control does not supply those algorithms. [Remote control](remote-control-workflows.md)
and [MIDI mapping](midi-user-mapping.md) retain generic/manual mapping and finite
configuration codec boundaries; User Mode recommendations do not prove exact token
equivalence or complete protocol support. [Project/media](project-media-workflows.md)
owns shared save/history/media operations. Entry points do not imply transactions.

The [future fixtures](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/fixtures.json)
require independently accepted matching hardware/firmware/platform/ports and a
working positive response before each role investigation. Hardware is absent here.
Retain actual mode/layout, target/track/clip, focus/selection, arm/monitor/record,
Automation Arm, transport/Workflow, source references and accepted values. A source
paragraph cannot supply these capabilities. Missing control/hardware remains U.

Audio, recording and no-effect probes additionally require nonempty source,
enabled active eligible instrument/effect/envelope, nonzero base/depth/amount/gain/
send, correct receiver monitoring and nonmuted positive output/wet return. Confirm
admitted input and nonzero response independently. Recording needs explicit valid
record context and running transport plus paired working pass. Silent source,
inactive section, zero wet amount, muted return or absent hardware is not a pass.

No private USB/MIDI/LED/framebuffer format, pressure/force law, latency, numerical
scale/pad map, RNG, audio waveform, voice model, tolerance, rate invariance or
firmware updater is invented. Setup/update text authorizes no hardware action,
installation, original/native/runtime probe, emulator or independent implementation.

## Model requirements

## Push 1

### REQ-PUSH1-WF-001 — USB setup role

**D12/target-U.** Push 1 is described as automatically recognized when connected over USB while Live is running, without manual driver or Settings setup. Accepted platform, firmware, enumeration, recovery and latency remain unknown.

Evidence: [P1-B007](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json).

### REQ-PUSH1-WF-002 — Browse navigation and load

**D12/target-U.** Browse opens a column browser; In/Out shifts hierarchy, Selection/State buttons navigate, encoders scroll and Shift up/down pages. Text distinguishes selected preset load from device default load and already-loaded next-entry behavior; no figure-derived button identity or exact light color is imposed.

Evidence: [P1-B009](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B010](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B011](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B012](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B013](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B014](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json).

### REQ-PUSH1-WF-003 — Browse context filtering

**D12/target-U.** Push 1 browsing depends on selected instrument/effect context; an empty MIDI track shows available device families. Only currently loadable folders are visible, with sample-only locations described for an individual Drum Rack pad.

Evidence: [P1-B015](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json).

### REQ-PUSH1-WF-004 — Drum layout roles

**D12/target-U.** In Note Mode with Drum Rack, the chapter describes Loop Selector sections for play/sequence/length, a velocity layout and full-grid playing. Note-based switching/momentary access is described, but the separate Layout wording is unresolved; no physical pad map or complete transition table is adopted.

Evidence: [P1-B017](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B018](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B019](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B021](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B030](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B035](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B036](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B037](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json).

### REQ-PUSH1-WF-005 — Drum pad bank and silent selection

**D12/target-U.** Touch strip and Octave controls navigate Drum Rack pads, with Shift finer movement; Select plus pad selects without playing. Exact pad indices, MIDI notes and pressure response remain unknown.

Evidence: [P1-B029](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B045](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json).

### REQ-PUSH1-WF-006 — Individual drum browsing and copy

**D12/target-U.** Device selection can focus an individual Drum Rack pad for Browse replacement; other pad taps select further browse targets. Duplicate held from source pad to destination replaces destination devices while preserving already recorded destination notes.

Evidence: [P1-B039](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B040](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B041](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B043](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json).

### REQ-PUSH1-WF-007 — Drum step gestures

**D12/target-U.** Step taps add notes and start clip playback; tapping occupied steps deletes them, Mute plus step deactivates without deletion, Solo plus pad solos a sound, and Delete plus pad removes its notes within the current loop. Triplet layout leaves some pads inactive; no grid/sample arithmetic follows.

Evidence: [P1-B046](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B047](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B049](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B054](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json).

### REQ-PUSH1-WF-008 — Record and overdub controls

**D12/target-U.** Metronome is available for real-time recording; successive Record actions record, stop recording while playback continues, then enable overdub. General count-in/record eligibility and actual recorded notes remain with recording owners.

Evidence: [P1-B058](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B059](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B060](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json).

### REQ-PUSH1-WF-009 — New and workflow modes

**D12/target-U.** Scene Workflow Duplicate captures playing clips into a new scene; New prepares selected-track material instead. Clip Workflow Duplicate/New operates on selected clip/track while other tracks continue, with Shift-Duplicate scene behavior. Seamless wording supplies no transition tolerance.

Evidence: [P1-B061](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B217](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B219](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B220](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B223](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B224](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json).

### REQ-PUSH1-WF-010 — Fixed Length controls

**D12/target-U.** Fixed Length selects predetermined new-clip length, holding it opens length choice; disabled recording runs until a documented stop action. Enabling during record stops writing and loops the preceding span according to setting, without a beat/sample endpoint law.

Evidence: [P1-B063](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B064](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B065](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B066](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json).

### REQ-PUSH1-WF-011 — Repeat and swing roles

**D12/target-U.** Repeat produces repeated held-pad notes, with rate via Scene/Grid and state/settings remembered per track. A short press latches while a hold is momentary; pressure and Swing influence output. No force curve, note rate or swing calculation is supplied.

Evidence: [P1-B069](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B070](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B071](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B072](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json).

### REQ-PUSH1-WF-012 — Quantize entry and scope

**D12/target-U.** Quantize applies selected clip note quantization; holding exposes Swing Amount, Quantize To/Amount and Record Quantize. Quantize plus drum pad narrows scope to that drum. Numeric quantization and record-grid enums retain existing owners.

Evidence: [P1-B074](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B075](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B076](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B077](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B078](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B079](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json).

### REQ-PUSH1-WF-013 — Pitched pad and scale layouts

**D12/target-U.** Instrument Note Mode offers pitched playing and loop controls; Scales selects key/scale and Fixed/In Key/Chromatic/layout options. Scale options are described as saved with Set. Scales is ineligible for Drum Rack or Session context; no note-number map, tuning or default key law is prescribed.

Evidence: [P1-B085](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B093](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B095](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B096](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B097](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B099](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B100](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B101](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B102](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B103](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B244](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json).

### REQ-PUSH1-WF-014 — Melodic step and loop layout

**D12/target-U.** Note switches to melodic step layouts, rows represent chosen pitches and columns selected grid steps. Held Note exposes loop controls and Shift-Note locks them per track; Octave/touch strip changes range. Numeric mapping/phase and the 32-note layout remain ungraded.

Evidence: [P1-B107](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B108](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B109](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B110](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B111](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B113](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json).

### REQ-PUSH1-WF-015 — Loop page selection and copy

**D12/target-U.** Loop-length pads select loop span or viewed sequencer page. A locked view need not be the playing page; reselecting loop restores follow, whereas selecting outside loop sets that page as loop. Duplicate-page adds copied notes over existing destination notes; Delete-page clears first.

Evidence: [P1-B116](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B117](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B123](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B124](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json).

### REQ-PUSH1-WF-016 — Combined melodic playing and sequencing

**D12/target-U.** Melodic Sequencer plus Notes combines real-time pitch selection with steps. Select avoids playing; a step adds selected notes, holding it exposes contained pitches, and removing a selected pitch removes it from that step. Duplicate adds copied notes without clearing destination.

Evidence: [P1-B126](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B128](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B129](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B138](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B139](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B140](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json).

### REQ-PUSH1-WF-017 — Note navigation and arm context

**D12/target-U.** Left/right selects tracks and MIDI selection is described as auto-arming. Up/down moves scenes, with Scene versus Clip Workflow determining launched scope; source describes immediate Legato-like position continuation. No constructor arm default or timing law is established.

Evidence: [P1-B152](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B153](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B154](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B155](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json).

### REQ-PUSH1-WF-018 — Device mode and banks

**D12/target-U.** Device enables parameter encoders; Selection buttons choose devices and State buttons enable/disable the selected device. In/Out reaches additional parameter banks or rack chains. Exact banks/targets, codecs and DSP remain device/rack owned.

Evidence: [P1-B157](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B158](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B159](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B161](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B162](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json).

### REQ-PUSH1-WF-019 — Mix modes and split pan

**D12/target-U.** Volume, Pan/Send and Track modes select mix controls; Shift refines adjustment, Master selects Main and held group selection folds/unfolds. In split stereo pan, Pan/Send shows value but disables dial, while Track mode offers appropriate pan controls.

Evidence: [P1-B164](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B165](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B166](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B167](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B168](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B169](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B170](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B171](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json).

### REQ-PUSH1-WF-020 — Automation entry and indicators

**D12/target-U.** Automation toggles Session Automation Arm; Delete plus encoder touch deletes recorded parameter automation or resets unautomated parameter to default. Recorded/overridden parameters have rectangle/bracket presentation; Shift-Automation re-enables overridden automation.

Evidence: [P1-B173](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B174](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B175](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B176](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json).

### REQ-PUSH1-WF-021 — Held-step editing and automation

**D12/target-U.** Holding steps exposes note Nudge, coarse/fine Length and Velocity with multistep selection; empty-step edits can create notes and Duplicate copies note settings. Device/Volume modes permit per-step automation even without notes. Exact values/timebase remain unproven.

Evidence: [P1-B178](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B179](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B181](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B183](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B184](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B185](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B186](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B187](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B188](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B189](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B190](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B192](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json).

### REQ-PUSH1-WF-022 — Session entry, clip and stop controls

**D12/target-U.** Session/Note hold gives momentary mode access. Session pad/Scene controls launch corresponding material and Select chooses without launch; Stop mode stops a track and Shift-Stop stops all clips. The selected-track new-record sentence lacks full slot prerequisites and stays context only.

Evidence: [P1-B194](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B195](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B200](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B201](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B202](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B237](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B300](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json).

### REQ-PUSH1-WF-023 — Session navigation and overview

**D12/target-U.** Session arrows and modifiers move the controlled region; Shift exposes Session Overview where pads choose larger blocks and scene controls larger scene ranges. Region borders link software/hardware focus; no numeric pad-to-track/scene or viewport oracle is added.

Evidence: [P1-B203](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B204](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B205](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B207](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json).

### REQ-PUSH1-WF-024 — User preferences and alternate mode

**D12/target-U.** Held User opens pad/aftertouch response and Workflow preferences; User Mode disables built-in functionality for alternate mapping. Recommended relative-encoder mode and sensitivity/threshold examples supply no complete protocol, force curve or configuration-token equivalence.

Evidence: [P1-B214](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B215](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B216](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B217](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B226](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B248](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json).

### REQ-PUSH1-WF-025 — Touch strip contextual roles

**D12/target-U.** Instrument real-time touch strip controls pitch bend or mod wheel, toggled by Select-tap; melodic sequencing uses note-range navigation and Drum Rack uses bank selection. Real-time expression is not offered in melodic step-sequencer context.

Evidence: [P1-B293](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B294](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json).

### REQ-PUSH1-WF-026 — Track/effect and common edit entrypoints

**D12/target-U.** Add Track/Add Effect and modifiers expose track-type and insertion-side entrypoints, with selected group context affecting placement. Undo/Shift-Undo invokes Live history, Delete is context-sensitive, Double extends loop material, and Record-New on armed MIDI triggers Capture. Generic history/record/rack semantics stay with their owners.

Evidence: [P1-B081](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B082](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B083](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B084](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B240](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B241](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B281](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B282](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B284](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json), [P1-B289](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1-blocks.json).

### REQ-PUSH1-WF-U-PROTOCOL — Hardware, firmware and protocol

**U/target-U.** Accepted hardware/firmware/platform/USB/ports, messages, LED palette/framebuffer, touch/pressure/velocity calibration, pedal polarity, latency and User Mode protocol remain unknown. Source presence and control names are not hardware capability proof.

Evidence: unsupported outcome; ungraded investigation obligation for this model.

### REQ-PUSH1-WF-U-CONTEXT — Model and ambiguous source contexts

**U/target-U.** Per-mode/track/layout defaults, unsupported/empty/selected-slot recording predicates, conflicting button/context wording, model note maps and same-label behavior require evidence. Push 1 source cannot establish Push 2/3 parity.

Evidence: unsupported outcome; ungraded investigation obligation for this model.

### REQ-PUSH1-WF-U-EDIT — Editing and boundary outcomes

**U/target-U.** Empty/end/overlap/range/duplicate/choke/note/step boundaries, arbitrary slice placement, quantization, note expression/tuning and admitted malformed controls have no new numerical, refusal or normalization law.

Evidence: unsupported outcome; ungraded investigation obligation for this model.

### REQ-PUSH1-WF-U-STATE — History and durable state

**U/target-U.** Undo grouping, cancel/rollback, saved override/arm/mode/selection/Workflow/scale/pad settings, defaults, device/clip transfers and reopen migration remain unknown beyond documentary roles.

Evidence: unsupported outcome; ungraded investigation obligation for this model.

### REQ-PUSH1-WF-U-CLOCK — Transport, recording and rates

**U/target-U.** Recording ownership, event generation, quantization/phase, repeat/swing/pressure response, automation return, engine/sample-rate/block/tempo/transport transitions and synchronization remain ungraded.

Evidence: unsupported outcome; ungraded investigation obligation for this model.

### REQ-PUSH1-WF-U-LOSS — Failure, source loss and teardown

**U/target-U.** Controller/port/media/device/track loss, disconnection/reconnect, engine restart, concurrent editing, close/replace Set and quit during held inputs/record/pending operations have no new recovery, cleanup or silence deadline.

Evidence: unsupported outcome; ungraded investigation obligation for this model.

## Push 2

### REQ-PUSH2-WF-001 — Power/USB and firmware setup context

**D12/target-U.** Push 2 setup describes included power, USB and power-on followed by automatic Live recognition without manual driver/Settings setup. Live updates may prompt firmware update. No firmware bytes, supported version set, updater, deadline or recovery law is specified.

Evidence: [P2-B006](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B007](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json).

### REQ-PUSH2-WF-002 — Browse columns, preview and load

**D12/target-U.** Browse exposes context-dependent columns/Collections, encoders/arrows navigate and upper controls move hierarchy. Preview toggles browser audition, Shift-Master adjusts preview level and Load loads selection. Instrument/effect/empty-track context filters available content.

Evidence: [P2-B009](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B010](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B011](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B012](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B013](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B014](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B015](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B016](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json).

### REQ-PUSH2-WF-003 — Drum layouts and Layout hold

**D12/target-U.** With Drum Rack in Note Mode, Layout cycles Loop Selector, velocity and full-grid modes; held Layout exposes alternate controls and Shift-Layout locks them. Octave/touch strip changes drum banks without automatically changing the sequenced subset across layout changes.

Evidence: [P2-B018](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B019](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B020](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B022](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B030](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B031](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B033](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B034](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B036](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B037](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B038](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json).

### REQ-PUSH2-WF-004 — Individual pad browse and selection

**D12/target-U.** Device focus plus pad and second upper display button selects pad-level Browse. Load changes to Load Next with a previous-entry option; Select-pad avoids triggering, and expanded rack lower controls/arrows select pads without playing.

Evidence: [P2-B040](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B041](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B042](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B043](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B044](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B045](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json).

### REQ-PUSH2-WF-005 — Pad copy and local options

**D12/target-U.** Duplicate source-to-destination replaces destination pad devices but retains its recorded notes. Selected pad offers choke group/transposition; Shift-pad opens custom-color choice saved with Set and shown on Push, not Live. No LED palette, note number or choke/DSP law follows.

Evidence: [P2-B047](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B048](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B049](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B050](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B051](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json).

### REQ-PUSH2-WF-006 — Drum step editing

**D12/target-U.** Pad selection enables sequencing; steps add/delete notes, Mute deactivates without deletion and Solo solos the sound. Delete can clear pattern/pad notes; Delete on a pad without notes in current pattern removes its devices. Triplet layout has inactive pads; no event/grid equation is supplied.

Evidence: [P2-B053](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B054](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B056](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B058](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B063](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json).

### REQ-PUSH2-WF-007 — Record, Accent and overdub

**D12/target-U.** Record alternates record/playback/overdub, with metronome/count-in display context. Accent overrides velocity-sensitive playing/step entry and velocity-pad selection; tap latches and hold is momentary. No velocity byte/force curve, countdown or event timing oracle is added.

Evidence: [P2-B067](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B068](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B069](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B070](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B071](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B072](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B073](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json).

### REQ-PUSH2-WF-008 — New and Workflow modes

**D12/target-U.** Scene Workflow Duplicate captures playing clips and New omits selected clip while preparing new material. Clip Workflow Duplicate/New narrows to selected track/clip while other clips continue; Shift-Duplicate captures a scene. Seamless language supplies no audio or scheduler metric.

Evidence: [P2-B074](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B339](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B341](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B342](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B345](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B346](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json).

### REQ-PUSH2-WF-009 — Fixed Length and Phrase Sync roles

**D12/target-U.** Fixed Length and held length selector govern new recording span; enabling during record stops writing and loops preceding material. Phrase Sync relates recording start inside the chosen phrase to current song phase, unlike described beginning-of-clip start. No phrase modulo or quantization formula is adopted.

Evidence: [P2-B076](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B077](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B078](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B079](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B080](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json).

### REQ-PUSH2-WF-010 — Quantize controls and record-swing context

**D12/target-U.** Quantize and held settings expose note-grid, amount, swing and record quantization; pad modifier narrows to that drum. Record Quantize with Swing is described as not applying swing to automatically quantized notes. Algorithms and exact note positions stay with MIDI/groove/record owners or U.

Evidence: [P2-B087](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B088](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B089](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B090](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B091](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B092](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json).

### REQ-PUSH2-WF-011 — Focus-dependent Arrangement recording

**D12/target-U.** Record toggles Arrangement recording when Arrangement is focused; Shift-Record requests it from Session focus. In Arrangement focus Shift-Record instead toggles Session recording. Other selection/recording prerequisites and actual written events retain their owners.

Evidence: [P2-B094](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B095](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json).

### REQ-PUSH2-WF-012 — Pitched/Scale controls

**D12/target-U.** Instrument Note Mode offers pitched pads; Scale selects key/type, Layout/Direction, Fixed and In Key/Chromatic settings. Scale settings are described as Set-persistent and default-Set eligible; Delete-pad removes same-pitch notes in current loop. No pad-note/tuning/default/velocity equation follows.

Evidence: [P2-B102](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B110](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B112](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B113](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B114](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B116](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B117](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B118](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B119](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B120](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B121](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B122](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json).

### REQ-PUSH2-WF-013 — Melodic sequencer layout and range

**D12/target-U.** Layout selects melodic sequencers; held Layout exposes loop pads and Shift-Layout locks per track. Rows use selected scale pitches and columns chosen grid steps; Octave/touch strip and Shift alter range. No exact note-to-pad or step-time equation is supplied.

Evidence: [P2-B124](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B125](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B126](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B127](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B128](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B130](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json).

### REQ-PUSH2-WF-014 — Loop pages, follow and duplication

**D12/target-U.** Loop pads set span/view; viewed page may differ from sounding page. Reselecting loop or holding Page navigation restores follow, while out-of-loop page selection changes loop. Page Duplicate adds notes over destination and Delete-page clears first.

Evidence: [P2-B133](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B134](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B135](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B142](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B143](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json).

### REQ-PUSH2-WF-015 — Track navigation and arm context

**D12/target-U.** Lower controls/arrows select tracks; MIDI selection is described as auto-arming and held track control or Record-plus-track manually arms. Up/down has Scene versus Clip Workflow scope and source describes immediate Legato-like continuation. No universal arm/default or timing law is supplied.

Evidence: [P2-B215](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B216](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B217](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B218](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B219](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B220](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json).

### REQ-PUSH2-WF-016 — Device editing and pages

**D12/target-U.** Device mode selects current-track devices via upper display controls; pressing selected control enters Edit with lower parameter pages and navigation for further pages. Leftmost upper control returns to top level. Actual target banks/plug-in support remain separate.

Evidence: [P2-B222](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B223](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B224](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B225](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B226](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json).

### REQ-PUSH2-WF-017 — Device insertion, mute, reorder and racks

**D12/target-U.** Add Device browses insertable types; instrument loading replaces existing instrument, effects have documented chain-side roles. Delete/Mute plus device and held-control encoder reorder are entrypoints. Rack device unfolding/macros/chain selection has distinct context, with Drum Rack fold state described as software-controlled here.

Evidence: [P2-B228](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B229](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B230](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B231](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B232](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B233](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B234](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B235](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B238](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B239](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B240](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json).

### REQ-PUSH2-WF-018 — Track/global Mix and split pan

**D12/target-U.** Mix alternates selected-track and visible-track global controls; Track Input/Output exposes routing. Extra return/track navigation, Shift refinement and Master previous-track return are provided. Split pan disables Global dial while Track mode offers corresponding pan controls.

Evidence: [P2-B242](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B243](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B244](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B245](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B246](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B247](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B248](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B249](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B250](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B251](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json).

### REQ-PUSH2-WF-019 — Mix-context rack/group expansion

**D12/target-U.** In Mix context, group/rack tracks can be unfolded with their lower display control to expose contained tracks/chains; arrows reach additional contents and Select-pad jumps to its mixer. This is distinct from Device-context Drum Rack unfolding.

Evidence: [P2-B253](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B254](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B255](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json).

### REQ-PUSH2-WF-020 — Automation controls and status

**D12/target-U.** Automation toggles Session Automation Arm; Delete-touch encoder deletes automation or resets unautomated default. Display dots distinguish automated/overridden parameters; Shift-Automation re-enables overridden automation. Numeric default, events, persistence and return timing remain U.

Evidence: [P2-B257](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B258](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B259](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B260](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json).

### REQ-PUSH2-WF-021 — Held-step automation and notes

**D12/target-U.** Clip mode held steps expose note Nudge, coarse/fine Length and Velocity including multiple/empty steps; Device/Mix held steps edit per-step parameter automation even without notes. No note-time percentage conversion or generated event law is supplied.

Evidence: [P2-B262](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B263](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B264](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B265](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B294](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B296](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B297](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B298](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B299](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B300](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B301](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B302](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json).

### REQ-PUSH2-WF-022 — Session entry, selection and stopping

**D12/target-U.** Held Session/Note offers momentary modes; Session pad/scene controls launch material, Select-pad selects without launch, Duplicate copies clip and Stop Clip/Mute/Solo have selected-track, held-track and locked contexts. Shift-Stop Clip stops all. New-record selected-track sentence lacks full slot context and stays U.

Evidence: [P2-B304](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B305](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B311](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B312](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B313](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B314](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B315](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B316](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B318](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B319](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B320](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B322](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json).

### REQ-PUSH2-WF-023 — Session Overview access

**D12/target-U.** Held Layout opens Session Overview; Shift-Layout locks and Layout unlocks it. Pads select larger scene/track blocks and scene controls wider ranges. No figure-derived numeric pad/block mapping or LED palette is prescribed.

Evidence: [P2-B325](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B326](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json).

### REQ-PUSH2-WF-024 — Setup response and brightness controls

**D12/target-U.** Setup exposes Pad Sensitivity, Gain, Dynamics, Display Light, LED Brightness and Workflow. The source describes response curves and a linear-setting recipe, but these supply no force/velocity/LED calibration, numeric hardware output or default-build guarantee.

Evidence: [P2-B332](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B333](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B334](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B335](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B336](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B337](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B338](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B339](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json).

### REQ-PUSH2-WF-025 — Simpler sample display/control entry

**D12/target-U.** Push 2 sample workflow uses Simpler: empty state prompts sample browsing, loaded waveform/position/zoom controls and Classic/One-Shot/Slicing choices are exposed. Simpler Edit pages, crop/reverse and slice creation/nudge/split/delete are controller entrypoints only; all mode/voice/DSP/sample semantics remain with sample-instrument and conversion/media owners.

Evidence: [P2-B171](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B172](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B173](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B175](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B176](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B177](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B178](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B180](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B181](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B182](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B184](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B197](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B198](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B202](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B211](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B212](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B213](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json).

### REQ-PUSH2-WF-026 — Clip mode controls and display

**D12/target-U.** Clip opens selected-clip parameters with audio/no-selection prompt, loop/start/end controls, zoom and audio Warp/gain/transpose context. MIDI layouts have Crop and sequenceable-area display/range navigation. Clip View and MIDI owners retain region/edit algorithms; no pad/time or folded-view numeric law is added.

Evidence: [P2-B267](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B268](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B269](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B271](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B272](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B273](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B274](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B275](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B279](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B281](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B283](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B288](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B290](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B292](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json).

### REQ-PUSH2-WF-027 — Touch strip and User Mode roles

**D12/target-U.** Instrument real-time touch strip selects pitch bend/mod wheel with Select-tap; melodic sequencing changes range and Drum Rack changes bank. User Mode disables built-in roles for alternate mapping; recommended relative mode is not exact configuration-token/codec equivalence.

Evidence: [P2-B371](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json), [P2-B378](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2-blocks.json).

### REQ-PUSH2-WF-U-PROTOCOL — Hardware, firmware and protocol

**U/target-U.** Accepted hardware/firmware/platform/USB/ports, messages, LED palette/framebuffer, touch/pressure/velocity calibration, pedal polarity, latency and User Mode protocol remain unknown. Source presence and control names are not hardware capability proof.

Evidence: unsupported outcome; ungraded investigation obligation for this model.

### REQ-PUSH2-WF-U-CONTEXT — Model and ambiguous source contexts

**U/target-U.** Per-mode/track/layout defaults, unsupported/empty/selected-slot recording predicates, conflicting button/context wording, model note maps and same-label behavior require evidence. Push 1 source cannot establish Push 2/3 parity.

Evidence: unsupported outcome; ungraded investigation obligation for this model.

### REQ-PUSH2-WF-U-EDIT — Editing and boundary outcomes

**U/target-U.** Empty/end/overlap/range/duplicate/choke/note/step boundaries, arbitrary slice placement, quantization, note expression/tuning and admitted malformed controls have no new numerical, refusal or normalization law.

Evidence: unsupported outcome; ungraded investigation obligation for this model.

### REQ-PUSH2-WF-U-STATE — History and durable state

**U/target-U.** Undo grouping, cancel/rollback, saved override/arm/mode/selection/Workflow/scale/pad settings, defaults, device/clip transfers and reopen migration remain unknown beyond documentary roles.

Evidence: unsupported outcome; ungraded investigation obligation for this model.

### REQ-PUSH2-WF-U-CLOCK — Transport, recording and rates

**U/target-U.** Recording ownership, event generation, quantization/phase, repeat/swing/pressure response, automation return, engine/sample-rate/block/tempo/transport transitions and synchronization remain ungraded.

Evidence: unsupported outcome; ungraded investigation obligation for this model.

### REQ-PUSH2-WF-U-LOSS — Failure, source loss and teardown

**U/target-U.** Controller/port/media/device/track loss, disconnection/reconnect, engine restart, concurrent editing, close/replace Set and quit during held inputs/record/pending operations have no new recovery, cleanup or silence deadline.

Evidence: unsupported outcome; ungraded investigation obligation for this model.

## Finite cases and remaining obligations

The [77 proposed cases](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/cases.json) map to 65
[requirements](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/requirements.json): 53 D12 and 12 U. Push 1 has 26 D12/six U
and 38 cases; Push 2 has 27 D12/six U and 39 cases. Eighteen cases have only visible
documentary proposals; 59 have null documentary oracles. All 77 target oracles are
null/U and unexecuted. These counts do not close either model or any profile family.
Each named action branch/control mode requires its own later retained result.

| Case | Requirement | Kind | Action focus |
| --- | --- | --- | --- |
| P1-WF-001 | REQ-PUSH1-WF-001 | protocol | USB setup role |
| P1-WF-002 | REQ-PUSH1-WF-002 | control | Browse navigation and load |
| P1-WF-003 | REQ-PUSH1-WF-003 | control | Browse context filtering |
| P1-WF-004 | REQ-PUSH1-WF-004 | pad-role | Drum layout roles |
| P1-WF-005 | REQ-PUSH1-WF-005 | pad-role | Drum pad bank and silent selection |
| P1-WF-006 | REQ-PUSH1-WF-006 | control | Individual drum browsing and copy |
| P1-WF-007 | REQ-PUSH1-WF-007 | midi-output | Drum step gestures |
| P1-WF-008 | REQ-PUSH1-WF-008 | recording | Record and overdub controls |
| P1-WF-009 | REQ-PUSH1-WF-009 | timing | New and workflow modes |
| P1-WF-010 | REQ-PUSH1-WF-010 | timing | Fixed Length controls |
| P1-WF-011 | REQ-PUSH1-WF-011 | timing | Repeat and swing roles |
| P1-WF-012 | REQ-PUSH1-WF-012 | editing | Quantize entry and scope |
| P1-WF-013 | REQ-PUSH1-WF-013 | pad-role | Pitched pad and scale layouts |
| P1-WF-014 | REQ-PUSH1-WF-014 | pad-role | Melodic step and loop layout |
| P1-WF-015 | REQ-PUSH1-WF-015 | timing | Loop page selection and copy |
| P1-WF-016 | REQ-PUSH1-WF-016 | pad-role | Combined melodic playing and sequencing |
| P1-WF-017 | REQ-PUSH1-WF-017 | timing | Note navigation and arm context |
| P1-WF-018 | REQ-PUSH1-WF-018 | control | Device mode and banks |
| P1-WF-019 | REQ-PUSH1-WF-019 | control | Mix modes and split pan |
| P1-WF-020 | REQ-PUSH1-WF-020 | control | Automation entry and indicators |
| P1-WF-021 | REQ-PUSH1-WF-021 | editing | Held-step editing and automation |
| P1-WF-022 | REQ-PUSH1-WF-022 | pad-role | Session entry, clip and stop controls |
| P1-WF-023 | REQ-PUSH1-WF-023 | pad-role | Session navigation and overview |
| P1-WF-024 | REQ-PUSH1-WF-024 | control | User preferences and alternate mode |
| P1-WF-025 | REQ-PUSH1-WF-025 | signal | Touch strip contextual roles |
| P1-WF-026 | REQ-PUSH1-WF-026 | control | Track/effect and common edit entrypoints |
| P2-WF-001 | REQ-PUSH2-WF-001 | protocol | Power/USB and firmware setup context |
| P2-WF-002 | REQ-PUSH2-WF-002 | control | Browse columns, preview and load |
| P2-WF-003 | REQ-PUSH2-WF-003 | pad-role | Drum layouts and Layout hold |
| P2-WF-004 | REQ-PUSH2-WF-004 | control | Individual pad browse and selection |
| P2-WF-005 | REQ-PUSH2-WF-005 | control | Pad copy and local options |
| P2-WF-006 | REQ-PUSH2-WF-006 | midi-output | Drum step editing |
| P2-WF-007 | REQ-PUSH2-WF-007 | recording | Record, Accent and overdub |
| P2-WF-008 | REQ-PUSH2-WF-008 | timing | New and Workflow modes |
| P2-WF-009 | REQ-PUSH2-WF-009 | timing | Fixed Length and Phrase Sync roles |
| P2-WF-010 | REQ-PUSH2-WF-010 | editing | Quantize controls and record-swing context |
| P2-WF-011 | REQ-PUSH2-WF-011 | recording | Focus-dependent Arrangement recording |
| P2-WF-012 | REQ-PUSH2-WF-012 | pad-role | Pitched/Scale controls |
| P2-WF-013 | REQ-PUSH2-WF-013 | pad-role | Melodic sequencer layout and range |
| P2-WF-014 | REQ-PUSH2-WF-014 | timing | Loop pages, follow and duplication |
| P2-WF-015 | REQ-PUSH2-WF-015 | timing | Track navigation and arm context |
| P2-WF-016 | REQ-PUSH2-WF-016 | control | Device editing and pages |
| P2-WF-017 | REQ-PUSH2-WF-017 | control | Device insertion, mute, reorder and racks |
| P2-WF-018 | REQ-PUSH2-WF-018 | control | Track/global Mix and split pan |
| P2-WF-019 | REQ-PUSH2-WF-019 | control | Mix-context rack/group expansion |
| P2-WF-020 | REQ-PUSH2-WF-020 | control | Automation controls and status |
| P2-WF-021 | REQ-PUSH2-WF-021 | editing | Held-step automation and notes |
| P2-WF-022 | REQ-PUSH2-WF-022 | pad-role | Session entry, selection and stopping |
| P2-WF-023 | REQ-PUSH2-WF-023 | pad-role | Session Overview access |
| P2-WF-024 | REQ-PUSH2-WF-024 | control | Setup response and brightness controls |
| P2-WF-025 | REQ-PUSH2-WF-025 | control | Simpler sample display/control entry |
| P2-WF-026 | REQ-PUSH2-WF-026 | editing | Clip mode controls and display |
| P2-WF-027 | REQ-PUSH2-WF-027 | signal | Touch strip and User Mode roles |
| P1-U-HARDWARE | REQ-PUSH1-WF-U-PROTOCOL | protocol | Hardware |
| P1-U-INACTIVE | REQ-PUSH1-WF-U-CONTEXT | negative | Inactive |
| P1-U-SELECTED-SLOT | REQ-PUSH1-WF-U-CONTEXT | boundary | Selected slot |
| P1-U-BOUNDARIES | REQ-PUSH1-WF-U-EDIT | boundary | Boundaries |
| P1-U-MALFORMED | REQ-PUSH1-WF-U-EDIT | malformed | Malformed |
| P1-U-UNDO | REQ-PUSH1-WF-U-STATE | undo | Undo |
| P1-U-CANCEL | REQ-PUSH1-WF-U-STATE | cancel | Cancel |
| P1-U-REOPEN | REQ-PUSH1-WF-U-STATE | persistence | Reopen |
| P1-U-RECORD-AND-AUTOMATION | REQ-PUSH1-WF-U-CLOCK | automation | Record and automation |
| P1-U-TRANSPORT-RATE | REQ-PUSH1-WF-U-CLOCK | sample-rate | Transport rate |
| P1-U-DISCONNECT | REQ-PUSH1-WF-U-LOSS | source-loss | Disconnect |
| P1-U-TEARDOWN | REQ-PUSH1-WF-U-LOSS | teardown | Teardown |
| P2-U-HARDWARE | REQ-PUSH2-WF-U-PROTOCOL | protocol | Hardware |
| P2-U-INACTIVE | REQ-PUSH2-WF-U-CONTEXT | negative | Inactive |
| P2-U-SELECTED-SLOT | REQ-PUSH2-WF-U-CONTEXT | boundary | Selected slot |
| P2-U-BOUNDARIES | REQ-PUSH2-WF-U-EDIT | boundary | Boundaries |
| P2-U-MALFORMED | REQ-PUSH2-WF-U-EDIT | malformed | Malformed |
| P2-U-UNDO | REQ-PUSH2-WF-U-STATE | undo | Undo |
| P2-U-CANCEL | REQ-PUSH2-WF-U-STATE | cancel | Cancel |
| P2-U-REOPEN | REQ-PUSH2-WF-U-STATE | persistence | Reopen |
| P2-U-RECORD-AND-AUTOMATION | REQ-PUSH2-WF-U-CLOCK | automation | Record and automation |
| P2-U-TRANSPORT-RATE | REQ-PUSH2-WF-U-CLOCK | sample-rate | Transport rate |
| P2-U-DISCONNECT | REQ-PUSH2-WF-U-LOSS | source-loss | Disconnect |
| P2-U-TEARDOWN | REQ-PUSH2-WF-U-LOSS | teardown | Teardown |

## Source-context questions

[Research local questions](../research/push-controller-workflows.md#source-context-questions)
retain Push 1 Note/Layout wording, selected-track/new-clip recording context and
mode-specific settings/labels. Ambiguous text is not silently repaired from Push 2
or source figures. Source Session/overview colors and pressure/velocity recipes
are retained but not adopted as LED or physical-calibration laws.

Per-model U probes retain inactive/unsupported paths, occupied/empty/boundary
targets, malformed admitted inputs, cancel, Undo/Redo, save/reopen/migration,
automation ownership, transport/rates, disconnection/source loss and teardown.
Pedals, every remaining reference control, profile bank/protocol and firmware
failure handling remain incomplete. No whole hardware family or compatibility is
claimed. [Q-027](../questions.md#q-027-whole-product-specification-evidence-and-version-coverage)
retains publication/build applicability.

## Analyst evidence appendix

[Source ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/sources.json) pins both exact URLs/final URLs, UTC capture,
Version 12 identity, HTML size and SHA256. [Owner pins](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/owner-pins.json)
retain 15 canonical boundaries unchanged. [Counts](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/counts.json),
[frozen manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manifest-author-r1.json), [parser](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/source_parser.py)
and read-only [validator](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/validate.py) identify the reviewable packet.

| Model | Retained chapter | Blocks | Text |
| --- | --- | --- | --- |
| Push 1 | §35/using-push-1; setup through control reference/footswitches |303| [Push 1 text](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-1.txt) |
| Push 2 | §36/using-push-2; setup through control reference/footswitches |403| [Push 2 text](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/manual-push-2.txt) |

Original HTML lines, anchors, section and heading context accompany each derived
block. Figures/PDFs/videos and native/controller code were not inspected. Root
integrates shared indexes, coverage, questions and log after independent review.
