"""Read-only finite audit-adoption checks; no original or prior live-canonical validator calls."""
from pathlib import Path
from hashlib import sha256
from copy import deepcopy
from collections import Counter
import json,re,runpy,subprocess,sys
P=Path(__file__).resolve().parent;ROOT=P.parents[3];B=P.parent;A=B/'warping-source-audit'
assert sys.dont_write_bytecode and sys.argv[1:] in (['--check'],['--preflight'])
preflight=sys.argv[1:]==['--preflight'];manifest=P/'manifest-author-r2.json'
assert preflight != manifest.exists(),'Preflight before seal only; frozen replay uses --check'
load=lambda q:json.loads(q.read_text())
def info(q):
 raw=q.read_bytes();return dict(bytes=len(raw),sha256=sha256(raw).hexdigest())
def pin(q,r):assert info(q)=={k:r[k] for k in ['bytes','sha256']},q
def pointer(value,ptr):
 for k in ptr.split('/')[1:]:value=value[int(k)] if isinstance(value,list) else value[k.replace('~1','/').replace('~0','~')]
 return value
before={str(q.relative_to(P)):info(q) for q in P.rglob('*') if q.is_file()};assert not any('__pycache__' in n for n in before)
old=load(P/'old-files-r2.json');assert len(old['files'])==15
for n,r in old['files'].items():pin(P/n,r)
pin(ROOT/old['original_review']['path'],old['original_review'])
assert info(P/'manifest-author-r1.json')['sha256']=='b17efb2eb29b165239bab421e53e49f69117e69fa80f97927ad0e54dac76ba68'
m1=load(P/'manifest-author-r1.json');assert len(m1['files'])==14 and set(old['files'])==set(m1['files'])|{'manifest-author-r1.json'}
for n,r in m1['files'].items():assert old['files'][n]==r
inputs=load(P/'inputs-r2.json');assert len(inputs)==len({r['path'] for r in inputs})==68
assert not any(r['path'].startswith('wiki/') for r in inputs),'No mutable canonical replay pin'
external={r['path']:info(ROOT/r['path']) for r in inputs}
for r in inputs:pin(ROOT/r['path'],r)
assert info(A/'manifest.json')['sha256']=='b225aed9cdd516e68e98aee32c2cd06a814667a97ba20701a2ea85abb45f9700'
for n,r in load(A/'manifest.json')['files'].items():pin(A/n,r)
for r in load(A/'input-pins.json'):pin(ROOT/r['path'],r)
adoption=load(P/'audit-adoption-r2.json');pin(ROOT/adoption['audit_manifest']['path'],adoption['audit_manifest']);pin(ROOT/adoption['audit_review']['path'],adoption['audit_review'])
assert adoption['audit_review']['sha256']=='b2ff0863665df4bc4d3e3e463be1238aaeb50040955ba2d81819dc5cbbab19d6'
assert load(ROOT/adoption['audit_review']['path'])['required_findings']==[]
# Pure retained-source parser, pinned among the15 original files; no __main__ or old validator.
source=load(P/'sources.json')[0];pin(P/source['path'],source);config=load(P/'derivations.json')
parser=runpy.run_path(str(P/'source_parser.py'));blocks=parser['extract']((P/source['path']).read_text(),config['name'],config['start_anchor'],config['stop_heading_level'])
assert blocks==load(P/'manual-blocks.json') and len(blocks)==131
assert (P/'manual.txt').read_text()==''.join(f"{r['locator']} HTML:{r['html_line']} {r['text']}\n" for r in blocks)
byblock={r['locator']:r for r in blocks}
oldreq=load(P/'requirements.json');oldcases=load(P/'cases.json');reqs=load(P/'requirements-r2.json');cases=load(P/'cases-r2.json')
assert len(oldreq)==len(reqs)==50 and len(oldcases)==88 and len(cases)==91
assert [r['id'] for r in reqs]==[r['id'] for r in oldreq] and [c['id'] for c in cases[:88]]==[c['id'] for c in oldcases]
assert Counter(r['provenance'] for r in reqs)=={'D12':44,'U':6}
changed_req={r['id'] for a,r in zip(oldreq,reqs) if a!=r};assert changed_req=={'REQ-WFW-001','REQ-WFW-003','REQ-WFW-021','REQ-WFW-029'}
for a,z in zip(oldreq,reqs):
 assert set(a)==set(z)
 assert {k for k in a if a[k]!=z[k]}<=({'contract'} if z['id'] in changed_req else set())
 assert z['target_applicability']=='U' and set(z['source_blocks'])<=set(byblock)
rm={r['id']:r for r in reqs}
# Every non-delta old field remains exact; no runtime grading change permitted.
allowed={'setup_and_action','source_claim','documentary_expected','finite_contexts'}
for a,z in zip(oldcases,cases):
 assert {k for k in set(a)|set(z) if a.get(k)!=z.get(k)}<=allowed
for n in [8,18,22]:assert cases[n-1]==oldcases[n-1]
assert cases[20]['setup_and_action'].startswith(oldcases[20]['setup_and_action'])
assert reqs[26]==oldreq[26] # Short Warp Marker vs long start-marker source clause preserved.
assert [c['id'] for c in cases[88:]]==['WFW-089','WFW-090','WFW-091']
def check_oracles(rows):
 assert len(rows)==len({c['id'] for c in rows})==91
 for c in rows:
  assert len(c['requirements'])==1 and c['requirements'][0] in rm
  r=rm[c['requirements'][0]];assert c['source_claim']==r['contract'] and c['source_blocks']==r['source_blocks']
  assert c['preconditions']==['F0','positive-path-gate']
  assert c['expected'] is c['comparison'] is None and c['target_grade']=='U' and c['executed'] is False
  visible=c['kind'] in ['control','state','boundary'] and r['provenance']=='D12'
  if visible:assert c['documentary_expected'] and c['documentary_comparator'].startswith('Only named visible control')
  else:assert c['documentary_expected'] is c['documentary_comparator'] is None
  assert set(c.get('source_context_blocks',[]))<=set(byblock)
 assert {r for c in rows for r in c['requirements']}==set(rm)
check_oracles(cases)
assert sum(c['documentary_expected'] is not None for c in cases)==41
assert sum(cases[i]!=oldcases[i] for i in range(88))==24
# Exact finite patch replay reconstructs requirements/cases/fixtures from unchanged originals.
delta=load(P/'delta-r2.json');assert len(delta['field_deltas'])==64 and delta['new_normative_IDs']==[]
patched={n:deepcopy(load(P/n)) for n in ['requirements.json','cases.json','fixtures.json']}
for d in delta['field_deltas']:
 obj=patched[d['old_file']];keys=d['pointer'].split('/')[1:]
 for k in keys[:-1]:obj=obj[int(k)] if isinstance(obj,list) else obj[k.replace('~1','/').replace('~0','~')]
 key=int(keys[-1]) if isinstance(obj,list) else keys[-1].replace('~1','/').replace('~0','~')
 if d['operation']=='add':
  if isinstance(obj,list):assert key==len(obj);obj.append(deepcopy(d['new']))
  else:assert key not in obj;obj[key]=deepcopy(d['new'])
  assert d['old'] is None
 else:assert d['operation']=='replace' and obj[key]==d['old'];obj[key]=deepcopy(d['new'])
for a,z in [('requirements.json','requirements-r2.json'),('cases.json','cases-r2.json'),('fixtures.json','fixtures-r2.json')]:assert patched[a]==load(P/z)
fixture=load(P/'fixtures-r2.json');original_fixture=load(P/'fixtures.json');assert all(fixture[k]==v for k,v in original_fixture.items())
assert set(fixture)-set(original_fixture)=={'R2-positive-contexts','R2-source-history','R2-owner-boundaries'}
# Guard assertions are structural admission checks, not measured processing or source proof.
def contexts_ok(rows):
 assert all(x in rows[6]['setup_and_action'] for x in ['actually active playing','genuine nonempty generated','Flags, audio activity'])
 assert all(x in rows[9]['setup_and_action'] for x in ['explicitly activate Tempo Follower','genuine interpretation','no active leader'])
 assert all(x in rows[47]['setup_and_action'] for x in ['independently establish actually active','not active-leader proof'])
 assert 'separately admitted productive external reference' in rows[46]['setup_and_action']
 assert 'explicitly invoke' in rows[28]['setup_and_action']
 assert all(x in rows[90]['setup_and_action'] for x in ['genuine Sample Editor scrolling','Arrangement scrub','clip scrub'])
 assert all(x in rows[26]['setup_and_action'] for x in ['uneven short','long Auto-Warp','start-marker'])
contexts_ok(cases)
rejected=0
for mode in ['old-ID','actual-grade','timing-documentary','positive-leader','wrong-mode-context']:
 rows=deepcopy(cases)
 if mode=='old-ID':rows[0]['requirements']=['invented']
 elif mode=='actual-grade':rows[0]['expected']='invented numeric tempo result'
 elif mode=='timing-documentary':rows[45]['documentary_comparator']='invented Link phase tolerance'
 elif mode=='positive-leader':rows[6]['setup_and_action']='leader flags only'
 else:rows[90]['setup_and_action']='Follow switch visible only'
 try:check_oracles(rows);contexts_ok(rows)
 except (AssertionError,KeyError):rejected+=1
 else:raise AssertionError('Invalid successor accepted')
assert rejected==5
assert [g['audit_group'] for g in adoption['groups']]==[f'G{i:02}' for i in range(1,17)]
auditg=load(A/'proposed-deltas-derived.json')
for i,g in enumerate(adoption['groups']):
 oldg=auditg[i];assert g['source_blocks']==oldg['source_blocks'] and g['claim_ids']==oldg['claim_ids'] and g['title']==oldg['title']
 assert g['new_normative_IDs']==[] and g['private_or_numerical_law'] is False
 for cid,ptr in zip(g['case_ids'],g['case_pointers']):assert pointer(cases,ptr)['id']==cid
assert adoption['Q032']=='open' and adoption['zero_completed_topics'] is True
# Exact five historical pin rows are validated against R1 snapshots, never current wiki.
consumers=load(P/'canonical-consumers-r2.json');assert consumers['direct_live_pin_records']==5
assert consumers['own_R1_snapshot_routes']==m1['canonical_snapshots']
for row in consumers['records']:
 if row['disposition'].startswith('historical live'):
  q=ROOT/row['consumer'];pin(q,row['consumer_identity_as_of']);assert pointer(load(q),row['pointer'])==row['record'];pin(ROOT/row['historical_snapshot'],row['record'])
 else:assert row['disposition']=='as-of copied snapshot, unaffected'
sp=ROOT/'wiki/specs/warping-workflows.md';rp=ROOT/'wiki/research/warping-workflows.md';canonical={str(q):info(q) for q in [sp,rp]}
for q,n in [(sp,'spec-r2.md'),(rp,'research-r2.md')]:assert q.read_bytes()==(P/n).read_bytes() and 'revision: 2\n' in q.read_text()
spec=sp.read_text()
for r in reqs:assert f"### {r['id']} — {r['title']}\n\n**{r['provenance']}/target-U.** {r['contract']}" in spec
for c in cases:assert f"| {c['id']} | {c['requirements'][0]} | {c['kind']} | {c['title']} |" in spec
sys.path.insert(0,str(ROOT/'tools'))
from spec_browser import spec_rows
rows=spec_rows(sp,spec);assert len(rows)==50 and {r['id'] for r in rows}==set(rm)
links=0
for q in [sp,rp,P/'README-r2.md']:
 for target in re.findall(r'\[[^\]]*\]\(([^)\s]+)\)',q.read_text()):
  if re.match('[A-Za-z]+:',target):continue
  name,_,fragment=target.partition('#');dest=(q.parent/name).resolve() if name else q
  if preflight and dest==manifest:continue
  assert dest.is_file(),(q,target)
  if fragment and dest.suffix=='.md':
   slug=lambda h:re.sub(r'[^\w\- ]','',re.sub(r'<[^>]*>|[`*]','',h).lower()).replace(' ','-')
   assert fragment in {slug(h) for h in re.findall(r'^#+\s+(.+)$',dest.read_text(),re.M)},(q,target)
  links+=1
whitespace=0
for q in [sp,rp]+[P/n for n in before if Path(n).suffix in ['.py','.json','.md','.txt']]:
 if q.suffix=='.json':load(q)
 r=subprocess.run(['git','diff','--no-index','--check','/dev/null',str(q)],capture_output=True);assert r.returncode in (0,1) and not r.stdout and not r.stderr,q;whitespace+=1
if not preflight:
 m=load(manifest);assert m['revision']==2 and set(m['files'])==set(before)-{manifest.name}
 for n,r in m['files'].items():pin(P/n,r)
 for r in m['canonical_snapshots']:pin(ROOT/r['canonical'],r);pin(P/r['snapshot'],r)
assert before=={str(q.relative_to(P)):info(q) for q in P.rglob('*') if q.is_file()}
assert external=={r['path']:info(ROOT/r['path']) for r in inputs} and canonical=={str(q):info(q) for q in [sp,rp]}
print(json.dumps(dict(status='passed-read-only-preflight' if preflight else 'passed-read-only-frozen',scope='partial documentary Warp ownerR2 integrity; independent review pending',old_R1_files_preserved=15,original_review_preserved=True,requirements=50,provenance={'D12':44,'U':6},old_requirement_IDs_retained=50,changed_contracts=4,cases=91,old_case_IDs_retained=88,changed_old_case_records=24,new_U_case_records=3,documentary_visible=41,documentary_null=50,exact_field_deltas=64,source_blocks=131,input_pins=68,audit_groups=16,historical_direct_consumer_pins=5,browser_exact_IDs=50,canonical_snapshots=2,local_links=links,rejection_fixtures=5,untracked_whitespace_files=whitespace,all_actual_null_U_unexecuted=True,all_signal_timing_analysis_U_docoracles_null=True,old_validator_or_original_runtime_execution=False,writes=False),indent=2))
