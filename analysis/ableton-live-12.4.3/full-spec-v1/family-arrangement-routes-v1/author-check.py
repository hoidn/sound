#!/usr/bin/env python3
"""Owned read-only selected-data check; no old scripts, source parser or runtime imports."""
import copy,hashlib,json,re
from collections import Counter
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];F='analysis/ableton-live-12.4.3/full-spec-v1/'
def read(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def verify(b,p):assert len(b)==p['bytes'] and sha(b)==p['sha256'],p['path']
def at(v,p):
 if not p:return v
 assert p.startswith('/')
 for k in p[1:].split('/'):
  k=k.replace('~1','/').replace('~0','~');v=v[int(k)]if isinstance(v,list)else v[k]
 return v
pins=read(H/'source-pins.json')
for p in pins['pins']:verify((R/p['path']).read_bytes(),p)
p=pins['canonical_research_prefix'];b=(R/p['path']).read_bytes();verify(b[:p['bytes']],p);assert b'## Bounded Arrangement route inventory' in b[p['bytes']:]
led=read(H/'route-ledger.json');verify((R/led['owner']['path']).read_bytes(),led['owner'])
owner=(R/led['owner']['path']).read_text().splitlines()
for p in list(led['requirement_spans'].values())+list(led['owner_clause_spans'].values()):
 a,b=p['lines'];assert sha(('\n'.join(owner[a-1:b])+'\n').encode())==p['sha256']
reqs=read(R/(F+'arrangement/requirements-r2.json'));assert len(reqs)==42
for i,r in enumerate(reqs):
 a,b=led['requirement_spans'][f'{i+1:03}']['lines'];current='\n'.join(owner[a-1:b]);assert current.split('\n',1)[1].strip()==r['contract'].strip()
 assert r['target']=='U' and r['complete']is False
for p in led['predecessors']:
 verify((R/p['path']).read_bytes(),p);name=Path(p['path']).parent.name
 review=read(R/(F+'reviews/'+name+'-review.json'));assert review['disposition'].startswith('approved-bounded-')and review['reviewed_manifest']['sha256']==p['sha256']
review=read(R/(F+'reviews/arrangement-editing-owner-r3-review.json'));assert review['disposition']=='approved-partial-owner-successor'and review['required_findings']==[]
assert review['checks']['documentary_named']==43 and review['checks']['documentary_null']==41
areview=read(R/(F+'reviews/arrangement-source-audit-review-final.json'));assert areview['disposition']=='approved-partial-source-audit-after-focused-correction' and areview['required_findings']==[]
sources=read(H/'sources.json')['records'];blocks=read(R/(F+'arrangement-source-audit/source-blocks.json'));blockcount=0
for sid,s in sources.items():
 p=R/s['path'];assert p.exists()
 if s['kind']=='manual-block-locator':
  blockcount+=1;v=at(blocks,s['pointer']);assert v['id']==sid==s['block_id'] and sha(v['text'].encode())==s['text_sha256']
  html=(R/s['html_path']).read_text();raw=html[s['raw_start']:s['raw_end']]
  assert raw==v['raw_html'] and sha(raw.encode())==s['raw_html_sha256']
  assert s['version']==v['source_version'] and s['target_parity']=='U'
  assert s['html_line']==v['html_line'] and s['html_column']==v['html_column']
 elif s['kind']=='retained-original-jsonl-record':
  raw=p.read_bytes()[s['byte_offset']:s['byte_offset']+s['raw_bytes']];assert sha(raw)==s['raw_sha256'] and p.read_bytes().splitlines(keepends=True)[s['line']-1]==raw
  rec=at(json.loads(raw),s['pointer']);assert rec['entry']==s['entry']and sha(rec['code'].encode())==s['code_sha256']and rec['warnings']==s['warnings']
  assert s['C_lines']==[1,len(rec['code'].splitlines())]and s['native_call_PC']is None
 elif s['kind']=='retained-original-json-record':
  rec=at(read(p),s['pointer']);assert rec['entry']==s['entry']and sha(rec['code'].encode())==s['code_sha256']and rec['warnings']==s['warnings']
  assert s['C_lines']==[1,len(rec['code'].splitlines())]and s['native_call_PC']is None
 elif s.get('pointer'):
  at(read(p),s['pointer'])
assert blockcount==139 and len(sources)==155
for i,req in enumerate(reqs):
 g=led['documentary_source_groups'][req['id']];assert g['pointer']=='/'+str(i)
 assert g['source_blocks']==[c['block']for c in req['source_context']]
 assert all(s in sources for s in g['source_blocks'])
assert sum(len(g['source_blocks'])for g in led['documentary_source_groups'].values())==228
chain=read(H/'chain-edges.json');original=read(R/(F+'integration-structure-v1/document-component-edges.json'))['edges']
assert len(chain['inherited_document_edges'])==8 and chain['new_traversals']==chain['new_indirect_resolution_credit']==0
for e in chain['inherited_document_edges']:
 x=dict(e);x.pop('qualification');assert x==next(v for v in original if v['id']==e['id']);assert e['runtime_sequence_proved']is False
code=at(read(R/sources['REGISTRY']['path']),'/record/code').splitlines()
for row in chain['registry_nominations']:
 line=code[row['C_line']-1];assert sha(line.encode())==row['text_sha256']and '"'+row['command']+'"'in line
assert len(chain['unknown_bridges'])==6 and chain['runtime_route']is None
batch=read(H/'batch-inputs.json');cases=read(R/batch['cases_provider']['path']);verify((R/batch['cases_provider']['path']).read_bytes(),batch['cases_provider'])
assert len(cases)==84 and len(batch['scenario_navigation'])==84 and batch['execution_selected']is False
corrected=set(batch['corrected_numeric_cases']);assert corrected=={'AR-010','AR-016','AR-017','AR-024','AR-025','AR-026','AR-027','AR-028','AR-029'}
def scenario_scope(v):
 assert len(v)==84 and len({c['id']for c in v})==84
 assert sum(c['documentary_expected']is not None for c in v)==43
 assert sum(c['documentary_expected']is None for c in v)==41
 for c in v:
  assert c['expected']is None and c['comparison']is None and c['actual_expected']is None and c['actual_comparison']is None
  assert c['target']=='U'and c['executed']is False and c['complete']is False
  assert (c['documentary_expected']is None)==(c['documentary_comparator']is None)
  if c['id']in corrected:assert c['documentary_expected']is None and c['documentary_comparator']is None
scenario_scope(cases)
for nav,c in zip(batch['scenario_navigation'],cases):
 assert at(cases,nav['pointer'])==c and nav['id']==c['id'] and nav['requirements']==c['requirements']and nav['preconditions']==c['preconditions']
 assert nav['action_sha256']==sha(c['setup_and_action'].encode())
 assert nav['documentary_pair']==('named'if c['documentary_expected']is not None else'null')
 assert 'setup_and_action' not in nav and 'documentary_expected' not in nav
# Retained productive cases carry prerequisite phrases; checking them never executes a fixture.
def premises(v):
 by={c['id']:c['setup_and_action']for c in v}
 assert all(x in by['AR-023']for x in ['actually playing nonzero','active nonzero track effect','nonmuted'])
 assert all(x in by['AR-055']for x in ['Before this negative','same-start','successful simultaneous'])
 assert all(x in by['AR-056']for x in ['actually moving playhead','genuine automatic Arrangement scrolling','actual paused Follow','Stop alone never'])
 assert all(x in by['AR-064']for x in ['successful concrete edits','admitted valid save/reopen baseline'])
 assert all(x in by['AR-065']for x in ['genuinely active admitted','mere eligibility is insufficient'])
premises(cases)
package=read(R/sources['PACKAGE']['path']);clips=package['demo']['main_lane_clips'];assert len(clips)==64 and Counter(c['type']for c in clips)=={'MidiClip':55,'AudioClip':9}
assert len(package['demo']['locators'])==9 and package['demo']['linked_track_groups']==[]
for typ,branch in [('MidiClip','ClipTimeable'),('AudioClip','Sample')]:assert all('/MainSequencer/'+branch+'/ArrangerAutomation/Events/'in c['xpath']for c in clips if c['type']==typ)
for cls in ['AudioClip','MidiClip','ClipFades','Locator','LinkedTrackGroup']:assert cls in package['schema']['classes']
def inventory(v):
 rows=v['rows'];assert len(rows)==len({r['id']for r in rows})==v['required_predicate_context_rows']==345
 assert {r['requirement']for r in rows}=={f'REQ-ARRANGEMENT-{i:03}'for i in range(1,43)}
 routes={k:Counter(r['route']for r in rows)[k]for k in ['X-route','S-route','no-established-route']}
 assert routes==v['counts_inventory_only']=={'X-route':0,'S-route':6,'no-established-route':339}
 assert Counter(r['owner_evidence_status']for r in rows)=={'D-manual':181,'U':158,'D-package':6}
 for r in rows:
  assert r['route_evidence']and set(r['route_evidence'])<=sources.keys()
  assert r['public_application_binding']=='no-established-route'and r['actual_expected']is None and r['actual_comparison']is None and r['executed']is False
  assert r['missing_join']in v['join_catalog'] and r['documentary_source_group']in v['documentary_source_groups']
  assert r['case_navigation']==r['requirement']
  expected=[c['id']for c in cases if r['requirement']in c['requirements']];assert v['case_catalog'][r['case_navigation']]==expected
  assert r['batch_selector']in{b['id']for b in batch['prospective_static_selectors']}
  if r['owner_evidence_status']=='D-manual':assert r['exact_target_status']=='U'and r['route']=='no-established-route'
  if r['route']=='S-route':assert r['requirement']=='REQ-ARRANGEMENT-031'and r['route_evidence']==['PACKAGE']
  if r['context'].startswith('Timing/state'):assert r['owner_span']==v['owner_clause_spans']['TIMING']['lines']
  else:assert r['owner_span']==v['requirement_spans'][r['requirement'][-3:]]['lines']
 assert 'REQ033'in v['context_limits']['repeated_owner_references']
inventory(led)
assert len((H/'outcomes.tsv').read_text().splitlines())==346
negative=[]
def rejects(name,fn):
 try:fn()
 except (AssertionError,IndexError,KeyError,ValueError):negative.append(name)
 else:raise AssertionError('negative accepted '+name)
rejects('corrupt retained bytes',lambda:verify(b'bad',{'path':'fixture','bytes':3,'sha256':sha(b'abc')}))
assert at({'a/b':[{'~k':1}]},'/a~1b/0/~0k')==1
rejects('missing provider pointer',lambda:at({'a':[]},'/a/0'))
x=copy.deepcopy(led);x['rows'].pop();rejects('omitted required predicate',lambda:inventory(x))
x=copy.deepcopy(led);x['rows'][0]['exact_target_status']='S';rejects('D12 promoted to target proof',lambda:inventory(x))
x=copy.deepcopy(led);x['rows'][0]['route']='X-route';rejects('auxiliary numerical leaf promoted',lambda:inventory(x))
x=copy.deepcopy(led);x['rows'][0]['public_application_binding']='established';rejects('generic edge promoted to public edit',lambda:inventory(x))
x=copy.deepcopy(cases);next(c for c in x if c['id']=='AR-025')['documentary_expected']='duration is exact';rejects('ARR-R2-REVIEW001 numeric pair restored',lambda:scenario_scope(x))
x=copy.deepcopy(cases);x[0]['actual_expected']='passes';rejects('actual oracle invented',lambda:scenario_scope(x))
x=copy.deepcopy(cases);next(c for c in x if c['id']=='AR-023')['setup_and_action']='effect enabled';rejects('productive processing replaced by flag',lambda:premises(x))
x=copy.deepcopy(cases);next(c for c in x if c['id']=='AR-055')['setup_and_action']='different-start fade only';rejects('same-start positive baseline removed',lambda:premises(x))
x=copy.deepcopy(cases);next(c for c in x if c['id']=='AR-056')['setup_and_action']='Follow flag on';rejects('moving Follow baseline removed',lambda:premises(x))
print(json.dumps({'status':'PASS','scope':'selected data and documentary/native provenance only; no old scripts or original/provider/native/decoder/harness/model/comparator/fixture execution','required_predicate_context_inventory_only':345,'routes_inventory_only':led['counts_inventory_only'],'owner_requirements':42,'owner_clause_spans':len(led['owner_clause_spans']),'scenario_navigation':84,'documentary_named':43,'documentary_null':41,'manual_source_blocks':139,'source_context_occurrences':228,'sources':155,'pins':len(pins['pins']),'inherited_document_edges':8,'new_traversals_or_indirect_credit':0,'canonical_prefix_bytes':pins['canonical_research_prefix']['bytes'],'negative_controls_rejected':negative,'actual_oracles_or_grades':0},indent=2))
