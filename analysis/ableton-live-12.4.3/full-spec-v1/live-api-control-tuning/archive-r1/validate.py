"""Read-only integrity checks, never API/runtime or behavioral verification."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys
P=Path(__file__).resolve().parent
ROOT=P.parents[3]
M=P.parent/'max-api'
load=lambda n:json.loads((P/n).read_text())
sha=lambda b:hashlib.sha256(b).hexdigest()
for row in load('inventory-pins.json')+load('owner-pins.json'):
 raw=(ROOT/row['path']).read_bytes()
 assert len(raw)==row['bytes'] and sha(raw)==row['sha256'],row['path']
for name,info in json.loads((M/'manifest-inventory-r1.json').read_text())['files'].items():
 raw=(M/name).read_bytes()
 assert len(raw)==info['bytes'] and sha(raw)==info['sha256'],name
allblocks=json.loads((M/'reference-blocks.json').read_text())
blocks=load('source-blocks.json')
assert len(blocks)==6 and all(v==allblocks[k] for k,v in blocks.items())
original_sources=json.loads((M/'all-sources-r1.json').read_text())
assert load('sources.json')==[s for s in original_sources if s['id'] in blocks]
req=load('requirements.json');cases=load('cases.json');ledger=load('member-ledger.json')
index={r['id']:r for r in req}
assert len(index)==len(req)==33 and len({c['id'] for c in cases})==len(cases)==41
members=[m for m in json.loads((M/'lom-members.json').read_text()) if m['source_id'] in blocks]
assert len(members)==len(ledger)==28
assert {m['id'] for m in members}=={l['member'] for l in ledger}
for m in members:
 l=next(l for l in ledger if l['member']==m['id'])
 r=index[l['requirements'][0]]
 assert r['member']==m['id'] and r['declaration']==m['heading'] and r['source_url']==m['url']
 rows=blocks[m['source_id']];start=next(i for i,b in enumerate(rows) if b['block']==m['block'])
 end=next((i for i in range(start+1,len(rows)) if rows[i]['tag'] in ['h2','h3']),len(rows))
 assert r['source_blocks']==[b['block'] for b in rows[start:end]]
 assert not l['semantic_complete'] and l['target_applicability']=='U'
 assert l['cases']==[c['id'] for c in cases if c['requirements']==l['requirements']]
assert len([r for r in req if r['provenance']=='D-current-public'])==29
assert all(r['target_applicability']=='U' for r in req)
for c in cases:
 assert len(c['requirements'])==1 and c['requirements'][0] in index
 assert all(c[k] is None for k in ['documentary_expected','documentary_comparator','expected','comparison'])
 assert c['target_grade']=='U' and not c['executed']
 assert len(c['setup_and_action'])>100 and c['preconditions']==['owned-context','positive-guard']
 r=index[c['requirements'][0]]
 assert c['source_claim']==(r['contract'] if r['provenance']=='D-current-public' else None)
assert {c['requirements'][0] for c in cases}==set(index)
links=0
for snapshot,canonical in [('spec-r1.md','wiki/specs/live-api-control-tuning.md'),('research-r1.md','wiki/research/live-api-control-tuning.md')]:
 text=(P/snapshot).read_text();assert text==(ROOT/canonical).read_text()
 for target in re.findall(r'\]\(([^)]+)\)',text):
  if '://' in target:continue
  target=target.split('#')[0]
  if not target:continue
  assert ((ROOT/canonical).parent/target).resolve().exists(),target
  links+=1
sys.path.insert(0,str(ROOT/'tools'))
import spec_browser
assert {r['id'] for r in spec_browser.spec_rows(ROOT/'wiki/specs/live-api-control-tuning.md',(P/'spec-r1.md').read_text())}==set(index)
for path in P.iterdir():
 if path.suffix not in {'.json','.py','.md','.txt'}:continue
 if path.suffix=='.json':json.loads(path.read_text())
 result=subprocess.run(['git','diff','--no-index','--check','/dev/null',str(path)],capture_output=True)
 assert not result.stdout and not result.stderr,(path,result.stdout,result.stderr)
if (P/'manifest-author-r1.json').exists():
 for name,info in load('manifest-author-r1.json')['files'].items():
  raw=(P/name).read_bytes();assert len(raw)==info['bytes'] and sha(raw)==info['sha256'],name
print(json.dumps(dict(status='pass',references=6,source_blocks=sum(map(len,blocks.values())),direct_members=28,partial_member_mappings=28,semantic_complete_members=0,requirements=33,cases=41,browser_ids=33,local_links=links,all_actual_oracles_null=True,scope='author integrity only; independent semantic review required'),indent=2))
