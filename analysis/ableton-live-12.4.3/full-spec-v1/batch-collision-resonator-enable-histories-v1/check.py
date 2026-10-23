#!/usr/bin/env python3
"""Retained-data integrity/whole-class checks only; no runtime/provider acquisitions."""
import copy
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def verify_data(config, result, observed, pre_raw):
    assert result['status'] == 'COMPLETE-12-ONE-ATTEMPT-EACH' and result['error'] is None
    pre = result['pre_call_manifest']
    assert len(pre_raw) == pre['bytes'] and sha(pre_raw) == pre['sha256']
    assert pre_raw.decode() == pre['exact_utf8']
    frozen = json.loads(pre_raw)
    assert frozen['status'] == 'FROZEN-BEFORE-ORIGINAL-CALLS'
    assert result['custody_before'] == result['custody_after'] and len(result['custody_before']) == 34
    assert len(config['inputs']) == len(result['children']) == len(observed['observations']) == 12
    assert len({r['pid'] for r in result['children']}) == 12
    expected = {(i, s, context) for i in (0, 1) for s in (None, 0, 1) for context in ('held', 'released')}
    assert {(r['initial_index25'], r['sent_index25'], r['context']) for r in config['inputs']} == expected
    for selected, captured, row in zip(config['inputs'], result['children'], observed['observations']):
        assert selected['id'] == captured['id'] == row['id']
        assert selected['parameter_tokens'][58] == '0.0' and len(selected['parameter_tokens']) == 139
        assert selected['events'] == [[4097, 144, 60, 100]] + ([[7168, 128, 60, 0]] if selected['context'] == 'released' else [])
        assert selected['audio_prediction'] is selected['difference_prediction'] is selected['candidate_grade'] is None
        assert row['audio_prediction'] is row['candidate_grade'] is None
        assert captured['exit'] == 0 and not captured['timeout'] and captured['cleanup'] is None
        assert captured['stderr.txt']['bytes'] == 0
        assert captured['output.f32']['bytes'] == 188416
        assert row['raw_output'] == captured['output.f32']
        assert row['full']['sha256'] == captured['output.f32']['sha256'] and row['full']['finite']
        assert row['full']['frames'] == 23552
        assert row['warmup']['frames'] == 11264 and row['first_segment']['frames'] == 8192 and row['second_segment']['frames'] == 4096
        assert captured['prefix_before_setter_sha256'] == hashlib.sha256((HERE / 'attempts' / selected['id'] / 'output.f32').read_bytes()[:155648]).hexdigest()
        assert row['direct_export_calls'] == captured['projection']['direct_export_calls'] == selected['direct_export_calls']
        assert row['CalcA_calls'] == selected['CalcA_calls'] == 46
    assert len(observed['comparisons']) == 8
    assert {r['transition'] for r in observed['comparisons']} == {r['id'] for r in config['inputs'] if r['sent_index25'] is not None}
    for pair in observed['comparisons']:
        assert pair['prefix_warmup_and_first_segment']['byte_identical']
        assert pair['prefix_warmup_and_first_segment']['max_abs_difference'] == 0.0
        assert pair['prediction'] is pair['universal_law'] is pair['candidate_grade'] is None
        assert pair['post_setter_second_segment']['general_no_effect_or_causality_law'] is None
        assert pair['post_setter_second_segment']['candidate_grade'] is None
    assert all(r['productive_finite_contrast'] and r['enabled_peak'] > r['disabled_peak'] and r['enabled_peak'] > 0
               for r in observed['productive_controls'])
    summary = observed['summary']
    assert summary['direct_export_total'] == sum(r['direct_export_calls'] for r in config['inputs']) == 2264
    assert summary['CalcA_total'] == 552 and summary['raw_output_bytes'] == 2260992
    assert summary['matched_prefixes_bit_identical'] == 8
    assert summary['post_setter_byte_equal'] == 4 and summary['post_setter_byte_different'] == 4


def main():
    config = json.loads((HERE / 'inputs.json').read_text())
    result = json.loads((HERE / 'results.json').read_text())
    observed = json.loads((HERE / 'observations.json').read_text())
    pre = (HERE / 'pre-call-manifest.json').read_bytes()
    verify_data(config, result, observed, pre)
    frozen = json.loads(pre)
    for pin in frozen['files']:
        raw = (HERE / pin['path']).read_bytes()
        assert len(raw) == pin['bytes'] and sha(raw) == pin['sha256']
    for row in result['children']:
        for name in ('stdout.txt', 'stderr.txt', 'output.f32'):
            pin = row[name]
            path = HERE / 'attempts' / row['id'] / name
            assert str(path) == pin['path']
            raw = path.read_bytes()
            assert len(raw) == pin['bytes'] and sha(raw) == pin['sha256']
    controls = []
    for name, kind, mutate in [
        ('lost-history', 'config', lambda d: d['inputs'].pop()),
        ('R2-enabled', 'config', lambda d: d['inputs'][0]['parameter_tokens'].__setitem__(58, '1.0')),
        ('replayed-event-coordinate', 'config', lambda d: d['inputs'][0]['events'][0].__setitem__(0, 4096)),
        ('duplicate-process-ID', 'result', lambda d: d['children'][0].update(pid=d['children'][1]['pid'])),
        ('concealed-stderr', 'result', lambda d: d['children'][0]['stderr.txt'].update(bytes=80)),
        ('failed-prefix-attributed', 'observed', lambda d: d['comparisons'][0]['prefix_warmup_and_first_segment'].update(byte_identical=False)),
        ('invented-general-law', 'observed', lambda d: d['comparisons'][0].update(universal_law='no effect')),
        ('candidate-pass-invented', 'observed', lambda d: d['observations'][0].update(candidate_grade='pass')),
        ('wrong-direct-call-total', 'observed', lambda d: d['summary'].update(direct_export_total=2263)),
    ]:
        copies = {'config': copy.deepcopy(config), 'result': copy.deepcopy(result), 'observed': copy.deepcopy(observed)}
        mutate(copies[kind])
        try:
            verify_data(copies['config'], copies['result'], copies['observed'], pre)
        except AssertionError:
            controls.append({'name': name, 'rejected': True})
        else:
            raise AssertionError(name)
    print(json.dumps({'status': 'PASS', 'retained_actual_records': 12, 'whole_class': '8transitions+4controls',
                      'pre_call_payloads_unchanged': len(frozen['files']), 'actual_raw_files_verified': 36,
                      'custody_record_pairs': 34, 'negative_controls': controls,
                      'scope': 'Retained new packet only. No runtime/source/provider reads or execution; no independent actual approval claimed.'}, indent=2))


if __name__ == '__main__':
    main()
