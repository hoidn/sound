"""Read-only current MPE successor checks; no historical checker replay."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
from copy import deepcopy
import ast,json,re,runpy,subprocess,sys
P=Path(__file__).resolve().parent;ROOT=P.parents[3];A=P.parent/'mpe-source-audit'
load=lambda p:json.loads(p.read_text())
def dg(p):
 b=p.read_bytes();return dict(bytes=len(b),sha256=sha256(b).hexdigest())
def pin(p,r):assert dg(p)=={k:r[k] for k in ['bytes','sha256']},str(p)
def tree():return {str(p.relative_to(P)):dg(p) for p in P.rglob('*') if p.is_file()}
def ptr(v,s):
 for k in s.split('/')[1:]:v=v[int(k)] if isinstance(v,list) else v[k.replace('~1','/').replace('~0','~')]
 return v
def check(req,cases,ledger,fixture,oldreq):
 old=[c for c in load(P/'cases.json') if c['id'].startswith('MPE-')]
 assert len(req)==18 and len(cases)==50 and cases[:27]==old
 assert [r['id'] for r in req]==[f'REQ-MPE-{i:03}' for i in range(1,19)]
 assert [c['id'] for c in cases]==[f'MPE-{i:03}' for i in range(1,51)]
 assert [i+1 for i in range(18) if oldreq[i]!=req[i]]==[1,4,6,7,9,11,12,14,15]
 assert Counter(c['documentary_grade'] for c in cases)=={'D12':39,'U':11}
 for c in cases:assert c['target_build_grade']=='U' and c['execution']=='unexecuted'
 blocks=load(A/'source-blocks.json');byid={c['id']:c for c in cases}
 for c in cases[27:]:
  assert c['expected'] is c['comparator'] is c['actual_expected'] is c['actual_comparison'] is None
  assert c['source_claim'] and c['action'] and c['requirement'] in {r['id'] for r in req}
  for ref in c['source_context']:
   assert ref['catalog']=='../mpe-source-audit/source-blocks.json'
   assert ptr(blocks,ref['json_pointer'])['id']==ref['id']
  for ref in c['related_owner_context']:
   assert ref['catalog']=='../mpe-source-audit/selected-owner-contexts.json'
   selected=ptr(load(A/'selected-owner-contexts.json'),ref['json_pointer']);assert selected['id']==ref['id']
   if selected['kind']=='JSON':assert ptr(load(ROOT/selected['catalog']),selected['json_pointer'])==selected['quoted_scoped_predicate']
   else:
    a,z=selected['text_span'];assert (A/selected['snapshot']).read_text()[a:z]==selected['quoted_scoped_predicate']
  if c['documentary_expected'] is None:assert c['documentary_comparator'] is None
 assert sum(c['documentary_expected'] is not None for c in cases[27:])==10
 assert [c['id'] for c in cases[27:] if c['documentary_grade']=='U']==['MPE-029','MPE-048']
 for n in [29,33,34,35,36,37,38,39,40,41,45,47,48]:
  assert byid[f'MPE-{n:03}']['documentary_expected'] is byid[f'MPE-{n:03}']['documentary_comparator'] is None
 expected_sources={28:[3,4],29:[3,5],30:[10,11,12],31:[6,7,9,15,16],32:[17,18,19,21],33:[21],34:[20,22],35:[25,26,27],36:[23,24],37:[29],38:[30],39:[31,32],40:[33],41:[35],42:[34],43:[36],44:[38,39],45:[40,41],46:[13],47:[46],48:[45,47],49:[50,51,52,55,56,57],50:[60,61,62,63,64,65,66]}
 for n,nums in expected_sources.items():assert [(x['id'],x['json_pointer']) for x in byid[f'MPE-{n:03}']['source_context']]==[(f'MPE-B{i:03}',f'/{i-1}') for i in nums]
 assert 'before selecting it' in req[0]['preconditions']
 assert 'a,b,c' in byid['MPE-033']['action'] and '20/40/30' in byid['MPE-033']['action']
 assert 'genuinely successful nonzero ordinary vertical edit' in byid['MPE-035']['action']
 assert 'Explicitly grid OFF' in byid['MPE-040']['action'] and 'Alt Windows/Cmd Mac' in byid['MPE-040']['action']
 assert 'genuine visible over-note Pitch' in byid['MPE-042']['action'] and 'C3' in byid['MPE-042']['action']
 assert 'independently working productive per-note source/route baseline' in byid['MPE-046']['action']
 assert 'NOT the baseline' in byid['MPE-046']['action'] and 'lowest dot' in byid['MPE-046']['action']
 assert 'nonzero relevant modulation depth/gain and nonmuted positive output baseline' in byid['MPE-048']['action']
 assert 'enabled-default save/new-instance baseline' in byid['MPE-047']['action']
 assert 'Session and Arrangement' in byid['MPE-049']['action'] and 'reopen menu' in byid['MPE-049']['action']
 assert 'actually select an independently allowed note-channel count' in byid['MPE-050']['action']
 assert 'requires NO MPE hardware' in fixture['offline']
 assert 'not optional Pitch Bend lane/C3 resolution' in fixture['pitch_context']
 assert 'no universal ±48' in fixture['matching']
 assert fixture['actual_expected'] is fixture['actual_comparison'] is None and fixture['target']=='U' and fixture['executed'] is False
 assert [g['group'] for g in ledger]==[f'MPA-G{i:02}' for i in range(1,14)]
 for g in ledger:
  assert g['case_pointers'] and g['retained_unknowns'] and g['complete'] is False and g['coverage_credit']==0
  for ref in g['case_pointers']:assert ref['catalog']=='mpe-cases-r3.json' and ptr(cases,ref['json_pointer'])['id']==ref['id'] and ptr(cases,ref['json_pointer'])['audit_group']==g['group']
 # Actual historical action subsets, not facts borrowed from expected strings.
 assert 'admissible c' in old[4]['action'] and 'values a and b' in old[4]['setup']
 assert 'Shift-drag' in old[5]['action'] and 'save/reopen' in old[6]['action']
 assert 'x2' in old[9]['action'] and old[13]['action']=='Save its enabled MPE default; create instance from default.'
 assert 'each output route' in old[14]['action'] and 'one lower zone, one upper' in old[15]['action'] and '3..8' in old[16]['action']
def main():
 assert sys.dont_write_bytecode and sys.argv[1:]==['--check']
 before=tree();inputs=load(P/'mpe-inputs-r3.json');assert len(inputs)==len({r['path'] for r in inputs})==40
 watch={r['path']:dg(ROOT/r['path']) for r in inputs}
 for r in inputs:pin(ROOT/r['path'],r)
 prior=load(P/'mpe-prior-files-r3.json');assert len(prior)==79
 for n,r in prior.items():pin(P/n,r)
 assert dg(A/'manifest.json')['sha256']=='f192b181c9845bcb3d899ef48e084144f9352c5679d7a567a13648713632795d'
 assert load(P.parent/'reviews/mpe-source-audit-review.json')['disposition']=='approved-as-partial-source-audit'
 assert dg(P.parent/'reviews/mpe-source-audit-review.json')['sha256']=='1f5371c1c3f45b455335b49cfa5e9d05c3ca2a9649cff7a0bcbaa312f5f0667b'
 assert dg(P.parent/'reviews/groove-owner-r3-review.json')['sha256']=='3379b533e81c5655c4caf31b78246582003cbc6b29baa3873c1c2f7eb1049ef4'
 source=load(A/'source-context.json');pin(ROOT/source['path'],source)
 raw=(ROOT/source['path']).read_text();blocks,resources=runpy.run_path(str(A/'source_parser.py'))['extract'](raw,'MPE')
 assert blocks==load(A/'source-blocks.json') and len(blocks)==66 and len(resources)==28
 for b in blocks:assert raw[b['raw_start']:b['raw_end']]==b['raw_html']
 faq=load(A/'faq-context.json');a,z=faq['raw_span'];assert (ROOT/faq['path']).read_text()[a:z]==faq['exact_excerpt'];assert sha256(faq['exact_excerpt'].encode()).hexdigest()==faq['excerpt_sha256']
 assert source['capture_utc'] is faq['capture_utc'] is None
 author=runpy.run_path(str(P/'mpe-author-r3.py'));built=author['build']()
 for n,data in built.items():assert load(P/n)==data,n
 req,cases,ledger,fixture=(built[n] for n in ['mpe-requirements-r3.json','mpe-cases-r3.json','mpe-adoption-r3.json','mpe-fixtures-r3.json'])
 oldreq=author['original_requirements']();check(req,cases,ledger,fixture,oldreq)
 assert len(load(P/'cases.json'))==83 and len(load(P/'groove-cases-r3.json'))==34
 union=cases+[c for c in load(P/'cases.json') if c['id'].startswith('TUN-')]+load(P/'groove-cases-r3.json')
 assert len(union)==len({c['id'] for c in union})==116
 assert (P/'mpe-spec-before-r3.md').read_bytes()==(P/'mpe-workflows-author-r2.md').read_bytes()
 assert (P/'mpe-research-before-r3.md').read_bytes()==(P/'groove-research-author-r3.md').read_bytes()
 for snap,canonical,revision in [('mpe-workflows-author-r3.md','wiki/specs/mpe-workflows.md',3),('mpe-research-author-r3.md','wiki/research/mpe-tuning-grooves.md',4)]:
  assert (P/snap).read_bytes()==(ROOT/canonical).read_bytes()
  assert f'revision: {revision}\n' in (P/snap).read_text() and '**AS-OF AUTHOR FREEZE:**' in (P/snap).read_text()
 spec=(P/'mpe-workflows-author-r3.md').read_text()
 for r in req:assert '| '+' | '.join(r[k] for k in ['id','preconditions','contract','evidence'])+' |' in spec
 module=ast.parse((ROOT/'tools/spec_browser.py').read_text());defs=[x for x in module.body if isinstance(x,ast.FunctionDef) and x.name in ['anchor','frontmatter','cells','spec_rows']];assert len(defs)==4
 env={'re':re};exec(compile(ast.Module(body=defs,type_ignores=[]),'four-analyst-browser-functions','exec'),env)
 browser=env['spec_rows'](Path('mpe-workflows.md'),spec);assert len(browser)==18 and {x['id'] for x in browser}=={r['id'] for r in req}
 impact=load(P/'mpe-consumer-impact-r3.json');assert len(impact['records'])==23 and len(impact['consumer_identities'])==20
 assert len(impact['active_author_asof_excluded'])==1 and impact['consumers_modified'] is impact['historical_replay'] is False
 for x in impact['records']:assert dg(P/x['historical_snapshot'])['sha256']==x['literal_sha256']
 for canonical,x in impact['other_canonicals_asof'].items():pin(P/x['provider'],x) # immutable as-of providers, not future live canonical gates
 rejected=0
 for mutation in ['rewrite-old-admissible-value','wrong-meter-source','default-is-meter','erase-per-note-positive','erase-output-positive','hardware-for-offline','resolve-optional-lane','invent-numeric-oracle','enable-after-selection']:
  rr,cc,ll,ff=deepcopy(req),deepcopy(cases),deepcopy(ledger),deepcopy(fixture)
  if mutation=='rewrite-old-admissible-value':cc[4]['setup']='Values20/40/30 universal'
  elif mutation=='wrong-meter-source':cc[45]['source_context']=[dict(catalog='../mpe-source-audit/source-blocks.json',json_pointer='/45',id='MPE-B046')]
  elif mutation=='default-is-meter':cc[13]['action']='Save default and infer per-note meter proof'
  elif mutation=='erase-per-note-positive':cc[45]['action']=cc[45]['action'].replace('independently working productive per-note source/route baseline','only a generic activity indicator')
  elif mutation=='erase-output-positive':cc[47]['action']=cc[47]['action'].replace('nonzero relevant modulation depth/gain and nonmuted positive output baseline','an enabled flag')
  elif mutation=='hardware-for-offline':ff['offline']='Requires controller hardware for every clip edit'
  elif mutation=='resolve-optional-lane':ff['pitch_context']='Hidden overlay proves optional lane unavailable'
  elif mutation=='invent-numeric-oracle':cc[39]['documentary_expected']='All pitch values equal48'
  elif mutation=='enable-after-selection':rr[0]['preconditions']=rr[0]['preconditions'].replace('before selecting it','after selecting it')
  try:check(rr,cc,ll,ff,oldreq)
  except AssertionError:rejected+=1
  else:raise AssertionError('unsafe mutation accepted: '+mutation)
 assert rejected==9
 links=0
 for f in [ROOT/'wiki/specs/mpe-workflows.md',ROOT/'wiki/research/mpe-tuning-grooves.md',P/'README-mpe-r3.md']:
  for dest in re.findall(r'\]\(([^)]+)\)',f.read_text()):
   if re.match(r'^[A-Za-z]+:',dest):continue
   path,_,frag=dest.partition('#');target=(f.parent/path).resolve() if path else f
   assert target.is_file() or target==P/'mpe-manifest-author-r3.json' and not target.exists(),(f,dest)
   if frag and target.suffix=='.md':assert frag in {env['anchor'](line.lstrip('#')) for line in target.read_text().splitlines() if line.startswith('#')},(f,dest)
   links+=1
 for n in before:
  if n in prior or n in ['mpe-spec-before-r3.md','mpe-research-before-r3.md']:continue
  f=P/n
  if f.suffix=='.json':load(f)
  result=subprocess.run(['git','diff','--no-index','--check','/dev/null',str(f)],capture_output=True,text=True)
  assert result.returncode in (0,1) and not result.stdout and not result.stderr,(n,result.stdout,result.stderr)
 seal=P/'mpe-manifest-author-r3.json'
 if seal.exists():
  manifest=load(seal);assert set(before)==set(manifest['files'])|{seal.name}
  for n,r in manifest['files'].items():pin(P/n,r)
 assert tree()==before and watch=={r['path']:dg(ROOT/r['path']) for r in inputs}
 print(json.dumps(dict(status='pass',sealed=seal.exists(),requirements=18,refined_rows=[1,4,6,7,9,11,12,14,15],unchanged_rows=9,cases=50,old_MPE_verbatim=27,shared_original_verbatim=83,Groove_unchanged=34,Tuning_unchanged=32,logical_current_union=116,new_D12=21,new_U=2,MPE_D12=39,MPE_U=11,new_named_documentary=10,new_documentary_null=13,actual_all_null_U_unexecuted=True,source_blocks=66,source_resources=28,input_pins=40,old_files_preserved=79,browser_exact_ids=18,links=links,unsafe_mutations=rejected,bounded_groups=13,historical_consumer_occurrences=23,frozen_consumer_files=20,active_author_asof_files=1,historical_replay=False,packet_inputs_unchanged=True,writes=False,runtime=False,complete_topics=0),indent=2))
if __name__=='__main__':main()
