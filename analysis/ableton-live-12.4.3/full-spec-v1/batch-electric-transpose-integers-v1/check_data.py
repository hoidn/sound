"""Packet-only rechecks of exact inputs, receipts and descriptive stereo data."""
from datetime import datetime
import copy
import hashlib
import json
from pathlib import Path
import runpy
import sys

HERE = Path(__file__).resolve().parent
D = runpy.run_path(str(HERE / 'data.py'), run_name='owned_packet_data')


def load(name):
    return json.loads((HERE / name).read_text())


def check_record(row, receipt, config, stdout, stderr, raw):
    folder = HERE / 'attempts' / row['id']
    assert receipt['id'] == row['id'] and receipt['transpose_integer'] == row['transpose_integer']
    assert receipt['fresh_ordinal'] == row['fresh_ordinal'] and receipt['pid'] > 0
    assert receipt['argv'] == [config['executable']['path'], config['bundle_slice_expected']['path'], row['script']['path'], str(folder / 'output.f32'), '--imports']
    assert receipt['child_environment'] == config['environment']
    assert receipt['attempts'] == 1 and receipt['exit'] == 0 and not receipt['timeout']
    assert receipt['error'] is None and receipt['cleanup'] == [] and 'custody_error' not in receipt
    assert receipt['waveform_prediction'] is receipt['portable_comparator'] is None
    assert stderr == b'' and len(raw) == 442912 and 0 < len(stdout) <= 4194304
    for key, data in [('stdout', stdout), ('stderr', stderr), ('output', raw)]:
        assert receipt[key]['bytes'] == len(data) and receipt[key]['sha256'] == hashlib.sha256(data).hexdigest()
    assert D['protocol'](stdout.decode('ascii'), row, config) == receipt['protocol']
    observed = D['audio'](raw)
    assert observed == receipt['observed_output'] and observed['whole']['all_finite'] and observed['whole']['frames'] == 55364
    expected = list(config['runtime_expected'])
    image = config['bundle_slice_expected']
    expected.append({'path': image['path'], 'slice_offset': image['x86_64_offset'], 'bytes': image['x86_64_size'], 'sha256': image['x86_64_sha256']})
    expected += [D['identity'](HERE / n) for n in ('inputs.json', 'data.py', 'run_batch.py', 'check_data.py')]
    expected.append(row['script'])
    assert receipt['custody_before'] == receipt['custody_after'] == expected
    times = [datetime.fromisoformat(receipt[k]) for k in ('utc_start', 'spawn_utc', 'child_end_utc', 'utc_end')]
    assert times == sorted(times) and 0 <= receipt['child_wall_seconds'] <= 20
    return observed


def check():
    config = load('inputs.json')
    controls = D['selfchecks'](config)
    pre = load('pre-call-manifest.json')
    for item in pre['payloads']:
        actual = D['identity'](HERE / item['path'])
        assert all(actual[k] == item[k] for k in ('bytes', 'sha256'))
    inherited = load('inherited-controls.json')
    assert inherited['new_original_calls'] == 0 and [c['transpose_integer'] for c in inherited['controls']] == [0, 12, 24]
    assert all(c['fresh_receipt'] is None and c['historical_raw_output_not_opened']['bytes'] == 442912 for c in inherited['controls'])
    for c in inherited['controls']:
        row = config['rows'][c['transpose_integer']]
        assert c['parameter_f32_bits_le'] == row['parameter_f32_bits_le']
        assert c['parameter_vector_sha256'] == row['parameter_vector_sha256']
    summary, context = load('execution-summary.json'), load('execution-context.json')
    assert summary['status'] == 'COMPLETE-22-ONCE' and summary['error'] is None
    assert summary['attempted_children'] == summary['successful_protocols'] == 22
    assert summary['selected_export_calls_with_valid_protocol'] == 3190 and summary['CalcA_with_valid_protocol'] == 2398
    assert summary['loader_initializer_entries_logged_separately'] == 0 and summary['all_native_calls_count'] is None
    assert summary['source_before'] == summary['source_after'] == context['source_before'] == config['source_pins']
    assert summary['retries'] == 0 and summary['unattempted_ids'] == [] and summary['inherited_not_replayed'] == 3
    records = [json.loads(s) for s in (HERE / 'results.jsonl').read_text().splitlines()]
    fresh = [r for r in config['rows'] if r['disposition'] == 'fresh-planned']
    assert len(records) == len(fresh) == 22 and len({r['pid'] for r in records}) == 22
    points, first_imports, first_exports = [], None, None
    fixtures = None
    for row, receipt in zip(fresh, records):
        folder = HERE / 'attempts' / row['id']
        assert sorted(p.name for p in folder.iterdir()) == ['output.f32', 'stderr.txt', 'stdout.txt']
        stdout, stderr, raw = [(folder / n).read_bytes() for n in ('stdout.txt', 'stderr.txt', 'output.f32')]
        observed = check_record(row, receipt, config, stdout, stderr, raw)
        protocol = receipt['protocol']
        if first_imports is None:
            first_imports, first_exports = protocol['import_declarations'], protocol['exports_declared_not_all_invoked']
        assert first_imports == protocol['import_declarations'] and first_exports == protocol['exports_declared_not_all_invoked']
        points.append({'id': row['id'], 'transpose_integer': row['transpose_integer'], 'provenance': 'fresh-once-only',
                       'input_script': row['script'], 'parameter_vector_sha256': row['parameter_vector_sha256'],
                       'receipt_pointer': '#/' + str(row['fresh_ordinal'] - 1), 'pid': receipt['pid'],
                       'output': receipt['output'], 'observed_output': observed,
                       'waveform_prediction': None,
                       'portable_comparator': None, 'candidate_grade': None})
        if fixtures is None:
            fixtures = row, receipt, stdout, stderr, raw
    for a, b in zip(records, records[1:]):
        assert a['utc_end'] <= b['utc_start']
    for c in inherited['controls']:
        points.append({'id': f"ETI-{c['transpose_integer']:02d}", 'transpose_integer': c['transpose_integer'],
                       'provenance': 'inherited-approved-not-reexecuted', 'approved_control_pointer': c['source_pointer'],
                       'fresh_receipt': None, 'historical_output': c['historical_raw_output_not_opened'],
                       'approved_observations': c['approved_observations'], 'waveform_prediction': None,
                       'portable_comparator': None, 'candidate_grade': None})
    points.sort(key=lambda x: x['transpose_integer'])
    assert [r['transpose_integer'] for r in points] == list(range(25))
    row, receipt, stdout, stderr, raw = fixtures
    rejected = []
    for name, mutate in [('replayed inherited byte', lambda x: x.update(transpose_integer=12)),
                         ('invented prediction', lambda x: x.update(waveform_prediction='silent')),
                         ('nonzero exit', lambda x: x.update(exit=87)),
                         ('timeout hidden', lambda x: x.update(timeout=True)),
                         ('changed argv', lambda x: x['argv'].__setitem__(2, 'wrong.script')),
                         ('custody mismatch', lambda x: x['custody_after'][0].update(sha256='0' * 64)),
                         ('changed flags', lambda x: x['protocol']['flags'][0]['runs'][0].update(flag=3)),
                         ('right-channel metric erased', lambda x: x['observed_output']['whole']['per_channel'].pop())]:
        bad = copy.deepcopy(receipt); mutate(bad)
        try:
            check_record(row, bad, config, stdout, stderr, raw)
        except AssertionError:
            rejected.append(name)
        else:
            raise AssertionError('Bad retained receipt accepted: ' + name)
    for name, s, e, audio in [('stderr anomaly', stdout, b'fault', raw), ('truncated audio', stdout, stderr, raw[:-8]),
                              ('changed audio bytes', stdout, stderr, bytes([raw[0] ^ 1]) + raw[1:]),
                              ('changed stdout', stdout + b'FAULT test\n', stderr, raw)]:
        try:
            check_record(row, receipt, config, s, e, audio)
        except AssertionError:
            rejected.append(name)
        else:
            raise AssertionError('Bad retained data accepted: ' + name)
    return {'status': 'PASS packet-only checks', 'controls': controls, 'retained_negative_controls': rejected,
            'logical_points': 25, 'fresh_children': 22, 'inherited_not_replayed': 3, 'fresh_stereo_bytes': 9744064,
            'selected_export_calls': 3190, 'CalcA': 2398, 'loader_initializer_log_entries_separate': 0,
            'all_native_calls': None, 'per_child_custody_pairs': len(records[0]['custody_before']),
            'total_runtime_local_custody_pairs': sum(len(r['custody_before']) for r in records),
            'fresh_all_finite_both_channels': all(r['observed_output']['whole']['all_finite'] for r in records),
            'all_fresh_channels_byte_identical': all(r['observed_output']['whole']['channels_byte_identical'] for r in records),
            'fresh_warmups_numeric_zero': all(r['observed_output']['warmup']['nonzero_frames'] == 0 for r in records),
            'fresh_wholly_zero_outputs': sum(r['observed_output']['whole']['nonzero_frames'] == 0 for r in records),
            'inherited_control_raw_reads': 0, 'checker_original_calls': 0, 'external_runtime_reads': 0,
            'method': 'Same descriptive stereo peak/rms/mean/nonzero formula as approved P1. Whole/warmup/render separate; no tolerance/f0/model/fit. Three controls inherited only, not old raw audio decoded or replayed.',
            'points': points}



if __name__ == '__main__':
    assert sys.argv[1:] == ['--check']
    print(json.dumps(check(), indent=2, allow_nan=False))
