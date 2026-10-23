#!/usr/bin/env python3
"""Ordinary recording of a whole existing one-double xexec call class; never builds/imports old helpers."""
import copy
import ctypes
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
TARGET = '0x10235b910'

def now():
    return datetime.now(timezone.utc).isoformat()

def identity(path):
    path = Path(path)
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return {'path': str(path.resolve()), 'bytes': path.stat().st_size, 'sha256': h.hexdigest()}

def save(path, value):
    with Path(path).open('w') as f:
        json.dump(value, f, indent=2, allow_nan=False)
        f.write('\n')
        f.flush()
        os.fsync(f.fileno())

def validate(config):
    rows = config['rows']
    assert config['target'] == TARGET and config['counts'] == {'calls': 117, 'processes': 117, 'control_pairs': 8, 'new_discovery_pairs': 109}
    assert len(rows) == 117 and [r['id'] for r in rows] == [f'PQ{i:04d}' for i in range(1, 118)]
    assert len({r['input_binary64_hex'] for r in rows}) == 117
    assert sum(r['expected_output_binary64_hex'] is not None for r in rows) == 8
    assert sum(r['historical_source'] is not None for r in rows) == 8
    assert {r['input_binary64_hex'] for r in rows if 'NaN' in ' '.join(r['classes'])} == {'7ff8000000000000', 'fff8000000000000'}
    for r in rows:
        assert len(r['input_binary64_hex']) == 16
        assert bytes.fromhex(r['input_binary64_hex'])[::-1].hex() == r['input_bytes_le_hex']
        assert r['token'].startswith('d:') and len(r['token']) < 80 and r['classes']
        assert (r['expected_output_binary64_hex'] is None) == (r['expected_kind'] == 'NULL-discovery')
        assert r['expected_output_binary64_hex'] is None or len(r['expected_output_binary64_hex']) == 16
    return True

def parser_check(rows):
    # Same installed libc entry used by the unchanged loader; no original program call.
    libc = ctypes.CDLL(None)
    libc.strtod.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_void_p)]
    libc.strtod.restype = ctypes.c_double
    result = []
    for r in rows:
        raw = r['token'][2:].encode('ascii')
        buf = ctypes.create_string_buffer(raw)
        end = ctypes.c_void_p()
        value = libc.strtod(ctypes.cast(buf, ctypes.c_char_p), ctypes.byref(end))
        parsed = struct.pack('>d', value).hex()
        consumed = end.value - ctypes.addressof(buf)
        assert consumed == len(raw) and parsed == r['input_binary64_hex'], r['id']
        result.append({'id': r['id'], 'token': r['token'], 'parsed_binary64_hex': parsed, 'characters_consumed': consumed})
    return result

def controls(config):
    rejected = []
    for label, mutate in [
        ('omit-final-vector', lambda c: c['rows'].pop()),
        ('duplicate-bitpair', lambda c: c['rows'][1].update(input_binary64_hex=c['rows'][0]['input_binary64_hex'])),
        ('wrong-endian', lambda c: c['rows'][0].update(input_bytes_le_hex='0100000000000000')),
        ('missing-known-control', lambda c: c['rows'][0].update(expected_output_binary64_hex=None)),
        ('wrong-target', lambda c: c.update(target='0x0')),
        ('firstN-cap-truncation', lambda c: c['counts'].update(calls=6))]:
        changed = copy.deepcopy(config)
        mutate(changed)
        try:
            validate(changed)
        except AssertionError:
            rejected.append(label)
        else:
            raise AssertionError('Control accepted: ' + label)
    broken = copy.deepcopy(config['rows'][:1])
    broken[0]['token'] = 'd:1.0junk'
    try:
        parser_check(broken)
    except AssertionError:
        rejected.append('parser-trailing-junk')
    else:
        raise AssertionError('Parser junk accepted')
    return rejected

def custody(context):
    observed = []
    for pin in context['source_pins'] + context['runtime_expected']:
        actual = identity(pin['path'])
        assert all(actual[k] == pin[k] for k in ('bytes', 'sha256')), pin['path']
        observed.append(actual)
    observed += [identity(HERE / n) for n in ('inputs.json', 'context.json', 'run_batch.py', 'analyze.py')]
    return observed

def limits():
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    resource.setrlimit(resource.RLIMIT_CPU, (20, 20))
    resource.setrlimit(resource.RLIMIT_FSIZE, (1048576, 1048576))

def returned(out, err, rc):
    assert rc == 0 and not err
    assert not re.search(r'(?m)^(?:TRAP|FAULT|xexec:|HIT)', out + err)
    calls = re.findall(r'^call (\d+) (0x[0-9a-f]+) rax=(0x[0-9a-f]+) rdx=(0x[0-9a-f]+) xmm0=(0x[0-9a-f]+) xmm1=(0x[0-9a-f]+)$', out, re.M)
    assert len(calls) == 1 and calls[0][:2] == ('0', TARGET)
    assert not re.search(r'(?m)^(?:used|out|dump|poke) ', out), 'unexpected import use/setup/output'
    return {k: f'{int(v,16):016x}' for k, v in zip(('rax', 'rdx', 'xmm0', 'xmm1'), calls[0][2:])}

def main():
    config = json.loads((HERE / 'inputs.json').read_text())
    context = json.loads((HERE / 'context.json').read_text())
    validate(config)
    checks = controls(config)
    parser = parser_check(config['rows'])
    if sys.argv[1:] == ['--check-data']:
        print(json.dumps({'status': 'PASS', 'input_rows': 117, 'negative_controls': checks, 'strtod_bits': 117, 'original_calls': 0, 'binary_custody_reads': 0}))
        return
    assert sys.argv[1:] == ['--run']
    attempts = HERE / 'attempts'
    attempts.mkdir(exist_ok=False)
    result = {'schema': 'whole-playback-one-double-actual-v1', 'status': 'RUNNING', 'utc_start': now(), 'outer_pid': os.getpid(), 'outer_argv': sys.argv, 'python': sys.version, 'sys_flags': str(sys.flags), 'host': list(os.uname()), 'environment': context['environment'], 'input_controls': checks, 'strtod_argument_bits': parser, 'children': [], 'error': None}
    save(HERE / 'results.json', result)
    try:
        result['custody_before'] = custody(context)
        save(HERE / 'results.json', result)
        for r in config['rows']:
            directory = attempts / r['id']
            directory.mkdir()
            argv = [context['runtime_expected'][1]['path'], context['runtime_expected'][0]['path'], '--imports', 'call', TARGET, r['token']]
            child = {'id': r['id'], 'argv': argv, 'utc_start': now(), 'pid': None, 'timeout': False, 'exit': None, 'cleanup': None}
            result['children'].append(child)
            started = time.monotonic()
            p = None
            try:
                with (directory / 'stdout.txt').open('xb') as out, (directory / 'stderr.txt').open('xb') as err:
                    p = subprocess.Popen(argv, stdin=subprocess.DEVNULL, stdout=out, stderr=err, cwd=HERE, env=context['environment'], preexec_fn=limits, start_new_session=True)
                    child['pid'] = p.pid
                    try:
                        child['exit'] = p.wait(timeout=20)
                    except subprocess.TimeoutExpired:
                        child['timeout'] = True
                        os.killpg(p.pid, signal.SIGKILL)
                        child['exit'] = p.wait(timeout=5)
                        child['cleanup'] = 'selected group SIGKILL, child reaped; escaped descendants/uncatchable outer death not proved'
            finally:
                if p is not None and p.poll() is None:
                    os.killpg(p.pid, signal.SIGKILL)
                    child['exit'] = p.wait(timeout=5)
                    child['cleanup'] = 'selected group killed/reaped on interrupted wait'
                child.update(utc_end=now(), monotonic_seconds=time.monotonic() - started)
                child['stdout'] = identity(directory / 'stdout.txt')
                child['stderr'] = identity(directory / 'stderr.txt')
                save(HERE / 'results.json', result)
            assert not child['timeout']
            out = (directory / 'stdout.txt').read_text()
            err = (directory / 'stderr.txt').read_text()
            child['return_registers_hex'] = returned(out, err, child['exit'])
            child['projected_binary64_hex'] = child['return_registers_hex']['xmm0']
            child['control_match'] = None if r['expected_output_binary64_hex'] is None else child['projected_binary64_hex'] == r['expected_output_binary64_hex']
            save(HERE / 'results.json', result)
            assert child['control_match'] is not False, 'historical control mismatch; retain and stop'
            print(r['id'] + ' exit0 xmm0=' + child['projected_binary64_hex'], flush=True)
        result['custody_after'] = custody(context)
        assert result['custody_before'] == result['custody_after']
        result['status'] = 'COMPLETE-117-ONE-ATTEMPT-EACH'
    except BaseException as error:
        result['status'] = 'STOPPED-NO-RETRY'
        result['error'] = {'type': type(error).__name__, 'message': str(error)}
        try:
            result['custody_after_failure'] = custody(context)
        except BaseException as failure:
            result['custody_after_failure_error'] = str(failure)
        raise
    finally:
        result['utc_end'] = now()
        save(HERE / 'results.json', result)

if __name__ == '__main__':
    main()
