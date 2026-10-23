#!/usr/bin/env python3
"""Only staged owner data plus pinned approved summary/old owner/release metadata."""
import argparse, copy, hashlib, json, pathlib, re
P = pathlib.Path(__file__).resolve().parent
ROOT = P.parents[3]
ALLOWED = {ROOT / n for n in [
    'wiki/specs/device-analog.md',
    'analysis/ableton-live-12.4.3/full-spec-v1/reviews/analog-transpose-integers-v1-review.json',
    'analysis/ableton-live-12.4.3/full-spec-v1/reviews/analog-kind3-host-domains-v1-review.json',
    'analysis/ableton-live-12.4.3/full-spec-v1/owner-analog-r3-finite-v1/case-aliases.json',
    'analysis/ableton-live-12.4.3/full-spec-v1/owner-analog-r4-velocity-finite-v1/cases128.json',
    'analysis/ableton-live-12.4.3/full-spec-v1/owner-analog-r5-note-keys-finite-v1/cases128.json',
    'analysis/ableton-live-12.4.3/full-spec-v1/owner-analog-r6-channel-finite-v1/cases16.json',
    'analysis/ableton-live-12.4.3/full-spec-v1/owner-analog-r7-release-velocity-finite-v1/cases128.json',
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
            need(new[key].startswith(old[key]), 'old003 prefix')
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

def make_catalogs(tr,kr):
 ts=tr['approved_summary'];ks=kr['approved_summary'];q=copy.deepcopy(ks['shared_input']['Transpose_stale_label_qualification'])
 cases=[];trans=[];tids={};kinds=[];aliases=[]
 for i,p in enumerate(ts['approved_points']):
  v=p['transpose_integer'];fresh=v!=12;cid=None if not fresh else f'DAN-{472+v if v<12 else 471+v:03}';ref=cid or 'DAN-028';tids[v]=ref
  if fresh:
   cases.append({'case_id':cid,'kind':'finite-native-observation','source_class':'Transpose25','requirements':['REQ-DEVICE-ANALOG-003'],'host_index':4,'host_value':v,'vector_sha256':p['parameter_vector_sha256'],'approved_review':'Transpose','approved_review_pointer':f'#/approved_summary/approved_points/{i}','approved_point':p,'native_expected':{'original_output':p['audio'],'word_summary':p['native_output_summary']},'measurement_only_auxiliary':False,'historical_Transpose_label_qualification':q,'fresh_waveform_prior':None,'portable_expected':None,'portable_comparator':None,'candidate_grade':None})
  trans.append({'host_index':4,'host_value':v,'case_ref':ref,'new_case_id':cid,'kind':'new-finite-observation' if fresh else 'inherited-reference-only','existing_refs':[] if fresh else ['DAN-028','CONTROL-DAN028-P1'],'approved_review_pointer':f'#/approved_summary/approved_points/{i}','new_original_calls_by_owner':0,'new_inherited_receipt':None,'historical_Transpose_label_qualification':q})
 fresh_count=0;byhash={}
 for i,z in enumerate(ks['approved_vectors']):
  prov=z['provenance'];new_case=None
  if prov=='fresh-selected':
   cid=f'DAN-{496+fresh_count:03}';fresh_count+=1;new_case=cid
   a=z['actual'];cases.append({'case_id':cid,'kind':'finite-native-observation','source_class':'kind3-208','requirements':['REQ-DEVICE-ANALOG-003'],'host_index':z['changed_host_index'],'host_value':z['changed_host_value'],'vector_sha256':z['vector_sha256'],'approved_review':'kind3','approved_review_pointer':f'#/approved_summary/approved_vectors/{i}','approved_point':z,'native_expected':{'original_output':a['audio'],'word_summary':a['native_output_summary']},'measurement_only_auxiliary':z['measurement_only_auxiliary'],'historical_Transpose_label_qualification':q,'fresh_waveform_prior':None,'portable_expected':None,'portable_comparator':None,'candidate_grade':None})
  elif prov=='baseline':cid='DAN-028'
  elif prov=='Transpose-approved':cid=tids[z['changed_host_value']]
  elif prov=='R3-mode':cid=z['historical']['id']
  elif prov=='released-DAN029':cid='DAN-029'
  else:raise ValueError('unsupported inherited provenance')
  item={'vector_sha256':z['vector_sha256'],'host_index':z['changed_host_index'],'host_value':z['changed_host_value'],'case_ref':cid,'new_kind3_case_id':new_case,'provenance_in_kind3_batch':prov,'fresh_in_kind3_batch':prov=='fresh-selected','new_case_in_this_proposal':int(cid.split('-')[1])>=472,'measurement_only_auxiliary':z['measurement_only_auxiliary'],'approved_review_pointer':f'#/approved_summary/approved_vectors/{i}','inherited_reference_metadata':z['historical'],'historical_Transpose_label_qualification':q,'new_original_calls_by_owner':0,'portable_comparator':None,'candidate_grade':None};kinds.append(item);byhash[z['vector_sha256']]=item
 for i,a in enumerate(ks['approved_aliases']):
  item=byhash[a['vector_sha256']];aliases.append({**a,'case_ref':item['case_ref'],'new_kind3_case_id':item['new_kind3_case_id'],'reference_provenance':item['provenance_in_kind3_batch'],'vector_catalog_pointer':item['approved_review_pointer'],'historical_Transpose_label_qualification':q,'new_original_calls_by_owner':0})
 assert len(cases)==232 and len(trans)==25 and len(kinds)==254 and len(aliases)==338 and fresh_count==208
 assert [x['case_id'] for x in cases]==[f'DAN-{i:03}' for i in range(472,704)]
 return ({'schema':'analog-r8-native-finite-cases-v1','new_case_count':232,'portable_grade_admission':False,'shared_inputs':{'Transpose':ts['shared_input'],'kind3':ks['shared_input']},'cases':cases},
 {'schema':'analog-r8-whole25-Transpose-joins-v1','logical_points':25,'new_cases':24,'inherited_baseline_refs':1,'catalog':trans},
 {'schema':'analog-r8-whole338-alias254-vector-joins-v1','aliases':aliases,'vectors':kinds,'logical_aliases':338,'unique_vectors':254,'new_kind3_cases':208,'new_Transpose_references':24,'old_reference_vectors':22,'new_original_calls_by_owner':0},
 {'schema':'analog-r8-new232-case-review-joins-v1','joins':[{'case_id':x['case_id'],'approved_review':x['approved_review'],'approved_review_pointer':x['approved_review_pointer'],'vector_sha256':x['vector_sha256'],'source_class':x['source_class'],'owner_original_calls':0,'historical_Transpose_label_qualification':q} for x in cases]})
def old_catalog_check(data, baseline):
    items = data['catalog']
    need(len(items) == baseline['object_count'] and {str(i): sha(enc(x)) for i,x in enumerate(items)} == baseline['object_digests'], 'all old catalog objects')
    need([x['case_id'] for x in items if x['case_id'] is not None] == baseline['case_IDs'], 'old catalog IDs')

def catalog_check(actual, expected):
    need(actual == expected, 'complete reviewed mappings/native identities/NULLs/qualifications')

def controls(data, expected, before, after, baseline, old_catalogs):
    rejected=[]
    def reject(name,fn):
        try:fn()
        except (ValueError,KeyError,IndexError):rejected.append(name)
        else:raise AssertionError('negative accepted '+name)
    edits=[
      ('omit fresh case',lambda d:d[0]['cases'].pop()),
      ('duplicate ID',lambda d:d[0]['cases'][1].update(case_id='DAN-472')),
      ('wrong kind3 ID',lambda d:d[0]['cases'][24].update(case_id='DAN-495')),
      ('wrong native hash',lambda d:d[0]['cases'][0]['native_expected']['original_output'].update(sha256='0'*64)),
      ('erase native summary',lambda d:d[0]['cases'][0]['native_expected'].pop('word_summary')),
      ('invent portable expected',lambda d:d[0]['cases'][0].update(portable_expected=0)),
      ('invent comparator',lambda d:d[0]['cases'][0].update(portable_comparator='exact')),
      ('invent grade',lambda d:d[0]['cases'][0].update(candidate_grade='PASS')),
      ('rewrite NULL prior',lambda d:d[0]['cases'][0].update(fresh_waveform_prior='fitted')),
      ('erase auxiliary qualification',lambda d:next(x for x in d[0]['cases'] if x['measurement_only_auxiliary']).update(measurement_only_auxiliary=False)),
      ('erase stale label qualifier',lambda d:d[0]['cases'][0].update(historical_Transpose_label_qualification=None)),
      ('change source pointer',lambda d:d[0]['cases'][0].update(approved_review_pointer='#/wrong')),
      ('wrong selected host word',lambda d:d[0]['cases'][0].update(host_index=5)),
      ('wrong vector identity',lambda d:d[0]['cases'][0].update(vector_sha256='0'*64)),
      ('missing Transpose point',lambda d:d[1]['catalog'].pop()),
      ('invent baseline ID',lambda d:d[1]['catalog'][12].update(new_case_id='DAN-704')),
      ('invent inherited receipt',lambda d:d[1]['catalog'][12].update(new_inherited_receipt={'pid':1})),
      ('wrong baseline reference',lambda d:d[1]['catalog'][12].update(case_ref='DAN-472')),
      ('missing alias',lambda d:d[2]['aliases'].pop()),
      ('wrong alias join',lambda d:d[2]['aliases'][0].update(case_ref='DAN-999')),
      ('duplicate vector',lambda d:d[2]['vectors'].__setitem__(1,copy.deepcopy(d[2]['vectors'][0]))),
      ('duplicate Transpose case',lambda d:next(x for x in d[2]['vectors'] if x['provenance_in_kind3_batch']=='Transpose-approved').update(new_kind3_case_id='DAN-704')),
      ('invent owner calls',lambda d:d[2].update(new_original_calls_by_owner=1)),
      ('wrong new join',lambda d:d[3]['joins'][0].update(approved_review='kind3')),
      ('omit joined qualifier',lambda d:d[3]['joins'][0].pop('historical_Transpose_label_qualification'))]
    for name,edit in edits:
        bad=copy.deepcopy(data);edit(bad)
        need(bad!=data,'meaningful negative '+name)
        reject(name,lambda:catalog_check(bad,expected))
    for name,old,new in [
      ('change other wholeREQ','Live sends 203 host values.','Live sends 202 host values.'),
      ('change old003 prefix',next(x for x in bodies(before)['REQ-DEVICE-ANALOG-003'].splitlines()[1:] if x.strip()), 'altered old parameter clause'),
      ('change old row','| DAN-001 |','| DAN-999 |'),
      ('change tolerance','0.05 dB; mean (DC)','0.5 dB; mean (DC)'),
      ('change old annex','Fifteen fresh output','Fourteen fresh output')]:
        need(old and old in after,'preservation control anchor '+name)
        reject(name,lambda old=old,new=new:preservation(before,after.replace(old,new,1),baseline))
    for name,item in old_catalogs.items():
        bad=copy.deepcopy(item);bad['catalog'].pop()
        reject('omit old catalog '+name,lambda:old_catalog_check(bad,baseline['old_catalogs'][name]))
    for name in ['batch-analog-transpose-integers-v1','batch-analog-kind3-host-domains-v1']:
        reject('refuse actual '+name,lambda name=name:read(P.parent/name/'manifest.json'))
    return rejected

def check():
    baseline,delta=load('baseline.json'),load('owner-delta.json')
    data=[load(n) for n in ['cases232.json','transpose-catalog25.json','kind3-catalog338.json','joins232.json']]
    before=verify(baseline['owner_before']).decode()
    reviews={name:json.loads(verify(pin)) for name,pin in baseline['approved_reviews'].items()}
    need(all(x['blocking_findings']==[] and x['disposition']=='APPROVED_BOUNDED_ACTUAL_SOURCE' for x in reviews.values()),'approved summaries')
    expected=list(make_catalogs(reviews['Transpose'],reviews['kind3']))
    expected[0]['approved_reviews']=baseline['approved_reviews']
    catalog_check(data,expected)
    after=compose(before,delta)
    need(sig(after)=={k:delta['owner_after'][k] for k in ['bytes','sha256']},'target identity')
    need(compose(after,delta,True)==before,'full reverse to R7')
    preservation(before,after,baseline)
    aliases=json.loads(verify(baseline['R3_aliases']))
    need({x['id']:sha(enc(x)) for x in aliases['cases']}==baseline['R3_objects'] and len(aliases['cases'])==28,'R3 objects')
    need(sha(enc(aliases['baseline_control']))==baseline['R3_control'],'R3 control')
    old_catalogs={};old_ids={f'DAN-{i:03}' for i in range(1,48)}|{x['id'] for x in aliases['cases']}
    for name,item in baseline['old_catalogs'].items():
        old_catalogs[name]=json.loads(verify(item['pin']));old_catalog_check(old_catalogs[name],item);old_ids.update(item['case_IDs'])
    need(old_ids==set(baseline['old_IDs'])=={f'DAN-{i:03}' for i in range(1,472)},'471 prior IDs')
    release=json.loads(verify(baseline['release_manifest']))
    need(release['files']==baseline['release_inventory'] and release['case_count']==38 and release['evaluation_count']==42,'released metadata')
    negatives=controls(data,expected,before,after,baseline,old_catalogs)
    if (P/'manifest.json').exists():
        manifest=load('manifest.json')
        need({x.name for x in P.iterdir() if x.is_file()}=={'manifest.json'}|{x['path'] for x in manifest['payloads']},'sealed tree')
        for item in manifest['payloads']:
            raw=read(P/item['path']);need(len(raw)==item['bytes'] and sha(raw)==item['sha256'],'sealed payload')
    return {'status':'PASS','scope':'New wording/mapping/IDs/preservation only; approved observations inherited',
      'composed_owner':delta['owner_after'],'reverse_to_R7_exact':True,'whole_other_bodies_exact':22,
      'old003prefix_exact':True,'old_rows_exact':67,'old_IDs_exact':471,'new_IDs':232,'total_navigation_IDs':703,
      'R3objects_exact':28,'old_catalogs_exact':{'R4':128,'R5':128,'R6':16,'R7':128},
      'old_acceptance_annexes_prefix_exact':True,'released_groups_evaluations':[38,42],
      'Transpose_catalog':25,'kind3_aliases':338,'kind3_vectors':254,'new_Transpose':24,'new_kind3':208,
      'negative_controls_pass':negatives,'actual_packet_reads':0,'original_calls':0}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true',required=True);parser.parse_args()
    print(json.dumps(check(),indent=2))
