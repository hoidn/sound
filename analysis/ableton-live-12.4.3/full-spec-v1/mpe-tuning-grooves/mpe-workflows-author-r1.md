---
id: SPEC-MPE-WORKFLOWS
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3; current Live 12 documentation, exact-build applicability unknown
---

# Per-note expression and MPE routing workflows

## Scope and ownership

Canonical owner for per-note expression viewing/editing and MPE input/output
configuration in F-04. This is a partial documented-domain contract, not a release
or compatibility result. D12 means retained current official Live 12 documentation;
**all exact 12.4.3 behavioral grades are U**. S-presence means installed resource
vocabulary only and supports none of the editor or channel-emission laws below.
No original application, hardware, plug-in or candidate was executed.

[MIDI note storage](midi-note-storage.md) owns note/expression file fields and
validation. [MIDI editing and tools](midi-editing-tools.md) owns note selection,
movement/stretch commands, velocity editing and expression-generating tools.
This page owns the attached-expression consequences of those commands.
[Automation envelopes](automation-envelopes.md) does not supply an MPE
interpolator by analogy. [Tuning systems](tuning-systems.md) owns tuning's pitch
range prerequisite. Device-specific modulation destinations/sound, recording,
general routing and hardware protocols remain with their respective owners.

## Inputs, units and state

Cases use an editable MIDI clip with two distinguishable notes, ordinary finite
breakpoints strictly inside each note, explicit tab/fold/grid state, and reset
state per case. Time is in quarter-note beats; pitch labels use semitones where
displayed. Slide/Pressure and note velocities are named expression values; their
UI domains, scaling and conversion to stored/MIDI values are U here. In
particular, storage's CC -2 domain is not a semitone conversion law.

Clip selection, note/breakpoint/time selection, grid and lane visibility,
expression data, controller MPE enablement, track input choice, output target,
output zone/channel range and plug-in MPE state are distinct. UI cases compare
visible state and represented editing results, without pixel or latency claims.
Output-zone cases compare selectable configuration only; message bytes,
allocation/stealing, RPN negotiation and receiver audio are U.

## Requirements

All rows are D12 with target U. M/H locators are pinned in the analyst appendix.

| ID | Inputs / precondition | Observable transition and limits | Evidence |
| --- | --- | --- | --- |
| REQ-MPE-001 | Enable a controller's MPE mode in MIDI settings; choose that controller as track input. | Input channel selection is fixed to All Channels. Receiving/recording per-note expression requires the controller's MPE mode. Disabled-mode interpretation and hot-unplug outcome U. | M1 |
| REQ-MPE-002 | Open any MIDI clip, including one made without MPE hardware; choose Note Expression or Alt+3 (Win)/Option+3 (Mac). | Provide Pitch, Slide, Pressure, Velocity and Release Velocity editing. Pitch overlays notes; chapter 12 describes the other four as lanes, with Slide/Pressure initially visible. Optional Pitch Bend lane contexts remain U (below). | M1–M2 |
| REQ-MPE-003 | Toggle lane selectors or the triangle; drag lane split lines. | Selectors show/hide lanes; triangle toggles enabled lanes together, shows all when none enabled; Alt/Option-click shows all. Splits resize an individual lane or all lanes. Hiding lanes through triangle/split also hides selectors. Minimum sizes U. | M2 |
| REQ-MPE-004 | Note Expression open; select a note or expression dimension. | Selected note has an overlay and editable Pitch/Slide/Pressure breakpoints; Velocity/Release Velocity use markers. Other notes/envelopes are dimmed. Selecting a line exposes its draggable breakpoints/segments; background drag defines selection. | M3 |
| REQ-MPE-005 | Active envelope; click a segment, click a breakpoint, or choose Edit Value/Add Value. | Segment click adds a breakpoint; breakpoint click deletes it. Edit Value sets a typed exact value; Add Value adds a preview breakpoint at a typed value. Multiple selected breakpoint values move relatively. Hover/create/drag exposes the value at the cursor position. Invalid input/rounding U. | M3 |
| REQ-MPE-006 | Drag a selected breakpoint or a selected line segment. | Selected breakpoints move together. Segment in a time selection inserts breakpoints at selection edges and moves that section together. Shift-drag restricts an axis and supports finer vertical adjustment. Dragging horizontally over a neighbor can remove it. Thresholds/equal-time ordering/clipping U. | M3 |
| REQ-MPE-007 | Use Note Expression grid, Ctrl+4 (Win)/Cmd+4 (Mac), then save clip. | Grid starts disabled, is separate from other tabs and is saved with clip. Enabled edits snap to neighboring breakpoint times; creation near grid lines snaps. Pixel thresholds, grid storage and load failures U. | M3 |
| REQ-MPE-008 | Alt/Option-drag a segment, then Alt/Option-double-click it. | First gesture curves segment; second restores a straight segment. Exact interpolation/sample values U; ordinary automation's evaluator is not imported. | M3 |
| REQ-MPE-009 | Click outside a note then drag a highlighted non-Pitch expression vertically; alternatively select all breakpoints in one envelope then drag. | First gesture proportionally scales Slide/Pressure/Velocity/Release Velocity over note duration, also across selected notes. Second adds equal value/time movement to selected breakpoints. Pitch is excluded from proportional scaling. Scale origin, zero crossing and clipping U. | M3 |
| REQ-MPE-010 | Move a note or stretch it with note stretch markers or ÷2/x2. | Attached expression follows note movement and stretches with note duration. Absolute-time copy/trim, transpose/bend interaction, interpolation and boundary reconstruction U. Note-command targeting remains with MIDI editing. | M3 |
| REQ-MPE-011 | Pitch edit/draw with grid off; hold Alt (Win)/Cmd (Mac). Open Note Expression and invoke Zoom to Clip Selection. | Modifier snaps Pitch to nearest semitone; with grid on it bypasses this behavior. Zoom includes pitch bends in selected time. Chapter 12 says Fold hides over-note Pitch envelopes; availability of a separate folded Pitch Bend lane is unresolved. Tie direction U. | M3 |
| REQ-MPE-012 | Select one or multiple notes in Note Expression and invoke Clear All Envelopes. | Clear all selected notes' expression envelopes. Whether note velocities/release velocities reset, resulting defaults, undo scope and note data beyond envelopes U. | M3 |
| REQ-MPE-013 | Enable Draw Mode with B/menu/switch, or hold B temporarily; draw Pitch/Slide/Pressure. | Draw edits selected expression; grid-on drawing creates steps at visible grid width. Alt (Win)/Cmd (Mac) temporarily enables grid drawing while grid off; Shift gives finer vertical adjustment. Sampling, endpoint and sparse gesture laws U. | M4 |
| REQ-MPE-014 | MPE controller values pass a MIDI track meter; use an MPE-enabled plug-in. | Meter's lowest dot indicates per-note changes in blue. Plug-in MPE mode is saved with device default configuration; MPE-enabled plug-ins with MIDI outs can output MPE. Plug-in failures, expression destinations and emitted encoding U. | M2, M5 |
| REQ-MPE-015 | Select external output target in External Instrument or track MIDI To; choose MPE then MPE Settings. For plug-in use MPE-enabled device context menu. | Open MPE/Multi-channel Settings for that routing target. Track mixer access applies in Session/Arrangement. Missing target and modal cancel behavior U. | M6 |
| REQ-MPE-016 | Choose lower/upper MPE output zone and note-channel count. | One zone per track; lower global channel is 1 and upper global channel 16, with note channels drawn from other channels. Two tracks are needed for both zones. Zones are documented for output only. Input zone filtering, allocation and overlapping-track conflicts U. | M7 |
| REQ-MPE-017 | Select multi-channel mode instead of zone mode. | Allow an arbitrary range of note channels. Accepted limits, reversed/empty ranges, inclusion of global channels, defaults and persistence U. A MIDI channel label does not establish a wire codec. | M7 |
| REQ-MPE-018 | MPE controller and receiving MPE instrument use pitch bend. | Correct tracking requires matching pitch-bend ranges. No default range, numeric editor domain, asymmetric endpoint scale, RPN behavior or live range-change policy is inferred. Tuning-specific ±48 prerequisite belongs to tuning owner. | H1 |

## Acceptance cases and lifecycle

The canonical authored [cases](../../analysis/ableton-live-12.4.3/full-spec-v1/mpe-tuning-grooves/cases.json)
contain **MPE-001–027: 18 D12 field-gradable proposals and 9 U cases**. Every
target-build grade is U and every case is unexecuted. Graders compare only stated
fields; no case establishes acoustic fidelity or unasserted expression values.
MPE-010's simple translation compares breakpoint time shifts of +2 beats;
stretching only grades the documented corresponding timing change, leaving
endpoint reconstruction U. MPE-016 explicitly tests the two global channels
and the single-zone limit, without claiming a channel-allocation sequence.

MPE-019–027 retain malformed numeric text, limits/codec, zero-duration/endpoints,
cancel, undo/redo, persistence, held-note route changes, device deletion/teardown
and folded-Pitch context obligations. Undo grouping, dialog commit timing,
save/reopen of all output settings, sounding-note reset messages and resource
failure are required unknowns. The UI gestures are synchronous descriptions;
no engine scheduling, sample-accurate update, CPU or cleanup guarantee follows.

## Unresolved scope and neighboring evidence

Full MPE coverage additionally requires note-on/off/channel reuse, simultaneous
same-pitch notes, pressure type conversion, global versus per-note controls,
MIDI effect forwarding, plugin formats, device bypass and defaults, automation,
chase/loop/record/overdub, disconnect/reconnect and malformed incoming MIDI.
These stay in the whole-product denominator. Per-note storage has its own
boundary-event unknowns; this page does not settle them through editor prose.

Chapter 12's hidden folded Pitch envelope and the MIDI Tools chapter's optional
Pitch Bend lane may refer to different views or states. The
[editing/tools visibility issue C3](midi-editing-tools.md#contradictions-and-incomplete-behavior)
owns the neighboring tool conflict. This page retains the context question as
U rather than declaring matching semantics from similar labels.

## Analyst evidence appendix

Canonical synthesis and source hashes:
[MPE, tuning and groove evidence](../research/mpe-tuning-grooves.md).
[Source records](../../analysis/ableton-live-12.4.3/full-spec-v1/mpe-tuning-grooves/sources.json)
pin official URLs, date and HTML hashes. M locators refer to numbered retained
`manual-12-editing-mpe.txt` in that packet; text after line 153 is navigation,
not additional behavioral evidence. Images were not inspected.

| Locator | Exact current-document section / text lines |
| --- | --- |
| M1 | Introduction, 3–15 |
| M2 | `viewing-mpe-data`, 16–34 |
| M3 | `editing-mpe-data`, 35–94 |
| M4 | `drawing-envelopes`, 95–119 |
| M5 | `mpe-in-external-plug-ins`, 123–127 |
| M6 | `accessing-the-mpemulti-channel-settings-dialog`, 128–142 |
| M7 | `the-mpemulti-channel-settings-dialog`, 143–153 |
| H1 | MPE FAQ, Troubleshooting MPE, rendered source L103–106; exact retained web-rendered text and hash recorded in research page |

Installed schema lines 5183–5187 declare MPE settings; the Drift preset contains
per-note bend-related configuration. These are S-presence corroboration only,
not a source for defaults or any D12 editor law. File fields remain with storage.
