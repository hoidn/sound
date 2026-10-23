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
    assert receipt['id'] == row['id'] and receipt['velocity_byte'] == row['velocity_byte']
    assert receipt['fresh_ordinal'] == row['fresh_ordinal'] and receipt['pid'] > 0
    assert receipt['argv'] == [config['executable']['path'], config['bundle_slice_expected']['path'], row['script']['path'], str(folder / 'output.f32'), '--imports']
    assert receipt['child_environment'] == config['environment']
    assert receipt['attempts'] == 1 and receipt['exit'] == 0 and not receipt['timeout']
    assert receipt['error'] is None and receipt['cleanup'] == [] and 'custody_error' not in receipt
    assert receipt['waveform_prediction'] is receipt['portable_comparator'] is None
    assert stderr == b'' and len(raw) == 352800 and 0 < len(stdout) <= 4194304
    for key, data in [('stdout', stdout), ('stderr', stderr), ('output', raw)]:
        assert receipt[key]['bytes'] == len(data) and receipt[key]['sha256'] == hashlib.sha256(data).hexdigest()
    assert D['protocol'](stdout.decode('ascii'), row, config) == receipt['protocol']
    observed = D['metrics'](raw)
    assert observed == receipt['observed_output'] and observed['all_finite'] and observed['frames'] == 44100
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
    inherited = load('inherited-velocity100.json')
    assert inherited['fresh_receipt'] is None and inherited['new_original_calls'] == 0
    assert inherited['approved_projection']['id'] == 'baseline-DAN028'
    assert inherited['approved_projection']['parameter_vector_sha256'] == config['parameter_vector_sha256']
    assert inherited['approved_projection']['output_sha256'] == inherited['historical_raw_output_not_opened']['sha256']
    assert inherited['historical_raw_output_not_opened']['bytes'] == 352800
    summary, context = load('execution-summary.json'), load('execution-context.json')
    assert summary['status'] == 'COMPLETE-127-ONCE' and summary['error'] is None
    assert summary['attempted_children'] == summary['successful_protocols'] == 127
    assert summary['selected_export_calls_with_valid_protocol'] == 37211 and summary['CalcA_with_valid_protocol'] == 11049
    assert summary['loader_initializer_entries_logged_separately'] == 127 and summary['all_native_calls_count'] is None
    assert summary['source_before'] == summary['source_after'] == context['source_before'] == config['source_pins']
    assert summary['retries'] == 0 and summary['unattempted_ids'] == [] and summary['inherited_not_replayed'] == 1
    records = [json.loads(s) for s in (HERE / 'results.jsonl').read_text().splitlines()]
    fresh = [r for r in config['rows'] if r['disposition'] == 'fresh-planned']
    assert len(records) == len(fresh) == 127 and len({r['pid'] for r in records}) == 127
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
        same_hash = receipt['output']['sha256'] == inherited['historical_raw_output_not_opened']['sha256']
        assert receipt['output_sha256_matches_inherited_velocity100'] == same_hash
        points.append({'id': row['id'], 'velocity_byte': row['velocity_byte'], 'provenance': 'fresh-once-only',
                       'input_script': row['script'], 'parameter_vector_sha256': row['parameter_vector_sha256'],
                       'receipt_pointer': '#/' + str(row['fresh_ordinal'] - 1), 'pid': receipt['pid'],
                       'output': receipt['output'], 'observed_output': observed,
                       'output_sha256_matches_inherited100': same_hash, 'waveform_prediction': None,
                       'portable_comparator': None, 'candidate_grade': None})
        if fixtures is None:
            fixtures = row, receipt, stdout, stderr, raw
    for a, b in zip(records, records[1:]):
        assert a['utc_end'] <= b['utc_start']
    points.append({'id': 'AVB-100', 'velocity_byte': 100, 'provenance': 'inherited-approved-not-reexecuted',
                   'approved_summary_pointer': 'inherited-velocity100.json#/approved_projection',
                   'fresh_receipt': None, 'historical_output': inherited['historical_raw_output_not_opened'],
                   'observed_output': inherited['approved_projection']['observed_output_recomputed'],
                   'portable_comparator': None, 'candidate_grade': None})
    points.sort(key=lambda x: x['velocity_byte'])
    assert [r['velocity_byte'] for r in points] == list(range(128))
    row, receipt, stdout, stderr, raw = fixtures
    rejected = []
    for name, mutate in [('replayed inherited byte', lambda x: x.update(velocity_byte=100)),
                         ('invented prediction', lambda x: x.update(waveform_prediction='silent')),
                         ('nonzero exit', lambda x: x.update(exit=87)),
                         ('timeout hidden', lambda x: x.update(timeout=True)),
                         ('changed argv', lambda x: x['argv'].__setitem__(2, 'wrong.script')),
                         ('custody mismatch', lambda x: x['custody_after'][0].update(sha256='0' * 64)),
                         ('changed flags', lambda x: x['protocol']['flags'][0].update(flag=3)),
                         ('right-channel metric erased', lambda x: x['observed_output']['per_channel'].pop())]:
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
            'logical_points': 128, 'fresh_children': 127, 'inherited_not_replayed': 1, 'fresh_stereo_bytes': 44805600,
            'selected_export_calls': 37211, 'CalcA': 11049, 'loader_initializer_log_entries_separate': 127,
            'all_native_calls': None, 'per_child_custody_pairs': len(records[0]['custody_before']),
            'total_runtime_local_custody_pairs': sum(len(r['custody_before']) for r in records),
            'fresh_all_finite_both_channels': all(r['observed_output']['all_finite'] for r in records),
            'all_fresh_channels_byte_identical': all(r['observed_output']['channels_byte_identical'] for r in records),
            'fresh_output_hash_matches_inherited100': sum(r['output_sha256_matches_inherited_velocity100'] for r in records),
            'fresh_wholly_zero_outputs': sum(r['observed_output']['nonzero_frames'] == 0 for r in records),
            'inherited_control_raw_reads': 0, 'checker_original_calls': 0, 'external_runtime_reads': 0,
            'method': 'Same approvedP1 descriptive stereo peak/rms/mean/nonzero formula; no tolerance/f0/model/fit. Old100hash/metrics inherited only, not oldrawaudio decode. Hashidentity is distinguished from new bytewise baselinecomparison.',
            'points': points}


if __name__ == '__main__':
    assert sys.argv[1:] == ['--check']
    print(json.dumps(check(), indent=2, allow_nan=False))
