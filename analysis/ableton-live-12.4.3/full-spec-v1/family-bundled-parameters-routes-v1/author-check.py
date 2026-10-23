#!/usr/bin/env python3
"""Read selected retained bytes and packet claims only. No study/tool imports or execution."""
import copy,csv,hashlib,json
from collections import Counter
from pathlib import Path
H=Path(__file__).resolve().parent; R=H.parents[3]
F='analysis/ableton-live-12.4.3/full-spec-v1/'
def read(p): return json.loads(p.read_text())
def sha(b): return hashlib.sha256(b).hexdigest()
def verify(b,p): assert len(b)==p['bytes'] and sha(b)==p['sha256'],p['path']
def at(v,p):
 for k in p.split('/')[1:]:
  k=k.replace('~1','/').replace('~0','~');v=v[int(k)] if isinstance(v,list) else v[k]
 return v
pins=read(H/'source-pins.json')
for p in pins['pins']: verify((R/p['path']).read_bytes(),p)
p=pins['canonical_research_prefix'];b=(R/p['path']).read_bytes();verify(b[:p['bytes']],p)
assert b'## Bounded bundled-parameter route inventory' in b[p['bytes']:]
led=read(H/'route-ledger.json');owner=(R/led['owner']['path']).read_text().splitlines()
verify((R/led['owner']['path']).read_bytes(),led['owner'])
for p in list(led['owner_clauses'].values())+list(led['assumption_spans'].values()):
 a,b=p['lines'];assert sha(('\n'.join(owner[a-1:b])+'\n').encode())==p['sha256_of_text']
for tag,p in led['assumption_spans'].items():assert owner[p['lines'][0]-1].startswith('| '+tag+' |')
for p,name in zip(led['predecessors'],['component-resolution-v1','integration-structure-v1','family-electric-routes-v1']):
 verify((R/p['path']).read_bytes(),p)
 review=read(R/(F+'reviews/'+name+'-review.json'));assert review['disposition'].startswith('approved-bounded-');assert review['reviewed_manifest']['sha256']==p['sha256']
sources=read(H/'sources.json')['records']
for key,s in sources.items():
 p=R/s['path'];assert p.exists()
 if s['kind']=='original-jsonl-record':
  raw=p.read_bytes()[s['byte_offset']:s['byte_offset']+s['raw_bytes']]
  assert sha(raw)==s['raw_sha256'];assert p.read_bytes().splitlines(keepends=True)[s['line']-1]==raw
  rec=at(json.loads(raw),s['pointer']);assert rec['entry']==s['entry']
  assert sha(rec['code'].encode())==s['code_sha256'] and s['warnings']==rec.get('warnings',[])
  assert s['C_lines']==[1,len(rec['code'].splitlines())]
 elif s['kind']=='retained-C-companion':
  assert sha(p.read_bytes())==s['code_sha256'];assert s['C_lines']==[1,len(p.read_bytes().splitlines())]
  assert read(R/s['dossier'])['entry']==s['entry']
 elif s['kind']=='original-json-record':
  rec=at(read(p),s['pointer']);assert rec['entry']==s['entry'];assert sha(rec['code'].encode())==s['code_sha256']
 elif s['kind']=='carried-review-interpretation':assert s['original_record_locator'] is None and s['native_call_PC'] is None
 if s.get('selector','').startswith('/'):at(read(p),s['selector'])
assert len(sources)==60
batch=read(H/'batch-inputs.json');casefile=read(R/batch['release_cases_path']);cases=casefile['cases']
assert len(cases)==82
for i,c in enumerate(batch['release_case_navigation']):
 original=at(casefile,c['pointer']);assert c['id']==original['id'] and c['device']==original['device']
 assert c['requirements']==original['requirements'] and c['input']['path']=='handoff/bundled-device-parameters-v1/'+original['input']
 verify((R/c['input']['path']).read_bytes(),c['input']);assert c['reference_execution']=='not-run'
 assert 'expected' not in c
sel=batch['metadata_selector'];tab=list(csv.DictReader((R/sel['path']).read_text().splitlines(),delimiter='\t'))
assert len(tab)==sel['rows']==502 and dict(Counter(t['device'] for t in tab))==sel['devices']
assert len({(t['device'],t['path']) for t in tab})==502
positions={d+'/'+p for d,paths in batch['excluded_position_paths'].items() for p in paths};assert len(positions)==9
# These release guards inspect existing metadata only, never execute/import a comparator.
def release_scope_check(case_list):
 for c in case_list:
  state=c.get('expected',{}).get('state',{});labels=c.get('expected',{}).get('labels',{})
  assert all(c['device']+'/'+p not in positions for p in state),'excluded position value judged'
  assert not (c['device']=='Cabinet' and 'MicrophoneTypeSwitch' in labels),'excluded switch label judged'
release_scope_check(cases)
expected_u={'BP056', 'BP065', 'BP009', 'BP082', 'BP121', 'BP122', 'BP005', 'BP016', 'BP097', 'BP073', 'BP066', 'BP057', 'BP083', 'BP102', 'BP108', 'BP071', 'BP107', 'BP017', 'BP080', 'BP069', 'BP130', 'BP075', 'BP125', 'BP126', 'BP124', 'BP003', 'BP129', 'BP052', 'BP096', 'BP072', 'BP123', 'BP007', 'BP098', 'BP081', 'BP120', 'BP074', 'BP070'}
def ledger_check(v):
 rows=v['rows']; ids={r['id'] for r in rows}
 assert len(rows)==len(ids)==v['required_outcomes_enumerated']==135
 assert {r['requirement'] for r in rows}=={f'REQ-BUNDLED-DEVICE-PARAMETERS-{n:03}' for n in range(1,16)}
 assert dict(Counter(r['route'] for r in rows))==v['counts_inventory_only']=={'S-route':120,'X-route':1,'no-established-route':14}
 assert {r['id'] for r in rows if r['owner_evidence_status']=='U'}==expected_u
 for r in rows:
  assert r['source_span']==v['owner_clauses'][r['source_clause']]['lines']
  assert r['public_application_binding']=='no-established-route'
  assert r['route_evidence'] and set(r['route_evidence'])<=sources.keys()
  assert r['missing_join'] in v['join_catalog']
  assert set(r['assumptions'])<=v['assumption_spans'].keys()
  assert r['case_links_are_requirement_navigation_only']
  assert r['existing_release_case_links']['requirement']==r['requirement']
  assert v['existing_release_case_catalog'][r['requirement']]==[c['id'] for c in cases if r['requirement'] in c['requirements']]
  if 'alias_of'in r:assert r['alias_of'] in ids and r['alias_of']!=r['id']
 x=[r for r in rows if r['route']=='X-route'];assert len(x)==1 and x[0]['route_evidence']==['ELvoices','ELmap'] and x[0]['missing_join']=='Jlocal'
 assert set(v['owner_clauses'])==set(v['clause_dispositions'])
 assert {r['source_clause'] for r in rows}==set(v['owner_clauses'])-{'014.7','TABLES'}
 assert all(r['owner_evidence_status']=='U' for r in rows if r['route']=='no-established-route')
ledger_check(led)
voices=at(read(R/sources['ELvoices']['path']),'/voices/limit');assert set(voices)=={str(i)for i in range(31)}
assert all(v['voice_limit_is_p_plus_2'] is True for v in voices.values())
assert len((H/'clauses.tsv').read_text().splitlines())==136
# Meaningful negative fixtures must actually fail the same guards used above.
negative=[]
def rejects(name,fn):
 try:fn()
 except (AssertionError,IndexError,KeyError,ValueError):negative.append(name)
 else:raise AssertionError('negative fixture accepted: '+name)
rejects('changed selected bytes',lambda:verify(b'bad',{'path':'fixture','bytes':3,'sha256':sha(b'abc')}))
assert at({'a/b':[{'~key':7}]},'/a~1b/0/~0key')==7
rejects('missing source selector',lambda:at({'voices':{}},'/voices/limit'))
x=copy.deepcopy(led);x['rows'].pop();rejects('omitted required outcome',lambda:ledger_check(x))
x=copy.deepcopy(led);x['rows'][1]['id']=x['rows'][0]['id'];rejects('duplicate outcome',lambda:ledger_check(x))
x=copy.deepcopy(led);x['rows'][0]['public_application_binding']='established';rejects('helper promoted to public binding',lambda:ledger_check(x))
x=copy.deepcopy(led);next(r for r in x['rows']if r['owner_evidence_status']=='U')['owner_evidence_status']='S';rejects('U promoted by investigative route',lambda:ledger_check(x))
x=copy.deepcopy(led);x['rows'][0]['source_span']=[1,1];rejects('wrong owner span',lambda:ledger_check(x))
x=copy.deepcopy(cases);x[0]['device']='Corpus';x[0]['expected']['state']['ExcitationX']=0.5;rejects('excluded position value judged',lambda:release_scope_check(x))
x=copy.deepcopy(cases);x[0]['device']='Cabinet';x[0]['expected']['labels']['MicrophoneTypeSwitch']='Dynamic';rejects('excluded Cabinet switch label judged',lambda:release_scope_check(x))
print(json.dumps({'status':'PASS','checks':'selected pins,53owner spans/A1A2A3,60source locators,82case pointers/input identities,502metadata keys,31historical voice selectors,release exclusions,prefix preserved','required_outcomes_inventory_only':135,'counts_inventory_only':led['counts_inventory_only'],'U_rows_preserved':len(expected_u),'negative_fixtures_rejected':negative,'original_provider_decoder_harness_model_comparator_calls':0,'canonical_prefix_bytes':pins['canonical_research_prefix']['bytes']},indent=2))
