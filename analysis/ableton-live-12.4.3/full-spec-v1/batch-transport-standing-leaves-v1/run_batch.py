#!/usr/bin/env python3
"""Fixed complete Transport hash-word class, existing X2 model/stubs only."""
import copy
from datetime import datetime, timezone
import hashlib
import json
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
INIT, CONVERT = 0x1014206e0, 0x10151b630


def utc():
    return datetime.now(timezone.utc).isoformat()


def digest(path):
    raw = path.read_bytes()
    return {'path': str(path), 'resolved_path': str(path.resolve()),
            'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def save(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2) + '\n')


def validate(c):
    rows = [r for g in c['groups'] for r in g['conversions']]
    assert len(c['groups']) == 8 and len(rows) == 316
    assert len({(r['kind'], r['input_bytes_hex']) for r in rows}) == 316
    assert sum(r['historical_exact_kind_text_member'] for r in rows) == 3
    for g in c['groups']:
        F, width, tid = (23, 32, 18) if g['kind'] == 'float' else (52, 64, 23)
        assert len(g['conversions']) == F + 2
        assert [r['fraction_integer'] for r in g['conversions']] == [0] + [1 << i for i in range(F)] + [(1 << F) - 1]
        assert g['owned_buffers'] == len(g['conversions']) * 4 < 256
        assert g['direct_calls'] == len(g['conversions']) + 1 < 256
        expected_tokens = ['--imports', 'call', hex(INIT)]
        for i, r in enumerate(g['conversions']):
            word = (g['sign'] << (width - 1)) | (((1 << (width - F - 1)) - 1) << F) | r['fraction_integer']
            text = '#' + format(word, '0' + str(width // 4) + ('X' if g['hex_case'] == 'upper' else 'x'))
            assert r['text'] == text and r['input_bytes_hex'] == text.encode('ascii').hex()
            assert r['type_id'] == tid and r['width'] == width
            assert r['word_hex'] == format(word, '0' + str(width // 4) + 'x')
            assert r['expected_selected_bits_from_current_owner'] == r['word_hex']
            assert r['owned_buffer_indices'] == list(range(i * 4, i * 4 + 4))
            assert r['original_call_index'] == i + 1
            k = i * 4
            expected_tokens += ['mk', 'hex:' + struct.pack('<I', tid).hex(), 'mk', f'ptrs:0x106a4b178,b{k}',
                                'mk', 'hex:' + r['input_bytes_hex'] + '00', 'call', hex(CONVERT),
                                f'ref:b{k + 1}', f'ptrs:b{k + 2},{len(text)}']
        assert expected_tokens == g['tokens']
        p = ROOT / g['gdb_script']
        assert p.parent == HERE / 'scripts'
        assert all(digest(p)[k] == g['gdb_script_pin'][k] for k in ('bytes', 'sha256'))
        assert p.read_text().count('\nreturn\ncontinue\nend\n') == 4
    assert sum(g['direct_calls'] for g in c['groups']) == 324


def controls(c):
    passed = []
    for name, change in (
        ('omit-class-member', lambda x: x['groups'][0]['conversions'].pop()),
        ('wrong-type', lambda x: x['groups'][0]['conversions'][0].update(type_id=16)),
        ('canonicalized-payload', lambda x: x['groups'][0]['conversions'][1].update(word_hex='7fc00000')),
        ('altered-input-bytes', lambda x: x['groups'][0]['conversions'][0].update(input_bytes_hex='00')),
        ('wrong-original-argv', lambda x: x['groups'][0]['tokens'].__setitem__(2, '0x0')),
        ('overflow-buffer-count', lambda x: x['groups'][0].update(owned_buffers=256)),
        ('missing-case-group', lambda x: x['groups'].pop())):
        altered = copy.deepcopy(c)
        change(altered)
        try:
            validate(altered)
        except AssertionError:
            passed.append(name)
        else:
            raise AssertionError('Control accepted: ' + name)
    return passed


def custody(c):
    out = []
    for expected in c['source_pins'] + c['runtime_expected']:
        actual = digest(ROOT / expected['path'])
        assert actual['sha256'] == expected['sha256'], expected['path']
        if 'bytes' in expected:
            assert actual['bytes'] == expected['bytes']
        out.append(actual)
    for path in c['runtime_record_before_after']:
        out.append(digest(Path(path)))
    for g in c['groups']:
        out.append(digest(ROOT / g['gdb_script']))
    out += [digest(HERE / 'inputs.json'), digest(Path(__file__))]
    return out


def limits():
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    resource.setrlimit(resource.RLIMIT_CPU, (20, 20))
    resource.setrlimit(resource.RLIMIT_FSIZE, (4194304, 4194304))


def project(stdout, stderr, group):
    calls, hits, used = [], [], {}
    bindings = {}
    for line in stdout.splitlines():
        f = line.split()
        if not f:
            continue
        if f[0] == 'call':
            calls.append({'index': int(f[1]), 'address': f[2], 'raw_registers': dict(x.split('=') for x in f[3:])})
        elif f[0] == 'HIT':
            hits.append({'during_original_call_index': len(calls), 'address': f[1], 'unsigned_raw': f[2]})
        elif f[0] == 'used':
            used[f[1]] = int(f[2])
        elif f[0] == 'import':
            bindings[f[2]] = f[1]
    assert not re.search(r'(?m)^(TRAP|FAULT|xexec:)', stderr)
    assert 'Program received signal' not in stdout + stderr
    inferior = re.findall(r'\[Inferior (\d+) \(process (\d+)\) exited normally\]', stdout)
    assert len(inferior) == 1, 'No unique recorded normal inferior exit'
    assert [int(r['address'], 16) for r in calls] == [INIT] + [CONVERT] * len(group['conversions'])
    assert [r['index'] for r in calls] == list(range(group['direct_calls']))
    assert len(hits) == len(group['conversions'])
    observations = []
    for request, hit in zip(group['conversions'], hits):
        assert hit['during_original_call_index'] == request['original_call_index']
        assert hit['address'] == request['expected_SetValue_stub']
        width = request['width']
        raw = int(hit['unsigned_raw'], 16)
        selected = raw & ((1 << width) - 1)
        bits = format(selected, '0' + str(width // 4) + 'x')
        observations.append({'id': request['id'], 'kind': request['kind'], 'input_bytes_hex': request['input_bytes_hex'],
                             'type_id': request['type_id'], 'input_word_hex': request['word_hex'],
                             'setter_stub': hit['address'], 'raw_unsigned_HIT': hit['unsigned_raw'],
                             'selected_typed_bits_hex': bits, 'selected_typed_bytes_le': selected.to_bytes(width // 8, 'little').hex(),
                             'owner_expected_bits': request['expected_selected_bits_from_current_owner'],
                             'owner_bit_oracle_agreement': bits == request['expected_selected_bits_from_current_owner'],
                             'candidate_grade': None})
    assert all(bindings.get(name) in ('linux', 'linux-data') for name in used)
    return {'inferior_id': int(inferior[0][0]), 'inferior_pid': int(inferior[0][1]),
            'inferior_exit_evidence': 'GDB normal-exit record, distinct from debugger OS return code',
            'calls': calls, 'HITs': hits, 'used_imports': used, 'import_binding_classes': bindings,
            'observations': observations}


def main(c):
    attempts = HERE / 'attempts'
    attempts.mkdir(exist_ok=False)
    result = {'status': 'RUNNING', 'utc_start': utc(), 'outer_pid': os.getpid(), 'outer_argv': sys.argv,
              'python': sys.version, 'host': list(os.uname()), 'environment': c['environment'],
              'limits': c['limits'], 'groups': [], 'error': None, 'stop_semantics': c['stop_semantics']}
    save('results.json', result)
    try:
        result['custody_before'] = custody(c)
        for group in c['groups']:
            d = attempts / group['id']
            d.mkdir()
            argv = ['/usr/bin/gdb', '-q', '-batch', '-nx', '-x', str(ROOT / group['gdb_script']), '--args',
                    c['runtime_expected'][0]['path'], c['runtime_expected'][1]['path'], *group['tokens']]
            record = {'id': group['id'], 'argv': argv, 'utc_start': utc(), 'debugger_pid': None,
                      'debugger_exit': None, 'timeout': False, 'cleanup': None}
            result['groups'].append(record)
            start = time.monotonic()
            with (d / 'stdout.txt').open('xb') as out, (d / 'stderr.txt').open('xb') as err:
                p = subprocess.Popen(argv, cwd=HERE, env=c['environment'], stdin=subprocess.DEVNULL,
                                     stdout=out, stderr=err, start_new_session=True, preexec_fn=limits)
                record['debugger_pid'] = p.pid
                try:
                    record['debugger_exit'] = p.wait(timeout=20)
                except BaseException as error:
                    record['timeout'] = isinstance(error, subprocess.TimeoutExpired)
                    os.killpg(p.pid, signal.SIGKILL)
                    record['debugger_exit'] = p.wait(timeout=5)
                    record['cleanup'] = 'Selected new group SIGKILL/reaped; escaped descendants/uncatchable outer death not proven covered'
                    raise
                finally:
                    record.update(utc_end=utc(), monotonic_seconds=time.monotonic() - start)
            record['stdout'], record['stderr'] = digest(d / 'stdout.txt'), digest(d / 'stderr.txt')
            save('results.json', result)
            assert record['debugger_exit'] == 0 and not record['timeout']
            record['projection'] = project((d / 'stdout.txt').read_text(), (d / 'stderr.txt').read_text(), group)
            print(group['id'] + ' converter_calls=' + str(len(record['projection']['observations'])) + ' normal-inferior-exit', flush=True)
            save('results.json', result)
        result['custody_after'] = custody(c)
        assert result['custody_before'] == result['custody_after']
        result['status'] = 'COMPLETE-WHOLE-316-ONE-ATTEMPT-PER-GROUP'
    except BaseException as error:
        result['status'] = 'STOPPED-NO-RETRY'
        result['error'] = {'type': type(error).__name__, 'message': str(error)}
        try:
            result['custody_after_failure'] = custody(c)
        except BaseException as failure:
            result['custody_after_failure_error'] = str(failure)
        raise
    finally:
        result['utc_end'] = utc()
        save('results.json', result)


if __name__ == '__main__':
    assert len(sys.argv) == 2 and sys.argv[1] in ('--check-inputs', '--run')
    config = json.loads((HERE / 'inputs.json').read_text())
    validate(config)
    checked = controls(config)
    if sys.argv[1] == '--check-inputs':
        print(json.dumps({'status': 'PASS', 'input_strings': 316, 'author_negatives': checked, 'original_invocations': 0}))
    else:
        main(config)
