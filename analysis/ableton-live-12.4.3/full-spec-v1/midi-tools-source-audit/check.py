"""Finite retained MIDI Tools audit; only inspected analyst parser/data, no vendor execution."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
from copy import deepcopy
import json,re,runpy,subprocess,sys
P=Path(__file__).resolve().parent;ROOT=P.parents[3];K=P.parent/'midi-editing'
load=lambda p:json.loads(p.read_text())
def dg(p):
 b=p.read_bytes();return dict(bytes=len(b),sha256=sha256(b).hexdigest())
def pin(p,row):assert dg(p)=={k:row[k] for k in ('bytes','sha256')},str(p)
def ptr(v,s):
 for k in s.split('/')[1:] if s else []:v=v[int(k)] if isinstance(v,list) else v[k.replace('~1','/').replace('~0','~')]
 return v
STATUS={'R':'represented-actual-bounded-subset','G':'missing-selected-clause-action-or-context','U':'documented-outcome-or-source-context-U','O':'other-owner-selected-context','M':'research-or-guidance','E':'editorial-or-structural'}
def reqs():
 out=[]
 for line in (K/'spec-r2.md').read_text().splitlines():
  if line.startswith('| REQ-MIDI-EDIT-'):
   cells=[v.strip() for v in line.strip('|').split('|')];assert len(cells)==5
   out.append(dict(zip(('id','operation','preconditions','contract','evidence'),cells),literal_row=line))
 assert len(out)==43;return out

def build():
 plan=load(P/'plan.json');source=load(K/'sources.json')[1];raw=(K/source['html']).read_text()
 assert dg(K/source['html'])==dict(bytes=305130,sha256='ebe83b52ba7b11ada85691f524f8e817534c604eac1c0edd4aa9c7b9327fd6ab')
 parse=runpy.run_path(str(P.parent/'clip-view-source-audit/source_parser.py'))['extract'];blocks,resources=parse(raw,'TOOLS')
 ownerreq=reqs();cases=load(K/'acceptance-cases-r2.json');allcases=cases['cases'];facets=[]
 for bi,b in enumerate(blocks):
  parts=[dict(part=0,span=[0,len(b['text'])],disposition='E',requirements=[],cases=[],proposal_groups=[],assessment='Exact numbered heading only; no semantic completion.')] if b['kind'].startswith('h') else plan['parts'][b['id']]
  for row in parts:
   a,z=row['span'];quote=b['text'][a:z]
   facets.append(dict(id=f'MTA-A{len(facets)+1:03}',block=b['id'],block_json_pointer=f'/blocks/{bi}',part=row['part'],text_span=[a,z],quote=quote,quote_sha256=sha256(quote.encode()).hexdigest(),qualifier_context_pointer=f'/blocks/{bi}/text',disposition=STATUS[row['disposition']],assessment=row['assessment'],requirement_refs=[dict(catalog='owner_requirements',json_pointer=f'/{n-1}',id=ownerreq[n-1]['id']) for n in row['requirements']],case_refs=[dict(catalog='owner_cases',json_pointer=f'/{n-1}',id=allcases[n-1]['id']) for n in row['cases']],external_refs=[dict(catalog='external_contexts',json_pointer=f'/{i}',id=r['id']) for id in row.get('external_context_ids',plan['external_associations'].get(b['id'],[])) for i,r in enumerate(plan['external_contexts']) if r['id']==id],proposals=row.get('proposal_groups',[]),documentary_expected=None,documentary_comparison=None,actual_expected=None,actual_comparison=None,target='U',executed=False,complete=False,coverage_credit=0))
 for r in resources:r.update(pixels_or_destination_inspected=False,target='U',complete=False,role='Literal caption/link text, image baseURL/alt/attributekeys read; repeated size/srcset values retained/hashchecked. No pixels or separately followed destination inspected.')
 proposals=deepcopy(plan['proposals'])
 for g in proposals:
  g['assessment_ids']=[f['id'] for f in facets if g['id'] in f['proposals']]
  g['missing_facet_ids']=[f['id'] for f in facets if g['id'] in f['proposals'] and f['disposition']==STATUS['G']]
 questions=deepcopy(plan['source_questions'])
 for q in questions:
  q['quotes']=[dict(block=b['id'],json_pointer=f'/blocks/{i}/text',quote=b['text'],html_line=b['html_line']) for i,b in enumerate(blocks) if b['id'] in q['blocks']]
  if 'additional_source' in q:
   b,_=parse((ROOT/q['additional_source']['source_path']).read_text(),'MIDI');record=next(r for r in b if r['id']==q['additional_source']['block']);q['additional_source'].update(quote=record['text'],raw_start=record['raw_start'],raw_end=record['raw_end'],html_line=record['html_line'],source_sha256=dg(ROOT/q['additional_source']['source_path'])['sha256'])
  q.update(documentary_expected=None,documentary_comparison=None,actual_expected=None,actual_comparison=None,target='U',executed=False,complete=False)
 reverse={kind:[dict(id=r['id'],json_pointer=f'/{key}/{i}',related_facets=[f['id'] for f in facets if any(a['id']==r['id'] for a in f[field])],complete=False,target='U',role='Exact as-of ID retained; related subset never closes whole obligation. Empty primary-source references may be EditingMIDI or explicit operational U outside this chapter.') for i,r in enumerate(rows)] for kind,key,rows,field in [('requirements','owner_requirements',ownerreq,'requirement_refs'),('cases','owner_cases',allcases,'case_refs')]}
 tools=[dict(block=b['id'],heading=b['text'],anchor=b['attributes']['id'],source_json_pointer=f'/blocks/{i}') for i,b in enumerate(blocks) if b['kind']=='h3' and b['attributes'].get('data-number','').startswith(('11.2.','11.3.'))]
 summary=dict(primary_chapter='Full retained MIDI Tools only; separate244block EditingMIDI chapter not newly fully audited here',blocks=len(blocks),block_kinds=dict(Counter(b['kind'] for b in blocks)),paragraph_list_parts=sum(map(len,plan['parts'].values())),facets=len(facets),dispositions=dict(Counter(f['disposition'] for f in facets)),resources=len(resources),resource_kinds=dict(Counter(r['kind'] for r in resources)),requirements_asof=43,cases_asof=60,tool_profiles=len(tools),proposals=len(proposals),selected_external_records=len(plan['external_contexts']),source_context_questions=len(questions),input_pins=len(load(P/'inputs.json')),actual_nonnull=0,new_documentary_nonnull=0,executed=0,new_normative_IDs=0,complete_topics=0,coverage_credit=0)
 return dict(role='Full retained source semantic reconciliation; partial source-only judgments/proposals, not normative adoption or product/topic completeness',source=dict(**source,file_pin=dict(path=str((K/source['html']).relative_to(ROOT)),**dg(K/source['html'])),exact_capture_utc=None,locator_limit='raw_start/raw_end are decoded Unicode character positions; heading ancestry is context, never inherited paragraph anchor or TOC completion'),blocks=blocks,resources=resources,owner_requirements=ownerreq,owner_cases=allcases,owner_actual_status=cases['actual_result_status'],owner_fixture=load(K/'fixtures-r2.json'),owner_asof=dict(spec_provider=str((K/'spec-r2.md').relative_to(ROOT)),research_provider=str((K/'research-r2.md').relative_to(ROOT)),case_provider=str((K/'acceptance-cases-r2.json').relative_to(ROOT)),manifest=str((K/'manifest-author-r2.json').relative_to(ROOT)),policy='Immutable R2 as-of data only; root may advance additive ownerR3 independently. No live canonical hash/status/count gate or claim those later actions absent.43clauses60actions read across this and prior EditingMIDI audit, exact current R2 provider bytes reverified.'),external_contexts=plan['external_contexts'],global_external_context=plan['global_external_context'],assessments=facets,proposals=proposals,source_questions=questions,common_future_prerequisites=plan['common_future_prerequisites'],tool_profiles=tools,reverse_catalogs=reverse,summary=summary)

def semantic_guards(a):
 assert len(a['blocks'])==146 and len(a['resources'])==101 and len(a['assessments'])==302
 assert Counter(b['kind'] for b in a['blocks'])=={'p':120,'li':4,'h1':1,'h2':3,'h3':18}
 assert Counter(r['kind'] for r in a['resources'])=={'image':42,'caption':42,'link':17}
 assert len(a['owner_requirements'])==43 and len(a['owner_cases'])==60 and len(a['tool_profiles'])==17
 plan=load(P/'plan.json');byblock={b['id']:[] for b in a['blocks']}
 assert set(plan['parts'])=={b['id'] for b in a['blocks'] if not b['kind'].startswith('h')}
 for f in a['assessments']:
  b=ptr(a,f['block_json_pointer']);assert b['id']==f['block'];byblock[b['id']].append(f)
  start,end=f['text_span'];assert f['quote']==b['text'][start:end] and f['quote_sha256']==sha256(f['quote'].encode()).hexdigest()
  assert ptr(a,f['qualifier_context_pointer'])==b['text']
  if not b['kind'].startswith('h'):
   p=plan['parts'][b['id']][f['part']];assert f['disposition']==STATUS[p['disposition']] and f['assessment']==p['assessment'] and f['text_span']==p['span']
   assert [r['id'] for r in f['case_refs']]==[f'MED-{i:03}' for i in p['cases']]
   assert [r['id'] for r in f['requirement_refs']]==[f'REQ-MIDI-EDIT-{i:03}' for i in p['requirements']]
   assert f['proposals']==p['proposal_groups']
  for r in f['case_refs']+f['requirement_refs']+f['external_refs']:assert ptr(a[r['catalog']],r['json_pointer'])['id']==r['id']
  assert all(f[k] is None for k in ('actual_expected','actual_comparison','documentary_expected','documentary_comparison'))
  assert f['target']=='U' and f['executed'] is f['complete'] is False and f['coverage_credit']==0
  if f['disposition']==STATUS['G']:assert f['proposals']
 for b in a['blocks']:
  covered=set();rows=byblock[b['id']];assert [f['part'] for f in rows]==list(range(len(rows)))
  for f in rows:
   positions=set(range(*f['text_span']));assert not covered.intersection(positions);covered|=positions
  assert all(i in covered for i,ch in enumerate(b['text']) if not ch.isspace()),b['id']
 assert [g['id'] for g in a['proposals']]==[f'MTA-G{i:02}' for i in range(1,22)]
 for g in a['proposals']:
  assert g['assessment_ids'] and g['proposed_minimal_delta'] and g['proposed_future_positive_baseline'] and g['limits']
  assert g['assessment_ids']==[f['id'] for f in a['assessments'] if g['id'] in f['proposals']]
  assert all(g[k] is None for k in ('actual_expected','actual_comparison','documentary_expected','documentary_comparison'))
  assert g['target']=='U' and g['executed'] is g['complete'] is False and g['coverage_credit']==0 and g['new_normative_IDs']==[]
 common=a['common_future_prerequisites'];assert 'NONEMPTY' in common['input'] and 'empty generator results stay U' in common['negative']
 assert 'genuinely observed productive nonzero offset baseline before zero' in a['proposals'][13]['proposed_future_positive_baseline']
 assert 'no fixedor guaranteed distinct rotation' in next(f['assessment'] for f in byblock['TOOLS:B143'] if f['part']==2)
 assert 'never implies adding timeline duration' in a['proposals'][5]['limits']
 assert 'actually observe nonempty generated notes' in a['proposals'][17]['proposed_future_positive_baseline']
 assert 'genuinely observed nonempty working output' in a['proposals'][18]['proposed_future_positive_baseline']
 assert 'actual nonempty output before origin/velocity/capacity' in a['proposals'][20]['proposed_future_positive_baseline']
 for n in [5,55,56,118]:assert all(f['disposition']==STATUS['U'] for f in byblock[f'TOOLS:B{n:03}'])
 assert byblock['TOOLS:B019'][0]['external_refs']==[] and byblock['TOOLS:B019'][0]['disposition']==STATUS['G']
 # True actions retained despite narrower missing branches.
 for b,n in [(9,24),(10,24),(16,25),(31,27),(34,28),(35,28),(51,31),(82,35),(86,35),(87,35),(88,35),(103,38),(105,38),(114,39),(120,40),(139,42),(144,43)]:
  assert any(f['disposition']==STATUS['R'] and any(r['id']==f'MED-{n:03}' for r in f['case_refs']) for f in byblock[f'TOOLS:B{b:03}'])
 assert byblock['TOOLS:B076'][2]['disposition']==STATUS['R'] and any(f['disposition']==STATUS['G'] for f in byblock['TOOLS:B078'])
 for q in a['source_questions']:
  for r in q['quotes']:assert ptr(a,r['json_pointer'])==r['quote']
  assert all(q[k] is None for k in ('actual_expected','actual_comparison','documentary_expected','documentary_comparison')) and q['target']=='U' and q['executed'] is q['complete'] is False

def main():
 assert sys.dont_write_bytecode and sys.argv[1:] in (['--check'],['--write'])
 writing=sys.argv[1:]==['--write'];seal=P/'manifest.json'
 if writing:assert not seal.exists(),'refuse write after seal';assert not (P/'audit.json').exists(),'refuse overwrite existing audit'
 before={str(p):dg(p) for p in P.rglob('*') if p.is_file()};inputs=load(P/'inputs.json');assert len(inputs)==len({p['path'] for p in inputs})==45
 watched={r['path']:dg(ROOT/r['path']) for r in inputs}
 for r in inputs:pin(ROOT/r['path'],r)
 assert sum(r['path'].startswith(str(K.relative_to(ROOT))+'/') for r in inputs)==25
 m=load(K/'manifest-author-r2.json');assert dg(K/'manifest-author-r2.json')['sha256']=='c6d50d13268b6e00efc3e59a3c1bead0d18e8c23a3505b1b0a7d595dc4a198b2'
 for n,r in m['files'].items():pin(K/n,r)
 a=build();semantic_guards(a)
 for r in a['external_contexts']:
  if 'row' in r:assert ptr(load(ROOT/r['catalog']),r['json_pointer'])==r['row']
  else:assert (ROOT/r['catalog']).read_text()[slice(*r['text_span'])]==r['quote']
 raw=(K/a['source']['html']).read_text()
 for b in a['blocks']:
  assert raw[b['raw_start']:b['raw_end']]==b['raw_html'] and raw.count('\n',0,b['raw_start'])+1==b['html_line']
  assert b['html_column']==b['raw_start']-(raw.rfind('\n',0,b['raw_start'])+1)
 for r in a['resources']:
  start=r['raw_start'];end=raw.index('>',start)+1;assert sha256(raw[start:end].encode()).hexdigest()==r['starttag_sha256'] and r['pixels_or_destination_inspected'] is r['complete'] is False
 assert a['owner_requirements']==reqs() and a['owner_cases']==load(K/'acceptance-cases-r2.json')['cases']
 for c in a['owner_cases']:assert c['target_12_4_3_grade']=='U' and c['execution']=='not-run'
 assert a['owner_actual_status']['actual_expected'] is a['owner_actual_status']['actual_comparison'] is None and a['owner_actual_status']['executed'] is False
 for q in a['source_questions']:
  if 'additional_source' in q:
   r=q['additional_source'];assert dg(ROOT/r['source_path'])['sha256']==r['source_sha256']
 # Meaningful rejection fixtures on the actual derived audit, not source execution.
 rejected=0
 for mutation in ['omit-qualified-part','wrong-case-subset','invent-actual','waive-nonempty-generator','zero-only-Strum-baseline','Chop-timeline-insertion','resolve-C3','erase-true-Mirror','force-distinct-RNG','empty-Seed-capacity-baseline','transfer-addon-to-bundled-use']:
  t=deepcopy(a)
  if mutation=='omit-qualified-part':t['assessments']=[f for f in t['assessments'] if not (f['block']=='TOOLS:B013' and f['part']==1)]
  elif mutation=='wrong-case-subset':next(f for f in t['assessments'] if f['block']=='TOOLS:B078')['case_refs']=[dict(catalog='owner_cases',json_pointer='/26',id='MED-027')]
  elif mutation=='invent-actual':t['proposals'][0]['actual_expected']='pass'
  elif mutation=='waive-nonempty-generator':t['common_future_prerequisites']['input']='NonzeroDensity flag alone is sufficient'
  elif mutation=='zero-only-Strum-baseline':t['proposals'][13]['proposed_future_positive_baseline']='EnableStrum and compare zero controls; no prior genuine effect.'
  elif mutation=='Chop-timeline-insertion':t['proposals'][5]['limits']='PositiveGaps inserts timeline duration'
  elif mutation=='resolve-C3':next(f for f in t['assessments'] if f['block']=='TOOLS:B055')['disposition']=STATUS['R']
  elif mutation=='erase-true-Mirror':next(f for f in t['assessments'] if f['block']=='TOOLS:B076' and f['part']==2)['disposition']=STATUS['G']
  elif mutation=='force-distinct-RNG':next(f for f in t['assessments'] if f['block']=='TOOLS:B143' and f['part']==2)['assessment']='Every randomization must differ'
  elif mutation=='empty-Seed-capacity-baseline':t['proposals'][17]['proposed_future_positive_baseline']='NonzeroDensity is enough, allow empty output capacity comparison.'
  elif mutation=='transfer-addon-to-bundled-use':
   target=next(f for f in t['assessments'] if f['block']=='TOOLS:B019' and f['part']==0);target['external_refs']=next(f for f in t['assessments'] if f['block']=='TOOLS:B019' and f['part']==1)['external_refs']
  try:semantic_guards(t)
  except AssertionError:rejected+=1
  else:raise AssertionError('accepted '+mutation)
 assert rejected==11
 fixture='<div id="chapter_content"><h1 id="r">Root</h1><p>Set 1.1.1 now. Keep selection.</p><h2 id="c">Child</h2><ul><li>Qualified input.</li></ul><img alt="" src="not-opened"><figcaption>Literal caption.</figcaption></div>'
 bb,rr=runpy.run_path(str(P.parent/'clip-view-source-audit/source_parser.py'))['extract'](fixture,'FIX')
 assert [b['kind'] for b in bb]==['h1','p','h2','li'] and bb[1]['text']=='Set 1.1.1 now. Keep selection.' and bb[-1]['heading_context'][-1]['anchor']=='c' and [r['kind'] for r in rr]==['image','caption']
 if writing:(P/'audit.json').write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n')
 else:
  assert load(P/'audit.json')==a,'exact reproduction'
  if seal.exists():
   manifest=load(seal);assert {str(p.relative_to(P)) for p in P.rglob('*') if p.is_file()}==set(manifest['files'])|{'manifest.json'}
   for n,r in manifest['files'].items():pin(P/n,r)
   assert manifest['summary']==a['summary']
  for f in P.rglob('*'):
   if f.is_file():
    if f.suffix=='.json':load(f)
    r=subprocess.run(['git','diff','--no-index','--check','/dev/null',str(f)],capture_output=True,text=True);assert r.returncode in (0,1) and not r.stdout and not r.stderr,(str(f),r.stdout,r.stderr)
  for dest in re.findall(r'\]\(([^)]+)\)',(P/'README.md').read_text()):
   if not re.match(r'^[A-Za-z]+:',dest):assert (P/dest.split('#')[0]).is_file(),dest
  assert before=={str(p):dg(p) for p in P.rglob('*') if p.is_file()}
 assert watched=={r['path']:dg(ROOT/r['path']) for r in inputs}
 print(json.dumps(dict(status='pass',sealed=seal.exists(),summary=a['summary'],negative_fixtures=rejected,retained_positive_contexts=17,parser_fixture=True,inputs_unchanged=True,packet_unchanged=not writing,writes=writing,original_runtime_network_candidate=False),indent=2))
if __name__=='__main__':main()
