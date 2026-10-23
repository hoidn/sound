"""Read-only finite audit checks, including source, pointers and productive-baseline mutants."""
from pathlib import Path
from hashlib import sha256
from copy import deepcopy
from collections import Counter
import json,re,runpy,subprocess,sys
P=Path(__file__).resolve().parent;ROOT=P.parents[3];K=P.parent/'arrangement'
load=lambda p:json.loads(p.read_text())
def dg(p):
 b=p.read_bytes();return dict(bytes=len(b),sha256=sha256(b).hexdigest())
def pin(p,r):assert dg(p)=={k:r[k] for k in ['bytes','sha256']},str(p)
def tree():return {str(p.relative_to(P)):dg(p) for p in P.rglob('*') if p.is_file()}
def check_claims(claims,blocks,d):
 by={b['id']:[] for b in blocks};plan=load(P/'claim-plan.json');cat=load(P/'owner-catalog-asof.json');ext=load(P/'selected-owner-contexts.json');mapping=load(P/'external-reference-plan.json')
 assert len({x['id'] for x in claims})==len(claims)
 for c in claims:
  b=d['pointer'](blocks,c['block_pointer']);assert c['source_block']==b['id'];by[b['id']].append(c)
  a,z=c['text_span'];assert c['source_excerpt']==b['text'][a:z] and c['excerpt_sha256']==sha256(c['source_excerpt'].encode()).hexdigest()
  assert c['literal_paragraph_anchor']==b['attributes'].get('id')
  assert c['source_locator']=={k:b[k] for k in ['source_path','source_sha256','source_url','source_capture_utc','source_version','html_line','html_column','raw_start','raw_end','heading_context']}
  assert all(c['source_locator'][k] for k in ['source_capture_utc','source_version','heading_context'])
  if b['kind'].startswith('h'):assert not c['requirements'] and not c['cases']
  else:
   row=plan[b['id']][c['sentence']]
   assert c['requirements']==[d['ref'](cat,'requirements',n) for n in row['requirements']]
   assert c['cases']==[d['ref'](cat,'cases',n) for n in row['cases']]
   assert c['disposition']==d['STATUS'][row['disposition']] and c['assessment']==row['assessment'] and c['proposal_groups']==row['groups']
  for r in c['requirements']+c['cases']:
   assert d['pointer'](cat,r['json_pointer'])==r['quoted_scoped_predicate']
   assert sha256(r['quoted_scoped_predicate'].encode()).hexdigest()==r['text_sha256']
   assert d['pointer'](cat,r['json_pointer'].rsplit('/',1)[0])['id']==r['id']
  assert c['selected_external_contexts']==[dict(catalog='selected-owner-contexts.json',json_pointer=f'/{i}',id=ext[i]['id'],role='Actual selected quoted clause/action only; no family closure') for i in mapping.get(b['id'],[])]
  assert c['actual_expected'] is c['actual_comparison'] is None and c['target']=='U' and c['executed'] is c['complete'] is False and c['behavioral_coverage_credit']==0
 for b in blocks:
  covered=set()
  for c in by[b['id']]:covered.update(range(*c['text_span']))
  assert all(i in covered for i,ch in enumerate(b['text']) if not ch.isspace()),b['id']

def main():
 assert sys.dont_write_bytecode and len(sys.argv)==1,'python3 -B validate.py, no arguments'
 before=tree();pins=load(P/'input-pins.json');assert len(pins)==len({r['path'] for r in pins})==50
 watched={r['path']:dg(ROOT/r['path']) for r in pins}
 # Live canonical bytes are watched for accidental mutation, never required to equal an as-of pin.
 live=[ROOT/'wiki/specs/arrangement-editing.md',ROOT/'wiki/research/arrangement-editing.md'];live_before={str(p):dg(p) for p in live}
 for r in pins:pin(ROOT/r['path'],r)
 assert dg(K/'manifest.json')['sha256']=='6fe44f181360d1b2c186b394e671c673b3830bbb226fef208c4292ff655cb10f'
 old=load(K/'manifest.json');assert len(old['payloads'])==11
 for name,r in old['payloads'].items():pin(K/name,r)
 review=load(P.parent/'reviews/arrangement-review.json');assert review['status']=='approved-partial-documentation-domain-draft' and not review['findings']
 assert review['manifest_sha256']==dg(K/'manifest.json')['sha256'] and review['spec_sha256']==dg(P/'spec-asof-r1.md')['sha256']=='2ae6253a56b5e605acac83f7eb66e3f2b526404773ae2226eee0ca97b2c79d18'
 for sc in load(P/'source-context.json'):
  f=ROOT/sc['source'];m=load(ROOT/sc['metadata']);assert m['id']==sc['original_id'] and dg(f)['sha256']==m['files'][f.name]
  assert m['captured_utc'].startswith('2026-10-19T19:53:') and 'no patch/build' in m['version']
 for r in load(P/'owner-routes.json')+load(P/'owner-context.json'):pin(P/r['snapshot'],r)
 d=runpy.run_path(str(P/'derive.py'));ext=load(P/'selected-owner-contexts.json');assert len(ext)==109
 for r in ext:
  if r['kind']=='JSON':
   value=d['pointer'](load(ROOT/r['catalog']),r['json_pointer'])
   assert value==r['quoted_scoped_predicate'] and value['id']==r['id'] and sha256(json.dumps(value,sort_keys=True,ensure_ascii=False).encode()).hexdigest()==r['row_sha256']
  else:
   a,z=r['text_span'];v=(P/r['snapshot']).read_text()[a:z];assert v==r['quoted_scoped_predicate'] and sha256(v.encode()).hexdigest()==r['text_sha256']
 d=runpy.run_path(str(P/'derive.py'));built=d['build']();assert len(built)==8
 for name,data in built.items():assert load(P/name)==data,name
 blocks,claims,props=built['source-blocks.json'],built['claims.json'],load(P/'proposed-deltas.json')
 assert len(blocks)==186 and len(claims)==314 and Counter(b['kind'] for b in blocks)=={'h1':1,'h2':18,'h3':2,'p':108,'li':57}
 assert sum(len(b['text']) for b in blocks)==33957
 assert blocks[0]['id']=='ARR-B001' and blocks[163]['id']=='ARR-B164' and blocks[164]['id']=='CON-B030' and blocks[-1]['id']=='CON-B051'
 check_claims(claims,blocks,d);d['guard'](load(P/'claim-plan.json'),props)
 for b in blocks:
  raw=(ROOT/b['source_path']).read_text();assert raw[b['raw_start']:b['raw_end']]==b['raw_html']
  assert raw.count('\n',0,b['raw_start'])+1==b['html_line']
  assert b['html_column']==b['raw_start']-(raw.rfind('\n',0,b['raw_start'])+1)
 assert Counter(r['kind'] for r in built['resources.json'])=={'link':55,'image':42,'caption':40}
 for r in built['resources.json']:
  raw=(ROOT/r['source_path']).read_text();a=r['raw_start'];z=raw.index('>',a)+1;assert sha256(raw[a:z].encode()).hexdigest()==r['starttag_sha256']
  assert r['pixels_or_destination_inspected'] is r['complete'] is False
 inline=[r for r in built['resources.json'] if r['kind']=='image' and r['literal_container_block']=='ARR-B104'];assert len(inline)==2 and all(r['attributes']['alt']=='' for r in inline)
 cat=built['owner-catalog-asof.json'];assert set(re.findall(r'^### (REQ-ARRANGEMENT-\d{3})',(P/'spec-asof-r1.md').read_text(),re.M))=={r['id'] for r in cat['requirements']}
 for kind,n in [('requirements',35),('cases',65)]:
  assert len(cat[kind])==len(built['existing-catalog-reconciliation.json'][kind])==n
  for r in cat[kind]:
   a,z=r['markdown_span'];assert (P/r['snapshot']).read_text()[a:z]==r['original_markdown']
 for r in built['proposed-deltas-derived.json']:
  assert r['source_facets']==[c['id'] for c in claims if r['id'] in c['proposal_groups']]
  assert r['proposed_finite_action'] and r['retained_unknowns'] and r['existing_case_refs'] is not None
 for q in load(P/'source-questions.json'):
  assert q['state'] in ['U','unresolved-source-context','uninspected'] and set(q['source_blocks'])<={b['id'] for b in blocks}
  assert q['actual_expected'] is q['actual_comparison'] is None and q['target']=='U' and q['executed'] is q['complete'] is False
 fixtures=load(P/'fixtures.json');parse=runpy.run_path(str(P/'source_parser.py'))['extract'];tiny,rs=parse(fixtures['parser_fixture'],'T')
 assert Counter(b['kind'] for b in tiny)=={'h1':1,'h2':1,'p':2,'li':1,'tr':2}
 assert tiny[1]['text']=='Set 1.1.1 Here. Next sentence.' and tiny[4]['text']=='One | Two'
 assert tiny[-1]['text']=='Use or selectors.' and tiny[-1]['heading_context'][-1]['anchor']=='child' and len(rs)==3 and rs[-1]['text']=='Label only.'
 assert 'outside scope' not in str(tiny)
 rejected=0
 for name in fixtures['negative_mutations']:
  cc,pp,plan=deepcopy(claims),deepcopy(props),deepcopy(load(P/'claim-plan.json'))
  if name=='omit-source-block':cc=[c for c in cc if c['source_block']!='ARR-B040']
  elif name=='alter-source-quote':cc[1]['source_excerpt']+=' changed'
  elif name=='valid-but-wrong-case':next(c for c in cc if c['source_block']=='ARR-B070')['cases']=[d['ref'](cat,'cases',38)]
  elif name=='inverse-loop-command-as-covered':plan['ARR-B106'][0].update(cases=[37],requirements=[17],disposition='R')
  elif name=='weaken-Follow-positive-baseline':pp[3]['specific_positive_baseline']='Follow button visible with eligible clip'
  elif name=='remove-linked-fade-positive-baseline':pp[9]['same_start_fade_positive_before_different_start_negative']=False
  elif name=='remove-processed-return-baseline':pp[13]['genuine_nonzero_active_processed_return_before_bypass']=False
  elif name=='promote-actual-oracle':pp[0]['actual_expected']='invented host result'
  else:raise AssertionError(name)
  try:check_claims(cc,blocks,d);d['guard'](plan,pp)
  except AssertionError:rejected+=1
  else:raise AssertionError('Accepted negative mutation: '+name)
 assert rejected==8
 if (P/'manifest.json').exists():
  mf=load(P/'manifest.json');assert set(before)==set(mf['files'])|{'manifest.json'}
  for name,r in mf['files'].items():pin(P/name,r)
  assert mf['summary']==built['summary.json']
 links=0
 for target in re.findall(r'\]\(([^)]+)\)',(P/'README.md').read_text()):
  if re.match(r'^[A-Za-z]+:',target):continue
  assert (P/target.split('#')[0]).is_file(),target;links+=1
 # As-of verbatim wiki snapshots are checked by their sealed bytes, not reformatted.
 snapshots={r['snapshot'] for r in load(P/'owner-routes.json')}|{'spec-asof-r1.md','research-asof-r1.md'}
 authored=[p for p in P.rglob('*') if p.is_file() and p.name not in snapshots]
 for p in authored:
  if p.suffix=='.json':load(p)
  out=subprocess.run(['git','diff','--no-index','--check','/dev/null',str(p)],capture_output=True,text=True)
  assert out.returncode in (0,1) and not out.stdout and not out.stderr,(str(p),out.stdout,out.stderr)
 assert tree()==before and watched=={r['path']:dg(ROOT/r['path']) for r in pins} and live_before=={str(p):dg(p) for p in live}
 print(json.dumps(dict(status='pass',sealed=(P/'manifest.json').exists(),scope='Finite textual/pointer/null/positive-baseline integrity only; independent semantic review pending',summary=built['summary.json'],pins=len(pins),old_owner_payloads=11,selected_external_records=len(ext),primary_clause_action_pointers=sum(len(c['requirements'])+len(c['cases']) for c in claims),external_qualified_context_pointers=sum(len(c['selected_external_contexts']) for c in claims),negative_fixtures=rejected,parser_fixture=True,README_links=links,authored_whitespace_files=len(authored),watched_paths=len(before)+len(watched)+len(live),packet_inputs_current_canonicals_unchanged=True,writes=False,application_runtime_vendor_native_hardware_network_candidate_execution=False),indent=2))
if __name__=='__main__':main()
