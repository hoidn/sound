"""Finite data-only retained HTML/Markdown reconciliation. --check is read-only."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
import json,re,runpy,sys
P=Path(__file__).resolve().parent;ROOT=P.parents[3]
load=lambda p:json.loads(p.read_text())
def digest(p):
 b=p.read_bytes();return dict(bytes=len(b),sha256=sha256(b).hexdigest())
def pointer(data,p):
 for x in p.strip('/').split('/'):
  data=data[int(x)] if isinstance(data,list) else data[x.replace('~1','/').replace('~0','~')]
 return data
STATUS={'R':'represented-bounded-source-clause-action-subset','U':'documented-but-outcome-U','G':'missing-selected-owner-clause-case-or-qualifier','O':'other-owner-context-not-newly-closed','M':'research-guidance-context','E':'editorial-or-structural'}
def catalog():
 t=(P/'spec-asof-r1.md').read_text();req=[];cases=[]
 matches=list(re.finditer(r'^### (REQ-ARRANGEMENT-\d{3})[^\n]*\n',t,re.M))
 for m in matches:
  n=re.search(r'^##?\s|^###\s',t[m.end():],re.M);z=m.end()+n.start() if n else len(t)
  req.append(dict(id=m[1],snapshot='spec-asof-r1.md',markdown_span=[m.start(),z],original_markdown=t[m.start():z],contract=t[m.end():z],target='U',complete=False))
 for m in re.finditer(r'^\| (AR-\d{3}) \|.*$',t,re.M):
  cells=[c.strip() for c in m[0].strip('|').split('|')];assert len(cells)==5
  cases.append(dict(id=cells[0],requirement_suffix=cells[1],kind=cells[2],setup_and_action=cells[3],original_documentary_predicate=cells[4],snapshot='spec-asof-r1.md',markdown_span=list(m.span()),original_markdown=m[0],actual_expected=None,actual_comparison=None,target='U',executed=False,complete=False))
 assert len(req)==35 and len(cases)==65
 fixture=t[t.index('Fixtures below are reproducible'):t.index('| Case | Requirement suffix')]
 return dict(requirements=req,cases=cases,fixture=dict(snapshot='spec-asof-r1.md',text=fixture,text_span=[t.index(fixture),t.index(fixture)+len(fixture)],role='Future scenario definition; no actual media/Set or execution supplied'))
def ref(cat,kind,n):
 rows=cat[kind];i=n-1;r=rows[i];f='contract' if kind=='requirements' else 'setup_and_action'
 return dict(id=r['id'],catalog='owner-catalog-asof.json',json_pointer=f'/{kind}/{i}/{f}',quoted_scoped_predicate=r[f],text_sha256=sha256(r[f].encode()).hexdigest(),original_snapshot=r['snapshot'],original_markdown_span=r['markdown_span'],role='Derived exact Markdown transcription, not an original machine catalog; assessed subset only')
def guard(plan,props):
 assert not plan['ARR-B106'][0]['requirements'] and not plan['ARR-B106'][0]['cases'],'Select Loop is not inverse Loop Selection case coverage'
 assert all(x['disposition']=='G' for x in plan['ARR-B026']),'Follow action needs productive running baseline'
 assert plan['ARR-B040'][0]['disposition']=='U','Chase prose is not a note output oracle'
 assert all('ASA-G10' in x['groups'] for x in plan['ARR-B156']),'Same-start positive before linked mismatch'
 for x in props:
  assert x['target']=='U' and x['executed'] is False and x['complete'] is False
  assert all(x[k] is None for k in ['expected','comparison','documentary_expected','documentary_comparison','actual_expected','actual_comparison'])
  assert x['positive_guard']['active_nonempty_audible_baseline_before_suppression'] is True
  if x['id']=='ASA-G04':assert x['specific_positive_baseline']=='Genuinely moving playhead and independently observed automatic scrolling before edit/scroll/ruler pause.'
  if x['id']=='ASA-G10':assert x['same_start_fade_positive_before_different_start_negative'] is True
  if x['id']=='ASA-G14':assert x['genuine_nonzero_active_processed_return_before_bypass'] is True

def build():
 cat=catalog();plan=load(P/'claim-plan.json');ext=load(P/'selected-owner-contexts.json');mapping=load(P/'external-reference-plan.json');blocks=[];resources=[];claims=[];contexts=load(P/'source-context.json')
 for sc in contexts:
  raw=(ROOT/sc['source']).read_text();meta=load(ROOT/sc['metadata']);sourceblocks,res=runpy.run_path(str(P/'source_parser.py'))['extract'](raw,sc['id'])
  if sc['id']=='CON':
   selected={'arrangement-and-session','tracks','audio-and-midi'}
   sourceblocks=[b for b in sourceblocks if b['heading_context'][-1]['anchor'] in selected];res=[r for r in res if r['heading_context_anchor'] in selected]
  for b in sourceblocks:b.update(source_path=sc['source'],source_sha256=digest(ROOT/sc['source'])['sha256'],source_url=meta['url'],source_capture_utc=meta.get('capture_utc',meta.get('captured_utc')),source_version=meta.get('version',meta.get('version_statement')),scope=sc['selection'])
  blocks+=sourceblocks
  for r in res:r.update(source_path=sc['source'],source_sha256=digest(ROOT/sc['source'])['sha256'],source_url=meta['url'],source_capture_utc=meta.get('capture_utc',meta.get('captured_utc')))
  resources+=res
 for bi,b in enumerate(blocks):
  rows=[dict(sentence=0,text_span=[0,len(b['text'])],disposition='E',requirements=[],cases=[],groups=[],assessment='Literal numbered heading and retained ancestry only; no leaf semantic or direct TOC match coverage.')] if b['kind'].startswith('h') else plan[b['id']]
  prev=0
  for x in rows:
   a,z=x['text_span'];assert not b['text'][prev:a].strip() and a<z<=len(b['text']);prev=z
   claims.append(dict(id=f'ASA-C{len(claims)+1:03}',source_block=b['id'],block_pointer=f'/{bi}',sentence=x['sentence'],text_span=[a,z],source_excerpt=b['text'][a:z],excerpt_sha256=sha256(b['text'][a:z].encode()).hexdigest(),source_locator={k:b[k] for k in ['source_path','source_sha256','source_url','source_capture_utc','source_version','html_line','html_column','raw_start','raw_end','heading_context']},literal_paragraph_anchor=b['attributes'].get('id'),disposition=STATUS[x['disposition']],assessment=x['assessment'],requirements=[ref(cat,'requirements',n) for n in x['requirements']],cases=[ref(cat,'cases',n) for n in x['cases']],selected_external_contexts=[dict(catalog='selected-owner-contexts.json',json_pointer=f'/{i}',id=ext[i]['id'],role='Actual selected quoted clause/action only; no family closure') for i in mapping.get(b['id'],[])],proposal_groups=x['groups'],actual_expected=None,actual_comparison=None,target='U',executed=False,complete=False,behavioral_coverage_credit=0))
  assert not b['text'][prev:].strip()
 for i,r in enumerate(resources):
  r.update(id=f'ASA-R{i+1:03}',literal_container_block=next((b['id'] for b in blocks if b['source_path']==r['source_path'] and b['raw_start']<=r['raw_start']<b['raw_end']),None),container_role='Raw containment only, not inherited control semantics',disposition='caption-label-read' if r['kind']=='caption' else 'image-pixels-uninspected' if r['kind']=='image' else 'linked-destination-uninspected',scope='Literal text and every attribute/URL variant read as data; no image pixels or separate destination inspected',pixels_or_destination_inspected=False,complete=False,target='U')
 props=load(P/'proposed-deltas.json');guard(plan,props)
 for x in props:
  x['source_facets']=[c['id'] for c in claims if x['id'] in c['proposal_groups']];assert x['source_facets']
  x['existing_case_refs']=[ref(cat,'cases',n) for n in x.pop('case_numbers')]
 reverse={kind:[dict(id=r['id'],catalog='owner-catalog-asof.json',json_pointer=f'/{kind}/{i}',facets=[c['id'] for c in claims if any(v['id']==r['id'] for v in c[kind])],status='Partial textual clause/action reconciliation only; no complete ID' if any(any(v['id']==r['id'] for v in c[kind]) for c in claims) else 'Existing package-only representation or explicit lifecycle/boundary U retained; no new chapter source/result invented',target='U',complete=False) for i,r in enumerate(cat[kind])] for kind in ['requirements','cases']}
 headings=[dict(source_block=b['id'],anchor=b['attributes']['id'],number=b['attributes'].get('data-number'),source_url=b['source_url']+'#'+b['attributes']['id'],heading_ancestry=b['heading_context'],structural_descendant_facets=[c['id'] for c in claims if c['source_locator']['source_path']==b['source_path'] and any(h['anchor']==b['attributes']['id'] for h in c['source_locator']['heading_context'])],role='Actual numbered heading/ancestry, not direct TOC join or complete leaf coverage',complete=False) for b in blocks if b['kind'].startswith('h')]
 summary=dict(scope='Full retained Arrangement chapter 6 including 6.3 and 6.15, plus selected full Concepts 3.6–3.8; partial audit only',source_blocks=len(blocks),primary_arrangement_blocks=sum(b['source_path']==contexts[0]['source'] for b in blocks),selected_concepts_blocks=sum(b['source_path']==contexts[1]['source'] for b in blocks),block_kinds=dict(Counter(b['kind'] for b in blocks)),normalized_text_characters=sum(len(b['text']) for b in blocks),facets=len(claims),dispositions=dict(Counter(c['disposition'] for c in claims)),resources=len(resources),resource_kinds=dict(Counter(r['kind'] for r in resources)),requirements=35,cases=65,selected_external_context_records=len(ext),proposal_groups=len(props),all_actual_oracles_null_U=True,executed=0,new_normative_IDs=0,complete_topics=0,behavioral_coverage_credit=0,read_scope='All 164 Arrangement blocks/89p/57li/18headings and selected 22 Concepts blocks/19p/3headings read; all 35 actual contracts and 65 actual actions and fixture read. All 107 Arrangement and 30 selected Concepts literal resource attributes/text/captions read; image pixels/destinations uninspected. 109 selected external quoted clauses/actions plus selected fixture recipes read; not whole external families. Full source character/span accounting is omission detection only, not semantic sufficiency or target proof.')
 return {'source-blocks.json':blocks,'resources.json':resources,'owner-catalog-asof.json':cat,'claims.json':claims,'proposed-deltas-derived.json':props,'existing-catalog-reconciliation.json':reverse,'subsection-routing.json':headings,'summary.json':summary}
def main():
 assert sys.dont_write_bytecode and sys.argv[1:] in (['--check'],['--write'])
 if sys.argv[1:]==['--write']:assert not (P/'manifest.json').exists(),'refuse overwrite after seal'
 watched=[p for p in P.rglob('*') if p.is_file()]+[ROOT/x['path'] for x in load(P/'input-pins.json')];before={str(p):digest(p) for p in watched}
 result=build()
 for name,data in result.items():
  if sys.argv[1:]==['--check']:assert load(P/name)==data,name
  else:(P/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
 if sys.argv[1:]==['--check']:assert before=={str(p):digest(p) for p in watched},'read-only identities'
 print(json.dumps(result['summary.json'],indent=2))
if __name__=='__main__':main()
