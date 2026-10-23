"""Read-only finite MPE audit source/pointer/null/baseline checks; no vendor/runtime code."""
from pathlib import Path
from hashlib import sha256
from copy import deepcopy
from collections import Counter
import json,re,runpy,subprocess,sys
P=Path(__file__).resolve().parent;ROOT=P.parents[3];K=P.parent/'mpe-tuning-grooves'
load=lambda p:json.loads(p.read_text())
def dg(p):
 b=p.read_bytes();return dict(bytes=len(b),sha256=sha256(b).hexdigest())
def pin(p,r):assert dg(p)=={k:r[k] for k in ['bytes','sha256']},str(p)
def tree():return {str(p.relative_to(P)):dg(p) for p in P.rglob('*') if p.is_file()}
def check_claims(claims,blocks,d):
 by={b['id']:[] for b in blocks};plan=load(P/'claim-plan.json');cat=load(P/'owner-catalog-asof.json');ext=load(P/'selected-owner-contexts.json');mapping=load(P/'external-reference-plan.json');sc=load(P/'source-context.json')
 for c in claims:
  b=d['pointer'](blocks,c['block_pointer']);assert b['id']==c['source_block'];by[b['id']].append(c)
  a,z=c['text_span'];assert c['source_excerpt']==b['text'][a:z] and sha256(c['source_excerpt'].encode()).hexdigest()==c['excerpt_sha256']
  loc=c['source_locator'];assert loc['heading_context']==b['heading_context'] and loc['literal_anchor']==b['attributes'].get('id') and loc['raw_start']==b['raw_start'] and loc['raw_end']==b['raw_end'] and loc['html_line']==b['html_line'] and loc['html_column']==b['html_column']
  assert loc['capture_utc'] is None and loc['capture_date']==sc['capture_date'] and loc['source_sha256']==sc['sha256'] and loc['version']==sc['version']
  if b['kind'].startswith('h'):assert c['requirements']==c['cases']==[]
  else:
   r=plan[b['id']][c['sentence']];assert c['assessment']==r['assessment'] and c['disposition']==d['STATUS'][r['disposition']] and c['proposal_groups']==r['groups']
   for kind in ['requirements','cases']:assert c[kind]==[d['ref'](cat,kind,n) for n in r[kind]]
  for r in c['requirements']+c['cases']:
   value=d['pointer'](load(ROOT/r['catalog']),r['json_pointer']);assert value==r['quoted_scoped_predicate'] and value['id']==r['id']
  assert c['selected_external_contexts']==[dict(catalog='selected-owner-contexts.json',json_pointer=f'/{i}',id=ext[i]['id']) for i in mapping.get(b['id'],[])]
  assert c['actual_expected'] is c['actual_comparison'] is None and c['target']=='U' and c['executed'] is c['complete'] is False and c['coverage_credit']==0
 for b in blocks:
  covered=set()
  for c in by[b['id']]:covered.update(range(*c['text_span']))
  assert all(i in covered for i,ch in enumerate(b['text']) if not ch.isspace()),b['id']
 assert len({c['id'] for c in claims})==len(claims)

def main():
 assert sys.dont_write_bytecode and len(sys.argv)==1,'python3 -B validate.py, no arguments'
 before=tree();pins=load(P/'input-pins.json');assert len(pins)==len({r['path'] for r in pins})==77
 watched={r['path']:dg(ROOT/r['path']) for r in pins};live=[ROOT/'wiki/specs/mpe-workflows.md'];live_before={str(p):dg(p) for p in live}
 for r in pins:pin(ROOT/r['path'],r)
 assert dg(K/'manifest-author-r2.json')['sha256']=='a93a5dca90cf0aa83dd712beaea955549dda093a89668d4294335a45c0e8748a'
 mf=load(K/'manifest-author-r2.json');assert len(mf['payloads'])==60
 for r in mf['payloads']:pin(K/r['path'],r)
 review=load(P.parent/'reviews/mpe-tuning-grooves-review-final.json');assert review['disposition']=='approved-as-partial-analyst-draft' and review['reviewed_manifest_sha256']==dg(K/'manifest-author-r2.json')['sha256']
 assert dg(P/'spec-asof-r2.md')==dg(K/'mpe-workflows-author-r2.md') and dg(P/'research-asof-r2.md')==dg(K/'mpe-tuning-grooves-author-r2.md')
 for r in load(P/'owner-routes.json'):pin(P/r['snapshot'],r) # No live historical wiki equality.
 d=runpy.run_path(str(P/'derive.py'));ext=load(P/'selected-owner-contexts.json');assert len(ext)==26
 for r in ext:
  if r['kind']=='JSON':
   v=d['pointer'](load(ROOT/r['catalog']),r['json_pointer']);assert v==r['quoted_scoped_predicate'] and v['id']==r['id'] and sha256(json.dumps(v,sort_keys=True,ensure_ascii=False).encode()).hexdigest()==r['row_sha256']
  else:
   a,z=r['text_span'];v=(P/r['snapshot']).read_text()[a:z];assert v==r['quoted_scoped_predicate'] and sha256(v.encode()).hexdigest()==r['text_sha256']
 neighbor=load(P/'neighbor-source-context.json');raw=(ROOT/neighbor['source_path']).read_text();assert dg(ROOT/neighbor['source_path'])['sha256']==neighbor['sha256'] and len(neighbor['selected_blocks'])==14
 for b in neighbor['selected_blocks']:assert raw[b['raw_start']:b['raw_end']]==b['raw_html']
 assert 'only displayed in the MPE Editor' in neighbor['selected_blocks'][-1]['text']
 assert 'displayed in the MIDI Note Editor' in neighbor['selected_blocks'][-2]['text']
 faq=load(P/'faq-context.json');raw=(ROOT/faq['path']).read_text();a,z=faq['raw_span'];assert raw[a:z]==faq['exact_excerpt'] and sha256(raw[a:z].encode()).hexdigest()==faq['excerpt_sha256']
 assert 'L106: The Pitch Bend range of your MPE controller and the MPE-capable instrument need to match for correct tracking.' in raw[a:z]
 assert faq['capture_utc'] is None and faq['direct_http_status'].startswith('403')
 built=d['build']();assert len(built)==9
 for n,v in built.items():assert load(P/n)==v,n
 blocks,claims=built['source-blocks.json'],built['claims.json'];props=load(P/'proposed-deltas.json');plan=load(P/'claim-plan.json')
 assert len(blocks)==66 and len(claims)==110 and Counter(b['kind'] for b in blocks)=={'h1':1,'h2':6,'h3':2,'p':31,'li':26}
 assert sum(len(b['text']) for b in blocks)==12125
 check_claims(claims,blocks,d);d['guards'](plan,props)
 source=load(P/'source-context.json');raw=(ROOT/source['path']).read_text()
 for b in blocks:
  assert raw[b['raw_start']:b['raw_end']]==b['raw_html'] and raw.count('\n',0,b['raw_start'])+1==b['html_line']
  assert b['html_column']==b['raw_start']-(raw.rfind('\n',0,b['raw_start'])+1)
 assert Counter(r['kind'] for r in built['resources.json'])=={'image':12,'caption':12,'link':4}
 for r in built['resources.json']:
  a=r['raw_start'];z=raw.index('>',a)+1;assert sha256(raw[a:z].encode()).hexdigest()==r['starttag_sha256']
  assert r['pixels_or_destination_inspected'] is r['complete'] is False and r['capture_utc'] is None
 cat=built['owner-catalog-asof.json'];assert set(re.findall(r'^\| (REQ-MPE-\d{3}) \|',(P/'spec-asof-r2.md').read_text(),re.M))=={r['id'] for r in cat['requirements']}
 for r in cat['requirements']:
  a,z=r['markdown_span'];assert (P/r['snapshot']).read_text()[a:z]==r['original_markdown']
 for r in cat['cases']:
  assert d['pointer'](load(ROOT/r['original_catalog']),r['original_json_pointer'])==r['original_record']
  assert r['original_record']['target_build_grade']=='U' and r['original_record']['execution']=='unexecuted'
 for kind,count in [('requirements',18),('cases',27)]:assert len(built['existing-catalog-reconciliation.json'][kind])==len(cat[kind])==count
 for r in built['proposed-deltas-derived.json']:
  assert r['source_facets']==[c['id'] for c in claims if r['id'] in c['proposal_groups']] and r['source_facets']
 life=load(P/'retained-lifecycle-contexts.json');assert life['existing_cases']==[f'MPE-{i:03}' for i in range(19,28)] and life['documentary_expected'] is life['documentary_comparison'] is life['actual_expected'] is life['actual_comparison'] is None and life['target']=='U' and life['executed'] is life['complete'] is False
 for q in load(P/'source-questions.json'):assert q['actual_expected'] is q['actual_comparison'] is None and q['target']=='U' and set(q['source_blocks'])<={b['id'] for b in blocks}
 fixtures=load(P/'fixtures.json');tiny,rs=runpy.run_path(str(P/'source_parser.py'))['extract'](fixtures['parser_fixture'],'T')
 assert Counter(b['kind'] for b in tiny)=={'h1':1,'h2':1,'p':2,'li':1,'tr':1} and tiny[1]['text']=='Set 1.1.1 Here. Next.' and tiny[3]['text']=='A | B'
 assert tiny[-1]['heading_context'][-1]['anchor']=='c' and len(rs)==3 and rs[-1]['text']=='Label.' and 'outside scope' not in str(tiny)
 rejected=0
 for name in fixtures['negative_mutations']:
  cc,pp,cp=deepcopy(claims),deepcopy(props),deepcopy(plan)
  if name=='omit-source-block':cc=[c for c in cc if c['source_block']!='MPE-B024']
  elif name=='alter-source-quote':cc[1]['source_excerpt']+=' changed'
  elif name=='valid-but-wrong-case':next(c for c in cc if c['source_block']=='MPE-B028')['cases']=[d['ref'](cat,'cases',7)]
  elif name=='meter-as-default-case-coverage':cp['MPE-B013'][0]['disposition']='R'
  elif name=='resolve-fold-context':cp['MPE-B034'][0]['disposition']='R'
  elif name=='weaken-per-note-baseline':pp[6]['positive_guard']['genuinely_nonzero_independent_per_note_expression_before_exclusion']=False
  elif name=='indicator-as-delivery-baseline':pp[11]['positive_guard']['productive_controller_route_not_merely_indicator']=False
  elif name=='promote-actual-oracle':pp[0]['actual_expected']='invented event'
  else:raise AssertionError(name)
  try:check_claims(cc,blocks,d);d['guards'](cp,pp)
  except AssertionError:rejected+=1
  else:raise AssertionError('Accepted mutation: '+name)
 assert rejected==8
 if (P/'manifest.json').exists():
  own=load(P/'manifest.json');assert set(before)==set(own['files'])|{'manifest.json'}
  for n,r in own['files'].items():pin(P/n,r)
  assert own['summary']==built['summary.json']
 links=0
 for target in re.findall(r'\]\(([^)]+)\)',(P/'README.md').read_text()):
  if re.match(r'^[A-Za-z]+:',target):continue
  assert (P/target.split('#')[0]).is_file(),target;links+=1
 snapshots={r['snapshot'] for r in load(P/'owner-routes.json')}|{'spec-asof-r2.md','research-asof-r2.md'}
 authored=[p for p in P.rglob('*') if p.is_file() and p.name not in snapshots]
 for p in authored:
  if p.suffix=='.json':load(p)
  out=subprocess.run(['git','diff','--no-index','--check','/dev/null',str(p)],capture_output=True,text=True);assert out.returncode in (0,1) and not out.stdout and not out.stderr,(str(p),out.stdout,out.stderr)
 assert before==tree() and watched=={r['path']:dg(ROOT/r['path']) for r in pins} and live_before=={str(p):dg(p) for p in live}
 print(json.dumps(dict(status='pass',sealed=(P/'manifest.json').exists(),scope='Finite source/pointer/null/positive-baseline integrity only; separate semantic review pending',summary=built['summary.json'],input_pins=len(pins),unchanged_shared_R2_payloads=60,selected_external_records=len(ext),primary_clause_action_pointers=sum(len(c['requirements'])+len(c['cases']) for c in claims),external_qualified_pointers=sum(len(c['selected_external_contexts']) for c in claims),negative_fixtures=rejected,parser_fixture=True,README_links=links,authored_whitespace_files=len(authored),watched_paths=len(before)+len(watched)+len(live),all_watched_unchanged=True,writes=False,original_runtime_native_hardware_network_candidate_execution=False),indent=2))
if __name__=='__main__':main()
