"""Exactly two fixed original children ONLY on Root's explicit one-shot selection."""
from pathlib import Path
import datetime, hashlib, json, math, re, resource, struct, subprocess, sys, time

PRE = Path(__file__).resolve().parent
NAMES = ['control', 'left-step']

def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b): return hashlib.sha256(b).hexdigest()
def ident(p):
    b = p.read_bytes()
    return {'path': str(p), 'bytes': len(b), 'sha256': sha(b)}
def save(p, value):
    with p.open('x') as f: f.write(json.dumps(value, indent=2, allow_nan=False) + '\n')

def finite_output(b):
    return len(b) == 131072 and all(math.isfinite(v) for f in struct.iter_unpack('<ff', b) for v in f)

def valid_log(text, err, expected_params, input_path):
    lines = text.splitlines()
    params = [s.split()[1:] for s in lines if s.startswith('param ')]
    if len(params) != 39 or any(len(v) != 2 for v in params): return False
    try:
        if any(a[0] != e[0] or struct.pack('<f', float(a[1])) != struct.pack('<f', float(e[1]))
               for a, e in zip(params, expected_params)): return False
    except (ValueError, OverflowError): return False
    processes = [s for s in lines if s.startswith('process ')]
    if len(processes) != 2: return False
    for line in processes:
        m = re.fullmatch(r'process 8192 512 flags:((?: \d+x\(ret=-?\d+,flag=-?\d+\))+) blocks=16', line)
        if m is None or sum(int(v) for v in re.findall(r'(\d+)x\(', m[1])) != 16: return False
    commands = [s.split()[0] for s in lines if s.split() and s.split()[0] in
                {'mxcsr', 'transport', 'create', 'rate', 'param', 'inflag', 'input', 'process', 'destroy', 'event', 'reset', 'info'}]
    expected = ['mxcsr', 'transport', 'create', 'rate'] + ['param'] * 38
    expected += ['inflag', 'input', 'process', 'param', 'process', 'destroy']
    if commands != expected: return False
    fixed = ['mxcsr 0x1f80', 'transport 0 0 120', 'create ok', 'rate 44100 ret=1',
             'inflag 1', 'input ' + input_path, 'destroy']
    return (all(lines.count(s) == 1 for s in fixed) and not err
            and [s for s in lines if s.startswith('cxx-failbits ')] == ['cxx-failbits 0']
            and not any('TRAP' in s or 'FAULT' in s or s.startswith('xdev:') for s in lines))

def main():
    if len(sys.argv) != 3 or sys.argv[1] != '--capture-selected-once':
        raise SystemExit('Root-selected one-shot invocation and exact reviewed manifest SHA required. No replay mode.')
    seal = PRE / 'manifest-preflight.json'
    assert sha(seal.read_bytes()) == sys.argv[2]
    manifest = json.loads(seal.read_text())
    for r in manifest['files']:
        b = (PRE / r['path']).read_bytes()
        assert len(b) == r['bytes'] and sha(b) == r['sha256']
    p = json.loads((PRE / 'proposal.json').read_text())
    for r in p['source_pins'].values(): assert ident(Path(r['path'])) == r
    bundle = Path(p['source_pins']['bundle']['path']).read_bytes()
    s = p['x86_slice']
    assert sha(bundle[s['offset']:s['offset'] + s['bytes']]) == s['sha256']
    for name in NAMES:
        assert (PRE / (name + '.script')).read_text().splitlines() == p['scripts'][name]
    inp = Path(p['source_pins']['input']['path']).read_bytes()
    assert finite_output(inp)
    assert [(i, *f) for i, f in enumerate(struct.iter_unpack('<ff', inp)) if any(f)] == [(4096, 1., 1.)]
    history = json.loads((PRE / 'preservation-inputs.json').read_text())
    watched = {Path(r['path']) for r in history}
    watched.update(Path(r['path']) for r in p['source_pins'].values())
    watched.update(f for f in PRE.iterdir() if f.is_file())
    for r in history: assert ident(Path(r['path'])) == r
    before = [ident(f) for f in sorted(watched)]
    dest = Path(p['final_directory'])
    dest.mkdir(exist_ok=False)  # Partial attempts are retained; never reused or removed.
    raw = dest / 'raw'
    raw.mkdir(exist_ok=False)
    for f in PRE.iterdir():
        if f.is_file():
            with (dest / f.name).open('xb') as out: out.write(f.read_bytes())
    save(dest / 'watch-before.json', before)
    env = p['child_environment_complete']
    assert env['XDEV_TIME'] == '0' and set(env) <= {'PATH', 'LANG', 'LC_ALL', 'LC_CTYPE', 'TZ', 'XDEV_TIME'}
    limits = {k: list(resource.getrlimit(getattr(resource, k))) for k in dir(resource) if k.startswith('RLIMIT_')}
    limits['RLIMIT_CORE'] = [0, 0]
    save(dest / 'attempt.json', {'started_utc': utc(), 'preflight_sha256': sys.argv[2],
         'scope': 'At most two launch attempts, control then left-step; no retry/extra baseline.',
         'cwd': str(raw), 'complete_child_environment': env, 'child_limits': limits, 'timeout_seconds': 30,
         'max_attempts': 2, 'max_requested_direct_exports': 148, 'nested_calls_not_counted': True,
         'criterion': None, 'grade': None, 'readiness_is_not_execution': True})
    for name in NAMES:
        with (raw / (name + '.script')).open('xb') as f: f.write((PRE / (name + '.script')).read_bytes())
    def core_off(): resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    runs = []
    for name in NAMES:
        output, so, se = [raw / (name + suffix) for suffix in ['.f32', '.stdout', '.stderr']]
        assert not any(f.exists() for f in [output, so, se])
        argv = [p['source_pins']['xdev']['path'], p['source_pins']['bundle']['path'],
                str(raw / (name + '.script')), str(output), '--imports']
        row = {'name': name, 'argv': argv, 'started_utc': utc(), 'launch_attempted': False,
               'popen_returned_pid': False, 'exit_code': None, 'signal': None, 'timeout': False, 'exception': None,
               'original_export_execution': 'Unknown from launch alone; partial execution requires precise log evidence.'}
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
        row['declared_imports'] = [s for s in text.splitlines() if s.startswith('import ')]
        row['used_imports'] = [s for s in text.splitlines() if s.startswith('used ')]
        row['process_lines'] = [s for s in text.splitlines() if s.startswith('process ')]
        row['log_valid'] = valid_log(text, err, [s.split()[1:] for s in p['scripts'][name] if s.startswith('param ')],
                                     p['source_pins']['input']['path'])
        row['numeric_valid'] = False
        if output.is_file():
            row['output'] = ident(output)
            row['numeric_valid'] = finite_output(output.read_bytes())
        row['valid_capture'] = (row['exit_code'] == 0 and not row['timeout'] and row['exception'] is None
                                and row['log_valid'] and row['numeric_valid'])
        row['positive_ringing_or_4000_frame_law'] = 'Not inferred; silent or unchanged finite output is structurally valid.'
        save(dest / (name + '-result.json'), row)
        runs.append(row)
        if not row['valid_capture']: break
    after = [ident(f) for f in sorted(watched)]
    changed = [{'before': a, 'after': z} for a, z in zip(before, after) if a != z]
    save(dest / 'watch-after.json', {'checked_utc': utc(), 'files': after, 'changed': changed})
    result = {'finished_utc': utc(), 'runs': runs,
              'attempted_launches': sum(r['launch_attempted'] for r in runs),
              'returned_pid_children': sum(r['popen_returned_pid'] for r in runs),
              'structurally_valid_captures': sum(r['valid_capture'] for r in runs),
              'returned_pid_scope': 'Returned usable child/PID only; failed Popen does not prove no OS child briefly existed.',
              'all2_structurally_valid': len(runs) == 2 and all(r['valid_capture'] for r in runs),
              'watch_count': len(before), 'watch_unchanged': not changed, 'criterion': None, 'grade': None,
              'new_normative_cases': 0, 'actual_ringing_step_or_unaffected_channel_claim': None}
    save(dest / 'results.json', result)
    print(json.dumps(result, indent=2, allow_nan=False))

if __name__ == '__main__': main()
