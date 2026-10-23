"""Finite Audio-to-MIDI R3 integrity checker, stdout only; no write mode.
Only pinned own pure HTML parser and four own Browser definitions execute.
No historical checker/author, vendor code, application or source examples run.
"""
from pathlib import Path
from hashlib import sha256
from copy import deepcopy
from collections import Counter
import ast,json,re,runpy,sys

P=Path(__file__).resolve().parent
ROOT=P.parents[3]
load=lambda p:json.loads(p.read_text())
def dg(p):
 b=p.read_bytes();return dict(bytes=len(b),sha256=sha256(b).hexdigest())
def pin(p,r):assert dg(p)=={k:r[k] for k in ('bytes','sha256')},p
def ptr(v,p):
 for k in p.split('/')[1:]:v=v[int(k)] if isinstance(v,list) else v[k.replace('~1','/').replace('~0','~')]
 return v
def diff(old,new):
 return [dict(json_pointer=f'/{i}/{k}',id=y['id'],old=x.get(k),new=y.get(k)) for i,(x,y) in enumerate(zip(old,new)) for k in sorted(set(x)|set(y)) if x.get(k)!=y.get(k)]

def guards(s,oldreq,oldcases,audit,blocks,selected):
 r,c,f,o,x,a,b=(s[k] for k in ('requirements','cases','fixtures','oracles','context','adoption','blocks'))
 assert b==blocks and len(b)==40 and Counter(z['kind'] for z in b)=={'p':26,'li':6,'h1':1,'h2':5,'h3':2}
 assert x['selected_blocks']==selected and len(selected)==6
 assert x['actual_expected'] is x['actual_comparison'] is None and x['target']=='U' and x['executed'] is False
 assert [q['id'] for q in r]==[q['id'] for q in oldreq] and len(r)==14
 changes=diff(oldreq,r);assert changes==a['requirement_field_delta'] and len(changes)==7
 assert {z['json_pointer'] for z in changes}=={f'/{i}/body' for i in (0,1,6,7,8)}|{f'/{i}/qualification_source_refs' for i in (7,8)}
 for i in (0,1,6,7,8):assert r[i]['body'].startswith(oldreq[i]['body']) and len(r[i]['body'])>len(oldreq[i]['body'])
 for i in (7,8):
  assert 'factory conversion history without a custom' in r[i]['body'] and 'single instrument' in r[i]['body']
  assert r[i]['qualification_source_refs']==[dict(catalog='source-context-r3.json',json_pointer=f'/selected_blocks/{j}',id=f'DEV:B{134+j}') for j in range(6)]
 assert len(c)==37 and c[:29]==oldcases and [z['id'] for z in c]==[f'ATM-{i:03}' for i in range(1,38)]
 assert all(z['target']=='U' and z['execution']=='not-run' for z in c)
 assert Counter(z['basis'] for z in c)=={'D12':25,'U':12}
 sourceids={30:[3,4,21,25,29],31:[6,9,10,11],32:[6],33:[8],34:[12],35:[18],36:[22,27],37:[27]}
 named={30:'named-command-entry-only',31:'named-dialog-role-only',35:'named-nested-placement-only',36:'named-replacement-permission-only'}
 snippets={30:['EACH route','four named commands','once through Create','once through the selected clip context menu'],31:['THREE separate reset copies','beat-resolution division','transient division','Warp Marker division','actually click OK'],32:['SAME independently corroborated valid prospective129-region','before EACH','First lower the slice resolution','Reset to the original129 plan','separately select a smaller source region'],33:['genuine nonidentity Warp','productive distinguishable nonzero','explicitly set Preserve warped timing ON','explicitly set it OFF'],34:['UNMODIFIED factory','distinct from ATM011','basic envelope, loop and crossfade','Actually change','genuinely active nondegenerate'],35:['TWO actual','multi-select','CtrlG (Win)','CmdG (Mac)','AFTER that sub-Rack','productive supported processing'],36:['EACH result','factory/no-custom','NONEMPTY generated notes','independently nonzero active instrument','existing supported replacement route'],37:['factory/no-custom','NONEMPTY generated notes','nonzero active instrument','Actually move','Synth to Piano']}
 for n in range(30,38):
  q=c[n-1];assert q['basis']=='D12' and q['expected'] is q['actual_expected'] is q['actual_comparison'] is None
  assert all(token in q['action'] for token in snippets[n]),q['id']
  assert q['source_refs']==[dict(catalog='../audio-to-midi-source-audit/audit.json',json_pointer=f'/blocks/{i-1}',id=f'ATM:B{i:03}') for i in sourceids[n]]
  assert all(k in f['recipes'] for k in q['future_prerequisites'])
  assert q['documentary_comparison']==named.get(n)
  if n in named:assert isinstance(q['documentary_expected'],str) and q['documentary_expected']
  else:assert q['documentary_expected'] is None
  assert q['source_claim'] and 'U' in q['unknown']
  req=next(v for v in r if v['id']==q['requirement']);assert q['source_anchors']==req['source_anchors']+(['convert-melody-to-new-midi-track'] if n==36 else [])
  assert q['related_requirements']==(['REQ-AUDIO-TO-MIDI-009'] if n==36 else [])
 assert f['supplied_assets'] is f['executed'] is False and f['target']=='U' and f['actual_expected'] is f['actual_comparison'] is None
 assert 'NONEMPTY generated notes' in f['recipes']['PRODUCTIVE'] and 'independently nonzero contribution' in f['recipes']['PRODUCTIVE'] and 'active nonmuted output' in f['recipes']['PRODUCTIVE']
 assert 'factory/no-custom Harmony or Melody' in f['recipes']['FACTORY-CONVERSION'] and 'old ATM015/016' in f['recipes']['FACTORY-CONVERSION'] and 'F4 input validity alone is insufficient' in f['recipes']['FACTORY-CONVERSION']
 assert 'UNMODIFIED factory' in f['recipes']['FACTORY-SLICING'] and 'custom template never proves' in f['recipes']['FACTORY-SLICING']
 assert o['old_legacy_documentary_nonnull']==17 and o['new_named_documentary']==4 and o['new_null_documentary']==4
 assert o['actual_oracles']==[dict(id=q['id'],catalog='cases-r3.json',json_pointer=f'/{i}',actual_expected=None,actual_comparison=None,target='U',execution='not-run') for i,q in enumerate(c)]
 assert o['unsupported_domains']==['recognition','numeric','timing','signal','file'] and o['supplied_assets']==o['executed_cases']==o['coverage_credit']==o['complete_topics']==0
 assert len(a['groups'])==5 and a['unchanged_case_prefix']==29 and a['old_owner_files_preserved']==20 and a['coverage_credit']==a['complete_topics']==0
 associations=[([0,1],[29,30],[0,2,8]),([],[31,32],[4,5,7]),([],[33],[10]),([6],[34],[13]),([7,8],[35,36],[14,15,16])]
 for i,(g,(rp,cp,op)) in enumerate(zip(a['groups'],associations)):
  assert g['id']==audit['proposals'][i]['id'] and g['audit_proposal_pointer']==f'/proposals/{i}'
  ids=[audit['assessments'][int(z[-2:])-1]['block'] for z in audit['proposals'][i]['assessment_ids']]
  assert g['source_contexts']==[dict(audit_pointer=f'/blocks/{int(z[-3:])-1}',id=z,quote=blocks[int(z[-3:])-1]['text']) for z in ids]
  assert g['requirement_pointers']==[f'/{j}/body' for j in rp] and g['new_case_pointers']==[f'/{j}' for j in cp] and g['retained_case_pointers']==[f'/{j}' for j in op]
  for z in cp:assert c[z]['audit_groups']==[g['id']]
  assert g['completion'] is False and g['target']=='U' and g['limits']==audit['proposals'][i]['limits']

def main():
 assert sys.dont_write_bytecode and sys.argv[1:]==['--check'],'Read-only --check only; writes refused'
 initial={str(p):dg(p) for p in P.rglob('*') if p.is_file()}
 inputs=load(P/'inputs-r3.json');watched=sorted(set([ROOT/r['path'] for r in inputs['files']]+[ROOT/'wiki/specs/audio-to-midi.md',ROOT/'wiki/research/audio-to-midi.md']))
 before={str(p):dg(p) for p in watched}
 assert len(inputs['files'])==len({r['path'] for r in inputs['files']})==33
 assert len(inputs['old_owner_files'])==20
 for r in inputs['files']+inputs['old_owner_files']:pin(ROOT/r['path'],r)
 assert dg(P/'manifest.json')['sha256']=='24e6485573f4c3c6a9c9eeeec348f604aa2fbc10961c1c84bfe885be2d3f25c3'
 assert dg(P/'manifest-author-r1.json')['sha256']=='ba18658fdfed6ff6241b4b9f943b2dbecc0e0631e2af2606d9b132233f432e0d'
 assert (P/'manifest-author-r1.json').read_bytes()==(P/'revisions/author-r1/manifest.json').read_bytes()
 # Direct finite provider checks only; never invoke old checkers or redirect Path.
 for record in load(P/'manifest-author-r1.json')['payloads']:pin(P/'revisions/author-r1'/record['path'],record)
 for record in load(P/'manifest.json')['payloads']:
  provider=inputs['historical_canonical_providers'].get(record['sha256'],record['path']);pin(ROOT/provider,record)
 audit=load(P.parent/'audio-to-midi-source-audit/audit.json')
 parse=runpy.run_path(str(P.parent/'midi-editing-source-audit/source_parser.py'))['extract']
 raw=(P/'manual-conversion-2026-10-19.html').read_text();blocks,resources=parse(raw,'ATM')
 assert blocks==audit['blocks'] and len(resources)==14
 for b in blocks:
  assert raw[b['raw_start']:b['raw_end']]==b['raw_html'] and raw.count('\n',0,b['raw_start'])+1==b['html_line']
  assert b['html_column']==b['raw_start']-(raw.rfind('\n',0,b['raw_start'])+1)
 for x,y in zip(resources,audit['resources']):
  assert all(y[k]==v for k,v in x.items()) and y['pixels_or_destination_inspected'] is False
  start=x['raw_start'];assert sha256(raw[start:raw.index('>',start)+1].encode()).hexdigest()==x['starttag_sha256']
 adjacent,unused=parse((P.parent/'racks/manual-devices-2026-10-19.html').read_text(),'DEV');assert len(adjacent)==153
 state={k:load(P/n) for k,n in [('requirements','requirements-r3.json'),('cases','cases-r3.json'),('fixtures','fixtures-r3.json'),('oracles','oracle-policy-r3.json'),('context','source-context-r3.json'),('adoption','adoption-r3.json')]};state['blocks']=deepcopy(blocks)
 assert state['context']['source']==load(P.parent/'racks/sources.json')[1]
 oldreq=load(P/'requirements.json');oldcases=load(P/'cases.json');check=lambda s:guards(s,oldreq,oldcases,audit,blocks,adjacent[133:139]);check(state)
 rejected=[]
 for name in ('omit-source','dual-wrong-source','invent-actual','numeric-comparator','erase-old-transients','no-productive-baseline','no-factory-history','custom-proves-factory','omit-recovery-reset','invent-context'):
  t=deepcopy(state)
  if name=='omit-source':t['blocks'].pop()
  elif name=='dual-wrong-source':t['cases'][30]['source_refs'][0]['id']='ATM:B012';t['cases'][30]['source_claim']='Factory macro instead of chooser'
  elif name=='invent-actual':t['cases'][29]['actual_expected']='pass'
  elif name=='numeric-comparator':t['cases'][31]['documentary_expected']='129 verified';t['cases'][31]['documentary_comparison']='numeric-equality'
  elif name=='erase-old-transients':t['cases'][17]['action']='Edit one marker before one command'
  elif name=='no-productive-baseline':t['fixtures']['recipes']['PRODUCTIVE']='Enabled flag only, empty output accepted'
  elif name=='no-factory-history':t['fixtures']['recipes']['FACTORY-CONVERSION']='F4 is enough'
  elif name=='custom-proves-factory':t['fixtures']['recipes']['FACTORY-SLICING']='Any custom template proves factory mapping'
  elif name=='omit-recovery-reset':t['cases'][31]['action']=t['cases'][31]['action'].replace('Reset to the original129 plan','Keep reduced plan')
  else:t['context']['selected_blocks'][1]['text']='Every conversion always produces a piano Rack'
  try:check(t)
  except AssertionError:rejected.append(name)
  else:raise AssertionError('Unsafe mutation accepted: '+name)
 assert len(rejected)==10
 # Exactly the four inspected pure Browser definitions; no module main/build/import.
 tree=ast.parse((ROOT/'tools/spec_browser.py').read_text());names={'anchor','frontmatter','cells','spec_rows'}
 defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names];assert len(defs)==4
 env={'re':re};exec(compile(ast.Module(body=defs,type_ignores=[]),'pinned-own-browser-defs','exec'),env)
 spec=(P/'spec-r3.md').read_text();assert spec==(ROOT/'wiki/specs/audio-to-midi.md').read_text()
 assert (P/'research-r3.md').read_text()==(ROOT/'wiki/research/audio-to-midi.md').read_text()
 assert 'revision: 3\n' in spec and 'packet R2 only' in spec
 rows=env['spec_rows'](ROOT/'wiki/specs/audio-to-midi.md',spec);assert [z['id'] for z in rows]==[r['id'] for r in state['requirements']]
 for r in state['requirements']:assert spec.count(r['body'])==1
 table=[env['cells'](line) for line in spec.splitlines() if line.startswith('| ATM-')];assert len(table)==37
 for row,c in zip(table,state['cases']):assert row[0]==c['id'] and row[3]==c['action']
 census=load(P/'consumer-census-r3.json');assert census['file_count']==len(census['files'])==7 and census['literal_pointer_count']==22
 assert census['providers']==inputs['historical_canonical_providers'] and census['current_paths_rewritten'] is census['historical_adapters_run'] is False
 for record in census['files']:
  pin(ROOT/record['path'],record);data=load(ROOT/record['path'])
  for hit in record['occurrences']:assert ptr(data,hit['json_pointer'])==hit['old_sha256'] and dg(ROOT/census['providers'][hit['old_sha256']])['sha256']==hit['old_sha256']
 fb,fr=parse('<div id="chapter_content"><h1 id="root">Root</h1><p>Choose <em>one</em> branch.</p><h2 id="child">Child</h2><ul><li>Known input only.</li></ul><figcaption>Literal caption.</figcaption></div>','FIX')
 assert [b['text'] for b in fb]==['Root','Choose one branch.','Child','Known input only.'] and fr[-1]['text']=='Literal caption.' and fb[-1]['heading_context'][-1]['anchor']=='child'
 links=0
 for path in (P/'README-r3.md',P/'spec-r3.md',P/'research-r3.md'):
  rawtext=path.read_text();parent=ROOT/'wiki/specs' if path.name=='spec-r3.md' else ROOT/'wiki/research' if path.name=='research-r3.md' else P
  for dest in re.findall(r'\]\(([^)]+)\)',rawtext):
   if re.match('[A-Za-z]+:',dest):continue
   file,sep,frag=dest.partition('#');target=(parent/file) if file else path
   assert target.is_file(),(path,dest)
   if sep and target.suffix=='.md':assert frag in {env['anchor'](line.lstrip('# ')) for line in target.read_text().splitlines() if line.startswith('#')},(path,dest)
   if sep and target.suffix=='.html':assert re.search(r'\bid=["\']'+re.escape(frag)+r'["\']',target.read_text()),dest
   links+=1
 seal=P/'manifest-author-r3.json'
 if seal.exists():
  m=load(seal);assert m['summary']==summary();expected={r['path'] for r in inputs['old_owner_files']}|{str(P/n) for n in m['files']}|{str(seal)}
  assert set(initial)==expected
  for n,r in m['files'].items():pin(P/n,r)
 for path in P.glob('*r3*'):
  if path.is_file():
   rawtext=path.read_bytes();assert rawtext.endswith(b'\n') and all(line.rstrip(b' \t')==line for line in rawtext.splitlines()),path
   if path.suffix=='.json':load(path)
 assert initial=={str(p):dg(p) for p in P.rglob('*') if p.is_file()}
 assert before=={str(p):dg(p) for p in watched}
 print(json.dumps(dict(status='pass',sealed=seal.exists(),summary=summary(),input_pins=33,old_files_preserved=20,outer_watched=len(watched),all_unchanged=True,packet_unchanged=True,rejected_mutations=rejected,parser_fixture=True,browser_IDs=14,local_links=links,writes=False,old_checkers_or_adapters=False,original_vendor_native_runtime_UI_hardware_network_candidate=False),indent=2))

def summary():return dict(requirements=14,D12_requirements=11,U_requirements=3,cases=37,D12_cases=25,U_cases=12,old_case_records_verbatim=29,requirement_field_deltas=7,changed_requirement_bodies=5,new_cases=8,new_named_documentary=4,new_null_documentary=4,actual_nonnull=0,executed=0,source_blocks=40,selected_adjacent_paragraphs=6,complete_topics=0,coverage_credit=0)
if __name__=='__main__':main()
