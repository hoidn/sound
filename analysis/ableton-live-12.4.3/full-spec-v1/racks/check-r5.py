"""Read-only R5 metadata correction checker; no old tool/import/replay/adapters."""
from pathlib import Path
from hashlib import sha256
from copy import deepcopy
import json,re,sys
P=Path(__file__).resolve().parent;R=P.parents[3]
def j(p):return json.loads(p.read_text())
def pin(p):
 b=p.read_bytes();return dict(path=str(p.relative_to(R)),bytes=len(b),sha256=sha256(b).hexdigest())
def qualified(old,new):
 assert len(new['groups'])==20
 expected=deepcopy(old)
 for i,g in enumerate(new['groups']):
  v=g['remaining_U'];assert isinstance(v,dict),'unqualified current no-adoption claim'
  assert set(v)=={'historical_source_audit_scope','current_owner_adoption','current_unknown_outcomes'}
  historical=v['historical_source_audit_scope']
  assert historical==dict(as_of='AS-OF SOURCE AUDIT',role='Inherited historical proposal scope only; not the current owner adoption disposition.',text=old['groups'][i]['remaining_U'])
  assert v['current_owner_adoption']==dict(bounded_new_requirement_IDs=10,bounded_new_cases=20,total_requirement_IDs=38,total_cases=101,metadata_correction_only=True)
  assert v['current_unknown_outcomes']=='Current remaining unknown outcomes: exact12.4.3 applicability, numeric/signal/time/file/protocol/RNG outcomes and source-silent lifecycle results remain U; failed, unavailable or empty positive prerequisites remain U. Bounded adoption does not complete any group/profile or supply an executed result.'
  assert 'No new normative ID/case adoption' not in v['current_unknown_outcomes']
  expected['groups'][i]['remaining_U']=v
 assert new==expected,'nonmetadata field changed'

def main():
 assert sys.dont_write_bytecode and sys.argv[1:]==['--check'],'Read-only --check only; no write mode'
 response=j(P/'response-r5.json');old=j(P/'adoption-r4.json');new=j(P/'adoption-r5.json')
 pins=response['prior_files']+[response['required_review']]
 inherited=j(R/response['inherited_immutable_inputs']['path'])['files'];pins+=inherited
 watched={R/q['path'] for q in pins}|{p for p in P.iterdir() if p.is_file()}|{R/q['path'] for q in response['canonical_pages']};before={str(p):pin(p) for p in watched}
 assert len(response['prior_files'])==67 and response['required_review']['sha256']=='6eca0b051ea6b33dd83a7666116d48d25d2be5374638da5d07567f199ca4881f'
 for q in pins:assert pin(R/q['path'])==q,q['path']
 qualified(old,new)
 deltas=[dict(json_pointer=f'/groups/{i}/remaining_U',before=old['groups'][i]['remaining_U'],after=new['groups'][i]['remaining_U']) for i in range(20)]
 assert response['exact_field_deltas']==deltas
 rejected=[]
 for label,edit in [
 ('unqualified-current-no-adoption',lambda d:d['groups'][0].update(remaining_U=old['groups'][0]['remaining_U'])),
 ('historical-label-erased',lambda d:d['groups'][1]['remaining_U']['historical_source_audit_scope'].update(as_of='CURRENT OWNER')),
 ('current-adoption-erased',lambda d:d['groups'][2]['remaining_U']['current_owner_adoption'].update(bounded_new_cases=0)),
 ('no-adoption-as-current-unknown',lambda d:d['groups'][3]['remaining_U'].update(current_unknown_outcomes=old['groups'][3]['remaining_U'])),
 ('behavioral-action-changed',lambda d:d['new_cases'][0].update(setup_action='label only'))]:
  bad=deepcopy(new);edit(bad)
  try:qualified(old,bad)
  except AssertionError:rejected.append(label)
  else:raise AssertionError('Unsafe fixture accepted '+label)
 # Preserve all38contracts/101objects through their existing immutable providers, no duplicate catalogs.
 req=j(P/'requirements-r4.json');cases=j(P/'cases-r4.json')['cases'];assert len(req)==38 and len(cases)==101 and new['new_cases']==old['new_cases']
 for q in response['current_behavior_providers']:assert pin(R/q['path'])==q
 status=j(P/'actual-status-r4.json')['cases'];assert len(status)==101 and all(x['actual_expected'] is None and x['actual_comparison'] is None and x['executed'] is False and x['target']=='U' for x in status)
 def bodies(text):return re.findall(r'^### (REQ-DEVICE-RACKS-\d+) — ([^\n]+)\n(.*?)(?=^### |^## |\Z)',text,re.M|re.S)
 links=0
 for x in response['canonical_pages']:
  before_text=(R/x['before_provider']['path']).read_text();out=before_text.replace('revision: 4\n','revision: 5\n',1)+x['appended']
  assert pin(R/x['before_provider']['path'])==x['before_provider'] and pin(R/x['after_provider']['path'])==x['after_provider']
  assert out==(R/x['path']).read_text()==(R/x['after_provider']['path']).read_text()
  if '/specs/' in x['path']:assert bodies(out)==bodies(before_text) and len(bodies(out))==38
  for dest in re.findall(r'\]\(([^)\s]+)\)',out):
   if re.match(r'^[a-z]+:',dest) or dest.startswith('#'):continue
   assert ((R/x['path']).parent/dest.split('#')[0]).exists(),dest;links+=1
 prior_paths={q['path'] for q in response['prior_files']}
 for p in watched:
  if p.parent==P and str(p.relative_to(R)) not in prior_paths or p in {R/q['path'] for q in response['canonical_pages']}:
   assert all(line.rstrip()==line for line in p.read_text().splitlines()),str(p)
 seal=P/'manifest-author-r5.json'
 if seal.exists():
  m=j(seal)
  for q in m['files']+m['current_canonical']:assert pin(R/q['path'])==q,q['path']
  assert {str(p.relative_to(R)) for p in P.iterdir() if p.is_file()}=={q['path'] for q in m['files']}|{str(seal.relative_to(R))}
 assert before=={str(p):pin(p) for p in watched}
 print(json.dumps(dict(status='pass',sealed=seal.exists(),prior_files=67,inherited_immutable_pins=len(inherited),metadata_fields=20,requirements_unchanged=38,case_objects_unchanged=101,new_case_source_claim_oracle_guard_changes=0,actual_nonnull=0,executed=0,complete=0,negative_fixtures=rejected,retained_positive='All20qualified historical-source/current-owner fields accepted;38requirement bodies and101caseobjects unchanged',links=links,watched_paths=len(watched),all_unchanged=True,writes=False,old_tools_replays_adapters_runtime=False),indent=2))
if __name__=='__main__':main()
