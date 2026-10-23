"""Three fixed X captures ONLY after independent preflight and Root's explicit selection."""
from pathlib import Path
import datetime, hashlib, json, math, resource, struct, subprocess, sys, time
PRE = Path(__file__).resolve().parent
NAMES = ['gate1-held', 'gate1-off', 'gate0-off']

def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b): return hashlib.sha256(b).hexdigest()
def ident(p):
    b = p.read_bytes()
    return {'path': str(p), 'bytes': len(b), 'sha256': sha(b)}
def save(p, value):
    with p.open('x') as f: f.write(json.dumps(value, indent=2, allow_nan=False) + '\n')

def validate_scripts(proposal):
    base = Path(proposal['source_pins']['historical_script']['path']).read_text()
    for name in NAMES:
        expected = base.replace('param 13 0.0\n', 'param 13 1.0\n') if name != 'gate0-off' else base
        if name != 'gate1-held':
            expected = expected.replace('event 1537 0x90 60 100\n', 'event 1537 0x90 60 100\nevent 8193 0x80 60 64\n')
        text = (PRE / (name + '.script')).read_text()
        assert text == expected
        lines = text.splitlines()
        assert [int(s.split()[1]) for s in lines if s.startswith('param ')] == list(range(38))
        assert sum(s.startswith('process ') for s in lines) == 1
        assert sum(s.startswith('event ') for s in lines) == (1 if name == 'gate1-held' else 2)
        assert sum(s.startswith(('create', 'rate ', 'param ', 'destroy')) for s in lines) + 32 == 73
    assert len(NAMES) == 3 and 3 * 73 <= 256

def main():
    if len(sys.argv) != 3 or sys.argv[1] != '--capture-selected-once':
        raise SystemExit('Requires Root-selected one-shot invocation and exact reviewed manifest SHA; no replay mode.')
    seal = PRE / 'manifest-preflight.json'
    assert sha(seal.read_bytes()) == sys.argv[2]
    manifest = json.loads(seal.read_text())
    for r in manifest['files']:
        b = (PRE / r['path']).read_bytes()
        assert len(b) == r['bytes'] and sha(b) == r['sha256']
    proposal = json.loads((PRE / 'proposal.json').read_text())
    pins = proposal['source_pins']
    for r in pins.values(): assert ident(Path(r['path'])) == r
    bundle = Path(pins['bundle']['path']).read_bytes()
    section = proposal['x86_slice']
    assert sha(bundle[section['offset']:section['offset'] + section['bytes']]) == section['sha256']
    validate_scripts(proposal)
    inp = list(struct.iter_unpack('<ff', Path(pins['input']['path']).read_bytes()))
    assert len(inp) == 16384 and [(i, *v) for i, v in enumerate(inp) if any(v)] == [(4096, 1., 1.)]
    watched = {Path(r['path']) for r in json.loads(Path(pins['history_watch_provider']['path']).read_text())}
    for root in proposal['history_watch']['extra_immutable_roots']:
        watched.update(p for p in Path(root).rglob('*') if p.is_file())
    watched.update(Path(s) for s in proposal['history_watch']['extra_files'])
    watched.update(Path(r['path']) for r in pins.values())
    watched.update(p for p in PRE.rglob('*') if p.is_file())
    before = [ident(p) for p in sorted(watched)]
    # A partial attempt is retained forever. This collector never removes or reuses it.
    dest = Path(proposal['final_directory'])
    dest.mkdir(exist_ok=False)
    raw = dest / 'raw'
    raw.mkdir(exist_ok=False)
    for r in manifest['files']:
        with (dest / r['path']).open('xb') as f: f.write((PRE / r['path']).read_bytes())
    with (dest / 'manifest-preflight.json').open('xb') as f: f.write(seal.read_bytes())
    save(dest / 'watch-before.json', before)
    save(dest / 'context-asof.json', {str(p): p.read_text() for p in sorted(watched) if '/wiki/' in str(p)})
    env = proposal['child_environment_complete']
    assert env['XDEV_TIME'] == '0' and set(env) <= {'PATH', 'LANG', 'LC_ALL', 'LC_CTYPE', 'TZ', 'XDEV_TIME'}
    limits = {k: list(resource.getrlimit(getattr(resource, k))) for k in dir(resource) if k.startswith('RLIMIT_')}
    limits['RLIMIT_CORE'] = [0, 0]
    save(dest / 'attempt.json', {'started_utc': utc(), 'preflight_manifest_sha256': sys.argv[2],
         'scope': 'Root-selected maximum3 original-x86 children A/B/C, no retries or extra baseline.',
         'child_environment_complete': env, 'child_limits': limits, 'timeout_seconds_per_child': 30,
         'cwd': str(raw), 'max_launch_attempts': 3, 'requested_direct_exports_max': 219,
         'direct_count_excludes_loader_and_nested_calls': True, 'no_retry': True,
         'diagnostic_automatic': False, 'criterion': None, 'grade': None})
    for name in NAMES:
        with (raw / (name + '.script')).open('xb') as f: f.write((PRE / (name + '.script')).read_bytes())
    def core_off(): resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    def run(name):
        out, so, se = [raw / (name + suffix) for suffix in ['.f32', '.stdout', '.stderr']]
        assert not any(p.exists() for p in [out, so, se])
        argv = [pins['xdev']['path'], pins['bundle']['path'], str(raw / (name + '.script')), str(out), '--imports']
        row = {'name': name, 'argv': argv, 'started_utc': utc(), 'launch_attempted': False, 'popen_returned_pid': False,
               'original_export_execution': 'Unknown from launch alone; inspect command logs, status and output. No unlogged partial execution is inferred.',
               'exit_code': None, 'signal': None, 'timeout': False, 'exception': None}
        start = time.monotonic()
        with so.open('xb') as stdout, se.open('xb') as stderr:
            try:
                row['launch_attempted'] = True
                child = subprocess.Popen(argv, cwd=raw, env=env, stdout=stdout, stderr=stderr, preexec_fn=core_off)
                row['pid'] = child.pid
                row['popen_returned_pid'] = True
                try: child.wait(timeout=30)
                except subprocess.TimeoutExpired:
                    row['timeout'] = True
                    child.kill()
                    child.wait()
                row['exit_code'] = child.returncode
                if child.returncode < 0: row['signal'] = -child.returncode
            except Exception as exc: row['exception'] = repr(exc)
        row.update(finished_utc=utc(), elapsed_seconds=time.monotonic() - start, stdout=ident(so), stderr=ident(se))
        text, err = so.read_text(errors='replace'), se.read_text(errors='replace')
        lines = text.splitlines()
        row['used_imports'] = [s for s in lines if s.startswith('used ')]
        row['declared_imports'] = [s for s in lines if s.startswith('import ')]
        row['fault_or_trap'] = [s for s in (text + '\n' + err).splitlines() if 'TRAP' in s or 'FAULT' in s or s.startswith('xdev:')]
        row['process_lines'] = [s for s in lines if s.startswith('process ')]
        row['cxx_failbits'] = [s for s in lines if s.startswith('cxx-failbits ')]
        row['event_lines'] = [s for s in lines if s.startswith('event ')]
        row['parameter_lines'] = [s for s in lines if s.startswith('param ')]
        expected_params = [s.split()[1:] for s in (PRE / (name + '.script')).read_text().splitlines() if s.startswith('param ')]
        actual_params = [s.split()[1:] for s in row['parameter_lines']]
        row['parameter_echo_valid'] = (len(actual_params) == 38 and all(len(v) == 2 for v in actual_params)
            and [v[0] for v in actual_params] == [v[0] for v in expected_params]
            and all(struct.pack('<f', float(a[1])) == struct.pack('<f', float(e[1])) for a, e in zip(actual_params, expected_params)))
        expected_events = ['event 1537 0x90 60 100'] + ([] if name == 'gate1-held' else ['event 8193 0x80 60 64'])
        row['numeric_valid'] = False
        row['numeric_error'] = None
        row['productive_before_off_both_channels'] = False
        if out.is_file():
            row['output'] = ident(out)
            try:
                b = out.read_bytes()
                assert len(b) == 131072, 'wrong output byte count'
                x = list(struct.iter_unpack('<ff', b))
                assert all(math.isfinite(v) for f in x for v in f), 'nonfinite output'
                channels = []
                for c in (0, 1):
                    pre, active, late = [[f[c] for f in x[a:z]] for a, z in [(0, 4096), (4096, 8192), (8192, 16384)]]
                    r = {'channel': c, 'prefix_peak': max(map(abs, pre)), 'before_off_peak': max(map(abs, active)),
                         'prefix_mean_square': math.fsum(v*v for v in pre)/len(pre),
                         'before_off_mean_square': math.fsum(v*v for v in active)/len(active),
                         'before_off_nonzero': sum(v != 0 for v in active),
                         'later_peak': max(map(abs, late)), 'later_mean_square': math.fsum(v*v for v in late)/len(late)}
                    r['productive_before_off'] = r['before_off_nonzero'] > 0 and r['before_off_peak'] > r['prefix_peak'] and r['before_off_mean_square'] > r['prefix_mean_square']
                    channels.append(r)
                row['channels'] = channels
                row['numeric_valid'] = True
                row['productive_before_off_both_channels'] = all(r['productive_before_off'] for r in channels)
            except (AssertionError, ValueError, OverflowError) as exc: row['numeric_error'] = str(exc)
        # Energy is a descriptive applicability premise, NEVER structural validity or continuation.
        row['valid_capture'] = (row['exit_code'] == 0 and not row['timeout'] and row['exception'] is None
            and not row['fault_or_trap'] and not err and row['cxx_failbits'] == ['cxx-failbits 0']
            and len(row['process_lines']) == 1 and row['process_lines'][0].startswith('process 16384 512 flags:')
            and row['event_lines'] == expected_events and row['parameter_echo_valid'] and 'create ok' in lines and 'rate 44100 ret=1' in lines
            and 'destroy' in lines and row['numeric_valid'])
        row['release_tail_inference'] = 'Not selected; if productive-before-off absent, applicability premise also absent.'
        save(dest / (name + '-result.json'), row)
        return row
    runs = []
    for name in NAMES:
        row = run(name)
        runs.append(row)
        if not row['valid_capture']: break
    after = [ident(p) for p in sorted(watched)]
    changed = [{'before': a, 'after': b} for a, b in zip(before, after) if a != b]
    save(dest / 'watch-after.json', {'checked_utc': utc(), 'files': after, 'changed': changed})
    result = {'finished_utc': utc(), 'runs': runs,
              'attempted_launches': sum(r['launch_attempted'] for r in runs),
              'returned_pid_children': sum(r['popen_returned_pid'] for r in runs),
              'structurally_valid_captures': sum(r['valid_capture'] for r in runs),
              'returned_pid_scope': 'Popen returned a usable child/PID; failed Popen does not prove no OS child briefly existed.',
              'watch_count': len(before),
              'watch_unchanged': not changed, 'all3_structurally_valid': len(runs) == 3 and all(r['valid_capture'] for r in runs),
              'historical_fourth_control_only': pins['historical_reference'], 'criterion': None, 'grade': None,
              'new_normative_cases': 0, 'noteoff_delivery_or_gate_law': 'UNESTABLISHED; structural/event logs and energy alone do not prove it.',
              'wholeLive_arm64_or_candidate_claim': False}
    save(dest / 'results.json', result)
    print(json.dumps({'destination': str(dest), 'runs': [{'name': r['name'], 'exit': r['exit_code'],
          'launch_attempted': r['launch_attempted'], 'popen_returned_pid': r['popen_returned_pid'],
          'valid_capture': r['valid_capture'], 'output': r.get('output'),
          'productive_before_off_both_channels': r['productive_before_off_both_channels']} for r in runs],
          'attempted_launches': result['attempted_launches'],
          'returned_pid_children': result['returned_pid_children'],
          'structurally_valid_captures': result['structurally_valid_captures'],
          'watch_count': len(before), 'watch_unchanged': not changed, 'grade': None}, indent=2))

if __name__ == '__main__': main()
