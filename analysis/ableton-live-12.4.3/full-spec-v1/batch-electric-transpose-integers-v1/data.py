"""Owned fixed-class/input/protocol/stereo checks; no original entrypoint."""
import collections
import copy
import hashlib
import math
from pathlib import Path
import re
import struct

HERE = Path(__file__).resolve().parent
INHERITED = {0, 12, 24}


def identity(path):
    path = Path(path)
    h = hashlib.sha256(); size = 0
    with path.open('rb') as f:
        for b in iter(lambda: f.read(1048576), b''):
            h.update(b); size += len(b)
    return {'path': str(path), 'resolved_path': str(path.resolve()), 'bytes': size, 'sha256': h.hexdigest()}


def validate(config):
    rows = config['rows']
    assert len(rows) == 25 and [r['transpose_integer'] for r in rows] == list(range(25))
    assert len({r['id'] for r in rows}) == 25
    base = (HERE / 'baseline-template.script').read_bytes()
    assert identity(HERE / 'baseline-template.script') == config['baseline_template']
    lines = base.decode('ascii').splitlines()
    assert len(lines) == 42 and lines[:2] == ['create', 'rate 44100']
    assert lines[35:] == ['event 11264 0x90 60 100', 'event 33314 0x80 60 0', 'inflag 0', 'input zero', 'process 11264 512', 'process 44100 512', 'destroy']
    params = [line.split() for line in lines[2:35]]
    assert [int(r[1]) for r in params] == list(range(33)) and all(r[0] == 'param' for r in params)
    bits = [struct.pack('<f', float(r[2])).hex() for r in params]
    assert bits == config['baseline_parameter_f32_bits_le']
    assert bits[2] == '116d343f' and bits[30] == '00004041' and bits[32] == '00004042'
    assert hashlib.sha256(bytes.fromhex(''.join(bits))).hexdigest() == config['baseline_parameter_vector_sha256']
    fresh = 0
    for row in rows:
        n = row['transpose_integer']
        assert type(n) is int and row['id'] == f'ETI-{n:02d}'
        assert row['waveform_prediction'] is row['portable_comparator'] is None
        expected_bits = bits.copy(); expected_bits[30] = struct.pack('<f', n).hex()
        assert row['parameter_f32_bits_le'] == expected_bits
        assert row['parameter_vector_sha256'] == hashlib.sha256(bytes.fromhex(''.join(expected_bits))).hexdigest()
        if n in INHERITED:
            assert row['disposition'] == 'inherited-no-replay' and row['fresh_receipt'] is None
            assert 'script' not in row and 'fresh_ordinal' not in row
        else:
            fresh += 1
            assert row['disposition'] == 'fresh-planned' and row['fresh_ordinal'] == fresh
            path = HERE / 'scripts' / (row['id'] + '.script')
            assert identity(path) == row['script']
            assert path.read_bytes() == base.replace(b'param 30 12.0\n', f'param 30 {float(n)!r}\n'.encode())
    assert fresh == 22
    assert config['environment'] == {'PATH': '/usr/bin:/bin', 'LC_ALL': 'C', 'LANG': 'C', 'TZ': 'UTC', 'XDEV_TIME': '0'}
    limits = config['limits']
    assert limits['children'] == 22 and limits['selected_export_calls_each'] == 1 + 1 + 33 + 22 + 87 + 1 == 145
    assert limits['selected_export_calls_total'] == 3190 and limits['CalcA_total'] == 2398
    assert limits['new_stereo_bytes_each'] == 442912 and limits['new_stereo_bytes_total'] == 9744064
    assert limits['regular_file_bytes'] == 4194304 and limits['timeout_seconds_each'] == limits['cpu_seconds'] == 20


def protocol(log, row, config):
    assert not re.search(r'(?im)^(?:TRAP|FAULT|xdev:)', log)
    # The approved Electric capture begins with its slice line, without initializer entries.
    initializers = re.findall(r'^init (0x[0-9a-f]+)$', log, re.M)
    assert initializers == [] and log.startswith('slice offset=16384 size=267648\n')
    assert re.findall(r'^slice offset=(\d+) size=(\d+)$', log, re.M) == [('16384', '267648')]
    assert re.findall(r'^create (\S+)$', log, re.M) == ['ok']
    assert re.findall(r'^destroy$', log, re.M) == ['destroy']
    assert re.findall(r'^cxx-failbits (\S+)$', log, re.M) == ['0']
    rate = re.findall(r'^rate 44100 ret=(-?\d+)$', log, re.M)
    assert len(rate) == 1
    params = re.findall(r'^param (\d+) (\S+)$', log, re.M)
    assert [int(i) for i, _ in params] == list(range(33))
    assert [struct.pack('<f', float(x)).hex() for _, x in params] == row['parameter_f32_bits_le']
    assert re.findall(r'^event (\d+) (0x[0-9a-f]+) (\d+) (\d+)$', log, re.M) == [('11264', '0x90', '60', '100'), ('33314', '0x80', '60', '0')]
    assert re.findall(r'^inflag (-?\d+)$', log, re.M) == ['0']
    assert re.findall(r'^input (\S+)$', log, re.M) == ['zero']
    assert not re.search(r'(?m)^(?:reset|transport|mxcsr|info)\b', log)
    processes = re.findall(r'^process (\d+) (\d+) flags:(.*) blocks=(\d+)$', log, re.M)
    assert [(int(n), int(b), int(k)) for n, b, _, k in processes] == [(11264, 512, 22), (44100, 512, 87)]
    flags = []
    for n, block, sequence, count in processes:
        assert re.fullmatch(r'(?: [1-9][0-9]*x\(ret=-?\d+,flag=-?\d+\))+', sequence)
        runs = [{'blocks': int(k), 'return': int(ret), 'flag': int(flag)} for k, ret, flag in re.findall(r'(\d+)x\(ret=(-?\d+),flag=(-?\d+)\)', sequence)]
        assert sum(x['blocks'] for x in runs) == int(count)
        assert all(x['return'] == 0 and x['flag'] in (0, 1) for x in runs)
        flags.append({'frames': int(n), 'block': int(block), 'runs': runs})
    exports = re.findall(r'^export (\S+) (0x[0-9a-f]+)$', log, re.M)
    assert len(exports) == 7 and len(dict(exports)) == 7 and dict(exports) == config['approved_export_declarations']
    imports = re.findall(r'^import (trap|linux|data) (\S+) slots=(\d+)$', log, re.M)
    assert len(imports) == 133 and len({x[1] for x in imports}) == 133
    assert dict(collections.Counter(x[0] for x in imports)) == {'trap': 26, 'linux': 100, 'data': 7}
    bindings = {name: kind for kind, name, _ in imports}
    used = re.findall(r'^used (\S+) ([1-9][0-9]*)$', log, re.M)
    assert len(dict(used)) == len(used) == 64
    assert set(name for name, _ in used) <= set(config['approved_allowed_used_symbols'])
    assert all(bindings.get(name) == 'linux' for name, _ in used), 'Unbound/non-Linux used import'
    return {'initializer_entries_logged': initializers, 'selected_direct_exports_from_script_protocol': 145,
            'nested_original_calls': None, 'rate_return_logged': int(rate[0]), 'flags': flags,
            'exports_declared_not_all_invoked': dict(exports),
            'import_declarations': [{'binding': k, 'symbol': n, 'slots': int(s)} for k, n, s in imports],
            'actual_used_code_import_counts': {k: int(v) for k, v in used}, 'cxx_failbits': 0}


def metrics(raw):
    assert len(raw) > 0 and len(raw) % 8 == 0
    frames = list(struct.iter_unpack('<ff', raw))
    finite = all(math.isfinite(v) for pair in frames for v in pair)
    nonzero = [i for i, pair in enumerate(frames) if any(v != 0 for v in pair)]
    return {'frames': len(frames), 'all_finite': finite,
            'nonfinite_scalar_count': sum(not math.isfinite(v) for pair in frames for v in pair),
            'channels_byte_identical': all(raw[i:i + 4] == raw[i + 4:i + 8] for i in range(0, len(raw), 8)),
            'nonzero_frames': len(nonzero), 'first_nonzero_frame': nonzero[0] if nonzero else None,
            'last_nonzero_frame': nonzero[-1] if nonzero else None,
            'per_channel': [{'peak_abs': max(abs(pair[c]) for pair in frames),
                             'rms': math.sqrt(math.fsum(pair[c] * pair[c] for pair in frames) / len(frames)),
                             'mean': math.fsum(pair[c] for pair in frames) / len(frames)} for c in (0, 1)] if finite else None}


def audio(raw):
    assert len(raw) == 442912
    return {'whole': metrics(raw), 'warmup': metrics(raw[:90112]), 'render': metrics(raw[90112:]),
            'render_stereo_sha256': hashlib.sha256(raw[90112:]).hexdigest()}


def selfchecks(config):
    validate(config)
    rejected = []
    for name, mutate in [('omit integer', lambda c: c['rows'].pop()),
                         ('duplicate integer', lambda c: c['rows'][1].update(transpose_integer=0)),
                         ('fractional integer', lambda c: c['rows'][1].update(transpose_integer=1.5)),
                         ('out of domain', lambda c: c['rows'][1].update(transpose_integer=25)),
                         ('replay inherited control', lambda c: c['rows'][0].update(disposition='fresh-planned')),
                         ('invent waveform', lambda c: c['rows'][1].update(waveform_prediction='sine')),
                         ('change volume bits', lambda c: c['baseline_parameter_f32_bits_le'].__setitem__(2, '0000003f')),
                         ('wrong input identity', lambda c: c['rows'][1]['script'].update(sha256='0' * 64)),
                         ('ambient override', lambda c: c['environment'].update(LD_PRELOAD='x')),
                         ('wrong export count', lambda c: c['limits'].update(selected_export_calls_total=22))]:
        bad = copy.deepcopy(config); mutate(bad)
        try:
            validate(bad)
        except (AssertionError, KeyError):
            rejected.append(name)
        else:
            raise AssertionError('Bad input accepted: ' + name)
    zero = struct.pack('<ff', 0, 0)
    assert metrics(zero)['first_nonzero_frame'] is None
    assert not metrics(struct.pack('<ff', 0, 1))['channels_byte_identical']
    assert not metrics(struct.pack('<ff', 0, float('nan')))['all_finite']
    assert not metrics(struct.pack('<ff', float('inf'), 0))['all_finite']
    assert metrics(struct.pack('<ff', -0.0, 0.0))['nonzero_frames'] == 0
    assert not metrics(struct.pack('<ff', -0.0, 0.0))['channels_byte_identical']
    for bad in (b'', b'123', b'1234'):
        try:
            metrics(bad)
        except AssertionError:
            pass
        else:
            raise AssertionError('Truncated frame accepted')
    row = config['rows'][1]
    # Synthetic symbols are supplied only to this owned-data positive/negative test.
    synthetic = copy.deepcopy(config)
    synthetic['approved_allowed_used_symbols'] = [f'synth_linux_{i}' for i in range(64)]
    log = 'slice offset=16384 size=267648\n'
    log += ''.join(f'import {kind} synth_{kind}_{i} slots=1\n' for kind, count in [('trap', 26), ('linux', 100), ('data', 7)] for i in range(count))
    log += ''.join(f'export {name} {value}\n' for name, value in config['approved_export_declarations'].items())
    log += 'create ok\nrate 44100 ret=0\n'
    log += ''.join(f'param {i} {struct.unpack("<f", bytes.fromhex(h))[0]}\n' for i, h in enumerate(row['parameter_f32_bits_le']))
    log += 'event 11264 0x90 60 100\nevent 33314 0x80 60 0\ninflag 0\ninput zero\nprocess 11264 512 flags: 22x(ret=0,flag=0) blocks=22\nprocess 44100 512 flags: 87x(ret=0,flag=1) blocks=87\ndestroy\ncxx-failbits 0\n'
    log += ''.join(f'used synth_linux_{i} 1\n' for i in range(64))
    protocol(log, row, synthetic)
    badlogs = {'unexpected initializer': 'init 0x1\n' + log,
               'wrong transpose': log.replace('param 30 1.0', 'param 30 2.0'),
               'wrong warmup coordinate': log.replace('event 11264', 'event 0'),
               'missing setter': log.replace('param 0 30.0\n', ''),
               'wrong return': log.replace('ret=0,flag=1', 'ret=1,flag=1'),
               'wrong flag': log.replace('ret=0,flag=1', 'ret=0,flag=4'),
               'missing warmup process': log.replace('process 11264 512 flags: 22x(ret=0,flag=0) blocks=22\n', ''),
               'cxx failure': log.replace('cxx-failbits 0', 'cxx-failbits 1'),
               'trap invoked': log.replace('used synth_linux_0 ', 'used synth_trap_0 '),
               'data binding invoked': log.replace('used synth_linux_0 ', 'used synth_data_0 '),
               'new setup operation': log + 'reset\n', 'fault text': log + 'FAULT sig=11\n'}
    protocol_rejected = []
    for name, bad in badlogs.items():
        try:
            protocol(bad, row, synthetic)
        except AssertionError:
            protocol_rejected.append(name)
        else:
            raise AssertionError('Bad protocol accepted: ' + name)
    return {'input_negative_controls': rejected, 'synthetic_protocol_negative_controls': protocol_rejected,
            'descriptive_data_controls': ['zero NULL first/last', 'right-only signal', 'right NaN', 'left infinity', 'signed-zero identity vs numeric zero', 'truncated geometry']}
