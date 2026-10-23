"""Owner wording/mapping/preservation only; reads approved summary, never actuals."""
import copy
import hashlib
import json
from pathlib import Path
import re
import sys

P = Path(__file__).resolve().parent
ROOT = P.parents[3]
B = ROOT / 'analysis/ableton-live-12.4.3/full-spec-v1'
ALLOWED = {ROOT / 'wiki/specs/device-analog.md', ROOT / 'handoff/device-analog-v1/manifest.json',
           B / 'reviews/analog-note-keys-v1-review.json',
           B / 'owner-analog-r3-finite-v1/case-aliases.json',
           B / 'owner-analog-r4-velocity-finite-v1/cases128.json',
           B / 'owner-analog-r4-velocity-finite-v1/manifest.json'}


def need(ok, message):
    if not ok:
        raise ValueError(message)


def read(path):
    p = Path(path).resolve()
    need(p.parent == P or p in ALLOWED, 'Outside owner/approved-summary metadata: ' + str(p))
    return p.read_bytes()


def load(name):
    return json.loads(read(P / name))


def digest(raw):
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def textpin(text):
    return digest(text.encode())


def objecthash(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()).hexdigest()


def verify(pin):
    raw = read(ROOT / pin['path'])
    need(digest(raw) == {k: pin[k] for k in ('bytes', 'sha256')}, 'Identity ' + pin['path'])
    return raw


def bodies(text):
    return {m[1]: m[0] for m in re.finditer(r'^### (REQ-DEVICE-ANALOG-\d{3})[^\n]*\n.*?(?=^### REQ-|^## |\Z)', text, re.M | re.S)}


def sections(text):
    return {m[1]: m[0] for m in re.finditer(r'^## ([^\n]+)\n.*?(?=^## |\Z)', text, re.M | re.S)}


def rows(text):
    return [x for x in text.splitlines() if x.startswith('| DAN-')]


def compose(text, delta, reverse=False):
    replacements = list(reversed(delta['replacements'])) if reverse else delta['replacements']
    for item in replacements:
        old, new = (item['new'], item['old']) if reverse else (item['old'], item['new'])
        need(text.count(old) == 1, 'Nonunique fragment ' + item['label'])
        text = text.replace(old, new, 1)
    return text


def preservation(before, after, baseline):
    old, new = bodies(before), bodies(after)
    need(len(old) == len(new) == 23 and old.keys() == new.keys(), 'REQ identity set')
    need({k: textpin(v) for k, v in old.items()} == baseline['requirement_bodies'], 'Before REQ pins')
    for k in old:
        if k == 'REQ-DEVICE-ANALOG-004':
            need(new[k].startswith(old[k]), '004 old prefix changed')
        else:
            need(new[k] == old[k], 'Other whole REQ changed ' + k)
    need(rows(before) == rows(after) == baseline['case_rows'] and len(rows(after)) == 67, 'Old table rows')
    for k, pin in baseline['protected_sections'].items():
        need(textpin(sections(before)[k]) == textpin(sections(after)[k]) == pin, 'Protected section ' + k)
    need(sections(after)['Acceptance cases'].startswith(sections(before)['Acceptance cases']), 'Old acceptance section prefix')


def expected_case(point, index, case_id):
    key = point['note_key']; fresh = key != 60
    return {'note_key': key, 'observation_id': point['id'], 'case_id': case_id,
            'kind': 'finite-native-observation' if fresh else 'inherited-reference-only',
            'requirements': ['REQ-DEVICE-ANALOG-004'],
            'context_requirements_not_newly_validated': ['REQ-DEVICE-ANALOG-006'],
            'existing_case_refs': [] if fresh else ['DAN-028', 'CONTROL-DAN028-P1'],
            'approved_review_pointer': f'#/approved_summary/approved_points/{index}',
            'approved_point_sha256': objecthash(point),
            'input': {'shared_input_pointer': '#/shared_input', 'note_key': key,
                      'events': point['input_events'], 'script': point['input_script']},
            'native_expected': {'provenance': 'X: original x86_64 in exact supplied-data context',
                                'output': point['output'] if fresh else point['historical_output'],
                                'descriptive_both_channel_metrics': point['observed_output'],
                                'hash_matches_inherited60': point['output_sha256_matches_inherited60'] if fresh else None},
            'original_waveform_prior': point['waveform_prediction'], 'portable_expected': None,
            'portable_comparator': None, 'candidate_grade': None,
            'fresh_pid': point['fresh_pid'] if fresh else None,
            'fresh_receipt': point['receipt'] if fresh else None,
            'fresh_utc': point['fresh_utc'] if fresh else None,
            'historical_reference': None if fresh else point['historical_reference'],
            'limitations': 'Only exact203word/P1/key-byte class at fixedvelocity100/eightmodifiers0. No f0, pitch/clamp/alias mechanism, general key or onset law, physical calibration, public/Live/ARM law, portable waveform criterion, tolerance or grade.'}


def mapping(catalog, joins, review):
    summary = review['approved_summary']; pts = summary['approved_points']
    need(catalog['shared_input'] == summary['shared_input'], 'Shared203words/history')
    need([p['note_key'] for p in pts] == list(range(128)), 'Complete approved universe')
    need(len(catalog['catalog']) == len(joins['joins']) == 128, 'Full catalog/joins')
    next_id = 203
    for i, p in enumerate(pts):
        fresh = p['note_key'] != 60; case_id = f'DAN-{next_id:03d}' if fresh else None
        if fresh:
            next_id += 1
        need(catalog['catalog'][i] == expected_case(p, i, case_id), 'Case join ' + str(i))
        expected = {'note_key': p['note_key'], 'case_id': case_id,
                    'approved_review_pointer': f'#/approved_summary/approved_points/{i}',
                    'approved_point_sha256': objecthash(p), 'provenance': p['provenance'],
                    'new_ID': fresh, 'original_calls_in_approved_batch': 1 if fresh else 0}
        need(joins['joins'][i] == expected, 'Join row ' + str(i))
    need(next_id == 330 and catalog['logical_points'] == 128 and catalog['fresh_cases'] == 127 and catalog['inherited_references'] == 1, 'IDs/counts')


def negatives(catalog, joins, review, before, after, baseline):
    passed = []
    def reject(name, action):
        try:
            action()
        except (ValueError, KeyError, IndexError):
            passed.append(name)
        else:
            raise AssertionError('Accepted negative ' + name)
    def changed(name, edit):
        x, y = copy.deepcopy(catalog), copy.deepcopy(joins)
        edit(x, y); reject(name, lambda: mapping(x, y, review))
    changed('omit key', lambda x,y: x['catalog'].pop())
    changed('duplicate key', lambda x,y: x['catalog'].__setitem__(1, copy.deepcopy(x['catalog'][0])))
    changed('wrong integer key', lambda x,y: x['catalog'][1].update(note_key=128))
    changed('swap fresh IDs', lambda x,y: x['catalog'][0].update(case_id='DAN-204'))
    changed('invent inherited ID', lambda x,y: x['catalog'][60].update(case_id='DAN-263'))
    changed('invent inherited PID', lambda x,y: x['catalog'][60].update(fresh_pid=1))
    changed('wrong off key', lambda x,y: x['catalog'][0]['input']['events'][1].update(key=1))
    changed('wrong receipt', lambda x,y: x['catalog'][1]['fresh_receipt'].update(zero_based_record=0))
    changed('change203word', lambda x,y: x['shared_input']['parameter_f32_bits_le'].__setitem__(99, '00000000'))
    changed('wrong velocity', lambda x,y: x['shared_input']['history']['note_on'].update(velocity=127))
    changed('change native hash', lambda x,y: x['catalog'][0]['native_expected']['output'].update(sha256='0'*64))
    changed('erase right metric', lambda x,y: x['catalog'][0]['native_expected']['descriptive_both_channel_metrics']['per_channel'].pop())
    changed('general pitch admission', lambda x,y: x['catalog'][0]['requirements'].append('REQ-DEVICE-ANALOG-006'))
    changed('rewrite NULL prior', lambda x,y: x['catalog'][0].update(original_waveform_prior='fit'))
    changed('invent portable comparator', lambda x,y: x['catalog'][0].update(portable_comparator='exact'))
    changed('invent grade', lambda x,y: x['catalog'][0].update(candidate_grade='PASS'))
    changed('wrong summary pointer', lambda x,y: y['joins'][0].update(approved_review_pointer='#/wrong'))
    reject('change pitch body', lambda: preservation(before, after.replace('335 cases.', '336 cases.', 1), baseline))
    reject('lose004prefix', lambda: preservation(before, after.replace('Release velocity has no effect.', 'Release velocity unknown.', 1), baseline))
    reject('change old row', lambda: preservation(before, after.replace('| DAN-001 |', '| DAN-999 |', 1), baseline))
    reject('change old tolerance', lambda: preservation(before, after.replace('0.05 dB; mean (DC)', '0.5 dB; mean (DC)', 1), baseline))
    reject('open actual/raw', lambda: read(B / 'batch-analog-note-keys-v1/manifest.json'))
    return passed


def check():
    baseline, delta, catalog, joins = [load(n) for n in ('baseline.json', 'owner-delta.json', 'cases128.json', 'joins128.json')]
    raw = read(ROOT / baseline['owner_before']['path']).decode()
    if textpin(raw) == {k: delta['owner_after'][k] for k in ('bytes', 'sha256')}:
        before = compose(raw, delta, reverse=True)
    else:
        before = raw
    need(textpin(before) == {k: baseline['owner_before'][k] for k in ('bytes', 'sha256')}, 'Canonical before identity')
    after = compose(before, delta)
    need(textpin(after) == {k: delta['owner_after'][k] for k in ('bytes', 'sha256')} and compose(after, delta, reverse=True) == before, 'Target/reversal')
    need(baseline['authority_review'] == catalog['authority_review'] == joins['authority_review'], 'Review pins')
    review = json.loads(verify(baseline['authority_review']))
    need(review['blocking_findings'] == [] and review['required_corrections'] == [] and review['exact_manifest']['sha256'] == '78179c8f03507148e126bd370a9cea5db2f8c902807b9fa928a49b325823000e', 'Sole approved actual summary')
    preservation(before, after, baseline)
    r3 = json.loads(verify(baseline['r3_aliases']))
    need({p['id']: objecthash(p) for p in r3['cases']} == baseline['r3_object_digests'] and objecthash(r3['baseline_control']) == baseline['r3_control_digest'], 'R3objects/control')
    r4 = json.loads(verify(baseline['r4_catalog']))
    need([objecthash(x) for x in r4['catalog']] == baseline['r4_object_digests'] and len(r4['catalog']) == 128, 'R4wholecatalog128')
    verify(baseline['r4_manifest'])
    release = json.loads(verify(baseline['released_manifest']))
    need(release['files'] == baseline['released_inventory'] and release['case_count'] == 38 and release['evaluation_count'] == 42, 'Released metadata unchanged')
    need(baseline['old_case_IDs'] == [f'DAN-{n:03d}' for n in range(1,203)], 'Prior202navigationIDs')
    mapping(catalog, joins, review)
    controls = negatives(catalog, joins, review, before, after, baseline)
    if (P / 'manifest.json').exists():
        m = load('manifest.json')
        need({x.name for x in P.iterdir() if x.is_file()} == {x['path'] for x in m['payloads']} | {'manifest.json'}, 'Sealed membership')
        for pin in m['payloads']:
            need(digest(read(P / pin['path'])) == {k: pin[k] for k in ('bytes','sha256')}, 'Payload ' + pin['path'])
    return {'status': 'PASS', 'scope': 'Added owner wording/mapping/IDs/preservation only; observations inherited by approved summary, no actual re-review',
            'composed_owner': delta['owner_after'], 'reverse_to_R4_exact': True, 'other_whole_requirement_bodies_exact': 22,
            'old004prefix_exact': True, 'old_rows_exact': 67, 'old_IDs_preserved': 202, 'new_IDs': [203,329],
            'new_case_count': 127, 'logical_catalog': 128, 'inherited_ref_no_newID': 1, 'R3objects_exact': 28,
            'R4catalog_objects_exact': 128, 'released_metadata_only': [38,42], 'negative_controls': controls,
            'actual_payload_source_raw_reads': 0, 'metric_recomputations': 0, 'original_calls': 0}


if __name__ == '__main__':
    need(sys.argv[1:] == ['--check'], 'Only --check')
    print(json.dumps(check(), indent=2, allow_nan=False))
