"""Finite retained-text capture/check only. Never executes decompiled/vendor text."""
from pathlib import Path
from hashlib import sha256
from copy import deepcopy
from collections import Counter
import json,re,sys,subprocess
P=Path(__file__).resolve().parent;ROOT=P.parents[3]
assert sys.dont_write_bytecode and sys.argv[1:] in (['--write'],['--check'])
checking=sys.argv[1:]==['--check'];assert checking or not (P/'manifest.json').exists(),'Sealed research packet; refuse overwrite'
def load(q):return json.loads(q.read_text())
def identity(q):
 h=sha256();size=0
 with q.open('rb') as f:
  for block in iter(lambda:f.read(1024*1024),b''):h.update(block);size+=len(block)
 return dict(bytes=size,sha256=h.hexdigest())
def path(s):return Path(s) if Path(s).is_absolute() else ROOT/s
def selected_lines(q,numbers):
 result=[];wanted=set(numbers)
 with q.open('rb') as f:
  for n,raw in enumerate(f,1):
   if n in wanted:result.append(dict(line=n,raw_line_sha256=sha256(raw).hexdigest(),raw_line_bytes=len(raw),record=json.loads(raw)))
   if n>=max(wanted):break
 assert [r['line'] for r in result]==sorted(numbers)
 return result
def pointer(x,p):
 for k in p.lstrip('/').split('/') if p else []:
  k=k.replace('~1','/').replace('~0','~');x=x[int(k)] if isinstance(x,list) else x[k]
 return x
if checking:
 initial_packet={str(q.relative_to(P)):identity(q) for q in P.rglob('*') if q.is_file()}
 initial_sources={r['path']:identity(path(r['path'])) for r in load(P/'source-pins.json')}
plan=load(P/'plan.json');C=Path(plan['corpus']);assert len(plan['functions'])==14 and len(plan['additional_trace_edges'])==2
assert plan['source_export_utc'] is None and plan['analyst_extraction_utc']
meta=load(C/'indexes/manifest.json');run=load(C/'decomp/run.json')
assert meta['program']==run['program']=='Live.arm64' and meta['executable_sha256']==run['executable_sha256']==plan['target_export_identity']
index={n:selected_lines(C/'indexes'/n,lines) for n,lines in plan['index_lines'].items()}
functions=[];chunks={}
for choice in plan['functions']:
 q=C/'decomp/chunks'/choice['chunk'];chunks[q]=identity(q)
 row=selected_lines(q,[choice['line']])[0];record=row['record'];code=record['code'];assert record['entry']==choice['entry']
 assert len(code.encode())==record['code_bytes'] and sha256(code.encode()).hexdigest()==record['code_sha256']
 kept={k:v for k,v in record.items() if k!='code'}
 item=dict(source_path=str(q),source_line=row['line'],raw_line_sha256=row['raw_line_sha256'],raw_line_bytes=row['raw_line_bytes'],metadata=kept,read_scope=choice['read_scope'],retained_code=None,excerpts=[])
 if choice['read_scope'].startswith('full'):item['retained_code']=code
 elif choice['read_scope']=='excerpt-only':
  lines=code.splitlines(True);hits=[i for i,s in enumerate(lines) if choice['needle'] in s];assert len(hits)==1
  a=max(0,hits[0]-3);z=min(len(lines),hits[0]+4);text=''.join(lines[a:z]);start=sum(map(len,lines[:a]))
  item['excerpts']=[dict(code_json_pointer='/code',line_start=a+1,line_end_inclusive=z,character_start=start,character_end_exclusive=start+len(text),text=text,text_sha256=sha256(text.encode()).hexdigest())]
 else:assert choice['read_scope']=='metadata-only'
 functions.append(item)
context=load(P/'context.json');assert (P/context['question']['snapshot']).read_text()==context['question']['text']
assert sha256(context['question']['text'].encode()).hexdigest()==context['question']['text_sha256']
sourcepaths={C/'indexes/manifest.json',C/'decomp/run.json',C/'decomp/coverage.json',C/'check-indexes.json',C/'check-decomp.json',C/'logs/full/result.json'}|set(chunks)|{C/'indexes'/n for n in [*index,'vtables.jsonl']}
for n in [*index,'vtables.jsonl']:
 assert identity(C/'indexes'/n)=={k:meta['files'][n][k] for k in ['bytes','sha256']}
for row in context['source_contexts']:
 sourcepaths.add(ROOT/row['catalog']);assert pointer(load(ROOT/row['catalog']),row['pointer'])==row['record']
 packet='settings-learning' if row['source']['id']=='D12-FIRST-STEPS' else 'clip-view'
 q=P.parent/packet/row['source']['file'];assert identity(q)=={k:row['source'][k] for k in ['bytes','sha256']};sourcepaths.add(q);sourcepaths.add(P.parent/packet/'source.json')
for owner in context['owners']:
 for field in ['requirement','case']:
  q=ROOT/owner[field+'_catalog'];assert pointer(load(q),owner[field+'_pointer'])==owner[field];sourcepaths.add(q)
 sourcepaths.add(ROOT/owner['immutable_spec'])
sourcepaths|={ROOT/context['retained_non_adoption']['path'],P.parent/'settings-owner-reconciliation/manifest.json',P.parent/'reviews/settings-owner-reconciliation-review.json'}
pins=[dict(path=str(q) if not q.is_relative_to(ROOT) else str(q.relative_to(ROOT)),**identity(q)) for q in sorted(sourcepaths)]
assert not any(r['path'].startswith('wiki/') for r in pins)
vtable=(C/'indexes/vtables.jsonl').read_text();assert len(vtable.splitlines())==80
assert not any(n in vtable for n in plan['negative_queries'][1]['needles'])
assert index['strings.jsonl'][7]['record']['refs']==index['strings.jsonl'][8]['record']['refs']==[]
for edge in plan['additional_trace_edges']:
 record=next(r['record'] for r in index['calls.jsonl'] if r['line']==edge['index_line'])
 assert record['caller']==edge['caller'] and record['callee']==edge['callee']
ledger=load(P/'trace-ledger.json')
def verify(fns,claims):
 assert [x['metadata']['entry'] for x in fns]==[x['entry'] for x in plan['functions']]
 assert len(claims)==9 and len({x['id'] for x in claims})==9
 assert sum(x['read_scope'].startswith('full') for x in fns)==10 and sum(x['read_scope']=='excerpt-only' for x in fns)==3
 assert fns[13]['read_scope']=='metadata-only' and fns[13]['retained_code'] is None and not fns[13]['excerpts'] and fns[13]['metadata']['code_bytes']==100894
 assert fns[0]['metadata']['warnings'] and fns[7]['metadata']['warnings'] and fns[13]['metadata']['warnings']
 docs={'functions.json':fns,'index-records.json':index,'context.json':context,'plan.json':plan}
 for c in claims:
  assert c['private_research_only'] and c['normative_credit']==0 and c['actual_expected'] is c['actual_comparison'] is None and c['target_grade']=='U' and c['executed'] is False
  for ref in c['evidence']:
   name,_,ptr=ref.partition('#');pointer(docs[name],ptr)
verify(functions,ledger);rejected=0
for mode in ['omitted-body-record','bad-pointer','promoted-metadata','discarded-warning']:
 f=deepcopy(functions);cs=deepcopy(ledger)
 if mode=='omitted-body-record':f.pop(5)
 elif mode=='bad-pointer':cs[0]['evidence']=['functions.json#/9999']
 elif mode=='promoted-metadata':cs[-1]['normative_credit']=1
 else:f[0]['metadata']['warnings']=[]
 try:verify(f,cs)
 except (AssertionError,IndexError,KeyError):rejected+=1
 else:raise AssertionError(mode)
assert rejected==4
summary=dict(status='inconclusive-research-navigation-only',question='Q-031 remains open',target_identity='Retained export metadata Live.arm64 SHA '+plan['target_export_identity']+'; no original binary reread',selected_decomp_records=14,full_small_bodies_read=10,incidental_unlinked_full_bodies=3,registration_excerpt_only=3,large_RTTI_body_metadata_only=1,large_body_full_read=False,additional_followed_call_edges=2,index_record_counts={n:len(v) for n,v in index.items()},corpus_parent_files_pinned=len([r for r in pins if Path(r['path']).is_absolute()]),source_pins=len(pins),source_export_utc=None,analyst_extraction_utc=plan['analyst_extraction_utc'],read_scope='Retained selected text/metadata and two documentary source contexts only, not a whole callgraph, type/vtable or clip-creation trace',private_binding_lead=True,actual_preference_to_newclip_boundary_established=False,new_normative_requirements=0,new_cases=0,U_case_credit=0,completed_topics=0,behavioral_coverage_credit=0,actual_results_null_U_unexecuted=True,rejection_fixtures=4,original_function_native_REA_export_runtime_network_candidate_execution=False)
outputs={'functions.json':functions,'index-records.json':index,'source-pins.json':pins,'summary.json':summary}
if checking:
 before={str(q.relative_to(P)):identity(q) for q in P.rglob('*') if q.is_file()};external={r['path']:identity(path(r['path'])) for r in pins}
 for name,value in outputs.items():assert load(P/name)==value,name
 manifest=load(P/'manifest.json');assert set(manifest['files'])==set(before)-{'manifest.json'}
 for name,r in manifest['files'].items():assert identity(P/name)==r
 for q in P.iterdir():
  if q.suffix in ['.md','.json','.py']:
   r=subprocess.run(['git','diff','--no-index','--check','/dev/null',str(q)],capture_output=True);assert r.returncode in (0,1) and not r.stdout and not r.stderr,q
 for ref in re.findall(r'\]\(([^)]+)\)',(P/'README.md').read_text()):assert (P/ref.partition('#')[0]).is_file(),ref
 assert before=={str(q.relative_to(P)):identity(q) for q in P.rglob('*') if q.is_file()} and external=={r['path']:identity(path(r['path'])) for r in pins}
 assert initial_packet==before and initial_sources==external
 print(json.dumps(dict(status='passed-read-only-frozen',summary=summary,writes=False),indent=2))
else:
 for name,value in outputs.items():
  q=P/name;assert not q.exists();q.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(summary,indent=2))
