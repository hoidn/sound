#!/usr/bin/env python3
"""Owner-only staged data and named approved-summary/old-owner/release metadata."""
from pathlib import Path
import argparse, copy, hashlib, json, re, struct
P=Path(__file__).resolve().parent
ROOT=P.parents[3]
ALLOWED={ROOT/x for x in [
 'wiki/specs/device-tension.md',
 'analysis/ableton-live-12.4.3/full-spec-v1/reviews/tension-note-keys-v1-review.json',
 'analysis/ableton-live-12.4.3/full-spec-v1/owner-tension-r3-retained-v1/adoption-map.json',
 'analysis/ableton-live-12.4.3/full-spec-v1/owner-tension-r4-sensitivity-v1/adoption-map.json',
 'analysis/ableton-live-12.4.3/full-spec-v1/owner-tension-r5-velocity-finite-v1/cases128.json',
 'handoff/device-tension-v1/manifest.json']}
def need(x,why):
 if not x:raise ValueError(why)
def read(path):
 path=Path(path).resolve();need(path.parent==P or path in ALLOWED,'refuse outside staged/approved metadata');return path.read_bytes()
def load(name):return json.loads(read(P/name))
def sha(raw):return hashlib.sha256(raw).hexdigest()
def enc(x):return (json.dumps(x,indent=2,ensure_ascii=False)+'\n').encode()
def sig(text):return {'bytes':len(text.encode()),'sha256':sha(text.encode())}
def verify(pin):
 raw=read(ROOT/pin['path']);need(len(raw)==pin['bytes'] and sha(raw)==pin['sha256'],'pin '+pin['path']);return raw

def bodies(text):return {m[1]:m[0] for m in re.finditer(r'^### (REQ-DEVICE-TENSION-\d{3})[^\n]*\n.*?(?=^### REQ-|^## |\Z)',text,re.M|re.S)}
def sections(text):return {m[1]:m[0] for m in re.finditer(r'^## ([^\n]+)\n.*?(?=^## |\Z)',text,re.M|re.S)}
def compose(text,delta,reverse=False):
 for item in (list(reversed(delta['replacements'])) if reverse else delta['replacements']):
  old,new=(item['new'],item['old']) if reverse else (item['old'],item['new']);need(text.count(old)==1,'unique '+item['label']);text=text.replace(old,new,1)
 return text

def preserve(before,after,b):
 old,new=bodies(before),bodies(after);need(len(old)==len(new)==15 and old.keys()==new.keys(),'REQ universe')
 need({k:sig(v) for k,v in old.items()}==b['requirement_bodies'],'prior bodies')
 for k,v in old.items():need(new[k].startswith(v) if k=='REQ-DEVICE-TENSION-003' else new[k]==v,'prior body '+k)
 need([x for x in before.splitlines() if x.startswith('| DTN-')]==[x for x in after.splitlines() if x.startswith('| DTN-')]==b['old_rows'] and len(b['old_rows'])==42,'42 oldrows')
 a,z=sections(before),sections(after)
 for k,v in b['protected_sections'].items():need(sig(a[k])==sig(z[k])==v,'protected '+k)
 need(sig(a['Acceptance cases'])==b['old_acceptance_prefix'] and z['Acceptance cases'].startswith(a['Acceptance cases']),'allold Acceptanceprefix')
 release=lambda text:text[text.index('The [finite handoff plan]'):text.index('## Tension guarded getter qualification')]
 need(sig(release(before))==sig(release(after))==b['release_prose'],'releaseprose')

def expected(point,key,cid):
 fresh=key not in {36,48,60,72,84};refs=[] if fresh else ['DTN-001' if key==60 else 'DTN-004']
 native={'original_output':point['output'],'native_unsigned_summary':point['observed_unsigned_summary']} if fresh else {'historical_metadata':point['inherited_control'],'no_new_measurement':True}
 return {'note_key':key,'case_id':cid,'existing_case_refs':refs,'kind':'finite-native-observation' if fresh else 'inherited-reference-only','requirements':['REQ-DEVICE-TENSION-003'],'context_requirements':['REQ-DEVICE-TENSION-004','REQ-DEVICE-TENSION-007'],'approved_review_pointer':f'#/approved_summary/approved_points/{key}','approved_point':point,'native_expected':native,'fresh_waveform_prior':None,'portable_expected':None,'portable_comparator':None,'candidate_grade':None,'review_qualifications_pointer':'#/review_qualifications','limits':'Only matching on/off note keys vary in exact constructor-default129word / velocity100 / rate44100 / noteon4096off26146 / 44100frames512 history. No broader timing, range, pitch/f0, clamp/alias, velocity, comparator, calibration, physical, publicA1A2 or ARM/Apple law. Prior velocity parent-binding gap remains unchanged.'}
def mapping(c,j,review):
 s=review['approved_summary'];need(c['shared_input']==s['shared_input'] and c['review_qualifications']==review['qualifications'],'approvedshared andqualifications')
 need(len(c['catalog'])==len(j['joins'])==len(s['approved_points'])==128,'whole128')
 need((c['logical_points'],c['fresh_cases'],c['inherited_references'])==(128,123,5),'123+5counts')
 number=168
 for key,point in enumerate(s['approved_points']):
  fresh=key not in {36,48,60,72,84};need(point['note_key']==key and (point['provenance']=='fresh-once-only')==fresh,'provenance')
  cid=f'DTN-{number:03d}' if fresh else None
  if fresh:number+=1
  item=expected(point,key,cid);need(c['catalog'][key]==item,'catalog '+str(key))
  need(j['joins'][key]=={'note_key':key,'case_id':cid,'existing_case_refs':item['existing_case_refs'],'approved_review_pointer':item['approved_review_pointer'],'fresh_observation':fresh,'owner_new_original_calls':0},'join '+str(key))
  if fresh:
   ev=point['input_events'];need(ev==[{'frame':f,'status':st,'key':key,'velocity':v,'packed16_le_hex':struct.pack('<qBBBB4x',f,st,key,v,0).hex()} for f,st,v in [(4096,144,100),(26146,128,0)]],'fresh eventbytes')
  else:
   ctrl=point['inherited_control'];need(ctrl['input_projection']['events']==[[4096,144,key,100],[26146,128,key,0]],'old events')
   need(ctrl['fresh_pid'] is ctrl['fresh_receipt'] is ctrl['new_descriptive_metrics'] is None and point['fresh_receipt'] is None,'no inventedoldfacts')
 need(number==291,'DTN168 through290')

def wording(delta):
 text=' '.join(' '.join(x['new'] for x in delta['replacements']).split())
 for token in ['123 finite **X native observations**','No general note range','REQ-007 remains unchanged velocity context','122 distinct fresh output hashes','not retroactively repaired','not continuous provider/build/interpreter/OS-exec','All 167 earlier IDs','portable expected outputs, comparators and candidate grades remain NULL','27 released evaluations remain unchanged','actual/source/raw/numeric proof is inherited without replay']:
  need(token in text,'boundedwording '+token)

def old_catalog(data,b):
 need(len(data['catalog'])==b['object_count']==128,'old128')
 need({str(i):sha(enc(x)) for i,x in enumerate(data['catalog'])}==b['object_digests'],'alloldobjects')
 need([x['case_id'] for x in data['catalog'] if x['case_id'] is not None]==b['case_IDs'],'old125IDs')
 need(data['bookkeeping_qualifications']==b['bookkeeping_qualifications'] and data['bookkeeping_qualifications']['parent_pre_call_file_bound'] is False,'oldervelocityparentgap')

def controls(c,j,r,before,after,b,old,delta):
 rejected=[]
 def reject(name,fn):
  try:fn()
  except (ValueError,KeyError,IndexError,struct.error):rejected.append(name)
  else:raise AssertionError('negativeaccepted '+name)
 def mutate(name,fn):
  x,y=copy.deepcopy(c),copy.deepcopy(j);fn(x,y);reject(name,lambda:mapping(x,y,r))
 mutate('wrong127freshcount',lambda x,y:x.update(fresh_cases=127))
 mutate('omit key127',lambda x,y:x['catalog'].pop())
 mutate('duplicate key',lambda x,y:x['catalog'].__setitem__(1,copy.deepcopy(x['catalog'][0])))
 mutate('reuse oldID167',lambda x,y:x['catalog'][0].update(case_id='DTN-167'))
 mutate('inherited36 newID',lambda x,y:x['catalog'][36].update(case_id='DTN-204'))
 mutate('wrong60ref',lambda x,y:x['catalog'][60].update(existing_case_refs=['DTN-004']))
 mutate('invent oldPID',lambda x,y:x['catalog'][84]['approved_point']['inherited_control'].update(fresh_pid=1))
 mutate('invent oldmetrics',lambda x,y:x['catalog'][48]['approved_point']['inherited_control'].update(new_descriptive_metrics={'rms':1}))
 mutate('change nativehash',lambda x,y:x['catalog'][0]['native_expected']['original_output'].update(sha256='0'*64))
 mutate('erase secondchannel',lambda x,y:x['catalog'][0]['native_expected']['native_unsigned_summary']['nonzero_sample_counts'].pop())
 mutate('change fixedword',lambda x,y:x['shared_input']['words'][0].update(little_endian_hex='00000000'))
 mutate('offkey mismatch',lambda x,y:x['catalog'][0]['approved_point']['input_events'][1].update(key=1))
 mutate('portable waveform',lambda x,y:x['catalog'][0].update(portable_expected='hash'))
 mutate('new comparator',lambda x,y:x['catalog'][0].update(portable_comparator='exact'))
 mutate('prior fit',lambda x,y:x['catalog'][0].update(fresh_waveform_prior='fitted'))
 mutate('gradepass',lambda x,y:x['catalog'][0].update(candidate_grade='PASS'))
 mutate('wrongapprovedpointer',lambda x,y:y['joins'][0].update(approved_review_pointer='#/wrong'))
 mutate('ownernewcall',lambda x,y:y['joins'][0].update(owner_new_original_calls=1))
 for name,a,z in [('otherbody','Live sends indices 0 to 129 except 2','Live sends indices 0 to 128 except 2'),('003prefix','A note-on with velocity 0 acts as a note-off.','A general new velocity rule.'),('007body','Other velocity amounts remain U.','Other velocity amounts now pass.'),('oldrow','| DTN-001 |','| DTN-999 |'),('oldmargin','3.16792297039e-05','3e-05'),('release','27 calibrated finite output evaluations only.','28 calibrated finite output evaluations only.')]:
  need(a in after,'controlanchor '+name);reject('modify '+name,lambda a=a,z=z:preserve(before,after.replace(a,z,1),b))
 bad=copy.deepcopy(old);bad['bookkeeping_qualifications']['parent_pre_call_file_bound']=True;reject('retroactivelyclosevelocityparentgap',lambda:old_catalog(bad,b['R5_catalog']))
 bad=copy.deepcopy(old);bad['catalog'].pop();reject('omitoldR5object',lambda:old_catalog(bad,b['R5_catalog']))
 for token in ['not retroactively repaired','123 finite **X native observations**','27 released evaluations remain unchanged']:
  bad=copy.deepcopy(delta)
  for x in bad['replacements']:x['new']=x['new'].replace(token,'')
  reject('erase '+token,lambda bad=bad:wording(bad))
 reject('actualpacketaccess',lambda:read(P.parent/'batch-tension-note-keys-v1/manifest.json'))
 reject('old222actualaccess',lambda:read(P.parent/'batch-tension-uncalibrated-sensitivity-v1/manifest.json'))
 return rejected

def check():
 b,d,c,j=[load(n) for n in ['baseline.json','owner-delta.json','cases128.json','joins128.json']]
 before=verify(b['owner_before']).decode();need(b['approved_review']==c['approved_review']==j['approved_review'],'reviewpins')
 review=json.loads(verify(b['approved_review']));need(review['blocking_findings']==review['required_corrections']==[] and review['disposition'].startswith('APPROVED'),'sole actualapproval')
 after=compose(before,d);need(sig(after)=={k:d['owner_after'][k] for k in ['bytes','sha256']},'target');need(compose(after,d,True)==before,'reverse');preserve(before,after,b);mapping(c,j,review);wording(d)
 mapcounts={}
 for name,item in b['retained_owner_maps'].items():
  data=json.loads(verify(item['pin']))[item['collection_key']];digest={str(i):sha(enc(x)) for i,x in enumerate(data)} if isinstance(data,list) else {k:sha(enc(v)) for k,v in data.items()};need(len(data)==item['object_count'] and digest==item['object_digests'],'oldmap');mapcounts[name]=len(data)
 old=json.loads(verify(b['R5_catalog']['pin']));old_catalog(old,b['R5_catalog']);need(b['old_IDs']==[f'DTN-{i:03d}' for i in range(1,168)] and [f'DTN-{i:03d}' for i in range(43,168)]==b['R5_catalog']['case_IDs'],'167oldIDs')
 release=json.loads(verify(b['release_manifest']));need(release['files']==b['release_inventory'] and len(release['files'])==35 and release['case_count']==release['evaluation_count']==27,'release metadata')
 negatives=controls(c,j,review,before,after,b,old,d)
 for x in d['replacements']:
  for target in re.findall(r'\]\(([^)]+)\)',x['new']):need((ROOT/'wiki/specs'/target.split('#')[0]).resolve().exists(),'newlink')
 if (P/'manifest.json').exists():
  m=load('manifest.json');need({x.name for x in P.iterdir() if x.is_file()}=={'manifest.json'}|{x['path'] for x in m['payloads']},'exactsealedtree')
  for item in m['payloads']:raw=read(P/item['path']);need(len(raw)==item['bytes'] and sha(raw)==item['sha256'],'sealedpayload')
 return {'status':'PASS','scope':'NEW owner wording/mapping/IDs/preservation ONLY; approvedactualsummary inherited','target':d['owner_after'],'reverse_to_R5_exact':True,'whole_other_bodies_exact':14,'REQ004_007_whole_exact':True,'old003prefix_exact':True,'old_rows_exact':42,'old_IDs_exact':167,'new_IDs':123,'new_ID_range':['DTN-168','DTN-290'],'full_catalog':128,'inherited_references':5,'total_navigation_IDs':290,'retained_owner_map_counts':mapcounts,'R5_catalog_exact':128,'old_velocity_parent_gap_preserved':True,'old_acceptance_prefix_exact':True,'release_evaluations':27,'release_inventory_entries':35,'negative_controls':negatives,'actual_packet_reads':0,'numeric_metric_recomputations':0,'original_calls':0}
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true',required=True);parser.parse_args();print(json.dumps(check(),indent=2))
