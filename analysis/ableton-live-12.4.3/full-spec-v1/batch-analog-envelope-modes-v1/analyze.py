#!/usr/bin/env python3
"""Observed finite binary32 data only; never launches the original or a model."""
import hashlib
import json
import math
from pathlib import Path
import re
import struct
import sys

HERE = Path(__file__).resolve().parent


def metrics(raw):
    assert len(raw) % 8 == 0
    frames = list(struct.iter_unpack('<ff', raw))
    assert frames
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


def compare(raw, baseline):
    assert len(raw) == len(baseline) and len(raw) % 8 == 0
    a = list(struct.iter_unpack('<ff', raw))
    b = list(struct.iter_unpack('<ff', baseline))
    bit_frames = [i for i in range(len(a)) if raw[8 * i:8 * i + 8] != baseline[8 * i:8 * i + 8]]
    numeric = [i for i, (x, y) in enumerate(zip(a, b)) if x != y]
    finite = all(math.isfinite(v) for x, y in zip(a, b) for v in x + y)
    return {'byte_identical': raw == baseline, 'byte_differing_frames': len(bit_frames),
            'numeric_differing_frames': len(numeric), 'first_byte_differing_frame': bit_frames[0] if bit_frames else None,
            'last_byte_differing_frame': bit_frames[-1] if bit_frames else None,
            'first_numeric_differing_frame': numeric[0] if numeric else None,
            'last_numeric_differing_frame': numeric[-1] if numeric else None,
            'max_abs_scalar_difference': max(abs(x[c] - y[c]) for x, y in zip(a, b) for c in (0, 1)) if finite else None,
            'rms_scalar_difference': math.sqrt(math.fsum((x[c] - y[c]) ** 2 for x, y in zip(a, b) for c in (0, 1)) / (len(a) * 2)) if finite else None}


def controls():
    zero = struct.pack('<ff', 0, 0)
    minus_zero = struct.pack('<ff', -0.0, 0.0)
    assert compare(minus_zero, zero)['byte_differing_frames'] == 1
    assert compare(minus_zero, zero)['numeric_differing_frames'] == 0
    one_channel = struct.pack('<ff', 0, 1)
    assert metrics(one_channel)['channels_byte_identical'] is False
    assert compare(one_channel, zero)['numeric_differing_frames'] == 1
    assert metrics(struct.pack('<ff', float('nan'), 0))['all_finite'] is False
    assert metrics(struct.pack('<ff', float('inf'), 0))['nonfinite_scalar_count'] == 1
    assert metrics(zero)['first_nonzero_frame'] is None
    assert metrics(zero + one_channel)['first_nonzero_frame'] == 1
    for bad in (b'', b'123', b'1234'):
        try:
            metrics(bad)
        except AssertionError:
            pass
        else:
            raise AssertionError('Bad frame geometry accepted')
    return ['signed-zero bit/numeric separation', 'right-channel-only difference retained',
            'NaN not finite', 'infinity not finite', 'all-zero first frame remains null',
            'zero-based first-nonzero frame', 'empty/truncated frame geometry rejected']


def derive():
    config = json.loads((HERE / 'inputs.json').read_text())
    result = json.loads((HERE / 'results.json').read_text())
    assert result['status'] == 'COMPLETE-21-ONE-ATTEMPT-EACH' and result['error'] is None
    assert result['custody_before'] == result['custody_after']
    assert len(result['children']) == len(config['inputs']) == 21
    assert [r['id'] for r in result['children']] == [r['id'] for r in config['inputs']]
    assert len({r['pid'] for r in result['children']}) == 21
    baseline = (HERE / 'attempts' / config['inputs'][0]['id'] / 'output.f32').read_bytes()
    observations = []
    for setting, record in zip(config['inputs'], result['children']):
        assert record['exit'] == 0 and not record['timeout']
        assert record['stderr']['bytes'] == 0
        directory = HERE / 'attempts' / record['id']
        assert set(p.name for p in directory.iterdir()) == {'stdout.txt', 'stderr.txt', 'output.f32'}
        for key in ('stdout', 'stderr', 'output'):
            path = directory / {'stdout': 'stdout.txt', 'stderr': 'stderr.txt', 'output': 'output.f32'}[key]
            raw = path.read_bytes()
            assert len(raw) == record[key]['bytes'] and hashlib.sha256(raw).hexdigest() == record[key]['sha256']
        raw = (directory / 'output.f32').read_bytes()
        assert len(raw) == 352800
        log = (directory / 'stdout.txt').read_text()
        assert log.count('\ncreate ok\n') == 1 and log.count('\ndestroy\n') == 1
        assert len(re.findall(r'^rate 44100 ret=', log, re.M)) == 1
        param_log = re.findall(r'^param (\d+) (\S+)$', log, re.M)
        assert [int(i) for i, _ in param_log] == list(range(203))
        assert [struct.pack('<f', float(v)).hex() for _, v in param_log] == setting['parameter_f32_bits_le']
        process_log = re.findall(r'^process 44100 512 flags:(.*) blocks=87$', log, re.M)
        assert len(process_log) == 1
        flags = [{'blocks': int(n), 'return': int(ret), 'flag': int(flag)} for n, ret, flag in
                 re.findall(r'(\d+)x\(ret=(-?\d+),flag=(-?\d+)\)', process_log[0])]
        assert sum(r['blocks'] for r in flags) == 87
        exports = dict(re.findall(r'^export (\S+) (0x[0-9a-f]+)$', log, re.M))
        assert len(exports) == 7
        observations.append({'id': record['id'], 'change': setting['change'],
                             'input_vector_sha256': setting['parameter_vector_sha256'],
                             'output_sha256': record['output']['sha256'], 'observed_output': metrics(raw),
                             'observed_process_flags': flags, 'resolved_x86_export_addresses': exports,
                             'observed_difference_from_same_batch_baseline': compare(raw, baseline),
                             'oracle_applied_in_this_batch': None, 'comparison_grade': None})
    return {'schema': 'finite-Analog-P1-observations-v1', 'status': 'PENDING-INDEPENDENT-BATCH-REVIEW',
            'units': '21processes/21outputs;20new one-control vectors+one existing input baseline. Not21required outcomes or grades.',
            'method': 'Raw little-endian interleaved stereo binary32, no resampling/downmix/model. Scalar values exactly widen to Python floats; fsum and sqrt summaries use host binary64 and are descriptive, not calibrated acceptance metrics. Byte and numeric frame comparisons are distinct.',
            'scope': 'One fixed supplied history only. Equality does not establish inactive control or absence of effect; differences establish no general Loop/FreeRun/Legato law, latching, settling, latency or public/ARM/Apple behavior. No waveform determinism assertion from one attempt.',
            'controls': controls(), 'outputs': observations,
            'summary': {'children': 21, 'outputs': 21, 'bytes': sum(c['output']['bytes'] for c in result['children']),
                        'changed_vectors_byte_identical_to_baseline': sum(o['observed_difference_from_same_batch_baseline']['byte_identical'] for o in observations[1:]),
                        'changed_vectors_byte_different_from_baseline': sum(not o['observed_difference_from_same_batch_baseline']['byte_identical'] for o in observations[1:]),
                        'all_finite': all(o['observed_output']['all_finite'] for o in observations),
                        'all_channels_byte_identical': all(o['observed_output']['channels_byte_identical'] for o in observations),
                        'direct_export_calls_from_scripts_and_log': 6153, 'CalcA': 1827,
                        'nested_original_calls': 'unknown; initializers/constructor/library callees not counted',
                        'retries': 0, 'timeouts': 0, 'nonzero_exits': 0}}


if __name__ == '__main__':
    assert len(sys.argv) == 2 and sys.argv[1] in ('--write', '--check')
    observed = derive()
    if sys.argv[1] == '--write':
        (HERE / 'observations.json').write_text(json.dumps(observed, indent=2, allow_nan=False) + '\n')
    else:
        assert json.loads((HERE / 'observations.json').read_text()) == observed
    print(json.dumps({'status': 'PASS', 'mode': sys.argv[1], 'summary': observed['summary'],
                      'author_data_controls': observed['controls'], 'new_original_execution': 0}))
