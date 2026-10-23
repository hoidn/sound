"""Read-only finite retained-data checks; never imports/calls original code."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
from copy import deepcopy
import json
import re
import struct
import sys

D = Path(__file__).resolve().parent
load = lambda p: json.loads(p.read_text())


def pin(p):
    h = sha256()
    n = 0
    with p.open('rb') as f:
        for b in iter(lambda: f.read(1048576), b''):
            h.update(b)
            n += len(b)
    return dict(bytes=n, sha256=h.hexdigest())


def pointer(v, s):
    assert s.startswith('/')
    for k in s[1:].split('/'):
        k = k.replace('~1', '/').replace('~0', '~')
        v = v[int(k)] if isinstance(v, list) else v[k]
    return v


def signed(v, bits):
    return v - (1 << bits) if v & (1 << (bits - 1)) else v


def guards(r, a):
    fs = r['functions']
    assert len(fs) == len({f['id'] for f in fs}) == 67
    assert Counter(f['read_scope'] for f in fs) == {
        'full-body': 56, 'incidental-full-body-unassigned': 2,
        'metadata-only-body-not-read': 9}
    for f in fs:
        assert f['record']['entry'] == f['id']
        if f['read_scope'].startswith('metadata'):
            assert 'code' not in f['record']
        else:
            b = f['record']['code'].encode()
            assert len(b) == f['record']['code_bytes']
            assert sha256(b).hexdigest() == f['record']['code_sha256']
    assert [len(r['index_records'][k]) for k in ['aliases', 'calls', 'indirect']] == [67, 84, 8]
    assert len(a['claims']) == 8 and len(a['case_routes']) == 41
    for c in a['claims']:
        assert c['observable_expected'] is c['observable_comparison'] is c['actual_expected'] is c['actual_comparison'] is None
        assert c['target'] == 'U' and c['executed'] is False and c['new_normative_credit'] == 0
        for f in c['function_refs']:
            assert f['catalog'] == 'records.json'
            assert pointer(r, f['pointer'])['id'] == f['id']
    cases = r['owner_profile']['cases']
    assert len(cases) == len({c['id'] for c in cases}) == 41
    assert Counter(c['provenance'] for c in cases) == dict(D12=26, Dpkg=3, U=12)
    assert [c['id'] for c in a['case_routes']] == [c['id'] for c in cases]
    for route, old in zip(a['case_routes'], cases):
        assert pointer(r, route['retained_record_pointer']) == old
        assert pointer({'profiles': {'utility': r['owner_profile']}}, route['provider_pointer']) == old
        assert route['id'] == old['id'] and route['original_provenance'] == old['provenance']
        assert route['original_target_grade'] == old['target_grade']
        assert route['next_path'] == a['route_definitions'][route['route']]
        assert route['grade_in_this_packet'] is route['actual_expected'] is route['actual_comparison'] is None
        assert route['application_target'] == 'U' and route['executed'] is route['no_route_established'] is False
    assert [c['id'] for c in a['case_routes'] if c['route'] == 'FILES'] == ['DUT-023', 'DUT-024', 'DUT-025']
    dep = a['depth_status']
    assert dep['new_required_observable_outcomes_graded'] == dep['no_route_findings'] == dep['complete_profiles'] == dep['reviewed_family_contracts_added'] == 0
    assert dep['carried_historical_file_only_scenarios'] == 3 and dep['application_scenarios_still_U_with_named_next_path'] == 38
    assert dep['atomic_required_outcome_denominator_established'] is False and dep['scenario_denominator'] == 41
    assert a['source_execution'] is False
    assert 'NOT no-route' in a['conclusion']
    assert 'application UI/storage message route' in a['claims'][2]['assessment']
    assert 'conditional' in a['claims'][2]['assessment']
    assert 'NOT initialized runtime expected state' in a['claims'][5]['assessment']
    assert 'metadata-only' in a['claims'][6]['assessment']
    assert a['byte_read_scope'] == dict(reads=9, bytes=888, source_hash_verified=True,
        bounded_instruction_fields_only=True, new_execution=False,
        constant_values_are_runtime_expectations=False)
    br = r['byte_reads']
    assert len(br['reads']) == 9 and sum(q['length'] for q in br['reads']) == 888
    reads = {q['address']: q for q in br['reads']}
    assert len(reads) == 9
    for q in br['reads']:
        b = bytes.fromhex(q['raw_hex'])
        assert len(b) == q['length'] and sha256(b).hexdigest() == q['sha256']
        addr = int(q['address'], 16)
        seg = next(s for s in br['segments'] if int(s['vmaddr'], 16) <= addr and addr + len(b) <= int(s['vmaddr'], 16) + s['vmsize'])
        assert q['segment'] == seg['name']
        assert q['file_offset'] == seg['fileoff'] + addr - int(seg['vmaddr'], 16)
        assert q['file_offset'] + len(b) <= seg['fileoff'] + seg['filesize']
    assert reads['0x106541200']['u64_le'] == ['0x1021658b0']
    assert reads['0x10584cbc0']['float32_le'] == [1.0, 0.0, 0.0, 0.0]
    assert reads['0x1054e91a8']['u64_le'] == ['0x1']
    assert reads['0x1059cd280']['raw_hex'] == 'e104b53ff9ea4f33'
    assert reads['0x106dd34b8']['raw_hex'] == '00' * 16
    fields = br['instruction_operand_checks']
    assert fields['kernel_load'] == dict(word='0x39433c08', rt=8, rn=0, unsigned_byte_offset=207)
    assert fields['kernel_zero_registers'] == dict(words=['0x2f00e400', '0x2f00e401'], vector_registers=['D0', 'D1'], value_bits=0)
    assert fields['kernel_flag_branch'] == dict(word='0x370016c8', rt=8, tested_bit=0, target='0x1047bda74', target_word='0xd65f03c0')
    assert fields['wrapper_call'] == dict(word='0x94995fac', site='0x1021658e0', target='0x1047bd790')
    assert fields['wrapper_store_pair'] == dict(word='0x2d080660', rt=0, rt2=1, rn=19, byte_offset=64, register_width_bits=32)
    kw = struct.unpack('<186I', bytes.fromhex(reads['0x1047bd790']['raw_hex']))
    assert kw[:4] == (0x39433c08, 0x2f00e400, 0x2f00e401, 0x370016c8)
    # Exact A64 operand fields only: LDRB unsigned immediate; TBNZ; BL; STP S pair.
    w = kw[0]
    assert w & 0xffc00000 == 0x39400000 and w & 31 == 8 and (w >> 5) & 31 == 0 and (w >> 10) & 4095 == 207
    w = kw[3]
    assert w & 0x7f000000 == 0x37000000 and w & 31 == 8
    assert ((w >> 19) & 31) + ((w >> 31) << 5) == 0
    target = 0x1047bd790 + 12 + signed((w >> 5) & 16383, 14) * 4
    assert target == 0x1047bda74 and kw[(target - 0x1047bd790) // 4] == 0xd65f03c0
    ww = struct.unpack('<18I', bytes.fromhex(reads['0x1021658b0']['raw_hex']))
    assert ww[-1] == 0xd65f03c0
    w = ww[12]
    assert w == 0x94995fac and 0x1021658b0 + 48 + signed(w & 0x3ffffff, 26) * 4 == 0x1047bd790
    w = ww[13]
    assert w == 0x2d080660 and w & 0xffc00000 == 0x2d000000
    assert (w & 31, (w >> 10) & 31, (w >> 5) & 31, signed((w >> 15) & 127, 7) * 4) == (0, 1, 19, 64)
    assert not [v for v in r['index_records']['calls'] if v['record']['caller'] == '0x1047bd790']
    assert not [v for v in r['index_records']['indirect'] if v['record']['function'] == '0x1047bd790']


def main():
    assert sys.dont_write_bytecode and sys.argv[1:] == ['--check'], 'Read-only --check only; no writer/native/original execution'
    inp = load(D / 'inputs.json')
    watched = {Path(p) for p in inp['files']} | {p for p in D.iterdir() if p.is_file()}
    before = {str(p): pin(p) for p in watched}
    assert len(inp['files']) == 22
    for p, want in inp['files'].items():
        assert not p.startswith(str(D.parents[3] / 'wiki')) and pin(Path(p)) == want
    r, a = load(D / 'records.json'), load(D / 'assessment.json')
    guards(r, a)
    corpus = Path('/var/tmp/sound-analysis/corpus')
    for p in [corpus / 'decomp/run.json', corpus / 'indexes/manifest.json']:
        assert load(p)['executable_sha256'] == inp['target_identity']
    allf = []
    for ch, ns in inp['selected_full_lines'].items():
        p = corpus / 'decomp/chunks' / f'chunk-{ch}.jsonl'
        for n, raw in enumerate(p.open('rb'), 1):
            mode = ('full-body' if n in ns else
                'incidental-full-body-unassigned' if n in inp['incidental_full_lines'].get(ch, []) else
                'metadata-only-body-not-read' if n in inp['metadata_only_lines'].get(ch, []) else None)
            if mode:
                value = json.loads(raw)
                if mode.startswith('metadata'):
                    value.pop('code')
                allf.append(dict(id=value['entry'], parent=str(p), line=n,
                    raw_line_sha256=sha256(raw).hexdigest(), read_scope=mode, record=value))
    assert allf == r['functions']
    allids = {x['id'] for x in allf}
    full = {x['id'] for x in allf if x['read_scope'] == 'full-body'}
    for name, key, ids in [('aliases', 'entry', allids), ('calls', 'caller', full), ('indirect', 'function', full)]:
        p = corpus / 'indexes' / f'{name}.jsonl'
        pat = re.compile(('"' + key + '":"(0x[0-9a-f]+)"').encode())
        rows = []
        for n, raw in enumerate(p.open('rb'), 1):
            m = pat.search(raw)
            if m and m[1].decode() in ids:
                rows.append(dict(parent=str(p), line=n, raw_line_sha256=sha256(raw).hexdigest(), record=json.loads(raw)))
        assert rows == r['index_records'][name]
    assert pointer(load(Path(inp['owner_provider'])), inp['owner_pointer']) == r['owner_profile']
    binary = Path(r['byte_reads']['source'])
    assert pin(binary)['sha256'] == inp['target_identity']
    with binary.open('rb') as f:
        head = struct.unpack('<8I', f.read(32))
        assert list(head) == r['byte_reads']['header_fields'] and head[:2] == (0xfeedfacf, 0x100000c)
        commands = f.read(head[5])
        segments, off = [], 0
        for _ in range(head[4]):
            cmd, size = struct.unpack_from('<II', commands, off)
            assert size >= 8 and off + size <= len(commands)
            if cmd == 0x19:
                name = commands[off+8:off+24].rstrip(b'\0').decode()
                vm, vs, fo, fs = struct.unpack_from('<4Q', commands, off+24)
                segments.append(dict(name=name, vmaddr=hex(vm), vmsize=vs, fileoff=fo, filesize=fs))
            off += size
        assert off == head[5] and segments == r['byte_reads']['segments']
        for q in r['byte_reads']['reads']:
            f.seek(q['file_offset'])
            b = f.read(q['length'])
            assert b.hex() == q['raw_hex']
            if 'u64_le' in q:
                assert q['u64_le'] == [hex(v) for v in struct.unpack('<' + 'Q' * (len(b)//8), b)]
                assert q['float32_le'] == list(struct.unpack('<' + 'f' * (len(b)//4), b))
            else:
                assert q['instruction_words_le'] == [hex(v) for v in struct.unpack('<' + 'I' * (len(b)//4), b)]
    rejected = []
    for mutation in ['omit-kernel', 'promote-unread-body', 'wrong-function-pointer', 'joint-wrong-case-index', 'actual-grade', 'promote-file-grade', 'no-route', 'runtime-constant', 'unconditional-mute', 'raw-byte', 'joint-mapping', 'lost-UI-frontier']:
        rr, aa = deepcopy(r), deepcopy(a)
        if mutation == 'omit-kernel': rr['functions'].pop()
        elif mutation == 'promote-unread-body': next(f for f in rr['functions'] if f['read_scope'].startswith('metadata'))['read_scope'] = 'full-body'
        elif mutation == 'wrong-function-pointer': aa['claims'][0]['function_refs'][0]['pointer'] = '/functions/0'
        elif mutation == 'joint-wrong-case-index':
            aa['case_routes'][1]['provider_pointer'] = '/profiles/utility/cases/0'
            aa['case_routes'][1]['retained_record_pointer'] = '/owner_profile/cases/0'
        elif mutation == 'actual-grade': aa['case_routes'][0]['actual_expected'] = 'pass'
        elif mutation == 'promote-file-grade': aa['case_routes'][22]['application_target'] = 'Dpkg'
        elif mutation == 'no-route': aa['depth_status']['no_route_findings'] = 38
        elif mutation == 'runtime-constant': aa['byte_read_scope']['constant_values_are_runtime_expectations'] = True
        elif mutation == 'unconditional-mute': aa['claims'][2]['assessment'] = 'Mute always proves stereo silence.'
        elif mutation == 'raw-byte': rr['byte_reads']['reads'][0]['raw_hex'] = '00' * 16
        elif mutation == 'joint-mapping': rr['byte_reads']['reads'][0]['file_offset'] += 4
        else: aa['claims'][2]['assessment'] = aa['claims'][2]['assessment'].replace('application UI/storage message route', 'already settled route')
        try: guards(rr, aa)
        except (AssertionError, KeyError, IndexError, ValueError, TypeError): rejected.append(mutation)
        else: raise AssertionError('Unsafe fixture accepted: ' + mutation)
    manifest = D / 'manifest.json'
    if manifest.exists():
        m = load(manifest)
        assert set(m['payloads']) == {p.name for p in D.iterdir() if p.is_file() and p != manifest}
        assert m['immutable_inputs'] == inp['files']
        for n, expected in m['payloads'].items(): assert pin(D/n) == expected
    for p in D.iterdir():
        if p.is_file():
            b = p.read_bytes()
            assert b.endswith(b'\n') and b'\0' not in b and all(v.rstrip(b' \t') == v for v in b.splitlines())
    for dest in re.findall(r'\]\(([^)]+)\)', (D/'README.md').read_text()):
        assert (D/dest).exists() or dest == 'manifest.json' and not manifest.exists()
    assert before == {str(p): pin(p) for p in watched}
    print(json.dumps(dict(status='pass', sealed=manifest.exists(), full_selected=56,
        incidental_full_unassigned=2, omitted_legacy_bodies=9, direct_edges=84,
        unresolved_computed_sites=8, aliases=67, case_routes=41,
        bounded_byte_reads=9, bounded_bytes=888, pins=22,
        negative_fixtures=rejected, unchanged_watch=len(watched), writes=False,
        new_observable_grades=0, no_route_findings=0, complete_profiles=0), indent=2))


if __name__ == '__main__':
    main()
