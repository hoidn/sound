"""Read-only bounded Video R2 validation; no author/source/example/runtime execution."""
from pathlib import Path
from copy import deepcopy
from hashlib import sha256
from collections import Counter
import json,re,runpy,subprocess,sys
P=Path(__file__).resolve().parent;ROOT=P.parents[3];B=P.parent
assert sys.dont_write_bytecode and sys.argv[1:] in (['--check'],['--preflight'])
preflight=sys.argv[1:]==['--preflight'];assert not preflight or not (P/'manifest-author-r2.json').exists()
def load(q):return json.loads(q.read_text())
def info(q):
 b=q.read_bytes();return dict(bytes=len(b),sha256=sha256(b).hexdigest())
def pin(q,p):assert info(q)=={k:p[k] for k in ['bytes','sha256']},q
def pointer(v,p):
 for k in p[1:].split('/') if p else []:
  k=k.replace('~1','/').replace('~0','~');v=v[int(k)] if isinstance(v,list) else v[k]
 return v
before={str(q.relative_to(P)):info(q) for q in P.rglob('*') if q.is_file()};assert not any('__pycache__' in p for p in before)
oldmanifest=load(P/'manifest-author-r1.json');assert info(P/'manifest-author-r1.json')['sha256']=='ba9c19eb8836759b57c33e939aa294a390dd9d0199b00948396b769d0566467e'
assert len(oldmanifest['files'])==13
for n,r in oldmanifest['files'].items():pin(P/n,r);pin(P/'archive-r1'/n,r);assert (P/n).read_bytes()==(P/'archive-r1'/n).read_bytes()
assert (P/'manifest-author-r1.json').read_bytes()==(P/'archive-r1/manifest-author-r1.json').read_bytes()
archives=load(P/'archive-r1-pins.json');assert len(archives)==14
for r in archives:pin(ROOT/r['path'],r)
assert {str(q.relative_to(ROOT)) for q in (P/'archive-r1').iterdir()}=={r['path'] for r in archives}
inputs=load(P/'inputs-r2.json');assert len(inputs)==len({r['path'] for r in inputs})
assert not {'wiki/specs/video-workflows.md','wiki/research/video-workflows.md'}&{r['path'] for r in inputs}
external_before={r['path']:info(ROOT/r['path']) for r in inputs}
for r in inputs:pin(ROOT/r['path'],r)
source=load(P/'source.json');pin(P/source['file'],source)
for r in load(P/'dependencies.json'):pin(ROOT/r['path'],r)
# Inspected existing analyst Chapter parser only. Its guarded source writer is inactive.
parser=runpy.run_path(str(ROOT/load(P/'dependencies.json')[0]['path']))['Chapter']();parser.feed((P/source['file']).read_text())
for i,b in enumerate(parser.rows,1):b['id']=f'VID-B{i:03}'
assert len(parser.rows)==39 and parser.rows==load(P/'source-blocks.json');blocks={b['id']:b for b in parser.rows}
oldreq=load(P/'requirements.json');oldcases=load(P/'cases.json');reqs=load(P/'requirements-r2.json');cases=load(P/'cases-r2.json')
assert len(oldreq)==18 and reqs[:18]==oldreq and len(reqs)==20 and len({r['id'] for r in reqs})==20
assert [r['id'] for r in reqs[18:]]==['REQ-VIDEO-WORKFLOW-017','REQ-VIDEO-WORKFLOW-018']
assert len(oldcases)==28 and len(cases)==34 and [c['id'] for c in cases[:28]]==[c['id'] for c in oldcases]
rm={r['id']:r for r in reqs};cm={c['id']:c for c in cases}
for r in reqs:
 assert r['target_applicability']=='U' and r['contract']
 for e in r['evidence']:assert e['anchor']==blocks[e['block']]['anchor'] and e['html_line']==blocks[e['block']]['html_line']
def validate_cases(rows,fixture):
 assert len(rows)==len({c['id'] for c in rows})==34
 assert all(t in fixture['positive_guard'] for t in ['First independently verify','nonmuted/nonzero','never a successful absence test'])
 for c in rows:
  assert set(c['requirements'])<=set(rm) and c['fixture']=='fixtures-r2.json#VID-OWNED' and c['setup_and_action']
  assert c['expected'] is c['comparison'] is None and c['target_grade']=='U' and c['executed'] is False
  if c['kind'] in ['signal','file','timing'] or c['id'].startswith('VID-U-'):assert c['documentary_expected'] is c['documentary_comparator'] is None
  assert c['source_claim']==(None if c['id'].startswith('VID-U-') else rm[c['requirements'][0]]['contract'])
  assert c['evidence']==rm[c['requirements'][0]]['evidence']
 assert {r for c in rows for r in c['requirements']}==set(rm)
fixture=load(P/'fixtures-r2.json');validate_cases(cases,fixture);assert 'leading/interior/trailing' in fixture['media'] and 'Only interior gaps require positive material on both sides' in fixture['media']
rejected=0
for mode in ['graded-timing','duplicate-ID','absent-positive-guard']:
 rows=deepcopy(cases);f=deepcopy(fixture)
 if mode=='graded-timing':next(c for c in rows if c['id']=='VID-018')['documentary_expected']='unsupported waveform pass'
 elif mode=='duplicate-ID':rows[-1]['id']=rows[0]['id']
 else:f['positive_guard']=''
 try:validate_cases(rows,f)
 except AssertionError:rejected+=1
 else:raise AssertionError('Invalid case/fixture accepted')
assert rejected==3
assert cm['VID-005']['kind']=='file'
assert {(x['partial_stream'],x['gap_position']) for x in cm['VID-009']['finite_contexts']}=={(s,p) for s in ['video','audio'] for p in ['leading','interior','trailing']}
assert len(cm['VID-008']['finite_contexts'])==6 and {x['platform'] for x in cm['VID-008']['finite_contexts']}=={'Windows','Mac'}
assert {(x['platform'],x['gesture']) for x in cm['VID-008']['finite_contexts'] if '+' in x['gesture']}=={('Windows','Alt+double-click'),('Mac','Option+double-click')}
assert len(cm['VID-007']['finite_contexts'])==4 and len(cm['VID-010']['finite_contexts'])==2
assert {x['prior_window'] for x in cm['VID-017']['finite_contexts']}=={'independently known hidden','independently known visible'}
assert len(cm['VID-018']['finite_contexts'])==3
assert {x['flagged_count'] for x in cm['VID-U-LEADER-COUNTS']['finite_contexts']}=={0,1,3}
assert all(cm[x]['source_claim'] is None for x in ['VID-U-DEFAULT-HISTORY','VID-U-LEADER-COUNTS','VID-U-EXPORT-RANGE','VID-U-AVAILABILITY'])
assert all(cm[x]['finite_contexts'] for x in ['VID-U-UNDO','VID-U-CANCEL','VID-U-PERSISTENCE','VID-U-SOURCE-LOSS','VID-U-RATE','VID-U-TRANSPORT','VID-U-DISPLAY','VID-U-TEARDOWN'])
adoption=load(P/'audit-adoption-r2.json');pin(ROOT/adoption['review']['path'],adoption['review']);pin(ROOT/adoption['audit_manifest']['path'],adoption['audit_manifest'])
assert adoption['review']['sha256']=='e0fd362930fe0514e164cfd4aaecdde9139851d64e2b75e57ffe7b1ae9da8524'
review=load(ROOT/adoption['review']['path']);assert review['findings']==[] and review['reviewed_manifest_sha256']==adoption['audit_manifest']['sha256']=='27eee803998ec4903be8e9c922c7e34afa4493b2b685917562bc91f9dd8f0c40'
assert [g['id'] for g in adoption['groups']]==[f'G{i:02}' for i in range(1,10)] and all(g['adopted'] for g in adoption['groups'])
delta=load(P/'delta-r2.json')
for key,name in [('old_manifest','manifest-author-r1.json'),('old_requirement_catalog','requirements.json'),('old_case_catalog','cases.json')]:pin(P/name,delta[key])
actual=[]
for i,(a,b) in enumerate(zip(oldcases,cases)):
 for field in sorted(set(a)|set(b)):
  if a.get(field)!=b.get(field) or (field in a)!=(field in b):actual.append(dict(id=a['id'],old_pointer='/'+str(i)+'/'+field,new_pointer='/'+str(i)+'/'+field,field=field,old_present=field in a,new_present=field in b,old=a.get(field),new=b.get(field)))
assert delta['existing_case_field_changes']==actual
assert delta['changed_existing_action_IDs']==[a['id'] for a,b in zip(oldcases,cases) if a['setup_and_action']!=b['setup_and_action']]
assert delta['cleared_signal_file_timing_documentary_expectation_IDs']==['VID-005','VID-009','VID-011','VID-012','VID-013']
assert delta['new_requirement_ids']==[r['id'] for r in reqs[18:]] and delta['new_case_ids']==[c['id'] for c in cases[28:]]
# Exactly four local historical Video pin reads, not a global adapter/replay.
redirects=load(P/'historical-pin-redirects-r2.json');assert len(redirects)==4
expected={(str((B/'inventory-revisions/r4-citation-crosswalk/inputs.json').relative_to(ROOT)),p) for p in ['/pins/67','/pins/71']}|{(str((B/'video-source-audit/input-pins.json').relative_to(ROOT)),p) for p in ['/29','/30']}
assert {(r['consumer'],r['record_pointer']) for r in redirects}==expected
def historical_read(consumer,ptr,record):
 matches=[r for r in redirects if (r['consumer'],r['record_pointer'])==(consumer,ptr)];assert len(matches)==1,'Unapproved historical read'
 r=matches[0];assert record['path']==r['original_path'] and record['bytes']==r['original_bytes'] and record['sha256']==r['original_sha256']
 assert r['original_path'] in ['wiki/specs/video-workflows.md','wiki/research/video-workflows.md']
 q=ROOT/r['historical_snapshot']['path'];assert q.parent==P/'archive-r1';pin(q,record);pin(q,r['historical_snapshot']);return q.read_bytes()
for r in redirects:
 record=pointer(load(ROOT/r['consumer']),r['record_pointer']);data=historical_read(r['consumer'],r['record_pointer'],record)
 assert data==(P/('spec-r1.md' if '/specs/' in r['original_path'] else 'research-r1.md')).read_bytes()
rejected_redirects=0
for mode in ['wrong-pointer','wrong-hash','wrong-path']:
 r=redirects[0];record=deepcopy(pointer(load(ROOT/r['consumer']),r['record_pointer']));ptr=r['record_pointer']
 if mode=='wrong-pointer':ptr='/unapproved'
 elif mode=='wrong-hash':record['sha256']='0'*64
 else:record['path']='wiki/specs/stem-separation.md'
 try:historical_read(r['consumer'],ptr,record)
 except AssertionError:rejected_redirects+=1
 else:raise AssertionError('Unapproved historical redirect accepted')
assert rejected_redirects==3
# Payload identity only; never run frozen consumers against changed current canonicals.
for rel in ['video-source-audit','inventory-revisions/r4-citation-crosswalk']:
 folder=B/rel
 for n,r in load(folder/'manifest.json')['files'].items():pin(folder/n,r)
sp=ROOT/'wiki/specs/video-workflows.md';rp=ROOT/'wiki/research/video-workflows.md';canonical_before={str(q):info(q) for q in [sp,rp]}
assert sp.read_bytes()==(P/'spec-r2.md').read_bytes() and rp.read_bytes()==(P/'research-r2.md').read_bytes()
for q in [sp,rp]:assert 'revision: 2\n' in q.read_text()
for r in reqs:assert f"### {r['id']} — {r['title']}\n\n**{r['strength']}/target-U.** {r['contract']}" in sp.read_text()
sys.path.insert(0,str(ROOT/'tools'))
from spec_browser import spec_rows
rows=spec_rows(sp,sp.read_text());assert len(rows)==20 and {r['id'] for r in rows}==set(rm)
assert all(x.casefold() in rp.read_text().casefold() for x in ['B017','B018','B021','B028','B029','B039','Partial Movies, Partial Tracks and Movies with Partial Tracks','all three original R4 unmatched rows','Other\nStem/Synchronization'])
counts=load(P/'counts-r2.json');assert counts==dict(requirements=20,strengths={'D12':18,'U':2},cases=34,documentary_visible_cases=12,all_target_null_U_unexecuted=True,old_requirements_retained=18,old_case_IDs_retained=28,new_requirement_IDs=2,new_case_IDs=6,adopted_audit_groups=9,historical_Video_pin_redirects=4,source_blocks_unchanged=39,completed_topics=0)
assert Counter(r['strength'] for r in reqs)==counts['strengths'] and sum(c['documentary_expected'] is not None for c in cases)==12
if not preflight:
 m=load(P/'manifest-author-r2.json');assert m['counts']==counts and set(m['files'])==set(before)-{'manifest-author-r2.json'}
 for n,r in m['files'].items():pin(P/n,r)
 assert len(m['canonical_snapshots'])==2
 for r in m['canonical_snapshots']:pin(ROOT/r['canonical'],r);pin(P/r['snapshot'],r)
links=0
for q in [sp,rp,P/'README-r2.md']:
 for target in re.findall(r'\[[^\]]*\]\(([^)\s]+)\)',q.read_text()):
  if re.match('[A-Za-z]+:',target):continue
  name,_,fragment=target.partition('#');dest=(q.parent/name).resolve() if name else q
  if preflight and dest==P/'manifest-author-r2.json':continue
  assert dest.is_file(),(q,target)
  if fragment and dest.suffix=='.md':
   slug=lambda h:re.sub(r'[^\w\- ]','',re.sub(r'<[^>]*>|[`*]','',h).lower()).replace(' ','-')
   assert fragment in {slug(h) for h in re.findall(r'^#+\s+(.+)$',dest.read_text(),re.M)},(q,target)
  links+=1
for q in [sp,rp]+[P/n for n in before if Path(n).suffix in ['.json','.md','.py','.txt']]:
 if q.suffix=='.json':load(q)
 r=subprocess.run(['git','diff','--no-index','--check','/dev/null',str(q)],capture_output=True);assert r.returncode in (0,1) and not r.stdout and not r.stderr,q
assert before=={str(q.relative_to(P)):info(q) for q in P.rglob('*') if q.is_file()}
assert external_before=={r['path']:info(ROOT/r['path']) for r in inputs} and canonical_before=={str(q):info(q) for q in [sp,rp]}
print(json.dumps(dict(status='passed-read-only-preflight' if preflight else 'passed-read-only-frozen',counts=counts,input_pins=len(inputs),source_blocks=39,original_files_and_archive_files_preserved=14,browser_exact_IDs=20,local_links=links,local_historical_Video_pin_reads=4,historical_redirect_rejection_fixtures=3,case_fixture_rejections=3,full_crosspacket_replay=False,writes=False,original_runtime_network_hardware_execution=False),indent=2))
