"""Finite read-only five-section source reconciliation; --check only.
Runs only pinned analyst HTML parser and four AST-selected pure Browser functions.
Never imports old owner scripts/main or package/vendor/application code.
"""
from pathlib import Path
from hashlib import sha256
from collections import Counter
from copy import deepcopy
import ast,json,re,runpy,sys
P=Path(__file__).resolve().parent;ROOT=P.parents[3];K=P.parent/'synthesis-instruments'
NAMES={'drift':'DF','drum-sampler':'DS','meld':'ME','operator':'OP','wavetable':'WT'}
STATUS={'R':'represented-qualified-clause-and-actual-action-subset','X':'mixed-represented-subset-and-gap-or-unresolved-context','U':'documented-outcome-or-source-context-U','M':'research-or-guidance','E':'editorial-or-structural'}
load=lambda p:json.loads(p.read_text())
def dg(p):
 b=p.read_bytes();return dict(bytes=len(b),sha256=sha256(b).hexdigest())
def pin(p,r):assert dg(p)=={k:r[k] for k in ('bytes','sha256')},p
def ptr(x,p):
 for k in p.split('/')[1:]:x=x[int(k)] if isinstance(x,list) else x[k.replace('~1','/').replace('~0','~')]
 return x
def section(b):return next(h['anchor'] for h in b['heading_context'] if h['level']==2)
def build():
 plan=load(P/'plan.json');parse=runpy.run_path(str(P.parent/'midi-editing-source-audit/source_parser.py'))['extract']
 allb,allr=parse((P.parent/'sample-instruments/manual-instruments-2026-10-19.html').read_text(),'INS');assert len(allb)==1200
 blocks=[b for b in allb if any(h['level']==2 and h['anchor'] in NAMES for h in b['heading_context'])]
 ranges=[(rows[0]['raw_start'],rows[-1]['raw_end']) for n in NAMES if (rows:=[b for b in blocks if section(b)==n])]
 resources=[r for r in allr if any(lo<=r['raw_start']<hi for lo,hi in ranges)]
 req=load(K/'requirements.json');cases=load(K/'cases.json');ri={r['id']:i for i,r in enumerate(req)};ci={c['id']:i for i,c in enumerate(cases)};counts=Counter();routes={};assess=[]
 for bi,b in enumerate(blocks):
  n=section(b);counts[n]+=1;local=f'{n}:B{counts[n]:03}'
  routes[b['id']]=dict(section=n,device=NAMES[n],old_local_locator=local,actual_paragraph_anchor=b['attributes'].get('id'),heading_context=b['heading_context'])
  q=dict(disposition='E',selected_requirements=[],proposal_groups=[],assessment='Literal actual numbered heading and ancestry retained; no source-title or count closure, selected leaf coverage or target behavior from heading presence.') if b['kind'].startswith('h') else plan['judgments'][b['id']]
  selected={f'REQ-SYN-{NAMES[n]}-{i:03}' for i in q['selected_requirements']}
  declared={r['id'] for r in req if local in r['source_blocks']};rids=sorted(selected|declared);cids=[c['id'] for c in cases if any(id in c['requirements'] for id in rids)]
  assess.append(dict(id=f'SIA-A{bi+1:03}',block=b['id'],local_locator=local,block_pointer=f'/blocks/{bi}',full_qualifier_context_pointer=f'/blocks/{bi}/text',source_text_span=[0,len(b['text'])],quote=b['text'],quote_sha256=sha256(b['text'].encode()).hexdigest(),scope='Whole source context; repeated notes group adjacent related parameter roles, not an atomic facet census or complete clause/action coverage.',disposition=STATUS[q['disposition']],assessment=q['assessment'],requirement_refs=[dict(catalog='owner_requirements',id=id,json_pointer=f'/{ri[id]}',scoped_predicate_pointer=f'/{ri[id]}/contract',association='manual selected context' if id in selected else 'exact historical citation, support limited by assessment') for id in rids],case_refs=[dict(catalog='owner_cases',id=id,json_pointer=f'/{ci[id]}',actual_action_pointer=f'/{ci[id]}/setup_and_action',association='Related finite history only; actual operations limited by assessment and quoted case, never expected/setup implies invocation.') for id in cids],proposal_groups=q['proposal_groups'],documentary_expected=None,documentary_comparison=None,actual_expected=None,actual_comparison=None,target='U',executed=False,complete=False,coverage_credit=0))
 for r in resources:r.update(role='Literal primary URL/emptyalt/caption/link labels read; repeated responsive attrs retained/hashchecked. Pixels and destinations uninspected; inline emptyalt glyph not reconstructed.',pixels_or_destination_inspected=False,target='U',complete=False)
 proposals=deepcopy(plan['proposals'])
 for g in proposals:g['assessment_ids']=[a['id'] for a in assess if g['id'] in a['proposal_groups']]
 local_index={routes[b['id']]['old_local_locator']:i for i,b in enumerate(blocks)};questions=deepcopy(plan['source_questions'])
 for q in questions:q.update(quotes=[dict(local_locator=l,id=blocks[local_index[l]]['id'],json_pointer=f'/blocks/{local_index[l]}/text',quote=blocks[local_index[l]]['text']) for l in q['blocks']],case_refs=[dict(id=id,json_pointer=f'/{ci[id]}',actual_action_pointer=f'/{ci[id]}/setup_and_action') for id in q['case_ids']],documentary_expected=None,documentary_comparison=None,actual_expected=None,actual_comparison=None,target='U',executed=False,complete=False)
 reverse={name:[dict(id=r['id'],json_pointer=f'/{catalog}/{i}',related_assessment_ids=[a['id'] for a in assess if any(x['id']==r['id'] for x in a[field])],scope='Exact asof owner record, not complete contract/case closure; all50 lifecycle probes remain U and need no primary-source association.',target='U',complete=False) for i,r in enumerate(rows)] for name,catalog,rows,field in [('requirements','owner_requirements',req,'requirement_refs'),('cases','owner_cases',cases,'case_refs')]}
 summary=dict(primary='Five selected h2 sections only; full1200 chapter parse for filtering',blocks=567,block_kinds=dict(Counter(b['kind'] for b in blocks)),per_section=dict(Counter(section(b) for b in blocks)),whole_context_judgments=567,paragraph_list_manual_judgments=500,atomic_facets=False,dispositions=dict(Counter(a['disposition'] for a in assess)),resources=112,resource_kinds=dict(Counter(r['kind'] for r in resources)),requirements=109,requirement_grades=dict(Counter(r['provenance'] for r in req)),cases=154,case_kinds=dict(Counter(c['kind'] for c in cases)),named_documentary_comparators=58,null_documentary_comparators=96,original_signal_obligations=46,original_U_lifecycle=50,proposals=37,source_questions=8,immutable_file_pins=88,old_packet_history_files=81,existing_exact_canonical_providers=2,new_normative_IDs=0,new_cases=0,new_documentary_nonnull=0,actual_nonnull=0,executed=0,coverage_credit=0,complete_topics=0)
 return dict(role='Source-only wholecontext reconciliation, not owner adoption, complete source-claim decomposition or product/topic completion.',source=load(K/'sources.json')[0],source_capture_utc='2026-10-19T20:27:58.247940+00:00',read_scope=plan['read_scope'],blocks=blocks,resources=resources,block_routes=routes,owner_requirements=req,owner_cases=cases,owner_fixtures=load(K/'stimulus-recipes.json'),owner_asof=dict(manifest='synthesis-instruments/manifest-author-r2.json',sha256='cec69e5a46c33ba04207835156704f9083931bb502740553391d6e2b387006e5',spec='synthesis-instruments/spec-r2.md',research='synthesis-instruments/research-r2.md',policy='Exact asof snapshots, not livecanonical gates. R1 partial semantic approval and R2 editorial approval retain only their actual prior scopes.'),case_scope=[dict(id=c['id'],json_pointer=f'/owner_cases/{i}',retained_kind=c['kind'],target='U',audit_actual_expected=None,audit_actual_comparison=None,executed=False) for i,c in enumerate(cases)],assessments=assess,proposals=proposals,source_questions=questions,common_future_prerequisites=plan['common_future_prerequisites'],reverse_catalogs=reverse,summary=summary)

def guards(a,plan):
 assert len(a['blocks'])==len(a['assessments'])==567 and len(a['resources'])==112
 assert Counter(section(b) for b in a['blocks'])=={'drift':95,'drum-sampler':54,'meld':96,'operator':211,'wavetable':111}
 assert Counter(b['kind'] for b in a['blocks'])=={'p':453,'li':47,'h2':5,'h3':42,'h4':20}
 assert Counter(r['kind'] for r in a['resources'])=={'image':51,'caption':50,'link':11}
 assert all(r['attributes'].get('alt')=='' for r in a['resources'] if r['kind']=='image')
 assert set(plan['judgments'])=={b['id'] for b in a['blocks'] if not b['kind'].startswith('h')}
 assert a['owner_requirements']==load(K/'requirements.json') and a['owner_cases']==load(K/'cases.json') and a['owner_fixtures']==load(K/'stimulus-recipes.json')
 ri={r['id']:i for i,r in enumerate(a['owner_requirements'])}
 for f in a['assessments']:
  b=ptr(a,f['block_pointer']);assert b['id']==f['block'] and f['source_text_span']==[0,len(b['text'])] and f['quote']==b['text']==ptr(a,f['full_qualifier_context_pointer']) and f['quote_sha256']==sha256(b['text'].encode()).hexdigest()
  assert a['block_routes'][b['id']]['old_local_locator']==f['local_locator']
  if not b['kind'].startswith('h'):
   q=plan['judgments'][b['id']];assert f['assessment']==q['assessment'] and f['disposition']==STATUS[q['disposition']] and f['proposal_groups']==q['proposal_groups']
   selected={f"REQ-SYN-{NAMES[section(b)]}-{i:03}" for i in q['selected_requirements']};declared={r['id'] for r in a['owner_requirements'] if f['local_locator'] in r['source_blocks']}
   assert {r['id'] for r in f['requirement_refs']}==selected|declared
  for r in f['requirement_refs']+f['case_refs']:
   x=ptr(a[r['catalog']],r['json_pointer']);assert x['id']==r['id'];key='actual_action_pointer' if r['catalog']=='owner_cases' else 'scoped_predicate_pointer';field='setup_and_action' if r['catalog']=='owner_cases' else 'contract';assert ptr(a[r['catalog']],r[key])==x[field]
  assert all(f[k] is None for k in ('documentary_expected','documentary_comparison','actual_expected','actual_comparison')) and f['target']=='U' and f['executed'] is f['complete'] is False and f['coverage_credit']==0
 assert len(a['proposals'])==37
 for i,g in enumerate(a['proposals']):
  assert {k:v for k,v in g.items() if k!='assessment_ids'}==plan['proposals'][i] and g['assessment_ids']==[f['id'] for f in a['assessments'] if g['id'] in f['proposal_groups']] and g['assessment_ids']
  assert all(g[k] is None for k in ('documentary_expected','documentary_comparison','actual_expected','actual_comparison')) and g['target']=='U' and g['executed'] is g['complete'] is False and not g['new_normative_IDs'] and g['coverage_credit']==0 and g['ui_only_branch_requires_audio_or_hardware'] is False
 assert a['common_future_prerequisites']==plan['common_future_prerequisites'] and 'NONEMPTY' in a['common_future_prerequisites'][2] and 'BEFORE' in a['common_future_prerequisites'][2] and 'BOTH' in a['common_future_prerequisites'][3]
 assert 'BOTH' in a['proposals'][18]['proposed_future_positive_baseline'] and 'Trigger' in a['proposals'][9]['proposed_future_positive_baseline']
 assert all(c['expected'] is c['comparison'] is None and c['target_grade']=='U' and c['executed'] is False for c in a['owner_cases'])
 for c in a['owner_cases']:
  assert c['preconditions']==['common-setup','positive-signal-guard'] and c['fixture'].startswith('stimulus-recipes.json#')
  if c['documentary_expected'] is not None:assert c['documentary_expected']==a['owner_requirements'][ri[c['requirements'][0]]]['contract']
  if c['kind']=='signal-obligation' or '-U-' in c['id']:assert c['documentary_comparator'] is None
 assert sum(c['documentary_comparator'] is not None for c in a['owner_cases'])==58
 assert len(a['case_scope'])==154
 for s in a['case_scope']:
  c=ptr(a,s['json_pointer']);assert c['id']==s['id'] and c['kind']==s['retained_kind'] and s['target']=='U' and s['audit_actual_expected'] is s['audit_actual_comparison'] is None and s['executed'] is False
 for key,cat,field in [('requirements','owner_requirements','requirement_refs'),('cases','owner_cases','case_refs')]:
  assert len(a['reverse_catalogs'][key])==len(a[cat])
  for r in a['reverse_catalogs'][key]:assert ptr(a,r['json_pointer'])['id']==r['id'] and r['related_assessment_ids']==[f['id'] for f in a['assessments'] if any(x['id']==r['id'] for x in f[field])]
 assert len(a['source_questions'])==8
 for i,q in enumerate(a['source_questions']):
  assert all(q[k]==v for k,v in plan['source_questions'][i].items())
  for r in q['quotes']:assert ptr(a,r['json_pointer'])==r['quote']
  for r in q['case_refs']:assert ptr(a['owner_cases'],r['json_pointer'])['id']==r['id'] and ptr(a['owner_cases'],r['actual_action_pointer'])==ptr(a['owner_cases'],r['json_pointer'])['setup_and_action']
  assert all(q[k] is None for k in ('documentary_expected','documentary_comparison','actual_expected','actual_comparison')) and q['target']=='U' and q['executed'] is q['complete'] is False
 # Independently finite unsafe-association rules, also applied with dual-mutated plan.
 byloc={f['local_locator']:f for f in a['assessments']}
 for loc,fragment in {'drift:B010':'does not explicitly change either Oct','drum-sampler:B017':'does not explicitly hover','drum-sampler:B022':'actually drags X/Y vertically then horizontally','meld:B005':'does not explicitly select A/B tabs or Copy to A','meld:B012':'not actual changes of all macro knobs','operator:B208':'only inspects envelope-level','wavetable:B078':'notunambiguousactualwave-selection','wavetable:B007':'not a spectral threshold','meld:B047':'no Wavetable math borrowed'}.items():assert fragment in byloc[loc]['assessment'],loc
 assert byloc['operator:B199']['disposition']==STATUS['U']
 assert 'no restart/timing law selected' in a['source_questions'][0]['question'] and 'No union/menu-count' in a['source_questions'][1]['question'] and 'do not borrow Wavetable' in a['source_questions'][2]['question']
 assert a['source_capture_utc']=='2026-10-19T20:27:58.247940+00:00' and a['summary']['atomic_facets'] is False and a['summary']['new_normative_IDs']==a['summary']['new_cases']==a['summary']['coverage_credit']==0

def main():
 assert sys.dont_write_bytecode and sys.argv[1:]==['--check'],'Read-only --check only; writes refused before input reads'
 before={str(p):dg(p) for p in P.iterdir() if p.is_file()};inp=load(P/'inputs.json');assert len(inp['files'])==88
 watched={r['path']:dg(ROOT/r['path']) for r in inp['files']}
 for r in inp['files']:pin(ROOT/r['path'],r)
 for r in inp['canonical_providers']:pin(ROOT/r['provider'],r)
 for rev,base in [(1,K),(1,K/'archive-r1'),(2,K)]:
  m=load(base/f'manifest-author-r{rev}.json')
  for r in m['payloads']:pin(base/r['file'],r)
  for r in m['external_pins']:pin(K/r['file'],r)
 for r in load(K/'sources.json'):pin(K/r['file'],r) # retained copies only, never installed path fields
 a=build();plan=load(P/'plan.json');guards(a,plan);assert a==load(P/'audit.json')
 spec=(K/'spec-r2.md').read_text()
 for r in a['owner_requirements']:
  if r['provenance']=='D12':assert f"| {r['id']} | {r['contract']} |" in spec
  else:assert f"### {r['id']} — lifecycle obligations" in spec
 # Execute four inspected pure Browser definitions, not its imports/main/build.
 tree=ast.parse((ROOT/'tools/spec_browser.py').read_text());defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in {'anchor','frontmatter','cells','spec_rows'}];assert len(defs)==4
 env={'re':re};exec(compile(ast.Module(body=defs,type_ignores=[]),'four-pure-analyst-browser-definitions','exec'),env)
 assert {r['id'] for r in env['spec_rows'](K/'spec-r2.md',spec)}=={r['id'] for r in a['owner_requirements']}
 raw=(P.parent/'sample-instruments/manual-instruments-2026-10-19.html').read_text()
 for b in a['blocks']:assert raw[b['raw_start']:b['raw_end']]==b['raw_html'] and raw.count('\n',0,b['raw_start'])+1==b['html_line'] and b['html_column']==b['raw_start']-(raw.rfind('\n',0,b['raw_start'])+1)
 for r in a['resources']:
  start=r['raw_start'];assert sha256(raw[start:raw.index('>',start)+1].encode()).hexdigest()==r['starttag_sha256'] and r['pixels_or_destination_inspected'] is False
 for n in NAMES:
  new=[b for b in a['blocks'] if section(b)==n];old=load(K/f'manual-{n}-blocks.json');assert len(new)==len(old)
  for b,o in zip(new,old):assert all(b[k]==o[k] for k in ('kind','text','html_line')) and a['block_routes'][b['id']]['old_local_locator']==o['locator']
 rejected=[]
 names=['omit-list','wrong-action-pointer','alter-old-case','signal-comparator','invent-actual','borrow-setup-Oct','borrow-enumeration-LFO','borrow-label-macro','borrow-inspection-command','erase-true-XY','borrow-symmetric-copy','grade-alias-claim','borrow-Meld-math','resolve-Loop','resolve-typecount','erase-positive','erase-both-voices','wrong-Hold-mode','drop-resource']
 for name in names:
  t=deepcopy(a);p=deepcopy(plan)
  if name=='omit-list':t['blocks'].remove(next(b for b in t['blocks'] if b['kind']=='li'))
  elif name=='wrong-action-pointer':next(f for f in t['assessments'] if f['case_refs'])['case_refs'][0]['actual_action_pointer']='/1/setup_and_action'
  elif name=='alter-old-case':t['owner_cases'][0]['setup_and_action']='Inspect only'
  elif name=='signal-comparator':next(c for c in t['owner_cases'] if c['kind']=='signal-obligation')['documentary_comparator']='Exact waveforms'
  elif name=='invent-actual':t['proposals'][0]['actual_expected']='pass'
  elif name in {'borrow-setup-Oct','borrow-enumeration-LFO','borrow-label-macro','borrow-inspection-command','erase-true-XY','borrow-symmetric-copy','grade-alias-claim','borrow-Meld-math'}:
   loc={'borrow-setup-Oct':'drift:B010','borrow-enumeration-LFO':'wavetable:B078','borrow-label-macro':'meld:B012','borrow-inspection-command':'operator:B208','erase-true-XY':'drum-sampler:B022','borrow-symmetric-copy':'meld:B005','grade-alias-claim':'wavetable:B007','borrow-Meld-math':'meld:B047'}[name]
   f=next(f for f in t['assessments'] if f['local_locator']==loc);f['assessment']='All exact source outcomes and gestures exercised';p['judgments'][f['block']]['assessment']=f['assessment']
  elif name in {'resolve-Loop','resolve-typecount'}:
   i=0 if name=='resolve-Loop' else 1;t['source_questions'][i]['question']='Resolved';p['source_questions'][i]['question']='Resolved'
  elif name=='erase-positive':t['common_future_prerequisites'][2]='Enabled flag enough';p['common_future_prerequisites'][2]='Enabled flag enough'
  elif name=='erase-both-voices':t['proposals'][18]['proposed_future_positive_baseline']='One engine flag enough';p['proposals'][18]['proposed_future_positive_baseline']='One engine flag enough'
  elif name=='wrong-Hold-mode':t['proposals'][9]['proposed_future_positive_baseline']='Gate is productive Hold';p['proposals'][9]['proposed_future_positive_baseline']='Gate is productive Hold'
  else:t['resources'].pop()
  try:guards(t,p)
  except AssertionError:rejected.append(name)
  else:raise AssertionError('Unsafe mutation accepted: '+name)
 parse=runpy.run_path(str(P.parent/'midi-editing-source-audit/source_parser.py'))['extract'];fb,fr=parse('<div id="chapter_content"><h1 id="root">Root</h1><h2 id="wavetable" data-number="31.13">Wavetable</h2><ul><li>Distinct source.</li><li>Conditional output.</li></ul><p>Use <img alt="" data-src="uninspected"> button.</p><table><tr><th>Source</th><td>Qualified.</td></tr></table><figcaption>Literal.</figcaption><h2 id="other">Other</h2><p>Excluded.</p></div>','FIX')
 assert [b['kind'] for b in fb]==['h1','h2','li','li','p','tr','h2','p'] and fb[4]['text']=='Use button.' and fb[5]['cells'][1]['text']=='Qualified.' and len(fr)==2
 links=0
 for base,text in [(K/'spec-r2.md',spec),(K/'research-r2.md',(K/'research-r2.md').read_text()),(P/'README.md',(P/'README.md').read_text())]:
  # snapshots retain original wiki-relative URLs; resolve that asof context without live byte gating.
  context=ROOT/'wiki/specs' if base.name=='spec-r2.md' else ROOT/'wiki/research' if base.name=='research-r2.md' else P
  for dest in re.findall(r'\]\(([^)]+)\)',text):
   if not re.match('[A-Za-z]+:',dest):assert (context/dest.split('#')[0]).is_file(),dest;links+=1
 seal=P/'manifest.json'
 if seal.exists():
  m=load(seal);assert m['summary']==a['summary'] and set(before)=={str(P/n) for n in m['files']}|{str(seal)}
  for n,r in m['files'].items():pin(P/n,r)
 for path in P.iterdir():
  data=path.read_bytes();assert data.endswith(b'\n') and all(line.rstrip(b' \t')==line for line in data.splitlines()),path
  if path.suffix=='.json':load(path)
 assert watched=={r['path']:dg(ROOT/r['path']) for r in inp['files']} and before=={str(p):dg(p) for p in P.iterdir() if p.is_file()}
 print(json.dumps(dict(status='pass',sealed=seal.exists(),summary=a['summary'],rejected_mutations=rejected,parser_list_table_inlineglyph_fixture=True,browser_exact_IDs=109,local_links=links,input_pins_unchanged=True,packet_unchanged=True,writes=False,old_scripts_decodes_replay_runtime_native_hardware_network_candidate=False),indent=2))
if __name__=='__main__':main()
