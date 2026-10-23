"""Read-only retained conversion audit; no old author, original code or writes."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
from copy import deepcopy
import json,runpy,sys
P=Path(__file__).resolve().parent;ROOT=P.parents[3];K=P.parent/'audio-to-midi'
assert sys.dont_write_bytecode and sys.argv[1:]==['--check'],'Only read-only --check is supported'
load=lambda p:json.loads(p.read_text())
def identity(p):
 b=p.read_bytes();return dict(bytes=len(b),sha256=sha256(b).hexdigest())
def pointer(v,p):
 for k in p.split('/')[1:]:v=v[int(k)] if isinstance(v,list) else v[k]
 return v
a=load(P/'audit.json');plan=load(P/'plan.json');inputs=load(P/'inputs.json')
watched={q for q in P.rglob('*') if q.is_file()}|{ROOT/r['path'] for r in inputs};before={str(q):identity(q) for q in watched}
assert len(inputs)==23 and len({r['path'] for r in inputs})==23 and not any(r['path'].startswith('wiki/') for r in inputs)
for r in inputs:assert identity(ROOT/r['path'])=={k:r[k] for k in ['bytes','sha256']},r['path']
assert a['source']==load(K/'source.json') and identity(ROOT/a['source']['path'])=={k:a['source'][k] for k in ['bytes','sha256']}
parse=runpy.run_path(str(P.parent/'midi-editing-source-audit/source_parser.py'))['extract'];raw=(ROOT/a['source']['path']).read_text();blocks,resources=parse(raw,'ATM')
assert a['blocks']==blocks and len(blocks)==40 and Counter(b['kind'] for b in blocks)=={'p':26,'li':6,'h1':1,'h2':5,'h3':2}
assert len(resources)==len(a['resources'])==14 and Counter(r['kind'] for r in resources)=={'image':4,'caption':4,'link':6}
for r,v in zip(resources,a['resources']):
 assert all(v[k]==x for k,x in r.items()) and v['pixels_or_destination_inspected'] is v['complete'] is False
 assert sha256(raw[v['raw_start']:raw.index('>',v['raw_start'])+1].encode()).hexdigest()==v['starttag_sha256']
for b in blocks:assert raw[b['raw_start']:b['raw_end']]==b['raw_html'] and raw.count('\n',0,b['raw_start'])+1==b['html_line']
assert a['owner_requirements']==load(K/'requirements.json') and len(a['owner_requirements'])==14
assert a['owner_cases']==load(K/'cases.json') and len(a['owner_cases'])==29 and a['owner_fixtures']==load(K/'fixtures.json')
assert all(c['target']=='U' and c['execution']=='not-run' for c in a['owner_cases'])
for key in ['assessments','proposals','common_future_prerequisites']:assert a[key]==plan[key]
def guards(v):
 assert len(v['assessments'])==40 and len(v['proposals'])==5
 for i,r in enumerate(v['assessments']):
  assert r['id']==f'ACA-A{i+1:02}' and r['block']==blocks[i]['id'] and r['source_pointer']==f'/blocks/{i}/text' and pointer(v,r['source_pointer'])==blocks[i]['text']
  for field in ['represented_requirement_refs','represented_case_refs']:
   for ref in r[field]:assert pointer(v,ref['pointer'])['id']==ref['id']
 for r in v['assessments']+v['proposals']:
  assert all(r[k] is None for k in ['documentary_expected','documentary_comparison','actual_expected','actual_comparison']) and r['target']=='U' and r['executed'] is r['complete'] is False and r['coverage_credit']==0
 for i,g in enumerate(v['proposals'],1):
  assert g['id']==f'ACA-G{i:02}' and g['new_normative_IDs']==[] and g['assessment_ids']==[r['id'] for r in v['assessments'] if g['id'] in r['open_proposal_groups']] and g['assessment_ids']
 assert 'NONEMPTY generated notes' in v['proposals'][4]['proposed_future_positive_baseline']
 assert 'Slice-only128 bound; no generic Rack/Convert note cap' in v['proposals'][1]['limits']
 assert 'independently corroborated overlimit plan' in v['proposals'][1]['proposed_minimal_delta']
 assert 'factory' in v['proposals'][2]['proposed_minimal_delta'] and 'unmodified' in v['proposals'][2]['proposed_minimal_delta']
 assert [r['id'] for r in v['assessments'][15]['represented_case_refs']]==['ATM-009','ATM-013']
 assert [r['id'] for r in v['assessments'][38]['represented_case_refs']]==['ATM-018']
 assert 'not expected recognition output' in v['common_future_prerequisites']['positive'] or 'simple enable flags' in v['common_future_prerequisites']['positive']
 assert v['summary']==dict(blocks=40,paragraphs=26,list_items=6,headings=8,resources=14,images=4,captions=4,links=6,requirements=14,cases=29,whole_context_assessments=40,proposals=5,new_normative_IDs=0,new_cases=0,actual_nonnull=0,new_documentary_nonnull=0,executed=0,coverage_credit=0,complete=0)
guards(a)
mutations=['omit-source-block','invent-actual','generic-cap','empty-preview','erase-true-resequencing','erase-true-transients','custom-proves-factory','invent-REQ']
for name in mutations:
 t=deepcopy(a)
 if name=='omit-source-block':t['assessments'].pop()
 elif name=='invent-actual':t['proposals'][0]['actual_expected']='pass'
 elif name=='generic-cap':t['proposals'][1]['limits']='All Racks and Convert commands have128note cap'
 elif name=='empty-preview':t['proposals'][4]['proposed_future_positive_baseline']='Enabled instrument flag; empty notes allowed'
 elif name=='erase-true-resequencing':t['assessments'][15]['represented_case_refs']=[]
 elif name=='erase-true-transients':t['assessments'][38]['represented_case_refs']=[]
 elif name=='custom-proves-factory':t['proposals'][2]['proposed_minimal_delta']='Any custom template proves defaults'
 else:t['proposals'][0]['new_normative_IDs']=['invented']
 try:guards(t)
 except AssertionError:pass
 else:raise AssertionError('Unsafe mutation accepted: '+name)
fb,fr=parse('<div id="chapter_content"><h1 id="r">Root</h1><p>Set 1.1.1. Keep fixed.</p><ul><li>Qualified.</li></ul><img alt="" src="unopened"><figcaption>Caption</figcaption></div>','FIX')
assert [b['kind'] for b in fb]==['h1','p','li'] and fb[1]['text']=='Set 1.1.1. Keep fixed.' and [r['kind'] for r in fr]==['image','caption']
if (P/'manifest.json').exists():
 m=load(P/'manifest.json');assert set(m['files'])=={q.name for q in P.iterdir() if q.is_file()}-{'manifest.json'} and m['summary']==a['summary']
 for n,r in m['files'].items():assert identity(P/n)==r
for q in P.iterdir():
 if q.is_file():
  b=q.read_bytes();assert b.endswith(b'\n') and all(x.rstrip(b' \t')==x for x in b.splitlines())
assert before=={str(q):identity(q) for q in watched}
print(json.dumps(dict(status='pass',sealed=(P/'manifest.json').exists(),summary=a['summary'],input_pins=23,watched_paths=len(watched),unchanged=True,rejected_mutations=mutations,parser_fixture=True,writes=False,original_native_runtime_network_candidate=False),indent=2))
