#!/usr/bin/env python3
"""One whole Analog P1 sweep through the unchanged recorded xdev factory model."""
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
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]


def utc():
    return datetime.now(timezone.utc).isoformat()


def digest(path):
    raw = path.read_bytes()
    return {'path': str(path), 'resolved_path': str(path.resolve()), 'bytes': len(raw),
            'sha256': hashlib.sha256(raw).hexdigest()}


def save(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2, allow_nan=False) + '\n')


def validate(config):
    records = config['inputs']
    selected = config['whole_class']['new_single_control_vectors']
    assert len(records) == 21 and len(selected) == 20
    assert len({r['id'] for r in records}) == 21
    assert records[0]['change'] is None and [r['change'] for r in records[1:]] == selected
    assert {(r['host_index'], r['host_value']) for r in selected} == {
        (i, v) for i in (89, 101, 172, 184) for v in (1, 2, 3)} | {
        (i, 1) for i in (90, 91, 102, 103, 173, 174, 185, 186)}
    base = (ROOT / config['baseline_source']).read_text()
    for r in records:
        script = ROOT / r['script']['path']
        assert script.parent == HERE / 'scripts'
        assert all(digest(script)[k] == r['script'][k] for k in ('bytes', 'sha256'))
        lines = script.read_text().splitlines()
        params = [l.split() for l in lines if l.startswith('param ')]
        assert [int(p[1]) for p in params] == list(range(203))
        bits = [struct.pack('<f', float(p[2])).hex() for p in params]
        assert bits == r['parameter_f32_bits_le']
        assert hashlib.sha256(bytes.fromhex(''.join(bits))).hexdigest() == r['parameter_vector_sha256']
        assert float(params[99][2]) == 1.0
        expected = base
        if r['change']:
            c = r['change']
            old = next(l for l in base.splitlines() if l.startswith('param ' + str(c['host_index']) + ' '))
            expected = base.replace(old + '\n', 'param ' + str(c['host_index']) + ' ' + str(c['host_value']) + '\n')
        assert script.read_text() == expected
        assert lines[:2] == ['create', 'rate 44100']
        assert lines[-6:] == ['event 4400 0x90 60 100', 'event 35270 0x80 60 64', 'inflag 0', 'input zero', 'process 44100 512', 'destroy']
        assert len(lines) == 211
    assert config['limits']['direct_export_each'] == 1 + 1 + 203 + math.ceil(44100 / 512) + 1 == 293
    assert config['limits']['direct_export_total'] == 293 * 21 == 6153
    assert config['limits']['output_bytes_total'] == 44100 * 8 * 21 == 7408800
    return True


def synthetic(config):
    import copy
    passed = []
    for name, mutation in (
        ('omit-one-vector', lambda c: c['inputs'].pop()),
        ('duplicate-id', lambda c: c['inputs'][1].update(id=c['inputs'][0]['id'])),
        ('wrong-mode-alphabet', lambda c: c['whole_class']['new_single_control_vectors'][0].update(host_value=4)),
        ('wrong-binary32-vector', lambda c: c['inputs'][0]['parameter_f32_bits_le'].__setitem__(0, '00000000')),
        ('wrong-script-pin', lambda c: c['inputs'][0]['script'].update(sha256='0' * 64)),
        ('wrong-direct-call-bound', lambda c: c['limits'].update(direct_export_each=256))):
        altered = copy.deepcopy(config)
        mutation(altered)
        try:
            validate(altered)
        except AssertionError:
            passed.append(name)
        else:
            raise AssertionError('Synthetic control accepted: ' + name)
    return passed


def custody(config):
    records = []
    for expected in config['source_pins'] + config['runtime_expected']:
        actual = digest(ROOT / expected['path'])
        assert all(actual[k] == expected[k] for k in ('bytes', 'sha256')), expected['path']
        if 'resolved_path' in expected:
            assert actual['resolved_path'] == expected['resolved_path']
        records.append(actual)
    original = config['bundle_slice_expected']
    raw = Path(original['path']).read_bytes()
    selected = raw[original['x86_64_offset']:original['x86_64_offset'] + original['x86_64_size']]
    assert len(selected) == original['x86_64_size'] and hashlib.sha256(selected).hexdigest() == original['x86_64_sha256']
    records.append({'path': original['path'], 'selected_slice_offset': original['x86_64_offset'],
                    'bytes': len(selected), 'sha256': hashlib.sha256(selected).hexdigest()})
    records += [digest(HERE / 'inputs.json'), digest(Path(__file__)), digest(Path(sys.executable))]
    return records


def child_limits():
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    resource.setrlimit(resource.RLIMIT_CPU, (20, 20))
    resource.setrlimit(resource.RLIMIT_FSIZE, (1048576, 1048576))


def main(config):
    # Exclusive attempt directory prevents accidental replay, including after failures.
    attempts = HERE / 'attempts'
    attempts.mkdir(exist_ok=False)
    result = {'schema': 'analog-P1-one-sweep-results-v1', 'status': 'RUNNING', 'utc_start': utc(),
              'outer_pid': os.getpid(), 'outer_argv': sys.argv, 'python': sys.version,
              'host': list(os.uname()), 'environment': config['environment'],
              'limits': config['limits'], 'children': [], 'error': None}
    save('results.json', result)
    try:
        result['custody_before'] = custody(config)
        for r in config['inputs']:
            d = attempts / r['id']
            d.mkdir()
            argv = ['/var/tmp/sound-analysis/t12-analog/xdev', config['bundle_slice_expected']['path'],
                    str(ROOT / r['script']['path']), str(d / 'output.f32'), '--imports']
            record = {'id': r['id'], 'argv': argv, 'utc_start': utc(), 'pid': None,
                      'timeout': False, 'exit': None, 'cleanup': None}
            result['children'].append(record)
            started = time.monotonic()
            with (d / 'stdout.txt').open('xb') as stdout, (d / 'stderr.txt').open('xb') as stderr:
                p = subprocess.Popen(argv, stdin=subprocess.DEVNULL, stdout=stdout, stderr=stderr,
                                     cwd=HERE, env=config['environment'], start_new_session=True,
                                     preexec_fn=child_limits)
                record['pid'] = p.pid
                try:
                    record['exit'] = p.wait(timeout=20)
                except subprocess.TimeoutExpired:
                    record['timeout'] = True
                    os.killpg(p.pid, signal.SIGKILL)
                    record['exit'] = p.wait(timeout=5)
                    record['cleanup'] = 'SIGKILL issued to selected new process group; child reaped; escaped descendants/uncatchable outer death not proved covered'
            record.update(utc_end=utc(), monotonic_seconds=time.monotonic() - started)
            record['stdout'] = digest(d / 'stdout.txt')
            record['stderr'] = digest(d / 'stderr.txt')
            if (d / 'output.f32').exists():
                record['output'] = digest(d / 'output.f32')
            save('results.json', result)
            log = (d / 'stdout.txt').read_text()
            assert not record['timeout'] and record['exit'] == 0, 'original child failed'
            assert record['stderr']['bytes'] == 0 and record['output']['bytes'] == 352800
            assert 'create ok\n' in log and 'cxx-failbits 0\n' in log
            assert not re.search(r'(?im)^(?:TRAP|FAULT|xdev:)', log)
            assert 'process 44100 512 flags:' in log and 'blocks=87\n' in log
            assert len(re.findall(r'^param ', log, re.M)) == 203
            record['used_imports'] = dict((name, int(count)) for name, count in re.findall(r'^used (\S+) (\d+)$', log, re.M))
            print(r['id'] + ' exit=0 bytes=352800', flush=True)
        result['custody_after'] = custody(config)
        assert result['custody_before'] == result['custody_after']
        result['status'] = 'COMPLETE-21-ONE-ATTEMPT-EACH'
    except BaseException as error:
        result['status'] = 'STOPPED-NO-RETRY'
        result['error'] = {'type': type(error).__name__, 'message': str(error)}
        try:
            result['custody_after_failure'] = custody(config)
        except BaseException as custody_error:
            result['custody_after_failure_error'] = str(custody_error)
        raise
    finally:
        result['utc_end'] = utc()
        save('results.json', result)


if __name__ == '__main__':
    assert len(sys.argv) == 2 and sys.argv[1] in ('--check-inputs', '--run')
    config = json.loads((HERE / 'inputs.json').read_text())
    validate(config)
    guards = synthetic(config)
    if sys.argv[1] == '--check-inputs':
        print(json.dumps({'status': 'PASS', 'inputs': 21, 'negative_controls': guards,
                          'original_calls': 0, 'image_runtime_reads': 0}))
    else:
        main(config)
