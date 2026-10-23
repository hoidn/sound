---
id: SPEC-KEYBOARD-NAVIGATION
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3
---

# Keyboard navigation and accessibility workflows

## Scope and authority

This partial contract owns focus/navigation and accessibility workflow, plus an
explicitly unclosed shortcut discovery inventory. Domain actions remain with
[Arrangement](arrangement-editing.md), [MIDI editing](midi-editing-tools.md),
[automation](automation-envelopes.md), [Warp](warp-markers.md),
[browser](browser-workflows.md), [rack/device](device-racks.md),
[plug-in hosting](plugin-hosting.md), [groove](groove-workflows.md) and
[recording](recording-comping.md) owners. A key binding does not specify the
underlying engine/edit algorithm or imply it is enabled in every context.

D12 describes captured current Version12 documentation. All exact12.4.3 behavior
is U. No application, UI, reader, original code, candidate or screenshot was run
or inspected. See [research evidence](../research/keyboard-navigation.md).

## Inputs and observable outcomes

Inputs include OS/layout/IME, key chord, focused region/selection, enabled controls,
visibility, navigation settings, editor/modal state, parameter domain and reader.
Observe focus, view/chooser/selection, confirmed versus cancelled edit and exposed
announcement options. Do not require an internal dispatch API, exact accessible
protocol tree, speech string, waveform, pixel or timing metric without evidence.
Only discrete supported navigation predicates have documentary expectations.

## Requirements

### REQ-KEYBOARD-NAV-001 — Accessibility scope

**D12; exact-build U.** The documented host uses native macOS/Windows accessibility facilities and offers high contrast. Support is partial: browser tags/filters, MPE editing, Max and some plug-ins are not supported; Wavetable matrix and advanced Operator controls are not fully optimized. This is a documented limitation, not permission to remove those features or proof of exact-build accessibility. [Source accessibility-and-keyboard-navigation](#source-accessibility-and-keyboard-navigation).

### REQ-KEYBOARD-NAV-002 — Tab mode

**D12; exact-build U.** With Use Tab Key to Move Focus enabled, Tab/Shift-Tab move next/previous control. With it off, Tab switches Session/Arrangement. Text editors, plug-in windows and modal interception require their own applicability evidence. [Source using-tab-for-navigation](#source-using-tab-for-navigation).

### REQ-KEYBOARD-NAV-003 — Wrap and mixer neighbors

**D12; exact-build U.** Wrap Tab Navigation enabled cycles last-to-first and first-to-last within an area. Ctrl-Tab/Ctrl-Shift-Tab on Windows or Option-Tab/Option-Shift-Tab on Mac move next/previous mixer control in the same row. Exact focus order for every view remains U. [Source using-tab-for-navigation](#source-using-tab-for-navigation).

### REQ-KEYBOARD-NAV-004 — Arrangement arrow option

**D12; exact-build U.** Move Clips with Arrow Keys on allows horizontal movement of selected clips/time selection; off makes left/right collapse time selection to its start/end. Exact move amount/selection semantics are owned by Arrangement or U. [Source using-tab-for-navigation](#source-using-tab-for-navigation).

### REQ-KEYBOARD-NAV-005 — Settings traversal exception

**D12; exact-build U.** Ctrl-comma on Windows or Cmd-comma on Mac opens Settings. Settings Tab/Shift-Tab traverse options regardless of global Tab mode. Up/down adjust focused option values or choices; Enter toggles focused toggles. Per-control step/domain is U. [Source settings-menu](#source-settings-menu).

### REQ-KEYBOARD-NAV-006 — Settings pages and close

**D12; exact-build U.** Ctrl-Tab and Ctrl-Shift-Tab on Windows, Option-Tab and Option-Shift-Tab on Mac change Settings pages; focused page chooser supports up/down. Shift-Tab from first page control returns to page chooser. Escape closes Settings; setting rollback is not implied. [Source settings-menu](#source-settings-menu).

### REQ-KEYBOARD-NAV-007 — Preferred language

**D12; exact-build U.** Changing preferred UI language requires restart for the change to take effect. Restart/language fallback, translation completeness and unsaved-session behavior remain U. [Source settings-menu](#source-settings-menu).

### REQ-KEYBOARD-NAV-008 — Screen reader announcements

**D12; exact-build U.** Options Accessibility includes Speak Menu Commands, Speak Minimum and Maximum Slider Values and Speak Time in Seconds. Info/help descriptions depend on screen-reader help-text settings; macOS uses VoiceOver verbosity or VO-Shift-H. Announcement content/order/timing, protocol trees and device coverage are U. [Source options-menu](#source-options-menu).

### REQ-KEYBOARD-NAV-009 — Main-view focus

**D12; exact-build U.** Alt on Windows or Option on Mac plus0..7 focuses Control Bar, Session, Arrangement, Clip editor, Device, Browser, Groove Pool, Learn respectively. Control Bar restores its last-focused control on return. Other-view restoration, hidden-area behavior and modifier/layout collisions remain U. [Source navigate-menu](#source-navigate-menu).

### REQ-KEYBOARD-NAV-010 — Session navigation

**D12; exact-build U.** Arrow keys navigate track titles, clip slots and scenes. Tab/Shift-Tab move between track/slot and mixer controls; neighbor commands move to same control on adjacent tracks. Escape from a track element focuses that track title. Clip/scene launch semantics remain with launch/playback owners. [Source session-view---alt-1-win--option-1-mac](#source-session-view---alt-1-win--option-1-mac).

### REQ-KEYBOARD-NAV-011 — Arrangement navigation and edge edit

**D12; exact-build U.** Up/down move tracks; left/right navigate time on the current grid; modified left/right navigate clip edges/locators. Enter at clip edge begins length adjustment with horizontal arrows; Enter confirms, Escape cancels. Exact boundary edits/history remain Arrangement-owned or U. [Source arrangement-view---alt-2-win--option-2-mac](#source-arrangement-view---alt-2-win--option-2-mac).

### REQ-KEYBOARD-NAV-012 — Clip editor focus and initial editor

**D12; exact-build U.** First opening an audio clip selects Sample Editor and MIDI clip selects MIDI Note Editor. Alt/Option3 focuses active editor; Alt/Option-Shift-P focuses clip panels. Documented note/marker key commands dispatch to MIDI/Warp owners; no editor codec or DSP is inferred. [Source clip-view---alt-3-win--option-3-mac](#source-clip-view---alt-3-win--option-3-mac).

### REQ-KEYBOARD-NAV-013 — Device navigation

**D12; exact-build U.** Devices are represented as accessibility groups. Left/right navigate devices; Tab/Shift-Tab traverse selected-device controls. Device cut/copy/paste/duplicate/delete reuse common device rules. Complete accessible control tree, third-party editors and complex devices remain U. [Source device-view---alt-4-win--option-4-mac](#source-device-view---alt-4-win--option-4-mac).

### REQ-KEYBOARD-NAV-014 — Browser navigation

**D12; exact-build U.** From focused search, Tab reaches filter-view toggle, filter menu, then sidebar; from sidebar Tab reaches shown filters or content pane. Down from search reaches content. Sidebar up/down changes label, left/right move sidebar/content, content right/left expand/collapse folders, Shift-up/down extends selection. Browser search/preview outcomes remain owned by browser workflows; tagging/filter accessibility stays unsupported in source. [Source browser---alt-5-win--option-5-mac](#source-browser---alt-5-win--option-5-mac).

### REQ-KEYBOARD-NAV-015 — Groove Pool and Learn

**D12; exact-build U.** Groove Pool Tab/Shift-Tab traverse groove parameters; up/down adjusts values. Learn focus opens access to lessons. Groove parameter math and lesson/network/content availability remain separate unknowns. [Source groove-pool---alt-6-win--option-6-mac](#source-groove-pool---alt-6-win--option-6-mac).

### REQ-KEYBOARD-NAV-016 — Breakpoint create/select/move

**D12; exact-build U.** Envelope insert marker moves horizontally on grid and shows value at location. Enter creates or selects a breakpoint at the marker; horizontal arrows move the pending point; Enter confirms. Alt/Option-left/right jumps previous/next breakpoint. Automation interpolation remains with its canonical owner. [Source navigating-between-breakpoints](#source-navigating-between-breakpoints).

### REQ-KEYBOARD-NAV-017 — Breakpoint value edit and cancel

**D12; exact-build U.** Tab/Shift-Tab select next/previous breakpoint. Typed number or up/down edits selected value; Enter confirms and deselects; Escape cancels and deselects. Delete removes selected point. Exact numeric parser, multi-point/equal-time cases, history and visual animation metrics remain U. [Source selecting-and-editing-breakpoints](#source-selecting-and-editing-breakpoints).

### REQ-KEYBOARD-NAV-018 — Envelope chooser cycling

**D12; exact-build U.** Alt/Option-up/down cycles automated device envelopes on the track. Adding Shift cycles all device parameters including ones without envelopes. Order, empty-list wrap, hidden device and selection effects remain U. [Source switching-between-automation-envelopes-in-arrangement-view](#source-switching-between-automation-envelopes-in-arrangement-view).

### REQ-KEYBOARD-NAV-019 — Shortcut discovery boundary

**D12; exact-build U.** The separately retained292-row shortcut catalog records documented command/binding pairs and source syntax for both platforms. It is a discovery inventory, not292 closed commands or executable tests. Per-row context, current-build applicability, command ownership and conflict resolution need reconciliation before release. [Source menu-and-keyboard-navigation-settings](#source-menu-and-keyboard-navigation-settings).

### REQ-KEYBOARD-NAV-020 — Focus conflicts and invalid inputs

**U; exact-build U.** Keyboard layout/IME, text-edit/Computer MIDI keyboard/key mapping conflicts, hidden/disabled controls, modal/plug-in windows, no-selection/boundary focus and unsupported accessibility operations have no general dispatch or error oracle. [Source navigating-in-live](#source-navigating-in-live).

### REQ-KEYBOARD-NAV-021 — Lifecycle and protocol outcomes

**U; exact-build U.** Focus/history/settings persistence through save/reopen, undo/redo, engine disconnect, reader restart, window/device deletion, teardown and failed accessibility communication remain U. No exact announcement, timing, pixel or resource tolerance is assigned. [Source accessibility-and-keyboard-navigation](#source-accessibility-and-keyboard-navigation).

## Cases and fixtures

All42 [cases](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/cases.json)
are finite definitions with [explicit prerequisites](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/fixtures.json),
not executed target observations. The discovery comparison checks documentation
extraction only. Unsupported/missing prerequisites remain unexecuted. Unknown
case outcomes are null; escape cancellation is scoped to the documented edit.

| Case | Requirement suffix | Kind | Action | Predicate or unknown |
| --- | --- | --- | --- | --- |
| NAV-001 | 001 | scope | F1: inspect captured support limitations for reader/device/browser/MPE/Max scope | Documentary limited scope only; no all-controls accessibility pass |
| NAV-002 | 002 | positive | F1: focus two known enabled main-window controls; global Use Tab on, press Tab then Shift-Tab | Next then previous focused control within the established area |
| NAV-003 | 002 | negative | F1: global Use Tab off, focused main Session view outside text/modal/editor; press Tab twice | View switches Session→Arrangement→Session; exact focus restoration U |
| NAV-004 | 003 | boundary | F1: known finite area with confirmed first/last enabled controls; Wrap on; Tab from last then Shift-Tab from first | Focus wraps to first then last respectively; unsupported area boundaries U |
| NAV-005 | 003 | positive | F1: two adjacent tracks with matching visible mixer controls; focus one control and invoke next/previous neighbor chords | Same-row control on neighboring track is focused |
| NAV-006 | 004 | positive | F1: Arrangement selected clip/time selection with movement option on, horizontal arrows | Movement behavior dispatched; exact displacement delegated to Arrangement |
| NAV-007 | 004 | negative | F1: movement option off, nonempty time selection from beat2 to4; left, reset same selection, right | Selection collapses to start then end respectively |
| NAV-008 | 005 | positive | F1: global Tab mode off; open Settings, focus a known enabled control, Tab then Shift-Tab | Settings traversal works regardless of global Tab mode |
| NAV-009 | 005 | positive | F1: known Settings toggle initially off, press Enter; known chooser focus, arrow down/up | Toggle changes state; chooser traverses available choices; step/wrap U |
| NAV-010 | 006 | positive | F1: Settings open; use platform page-navigation chords and focused chooser arrows | Settings page selection changes through documented controls |
| NAV-011 | 006 | boundary | F1: first control on current Settings page, press Shift-Tab, then Escape | Focus returns to page chooser, then Settings closes; no setting rollback implied |
| NAV-012 | 007 | persistence | F1: choose different installed preferred language in Settings then inspect before/after authorized future restart | Restart is required for language application; restart/session details U |
| NAV-013 | 008 | positive | F2: supported reader running; Options Accessibility inspect menu/minmax/time announcement options, enable applicable help-text setting | Documented options/help access exist; exact speech wording/timing/support coverage U |
| NAV-014 | 009 | positive | F1: invoke Alt/Option0..7 separately with applicable main views present and focus elsewhere | Control Bar, Session, Arrangement, Clip editor, Device, Browser, Groove Pool, Learn focused respectively |
| NAV-015 | 009 | persistence | F1: focus a known Control Bar control C, leave to present Session view, invoke Control Bar focus | Focus returns to C; no other-view memory claim |
| NAV-016 | 010 | positive | F1: Session with2tracks/2scenes and existing clips; traverse titles/slots/scenes with arrows, Tab to mixer | Navigation reaches documented regions; clip launching not tested by focus alone |
| NAV-017 | 010 | positive | F1: focus volume control on named Session track A; press Escape | Track A title receives focus |
| NAV-018 | 011 | positive | F1: Arrangement with clips and locator on known nonzero positions; content lane focused, use grid arrows then modified edge navigation | Navigation follows grid and previous/next edge/locator roles; exact tie U |
| NAV-019 | 011 | cancel | F1: insert marker at known clip edge; Enter, horizontal arrow once, Escape | Pending length edit cancelled by documented gesture; exact restored bytes/history U |
| NAV-020 | 011 | positive | F1: same edge-edit setup; Enter, horizontal arrow once, Enter | Pending edge edit confirmed; resulting boundary owned by Arrangement |
| NAV-021 | 012 | positive | F1: first open fresh audio clip, then first open fresh MIDI clip in appropriate tracks | Sample versus MIDI Note Editor selected respectively |
| NAV-022 | 012 | positive | F1: active clip editor present, focus elsewhere; invoke Alt/Option3 then panel-focus chord | Active editor then clip panels receive focus |
| NAV-023 | 013 | positive | F2: reader with simple supported device chain, known active controls; left/right between devices, Tab/Shift-Tab controls | Device groups and documented traversal accessible; complex/third-party surfaces outside this predicate |
| NAV-024 | 014 | positive | F1: Browser search focused, sequential Tab with filter-view shown versus hidden; separately Down from search | Focus reaches documented toggle/menu/sidebar/filter-or-content path; Down reaches content |
| NAV-025 | 014 | positive | F1: browser sidebar focused; up/down label, right/left to content, known folder expand/collapse and Shift selection | Documented region/label/folder/selection navigation; tagging/filter speech unsupported in source |
| NAV-026 | 015 | positive | F1: Groove Pool with one assigned groove and accepted parameter values; Tab/Shift-Tab then up/down | Parameter navigation/editing eligibility; groove math delegated |
| NAV-027 | 015 | positive | F1: Learn view available, invoke Alt/Option7 | Learn view focused; lesson availability/network outcomes U |
| NAV-028 | 016 | positive | F3: envelope at valid non-breakpoint grid position, Enter, move pending point, Enter | New point creation/move/confirm path; numeric interpolation U |
| NAV-029 | 016 | positive | F3: at least3 distinct-time existing breakpoints; Alt/Option-left/right from middle location | Focus/marker navigates previous/next breakpoint; same-time ties U |
| NAV-030 | 017 | positive | F3: existing selected breakpoint with accepted value; type different accepted value, Enter | Value edit confirmed and point deselected; parser/rounding U |
| NAV-031 | 017 | cancel | F3: same accepted point/value, begin alternate accepted value edit, Escape | Edit cancelled and point deselected; exact byte/history outcomes U |
| NAV-032 | 017 | positive | F3: point selected, Tab/Shift-Tab to neighbors; select one and Delete | Next/previous selection and selected-point deletion; multi/equal-time U |
| NAV-033 | 018 | positive | F3: track with known automated parameter A and unautomated B; cycle Alt/Option-up/down versus Shift-added variant | First traverses automated envelopes; second includes unautomated parameters; exact order/wrap U |
| NAV-034 | 019 | discovery | Retained source table extraction: compare all292 command and platform-cell texts with27 original tables | Exact documented binding inventory and locators only; no command dispatch or target coverage pass |
| NAV-035 | 020 | negative | F1: unselected/hidden/disabled controls, text input and modal/plugin editor intercept same chords; record focus/state | U: context interception/disabled-command result absent |
| NAV-036 | 020 | boundary | F1: empty Set/area, first/last control with Wrap off, empty chooser and equal-time breakpoints | U: full applicable area/order/tie/boundary outcomes absent |
| NAV-037 | 020 | malformed | F3: type invalid/out-of-domain/nonfinite breakpoint number then confirm/cancel | U: parser/reject/clamp/history/focus outcome absent |
| NAV-038 | 020 | interaction | F1: change keyboard layout/IME, Computer MIDI keyboard and key-map assignments for overlapping keys | U: precedence/remap/platform availability absent |
| NAV-039 | 021 | error | F2: unavailable reader/accessibility protocol failure or device disconnect during focus traversal | U: announcements, recovery, fallback and control state absent |
| NAV-040 | 021 | undo | F1/F3: edit focus/selection/point/settings, request undo/redo and inspect restored values/focus | U: undo grouping/scope/focus and settings survival absent |
| NAV-041 | 021 | persistence | F1/F2: save/reopen with nondefault Tab/Wrap/focused areas and reader options | U: per-setting/per-area persistence and focus restoration absent |
| NAV-042 | 021 | teardown | F1/F2: focused control/point/window/device disappears or application closes with active reader/edit | U: focus fallback, pending edit/speech/resources and shutdown outcome absent |

## Shortcut inventory and remaining obligations

[292 table rows](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/shortcut-bindings.json)
retain command label, platform-cell syntax and exact source table/row/HTML line.
They include alternative chords, pointer gestures, contextual duplicates and
post-target/version-uncertain commands; do not treat them as292 unique features,
closed requirements or passing scenarios. Reconcile each binding's applicability,
context and canonical action before proposing an executable command test. The
catalog deliberately preserves source syntax; whitespace is not parsed into an
unproven shortcut/chord language.

Full focus order, every device's accessible tree, unsupported-feature evolution,
protocol failures, UI contrast geometry, OS reader interoperability and all listed
error/undo/save/reopen/teardown combinations remain unknown. General Clip View,
UI layout and every menu/shortcut action remain larger obligations. This packet
closes none of those families or exact-build applicability questions.

## Analyst source appendix

Two official chapters were retained with URL, UTC time, size and SHA-256 in
[sources.json](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/sources.json).
Accessibility HTML digest `39757eb6da631c78fa61dd39be02aec3f07af2e623dce159ee9e468fd3cea2a8`; shortcut HTML digest
`9a754776da08e1925d73ee50366264aa1f2b03b11bebafeda0ebacecabfce908`.
No figures inspected and no generic screen-reader support assumed from prose.

### Source accessibility-and-keyboard-navigation

[accessibility-and-keyboard-navigation](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/accessibility-and-keyboard-navigation-2026-10-19.html#accessibility-and-keyboard-navigation), retained HTML line 280; exact digest above.

### Source arrangement-view---alt-2-win--option-2-mac

[arrangement-view---alt-2-win--option-2-mac](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/accessibility-and-keyboard-navigation-2026-10-19.html#arrangement-view---alt-2-win--option-2-mac), retained HTML line 280; exact digest above.

### Source browser---alt-5-win--option-5-mac

[browser---alt-5-win--option-5-mac](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/accessibility-and-keyboard-navigation-2026-10-19.html#browser---alt-5-win--option-5-mac), retained HTML line 280; exact digest above.

### Source clip-view---alt-3-win--option-3-mac

[clip-view---alt-3-win--option-3-mac](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/accessibility-and-keyboard-navigation-2026-10-19.html#clip-view---alt-3-win--option-3-mac), retained HTML line 280; exact digest above.

### Source device-view---alt-4-win--option-4-mac

[device-view---alt-4-win--option-4-mac](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/accessibility-and-keyboard-navigation-2026-10-19.html#device-view---alt-4-win--option-4-mac), retained HTML line 280; exact digest above.

### Source groove-pool---alt-6-win--option-6-mac

[groove-pool---alt-6-win--option-6-mac](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/accessibility-and-keyboard-navigation-2026-10-19.html#groove-pool---alt-6-win--option-6-mac), retained HTML line 280; exact digest above.

### Source menu-and-keyboard-navigation-settings

[menu-and-keyboard-navigation-settings](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/accessibility-and-keyboard-navigation-2026-10-19.html#menu-and-keyboard-navigation-settings), retained HTML line 280; exact digest above.

### Source navigate-menu

[navigate-menu](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/accessibility-and-keyboard-navigation-2026-10-19.html#navigate-menu), retained HTML line 280; exact digest above.

### Source navigating-between-breakpoints

[navigating-between-breakpoints](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/accessibility-and-keyboard-navigation-2026-10-19.html#navigating-between-breakpoints), retained HTML line 280; exact digest above.

### Source navigating-in-live

[navigating-in-live](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/accessibility-and-keyboard-navigation-2026-10-19.html#navigating-in-live), retained HTML line 280; exact digest above.

### Source options-menu

[options-menu](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/accessibility-and-keyboard-navigation-2026-10-19.html#options-menu), retained HTML line 280; exact digest above.

### Source selecting-and-editing-breakpoints

[selecting-and-editing-breakpoints](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/accessibility-and-keyboard-navigation-2026-10-19.html#selecting-and-editing-breakpoints), retained HTML line 312; exact digest above.

### Source session-view---alt-1-win--option-1-mac

[session-view---alt-1-win--option-1-mac](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/accessibility-and-keyboard-navigation-2026-10-19.html#session-view---alt-1-win--option-1-mac), retained HTML line 280; exact digest above.

### Source settings-menu

[settings-menu](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/accessibility-and-keyboard-navigation-2026-10-19.html#settings-menu), retained HTML line 280; exact digest above.

### Source switching-between-automation-envelopes-in-arrangement-view

[switching-between-automation-envelopes-in-arrangement-view](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/accessibility-and-keyboard-navigation-2026-10-19.html#switching-between-automation-envelopes-in-arrangement-view), retained HTML line 332; exact digest above.

### Source using-tab-for-navigation

[using-tab-for-navigation](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/accessibility-and-keyboard-navigation-2026-10-19.html#using-tab-for-navigation), retained HTML line 280; exact digest above.

