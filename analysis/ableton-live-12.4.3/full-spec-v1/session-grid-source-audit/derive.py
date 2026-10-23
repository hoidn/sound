"""Finite retained Session grid/scenes reconciliation; source HTML/JSON are inert data."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
import json,re,runpy,sys
P=Path(__file__).resolve().parent;ROOT=P.parents[3];K=P.parent/'session-workflows'
load=lambda p:json.loads(p.read_text())
def digest(p):
 b=p.read_bytes();return dict(bytes=len(b),sha256=sha256(b).hexdigest())
def spans(text):
 result=[];start=0
 for m in re.finditer(r'(?<=[.!?])\s+(?=[A-Z])',text):result.append([start,m.start()]);start=m.end()
 return result+[[start,len(text)]]
STATUS={'R':'represented-bounded-source-clause-action-subset','U':'documented-but-outcome-U','G':'missing-selected-owner-clause-case-or-qualifier','O':'other-owner-context-not-newly-closed','M':'research-guidance-context','E':'editorial-or-structural'}
def ref(kind,number):
 rows=load(K/(kind+'.json'));id=(f'REQ-SESSION-VIEW-{number:03}' if kind=='requirements' else f'SV-{number:03}') if isinstance(number,int) else number
 i=next(i for i,r in enumerate(rows) if r['id']==id);field='contract' if kind=='requirements' else 'setup_and_action';value=rows[i][field]
 return dict(id=id,catalog=str((K/(kind+'.json')).relative_to(ROOT)),json_pointer=f'/{i}/{field}',scoped_predicate=value,value_sha256=sha256(value.encode()).hexdigest(),role='Quoted actual contract/action; only assessed subset, no whole-ID closure.')

def build():
 source=load(K/'source.json');assert digest(ROOT/source['path'])=={k:source[k] for k in ['bytes','sha256']}
 raw=(ROOT/source['path']).read_text();blocks,resources=runpy.run_path(str(P/'source_parser.py'))['extract'](raw,'SV');old=load(K/'source-blocks.json')
 assert len(blocks)==len(old)==77
 for b,o in zip(blocks,old):
  assert (b['id'],b['kind'],b['text'],b['html_line'])==(o['id'],o['tag'],o['text'],o['html_line'])
  b['old_packet_anchor_context']=o['anchor'];b['old_anchor_role']='Original last-heading context, not a literal paragraph/row anchor.'
 plan=load(P/'claim-plan.json');external=load(P/'external-contexts.json');md=load(P/'external-markdown-contexts.json');mapping=load(P/'external-reference-plan.json');claims=[]
 for bi,b in enumerate(blocks):
  rows=[dict(sentence=0,disposition='E',requirements=[],cases=[],gaps=[],assessment='Literal numbered heading/ancestry only; no semantic leaf credit.')] if b['kind'].startswith('h') else plan[b['id']]
  parts=[[0,len(b['text'])]] if b['kind'].startswith('h') else spans(b['text']);assert [r['sentence'] for r in rows]==list(range(len(parts)))
  linked=mapping.get(b['id'],dict(external_record_indices=[],markdown_record_indices=[]))
  er=[dict(context_catalog='external-contexts.json',context_json_pointer=f'/{i}',id=external[i]['id'],catalog=external[i]['catalog'],json_pointer=external[i]['json_pointer'],role='Selected actual predicate/action context only; assessment does not claim full coverage.') for i in linked['external_record_indices']]
  mr=[dict(context_catalog='external-markdown-contexts.json',context_json_pointer=f'/{i}',id=md[i]['id'],snapshot=md[i]['snapshot'],quoted_scoped_predicate=md[i]['text'],text_sha256=md[i]['text_sha256'],role='As-of exact Markdown clause/scenario; no invented original JSON catalog.') for i in linked['markdown_record_indices']]
  for x,(a,z) in zip(rows,parts):
   claims.append(dict(id=f'SGA-C{len(claims)+1:03}',block=b['id'],block_json_pointer=f'/{bi}',sentence=x['sentence'],text_span=[a,z],source_excerpt=b['text'][a:z],excerpt_sha256=sha256(b['text'][a:z].encode()).hexdigest(),source_locator=dict(local_source_id=source['id'],original_source_id='D12-session-view',source_catalog=str((K/'source.json').relative_to(ROOT)),source_path=source['path'],source_url=source['url'],source_sha256=source['sha256'],source_capture_utc=source['capture_utc'],source_version=source['version'],html_line=b['html_line'],html_column=b['html_column'],raw_start=b['raw_start'],raw_end=b['raw_end'],literal_anchor=b['attributes'].get('id'),heading_context=b['heading_context'],subsection_url=source['url']+'#'+b['heading_context'][-1]['anchor'],locator_limit='Raw offsets count decoded Unicode characters. Old packet anchor is last-heading context; literal paragraph ID is not inherited; structural ancestry is not direct TOC or leaf semantic coverage.'),disposition=STATUS[x['disposition']],assessment=x['assessment'],requirements=[ref('requirements',n) for n in x['requirements']],cases=[ref('cases',n) for n in x['cases']],external_context_references=er,external_markdown_references=mr,proposal_groups=['SGA-'+g for g in x['gaps']],target='U',actual_expected=None,actual_comparison=None,executed=False,complete=False,behavioral_coverage_credit=0))
 for i,r in enumerate(resources,1):
  parent=next((b['id'] for b in blocks if b['raw_start']<=r['raw_start']<b['raw_end']),None)
  r.update(id=f'SGA-R{i:03}',source_sha256=source['sha256'],source_url=source['url'],source_capture_utc=source['capture_utc'],literal_container_block=parent,container_role='Raw containment only, no inherited prerequisite or semantic association.',target='U',complete=False,pixels_or_destination_inspected=False,scope='Literal text/attributes read; linked destinations and image pixels not separately inspected. Internal target text read only as part of retained chapter.',disposition='caption-label-read' if r['kind']=='caption' else 'image-pixels-uninspected' if r['kind']=='image' else 'linked-destination-not-separately-inspected')
 proposals=[]
 for x in load(P/'proposed-deltas.json'):
  row=dict(x);row.update(claim_ids=[c['id'] for c in claims if x['id'] in c['proposal_groups']],status='audit-only proposed owner reconciliation; no current normative adoption',positive_guard=dict(admitted_exact_feature_mode_history_focus=True,independently_valid_owned_nonempty_source=True,active_unmuted_nonzero_output_where_relevant=True,paired_successful_baseline_before_negative=True,requires_genuinely_playing_Arrangement_before_stop=x['id']=='SGA-G14',requires_productive_recording_before_property_edit=x['id']=='SGA-G13',missing_or_failed_prerequisite_stays_U=True,runtime_fixtures_supplied=False),documentary_expected=None,documentary_comparison=None,expected=None,comparison=None,target='U',executed=False,complete=False,behavioral_coverage_credit=0)
  assert row['claim_ids'];proposals.append(row)
 reverse={}
 for kind in ['requirements','cases']:
  reverse[kind]=[]
  for i,r in enumerate(load(K/(kind+'.json'))):
   hit=[c for c in claims if any(t['id']==r['id'] for t in c[kind])]
   reverse[kind].append(dict(id=r['id'],catalog=str((K/(kind+'.json')).relative_to(ROOT)),json_pointer=f'/{i}',source_facets=[c['id'] for c in hit],represented_subset_facets=[c['id'] for c in hit if c['disposition']==STATUS['R']],status='Partial source/action reconciliation; no complete ID' if hit else 'Explicit existing U operational obligation retained without new source/runtime oracle',target='U',complete=False))
 headings=[]
 for b in blocks:
  if b['kind'].startswith('h'):headings.append(dict(block=b['id'],anchor=b['attributes']['id'],number=b['attributes'].get('data-number'),heading=b['text'],source_url=source['url']+'#'+b['attributes']['id'],structural_descendant_facets=[c['id'] for c in claims if any(h['anchor']==b['attributes']['id'] for h in c['source_locator']['heading_context'])],semantics='Literal retained heading ancestry only, not direct TOC match or semantic leaf coverage',complete=False))
 summary=dict(scope='Full retained Session chapter7 text and literal resources versus current grid/scenes owner; partial source reconciliation only',source_blocks=len(blocks),block_kinds=dict(Counter(b['kind'] for b in blocks)),source_text_characters=sum(len(b['text']) for b in blocks),source_tables=sum(b['kind']=='tr' for b in blocks),facets=len(claims),dispositions=dict(Counter(c['disposition'] for c in claims)),resources=len(resources),resource_kinds=dict(Counter(r['kind'] for r in resources)),requirements=29,cases=40,proposed_groups=len(proposals),all_actual_oracles_null_U=True,executed=0,new_normative_IDs=0,behavioral_coverage_credit=0,complete_topics=0,read_scope='All77 normalized source blocks/53paragraphs/13listitems/11headings,29 actual clauses,40 actual actions/documentary predicates and fixture read. All59 literal resource records text/attrs/captions read; pixels/destinations uninspected, including two blank inline selector glyphs. Selected50 external JSON records/14 Markdown clauses/actions and Group MixingB043 with nearby context read; no full external family/source audit. Text/span completeness detects omission, not semantic sufficiency.')
 return {'source-blocks.json':blocks,'resources.json':resources,'claims.json':claims,'proposed-deltas-derived.json':proposals,'existing-catalog-reconciliation.json':reverse,'subsection-routing.json':headings,'summary.json':summary}

def main():
 assert sys.dont_write_bytecode and sys.argv[1:] in (['--check'],['--write'])
 if sys.argv[1:]==['--write']:assert not (P/'manifest.json').exists(),'refuse overwrite after seal'
 result=build()
 for name,value in result.items():
  if sys.argv[1:]==['--check']:assert load(P/name)==value,name
  else:(P/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
 print(json.dumps(result['summary.json'],indent=2))
if __name__=='__main__':main()
