#!/usr/bin/env python3
"""Validate only staged owner data and an approved review summary; never actual payloads."""
import argparse, copy, hashlib, json, pathlib, re
P = pathlib.Path(__file__).resolve().parent
ROOT = P.parents[3]
ALLOWED = {ROOT / 'wiki/specs/device-analog.md',
           ROOT / 'analysis/ableton-live-12.4.3/full-spec-v1/reviews/analog-velocity-bytes-v1-review.json',
           ROOT / 'analysis/ableton-live-12.4.3/full-spec-v1/owner-analog-r3-finite-v1/case-aliases.json',
           ROOT / 'handoff/device-analog-v1/manifest.json'}

def need(value, message):
    if not value:
        raise ValueError(message)

def read(path):
    path = pathlib.Path(path).resolve()
    need(path.parent == P or path in ALLOWED, 'refuse outside staged/explicit approved data: ' + str(path))
    return path.read_bytes()

def load(name):
    return json.loads(read(P / name))

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def signature(text):
    return {'bytes': len(text.encode()), 'sha256': sha(text.encode())}

def verify(pin):
    raw = read(ROOT / pin['path'])
    need(len(raw) == pin['bytes'] and sha(raw) == pin['sha256'], 'identity ' + pin['path'])
    return raw

def bodies(text):
    return {m[1]: m[0] for m in re.finditer(r'^### (REQ-DEVICE-ANALOG-\d{3})[^\n]*\n.*?(?=^### REQ-|^## |\Z)', text, re.M | re.S)}

def sections(text):
    return {m[1]: m[0] for m in re.finditer(r'^## ([^\n]+)\n.*?(?=^## |\Z)', text, re.M | re.S)}

def encoded(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode()

def compose(text, delta, reverse=False):
    items = list(reversed(delta['replacements'])) if reverse else delta['replacements']
    for replacement in items:
        before, after = (replacement['new'], replacement['old']) if reverse else (replacement['old'], replacement['new'])
        need(text.count(before) == 1, 'replacement not unique ' + replacement['label'])
        text = text.replace(before, after, 1)
    return text

def preservation(before, after, baseline):
    old, new = bodies(before), bodies(after)
    need(len(old) == len(new) == 23 and old.keys() == new.keys(), 'REQ set')
    need({k: signature(v) for k, v in old.items()} == baseline['requirement_bodies'], 'old body pins')
    for key in old:
        if key in baseline['preserve_prefix_and_only_append_to']:
            need(new[key].startswith(old[key]), 'old prefix lost ' + key)
        else:
            need(new[key] == old[key], 'other whole body changed ' + key)
    rows = lambda s: [line for line in s.splitlines() if line.startswith('| DAN-')]
    need(rows(before) == rows(after) == baseline['case_rows'] and len(rows(after)) == 67, 'old rows')
    for key, pin in baseline['protected_sections'].items():
        need(signature(sections(before)[key]) == signature(sections(after)[key]) == pin, 'protected section ' + key)

def expected_case(point, index, case_id):
    v = point['velocity_byte']; fresh = v != 100
    return {
      'catalog_velocity_byte': v, 'observation_id': point['id'], 'case_id': case_id,
      'existing_case_refs': [] if fresh else ['DAN-028', 'CONTROL-DAN028-P1'],
      'kind': 'finite-native-observation' if fresh else 'inherited-reference-only',
      'requirements': ['REQ-DEVICE-ANALOG-004', 'REQ-DEVICE-ANALOG-017'],
      'approved_review_pointer': f'#/approved_summary/approved_points/{index}',
      'input': {'shared_input_pointer': '#/shared_input', 'velocity_byte': v, 'script': point['input_script']},
      'native_expected': {'provenance': 'X: original x86_64 under recorded supplied-data harness context',
         'output': point['output'] if fresh else point['historical_output'],
         'descriptive_both_channel_metrics': point['observed_output'],
         'hash_matches_historical100': point['output_sha256_matches_inherited100'] if fresh else None,
         'raw_all_positive_zero': True if v == 0 else None},
      'original_waveform_prior': point['waveform_prediction'], 'portable_expected': None,
      'portable_comparator': None, 'candidate_grade': None,
      'fresh_pid': point['fresh_pid'], 'fresh_receipt': point['receipt'] if fresh else None,
      'fresh_utc': point['fresh_utc'],
      'historical_reference': None if fresh else {'review': point['historical_approved_review'],
         'pointer': point['historical_approved_review_point'], 'projection': point['historical_projection']},
      'limitation': 'Only the exact shared 203-value vector/history with all 8 AmpMod/AttackMod fields 0; hash identity to inherited metadata only, not an old-audio comparison, repeat-run law, portable metric, productive velocity curve, general zero-note semantics or public/ARM/calibration proof.'}

def check_catalog(catalog, joins, review):
    summary = review['approved_summary']; points = summary['approved_points']
    need(catalog['shared_input'] == summary['shared_input'], 'shared vector/history')
    need([x['velocity_byte'] for x in points] == list(range(128)), 'approved complete summary')
    need(len(catalog['catalog']) == len(joins['joins']) == 128, 'catalog universe')
    case_index = 76
    for index, point in enumerate(points):
        v = point['velocity_byte']; fresh = v != 100
        case_id = f'DAN-{case_index:03}' if fresh else None
        if fresh:
            case_index += 1
        need(catalog['catalog'][index] == expected_case(point, index, case_id), 'case mapping ' + str(v))
        expected_join = {'velocity_byte': v, 'case_id': case_id,
                         'approved_review_pointer': f'#/approved_summary/approved_points/{index}',
                         'provenance': point['provenance'], 'new_ID': fresh, 'original_calls': 1 if fresh else 0}
        need(joins['joins'][index] == expected_join, 'join ' + str(v))
    need(case_index == 203, 'ID end')
    need(catalog['logical_points'] == 128 and catalog['fresh_cases'] == 127 and catalog['inherited_references'] == 1, 'denominators')

def controls(catalog, joins, review, before, after, baseline):
    results = []
    def reject(name, callback):
        try:
            callback()
        except (ValueError, KeyError, IndexError):
            results.append(name)
        else:
            raise AssertionError('negative control accepted: ' + name)
    def changed(name, edit):
        x, y = copy.deepcopy(catalog), copy.deepcopy(joins)
        edit(x, y)
        reject(name, lambda: check_catalog(x, y, review))
    changed('omit selected byte', lambda x,y: x['catalog'].pop())
    changed('duplicate byte', lambda x,y: x['catalog'].__setitem__(1, copy.deepcopy(x['catalog'][0])))
    changed('wrong numeric velocity', lambda x,y: x['catalog'][2].__setitem__('catalog_velocity_byte', 128))
    changed('swap fresh IDs', lambda x,y: x['catalog'][1].__setitem__('case_id', 'DAN-078'))
    changed('inherit100 new ID', lambda x,y: x['catalog'][100].__setitem__('case_id', 'DAN-176'))
    changed('inherit100 invented fresh PID', lambda x,y: x['catalog'][100].__setitem__('fresh_pid', 1))
    changed('alter native output hash', lambda x,y: x['catalog'][0]['native_expected']['output'].__setitem__('sha256', '0'*64))
    changed('erase second channel metric', lambda x,y: x['catalog'][1]['native_expected']['descriptive_both_channel_metrics']['per_channel'].pop())
    changed('change shared203word', lambda x,y: x['shared_input']['parameter_f32_bits_le'].__setitem__(99, '00000000'))
    changed('invent portable comparator', lambda x,y: x['catalog'][1].__setitem__('portable_comparator', 'exact'))
    changed('rewrite original NULL prior', lambda x,y: x['catalog'][1].__setitem__('original_waveform_prior', 'retrospective'))
    changed('wrong receipt index', lambda x,y: x['catalog'][1]['fresh_receipt'].__setitem__('zero_based_record', 0))
    changed('wrong event frame', lambda x,y: x['shared_input']['history']['note_on'].__setitem__('frame', 4096))
    changed('invent candidate grade', lambda x,y: x['catalog'][1].__setitem__('candidate_grade', 'PASS'))
    changed('wrong approved summary pointer', lambda x,y: y['joins'][0].__setitem__('approved_review_pointer', '#/unapproved'))
    changed('invent inherited execution', lambda x,y: y['joins'][100].__setitem__('original_calls', 1))
    reject('change another whole REQ', lambda: preservation(before, after.replace('Live sends 203 host values.', 'Live sends 202 host values.', 1), baseline))
    reject('remove old004 prefix', lambda: preservation(before, after.replace('Release velocity has no effect.', 'Release velocity unknown.', 1), baseline))
    reject('change old case row', lambda: preservation(before, after.replace('| DAN-001 |', '| DAN-999 |', 1), baseline))
    reject('change old tolerance', lambda: preservation(before, after.replace('0.05 dB; mean (DC)', '0.5 dB; mean (DC)', 1), baseline))
    reject('open actual/audio/source path', lambda: read(P.parent / 'batch-analog-velocity-bytes-v1/manifest.json'))
    return results

def check():
    baseline, delta, catalog, joins = [load(n) for n in ['baseline.json', 'owner-delta.json', 'cases128.json', 'joins128.json']]
    before = verify(baseline['owner_before']).decode()
    need(baseline['authority_review'] == catalog['authority_review'] == joins['authority_review'], 'authority pins')
    review = json.loads(verify(baseline['authority_review']))
    need(review['exact_manifest']['sha256'] == 'f55b09318d1938ef6eb19ab7381d859d1e67e20f53f57840e9d3b4c6ffc930de' and review['blocking_findings'] == [], 'approved authority')
    after = compose(before, delta)
    need(signature(after) == {k: delta['owner_after'][k] for k in ['bytes', 'sha256']}, 'composed target')
    need(compose(after, delta, reverse=True) == before, 'reverse exact')
    preservation(before, after, baseline)
    aliases = json.loads(verify(baseline['r3_aliases']))
    need({x['id']: sha(encoded(x)) for x in aliases['cases']} == baseline['r3_object_digests'] and len(aliases['cases']) == 28, '28 R3 objects')
    need(sha(encoded(aliases['baseline_control'])) == baseline['r3_control_digest'], 'R3 control')
    release = json.loads(verify(baseline['released_manifest']))
    need(release['files'] == baseline['released_inventory'] and release['case_count'] == 38 and release['evaluation_count'] == 42, 'release metadata')
    check_catalog(catalog, joins, review)
    neg = controls(catalog, joins, review, before, after, baseline)
    if (P / 'manifest.json').exists():
        manifest = load('manifest.json')
        actual = {str(x.relative_to(P)) for x in P.iterdir() if x.is_file()}
        need(actual == {'manifest.json'} | {x['path'] for x in manifest['payloads']}, 'sealed tree')
        for pin in manifest['payloads']:
            raw = read(P / pin['path'])
            need(len(raw) == pin['bytes'] and sha(raw) == pin['sha256'], 'payload ' + pin['path'])
    return {'status': 'PASS', 'scope': 'Owner wording/mapping/preservation only, approved summary inherited, no observation/source/raw re-review or original call',
            'composed_owner': delta['owner_after'], 'reverse_to_R3_exact': True,
            'whole_other_bodies_exact': 21, 'old004_017_prefixes_exact': True,
            'old_case_rows_exact': 67, 'old_IDs_preserved': 75, 'new_IDs': 127, 'total_navigation_IDs': 202,
            'catalog_points': 128, 'inherited_no_new_ID': 1, 'R3objects_exact': 28,
            'released_metadata_only': [38, 42], 'negative_controls_pass': neg,
            'portable_expected_comparator_grade': None, 'actual_payload_reads': 0, 'original_calls': 0}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true', required=True)
    parser.parse_args()
    print(json.dumps(check(), indent=2))
