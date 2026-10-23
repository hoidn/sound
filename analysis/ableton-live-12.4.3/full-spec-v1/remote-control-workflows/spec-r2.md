---
id: SPEC-REMOTE-CONTROL-WORKFLOWS
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 2
target: Ableton Live 12 Suite 12.4.3
---

# Manual MIDI/key mapping and generic control-surface workflows

## Scope and canonical owners

This partial F-08 draft owns documented manual assignment/edit/delete and common
Mapping Browser, generic surface setup, lock entry/status and mapping-context
roles. **D12** means current Version12 prose, not exact12.4.3 evidence. All target
outcomes are null/U/unexecuted. This is not a release or compatibility result.
[Coverage design](../research/full-live-specification-design.md) governs closure;
[research](../research/remote-control-workflows.md) owns interpretation/questions.

[MIDI user mapping](midi-user-mapping.md) revision6 and the immutable
[midi-config-v4 release](../../handoff/midi-config-v4/README.md) retain finite
configuration/tokens/addresses, numeric transforms, takeover/history/precision,
encoder compaction and bank-span laws. No finite law is copied or broadened to
manual MIDI Learn, arbitrary scripts, buttons or a whole host. Existing
REQ-MIDI-USER-007/008 bank contents/host lock effects stay unknown. New lock
affordances and source prose below do not settle those host effects.

[Keyboard/navigation](keyboard-navigation.md) owns global shortcuts, focus,
accessibility and its discovery catalog. Manual key assignment does not imply
global dispatch or Computer MIDI Keyboard notes. [Routing](routing-monitoring-latency.md)
REQ-RML-011/012 owns port/channel and Track/Sync/Remote roles; this page links those
prerequisites. [Racks](device-racks.md) owns Macro assignment/ranges/delegation;
[MPE](mpe-workflows.md) owns expression/zone configuration;
[Max hosting](max-for-live-hosting.md) owns its editor/API scope, without arbitrary
patch or controller compatibility. [Clip View](clip-view-workflows.md) owns panel
selection. [Session View](session-view-workflows.md) owns scene navigation/launch/
cancel; [clip launch](clip-launch.md) and [Session launch](session-launch-workflows.md)
retain their finite laws and runtime unknowns. [Automation](automation-envelopes.md)
retains evaluation and unresolved override/editing; mapped input supplies no new
interpolation or arbitration law. Generic setup closes none of the149 controller
directory profiles or Push-specific protocols.

## Inputs, state and comparison

The [future fixture](../../analysis/ableton-live-12.4.3/full-spec-v1/remote-control-workflows/fixtures.json) requires actual eligible active targets,
usable input/channel/port, known focus/layout/key preferences and independently
working mapped-device response. Audible/feedback/no-effect probes require
nonzero eligible input, active unmuted source/output and paired positive baseline.
The rows/settings/LED are not delivery, protocol, numeric value or audio proof.
No source MIDI/media/hardware is supplied and no Live/native/candidate ran.

All cases have target `expected:null`, `comparison:null`, `target_grade:U`,
`executed:false`. Only named visible control/browser/status proposals have
documentary predicates. Signal, transform, mapping-event, protocol and timing
cases also have null documentary expected/comparator; their `source_claim` is
source context only. No numerical curve, codec, quantization, default, convergence
law, feedback byte, hardware action, timing tolerance or architecture is invented.

## Documentary requirements

### REQ-REMOTE-WORKFLOW-001 — Slot-bound assignments

**D12/target-U.** MIDI and computer-key assignments to Session slots belong to the slot, not the contained clip. Clip launch effects remain with the Session/clip-launch owners; replacement, move and delete identity rules beyond this distinction remain U.

Evidence: `RC-B003` (#midi-and-key-remote-control, HTML280).

### REQ-REMOTE-WORKFLOW-002 — Assigned MIDI notes and track input

**D12/target-U.** The chapter describes a MIDI note assigned to remote control as unavailable for MIDI-track instrument input. This is a documentary exclusivity role, not a general channel/port interception, note-off or MPE dispatch law.

Evidence: `RC-B010` (#midi-remote-control, HTML280), `RC-B011` (#midi-remote-control, HTML280).

### REQ-REMOTE-WORKFLOW-003 — Named surface setup

**D12/target-U.** For a natively supported surface, choose its name in Control Surface settings and choose input/output ports in adjacent columns. The source describes up to six supported surfaces simultaneously; an absent chooser entry leads to manual setup, not proof of incompatibility or any particular profile protocol.

Evidence: `RC-B012` (#midi-remote-control, HTML280), `RC-B014` (#natively-supported-control-surfaces, HTML280), `RC-B015` (#natively-supported-control-surfaces, HTML294), `RC-B025` (#manual-control-surface-setup, HTML334).

### REQ-REMOTE-WORKFLOW-004 — Conditional preset-dump setup

**D12/target-U.** Some surfaces require a preset dump and expose an enabled Dump button for setup. The hardware must first be ready to receive it using its own documented preparation. No universal dump requirement, payload, success detector, timeout or device-state restoration follows.

Evidence: `RC-B016` (#natively-supported-control-surfaces, HTML294).

### REQ-REMOTE-WORKFLOW-005 — Manual override of instant assignments

**D12/target-U.** Manual assignments may override instant mappings, with Remote enabled for the relevant ports. The override scope, conflict arbitration, release/restoration and host effect are not established by this chapter or by the finite configuration release.

Evidence: `RC-B018` (#instant-mappings, HTML294), `RC-B019` (#instant-mappings, HTML294).

### REQ-REMOTE-WORKFLOW-006 — Selection-following instant control

**D12/target-U.** Instant mappings are described as following selected devices. Exact per-surface parameter banks, unsupported devices, selection/focus races and host delivery remain U; this does not complete the existing host/bank unknowns.

Evidence: `RC-B018` (#instant-mappings, HTML294), `RC-B020` (#instant-mappings, HTML294).

### REQ-REMOTE-WORKFLOW-007 — Lock menu and status affordances

**D12/target-U.** For a surface that supports device locking, the device-title context menu Lock to entry enables/disables its lock; the available surface names correspond to configured surfaces, and a hand icon indicates locked status. Some surfaces do not support locking. This clause owns the generic entry/status affordance only.

Evidence: `RC-B021` (#instant-mappings, HTML314), `RC-B022` (#instant-mappings, HTML334), `RC-B023` (#instant-mappings, HTML334).

### REQ-REMOTE-WORKFLOW-008 — Lock focus and arming context

**D12/target-U.** The manual describes supported device locking as retaining access across focus changes and describes a default automatic instrument lock when a MIDI track is armed. These are documentary contexts only: capability, arm-selection interaction, constructor default, bank contents and host lock effects remain U under the existing mapping owner.

Evidence: `RC-B021` (#instant-mappings, HTML314), `RC-B023` (#instant-mappings, HTML334).

### REQ-REMOTE-WORKFLOW-009 — Manual setup entry boundary

**D12/target-U.** An unlisted control surface can be set up for manual mapping through MIDI Ports. This workflow uses the routing owner's Remote input/output roles, rather than redefining Track/Sync/Remote or promising arbitrary hardware support.

Evidence: `RC-B025` (#manual-control-surface-setup, HTML334), `RC-B026` (#manual-control-surface-setup, HTML348).

### REQ-REMOTE-WORKFLOW-010 — Feedback prerequisite

**D12/target-U.** Physical/visual feedback surfaces require the output-port Remote role so value changes can be reflected by faders or LEDs. The general port switch belongs to routing; feedback eligibility, startup state, bytes, loops and physical movement law remain U.

Evidence: `RC-B027` (#manual-control-surface-setup, HTML348).

### REQ-REMOTE-WORKFLOW-011 — Incoming activity indicator

**D12/target-U.** The Control Bar MIDI indicators flash when Live recognizes incoming MIDI. This is an activity indicator role, not proof of a mapping, source identity, output feedback, MIDI-track admission or hardware synchronization.

Evidence: `RC-B028` (#manual-control-surface-setup, HTML348).

### REQ-REMOTE-WORKFLOW-012 — Takeover selection context

**D12/target-U.** The source presents None, Pick-Up and Value Scaling for absolute controls used across destination banks. This clause supplies documentary chooser vocabulary and setup context only; finite transforms, previous-value history, exemptions and precision stay with REQ-MIDI-USER-005/010 and midi-config-v4. Target displayed labels/default remain unproven.

Evidence: `RC-B029` (#manual-control-surface-setup, HTML348), `RC-B031` (#takeover-mode, HTML362), `RC-B032` (#takeover-mode, HTML362), `RC-B033` (#takeover-mode, HTML362), `RC-B034` (#takeover-mode, HTML362).

### REQ-REMOTE-WORKFLOW-013 — Mapping Browser view and columns

**D12/target-U.** The Mapping Browser is shown for the active manual MIDI, key or Macro mapping mode and lists that mode's mappings with control element, parameter path/name and Min/Max. This owns common browser presentation; rack Macro assignment/delegation remains with device-racks.

Evidence: `RC-B036` (#the-mapping-browser, HTML376).

### REQ-REMOTE-WORKFLOW-014 — Range edit and inversion entrypoints

**D12/target-U.** Mapping Browser Min/Max entries can be edited, and a context command inverts them. This is an editing affordance only: accepted domains, parsing, stored representation, target scaling/rounding and resulting values remain with existing finite owners or U.

Evidence: `RC-B036` (#the-mapping-browser, HTML376).

### REQ-REMOTE-WORKFLOW-015 — Delete a selected mapping

**D12/target-U.** The Mapping Browser deletes selected mappings with Backspace on Windows or Delete on Mac. Restoration of target value, control ownership, held-input cleanup and Undo grouping are not specified.

Evidence: `RC-B036` (#the-mapping-browser, HTML376).

### REQ-REMOTE-WORKFLOW-016 — Instant mappings outside the browser

**D12/target-U.** Context-based instant mappings are not listed in the Mapping Browser. Absence from this manual-mapping list does not prove absence of active instant control.

Evidence: `RC-B037` (#the-mapping-browser, HTML376).

### REQ-REMOTE-WORKFLOW-017 — MIDI Map Mode entry and exit

**D12/target-U.** The MIDI switch enters Map Mode, highlighting assignable controls blue and exposing Mapping Browser; the switch exits and hides the browser. Reentering allows review. Ctrl+Alt+B on Windows or Cmd+Option+B on Mac opens a closed Browser in this context; exact geometry/color metrics are not specified.

Evidence: `RC-B039` (#assigning-midi-remote-control, HTML388), `RC-B040` (#assigning-midi-remote-control, HTML388), `RC-B043` (#assigning-midi-remote-control, HTML388).

### REQ-REMOTE-WORKFLOW-018 — Create a manual MIDI assignment

**D12/target-U.** In MIDI Map Mode, select an eligible parameter and send a controller MIDI message; the new assignment is listed in Mapping Browser. Supported message grammar, duplicate/conflict resolution, transaction boundaries and host delivery are not established here.

Evidence: `RC-B039` (#assigning-midi-remote-control, HTML388), `RC-B040` (#assigning-midi-remote-control, HTML388), `RC-B041` (#assigning-midi-remote-control, HTML388), `RC-B042` (#assigning-midi-remote-control, HTML388).

### REQ-REMOTE-WORKFLOW-019 — Note-target roles

**D12/target-U.** The source assigns note gestures to switches/options and describes a single note toggling a variable parameter between endpoints, while a note range supplies discrete spaced values. Session slot input follows its Launch Mode owner. Exact note grammar, toggle dispatch, spacing/interpolation, endpoint codec and timing remain U.

Evidence: `RC-B045` (#mapping-to-midi-notes, HTML388), `RC-B046` (#mapping-to-midi-notes, HTML388), `RC-B047` (#mapping-to-midi-notes, HTML388), `RC-B048` (#mapping-to-midi-notes, HTML388), `RC-B049` (#mapping-to-midi-notes, HTML388).

### REQ-REMOTE-WORKFLOW-020 — Chromatic slot-range assignment gesture

**D12/target-U.** For a chromatic Session-slot note range, the documented assignment gesture holds a root key, then a lower and higher key to define bounds. The root is described as default transposition. Transposition, note allocation, range codec and sound remain U.

Evidence: `RC-B050` (#mapping-to-midi-notes, HTML388).

### REQ-REMOTE-WORKFLOW-021 — Absolute input family boundary

**D12/target-U.** The chapter describes absolute control input, pitch bend and high-resolution absolute input with target-dependent effects. Its numerical threshold/range examples are retained as source context only. The released configuration transforms remain scoped to their stated parameters/assumptions; no manual-Learn, switch, radio or slot law is imported from them.

Evidence: `RC-B052` (#mapping-to-absolute-midi-controllers, HTML388), `RC-B053` (#mapping-to-absolute-midi-controllers, HTML388), `RC-B054` (#mapping-to-absolute-midi-controllers, HTML388), `RC-B055` (#mapping-to-absolute-midi-controllers, HTML388), `RC-B056` (#mapping-to-absolute-midi-controllers, HTML388), `RC-B057` (#mapping-to-absolute-midi-controllers, HTML388).

### REQ-REMOTE-WORKFLOW-022 — Relative-mode detection and selection

**D12/target-U.** The source names Signed Bit, Signed Bit 2, Bin Offset and Twos Complement families plus linear variants. For unsupported-native surfaces it describes detection of type/acceleration, aided by a slow left movement during assignment; a Status Bar mode chooser offers a suggestion and manual selection. Detection success, exact UI list and mapping to configuration tokens remain U.

Evidence: `RC-B059` (#mapping-to-relative-midi-controllers, HTML388), `RC-B060` (#mapping-to-relative-midi-controllers, HTML388), `RC-B061` (#mapping-to-relative-midi-controllers, HTML388), `RC-B062` (#mapping-to-relative-midi-controllers, HTML388), `RC-B068` (#mapping-to-relative-midi-controllers, HTML388).

### REQ-REMOTE-WORKFLOW-023 — Relative target roles

**D12/target-U.** For Session View slots, increment messages are described as treated like Note On and decrement messages like Note Off. Relative increment/decrement gestures are described as switch on/off and option forward/back; continuous interpretation depends on controller type. Exact codecs, steps, acceleration, endpoint/wrap and event dispatch remain U here; existing released relative computations are not broadened.

Evidence: `RC-B063` (#mapping-to-relative-midi-controllers, HTML388), `RC-B064` (#mapping-to-relative-midi-controllers, HTML388), `RC-B065` (#mapping-to-relative-midi-controllers, HTML388), `RC-B066` (#mapping-to-relative-midi-controllers, HTML388), `RC-B067` (#mapping-to-relative-midi-controllers, HTML388).

### REQ-REMOTE-WORKFLOW-024 — Relative Session mapping strip

**D12/target-U.** Both MIDI and Key Map modes expose a strip of assignable controls below the Session grid for relative navigation/launch roles. This is a mapping entrypoint, not a launch/scene scheduling law.

Evidence: `RC-B070` (#relative-session-view-navigation, HTML388), `RC-B071` (#relative-session-view-navigation, HTML388).

### REQ-REMOTE-WORKFLOW-025 — Highlighted-scene navigation assignment

**D12/target-U.** The strip offers up/down highlighted-scene controls assignable to keys/notes/controllers and a scene-number box assignable to a MIDI controller for scrolling. Endpoint/wrap, number encoding, relative decoder and focus precedence remain U.

Evidence: `RC-B072` (#relative-session-view-navigation, HTML406), `RC-B073` (#relative-session-view-navigation, HTML406).

### REQ-REMOTE-WORKFLOW-026 — Highlighted-scene launch and cancel entrypoints

**D12/target-U.** The strip offers launch-highlighted-scene and cancel-triggered-scene assignment targets. Scene launch/cancel behavior and Select Next Scene on Launch stay with REQ-SESSION-VIEW-010/011; this clause adds only mapped entrypoints.

Evidence: `RC-B074` (#relative-session-view-navigation, HTML406), `RC-B075` (#relative-session-view-navigation, HTML406).

### REQ-REMOTE-WORKFLOW-027 — Per-track highlighted-row clip launch target

**D12/target-U.** The strip supplies per-track assignable controls to launch the clip at the highlighted scene. This is a target-entrypoint role only; empty-slot recording/stop, clip launch timing and playing/selection changes remain with existing owners or U.

Evidence: `RC-B076` (#relative-session-view-navigation, HTML406).

### REQ-REMOTE-WORKFLOW-028 — Highlighted-scene viewport role

**D12/target-U.** Relative Session mapping is described as keeping the highlighted scene centered in Session View. No pixel metric, edge-of-list padding, hidden-row or resizing policy is established.

Evidence: `RC-B077` (#relative-session-view-navigation, HTML406).

### REQ-REMOTE-WORKFLOW-029 — Clip View mapping follows selection context

**D12/target-U.** Mappings created for Clip View controls can affect different selected clips, including multi-selection; the manual recommends relative controls to avoid value jumps. Shared panel/selection UI stays with Clip View. This is not a numerical smoothing guarantee, target identity formula or general multi-edit transaction law.

Evidence: `RC-B079` (#mapping-to-clip-view-controls, HTML406).

### REQ-REMOTE-WORKFLOW-030 — Key Map Mode entry and exit

**D12/target-U.** The KEY switch enters Key Map Mode with red-highlighted assignable controls and Mapping Browser; the View menu can show a hidden Browser. Exiting hides Mapping Browser, and reentering allows review. This does not define global shortcut or Computer MIDI Keyboard dispatch.

Evidence: `RC-B081` (#computer-keyboard-remote-control, HTML418), `RC-B082` (#computer-keyboard-remote-control, HTML418), `RC-B085` (#computer-keyboard-remote-control, HTML418).

### REQ-REMOTE-WORKFLOW-031 — Create a computer-key assignment

**D12/target-U.** In Key Map Mode select a red-highlighted eligible control and press a computer key; Mapping Browser displays the new assignment. Only highlighted controls are offered for mapping; duplicate keys, reserved chords, layouts and text-focus interception remain U.

Evidence: `RC-B083` (#computer-keyboard-remote-control, HTML418), `RC-B084` (#computer-keyboard-remote-control, HTML418).

### REQ-REMOTE-WORKFLOW-032 — Computer-key target roles

**D12/target-U.** Mapped computer keys are described as operating slot clips according to Launch Mode, toggling switches and cycling option buttons. This is manual key mapping, distinct from Computer MIDI Keyboard note generation; global shortcuts, key-repeat, held releases and precedence remain U.

Evidence: `RC-B086` (#computer-keyboard-remote-control, HTML418), `RC-B087` (#computer-keyboard-remote-control, HTML418), `RC-B088` (#computer-keyboard-remote-control, HTML418), `RC-B089` (#computer-keyboard-remote-control, HTML418), `RC-B090` (#computer-keyboard-remote-control, HTML418).

### REQ-REMOTE-WORKFLOW-U-CONTEXT — Key and focus arbitration

**U/target-U.** Layout/IME, Computer MIDI Keyboard, global shortcuts, text/modal/plugin focus, navigation preferences, repeats and duplicate input-source precedence remain unknown.

### REQ-REMOTE-WORKFLOW-U-NUMERICAL — Manual mapping numerical and protocol outcomes

**U/target-U.** Manual MIDI Learn admission, message bytes, relative detection/codecs, scales, display curves, thresholds, takeover application, feedback and sample/event timing remain unknown beyond separately released finite clauses.

### REQ-REMOTE-WORKFLOW-U-PROFILES — Per-profile and host behavior

**U/target-U.** Generic setup does not specify the 149 inventoried controller directories, Push generations, arbitrary scripts, user-profile discovery/reload, exact device bank contents, host lock/arm effects or preset-dump protocols.

### REQ-REMOTE-WORKFLOW-U-BOUNDARIES — Assignment domains and malformed controls

**U/target-U.** Invalid/unsupported controls/messages/ranges, empty or deleted targets, range gestures, exhausted surface rows, and cancellation commit points lack output oracles.

### REQ-REMOTE-WORKFLOW-U-LIFECYCLE — Persistence, undo, automation and teardown

**U/target-U.** Set/global ownership, save/reopen/migration, undo grouping, automation override, source loss/reconnection, reset history and cleanup during held input/device deletion remain required unknowns.

## Finite acceptance proposals and unknowns

[47 cases](../../analysis/ableton-live-12.4.3/full-spec-v1/remote-control-workflows/cases.json) cover 32 D12 roles and5 U requirements.
Compound clauses remain partial until each branch, applicable platform/controller
and lifecycle kind closes. Unknown categories include context/conflicts, numeric/
feedback/timing, per-profile/dump, boundary/malformed/cancel, persistence/undo/
automation/loss/teardown. Missing controls or actual dialog availability remains U.

| Case | Requirement | Kind / finite action |
| --- | --- | --- |
| RC-001 | REQ-REMOTE-WORKFLOW-001 | mapping-effect: Use two populated slots A/B with distinct active clips and a confirmed mapped A baseline. Replace only A content on an owned copy, then move a clip separately; retain slot, clip, assignment and playing identities. No launch or remapping identity oracle is supplied. |
| RC-002 | REQ-REMOTE-WORKFLOW-002 | signal: Confirm a valid note produces nonzero output on a known armed/monitored instrument and separate remote target. Assign that note to a slot, retain exact input port/channel and independently observed events, then compare an unassigned neighboring note. Do not infer a MIDI byte/filter law. |
| RC-003 | REQ-REMOTE-WORKFLOW-003 | control: With an independently identified supported surface and available ports, inspect its named row and input/output choices. Compare a separate unlisted controller through manual setup. Inspect offered rows; a seventh-device result is U. |
| RC-004 | REQ-REMOTE-WORKFLOW-004 | protocol: Retain an independently supported surface setup and manufacturer readiness procedure. Inspect whether Dump is offered/enabled and compare a known no-dump setup. Any future actual dump requires separately authorized hardware context; payload and setup outcome remain U. |
| RC-005 | REQ-REMOTE-WORKFLOW-005 | mapping-effect: Establish a positive instant-controlled parameter on device A, then create one manual mapping for that physical control to distinct eligible B. Retain Remote/focus/selection and compare deletion in a reset copy. No winner, timing or restored-route oracle is assigned. |
| RC-006 | REQ-REMOTE-WORKFLOW-006 | mapping-effect: Use a known supported instant surface and two independently responsive unlocked devices A/B with distinct controls. Select A then B while retaining actual bank/target state; separately change view focus without selecting another device. Host target/value results stay U. |
| RC-007 | REQ-REMOTE-WORKFLOW-007 | control: With independently confirmed lock-capable surface S, inspect device A context menu, select S and inspect hand status; revisit the same entry to unlock. Compare an independently known unsupported surface without presuming its menu presentation. |
| RC-008 | REQ-REMOTE-WORKFLOW-008 | mapping-effect: With lock-capable S and independently responsive instruments A/B, explicitly lock A, select B and vary focus. In separate reset fresh/loaded copies arm A with lock state retained. Record actual control destinations without assuming default lock or resolving host semantics. |
| RC-009 | REQ-REMOTE-WORKFLOW-009 | control: Identify an available input from an unlisted owned controller, inspect MIDI Ports and explicitly enable the routing owner's Remote input role. Keep Track/Sync settings declared; verify usable input separately before attempting an assignment. |
| RC-010 | REQ-REMOTE-WORKFLOW-010 | signal: Use an independently working feedback surface, selected output and active mapped target; retain a positive feedback baseline. Disable only output Remote in a reset trial, preserving input and value changes. No feedback bytes, motor deadline or silence criterion is supplied. |
| RC-011 | REQ-REMOTE-WORKFLOW-011 | control: Retain independently identified usable controller traffic and inspect incoming activity, then separately send an unmapped eligible control. Keep mapped-target response and track input observations independent of indicator status. |
| RC-012 | REQ-REMOTE-WORKFLOW-012 | control: Inspect the offered takeover choices and record the explicitly selected choice. Use two known destination banks and nonmatching physical/current parameter positions only for separately ungraded value trials; do not assume a default or test a new convergence formula. |
| RC-013 | REQ-REMOTE-WORKFLOW-013 | control: Prepare distinct manual MIDI and key mappings and a separately owned rack Macro map. Enter each mode individually and inspect visible rows/columns; compare their target identities and return to normal view. Macro assignment behavior is not retested here. |
| RC-014 | REQ-REMOTE-WORKFLOW-014 | control: Select a known manual mapping with two independently accepted unequal endpoints; edit each endpoint and invoke the inversion command. Retain displayed before/after entries without assigning a numerical target or exact serialization oracle. |
| RC-015 | REQ-REMOTE-WORKFLOW-015 | control: Create two distinct confirmed browser mappings A/B; select only A row, invoke the platform deletion key, and inspect remaining rows. Test target input, undo and held-note effects separately as U; do not delete source media or devices. |
| RC-016 | REQ-REMOTE-WORKFLOW-016 | control: Establish positive instant control with no manual assignments, open MIDI Map Mode and inspect browser; then create one independent manual row. Retain positive device response separately from list membership. |
| RC-017 | REQ-REMOTE-WORKFLOW-017 | control: In the main window outside text/modal/plugin focus, enter MIDI Map Mode, inspect eligible highlights/browser, close and reopen Browser with the platform chord, then exit and reenter. Retain key/navigation preferences and active view. |
| RC-018 | REQ-REMOTE-WORKFLOW-018 | control: With active Remote input, known channel and independently received eligible control, select one highlighted unassigned target and send that input. Inspect new row/control/target identity and reenter for review; compare a different unassigned target in a reset copy. |
| RC-019 | REQ-REMOTE-WORKFLOW-019 | mapping-effect: In separate mappings use a known eligible note for an activator, finite option selector and variable control with accepted endpoints, then a known supported note range. Retain actual message/channel identity and active baseline; launch mode is declared separately and no value equation is graded. |
| RC-020 | REQ-REMOTE-WORKFLOW-020 | control: With a populated audible slot selected in MIDI Map Mode, use three independently identified distinct supported notes in root/lower/upper order with root held. Retain created mapping fields; compare release/order/boundary variants only as unknown probes, without pitch-output criteria. |
| RC-021 | REQ-REMOTE-WORKFLOW-021 | transform: Use independently supported absolute CC, pitch-bend and high-resolution input in separate fresh mappings to an active eligible target. Retain actual offered mode and raw source identity. Do not infer half-pairing, switch threshold, radio quantization or fader/gain law from prose. |
| RC-022 | REQ-REMOTE-WORKFLOW-022 | control: With an independently known relative encoder family and eligible active target, assign using slow left movement, record the suggested and offered modes, and select the known offered type manually. Repeat one other family separately; no classifier success or byte-decoder oracle is assigned. |
| RC-023 | REQ-REMOTE-WORKFLOW-023 | transform: Use a positively identified relative encoder and separately eligible slot, switch, option and continuous targets. Establish active responses, send each declared direction separately, and retain offered mode, endpoints and launch mode. No arbitrary raw value or exact step is predicted. |
| RC-024 | REQ-REMOTE-WORKFLOW-024 | control: Use Session with populated A/B/C scenes and distinct tracks. Enter MIDI then Key Map Mode separately, inspect the assignable strip, and exit each. Grid/focus/selection rendering remains with Session View. |
| RC-025 | REQ-REMOTE-WORKFLOW-025 | mapping-effect: Map separate eligible up/down controls and a known encoder to the scene box; start at middle populated scene B among A/B/C and retain highlight, focus and mapped input before each direction. Probe first/last and empty scenes separately as U. |
| RC-026 | REQ-REMOTE-WORKFLOW-026 | control: In Map Mode inspect and separately assign highlighted-scene launch/cancel targets using distinct controls. Declare Select Next Scene on Launch and selected scene. Future cancel trials require independently confirmed pending state under the existing scene owner, with timing ungraded. |
| RC-027 | REQ-REMOTE-WORKFLOW-027 | control: Use two active tracks with distinct populated clips in highlighted scene B, inspect corresponding assignable strip controls and create distinct mappings. Retain track/slot/scene identities; empty and armed-slot effects remain unknown. |
| RC-028 | REQ-REMOTE-WORKFLOW-028 | control: Use enough owned scenes to scroll, map valid navigation and begin at an interior scene; inspect highlighted-row viewport placement after two separate moves. First/last scene and resize behavior remain U, with no pixel tolerance. |
| RC-029 | REQ-REMOTE-WORKFLOW-029 | mapping-effect: Use two independently active clips with the same eligible Clip View control but distinct current values. Map once, select A then B and then both in reset trials; retain selected identities and actual mapping. Do not assume clip-specific binding or target value continuity. |
| RC-030 | REQ-REMOTE-WORKFLOW-030 | control: With main window focus and explicit keyboard layout, Computer MIDI Keyboard and navigation preferences, enter KEY mode, inspect eligible highlights/browser, show hidden Browser via View menu, exit and reenter. Keep text/modal/plugin focus out of the positive trial. |
| RC-031 | REQ-REMOTE-WORKFLOW-031 | control: In KEY mode choose one red-highlighted unassigned target and a known otherwise unused key under retained layout/focus/preferences. Inspect the new row and target identity; separately inspect a nonhighlighted control without presuming a click/error result. |
| RC-032 | REQ-REMOTE-WORKFLOW-032 | mapping-effect: Use separate known unused mapped keys for an active slot, switch and finite option selector, with actual focus/layout/Computer MIDI Keyboard state declared. Retain down/up/repeat and compare an unmapped key. Launch and input arbitration outputs stay ungraded. |
| RC-U-KEY-CONTEXT | REQ-REMOTE-WORKFLOW-U-CONTEXT | context: Repeat a positively mapped key with Computer MIDI Keyboard on/off, declared Tab/navigation settings, text edit, modal and plugin focus, then a second layout/IME in separate owned trials. |
| RC-U-DUPLICATE | REQ-REMOTE-WORKFLOW-U-CONTEXT | conflict: After one working manual mapping add duplicate key or MIDI address, competing instant mapping and two input ports/channels separately; retain actual accepted assignments and input order. |
| RC-U-NUMERIC | REQ-REMOTE-WORKFLOW-U-NUMERICAL | transform: For known eligible active targets retain accepted Min/Max, current value, actual mode and raw input; compare equal/reversed endpoints, stepped targets, takeover after bank change and first high-resolution input without a new numeric oracle. |
| RC-U-FEEDBACK | REQ-REMOTE-WORKFLOW-U-NUMERICAL | signal: With positive feedback and nonzero mapped target path retain actual outbound messages and hardware state through bank/focus changes, disabled output and reconnect; do not infer bytes or motor/LED timing. |
| RC-U-TIMING | REQ-REMOTE-WORKFLOW-U-NUMERICAL | timing: Retain actual input timestamps and active target/source across transport stopped/running, tempo changes and accepted sample rates/block sizes. No cadence, debounce, latency, key-repeat or rate-equivalence criterion exists. |
| RC-U-PROFILE | REQ-REMOTE-WORKFLOW-U-PROFILES | profile: Select one independently identified profile/build and available supported device; retain offered banks, lock capability, host target identities and required hardware setup. Other profiles remain individually untested. |
| RC-U-DUMP | REQ-REMOTE-WORKFLOW-U-PROFILES | protocol: For separately authorized future hardware work only, retain known readiness and active baseline, then explore unavailable/failed/interrupted dump and recovery. This packet authorizes and executes no dump. |
| RC-U-BOUNDARY | REQ-REMOTE-WORKFLOW-U-BOUNDARIES | boundary: After positive active mappings inspect first/last/empty scenes, nonhighlighted targets, zero/equal/reversed/offered-boundary ranges, note-range order and sixth/seventh surface rows. Record offered bounds rather than inventing clamp/reject. |
| RC-U-MALFORMED | REQ-REMOTE-WORKFLOW-U-BOUNDARIES | malformed: In disposable owned settings enter invalid/nonfinite range text and unsupported/partial MIDI input separately after accepted baseline; retain errors and resulting mappings without assuming accepted grammar. |
| RC-U-CANCEL | REQ-REMOTE-WORKFLOW-U-BOUNDARIES | cancellation: Begin mapping/range or offered surface settings operation, cancel with available Escape/dialog control before and after independently observed commit in separate copies; do not assume rollback. |
| RC-U-PERSISTENCE | REQ-REMOTE-WORKFLOW-U-LIFECYCLE | persistence: Save/reopen an owned Set and separately restart with explicit mappings, ranges, relative modes, takeover and locked surface; import an owned clip/device/rack into another Set and retain mapping/identity/settings ownership. |
| RC-U-UNDO | REQ-REMOTE-WORKFLOW-U-LIFECYCLE | undo-redo: Create/edit/delete one mapping and change a surface lock/range, then request Undo/Redo only where available; retain browser rows, target value and settings separately. |
| RC-U-AUTOMATION | REQ-REMOTE-WORKFLOW-U-LIFECYCLE | automation: With known eligible automated target and active mapped input, vary manual/mapped control, clip/Arrangement envelope and re-enable in separate reset trials; no override arbitration or interpolation rule follows. |
| RC-U-LOSS | REQ-REMOTE-WORKFLOW-U-LIFECYCLE | source-loss: After usable mapped input and feedback disconnect only selected controller/input/output, reconnect and change port identity separately; retain held inputs, mapping rows and physical/target states. |
| RC-U-TEARDOWN | REQ-REMOTE-WORKFLOW-U-LIFECYCLE | teardown: With active mapped target and held note/key or pending feedback, delete target/device/track, close Set, remove surface and close app in separate future trials. Stuck-note prevention, reset history and resource cleanup remain U. |

## Analysis-only evidence and freeze

Official [Version12 MIDI and Key Remote Control](https://www.ableton.com/en/live-manual/12/midi-and-key-remote-control/),
captured 2026-10-19T21:57:26.580620+00:00, 264686bytes,
SHA-256 `63dfe96294283a8f5d1bb0876dad48c29a9173a82fe81cfa1ce74ac24726b523`. [Retained HTML](../../analysis/ableton-live-12.4.3/full-spec-v1/remote-control-workflows/manual-midi-key-remote-2026-10-19.html)
and [90 exact text blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/remote-control-workflows/source-blocks.json) preserve anchors/HTML lines;
figures were not separately inspected. Current web documentation has no immutable
12.4.3 publication identity. Numerical threshold examples and lock-on-arm default
wording are context, not a new released oracle. [Requirements](../../analysis/ableton-live-12.4.3/full-spec-v1/remote-control-workflows/requirements.json),
[counts](../../analysis/ableton-live-12.4.3/full-spec-v1/remote-control-workflows/counts.json), [owner pins](../../analysis/ableton-live-12.4.3/full-spec-v1/remote-control-workflows/owner-pins.json) and
[manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/remote-control-workflows/manifest-author-r2.json) freeze the partial review packet.
