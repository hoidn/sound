---
id: SPEC-MPE-WORKFLOWS
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 3
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
| REQ-MPE-001 | Enable a controller's MPE mode in MIDI settings; choose that controller as track input. Enable that controller in Link, Tempo & MIDI Settings before selecting it as track input. | Input channel selection is fixed to All Channels. Receiving/recording per-note expression requires the controller's MPE mode. Disabled-mode interpretation and hot-unplug outcome U. This source order does not establish hot-enabling an already selected controller. Ordinary recording eligibility remains with the recording owner. | M1; MPE-B003, MPE-B004, MPE-B005 |
| REQ-MPE-002 | Open any MIDI clip, including one made without MPE hardware; choose Note Expression or Alt+3 (Win)/Option+3 (Mac). | Provide Pitch, Slide, Pressure, Velocity and Release Velocity editing. Pitch overlays notes; chapter 12 describes the other four as lanes, with Slide/Pressure initially visible. Optional Pitch Bend lane contexts remain U (below). | M1–M2 |
| REQ-MPE-003 | Toggle lane selectors or the triangle; drag lane split lines. | Selectors show/hide lanes; triangle toggles enabled lanes together, shows all when none enabled; Alt/Option-click shows all. Splits resize an individual lane or all lanes. Hiding lanes through triangle/split also hides selectors. Minimum sizes U. | M2 |
| REQ-MPE-004 | Note Expression open; select a note or expression dimension. Actually drag the envelope background for a time selection. | Selected note has an overlay and editable Pitch/Slide/Pressure breakpoints; Velocity/Release Velocity use markers. Other notes/envelopes are dimmed. Selecting a line exposes its draggable breakpoints/segments; background drag defines selection. Note selection and background selection are separate inputs; Pitch/Slide/Pressure use envelopes while Velocity/Release Velocity use markers. | M3; MPE-B015, MPE-B016 |
| REQ-MPE-005 | Active envelope; click a segment, click a breakpoint, or choose Edit Value/Add Value with an admissible expression UI value. | Segment click adds a breakpoint; breakpoint click deletes it. Edit Value sets the typed admissible value; Add Value adds a preview breakpoint at that value. Multiple selected breakpoint values move relatively. Hover/create/drag exposes the value at the cursor position. Specific admissible numeric domains, invalid input and rounding U. | M3 |
| REQ-MPE-006 | Drag a selected breakpoint or a selected line segment. Select a segment by clicking near it, or Shift-clicking directly on it, then drag with the left mouse button held. | Selected breakpoints move together. Segment in a time selection inserts breakpoints at selection edges and moves that section together. Shift-drag restricts an axis and supports finer vertical adjustment. Dragging horizontally over a neighbor can remove it. Thresholds/equal-time ordering/clipping U. Selected-point group movement, selected-time segment movement, axis restriction, fine vertical adjustment and horizontal neighbor crossing are distinct admitted gestures; no resolution ratio is specified. | M3; MPE-B020, MPE-B022, MPE-B025, MPE-B026, MPE-B027 |
| REQ-MPE-007 | Use Note Expression grid, Ctrl+4 (Win)/Cmd+4 (Mac), then save clip. The Options Snap to Grid entry is another documented input. | Grid starts disabled, is separate from other tabs and is saved with clip. Enabled edits snap to neighboring breakpoint times; creation near grid lines snaps. Pixel thresholds, grid storage and load failures U. Actual neighboring-time movement and near-grid creation are distinct from merely toggling or saving the grid. | M3; MPE-B023, MPE-B024 |
| REQ-MPE-008 | Alt/Option-drag a segment, then Alt/Option-double-click it. | First gesture curves segment; second restores a straight segment. Exact interpolation/sample values U; ordinary automation's evaluator is not imported. | M3 |
| REQ-MPE-009 | Click outside a note then drag a highlighted non-Pitch expression vertically; alternatively select all breakpoints in one envelope then drag. For equal group movement select the envelope, then Ctrl+A Windows/Cmd+A Mac before vertical or horizontal dragging. | First gesture proportionally scales Slide/Pressure/Velocity/Release Velocity over note duration, also across selected notes. Second adds equal value/time movement to selected breakpoints. Pitch is excluded from proportional scaling. Scale origin, zero crossing and clipping U. The outside-note hover gesture applies to each named non-Pitch dimension and multiple selected notes; the equal group gesture also moves time horizontally. | M3; MPE-B029, MPE-B030 |
| REQ-MPE-010 | Move a note or stretch it with note stretch markers or ÷2/x2. | Attached expression follows note movement and stretches with note duration. Absolute-time copy/trim, transpose/bend interaction, interpolation and boundary reconstruction U. Note-command targeting remains with MIDI editing. | M3 |
| REQ-MPE-011 | Pitch edit/draw with grid off; hold Alt (Win)/Cmd (Mac). Open Note Expression and invoke Zoom to Clip Selection. Z is the other documented Zoom to Clip Selection entry. | Modifier snaps Pitch to nearest semitone; with grid on it bypasses this behavior. Zoom includes pitch bends in selected time. Chapter 12 says Fold hides over-note Pitch envelopes; availability of a separate folded Pitch Bend lane is unresolved. Tie direction U. Literal Pitch modifiers are Alt on Windows and Cmd on macOS, including Draw Mode; this is distinct from the Alt/Option curve gesture. Folded over-note Pitch and an optional Pitch Bend lane are not equated. | M3; MPE-B033, MPE-B034, MPE-B035 |
| REQ-MPE-012 | Select one or multiple notes in Note Expression and invoke Clear All Envelopes. Invoke the MIDI Note Editor context menu or a per-note expression lane context menu. | Clear all selected notes' expression envelopes. Whether note velocities/release velocities reset, resulting defaults, undo scope and note data beyond envelopes U. Each menu provides the selected-note envelope-clearing role; marker reset/defaults and unselected-data policy remain U. | M3; MPE-B036 |
| REQ-MPE-013 | Enable Draw Mode with B/menu/switch, or hold B temporarily; draw Pitch/Slide/Pressure. | Draw edits selected expression; grid-on drawing creates steps at visible grid width. Alt (Win)/Cmd (Mac) temporarily enables grid drawing while grid off; Shift gives finer vertical adjustment. Sampling, endpoint and sparse gesture laws U. | M4 |
| REQ-MPE-014 | MPE controller values pass a MIDI track meter; use an MPE-enabled plug-in. Independently distinguish per-note changes passing the selected track meter from generic Control Bar activity. | Meter's lowest dot indicates per-note changes in blue. Plug-in MPE mode is saved with device default configuration; MPE-enabled plug-ins with MIDI outs can output MPE. Plug-in failures, expression destinations and emitted encoding U. The enabled and disabled plug-in MPE Mode states are both included in the documented device-default saving role. A blue lowest track-meter dot is not proof of note delivery, isolated audio or plug-in MIDI output; those need independently admitted input/route/receiver context. | M2, M5; MPE-B013, MPE-B045, MPE-B046, MPE-B047 |
| REQ-MPE-015 | Select external output target in External Instrument or track MIDI To; choose MPE then MPE Settings. For plug-in use MPE-enabled device context menu. After choosing MPE, reopen the menu to choose MPE Settings; the plug-in entry is in its device-title-bar context menu. | Open MPE/Multi-channel Settings for that routing target. Track mixer access applies in Session/Arrangement. Missing target and modal cancel behavior U. Session and Arrangement mixer routes must each use their actual selected MIDI To target; merely seeing a menu does not open its associated dialog. | M6; MPE-B055, MPE-B056, MPE-B057 |
| REQ-MPE-016 | Choose lower/upper MPE output zone and note-channel count. | One zone per track; lower global channel is 1 and upper global channel 16, with note channels drawn from other channels. Two tracks are needed for both zones. Zones are documented for output only. Input zone filtering, allocation and overlapping-track conflicts U. | M7 |
| REQ-MPE-017 | Select multi-channel mode instead of zone mode. | Allow an arbitrary range of note channels. Accepted limits, reversed/empty ranges, inclusion of global channels, defaults and persistence U. A MIDI channel label does not establish a wire codec. | M7 |
| REQ-MPE-018 | MPE controller and receiving MPE instrument use pitch bend. | Correct tracking requires matching pitch-bend ranges. No default range, numeric editor domain, asymmetric endpoint scale, RPN behavior or live range-change policy is inferred. Tuning-specific ±48 prerequisite belongs to tuning owner. | H1 |

## Acceptance cases and lifecycle

The current [MPE-only cases](../../analysis/ableton-live-12.4.3/full-spec-v1/mpe-tuning-grooves/mpe-cases-r3.json)
contain **50 records:39 D12 documentary source contexts and11 U probes**. All27
original MPE records remain verbatim, including18 D12 proposals and9 U records;
23 appended actions add21 bounded D12 contexts and2 U integration probes.
Every actual target outcome remains null/U/unexecuted. The old shared83-case
catalog remains exact historical MPE/Groove context and current for unchanged
Tuning32; it is not appended or counted twice. Current Groove34 is separately
selected by its own owner. [Actual status](../../analysis/ableton-live-12.4.3/full-spec-v1/mpe-tuning-grooves/mpe-actual-status-r3.json)
keeps legacy expected/comparator strings documentary, never prior measurements.

The true old actions remain:005 create/delete/single entered admissible c;
006 selected-time segment/Shift-horizontal;007 grid/tab/save-reopen;010 move/x2;
014 enabled-default save/new instance;015 all three dialog routes;016 two-zone
tracks and017 admitted3..8 endpoints. Original010 time arithmetic,013 visible-grid
width proposal and all MTG review qualifications remain unchanged historical
records; no new numeric oracle is added here. Old001 selected-then-enable remains
an unexecuted historical recipe, not hot-enable-after-selection proof. New028
performs the source's explicit enable-before-selection order. Old014 is not an
actual meter, per-note input or output action. MPE005 retains three independently
admissible distinct interior Pressure UI values a,b,c; no20/40/30 domain is supplied.

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

Revision 2 applies MTG-REVIEW-003's admitted-value precondition. Requirement and
case counts are unchanged; the exact revision-1 packet is retained under the
research page's revision archive.


## R3 bounded retained-source adoption

The [reviewed source audit](../../analysis/ableton-live-12.4.3/full-spec-v1/mpe-source-audit/README.md)
read66 retained chapter blocks and110 judged source facets against18 clauses and
27 actions. Its [independent review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/mpe-source-audit-review.json)
approved partial source reconciliation, not this owner increment or source-topic
completion. All13 groups receive bounded role/input refinements or explicit
future actions through the [adoption ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/mpe-tuning-grooves/mpe-adoption-r3.json).
No new requirement ID or interpolation/channel/voice implementation is added.
[Exact delta](../../analysis/ableton-live-12.4.3/full-spec-v1/mpe-tuning-grooves/mpe-delta-r3.json)
refines nine rows; the other nine and all27 old cases stay exact.

New actions distinguish partial/none-enabled lane sets and split hiding, actual
background selection, cursor/Add Value/multiple Edit Value, selected point/segment
and neighbor/fine gestures, actual grid entry/snapping, four non-Pitch scale
contexts and equal group time movement, attached-expression halving/marker routes,
literal Pitch modifiers/zoom/Fold contexts, both clear menus, Draw inputs, genuine
track-meter input, disabled-default history and both mixer/zone-count controls.
Underlying note stretching MED008/MED012 and actual mode switching CV008 remain
with their existing owners. The new recording and plug-in output integration
probes have no documentary or actual output comparator. Initial lane/grid/custom
histories do not establish a factory reset or default constructor.

[Future prerequisites](../../analysis/ableton-live-12.4.3/full-spec-v1/mpe-tuning-grooves/mpe-fixtures-r3.json)
are conditional. Offline ordinary MIDI clip edits require **no MPE hardware**,
controller, MIDI output, instrument or sounding path. They require valid editable
nonempty data, admitted values/control/focus/selection and productive matching
edits before negative or exclusion observations. Actual input/record/output and
sound probes additionally require independently recognized genuine nonzero
per-note source, accepted active route/compatible receiver, nonzero relevant
modulation depth/gain and nonmuted positive output where relevant. A generic
Control Bar activity flash, lowest track-meter dot, enabled flag or saved default
is not per-note delivery proof. Configuration-only inspection needs no actual
wire traffic. Missing or failed prerequisites remain U, never absence success.

Fold describes the over-note Pitch context only; optional folded Pitch Bend lane
and MIDI tools C3 remain unresolved. Alt Windows/**Cmd** Mac is the literal Pitch
grid modifier, while curvature uses Alt/Option. FAQ018 requires matching ranges;
Tuning015's scoped ±48 prerequisite is not a universal MPE range. New numeric,
audio/MIDI, file, timing, protocol and curve outcomes stay documentary-null as
appropriate, with source_claim only; named UI relations do not grade RGB pixels,
precision, signal, serialization or scheduling. All actual outcomes are null/U.

All79 prior packet files, sources, seals, reports and archives remain exact in
place. [Consumer history](../../analysis/ableton-live-12.4.3/full-spec-v1/mpe-tuning-grooves/mpe-consumer-impact-r3.json)
retains qualified old-hash occurrences as-of, without consumer mutation or broad
historical replay/adapters. Only this MPE page and shared research routing advance;
Groove/Tuning canonicals and their catalogs remain unchanged. The current
[MPE R3 seal](../../analysis/ableton-live-12.4.3/full-spec-v1/mpe-tuning-grooves/mpe-manifest-author-r3.json)
freezes this partial increment. **AS-OF AUTHOR FREEZE:** independent owner review
is pending; current disposition belongs to the [spec index](index.md). No release,
coverage completion, original/native/vendor/UI/Max/API/runtime/hardware/network/
installation, source capture or candidate operation occurred.
