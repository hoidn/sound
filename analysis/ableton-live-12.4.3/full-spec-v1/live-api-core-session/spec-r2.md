---
id: SPEC-LIVE-API-CORE-SESSION
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 2
target: Ableton Live 12 Suite 12.4.3; public LOM index 12.4.5 applicability U
---

# Public Live API core and Session direct members

## Scope and authority

This partial F-05/F-08 documentary contract maps direct declarations in ten
retained public references: Application, Application.View, Song, Song.View,
Track, Track.View, Scene, ClipSlot, CuePoint and TakeLane. It does not flatten
inheritance or complete these classes, the 45-reference API or arbitrary Max
compatibility. [Research](../research/live-api-core-session.md) retains exact
source contexts; [coverage design](../research/full-live-specification-design.md)
governs closure.

**D-current-public/target-U:** the immutable R1 inventory's index explicitly
declares Live **12.4.5**, after target12.4.3. Source signatures/access/context
are documentary, not runtime observations. All API/numeric/message/timing/signal
documentary expected/comparison fields are null and source_claim is separate.
Every target expectation/comparison is null, grade U and unexecuted. Source
examples, bounds and defaults are not target numeric or serialization laws.
No source script/example/patch, Live API call, Max, hardware, original/native
code, installation or candidate was run.

## Existing owners and future prerequisites

[Bridge workflows](live-api-bridge-workflows.md) owns initialization, navigation,
IDs, get/set/call/observe, notification and remote roles; this page maps only
the selected per-member declarations. [Set structure](live-set-structure.md)
retains storage and identifiers; [transport](transport-state.md),
[playback](playback-core.md) and [clip launch](clip-launch.md) retain finite
value/grid/timing laws. REQ-CLIP-LAUNCH-020/021/022/023 remain unknown in their
native/runtime scopes. Public API enum numbers, sentinel values, units and
names do not equate to stored/native fields or labels.

[Session](session-view-workflows.md), [launch workflows](session-launch-workflows.md),
[Arrangement](arrangement-editing.md), [recording/comping](recording-comping.md),
[routing](routing-monitoring-latency.md), [racks](device-racks.md),
[device hosting](bundled-device-hosting.md), [Browser](browser-workflows.md),
[keyboard navigation](keyboard-navigation.md), [workspace](application-workspace.md)
and [project/media](project-media-workflows.md) retain their UI, track/scene,
record, route, save/history and device operations. API selection is distinct
from UI focus, appointed-device, selected-track and visibility contexts.
[Automation envelopes](automation-envelopes.md) REQ-AUTOMATION-ENVELOPES-013 and
[automation workflows](automation-workflows.md), [mix graph](mix-graph.md),
[mixer values](mixer-values.md), [tuning](tuning-systems.md),
[grooves](groove-workflows.md) and [Push](push-controller-workflows.md) retain
their finite scope and unknowns. No new numeric DSP, pitch, meter calibration,
automation evaluator, UI overwrite/default, storage codec or scheduling law.

Use the [future prerequisites](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/fixtures.json): an independently
valid owned patch/device and actually available initialized API context;
positively resolved eligible object/member, correct track kind, actual admitted
arguments, explicit transport/record/selection/freeze/preferences and productive
read/change baseline. Names, booleans, values and object identities require
member-specific admissibility. For record/launch/meter/audio/automation probes,
require active nonempty source, eligible arm/monitor/record path, nonzero
gain/send/wet/amount and nonmuted output. Unsupported hardware, absent members,
zero signal or missing source remains U, never no-effect. No patch or actual
fixture/API result is supplied.

## Denominator and typed contract interpretation

The [denominator ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/denominator.json) preserves the global
45 references/588 explicit direct declarations. This family maps **226 direct
members in ten references: 30 children, 123 properties and 73 functions**.
All226 have member-specific requirements, exact source blocks, typed signatures
where stated, unknown flags and finite cases. Zero selected declarations are
unmapped; **all226 remain incomplete/target-U**. Other35references/362direct
members remain outside this family's mapping; inherited members/root aliases
are an additional unclosed denominator, not silently counted as absent.

The [member ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json) records the exact source
heading/category/URL/HTML line and column, per-member access, value type,
ordered arguments, explicit optionality/default and return type when stated.
Null means unstated, not void, no arguments, required, unsupported or rejected.
An omitted parameter list is not an empty signature. Access lists preserve only
explicit get/set/observe declarations. Function call role comes from its own
Functions section; it supplies no observer/set capability. Publisher types
symbol/unicode/list/dictionary/object/bool/int/long/float remain that vocabulary,
without native width, codec, atom shape or coercion inference. Descriptions
below are retained publisher prose scoped to the exact direct declaration;
source context and unknowns do not acquire an executable comparator.

## Direct-member requirements

## Application

### REQ-LAPI-CORE-001 — Application.view

**D-current-public/target-U.** For the documented Application context, `view` is a direct children declaration with source type `Application.View` and documented get role. No additional member-specific behavior is stated beyond its heading and access declaration. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `Application.View`; access `get`; result type `Application.View`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-APPLICATION member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-APPLICATION:B0002`, `C74-LOM-APPLICATION:B0004`, `C74-LOM-APPLICATION:B0006`, `C74-LOM-APPLICATION:B0007`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-001` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-002 — Application.control_surfaces

**D-current-public/target-U.** For the documented Application context, `control_surfaces` is a direct children declaration with source type `list of ControlSurface` and documented get/observe role. Publisher member description: A list of the control surfaces currently selected in Live's Preferences. If None is selected in any of the slots or the script is inactive (e.g. when Push2 is selected, but no Push is connected), id 0 will be returned at those indices. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `list of ControlSurface`; access `get,observe`; result type `list of ControlSurface`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-APPLICATION member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-APPLICATION:B0002`, `C74-LOM-APPLICATION:B0004`, `C74-LOM-APPLICATION:B0008`, `C74-LOM-APPLICATION:B0009`, `C74-LOM-APPLICATION:B0010`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-002`, `LCS-BRANCH-001` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-003 — Application.current_dialog_button_count

**D-current-public/target-U.** For the documented Application context, `current_dialog_button_count` is a direct properties declaration with source type `int` and documented get role. Publisher member description: The number of buttons in the current message box. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `int`; access `get`; result type `int`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-APPLICATION member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-APPLICATION:B0002`, `C74-LOM-APPLICATION:B0004`, `C74-LOM-APPLICATION:B0012`, `C74-LOM-APPLICATION:B0013`, `C74-LOM-APPLICATION:B0014`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-003` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-004 — Application.current_dialog_message

**D-current-public/target-U.** For the documented Application context, `current_dialog_message` is a direct properties declaration with source type `symbol` and documented get role. Publisher member description: The text of the current message box (empty if no message box is currently shown). The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `symbol`; access `get`; result type `symbol`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-APPLICATION member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-APPLICATION:B0002`, `C74-LOM-APPLICATION:B0004`, `C74-LOM-APPLICATION:B0015`, `C74-LOM-APPLICATION:B0016`, `C74-LOM-APPLICATION:B0017`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-004`, `LCS-BRANCH-002` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-005 — Application.open_dialog_count

**D-current-public/target-U.** For the documented Application context, `open_dialog_count` is a direct properties declaration with source type `int` and documented get/observe role. Publisher member description: The number of dialog boxes shown. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `int`; access `get,observe`; result type `int`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-APPLICATION member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-APPLICATION:B0002`, `C74-LOM-APPLICATION:B0004`, `C74-LOM-APPLICATION:B0018`, `C74-LOM-APPLICATION:B0019`, `C74-LOM-APPLICATION:B0020`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-005` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-006 — Application.average_process_usage

**D-current-public/target-U.** For the documented Application context, `average_process_usage` is a direct properties declaration with source type `float` and documented get/observe role. Publisher member description: Reports Live's average CPU load. Note that Live's CPU meter shows the audio processing load but not Live's overall CPU usage. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `float`; access `get,observe`; result type `float`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-APPLICATION member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-APPLICATION:B0002`, `C74-LOM-APPLICATION:B0004`, `C74-LOM-APPLICATION:B0021`, `C74-LOM-APPLICATION:B0022`, `C74-LOM-APPLICATION:B0023`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-006` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-007 — Application.peak_process_usage

**D-current-public/target-U.** For the documented Application context, `peak_process_usage` is a direct properties declaration with source type `float` and documented get/observe role. Publisher member description: Reports Live's peak CPU load. Note that Live's CPU meter shows the audio processing load but not Live's overall CPU usage. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `float`; access `get,observe`; result type `float`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-APPLICATION member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-APPLICATION:B0002`, `C74-LOM-APPLICATION:B0004`, `C74-LOM-APPLICATION:B0024`, `C74-LOM-APPLICATION:B0025`, `C74-LOM-APPLICATION:B0026`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-007` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-008 — Application.get_bugfix_version

**D-current-public/target-U.** For the documented Application context, `get_bugfix_version` is a direct functions declaration and documented call role. Publisher member description: Returns: the 2 in Live 9.1.2. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `unstated`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-APPLICATION member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-APPLICATION:B0002`, `C74-LOM-APPLICATION:B0004`, `C74-LOM-APPLICATION:B0028`, `C74-LOM-APPLICATION:B0029`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-008` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-009 — Application.get_document

**D-current-public/target-U.** For the documented Application context, `get_document` is a direct functions declaration and documented call role. Publisher member description: Returns: the current Live Set. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `unstated`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-APPLICATION member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-APPLICATION:B0002`, `C74-LOM-APPLICATION:B0004`, `C74-LOM-APPLICATION:B0030`, `C74-LOM-APPLICATION:B0031`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-009` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-010 — Application.get_major_version

**D-current-public/target-U.** For the documented Application context, `get_major_version` is a direct functions declaration and documented call role. Publisher member description: Returns: the 9 in Live 9.1.2. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `unstated`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-APPLICATION member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-APPLICATION:B0002`, `C74-LOM-APPLICATION:B0004`, `C74-LOM-APPLICATION:B0032`, `C74-LOM-APPLICATION:B0033`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-010` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-011 — Application.get_minor_version

**D-current-public/target-U.** For the documented Application context, `get_minor_version` is a direct functions declaration and documented call role. Publisher member description: Returns: the 1 in Live 9.1.2. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `unstated`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-APPLICATION member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-APPLICATION:B0002`, `C74-LOM-APPLICATION:B0004`, `C74-LOM-APPLICATION:B0034`, `C74-LOM-APPLICATION:B0035`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-011` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-012 — Application.get_version_string

**D-current-public/target-U.** For the documented Application context, `get_version_string` is a direct functions declaration and documented call role. Publisher member description: Returns: the text 9.1.2 in Live 9.1.2. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `unstated`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-APPLICATION member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-APPLICATION:B0002`, `C74-LOM-APPLICATION:B0004`, `C74-LOM-APPLICATION:B0036`, `C74-LOM-APPLICATION:B0037`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-012` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-013 — Application.press_current_dialog_button

**D-current-public/target-U.** For the documented Application context, `press_current_dialog_button` is a direct functions declaration and documented call role. Publisher member description: Parameter: index Press the button with the given index in the current dialog box. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `unstated`. Arguments, in source order: `index` (type unstated, optionality unstated).

Evidence: [C74-LOM-APPLICATION member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-APPLICATION:B0002`, `C74-LOM-APPLICATION:B0004`, `C74-LOM-APPLICATION:B0038`, `C74-LOM-APPLICATION:B0039`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-013` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

## Application.View

### REQ-LAPI-CORE-014 — Application.View.browse_mode

**D-current-public/target-U.** For the documented Application.View context, `browse_mode` is a direct properties declaration with source type `bool` and documented get/observe role. Publisher member description: 1 = Hot-Swap Mode is active for any target. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `bool`; access `get,observe`; result type `bool`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-APPLICATION_VIEW member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-APPLICATION_VIEW:B0002`, `C74-LOM-APPLICATION_VIEW:B0004`, `C74-LOM-APPLICATION_VIEW:B0006`, `C74-LOM-APPLICATION_VIEW:B0007`, `C74-LOM-APPLICATION_VIEW:B0008`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-014` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-015 — Application.View.focused_document_view

**D-current-public/target-U.** For the documented Application.View context, `focused_document_view` is a direct properties declaration with source type `unicode` and documented get/observe role. Publisher member description: The name of the currently visible view in the focused Live window ('Session' or 'Arranger'). The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unicode`; access `get,observe`; result type `unicode`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-APPLICATION_VIEW member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-APPLICATION_VIEW:B0002`, `C74-LOM-APPLICATION_VIEW:B0004`, `C74-LOM-APPLICATION_VIEW:B0009`, `C74-LOM-APPLICATION_VIEW:B0010`, `C74-LOM-APPLICATION_VIEW:B0011`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-015` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-016 — Application.View.available_main_views

**D-current-public/target-U.** For the documented Application.View context, `available_main_views` is a direct functions declaration and documented call role. Publisher member description: Returns: view names [list of symbols]. This is a constant list of view names to be used as an argument when calling other functions: Browser Arranger Session Detail Detail/Clip Detail/DeviceChain. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `list of symbols`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-APPLICATION_VIEW member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-APPLICATION_VIEW:B0002`, `C74-LOM-APPLICATION_VIEW:B0004`, `C74-LOM-APPLICATION_VIEW:B0013`, `C74-LOM-APPLICATION_VIEW:B0014`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-016` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-017 — Application.View.focus_view

**D-current-public/target-U.** For the documented Application.View context, `focus_view` is a direct functions declaration and documented call role. Publisher member description: Parameter: view_name Shows named view and focuses on it. You can also pass an empty view_name “ ", which refers to the Arrangement or Session View (whichever is visible in the main window). The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `unstated`. Arguments, in source order: `view_name` (type unstated, optionality unstated).

Evidence: [C74-LOM-APPLICATION_VIEW member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-APPLICATION_VIEW:B0002`, `C74-LOM-APPLICATION_VIEW:B0004`, `C74-LOM-APPLICATION_VIEW:B0015`, `C74-LOM-APPLICATION_VIEW:B0016`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-017` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-018 — Application.View.hide_view

**D-current-public/target-U.** For the documented Application.View context, `hide_view` is a direct functions declaration and documented call role. Publisher member description: Parameter: view_name Hides the named view. You can also pass an empty view_name “ ", which refers to the Arrangement or Session View (whichever is visible in the main window). The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `unstated`. Arguments, in source order: `view_name` (type unstated, optionality unstated).

Evidence: [C74-LOM-APPLICATION_VIEW member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-APPLICATION_VIEW:B0002`, `C74-LOM-APPLICATION_VIEW:B0004`, `C74-LOM-APPLICATION_VIEW:B0017`, `C74-LOM-APPLICATION_VIEW:B0018`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-018` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-019 — Application.View.is_view_visible

**D-current-public/target-U.** For the documented Application.View context, `is_view_visible` is a direct functions declaration and documented call role. Publisher member description: Parameter: view_name Returns: [bool] Whether the specified view is currently visible. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `bool`. Arguments, in source order: `view_name` (type unstated, optionality unstated).

Evidence: [C74-LOM-APPLICATION_VIEW member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-APPLICATION_VIEW:B0002`, `C74-LOM-APPLICATION_VIEW:B0004`, `C74-LOM-APPLICATION_VIEW:B0019`, `C74-LOM-APPLICATION_VIEW:B0020`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-019` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-020 — Application.View.scroll_view

**D-current-public/target-U.** For the documented Application.View context, `scroll_view` is a direct functions declaration and documented call role. Publisher member description: Parameters: direction view_name modifier_pressed direction [int] is 0 = up, 1 = down, 2 = left, 3 = right modifier_pressed [bool] If view_name is "Arranger" and modifier_pressed is 1 and direction is left or right, then the size of the selected time region is modified, otherwise the position of the playback cursor is moved. Not all views are scrollable, and not in all directions. Currently, only the Arranger, Browser, Session, and Detail/DeviceChain views can be scrolled. You can also pass an empty view_name " ", which refers to the Arrangement or Session View (whichever view is visible). The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `unstated`. Arguments, in source order: `direction` (int, optionality unstated); `view_name` (type unstated, optionality unstated); `modifier_pressed` (bool, optionality unstated).

Evidence: [C74-LOM-APPLICATION_VIEW member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-APPLICATION_VIEW:B0002`, `C74-LOM-APPLICATION_VIEW:B0004`, `C74-LOM-APPLICATION_VIEW:B0021`, `C74-LOM-APPLICATION_VIEW:B0022`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-020`, `LCS-BRANCH-003` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-021 — Application.View.show_view

**D-current-public/target-U.** For the documented Application.View context, `show_view` is a direct functions declaration and documented call role. Publisher member description: Parameter: view_name The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `unstated`. Arguments, in source order: `view_name` (type unstated, optionality unstated).

Evidence: [C74-LOM-APPLICATION_VIEW member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-APPLICATION_VIEW:B0002`, `C74-LOM-APPLICATION_VIEW:B0004`, `C74-LOM-APPLICATION_VIEW:B0023`, `C74-LOM-APPLICATION_VIEW:B0024`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-021` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-022 — Application.View.toggle_browse

**D-current-public/target-U.** For the documented Application.View context, `toggle_browse` is a direct functions declaration and documented call role. Publisher member description: Displays the device chain and the browser and activates Hot-Swap Mode for the selected device. Calling this function again deactivates Hot-Swap Mode. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `unstated`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-APPLICATION_VIEW member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-APPLICATION_VIEW:B0002`, `C74-LOM-APPLICATION_VIEW:B0004`, `C74-LOM-APPLICATION_VIEW:B0025`, `C74-LOM-APPLICATION_VIEW:B0026`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-022` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-023 — Application.View.zoom_view

**D-current-public/target-U.** For the documented Application.View context, `zoom_view` is a direct functions declaration and documented call role. Publisher member description: Parameter: direction view_name modifier_pressed direction [int] - 0 = up, 1 = down, 2 = left, 3 = right modifier_pressed [bool] If view_name is 'Arrangement', modifier_pressed is 1, and direction is left or right, then the size of the selected time region is modified, otherwise the position of the playback cursor is moved. If view_name is Arrangement and modifier_pressed is 1 and direction is up or down, then only the height of the highlighted track is changed, otherwise the height of all tracks is changed. Only the Arrangement and Session Views can be zoomed. For Session View, the behaviour of zoom_view is identical to scroll_view. You can also pass an empty view_name “ ", which refers to the Arrangement or Session View (whichever is visible in the main window). The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `unstated`. Arguments, in source order: `direction` (int, optionality unstated); `view_name` (type unstated, optionality unstated); `modifier_pressed` (bool, optionality unstated).

Evidence: [C74-LOM-APPLICATION_VIEW member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-APPLICATION_VIEW:B0002`, `C74-LOM-APPLICATION_VIEW:B0004`, `C74-LOM-APPLICATION_VIEW:B0027`, `C74-LOM-APPLICATION_VIEW:B0028`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-023`, `LCS-BRANCH-004` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

## Song

### REQ-LAPI-CORE-024 — Song.cue_points

**D-current-public/target-U.** For the documented Song context, `cue_points` is a direct children declaration with source type `list of CuePoint` and documented get/observe role. Publisher member description: Cue points are the markers in the Arrangement to which you can jump. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `list of CuePoint`; access `get,observe`; result type `list of CuePoint`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0006`, `C74-LOM-SONG:B0007`, `C74-LOM-SONG:B0008`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-024` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-025 — Song.return_tracks

**D-current-public/target-U.** For the documented Song context, `return_tracks` is a direct children declaration with source type `list of Track` and documented get/observe role. No additional member-specific behavior is stated beyond its heading and access declaration. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `list of Track`; access `get,observe`; result type `list of Track`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0009`, `C74-LOM-SONG:B0010`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-025` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-026 — Song.scenes

**D-current-public/target-U.** For the documented Song context, `scenes` is a direct children declaration with source type `list of Scene` and documented get/observe role. No additional member-specific behavior is stated beyond its heading and access declaration. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `list of Scene`; access `get,observe`; result type `list of Scene`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0011`, `C74-LOM-SONG:B0012`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-026` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-027 — Song.tracks

**D-current-public/target-U.** For the documented Song context, `tracks` is a direct children declaration with source type `list of Track` and documented get/observe role. No additional member-specific behavior is stated beyond its heading and access declaration. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `list of Track`; access `get,observe`; result type `list of Track`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0013`, `C74-LOM-SONG:B0014`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-027` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-028 — Song.visible_tracks

**D-current-public/target-U.** For the documented Song context, `visible_tracks` is a direct children declaration with source type `list of Track` and documented get/observe role. Publisher member description: A track is visible if it's not part of a folded group. If a track is scrolled out of view it's still considered visible. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `list of Track`; access `get,observe`; result type `list of Track`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0015`, `C74-LOM-SONG:B0016`, `C74-LOM-SONG:B0017`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-028` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-029 — Song.master_track

**D-current-public/target-U.** For the documented Song context, `master_track` is a direct children declaration with source type `Track` and documented get role. No additional member-specific behavior is stated beyond its heading and access declaration. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `Track`; access `get`; result type `Track`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0018`, `C74-LOM-SONG:B0019`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-029` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-030 — Song.view

**D-current-public/target-U.** For the documented Song context, `view` is a direct children declaration with source type `Song.View` and documented get role. No additional member-specific behavior is stated beyond its heading and access declaration. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `Song.View`; access `get`; result type `Song.View`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0020`, `C74-LOM-SONG:B0021`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-030` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-031 — Song.groove_pool

**D-current-public/target-U.** For the documented Song context, `groove_pool` is a direct children declaration with source type `GroovePool` and documented get role. Publisher member description: Live's groove pool. Available since Live 11.0. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `GroovePool`; access `get`; result type `GroovePool`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0022`, `C74-LOM-SONG:B0023`, `C74-LOM-SONG:B0024`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-031` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-032 — Song.tuning_system

**D-current-public/target-U.** For the documented Song context, `tuning_system` is a direct children declaration with source type `TuningSystem` and documented get/observe role. Publisher member description: Live's currently active tuning system. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `TuningSystem`; access `get,observe`; result type `TuningSystem`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0025`, `C74-LOM-SONG:B0026`, `C74-LOM-SONG:B0027`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-032` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-033 — Song.appointed_device

**D-current-public/target-U.** For the documented Song context, `appointed_device` is a direct properties declaration with source type `Device` and documented get/observe role. Publisher member description: The appointed device is the one used by a control surface unless the control surface itself chooses which device to use. It is marked by a blue hand. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `Device`; access `get,observe`; result type `Device`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0029`, `C74-LOM-SONG:B0030`, `C74-LOM-SONG:B0031`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-033` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-034 — Song.arrangement_overdub

**D-current-public/target-U.** For the documented Song context, `arrangement_overdub` is a direct properties declaration with source type `bool` and documented get/set/observe role. Publisher member description: Get/set the state of the MIDI Arrangement Overdub button. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `bool`; access `get,set,observe`; result type `bool`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0032`, `C74-LOM-SONG:B0033`, `C74-LOM-SONG:B0034`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-034` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-035 — Song.back_to_arranger

**D-current-public/target-U.** For the documented Song context, `back_to_arranger` is a direct properties declaration with source type `bool` and documented get/set/observe role. Publisher member description: Get/set/observe the current state of the Back to Arrangement button located in Live's transport bar (1 = highlighted). This button is used to indicate that the current state of the playback differs from what is stored in the Arrangement. Setting this property to 0 will make Live go back to playing the content of the arrangement. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `bool`; access `get,set,observe`; result type `bool`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0035`, `C74-LOM-SONG:B0036`, `C74-LOM-SONG:B0037`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-035` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-036 — Song.can_capture_midi

**D-current-public/target-U.** For the documented Song context, `can_capture_midi` is a direct properties declaration with source type `bool` and documented get/observe role. Publisher member description: 1 = Recently played MIDI material exists that can be captured into a Live Track. See capture_midi. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `bool`; access `get,observe`; result type `bool`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0038`, `C74-LOM-SONG:B0039`, `C74-LOM-SONG:B0040`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-036` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-037 — Song.can_jump_to_next_cue

**D-current-public/target-U.** For the documented Song context, `can_jump_to_next_cue` is a direct properties declaration with source type `bool` and documented get/observe role. Publisher member description: 0 = there is no cue point to the right of the current one, or none at all. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `bool`; access `get,observe`; result type `bool`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0041`, `C74-LOM-SONG:B0042`, `C74-LOM-SONG:B0043`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-037` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-038 — Song.can_jump_to_prev_cue

**D-current-public/target-U.** For the documented Song context, `can_jump_to_prev_cue` is a direct properties declaration with source type `bool` and documented get/observe role. Publisher member description: 0 = there is no cue point to the left of the current one, or none at all. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `bool`; access `get,observe`; result type `bool`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0044`, `C74-LOM-SONG:B0045`, `C74-LOM-SONG:B0046`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-038` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-039 — Song.can_redo

**D-current-public/target-U.** For the documented Song context, `can_redo` is a direct properties declaration with source type `bool` and documented get role. Publisher member description: 1 = there is something in the history to redo. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `bool`; access `get`; result type `bool`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0047`, `C74-LOM-SONG:B0048`, `C74-LOM-SONG:B0049`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-039` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-040 — Song.can_undo

**D-current-public/target-U.** For the documented Song context, `can_undo` is a direct properties declaration with source type `bool` and documented get role. Publisher member description: 1 = there is something in the history to undo. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `bool`; access `get`; result type `bool`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0050`, `C74-LOM-SONG:B0051`, `C74-LOM-SONG:B0052`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-040` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-041 — Song.clip_trigger_quantization

**D-current-public/target-U.** For the documented Song context, `clip_trigger_quantization` is a direct properties declaration with source type `int` and documented get/set/observe role. Publisher member description: Reflects the quantization setting in the transport bar. 0 = None 1 = 8 Bars 2 = 4 Bars 3 = 2 Bars 4 = 1 Bar 5 = 1/2 6 = 1/2T 7 = 1/4 8 = 1/4T 9 = 1/8 10 = 1/8T 11 = 1/16 12 = 1/16T 13 = 1/32 The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `int`; access `get,set,observe`; result type `int`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0053`, `C74-LOM-SONG:B0054`, `C74-LOM-SONG:B0055`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-041` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-042 — Song.count_in_duration

**D-current-public/target-U.** For the documented Song context, `count_in_duration` is a direct properties declaration with source type `int` and documented get/observe role. Publisher member description: The duration of the Metronome's Count-In setting as an index, mapped as follows: 0 = None 1 = 1 Bar 2 = 2 Bars 3 = 4 Bars The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `int`; access `get,observe`; result type `int`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0056`, `C74-LOM-SONG:B0057`, `C74-LOM-SONG:B0058`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-042` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-043 — Song.current_song_time

**D-current-public/target-U.** For the documented Song context, `current_song_time` is a direct properties declaration with source type `float` and documented get/set/observe role. Publisher member description: The playing position in the Live Set, in beats. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `float`; access `get,set,observe`; result type `float`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0059`, `C74-LOM-SONG:B0060`, `C74-LOM-SONG:B0061`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-043` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-044 — Song.exclusive_arm

**D-current-public/target-U.** For the documented Song context, `exclusive_arm` is a direct properties declaration with source type `bool` and documented get role. Publisher member description: Current status of the exclusive Arm option set in the Live preferences. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `bool`; access `get`; result type `bool`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0062`, `C74-LOM-SONG:B0063`, `C74-LOM-SONG:B0064`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-044` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-045 — Song.exclusive_solo

**D-current-public/target-U.** For the documented Song context, `exclusive_solo` is a direct properties declaration with source type `bool` and documented get role. Publisher member description: Current status of the exclusive Solo option set in the Live preferences. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `bool`; access `get`; result type `bool`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0065`, `C74-LOM-SONG:B0066`, `C74-LOM-SONG:B0067`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-045` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-046 — Song.file_path

**D-current-public/target-U.** For the documented Song context, `file_path` is a direct properties declaration with source type `symbol` and documented get role. Publisher member description: The path to the current Live Set, in OS-native format. If the Live Set hasn't been saved, the path is empty. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `symbol`; access `get`; result type `symbol`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0068`, `C74-LOM-SONG:B0069`, `C74-LOM-SONG:B0070`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-046` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-047 — Song.groove_amount

**D-current-public/target-U.** For the documented Song context, `groove_amount` is a direct properties declaration with source type `float` and documented get/set/observe role. Publisher member description: The groove amount from the current set's groove pool (0. - 1.0). The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `float`; access `get,set,observe`; result type `float`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0071`, `C74-LOM-SONG:B0072`, `C74-LOM-SONG:B0073`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-047` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-048 — Song.is_ableton_link_enabled

**D-current-public/target-U.** For the documented Song context, `is_ableton_link_enabled` is a direct properties declaration with source type `bool` and documented get/set/observe role. Publisher member description: Enable/disable Ableton Link. The Link toggle in the Live's transport bar must be visible to enable Link. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `bool`; access `get,set,observe`; result type `bool`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0074`, `C74-LOM-SONG:B0075`, `C74-LOM-SONG:B0076`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-048` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-049 — Song.is_ableton_link_start_stop_sync_enabled

**D-current-public/target-U.** For the documented Song context, `is_ableton_link_start_stop_sync_enabled` is a direct properties declaration with source type `bool` and documented get/set/observe role. Publisher member description: Enable/disable Ableton Link Start Stop Sync. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `bool`; access `get,set,observe`; result type `bool`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0077`, `C74-LOM-SONG:B0078`, `C74-LOM-SONG:B0079`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-049` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-050 — Song.is_counting_in

**D-current-public/target-U.** For the documented Song context, `is_counting_in` is a direct properties declaration with source type `bool` and documented get/observe role. Publisher member description: 1 = the Metronome is currently counting in. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `bool`; access `get,observe`; result type `bool`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0080`, `C74-LOM-SONG:B0081`, `C74-LOM-SONG:B0082`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-050` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-051 — Song.is_playing

**D-current-public/target-U.** For the documented Song context, `is_playing` is a direct properties declaration with source type `bool` and documented get/set/observe role. Publisher member description: Get/set if Live's transport is running. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `bool`; access `get,set,observe`; result type `bool`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0083`, `C74-LOM-SONG:B0084`, `C74-LOM-SONG:B0085`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-051` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-052 — Song.last_event_time

**D-current-public/target-U.** For the documented Song context, `last_event_time` is a direct properties declaration with source type `float` and documented get role. Publisher member description: The beat time of the last event (i.e. automation breakpoint, clip end, cue point, loop end) in the Arrangement. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `float`; access `get`; result type `float`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0086`, `C74-LOM-SONG:B0087`, `C74-LOM-SONG:B0088`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-052` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-053 — Song.loop

**D-current-public/target-U.** For the documented Song context, `loop` is a direct properties declaration with source type `bool` and documented get/set/observe role. Publisher member description: Get/set the enabled state of the Arrangement loop. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `bool`; access `get,set,observe`; result type `bool`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0089`, `C74-LOM-SONG:B0090`, `C74-LOM-SONG:B0091`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-053` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-054 — Song.loop_length

**D-current-public/target-U.** For the documented Song context, `loop_length` is a direct properties declaration with source type `float` and documented get/set/observe role. Publisher member description: Arrangement loop length in beats. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `float`; access `get,set,observe`; result type `float`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0092`, `C74-LOM-SONG:B0093`, `C74-LOM-SONG:B0094`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-054` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-055 — Song.loop_start

**D-current-public/target-U.** For the documented Song context, `loop_start` is a direct properties declaration with source type `float` and documented get/set/observe role. Publisher member description: Arrangement loop start in beats. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `float`; access `get,set,observe`; result type `float`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0095`, `C74-LOM-SONG:B0096`, `C74-LOM-SONG:B0097`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-055` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-056 — Song.metronome

**D-current-public/target-U.** For the documented Song context, `metronome` is a direct properties declaration with source type `bool` and documented get/set/observe role. Publisher member description: Get/set the enabled state of the metronome. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `bool`; access `get,set,observe`; result type `bool`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0098`, `C74-LOM-SONG:B0099`, `C74-LOM-SONG:B0100`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-056` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-057 — Song.midi_recording_quantization

**D-current-public/target-U.** For the documented Song context, `midi_recording_quantization` is a direct properties declaration with source type `int` and documented get/set/observe role. Publisher member description: Get/set the current Record Quantization value. 0 = None 1 = 1/4 2 = 1/8 3 = 1/8T 4 = 1/8 + 1/8T 5 = 1/16 6 = 1/16T 7 = 1/16 + 1/16T 8 = 1/32 The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `int`; access `get,set,observe`; result type `int`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0101`, `C74-LOM-SONG:B0102`, `C74-LOM-SONG:B0103`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-057` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-058 — Song.name

**D-current-public/target-U.** For the documented Song context, `name` is a direct properties declaration with source type `symbol` and documented get role. Publisher member description: The name of the current Live Set. If the Live Set hasn't been saved, the name is empty. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `symbol`; access `get`; result type `symbol`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0104`, `C74-LOM-SONG:B0105`, `C74-LOM-SONG:B0106`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-058` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-059 — Song.nudge_down

**D-current-public/target-U.** For the documented Song context, `nudge_down` is a direct properties declaration with source type `bool` and documented get/set/observe role. Publisher member description: 1 = the Tempo Nudge Down button in the transport bar is currently pressed. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `bool`; access `get,set,observe`; result type `bool`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0107`, `C74-LOM-SONG:B0108`, `C74-LOM-SONG:B0109`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-059` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-060 — Song.nudge_up

**D-current-public/target-U.** For the documented Song context, `nudge_up` is a direct properties declaration with source type `bool` and documented get/set/observe role. Publisher member description: 1 = the Tempo Nudge Up button in the transport bar is currently pressed. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `bool`; access `get,set,observe`; result type `bool`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0110`, `C74-LOM-SONG:B0111`, `C74-LOM-SONG:B0112`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-060` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-061 — Song.tempo_follower_enabled

**D-current-public/target-U.** For the documented Song context, `tempo_follower_enabled` is a direct properties declaration with source type `bool` and documented get/set/observe role. Publisher member description: 1 = the Tempo Follower controls the tempo. The Tempo Follower Toggle must be made visible in the preferences for this property to be effective. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `bool`; access `get,set,observe`; result type `bool`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0113`, `C74-LOM-SONG:B0114`, `C74-LOM-SONG:B0115`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-061` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-062 — Song.overdub

**D-current-public/target-U.** For the documented Song context, `overdub` is a direct properties declaration with source type `bool` and documented get/set/observe role. Publisher member description: 1 = MIDI Arrangement Overdub is enabled in the transport. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `bool`; access `get,set,observe`; result type `bool`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0116`, `C74-LOM-SONG:B0117`, `C74-LOM-SONG:B0118`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-062` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-063 — Song.punch_in

**D-current-public/target-U.** For the documented Song context, `punch_in` is a direct properties declaration with source type `bool` and documented get/set/observe role. Publisher member description: 1 = the Punch-In button is enabled in the transport. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `bool`; access `get,set,observe`; result type `bool`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0119`, `C74-LOM-SONG:B0120`, `C74-LOM-SONG:B0121`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-063` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-064 — Song.punch_out

**D-current-public/target-U.** For the documented Song context, `punch_out` is a direct properties declaration with source type `bool` and documented get/set/observe role. Publisher member description: 1 = the Punch-Out button is enabled in the transport. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `bool`; access `get,set,observe`; result type `bool`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0122`, `C74-LOM-SONG:B0123`, `C74-LOM-SONG:B0124`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-064` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-065 — Song.re_enable_automation_enabled

**D-current-public/target-U.** For the documented Song context, `re_enable_automation_enabled` is a direct properties declaration with source type `bool` and documented get/observe role. Publisher member description: 1 = the Re-Enable Automation button is on. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `bool`; access `get,observe`; result type `bool`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0125`, `C74-LOM-SONG:B0126`, `C74-LOM-SONG:B0127`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-065` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-066 — Song.record_mode

**D-current-public/target-U.** For the documented Song context, `record_mode` is a direct properties declaration with source type `bool` and documented get/set/observe role. Publisher member description: 1 = the Arrangement Record button is on. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `bool`; access `get,set,observe`; result type `bool`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0128`, `C74-LOM-SONG:B0129`, `C74-LOM-SONG:B0130`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-066` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-067 — Song.root_note

**D-current-public/target-U.** For the documented Song context, `root_note` is a direct properties declaration with source type `int` and documented get/set/observe role. Publisher member description: The root note of the scale currently selected in Live. The root note can be a number between 0 and 11, where 0 = C and 11 = B. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `int`; access `get,set,observe`; result type `int`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0131`, `C74-LOM-SONG:B0132`, `C74-LOM-SONG:B0133`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-067` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-068 — Song.scale_intervals

**D-current-public/target-U.** For the documented Song context, `scale_intervals` is a direct properties declaration with source type `list` and documented get/observe role. Publisher member description: A list of integers representing the intervals in Live's current scale (see scale_name and scale_mode). An interval is expressed as the difference between the scale degree at the list index and the first scale degree. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `list`; access `get,observe`; result type `list`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0134`, `C74-LOM-SONG:B0135`, `C74-LOM-SONG:B0136`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-068` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-069 — Song.scale_mode

**D-current-public/target-U.** For the documented Song context, `scale_mode` is a direct properties declaration with source type `bool` and documented get/set/observe role. Publisher member description: Access to the Scale Mode setting in Live. When on, key tracks that belong to the currently selected scale are highlighted in Live's MIDI Note Editor, and pitch-based parameters in MIDI Tools and Devices can be edited in scale degrees rather than semitones. See also root_note, scale_name, and scale_intervals. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `bool`; access `get,set,observe`; result type `bool`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0137`, `C74-LOM-SONG:B0138`, `C74-LOM-SONG:B0139`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-069` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-070 — Song.scale_name

**D-current-public/target-U.** For the documented Song context, `scale_name` is a direct properties declaration with source type `unicode` and documented get/set/observe role. Publisher member description: The name of the scale selected in Live, as displayed in the Current Scale Name chooser. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unicode`; access `get,set,observe`; result type `unicode`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0140`, `C74-LOM-SONG:B0141`, `C74-LOM-SONG:B0142`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-070` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-071 — Song.select_on_launch

**D-current-public/target-U.** For the documented Song context, `select_on_launch` is a direct properties declaration with source type `bool` and documented get role. Publisher member description: 1 = the "Select on Launch" option is set in Live's preferences. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `bool`; access `get`; result type `bool`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0143`, `C74-LOM-SONG:B0144`, `C74-LOM-SONG:B0145`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-071` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-072 — Song.session_automation_record

**D-current-public/target-U.** For the documented Song context, `session_automation_record` is a direct properties declaration with source type `bool` and documented get/set/observe role. Publisher member description: The state of the Automation Arm button. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `bool`; access `get,set,observe`; result type `bool`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0146`, `C74-LOM-SONG:B0147`, `C74-LOM-SONG:B0148`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-072` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-073 — Song.session_record

**D-current-public/target-U.** For the documented Song context, `session_record` is a direct properties declaration with source type `bool` and documented get/set/observe role. Publisher member description: The state of the Session Overdub button. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `bool`; access `get,set,observe`; result type `bool`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0149`, `C74-LOM-SONG:B0150`, `C74-LOM-SONG:B0151`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-073` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-074 — Song.session_record_status

**D-current-public/target-U.** For the documented Song context, `session_record_status` is a direct properties declaration with source type `int` and documented get/observe role. Publisher member description: Reflects the state of the Session Record button. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `int`; access `get,observe`; result type `int`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0152`, `C74-LOM-SONG:B0153`, `C74-LOM-SONG:B0154`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-074` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-075 — Song.signature_denominator

**D-current-public/target-U.** For the documented Song context, `signature_denominator` is a direct properties declaration with source type `int` and documented get/set/observe role. No additional member-specific behavior is stated beyond its heading and access declaration. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `int`; access `get,set,observe`; result type `int`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0155`, `C74-LOM-SONG:B0156`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-075` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-076 — Song.signature_numerator

**D-current-public/target-U.** For the documented Song context, `signature_numerator` is a direct properties declaration with source type `int` and documented get/set/observe role. No additional member-specific behavior is stated beyond its heading and access declaration. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `int`; access `get,set,observe`; result type `int`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0157`, `C74-LOM-SONG:B0158`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-076` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-077 — Song.song_length

**D-current-public/target-U.** For the documented Song context, `song_length` is a direct properties declaration with source type `float` and documented get/observe role. Publisher member description: A little more than last_event_time, in beats. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `float`; access `get,observe`; result type `float`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0159`, `C74-LOM-SONG:B0160`, `C74-LOM-SONG:B0161`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-077` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-078 — Song.start_time

**D-current-public/target-U.** For the documented Song context, `start_time` is a direct properties declaration with source type `float` and documented get/set/observe role. Publisher member description: The position in the Live Set where playing will start, in beats. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `float`; access `get,set,observe`; result type `float`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0162`, `C74-LOM-SONG:B0163`, `C74-LOM-SONG:B0164`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-078` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-079 — Song.swing_amount

**D-current-public/target-U.** For the documented Song context, `swing_amount` is a direct properties declaration with source type `float` and documented get/set/observe role. Publisher member description: Range: 0.0 - 1.0; affects MIDI Recording Quantization and all direct calls to Clip.quantize. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `float`; access `get,set,observe`; result type `float`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0165`, `C74-LOM-SONG:B0166`, `C74-LOM-SONG:B0167`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-079` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-080 — Song.tempo

**D-current-public/target-U.** For the documented Song context, `tempo` is a direct properties declaration with source type `float` and documented get/set/observe role. Publisher member description: Current tempo of the Live Set in BPM, 20.0 ... 999.0. The tempo may be automated, so it can change depending on the current song time. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `float`; access `get,set,observe`; result type `float`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0168`, `C74-LOM-SONG:B0169`, `C74-LOM-SONG:B0170`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-080` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-081 — Song.capture_and_insert_scene

**D-current-public/target-U.** For the documented Song context, `capture_and_insert_scene` is a direct functions declaration and documented call role. Publisher member description: Capture the currently playing clips and insert them as a new scene below the selected scene. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `unstated`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0172`, `C74-LOM-SONG:B0173`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-081` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-082 — Song.capture_midi

**D-current-public/target-U.** For the documented Song context, `capture_midi` is a direct functions declaration and documented call role. Publisher member description: Parameter: destination [int] 0 = auto, 1 = session, 2 = arrangement Capture recently played MIDI material from audible tracks into a Live Clip. If destinaton is not set or it is set to auto, the Clip is inserted into the view currently visible in the focused Live window. Otherwise, it is inserted into the specified view. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `unstated`. Arguments, in source order: `destination` (int, optionality optional; omission explicitly supported by Song B0175 prose).

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0174`, `C74-LOM-SONG:B0175`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-082`, `LCS-BRANCH-008` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-083 — Song.continue_playing

**D-current-public/target-U.** For the documented Song context, `continue_playing` is a direct functions declaration and documented call role. Publisher member description: From the current playback position. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `unstated`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0176`, `C74-LOM-SONG:B0177`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-083` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-084 — Song.create_audio_track

**D-current-public/target-U.** For the documented Song context, `create_audio_track` is a direct functions declaration and documented call role. Publisher member description: Parameter: index Index determines where the track is added, it is only valid between 0 and len(song.tracks). Using an index of -1 will add the new track at the end of the list. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `unstated`. Arguments, in source order: `index` (type unstated, optionality unstated).

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0178`, `C74-LOM-SONG:B0179`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-084` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-085 — Song.create_midi_track

**D-current-public/target-U.** For the documented Song context, `create_midi_track` is a direct functions declaration and documented call role. Publisher member description: Parameter: index Index determines where the track is added, it is only valid between 0 and len(song.tracks). Using an index of -1 will add the new track at the end of the list. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `unstated`. Arguments, in source order: `index` (type unstated, optionality unstated).

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0180`, `C74-LOM-SONG:B0181`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-085` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-086 — Song.create_return_track

**D-current-public/target-U.** For the documented Song context, `create_return_track` is a direct functions declaration and documented call role. Publisher member description: Adds a new return track at the end. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `unstated`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0182`, `C74-LOM-SONG:B0183`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-086` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-087 — Song.create_scene

**D-current-public/target-U.** For the documented Song context, `create_scene` is a direct functions declaration and documented call role. Publisher member description: Parameter: index Returns: The new scene Index determines where the scene is added. It is only valid between 0 and len(song.scenes). Using an index of -1 will add the new scene at the end of the list. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `unstated`. Arguments, in source order: `index` (type unstated, optionality unstated).

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0184`, `C74-LOM-SONG:B0185`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-087`, `LCS-BRANCH-005` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-088 — Song.delete_scene

**D-current-public/target-U.** For the documented Song context, `delete_scene` is a direct functions declaration and documented call role. Publisher member description: Parameter: index Delete the scene at the given index. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `unstated`. Arguments, in source order: `index` (type unstated, optionality unstated).

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0186`, `C74-LOM-SONG:B0187`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-088` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-089 — Song.delete_track

**D-current-public/target-U.** For the documented Song context, `delete_track` is a direct functions declaration and documented call role. Publisher member description: Parameter: index Delete the track at the given index. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `unstated`. Arguments, in source order: `index` (type unstated, optionality unstated).

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0188`, `C74-LOM-SONG:B0189`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-089` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-090 — Song.delete_return_track

**D-current-public/target-U.** For the documented Song context, `delete_return_track` is a direct functions declaration and documented call role. Publisher member description: Parameter: index Delete the return track at the given index. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `unstated`. Arguments, in source order: `index` (type unstated, optionality unstated).

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0190`, `C74-LOM-SONG:B0191`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-090` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-091 — Song.duplicate_scene

**D-current-public/target-U.** For the documented Song context, `duplicate_scene` is a direct functions declaration and documented call role. Publisher member description: Parameter: index Index determines which scene to duplicate. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `unstated`. Arguments, in source order: `index` (type unstated, optionality unstated).

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0192`, `C74-LOM-SONG:B0193`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-091` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-092 — Song.duplicate_track

**D-current-public/target-U.** For the documented Song context, `duplicate_track` is a direct functions declaration and documented call role. Publisher member description: Parameter: index Index determines which track to duplicate. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `unstated`. Arguments, in source order: `index` (type unstated, optionality unstated).

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0194`, `C74-LOM-SONG:B0195`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-092` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-093 — Song.find_device_position

**D-current-public/target-U.** For the documented Song context, `find_device_position` is a direct functions declaration and documented call role. Publisher member description: Parameter: device [live object] target [live object] target position [int] Returns: [int] The position in the target's chain where the device can be inserted that is the closest possible to the target position. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `int`. Arguments, in source order: `device` (live object, optionality unstated); `target` (live object, optionality unstated); `target position` (int, optionality unstated).

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0196`, `C74-LOM-SONG:B0197`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-093` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-094 — Song.force_link_beat_time

**D-current-public/target-U.** For the documented Song context, `force_link_beat_time` is a direct functions declaration and documented call role. Publisher member description: Force the Link timeline to jump to Live's current beat time. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `unstated`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0198`, `C74-LOM-SONG:B0199`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-094` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-095 — Song.get_beats_loop_length

**D-current-public/target-U.** For the documented Song context, `get_beats_loop_length` is a direct functions declaration and documented call role. Publisher member description: Returns: bars.beats.sixteenths.ticks [symbol] The Arrangement loop length. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `symbol`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0200`, `C74-LOM-SONG:B0201`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-095` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-096 — Song.get_beats_loop_start

**D-current-public/target-U.** For the documented Song context, `get_beats_loop_start` is a direct functions declaration and documented call role. Publisher member description: Returns: bars.beats.sixteenths.ticks [symbol] The Arrangement loop start. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `symbol`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0202`, `C74-LOM-SONG:B0203`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-096` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-097 — Song.get_current_beats_song_time

**D-current-public/target-U.** For the documented Song context, `get_current_beats_song_time` is a direct functions declaration and documented call role. Publisher member description: Returns: bars.beats.sixteenths.ticks [symbol] The current Arrangement playback position. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `symbol`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0204`, `C74-LOM-SONG:B0205`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-097` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-098 — Song.get_current_smpte_song_time

**D-current-public/target-U.** For the documented Song context, `get_current_smpte_song_time` is a direct functions declaration and documented call role. Publisher member description: Parameter: format format [int] is the time code type to be returned 0 = the frame position shows the milliseconds 1 = Smpte24 2 = Smpte25 3 = Smpte30 4 = Smpte30Drop 5 = Smpte29 Returns: hours:min:sec The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `unstated`. Arguments, in source order: `format` (int, optionality unstated).

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0206`, `C74-LOM-SONG:B0207`, `C74-LOM-SONG:B0208`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-098` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-099 — Song.is_cue_point_selected

**D-current-public/target-U.** For the documented Song context, `is_cue_point_selected` is a direct functions declaration and documented call role. Publisher member description: Returns: bool 1 = the current Arrangement playback position is at a cue point The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `bool`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0209`, `C74-LOM-SONG:B0210`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-099` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-100 — Song.jump_by

**D-current-public/target-U.** For the documented Song context, `jump_by` is a direct functions declaration and documented call role. Publisher member description: Parameter: beats beats [float] is the amount to jump relatively to the current position The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `unstated`. Arguments, in source order: `beats` (float, optionality unstated).

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0211`, `C74-LOM-SONG:B0212`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-100` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-101 — Song.jump_to_next_cue

**D-current-public/target-U.** For the documented Song context, `jump_to_next_cue` is a direct functions declaration and documented call role. Publisher member description: Jump to the right, if possible. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `unstated`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0213`, `C74-LOM-SONG:B0214`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-101`, `LCS-BRANCH-007` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-102 — Song.jump_to_prev_cue

**D-current-public/target-U.** For the documented Song context, `jump_to_prev_cue` is a direct functions declaration and documented call role. Publisher member description: Jump to the left, if possible. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `unstated`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0215`, `C74-LOM-SONG:B0216`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-102` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-103 — Song.move_device

**D-current-public/target-U.** For the documented Song context, `move_device` is a direct functions declaration and documented call role. Publisher member description: Parameter: device [live object] target [live object] target position [int] Returns: [int] The position in the target's chain where the device was inserted. Move the device to the specified position in the target chain. If the device cannot be moved to the specified position, the nearest possible position is chosen. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `int`. Arguments, in source order: `device` (live object, optionality unstated); `target` (live object, optionality unstated); `target position` (int, optionality unstated).

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0217`, `C74-LOM-SONG:B0218`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-103` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-104 — Song.play_selection

**D-current-public/target-U.** For the documented Song context, `play_selection` is a direct functions declaration and documented call role. Publisher member description: Do nothing if no selection is set in Arrangement, or play the current selection. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `unstated`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0219`, `C74-LOM-SONG:B0220`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-104`, `LCS-BRANCH-006` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-105 — Song.re_enable_automation

**D-current-public/target-U.** For the documented Song context, `re_enable_automation` is a direct functions declaration and documented call role. Publisher member description: Trigger 'Re-Enable Automation', re-activating automation in all running Session clips. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `unstated`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0221`, `C74-LOM-SONG:B0222`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-105` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-106 — Song.redo

**D-current-public/target-U.** For the documented Song context, `redo` is a direct functions declaration and documented call role. Publisher member description: Causes the Live application to redo the last operation. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `unstated`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0223`, `C74-LOM-SONG:B0224`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-106` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-107 — Song.scrub_by

**D-current-public/target-U.** For the documented Song context, `scrub_by` is a direct functions declaration and documented call role. Publisher member description: Parameter: beats beats [float] the amount to scrub relative to the current Arrangement playback position Same as jump_by, at the moment. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `unstated`. Arguments, in source order: `beats` (float, optionality unstated).

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0225`, `C74-LOM-SONG:B0226`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-107` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-108 — Song.set_or_delete_cue

**D-current-public/target-U.** For the documented Song context, `set_or_delete_cue` is a direct functions declaration and documented call role. Publisher member description: Toggle cue point at current Arrangement playback position. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `unstated`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0227`, `C74-LOM-SONG:B0228`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-108` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-109 — Song.start_playing

**D-current-public/target-U.** For the documented Song context, `start_playing` is a direct functions declaration and documented call role. Publisher member description: Start playback from the insert marker. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `unstated`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0229`, `C74-LOM-SONG:B0230`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-109` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-110 — Song.stop_all_clips

**D-current-public/target-U.** For the documented Song context, `stop_all_clips` is a direct functions declaration and documented call role. Publisher member description: Parameter (optional): quantized Calling the function with 0 will stop all clips immediately, independent of the launch quantization. The default is '1'. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `unstated`. Arguments, in source order: `quantized` (type unstated, optionality optional, source default 1).

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0231`, `C74-LOM-SONG:B0232`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-110` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-111 — Song.stop_playing

**D-current-public/target-U.** For the documented Song context, `stop_playing` is a direct functions declaration and documented call role. Publisher member description: Stop the playback. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `unstated`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0233`, `C74-LOM-SONG:B0234`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-111` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-112 — Song.tap_tempo

**D-current-public/target-U.** For the documented Song context, `tap_tempo` is a direct functions declaration and documented call role. Publisher member description: Same as pressing the Tap Tempo button in the transport bar. The new tempo is calculated based on the time between subsequent calls of this function. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `unstated`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0235`, `C74-LOM-SONG:B0236`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-112` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-113 — Song.trigger_session_record

**D-current-public/target-U.** For the documented Song context, `trigger_session_record` is a direct functions declaration and documented call role. Publisher member description: Parameter: record_length (optional) Starts recording in either the selected slot or the next empty slot, if the track is armed. If record_length is provided, the slot will record for the given length in beats. If triggered while recording, recording will stop and clip playback will start. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `unstated`. Arguments, in source order: `record_length` (type unstated, optionality optional).

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0237`, `C74-LOM-SONG:B0238`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-113` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-114 — Song.undo

**D-current-public/target-U.** For the documented Song context, `undo` is a direct functions declaration and documented call role. Publisher member description: Causes the Live application to undo the last operation. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `unstated`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG:B0002`, `C74-LOM-SONG:B0004`, `C74-LOM-SONG:B0239`, `C74-LOM-SONG:B0240`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-114` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

## Song.View

### REQ-LAPI-CORE-115 — Song.View.detail_clip

**D-current-public/target-U.** For the documented Song.View context, `detail_clip` is a direct children declaration with source type `Clip` and documented get/set/observe role. Publisher member description: The clip currently displayed in the Live application's Detail View. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `Clip`; access `get,set,observe`; result type `Clip`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG_VIEW member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG_VIEW:B0002`, `C74-LOM-SONG_VIEW:B0004`, `C74-LOM-SONG_VIEW:B0006`, `C74-LOM-SONG_VIEW:B0007`, `C74-LOM-SONG_VIEW:B0008`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-115` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-116 — Song.View.highlighted_clip_slot

**D-current-public/target-U.** For the documented Song.View context, `highlighted_clip_slot` is a direct children declaration with source type `ClipSlot` and documented get/set role. Publisher member description: The slot highlighted in the Session View. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `ClipSlot`; access `get,set`; result type `ClipSlot`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG_VIEW member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG_VIEW:B0002`, `C74-LOM-SONG_VIEW:B0004`, `C74-LOM-SONG_VIEW:B0009`, `C74-LOM-SONG_VIEW:B0010`, `C74-LOM-SONG_VIEW:B0011`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-116` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-117 — Song.View.mod_mapping_device

**D-current-public/target-U.** For the documented Song.View context, `mod_mapping_device` is a direct children declaration with source type `Device` and documented get/set/observe role. Publisher member description: When assigned a device id, modulation mapping mode is active. When assigned id 0, mapping mode is not active. Affects only Push 3 at this time. The device value that is used to enable modulation mapping is also used for the following purposes: - When the device is removed, mapping mode is exited automatically without reporting a chosen parameter for mapping. When a parameter is chosen that belongs to the assigned device, this parameter will not be chosen for mapping. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `Device`; access `get,set,observe`; result type `Device`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG_VIEW member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG_VIEW:B0002`, `C74-LOM-SONG_VIEW:B0004`, `C74-LOM-SONG_VIEW:B0012`, `C74-LOM-SONG_VIEW:B0013`, `C74-LOM-SONG_VIEW:B0014`, `C74-LOM-SONG_VIEW:B0015`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-117`, `LCS-BRANCH-009` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-118 — Song.View.mod_mapping_parameter

**D-current-public/target-U.** For the documented Song.View context, `mod_mapping_parameter` is a direct children declaration with source type `DeviceParameter` and documented get/observe role. Publisher member description: The parameter selected for modulation mapping, or id 0. Observing this property outputs the id of a parameter that is selected in the Live UI or that is chosen for mapping on Push. Reports id 0 when no parameter is chosen, for example when a parameter is deselected in the Live UI. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `DeviceParameter`; access `get,observe`; result type `DeviceParameter`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG_VIEW member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG_VIEW:B0002`, `C74-LOM-SONG_VIEW:B0004`, `C74-LOM-SONG_VIEW:B0016`, `C74-LOM-SONG_VIEW:B0017`, `C74-LOM-SONG_VIEW:B0018`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-118` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-119 — Song.View.selected_chain

**D-current-public/target-U.** For the documented Song.View context, `selected_chain` is a direct children declaration with source type `Chain` and documented get/set/observe role. Publisher member description: The highlighted chain, or "id 0" The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `Chain`; access `get,set,observe`; result type `Chain`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG_VIEW member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG_VIEW:B0002`, `C74-LOM-SONG_VIEW:B0004`, `C74-LOM-SONG_VIEW:B0019`, `C74-LOM-SONG_VIEW:B0020`, `C74-LOM-SONG_VIEW:B0021`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-119` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-120 — Song.View.selected_parameter

**D-current-public/target-U.** For the documented Song.View context, `selected_parameter` is a direct children declaration with source type `DeviceParameter` and documented get/observe role. Publisher member description: The selected parameter, or "id 0" The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `DeviceParameter`; access `get,observe`; result type `DeviceParameter`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG_VIEW member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG_VIEW:B0002`, `C74-LOM-SONG_VIEW:B0004`, `C74-LOM-SONG_VIEW:B0022`, `C74-LOM-SONG_VIEW:B0023`, `C74-LOM-SONG_VIEW:B0024`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-120` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-121 — Song.View.selected_scene

**D-current-public/target-U.** For the documented Song.View context, `selected_scene` is a direct children declaration with source type `Scene` and documented get/set/observe role. No additional member-specific behavior is stated beyond its heading and access declaration. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `Scene`; access `get,set,observe`; result type `Scene`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG_VIEW member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG_VIEW:B0002`, `C74-LOM-SONG_VIEW:B0004`, `C74-LOM-SONG_VIEW:B0025`, `C74-LOM-SONG_VIEW:B0026`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-121` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-122 — Song.View.selected_track

**D-current-public/target-U.** For the documented Song.View context, `selected_track` is a direct children declaration with source type `Track` and documented get/set/observe role. No additional member-specific behavior is stated beyond its heading and access declaration. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `Track`; access `get,set,observe`; result type `Track`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG_VIEW member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG_VIEW:B0002`, `C74-LOM-SONG_VIEW:B0004`, `C74-LOM-SONG_VIEW:B0027`, `C74-LOM-SONG_VIEW:B0028`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-122` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-123 — Song.View.draw_mode

**D-current-public/target-U.** For the documented Song.View context, `draw_mode` is a direct properties declaration with source type `bool` and documented get/set/observe role. Publisher member description: Reflects the state of the envelope/automation Draw Mode Switch in the transport bar, as toggled with Cmd/Ctrl-B. 0 = breakpoint editing (shows arrow), 1 = drawing (shows pencil) The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `bool`; access `get,set,observe`; result type `bool`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG_VIEW member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG_VIEW:B0002`, `C74-LOM-SONG_VIEW:B0004`, `C74-LOM-SONG_VIEW:B0030`, `C74-LOM-SONG_VIEW:B0031`, `C74-LOM-SONG_VIEW:B0032`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-123` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-124 — Song.View.follow_song

**D-current-public/target-U.** For the documented Song.View context, `follow_song` is a direct properties declaration with source type `bool` and documented get/set/observe role. Publisher member description: Reflects the state of the Follow switch in the transport bar as toggled with Cmd/Ctrl-F. 0 = don't follow playback position, 1 = follow playback position The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `bool`; access `get,set,observe`; result type `bool`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SONG_VIEW member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG_VIEW:B0002`, `C74-LOM-SONG_VIEW:B0004`, `C74-LOM-SONG_VIEW:B0033`, `C74-LOM-SONG_VIEW:B0034`, `C74-LOM-SONG_VIEW:B0035`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-124` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-125 — Song.View.select_device

**D-current-public/target-U.** For the documented Song.View context, `select_device` is a direct functions declaration and documented call role. Publisher member description: Parameter: id NN Selects the given device object in its track. You may obtain the id using a live.path or by using get devices on a track, for example. The track containing the device will not be shown automatically, and the device gets the appointed device (blue hand) only if its track is selected. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `unstated`. Arguments, in source order: `id NN` (type unstated, optionality unstated).

Evidence: [C74-LOM-SONG_VIEW member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SONG_VIEW:B0002`, `C74-LOM-SONG_VIEW:B0004`, `C74-LOM-SONG_VIEW:B0037`, `C74-LOM-SONG_VIEW:B0038`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-125`, `LCS-BRANCH-010` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

## Track

### REQ-LAPI-CORE-126 — Track.take_lanes

**D-current-public/target-U.** For the documented Track context, `take_lanes` is a direct children declaration with source type `list of TakeLane` and documented get/observe role. Publisher member description: The list of this track's take lanes The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `list of TakeLane`; access `get,observe`; result type `list of TakeLane`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-TRACK member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-TRACK:B0002`, `C74-LOM-TRACK:B0004`, `C74-LOM-TRACK:B0006`, `C74-LOM-TRACK:B0007`, `C74-LOM-TRACK:B0008`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-126` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-127 — Track.clip_slots

**D-current-public/target-U.** For the documented Track context, `clip_slots` is a direct children declaration with source type `list of ClipSlot` and documented get/observe role. No additional member-specific behavior is stated beyond its heading and access declaration. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `list of ClipSlot`; access `get,observe`; result type `list of ClipSlot`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-TRACK member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-TRACK:B0002`, `C74-LOM-TRACK:B0004`, `C74-LOM-TRACK:B0009`, `C74-LOM-TRACK:B0010`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-127` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-128 — Track.arrangement_clips

**D-current-public/target-U.** For the documented Track context, `arrangement_clips` is a direct children declaration with source type `list of Clip` and documented get/observe role. Publisher member description: The list of this track's Arrangement View clip IDs Available since Live 11.0. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `list of Clip`; access `get,observe`; result type `list of Clip`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-TRACK member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-TRACK:B0002`, `C74-LOM-TRACK:B0004`, `C74-LOM-TRACK:B0011`, `C74-LOM-TRACK:B0012`, `C74-LOM-TRACK:B0013`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-128` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-129 — Track.devices

**D-current-public/target-U.** For the documented Track context, `devices` is a direct children declaration with source type `list of Device` and documented get/observe role. Publisher member description: Includes mixer device. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `list of Device`; access `get,observe`; result type `list of Device`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-TRACK member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-TRACK:B0002`, `C74-LOM-TRACK:B0004`, `C74-LOM-TRACK:B0014`, `C74-LOM-TRACK:B0015`, `C74-LOM-TRACK:B0016`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-129` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-130 — Track.group_track

**D-current-public/target-U.** For the documented Track context, `group_track` is a direct children declaration with source type `Track` and documented get role. Publisher member description: The Group Track, if the Track is grouped. If it is not, id 0 is returned. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `Track`; access `get`; result type `Track`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-TRACK member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-TRACK:B0002`, `C74-LOM-TRACK:B0004`, `C74-LOM-TRACK:B0017`, `C74-LOM-TRACK:B0018`, `C74-LOM-TRACK:B0019`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-130` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-131 — Track.mixer_device

**D-current-public/target-U.** For the documented Track context, `mixer_device` is a direct children declaration with source type `MixerDevice` and documented get role. No additional member-specific behavior is stated beyond its heading and access declaration. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `MixerDevice`; access `get`; result type `MixerDevice`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-TRACK member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-TRACK:B0002`, `C74-LOM-TRACK:B0004`, `C74-LOM-TRACK:B0020`, `C74-LOM-TRACK:B0021`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-131` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-132 — Track.view

**D-current-public/target-U.** For the documented Track context, `view` is a direct children declaration with source type `Track.View` and documented get role. No additional member-specific behavior is stated beyond its heading and access declaration. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `Track.View`; access `get`; result type `Track.View`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-TRACK member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-TRACK:B0002`, `C74-LOM-TRACK:B0004`, `C74-LOM-TRACK:B0022`, `C74-LOM-TRACK:B0023`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-132` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-133 — Track.arm

**D-current-public/target-U.** For the documented Track context, `arm` is a direct properties declaration with source type `bool` and documented get/set/observe role. Publisher member description: 1 = track is armed for recording. [not in return/master tracks] The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `bool`; access `get,set,observe`; result type `bool`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-TRACK member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-TRACK:B0002`, `C74-LOM-TRACK:B0004`, `C74-LOM-TRACK:B0025`, `C74-LOM-TRACK:B0026`, `C74-LOM-TRACK:B0027`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-133` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-134 — Track.available_input_routing_channels

**D-current-public/target-U.** For the documented Track context, `available_input_routing_channels` is a direct properties declaration with source type `dictionary` and documented get/observe role. Publisher member description: The list of available source channels for the track's input routing. It's represented as a dictionary with the following key: available_input_routing_channels [list] The list contains dictionaries as described in input_routing_channel. Only available on MIDI and audio tracks. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `dictionary`; access `get,observe`; result type `dictionary`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-TRACK member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-TRACK:B0002`, `C74-LOM-TRACK:B0004`, `C74-LOM-TRACK:B0028`, `C74-LOM-TRACK:B0029`, `C74-LOM-TRACK:B0030`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-134` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-135 — Track.available_input_routing_types

**D-current-public/target-U.** For the documented Track context, `available_input_routing_types` is a direct properties declaration with source type `dictionary` and documented get/observe role. Publisher member description: The list of available source types for the track's input routing. It's represented as a dictionary with the following key: available_input_routing_types [list] The list contains dictionaries as described in input_routing_type. Only available on MIDI and audio tracks. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `dictionary`; access `get,observe`; result type `dictionary`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-TRACK member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-TRACK:B0002`, `C74-LOM-TRACK:B0004`, `C74-LOM-TRACK:B0031`, `C74-LOM-TRACK:B0032`, `C74-LOM-TRACK:B0033`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-135` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-136 — Track.available_output_routing_channels

**D-current-public/target-U.** For the documented Track context, `available_output_routing_channels` is a direct properties declaration with source type `dictionary` and documented get/observe role. Publisher member description: The list of available target channels for the track's output routing. It's represented as a dictionary with the following key: available_output_routing_channels [list] The list contains dictionaries as described in output_routing_channel. Not available on the master track. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `dictionary`; access `get,observe`; result type `dictionary`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-TRACK member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-TRACK:B0002`, `C74-LOM-TRACK:B0004`, `C74-LOM-TRACK:B0034`, `C74-LOM-TRACK:B0035`, `C74-LOM-TRACK:B0036`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-136` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-137 — Track.available_output_routing_types

**D-current-public/target-U.** For the documented Track context, `available_output_routing_types` is a direct properties declaration with source type `dictionary` and documented get/observe role. Publisher member description: The list of available target types for the track's output routing. It's represented as a dictionary with the following key: available_output_routing_types [list] The list contains dictionaries as described in output_routing_type. Not available on the master track. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `dictionary`; access `get,observe`; result type `dictionary`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-TRACK member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-TRACK:B0002`, `C74-LOM-TRACK:B0004`, `C74-LOM-TRACK:B0037`, `C74-LOM-TRACK:B0038`, `C74-LOM-TRACK:B0039`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-137` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-138 — Track.back_to_arranger

**D-current-public/target-U.** For the documented Track context, `back_to_arranger` is a direct properties declaration with source type `bool` and documented get/set/observe role. Publisher member description: Get/set/observe the current state of the Single Track Back to Arrangement button (1 = highlighted). This button is used to indicate that the current state of the playback differs from what is stored in the Arrangement. Setting this property to 0 will make Live go back to playing the track's arrangement content. For group tracks, this means that all of the tracks that belong to the group and any subgroups will go back to playing the arrangement. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `bool`; access `get,set,observe`; result type `bool`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-TRACK member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-TRACK:B0002`, `C74-LOM-TRACK:B0004`, `C74-LOM-TRACK:B0040`, `C74-LOM-TRACK:B0041`, `C74-LOM-TRACK:B0042`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-138` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-139 — Track.can_be_armed

**D-current-public/target-U.** For the documented Track context, `can_be_armed` is a direct properties declaration with source type `bool` and documented get role. Publisher member description: 0 for return and master tracks. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `bool`; access `get`; result type `bool`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-TRACK member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-TRACK:B0002`, `C74-LOM-TRACK:B0004`, `C74-LOM-TRACK:B0043`, `C74-LOM-TRACK:B0044`, `C74-LOM-TRACK:B0045`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-139` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-140 — Track.can_be_frozen

**D-current-public/target-U.** For the documented Track context, `can_be_frozen` is a direct properties declaration with source type `bool` and documented get role. Publisher member description: 1 = the track can be frozen, 0 = otherwise. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `bool`; access `get`; result type `bool`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-TRACK member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-TRACK:B0002`, `C74-LOM-TRACK:B0004`, `C74-LOM-TRACK:B0046`, `C74-LOM-TRACK:B0047`, `C74-LOM-TRACK:B0048`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-140` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-141 — Track.can_show_chains

**D-current-public/target-U.** For the documented Track context, `can_show_chains` is a direct properties declaration with source type `bool` and documented get role. Publisher member description: 1 = the track contains an Instrument Rack device that can show chains in Session View. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `bool`; access `get`; result type `bool`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-TRACK member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-TRACK:B0002`, `C74-LOM-TRACK:B0004`, `C74-LOM-TRACK:B0049`, `C74-LOM-TRACK:B0050`, `C74-LOM-TRACK:B0051`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-141` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-142 — Track.color

**D-current-public/target-U.** For the documented Track context, `color` is a direct properties declaration with source type `int` and documented get/set/observe role. Publisher member description: The RGB value of the track's color in the form 0x00rrggbb or (2^16 * red) + (2^8) * green + blue, where red, green and blue are values from 0 (dark) to 255 (light). When setting the RGB value, the nearest color from the track color chooser is taken. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `int`; access `get,set,observe`; result type `int`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-TRACK member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-TRACK:B0002`, `C74-LOM-TRACK:B0004`, `C74-LOM-TRACK:B0052`, `C74-LOM-TRACK:B0053`, `C74-LOM-TRACK:B0054`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-142` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-143 — Track.color_index

**D-current-public/target-U.** For the documented Track context, `color_index` is a direct properties declaration with source type `long` and documented get/set/observe role. Publisher member description: The color index of the track. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `long`; access `get,set,observe`; result type `long`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-TRACK member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-TRACK:B0002`, `C74-LOM-TRACK:B0004`, `C74-LOM-TRACK:B0055`, `C74-LOM-TRACK:B0056`, `C74-LOM-TRACK:B0057`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-143` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-144 — Track.fired_slot_index

**D-current-public/target-U.** For the documented Track context, `fired_slot_index` is a direct properties declaration with source type `int` and documented get/observe role. Publisher member description: Reflects the blinking clip slot. -1 = no slot fired, -2 = Clip Stop Button fired First clip slot has index 0. [not in return/master tracks] The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `int`; access `get,observe`; result type `int`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-TRACK member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-TRACK:B0002`, `C74-LOM-TRACK:B0004`, `C74-LOM-TRACK:B0058`, `C74-LOM-TRACK:B0059`, `C74-LOM-TRACK:B0060`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-144` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-145 — Track.fold_state

**D-current-public/target-U.** For the documented Track context, `fold_state` is a direct properties declaration with source type `int` and documented get/set role. Publisher member description: 0 = tracks within the Group Track are visible, 1 = Group Track is folded and the tracks within the Group Track are hidden [only available if is_foldable = 1] The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `int`; access `get,set`; result type `int`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-TRACK member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-TRACK:B0002`, `C74-LOM-TRACK:B0004`, `C74-LOM-TRACK:B0061`, `C74-LOM-TRACK:B0062`, `C74-LOM-TRACK:B0063`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-145` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-146 — Track.has_audio_input

**D-current-public/target-U.** For the documented Track context, `has_audio_input` is a direct properties declaration with source type `bool` and documented get role. Publisher member description: 1 for audio tracks. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `bool`; access `get`; result type `bool`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-TRACK member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-TRACK:B0002`, `C74-LOM-TRACK:B0004`, `C74-LOM-TRACK:B0064`, `C74-LOM-TRACK:B0065`, `C74-LOM-TRACK:B0066`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-146` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-147 — Track.has_audio_output

**D-current-public/target-U.** For the documented Track context, `has_audio_output` is a direct properties declaration with source type `bool` and documented get role. Publisher member description: 1 for audio tracks and MIDI tracks with instruments. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `bool`; access `get`; result type `bool`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-TRACK member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-TRACK:B0002`, `C74-LOM-TRACK:B0004`, `C74-LOM-TRACK:B0067`, `C74-LOM-TRACK:B0068`, `C74-LOM-TRACK:B0069`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-147` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-148 — Track.has_midi_input

**D-current-public/target-U.** For the documented Track context, `has_midi_input` is a direct properties declaration with source type `bool` and documented get role. Publisher member description: 1 for MIDI tracks. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `bool`; access `get`; result type `bool`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-TRACK member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-TRACK:B0002`, `C74-LOM-TRACK:B0004`, `C74-LOM-TRACK:B0070`, `C74-LOM-TRACK:B0071`, `C74-LOM-TRACK:B0072`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-148` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-149 — Track.has_midi_output

**D-current-public/target-U.** For the documented Track context, `has_midi_output` is a direct properties declaration with source type `bool` and documented get role. Publisher member description: 1 for MIDI tracks with no instruments and no audio effects. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `bool`; access `get`; result type `bool`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-TRACK member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-TRACK:B0002`, `C74-LOM-TRACK:B0004`, `C74-LOM-TRACK:B0073`, `C74-LOM-TRACK:B0074`, `C74-LOM-TRACK:B0075`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-149` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-150 — Track.implicit_arm

**D-current-public/target-U.** For the documented Track context, `implicit_arm` is a direct properties declaration with source type `bool` and documented get/set/observe role. Publisher member description: A second arm state, only used by Push so far. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `bool`; access `get,set,observe`; result type `bool`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-TRACK member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-TRACK:B0002`, `C74-LOM-TRACK:B0004`, `C74-LOM-TRACK:B0076`, `C74-LOM-TRACK:B0077`, `C74-LOM-TRACK:B0078`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-150` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-151 — Track.input_meter_left

**D-current-public/target-U.** For the documented Track context, `input_meter_left` is a direct properties declaration with source type `float` and documented get/observe role. Publisher member description: Smoothed momentary peak value of left channel input meter, 0.0 to 1.0. For tracks with audio output only. This value corresponds to the meters shown in Live. Please take into account that the left/right audio meters put a significant load onto the GUI part of Live. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `float`; access `get,observe`; result type `float`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-TRACK member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-TRACK:B0002`, `C74-LOM-TRACK:B0004`, `C74-LOM-TRACK:B0079`, `C74-LOM-TRACK:B0080`, `C74-LOM-TRACK:B0081`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-151` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-152 — Track.input_meter_level

**D-current-public/target-U.** For the documented Track context, `input_meter_level` is a direct properties declaration with source type `float` and documented get/observe role. Publisher member description: Hold peak value of input meters of audio and MIDI tracks, 0.0 ... 1.0. For audio tracks it is the maximum of the left and right channels. The hold time is 1 second. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `float`; access `get,observe`; result type `float`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-TRACK member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-TRACK:B0002`, `C74-LOM-TRACK:B0004`, `C74-LOM-TRACK:B0082`, `C74-LOM-TRACK:B0083`, `C74-LOM-TRACK:B0084`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-152` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-153 — Track.input_meter_right

**D-current-public/target-U.** For the documented Track context, `input_meter_right` is a direct properties declaration with source type `float` and documented get/observe role. Publisher member description: Smoothed momentary peak value of right channel input meter, 0.0 to 1.0. For tracks with audio output only. This value corresponds to the meters shown in Live. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `float`; access `get,observe`; result type `float`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-TRACK member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-TRACK:B0002`, `C74-LOM-TRACK:B0004`, `C74-LOM-TRACK:B0085`, `C74-LOM-TRACK:B0086`, `C74-LOM-TRACK:B0087`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-153` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-154 — Track.input_routing_channel

**D-current-public/target-U.** For the documented Track context, `input_routing_channel` is a direct properties declaration with source type `dictionary` and documented get/set/observe role. Publisher member description: The currently selected source channel for the track's input routing. It's represented as a dictionary with the following keys: display_name [symbol] identifier [symbol] Can be set to all values found in the track's available_input_routing_channels. Only available on MIDI and audio tracks. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `dictionary`; access `get,set,observe`; result type `dictionary`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-TRACK member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-TRACK:B0002`, `C74-LOM-TRACK:B0004`, `C74-LOM-TRACK:B0088`, `C74-LOM-TRACK:B0089`, `C74-LOM-TRACK:B0090`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-154` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-155 — Track.input_routing_type

**D-current-public/target-U.** For the documented Track context, `input_routing_type` is a direct properties declaration with source type `dictionary` and documented get/set/observe role. Publisher member description: The currently selected source type for the track's input routing. It's represented as a dictionary with the following keys: display_name [symbol] identifier [symbol] Can be set to all values found in the track's available_input_routing_types. Only available on MIDI and audio tracks. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `dictionary`; access `get,set,observe`; result type `dictionary`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-TRACK member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-TRACK:B0002`, `C74-LOM-TRACK:B0004`, `C74-LOM-TRACK:B0091`, `C74-LOM-TRACK:B0092`, `C74-LOM-TRACK:B0093`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-155`, `LCS-BRANCH-014` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-156 — Track.is_foldable

**D-current-public/target-U.** For the documented Track context, `is_foldable` is a direct properties declaration with source type `bool` and documented get role. Publisher member description: 1 = track can be (un)folded to hide or reveal the contained tracks. This is currently the case for Group Tracks. Instrument and Drum Racks return 0 although they can be opened/closed. This will be fixed in a later release. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `bool`; access `get`; result type `bool`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-TRACK member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-TRACK:B0002`, `C74-LOM-TRACK:B0004`, `C74-LOM-TRACK:B0094`, `C74-LOM-TRACK:B0095`, `C74-LOM-TRACK:B0096`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-156` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-157 — Track.is_frozen

**D-current-public/target-U.** For the documented Track context, `is_frozen` is a direct properties declaration with source type `bool` and documented get/observe role. Publisher member description: 1 = the track is currently frozen. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `bool`; access `get,observe`; result type `bool`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-TRACK member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-TRACK:B0002`, `C74-LOM-TRACK:B0004`, `C74-LOM-TRACK:B0097`, `C74-LOM-TRACK:B0098`, `C74-LOM-TRACK:B0099`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-157` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-158 — Track.is_grouped

**D-current-public/target-U.** For the documented Track context, `is_grouped` is a direct properties declaration with source type `bool` and documented get role. Publisher member description: 1 = the track is contained within a Group Track. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `bool`; access `get`; result type `bool`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-TRACK member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-TRACK:B0002`, `C74-LOM-TRACK:B0004`, `C74-LOM-TRACK:B0100`, `C74-LOM-TRACK:B0101`, `C74-LOM-TRACK:B0102`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-158` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-159 — Track.is_part_of_selection

**D-current-public/target-U.** For the documented Track context, `is_part_of_selection` is a direct properties declaration with source type `bool` and documented get role. No additional member-specific behavior is stated beyond its heading and access declaration. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `bool`; access `get`; result type `bool`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-TRACK member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-TRACK:B0002`, `C74-LOM-TRACK:B0004`, `C74-LOM-TRACK:B0103`, `C74-LOM-TRACK:B0104`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-159` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-160 — Track.is_showing_chains

**D-current-public/target-U.** For the documented Track context, `is_showing_chains` is a direct properties declaration with source type `bool` and documented get/set/observe role. Publisher member description: Get or set whether a track with an Instrument Rack device is currently showing its chains in Session View. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `bool`; access `get,set,observe`; result type `bool`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-TRACK member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-TRACK:B0002`, `C74-LOM-TRACK:B0004`, `C74-LOM-TRACK:B0105`, `C74-LOM-TRACK:B0106`, `C74-LOM-TRACK:B0107`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-160` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-161 — Track.is_visible

**D-current-public/target-U.** For the documented Track context, `is_visible` is a direct properties declaration with source type `bool` and documented get role. Publisher member description: 0 = track is hidden in a folded Group Track. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `bool`; access `get`; result type `bool`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-TRACK member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-TRACK:B0002`, `C74-LOM-TRACK:B0004`, `C74-LOM-TRACK:B0108`, `C74-LOM-TRACK:B0109`, `C74-LOM-TRACK:B0110`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-161` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-162 — Track.mute

**D-current-public/target-U.** For the documented Track context, `mute` is a direct properties declaration with source type `bool` and documented get/set/observe role. Publisher member description: [not in master track] The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `bool`; access `get,set,observe`; result type `bool`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-TRACK member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-TRACK:B0002`, `C74-LOM-TRACK:B0004`, `C74-LOM-TRACK:B0111`, `C74-LOM-TRACK:B0112`, `C74-LOM-TRACK:B0113`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-162` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-163 — Track.muted_via_solo

**D-current-public/target-U.** For the documented Track context, `muted_via_solo` is a direct properties declaration with source type `bool` and documented get/observe role. Publisher member description: 1 = the track or chain is muted due to Solo being active on at least one other track. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `bool`; access `get,observe`; result type `bool`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-TRACK member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-TRACK:B0002`, `C74-LOM-TRACK:B0004`, `C74-LOM-TRACK:B0114`, `C74-LOM-TRACK:B0115`, `C74-LOM-TRACK:B0116`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-163` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-164 — Track.name

**D-current-public/target-U.** For the documented Track context, `name` is a direct properties declaration with source type `symbol` and documented get/set/observe role. Publisher member description: As shown in track header. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `symbol`; access `get,set,observe`; result type `symbol`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-TRACK member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-TRACK:B0002`, `C74-LOM-TRACK:B0004`, `C74-LOM-TRACK:B0117`, `C74-LOM-TRACK:B0118`, `C74-LOM-TRACK:B0119`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-164` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-165 — Track.output_meter_left

**D-current-public/target-U.** For the documented Track context, `output_meter_left` is a direct properties declaration with source type `float` and documented get/observe role. Publisher member description: Smoothed momentary peak value of left channel output meter, 0.0 to 1.0. For tracks with audio output only. This value corresponds to the meters shown in Live. Please take into account that the left/right audio meters add a significant load to Live GUI resource usage. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `float`; access `get,observe`; result type `float`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-TRACK member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-TRACK:B0002`, `C74-LOM-TRACK:B0004`, `C74-LOM-TRACK:B0120`, `C74-LOM-TRACK:B0121`, `C74-LOM-TRACK:B0122`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-165` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-166 — Track.output_meter_level

**D-current-public/target-U.** For the documented Track context, `output_meter_level` is a direct properties declaration with source type `float` and documented get/observe role. Publisher member description: Hold peak value of output meters of audio and MIDI tracks, 0.0 to 1.0. For audio tracks, it is the maximum of the left and right channels. The hold time is 1 second. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `float`; access `get,observe`; result type `float`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-TRACK member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-TRACK:B0002`, `C74-LOM-TRACK:B0004`, `C74-LOM-TRACK:B0123`, `C74-LOM-TRACK:B0124`, `C74-LOM-TRACK:B0125`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-166` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-167 — Track.output_meter_right

**D-current-public/target-U.** For the documented Track context, `output_meter_right` is a direct properties declaration with source type `float` and documented get/observe role. Publisher member description: Smoothed momentary peak value of right channel output meter, 0.0 to 1.0. For tracks with audio output only. This value corresponds to the meters shown in Live. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `float`; access `get,observe`; result type `float`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-TRACK member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-TRACK:B0002`, `C74-LOM-TRACK:B0004`, `C74-LOM-TRACK:B0126`, `C74-LOM-TRACK:B0127`, `C74-LOM-TRACK:B0128`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-167` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-168 — Track.performance_impact

**D-current-public/target-U.** For the documented Track context, `performance_impact` is a direct properties declaration with source type `float` and documented get/observe role. Publisher member description: Reports the performance impact of this track. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `float`; access `get,observe`; result type `float`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-TRACK member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-TRACK:B0002`, `C74-LOM-TRACK:B0004`, `C74-LOM-TRACK:B0129`, `C74-LOM-TRACK:B0130`, `C74-LOM-TRACK:B0131`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-168` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-169 — Track.output_routing_channel

**D-current-public/target-U.** For the documented Track context, `output_routing_channel` is a direct properties declaration with source type `dictionary` and documented get/set/observe role. Publisher member description: The currently selected target channel for the track's output routing. It's represented as a dictionary with the following keys: display_name [symbol] identifier [symbol] Can be set to all values found in the track's available_output_routing_channels. Not available on the master track. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `dictionary`; access `get,set,observe`; result type `dictionary`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-TRACK member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-TRACK:B0002`, `C74-LOM-TRACK:B0004`, `C74-LOM-TRACK:B0132`, `C74-LOM-TRACK:B0133`, `C74-LOM-TRACK:B0134`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-169` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-170 — Track.output_routing_type

**D-current-public/target-U.** For the documented Track context, `output_routing_type` is a direct properties declaration with source type `dictionary` and documented get/set/observe role. Publisher member description: The currently selected target type for the track's output routing. It's represented as a dictionary with the following keys: display_name [symbol] identifier [symbol] Can be set to all values found in the track's available_output_routing_types. Not available on the master track. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `dictionary`; access `get,set,observe`; result type `dictionary`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-TRACK member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-TRACK:B0002`, `C74-LOM-TRACK:B0004`, `C74-LOM-TRACK:B0135`, `C74-LOM-TRACK:B0136`, `C74-LOM-TRACK:B0137`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-170` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-171 — Track.playing_slot_index

**D-current-public/target-U.** For the documented Track context, `playing_slot_index` is a direct properties declaration with source type `int` and documented get/observe role. Publisher member description: First slot has index 0, -2 = Clip Stop slot fired in Session View, -1 = Arrangement recording with no Session clip playing. [not in return/master tracks] The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `int`; access `get,observe`; result type `int`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-TRACK member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-TRACK:B0002`, `C74-LOM-TRACK:B0004`, `C74-LOM-TRACK:B0138`, `C74-LOM-TRACK:B0139`, `C74-LOM-TRACK:B0140`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-171` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-172 — Track.solo

**D-current-public/target-U.** For the documented Track context, `solo` is a direct properties declaration with source type `bool` and documented get/set/observe role. Publisher member description: Remark: when setting this property, the exclusive Solo logic is bypassed, so you have to unsolo the other tracks yourself. [not in master track] The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `bool`; access `get,set,observe`; result type `bool`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-TRACK member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-TRACK:B0002`, `C74-LOM-TRACK:B0004`, `C74-LOM-TRACK:B0141`, `C74-LOM-TRACK:B0142`, `C74-LOM-TRACK:B0143`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-172` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-173 — Track.create_audio_clip

**D-current-public/target-U.** For the documented Track context, `create_audio_clip` is a direct functions declaration and documented call role. Publisher member description: Parameters: file_path [symbol] position [float] Given an absolute path to a valid audio file in a supported format, creates an audio clip that references the file at the specified position in the arrangement view. Prints an error if the track is not an audio track, if the track is frozen, or if the track is being recorded into. The position must be within the range [0., 1576800]. See the ClipSlot.create_audio_clip function if you need to create audio clips in session view instead. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `unstated`. Arguments, in source order: `file_path` (symbol, optionality unstated); `position` (float, optionality unstated).

Evidence: [C74-LOM-TRACK member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-TRACK:B0002`, `C74-LOM-TRACK:B0004`, `C74-LOM-TRACK:B0145`, `C74-LOM-TRACK:B0146`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-173`, `LCS-BRANCH-011` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-174 — Track.create_midi_clip

**D-current-public/target-U.** For the documented Track context, `create_midi_clip` is a direct functions declaration and documented call role. Publisher member description: Parameters: start_time [float] length [float] Creates an empty MIDI clip and inserts it into the arrangement at the specified time. Throws an error when called on a non-MIDI track or a frozen track, when the specified time is outside the [0., 1576800.] range, or when the track is currently being recorded into. See the ClipSlot.create_clip function if you need to create audio clips in session view instead. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `unstated`. Arguments, in source order: `start_time` (float, optionality unstated); `length` (float, optionality unstated).

Evidence: [C74-LOM-TRACK member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-TRACK:B0002`, `C74-LOM-TRACK:B0004`, `C74-LOM-TRACK:B0147`, `C74-LOM-TRACK:B0148`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-174`, `LCS-BRANCH-012` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-175 — Track.create_take_lane

**D-current-public/target-U.** For the documented Track context, `create_take_lane` is a direct functions declaration and documented call role. Publisher member description: Creates a take lane for this track. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `unstated`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-TRACK member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-TRACK:B0002`, `C74-LOM-TRACK:B0004`, `C74-LOM-TRACK:B0149`, `C74-LOM-TRACK:B0150`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-175` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-176 — Track.delete_clip

**D-current-public/target-U.** For the documented Track context, `delete_clip` is a direct functions declaration and documented call role. Publisher member description: Parameter: clip Delete the given clip. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `unstated`. Arguments, in source order: `clip` (type unstated, optionality unstated).

Evidence: [C74-LOM-TRACK member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-TRACK:B0002`, `C74-LOM-TRACK:B0004`, `C74-LOM-TRACK:B0151`, `C74-LOM-TRACK:B0152`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-176` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-177 — Track.delete_device

**D-current-public/target-U.** For the documented Track context, `delete_device` is a direct functions declaration and documented call role. Publisher member description: Parameter: index Delete the device at the given index. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `unstated`. Arguments, in source order: `index` (type unstated, optionality unstated).

Evidence: [C74-LOM-TRACK member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-TRACK:B0002`, `C74-LOM-TRACK:B0004`, `C74-LOM-TRACK:B0153`, `C74-LOM-TRACK:B0154`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-177` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-178 — Track.duplicate_clip_slot

**D-current-public/target-U.** For the documented Track context, `duplicate_clip_slot` is a direct functions declaration and documented call role. Publisher member description: Parameter: index Works like 'Duplicate' in a clip's context menu. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `unstated`. Arguments, in source order: `index` (type unstated, optionality unstated).

Evidence: [C74-LOM-TRACK member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-TRACK:B0002`, `C74-LOM-TRACK:B0004`, `C74-LOM-TRACK:B0155`, `C74-LOM-TRACK:B0156`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-178` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-179 — Track.duplicate_clip_to_arrangement

**D-current-public/target-U.** For the documented Track context, `duplicate_clip_to_arrangement` is a direct functions declaration and documented call role. Publisher member description: Parameters: clip``destination_time [float] Duplicate the given clip to the Arrangement, placing it at the given destination_time in beats. The source clip can be a session or an arrangement clip. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `unstated`. Arguments, in source order: `clip` (type unstated, optionality unstated); `destination_time` (float, optionality unstated).

Evidence: [C74-LOM-TRACK member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-TRACK:B0002`, `C74-LOM-TRACK:B0004`, `C74-LOM-TRACK:B0157`, `C74-LOM-TRACK:B0158`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-179` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-180 — Track.insert_device

**D-current-public/target-U.** For the documented Track context, `insert_device` is a direct functions declaration and documented call role. Publisher member description: Parameters: device_name [symbol] target_index [int] (optional) Attempts to insert the device specified by device_name at the given index in the track's device chain. If no index is provided, attempts to insert the device at the end of the chain. Throws an error if insertion is not possible. device_name is the name as it appears in the UI of Live. Not all indices are valid. As can be expected, indices outside of the range defined by the current length of the device chain are invalid, but there are other limitations: for example, a MIDI effect can't be inserted after an instrument. The rule of thumb is that if an index would be invalid when inserting using the mouse, it's invalid here. At the moment, only native Live devices can be inserted. Max for Live devices and plug-in are not supported. Available since Live 12.3. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `unstated`. Arguments, in source order: `device_name` (symbol, optionality unstated); `target_index` (int, optionality optional).

Evidence: [C74-LOM-TRACK member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-TRACK:B0002`, `C74-LOM-TRACK:B0004`, `C74-LOM-TRACK:B0159`, `C74-LOM-TRACK:B0160`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-180`, `LCS-BRANCH-013` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-181 — Track.jump_in_running_session_clip

**D-current-public/target-U.** For the documented Track context, `jump_in_running_session_clip` is a direct functions declaration and documented call role. Publisher member description: Parameter: beats beats [float] is the amount to jump relatively to the current clip position. Modify playback position in running Session clip, if any. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `unstated`. Arguments, in source order: `beats` (float, optionality unstated).

Evidence: [C74-LOM-TRACK member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-TRACK:B0002`, `C74-LOM-TRACK:B0004`, `C74-LOM-TRACK:B0161`, `C74-LOM-TRACK:B0162`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-181` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-182 — Track.stop_all_clips

**D-current-public/target-U.** For the documented Track context, `stop_all_clips` is a direct functions declaration and documented call role. Publisher member description: Stops all playing and fired clips in this track. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `unstated`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-TRACK member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-TRACK:B0002`, `C74-LOM-TRACK:B0004`, `C74-LOM-TRACK:B0163`, `C74-LOM-TRACK:B0164`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-182` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

## Track.View

### REQ-LAPI-CORE-183 — Track.View.selected_device

**D-current-public/target-U.** For the documented Track.View context, `selected_device` is a direct children declaration with source type `Device` and documented get/observe role. Publisher member description: The selected device or the first selected device (in case of multi/group selection). The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `Device`; access `get,observe`; result type `Device`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-TRACK_VIEW member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-TRACK_VIEW:B0002`, `C74-LOM-TRACK_VIEW:B0004`, `C74-LOM-TRACK_VIEW:B0006`, `C74-LOM-TRACK_VIEW:B0007`, `C74-LOM-TRACK_VIEW:B0008`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-183` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-184 — Track.View.device_insert_mode

**D-current-public/target-U.** For the documented Track.View context, `device_insert_mode` is a direct properties declaration with source type `int` and documented get/set/observe role. Publisher member description: Determines where a device will be inserted when loaded from the browser. 0 = add device at the end, 1 = add device to the left of the selected device, 2 = add device to the right of the selected device. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `int`; access `get,set,observe`; result type `int`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-TRACK_VIEW member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-TRACK_VIEW:B0002`, `C74-LOM-TRACK_VIEW:B0004`, `C74-LOM-TRACK_VIEW:B0010`, `C74-LOM-TRACK_VIEW:B0011`, `C74-LOM-TRACK_VIEW:B0012`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-184` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-185 — Track.View.is_collapsed

**D-current-public/target-U.** For the documented Track.View context, `is_collapsed` is a direct properties declaration with source type `bool` and documented get/set/observe role. Publisher member description: In Arrangement View: 1 = track collapsed, 0 = track opened. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `bool`; access `get,set,observe`; result type `bool`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-TRACK_VIEW member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-TRACK_VIEW:B0002`, `C74-LOM-TRACK_VIEW:B0004`, `C74-LOM-TRACK_VIEW:B0013`, `C74-LOM-TRACK_VIEW:B0014`, `C74-LOM-TRACK_VIEW:B0015`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-185` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-186 — Track.View.select_instrument

**D-current-public/target-U.** For the documented Track.View context, `select_instrument` is a direct functions declaration and documented call role. Publisher member description: Returns: bool 0 = there are no devices to select Selects track's instrument or first device, makes it visible and focuses on it. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `bool`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-TRACK_VIEW member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-TRACK_VIEW:B0002`, `C74-LOM-TRACK_VIEW:B0004`, `C74-LOM-TRACK_VIEW:B0017`, `C74-LOM-TRACK_VIEW:B0018`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-186`, `LCS-BRANCH-015` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

## Scene

### REQ-LAPI-CORE-187 — Scene.clip_slots

**D-current-public/target-U.** For the documented Scene context, `clip_slots` is a direct children declaration with source type `list of ClipSlot` and documented get/observe role. No additional member-specific behavior is stated beyond its heading and access declaration. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `list of ClipSlot`; access `get,observe`; result type `list of ClipSlot`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SCENE member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SCENE:B0002`, `C74-LOM-SCENE:B0004`, `C74-LOM-SCENE:B0006`, `C74-LOM-SCENE:B0007`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-187` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-188 — Scene.color

**D-current-public/target-U.** For the documented Scene context, `color` is a direct properties declaration with source type `int` and documented get/set/observe role. Publisher member description: The RGB value of the scene's color in the form 0x00rrggbb or (2^16 * red) + (2^8) * green + blue, where red, green and blue are values from 0 (dark) to 255 (light). When setting the RGB value, the nearest color from the Scene color chooser is taken. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `int`; access `get,set,observe`; result type `int`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SCENE member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SCENE:B0002`, `C74-LOM-SCENE:B0004`, `C74-LOM-SCENE:B0009`, `C74-LOM-SCENE:B0010`, `C74-LOM-SCENE:B0011`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-188` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-189 — Scene.color_index

**D-current-public/target-U.** For the documented Scene context, `color_index` is a direct properties declaration with source type `long` and documented get/set/observe role. Publisher member description: The color index of the scene. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `long`; access `get,set,observe`; result type `long`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SCENE member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SCENE:B0002`, `C74-LOM-SCENE:B0004`, `C74-LOM-SCENE:B0012`, `C74-LOM-SCENE:B0013`, `C74-LOM-SCENE:B0014`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-189` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-190 — Scene.is_empty

**D-current-public/target-U.** For the documented Scene context, `is_empty` is a direct properties declaration with source type `bool` and documented get role. Publisher member description: 1 = none of the slots in the scene is filled. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `bool`; access `get`; result type `bool`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SCENE member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SCENE:B0002`, `C74-LOM-SCENE:B0004`, `C74-LOM-SCENE:B0015`, `C74-LOM-SCENE:B0016`, `C74-LOM-SCENE:B0017`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-190` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-191 — Scene.is_triggered

**D-current-public/target-U.** For the documented Scene context, `is_triggered` is a direct properties declaration with source type `bool` and documented get/observe role. Publisher member description: 1 = scene is blinking. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `bool`; access `get,observe`; result type `bool`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SCENE member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SCENE:B0002`, `C74-LOM-SCENE:B0004`, `C74-LOM-SCENE:B0018`, `C74-LOM-SCENE:B0019`, `C74-LOM-SCENE:B0020`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-191` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-192 — Scene.name

**D-current-public/target-U.** For the documented Scene context, `name` is a direct properties declaration with source type `symbol` and documented get/set/observe role. Publisher member description: The name of the scene. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `symbol`; access `get,set,observe`; result type `symbol`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SCENE member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SCENE:B0002`, `C74-LOM-SCENE:B0004`, `C74-LOM-SCENE:B0021`, `C74-LOM-SCENE:B0022`, `C74-LOM-SCENE:B0023`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-192` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-193 — Scene.tempo

**D-current-public/target-U.** For the documented Scene context, `tempo` is a direct properties declaration with source type `float` and documented get/set/observe role. Publisher member description: The scene's tempo. Returns -1 if the scene tempo is disabled. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `float`; access `get,set,observe`; result type `float`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SCENE member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SCENE:B0002`, `C74-LOM-SCENE:B0004`, `C74-LOM-SCENE:B0024`, `C74-LOM-SCENE:B0025`, `C74-LOM-SCENE:B0026`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-193`, `LCS-BRANCH-017` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-194 — Scene.tempo_enabled

**D-current-public/target-U.** For the documented Scene context, `tempo_enabled` is a direct properties declaration with source type `bool` and documented get/set/observe role. Publisher member description: The active state of the scene tempo. When disabled, the scene will use the song's tempo, and the tempo value returned will be -1. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `bool`; access `get,set,observe`; result type `bool`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SCENE member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SCENE:B0002`, `C74-LOM-SCENE:B0004`, `C74-LOM-SCENE:B0027`, `C74-LOM-SCENE:B0028`, `C74-LOM-SCENE:B0029`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-194` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-195 — Scene.time_signature_numerator

**D-current-public/target-U.** For the documented Scene context, `time_signature_numerator` is a direct properties declaration with source type `int` and documented get/set/observe role. Publisher member description: The scene's time signature numerator. Returns -1 if the scene time signature is disabled. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `int`; access `get,set,observe`; result type `int`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SCENE member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SCENE:B0002`, `C74-LOM-SCENE:B0004`, `C74-LOM-SCENE:B0030`, `C74-LOM-SCENE:B0031`, `C74-LOM-SCENE:B0032`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-195` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-196 — Scene.time_signature_denominator

**D-current-public/target-U.** For the documented Scene context, `time_signature_denominator` is a direct properties declaration with source type `int` and documented get/set/observe role. Publisher member description: The scene's time signature denominator. Returns -1 if the scene time signature is disabled. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `int`; access `get,set,observe`; result type `int`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SCENE member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SCENE:B0002`, `C74-LOM-SCENE:B0004`, `C74-LOM-SCENE:B0033`, `C74-LOM-SCENE:B0034`, `C74-LOM-SCENE:B0035`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-196` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-197 — Scene.time_signature_enabled

**D-current-public/target-U.** For the documented Scene context, `time_signature_enabled` is a direct properties declaration with source type `bool` and documented get/set/observe role. Publisher member description: The active state of the scene time signature. When disabled, the scene will use the song's time signature, and the time signature values returned will be -1. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `bool`; access `get,set,observe`; result type `bool`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-SCENE member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SCENE:B0002`, `C74-LOM-SCENE:B0004`, `C74-LOM-SCENE:B0036`, `C74-LOM-SCENE:B0037`, `C74-LOM-SCENE:B0038`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-197` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-198 — Scene.fire

**D-current-public/target-U.** For the documented Scene context, `fire` is a direct functions declaration and documented call role. Publisher member description: Parameter: force_legato (optional) [bool] can_select_scene_on_launch (optional) [bool] Fire all clip slots contained within the scene and select this scene. Starts recording of armed and empty tracks within a Group Track in this scene if Preferences->Launch->Start Recording on Scene Launch is ON. Calling with force_legato = 1 (default = 0) will launch all clips immediately in Legato, independent of their launch mode. When calling with can_select_scene_on_launch = 0 (default = 1) the scene is fired without selecting it. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `unstated`. Arguments, in source order: `force_legato` (bool, optionality optional, source default 0); `can_select_scene_on_launch` (bool, optionality optional, source default 1).

Evidence: [C74-LOM-SCENE member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SCENE:B0002`, `C74-LOM-SCENE:B0004`, `C74-LOM-SCENE:B0040`, `C74-LOM-SCENE:B0041`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-198` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-199 — Scene.fire_as_selected

**D-current-public/target-U.** For the documented Scene context, `fire_as_selected` is a direct functions declaration and documented call role. Publisher member description: Parameter: force_legato (optional) [bool] Fire the selected scene, then select the next scene. It doesn't matter on which scene you are calling this function. Calling with force_legato = 1 (default = 0) will launch all clips immediately in Legato, independent of their launch mode. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `unstated`. Arguments, in source order: `force_legato` (bool, optionality optional, source default 0).

Evidence: [C74-LOM-SCENE member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SCENE:B0002`, `C74-LOM-SCENE:B0004`, `C74-LOM-SCENE:B0042`, `C74-LOM-SCENE:B0043`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-199`, `LCS-BRANCH-016` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-200 — Scene.set_fire_button_state

**D-current-public/target-U.** For the documented Scene context, `set_fire_button_state` is a direct functions declaration and documented call role. Publisher member description: Parameter: state [bool] If the state is set to 1, Live simulates pressing of scene button until the state is set to 0 or until the scene is stopped otherwise. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `unstated`. Arguments, in source order: `state` (bool, optionality unstated).

Evidence: [C74-LOM-SCENE member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-SCENE:B0002`, `C74-LOM-SCENE:B0004`, `C74-LOM-SCENE:B0044`, `C74-LOM-SCENE:B0045`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-200` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

## ClipSlot

### REQ-LAPI-CORE-201 — ClipSlot.clip

**D-current-public/target-U.** For the documented ClipSlot context, `clip` is a direct children declaration with source type `Clip` and documented get role. Publisher member description: id 0 if slot is empty The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `Clip`; access `get`; result type `Clip`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-CLIPSLOT member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-CLIPSLOT:B0002`, `C74-LOM-CLIPSLOT:B0004`, `C74-LOM-CLIPSLOT:B0006`, `C74-LOM-CLIPSLOT:B0007`, `C74-LOM-CLIPSLOT:B0008`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-201` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-202 — ClipSlot.color

**D-current-public/target-U.** For the documented ClipSlot context, `color` is a direct properties declaration with source type `long` and documented get/observe role. Publisher member description: The color of the first clip in the Group Track if the clip slot is a Group Track slot. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `long`; access `get,observe`; result type `long`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-CLIPSLOT member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-CLIPSLOT:B0002`, `C74-LOM-CLIPSLOT:B0004`, `C74-LOM-CLIPSLOT:B0010`, `C74-LOM-CLIPSLOT:B0011`, `C74-LOM-CLIPSLOT:B0012`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-202` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-203 — ClipSlot.color_index

**D-current-public/target-U.** For the documented ClipSlot context, `color_index` is a direct properties declaration with source type `long` and documented get/observe role. Publisher member description: The color index of the first clip in the Group Track if the clip slot is a Group Track slot. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `long`; access `get,observe`; result type `long`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-CLIPSLOT member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-CLIPSLOT:B0002`, `C74-LOM-CLIPSLOT:B0004`, `C74-LOM-CLIPSLOT:B0013`, `C74-LOM-CLIPSLOT:B0014`, `C74-LOM-CLIPSLOT:B0015`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-203` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-204 — ClipSlot.controls_other_clips

**D-current-public/target-U.** For the documented ClipSlot context, `controls_other_clips` is a direct properties declaration with source type `bool` and documented get/observe role. Publisher member description: 1 for a Group Track slot that has non-deactivated clips in the tracks within its group. Control of empty clip slots doesn't count. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `bool`; access `get,observe`; result type `bool`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-CLIPSLOT member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-CLIPSLOT:B0002`, `C74-LOM-CLIPSLOT:B0004`, `C74-LOM-CLIPSLOT:B0016`, `C74-LOM-CLIPSLOT:B0017`, `C74-LOM-CLIPSLOT:B0018`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-204` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-205 — ClipSlot.has_clip

**D-current-public/target-U.** For the documented ClipSlot context, `has_clip` is a direct properties declaration with source type `bool` and documented get/observe role. Publisher member description: 1 = a clip exists in this clip slot. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `bool`; access `get,observe`; result type `bool`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-CLIPSLOT member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-CLIPSLOT:B0002`, `C74-LOM-CLIPSLOT:B0004`, `C74-LOM-CLIPSLOT:B0019`, `C74-LOM-CLIPSLOT:B0020`, `C74-LOM-CLIPSLOT:B0021`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-205` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-206 — ClipSlot.has_stop_button

**D-current-public/target-U.** For the documented ClipSlot context, `has_stop_button` is a direct properties declaration with source type `bool` and documented get/set/observe role. Publisher member description: 1 = this clip stops its track (or tracks within a Group Track). The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `bool`; access `get,set,observe`; result type `bool`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-CLIPSLOT member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-CLIPSLOT:B0002`, `C74-LOM-CLIPSLOT:B0004`, `C74-LOM-CLIPSLOT:B0022`, `C74-LOM-CLIPSLOT:B0023`, `C74-LOM-CLIPSLOT:B0024`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-206` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-207 — ClipSlot.is_group_slot

**D-current-public/target-U.** For the documented ClipSlot context, `is_group_slot` is a direct properties declaration with source type `bool` and documented get role. Publisher member description: 1 = this clip slot is a Group Track slot. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `bool`; access `get`; result type `bool`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-CLIPSLOT member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-CLIPSLOT:B0002`, `C74-LOM-CLIPSLOT:B0004`, `C74-LOM-CLIPSLOT:B0025`, `C74-LOM-CLIPSLOT:B0026`, `C74-LOM-CLIPSLOT:B0027`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-207` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-208 — ClipSlot.is_playing

**D-current-public/target-U.** For the documented ClipSlot context, `is_playing` is a direct properties declaration with source type `bool` and documented get role. Publisher member description: 1 = playing_status != 0, otherwise 0. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `bool`; access `get`; result type `bool`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-CLIPSLOT member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-CLIPSLOT:B0002`, `C74-LOM-CLIPSLOT:B0004`, `C74-LOM-CLIPSLOT:B0028`, `C74-LOM-CLIPSLOT:B0029`, `C74-LOM-CLIPSLOT:B0030`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-208` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-209 — ClipSlot.is_recording

**D-current-public/target-U.** For the documented ClipSlot context, `is_recording` is a direct properties declaration with source type `bool` and documented get role. Publisher member description: 1 = playing_status == 2, otherwise 0. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `bool`; access `get`; result type `bool`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-CLIPSLOT member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-CLIPSLOT:B0002`, `C74-LOM-CLIPSLOT:B0004`, `C74-LOM-CLIPSLOT:B0031`, `C74-LOM-CLIPSLOT:B0032`, `C74-LOM-CLIPSLOT:B0033`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-209` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-210 — ClipSlot.is_triggered

**D-current-public/target-U.** For the documented ClipSlot context, `is_triggered` is a direct properties declaration with source type `bool` and documented get/observe role. Publisher member description: 1 = clip slot button (Clip Launch, Clip Stop or Clip Record) or button of contained clip are blinking. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `bool`; access `get,observe`; result type `bool`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-CLIPSLOT member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-CLIPSLOT:B0002`, `C74-LOM-CLIPSLOT:B0004`, `C74-LOM-CLIPSLOT:B0034`, `C74-LOM-CLIPSLOT:B0035`, `C74-LOM-CLIPSLOT:B0036`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-210` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-211 — ClipSlot.playing_status

**D-current-public/target-U.** For the documented ClipSlot context, `playing_status` is a direct properties declaration with source type `int` and documented get/observe role. Publisher member description: 0 = all clips in tracks within a Group Track stopped or all tracks within a Group Track are empty. 1 = at least one clip in a track within a Group Track is playing. 2 = at least one clip in a track within a Group Track is playing or recording. Equals 0 if this is not a clip slot of a Group Track. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `int`; access `get,observe`; result type `int`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-CLIPSLOT member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-CLIPSLOT:B0002`, `C74-LOM-CLIPSLOT:B0004`, `C74-LOM-CLIPSLOT:B0037`, `C74-LOM-CLIPSLOT:B0038`, `C74-LOM-CLIPSLOT:B0039`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-211`, `LCS-BRANCH-018` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-212 — ClipSlot.will_record_on_start

**D-current-public/target-U.** For the documented ClipSlot context, `will_record_on_start` is a direct properties declaration with source type `bool` and documented get role. Publisher member description: 1 = clip slot will record on start. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `bool`; access `get`; result type `bool`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-CLIPSLOT member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-CLIPSLOT:B0002`, `C74-LOM-CLIPSLOT:B0004`, `C74-LOM-CLIPSLOT:B0040`, `C74-LOM-CLIPSLOT:B0041`, `C74-LOM-CLIPSLOT:B0042`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-212` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-213 — ClipSlot.create_audio_clip

**D-current-public/target-U.** For the documented ClipSlot context, `create_audio_clip` is a direct functions declaration and documented call role. Publisher member description: Parameter: path Given an absolute path to a valid audio file in a supported format, creates an audio clip that references the file in the clip slot. Throws an error if the clip slot doesn't belong to an audio track or if the track is frozen. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `unstated`. Arguments, in source order: `path` (type unstated, optionality unstated).

Evidence: [C74-LOM-CLIPSLOT member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-CLIPSLOT:B0002`, `C74-LOM-CLIPSLOT:B0004`, `C74-LOM-CLIPSLOT:B0044`, `C74-LOM-CLIPSLOT:B0045`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-213` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-214 — ClipSlot.create_clip

**D-current-public/target-U.** For the documented ClipSlot context, `create_clip` is a direct functions declaration and documented call role. Publisher member description: Parameter: length Length is given in beats and must be a greater value than 0.0. Can only be called on empty clip slots in MIDI tracks. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `unstated`. Arguments, in source order: `length` (type unstated, optionality unstated).

Evidence: [C74-LOM-CLIPSLOT member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-CLIPSLOT:B0002`, `C74-LOM-CLIPSLOT:B0004`, `C74-LOM-CLIPSLOT:B0046`, `C74-LOM-CLIPSLOT:B0047`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-214`, `LCS-BRANCH-019` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-215 — ClipSlot.delete_clip

**D-current-public/target-U.** For the documented ClipSlot context, `delete_clip` is a direct functions declaration and documented call role. Publisher member description: Deletes the contained clip. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `unstated`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-CLIPSLOT member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-CLIPSLOT:B0002`, `C74-LOM-CLIPSLOT:B0004`, `C74-LOM-CLIPSLOT:B0048`, `C74-LOM-CLIPSLOT:B0049`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-215` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-216 — ClipSlot.duplicate_clip_to

**D-current-public/target-U.** For the documented ClipSlot context, `duplicate_clip_to` is a direct functions declaration and documented call role. Publisher member description: Parameter: target_clip_slot [ClipSlot] Duplicates the slot's clip to the given clip slot, overriding the target clip slot's clip if it's not empty. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `unstated`. Arguments, in source order: `target_clip_slot` (ClipSlot, optionality unstated).

Evidence: [C74-LOM-CLIPSLOT member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-CLIPSLOT:B0002`, `C74-LOM-CLIPSLOT:B0004`, `C74-LOM-CLIPSLOT:B0050`, `C74-LOM-CLIPSLOT:B0051`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-216` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-217 — ClipSlot.fire

**D-current-public/target-U.** For the documented ClipSlot context, `fire` is a direct functions declaration and documented call role. Publisher member description: Parameter: record_length (optional) launch_quantization (optional) Fires the clip or triggers the Stop Button, if any. Starts recording if slot is empty and track is armed. Starts recording of armed and empty tracks within a Group Track if Preferences->Launch->Start Recording on Scene Launch is ON. If record_length is provided, the slot will record for the given length in beats. launch_quantization overrides the global quantization if provided. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `unstated`. Arguments, in source order: `record_length` (type unstated, optionality optional); `launch_quantization` (type unstated, optionality optional).

Evidence: [C74-LOM-CLIPSLOT member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-CLIPSLOT:B0002`, `C74-LOM-CLIPSLOT:B0004`, `C74-LOM-CLIPSLOT:B0052`, `C74-LOM-CLIPSLOT:B0053`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-217` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-218 — ClipSlot.set_fire_button_state

**D-current-public/target-U.** For the documented ClipSlot context, `set_fire_button_state` is a direct functions declaration and documented call role. Publisher member description: Parameter: state [bool] 1 = Live simulates pressing of Clip Launch button until the state is set to 0 or until the slot is stopped otherwise. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `unstated`. Arguments, in source order: `state` (bool, optionality unstated).

Evidence: [C74-LOM-CLIPSLOT member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-CLIPSLOT:B0002`, `C74-LOM-CLIPSLOT:B0004`, `C74-LOM-CLIPSLOT:B0054`, `C74-LOM-CLIPSLOT:B0055`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-218` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-219 — ClipSlot.stop

**D-current-public/target-U.** For the documented ClipSlot context, `stop` is a direct functions declaration and documented call role. Publisher member description: Stops playing or recording clips in this track or the tracks within the group, if any. It doesn't matter on which slot of the track you call this function. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `unstated`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-CLIPSLOT member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-CLIPSLOT:B0002`, `C74-LOM-CLIPSLOT:B0004`, `C74-LOM-CLIPSLOT:B0056`, `C74-LOM-CLIPSLOT:B0057`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-219` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

## CuePoint

### REQ-LAPI-CORE-220 — CuePoint.name

**D-current-public/target-U.** For the documented CuePoint context, `name` is a direct properties declaration with source type `symbol` and documented get/set/observe role. No additional member-specific behavior is stated beyond its heading and access declaration. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `symbol`; access `get,set,observe`; result type `symbol`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-CUEPOINT member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-CUEPOINT:B0002`, `C74-LOM-CUEPOINT:B0004`, `C74-LOM-CUEPOINT:B0006`, `C74-LOM-CUEPOINT:B0007`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-220` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-221 — CuePoint.time

**D-current-public/target-U.** For the documented CuePoint context, `time` is a direct properties declaration with source type `float` and documented get/observe role. Publisher member description: Arrangement position of the marker in beats. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `float`; access `get,observe`; result type `float`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-CUEPOINT member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-CUEPOINT:B0002`, `C74-LOM-CUEPOINT:B0004`, `C74-LOM-CUEPOINT:B0008`, `C74-LOM-CUEPOINT:B0009`, `C74-LOM-CUEPOINT:B0010`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-221` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-222 — CuePoint.jump

**D-current-public/target-U.** For the documented CuePoint context, `jump` is a direct functions declaration and documented call role. Publisher member description: Set current Arrangement playback position to marker, quantized if song is playing. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `unstated`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-CUEPOINT member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-CUEPOINT:B0002`, `C74-LOM-CUEPOINT:B0004`, `C74-LOM-CUEPOINT:B0012`, `C74-LOM-CUEPOINT:B0013`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-222` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

## TakeLane

### REQ-LAPI-CORE-223 — TakeLane.arrangement_clips

**D-current-public/target-U.** For the documented TakeLane context, `arrangement_clips` is a direct children declaration with source type `list of Clip` and documented get/observe role. Publisher member description: The list of this take lane's Arrangement View clip IDs The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `list of Clip`; access `get,observe`; result type `list of Clip`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-TAKELANE member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-TAKELANE:B0002`, `C74-LOM-TAKELANE:B0004`, `C74-LOM-TAKELANE:B0006`, `C74-LOM-TAKELANE:B0007`, `C74-LOM-TAKELANE:B0008`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-223` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-224 — TakeLane.name

**D-current-public/target-U.** For the documented TakeLane context, `name` is a direct properties declaration with source type `symbol` and documented get/set/observe role. Publisher member description: The name as shown in the take lane header. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `symbol`; access `get,set,observe`; result type `symbol`. Arguments: unstated; no empty-signature inference.

Evidence: [C74-LOM-TAKELANE member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-TAKELANE:B0002`, `C74-LOM-TAKELANE:B0004`, `C74-LOM-TAKELANE:B0010`, `C74-LOM-TAKELANE:B0011`, `C74-LOM-TAKELANE:B0012`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-224` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-225 — TakeLane.create_audio_clip

**D-current-public/target-U.** For the documented TakeLane context, `create_audio_clip` is a direct functions declaration and documented call role. Publisher member description: Parameters: file_path [symbol] start_time [float] Given a valid audio file in a supported format, passing its absolute path (on Mac, starting with /Volumes/(drive name)/) creates an audio clip referencing the file in the arrangement view at the specified start_time in beats. Prints an error if the track is not an audio track, if the track is frozen or if the track is being recorded into. start_time must be within the range [0., 1576800]. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `unstated`. Arguments, in source order: `file_path` (symbol, optionality unstated); `start_time` (float, optionality unstated).

Evidence: [C74-LOM-TAKELANE member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-TAKELANE:B0002`, `C74-LOM-TAKELANE:B0004`, `C74-LOM-TAKELANE:B0014`, `C74-LOM-TAKELANE:B0015`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-225`, `LCS-BRANCH-020` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-226 — TakeLane.create_midi_clip

**D-current-public/target-U.** For the documented TakeLane context, `create_midi_clip` is a direct functions declaration and documented call role. Publisher member description: Parameters: start_time [float] length [float] Creates an empty MIDI clip with the specified length in beats and inserts it into the arrangement at the specified start_time in beats. Prints an error if the track is not a MIDI track, if the track is frozen or when the track is currently being recorded into. start_time must be within the range [0., 1576800]. The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.

Source fields: value type `unstated`; access `function-call role`; result type `unstated`. Arguments, in source order: `start_time` (float, optionality unstated); `length` (float, optionality unstated).

Evidence: [C74-LOM-TAKELANE member blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/source-blocks.json); exact keys `C74-LOM-TAKELANE:B0002`, `C74-LOM-TAKELANE:B0004`, `C74-LOM-TAKELANE:B0016`, `C74-LOM-TAKELANE:B0017`; [typed ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/member-ledger.json).

Finite cases: `LCS-226` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

## Required unknowns

### REQ-LAPI-CORE-U-TYPES — Missing argument/result and value grammar

**U/target-U.** Unannotated function argument/result types, omitted parameter lists, optionality, empty/symbol/unicode/list/object/dictionary representations, error channels and enum conversion are unknown. Omitted return prose does not imply void.

Finite cases: `LCS-U-TYPES` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-U-CONTEXT — Unresolved source context and alias predicates

**U/target-U.** Arranger/Arrangement and empty view-name spelling, ClipSlot group status overlap, Track MIDI-to-Session cross-reference wording and thin member descriptions remain unresolved; no naming inference fills missing effects.

Finite cases: `LCS-U-CONTEXT` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-U-TARGET — Exact build and cross-owner reconciliation

**U/target-U.** The public index declares 12.4.5. Exact 12.4.3 access, types, ranges, defaults, optionality, membership and outcomes remain unknown even for features described since 12.3 or 11.0. No existing finite native or stored law is overwritten.

Finite cases: `LCS-U-TARGET` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-U-LIFECYCLE — Persistence and transaction boundaries

**U/target-U.** Member-specific save/reopen, undo grouping, redo, cancellation, failure, source loss, Set replacement, IDs and teardown behavior are not fully specified by these declarations or generic bridge prose.

Finite cases: `LCS-U-LIFECYCLE`, `LCS-U-UNDO`, `LCS-U-CANCEL`, `LCS-U-TEARDOWN`, `LCS-U-CONCURRENCY` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-U-TIME — Timing signal and observation limits

**U/target-U.** Scheduling, quantization interaction, clock units/conversion, rates, automation precedence, notification count/order, meter smoothing/hold, audible continuity and real-time capacity have no new calibrated target oracle.

Finite cases: `LCS-U-TIME`, `LCS-U-AUTOMATION`, `LCS-U-RATE`, `LCS-U-TRANSPORT` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-U-INHERITANCE — Unmapped and inherited API surface

**U/target-U.** Only the 226 explicit direct members in these ten references are mapped here. Other 35 references/362 direct declarations, inherited members, roots/aliases and arbitrary bridge/protocol/Max compatibility remain outside this partial mapping and unresolved.

Finite cases: `LCS-U-INHERITANCE` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-U-HARDWARE — Controller and synchronization availability

**U/target-U.** ControlSurface entries, Push-specific implicit arm/modulation mapping, Link/Tap/network and physical-port observations require independently supported actual hardware/firmware/context; no surrogate establishes support.

Finite cases: `LCS-U-HARDWARE` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

### REQ-LAPI-CORE-U-ERRORS — Creation deletion movement and availability gaps

**U/target-U.** Track/list endpoints, frozen/recording and media eligibility, deletion of absent objects, unsupported insertion, selection loss and partial failures require more context-specific evidence. Prints versus throws and unspecified errors are not one error protocol.

Finite cases: `LCS-U-ERRORS`, `LCS-U-SOURCE-LOSS` in the [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json).

## Finite cases and evidence limits

The [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/cases.json) has 262 finite future proposals.
Each direct declaration has its own positive case; get/set/observe clauses are
separate stated steps within that case, requiring independent admitted states
and productive observation. Twenty additional per-member probes cover selected
negative/boundary/source contexts. Sixteen U cases retain types, version,
inheritance, hardware, recovery, persistence, undo/redo, cancel, source loss,
automation, rate, transport, concurrency and teardown. This is not all branch
combinations or all per-member lifecycle coverage. Full argument/error/return
grammar and every required unknown need further evidence before closure.

The [sources](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/sources.json), [counts](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/counts.json),
[input pins](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/inventory-pins.json), [owner pins](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/owner-pins.json)
and [author seal](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/manifest-author-r2.json) preserve immutable
R1 evidence and canonical snapshots. The local validator is read-only after
freeze; hash/parser checks prove identity and mapping, not runtime behavior.
Root integrates catalogs and independent review. No handoff is released here.
