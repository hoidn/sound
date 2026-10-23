"""Read-only finite audit checks. No old checker replay, source execution or report writes."""
from pathlib import Path
from hashlib import sha256
from copy import deepcopy
from collections import Counter
import json,re,runpy,subprocess,sys
P=Path(__file__).resolve().parent;ROOT=P.parents[3];K=P.parent/'midi-editing'
load=lambda p:json.loads(p.read_text())
def dg(p):
 b=p.read_bytes();return dict(bytes=len(b),sha256=sha256(b).hexdigest())
def pin(p,r):assert dg(p)=={k:r[k] for k in ('bytes','sha256')},str(p)
def tree():return {str(p.relative_to(P)):dg(p) for p in P.rglob('*') if p.is_file()}
def pointer(value,ptr):
 for part in ptr.split('/')[1:] if ptr else []:value=value[int(part)] if isinstance(value,list) else value[part.replace('~1','/').replace('~0','~')]
 return value

def check_claims(claims,blocks,derive):
 byblock={b['id']:[] for b in blocks};plan=load(P/'claim-plan.json');assoc=load(P/'cross-owner-associations.json')
 assert [c['id'] for c in claims]==[f'MIDA-C{i:03}' for i in range(1,507)]
 for c in claims:
  b=pointer(blocks,c['block_json_pointer']);assert b['id']==c['block'];byblock[b['id']].append(c)
  a,z=c['text_span'];assert 0<=a<z<=len(b['text']) and c['source_excerpt']==b['text'][a:z]
  assert c['excerpt_sha256']==sha256(c['source_excerpt'].encode()).hexdigest()
  assert c['full_paragraph_text']==b['text'] and c['full_paragraph_sha256']==sha256(b['text'].encode()).hexdigest()
  loc=c['source_locator'];assert loc['source_capture_utc'] is None
  assert loc['raw_start']==b['raw_start'] and loc['raw_end']==b['raw_end'] and loc['heading_context']==b['heading_context']
  assert loc['literal_anchor']==b['attributes'].get('id')
  if b['kind'].startswith('h'):assert c['requirements']==c['cases']==[] and c['disposition']==derive['STATUS']['E']
  else:
   part=plan[b['id']][c['part']];assert part['span']==c['text_span']
   assert c['requirements']==[derive['local_ref']('requirements',n) for n in part['requirements']]
   assert c['cases']==[derive['local_ref']('cases',n) for n in part['cases']]
   assert c['disposition']==derive['STATUS'][part['disposition']] and c['assessment']==part['assessment'] and c['proposal_groups']==part['proposal_groups']
  assert c['cross_owner_related_context']==assoc.get(b['id'],[])
  for ref in c['requirements']+c['cases']:
   value=pointer(load(ROOT/ref['catalog']),ref['json_pointer']);assert value==ref['scoped_predicate_or_action'] and derive['value_hash'](value)==ref['value_sha256']
   assert pointer(load(ROOT/ref['catalog']),ref['json_pointer'].rsplit('/',1)[0])['id']==ref['id']
  for ref in c['cross_owner_related_context']:assert pointer(load(ROOT/ref['catalog']),ref['json_pointer'])['id']==ref['id']
  assert all(c[k] is None for k in ('actual_expected','actual_comparison','documentary_expected','documentary_comparison'))
  assert c['target']=='U' and c['executed'] is c['complete'] is False and c['behavioral_coverage_credit']==0
  if c['disposition']==derive['STATUS']['G']:assert c['proposal_groups']
 for b in blocks:
  entries=byblock[b['id']];assert [c['part'] for c in entries]==list(range(len(entries)))
  seen=set()
  for c in entries:
   positions=set(range(*c['text_span']));assert not seen.intersection(positions);seen.update(positions)
  assert all(i in seen for i,x in enumerate(b['text']) if not x.isspace()),b['id']
 # These check actual source/action subsets rather than generic source citations.
 for c in byblock['MIDI:B114']:assert c['disposition']==derive['STATUS']['R'] and {r['id'] for r in c['cases']}=={'MED-058','MED-059','MED-060'}
 for c in byblock['MIDI:B217']:assert c['disposition']==derive['STATUS']['G'] and 'MED-020' in {r['id'] for r in c['cases']} and 'MIDA-G35' in c['proposal_groups']
 assert {c['disposition'] for c in byblock['MIDI:B123']}=={derive['STATUS']['U']}


def check_proposals(proposals,claims,context):
 assert [g['id'] for g in proposals]==[f'MIDA-G{i:02}' for i in range(1,39)]
 for g in proposals:
  assert all(g[k] is None for k in ('expected','comparison','documentary_expected','documentary_comparison'))
  assert g['target']=='U' and g['executed'] is g['complete'] is False and g['behavioral_coverage_credit']==0
  assert g['claim_ids']==[c['id'] for c in claims if g['id'] in c['proposal_groups']]
  assert g['gap_claim_ids']==[c['id'] for c in claims if g['id'] in c['proposal_groups'] and c['disposition']=='missing-selected-owner-clause-case-or-qualifier']
  assert g['claim_ids'] and (g['gap_claim_ids'] or g['id']=='MIDA-G20')
  assert g['proposed_minimal_delta'] and g['proposed_future_action_and_positive_baseline'] and g['limits']
  guard=g['positive_guard']
  assert all(guard[k] is True for k in ('independently_owned_valid_nonempty_editable_source','exact_feature_mode_focus_selection_history_required','successful_productive_paired_baseline_before_negative','active_nonzero_sounding_path_only_where_audio_relevant','unavailable_prerequisite_remains_U'))
  assert guard['supplied_runtime_or_fixture_results'] is False
  assert guard['requires_genuine_automatic_scroll_then_actual_edit_pause']==(g['id']=='MIDA-G04')
 assert context['existing_R1_notes']['generator_nonempty_baseline_required'] is True
 assert context['existing_R1_notes']['Chop_positive_gap_is_timeline_insertion'] is False
 assert context['target']=='U' and context['expected'] is context['comparison'] is None and context['executed'] is context['complete'] is False
 assert 'no RNG/sample/distribution' in proposals[19]['limits']
 assert 'no moving scroll while stopped' in proposals[3]['limits'].lower()
 assert all(x in proposals[3]['proposed_future_action_and_positive_baseline'].lower() for x in ('moving playhead crossing zoomed viewport','independently observe automatic scroll','perform real edit','independently observe pause'))


def main():
 assert sys.dont_write_bytecode and sys.argv[1:]==['--check'],'Use python3 -B validate.py --check'
 before=tree();inputs=load(P/'input-pins.json');assert len(inputs)==len({r['path'] for r in inputs})==47
 watched={r['path']:dg(ROOT/r['path']) for r in inputs}
 for r in inputs:pin(ROOT/r['path'],r)
 assert (P/'source_parser.py').read_bytes()==(P.parent/'clip-view-source-audit/source_parser.py').read_bytes()
 assert dg(K/'manifest-author-r2.json')['sha256']=='c6d50d13268b6e00efc3e59a3c1bead0d18e8c23a3505b1b0a7d595dc4a198b2'
 owner=load(K/'manifest-author-r2.json');assert len(owner['files'])==24
 for name,r in owner['files'].items():pin(K/name,r)
 assert sum(r['path'].startswith(str(K.relative_to(ROOT))+'/') for r in inputs)==25 # Future additive successors do not invalidate as-of pins.
 for r in load(P/'owner-context.json'):pin(P/r['snapshot'],r);pin(ROOT/r['provider'],r)
 for r in load(P/'external-owner-routes.json'):
  pin(P/r['snapshot'],r['origin_identity_asof'])
  text=(P/r['snapshot']).read_text()
  for q in r['selected_clauses']:assert q['excerpt'] in text and text.splitlines()[q['line']-1].startswith(('### '+q['id'], '| '+q['id']+' |'))
 # Immutable provider rows, never the future mutable canonical.
 text=(P/'owner-snapshots/spec-r2.md').read_text();rows=load(P/'owner-requirements.json')
 assert len(rows)==43 and [r['id'] for r in rows]==[f'REQ-MIDI-EDIT-{i:03}' for i in range(1,44)]
 assert [line for line in text.splitlines() if re.match(r'^\| REQ-MIDI-EDIT-',line)]==[r['literal_row'] for r in rows]
 for r in rows:assert text.splitlines()[r['line']-1]==r['literal_row']
 external=load(P/'external-contexts.json');assert len(external)==58
 for r in external:assert pointer(load(ROOT/r['catalog']),r['json_pointer'])==r['row'] and r['newly_independently_approved'] is False
 cases=load(K/'acceptance-cases-r2.json');assert len(cases['cases'])==60 and [r['id'] for r in cases['cases']]==[f'MED-{i:03}' for i in range(1,61)]
 assert Counter(r['documented_domain_grade'] for r in cases['cases'])=={'D12':46,'U':14}
 assert all(r['target_12_4_3_grade']=='U' and r['execution']=='not-run' for r in cases['cases'])
 actual=cases['actual_result_status'];assert actual['actual_expected'] is actual['actual_comparison'] is None and actual['target_grade']=='U' and actual['executed'] is False
 derive=runpy.run_path(str(P/'derive.py'));built=derive['build']()
 for name,value in built.items():assert load(P/name)==value,name
 blocks,claims,proposals=built['source-blocks.json'],built['claims.json'],built['proposed-deltas-derived.json']
 assert len(blocks)==244 and Counter(b['kind'] for b in blocks)=={'h1':1,'h2':8,'h3':23,'h4':15,'p':147,'li':50}
 plan=load(P/'claim-plan.json');assert set(plan)=={b['id'] for b in blocks if not b['kind'].startswith('h')} and sum(map(len,plan.values()))==459
 context=load(P/'review-context.json');check_claims(claims,blocks,derive);check_proposals(proposals,claims,context)
 raw=(ROOT/load(P/'initial-scope.json')['source']['path']).read_text()
 for b in blocks:
  assert raw[b['raw_start']:b['raw_end']]==b['raw_html']
  assert raw.count('\n',0,b['raw_start'])+1==b['html_line'] and b['html_column']==b['raw_start']-(raw.rfind('\n',0,b['raw_start'])+1)
 for r in built['resources.json']:
  a=r['raw_start'];z=raw.index('>',a)+1;assert sha256(raw[a:z].encode()).hexdigest()==r['starttag_sha256']
  assert r['pixels_or_destination_inspected'] is r['complete'] is False and r['target']=='U' and r['source_capture_utc'] is None
 assert Counter(r['kind'] for r in built['resources.json'])=={'link':42,'image':51,'caption':51}
 for kind,source in [('requirements',rows),('cases',cases['cases'])]:
  reverse=built['existing-catalog-reconciliation.json'][kind];assert [r['id'] for r in source]==[r['id'] for r in reverse]
  for r in reverse:assert pointer(load(ROOT/r['catalog']),r['json_pointer'])['id']==r['id'] and r['target']=='U' and r['complete'] is False
 for q in load(P/'source-questions.json'):
  assert q['target']=='U' and q['expected'] is q['comparison'] is None and q['executed'] is q['complete'] is False
  for ref in q['source_quotes']:assert pointer(load(ROOT/ref['catalog']),ref['json_pointer'])==ref['quote']
 # Small parser/provenance fixture. It executes only our inspected inert HTMLParser.
 fixtures=load(P/'fixtures.json');tiny,resources=runpy.run_path(str(P/'source_parser.py'))['extract'](fixtures['parser_fixture'],'TEST')
 assert Counter(b['kind'] for b in tiny)=={'h1':1,'h2':1,'p':1,'li':2}
 assert tiny[1]['text']=='Set 1.1.1 Here. Next sentence. Keep selected notes.'
 assert tiny[-1]['heading_context'][-1]['anchor']=='child' and [r['kind'] for r in resources]==['image','caption']
 rejected=0
 for mutation in fixtures['negative_mutations']:
  cc,pp,rr=deepcopy(claims),deepcopy(proposals),deepcopy(context)
  if mutation=='omit-qualified-source-part':cc=[c for c in cc if not (c['block']=='MIDI:B114' and c['part']==1)]
  elif mutation=='wrong-source-pointer':cc[1]['block_json_pointer']='/0'
  elif mutation=='wrong-case-association':next(c for c in cc if c['block']=='MIDI:B030')['cases']=[derive['local_ref']('cases',1)]
  elif mutation=='promote-actual-oracle':cc[1]['actual_expected']='fabricated'
  elif mutation=='remove-productive-follow-baseline':pp[3]['proposed_future_action_and_positive_baseline']='Set Follow flag, edit and inspect absence; no prior productive scrolling.'
  elif mutation=='force-Humanize-equivalence':next(c for c in cc if c['block']=='MIDI:B123')['disposition']=derive['STATUS']['R']
  elif mutation=='rewrite-true-Interval-as-gap':next(c for c in cc if c['block']=='MIDI:B114')['disposition']=derive['STATUS']['G']
  elif mutation=='erase-Chance-action-gap':next(c for c in cc if c['block']=='MIDI:B217')['disposition']=derive['STATUS']['R']
  elif mutation=='waive-nonempty-generation':rr['existing_R1_notes']['generator_nonempty_baseline_required']=False
  elif mutation=='invent-Chop-timeline-insertion':rr['existing_R1_notes']['Chop_positive_gap_is_timeline_insertion']=True
  else:raise AssertionError(mutation)
  try:check_claims(cc,blocks,derive);check_proposals(pp,cc,rr)
  except AssertionError:rejected+=1
  else:raise AssertionError('Mutation accepted: '+mutation)
 assert rejected==10
 if (P/'manifest.json').exists():
  manifest=load(P/'manifest.json');assert set(before)==set(manifest['files'])|{'manifest.json'}
  for name,r in manifest['files'].items():pin(P/name,r)
  assert manifest['summary']==built['summary.json']
 links=0
 for target in re.findall(r'\]\(([^)]+)\)',(P/'README.md').read_text()):
  if re.match(r'^[A-Za-z]+:',target):continue
  assert (P/target.split('#')[0]).is_file(),target;links+=1
 authored=[p for p in P.rglob('*') if p.is_file() and 'owner-snapshots' not in p.parts]
 for p in authored:
  if p.suffix=='.json':load(p)
  result=subprocess.run(['git','diff','--no-index','--check','/dev/null',str(p)],capture_output=True,text=True)
  assert result.returncode in (0,1) and not result.stdout and not result.stderr,(str(p),result.stdout,result.stderr)
 assert tree()==before and watched=={r['path']:dg(ROOT/r['path']) for r in inputs}
 print(json.dumps(dict(status='pass',sealed=(P/'manifest.json').exists(),scope='Audit integrity/provenance/omission/guard checks, not independent semantic approval or product validation',source_blocks=244,facets=len(claims),proposals=len(proposals),inputs=len(inputs),owner_history_files=25,selected_external_records=58,negative_fixtures=rejected,retained_positive_contexts=len(fixtures['retained_positive_contexts']),parser_fixture=True,README_links=links,authored_whitespace_files=len(authored),packet_and_inputs_unchanged=True,writes=False,runtime_or_network_execution=False),indent=2))
if __name__=='__main__':main()
