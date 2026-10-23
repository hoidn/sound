"""Finite MPE source reconciliation. Only analyst HTML/JSON/Markdown data; no host calls."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
import json,re,runpy,sys
P=Path(__file__).resolve().parent;ROOT=P.parents[3];K=P.parent/'mpe-tuning-grooves'
load=lambda p:json.loads(p.read_text())
def digest(p):
 b=p.read_bytes();return dict(bytes=len(b),sha256=sha256(b).hexdigest())
def pointer(o,ptr):
 for k in ptr.strip('/').split('/'):o=o[int(k)] if isinstance(o,list) else o[k.replace('~1','/').replace('~0','~')]
 return o
STATUS={'R':'represented-bounded-source-clause-action-subset','U':'documented-but-outcome-U','G':'missing-selected-owner-clause-case-or-qualifier','O':'other-owner-context-not-newly-closed','M':'research-guidance-context','E':'editorial-or-structural'}
def catalog():
 t=(P/'spec-asof-r2.md').read_text();req=[]
 for m in re.finditer(r'^\| (REQ-MPE-\d{3}) \|.*$',t,re.M):
  c=[x.strip() for x in m[0].strip('|').split('|')];assert len(c)==4
  req.append(dict(id=c[0],inputs=c[1],contract=c[2],evidence=c[3],snapshot='spec-asof-r2.md',markdown_span=list(m.span()),original_markdown=m[0]))
 cases=[dict(id=r['id'],original_catalog=str((K/'cases.json').relative_to(ROOT)),original_json_pointer=f'/{i}',original_record=r) for i,r in enumerate(load(K/'cases.json')) if r['id'].startswith('MPE-')]
 assert len(req)==18 and len(cases)==27 and [r['id'] for r in cases]==[f'MPE-{i:03}' for i in range(1,28)]
 a=t.index('## Inputs, units and state');z=t.index('## Requirements',a)
 return dict(requirements=req,cases=cases,common_fixture=dict(snapshot='spec-asof-r2.md',text_span=[a,z],text=t[a:z],role='Future scenario recipe; no actual fixtures or target numeric domain'))
def ref(cat,kind,n):
 r=cat[kind][n-1]
 if kind=='requirements':return dict(id=r['id'],catalog=str((P/'owner-catalog-asof.json').relative_to(ROOT)),json_pointer=f'/requirements/{n-1}',quoted_scoped_predicate=r,role='Exact Markdown table-row transcription; not an original machine requirement catalog')
 return dict(id=r['id'],catalog=r['original_catalog'],json_pointer=r['original_json_pointer'],quoted_scoped_predicate=r['original_record'],role='Exact original shared catalog record, scoped setup/action and documentary predicate only; expected is not an actual oracle')
def guards(plan,props):
 assert plan['MPE-B013'][0]['disposition']=='G' and plan['MPE-B016'][1]['disposition']=='G','Meter/default or selected/background action mismatch'
 assert plan['MPE-B034'][0]['disposition']=='U','Fold/optional-lane context must remain unknown'
 for g in props:
  assert g['target']=='U' and g['executed'] is g['complete'] is False and g['coverage_credit']==0
  assert all(g[k] is None for k in ['expected','comparison','documentary_expected','documentary_comparison','actual_expected','actual_comparison'])
  assert all(g['positive_guard'][k] is True for k in ['admitted_control_and_operation','confirmed_admissible_UI_values','genuinely_nonzero_independent_per_note_expression_before_exclusion','productive_controller_route_not_merely_indicator','nonmuted_active_receiver_and_nonzero_depth_where_relevant','failed_prerequisite_stays_U'])
  assert g['positive_guard']['fixtures_supplied'] is False and g['positive_guard']['controller_required_for_offline_editor'] is False

def build():
 sc=load(P/'source-context.json');meta=pointer(load(ROOT/sc['catalog']),sc['json_pointer']);assert sc['capture_date']==meta['captured'] and sc['capture_utc'] is None and digest(ROOT/sc['path'])=={k:sc[k] for k in ['bytes','sha256']}
 raw=(ROOT/sc['path']).read_text();blocks,resources=runpy.run_path(str(P/'source_parser.py'))['extract'](raw,'MPE');cat=catalog();plan=load(P/'claim-plan.json');ext=load(P/'selected-owner-contexts.json');mapping=load(P/'external-reference-plan.json');claims=[]
 for bi,b in enumerate(blocks):
  rows=[dict(sentence=0,text_span=[0,len(b['text'])],disposition='E',requirements=[],cases=[],groups=[],assessment='Literal numbered chapter heading/ancestry only; no semantic leaf or directTOC completion.')] if b['kind'].startswith('h') else plan[b['id']]
  prev=0
  for x in rows:
   a,z=x['text_span'];assert not b['text'][prev:a].strip() and a<z<=len(b['text']);prev=z
   claims.append(dict(id=f'MPA-C{len(claims)+1:03}',source_block=b['id'],block_pointer=f'/{bi}',sentence=x['sentence'],text_span=[a,z],source_excerpt=b['text'][a:z],excerpt_sha256=sha256(b['text'][a:z].encode()).hexdigest(),source_locator=dict(source_id=sc['source_id'],source_path=sc['path'],source_url=sc['url'],source_sha256=sc['sha256'],capture_date=sc['capture_date'],capture_utc=None,version=sc['version'],html_line=b['html_line'],html_column=b['html_column'],raw_start=b['raw_start'],raw_end=b['raw_end'],literal_anchor=b['attributes'].get('id'),heading_context=b['heading_context'],locator_limit='Offsets count decodedUnicode characters; actual ancestry not a paragraph anchor or semantic leaf coverage'),disposition=STATUS[x['disposition']],assessment=x['assessment'],requirements=[ref(cat,'requirements',n) for n in x['requirements']],cases=[ref(cat,'cases',n) for n in x['cases']],selected_external_contexts=[dict(catalog='selected-owner-contexts.json',json_pointer=f'/{i}',id=ext[i]['id']) for i in mapping.get(b['id'],[])],proposal_groups=x['groups'],actual_expected=None,actual_comparison=None,target='U',executed=False,complete=False,coverage_credit=0))
  assert not b['text'][prev:].strip()
 for i,r in enumerate(resources):r.update(id=f'MPA-R{i+1:03}',source_path=sc['path'],source_sha256=sc['sha256'],source_url=sc['url'],capture_date=sc['capture_date'],capture_utc=None,literal_container_block=next((b['id'] for b in blocks if b['raw_start']<=r['raw_start']<b['raw_end']),None),disposition='caption-label-read' if r['kind']=='caption' else 'image-pixels-uninspected' if r['kind']=='image' else 'linked-destination-uninspected',scope='Every literal attribute/URL variant/text/caption read as data; image pixels and separate destinations uninspected',pixels_or_destination_inspected=False,complete=False,target='U')
 props=load(P/'proposed-deltas.json');guards(plan,props)
 for g in props:g.update(source_facets=[c['id'] for c in claims if g['id'] in c['proposal_groups']],existing_case_refs=[ref(cat,'cases',n) for n in g.pop('case_numbers')]);assert g['source_facets']
 reverse={kind:[dict(id=r['id'],catalog='owner-catalog-asof.json',json_pointer=f'/{kind}/{i}',source_facets=[c['id'] for c in claims if any(x['id']==r['id'] for x in c[kind])],status='Selected renderedFAQ supports configured matching-range role only' if r['id'] in ['REQ-MPE-018','MPE-018'] else 'Partial retained chapter/action reconciliation, not completeID' if any(any(x['id']==r['id'] for x in c[kind]) for c in claims) else 'Existing explicit boundary/lifecycle U retained; no source/runtime oracle invented',actual_expected=None,actual_comparison=None,target='U',complete=False) for i,r in enumerate(cat[kind])] for kind in ['requirements','cases']}
 faq=load(P/'faq-context.json');faq.update(requirements=[ref(cat,'requirements',18)],cases=[ref(cat,'cases',18)],disposition='Documented matching-configuration prerequisite; tracking sound/defaults/codec outcomeU',complete=False,coverage_credit=0)
 headings=[dict(block=b['id'],anchor=b['attributes']['id'],number=b['attributes']['data-number'],heading_context=b['heading_context'],source_url=sc['url']+'#'+b['attributes']['id'],descendant_facets=[c['id'] for c in claims if any(h['anchor']==b['attributes']['id'] for h in c['source_locator']['heading_context'])],role='Actual retained heading ancestry only, no directTOC match or leaf completion',complete=False) for b in blocks if b['kind'].startswith('h')]
 summary=dict(scope='Entire retained Editing MPE chapter 12 versus selected MPE owner; selected FAQ matching-range and 14 neighboring MIDI tool blocks are context only',source_blocks=len(blocks),block_kinds=dict(Counter(b['kind'] for b in blocks)),source_tables=sum(b['kind']=='tr' for b in blocks),source_text_characters=sum(len(b['text']) for b in blocks),facets=len(claims),dispositions=dict(Counter(c['disposition'] for c in claims)),resources=len(resources),resource_kinds=dict(Counter(r['kind'] for r in resources)),requirements=18,cases=27,shared_packet_requirements=53,shared_packet_cases=83,selected_external_contexts=len(ext),proposal_groups=len(props),capture_UTC_supplied=False,all_actual_oracles_null_U=True,executed=0,new_normative_IDs=0,coverage_credit=0,complete_topics=0,read_scope='All 66 chapter blocks/31 paragraphs/26 list items/9 headings, 18 actual clause rows/27 actual actions and predicates/common recipe read. All 28 literal resources text/attributes/captions read; pixels/destinations uninspected. Only selected rendered FAQ L102–106, 14 raw Glissando/LFO blocks and 26 actual external records/spans read; no full FAQ/MIDI/tools/device/controller review. Source character accounting detects omissions only, not semantic sufficiency.')
 return {'source-blocks.json':blocks,'resources.json':resources,'owner-catalog-asof.json':cat,'claims.json':claims,'proposed-deltas-derived.json':props,'existing-catalog-reconciliation.json':reverse,'faq-reconciliation.json':faq,'subsection-routing.json':headings,'summary.json':summary}
def main():
 assert sys.dont_write_bytecode and sys.argv[1:] in (['--check'],['--write'])
 if sys.argv[1:]==['--write']:assert not (P/'manifest.json').exists(),'refuse overwrite after seal'
 watched=[p for p in P.rglob('*') if p.is_file()]+[ROOT/r['path'] for r in load(P/'input-pins.json')];before={str(p):digest(p) for p in watched}
 built=build()
 for n,v in built.items():
  if sys.argv[1:]==['--check']:assert load(P/n)==v,n
  else:(P/n).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
 if sys.argv[1:]==['--check']:assert before=={str(p):digest(p) for p in watched}
 print(json.dumps(built['summary.json'],indent=2))
if __name__=='__main__':main()
