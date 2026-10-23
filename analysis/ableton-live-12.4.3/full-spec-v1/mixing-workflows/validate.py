"""Read-only retained-source and author integrity; no product operation."""
from pathlib import Path
import hashlib,json,runpy,re,subprocess,sys
P=Path(__file__).resolve().parent
ROOT=P.parents[3]
R=P.parent/'routing-monitoring'
load=lambda p:json.loads(p.read_text())
sha=lambda b:hashlib.sha256(b).hexdigest()
before={str(f.relative_to(P)):sha(f.read_bytes()) for f in P.rglob('*') if f.is_file()}
for pin in load(P/'input-owner-pins.json'):
 raw=(ROOT/pin['path']).read_bytes();assert len(raw)==pin['bytes'] and sha(raw)==pin['sha256'],pin['path']
for name,pin in load(R/'manifest-author-r1.json')['files'].items():
 raw=(R/name).read_bytes();assert len(raw)==pin['bytes'] and sha(raw)==pin['sha256'],name
parser=runpy.run_path(str(R/'capture.py'))['Extract']('mixing');parser.feed((R/'manual-12-mixing-2026-10-19.html').read_text())
for i,b in enumerate(parser.rows,1):b['locator']=f'mixing:B{i:03d}'
assert parser.rows==load(P/'source-blocks.json') and len(parser.rows)==94
bs,req,cases=runpy.run_path(str(P/'author.py'))['build']()
assert bs==load(P/'source-blocks.json') and req==load(P/'requirements.json') and cases==load(P/'cases.json')
assert len(req)==len({r['id'] for r in req})==23 and len(cases)==len({c['id'] for c in cases})==33
assert len([r for r in req if r['provenance']=='D12'])==18
index={r['id']:r for r in req};blocks={b['locator']:b for b in bs}
for r in req:
 assert r['target_applicability']=='U'
 for e in r['evidence']:assert e['anchor']==blocks[e['block']]['anchor'] and e['html_line']==blocks[e['block']]['html_line']
for c in cases:
 assert c['requirements'][0] in index and c['expected'] is None and c['comparison'] is None and c['target_grade']=='U' and c['executed'] is False
 assert c['preconditions']==['owned-context','positive-guard'] and len(c['setup_and_action'])>100
 if c['kind'] in {'signal','transform','unresolved'} or c['id'] in {'MXW-003','MXW-007'}:assert c['documentary_expected'] is None and c['documentary_comparator'] is None
assert {c['requirements'][0] for c in cases}==set(index)
links=0
for snap,canonical in [('spec-r1.md','wiki/specs/mixing-workflows.md'),('research-r1.md','wiki/research/mixing-workflows.md')]:
 assert (P/snap).read_bytes()==(ROOT/canonical).read_bytes()
 for target in re.findall(r'\]\(([^)]+)\)',(P/snap).read_text()):
  if '://' in target:continue
  target=target.split('#')[0]
  if not target:continue
  assert ((ROOT/canonical).parent/target).resolve().exists(),target
  links+=1
sys.path.insert(0,str(ROOT/'tools'));import spec_browser
assert {r['id'] for r in spec_browser.spec_rows(ROOT/'wiki/specs/mixing-workflows.md',(P/'spec-r1.md').read_text())}==set(index)
for f in P.iterdir():
 if f.suffix in {'.md','.json','.py','.txt'}:
  if f.suffix=='.json':load(f)
  r=subprocess.run(['git','diff','--no-index','--check','/dev/null',str(f)],capture_output=True);assert not r.stdout and not r.stderr,f
if (P/'manifest-author-r1.json').exists():
 for name,pin in load(P/'manifest-author-r1.json')['files'].items():
  raw=(P/name).read_bytes();assert len(raw)==pin['bytes'] and sha(raw)==pin['sha256'],name
assert before=={str(f.relative_to(P)):sha(f.read_bytes()) for f in P.rglob('*') if f.is_file()}
print(json.dumps(dict(status='pass',source_blocks=94,requirements=23,cases=33,visible_documentary_roles=13,null_documentary_oracles=20,all_target_null_U_unexecuted=True,browser_ids=23,local_links=links,writes=False,scope='author integrity only; independent semantic review pending'),indent=2))
