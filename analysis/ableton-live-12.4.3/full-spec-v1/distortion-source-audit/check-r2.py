"""Focused read-only literal correction. No old checker/definitions/main, parser or vendor code executes."""
from pathlib import Path
from hashlib import sha256
from copy import deepcopy
import json,sys
A=Path(__file__).resolve().parent;R=A.parents[3];D=A.parent/'distortion'
def j(p):return json.loads(p.read_text())
def dg(p):
 b=p.read_bytes();return dict(bytes=len(b),sha256=sha256(b).hexdigest())
def pinned(q):assert dg(R/q['path'])=={k:q[k] for k in ['bytes','sha256']},q['path']
NOTE='Morph continuous LP-to-BP-to-HP is the source role. 007 inspects Morph without an actual Morph move; 030 actually tests nine filter types, Pre off/on and filter-sensitive/nonlinear positive baselines. Neither 007 nor 030 explicitly changes gain-stage Filter Frequency. That gesture remains documented-but-unexercised/U, alongside the missing explicit Morph operation; analysis and feedback Frequency controls are separate.'
GROUP='Preserve 007/030 actual selection of nine filters, Pre off/on and filter-sensitive/nonlinear positive baselines. Gain-stage Filter Frequency changes are documented-but-unexercised/U in these selected inputs; add an explicit future gain-stage Filter Frequency change within this same bounded group. 007 inspects Resonance/Peak Gain/Morph; add actual respective Resonance, Peak Gain and Morph operations on source-eligible filters, retaining the Resampling exception and independently productive filter AND nonlinear shaper controls before each contrast.'

def corrected(a,p):
 assert a['assessments'][136]['id']=='DSA-A137' and a['assessments'][136]['local_block']=='roar:B039' and p['judgments'][136]['local_block']=='roar:B039'
 assert a['assessments'][136]['assessment']==p['judgments'][136]['assessment']==NOTE
 assert a['proposals'][5]['id']==p['proposals'][5]['id']=='DSA-G06'
 assert a['proposals'][5]['proposed_minimal_delta']==p['proposals'][5]['proposed_minimal_delta']==GROUP
 for g in (a['assessments'][136],a['proposals'][5]):
  assert all(g[k] is None for k in ['documentary_expected','documentary_comparison','actual_expected','actual_comparison']) and g['target']=='U' and not g['executed'] and not g['complete'] and g['coverage_credit']==0
 for ident,text in [('DST-ROAR-007','Select each of nine filters; inspect Resonance, Peak Gain and Morph; toggle Pre.'),('DST-ROAR-030','Test all nine filter types on S3 with shaper on, contrasting Amount>0, Pre off/on. Establish both filter-sensitive and nonlinear baselines; isolate generated harmonics to distinguish Pre placement. Apply P-AUDIO; if prerequisites are not independently established, outcome remains U.')]:
  assert next(c for c in a['owner_cases'] if c['id']==ident)['input']==text
 assert a['owner_cases']==j(D/'cases.json') and a['owner_requirements']==j(D/'requirements.json') and a['owner_fixtures']==j(D/'fixture-signals.json')
 return True

def main():
 assert sys.dont_write_bytecode and sys.argv[1:]==['--check'],'Read-only --check only; unsupported arguments refused before input reads'
 response=j(A/'response-r2.json');ins=j(A/'inputs.json');old=j(A/'audit.json');oldplan=j(A/'plan.json')
 watch={R/q['path'] for q in ins['files']}|{R/q['path'] for q in response['preserved_R1_files']}|{R/response['review']['path']}|{p for p in A.iterdir() if p.is_file()};before={str(p):dg(p) for p in watch}
 for q in ins['files']+response['preserved_R1_files']+[response['review'],response['prior_manifest']]:pinned(q)
 assert len(ins['files'])==89 and len(response['preserved_R1_files'])==6
 assert response['prior_manifest']['sha256']=='7663ae7c56e1b7e6f5b9d3033fad1fbdb12cc5fe009a7951b01386d53b9b0dda'
 assert response['review']['sha256']=='17551c49974b02f13ba770dc5d4d0de0cdcb5d702a47a2c7897ef0df27d0513e'
 assert response['required_finding']=='DSA-REVIEW-001' and response['new_normative_IDs']==[] and response['new_cases']==response['coverage_credit']==0 and response['target']=='U' and not response['executed'] and not response['complete']
 assert all(response[k] is None for k in ['documentary_expected','documentary_comparison','actual_expected','actual_comparison'])
 prior=j(A/'manifest.json');assert len(prior['files'])==5
 for name,pin in prior['files'].items():assert dg(A/name)==pin
 expected=[('audit.json','/assessments/136/assessment',old['assessments'][136]['assessment'],NOTE),('plan.json','/judgments/136/assessment',oldplan['judgments'][136]['assessment'],NOTE),('audit.json','/proposals/5/proposed_minimal_delta',old['proposals'][5]['proposed_minimal_delta'],GROUP),('plan.json','/proposals/5/proposed_minimal_delta',oldplan['proposals'][5]['proposed_minimal_delta'],GROUP)]
 assert response['changes']==[dict(document=d,json_pointer=p,before=b,after=c) for d,p,b,c in expected]
 # Exactly four known fields in two logical views, no generic patch/replay framework.
 a=deepcopy(old);p=deepcopy(oldplan)
 a['assessments'][136]['assessment']=p['judgments'][136]['assessment']=NOTE
 a['proposals'][5]['proposed_minimal_delta']=p['proposals'][5]['proposed_minimal_delta']=GROUP
 corrected(a,p)
 restored=deepcopy(a);restored['assessments'][136]['assessment']=old['assessments'][136]['assessment'];restored['proposals'][5]['proposed_minimal_delta']=old['proposals'][5]['proposed_minimal_delta'];assert restored==old
 restored=deepcopy(p);restored['judgments'][136]['assessment']=oldplan['judgments'][136]['assessment'];restored['proposals'][5]['proposed_minimal_delta']=oldplan['proposals'][5]['proposed_minimal_delta'];assert restored==oldplan
 assert len(a['assessments'])==216 and len(a['proposals'])==10 and len(a['source_questions'])==6 and len(a['owner_requirements'])==67 and len(a['owner_cases'])==190
 rejected=[]
 for name,note,group in [('baseline-promoted-to-Frequency',response['changes'][0]['before'],GROUP),('analysis-Frequency-borrowed','009 analysis Frequency proves gain-stage Frequency operated',GROUP),('feedback-Frequency-borrowed',NOTE,'012 feedback Frequency proves gain-stage Frequency operated'),('erase-true-types-Pre','No filter selection or Pre action exists',GROUP),('one-filter-no-nonlinear-baseline',NOTE,GROUP.replace('independently productive filter AND nonlinear shaper controls','a selected filter flag'))]:
  bad=deepcopy(a);bp=deepcopy(p);bad['assessments'][136]['assessment']=bp['judgments'][136]['assessment']=note;bad['proposals'][5]['proposed_minimal_delta']=bp['proposals'][5]['proposed_minimal_delta']=group
  try:corrected(bad,bp)
  except AssertionError:rejected.append(name)
  else:raise AssertionError('Unsafe joint plan/audit mutation accepted '+name)
 for name,change in [('invent-oracle',lambda v:v['proposals'][5].update(actual_expected='pass')),('mutate-old-case',lambda v:next(c for c in v['owner_cases'] if c['id']=='DST-ROAR-007').update(input='Actually sweep gain-stage Frequency'))]:
  bad=deepcopy(a);change(bad)
  try:corrected(bad,p)
  except AssertionError:rejected.append(name)
  else:raise AssertionError('Unsafe mutation accepted '+name)
 for name in ['response-r2.json','README-r2.md','check-r2.py']:
  assert all(l.rstrip()==l for l in (A/name).read_text().splitlines()),name
 if (A/'manifest-r2.json').exists():
  mf=j(A/'manifest-r2.json');assert len(mf['files'])==3
  for q in mf['files']:pinned(q)
  assert {p.name for p in A.iterdir() if p.is_file()}=={Path(q['path']).name for q in response['preserved_R1_files']}|{'response-r2.json','README-r2.md','check-r2.py','manifest-r2.json'}
 assert before=={str(p):dg(p) for p in watch}
 print(json.dumps(dict(status='pass',sealed=(A/'manifest-r2.json').exists(),logical_field_changes=4,preserved_R1_files=6,immutable_inputs=89,owner_history_files=83,contexts=216,groups=10,questions=6,clauses=67,cases=190,all_actual_U=True,new_adoption=0,negative_fixtures=rejected,no_old_code_import_compile_main_replay=True,watched_paths=len(watch),all_unchanged=True,writes=False,independent_review='pending as of author freeze'),indent=2))
if __name__=='__main__':main()
