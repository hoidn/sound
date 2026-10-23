#!/usr/bin/env python3
"""Owned read-only selected-data check; no old scripts, bodies or original tool imports."""
import copy,hashlib,json,re
from collections import Counter
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];F='analysis/ableton-live-12.4.3/full-spec-v1/';P=F+'native-midi-effects/'
def read(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def verify(b,p):assert len(b)==p['bytes']and sha(b)==p['sha256'],p['path']
def at(v,p):
 if not p:return v
 assert p.startswith('/')
 for k in p[1:].split('/'):
  k=k.replace('~1','/').replace('~0','~');v=v[int(k)]if isinstance(v,list)else v[k]
 return v
pins=read(H/'source-pins.json')
for p in pins['pins']:verify((R/p['path']).read_bytes(),p)
p=pins['canonical_research_prefix'];data=(R/p['path']).read_bytes();verify(data[:p['bytes']],p);assert b'## Bounded native MIDI family routes' in data[p['bytes']:]
led=read(H/'route-ledger.json');verify((R/led['owner']['path']).read_bytes(),led['owner']);owner=(R/led['owner']['path']).read_text().splitlines()
for p in led['requirement_spans'].values():
 a,b=p['lines'];assert sha(('\n'.join(owner[a-1:b])+'\n').encode())==p['sha256']
reqfile=read(R/(P+'requirements-r3.json'));reqs=reqfile['requirements'];assert len(reqs)==27 and reqfile['revision']==3
for i,req in enumerate(reqs):
 a,b=led['requirement_spans'][f'{i+1:03}']['lines'];assert '\n'.join(owner[a-1:b]).split('\n',1)[1].strip()==req['contract'].strip()
for p in pins['predecessors']:
 verify((R/p['path']).read_bytes(),p);name=Path(p['path']).parent.name
 review=read(R/(F+'reviews/'+name+'-review.json'));assert review['disposition'].startswith('approved-bounded')and review['reviewed_manifest']['sha256']==p['sha256']
review=read(R/(F+'reviews/native-midi-effects-owner-r3-review.json'));assert review['disposition']=='approved-partial'and review['findings']==[]and review['scope']['cases']==176
review=read(R/(F+'reviews/native-midi-effects-source-audit-review.json'));assert review['disposition']=='approved-partial-source-audit'and review['findings']==[]
manifest=read(R/(F+'component-resolution-v1/manifest.json'))
for path,p in pins['large_data_export_identities_from_frozen_component_manifest'].items():
 assert p==next(x for x in manifest['files']if x['path']==Path(path).name)
 assert (R/path).stat().st_size==p['bytes'] # Full immutable-export hashes are predecessor evidence, not re-replayed here.
plan=read(H/'query-plan.json');ass=read(H/'processor-associations.json');native=[json.loads(l)for l in (H/'native-data.jsonl').read_text().splitlines()];calls=[json.loads(l)for l in (H/'selected-calls.jsonl').read_text().splitlines()]
assert len(native)==538 and len(calls)==212
assert Counter(x['kind']for x in native)=={'lexical-owner':165,'lexical-membership':165,'selected-alias-data':165,'RTTI-data':8,'table-prefix-data':8,'literal-store-candidate':27}
# Read only selected byte slices, not full corpus/provider content or source bodies.
handles={}
try:
 for row in native+calls:
  p=Path(row['provider']);p=p if p.is_absolute()else R/p
  if str(p)not in handles:handles[str(p)]=p.open('rb')
  f=handles[str(p)];f.seek(row['byte_offset']);raw=f.read(row['raw_bytes'])
  assert sha(raw)==row['raw_sha256']and json.loads(raw)==row['record']
finally:
 for f in handles.values():f.close()
counts=plan['census_before_materialization'];assert counts=={'lexical_owner_rows':165,'membership_rows':165,'alias_slices':165,'RTTI_rows':8,'table_rows':8,'slots':49,'distinct_slot_targets':35,'literal_store_candidates':27}
assert all(counts[k]<=plan['caps'][k]for k in counts)
names=set(plan['names']);owners={x['record']['scope_id']:x['record']for x in native if x['kind']=='lexical-owner'}
assert len(names)==8 and all(any(n in str(v['lexical_owner'])for n in names)for v in owners.values())
assert all('OMidiScaleSelector'not in str(v['lexical_owner'])for v in owners.values())
aliases={x['record']['entry']:x['record']for x in native if x['kind']=='selected-alias-data'}
for x in native:
 v=x['record']
 if x['kind']=='lexical-membership':assert v['entry']in aliases and any(p[1]in owners for p in v['candidates'])
 if x['kind']in['RTTI-data','table-prefix-data']:assert bool(re.fullmatch(r'\d+('+ '|'.join(names)+r')',v['literal_type_encoding']))
slots=[s for x in native if x['kind']=='table-prefix-data'for s in x['record']['slots']];assert len(slots)==49 and len({s['target']for s in slots})==35
for x in native:
 if x['kind']=='table-prefix-data':assert x['record']['native_table_extent']is None
callcounts=Counter(tag for x in calls for tag in x['fixed_query_groups']);assert dict(callcounts)==plan['call_query']['census_before_materialization']=={'aliases-out':83,'table_targets-out':127,'table_targets-in':2}
assert plan['call_query']['aliases-in']==0 and all(n<=512 for n in callcounts.values())
def association_scope(v):
 assert v['new_indirect_credit']==0 and v['bodies_selected']==0 and len(v['devices'])==8
 for name,d in v['devices'].items():
  assert d['processor_body_source_provider']is None and d['processor_body_source_locator']is None and d['outgoing_event_sink']is None and d['receiver_binding']=='unknown'
  table=native[d['table_record_line']-1]['record'];assert table['address_point']==d['address_point']and len(table['slots'])==d['table_prefix_slots']and d['native_table_extent']is None
  assert len(d['alias_entries'])==len(d['alias_record_lines'])
  for line,entry in zip(d['alias_record_lines'],d['alias_entries']):assert native[line-1]['record']['entry']==entry
association_scope(ass)
chain=read(H/'chain-edges.json');assert chain['new_traversal']is False and chain['new_indirect_credit']==0 and chain['runtime_route']is None and chain['grade']is None
source=read(H/'sources.json');audit=read(R/source['providers']['AUDIT']['path']);html=(R/source['manual_html']).read_text();assert len(audit['blocks'])==len(source['manual_audit_blocks'])==112
for loc in source['manual_audit_blocks']:
 b=at(audit,loc['pointer']);assert b['id']==loc['id']and sha(b['text'].encode())==loc['text_sha256'];raw=html[loc['raw_start']:loc['raw_end']];assert raw==b['raw_html']and sha(raw.encode())==loc['raw_html_sha256']
 assert b['html_line']==loc['html_line']and b['html_column']==loc['html_column']
for g in led['source_groups'].values():
 for span in g['manual_spans']:
  a,b=span['numbered_lines'];assert 3<=a<=b<=142;assert sha(''.join((R/span['path']).read_text().splitlines(keepends=True)[a-1:b]).encode())==span['sha256']
batch=read(H/'batch-inputs.json');casefile=read(R/batch['scenario_provider']['path']);cases=casefile['cases'];assert casefile['revision']==3 and len(cases)==176
verify((R/batch['scenario_provider']['path']).read_bytes(),batch['scenario_provider']);fixture=read(R/batch['current_fixture_overlay_provider']['path'])
def scenario_scope(v):
 assert len(v)==176 and len({c['id']for c in v})==176 and Counter(c['grade']for c in v)=={'D12':54,'U':122}
 for c in v:
  assert c['exact_build_grade']=='U'and c['execution']=='unexecuted'and c.get('actual_expected')is None and c.get('actual_comparison')is None
  if c['id']in {f'NME-{i:03}'for i in range(67,97)}:
   assert all(c.get(k)is None for k in ['documentary_oracle','comparator','documentary_expected','documentary_comparison','actual_expected','actual_comparison'])
scenario_scope(cases)
for nav,c in zip(batch['scenario_navigation'],cases):
 assert at(casefile,nav['pointer'])==c and nav['id']==c['id']and nav['requirement']==c['requirement']and nav['device']==c['device']
 assert nav['setup_sha256']==sha(c['setup'].encode())and nav['action_sha256']==sha(c['action'].encode())
 for ref in nav['source_references']:
  provider=R/ref['path'];target=at(read(provider),ref['pointer']);assert target['id']==ref['block_id']
 assert 'setup'not in nav and 'action'not in nav and 'documentary_oracle'not in nav
assert fixture['current_version_overlay']['applies_to']==[c['id']for c in cases]
def overlay_scope(v):
 o=v['current_version_overlay'];assert 'NONEMPTY'in o['event_positive']and 'BOTH'in o['both_events']and 'Meter/flag/preset alone is not delivery'in o['event_positive']
 assert 'UI'in o['ui_only']and 'no universal nonempty-output promise'in o['event_positive']
 assert 'All176 actual'in o['oracle']and 'null U/unexecuted'in o['oracle']
overlay_scope(fixture)
def retained_narrowings(v):
 by={c['id']:c for c in v}
 for key in ['NME-NL-L01','NME-NL-L05']:assert 'Latch off'in by[key]['setup']and 'Length enabled'in by[key]['setup']
 assert all(by[k]['documentary_oracle']is None for k in ['NME-050','NME-051'])
 assert 'unit/upper endpoint U'in by['NME-043']['setup']and 'displacement'in by['NME-064']['documentary_oracle']and 'U'in by['NME-064']['documentary_oracle']
retained_narrowings(cases)
def inventory(v):
 rows=v['rows'];assert len(rows)==len({r['id']for r in rows})==v['required_predicate_context_rows']==309
 assert v['counts_inventory_only']=={'X-route':0,'S-route':0,'no-established-route':309}and all(r['route']=='no-established-route'for r in rows)
 assert {r['requirement']for r in rows}=={f'REQ-NATIVE-MIDI-{i:03}'for i in range(1,28)}and Counter(r['owner_evidence_status']for r in rows)=={'D12':91,'U':218}
 assert set(v['unsupported_law_status'].values())=={'U'}and len(v['unsupported_law_status'])==10
 for r in rows:
  assert r['actual_expected']is None and r['actual_comparison']is None and r['executed']is False
  assert r['exact_build_status']=='U'and r['public_application_binding']=='no-established-route'and r['public_input_to_same_processor']==r['same_processor_to_outgoing_event']=='unknown'
  assert r['join']in v['join_catalog']and set(r['route_evidence'])<=source['providers'].keys()
  span=v['requirement_spans']['INPUTS'if r['observable'].startswith('Untouched/non-note')else r['requirement'][-3:]];assert r['source_span']==span['lines']
  assert v['case_catalog'][r['case_navigation']]==[c['id']for c in cases if c['requirement']==r['requirement']]
 assert Counter(r['device']for r in rows if r['requirement']=='REQ-NATIVE-MIDI-027')=={d:11 for d in ass['devices']}
inventory(led);assert len((H/'outcomes.tsv').read_text().splitlines())==310
neg=[]
def rejects(name,fn):
 try:fn()
 except (AssertionError,IndexError,KeyError,ValueError):neg.append(name)
 else:raise AssertionError('negative accepted '+name)
rejects('corrupt selected bytes',lambda:verify(b'bad',{'path':'fixture','bytes':3,'sha256':sha(b'abc')}));assert at({'a/b':[{'~x':7}]},'/a~1b/0/~0x')==7
rejects('missing selected pointer',lambda:at({'a':[]},'/a/0'))
x=copy.deepcopy(led);x['rows'].pop();rejects('omitted required predicate',lambda:inventory(x))
x=copy.deepcopy(led);x['rows'][0]['route']='S-route';rejects('alias/table promoted to law',lambda:inventory(x))
x=copy.deepcopy(led);x['rows'][0]['same_processor_to_outgoing_event']='established';rejects('output delivery inferred',lambda:inventory(x))
x=copy.deepcopy(ass);x['new_indirect_credit']=1;rejects('table prefix promoted to indirect credit',lambda:association_scope(x))
x=copy.deepcopy(ass);next(iter(x['devices'].values()))['native_table_extent']=64;rejects('prefix treated as complete table',lambda:association_scope(x))
x=copy.deepcopy(led);x['unsupported_law_status']['RandomAltCardinality']='resolved13';rejects('Alt cardinality invented',lambda:inventory(x))
x=copy.deepcopy(led);x['unsupported_law_status']['Range128vs127UnitsEndpoints']='same';rejects('Range units/enum inferred',lambda:inventory(x))
x=copy.deepcopy(led);x['unsupported_law_status']['CCSendMergeOrder']='ordered';rejects('CC order inferred',lambda:inventory(x))
x=copy.deepcopy(cases);x[0]['actual_expected']='passes';rejects('actual oracle invented',lambda:scenario_scope(x))
x=copy.deepcopy(fixture);x['current_version_overlay']['event_positive']='enabled flag';rejects('productive event premise removed',lambda:overlay_scope(x))
x=copy.deepcopy(cases);next(c for c in x if c['id']=='NME-NL-L01')['setup']='NoteOn Latch on';rejects('disabled Length automation',lambda:retained_narrowings(x))
print(json.dumps({'status':'PASS','scope':'selected DATA integrity/provenance only, no body expansion or old script/native/provider/original/model/comparator/fixture/build execution','owner_requirements':27,'current_cases':176,'documentary_case_grades':{'D12':54,'U':122},'required_predicate_context_inventory_only':309,'predicate_evidence_labels':{'D12':91,'U':218},'route_inventory_only':led['counts_inventory_only'],'native_metadata_rows':538,'selected_call_rows':212,'manual_audit_blocks':112,'pins':len(pins['pins']),'bodies_selected':0,'new_indirect_credit':0,'canonical_prefix_bytes':pins['canonical_research_prefix']['bytes'],'negative_controls_rejected':neg},indent=2))
