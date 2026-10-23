"""Author the bounded Clip View documentary workflow packet, without original execution."""
from pathlib import Path
from collections import Counter
import json

P=Path(__file__).resolve().parent
ROOT=P.parents[3]
BLOCKS={r['locator']:r for r in json.loads((P/'manual-blocks.json').read_text())}
REQ=[]
CASES=[]

def write(name,value):
    (P/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')

def add(numbers,kind,contract,action):
    n=len(REQ)+1;rid=f'REQ-CLIP-VIEW-{n:03d}';refs=[f'CV:B{i:03d}' for i in numbers]
    assert all(r in BLOCKS for r in refs)
    REQ.append({'id':rid,'provenance':'D12','target_applicability':'U','contract':contract,'source_id':'D12-CLIP-VIEW','source_blocks':refs,'html_lines':sorted({BLOCKS[r]['html_line'] for r in refs})})
    CASES.append({'id':f'CV-{n:03d}','requirements':[rid],'kind':kind,'fixture':'fixtures.json#CV-BASE','setup_and_action':action,'documentary_expected':contract,'documentary_comparator':None if kind in ['signal-obligation','timing-obligation'] else 'Compare only named visible controls, choices/eligibility, identities, file locations or explicit state relations; no pixels, hidden state, audio or timing tolerance.','expected':None,'comparison':None,'target_grade':'U','executed':False,'source_blocks':refs})

rows=[
([3,4,5,6], 'positive', 'Clip double-click in Session/Arrangement, Selector, Toggle or Ctrl+Alt+3 Win/Cmd+Option+3 Mac opens Clip View. Toggle while Device View is open stacks Clip View above it. Dragging top border resizes; bottom closes it.', 'With selected Session audio A then Arrangement MIDI M, use each opening route; Device View open then Toggle; resize then drag to bottom and reopen. Focus/modal assumptions explicit in CV-BASE.'),
([7,8], 'selection', 'Clip View opens in focused window and displays current clip even when selected in other window. F12 moves view between windows; Shift+Tab does so only when Use Tab Key to Navigate is off.', 'Two windows with A/M; alternate focused window and clip selection, F12, Shift+Tab with navigation option off/on. Shortcut conflicts with OS/device remain U.'),
([13,15,16], 'signal-obligation', 'Clip Activator off deactivates clip playback in Session launch or Arrangement timeline; context Deactivate/0 also available. Multi-selection off deactivates all selected clips.', 'Audible A and B first active with unmuted routed output; select both and switch Activator off. Test single A via context and focused 0 separately. Playback cutoff/held-note/tail timing remains U.'),
([18,19,20,21], 'positive', 'Clip Rename and Edit Info Text are available through specified title/Edit/clip menus. Audio clip rename does not rename source sample. Multi-selection shows count; common new name is not displayed as title.', 'Rename A to Owned A through title context, confirm source path/name unchanged; edit Info Text; select A/B, rename both to Pair and inspect count/title versus single-clip names.'),
([23,24,25,26], 'selection', 'New clips inherit track color; palette changes clip color. Track/group Assign Color commands affect clips only in the invoking Session or Arrangement view. Multi-selection title is striped while individual selected clips accept color.', 'Distinct track/group and clip colors in both views; invoke Assign Track Color in Session then inspect Arrangement unchanged; repeat opposite direction; multi-select A/B and choose one palette entry.'),
([11,34,35], 'positive', 'Title plus panels/editor are shared layout. Main/Extended properties are common; audio adds Audio Utilities/Transform, MIDI adds Pitch-Time/Transform/Generate. Editors and additional properties depend on clip type.', 'Select A then M and inspect panel names; compare controls without changing content. Actual MIDI note/tool operations remain with MIDI owner.'),
([36,37,38], 'positive', 'Panels support horizontal, vertical or automatic arrangement through border drag/View menu/title context. Arrangement is remembered on future opening. Title double-click/Fold minimizes panels.', 'Drag panel right edge left/right, select each layout menu option, Fold then reopen; close/reopen view and inspect chosen layout. Restart/Set/global persistence scope remains U.'),
([40,41,42,43,44,45], 'positive', 'Audio editor modes are Sample/Envelope; MIDI modes Notes/Envelope/MPE. Tabs/View commands or Alt+Tab Win/Option+Tab Mac switch modes.', 'Select A then M, enumerate tabs and switch via each route with editor focused; no MIDI expression or envelope computation is defined here.'),
([49,50,51], 'positive', 'Start/End value fields define unlooped playing region. Warped audio displays bars-beats-sixteenths; unwarped displays minutes-seconds-milliseconds.', 'A Warp on: Start 1.1.1 End 3.1.1; Warp off inspect units and set 0:01.000 to 0:03.000. Loop off; do not equate representation with a stored time conversion law.'),
([50], 'timing-obligation', 'Set Start/End during playback take current playhead position according to global quantization; exact rounding/ties/dispatch are unspecified here.', 'Playing warped A, global quantization 1 Bar then 1/4 then None; invoke each Set at recorded off-grid times. Clip update rate explicitly retained; do not substitute released launch arithmetic for these setters.'),
([52,53,150,151], 'negative', 'Loop Position/Length and Loop toggle define repeat region; initial Loop Length is described as total clip length. Audio loop is unavailable until Warp on; unwarped audio cannot loop.', 'Select A Warp off and inspect Loop eligibility, enable Warp and Loop, set Position 2.1.1 Length 1.0.0. New-clip default and previously imported defaults are separate contexts; exact target default U.'),
([54,55,56], 'timing-obligation', 'Set Loop Position moves start to current playhead rounded by global quantization and enables loop; Set Loop Length then moves end to current position. With loop off, Set Length ends loop at current position preserving preset length and enables it.', 'A preset loop length one bar, Loop off. Trial 1 set Position then later Length while playing; reset then trial 2 Set Length only. Global quantization 1 Bar then None; retain resulting start/length without inventing rounding.'),
([57], 'positive', 'Set buttons, Loop toggle, loop region and Start/End positions are eligible MIDI mapping targets; actual controller mapping/takeover belongs to MIDI user mapping.', 'Enter MIDI Map Mode with selected A, inspect each named target; do not assert mapping emission, value codec, relative step or hardware behavior.'),
([59,60], 'signal-obligation', 'Clip time signature is per-clip display state, independent from project meter and does not change clip playback.', 'Audible A loop and B distinct loop, project 4/4; change A clip meter to 3/4 then 7/8 with global meter fixed. Compare visible rulers and future playback timing, requiring retained audible baseline; no bit equality asserted.'),
([66,67,68], 'positive', 'Scale button/root/name are clip properties. Audio scale forwards to scale-aware devices rather than altering raw clip playback; MIDI piano highlighting and scale edits belong to MIDI owner.', 'A with no devices then independently identified scale-aware device: scale off/on C major then D minor. Inspect controls only; device response and raw-audio invariance remain ungraded under own owners.'),
([70,71,74,75], 'negative', 'Extended panel shows launch controls for Session clips only. Arrangement audio has no Extended panel; Arrangement MIDI has MIDI bank/program only. Full launch and Follow Actions remain with clip-launch and future Session packet.', 'Select Session A/M then Arrangement A/M; inspect Extended presence and launch versus program controls without assuming engine fire semantics.'),
([77,78,79], 'positive', 'MIDI bank/sub-bank/program selectors support documented 128 choices each and send on clip launch to supporting targets. Dash leaves corresponding message unset. MIDI bytes, value numbering and target support remain U.', 'Session M routed to declared supporting target or record prerequisite as unavailable; inspect each selector first/last displayed choices and dash, independently select bank/sub-bank/program. Grade selectors only; no transmission oracle.'),
([81,84,85], 'signal-obligation', 'Warp off plays sample at original tempo irrespective of Set tempo; Warp on follows Set tempo when metrical structure is valid. Preparation/analysis and Warp algorithms remain with their owners.', 'A independently prepared beat loop, Warp off/on, Set tempo 120 then 90 then 150; active audible output, no groove/devices. Audio/time criterion remains U; only toggle/eligibility is observable documentary control.'),
([87,88], 'positive', 'Reverse creates a new reversed sample and repoints clip, applying clip settings under documented transformation rules. Before save it resides in Temporary Folder; after Set save under Project Samples/Processed/Reverse.', 'Owned copy A with known asymmetric source, invoke Reverse; retain new source identity/location before and after saving test Set. Do not mutate original evidence or assume PCM representation.'),
([89], 'signal-obligation', 'On reverse, Warp Markers and region/loop positions are reflected with sample material; clip envelopes keep timeline positions. Exact endpoint/frame/marker transformation is not specified.', 'A with distinguishable marker in second bar, asymmetric region/loop and first-half volume envelope; reverse and retain positions, source audio and envelope. No reflection arithmetic or endpoint equality invented.'),
([90,92], 'timing-obligation', 'Long reversal may show progress and temporarily lock further actions while existing clips continue. When waveform generation begins, other actions/playback become available. Reverse pair is cached until application closes; no duration deadline or glitch-free guarantee.', 'Retain test-owned long source, reverse while independent B plays, observe progress/action eligibility; revert and reverse again in same session, then after restart. Caching speed and audio continuity are ungraded.'),
([91], 'negative', 'Session cannot reverse multiple clips together. Arrangement time-range Reverse Clip(s)/R is owned by Arrangement editing, whose MIDI-containing selection limitation remains applicable.', 'Session select A/B and inspect Reverse availability; compare single A. Arrangement operation is routed to REQ-ARRANGEMENT-007 rather than redefined here; exact disabled-command UI U.'),
([94,95,96], 'positive', 'Edit opens configured external sample editor; Live playback must stop before external processing. Return uses edited version; Warp Markers retained only when sample length unchanged. Shared source edits can affect other referencing clips.', 'Owned shared sample A on two clips, stop transport and open declared configured external editor; make same-length then different-length copies in separate trials and return. Missing editor/errors and byte/frame meaning of equal length remain U.'),
([98,99,100], 'negative', 'Clip Fade toggle is Session-only; Arrangement uses fade envelopes. Manual describes signal-dependent 0-4 ms edge fades and new-clip default on when Create Fades on Clip Edges enabled. Exact fade kernel remains with playback/Arrangement owners.', 'Compare Session/Arrangement A; preference on/off create new test clips and inspect toggle. Use source with nonzero edge positive baseline for any future fade output; no shape or timing tolerance inferred.'),
([102,106], 'positive', 'RAM toggle requests referenced audio in memory rather than realtime disk reads; capacity/resource/disk-overload observations in prose are not a memory guarantee or benchmark.', 'Toggle RAM on/off for A and inspect control only. Resource-limit and actual I/O/memory behavior require retained evidence and remain U.'),
([108,109], 'positive', 'Hi-Q toggles higher-quality rate conversion with described CPU tradeoff. Approximate 19-semitone audibility prose supplies no spectral/CPU metric or universal threshold.', 'A source rate differing from host, nonzero transposition, inspect Hi-Q on/off; do not grade aliasing/CPU from qualitative prose or infer the interpolation kernel.'),
([112,113,114], 'positive', 'Audio Gain uses dB; Pitch semitone knob/field and separate cents field are distinct, with 100 cents per semitone. Multi-selected differing gains display split triangle handles.', 'A/B Gain -12/-6 dB and Pitch 0/+7 st, select both and inspect split handles; set single A Pitch +12 and cents +25 via named controls. Exact gain/frequency conversion and domain endpoints U.'),
([130,131,132,133], 'negative', 'Audio Transform panel offers Quantize for warped clips using current grid or specified meter and Amount; audio has no Generate panel. Marker movement/selection/rounding stays with Warp owner/future Warp workflow packet.', 'Warped A inspect Quantize grid/meter/Amount controls and absence of Generate; Warp off compare eligibility without asserting refusal/auto-enable. Do not reproduce MIDI transform/generator laws.'),
([138,139], 'positive', 'Editor time-ruler vertical drag zooms and horizontal drag scrolls; wheel/trackpad scrolls. Behavior is shared by Sample and MIDI editors.', 'A then M, drag ruler vertically/horizontally and scroll wheel with distinct time selection; compare visible time extent only, no pixel or gesture sensitivity law.'),
([140], 'positive', 'Z/Zoom to Clip Selection zooms current time selection; X returns one zoom state per press, including repeated Z history.', 'Select beats 2-3, press Z; narrower selection Z again, press X twice and inspect prior extents. History beyond these operations remains U.'),
([141,142], 'selection', 'Selector overview spans clip Start-End; outline represents visible editor portion and dragging scrolls/zooms. Follow scrolls with playhead, pauses for editor edits and resumes after stop/restart or click in scrub area. MIDI-specific editor Follow stays with MIDI owner.', 'A time selection zoomed, drag overview then enable Follow; play, edit region, stop/restart and separately click scrub. Inspect display relation only; scheduler/latency U.'),
([145], 'positive', 'Start/End markers drag or move with left/right arrows; Alt Win/Option Mac plus arrows on either selected marker moves whole region.', 'A Start beat 1 End beat 5, select start then end in separate trials and arrow; repeat with Alt/Option, inspect both markers relative movement. Step/snap boundary law remains U.'),
([146,148], 'positive', 'Permanent Scrub Areas on permits click in lower waveform or scrub area to jump playback; off permits Shift-click in scrub area or beat-time ruler.', 'A playing, preference on click lower waveform and scrub; off Shift-click scrub and ruler. Upper/lower hit-test edge, setting persistence and exact click versus edit precedence remain U.'),
([147], 'timing-obligation', 'Scrub jumps use global quantization; holding left button repeats a portion the size of selected quantization, with small/None allowing scrubbing. Chase MIDI Notes routes to playback-core note/chase gaps; no repeated-note oracle is supplied here.', 'A with distinguishable beats, playing/unmuted; global quantization 1 Bar then 1/16 then None, click and hold scrub at recorded positions then release. Clip update rate and editor focus retained; exact boundary/timing U.'),
([152,153,154,155,156,157], 'positive', 'Loop brace handles edit start/end; brace drag moves it. Left/right nudges grid, up/down shifts by length; Ctrl Win/Cmd Mac left/right resizes by grid, up/down doubles/halves length.', 'A loop one bar at beat 5, fixed 1/4 grid; select brace, apply each direction in reset trials, inspect extent and position. Minimum lengths, snap/tie and cross-source bounds U.'),
([159], 'signal-obligation', 'Clip begins at start marker regardless of loop brace, allowing initial material to run into a later loop.', 'A Start beat 1, Loop Position beat 5 Length 4 beats, source nonempty through beat 9; launch from stopped and running transport separately, retain attack/run-in/repeat positions. Launch dispatch remains existing owner.'),
([161,162,163], 'positive', 'Sample header displays name/rate/depth/channel count. Multi-selection shows sample count and asterisk for differing properties. Name click/Show in Browser reveals source.', 'A mono 48 kHz 24-bit and B stereo 44.1 kHz 16-bit owned validated media; select singly/together inspect fields/asterisks/count, click name and Show in Browser. Source deduplication/count for shared references U.'),
([165,166], 'positive', 'Unlooped Crop Clip Sample uses Start-End; looped cropping begins at earlier Start/Loop Start and ends at Loop End.', 'Reset owned A: unlooped Start beat 3 End 7; then looped Start3 LoopStart5 LoopEnd9; then Start5 LoopStart3 LoopEnd9. Invoke Crop Clip Sample and inspect generated region bounds; frame rounding U.'),
([167,169], 'positive', 'Time selection exposes Crop Clip Sample to Time Selection; Ctrl+Shift+J Win/Cmd+Shift+J Mac triggers applicable crop command.', 'A with nonempty time selection beats 2-4 distinct from region/loop, inspect time-selection command and invoke via menu then shortcut on reset copy. Degenerate selection/precedence outcomes U.'),
([168], 'positive', 'Audio crop creates a new shorter sample, temporarily in configured Temporary Folder and after save in Project Samples/Processed/Crop.', 'Crop owned A, inspect new source reference/path before save and after saving test Set; exact source ownership, references used by other clips and file bytes remain U.'),
([172,173], 'positive', 'Browser drag to Clip View or selected browser sample double-click/Enter replaces referenced sample. Pitch/volume settings remain; Warp Markers retained only for exact same source length.', 'A Gain -6 dB Pitch +7 st, marker interior; replace with equal-length C then unequal-length B in reset copies via each route. Keep file descriptors retained; exact length metric/unequal-marker reset behavior U.'),
([174,175], 'positive', 'Show Similar Files opens similarity search; Manage Sample File opens Set File Manager with current source selected. File Manager replacements/destructive edits can affect all clips/instruments sharing source.', 'A shared by two clips, inspect Show Similar Files and Manage Sample File selection; route actual global replacement to project/media owner. No similar-result ordering or automatic asset replacement law.'),
([177], 'selection', 'Drag from empty clip slot or Ctrl Win/Cmd Mac/Shift extends clip multi-selection. Visible properties generally include only common properties of selected contents.', 'Session A/B then A/M, create selection by each gesture; inspect audio-only controls versus common properties. Exact full eligibility matrix remains U.'),
([178], 'boundary', 'Mixed-value multi-selection shows a value range. Dragging control to absolute maximum/minimum makes selected settings identical and subsequently adjustable as one.', 'A/B Pitch -7/+7 st with other settings equal; multi-select, drag Pitch to displayed upper endpoint, inspect both single-clip values and then change common value; repeat lower endpoint on reset copy. Relative movement/clipping before endpoint U.'),
([180], 'timing-obligation', 'Clip Update Rate in Record/Warp/Launch settings quantizes changes to a running clip. Launch Mode/Warp Mode can be defaults for new clips. Complete affected-control set, rate choices and precedence versus global launch quantization are U.', 'A running, retain displayed Clip Update Rate then change Start/Loop Length/Gain at off-grid times; repeat with another displayed rate and stopped transport. Inspect settings, but do not transfer launch-grid arithmetic or infer immediate update.'),
([28,29,30,31], 'positive', 'Save Default Clip button is audio-specific and supports multi-selected samples; its ASD/new-import/nonretroactive semantics are owned by REQ-MEDIA-FILE-010, distinct from Live Clip devices.', 'A/B audio selection inspect enabled Save Default Clip route, then M inspect absence; apply only on test-owned media under media-file owner cases. Do not duplicate default fieldset or serialize ASD here.')]
for row in rows:add(*row)

unknowns=[
('REGION', 'Required region/loop input bounds and error outcomes remain unknown.', [
('BOUNDARY','boundary','A: Start=End, End before Start, loop zero/negative length, loop beyond source, then one sample and one grid tick inside/outside source end in disposable copies.','Minimum length, allowed out-of-source regions, clamp/reject/rounding and visible error are U.'),
('MALFORMED','malformed','A: enter abc, NaN and infinity text in Start/End/Loop fields, then attempt open of disposable saved clip state with an invalid region value.','Parser, refusal/normalization, prior-state preservation and error UI are U.')]),
('TIMING', 'Required ordering between edits, scrub, launch and transport remains unknown.', [
('TIMING','timing','A running at 120 BPM: at same captured request beat issue Set Start, Set Loop Length, scrub and launch; repeat reversed action order, with global quantization None/1 Bar and recorded Update Rate.','Same-time precedence, rounding ties, timeline/selection ownership and dispatch frame are U.'),
('TRANSPORT','transport','A playing run-in loop; stop, seek behind Start, restart and change global tempo 120 to 90 with audio Warp off/on separately.','Clock reset, looping/scrub latches, tails and instant marker-update semantics are U.')]),
('UNDO', 'Required edit/processed-file undo/redo transactions remain unknown.', [
('UNDO','undo-redo','Rename A, move Start, replace source then Reverse; request Undo for each and Redo, inspect clip settings/references/files and other shared-source clips.','History grouping, processed-file retention, external-edit undo and restoration are U.'),
('AUTOMATION','automation','A: attempt recorded automation/clip envelope or MIDI mapping for Gain/Pitch/Loop Start, apply manual edit and re-enable automated ownership.','Supported controls, automation/modulation/manual precedence, smoothing and transaction visibility are U.')]),
('PERSIST', 'Required save/reopen/default/processed-file state remains unknown.', [
('PERSISTENCE','persistence','A cropped/reversed and B sharing original, multi-selection layout vertical; save/reopen, reload Default Clip, collect media, relocate original sources in a disposable copy.','Actual fieldset, default precedence, reference identity and layout/history scope are U.'),
('SOURCE-LOSS','source-loss','A active playback, remove or rename its test-owned source and separately make Temporary/Project folders unwritable before Reverse/Crop; invoke Manage Sample File afterward.','Cached playback, retry/refusal/relink/rollback, partial file and original preservation outcomes are U.')]),
('CANCEL', 'Required cancellation/progress/error outcomes remain unknown.', [
('CANCEL','cancellation','A long Reverse/Crop begins with recorded progress; attempt available Cancel/Escape or dismiss source replacement/dialog before commitment, in separate trials.','Cancel availability, cutoff progress boundary, rollback, dirty flag and partial-file cleanup are U.'),
('ERROR','error','A external editor absent or fails, source decoding invalid, destination disk full or locked; attempt Edit/replace/Reverse/Crop on separate disposable copies.','Messages, fallback/recovery, clip/source/result ownership and previous-state preservation are U.')]),
('TEARDOWN', 'Required clip/view/Set teardown and concurrent-selection outcomes remain unknown.', [
('TEARDOWN','teardown','A processing Reverse/Crop while B plays: delete A, close Clip View, close Set and quit application in separate trials; retain pending/source/processed-file states.','Worker cancellation, pending output, resources, other-clip audio and recovery remain U.'),
('SELECTION-RACE','selection','A source replace preview or region drag active; select B in other window, change multi-selection, then complete gesture.','Which clip owns in-flight edit, UI focus, preview cancellation and stale-target safety remain U.')]),
('AUDIO', 'Required numerical audio and media-boundary oracles remain unknown.', [
('AUDIO','signal-obligation','A with nonzero source edges and audible output: Gain 0/-6 dB, Pitch 0/+12, Hi-Q off/on at distinct source/host rates, Fade off/on in Session.','Gain mapping, interpolation, alias/fade kernels, dither and numerical tolerance are U; no-effects need positive baseline.'),
('RATE','sample-rate','A fixed region/loop, host 44.1/48/96 kHz and 64/256 frames; repeated scrub/reverse/crop under retained source rates; change rate while stopped/playing if supported.','Rate-change support, endpoint/frame rounding, block invariance and performance deadlines remain U.')]),
('MULTI', 'Required multi-selection/common-value/context outcomes remain unknown.', [
('MULTI','boundary','Select zero, one, two shared-source audio clips with conflicting defaults, A+M, and mixed Session/Arrangement clips where UI permits; rename/color/gain/default-save.','Full eligibility matrix, duplicate source writes/conflict order, limits and cross-view selection support are U.'),
('PROGRAM','midi-output','M selectors dash/first/last with declared supporting target, launch, relaunch and scrub with pending bank/program plus note on.','MIDI value numbering/bytes/order, selector independence/dash suppression scope, plugins versus external targets, chase/relaunch and malformed saved selections are U.')])]
for group,contract,entries in unknowns:
    rid=f'REQ-CLIP-VIEW-U-{group}'
    REQ.append({'id':rid,'provenance':'U','target_applicability':'U','contract':contract,'source_blocks':[]})
    for suffix,kind,action,missing in entries:
        CASES.append({'id':f'CV-U-{suffix}','requirements':[rid],'kind':kind,'fixture':'fixtures.json#CV-BASE','setup_and_action':action,'documentary_expected':None,'documentary_comparator':None,'expected':None,'comparison':None,'target_grade':'U','executed':False,'unknown':missing,'source_blocks':[]})
write('requirements.json',REQ)
write('cases.json',CASES)
write('fixtures.json',{'id':'CV-BASE','status':'future-owned-input-recipe-not-reference-fixtures','preconditions':['Editable test-owned Set; no modal dialog/rename entry except explicitly under test; declared Win/macOS platform; original Linux UI support not inferred.','Retain before testing: source bytes/hash/length/rate/depth/channels, sample reference, Clip Start/End/Loop, Warp/markers/mode, tempo/meter, launch quantization, Clip Update Rate, groove/scale, gain/pitch/Hi-Q/Fade, clip active state, output routes/mutes, track/device state and settings/focus.','Future sample A: independently validated owned asymmetric eight-bar audio, 48 kHz 24-bit mono with distinct attacks/sustain and nonzero edges. B: shorter owned audio,44.1 kHz16-bit stereo; C: independently equal-length alternate of A with distinct content. Files are not supplied or claimed executed.','M: editable MIDI clip with two distinct notes and known instrument for audible controls only. MIDI edits/expression/computation remain under their canonical owners.','Audible tests require valid source/held note where applicable, clip/track/master active unmuted, monitoring/routing enabled and nonzero gain. No-effect needs paired active positive baseline and deliberately changed tested control only.','Reset test-owned copies between trials. All actual time/file/PCM/MIDI outputs and target comparisons remain U; expected:null is never a pass.'],'original_execution':False,'candidate_comparison':False})
routing={}
used={r for q in REQ for r in q['source_blocks']}
for loc,b in BLOCKS.items():
    n=int(loc.split('B')[1])
    if loc in used:owner='clip-view-workflows.md (bounded clauses only)'
    elif n==9:owner='session-view-workflows.md'
    elif 61<=n<=64:owner='groove-workflows.md'
    elif 115<=n<=128 or 133<=n<=136 or n in [158,170]:owner='midi-editing-tools.md (source context requires reconciliation; no new law here)'
    elif n in [72,73,74,75]:owner='clip-launch.md plus pending full Session/follow-action packet'
    else:owner='context/heading or neighboring owner; no coverage completion claim'
    routing[loc]={'owner':owner,'section':b['heading_context'][-1]['section'],'html_line':b['html_line']}
write('source-routing.json',routing)
assert len(REQ)==54 and len(CASES)==62
assert len({r['id'] for r in REQ})==len(REQ) and len({c['id'] for c in CASES})==len(CASES)
assert {r['id'] for r in REQ}=={r for c in CASES for r in c['requirements']}

link='../../analysis/ableton-live-12.4.3/full-spec-v1/clip-view/'
spec='''---
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

[Finite input recipe](REPLACE_LINKfixtures.json) requires future independently
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
'''.replace('REPLACE_LINK',link)
for r in REQ:
    if r['provenance']=='D12':spec+=f'| {r["id"]} | {r["contract"]} | '+', '.join('`'+b+'`' for b in r['source_blocks'])+' |\n'
spec+='''
## Unknown lifecycle, boundaries and errors

| U requirement | Required outcomes | Case suffixes |
| --- | --- | --- |
'''
for group,contract,entries in unknowns:
    spec+=f'| REQ-CLIP-VIEW-U-{group} | {contract} | '+', '.join('`CV-U-'+e[0]+'`' for e in entries)+' |\n'
spec+='''
All malformed/source-loss/disk/external-edit/close tests operate on disposable
owned media and Set copies. Cancellation availability, unsupported action/refusal,
undo grouping, processed-file persistence, shared-reference side effects and
concurrent selection are explicit unknowns. Synchronous menu descriptions do not
make error, cancel or teardown obligations inapplicable. Runtime cases compare
no application until an independent source/oracle exists.

## Acceptance catalog and timing limits

The [requirement view](REPLACE_LINKrequirements.json) and
[62 finite cases](REPLACE_LINKcases.json) contain 46 D12 cases and 16 U cases.
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
Version12, captured 2026-10-19. [Source metadata](REPLACE_LINKsource.json) retains
UTC/URL/length and SHA-256
`30f156e6d83c8f4caf3fe9dcf55bb2b764dc42ed8cbd3847863a53747851bd80`.
[HTML](REPLACE_LINKmanual-clip-view-2026-10-19.html) is immutable source;
[180 paragraph/heading blocks](REPLACE_LINKmanual-blocks.json) retain exact HTML
lines and full numbered heading context. [Text](REPLACE_LINKmanual-text.txt)
is navigation only. CV:B001-B180 covers chapter8 through §8.14, excluding sidebar
TOC/footer. [Source routing](REPLACE_LINKsource-routing.json) distinguishes this
owner from neighboring content and context; it is not a complete coverage ledger.

[Author manifest](REPLACE_LINKmanifest-author-r1.json) freezes payloads, both
canonical snapshots and the inventory TOC pin. [Author validation](REPLACE_LINKvalidation-author-r1.json)
reports focused identity/catalog/link/whitespace checks only. These analysis
links require sanitization and separate review before handoff.

## Revision and handoff

Revision1 is a frozen partial author draft awaiting independent semantic review.
No existing release is expanded or changed; no handoff is published here.
'''.replace('REPLACE_LINK',link)
(ROOT/'wiki/specs/clip-view-workflows.md').write_text(spec)
research='''---
id: RES-CLIP-VIEW-WORKFLOWS
type: research
status: current
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3
---

# Shared Clip View and audio property evidence

## Scope and source selection

This partial F-04 analyst packet routes shared Clip View UI and unowned audio
properties to [the canonical draft](../specs/clip-view-workflows.md).
[Full coverage design](full-live-specification-design.md) governs closure.
The [inventory TOC](../../analysis/ableton-live-12.4.3/full-spec-v1/inventory/manual-toc.json)
selects the exact official `/en/live-manual/12/clip-view/` chapter URL; no prior
Clip View HTML capture was found in the active packets. The chapter was retained
once; no original program, external editor, hardware or candidate was run.

[Source metadata](REPLACE_LINKsource.json) identifies official Version12 HTML,
capture UTC and URLs,306606 bytes, SHA-256
`30f156e6d83c8f4caf3fe9dcf55bb2b764dc42ed8cbd3847863a53747851bd80`.
No patch-level publication revision is available: all exact12.4.3 runtime
applicability remains U. The [180 block view](REPLACE_LINKmanual-blocks.json)
retains paragraph text, source HTML lines and full numbered heading context.
The extractor stops at sidebar navigation, so unrelated TOC entries are not
miscounted as chapter behavior. HTML bytes are preserved; normalized text and
JSON are analyst navigation artifacts. Figures were not inspected separately.

## Canonical ownership and source interpretation

The canonical spec owns46 D12 requirements and8 required-U obligations, with62
finite unexecuted cases. Documentary visible-state proposals have explicit
comparators; timing/signal obligations and every exact-target oracle remain null.
No media fixture/reference render was fabricated. Future owned A/B/C media and
MIDI M must be retained independently before any action can be evaluated.

Shared clip selection, fields/panels, regions, looping/scrub gestures, multiclip
properties and audio-specific source actions are distinct from MIDI note/MPE
editing or global note/time serialization. The
[source-routing view](REPLACE_LINKsource-routing.json) routes the chapter's
neighboring MIDI tools, groove and launch prose to their existing owners, not
to duplicated requirements. [MIDI editing](midi-editing-tools.md),
[MPE](mpe-tuning-grooves.md), [media](media-file-workflows.md) and
[clip launch](clip-launch.md) retain narrower evidence. Detailed Warp processing
and full Session/Follow Actions still require separate packets.

Specific predicates preserved in the draft/cases include audio Warp as Loop
eligibility; Session-only Fade toggle versus Arrangement envelopes; independent
clip/project meter; source-relative marker/region reversal versus unchanged
clip envelope time; equal-length source replacement/edit marker retention;
Temporary versus saved Project paths for new Crop/Reverse media; separate launch
quantization and Clip Update Rate; and mixed-value endpoint unification. These
are documentary relationships, not observed control law or DSP equivalence.

New source context requiring later reconciliation belongs to the MIDI owner:
CV:B126 §8.5.2 half-grid Humanize prose versus existing quarter-grid per direction
may concern total width versus one-sided displacement. CV:B122 Interval Size and
Add Interval button versus immediate-slider prose may depend on the gesture.
CV-U-MIDI-UTILITIES keeps both contexts open rather than declaring contradiction
or copying either as a new normative law. The source HTML at respective lines
720 and708 supplies exact current capture locators.

Clip meter display-only `CV:B059-B060` does not invalidate a distinct stored
follow-time normalization using clip meter in the launch owner. Scrub and Set
button prose does not establish that launch-grid rounding code runs for those
gestures. Hi-Q19-semitone/CPU claims are qualitative/conditional, not measurable
bounds. Fade0-4ms is documentary only; exact kernel stays with existing audio
owners and remains unproven outside their finite released scope.

## Remaining required evidence

Exact-build version parity, source/frame/time codecs, reverse/crop marker
arithmetic, scrub/region/update scheduling, gain/pitch/interpolation/fade audio,
program-message numbering/order, full shared-source/default/multi-selection
matrix, undo/persistence/cancel/malformed/error/teardown/resource behavior,
platform focus/accessibility and complete settings precedence remain U.
No absent original/candidate evidence is labelled pass or inapplicable.

## Freeze and review

[Manifest](REPLACE_LINKmanifest-author-r1.json) freezes exact payloads/canonical
snapshots plus the inventory TOC source. Run
`python3 analysis/ableton-live-12.4.3/full-spec-v1/clip-view/validate.py` for focused
hash, source locator, case, local link, metadata and untracked-aware whitespace
checks. [Validation](REPLACE_LINKvalidation-author-r1.json) does not establish
behavior. Root alone owns shared catalogs, coverage, questions, plan and log.
Separate semantic review is pending; no handoff or implementation scope is changed.
'''.replace('REPLACE_LINK',link)
(ROOT/'wiki/research/clip-view-workflows.md').write_text(research)
write('counts.json',{'requirements':len(REQ),'provenance':dict(Counter(r['provenance'] for r in REQ)),'cases':len(CASES),'case_kinds':dict(Counter(c['kind'] for c in CASES)),'target_graded':0})
print((P/'counts.json').read_text())
