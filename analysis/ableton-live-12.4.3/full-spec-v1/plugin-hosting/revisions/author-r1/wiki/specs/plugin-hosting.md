---
id: SPEC-PLUGIN-HOSTING
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3
---

# Plug-in hosting workflows

## Scope and authority

This partial analyst contract owns third-party plug-in placement, parameter-panel
configuration, editors, selected sidechain and program workflows. It complements
[discovery](plugin-discovery.md), [racks/common device actions](device-racks.md)
and [bundled-device hosting](bundled-device-hosting.md). Scanner isolation is not
instantiation isolation. Engine compensation/routing and full plug-in API behavior
remain separate obligations; no API/callback architecture is prescribed.

D12 means a predicate supported by captured Version 12 documentation; its
applicability to exact 12.4.3 is unknown throughout. No original or candidate
application, plug-in, editor or codec was executed. No fixture binary is supplied.
Presence or format support is not proof of arbitrary vendor compatibility.
Sources and limitations belong to [the research owner](../research/plugin-hosting.md).

## Inputs, state and observable outcomes

Inputs are format/role/capabilities, track placement, published parameter identity,
panel and editor state, window preferences, mappings/envelopes, program selection,
files and routing. Observe panel membership/order, warnings, editor visibility and
parameter state, Set-restored configuration and file-dialog operation. Do not
substitute internal callback logs for an app-observable requirement. Discrete
membership/order predicates have no numerical tolerance; all audio/timing/rounding
oracles remain U unless explicitly retained from a later evidence packet.

## Requirements

### REQ-PLUGIN-HOSTING-001 — Placement and formats

**D12; exact-build U.** VST2/VST3 and macOS AU2/AU3 are documented formats. Instruments accept MIDI and output audio on MIDI tracks; effects belong on audio tracks or after instruments. Format availability does not prove any particular plug-in compatible. [Source using-plug-ins](#source-using-plug-ins).

### REQ-PLUGIN-HOSTING-002 — Initial parameter panel

**D12; exact-build U.** For an unconfigured instance with no overriding default, a plug-in with at most 64 modifiable parameters exposes them in the Live panel; above 64 the initial panel is empty. Parameter enumeration/filtering and hidden/read-only parameter counting remain U. [Source plug-ins-in-the-device-view](#source-plug-ins-in-the-device-view).

### REQ-PLUGIN-HOSTING-003 — Panel visibility and X-Y assignments

**D12; exact-build U.** The title-bar unfold control shows/hides the panel. Two choosers assign parameters to the X-Y field. Numeric X-Y interpolation, automation and coupled parameter writes remain U. [Source plug-ins-in-the-device-view](#source-plug-ins-in-the-device-view).

### REQ-PLUGIN-HOSTING-004 — Floating editor correspondence

**D12; exact-build U.** Show/Hide Plug-In Window opens the original plug-in editor; an exposed parameter can be changed from either editor or Live panel with the same parameter effect. Update timing/rounding/threading and unsupported editors remain U. [Source showing-plug-in-panels-in-separate-windows](#source-showing-plug-in-panels-in-separate-windows).

### REQ-PLUGIN-HOSTING-005 — Window preferences

**D12; exact-build U.** Auto-Open opens editors for browser-loaded devices. Multiple Plug-In Windows allows concurrent editors; with it off, Ctrl on Windows or Cmd on Mac while opening preserves previous windows. Auto-Hide limits displayed editors to the selected track. Option interactions and restoration order remain U. [Source showing-plug-in-panels-in-separate-windows](#source-showing-plug-in-panels-in-separate-windows).

### REQ-PLUGIN-HOSTING-006 — Global editor visibility

**D12; exact-build U.** The View command or Ctrl-Alt-P on Windows / Cmd-Option-P on Mac toggles already-open editors; the shortcut requires prior manual opening or Auto-Open enabled. A visible editor title identifies its track. Exact geometry, focus, resize and accessibility remain U. [Source showing-plug-in-panels-in-separate-windows](#source-showing-plug-in-panels-in-separate-windows).

### REQ-PLUGIN-HOSTING-007 — Configure admission

**D12; exact-build U.** Configure adds published parameters by clicking them in the original editor, with an actual value change required by some plug-ins. Unpublished parameters cannot be added. A click-only failure is not a host failure unless that plug-in publishes by click. [Source plug-in-configure-mode](#source-plug-in-configure-mode).

### REQ-PLUGIN-HOSTING-008 — Configure reorder and deletion warning

**D12; exact-build U.** In Configure, displayed parameters can be reordered by drag and removed with Delete. Existing automation, clip envelopes, MIDI/key/Macro mappings trigger a warning before deletion. Warning choices, cancellation side effects and data survival after confirmation remain U. [Source plug-in-configure-mode](#source-plug-in-configure-mode).

### REQ-PLUGIN-HOSTING-009 — Instances and persistence

**D12; exact-build U.** Configured parameter lists belong to individual instances and are saved in the Set. A configured device can be retained in a saved rack or configuration default. Plug-in DSP state, missing binaries, default precedence and exact saved representation remain U; generic rack/default actions route to SPEC-DEVICE-RACKS. [Source plug-in-configure-mode](#source-plug-in-configure-mode).

### REQ-PLUGIN-HOSTING-010 — Editorless plug-ins

**D12; exact-build U.** For a plug-in without its own window, Configure permits reordering but not deleting its Live-panel parameters. Editor creation/teardown failure is a separate U condition. [Source plug-in-configure-mode](#source-plug-in-configure-mode).

### REQ-PLUGIN-HOSTING-011 — Temporary parameter entries

**D12; exact-build U.** Changing a parameter in the floating editor creates temporary automation/clip-envelope/X-Y chooser entries, removed when another parameter is adjusted. Editing its envelope, selecting another parameter in the envelope chooser, or selecting it in an X-Y chooser makes the entry permanent. Duplicate handling, visibility order and interrupted changes remain U. [Source plug-in-configure-mode](#source-plug-in-configure-mode).

### REQ-PLUGIN-HOSTING-012 — Recording and mapping additions

**D12; exact-build U.** Changing editor parameters during recording records automation and adds the automated parameters to the panel when recording stops. In MIDI/key/Macro mapping mode, adjusting an editor parameter creates and selects its panel entry. Recording prerequisites, envelope values and mapping transforms remain with their canonical owners or U. [Source plug-in-configure-mode](#source-plug-in-configure-mode).

### REQ-PLUGIN-HOSTING-013 — Sidechain source and endpoints

**D12; exact-build U.** A supporting plug-in can choose an internal routing point as trigger. Gain affects this trigger, not source mix volume; Mix=100% uses only the sidechain and Mix=0% bypasses the sidechain trigger. Intermediate mixing law, channel conversion, latency and plug-in response remain U. [Source sidechain-parameters](#source-sidechain-parameters).

### REQ-PLUGIN-HOSTING-014 — Sidechain Mute control

**D12; exact-build U.** The documented Mute permits auditioning the plug-in output while bypassing the sidechain source input. The exact affected routing branch and interactions with independent source monitoring/sends remain U; no global track-mute law is inferred. [Source sidechain-parameters](#source-sidechain-parameters).

### REQ-PLUGIN-HOSTING-015 — VST programs and files

**D12; exact-build U.** The selected VST program belongs to its instance; edits affect that program. The chooser selects programs; Rename Plug-In Preset renames the current one. Load accepts a program or bank; Save can target the current program or bank via the format choice. VST2/VST3 per-format applicability, binary formats and failure/atomicity remain U. [Source vst-presets-and-banks](#source-vst-presets-and-banks).

### REQ-PLUGIN-HOSTING-016 — Audio Units distinctions

**D12; exact-build U.** AU is macOS-only. Some modes are accessible only through the original editor. Some AU presets are read-only and cannot be dragged elsewhere; documented preset storage is under the user Library Audio/Presets manufacturer/plug-in path. Actual extension spelling/encoding, AU2/AU3 differences and exact permissions/failure results remain U. [Source audio-units-plug-ins](#source-audio-units-plug-ins).

### REQ-PLUGIN-HOSTING-017 — Processing and timing

**U; exact-build U.** No host processing-block, MIDI/event schedule, automation delivery, channel layout, latency notification, bypass/tail, render or dropout oracle is established here. Discovery/placement/UI presence does not prove processing compatibility. [Source plug-in-configure-mode](#source-plug-in-configure-mode).

### REQ-PLUGIN-HOSTING-018 — Opaque state and identity

**U; exact-build U.** State restore, vendor version/format substitution, duplicate identifiers, missing/disabled plug-ins, reopening and unavailable plug-in recovery remain unknown beyond the configured-panel documentary clause. [Source plug-in-configure-mode](#source-plug-in-configure-mode).

### REQ-PLUGIN-HOSTING-019 — Malformed data and faults

**U; exact-build U.** Malformed program/bank/state, instantiation failure, editor crash/hang and invalid plug-in responses have no established application outcome. Scanner fault behavior remains owned by SPEC-PLUGIN-DISCOVERY and is not imported as instantiation isolation. [Source vst-presets-and-banks](#source-vst-presets-and-banks).

### REQ-PLUGIN-HOSTING-020 — Cancel undo and teardown

**U; exact-build U.** Cancel of configuration warnings or file dialogs, undo/redo of parameter-list/device operations and removal/Set-close with editors, automation or active notes remain unknown. No leak/crash/focus/tail criterion is invented. [Source plug-in-configure-mode](#source-plug-in-configure-mode).

### REQ-PLUGIN-HOSTING-021 — Multi-I/O and remote control integration

**D12; exact-build U.** Panel parameters can be MIDI-mapped; continuous parameters accept clip envelopes; supporting plug-ins can participate in track I/O routing and accept custom info text. Exact port selection, event routing, envelope laws and text persistence remain with existing owners or U. [Source plug-in-configure-mode](#source-plug-in-configure-mode).

## Acceptance fixtures and cases

[Fixture definitions](../../analysis/ableton-live-12.4.3/full-spec-v1/plugin-hosting/fixtures.json)
require independent capability verification. An unavailable prerequisite leaves
a case unexecuted, never passing. Known-good means independently established
input/vendor behavior, not behavior inferred from the candidate being tested.

All 40 [case definitions](../../analysis/ableton-live-12.4.3/full-spec-v1/plugin-hosting/cases.json)
remain unexecuted for target compatibility. D12 predicates are scoped documentary
expectations only; U probes have null oracles. No binary fixtures were created.

| Case | Requirement suffix | Kind | Setup / action | Predicate or unknown |
| --- | --- | --- | --- | --- |
| PH-001 | 001 | positive | F1: insert instrument on a MIDI track and effect after it; insert effect on an audio track | Check the documented input/output roles and permitted positions; no audio equation |
| PH-002 | 001 | negative | F1: attempt instrument placement after an audio-only source and effect before an instrument on a bare MIDI chain | Only documented placement eligibility is asserted; resulting relocation/rejection UI is U |
| PH-003 | 002 | boundary | F2: fresh known-published 64-parameter instance, no configuration default | All 64 modifiable parameters appear in the panel |
| PH-004 | 002 | boundary | F2: separate fresh 65-parameter instance under same default-free conditions | Initial parameter panel is empty; editor availability is separate |
| PH-005 | 003 | positive | F2: unfold then fold the panel and select distinct parameters P1/P2 in X/Y choosers | Visibility follows unfold state; chosen assignments identify P1/P2; numerical response U |
| PH-006 | 004 | positive | F2: editor and panel expose P1; make one discrete value change in each direction | Corresponding exposed parameter effect matches; latency/rounding metric U |
| PH-007 | 005 | positive | F3: enable Auto-Open then load editor-capable device from browser | Editor opens on load |
| PH-008 | 005 | positive | F3: Multiple Windows off, open editor A then modifier-open editor B | A remains open alongside B |
| PH-009 | 005 | positive | F3: Multiple Windows on, open A and B; enable Auto-Hide and select their tracks in turn | Concurrent editors are permitted; displayed editors belong to selected track under Auto-Hide |
| PH-010 | 006 | positive | F3: open A manually, invoke global visibility command twice | Already-open editor hides and shows; visible title identifies its owning track |
| PH-011 | 006 | negative | F3: fresh instance never manually opened, Auto-Open off; invoke editor visibility shortcut | Shortcut does not establish an initial editor opening; other state changes U |
| PH-012 | 007 | positive | F2: enter Configure, adjust a published editor parameter known to publish on change | Parameter is added to Live panel |
| PH-013 | 007 | negative | F2: edit a parameter independently known not to be published | That unpublished parameter cannot be added to Live panel |
| PH-014 | 008 | positive | F2: Configure panel [P1,P2,P3], drag P3 before P1 | Relative configured order becomes [P3,P1,P2] |
| PH-015 | 008 | positive | F2: add known automation to P1, select P1 in Configure, press Delete | Warning occurs before removal; no implicit confirmation outcome |
| PH-016 | 008 | positive | F2: repeat warning fixture separately for clip envelope and each MIDI/key/Macro mapping | Each applicable existing association warns before removal |
| PH-017 | 009 | persistence | F2: two same-type instances A/B, configure only A; save and reopen Set in same working environment | A configuration survives and B remains independently configured; opaque plug-in state equality U |
| PH-018 | 010 | negative | F4: editorless instance, try Delete on a configured parameter then reorder two entries | Deletion is unavailable; reordering is permitted |
| PH-019 | 011 | positive | F2: outside Configure, adjust P1 then P2 in floating editor without envelope editing | Temporary chooser entry follows current parameter; P1 temporary entry is removed on P2 adjustment |
| PH-020 | 011 | positive | F2: adjust P1 then select P1 in X-Y chooser, later adjust P2 | P1 becomes permanent in the panel rather than disappearing with the next adjustment |
| PH-021 | 011 | positive | F2: adjust P1 then edit its automation envelope before adjusting P2; repeat with clip envelope | Edited parameter becomes permanent; numerical envelope behavior U |
| PH-022 | 011 | positive | F2: temporary P1, select another parameter in automation chooser; repeat in clip-envelope chooser | P1 becomes permanent by documented promotion path |
| PH-023 | 012 | positive | F2: establish recording prerequisites via recording/automation owners; adjust published P1 in editor, stop recording | Automation is recorded and P1 is added to the panel after stop; values/timing U |
| PH-024 | 012 | positive | F2: separately enter MIDI, key and Macro mapping modes; adjust a published P1 in editor | Entry is created and selected for mapping in each applicable mode; mapping arithmetic U |
| PH-025 | 013 | boundary | F5: supporting plug-in, independent sidechain/source fixtures; Mix=0 then100 | Endpoint trigger sources follow the documented roles; quantitative output response U |
| PH-026 | 013 | positive | F5: increase external-sidechain Gain while separately monitoring a fixed-level source mix | Gain affects trigger path; source mix level is not increased by that control; finite tolerance U |
| PH-027 | 014 | interaction | F5: source reaches plug-in sidechain and independent track/sends; toggle sidechain Mute | U: affected branch identity and output/source audition matrix need evidence; not graded |
| PH-028 | 015 | positive | F6: choose program B then rename it via Rename Plug-In Preset; inspect separate instance A | Program chooser/name reflect selected instance operation; vendor program side effects and cross-instance equivalence U |
| PH-029 | 015 | positive | F6: Save Preset versus Save Bank using explicit dialog format; load each into compatible same-format instance | Program-versus-bank operation selected; exact bytes and per-format applicability U |
| PH-030 | 016 | negative | F7: independently identified read-only AU preset, attempt browser drag | Preset cannot be relocated by that drag; warning/error/permissions U |
| PH-031 | 016 | positive | F7: AU with known mode available only in original editor; open editor | Mode is accessible there; Live-panel exposure is not required by this clause |
| PH-032 | 017 | timing | F1: process note/controller/automation changes at block boundaries with changing rate/buffer and reported latency | U: sample/event order, compensation, ramp, tail and performance oracles absent |
| PH-033 | 018 | persistence | F6: save opaque vendor state, remove binary or substitute vendor version/format and reopen copy of Set | U: identity resolution, fallback, warning and restoration behavior absent |
| PH-034 | 019 | malformed | F6: separately load truncated/wrong-format program, bank and state; record result on copied Set | U: no refusal/repair/partial-load/dialog/rollback oracle |
| PH-035 | 019 | error | F1: independently controlled instantiation/editor fault or hang, without invoking discovery scanner | U: isolation, recovery, timeout and retained-state outcomes absent |
| PH-036 | 020 | cancel | F2: cancel associated-parameter Delete warning and separately cancel program file dialogs | U: selection/list/associations/files/dirty-state effects absent |
| PH-037 | 020 | undo | F2: configure/reorder/remove parameter, then undo/redo; separately device insert/delete | U: history grouping, mapping survival and restored state absent |
| PH-038 | 020 | teardown | F1/F3: active notes and open editors, remove device then close Set/application | U: note-offs, tails, editor resources/focus, saves and shutdown outcome absent |
| PH-039 | 021 | positive | F2: panel P1 in MIDI mapping, then continuous P1 in clip-envelope chooser; set custom info text | Documented eligibility and text entry only; transformation/retention U |
| PH-040 | 021 | interaction | F8: supporting multi-I/O instrument/effect, enumerate and select available source/target routing entries | Routing participation is documented; port counts, exact identities and signal semantics U |

## Open obligations and interactions

Every engine/API, vendor DSP, timing/latency, channel conversion, format-specific
program behavior and lifecycle outcome above remains open. REQ-008 documents a
warning but never implies cancel/undo behavior. REQ-009 documents panel-list
persistence, not opaque-state round-trip equality. REQ-014 retains an ambiguous
sidechain routing description without assigning a global mute action. Exact
12.4.3 applicability and all listed unsupported states prevent full hosting
coverage or release of this packet as a complete implementation contract.

## Analyst source appendix

Captured official [Using Plug-Ins](https://www.ableton.com/en/live-manual/12/using-plug-ins/),
Version12, 2026-10-19. Retained HTML SHA-256
`df44bdab506fa5422fbe4da0fceaff6e8250e3117d9f5b53802889c83e3e7a1a`.
The source describes multiple platforms and includes historical Intel/PowerPC
notes; none proves Apple-silicon/vendor architecture compatibility. No figures
were inspected. Discovery and source-enable/rescan/crash paragraphs route to
SPEC-PLUGIN-DISCOVERY rather than competing new requirements.

### Source audio-units-plug-ins

[audio-units-plug-ins](../../analysis/ableton-live-12.4.3/full-spec-v1/plugin-hosting/manual-plugins-2026-10-19.html#audio-units-plug-ins), retained HTML line 424; source digest above. HTML anchors locate the original bytes; rendered line numbers are not byte offsets.

### Source plug-in-configure-mode

[plug-in-configure-mode](../../analysis/ableton-live-12.4.3/full-spec-v1/plugin-hosting/manual-plugins-2026-10-19.html#plug-in-configure-mode), retained HTML line 344; source digest above. HTML anchors locate the original bytes; rendered line numbers are not byte offsets.

### Source plug-ins-in-the-device-view

[plug-ins-in-the-device-view](../../analysis/ableton-live-12.4.3/full-spec-v1/plugin-hosting/manual-plugins-2026-10-19.html#plug-ins-in-the-device-view), retained HTML line 292; source digest above. HTML anchors locate the original bytes; rendered line numbers are not byte offsets.

### Source showing-plug-in-panels-in-separate-windows

[showing-plug-in-panels-in-separate-windows](../../analysis/ableton-live-12.4.3/full-spec-v1/plugin-hosting/manual-plugins-2026-10-19.html#showing-plug-in-panels-in-separate-windows), retained HTML line 334; source digest above. HTML anchors locate the original bytes; rendered line numbers are not byte offsets.

### Source sidechain-parameters

[sidechain-parameters](../../analysis/ableton-live-12.4.3/full-spec-v1/plugin-hosting/manual-plugins-2026-10-19.html#sidechain-parameters), retained HTML line 356; source digest above. HTML anchors locate the original bytes; rendered line numbers are not byte offsets.

### Source using-plug-ins

[using-plug-ins](../../analysis/ableton-live-12.4.3/full-spec-v1/plugin-hosting/manual-plugins-2026-10-19.html#using-plug-ins), retained HTML line 280; source digest above. HTML anchors locate the original bytes; rendered line numbers are not byte offsets.

### Source vst-presets-and-banks

[vst-presets-and-banks](../../analysis/ableton-live-12.4.3/full-spec-v1/plugin-hosting/manual-plugins-2026-10-19.html#vst-presets-and-banks), retained HTML line 394; source digest above. HTML anchors locate the original bytes; rendered line numbers are not byte offsets.

