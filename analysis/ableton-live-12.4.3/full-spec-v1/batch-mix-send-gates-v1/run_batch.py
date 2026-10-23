"""One fixed25-call batch; --check-plan is data-only, --run-once never retries."""
import copy
import datetime
import hashlib
import itertools
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
ENTRY = '0x101b40d30'


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def identity(path):
    path = Path(path)
    h = hashlib.sha256()
    size = 0
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1048576), b''):
            h.update(block)
            size += len(block)
    return {'path': str(path), 'bytes': size, 'sha256': h.hexdigest()}


def put(path, value):
    with Path(path).open('x') as f:
        json.dump(value, f, indent=2)
        f.write('\n')
        f.flush()
        os.fsync(f.fileno())


def validate(catalog):
    rows = catalog['rows']
    assert len(rows) == 32 and len({r['id'] for r in rows}) == 32
    assert [r['context'] for r in rows] == ['identity-G'] * 16 + ['nonidentity-G'] * 16
    assert [r['boolean_bits'] for r in rows] == [list(b) for b in itertools.product((0, 1), repeat=4)] * 2
    assert sum(r['disposition'] == 'fresh-planned' for r in rows) == 25
    assert sum(r['disposition'] == 'inherited-not-executed' for r in rows) == 7
    known = {'identity-G': {'0111': 'retained-006', '1011': 'retained-008', '1101': 'retained-002', '1110': 'retained-010', '1111': 'retained-001'},
             'nonidentity-G': {'1101': 'retained-004', '1111': 'retained-003'}}
    for r in rows:
        w = [int(x, 16) for x in r['word_u32_hex']]
        assert len(w) == 13
        assert [w[i] for i in (0, 1, 2, 8)] == [0x3f800000 if b else 0 for b in r['boolean_bits']]
        assert w[3:8] == [0x3f000000, 0x3f666666, 0x3dcccccd, 0x3e4ccccd, 0x3f19999a]
        assert w[9:] == ([0x3f800000, 0, 0, 0x3f800000] if r['context'] == 'identity-G' else [0x3f000000, 0x3d4ccccd, 0x3d8f5c29, 0x3e800000])
        hx = struct.pack('<13I', *w).hex()
        assert r['input_hex'] == hx
        assert r['tokens'] == ['call', ENTRY, 'buf:8', 'hex:' + hx, 'buf:16', 'dump', 'b2', '16']
        bits = ''.join(map(str, r['boolean_bits']))
        assert r['id'] == r['context'] + '-' + bits
        if bits in known[r['context']]:
            assert r['disposition'] == 'inherited-not-executed'
            assert r['inherited_id'] == known[r['context']][bits]
        else:
            assert r['disposition'] == 'fresh-planned' and r['predicted_output'] is None
    assert [r['fresh_ordinal'] for r in rows if r['disposition'] == 'fresh-planned'] == list(range(1, 26))


def protocol(stdout, row):
    lines = stdout.decode('ascii').splitlines()
    assert lines[0] == 'loaded rebases=789951 binds-linux=103 binds-trap=42781 symbols=1882'
    imports, used, buffers, returned, dump = [], {}, {}, None, None
    for line in lines[1:]:
        if (m := re.fullmatch(r'import (linux|linux-data|trap) (\S+) slots=(\d+)', line)):
            imports.append({'binding': m[1], 'symbol': m[2], 'slots': int(m[3])})
        elif (m := re.fullmatch(r'call 0 ' + ENTRY + r' rax=0x([0-9a-f]+) rdx=0x([0-9a-f]+) xmm0=0x([0-9a-f]+) xmm1=0x([0-9a-f]+)', line)):
            assert returned is None
            returned = dict(zip(('rax', 'rdx', 'xmm0', 'xmm1'), (f'{int(x,16):016x}' for x in m.groups())))
            assert all(len(x) == 16 for x in returned.values())
        elif (m := re.fullmatch(r'out b([012]) (0x[0-9a-f]+) ([0-9a-f]+)', line)):
            assert m[1] not in buffers
            buffers[m[1]] = {'address': m[2], 'hex': m[3]}
        elif (m := re.fullmatch(r'dump b2 (0x[0-9a-f]+) ([0-9a-f]+)', line)):
            assert dump is None
            dump = {'address': m[1], 'hex': m[2]}
        elif (m := re.fullmatch(r'used (\S+) ([1-9][0-9]*)', line)):
            assert m[1] not in used
            used[m[1]] = int(m[2])
        else:
            raise AssertionError('Unexpected output line: ' + line[:180])
    assert len(imports) == 1882 and returned is not None
    assert set(buffers) == {'0', '1', '2'}
    assert len(buffers['0']['hex']) == 16
    assert buffers['1']['hex'] == row['input_hex']
    assert len(buffers['2']['hex']) == 32 and dump == buffers['2']
    assert used == {}, 'Unexpected actual imported-code use; stop later children'
    words = struct.unpack('<4I', bytes.fromhex(dump['hex']))
    assert all((w & 0x7f800000) != 0x7f800000 for w in words), 'Nonfinite output'
    return {'imports_bound_not_invoked': imports, 'actual_used_import_counts': used, 'return_lanes_u64_hex': returned,
            'buffers': buffers, 'output_hex': dump['hex'], 'output_u32_hex': [f'{x:08x}' for x in words],
            'output_all_finite': True, 'oracle_prediction': None}


def selfcheck(catalog):
    validate(catalog)
    failures = []
    changes = [('missing tuple', lambda c: c['rows'].pop()),
               ('duplicate tuple', lambda c: c['rows'].__setitem__(1, c['rows'][0])),
               ('wrong entry', lambda c: c['rows'][0]['tokens'].__setitem__(1, '0x1')),
               ('new constructor', lambda c: c['rows'][0]['tokens'].extend(['call', '0x1'])),
               ('wrong fixed gain', lambda c: c['rows'][0]['word_u32_hex'].__setitem__(3, '3f800000')),
               ('nonboolean gate', lambda c: c['rows'][0]['word_u32_hex'].__setitem__(0, '3f000000')),
               ('wrong group context', lambda c: c['rows'][16]['word_u32_hex'].__setitem__(9, '3f800000')),
               ('historical replay', lambda c: c['rows'][15].__setitem__('disposition', 'fresh-planned')),
               ('false inherited join', lambda c: c['rows'][0].__setitem__('disposition', 'inherited-not-executed')),
               ('fabricated oracle', lambda c: c['rows'][0].__setitem__('predicted_output', 'zeros')),
               ('arbitrary order', lambda c: c['rows'].reverse())]
    for name, change in changes:
        c = copy.deepcopy(catalog)
        change(c)
        try:
            validate(c)
        except (AssertionError, KeyError):
            failures.append(name)
        else:
            raise AssertionError('Negative control accepted: ' + name)
    return failures


def protocol_selfcheck(catalog):
    row = catalog['rows'][0]
    prefix = 'loaded rebases=789951 binds-linux=103 binds-trap=42781 symbols=1882\n'
    prefix += ''.join(f'import trap synthetic_{i} slots=1\n' for i in range(1882))
    tail = ('call 0 ' + ENTRY + ' rax=0x8 rdx=0x123 xmm0=0x0 xmm1=0x0\n'
            'out b0 0x111 0000000000000000\n'
            'out b1 0x222 ' + row['input_hex'] + '\n'
            'out b2 0x333 00000000000000000000000000000000\n'
            'dump b2 0x333 00000000000000000000000000000000\n')
    good = prefix + tail
    assert protocol(good.encode(), row)['output_all_finite']
    bad = {'missing import declaration': good.replace('import trap synthetic_0 slots=1\n', ''),
           'missing returned call': good.replace(tail.splitlines()[0] + '\n', ''),
           'duplicate returned call': good + tail.splitlines()[0] + '\n',
           'unexpected entry': good.replace('call 0 ' + ENTRY, 'call 0 0x1'),
           'bad dump pointer': good.replace('dump b2 0x333', 'dump b2 0x334'),
           'short output': good.replace('00000000000000000000000000000000', '00'),
           'nonfinite output': good.replace('00000000000000000000000000000000', '0000807f000000000000000000000000'),
           'unexpected actual import use': good + 'used synthetic_0 1\n',
           'fault text': good + 'FAULT sig=11\n',
           'patched model': good + 'patched 0x1 alloc32\n',
           'oversized returned lane': good.replace('rax=0x8 ', 'rax=0x10000000000000000 '),
           'input buffer mutation': good.replace(row['input_hex'], 'f' * 104)}
    rejected = []
    for name, text in bad.items():
        try:
            protocol(text.encode(), row)
        except (AssertionError, ValueError):
            rejected.append(name)
        else:
            raise AssertionError('Protocol negative accepted: ' + name)
    return rejected


def limits():
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    resource.setrlimit(resource.RLIMIT_FSIZE, (8388608, 8388608))


def main():
    catalog = json.loads((HERE / 'catalog.json').read_text())
    controls = selfcheck(catalog)
    protocol_controls = protocol_selfcheck(catalog)
    if sys.argv[1:] == ['--check-plan']:
        print(json.dumps({'status': 'PASS data-only fixed catalog and synthetic protocol', 'catalog_negative_controls': controls, 'protocol_negative_controls': protocol_controls, 'original_calls': 0}))
        return
    assert sys.argv[1:] == ['--run-once']
    assert not (HERE / 'results.jsonl').exists() and not (HERE / 'execution-summary.json').exists()
    plan = json.loads((HERE / 'execution-plan.json').read_text())
    pins = json.loads((HERE / 'authority-pins.json').read_text())
    pre = json.loads((HERE / 'pre-call-manifest.json').read_text())
    for p in pre['payloads']:
        assert identity(HERE / p['path']) == dict(p, path=str(HERE / p['path']))
    for pin in pins:
        assert identity(pin['path']) == pin, 'Authority mismatch: ' + pin['path']
    expected = {p['path']: p for p in pins}
    custody_paths = plan['runtime_custody_paths']
    fresh = [r for r in catalog['rows'] if r['disposition'] == 'fresh-planned']
    start = utc()
    completed = 0
    error = None
    with (HERE / 'results.jsonl').open('x') as output:
        for row in fresh:
            receipt = {'id': row['id'], 'planned_ordinal': row['fresh_ordinal'], 'started_utc': utc(), 'pid': None,
                       'argv': [plan['binary']['path'], plan['image']['path'], '--imports', *row['tokens']],
                       'environment': plan['environment'], 'stdin': 'DEVNULL', 'timeout_seconds': 20,
                       'new_session': True, 'core_limit': 0, 'retry': False, 'timed_out': False,
                       'cleanup': [], 'exit_status': None, 'error': None, 'protocol': None}
            before, after = [], []
            try:
                before = [identity(p) for p in custody_paths]
                assert all(p == expected[p['path']] for p in before), 'Prechild custody mismatch'
                stdout_path, stderr_path = [HERE / (row['id'] + suffix) for suffix in ('.stdout', '.stderr')]
                with stdout_path.open('xb') as out, stderr_path.open('xb') as err:
                    receipt['spawn_started_utc'] = utc()
                    child = subprocess.Popen(receipt['argv'], cwd=HERE, env=plan['environment'], stdin=subprocess.DEVNULL,
                                             stdout=out, stderr=err, start_new_session=True, preexec_fn=limits)
                    receipt['pid'] = child.pid
                    t0 = time.monotonic()
                    try:
                        receipt['exit_status'] = child.wait(timeout=20)
                    except subprocess.TimeoutExpired:
                        receipt['timed_out'] = True
                        for sig, bound in ((signal.SIGTERM, 1), (signal.SIGKILL, 1)):
                            try:
                                os.killpg(child.pid, sig)
                                receipt['cleanup'].append({'signal': sig.name, 'process_group': child.pid})
                            except ProcessLookupError:
                                receipt['cleanup'].append({'signal': sig.name, 'process_group_already_gone': True})
                            try:
                                receipt['exit_status'] = child.wait(timeout=bound)
                                break
                            except subprocess.TimeoutExpired:
                                pass
                    receipt['child_wall_seconds'] = time.monotonic() - t0
                    receipt['child_finished_utc'] = utc()
                    out.flush(); err.flush()
                    os.fsync(out.fileno()); os.fsync(err.fileno())
                receipt['stdout'] = identity(stdout_path)
                receipt['stderr'] = identity(stderr_path)
                assert receipt['exit_status'] == 0 and not receipt['timed_out'], 'Child failure'
                assert stderr_path.stat().st_size == 0, 'Nonempty stderr'
                assert stdout_path.stat().st_size <= 8388608, 'Oversized stdout'
                receipt['protocol'] = protocol(stdout_path.read_bytes(), row)
                # The result is retained verbatim before checking custody or attempting another child.
                raw_path = HERE / (row['id'] + '.raw')
                with raw_path.open('xb') as raw:
                    raw.write(bytes.fromhex(receipt['protocol']['output_hex']))
                    raw.flush(); os.fsync(raw.fileno())
                receipt['raw_output'] = identity(raw_path)
                completed += 1
            except Exception as exc:
                receipt['error'] = type(exc).__name__ + ': ' + str(exc)
            finally:
                try:
                    after = [identity(p) for p in custody_paths]
                    if not all(p == expected[p['path']] for p in after):
                        receipt['error'] = (receipt['error'] or '') + ' Postchild custody mismatch'
                except Exception as exc:
                    receipt['error'] = (receipt['error'] or '') + ' Postchild identity error: ' + repr(exc)
                receipt.update(before=before, after=after, finished_utc=utc())
                output.write(json.dumps(receipt) + '\n')
                output.flush(); os.fsync(output.fileno())
            print(json.dumps({'ordinal': row['fresh_ordinal'], 'id': row['id'], 'pid': receipt['pid'], 'rc': receipt['exit_status'], 'error': receipt['error']}), flush=True)
            if receipt['error']:
                error = receipt['error']
                break
    authority_after = [identity(p['path']) for p in pins]
    if authority_after != pins:
        error = (error or '') + ' Final authority custody mismatch'
    put(HERE / 'execution-summary.json', {'started_utc': start, 'finished_utc': utc(), 'outer_pid': os.getpid(),
                                       'authority_before': pins, 'authority_after': authority_after,
                                       'planned_children': 25, 'attempted_children': row['fresh_ordinal'],
                                       'successful_protocols': completed, 'error': error, 'retries': 0,
                                       'inherited_not_executed': 7, 'spawned_children': sum(json.loads(x)['pid'] is not None for x in (HERE / 'results.jsonl').read_text().splitlines()),
                                       'returned_direct_calls_with_valid_protocol': completed,
                                       'unattempted_ids': [r['id'] for r in fresh[row['fresh_ordinal']:]]})
    if error:
        raise SystemExit('Stopped; all existing history retained. No retry authorized.')


if __name__ == '__main__':
    main()
