"""Read-only bounded Dynamics R2 analyst-data check. No old tools, source execution or decode."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
from datetime import datetime, timezone
import ast, copy, json, re, sys
P=Path(__file__).resolve().parent
ROOT=P.parents[3]
A=P.parent/'dynamics-source-audit'
PROFILES=['compressor','gate','glue-compressor','limiter','multiband-dynamics']

def load(p):return json.loads(p.read_text())
def identity(p):
    b=p.read_bytes();return dict(bytes=len(b),sha256=sha256(b).hexdigest())
def pointer(v,s):
    for k in s.strip('/').split('/') if s else []:
        k=k.replace('~1','/').replace('~0','~');v=v[int(k)] if isinstance(v,list) else v[k]
    return v

def browser(path):
    t=ast.parse(path.read_text());names={'anchor','frontmatter','cells','spec_rows'}
    nodes=[n for n in t.body if isinstance(n,ast.FunctionDef) and n.name in names]
    assert {n.name for n in nodes}==names
    s={'re':re};exec(compile(ast.Module(body=nodes,type_ignores=[]),str(path),'exec'),s)
    return s['spec_rows']

def planned():
    return [(f'DYN-{p.upper()}-{n:03}',p,g) for p,nums in [
        ('compressor',[(28,1),(29,2),(30,3),(31,4),(32,5)]),
        ('gate',[(25,6),(26,7),(27,4),(28,5)]),
        ('glue-compressor',[(26,8),(27,9),(28,10),(29,4)]),
        ('limiter',[(25,11),(26,12),(27,13),(28,14)]),
        ('multiband-dynamics',[(30,15),(31,16),(32,17),(33,18),(34,19),(35,20),(36,4)])] for n,g in nums]

def data_checks(cases,fixture,adoption,old,audit,req):
    assert len(cases)==153 and cases[:129]==old
    assert len({c['id'] for c in cases})==153
    assert Counter(c['provenance'] for c in cases)==dict(D12=47,Dpkg=5,U=101)
    assert len(req)==62 and req==audit['owner_requirements']
    assert all(c['execution']=='unexecuted; no Live or candidate result' for c in cases)
    ids={r['id'] for r in req}
    for c,(ident,profile,gn) in zip(cases[129:],planned()):
        assert c['id']==ident and c['device']==profile and c['adoption_group']==f'DYSA-G{gn:02}'
        assert c['requirement'] in ids and all(k in ids for k in c['related_requirements'])
        assert c['provenance']=='U' and c['exact_target_applicability']=='unknown' and c['source_claim']
        assert all(c[k] is None for k in ['expected','comparison','documentary_expected','documentary_comparison','actual_expected','actual_comparison'])
        assert c['overlay']=='fixtures-r2.json#/current_version_overlay'
        group=audit['proposals'][gn-1]
        selected=[(i,b) for i,b in enumerate(audit['blocks']) if b['id'] in group['source_blocks'] and any(h['level']==2 and h['anchor']==profile for h in b['heading_context'])]
        assert c['source_references']==[dict(path=str((A/'audit.json').relative_to(ROOT)),pointer='/blocks/'+str(i),block_id=b['id']) for i,b in selected]
        for ref in c['source_references']:assert pointer(audit,ref['pointer'])['id']==ref['block_id']
    assert len(adoption['groups'])==20
    for g,oldg in zip(adoption['groups'],audit['proposals']):
        assert g['id']==oldg['id'] and g['source_blocks']==oldg['source_blocks']
        assert pointer(audit,g['audit_pointer'])==oldg
        assert g['new_cases']==[c['id'] for c in cases[129:] if c['adoption_group']==g['id']] and g['new_cases']
        assert all(g[k] is None for k in ['documentary_expected','documentary_comparison','actual_expected','actual_comparison'])
        assert not g['complete'] and not g['executed'] and not g['coverage_credit'] and g['target']=='U'
    overlay=fixture['current_version_overlay']
    assert overlay['applies_to']==[c['id'] for c in cases]
    assert 'no audio/hardware output' in overlay['policy']
    assert 'NONEMPTY' in overlay['productive'] and 'nonmuted wet/output BEFORE' in overlay['productive']
    assert 'normal AND external-detector' in overlay['detector'] and 'Listen replaces' in overlay['detector']
    assert 'BOTH independent' in overlay['both']
    assert 'GlueRange0 retains independent Makeup/SoftClip' in overlay['neutral'] and 'gains/crossover' in overlay['neutral']
    assert 'N02' in overlay['rates'] and 'EACH rate' in overlay['rates'] and 'do not select a newrate policy' in overlay['rates']
    assert 'not a Dpkg file-grade rewrite' in overlay['file_only']
    assert fixture['source_questions']==audit['source_questions']
    assert len(fixture['actual_oracles'])==153
    for c,o in zip(cases,fixture['actual_oracles']):assert o==dict(id=c['id'],actual_expected=None,actual_comparison=None,target='U',executed=False)
    by={c['id']:c for c in cases}
    fragments={
        'DYN-COMPRESSOR-028':['productive compression','whole-path identity'],
        'DYN-COMPRESSOR-031':['normal AND external-detector','Makeup availability using old003','Listen replaces'],
        'DYN-COMPRESSOR-032':['OPTIONAL','three independent resets','not a required remedy'],
        'DYN-GATE-025':['known productive NONEMPTY open/closed','Floor -inf,0'],
        'DYN-GLUE-COMPRESSOR-026':['BEFORE Range0','productive Makeup/SoftClip','no full bypass/identity'],
        'DYN-GLUE-COMPRESSOR-028':['title-bar context menu','Two-times processing is source-only','MAY exceed0dB','never require overshoot'],
        'DYN-LIMITER-026':['manual Release contribution','SAME manual Release'],
        'DYN-LIMITER-027':['EACH M/S member','both members have independent positives','L/R','Link0 and100','No midpoint law'],
        'DYN-LIMITER-028':['productive active Soft Clip','known nonclip history','without a reconstruction kernel'],
        'DYN-MULTIBAND-DYNAMICS-030':['EACH relevant band','gain AND dynamics','allfour High/Low'],
        'DYN-MULTIBAND-DYNAMICS-031':['independently successful prior region edit','Below edge','double-click','old004/005 true MidAbove'],
        'DYN-MULTIBAND-DYNAMICS-032':['Above attack on upward','Below attack on downward','release on upward'],
        'DYN-MULTIBAND-DYNAMICS-033':['PLUS separately genuinely productive gains and crossover','THEN set Amount0','not total bypass/identity'],
        'DYN-MULTIBAND-DYNAMICS-034':['need no audio/hardware','edit threshold/ratio','old007 page-selection'],
        'DYN-MULTIBAND-DYNAMICS-035':['OPTIONAL','CAN SOMETIMES','MAY destroy','not guaranteed recovery'],
        'DYN-MULTIBAND-DYNAMICS-036':['normal AND external-detector','NO EQ control or main Dry/Wet','Listen replaces']}
    for ident,parts in fragments.items():
        t=by[ident]['setup']+' '+by[ident]['input'];assert all(x in t for x in parts),ident
    return True

def negative_tests(cases,fixture,adoption,old,audit,req):
    tests=[]
    def add(name,fn):tests.append((name,fn))
    add('old-case-edited',lambda c,f,a:c[0].update(input='changed'))
    add('old-Dpkg-promoted',lambda c,f,a:next(x for x in c if x['provenance']=='Dpkg').update(provenance='D12'))
    add('new-documentary-number',lambda c,f,a:c[129].update(expected='numeric comparison'))
    add('new-actual-oracle',lambda c,f,a:c[129].update(actual_expected='pass'))
    add('overlay-actual-oracle',lambda c,f,a:f['actual_oracles'][0].update(actual_comparison='value'))
    add('missing-main-positive',lambda c,f,a:f['current_version_overlay'].update(productive='enabled flag only'))
    add('missing-detector-positive',lambda c,f,a:f['current_version_overlay'].update(detector='normal only'))
    add('one-channel-only',lambda c,f,a:f['current_version_overlay'].update(both='left only'))
    add('rate-policy-invented',lambda c,f,a:f['current_version_overlay'].update(rates='reinterpret unchanged frames at allrates'))
    add('wrong-source-pointer',lambda c,f,a:c[129]['source_references'][0].update(pointer='/blocks/0'))
    def newcase(c,ident):return next(x for x in c if x['id']==ident)
    add('optional-advice-guaranteed',lambda c,f,a:newcase(c,'DYN-MULTIBAND-DYNAMICS-035').update(input='Always restores every input'))
    add('external-Makeup-history-erased',lambda c,f,a:newcase(c,'DYN-COMPRESSOR-031').update(input='Sidechain on, guess Makeup unavailable'))
    add('Range0-identity',lambda c,f,a:newcase(c,'DYN-GLUE-COMPRESSOR-026').update(input='Range0 is full identity'))
    add('SoftClip-unconditional-bound',lambda c,f,a:newcase(c,'DYN-GLUE-COMPRESSOR-028').update(input='Always below -0.5dB'))
    add('Release-unproductive',lambda c,f,a:newcase(c,'DYN-LIMITER-026').update(setup='Auto enabled, knob present'))
    add('Below-crossing-borrowed',lambda c,f,a:newcase(c,'DYN-MULTIBAND-DYNAMICS-032').update(input='Both attack on upward crossing'))
    add('Amount0-gains-erased',lambda c,f,a:newcase(c,'DYN-MULTIBAND-DYNAMICS-033').update(setup='Amount0 is whole bypass'))
    add('Multiband-EQ-borrowed',lambda c,f,a:newcase(c,'DYN-MULTIBAND-DYNAMICS-036').update(input='Enable EQ and main Dry/Wet'))
    for name,fn in tests:
        c,f,a=copy.deepcopy((cases,fixture,adoption));fn(c,f,a)
        try:data_checks(c,f,a,old,audit,req)
        except (AssertionError,KeyError,IndexError):pass
        else:raise AssertionError('Unsafe fixture accepted '+name)
    return [n for n,_ in tests]

PENDING=[]
def links(origin,text):
    count=0
    for target in re.findall(r'\[[^\]]*\]\(([^)\s]+)\)',text):
        if re.match(r'(https?://|mailto:|#)',target):continue
        target=target.split('#',1)[0]
        if not target:continue
        x=(origin.parent/target).resolve()
        if not x.exists() and not(P/'manifest-author-r2.json').exists() and x in {P/'manifest-author-r2.json',P/'validation-r2.json'}:PENDING.append(str(x.relative_to(ROOT)));continue
        assert x.exists(),(origin,target);count+=1
    return count

def main():
    assert sys.dont_write_bytecode and sys.argv[1:]==['--check'],'Read-only --check only; no write mode.'
    first={x:identity(x) for x in P.rglob('*') if x.is_file()}
    inputs=load(P/'inputs-r2.json');wiki=[ROOT/'wiki/specs/dynamics-devices.md',ROOT/'wiki/research/dynamics-devices.md']
    watch=set(first)|{ROOT/x['path'] for x in inputs['files']}|set(wiki);before={x:identity(x) for x in watch}
    assert all(before[x]==v for x,v in first.items())
    for x in inputs['files']:assert identity(ROOT/x['path'])=={k:x[k] for k in ['bytes','sha256']},x['path']
    assert len(inputs['old_packet_files'])==27
    for name,row in inputs['old_packet_files'].items():assert identity(P/name)=={k:row[k] for k in ['bytes','sha256']}
    assert identity(P/'manifest-author-r1.json')['sha256']=='7eaf6c5b97efad1352aaf2820c21a66ebb5c6d53bbf9e7f218df516418a825eb'
    assert identity(A/'manifest.json')['sha256']=='434c0f7bedf3c1d7c720fc506e70ffbf38b8f2df3630e890fdd9c6ae62192c9a'
    audit=load(A/'audit.json');old=load(P/'cases.json');req=load(P/'requirements.json');cases=load(P/'cases-r2.json');fixture=load(P/'fixtures-r2.json');adoption=load(P/'adoption-r2.json')
    parserpath=P.parent/'midi-editing-source-audit/source_parser.py';assert identity(parserpath)['sha256']=='648bb1ebce827d136ab6074d6b80fe32475534d87d57a367e9de9aa9fc8fdad8'
    scope={};exec(compile(parserpath.read_text(),str(parserpath),'exec'),scope)
    raw=Path(audit['source']['path']);assert identity(raw)==dict(bytes=588328,sha256='9cb15cb3d80bda4771e5add2c2b74f5c57d73ee8850e198acf7cf8a51dfd1299')
    blocks,res=scope['extract'](raw.read_text(),'FX');selected=[b for b in blocks if any(h['level']==2 and h['anchor'] in PROFILES for h in b['heading_context'])]
    anchors={h['anchor'] for b in selected for h in b['heading_context'] if h['level']>=2};res=[x for x in res if x['heading_context_anchor'] in anchors]
    assert selected==audit['blocks'] and len(selected)==123 and len(res)==38
    assert [{k:y[k] for k in x} for x,y in zip(res,audit['resources'])]==res
    data_checks(cases,fixture,adoption,old,audit,req);negatives=negative_tests(cases,fixture,adoption,old,audit,req)
    spec=wiki[0].read_text();research=wiki[1].read_text();s0=(P/'spec-r1.md').read_text()
    section=lambda t:t.split('## Individual device requirements\n',1)[1].split('## Measurable acceptance and unresolved cases\n',1)[0]
    assert section(s0)==section(spec),'Normative section must be unchanged'
    assert req==audit['owner_requirements'] and len(req)==62 and all(x['text'] in spec for x in req)
    for snapshot,live in [('spec-r2.md',wiki[0]),('research-r2.md',wiki[1])]:assert (P/snapshot).read_bytes()==live.read_bytes()
    for snap in load(A/'inputs.json')['canonical_snapshots']:assert (ROOT/snap['provider']).read_bytes()==snap['text'].encode()
    norm_ids=[x['id'] for x in browser(ROOT/'tools/spec_browser.py')(wiki[0],spec)]
    assert set(norm_ids)=={x['id'] for x in req} and len(norm_ids)==62
    consumer=load(P/'consumers-asof-r2.json');assert len(consumer['occurrences'])==15 and consumer['paths']==5
    for c in consumer['occurrences']:
        assert pointer(load(ROOT/c['consumer']['path']),c['pointer'])==c['sha256']
        assert identity(ROOT/c['historical_provider'])['sha256']==c['sha256']
    linkcount=links(wiki[0],spec)+links(wiki[1],research)+links(P/'README-r2.md',(P/'README-r2.md').read_text())
    for p in [P/'check-r2.py',P/'README-r2.md',P/'spec-r2.md',P/'research-r2.md',*wiki]:assert all(x.rstrip()==x for x in p.read_text().splitlines()),p
    sealed=(P/'manifest-author-r2.json').exists()
    if sealed:
        m=load(P/'manifest-author-r2.json');assert {str(x.relative_to(ROOT)) for x in P.rglob('*') if x.is_file()}=={x['path'] for x in m['payloads']}|{str((P/'manifest-author-r2.json').relative_to(ROOT))}
        for row in m['payloads']:assert identity(ROOT/row['path'])=={k:row[k] for k in ['bytes','sha256']},row['path']
    assert before=={x:identity(x) for x in watch},'Read-only watch changed'
    print(json.dumps(dict(status='pass' if sealed else 'pass-unsealed-preflight',utc=datetime.now(timezone.utc).isoformat(),sealed=sealed,pending_declared_artifacts=sorted(set(PENDING)),requirements=62,normative_section_exact=True,browser_IDs=62,cases=153,old_case_objects_exact=129,old_files_exact=27,documentary_D12=47,Dpkg_file_only=5,U=101,new_documentary_null=24,actual_null_U=153,source_blocks=123,literal_resources=38,input_pins=len(inputs['files']),consumer_occurrences=15,consumer_paths=5,unsafe_fixtures_rejected=negatives,links=linkcount,watched_unchanged=len(watch),writes=False,scope='Current owner integrity/finite author guards only; independent ROOT review pending, no runtime/coverage/completion.',complete=False),indent=2))

if __name__=='__main__':main()
