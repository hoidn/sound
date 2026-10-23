"""Owned input/protocol/retained-statistics functions; no original entrypoint."""
import collections
import copy
import hashlib
import math
from pathlib import Path
import re
import struct

HERE = Path(__file__).resolve().parent


def identity(path):
    path = Path(path)
    h = hashlib.sha256()
    size = 0
    with path.open('rb') as f:
        for b in iter(lambda: f.read(1048576), b''):
            h.update(b)
            size += len(b)
    return {'path': str(path), 'resolved_path': str(path.resolve()), 'bytes': size, 'sha256': h.hexdigest()}


def validate(config):
    rows = config['rows']
    assert len(rows) == 128 and [r['release_velocity_byte'] for r in rows] == list(range(128))
    assert len({r['id'] for r in rows}) == 128
    base = (HERE / 'baseline-template.script').read_bytes()
    assert identity(HERE / 'baseline-template.script') == config['baseline_template']
    lines = base.decode('ascii').splitlines()
    assert len(lines) == 211 and lines[:2] == ['create', 'rate 44100']
    assert lines[-6:] == ['event 4400 0x90 60 100', 'event 35270 0x80 60 64', 'inflag 0', 'input zero', 'process 44100 512', 'destroy']
    params = [line.split() for line in lines[2:205]]
    assert [int(r[1]) for r in params] == list(range(203)) and all(r[0] == 'param' for r in params)
    bits = [struct.pack('<f', float(r[2])).hex() for r in params]
    assert bits == config['parameter_f32_bits_le'] and bits[99] == '0000803f'
    assert hashlib.sha256(bytes.fromhex(''.join(bits))).hexdigest() == config['parameter_vector_sha256']
    fresh = 0
    for row in rows:
        release = row['release_velocity_byte']
        assert type(release) is int and row['id'] == f'ARV-{release:03d}'
        assert row['waveform_prediction'] is row['portable_comparator'] is row['portable_expected'] is row['candidate_grade'] is None
        assert row['parameter_vector_sha256'] == config['parameter_vector_sha256']
        assert row['events'] == [{'frame': f, 'status': status, 'key': 60, 'velocity': v, 'packed16_le_hex': struct.pack('<qBBBB4x', f, status, 60, v, 0).hex()} for f, status, v in [(4400, 0x90, 100), (35270, 0x80, release)]]
        if release == 64:
            assert row['disposition'] == 'inherited-no-replay' and row['fresh_receipt'] is None
            assert 'script' not in row and 'fresh_ordinal' not in row
        else:
            fresh += 1
            assert row['disposition'] == 'fresh-planned' and row['fresh_ordinal'] == fresh
            path = HERE / 'scripts' / (row['id'] + '.script')
            assert identity(path) == row['script']
            expected = base.replace(b'event 35270 0x80 60 64\n', f'event 35270 0x80 60 {release}\n'.encode())
            assert path.read_bytes() == expected
    assert fresh == 127
    assert config['environment'] == {'PATH': '/usr/bin:/bin', 'LC_ALL': 'C', 'LANG': 'C', 'TZ': 'UTC', 'XDEV_TIME': '0'}
    limits = config['limits']
    assert limits['children'] == 127 and limits['selected_export_calls_each'] == 1 + 1 + 203 + 87 + 1 == 293
    assert limits['selected_export_calls_total'] == 37211 and limits['CalcA_total'] == 11049
    assert limits['new_stereo_bytes_each'] == 352800 and limits['new_stereo_bytes_total'] == 44805600
    assert limits['regular_file_bytes'] == 4194304 and limits['timeout_seconds_each'] == limits['cpu_seconds'] == 20


def protocol(log, row, config):
    assert not re.search(r'(?im)^(?:TRAP|FAULT|xdev:)', log)
    assert re.findall(r'^init (0x[0-9a-f]+)$', log, re.M) == ['0x314d0']
    assert re.findall(r'^slice offset=(\d+) size=(\d+)$', log, re.M) == [('16384', '500880')]
    assert re.findall(r'^create (\S+)$', log, re.M) == ['ok']
    assert re.findall(r'^destroy$', log, re.M) == ['destroy']
    assert re.findall(r'^cxx-failbits (\S+)$', log, re.M) == ['0']
    rate = re.findall(r'^rate 44100 ret=(-?\d+)$', log, re.M)
    assert len(rate) == 1
    params = re.findall(r'^param (\d+) (\S+)$', log, re.M)
    assert [int(i) for i, _ in params] == list(range(203))
    assert [struct.pack('<f', float(x)).hex() for _, x in params] == config['parameter_f32_bits_le']
    assert re.findall(r'^event (\d+) (0x[0-9a-f]+) (\d+) (\d+)$', log, re.M) == [('4400', '0x90', '60', '100'), ('35270', '0x80', '60', str(row['release_velocity_byte']))]
    assert re.findall(r'^inflag (-?\d+)$', log, re.M) == ['0']
    assert re.findall(r'^input (\S+)$', log, re.M) == ['zero']
    assert not re.search(r'(?m)^(?:reset|transport|mxcsr|info)\b', log)
    process = re.findall(r'^process 44100 512 flags:(.*) blocks=87$', log, re.M)
    assert len(process) == 1
    assert re.fullmatch(r'(?: [1-9][0-9]*x\(ret=-?\d+,flag=-?\d+\))+', process[0])
    flags = [{'blocks': int(n), 'return': int(ret), 'flag': int(flag)} for n, ret, flag in re.findall(r'(\d+)x\(ret=(-?\d+),flag=(-?\d+)\)', process[0])]
    assert flags and sum(x['blocks'] for x in flags) == 87
    assert all(x['return'] == 0 and x['flag'] in (0, 1) for x in flags)
    exports = re.findall(r'^export (\S+) (0x[0-9a-f]+)$', log, re.M)
    assert len(exports) == 7 and len(dict(exports)) == 7
    assert set(dict(exports)) == {'_CreateInstanceU', '_DestroyInstanceU', '_SetSampleRateU', '_GetPlugInfoU', '_CalcA', '_SetParameterA', '_ResetA'}
    imports = re.findall(r'^import (trap|linux|data) (\S+) slots=(\d+)$', log, re.M)
    assert len(imports) == 132 and len({x[1] for x in imports}) == 132
    assert dict(collections.Counter(x[0] for x in imports)) == {'trap': 26, 'linux': 99, 'data': 7}
    bindings = {name: kind for kind, name, _ in imports}
    used = re.findall(r'^used (\S+) ([1-9][0-9]*)$', log, re.M)
    assert len(dict(used)) == len(used)
    assert all(bindings.get(name) == 'linux' for name, _ in used), 'Unbound/non-Linux used import'
    return {'initializer_entries_logged': ['0x314d0'], 'selected_direct_exports_from_script_protocol': 293,
            'nested_original_calls': None, 'rate_return_logged': int(rate[0]), 'flags': flags,
            'exports_declared_not_all_invoked': dict(exports),
            'import_declarations': [{'binding': k, 'symbol': n, 'slots': int(s)} for k, n, s in imports],
            'actual_used_code_import_counts': {k: int(v) for k, v in used}, 'cxx_failbits': 0}


def metrics(raw):
    # Same descriptive formula as approved P1; no calibrated comparator or model.
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


def selfchecks(config):
    validate(config)
    rejected = []
    changes = [('omit byte', lambda c: c['rows'].pop()),
               ('duplicate byte', lambda c: c['rows'][1].update(release_velocity_byte=0)),
               ('fractional byte', lambda c: c['rows'][0].update(release_velocity_byte=0.5)),
               ('out-of-domain byte', lambda c: c['rows'][0].update(release_velocity_byte=128)),
               ('inherited control replay', lambda c: c['rows'][64].update(disposition='fresh-planned')),
               ('new expected waveform', lambda c: c['rows'][0].update(waveform_prediction='silent')),
               ('inconsistent packed offevent', lambda c: c['rows'][0]['events'][1].update(velocity=64)),
               ('changed param99', lambda c: c['parameter_f32_bits_le'].__setitem__(99, '00000000')),
               ('wrong script identity', lambda c: c['rows'][0]['script'].update(sha256='0' * 64)),
               ('inherited environment override', lambda c: c['environment'].update(LD_PRELOAD='x')),
               ('wrong direct count', lambda c: c['limits'].update(selected_export_calls_total=127))]
    for name, mutate in changes:
        bad = copy.deepcopy(config)
        mutate(bad)
        try:
            validate(bad)
        except (AssertionError, KeyError):
            rejected.append(name)
        else:
            raise AssertionError('Bad selected input accepted: ' + name)
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
    row = config['rows'][0]
    bindings = [('trap', 26), ('linux', 99), ('data', 7)]
    log = 'init 0x314d0\nslice offset=16384 size=500880\n'
    log += ''.join(f'import {kind} synth_{kind}_{i} slots=1\n' for kind, count in bindings for i in range(count))
    log += ''.join(f'export {name} 0x1\n' for name in ['_CreateInstanceU', '_DestroyInstanceU', '_SetSampleRateU', '_GetPlugInfoU', '_CalcA', '_SetParameterA', '_ResetA'])
    log += 'create ok\nrate 44100 ret=0\n'
    log += ''.join(f'param {i} {struct.unpack("<f", bytes.fromhex(h))[0]}\n' for i, h in enumerate(config['parameter_f32_bits_le']))
    log += 'event 4400 0x90 60 100\nevent 35270 0x80 60 0\ninflag 0\ninput zero\nprocess 44100 512 flags: 87x(ret=0,flag=1) blocks=87\ndestroy\ncxx-failbits 0\nused synth_linux_0 1\n'
    protocol(log, row, config)
    badlogs = {'missing initializer': log.replace('init 0x314d0\n', ''),
               'wrong event byte': log.replace('event 4400 0x90 60 100', 'event 4400 0x90 60 127'),
               'wrong frame phase': log.replace('event 4400', 'event 4401'),
               'wrong off byte': log.replace('event 35270 0x80 60 0', 'event 35270 0x80 60 1'),
               'new off type': log.replace('event 35270 0x80', 'event 35270 0x90'),
               'missing setter': log.replace('param 0 2.0\n', ''),
               'nonzero process return': log.replace('ret=0,flag=1', 'ret=1,flag=1'),
               'wrong flag': log.replace('ret=0,flag=1', 'ret=0,flag=4'),
               'cxx failure': log.replace('cxx-failbits 0', 'cxx-failbits 1'),
               'unexpected used import': log.replace('used synth_linux_0', 'used synth_trap_0'),
               'data binding invoked as code': log.replace('used synth_linux_0', 'used synth_data_0'),
               'new setup operation': log + 'reset\n',
               'fault text': log + 'FAULT sig=11\n'}
    protocol_rejected = []
    for name, bad in badlogs.items():
        try:
            protocol(bad, row, config)
        except AssertionError:
            protocol_rejected.append(name)
        else:
            raise AssertionError('Bad synthetic protocol accepted: ' + name)
    return {'input_negative_controls': rejected, 'synthetic_protocol_negative_controls': protocol_rejected,
            'descriptive_data_controls': ['zero retains NULL first/last', 'right-channel-only signal retained', 'right NaN rejected', 'left infinity rejected', 'signed-zero bytes retained separately from numeric zero', 'empty/truncated geometry rejected']}
