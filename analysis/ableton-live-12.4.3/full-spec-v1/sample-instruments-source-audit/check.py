"""Read-only finite retained-source audit. No old main/sample/patch/vendor execution."""
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
D=F/'sample-instruments'
NAMES=['impulse','sampler','simpler']


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
    spec=importlib.util.spec_from_file_location('sample_audit_pure_parser',path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.extract


def derive(plan,inputs):
    source=load(D/'sources.json')[0];raw=(D/source['file']).read_text()
    full,resources=parser()(raw,'INST')
    blocks=[b for b in full if any(h['level']==2 and h['anchor'] in NAMES for h in b['heading_context'])]
    anchors={h['anchor'] for b in blocks for h in b['heading_context'] if h['level']>=2}
    resources=[r for r in resources if r['heading_context_anchor'] in anchors]
    req=load(D/'requirements.json');cases=load(D/'cases.json')
    assessments=[];counts=Counter();routes=[]
    null=dict(documentary_expected=None,documentary_comparison=None,actual_expected=None,actual_comparison=None,target='U',executed=False,complete=False,coverage_credit=0)
    for i,b in enumerate(blocks):
        name=next(h['anchor'] for h in b['heading_context'] if h['level']==2)
        counts[name]+=1;local=f'{name}:B{counts[name]:03}'
        row=plan['judgments'][i];assert row['profile']==name and row['local_block']==local
        rs=[];cs=[]
        for n in row['requirement_suffixes']:
            ident=f'REQ-{name.upper()}-{n:03}';j=next(j for j,r in enumerate(req[name]) if r['id']==ident)
            rs.append(dict(id=ident,pointer=f'/owner_requirements/{name}/{j}',predicate_pointer=f'/owner_requirements/{name}/{j}/body',role='Only the represented subset explicitly assessed, not whole-block closure.'))
        for n in row['case_suffixes']:
            ident=f'{name.upper()}-{n:03}';j=next(j for j,c in enumerate(cases) if c['id']==ident)
            cs.append(dict(id=ident,pointer=f'/owner_cases/{j}',setup_pointer=f'/owner_cases/{j}/setup',action_pointer=f'/owner_cases/{j}/action',role='Only the actual action/SETUP subset explicitly scoped in this assessment; not the entire case expected predicate and never runtime or citation-based completion.'))
        disposition=('editorial-or-structural' if b['kind'].startswith('h') else 'represented-subset-with-action-or-prerequisite-gap' if rs and row['proposal_numbers'] else 'represented-subset-or-qualified-source-context' if rs else 'source-only-ui-entry-or-research-guidance' if row['proposal_numbers'] else 'research-guidance-or-historical-context')
        assessments.append(dict(id=f'SISA-A{i+1:03}',block=b['id'],local_block=local,source_pointer=f'/blocks/{i}/text',quote=b['text'],quote_sha256=sha256(b['text'].encode()).hexdigest(),assessment=row['assessment'],disposition=disposition,represented_requirement_refs=rs,represented_case_refs=cs,open_proposal_groups=[f'SISA-G{n:02}' for n in row['proposal_numbers']],**null))
        routes.append(dict(local_block=local,source_block=b['id'],pointer=f'/blocks/{i}'))
    proposals=deepcopy(plan['proposals'])
    for g in proposals:
        g['assessment_ids']=[a['id'] for a in assessments if g['id'] in a['open_proposal_groups']]
        g['source_blocks']=[a['block'] for a in assessments if g['id'] in a['open_proposal_groups']]
    questions=deepcopy(plan['source_questions'])
    for q in questions:
        q['quotes']=[dict(local_block=a['local_block'],pointer=a['source_pointer'],quote=a['quote']) for a in assessments if a['local_block'] in q['local_blocks']];q.update(null)
    scopes=[dict(id=c['id'],pointer=f'/owner_cases/{i}',setup_pointer=f'/owner_cases/{i}/setup',action_pointer=f'/owner_cases/{i}/action',legacy_strength=c['strength'],legacy_expected_role='Original documentary proposal, NOT measured actual result; oldunknown string/comparator preserved.',actual_expected=None,actual_comparison=None,target='U',executed=False) for i,c in enumerate(cases)]
    return dict(role='Source-only partial audit, no normative adoption or compatibility credit.',source=source,source_scope='Full three selectedh2sections309blocks only;1200wholechapterblocks parsed for filtering, no wholechapter semantic audit. Whole-context judgments NOTatomicfacets or completion.',blocks=blocks,resources=[dict(r,pixels_or_destination_inspected=False,role='Literal URLs/emptyalts/captions/link text read; repeatedresponsiveattributes retained/hashchecked, no pixels/destinations.') for r in resources],block_routes=routes,owner_requirements=req,owner_cases=cases,owner_fixtures=load(D/'fixtures.json'),owner_contract_scope='Original immutableR2providers ininputs, independentlyapprovedpartial. Historicalpendingtext preservedasof, not currentreviewstatus. No futurelivecanonical gates.',case_scope=scopes,assessments=assessments,proposals=proposals,source_questions=questions,common_future_prerequisites=plan['common_future_prerequisites'],summary=dict(blocks=len(blocks),selected_by_profile=dict(counts),block_kinds=dict(Counter(b['kind'] for b in blocks)),selected_table_rows=sum(b['kind']=='tr' for b in blocks),selected_table_cells=sum(len(b.get('cells',[])) for b in blocks),whole_context_judgments=len(assessments),atomic_facets_claimed=False,resources=len(resources),resource_kinds=dict(Counter(r['kind'] for r in resources)),owner_requirements=61,owner_cases=88,D_current_manual_requirements=46,U_requirements=15,D_current_manual_cases=72,U_cases=16,proposals=33,source_questions=6,immutable_pins=len(inputs['files']),asof_providers=4,new_normative_IDs=0,new_cases=0,new_documentary_nonnull=0,actual_nonnull=0,executed=0,coverage_credit=0,complete_topics=0))


def guards(a):
    assert len(a['blocks'])==len(a['assessments'])==309 and len(a['proposals'])==33
    for i,x in enumerate(a['assessments']):
        b=a['blocks'][i];assert x['id']==f'SISA-A{i+1:03}' and x['block']==b['id'] and x['quote']==pointer(a,x['source_pointer'])==b['text']
        assert sha256(x['quote'].encode()).hexdigest()==x['quote_sha256']
        for k in ('represented_requirement_refs','represented_case_refs'):
            for ref in x[k]:assert pointer(a,ref['pointer'])['id']==ref['id']
    for x in a['assessments']+a['proposals']+a['source_questions']:
        assert all(x[k] is None for k in ('documentary_expected','documentary_comparison','actual_expected','actual_comparison'))
        assert x['target']=='U' and x['executed'] is x['complete'] is False and x['coverage_credit']==0
    for i,g in enumerate(a['proposals'],1):
        assert g['id']==f'SISA-G{i:02}' and g['new_normative_IDs']==[]
        assert g['assessment_ids']==[r['id'] for r in a['assessments'] if g['id'] in r['open_proposal_groups']] and g['assessment_ids']
        assert g['source_blocks']==[r['block'] for r in a['assessments'] if g['id'] in r['open_proposal_groups']]
    by={r['local_block']:r for r in a['assessments']}
    ids=lambda local:[r['id'] for r in by[local]['represented_case_refs']]
    assert 'SIMPLER-022' in ids('simpler:B063') and not by['simpler:B063']['open_proposal_groups']
    assert 'SAMPLER-025' in ids('sampler:B157') and not by['sampler:B157']['open_proposal_groups']
    assert not by['simpler:B056']['represented_case_refs'], 'Volume-LFO does not prove Filter-LFO'
    assert ids('sampler:B123')==['SAMPLER-022'], 'Fixed support belongs to B130, not no-output paragraph'
    assert 'EMPTY-ALTIMAGE' in by['sampler:B108']['assessment'] and 'exactimage-labelassociationU' in by['sampler:B108']['assessment']
    assert 'SIMPLER-008' in ids('simpler:B018') and 'SIMPLER-009' in ids('simpler:B019')
    assert 'SAMPLER-015' in ids('sampler:B102') and 'SAMPLER-016' in ids('sampler:B110')
    assert 'IMPULSE-006' in ids('impulse:B007') and 'IMPULSE-007' in ids('impulse:B007')
    assert not by['sampler:B099']['represented_case_refs'] and 'UNLOOPED ONLY' in a['proposals'][18]['proposed_future_positive_baseline']
    g=a['proposals'];c=a['common_future_prerequisites']
    assert 'BOTHdistinctnotes/voices/layers/slices/targets' in c['independent_members'] and 'NONEMPTY' in c['productive_source']
    assert 'Samplefilename/enabledflags do not prove playback' in c['productive_source']
    assert 'SimplercopyReverse differsSamplerGLOBALno-copyReverse' in c['loops']
    assert 'BOTHindependently productive distinctvoices/targets' in g[3]['proposed_future_positive_baseline']
    assert 'EACHslice independently productive' in g[5]['proposed_future_positive_baseline']
    assert 'Volumeproof doesNOTproveFilterroute' in g[9]['proposed_future_positive_baseline']
    assert 'nonzeroatNoteOn' in g[10]['proposed_minimal_delta']
    assert 'NOsoundequivalence' in g[12]['proposed_future_positive_baseline']
    assert 'supportedconfiguredsurface' in g[13]['proposed_minimal_delta']
    assert 'NormalizePan needNOTcenter' in g[14]['proposed_future_positive_baseline']
    assert 'keyANDvelocityANDselector' in g[15]['proposed_minimal_delta']
    assert 'EACHeligiblelayer independentlyproductive' in g[16]['proposed_future_positive_baseline'] and 'No boundedtrialguarantee' in g[16]['proposed_future_positive_baseline']
    assert 'Back-and-ForthSustain' in g[18]['proposed_minimal_delta'] and 'EXCEPTIONS controlling' in g[18]['proposed_future_positive_baseline']
    assert 'EndONLYwherefound(LFO/Filter/Pitchsourcequalification)' in g[19]['proposed_minimal_delta']
    assert 'loaded-sample FM andAM' in g[20]['proposed_minimal_delta'] and 'BEFOREremoving sample' in g[20]['proposed_future_positive_baseline']
    assert 'BOTHfilterANDshaper' in g[22]['proposed_future_positive_baseline']
    assert 'BOTHdistinctnotes/voices' in g[23]['proposed_future_positive_baseline']
    assert 'BOTHdistincttargets/notes' in g[24]['proposed_future_positive_baseline']
    assert 'No MIDIbyte/14bitcodec' in g[25]['proposed_future_positive_baseline']
    assert 'externalfilesABSENT' in g[26]['proposed_future_positive_baseline']
    assert 'No sixmiddletriggernotes' in g[27]['proposed_future_positive_baseline']
    assert 'Clip-envelope' in g[28]['proposed_minimal_delta'] or 'clip-envelope' in g[28]['proposed_minimal_delta']
    assert 'BOTHdistinctslotvoices independentlyproductive BEFOREloss' in g[29]['proposed_future_positive_baseline']
    assert 'Triggertrial' in g[31]['proposed_minimal_delta'] and 'no silencefromearlierSampleEnd' in g[31]['proposed_future_positive_baseline']
    assert 'EACHslot/source/destination independentlyproductive NONZEROoutput' in g[32]['proposed_future_positive_baseline']
    assert a['summary']['selected_table_rows']==a['summary']['selected_table_cells']==0
    assert a['summary']['new_cases']==a['summary']['new_normative_IDs']==a['summary']['coverage_credit']==a['summary']['complete_topics']==0


def main():
    assert sys.dont_write_bytecode and sys.argv[1:]==['--check'],'Read-only --check only; no writer/oldmain/sample execution'
    inputs=load(P/'inputs.json');plan=load(P/'plan.json');a=load(P/'audit.json')
    watch={R/x['path'] for x in inputs['files']}|{p for p in P.iterdir() if p.is_file()};before={str(p):dg(p) for p in watch}
    assert len(inputs['files'])==68 and len({x['path'] for x in inputs['files']})==68
    assert all(not x['path'].startswith('wiki/') for x in inputs['files'])
    for x in inputs['files']:assert dg(R/x['path'])=={k:x[k] for k in ('bytes','sha256')},x['path']
    assert dg(D/'manifest-author-r2.json')['sha256']=='391bc843dc9abb2b1ad120db7fe38d0c7060dcc4a396c3e1133a389de0e836f9'
    assert dg(D/'manifest-author-r1.json')['sha256']==dg(D/'revisions/r1/manifest-author-r1.json')['sha256']=='277da7d53e395b45bf9d58ea803636d79002e20101163ec244f20a9ce100cf4b'
    for root,filename,count in [(D,'manifest-author-r2.json',35),(D/'revisions/r1','manifest-author-r1.json',28)]:
        old=load(root/filename);assert len(old['payloads'])==count
        for x in old['payloads']:assert dg(root/x['path'])=={k:x[k] for k in ('bytes','sha256')}
    for s in inputs['canonical_snapshots']:assert dg(R/s['provider'])==dict(bytes=len(s['text'].encode()),sha256=sha256(s['text'].encode()).hexdigest())=={k:s[k] for k in ('bytes','sha256')}
    assert a==derive(plan,inputs)
    assert a['source']['captured_utc']=='2026-10-19T20:27:58.247940+00:00'
    assert dg(D/a['source']['file'])==dict(bytes=618718,sha256='3975fec856ada335526b35504ab3ca058dbf8f2885169944e0a819d45990fd6a')
    raw=(D/a['source']['file']).read_text()
    for b in a['blocks']:
        assert raw[b['raw_start']:b['raw_end']]==b['raw_html']
        assert raw.count('\n',0,b['raw_start'])+1==b['html_line']
        assert b['raw_start']-raw.rfind('\n',0,b['raw_start'])-1==b['html_column']
    for x in a['resources']:assert sha256(raw[x['raw_start']:raw.index('>',x['raw_start'])+1].encode()).hexdigest()==x['starttag_sha256'] and x['pixels_or_destination_inspected'] is False
    assert a['owner_requirements']==load(D/'requirements.json') and a['owner_cases']==load(D/'cases.json')
    req=[r for rows in a['owner_requirements'].values() for r in rows];cases=a['owner_cases']
    assert len(req)==len({r['id'] for r in req})==61 and len(cases)==len({c['id'] for c in cases})==88
    assert Counter(r['strength'] for r in req)==dict(D=46,U=15) and Counter(c['strength'] for c in cases)==dict(D=72,U=16)
    for name in ['simpler','sampler','impulse']:
        spec=next(s['text'] for s in inputs['canonical_snapshots'] if s['original_canonical']==f'wiki/specs/device-{name}.md')
        for r in a['owner_requirements'][name]:assert r['body'] in spec and spec.count('### '+r['id']+' — ')==1
    for i,c in enumerate(cases):
        assert c['exact_12_4_3']=='U' and c['executed'] is False
        if c['strength']=='U':assert c['comparator']=='unknown'
        s=a['case_scope'][i];assert pointer(a,s['pointer'])==c and pointer(a,s['action_pointer'])==c['action']
        assert s['actual_expected'] is s['actual_comparison'] is None and s['target']=='U' and s['executed'] is False
    for ident in ['SIMPLER-022','SAMPLER-025']:assert next(c for c in cases if c['id']==ident)['positive_control']
    guards(a);reject=[]
    mutations=[('omit-context',None),('wrong-pointer',None),('invent-oracle',None),('erase-corrected-LFO',None),('erase-corrected-filter',None),('erase-true-loop',None),('Volume-to-Filter-association',None),('empty-alt-label-invention',None),('Reverse-parity-borrow',None),('both-voices-unproductive',(3,'proposed_future_positive_baseline','Onlyenabledflags')),('slice-name-positive',(5,'proposed_future_positive_baseline','Namesonly')),('Volume-proves-Filter',(9,'proposed_future_positive_baseline','Volumeprovesallroutes')),('conversion-sound-identity',(12,'proposed_future_positive_baseline','Alwaysequivalent')),('universal-surface',(13,'proposed_minimal_delta','Allsurfacesalwayslock')),('NormalizePan-center',(14,'proposed_future_positive_baseline','Alwayscenter')),('one-zone-instead-of-three',(15,'proposed_minimal_delta','Keyonly')),('RR-bounded-completion',(16,'proposed_future_positive_baseline','Twentytrialsprovecomplete')),('unlooped-law-applied-to-loops',(18,'proposed_future_positive_baseline','Endalwaysterminates')),('VolumeEnd-invented',(19,'proposed_minimal_delta','AllenvelopeshaveEnd')),('empty-Osc-negative-vacuous',(20,'proposed_future_positive_baseline','Emptyfileonly')),('one-order-component',(22,'proposed_future_positive_baseline','Shaperenabledonly')),('Aux-one-target',(24,'proposed_future_positive_baseline','Oneflag')),('MIDI-codec-law',(25,'proposed_future_positive_baseline','14bitdeterminescodec')),('external-input-invented',(26,'proposed_future_positive_baseline','REXsupplied')),('Impulse-middlemap-invented',(27,'proposed_future_positive_baseline','Diatonicmap')),('Link-no-second-voice',(29,'proposed_future_positive_baseline','Onlyslot7exists')),('Gate-borrowed-FadeOut',(31,'proposed_minimal_delta','SameasSimplerFade')),('output-picker-is-audio',(32,'proposed_future_positive_baseline','Pickerpresenceonly'))]
    for name,change in mutations:
        t=deepcopy(a)
        if change:
            i,k,v=change;t['proposals'][i][k]=v
        elif name=='omit-context':t['assessments'].pop()
        elif name=='wrong-pointer':t['assessments'][1]['source_pointer']='/blocks/2/text'
        elif name=='invent-oracle':t['proposals'][0]['actual_expected']='pass'
        elif name=='Volume-to-Filter-association':
            by={x['local_block']:x for x in t['assessments']};by['simpler:B056']['represented_case_refs']=deepcopy(by['simpler:B063']['represented_case_refs'])
        elif name=='empty-alt-label-invention':next(x for x in t['assessments'] if x['local_block']=='sampler:B108')['assessment']='Image establishes exact Off glyph'
        elif name=='Reverse-parity-borrow':t['common_future_prerequisites']['loops']='BothReversecommandscreatecopies'
        else:
            local={'erase-corrected-LFO':'simpler:B063','erase-corrected-filter':'sampler:B157','erase-true-loop':'sampler:B102'}[name];next(x for x in t['assessments'] if x['local_block']==local)['represented_case_refs']=[]
        try:guards(t)
        except AssertionError:reject.append(name)
        else:raise AssertionError('Unsafe mutation accepted '+name)
    bs,rs=parser()('<p>Outside</p><div id="chapter_content"><h1 id="r">Root</h1><div><h2 id="sampler">Sampler</h2><p>Sample End, unless looping.</p><ul><li>End qualified.</li></ul><table><tr><td>Cell A</td><td>Cell B</td></tr></table><img alt="" src="unopened"><figcaption>Caption.</figcaption></div></div><p>After</p>','TEST')
    assert [b['kind'] for b in bs]==['h1','h2','p','li','tr'] and bs[-1]['cells'][1]['text']=='Cell B' and [r['kind'] for r in rs]==['image','caption']
    links=0
    for url in re.findall(r'\]\(([^)]+)\)',(P/'README.md').read_text()):assert (P/url.split('#')[0]).exists();links+=1
    for q in P.iterdir():
        if q.is_file():
            b=q.read_bytes();assert b.endswith(b'\n') and b'\0' not in b and all(x.rstrip(b' \t')==x for x in b.splitlines())
    if (P/'manifest.json').exists():
        m=load(P/'manifest.json');assert set(m['files'])=={p.name for p in P.iterdir() if p.is_file()}-{'manifest.json'}
        for name,v in m['files'].items():assert dg(P/name)==v
    assert before=={str(p):dg(p) for p in watch}
    print(json.dumps(dict(status='pass',sealed=(P/'manifest.json').exists(),summary=a['summary'],negative_fixtures=reject,parser_table_boundary_fixture=True,links=links,watched_paths=len(watch),all_unchanged=True,writes=False,old_main_decodes_samples_or_runtime=False),indent=2))


if __name__=='__main__':
    main()
