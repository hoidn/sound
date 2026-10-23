#!/usr/bin/env python3
"""Only current owner, approved summary and retained owner/release metadata; no actual reads."""
import argparse, copy, hashlib, json, pathlib, re
P = pathlib.Path(__file__).resolve().parent
ROOT = P.parents[3]
ALLOWED = {ROOT / n for n in [
    'wiki/specs/device-tension.md',
    'analysis/ableton-live-12.4.3/full-spec-v1/reviews/tension-velocity-bytes-v1-review.json',
    'analysis/ableton-live-12.4.3/full-spec-v1/owner-tension-r3-retained-v1/adoption-map.json',
    'analysis/ableton-live-12.4.3/full-spec-v1/owner-tension-r4-sensitivity-v1/adoption-map.json',
    'handoff/device-tension-v1/manifest.json']}

def need(v, message):
    if not v:
        raise ValueError(message)

def read(path):
    path = pathlib.Path(path).resolve()
    need(path.parent == P or path in ALLOWED, 'refuse outside staged/approved data')
    return path.read_bytes()

def load(name):
    return json.loads(read(P / name))

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def enc(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode()

def sig(text):
    return {'bytes': len(text.encode()), 'sha256': sha(text.encode())}

def verify(pin):
    raw = read(ROOT / pin['path'])
    need(len(raw) == pin['bytes'] and sha(raw) == pin['sha256'], 'identity ' + pin['path'])
    return raw

def bodies(text):
    return {m[1]: m[0] for m in re.finditer(r'^### (REQ-DEVICE-TENSION-\d{3})[^\n]*\n.*?(?=^### REQ-|^## |\Z)', text, re.M | re.S)}

def sections(text):
    return {m[1]: m[0] for m in re.finditer(r'^## ([^\n]+)\n.*?(?=^## |\Z)', text, re.M | re.S)}

def compose(text, delta, reverse=False):
    items = list(reversed(delta['replacements'])) if reverse else delta['replacements']
    for item in items:
        old, new = (item['new'], item['old']) if reverse else (item['old'], item['new'])
        need(text.count(old) == 1, 'unique replacement ' + item['label'])
        text = text.replace(old, new, 1)
    return text

def preservation(before, after, baseline):
    old, new = bodies(before), bodies(after)
    need(len(old) == len(new) == 15 and old.keys() == new.keys(), 'REQ set')
    need({k: sig(v) for k,v in old.items()} == baseline['requirement_bodies'], 'baseline bodies')
    for key in old:
        if key in baseline['append_only_requirements']:
            need(new[key].startswith(old[key]), 'old prefix ' + key)
        else:
            need(new[key] == old[key], 'whole other body ' + key)
    rows = lambda s: [x for x in s.splitlines() if x.startswith('| DTN-')]
    need(rows(before) == rows(after) == baseline['old_rows'] and len(rows(after)) == 42, 'old rows')
    for key, pin in baseline['protected_sections'].items():
        need(sig(sections(before)[key]) == sig(sections(after)[key]) == pin, 'protected section ' + key)
    release_text = lambda s: s[s.index('The [finite handoff plan]'):s.index('## Tension guarded getter qualification')]
    need(sig(release_text(before)) == sig(release_text(after)) == baseline['release_prose'], 'release prose')

def expected(point, index, case_id):
    v = point['velocity']; fresh = point['provenance'] == 'fresh-once-reviewed'
    refs = [] if fresh else ['DTN-001' if v == 100 else 'DTN-005']
    native = ({'original_output': point['output'], 'native_word_summary': point['summary']}
              if fresh else {'historical_metadata': point['historical'], 'no_new_measurement': True})
    return {'velocity': v, 'case_id': case_id, 'existing_case_refs': refs,
            'kind': 'finite-native-observation' if fresh else 'inherited-reference-only',
            'requirements': ['REQ-DEVICE-TENSION-003', 'REQ-DEVICE-TENSION-007'],
            'approved_review_pointer': f'#/approved_summary/approved_points/{index}',
            'approved_point': point, 'native_expected': native,
            'fresh_waveform_prior': None, 'portable_expected': None,
            'portable_comparator': None, 'candidate_grade': None,
            'bookkeeping_qualification_pointer': '#/bookkeeping_qualifications',
            'limits': 'Only exact supplied default 129-word C4 history. No new waveform metric, f0, velocity law, stability/calibration/tolerance, public A1/A2 or ARM/Apple behavior.'}

def catalog_check(catalog, joins, review):
    summary = review['approved_summary']; points = summary['approved_points']
    need(catalog['shared_input'] == summary['shared_input'], 'shared input')
    need(catalog['bookkeeping_qualifications'] == review['bookkeeping_qualifications'], 'parent/durability qualifications')
    need(catalog['bookkeeping_qualifications']['parent_pre_call_file_bound'] is False, 'parent custody stays unknown')
    need(summary['parent_custody_qualification_required'] is True, 'required qualification')
    need([p['velocity'] for p in points] == list(range(128)), 'approved universe')
    need(len(catalog['catalog']) == len(joins['joins']) == 128, 'whole catalog')
    number = 43
    for index, point in enumerate(points):
        v = point['velocity']; fresh = v not in {1, 100, 127}
        need((point['provenance'] == 'fresh-once-reviewed') == fresh, 'fresh provenance')
        case_id = f'DTN-{number:03}' if fresh else None
        if fresh:
            number += 1
        item = expected(point, index, case_id)
        need(catalog['catalog'][index] == item, 'case ' + str(v))
        join = {'velocity': v, 'case_id': case_id, 'existing_case_refs': item['existing_case_refs'],
                'approved_review_pointer': item['approved_review_pointer'],
                'fresh_observation': fresh, 'owner_new_original_calls': 0}
        need(joins['joins'][index] == join, 'join ' + str(v))
    need(number == 168 and catalog['logical_points'] == 128 and catalog['fresh_cases'] == 125 and catalog['inherited_references'] == 3, 'ID/counts')

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
    mutate('omit velocity', lambda x,y: x['catalog'].pop())
    mutate('duplicate velocity', lambda x,y: x['catalog'].__setitem__(2, copy.deepcopy(x['catalog'][0])))
    mutate('wrong fresh ID', lambda x,y: x['catalog'][0].__setitem__('case_id', 'DTN-042'))
    mutate('inherited1 duplicate new ID', lambda x,y: x['catalog'][1].__setitem__('case_id', 'DTN-044'))
    mutate('wrong inherited100 reference', lambda x,y: x['catalog'][100].__setitem__('existing_case_refs', ['DTN-005']))
    mutate('invent inherited fresh PID', lambda x,y: x['catalog'][127]['approved_point'].__setitem__('new_pid', 1))
    mutate('change native hash', lambda x,y: x['catalog'][0]['native_expected']['original_output'].__setitem__('sha256', '0'*64))
    mutate('erase second-channel count', lambda x,y: x['catalog'][0]['native_expected']['native_word_summary']['nonzero_samples'].pop())
    mutate('change shared input word', lambda x,y: x['shared_input']['words'][0].__setitem__('little_endian_hex', '00000000'))
    mutate('change note phase', lambda x,y: x['catalog'][0]['approved_point']['events'][0].__setitem__(0, 4400))
    mutate('invent portable comparator', lambda x,y: x['catalog'][0].__setitem__('portable_comparator', 'exact'))
    mutate('rewrite NULL waveform prior', lambda x,y: x['catalog'][0].__setitem__('fresh_waveform_prior', 'fitted'))
    mutate('invent candidate pass', lambda x,y: x['catalog'][0].__setitem__('candidate_grade', 'PASS'))
    mutate('wrong approved join', lambda x,y: y['joins'][0].__setitem__('approved_review_pointer', '#/unapproved'))
    mutate('invent owner execution', lambda x,y: y['joins'][0].__setitem__('owner_new_original_calls', 1))
    mutate('promote parent precall custody to pass', lambda x,y: x['bookkeeping_qualifications'].__setitem__('parent_pre_call_file_bound', True))
    mutate('erase fsync qualification', lambda x,y: x['bookkeeping_qualifications'].__setitem__('durability', 'all raw and JSON fsynced'))
    reject('change another REQ', lambda: preservation(before, after.replace('Live sends indices 0 to 129 except 2', 'Live sends indices 0 to 128 except 2', 1), baseline))
    reject('lose old003 prefix', lambda: preservation(before, after.replace('A note-on with velocity 0 acts as a note-off.', 'Velocity0 gives a general new law.', 1), baseline))
    reject('change old row', lambda: preservation(before, after.replace('| DTN-001 |', '| DTN-999 |', 1), baseline))
    reject('change old tolerance', lambda: preservation(before, after.replace('Frequency within 2 × 10⁻⁶ relative', 'Frequency within 3 × 10⁻⁶ relative', 1), baseline))
    reject('change R4 sensitivity row', lambda: preservation(before, after.replace('3.16792297039e-05', '3e-05', 1), baseline))
    reject('change release prose', lambda: preservation(before, after.replace('27 calibrated finite output evaluations only.', '28 calibrated finite output evaluations only.', 1), baseline))
    reject('open new actual payload', lambda: read(P.parent / 'batch-tension-velocity-bytes-v1/manifest.json'))
    reject('open old222 actual payload', lambda: read(P.parent / 'batch-tension-uncalibrated-sensitivity-v1/manifest.json'))
    return rejected

def check():
    baseline, delta, catalog, joins = [load(n) for n in ['baseline.json', 'owner-delta.json', 'cases128.json', 'joins128.json']]
    before = verify(baseline['owner_before']).decode()
    need(baseline['approved_review'] == catalog['approved_review'] == joins['approved_review'], 'review pins')
    review = json.loads(verify(baseline['approved_review']))
    need(review['blocking_findings_for_finite_observations'] == [] and review['frozen_packet']['manifest']['sha256'] == 'cc180fa914de8ee4c22365d07f6910449b37cf23c11bbf62318b51dd790d3508', 'approved authority')
    after = compose(before, delta)
    need(sig(after) == {k: delta['owner_after'][k] for k in ['bytes', 'sha256']}, 'composed target')
    need(compose(after, delta, reverse=True) == before, 'reverse exact')
    preservation(before, after, baseline)
    map_counts = {}
    for name, item in baseline['retained_owner_maps'].items():
        metadata = json.loads(verify(item['pin']))
        objects = metadata[item['collection_key']]
        digest = ({str(i): sha(enc(x)) for i,x in enumerate(objects)} if isinstance(objects, list)
                  else {k: sha(enc(v)) for k,v in objects.items()})
        need(len(objects) == item['object_count'] and digest == item['object_digests'], 'retained owner objects')
        map_counts[name] = len(objects)
    release = json.loads(verify(baseline['release_manifest']))
    need(release['files'] == baseline['release_inventory'] and len(release['files']) == 35 and release['case_count'] == release['evaluation_count'] == 27, 'release metadata')
    catalog_check(catalog, joins, review)
    negatives = controls(catalog, joins, review, before, after, baseline)
    if (P / 'manifest.json').exists():
        manifest = load('manifest.json')
        need({x.name for x in P.iterdir() if x.is_file()} == {'manifest.json'} | {x['path'] for x in manifest['payloads']}, 'sealed tree')
        for item in manifest['payloads']:
            raw = read(P / item['path'])
            need(len(raw) == item['bytes'] and sha(raw) == item['sha256'], 'sealed payload')
    return {'status': 'PASS', 'scope': 'New owner wording/IDs/mapping/preservation only; approved actual summary inherited',
            'composed_owner': delta['owner_after'], 'reverse_to_R4_exact': True,
            'whole_other_bodies_exact': 13, 'old003_007prefixes_exact': True,
            'old_rows_IDs_exact': 42, 'new_IDs': 125, 'total_navigation_IDs': 167,
            'catalog': 128, 'inherited_reference_only': 3, 'retained_owner_objects': map_counts,
            'R4sensitivity_section_exact': True, 'release_evaluations': 27, 'release_inventory_metadata_entries': 35,
            'parent_pre_call_file_bound': False, 'durability_qualification_exact': True,
            'negative_controls_pass': negatives, 'actual_packet_reads': 0, 'original_calls': 0}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true', required=True)
    parser.parse_args()
    print(json.dumps(check(), indent=2))
