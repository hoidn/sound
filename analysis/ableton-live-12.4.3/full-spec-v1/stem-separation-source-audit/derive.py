"""Finite 32-block source/claim reconciliation; --check never writes."""
from pathlib import Path
from html.parser import HTMLParser
from collections import Counter
import hashlib
import json
import re
import sys

P=Path(__file__).resolve().parent
ROOT=P.parents[3]
OLD=P.parent/'stem-separation'
SENTENCE_RE=r'(?<=[.!?])\s+(?=[A-Z])'
ALLOWED={'represented-supported-source-clause-and-case-subset','documented-but-outcome-U','missing-requirement-case-or-context','research-only-private-model-or-marketing','editorial'}

def load(p):return json.loads(p.read_text())
def info(p):
 d=p.read_bytes();return dict(bytes=len(d),sha256=hashlib.sha256(d).hexdigest())
def pin(p,r):assert info(p)=={k:r[k] for k in ('bytes','sha256')},p

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
            if r['text']:r['id']=f'STEM-B{len(self.rows)+1:03d}';self.rows.append(r)
            self.active=None
        if self.resource is not None and self.resource['tag']==tag:
            r=self.resource;r['text']=' '.join(r['text'].split());self.resources.append(r);self.resource=None
        if tag=='div' and self.depth:self.depth-=1

def spans(text):
    rows=[];cursor=0
    for part in re.split(SENTENCE_RE,text):
        start=text.index(part,cursor);rows.append((start,start+len(part),part));cursor=start+len(part)
    return rows

def check_reconciliation(blocks,claims):
    assert len(blocks)==32 and {c['block'] for c in claims}=={b['id'] for b in blocks}
    for b in blocks:
        relevant=[c for c in claims if c['block']==b['id']]
        covered=set()
        for c in relevant:
            start,end=c['text_span'];assert 0<=start<end<=len(b['text'])
            assert b['text'][start:end]==c['source_excerpt']
            covered.update(range(start,end))
        assert {i for i,x in enumerate(b['text']) if not x.isspace()}<=covered,b['id']
    assert len({c['id'] for c in claims})==len(claims)

def selfchecks(blocks,claims):
    check_reconciliation(blocks,claims)
    rejected=0
    def reject(bs,cs):
        nonlocal rejected
        try:check_reconciliation(bs,cs)
        except AssertionError:rejected+=1;return
        raise AssertionError('Malformed ledger accepted')
    reject(blocks,[c for c in claims if c['block']!='STEM-B029'])
    changed=json.loads(json.dumps(claims));changed[0]['source_excerpt']+=' invented';reject(blocks,changed)
    changed=json.loads(json.dumps(claims));changed[0]['text_span']=[0,len(blocks[0]['text'])+1];reject(blocks,changed)
    reject(blocks,claims+[claims[0]])
    assert rejected==4
    fixture=Chapter('<p>outside</p><div id="chapter_content"><h1 id="x" data-number="22">22. Test</h1><p>A <b>bold</b> body.</p><img data-src="not-fetched.png"><figcaption>Caption.</figcaption><a href="#x">Link</a></div><p>outside2</p>');fixture.feed(fixture.text)
    assert [r['text'] for r in fixture.rows]==['22. Test','A bold body.']
    assert Counter(r['kind'] for r in fixture.resources)=={'image':1,'caption':1,'link':1}
    assert spans('They have a 44.1 kHz rate. Another sentence.')[0][2]=='They have a 44.1 kHz rate.'
    return dict(parser_body_only_inline_text_and_resource_separation=True,decimal_number_not_sentence_boundary=True,dropped_paragraph_rejected=True,altered_quote_rejected=True,out_of_bounds_span_rejected=True,duplicate_claim_ID_rejected=True)

def derive():
    oldmanifest=load(OLD/'manifest-author-r1.json')
    assert info(OLD/'manifest-author-r1.json')['sha256']=='e7d75c3e9d692b3bf15187bb2284510c1c0e9b0362145cbe67bd91ec90d0d9d2'
    assert len(oldmanifest['files'])==13
    for n,r in oldmanifest['files'].items():pin(OLD/n,r)
    for r in load(P/'input-pins.json'):pin(ROOT/r['path'],r)
    source=load(OLD/'source.json');raw=(OLD/source['file']).read_text();parser=Chapter(raw);parser.feed(raw)
    blocks=load(OLD/'source-blocks.json');assert len(parser.rows)==32
    for r,b in zip(parser.rows,blocks):assert {k:r[k] for k in b}==b
    for snap,path in [('spec-r1.md','wiki/specs/stem-separation.md'),('research-r1.md','wiki/research/stem-separation.md')]:assert (OLD/snap).read_bytes()==(ROOT/path).read_bytes()
    requirements=load(OLD/'requirements.json');cases=load(OLD/'cases.json')
    reqmap={r['id']:(i,r) for i,r in enumerate(requirements)};casemap={r['id']:(i,r) for i,r in enumerate(cases)}
    assert len(reqmap)==18 and len(casemap)==29
    assert all(r['target_applicability']=='U' for r in requirements)
    for c in cases:
        assert c['expected'] is c['comparison'] is None and c['target_grade']=='U' and c['executed'] is False
        if c['kind'] in {'signal','timing','file'} or c['id'].startswith('STEM-U-'):assert c['documentary_expected'] is c['documentary_comparator'] is None
    gaps={g['id']:g for g in load(P/'proposed-deltas.json')};assert len(gaps)==13
    for g in gaps.values():
        assert g['proposal_status']=='audit-proposal-only-not-current-normative-requirement' and g['behavioral_coverage_credit']==0
        for c in g['proposed_case_deltas']:
            assert all(c[k] is None for k in ('expected','comparison','documentary_expected','documentary_comparator')) and c['target_grade']=='U' and c['executed'] is False
    claims=[]
    for i,plan in enumerate(load(P/'claim-plan.json'),1):
        b=next(b for b in blocks if b['id']==plan['block']);start,end,quote=((0,len(b['text']),b['text']) if b['tag'].startswith('h') else spans(b['text'])[plan['sentence']])
        assert plan['disposition'] in ALLOWED and plan['assessment']
        mapping=[];actions=[]
        for suffix in plan['requirement_suffixes']:
            rid='REQ-STEM-SEPARATION-'+(f'{suffix:03d}' if isinstance(suffix,int) else suffix);j,r=reqmap[rid]
            mapping.append(dict(id=rid,catalog=str((OLD/'requirements.json').relative_to(ROOT)),json_pointer='/'+str(j),contract_json_pointer='/'+str(j)+'/contract',existing_contract=r['contract'],strength=r['strength'],evidence_role=('supports explicitly assessed documentary subset' if plan['existing_clause_sufficient_for_stated_subset'] and not rid.startswith('REQ-STEM-SEPARATION-U-') else 'related owner/unknown/context only; not source-claim coverage'),direct_source_block_citation_present=any(e['block']==b['id'] for e in r['evidence']),is_runtime_proof=False))
        for cid in plan['case_ids']:
            j,c=casemap[cid]
            actions.append(dict(id=cid,catalog=str((OLD/'cases.json').relative_to(ROOT)),json_pointer='/'+str(j),action_json_pointer='/'+str(j)+'/setup_and_action',action=c['setup_and_action'],requirement_ids=c['requirements'],documentary_expected=c['documentary_expected'],documentary_comparator=c['documentary_comparator'],expected=c['expected'],comparison=c['comparison'],target_grade=c['target_grade'],executed=c['executed'],relationship=('explicit action for stated subset only; see assessment; no whole-clause closure' if plan['existing_case_action_explicit_for_stated_subset'] else 'related or partial context only; action does not enumerate this exact predicate; see assessment')))
        assert set(plan['gaps'])<=set(gaps)
        claims.append(dict(id=f'STEMA-C{i:03d}',**plan,text_span=[start,end],source_excerpt=quote,source_locator=dict(source_id=source['id'],source_sha256=source['sha256'],source_url=source['url'],source_version=source['version'],source_capture_utc=source['capture_utc'],source_record_catalog=str((OLD/'source.json').relative_to(ROOT)),source_record_json_pointer='',block_catalog=str((OLD/'source-blocks.json').relative_to(ROOT)),block_json_pointer='/'+str(blocks.index(b)),block_text_json_pointer='/'+str(blocks.index(b))+'/text',html_line=b['html_line'],html_column=parser.rows[blocks.index(b)]['html_column'],heading_context_anchor=b['anchor'],anchor_role='retained parser heading context, not an ID on the paragraph',exact_heading_url=source['url']+'#'+b['anchor']),existing_requirements=mapping,existing_cases=actions,claim_role='editorial heading' if b['tag'].startswith('h') else 'analyst-separated source claim/context',target_applicability='U',semantic_coverage='partial-or-unknown; explicit disposition only',behavioral_coverage_credit=0,complete=False))
    check_reconciliation(blocks,claims)
    reconcile=[]
    for b,rawb in zip(blocks,parser.rows):
        selected=[c for c in claims if c['block']==b['id']]
        reconcile.append(dict(block=b['id'],source_text=b['text'],source_tag=b['tag'],source_anchor=b['anchor'],raw_locator=rawb,claim_ids=[c['id'] for c in selected],all_normalized_nonwhitespace_text_assigned=True,claim_dispositions=dict(Counter(c['disposition'] for c in selected)),meaning='Text assignment reconciliation only; not proof of complete semantic extraction, operation coverage, target behavior or chapter closure'))
    toc=load(P.parent/'inventory/manual-toc.json');routes=[]
    headings=[r for r in parser.rows if r['tag'].startswith('h')]
    for h in headings:
        attrs=dict(h['attrs']);url=source['url']+'#'+h['anchor'];matched=[(i,r) for i,r in enumerate(toc) if r['url']==url]
        assert len(matched)==1
        j,row=matched[0]
        routes.append(dict(anchor=h['anchor'],heading_id=h['id'],heading_tag=h['tag'],source_number=attrs['data-number'],source_heading_text=h['text'],exact_url=url,TOC_identity=row['id'],TOC_json_pointer='/'+str(j),original_TOC_leaf=row['leaf'],source_block_ids=[b['id'] for b in blocks if b['anchor']==h['anchor']],route_role='actual retained heading/subsection context only; not leaf semantic coverage',target_applicability='U',complete=False))
    resources=[]
    resource_plan=load(P/'resource-disposition-plan.json');ordinals=Counter()
    for i,r in enumerate(parser.resources,1):
        ordinals[r['kind']]+=1
        related=next((x for x in resource_plan if x['resource_kind']==r['kind'] and x['ordinal']==ordinals[r['kind']]),None)
        resources.append(dict(id=f'STEMA-RESOURCE-{i:03d}',source_sha256=source['sha256'],**r,body_claim_contexts=[] if related is None else [c['id'] for c in claims if c['block'] in related['body_blocks']],disposition='image-uninspected' if related is None else related['disposition']))
    assert len(resource_plan)==14 and all(r['body_claim_contexts'] for r in resources if r['kind']!='image')
    assert Counter(r['kind'] for r in resources)=={'image':8,'caption':8,'link':6}
    scan=load(P/'downstream-scan.json')
    for record in scan['files']:
        snapshot=P/record['snapshot'];pin(snapshot,record)
        text=snapshot.read_text();found=[dict(line=i,text=line) for i,line in enumerate(text.splitlines(),1) if re.search(scan['pattern'],line)]
        assert found==record['matches'] and found
    summary=dict(scope='full retained32-block paragraph/source-claim reconciliation; beginning source audit, no chapter/app completion',source_blocks=32,source_headings=4,substantive_paragraphs=28,source_list_items=0,claim_context_records=len(claims),dispositions=dict(Counter(c['disposition'] for c in claims)),resources=dict(Counter(r['kind'] for r in resources)),original_requirements=18,original_cases=29,proposed_delta_groups=len(gaps),proposed_future_case_actions=sum(len(g['proposed_case_deltas']) for g in gaps.values()),all_target_U=True,new_normative_requirements=0,behavioral_coverage_credit=0,completed_topics=0,source_read_scope='All32retained blocks and every paragraph sentence manually read; source-specific facets including conditional and exception contexts assessed against all18clauses/29actions. HTML resource attributes/captions read; image pixels and linked destination content not inspected. Whole source sentences may support several explicit facets; no automatic claim that sentence assignment proves semantic completeness.',selfchecks=selfchecks(blocks,claims))
    return {'claims.json':claims,'block-reconciliation.json':reconcile,'source-routes.json':routes,'resources.json':resources,'summary.json':summary}

def main():
    assert sys.argv[1:] in ([],['--check'],['--preflight'])
    check=sys.argv[1:]==['--check'];preflight=sys.argv[1:]==['--preflight'];manifest=P/'manifest.json'
    if not check:assert not manifest.exists(),'Frozen audit; successor revision required'
    before={str(p.relative_to(P)):info(p) for p in P.rglob('*') if p.is_file()}
    outputs=derive()
    if check or preflight:
        for name,value in outputs.items():assert load(P/name)==value,name
        if check:
            m=load(manifest)
            assert set(m['files'])==set(before)-{'manifest.json'}
            for name,r in m['files'].items():pin(P/name,r)
        for name in before:
            path=P/name
            if name.startswith('downstream-snapshots/'):continue
            text=path.read_text();assert text.endswith('\n') and all(line==line.rstrip() for line in text.splitlines()),path
        readme=(P/'README.md').read_text()
        for link in re.findall(r'\]\(([^)]+)\)',readme):assert (P/link.split('#')[0]).resolve().exists(),link
        assert before=={str(p.relative_to(P)):info(p) for p in P.rglob('*') if p.is_file()}
        print(json.dumps(dict(status='passed-read-only-preflight' if preflight else 'passed-read-only-frozen',input_pins=len(load(P/'input-pins.json')),summary=outputs['summary.json']),indent=2))
    else:
        for name,value in outputs.items():(P/name).write_text(json.dumps(value,indent=2)+'\n')

if __name__=='__main__':main()
