"""Owner wording/mapping/preservation ONLY; no actual/source/raw/numeric execution."""
from pathlib import Path
import argparse,copy,hashlib,json,re
P=Path(__file__).resolve().parent;R=P.parents[3]
def need(v,s):
 if not v:raise AssertionError(s)
def sha(x):return hashlib.sha256(x).hexdigest()
def obj(x):return sha(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode())
def load(n):return json.loads((P/n).read_bytes())
def verify(x):
 p=(R/x['path']).resolve();text=str(p)
 need(p==R/'wiki/specs/device-tension.md' or p==R/'analysis/ableton-live-12.4.3/full-spec-v1/reviews/tension-midi-axes-v1-review.json' or ('/full-spec-v1/owner-tension-' in text and p.suffix=='.json') or p==R/'handoff/device-tension-v1/manifest.json','owner/summary/manifest metadata only')
 b=p.read_bytes();need(len(b)==x['bytes'] and sha(b)==x['sha256'],'pin');return b

def validate(c,new,j,s,qual):
 need(len(c['catalog'])==143 and len(new)==142 and len(c['aliases'])==144 and len(j['unique_histories'])==143 and len(j['aliases'])==144,'whole unit counts')
 need(c['shared_input']==s['shared_input'] and c['aliases']==s['aliases'] and c['approved_review_qualifications']==qual,'shared authority/qualification')
 need([x['case_id'] for x in new]==[f'DTN-{v:03d}' for v in range(397,539)] and new==c['catalog'][1:],'142contiguous IDs')
 need(len({x['history_sha256'] for x in c['catalog']})==143 and len({x['parameter_vector_sha256'] for x in c['catalog']})==1,'fullhistory dedup not parameteronly')
 for i,(x,h,p) in enumerate(zip(c['catalog'],s['input_histories'],s['approved_points'])):
  need(x['id']==h['id'] and x['history']==h['history'] and x['events']==h['events'] and x['history_sha256']==h['history_sha256'] and x['parameter_vector_sha256']==h['parameter_vector_sha256'],'all inputhistory')
  need(x['approved_point_pointer']==f'/approved_summary/approved_points/{i}' and x['input_history_pointer']==f'/approved_summary/input_histories/{i}' and x['approved_point_sha256']==obj(p) and x['input_history_sha256']==obj(h),'whole summary joins')
  need(x['new_application_predicate_proof'] is False and x['qualification_pointer']=='cases143.json#/approved_review_qualifications' and all(x[z] is None for z in ['fresh_waveform_prior','portable_expected','portable_comparator','candidate_grade','new_metrics_for_inherited']),'NULL/application/qualification')
  need(x['provenance']==p['provenance'],'provenance')
  if i:
   need(x['case_id']==f'DTN-{396+i:03d}' and x['existing_case_refs']==[] and x['requirements']==['REQ-DEVICE-TENSION-003'],'fresh ID/navigation')
   need(x['native_observation']=={z:p[z] for z in ['script','pid','receipt_pointer','output','observed_unsigned_summary']} and x['new_pid']==p['pid'] and x['new_receipt']==p['receipt_pointer'] and x['historical'] is None,'copied native facts')
  else:need(x['case_id'] is None and x['existing_case_refs']==['DTN-001','defaults_44'] and x['native_observation'] is None and x['new_pid'] is x['new_receipt'] is None and x['historical']==p['historical'],'inherited sharedbaseline nofreshfacts')
  need(j['unique_histories'][i]=={'id':x['id'],'case_id':x['case_id'],'existing_case_refs':x['existing_case_refs'],'approved_point_pointer':x['approved_point_pointer'],'input_history_pointer':x['input_history_pointer'],'history_sha256':x['history_sha256']},'unique mapping')
 for a,z in zip(s['aliases'],j['aliases']):
  x=c['catalog'][int(a['unique_id'].split('U')[1])];need(z==dict(a,case_id=x['case_id'],existing_case_refs=x['existing_case_refs']),'allalias mapping')
 need(j['aliases'][0]['case_id'] is None and j['aliases'][16]['case_id'] is None and j['aliases'][0]['unique_id']==j['aliases'][16]['unique_id'],'baseline collapse')

def main():
 b=load('baseline.json');d=load('owner-delta.json');c=load('cases143.json');new=load('new-cases142.json');j=load('joins144.json');rr=json.loads(verify(b['approved_review']));s=rr['approved_summary']
 before=verify(b['owner_before']).decode();need(d['owner_before']==b['owner_before'],'base');after=before
 for x in d['replacements']:need(after.count(x['old'])==1,'unique old');after=after.replace(x['old'],x['new'])
 need(len(after.encode())==d['owner_after']['bytes'] and sha(after.encode())==d['owner_after']['sha256'],'target')
 rev=after
 for x in reversed(d['replacements']):need(rev.count(x['new'])==1,'unique new');rev=rev.replace(x['new'],x['old'])
 need(rev==before,'full reverse')
 bodies=lambda t:{m[1]:m[0] for m in re.finditer(r'^### (REQ-DEVICE-TENSION-\d{3})[^\n]*\n.*?(?=^### REQ-|^## |\Z)',t,re.M|re.S)}
 old=bodies(before);afterb=bodies(after);need(len(old)==len(afterb)==15,'15REQ')
 for k,v in old.items():need(sha(v.encode())==b['requirement_bodies'][k]['sha256'] and (afterb[k].startswith(v) if k.endswith('003') else afterb[k]==v),'14otherwhole+003prefix')
 need([x for x in after.splitlines() if x.startswith('| DTN-')]==b['old_rows'] and len(b['old_rows'])==42 and b['old_IDs']==[f'DTN-{i:03d}' for i in range(1,397)],'42rows396IDs')
 secs=lambda t:{m[1]:m[0] for m in re.finditer(r'^## ([^\n]+)\n.*?(?=^## |\Z)',t,re.M|re.S)}
 se=secs(after);oldse=secs(before)
 for h,digest in b['protected_sections'].items():need(sha(se[h].encode())==digest,'protected '+h)
 need(sha(oldse['Acceptance cases'].encode())==b['old_acceptance_prefix'] and se['Acceptance cases'].startswith(oldse['Acceptance cases']),'oldAcceptanceprefix')
 for it in b['old_objects']:need(obj(json.loads(verify(it['pin'])))==it['object_sha256'],'R3–R7fullobjects')
 rel=json.loads(verify(b['release_manifest']));need(rel['files']==b['release_inventory'] and rel['evaluation_count']==27 and len(rel['files'])==35,'release27/35metadata')
 validate(c,new,j,s,rr['qualifications']);neg=[]
 mutations=[('omithistory',lambda a,n,z:a['catalog'].pop()),('omitalias',lambda a,n,z:a['aliases'].pop()),('newbaselineID',lambda a,n,z:a['catalog'][0].update(case_id='DTN-539')),('inventbaselinePID',lambda a,n,z:a['catalog'][0].update(new_pid=1)),('parameteronlydedup',lambda a,n,z:a['catalog'][1].update(history_sha256=a['catalog'][0]['history_sha256'])),('unmatchedchannel',lambda a,n,z:a['catalog'][1]['events'][1].__setitem__(1,128)),('wrongoffvelocity',lambda a,n,z:a['catalog'][-1]['events'][1].__setitem__(3,126)),('duplicateID',lambda a,n,z:a['catalog'][2].update(case_id='DTN-397')),('portableexpected',lambda a,n,z:a['catalog'][1].update(portable_expected=0)),('comparator',lambda a,n,z:a['catalog'][1].update(portable_comparator='waveform')),('grade',lambda a,n,z:a['catalog'][1].update(candidate_grade='PASS')),('fitprior',lambda a,n,z:a['catalog'][1].update(fresh_waveform_prior='fit')),('newappProof',lambda a,n,z:a['catalog'][1].update(new_application_predicate_proof=True)),('dropqualification',lambda a,n,z:a['catalog'][1].update(qualification_pointer=None)),('wrongrawhash',lambda a,n,z:a['catalog'][1]['native_observation']['output'].update(sha256='0'*64)),('dropjoin',lambda a,n,z:z['unique_histories'].pop()),('newaliasID',lambda a,n,z:z['aliases'][0].update(case_id='DTN-539'))]
 for name,fn in mutations:
  a,n,z=copy.deepcopy((c,new,j));fn(a,n,z)
  try:validate(a,n,z,s,rr['qualifications'])
  except (AssertionError,KeyError,IndexError):neg.append(name)
  else:raise AssertionError('negativeaccepted '+name)
 for name,mut in [('old002body',after.replace('### REQ-DEVICE-TENSION-002','### REQ-DEVICE-TENSION-202',1)),('oldrow',after.replace('| DTN-001 |','| DTN-999 |',1)),('old003prefix',after.replace('control grid of P','changed grid of P',1)),('oldvelocitygap',after.replace('parent-launch','parentlaunch',1))]:
  need(mut!=after,'meaningful '+name)
  for x in reversed(d['replacements']):mut=mut.replace(x['new'],x['old'],1)
  need(mut!=before,'preservation '+name);neg.append(name)
 for x in d['replacements']:
  for link in re.findall(r'\]\(([^)]+)\)',x['new']):need((R/'wiki/specs'/link.split('#')[0]).resolve().exists(),'newlink')
 if (P/'manifest.json').exists():
  m=load('manifest.json');need({x.name for x in P.iterdir()}=={'manifest.json'}|{x['path'] for x in m['payloads']},'sealedtree')
  for x in m['payloads']:raw=(P/x['path']).read_bytes();need(len(raw)==x['bytes'] and sha(raw)==x['sha256'],'payload')
 return {'status':'PASS','owner_after':d['owner_after'],'newIDs':142,'ranges':[['DTN-397','DTN-411'],['DTN-412','DTN-538']],'whole_histories':143,'logical_aliases':144,'baseline_inherited_once':True,'14otherwholeREQ_002exact_old003prefix':True,'old_rows_exact':42,'old_IDs':396,'oldR3R7objects_exact':len(b['old_objects']),'oldAcceptanceprefix_exact':True,'released_evaluations_inventory':[27,35],'full_reverse':True,'negative_controls':neg,'observations_re_reviewed':False,'actual_packet_reads':0,'original_calls':0}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--check',action='store_true',required=True);p.parse_args();print(json.dumps(main(),indent=2))
