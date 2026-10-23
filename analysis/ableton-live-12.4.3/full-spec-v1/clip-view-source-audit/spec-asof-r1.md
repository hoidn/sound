---
id: SPEC-CLIP-VIEW-WORKFLOWS
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3; documentary Version 12 with exact-build applicability unknown
---

# Shared Clip View workflows and audio clip properties

## Scope and authority

This partial F-04 draft owns shared Clip View selection/panel/region/scrub UI,
multiclip property editing and unowned audio-property/sample actions. It is
neither complete Clip View coverage nor a released implementation input.
[Coverage design](../research/full-live-specification-design.md) and
[research owner](../research/clip-view-workflows.md) govern evidence/limits.
**D12** means the retained official Version 12 chapter; **every exact-12.4.3
runtime outcome remains U**. No original program, media operation, MIDI hardware,
external editor or candidate was executed. Figures were not separately inspected.

### Canonical boundaries

- [Session workflows](session-view-workflows.md) owns grid/scenes, Track Status
  Display, transfers and selection-on-launch; this page owns Clip View rendering
  of the resulting selected clip.
- [Clip launch](clip-launch.md) owns launch/follow fields and its finite grid
  arithmetic; [playback core](playback-core.md) owns its finite engine timing,
  unwarped playback and fade contracts. These do not define Set buttons, scrub
  dispatch, Clip Update Rate or arbitrary Follow Action scheduling.
- [Warp markers](warp-markers.md) owns serialization, scripting marker edits and
  its finite time conversion; full Warp algorithms and interactive marker/audio
  quantization remain a future packet. Here Warp supplies UI preconditions only.
- [MIDI editing/tools](midi-editing-tools.md) owns note edits, multi-note focus,
  utilities, MIDI crop and Duplicate Loop; [MPE](mpe-workflows.md) owns expression;
  [groove](groove-workflows.md), [tuning](tuning-systems.md),
  [conversion](audio-to-midi.md) and [automation](automation-envelopes.md) own
  their respective computation. Panel availability does not expand their scope.
- [Media files](media-file-workflows.md) owns analysis/default clips and Live Clip
  distinction; [project/media](project-media-workflows.md) owns shared reference
  repair/collection. This page owns UI entry points and audio Crop/Reverse/Edit
  predicates, not ASD/ALC/media codecs or a filesystem transaction guarantee.
- [Arrangement editing](arrangement-editing.md) owns Arrangement Reverse Clip(s),
  selection and fade envelopes. [Keyboard/navigation](keyboard-navigation.md)
  retains global focus/accessibility; chapter-specific shortcuts below require
  their explicit focus/settings preconditions.

## Preconditions and observable state

[Finite input recipe](../../analysis/ableton-live-12.4.3/full-spec-v1/clip-view/fixtures.json) requires future independently
validated owned A/B/C audio and editable MIDI M, reset copies and retained source
identity, region, Warp/loop/mode, tempo/meter, global quantization, Clip Update
Rate, focus/settings and output state. Media files and rendered reference outputs
are not provided. Missing inputs yield U, never a pass. Audible comparisons need
valid sources and active/unmuted/nonzero output plus a paired positive baseline.

Start/End, Loop Position/Length, source media duration, editor time selection,
clip meter, project meter, global launch quantization, Clip Update Rate, Warp
mapping and clip envelope time are distinct. Bars-beats-sixteenths versus
minutes-seconds-milliseconds are visible representations, not new stored-time
conversion laws. No frame rounding, PCM identity, gain/pitch/FM/filter/RNG law,
MIDI encoding, CPU benchmark or numerical tolerance is invented.

## Requirements

Each row is D12/target-U with an exact retained paragraph locator. The same-number
`CV-NNN` case contains finite setup/actions and either a visible-state proposal
or an ungraded timing/signal obligation. The eight U requirements are separate
required gaps, not inapplicable cases.

| Requirement | Documented contract and limits | Source blocks |
| --- | --- | --- |
| REQ-CLIP-VIEW-001 | Clip double-click in Session/Arrangement, Selector, Toggle or Ctrl+Alt+3 Win/Cmd+Option+3 Mac opens Clip View. Toggle while Device View is open stacks Clip View above it. Dragging top border resizes; bottom closes it. | `CV:B003`, `CV:B004`, `CV:B005`, `CV:B006` |
| REQ-CLIP-VIEW-002 | Clip View opens in focused window and displays current clip even when selected in other window. F12 moves view between windows; Shift+Tab does so only when Use Tab Key to Navigate is off. | `CV:B007`, `CV:B008` |
| REQ-CLIP-VIEW-003 | Clip Activator off deactivates clip playback in Session launch or Arrangement timeline; context Deactivate/0 also available. Multi-selection off deactivates all selected clips. | `CV:B013`, `CV:B015`, `CV:B016` |
| REQ-CLIP-VIEW-004 | Clip Rename and Edit Info Text are available through specified title/Edit/clip menus. Audio clip rename does not rename source sample. Multi-selection shows count; common new name is not displayed as title. | `CV:B018`, `CV:B019`, `CV:B020`, `CV:B021` |
| REQ-CLIP-VIEW-005 | New clips inherit track color; palette changes clip color. Track/group Assign Color commands affect clips only in the invoking Session or Arrangement view. Multi-selection title is striped while individual selected clips accept color. | `CV:B023`, `CV:B024`, `CV:B025`, `CV:B026` |
| REQ-CLIP-VIEW-006 | Title plus panels/editor are shared layout. Main/Extended properties are common; audio adds Audio Utilities/Transform, MIDI adds Pitch-Time/Transform/Generate. Editors and additional properties depend on clip type. | `CV:B011`, `CV:B034`, `CV:B035` |
| REQ-CLIP-VIEW-007 | Panels support horizontal, vertical or automatic arrangement through border drag/View menu/title context. Arrangement is remembered on future opening. Title double-click/Fold minimizes panels. | `CV:B036`, `CV:B037`, `CV:B038` |
| REQ-CLIP-VIEW-008 | Audio editor modes are Sample/Envelope; MIDI modes Notes/Envelope/MPE. Tabs/View commands or Alt+Tab Win/Option+Tab Mac switch modes. | `CV:B040`, `CV:B041`, `CV:B042`, `CV:B043`, `CV:B044`, `CV:B045` |
| REQ-CLIP-VIEW-009 | Start/End value fields define unlooped playing region. Warped audio displays bars-beats-sixteenths; unwarped displays minutes-seconds-milliseconds. | `CV:B049`, `CV:B050`, `CV:B051` |
| REQ-CLIP-VIEW-010 | Set Start/End during playback take current playhead position according to global quantization; exact rounding/ties/dispatch are unspecified here. | `CV:B050` |
| REQ-CLIP-VIEW-011 | Loop Position/Length and Loop toggle define repeat region; initial Loop Length is described as total clip length. Audio loop is unavailable until Warp on; unwarped audio cannot loop. | `CV:B052`, `CV:B053`, `CV:B150`, `CV:B151` |
| REQ-CLIP-VIEW-012 | Set Loop Position moves start to current playhead rounded by global quantization and enables loop; Set Loop Length then moves end to current position. With loop off, Set Length ends loop at current position preserving preset length and enables it. | `CV:B054`, `CV:B055`, `CV:B056` |
| REQ-CLIP-VIEW-013 | Set buttons, Loop toggle, loop region and Start/End positions are eligible MIDI mapping targets; actual controller mapping/takeover belongs to MIDI user mapping. | `CV:B057` |
| REQ-CLIP-VIEW-014 | Clip time signature is per-clip display state, independent from project meter and does not change clip playback. | `CV:B059`, `CV:B060` |
| REQ-CLIP-VIEW-015 | Scale button/root/name are clip properties. Audio scale forwards to scale-aware devices rather than altering raw clip playback; MIDI piano highlighting and scale edits belong to MIDI owner. | `CV:B066`, `CV:B067`, `CV:B068` |
| REQ-CLIP-VIEW-016 | Extended panel shows launch controls for Session clips only. Arrangement audio has no Extended panel; Arrangement MIDI has MIDI bank/program only. Full launch and Follow Actions remain with clip-launch and future Session packet. | `CV:B070`, `CV:B071`, `CV:B074`, `CV:B075` |
| REQ-CLIP-VIEW-017 | MIDI bank/sub-bank/program selectors support documented 128 choices each and send on clip launch to supporting targets. Dash leaves corresponding message unset. MIDI bytes, value numbering and target support remain U. | `CV:B077`, `CV:B078`, `CV:B079` |
| REQ-CLIP-VIEW-018 | Warp off plays sample at original tempo irrespective of Set tempo; Warp on follows Set tempo when metrical structure is valid. Preparation/analysis and Warp algorithms remain with their owners. | `CV:B081`, `CV:B084`, `CV:B085` |
| REQ-CLIP-VIEW-019 | Reverse creates a new reversed sample and repoints clip, applying clip settings under documented transformation rules. Before save it resides in Temporary Folder; after Set save under Project Samples/Processed/Reverse. | `CV:B087`, `CV:B088` |
| REQ-CLIP-VIEW-020 | On reverse, Warp Markers and region/loop positions are reflected with sample material; clip envelopes keep timeline positions. Exact endpoint/frame/marker transformation is not specified. | `CV:B089` |
| REQ-CLIP-VIEW-021 | Long reversal may show progress and temporarily lock further actions while existing clips continue. When waveform generation begins, other actions/playback become available. Reverse pair is cached until application closes; no duration deadline or glitch-free guarantee. | `CV:B090`, `CV:B092` |
| REQ-CLIP-VIEW-022 | Session cannot reverse multiple clips together. Arrangement time-range Reverse Clip(s)/R is owned by Arrangement editing, whose MIDI-containing selection limitation remains applicable. | `CV:B091` |
| REQ-CLIP-VIEW-023 | Edit opens configured external sample editor; Live playback must stop before external processing. Return uses edited version; Warp Markers retained only when sample length unchanged. Shared source edits can affect other referencing clips. | `CV:B094`, `CV:B095`, `CV:B096` |
| REQ-CLIP-VIEW-024 | Clip Fade toggle is Session-only; Arrangement uses fade envelopes. Manual describes signal-dependent 0-4 ms edge fades and new-clip default on when Create Fades on Clip Edges enabled. Exact fade kernel remains with playback/Arrangement owners. | `CV:B098`, `CV:B099`, `CV:B100` |
| REQ-CLIP-VIEW-025 | RAM toggle requests referenced audio in memory rather than realtime disk reads; capacity/resource/disk-overload observations in prose are not a memory guarantee or benchmark. | `CV:B102`, `CV:B106` |
| REQ-CLIP-VIEW-026 | Hi-Q toggles higher-quality rate conversion with described CPU tradeoff. Approximate 19-semitone audibility prose supplies no spectral/CPU metric or universal threshold. | `CV:B108`, `CV:B109` |
| REQ-CLIP-VIEW-027 | Audio Gain uses dB; Pitch semitone knob/field and separate cents field are distinct, with 100 cents per semitone. Multi-selected differing gains display split triangle handles. | `CV:B112`, `CV:B113`, `CV:B114` |
| REQ-CLIP-VIEW-028 | Audio Transform panel offers Quantize for warped clips using current grid or specified meter and Amount; audio has no Generate panel. Marker movement/selection/rounding stays with Warp owner/future Warp workflow packet. | `CV:B130`, `CV:B131`, `CV:B132`, `CV:B133` |
| REQ-CLIP-VIEW-029 | Editor time-ruler vertical drag zooms and horizontal drag scrolls; wheel/trackpad scrolls. Behavior is shared by Sample and MIDI editors. | `CV:B138`, `CV:B139` |
| REQ-CLIP-VIEW-030 | Z/Zoom to Clip Selection zooms current time selection; X returns one zoom state per press, including repeated Z history. | `CV:B140` |
| REQ-CLIP-VIEW-031 | Selector overview spans clip Start-End; outline represents visible editor portion and dragging scrolls/zooms. Follow scrolls with playhead, pauses for editor edits and resumes after stop/restart or click in scrub area. MIDI-specific editor Follow stays with MIDI owner. | `CV:B141`, `CV:B142` |
| REQ-CLIP-VIEW-032 | Start/End markers drag or move with left/right arrows; Alt Win/Option Mac plus arrows on either selected marker moves whole region. | `CV:B145` |
| REQ-CLIP-VIEW-033 | Permanent Scrub Areas on permits click in lower waveform or scrub area to jump playback; off permits Shift-click in scrub area or beat-time ruler. | `CV:B146`, `CV:B148` |
| REQ-CLIP-VIEW-034 | Scrub jumps use global quantization; holding left button repeats a portion the size of selected quantization, with small/None allowing scrubbing. Chase MIDI Notes routes to playback-core note/chase gaps; no repeated-note oracle is supplied here. | `CV:B147` |
| REQ-CLIP-VIEW-035 | Loop brace handles edit start/end; brace drag moves it. Left/right nudges grid, up/down shifts by length; Ctrl Win/Cmd Mac left/right resizes by grid, up/down doubles/halves length. | `CV:B152`, `CV:B153`, `CV:B154`, `CV:B155`, `CV:B156`, `CV:B157` |
| REQ-CLIP-VIEW-036 | Clip begins at start marker regardless of loop brace, allowing initial material to run into a later loop. | `CV:B159` |
| REQ-CLIP-VIEW-037 | Sample header displays name/rate/depth/channel count. Multi-selection shows sample count and asterisk for differing properties. Name click/Show in Browser reveals source. | `CV:B161`, `CV:B162`, `CV:B163` |
| REQ-CLIP-VIEW-038 | Unlooped Crop Clip Sample uses Start-End; looped cropping begins at earlier Start/Loop Start and ends at Loop End. | `CV:B165`, `CV:B166` |
| REQ-CLIP-VIEW-039 | Time selection exposes Crop Clip Sample to Time Selection; Ctrl+Shift+J Win/Cmd+Shift+J Mac triggers applicable crop command. | `CV:B167`, `CV:B169` |
| REQ-CLIP-VIEW-040 | Audio crop creates a new shorter sample, temporarily in configured Temporary Folder and after save in Project Samples/Processed/Crop. | `CV:B168` |
| REQ-CLIP-VIEW-041 | Browser drag to Clip View or selected browser sample double-click/Enter replaces referenced sample. Pitch/volume settings remain; Warp Markers retained only for exact same source length. | `CV:B172`, `CV:B173` |
| REQ-CLIP-VIEW-042 | Show Similar Files opens similarity search; Manage Sample File opens Set File Manager with current source selected. File Manager replacements/destructive edits can affect all clips/instruments sharing source. | `CV:B174`, `CV:B175` |
| REQ-CLIP-VIEW-043 | Drag from empty clip slot or Ctrl Win/Cmd Mac/Shift extends clip multi-selection. Visible properties generally include only common properties of selected contents. | `CV:B177` |
| REQ-CLIP-VIEW-044 | Mixed-value multi-selection shows a value range. Dragging control to absolute maximum/minimum makes selected settings identical and subsequently adjustable as one. | `CV:B178` |
| REQ-CLIP-VIEW-045 | Clip Update Rate in Record/Warp/Launch settings quantizes changes to a running clip. Launch Mode/Warp Mode can be defaults for new clips. Complete affected-control set, rate choices and precedence versus global launch quantization are U. | `CV:B180` |
| REQ-CLIP-VIEW-046 | Save Default Clip button is audio-specific and supports multi-selected samples; its ASD/new-import/nonretroactive semantics are owned by REQ-MEDIA-FILE-010, distinct from Live Clip devices. | `CV:B028`, `CV:B029`, `CV:B030`, `CV:B031` |

## Unknown lifecycle, boundaries and errors

| U requirement | Required outcomes | Case suffixes |
| --- | --- | --- |
| REQ-CLIP-VIEW-U-REGION | Required region/loop input bounds and error outcomes remain unknown. | `CV-U-BOUNDARY`, `CV-U-MALFORMED` |
| REQ-CLIP-VIEW-U-TIMING | Required ordering between edits, scrub, launch and transport remains unknown. | `CV-U-TIMING`, `CV-U-TRANSPORT` |
| REQ-CLIP-VIEW-U-UNDO | Required edit/processed-file undo/redo transactions remain unknown. | `CV-U-UNDO`, `CV-U-AUTOMATION` |
| REQ-CLIP-VIEW-U-PERSIST | Required save/reopen/default/processed-file state remains unknown. | `CV-U-PERSISTENCE`, `CV-U-SOURCE-LOSS` |
| REQ-CLIP-VIEW-U-CANCEL | Required cancellation/progress/error outcomes remain unknown. | `CV-U-CANCEL`, `CV-U-ERROR` |
| REQ-CLIP-VIEW-U-TEARDOWN | Required clip/view/Set teardown and concurrent-selection outcomes remain unknown. | `CV-U-TEARDOWN`, `CV-U-SELECTION-RACE` |
| REQ-CLIP-VIEW-U-AUDIO | Required numerical audio and media-boundary oracles remain unknown. | `CV-U-AUDIO`, `CV-U-RATE` |
| REQ-CLIP-VIEW-U-MULTI | Required multi-selection/common-value/context outcomes remain unknown. | `CV-U-MULTI`, `CV-U-PROGRAM` |

All malformed/source-loss/disk/external-edit/close tests operate on disposable
owned media and Set copies. Cancellation availability, unsupported action/refusal,
undo grouping, processed-file persistence, shared-reference side effects and
concurrent selection are explicit unknowns. Synchronous menu descriptions do not
make error, cancel or teardown obligations inapplicable. Runtime cases compare
no application until an independent source/oracle exists.

## Acceptance catalog and timing limits

The [requirement view](../../analysis/ableton-live-12.4.3/full-spec-v1/clip-view/requirements.json) and
[62 finite cases](../../analysis/ableton-live-12.4.3/full-spec-v1/clip-view/cases.json) contain 46 D12 cases and 16 U cases.
All have `executed:false`, `target_grade:U`, `expected:null` and `comparison:null`.
Documentary visible-state comparators apply only to the named choices/relations;
all signal and timing obligations have no documentary comparator. There are
**54 requirements:46 D12 and8 U**, with **zero exact-target graded cases**.
Positive, negative, boundary, selection and timing/signal proposals are retained
alongside malformed/cancel/undo/persistence/source-loss/automation/teardown/rate
and MIDI-output obligations. No requirement or full product family is complete.

Source hypotheses stay scoped: an audio Scale change without devices does not
establish a downstream scale-aware device response; Warp off forbids audio loop
but not all playback; reverse reflects material-bound positions while clip
envelopes stay in clip time; equal source length is the documented predicate for
marker retention on replace/external edit, with actual length metric U. Session
Clip Fade toggle is distinct from Arrangement fades. Global launch quantization
and Clip Update Rate are not silently assigned one arithmetic law. The clip
meter display-only claim does not override already scoped launch/follow timing
requirements that use clip meter for a separate stored-time operation.

## Source-context questions

**CV-U-MIDI-UTILITIES:** `CV:B126` (§8.5.2) describes Humanize variation up to half
a grid division, while the MIDI owner REQ-MIDI-EDIT-012 says a quarter division
each direction. Total span versus per-direction displacement may reconcile these;
no contradiction or replacement law is asserted. `CV:B122` describes an Add
Interval button and Interval Size control, while REQ-MIDI-EDIT-011 separately
specifies immediate slider action. Exact gesture/preconditions need matching
before reconciliation. Neither computation is reauthored here. Root owns the
shared question and affected-owner update through separate reviewed changes.

Other required unknowns include exact-build parity, all audio/marker/time
arithmetic, full multi-selection/common-property matrix, file/preview/history
transactions, selector bytes/delivery, complete accessibility and settings
precedence. Full Session/Follow Actions and detailed Warp behavior remain
separate unclosed packets.

## Analyst evidence appendix

Official [Clip View chapter](https://www.ableton.com/en/live-manual/12/clip-view/),
Version12, captured 2026-10-19. [Source metadata](../../analysis/ableton-live-12.4.3/full-spec-v1/clip-view/source.json) retains
UTC/URL/length and SHA-256
`30f156e6d83c8f4caf3fe9dcf55bb2b764dc42ed8cbd3847863a53747851bd80`.
[HTML](../../analysis/ableton-live-12.4.3/full-spec-v1/clip-view/manual-clip-view-2026-10-19.html) is immutable source;
[180 paragraph/heading blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/clip-view/manual-blocks.json) retain exact HTML
lines and full numbered heading context. [Text](../../analysis/ableton-live-12.4.3/full-spec-v1/clip-view/manual-text.txt)
is navigation only. CV:B001-B180 covers chapter8 through §8.14, excluding sidebar
TOC/footer. [Source routing](../../analysis/ableton-live-12.4.3/full-spec-v1/clip-view/source-routing.json) distinguishes this
owner from neighboring content and context; it is not a complete coverage ledger.

[Author manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/clip-view/manifest-author-r1.json) freezes payloads, both
canonical snapshots and the inventory TOC pin. [Author validation](../../analysis/ableton-live-12.4.3/full-spec-v1/clip-view/validation-author-r1.json)
reports focused identity/catalog/link/whitespace checks only. These analysis
links require sanitization and separate review before handoff.

## Revision and handoff

Revision1 is a frozen partial author draft awaiting independent semantic review.
No existing release is expanded or changed; no handoff is published here.
