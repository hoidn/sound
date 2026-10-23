---
id: SPEC-SETTINGS-LEARNING-WORKFLOWS
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3
---

# Settings, Learn View and Info View workflows

This partial F-07/F-08 contract owns newly documented settings/help entry points,
appearance and Learn/Info View roles. The [coverage design](../research/full-live-specification-design.md)
governs closure; [research](../research/settings-learning-workflows.md) owns exact
evidence. It is not a complete preference, delivery or learning-content contract.

**D12/target-U:** the captured current Version12 chapter supports documentary
prose only. All exact12.4.3 outcomes/comparisons, including Learn View and newer
settings/Places availability, remain null/U/unexecuted. No figures, UI, content,
audio/video, network/account, installer/update, native code or candidate ran.
Named UI roles do not prove content availability or private service behavior.

## Canonical boundaries

[Keyboard navigation](keyboard-navigation.md) owns preferred language, focus,
Tab/Wrap/arrow options and settings traversal. [Clip View](clip-view-workflows.md)
REQ004 owns clip Info Text; REQ005's new-clip inheritance wording needs the explicit
Clip Color preference context below. [Session](session-view-workflows.md) retains
its particular entry points. This page adds only track/device notes and general
Info View presentation. No existing sealed owner is silently revised.

[Media](media-file-workflows.md) owns analysis files, destructive Sample Editor
and decoding cache; [recording](recording-comping.md) owns temporary recordings
and format defaults; [project/media](project-media-workflows.md) owns file/project
operations and library content. [Max host](max-for-live-hosting.md),
[plug-in hosting](plugin-hosting.md), [routing](routing-monitoring-latency.md),
[synchronization](synchronization-workflows.md), [clip launch](session-launch-workflows.md)
and [Warp](warp-markers.md) retain their settings behavior. The chapter's tab
summaries route to those owners rather than duplicate their contracts.

## Requirements

Use [future owned setups](../../analysis/ableton-live-12.4.3/full-spec-v1/settings-learning/fixtures.json)
with explicit feature availability/focus/preferences and paired positive baselines.
Compound clauses remain partial until each branch, state and required case kind
has evidence. Numeric/color/RNG/time/audio/codec comparisons remain unknown.

### REQ-SETTINGS-LEARNING-001 — Learn content and resources

**D12/target-U.** Learn View provides structured modules with video and explanatory text; modules can be added without a Live update. Its home page links to the manual and Knowledge Base. Available lesson catalog, delivery service, download/cache and authenticity protocol remain unknown.

Evidence: `SET-B008`; [exact routes](#analysis-only-evidence).

### REQ-SETTINGS-LEARNING-002 — Learn entry and in-session page retention

**D12/target-U.** Close Learn with its X and reopen from Help or Ctrl+Alt+7 Windows/Cmd+Option+7 macOS. Before Live closes, reopening returns to the last visited page. First-open default visibility is documentary only, not an observed target constructor default; application-restart restoration remains unknown.

Evidence: `SET-B009`; [exact routes](#analysis-only-evidence).

### REQ-SETTINGS-LEARNING-003 — Lesson filter, completion and navigation

**D12/target-U.** Lessons can be filtered by topic and marked completed. Complete Lesson gives a home-page check mark. Lesson Home or < Lessons returns home; bottom related-lesson links are described only when home shows all lessons. Completion persistence across application/reinstall/account contexts is unknown.

Evidence: `SET-B010`, `SET-B011`, `SET-B012`; [exact routes](#analysis-only-evidence).

### REQ-SETTINGS-LEARNING-004 — Lesson player controls

**D12/target-U.** The lesson player offers play/pause, progress scrubbing, volume, subtitles and picture-in-picture controls. This lists named public controls, not decoder support, actual video/audio output, subtitle languages or timing precision.

Evidence: `SET-B013`; [exact routes](#analysis-only-evidence).

### REQ-SETTINGS-LEARNING-005 — Picture-in-picture window transitions

**D12/target-U.** Opening lesson picture-in-picture closes Learn and allows window movement/resizing. Its X closes it; Learn View arrow reopens Learn and closes picture-in-picture. The source describes always above application windows, including other apps; the arrow then brings Live into focus. OS permissions, exclusive/fullscreen conflicts and geometry persistence remain unknown.

Evidence: `SET-B014`, `SET-B016`, `SET-B017`; [exact routes](#analysis-only-evidence).

### REQ-SETTINGS-LEARNING-006 — Lesson playback position and seek roles

**D12/target-U.** Within picture-in-picture, hover exposes progress and backward/forward 15 controls. While Live remains open the lesson video resumes from the prior position, even after closing either view during playback. Exact seek interval units, endpoint rounding, transport ordering, audio/video timing and decoder output are not calibrated here.

Evidence: `SET-B015`; [exact routes](#analysis-only-evidence).

### REQ-SETTINGS-LEARNING-007 — Learn connectivity and reload

**D12/target-U.** Learn View requires an Internet connection. Following loss and reconnection, Reload refreshes it. The text does not establish offline-cache behavior, authentication, network error text, retry policy or recovery deadline.

Evidence: `SET-B018`; [exact routes](#analysis-only-evidence).

### REQ-SETTINGS-LEARNING-008 — Info View contextual help and visibility

**D12/target-U.** Info View displays the hovered UI element name/function. Its bottom-left view toggle or ? key shows/hides it. Exact help strings, keyboard-layout/focus conflicts, hover delay and accessibility announcements are unknown; global key context remains with keyboard navigation.

Evidence: `SET-B020`, `SET-B021`; [exact routes](#analysis-only-evidence).

### REQ-SETTINGS-LEARNING-009 — Track and device Info Text entry points

**D12/target-U.** Track/device context-menu Edit Info Text opens editable notes in Info View; the chapter describes notes saved/displayed with the Set. Clip Edit Info Text remains owned by REQ-CLIP-VIEW-004, not duplicated here. Text codec/limits, undo and exact persistence/error transactions remain unknown.

Evidence: `SET-B022`; [exact routes](#analysis-only-evidence).

### REQ-SETTINGS-LEARNING-010 — Platform Settings entry

**D12/target-U.** Settings opens from Options on Windows or Live menu on macOS, or Ctrl+, Windows/Cmd+, macOS. Keyboard traversal/close/page shortcuts and preferred-language selection remain with keyboard-navigation; no crossplatform key equivalence is inferred.

Evidence: `SET-B028`, `SET-B029`; [exact routes](#analysis-only-evidence).

### REQ-SETTINGS-LEARNING-011 — Window zoom roles

**D12/target-U.** Display settings offer separate zoom for main window, second window if open, and Settings window. Mouse adjustment of Settings zoom updates after mouse-button release. Offered range, scale arithmetic, permonitor layout and persistence are unknown; preferred language belongs to keyboard-navigation.

Evidence: `SET-B032`; [exact routes](#analysis-only-evidence).

### REQ-SETTINGS-LEARNING-012 — Display option roles

**D12/target-U.** Display Options includes Outline View in Focus, scrollbar presentation, Arrangement/clip Follow and UI-label visibility. Enabling Outline draws a border around the selected view. Exact option enums and underlying Follow navigation/transport behavior remain with relevant view owners or unknown.

Evidence: `SET-B033`; [exact routes](#analysis-only-evidence).

### REQ-SETTINGS-LEARNING-013 — Mouse and pen settings

**D12/target-U.** Mouse and Pen Input exposes Pen Tablet Mode, permanent scrub areas and pitch-locked MIDI drawing options. Actual pen protocol, gesture thresholds, scrubbing audio and note drawing remain with editing owners or unknown.

Evidence: `SET-B035`; [exact routes](#analysis-only-evidence).

### REQ-SETTINGS-LEARNING-014 — Suppressed warning restoration

**D12/target-U.** Application Options can restore warning dialogs previously suppressed through Don't Show Again. The warning set, exact dialog text, perwarning/global scope, account and restart retention remain unknown.

Evidence: `SET-B036`; [exact routes](#analysis-only-evidence).

### REQ-SETTINGS-LEARNING-015 — Theme and appearance controls

**D12/target-U.** Theme offers a color scheme, light/dark or OS-follow appearance, warm/cool/neutral palette tone and high contrast. Customization adjusts grid opacity, brightness, color intensity and hue. Numeric ranges, color values, assets and OS-change propagation timing remain unknown.

Evidence: `SET-B039`, `SET-B040`; [exact routes](#analysis-only-evidence).

### REQ-SETTINGS-LEARNING-016 — Track and clip color preferences

**D12/target-U.** Track and Clip Colors controls automatic track colors, a default track color and Reduced Automatic Colors. Clip Color may choose random colors or track color for new clips. No palette enumeration, random distribution or color-sequence oracle follows. This preference context qualifies the Clip View new-clip inheritance wording; matched target resolution remains unknown.

Evidence: `SET-B041`; [exact routes](#analysis-only-evidence).

### REQ-SETTINGS-LEARNING-017 — Audio device and system-output settings

**D12/target-U.** Audio settings expose input/output devices, sample rate/latency and calibration testing. The source describes macOS CoreAudio and Windows driver selection/driver-owned management, recommending ASIO without prohibiting other drivers. macOS Use System Device follows the OS Sound output choice. Accepted devices/drivers/rates, fallback and transition artifacts remain unknown.

Evidence: `SET-B043`, `SET-B044`, `SET-B045`; [exact routes](#analysis-only-evidence).

### REQ-SETTINGS-LEARNING-018 — Library settings and Places labels

**D12/target-U.** Library settings choose default Pack/User Library locations and dependent-file copying when moving clips/tracks/presets to Browser. They also show/hide Cloud, Push and Splice Places labels. General file-copy/project and Browser operations remain with existing owners. Visible labels do not establish service availability, credentials, cloud protocol or target feature presence.

Evidence: `SET-B064`; [exact routes](#analysis-only-evidence).

### REQ-SETTINGS-LEARNING-019 — Licenses and Updates settings category

**D12/target-U.** The chapter identifies Licenses and Updates settings for authorization, automatic updates and usage data. It supplies no detailed command surface, default consent, telemetry payload, update protocol, rollback or entitlement rules; those remain required unknowns.

Evidence: `SET-B070`; [exact routes](#analysis-only-evidence).

### REQ-SETTINGS-LEARNING-U-DELIVERY — Installation, authorization and update operations

**U/target-U.** Installation/authentication/license entitlement, online/offline authorization, usage-data consent and telemetry, update/download/install/rollback, OS permissions and recovery remain required unknowns. SET-B003 is a source pointer and publisher licensing prose, not a new independently interpreted license contract.

### REQ-SETTINGS-LEARNING-U-LIFECYCLE — Settings, help and media lifecycle

**U/target-U.** Malformed/boundary input, unavailable content/device, cancel/undo/persistence/restart, focus/mapping conflicts, monitor/rate changes and teardown remain unknown.

## Source-context question

**SET-U-CLIP-COLOR:** SET-B041 permits new-clip random color or track color;
REQ-CLIP-VIEW-005 describes track-color inheritance without that preference.
Retain both exact source contexts. Do not infer a contradiction, silently change
the sealed Clip View owner, or use a random-result inequality as an oracle.
Matched version/preference evidence and a separately reviewed successor are needed.

## Finite acceptance proposals

[30 cases](../../analysis/ableton-live-12.4.3/full-spec-v1/settings-learning/cases.json)
cover19documentary source roles and11operational U probes for21requirements
(19D12/2U). The lesson timing case has null documentary output/comparator;
all30target expected/comparison fields are null/U/unexecuted. No future fixture
is supplied content or a result. Installation/authorization/update operations
remain U; licensing prose is not independently interpreted as a legal contract.

## Analysis-only evidence

Official [Version12 First Steps](https://www.ableton.com/en/live-manual/12/first-steps/), captureUTC
2026-10-19T21:59:13.502275+00:00, 261023bytes, SHA-256 `59601f2af92f1148b23213edc0471339c9ac1188a401f717e3067d67b55e2746`;
[retained HTML](../../analysis/ableton-live-12.4.3/full-spec-v1/settings-learning/manual-first-steps-2026-10-19.html).
[70 blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/settings-learning/source-blocks.json)
retain chapter anchors/HTML lines; figures uninspected, current-site revision
and exact12.4.3 applicability unknown. The existing analyst parser is pinned
in dependencies.json. [Requirements](../../analysis/ableton-live-12.4.3/full-spec-v1/settings-learning/requirements.json)
and [author seal](../../analysis/ableton-live-12.4.3/full-spec-v1/settings-learning/manifest-author-r1.json)
freeze this partial analyst draft, not implementation inputs or a release expansion.
