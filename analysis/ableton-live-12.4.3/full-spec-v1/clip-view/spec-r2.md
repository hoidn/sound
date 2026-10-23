---
id: SPEC-CLIP-VIEW-WORKFLOWS
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 2
target: Ableton Live 12 Suite 12.4.3; documentary Version12 applicability U
---

# Shared Clip View workflows and audio clip properties

## Scope and authority

This partial successor reconciles all24 groups from the independently reviewed
retained-source audit. It adds bounded local input/control gestures and explicit
prerequisites; no source topic or target feature is complete. Audit approval is
not approval of this owner successor, runtime behavior or an implementation
handoff. Separate independent owner review remains pending as of author freeze.

Shared panels, editor selection, local region/sample UI and audio command entries
remain here. [Session](session-view-workflows.md) owns statuses/launch selection;
[launch](session-launch-workflows.md), [finite launch](clip-launch.md) and
[playback](playback-core.md) retain scheduling/engine laws. [Warp workflows](warping-workflows.md)
and [native markers](warp-markers.md) own their respective interactive and finite
subsets. [MIDI editing](midi-editing-tools.md), [MPE](mpe-workflows.md),
[grooves](groove-workflows.md), [automation](automation-workflows.md),
[media defaults](media-file-workflows.md), [project/media](project-media-workflows.md),
[Arrangement](arrangement-editing.md), [settings](settings-learning-workflows.md),
[Browser](browser-content-workflows.md), [mixing](mixing-workflows.md),
[remote mapping](remote-control-workflows.md) and [keyboard](keyboard-navigation.md)
retain underlying effects. In particular Group Assign uses existing Mixing012/
MXW012; no duplicate group-color case or new color law is added here.

D12 means retained current Version12 documentation, not exact12.4.3 evidence.
Every actual `expected`/`comparison` is null, target U and unexecuted. Original
source/cache/quality/CPU/default prose never mandates private architecture or
proves timing, numeric, signal, file, process, protocol or random outcomes. New
sensitive cases also keep documentary outcomes null; `source_claim` is prose
only. Legacy documentary fields retain only their stated bounded source roles.
No application, original function, candidate, reader, hardware, editor, media,
network/account or configuration operation was executed. Images/destinations
remain uninspected. [Research](../research/clip-view-workflows.md) gives provenance.

## Preconditions and unresolved contexts

The [future owned-input fixture](../../analysis/ableton-live-12.4.3/full-spec-v1/clip-view/fixtures-r2.json)
requires independently validated A/B/C media or editable MIDI M, matched focus,
platform, source/region/loop/Warp/grid/meter, quantization/UpdateRate and output
state. Every unavailable/negative trial begins from a genuinely productive
matched input/control/output baseline. Missing input/capability is U, not a pass.
No media fixture/reference render was fabricated.

Follow needs genuine automatic scrolling across the visible boundary before a
real edit and a separately established pause. Options/toggle, stop alone/restart,
Arrangement scrub and clip scrub use separate reset histories. Stop alone is
resumption/eligibility context; it does not require moving scrolling while stopped.

[Q-031](../questions.md#q-031-new-clip-color-preference-context) retains color preference/version/history uncertainty.
[Q-053](../questions.md#q-053-midi-utility-gesture-and-humanize-source-contexts) retains Humanize context uncertainty.
The exact detailed MIDI Intervals paragraph distinguishes selected-slider
addition from no-selection slider-setting/button application; existing MIDI011
owns it, with actual future actions routed to that owner. This is source context,
not a new Clip View note law or full Q053 resolution. Half-grid versus quarter-
before/after Humanize is not adopted as equivalence or RNG/displacement policy.

## Requirements

Each bare first-cell ID is current and browser-discoverable. Source/context
blocks resolve to [exact quotes and HTML locators](../../analysis/ableton-live-12.4.3/full-spec-v1/clip-view/source-context-r2.json).
Numeric representations do not establish stored-time/PCM/note or control laws.

| Requirement | Documentary contract and limits | Basis | Source blocks |
| --- | --- | --- | --- |
| REQ-CLIP-VIEW-001 | Clip double-click in Session/Arrangement, Selector, Toggle or Ctrl+Alt+3 Win/Cmd+Option+3 Mac opens Clip View. Toggle while Device View is open stacks Clip View above it. Dragging top border resizes; bottom closes it. In Session, a Track Status Display click opens the Clip View for that track’s currently playing clip; require independently established playing status, not a stopped/empty/group/monitored interpretation. Session owns the status presentation. | D12; target U | CV:B003, CV:B004, CV:B005, CV:B006, CV:B009 |
| REQ-CLIP-VIEW-002 | Clip View opens in focused window and displays current clip even when selected in other window. F12 moves view between windows; Shift+Tab does so only when Use Tab Key to Navigate is off. | D12; target U | CV:B007, CV:B008 |
| REQ-CLIP-VIEW-003 | Clip Activator off deactivates clip playback in Session launch or Arrangement timeline; context Deactivate/0 also available. Multi-selection off deactivates all selected clips. | D12; target U | CV:B013, CV:B015, CV:B016 |
| REQ-CLIP-VIEW-004 | Clip Rename and Edit Info Text are available through specified title/Edit/clip menus. Audio clip rename does not rename source sample. Multi-selection shows count; common new name is not displayed as title. The source reference-name default is retained only for independently admitted creation/reference history; saved defaults, imports, filename grammar and target initial state remain U. | D12; target U | CV:B018, CV:B019, CV:B020, CV:B021 |
| REQ-CLIP-VIEW-005 | The source describes new clips using track color, but Q031 keeps matched Clip Color preference/version/creation history unresolved; no unconditional inheritance or random-color law is chosen. Title and clip-context palettes change clip color. Track Assign Color commands affect clips only in the invoking Session or Arrangement view. Group Assign behavior and its existing active-view/member/nonmember case remain REQ-MIXING-WORKFLOW-012/MXW-012, not a new Clip View law or duplicated test. Multi-selection title is striped while individual selected clips accept color. | D12; target U | CV:B023, CV:B024, CV:B025, CV:B026 |
| REQ-CLIP-VIEW-006 | Title plus panels/editor are shared layout. Main/Extended properties are common; audio adds Audio Utilities/Transform, MIDI adds Pitch-Time/Transform/Generate. Editors and additional properties depend on clip type. | D12; target U | CV:B011, CV:B034, CV:B035 |
| REQ-CLIP-VIEW-007 | Panels support horizontal, vertical or automatic arrangement through border drag/View menu/title context. Arrangement is remembered on future opening. Title double-click/Fold minimizes panels. | D12; target U | CV:B036, CV:B037, CV:B038 |
| REQ-CLIP-VIEW-008 | Audio editor modes are Sample/Envelope; MIDI modes Notes/Envelope/MPE. Tabs/View commands or Alt+Tab Win/Option+Tab Mac switch modes. | D12; target U | CV:B040, CV:B041, CV:B042, CV:B043, CV:B044, CV:B045 |
| REQ-CLIP-VIEW-009 | Start/End value fields define unlooped playing region. Warped audio displays bars-beats-sixteenths; unwarped displays minutes-seconds-milliseconds. | D12; target U | CV:B049, CV:B050, CV:B051 |
| REQ-CLIP-VIEW-010 | Set Start/End during playback take current playhead position according to global quantization; exact rounding/ties/dispatch are unspecified here. | D12; target U | CV:B050 |
| REQ-CLIP-VIEW-011 | Loop Position/Length and Loop toggle define repeat region; initial Loop Length is described as total clip length. Audio loop is unavailable until Warp on; unwarped audio cannot loop. | D12; target U | CV:B052, CV:B053, CV:B150, CV:B151 |
| REQ-CLIP-VIEW-012 | Set Loop Position moves start to current playhead rounded by global quantization and enables loop; Set Loop Length then moves end to current position. With loop off, Set Length ends loop at current position preserving preset length and enables it. | D12; target U | CV:B054, CV:B055, CV:B056 |
| REQ-CLIP-VIEW-013 | Set buttons, Loop toggle, loop region and Start/End positions are eligible MIDI mapping targets; actual controller mapping/takeover belongs to MIDI user mapping. | D12; target U | CV:B057 |
| REQ-CLIP-VIEW-014 | Clip time signature is per-clip display state, independent from project meter and does not change clip playback. | D12; target U | CV:B059, CV:B060 |
| REQ-CLIP-VIEW-015 | Scale button/root/name are clip properties. Audio scale forwards to scale-aware devices rather than altering raw clip playback; MIDI piano highlighting and scale edits belong to MIDI owner. | D12; target U | CV:B066, CV:B067, CV:B068 |
| REQ-CLIP-VIEW-016 | Extended panel shows launch controls for Session clips only. Arrangement audio has no Extended panel; Arrangement MIDI has MIDI bank/program only. Full launch and Follow Actions remain with clip-launch and future Session packet. | D12; target U | CV:B070, CV:B071, CV:B074, CV:B075 |
| REQ-CLIP-VIEW-017 | MIDI bank/sub-bank/program selectors support documented 128 choices each and send on clip launch to supporting targets. Dash leaves corresponding message unset. MIDI bytes, value numbering and target support remain U. | D12; target U | CV:B077, CV:B078, CV:B079 |
| REQ-CLIP-VIEW-018 | Warp off plays sample at original tempo irrespective of Set tempo; Warp on follows Set tempo when metrical structure is valid. Preparation/analysis and Warp algorithms remain with their owners. | D12; target U | CV:B081, CV:B084, CV:B085 |
| REQ-CLIP-VIEW-019 | Reverse creates a new reversed sample and repoints clip, applying clip settings under documented transformation rules. Before save it resides in Temporary Folder; after Set save under Project Samples/Processed/Reverse. | D12; target U | CV:B087, CV:B088 |
| REQ-CLIP-VIEW-020 | On reverse, Warp Markers and region/loop positions are reflected with sample material; clip envelopes keep timeline positions. Exact endpoint/frame/marker transformation is not specified. | D12; target U | CV:B089 |
| REQ-CLIP-VIEW-021 | When a long reversal exposes progress, the source names Status Bar progress and temporary action lock while already playing clips continue. Newly observed waveform generation is the documented eligibility context for reversed-clip playback and other actions. Revert/reverse and close/reopen histories remain separate; source speed/cache prose is not a deadline, universal glitch-free promise or internal cache architecture requirement. | D12; target U | CV:B090, CV:B092 |
| REQ-CLIP-VIEW-022 | Session cannot reverse multiple clips together. Arrangement time-range Reverse Clip(s)/R is owned by Arrangement editing, whose MIDI-containing selection limitation remains applicable. | D12; target U | CV:B091 |
| REQ-CLIP-VIEW-023 | Edit opens configured external sample editor; Live playback must stop before external processing. Return uses edited version; Warp Markers retained only when sample length unchanged. Shared source edits can affect other referencing clips. | D12; target U | CV:B094, CV:B095, CV:B096 |
| REQ-CLIP-VIEW-024 | Clip Fade toggle is Session-only; Arrangement uses fade envelopes. Manual describes signal-dependent 0-4 ms edge fades and new-clip default on when Create Fades on Clip Edges enabled. Exact fade kernel remains with playback/Arrangement owners. | D12; target U | CV:B098, CV:B099, CV:B100 |
| REQ-CLIP-VIEW-025 | RAM toggle requests referenced audio in memory rather than realtime disk reads; capacity/resource/disk-overload observations in prose are not a memory guarantee or benchmark. | D12; target U | CV:B102, CV:B106 |
| REQ-CLIP-VIEW-026 | Hi-Q toggles higher-quality rate conversion with described CPU tradeoff. Approximate 19-semitone audibility prose supplies no spectral/CPU metric or universal threshold. | D12; target U | CV:B108, CV:B109 |
| REQ-CLIP-VIEW-027 | Audio Gain uses dB; Pitch semitone knob/field and separate cents field are distinct, with 100 cents per semitone. Multi-selected differing gains display split triangle handles. | D12; target U | CV:B112, CV:B113, CV:B114 |
| REQ-CLIP-VIEW-028 | Audio Transform panel offers Quantize for warped clips using current grid or specified meter and Amount; audio has no Generate panel. Marker movement/selection/rounding stays with Warp owner/future Warp workflow packet. | D12; target U | CV:B130, CV:B131, CV:B132, CV:B133 |
| REQ-CLIP-VIEW-029 | Editor time-ruler vertical drag zooms and horizontal drag scrolls; wheel/trackpad scrolls. Behavior is shared by Sample and MIDI editors. | D12; target U | CV:B138, CV:B139 |
| REQ-CLIP-VIEW-030 | Z/Zoom to Clip Selection zooms current time selection; X returns one zoom state per press, including repeated Z history. | D12; target U | CV:B140 |
| REQ-CLIP-VIEW-031 | Selector overview spans clip Start-End; its outline represents the visible editor portion. Within-outline horizontal/vertical drags provide scrolling/zooming roles. Follow is offered by its toggle and Options command. With a genuinely established automatically scrolling playhead baseline, an actual Sample/MIDI editor edit pauses Follow. The source names stop, restart, Arrangement scrub and clip scrub as resumption contexts; this does not promise moving scrolling while stopped, a deadline or universal focus/interception behavior. MIDI-specific editing remains with its owner. | D12; target U | CV:B141, CV:B142 |
| REQ-CLIP-VIEW-032 | Start/End markers drag or move with left/right arrows; Alt Win/Option Mac plus arrows on either selected marker moves whole region. | D12; target U | CV:B145 |
| REQ-CLIP-VIEW-033 | Permanent Scrub Areas on permits click in lower waveform or scrub area to jump playback; off permits Shift-click in scrub area or beat-time ruler. | D12; target U | CV:B146, CV:B148 |
| REQ-CLIP-VIEW-034 | Scrub jumps use global quantization; holding left button repeats a portion the size of selected quantization, with small/None allowing scrubbing. Chase MIDI Notes routes to playback-core note/chase gaps; no repeated-note oracle is supplied here. | D12; target U | CV:B147 |
| REQ-CLIP-VIEW-035 | Loop brace handles edit start/end; brace drag moves it. Left/right nudges grid, up/down shifts by length; Ctrl Win/Cmd Mac left/right resizes by grid, up/down doubles/halves length. | D12; target U | CV:B152, CV:B153, CV:B154, CV:B155, CV:B156, CV:B157 |
| REQ-CLIP-VIEW-036 | Clip begins at start marker regardless of loop brace, allowing initial material to run into a later loop. | D12; target U | CV:B159 |
| REQ-CLIP-VIEW-037 | Sample header displays name/rate/depth/channel count. Multi-selection shows sample count and asterisk for differing properties. Name click/Show in Browser reveals source. | D12; target U | CV:B161, CV:B162, CV:B163 |
| REQ-CLIP-VIEW-038 | Unlooped Crop Clip Sample uses Start-End; looped cropping begins at earlier Start/Loop Start and ends at Loop End. | D12; target U | CV:B165, CV:B166 |
| REQ-CLIP-VIEW-039 | Time selection exposes Crop Clip Sample to Time Selection; Ctrl+Shift+J Win/Cmd+Shift+J Mac triggers applicable crop command. | D12; target U | CV:B167, CV:B169 |
| REQ-CLIP-VIEW-040 | Audio crop creates a new shorter sample, temporarily in configured Temporary Folder and after save in Project Samples/Processed/Crop. | D12; target U | CV:B168 |
| REQ-CLIP-VIEW-041 | Browser drag to Clip View or selected browser sample double-click/Enter replaces referenced sample. Pitch/volume settings remain; Warp Markers retained only for exact same source length. | D12; target U | CV:B172, CV:B173 |
| REQ-CLIP-VIEW-042 | Show Similar Files opens similarity search; Manage Sample File opens Set File Manager with current source selected. File Manager replacements/destructive edits can affect all clips/instruments sharing source. | D12; target U | CV:B174, CV:B175 |
| REQ-CLIP-VIEW-043 | Drag from empty clip slot or Ctrl Win/Cmd Mac/Shift extends clip multi-selection. Visible properties generally include only common properties of selected contents. | D12; target U | CV:B177 |
| REQ-CLIP-VIEW-044 | Mixed-value multi-selection shows a value range. Dragging control to absolute maximum/minimum makes selected settings identical and subsequently adjustable as one. | D12; target U | CV:B178 |
| REQ-CLIP-VIEW-045 | Clip Update Rate in Record/Warp/Launch settings quantizes changes to a running clip. Launch Mode/Warp Mode can be defaults for new clips. Complete affected-control set, rate choices and precedence versus global launch quantization are U. Global new-clip Launch Mode/Warp Mode defaults are distinct from sample-specific Save Default Clip and require admitted type/view/history: no MIDI audio-Warp or Arrangement Session-launch constructor is inferred. | D12; target U | CV:B180 |
| REQ-CLIP-VIEW-046 | Save Default Clip button is audio-specific and supports multi-selected samples; its ASD/new-import/nonretroactive semantics are owned by REQ-MEDIA-FILE-010, distinct from Live Clip devices. | D12; target U | CV:B028, CV:B029, CV:B030, CV:B031 |
| REQ-CLIP-VIEW-U-REGION | Required region/loop input bounds and error outcomes remain unknown. | U; target U | No supported outcome |
| REQ-CLIP-VIEW-U-TIMING | Required ordering between edits, scrub, launch and transport remains unknown. | U; target U | No supported outcome |
| REQ-CLIP-VIEW-U-UNDO | Required edit/processed-file undo/redo transactions remain unknown. | U; target U | No supported outcome |
| REQ-CLIP-VIEW-U-PERSIST | Required save/reopen/default/processed-file state remains unknown. | U; target U | No supported outcome |
| REQ-CLIP-VIEW-U-CANCEL | Required cancellation/progress/error outcomes remain unknown. | U; target U | No supported outcome |
| REQ-CLIP-VIEW-U-TEARDOWN | Required clip/view/Set teardown and concurrent-selection outcomes remain unknown. | U; target U | No supported outcome |
| REQ-CLIP-VIEW-U-AUDIO | Required numerical audio and media-boundary oracles remain unknown. | U; target U | No supported outcome |
| REQ-CLIP-VIEW-U-MULTI | Required multi-selection/common-value/context outcomes remain unknown. | U; target U | No supported outcome |
| REQ-CLIP-VIEW-047 | In an independently admitted audio-loop context, Edit offers Duplicate Loop as a command entry. The chapter describes loop-length/content duplication generally; no audio content-copy, generated length/identity, timing, waveform or file-operation oracle is supplied here. Existing REQ-MIDI-EDIT-019/MED-019 owns its explicit MIDI duplicate/outside-note relationship. | D12; target U | CV:B158 |

## Finite future actions

The [92-case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/clip-view/cases-r2.json)
preserves all62 existing IDs and their true bounded subsets. It strengthens
CV031's Follow baseline and scopes CV005/CV031 documentary descriptions;30
cases add actual local gestures. CV027's known Gain values are not every slider
gesture; CV045 already genuinely changes Gain. Existing opening/window/editor,
repeated zoom, scrub preference, all crop branches/replacement routes and both
mixed-value extrema remain represented subsets, not missing or complete topics.

| Case | Requirements | Kind | Target |
| --- | --- | --- | --- |
| CV-001 | REQ-CLIP-VIEW-001 | positive | U; not executed |
| CV-002 | REQ-CLIP-VIEW-002 | selection | U; not executed |
| CV-003 | REQ-CLIP-VIEW-003 | signal-obligation | U; not executed |
| CV-004 | REQ-CLIP-VIEW-004 | positive | U; not executed |
| CV-005 | REQ-CLIP-VIEW-005 | selection | U; not executed |
| CV-006 | REQ-CLIP-VIEW-006 | positive | U; not executed |
| CV-007 | REQ-CLIP-VIEW-007 | positive | U; not executed |
| CV-008 | REQ-CLIP-VIEW-008 | positive | U; not executed |
| CV-009 | REQ-CLIP-VIEW-009 | positive | U; not executed |
| CV-010 | REQ-CLIP-VIEW-010 | timing-obligation | U; not executed |
| CV-011 | REQ-CLIP-VIEW-011 | negative | U; not executed |
| CV-012 | REQ-CLIP-VIEW-012 | timing-obligation | U; not executed |
| CV-013 | REQ-CLIP-VIEW-013 | positive | U; not executed |
| CV-014 | REQ-CLIP-VIEW-014 | signal-obligation | U; not executed |
| CV-015 | REQ-CLIP-VIEW-015 | positive | U; not executed |
| CV-016 | REQ-CLIP-VIEW-016 | negative | U; not executed |
| CV-017 | REQ-CLIP-VIEW-017 | positive | U; not executed |
| CV-018 | REQ-CLIP-VIEW-018 | signal-obligation | U; not executed |
| CV-019 | REQ-CLIP-VIEW-019 | positive | U; not executed |
| CV-020 | REQ-CLIP-VIEW-020 | signal-obligation | U; not executed |
| CV-021 | REQ-CLIP-VIEW-021 | timing-obligation | U; not executed |
| CV-022 | REQ-CLIP-VIEW-022 | negative | U; not executed |
| CV-023 | REQ-CLIP-VIEW-023 | positive | U; not executed |
| CV-024 | REQ-CLIP-VIEW-024 | negative | U; not executed |
| CV-025 | REQ-CLIP-VIEW-025 | positive | U; not executed |
| CV-026 | REQ-CLIP-VIEW-026 | positive | U; not executed |
| CV-027 | REQ-CLIP-VIEW-027 | positive | U; not executed |
| CV-028 | REQ-CLIP-VIEW-028 | negative | U; not executed |
| CV-029 | REQ-CLIP-VIEW-029 | positive | U; not executed |
| CV-030 | REQ-CLIP-VIEW-030 | positive | U; not executed |
| CV-031 | REQ-CLIP-VIEW-031 | selection | U; not executed |
| CV-032 | REQ-CLIP-VIEW-032 | positive | U; not executed |
| CV-033 | REQ-CLIP-VIEW-033 | positive | U; not executed |
| CV-034 | REQ-CLIP-VIEW-034 | timing-obligation | U; not executed |
| CV-035 | REQ-CLIP-VIEW-035 | positive | U; not executed |
| CV-036 | REQ-CLIP-VIEW-036 | signal-obligation | U; not executed |
| CV-037 | REQ-CLIP-VIEW-037 | positive | U; not executed |
| CV-038 | REQ-CLIP-VIEW-038 | positive | U; not executed |
| CV-039 | REQ-CLIP-VIEW-039 | positive | U; not executed |
| CV-040 | REQ-CLIP-VIEW-040 | positive | U; not executed |
| CV-041 | REQ-CLIP-VIEW-041 | positive | U; not executed |
| CV-042 | REQ-CLIP-VIEW-042 | positive | U; not executed |
| CV-043 | REQ-CLIP-VIEW-043 | selection | U; not executed |
| CV-044 | REQ-CLIP-VIEW-044 | boundary | U; not executed |
| CV-045 | REQ-CLIP-VIEW-045 | timing-obligation | U; not executed |
| CV-046 | REQ-CLIP-VIEW-046 | positive | U; not executed |
| CV-U-BOUNDARY | REQ-CLIP-VIEW-U-REGION | boundary | U; not executed |
| CV-U-MALFORMED | REQ-CLIP-VIEW-U-REGION | malformed | U; not executed |
| CV-U-TIMING | REQ-CLIP-VIEW-U-TIMING | timing | U; not executed |
| CV-U-TRANSPORT | REQ-CLIP-VIEW-U-TIMING | transport | U; not executed |
| CV-U-UNDO | REQ-CLIP-VIEW-U-UNDO | undo-redo | U; not executed |
| CV-U-AUTOMATION | REQ-CLIP-VIEW-U-UNDO | automation | U; not executed |
| CV-U-PERSISTENCE | REQ-CLIP-VIEW-U-PERSIST | persistence | U; not executed |
| CV-U-SOURCE-LOSS | REQ-CLIP-VIEW-U-PERSIST | source-loss | U; not executed |
| CV-U-CANCEL | REQ-CLIP-VIEW-U-CANCEL | cancellation | U; not executed |
| CV-U-ERROR | REQ-CLIP-VIEW-U-CANCEL | error | U; not executed |
| CV-U-TEARDOWN | REQ-CLIP-VIEW-U-TEARDOWN | teardown | U; not executed |
| CV-U-SELECTION-RACE | REQ-CLIP-VIEW-U-TEARDOWN | selection | U; not executed |
| CV-U-AUDIO | REQ-CLIP-VIEW-U-AUDIO | signal-obligation | U; not executed |
| CV-U-RATE | REQ-CLIP-VIEW-U-AUDIO | sample-rate | U; not executed |
| CV-U-MULTI | REQ-CLIP-VIEW-U-MULTI | boundary | U; not executed |
| CV-U-PROGRAM | REQ-CLIP-VIEW-U-MULTI | midi-output | U; not executed |
| CV-047 | REQ-CLIP-VIEW-001 | control | U; not executed |
| CV-048 | REQ-CLIP-VIEW-004 | history | U; not executed |
| CV-049 | REQ-CLIP-VIEW-004 | control | U; not executed |
| CV-050 | REQ-CLIP-VIEW-005 | control | U; not executed |
| CV-051 | REQ-CLIP-VIEW-046 | file-obligation | U; not executed |
| CV-052 | REQ-CLIP-VIEW-007 | control | U; not executed |
| CV-053 | REQ-CLIP-VIEW-007 | control | U; not executed |
| CV-054 | REQ-CLIP-VIEW-011 | history | U; not executed |
| CV-055 | REQ-CLIP-VIEW-014 | timing-obligation | U; not executed |
| CV-056 | REQ-CLIP-VIEW-017 | numeric | U; not executed |
| CV-057 | REQ-CLIP-VIEW-017 | midi-output | U; not executed |
| CV-058 | REQ-CLIP-VIEW-021 | timing-obligation | U; not executed |
| CV-059 | REQ-CLIP-VIEW-023 | file-obligation | U; not executed |
| CV-060 | REQ-CLIP-VIEW-027 | numeric | U; not executed |
| CV-061 | REQ-CLIP-VIEW-027 | numeric | U; not executed |
| CV-062 | REQ-CLIP-VIEW-029, REQ-CLIP-VIEW-030 | control | U; not executed |
| CV-063 | REQ-CLIP-VIEW-031 | control | U; not executed |
| CV-064 | REQ-CLIP-VIEW-031 | timing-obligation | U; not executed |
| CV-065 | REQ-CLIP-VIEW-031 | timing-obligation | U; not executed |
| CV-066 | REQ-CLIP-VIEW-031 | timing-obligation | U; not executed |
| CV-067 | REQ-CLIP-VIEW-031 | timing-obligation | U; not executed |
| CV-068 | REQ-CLIP-VIEW-032 | numeric | U; not executed |
| CV-069 | REQ-CLIP-VIEW-034 | numeric | U; not executed |
| CV-070 | REQ-CLIP-VIEW-035 | numeric | U; not executed |
| CV-071 | REQ-CLIP-VIEW-035 | numeric | U; not executed |
| CV-072 | REQ-CLIP-VIEW-047 | signal-obligation | U; not executed |
| CV-073 | REQ-CLIP-VIEW-038, REQ-CLIP-VIEW-039 | file-obligation | U; not executed |
| CV-074 | REQ-CLIP-VIEW-044 | numeric | U; not executed |
| CV-075 | REQ-CLIP-VIEW-045 | configuration | U; not executed |
| CV-076 | REQ-CLIP-VIEW-005 | history | U; not executed |

## Preservation, routes and gaps

[Exact deltas](../../analysis/ableton-live-12.4.3/full-spec-v1/clip-view/delta-r2.json)
retain54 requirements/62 cases, add one audio Duplicate Loop entry clause and30
cases, and record six contract refinements, one action refinement and two bounded
documentary descriptions. All17 R1 files remain exact in place, including its
seal/freeze/checker/reports/snapshots. Exact pre-edit canonical pages are retained;
old pending-review prose remains historical as-of its author freeze.

The [24-group reconciliation](../../analysis/ableton-live-12.4.3/full-spec-v1/clip-view/reconciliation-r2.json)
separates local adoption, existing predicates and external-owner extensions.
[Routed proposals](../../analysis/ableton-live-12.4.3/full-spec-v1/clip-view/routed-proposals-r2.json)
are not new normative IDs/cases, and do not close Groove/Media/MIDI/shared-reference
gaps. Historical consumer identities are enumerated without automatic adapter or
replay obligations; concrete dependency/check/release gates still require narrow
replay. Full defaults/history/build/platform/reader, malformed/undo/persistence,
source-loss/cancel/teardown, numeric/timing/file/audio/API/protocol outcomes remain U.
