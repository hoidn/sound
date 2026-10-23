"""Finite Editing MIDI retained-source audit. Source/owner inputs are inert data."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
import json,runpy,sys
P=Path(__file__).resolve().parent;ROOT=P.parents[3];K=P.parent/'midi-editing'
load=lambda p:json.loads(p.read_text())
def digest(p):
 b=p.read_bytes();return dict(bytes=len(b),sha256=sha256(b).hexdigest())
def value_hash(value):return sha256(json.dumps(value,ensure_ascii=False,sort_keys=True).encode()).hexdigest()
STATUS={'R':'represented-bounded-source-clause-action-subset','U':'documented-but-outcome-U','G':'missing-selected-owner-clause-case-or-qualifier','O':'other-owner-context-not-newly-closed','M':'research-guidance-or-mechanism-context','E':'editorial-or-structural'}
def local_ref(kind,number):
 if kind=='requirements':
  rows=load(P/'owner-requirements.json');index=next(i for i,r in enumerate(rows) if r['id']==f'REQ-MIDI-EDIT-{number:03}');field='contract';catalog=str((P/'owner-requirements.json').relative_to(ROOT));row=rows[index]
 else:
  rows=load(K/'acceptance-cases-r2.json')['cases'];index=next(i for i,r in enumerate(rows) if r['id']==f'MED-{number:03}');field='setup_action';catalog=str((K/'acceptance-cases-r2.json').relative_to(ROOT));row=rows[index]
 out=dict(id=row['id'],catalog=catalog,json_pointer=('/cases' if kind=='cases' else '')+f'/{index}/{field}',scoped_predicate_or_action=row[field],value_sha256=value_hash(row[field]),role='Exact stated predicate/action subset only; related pointer never implies whole-ID or all source-part representation.')
 if kind=='cases':out.update(historical_documentary_expected=row.get('expected'),historical_documentary_comparator=row.get('comparator'),actual_expected=None,actual_comparison=None,target='U',executed=False)
 return out

def build():
 scope=load(P/'initial-scope.json');source=scope['source'];raw=(ROOT/source['path']).read_text();assert digest(ROOT/source['path'])=={k:source[k] for k in ('bytes','sha256')}
 blocks,resources=runpy.run_path(str(P/'source_parser.py'))['extract'](raw,'MIDI');assert len(blocks)==244 and len(resources)==144
 plan=load(P/'claim-plan.json');assoc=load(P/'cross-owner-associations.json');claims=[]
 for bi,b in enumerate(blocks):
  parts=[dict(part=0,span=[0,len(b['text'])],disposition='E',requirements=[],cases=[],proposal_groups=[],assessment='Literal heading/ancestry, including retained manual footer. No source-topic completion or command law.')] if b['kind'].startswith('h') else plan[b['id']]
  for part in parts:
   a,z=part['span'];quote=b['text'][a:z];context=b['heading_context'];anchor=context[-1].get('anchor') if context else None
   claims.append(dict(id=f'MIDA-C{len(claims)+1:03}',block=b['id'],block_json_pointer=f'/{bi}',part=part['part'],text_span=[a,z],source_excerpt=quote,excerpt_sha256=sha256(quote.encode()).hexdigest(),full_paragraph_text=b['text'],full_paragraph_sha256=sha256(b['text'].encode()).hexdigest(),source_locator=dict(source_catalog=str((K/'sources.json').relative_to(ROOT)),source_catalog_json_pointer='/0',source_path=source['path'],source_url=source['url'],source_sha256=source['sha256'],source_capture_date=source['capture_date'],source_capture_utc=None,source_version=source['version'],html_line=b['html_line'],html_column=b['html_column'],raw_start=b['raw_start'],raw_end=b['raw_end'],literal_anchor=b['attributes'].get('id'),heading_context=context,subsection_url=source['url']+('#'+anchor if anchor else ''),locator_limit='Raw offsets are decoded Unicode character positions. Ancestry supplies reading context only, never an inherited paragraph/TOC citation.'),disposition=STATUS[part['disposition']],assessment=part['assessment'],full_paragraph_context_assessment=part.get('full_paragraph_context_assessment',part['assessment']),requirements=[local_ref('requirements',n) for n in part['requirements']],cases=[local_ref('cases',n) for n in part['cases']],cross_owner_related_context=assoc.get(b['id'],[]),proposal_groups=part['proposal_groups'],target='U',documentary_expected=None,documentary_comparison=None,actual_expected=None,actual_comparison=None,executed=False,complete=False,behavioral_coverage_credit=0))
 for i,r in enumerate(resources,1):
  r.update(id=f'MIDA-R{i:03}',source_path=source['path'],source_sha256=source['sha256'],source_capture_date=source['capture_date'],source_capture_utc=None,target='U',complete=False,pixels_or_destination_inspected=False,scope='Literal42link texts/hrefs and51caption texts read;51image alt/attribute keys and retained repeated URL variants checked as data. No image pixels or separately followed destinations inspected.',disposition='caption-label-read' if r['kind']=='caption' else 'image-pixels-uninspected' if r['kind']=='image' else 'linked-destination-not-separately-inspected')
 proposals=[]
 for item in load(P/'proposed-deltas.json'):
  row=dict(item);row.update(claim_ids=[c['id'] for c in claims if row['id'] in c['proposal_groups']],gap_claim_ids=[c['id'] for c in claims if row['id'] in c['proposal_groups'] and c['disposition']==STATUS['G']],status='Audit-only proposed reconciliation, no normative adoption or execution queue',positive_guard=dict(independently_owned_valid_nonempty_editable_source=True,exact_feature_mode_focus_selection_history_required=True,successful_productive_paired_baseline_before_negative=True,active_nonzero_sounding_path_only_where_audio_relevant=True,requires_genuine_automatic_scroll_then_actual_edit_pause=row['id']=='MIDA-G04',unavailable_prerequisite_remains_U=True,supplied_runtime_or_fixture_results=False),documentary_expected=None,documentary_comparison=None,expected=None,comparison=None,target='U',executed=False,complete=False,behavioral_coverage_credit=0);assert row['claim_ids'];assert row['gap_claim_ids'] or row['id']=='MIDA-G20';proposals.append(row)
 reverse={}
 for kind,rows in [('requirements',load(P/'owner-requirements.json')),('cases',load(K/'acceptance-cases-r2.json')['cases'])]:
  reverse[kind]=[]
  for i,r in enumerate(rows):
   related=[c for c in claims if any(x['id']==r['id'] for x in c[kind])]
   reverse[kind].append(dict(id=r['id'],catalog=str(((P/'owner-requirements.json') if kind=='requirements' else (K/'acceptance-cases-r2.json')).relative_to(ROOT)),json_pointer=('/cases' if kind=='cases' else '')+f'/{i}',related_primary_source_facets=[c['id'] for c in related],represented_subset_facets=[c['id'] for c in related if c['disposition']==STATUS['R']],status='Related exact primary-source subset; no whole-ID completion' if related else 'Existing owner obligation/tool action read and retained; separate Tools chapter or explicit U obligation is outside primary-source semantic closure',target='U',complete=False))
 headings=[dict(block=b['id'],block_json_pointer=f'/{i}',heading=b['text'],anchor=b['attributes'].get('id'),section=b['attributes'].get('data-number'),role='Retained literal structural context, no semantic/TOC completeness',complete=False) for i,b in enumerate(blocks) if b['kind'].startswith('h')]
 summary=dict(scope=scope['primary_scope'],source_blocks=len(blocks),block_kinds=dict(Counter(b['kind'] for b in blocks)),nonheading_blocks=len(plan),source_facets=len(claims),nonheading_facets=sum(len(parts) for parts in plan.values()),dispositions=dict(Counter(c['disposition'] for c in claims)),literal_resources=len(resources),resource_kinds=dict(Counter(r['kind'] for r in resources)),requirements=43,cases=60,tool_requirement_actions_read=17,selected_external_records=58,proposed_groups=len(proposals),source_questions=5,immutable_input_pins=len(load(P/'input-pins.json')),all_actual_and_new_documentary_oracles_null_U=True,executed=0,new_normative_IDs=0,behavioral_coverage_credit=0,complete_topics=0,read_scope='All244 retained blocks:147paragraphs/50list items/47headings read, including every sentence and embedded list with full paragraph qualifiers. All43 current clause bodies,60 setup/actions/legacy documentary strings and R2 fixture read, including17 tool actions before primary-source gaps. All42literal linktexts/hrefs,51captions,51image alt/attribute keys read; repeated URL variant attributes retained/hashchecked, no pixels or separately followed destinations. Only58selected adjacent-owner records plus named snapshot clauses read, no full cross-owner audit. Separate MIDI Tools chapter not fully semantically audited. Sentence/character accounting checks omissions only, not semantic sufficiency.')
 return {'source-blocks.json':blocks,'resources.json':resources,'claims.json':claims,'proposed-deltas-derived.json':proposals,'existing-catalog-reconciliation.json':reverse,'subsection-routing.json':headings,'summary.json':summary}

def main():
 assert sys.dont_write_bytecode and sys.argv[1:] in (['--check'],['--write'])
 if sys.argv[1:]==['--write']:assert not (P/'manifest.json').exists(),'refuse overwrite after seal'
 result=build()
 for name,value in result.items():
  if sys.argv[1:]==['--check']:assert load(P/name)==value,name
  else:(P/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(result['summary.json'],indent=2))
if __name__=='__main__':main()
