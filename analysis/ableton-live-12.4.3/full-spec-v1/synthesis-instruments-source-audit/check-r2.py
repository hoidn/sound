"""Focused literal source-association successor; no old code/import/main/parser/replay runs."""
from pathlib import Path
from hashlib import sha256
from copy import deepcopy
from collections import Counter
import json,sys
A=Path(__file__).resolve().parent;R=A.parents[3]
X='mixed-represented-subset-and-gap-or-unresolved-context';U='documented-outcome-or-source-context-U'
DRIVE='Filter Drive is additional input gain before the filter, distinct from Shaper Drive. OP015 actually selects Morph snap context options and only inspects Drive eligibility; it does not change Filter Drive. The eligible Filter Drive gesture remains documented-but-unexercised/U under existing G25, with its productive NONEMPTY main/filter positive baseline; no gain coefficient, normalization or audio identity is supplied.'
MORPH='Morph controls the Morph filter position. OP015 actually invokes each named Morph snap, not a continuous Morph slider change. That continuous gesture remains documented-but-unexercised/U under existing G25 with eligible productive NONEMPTY main/filter positive baseline; OP017 Shaper Drive and wet bypass are separate true histories, not evidence for Morph. No curve, coefficient or timing law is supplied.'
def j(p):return json.loads(p.read_text())
def dg(p):
 b=p.read_bytes();return dict(bytes=len(b),sha256=sha256(b).hexdigest())
def pincheck(q):assert dg(R/q['path'])=={k:q[k] for k in ['bytes','sha256']},q['path']
def ptr(v,p):
 for k in p.strip('/').split('/'):v=v[int(k)] if isinstance(v,list) else v[k.replace('~1','/').replace('~0','~')]
 return v

def views(old,plan,restore=False):
 # Only these two known judgments, their forward/reverse links, one group membership and counts.
 a=deepcopy(old);p=deepcopy(plan)
 p['judgments']['INS:B630']['selected_requirements']=[15];p['judgments']['INS:B630']['assessment']=DRIVE
 p['judgments']['INS:B631'].update(disposition='X',selected_requirements=[15],proposal_groups=['G25'],assessment=MORPH)
 for i,note in [(393,DRIVE),(394,MORPH)]:
  a['assessments'][i].update(assessment=note,requirement_refs=deepcopy(old['assessments'][302]['requirement_refs']),case_refs=deepcopy(old['assessments'][302]['case_refs']))
 a['assessments'][394].update(disposition=X,proposal_groups=['G25'])
 for kind in ['requirements','cases']:
  for i,remove,add in [(68,['SIA-A394'],[]),(74,['SIA-A394'],[]),(75,['SIA-A395'],[]),(73,[],['SIA-A394','SIA-A395'])]:
   ids=old['reverse_catalogs'][kind][i]['related_assessment_ids'];a['reverse_catalogs'][kind][i]['related_assessment_ids']=sorted([v for v in ids if v not in remove]+add)
 a['proposals'][24]['assessment_ids']=old['proposals'][24]['assessment_ids']+['SIA-A395']
 a['summary']['dispositions'][X]=360;a['summary']['dispositions'][U]=96
 if restore:
  for key in ['INS:B630','INS:B631']:p['judgments'][key]=deepcopy(plan['judgments'][key])
  for i in [393,394]:a['assessments'][i]=deepcopy(old['assessments'][i])
  for kind in ['requirements','cases']:
   for i in [68,73,74,75]:a['reverse_catalogs'][kind][i]=deepcopy(old['reverse_catalogs'][kind][i])
  a['proposals'][24]=deepcopy(old['proposals'][24]);a['summary']['dispositions']=deepcopy(old['summary']['dispositions'])
 return a,p

def paths():
 out=[('plan.json','/judgments/INS:B630/'+k) for k in ['selected_requirements','assessment']]
 out += [('plan.json','/judgments/INS:B631/'+k) for k in ['disposition','selected_requirements','proposal_groups','assessment']]
 out += [('audit.json','/assessments/393/'+k) for k in ['assessment','requirement_refs','case_refs']]
 out += [('audit.json','/assessments/394/'+k) for k in ['disposition','assessment','requirement_refs','case_refs','proposal_groups']]
 out += [('audit.json',f'/reverse_catalogs/{kind}/{i}/related_assessment_ids') for kind in ['requirements','cases'] for i in [68,74,75,73]]
 out += [('audit.json','/proposals/24/assessment_ids'),('audit.json','/summary/dispositions/'+X),('audit.json','/summary/dispositions/'+U)]
 return out

def validate(a,p,old,plan):
 good,gp=views(old,plan);assert a==good and p==gp,'Only exact literal correction is allowed'
 for i,key,note in [(393,'INS:B630',DRIVE),(394,'INS:B631',MORPH)]:
  q=a['assessments'][i];assert q['assessment']==p['judgments'][key]['assessment']==note
  assert q['disposition']==X and q['proposal_groups']==p['judgments'][key]['proposal_groups']==['G25']
  assert q['requirement_refs'][0]['id']=='REQ-SYN-OP-015' and q['case_refs'][0]['id']=='SYN-OP-015'
  assert all(q[k] is None for k in ['documentary_expected','documentary_comparison','actual_expected','actual_comparison']) and q['target']=='U' and not q['executed'] and not q['complete'] and q['coverage_credit']==0
 assert a['owner_cases']==old['owner_cases'] and a['owner_requirements']==old['owner_requirements'] and a['owner_fixtures']==old['owner_fixtures']
 assert a['owner_cases'][73]['setup_and_action']=='Enumerate type/circuit eligibility and slopes; select Morph and each snap context option; inspect Drive eligibility without assigning coefficients.'
 assert a['assessments'][303]==old['assessments'][303] and a['assessments'][395:398]==old['assessments'][395:398]
 for i in [302,303,395,396,397]:assert a['assessments'][i]==old['assessments'][i]
 assert dict(Counter(q['disposition'] for q in a['assessments']))==a['summary']['dispositions']
 assert a['proposals'][24]['proposed_future_action']==old['proposals'][24]['proposed_future_action']
 assert a['proposals'][24]['proposed_future_positive_baseline']==old['proposals'][24]['proposed_future_positive_baseline']
 return True

def main():
 assert sys.dont_write_bytecode and sys.argv[1:]==['--check'],'Read-only --check only; unsupported arguments refused before inputs'
 response=j(A/'response-r2.json');ins=j(A/'inputs.json');old=j(A/'audit.json');plan=j(A/'plan.json')
 watch={R/q['path'] for q in ins['files']+response['preserved_R1_files']+[response['review']]}|{p for p in A.iterdir() if p.is_file()};before={str(p):dg(p) for p in watch}
 for q in ins['files']+response['preserved_R1_files']+[response['review']]:pincheck(q)
 assert len(ins['files'])==88 and len(response['preserved_R1_files'])==6
 assert response['prior_manifest']['sha256']=='6cc774ae4b0596cdacb01544b762bfe1fa210ef7595063b64d515f8540c18c6b';pincheck(response['prior_manifest'])
 assert response['review']['sha256']=='d2df70867957a605351c2e1e962816cfee120fcfe288bf038b354027c7a9f28e'
 assert response['required_finding']=='SIA-REVIEW-001' and response['new_normative_IDs']==[] and response['new_cases']==response['coverage_credit']==0 and response['target']=='U' and not response['executed'] and not response['complete']
 assert all(response[k] is None for k in ['documentary_expected','documentary_comparison','actual_expected','actual_comparison'])
 prior=j(A/'manifest.json');assert len(prior['files'])==5
 for name,pin in prior['files'].items():assert dg(A/name)==pin
 a,p=views(old,plan);validate(a,p,old,plan)
 assert views(old,plan,restore=True)==(old,plan)
 prior_docs={'audit.json':old,'plan.json':plan};docs={'audit.json':a,'plan.json':p}
 expected=[dict(document=d,json_pointer=q,before=ptr(prior_docs[d],q),after=ptr(docs[d],q)) for d,q in paths()]
 assert len(expected)==25 and all(v['before']!=v['after'] for v in expected) and response['changes']==expected
 assert len(a['assessments'])==567 and len(a['resources'])==112 and len(a['proposals'])==37 and len(a['source_questions'])==8 and len(a['owner_requirements'])==109 and len(a['owner_cases'])==154
 rejected=[]
 def wrong_route(b,bp,i,key,selected):
  bp['judgments'][key]['selected_requirements']=selected
  b['assessments'][i]['requirement_refs']=deepcopy(old['assessments'][i]['requirement_refs'])
  b['assessments'][i]['case_refs']=deepcopy(old['assessments'][i]['case_refs'])
 def wrong_note(b,bp,i,key,note):
  b['assessments'][i]['assessment']=bp['judgments'][key]['assessment']=note
 for name,change in [
 ('borrow-envelope-and-key',lambda b,bp:wrong_route(b,bp,393,'INS:B630',[16,10])),
 ('borrow-ShaperDrive-for-Morph',lambda b,bp:wrong_route(b,bp,394,'INS:B631',[17])),
 ('Drive-inspection-promoted-to-operation',lambda b,bp:wrong_note(b,bp,393,'INS:B630','OP015 actually changes Filter Drive')),
 ('snaps-promoted-to-continuous-Morph',lambda b,bp:wrong_note(b,bp,394,'INS:B631','OP015 actually sweeps continuous Morph')),
 ('remove-true-snaps',lambda b,bp:b['assessments'][303].update(assessment='No Morph snap action')),
 ('erase-true-ShaperDrive',lambda b,bp:b['assessments'][396].update(case_refs=[])),
 ('miss-reverse-Morph-route',lambda b,bp:b['reverse_catalogs']['cases'][73]['related_assessment_ids'].remove('SIA-A395')),
 ('miss-G25-gap',lambda b,bp:b['proposals'][24]['assessment_ids'].remove('SIA-A395')),
 ('invent-oracle',lambda b,bp:b['assessments'][393].update(actual_expected='pass')),
 ('mutate-old-action',lambda b,bp:b['owner_cases'][73].update(setup_and_action='Change Filter Drive and continuous Morph')),
 ('erase-productive-baseline',lambda b,bp:b['proposals'][24].update(proposed_future_positive_baseline='selected flag only'))]:
  bad=deepcopy(a);bp=deepcopy(p);change(bad,bp)
  try:validate(bad,bp,old,plan)
  except AssertionError:rejected.append(name)
  else:raise AssertionError('Unsafe mutation accepted '+name)
 for name in ['response-r2.json','README-r2.md','check-r2.py']:assert all(l.rstrip()==l for l in (A/name).read_text().splitlines()),name
 if (A/'manifest-r2.json').exists():
  mf=j(A/'manifest-r2.json');assert len(mf['files'])==3
  for q in mf['files']:pincheck(q)
  assert {p.name for p in A.iterdir() if p.is_file()}=={Path(q['path']).name for q in response['preserved_R1_files']}|{'response-r2.json','README-r2.md','check-r2.py','manifest-r2.json'}
 assert before=={str(p):dg(p) for p in watch}
 print(json.dumps(dict(status='pass',sealed=(A/'manifest-r2.json').exists(),literal_fields=25,manual_fields=6,forward_fields=8,reverse_fields=8,group_fields=1,derived_counts=2,preserved_R1_files=6,immutable_inputs=88,owner_history_files=81,contexts=567,resources=112,groups=37,questions=8,clauses=109,cases=154,all_actual_U=True,new_adoption=0,negative_fixtures=rejected,positive_retained=['OP015 named Morph snaps','OP017 distinct Shaper Drive and wet bypass'],no_old_code_import_compile_main_parser_replay=True,watched_paths=len(watch),all_unchanged=True,writes=False,independent_review='Root focused review pending as of author freeze'),indent=2))
if __name__=='__main__':main()
