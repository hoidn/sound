"""Reviewer-only finite metadata/raw arithmetic. No project modules or programs run."""
from pathlib import Path
import datetime
import hashlib
import json
import math
import struct

BASE = Path('/home/ollie/Documents/sound/analysis/ableton-live-12.4.3/full-spec-v1')
P = BASE / 'depth-corpus-midi-noteoff-decay-zero'
PRE = BASE / 'depth-corpus-midi-noteoff-decay-zero-preparation'
NAMES = ['gate1-held', 'gate1-off', 'gate0-off']


def read_json(path):
    return json.loads(path.read_text())


def identity(path):
    data = path.read_bytes()
    return {'path': str(path), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def check_identity(row, path=None):
    path = Path(row['path']) if path is None else path
    got = identity(path)
    assert all(got[k] == row[k] for k in ['bytes', 'sha256']), str(path)


def samples(path):
    data = path.read_bytes()
    assert len(data) == 131072
    frames = list(struct.iter_unpack('<ff', data))
    assert all(math.isfinite(v) for frame in frames for v in frame)
    return data, frames


manifest = read_json(P / 'manifest.json')
assert identity(P / 'manifest.json')['sha256'] == 'dd0166b6b5faeb5d3592894d43cdb57ca25991931dd4f6a09795186efb3cd934'
assert len(manifest['files']) == 45
assert {str(q.relative_to(P)) for q in P.rglob('*') if q.is_file()} == {r['path'] for r in manifest['files']} | {'manifest.json'}
for row in manifest['files']:
    check_identity(row, P / row['path'])
prep_manifest = read_json(PRE / 'manifest-preflight.json')
for row in prep_manifest['files']:
    assert (P / row['path']).read_bytes() == (PRE / row['path']).read_bytes()
assert (P / 'manifest-preflight.json').read_bytes() == (PRE / 'manifest-preflight.json').read_bytes()
proposal = read_json(P / 'proposal.json')
for row in proposal['source_pins'].values():
    check_identity(row)
for name in ['corpus-midi-noteoff-decay-zero-preflight-review.json']:
    assert (P / name).read_bytes() == (BASE / 'reviews' / name).read_bytes()
for q in (P / 'root-evidence').iterdir():
    assert q.read_bytes() == (BASE / 'depth-corpus-midi-noteoff-decay-zero-root' / q.name).read_bytes()

selection = read_json(P / 'root-evidence/root-selection.json')
invocation = read_json(P / 'root-evidence/root-invocation.json')
assert selection['argv'] == invocation['argv']
assert invocation['argv'][-1] == identity(PRE / 'manifest-preflight.json')['sha256']
assert invocation['argv'][-2] == '--capture-selected-once'
assert invocation['argv'][1:3] == ['-B', str(PRE / 'capture-once.py')]
assert selection['selected_utc'] <= invocation['started_utc'] < invocation['finished_utc']
assert invocation['exit_code'] == 0 and invocation['collector_invocations'] == 1 and not invocation['retry']
assert invocation['diagnostic_invocations'] == 0
for field in ['stdout', 'stderr', 'watch_before', 'watch_after']:
    check_identity(invocation[field])
attempt = read_json(P / 'attempt.json')
assert attempt['child_environment_complete'] == proposal['child_environment_complete']
assert set(attempt['child_environment_complete']) == {'PATH', 'LANG', 'LC_ALL', 'LC_CTYPE', 'XDEV_TIME'}
assert attempt['child_limits']['RLIMIT_CORE'] == [0, 0]
assert attempt['timeout_seconds_per_child'] == 30 and attempt['max_launch_attempts'] == 3
assert attempt['no_retry'] and not attempt['diagnostic_automatic']
assert attempt['cwd'] == str(P / 'raw')

result = read_json(P / 'results.json')
assert [r['name'] for r in result['runs']] == NAMES
assert all(result[k] == 3 for k in ['attempted_launches', 'returned_pid_children', 'structurally_valid_captures'])
assert result['all3_structurally_valid'] and result['criterion'] is None and result['grade'] is None
data = {}
summaries = []
for row in result['runs']:
    name = row['name']
    assert row == read_json(P / (name + '-result.json'))
    assert row['launch_attempted'] and row['popen_returned_pid'] and row['valid_capture']
    assert isinstance(row['pid'], int) and row['pid'] > 0
    assert row['exit_code'] == 0 and not row['timeout']
    assert row['signal'] is None and row['exception'] is None
    assert invocation['started_utc'] < row['started_utc'] < row['finished_utc'] < invocation['finished_utc']
    assert row['argv'] == [proposal['source_pins']['xdev']['path'], proposal['source_pins']['bundle']['path'],
                           str(P / 'raw' / (name + '.script')), str(P / 'raw' / (name + '.f32')), '--imports']
    script = (P / (name + '.script')).read_text()
    assert script == (PRE / (name + '.script')).read_text() == (P / 'raw' / (name + '.script')).read_text()
    parent = BASE / 'depth-corpus-midi-gate-before-impulse-preparation' / (name + '.script')
    assert script == parent.read_text().replace('param 34 1.0\n', 'param 34 0.0\n')
    text = (P / 'raw' / (name + '.stdout')).read_text()
    lines = text.splitlines()
    assert not (P / 'raw' / (name + '.stderr')).read_bytes()
    assert not any('TRAP' in s or 'FAULT' in s or s.startswith('xdev:') for s in lines)
    for field in ['stdout', 'stderr', 'output']:
        check_identity(row[field])
    for key, prefix in [('used_imports', 'used '), ('declared_imports', 'import '),
                        ('event_lines', 'event '), ('parameter_lines', 'param '),
                        ('process_lines', 'process '), ('cxx_failbits', 'cxx-failbits ')]:
        assert row[key] == [s for s in lines if s.startswith(prefix)]
    expected_process = 'process 16384 512 flags: ' + ('21x(ret=0,flag=1) 11x(ret=0,flag=0)' if name == 'gate1-off' else '32x(ret=0,flag=1)') + ' blocks=32'
    assert row['process_lines'] == [expected_process]
    assert row['cxx_failbits'] == ['cxx-failbits 0'] and row['fault_or_trap'] == []
    assert all(s in lines for s in ['create ok', 'rate 44100 ret=1', 'destroy', 'mxcsr 0x1f80', 'transport 0 0 120', 'inflag 1'])
    expected_events = ['event 1537 0x90 60 100'] + ([] if name == 'gate1-held' else ['event 3073 0x80 60 64'])
    assert row['event_lines'] == expected_events
    want = [s.split()[1:] for s in script.splitlines() if s.startswith('param ')]
    got = [s.split()[1:] for s in row['parameter_lines']]
    assert len(want) == len(got) == 38
    assert [int(v[0]) for v in got] == list(range(38))
    assert [struct.pack('<f', float(v[1])) for v in got] == [struct.pack('<f', float(v[1])) for v in want]
    assert float(want[13][1]) == (0 if name == 'gate0-off' else 1)
    assert float(want[12][1]) == 1 and float(want[17][1]) == 0
    assert struct.pack('<f', float(want[34][1])) == bytes(4)
    prior = [s.split()[1:] for s in parent.read_text().splitlines() if s.startswith('param ')]
    changed_bits = [i for i, (a, z) in enumerate(zip(want, prior)) if struct.pack('<f', float(a[1])) != struct.pack('<f', float(z[1]))]
    assert changed_bits == [34] and struct.pack('<f', float(prior[34][1])) == bytes.fromhex('0000803f')
    data[name] = samples(P / 'raw' / (name + '.f32'))
    for c in (0, 1):
        pre, early, later = [[f[c] for f in data[name][1][a:z]] for a, z in [(0, 4096), (4096, 8192), (8192, 16384)]]
        measured = {'channel': c, 'prefix_peak': max(map(abs, pre)), 'early_response_peak': max(map(abs, early)),
                    'prefix_mean_square': math.fsum(v*v for v in pre)/len(pre),
                    'early_response_mean_square': math.fsum(v*v for v in early)/len(early),
                    'early_response_nonzero': sum(v != 0 for v in early),
                    'later_peak': max(map(abs, later)), 'later_mean_square': math.fsum(v*v for v in later)/len(later)}
        measured['productive_response'] = measured['early_response_nonzero'] > 0 and measured['early_response_peak'] > measured['prefix_peak'] and measured['early_response_mean_square'] > measured['prefix_mean_square']
        assert measured == row['channels'][c]
    summaries.append({'name': name, 'pid': row['pid'], 'raw_sha256': row['output']['sha256'],
                      'bytes': row['output']['bytes'], 'finite': True, 'events': expected_events})
assert len({r['pid'] for r in result['runs']}) == 3
stdout = read_json(P / 'root-evidence/root-stdout.json')
assert stdout['attempted_launches'] == stdout['returned_pid_children'] == stdout['structurally_valid_captures'] == 3
assert stdout['runs'] == [{'name': r['name'], 'exit': r['exit_code'], 'launch_attempted': r['launch_attempted'],
                          'popen_returned_pid': r['popen_returned_pid'], 'valid_capture': r['valid_capture'],
                          'output': r['output'], 'productive_response_both_channels': r['productive_response_both_channels']} for r in result['runs']]

durable = {}
for label, bp, ap, n in [('collector', P/'watch-before.json', P/'watch-after.json', 725),
                         ('Root', P/'root-evidence/watch-before.json', P/'root-evidence/watch-after.json', 2457),
                         ('diagnostic', P/'root-evidence/diagnostic-watch-before.json', P/'root-evidence/diagnostic-watch-after.json', 31)]:
    before, after = read_json(bp), read_json(ap)
    if isinstance(after, dict):
        assert after['changed'] == []
        after = after['files']
    assert len(before) == n and len({r['path'] for r in before}) == n and before == after
    durable[label] = n
asof = read_json(P/'context-asof.json')
bm = {r['path']: r for r in read_json(P/'watch-before.json')}
assert len(asof) == 5
for name, text in asof.items():
    encoded = text.encode()
    assert len(encoded) == bm[name]['bytes'] and hashlib.sha256(encoded).hexdigest() == bm[name]['sha256']

saved = read_json(P / 'descriptive.json')
alias = {'A': 'gate1-held', 'B': 'gate1-off', 'C': 'gate0-off'}
for label, name in alias.items():
    check_identity(saved['inputs'][label])
    assert Path(saved['inputs'][label]['path']) == P/'raw'/(name+'.f32')
    data[label] = data[name]
for label in ['old_A34one', 'old_B34one', 'old_held0']:
    check_identity(saved['inputs'][label])
    data[label] = samples(Path(saved['inputs'][label]['path']))
rows = []
pairs = [('A', 'B'), ('A', 'old_A34one'), ('B', 'old_B34one'), ('C', 'old_held0')]
for a, z in pairs:
    for c in (0, 1):
        for first, last in [(0, 3072), (3072, 4096), (4096, 4352), (4096, 8192), (8192, 16384)]:
            values = list(zip([v[c] for v in data[a][1][first:last]], [v[c] for v in data[z][1][first:last]]))
            energy = math.fsum(v*v for v, w in values)
            difference = math.fsum((v-w)*(v-w) for v, w in values)
            rows.append({'first': a, 'second': z, 'channel': c, 'start': first, 'end_exclusive': last,
                         'differing_samples': sum(v != w for v, w in values),
                         'max_abs_difference': max(abs(v-w) for v, w in values),
                         'relative_rms_to_first': math.sqrt(difference/energy) if energy else None})
assert rows == saved['rows'] and len(rows) == 40
full_equal = {a+'__'+z: data[a][0] == data[z][0] for a, z in pairs}
post_equal = {a+'__'+z: data[a][0][4096*8:] == data[z][0][4096*8:] for a, z in pairs}
assert full_equal == saved['full_byte_equal'] == {'A__B': False, 'A__old_A34one': False, 'B__old_B34one': False, 'C__old_held0': True}
assert post_equal == saved['post4096_equal'] == {'A__B': False, 'A__old_A34one': True, 'B__old_B34one': False, 'C__old_held0': True}
assert data['A'][0][4096*8:] == data['old_held0'][0][4096*8:]
assert data['C'][0] == data['old_held0'][0]
assert any(v != 0 for f in data['B'][1][8192:] for v in f)
ds = read_json(P/'root-evidence/diagnostic-selection.json')
dr = read_json(P/'root-evidence/diagnostic-receipt.json')
assert ds['selected_utc'] <= dr['started_utc'] < dr['finished_utc']
assert ds['argv'] == dr['argv'] and dr['exit'] == 0 and dr['original_calls'] == 0
check_identity(ds['source']); check_identity(dr['stdout']); check_identity(dr['stderr'])
print(json.dumps({'checked_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'status': 'PASS bounded endpoint raw/metadata observations only; no criterion or gate law',
    'packet_payloads': 45, 'packet_files': 46, 'source_pins': len(proposal['source_pins']),
    'rows': summaries, 'actual_channels_independently_recomputed': {r['name']: r['channels'] for r in result['runs']},
    'durable_paired_watches': durable, 'asof_wiki_texts': 5,
    'descriptive_rows_exact': rows, 'full_byte_equal': full_equal, 'post4096_byte_equal': post_equal,
    'B_later_nonzero_by_channel': [sum(f[c] != 0 for f in data['B'][1][8192:]) for c in (0, 1)],
    'collector_invocations_by_reviewer': 0, 'native_children_by_reviewer': 0,
    'criterion': None, 'grade': None}, indent=2, allow_nan=False))
