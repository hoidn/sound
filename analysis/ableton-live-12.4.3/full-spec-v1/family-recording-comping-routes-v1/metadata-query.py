"""Fixed retained-index DATA query; no bodies, traversal or source mutations.

Default prints census only. --rows emits bounded selected data after all caps.
"""
import collections
import hashlib
import json
import pathlib
import re
import sys

P = pathlib.Path(__file__).resolve().parent
F = P.parent
C = F / 'component-resolution-v1'
NAMES = '''ORecorder TSessionOverdubber OMidiRecorder OMidiSequencerStartRecordingEvent
OAudioRecorder OAudioRecorderEvent ASessionRecordingLogic ARecorder ARecorderModule
LRecorderModule ARecordingGestures ATakeLane ATakeLanes AAudioRecorder LAudioRecorder
AAudioRecorderModule AMidiRecorder LMidiRecorder AMidiRecorderModule ANoteRecorder
AArrangerTakeLaneClipsLayerView ARecordingViewLayer APunchInLayer ATakeLaneController
ATakeLaneHeader ATakeLaneView TMustMergeOnRecordingStop AProtocolRecordingClipDeck
TProtocolRecordingRecBehaviorFactory TSlotRecordingRecBehaviorFactory
TNotPossibleWhileRecordingException TFileEmptyOrRecordingException'''.split()
EXCLUDED = ['AEventRecorder', 'AArrangementAutomationRecorder', 'AAutomationRecorder',
            'AFakeArrangementAutomationRecorder', 'ASongTempoArrangementAutomationRecorder',
            'ATimeSignatureArrangementAutomationRecorder',
            'ARecordingOrOfflineClipTimelineEditor', 'SkRecorder']


def scan(path, kind, select, project=None):
    out = []
    offset = 0
    with path.open('rb') as f:
        for line, raw in enumerate(f, 1):
            d = json.loads(raw)
            if select(d):
                out.append({'kind': kind, 'provider': str(path), 'source_line': line,
                            'source_byte': offset, 'raw_bytes': len(raw),
                            'raw_sha256': hashlib.sha256(raw).hexdigest(),
                            'record': project(d) if project else d})
            offset += len(raw)
    return out


def main():
    encodings = {str(len(n)) + n for n in NAMES}

    def table_projection(d):
        p = dict(d)
        p['exported_prefix_slot_count'] = len(d['slots'])
        p['selected_slot_policy'] = ('large-table-header/store + leading3 construction/lifetime prefix only'
                                     if len(d['slots']) > 16 else 'complete retained small exported prefix')
        p['slots'] = d['slots'][:3] if len(d['slots']) > 16 else d['slots']
        p['not_complete_render_callback_or_native_extent'] = True
        return p

    tables = scan(C / 'class-tables.jsonl', 'table-data',
                  lambda d: d['literal_type_encoding'] in encodings and d['offset_to_top'] == 0,
                  table_projection)
    points = {x['record']['address_point'] for x in tables}
    rtti = scan(C / 'class-rtti.jsonl', 'RTTI-data', lambda d: d['literal_type_encoding'] in encodings)
    stores = scan(C / 'class-stores.jsonl', 'store-data', lambda d: d['address_point'] in points)
    rx = re.compile(r'(?<![A-Za-z0-9_])(?:' + '|'.join(map(re.escape, NAMES)) + r')(?![A-Za-z0-9_])')
    owners = scan(C / 'symbol-owners.jsonl', 'lexical-owner-data',
                  lambda d: bool(rx.search(d.get('lexical_owner') or '')) and
                  not (d.get('lexical_owner') or '').startswith(('boost::', 'std::', 'flip::')))
    scopes = {x['record']['scope_id'] for x in owners}
    members = scan(C / 'symbol-memberships.jsonl', 'membership-data',
                   lambda d: any(c[1] in scopes for c in d.get('candidates', [])))
    entries = {x['record']['entry'] for x in members}
    indexes = pathlib.Path('/var/tmp/sound-analysis/corpus/indexes')
    aliases = scan(indexes / 'aliases.jsonl', 'alias-data', lambda d: d['entry'] in entries)
    # Fixed selected aliases only, both directions. Prefix/store targets are
    # unexpanded construction/lifetime frontiers, never arbitrary callee seeds.
    calls = scan(indexes / 'calls.jsonl', 'call-data',
                 lambda d: d['caller'] in entries or d.get('callee') in entries or d.get('to') in entries)
    indirect = scan(indexes / 'indirect.jsonl', 'indirect-data',
                    lambda d: d.get('function') in entries or d.get('caller') in entries)
    counts = {'tables': len(tables), 'selected_slots': sum(len(x['record']['slots']) for x in tables),
              'full_exported_slots_metadata_only': sum(x['record']['exported_prefix_slot_count'] for x in tables),
              'large_table_headers_prefix3': sum(x['record']['exported_prefix_slot_count'] > 16 for x in tables),
              'RTTI_rows': len(rtti), 'store_rows': len(stores), 'owner_rows': len(owners),
              'alias_rows': len(aliases), 'membership_rows': len(members),
              'aliases_plus_memberships': len(aliases) + len(members),
              'call_rows': len(calls), 'indirect_rows': len(indirect),
              'calls_plus_indirect': len(calls) + len(indirect)}
    within = (len(tables) <= 32 and counts['selected_slots'] <= 512 and len(stores) <= 128 and
              counts['aliases_plus_memberships'] <= 512 and counts['calls_plus_indirect'] <= 512)
    plan = {'schema': 'recording-comping-fixed-metadata-census-v1', 'exact_types': NAMES,
            'explicit_scope_exclusions': EXCLUDED,
            'preliminary_broad_query': {'table_candidates': 190, 'full_prefix_slots': 3281,
                                      'owner_rows': 82, 'overlapping_owner_function_memberships': 119,
                                      'retained': False},
            'simple_primary_discovery_before_owner_scope': {'tables': 40, 'policy_selected_slots': 215},
            'scope_authorization': 'Root approved exact32semantically bounded simple-primarytable scope with8explicit owner/unbound exclusions before selected row retention.',
            'caps': {'tables': 32, 'selected_slots': 512, 'stores': 128,
                     'aliases_plus_memberships': 512, 'calls_plus_indirect': 512},
            'counts': counts, 'within_caps': within,
            'table_summary': [{'type': x['record']['literal_type_encoding'],
                               'address_point': x['record']['address_point'],
                               'full_exported_prefix_slots': x['record']['exported_prefix_slot_count'],
                               'selected_slots': len(x['record']['slots']),
                               'original_line': x['source_line'], 'original_raw_sha256': x['raw_sha256']}
                              for x in tables],
            'alias_entries': sorted(entries, key=lambda v: int(v, 16)),
            'data_only': True, 'new_bodies_selected': 0, 'new_traversal': False,
            'materialized_at_census': False}
    if sys.argv[1:] == ['--rows']:
        if not within:
            raise SystemExit('CAP EXCESS; no rows emitted; report complete census')
        for row in owners + members + aliases + rtti + tables + stores + calls + indirect:
            print(json.dumps(row, separators=(',', ':')))
    elif not sys.argv[1:]:
        print(json.dumps(plan, indent=2))
    else:
        raise SystemExit('unsupported arguments')


if __name__ == '__main__':
    main()
