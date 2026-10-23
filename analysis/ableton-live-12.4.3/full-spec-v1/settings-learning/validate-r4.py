"""Read-only two-frontend Settings R4 validation; no author/product/source-example execution."""
from pathlib import Path
from hashlib import sha256
from copy import deepcopy
from collections import Counter
import json,re,runpy,subprocess,sys
P=Path(__file__).resolve().parent;ROOT=P.parents[3];B=P.parent
assert sys.dont_write_bytecode and sys.argv[1:] in (['--check'],['--preflight'])
preflight=sys.argv[1:]==['--preflight'];assert not preflight or not (P/'manifest-author-r4.json').exists()
def load(q):return json.loads(q.read_text())
def info(q):
 b=q.read_bytes();return dict(bytes=len(b),sha256=sha256(b).hexdigest())
def pin(q,r):assert info(q)=={k:r[k] for k in ['bytes','sha256']},q
before={str(q.relative_to(P)):info(q) for q in P.rglob('*') if q.is_file()};assert not any('__pycache__' in n for n in before)
prior=load(P/'manifest-author-r3.json');assert info(P/'manifest-author-r3.json')['sha256']=='4570f813d2908468657d937aed206ea04dae2b801edaa1839d04c1797a60adb6' and len(prior['files'])==45
for n,r in prior['files'].items():pin(P/n,r)
inputs=load(P/'inputs-r4.json');assert len(inputs)==len({r['path'] for r in inputs})
assert not any(r['path'].startswith('wiki/') for r in inputs),'No mutable cross-owner canonical pins'
external_before={r['path']:info(ROOT/r['path']) for r in inputs}
for r in inputs:pin(ROOT/r['path'],r)
comp=B/'settings-owner-reconciliation';assert info(comp/'manifest.json')['sha256']=='057f3c360b605d3f8d876d9f9b187bca5c15abd4a5f3c6628de870a9fc9d4b67'
for n,r in load(comp/'manifest.json')['files'].items():pin(comp/n,r)
for r in load(comp/'source-input-pins.json'):pin(ROOT/r['path'],r)
review=load(B/'reviews/settings-owner-reconciliation-review.json');assert review['findings']==[] and review['reviewed_manifest_sha256']==info(comp/'manifest.json')['sha256']
assert info(B/'reviews/settings-owner-reconciliation-review.json')['sha256']=='7cb939ffccb397dba402a4ffa74f2b907704793cf5c8748e61ad37cdbe835172'
source=load(P/'source.json');pin(P/source['file'],source);dep=load(P/'dependencies.json')[0];pin(ROOT/dep['path'],dep)
# Inspected analyst HTMLParser class only; its guarded writer never runs here.
parser=runpy.run_path(str(ROOT/dep['path']))['Chapter']();parser.feed((P/source['file']).read_text())
for i,b in enumerate(parser.rows,1):b['id']=f'SET-B{i:03}'
assert parser.rows==load(P/'source-blocks.json') and len(parser.rows)==70
oldreq=load(P/'requirements.json');oldcases=load(P/'cases-r3.json');reqs=load(P/'requirements-r4.json');cases=load(P/'cases-r4.json');assert len(oldreq)==21 and len(oldcases)==31
assert len(reqs)==23 and reqs[:21]==oldreq and len(cases)==33 and cases[:31]==oldcases
assert [r['id'] for r in reqs[21:]]==['REQ-SETTINGS-LEARNING-020','REQ-SETTINGS-LEARNING-021']
assert [c['id'] for c in cases[31:]]==['SET-020','SET-021']
rm={r['id']:r for r in reqs};assert len(rm)==23 and Counter(r['strength'] for r in reqs)=={'D12':21,'U':2}
for r in reqs:
 assert r['target_applicability']=='U'
 for e in r['evidence']:
  b=parser.rows[int(e['block'].split('B')[1])-1];assert e['anchor']==b['anchor'] and e['html_line']==b['html_line']
def check_new(rows):
 assert len(rows)==len({c['id'] for c in rows})==33
 assert rows[:31]==oldcases
 for c in rows:
  assert set(c['requirements'])<=set(rm) and c['expected'] is c['comparison'] is None and c['target_grade']=='U' and c['executed'] is False
  if c['kind']=='timing' or c['id'].startswith('SET-U-'):assert c['documentary_expected'] is c['documentary_comparator'] is None
 for c in rows[31:]:
  assert c['kind']=='control' and c['fixture']=='fixtures-r2.json#SET-OWNED'
  assert c['source_claim']==rm[c['requirements'][0]]['contract'] and c['evidence']==rm[c['requirements'][0]]['evidence']
  assert c['documentary_expected'] and c['documentary_comparator'] and len(c['finite_contexts'])==2
  assert all(x in c['prerequisites'] for x in ['independently eligible','genuine working positive','Missing capability/input is U'])
 assert {r for c in rows for r in c['requirements']}==set(rm)
check_new(cases)
rejected=0
for mode in ['old-record-change','new-target-grade','missing-positive-guard']:
 x=deepcopy(cases)
 if mode=='old-record-change':x[16]['setup_and_action']+=' changed'
 elif mode=='new-target-grade':x[-1]['expected']='unsupported scan result'
 else:x[-1]['prerequisites']=''
 try:check_new(x)
 except AssertionError:rejected+=1
 else:raise AssertionError('Invalid successor accepted')
assert rejected==3
assert [r['evidence'][0]['block'] for r in reqs[21:]]==['SET-B059','SET-B066']
assert [c['evidence'][0]['block'] for c in cases[31:]]==['SET-B059','SET-B066']
fixture=load(P/'fixtures-r2.json');assert fixture['id']=='SET-OWNED' and 'not a passing negative test' in fixture['positive_guard']
delta=load(P/'delta-r4.json');pin(P/'manifest-author-r3.json',delta['prior_manifest'])
assert delta['old_requirement_records_verbatim']==21 and delta['old_case_records_verbatim']==31
assert delta['new_requirement_ids']==[r['id'] for r in reqs[21:]] and delta['new_case_ids']==[c['id'] for c in cases[31:]]
assert delta['adopted_local_facets']==['SOR-022','SOR-031','SOR-032'] and delta['no_new_search_or_Edit_lifecycle_law'] is True
pin(P/delta['discovery_context']['snapshot'],delta['discovery_context'])
context=(P/delta['discovery_context']['snapshot']).read_text();assert '### REQ-PLUGIN-DISCOVERY-002' in context and 'Which labelled control is which switch' in context
assert 'system folders' in context and 'custom folder' in context
# Unchanged historical pin identities; no old R4/SOR/audit tool is replayed against current pages.
r4=load(B/'inventory-revisions/r4-citation-crosswalk/inputs.json')['pins']
for i,n,path in [(64,'research-r1.md','wiki/research/settings-learning-workflows.md'),(68,'spec-r1.md','wiki/specs/settings-learning-workflows.md')]:assert r4[i]['path']==path;pin(P/n,r4[i])
sp=ROOT/'wiki/specs/settings-learning-workflows.md';rp=ROOT/'wiki/research/settings-learning-workflows.md';canonical_before={str(q):info(q) for q in [sp,rp]}
for q,n in [(sp,'spec-r4.md'),(rp,'research-r4.md')]:assert q.read_bytes()==(P/n).read_bytes() and 'revision: 4\n' in q.read_text()
for r in reqs:assert f"### {r['id']} — {r['title']}\n\n**{r['strength']}/target-U.** {r['contract']}" in sp.read_text()
sys.path.insert(0,str(ROOT/'tools'))
from spec_browser import spec_rows
browser=spec_rows(sp,sp.read_text());assert len(browser)==23 and {r['id'] for r in browser}==set(rm)
assert all(x in rp.read_text() for x in ['SOR021','MF011','MF015','RC-020','explicit Off','Max for Live add-on','Resync remains','Q031','No all-G09 closure'])
assert sum(c['documentary_expected'] is not None for c in cases)==20
if not preflight:
 m=load(P/'manifest-author-r4.json');assert set(m['files'])==set(before)-{'manifest-author-r4.json'}
 for n,r in m['files'].items():pin(P/n,r)
 for r in m['canonical_snapshots']:pin(ROOT/r['canonical'],r);pin(P/r['snapshot'],r)
links=0
for q in [sp,rp,P/'README-r4.md']:
 for target in re.findall(r'\[[^\]]*\]\(([^)\s]+)\)',q.read_text()):
  if re.match('[A-Za-z]+:',target):continue
  n,_,frag=target.partition('#');dest=(q.parent/n).resolve() if n else q
  if preflight and dest==P/'manifest-author-r4.json':continue
  assert dest.is_file(),(q,target)
  if frag and dest.suffix=='.md':
   slug=lambda h:re.sub(r'[^\w\- ]','',re.sub(r'<[^>]*>|[`*]','',h).lower()).replace(' ','-')
   assert frag in {slug(h) for h in re.findall(r'^#+\s+(.+)$',dest.read_text(),re.M)},target
  links+=1
for q in [sp,rp]+[P/n for n in before if Path(n).suffix in ['.md','.json','.py','.txt']]:
 if q.suffix=='.json':load(q)
 r=subprocess.run(['git','diff','--no-index','--check','/dev/null',str(q)],capture_output=True);assert r.returncode in (0,1) and not r.stdout and not r.stderr,q
assert before=={str(q.relative_to(P)):info(q) for q in P.rglob('*') if q.is_file()}
assert external_before=={r['path']:info(ROOT/r['path']) for r in inputs} and canonical_before=={str(q):info(q) for q in [sp,rp]}
print(json.dumps(dict(status='passed-read-only-preflight' if preflight else 'passed-read-only-frozen',prior_R3_payloads_and_seal_preserved=46,requirements=23,requirement_strengths={'D12':21,'U':2},old_requirement_records_verbatim=21,cases=33,old_case_records_verbatim=31,documentary_visible=20,null_documentary=13,all_actual_outcomes_null_U_unexecuted=True,source_blocks=70,input_pins=len(inputs),reconciliation_payloads=66,reconciliation_source_pins=32,browser_exact_IDs=23,local_links=links,rejection_fixtures=3,other_G09_obligations='pending',full_historical_crosspacket_replay=False,writes=False),indent=2))
