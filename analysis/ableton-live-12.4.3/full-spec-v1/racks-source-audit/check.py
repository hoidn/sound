"""Compact full retained Racks source audit; own parser/data only.
--check is read-only. Author --write refuses an existing audit or frozen seal.
No original/vendor functions, source scripts, hardware or application execute.
"""
from pathlib import Path
from hashlib import sha256
from collections import Counter
from copy import deepcopy
import json,re,runpy,sys
P=Path(__file__).resolve().parent;ROOT=P.parents[3];K=P.parent/'racks'
load=lambda p:json.loads(p.read_text())
def dg(p):b=p.read_bytes();return dict(bytes=len(b),sha256=sha256(b).hexdigest())
def pin(p,r):assert dg(p)=={k:r[k] for k in ['bytes','sha256']},p
def ptr(v,p):
 for k in p.split('/')[1:] if p else []:v=v[int(k)] if isinstance(v,list) else v[k.replace('~1','/').replace('~0','~')]
 return v
STATUS=dict(R='represented-source-clause-and-actual-case-subset',G='missing-selected-clause-action-or-context',U='documented-outcome-or-source-context-U',M='research-or-guidance',E='editorial-or-structural',O='other-owner-selected-context')
def snapshot(kind):return next(r for r in load(P/'inputs.json')['canonical_snapshots'] if '/'+kind+'/' in r['original_canonical'])
def reqs():
 spec=snapshot('specs')['text'];out=[]
 for m in re.finditer(r'^### (REQ-DEVICE-RACKS-\d{3}) — ([^\n]+)\n(.*?)(?=^### |^## |\Z)',spec,re.M|re.S):
  out.append(dict(id=m[1],title=m[2],contract=m[3],snapshot='inputs.json#/canonical_snapshots/1/text',text_span=[m.start(3),m.end(3)]))
 assert len(out)==28;return out

def build():
 inputs=load(P/'inputs.json');plan=load(P/'plan.json');source=load(K/'sources.json')[0]
 parse=runpy.run_path(str(P.parent/'clip-view-source-audit/source_parser.py'))['extract']
 raw=(K/source['file']).read_text();blocks,resources=parse(raw,'RACK');requirements=reqs();cases=load(K/'cases.json');facets=[]
 for bi,block in enumerate(blocks):
  pieces=[dict(part=0,span=[0,len(block['text'])],disposition='E',requirements=[],cases=[],proposal_groups=[],assessment='Literal numbered heading/ancestry only; no semantic behavior or direct TOC/leaf closure.')] if block['kind'].startswith('h') else plan['parts'][block['id']]
  for piece in pieces:
   start,end=piece['span'];quote=block['text'][start:end]
   facets.append(dict(id=f'RKA-A{len(facets)+1:03}',block=block['id'],block_pointer=f'/blocks/{bi}',part=piece['part'],text_span=[start,end],quote=quote,quote_sha256=sha256(quote.encode()).hexdigest(),full_qualifier_context_pointer=f'/blocks/{bi}/text',literal_paragraph_anchor=block['attributes'].get('id'),disposition=STATUS[piece['disposition']],assessment=piece['assessment'],requirement_refs=[dict(catalog='owner_requirements',json_pointer=f'/{i-1}',id=requirements[i-1]['id'],scoped_predicate_pointer=f'/{i-1}/contract') for i in piece['requirements']],case_refs=[dict(catalog='owner_cases',json_pointer=f'/{i-1}',id=cases['cases'][i-1]['id'],actual_action_pointer=f'/{i-1}/setup_action') for i in piece['cases']],proposals=piece['proposal_groups'],documentary_expected=None,documentary_comparison=None,actual_expected=None,actual_comparison=None,target='U',executed=False,complete=False,coverage_credit=0))
 for resource in resources:resource.update(role='Literal caption/link text, image data-src/baseURL/emptyalt/attribute keys read; repeated srcset/sizes retained/hashchecked. No pixels, diagrams or linked destinations inspected.',pixels_or_destination_inspected=False,complete=False,target='U')
 proposals=deepcopy(plan['proposals'])
 for proposal in proposals:
  proposal['assessment_ids']=[f['id'] for f in facets if proposal['id'] in f['proposals']]
  if proposal['id']=='RKA-G22':proposal['operational_U_case_refs']=[dict(catalog='owner_cases',json_pointer=f'/{i}',id=c['id']) for i,c in enumerate(cases['cases']) if c['id'] in plan['owner_operational_U_cases']]
 reverse={key:[dict(id=r['id'],json_pointer=f'/{catalog}/{i}',related_assessment_ids=[f['id'] for f in facets if any(v['id']==r['id'] for v in f[field])],scope='Exact historical/asof IDs retained; selected-source association is not whole requirement/case closure. CommonDevices-only and installed/operationalU may have no primary text association.',complete=False,target='U') for i,r in enumerate(rows)] for key,catalog,rows,field in [('requirements','owner_requirements',requirements,'requirement_refs'),('cases','owner_cases',cases['cases'],'case_refs')]}
 questions=deepcopy(plan['source_questions'])
 for question in questions:
  question['quotes']=[dict(block=b['id'],json_pointer=f'/blocks/{i}/text',quote=b['text']) for i,b in enumerate(blocks) if b['id'] in question['blocks']]
  question.update(documentary_expected=None,documentary_comparison=None,actual_expected=None,actual_comparison=None,executed=False,complete=False)
 summary=dict(primary='Full retained Racks primary chapter only; CommonDevices153blocks not fully semantically audited',blocks=len(blocks),block_kinds=dict(Counter(b['kind'] for b in blocks)),text_parts=sum(map(len,plan['parts'].values())),assessments=len(facets),dispositions=dict(Counter(f['disposition'] for f in facets)),resources=len(resources),resource_kinds=dict(Counter(r['kind'] for r in resources)),owner_requirements=28,owner_cases=61,installed_source_assertions=3,documented_old_criteria=46,old_U_cases=12,proposals=22,selected_common_device_paragraphs=7,immutable_file_pins=len(inputs['files']),embedded_canonical_snapshots=2,new_normative_IDs=0,new_cases=0,new_documentary_nonnull=0,actual_nonnull=0,executed=0,complete_topics=0,coverage_credit=0)
 return dict(role='Audit-only retained-source paragraph/subclaim reconciliation with finite proposed actions; no owner adoption or full behavioral completion.',source=dict(**source,file_pin=dict(path=str((K/source['file']).relative_to(ROOT)),**dg(K/source['file'])),locator_policy='raw spans are decodedUnicode character offsets; actual paragraph id is separate from heading ancestry; section titles/links are not semantic closure'),blocks=blocks,resources=resources,owner_requirements=requirements,owner_cases=cases['cases'],owner_criterion_scope=cases['criterion_scope'],owner_asof=dict(corrected_manifest='racks/manifest.json',sha256='42f16a02b5b7de3190eee8c40b4dcb19a85f9232eb0ff5bdb75b8a3183c83779',spec='inputs.json#/canonical_snapshots/1/text',research='inputs.json#/canonical_snapshots/0/text',policy='Exactembeddedasof canonical snapshots; no currentlivecanonicalhashgate. Researchpendingrecheck prose is historicalauthorstatus; retainedfinalreview independentlyapprovedpartial RR01/RR02correction.'),selected_common_device_context=plan['selected_common_device_context'],assessments=facets,proposals=proposals,source_questions=questions,common_future_prerequisites=plan['common_future_prerequisites'],reverse_catalogs=reverse,read_scope=plan['read_scope'],summary=summary)

def guards(a):
 plan=load(P/'plan.json');assert len(a['blocks'])==124 and len(a['resources'])==53 and len(a['assessments'])==264
 assert Counter(b['kind'] for b in a['blocks'])=={'p':70,'li':31,'h1':1,'h2':8,'h3':12,'h4':2}
 assert Counter(r['kind'] for r in a['resources'])=={'image':25,'caption':22,'link':6}
 assert len(a['owner_requirements'])==28 and len(a['owner_cases'])==61
 perblock={b['id']:[] for b in a['blocks']};assert set(plan['parts'])=={b['id'] for b in a['blocks'] if not b['kind'].startswith('h')}
 for facet in a['assessments']:
  block=ptr(a,facet['block_pointer']);assert block['id']==facet['block'];perblock[block['id']].append(facet)
  lo,hi=facet['text_span'];assert facet['quote']==block['text'][lo:hi] and facet['quote_sha256']==sha256(facet['quote'].encode()).hexdigest() and ptr(a,facet['full_qualifier_context_pointer'])==block['text']
  assert facet['literal_paragraph_anchor']==block['attributes'].get('id')
  if not block['kind'].startswith('h'):
   p=plan['parts'][block['id']][facet['part']];assert facet['disposition']==STATUS[p['disposition']] and facet['assessment']==p['assessment'] and facet['text_span']==p['span']
   assert [r['id'] for r in facet['case_refs']]==[f'RCK-{i:03}' for i in p['cases']]
   assert [r['id'] for r in facet['requirement_refs']]==[f'REQ-DEVICE-RACKS-{i:03}' for i in p['requirements']]
   assert facet['proposals']==p['proposal_groups']
  for r in facet['case_refs']+facet['requirement_refs']:
   assert ptr(a[r['catalog']],r['json_pointer'])['id']==r['id']
   if r['catalog']=='owner_cases':assert ptr(a[r['catalog']],r['actual_action_pointer'])==ptr(a[r['catalog']],r['json_pointer'])['setup_action']
  assert all(facet[k] is None for k in ['documentary_expected','documentary_comparison','actual_expected','actual_comparison'])
  assert facet['target']=='U' and facet['executed'] is facet['complete'] is False and facet['coverage_credit']==0
  if facet['disposition']==STATUS['G']:assert facet['proposals']
 for b in a['blocks']:
  covered=set();rows=perblock[b['id']];assert [r['part'] for r in rows]==list(range(len(rows)))
  for f in rows:
   pos=set(range(*f['text_span']));assert not covered.intersection(pos);covered|=pos
  assert all(i in covered for i,ch in enumerate(b['text']) if not ch.isspace()),b['id']
 assert [p['id'] for p in a['proposals']]==[f'RKA-G{i:02}' for i in range(1,23)]
 for p in a['proposals']:
  assert p['proposed_minimal_delta'] and p['proposed_future_positive_baseline'] and p['limits'] and p['new_normative_IDs']==[]
  assert p['assessment_ids']==[f['id'] for f in a['assessments'] if p['id'] in f['proposals']]
  assert p['assessment_ids'] or p['id']=='RKA-G22' and p['operational_U_case_refs']
  assert all(p[k] is None for k in ['documentary_expected','documentary_comparison','actual_expected','actual_comparison']) and p['target']=='U' and p['executed'] is p['complete'] is False and p['coverage_credit']==0
 # Explicit actual-action distinctions, not source-block citation inference.
 assert perblock['RACK:B019'][1]['disposition']==STATUS['G'] # existingGroup != emptygenericRack
 assert perblock['RACK:B059'][0]['disposition']==STATUS['G'] # keyfade020 != velocityfade
 assert perblock['RACK:B064'][0]['disposition']==STATUS['G'] # keyfade020 != MIDIselectorfade
 assert perblock['RACK:B086'][2]['disposition']==STATUS['G'] # browser-samplelayer042 != pad-to-pad
 assert all(f['disposition']==STATUS['G'] for f in perblock['RACK:B087'][:2]) # configured043 != Receivechange
 assert perblock['RACK:B109'][0]['disposition']==STATUS['R'] and perblock['RACK:B109'][1]['disposition']==STATUS['G']
 assert perblock['RACK:B121'][1]['disposition']==STATUS['R'] and perblock['RACK:B121'][3]['disposition']==STATUS['G'] # realpan044 != titlefocus
 assert all(f['disposition']==STATUS['R'] for f in perblock['RACK:B122']) # real045equalvol retained
 assert perblock['RACK:B085'][1]['disposition']==STATUS['R'] and any(r['id']=='RCK-042' for r in perblock['RACK:B085'][1]['case_refs'])
 assert 'NoteANDCC baselines both required' in a['common_future_prerequisites']['negative']
 assert 'sustained' in a['proposals'][7]['proposed_future_positive_baseline'] and 'nonmutedwet/output' in a['proposals'][7]['proposed_future_positive_baseline']
 assert 'BOTH mapped controls independently genuinely productive' in a['proposals'][17]['proposed_future_positive_baseline']
 assert 'sixreturns supportedsource, seventh061U' in a['proposals'][9]['limits']
 assert 'empty-altinlineglyph omission' in a['proposals'][14]['proposed_minimal_delta']
 for q in a['source_questions']:
  for r in q['quotes']:assert ptr(a,r['json_pointer'])==r['quote']
  assert all(q[k] is None for k in ['documentary_expected','documentary_comparison','actual_expected','actual_comparison']) and q['target']=='U' and q['executed'] is q['complete'] is False
 assert len(a['reverse_catalogs']['requirements'])==28 and len(a['reverse_catalogs']['cases'])==61
 for key,catalog,field in [('requirements','owner_requirements','requirement_refs'),('cases','owner_cases','case_refs')]:
  for r in a['reverse_catalogs'][key]:
   assert ptr(a,r['json_pointer'])['id']==r['id']
   assert r['related_assessment_ids']==[f['id'] for f in a['assessments'] if any(v['id']==r['id'] for v in f[field])]
 for r in a['owner_requirements']:assert snapshot('specs')['text'][slice(*r['text_span'])]==r['contract']

def main():
 assert sys.dont_write_bytecode and sys.argv[1:] in (['--write'],['--check'])
 writing=sys.argv[1:]==['--write'];seal=P/'manifest.json'
 if writing:assert not seal.exists(),'Frozen audit: writes refused';assert not(P/'audit.json').exists(),'Refuse existingaudit overwrite'
 before={str(p):dg(p) for p in P.rglob('*') if p.is_file()};inputs=load(P/'inputs.json');assert len(inputs['files'])==len({r['path'] for r in inputs['files']})==21
 watched={r['path']:dg(ROOT/r['path']) for r in inputs['files']}
 for r in inputs['files']:pin(ROOT/r['path'],r)
 assert dg(K/'manifest.json')['sha256']=='42f16a02b5b7de3190eee8c40b4dcb19a85f9232eb0ff5bdb75b8a3183c83779'
 for s in inputs['canonical_snapshots']:
  raw=s['text'].encode();assert len(raw)==s['bytes'] and sha256(raw).hexdigest()==s['sha256']
  entry=next(r for r in load(K/'manifest.json')['payloads'] if r['path']==s['original_canonical']);assert all(s[k]==entry[k] for k in ['bytes','sha256'])
 a=build();guards(a);raw=(K/a['source']['file']).read_text()
 for b in a['blocks']:
  assert raw[b['raw_start']:b['raw_end']]==b['raw_html'] and raw.count('\n',0,b['raw_start'])+1==b['html_line']
  assert b['html_column']==b['raw_start']-(raw.rfind('\n',0,b['raw_start'])+1)
 for r in a['resources']:
  start=r['raw_start'];end=raw.index('>',start)+1;assert sha256(raw[start:end].encode()).hexdigest()==r['starttag_sha256'] and r['pixels_or_destination_inspected'] is False
 parse=runpy.run_path(str(P.parent/'clip-view-source-audit/source_parser.py'))['extract'];db,_=parse((K/'manual-devices-2026-10-19.html').read_text(),'DEV');assert len(db)==153
 assert a['selected_common_device_context']==[db[i-1] for i in [55,108,109,125,126,127,128]]
 assert a['owner_requirements']==reqs() and a['owner_cases']==load(K/'cases.json')['cases']
 assert Counter(c['criterion_domain'] for c in a['owner_cases'])=={'installed-document':3,'Live-12-documented':46,'unknown':12}
 for c in a['owner_cases']:assert c['execution']=='unexecuted'
 # Independent negative fixtures exercise omission, borrowed actions and productive prerequisites.
 rejected=[]
 for name in ['omit-qualified-clause','wrong-case-pointer','borrow-keyfade-for-velocity','borrow-sample-layer-for-pads','borrow-configured-Multi-for-Receive','erase-true-equal-volume','invent-actual','note-only-CC-baseline','no-sustained-tail','one-mapped-Rand-baseline','support-seventh-return','invent-inline-glyph']:
  t=deepcopy(a)
  if name=='omit-qualified-clause':t['assessments']=[f for f in t['assessments'] if not(f['block']=='RACK:B109' and f['part']==1)]
  elif name=='wrong-case-pointer':next(f for f in t['assessments'] if f['block']=='RACK:B059')['case_refs'][0]['json_pointer']='/18'
  elif name=='borrow-keyfade-for-velocity':next(f for f in t['assessments'] if f['block']=='RACK:B059')['disposition']=STATUS['R']
  elif name=='borrow-sample-layer-for-pads':next(f for f in t['assessments'] if f['block']=='RACK:B086' and f['part']==2)['disposition']=STATUS['R']
  elif name=='borrow-configured-Multi-for-Receive':next(f for f in t['assessments'] if f['block']=='RACK:B087')['disposition']=STATUS['R']
  elif name=='erase-true-equal-volume':next(f for f in t['assessments'] if f['block']=='RACK:B122')['disposition']=STATUS['G']
  elif name=='invent-actual':t['proposals'][0]['actual_expected']='pass'
  elif name=='note-only-CC-baseline':t['common_future_prerequisites']['negative']='Note reception only proves controller exclusion'
  elif name=='no-sustained-tail':t['proposals'][7]['proposed_future_positive_baseline']='Effect enabled flag only'
  elif name=='one-mapped-Rand-baseline':t['proposals'][17]['proposed_future_positive_baseline']='A mapped only; B flag is enough'
  elif name=='support-seventh-return':t['proposals'][9]['limits']='Seven returns supported'
  else:t['proposals'][14]['proposed_minimal_delta']='Read emptyandgap as proven plus/minus image glyphs'
  try:guards(t)
  except AssertionError:rejected.append(name)
  else:raise AssertionError('Unsafeauditmutationaccepted: '+name)
 assert len(rejected)==12
 fixture='<div id="chapter_content"><h1 id="root">Root</h1><p>Use <img alt="" data-src="uninspected"> and <img alt="" data-src="uninspected"> buttons. Keep 1.1.1.</p><h2 id="child">Child</h2><ul><li>Qualified input.</li></ul><figcaption>Caption.</figcaption></div>'
 fb,fr=parse(fixture,'FIX');assert [x['kind'] for x in fb]==['h1','p','h2','li'] and fb[1]['text']=='Use and buttons. Keep 1.1.1.' and fb[-1]['heading_context'][-1]['anchor']=='child' and Counter(x['kind'] for x in fr)=={'image':2,'caption':1}
 if writing:(P/'audit.json').write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n')
 else:
  assert load(P/'audit.json')==a
  if seal.exists():
   m=load(seal);assert {str(p.relative_to(P)) for p in P.rglob('*') if p.is_file()}==set(m['files'])|{seal.name}
   for n,r in m['files'].items():pin(P/n,r)
   assert m['summary']==a['summary']
  for p in P.rglob('*'):
   if p.is_file():
    raw=p.read_bytes();assert raw.endswith(b'\n') and all(line.rstrip(b' \t')==line for line in raw.splitlines()),p
    if p.suffix=='.json':load(p)
  for dest in re.findall(r'\]\(([^)]+)\)',(P/'README.md').read_text()):
   if not re.match('[A-Za-z]+:',dest):assert (P/dest.split('#')[0]).is_file(),dest
  assert before=={str(p):dg(p) for p in P.rglob('*') if p.is_file()}
 assert watched=={r['path']:dg(ROOT/r['path']) for r in inputs['files']}
 print(json.dumps(dict(status='pass',sealed=seal.exists(),summary=a['summary'],rejection_fixtures=rejected,parser_inline_image_fixture=True,pins_unchanged=True,packet_unchanged=not writing,writes=writing,original_native_vendor_runtime_hardware_network=False),indent=2))
if __name__=='__main__':main()
