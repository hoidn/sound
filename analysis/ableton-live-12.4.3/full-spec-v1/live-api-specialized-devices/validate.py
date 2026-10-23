"""Read-only source/member/author consistency, not behavioral verification."""
from pathlib import Path
import hashlib,json,re,runpy,subprocess,sys
P=Path(__file__).resolve().parent
ROOT=P.parents[3]
M=P.parent/'max-api'
load=lambda p:json.loads(p.read_text())
sha=lambda b:hashlib.sha256(b).hexdigest()
before={str(p.relative_to(P)):sha(p.read_bytes()) for p in P.rglob('*') if p.is_file()}
for row in load(P/'input-owner-pins.json'):
 raw=(ROOT/row['path']).read_bytes();assert len(raw)==row['bytes'] and sha(raw)==row['sha256'],row['path']
for name,pin in load(M/'manifest-inventory-r1.json')['files'].items():
 raw=(M/name).read_bytes();assert len(raw)==pin['bytes'] and sha(raw)==pin['sha256'],name
extract=runpy.run_path(str(M/'derive_inventory.py'))['extract']
blocks=load(P/'source-blocks.json')
for source in load(P/'sources.json'):assert extract((M/source['file']).read_text())==blocks[source['id']]
profiles,bs,members,req,cases=runpy.run_path(str(P/'author.py'))['build']()
for name,x in [('profiles.json',profiles),('source-blocks.json',bs),('member-ledger.json',members),('requirements.json',req),('cases.json',cases)]:assert load(P/name)==x
assert len(profiles)==14 and len(members)==108 and len(req)==113 and len(cases)==123
assert len({m['id'] for m in members})==108
original=[m for m in load(M/'lom-members.json') if m['source_id'] in blocks]
assert {m['id'] for m in original}=={m['id'] for m in members}
assert all(not m['complete'] and m['target_unresolved'] for m in members)
assert len([r for r in req if r['provenance']=='D-current-public'])==108
assert all(r['target_applicability']=='U' for r in req)
for m in members:
 r=next(r for r in req if r['direct_member']==m['id'])
 c=next(c for c in cases if c['requirements']==[r['id']])
 assert m['requirements']==[r['id']] and m['cases']==[c['id']]
 assert r['documented_access']==m['documented_access'] and r['documented_type']==m['documented_type']
 assert c['source_claim']==r['contract'] and r['source_blocks']==[b['block'] for b in m['source_body']]
for c in cases:
 assert all(c[k] is None for k in ['expected','comparison','documentary_expected','documentary_comparator'])
 assert c['target_grade']=='U' and not c['executed'] and len(c['setup_and_action'])>100
 assert c['preconditions']==['admitted-context','positive-baseline']
assert {c['requirements'][0] for c in cases}=={r['id'] for r in req}
links=0
for snap,canonical in [('spec-r1.md','wiki/specs/live-api-specialized-devices.md'),('research-r1.md','wiki/research/live-api-specialized-devices.md')]:
 assert (P/snap).read_bytes()==(ROOT/canonical).read_bytes()
 for target in re.findall(r'\]\(([^)]+)\)',(P/snap).read_text()):
  if '://' in target:continue
  target=target.split('#')[0]
  if not target:continue
  assert ((ROOT/canonical).parent/target).resolve().exists(),target
  links+=1
sys.path.insert(0,str(ROOT/'tools'))
import spec_browser
assert {r['id'] for r in spec_browser.spec_rows(ROOT/'wiki/specs/live-api-specialized-devices.md',(P/'spec-r1.md').read_text())}=={r['id'] for r in req}
for path in P.iterdir():
 if path.suffix in {'.md','.py','.json','.txt'}:
  if path.suffix=='.json':load(path)
  result=subprocess.run(['git','diff','--no-index','--check','/dev/null',str(path)],capture_output=True);assert not result.stdout and not result.stderr,path
if (P/'manifest-author-r1.json').exists():
 for name,pin in load(P/'manifest-author-r1.json')['files'].items():
  raw=(P/name).read_bytes();assert len(raw)==pin['bytes'] and sha(raw)==pin['sha256'],name
assert before=={str(p.relative_to(P)):sha(p.read_bytes()) for p in P.rglob('*') if p.is_file()}
print(json.dumps(dict(status='pass',scope='author integrity only; independent semantic review pending',references=14,source_blocks=sum(map(len,blocks.values())),direct_members=108,partial_member_mappings=108,semantic_complete_members=0,requirements=113,cases=123,browser_ids=113,local_links=links,all_actual_oracles_null=True,writes=False),indent=2))
