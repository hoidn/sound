"""Packet-only checks of fixed Tension inputs, receipts and unsigned stereo summaries."""
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


def check_record(row, receipt, c, stdout, stderr, raw):
    folder = HERE / 'attempts' / row['id']
    assert receipt['id'] == row['id'] and receipt['note_key'] == row['note_key']
    assert receipt['fresh_ordinal'] == row['fresh_ordinal'] and receipt['pid'] > 0
    assert receipt['argv'] == [c['executable']['path'], c['bundle_slice_expected']['path'], row['script']['path'], str(folder / 'output.f32'), '--imports']
    assert receipt['child_environment'] == c['environment']
    assert receipt['attempts'] == 1 and receipt['exit'] == 0 and not receipt['timeout']
    assert receipt['error'] is None and receipt['cleanup'] == [] and 'custody_error' not in receipt
    assert receipt['waveform_prediction'] is receipt['portable_comparator'] is receipt['portable_expected'] is receipt['candidate_grade'] is None
    assert stderr == b'' and len(raw) == 352800 and 0 < len(stdout) <= 4194304
    for k, b in [('stdout', stdout), ('stderr', stderr), ('output', raw)]:
        assert receipt[k]['bytes'] == len(b) and receipt[k]['sha256'] == hashlib.sha256(b).hexdigest()
    assert D['protocol'](stdout.decode('ascii'), row, c) == receipt['protocol']
    observed = D['metrics'](raw)
    assert observed == receipt['observed_output'] and observed['all_finite'] and observed['frames'] == 44100
    expected = list(c['runtime_expected']); image = c['bundle_slice_expected']
    expected.append({'path': image['path'], 'slice_offset': image['x86_64_offset'], 'bytes': image['x86_64_size'], 'sha256': image['x86_64_sha256']})
    expected += [D['identity'](HERE / n) for n in ('inputs.json', 'data.py', 'run_batch.py', 'check_data.py', 'launch.py')]
    expected.append(row['script'])
    assert receipt['custody_before'] == receipt['custody_after'] == expected
    times = [datetime.fromisoformat(receipt[k]) for k in ('utc_start', 'spawn_utc', 'child_end_utc', 'utc_end')]
    assert times == sorted(times) and 0 <= receipt['child_wall_seconds'] <= 20
    return observed


def check_parent(c, context, summary, launch):
    assert context['parent_launch_receipt'] == launch and launch['pid'] == context['outer_pid'] == summary['outer_pid']
    assert launch['exec_argv'] == c['parent_exec_argv'] and launch['exec_environment'] == c['environment'] and launch['core_limit'] == [0, 0]
    assert launch['launch_argv'] == c['parent_launch_argv'][3:] and context['outer_argv'] == c['parent_exec_argv'][3:]
    pre = (HERE / 'pre-call-manifest.json').read_bytes()
    assert launch['pre_call_manifest'] == {'bytes': len(pre), 'sha256': hashlib.sha256(pre).hexdigest()}
    assert datetime.fromisoformat(launch['utc']) <= datetime.fromisoformat(context['utc_start'])


def check():
    c = load('inputs.json'); controls = D['selfchecks'](c)
    pre = load('pre-call-manifest.json')
    for item in pre['payloads']:
        actual = D['identity'](HERE / item['path'])
        assert all(actual[k] == item[k] for k in ('bytes', 'sha256'))
    inherited = load('inherited-controls.json')
    assert inherited['old_raw_audio_reads'] == inherited['new_original_calls'] == 0
    assert [x['note_key'] for x in inherited['controls']] == [36, 48, 60, 72, 84]
    for x in inherited['controls']:
        assert x['fresh_receipt'] is x['fresh_pid'] is x['new_descriptive_metrics'] is None
        assert x['parameter_vector_sha256'] == c['parameter_vector_sha256']
        assert x['input_projection']['events'] == [[4096, 144, x['note_key'], 100], [26146, 128, x['note_key'], 0]]
        assert x['input_projection']['changes'] == {} and x['input_projection']['preset'] is None
    summary, context, launch = [load(n) for n in ('execution-summary.json', 'execution-context.json', 'launch-receipt.json')]
    check_parent(c, context, summary, launch)
    assert summary['status'] == 'COMPLETE-123-ONCE' and summary['error'] is None
    assert summary['attempted_children'] == summary['successful_protocols'] == 123
    assert summary['selected_export_calls_with_valid_protocol'] == 26937 and summary['CalcA_with_valid_protocol'] == 10701
    assert summary['loader_initializer_entries_logged_separately'] == 123 and summary['all_native_calls_count'] is None
    assert summary['source_before'] == summary['source_after'] == context['source_before'] == c['source_pins']
    assert summary['retries'] == 0 and summary['unattempted_ids'] == [] and summary['inherited_not_replayed'] == 5
    records = [json.loads(x) for x in (HERE / 'results.jsonl').read_text().splitlines()]
    fresh = [x for x in c['rows'] if x['disposition'] == 'fresh-planned']
    assert len(records) == len(fresh) == 123 and len({r['pid'] for r in records}) == 123
    points = []; fixture = None
    for row, receipt in zip(fresh, records):
        folder = HERE / 'attempts' / row['id']
        assert sorted(p.name for p in folder.iterdir()) == ['output.f32', 'stderr.txt', 'stdout.txt']
        stdout, stderr, raw = [(folder / n).read_bytes() for n in ('stdout.txt', 'stderr.txt', 'output.f32')]
        observed = check_record(row, receipt, c, stdout, stderr, raw)
        points.append({'id': row['id'], 'note_key': row['note_key'], 'provenance': 'fresh-once-only',
                       'input_script': row['script'], 'input_events': row['events'],
                       'parameter_vector_sha256': row['parameter_vector_sha256'],
                       'receipt_pointer': '#/' + str(row['fresh_ordinal'] - 1), 'pid': receipt['pid'],
                       'output': receipt['output'], 'observed_unsigned_summary': observed,
                       'waveform_prediction': None, 'portable_expected': None, 'portable_comparator': None, 'candidate_grade': None})
        if fixture is None:
            fixture = row, receipt, stdout, stderr, raw
    for a, b in zip(records, records[1:]):
        assert a['utc_end'] <= b['utc_start']
    for x in inherited['controls']:
        points.append({'id': f"TNK-{x['note_key']:03d}", 'note_key': x['note_key'],
                       'provenance': 'inherited-no-replay', 'inherited_control': x, 'fresh_receipt': None,
                       'waveform_prediction': None, 'portable_expected': None, 'portable_comparator': None, 'candidate_grade': None})
    points.sort(key=lambda x: x['note_key']); assert [x['note_key'] for x in points] == list(range(128))
    row, receipt, stdout, stderr, raw = fixture; rejected = []
    for name, edit in [('invent inheritedfresh', lambda x: x.update(note_key=36)),
                       ('invent prior', lambda x: x.update(waveform_prediction='tone')),
                       ('nonzero exit', lambda x: x.update(exit=87)), ('hide timeout', lambda x: x.update(timeout=True)),
                       ('wrong argv', lambda x: x['argv'].__setitem__(2, 'wrong.script')),
                       ('custody mismatch', lambda x: x['custody_after'][0].update(sha256='0'*64)),
                       ('wrong flag', lambda x: x['protocol']['flags'][0].update(flag=4)),
                       ('erase right summary', lambda x: x['observed_output']['nonzero_sample_counts'].pop())]:
        bad = copy.deepcopy(receipt); edit(bad)
        try:
            check_record(row, bad, c, stdout, stderr, raw)
        except AssertionError:
            rejected.append(name)
        else:
            raise AssertionError('Accepted bad receipt ' + name)
    for name, out, err, audio in [('stderr fault', stdout, b'fault', raw), ('truncated raw', stdout, stderr, raw[:-8]),
                                   ('changed raw', stdout, stderr, bytes([raw[0] ^ 1]) + raw[1:]),
                                   ('changed log', stdout + b'FAULT test\n', stderr, raw)]:
        try:
            check_record(row, receipt, c, out, err, audio)
        except AssertionError:
            rejected.append(name)
        else:
            raise AssertionError('Accepted bad data ' + name)
    parent_controls = []
    for name, edit in [('wrong execPID', lambda x: x.update(pid=1)),
                       ('changed execenv', lambda x: x['exec_environment'].update(XDEV_LIBM_ULP='1')),
                       ('wrong precallseal', lambda x: x['pre_call_manifest'].update(sha256='0'*64)),
                       ('changed execargv', lambda x: x['exec_argv'].__setitem__(3, 'wrong.py'))]:
        bad = copy.deepcopy(launch); edit(bad); ctx = copy.deepcopy(context); ctx['parent_launch_receipt'] = bad
        try:
            check_parent(c, ctx, summary, bad)
        except AssertionError:
            parent_controls.append(name)
        else:
            raise AssertionError('Accepted bad parent ' + name)
    return {'status': 'PASS packet-only checks', 'controls': controls, 'retained_negative_controls': rejected,
            'parent_negative_controls': parent_controls, 'logical_points': 128, 'fresh_children': 123,
            'inherited_no_replay': 5, 'fresh_stereo_bytes': 43394400, 'selected_exports': 26937, 'CalcA': 10701,
            'initializer_logs_separate': 123, 'all_native_calls': None,
            'per_child_custody_pairs': len(records[0]['custody_before']),
            'total_runtime_local_pairs': sum(len(r['custody_before']) for r in records),
            'all_fresh_finite_both_channels': all(r['observed_output']['all_finite'] for r in records),
            'all_fresh_stereo_byte_equal': all(r['observed_output']['channels_byte_identical'] for r in records),
            'silent_fresh_keys': [r['note_key'] for r in records if r['observed_output']['nonzero_sample_counts'] == [0, 0]],
            'oldraw_audio_reads': 0, 'external_runtime_reads': 0, 'checker_original_calls': 0,
            'method': 'Same approved Tension unsigned finite/channel/nonzero/negativezero summary class. No float estimator, f0/fit/newmetric/window/tolerance/calibration.',
            'points': points}


if __name__ == '__main__':
    assert sys.argv[1:] == ['--check']
    print(json.dumps(check(), indent=2, allow_nan=False))
