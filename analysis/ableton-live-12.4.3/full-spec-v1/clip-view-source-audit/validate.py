"""Read-only finite source/association/baseline/oracle checks; never rewrites reports."""
from pathlib import Path
from hashlib import sha256
from copy import deepcopy
from collections import Counter
import contextlib,io,json,re,runpy,subprocess,sys
P=Path(__file__).resolve().parent;ROOT=P.parents[3];K=P.parent/'clip-view'
load=lambda p:json.loads(p.read_text())
def dg(p):
 b=p.read_bytes();return dict(bytes=len(b),sha256=sha256(b).hexdigest())
def pin(p,r):assert dg(p)=={k:r[k] for k in ['bytes','sha256']},str(p)
def tree():return {str(p.relative_to(P)):dg(p) for p in P.rglob('*') if p.is_file()}
def pointer(value,ptr):
 for part in ptr.split('/')[1:] if ptr else []:value=value[int(part)] if isinstance(value,list) else value[part.replace('~1','/').replace('~0','~')]
 return value

def check_claims(claims,blocks,derive):
 byblock={b['id']:[] for b in blocks};plan=load(P/'claim-plan.json')
 assert len({c['id'] for c in claims})==len(claims)
 for c in claims:
  assert c['block'] in byblock;byblock[c['block']].append(c)
  b=pointer(blocks,c['block_json_pointer']);assert b['id']==c['block']
  a,z=c['text_span'];assert c['source_excerpt']==b['text'][a:z] and c['excerpt_sha256']==sha256(c['source_excerpt'].encode()).hexdigest()
  assert c['source_locator']['raw_start']==b['raw_start'] and c['source_locator']['raw_end']==b['raw_end']
  assert c['source_locator']['heading_context']==b['heading_context']
  if b['kind'].startswith('h'):assert c['requirements']==c['cases']==[]
  else:
   row=plan[b['id']][c['sentence']]
   assert c['requirements']==[derive['ref']('requirements',i) for i in row['requirements']]
   assert c['cases']==[derive['ref']('cases',i) for i in row['cases']]
   assert c['disposition']==derive['STATUS'][row['disposition']] and c['assessment']==row['assessment']
  for ref in c['requirements']+c['cases']:
   quoted=pointer(load(ROOT/ref['catalog']),ref['json_pointer'])
   assert quoted==ref['scoped_predicate'] and sha256(quoted.encode()).hexdigest()==ref['value_sha256']
   assert pointer(load(ROOT/ref['catalog']),ref['json_pointer'].rsplit('/',1)[0])['id']==ref['id']
  assert c['actual_expected'] is c['actual_comparison'] is None and c['target']=='U'
  assert c['executed'] is c['complete'] is False and c['behavioral_coverage_credit']==0
 for b in blocks:
  seen=set()
  for c in byblock[b['id']]:seen.update(range(*c['text_span']))
  assert all(i in seen for i,x in enumerate(b['text']) if not x.isspace()),b['id']

def check_proposals(proposals):
 assert [g['id'] for g in proposals]==[f'CVA-G{i:02}' for i in range(1,25)]
 for g in proposals:
  assert all(g[k] is None for k in ['documentary_expected','documentary_comparison','expected','comparison'])
  assert g['target']=='U' and g['executed'] is g['complete'] is False and g['behavioral_coverage_credit']==0
  guard=g['positive_guard']
  assert all(guard[k] is True for k in ['admitted_exact_feature_mode_history_and_focus','independently_valid_owned_nonempty_source','active_unmuted_nonzero_output_where_applicable','paired_successful_functioning_baseline_before_negative','missing_or_failed_prerequisite_stays_U'])
  assert guard['fixtures_or_runtime_results_supplied'] is False
  assert guard['requires_functioning_scroll_before_edit']==(g['id']=='CVA-G15')
  assert g['claim_ids'] and g['proposed_case_action'] and g['limits']


def main():
 assert sys.dont_write_bytecode and len(sys.argv)==1,'Use python -B validate.py without arguments'
 before=tree();inputs=load(P/'input-pins.json');assert len(inputs)==len({r['path'] for r in inputs})==26
 external_before={r['path']:dg(ROOT/r['path']) for r in inputs}
 for r in inputs:pin(ROOT/r['path'],r)
 assert dg(K/'manifest-author-r1.json')['sha256']=='8b4add6a3870f93c5f8f75c94663c10702510664a2c1e92abd9dd4e3afe923e9'
 manifest=load(K/'manifest-author-r1.json');assert len(manifest['payloads'])==14
 for row in manifest['payloads']:pin(K/row['file'],row)
 review=load(K.parent/'reviews/clip-view-workflows-review.json');assert review['disposition']=='approved-as-partial-analyst-draft' and review['findings']==[]
 for r in load(P/'owner-context.json'):
  pin(P/r['snapshot'],r);pin(ROOT/r['provider'],r)
 for r in load(P/'owner-routes.json'):pin(P/r['snapshot'],r) # No future live canonical assertion.
 external=load(P/'external-contexts.json');assert len(external)==15
 for r in external:
  row=pointer(load(ROOT/r['catalog']),r['json_pointer']);assert row==r['row'] and row['id']==r['id']
  assert sha256(json.dumps(row,sort_keys=True,ensure_ascii=False).encode()).hexdigest()==r['row_sha256']
 derive=runpy.run_path(str(P/'derive.py'));built=derive['build']();assert len(built)==7
 for name,value in built.items():assert load(P/name)==value,name
 blocks,claims,proposals=built['source-blocks.json'],built['claims.json'],built['proposed-deltas-derived.json']
 assert len(blocks)==180 and len(claims)==309 and Counter(b['kind'] for b in blocks)=={'p':137,'h1':1,'h2':14,'h3':18,'h4':4,'li':6}
 check_claims(claims,blocks,derive);check_proposals(proposals)
 source=load(K/'source.json');raw=(K/source['file']).read_text()
 for b in blocks:
  assert raw[b['raw_start']:b['raw_end']]==b['raw_html']
  assert raw.count('\n',0,b['raw_start'])+1==b['html_line'] and b['html_column']==b['raw_start']-(raw.rfind('\n',0,b['raw_start'])+1)
 for r in built['resources.json']:
  a=r['raw_start'];z=raw.index('>',a)+1;assert sha256(raw[a:z].encode()).hexdigest()==r['starttag_sha256']
  assert r['pixels_or_destination_inspected'] is r['complete'] is False
 assert len(built['resources.json'])==128
 # Every exact old row appears in reverse index, including explicit U operational cases.
 for kind,count in [('requirements',54),('cases',62)]:
  rows=load(K/(kind+'.json'));back=built['existing-catalog-reconciliation.json'][kind]
  assert len(rows)==len(back)==count and [r['id'] for r in rows]==[r['id'] for r in back]
  for i,(row,r) in enumerate(zip(rows,back)):
   assert pointer(load(ROOT/r['catalog']),r['json_pointer'])==row and r['json_pointer']==f'/{i}'
   assert r['source_facets']==[c['id'] for c in claims if any(x['id']==r['id'] for x in c[kind])]
   assert r['complete'] is False and r['target']=='U'
 for c in load(K/'cases.json'):
  assert c['expected'] is c['comparison'] is None and c['executed'] is False and c['target_grade']=='U'
 for q in load(P/'source-questions.json'):
  assert q['state'] in ['U','unresolved-source-context']
  assert set(q['source_blocks'])<={b['id'] for b in blocks}
  assert all(0<=i<len(external) for i in q['external_contexts'])
 # Decimal text, source hierarchy, tables and resource exclusions independently exercised.
 fixtures=load(P/'fixtures.json');parse=runpy.run_path(str(P/'source_parser.py'))['extract'];tiny,rs=parse(fixtures['parser_fixture'],'TEST')
 assert Counter(b['kind'] for b in tiny)=={'h1':1,'h2':1,'p':1,'li':1,'tr':2}
 assert [tiny[1]['text'][a:z] for a,z in derive['spans'](tiny[1]['text'])]==['Set 1.1.1 Here.','Next sentence.']
 assert tiny[-1]['heading_context'][-1]['anchor']=='child' and [r['kind'] for r in rs]==['image','caption'] and rs[-1]['text']=='Label only.'
 rejected=0
 for mutation in fixtures['negative_mutations']:
  cc,pp=deepcopy(claims),deepcopy(proposals)
  if mutation=='omit-source-block':cc=[c for c in cc if c['block']!='CV:B003']
  elif mutation=='alter-quote':cc[1]['source_excerpt']+=' changed'
  elif mutation=='misassociate-case':next(c for c in cc if c['block']=='CV:B142')['cases']=[derive['ref']('cases',1)]
  elif mutation=='remove-productive-follow-baseline':pp[14]['positive_guard']['requires_functioning_scroll_before_edit']=False
  elif mutation=='promote-actual-oracle':pp[0]['expected']='invented result'
  else:raise AssertionError(mutation)
  try:check_claims(cc,blocks,derive);check_proposals(pp)
  except AssertionError:rejected+=1
  else:raise AssertionError('Mutation accepted: '+mutation)
 assert rejected==5
 if (P/'manifest.json').exists():
  current=load(P/'manifest.json');assert set(before)==set(current['files'])|{'manifest.json'}
  for name,r in current['files'].items():pin(P/name,r)
  assert current['summary']==built['summary.json']
 links=0
 for target in re.findall(r'\]\(([^)]+)\)',(P/'README.md').read_text()):
  if re.match(r'^[A-Za-z]+:',target):continue
  assert (P/target.split('#')[0]).is_file(),target;links+=1
 authored=[p for p in P.rglob('*') if p.is_file() and 'owner-snapshots' not in p.parts and p.name not in ['spec-asof-r1.md','research-asof-r1.md']]
 for p in authored:
  if p.suffix=='.json':load(p)
  r=subprocess.run(['git','diff','--no-index','--check','/dev/null',str(p)],capture_output=True,text=True)
  assert r.returncode in (0,1) and not r.stdout and not r.stderr,(str(p),r.stdout,r.stderr)
 assert tree()==before and external_before=={r['path']:dg(ROOT/r['path']) for r in inputs}
 print(json.dumps(dict(status='pass',sealed=(P/'manifest.json').exists(),scope='Retained source/pointer/guard integrity only; independent semantic audit review pending',summary=built['summary.json'],input_pins=len(inputs),original_owner_payloads=14,asof_primary_snapshots=2,external_route_snapshots=13,selected_external_records=15,qualified_contract_action_pointers=sum(len(c['requirements'])+len(c['cases']) for c in claims),negative_fixtures=rejected,parser_decimal_table_hierarchy_resource_fixture=True,README_links=links,authored_whitespace_files=len(authored),packet_and_inputs_unchanged=True,writes=False,original_runtime_network_hardware_candidate_execution=False),indent=2))
if __name__=='__main__':main()
