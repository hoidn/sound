"""Analyst documentary mapping only; never imports or invokes a Live API."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import re

P = Path(__file__).resolve().parent
ROOT = P.parents[3]
ORIGIN = P.parent / 'max-api'
assert not (P / 'manifest-author-r1.json').exists(), 'Sealed payloads are immutable'


def load(p):
    return json.loads(p.read_text())


def dump(name, data):
    (P / name).write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')


def pin(path):
    raw = path.read_bytes()
    return dict(path=str(path.relative_to(ROOT)), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())


names = ['Application', 'Application.View', 'Song', 'Song.View', 'Track', 'Track.View', 'Scene', 'ClipSlot', 'CuePoint', 'TakeLane']
entries = {e['name']: e for e in load(ORIGIN / 'lom-entries.json')}
members = load(ORIGIN / 'lom-members.json')
all_blocks = load(ORIGIN / 'reference-blocks.json')
all_sources = {s['id']: s for s in load(ORIGIN / 'all-sources-r1.json')}
selected = [entries[n] for n in names]
sources = [dict(all_sources[e['source_id']], retained_path='../max-api/' + all_sources[e['source_id']]['file']) for e in selected]
blocks = {e['source_id']: all_blocks[e['source_id']] for e in selected}
dump('sources.json', sources)
dump('source-blocks.json', blocks)
(P / 'source-blocks.txt').write_text(''.join(f"{sid}:{r['block']} HTML:{r['html_line']}:{r['html_column']} {r['tag']} {r['text']}".rstrip() + '\n' for sid, rows in blocks.items() for r in rows))
dump('inventory-pins.json', [pin(ORIGIN / n) for n in ['manifest-inventory-r1.json', 'all-sources-r1.json', 'reference-blocks.json', 'lom-entries.json', 'lom-members.json', 'derive_inventory.py', 'source-page-r1.md']])
owners = ['live-api-bridge-workflows', 'live-set-structure', 'transport-state', 'playback-core', 'clip-launch', 'session-view-workflows', 'session-launch-workflows', 'recording-comping', 'routing-monitoring-latency', 'application-workspace', 'keyboard-navigation', 'device-racks', 'automation-envelopes', 'automation-workflows', 'project-media-workflows', 'mix-graph', 'mixer-values', 'arrangement-editing', 'tuning-systems', 'groove-workflows', 'browser-workflows', 'bundled-device-hosting', 'push-controller-workflows']
dump('owner-pins.json', [pin(ROOT / f'wiki/specs/{n}.md') for n in owners] + [pin(ROOT / 'tools/spec_browser.py')])

# Exact parameter names/order. A null type means the reference does not annotate it.
# No parameter list in a paragraph is NOT treated as a declaration of no arguments.
params = {
    'Application.press_current_dialog_button': [('index', None, None)],
    'Application.View.focus_view': [('view_name', None, None)],
    'Application.View.hide_view': [('view_name', None, None)],
    'Application.View.is_view_visible': [('view_name', None, None)],
    'Application.View.show_view': [('view_name', None, None)],
    'Application.View.scroll_view': [('direction', 'int', None), ('view_name', None, None), ('modifier_pressed', 'bool', None)],
    'Application.View.zoom_view': [('direction', 'int', None), ('view_name', None, None), ('modifier_pressed', 'bool', None)],
    'Song.capture_midi': [('destination', 'int', None)],
    'Song.get_current_smpte_song_time': [('format', 'int', None)],
    'Song.find_device_position': [('device', 'live object', None), ('target', 'live object', None), ('target position', 'int', None)],
    'Song.move_device': [('device', 'live object', None), ('target', 'live object', None), ('target position', 'int', None)],
    'Song.jump_by': [('beats', 'float', None)],
    'Song.scrub_by': [('beats', 'float', None)],
    'Song.stop_all_clips': [('quantized', None, True)],
    'Song.trigger_session_record': [('record_length', None, True)],
    'Song.View.select_device': [('id NN', None, None)],
    'Track.create_audio_clip': [('file_path', 'symbol', None), ('position', 'float', None)],
    'Track.create_midi_clip': [('start_time', 'float', None), ('length', 'float', None)],
    'Track.delete_clip': [('clip', None, None)],
    'Track.duplicate_clip_to_arrangement': [('clip', None, None), ('destination_time', 'float', None)],
    'Track.insert_device': [('device_name', 'symbol', None), ('target_index', 'int', True)],
    'Track.jump_in_running_session_clip': [('beats', 'float', None)],
    'Scene.fire': [('force_legato', 'bool', True), ('can_select_scene_on_launch', 'bool', True)],
    'Scene.fire_as_selected': [('force_legato', 'bool', True)],
    'Scene.set_fire_button_state': [('state', 'bool', None)],
    'ClipSlot.create_audio_clip': [('path', None, None)],
    'ClipSlot.create_clip': [('length', None, None)],
    'ClipSlot.duplicate_clip_to': [('target_clip_slot', 'ClipSlot', None)],
    'ClipSlot.fire': [('record_length', None, True), ('launch_quantization', None, True)],
    'ClipSlot.set_fire_button_state': [('state', 'bool', None)],
    'TakeLane.create_audio_clip': [('file_path', 'symbol', None), ('start_time', 'float', None)],
    'TakeLane.create_midi_clip': [('start_time', 'float', None), ('length', 'float', None)],
}
for name in ['create_audio_track', 'create_midi_track', 'create_scene', 'delete_scene', 'delete_track', 'delete_return_track', 'duplicate_scene', 'duplicate_track']:
    params['Song.' + name] = [('index', None, None)]
for name in ['delete_device', 'duplicate_clip_slot']:
    params['Track.' + name] = [('index', None, None)]
returns = {
    'Application.View.available_main_views': 'list of symbols',
    'Application.View.is_view_visible': 'bool',
    'Song.find_device_position': 'int', 'Song.move_device': 'int',
    'Song.get_beats_loop_length': 'symbol', 'Song.get_beats_loop_start': 'symbol',
    'Song.get_current_beats_song_time': 'symbol', 'Song.is_cue_point_selected': 'bool',
    'Track.View.select_instrument': 'bool',
}
defaults = {'Song.stop_all_clips': {'quantized': '1'}, 'Scene.fire': {'force_legato': '0', 'can_select_scene_on_launch': '1'}, 'Scene.fire_as_selected': {'force_legato': '0'}}

# Finite actions for every function, written as future observations, never API code.
actions = {
    'Application.get_bugfix_version': 'Retain independently identified host build, request its bugfix component once and retain the raw result; the 9.1.2 example is not an expected installed build.',
    'Application.get_major_version': 'Retain independently identified host build, request its major component once and retain raw output without requiring the example value 9.',
    'Application.get_minor_version': 'Retain independently identified host build, request its minor component once and retain raw output without requiring the example value 1.',
    'Application.get_version_string': 'Retain independently identified host build, request the version string once and retain text without deriving formatting for an actual build from the 9.1.2 example.',
    'Application.get_document': 'With one independently identified owned current Set, request the document and retain actual identity; separately change to another owned Set only in the source-loss case.',
    'Application.press_current_dialog_button': 'Use an independently available harmless owned-context dialog with separately identified button indices and cancel route; choose one admitted index once and retain UI state. Do not use installation, authorization, deletion or update dialogs.',
    'Application.View.available_main_views': 'Request available view names once in an initialized view context and retain the actual list without using source list order as a message oracle.',
    'Application.View.focus_view': 'Use independently offered Browser then Detail/Clip names on separate reset copies; request focus for each. Separately test the source-described empty-name context only after actual accepted spelling is known.',
    'Application.View.hide_view': 'Positively show an independently hideable named view, then request hiding that same view. Empty-name quoting remains a separate source-context U probe.',
    'Application.View.show_view': 'Choose an independently offered hidden named view, request show_view with that name, and retain visible/focus state. The paragraph gives a parameter only; its effect is not expanded from the function name.',
    'Application.View.is_view_visible': 'Independently show and hide one offered view on reset copies and query that name in both states; retain raw result with no boolean/message oracle.',
    'Application.View.scroll_view': 'With valid Arranger selection and independently accepted direction/modifier inputs, compare source directions left/right with modifier off/on in four reset trials. Add one eligible Browser trial; no pixel/beat displacement oracle.',
    'Application.View.zoom_view': 'Use an eligible visible Arrangement with highlighted track; compare horizontal and vertical direction/modifier pairs on reset copies. Separately use an eligible Session view; Arranger versus Arrangement accepted-name question remains U.',
    'Application.View.toggle_browse': 'Independently select a device with available Hot-Swap context, request toggle_browse once then again, and retain device-chain/browser/Hot-Swap state after each.',
    'Song.capture_and_insert_scene': 'Use two playing nonempty Session clips and a distinct selected scene; request capture once on an owned copy and inspect the scene list and content, without ID/order timing comparator.',
    'Song.capture_midi': 'First establish can_capture_midi and recently played audible MIDI. Compare explicit destination 1 versus 2 on reset Sets, then omitted/auto context only if accepted; retain focused-window/view and created material without buffer/note algorithm oracle.',
    'Song.continue_playing': 'Establish a nonzero current playback position on an active audible owned Set, stop, request continue_playing once and retain position/play state without timing oracle.',
    'Song.create_audio_track': 'Use a known editable Set with independently counted tracks; compare insertion at source-described 0, current count, and -1 in separate copies. Retain track order/type with no native index codec assumption.',
    'Song.create_midi_track': 'Use a known editable Set with independently counted tracks; compare insertion at 0, current count, and -1 in separate copies. Retain track order/type without requiring a constructor default.',
    'Song.create_return_track': 'Retain current return list on an editable owned Set, request one new return, then inspect membership and position without deriving send topology/defaults.',
    'Song.create_scene': 'Compare insertion at 0, current scene count and -1 on reset owned Sets; retain actual returned object and list, with no numeric ID equality oracle.',
    'Song.delete_scene': 'On a disposable copy with distinguishable scenes, independently identify an admitted nonempty scene index, request its deletion once and inspect neighboring scene/slot state.',
    'Song.delete_track': 'Use an extra owned ordinary track with a known admitted index, request deletion once on a copy, and inspect lists/routes; never target the only ordinary track or Main as an assumed positive case.',
    'Song.delete_return_track': 'Use one extra distinguishable owned return with a known admitted index; request deletion once and retain actual track/send state without rollback assumptions.',
    'Song.duplicate_scene': 'Use a distinguishable owned nonempty scene and known admitted index, request duplication once, inspect content/list and reset history before other actions.',
    'Song.duplicate_track': 'Use a distinguishable owned track with a clip/device and known admitted index; request duplication once and inspect actual content/routes without full clone-equivalence oracle.',
    'Song.find_device_position': 'Use a separately movable owned device, valid target chain, and admitted target position; request candidate insertion position, then inspect whether the source/target remain unchanged without prescribing a numeric result.',
    'Song.move_device': 'Use a separately movable owned native device and eligible target chain with independently admitted position; request one move, retain returned position and both chains. Nearest-placement boundary is separate and ungraded.',
    'Song.force_link_beat_time': 'Only with an independently available enabled Link setup and productive positive transport baseline, request forcing Link beat time once; record actual timing with no phase, network or timing oracle.',
    'Song.get_beats_loop_length': 'Establish a known valid Arrangement loop, request its beat-form length once, retain returned text with no tick-resolution/serialization oracle.',
    'Song.get_beats_loop_start': 'Establish a known valid nonzero Arrangement loop start, request beat-form start once and retain text without a format arithmetic oracle.',
    'Song.get_current_beats_song_time': 'Establish explicit stopped then running Arrangement positions on reset trials; request beat-form current time in each, retaining raw output without clock comparator.',
    'Song.get_current_smpte_song_time': 'Use a known Arrangement position; request each source-listed format 0 through 5 in separate trials. Record strings without frame-rate rounding/drop-frame algorithms.',
    'Song.is_cue_point_selected': 'Create/identify an owned locator and independently position playback at it, query selection; compare a distinct nonlocator position on a reset copy without a float equality oracle.',
    'Song.jump_by': 'With explicit current position and eligible active audible playback, request a separately admitted positive one-beat relative jump, then compare a separately admitted negative one-beat jump on a reset copy.',
    'Song.scrub_by': 'With explicit current Arrangement position and eligible playback, request separately admitted positive and negative one-beat scrub amounts on reset copies; do not infer future identity with jump_by from at-the-moment prose.',
    'Song.jump_to_next_cue': 'Use distinguishable locators on both sides of current playback and a positive can_jump_to_next_cue state; request next once, then retain new state.',
    'Song.jump_to_prev_cue': 'Use distinguishable locators on both sides and a positive can_jump_to_prev_cue state; request previous once and retain position/state.',
    'Song.play_selection': 'Use a nonempty Arrangement time selection over active nonmuted material and request play_selection once. The no-selection branch has a separate negative probe.',
    'Song.re_enable_automation': 'Use running Session clips with independently productive nonzero automation and an established override/Re-Enable indication; request re-enable once and retain indicated/value/output state without envelope or signal oracle.',
    'Song.redo': 'On an owned copy, undo one independently undoable name edit, establish can_redo, request redo once and inspect history/name without transaction grouping law.',
    'Song.undo': 'On an owned copy make one independently undoable name edit, establish can_undo, request undo once and inspect history/name without universal API undoability law.',
    'Song.set_or_delete_cue': 'At an independently identified nonlocator Arrangement position request the toggle once, then once again on that context; retain actual locator list without boundary snapping oracle.',
    'Song.start_playing': 'Use a known insert marker over active audible material, explicit stopped transport and separately valid output; request start once and retain state without sample-accurate position oracle.',
    'Song.stop_playing': 'Establish active nonzero playback and request stop once, retain actual transport/output state without release/tail deadline.',
    'Song.stop_all_clips': 'Use playing nonempty clips on two tracks with nonzero output; compare omitted quantized and explicit 0 on reset copies. Timing and source default token acceptance remain ungraded.',
    'Song.tap_tempo': 'With Tap available and tempo context explicit, make two independently accepted requests with retained external event times; keep any tempo estimate ungraded and do not derive a fitting/filter law.',
    'Song.trigger_session_record': 'Use a selected empty eligible slot, armed owned track, active nonzero source and explicit monitor/transport; request with independently admitted record_length in beats, then request while recording on a separate eligible trial. Retain transition/material without duration oracle.',
    'Song.View.select_device': 'Resolve an owned device ID in a selected track and request selection; compare the same request with its track not selected on a reset copy. Retain selected/appointed/track-visible state separately.',
    'Track.create_audio_clip': 'Use editable nonfrozen audio track not recording and an independently supported readable owned audio file; request creation at admitted position 4 beats, retaining file reference and Arrangement clip.',
    'Track.create_midi_clip': 'Use editable nonfrozen MIDI track not recording; request a clip at admitted start_time 4 and length 4 beats, retaining Arrangement content without note/default laws.',
    'Track.create_take_lane': 'Use an independently eligible owned track with explicit lane context; request one take lane and inspect membership, without assuming eligibility of all track types.',
    'Track.delete_clip': 'Identify an owned existing clip belonging to an eligible track, request deletion once on a disposable Set and inspect source container and history.',
    'Track.delete_device': 'Use a separately deletable extra owned native device at an admitted index; request deletion once and retain chain/output on a copy.',
    'Track.duplicate_clip_slot': 'Use a known nonempty owned Session slot at an admitted index, request duplication and inspect actual source/destination slots without inferring destination from a name alone.',
    'Track.duplicate_clip_to_arrangement': 'Use an owned Session clip then an Arrangement clip on reset copies, request duplication at independently admitted destination_time 8 beats and inspect material/position.',
    'Track.insert_device': 'Use an actually available eligible native device UI name and legal chain position; compare omitted target_index with one admitted explicit index. Max/plug-in and illegal ordering are separate negative probes.',
    'Track.jump_in_running_session_clip': 'Establish an actually running nonempty Session clip and nonzero output; request admitted one-beat relative move once and retain position/output without loop/wrap/scheduling law.',
    'Track.stop_all_clips': 'Use playing and separately fired clips in the owned track with positive nonzero baseline; request stop once and retain playing/fired/output state without timing oracle.',
    'Track.View.select_instrument': 'Use an eligible track with an instrument and a separate reset copy with an independently selectable first device but no instrument; request selection and retain result/focus without type coercion law.',
    'Scene.fire': 'Use a nonempty scene with active eligible output; compare explicit force_legato 0/1 and can_select_scene_on_launch 0/1 on four reset copies, with source-record preference and arm/empty-group state explicit.',
    'Scene.fire_as_selected': 'With a distinct selected scene and a different resolved receiver scene, request fire_as_selected with force_legato 0 then 1 on reset copies. Retain selected/next/playing state; final-scene boundary separate.',
    'Scene.set_fire_button_state': 'Use a nonempty playable scene and explicit global/scene enable context, request state 1 then 0 after a productive launch baseline; retain event/state history without press-duration law.',
    'ClipSlot.create_audio_clip': 'Use an eligible nonfrozen audio track slot and supported readable owned audio path; request creation once. Occupied-slot behavior is not presumed by this positive setup.',
    'ClipSlot.create_clip': 'Use an empty slot on an eligible editable MIDI track and request admitted length 4 beats; inspect created clip without default-note/loop laws.',
    'ClipSlot.delete_clip': 'Use a known owned occupied slot and request deletion once on a disposable copy; retain slot/content and undo state.',
    'ClipSlot.duplicate_clip_to': 'Use distinguishable owned source/target slots; compare an empty target and an occupied target on reset copies and retain actual destination/content without ID clone equivalence.',
    'ClipSlot.fire': 'Compare occupied playable slot, empty armed MIDI slot and a valid armed/empty grouped context with Start Recording on Scene Launch ON, using separate copies and explicit admitted optional values. Retain play/record/stop state without quantization law.',
    'ClipSlot.set_fire_button_state': 'Use playable nonempty slot with explicit launch mode/global-enable context and positive output; request state 1 then 0 and retain state without resolving launch mode press/release timing.',
    'ClipSlot.stop': 'Use two slots in one owned track and a valid group copy with active nonzero playback; request stop from a different slot than the playing one and retain stopped/recording state without timing law.',
    'CuePoint.jump': 'Use an owned locator at an admitted distinct position and compare stopped versus playing transport with nonzero audible source; request jump and retain current position without a quantized-time oracle.',
    'TakeLane.create_audio_clip': 'Use a take lane on eligible nonfrozen audio track not recording and a readable owned supported audio file; request start_time 4 beats, retaining lane and Arrangement placement. OS path syntax needs its actual platform.',
    'TakeLane.create_midi_clip': 'Use a take lane on eligible nonfrozen MIDI track not recording; request start_time 4 and length 4 beats, retaining actual lane content without hidden length validation law.',
}

fixtures = {
    'common': 'Future prerequisites only: independently valid owned patch/device, actually available accepted Live/Max/API context, initialization and positively resolved same-context object/path/ID. Record host/Max/build/platform, object kind, list membership, selection/focus, actual supported member, arm/monitor/record/transport, preference and freeze state. No patch, API program, ALS, native host or actual output is supplied.',
    'active-positive-guard': 'Before negative/no-effect probes require independently valid owned patch, available initialized Live/Max/API context, eligible existing object/member and matched positive baseline from the same member. For signal/record/launch/meter cases require active nonempty source/clip, explicit playing or eligible recording, independently productive automation if relevant, correct routing/monitor/arm, nonzero gain/send/wet/amount and nonmuted output. Missing gates cannot prove no-effect and remain U.',
    'values': 'Use two independently admitted distinguishable values A/B: bool 0/1 only where the source declares that type; name symbols api-owned-A/api-owned-B; lists/children only independently valid same-context objects; dictionary routing only the exact independently returned available dictionary entries, retaining display_name and identifier separately. Numeric trials must satisfy the member-specific source range/context; 4/8 beats and 120/121 BPM are analyst choices, never defaults or outcome laws. No generic float, enum, id, string/symbol/unicode codec or dictionary coercion is inferred.',
    'observation': 'Use an independently accepted UI change and separately admitted observed property; first retain successful explicit read and productive change. Capture raw messages before and after one change, without assuming initial notification, count, ordering, cadence, subscriptions or event grammar.',
    'destructive-isolation': 'All create/delete/move/overwrite/record/save proposals concern disposable owned copies with independently known cancel/restore routes, never actual user assets, device installation, accounts or license state.',
    'not-provided': 'No API calls, script/example/patch execution, Live/Max/hardware, original/native code, installation, fake host or independent candidate. Every action is a future analyst observation proposal and all actual outputs remain U.',
}
dump('fixtures.json', fixtures)
requirements, cases, ledger = [], [], []


def add_case(r, suffix, kind, action, claim=None):
    cases.append(dict(id='LCS-' + suffix, requirements=[r['id']], member=r.get('member'), kind=kind,
                      preconditions=['common', 'active-positive-guard', 'values', 'destructive-isolation'],
                      setup_and_action=action, source_blocks=r['source_blocks'], source_claim=claim,
                      documentary_expected=None, documentary_comparator=None,
                      expected=None, comparison=None, target_grade='U', executed=False))


for e in selected:
    rows = blocks[e['source_id']]
    class_members = [m for m in members if m['reference_entry'] == e['id']]
    assert [m['id'] for m in class_members] == e['declared_members']
    for m in class_members:
        start = next(i for i, b in enumerate(rows) if b['block'] == m['block'])
        end = next((i for i in range(start + 1, len(rows)) if rows[i]['tag'] in ('h2', 'h3')), len(rows))
        section = rows[start:end]
        desc = [b for b in section[1:] if not b['text'].startswith('Access:') and b['text']]
        access_rows = [b for b in section[1:] if b['text'].startswith('Access:')]
        access = [v for v in ['get', 'set', 'observe'] if any(v in b['text'] for b in access_rows)]
        typ = m['heading'][len(m['anchor']):].strip() or None
        key = e['name'] + '.' + m['anchor']
        is_func = m['category'] == 'functions'
        arguments = None if key not in params else [dict(name=n, type=t, optional=o, source_default=defaults.get(key, {}).get(n)) for n, t, o in params[key]]
        body = ' '.join(b['text'] for b in desc)
        return_text = body.split('Returns:', 1)[1] if 'Returns:' in body else None
        signature = dict(value_type=typ, access=access if not is_func else None,
                         arguments=arguments, result_type=returns.get(key) if is_func else typ,
                         return_source_text=return_text,
                         type_system='Publisher vocabulary only; no wire/native/Python coercion inferred')
        unknown = ['target-12.4.3-applicability', 'runtime-message-representation', 'lifecycle-and-error-closure']
        if not desc: unknown.append('no-member-description-beyond-heading-access')
        if is_func and arguments is None: unknown.append('argument-list-not-stated-not-proved-empty')
        if is_func and signature['result_type'] is None: unknown.append('result-type-not-stated-not-proved-void')
        if key == 'Application.View.show_view': unknown.append('effect-not-described-beyond-parameter')
        if arguments and any(a['type'] is None for a in arguments): unknown.append('some-argument-types-not-stated')
        if arguments and any(a['optional'] is None for a in arguments): unknown.append('some-argument-optionality-not-stated')
        scope = 'call' if is_func else '/'.join(access)
        contract = f"For the documented {e['name']} context, `{m['anchor']}` is a direct {m['category']} declaration" + (f" with source type `{typ}`" if typ else '') + f" and documented {scope} role. "
        contract += ('Publisher member description: ' + body if body else 'No additional member-specific behavior is stated beyond its heading and access declaration.')
        contract += ' The exact typed/access/argument/result fields and explicit omissions are recorded in the member ledger; this documentary role supplies no target runtime oracle.'
        n = len(requirements) + 1
        r = dict(id=f'REQ-LAPI-CORE-{n:03d}', title=key, section=e['name'], member=m['id'], category=m['category'], provenance='D-current-public', target_applicability='U', contract=contract,
                 signature=signature, class_context=dict(description=rows[1]['text'], canonical_path=rows[3]['text'], source_blocks=[e['source_id'] + ':' + rows[i]['block'] for i in [1, 3]]),
                 source_blocks=[e['source_id'] + ':' + b['block'] for b in [rows[1], rows[3]] + section],
                 source_member_url=m['url'], unknown_fields=unknown)
        requirements.append(r)
        if is_func:
            assert key in actions, key
            action = actions[key]
        else:
            action = f"Resolve eligible `{key}` in the source-specific class/track/window context and record actual source type and access. "
            action += 'Explicitly read once in independently established state A. ' if 'get' in access else ''
            action += f"On a reset copy, assign independently admitted distinct state B for `{m['anchor']}` and explicitly inspect readback/selection; object targets must be same-context eligible identities. " if 'set' in access else ''
            action += f"On another reset copy, establish productive observation for `{m['anchor']}`, make one independently accepted state change A to B and retain raw notifications separately from explicit reads. " if 'observe' in access else ''
            action += 'Apply every restriction, unit, availability and sentinel context in the exact member description, with active-positive-guard for launch/record/automation/meter/audio contexts; unsupported contexts remain U.'
        add_case(r, f'{n:03d}', 'member-positive', action, contract)
        ledger.append(dict(inventory_member=m, requirement=r['id'], cases=[cases[-1]['id']], mapping='documentary-direct-member-mapped', signature=signature, class_context=r['class_context'],
                           description_blocks=[e['source_id'] + ':' + b['block'] for b in desc], unknown_fields=unknown, target_applicability='U', complete=False))

assert len(requirements) == 226 and len(actions) == 73

# These cover real source branches; numerical/error output remains ungraded.
probes = [
    ('Application', 'control_surfaces', 'negative', 'Compare an independently active connected supported control surface slot with None/inactive slot on reset preferences; absent hardware stays U, not a simulated controller or universal empty-list law.'),
    ('Application', 'current_dialog_message', 'boundary', 'Compare a harmless actual dialog with an independently confirmed no-dialog state; retain message text without locale or empty-token codec oracle.'),
    ('Application.View', 'scroll_view', 'boundary', 'After productive eligible scrolling, try one independently identified unscrollable view/direction on a separate copy; capture behavior without inferring rejection or no-effect from omission.'),
    ('Application.View', 'zoom_view', 'source-context', 'Compare independently admitted Arranger and Arrangement spelling contexts and source-described empty view name, preserving exact input/output; no normalization or alias equivalence expected.'),
    ('Song', 'create_scene', 'boundary', 'After valid insertion baseline test index one below -1 and one beyond independently known scene count on separate copies; retain actual errors/list state without invented clamping or rollback law.'),
    ('Song', 'play_selection', 'negative', 'After productive selected-region playback baseline, clear only the Arrangement selection and repeat; retain state/output with no signal or timing no-effect oracle.'),
    ('Song', 'jump_to_next_cue', 'boundary', 'After productive next-locator baseline use last-locator and no-locator copies with can_jump state retained; record actual state without assuming boundary wrap or silence.'),
    ('Song', 'capture_midi', 'negative', 'After can_capture_midi positive audible-source baseline, use a separately confirmed no-eligible-material context. Retain eligibility/result without inferring private capture buffer size or failures.'),
    ('Song.View', 'mod_mapping_device', 'source-context', 'Only with independently supported Push 3 context compare an assigned eligible device, same-device parameter choice and device removal; without that hardware/feature mark U, never borrow Push 1/2 or generic API support.'),
    ('Song.View', 'select_device', 'boundary', 'Compare selected versus unselected owning-track contexts after productive device selection; appointed-device and auto-track-visibility are distinct retained observations.'),
    ('Track', 'create_audio_clip', 'negative', 'After valid audio-track creation baseline compare non-audio track, frozen audio track and recording audio track on separate owned copies; retain print/error/result without exact exception/rollback law.'),
    ('Track', 'create_midi_clip', 'boundary', 'After valid MIDI creation baseline compare start_time 0 and source upper endpoint 1576800, then a separately invalid outside position; retain outputs without treating the source numeric range as a target oracle.'),
    ('Track', 'insert_device', 'negative', 'After legal native-device insertion baseline compare an independently available MIDI effect after an instrument and an independently available Max/plug-in device name on separate owned copies. Missing installed content remains U.'),
    ('Track', 'input_routing_type', 'boundary', 'After an accepted available dictionary choice/readback, compare another independently returned choice then an owned unlisted identifier on separate copies; do not infer labels-as-identifiers, coercion or route error grammar.'),
    ('Track.View', 'select_instrument', 'negative', 'After productive instrument/first-device selection baseline use an eligible empty device-chain copy and retain result/focus without assuming boolean transport encoding.'),
    ('Scene', 'fire_as_selected', 'boundary', 'After a productive selected-scene baseline compare final-scene and empty-scene contexts with next-scene availability retained; no implied wrap, creation or stop law.'),
    ('Scene', 'tempo', 'boundary', 'Compare an eligible scene with tempo enabled and disabled while song tempo differs; retain API value and playback context without using -1 as a persisted tempo or scheduler rule.'),
    ('ClipSlot', 'playing_status', 'source-context', 'Compare ordinary empty slot, group with all tracks empty/stopped, group playing only, and group with recording under explicit prerequisites. Preserve overlapping source wording for states 1/2 without resolving precedence.'),
    ('ClipSlot', 'create_clip', 'boundary', 'After empty MIDI slot length 4 baseline compare length 0, negative length, occupied slot and non-MIDI slot on separate copies; capture errors/content with no invented exception or partial-write law.'),
    ('TakeLane', 'create_audio_clip', 'source-context', 'After valid lane creation baseline retain exact actual platform path, lane membership and track membership; compare frozen and recording track contexts. Do not generalize the source Mac /Volumes example as all-platform required syntax.'),
]
for cls, anchor, kind, action in probes:
    r = next(r for r in requirements if r['title'] == cls + '.' + anchor)
    add_case(r, f'BRANCH-{len(cases) - 225:03d}', kind, action, r['contract'])
    next(m for m in ledger if m['requirement'] == r['id'])['cases'].append(cases[-1]['id'])

unknowns = [
    ('TYPES', 'Missing argument/result and value grammar', 'Unannotated function argument/result types, omitted parameter lists, optionality, empty/symbol/unicode/list/object/dictionary representations, error channels and enum conversion are unknown. Omitted return prose does not imply void.', 'malformed', 'After an accepted member-specific typed baseline, vary one wrong scalar/list/object/dictionary shape and one missing/extra argument on reset copies; retain raw responses and state without assuming rejection, conversion or atomicity.'),
    ('CONTEXT', 'Unresolved source context and alias predicates', 'Arranger/Arrangement and empty view-name spelling, ClipSlot group status overlap, Track MIDI-to-Session cross-reference wording and thin member descriptions remain unresolved; no naming inference fills missing effects.', 'source-context', 'Use only actually available view/group/track contexts and retain paired productive baselines while changing the one source-context predicate; capture admitted spellings and raw outcomes without alias or enum equivalence.'),
    ('TARGET', 'Exact build and cross-owner reconciliation', 'The public index declares 12.4.5. Exact 12.4.3 access, types, ranges, defaults, optionality, membership and outcomes remain unknown even for features described since 12.3 or 11.0. No existing finite native or stored law is overwritten.', 'version', 'Retain separately identified source-version and actual supported target contexts with one independently readable member of each of the ten classes; absent member or build stays U without fallback or inferred parity.'),
    ('LIFECYCLE', 'Persistence and transaction boundaries', 'Member-specific save/reopen, undo grouping, redo, cancellation, failure, source loss, Set replacement, IDs and teardown behavior are not fully specified by these declarations or generic bridge prose.', 'persistence', 'On a disposable owned Set make one independently successful API-mediated name/selection edit, save through an independently valid generic owner workflow and reopen; re-resolve identity and retain state without persistence or ID oracle.'),
    ('TIME', 'Timing signal and observation limits', 'Scheduling, quantization interaction, clock units/conversion, rates, automation precedence, notification count/order, meter smoothing/hold, audible continuity and real-time capacity have no new calibrated target oracle.', 'timing', 'With explicit active nonzero audible clip and independent positive meter/transport baseline, issue one supported state/position request and retain raw event/audio/clock observations without numerical, latency, continuity or rate comparator.'),
    ('INHERITANCE', 'Unmapped and inherited API surface', 'Only the 226 explicit direct members in these ten references are mapped here. Other 35 references/362 direct declarations, inherited members, roots/aliases and arbitrary bridge/protocol/Max compatibility remain outside this partial mapping and unresolved.', 'boundary', 'Compare an independently declared direct member with a separately independently documented inherited/root context only if that evidence exists; never use this inventory as a negative capability or complete runtime reflection oracle.'),
    ('HARDWARE', 'Controller and synchronization availability', 'ControlSurface entries, Push-specific implicit arm/modulation mapping, Link/Tap/network and physical-port observations require independently supported actual hardware/firmware/context; no surrogate establishes support.', 'negative', 'Retain productive actual supported hardware/Link context before one controlled disconnect/disable trial. If no supported context exists, leave the entire observation U rather than fake the device or port.'),
    ('ERRORS', 'Creation deletion movement and availability gaps', 'Track/list endpoints, frozen/recording and media eligibility, deletion of absent objects, unsupported insertion, selection loss and partial failures require more context-specific evidence. Prints versus throws and unspecified errors are not one error protocol.', 'recovery', 'After valid owned create/move/delete baselines, remove only an owned prerequisite on a separate copy, attempt one action and use an independently accepted recovery path; capture resulting lists/media/history without cleanup or rollback guarantee.'),
]
for code, title, contract, kind, action in unknowns:
    r = dict(id='REQ-LAPI-CORE-U-' + code, title=title, section='Required unknowns', provenance='U', target_applicability='U', contract=contract, source_blocks=[])
    requirements.append(r)
    add_case(r, 'U-' + code, kind, action)
for suffix, kind, action, code in [
    ('UNDO', 'undo', 'Perform one successful owned track/scene name edit with can_undo established; request undo then separately available redo and inspect history/state. Do not infer grouping of create/delete/move or all API changes.', 'LIFECYCLE'),
    ('CANCEL', 'cancel', 'Use an independently cancelable harmless owned view/dialog/file-selection workflow after a positive confirmed baseline; cancel once and inspect actual object/selection/history without no-write or rollback guarantee.', 'LIFECYCLE'),
    ('SOURCE-LOSS', 'source-loss', 'After productive supported owned audio-creation baseline, make only that owned audio source unavailable on a copy and repeat or reopen through an accepted route; capture media/object/errors, no silence or transaction oracle.', 'ERRORS'),
    ('TEARDOWN', 'teardown', 'After productive read/observe/call baseline close only the owned Set/device through an independently valid UI route, then release observer/binding in the supported context; retain messages and state without callbacks-after-close or resource-cleanup law.', 'LIFECYCLE'),
    ('AUTOMATION', 'automation', 'Use independently productive nonzero tempo/parameter automation and an active supported writable API member; compare automation active, overridden and explicitly re-enabled contexts on reset copies with actual nonmuted output. No numeric evaluator or precedence law.', 'TIME'),
    ('RATE', 'sample-rate', 'Only with actually supported configured rates and positive nonzero playback/meter baseline compare two independently accepted rates on reset contexts; retain API/output observations without rate invariance or hold-time tolerance.', 'TIME'),
    ('TRANSPORT', 'transport', 'After productive eligible clip/scene/take recording baseline compare stopped, playing and explicitly armed recording contexts in separate copies; record launch/selection/history without scheduler or implicit arm assumptions.', 'TIME'),
    ('CONCURRENCY', 'concurrency', 'After a stable eligible list and positive bound-object read, reorder or remove one owned list element through an accepted action between two observations; retain object/path/results without atomic-snapshot or notification-order law.', 'LIFECYCLE'),
]:
    r = next(r for r in requirements if r['id'] == 'REQ-LAPI-CORE-U-' + code)
    add_case(r, 'U-' + suffix, kind, action)

for r in requirements:
    r['cases'] = [c['id'] for c in cases if r['id'] in c['requirements']]
denominator = dict(global_reference_entries=45, global_direct_members=588, selected_reference_entries=10, selected_direct_members=226,
                   mapped_direct_members=len(ledger), selected_unmapped_direct_members=0, outside_family_direct_members=362, outside_family_reference_entries=35,
                   complete_members=0, complete_entries=0, target_applicable_members=0,
                   selected_categories=dict(Counter(m['inventory_member']['category'] for m in ledger)),
                   classes=[dict(name=e['name'], inventory_entry=e['id'], direct_members=len(e['declared_members']), mapped=len(e['declared_members']), unmapped=0, unknown_members=len(e['declared_members']), complete=False) for e in selected],
                   semantics='Mapped means a source-backed declaration contract and finite proposal, not complete behavior, executable fixture, inherited closure or target applicability. Every member retains explicit unknown flags; other-family declarations remain unmapped by this owner.')
dump('member-ledger.json', ledger)
dump('denominator.json', denominator)
dump('requirements.json', requirements)
dump('cases.json', cases)
counts = dict(requirements=len(requirements), requirement_grades=dict(Counter(r['provenance'] for r in requirements)), cases=len(cases), case_kinds=dict(Counter(c['kind'] for c in cases)), documentary_oracles=0, null_documentary_oracles=len(cases), target_oracles=0, sources=10, source_blocks=sum(map(len, blocks.values())), mapped_direct_members=226, unmapped_family_direct_members=0, unknown_members=226, complete_members=0)
dump('counts.json', counts)

prefix = '../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-core-session/'
meta = lambda kind: f'''---
id: {'SPEC' if kind == 'spec' else 'RESEARCH'}-LIVE-API-CORE-SESSION
type: {kind}
status: draft
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3; public LOM index 12.4.5 applicability U
---

'''
spec = meta('spec') + '''# Public Live API core and Session direct members

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

Use the [future prerequisites](''' + prefix + '''fixtures.json): an independently
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

The [denominator ledger](''' + prefix + '''denominator.json) preserves the global
45 references/588 explicit direct declarations. This family maps **226 direct
members in ten references: 30 children, 123 properties and 73 functions**.
All226 have member-specific requirements, exact source blocks, typed signatures
where stated, unknown flags and finite cases. Zero selected declarations are
unmapped; **all226 remain incomplete/target-U**. Other35references/362direct
members remain outside this family's mapping; inherited members/root aliases
are an additional unclosed denominator, not silently counted as absent.

The [member ledger](''' + prefix + '''member-ledger.json) records the exact source
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

'''
for name in names + ['Required unknowns']:
    spec += f'## {name}\n\n'
    for r in requirements:
        if r['section'] != name: continue
        spec += f"### {r['id']} — {r['title']}\n\n**{r['provenance']}/target-U.** {r['contract']}\n\n"
        if 'signature' in r:
            s = r['signature']
            spec += f"Source fields: value type `{s['value_type'] or 'unstated'}`; access `{','.join(s['access']) if s['access'] is not None else 'function-call role'}`; result type `{s['result_type'] or 'unstated'}`. "
            if s['arguments'] is None: spec += 'Arguments: unstated; no empty-signature inference.\n\n'
            else: spec += 'Arguments, in source order: ' + '; '.join(f"`{a['name']}` ({a['type'] or 'type unstated'}, optionality {'optional' if a['optional'] is True else 'unstated'}" + (f", source default {a['source_default']}" if a['source_default'] is not None else '') + ')' for a in s['arguments']) + '.\n\n'
        if r['source_blocks']:
            spec += 'Evidence: [' + r['source_blocks'][0].split(':')[0] + ' member blocks](' + prefix + 'source-blocks.json); exact keys `' + '`, `'.join(r['source_blocks']) + '`; [typed ledger](' + prefix + 'member-ledger.json).\n\n'
        spec += 'Finite cases: `' + '`, `'.join(r['cases']) + '` in the [case catalog](' + prefix + 'cases.json).\n\n'
spec += '''## Finite cases and evidence limits

The [case catalog](''' + prefix + '''cases.json) has ''' + str(len(cases)) + ''' finite future proposals.
Each direct declaration has its own positive case; get/set/observe clauses are
separate stated steps within that case, requiring independent admitted states
and productive observation. Twenty additional per-member probes cover selected
negative/boundary/source contexts. Sixteen U cases retain types, version,
inheritance, hardware, recovery, persistence, undo/redo, cancel, source loss,
automation, rate, transport, concurrency and teardown. This is not all branch
combinations or all per-member lifecycle coverage. Full argument/error/return
grammar and every required unknown need further evidence before closure.

The [sources](''' + prefix + '''sources.json), [counts](''' + prefix + '''counts.json),
[input pins](''' + prefix + '''inventory-pins.json), [owner pins](''' + prefix + '''owner-pins.json)
and [author seal](''' + prefix + '''manifest-author-r1.json) preserve immutable
R1 evidence and canonical snapshots. The local validator is read-only after
freeze; hash/parser checks prove identity and mapping, not runtime behavior.
Root integrates catalogs and independent review. No handoff is released here.
'''
(ROOT / 'wiki/specs/live-api-core-session.md').write_text(spec)
(P / 'spec-r1.md').write_text(spec)

research = meta('research') + '''# Public LOM core and Session member mapping

## Evidence and method

The [canonical draft](../specs/live-api-core-session.md) maps 226 direct
declarations, not complete classes. Reused unchanged immutable [R1 inventory
manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/max-api/manifest-inventory-r1.json)
SHA67e24da58fb1d91d8c55659c65eb0779a3c3e8cc2424ddcf07915032d8637a73.
No recapture or mutable source-family canonical pin. All65 R1 payload hashes
are checked. Ten exact class sources retain original URL, UTC, bytes and SHA
in [sources](''' + prefix + '''sources.json); HTML remains at its immutable
original location. The source index says Live12.4.5, not target12.4.3. Source
paragraphs/headers/access declarations were read as data. No scripts/examples,
API/Max/native/original/candidate, hardware or patch were executed.

All ''' + str(sum(map(len, blocks.values()))) + ''' retained class blocks are
present in [source blocks](''' + prefix + '''source-blocks.json) and text with
HTML line/column locations. The original pinned article-only extractor checks
these against exact HTML bytes; sidebar/reference links do not add declarations.
Member spans start at the exact h3 and stop before the next h2/h3. Class context
is retained through B0002 and canonical path B0004. Type/access comes from the heading/access
paragraph; manual argument names/order/type and explicit result annotations
come from each actual member description. Unannotated signatures stay null;
the original function paragraph is preserved so the ledger is auditable.
Copied publisher prose supplies source_claim, never a numerical/API oracle.

## Denominator and remaining work

Global inventory45entries/588direct declarations remains unchanged. Selected
ten entries226members are mapped to226D-current-public clauses and finite
member cases; 8U requirements retain cross-cutting gaps. Remaining outside
family35entries/362members are unmapped here. Every226member has explicit U
flags and complete:false; target-applicable/complete member and class counts
are zero. Inherited/root/alias members are not flattened or assumed absent.
Full per-member branches/errors/argument/result grammars and lifecycle remain
required; mapping every source heading does not complete behavior.

## Source context questions

| Local question | Exact source context | Retained unknown |
| --- | --- | --- |
| Q-LCS-001 | Application.View B0014, B0022, B0028 | available_main_views/scroll use Arranger but zoom uses Arrangement. Empty view-name typography also differs. No alias/empty quoting normalization. |
| Q-LCS-002 | ClipSlot B0030/B0033/B0039 | is_playing/recording predicates and status2 description overlaps status1 by saying playing or recording. Preserve wording; no numeric status precedence inferred. |
| Q-LCS-003 | Track B0148; ClipSlot B0044/B0046 | MIDI-create paragraph refers to ClipSlot.create_clip for audio in Session. Preserve apparent cross-reference wording issue; do not adopt MIDI function as audio creator. |
| Q-LCS-004 | Track B0016; Song B0018; bridge owner | devices includes mixer prose and master_track API name cannot overwrite installed device topology or Main storage/native names; aliases and reflection closure U. |
| Q-LCS-005 | Song.View B0014/B0015/B0018; Track B0078 | Push3-only modulation context and Push implicit arm are not generic or Push1/2 capability. Actual firmware/hardware and API target availability U. |
| Q-LCS-006 | Track B0096/B0160; Song B0024 | future fix language, insert_device since12.3 and groove since11 do not establish exact12.4.3 semantics; chronology/current-source conflict U. |
| Q-LCS-007 | Track B0146/B0148; TakeLane B0015/B0017; ClipSlot B0045 | Prints versus throws, audio path/platform wording, insertion into take-lane versus Arrangement, range/length/error distinctions remain context-specific; no universal exception or rollback protocol. |
| Q-LCS-008 | Application.View B0024; unannotated function headings/access-only members | show_view only lists view_name. Missing behavior/type/optionality/return prose remains missing, not filled from names or memory. |
| Q-LCS-009 | Song B0055/B0103/B0133/B0167/B0170; Scene B0026–B0038; Track meter blocks | Source numeric enums/ranges/sentinels/meter words do not overwrite finite stored/native values or supply wire/message/signal/timing comparators. |

## Review and freeze

[Requirements](''' + prefix + '''requirements.json), [cases](''' + prefix + '''cases.json),
[typed member ledger](''' + prefix + '''member-ledger.json), [denominator](''' + prefix + '''denominator.json),
[future prerequisites](''' + prefix + '''fixtures.json) and [counts](''' + prefix + '''counts.json)
are sealed with both canonical snapshots. Twenty-three canonical owner pins
plus browser-parser pin keep ownership visible; seven immutable inventory pins
avoid mutable source-family revision changes. The validator checks all65original
R1 payloads, ten source/block identities, member spans/signatures/IDs, exact
browser requirement equality, links, whitespace and snapshots without writes.
Independent review pending; no semantic/runtime or complete-API approval.
'''
(ROOT / 'wiki/research/live-api-core-session.md').write_text(research)
(P / 'research-r1.md').write_text(research)
print(json.dumps(counts, indent=2))
