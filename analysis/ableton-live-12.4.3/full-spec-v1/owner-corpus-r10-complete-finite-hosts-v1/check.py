"""Only NEW owner wording/mapping/preservation; original evidence remains inherited."""
from pathlib import Path
import argparse,copy,hashlib,json,re
P=Path(__file__).resolve().parent;R=P.parents[3]
def need(v,s):
 if not v:raise AssertionError(s)
def sha(b):return hashlib.sha256(b).hexdigest()
def obj(x):return sha(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode())
def load(n):return json.loads((P/n).read_bytes())
def verify(x):
 p=(R/x['path']).resolve();s=str(p)
 need(p==R/'wiki/specs/device-corpus.md' or p==R/'analysis/ableton-live-12.4.3/full-spec-v1/reviews/corpus-complete-finite-host-domains-v1-review.json' or (('/full-spec-v1/owner-corpus-' in s or '/full-spec-v1/corpus-owner-' in s) and p.suffix=='.json') or p==R/'handoff/device-corpus-v5/manifest.json','owner/summary/manifest only')
 b=p.read_bytes();need(len(b)==x['bytes'] and sha(b)==x['sha256'],'pin');return b

def validate(c,n,j,s,old,r):
 need(len(c['catalog'])==264 and len(n)==201 and len(c['aliases'])==277 and len(j['vectors'])==264 and len(j['aliases'])==277,'complete units')
 need(c['shared_input']==s['shared_input'] and c['aliases']==s['aliases'] and c['review_qualifications']==r['qualifications'] and c['inherited_common_qualification']==r['inherited_common_qualification'] and c['this_packet_checker_status']==r['safe_owned_check'],'authority/qualification scopes')
 need(n==[x for x in c['catalog'] if x['case_id']] and [x['case_id'] for x in n]==[f'DCO-{i:03d}' for i in range(94,295)],'201newIDs')
 need(len({x['vector_sha256'] for x in c['catalog']})==264,'unique fullvectors');fresh=94;oldcount=0;unnum=0;refs=[]
 for i,(x,v,p) in enumerate(zip(c['catalog'],s['input_vectors'],s['approved_points'])):
  need(x['vector_id']==v['id'] and x['vector_sha256']==v['vector_sha256'] and x['complete_history_sha256']==v['complete_history_sha256'] and x['first_alias']==v['first_alias'] and x['alias_ids']==v['alias_ids'],'full vectoridentity')
  need(x['parameter_tokens']==v['parameter_tokens'] and x['parameter_f32_bits_le']==v['parameter_f32_bits_le'] and x['parameter_f64_reconstructed_le']==v['parameter_f64_reconstructed_le'],'all38words/f32/f64')
  need(x['approved_point_pointer']==f'/approved_summary/approved_points/{i}' and x['input_vector_pointer']==f'/approved_summary/input_vectors/{i}' and x['approved_point_sha256']==obj(p) and x['input_vector_sha256']==obj(v),'complete summary joins')
  need(all(x[k] is None for k in ['waveform_prior','new_expected_waveform','portable_expected','portable_comparator','grade','new_metrics_for_inherited']) and x['new_application_predicate_proof'] is False,'NULLs/application')
  need(x['provenance']==p['provenance'],'provenance')
  if p['provenance']=='fresh-once-only':
   need(x['case_id']==f'DCO-{fresh:03d}' and x['vector_sha256'] not in old,'freshIDs/missingclass');fresh+=1
   need(x['native_observation']=={k:p[k] for k in ['script','pid','receipt_pointer','output','observed_unsigned_summary']} and x['new_pid']==p['pid'] and x['new_receipt']==p['receipt_pointer'],'fresh copied facts')
   need(x['fresh_checker_status']=='THIS pre-call-bound data checker PASS' and x['inherited_checker_qualification'] is None and x['prior_reference'] is None and x['existing_case_reference'] is None and not x['unnumbered_shape5_metadata'] and x['requirements']==['REQ-DEVICE-CORPUS-002'],'new goodchecker distinct')
  else:
   oldcount+=1;z=old[x['vector_sha256']];ref=z['case_id'] or z['existing_case_reference'];refs.append(ref)
   need(x['case_id'] is None and x['existing_case_reference']==ref and x['unnumbered_shape5_metadata']==z['qualification_only_unnumbered_shape5'],'fullhash oldowner mapping')
   need(x['native_observation'] is None and x['new_pid'] is x['new_receipt'] is None and x['fresh_checker_status'] is None and x['requirements']==[],'no newoldfacts')
   need(x['prior_reference']=={'old_R9_vector_id':z['vector_id'],'old_R9_catalog_sha256':obj(z),'old_R9_reference':ref,'old_qualification_pointer':z['common_qualification'],'prior_summary_reference':p['historical'],'no_new_pid_receipt_metrics':True},'oldqualifiers exact')
   need(x['inherited_checker_qualification']=='Preserve exact per-reference original checker FAIL/additive postcapture DATA/default/source limits; no repair','oldfailure not repaired')
   if x['unnumbered_shape5_metadata']:unnum+=1;need(ref is None and z['vector_id']=='CNI-V036','shape5 unnumbered')
  need(j['vectors'][i]=={'vector_id':x['vector_id'],'vector_sha256':x['vector_sha256'],'case_id':x['case_id'],'existing_case_reference':x['existing_case_reference'],'unnumbered_shape5_metadata':x['unnumbered_shape5_metadata'],'approved_point_pointer':x['approved_point_pointer'],'input_vector_pointer':x['input_vector_pointer']},'allvector joins')
 need(fresh==295 and oldcount==63 and unnum==1 and len([x for x in refs if x])==62,'201/63/unnumbered')
 by={x['vector_sha256']:x for x in c['catalog']}
 for a,z in zip(s['aliases'],j['aliases']):x=by[a['vector_sha256']];need(z==dict(a,case_id=x['case_id'],existing_case_reference=x['existing_case_reference']),'277alias fullhash joins')

def main():
 b=load('baseline.json');d=load('owner-delta.json');c=load('catalog264.json');n=load('new-cases201.json');j=load('joins277.json');r=json.loads(verify(b['approved_review']));s=r['approved_summary'];oldcat=json.loads(verify(b['R9_catalog_pin']));old={x['vector_sha256']:x for x in oldcat['vectors']};need(len(old)==63,'old63')
 before=verify(b['owner_before']).decode();need(d['owner_before']==b['owner_before'],'base');after=before
 for x in d['replacements']:need(after.count(x['old'])==1,'uniqueold');after=after.replace(x['old'],x['new'])
 need(len(after.encode())==d['owner_after']['bytes'] and sha(after.encode())==d['owner_after']['sha256'],'target')
 rev=after
 for x in reversed(d['replacements']):need(rev.count(x['new'])==1,'uniquenew');rev=rev.replace(x['new'],x['old'])
 need(rev==before,'full reversal')
 bodies=lambda t:{m[1]:m[0] for m in re.finditer(r'^### (REQ-DEVICE-CORPUS-\d{3})[^\n]*\n.*?(?=^### REQ-|^## |\Z)',t,re.M|re.S)}
 oldb=bodies(before);newb=bodies(after);need(len(oldb)==len(newb)==13,'13REQ')
 for k,v in oldb.items():need(sha(v.encode())==b['requirement_bodies'][k]['sha256'] and (newb[k].startswith(v) if k.endswith('002') else newb[k]==v),'12whole+002prefix')
 need([x for x in after.splitlines() if re.match(r'^\| DCO-\d{3} \|',x)]==b['old_rows'] and len(b['old_rows'])==36 and b['old_IDs']==[f'DCO-{i:03d}' for i in range(1,94)],'93oldIDs36rows')
 secs=lambda t:{m[1]:m[0] for m in re.finditer(r'^## ([^\n]+)\n.*?(?=^## |\Z)',t,re.M|re.S)}
 for name,h in b['protected_sections'].items():need(sha(secs(after)[name].encode())==h,'oldsections '+name)
 for x in b['old_objects']:need(obj(json.loads(verify(x['pin'])))==x['json_object_sha256'],'R3–R9objects')
 release=json.loads(verify(b['release_manifest']));need(obj(release)==b['release_manifest_object_sha256'] and release['case_count']==27 and release['evaluation_count']==73,'release27/73metadata')
 validate(c,n,j,s,old,r);neg=[]
 freshindex=next(i for i,x in enumerate(c['catalog']) if x['case_id']);oldindex=next(i for i,x in enumerate(c['catalog']) if not x['case_id']);shape=next(i for i,x in enumerate(c['catalog']) if x['unnumbered_shape5_metadata'])
 for name,mut in [('omitalias',lambda a,z,m:a['aliases'].pop()),('omitvector',lambda a,z,m:a['catalog'].pop()),('duplicateID',lambda a,z,m:a['catalog'][freshindex+1].update(case_id='DCO-094')),('inventoldID',lambda a,z,m:a['catalog'][oldindex].update(case_id='DCO-295')),('oldpositionjoin',lambda a,z,m:a['catalog'][oldindex].update(existing_case_reference='DCO-021')),('shape5ID',lambda a,z,m:a['catalog'][shape].update(existing_case_reference='DCO-021')),('inventoldPID',lambda a,z,m:a['catalog'][oldindex].update(new_pid=1)),('new201mislabelFAIL',lambda a,z,m:a['catalog'][freshindex].update(fresh_checker_status='old checker FAIL')),('repairpriorFAIL',lambda a,z,m:a['catalog'][oldindex].update(inherited_checker_qualification=None)),('portableexpected',lambda a,z,m:a['catalog'][freshindex].update(portable_expected=1)),('newcomparator',lambda a,z,m:a['catalog'][freshindex].update(portable_comparator='waveform')),('grade',lambda a,z,m:a['catalog'][freshindex].update(grade='PASS')),('fitprior',lambda a,z,m:a['catalog'][freshindex].update(waveform_prior='fit')),('applicationproof',lambda a,z,m:a['catalog'][freshindex].update(new_application_predicate_proof=True)),('wrongf64',lambda a,z,m:a['catalog'][freshindex]['parameter_f64_reconstructed_le'].__setitem__(7,'0'*16)),('wrongnativehash',lambda a,z,m:a['catalog'][freshindex]['native_observation']['output'].update(sha256='0'*64)),('dropjoin',lambda a,z,m:m['vectors'].pop()),('newaliasID',lambda a,z,m:m['aliases'][0].update(case_id='DCO-295'))]:
  a,z,m=copy.deepcopy((c,n,j));mut(a,z,m)
  try:validate(a,z,m,s,old,r)
  except (AssertionError,KeyError,IndexError):neg.append(name)
  else:raise AssertionError('negative accepted '+name)
 for name,mut in [('old001body',after.replace('### REQ-DEVICE-CORPUS-001','### REQ-DEVICE-CORPUS-901',1)),('oldrow',after.replace('| DCO-001 |','| DCO-999 |',1)),('R9erratum',after.replace('Preserve all36 prior IDs/36 old rows','Preserve all13IDs/36oldrows',1)),('oldtiming',after.replace('**Latency.** None.','**Latency.** Changed.',1))]:
  need(mut!=after,'meaningful '+name)
  for x in reversed(d['replacements']):mut=mut.replace(x['new'],x['old'],1)
  need(mut!=before,'preservation '+name);neg.append(name)
 for x in d['replacements']:
  for link in re.findall(r'\]\(([^)]+)\)',x['new']):need((R/'wiki/specs'/link.split('#')[0]).resolve().exists(),'newlink')
 if (P/'manifest.json').exists():
  m=load('manifest.json');need({x.name for x in P.iterdir()}=={'manifest.json'}|{x['path'] for x in m['payloads']},'sealedtree')
  for x in m['payloads']:raw=(P/x['path']).read_bytes();need(len(raw)==x['bytes'] and sha(raw)==x['sha256'],'payload')
 return {'status':'PASS','owner_after':d['owner_after'],'newcases':201,'range':['DCO-094','DCO-294'],'wholevectors':264,'aliases':277,'inherited_hashrefs':63,'inherited_case_refs':62,'unnumbered_shape5':1,'12otherwholeREQ_old002prefix_exact':True,'old93IDs36rows_exact':True,'R3R9objectproviders_exact':len(b['old_objects']),'R9countwording_erratum_exact':True,'oldcriteria_U_modal176_parked96_history_protected':True,'releasegroups_evaluations':[27,73],'fullreverse_exact':True,'fresh201_this_preboundcheckerPASS_distinct_from_old63qualifications':True,'negativecontrols':neg,'actual_packet_reads':0,'source_raw_numeric_rechecks':0,'original_calls':0}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--check',required=True,action='store_true');p.parse_args();print(json.dumps(main(),indent=2))
