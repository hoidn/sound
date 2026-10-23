"""Record the whole selected receiver-free M batch with the existing X2 loader.

No historical helper is imported. --self-check reads proposal data only;
--execute requires the separately retained Root selection digest, once.
"""
import copy
import ctypes
import datetime
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
BASE = HERE.parent
PROPOSAL = BASE / 'depth-automation-monotone-boundary-proposal-v1'
SELECT = BASE / 'reviews/automation-monotone-boundaries-root-actual-selection.json'
ENV = {'PATH': '/usr/bin:/bin', 'LANG': 'C', 'LC_ALL': 'C', 'TZ': 'UTC'}
PREFIX = ['/var/tmp/sound-analysis/xexec/x2-envelope-warp/xexec2',
          '/var/tmp/sound-analysis/helpers/Live_x86_64/Live_x86_64.x86_64', '--imports']
CALL = re.compile(r'call (\d+) (0x[0-9a-f]+) rax=(0x[0-9a-f]+) rdx=(0x[0-9a-f]+) xmm0=(0x[0-9a-f]+) xmm1=(0x[0-9a-f]+)')


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def identity(path):
    p = Path(path)
    h = hashlib.sha256()
    size = 0
    with p.open('rb') as f:
        for block in iter(lambda: f.read(1048576), b''):
            h.update(block)
            size += len(block)
    return {'path': str(p), 'bytes': size, 'sha256': h.hexdigest()}


def load(path):
    return json.loads(Path(path).read_text())


def write(name, obj):
    p = HERE / name
    with p.open('x') as f:
        json.dump(obj, f, indent=2, allow_nan=False)
        f.write('\n')
        f.flush()
        os.fsync(f.fileno())
    p.chmod(0o444)


def validate(vectors, processes):
    assert len(vectors) == 2138 and len(processes) == 17
    assert len({tuple(r['pair_binary64']) for r in vectors}) == 2138
    assert [p['native_calls'] for p in processes] == [128] * 16 + [90]
    assert [i for p in processes for i in p['vector_ids']] == [r['id'] for r in vectors]
    for r in vectors:
        assert len(r['tokens']) == 6 and r['tokens'][:2] == ['call', '0x1011f2080']
        assert all(t.startswith('d:') for t in r['tokens'][2:])
        assert r['arguments_binary64'] == ['0x0000000000000000', *r['pair_binary64'], '0x3ff0000000000000']
        assert r['expected_boolean'] is None or type(r['expected_boolean']) is bool
    assert [sum(r['expected_boolean'] is x for r in vectors) for x in [True, False, None]] == [578, 1301, 259]
    byid = {r['id']: r for r in vectors}
    for p in processes:
        assert p['argv_prefix'] == PREFIX
        argv = PREFIX + [t for i in p['vector_ids'] for t in byid[i]['tokens']]
        assert hashlib.sha256(json.dumps(argv, separators=(',', ':')).encode()).hexdigest() == p['argv_json_sha256']
        assert sum(len(t.encode()) + 1 for t in argv) == p['argv_utf8_bytes_with_NUL'] < 32768
    return byid


def parse_output(text, count):
    calls, imports, used, loaded = [], [], [], []
    for line in text.splitlines():
        m = CALL.fullmatch(line)
        if m:
            i, addr, *regs = m.groups()
            assert int(i) == len(calls) and addr == '0x1011f2080'
            calls.append({'index': int(i), 'address': addr, **dict(zip(['rax', 'rdx', 'xmm0', 'xmm1'], regs))})
        elif line.startswith('import '):
            imports.append(line)
        elif line.startswith('loaded '):
            loaded.append(line)
        elif line.startswith('used '):
            used.append(line)
        else:
            raise ValueError('unexpected output record: ' + line[:120])
    assert len(calls) == count and len(loaded) == 1
    return {'calls': calls, 'imports': imports, 'loaded': loaded, 'used': used}


def self_check():
    vectors = load(PROPOSAL / 'inputs.json')['vectors']
    processes = load(PROPOSAL / 'process-shapes.json')['processes']
    validate(vectors, processes)
    mutations = [lambda v, p: v.pop(), lambda v, p: p.pop(),
                 lambda v, p: p[-1]['vector_ids'].pop(),
                 lambda v, p: v[0]['tokens'].__setitem__(1, '0x102526870'),
                 lambda v, p: v[0]['tokens'].__setitem__(2, 'ref:object'),
                 lambda v, p: next(r for r in v if r['expected_boolean'] is None).update(expected_boolean=False),
                 lambda v, p: p[0]['argv_prefix'].__setitem__(0, '/wrong/loader'),
                 lambda v, p: p[0].update(argv_utf8_bytes_with_NUL=1)]
    for mutate in mutations:
        v, p = copy.deepcopy(vectors), copy.deepcopy(processes)
        mutate(v, p)
        try:
            validate(v, p)
        except AssertionError:
            pass
        else:
            raise AssertionError('invalid batch accepted')
    good = 'loaded test\ncall 0 0x1011f2080 rax=0x1 rdx=0x0 xmm0=0x0 xmm1=0x0\n'
    assert parse_output(good, 1)['calls'][0]['rax'] == '0x1'
    for bad, n in [(good, 2), (good.replace('call 0', 'call 1'), 1),
                   (good.replace('0x1011f2080', '0x10'), 1), (good + 'FAULT test\n', 1)]:
        try:
            parse_output(bad, n)
        except (AssertionError, ValueError):
            pass
        else:
            raise AssertionError('invalid receipt accepted')
    return {'status': 'PASS-data-only', 'vectors': 2138, 'processes': 17, 'negative_controls': 12,
            'original_calls': 0, 'image_loader_reads': 0}


def child_limits():
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    resource.setrlimit(resource.RLIMIT_FSIZE, (2097152, 2097152))


def execute(digest):
    assert len(digest) == 64 and identity(SELECT)['sha256'] == digest
    selected = load(SELECT)
    assert selected['selected_native_calls'] == 2138 and selected['selected_processes'] == 17
    assert selected['whole_withheld_factory_rows'] == 50 and selected['new_setup_or_model'] is False
    for pin in selected['gates']:
        assert identity(pin['path']) == pin
    manifest = load(PROPOSAL / 'manifest.json')
    assert identity(PROPOSAL / 'manifest.json')['sha256'] == 'c036d2e44c6f808e5796f67bf81a3b5c135cb9c2a3f50086f9bfb8ce46f6a46b'
    for pin in manifest['files']:
        actual = identity(PROPOSAL / pin['path'])
        assert all(actual[k] == pin[k] for k in ['bytes', 'sha256'])
    vectors = load(PROPOSAL / 'inputs.json')['vectors']
    processes = load(PROPOSAL / 'process-shapes.json')['processes']
    byid = validate(vectors, processes)
    assert sys.byteorder == 'little' and os.uname().machine == 'x86_64'
    assert sum(len(t.encode()) + 1 for t in ENV.values()) + 32768 + 8192 < os.sysconf('SC_ARG_MAX')
    os.umask(0o077)
    write('attempt.json', {'utc': utc(), 'outer_pid': os.getpid(), 'one_attempt_no_retry': True, 'selection': identity(SELECT)})
    binaries = [identity(p) for p in PREFIX[:2]]
    assert binaries == selected['binary_identities']
    libc = ctypes.CDLL(None)
    libc.strtod.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_void_p)]
    libc.strtod.restype = ctypes.c_double
    libc.gnu_get_libc_version.restype = ctypes.c_char_p
    conversions = {}
    for r in vectors:
        for token, expected in zip(r['tokens'][2:], r['arguments_binary64']):
            text = token[2:]
            buf = ctypes.create_string_buffer(text.encode('ascii'))
            end = ctypes.c_void_p()
            value = libc.strtod(buf, ctypes.byref(end))
            assert end.value == ctypes.addressof(buf) + len(text)
            raw = struct.pack('<d', value)
            assert '0x' + raw[::-1].hex() == expected
            conversions[token] = {'binary64_le': raw.hex(), 'temporary_float32_le': struct.pack('<f', ctypes.c_float(value).value).hex()}
    write('inputs.json', {'frozen_utc': utc(), 'vectors': vectors, 'processes': processes, 'native_calls': 2138,
                          'withheld_factory_rows': 50, 'NULL_retained': 259})
    write('host-context.json', {'utc': utc(), 'python': sys.version, 'uname': list(os.uname()),
                              'libc': libc.gnu_get_libc_version().decode(), 'conversions': conversions,
                              'full_consumption_and_all_argument_bits_checked': True, 'environment': ENV,
                              'limits': 'Host strtod/temporary-float bytes only; no child register/FP-mode trace or ARM equivalence.'})
    write('custody-before.json', {'utc': utc(), 'identities': binaries})
    sourcepaths = [SELECT, PROPOSAL / 'manifest.json', PROPOSAL / 'inputs.json', PROPOSAL / 'process-shapes.json',
                   ROOT / 'wiki/specs/automation-envelopes.md',
                   ROOT / 'analysis/ableton-live-12.4.3/r2/x2-envelope-warp-v1/xexec2.c']
    write('source-pins.json', {'pins': [identity(p) for p in sourcepaths], 'model': 'Inherited unchanged X2 loader/stubs, receiver-free four doubles, RAX&1 only. No new original setup.'})
    write('manifest-before.json', {'utc': utc(), 'original_calls_so_far': 0, 'maximum_processes': 17, 'native_calls': 2138,
                                  'payloads': [identity(HERE / n) for n in ['collect-once.py', 'inputs.json', 'host-context.json', 'custody-before.json', 'source-pins.json']]})
    print('Pre-call manifest frozen; whole2138 exact host arguments and image/loader custody PASS.', flush=True)
    (HERE / 'raw').mkdir()
    receipts, observations, mismatches = [], [], []
    stopped = None
    with (HERE / 'receipts.jsonl').open('x') as receiptfile:
        for p in processes:
            argv = PREFIX + [t for i in p['vector_ids'] for t in byid[i]['tokens']]
            start, mono = utc(), time.monotonic_ns()
            code, pid, timedout, error, parsed = None, None, False, None, None
            try:
                with (HERE / 'raw' / (p['id'] + '.stdout')).open('xb') as out, (HERE / 'raw' / (p['id'] + '.stderr')).open('xb') as err:
                    child = subprocess.Popen(argv, stdin=subprocess.DEVNULL, stdout=out, stderr=err, cwd=HERE,
                                             env=ENV, start_new_session=True, preexec_fn=child_limits)
                    pid = child.pid
                    try:
                        code = child.wait(timeout=20)
                    except subprocess.TimeoutExpired:
                        timedout = True
                        os.killpg(child.pid, signal.SIGKILL)
                        code = child.wait(timeout=5)
            except (OSError, subprocess.SubprocessError) as e:
                error = repr(e)
            outpath, errpath = [HERE / 'raw' / (p['id'] + '.' + x) for x in ['stdout', 'stderr']]
            for path in [outpath, errpath]:
                path.chmod(0o444)
            try:
                parsed = parse_output(outpath.read_text(encoding='ascii'), p['native_calls'])
            except (AssertionError, ValueError, UnicodeError) as e:
                error = repr(e)
            receipt = {'id': p['id'], 'argv': argv, 'pid': pid, 'start_utc': start, 'end_utc': utc(),
                       'start_monotonic_ns': mono, 'end_monotonic_ns': time.monotonic_ns(),
                       'exit_code': code, 'timeout': timedout, 'timeout_seconds': 20, 'error': error, 'retry': False,
                       'stdin': 'DEVNULL', 'environment': ENV, 'core_limit': 0, 'per_file_limit': 2097152,
                       'stdout': identity(outpath), 'stderr': identity(errpath), 'parsed': parsed}
            receiptfile.write(json.dumps(receipt) + '\n')
            receiptfile.flush()
            os.fsync(receiptfile.fileno())
            receipts.append(receipt)
            if parsed:
                for i, call in zip(p['vector_ids'], parsed['calls']):
                    expected = byid[i]['expected_boolean']
                    got = int(call['rax'], 16) & 1
                    observation = {'vector_id': i, 'observed_RAX_and_1': got, 'expected_boolean': expected,
                                   'comparison': 'ungraded-discovery' if expected is None else 'agree' if got == expected else 'mismatch'}
                    observations.append(observation)
                    if expected is not None and got != expected:
                        mismatches.append(observation)
            print(p['id'], pid, code, len(parsed['calls']) if parsed else None, flush=True)
            if code != 0 or timedout or error or receipt['stderr']['bytes'] or not parsed or parsed['used']:
                stopped = {'after': p['id'], 'reason': 'status/timeout/parse/stderr/import failure; no retry or remaining attempt'}
                break
    (HERE / 'receipts.jsonl').chmod(0o444)
    after = [identity(p) for p in PREFIX[:2]]
    write('custody-after.json', {'utc': utc(), 'identities': after, 'matches_before': after == binaries})
    write('analysis.json', {'status': 'COMPLETE' if not stopped and len(receipts) == 17 and after == binaries else 'PARTIAL_OR_CUSTODY_FAILURE',
                           'stopped': stopped, 'processes': len(receipts), 'returned_calls': len(observations),
                           'observations': observations, 'mismatches': mismatches,
                           'new_application_grades': 0, 'whole_withheld_factory_rows': 50,
                           'limits': 'Finite local x86 observations, no current event/provider/normalization/save/audio/ARM proof; no expectation repair or automatic successor.'})
    print(json.dumps({'processes': len(receipts), 'returned_calls': len(observations), 'mismatches': len(mismatches), 'custody_equal': after == binaries, 'stopped': stopped}), flush=True)


if __name__ == '__main__':
    if sys.argv[1:] == ['--self-check']:
        print(json.dumps(self_check()))
    elif len(sys.argv) == 3 and sys.argv[1] == '--execute':
        execute(sys.argv[2])
    else:
        raise SystemExit('Use --self-check or --execute <Root-selection-sha256>')
