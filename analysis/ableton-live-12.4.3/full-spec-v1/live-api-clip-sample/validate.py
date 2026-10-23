"""Read-only sealed source/citation/member/case reconciliation; no API execution.
Prints only; never rewrites manifest, snapshot, validation or freeze files.
"""
from pathlib import Path
from hashlib import sha256
from collections import Counter
import json,re,runpy,subprocess,sys
P=Path(__file__).resolve().parent
ROOT=P.parents[3]
INV=P.parent/'max-api'

def load(p):return json.loads(p.read_text())
def sha(p):return sha256(p.read_bytes()).hexdigest()
def check_pin(p,v):
 assert p.is_file() and p.stat().st_size==v['bytes'] and sha(p)==v['sha256'],str(p)

def check():
 before={str(p.relative_to(P)):sha(p) for p in P.rglob('*') if p.is_file()}
 assert not any('__pycache__' in s for s in before),'Run with python3 -B'
 external=load(P/'external-pins.json')
 assert len({r['path'] for r in external})==len(external)
 for pin in external:check_pin(ROOT/pin['path'],pin)
 # Inventory R1 remains exact; all53 source bytes pinned without claiming semantic read of all53.
 inv=load(INV/'manifest-inventory-r1.json')
 sources=load(INV/'all-sources-r1.json')
 assert len(sources)==53 and len({s['id'] for s in sources})==53
 for s in sources:
  assert inv['files'][s['file']]==dict(bytes=s['bytes'],sha256=s['sha256'])
  check_pin(INV/s['file'],s)
 extract=runpy.run_path(str(INV/'derive_inventory.py'))['extract']
 inventoryblocks=load(INV/'reference-blocks.json')
 selected=load(P/'sources.json');blocks=load(P/'source-blocks.json')
 assert len(selected)==5 and sum(map(len,blocks.values()))==379
 for source in selected:
  assert source in sources
  assert extract((INV/source['file']).read_text())==blocks[source['id']]==inventoryblocks[source['id']]
 assert 'Ableton Live version 12.4.5' in ' '.join(b['text'] for b in inventoryblocks['C74-LOM-INDEX'])
 # Reproduce derived author data/prose without invoking guarded author --write.
 author=runpy.run_path(str(P/'author.py'))
 expected=author['build']()
 for name,v in expected.items():assert load(P/(name.replace('_','-')+'.json'))==v,name
 spec,research=author['pages'](expected)
 specpath=ROOT/'wiki/specs/live-api-clip-sample.md';researchpath=ROOT/'wiki/research/live-api-clip-sample.md'
 assert specpath.read_text()==spec==(P/'spec-r1.md').read_text()
 assert researchpath.read_text()==research==(P/'research-r1.md').read_text()
 profiles=expected['profiles'];members=expected['members'];reqs=expected['requirements'];cases=expected['cases']
 assert len(profiles)==5 and [len(x['declared_members']) for x in profiles]==[77,6,28,19,1]
 original=[m for m in load(INV/'lom-members.json') if m['reference_entry'] in {p['id'] for p in profiles}]
 assert {m['id'] for m in members}=={m['id'] for m in original} and len(members)==131
 assert Counter(m['category'] for m in members)=={'children':2,'properties':84,'functions':45}
 assert all(p['target_applicability']=='U' and not p['complete'] and p['specification']=='partial-documentary-only' for p in profiles)
 rids={r['id'] for r in reqs};cids={c['id'] for c in cases}
 assert len(rids)==len(reqs)==143 and len(cids)==len(cases)==163
 assert Counter(r['provenance'] for r in reqs)=={'D-current-public':131,'U':12}
 assert Counter(c['provenance'] for c in cases)=={'D-current-public':131,'U':32}
 assert set.union(*(set(p['declared_members']) for p in profiles))=={m['id'] for m in members}
 for m in members:
  assert len(m['requirements'])==len(m['cases'])==1 and not m['complete'] and m['target_unresolved']
  r=next(r for r in reqs if r['id']==m['requirements'][0]);c=next(c for c in cases if c['id']==m['cases'][0])
  assert r['direct_member']==m['id'] and c['direct_members']==[m['id']] and c['requirements']==[r['id']]
  assert r['documented_access']==m['documented_access'] and r['documented_type']==m['documented_type']
  assert c['source_claim']==r['contract'] and c['evidence']==r['evidence']
  source=next(s for s in selected if s['id']==m['source_id'])
  for e,b in zip(r['evidence'],m['source_body']):
   assert e['block']==b['block'] and e['html_line']==b['html_line'] and e['html_column']==b['html_column']
   assert e['source_sha256']==source['sha256'] and e['url']==m['url']
   assert b in blocks[e['source']]
  for owner in m['existing_behavior_owners']:assert (ROOT/owner).is_file()
 assert set.union(*(set(c['requirements']) for c in cases))==rids
 for c in cases:
  assert c['setup_and_action'] and c['fixture']=='fixtures.json#LCS-OWNED'
  assert {'admitted-api-object','member-context','paired-positive-baseline','active-path-if-audible'}<=set(c['preconditions'])
  assert all(c[k] is None for k in ['expected','comparison','documentary_expected','documentary_comparator'])
  assert c['target_grade']=='U' and c['executed'] is False
  if c['provenance']=='U':assert c['source_claim'] is None and not c['evidence']
 for r in reqs:
  assert r['target_applicability']=='U'
  assert bool(r['evidence'])==(r['provenance']=='D-current-public')
 # Actual existing spec browser parser, imported without build/output.
 sys.path.insert(0,str(ROOT/'tools'))
 from spec_browser import spec_rows,frontmatter
 browsed=spec_rows(specpath,spec)
 assert len(browsed)==143 and {r['id'] for r in browsed}==rids
 for text in [spec,research]:
  meta=frontmatter(text)
  assert {'id','type','status','updated','access'}<=set(meta) and meta['access']=='analysis'
 links=0
 for canonical in [specpath,researchpath]:
  for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)',canonical.read_text()):
   if re.match(r'https?://',target):continue
   name,_,fragment=target.partition('#');dest=canonical.parent/name
   assert dest.is_file(),target
   links+=1
 releasepayloads=0
 for pin in external:
  if pin['path'].startswith('handoff/') and pin['path'].endswith('/manifest.json'):
   manifestpath=ROOT/pin['path']
   for item in load(manifestpath)['files']:
    check_pin(manifestpath.parent/item['path'],item);releasepayloads+=1
 manifest=load(P/'manifest-author-r1.json')
 assert manifest['counts']==expected['counts'] and manifest['status']=='partial-author-freeze-awaiting-independent-semantic-review'
 assert set(manifest['files'])|{'manifest-author-r1.json'}<=set(before)
 assert set(before)<=set(manifest['files'])|{'manifest-author-r1.json','validation-author-r1.json','freeze-author-r1.json'}
 for name,pin in manifest['files'].items():check_pin(P/name,pin)
 for snap in manifest['canonical_snapshots']:
  check_pin(ROOT/snap['canonical'],snap);check_pin(P/snap['snapshot'],snap)
 if (P/'freeze-author-r1.json').exists():
  freeze=load(P/'freeze-author-r1.json')
  for name,pin in freeze['files'].items():check_pin(P/name,pin)
 whitespace=0
 for path in [specpath,researchpath]+[p for p in P.iterdir() if p.suffix in {'.py','.json','.md','.txt'}]:
  result=subprocess.run(['git','diff','--no-index','--check','/dev/null',str(path)],capture_output=True)
  assert result.returncode in (0,1) and not result.stdout and not result.stderr,str(path)
  whitespace+=1
 assert before=={str(p.relative_to(P)):sha(p) for p in P.rglob('*') if p.is_file()},'Validator mutated files'
 return dict(status='pass',scope='Source/member/requirement/case/browser/null/pin/snapshot/link integrity only; semantic review pending',source_inventory_raw_hashes=53,selected_profiles=5,selected_source_blocks=379,direct_members=131,mapped_to_partial_roles=131,target_unresolved_members=131,inherited_members_flattened=0,complete_profiles=0,requirements=143,cases=163,exact_browser_ID_set=143,external_pins=len(external),immutable_release_payloads=releasepayloads,all_documentary_target_oracles_null=True,all_target_U_unexecuted=True,canonical_snapshots=2,payloads=len(manifest['files']),local_links=links,untracked_whitespace_files=whitespace,writes=False,original_Max_API_patch_JS_example_hardware_candidate_execution=False)

if __name__=='__main__':
 assert not sys.argv[1:],'Read-only validator accepts no mutation flags'
 print(json.dumps(check(),indent=2))
