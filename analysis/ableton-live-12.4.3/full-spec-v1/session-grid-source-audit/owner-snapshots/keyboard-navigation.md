---
id: SPEC-KEYBOARD-NAVIGATION
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 5
target: Ableton Live 12 Suite 12.4.3
---

# Keyboard navigation and accessibility workflows

## Scope and authority

This partial successor owns keyboard focus, navigation, accessible-control and
input-entry roles. The [approved partial source audit](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation-source-audit/README-r2.md)
was reconciled through all 23 proposal groups; that audit approval is not owner
adoption approval, runtime evidence, or source-topic completion. The separate
292-row shortcut catalog remains discovery, with zero commands marked complete.

Underlying behavior stays with [Arrangement](arrangement-editing.md),
[MIDI editing](midi-editing-tools.md), [automation](automation-envelopes.md),
[native Warp markers](warp-markers.md), [Warp workflows](warping-workflows.md),
[Browser](browser-workflows.md), [Browser content](browser-content-workflows.md),
[Session](session-view-workflows.md), [launch](session-launch-workflows.md),
[mixing](mixing-workflows.md), [recording](recording-comping.md),
[routing](routing-monitoring-latency.md), [remote control](remote-control-workflows.md),
[settings](settings-learning-workflows.md), [device/racks](device-racks.md),
[plug-in hosting](plugin-hosting.md), [grooves](groove-workflows.md) and
[export](audio-video-export.md). Keyboard entries do not replace those owners'
numeric, edit, scheduling, launch, file, signal, API or protocol contracts.

D12 means captured current Version12 documentation, not exact12.4.3 evidence.
Every target outcome is U and every case is unexecuted. No application, UI,
reader, original function, candidate, image, hardware or network was run or
inspected for this successor. See [research](../research/keyboard-navigation.md).

## Inputs, contexts and oracles

Record platform, language/layout/IME, actual key chord, focused region, selection,
visibility, enabled controls, navigation settings, editor/modal state, valid
parameter domain, reader and genuinely productive control baseline. Main-window
Tab traversal requires global Use Tab ON; deliberate view switching requires OFF.
Settings traversal has the source-supported independent exception. Unsupported
capability or absent baseline remains U, never a negative pass.

The machine case field `expected` retains the old documentary UI expectations
and narrowly added visible input/control roles. It is never an actual target
oracle. Every `actual_expected` and `actual_comparison` is null. New numeric,
reader, timing, signal, analysis, configuration, clipboard/history and unresolved
cases also have null documentary outputs; their prose `source_claim` records
only the public role. No exact accessible tree, utterance, palette, waveform,
value, RNG result, deadline, key priority, default or platform equivalence follows.

[Q-052](../questions.md#q-052-keyboard-export-and-midi-note-modifier-source-differences) remains open: conflicting export and selected-note modifier texts are
retained without choosing dispatch. B350 is enabled-use context for Computer
MIDI octave/velocity rows, not the three toggle rows. B351 is related general
single-letter text, not a proved row-specific prerequisite or forced Shift rule.

## Requirements

### REQ-KEYBOARD-NAV-001 — Accessibility scope

**D12; target U; not run.** The documented host uses native macOS/Windows accessibility facilities and offers high contrast. Support is partial: browser tags/filters, MPE editing, Max and some plug-ins are not supported; Wavetable matrix and advanced Operator controls are not fully optimized. This is a documented limitation, not permission to remove those features or proof of exact-build accessibility. The chapter also lists audio-clip fade editing as not currently supported for screen readers. These remain publication-scope limitations, not a target-build exclusion or successful unsupported-operation test.

Source/context blocks: KN1:B002, KN1:B003, KN1:B004, KN1:B005, KN1:B006, KN1:B007, KN1:B080, KN1:B109, KN1:B120, KN1:B128. Exact quotes and locators: [source context](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/source-context-r5.json); [typed requirement](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/requirements-r5.json).

### REQ-KEYBOARD-NAV-002 — Tab mode

**D12; target U; not run.** With Use Tab Key to Move Focus enabled, Tab/Shift-Tab move next/previous control. With it off, Tab switches Session/Arrangement. Text editors, plug-in windows and modal interception require their own applicability evidence. The documented setting is exposed through Navigate and Display & Input Settings; actual focus/interception outside an independently admitted main-window context remains U.

Source/context blocks: KN1:B013, KN1:B014, KN1:B015, KN1:B019, KN1:B045. Exact quotes and locators: [source context](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/source-context-r5.json); [typed requirement](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/requirements-r5.json).

### REQ-KEYBOARD-NAV-003 — Wrap and mixer neighbors

**D12; target U; not run.** Wrap Tab Navigation enabled cycles last-to-first and first-to-last within an area. Ctrl-Tab/Ctrl-Shift-Tab on Windows or Option-Tab/Option-Shift-Tab on Mac move next/previous mixer control in the same row. Exact focus order for every view remains U. Wrap Tab Navigation is offered through Navigate and Display & Input Settings. The source stopping contrast does not define every off-mode boundary or focus area.

Source/context blocks: KN1:B017, KN1:B018, KN1:B021. Exact quotes and locators: [source context](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/source-context-r5.json); [typed requirement](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/requirements-r5.json).

### REQ-KEYBOARD-NAV-004 — Arrangement arrow option

**D12; target U; not run.** Move Clips with Arrow Keys on allows horizontal movement of selected clips/time selection; off makes left/right collapse time selection to its start/end. Exact move amount/selection semantics are owned by Arrangement or U.

Source/context blocks: KN1:B022, KN2:B374. Exact quotes and locators: [source context](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/source-context-r5.json); [typed requirement](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/requirements-r5.json).

### REQ-KEYBOARD-NAV-005 — Settings traversal exception

**D12; target U; not run.** Ctrl-comma on Windows or Cmd-comma on Mac opens Settings. Settings Tab/Shift-Tab traverse options regardless of global Tab mode. Up/down adjust focused option values or choices; Enter toggles focused toggles. Per-control step/domain is U.

Source/context blocks: KN1:B024, KN1:B025, KN1:B026. Exact quotes and locators: [source context](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/source-context-r5.json); [typed requirement](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/requirements-r5.json).

### REQ-KEYBOARD-NAV-006 — Settings pages and close

**D12; target U; not run.** Ctrl-Tab and Ctrl-Shift-Tab on Windows, Option-Tab and Option-Shift-Tab on Mac change Settings pages; focused page chooser supports up/down. Shift-Tab from first page control returns to page chooser. Escape closes Settings; setting rollback is not implied.

Source/context blocks: KN1:B027, KN1:B028. Exact quotes and locators: [source context](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/source-context-r5.json); [typed requirement](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/requirements-r5.json).

### REQ-KEYBOARD-NAV-007 — Preferred language

**D12; target U; not run.** Changing preferred UI language requires restart for the change to take effect. Restart/language fallback, translation completeness and unsaved-session behavior remain U.

Source/context blocks: KN1:B029. Exact quotes and locators: [source context](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/source-context-r5.json); [typed requirement](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/requirements-r5.json).

### REQ-KEYBOARD-NAV-008 — Screen reader announcements

**D12; target U; not run.** Options Accessibility includes Speak Menu Commands, Speak Minimum and Maximum Slider Values and Speak Time in Seconds. Info/help descriptions depend on screen-reader help-text settings; macOS uses VoiceOver verbosity or VO-Shift-H. Announcement content/order/timing, protocol trees and device coverage are U. The source gives Alt+O on Windows and VO+M then O with macOS VoiceOver for the Options/Accessibility entry. These are platform-specific source roles, not a new generic reader-modifier encoding or guarantee for every reader.

Source/context blocks: KN1:B031, KN1:B032, KN1:B034. Exact quotes and locators: [source context](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/source-context-r5.json); [typed requirement](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/requirements-r5.json).

### REQ-KEYBOARD-NAV-009 — Main-view focus

**D12; target U; not run.** Alt on Windows or Option on Mac plus0..7 focuses Control Bar, Session, Arrangement, Clip editor, Device, Browser, Groove Pool, Learn respectively. Control Bar restores its last-focused control on return. Other-view restoration, hidden-area behavior and modifier/layout collisions remain U. The source gives Alt+N on Windows and VO+M then N with macOS VoiceOver to open Navigate. Main-view focus chords do not prove menu traversal, hidden-view creation or all-focus dispatch.

Source/context blocks: KN1:B047, KN1:B048, KN1:B050, KN1:B051, KN1:B061, KN1:B081, KN1:B110, KN1:B121, KN1:B129, KN1:B132. Exact quotes and locators: [source context](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/source-context-r5.json); [typed requirement](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/requirements-r5.json).

### REQ-KEYBOARD-NAV-010 — Session navigation

**D12; target U; not run.** Arrow keys navigate track titles, clip slots and scenes. Tab/Shift-Tab move between track/slot and mixer controls; neighbor commands move to same control on adjacent tracks. Escape from a track element focuses that track title. Clip/scene launch semantics remain with launch/playback owners.

Source/context blocks: KN1:B053, KN1:B054, KN1:B055, KN1:B057, KN1:B058, KN1:B059, KN1:B060. Exact quotes and locators: [source context](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/source-context-r5.json); [typed requirement](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/requirements-r5.json).

### REQ-KEYBOARD-NAV-011 — Arrangement navigation and edge edit

**D12; target U; not run.** Up/down move tracks; left/right navigate time on the current grid; modified left/right navigate clip edges/locators. Enter at clip edge begins length adjustment with horizontal arrows; Enter confirms, Escape cancels. Exact boundary edits/history remain Arrangement-owned or U.

Source/context blocks: KN1:B065, KN1:B066, KN1:B068, KN1:B070, KN1:B077. Exact quotes and locators: [source context](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/source-context-r5.json); [typed requirement](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/requirements-r5.json).

### REQ-KEYBOARD-NAV-012 — Clip editor focus and initial editor

**D12; target U; not run.** First opening an audio clip selects Sample Editor and MIDI clip selects MIDI Note Editor. Alt/Option3 focuses active editor; Alt/Option-Shift-P focuses clip panels. Documented note/marker key commands dispatch to MIDI/Warp owners; no editor codec or DSP is inferred. With an independently admitted clip and known closed Clip View entry context, the source offers double-click from Session/Arrangement or Ctrl+Alt+3 on Windows/Cmd+Option+3 on Mac to open Clip View. The shortcut table calls that chord Hide/Show Clip View; already-visible/toggle/focus histories remain U rather than an unconditional always-open law.

Source/context blocks: KN1:B082, KN1:B084, KN1:B085, KN2:B019. Exact quotes and locators: [source context](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/source-context-r5.json); [typed requirement](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/requirements-r5.json).

### REQ-KEYBOARD-NAV-013 — Device navigation

**D12; target U; not run.** Devices are represented as accessibility groups. Left/right navigate devices; Tab/Shift-Tab traverse selected-device controls. Device cut/copy/paste/duplicate/delete reuse common device rules. Complete accessible control tree, third-party editors and complex devices remain U.

Source/context blocks: KN1:B112, KN1:B113, KN1:B114, KN1:B115, KN1:B116, KN1:B117, KN1:B118, KN1:B119. Exact quotes and locators: [source context](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/source-context-r5.json); [typed requirement](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/requirements-r5.json).

### REQ-KEYBOARD-NAV-014 — Browser navigation

**D12; target U; not run.** From focused search, Tab reaches filter-view toggle, filter menu, then sidebar; from sidebar Tab reaches shown filters or content pane. Down from search reaches content. Sidebar up/down changes label, left/right move sidebar/content, content right/left expand/collapse folders, Shift-up/down extends selection. Browser search/preview outcomes remain owned by browser workflows; tagging/filter accessibility stays unsupported in source. Browser Workflows004 owns Ctrl+F/Cmd+F search focus with All selection. Browser Content046 owns an eligible selected item preview request via right arrow even while Preview is off; Browser Workflows009 owns generic preview sound. These linked predicates are not duplicated or expanded into all-focus/search/audio behavior here.

Source/context blocks: KN1:B123, KN1:B124, KN1:B125, KN1:B126, KN1:B127, KN1:B128. Exact quotes and locators: [source context](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/source-context-r5.json); [typed requirement](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/requirements-r5.json).

### REQ-KEYBOARD-NAV-015 — Groove Pool and Learn

**D12; target U; not run.** Groove Pool Tab/Shift-Tab traverse groove parameters; up/down adjusts values. Learn focus opens access to lessons. Groove parameter math and lesson/network/content availability remain separate unknowns.

Source/context blocks: KN1:B131, KN1:B133. Exact quotes and locators: [source context](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/source-context-r5.json); [typed requirement](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/requirements-r5.json).

### REQ-KEYBOARD-NAV-016 — Breakpoint create/select/move

**D12; target U; not run.** Envelope insert marker moves horizontally on grid and shows value at location. Enter creates or selects a breakpoint at the marker; horizontal arrows move the pending point; Enter confirms. Alt/Option-left/right jumps previous/next breakpoint. Automation interpolation remains with its canonical owner. The same documented operations have supported track Arrangement automation-lane and clip Envelope Editor contexts where actually available; no every-area/every-envelope cross-product is promised. Alt-click on Windows/Option-click on Mac can move the insert marker to an existing breakpoint and select it. Exact coordinates and parameter-value math remain with automation owners.

Source/context blocks: KN1:B136, KN1:B138, KN1:B139, KN1:B140, KN1:B143, KN1:B144. Exact quotes and locators: [source context](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/source-context-r5.json); [typed requirement](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/requirements-r5.json).

### REQ-KEYBOARD-NAV-017 — Breakpoint value edit and cancel

**D12; target U; not run.** Tab/Shift-Tab select next/previous breakpoint. Typed number or up/down edits selected value; Enter confirms and deselects; Escape cancels and deselects. Delete removes selected point. Exact numeric parser, multi-point/equal-time cases, history and visual animation metrics remain U.

Source/context blocks: KN1:B136, KN1:B145, KN1:B148, KN1:B149. Exact quotes and locators: [source context](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/source-context-r5.json); [typed requirement](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/requirements-r5.json).

### REQ-KEYBOARD-NAV-018 — Envelope chooser cycling

**D12; target U; not run.** In Arrangement View, Alt/Option-up/down cycles automated device envelopes on the track. Adding Shift cycles all device parameters including ones without envelopes. Order, empty-list wrap, hidden device and selection effects remain U.

Source/context blocks: KN1:B151, KN1:B152. Exact quotes and locators: [source context](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/source-context-r5.json); [typed requirement](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/requirements-r5.json).

### REQ-KEYBOARD-NAV-019 — Shortcut discovery boundary

**D12; target U; not run.** The separately retained292-row shortcut catalog records documented command/binding pairs and source syntax for both platforms. It is a discovery inventory, not292 closed commands or executable tests. Per-row context, current-build applicability, command ownership and conflict resolution need reconciliation before release. Source qualifiers stay local to the rows they support. B350 enabled Computer MIDI octave/velocity use is not a prerequisite for the MIDI Map/Key Map/Computer MIDI toggles; B351 is related general single-letter-plus-Shift context, not a forced per-row modifier or global dispatch exception. Command ownership and actual target dispatch remain unreconciled.

Source/context blocks: KN2:B037, KN2:B081, KN2:B110, KN2:B336, KN2:B345, KN2:B346, KN2:B347, KN2:B348, KN2:B349, KN2:B350, KN2:B351. Exact quotes and locators: [source context](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/source-context-r5.json); [typed requirement](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/requirements-r5.json).

### REQ-KEYBOARD-NAV-020 — Focus conflicts and invalid inputs

**U; target U; not run.** Keyboard layout/IME, text-edit/Computer MIDI keyboard/key mapping conflicts, hidden/disabled controls, modal/plug-in windows, no-selection/boundary focus and unsupported accessibility operations have no general dispatch or error oracle.

Source/context blocks: KN1:B045, KN2:B351. Exact quotes and locators: [source context](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/source-context-r5.json); [typed requirement](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/requirements-r5.json).

### REQ-KEYBOARD-NAV-021 — Lifecycle and protocol outcomes

**U; target U; not run.** Focus/history/settings persistence through save/reopen, undo/redo, engine disconnect, reader restart, window/device deletion, teardown and failed accessibility communication remain U. No exact announcement, timing, pixel or resource tolerance is assigned.

Source/context blocks: KN1:B002, KN1:B135, KN1:B147. Exact quotes and locators: [source context](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/source-context-r5.json); [typed requirement](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/requirements-r5.json).

### REQ-KEYBOARD-NAV-022 — Platform menu entry and navigation

**D12; target U; not run.** On Windows the source offers Alt plus a menu first letter (Alt+F for File), then up/down among items, left/right to neighboring menus and Enter to choose. On Mac Cmd+? opens menu-entry search, with up/down among suggestions and Enter choosing one. These roles apply only in independently admitted platform/language/focus/menu contexts; no universal translated-letter, search ranking or command-result law follows.

Source/context blocks: KN2:B382, KN2:B383, KN2:B384, KN2:B385, KN2:B386. Exact quotes and locators: [source context](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/source-context-r5.json); [typed requirement](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/requirements-r5.json).

### REQ-KEYBOARD-NAV-023 — Context-menu entry and settings scope

**D12; target U; not run.** For an admitted interface region with an available context menu, the source offers right-click Windows/Ctrl-click Mac; Menu or Shift+F10 Windows, and VO+Shift+M Mac. Some entries are context-menu-only, and some modify general Settings rather than only the selected item. Exact items, global state effects, protocol tree, reader success and rollback remain U.

Source/context blocks: KN2:B388, KN2:B389, KN1:B053. Exact quotes and locators: [source context](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/source-context-r5.json); [typed requirement](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/requirements-r5.json).

### REQ-KEYBOARD-NAV-024 — Control Bar groups with help context

**D12; target U; not run.** The source describes Control Bar controls as accessible groupings and Tab/Shift-Tab traversal with Speak Help Text active. Require a functioning supported reader and admitted controls before proposing group/help observations. This adds no complete accessible tree, exact help string, speech/protocol/timing or other-view restoration guarantee.

Source/context blocks: KN1:B049, KN1:B050. Exact quotes and locators: [source context](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/source-context-r5.json); [typed requirement](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/requirements-r5.json).

### REQ-KEYBOARD-NAV-025 — Session keyboard command entries

**D12; target U; not run.** At a focused eligible MIDI-track clip slot, Ctrl+Shift+M Windows/Cmd+Shift+M Mac is the documented empty MIDI-clip insertion entry. Enter on a selected scene is the documented scene launch entry. Session View001/SV001 already owns selected-clip Enter; it is only a linked positive integration baseline here. Track/scene selection, return-slot eligibility, launch/record gates, quantization and delivered audio/timing remain with Session/launch/record/routing owners, not a new scheduler or clip codec.

Source/context blocks: KN1:B054, KN1:B055. Exact quotes and locators: [source context](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/source-context-r5.json); [typed requirement](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/requirements-r5.json).

Related owner context: [session-view-workflows](session-view-workflows.md), [session-launch-workflows](session-launch-workflows.md), [routing-monitoring-latency](routing-monitoring-latency.md).

### REQ-KEYBOARD-NAV-026 — Arrangement mixer, grid and locator entries

**D12; target U; not run.** In an admitted Arrangement mixer context, Ctrl+Tab Windows/Option+Tab Mac moves between track mixers; Tab/Shift-Tab traverses the admitted track mixer controls. The source offers + and - to widen/narrow the Arrangement grid, without specifying a numeric ratio or dispatch in other focus contexts. At an admitted timeline location, Tab can reach Set Locator and Enter requests the Arrangement owner’s locator creation; Tab/Shift-Tab navigate locators and Delete requests its selected-locator deletion. Exact positions, identity, ordering, ties and grid/zoom interception remain U or Arrangement-owned.

Source/context blocks: KN1:B069, KN1:B072, KN1:B073, KN1:B074, KN1:B066. Exact quotes and locators: [source context](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/source-context-r5.json); [typed requirement](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/requirements-r5.json).

Related owner context: [arrangement-editing](arrangement-editing.md).

### REQ-KEYBOARD-NAV-027 — Arrangement content keyboard entries

**D12; target U; not run.** In the source timeline context Shift plus arrows selects content; left/right moves selected content; Ctrl Windows/Cmd Mac plus X/C/V/D provides Cut/Copy/Paste/Duplicate, and Delete deletes. These are bounded input/action roles, not byte/state/clipboard, move-amount or edit/history algorithms. Applicable selection and Move Clips with Arrow Keys state must be retained.

Source/context blocks: KN1:B075. Exact quotes and locators: [source context](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/source-context-r5.json); [typed requirement](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/requirements-r5.json).

Related owner context: [arrangement-editing](arrangement-editing.md).

### REQ-KEYBOARD-NAV-028 — MIDI time selection and insert-marker entries

**D12; target U; not run.** In an admitted MIDI Note Editor context, Shift+left/right from an insert marker selects time; Enter selects notes contained in that time selection. Ctrl Windows/Option Mac plus left/right is the source insert-marker previous/next note-boundary entry. Previous/next selected-note and same-pitch modifier differences stay U under Q052; do not infer a global shortcut precedence or selection algorithm.

Source/context blocks: KN1:B089, KN1:B090, KN1:B091. Exact quotes and locators: [source context](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/source-context-r5.json); [typed requirement](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/requirements-r5.json).

Related owner context: [midi-editing-tools](midi-editing-tools.md).

### REQ-KEYBOARD-NAV-029 — MIDI note-edit keyboard roles

**D12; target U; not run.** For admitted selected editable notes, the source offers up/down transpose, Shift+up/down octave transpose, Shift+left/right length edit, left/right time move, Ctrl Windows/Cmd Mac plus up/down velocity edit, and Ctrl+Alt Windows/Cmd+Option Mac plus up/down probability edit. Existing MIDI owners retain pitch/scale/time/value domains and laws; no exact step, codec, RNG probability realization or generated note/audio output is specified here.

Source/context blocks: KN1:B097, KN1:B098, KN1:B099, KN1:B100, KN1:B101, KN1:B102. Exact quotes and locators: [source context](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/source-context-r5.json); [typed requirement](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/requirements-r5.json).

Related owner context: [midi-editing-tools](midi-editing-tools.md).

### REQ-KEYBOARD-NAV-030 — MIDI Note Editor Preview control

**D12; target U; not run.** Options offers MIDI Note Editor Preview. REQ-MIDI-EDIT-022 owns existing preview/add/move audition behavior; this clause adds the Options entry and retains the source selected-note preview context only. Require independently working owned note/instrument/preview/output paths. No signal, onset, note/voice codec, preview-off exclusion or supported-instrument universality is added.

Source/context blocks: KN1:B088. Exact quotes and locators: [source context](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/source-context-r5.json); [typed requirement](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/requirements-r5.json).

Related owner context: [midi-editing-tools](midi-editing-tools.md).

### REQ-KEYBOARD-NAV-031 — Audio-editor keyboard entry roles

**D12; target U; not run.** In an admitted audio Sample Editor context, the source offers Ctrl Windows/Option Mac plus left/right to move its insert marker, Shift plus left/right for time selection, and arrows to move a selected Warp Marker. Ctrl+I Windows/Cmd+I Mac is the insert-and-select Warp Marker entry; Ctrl+Shift+I Windows/Cmd+Shift+I Mac inserts a transient. Native marker/storage and interactive Warp owners retain coordinates, validation, generated identity, detector and sound laws.

Source/context blocks: KN1:B104, KN1:B105, KN1:B106, KN1:B107, KN1:B108. Exact quotes and locators: [source context](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/source-context-r5.json); [typed requirement](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/requirements-r5.json).

Related owner context: [clip-view-workflows](clip-view-workflows.md), [warping-workflows](warping-workflows.md), [warp-markers](warp-markers.md).

### REQ-KEYBOARD-NAV-032 — Envelope-area and reader-feedback contexts

**D12; target U; not run.** The documented keyboard envelope operations are offered in Arrangement track automation lanes and clip Envelope Editor contexts where actually supported. The chapter describes reader feedback while changes are made. Establish genuine valid area/point/value and supported-reader feedback baselines separately; no Arrangement-modulation constructor, complete cross-product, accessible tree or exact announcement/event/timing follows.

Source/context blocks: KN1:B135, KN1:B136. Exact quotes and locators: [source context](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/source-context-r5.json); [typed requirement](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/requirements-r5.json).

Related owner context: [automation-envelopes](automation-envelopes.md), [automation-workflows](automation-workflows.md).

### REQ-KEYBOARD-NAV-033 — Breakpoint visual feedback roles

**D12; target U; not run.** The source describes a focused breakpoint as different-colored from the main envelope and the same color as hover; a selected editable breakpoint pulses. After moving and undoing a breakpoint it describes temporary focused/hover color feedback, with vertically aligned editing as context. Exact palette/pixels, frame rate, duration, same-time ordering and byte/history restoration remain U; no timing or animation comparator is assigned.

Source/context blocks: KN1:B141, KN1:B146, KN1:B147. Exact quotes and locators: [source context](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/source-context-r5.json); [typed requirement](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/requirements-r5.json).

Related owner context: [automation-workflows](automation-workflows.md).

### REQ-KEYBOARD-NAV-034 — Momentary latching control role

**D12; target U; not run.** The source lists momentary hold/release latching for A Arrangement Automation, B Draw Mode, S selected-track Solo, Z Arrangement-selection zoom, F1..F8 first-eight Track Activators, and Tab view switching. Releasing a genuinely admitted latched shortcut is described as returning UI to its previous state. Source about500ms is qualified context, not a strict threshold, target deadline or global focus/keymap/Computer MIDI exception. The Tab view-switch history requires explicit global Use Tab Key to Move Focus OFF; enabled Tab traversal is a different documented role, not an inferred latching exception.

Source/context blocks: KN2:B353, KN2:B354, KN2:B355, KN2:B356, KN2:B357, KN2:B358, KN2:B359. Exact quotes and locators: [source context](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/source-context-r5.json); [typed requirement](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/requirements-r5.json).

### REQ-KEYBOARD-NAV-035 — Documented latching-disable entry

**D12; target U; not run.** The source names Options.txt entry -DisableHotKeyLatching for turning off momentary latching. This is a public option-purpose role only: exact path, encoding, file admission, load/reload timing, persistence, platform/default and failed-file behavior remain U with configuration owners. No file operation or result is graded.

Source/context blocks: KN2:B360. Exact quotes and locators: [source context](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/source-context-r5.json); [typed requirement](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/requirements-r5.json).

Related owner context: [settings-learning-workflows](settings-learning-workflows.md).

### REQ-KEYBOARD-NAV-036 — Enabled Computer MIDI octave and velocity-use context

**D12; target U; not run.** For independently enabled, functioning Computer MIDI Keyboard use, the discovery source names X/Z for octave-range and C/V for incoming note-velocity-range adjustment. B350 supports the enabled-use context for those two range rows. B350 is not an enabled prerequisite for MIDI Map/Key Map/Computer MIDI toggle rows. B351 remains related general single-letter-plus-Shift text, not a proved modifier for any of the five rows. No exact range/value/note codec, dispatch exception or key-repeat law is supplied.

Source/context blocks: KN2:B348, KN2:B349, KN2:B350, KN2:B351. Exact quotes and locators: [source context](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/source-context-r5.json); [typed requirement](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/requirements-r5.json).

### REQ-KEYBOARD-NAV-037 — Selected Clip Panel focus

**D12; target U; not run.** The shortcut table lists Alt+8 Windows/Option+8 Mac for focus to the selected Clip Panel. This is separate from0..7 main-view focus and Alt/Option+Shift+P clip-panels focus. Require an independently present eligible selected panel; hidden/missing-panel, selection/interception, reader and focus-restoration outcomes remain U.

Source/context blocks: KN2:B035. Exact quotes and locators: [source context](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/source-context-r5.json); [typed requirement](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/requirements-r5.json).

### REQ-KEYBOARD-NAV-038 — Audio Settings keyboard setup context

**D12; target U; not run.** The source describes opening Settings, navigating to its Audio page with arrows and traversing admitted device options with Tab. macOS CoreAudio/driver-type and Windows driver/device-program descriptions are platform-specific setup context only. Existing routing/settings owners retain device availability/configuration; no any-device success, driver protocol, hardware, buffer or numeric latency law is added.

Source/context blocks: KN1:B036, KN1:B037, KN1:B038. Exact quotes and locators: [source context](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/source-context-r5.json); [typed requirement](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/requirements-r5.json).

Related owner context: [routing-monitoring-latency](routing-monitoring-latency.md), [settings-learning-workflows](settings-learning-workflows.md).

### REQ-KEYBOARD-NAV-039 — MIDI surface settings keyboard context

**D12; target U; not run.** The source describes keyboard-selectable Control Surface choosers in Link, Tempo & MIDI and per-surface input/output choices. Its six-menu count, qualified automatic detection/many-no-configuration and script/reader variation are current publication context, not target capacity, every-device detection or149-profile compatibility. Generic remote/routing owners retain port/script setup; no protocol, firmware, hardware or reader-success result follows.

Source/context blocks: KN1:B040, KN1:B041, KN1:B042. Exact quotes and locators: [source context](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/source-context-r5.json); [typed requirement](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/requirements-r5.json).

Related owner context: [remote-control-workflows](remote-control-workflows.md), [routing-monitoring-latency](routing-monitoring-latency.md).

### REQ-KEYBOARD-NAV-U-SOURCE — Unresolved source dispatch differences

**U; target U; not run.** Q052 stays open. Accessibility export Ctrl+R/Cmd+R differs from shortcut-table Ctrl+Shift+R/Cmd+Shift+R export and Ctrl+R/Cmd+R Rename. Accessibility Windows Ctrl previous/next note and same-pitch navigation differs from shortcut-table Windows Alt; Mac Option agreement does not settle all context. Preserve both source texts and original292 rows. No preferred dispatch, Shift extension precedence, export default or negative/no-effect law is chosen.

Source/context blocks: KN1:B079, KN1:B093, KN1:B094, KN1:B095, KN2:B051, KN2:B075, KN2:B174, KN2:B175. Exact quotes and locators: [source context](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/source-context-r5.json); [typed requirement](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/requirements-r5.json).

Related owner context: [audio-video-export](audio-video-export.md), [midi-editing-tools](midi-editing-tools.md).

## Finite future cases

The [96-case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/cases-r5.json) retains all42 prior IDs and documentary expectations. Four actions are refined;54 cases are added. Shared [fixtures](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/fixtures-r5.json) require productive baselines. The table is navigation; catalog actions, exact block pointers and null oracles are authoritative.

| Case | Requirement | Kind | Documentary output | Target |
| --- | --- | --- | --- | --- |
| NAV-001 | REQ-KEYBOARD-NAV-001 | scope | UI role only | U; not run |
| NAV-002 | REQ-KEYBOARD-NAV-002 | positive | UI role only | U; not run |
| NAV-003 | REQ-KEYBOARD-NAV-002 | negative | UI role only | U; not run |
| NAV-004 | REQ-KEYBOARD-NAV-003 | boundary | UI role only | U; not run |
| NAV-005 | REQ-KEYBOARD-NAV-003 | positive | UI role only | U; not run |
| NAV-006 | REQ-KEYBOARD-NAV-004 | positive | UI role only | U; not run |
| NAV-007 | REQ-KEYBOARD-NAV-004 | negative | UI role only | U; not run |
| NAV-008 | REQ-KEYBOARD-NAV-005 | positive | UI role only | U; not run |
| NAV-009 | REQ-KEYBOARD-NAV-005 | positive | UI role only | U; not run |
| NAV-010 | REQ-KEYBOARD-NAV-006 | positive | UI role only | U; not run |
| NAV-011 | REQ-KEYBOARD-NAV-006 | boundary | UI role only | U; not run |
| NAV-012 | REQ-KEYBOARD-NAV-007 | persistence | UI role only | U; not run |
| NAV-013 | REQ-KEYBOARD-NAV-008 | positive | UI role only | U; not run |
| NAV-014 | REQ-KEYBOARD-NAV-009 | positive | UI role only | U; not run |
| NAV-015 | REQ-KEYBOARD-NAV-009 | persistence | UI role only | U; not run |
| NAV-016 | REQ-KEYBOARD-NAV-010 | positive | UI role only | U; not run |
| NAV-017 | REQ-KEYBOARD-NAV-010 | positive | UI role only | U; not run |
| NAV-018 | REQ-KEYBOARD-NAV-011 | positive | UI role only | U; not run |
| NAV-019 | REQ-KEYBOARD-NAV-011 | cancel | UI role only | U; not run |
| NAV-020 | REQ-KEYBOARD-NAV-011 | positive | UI role only | U; not run |
| NAV-021 | REQ-KEYBOARD-NAV-012 | positive | UI role only | U; not run |
| NAV-022 | REQ-KEYBOARD-NAV-012 | positive | UI role only | U; not run |
| NAV-023 | REQ-KEYBOARD-NAV-013 | positive | UI role only | U; not run |
| NAV-024 | REQ-KEYBOARD-NAV-014 | positive | UI role only | U; not run |
| NAV-025 | REQ-KEYBOARD-NAV-014 | positive | UI role only | U; not run |
| NAV-026 | REQ-KEYBOARD-NAV-015 | positive | UI role only | U; not run |
| NAV-027 | REQ-KEYBOARD-NAV-015 | positive | UI role only | U; not run |
| NAV-028 | REQ-KEYBOARD-NAV-016 | positive | UI role only | U; not run |
| NAV-029 | REQ-KEYBOARD-NAV-016 | positive | UI role only | U; not run |
| NAV-030 | REQ-KEYBOARD-NAV-017 | positive | UI role only | U; not run |
| NAV-031 | REQ-KEYBOARD-NAV-017 | cancel | UI role only | U; not run |
| NAV-032 | REQ-KEYBOARD-NAV-017 | positive | UI role only | U; not run |
| NAV-033 | REQ-KEYBOARD-NAV-018 | positive | UI role only | U; not run |
| NAV-034 | REQ-KEYBOARD-NAV-019 | discovery | UI role only | U; not run |
| NAV-035 | REQ-KEYBOARD-NAV-020 | negative | null | U; not run |
| NAV-036 | REQ-KEYBOARD-NAV-020 | boundary | null | U; not run |
| NAV-037 | REQ-KEYBOARD-NAV-020 | malformed | null | U; not run |
| NAV-038 | REQ-KEYBOARD-NAV-020 | interaction | null | U; not run |
| NAV-039 | REQ-KEYBOARD-NAV-021 | error | null | U; not run |
| NAV-040 | REQ-KEYBOARD-NAV-021 | undo | null | U; not run |
| NAV-041 | REQ-KEYBOARD-NAV-021 | persistence | null | U; not run |
| NAV-042 | REQ-KEYBOARD-NAV-021 | teardown | null | U; not run |
| NAV-043 | REQ-KEYBOARD-NAV-001 | control | UI role only | U; not run |
| NAV-044 | REQ-KEYBOARD-NAV-002 | control | UI role only | U; not run |
| NAV-045 | REQ-KEYBOARD-NAV-003 | control | UI role only | U; not run |
| NAV-046 | REQ-KEYBOARD-NAV-004 | initial-context | null | U; not run |
| NAV-047 | REQ-KEYBOARD-NAV-005 | control | UI role only | U; not run |
| NAV-048 | REQ-KEYBOARD-NAV-005 | control | UI role only | U; not run |
| NAV-049 | REQ-KEYBOARD-NAV-005 | numeric | null | U; not run |
| NAV-050 | REQ-KEYBOARD-NAV-008 | control | UI role only | U; not run |
| NAV-051 | REQ-KEYBOARD-NAV-008 | reader | null | U; not run |
| NAV-052 | REQ-KEYBOARD-NAV-008 | reader | null | U; not run |
| NAV-053 | REQ-KEYBOARD-NAV-008 | reader | null | U; not run |
| NAV-054 | REQ-KEYBOARD-NAV-009 | control | UI role only | U; not run |
| NAV-055 | REQ-KEYBOARD-NAV-022 | control | UI role only | U; not run |
| NAV-056 | REQ-KEYBOARD-NAV-022 | control | UI role only | U; not run |
| NAV-057 | REQ-KEYBOARD-NAV-023 | control | UI role only | U; not run |
| NAV-058 | REQ-KEYBOARD-NAV-023 | state | null | U; not run |
| NAV-059 | REQ-KEYBOARD-NAV-024 | reader | null | U; not run |
| NAV-060 | REQ-KEYBOARD-NAV-025 | state | UI role only | U; not run |
| NAV-061 | REQ-KEYBOARD-NAV-025 | timing | null | U; not run |
| NAV-062 | REQ-KEYBOARD-NAV-026 | numeric | null | U; not run |
| NAV-063 | REQ-KEYBOARD-NAV-026 | state | UI role only | U; not run |
| NAV-064 | REQ-KEYBOARD-NAV-027 | edit | null | U; not run |
| NAV-065 | REQ-KEYBOARD-NAV-012 | control | UI role only | U; not run |
| NAV-066 | REQ-KEYBOARD-NAV-030 | signal | null | U; not run |
| NAV-067 | REQ-KEYBOARD-NAV-028 | state | null | U; not run |
| NAV-068 | REQ-KEYBOARD-NAV-028 | timing | null | U; not run |
| NAV-069 | REQ-KEYBOARD-NAV-029 | numeric | null | U; not run |
| NAV-070 | REQ-KEYBOARD-NAV-029 | numeric | null | U; not run |
| NAV-071 | REQ-KEYBOARD-NAV-029 | numeric | null | U; not run |
| NAV-072 | REQ-KEYBOARD-NAV-029 | numeric | null | U; not run |
| NAV-073 | REQ-KEYBOARD-NAV-029 | numeric | null | U; not run |
| NAV-074 | REQ-KEYBOARD-NAV-029 | numeric | null | U; not run |
| NAV-075 | REQ-KEYBOARD-NAV-031 | timing | null | U; not run |
| NAV-076 | REQ-KEYBOARD-NAV-031 | timing | null | U; not run |
| NAV-077 | REQ-KEYBOARD-NAV-031 | analysis | null | U; not run |
| NAV-078 | REQ-KEYBOARD-NAV-031 | analysis | null | U; not run |
| NAV-079 | REQ-KEYBOARD-NAV-013 | edit | null | U; not run |
| NAV-080 | REQ-KEYBOARD-NAV-014 | state | null | U; not run |
| NAV-081 | REQ-KEYBOARD-NAV-016 | state | null | U; not run |
| NAV-082 | REQ-KEYBOARD-NAV-016 | state | UI role only | U; not run |
| NAV-083 | REQ-KEYBOARD-NAV-016 | state | UI role only | U; not run |
| NAV-084 | REQ-KEYBOARD-NAV-017 | numeric | null | U; not run |
| NAV-085 | REQ-KEYBOARD-NAV-032 | reader | null | U; not run |
| NAV-086 | REQ-KEYBOARD-NAV-033 | control | UI role only | U; not run |
| NAV-087 | REQ-KEYBOARD-NAV-033 | timing | null | U; not run |
| NAV-088 | REQ-KEYBOARD-NAV-034 | timing | null | U; not run |
| NAV-089 | REQ-KEYBOARD-NAV-035 | configuration | null | U; not run |
| NAV-090 | REQ-KEYBOARD-NAV-036 | numeric | null | U; not run |
| NAV-091 | REQ-KEYBOARD-NAV-037 | control | UI role only | U; not run |
| NAV-092 | REQ-KEYBOARD-NAV-038 | control | UI role only | U; not run |
| NAV-093 | REQ-KEYBOARD-NAV-039 | control | null | U; not run |
| NAV-094 | REQ-KEYBOARD-NAV-U-SOURCE | unresolved | null | U; not run |
| NAV-095 | REQ-KEYBOARD-NAV-U-SOURCE | unresolved | null | U; not run |
| NAV-096 | REQ-KEYBOARD-NAV-020 | unresolved | null | U; not run |

## Evidence, preservation and remaining work

Two original official chapters retain exact URLs, capture UTCs, Version12 labels,
bytes and hashes in [source metadata](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/sources.json).
All541 source blocks and292 discovery rows retain their original identities.
R5 selects exact text/row contexts, not uninspected figure labels or link content.
Full source audit enumeration is distinct from this bounded owner adoption.

The [23-group reconciliation](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/reconciliation-r5.json)
routes existing predicates and records retained unknowns rather than asserting
whole-group completion. [Exact deltas](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/delta-r5.json)
retain21 prior requirements and42 cases, add19 requirements and54 cases, and
explain the10 body and4 action refinements. Original R4/history files remain
byte-identical in place; exact prior canonical bytes are retained separately.

Independent owner semantic review and any handoff remain pending. Q052, target
availability, every reader/platform/context combination, full292-command
applicability, malformed/intercepted input, persistence, undo, transport/rate,
teardown and unavailable-capability results remain U. Source-filled rows are
neither product completion nor reference/candidate comparison success.
