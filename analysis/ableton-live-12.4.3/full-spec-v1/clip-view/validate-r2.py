#!/usr/bin/env python3
"""Readonly Clip View successor source/history checks and finite semantic guard fixtures."""
import argparse
import ast
import copy
import hashlib
import importlib.util
import json
import re
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
AUDIT=HERE.parent/'clip-view-source-audit'
def load(p):return json.loads(Path(p).read_text())
def ident(p):
 raw=Path(p).read_bytes();return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def at(x,pointer):
 for k in pointer.strip('/').split('/') if pointer else []:
  k=k.replace('~1','/').replace('~0','~');x=x[int(k)] if isinstance(x,list) else x[k]
 return x

def semantic_guards(reqs,cases,routed,reused):
 r={x['id']:x for x in reqs};c={x['id']:x for x in cases};g={x['id']:x for x in routed}
 assert len(reqs)==55 and len(cases)==92
 for x in reqs:assert x['target_applicability']=='U' and x['complete'] is False
 for x in cases:
  assert x['expected'] is None and x['comparison'] is None and x['target_grade']=='U' and x['executed'] is False and x['complete'] is False,'invented actual outcome/closure'
  if x['id'] in {f'CV-{i:03}' for i in range(47,77)} and x['kind']!='control':assert x['documentary_expected'] is None and x['documentary_comparator'] is None,'new sensitive documentary outcome'
 for cid in ['CV-065','CV-066','CV-067']:
  a=c[cid]['setup_and_action'];assert 'independently confirm Follow automatically scrolls before a real editor edit' in a,'Follow flag mistaken for productive baseline'
  assert 'independently establish the paused-Follow relation' in a,'actual Follow pause missing'
 assert 'Stop alone does not assert moving scrolling while stopped' in c['CV-066']['setup_and_action'],'stopped-scroll law'
 assert 'Arrangement scrub area versus clip scrub area' in c['CV-067']['setup_and_action'],'two scrub contexts conflated'
 assert 'Options Follow versus toggle' in c['CV-065']['setup_and_action'],'two Follow control entries conflated'
 assert 'Only if progress actually observable' in c['CV-058']['setup_and_action'] and 'establish new waveform generation before requesting' in c['CV-058']['setup_and_action'],'conditional Reverse readiness missing'
 assert 'click Clip View Edit explicitly' in c['CV-059']['setup_and_action'],'editor configuration mistaken for Edit click'
 assert 'keeping cents fixed' in c['CV-060']['setup_and_action'],'pitch knob/field distinction lost'
 assert 'actually change the cents value field with the semitone amount fixed' in c['CV-061']['setup_and_action'],'separate cents control action lost'
 assert r['REQ-CLIP-VIEW-027']['contract']==load(HERE/'requirements.json')[26]['contract'],'Gain law/coverage broadened'
 assert 'no unconditional inheritance' in r['REQ-CLIP-VIEW-005']['contract'] and 'Q031' in r['REQ-CLIP-VIEW-005']['contract'],'Q031 unqualified inheritance'
 assert 'Humanize half-grid versus quarter-before/after remains Q053/U' in g['CVA-G13']['current_context'],'Humanize forced equivalence'
 assert len(reused)==1 and reused[0]['case']['row']['id']=='MXW-012' and 'nonmember control' in reused[0]['case']['row']['setup_and_action'],'existing Group Assign baseline not reused'
 for x in cases[62:]:assert 'invoke Group Assign' not in x['setup_and_action'],'duplicate local Group Assign case'
 assert 'output capture first' in c['CV-057']['setup_and_action'] and 'Missing hardware/support/capture is U' in c['CV-057']['setup_and_action'],'program absence vacuous'
 assert 'no time selection' in c['CV-073']['setup_and_action'] and all(b in c['CV-073']['setup_and_action'] for b in ['unlooped Start3 End7','Start3 LoopStart5 LoopEnd9','Start5 LoopStart3 LoopEnd9']),'ordinary crop branches/selection conflated'
 assert 'WarpMode only for supported audio' in c['CV-075']['setup_and_action'],'invented type/view default path'

def fixtures(reqs,cases,routed,reused):
 result=[]
 def reject(name,change):
  rr,cc,gg,ee=copy.deepcopy((reqs,cases,routed,reused));change(rr,cc,gg,ee)
  try:semantic_guards(rr,cc,gg,ee)
  except AssertionError:result.append({'fixture':name,'result':'rejected'});return
  raise AssertionError('unsafe mutation accepted: '+name)
 def case(cid):return next(i for i,x in enumerate(cases) if x['id']==cid)
 reject('enabled Follow replaces genuine scrolling',lambda r,c,g,e:c[case('CV-065')].update(setup_and_action=c[case('CV-065')]['setup_and_action'].replace('independently confirm Follow automatically scrolls before a real editor edit','merely set enabled flag')))
 reject('missing post-edit pause',lambda r,c,g,e:c[case('CV-067')].update(setup_and_action=c[case('CV-067')]['setup_and_action'].replace('independently establish the paused-Follow relation','assume paused')))
 reject('stopped moving-scroll inference',lambda r,c,g,e:c[case('CV-066')].update(setup_and_action=c[case('CV-066')]['setup_and_action'].replace('Stop alone does not assert moving scrolling while stopped','Require moving scrolling while stopped')))
 reject('Group Assign local duplicate',lambda r,c,g,e:c[case('CV-050')].update(setup_and_action='invoke Group Assign on selected group'))
 reject('missing actual cents-field gesture',lambda r,c,g,e:c[case('CV-061')].update(setup_and_action='Known Pitch/cents values only'))
 reject('numeric Pitch documentary outcome',lambda r,c,g,e:c[case('CV-060')].update(documentary_expected='exactfrequency'))
 reject('file Crop documentary outcome',lambda r,c,g,e:c[case('CV-073')].update(documentary_expected='exact generated bytes'))
 reject('Q031 unconditional inheritance',lambda r,c,g,e:r[4].update(contract='All new clips inherit track color'))
 reject('Humanize forced source equivalence',lambda r,c,g,e:next(x for x in g if x['id']=='CVA-G13').update(current_context='Halfgrid and quartergrid are equivalent'))
 reject('program output baseline absent',lambda r,c,g,e:c[case('CV-057')].update(setup_and_action=c[case('CV-057')]['setup_and_action'].replace('output capture first','unknown capture')))
 reject('Reverse readiness stage omitted',lambda r,c,g,e:c[case('CV-058')].update(setup_and_action=c[case('CV-058')]['setup_and_action'].replace('establish new waveform generation before requesting','assume immediate availability before')))
 reject('target actual result fabricated',lambda r,c,g,e:c[case('CV-047')].update(expected='pass'))
 semantic_guards(reqs,cases,routed,reused)
 result += [{'fixture':'genuine Follow baseline, pause and separate six resumption/control histories','result':'accepted'},{'fixture':'existing Group case reused and separate pitch fields retained','result':'accepted'},{'fixture':'source-only selected/no-selection distinction and Humanize unresolved','result':'accepted'}]
 return result

def main():
 p=argparse.ArgumentParser();p.add_argument('--check',action='store_true',required=True);p.parse_args()
 preservation=load(HERE/'preservation-r1-before-r2.json');assert len(preservation['packet_files'])==17
 for path,pin in preservation['packet_files'].items():assert ident(HERE/path)==pin,path
 for canonical,pin in preservation['canonical_before'].items():assert ident(HERE/pin['snapshot'])=={'bytes':pin['bytes'],'sha256':pin['sha256']},canonical
 oldmf=load(HERE/'manifest-author-r1.json')
 for pin in oldmf['payloads']+oldmf['external_pins']:assert ident(HERE/pin['file'])=={'bytes':pin['bytes'],'sha256':pin['sha256']}
 for rec in oldmf['canonical_snapshots']:
  assert (HERE/rec['snapshot']).read_bytes()==(HERE/preservation['canonical_before'][rec['canonical']]['snapshot']).read_bytes()
 for name in ['inputs-r2.json','consumer-inputs-r2.json']:
  for pin in load(HERE/name):assert ident(ROOT/pin['path'])=={'bytes':pin['bytes'],'sha256':pin['sha256']},pin['path']
 # Import only own pure static author module; no source parser or vendor function.
 module_spec=importlib.util.spec_from_file_location('clipview_r2_static_author',HERE/'author-r2.py');author=importlib.util.module_from_spec(module_spec);module_spec.loader.exec_module(author)
 for name,raw in author.build().items():assert (HERE/name).read_bytes()==raw,name
 for path,snapshot in [('wiki/specs/clip-view-workflows.md','spec-r2.md'),('wiki/research/clip-view-workflows.md','research-r2.md')]:assert (ROOT/path).read_bytes()==(HERE/snapshot).read_bytes(),path
 reqs=load(HERE/'requirements-r2.json');cases=load(HERE/'cases-r2.json');routed=load(HERE/'routed-proposals-r2.json');reused=load(HERE/'reused-external-cases-r2.json')
 assert len({r['id'] for r in reqs})==55 and len({c['id'] for c in cases})==92
 oldreq=load(HERE/'requirements.json');oldcases=load(HERE/'cases.json');data=load(HERE/'adoption-data-r2.json')
 assert [r['id'] for r in reqs[:54]]==[r['id'] for r in oldreq] and [c['id'] for c in cases[:62]]==[c['id'] for c in oldcases]
 for a,b in zip(oldreq,reqs):assert b['contract']==data['requirement_contract_patches'].get(a['id'],a['contract'])
 for a,b in zip(oldcases,cases):
  for key in ['id','requirements','kind','expected','comparison','target_grade','executed','source_blocks']:assert a[key]==b[key],(a['id'],key)
  assert b['setup_and_action']==data['case_action_patches'].get(a['id'],a['setup_and_action'])
  assert b['documentary_expected']==data['case_documentary_patches'].get(a['id'],a['documentary_expected'])
 assert sum(a['contract']!=b['contract'] for a,b in zip(oldreq,reqs))==6
 assert sum(a['setup_and_action']!=b['setup_and_action'] for a,b in zip(oldcases,cases))==1
 assert sum(a['documentary_expected']!=b['documentary_expected'] for a,b in zip(oldcases,cases))==2
 semantic_guards(reqs,cases,routed,reused);results=fixtures(reqs,cases,routed,reused);assert results==load(HERE/'focused-fixtures-r2.json')
 blocks=load(AUDIT/'source-blocks.json');assert len(blocks)==180
 source=load(HERE/'source.json');html=(HERE/source['file']).read_text();assert ident(HERE/source['file'])=={'bytes':source['bytes'],'sha256':source['sha256']}
 for row in load(HERE/'source-context-r2.json'):
  b=at(blocks,row['json_pointer']);assert b['id']==row['block'] and b['text']==row['quote']
  assert row['literal_element_id']==b['attributes'].get('id') and html[row['raw_start']:row['raw_end']]==b['raw_html']
  assert hashlib.sha256(b['raw_html'].encode()).hexdigest()==row['raw_html_sha256']
 for x in reqs+cases:
  for e in x['evidence']:assert at(blocks,e['json_pointer'])['id']==e['block'] and e['block'] in x['source_blocks']
 groups=load(HERE/'reconciliation-r2.json');audit_groups=load(AUDIT/'proposed-deltas.json');assert len(groups)==24 and {g['audit_group'] for g in groups}=={g['id'] for g in audit_groups}
 for g in groups:
  assert at(load(ROOT/g['audit_proposal']['catalog']),g['audit_proposal']['json_pointer'])['id']==g['audit_group']
  for ref in g['requirement_refs']+g['case_refs']:assert at(load(ROOT/ref['catalog']),ref['json_pointer'])['id']==ref['id']
  assert not g['complete'] and g['target']=='U'
 for x in reused:
  for key in ['requirement','case']:ref=x[key];assert at(load(ROOT/ref['catalog']),ref['json_pointer'])==ref['row']
 query=load(HERE.parent/'reviews/midi-utility-source-context-query.json');midi=(ROOT/query['immutable_inputs'][0]['path']).read_text()
 for rec in query['selected_MIDI_records']:assert midi[rec['raw_start']:rec['raw_end']]==rec['raw_html']
 interval=query['selected_MIDI_records'][2];assert interval['raw_start']==84834 and interval['raw_end']==85289
 assert 'When no notes are selected, the slider merely sets the interval size' in interval['text']
 # Four inspected pure Markdown parser definitions; never invoke browser build/write.
 parsed=ast.parse((ROOT/'tools/spec_browser.py').read_text());functions=[n for n in parsed.body if isinstance(n,ast.FunctionDef) and n.name in {'frontmatter','cells','anchor','spec_rows'}];assert len(functions)==4
 env={'re':re};exec(compile(ast.Module(body=functions,type_ignores=[]),'spec_browser:pure-definitions','exec'),env)
 found=env['spec_rows'](ROOT/'wiki/specs/clip-view-workflows.md',(ROOT/'wiki/specs/clip-view-workflows.md').read_text());assert len(found)==55 and {x['id'] for x in found}=={x['id'] for x in reqs}
 impact=load(HERE/'historical-consumer-routing-r2.json');assert len(impact['records'])==17
 for item in impact['records']:
  assert at(load(ROOT/item['file']),item['json_pointer'])==item['record']
  assert ident(ROOT/item['exact_before_snapshot'])==item['before_identity']
 for name in ['wiki/specs/clip-view-workflows.md','wiki/research/clip-view-workflows.md']:
  page=ROOT/name
  for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)',page.read_text()):
   if target.startswith(('https:','http:','#')):continue
   destination=(page.parent/target.split('#')[0]).resolve();assert destination.is_file(),(name,target)
   if '#' in target and destination.suffix=='.md':assert target.split('#',1)[1] in [env['anchor'](line.lstrip('#').strip()) for line in destination.read_text().splitlines() if line.startswith('#')],(name,target)
 sealed=HERE/'manifest-author-r2.json'
 if sealed.exists():
  mf=load(sealed);actual={q.relative_to(ROOT).as_posix() for q in HERE.rglob('*') if q.is_file() and q!=sealed};assert {x['path'] for x in mf['payloads']}==actual
  for pin in mf['payloads']+mf['canonicals']:assert ident(ROOT/pin['path'])=={'bytes':pin['bytes'],'sha256':pin['sha256']}
  assert mf['external_pins']==list({x['path']:x for x in load(HERE/'inputs-r2.json')+load(HERE/'consumer-inputs-r2.json')}.values())
 new=[q for q in HERE.rglob('*') if q.is_file() and q.relative_to(HERE).as_posix() not in preservation['packet_files']]
 for q in new+[ROOT/'wiki/specs/clip-view-workflows.md',ROOT/'wiki/research/clip-view-workflows.md']:
  if 'canonical-before-r2' in q.parts:continue
  if q.suffix in {'.json','.md','.py'}:
   b=q.read_bytes();assert b.endswith(b'\n') and b'\r\n' not in b and not any(line.rstrip(b' \t')!=line for line in b.splitlines()),q
 print(json.dumps({'result':'pass','mode':'readonly','sealed':sealed.exists(),'original_files':17,'input_pins':45,'historical_references':17,'requirements':55,'cases':92,'source_contexts':121,'audit_groups':24,'browser_IDs':55,'actual_nonnull':0,'executed':0,'complete':0,'negative_fixtures':12,'positive_fixtures':3}))
if __name__=='__main__':main()
