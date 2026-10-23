"""Bounded retained Video source audit. Only analyst data/HTML is parsed; --check never writes."""
from pathlib import Path
from html.parser import HTMLParser
from collections import Counter
import hashlib,json,re,sys
P=Path(__file__).resolve().parent
ROOT=P.parents[3]
OLD=P.parent/'video-workflows'
SENTENCE_RE=r'(?<=[.!?])\s+(?=[A-Z])'
ALLOWED={'editorial','research-or-guidance-context','represented-supported-source-clause-and-case-subset','documented-but-outcome-U','missing-requirement-case-or-context','routed-existing-owner-context'}
def load(p):return json.loads(p.read_text())
def info(p):
 b=p.read_bytes();return dict(bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def pin(p,r):assert info(p)=={k:r[k] for k in ('bytes','sha256')},p
def pointer(v,path):
 if path=='':return v
 assert path.startswith('/')
 for k in path[1:].split('/'):
  k=k.replace('~1','/').replace('~0','~');v=v[int(k)] if isinstance(v,list) else v[k]
 return v
class Chapter(HTMLParser):
    def __init__(self,text):
        super().__init__();self.text=text;self.lines=text.splitlines(keepends=True);self.depth=0;self.active=None;self.anchor=None;self.rows=[];self.resource=None;self.resources=[]
    def position(self):
        line,col=self.getpos();return sum(len(x) for x in self.lines[:line-1])+col
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='div':
            if a.get('id')=='chapter_content':self.depth=1
            elif self.depth:self.depth+=1
        if not self.depth:return
        if tag in {'h1','h2','h3','h4','h5','h6','p','li'} and self.active is None:
            if tag.startswith('h'):self.anchor=a.get('id')
            self.active=dict(tag=tag,anchor=self.anchor,html_line=self.getpos()[0],html_column=self.getpos()[1],raw_start_tag=self.get_starttag_text(),attrs=[list(x) for x in attrs],text='',_start=self.position())
        if tag=='img':self.resources.append(dict(kind='image',html_line=self.getpos()[0],html_column=self.getpos()[1],attrs=[list(x) for x in attrs],text=None,inspection='image/link-uninspected; HTML attributes only; no fetch or pixel evidence'))
        if tag in {'a','figcaption'}:
            assert self.resource is None
            self.resource=dict(kind='link' if tag=='a' else 'caption',tag=tag,html_line=self.getpos()[0],html_column=self.getpos()[1],attrs=[list(x) for x in attrs],text='',inspection='image/link-uninspected; link destination not visited' if tag=='a' else 'editorial caption text read; image remains uninspected')
    def handle_data(self,data):
        if self.active is not None:self.active['text']+=data
        if self.resource is not None:self.resource['text']+=data
    def handle_endtag(self,tag):
        if self.active is not None and self.active['tag']==tag:
            r=self.active;r['text']=' '.join(r['text'].split());r['raw_html']=self.text[r.pop('_start'):self.position()+len('</'+tag+'>')]
            if r['text']:r['id']=f'VID-B{len(self.rows)+1:03d}';self.rows.append(r)
            self.active=None
        if self.resource is not None and self.resource['tag']==tag:
            r=self.resource;r['text']=' '.join(r['text'].split());self.resources.append(r);self.resource=None
        if tag=='div' and self.depth:self.depth-=1

def spans(text):
    rows=[];cursor=0
    for part in re.split(SENTENCE_RE,text):
        start=text.index(part,cursor);rows.append((start,start+len(part),part));cursor=start+len(part)
    return rows


def reconcile(blocks,claims):
 assert len(blocks)==39 and {c['block'] for c in claims}=={b['id'] for b in blocks}
 assert len({c['id'] for c in claims})==len(claims)
 for b in blocks:
  covered=set()
  for c in [x for x in claims if x['block']==b['id']]:
   a,z=c['text_span'];assert 0<=a<z<=len(b['text']) and b['text'][a:z]==c['source_excerpt'];covered.update(range(a,z))
  assert {i for i,ch in enumerate(b['text']) if not ch.isspace()}<=covered,b['id']
def selfchecks(blocks,claims):
 reconcile(blocks,claims)
 def reject(bs,cs):
  try:reconcile(bs,cs)
  except AssertionError:return
  raise AssertionError('Invalid ledger accepted')
 reject(blocks,[c for c in claims if c['block']!='VID-B029'])
 x=json.loads(json.dumps(claims));x[0]['source_excerpt']+=' changed';reject(blocks,x)
 x=json.loads(json.dumps(claims));x[0]['text_span']=[0,99999];reject(blocks,x)
 reject(blocks,claims+[claims[0]])
 assert pointer({'rows':[{'id':'x'}]},'/rows/0/id')=='x'
 try:pointer({'rows':[]},'/rows/1/id')
 except IndexError:pass
 else:raise AssertionError('Bad pointer accepted')
 f=Chapter('<p>outside</p><div id="chapter_content"><h1 id="v" data-number="28">28. Video</h1><p>A <b>bold</b> body.</p><ol><li>1.1.1 /00.00.00.00.</li></ol><img data-src="unfetched"><figcaption>Caption.</figcaption><a href="#v">Link</a></div><p>outside2</p>');f.feed(f.text)
 assert [r['text'] for r in f.rows]==['28. Video','A bold body.','1.1.1 /00.00.00.00.']
 assert Counter(r['kind'] for r in f.resources)=={'image':1,'caption':1,'link':1}
 assert spans('Start at1.1.1 /00.00.00.00. Another sentence.')[0][2]=='Start at1.1.1 /00.00.00.00.'
 return dict(dropped_block_rejected=True,altered_quote_rejected=True,invalid_span_rejected=True,duplicate_ID_rejected=True,invalid_JSON_pointer_rejected=True,chapter_body_inline_list_caption_resource_separation=True,timecode_not_split=True)
def derive():
 om=load(OLD/'manifest-author-r1.json');assert info(OLD/'manifest-author-r1.json')['sha256']=='ba9c19eb8836759b57c33e939aa294a390dd9d0199b00948396b769d0566467e'
 assert len(om['files'])==13
 for n,r in om['files'].items():pin(OLD/n,r)
 for p in load(P/'input-pins.json'):pin(ROOT/p['path'],p)
 for snap,path in om['canonical_snapshots'].items():assert (OLD/snap).read_bytes()==(ROOT/path).read_bytes()
 source=load(OLD/'source.json');raw=(OLD/source['file']).read_text();parser=Chapter(raw);parser.feed(raw);blocks=load(OLD/'source-blocks.json')
 assert len(parser.rows)==len(blocks)==39
 for r,b in zip(parser.rows,blocks):assert {k:r[k] for k in b}==b
 requirements=load(OLD/'requirements.json');cases=load(OLD/'cases.json');assert len(requirements)==18 and len(cases)==28
 rm={r['id']:(i,r) for i,r in enumerate(requirements)};cm={c['id']:(i,c) for i,c in enumerate(cases)};assert len(rm)==18 and len(cm)==28
 assert all(r['target_applicability']=='U' for r in requirements)
 assert all(c['expected'] is c['comparison'] is None and c['target_grade']=='U' and c['executed'] is False for c in cases)
 assert all(c['documentary_comparator'] is None for c in cases if c['kind'] in {'timing','signal'} or c['id'].startswith('VID-U-'))
 gaps={g['id']:g for g in load(P/'proposed-deltas.json')};assert len(gaps)==9
 for g in gaps.values():
  assert g['proposal_status']=='audit-proposal-only-not-current-normative-requirement' and g['behavioral_coverage_credit']==0 and g['positive_guard']
  for c in g['proposed_case_deltas']:assert all(c[k] is None for k in ['expected','comparison','documentary_expected','documentary_comparator']) and c['target_grade']=='U' and c['executed'] is False
 claims=[]
 for i,p in enumerate(load(P/'claim-plan.json'),1):
  b=next(b for b in blocks if b['id']==p['block']);j=blocks.index(b)
  a,z,quote=(0,len(b['text']),b['text']) if p['sentence'] is None else spans(b['text'])[p['sentence']]
  assert p['disposition'] in ALLOWED and p['assessment'] and set(p['gaps'])<=set(gaps)
  rs=[];cs=[]
  for suffix in p['requirement_suffixes']:
   rid='REQ-VIDEO-WORKFLOW-'+(f'{suffix:03}' if isinstance(suffix,int) else suffix);k,r=rm[rid]
   rs.append(dict(id=rid,catalog=str((OLD/'requirements.json').relative_to(ROOT)),json_pointer='/'+str(k),contract_json_pointer='/'+str(k)+'/contract',existing_contract=r['contract'],strength=r['strength'],direct_source_block_citation_present=any(e['block']==b['id'] for e in r['evidence']),evidence_role='supports explicitly assessed subset only' if p['existing_clause_sufficient_for_stated_subset'] else 'related/partial/unknown context, not coverage',is_runtime_proof=False))
  for cid in p['case_ids']:
   k,c=cm[cid];cs.append(dict(id=cid,catalog=str((OLD/'cases.json').relative_to(ROOT)),json_pointer='/'+str(k),action_json_pointer='/'+str(k)+'/setup_and_action',action=c['setup_and_action'],requirement_ids=c['requirements'],**{key:c[key] for key in ['documentary_expected','documentary_comparator','expected','comparison','target_grade','executed']},relationship='explicit action for assessed subset only' if p['existing_case_action_explicit_for_stated_subset'] else 'related/partial action, exact facet not enumerated'))
  for path in p['related_owner_context']:assert (ROOT/path).is_file()
  claims.append(dict(id=f'VIDA-C{i:03}',**p,text_span=[a,z],source_excerpt=quote,source_locator=dict(source_id=source['id'],source_sha256=source['sha256'],source_url=source['url'],source_version=source['version'],source_capture_utc=source['capture_utc'],source_catalog=str((OLD/'source.json').relative_to(ROOT)),source_json_pointer='',block_catalog=str((OLD/'source-blocks.json').relative_to(ROOT)),block_json_pointer='/'+str(j),block_text_json_pointer='/'+str(j)+'/text',html_line=b['html_line'],html_column=parser.rows[j]['html_column'],heading_context_anchor=b['anchor'],anchor_role='inherited heading context, not paragraph/list ID',exact_heading_url=source['url']+'#'+b['anchor']),existing_requirements=rs,existing_cases=cs,target_applicability='U',semantic_coverage='explicit subset assessment only; no complete behavior',behavioral_coverage_credit=0,complete=False))
 reconcile(blocks,claims)
 for g in gaps.values():
  assert g['supporting_claim_ids']==[c['id'] for c in claims if g['id'] in c['gaps']]
  assert {c['block'] for c in claims if c['id'] in g['supporting_claim_ids']}<=set(g['source_blocks'])
 questions=load(P/'source-questions.json');assert len(questions)==7 and len({q['id'] for q in questions})==7
 for q in questions:assert set(q['claim_ids'])<={c['id'] for c in claims} and q['status'].startswith('U;')
 reconciliation=[dict(block=b['id'],source_text=b['text'],source_tag=b['tag'],source_anchor=b['anchor'],raw_locator=r,claim_ids=[c['id'] for c in claims if c['block']==b['id']],all_normalized_nonwhitespace_text_assigned=True,meaning='Text omission guard only; analyst facets do not prove every semantic implication or branch complete') for b,r in zip(blocks,parser.rows)]
 toc=load(P.parent/'inventory/manual-toc.json');assert len(toc)==880 and sum(r['leaf'] for r in toc)==708 and len({r['url'].split('#')[0] for r in toc})==43
 routes=[]
 for h in [r for r in parser.rows if r['tag'].startswith('h')]:
  url=source['url']+'#'+h['anchor'];matches=[dict(json_pointer='/'+str(i),row=r) for i,r in enumerate(toc) if r['url']==url]
  routes.append(dict(block=h['id'],anchor=h['anchor'],heading_tag=h['tag'],heading_number=dict(h['attrs'])['data-number'],heading_text=h['text'],exact_url=url,original_TOC_matches=matches,join_rule='literal URL only; no aliases, normalization or ancestor join',route_role='actual retained heading only, not semantic coverage',complete=False,target_applicability='U'))
 r4path=P.parent/'inventory-revisions/r4-citation-crosswalk/unmatched-citations.json';pin(r4path,load(r4path.parent/'manifest.json')['files']['unmatched-citations.json']);unmatched=load(r4path);r4=[dict(catalog=str(r4path.relative_to(ROOT)),json_pointer='/'+str(i),record=r) for i,r in enumerate(unmatched) if r['packet']=='video-workflows']
 assert len(r4)==3 and {r['record']['evidence']['anchor'] for r in r4}=={'movies-with-partial-tracks','warp-markers'}
 context=dict(literal_labels=[dict(text=s,is_actual_heading=any(h['heading_text'].split(' ',1)[-1]==s for h in routes),alias_of=None) for s in ['Partial Movies','Partial Tracks','Movies with Partial Tracks']],rule='These three labels are not aliases. Only Movies with Partial Tracks is the actual retained heading; partial/truncated movie files and partial audio/video track intervals are distinct future contexts.',retained_R4_unmatched=r4,TOC_unmatched_actual_heading_URLs=[r['exact_url'] for r in routes if not r['original_TOC_matches']],meaning='R4 remains unchanged; actual h4 discovery does not repair literal original TOC matches or prove behavior.')
 resources=[];rp=load(P/'resource-disposition-plan.json');counts=Counter()
 for i,r in enumerate(parser.resources,1):
  counts[r['kind']]+=1;plan=next((p for p in rp if p['kind']==r['kind'] and p['ordinal']==counts[r['kind']]),None)
  assert r['kind']=='image' or plan
  resources.append(dict(id=f'VIDA-RESOURCE-{i:03}',source_sha256=source['sha256'],**r,body_claim_contexts=[] if plan is None else [c['id'] for c in claims if c['block'] in plan['blocks']],disposition='image-uninspected' if plan is None else plan['disposition'],is_behavioral_proof=False))
 owners=load(P/'owner-context.json')['owners']
 assert len(owners)==9 and len({r['canonical_route'] for r in owners})==9
 for r in owners:
  pin(P/r['snapshot'],r)
  if r['origin_role'].startswith('exact original R1'):assert (ROOT/r['origin_read_path']).read_bytes()==(P/r['snapshot']).read_bytes()
 assert {q for p in load(P/'claim-plan.json') for q in p['related_owner_context']}<={r['canonical_route'] for r in owners}
 scan=load(P/'downstream-scan.json')
 for r in scan['files']:
  q=P/r['snapshot'];pin(q,r);assert [dict(line=i,text=l) for i,l in enumerate(q.read_text().splitlines(),1) if re.search(scan['pattern'],l)]==r['matches']
 catalogs=[]
 for name,rows,key in [('requirements',requirements,'contract'),('cases',cases,'setup_and_action')]:
  for i,r in enumerate(rows):
   linked=[c['id'] for c in claims if r['id'] in [x['id'] for x in c['existing_requirements' if name=='requirements' else 'existing_cases']]]
   catalogs.append(dict(kind=name,id=r['id'],catalog=str((OLD/(name+'.json')).relative_to(ROOT)),json_pointer='/'+str(i),text_json_pointer='/'+str(i)+'/'+key,text=r[key],source_claim_ids=linked,disposition='explicit source-facet subset mappings only' if linked else 'source-silent operational/unknown context retained; not paragraph coverage',**({k:r[k] for k in ['documentary_expected','documentary_comparator','expected','comparison','target_grade','executed']} if name=='cases' else dict(strength=r['strength'],target_applicability=r['target_applicability']))))
 summary=dict(scope='all39 retained body blocks/source-specific facets only; no complete chapter/product/behavior claim',source_blocks=39,source_headings=sum(b['tag'].startswith('h') for b in blocks),paragraphs=sum(b['tag']=='p' for b in blocks),list_items=sum(b['tag']=='li' for b in blocks),claim_context_records=len(claims),dispositions=dict(Counter(c['disposition'] for c in claims)),original_requirements=18,original_cases=28,mapped_requirement_IDs=len({r['id'] for c in claims for r in c['existing_requirements']}),mapped_case_IDs=len({r['id'] for c in claims for r in c['existing_cases']}),resources=dict(counts),actual_heading_TOC_matches=sum(bool(r['original_TOC_matches']) for r in routes),unmatched_actual_headings=sum(not r['original_TOC_matches'] for r in routes),R4_unmatched_records_retained=len(r4),proposed_delta_groups=len(gaps),proposed_future_actions=sum(len(g['proposed_case_deltas']) for g in gaps.values()),all_target_U=True,new_normative_requirements=0,behavioral_coverage_credit=0,completed_topics=0,selfchecks=selfchecks(blocks,claims))
 return {'claims.json':claims,'block-reconciliation.json':reconciliation,'source-routes.json':routes,'unmatched-anchor-context.json':context,'resources.json':resources,'existing-catalog-dispositions.json':catalogs,'summary.json':summary}
def main():
 assert sys.argv[1:] in ([],['--check'],['--preflight'])
 check=sys.argv[1:]==['--check'];pre=sys.argv[1:]==['--preflight'];manifest=P/'manifest.json'
 if not check:assert not manifest.exists(),'Sealed audit; refuse overwrite, create successor instead'
 before={str(q.relative_to(P)):info(q) for q in P.rglob('*') if q.is_file()}
 external={str(ROOT/p['path']):info(ROOT/p['path']) for p in load(P/'input-pins.json')}
 outputs=derive()
 if check or pre:
  for n,v in outputs.items():assert load(P/n)==v,n
  if check:
   m=load(manifest);assert set(m['files'])==set(before)-{'manifest.json'}
   for n,r in m['files'].items():pin(P/n,r)
  for n in before:
   if n.startswith('downstream-snapshots/'):continue
   text=(P/n).read_text();assert text.endswith('\n') and all(l==l.rstrip() for l in text.splitlines()),n
  for link in re.findall(r'\]\(([^)]+)\)',(P/'README.md').read_text()):assert (P/link.split('#')[0]).resolve().exists(),link
  assert before=={str(q.relative_to(P)):info(q) for q in P.rglob('*') if q.is_file()}
  assert external=={str(ROOT/p['path']):info(ROOT/p['path']) for p in load(P/'input-pins.json')}
  print(json.dumps(dict(status='passed-read-only-preflight' if pre else 'passed-read-only-frozen',input_pins=len(external),summary=outputs['summary.json']),indent=2))
 else:
  for n,v in outputs.items():
   assert not (P/n).exists(),'Refuse existing derived output overwrite'
   (P/n).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
if __name__=='__main__':main()
