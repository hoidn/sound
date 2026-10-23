"""Finite retained-data check only. Never imports, compiles or invokes retained original code."""
from pathlib import Path
from hashlib import sha256
from copy import deepcopy
import json
import struct
import sys

A = Path(__file__).resolve().parent
R = A.parents[3]
TARGET = '3a99ceeabce62ccd069b6b55d99d186c9bdf8a6b80a7e3350dd0f9d1c383cfad'

def j(p):
    return json.loads(p.read_text())

def dg(p):
    b = p.read_bytes()
    return {'bytes': len(b), 'sha256': sha256(b).hexdigest()}

def resolve(p):
    return Path(p) if p.startswith('/') else R / p

def pointer(v, p):
    assert p.startswith('/')
    for key in p[1:].split('/'):
        if isinstance(v, list):
            assert key.isdigit() and (key == '0' or not key.startswith('0'))
            v = v[int(key)]
        else:
            v = v[key.replace('~1','/').replace('~0','~')]
    return v

def semantic(t, data):
    assert t['image_sha256'] == TARGET and t['A1'] == 'U-unresolved'
    assert t['source_only'] and not t['original_or_X_executed'] and not t['executed']
    assert t['new_normative_requirements'] == t['new_cases'] == []
    assert all(t[k] is None for k in ['documentary_expected', 'documentary_comparison', 'actual_expected', 'actual_comparison'])
    assert t['target'] == 'U' and t['coverage_credit'] == 0 and not t['complete']
    assert data['original_export_utc'] is None and 'mtime' in data['export_utc_reason']
    fs = {x['record']['entry']: x['record'] for x in data['functions']}
    assert len(fs) == len(data['functions']) == 45
    assert 'return &DAT_106e51f90;' in fs['0x1026f0200']['code']
    assert 'return &DAT_106e51f90;' in fs['0x1026f020c']['code']
    assert 'param_1[1] = param_2;' in fs['0x10150b1cc']['code']
    assert '*puVar2 = &PTR_FUN_1067fb1b8;' in fs['0x1026f070c']['code']
    assert '*param_1 = &PTR_thunk_FUN_1025003c0_1067c7a48;' in fs['0x1024f5710']['code']
    words = {(x['base'], x['slot']): x for x in data['words']['reads']}
    for key, val in [(('0x1067fb1b8','0x170'),'0x1026f020c'), (('0x1067c7a48','0xb8'),'0x1024f5c08'), (('0x1067c74e8','0x280'),'0x1024f51c8')]:
        assert words[key]['value'] == val
    assert len(words) == 12 and len(data['words']['unbacked_metadata']) == 3
    assert len(data['words']['incidental_diagnostic_reads']) == 1
    assert data['words']['incidental_diagnostic_reads'][0]['value'] == '0x10'
    assert all('raw' not in x and 'no retained file bytes' in x['disposition'] for x in data['words']['unbacked_metadata'])
    for claim in t['claims']:
        code_refs = [e for e in claim['evidence'] if 'entry' in e]
        assert [e['entry'] for e in code_refs] == claim.get('entries', [])
        for e in claim['evidence']:
            assert e['path'] == 'records.json'
            v = pointer(data, e['pointer'])
            if 'entry' in e:
                assert v == fs[e['entry']]['code']
    assert [x['id'] for x in t['claims']] == [f'A1-T{x:02}' for x in range(1,9)]
    assert 'not selected on that path' in t['claims'][1]['claim']
    assert 'not a single direct float return' in t['claims'][3]['claim']
    assert 'not a float-current-value getter' in t['claims'][3]['claim']
    assert 'not fully joined' in t['claims'][-1]['claim'] and 'remainsU' in t['claims'][-1]['claim']
    assert len(t['frontier']) == 3 and 'Empty C2 indirect targets are not proof' in t['frontier'][2]['question']
    return True

def main():
    assert sys.dont_write_bytecode and sys.argv[1:] == ['--check'], 'Readonly --check only; refusal before inputs'
    inp, data, t = (j(A / n) for n in ['inputs.json','records.json','trace.json'])
    watch = {resolve(p) for p in inp['files']} | set(A.iterdir())
    before = {str(p): dg(p) for p in watch}
    for p, pin in inp['files'].items():
        assert dg(resolve(p)) == pin, p
    for x in data['functions']:
        raw = resolve(x['path']).read_bytes().splitlines()[x['line']-1]
        assert len(raw) == x['raw_line_bytes'] and sha256(raw).hexdigest() == x['raw_line_sha256']
        assert json.loads(raw) == x['record']
        rec = x['record']
        assert len(rec['code'].encode()) == rec['code_bytes'] and sha256(rec['code'].encode()).hexdigest() == rec['code_sha256']
        assert rec['error'] is None and not rec['partial_code'] and not rec['timed_out']
    # Cache only retained JSON/text inputs as data, no executable source loading.
    line_cache = {}
    for x in data['index_records']:
        path = x['path']
        if path not in line_cache:
            needed = {v['line'] for v in data['index_records'] if v['path'] == path}
            with resolve(path).open('rb') as f:
                line_cache[path] = {n: raw.rstrip(b'\n') for n,raw in enumerate(f,1) if n in needed}
        raw = line_cache[path][x['line']]
        assert sha256(raw).hexdigest() == x['raw_line_sha256'] and json.loads(raw) == x['record']
    image = resolve(data['words']['image']['path'])
    b = image.read_bytes()
    assert len(b) == data['words']['image']['bytes'] and sha256(b).hexdigest() == TARGET
    h = struct.unpack_from('<IiiIIIII', b)
    assert h[0] == 0xfeedfacf and h[1] == 0x100000c and b[:32].hex() == data['words']['image']['header']
    off = 32
    segs = []
    for _ in range(h[4]):
        cmd,size = struct.unpack_from('<II',b,off)
        assert size >= 8
        if cmd == 0x19:
            name,va,vs,fo,fs = struct.unpack_from('<16sQQQQ',b,off+8)
            segs.append(dict(name=name.split(b'\0')[0].decode(),vmaddr=va,vmsize=vs,fileoff=fo,filesize=fs))
        off += size
    assert off == 32+h[5] and segs == data['words']['segments']
    for x in data['words']['reads'] + data['words']['incidental_diagnostic_reads']:
        va = int(x['vmaddr'],16)
        assert va == int(x['base'],16)+int(x['slot'],16)
        s = next(s for s in segs if s['vmaddr'] <= va and va+8 <= s['vmaddr']+s['filesize'])
        fo = s['fileoff']+va-s['vmaddr']
        assert fo == x['fileoff'] and s['name'] == x['segment']
        raw = b[fo:fo+8]
        assert raw.hex() == x['raw'] and hex(int.from_bytes(raw,'little')) == x['value']
    for x in data['words']['unbacked_metadata']:
        va = int(x['vmaddr'],16)
        s = next(s for s in segs if s['vmaddr'] <= va < s['vmaddr']+s['vmsize'])
        assert va+8 > s['vmaddr']+s['filesize'] and x['segment'] == s['name']
    for x in data['excerpts']:
        p = resolve(x['path'])
        if 'text' in x:
            raw = ''.join(p.read_text().splitlines(keepends=True)[x['line_start']-1:x['line_end']])
            assert raw == x['text'] and sha256(raw.encode()).hexdigest() == x['text_sha256']
        else:
            ds = j(p)['disassembly']
            assert [v for v in ds if int(x['address_start'],16) <= int(v['address'],16) <= int(x['address_end'],16)] == x['instructions']
    for x in data['canonical_asof']:
        raw = x['text'].encode()
        assert len(raw) == x['bytes'] and sha256(raw).hexdigest() == x['sha256']
    # No check of current mutable canonical/source consumers is required.
    semantic(t,data)
    bad = []
    variants = [
        ('A1-promoted',lambda t,d:t.update(A1='S-identity-proved')),
        ('actual-oracle',lambda t,d:t.update(actual_expected=0.5)),
        ('documentary-oracle',lambda t,d:t.update(documentary_comparison='exact')),
        ('source-execution',lambda t,d:t.update(original_or_X_executed=True)),
        ('new-normative-credit',lambda t,d:t.update(new_normative_requirements=['REQ-A1'])),
        ('factory-other-branch',lambda t,d:d['words']['reads'][0].update(value='0x1026ee884')),
        ('wrong-bind-slot',lambda t,d:next(x for x in d['words']['reads'] if x['base']=='0x1067c7a48' and x['slot']=='0xb8').update(value='0x1024f5f0c')),
        ('metadata-zero-fill-fabricated',lambda t,d:d['words']['unbacked_metadata'][0].update(raw='0000000000000000')),
        ('mtime-as-export-UTC',lambda t,d:d.update(original_export_utc='2026-10-19T00:00:00Z')),
        ('flag-as-current-value',lambda t,d:t['claims'][3].update(claim='unit directly returns current float')),
        ('empty-target-proof',lambda t,d:t['frontier'][2].update(question='Empty C2 targets prove no edge')),
        ('wrong-code-source-association',lambda t,d:t['claims'][0]['evidence'][0].update(pointer='/functions/0/record/signature')),
        ('frontier-closed',lambda t,d:t['claims'][-1].update(claim='all fully joined; A1 accepted'))]
    for name, change in variants:
        tc,dc = deepcopy(t),deepcopy(data)
        change(tc,dc)
        try:
            semantic(tc,dc)
        except (AssertionError,KeyError,StopIteration):
            bad.append(name)
        else:
            raise AssertionError('Unsafe variant accepted '+name)
    seal = A/'manifest.json'
    if seal.exists():
        m = j(seal)
        assert set(m['files']) == {p.name for p in A.iterdir() if p.name != 'manifest.json'}
        for name,pin in m['files'].items():
            assert dg(A/name) == pin
    for p in A.iterdir():
        assert all(l == l.rstrip() for l in p.read_text().splitlines()), p
    assert before == {str(p): dg(p) for p in watch}
    print(json.dumps(dict(status='pass',sealed=seal.exists(),functions=45,code_bytes=sum(x['record']['code_bytes'] for x in data['functions']),index_records=len(data['index_records']),active_file_backed_words=12,incidental_file_backed_words=1,unbacked_metadata_addresses=3,source_pins=len(inp['files']),negative_fixtures=bad,watch_unchanged=len(watch),writes=False,A1='U-unresolved',new_requirements=0,new_cases=0,coverage_credit=0,complete=False),indent=2))

if __name__ == '__main__':
    main()
