"""Read-only Resync owner successor validation; no old live-canonical checker replay."""
from pathlib import Path
from hashlib import sha256
from copy import deepcopy
from collections import Counter
import json,re,runpy,subprocess,sys
P=Path(__file__).resolve().parent;ROOT=P.parents[3];B=P.parent
assert sys.dont_write_bytecode and sys.argv[1:] in (['--check'],['--preflight'])
preflight=sys.argv[1:]==['--preflight'];manifest=P/'manifest-author-r3.json'
assert preflight != manifest.exists(),'Preflight only before seal; --check only after seal'
load=lambda q:json.loads(q.read_text())
def info(q):
 raw=q.read_bytes();return dict(bytes=len(raw),sha256=sha256(raw).hexdigest())
def pin(q,r):assert info(q)=={k:r[k] for k in ['bytes','sha256']},q
before={str(q.relative_to(P)):info(q) for q in P.rglob('*') if q.is_file()};assert not any('__pycache__' in n for n in before)
old=load(P/'old-files-r3.json')['files'];assert len(old)==48
assert info(P/'manifest-author-r2.json')['sha256']=='7ebf0944815b79373d660c74ba9a3dfbae60668d079cfa3fdeec9d00c1cb5e77'
r2=load(P/'manifest-author-r2.json');assert set(old)==set(r2['files'])|{'manifest-author-r2.json','validation-author-r2.json','freeze-author-r2.json'}
for n,r in old.items():pin(P/n,r)
for n,r in r2['files'].items():assert old[n]==r
inputs=load(P/'inputs-r3.json');assert len(inputs)==len({r['path'] for r in inputs})
assert not any(r['path'].startswith('wiki/') for r in inputs),'No evolving canonical replay pins'
external={r['path']:info(ROOT/r['path']) for r in inputs}
for r in inputs:pin(ROOT/r['path'],r)
comp=B/'resync-source-reconciliation';review=B/'reviews/resync-source-reconciliation-review.json'
assert info(comp/'manifest.json')['sha256']=='73c27ff10d9ce3999ac93f01e618e770bbe532f86f8fb2c065c14699a6fe97e5'
assert info(review)['sha256']=='84b1b4187b9159118e68239689ded2a0748efc56fdbb22dcfe96e21748c804ff'
assert load(review)['findings']==[] and load(review)['reviewed_manifest_sha256']==info(comp/'manifest.json')['sha256']
for n,r in load(comp/'manifest.json')['files'].items():pin(comp/n,r)
for r in load(comp/'input-pins.json'):pin(ROOT/r['path'],r)
# Load guarded analyst parsers only; neither __main__ writer/check entrypoint runs.
dep=load(P/'dependencies.json')[0];pin(ROOT/dep['path'],dep)
parser=runpy.run_path(str(ROOT/dep['path']))['Chapter']();parser.feed((P/'manual-sync-2026-10-19.html').read_text())
for i,row in enumerate(parser.rows,1):row['id']=f'SYNC-B{i:03}'
assert parser.rows==load(P/'source-blocks.json') and len(parser.rows)==54
context=load(comp/'source-context.json');selection=context['raw_selection'];raw=(ROOT/selection['source_path']).read_text();frag=raw[selection['character_start']:selection['character_end_exclusive']]
assert frag==(comp/selection['file']).read_text() and raw[:selection['character_start']].count('\n')+1==selection['html_line_start']
extract=runpy.run_path(str(comp/'check.py'))['Extract']();extract.feed(frag)
assert extract.blocks==[dict(tag=x['kind'],text=x['text']) for x in load(comp/'selected-source.json')['blocks'][:21]]
assert dict(tag='h4',id='sync',number='17.3.1.2') in extract.headers and len(extract.images)==4 and len(extract.captions)==4
sources=load(P/'source-r3.json');assert sources['primary_R2_source']==load(P/'source.json') and sources['source_context']==context and sources['additional_routing_source']==context['routing']
route=load(B/'routing-monitoring/manual-routing-blocks.json');assert len(route)==125
lookup={r['id']:r for r in parser.rows}
for n,e in zip([38,41,42,43],sources['new_evidence']):
 b=route[n-1];assert b['locator']==f'routing:B{n:03}' and e['block']==b['locator'] and e['block_pointer']=='/'+str(n-1)
 assert e['text']==b['text'] and e['html_line']==b['html_line'] and e['direct_paragraph_anchor']==b['anchor'] is None
 assert e['heading_context']==b['heading_context'] and e['anchor']==b['heading_context'][-1]['anchor']=='sync'
 lookup[e['block']]=dict(anchor=e['anchor'],html_line=e['html_line'])
oldreq=load(P/'requirements-r2.json');oldcases=load(P/'cases-r2.json');reqs=load(P/'requirements-r3.json');cases=load(P/'cases-r3.json')
assert len(oldreq)==27 and len(oldcases)==37 and len(reqs)==29 and len(cases)==42
assert reqs[:27]==oldreq and cases[:37]==oldcases
assert [r['id'] for r in reqs[27:]]==['REQ-SYNC-WORKFLOW-026','REQ-SYNC-WORKFLOW-027']
assert [c['id'] for c in cases[37:]]==['SYNC-026','SYNC-027-STOP-START','SYNC-027-START-ONLY','SYNC-027-DONT-RESYNC','SYNC-U-RESYNC-LIFECYCLE']
rm={r['id']:r for r in reqs};assert len(rm)==29 and Counter(r['strength'] for r in reqs)=={'D12':27,'U':2}
for r in reqs:
 assert r['target_applicability']=='U'
 for e in r['evidence']:assert e['anchor']==lookup[e['block']]['anchor'] and e['html_line']==lookup[e['block']]['html_line']
assert [[e['block'] for e in r['evidence']] for r in reqs[27:]]==[['routing:B038','routing:B041','routing:B042'],['routing:B043']]
fixture=load(P/'fixtures-r3.json');assert fixture['id']=='SYNC-RESYNC-OWNED'
def checkcases(rows):
 assert len(rows)==len({c['id'] for c in rows})==42 and rows[:37]==oldcases
 for c in rows:
  assert set(c['requirements'])<=set(rm) and c['expected'] is c['comparison'] is None and c['target_grade']=='U' and c['executed'] is False
  if c['kind']!='control':assert c['documentary_expected'] is c['documentary_comparator'] is None
 for c in rows[37:]:
  assert c['fixture']=='fixtures-r3.json#SYNC-RESYNC-OWNED' and c['positive_guard']==fixture['positive_guard'] and c['finite_contexts']
  assert all(s in c['positive_guard'] for s in ['genuine usable outgoing MIDI Clock','receiver synchronization','nonzero','Missing feature'])
  if c['id'].startswith('SYNC-U-'):assert c['source_claim'] is None and c['evidence']==[]
  else:assert c['source_claim']==rm[c['requirements'][0]]['contract'] and c['evidence']==rm[c['requirements'][0]]['evidence']
 assert rows[37]['kind']=='control' and rows[37]['documentary_expected'] and rows[37]['documentary_comparator']
 for c,label in zip(rows[38:41],['Stop and Start','Start Only','Don’t Resync']):assert c['kind']=='protocol/timing' and c['finite_contexts'][0]==label
 assert 'known-positive resync-capable' in rows[40]['setup_and_action'] and 'Ordinary Clock' in rows[40]['setup_and_action']
 assert {r for c in rows for r in c['requirements']}==set(rm)
checkcases(cases)
rejected=0
for mode in ['old-action','graded-protocol','missing-positive','wrong-symbolic-mode']:
 c=deepcopy(cases)
 if mode=='old-action':c[11]['setup_and_action']+=' changed'
 elif mode=='graded-protocol':c[38]['documentary_comparator']='invented phase pass'
 elif mode=='missing-positive':c[40]['positive_guard']=''
 else:c[39]['finite_contexts'][0]='guessed mode'
 try:checkcases(c)
 except AssertionError:rejected+=1
 else:raise AssertionError('Invalid R3 case accepted')
assert rejected==4
# Seven append operations reconstruct both entire new catalogs without old-field edits.
delta=load(P/'delta-r3.json');assert len(delta['field_deltas'])==7 and delta['old_requirements_verbatim']==27 and delta['old_cases_verbatim']==37
pin(ROOT/delta['prior_manifest']['path'],delta['prior_manifest']);pin(ROOT/delta['source_reconciliation']['path'],delta['source_reconciliation']);pin(ROOT/delta['source_review']['path'],delta['source_review'])
patched={'requirements-r2.json':deepcopy(oldreq),'cases-r2.json':deepcopy(oldcases)}
for d in delta['field_deltas']:
 rows=patched[d['old_file']];assert d['operation']=='add' and d['old'] is None and d['pointer']=='/'+str(len(rows));rows.append(d['new'])
assert patched['requirements-r2.json']==reqs and patched['cases-r2.json']==cases
history=load(P/'canonical-consumers-r3.json');assert history['current_R2_snapshots']==r2['canonical_snapshots'] and len(history['matching_records'])==5
for r in history['matching_records']:
 if r['kind']=='preserved R2 self-history pin':
  q=ROOT/r['consumer'];assert info(q)==r['consumer_identity_as_of'];v=load(q)
  for k in r['pointer'].strip('/').split('/'):v=v[int(k)] if isinstance(v,list) else v[k]
  assert v==r['record'];pin(P/v['snapshot'],v)
 else:assert r['kind']=='as-of snapshot context, no live redirect' and r['record']['role'].startswith('as-of copied context')
assert len(load(P/'historical-pin-redirects-r2.json'))==4
sp=ROOT/'wiki/specs/synchronization-workflows.md';rp=ROOT/'wiki/research/synchronization-workflows.md';canonical={str(q):info(q) for q in [sp,rp]}
for q,n in [(sp,'spec-r3.md'),(rp,'research-r3.md')]:assert q.read_bytes()==(P/n).read_bytes() and 'revision: 3\n' in q.read_text()
for r in reqs:assert f"### {r['id']} — {r['title']}\n\n**{r['strength']}/target-U.** {r['contract']}" in sp.read_text()
sys.path.insert(0,str(ROOT/'tools'))
from spec_browser import spec_rows
browser=spec_rows(sp,sp.read_text());assert len(browser)==29 and {r['id'] for r in browser}==set(rm)
links=0
for q in [sp,rp,P/'README-r3.md']:
 for target in re.findall(r'\[[^\]]*\]\(([^)\s]+)\)',q.read_text()):
  if re.match('[A-Za-z]+:',target):continue
  name,_,fragment=target.partition('#');dest=(q.parent/name).resolve() if name else q
  if preflight and dest==manifest:continue
  assert dest.is_file(),(q,target)
  if fragment and dest.suffix=='.md':
   slug=lambda h:re.sub(r'[^\w\- ]','',re.sub(r'<[^>]*>|[`*]','',h).lower()).replace(' ','-')
   assert fragment in {slug(h) for h in re.findall(r'^#+\s+(.+)$',dest.read_text(),re.M)},target
  links+=1
whitespace=0
for q in [sp,rp]+[P/n for n in before if Path(n).suffix in ['.json','.md','.py','.txt']]:
 if q.suffix=='.json':load(q)
 r=subprocess.run(['git','diff','--no-index','--check','/dev/null',str(q)],capture_output=True);assert r.returncode in (0,1) and not r.stdout and not r.stderr,q;whitespace+=1
if not preflight:
 m=load(manifest);assert m['revision']==3 and set(m['files'])==set(before)-{manifest.name}
 for n,r in m['files'].items():pin(P/n,r)
 for r in m['canonical_snapshots']:pin(ROOT/r['canonical'],r);pin(P/r['snapshot'],r)
assert before=={str(q.relative_to(P)):info(q) for q in P.rglob('*') if q.is_file()}
assert external=={r['path']:info(ROOT/r['path']) for r in inputs} and canonical=={str(q):info(q) for q in [sp,rp]}
print(json.dumps(dict(status='passed-read-only-preflight' if preflight else 'passed-read-only-frozen',scope='partial Resync ownerR3 source/pin/delta/null integrity only',old_R2_tree_files_preserved=48,requirements=29,strengths={'D12':27,'U':2},cases=42,old_requirement_records_verbatim=27,old_case_records_verbatim=37,append_deltas=7,documentary_visible=9,documentary_null=33,original_Sync_blocks=54,new_routing_evidence_blocks=4,complete_retained_routing_Sync_context_blocks=10,input_pins=len(inputs),browser_exact_IDs=29,canonical_snapshots=2,local_links=links,rejection_fixtures=4,untracked_whitespace_files=whitespace,all_actual_null_U_unexecuted=True,new_protocol_timing_lifecycle_docoracles_null=True,old_checker_or_current_consumer_execution=False,original_hardware_network_candidate_execution=False,writes=False),indent=2))
