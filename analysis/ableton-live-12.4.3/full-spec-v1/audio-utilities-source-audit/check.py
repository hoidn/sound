"""Finite Utility/Tuner/Spectrum retained-source audit. --check is read-only.
Uses only pinned own pure HTML parser; original captures/checkers/package code
are hashed as data, never imported, decoded or executed. No write mode.
"""
from pathlib import Path
from hashlib import sha256
from collections import Counter
from copy import deepcopy
import json,re,runpy,sys
P=Path(__file__).resolve().parent;ROOT=P.parents[3];K=P.parent/'audio-utilities'
load=lambda p:json.loads(p.read_text())
def dg(p):
 b=p.read_bytes();return dict(bytes=len(b),sha256=sha256(b).hexdigest())
def pin(p,r):assert dg(p)=={k:r[k] for k in ('bytes','sha256')},p
def ptr(v,p):
 for k in p.split('/')[1:]:v=v[int(k)] if isinstance(v,list) else v[k.replace('~1','/').replace('~0','~')]
 return v
STATUS=dict(R='represented-source-clause-and-actual-case-subset',G='missing-selected-clause-action-or-qualifier',U='documented-outcome-or-source-context-U',M='research-or-guidance',O='other-owner-context-only',E='editorial-or-structural')
def profile(block):return next(h['anchor'] for h in block['heading_context'] if h['level']==2)
def build():
 plan=load(P/'plan.json');parse=runpy.run_path(str(P.parent/'midi-editing-source-audit/source_parser.py'))['extract']
 allblocks,allresources=parse((K/'manual-audio-effects-2026-10-19.html').read_text(),'FX');assert len(allblocks)==1137
 blocks=[b for b in allblocks if any(h['level']==2 and h['anchor'] in {'utility','tuner','spectrum'} for h in b['heading_context'])]
 resources=[r for r in allresources if blocks[0]['raw_start']<=r['raw_start']<blocks[-1]['raw_end']]
 owners={name:load(K/f'{name}-cases.json') for name in ['utility','tuner','spectrum']};facets=[];routes={};counts=Counter()
 for bi,b in enumerate(blocks):
  name=profile(b);counts[name]+=1;routes[b['id']]=dict(profile=name,owner_local_block=f'{name}:B{counts[name]:02}',raw_paragraph_anchor=b['attributes'].get('id'),nearest_heading=b['heading_context'][-1])
  pieces=[dict(part=0,span=[0,len(b['text'])],disposition='E',requirements=[],cases=[],proposal_groups=[],assessment='Literal actual numbered heading/ancestry only; no semantic closure or leaf coverage from heading presence.')] if b['kind'].startswith('h') else plan['parts'][b['id']]
  for piece in pieces:
   lo,hi=piece['span'];quote=b['text'][lo:hi]
   facets.append(dict(id=f'UAS-A{len(facets)+1:03}',block=b['id'],block_pointer=f'/blocks/{bi}',profile=name,owner_local_block=routes[b['id']]['owner_local_block'],part=piece['part'],text_span=[lo,hi],quote=quote,quote_sha256=sha256(quote.encode()).hexdigest(),full_qualifier_context_pointer=f'/blocks/{bi}/text',disposition=STATUS[piece['disposition']],assessment=piece['assessment'],requirement_refs=[dict(catalog=f'owner_profiles/{name}/requirements',json_pointer=f'/{i-1}',id=owners[name]['requirements'][i-1]['id'],scoped_predicate_pointer=f'/{i-1}/contract') for i in piece['requirements']],case_refs=[dict(catalog=f'owner_profiles/{name}/cases',json_pointer=f'/{i-1}',id=owners[name]['cases'][i-1]['id'],actual_setup_pointer=f'/{i-1}/setup',actual_action_pointer=f'/{i-1}/actions') for i in piece['cases']],proposal_groups=piece['proposal_groups'],documentary_expected=None,documentary_comparison=None,actual_expected=None,actual_comparison=None,target='U',executed=False,complete=False,coverage_credit=0))
 for resource in resources:resource.update(role='Literal imageURL/emptyalt/attributes/caption text read; repeated srcset/sizes retained/hashchecked. No pixels or followed destinations. Spectrum inlineDevice_unfold URL does not identify a visually inspected glyph.',pixels_or_destination_inspected=False,target='U',complete=False)
 proposals=deepcopy(plan['proposals'])
 for g in proposals:g['assessment_ids']=[a['id'] for a in facets if g['id'] in a['proposal_groups']]
 reverse={name:{kind:[dict(id=row['id'],json_pointer=f'/owner_profiles/{name}/{kind}/{i}',related_assessment_ids=[a['id'] for a in facets if any(x['id']==row['id'] for x in a[field])],scope='Exact asof record preserved. A source/action subset, file-only observation or U probe is not complete device/source coverage.',target_application='U',complete=False) for i,row in enumerate(owners[name][kind])] for kind,field in [('requirements','requirement_refs'),('cases','case_refs')]} for name in owners}
 questions=deepcopy(plan['source_questions'])
 for q in questions:q.update(quotes=[dict(block=b['id'],json_pointer=f'/blocks/{i}/text',quote=b['text']) for i,b in enumerate(blocks) if b['id'] in q['blocks']],documentary_expected=None,documentary_comparison=None,actual_expected=None,actual_comparison=None,target='U',executed=False,complete=False)
 summary=dict(primary='Only Utility/Tuner/Spectrum full selectedsections;1137chapter blocks parsed for filtering only',blocks=len(blocks),block_kinds=dict(Counter(b['kind'] for b in blocks)),source_text_parts=93,assessments=len(facets),dispositions=dict(Counter(f['disposition'] for f in facets)),resources=len(resources),resource_kinds=dict(Counter(r['kind'] for r in resources)),requirements=41,cases=103,D12_cases=56,Dpkg_file_only_cases=6,U_cases=41,proposals=9,source_questions=3,immutable_file_pins=50,embedded_canonical_snapshots=4,new_normative_IDs=0,new_cases=0,new_documentary_nonnull=0,actual_nonnull=0,executed=0,coverage_credit=0,complete_topics=0)
 return dict(role='Analyst source reconciliation only; concrete proposals are not owner adoption or runtime coverage.',source=load(K/'sources.json')[0],source_capture_utc=None,scope=plan['read_scope'],blocks=blocks,resources=resources,block_routes=routes,owner_profiles=owners,owner_fixtures=load(K/'fixture-signals.json'),owner_asof=dict(manifest='audio-utilities/manifest-author-r1.json',sha256='5f00a299ae0a7daefd61cc43b29f089fe8b80bc59e773ffcc244836b592548bb',canonical_providers='inputs.json#/canonical_snapshots',policy='Exact embedded4asof snapshots; no futurelivecanonicalhashgate. Independent original review approvedpartial; oldauthorpendingprose historical.'),case_scope=[dict(profile=name,id=c['id'],catalog_pointer=f'/owner_profiles/{name}/cases/{i}',retained_grade=c['target_grade'],retained_comparison_scope=c['comparison'],application_target='U',audit_actual_expected=None,audit_actual_comparison=None,executed=False,file_only=c['provenance']=='Dpkg') for name in owners for i,c in enumerate(owners[name]['cases'])],assessments=facets,proposals=proposals,source_questions=questions,selected_tuning_context=plan['selected_tuning_context'],common_future_prerequisites=plan['common_future_prerequisites'],reverse_catalogs=reverse,summary=summary)

def guards(a):
 plan=load(P/'plan.json');assert len(a['blocks'])==46 and len(a['resources'])==19 and len(a['assessments'])==101
 assert Counter(b['kind'] for b in a['blocks'])=={'h2':3,'h3':5,'p':35,'li':3}
 assert [b['id'] for b in a['blocks']]==[f'FX:B{i}' for i in range(1044,1090)]
 assert Counter(profile(b) for b in a['blocks'])=={'utility':14,'tuner':21,'spectrum':11}
 assert Counter(r['kind'] for r in a['resources'])=={'image':10,'caption':9}
 per={b['id']:[] for b in a['blocks']};assert set(plan['parts'])=={b['id'] for b in a['blocks'] if not b['kind'].startswith('h')}
 for f in a['assessments']:
  b=ptr(a,f['block_pointer']);assert b['id']==f['block'];per[b['id']].append(f);lo,hi=f['text_span']
  assert f['quote']==b['text'][lo:hi] and f['quote_sha256']==sha256(f['quote'].encode()).hexdigest() and ptr(a,f['full_qualifier_context_pointer'])==b['text']
  assert f['profile']==profile(b) and f['owner_local_block']==a['block_routes'][b['id']]['owner_local_block']
  if not b['kind'].startswith('h'):
   p=plan['parts'][b['id']][f['part']];assert f['text_span']==p['span'] and f['assessment']==p['assessment'] and f['disposition']==STATUS[p['disposition']] and f['proposal_groups']==p['proposal_groups']
   assert [r['id'] for r in f['requirement_refs']]==[a['owner_profiles'][f['profile']]['requirements'][i-1]['id'] for i in p['requirements']]
   assert [r['id'] for r in f['case_refs']]==[a['owner_profiles'][f['profile']]['cases'][i-1]['id'] for i in p['cases']]
  for r in f['requirement_refs']+f['case_refs']:
   rows=ptr(a,'/'+r['catalog']);assert ptr(rows,r['json_pointer'])['id']==r['id']
   if 'actual_action_pointer' in r:assert ptr(rows,r['actual_action_pointer'])==ptr(rows,r['json_pointer'])['actions'] and ptr(rows,r['actual_setup_pointer'])==ptr(rows,r['json_pointer'])['setup']
   else:assert ptr(rows,r['scoped_predicate_pointer'])==ptr(rows,r['json_pointer'])['contract']
  assert all(f[k] is None for k in ('documentary_expected','documentary_comparison','actual_expected','actual_comparison')) and f['target']=='U' and f['executed'] is f['complete'] is False and f['coverage_credit']==0
 for b in a['blocks']:
  mask=[False]*len(b['text'])
  for f in per[b['id']]:
   for i in range(*f['text_span']):assert not mask[i];mask[i]=True
  assert all(mask[i] or ch.isspace() for i,ch in enumerate(b['text'])),b['id']
 for i,g in enumerate(a['proposals']):
  assert {k:v for k,v in g.items() if k!='assessment_ids'}==plan['proposals'][i]
  assert g['assessment_ids']==[f['id'] for f in a['assessments'] if g['id'] in f['proposal_groups']] and g['assessment_ids']
  assert all(g[k] is None for k in ('documentary_expected','documentary_comparison','actual_expected','actual_comparison')) and g['target']=='U' and g['executed'] is g['complete'] is False and not g['new_normative_IDs'] and g['coverage_credit']==0
 assert len(a['proposals'])==9
 # Guard actual source/action distinctions independently of labels/titles.
 assert per['FX:B1089'][0]['disposition']==STATUS['R'] and per['FX:B1089'][1]['disposition']==STATUS['G']
 assert per['FX:B1061'][1]['disposition']==STATUS['G'] # Targetball004005 != arrows
 assert all(f['disposition']==STATUS['G'] for f in per['FX:B1059'][2:]) # viewbuttons != bothcolors
 assert per['FX:B1081'][2]['disposition']==STATUS['R'] and per['FX:B1081'][4]['disposition']==STATUS['R']
 assert per['FX:B1054'][0]['disposition']==STATUS['R'] and [r['id'] for r in per['FX:B1054'][0]['case_refs']]==['DSP-018','DSP-019']
 assert per['FX:B1086'][2]['disposition']==STATUS['R'] and [r['id'] for r in per['FX:B1086'][2]['case_refs']]==['DUT-016','DUT-017','DUT-018']
 assert a['common_future_prerequisites']==plan['common_future_prerequisites']
 assert 'BOTH available Width and Mid/Side controls genuinely productive' in a['proposals'][0]['proposed_future_positive_baseline']
 assert 'sustained NONZERO downstream output tail BEFORE Mute' in a['proposals'][2]['proposed_future_positive_baseline']
 assert 'Relevant low/DC component independently established AND nonlinear effect afterUtility' in a['proposals'][3]['proposed_future_positive_baseline']
 assert 'actual successful manual Range AND zoom' in a['proposals'][6]['proposed_future_positive_baseline']
 for name,owner in a['owner_profiles'].items():
  assert owner==load(K/f'{name}-cases.json')
  for c in owner['cases']:
   assert c['execution']=='unexecuted'
   if c['provenance']=='Dpkg':assert c['target_grade']=='Dpkg' and 'retained-file values only' in c['comparison']
   else:assert c['target_grade']=='U'
   if c['provenance']=='U':assert c['expected'] is None and c['comparison']=='No expected outcome or tolerance; do not grade.'
  for kind,field in [('requirements','requirement_refs'),('cases','case_refs')]:
   assert len(a['reverse_catalogs'][name][kind])==len(owner[kind])
   for r in a['reverse_catalogs'][name][kind]:assert ptr(a,r['json_pointer'])['id']==r['id'] and r['related_assessment_ids']==[f['id'] for f in a['assessments'] if any(x['id']==r['id'] for x in f[field])]
 for row in a['case_scope']:
  c=ptr(a,row['catalog_pointer']);assert c['id']==row['id'] and row['retained_grade']==c['target_grade'] and row['file_only']==(c['provenance']=='Dpkg') and row['application_target']=='U' and row['audit_actual_expected'] is row['audit_actual_comparison'] is None and row['executed'] is False
 assert a['selected_tuning_context']==plan['selected_tuning_context']
 for key in ('source_audit_context','current_tuning_requirement','current_tuning_case'):
  r=a['selected_tuning_context'][key];assert ptr(load(ROOT/r['path']),r['json_pointer'])==r['record']
 s=a['selected_tuning_context']['source_audit_context']['record'];assert (ROOT/s['source_path']).read_text()[slice(*s['text_span'])]==s['quote'] and s['capture_utc'] is None
 assert a['selected_tuning_context']['current_tuning_case']['record']['id']=='TUN-015' and 'External MPE-capable receiver' in a['selected_tuning_context']['current_tuning_case']['record']['setup']
 for q in a['source_questions']:
  for r in q['quotes']:assert ptr(a,r['json_pointer'])==r['quote']
  assert all(q[k] is None for k in ('documentary_expected','documentary_comparison','actual_expected','actual_comparison')) and q['target']=='U' and q['executed'] is q['complete'] is False

def main():
 assert sys.dont_write_bytecode and sys.argv[1:]==['--check'],'Read-only --check only; writes refused'
 packet_before={str(p):dg(p) for p in P.rglob('*') if p.is_file()};inputs=load(P/'inputs.json');assert len(inputs['files'])==50
 before={r['path']:dg(ROOT/r['path']) for r in inputs['files']}
 for r in inputs['files']:pin(ROOT/r['path'],r)
 manifest=load(K/'manifest-author-r1.json');assert len(manifest['payloads'])==44 and dg(K/'manifest-author-r1.json')['sha256']=='5f00a299ae0a7daefd61cc43b29f089fe8b80bc59e773ffcc244836b592548bb'
 snapshots={s['original_canonical']:s for s in inputs['canonical_snapshots']};assert len(snapshots)==4
 for r in manifest['payloads']:
  if r['path'] in snapshots:
   s=snapshots[r['path']];raw=s['text'].encode();assert dict(bytes=len(raw),sha256=sha256(raw).hexdigest())=={k:r[k] for k in ('bytes','sha256')}=={k:s[k] for k in ('bytes','sha256')}
  else:pin(ROOT/r['path'],r) # Retained bytes only, including compressed files.
 a=build();guards(a);assert a==load(P/'audit.json')
 for name,owner in a['owner_profiles'].items():
  text=snapshots[f'wiki/specs/device-{name}.md']['text'];matches=list(re.finditer(r'^### (REQ-[A-Z0-9-]+) — ([^\n]+)\n\n\*\*(D12|Dpkg|U)\.\*\* (.*?)\n\nEvidence:',text,re.M|re.S))
  assert [(m[1],m[2],m[3],m[4]) for m in matches]==[(r['id'],r['title'],r['grade'],r['contract']) for r in owner['requirements']]
  table=[line for line in text.splitlines() if re.match(r'\| (DUT|DTU|DSP)-\d{3} ',line)];assert len(table)==len(owner['cases'])
  for line,c in zip(table,owner['cases']):
   cells=[v.strip() for v in re.split(r'(?<!\\)\|',line.strip().strip('|'))]
   assert cells[0]==c['id'] and cells[2]==f"{c['kind']}: {c['setup']}. {c['actions']}" and cells[3]==(c['expected'] if c['expected'] is not None else 'Unknown; no oracle, do not grade.')
 raw=(K/'manual-audio-effects-2026-10-19.html').read_text()
 for b in a['blocks']:assert raw[b['raw_start']:b['raw_end']]==b['raw_html'] and raw.count('\n',0,b['raw_start'])+1==b['html_line'] and b['html_column']==b['raw_start']-(raw.rfind('\n',0,b['raw_start'])+1)
 for r in a['resources']:
  start=r['raw_start'];assert sha256(raw[start:raw.index('>',start)+1].encode()).hexdigest()==r['starttag_sha256'] and r['pixels_or_destination_inspected'] is False
 for name in a['owner_profiles']:
  selected=[b for b in a['blocks'] if profile(b)==name];old=load(K/f'manual-{name}-blocks.json');assert len(selected)==len(old)
  for new,oldrow in zip(selected,old):assert all(new[key]==oldrow[key] for key in ('kind','text','html_line')) and a['block_routes'][new['id']]['owner_local_block']==oldrow['locator']
 rejected=[]
 for name in ('omit-source-part','wrong-case-pointer','invent-actual','erase-true-DCfilter','borrow-ball-for-arrows','borrow-viewbuttons-for-colors','erase-both-displayroutes','erase-true-gainsteps','one-width-baseline','no-sustained-tail','DC-without-nonlinear','no-manual-Range-positive','Dpkg-runtime-promotion','TUN015-as-Tuner'):
  t=deepcopy(a)
  if name=='omit-source-part':t['assessments'].pop()
  elif name=='wrong-case-pointer':next(f for f in t['assessments'] if f['block']=='FX:B1061')['case_refs'][0]['json_pointer']='/2'
  elif name=='invent-actual':t['proposals'][0]['actual_expected']='pass'
  elif name=='erase-true-DCfilter':next(f for f in t['assessments'] if f['block']=='FX:B1089')['disposition']=STATUS['G']
  elif name=='borrow-ball-for-arrows':next(f for f in t['assessments'] if f['block']=='FX:B1061' and f['part']==1)['disposition']=STATUS['R']
  elif name=='borrow-viewbuttons-for-colors':next(f for f in t['assessments'] if f['block']=='FX:B1059' and f['part']==3)['disposition']=STATUS['R']
  elif name=='erase-both-displayroutes':next(f for f in t['assessments'] if f['block']=='FX:B1054')['case_refs'].pop()
  elif name=='erase-true-gainsteps':next(f for f in t['assessments'] if f['block']=='FX:B1086' and f['part']==2)['case_refs'].pop()
  elif name=='one-width-baseline':t['proposals'][0]['proposed_future_positive_baseline']='Widthonly enabled'
  elif name=='no-sustained-tail':t['proposals'][2]['proposed_future_positive_baseline']='Effectenabled, silenttail acceptable'
  elif name=='DC-without-nonlinear':t['proposals'][3]['proposed_future_positive_baseline']='DC input only'
  elif name=='no-manual-Range-positive':t['proposals'][6]['proposed_future_positive_baseline']='Autoenabled only'
  elif name=='Dpkg-runtime-promotion':next(r for r in t['case_scope'] if r['file_only'])['application_target']='Dpkg'
  else:t['selected_tuning_context']['current_tuning_case']['record']['setup']='Tunerreferenceproof'
  try:guards(t)
  except AssertionError:rejected.append(name)
  else:raise AssertionError('Unsafe audit mutation accepted: '+name)
 assert len(rejected)==14
 parse=runpy.run_path(str(P.parent/'midi-editing-source-audit/source_parser.py'))['extract'];fb,fr=parse('<div id="chapter_content"><h1 id="root">Root</h1><h2 id="spectrum">Spectrum</h2><p>Press <img alt="" data-src="uninspected"> button. Keep 1.1.1.</p><figcaption>Literal.</figcaption><h2 id="other">Other</h2><p>Excluded.</p></div>','FIX')
 assert fb[2]['text']=='Press button. Keep 1.1.1.' and fb[2]['heading_context'][-1]['anchor']=='spectrum' and fb[-1]['heading_context'][-1]['anchor']=='other' and Counter(r['kind'] for r in fr)=={'image':1,'caption':1}
 seal=P/'manifest.json'
 if seal.exists():
  m=load(seal);assert m['summary']==a['summary'] and set(packet_before)=={str(P/n) for n in m['files']}|{str(seal)}
  for n,r in m['files'].items():pin(P/n,r)
 for path in P.iterdir():
  rawtext=path.read_bytes();assert rawtext.endswith(b'\n') and all(line.rstrip(b' \t')==line for line in rawtext.splitlines()),path
  if path.suffix=='.json':load(path)
 for dest in re.findall(r'\]\(([^)]+)\)',(P/'README.md').read_text()):
  if not re.match('[A-Za-z]+:',dest):assert (P/dest.split('#')[0]).is_file(),dest
 assert before=={r['path']:dg(ROOT/r['path']) for r in inputs['files']} and packet_before=={str(p):dg(p) for p in P.rglob('*') if p.is_file()}
 print(json.dumps(dict(status='pass',sealed=seal.exists(),summary=a['summary'],rejected_mutations=rejected,parser_inline_glyph_fixture=True,input_pins_unchanged=True,packet_unchanged=True,writes=False,old_checkers_decodes_runtime_native_hardware_network_candidate=False),indent=2))
if __name__=='__main__':main()
