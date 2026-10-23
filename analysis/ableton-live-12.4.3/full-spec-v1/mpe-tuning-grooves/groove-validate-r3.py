"""Read-only current Groove checks; old combined packet/checkers remain history."""
from pathlib import Path
from hashlib import sha256
from copy import deepcopy
from collections import Counter
import ast,json,re,runpy,subprocess,sys
P=Path(__file__).resolve().parent;ROOT=P.parents[3];A=P.parent/'groove-source-audit'
load=lambda f:json.loads(f.read_text())
def dg(f):
 b=f.read_bytes();return dict(bytes=len(b),sha256=sha256(b).hexdigest())
def pin(f,p):assert dg(f)=={k:p[k] for k in ['bytes','sha256']},str(f)
def tree():return {str(f.relative_to(P)):dg(f) for f in P.rglob('*') if f.is_file()}
def ptr(v,s):
 for k in s.split('/')[1:]:v=v[int(k)] if isinstance(v,list) else v[k.replace('~1','/').replace('~0','~')]
 return v
def check(req,cases,ledger,fixture,oldreq):
 old=[c for c in load(P/'cases.json') if c['id'].startswith('GRV-')]
 assert len(req)==14 and len(cases)==34 and cases[:24]==old
 assert len({c['id'] for c in cases})==34
 assert [c['id'] for c in cases[24:]]==[f'GRV-{i:03}' for i in range(25,35)]
 assert [i for i,(a,b) in enumerate(zip(oldreq,req)) if a!=b]==[0,9,13]
 assert {r['id'] for r in req}=={r['id'] for r in oldreq}
 assert 'Clip Groove chooser' in req[0]['contract'] and 'Groove Pool' in req[0]['contract']
 assert 'positive velocity values' in req[9]['contract'] and 'overwriting a volume clip envelope already' in req[9]['contract']
 assert 'double-clicking' in req[13]['contract'] and 'pressing Enter' in req[13]['contract'] and 'Groove Pool' in req[13]['contract']
 assert ['CV:B062' in req[0]['evidence'],'CV:B064' in req[9]['evidence'],'CV:B063' in req[13]['evidence']]==[True,True,True]
 assert Counter(c['documentary_grade'] for c in cases)=={'D12':23,'U':11}
 for c in cases:assert c['target_build_grade']=='U' and c['execution']=='unexecuted'
 ids={r['id'] for r in req};audit=load(A/'audit.json')
 for c in cases[24:]:
  assert c['requirement'] in ids and set(c.get('additional_requirements',[]))<=ids
  assert c['expected'] is c['comparator'] is c['actual_expected'] is c['actual_comparison'] is None
  assert c['source_claim'] and c['source_context'] and c['action']
  for x in c['source_context']:
   row=ptr(audit,x['json_pointer']);actual=row.get('id') or row['row']['id'];assert actual==x['id']
   assert x['catalog']=='../groove-source-audit/audit.json'
 assert sum(c['documentary_comparator'] is None for c in cases[24:])==3
 byid={c['id']:c for c in cases}
 for caseid,sourceid,index in [('GRV-032','CV:B064',2),('GRV-033','CV:B062',0),('GRV-034','CV:B063',1)]:
  external=[x for x in byid[caseid]['source_context'] if x['json_pointer'].startswith('/external_contexts/')]
  assert [(x['id'],x['json_pointer']) for x in external]==[(sourceid,f'/external_contexts/{index}')]
 for n in [27,28,29]:assert byid[f'GRV-{n:03}']['documentary_expected'] is byid[f'GRV-{n:03}']['documentary_comparator'] is None
 overwrite=byid['GRV-032']['action']
 assert 'independently confirmed positive velocity influence' in overwrite and 'nonflat pre-existing clip-volume envelope' in overwrite
 assert 'Velocity0' in overwrite and 'not this' in overwrite
 assert 'genuinely confirmed groove timing effect' in byid['GRV-029']['action'] and 'unmuted nonzero' in byid['GRV-029']['action']
 assert 'genuinely successful ordinary operations' in byid['GRV-026']['action']
 assert 'double-click' in byid['GRV-034']['action'] and 'actually press Enter' in byid['GRV-034']['action'] and 'Groove Pool entry identities' in byid['GRV-034']['action']
 assert [g['group'] for g in ledger]==[f'GSA-G{i:02}' for i in range(1,11)]
 assert Counter(g['disposition'] for g in ledger)=={'bounded-local-source-context':9,'research-recommendation-only':1}
 for g in ledger:
  assert g['complete'] is False and g['coverage_credit']==0
  for x in g['case_pointers']:
   assert x['catalog']=='groove-cases-r3.json';case=ptr(cases,x['json_pointer']);assert case['id']==x['id'] and case['audit_group']==g['group']
 assert ledger[8]['case_pointers']==[] and not any(c['audit_group']=='GSA-G09' for c in cases[24:])
 assert 'no guaranteed distinct realization' in fixture['random']
 assert fixture['actual_expected'] is fixture['actual_comparison'] is None and fixture['target']=='U' and fixture['executed'] is False
def main():
 assert sys.dont_write_bytecode and sys.argv[1:]==['--check']
 before=tree();inputs=load(P/'groove-inputs-r3.json');assert len(inputs)==len({p['path'] for p in inputs})==28
 ebefore={p['path']:dg(ROOT/p['path']) for p in inputs}
 for p in inputs:pin(ROOT/p['path'],p)
 prior=load(P/'groove-prior-files-r3.json');assert len(prior)==61
 for n,p in prior.items():pin(P/n,p)
 assert dg(P/'manifest-author-r2.json')['sha256']=='a93a5dca90cf0aa83dd712beaea955549dda093a89668d4294335a45c0e8748a'
 assert dg(A/'manifest-r2.json')['sha256']=='848a449e4b65d06e8d61649ca330ffac69955ef877e2adbe5f8ef03013df6f47'
 assert load(P.parent/'reviews/groove-source-audit-review-final.json')['disposition']=='approved-partial-source-audit'
 # Reconstruct exactly the reviewed association view as data; no old check main.
 original=load(A/'audit.json');effective=deepcopy(original);patches=load(A/'correction-r2.json')['patches']
 assert [x['pointer'] for x in patches]==['/assessments/27/requirement_refs','/assessments/27/case_refs']
 for x in patches:
  field=x['pointer'].rsplit('/',1)[1];assert effective['assessments'][27][field]==x['before'] and x['after']==[];effective['assessments'][27][field]=x['after']
 assert effective['assessments'][27]['external_context_refs']==original['assessments'][27]['external_context_refs']
 raw=(ROOT/original['source']['file']['path']).read_text();pin(ROOT/original['source']['file']['path'],original['source']['file'])
 parsed,resources=runpy.run_path(str(P.parent/'clip-view-source-audit/source_parser.py'))['extract'](raw,'GRV')
 assert parsed==original['blocks'] and len(parsed)==32 and len(resources)==17
 for b in parsed:assert raw[b['raw_start']:b['raw_end']]==b['raw_html']
 clip=(ROOT/'analysis/ableton-live-12.4.3/full-spec-v1/clip-view/manual-clip-view-2026-10-19.html').read_text()
 for e in original['external_contexts'][:3]:
  row=e['row'];assert clip[row['raw_start']:row['raw_end']]==row['raw_html']
 author=runpy.run_path(str(P/'groove-author-r3.py'));built=author['build']()
 for n,data in built.items():assert load(P/n)==data,n
 req,cases,ledger,fixture=(built[n] for n in ['groove-requirements-r3.json','groove-cases-r3.json','groove-adoption-r3.json','groove-fixtures-r3.json'])
 oldreq=author['original_requirements']();check(req,cases,ledger,fixture,oldreq)
 assert len(load(P/'cases.json'))==83
 assert Counter(c['id'].split('-')[0] for c in load(P/'cases.json'))=={'MPE':27,'TUN':32,'GRV':24}
 for beforefile,provider in [('groove-spec-before-r3.md','groove-workflows-author-r2.md'),('groove-research-before-r3.md','mpe-tuning-grooves-author-r2.md')]:assert (P/beforefile).read_bytes()==(P/provider).read_bytes()
 for snap,canonical in [('groove-workflows-author-r3.md','wiki/specs/groove-workflows.md'),('groove-research-author-r3.md','wiki/research/mpe-tuning-grooves.md')]:
  assert (P/snap).read_bytes()==(ROOT/canonical).read_bytes();assert 'revision: 3' in (P/snap).read_text() and '**AS-OF AUTHOR FREEZE:**' in (P/snap).read_text()
 spec=(P/'groove-workflows-author-r3.md').read_text()
 for r in req:assert '| '+' | '.join(r[k] for k in ['id','preconditions','contract','evidence'])+' |' in spec
 module=ast.parse((ROOT/'tools/spec_browser.py').read_text());defs=[x for x in module.body if isinstance(x,ast.FunctionDef) and x.name in ['anchor','frontmatter','cells','spec_rows']];assert len(defs)==4
 env={'re':re};exec(compile(ast.Module(body=defs,type_ignores=[]),'four-analyst-browser-functions','exec'),env)
 browser=env['spec_rows'](Path('groove-workflows.md'),spec);assert len(browser)==14 and {x['id'] for x in browser}=={x['id'] for x in req}
 impact=load(P/'groove-consumer-impact-r3.json');assert len(impact['records'])==30 and len({x['consumer'] for x in impact['records']})==21
 for x in impact['records']:assert dg(P/x['historical_snapshot'])['sha256']==x['literal_sha256']
 # Do not turn historical consumer or mutable MPE/Tuning canonical metadata into gates.
 assert impact['consumers_modified'] is impact['historical_replay'] is False
 for v in impact['other_canonicals_asof'].values():pin(P.parent/v['provider'],v)
 rejected=0
 for mutation in ['old-case-change','wrong-Clip-source','missing-positive-velocity','missing-prior-envelope','missing-Warp-effect','invented-actual','Random-guarantee']:
  rr,cc,ll,ff=deepcopy(req),deepcopy(cases),deepcopy(ledger),deepcopy(fixture)
  if mutation=='old-case-change':cc[9]['expected']='invented result'
  elif mutation=='wrong-Clip-source':cc[-3]['source_context'][-1].update(json_pointer='/external_contexts/1',id='CV:B063')
  elif mutation=='missing-positive-velocity':cc[-3]['action']=cc[-3]['action'].replace('independently confirmed positive velocity influence','only a nonzero flag')
  elif mutation=='missing-prior-envelope':cc[-3]['action']=cc[-3]['action'].replace('nonflat pre-existing clip-volume envelope','unknown envelope')
  elif mutation=='missing-Warp-effect':cc[-6]['action']=cc[-6]['action'].replace('genuinely confirmed groove timing effect','Warp enabled flag')
  elif mutation=='invented-actual':cc[-1]['actual_expected']='pass'
  elif mutation=='Random-guarantee':ff['random']='Require distinct realization every trial'
  try:check(rr,cc,ll,ff,oldreq)
  except AssertionError:rejected+=1
  else:raise AssertionError('mutation accepted '+mutation)
 assert rejected==7
 links=0
 for f in [ROOT/'wiki/specs/groove-workflows.md',ROOT/'wiki/research/mpe-tuning-grooves.md',P/'README-groove-r3.md']:
  for dest in re.findall(r'\]\(([^)]+)\)',f.read_text()):
   if re.match(r'^[A-Za-z]+:',dest):continue
   path,_,frag=dest.partition('#');target=(f.parent/path).resolve() if path else f
   assert target.is_file() or target==P/'groove-manifest-author-r3.json' and not target.exists(),(f,dest)
   if frag and target.suffix=='.md':assert frag in {env['anchor'](x.lstrip('#')) for x in target.read_text().splitlines() if x.startswith('#')},(f,dest)
   links+=1
 for n in before:
  if n in prior or n in ['groove-spec-before-r3.md','groove-research-before-r3.md']:continue
  f=P/n
  if f.suffix=='.json':load(f)
  o=subprocess.run(['git','diff','--no-index','--check','/dev/null',str(f)],capture_output=True,text=True);assert o.returncode in (0,1) and not o.stdout and not o.stderr,(n,o.stdout,o.stderr)
 seal=P/'groove-manifest-author-r3.json'
 if seal.exists():
  m=load(seal);assert set(before)==set(m['files'])|{seal.name}
  for n,pinrow in m['files'].items():pin(P/n,pinrow)
 assert tree()==before and ebefore=={p['path']:dg(ROOT/p['path']) for p in inputs}
 print(json.dumps(dict(status='pass',sealed=seal.exists(),Groove_requirements=14,changed_rows=[1,10,14],unchanged_rows=11,Groove_cases=34,old_Groove_records_verbatim=24,shared_original_records_verbatim=83,MPE_records=27,Tuning_records=32,new_cases=10,Groove_D12_contexts=23,Groove_U=11,new_named_documentary=7,new_documentary_null=3,all_actual_null_U_unexecuted=True,source_blocks=32,source_resources=17,input_pins=28,old_files_preserved=61,browser_exact_ids=14,links=links,mutations=rejected,bounded_groups=9,research_only_groups=1,historical_consumer_occurrences=30,historical_consumer_files=21,historical_replay=False,packet_inputs_unchanged=True,writes=False,runtime=False,complete_topics=0),indent=2))
if __name__=='__main__':main()
