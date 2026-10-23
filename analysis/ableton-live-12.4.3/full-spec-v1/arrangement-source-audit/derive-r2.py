"""ASA-REVIEW-001 only: derive three corrected historical case-association assessments."""
from pathlib import Path
from copy import deepcopy
import json,runpy,sys
P=Path(__file__).resolve().parent
load=lambda p:json.loads(p.read_text())
ASSESSMENT="Session001/SV001 actually selects clip A by name then presses Enter, navigates to B with arrows and separately clicks B's triangular launch control. The source contract permits launch at any time and in any order, but these selected historical R1 actions do not exercise a deliberate nonsequential history. Later Session R3 SV041 is not borrowed into this as-of association. SessionLaunch001/008 actual setting roles remain selected context; Session Launch Mode is not applied to Arrangement clips."
def corrected():
 old=runpy.run_path(str(P/'derive.py'))['build']()
 for n,v in old.items():assert load(P/n)==v,'Preserved R1 derivation: '+n
 plan=deepcopy(load(P/'claim-plan.json'));claims=deepcopy(old['claims.json'])
 for r in plan['CON-B032']:r['assessment']=ASSESSMENT
 hits=[c for c in claims if c['source_block']=='CON-B032'];assert [c['id'] for c in hits]==['ASA-C270','ASA-C271','ASA-C272']
 for c in hits:c['assessment']=ASSESSMENT
 return {'claim-plan-r2.json':plan,'claims-r2.json':claims}
def verify(plan,claims):
 expected=corrected();assert plan==expected['claim-plan-r2.json'] and claims==expected['claims-r2.json']
 # Actual original R1 gesture, source predicate and arbitrary-order text remain distinct.
 ext=load(P/'selected-owner-contexts.json');case=next(r for r in ext if r['id']=='SV-001')
 assert case['catalog'].endswith('/session-workflows/cases.json') and case['json_pointer']=='/0'
 assert case['quoted_scoped_predicate']['setup_and_action']=="Select owned clip A by name, press Enter, navigate to B with arrows and separately click B's triangular launch control."
 assert not any('041' in r['id'] for c in claims if c['source_block']=='CON-B032' for r in c['selected_external_contexts'])
 assert any('in any order' in c['source_excerpt'] for c in claims if c['source_block']=='CON-B032')
def main():
 assert sys.dont_write_bytecode and sys.argv[1:] in (['--check'],['--write'])
 if sys.argv[1:]==['--write']:assert not (P/'manifest-author-r2.json').exists(),'refuse overwrite after R2 seal'
 result=corrected()
 for n,v in result.items():
  if sys.argv[1:]==['--check']:assert load(P/n)==v,n
  else:(P/n).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
 verify(result['claim-plan-r2.json'],result['claims-r2.json'])
 print(json.dumps(dict(status='pass',scope='Focused historical source/case-association wording only',corrected_plan_rows=3,corrected_claims=3,all_other_fields_unchanged=True,source_or_case_IDs_changed=0,new_normative_IDs=0,target='U',executed=0,complete=0),indent=2))
if __name__=='__main__':main()
