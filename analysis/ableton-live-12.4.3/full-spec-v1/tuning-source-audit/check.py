"""Finite Tuning retained-source audit; own analyst parser plus inert source/catalog data only."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
from copy import deepcopy
import json,re,runpy,subprocess,sys
P=Path(__file__).resolve().parent;ROOT=P.parents[3];K=P.parent/'mpe-tuning-grooves'
load=lambda p:json.loads(p.read_text())
def dg(p):
 b=p.read_bytes();return dict(bytes=len(b),sha256=sha256(b).hexdigest())
def pin(p,r):assert dg(p)=={k:r[k] for k in ('bytes','sha256')},str(p)
def ptr(v,s):
 for k in s.split('/')[1:] if s else []:v=v[int(k)] if isinstance(v,list) else v[k.replace('~1','/').replace('~0','~')]
 return v
STATUS={'R':'represented-actual-bounded-subset','G':'missing-selected-clause-action-or-context','U':'documented-outcome-or-source-context-U','O':'other-source-or-owner-context','M':'research-or-guidance','E':'editorial-or-structural'}
def requirements():
 rows=[]
 for line in (K/'tuning-systems-author-r2.md').read_text().splitlines():
  if line.startswith('| REQ-TUNING-'):
   c=[x.strip() for x in line.strip('|').split('|')];assert len(c)==4
   rows.append(dict(zip(('id','preconditions','contract','evidence'),c),literal_row=line))
 assert len(rows)==21;return rows

def build():
 plan=load(P/'plan.json');src=next(r for r in load(K/'sources.json') if r['id']=='SRC-MTG-USING-TUNING-SYSTEMS');f=K/src['html'];raw=f.read_text()
 assert dg(f)==dict(bytes=254421,sha256='90922bd082d31f1c383ceaae31aaece094e5cc769f601380cf7f50e10743eddf')
 parse=runpy.run_path(str(P.parent/'clip-view-source-audit/source_parser.py'))['extract'];blocks,resources=parse(raw,'TUN')
 req=requirements();shared=load(K/'cases.json');selected=[(i,r) for i,r in enumerate(shared) if r['id'].startswith('TUN-')];cases=[r for i,r in selected];facets=[]
 for bi,b in enumerate(blocks):
  pp=[dict(part=0,span=[0,len(b['text'])],disposition='E',requirements=[],cases=[],proposals=[],assessment='Exact numbered heading only; no semantic completion.')] if b['kind'].startswith('h') else plan['parts'][b['id']]
  for row in pp:
   start,end=row['span'];q=b['text'][start:end]
   facets.append(dict(id=f'TSA-A{len(facets)+1:03}',block=b['id'],block_json_pointer=f'/blocks/{bi}',part=row['part'],text_span=[start,end],quote=q,quote_sha256=sha256(q.encode()).hexdigest(),qualifier_context_pointer=f'/blocks/{bi}/text',disposition=STATUS[row['disposition']],assessment=row['assessment'],requirement_refs=[dict(catalog='owner_requirements',json_pointer=f'/{n-1}',id=req[n-1]['id']) for n in row['requirements']],case_refs=[dict(catalog='owner_cases',json_pointer=f'/{n-1}',id=cases[n-1]['id']) for n in row['cases']],external_refs=[dict(catalog='external_contexts',json_pointer=f'/{i}',id=r['id']) for id in plan['external_associations'].get(b['id'],[]) for i,r in enumerate(plan['external_contexts']) if r['id']==id],proposals=row['proposals'],documentary_expected=None,documentary_comparison=None,actual_expected=None,actual_comparison=None,target='U',executed=False,complete=False,coverage_credit=0))
 for r in resources:r.update(pixels_or_destination_inspected=False,target='U',complete=False,role='Literal8linktexts/hrefs,12captions and12imagealt/baseURL/attributekeys read; repeated srcsets retained/hashchecked. No pixels or separately followed destination inspected.')
 supplements=deepcopy(plan['supplemental_contexts'])
 for s in supplements:
  s['requirement_refs']=[dict(catalog='owner_requirements',json_pointer=f'/{n-1}',id=req[n-1]['id']) for n in s.pop('requirements')]
  s['case_refs']=[dict(catalog='owner_cases',json_pointer=f'/{n-1}',id=cases[n-1]['id']) for n in s.pop('cases')]
  s['external_refs']=[dict(catalog='external_contexts',json_pointer=f'/{i}',id=r['id']) for id in s.pop('external_context_ids',[]) for i,r in enumerate(plan['external_contexts']) if r['id']==id]
  s['role']='Selected supplemental source-context reconciliation only; no whole FAQ/ASCL/SCL semantic denominator or parser/format conformance claim'
 props=deepcopy(plan['proposals'])
 for g in props:
  g['assessment_ids']=[r['id'] for r in facets if g['id'] in r['proposals']];g['supplemental_context_ids']=[r['id'] for r in supplements if g['id'] in r['proposals']]
 questions=deepcopy(plan['source_context_questions'])
 for q in questions:q.update(documentary_expected=None,documentary_comparison=None,actual_expected=None,actual_comparison=None,target='U',executed=False,complete=False)
 reverse={kind:[dict(id=r['id'],json_pointer=f'/{key}/{i}',related_primary_facets=[a['id'] for a in facets if any(x['id']==r['id'] for x in a[field])],related_supplemental_contexts=[a['id'] for a in supplements if any(x['id']==r['id'] for x in a[field])],complete=False,target='U',role='Exact as-of ID retained; references never close entire clause/case/source topic') for i,r in enumerate(rr)] for kind,key,rr,field in [('requirements','owner_requirements',req,'requirement_refs'),('cases','owner_cases',cases,'case_refs')]}
 summary=dict(primary_scope='Complete retained UsingTuningSystems manual only; selected renderedFAQ/ASCL contexts not full supplementary source audits',blocks=len(blocks),block_kinds=dict(Counter(b['kind'] for b in blocks)),paragraph_list_parts=sum(map(len,plan['parts'].values())),primary_facets=len(facets),dispositions=dict(Counter(a['disposition'] for a in facets)),resources=len(resources),resource_kinds=dict(Counter(r['kind'] for r in resources)),requirements_asof=21,cases_asof=32,selected_supplemental_contexts=len(supplements),selected_external_records=len(plan['external_contexts']),proposal_groups=len(props),source_context_questions=len(questions),immutable_input_pins=len(load(P/'inputs.json')),old_history_files=61,new_documentary_nonnull=0,actual_nonnull=0,executed=0,new_normative_IDs=0,complete_topics=0,coverage_credit=0)
 return dict(role='Full primary-source semantic reconciliation; audit-only proposals, not owner adoption or product/source-topic completeness',source=dict(**src,file_pin=dict(path=str(f.relative_to(ROOT)),**dg(f)),capture_utc=None,locator_limit='raw_start/end are decoded Unicode character positions. Heading ancestry is reading context only; not inherited paragraph anchors or TOC completion.'),blocks=blocks,resources=resources,owner_requirements=req,owner_cases=cases,owner_case_origins=[dict(id=r['id'],catalog=str((K/'cases.json').relative_to(ROOT)),json_pointer=f'/{i}') for i,r in selected],owner_asof=dict(spec_provider=str((K/'tuning-systems-author-r2.md').relative_to(ROOT)),research_provider=str((K/'mpe-tuning-grooves-author-r2.md').relative_to(ROOT)),manifest=str((K/'manifest-author-r2.json').relative_to(ROOT)),policy='Immutable TuningR2/shared83/history only, exact currentTUNsubset21/32. Root MPE/Groove successors stay separate; no future livecanonical/status/count gate or oldchecker replay.'),legacy_expectations='Original expected/comparator strings are documentary proposals only. All32 TUNtarget gradesU/executionunexecuted, no target measurements; every new documentary/actual oracle nullU.',external_contexts=plan['external_contexts'],owner_boundary_contexts=plan['owner_boundary_contexts'],tuner_asof_snapshot=plan['tuner_asof_snapshot'],assessments=facets,supplemental_contexts=supplements,source_context_questions=questions,proposals=props,common_future_prerequisites=plan['common_future_prerequisites'],reverse_catalogs=reverse,summary=summary)

def guards(a):
 assert len(a['blocks'])==49 and Counter(b['kind'] for b in a['blocks'])=={'p':31,'li':11,'h1':1,'h2':4,'h3':2}
 assert len(a['assessments'])==68 and Counter(r['kind'] for r in a['resources'])=={'link':8,'image':12,'caption':12}
 assert len(a['owner_requirements'])==21 and len(a['owner_cases'])==32 and len(a['external_contexts'])==35 and len(a['supplemental_contexts'])==19
 plan=load(P/'plan.json');byblock={b['id']:[] for b in a['blocks']};assert set(plan['parts'])=={b['id'] for b in a['blocks'] if not b['kind'].startswith('h')}
 for f in a['assessments']:
  b=ptr(a,f['block_json_pointer']);assert b['id']==f['block'];byblock[b['id']].append(f)
  start,end=f['text_span'];assert f['quote']==b['text'][start:end] and f['quote_sha256']==sha256(f['quote'].encode()).hexdigest() and ptr(a,f['qualifier_context_pointer'])==b['text']
  if not b['kind'].startswith('h'):
   row=plan['parts'][b['id']][f['part']];assert f['text_span']==row['span'] and f['disposition']==STATUS[row['disposition']] and f['assessment']==row['assessment'] and f['proposals']==row['proposals']
   assert [r['id'] for r in f['requirement_refs']]==[f'REQ-TUNING-{n:03}' for n in row['requirements']]
   assert [r['id'] for r in f['case_refs']]==[f'TUN-{n:03}' for n in row['cases']]
  if f['disposition']==STATUS['G']:assert f['proposals']
 for rows in [a['assessments'],a['supplemental_contexts']]:
  for f in rows:
   for r in f['requirement_refs']+f['case_refs']+f['external_refs']:assert ptr(a[r['catalog']],r['json_pointer'])['id']==r['id']
   assert all(f[k] is None for k in ('documentary_expected','documentary_comparison','actual_expected','actual_comparison')) and f['target']=='U' and f['executed'] is f['complete'] is False and f['coverage_credit']==0
 for b in a['blocks']:
  seen=set();rows=byblock[b['id']];assert [f['part'] for f in rows]==list(range(len(rows)))
  for f in rows:
   positions=set(range(*f['text_span']));assert not seen.intersection(positions);seen|=positions
  assert all(i in seen for i,ch in enumerate(b['text']) if not ch.isspace()),b['id']
 assert [g['id'] for g in a['proposals']]==[f'TSA-G{i:02}' for i in range(1,13)]
 for g in a['proposals']:
  assert g['assessment_ids'] and g['proposed_minimal_delta'] and g['proposed_future_positive_baseline'] and g['limits']
  assert g['assessment_ids']==[f['id'] for f in a['assessments'] if g['id'] in f['proposals']]
  assert g['supplemental_context_ids']==[f['id'] for f in a['supplemental_contexts'] if g['id'] in f['proposals']]
  assert all(g[k] is None for k in ('documentary_expected','documentary_comparison','actual_expected','actual_comparison')) and g['target']=='U' and g['executed'] is g['complete'] is False and g['coverage_credit']==0 and g['new_normative_IDs']==[]
 assert 'genuinely effectiveacceptedtuning on activeunmutednonzero route before Bypass' in a['proposals'][7]['proposed_future_positive_baseline']
 assert 'productivefrequency/soundingpitchchange before identity-only audibleinvariance' in a['proposals'][5]['proposed_minimal_delta']
 assert 'productive validUTF8/recognizedextendedimport' in a['proposals'][10]['proposed_minimal_delta']
 assert 'LINKtextisnotpromiseofclickablebutton' in next(f for f in a['supplemental_contexts'] if f['id']=='TSA-S17')['assessment']
 tunersupp=next(f for f in a['supplemental_contexts'] if f['id']=='TSA-S06');assert tunersupp['requirement_refs']==tunersupp['case_refs']==[] and {r['id'] for r in tunersupp['external_refs']}=={'REQ-DEVICE-TUNER-010','REQ-DEVICE-TUNER-011','REQ-DEVICE-TUNER-012','DTU-028'}
 assert a['source']['capture_utc'] is None
 for s in a['supplemental_contexts']:
  assert s['capture_utc'] is None and 'rendered text, not publisher HTML' in s['source_kind']
  if s['article']=='ASCL':assert '12.1' in s['version']
 # Actual bounded old actions must remain represented, not replaced by generic gaps.
 for b,n in [(10,2),(13,3),(15,4),(16,5),(18,6),(23,7),(25,8),(26,9),(27,9),(29,10),(31,11),(35,12),(41,13),(42,13),(45,14),(46,14)]:
  assert any(f['disposition']==STATUS['R'] and any(r['id']==f'TUN-{n:03}' for r in f['case_refs']) for f in byblock[f'TUN:B{b:03}'])
 assert all(f['disposition']==STATUS['U'] for f in byblock['TUN:B017'])
 assert len(byblock['TUN:B025'])==2 and len(byblock['TUN:B028'])==3 and 'Ref. Pitch/Freq' in byblock['TUN:B025'][0]['quote']
 for q in a['source_context_questions']:assert q['target']=='U' and q['executed'] is q['complete'] is False and all(q[k] is None for k in ('documentary_expected','documentary_comparison','actual_expected','actual_comparison'))

def main():
 assert sys.dont_write_bytecode and sys.argv[1:] in (['--check'],['--write'])
 writing=sys.argv[1:]==['--write'];seal=P/'manifest.json'
 if writing:assert not seal.exists(),'refuse write after seal';assert not (P/'audit.json').exists(),'refuse overwrite existing audit'
 before={str(f):dg(f) for f in P.rglob('*') if f.is_file()};inputs=load(P/'inputs.json');assert len(inputs)==len({r['path'] for r in inputs})==85
 watched={r['path']:dg(ROOT/r['path']) for r in inputs}
 for r in inputs:pin(ROOT/r['path'],r)
 m=load(K/'manifest-author-r2.json');assert len(m['payloads'])==60 and dg(K/'manifest-author-r2.json')['sha256']=='a93a5dca90cf0aa83dd712beaea955549dda093a89668d4294335a45c0e8748a'
 for r in m['payloads']:pin(K/r['path'],r)
 assert {str((K/r['path']).relative_to(ROOT)) for r in m['payloads']}|{str((K/'manifest-author-r2.json').relative_to(ROOT))}<={r['path'] for r in inputs}
 a=build();guards(a)
 for r in a['external_contexts']:
  if 'row' in r:assert ptr(load(ROOT/r['catalog']),r['json_pointer'])==r['row']
  elif 'catalog' in r:assert (ROOT/r['catalog']).read_text()[slice(*r['text_span'])]==r['quote']
  else:assert a[r['snapshot']]['text'][slice(*r['text_span'])]==r['quote']
 snap=a['tuner_asof_snapshot'];assert dict(bytes=len(snap['text'].encode()),sha256=sha256(snap['text'].encode()).hexdigest())=={k:snap[k] for k in ('bytes','sha256')}
 frozen=next(r for r in load(P.parent/'audio-utilities/manifest-author-r1.json')['payloads'] if r['path']==snap['canonical_asof']);assert all(snap[k]==frozen[k] for k in ('bytes','sha256')) # No future live canonical check.
 raw=(K/a['source']['html']).read_text()
 for b in a['blocks']:
  assert raw[b['raw_start']:b['raw_end']]==b['raw_html'] and raw.count('\n',0,b['raw_start'])+1==b['html_line']
  assert b['html_column']==b['raw_start']-(raw.rfind('\n',0,b['raw_start'])+1)
 for r in a['resources']:
  s=r['raw_start'];z=raw.index('>',s)+1;assert sha256(raw[s:z].encode()).hexdigest()==r['starttag_sha256'] and r['pixels_or_destination_inspected'] is r['complete'] is False
 for s in a['supplemental_contexts']:assert dg(ROOT/s['source_path'])['sha256']==s['source_sha256'] and (ROOT/s['source_path']).read_text()[slice(*s['text_span'])]==s['quote']
 assert a['owner_requirements']==requirements() and [r['id'] for r in a['owner_cases']]==[f'TUN-{i:03}' for i in range(1,33)]
 assert Counter(c['documentary_grade'] for c in a['owner_cases'])=={'D12':21,'U':11}
 for r,c in zip(a['owner_case_origins'],a['owner_cases']):assert ptr(load(ROOT/r['catalog']),r['json_pointer'])==c and c['target_build_grade']=='U' and c['execution']=='unexecuted'
 for kind,field in [('requirements','owner_requirements'),('cases','owner_cases')]:assert [r['id'] for r in a['reverse_catalogs'][kind]]==[r['id'] for r in a[field]]
 rejected=0
 for mutation in ['omit-source-qualifier','wrong-case-association','invent-actual','flag-only-bypass','noeffect-reference-without-positive','invalid-import-without-positive','metadata-guaranteed-URI','Tuner-is-MPE-receiver-case','invent-capture-UTC','erase-Custom-persistence','choose-collision-survivor']:
  t=deepcopy(a)
  if mutation=='omit-source-qualifier':t['assessments']=[f for f in t['assessments'] if not (f['block']=='TUN:B028' and f['part']==1)]
  elif mutation=='wrong-case-association':next(f for f in t['assessments'] if f['block']=='TUN:B040')['case_refs']=[dict(catalog='owner_cases',json_pointer='/6',id='TUN-007')]
  elif mutation=='invent-actual':t['proposals'][0]['actual_expected']='pass'
  elif mutation=='flag-only-bypass':t['proposals'][7]['proposed_future_positive_baseline']='Loaded tuning flag suffices'
  elif mutation=='noeffect-reference-without-positive':t['proposals'][5]['proposed_minimal_delta']='Setidentitylabelandacceptunchangedsilence'
  elif mutation=='invalid-import-without-positive':t['proposals'][10]['proposed_minimal_delta']='Malformedfilerefusalpasseswithoutknownvalidimport'
  elif mutation=='metadata-guaranteed-URI':next(s for s in t['supplemental_contexts'] if s['id']=='TSA-S17')['assessment']='LINKguaranteesclickableURI'
  elif mutation=='Tuner-is-MPE-receiver-case':next(s for s in t['supplemental_contexts'] if s['id']=='TSA-S06')['case_refs']=[dict(catalog='owner_cases',json_pointer='/14',id='TUN-015')]
  elif mutation=='invent-capture-UTC':t['source']['capture_utc']='2026-10-19T00:00:00Z'
  elif mutation=='erase-Custom-persistence':next(f for f in t['assessments'] if f['block']=='TUN:B046')['disposition']=STATUS['G']
  elif mutation=='choose-collision-survivor':next(f for f in t['assessments'] if f['block']=='TUN:B017')['disposition']=STATUS['R']
  try:guards(t)
  except AssertionError:rejected+=1
  else:raise AssertionError('accepted '+mutation)
 assert rejected==11
 parse=runpy.run_path(str(P.parent/'clip-view-source-audit/source_parser.py'))['extract'];b,r=parse('<div id="chapter_content"><h1 id="a">Root</h1><p>Ref. Pitch/Freq is a label. Keep 1.1.1.</p><h2 id="b">Settings</h2><ul><li>Only after valid input.</li></ul><img alt="" src="not-opened"><figcaption>Label.</figcaption></div>','FIX')
 assert [x['kind'] for x in b]==['h1','p','h2','li'] and b[-1]['heading_context'][-1]['anchor']=='b' and b[1]['text']=='Ref. Pitch/Freq is a label. Keep 1.1.1.' and [x['kind'] for x in r]==['image','caption']
 if writing:(P/'audit.json').write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n')
 else:
  assert load(P/'audit.json')==a,'exact reproduction'
  if seal.exists():
   manifest=load(seal);assert {str(f.relative_to(P)) for f in P.rglob('*') if f.is_file()}==set(manifest['files'])|{'manifest.json'}
   for n,r in manifest['files'].items():pin(P/n,r)
   assert manifest['summary']==a['summary']
  for f in P.rglob('*'):
   if f.is_file():
    if f.suffix=='.json':load(f)
    result=subprocess.run(['git','diff','--no-index','--check','/dev/null',str(f)],capture_output=True,text=True);assert result.returncode in (0,1) and not result.stdout and not result.stderr,(str(f),result.stdout,result.stderr)
  for dest in re.findall(r'\]\(([^)]+)\)',(P/'README.md').read_text()):
   if not re.match(r'^[A-Za-z]+:',dest):assert (P/dest.split('#')[0]).is_file(),dest
  assert before=={str(f):dg(f) for f in P.rglob('*') if f.is_file()}
 assert watched=={r['path']:dg(ROOT/r['path']) for r in inputs}
 print(json.dumps(dict(status='pass',sealed=seal.exists(),summary=a['summary'],negative_fixtures=rejected,retained_positive_contexts=16,parser_fixture=True,all_inputs_unchanged=True,packet_unchanged=not writing,writes=writing,original_runtime_network_candidate=False),indent=2))
if __name__=='__main__':main()
