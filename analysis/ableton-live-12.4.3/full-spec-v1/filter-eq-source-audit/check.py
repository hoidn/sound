"""Read-only finite four-section Filter/EQ source audit; --check only.
Only pinned own pure HTML parser executes. Old captures/authors/validators,
package code/examples and installed originals never execute or decode.
"""
from pathlib import Path
from hashlib import sha256
from collections import Counter
from copy import deepcopy
import json,re,runpy,sys
P=Path(__file__).resolve().parent;ROOT=P.parents[3];K=P.parent/'filter-eq'
NAMES={'auto-filter':'AF','channel-eq':'CEQ','eq-eight':'EQ8','eq-three':'EQ3'}
load=lambda p:json.loads(p.read_text())
def dg(p):
 b=p.read_bytes();return dict(bytes=len(b),sha256=sha256(b).hexdigest())
def pin(p,r):assert dg(p)=={k:r[k] for k in ('bytes','sha256')},p
def ptr(v,p):
 for k in p.split('/')[1:]:v=v[int(k)] if isinstance(v,list) else v[k.replace('~1','/').replace('~0','~')]
 return v
def section(b):return next(h['anchor'] for h in b['heading_context'] if h['level']==2)
STATUS=dict(R='represented-qualified-clause-and-actual-action-subset',X='mixed-represented-subset-and-gap-or-unresolved-context',U='documented-outcome-or-source-context-U',M='research-or-guidance',E='editorial-or-structural')
def build():
 plan=load(P/'plan.json');parse=runpy.run_path(str(P.parent/'midi-editing-source-audit/source_parser.py'))['extract']
 allblocks,allresources=parse((P.parent/'audio-utilities/manual-audio-effects-2026-10-19.html').read_text(),'FX');assert len(allblocks)==1137
 blocks=[b for b in allblocks if any(h['level']==2 and h['anchor'] in NAMES for h in b['heading_context'])]
 ranges=[(rows[0]['raw_start'],rows[-1]['raw_end']) for name in NAMES if (rows:=[b for b in blocks if section(b)==name])]
 resources=[r for r in allresources if any(lo<=r['raw_start']<hi for lo,hi in ranges)]
 req=load(K/'requirements.json');cases=load(K/'cases.json');ri={r['id']:i for i,r in enumerate(req)};ci={c['id']:i for i,c in enumerate(cases)};routes={};counts=Counter();assessments=[]
 for bi,b in enumerate(blocks):
  name=section(b);code=NAMES[name];counts[name]+=1;routes[b['id']]=dict(section=name,device=code,old_local_locator=f'{name}:B{counts[name]:02}',actual_paragraph_anchor=b['attributes'].get('id'),heading_context=b['heading_context'])
  q=dict(disposition='E',requirements=[],cases=[],proposal_groups=[],assessment='Literal actual numbered heading and ancestry only; no behavioral closure or coverage from heading presence.') if b['kind'].startswith('h') else plan['judgments'][b['id']]
  rids=[f'REQ-DEVICE-{code}-{n:03}' for n in q['requirements']];cids=[f'{code}-C{n:03}' for n in q['cases']]
  assessments.append(dict(id=f'FEA-A{bi+1:03}',block=b['id'],block_pointer=f'/blocks/{bi}',full_qualifier_context_pointer=f'/blocks/{bi}/text',source_text_span=[0,len(b['text'])],quote=b['text'],quote_sha256=sha256(b['text'].encode()).hexdigest(),scope='Whole paragraph/list/heading context judgment; mixed clauses may have different support. Not atomic facets or complete claim/case coverage.',disposition=STATUS[q['disposition']],assessment=q['assessment'],requirement_refs=[dict(catalog='owner_requirements',json_pointer=f'/{ri[id]}',id=id,scoped_predicate_pointer=f'/{ri[id]}/text') for id in rids],case_refs=[dict(catalog='owner_cases',json_pointer=f'/{ci[id]}',id=id,actual_action_pointer=f'/{ci[id]}/setup_action') for id in cids],proposal_groups=q['proposal_groups'],documentary_expected=None,documentary_comparison=None,actual_expected=None,actual_comparison=None,target='U',executed=False,complete=False,coverage_credit=0))
 for r in resources:r.update(role='Literal imageURL/emptyalt/attribute/caption/link text read, responsive data retained/hashchecked. Pixels and linked destination uninspected. EQ8inlineDevice_unfold URL does not prove a rendered glyph.',pixels_or_destination_inspected=False,target='U',complete=False)
 proposals=deepcopy(plan['proposals'])
 for g in proposals:g['assessment_ids']=[a['id'] for a in assessments if g['id'] in a['proposal_groups']]
 questions=deepcopy(plan['source_questions'])
 for q in questions:q.update(quotes=[dict(id=b['id'],json_pointer=f'/blocks/{i}/text',quote=b['text']) for i,b in enumerate(blocks) if b['id'] in q['blocks']],case_refs=[dict(id=id,json_pointer=f'/{ci[id]}',actual_action_pointer=f'/{ci[id]}/setup_action') for id in q['case_ids']],documentary_expected=None,documentary_comparison=None,actual_expected=None,actual_comparison=None,target='U',executed=False,complete=False)
 reverse={name:[dict(id=r['id'],json_pointer=f'/{catalog}/{i}',related_assessment_ids=[a['id'] for a in assessments if any(x['id']==r['id'] for x in a[field])],scope='Exact asof record, not whole clause/action closure; file-only and operationalU may have no primary text association.',application_target='U',complete=False) for i,r in enumerate(rows)] for name,catalog,rows,field in [('requirements','owner_requirements',req,'requirement_refs'),('cases','owner_cases',cases,'case_refs')]}
 spec=(K/'spec-r3.md').read_text();lo=spec.index('## Auto Filter Legacy obligation');hi=spec.index('## Acceptance scope',lo)
 summary=dict(primary='Only four selected h2sections; full1137chapter parse for filtering only',blocks=len(blocks),block_kinds=dict(Counter(b['kind'] for b in blocks)),whole_context_judgments=len(assessments),atomic_facets=False,dispositions=dict(Counter(a['disposition'] for a in assessments)),resources=len(resources),resource_kinds=dict(Counter(r['kind'] for r in resources)),requirements=65,cases=128,D12_cases=78,Dpkg_file_only_cases=4,U_cases=46,proposals=12,source_questions=4,immutable_file_pins=105,existing_exact_canonical_providers=2,new_normative_IDs=0,new_cases=0,new_documentary_nonnull=0,actual_nonnull=0,executed=0,coverage_credit=0,complete_topics=0)
 return dict(role='Fullselectedsource reconciliation only; bounded proposals not owner adoption, target compatibility or completion.',source=load(K/'sources.json')[0],source_capture_utc=None,read_scope=plan['read_scope'],blocks=blocks,resources=resources,block_routes=routes,owner_requirements=req,owner_cases=cases,owner_fixtures=load(K/'fixture-signals.json'),owner_asof=dict(manifest='filter-eq/manifest-author-r3.json',sha256='d294a6bb22b9bd7d0a28165c6a9719dc4dd8733ba87a9e2879ab6354f6833167',spec='filter-eq/spec-r3.md',research='filter-eq/research-r3.md',policy='Immutable exact current-R3canonical providers, no livecanonicalhashgates; R1requiredcorrections/R2partialapproval/R3editorialapproval retain prior scopes.'),legacy_scope=dict(provider='filter-eq/spec-r3.md',text_span=[lo,hi],quote=spec[lo:hi],scope='CurrentmodernAutoFilter2 versusLegacyAutoFilter package/predecessor route only. No modernD12law borrowed; targetinteraction/audioU; no separateLegacy sourceaudit claimed.'),case_scope=[dict(id=c['id'],json_pointer=f'/owner_cases/{i}',retained_provenance=c['provenance'],retained_criterion=c['criterion'],application_target='U',audit_actual_expected=None,audit_actual_comparison=None,executed=False,file_only=c['provenance']=='Dpkg') for i,c in enumerate(cases)],assessments=assessments,proposals=proposals,source_questions=questions,common_future_prerequisites=plan['common_future_prerequisites'],reverse_catalogs=reverse,summary=summary)

def guards(a):
 plan=load(P/'plan.json');assert len(a['blocks'])==len(a['assessments'])==108 and len(a['resources'])==28
 assert Counter(b['kind'] for b in a['blocks'])=={'p':83,'li':11,'h2':4,'h3':8,'h4':2}
 assert Counter(section(b) for b in a['blocks'])=={'auto-filter':65,'channel-eq':12,'eq-eight':23,'eq-three':8}
 assert Counter(r['kind'] for r in a['resources'])=={'image':14,'caption':13,'link':1}
 assert set(plan['judgments'])=={b['id'] for b in a['blocks'] if not b['kind'].startswith('h')}
 assert a['owner_requirements']==load(K/'requirements.json') and a['owner_cases']==load(K/'cases.json') and a['owner_fixtures']==load(K/'fixture-signals.json')
 for f in a['assessments']:
  b=ptr(a,f['block_pointer']);assert b['id']==f['block'] and f['source_text_span']==[0,len(b['text'])] and f['quote']==b['text']==ptr(a,f['full_qualifier_context_pointer']) and f['quote_sha256']==sha256(b['text'].encode()).hexdigest()
  if not b['kind'].startswith('h'):
   q=plan['judgments'][b['id']];code=NAMES[section(b)];assert f['assessment']==q['assessment'] and f['disposition']==STATUS[q['disposition']] and f['proposal_groups']==q['proposal_groups']
   assert [r['id'] for r in f['requirement_refs']]==[f'REQ-DEVICE-{code}-{n:03}' for n in q['requirements']]
   assert [r['id'] for r in f['case_refs']]==[f'{code}-C{n:03}' for n in q['cases']]
  for r in f['requirement_refs']+f['case_refs']:
   assert ptr(a[r['catalog']],r['json_pointer'])['id']==r['id']
   key='actual_action_pointer' if r['catalog']=='owner_cases' else 'scoped_predicate_pointer';field='setup_action' if r['catalog']=='owner_cases' else 'text';assert ptr(a[r['catalog']],r[key])==ptr(a[r['catalog']],r['json_pointer'])[field]
  assert all(f[k] is None for k in ('documentary_expected','documentary_comparison','actual_expected','actual_comparison')) and f['target']=='U' and f['executed'] is f['complete'] is False and f['coverage_credit']==0
 assert len(a['proposals'])==12
 for i,g in enumerate(a['proposals']):
  assert {k:v for k,v in g.items() if k!='assessment_ids'}==plan['proposals'][i] and g['assessment_ids']==[f['id'] for f in a['assessments'] if g['id'] in f['proposal_groups']] and g['assessment_ids']
  assert all(g[k] is None for k in ('documentary_expected','documentary_comparison','actual_expected','actual_comparison')) and g['target']=='U' and g['executed'] is g['complete'] is False and not g['new_normative_IDs'] and g['coverage_credit']==0
 assert a['common_future_prerequisites']==plan['common_future_prerequisites']
 assert 'genuine periodic/stochastic filterANDoutput response' in a['proposals'][0]['proposed_future_positive_baseline']
 assert 'Each includedLowShelf ANDHighShelf independently genuinely productive' in a['proposals'][9]['proposed_future_positive_baseline']
 assert 'Both filters genuinely productive/distinguishable' in a['proposals'][10]['proposed_future_positive_baseline']
 assert Counter(c['provenance'] for c in a['owner_cases'])=={'D12':78,'Dpkg':4,'U':46}
 assert all(c['status']=='unexecuted' for c in a['owner_cases']) and all(c['expected'] is None for c in a['owner_cases'] if c['provenance']=='U')
 assert all(c['criterion']=='Exact retained XML strings; no application or audio assertion.' for c in a['owner_cases'] if c['provenance']=='Dpkg')
 assert len(a['case_scope'])==128
 for r in a['case_scope']:
  c=ptr(a,r['json_pointer']);assert c['id']==r['id'] and r['retained_provenance']==c['provenance'] and r['retained_criterion']==c['criterion'] and r['file_only']==(c['provenance']=='Dpkg') and r['application_target']=='U' and r['audit_actual_expected'] is r['audit_actual_comparison'] is None and r['executed'] is False
 for key,catalog,field in [('requirements','owner_requirements','requirement_refs'),('cases','owner_cases','case_refs')]:
  assert len(a['reverse_catalogs'][key])==len(a[catalog])
  for r in a['reverse_catalogs'][key]:assert ptr(a,r['json_pointer'])['id']==r['id'] and r['related_assessment_ids']==[f['id'] for f in a['assessments'] if any(x['id']==r['id'] for x in f[field])]
 for i,q in enumerate(a['source_questions']):
  assert all(q[k]==v for k,v in plan['source_questions'][i].items())
  for r in q['quotes']:assert ptr(a,r['json_pointer'])==r['quote']
  for r in q['case_refs']:assert ptr(a['owner_cases'],r['json_pointer'])['id']==r['id'] and ptr(a['owner_cases'],r['actual_action_pointer'])==ptr(a['owner_cases'],r['json_pointer'])['setup_action']
  assert all(q[k] is None for k in ('documentary_expected','documentary_comparison','actual_expected','actual_comparison')) and q['target']=='U' and q['executed'] is q['complete'] is False
 # Finite source/action distinctions, not closure by citation.
 byblock={f['block']:f for f in a['assessments']}
 assert byblock['FX:B060']['disposition']==STATUS['X'] and byblock['FX:B061']['disposition']==STATUS['X']
 assert byblock['FX:B087']['disposition']==STATUS['U'] and byblock['FX:B091']['disposition']==STATUS['X'] and byblock['FX:B081']['disposition']==STATUS['U']
 assert byblock['FX:B420']['disposition']==STATUS['R'] and len(byblock['FX:B420']['case_refs'])==6
 assert byblock['FX:B435']['disposition']==STATUS['R'] and [r['id'] for r in byblock['FX:B435']['case_refs']]==['EQ3-C005','EQ3-C006','EQ3-C007','EQ3-C013']
 legacy=a['legacy_scope'];assert (K/'spec-r3.md').read_text()[slice(*legacy['text_span'])]==legacy['quote'] and 'None of the current Auto Filter D12 laws is assigned to Legacy' in legacy['quote']

def main():
 assert sys.dont_write_bytecode and sys.argv[1:]==['--check'],'Read-only --check only; writes refused'
 packet_before={str(p):dg(p) for p in P.iterdir() if p.is_file()};inputs=load(P/'inputs.json');assert len(inputs['files'])==105
 before={r['path']:dg(ROOT/r['path']) for r in inputs['files']}
 for r in inputs['files']:pin(ROOT/r['path'],r)
 m=load(K/'manifest-author-r3.json');assert dg(K/'manifest-author-r3.json')['sha256']=='d294a6bb22b9bd7d0a28165c6a9719dc4dd8733ba87a9e2879ab6354f6833167'
 providers={r['canonical']:r for r in inputs['canonical_providers']};assert len(providers)==2
 for r in m['files']:pin(ROOT/providers[r['path']]['provider'] if r['path'] in providers else ROOT/r['path'],r)
 for r in inputs['canonical_providers']:pin(ROOT/r['provider'],r)
 for rev in (1,2):
  archive=K/f'revisions/author-r{rev}';old=load(archive/f'manifest-author-r{rev}.json')
  for r in old['files']:pin(archive/r['path'],r)
 for r in load(K/'sources.json'):pin(K/r['path'],r) # Only retained/external copies, never source_path installed originals.
 a=build();guards(a);assert a==load(P/'audit.json')
 spec=(K/'spec-r3.md').read_text();matches=list(re.finditer(r'^### (REQ-[A-Z0-9-]+) — ([^\n]+)\n\n\*\*(D12|Dpkg|U)\.\*\* (.*?)\n\nEvidence:',spec,re.M|re.S))
 assert [(m[1],m[2],m[3],m[4]) for m in matches]==[(r['id'],r['title'],r['provenance'],r['text']) for r in a['owner_requirements']]
 table=[line for line in spec.splitlines() if re.match(r'\| (AF|CEQ|EQ8|EQ3)-C\d{3} ',line)];assert len(table)==128
 cmap={c['id']:c for c in a['owner_cases']}
 for line in table:
  cells=[v.strip() for v in re.split(r'(?<!\\)\|',line.strip().strip('|'))];c=cmap[cells[0]];assert cells[2]==c['kind']+': '+c['setup_action'] and cells[3]==(c['expected'] or 'Unknown; no oracle, record without grading.')
 raw=(P.parent/'audio-utilities/manual-audio-effects-2026-10-19.html').read_text()
 for b in a['blocks']:assert raw[b['raw_start']:b['raw_end']]==b['raw_html'] and raw.count('\n',0,b['raw_start'])+1==b['html_line'] and b['html_column']==b['raw_start']-(raw.rfind('\n',0,b['raw_start'])+1)
 for r in a['resources']:
  start=r['raw_start'];assert sha256(raw[start:raw.index('>',start)+1].encode()).hexdigest()==r['starttag_sha256'] and r['pixels_or_destination_inspected'] is False
 for name in NAMES:
  new=[b for b in a['blocks'] if section(b)==name];old=load(K/f'manual-{name}-blocks.json');assert len(new)==len(old)
  for b,r in zip(new,old):assert all(b[k]==r[k] for k in ('kind','text','html_line')) and a['block_routes'][b['id']]['old_local_locator']==r['locator']
 rejected=[]
 for name in ('omit-list-item','wrong-action-pointer','invent-actual','resolve-Type-union','resolve-detector-tap','erase-true-LFO-baseline','grade-stochastic-signal','erase-Peak-positive','erase-lit-LED-positive','borrow-enumeration-as-operation','borrow-inspection-as-expandededit','borrow-PeakScale-as-shelves','file-runtime-promotion','borrow-modern-into-Legacy','no-Audition-positive'):
  t=deepcopy(a)
  if name=='omit-list-item':t['blocks'].remove(next(b for b in t['blocks'] if b['kind']=='li'))
  elif name=='wrong-action-pointer':next(f for f in t['assessments'] if f['block']=='FX:B420')['case_refs'][0]['actual_action_pointer']='/0/setup_action'
  elif name=='invent-actual':t['proposals'][0]['actual_expected']='pass'
  elif name=='resolve-Type-union':t['source_questions'][1]['question']='Seven-entryunionestablished'
  elif name=='resolve-detector-tap':t['source_questions'][0]['question']='Prefilterdetectorproven'
  elif name=='erase-true-LFO-baseline':next(c for c in t['owner_cases'] if c['id']=='AF-C021')['setup_action']='Enablebothwithoutisolatedpositives'
  elif name=='grade-stochastic-signal':next(c for c in t['owner_cases'] if c['id']=='AF-C058')['expected']='Equalrandomtraces'
  elif name=='erase-Peak-positive':next(c for c in t['owner_cases'] if c['id']=='EQ8-C018')['setup_action']='Peakzeroisfine'
  elif name=='erase-lit-LED-positive':next(c for c in t['owner_cases'] if c['id']=='EQ3-C005')['setup_action']='Disableunlitband'
  elif name=='borrow-enumeration-as-operation':next(f for f in t['assessments'] if f['block']=='FX:B060')['disposition']=STATUS['R']
  elif name=='borrow-inspection-as-expandededit':next(f for f in t['assessments'] if f['block']=='FX:B421')['disposition']=STATUS['R']
  elif name=='borrow-PeakScale-as-shelves':next(f for f in t['assessments'] if f['block']=='FX:B427')['disposition']=STATUS['R']
  elif name=='file-runtime-promotion':next(c for c in t['case_scope'] if c['file_only'])['application_target']='Dpkg'
  elif name=='borrow-modern-into-Legacy':t['legacy_scope']['quote']='ModernAutoFilterlawsapplytoLegacy'
  else:t['proposals'][10]['proposed_future_positive_baseline']='Twoenabledflagsenough'
  try:guards(t)
  except AssertionError:rejected.append(name)
  else:raise AssertionError('Unsafe mutation accepted: '+name)
 assert len(rejected)==15
 parse=runpy.run_path(str(P.parent/'midi-editing-source-audit/source_parser.py'))['extract'];fb,fr=parse('<div id="chapter_content"><h1 id="root">Root</h1><h2 id="eq-eight">EQ</h2><ul><li>48 or 12.</li><li>Conditional 2x.</li></ul><p>Use <img alt="" data-src="uninspected"> button.</p><figcaption>Literal.</figcaption><h2 id="other">Other</h2><p>Excluded.</p></div>','FIX')
 assert [b['kind'] for b in fb]==['h1','h2','li','li','p','h2','p'] and fb[4]['text']=='Use button.' and fb[3]['heading_context'][-1]['anchor']=='eq-eight' and len(fr)==2
 seal=P/'manifest.json'
 if seal.exists():
  m=load(seal);assert m['summary']==a['summary'] and set(packet_before)=={str(P/n) for n in m['files']}|{str(seal)}
  for n,r in m['files'].items():pin(P/n,r)
 for path in P.iterdir():
  raw=path.read_bytes();assert raw.endswith(b'\n') and all(line.rstrip(b' \t')==line for line in raw.splitlines()),path
  if path.suffix=='.json':load(path)
 for dest in re.findall(r'\]\(([^)]+)\)',(P/'README.md').read_text()):
  if not re.match('[A-Za-z]+:',dest):assert (P/dest.split('#')[0]).is_file(),dest
 assert before=={r['path']:dg(ROOT/r['path']) for r in inputs['files']} and packet_before=={str(p):dg(p) for p in P.iterdir() if p.is_file()}
 print(json.dumps(dict(status='pass',sealed=seal.exists(),summary=a['summary'],rejected_mutations=rejected,parser_list_inlineglyph_fixture=True,input_pins_unchanged=True,packet_unchanged=True,writes=False,old_authors_validators_decodes_runtime_native_hardware_network_candidate=False),indent=2))
if __name__=='__main__':main()
