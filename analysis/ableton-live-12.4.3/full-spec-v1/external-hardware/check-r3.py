"""Read-only bounded external-routing owner data check. No old tools or hardware/configuration."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime,timezone
import copy,json,re,sys
P=Path(__file__).resolve().parent
R=P.parents[3]
A=P.parent/'external-hardware-source-audit'
def j(p):return json.loads(p.read_text())
def dg(p):
    b=p.read_bytes();return dict(bytes=len(b),sha256=sha256(b).hexdigest())
def shape(c,f,ad):
    assert len(c)==60 and c[:56]==j(P/'cases.json') and len({x['id'] for x in c})==60
    req={r['id'] for r in j(P/'requirements.json')};assert len(req)==24
    planned=[('EHW-EA-011','REQ-EHW-EA-002',0,2),('EHW-EI-011','REQ-EHW-EI-002',1,13),('EHW-EA-012','REQ-EHW-EA-007',2,7),('EHW-EI-012','REQ-EHW-EI-006',2,17)]
    a=j(A/'audit.json')
    for x,(ident,rid,gn,bi) in zip(c[56:],planned):
        assert x['id']==ident and x['requirements']==[rid] and rid in req and x['adoption_group']==a['proposals'][gn]['id']
        assert x['strength']=='U' and x['exact_target_applicability']=='unknown' and not x['executed']
        assert all(x[k] is None for k in ['documentary_expected','documentary_comparator','expected','comparison','actual_expected','actual_comparison'])
        assert x['source_references']==[dict(path=str((A/'audit.json').relative_to(R)),pointer=f'/blocks/{bi}',block_id=a['blocks'][bi]['id'])]
        assert 'EACH independent genuinely NONEMPTY' in x['setup'] and 'BOTH main/aux and dry/return' in x['setup'] and 'no audio/hardware signal' in x['setup']
        assert x['fixture']=='fixtures-r3.json#/current_version_overlay'
    assert 'BOTH existing Configure' in c[56]['action'] and 'EACH To/From chooser before and after' in c[56]['action']
    assert 'actually choose one admitted lower MIDI channel then another' in c[57]['action'] and 'actual single channel+aux selection' in c[57]['action']
    for x,device in zip(c[58:],['External Audio Effect','External Instrument']):
        assert x['device']==device and 'For '+device+' ONLY' in x['action']
        assert 'OPTIONAL' in x['action'] and 'milliseconds BEFORE a successful rate change' in x['action'] and 'never requires calibration success' in x['action']
    o=f['current_version_overlay'];assert 'no audio/hardware signal' in o['policy'] and 'EACH independent genuinely NONEMPTY' in o['positive']
    assert 'Instrument has no inherited Configure/sendGain/DryWet' in o['roles'] and 'disabled slider is not physical compensation proof' in o['roles']
    assert 'Guidance OPTIONAL' in o['units'] and 'no mandatory' in o['units']
    assert f['actual_oracles']==[dict(id=x['id'],expected=None,comparison=None,target='U',executed=False) for x in c]
    assert f['source_questions']==a['source_questions'] and len(ad['groups'])==3 and not ad['new_normative_IDs'] and not ad['complete']
    assert 'historical_source_audit' in ad
    for n,(g,oldg) in enumerate(zip(ad['groups'],a['proposals'])):
        assert g['id']==oldg['id'] and g['audit_pointer']==f'/proposals/{n}' and g['source_blocks']==oldg['source_blocks']
        assert g['new_cases']==[x['id'] for x in c[56:] if x['adoption_group']==g['id']]
        assert not g['complete'] and not g['coverage_credit'] and not g['executed']
        assert all(g[k] is None for k in ['documentary_expected','documentary_comparison','actual_expected','actual_comparison'])
    return True
def main():
    assert sys.dont_write_bytecode and sys.argv[1:]==['--check'],'Read-only --check only; no writer or old-tool replay.'
    inp=j(P/'inputs-r3.json');wiki=[R/'wiki/specs/external-hardware-devices.md',R/'wiki/research/external-hardware-devices.md']
    paths={p for p in P.rglob('*') if p.is_file()}|{R/p for p in inp['files']}|set(wiki);before={p:dg(p) for p in paths}
    assert len(inp['old_packet_files'])==39
    for path,row in {**inp['old_packet_files'],**inp['files']}.items():assert dg(R/path)==row,path
    c=j(P/'cases-r3.json');f=j(P/'fixtures-r3.json');ad=j(P/'adoption-r3.json');shape(c,f,ad)
    tests=[('old-case',lambda c,f,a:c[0].update(action='changed')),('new-oracle',lambda c,f,a:c[56].update(documentary_expected='pass')),('actual-oracle',lambda c,f,a:f['actual_oracles'][0].update(expected='pass')),('source-pointer',lambda c,f,a:c[56]['source_references'][0].update(pointer='/blocks/0')),('config-inspection',lambda c,f,a:c[56].update(action='Inspect settings only')),('single-plugin-channel',lambda c,f,a:c[57].update(action='Select one channel')),('mandatory-calibration',lambda c,f,a:c[58].update(action='Always calibrate to minimum latency')),('wrong-device-guidance',lambda c,f,a:c[59].update(device='External Audio Effect')),('positive-erased',lambda c,f,a:c[56].update(setup='enabled flag')),('instrument-controls-copied',lambda c,f,a:f['current_version_overlay'].update(roles='Instrument has Configure and DryWet')),('group-complete',lambda c,f,a:a['groups'][0].update(complete=True))]
    for name,fn in tests:
        cc,ff,aa=copy.deepcopy((c,f,ad));fn(cc,ff,aa)
        try:shape(cc,ff,aa)
        except (AssertionError,KeyError,IndexError):pass
        else:raise AssertionError('Unsafe fixture accepted '+name)
    section=lambda t:t.split('## Individual requirements\n',1)[1].split('## Timing, lifecycle and boundary obligations\n',1)[0]
    assert section(wiki[0].read_text())==section((P/'spec-r2.md').read_text())
    assert {r['id'] for r in j(P/'requirements.json')}==set(re.findall(r'^\| (REQ-[A-Z0-9-]+) \|',wiki[0].read_text(),re.M))
    assert all(r['contract'] in wiki[0].read_text() for r in j(P/'requirements.json'))
    for name,p in [('spec-r3.md',wiki[0]),('research-r3.md',wiki[1])]:assert (P/name).read_bytes()==p.read_bytes()
    pending=[];links=0
    for p in [*wiki,P/'README-r3.md']:
        text=p.read_text();assert '\x00' not in text and text.endswith('\n') and all(s.rstrip()==s for s in text.splitlines())
        for target in re.findall(r'\[[^\]]*\]\(([^)\s]+)\)',text):
            if re.match(r'(https?://|mailto:|#)',target):continue
            dest=(p.parent/target.split('#',1)[0]).resolve()
            if not dest.exists() and not(P/'manifest-author-r3.json').exists() and dest in {P/'manifest-author-r3.json',P/'validation-r3.json'}:pending.append(str(dest.relative_to(R)));continue
            assert dest.exists(),(p,target);links+=1
    sealed=(P/'manifest-author-r3.json').exists()
    if sealed:
        m=j(P/'manifest-author-r3.json');assert set(m['payloads'])=={str(p.relative_to(R)) for p in P.rglob('*') if p.is_file() and p.name!='manifest-author-r3.json'}
        for path,row in m['payloads'].items():assert dg(R/path)==row
    assert before=={p:dg(p) for p in paths},'Read-only watch changed'
    print(json.dumps(dict(status='pass' if sealed else 'pass-unsealed-preflight',utc=datetime.now(timezone.utc).isoformat(),sealed=sealed,pending_declared_artifacts=sorted(set(pending)),requirements=24,normative_section_exact=True,cases=60,old_case_objects_exact=56,old_files_exact=39,new_documentary_null=4,current_actual_null_U=60,partial_groups=3,unsafe_fixtures_rejected=[n for n,_ in tests],input_pins=len(inp['files']),watched_unchanged=len(paths),links=links,writes=False,complete=False,limits='Finite owner integrity/author guards only. Independent semantic review pending; no runtime/configuration/hardware or coverage outcome.'),indent=2))
if __name__=='__main__':main()
