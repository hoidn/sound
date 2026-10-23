"""Read-only one-field A1 R2 provenance correction; no old checker/source execution."""
from pathlib import Path
from hashlib import sha256
from copy import deepcopy
import json
import re
import sys

A = Path(__file__).resolve().parent
R = A.parents[3]
OLD = 'Imported selected alias SNewCompound<AFloatParameterUnit> and literal registration102502328 identify the first constructed class'
NEW = 'Literal registration102502328 retains the class string AFloatParameterUnit and PTR_SNewCompound<AFloatParameterUnit>_1064faf80 label for the first constructed class'

def j(p):
    return json.loads(p.read_text())

def dg(p):
    b = p.read_bytes()
    return dict(bytes=len(b), sha256=sha256(b).hexdigest())

def ptr(v, p):
    assert p.startswith('/')
    for key in p[1:].split('/'):
        if isinstance(v, list):
            assert re.fullmatch(r'0|[1-9][0-9]*', key)
            v = v[int(key)]
        else:
            v = v[key.replace('~1','/').replace('~0','~')]
    return v

def corrected(delta, trace, records):
    assert len(delta['changes']) == 1
    c = delta['changes'][0]
    assert c['pointer'] == '/claims/2/claim' and c['old'] == trace['claims'][2]['claim']
    assert c['old'].count(OLD) == 1 and c['new'] == c['old'].replace(OLD, NEW, 1)
    assert 'Imported selected alias' not in c['new'] and 'PTR_SNewCompound<AFloatParameterUnit>_1064faf80' in c['new']
    s = delta['source']
    assert s == dict(provider='records.json',pointer='/functions/6/record/code',entry='0x102502328',literal_class='AFloatParameterUnit',literal_label='PTR_SNewCompound<AFloatParameterUnit>_1064faf80')
    body = ptr(records, s['pointer'])
    assert records['functions'][6]['record']['entry'] == s['entry']
    assert 'L"AFloatParameterUnit"' in body and s['literal_label'] in body
    assert 'FUN_10147e7c4(&DAT_106e488a8' in body
    # Existing selection does not contain the imported alias, though its parent does.
    assert not any(x['record'].get('name') == 'SNewCompound<AFloatParameterUnit>' for x in records['index_records'])
    assert len(records['functions']) == 45 and len(records['index_records']) == 119
    assert delta['unchanged'] == dict(functions=45,decompiled_code_bytes=35742,index_records=119,source_pins=45,A1='U-unresolved',new_requirements=0,new_cases=0,new_behavioral_oracles=0,coverage_credit=0,complete=False)
    effective = deepcopy(trace)
    effective['claims'][2]['claim'] = c['new']
    restored = deepcopy(effective)
    restored['claims'][2]['claim'] = c['old']
    assert restored == trace and effective['A1'] == 'U-unresolved'
    assert all(effective[k] is None for k in ['documentary_expected','documentary_comparison','actual_expected','actual_comparison'])
    assert effective['new_normative_requirements'] == effective['new_cases'] == []
    return effective

def main():
    assert sys.dont_write_bytecode and sys.argv[1:] == ['--check'], 'Read-only --check only; refusal before inputs'
    delta, trace, records, inp = (j(A/n) for n in ['delta-r2.json','trace.json','records.json','inputs.json'])
    review = A/delta['review']['path']
    paths = {Path(p) if p.startswith('/') else R/p for p in inp['files']} | set(A.iterdir()) | {review}
    before = {str(p):dg(p) for p in paths}
    assert len(delta['preserved_r1_files']) == 6 and len(inp['files']) == 45
    for n, pin in delta['preserved_r1_files'].items():
        assert dg(A/n) == pin
    assert dg(A/'manifest.json') == dict(bytes=2392,sha256='ff706c600ce4fc67bac86e88b2d3a4366dcc11ac1ca4bc2368034558e97fd976')
    for p, pin in inp['files'].items():
        assert dg(Path(p) if p.startswith('/') else R/p) == pin
    assert dg(review) == {k:delta['review'][k] for k in ['bytes','sha256']} == dict(bytes=20905,sha256='88ab28a44225f148c61dd5316b9ddb6c762eab8087d6ed83dbb64fd285693533')
    finding = j(review)['findings'][0]
    assert finding['id'] == 'A1-TRACE-REVIEW-001' and finding['path'] == 'trace.json /claims/2/claim'
    current = corrected(delta,trace,records)
    q = records['functions'][6]
    raw = (Path(q['path']) if q['path'].startswith('/') else R/q['path']).read_bytes().splitlines()[q['line']-1]
    assert sha256(raw).hexdigest() == q['raw_line_sha256'] and json.loads(raw) == q['record']
    assert sha256(ptr(records,delta['source']['pointer']).encode()).hexdigest() == q['record']['code_sha256']
    rejected = []
    for name in ['unsupported-imported-selected-alias','wrong-registration-pointer','wrong-registration-entry','extra-field-change','changed-selection','A1-promoted']:
        d = deepcopy(delta)
        if name == 'unsupported-imported-selected-alias': d['changes'][0]['new'] = d['changes'][0]['old']
        elif name == 'wrong-registration-pointer': d['source']['pointer'] = '/index_records/19/record/name'
        elif name == 'wrong-registration-entry': d['source']['entry'] = '0x1024f5674'
        elif name == 'extra-field-change': d['changes'].append(dict(pointer='/A1',old='U-unresolved',new='S'))
        elif name == 'changed-selection': d['unchanged']['index_records'] = 120
        else: d['unchanged']['A1'] = 'S'
        try:
            corrected(d,trace,records)
        except (AssertionError,KeyError,IndexError,TypeError):
            rejected.append(name)
        else:
            raise AssertionError('Unsafe correction accepted '+name)
    seal = A/'manifest-r2.json'
    if seal.exists():
        m = j(seal)
        assert set(m['files']) == {p.name for p in A.iterdir() if p.name != seal.name}
        for n,pin in m['files'].items():
            assert dg(A/n) == pin
    for p in A.iterdir():
        assert all(l == l.rstrip() for l in p.read_text().splitlines()), p
    for target in re.findall(r'\]\(([^)]+)\)', (A/'README-r2.md').read_text()):
        assert (A/target).exists() or target == 'manifest-r2.json' and not seal.exists()
    assert before == {str(p):dg(p) for p in paths}
    print(json.dumps(dict(status='pass',sealed=seal.exists(),preserved_r1_files=6,unchanged_source_pins=45,reused_bodies=45,reused_index_records=119,changed_trace_fields=['/claims/2/claim'],registration_entry=q['record']['entry'],registration_pointer=delta['source']['pointer'],negative_fixtures=rejected,watch_unchanged=len(paths),old_checker_executed=False,writes=False,A1=current['A1'],new_requirements=0,new_cases=0,new_behavioral_oracles=0,complete=False),indent=2))

if __name__ == '__main__':
    main()
