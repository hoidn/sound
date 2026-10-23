#!/usr/bin/env python3
"""Finite retained-byte observations only; never launches originals or grades a candidate."""
import hashlib
import json
import math
from pathlib import Path
import struct
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def samples(raw):
    assert len(raw) % 8 == 0
    assert all(word & 0x7f800000 != 0x7f800000 for (word,) in struct.iter_unpack('<I', raw)), 'nonfinite output'
    return list(struct.iter_unpack('<ff', raw))


def metric(raw):
    frames = samples(raw)
    values = [v for pair in frames for v in pair]
    return {'frames': len(frames), 'bytes': len(raw), 'sha256': sha(raw), 'finite': True,
            'peak_abs': max((abs(v) for v in values), default=0.0),
            'RMS_both_channels': math.sqrt(math.fsum(v * v for v in values) / len(values)) if values else 0.0,
            'nonzero_sample_words': sum((word & 0x7fffffff) != 0 for (word,) in struct.iter_unpack('<I', raw)),
            'channels_bit_identical': all(raw[i:i + 4] == raw[i + 4:i + 8] for i in range(0, len(raw), 8))}


def compare(a, b):
    assert len(a) == len(b)
    aa, bb = samples(a), samples(b)
    delta = [x - y for ap, bp in zip(aa, bb) for x, y in zip(ap, bp)]
    return {'frames': len(aa), 'byte_identical': a == b,
            'different_sample_words': sum(a[i:i + 4] != b[i:i + 4] for i in range(0, len(a), 4)),
            'max_abs_difference': max((abs(v) for v in delta), default=0.0),
            'RMS_difference': math.sqrt(math.fsum(v * v for v in delta) / len(delta)) if delta else 0.0,
            'general_no_effect_or_causality_law': None, 'candidate_grade': None}


def synthetic():
    passed = []
    for name, callback in [
        ('nonfinite-output-rejected', lambda: samples(struct.pack('<II', 0x7f800000, 0))),
        ('partial-frame-rejected', lambda: samples(b'\0' * 4)),
        ('unequal-comparison-length-rejected', lambda: compare(b'\0' * 8, b''))]:
        try:
            callback()
        except AssertionError:
            passed.append({'name': name, 'rejected': True})
        else:
            raise AssertionError(name)
    assert metric(struct.pack('<ff', 1.0, 1.0))['RMS_both_channels'] == 1.0
    assert compare(struct.pack('<ff', 1.0, -1.0), struct.pack('<ff', 0.0, 0.0))['max_abs_difference'] == 1.0
    assert not metric(struct.pack('<II', 0, 0x80000000))['channels_bit_identical']
    passed.append({'name': 'sign-zero-and-nonzero-controls', 'positive_check': True})
    return passed


def main():
    config = json.loads((HERE / 'inputs.json').read_text())
    result = json.loads((HERE / 'results.json').read_text())
    assert result['status'] == 'COMPLETE-12-ONE-ATTEMPT-EACH' and result['error'] is None
    assert len(result['children']) == 12 and len({r['pid'] for r in result['children']}) == 12
    assert result['custody_before'] == result['custody_after']
    raw = {}
    rows = []
    for selected, captured in zip(config['inputs'], result['children']):
        assert selected['id'] == captured['id'] and captured['exit'] == 0 and not captured['timeout']
        path = Path(captured['output.f32']['path'])
        assert path == HERE / 'attempts' / selected['id'] / 'output.f32'
        content = path.read_bytes()
        assert len(content) == captured['output.f32']['bytes'] == 188416
        assert sha(content) == captured['output.f32']['sha256']
        raw[selected['id']] = content
        rows.append({'id': selected['id'], 'role': selected['role'], 'input_pointer': '/inputs/' + str(len(rows)),
                     'initial_index25': selected['initial_index25'], 'sent_index25': selected['sent_index25'], 'context': selected['context'],
                     'full': metric(content), 'warmup': metric(content[:90112]),
                     'first_segment': metric(content[90112:155648]), 'second_segment': metric(content[155648:]),
                     'direct_export_calls': selected['direct_export_calls'], 'CalcA_calls': 46,
                     'raw_output': captured['output.f32'], 'audio_prediction': None, 'candidate_grade': None})
    comparisons = []
    for selected in config['inputs']:
        if selected['sent_index25'] is None:
            continue
        observed, control = raw[selected['id']], raw[selected['matched_control_id']]
        prefix = compare(observed[:155648], control[:155648])
        assert prefix['byte_identical'], 'unexplained prefix difference; no attribution'
        comparisons.append({'transition': selected['id'], 'matched_no_setter_control': selected['matched_control_id'],
                            'prefix_warmup_and_first_segment': prefix,
                            'post_setter_second_segment': compare(observed[155648:], control[155648:]),
                            'prediction': None, 'universal_law': None, 'candidate_grade': None})
    contrasts = []
    for context in ('held', 'released'):
        disabled, enabled = raw['initial0-no-setter-' + context], raw['initial1-no-setter-' + context]
        off, on = metric(disabled[90112:155648]), metric(enabled[90112:155648])
        assert on['peak_abs'] > off['peak_abs'] and on['peak_abs'] > 0
        contrasts.append({'context': context, 'enabled_peak': on['peak_abs'], 'disabled_peak': off['peak_abs'],
                          'productive_finite_contrast': True, 'physical_or_general_silence_threshold': None})
    observation = {'schema': 'collision-whole12-finite-observations-v1', 'status': 'OBSERVED-UNREVIEWED',
                   'observations': rows, 'comparisons': comparisons, 'productive_controls': contrasts,
                   'summary': {'children': 12, 'transitions': 8, 'controls': 4, 'CalcA_total': 552,
                               'direct_export_total': sum(r['direct_export_calls'] for r in rows), 'nested_calls': None,
                               'raw_output_bytes': sum(len(v) for v in raw.values()),
                               'matched_prefixes_bit_identical': 8,
                               'post_setter_byte_equal': sum(r['post_setter_second_segment']['byte_identical'] for r in comparisons),
                               'post_setter_byte_different': sum(not r['post_setter_second_segment']['byte_identical'] for r in comparisons)},
                   'limits': 'Finite histories under supplied recorded host only. No deterministic waveform/effect/no-effect/smoothing/automation timing/Live A1A2/Apple ARM/physical calibration or public law. Same/different is an observation, no new release comparator.',
                   'synthetic_controls': synthetic()}
    (HERE / 'observations.json').write_text(json.dumps(observation, indent=2, allow_nan=False) + '\n')
    print(json.dumps(observation['summary'], indent=2))


if __name__ == '__main__':
    if sys.argv[1:] == ['--check']:
        print(json.dumps({'status': 'PASS', 'controls': synthetic(), 'original_calls': 0}, indent=2))
    else:
        assert sys.argv[1:] == ['--analyze'], 'use --check or --analyze retained data only'
        main()
