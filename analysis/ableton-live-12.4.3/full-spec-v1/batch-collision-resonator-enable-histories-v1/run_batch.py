#!/usr/bin/env python3
"""One whole12 Collision enable-history batch, through the unchanged recorded xdev model."""
import copy
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import re
import resource
import signal
import struct
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]


def utc():
    return datetime.now(timezone.utc).isoformat()


def pin(path):
    path = Path(path)
    raw = path.read_bytes()
    return {'path': str(path), 'resolved_path': str(path.resolve()), 'bytes': len(raw),
            'sha256': hashlib.sha256(raw).hexdigest()}


def save(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2, allow_nan=False) + '\n')


def validate(config):
    inputs = config['inputs']
    assert len(inputs) == 12 and len({r['id'] for r in inputs}) == 12
    assert {(r['initial_index25'], r['sent_index25'], r['context']) for r in inputs} == {
        (i, s, c) for i in (0, 1) for s in (None, 0, 1) for c in ('held', 'released')}
    baseline = (ROOT / config['baseline_source']['path']).read_text()
    base_params = [line for line in baseline.splitlines() if line.startswith('param ')]
    assert len(base_params) == 139
    for r in inputs:
        expected_params = base_params.copy()
        expected_params[25] = f"param 25 {r['initial_index25']}.0"
        assert expected_params[58] == 'param 58 0.0'
        expected = ['create', 'rate 44100'] + expected_params
        expected += ['inflag 0', 'input zero', 'process 11264 512', 'event 4097 0x90 60 100']
        events = [[4097, 144, 60, 100]]
        if r['context'] == 'released':
            expected += ['event 7168 0x80 60 0']
            events += [[7168, 128, 60, 0]]
        expected += ['process 8192 512']
        if r['sent_index25'] is not None:
            expected += [f"param 25 {r['sent_index25']}.0"]
        expected += ['process 4096 512', 'destroy']
        script_path = ROOT / r['script']['path']
        assert script_path.parent == HERE / 'scripts'
        actual = pin(script_path)
        assert all(actual[k] == r['script'][k] for k in ('bytes', 'sha256', 'resolved_path'))
        assert script_path.read_text() == '\n'.join(expected) + '\n'
        assert r['parameter_tokens'] == [line.split()[2] for line in expected_params]
        assert r['parameter_f32_le'] == [struct.pack('<f', float(t)).hex() for t in r['parameter_tokens']]
        assert r['events'] == events and r['process_segments'] == [[11264, 512], [8192, 512], [4096, 512]]
        # Existing process-local frame model: no event exists at warm-up; none can replay in segment2.
        assert all(4096 < e[0] < 8192 for e in events)
        assert r['matched_control_id'] == f"initial{r['initial_index25']}-no-setter-{r['context']}"
        assert r['direct_export_calls'] == 188 + (r['sent_index25'] is not None)
        assert r['CalcA_calls'] == 46 and r['output_bytes'] == 188416
        assert r['audio_prediction'] is r['difference_prediction'] is r['candidate_grade'] is None
    assert config['limits']['CalcA_total'] == 552
    assert config['limits']['direct_export_total'] == sum(r['direct_export_calls'] for r in inputs) == 2264
    assert config['limits']['output_bytes_total'] == 12 * 188416 == 2260992
    assert config['environment'] == {'PATH': '/usr/bin:/bin', 'LANG': 'C', 'LC_ALL': 'C', 'TZ': 'UTC', 'XDEV_TIME': '0'}


def synthetic(config):
    controls = []
    for name, mutate in [
        ('missing-transition', lambda c: c['inputs'].pop()),
        ('duplicate-history', lambda c: c['inputs'][0].update(id=c['inputs'][1]['id'])),
        ('replay-coordinate', lambda c: c['inputs'][0]['events'][0].__setitem__(0, 4096)),
        ('R2-enabled', lambda c: c['inputs'][0]['parameter_tokens'].__setitem__(58, '1.0')),
        ('lost-no-setter-control', lambda c: c['inputs'][0].update(sent_index25=0)),
        ('changed-parameter-bits', lambda c: c['inputs'][0]['parameter_f32_le'].__setitem__(2, '0000803f')),
        ('invented-audio-oracle', lambda c: c['inputs'][0].update(audio_prediction='silent')),
        ('wrong-export-total', lambda c: c['limits'].update(direct_export_total=2263)),
        ('ambient-environment', lambda c: c['environment'].update(XDEV_LIBM_ULP='1')),
        ('wrong-script-identity', lambda c: c['inputs'][0]['script'].update(sha256='0' * 64))]:
        modified = copy.deepcopy(config)
        mutate(modified)
        try:
            validate(modified)
        except AssertionError:
            controls.append({'name': name, 'rejected': True})
        else:
            raise AssertionError('accepted negative: ' + name)
    return controls


def custody(config):
    rows = []
    selected = config['source_pins'] + config['runtime_expected'] + [r['script'] for r in config['inputs']]
    for expected in selected:
        actual = pin(ROOT / expected['path'])
        assert all(actual[k] == expected[k] for k in ('bytes', 'sha256', 'resolved_path')), expected['path']
        rows.append(actual)
    rows += [pin(HERE / name) for name in ('inputs.json', 'run_batch.py', 'analyze.py')]
    return rows


def limits():
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    resource.setrlimit(resource.RLIMIT_CPU, (20, 20))
    resource.setrlimit(resource.RLIMIT_FSIZE, (1048576, 1048576))


def projection(log, r):
    assert log.count('create ok\n') == 1 and log.count('destroy\n') == 1
    assert 'slice offset=16384 size=367488\n' in log
    assert not re.search(r'(?im)^(TRAP|FAULT|xdev:)', log)
    assert 'cxx-failbits 0\n' in log
    assert len(re.findall(r'^param ', log, re.M)) == 139 + (r['sent_index25'] is not None)
    processes = re.findall(r'^process (\d+) (\d+) flags:(.*?) blocks=(\d+)$', log, re.M)
    assert [(int(n), int(b), int(k)) for n, b, _, k in processes] == [(11264, 512, 22), (8192, 512, 16), (4096, 512, 8)]
    assert sum(int(k) for _, _, _, k in processes) == 46
    assert [(int(f), int(s, 16), int(a), int(b)) for f, s, a, b in re.findall(r'^event (\d+) (0x[0-9a-f]+) (\d+) (\d+)$', log, re.M)] == [tuple(e) for e in r['events']]
    bindings = {name: kind for kind, name in re.findall(r'^import (linux|data|trap) (\S+) slots=\d+$', log, re.M)}
    used = {name: int(n) for name, n in re.findall(r'^used (\S+) (\d+)$', log, re.M)}
    assert used and all(bindings.get(name) == 'linux' and n > 0 for name, n in used.items())
    return {'used_imports': used, 'binding_counts': {kind: list(bindings.values()).count(kind) for kind in ('linux', 'data', 'trap')},
            'process_records': [{'frames': int(n), 'block': int(b), 'flags_raw': flags, 'CalcA_calls': int(k)} for n, b, flags, k in processes],
            'direct_export_calls': r['direct_export_calls'], 'nested_calls': None}


def finite_peak(raw):
    assert len(raw) % 4 == 0
    assert all((word & 0x7f800000) != 0x7f800000 for (word,) in struct.iter_unpack('<I', raw))
    return max((abs(value) for (value,) in struct.iter_unpack('<f', raw)), default=0.0)


def run(config, expected_sha):
    raw_manifest = (HERE / 'manifest.json').read_bytes()
    assert hashlib.sha256(raw_manifest).hexdigest() == expected_sha
    manifest = json.loads(raw_manifest)
    assert manifest['status'] == 'FROZEN-BEFORE-ORIGINAL-CALLS'
    for row in manifest['files']:
        got = pin(HERE / row['path'])
        assert got['bytes'] == row['bytes'] and got['sha256'] == row['sha256']
    attempts = HERE / 'attempts'
    attempts.mkdir(exist_ok=False)
    result = {'schema': 'collision-whole12-one-attempt-results-v1', 'status': 'RUNNING', 'utc_start': utc(),
              'outer_pid': os.getpid(), 'outer_argv': sys.argv, 'python': sys.version, 'host': list(os.uname()),
              'environment': config['environment'], 'limits': config['limits'], 'children': [], 'error': None,
              'pre_call_manifest': {'bytes': len(raw_manifest), 'sha256': expected_sha, 'exact_utf8': raw_manifest.decode()},
              'group_stop_qualification': config['stop_semantics']}
    save('results.json', result)
    completed = {}
    try:
        before = custody(config)
        result['custody_before'] = before
        for r in config['inputs']:
            directory = attempts / r['id']
            directory.mkdir()
            argv = [config['runtime_expected'][0]['path'], config['runtime_expected'][1]['path'], str(ROOT / r['script']['path']), str(directory / 'output.f32'), '--imports']
            rec = {'id': r['id'], 'argv': argv, 'utc_start': utc(), 'pid': None, 'exit': None, 'timeout': False, 'cleanup': None}
            result['children'].append(rec)
            start = time.monotonic()
            with (directory / 'stdout.txt').open('xb') as stdout, (directory / 'stderr.txt').open('xb') as stderr:
                child = subprocess.Popen(argv, stdin=subprocess.DEVNULL, stdout=stdout, stderr=stderr, cwd=HERE,
                                         env=config['environment'], start_new_session=True, preexec_fn=limits)
                rec['pid'] = child.pid
                try:
                    rec['exit'] = child.wait(timeout=20)
                except subprocess.TimeoutExpired:
                    rec['timeout'] = True
                    os.killpg(child.pid, signal.SIGKILL)
                    rec['exit'] = child.wait(timeout=5)
                    rec['cleanup'] = 'Selected new process group killed/reaped; escaped descendants and uncatchable outer failures not proved covered'
            rec.update(utc_end=utc(), monotonic_seconds=time.monotonic() - start)
            for name in ('stdout.txt', 'stderr.txt', 'output.f32'):
                if (directory / name).exists():
                    rec[name] = pin(directory / name)
            save('results.json', result)
            assert rec['exit'] == 0 and not rec['timeout'], 'original child failed; no retries'
            assert rec['stderr.txt']['bytes'] == 0 and rec['output.f32']['bytes'] == 188416
            rec['projection'] = projection((directory / 'stdout.txt').read_text(), r)
            output = (directory / 'output.f32').read_bytes()
            rec['finite_peak_full'] = finite_peak(output)
            rec['prefix_before_setter_sha256'] = hashlib.sha256(output[:155648]).hexdigest()
            if r['sent_index25'] is not None:
                control = completed[r['matched_control_id']]
                assert output[:155648] == control[:155648], 'matched prefix differs: retain discovery, stop attribution/further attempts'
            elif r['initial_index25'] == 1:
                disabled = completed[f"initial0-no-setter-{r['context']}"]
                rec['productive_control'] = finite_peak(output[90112:155648]) > finite_peak(disabled[90112:155648])
                assert rec['productive_control'], 'productive enabled/disabled contrast absent'
            completed[r['id']] = output
            assert custody(config) == before, 'custody drift after child; stop'
            save('results.json', result)
            print(r['id'] + ' exit=0 bytes=188416', flush=True)
        result['custody_after'] = custody(config)
        assert result['custody_after'] == before
        result['status'] = 'COMPLETE-12-ONE-ATTEMPT-EACH'
    except BaseException as error:
        result['status'] = 'STOPPED-NO-RETRY'
        result['error'] = {'type': type(error).__name__, 'message': str(error)}
        try:
            result['custody_after_failure'] = custody(config)
        except BaseException as secondary:
            result['custody_failure'] = {'type': type(secondary).__name__, 'message': str(secondary)}
    result['utc_end'] = utc()
    save('results.json', result)
    assert result['status'] == 'COMPLETE-12-ONE-ATTEMPT-EACH', result['error']


if __name__ == '__main__':
    config = json.loads((HERE / 'inputs.json').read_text())
    validate(config)
    controls = synthetic(config)
    if sys.argv[1:] == ['--check']:
        print(json.dumps({'status': 'PASS', 'negative_controls': controls, 'original_calls': 0}, indent=2))
    else:
        assert len(sys.argv) == 3 and sys.argv[1] == '--run', 'use --check or --run PRECALL_MANIFEST_SHA; SHA is identity, standing task authorizes this whole batch'
        run(config, sys.argv[2])
