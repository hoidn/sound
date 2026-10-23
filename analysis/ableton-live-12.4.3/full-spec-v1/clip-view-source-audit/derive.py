"""Finite retained Clip View source reconciliation; original source remains inert data."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
import json,re,runpy,sys
P=Path(__file__).resolve().parent;ROOT=P.parents[3];K=P.parent/'clip-view'
load=lambda p:json.loads(p.read_text())
def digest(p):
 b=p.read_bytes();return dict(bytes=len(b),sha256=sha256(b).hexdigest())
def spans(text):
 result=[];start=0
 for m in re.finditer(r'(?<=[.!?])\s+(?=[A-Z])',text):result.append([start,m.start()]);start=m.end()
 return result+[[start,len(text)]]
STATUS={'R':'represented-bounded-source-clause-action-subset','U':'documented-but-outcome-U','G':'missing-selected-owner-clause-case-or-qualifier','O':'other-owner-context-not-newly-closed','M':'research-guidance-or-mechanism-context','E':'editorial-or-structural'}
def ref(kind,number):
 rows=load(K/(kind+'.json'));id=(f'REQ-CLIP-VIEW-{number:03}' if kind=='requirements' else f'CV-{number:03}') if isinstance(number,int) else number
 index=next(i for i,r in enumerate(rows) if r['id']==id);row=rows[index];field='contract' if kind=='requirements' else 'setup_and_action'
 return dict(id=id,catalog=str((K/(kind+'.json')).relative_to(ROOT)),json_pointer=f'/{index}/{field}',scoped_predicate=row[field],value_sha256=sha256(row[field].encode()).hexdigest(),role='Exact quoted predicate/action; only the stated assessed subset is represented, never whole-ID closure.')

def build():
 source=load(K/'source.json');raw=(K/source['file']).read_text();assert digest(K/source['file'])=={k:source[k] for k in ['bytes','sha256']}
 blocks,resources=runpy.run_path(str(P/'source_parser.py'))['extract'](raw,'CV')
 old=load(K/'manual-blocks.json');assert len(blocks)==len(old)==180
 assert all((a['id'],a['kind'],a['text'],a['html_line'])==(b['locator'],b['kind'],b['text'],b['html_line']) for a,b in zip(blocks,old))
 plan=load(P/'claim-plan.json');claims=[]
 for bi,b in enumerate(blocks):
  rows=[dict(sentence=0,disposition='E',requirements=[],cases=[],gaps=[],assessment='Literal numbered heading/ancestry only; not semantic leaf coverage.')] if b['kind'].startswith('h') else plan[b['id']]
  parts=[[0,len(b['text'])]] if b['kind'].startswith('h') else spans(b['text'])
  assert [r['sentence'] for r in rows]==list(range(len(parts)))
  for x,(a,z) in zip(rows,parts):
   claims.append(dict(id=f'CVA-C{len(claims)+1:03}',block=b['id'],block_json_pointer=f'/{bi}',sentence=x['sentence'],text_span=[a,z],source_excerpt=b['text'][a:z],excerpt_sha256=sha256(b['text'][a:z].encode()).hexdigest(),source_locator=dict(source_id=source['id'],source_catalog=str((K/'source.json').relative_to(ROOT)),source_path=str((K/source['file']).relative_to(ROOT)),source_url=source['url'],source_sha256=source['sha256'],source_capture_utc=source['captured_utc'],source_version=source['version'],html_line=b['html_line'],html_column=b['html_column'],raw_start=b['raw_start'],raw_end=b['raw_end'],literal_anchor=b['attributes'].get('id'),heading_context=b['heading_context'],subsection_url=source['url']+'#'+b['heading_context'][-1]['anchor'],locator_limit='Raw offsets are decoded Unicode character positions; heading ancestry is source context, not a direct TOC match or inherited paragraph anchor.'),disposition=STATUS[x['disposition']],assessment=x['assessment'],requirements=[ref('requirements',i) for i in x['requirements']],cases=[ref('cases',i) for i in x['cases']],proposal_groups=['CVA-'+g for g in x['gaps']],target='U',actual_expected=None,actual_comparison=None,executed=False,complete=False,behavioral_coverage_credit=0))
 for i,r in enumerate(resources,1):
  r.update(id=f'CVA-R{i:03}',source_id=source['id'],source_sha256=source['sha256'],source_url=source['url'],source_capture_utc=source['captured_utc'],target='U',complete=False,pixels_or_destination_inspected=False,scope='Literal text/attributes read; no image pixels or separately followed destination. Internal target prose was read only as part of this retained chapter.',disposition='editorial-caption-label-read' if r['kind']=='caption' else 'image-pixels-uninspected' if r['kind']=='image' else 'linked-destination-not-separately-inspected')
 proposals=[]
 for x in load(P/'proposed-deltas.json'):
  row=dict(x);row.update(claim_ids=[c['id'] for c in claims if x['id'] in c['proposal_groups']],status='audit-only proposed owner reconciliation; no normative IDs or current owner edits',positive_guard=dict(admitted_exact_feature_mode_history_and_focus=True,independently_valid_owned_nonempty_source=True,active_unmuted_nonzero_output_where_applicable=True,paired_successful_functioning_baseline_before_negative=True,requires_functioning_scroll_before_edit=x['baseline']=='functioning-follow',missing_or_failed_prerequisite_stays_U=True,fixtures_or_runtime_results_supplied=False),documentary_expected=None,documentary_comparison=None,expected=None,comparison=None,target='U',executed=False,complete=False,behavioral_coverage_credit=0)
  assert row['claim_ids'];proposals.append(row)
 reverse={}
 for kind in ['requirements','cases']:
  rows=load(K/(kind+'.json'));reverse[kind]=[]
  for i,r in enumerate(rows):
   matched=[c for c in claims if any(t['id']==r['id'] for t in c[kind])]
   reverse[kind].append(dict(id=r['id'],catalog=str((K/(kind+'.json')).relative_to(ROOT)),json_pointer=f'/{i}',source_facets=[c['id'] for c in matched],represented_subset_facets=[c['id'] for c in matched if c['disposition']==STATUS['R']],status='Partial source/action reconciliation; no complete requirement/case' if matched else 'Existing explicit U operational obligation retained; no new source oracle or closure',target='U',complete=False))
 headings=[]
 for b in blocks:
  if b['kind'].startswith('h'):
   ids=[c['id'] for c in claims if any(h['anchor']==b['attributes']['id'] for h in c['source_locator']['heading_context'])]
   headings.append(dict(block=b['id'],anchor=b['attributes']['id'],number=b['attributes'].get('data-number'),heading=b['text'],source_url=source['url']+'#'+b['attributes']['id'],structural_descendant_facets=ids,semantics='Exact retained heading ancestry only; no TOC alias or complete leaf credit.',complete=False))
 summary=dict(scope='Full retained chapter8 textual reconciliation only; source/accounting and proposals, no owner or product completion',source_blocks=len(blocks),block_kinds=dict(Counter(b['kind'] for b in blocks)),source_text_characters=sum(len(b['text']) for b in blocks),source_tables=sum(b['kind']=='tr' for b in blocks),facets=len(claims),dispositions=dict(Counter(c['disposition'] for c in claims)),resources=len(resources),resource_kinds=dict(Counter(r['kind'] for r in resources)),requirements=54,cases=62,proposed_groups=len(proposals),all_actual_oracles_null_U=True,executed=0,new_normative_IDs=0,behavioral_coverage_credit=0,complete_topics=0,read_scope='All180 blocks/137paragraphs/6list items/37headings read with full sentence qualifiers; all54 actual contract bodies and62 actual setup/actions plus fixture read. All128 literal resource text/attributes read via compact projection of repeated image URL variants; pixels/destinations uninspected. Selected external clauses/actions only, no full cross-owner audit. Structural character coverage is an omission check, not proof of semantic sufficiency.')
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
