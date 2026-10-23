"""Current Session append-only source/delta checks; read-only, never host execution."""
from pathlib import Path
from hashlib import sha256
from copy import deepcopy
from collections import Counter
import ast,json,re,runpy,subprocess,sys
P=Path(__file__).resolve().parent;ROOT=P.parents[3];A=P.parent/'session-grid-source-audit'
load=lambda p:json.loads(p.read_text())
def dg(p):
 b=p.read_bytes();return dict(bytes=len(b),sha256=sha256(b).hexdigest())
def pin(p,row):assert dg(p)=={k:row[k] for k in ['bytes','sha256']},str(p)
def tree():return {str(p.relative_to(P)):dg(p) for p in P.rglob('*') if p.is_file()}
def pointer(v,ptr):
 for k in ptr.split('/')[1:]:v=v[int(k)] if isinstance(v,list) else v[k.replace('~1','/').replace('~0','~')]
 return v
def check(r,c,adoption,fixture):
 oldr,oldc=load(P/'requirements.json'),load(P/'cases.json')
 assert len(r)==30 and len(c)==57 and r[:29]==oldr and c[:40]==oldc
 assert len({x['id'] for x in r})==30 and len({x['id'] for x in c})==57
 assert [x['id'] for x in c[40:]]==[f'SV-{i:03}' for i in range(41,56)]+['SV-U-ARRANGEMENT-STOP','SV-U-COPY-INDEPENDENCE']
 assert Counter(x['strength'] for x in r)=={'D12':29,'U':1}
 assert r[-1]['id']=='REQ-SESSION-VIEW-030' and r[-1]['evidence'][0]['block']=='SV-B060'
 assert 'entrypoint roles only' in r[-1]['contract']
 ids={x['id'] for x in r};blocks=load(A/'source-blocks.json')
 for row in r:
  assert row['target_applicability']=='U'
  for e in row['evidence']:
   b=blocks[int(e['block'][-3:])-1];assert b['id']==e['block'] and b['html_line']==e['html_line']
   assert b['old_packet_anchor_context']==e['anchor']
 for row in c:
  assert row['expected'] is row['comparison'] is None and row['target_grade']=='U' and row['executed'] is False
  assert set(row['requirements'])<=ids
 assert sum(x['documentary_comparator'] is not None for x in c)==38
 assert Counter(x['provenance'] for x in c[40:])=={'D12':15,'U':2}
 for row in c[40:]:
  assert row['source_claim'] and 'F-SV-R3' in row['preconditions']
  assert len(row['source_context'])==len(row['evidence'])
  for loc,e in zip(row['source_context'],row['evidence']):
   assert loc['catalog']=='../session-grid-source-audit/source-blocks.json'
   b=pointer(blocks,loc['json_pointer']);assert loc['block']==b['id']==e['block'] and b['html_line']==e['html_line']
 byid={x['id']:x for x in c}
 for id in ['SV-047','SV-051','SV-055','SV-U-ARRANGEMENT-STOP','SV-U-COPY-INDEPENDENCE']:
  assert byid[id]['documentary_expected'] is byid[id]['documentary_comparator'] is None
 assert 'SV-B060' in [x['block'] for x in byid['SV-053']['evidence']]
 assert 'genuinely successful scene Copy/Paste baseline' in byid['SV-053']['setup_and_action']
 assert 'genuinely playing nonempty Arrangement clips' in byid['SV-U-ARRANGEMENT-STOP']['setup_and_action']
 assert 'active transport' in byid['SV-U-ARRANGEMENT-STOP']['setup_and_action']
 assert 'unmuted nonzero outputs' in byid['SV-U-ARRANGEMENT-STOP']['setup_and_action']
 assert 'Independently play nonempty' in byid['SV-052']['setup_and_action'] and 'unmuted nonzero output' in byid['SV-052']['setup_and_action']
 assert all('genuinely' in byid[id]['setup_and_action'] for id in ['SV-053','SV-055'])
 assert [g['group'] for g in adoption]==[f'SGA-G{i:02}' for i in range(1,18)]
 assert Counter(g['disposition'] for g in adoption)=={'bounded-local-source-context':13,'bounded-U-probe-only':2,'external-owner-pending':2}
 for g in adoption:
  assert g['coverage_credit']==0 and g['complete'] is False
  for ref in g['current_case_pointers']:
   assert ref['catalog']=='cases-r3.json';case=pointer(c,ref['json_pointer']);assert case['id']==ref['id'] and g['group'] in case['audit_groups']
 assert adoption[9]['disposition']==adoption[12]['disposition']=='external-owner-pending'
 assert adoption[9]['current_case_pointers']==adoption[12]['current_case_pointers']==[]
 probe=fixture['group_probe'];assert probe['id']=='MXW-U-GROUP-SLOT' and probe['json_pointer']=='/45'
 group=pointer(load(P/probe['catalog']),probe['json_pointer'])
 assert group['id']==probe['id'] and 'genuinely playing nonempty contained clips' in group['setup_and_action']
 assert group['expected'] is group['comparison'] is group['source_claim'] is None
 assert not any('GROUP-SLOT' in row['id'] for row in c[40:])
 assert fixture['Arrangement_stop_positive_required'] is True
 assert fixture['expected'] is fixture['comparison'] is fixture['numeric_signal_file_timing_oracles'] is None
 assert fixture['target']=='U' and fixture['executed'] is False
def main():
 assert sys.dont_write_bytecode and sys.argv[1:]==['--check'],'Use python3 -B validate-r3.py --check'
 before=tree();inputs=load(P/'inputs-r3.json');assert len({r['path'] for r in inputs})==len(inputs)==57
 ebefore={r['path']:dg(ROOT/r['path']) for r in inputs}
 for x in inputs:pin(ROOT/x['path'],x)
 prior=load(P/'prior-files-r3.json');assert len(prior)==33
 for name,row in prior.items():pin(P/name,row)
 assert dg(P/'manifest-author-r2.json')['sha256']=='2465c28d4131f8d895c4e17ac5f23b43f41789e99ab59c2a93ba9cc14edc4cf5'
 for beforefile,provider in [('spec-before-r3.md','spec-r2.md'),('research-before-r3.md','research-r2.md')]:assert (P/beforefile).read_bytes()==(P/provider).read_bytes()
 assert dg(A/'manifest.json')['sha256']=='bc6255963fc90f29d34c729a8d2d984fe40546c90b17798e240db5db1eed55c8'
 mf=load(A/'manifest.json');assert len(mf['files'])==36
 for name,row in mf['files'].items():pin(A/name,row)
 assert load(P.parent/'reviews/session-grid-source-audit-review.json')['disposition']=='approved-partial-source-audit'
 source=load(P/'source.json');raw=(ROOT/source['path']).read_text();pin(ROOT/source['path'],source)
 parsed,resources=runpy.run_path(str(A/'source_parser.py'))['extract'](raw,'SV');stored=load(A/'source-blocks.json')
 assert len(parsed)==77 and len(resources)==59
 for a,b in zip(parsed,stored):
  assert all(a[k]==b[k] for k in a)
  assert raw[a['raw_start']:a['raw_end']]==a['raw_html']
 author=runpy.run_path(str(P/'author-r3.py'));built=author['build']()
 for name,value in built.items():assert load(P/name)==value,name
 r,c,adoption,fixture=(built[n] for n in ['requirements-r3.json','cases-r3.json','audit-adoption-r3.json','fixtures-r3.json'])
 check(r,c,adoption,fixture)
 assert built['delta-r3.json']['changed_old_fields']==[]
 for snap,canonical in [('spec-r3.md','wiki/specs/session-view-workflows.md'),('research-r3.md','wiki/research/session-view-workflows.md')]:
  assert (P/snap).read_bytes()==(ROOT/canonical).read_bytes()
  assert 'revision: 3' in (P/snap).read_text() and '**AS-OF AUTHOR FREEZE:**' in (P/snap).read_text()
 spec=(P/'spec-r3.md').read_text();oldspec=(P/'spec-before-r3.md').read_text()
 for row in r[:29]:
  assert row['contract'] in spec and row['contract'] in oldspec
 assert r[-1]['contract'] in spec
 impact=load(P/'consumer-impact-r3.json');assert len(impact['records'])==33 and len({x['consumer'] for x in impact['records']})==27
 for row in impact['records']:
  snapshot=P/row['historical_snapshot'];assert dg(snapshot)['sha256']==row['literal_sha256']
 # Historical metadata paths are not reopened as evolving current gates.
 assert impact['historical_consumers_replayed'] is impact['consumer_files_modified'] is False
 # Execute only four inspected pure Browser definitions, not its build/import path.
 tree_ast=ast.parse((ROOT/'tools/spec_browser.py').read_text());names={'anchor','frontmatter','cells','spec_rows'}
 functions=[n for n in tree_ast.body if isinstance(n,ast.FunctionDef) and n.name in names];assert len(functions)==4
 env={'re':re};exec(compile(ast.Module(body=functions,type_ignores=[]),'analyst-four-browser-functions','exec'),env)
 browsed=env['spec_rows'](Path('session-view-workflows.md'),spec);assert {x['id'] for x in browsed}=={x['id'] for x in r} and len(browsed)==30
 rejected=0
 for name in ['old-record-change','wrong-new-source','remove-Arrangement-baseline','actual-oracle','false-external-closure','duplicate-group-probe','clipboard-failed-baseline']:
  rr,cc,aa,ff=deepcopy(r),deepcopy(c),deepcopy(adoption),deepcopy(fixture)
  if name=='old-record-change':cc[0]['setup_and_action']+=' changed'
  elif name=='wrong-new-source':cc[52]['evidence'][0]['block']='SV-B061'
  elif name=='remove-Arrangement-baseline':cc[55]['setup_and_action']=cc[55]['setup_and_action'].replace('genuinely playing nonempty Arrangement clips','unspecified source')
  elif name=='actual-oracle':cc[-1]['expected']='invented result'
  elif name=='false-external-closure':aa[9]['disposition']='bounded-local-source-context'
  elif name=='duplicate-group-probe':cc[-1]['id']='SV-U-GROUP-SLOT'
  elif name=='clipboard-failed-baseline':cc[52]['setup_and_action']=cc[52]['setup_and_action'].replace('genuinely successful scene Copy/Paste baseline','merely present control')
  try:check(rr,cc,aa,ff)
  except AssertionError:rejected+=1
  else:raise AssertionError('accepted mutation '+name)
 assert rejected==7
 links=0
 def anchor(x):return re.sub(r'[^\w\- ]','',x.strip().lower()).replace(' ','-')
 for f in [ROOT/'wiki/specs/session-view-workflows.md',ROOT/'wiki/research/session-view-workflows.md',P/'README-r3.md']:
  for dest in re.findall(r'\]\(([^)]+)\)',f.read_text()):
   if re.match(r'^[A-Za-z]+:',dest):continue
   path,_,frag=dest.partition('#');target=(f.parent/path).resolve() if path else f
   assert target.is_file() or target==P/'manifest-author-r3.json' and not target.exists(),(f,dest)
   if frag and target.suffix=='.md':assert frag in {anchor(x.lstrip('#')) for x in target.read_text().splitlines() if x.startswith('#')},(f,dest)
   links+=1
 for name in before:
  f=P/name
  if name in prior or name in ['spec-before-r3.md','research-before-r3.md']:continue
  if f.suffix=='.json':load(f)
  o=subprocess.run(['git','diff','--no-index','--check','/dev/null',str(f)],capture_output=True,text=True)
  assert o.returncode in (0,1) and not o.stdout and not o.stderr,(name,o.stdout,o.stderr)
 seal=P/'manifest-author-r3.json'
 if seal.exists():
  manifest=load(seal);assert set(before)==set(manifest['files'])|{seal.name}
  for name,row in manifest['files'].items():pin(P/name,row)
 assert tree()==before and ebefore=={r['path']:dg(ROOT/r['path']) for r in inputs}
 print(json.dumps(dict(status='pass',sealed=seal.exists(),requirements=30,cases=57,old_requirement_records_verbatim=29,old_case_records_verbatim=40,new_requirements=1,new_cases=17,case_source_contexts_D12=43,case_U_probes=14,documentary_named_control=38,documentary_comparator_null=19,all_actual_null_U_unexecuted=True,source_blocks=77,old_files=33,input_pins=57,browser_exact_IDs=30,links=links,mutations=rejected,adoption_local_groups=13,U_only_groups=2,external_pending_groups=2,historical_hash_occurrences=33,historical_consumer_files=27,historical_replay=False,packet_inputs_unchanged=True,writes=False,runtime=False,complete_topics=0),indent=2))
if __name__=='__main__':main()
