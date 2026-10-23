"""Materialize a bounded analyst draft; never executes Live or changes source bytes."""
from pathlib import Path
import hashlib
import json
import re
from capture import extract, SOURCE, DIGEST

P = Path(__file__).resolve().parent
ROOT = P.parents[3]
assert (ROOT / 'wiki/schema.md').is_file()
blocks = {b['id']: b for b in extract()}
# Contract, exact source blocks, finite action, documentary observation, kind.
DATA = [
('Clip launch gestures', 'The triangular clip button requests playback; selecting a clip by name then Enter also launches it, and arrows move to neighboring clips. Grid position does not prescribe playback order. Launch mode/quantization arithmetic remains owned by SPEC-CLIP-LAUNCH and SPEC-PLAYBACK-CORE.', [8,12], 'Select owned clip A by name, press Enter, navigate to B with arrows and separately click B\'s triangular launch control.', 'Named gestures request the selected clips; exact event/sample boundary and mode-specific scheduling remain unknown.', 'documented-control'),
('Clip stop and deactivate contexts', 'Square Clip Stop controls exist in slots and Track Status. Pressing 0 on selected Session clips deactivates those clips. Stopping a Session clip leaves global Play highlighted and song position advancing. Reactivation/toggle policy is not stated here.', [9,10,13], 'With a playing Session clip and global transport, stop it using each square control in separate reset trials; separately select one then two clips and press 0.', 'Clip stop leaves global transport running; 0 is a selected-clip deactivation action. Waveform tails and exact stop boundary are ungraded.', 'documented-state'),
('Global double Stop', 'Pressing the Control Bar Stop button twice stops playback of the whole Set and returns Arrangement Position to 1.1.1. Single-stop/continue arithmetic remains in transport/playback contracts.', [14], 'Start a disposable Set away from 1.1.1, then press Control Bar Stop twice.', 'Set playback stops and displayed position returns to1.1.1; double-press timing threshold and sample boundary remain unknown.', 'documented-state'),
('Session clip metadata', 'Edit/menu-context Rename handles clips and multiple selected clips; Edit Info Text supplies clip annotation and context color palette supplies custom clip color. Text grammar, maximum lengths and multi-selection value conflicts are unknown.', [15], 'Rename selected clips A/B using Edit and context commands in separate trials; add owned info text and choose an admitted color.', 'The named commands and per-clip metadata edits are documented; exact multi-rename naming pattern and persistence remain unknown.', 'documented-control'),
('Grid selection and moving', 'Drag/drop moves clips in the grid. Shift or platform Ctrl/Cmd supports multi-clip selection before dragging; dragging from an empty slot can rubber-band select. The introductory paragraph names Ctrl without a platform qualifier; platform-specific modifier interpretation remains uncertain outside the explicitly qualified grid paragraph.', [16,54], 'In the five-scene grid select adjacent and nonadjacent clips, then drag them; separately rubber-band from a known empty slot.', 'Selection/move gestures are available; destination collision, cross-type refusal, exact geometry and cross-platform modifier equivalence remain unknown.', 'documented-control'),
('Group slots', 'A group slot is shaded when contained tracks have at least one clip in that scene, using the left-most clip color. Its launch control launches the corresponding clips; a group slot with no corresponding clips has a stop control. Clicking a group slot selects the referred clips.', [17], 'Prepare Group G with differently colored clips on two child tracks in scene A, a single child clip in B and no child clips in C; inspect and click each group slot.', 'Shading/color/control/selection reflect the stated configurations. Group launch/stop timing and nested-group behavior remain unknown.', 'documented-control'),
('Track clip exclusivity', 'A Session track plays only one clip at a time; alternative material belongs in that track\'s column. Voice tails, instruments and routed audio are not an extra clip playback instance.', [19], 'Use two nonempty distinguishable Session clips in one track; request B while A is playing and separately use another track as a control.', 'One clip per track is the documented playback relation; crossfades, pending requests and waveform evidence remain ungraded.', 'signal-obligation'),
('Track width gestures', 'Drag title-bar edges to resize Session tracks; Alt on Windows or Option on Mac while resizing one track resizes all Session tracks. Narrow presentation retains clip launch and essential track controls; minimum size and exact pixel layout are unknown.', [20], 'Resize one title edge normally, reset, then resize with the documented OS modifier.', 'Single/all-track resizing gestures are documented; pixel deltas, snapping and hidden-control thresholds remain unknown.', 'documented-control'),
('Track-header deactivation', 'With a Session track header selected, 0 deactivates that track. This context differs from selected-clip deactivation; the manual does not specify an activation toggle or selection precedence with a text editor focused.', [21], 'Select a known active track header with no text edit in progress and press 0; use selected-clip context in a separate reset trial.', 'The documented target is the selected track; downstream tails, sends and reactivation behavior are unknown.', 'documented-state'),
('Scene launch and cancellation', 'A Scene Launch control in the Main-track column launches the clips in its row together. Cancel Scene Launch in the Main-track context menu cancels a previously triggered scene launch. Exact cancellation deadline and already-committed launch behavior are unknown.', [22], 'Set explicit nonzero global quantization and request scene B while transport runs; independently confirm a pending launch before invoking Cancel Scene Launch. If no pending launch can be confirmed, retain U.', 'Scene request and pending-cancel gestures are documented; no sample deadline or rollback of already-playing clips is asserted.', 'documented-control'),
('Next-scene selection preference', 'After a scene launch the scene below is selected as the next to launch unless Select Next Scene on Launch in Launch Settings is Off. Last-scene wrap/creation, empty scenes and concurrent selection edits are unknown.', [23], 'With scenes A-E, select B then launch it under preference On; reset and repeat Off with a deliberately different prior selection.', 'On selects C; Off disables this automatic-next rule. The source does not specify every other selection side effect.', 'documented-state'),
('Scene metadata commands', 'Scene Rename is available in Edit/context menus and Tab can advance through successive scene renames. Edit Info Text supplies annotation; a context palette supplies color. Scene View title context also offers Rename/color for one or multiple selected scenes. Multi-scene naming transformation and platform/focus preferences remain unknown.', [24,44], 'Rename B then advance with Tab using a valid scene-name editing focus; separately annotate/color B and invoke Scene View title context on B/D.', 'The named commands/rename traversal are documented. Multi-name transformation and persistence are not graded.', 'documented-control'),
('Scene ordering and position numbers', 'Scene drag/drop reorders rows. Shift-click selects adjacent scenes; Ctrl-click selects nonadjacent scenes in the retained text. Dragging nonadjacent scenes collapses them together; Ctrl+Up/Down moves them without collapsing. Scene numbers reflect current row position rather than stable identity. OS modifier substitution and boundary behavior are unknown.', [25,26], 'Use five uniquely named scenes A-E. Select B/D; drag them to a distinct interior destination. Reset and move B/D by the stated Ctrl+arrow gesture. Record order and displayed numbers.', 'Drag groups the selected scenes; keyboard movement preserves nonadjacent grouping distinction; numbers follow resulting positions. Exact insertion index/step and OS mapping remain unknown.', 'documented-state'),
('Scene tempo/meter editing', 'Dragging the Main-title left edge reveals scene tempo/meter controls, documented hidden by default. Values can be dragged or typed then Enter, and edited in Scene View. Launching a scene with assigned values adjusts project tempo/meter. This is a Version12 documentary claim; target storage and scheduler behavior remain separate.', [28,29,30,31], 'Reveal controls in a test-owned fresh Set; assign B tempo120 and meter3/4 by typing, then change via drag in a separate trial; launch B with both assignments explicitly enabled.', 'Controls and entry gestures exist; documented project assignment follows launch. Default visibility, activation moment and exact target applicability remain U.', 'documented-state'),
('Scene documented numeric domain', 'The captured manual permits scene tempo20-999 BPM and meter numerator1-99 with denominator1,2,4,8,16. These are documentary UI domains, not a replacement for SPEC-TRANSPORT-STATE\'s narrower evidence on numeric storage, parsing or scheduling.', [32], 'Enter20 and999 BPM in separate scenes, then meter1/1 and99/16; enumerate stated denominators with an interior numerator.', 'Documented endpoints and denominator choices; clamping, text normalization and values outside the domain are unknown.', 'documented-control'),
('Disable/reset scene assignments', 'An enabled scene tempo/meter control can be disabled and reset with Return to Default or Delete; double-click disables it. The reset stored numeric value and retention on double-click are not supplied.', [33], 'Begin with B tempo137/meter3/4 assigned and enabled; independently reset using Return to Default, Delete and double-click in separate restored trials.', 'The stated controls become disabled; Return to Default/Delete are documented reset actions. No numerical reset sentinel or hidden-value retention is asserted.', 'documented-state'),
('Scene keyboard traversal', 'Left/right arrows navigate from selected slots/scenes to tempo/meter controls. Within scene name/tempo/meter editing, Tab/Shift-Tab advances/reverses controls and crosses to the next/previous scene at row ends. Enter on a selected tempo/meter control first selects the scene; a second Enter launches it. Keyboard accessibility preference/context interactions remain unproven.', [34,35], 'With main-window Tab focus navigation enabled where required, select B tempo control; press Enter once then again. Separately edit B name and traverse controls/neighbor scenes using Tab/Shift-Tab.', 'Documented traversal and two-stage Enter workflow; simultaneous mapping, text-editor capture and other preference states remain unknown.', 'documented-control'),
('Scene assignment indicator', 'A scene with assigned tempo and/or meter change has a colored Scene Launch button. The captured text supplies no exact color, contrast, accessibility label or mapping from scene custom color.', [36], 'Use distinct B tempo-only, C meter-only and D both assigned, alongside A with neither assigned; inspect launch controls.', 'Assigned changes have the documentary colored indicator; pixel/color values and unassigned presentation are unknown.', 'documented-control'),
('Pre-Live11 scene-name migration', 'For Sets made before Live11 with tempo/meter in scene names, the manual describes carrying those values into scene controls on opening newer Live and widening Main to expose them. Exact legacy grammar, build boundary, malformed-name handling and migration round trips remain unknown.', [37], 'Use a separately identified future owned pre-Live11 Set with known scene-name tempo/meter values; open a disposable copy. No suitable historical fixture is retained by this packet.', 'Documented carry-over and control visibility only; there is no current executable migration oracle or target pass.', 'documented-state'),
('Scene View selection context', 'Selecting one/multiple scenes, clicking a scene tempo/meter control, or clicking Main title opens Scene View. Its top edits tempo/meter; lower controls expose scene Follow Actions, whose execution belongs to the launch owner. For one selected scene its title shows name/number/color if assigned; multiple scenes show selection count.', [39,40,41,42,43], 'Open Scene View via each named context using B and B/D selections; inspect title and both control regions.', 'Documented panel/title roles and selection count; mixed property display and Follow Action execution remain unknown.', 'documented-control'),
('Track Status presentation', 'Looping clips show a pie chart with right-side loop length in beats and left-side number of played loops. A playing group shows a pie without numbers. One-shots show progress and remaining minutes:seconds. Monitored audio/MIDI show microphone/keyboard icons; Arrangement playback shows a miniature Arrangement. Overlapping status precedence and update rounding are unknown.', [46,47,48,49,50], 'Use separate reset looping, one-shot, monitored-audio, monitored-MIDI, group-playing and Arrangement-playing fixtures; inspect Track Status with independently confirmed activity.', 'Named context-dependent display roles; image pixels, timing/rounding and conflicting-state priority are unknown.', 'documented-control'),
('Multi-file import layout', 'Browser import or recording can populate Session. Multiple raw audio/MIDI files default to one Session column; Ctrl on Windows or Cmd on Mac before drop spreads them over tracks. This multi-track drop shortcut does not apply to Live Clips with embedded devices. Media decoding and recording remain in their owners.', [52,53], 'Use two independently valid owned raw audio files and separately two MIDI files; drop normally and with the OS modifier into empty slots. Repeat with two independently valid Live Clips.', 'Raw files use vertical or multi-track layout as documented; the shortcut is not promised for Live Clips. Exact .alc fallback, track creation defaults and errors remain unknown.', 'documented-control'),
('Select on Launch preference', 'Clip launch normally selects the clip for Clip View. Turning off Select on Launch in Launch Settings lets the current view/focus remain when clips or scenes launch. This preference is separate from Select Next Scene on Launch.', [56], 'Focus a return-track device panel; launch B clip and scene in separate trials with Select on Launch Off, then restore the same setup with On for clip launch.', 'Off documents view retention, while default clip launch selects it. Scene selection interactions, default preferences in this target and OS focus details remain unknown.', 'documented-state'),
('Stop-button editing', 'Edit Add/Remove Stop Button adds/removes grid Clip Stop controls. Removing an empty row/track stop control permits scene launch without affecting that track. Launch scheduling and empty armed-slot recording policy remain owned by launch/recording contracts.', [58], 'Play a nonempty clip on track A; remove the stop control from empty A/sceneC and launch C; compare restored-stop setup in a separate reset trial.', 'The remove-stop setup documents leaving A unaffected by C. Quantized stop audio/tails and competing recording settings are unknown.', 'signal-obligation'),
('Insert Scene', 'Create Insert Scene inserts an empty scene below the current selection. Multi-selection anchor, selection after insert and scene count limits are unknown.', [60,61], 'Select single interior scene B in A-E and invoke Create Insert Scene.', 'One new empty scene is inserted below B. Slot identity, undo and persistence remain unknown.', 'documented-state'),
('Capture and Insert Scene', 'Create Capture and Insert Scene inserts below current selection, copies currently running clips into it and launches it. The manual claims no audible interruption; this packet supplies no signal comparator or timing tolerance for that claim. Scene capture is distinct from Capture MIDI and Arrangement Record.', [60,62], 'Run distinct nonempty clips on A/B tracks, select scene C then invoke Capture and Insert Scene. Capture visible row/content/launch state and audio separately after a paired positive output baseline.', 'Documented new scene, copied running material and launch request. No-interruption audio and boundary alignment are explicitly ungraded.', 'documented-state'),
('Cross-view clip transfer', 'Copy/paste and drag permit Session/Arrangement clip transfer, including across separate windows. Arrangement-to-Session paste attempts matching top-to-bottom temporal ordering. Exact tiling, overlaps, metadata transfer and operation atomicity are unknown. Keyboard Second Window controls retain their OS-specific documented modifiers.', [75,76], 'Use two owned clips with separated Arrangement times; copy/paste into empty Session region. Separately drag through view selectors and between enabled main/second windows.', 'Transfer methods and intended temporal row ordering are documented; exact order for ties/overlaps and signal transformations are unknown.', 'documented-control'),
('Consolidate Time to New Scene', 'Arrangement Create/context Consolidate Time to New Scene makes one new clip per selected track from the selected time and places them in a new Session scene below prior selected scene. Audio tracks containing at least one selected clip generate new samples. The signal/destination contract for audio consolidation stays in REQ-ARRANGEMENT-010; exact silence-only, MIDI merge and file-failure behavior remain unknown.', [77], 'Select owned Arrangement material on audio A and MIDI B over one interior bar; select Session scene C as destination anchor; invoke Consolidate Time to New Scene and inspect scene/clip/file references.', 'Documented scene placement, per-track clips and sample creation condition; no sample bytes, normalization or codec oracle is supplied.', 'documented-state'),
]


def write(name, value):
    data = (json.dumps(value, indent=2, ensure_ascii=False)+'\n').encode() if not isinstance(value, str) else value.encode()
    path = P / name
    assert not path.exists() or path.read_bytes() == data, 'Refuse changed authored artifact: '+name
    path.write_bytes(data)


requirements, cases = [], []
for i, (title, contract, refs, action, expected, kind) in enumerate(DATA, 1):
    evidence = [{'block': f'SV-B{j:03d}', 'anchor': blocks[f'SV-B{j:03d}']['anchor'],
                 'html_line': blocks[f'SV-B{j:03d}']['html_line']} for j in refs]
    req = f'REQ-SESSION-VIEW-{i:03d}'
    requirements.append({'id': req, 'title': title, 'contract': contract, 'strength': 'D12', 'target_applicability': 'U', 'evidence': evidence})
    cases.append({'id': f'SV-{i:03d}', 'requirements': [req], 'kind': kind,
                  'preconditions': ['F-SV-GRID', 'per-case-context-overrides-fixture-defaults'],
                  'setup_and_action': action, 'documentary_expected': expected,
                  'documentary_comparator': None if kind == 'signal-obligation' else 'Named visible controls/choices/relationships only; no timing, waveform or hidden-state grade.',
                  'expected': None, 'comparison': None, 'target_grade': 'U', 'executed': False, 'evidence': evidence})
u_req = 'REQ-SESSION-VIEW-029'
requirements.append({'id': u_req, 'title': 'Lifecycle and boundary outcomes', 'contract': 'Required operational outcomes below remain unknown; documentary gestures and XML structure do not establish them.', 'strength': 'U', 'target_applicability': 'U', 'evidence': []})
unknowns = [
('BOUNDARY', 'Enter tempo19.999/1000, numerator0/100 and denominator3; press traversal/move commands at first/last scene; try empty selection and duplicate names.'),
('MALFORMED', 'On disposable copies open truncated/invalid media or invalid scene/slot saved state; import a claimed MIDI file with invalid contents.'),
('UNDO', 'Rename B, move B/D and insert a captured scene; Undo/Redo each action separately and inspect order, metadata and active playback.'),
('CANCEL', 'Begin multi-file drop/scene rename or pending launch and cancel before completion; repeat after independently observed commit in a separate copy.'),
('PERSISTENCE', 'Save/reopen owned Set with reordered/renamed/color scenes, nondefault widths, removed stop buttons and tempo/meter fields; inspect all values and view selection.'),
('SOURCE-LOSS', 'Remove an imported audio source or externally referenced clip asset from an owned copy, then launch/capture/transfer and inspect diagnostics/recovery.'),
('TRANSPORT', 'Run then stop/seek/restart with a pending scene, assigned tempo/meter and active clip; compare no-grid/global-grid/clip-grid configurations separately.'),
('AUTOMATION', 'Launch scene tempo/meter changes with active Arrangement automation and manually overridden controls; observe ownership without assuming precedence.'),
('TEARDOWN', 'During pending scene launch and active nonempty clips remove source track/group/scene in separate copies, then close/reopen Set.'),
('RATE', 'With active clips and status display, request44.1/48kHz and64/256-frame settings in separate running/stopped trials; no clock/driver capability inferred.'),
('FOCUS', 'Repeat 0/Enter/Tab/arrow gestures in clip-name edit, scene-name edit, tempo field, plug-in window and main window with Tab preference On/Off; record target/context.'),
('AUDIO', 'Record paired active-output baselines and scene-capture/stop/reorder transitions with owned distinct signals; interruption, crossfade, tails, scheduling and tolerance remain unknown.'),
]
for suffix, action in unknowns:
    cases.append({'id': 'SV-U-'+suffix, 'requirements': [u_req], 'kind': suffix.lower(),
                  'preconditions': ['F-SV-GRID', 'disposable-copies-only', 'active-nonmuted-positive-baseline-for-signal-claims'],
                  'setup_and_action': action, 'documentary_expected': None, 'documentary_comparator': None,
                  'expected': None, 'comparison': None, 'target_grade': 'U', 'executed': False, 'evidence': []})
assert len(DATA) == 28 and len(requirements) == 29 and len(cases) == 40
assert len({c['id'] for c in cases}) == 40
write('requirements.json', requirements)
write('cases.json', cases)
write('source.json', {'id': 'D12-SESSION', 'url': 'https://www.ableton.com/en/live-manual/12/session-view/', 'capture_utc': '2026-10-19T19:53:59.135059+00:00', 'version': 'Version12; exact12.4.3 applicability unknown', 'path': str(SOURCE.relative_to(ROOT)), 'bytes': 267328, 'sha256': DIGEST, 'source_metadata': '../recording/sources.json', 'figures': 'not separately inspected'})
write('fixtures.json', {'id': 'F-SV-GRID', 'status': 'authored future setup; no .als/media/recording retained or executed', 'set': 'Owned editable Set with five uniquely named scenes A-E; AudioA and MidiB plus GroupG containing AudioC/MidiD; at least one known empty slot in each track. Arm/record off unless case explicitly requires otherwise.', 'clips': 'Owned nonempty distinct one-bar A/B clip contents at admitted120BPM/4/4; audio is future retained220/440/660Hz tone assets, MIDI explicit valid owned note pairs; independently confirm current playback/control state before each trial.', 'contexts': 'Fresh reset per independent case; explicitly select per-case global quantization, scene assignments, clip launch mode, preferences and focus. Per-case settings override common setup. No implicit factory default, transparent instrument or reliable external driver is assumed.', 'positive_guard': 'Before testing stop/no-effect/continuity confirm active relevant clip, enabled/unmuted routing and nonzero audible output in a paired baseline. Silence, disabled clips, absent sources, zero sends or pending request without observed pending state cannot establish the outcome.', 'destructive': 'Use owned disposable copies only; never mutate immutable source/capture/published handoff bytes.', 'missing': 'Pre-Live11 migration Set and raw media/Live Clip fixtures must be separately retained and identified before future execution; their absence is unknown, never a pass.'})

front = '---\nid: {id}\ntype: {type}\nstatus: {status}\nupdated: 2026-10-19\naccess: analysis\nrevision: 1\ntarget: Ableton Live 12 Suite 12.4.3\n---\n\n'
spec = front.format(id='SPEC-SESSION-VIEW-WORKFLOWS', type='spec', status='draft')
spec += '''# Session View grid, scenes and presentation

This partial F-04/F-08 draft owns Session grid/scene gestures, selection,
metadata, scene assignment controls, Track Status and cross-view scene workflows.
[Coverage design](../research/full-live-specification-design.md) governs closure;
[research](../research/session-view-workflows.md) owns source interpretation.
It is not a complete Session specification or a released implementation input.

**D12/target-U:** the retained official Version12 chapter supplies documentary
behavior, not observed Live12.4.3 outcomes. Every target expectation/comparison
is null, every target grade U and every case unexecuted. U never passes. Named
choices and visible state proposals have documentary comparators only; no audio,
clock, numeric grammar, pixel, hidden-buffer or candidate architecture is imposed.

[Clip launch](clip-launch.md) owns launch modes, quantization, Legato, velocity
and Follow Actions; [playback](playback-core.md) and [transport](transport-state.md)
own finite timing computations. This draft does not resolve their unknowns.
[Arrangement](arrangement-editing.md) REQ020/021 owns Session override and Back
to Arrangement; REQ009/010 owns consolidation signal/destination. [Recording](recording-comping.md)
REQ031 owns Session performance recording, including the retained scene-name
qualifier; scene-field recording without that qualifier remains U.
[Set structure](live-set-structure.md) owns storage/scene identities, which are
distinct from position-based UI numbers. [MIDI mapping](midi-user-mapping.md),
[keyboard navigation](keyboard-navigation.md), [media](media-file-workflows.md)
and [Clip View](clip-view-workflows.md) retain their bounded owners. A link does
not establish composed behavior, focus precedence or version applicability.

## Requirements and finite cases

Use the [future fixture](../../analysis/ableton-live-12.4.3/full-spec-v1/session-workflows/fixtures.json)
with per-case mode/preference/focus overrides, reset histories and independently
confirmed active/nonzero output before any no-effect or continuity claim.
The [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/session-workflows/cases.json)
retains full finite actions and documentary expectations; the table is an index,
not evidence of exhaustive mode coverage. Compound requirements need additional
per-branch cases before coverage closure. Migration/media inputs are future
prerequisites, not existing captured fixtures or measured outputs.

'''
for r in requirements:
    spec += f"### {r['id']} — {r['title']}\n\n**{r['strength']}/target-U.** {r['contract']}\n\n"
    if r['evidence']:
        spec += 'Evidence: '+', '.join('`'+x['block']+'`' for x in r['evidence'])+'; [source blocks](#analysis-only-evidence).\n\n'
spec += '| Case | Requirement | Kind / finite action |\n| --- | --- | --- |\n'
for c in cases:
    spec += '| '+c['id']+' | '+c['requirements'][0]+' | '+c['kind']+': '+c['setup_and_action']+' |\n'
spec += '''
Counts:29 requirements (28 D12/1 U),40 proposed cases (28 documentary/signal
proposals and12 operational U probes). Two of the28 are signal obligations with
null documentary comparator; all40 target outcomes/comparisons remain null/U.
No original code, audio, candidate, hardware or whole application was executed.

## Unclosed outcomes

Exact-build applicability, complete per-gesture branches, field parsing/ranges,
selection/focus conflicts, OS modifier differences, launch/cancel deadlines,
last-scene boundaries, nested groups, capture continuity, transfer/consolidation
files, malformed inputs, undo/redo, persistence, source loss, automation ownership,
sample-rate/driver changes and teardown remain required unknowns. The current
chapter's scene-name recording wording is retained by the recording owner;
dedicated scene fields do not silently supersede that condition. Follow Action
execution and complete clip launch behavior remain with the launch owner.

## Analysis-only evidence

- [Retained chapter](../../analysis/ableton-live-12.4.3/full-spec-v1/recording/manual-12-session-view-2026-10-19.html),
  official [Version12 Session View](https://www.ableton.com/en/live-manual/12/session-view/),
  capture2026-10-19T19:53:59.135059+00:00,267328bytes,
  SHA-256 `16e29141f823e298d5fa7fee3b993861f6c38415f8432cd00ac89789e9470a31`.
- [77 exact HTML blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/session-workflows/source-blocks.json)
  retain heading context/line/text; [line view](../../analysis/ableton-live-12.4.3/full-spec-v1/session-workflows/source-blocks.txt)
  is derived navigation, not replacement source. Figures were not separately inspected.
- [Requirement/evidence catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/session-workflows/requirements.json)
  and [author manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/session-workflows/manifest-author-r1.json)
  freeze the review scope. Revision1 is an author draft awaiting independent review.
  No existing release is expanded and no application compatibility result is claimed.
'''
research = front.format(id='RES-SESSION-VIEW-WORKFLOWS', type='research', status='current')
research += '''# Session grid and scene workflow evidence

This is the evidence owner for [Session workflow contracts](../specs/session-view-workflows.md)
under the [full specification plan](full-live-specification-plan.md). It reuses
the exact official Session chapter retained in the recording packet; no new
network capture, original execution or binary investigation was performed.

## Source and extraction

[Source metadata](../../analysis/ableton-live-12.4.3/full-spec-v1/session-workflows/source.json)
retains original URL/capture UTC,267328bytes and SHA-256
`16e29141f823e298d5fa7fee3b993861f6c38415f8432cd00ac89789e9470a31`.
The [extractor](../../analysis/ableton-live-12.4.3/full-spec-v1/session-workflows/capture.py)
reads only the chapter_content HTML element, producing77 paragraph/list/heading
blocks with exact HTML lines and heading anchors. It asserts the source digest,
chapter start/end and refuses changed derived-artifact overwrites. Figures and
image-based glyphs were not inspected. The cross-view source paragraph loses
two inline icon glyphs in text extraction; its other named copy/paste and separate
window gestures remain readable. No icon appearance or hit target is inferred.

## Scope and interpretation

The behavior owner contains29 requirements/40 finite proposed cases. These are
partial documentary contracts, not28 closed gestures or a complete chapter.
All target outcomes are null/U/unexecuted. In particular:

- Scene controls' documented20-999BPM and meter domains do not replace the target
  storage/transport owner's traced numeric contracts. Text acceptance, clamping,
  clock rounding and timing remain U.
- Scene row numbers change with position; storage item identities are separate.
- Select Next Scene on Launch and Select on Launch are distinct settings. Current
  chapter defaults are documentation, not observed constructor preferences.
- The chapter's scene reorder paragraph names Ctrl without an OS qualifier; other
  import/selection paragraphs explicitly name Ctrl/Cmd. OS equivalence is unproven.
- General keyboard preferences and local edit traversal require explicit focus
  setup; shortcut labels alone do not prove dispatch priority.
- Capture and Insert Scene claims uninterrupted audio, but no signal/time
  comparator is supplied. Copied clips and visible launch state are separate.
- Session-to-Arrangement recording and override clauses remain in their existing
  canonicals. Retained scene-name tempo/meter recording language is not silently
  widened to all scene-field changes; exact-build applicability remains U.
- Follow Actions, clip launch scheduler, media decode and consolidation audio
  retain existing owners. No API, DSP, thread, buffer or candidate design follows
  from UI prose, file bytes or these cross-links.

## Packet and next evidence

[Finite future setups](../../analysis/ableton-live-12.4.3/full-spec-v1/session-workflows/fixtures.json)
name five scenes, audio/MIDI/group tracks, empty slots and independently valid
nonempty media/clips. Assets and a pre-Live11 migration Set are not yet retained;
no case may pass without its prerequisites. Twelve operational probes keep
boundary/malformed/undo/cancel/save/source-loss/transport/automation/teardown/rate/
focus/audio obligations open. Compound clauses need separate per-branch cases.

The [author seal](../../analysis/ableton-live-12.4.3/full-spec-v1/session-workflows/manifest-author-r1.json)
pins this source routing, cases, tools and canonical snapshots. Separate semantic
review, target-version evidence and eventual calibrated outcomes remain pending.
No profile/family is complete; no release or compatibility approval is implied.
'''
spec_path = ROOT / 'wiki/specs/session-view-workflows.md'
research_path = ROOT / 'wiki/research/session-view-workflows.md'
for path, value in [(spec_path, spec), (research_path, research)]:
    assert not path.exists() or path.read_text() == value, 'Refuse changed canonical'
    path.write_text(value)
write('spec-r1.md', spec)
write('research-r1.md', research)
print('29 requirements /40 target-U cases authored; freeze separately after checks')
