"""Read-only Stem R2 source/context/identity checks. No runtime/capture/author execution."""
from pathlib import Path
from collections import Counter
from copy import deepcopy
from hashlib import sha256
from itertools import combinations
import json
import re
import runpy
import subprocess
import sys

P=Path(__file__).resolve().parent;ROOT=P.parents[3];B=P.parent
assert sys.dont_write_bytecode,'Use -B'
assert sys.argv[1:] in (['--check'],['--preflight'])
preflight=sys.argv[1:]==['--preflight']
assert not preflight or not (P/'manifest-author-r2.json').exists(),'Preflight only before seal'
def load(p):return json.loads(p.read_text())
def digest(p):
 d=p.read_bytes();return dict(bytes=len(d),sha256=sha256(d).hexdigest())
def pin(p,r):assert digest(p)=={k:r[k] for k in ('bytes','sha256')},p

def pointer(value,ptr):
 for k in ptr.lstrip('/').split('/') if ptr else []:
  k=k.replace('~1','/').replace('~0','~');value=value[int(k)] if isinstance(value,list) else value[k]
 return value

before={str(p.relative_to(P)):digest(p) for p in P.rglob('*') if p.is_file()}
assert not any('__pycache__' in name for name in before)
oldmanifest=load(P/'manifest-author-r1.json')
assert digest(P/'manifest-author-r1.json')['sha256']=='e7d75c3e9d692b3bf15187bb2284510c1c0e9b0362145cbe67bd91ec90d0d9d2'
assert len(oldmanifest['files'])==13
for name,record in oldmanifest['files'].items():
 pin(P/name,record);pin(P/'archive-r1'/name,record);assert (P/name).read_bytes()==(P/'archive-r1'/name).read_bytes()
assert (P/'manifest-author-r1.json').read_bytes()==(P/'archive-r1/manifest-author-r1.json').read_bytes()
archive=load(P/'archive-r1-pins.json');assert len(archive)==14
for r in archive:pin(ROOT/r['path'],r)
assert {str(p.relative_to(ROOT)) for p in (P/'archive-r1').iterdir()}=={r['path'] for r in archive}
inputs=load(P/'inputs-r2.json');assert len(inputs)==len({r['path'] for r in inputs})
for r in inputs:pin(ROOT/r['path'],r)
assert not any(r['path'] in ['wiki/specs/stem-separation.md','wiki/research/stem-separation.md'] for r in inputs)
source=load(P/'source.json');pin(P/source['file'],source)
dependency=load(P/'dependencies.json')[0];pin(ROOT/dependency['path'],dependency)
# This is the already inspected guarded analyst HTML parser class only.
parser=runpy.run_path(str(ROOT/dependency['path']))['Chapter']();parser.feed((P/source['file']).read_text())
for i,r in enumerate(parser.rows,1):r['id']=f'STEM-B{i:03d}'
assert parser.rows==load(P/'source-blocks.json') and len(parser.rows)==32
blockmap={b['id']:b for b in parser.rows}
oldreq,oldcases=load(P/'requirements.json'),load(P/'cases.json')
reqs,cases=load(P/'requirements-r2.json'),load(P/'cases-r2.json')
assert len(oldreq)==18 and len(oldcases)==29 and reqs[:18]==oldreq
assert len(reqs)==len({r['id'] for r in reqs})==20
assert len(cases)==len({c['id'] for c in cases})==32
assert [c['id'] for c in cases[:29]]==[c['id'] for c in oldcases]
assert {r['id'] for r in reqs[18:]}=={'REQ-STEM-SEPARATION-016','REQ-STEM-SEPARATION-017'}
reqmap={r['id']:r for r in reqs};cm={c['id']:c for c in cases}
for old,c in zip(oldcases,cases):
 for field,value in old.items():
  if field not in {'setup_and_action','fixture'}:assert c[field]==value,(old['id'],field)
for r in reqs:
 assert r['target_applicability']=='U' and r['contract']
 for e in r['evidence']:assert e['anchor']==blockmap[e['block']]['anchor'] and e['html_line']==blockmap[e['block']]['html_line']
for c in cases:
 assert set(c['requirements'])<=set(reqmap) and c['setup_and_action'] and c['fixture']=='fixtures-r2.json#STEM-OWNED'
 assert c['expected'] is c['comparison'] is None and c['target_grade']=='U' and c['executed'] is False
 assert c['evidence']==reqmap[c['requirements'][0]]['evidence']
 if c['kind'] in {'signal','file','timing'} or c['id'].startswith('STEM-U-'):assert c['documentary_expected'] is c['documentary_comparator'] is None
 if c['id'].startswith('STEM-U-'):assert c['source_claim'] is None
 else:assert c['source_claim']==reqmap[c['requirements'][0]]['contract']
assert {rid for c in cases for rid in c['requirements']}==set(reqmap)
names=['Vocals','Drums','Bass','Others']
assert cm['STEM-002']['finite_contexts']==[dict(source=v,menu=m) for v in ['Browser audio file','Session audio clip','Arrangement audio clip'] for m in ['context menu','Create menu']]
assert [x['selected_elements'] for x in cm['STEM-003']['finite_contexts']]==[list(v) for n in range(1,5) for v in combinations(names,n)]
assert Counter(len(x['selected_elements']) for x in cm['STEM-003']['finite_contexts'])=={1:4,2:6,3:4,4:1}
assert [len(x['elements']) for x in cm['STEM-007']['finite_contexts']]==[2,3,4] and all(not x['merge'] for x in cm['STEM-007']['finite_contexts'])
assert [len(x['elements']) for x in cm['STEM-008']['finite_contexts'] if x['merge']]==[2,3]
assert {x['view'] for x in cm['STEM-009']['finite_contexts']}=={'Session','Arrangement'} and len(cm['STEM-009']['finite_contexts'])==4
assert len(cm['STEM-010']['finite_contexts'])==3
assert len(cm['STEM-014']['finite_contexts'])==6
assert len(cm['STEM-016']['finite_contexts'])==4 and len(cm['STEM-017']['finite_contexts'])==4
assert {(x['platform'],x['shortcut']) for x in cm['STEM-017']['finite_contexts']}=={('Windows','CtrlShiftJ'),('Mac','CmdShiftJ')}
assert cm['STEM-U-AVAILABILITY']['requirements']==['REQ-STEM-SEPARATION-U-LIFECYCLE']
for cid in ['STEM-U-UNDO','STEM-U-CANCEL','STEM-U-PERSISTENCE','STEM-U-LOSS','STEM-U-RATE','STEM-U-TRANSPORT','STEM-U-TEARDOWN']:assert cm[cid]['finite_contexts']
fixture=load(P/'fixtures-r2.json');assert fixture['id']=='STEM-OWNED' and all(x in fixture['guard'] for x in ['First verify','nonmuted/nonzero','never a successful absence test'])
adoption=load(P/'audit-adoption-r2.json')
assert [g['id'] for g in adoption['groups']]==[f'G{i:02d}' for i in range(1,14)] and all(g['adopted'] for g in adoption['groups'])
assert adoption['review']['sha256']=='84ca8ab89bd5fb69c7f7221d0fb14543167257bf420cad09c6029351f4a90828'
pin(ROOT/adoption['review']['path'],adoption['review'])
auditreview=load(ROOT/adoption['review']['path']);assert auditreview['reviewed_manifest_sha256']==adoption['audit_manifest']['sha256']=='f6cff20f304a9ea4e99c2d2c93b259556489234607e821fbbe6240232067eff5'
assert auditreview['findings']==[]
delta=load(P/'delta-r2.json')
assert delta['old_manifest_sha256']==digest(P/'manifest-author-r1.json')['sha256']
assert delta['old_requirement_catalog_sha256']==digest(P/'requirements.json')['sha256'] and delta['old_case_catalog_sha256']==digest(P/'cases.json')['sha256']
assert delta['old_requirement_records_verbatim']==18 and delta['old_case_ids_preserved']==29
actual_changes=[dict(id=a['id'],old_action_pointer=f'/{i}/setup_and_action',new_action_pointer=f'/{i}/setup_and_action',old_action=a['setup_and_action'],new_action=c['setup_and_action'],finite_contexts=c.get('finite_contexts')) for i,(a,c) in enumerate(zip(oldcases,cases)) if a['setup_and_action']!=c['setup_and_action']]
assert delta['refined_existing_actions']==actual_changes and delta['refined_existing_action_count']==len(actual_changes)==17
assert delta['new_requirement_ids']==[r['id'] for r in reqs[18:]] and delta['new_case_ids']==[c['id'] for c in cases[29:]]
# Explicit historical resolution only; never monkeypatch or execute other frozen tools.
redirects=load(P/'historical-pin-redirects-r2.json');assert len(redirects)==4
keys={(r['consumer'],r['record_pointer']) for r in redirects};assert len(keys)==4
expected_keys={(str((B/'inventory-revisions/r4-citation-crosswalk/inputs.json').relative_to(ROOT)),p) for p in ['/pins/65','/pins/69']}|{(str((B/'stem-separation-source-audit/input-pins.json').relative_to(ROOT)),p) for p in ['/17','/24']}
assert keys==expected_keys

def historical_read(consumer,ptr,record):
 matches=[r for r in redirects if r['consumer']==consumer and r['record_pointer']==ptr]
 assert len(matches)==1,'Unknown/unapproved historical redirect'
 r=matches[0]
 assert record['path']==r['original_path'] and record['bytes']==r['original_bytes'] and record['sha256']==r['original_sha256']
 assert r['original_path'] in ['wiki/specs/stem-separation.md','wiki/research/stem-separation.md']
 snap=ROOT/r['historical_snapshot']['path'];assert snap.parent==P/'archive-r1'
 pin(snap,r['historical_snapshot']);pin(snap,record)
 return snap.read_bytes()

for r in redirects:
 record=pointer(load(ROOT/r['consumer']),r['record_pointer'])
 data=historical_read(r['consumer'],r['record_pointer'],record)
 snapshot='spec-r1.md' if '/specs/' in r['original_path'] else 'research-r1.md'
 assert data==(P/snapshot).read_bytes()
rejected=0
for variant in ['unknown-pointer','wrong-hash','wrong-path']:
 r=redirects[0];record=deepcopy(pointer(load(ROOT/r['consumer']),r['record_pointer']));ptr=r['record_pointer']
 if variant=='unknown-pointer':ptr='/unapproved'
 if variant=='wrong-hash':record['sha256']='0'*64
 if variant=='wrong-path':record['path']='wiki/specs/synchronization-workflows.md'
 try:historical_read(r['consumer'],ptr,record)
 except AssertionError:rejected+=1
 else:raise AssertionError('Unsafe historical redirect accepted')
assert rejected==3
# Frozen consumer files/pointers and old catalogs remain unchanged; this is not a full R4/audit replay.
for rel in ['stem-separation-source-audit','inventory-revisions/r4-citation-crosswalk']:
 folder=B/rel;m=load(folder/'manifest.json')
 for name,r in m['files'].items():pin(folder/name,r)
# Inspect only historical Stem pin reads above; Sync input records are explicitly outside this resolver.
specpath=ROOT/'wiki/specs/stem-separation.md';researchpath=ROOT/'wiki/research/stem-separation.md'
assert (P/'spec-r2.md').read_bytes()==specpath.read_bytes() and (P/'research-r2.md').read_bytes()==researchpath.read_bytes()
spec=specpath.read_text();research=researchpath.read_text();assert 'revision: 2\n' in spec and 'revision: 2\n' in research
for r in reqs:assert f"### {r['id']} — {r['title']}\n\n**{r['strength']}/target-U.** {r['contract']}" in spec
sys.path.insert(0,str(ROOT/'tools'))
from spec_browser import spec_rows
rows=spec_rows(specpath,spec);assert len(rows)==20 and {r['id'] for r in rows}==set(reqmap)
assert all(x in research for x in ['B029','B030','B032','no mandatory speedup','nonmandatory','other Synchronization'])
counts=load(P/'counts-r2.json')
assert counts==dict(requirements=20,strengths={'D12':17,'U':3},cases=32,documentary_visible_cases=10,all_target_null_U_unexecuted=True,old_requirements_retained=18,old_cases_retained=29,new_requirement_IDs=2,new_case_IDs=3,adopted_audit_groups=13,historical_Stem_pin_redirects=4,source_blocks_unchanged=32,completed_topics=0)
assert Counter(r['strength'] for r in reqs)==counts['strengths'] and sum(c['documentary_expected'] is not None for c in cases)==10
if not preflight:
 m=load(P/'manifest-author-r2.json');assert m['counts']==counts and set(before)==set(m['files'])|{'manifest-author-r2.json'}
 for name,r in m['files'].items():pin(P/name,r)
links=0
for path in [specpath,researchpath,P/'README-r2.md']:
 for target in re.findall(r'\[[^\]]*\]\(([^)\s]+)\)',path.read_text()):
  if re.match(r'[A-Za-z]+:',target):continue
  name,_,fragment=target.partition('#');dest=(path.parent/name).resolve() if name else path
  if preflight and dest==P/'manifest-author-r2.json':continue
  assert dest.is_file(),(path,target)
  if fragment and dest.suffix=='.md':
   slug=lambda h:re.sub(r'[^\w\- ]','',re.sub(r'<[^>]*>|[`*]','',h).lower()).replace(' ','-')
   assert fragment in {slug(h) for h in re.findall(r'^#+\s+(.+)$',dest.read_text(),re.M)},(path,target)
  links+=1
for path in [specpath,researchpath]+[P/n for n in before if Path(n).suffix in {'.md','.json','.py','.txt'}]:
 if path.suffix=='.json':load(path)
 r=subprocess.run(['git','diff','--no-index','--check','/dev/null',str(path)],capture_output=True,text=True)
 assert r.returncode in (0,1) and not r.stdout and not r.stderr,(path,r.stdout,r.stderr)
assert before=={str(p.relative_to(P)):digest(p) for p in P.rglob('*') if p.is_file()}
print(json.dumps(dict(status='passed-read-only-preflight' if preflight else 'passed-read-only-frozen',counts=counts,source_blocks=32,old_R1_files_and_archive_files_preserved=14,input_pins=len(inputs),current_browser_ID_equality=20,local_links=links,historical_Stem_pin_reads_resolved=4,historical_redirect_rejection_selfchecks=3,full_R4_or_source_audit_checker_replayed=False,all_actual_outcomes_null_U_unexecuted=True,writes=False,original_runtime_network_hardware_execution=False),indent=2))
