#!/usr/bin/env python3
"""Only staged owner data plus pinned approved summary/old owner/release metadata."""
import argparse, copy, hashlib, json, pathlib, re
P = pathlib.Path(__file__).resolve().parent
ROOT = P.parents[3]
ALLOWED = {ROOT / n for n in [
    'wiki/specs/device-analog.md',
    'analysis/ableton-live-12.4.3/full-spec-v1/reviews/analog-channel-nibbles-v1-review.json',
    'analysis/ableton-live-12.4.3/full-spec-v1/owner-analog-r3-finite-v1/case-aliases.json',
    'analysis/ableton-live-12.4.3/full-spec-v1/owner-analog-r4-velocity-finite-v1/cases128.json',
    'analysis/ableton-live-12.4.3/full-spec-v1/owner-analog-r5-note-keys-finite-v1/cases128.json',
    'handoff/device-analog-v1/manifest.json']}

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
    return {m[1]: m[0] for m in re.finditer(r'^### (REQ-DEVICE-ANALOG-\d{3})[^\n]*\n.*?(?=^### REQ-|^## |\Z)', text, re.M | re.S)}

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
    need(len(old) == len(new) == 23 and old.keys() == new.keys(), 'REQ set')
    need({k: sig(v) for k,v in old.items()} == baseline['requirement_bodies'], 'baseline bodies')
    for key in old:
        if key in baseline['append_only_requirements']:
            need(new[key].startswith(old[key]), 'old004 prefix')
        else:
            need(new[key] == old[key], 'whole other body ' + key)
    rows = lambda s: [x for x in s.splitlines() if x.startswith('| DAN-')]
    need(rows(before) == rows(after) == baseline['old_rows'] and len(rows(after)) == 67, 'old rows')
    for key, pin in baseline['protected_sections'].items():
        need(sig(sections(before)[key]) == sig(sections(after)[key]) == pin, 'protected section ' + key)
    old_acceptance, new_acceptance = sections(before)['Acceptance cases'], sections(after)['Acceptance cases']
    need(sig(old_acceptance) == baseline['old_acceptance_prefix'] and new_acceptance.startswith(old_acceptance), 'all old acceptance/annex text')
    release_text = lambda s: s[s.index('Released locally on 2026-10-19:'):s.index('## Historical revision 1 evidence qualification')]
    need(sig(release_text(before)) == sig(release_text(after)) == baseline['release_prose'], 'release prose')

def expected(point, index, case_id):
    n = point['channel_nibble']; fresh = n != 0
    native = ({'original_output': point['output'], 'descriptive_both_channel_metrics': point['observed_output'],
               'hash_matches_inherited0': point['output_sha256_matches_inherited0']}
              if fresh else {'historical_output': point['historical_output'],
                             'approved_metrics': point['observed_output'], 'no_new_measurement': True})
    return {'channel_nibble': n, 'case_id': case_id,
            'existing_case_refs': [] if fresh else ['DAN-028', 'CONTROL-DAN028-P1'],
            'kind': 'finite-native-observation' if fresh else 'inherited-reference-only',
            'requirements': ['REQ-DEVICE-ANALOG-004'],
            'approved_review_pointer': f'#/approved_summary/approved_points/{index}',
            'approved_point': point, 'native_expected': native,
            'fresh_waveform_prior': None, 'portable_expected': None,
            'portable_comparator': None, 'candidate_grade': None,
            'limits': 'Only matching 0x90|n/0x80|n status low nibbles in fixed 203-word P1 key60/velocity100 history. No general channel/public A1/A2/ARM/Apple, determinism, pitch, physical calibration or portable tolerance law.'}

def catalog_check(catalog, joins, review):
    points = review['approved_summary']['approved_points']
    need(catalog['shared_input'] == review['approved_summary']['shared_input'], 'shared input')
    need([p['channel_nibble'] for p in points] == list(range(16)), 'approved universe')
    need(len(catalog['catalog']) == len(joins['joins']) == 16, 'whole catalog')
    for i, point in enumerate(points):
        n = point['channel_nibble']; fresh = n != 0
        case_id = f'DAN-{329+n:03}' if fresh else None
        item = expected(point, i, case_id)
        need(catalog['catalog'][i] == item, 'case ' + str(n))
        join = {'channel_nibble': n, 'case_id': case_id, 'existing_case_refs': item['existing_case_refs'],
                'approved_review_pointer': item['approved_review_pointer'],
                'fresh_observation': fresh, 'owner_original_calls': 0}
        need(joins['joins'][i] == join, 'join ' + str(n))
    need(catalog['logical_points'] == 16 and catalog['fresh_cases'] == 15 and catalog['inherited_ref_count'] == 1, 'counts')

def old_catalog_check(data, baseline):
    items = data['catalog']
    need(len(items) == baseline['object_count'] == 128 and {str(i): sha(enc(x)) for i,x in enumerate(items)} == baseline['object_digests'], 'all old catalog objects')
    need([x['case_id'] for x in items if x['case_id'] is not None] == baseline['case_IDs'], 'old catalog IDs')

def controls(catalog, joins, review, before, after, baseline, old_catalogs):
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
    mutate('omit nibble', lambda x,y: x['catalog'].pop())
    mutate('duplicate nibble', lambda x,y: x['catalog'].__setitem__(2, copy.deepcopy(x['catalog'][1])))
    mutate('wrong new ID', lambda x,y: x['catalog'][1].__setitem__('case_id', 'DAN-329'))
    mutate('inherited0 duplicate ID', lambda x,y: x['catalog'][0].__setitem__('case_id', 'DAN-330'))
    mutate('wrong inherited reference', lambda x,y: x['catalog'][0].__setitem__('existing_case_refs', ['DAN-203']))
    mutate('invent fresh inherited PID', lambda x,y: x['catalog'][0]['approved_point'].__setitem__('fresh_pid', 1))
    mutate('change native hash', lambda x,y: x['catalog'][1]['native_expected']['original_output'].__setitem__('sha256', '0'*64))
    mutate('erase channel metric', lambda x,y: x['catalog'][1]['native_expected']['descriptive_both_channel_metrics']['per_channel'].pop())
    mutate('change fixed203word', lambda x,y: x['shared_input']['parameter_f32_bits_le'].__setitem__(99, '00000000'))
    mutate('mismatched off channel', lambda x,y: x['catalog'][1]['approved_point']['events'][1].__setitem__('status', 128))
    mutate('invent portable comparator', lambda x,y: x['catalog'][1].__setitem__('portable_comparator', 'exact'))
    mutate('rewrite original NULL prior', lambda x,y: x['catalog'][1].__setitem__('fresh_waveform_prior', 'fitted'))
    mutate('invent candidate grade', lambda x,y: x['catalog'][1].__setitem__('candidate_grade', 'PASS'))
    mutate('wrong approved join', lambda x,y: y['joins'][1].__setitem__('approved_review_pointer', '#/unapproved'))
    mutate('invent owner execution', lambda x,y: y['joins'][1].__setitem__('owner_original_calls', 1))
    reject('change another body', lambda: preservation(before, after.replace('Live sends 203 host values.', 'Live sends 202 host values.', 1), baseline))
    reject('lose old004 prefix', lambda: preservation(before, after.replace('Release velocity has no effect.', 'Release velocity has new effect.', 1), baseline))
    reject('change old row', lambda: preservation(before, after.replace('| DAN-001 |', '| DAN-999 |', 1), baseline))
    reject('change old tolerance', lambda: preservation(before, after.replace('0.05 dB; mean (DC)', '0.5 dB; mean (DC)', 1), baseline))
    reject('change old R5 annex', lambda: preservation(before, after.replace('keys125/126/127 share hash', 'keys126/127 share hash', 1), baseline))
    for name, data in old_catalogs.items():
        bad = copy.deepcopy(data); bad['catalog'].pop()
        reject('omit old catalog object ' + name, lambda: old_catalog_check(bad, baseline['old_catalogs'][name]))
    reject('actual payload access', lambda: read(P.parent / 'batch-analog-channel-nibbles-v1/manifest.json'))
    return rejected

def check():
    baseline, delta, catalog, joins = [load(n) for n in ['baseline.json', 'owner-delta.json', 'cases16.json', 'joins16.json']]
    before = verify(baseline['owner_before']).decode()
    need(baseline['approved_review'] == catalog['approved_review'] == joins['approved_review'], 'review pins')
    review = json.loads(verify(baseline['approved_review']))
    need(review['blocking_findings'] == [] and review['exact_manifest']['sha256'] == '13a797e115f66d852da3d468b3cb63f32befd385eaee9757c847716253a3eeb5', 'approved authority')
    after = compose(before, delta)
    need(sig(after) == {k: delta['owner_after'][k] for k in ['bytes', 'sha256']}, 'composed target')
    need(compose(after, delta, reverse=True) == before, 'reverse exact')
    preservation(before, after, baseline)
    aliases = json.loads(verify(baseline['R3_aliases']))
    need({x['id']: sha(enc(x)) for x in aliases['cases']} == baseline['R3_objects'] and len(aliases['cases']) == 28, 'R3 objects')
    need(sha(enc(aliases['baseline_control'])) == baseline['R3_control'], 'R3 control')
    old_catalogs = {}; old_ids = {f'DAN-{i:03}' for i in range(1,48)} | {x['id'] for x in aliases['cases']}
    for name, item in baseline['old_catalogs'].items():
        data = json.loads(verify(item['pin'])); old_catalog_check(data, item)
        old_catalogs[name] = data; old_ids.update(item['case_IDs'])
    need(old_ids == set(baseline['old_IDs']) == {f'DAN-{i:03}' for i in range(1,330)}, '329 prior IDs')
    release = json.loads(verify(baseline['release_manifest']))
    need(release['files'] == baseline['release_inventory'] and release['case_count'] == 38 and release['evaluation_count'] == 42, 'release metadata')
    catalog_check(catalog, joins, review)
    negatives = controls(catalog, joins, review, before, after, baseline, old_catalogs)
    if (P / 'manifest.json').exists():
        manifest = load('manifest.json')
        need({x.name for x in P.iterdir() if x.is_file()} == {'manifest.json'} | {x['path'] for x in manifest['payloads']}, 'sealed tree')
        for item in manifest['payloads']:
            raw = read(P / item['path'])
            need(len(raw) == item['bytes'] and sha(raw) == item['sha256'], 'sealed payload')
    return {'status': 'PASS', 'scope': 'Only new owner wording/IDs/mapping/preservation, observations inherited',
            'composed_owner': delta['owner_after'], 'reverse_to_R5_exact': True,
            'whole_other_bodies_exact': 22, 'old004prefix_exact': True,
            'old_rows_exact': 67, 'old_IDs_exact': 329, 'new_IDs': 15, 'total_navigation_IDs': 344,
            'R3objects_exact': 28, 'R4catalog_exact': 128, 'R5catalog_exact': 128,
            'old_acceptance_annexes_prefix_exact': True, 'released_groups_evaluations': [38,42],
            'catalog': 16, 'inherited_reference_only': 1, 'negative_controls_pass': negatives,
            'actual_packet_reads': 0, 'original_calls': 0}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true', required=True)
    parser.parse_args()
    print(json.dumps(check(), indent=2))
