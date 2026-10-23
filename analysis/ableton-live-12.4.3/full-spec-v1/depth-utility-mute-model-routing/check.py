#!/usr/bin/env python3
"""Finite retained-data checks only. No source function is imported or executed."""
import copy
import hashlib
import json
from pathlib import Path
import struct
import sys

P = Path(__file__).resolve().parent
R = P.parents[3]

def pin(p):
    b = p.read_bytes()
    return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}

def path(p):
    p = Path(p)
    return p if p.is_absolute() else R / p

def limited_invariants(data, route):
    fs = {x['entry']: x['record']['code'] for x in data['functions']}
    assert len(fs) == 29
    d = route['object_domains']
    assert d == {'model_device': 'D', 'processor': 'P', 'same_object_proven': False,
                 'wrapper_offset': 0x350, 'wrapped_pointer_offset': 0x358,
                 'wrapper_pointer_delta': 8, 'model_metadata_vslot': 0x170,
                 'unit_bind_vslot': 0xb8}
    assert d['wrapper_offset'] + d['wrapper_pointer_delta'] == d['wrapped_pointer_offset']
    expected = [(0x1065411a0, 0, 0x10216533c), (0x106508df8, 0, 0x10214b918),
                (0x1067f9dd0, 0x170, 0x1026eb7b4),
                (0x1067b4860, 0xb8, 0x10242cb20), (0x106537c78, 0, 0x106d91730)]
    assert len(data['word_reads']['reads']) == 5
    for row, (base, slot, value) in zip(data['word_reads']['reads'], expected):
        assert (int(row['base'], 16), int(row['slot'], 16), int(row['value'], 16)) == (base, slot, value)
        assert int(row['vmaddr'], 16) == base + slot
        assert len(bytes.fromhex(row['raw'])) == 8
        assert struct.unpack('<Q', bytes.fromhex(row['raw']))[0] == value
    limits = route['limits']
    assert limits == {'out_text_storage_pointer_is_name_proof': False, 'guard_contents_proven': False,
                     'public_model_descriptor_join_closed': False, 'application_case_grade': 'U',
                     'application_cases_executed': False, 'requirements_added': 0, 'cases_added': 0,
                     'coverage_credit': 0, 'public_expected': None, 'public_comparison': None}
    assert route['factory_predicate'] == ('Prior float and enum comparisons fail; bool metadata comparison succeeds. '
                                         'Equal bool metadata addresses alone do not prove the preceding failures.')
    assert len(route['claims']) == 12 and len(route['open_joins']) == 6
    for c in route['claims']:
        s = c['source']; f = data['functions'][s['function_index']]
        assert f['entry'] == s['entry']
        assert f['record']['code'][s['code_start']:s['code_end']] == s['text'] and s['text']
        assert c['application_expected'] is None and c['application_comparison'] is None
        assert c['target_grade'] == 'U' and c['executed'] is False
        assert all(type(i) is int and 0 <= i < 29 for i in c['related_function_indices'])
        assert all(type(i) is int and 0 <= i < 5 for i in c['related_word_indices'])
    assert [c['related_word_indices'] for c in route['claims']] == [[], [], [], [2], [3], [], [4], [], [0, 1], [], [], []]
    assert [data['functions'][i]['entry'] for i in route['claims'][9]['related_function_indices']] == ['0x102f50558', '0x10155c8c0']
    assert [data['functions'][i]['entry'] for i in route['claims'][10]['related_function_indices']] == ['0x1025c1e98', '0x1025c1ea8', '0x102f59370', '0x1023a13e8', '0x10247ee5c']
    assert '0x350,L"mpMute"' in fs['0x102f4fb10']
    assert 'param_1 + 0x358' in fs['0x102f50558'] and '"Mute"' in fs['0x102f50558']
    assert 'PTR_FUN_1067f9dd0' in fs['0x1026ebc1c']
    assert 'DAT_106e51ba8' in fs['0x1026eb7a8'] and 'DAT_106e51ba8' in fs['0x1026eb7b4']
    assert 'FUN_10242c75c()' in fs['0x102422efc'] and '1067b4860' in fs['0x10242c75c']
    assert 'FUN_10242cee8(param_1,param_2)' in fs['0x10242cb20']
    assert data['functions'][15]['record']['warnings'] and 'jumptable' in fs['0x10242cb20']
    assert '*param_2 + 0x328' in fs['0x10242cee8']
    assert 'local_48 = "RampOut";' in fs['0x10242cee8'] and 'if ((int)uVar2 == 0)' in fs['0x10242cee8']
    assert 'local_48 = "Out";' in fs['0x10242cee8']
    assert 'local_60 = 0x6574754d' in fs['0x10215eafc'] and 'PTR___invoke_1065411a0' in fs['0x10215eafc']
    assert 'DefaultUpdateStatesHandler' in fs['0x1024874ac']
    assert '(*(code *)*param_3)(param_3[1],param_1,4)' in fs['0x10155c8c0']
    assert '(*param_3)(param_4,param_1,uVar7)' in fs['0x1025c1ea8']
    assert '1067e1d18' in fs['0x1025c1ea8'] and '*plVar21 + 0x330' in fs['0x1025c1ea8']

def main():
    # Refuse unknown options before any packet/source reads.
    if sys.argv[1:] != ['--check']:
        print('Only --check is supported; no write/seal mode.', file=sys.stderr)
        return 1
    m = json.loads((P / 'manifest.json').read_text())
    assert set(m['payloads']) == {'README.md', 'check.py', 'records.json', 'routing.json', 'inputs.json'}
    assert {x.name for x in P.iterdir()} == set(m['payloads']) | {'manifest.json'}
    inp = json.loads((P / 'inputs.json').read_text())
    watched = [P / n for n in list(m['payloads']) + ['manifest.json']] + [path(n) for n in inp['files']]
    before = {str(p): pin(p) for p in watched}
    for n, v in m['payloads'].items(): assert pin(P / n) == v, n
    for n, v in inp['files'].items(): assert pin(path(n)) == v, n
    data = json.loads((P / 'records.json').read_text())
    route = json.loads((P / 'routing.json').read_text())
    # Only selected original lines are decoded as JSON data.
    parents = {n: path(n).read_bytes().splitlines() for n in
               {x['path'] for x in data['functions'] + data['initial_navigation_aliases']}}
    for x in data['functions'] + data['initial_navigation_aliases']:
        raw = parents[x['path']][x['line'] - 1]
        assert len(raw) == x['raw_line_bytes_excluding_terminator']
        assert hashlib.sha256(raw).hexdigest() == x['raw_sha256'] and json.loads(raw) == x['record']
        if 'code' in x['record']:
            code = x['record']['code'].encode()
            assert len(code) == x['record']['code_bytes']
            assert hashlib.sha256(code).hexdigest() == x['record']['code_sha256']
    assert len(data['initial_navigation_aliases']) == 5
    assert len(data['selection_membership']['Root']) == 23 and len(data['selection_membership']['Delay']) == 8
    # Reuse exactly three immutable A1 records; never execute/import their contents.
    for ref, index, entry in zip(data['reused_function_providers'], [0, 34, 44],
                                 ['0x10147fd68', '0x10319c4dc', '0x10150b1cc']):
        assert ref['pointer'] == f'/functions/{index}' and ref['entry'] == entry
        f = json.loads(path(ref['path']).read_text())['functions'][index]['record']
        assert f['entry'] == entry and f['code_sha256'] == ref['code_sha256']
        if index == 34:
            assert 'FUN_1026eb7a8()' in f['code'] and 'FUN_102422efc(&local_60)' in f['code']
        if index == 44: assert 'param_1[1] = param_2' in f['code']
    # Ordinary file-only Mach-O header/segment fields; read exactly five8-byte words.
    w = data['word_reads']; image = path(w['image']['path'])
    assert pin(image) == {k: w['image'][k] for k in ['bytes', 'sha256']}
    with image.open('rb') as f:
        header = f.read(32); assert header.hex() == w['image']['header']
        magic, cpu, _, _, ncmds, cmdbytes, _, _ = struct.unpack('<8I', header)
        assert magic == 0xfeedfacf and cpu == 0x100000c
        commands = f.read(cmdbytes); offset = 0; segments = []
        for _ in range(ncmds):
            cmd, size = struct.unpack_from('<II', commands, offset)
            assert size >= 8 and offset + size <= len(commands)
            if cmd == 0x19:
                name = commands[offset+8:offset+24].split(b'\0')[0].decode('ascii')
                va, vs, fo, fs = struct.unpack_from('<4Q', commands, offset+24)
                segments.append(dict(name=name, vmaddr=va, vmsize=vs, fileoff=fo, filesize=fs))
            offset += size
        assert offset == len(commands) and segments == w['segments']
        for read in w['reads']:
            va = int(read['vmaddr'], 16)
            matches = [s for s in segments if s['vmaddr'] <= va and va + 8 <= s['vmaddr'] + s['filesize']]
            assert len(matches) == 1; s = matches[0]
            assert read['segment'] == s['name'] and read['fileoff'] == s['fileoff'] + va - s['vmaddr']
            f.seek(read['fileoff']); assert f.read(8).hex() == read['raw']
    limited_invariants(data, route)
    variants = []
    for key, value in [('same_object_proven', True), ('wrapped_pointer_offset', 0x350)]:
        q = copy.deepcopy(route); q['object_domains'][key] = value; variants.append((data, q))
    for key, value in [('public_model_descriptor_join_closed', True), ('out_text_storage_pointer_is_name_proof', True),
                       ('application_case_grade', 'D'), ('public_expected', 'zero'), ('coverage_credit', 1)]:
        q = copy.deepcopy(route); q['limits'][key] = value; variants.append((data, q))
    q = copy.deepcopy(data); q['word_reads']['reads'][2]['slot'] = '0x178'; variants.append((q, route))
    q = copy.deepcopy(data); q['word_reads']['reads'][3]['value'] = '0x10216533c'; variants.append((q, route))
    q = copy.deepcopy(route); q['claims'][0]['source']['function_index'] = 0; variants.append((data, q))
    q = copy.deepcopy(route); q['factory_predicate'] = 'Equal bool metadata implies factory selection.'; variants.append((data, q))
    for d, q in variants:
        try: limited_invariants(d, q)
        except (AssertionError, KeyError, IndexError): pass
        else: raise AssertionError('unsafe mutation accepted')
    assert before == {str(p): pin(p) for p in watched}, 'watched bytes changed'
    print(json.dumps({'status': 'PASS', 'scope': 'finite research-data integrity; no runtime/app grade',
                      'functions': 29, 'initial_alias_rows': 5, 'claims': 12, 'word_reads': 5,
                      'word_bytes': 40, 'unsafe_variants_rejected': len(variants),
                      'watched_unchanged': len(before), 'new_requirements': 0, 'new_cases': 0}))
    return 0

if __name__ == '__main__':
    sys.exit(main())
