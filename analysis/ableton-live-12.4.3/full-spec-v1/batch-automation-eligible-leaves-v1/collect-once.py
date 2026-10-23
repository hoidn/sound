"""One selected existing-loader batch; no imported historical helper or build.

--check reads retained data only. --execute is one attempt, guarded by an
exclusive marker. Inputs and host parser/custody manifest are frozen first.
"""
import argparse
import copy
import ctypes
import datetime
import hashlib
import json
import math
import os
from pathlib import Path
import re
import resource
import struct
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
BASE = ROOT / 'analysis/ableton-live-12.4.3/full-spec-v1'
X2 = ROOT / 'analysis/ableton-live-12.4.3/r2/x2-envelope-warp-v1'
T14 = ROOT / 'analysis/ableton-live-12.4.3/r2/t14-mix-v1'
ASSESS = BASE / 'reviews/automation-next-whole-batch-selection.json'
SELECT = BASE / 'reviews/automation-eligible-leaves-root-actual-selection.json'
ENV = {'PATH': '/usr/bin:/bin', 'LC_ALL': 'C', 'LANG': 'C', 'TZ': 'UTC'}
CALL = re.compile(r'^call (\d+) (0x[0-9a-f]+) rax=(0x[0-9a-f]+) rdx=(0x[0-9a-f]+) xmm0=(0x[0-9a-f]+) xmm1=(0x[0-9a-f]+)$')


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def identity(path):
    path = Path(path)
    h = hashlib.sha256()
    n = 0
    with path.open('rb') as f:
        for b in iter(lambda: f.read(1024 * 1024), b''):
            h.update(b)
            n += len(b)
    return {'path': str(path), 'bytes': n, 'sha256': h.hexdigest()}


def write(name, obj):
    path = HERE / name
    with path.open('x', encoding='utf-8') as f:
        json.dump(obj, f, indent=2, allow_nan=False)
        f.write('\n')
        f.flush()
        os.fsync(f.fileno())
    path.chmod(0o444)


def load(path):
    return json.loads(Path(path).read_text())


def parse_output(text):
    result = {'calls': [], 'dumps': [], 'used': {}, 'imports': [], 'loaded': []}
    for line in text.splitlines():
        m = CALL.fullmatch(line)
        if m:
            i, addr, *regs = m.groups()
            result['calls'].append({'index': int(i), 'address': addr,
                                    **dict(zip(['rax', 'rdx', 'xmm0', 'xmm1'], regs))})
        elif line.startswith('call '):
            raise ValueError('malformed call record')
        elif line.startswith('dump '):
            _, expr, addr, raw = line.split()
            result['dumps'].append({'expression': expr, 'address': addr, 'hex': raw})
        elif line.startswith('used '):
            _, symbol, count = line.split()
            result['used'][symbol] = int(count)
        elif line.startswith('import '):
            result['imports'].append(line)
        elif line.startswith('loaded '):
            result['loaded'].append(line)
    return result


def valid_inputs(rows):
    if len(rows) != 11 or [r['leaf'] for r in rows] != ['monotone', 'bezier'] + ['segment'] * 9:
        return False
    counts = [sum(t == 'call' for t in r['tokens']) for r in rows]
    if counts != [10, 15] + [1] * 9:
        return False
    for r in rows:
        if any(t in ('init', 'mkbuf', 'poke', 'poked', '--patch', 's:0') or t.startswith('--patch') for t in r['tokens']):
            return False
    a = rows[0]['tokens']
    if any(a[i:i + 2] != ['call', '0x1011f2080'] or len(a[i:i + 6]) != 6
           or not all(t.startswith('d:') for t in a[i + 2:i + 6]) for i in range(0, len(a), 6)):
        return False
    return len(a) == 60 and rows[0]['expected_boolean'] == [1, 1, 0, 1] + [0] * 6


def check():
    rows = load(HERE / 'inputs.json')['processes']
    assert valid_inputs(rows)
    negatives = []
    for kind in range(8):
        r = copy.deepcopy(rows)
        if kind == 0: r.pop()
        if kind == 1: r[0]['tokens'] = r[0]['tokens'][:36]
        if kind == 2: r[0]['expected_boolean'][4] = 1
        if kind == 3: r[1]['tokens'].extend(['call', '0x1011f1610', 'd:0', 'ref:b0'])
        if kind == 4: r[0]['tokens'][1] = '0x102526870'
        if kind == 5: r[2]['tokens'].insert(0, '--patch')
        if kind == 6: r[0]['leaf'] = 'float'
        if kind == 7: r[0]['tokens'][2] = 'ref:b0'
        assert not valid_inputs(r)
        negatives.append(kind)
    assert len(parse_output('call 0 0x10 rax=0x1 rdx=0x0 xmm0=0x0 xmm1=0x0\n')['calls']) == 1
    try:
        parse_output('call broken\n')
    except ValueError:
        negatives.append('malformed-call')
    else:
        raise AssertionError('malformed call accepted')
    before = load(HERE / 'manifest-before.json')
    for p in before['payloads']:
        assert identity(p['path']) == p
    receipts = [json.loads(s) for s in (HERE / 'receipts.jsonl').read_text().splitlines()]
    assert len(receipts) == 11
    for r, p in zip(rows, receipts):
        assert p['id'] == r['id'] and p['argv'][3:] == r['tokens']
        assert p['exit_code'] == 0 and not p['timeout'] and not p['stderr_bytes']
        for k in ['stdout', 'stderr']:
            assert identity(p[k]['path']) == p[k]
        parsed = parse_output(Path(p['stdout']['path']).read_text())
        assert parsed == p['parsed'] and not parsed['used']
    after = load(HERE / 'custody-after.json')
    assert after['identities'] == load(HERE / 'custody-before.json')['identities']
    analysis = load(HERE / 'analysis.json')
    assert analysis['native_calls'] == 34 and analysis['auxiliary_endpoints'] == 2
    assert analysis['new_application_grades'] == 0
    return {'status': 'PASS', 'negative_controls_rejected': len(negatives),
            'process_receipts': len(receipts), 'direct_calls': 34,
            'pre_call_payload_pins': len(before['payloads']),
            'comparison_findings': len(analysis['mismatches']),
            'method': 'data-only structure/hash/receipt checks; mismatch is retained, never changed into pass'}


def execute():
    os.umask(0o077)
    marker = os.open(HERE / 'attempt.json', os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o400)
    with os.fdopen(marker, 'w') as f:
        json.dump({'started_utc': utc(), 'outer_pid': os.getpid(), 'one_attempt_no_retry': True}, f)
        f.write('\n')
    selection = load(SELECT)
    assert identity(SELECT)['sha256'] == '2b354933a7fefa587e1b15d20522e5f5d7c16b5e4c9b9fa5925ebd826f96cfcc'
    assert identity(ASSESS)['sha256'] == 'ddd1bf2ebdcf7c836bb3f0fb1296abce72392b7660d10df857c42f46f5bd8b1a'
    a = load(ASSESS)
    inputs = a['input_universe']
    raw = [json.loads(s) for s in (T14 / 'raw/runs.jsonl').read_text().splitlines()]
    m = inputs['monotone']
    rows = [{'id': '01-monotone', 'leaf': 'monotone', 'tokens': sum([r['tokens'] for r in m['retained_finite_vectors'] + m['prospective_vectors']], []),
             'expected_boolean': [1, 1, 0, 1] + [0] * 6}]
    rows.append({'id': '02-bezier', 'leaf': 'bezier', 'tokens': raw[77]['argv'][1:],
                 'historical_scoped_output': parse_output(raw[77]['stdout'])})
    for i, s in enumerate(inputs['ideal_segments']['selected_records'], 3):
        rows.append({'id': f'{i:02d}-segment-{s["raw_locator"]["line"]}', 'leaf': 'segment', 'tokens': s['tokens'],
                     'historical_scoped_output': parse_output(raw[s['raw_locator']['line'] - 1]['stdout'])})
    assert valid_inputs(rows)
    image = selection['image']
    xloader = {'path': selection['loader_identities']['monotone_path'], 'sha256': selection['loader_identities']['monotone_sha256']}
    tloader = {'path': selection['loader_identities']['bezier_segment_path'], 'bytes': selection['loader_identities']['bezier_segment_bytes'], 'sha256': selection['loader_identities']['bezier_segment_sha256']}
    binaries = [identity(p['path']) for p in [image, xloader, tloader]]
    for expected, actual in zip([image, xloader, tloader], binaries):
        assert all(actual[k] == v for k, v in expected.items()), (expected, actual)
    libc = ctypes.CDLL(None)
    strtod = libc.strtod
    strtod.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_void_p)]
    strtod.restype = ctypes.c_double
    libc.gnu_get_libc_version.restype = ctypes.c_char_p
    conversions = {}
    for row in rows:
        row['argument_bits'] = []
        for pos, token in enumerate(row['tokens']):
            if token.startswith(('d:', 'f:')):
                text = token[2:]
                buf = ctypes.create_string_buffer(text.encode('ascii'))
                end = ctypes.c_void_p()
                value = strtod(buf, ctypes.byref(end))
                assert end.value == ctypes.addressof(buf) + len(text)
                double_bytes = struct.pack('<d', value)
                parsed_python = float.fromhex(text) if '0x' in text.lower() else float(text)
                assert double_bytes == struct.pack('<d', parsed_python)
                temporary_float = ctypes.c_float(value).value
                float_bytes = struct.pack('<f', temporary_float)
                chosen = double_bytes if token[0] == 'd' else float_bytes
                bits = {'token': token, 'token_index': pos, 'width_bits': len(chosen) * 8,
                        'little_endian_hex': chosen.hex(), 'uint_hex': hex(int.from_bytes(chosen, 'little')),
                        'host_strtod_binary64_le': double_bytes.hex(),
                        'host_computed_temporary_float32_le': float_bytes.hex()}
                row['argument_bits'].append(bits)
                conversions[token] = {k: v for k, v in bits.items() if k != 'token_index'}
                if text == 'nan':
                    assert int.from_bytes(double_bytes, 'little') == 0x7ff8000000000000
            elif token.startswith('hex:'):
                b = bytes.fromhex(token[4:])
                assert len(b) == 64
                row.setdefault('input_buffers', []).append({'token_index': pos, 'bytes': 64, 'little_endian_hex': b.hex(),
                    'eight_binary64_uint64_hex': [hex(x) for x in struct.unpack('<8Q', b)]})
    write('inputs.json', {'frozen_utc': utc(), 'processes': rows, 'native_evaluations': 34,
        'auxiliary_endpoints': inputs['bezier']['auxiliary_endpoints'], 'withheld_factory_registry_converter_rows': 50,
        'six_prospective_oracles': 'REQ009 local M false, predeclared; no public input admission or ARM claim'})
    write('host-context.json', {'captured_utc': utc(), 'python': sys.version, 'uname': list(os.uname()),
        'machine': os.uname().machine, 'byteorder': sys.byteorder, 'libc_gnu_version': libc.gnu_get_libc_version().decode(),
        'strtod_check': 'Actual host libc strtod called for each FP token, full consumption checked, exact binary64/float32 bytes frozen; chosen d:nan reproduces positive quiet0x7ff8000000000000',
        'parser_conversions': conversions, 'child_environment': ENV, 'stdin': 'DEVNULL', 'core_limit': [0, 0],
        'umask': '0077', 'timeout_seconds': 20, 'automatic_retry': False,
        'limits': 'Host parser verification, not child-register tracing. Loader source forms temporary float even for d:; compiler realization and per-process FP flags/mode were not traced. No ARM/Apple equivalence, NaN payload universe, invalid-input admission or fenv calibration.'})
    source_paths = [SELECT, ASSESS, BASE / 'family-automation-routes-v1/manifest.json', BASE / 'family-automation-routes-v1/batch-inputs.json',
                    BASE / 'family-automation-routes-v1/route-ledger.json', ROOT / 'wiki/specs/automation-envelopes.md',
                    X2 / 'manifest.json', X2 / 'xexec2.c', X2 / 'run_x2.py', X2 / 'seq.py', X2 / 'raw/runs.jsonl',
                    T14 / 'manifest.json', T14 / 'harness/xexec.c', T14 / 'harness/xexec.py', T14 / 'run_mix.py', T14 / 'raw/runs.jsonl']
    write('source-pins.json', {'pins': [identity(p) for p in source_paths],
        'stubs': 'Existing X2 and T14 source binding tables only; no new/imported Python helper, patch, callback stub, initializer, constructor registry or gdb interception. M historical receipt and B/S selected rows have no used imports. An unexpected use/trap/fault is retained and stops remaining calls.',
        'comparison': 'M RAX&1 only; Bezier xmm0/xmm1 exact binary64 pair plus documented binary32-Y presentation; segment40-byte dump. Ignore all other volatile registers. Any mismatch is retained without criterion change or rerun.'})
    write('custody-before.json', {'utc': utc(), 'identities': binaries, 'scope': 'Whole image and two existing loaders freshly hashed once before this batch; no binary analysis or code expansion.'})
    (HERE / 'collect-once.py').chmod(0o444)
    pre = [HERE / n for n in ['collect-once.py', 'inputs.json', 'host-context.json', 'source-pins.json', 'custody-before.json']]
    write('manifest-before.json', {'schema': 'pre-original-call-custody-manifest-v1', 'frozen_utc': utc(),
        'original_calls_so_far': 0, 'outer_pid': os.getpid(), 'maximum_processes': 11, 'native_evaluations': 34,
        'payloads': [identity(p) for p in pre], 'selection_pin': identity(SELECT), 'assessment_pin': identity(ASSESS)})
    print('Pre-call manifest frozen; qNaN/all argument checks and three binary identities PASS.', flush=True)
    (HERE / 'raw').mkdir()
    receipts = []
    stopped = None
    receiptfile = (HERE / 'receipts.jsonl').open('x', encoding='utf-8')
    for row in rows:
        loader = xloader['path'] if row['leaf'] == 'monotone' else tloader['path']
        argv = [loader, image['path'], '--imports', *row['tokens']]
        start, mono = utc(), time.monotonic_ns()
        stdout = stderr = b''
        timeout, pid, exitcode, launcherror = False, None, None, None
        try:
            child = subprocess.Popen(argv, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                cwd=HERE, env=ENV, preexec_fn=lambda: resource.setrlimit(resource.RLIMIT_CORE, (0, 0)))
            pid = child.pid
            try:
                stdout, stderr = child.communicate(timeout=20)
            except subprocess.TimeoutExpired:
                timeout = True
                child.kill()
                stdout, stderr = child.communicate()
            exitcode = child.returncode
        except OSError as e:
            launcherror = repr(e)
        end, monoend = utc(), time.monotonic_ns()
        for suffix, b in [('stdout', stdout), ('stderr', stderr)]:
            p = HERE / 'raw' / (row['id'] + '.' + suffix)
            with p.open('xb') as f:
                f.write(b)
                f.flush()
                os.fsync(f.fileno())
            p.chmod(0o444)
        parsed, parseerror = None, None
        try:
            parsed = parse_output(stdout.decode('ascii'))
        except (ValueError, UnicodeError) as e:
            parseerror = repr(e)
        record = {'id': row['id'], 'argv': argv, 'pid': pid, 'start_utc': start, 'end_utc': end,
            'start_monotonic_ns': mono, 'end_monotonic_ns': monoend, 'exit_code': exitcode,
            'timeout_seconds': 20, 'timeout': timeout, 'launch_error': launcherror, 'parse_error': parseerror,
            'environment': ENV, 'stdin': 'DEVNULL', 'core_limit': [0, 0], 'retry': False,
            'stdout': identity(HERE / 'raw' / (row['id'] + '.stdout')),
            'stderr': identity(HERE / 'raw' / (row['id'] + '.stderr')), 'stderr_bytes': len(stderr), 'parsed': parsed,
            'TRAP_or_FAULT_lines': [s for s in (stdout + b'\n' + stderr).decode('utf-8', errors='replace').splitlines() if 'TRAP' in s or 'FAULT' in s]}
        receiptfile.write(json.dumps(record, allow_nan=False) + '\n')
        receiptfile.flush()
        os.fsync(receiptfile.fileno())
        receipts.append(record)
        print(row['id'], 'pid', pid, 'exit', exitcode, 'calls', len(parsed['calls']) if parsed else None, flush=True)
        n = row['tokens'].count('call')
        if timeout or exitcode != 0 or stderr or launcherror or parseerror or record['TRAP_or_FAULT_lines'] or not parsed or parsed['used'] or len(parsed['calls']) != n:
            stopped = {'after': row['id'], 'reason': 'Unexpected execution/import/status/parse/count condition; no remaining process attempted.'}
            break
    receiptfile.close()
    (HERE / 'receipts.jsonl').chmod(0o444)
    after = [identity(p['path']) for p in [image, xloader, tloader]]
    write('custody-after.json', {'utc': utc(), 'identities': after, 'matches_before': after == binaries})
    assert after == binaries, 'Post-batch custody mismatch: retain results, no rerun'
    mismatches, observations = [], []
    for row, receipt in zip(rows, receipts):
        p = receipt['parsed']
        if not p:
            continue
        if row['leaf'] == 'monotone':
            values = [int(c['rax'], 16) & 1 for c in p['calls']]
            for i, (got, expected) in enumerate(zip(values, row['expected_boolean'])):
                observations.append({'leaf': 'monotone', 'index': i, 'value': got, 'expected': expected,
                                     'classification': 'historical' if i < 4 else 'prospective-local-REQ009'})
                if got != expected:
                    mismatches.append({'id': row['id'], 'index': i, 'expected': expected, 'observed': got})
        elif row['leaf'] == 'bezier':
            got = [[c['xmm0'], c['xmm1']] for c in p['calls']]
            expected = [[c['xmm0'], c['xmm1']] for c in row['historical_scoped_output']['calls']]
            observations.append({'leaf': 'bezier', 'binary64_pairs': got,
                'binary32_y_uint_hex': [hex(struct.unpack('<I', struct.pack('<f', struct.unpack('<d', struct.pack('<Q', int(v[1], 16)))[0]))[0]) for v in got],
                'all_exact_historical_pairs': got == expected})
            if got != expected: mismatches.append({'id': row['id'], 'expected': expected, 'observed': got})
        else:
            got = [d['hex'] for d in p['dumps']]
            expected = [d['hex'] for d in row['historical_scoped_output']['dumps']]
            observations.append({'leaf': 'segment', 'id': row['id'], 'dump40_hex': got,
                                 'all_exact_historical_dump_bytes': got == expected})
            if got != expected: mismatches.append({'id': row['id'], 'expected': expected, 'observed': got})
    write('analysis.json', {'status': 'COMPLETE' if not stopped and len(receipts) == 11 else 'STOPPED_PARTIAL',
        'stopped': stopped, 'native_calls': sum(len(r['parsed']['calls']) for r in receipts if r['parsed']),
        'processes': len(receipts), 'auxiliary_endpoints': 2, 'withheld_factory_registry_converter_rows': 50,
        'new_application_grades': 0, 'observations': observations, 'mismatches': mismatches,
        'limits': 'Finite local original x86 results only. No input admission/loaded event/provider/consumer/timebase/public normalization/Save/audio/ARM proof. Temporary float cast/FP flags and child-register payload are not independently traced. Required unsupported behavior staysU/coverageOPEN. No retry, criterion repair, owner/case/release/site change or successor.'})
    if not stopped:
        write('author-check.json', check())
    else:
        write('author-check.json', {'status': 'PARTIAL_EXECUTION_RETAINED_NO_RETRY', 'stopped': stopped})
    print(json.dumps(load(HERE / 'analysis.json')['mismatches']), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--execute', action='store_true')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    if args.execute == args.check:
        parser.error('choose exactly --execute or data-only --check')
    if args.check:
        print(json.dumps(check()))
    else:
        execute()
