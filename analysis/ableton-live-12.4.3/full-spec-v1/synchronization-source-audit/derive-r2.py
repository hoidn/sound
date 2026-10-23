"""Focused analyst audit correction; all original R1 files remain unchanged.
--check prints comparison only; --write refuses once the R2 manifest exists.
"""
from pathlib import Path
from hashlib import sha256
import copy,json,sys
P=Path(__file__).resolve().parent;A=P/'archive-r1'
load=lambda q:json.loads(q.read_text())

def build():
 names={'source-unit-ledger':'source-unit-ledger-r2','gap-proposals':'gap-proposals-r2','catalog-reconciliation':'catalog-reconciliation-r2','summary':'summary-r2'}
 old={name:load(A/(name+'.json')) for name in names};new=copy.deepcopy(old)
 unit=new['source-unit-ledger'][78];assert unit['id']=='SYNC-A079' and unit['block_id']=='SYNC-B035'
 assert unit['disposition']=='represented-partial-source-clause-and-case' and unit['cases'][0]['id']=='SYNC-012' and not unit['gap_ids']
 related_case=copy.deepcopy(unit['cases'][0]);old_req=copy.deepcopy(unit['requirements'])
 unit['disposition']='missing-clause-case-or-context'
 unit['cases']=[]
 unit['judgment']='The source clause faithfully states hidden Follow nonoperation, but case012 establishes active input and visibility, not an explicitly active Follower or known tempo interpretation before hiding. Active input is not a positive processing baseline; a separate running-Follower-before-hide action is missing.'
 unit['gap_ids']=['SA-G09']
 gap=dict(id='SA-G09',title='Running-Follower baseline before hiding Follow',kind='missing-positive-processing-baseline-and-targeted-case',blocks=['SYNC-B035'],clause_delta='No normative source clause changes: existing REQ-SYNC-WORKFLOW-012 already records hidden Follow nonoperation. This is an audit case-context correction only; no detector algorithm or timing law.',case_delta='Future evidence only, not execution authorization: on an independently admitted configured nonzero input and supported exact-build feature, show and explicitly activate Follow. Independently establish a separately known genuine positive interpretation/tempo-following baseline, not merely active input, a lit button or a peer count. Then hide only Follow while retaining the same input/source context and record control and actual processing state. Missing capability or failed positive baseline remains U, never a negative pass. Keep documentary/actual outputs and comparators null; no numeric tracking tolerance, acquisition/cessation deadline, automatic re-enable, restoration or default law.',source_units=['SYNC-A079'],current_context_only_requirements=old_req,current_context_only_cases=[related_case],status='audit-proposal-only; not a current normative clause/case and not a finding that partial approval was false',documentary_expected=None,documentary_comparator=None,expected=None,comparison=None,target_grade='U',executed=False)
 assert len(new['gap-proposals'])==8;new['gap-proposals'].append(gap)
 row=next(x for x in new['catalog-reconciliation']['cases'] if x['reference']['id']=='SYNC-012')
 assert row['source_units'].count('SYNC-A079')==1;row['source_units'].remove('SYNC-A079')
 summary=new['summary'];summary['dispositions']['represented-partial-source-clause-and-case']-=1;summary['dispositions']['missing-clause-case-or-context']+=1;summary['gaps']+=1
 # Enumerate the exact finite correction; no unrelated prose/source/case/oracle rewrite.
 deltas=[]
 for key in ['disposition','cases','judgment','gap_ids']:
  deltas.append(dict(old_file='source-unit-ledger.json',new_file='source-unit-ledger-r2.json',pointer='/78/'+key,operation='replace',old=old['source-unit-ledger'][78][key],new=new['source-unit-ledger'][78][key]))
 deltas.append(dict(old_file='gap-proposals.json',new_file='gap-proposals-r2.json',pointer='/8',operation='add',old=None,new=gap))
 ci=next(i for i,r in enumerate(old['catalog-reconciliation']['cases']) if r['reference']['id']=='SYNC-012')
 deltas.append(dict(old_file='catalog-reconciliation.json',new_file='catalog-reconciliation-r2.json',pointer=f'/cases/{ci}/source_units',operation='replace',old=old['catalog-reconciliation']['cases'][ci]['source_units'],new=row['source_units']))
 for keys in [('dispositions','represented-partial-source-clause-and-case'),('dispositions','missing-clause-case-or-context'),('gaps',)]:
  a,b=old['summary'],new['summary']
  for k in keys:a,b=a[k],b[k]
  deltas.append(dict(old_file='summary.json',new_file='summary-r2.json',pointer='/'+'/'.join(keys),operation='replace',old=a,new=b))
 review=A/'review-r1.json'
 response=dict(id='SYNCHRONIZATION-SOURCE-AUDIT-RESPONSE-R2',revision=2,finding='SYNC-SOURCE-AUDIT-REVIEW-001',review=dict(path='analysis/ableton-live-12.4.3/full-spec-v1/reviews/synchronization-source-audit-review.json',archive='archive-r1/review-r1.json',bytes=review.stat().st_size,sha256=sha256(review.read_bytes()).hexdigest()),original_manifest_sha256='72d2b3c6d6229d5f5a0a9f6fcc6f9477811c82637b58740ca14068342a6ba615',field_deltas=deltas,scope='Exactly one audit sufficiency classification, one related case-unit index, one all-null/U audit proposal and dependent counts. All129 other units, original clauses/actions/oracles/source/locators/pointers and all15 R1 root files stay byte-identical.',normative_owner_changes=False,actual_execution=False,independent_focused_rereview='pending')
 out={names[k]:v for k,v in new.items()};out['response-r2']=response
 return out

def main():
 assert sys.argv[1:] in (['--write'],['--check']),'choose --check or initial --write'
 if sys.argv[1:]==['--write']:
  assert not (P/'manifest-author-r2.json').exists(),'refuse R2 mutation after seal'
  for name,value in build().items():(P/(name+'.json')).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
 else:
  for name,value in build().items():assert load(P/(name+'.json'))==value,name
 print(json.dumps(dict(status='pass',scope='focused proposed audit correction only',source_units=130,gap_spans=10,gap_proposals=9,exact_JSON_field_deltas=9,all_target_U=True,normative_changes=False,execution=False),indent=2))
if __name__=='__main__':main()
