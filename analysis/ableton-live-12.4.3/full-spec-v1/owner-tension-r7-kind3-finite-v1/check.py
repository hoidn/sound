#!/usr/bin/env python3
"""Staged owner/approved summary/old owner/release MANIFEST only; never actuals."""
from pathlib import Path
import argparse,json,hashlib,re,copy
P=Path(__file__).resolve().parent;ROOT=P.parents[3]
ALLOWED={ROOT/x for x in ['wiki/specs/device-tension.md','analysis/ableton-live-12.4.3/full-spec-v1/reviews/tension-kind3-host-domains-v1-review.json','analysis/ableton-live-12.4.3/full-spec-v1/owner-tension-r3-retained-v1/adoption-map.json','analysis/ableton-live-12.4.3/full-spec-v1/owner-tension-r4-sensitivity-v1/adoption-map.json','analysis/ableton-live-12.4.3/full-spec-v1/owner-tension-r5-velocity-finite-v1/cases128.json','analysis/ableton-live-12.4.3/full-spec-v1/owner-tension-r6-note-keys-finite-v1/cases128.json','handoff/device-tension-v1/manifest.json']}
def need(x,why):
 if not x:raise ValueError(why)
def read(path):
 path=Path(path).resolve();need(path.parent==P or path in ALLOWED,'refuse outside staged/approved metadata');return path.read_bytes()
def load(n):return json.loads(read(P/n))
def sha(b):return hashlib.sha256(b).hexdigest()
def enc(x):return (json.dumps(x,indent=2,ensure_ascii=False)+'\n').encode()
def sig(t):return {'bytes':len(t.encode()),'sha256':sha(t.encode())}
def verify(pin):
 raw=read(ROOT/pin['path']);need(len(raw)==pin['bytes'] and sha(raw)==pin['sha256'],'pin '+pin['path']);return raw
def bodies(t):return {x[1]:x[0] for x in re.finditer(r'^### (REQ-DEVICE-TENSION-\d{3})[^\n]*\n.*?(?=^### REQ-|^## |\Z)',t,re.M|re.S)}
def sections(t):return {x[1]:x[0] for x in re.finditer(r'^## ([^\n]+)\n.*?(?=^## |\Z)',t,re.M|re.S)}
def compose(t,d,reverse=False):
 for x in (list(reversed(d['replacements'])) if reverse else d['replacements']):
  a,z=(x['new'],x['old']) if reverse else (x['old'],x['new']);need(t.count(a)==1,'unique '+x['label']);t=t.replace(a,z,1)
 return t

def preserve(before,after,b):
 old,new=bodies(before),bodies(after);need(len(old)==len(new)==15 and old.keys()==new.keys(),'15REQ')
 need({k:sig(v) for k,v in old.items()}==b['requirement_bodies'],'baselinebodies')
 for k,v in old.items():need(new[k].startswith(v) if k.endswith('002') else new[k]==v,'priorbody '+k)
 need([x for x in before.splitlines() if x.startswith('| DTN-')]==[x for x in after.splitlines() if x.startswith('| DTN-')]==b['old_rows'] and len(b['old_rows'])==42,'old42rows')
 a,z=sections(before),sections(after)
 for k,v in b['protected_sections'].items():need(sig(a[k])==sig(z[k])==v,'protected '+k)
 need(sig(a['Acceptance cases'])==b['old_acceptance_prefix'] and z['Acceptance cases'].startswith(a['Acceptance cases']),'oldAcceptance')
 release=lambda t:t[t.index('The [finite handoff plan]'):t.index('## Tension guarded getter qualification')]
 need(sig(release(before))==sig(release(after))==b['release_prose'],'releaseprose')

REFS={'defaults_44':'DTN-001','exc_hammer':'DTN-007','exc_bounce':'DTN-008','exc_bow':'DTN-009','damper_on':'DTN-017','pickup_on':'DTN-020','term_on':'DTN-019','body_type_0':'DTN-022','body_type_1':'DTN-022','body_type_2':'DTN-022','body_type_3':'DTN-022'}
def mapping(c,j,r):
 s=r['approved_summary'];need(c['shared_input']==s['shared_input'] and c['input_vectors']==s['input_vectors'] and c['review_qualifications']==r['qualifications'],'approvedinputqualifications')
 need((c['logical_alias_points'],c['unique_vectors'],c['fresh_cases'],c['historical_input_references'],c['shared_baseline_aliases'],c['new_application_predicate_proofs'])==(164,117,106,11,48,0),'counts')
 need(len(c['catalog'])==len(s['approved_points'])==117 and len(j['joins'])==len(s['aliases'])==164,'wholeuniverse')
 number=291;aux=[];byid={}
 for i,(row,point,v) in enumerate(zip(c['catalog'],s['approved_points'],s['input_vectors'])):
  fresh=point['provenance']=='fresh-once-only';cid=f'DTN-{number:03d}' if fresh else None
  if fresh:number+=1
  boundary=v['domain_index']==91 and v['host_value']==5
  need(row['id']==point['id']==v['id'] and row['unique_vector']==i and row['domain_index']==v['domain_index'] and row['host_value']==v['host_value'],'vectorjoin')
  need(row['approved_point']==point and row['approved_review_pointer']==f'#/approved_summary/approved_points/{i}' and row['input_vector_pointer']==f'#/input_vectors/{i}','approvedpoint')
  need(row['case_id']==cid and row['new_application_predicate_proof'] is False,'IDs/notappgrade')
  need(row['requirements']==([] if boundary else ['REQ-DEVICE-TENSION-002']) and row['navigation_context']=='REQ-DEVICE-TENSION-002','boundarynotapplicationpredicate')
  need(row['evidence_role']==('auxiliary-native-host-boundary' if boundary else 'finite-native-host-navigation'),'role')
  need(row['old_recipe_bridge_remains_U']==v.get('prior_recipe_only',False),'oldrecipeU')
  need(row['fresh_waveform_prior'] is row['portable_expected'] is row['portable_comparator'] is row['candidate_grade'] is None,'NULLcriteria')
  if fresh:
   need(row['kind']=='finite-native-observation' and row['existing_case_refs']==[],'freshkind')
   need(row['native_expected']=={'original_output':point['output'],'native_unsigned_summary':point['observed_unsigned_summary']},'nativefacts')
  else:
   h=point['historical_input_reference'];need(row['kind']=='historical-input-reference-only' and row['existing_case_refs']==[REFS[h['tag']]],'oldrefs')
   need(row['native_expected']=={'historical_input_metadata':h,'no_new_measurement':True} and point['fresh_pid'] is point['fresh_receipt'] is point['new_metrics'] is None,'nofabricatedold')
  if boundary:aux.append(cid)
  byid[row['id']]=row
 need(number==397 and aux==c['auxiliary_native_boundary_case_IDs']==['DTN-384'],'106IDs/oneboundary')
 for got,alias in zip(j['joins'],s['aliases']):
  row=byid[alias['unique_id']];need(got=={**alias,'case_id':row['case_id'],'existing_case_refs':row['existing_case_refs'],'evidence_role':row['evidence_role'],'new_application_predicate_proof':False,'owner_new_original_calls':0},'aliasjoin')
 need(sum(a['inherited_shared_baseline'] for a in j['joins'])==48 and len({a['unique_id'] for a in j['joins']})==117,'baselinededup')

def oldcatalog(data,meta):
 rows=data['catalog'];need(len(rows)==meta['object_count']==128 and {str(i):sha(enc(x)) for i,x in enumerate(rows)}==meta['object_digests'],'oldcatalogobjects')
 need([x['case_id'] for x in rows if x['case_id'] is not None]==meta['case_IDs'],'oldIDs')
 if 'bookkeeping_qualifications' in meta:need(data['bookkeeping_qualifications']==meta['bookkeeping_qualifications'] and data['bookkeeping_qualifications']['parent_pre_call_file_bound'] is False,'oldvelocitylaunchgap')
def wording(d):
 t=' '.join(' '.join(x['new'] for x in d['replacements']).split())
 for token in ['106 finite **X native observations**','eleven historical input references','not validation of Live','no application-predicate mapping','Three fresh members','does not retroactively repair','old velocity parent-launch file-binding/fsync gap is unchanged','portable expected outputs, comparators and candidate grades remain NULL','27 released evaluations / 35 release inventory entries remain unchanged','numeric proof is inherited from the sole approval without replay']:
  need(token in t,'boundedwording '+token)

def controls(c,j,r,before,after,b,old,d):
 out=[]
 def reject(name,fn):
  try:fn()
  except (ValueError,KeyError,IndexError):out.append(name)
  else:raise AssertionError('negativeaccepted '+name)
 def mutate(name,fn):
  x,y=copy.deepcopy(c),copy.deepcopy(j);fn(x,y);reject(name,lambda:mapping(x,y,r))
 mutate('omitvector',lambda x,y:x['catalog'].pop())
 mutate('omitalias',lambda x,y:y['joins'].pop())
 mutate('duplicatebaselinealias',lambda x,y:y['joins'].__setitem__(1,copy.deepcopy(y['joins'][0])))
 mutate('wrongfreshcount',lambda x,y:x.update(fresh_cases=117))
 mutate('reuseold290ID',lambda x,y:x['catalog'][1].update(case_id='DTN-290'))
 mutate('inventbaselineID',lambda x,y:x['catalog'][0].update(case_id='DTN-291'))
 mutate('oldpickupwrongtimingcase',lambda x,y:next(z for z in x['catalog'] if z['existing_case_refs']==['DTN-020']).update(existing_case_refs=['DTN-021']))
 mutate('inventoldPID',lambda x,y:x['catalog'][0]['approved_point'].update(fresh_pid=1))
 mutate('inventoldmetrics',lambda x,y:x['catalog'][0]['approved_point'].update(new_metrics={'rms':1}))
 mutate('boundarytoapplication',lambda x,y:next(z for z in x['catalog'] if z['case_id']=='DTN-384').update(requirements=['REQ-DEVICE-TENSION-002']))
 mutate('boundaryrolelost',lambda x,y:next(z for z in x['catalog'] if z['case_id']=='DTN-384').update(evidence_role='ordinaryLive'))
 mutate('othercaseapplicationgrade',lambda x,y:x['catalog'][1].update(new_application_predicate_proof=True))
 mutate('oldrecipebridgeclosed',lambda x,y:next(z for z in x['catalog'] if z['old_recipe_bridge_remains_U']).update(old_recipe_bridge_remains_U=False))
 mutate('nativehash',lambda x,y:x['catalog'][1]['native_expected']['original_output'].update(sha256='0'*64))
 mutate('rightchannelmetric',lambda x,y:x['catalog'][1]['native_expected']['native_unsigned_summary']['nonzero_sample_counts'].pop())
 mutate('portableexpected',lambda x,y:x['catalog'][1].update(portable_expected='hash'))
 mutate('portablecomparator',lambda x,y:x['catalog'][1].update(portable_comparator='exact'))
 mutate('waveformpriorfit',lambda x,y:x['catalog'][1].update(fresh_waveform_prior='tone'))
 mutate('candidatePASS',lambda x,y:x['catalog'][1].update(candidate_grade='PASS'))
 mutate('ownernewcall',lambda x,y:y['joins'][0].update(owner_new_original_calls=1))
 for name,a,z in [('002prefix','Live sends indices 0 to 129 except 2','Live sends indices 0 to 128 except 2'),('otherREQ','A note-on with velocity 0 acts as a note-off.','A new general velocity rule.'),('oldrow','| DTN-001 |','| DTN-999 |'),('oldR4margin','3.16792297039e-05','3e-05'),('oldR6key','There are 122 distinct fresh output hashes.','There are 123 distinct fresh output hashes.'),('release','27 calibrated finite output evaluations only.','28 calibrated finite output evaluations only.')]:
  need(a in after,'controlanchor '+name);reject('change '+name,lambda a=a,z=z:preserve(before,after.replace(a,z,1),b))
 for name,data in old.items():
  bad=copy.deepcopy(data);bad['catalog'].pop();reject('omitoldcatalog '+name,lambda bad=bad,name=name:oldcatalog(bad,b['old_catalogs'][name]))
 bad=copy.deepcopy(old['R5']);bad['bookkeeping_qualifications']['parent_pre_call_file_bound']=True;reject('retroactivelyfixoldvelocityparent',lambda:oldcatalog(bad,b['old_catalogs']['R5']))
 for token in ['not validation of Live','no application-predicate mapping','does not retroactively repair']:
  bad=copy.deepcopy(d)
  for x in bad['replacements']:x['new']=x['new'].replace(token,'')
  reject('erase '+token,lambda bad=bad:wording(bad))
 reject('currentactualpacketaccess',lambda:read(P.parent/'batch-tension-kind3-host-domains-v1/manifest.json'))
 reject('old222actualaccess',lambda:read(P.parent/'batch-tension-uncalibrated-sensitivity-v1/manifest.json'))
 return out

def check():
 b,d,c,j=[load(n) for n in ['baseline.json','owner-delta.json','cases117.json','joins164.json']];before=verify(b['owner_before']).decode();need(b['approved_review']==c['approved_review']==j['approved_review'],'reviewpins');r=json.loads(verify(b['approved_review']));need(r['blocking_findings']==r['required_corrections']==[] and r['disposition'].startswith('APPROVED'),'actualapproval')
 after=compose(before,d);need(sig(after)=={k:d['owner_after'][k] for k in ['bytes','sha256']},'target');need(compose(after,d,True)==before,'reverse');preserve(before,after,b);mapping(c,j,r);wording(d)
 mapcounts={}
 for name,item in b['retained_owner_maps'].items():
  xs=json.loads(verify(item['pin']))[item['collection_key']];dig={str(i):sha(enc(x)) for i,x in enumerate(xs)} if isinstance(xs,list) else {k:sha(enc(v)) for k,v in xs.items()};need(len(xs)==item['object_count'] and dig==item['object_digests'],'priorR3R4map');mapcounts[name]=len(xs)
 old={}
 for name,item in b['old_catalogs'].items():old[name]=json.loads(verify(item['pin']));oldcatalog(old[name],item)
 need(b['old_IDs']==[f'DTN-{i:03d}' for i in range(1,291)] and b['old_catalogs']['R5']['case_IDs']==[f'DTN-{i:03d}' for i in range(43,168)] and b['old_catalogs']['R6']['case_IDs']==[f'DTN-{i:03d}' for i in range(168,291)],'290priorIDs')
 rel=json.loads(verify(b['release_manifest']));need(rel['files']==b['release_inventory'] and len(rel['files'])==35 and rel['case_count']==rel['evaluation_count']==27,'release metadata')
 neg=controls(c,j,r,before,after,b,old,d)
 for x in d['replacements']:
  for target in re.findall(r'\]\(([^)]+)\)',x['new']):need((ROOT/'wiki/specs'/target.split('#')[0]).resolve().exists(),'newlink')
 if (P/'manifest.json').exists():
  m=load('manifest.json');need({x.name for x in P.iterdir() if x.is_file()}=={'manifest.json'}|{x['path'] for x in m['payloads']},'sealedtree')
  for x in m['payloads']:raw=read(P/x['path']);need(len(raw)==x['bytes'] and sha(raw)==x['sha256'],'sealedpayload')
 return {'status':'PASS','scope':'NEW owner wording/mapping/IDs/preservation ONLY; observations inherited','target':d['owner_after'],'reverse_to_R6_exact':True,'other_whole_bodies_exact':14,'old002prefix_exact':True,'old_rows_exact':42,'old_IDs_exact':290,'new_IDs':106,'newIDrange':['DTN-291','DTN-396'],'historical_input_references':11,'unique_vectors':117,'logical_alias_points':164,'baseline_aliases':48,'total_navigation_IDs':396,'auxiliary_native_boundary_IDs':['DTN-384'],'new_application_predicate_proofs':0,'R3R4map_counts':mapcounts,'old_R5_R6catalogs_exact':[128,128],'old_velocity_parentgap_preserved':True,'old_acceptance_prefix_exact':True,'release_evaluations':27,'release_inventory_entries':35,'negative_controls':neg,'actual_packet_reads':0,'numeric_metric_recomputations':0,'original_calls':0}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--check',action='store_true',required=True);p.parse_args();print(json.dumps(check(),indent=2))
