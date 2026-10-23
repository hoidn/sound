"""Read-only metadata census; no C body output/retention/semantic reading.

Fixed event wrappers plus already associated event-prefix targets, not callees.
"""
import collections
import hashlib
import json
import pathlib
import re

P = pathlib.Path(__file__).resolve().parent
R = P.parents[3]
F = P.parent
M = F / 'family-native-midi-effects-routes-v1'
I = F / 'depth-native-midi-effects-initialization-v1'
names = ['OMidi' + s + 'Processor' for s in (
    'Arpeggiator', 'CcControl', 'Chord', 'NoteLength', 'Pitcher',
    'Random', 'Scale', 'Velocity')]
event_names = {'OnMidiEvent', 'OnMidi'}
roles = collections.defaultdict(list)
mapdata = [json.loads(l) for l in (M / 'native-data.jsonl').read_text().splitlines()]
for number, row in enumerate(mapdata, 1):
    d = row['record']
    if row['kind'] == 'selected-alias-data':
        for name in names:
            if any(name + '::' + method + '>' in d['name'] for method in event_names):
                roles[d.get('thunk_target') or d['entry']].append({
                    'kind': 'class-qualified-event-wrapper', 'processor': name,
                    'native_map_line': number, 'alias_entry': d['entry'],
                    'alias_name': d['name'], 'known_thunk_target': d.get('thunk_target')})
    if row['kind'] == 'table-prefix-data' and len(d['slots']) == 8:
        # These exact five prefixes/offsets have prior selected source context.
        # No new slot/global data or target lookup is performed.
        for slot in d['slots']:
            if slot['offset'] in (24, 32, 48):
                roles[slot['target']].append({
                    'kind': 'existing-class-associated-event-prefix-target',
                    'processor_encoding': d['literal_type_encoding'],
                    'address_point': d['address_point'], 'slot_offset': slot['offset'],
                    'native_map_line': number,
                    'qualification': 'Already read conditional event-like source in approved initialization; physical prefix alone supplies no method name or public receiver proof.'})
assert len(roles) == 17
aliases = pathlib.Path('/var/tmp/sound-analysis/corpus/indexes/aliases.jsonl')
entryloc = {}
ordinal = 0
offset = 0
class_aliases = []
for line, raw in enumerate(aliases.open('rb'), 1):
    # All rows are index metadata. No source C bodies are in this provider.
    d = json.loads(raw)
    if d['entry'] in roles:
        assert not d['external']
        entryloc[d['entry']] = (ordinal // 100, d, line, offset, len(raw), hashlib.sha256(raw).hexdigest())
    labels = set([d['name']] + [s['name'] for s in d.get('symbols', [])])
    matched = [(name, label) for name in names for label in labels
               if re.search(r'(?<![A-Za-z0-9_])' + name + r'(?=::|[>,(* ])', label)]
    if matched:
        class_aliases.append({'entry': d['entry'], 'labels': matched,
                              'source_line': line, 'source_byte': offset,
                              'raw_bytes': len(raw), 'raw_sha256': hashlib.sha256(raw).hexdigest()})
    if not d['external']:
        ordinal += 1
    offset += len(raw)
assert ordinal == 418417 and len(entryloc) == 17
cpins = json.loads((F / 'component-resolution-v1/class-inputs.json').read_text())['decomp_chunk_pins']
pinby = {p['path']: p for p in cpins}
chunks = collections.defaultdict(set)
for entry, v in entryloc.items():
    chunks[v[0]].add(entry)
old = {x['entry'] for x in json.loads((I / 'source-locators.json').read_text())['records']}
records = []
selected_pins = []
for chunk, selected in sorted(chunks.items()):
    path = pathlib.Path('/var/tmp/sound-analysis/corpus/decomp/chunks') / f'chunk-{chunk:05}.jsonl'
    data = path.read_bytes()
    pin = pinby[str(path)]
    assert len(data) == pin['bytes'] and hashlib.sha256(data).hexdigest() == pin['sha256']
    selected_pins.append(pin)
    byte = 0
    found = set()
    for line, raw in enumerate(data.splitlines(keepends=True), 1):
        m = re.search(br'"entry"\s*:\s*"([^\"]+)"', raw[:100])
        entry = m[1].decode() if m else ''
        if entry in selected:
            d = json.loads(raw)
            code = d.get('code') or ''
            _, alias, aline, abyte, alen, ahash = entryloc[entry]
            records.append({'entry': entry, 'roles': roles[entry],
                            'source_path': str(path), 'source_line': line,
                            'source_byte': byte, 'raw_bytes': len(raw),
                            'raw_sha256': hashlib.sha256(raw).hexdigest(),
                            'C_utf8_bytes': len(code.encode()), 'C_lines': len(code.splitlines()),
                            'C_sha256': hashlib.sha256(code.encode()).hexdigest(),
                            'native_body_bytes': d['body_bytes'], 'native_body_ranges': d['body_ranges'],
                            'record_thunk': d['thunk'], 'state': d['state'],
                            'warnings': d['warnings'], 'error': d['error'],
                            'timed_out': d['timed_out'], 'partial_code': d['partial_code'],
                            'alias_name': alias['name'], 'alias_thunk': alias['thunk'],
                            'alias_thunk_target': alias.get('thunk_target'),
                            'alias_source_line': aline, 'alias_source_byte': abyte,
                            'alias_raw_bytes': alen, 'alias_raw_sha256': ahash,
                            'already_retained_and_read_in_initialization': entry in old})
            found.add(entry)
        byte += len(raw)
    assert selected == found
records.sort(key=lambda d: int(d['entry'], 16))
summary = {'unique_selected_entries': len(records),
           'new_entries_not_in_initialization': sum(not r['already_retained_and_read_in_initialization'] for r in records),
           'inherited_entries': sum(r['already_retained_and_read_in_initialization'] for r in records),
           'native_extent_bytes': sum(r['native_body_bytes'] for r in records),
           'total_C_utf8_bytes': sum(r['C_utf8_bytes'] for r in records),
           'total_C_lines': sum(r['C_lines'] for r in records),
           'max_C_lines': max(r['C_lines'] for r in records),
           'record_thunks': sum(bool(r['record_thunk']) for r in records),
           'warning_records': sum(bool(r['warnings']) for r in records),
           'selected_chunks': len(selected_pins)}
summary['within_caps'] = (len(records) <= 64 and summary['total_C_utf8_bytes'] <= 196608
                          and summary['max_C_lines'] <= 1500)
print(json.dumps({'schema': 'native-midi-processing-metadata-census-v1',
                  'caps': {'records': 64, 'C_utf8_bytes': 196608, 'C_lines_per_record': 1500},
                  'selection': 'All exact class-qualified OnMidi/OnMidiEvent wrapper aliases in approved family metadata plus every existing +24/+32/+48 event-associated target of the five eight-slot prefixes, as conditionally read in approved initialization. No callee chaining, new slot/global or creation/lifecycle round.',
                  'summary': summary, 'records': records,
                  'approved_C1_chunk_pins': selected_pins,
                  'class_alias_metadata_census': class_aliases,
                  'missing_named_handler_qualification': 'No explicit main/event-named processor alias for Chord/Pitch/Random/Scale/Velocity in this exact-token query; their existing prefix/source associations are candidates, not method names. This bounded lexical result is not native absence.',
                  'new_C_materialized': False, 'new_C_bodies_semantically_read': False,
                  'research_appended': False, 'approval_required_before_new_C': True}, indent=2))
