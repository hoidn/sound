"""Read-only retained external-routing source audit. No hardware, configuration or old tool."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime,timezone
import copy,json,sys
P=Path(__file__).resolve().parent
R=P.parents[3]
O=P.parent/'external-hardware'
def j(p):return json.loads(p.read_text())
def dg(p):
    b=p.read_bytes();return dict(bytes=len(b),sha256=sha256(b).hexdigest())
def ptr(v,path):
    for k in path.strip('/').split('/') if path else []:v=v[int(k)] if isinstance(v,list) else v[k]
    return v
def shape(a,p):
    assert len(a['blocks'])==len(a['assessments'])==20 and len(a['resources'])==9
    assert len(a['owner_requirements'])==24 and len(a['owner_cases'])==56
    assert a['owner_requirements']==j(O/'requirements.json') and a['owner_cases']==j(O/'cases.json') and a['owner_fixtures']==j(O/'fixtures.json')
    assert a['summary']==dict(new_normative_IDs=0,new_cases=0,adoption=0,coverage_credit=0,complete=False)
    assert p==dict(judgments=a['assessments'],proposals=a['proposals'],source_questions=a['source_questions'],common_future_prerequisites=a['common_future_prerequisites'])
    assert a['source_scope']['atomic_coverage'] is False and not a['source_scope']['pixels_and_destinations_inspected']
    for i,(b,q) in enumerate(zip(a['blocks'],a['assessments'])):
        assert q['id']==f'EHSA-A{i+1:03}' and q['block_id']==b['id'] and ptr(a,q['block_pointer'])==b
        assert not q['complete'] and not q['coverage_credit'] and q['target']=='U' and q['assessment']
        for rr in q['requirement_references']:
            r=ptr(j(R/rr['path']),rr['pointer']);assert r['id']==rr['id'] and rr['field']=='contract' and any(e['block']==q['local_block'] for e in r['evidence'])
        for rr in q['case_references']:
            c=ptr(j(R/rr['path']),rr['pointer']);assert c['id']==rr['id'] and 'action' in rr['fields'] and any(e['block']==q['local_block'] for e in c['evidence'])
    assert len(a['proposals'])==3 and len(a['source_questions'])==4
    for g in a['proposals']:
        assert all(g[k] is None for k in ['documentary_expected','documentary_comparison','actual_expected','actual_comparison'])
        assert g['target']=='U' and not g['executed'] and not g['complete'] and not g['new_normative_IDs'] and not g['coverage_credit']
        assert g['source_blocks'] and set(g['source_blocks'])<={b['id'] for b in a['blocks']}
    checks={2:['BOTH Configure','does not explicitly vary'],3:['actually clicks EACH','already admits BOTH'],5:['SIGNAL-MIX already actually selects','not universal insertion default'],6:['already compares OFF/ON','no numeric negation'],7:['state-only','guidance','BEFORE rate change'],13:['actually selects AN auxiliary','not two independent plugin-channel choices'],14:['before/after supported','No Configure'],15:['actually selects auxiliary','No missing auxiliary-selection claim'],17:['EI009 selects internal','no physical timing proof']}
    for n,parts in checks.items():assert all(x in a['assessments'][n]['assessment'] for x in parts),(n,parts)
    g=a['proposals'];assert 'EACH To/From' in g[0]['proposed_minimal_delta'] and 'two-channel' in g[1]['title']
    assert 'OPTIONAL' in g[2]['proposed_minimal_delta'] and 'BEFORE' in g[2]['proposed_minimal_delta']
    assert 'no cross-unit conversion' in g[2]['proposed_future_positive_baseline']
    c=a['common_future_prerequisites'];assert 'EACH independent genuinely NONEMPTY' in c['policy'] and 'BOTH main/auxiliary and dry/return' in c['policy']
    assert 'no copied Configure/sendGain/DryWet' in c['roles'] and 'no physical timing from disabled state' in c['units']
    assert all(c['expected'] is None and c['comparison'] is None and not c['executed'] for c in a['owner_cases'])
    return True
def negatives(a,p):
    tests=[('oracle',lambda a:a['proposals'][0].update(actual_expected='pass')),('completion',lambda a:a['summary'].update(complete=True)),('atomic',lambda a:a['source_scope'].update(atomic_coverage=True)),('old-case',lambda a:a['owner_cases'][0].update(action='changed')),('wrong-body-pointer',lambda a:a['assessments'][1]['requirement_references'][0].update(pointer='/1')),('peak-click-erased',lambda a:a['assessments'][3].update(assessment='Indicators inspected only')),('single-plugin-channel-promoted',lambda a:a['assessments'][13].update(assessment='Two plugin channels changed')),('aux-selection-erased',lambda a:a['assessments'][15].update(assessment='Only auxiliary listing inspected')),('optional-guidance-mandatory',lambda a:a['proposals'][2].update(proposed_minimal_delta='Always calibrate to minimum latency')),('positive-erased',lambda a:a['common_future_prerequisites'].update(policy='Enabled flag alone')),('instrument-controls-borrowed',lambda a:a['common_future_prerequisites'].update(roles='Instrument has Configure/sendGain/DryWet')),('disabled-proves-timing',lambda a:a['common_future_prerequisites'].update(units='Disabled slider proves perfect compensation'))]
    for name,mutate in tests:
        aa=copy.deepcopy(a);mutate(aa);pp=dict(judgments=aa['assessments'],proposals=aa['proposals'],source_questions=aa['source_questions'],common_future_prerequisites=aa['common_future_prerequisites'])
        try:shape(aa,pp)
        except (AssertionError,KeyError,IndexError):pass
        else:raise AssertionError('Unsafe fixture accepted '+name)
    return [n for n,_ in tests]
def main():
    assert sys.dont_write_bytecode and sys.argv[1:]==['--check'],'Read-only --check only; no writer or old main.'
    inp=j(P/'inputs.json');paths={x for x in P.iterdir() if x.is_file()}|{R/x for x in inp['files']}|{R/x for x in inp['canonical_asof']};before={p:dg(p) for p in paths}
    for path,digest in inp['files'].items():assert dg(R/path)==digest,path
    assert len(inp['old_packet_files'])==39
    for path,digest in inp['old_packet_files'].items():assert dg(O/path)==digest
    for path,row in inp['canonical_asof'].items():assert dg(R/row['provider'])=={k:row[k] for k in ['bytes','sha256']}
    a=j(P/'audit.json');p=j(P/'plan.json');shape(a,p);bad=negatives(a,p)
    parser=R/inp['parser'];assert dg(parser)['sha256']=='648bb1ebce827d136ab6074d6b80fe32475534d87d57a367e9de9aa9fc8fdad8';ns={};exec(compile(parser.read_text(),str(parser),'exec'),ns)
    blocks=[];resources=[]
    for source,sid,anchor in [('D12-AUDIO-EFFECTS','FX','external-audio-effect'),('SAMPLE-INSTRUMENTS-MANUAL','INST','external-instrument')]:
        src=next(s for s in a['sources'] if s['id']==source);raw=Path(src['path']);assert dg(raw)=={k:src[k] for k in ['bytes','sha256']}
        bb,rr=ns['extract'](raw.read_text(),sid);blocks += [b for b in bb if any(h['level']==2 and h['anchor']==anchor for h in b['heading_context'])];resources += [r for r in rr if r['heading_context_anchor']==anchor]
    assert blocks==a['blocks'] and resources==a['resources']
    sample='<div id="chapter_content"><h2 id="a">A</h2><p>inline <b>text</b></p><ul><li>x</li></ul><table><tr><td>one</td><td>two</td></tr></table><h2 id="b">B</h2><p>outside</p></div>'
    bb,rr=ns['extract'](sample,'TEST');assert [b['kind'] for b in bb]==['h2','p','li','tr','h2','p'] and bb[3]['text']=='one | two' and not rr
    for path in P.iterdir():
        if path.suffix in ['.json','.md','.py']:
            text=path.read_text();assert '\x00' not in text and text.endswith('\n') and all(s.rstrip()==s for s in text.splitlines())
    sealed=(P/'manifest.json').exists()
    if sealed:
        m=j(P/'manifest.json');assert set(m['payloads'])=={str(p.relative_to(R)) for p in P.iterdir() if p.is_file() and p.name!='manifest.json'}
        for path,digest in m['payloads'].items():assert dg(R/path)==digest
    assert before=={p:dg(p) for p in paths},'Read-only watch changed'
    print(json.dumps(dict(status='pass' if sealed else 'pass-unsealed-preflight',utc=datetime.now(timezone.utc).isoformat(),sealed=sealed,whole_context_blocks=20,resources=9,requirements=24,cases=56,old_files_exact=39,input_pins=49,proposals=3,questions=4,unsafe_fixtures_rejected=bad,parser_scope_fixture=True,watched_unchanged=len(paths),writes=False,adoption=0,complete=False,limits='Finite retained source/catalog integrity only; independent semantic review pending. No runtime/configuration/hardware or coverage result.'),indent=2))
if __name__=='__main__':main()
