"""Read-only finite source/pointer/baseline/null checks. No host/vendor execution."""
from pathlib import Path
from hashlib import sha256
from copy import deepcopy
from collections import Counter
import json,re,runpy,subprocess,sys
P=Path(__file__).resolve().parent;ROOT=P.parents[3];K=P.parent/'session-workflows'
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
  loc=c['source_locator'];assert loc['literal_anchor']==b['attributes'].get('id')
  assert loc['heading_context']==b['heading_context'] and loc['raw_start']==b['raw_start'] and loc['raw_end']==b['raw_end']
  if b['kind'].startswith('h'):assert c['requirements']==c['cases']==[]
  else:
   row=plan[b['id']][c['sentence']]
   assert c['requirements']==[derive['ref']('requirements',i) for i in row['requirements']]
   assert c['cases']==[derive['ref']('cases',i) for i in row['cases']]
   assert c['disposition']==derive['STATUS'][row['disposition']] and c['assessment']==row['assessment']
  for ref in c['requirements']+c['cases']:
   doc=load(ROOT/ref['catalog']);value=pointer(doc,ref['json_pointer']);assert value==ref['scoped_predicate'] and sha256(value.encode()).hexdigest()==ref['value_sha256']
   assert pointer(doc,ref['json_pointer'].rsplit('/',1)[0])['id']==ref['id']
  for ref in c['external_context_references']:
   r=pointer(load(P/ref['context_catalog']),ref['context_json_pointer'])
   assert all(ref[k]==r[k] for k in ['catalog','json_pointer','id'])
  for ref in c['external_markdown_references']:
   r=pointer(load(P/ref['context_catalog']),ref['context_json_pointer'])
   assert all(ref[k]==r[k] for k in ['snapshot','id','text_sha256']) and ref['quoted_scoped_predicate']==r['text']
  assert c['actual_expected'] is c['actual_comparison'] is None and c['target']=='U'
  assert c['executed'] is c['complete'] is False and c['behavioral_coverage_credit']==0
 for b in blocks:
  covered=set()
  for c in byblock[b['id']]:covered.update(range(*c['text_span']))
  assert all(i in covered for i,x in enumerate(b['text']) if not x.isspace()),b['id']

def check_proposals(proposals):
 assert [g['id'] for g in proposals]==[f'SGA-G{i:02}' for i in range(1,18)]
 for g in proposals:
  assert all(g[k] is None for k in ['documentary_expected','documentary_comparison','expected','comparison'])
  assert g['target']=='U' and g['executed'] is g['complete'] is False and g['behavioral_coverage_credit']==0
  guard=g['positive_guard'];assert all(guard[k] is True for k in ['admitted_exact_feature_mode_history_focus','independently_valid_owned_nonempty_source','active_unmuted_nonzero_output_where_relevant','paired_successful_baseline_before_negative','missing_or_failed_prerequisite_stays_U'])
  assert guard['runtime_fixtures_supplied'] is False
  assert guard['requires_genuinely_playing_Arrangement_before_stop']==(g['id']=='SGA-G14')
  assert guard['requires_productive_recording_before_property_edit']==(g['id']=='SGA-G13')
  assert g['claim_ids'] and g['proposed_case_action'] and g['limits']

def check_group_context(g):
 assert g['state']=='unresolved source-context distinction' and g['paired_session_block']=='SV-B017'
 assert all(g[k] is None for k in ['documentary_expected','documentary_comparison','expected','comparison'])
 assert g['target']=='U' and g['executed'] is g['complete'] is False
 assert all(g['future_probe_baseline'][k] is True for k in ['genuinely_playing_nonempty_children','active_transport_and_nonzero_output','separate_populated_and_empty_slot_contexts','missing_baseline_stays_U'])
 probe=g['productive_probe'];r=pointer(load(P/probe['context_catalog']),probe['context_json_pointer'])
 assert all(probe[k]==r[k] for k in ['id','catalog','json_pointer']) and probe['id']=='MXW-U-GROUP-SLOT'
 assert 'genuinely playing nonempty contained clips' in r['row']['setup_and_action']
 assert r['row']['source_claim'] is r['row']['documentary_expected'] is r['row']['documentary_comparator'] is r['row']['expected'] is r['row']['comparison'] is None


def main():
 assert sys.dont_write_bytecode and len(sys.argv)==1,'Use python -B validate.py without arguments'
 before=tree();inputs=load(P/'input-pins.json');assert len(inputs)==len({r['path'] for r in inputs})==52
 ebefore={r['path']:dg(ROOT/r['path']) for r in inputs}
 for r in inputs:pin(ROOT/r['path'],r)
 assert dg(K/'manifest-author-r2.json')['sha256']=='2465c28d4131f8d895c4e17ac5f23b43f41789e99ab59c2a93ba9cc14edc4cf5'
 owner=load(K/'manifest-author-r2.json');assert len(owner['files'])==18
 for name,row in owner['files'].items():pin(K/name,row)
 review=load(K.parent/'reviews/session-view-workflows-review-final.json');assert review['disposition']=='approved-as-partial-analyst-draft' and review['new_required_findings']==[]
 assert review['reviewed_manifest_sha256']==dg(K/'manifest-author-r2.json')['sha256']
 source=load(K/'source.json');context=load(P/'source-context.json');parent=pointer(load(ROOT/context['original_catalog']),context['original_json_pointer'])
 assert context['original_id']==parent['id']=='D12-session-view' and context['local_id']==source['id']=='D12-SESSION'
 assert source['capture_utc']==parent['captured_utc']==context['capture_utc'] and source['url']==parent['url']==context['source_url']
 pin(ROOT/source['path'],source);pin(ROOT/source['path'],parent)
 for r in load(P/'owner-context.json'):pin(P/r['snapshot'],r);pin(ROOT/r['provider'],r)
 for r in load(P/'owner-routes.json'):pin(P/r['snapshot'],r) # Never compare evolving live canonicals.
 external=load(P/'external-contexts.json');assert len(external)==50
 for r in external:
  value=pointer(load(ROOT/r['catalog']),r['json_pointer']);assert value==r['row'] and value['id']==r['id']
  assert sha256(json.dumps(value,sort_keys=True,ensure_ascii=False).encode()).hexdigest()==r['row_sha256']
 for r in load(P/'external-markdown-contexts.json'):
  assert r['text'] in (P/r['snapshot']).read_text() and sha256(r['text'].encode()).hexdigest()==r['text_sha256']
 group=load(P/'group-source-context.json');check_group_context(group)
 rawgroup=Path(group['source']['path']).read_text();pin(Path(group['source']['path']),group['source']);hit=group['exact_raw_selected_block'];assert rawgroup[hit['raw_start']:hit['raw_end']]==hit['raw_html']
 assert pointer(load(ROOT/group['old_block_catalog']),group['old_block_pointer'])['text']==hit['text']
 assert 'whenever at least one clip is available' in hit['text']
 derive=runpy.run_path(str(P/'derive.py'));built=derive['build']();assert len(built)==7
 for name,value in built.items():assert load(P/name)==value,name
 blocks,claims,proposals=built['source-blocks.json'],built['claims.json'],built['proposed-deltas-derived.json']
 assert len(blocks)==77 and len(claims)==142 and Counter(b['kind'] for b in blocks)=={'p':53,'h1':1,'h2':5,'h3':5,'li':13}
 check_claims(claims,blocks,derive);check_proposals(proposals)
 assert 'Group slots which have no corresponding clips contain stop buttons.' in blocks[16]['text']
 raw=(ROOT/source['path']).read_text()
 for b in blocks:
  assert raw[b['raw_start']:b['raw_end']]==b['raw_html']
  assert raw.count('\n',0,b['raw_start'])+1==b['html_line']
  assert b['html_column']==b['raw_start']-(raw.rfind('\n',0,b['raw_start'])+1)
  assert b['old_packet_anchor_context']==b['heading_context'][-1]['anchor']
 for r in built['resources.json']:
  a=r['raw_start'];z=raw.index('>',a)+1;assert sha256(raw[a:z].encode()).hexdigest()==r['starttag_sha256']
  assert r['pixels_or_destination_inspected'] is r['complete'] is False
 assert Counter(r['kind'] for r in built['resources.json'])=={'image':22,'caption':20,'link':17}
 inline=[r for r in built['resources.json'] if r['kind']=='image' and r['literal_container_block']=='SV-B075'];assert len(inline)==2 and all(r['attributes']['alt']=='' for r in inline)
 for kind,count in [('requirements',29),('cases',40)]:
  rows=load(K/(kind+'.json'));back=built['existing-catalog-reconciliation.json'][kind]
  assert len(rows)==len(back)==count and [r['id'] for r in rows]==[r['id'] for r in back]
  for i,(old,r) in enumerate(zip(rows,back)):
   assert pointer(load(ROOT/r['catalog']),r['json_pointer'])==old and r['json_pointer']==f'/{i}'
   assert r['source_facets']==[c['id'] for c in claims if any(t['id']==r['id'] for t in c[kind])]
   assert r['target']=='U' and r['complete'] is False
 for r in load(K/'requirements.json'):
  assert r['target_applicability']=='U'
  for e in r['evidence']:
   b=next(b for b in blocks if b['id']==e['block']);assert e['anchor']==b['old_packet_anchor_context'] and e['html_line']==b['html_line']
 for c in load(K/'cases.json'):assert c['expected'] is c['comparison'] is None and c['target_grade']=='U' and c['executed'] is False
 assert set(re.findall(r'^### (REQ-SESSION-VIEW-\d+)',(P/'spec-asof-r2.md').read_text(),re.M))=={r['id'] for r in load(K/'requirements.json')}
 for q in load(P/'source-questions.json'):assert q['state'] in ['U','unresolved-source-context','uninspected'] and set(q['source_blocks'])<={b['id'] for b in blocks}
 # Parser inclusion/ancestry/decimal and blank-inline resource fixture, despite no actual source tables.
 fixtures=load(P/'fixtures.json');parse=runpy.run_path(str(P/'source_parser.py'))['extract'];tiny,rs=parse(fixtures['parser_fixture'],'TEST')
 assert Counter(b['kind'] for b in tiny)=={'h1':1,'h2':1,'p':2,'li':1,'tr':2}
 assert [tiny[1]['text'][a:z] for a,z in derive['spans'](tiny[1]['text'])]==['Set 1.1.1 Here.','Next sentence.']
 assert tiny[-1]['heading_context'][-1]['anchor']=='child' and len(rs)==3 and rs[-1]['text']=='Label only.'
 assert tiny[-1]['text']=='Use or selectors.' and 'outside scope' not in str(tiny)
 rejected=0
 for name in fixtures['negative_mutations']:
  cc,pp,gg=deepcopy(claims),deepcopy(proposals),deepcopy(group)
  if name=='omit-source-block':cc=[c for c in cc if c['block']!='SV-B008']
  elif name=='alter-quote':cc[1]['source_excerpt']+=' changed'
  elif name=='misassociate-preference-case':next(c for c in cc if c['block']=='SV-B023')['cases']=[derive['ref']('cases',23)]
  elif name=='choose-group-stop-law':gg['state']='proved same stop law'
  elif name=='remove-playing-child-baseline':gg['future_probe_baseline']['genuinely_playing_nonempty_children']=False
  elif name=='remove-Arrangement-positive-baseline':pp[13]['positive_guard']['requires_genuinely_playing_Arrangement_before_stop']=False
  elif name=='promote-actual-oracle':pp[0]['expected']='invented result'
  else:raise AssertionError(name)
  try:check_claims(cc,blocks,derive);check_proposals(pp);check_group_context(gg)
  except AssertionError:rejected+=1
  else:raise AssertionError('Mutation accepted: '+name)
 assert rejected==7
 if (P/'manifest.json').exists():
  mf=load(P/'manifest.json');assert set(before)==set(mf['files'])|{'manifest.json'}
  for name,r in mf['files'].items():pin(P/name,r)
  assert mf['summary']==built['summary.json']
 links=0
 for target in re.findall(r'\]\(([^)]+)\)',(P/'README.md').read_text()):
  if re.match(r'^[A-Za-z]+:',target):continue
  assert (P/target.split('#')[0]).is_file(),target;links+=1
 authored=[p for p in P.rglob('*') if p.is_file() and 'owner-snapshots' not in p.parts and p.name not in ['spec-asof-r2.md','research-asof-r2.md']]
 for p in authored:
  if p.suffix=='.json':load(p)
  out=subprocess.run(['git','diff','--no-index','--check','/dev/null',str(p)],capture_output=True,text=True)
  assert out.returncode in (0,1) and not out.stdout and not out.stderr,(str(p),out.stdout,out.stderr)
 assert tree()==before and ebefore=={r['path']:dg(ROOT/r['path']) for r in inputs}
 print(json.dumps(dict(status='pass',sealed=(P/'manifest.json').exists(),scope='Finite source/pointer/null/guard integrity only; independent source-semantic review pending',summary=built['summary.json'],input_pins=52,current_owner_payloads=18,primary_asof_snapshots=2,external_route_snapshots=11,selected_external_JSON_records=50,selected_external_markdown_records=14,primary_contract_action_pointers=sum(len(c['requirements'])+len(c['cases']) for c in claims),external_qualified_context_pointers=sum(len(c['external_context_references'])+len(c['external_markdown_references']) for c in claims),existing_group_probe_reused=True,negative_fixtures=rejected,parser_table_decimal_hierarchy_inline_resources_fixture=True,README_links=links,authored_whitespace_files=len(authored),packet_and_inputs_unchanged=True,writes=False,original_runtime_network_hardware_candidate_execution=False),indent=2))
if __name__=='__main__':main()
