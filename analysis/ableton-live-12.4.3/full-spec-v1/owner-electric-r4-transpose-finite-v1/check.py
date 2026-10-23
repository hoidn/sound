#!/usr/bin/env python3
"""Owned staged-data check; no actual packet, runtime, old helper or release fixture reads."""
import argparse, copy, hashlib, json, pathlib, re
P = pathlib.Path(__file__).resolve().parent
ROOT = P.parents[3]
ALLOWED = {ROOT / n for n in [
    'wiki/specs/device-electric.md',
    'analysis/ableton-live-12.4.3/full-spec-v1/reviews/electric-transpose-integers-v1-review.json',
    'analysis/ableton-live-12.4.3/full-spec-v1/owner-electric-r3-finite-v1/cases.json',
    'handoff/device-electric-v2/manifest.json']}

def need(value, message):
    if not value:
        raise ValueError(message)

def read(path):
    path = pathlib.Path(path).resolve()
    need(path.parent == P or path in ALLOWED, 'refuse outside staged/approved data')
    return path.read_bytes()

def load(name):
    return json.loads(read(P / name))

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def encoded(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode()

def sig(text):
    return {'bytes': len(text.encode()), 'sha256': sha(text.encode())}

def verify(pin):
    raw = read(ROOT / pin['path'])
    need(len(raw) == pin['bytes'] and sha(raw) == pin['sha256'], 'identity ' + pin['path'])
    return raw

def bodies(text):
    return {m[1]: m[0] for m in re.finditer(r'^### (REQ-DEVICE-ELECTRIC-\d{3})[^\n]*\n.*?(?=^### REQ-|^## |\Z)', text, re.M | re.S)}

def sections(text):
    return {m[1]: m[0] for m in re.finditer(r'^## ([^\n]+)\n.*?(?=^## |\Z)', text, re.M | re.S)}

def compose(text, delta, reverse=False):
    replacements = list(reversed(delta['replacements'])) if reverse else delta['replacements']
    for item in replacements:
        old, new = (item['new'], item['old']) if reverse else (item['old'], item['new'])
        need(text.count(old) == 1, 'unique delta ' + item['label'])
        text = text.replace(old, new, 1)
    return text

def preservation(before, after, baseline):
    old, new = bodies(before), bodies(after)
    need(len(old) == len(new) == 16 and old.keys() == new.keys(), 'REQ set')
    need({k: sig(v) for k, v in old.items()} == baseline['requirement_bodies'], 'baseline bodies')
    for key in old:
        if key in baseline['append_only_requirements']:
            need(new[key].startswith(old[key]), 'old prefix ' + key)
        else:
            need(old[key] == new[key], 'other whole body ' + key)
    rows = lambda s: [line for line in s.splitlines() if line.startswith('| DEL-')]
    need(rows(before) == rows(after) == baseline['case_rows'] and len(rows(after)) == 40, 'old rows')
    for name, pin in baseline['protected_sections'].items():
        need(sig(sections(before)[name]) == sig(sections(after)[name]) == pin, 'section ' + name)
    release_text = lambda s: s[s.index('The [finite handoff plan]'):s.index('## Internal helper qualification')]
    need(sig(release_text(before)) == sig(release_text(after)) == baseline['release_prose'], 'released prose')

def expected(point, index, case_id):
    n = point['transpose_integer']; fresh = n not in {0, 12, 24}
    native = ({'original_output': point['output'], 'observed_whole_warmup_render': point['observed_output']}
              if fresh else {'historical_output': point['historical_output'],
                             'approved_observations': point['approved_observations'],
                             'historical_render_sha256': point['historical_render_stereo_sha256'],
                             'new_descriptive_metrics': None})
    return {'transpose_integer': n, 'case_id': case_id,
            'existing_case_refs': [] if fresh else point['existing_owner_case_refs'],
            'kind': 'finite-native-observation' if fresh else 'inherited-reference-only',
            'requirements': ['REQ-DEVICE-ELECTRIC-002', 'REQ-DEVICE-ELECTRIC-006'],
            'review_point_pointer': f'#/approved_summary/approved_points/{index}',
            'approved_point': point, 'native_expected': native,
            'original_waveform_prior': None, 'portable_expected': None,
            'portable_comparator': None, 'candidate_grade': None,
            'limits': 'Exact supplied 33-word P1 context only. No public stored dispatch, current receiver, f0/pitch law, physical calibration, portable tolerance, repeat/seed stability or ARM/Apple behavior.'}

def catalog_check(catalog, joins, review):
    points = review['approved_summary']['approved_points']
    need(catalog['shared_input'] == review['approved_summary']['shared_input'], 'shared input')
    need([p['transpose_integer'] for p in points] == list(range(25)), 'approved universe')
    need(len(catalog['catalog']) == len(joins['joins']) == 25, 'whole catalog')
    case_number = 9
    for index, point in enumerate(points):
        n = point['transpose_integer']; fresh = n not in {0, 12, 24}
        case_id = f'DEL-CS-{case_number:03}' if fresh else None
        if fresh:
            case_number += 1
        item = expected(point, index, case_id)
        need(catalog['catalog'][index] == item, 'case ' + str(n))
        join = {'transpose_integer': n, 'case_id': case_id,
                'existing_case_refs': item['existing_case_refs'],
                'review_point_pointer': item['review_point_pointer'],
                'fresh_observation': fresh, 'new_original_calls_by_owner': 0}
        need(joins['joins'][index] == join, 'join ' + str(n))
    need(case_number == 31, 'new ID end')
    need(catalog['logical_points'] == 25 and catalog['fresh_case_count'] == 22 and catalog['inherited_ref_count'] == 3, 'counts')

def controls(catalog, joins, review, before, after, baseline):
    rejected = []
    def reject(name, fn):
        try:
            fn()
        except (ValueError, KeyError, IndexError):
            rejected.append(name)
        else:
            raise AssertionError('negative accepted ' + name)
    def mutate(name, edit):
        x, y = copy.deepcopy(catalog), copy.deepcopy(joins)
        edit(x, y)
        reject(name, lambda: catalog_check(x, y, review))
    mutate('omit integer', lambda x,y: x['catalog'].pop())
    mutate('duplicate integer', lambda x,y: x['catalog'].__setitem__(2, copy.deepcopy(x['catalog'][1])))
    mutate('wrong numeric integer', lambda x,y: x['catalog'][1].__setitem__('transpose_integer', 25))
    mutate('wrong new ID', lambda x,y: x['catalog'][1].__setitem__('case_id', 'DEL-CS-008'))
    mutate('inherit12 duplicate new ID', lambda x,y: x['catalog'][12].__setitem__('case_id', 'DEL-CS-020'))
    mutate('wrong inherited owner reference', lambda x,y: x['catalog'][0].__setitem__('existing_case_refs', ['DEL-CS-001']))
    mutate('invent inherited fresh PID', lambda x,y: x['catalog'][0]['approved_point'].__setitem__('fresh_pid', 1))
    mutate('changed native hash', lambda x,y: x['catalog'][1]['native_expected']['original_output'].__setitem__('sha256', '0'*64))
    mutate('changed right render metric', lambda x,y: x['catalog'][1]['native_expected']['observed_whole_warmup_render']['render']['per_channel'].pop())
    mutate('changed shared warmup', lambda x,y: x['shared_input']['history'].__setitem__('warmup_frames', 0))
    mutate('changed index32', lambda x,y: x['catalog'][1]['approved_point']['parameter_f32_bits_le'].__setitem__(32, '00000000'))
    mutate('invent portable comparator', lambda x,y: x['catalog'][1].__setitem__('portable_comparator', 'exact'))
    mutate('rewrite NULL prior', lambda x,y: x['catalog'][1].__setitem__('original_waveform_prior', 'fitted'))
    mutate('invent candidate pass', lambda x,y: x['catalog'][1].__setitem__('candidate_grade', 'PASS'))
    mutate('wrong review point join', lambda x,y: y['joins'][1].__setitem__('review_point_pointer', '#/unapproved'))
    mutate('invent new owner execution', lambda x,y: y['joins'][1].__setitem__('new_original_calls_by_owner', 1))
    reject('change other REQ', lambda: preservation(before, after.replace('The channel has no effect:', 'The channel has an effect:', 1), baseline))
    reject('lose old002 prefix', lambda: preservation(before, after.replace('Live sends 33 host values.', 'Live sends 32 host values.', 1), baseline))
    reject('change old row', lambda: preservation(before, after.replace('| DEL-001 |', '| DEL-999 |', 1), baseline))
    reject('change general tolerance', lambda: preservation(before, after.replace('largest is 2.96 dB.', 'largest is 3 dB.', 1), baseline))
    reject('change released scope prose', lambda: preservation(before, after.replace('117 finite mono outputs, partial', '118 finite mono outputs, partial', 1), baseline))
    reject('actual payload access', lambda: read(P.parent / 'batch-electric-transpose-integers-v1/manifest.json'))
    return rejected

def check():
    baseline, delta, catalog, joins = [load(n) for n in ['baseline.json', 'owner-delta.json', 'cases25.json', 'joins25.json']]
    before = verify(baseline['owner_before']).decode()
    need(baseline['approved_review'] == catalog['approved_review'] == joins['approved_review'], 'review pins')
    review = json.loads(verify(baseline['approved_review']))
    need(review['blocking_findings'] == [] and review['exact_manifest']['sha256'] == '092db7a646dda115cc9f6357e12591fbe94a3a87cec3c3183316444f26351aad', 'approved observation authority')
    after = compose(before, delta)
    need(sig(after) == {k: delta['owner_after'][k] for k in ['bytes', 'sha256']}, 'composed target')
    need(compose(after, delta, reverse=True) == before, 'exact reverse')
    preservation(before, after, baseline)
    aliases = json.loads(verify(baseline['R3_cases']))
    need({x['id']: sha(encoded(x)) for x in aliases['cases']} == baseline['R3_objects'] and len(aliases['cases']) == 8, 'R3 objects')
    need({str(i): sha(encoded(x)) for i,x in enumerate(aliases['pair_relations'])} == baseline['R3_pairs'] and len(aliases['pair_relations']) == 2, 'R3 pairs')
    release = json.loads(verify(baseline['release_manifest']))
    need(release['files'] == baseline['release_inventory'] and len(release['files']) == 129 and release['case_count'] == release['evaluation_count'] == 117, 'release metadata')
    catalog_check(catalog, joins, review)
    negatives = controls(catalog, joins, review, before, after, baseline)
    if (P / 'manifest.json').exists():
        manifest = load('manifest.json')
        need({x.name for x in P.iterdir() if x.is_file()} == {'manifest.json'} | {x['path'] for x in manifest['payloads']}, 'sealed tree')
        for item in manifest['payloads']:
            raw = read(P / item['path'])
            need(len(raw) == item['bytes'] and sha(raw) == item['sha256'], 'sealed payload')
    return {'status': 'PASS', 'scope': 'Only new owner wording/mapping/IDs/preservation; approved observations inherited',
            'composed_owner': delta['owner_after'], 'reverse_to_R3_exact': True,
            'whole_other_bodies_exact': 14, 'old002_006prefixes_exact': True,
            'old_rows_IDs_exact': 40, 'new_IDs': 22, 'total_navigation_IDs': 62,
            'catalog': 25, 'inherited_ref_only': 3, 'R3objects_exact': 8, 'R3pairs_exact': 2,
            'released_inventory_metadata_entries': 129, 'released_evaluations': 117,
            'negative_controls_pass': negatives, 'actual_packet_reads': 0, 'original_calls': 0}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true', required=True)
    parser.parse_args()
    print(json.dumps(check(), indent=2))
