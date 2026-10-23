#!/usr/bin/env python3
"""Stdlib prepared collector. Self-checks never spawn or import retained drivers.

Original execution exists only behind --execute-after-review, a matching frozen
manifest and an independent readiness receipt. Preparation must use --self-check.
"""
import argparse
import copy
import hashlib
import json
import math
import os
import re
import resource
import signal
import struct
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path):
    return json.loads(path.read_text())


def verify_file(identity):
    p = Path(identity['path'])
    p = p if p.is_absolute() else ROOT / p
    raw = p.read_bytes()
    assert len(raw) == identity['bytes'] and sha(raw) == identity['sha256'], str(p)
    if 'resolved_path' in identity:
        assert str(p.resolve()) == identity['resolved_path']
    return raw


def f32(value):
    return struct.unpack('<f', struct.pack('<f', value))[0]


def output_samples(raw, frames):
    assert len(raw) == frames * 8, 'wrong stereo binary32 output size'
    samples = list(struct.iter_unpack('<ff', raw))
    assert all(math.isfinite(v) for row in samples for v in row), 'nonfinite output'
    return samples


def baseline_validation(raw, frames):
    samples = output_samples(raw, frames)
    energy = [math.fsum(row[c] * row[c] for row in samples) for c in range(2)]
    assert all(math.isfinite(v) and v > 0 for v in energy), 'baseline channel has no positive energy'
    return {'frames': frames, 'bytes': len(raw), 'sha256': sha(raw), 'all_samples_finite': True,
            'baseline_energy_left': energy[0], 'baseline_energy_right': energy[1]}


def pair_measurements(baseline, changed, frames, change_frame):
    result = baseline_validation(baseline, frames)
    left = output_samples(baseline, frames)
    right = output_samples(changed, frames)
    numeric_prefix_equal = all(left[n][c] == right[n][c] for n in range(change_frame) for c in range(2))
    bits_prefix_equal = baseline[:change_frame*8] == changed[:change_frame*8]
    assert numeric_prefix_equal and bits_prefix_equal, 'prechange prefix identity failed'
    first = [next((n for n in range(frames) if left[n][c] != right[n][c]), None) for c in range(2)]
    present = [n for n in first if n is not None]
    joint = min(present) if present else None
    result.update({'change_output_sha256': sha(changed), 'changed_all_samples_finite': True,
                   'prechange_numeric_identity': numeric_prefix_equal, 'prechange_byte_identity': bits_prefix_equal,
                   'first_numeric_difference': {'left': first[0], 'right': first[1], 'joint': joint},
                   'first_numeric_difference_from_change': {
                       'left': None if first[0] is None else first[0]-change_frame,
                       'right': None if first[1] is None else first[1]-change_frame,
                       'joint': None if joint is None else joint-change_frame},
                   'signed_zero_rule': '+0 and -0 compare numerically equal; prefix also requires exact bytes',
                   'status': 'UNGRADED-discovery; no trajectory oracle or settling claim'})
    return result


def validate_history(history):
    event = history['queued_event']['frame']
    blocks = history['block_frames']
    intervals = history['process_commands']
    assert event == 8192 and blocks == 512
    assert [p['frames'] for p in intervals] == [13312, 7680]
    assert all(p['frames'] % blocks == 0 for p in intervals)
    selected = [i+1 for i, p in enumerate(intervals) if 0 <= event < p['frames']]
    assert selected == [1], 'queued event would replay'
    assert history['total_frames'] == sum(p['frames'] for p in intervals) == 20992
    assert sum(p['frames']//blocks for p in intervals) == 41
    assert history['event_delivery'] == {'process_command': 1, 'callback_cumulative_start': 8192,
                                         'event_offset': 0, 'timestamp_cumulative': 8192}
    grid = history['grid_premise_only']
    period = 44100 // 1000
    g = event // period * period
    callback = event // blocks * blocks
    g_prime = g if g >= callback else g + period
    assert (period, g, g_prime, g_prime+1) == (44, 8184, 8228, 8229)
    assert (grid['P'], grid['g'], grid['g_prime_under_zero_phase_continuous_protocol'],
            grid['first_possible_changed_frame_under_owner_rule']) == (period, g, g_prime, g_prime+1)


def validate_script(run, entries, target, plan):
    p = HERE / run['script']['path']
    raw = p.read_bytes()
    assert len(raw) == run['script']['bytes'] and sha(raw) == run['script']['sha256']
    lines = raw.decode().splitlines()
    allowed = {'mxcsr', 'create', 'rate', 'param', 'transport', 'event', 'inflag', 'input', 'process', 'destroy'}
    assert all(line.split()[0] in allowed for line in lines)
    expected = ['mxcsr 0x1f80', 'create', 'rate 44100']
    expected += [f"param {e['index']} {e['binary32_value']!r}" for e in entries]
    value = target['baseline_binary32'] if run['role'] == 'baseline' else target['target_binary32']
    expected += ['transport 0 0 120', 'event 8192 0x90 48 100', 'inflag 0', 'input zero',
                 'process 13312 512', f"param {target['index']} {value!r}", 'process 7680 512', 'destroy']
    assert lines == expected
    assert sum(line.startswith('param ') for line in lines) == 204
    calls = 204 + 41 + 3
    assert calls == run['direct_export_invocations'] == 248 <= plan['limits']['direct_export_cap_per_child'] == 256
    assert run['CalcA_calls'] == 41
    assert run['output_bytes'] == run['frames'] * run['channels'] * 4 == 167936
    assert run['argv'][2] == str(p.resolve())
    assert run['argv'][3] == run['output_path']
    assert run['argv'][4:] == ['--imports']


def preflight():
    ids = read(HERE / 'identities.json')
    selection = read(HERE / 'selection.json')
    plan = read(HERE / 'execution-plan.json')
    vector = read(HERE / 'baseline-vector.json')
    for p in ids['source_pins'] + ids['external_pins']:
        verify_file(p)
    correction = selection['approved_route_correction']
    assert correction['manifest']['sha256'] == '44e0d729932f4d6626641b959d50db9ee178b07d141e666c55127b5ccb1e087d'
    assert correction['review']['sha256'] == '81b4d1ecccfe20bd7619f75b0fa7258d761e238a55e5e07b7d50fe55de789a10'
    review = read(ROOT / correction['review']['path'])
    assert review['disposition'] == 'approved-bounded-family-route-correction'
    assert review['reviewed_manifest']['sha256'] == correction['manifest']['sha256']
    t12 = read(ROOT / 'analysis/ableton-live-12.4.3/r2/t12-analog-v1/manifest.json')
    for name in ['xdev.c', 'xdev.h', 'xdev_load.c', 'xdev_bind.c', 'xdev_cxx.c']:
        p = ROOT / 'analysis/ableton-live-12.4.3/r2/t12-analog-v1/harness' / name
        assert sha(p.read_bytes()) == t12['files']['harness/'+name]['sha256']
    loader = next(p for p in ids['external_pins'] if p['path'] == '/var/tmp/sound-analysis/t12-analog/xdev')
    assert loader['sha256'] == t12['tools']['loader_sha256'] == '3eec4ad1cfa0765c9e8267806cf02b7e664a07157043e3a170388cfa4d63cf14'
    assert loader['bytes'] == 149608 and os.access(loader['path'], os.X_OK)
    assert Path(sys.executable).resolve() == Path(ids['host_as_of']['python_executable']).resolve()
    assert sys.version == ids['host_as_of']['python_version']
    assert os.confstr('CS_GNU_LIBC_VERSION') == ids['host_as_of']['glibc']
    assert os.uname().machine == ids['host_as_of']['uname']['machine'] == 'x86_64'
    meta = ids['original_bundle']
    original = Path(meta['path']).read_bytes()
    assert sha(original) == meta['file_sha256']
    assert sha(original[meta['x86_64_offset']:meta['x86_64_offset']+meta['x86_64_size']]) == meta['x86_64_sha256']
    evaluation = read(ROOT / 'handoff/device-analog-v1/cases.json')['cases'][11]['evaluations'][0]
    entries = vector['entries']
    assert evaluation['id'] == 'ANALOG-AUDIO-013-01' and len(entries) == 203
    for i, e in enumerate(entries):
        assert e['index'] == i and e['label'] == evaluation['parameter_order'][i]
        assert e['binary32_value'] == f32(evaluation['parameters'][e['label']])
        assert struct.pack('<f', e['binary32_value']).hex() == e['binary32_little_endian_hex']
    params = evaluation['parameters']
    for name in ['SignalChain1/OscillatorToggle', 'SignalChain1/FilterToggle', 'SignalChain1/AmplifierToggle',
                 'SignalChain1/Envelope.0/Enabled', 'SignalChain1/Envelope.1/Enabled',
                 'SignalChain1/Envelope.0/SustainLevel', 'SignalChain1/Envelope.1/SustainLevel']:
        assert params[name] == 1
    assert params['SignalChain1/OscillatorWaveShape'] == 1
    assert params['SignalChain1/FilterQFactor'] == f32(0.6)
    raw = read(ROOT / 'analysis/ableton-live-12.4.3/r2/t12-analog-v1/results/protocol.json')['parameter_changes']
    assert len(selection['targets']) == len(raw) == 8
    for target, old in zip(selection['targets'], raw):
        assert target['index'] == old['index']
        assert target['target_binary32'] == f32(old['value'])
        assert target['baseline_binary32'] == entries[target['index']]['binary32_value']
        assert target['target_hex'] != target['baseline_hex']
        assert target['target_hex'] == struct.pack('<f', target['target_binary32']).hex()
    validate_history(selection['history'])
    assert len(plan['runs']) == 16 and len(plan['pairs']) == 8
    assert plan['limits']['no_retries'] and plan['limits']['stop_first_fault_or_invalid']
    assert plan['limits']['core_bytes'] == 0
    assert plan['run_order'] == [r['id'] for r in plan['runs']]
    for run in plan['runs']:
        target = next(t for t in selection['targets'] if t['id'] == run['control_id'])
        validate_script(run, entries, target, plan)
        assert run['environment'] == ids['planned_child_environment'] == {
            'LC_ALL': 'C', 'LANG': 'C', 'TZ': 'UTC', 'PATH': '/usr/bin:/bin', 'XDEV_TIME': '0'}
        assert run['argv'][0] == loader['path'] and run['argv'][1] == meta['path']
        assert Path(run['output_path']).parent.parent == Path(plan['actual_output_root'])
    return ids, selection, plan


def reject(call, name):
    try:
        call()
    except (AssertionError, ValueError):
        return name
    raise AssertionError('negative selfcheck accepted: ' + name)


def selfchecks():
    ids, selection, plan = preflight()
    negative = []
    bad = copy.deepcopy(selection['history'])
    bad['queued_event']['frame'] = 4400
    negative.append(reject(lambda: validate_history(bad), 'replayed-legacy-note-history'))
    bad = copy.deepcopy(selection['history'])
    bad['process_commands'][1]['frames'] = 13312
    negative.append(reject(lambda: validate_history(bad), 'replay-capable-second-process'))
    pack = lambda rows: b''.join(struct.pack('<ff', *row) for row in rows)
    baseline = pack([(1., 2.), (1., 2.), (0., 0.), (1., 2.)])
    changed = pack([(1., 2.), (1., 2.), (-0., 0.), (2., 2.)])
    result = pair_measurements(baseline, changed, 4, 2)
    assert result['first_numeric_difference'] == {'left': 3, 'right': None, 'joint': 3}
    right_first = pack([(1., 2.), (1., 2.), (0., 3.), (2., 2.)])
    assert pair_measurements(baseline, right_first, 4, 2)['first_numeric_difference'] == {'left': 3, 'right': 2, 'joint': 2}
    assert pair_measurements(baseline, baseline, 4, 2)['first_numeric_difference']['joint'] is None
    negative.append(reject(lambda: output_samples(baseline[:-1], 4), 'wrong-full-output-size'))
    nonfinite = pack([(1., 2.), (1., 2.), (float('nan'), 1.), (1., 2.)])
    negative.append(reject(lambda: output_samples(nonfinite, 4), 'nonfinite-full-output'))
    zero_channel = pack([(1., 0.)] * 4)
    negative.append(reject(lambda: baseline_validation(zero_channel, 4), 'silent-baseline-channel'))
    early = pack([(2., 2.), (1., 2.), (0., 0.), (1., 2.)])
    negative.append(reject(lambda: pair_measurements(baseline, early, 4, 2), 'prechange-numeric-mismatch'))
    prefix_signed = pack([(1., 2.), (-0., 2.), (0., 0.), (1., 2.)])
    prefix_base = pack([(1., 2.), (0., 2.), (0., 0.), (1., 2.)])
    negative.append(reject(lambda: pair_measurements(prefix_base, prefix_signed, 4, 2), 'prechange-signedzero-byte-mismatch'))
    bad_run = copy.deepcopy(plan['runs'][0])
    bad_run['direct_export_invocations'] = 257
    target = selection['targets'][0]
    entries = read(HERE / 'baseline-vector.json')['entries']
    negative.append(reject(lambda: validate_script(bad_run, entries, target, plan), 'call-cap-metadata-mismatch'))
    fake = {'disposition': 'approved-bounded-analog-change-history-preparation',
            'ready_for_root_execution': True, 'reviewed_manifest': {'sha256': 'a'*64, 'path': str(HERE/'manifest.json')}}
    approval_checks(fake, 'a'*64, HERE/'manifest.json', plan['execution_gate'])
    no_approval = copy.deepcopy(fake)
    no_approval['ready_for_root_execution'] = False
    negative.append(reject(lambda: approval_checks(no_approval, 'a'*64, HERE/'manifest.json', plan['execution_gate']), 'readiness-not-approved'))
    negative.append(reject(lambda: approval_checks(fake, 'b'*64, HERE/'manifest.json', plan['execution_gate']), 'reviewed-seal-mismatch'))
    return {'status': 'PASS-preparation-integrity-and-owned-stdlib-selfchecks; pending-independent-readiness',
            'source_pins': len(ids['source_pins']), 'external_pins': len(ids['external_pins']),
            'baseline_components': 203, 'control_pairs': 8, 'prepared_children': 16,
            'direct_export_calls_per_child': 248, 'direct_export_cap': 256, 'CalcA_per_child': 41,
            'single_queued_note_delivery': True, 'negative_selfchecks_rejected': negative,
            'signedzero_numeric_firstdifference': 'equal; tested with postchange signedzero-only difference before a real difference',
            'unchanged_pair_result': 'None accepted', 'original_calls_performed': 0,
            'retained_model_comparator_measurement_or_driver_imported': False,
            'new_outputs_exist': Path(plan['actual_output_root']).exists(), 'grading': 'UNGRADED-discovery-only',
            'readiness_gates': ids['notready_gates']}


def check_log(raw, run):
    text = raw.decode('utf-8', errors='replace')
    assert len(raw) <= 262144
    assert not re.search(r'(?m)^(TRAP\b|xdev:)', text), 'loader trap/error'
    assert text.count('create ok\n') == 1 and 'create NULL' not in text
    assert re.findall(r'(?m)^cxx-failbits (\d+)$', text) == ['0']
    assert len(re.findall(r'(?m)^param ', text)) == 204
    assert len(re.findall(r'(?m)^rate ', text)) == 1 and len(re.findall(r'(?m)^destroy$', text)) == 1
    counts = [int(v) for v in re.findall(r'(?m)^process .* blocks=(\d+)$', text)]
    assert counts == [26, 15] and sum(counts) == 41
    assert len(re.findall(r'(?m)^export ', text)) == 7
    return {'logged_init_entries': len(re.findall(r'(?m)^init ', text)),
            'direct_export_calls_observed_from_commands_and_blocks': 204+1+1+41+1,
            'import_bindings_logged': len(re.findall(r'(?m)^import ', text)),
            'used_import_counter_rows': len(re.findall(r'(?m)^used ', text)),
            'loader_log_sha256': sha(raw)}


def approval_checks(receipt, manifest_sha, manifest_path, gate):
    assert receipt['disposition'] == gate['required_disposition'], 'independent readiness disposition required'
    assert receipt['ready_for_root_execution'] is True, 'independent readiness must explicitly pass'
    assert receipt['reviewed_manifest']['sha256'] == manifest_sha, 'readiness receipt must match frozen preparation'
    assert (ROOT / receipt['reviewed_manifest']['path']).resolve() == manifest_path.resolve()


def execute_after_review(receipt_path):
    manifest_path = HERE / 'manifest.json'
    assert manifest_path.is_file(), 'Root-frozen preparation manifest required'
    manifest_raw = manifest_path.read_bytes()
    receipt = read(receipt_path)
    plan = read(HERE / 'execution-plan.json')
    approval_checks(receipt, sha(manifest_raw), manifest_path, plan['execution_gate'])
    manifest = json.loads(manifest_raw)
    for p in manifest['files']:
        raw = (HERE / p['path']).read_bytes()
        assert len(raw) == p['bytes'] and sha(raw) == p['sha256'], p['path']
    readiness = selfchecks()  # Owned fabricated-byte/source checks only, before any original child.
    identities = read(HERE / 'identities.json')
    output_root = Path(plan['actual_output_root'])
    assert output_root.is_absolute() and output_root.parent == HERE.parent
    assert output_root.name == 'batch-analog-change-history-v1-actual'
    assert not output_root.exists(), 'refuse existing output root; no retry/overwrite'
    output_root.mkdir()
    record = {'status': 'running-UNGRADED-discovery', 'preparation_manifest_sha256': sha(manifest_raw),
              'readiness_receipt': {'path': str(receipt_path.resolve()), 'sha256': sha(receipt_path.read_bytes())},
              'preflight': readiness, 'runs': [], 'pairs': [], 'original_execution_attempted': False,
              'original_processes_started': 0}
    record_path = output_root / 'actual-record.json'

    def save():
        record_path.write_text(json.dumps(record, indent=2) + '\n')

    limits = plan['limits']

    def child_limits():
        resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
        resource.setrlimit(resource.RLIMIT_CPU, tuple(limits['cpu_seconds_soft_hard']))
        resource.setrlimit(resource.RLIMIT_AS, (limits['address_space_bytes'], limits['address_space_bytes']))
        resource.setrlimit(resource.RLIMIT_FSIZE, (limits['file_size_bytes_per_file'], limits['file_size_bytes_per_file']))

    try:
        for pair in plan['pairs']:
            outputs = {}
            for run_id in [pair['baseline_run'], pair['change_run']]:
                run = next(r for r in plan['runs'] if r['id'] == run_id)
                for external in identities['external_pins']:
                    verify_file(external)
                script = HERE / run['script']['path']
                assert sha(script.read_bytes()) == run['script']['sha256']
                run_dir = output_root / run_id
                run_dir.mkdir()
                print('START ' + run_id, flush=True)
                child = None
                item = {'id': run_id, 'argv': run['argv'], 'environment': run['environment'], 'limits': limits,
                        'status': 'started', 'attempt': 1}
                record['runs'].append(item)
                save()
                with Path(run['stdout_stderr_path']).open('xb') as log:
                    record['original_execution_attempted'] = True
                    child = subprocess.Popen(run['argv'], stdin=subprocess.DEVNULL, stdout=log, stderr=subprocess.STDOUT,
                                             cwd=run['cwd'], env=run['environment'], start_new_session=True,
                                             preexec_fn=child_limits)
                    record['original_processes_started'] += 1
                    try:
                        code = child.wait(timeout=limits['wall_timeout_seconds_per_child'])
                    except BaseException:
                        try:
                            os.killpg(child.pid, signal.SIGKILL)
                        except ProcessLookupError:
                            pass
                        child.wait()
                        item['status'] = 'timeout-or-interrupted-killed-no-retry'
                        save()
                        raise
                item['returncode'] = code
                assert code == 0, f'original child failed code={code}'
                item['log_checks'] = check_log(Path(run['stdout_stderr_path']).read_bytes(), run)
                raw = Path(run['output_path']).read_bytes()
                output_samples(raw, run['frames'])
                if run['role'] == 'baseline':
                    item['baseline_validation'] = baseline_validation(raw, run['frames'])
                item['output'] = {'path': run['output_path'], 'bytes': len(raw), 'sha256': sha(raw)}
                outputs[run['role']] = raw
                item['status'] = 'captured-UNGRADED'
                save()
                print('CAPTURED ' + run_id, flush=True)
            measured = pair_measurements(outputs['baseline'], outputs['change'], 20992, 13312)
            record['pairs'].append({'id': pair['id'], 'measurement': measured, 'expectation': 'unknown; no grade'})
            save()
        record['status'] = 'captured-all-eight-pairs-UNGRADED-pending-actualresult-review-owner-reconciliation'
        save()
    except BaseException as exc:
        record['status'] = 'stopped-first-fault-or-invalid-no-retry-UNGRADED'
        record['error'] = {'type': type(exc).__name__, 'message': str(exc)}
        save()
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--self-check', action='store_true')
    mode.add_argument('--execute-after-review', type=Path)
    parser.add_argument('--report-file', type=Path, help='Self-check report only; use outside frozen packet after seal.')
    args = parser.parse_args()
    if args.self_check:
        report = selfchecks()
        if args.report_file:
            args.report_file.write_text(json.dumps(report, indent=2) + '\n')
        print(json.dumps(report, indent=2))
    else:
        assert args.report_file is None
        execute_after_review(args.execute_after_review)


if __name__ == '__main__':
    main()
