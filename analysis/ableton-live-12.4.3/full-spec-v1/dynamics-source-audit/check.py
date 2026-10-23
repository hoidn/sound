"""Finite read-only five-section source audit. Only the pinned pure HTML parser runs."""
from collections import Counter
from copy import deepcopy
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import re
import sys

P=Path(__file__).resolve().parent
R=P.parents[3]
F=P.parent
D=F/'dynamics'
NAMES=['compressor','gate','glue-compressor','limiter','multiband-dynamics']


def load(p):
    return json.loads(p.read_text())


def dg(p):
    b=p.read_bytes()
    return dict(bytes=len(b),sha256=sha256(b).hexdigest())


def pointer(v,s):
    for k in s.strip('/').split('/') if s else []:
        k=k.replace('~1','/').replace('~0','~')
        v=v[int(k)] if isinstance(v,list) else v[k]
    return v


def parser():
    path=F/'midi-editing-source-audit/source_parser.py'
    assert dg(path)['sha256']=='648bb1ebce827d136ab6074d6b80fe32475534d87d57a367e9de9aa9fc8fdad8'
    spec=importlib.util.spec_from_file_location('dynamics_audit_pure_parser',path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.extract


def derive(plan,inputs):
    source=load(D/'sources.json')[0]
    raw=Path(source['path']).read_text()
    full,resources=parser()(raw,'FX')
    blocks=[b for b in full if any(h['level']==2 and h['anchor'] in NAMES for h in b['heading_context'])]
    anchors={h['anchor'] for b in blocks for h in b['heading_context'] if h['level']>=2}
    resources=[r for r in resources if r['heading_context_anchor'] in anchors]
    req=load(D/'requirements.json');cases=load(D/'cases.json')
    assessments=[];local_counts=Counter();routes=[]
    null=dict(documentary_expected=None,documentary_comparison=None,actual_expected=None,actual_comparison=None,target='U',executed=False,complete=False,coverage_credit=0)
    for i,b in enumerate(blocks):
        name=next(h['anchor'] for h in b['heading_context'] if h['level']==2)
        local_counts[name]+=1;local=f'{name}:B{local_counts[name]:03}'
        row=plan['judgments'][i]
        assert row['profile']==name and row['local_block']==local
        rs=[];cs=[]
        for n in row['requirement_suffixes']:
            ident=f'REQ-DYN-{name.upper()}-{n:03}'
            j=next(j for j,r in enumerate(req) if r['id']==ident)
            rs.append(dict(id=ident,pointer=f'/owner_requirements/{j}',predicate_pointer=f'/owner_requirements/{j}/text',role='Only the represented subset explicitly assessed here, not whole-block closure.'))
            cid=f'DYN-{name.upper()}-{n:03}'
            j=next(j for j,c in enumerate(cases) if c['id']==cid)
            cs.append(dict(id=cid,pointer=f'/owner_cases/{j}',setup_pointer=f'/owner_cases/{j}/setup',action_pointer=f'/owner_cases/{j}/input',role='Exact actual proposed action read; inspection is not productive audio execution.'))
        disposition=('editorial-or-structural' if b['kind'].startswith('h') else 'represented-subset-with-action-or-prerequisite-gap' if rs and row['proposal_numbers'] else 'represented-subset-or-qualified-documentary-context' if rs else 'research-guidance-or-historical-context')
        assessments.append(dict(id=f'DYSA-A{i+1:03}',block=b['id'],local_block=local,source_pointer=f'/blocks/{i}/text',quote=b['text'],quote_sha256=sha256(b['text'].encode()).hexdigest(),assessment=row['assessment'],disposition=disposition,represented_requirement_refs=rs,represented_case_refs=cs,open_proposal_groups=[f'DYSA-G{n:02}' for n in row['proposal_numbers']],**null))
        routes.append(dict(local_block=local,source_block=b['id'],pointer=f'/blocks/{i}'))
    proposals=deepcopy(plan['proposals'])
    for g in proposals:
        g['assessment_ids']=[a['id'] for a in assessments if g['id'] in a['open_proposal_groups']]
        g['source_blocks']=[a['block'] for a in assessments if g['id'] in a['open_proposal_groups']]
    questions=deepcopy(plan['source_questions'])
    for q in questions:
        q['quotes']=[dict(local_block=a['local_block'],pointer=a['source_pointer'],quote=a['quote']) for a in assessments if a['local_block'] in q['local_blocks']]
        q.update(null)
    scopes=[dict(id=c['id'],pointer=f'/owner_cases/{i}',action_pointer=f'/owner_cases/{i}/input',provenance=c['provenance'],legacy_expected_role='historical retained-file-only documentary assertion, not rerun' if c['provenance']=='Dpkg' else 'historical documentary proposal, not actual result' if c['provenance']=='D12' else 'unknown expected outcome remains null',actual_expected=None,actual_comparison=None,target='U',executed=False) for i,c in enumerate(cases)]
    return dict(role='Analyst source audit ONLY; no normative adoption, newcase or compatibility credit.',source=source,source_capture_utc=None,source_scope='Full selected five h2 sections only. Whole1137chapter blocks parsed for filtering, not fullchapter semantic read. Manual WHOLE-CONTEXT judgments, not atomic-facet completion.',blocks=blocks,resources=[dict(r,pixels_or_destination_inspected=False,role='Literal URL/emptyalt/caption/link text read; responsive attributes retained/hashchecked, no pixels or followed destinations.') for r in resources],block_routes=routes,owner_requirements=req,owner_cases=cases,owner_fixtures=load(D/'fixture-signals.json'),owner_contract_scope='Exact original R1 immutable spec/research providers in inputs.json; source links do not discharge untraced audio or lifecycle behavior.',case_scope=scopes,assessments=assessments,proposals=proposals,source_questions=questions,common_future_prerequisites=plan['common_future_prerequisites'],summary=dict(selected_blocks=len(blocks),selected_by_profile=dict(local_counts),block_kinds=dict(Counter(b['kind'] for b in blocks)),whole_context_judgments=len(assessments),atomic_facets_claimed=False,resources=len(resources),resource_kinds=dict(Counter(r['kind'] for r in resources)),owner_requirements=62,owner_cases=129,D12_cases=47,Dpkg_file_only_cases=5,U_cases=77,proposals=20,source_questions=4,immutable_pins=len(inputs['files']),asof_providers=2,new_normative_IDs=0,new_cases=0,new_documentary_nonnull=0,actual_nonnull=0,executed=0,coverage_credit=0,complete_topics=0))


def guards(a):
    assert len(a['blocks'])==len(a['assessments'])==123 and len(a['proposals'])==20
    for i,x in enumerate(a['assessments']):
        b=a['blocks'][i]
        assert x['id']==f'DYSA-A{i+1:03}' and x['block']==b['id'] and x['quote']==pointer(a,x['source_pointer'])==b['text']
        assert sha256(x['quote'].encode()).hexdigest()==x['quote_sha256']
        for k in ('represented_requirement_refs','represented_case_refs'):
            for ref in x[k]:assert pointer(a,ref['pointer'])['id']==ref['id']
    for x in a['assessments']+a['proposals']+a['source_questions']:
        assert all(x[k] is None for k in ('documentary_expected','documentary_comparison','actual_expected','actual_comparison'))
        assert x['target']=='U' and x['executed'] is x['complete'] is False and x['coverage_credit']==0
    for i,g in enumerate(a['proposals'],1):
        assert g['id']==f'DYSA-G{i:02}' and g['new_normative_IDs']==[]
        assert g['assessment_ids']==[r['id'] for r in a['assessments'] if g['id'] in r['open_proposal_groups']] and g['assessment_ids']
        assert g['source_blocks']==[r['block'] for r in a['assessments'] if g['id'] in r['open_proposal_groups']]
    bylocal={r['local_block']:r for r in a['assessments']}
    ids=lambda local:[r['id'] for r in bylocal[local]['represented_case_refs']]
    assert 'DYN-COMPRESSOR-007' in ids('compressor:B016') and not bylocal['compressor:B016']['open_proposal_groups']
    assert 'DYN-GATE-005' in ids('gate:B007') and not bylocal['gate:B007']['open_proposal_groups']
    assert 'DYN-LIMITER-004' in ids('limiter:B010') and not bylocal['limiter:B010']['open_proposal_groups']
    assert 'DYN-MULTIBAND-DYNAMICS-004' in ids('multiband-dynamics:B017')
    assert 'DYN-MULTIBAND-DYNAMICS-005' in ids('multiband-dynamics:B018')
    assert 'DYN-LIMITER-002' in ids('limiter:B007') and 'genuinely toggles Maximize' in bylocal['limiter:B007']['assessment']
    g=a['proposals'];c=a['common_future_prerequisites']
    assert 'ratio1' in g[0]['proposed_minimal_delta'] and 'No overall-path identity' in g[0]['proposed_minimal_delta']
    assert 'normal AND external-detector' in g[3]['proposed_future_positive_baseline'] and 'Listen REPLACES normal output' in g[3]['proposed_minimal_delta']
    assert 'Main wet and detector wet distinct' in g[3]['limits'] and 'No Multiband EQ control or Limiter external sidechain' in g[3]['limits']
    assert 'Makeup available/unavailable' in g[3]['proposed_minimal_delta']
    assert 'BEFORE Range0' in g[7]['proposed_minimal_delta'] and 'Range0 removes compression, not Makeup/SoftClip' in g[7]['proposed_minimal_delta']
    assert 'MAY exceed0dB' in g[9]['limits'] and 'no mandatory overshoot' in g[9]['limits']
    assert 'two-times' in g[9]['limits'] or 'Two-times' in g[9]['limits']
    assert 'SAME manual control' in g[11]['proposed_minimal_delta'] and 'productive limiting/recovery' in g[11]['proposed_future_positive_baseline']
    assert 'EACH relevant L/R or M/S member' in g[12]['proposed_future_positive_baseline'] and 'no50law' in g[12]['limits']
    assert 'Below edge and interior' in g[15]['proposed_minimal_delta'] and 'DOUBLECLICK as true' in g[15]['proposed_minimal_delta']
    assert 'BelowattackDOWN/releaseUP' in g[16]['limits']
    assert 'gains/crossover processing' in g[17]['limits'] and 'PLUS separate genuinely productive gain and crossover' in g[17]['proposed_future_positive_baseline']
    assert 'CAN SOMETIMES' in g[19]['limits'] and 'MAY destroy' in g[19]['limits']
    assert 'EACH rate' in c['rates'] and 'NOT calibrated detector dB' in c['no_numeric_oracle']
    assert 'historicalCreator12.4d1' in c['file_only']
    assert a['summary']['new_cases']==a['summary']['new_normative_IDs']==a['summary']['coverage_credit']==a['summary']['complete_topics']==0


def main():
    assert sys.dont_write_bytecode and sys.argv[1:]==['--check'],'Read-only --check only; writing/old-main/runtime refused'
    inputs=load(P/'inputs.json');plan=load(P/'plan.json');a=load(P/'audit.json')
    watch={R/x['path'] for x in inputs['files']}|{p for p in P.iterdir() if p.is_file()}
    before={str(p):dg(p) for p in watch}
    assert len(inputs['files'])==32 and len({x['path'] for x in inputs['files']})==32
    assert all(not x['path'].startswith('wiki/') for x in inputs['files'])
    for x in inputs['files']:assert dg(R/x['path'])=={k:x[k] for k in ('bytes','sha256')},x['path']
    old=load(D/'manifest-author-r1.json')
    assert dg(D/'manifest-author-r1.json')['sha256']=='7eaf6c5b97efad1352aaf2820c21a66ebb5c6d53bbf9e7f218df516418a825eb'
    for x in old['payloads']:assert dg(D/x['path'])=={k:x[k] for k in ('bytes','sha256')}
    assert len(old['payloads'])==26
    for s in inputs['canonical_snapshots']:
        assert dg(R/s['provider'])==dict(bytes=len(s['text'].encode()),sha256=sha256(s['text'].encode()).hexdigest())=={k:s[k] for k in ('bytes','sha256')}
    assert a==derive(plan,inputs)
    assert a['source_capture_utc'] is None
    assert a['source']['url']=='https://www.ableton.com/en/live-manual/12/live-audio-effect-reference/'
    assert dg(Path(a['source']['path']))==dict(bytes=588328,sha256='9cb15cb3d80bda4771e5add2c2b74f5c57d73ee8850e198acf7cf8a51dfd1299')
    raw=Path(a['source']['path']).read_text()
    for b in a['blocks']:
        assert raw[b['raw_start']:b['raw_end']]==b['raw_html']
        assert raw.count('\n',0,b['raw_start'])+1==b['html_line']
        assert b['raw_start']-raw.rfind('\n',0,b['raw_start'])-1==b['html_column']
    for r in a['resources']:assert sha256(raw[r['raw_start']:raw.index('>',r['raw_start'])+1].encode()).hexdigest()==r['starttag_sha256'] and r['pixels_or_destination_inspected'] is False
    for name in NAMES:
        oldblocks=load(D/f'manual-{name}-blocks.json')
        selected=[b for b in a['blocks'] if any(h['level']==2 and h['anchor']==name for h in b['heading_context'])]
        assert [x['text'] for x in oldblocks]==[x['text'] for x in selected]
    assert a['owner_requirements']==load(D/'requirements.json') and a['owner_cases']==load(D/'cases.json')
    assert len(a['owner_requirements'])==len({r['id'] for r in a['owner_requirements']})==62
    assert len(a['owner_cases'])==len({c['id'] for c in a['owner_cases']})==129
    assert Counter(c['provenance'] for c in a['owner_cases'])==dict(D12=47,Dpkg=5,U=77)
    spec=inputs['canonical_snapshots'][0]['text']
    for r in a['owner_requirements']:assert r['text'] in spec and spec.count('### '+r['id']+' — ')==1
    for i,c in enumerate(a['owner_cases']):
        if c['provenance']=='U':assert c['expected'] is None
        assert c['execution']=='unexecuted; no Live or candidate result'
        s=a['case_scope'][i];assert pointer(a,s['pointer'])==c and pointer(a,s['action_pointer'])==c['input']
        assert s['actual_expected'] is s['actual_comparison'] is None and s['target']=='U' and s['executed'] is False
    guards(a);reject=[]
    for name in ['omit-context','wrong-pointer','invent-oracle','erase-lookahead-choice','erase-true-Above-drag','erase-true-Maximize-toggle','detector-without-main','Listen-mixed','mainwet-detectorwet','Multiband-EQ-invented','Range0-full-identity','unconditional-SoftClip-bound','unproductive-Release','only-one-Link-member','Below-crossing-reversed','Amount0-gains-erased','guaranteed-uncompression','uncalibrated-rate-choice','preset-runtime-promotion']:
        t=deepcopy(a)
        if name=='omit-context':t['assessments'].pop()
        elif name=='wrong-pointer':t['assessments'][1]['source_pointer']='/blocks/2/text'
        elif name=='invent-oracle':t['proposals'][0]['actual_expected']='pass'
        elif name=='erase-lookahead-choice':t['assessments'][15]['represented_case_refs']=[]
        elif name=='erase-true-Above-drag':next(r for r in t['assessments'] if r['local_block']=='multiband-dynamics:B017')['represented_case_refs']=[]
        elif name=='erase-true-Maximize-toggle':next(r for r in t['assessments'] if r['local_block']=='limiter:B007')['represented_case_refs']=[]
        elif name=='detector-without-main':t['proposals'][3]['proposed_future_positive_baseline']='External signal enabled only'
        elif name=='Listen-mixed':t['proposals'][3]['proposed_minimal_delta']='Listen mixes with normal output'
        elif name=='mainwet-detectorwet':t['proposals'][3]['limits']='One wet control'
        elif name=='Multiband-EQ-invented':t['proposals'][3]['limits']=t['proposals'][3]['limits'].replace('No Multiband EQ control or Limiter external sidechain','Both have allcontrols')
        elif name=='Range0-full-identity':t['proposals'][7]['proposed_minimal_delta']='Range0 bypasses everything'
        elif name=='unconditional-SoftClip-bound':t['proposals'][9]['limits']='Always below-0.5dB'
        elif name=='unproductive-Release':t['proposals'][11]['proposed_future_positive_baseline']='Auto flag present'
        elif name=='only-one-Link-member':t['proposals'][12]['proposed_future_positive_baseline']='Left present only'
        elif name=='Below-crossing-reversed':t['proposals'][16]['limits']='BelowattackUP/releaseDOWN'
        elif name=='Amount0-gains-erased':t['proposals'][17]['limits']='Amount0 bypasses everything'
        elif name=='guaranteed-uncompression':t['proposals'][19]['limits']='Always restores transients'
        elif name=='uncalibrated-rate-choice':t['common_future_prerequisites']['rates']='Always reinterpret sameframes'
        else:t['common_future_prerequisites']['file_only']='Stored field proves runtime'
        try:guards(t)
        except AssertionError:reject.append(name)
        else:raise AssertionError('Unsafe mutation accepted '+name)
    blocks,res=parser()('<p>Outside</p><div id="chapter_content"><h1 id="r">Root</h1><div><h2 id="compressor">Comp</h2><p>Set 1.5 ms. Not a measured delay.</p><ul><li>Qualified only.</li></ul><figcaption>Caption.</figcaption><img alt="" src="unopened"></div></div><p>After</p>','TEST')
    assert [b['kind'] for b in blocks]==['h1','h2','p','li'] and blocks[2]['text']=='Set 1.5 ms. Not a measured delay.' and [r['kind'] for r in res]==['caption','image']
    assert '18 images, 14 captions and six links' in (P/'README.md').read_text()
    links=0
    for url in re.findall(r'\]\(([^)]+)\)',(P/'README.md').read_text()):assert (P/url.split('#')[0]).exists();links+=1
    for p in P.iterdir():
        if p.is_file():
            b=p.read_bytes();assert b.endswith(b'\n') and b'\0' not in b and all(x.rstrip(b' \t')==x for x in b.splitlines())
    if (P/'manifest.json').exists():
        m=load(P/'manifest.json');assert set(m['files'])=={p.name for p in P.iterdir() if p.is_file()}-{'manifest.json'}
        for name,v in m['files'].items():assert dg(P/name)==v
    assert before=={str(p):dg(p) for p in watch}
    print(json.dumps(dict(status='pass',sealed=(P/'manifest.json').exists(),summary=a['summary'],negative_fixtures=reject,parser_fixture=True,links=links,watched_paths=len(watch),all_unchanged=True,writes=False,old_main_decodes_or_runtime=False),indent=2))


if __name__=='__main__':
    main()
