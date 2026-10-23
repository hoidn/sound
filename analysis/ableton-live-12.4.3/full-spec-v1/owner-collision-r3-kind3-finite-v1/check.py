"""NEWowner wording/mapping/preservation only; no actual/source/raw/numeric execution."""
from pathlib import Path
import argparse,copy,hashlib,json,re
H=Path(__file__).resolve().parent;R=H.parents[3];F=H.parent
REVIEW_NAMES=['collision-kind3-host-domains-v1-partial-review.json','collision-kind3-unlaunched-continuation-v1-review.json']
def need(v,s):
 if not v:raise AssertionError(s)
def sha(b):return hashlib.sha256(b).hexdigest()
def obj(x):return sha(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode())
def load(n):return json.loads((H/n).read_bytes())
def verified(x):
 p=(R/x['path']).resolve();allowed={R/'wiki/specs/device-collision.md',R/'handoff/device-collision-v1/manifest.json',F/'owner-collision-r2-finite-v1/case-catalog.json'}|{F/'reviews'/n for n in REVIEW_NAMES};need(p in allowed,'onlyowner/approvedsummary/releasemanifest/oldownerJSON');b=p.read_bytes();need(len(b)==x['bytes']and sha(b)==x['sha256'],'pin');return b

def validate(c,n,j,ss,qq):
 need(c['shared_input']==ss[1]['shared_input']and c['review_qualifications']==qq,'unchangedshared/qualifications')
 need(c['counts']=={'domains':20,'aliases':105,'histories':86,'new_observations':84,'unlabelled_guard_failure':1,'historical_input_only_baseline':1}and len(c['catalog'])==86 and len(n)==84 and len(j['aliases'])==105 and len(j['unique_histories'])==86,'wholeunits')
 need(n==[z for z in c['catalog']if z['case_id']is not None]and[z['case_id']for z in n]==[f'DCL-{v:03d}'for v in range(63,147)],'84contiguousIDs/noextra')
 by={}
 for ri,s in enumerate(ss):
  for pi,p in enumerate(s['approved_points']):need(p['id']not in by,'noapprovedoverlap');by[p['id']]=(ri,pi,p)
 need(len(by)==84 and'i058-v01'not in by,'84onlynotfailed')
 for z,h in zip(c['catalog'],ss[1]['complete_histories']):
  for k in ['id','changed_index','value','vector_sha256','history_sha256','whole_history','script_bytes','script_sha256']:need(z[k]==h[k],'allcompleteinputs')
  need(all(z[k]is None for k in ['fresh_waveform_prior','portable_expected','portable_comparator','candidate_grade','new_metrics'])and z['new_application_predicate_proof']is False,'NULL/noapp')
  if z['id']in by:
   ri,pi,p=by[z['id']];need(z['disposition']=='APPROVED-FINITE-NATIVE-OBSERVATION-ONLY'and z['requirements']==['REQ-DEVICE-COLLISION-002'],'finiteonly')
   need(z['source_review']==c['source_reviews'][ri]and z['approved_point_pointer']==f'/approved_summary/approved_points/{pi}'and z['approved_point_sha256']==obj(p),'exactapprovedjoin')
   need(z['parameter_words']==p['parameter_words']and z['native_observation']=={k:p[k]for k in ['script','receipt','receipt_pointer','pid','utc_start','utc_end','audio','native_output_summary']},'approvedinput/outputidentities')
   need(z['new_pid']==p['pid']and z['new_receipt']==p['receipt_pointer']and z['qualification_scope']==f'cases86.json#/review_qualifications/{ri}','nativefacts/qualification')
  elif z['id']=='i058-v01':
   need(z['case_id']is z['new_pid']is z['new_receipt']is z['native_return_semantics']is None and z['approved_success']is False and z['requirements']==[]and z['disposition']=='GUARD-FAIL-UNAPPROVED-SUCCESS-NATIVE-SEMANTICS-U','failednoIDsuccess')
   need(z['discovery_pointer']=='/approved_summary/guard_rejected_discovery'and z['discovery_object_sha256']==obj(ss[0]['guard_rejected_discovery'])and z['qualification_scope']=='cases86.json#/review_qualifications/0','failedcitation')
  else:
   need(z['changed_index']is None and z['case_id']is z['new_pid']is z['new_receipt']is z['approved_actual']is None and z['existing_case_refs']==[]and z['requirements']==[]and z['disposition']=='HISTORICAL-INPUT-ONLY-NOT-APPROVED-X','baselineinputnotapproved')
   need(z['historical_input']==h['historical_input'],'historicalinput')
  need(j['unique_histories'][c['catalog'].index(z)]=={k:z[k]for k in ['id','case_id','disposition','history_sha256','vector_sha256']},'uniquejoins')
 b={z['id']:z for z in c['catalog']}
 for a,z in zip(ss[1]['approved_aliases'],j['aliases']):need(z==dict(a,case_id=b[a['id']]['case_id'],disposition=b[a['id']]['disposition']),'105exactaliases')
 need(len({x['history_sha256']for x in c['catalog']})==86 and sum(x['shared_baseline']for x in j['aliases'])==20,'fullhistdedup/baselinealiases')
 need('historicalasofpartial'in c['qualification_asof_policy'],'asofold69unlaunched')

def main():
 b=load('baseline.json');d=load('owner-delta.json');c=load('cases86.json');n=load('new-cases84.json');j=load('joins105.json');rr=[json.loads(verified(x))for x in b['approved_reviews']];ss=[x['approved_summary']for x in rr]
 need(all(x['source_pin_window'].startswith('CLEAR')for x in rr),'approvedwindows');need(not rr[0]['blocking_findings_for_15_finite_observations']and not rr[1]['blocking_findings'],'approvedsummaries')
 before=verified(b['owner_before']).decode();need(d['owner_before']==b['owner_before'],'base');after=before
 for x in d['replacements']:need(after.count(x['old'])==1,'uniqueold');after=after.replace(x['old'],x['new'])
 need(len(after.encode())==d['owner_after']['bytes']and sha(after.encode())==d['owner_after']['sha256'],'target');rev=after
 for x in reversed(d['replacements']):need(rev.count(x['new'])==1,'uniquenew');rev=rev.replace(x['new'],x['old'])
 need(rev==before,'fullreverse')
 bodies=lambda t:{v[1]:v[0]for v in re.finditer(r'^### (REQ-DEVICE-COLLISION-\d{3})[^\n]*\n.*?(?=^### REQ-|^## |\Z)',t,re.M|re.S)}
 old=bodies(before);new=bodies(after);need(len(old)==len(new)==18,'18REQ')
 for k,v in old.items():need(sha(v.encode())==b['requirement_bodies'][k]['sha256']and(new[k].startswith(v)if k.endswith('002')else new[k]==v),'17whole/002prefix')
 secs=lambda t:{v[1]:v[0]for v in re.finditer(r'^## ([^\n]+)\n.*?(?=^## |\Z)',t,re.M|re.S)}
 se=secs(after);oldse=secs(before)
 for k,v in b['protected_sections'].items():need(sha(se[k].encode())==v,'protected '+k)
 need(sha(oldse['Acceptance cases'].encode())==b['old_acceptance_prefix_sha256']and se['Acceptance cases'].startswith(oldse['Acceptance cases']),'oldAcceptanceprefix')
 need([x for x in after.splitlines()if x.startswith('| DCL-')]==b['old_rows']and len(b['old_rows'])==62 and b['old_IDs']==[f'DCL-{i:03d}'for i in range(1,63)],'50+12rows62IDs')
 need(obj(json.loads(verified(b['oldR2catalog'])))==b['oldR2catalog_object_sha256'],'fullR2histories/relations')
 rel=json.loads(verified(b['release_manifest']));need(rel['files']==b['release_inventory']and[rel['case_count'],rel['evaluation_count'],len(rel['files'])]==b['release_cases_evaluations_inventory']==[2,2,8],'released2/2/8metadata')
 need(c['source_reviews']==b['approved_reviews'],'tworeviewauthority');validate(c,n,j,ss,[x['qualifications']for x in rr]);negative=[]
 failed=next(i for i,x in enumerate(c['catalog'])if x['id']=='i058-v01');base=next(i for i,x in enumerate(c['catalog'])if x['changed_index']is None)
 tests=[('omitcase',lambda a,v,z:v.pop()),('omitalias',lambda a,v,z:z['aliases'].pop()),('omithistory',lambda a,v,z:a['catalog'].pop()),('failednewID',lambda a,v,z:a['catalog'][failed].update(case_id='DCL-147')),('failedsuccess',lambda a,v,z:a['catalog'][failed].update(approved_success=True)),('ret1meaning',lambda a,v,z:a['catalog'][failed].update(native_return_semantics='success')),('baselineID',lambda a,v,z:a['catalog'][base].update(case_id='DCL-148')),('baselineX',lambda a,v,z:a['catalog'][base].update(approved_actual='X')),('baselineoldcriterion',lambda a,v,z:a['catalog'][base].update(existing_case_refs=['DCL-002'])),('baselinePID',lambda a,v,z:a['catalog'][base].update(new_pid=1)),('duplicateID',lambda a,v,z:a['catalog'][2].update(case_id='DCL-063')),('wrongpriorreview',lambda a,v,z:a['catalog'][0].update(source_review=a['source_reviews'][1])),('wrongsummarypointer',lambda a,v,z:a['catalog'][0].update(approved_point_pointer='/approved_summary/approved_points/1')),('wrongnativehash',lambda a,v,z:a['catalog'][0]['native_observation']['audio'].update(sha256='0'*64)),('changedonframe',lambda a,v,z:a['catalog'][0]['whole_history']['events'][0].__setitem__(0,4097)),('changedwordbits',lambda a,v,z:a['catalog'][0]['parameter_words'][1].update(f32_le='00'*4)),('portableexpected',lambda a,v,z:a['catalog'][0].update(portable_expected='audio')),('comparator',lambda a,v,z:a['catalog'][0].update(portable_comparator='exact')),('grade',lambda a,v,z:a['catalog'][0].update(candidate_grade='PASS')),('fitprior',lambda a,v,z:a['catalog'][0].update(fresh_waveform_prior='fit')),('newappproof',lambda a,v,z:a['catalog'][0].update(new_application_predicate_proof=True)),('dropqualifications',lambda a,v,z:a['review_qualifications'][0].pop()),('dropasof',lambda a,v,z:a.update(qualification_asof_policy='69currentlyunlaunched')),('native59range',lambda a,v,z:a['shared_input']['domains'][7].update(native_max=6)),('parameteronlydedup',lambda a,v,z:a['catalog'][0].update(history_sha256=a['catalog'][base]['history_sha256']))]
 for name,fn in tests:
  a,v,z=copy.deepcopy((c,n,j));fn(a,v,z)
  try:validate(a,v,z,ss,[x['qualifications']for x in rr])
  except(AssertionError,KeyError,IndexError):negative.append(name)
  else:raise AssertionError('negativeaccepted '+name)
 for name,mut in [('oldREQ003',after.replace('### REQ-DEVICE-COLLISION-003','### REQ-DEVICE-COLLISION-103',1)),('oldREQ002prefix',after.replace('legacy integer fields','changed integer fields',1)),('oldrow',after.replace('| DCL-001 |','| DCL-999 |',1)),('oldnoiseU',after.replace('noise fixtures are ungraded','noise fixtures are graded',1))]:
  need(mut!=after,'meaningful '+name)
  for x in reversed(d['replacements']):mut=mut.replace(x['new'],x['old'],1)
  need(mut!=before,'preservationnegative '+name);negative.append(name)
 for x in d['replacements']:
  for link in re.findall(r'\]\(([^)]+)\)',x['new']):need((R/'wiki/specs'/link.split('#')[0]).resolve().exists(),'newlink')
 if(H/'manifest.json').exists():
  m=load('manifest.json');need({x.name for x in H.iterdir()}=={'manifest.json'}|{x['path']for x in m['payloads']},'sealedtree')
  for x in m['payloads']:raw=(H/x['path']).read_bytes();need(len(raw)==x['bytes']and sha(raw)==x['sha256'],'payloadpin')
 return {'status':'PASS','owner_after':d['owner_after'],'newIDs':84,'range':['DCL-063','DCL-146'],'domains_aliases_histories':[20,105,86],'approved_sources':[15,69],'failed_unlabelled':1,'historicalinput_baseline_unlabelled':1,'17otherwholeREQ_002prefix':True,'old_rows':62,'oldIDs':62,'R2history_objects_relations_exact':True,'oldAcceptanceprefix':True,'release_cases_evaluations_inventory':[2,2,8],'full_reverse':True,'negative_controls':negative,'actual_source_raw_numeric_re_reviewed':False,'original_calls':0,'canonical_modified':False}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--check',action='store_true',required=True);p.parse_args();print(json.dumps(main(),indent=2))
