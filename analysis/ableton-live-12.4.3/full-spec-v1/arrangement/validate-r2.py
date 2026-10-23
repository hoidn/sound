"""Read-only current Arrangement R2 check. Never replays survey/old consumers.
Only retained JSON/Markdown/HTML and own pure parser/browser definitions execute.
No report writes, original code, native analysis or application operations.
"""
from pathlib import Path
from hashlib import sha256
from copy import deepcopy
from collections import Counter
import ast,json,re,runpy,subprocess,sys
P=Path(__file__).resolve().parent;ROOT=P.parents[3];A=P.parent/'arrangement-source-audit'
assert sys.dont_write_bytecode and sys.argv[1:] in (['--check'],['--preflight'])
pre=sys.argv[1:]==['--preflight'];M=P/'manifest-author-r2.json'
assert pre != M.exists(),'Use --check after seal, --preflight before seal only'
load=lambda p:json.loads(p.read_text())
def info(p):
 raw=p.read_bytes();return dict(bytes=len(raw),sha256=sha256(raw).hexdigest())
def pin(p,r):assert info(p)=={k:r[k] for k in ['bytes','sha256']},p
def ptr(v,p):
 for k in p.split('/')[1:]:v=v[int(k)] if isinstance(v,list) else v[k.replace('~1','/').replace('~0','~')]
 return v
def files():return {str(q.relative_to(P)):info(q) for q in P.rglob('*') if q.is_file()}
before=files();early_canon={str(q):info(q) for q in [ROOT/'wiki/specs/arrangement-editing.md',ROOT/'wiki/research/arrangement-editing.md']};consumer_watch={r['consumer']:info(ROOT/r['consumer']) for r in load(P/'canonical-consumers-r2.json')['hash_occurrences']};inputs=load(P/'inputs-r2.json');assert len(inputs)==108 and len({r['path'] for r in inputs})==108
assert not any(r['path'].startswith('wiki/') for r in inputs)
external={r['path']:info(ROOT/r['path']) for r in inputs}
for r in inputs:pin(ROOT/r['path'],r)
old=load(P/'preservation-r1.json');assert len(old['files'])==12
for n,r in old['files'].items():pin(P/n,r)
assert info(P/'manifest.json')['sha256']=='6fe44f181360d1b2c186b394e671c673b3830bbb226fef208c4292ff655cb10f'
assert set(old['files'])==set(load(P/'manifest.json')['payloads'])|{'manifest.json'}
for n,r in load(P/'manifest.json')['payloads'].items():assert old['files'][n]==r
assert info(A/'manifest-author-r2.json')['sha256']=='24ab3e93c3fafe6debf3d4252934fae1375b4aba48a2f903a4e458c08c7217a5'
for n,r in load(A/'manifest-author-r2.json')['files'].items():pin(A/n,r)
for n,expected in [('spec-r1.md','2ae6253a56b5e605acac83f7eb66e3f2b526404773ae2226eee0ca97b2c79d18'),('research-r1.md','0035104ea8092f50bf175b05aeaf4c0ede1dacbe19d4e823006257e776a6eb83')]:assert info(P/n)['sha256']==expected
assert info(ROOT/'analysis/ableton-live-12.4.3/full-spec-v1/reviews/arrangement-source-audit-review-final.json')['sha256']=='d0c444776fc1e56e85f405a7ec7d29a80540d5891ef0f1ee95bcab39aaa3989f'
# Only the audit's pinned pure HTMLParser executes; raw source content stays data.
parser=runpy.run_path(str(A/'source_parser.py'))['extract']
ab,ar=parser((P/'manual-arrangement.html').read_text(),'ARR');cb,cr=parser((P/'manual-concepts.html').read_text(),'CON')
blocks=ab+cb[29:51];source=load(A/'source-blocks.json');assert len(ab)==164 and len(blocks)==186 and len(source)==186
for a,b in zip(blocks,source):
 for k,v in a.items():assert b[k]==v,(a['id'],k)
assert sum(len(r['text']) for r in blocks)==33957
oldcat=load(A/'owner-catalog-asof.json');oldreq=load(P/'requirements-r1-asof.json');oldcases=load(P/'cases-r1-asof.json')
assert oldreq==oldcat['requirements'] and oldcases==oldcat['cases']
reqs=load(P/'requirements-r2.json');cases=load(P/'cases-r2.json');fixture=load(P/'fixtures-r2.json')
assert len(reqs)==42 and len(cases)==84
assert [r['id'] for r in reqs]==[f'REQ-ARRANGEMENT-{i:03}' for i in range(1,43)]
assert [c['id'] for c in cases]==[f'AR-{i:03}' for i in range(1,85)]
assert [r['id'] for r in reqs[:35]]==[r['id'] for r in oldreq] and [c['id'] for c in cases[:65]]==[c['id'] for c in oldcases]
for a,b in zip(oldreq,reqs):
 for k,v in a.items():
  if k!='contract':assert b[k]==v,(b['id'],k)
 assert b['contract'].startswith(a['contract'].rstrip())
for a,b in zip(oldcases,cases):
 for k,v in a.items():
  if k!='setup_and_action':assert b[k]==v,(b['id'],k)
 assert b['setup_and_action'].startswith(a['setup_and_action'])
assert fixture['historical_fixture']==oldcat['fixture']
rm={r['id']:r for r in reqs};bm={b['id']:b for b in blocks}
assert Counter(r['provenance'] for r in reqs)=={'D12':38,'D-package':1,'U':3}
for r in reqs:
 assert r['target']=='U' and r['complete'] is False
 for e in r['source_context']:assert ptr(source,e['json_pointer'])['id']==e['block']
def check_oracles(rows):
 assert len(rows)==len({r['id'] for r in rows})==84
 for c in rows:
  assert set(c['requirements'])<=set(rm) and c['requirements']
  assert c['expected'] is c['comparison'] is c['actual_expected'] is c['actual_comparison'] is None
  assert c['target']=='U' and c['executed'] is False and c['complete'] is False
  assert (c['documentary_expected'] is None)==(c['documentary_comparator'] is None)
  if c['documentary_expected'] is not None:assert c['documentary_comparator'].startswith('Only')
 for i in [9,15,18,21,22,23,30,31,33,36,39,41,43,44,45,46,52,56,58,60,61,62,63,64,65]:assert rows[i-1]['documentary_expected'] is None
 for i in [2,4,5,6,7,14,17]:assert rows[64+i]['documentary_expected'] is None
 assert {x for c in rows for x in c['requirements']}==set(rm)
check_oracles(cases)
# Recursive finite delta exactly reconstructs current catalogs; no metadata-only closure.
def apply(original,deltas):
 obj=deepcopy(original)
 for d in deltas:
  ks=d['pointer'].split('/')[1:];parent=obj
  for k in ks[:-1]:parent=parent[int(k)] if isinstance(parent,list) else parent[k.replace('~1','/').replace('~0','~')]
  k=int(ks[-1]) if isinstance(parent,list) else ks[-1].replace('~1','/').replace('~0','~')
  if d['operation']=='add':
   assert d['old'] is None
   if isinstance(parent,list):assert k==len(parent);parent.append(deepcopy(d['new']))
   else:assert k not in parent;parent[k]=deepcopy(d['new'])
  elif d['operation']=='replace':assert parent[k]==d['old'];parent[k]=deepcopy(d['new'])
  else:raise AssertionError('Unexpected removal')
 return obj
delta=load(P/'delta-r2.json');assert apply(oldreq,delta['requirements'])==reqs and apply(oldcases,delta['cases'])==cases
assert delta['new_requirement_IDs']==[r['id'] for r in reqs[35:]] and delta['new_case_IDs']==[c['id'] for c in cases[65:]]
# Exact deterministic data/Markdown reproduction is read-only and runs only our new analyst author.
r=subprocess.run([sys.executable,'-B',str(P/'author-r2.py'),'--check'],capture_output=True,text=True);assert r.returncode==0,(r.stdout,r.stderr)
adopt=load(P/'audit-adoption-r2.json');proposals=load(A/'proposed-deltas-derived.json');claims=load(A/'claims-r2.json');cm={c['id']:c for c in claims}
assert len(adopt)==19 and [g['audit_group'] for g in adopt]==[g['id'] for g in proposals]
for i,(g,proposal) in enumerate(zip(adopt,proposals)):
 assert g['title']==proposal['title'] and g['source_facets']==proposal['source_facets'] and g['retained_unknowns']==proposal['retained_unknowns']
 assert g['source_blocks']==sorted({cm[f]['source_block'] for f in g['source_facets']})
 c=cases[65+i];assert c['audit_group']==g['audit_group'] and c['setup_and_action'].startswith(proposal['proposed_finite_action'])
 assert g['case_ids']==[c['id']] and g['case_pointers']==[f'/{65+i}'] and g['requirements']==c['requirements']
 assert c['source_claim']==' '.join(rm[n]['contract'].strip() for n in c['requirements'])
recon=load(P/'source-reconciliation-r2.json');assert len(recon)==len(claims)==314
for z,c in zip(recon,claims):
 assert z['facet']==c['id'] and z['source_excerpt']==c['source_excerpt'] and z['historical_audit_disposition']==c['disposition'] and z['historical_assessment']==c['assessment']
 b=ptr(source,z['source_pointer']);assert b['id']==z['source_block']==c['source_block'] and b['text'][slice(*c['text_span'])]==c['source_excerpt']
 assert z['expected'] is z['comparison'] is None and z['target']=='U' and z['executed'] is z['complete'] is False
 assert z['successor_groups']==[g['audit_group'] for g in adopt if c['id'] in g['source_facets']]
for r in load(P/'owner-contexts-r2.json'):assert ptr(load(ROOT/r['catalog']),r['json_pointer'])==r['record'] and r['record']['id']==r['id']
contexts=load(P/'owner-contexts-r2.json');assert len(contexts)==16
assert any(r['id']=='SV-041' and 'C then A then E' in r['record']['setup_and_action'] for r in contexts)
assert any(r['id']=='CV-063' for r in contexts)
consumers=load(P/'canonical-consumers-r2.json');assert len(consumers['records'])==10 and consumers['direct_pins']==8
for r in consumers['records']:
 pin(ROOT/r['consumer'],r['consumer_identity_asof']);assert ptr(load(ROOT/r['consumer']),r['pointer'])==r['record'];pin(P/r['historical_provider'],r['record'])
for r in consumers['hash_occurrences']:
 pin(ROOT/r['consumer'],r['consumer_identity_asof']);assert ptr(load(ROOT/r['consumer']),r['pointer'])==r['sha256'];assert info(P/r['historical_provider'])['sha256']==r['sha256']
# Productive baselines and exact platform-context guards, not source proof or actual fixture success.
def guards(rows):
 assert all(x in rows[22]['setup_and_action'] for x in ['actually playing nonzero','active nonzero track effect','nonmuted wet/return/output','enabled flag or zero'])
 assert all(x in rows[54]['setup_and_action'] for x in ['successful simultaneous','same-start','differing actual start'])
 assert all(x in rows[55]['setup_and_action'] for x in ['genuine automatic Arrangement scrolling','actual paused Follow','stopped'])
 assert all(x in rows[68]['setup_and_action'] for x in ['actual Arrangement scrolling','edit/horizontal-scroll/beat-time-ruler-click','stop-alone/restart'])
 assert 'CtrlAltShift (Win)/CmdOptionShift (Mac)' in rows[83]['setup_and_action']
 assert all(x in rows[71]['setup_and_action'] for x in ['historical SV001 is only A-name/Enter','Current SessionR3 SV041'])
 assert 'active transport and nonmuted audible output before OFF' in rows[81]['setup_and_action']
guards(cases)
rejected=0
for kind in ['actual-oracle','signal-documentary','wrong-requirement','no-productive-effect','no-same-start','no-follow-scroll','historical-session-overclaim']:
 rows=deepcopy(cases)
 if kind=='actual-oracle':rows[0]['expected']='invented runtime result'
 elif kind=='signal-documentary':rows[22]['documentary_expected']='invented waveform equality';rows[22]['documentary_comparator']='Only invented tolerance'
 elif kind=='wrong-requirement':rows[0]['requirements']=['REQ-UNRELATED']
 elif kind=='no-productive-effect':rows[22]['setup_and_action']='enabled flags only'
 elif kind=='no-same-start':rows[54]['setup_and_action']='different starts only'
 elif kind=='no-follow-scroll':rows[68]['setup_and_action']='Follow visible only'
 else:rows[71]['setup_and_action']='Old SV001 proves arbitrary nonsequential launches'
 try:check_oracles(rows);guards(rows)
 except (AssertionError,KeyError):rejected+=1
 else:raise AssertionError(kind)
assert rejected==7
# Browser exact public pure functions only: no broader renderer/native-helper imports.
browser=ROOT/'tools/spec_browser.py';tree=ast.parse(browser.read_text());names={'anchor','frontmatter','cells','spec_rows'}
defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names];assert {n.name for n in defs}==names
ns={'re':re};exec(compile(ast.Module(body=defs,type_ignores=[]),str(browser),'exec'),ns)
sp=ROOT/'wiki/specs/arrangement-editing.md';rp=ROOT/'wiki/research/arrangement-editing.md';canon={str(p):info(p) for p in [sp,rp]}
assert sp.read_bytes()==(P/'spec-r2.md').read_bytes() and rp.read_bytes()==(P/'research-r2.md').read_bytes()
for p in [sp,rp]:assert 'revision: 2\n' in p.read_text()
spec=sp.read_text();rows=ns['spec_rows'](sp,spec);assert len(rows)==42 and {r['id'] for r in rows}==set(rm)
assert {x for x in re.findall(r'^\| (AR-\d+) \|',spec,re.M)}=={c['id'] for c in cases}
links=0
for p in [sp,rp,P/'README-r2.md']:
 for dest in re.findall(r'\[[^\]]*\]\(([^)\s]+)\)',p.read_text()):
  if re.match('[A-Za-z]+:',dest):continue
  name,_,fragment=dest.partition('#');q=(p.parent/name).resolve() if name else p
  if pre and q==M:continue
  assert q.is_file(),(p,dest)
  if fragment and q.suffix=='.md':
   slug=lambda h:re.sub(r'[^\w\- ]','',re.sub(r'<[^>]*>|[`*]','',h).lower()).replace(' ','-')
   assert fragment in {slug(h) for h in re.findall(r'^#+\s+(.+)$',q.read_text(),re.M)},(p,dest)
  links+=1
white=0
for n in before:
 if n in old['files'] or n in ['spec-r1.md','research-r1.md']:continue
 q=P/n
 if q.suffix in ['.md','.json','.py']:
  if q.suffix=='.json':load(q)
  r=subprocess.run(['git','diff','--no-index','--check','/dev/null',str(q)],capture_output=True);assert r.returncode in (0,1) and not r.stdout and not r.stderr,(q,r.stdout,r.stderr);white+=1
if not pre:
 m=load(M);assert m['revision']==2 and set(m['files'])==set(before)-{M.name}
 for n,r in m['files'].items():pin(P/n,r)
 for r in m['canonicals']:pin(ROOT/r['path'],r);pin(P/r['snapshot'],r)
assert early_canon==canon and consumer_watch=={p:info(ROOT/p) for p in consumer_watch}
assert before==files() and external=={r['path']:info(ROOT/r['path']) for r in inputs} and canon=={str(p):info(p) for p in [sp,rp]}
print(json.dumps(dict(status='passed-read-only-preflight' if pre else 'passed-read-only-frozen',requirements=42,provenance=dict(Counter(r['provenance'] for r in reqs)),old_requirement_IDs_retained=35,cases=84,old_case_IDs_retained=65,changed_old_contracts=sum(a['contract']!=b['contract'] for a,b in zip(oldreq,reqs)),changed_old_actions=sum(a['setup_and_action']!=b['setup_and_action'] for a,b in zip(oldcases,cases)),new_requirements=7,new_compound_reset_cases=19,audit_groups=19,source_blocks=186,source_facets=314,source_reconciliation_is_not_completion=True,input_pins=108,historical_direct_pins=8,consumer_records=10,historical_hash_occurrences=len(consumers['hash_occurrences']),browser_exact_IDs=42,documentary_visible=sum(c['documentary_expected'] is not None for c in cases),documentary_null=sum(c['documentary_expected'] is None for c in cases),all_actual_null_U_unexecuted=True,old_files_preserved=12,selected_current_external_records=16,rejection_fixtures=rejected,local_links=links,whitespace_files=white,watched_unchanged=len({str((P/n).resolve()) for n in before}|{str((ROOT/n).resolve()) for n in external}|set(canon)|{str((ROOT/n).resolve()) for n in consumer_watch}),old_survey_or_historical_consumer_execution=False,original_runtime_native_hardware_network=False,writes=False,complete=0),indent=2))
