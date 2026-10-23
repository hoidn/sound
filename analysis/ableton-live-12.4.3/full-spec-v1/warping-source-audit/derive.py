"""Finite retained Warp chapter semantic ledger; no application or network calls.
Manual facets and sufficiency judgments are proposals, not coverage arithmetic.
--check is read-only; initial --write refuses once manifest.json exists.
"""
from pathlib import Path
from html.parser import HTMLParser
from hashlib import sha256
from collections import Counter
import json,re,sys
P=Path(__file__).resolve().parent;ROOT=P.parents[3];W=P.parent/'warping-workflows'
load=lambda q:json.loads(q.read_text())
def digest(q):
 b=q.read_bytes();return dict(bytes=len(b),sha256=sha256(b).hexdigest())
SENTENCE_RE=r'(?<=[.!?])\s+(?=[A-Z])'
STATUS={'R':'represented-supported-source-clause-and-case-subset','U':'documented-but-outcome-U','G':'missing-requirement-case-or-context','M':'research-or-guidance-context','E':'editorial','O':'routed-existing-owner-context'}
def sentences(text):
 spans=[];start=0
 for m in re.finditer(SENTENCE_RE,text):spans.append((start,m.start()));start=m.end()
 spans.append((start,len(text)));return [(a,z) for a,z in spans if text[a:z].strip()]
class Body(HTMLParser):
 def __init__(self,raw):
  super().__init__();self.raw=raw;self.offsets=[0]
  for m in re.finditer('\n',raw):self.offsets.append(m.end())
  self.depth=0;self.current=None;self.caption=None;self.link=None;self.blocks=[];self.resources=[];self.unassigned=[];self.heading=None
 def pos(self):
  line,col=self.getpos();return line,col,self.offsets[line-1]+col
 def handle_starttag(self,tag,attrs):
  attrs=dict(attrs)
  if tag=='div':
   if attrs.get('id')=='chapter_content':self.depth=1
   elif self.depth:self.depth+=1
  if not self.depth:return
  if tag in {'h1','h2','h3','h4','h5'}:self.heading=attrs.get('id')
  if self.current is None and tag in {'h1','h2','h3','h4','h5','p','li'}:
   line,col,offset=self.pos();self.current=dict(kind=tag,attributes=attrs,html_line=line,html_column=col,raw_start=offset,parts=[])
  if tag in {'a','img','figcaption'}:
   line,col,offset=self.pos();r=dict(kind={'a':'link','img':'image','figcaption':'caption'}[tag],html_line=line,html_column=col,raw_start=offset,attributes=attrs,starttag_sha256=sha256(self.get_starttag_text().encode()).hexdigest(),heading_context_anchor=self.heading)
   self.resources.append(r)
   if tag=='a':self.link=(r,[])
   if tag=='figcaption':self.caption=(r,[])
 def handle_data(self,value):
  if not self.depth:return
  if self.current is not None:self.current['parts'].append(value)
  if self.caption is not None:self.caption[1].append(value)
  if self.link is not None:self.link[1].append(value)
  if value.strip() and self.current is None and self.caption is None:self.unassigned.append(dict(html_line=self.getpos()[0],text=value))
 def handle_endtag(self,tag):
  if not self.depth:return
  if self.current is not None and tag==self.current['kind']:
   row=self.current;self.current=None;row['text']=' '.join(''.join(row.pop('parts')).split());row['raw_end']=self.raw.find('>',self.pos()[2])+1
   if row['text']:row['raw_html']=self.raw[row['raw_start']:row['raw_end']];self.blocks.append(row)
  if tag=='a' and self.link is not None:self.link[0]['text']=' '.join(''.join(self.link[1]).split());self.link=None
  if tag=='figcaption' and self.caption is not None:self.caption[0]['text']=' '.join(''.join(self.caption[1]).split());self.caption=None
  if tag=='div':self.depth-=1
OWN={
 'automation':[('automation-workflows','REQ-AUTO-WF-035','AW-035')],
 'sync':[('synchronization','REQ-SYNC-WORKFLOW-002','SYNC-002'),('synchronization','REQ-SYNC-WORKFLOW-011','SYNC-011'),('synchronization','REQ-SYNC-WORKFLOW-015','SYNC-015')],
 'video':[('video-workflows','REQ-VIDEO-WORKFLOW-011','VID-011')],
 'clip-entry':[('clip-view','REQ-CLIP-VIEW-001','CV-001')],
 'clip-warp':[('clip-view','REQ-CLIP-VIEW-018','CV-018')],
 'clip-follow':[('clip-view','REQ-CLIP-VIEW-031','CV-031')],
 'clip-quant':[('clip-view','REQ-CLIP-VIEW-028','CV-028')]
}
def ref(packet,name,id,field):
 q=P.parent/packet/name;rows=load(q);i=next(i for i,x in enumerate(rows) if x['id']==id);r=rows[i]
 result=dict(id=id,catalog=str(q.relative_to(ROOT)),json_pointer=f'/{i}/{field}',value_sha256=sha256(r[field].encode()).hexdigest())
 if name=='cases.json':result.update(kind=r['kind'],requirements=r['requirements'],documentary_expected_is_null=r['documentary_expected'] is None,documentary_comparator_is_null=r['documentary_comparator'] is None,expected_is_null=r['expected'] is None,comparison_is_null=r['comparison'] is None,target_grade=r['target_grade'],executed=r['executed'])
 else:result.update(provenance=r.get('provenance',r.get('strength')),target_applicability=r['target_applicability'])
 return result

def build():
 blocks=load(W/'manual-blocks.json');plan=load(P/'claim-plan.json');source=load(W/'sources.json')[0]
 assert digest(W/'manifest-author-r1.json')['sha256']=='b17efb2eb29b165239bab421e53e49f69117e69fa80f97927ad0e54dac76ba68'
 assert len(blocks)==131 and set(plan)=={str(i) for i,b in enumerate(blocks,1) if not b['kind'].startswith('h')}
 raw=(W/source['path']).read_text();body=Body(raw);body.feed(raw)
 assert len(body.blocks)==len(blocks)==131 and not body.unassigned,body.unassigned
 claims=[];reconciliation=[]
 for bi,(block,parsed) in enumerate(zip(blocks,body.blocks)):
  assert block['kind']==parsed['kind'] and block['text']==parsed['text'] and block['html_line']==parsed['html_line']
  ranges=[(0,len(block['text']))] if block['kind'].startswith('h') else sentences(block['text']);rows=plan.get(str(bi+1),[[0,'Source heading/hierarchy','E',[],[],[],'Exact heading preserved; no app outcome inferred.']]);ids=[]
  for row in rows:
   si,facet,code,reqnums,casenums,gaps,note,*owner=row;assert code in STATUS and 0<=si<len(ranges)
   a,z=ranges[si];quote=block['text'][a:z];id=f'WARPA-C{len(claims)+1:03}';ids.append(id)
   rr=[ref('warping-workflows','requirements.json',f'REQ-WFW-{x:03}' if isinstance(x,int) else 'REQ-WFW-'+x,'contract') for x in reqnums]
   cc=[ref('warping-workflows','cases.json',f'WFW-{x:03}','setup_and_action') for x in casenums]
   routes=[]
   for key in owner:
    for packet,rid,cid in OWN[key]:routes.append(dict(requirement=ref(packet,'requirements.json',rid,'contract'),case=ref(packet,'cases.json',cid,'setup_and_action'),scope='partial existing owner context; target U; not a new Warp or numerical contract'))
   h=block['heading_context'][-1]
   claims.append(dict(id=id,block=block['locator'],sentence=si,facet=facet,disposition=STATUS[code],assessment=note,gaps=gaps,text_span=[a,z],source_excerpt=quote,source_excerpt_sha256=sha256(quote.encode()).hexdigest(),source_locator=dict(source_id=source['id'],source_sha256=source['sha256'],source_version=source['declared_version'],source_capture_utc=source['captured_utc'],source_url=source['url'],block_catalog=str((W/'manual-blocks.json').relative_to(ROOT)),block_json_pointer=f'/{bi}',block_text_json_pointer=f'/{bi}/text',html_line=block['html_line'],html_column=parsed['html_column'],literal_anchor=block['anchor'],literal_anchor_url=source['url']+'#'+block['anchor'] if block['anchor'] else None,heading_context=block['heading_context'],heading_context_url=source['url']+'#'+h['anchor'],anchor_role='Paragraph anchor remains literal null; heading context is not its own ID, TOC match or semantic topic coverage.'),existing_requirements=rr,existing_cases=cc,existing_owner_routes=routes,existing_clause_sufficient_for_stated_subset=code in {'R','U'} and any(r['provenance']=='D12' for r in rr),existing_case_action_explicit_for_stated_subset=code in {'R','U'} and bool(cc),related_context_only=code in {'G','M','E'} or any(r['provenance']=='U' for r in rr),target_applicability='U',behavioral_coverage_credit=0,complete=False))
  reconciliation.append(dict(block=block,source_json_pointer=f'/{bi}',raw_paragraph_or_heading=parsed,claim_ids=ids,all_nonwhitespace_text_accounted_for=True,complete=False,target_applicability='U'))
 resources=[]
 for i,r in enumerate(body.resources):
  x=dict(r,id=f'WARPA-R{i+1:03}',disposition='caption-text-read; not image proof' if r['kind']=='caption' else 'image-or-linked-destination-uninspected',source_sha256=source['sha256'],target_applicability='U',complete=False,behavioral_coverage_credit=0)
  x['scope']='Literal retained markup/text/URL only. No image pixels, image-derived labels/palettes/coordinates, linked destination content, network or rendering inspection.'
  resources.append(x)
 proposals=[]
 guard='Future evidence only, not execution authorization: independently admitted exact-build feature/control, valid owned nonempty readable source and accepted short/long/loop/transient/marker identities. Retain preferences, first/prior analysis/default/save history, view/focus/selection, actual transport/leader/receiver/mode. Genuine positive relevant processing, nonmuted source/wet/return/output and independently nonzero amount/transpose/stretch where applicable must precede absence/no-effect/failure probes. Missing input/feature, wrong mode, zero/muted/dry-only path or failed baseline remains U, never a negative pass. No fixtures or runtime results supplied.'
 for i,g in enumerate(load(P/'proposed-deltas.json')):
  row=dict(g);row.update(catalog_pointer=f'/{i}',claim_ids=[c['id'] for c in claims if g['id'] in c['gaps']],source_blocks=sorted({c['block'] for c in claims if g['id'] in c['gaps']}),status='audit proposal only; not a current normative requirement/case or rejection of old partial approval',positive_guard=guard,documentary_expected=None,documentary_comparator=None,expected=None,comparison=None,target_grade='U',executed=False,behavioral_coverage_credit=0)
  assert row['claim_ids'];proposals.append(row)
 reqs=load(W/'requirements.json');cases=load(W/'cases.json');catalog=dict(requirements=[],cases=[])
 for name,rows,key in [('requirements',reqs,'existing_requirements'),('cases',cases,'existing_cases')]:
  for i,r in enumerate(rows):
   matches=[c for c in claims if any(x['id']==r['id'] for x in c[key])]
   catalog[name].append(dict(id=r['id'],catalog=str((W/(name+'.json')).relative_to(ROOT)),json_pointer=f'/{i}',claim_ids=[c['id'] for c in matches],supported_subset_claims=[c['id'] for c in matches if c['disposition'] in {STATUS['R'],STATUS['U']}],gap_or_related_context_claims=[c['id'] for c in matches if c['disposition']==STATUS['G']],status='partial assessed source/action subsets only' if matches else 'generic future unknown obligation; no direct documentary facet claimed',target_applicability='U',complete=False))
 questions=[dict(id='WA-Q01',topic='Version and initial/default contexts',state='U',detail='Current Version12 source is not target12.4.3. Initial preference/leader/default history differs from explicit edits, saved markers/ASD/custom settings/reset/migration.'),dict(id='Q-032',topic='Import/readiness preserved open',state='open',snapshot='owner-snapshots/Q032.md',detail='All-first-import playback/edit gating versus media long-analysis wording, command/drag destinations and exact formats/platform/class/history remain unresolved. No universal new codec/readiness law.'),dict(id='WA-Q02',topic='Native finite boundary',state='unchanged',detail='Existing held-after-open A2/A3/A4, scripting numeric/enum/default/shadow/list/conversion laws and released evidence remain scoped. Current public interactive/automatic prose settles none of those assumptions and supplies no native audio or generated-marker oracle.'),dict(id='WA-Q03',topic='Short/long example and marker contexts',state='U',detail='Source enabled short-policy wording is not a fifth/binary choice or Auto-always-warp. Per-bar long markers, two short-loop endpoints, odd nine/eight/bar-eight advice and actual source/display/region lengths remain separate; do not silently repair a source example.'),dict(id='WA-Q04',topic='Leader and the two Follow roles',state='U',detail='Actually active leader and genuinely generated automation/actual Tempo Follower interpretation differ from flags and active input. Editor Follow scrolling is a different function. No leader-election/clock/precedence/restoration family is supplied.'),dict(id='WA-Q05',topic='Preroll, tap history and transport boundaries',state='U',detail='Four taps is a source4/4 example; no other-meter count, recording count-in/preroll, initial phrase/position, Link deadline or tap estimator/accuracy law follows. Retain offered preroll/transport contexts only as independently admitted future unknowns, not default values.'),dict(id='WA-Q06',topic='Lifecycle and boundaries',state='U',detail='Existing generic boundary/undo/cancel/save/reopen/automation/loss/rate/recovery/teardown/error cases stay unexecuted and incomplete. Finite action labels do not establish admission/partial effects or a no-effect result.'),dict(id='WA-Q07',topic='Mechanisms, source recommendations and resources',state='research/uninspected',detail='Grains/crossings/pitch clarity/RNG/private model and quality/CPU descriptions impose no candidate algorithm, distribution, numeric/quality/stress or output inequality. Resource attributes/captions/links are retained; image pixels and linked pages/PDFs are not inspected.')]
 summary=dict(scope='Full retained Warp chapter paragraph/facet reconciliation only; no chapter/application completion',source_blocks=131,source_headings=sum(b['kind'].startswith('h') for b in blocks),paragraphs=sum(b['kind']=='p' for b in blocks),list_items=sum(b['kind']=='li' for b in blocks),claim_context_records=len(claims),dispositions=dict(Counter(c['disposition'] for c in claims)),resource_records=len(resources),resource_kinds=dict(Counter(r['kind'] for r in resources)),original_requirements=50,original_cases=88,proposed_delta_groups=len(proposals),all_target_U=True,new_normative_requirements=0,executed=0,behavioral_coverage_credit=0,completed_topics=0,source_read_scope='All131 blocks, every paragraph/list sentence and qualifiers manually read against all50 clauses/all88 actions/fixtures. Manual plan facets can share a literal sentence; character accounting is an omission check, not proof all implications were found. All copied owner contexts are as-of snapshots; only stated relevant owner subsets were semantically read. Image pixels/linked pages and original functions uninspected/unexecuted.')
 return {'claims.json':claims,'block-reconciliation.json':reconciliation,'resources.json':resources,'proposed-deltas-derived.json':proposals,'existing-catalog-dispositions.json':catalog,'source-questions.json':questions,'summary.json':summary}

def main():
 assert sys.argv[1:] in (['--check'],['--write']),'choose read-only --check or initial --write'
 if sys.argv[1:]==['--write']:assert not (P/'manifest.json').exists(),'refuse overwrite after seal'
 d=build()
 for name,value in d.items():
  if sys.argv[1:]==['--check']:assert load(P/name)==value,name
  else:(P/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
 print(json.dumps(d['summary.json'],indent=2))
if __name__=='__main__':main()
