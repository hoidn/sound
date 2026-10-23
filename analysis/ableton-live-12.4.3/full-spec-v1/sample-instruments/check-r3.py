"""Read-only Sample owner R3 data check; no old tools, preset decode or source execution."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import copy, json, re, sys
P=Path(__file__).resolve().parent
ROOT=P.parents[3]
A=P.parent/'sample-instruments-source-audit'
def load(p):return json.loads(p.read_text())
def identity(p):
    b=p.read_bytes();return dict(bytes=len(b),sha256=sha256(b).hexdigest())
def pointer(value,path):
    for k in path.strip('/').split('/') if path else []:
        k=k.replace('~1','/').replace('~0','~');value=value[int(k)] if isinstance(value,list) else value[k]
    return value
def effective_audit():
    audit=load(A/'audit.json')
    for row in load(A/'correction-r2.json')['changes']:
        if row['catalog']!='audit':continue
        prefix,key=row['pointer'].rsplit('/',1);obj=pointer(audit,prefix)
        assert obj[key]==row['before'];obj[key]=row['after']
    return audit
def validate(req,cases,fixtures,adoption,oldreq,oldcases,audit):
    assert sum(map(len,req.values()))==63 and len(cases)==102
    assert cases[:88]==oldcases and len({c['id'] for c in cases})==102
    for name,old in oldreq.items():assert req[name][:len(old)]==old
    assert {r['id'] for v in req.values() for r in v}-{r['id'] for v in oldreq.values() for r in v}=={'REQ-SIMPLER-024','REQ-SAMPLER-025'}
    ids={r['id'] for v in req.values() for r in v}
    added=cases[88:];assert len(added)==14
    for c in added:
        assert c['requirement'] in ids and c['strength']=='U' and c['exact_12_4_3']=='U' and not c['executed']
        assert all(c[k] is None for k in ['expected','comparator','documentary_expected','documentary_comparison','actual_expected','actual_comparison'])
        assert c['fixture']=='fixtures-r3.json#/current_version_overlay'
        assert c['action'] and c['documented_predicate'] and 'NONEMPTY' in c['setup'] and 'EACH relevant' in c['setup']
        g=next(g for g in audit['proposals'] if g['id']==c['adoption_group'])
        expected=[dict(path=str((A/'audit.json').relative_to(ROOT)),pointer=f'/blocks/{i}',block_id=b['id']) for i,b in enumerate(audit['blocks']) if b['id'] in g['source_blocks']]
        assert c['source_references']==expected
        for r in expected:assert pointer(audit,r['pointer'])['id']==r['block_id']
    by={c['id']:c for c in added}
    guards={
        'SIMPLER-036':['EACH Classic, One-Shot and Slicing','modified wheel/trackpad','vertical drag','horizontal drag'],
        'SIMPLER-037':['Actually click the Warp as button','setup alone never counts','separate fresh histories','÷2','×2'],
        'SIMPLER-038':['nonzero BEFORE Note On','Move Spread to zero while holding','matched new note','No detune, pan or gain law'],
        'SIMPLER-039':['EACH isolated route','nonzero Filter depth','Volume-only'],
        'SAMPLER-036':['double-click','uncheck Show Preset Name','Small, Medium and Large','without admitted configured supported hardware'],
        'SAMPLER-037':['Actually open the Sample chooser','reopen and select A','never chooser invocation'],
        'SAMPLER-038':['Disable BOTH sustain and release loops','extending beyond','longer-region positive','do not apply this unlooped predicate'],
        'SAMPLER-039':['sustain AND release-loop','back-and-forth sustain','back-and-forth release','nonzero loop fade'],
        'SAMPLER-040':['Click the Sampler image','no MIDI codec'],
        'SAMPLER-041':['Retrigger OFF play a note','Retrigger ON','two-history action','independently prove two'],
        'SAMPLER-042':['Loaded productive SAMPLE','FM and AM','BOTH compared pitches/velocities','not standalone'],
        'IMPULSE-019':['Clip Envelope','then through automation','EACH control source','Exclude global, mute/solo and Link'],
        'IMPULSE-020':['Actually select Trigger','actually select Gate','Sample End','shorter admitted Decay or leave U'],
        'IMPULSE-021':['Actually select the overall','actually select each admitted individual','source-list inspection only']}
    for ident,parts in guards.items():
        text=' '.join(str(v) for v in by[ident].values());assert all(x in text for x in parts),ident
    overlay=fixtures['current_version_overlay']
    assert 'UNLOOPED ONLY' in overlay['qualifiers'] and 'Volume-LFO only' in overlay['qualifiers']
    assert 'EACH relevant' in overlay['productive'] and 'no audio/hardware' in overlay['policy']
    assert overlay['actual_oracles']==[dict(id=c['id'],expected=None,comparison=None,target='U',executed=False) for c in cases]
    assert fixtures['source_questions']==audit['source_questions']
    assert len(adoption['groups'])==33 and 'historical_source_audit' in adoption
    for g,source in zip(adoption['groups'],audit['proposals']):
        assert g['id']==source['id'] and pointer(audit,g['audit_pointer'])==source and g['source_blocks']==source['source_blocks']
        assert g['new_cases']==[c['id'] for c in added if c['adoption_group']==g['id']]
        assert not g['complete'] and not g['coverage_credit'] and not g['executed']
        assert all(g[k] is None for k in ['documentary_expected','documentary_comparison','actual_expected','actual_comparison'])
    assert sum(bool(g['new_cases']) for g in adoption['groups'])==13
    return True
def main():
    assert sys.dont_write_bytecode and sys.argv[1:]==['--check'],'Read-only --check only; no writer or historical replay.'
    inputs=load(P/'inputs-r3.json');wiki=[ROOT/f'wiki/specs/device-{d}.md' for d in ['simpler','sampler','impulse']]+[ROOT/'wiki/research/sample-instruments.md']
    paths={p for p in P.rglob('*') if p.is_file()}|{ROOT/p for p in inputs['files']}|set(wiki)
    before={p:identity(p) for p in paths}
    assert len(inputs['old_packet_files'])==65
    for path,digest in inputs['old_packet_files'].items():assert identity(ROOT/path)==digest,path
    for path,digest in inputs['files'].items():assert identity(ROOT/path)==digest,path
    audit=effective_audit();req=load(P/'requirements-r3.json');cases=load(P/'cases-r3.json');f=load(P/'fixtures-r3.json');ad=load(P/'adoption-r3.json');oldreq=load(P/'requirements.json');oldcases=load(P/'cases.json')
    validate(req,cases,f,ad,oldreq,oldcases,audit)
    negative=[]
    mutations=[('old-body',lambda r,c,f,a:r['simpler'][0].update(body='changed')),('old-case',lambda r,c,f,a:c[0].update(action='changed')),('new-oracle',lambda r,c,f,a:c[88].update(expected='pass')),('actual-oracle',lambda r,c,f,a:f['current_version_overlay']['actual_oracles'][0].update(expected='pass')),('signal-positive',lambda r,c,f,a:c[88].update(setup='flag only')),('source-pointer',lambda r,c,f,a:c[88]['source_references'][0].update(pointer='/blocks/0')),('chooser-inspection',lambda r,c,f,a:c[93].update(action='Inspect chooser display')),('warp-setup',lambda r,c,f,a:c[89].update(action='Set Warp as2bars')),('loop-exception',lambda r,c,f,a:c[94].update(setup='Either loop may be enabled')),('automation-omitted',lambda r,c,f,a:c[99].update(action='Change knob only')),('route-inspection',lambda r,c,f,a:c[101].update(action='Inspect source menu')),('group-complete',lambda r,c,f,a:a['groups'][0].update(complete=True))]
    for name,mutate in mutations:
        rr,cc,ff,aa=copy.deepcopy((req,cases,f,ad));mutate(rr,cc,ff,aa)
        try:validate(rr,cc,ff,aa,oldreq,oldcases,audit)
        except (AssertionError,KeyError,IndexError):negative.append(name)
        else:raise AssertionError('Unsafe fixture accepted '+name)
    for d in ['simpler','sampler','impulse']:
        live=ROOT/f'wiki/specs/device-{d}.md';assert live.read_bytes()==(P/f'spec-{d}-r3.md').read_bytes()
        assert all(r['body'] in live.read_text() for r in req[d])
        assert set(re.findall(r'^### (REQ-[A-Z]+-\d{3}) ',live.read_text(),re.M))=={r['id'] for r in req[d]}
    assert wiki[-1].read_bytes()==(P/'research-r3.md').read_bytes()
    links=0;pending=[]
    for p in [*wiki,P/'README-r3.md']:
        text=p.read_text();assert '\x00' not in text and text.endswith('\n') and all(s.rstrip()==s for s in text.splitlines())
        for target in re.findall(r'\[[^\]]*\]\(([^)\s]+)\)',text):
            if re.match(r'(https?://|mailto:|#)',target):continue
            dest=(p.parent/target.split('#',1)[0]).resolve()
            if not dest.exists() and not(P/'manifest-author-r3.json').exists() and dest in {P/'manifest-author-r3.json',P/'validation-r3.json'}:pending.append(str(dest.relative_to(ROOT)));continue
            assert dest.exists(),(p,target);links+=1
    sealed=(P/'manifest-author-r3.json').exists()
    if sealed:
        manifest=load(P/'manifest-author-r3.json')
        assert set(manifest['payloads'])=={str(p.relative_to(ROOT)) for p in P.rglob('*') if p.is_file() and p.name!='manifest-author-r3.json'}
        for path,digest in manifest['payloads'].items():assert identity(ROOT/path)==digest,path
    assert before=={p:identity(p) for p in paths},'Read-only watch changed'
    print(json.dumps(dict(status='pass' if sealed else 'pass-unsealed-preflight',utc=datetime.now(timezone.utc).isoformat(),sealed=sealed,pending_declared_artifacts=sorted(set(pending)),requirements=63,old_requirement_objects_exact=61,cases=102,old_case_objects_exact=88,old_files_exact=65,new_documentary_null=14,current_actual_null_U=102,selected_partial_groups=13,unadopted_groups=20,unsafe_fixtures_rejected=negative,input_pins=len(inputs['files']),watched_unchanged=len(paths),links=links,writes=False,complete=False,scope='Finite owner data and author guards only; independent semantic review pending, no runtime or coverage credit.'),indent=2))
if __name__=='__main__':main()
