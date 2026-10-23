"""Exact cross-packet direct-member routing, not API semantic completion."""
from pathlib import Path
import hashlib,json,sys
P=Path(__file__).resolve().parent
BASE=P.parents[1]
ROOT=BASE.parents[2]
M=BASE/'max-api'
load=lambda p:json.loads(p.read_text())
sha=lambda b:hashlib.sha256(b).hexdigest()
FAMILIES=[('live-api-clip-sample','members.json','manifest-author-r1.json','live-api-clip-sample-review.json'),('live-api-core-session','member-ledger.json','manifest-author-r2.json','live-api-core-session-review-final.json'),('live-api-device-rack','member-ledger.json','manifest-author-r1.json','live-api-device-rack-review.json'),('live-api-control-tuning','member-ledger.json','manifest-author-r2.json','live-api-control-tuning-review-final.json'),('live-api-specialized-devices','member-ledger.json','manifest-author-r1.json','live-api-specialized-devices-review.json')]
def build():
 pins={}
 def pin(path):
  raw=path.read_bytes();rel=str(path.relative_to(ROOT));pins[rel]=dict(path=rel,bytes=len(raw),sha256=sha(raw));return rel
 for name in ['lom-entries.json','lom-members.json','manifest-inventory-r1.json','source-page-r1.md']:
  pin(M/name)
 for name,info in load(M/'manifest-inventory-r1.json')['files'].items():
  path=M/name;pin(path);assert pins[str(path.relative_to(ROOT))]['bytes']==info['bytes'] and pins[str(path.relative_to(ROOT))]['sha256']==info['sha256']
 original_entries=load(M/'lom-entries.json');original_members=load(M/'lom-members.json')
 original={m['id']:m for m in original_members}
 routed={};entry_owners={};requirements=[];caseindex=[];familyrows=[]
 for family,ledgerfile,manifestfile,reviewfile in FAMILIES:
  q=BASE/family;manifest=load(q/manifestfile);pin(q/manifestfile)
  for name,info in manifest['files'].items():
   path=q/name;pin(path);assert pins[str(path.relative_to(ROOT))]['bytes']==info['bytes'] and pins[str(path.relative_to(ROOT))]['sha256']==info['sha256']
  review=BASE/'reviews'/reviewfile;pin(review)
  evidence=load(review)
  assert evidence.get('reviewed_manifest_sha256',evidence.get('manifest_sha256',evidence.get('author_manifest_sha256')))==sha((q/manifestfile).read_bytes()),reviewfile
  assert 'approved' in evidence['disposition'],reviewfile
  rs=load(q/'requirements.json');cs=load(q/'cases.json');ledger=load(q/ledgerfile)
  rp=pin(q/'requirements.json');cp=pin(q/'cases.json');lp=pin(q/ledgerfile)
  reqindex={r['id']:(i,r) for i,r in enumerate(rs)};assert len(reqindex)==len(rs)
  caseids={c['id'] for c in cs};assert len(caseids)==len(cs)
  for i,r in enumerate(rs):
   requirements.append(dict(id=r['id'],packet=family,source=dict(path=rp,pointer=f'/{i}'),provenance=r.get('provenance',r.get('strength')),target_applicability=r['target_applicability'],semantic_complete=False))
  for i,c in enumerate(cs):
   assert c['expected'] is None and c['comparison'] is None and c['documentary_expected'] is None and c['documentary_comparator'] is None
   assert c['target_grade']=='U' and c['executed'] is False and set(c['requirements'])<=set(reqindex)
   caseindex.append(dict(packet=family,id=c['id'],source=dict(path=cp,pointer=f'/{i}'),requirements=c['requirements'],kind=c['kind'],documentary_expected_null=True,documentary_comparator_null=True,target_expected_null=True,target_comparison_null=True,target_grade='U',executed=False))
  for i,row in enumerate(ledger):
   mid=row.get('id',row.get('member',row.get('inventory_member_id',row.get('inventory_member',{}).get('id'))))
   rids=row.get('requirements') or [row.get('requirement',row.get('requirement_id'))]
   assert mid in original and mid not in routed and rids and all(r in reqindex for r in rids)
   refs=[dict(path=rp,pointer=f'/{reqindex[r][0]}',id=r,provenance=reqindex[r][1].get('provenance',reqindex[r][1].get('strength'))) for r in rids]
   cref=[dict(path=cp,pointer=f'/{j}',id=c['id']) for j,c in enumerate(cs) if set(c['requirements'])&set(rids)]
   assert cref
   source=original[mid];eid=source['reference_entry']
   if eid in entry_owners:assert entry_owners[eid]==family
   entry_owners[eid]=family
   routed[mid]=dict(inventory_member=source,packet=family,ledger=dict(path=lp,pointer=f'/{i}'),requirements=refs,cases=cref,documentary_status='explicit-semantic-U' if all(r['provenance']=='U' for r in refs) else 'partial-current-public-role',target_applicability='U',semantic_complete=False)
  # Include the zero-direct-member this_device entry by exact retained source ID.
  sourceids={s['id'] for s in load(q/'sources.json')}
  for e in original_entries:
   if e['source_id'] in sourceids:
    assert e['id'] not in entry_owners or entry_owners[e['id']]==family
    entry_owners[e['id']]=family
  familyrows.append(dict(packet=family,manifest=str((q/manifestfile).relative_to(ROOT)),manifest_sha256=sha((q/manifestfile).read_bytes()),review=str(review.relative_to(ROOT)),review_sha256=sha(review.read_bytes()),direct_members=len(ledger),requirements=len(rs),cases=len(cs),semantic_complete_members=0))
 assert len(routed)==588 and set(routed)==set(original)
 assert len(entry_owners)==45 and set(entry_owners)=={e['id'] for e in original_entries}
 assert len({r['id'] for r in requirements})==len(requirements)==626
 assert {r['provenance'] for r in requirements}=={'D-current-public','U'}
 assert len({(c['packet'],c['id']) for c in caseindex})==len(caseindex)==702
 entries=[dict(inventory_entry=e,packet=entry_owners[e['id']],mapped_direct_members=len(e['declared_members']),target_applicability='U',semantic_complete=False) for e in original_entries]
 members=[routed[m['id']] for m in original_members]
 assert sum(e['mapped_direct_members'] for e in entries)==588
 assert sum(m['documentary_status']=='explicit-semantic-U' for m in members)==1
 summary=dict(scope='Exact direct-member routing only; no complete API or target compatibility',reference_entries=45,direct_members=588,partial_current_public_member_roles=587,heading_only_semantic_U_members=1,zero_member_root_context_entries=1,requirements=626,packet_qualified_cases=702,unqualified_case_id_count=len({c['id'] for c in caseindex}),semantic_complete_members=0,semantic_complete_entries=0,all_actual_documentary_target_oracles_null=True,all_target_U_unexecuted=True,inherited_alias_root_closure='unknown; not flattened',bridge_workflows='separate overlapping owner; excluded from this direct-member count',families=familyrows)
 return {'entry-mappings.json':entries,'member-mappings.json':members,'requirement-index.json':requirements,'case-index.json':caseindex,'summary.json':summary,'input-pins.json':[pins[k] for k in sorted(pins)]}
if __name__=='__main__':
 assert sys.argv[1:] in ([],['--check'])
 outputs=build()
 if sys.argv[1:]:
  for name,data in outputs.items():assert load(P/name)==data,name
  manifest=load(P/'manifest.json')
  for name,info in manifest['files'].items():
   raw=(P/name).read_bytes();assert len(raw)==info['bytes'] and sha(raw)==info['sha256'],name
  print(json.dumps(dict(status='pass',reference_entries=45,direct_members=588,requirements=626,packet_qualified_cases=702,semantic_complete_members=0,external_pins=len(outputs['input-pins.json']),writes=False)))
 else:
  assert not (P/'manifest.json').exists(),'sealed; create an explicit successor'
  for name,data in outputs.items():(P/name).write_text(json.dumps(data,indent=2)+'\n')
  print(json.dumps(outputs['summary.json'],indent=2))
