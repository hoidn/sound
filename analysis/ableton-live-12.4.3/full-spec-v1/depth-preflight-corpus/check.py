"""Corpus D01 preflight: read-only retained data/hash/pointer checks; no original calls."""
from pathlib import Path
from hashlib import sha256
from collections import Counter, defaultdict
from copy import deepcopy
import json, re, sys
A = Path(__file__).resolve().parent
R = A.parents[3]
H = R/'handoff/device-corpus-v1'
T = R/'analysis/ableton-live-12.4.3/handoff-staging/device-corpus-v1-analysis/traceability.json'
def j(p): return json.loads(p.read_text())
def dg(p):
    b = p.read_bytes()
    return dict(bytes=len(b), sha256=sha256(b).hexdigest())
def ptr(x,p):
    assert p.startswith('/')
    for k in p[1:].split('/'):
        if isinstance(x,list):
            assert re.fullmatch(r'0|[1-9][0-9]*',k)
            x=x[int(k)]
        else: x=x[k.replace('~1','/').replace('~0','~')]
    return x
def semantic(p):
    assert p['release']['entire_resonator_models_omitted']==[]
    assert p['release']['model_index_values_present']==list(range(7))
    assert p['release']['graded_modal_occurrences']==1427 and p['release']['omitted_modal_occurrences']==174
    assert p['numerator']['newly_graded_outcomes']==0 and p['numerator']['candidate_conformance'].startswith('not-run/not-assessed')
    assert p['numerator']['complete_profiles']==p['numerator']['complete_family_contracts']==0
    assert p['r3_requirement_source_asof']['revision']==3 and not p['r3_requirement_source_asof']['future_live_hash_gate']
    assert len(p['r3_direct_U_requirement_contexts'])==5
    assert [x['requirement'] for x in p['r3_direct_U_requirement_contexts']]==['REQ-DEVICE-CORPUS-'+s for s in ['001','002','009','011','013']]
    for x in p['r3_direct_U_requirement_contexts']:
        assert x['new_expected'] is x['new_comparison'] is None and not x['executed']
        assert x['named_route'] and x['exact_r3_unknown_contexts']
        for q in x['exact_r3_unknown_contexts']:
            assert q['quote'].startswith(('- **U.**','- **X, U.**'))
            assert sha256(q['quote'].encode()).hexdigest()==q['sha256']
    assert len(p['unreleased_U_case_rows'])==4 and all(' | U | ' in x for x in p['unreleased_U_case_rows'])
    assert p['new_normative_IDs']==p['new_cases']==p['coverage_credit']==0 and not p['complete'] and not p['new_source_capture']
    assert not any(p['execution'].values())
    for x in p['context_asof']['excerpts']:
        assert not x['future_live_hash_gate'] and sha256(x['quote'].encode()).hexdigest()==x['quote_sha256']
    assert 'ordinary Reset has none' in p['protocol_correction'] and 'never automatically replaced' in p['protocol_correction']
    return True
def main():
    assert sys.dont_write_bytecode and sys.argv[1:]==['--check'], 'Readonly --check only; unsupported arguments refused before inputs'
    p=j(A/'preflight.json');m=j(H/'manifest.json');cases=j(H/'cases.json');t=j(T)
    watch={R/q for q in p['immutable_pins']}|{H/q['path'] for q in m['files']}|{q for q in A.iterdir() if q.is_file()}
    before={str(q):dg(q) for q in watch}
    for path,row in p['immutable_pins'].items(): assert dg(R/path)==row,path
    for row in m['files']: assert dg(H/row['path'])=={k:row[k] for k in ['bytes','sha256']},row['path']
    ev=[e for c in cases['cases'] for e in c['evaluations']]
    assert len(cases['cases'])==24 and len(ev)==len(t['evaluations'])==68 and len(m['files'])==83
    assert all(len(e['parameters'])==len(e['parameter_order'])==38 for e in ev)
    assert sorted({int(e['parameters']['ResonanceType']) for e in ev})==list(range(7))
    assert sum(len(v) for e in ev if e['metric']['kind']=='modal' for v in e['metric']['modes'])==1427
    counts=Counter();omitted=0
    assert len(p['omitted_modal_modes'])==sum(bool(e['ungraded_modes']) for e in t['evaluations'])==14
    for row in p['omitted_modal_modes']:
        assert R/row['source_path']==T
        original=ptr(t,row['source_pointer']);grouped=defaultdict(list)
        for q in original:grouped[(q['channel'],q['why'])].append(q['mode']);counts[q['why']]+=1
        expected=[dict(channel=k[0],why=k[1],mode_indices=v) for k,v in grouped.items()]
        assert row['groups']==expected and row['occurrences']==len(original)
        assert ptr(t,row['source_pointer'].rsplit('/',1)[0])['evaluation']==row['evaluation']
        omitted+=len(original)
    assert omitted==174 and dict(counts)==p['release']['omitted_occurrence_reasons']
    assert sorted(counts.values())==[2,172]
    semantic(p)
    rejected=[]
    for name,change in [('model-omission',lambda x:x['release'].update(entire_resonator_models_omitted=['Tube'])),('target-promotion',lambda x:x['r3_direct_U_requirement_contexts'][0].update(new_expected='pass')),('row-count-as-depth',lambda x:x['numerator'].update(newly_graded_outcomes=13)),('candidate-fraction',lambda x:x['numerator'].update(candidate_conformance='0/68')),('execution',lambda x:x['execution'].update(original_or_X=True)),('mutable-gate',lambda x:x['context_asof']['excerpts'][0].update(future_live_hash_gate=True))]:
        q=deepcopy(p);change(q)
        try: semantic(q)
        except AssertionError: rejected.append(name)
        else: raise AssertionError('Unsafe variant accepted '+name)
    for pointer in ['/evaluations/-1','/evaluations/999','/wrong/0']:
        try: ptr(t,pointer)
        except (AssertionError,KeyError,IndexError): rejected.append(pointer)
        else: raise AssertionError('Invalid source pointer accepted')
    sealed=(A/'manifest.json').exists()
    if sealed:
        seal=j(A/'manifest.json');assert set(seal['files'])=={q.name for q in A.iterdir() if q.is_file() and q.name!='manifest.json'}
        for name,row in seal['files'].items():assert dg(A/name)==row,name
    for target in re.findall(r'\]\(([^)]+)\)',(A/'README.md').read_text()):
        assert (A/target.split('#')[0]).exists(), target
    for q in A.iterdir():
        if q.is_file():assert all(s==s.rstrip() for s in q.read_text().splitlines()),q
    assert before=={str(q):dg(q) for q in watch}
    print(json.dumps(dict(status='pass',sealed=sealed,release_payloads=83,case_groups=24,evaluations=68,historical_released_modal_occurrences=1427,omitted_occurrences=omitted,omitted_evaluations=14,source_pointer_groups=14,direct_U_headings=5,immutable_pins=len(p['immutable_pins']),rejected_fixtures=rejected,watch_unchanged=len(watch),original_execution=False,newly_graded_outcomes=0,writes=False,complete=False),indent=2))
if __name__=='__main__': main()
