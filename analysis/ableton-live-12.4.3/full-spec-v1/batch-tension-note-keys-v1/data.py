"""Fixed Tension key inputs/protocol and unsigned stereo-bit summaries only."""
import collections
import copy
import hashlib
from pathlib import Path
import re
import struct

HERE = Path(__file__).resolve().parent
INHERITED = {36, 48, 60, 72, 84}
INDICES = [i for i in range(130) if i != 2]


def identity(path):
    p = Path(path); h = hashlib.sha256(); size = 0
    with p.open('rb') as f:
        for b in iter(lambda: f.read(1048576), b''):
            h.update(b); size += len(b)
    return {'path': str(p), 'resolved_path': str(p.resolve()), 'bytes': size, 'sha256': h.hexdigest()}


def validate(c):
    rows = c['rows']
    assert len(rows) == 128 and [r['note_key'] for r in rows] == list(range(128))
    assert len({r['id'] for r in rows}) == 128
    base = (HERE / 'baseline-template.script').read_bytes()
    assert identity(HERE / 'baseline-template.script') == c['baseline_template']
    lines = base.decode('ascii').splitlines()
    assert len(lines) == 137 and lines[:2] == ['create', 'rate 44100']
    assert lines[131:] == ['event 4096 0x90 60 100', 'event 26146 0x80 60 0', 'inflag 0', 'input zero', 'process 44100 512', 'destroy']
    params = [x.split() for x in lines[2:131]]
    assert [int(x[1]) for x in params] == INDICES and all(x[0] == 'param' for x in params)
    bits = [struct.pack('<f', float(x[2])).hex() for x in params]
    assert bits == c['parameter_f32_bits_le'] and c['parameter_indices'] == INDICES
    assert hashlib.sha256(bytes.fromhex(''.join(bits))).hexdigest() == c['parameter_vector_sha256'] == 'e00185698bafd4531b3562012e001afa759556d27405928685f07bf2f5c97eb8'
    fresh = 0
    for r in rows:
        k = r['note_key']; assert type(k) is int and r['id'] == f'TNK-{k:03d}'
        assert r['parameter_vector_sha256'] == c['parameter_vector_sha256']
        assert r['waveform_prediction'] is r['portable_expected'] is r['portable_comparator'] is r['candidate_grade'] is None
        assert r['events'] == [{'frame': f, 'status': s, 'key': k, 'velocity': v, 'packed16_le_hex': struct.pack('<qBBBB4x', f, s, k, v, 0).hex()} for f, s, v in [(4096, 0x90, 100), (26146, 0x80, 0)]]
        if k in INHERITED:
            assert r['disposition'] == 'inherited-no-replay' and r['fresh_receipt'] is None
            assert 'fresh_ordinal' not in r and 'script' not in r
        else:
            fresh += 1
            assert r['disposition'] == 'fresh-planned' and r['fresh_ordinal'] == fresh
            p = HERE / 'scripts' / (r['id'] + '.script')
            assert identity(p) == r['script']
            expected = base.replace(b'event 4096 0x90 60 100\n', f'event 4096 0x90 {k} 100\n'.encode()).replace(b'event 26146 0x80 60 0\n', f'event 26146 0x80 {k} 0\n'.encode())
            assert p.read_bytes() == expected
    assert fresh == c['limits']['children'] == 123
    assert c['environment'] == {'PATH': '/usr/bin:/bin', 'LANG': 'C.UTF-8', 'LC_ALL': 'C.UTF-8', 'TZ': 'UTC', 'XDEV_TIME': '0'}
    limits = c['limits']
    assert limits['selected_export_calls_each'] == 1 + 1 + 129 + 87 + 1 == 219
    assert limits['selected_export_calls_total'] == 26937 and limits['CalcA_total'] == 10701
    assert limits['new_stereo_bytes_each'] == 352800 and limits['new_stereo_bytes_total'] == 43394400
    assert limits['regular_file_bytes'] == 4194304 and limits['cpu_seconds'] == limits['timeout_seconds_each'] == 20


def protocol(log, row, c):
    assert not re.search(r'(?im)^(?:TRAP|FAULT|xdev:)', log)
    assert re.findall(r'^init (0x[0-9a-f]+)$', log, re.M) == ['0x260c0']
    assert re.findall(r'^slice offset=(\d+) size=(\d+)$', log, re.M) == [('16384', '501392')]
    assert re.findall(r'^create (\S+)$', log, re.M) == ['ok']
    assert re.findall(r'^destroy$', log, re.M) == ['destroy']
    assert re.findall(r'^cxx-failbits (\S+)$', log, re.M) == ['0']
    rate = re.findall(r'^rate 44100 ret=(-?\d+)$', log, re.M); assert len(rate) == 1
    params = re.findall(r'^param (\d+) (\S+)$', log, re.M)
    assert [int(i) for i, _ in params] == INDICES
    assert [struct.pack('<f', float(x)).hex() for _, x in params] == c['parameter_f32_bits_le']
    assert re.findall(r'^event (\d+) (0x[0-9a-f]+) (\d+) (\d+)$', log, re.M) == [('4096', '0x90', str(row['note_key']), '100'), ('26146', '0x80', str(row['note_key']), '0')]
    assert re.findall(r'^inflag (-?\d+)$', log, re.M) == ['0']
    assert re.findall(r'^input (\S+)$', log, re.M) == ['zero']
    assert not re.search(r'(?m)^(?:reset|transport|mxcsr|info)\b', log)
    process = re.findall(r'^process 44100 512 flags:(.*) blocks=87$', log, re.M)
    assert len(process) == 1 and re.fullmatch(r'(?: [1-9][0-9]*x\(ret=-?\d+,flag=-?\d+\))+', process[0])
    flags = [{'blocks': int(n), 'return': int(r), 'flag': int(f)} for n, r, f in re.findall(r'(\d+)x\(ret=(-?\d+),flag=(-?\d+)\)', process[0])]
    assert sum(x['blocks'] for x in flags) == 87 and all(x['return'] == 0 and x['flag'] in (0, 1) for x in flags)
    exports = re.findall(r'^export (\S+) (0x[0-9a-f]+)$', log, re.M)
    assert len(exports) == len(dict(exports)) == 7 and dict(exports) == c['approved_export_declarations']
    imports = re.findall(r'^import (trap|linux|data) (\S+) slots=(\d+)$', log, re.M)
    assert len(imports) == len({n for _, n, _ in imports}) == 142
    assert dict(collections.Counter(k for k, _, _ in imports)) == {'trap': 26, 'linux': 109, 'data': 7}
    declarations = [{'binding': k, 'symbol': n, 'slots': int(s)} for k, n, s in imports]
    assert declarations == c['approved_import_declarations']
    bindings = {n: k for k, n, _ in imports}
    used = re.findall(r'^used (\S+) ([1-9][0-9]*)$', log, re.M)
    assert used and len(dict(used)) == len(used) and all(bindings.get(n) == 'linux' for n, _ in used)
    return {'initializer_entries_logged': ['0x260c0'], 'selected_direct_exports_from_script_protocol': 219,
            'nested_original_calls': None, 'rate_return_logged': int(rate[0]), 'flags': flags,
            'exports_declared_not_all_invoked': dict(exports), 'import_declarations': declarations,
            'actual_used_code_import_counts': {n: int(v) for n, v in used}, 'cxx_failbits': 0}


def metrics(raw):
    # Same retained bit-summary class as approved Tension velocity captures: no float estimator.
    assert len(raw) > 0 and len(raw) % 8 == 0
    pairs = list(struct.iter_unpack('<II', raw))
    nonfinite = sum((v & 0x7f800000) == 0x7f800000 for pair in pairs for v in pair)
    return {'frames': len(pairs), 'all_finite': nonfinite == 0, 'nonfinite_scalar_count': nonfinite,
            'channels_byte_identical': all(l == r for l, r in pairs),
            'nonzero_sample_counts': [sum((pair[c] & 0x7fffffff) != 0 for pair in pairs) for c in (0, 1)],
            'negative_zero_sample_counts': [sum(pair[c] == 0x80000000 for pair in pairs) for c in (0, 1)]}


def selfchecks(c):
    validate(c); rejected = []
    for name, edit in [('missing key', lambda x: x['rows'].pop()),
                       ('duplicate key', lambda x: x['rows'][1].update(note_key=0)),
                       ('fractional key', lambda x: x['rows'][0].update(note_key=0.5)),
                       ('out of range', lambda x: x['rows'][0].update(note_key=128)),
                       ('replay inherited', lambda x: x['rows'][36].update(disposition='fresh-planned')),
                       ('invent prior', lambda x: x['rows'][0].update(waveform_prediction='tone')),
                       ('wrong packed offkey', lambda x: x['rows'][0]['events'][1].update(key=1)),
                       ('send excluded index2', lambda x: x['parameter_indices'].__setitem__(2, 2)),
                       ('wrong host word', lambda x: x['parameter_f32_bits_le'].__setitem__(0, '00000000')),
                       ('changed script pin', lambda x: x['rows'][0]['script'].update(sha256='0'*64)),
                       ('unselected libm override', lambda x: x['environment'].update(XDEV_LIBM_ULP='1')),
                       ('wrong export count', lambda x: x['limits'].update(selected_export_calls_total=123))]:
        bad = copy.deepcopy(c); edit(bad)
        try:
            validate(bad)
        except (AssertionError, KeyError):
            rejected.append(name)
        else:
            raise AssertionError('Accepted bad input ' + name)
    assert metrics(struct.pack('<II', 0, 0))['nonzero_sample_counts'] == [0, 0]
    assert metrics(struct.pack('<II', 0x80000000, 0))['negative_zero_sample_counts'] == [1, 0]
    assert not metrics(struct.pack('<II', 0, 1))['channels_byte_identical']
    assert not metrics(struct.pack('<II', 0, 0x7f800001))['all_finite']
    assert not metrics(struct.pack('<II', 0xff800000, 0))['all_finite']
    for raw in (b'', b'123', b'1234'):
        try:
            metrics(raw)
        except AssertionError:
            pass
        else:
            raise AssertionError('Accepted truncated frame')
    log = 'init 0x260c0\nslice offset=16384 size=501392\n'
    log += ''.join(f"import {r['binding']} {r['symbol']} slots={r['slots']}\n" for r in c['approved_import_declarations'])
    log += ''.join(f'export {n} {v}\n' for n, v in c['approved_export_declarations'].items())
    log += 'create ok\nrate 44100 ret=1\n'
    log += ''.join(f'param {i} {struct.unpack("<f", bytes.fromhex(h))[0]}\n' for i, h in zip(INDICES, c['parameter_f32_bits_le']))
    linux = next(r['symbol'] for r in c['approved_import_declarations'] if r['binding'] == 'linux')
    trap = next(r['symbol'] for r in c['approved_import_declarations'] if r['binding'] == 'trap')
    data = next(r['symbol'] for r in c['approved_import_declarations'] if r['binding'] == 'data')
    log += f'event 4096 0x90 0 100\nevent 26146 0x80 0 0\ninflag 0\ninput zero\nprocess 44100 512 flags: 87x(ret=0,flag=1) blocks=87\ndestroy\ncxx-failbits 0\nused {linux} 1\n'
    protocol(log, c['rows'][0], c); badlogs = {
        'wrong initializer': log.replace('init 0x260c0', 'init 0x314d0'),
        'wrong key': log.replace('event 4096 0x90 0 100', 'event 4096 0x90 1 100'),
        'offkey mismatch': log.replace('event 26146 0x80 0 0', 'event 26146 0x80 1 0'),
        'wrong phase': log.replace('event 4096', 'event 4400'),
        'nonzero process return': log.replace('ret=0,flag=1', 'ret=1,flag=1'),
        'invalid flag': log.replace('ret=0,flag=1', 'ret=0,flag=4'),
        'cxx failure': log.replace('cxx-failbits 0', 'cxx-failbits 1'),
        'used trap': log.replace(f'used {linux}', f'used {trap}'),
        'used data': log.replace(f'used {linux}', f'used {data}'),
        'new setup': log + 'reset\n', 'fault': log + 'FAULT sig=11\n'}
    protocol_controls = []
    for name, bad in badlogs.items():
        try:
            protocol(bad, c['rows'][0], c)
        except AssertionError:
            protocol_controls.append(name)
        else:
            raise AssertionError('Accepted bad protocol ' + name)
    return {'input_negative_controls': rejected, 'synthetic_protocol_negative_controls': protocol_controls,
            'unsigned_data_controls': ['positive zero retained', 'negative zero distinct', 'right subnormal retained', 'right signaling NaN nonfinite', 'left negative infinity nonfinite', 'empty/truncated frame rejected']}
