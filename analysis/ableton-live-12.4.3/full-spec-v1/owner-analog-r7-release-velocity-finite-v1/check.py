#!/usr/bin/env python3
"""Only staged owner data plus pinned approved summary/old owner/release metadata."""
import argparse, copy, hashlib, json, pathlib, re
P = pathlib.Path(__file__).resolve().parent
ROOT = P.parents[3]
ALLOWED = {ROOT / n for n in [
    'wiki/specs/device-analog.md',
    'analysis/ableton-live-12.4.3/full-spec-v1/reviews/analog-release-velocity-bytes-v1-review.json',
    'analysis/ableton-live-12.4.3/full-spec-v1/owner-analog-r3-finite-v1/case-aliases.json',
    'analysis/ableton-live-12.4.3/full-spec-v1/owner-analog-r4-velocity-finite-v1/cases128.json',
    'analysis/ableton-live-12.4.3/full-spec-v1/owner-analog-r5-note-keys-finite-v1/cases128.json',
    'analysis/ableton-live-12.4.3/full-spec-v1/owner-analog-r6-channel-finite-v1/cases16.json',
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

def expected(point,index,case_id):
 k=point['release_velocity_byte'];fresh=k!=64
 native=({'original_output':point['output'],'descriptive_both_channel_metrics':point['observed_output'],'hash_matches_inherited64':point['output_sha256_matches_inherited64']} if fresh else {'historical_output':point['inherited_source']['historical_raw_output_not_opened'],'approved_metrics':point['inherited_source']['approved_projection']['observed_output'],'no_new_measurement':True})
 return {'release_velocity_byte':k,'case_id':case_id,'existing_case_refs':[] if fresh else ['DAN-028','CONTROL-DAN028-P1'],'kind':'finite-native-observation' if fresh else 'inherited-reference-only','requirements':['REQ-DEVICE-ANALOG-004'],'approved_review_pointer':f'#/approved_summary/approved_points/{index}','approved_point':point,'native_expected':native,'fresh_waveform_prior':None,'portable_expected':None,'portable_comparator':None,'candidate_grade':None,'limits':'Only note-off data2 varies over 0..127 under status 0x80, key 60 and frame 35,270, with the fixed 203-word P1 / on-velocity 100 / eight modifiers 0 history. Fresh hashes equal approved inherited metadata only; no old audio read or general release, no-effect, dispatch, timing, public A1/A2, ARM/Apple, determinism, pitch, calibration or tolerance law. Parent, source, executable, floating-point and fsync limitations are inherited exactly from the approved review.'}

def catalog_check(catalog, joins, review):
    points = review['approved_summary']['approved_points']
    need(catalog['shared_input'] == review['approved_summary']['shared_input'], 'shared input')
    need([p['release_velocity_byte'] for p in points] == list(range(128)), 'approved universe')
    need(len(catalog['catalog']) == len(joins['joins']) == 128, 'whole catalog')
    for i, point in enumerate(points):
        k = point['release_velocity_byte']; fresh = k != 64
        case_id = None if not fresh else f'DAN-{345+k if k<64 else 344+k:03}'
        item = expected(point, i, case_id)
        need(catalog['catalog'][i] == item, 'case ' + str(k))
        join = {'release_velocity_byte': k, 'case_id': case_id, 'existing_case_refs': item['existing_case_refs'],
                'approved_review_pointer': item['approved_review_pointer'], 'fresh_observation': fresh, 'owner_original_calls': 0}
        need(joins['joins'][i] == join, 'join ' + str(k))
    need(catalog['logical_points'] == 128 and catalog['fresh_cases'] == 127 and catalog['inherited_ref_count'] == 1, 'counts')

def old_catalog_check(data, baseline):
    items = data['catalog']
    need(len(items) == baseline['object_count'] and {str(i): sha(enc(x)) for i,x in enumerate(items)} == baseline['object_digests'], 'all old catalog objects')
    need([x['case_id'] for x in items if x['case_id'] is not None] == baseline['case_IDs'], 'old catalog IDs')

def controls(catalog, joins, review, before, after, baseline, old_catalogs):
    rejected=[]
    def reject(name,fn):
        try: fn()
        except (ValueError,KeyError,IndexError): rejected.append(name)
        else: raise AssertionError('negative accepted '+name)
    mutations=[('omit byte',lambda x,y:x['catalog'].pop()),
      ('duplicate byte',lambda x,y:x['catalog'].__setitem__(1,copy.deepcopy(x['catalog'][0]))),
      ('wrong ID',lambda x,y:x['catalog'][0].update(case_id='DAN-344')),
      ('inherited64 new ID',lambda x,y:x['catalog'][64].update(case_id='DAN-409')),
      ('inherited64 wrong ref',lambda x,y:x['catalog'][64].update(existing_case_refs=['DAN-203'])),
      ('invent inherited PID',lambda x,y:x['catalog'][64]['approved_point'].update(pid=1)),
      ('changed native hash',lambda x,y:x['catalog'][0]['native_expected']['original_output'].update(sha256='0'*64)),
      ('erase right metric',lambda x,y:x['catalog'][0]['native_expected']['descriptive_both_channel_metrics']['per_channel'].pop()),
      ('changed203word',lambda x,y:x['shared_input']['parameter_words'][99].update(f32_le='00000000')),
      ('changed offdata2',lambda x,y:x['catalog'][0]['approved_point']['events'][1].update(velocity=64)),
      ('invent portable',lambda x,y:x['catalog'][0].update(portable_comparator='exact')),
      ('rewriteNULLprior',lambda x,y:x['catalog'][0].update(fresh_waveform_prior='fitted')),
      ('invent grade',lambda x,y:x['catalog'][0].update(candidate_grade='PASS')),
      ('wrong join',lambda x,y:y['joins'][0].update(approved_review_pointer='#/wrong')),
      ('invent ownercall',lambda x,y:y['joins'][0].update(owner_original_calls=1)),
      ('erase launcher qualifier',lambda x,y:x['shared_input']['parent_receipt'].update(scope='OS proved'))]
    for name, edit in mutations:
        x,y=copy.deepcopy(catalog),copy.deepcopy(joins);edit(x,y)
        reject(name,lambda:catalog_check(x,y,review))
    for name,old,new in [('change otherREQ','Live sends 203 host values.','Live sends 202 host values.'),
      ('lose old004prefix','Release velocity has no effect.','Release velocity has new effect.'),
      ('change row','| DAN-001 |','| DAN-999 |'),
      ('change tolerance','0.05 dB; mean (DC)','0.5 dB; mean (DC)'),
      ('change oldR6 annex','Fifteen fresh output','Fourteen fresh output')]:
        need(old in after,'control anchor');reject(name,lambda old=old,new=new:preservation(before,after.replace(old,new,1),baseline))
    for name,data in old_catalogs.items():
        bad=copy.deepcopy(data);bad['catalog'].pop()
        reject('omit oldcatalog '+name,lambda:old_catalog_check(bad,baseline['old_catalogs'][name]))
    reject('actual packet access',lambda:read(P.parent/'batch-analog-release-velocity-bytes-v1/manifest.json'))
    return rejected

def check():
    baseline, delta, catalog, joins = [load(n) for n in ['baseline.json', 'owner-delta.json', 'cases128.json', 'joins128.json']]
    before = verify(baseline['owner_before']).decode()
    need(baseline['approved_review'] == catalog['approved_review'] == joins['approved_review'], 'review pins')
    review = json.loads(verify(baseline['approved_review']))
    need(review['blocking_findings'] == [] and review['packet']['manifest']['sha256'] == '474c76d0837ff10f70e49be3cb6d741ebd976d7c6754d619921debb8a8586f1f', 'approved authority')
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
    need(old_ids == set(baseline['old_IDs']) == {f'DAN-{i:03}' for i in range(1,345)}, '344 prior IDs')
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
            'composed_owner': delta['owner_after'], 'reverse_to_R6_exact': True,
            'whole_other_bodies_exact': 22, 'old004prefix_exact': True,
            'old_rows_exact': 67, 'old_IDs_exact': 344, 'new_IDs': 127, 'total_navigation_IDs': 471,
            'R3objects_exact': 28, 'R4catalog_exact': 128, 'R5catalog_exact': 128, 'R6catalog_exact': 16,
            'old_acceptance_annexes_prefix_exact': True, 'released_groups_evaluations': [38,42],
            'catalog': 128, 'inherited_reference_only': 1, 'negative_controls_pass': negatives,
            'actual_packet_reads': 0, 'original_calls': 0}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true', required=True)
    parser.parse_args()
    print(json.dumps(check(), indent=2))
