"""Finite scoped-owner reconciliation. --check is read-only; creation refuses after seal."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
import json,re,sys
P=Path(__file__).resolve().parent;ROOT=P.parents[3];B=P.parent
REQUIRED=[34,48,52,53,54,55,58,59,60,61,62,66,68]
load=lambda p:json.loads(p.read_text())
def digest(p):d=p.read_bytes();return dict(bytes=len(d),sha256=sha256(d).hexdigest())
def pointer(v,p):
 if not p:return v
 for k in p.strip('/').split('/'):
  k=k.replace('~1','/').replace('~0','~');v=v[int(k)] if isinstance(v,list) else v[k]
 return v

def references(plan,bindings):
 result=[]
 for ref in plan['owner_refs']:
  owner=bindings[ref['owner']];rmeta=owner['catalogs']['requirements'];rpath=P/rmeta['snapshot'];rs=load(rpath)
  ri=next(i for i,r in enumerate(rs) if r['id']==ref['requirement_id']);req=rs[ri];field=rmeta['predicate_field'];quoted=req[field]
  assert isinstance(quoted,str) and quoted
  cases=[];cmeta=owner['catalogs']['cases'];cs=load(P/cmeta['snapshot'])
  for cid in ref['case_ids']:
   ci=next(i for i,c in enumerate(cs) if c['id']==cid);c=cs[ci];actionfield=next(k for k in ['setup_and_action','setup_action','action'] if k in c)
   requirements=c.get('requirements',[c.get('requirement')]);assert ref['requirement_id'] in requirements,(ref,cid,requirements)
   # Preserve raw legacy meanings. expected/predicate/comparator are documentary
   # in older catalogs, not actual passed output. No field is silently renamed.
   if 'target_grade' in c:assert c['target_grade']=='U' and c['expected'] is c['comparison'] is None and c['executed'] is False
   elif cmeta['origin'] is not None:assert c.get('exact_target',c.get('exact_12_4_3'))=='U' and c['execution']=='not-run'
   cases.append(dict(owner=ref['owner'],owner_packet=owner['owner_packet'],id=cid,snapshot_catalog=cmeta['snapshot'],json_pointer=f'/{ci}',action_json_pointer=f'/{ci}/{actionfield}',quoted_action=c[actionfield],original_catalog=cmeta['origin'],original_json_pointer=f'/{ci}' if cmeta['origin'] else None,catalog_kind=cmeta['kind'],raw_proposal_and_target_fields={k:c[k] for k in c if k in ['expected','comparison','documentary_expected','documentary_comparator','predicate','comparator','unknown','unresolved_probe','documentary_context','basis','provenance','kind','exact_target','exact_12_4_3','target_grade','executed','execution']},field_semantics=owner['case_field_semantics']))
  result.append(dict(owner=ref['owner'],owner_packet=owner['owner_packet'],id=ref['requirement_id'],snapshot_catalog=rmeta['snapshot'],json_pointer=f'/{ri}',predicate_json_pointer=f'/{ri}/{field}',quoted_scoped_predicate=quoted,original_catalog=rmeta['origin'],original_json_pointer=f'/{ri}' if rmeta['origin'] else None,catalog_kind=rmeta['kind'],relationship=ref['relationship'],cases=cases))
 return result

def verify_units(units,blocks):
 assert {u['block'] for u in units}=={f'SET-B{i:03d}' for i in REQUIRED}
 ids=set()
 for u in units:
  assert u['id'] not in ids;ids.add(u['id']);b=blocks[u['block']]
  assert u['paragraph_text']==b['text'] and b['text'][slice(*u['source_phrase_span'])]==u['source_phrase']
  assert u['actual_expected'] is u['actual_comparison'] is None and u['target_grade']=='U' and u['executed'] is False and not u['complete']
  for r in u['owner_references']:
   req=pointer(load(P/r['snapshot_catalog']),r['json_pointer']);assert req['id']==r['id']
   assert pointer(load(P/r['snapshot_catalog']),r['predicate_json_pointer'])==r['quoted_scoped_predicate']
   for c in r['cases']:
    assert c['owner']==r['owner']
    value=pointer(load(P/c['snapshot_catalog']),c['json_pointer']);assert value['id']==c['id']
    assert r['id'] in value.get('requirements',[value.get('requirement')])
    assert pointer(load(P/c['snapshot_catalog']),c['action_json_pointer'])==c['quoted_action']

def build():
 for r in load(P/'source-input-pins.json'):assert digest(ROOT/r['path'])=={k:r[k] for k in ['bytes','sha256']}
 audit=B/'settings-source-audit/manifest-r2.json';assert digest(audit)['sha256']=='e443795e09bdeae4f022043fd9a9244305aecaea3459d084506ccf854d248186'
 bindings={b['owner']:b for b in load(P/'owner-bindings.json')};assert len(bindings)==14
 for owner in bindings.values():
  spec=(P/owner['spec_snapshot']).read_text();assert digest(P/owner['spec_snapshot'])==owner['canonical_as_of_identity']
  assert digest(P/owner['manifest_snapshot'])==owner['manifest_as_of_identity']
  for key,meta in owner['catalogs'].items():
   if meta['origin'] is not None:assert digest(P/meta['snapshot'])=={k:meta[k] for k in ['bytes','sha256']}
   else:
    for record in load(P/meta['snapshot']):
     start,end=record['spec_character_span'];quote=record.get('quote',record.get('raw_row'));assert spec[start:end]==quote
  assert 'not a new live replay pin' in owner['scope']
 qctx=load(P/'q031-context.json');assert sha256(qctx['text'].encode()).hexdigest()==qctx['excerpt_sha256']
 source=load(B/'settings-learning/source.json');bs=load(B/'settings-learning/source-blocks.json');blocks={b['id']:b for b in bs};assert len(bs)==70
 units=[]
 for i,plan in enumerate(load(P/'plan.json'),1):
  b=blocks[plan['block']];phrase=plan['source_phrase'];start=b['text'].index(phrase)
  units.append(dict(id=f'SOR-{i:03d}',**plan,source_phrase_span=[start,start+len(phrase)],paragraph_text=b['text'],source_locator=dict(source_id=source['id'],source_sha256=source['sha256'],source_capture_utc=source['capture_utc'],source_version=source['version'],block_catalog=str((B/'settings-learning/source-blocks.json').relative_to(ROOT)),block_json_pointer='/'+str(bs.index(b)),text_json_pointer='/'+str(bs.index(b))+'/text',html_line=b['html_line'],heading_context_anchor=b['anchor'],anchor_role='retained extraction heading context, not a direct ID on this list/paragraph',heading_context_url=source['url']+'#'+b['anchor']),owner_references=references(plan,bindings),actual_expected=None,actual_comparison=None,target_grade='U',executed=False,complete=False,adoption='none; source/owner scoped assessment only',semantic_coverage='partial-or-unknown; a pointer/owner link is not coverage'))
 verify_units(units,blocks)
 # Separate Q031 scope assessment: neither owner statement nor palette/RNG law is adopted.
 colorblock=blocks['SET-B041'];cv=load(B/'clip-view/manual-blocks.json')[22];assert cv['locator']=='CV:B023'
 colorrefs=references(dict(owner_refs=[dict(owner='settings',requirement_id='REQ-SETTINGS-LEARNING-016',case_ids=['SET-016'],relationship='Settings R1 explicit new-clip preference context'),dict(owner='clip',requirement_id='REQ-CLIP-VIEW-005',case_ids=['CV-005'],relationship='unqualified inheritance wording; case mainly Assign Color/palette, not matched creation preference')]),bindings)
 color=dict(question='Q-031',status='separate-non-adoption; matched target version/preference context unresolved',source_contexts=[dict(catalog=str((B/'settings-learning/source-blocks.json').relative_to(ROOT)),pointer='/40',record=colorblock,source=source),dict(catalog=str((B/'clip-view/manual-blocks.json').relative_to(ROOT)),pointer='/22',record=cv,source=load(B/'clip-view/source.json'))],owner_references=colorrefs,assessment='First Steps explicitly allows random or track color for new clips; ClipView source paragraph/005 describes new clips using track color without declaring that preference. Retain both current-Version12 source contexts and different capture identities. They do not establish a target contradiction, factory preference, all-created-clip rule, random-result inequality or distribution. SET-016 explicitly compares modes in separate histories; CV-005 mainly exercises Assign Color/palette and lacks a creation trial with matched preference. A later separately reviewed owner successor would need matched admitted build/preference/new-clip histories; this reconciliation adopts none.',no_adoption=True,actual_expected=None,actual_comparison=None,documentary_expected=None,documentary_comparator=None,target_grade='U',executed=False,complete=False,question_excerpt=load(P/'q031-context.json'))
 summary=dict(scope='13 specified FirstSteps paragraphs only, plus separate Q031 non-adoption; not a full chapter/owner/product audit',paragraphs=13,subclaims=len(units),owners_snapshotted=14,dispositions=dict(Counter(u['disposition'] for u in units)),requirement_reference_occurrences=sum(len(u['owner_references']) for u in units),case_reference_occurrences=sum(len(r['cases']) for u in units for r in u['owner_references']),new_normative_requirements=0,owner_or_shared_mutations=0,source_recapture_or_runtime=False,all_reconciliation_actual_outcomes_null_U_unexecuted=True,proven_cross_owner_conflicts=0,Q031='separate non-adoption assessment; source qualification unresolved',source_read_scope='Read all13 exact specified paragraphs and relevant actual owner clauses/actions quoted at their packet-qualified pointers, preserving cases/conditions/legacy documentary roles. References are scoped subsets, context or gaps. Linked destination pixels/pages and other owner state spaces are outside this bounded reconciliation.',owner_snapshot_policy='As-of immutable local copies and existing exact R1/R2 spec snapshots; no new live canonical replay pins. Settings snapshot is explicitly R1 21requirements/30cases; later mutable owner versions are outside this captured assessment.')
 return dict(ledger=units,clip_color_non_adoption=color,summary=summary)

def fixtures(units,blocks):
 tests=0
 def reject(changed):
  nonlocal tests
  try:verify_units(changed,blocks)
  except (AssertionError,KeyError,IndexError,TypeError):tests+=1;return
  raise AssertionError('Invalid reconciliation fixture accepted')
 import copy
 reject([u for u in units if u['block']!='SET-B034'])
 c=copy.deepcopy(units);c[0]['source_phrase']='invented';reject(c)
 c=copy.deepcopy(units);c[0]['owner_references'][0]['predicate_json_pointer']='/999/body';reject(c)
 c=copy.deepcopy(units);c[0]['actual_expected']='pass';reject(c)
 # RC-002 exists in two packets: changing only its owner must not be accepted.
 c=copy.deepcopy(units);u=next(u for u in c if any(r['owner']=='remote' and r['id']=='REQ-REMOTE-WORKFLOW-002' for r in u['owner_references']));r=next(r for r in u['owner_references'] if r['owner']=='remote');r['cases'][0]['owner']='recording';reject(c)
 assert tests==5;return dict(dropped_paragraph_rejected=True,changed_quote_rejected=True,invalid_pointer_rejected=True,invented_actual_grade_rejected=True,cross_packet_RC_ID_collision_rejected=True)

def main():
 assert sys.argv[1:] in (['--check'],['--create'],['--preflight'])
 check=sys.argv[1:]==['--check'];preflight=sys.argv[1:]==['--preflight']
 if not check:assert not (P/'manifest.json').exists(),'Frozen packet; successor required'
 before={str(p.relative_to(P)):digest(p) for p in P.rglob('*') if p.is_file()}
 data=build();data['summary']['selfchecks']=fixtures(data['ledger'],{b['id']:b for b in load(B/'settings-learning/source-blocks.json')})
 files={'ledger.json':data['ledger'],'clip-color-non-adoption.json':data['clip_color_non_adoption'],'summary.json':data['summary']}
 if check or preflight:
  for name,v in files.items():assert load(P/name)==v,name
  if check:
   m=load(P/'manifest.json');assert set(before)==set(m['files'])|{'manifest.json'}
   for n,r in m['files'].items():assert digest(P/n)==r,n
  for n in before:
   if n.startswith('owners/'):continue
   path=P/n;text=path.read_text();assert text.endswith('\n') and all(line==line.rstrip() for line in text.splitlines()),path
  for link in re.findall(r'\]\(([^)]+)\)',(P/'README.md').read_text()):assert (P/link.split('#')[0]).resolve().is_file(),link
  assert before=={str(p.relative_to(P)):digest(p) for p in P.rglob('*') if p.is_file()}
  print(json.dumps(dict(status='passed-read-only-preflight' if preflight else 'passed-read-only-frozen',immutable_source_pins=len(load(P/'source-input-pins.json')),summary=data['summary']),indent=2))
 else:
  for name,v in files.items():(P/name).write_text(json.dumps(v,indent=2)+'\n')
if __name__=='__main__':main()
