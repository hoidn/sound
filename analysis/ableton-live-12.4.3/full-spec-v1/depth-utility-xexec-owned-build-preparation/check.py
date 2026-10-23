"""Read-only identity/AST/synthetic scope checks. Never import/run the collector."""
from pathlib import Path
import ast, hashlib, json, sys
P = Path(__file__).resolve().parent

def identity(p):
    b = p.read_bytes(); return {'path': str(p), 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}

def main():
    if sys.argv[1:] != ['--check']:
        print('REFUSED: only read-only --check is supported', file=sys.stderr); return 1
    inputs = json.loads((P / 'inputs.json').read_text()); plan = json.loads((P / 'plan.json').read_text())
    watched = {Path(v['path']) for v in inputs['pins']} | {p for p in P.iterdir() if p.is_file()}
    before = {str(p): identity(p) for p in watched}
    for row in inputs['pins']: assert identity(Path(row['path'])) == row
    tool = inputs['gcc_filesystem_metadata']; assert str(Path(tool['selected_path']).resolve()) == tool['resolved_path']
    assert not Path(plan['exclusive_destination']).exists()
    s = (P / 'build-once.py').read_text(); tree = ast.parse(s)
    fns = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    assignments = {n.targets[0].id: n.value for n in tree.body if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name)}
    expected_assignments = {
        'ROOT': "Path('/home/ollie/Documents/sound')",
        'BASE': "ROOT / 'analysis/ableton-live-12.4.3/full-spec-v1'",
        'PRE': "BASE / 'depth-utility-xexec-owned-build-preparation'",
        'DEST': "BASE / 'depth-utility-xexec-owned-build'",
        'CWD': "ROOT",
        'OLD': "Path('/var/tmp/sound-analysis/xexec/xexec')",
        'GCC': "Path('/usr/bin/gcc')",
        'SOURCE': "ROOT / 'tools/xexec/xexec.c'",
        'SOURCES': "[str(SOURCE)]",
        'FLAGS': "['-O1', '-g', '-Wall', '-Wextra', '-no-pie']",
        'OUTPUT': "DEST / 'xexec'",
        'ENV': "{'PATH': '/usr/bin:/bin', 'LANG': 'C', 'LC_ALL': 'C'}",
        'TIMEOUT': '45'}
    for name, expression in expected_assignments.items():
        assert ast.dump(assignments[name]) == ast.dump(ast.parse(expression, mode='eval').body)
    # Only these two complete new pure functions are evaluated; main/identity/imports/Popen never run.
    chosen = ast.Module(body=[fns['command'], fns['validate_spec']], type_ignores=[])
    allowed = {'str', 'ValueError', 'command'}
    for n in ast.walk(chosen):
        if isinstance(n, ast.Call):
            assert isinstance(n.func, ast.Name) and n.func.id in allowed or isinstance(n.func, ast.Attribute) and n.func.attr == 'startswith'
    argv = plan['fixed_argv']; split = argv.index('-o')
    assert split == 6 and argv[-2:] == ['-ldl', '-lm']
    flags = ['-O1', '-g', '-Wall', '-Wextra', '-no-pie']
    assert argv[1:split] == flags
    cwd = Path(plan['cwd']); sources = [str(cwd / 'tools/xexec/xexec.c')]
    assert argv[split+2:-2] == sources and argv[0] == '/usr/bin/gcc' and argv[split+1] == plan['output']
    assert plan['output'] == str(Path(plan['exclusive_destination']) / 'xexec')
    ns = {'Path': Path, 'GCC': Path(argv[0]), 'FLAGS': flags, 'OUTPUT': Path(plan['output']),
          'SOURCES': sources, 'CWD': cwd, 'ENV': plan['environment'],
          'OLD': Path(inputs['historical_binary']['path']), 'DEST': Path(plan['exclusive_destination'])}
    exec(compile(chosen, '<selected-new-pure-scope-check>', 'exec'), ns)
    assert ns['command']() == argv
    ns['validate_spec'](argv, str(cwd), plan['output'], plan['environment'])
    bad = []
    a = argv.copy(); a[split+1] = inputs['historical_binary']['path']; bad.append(('old output', a, str(cwd), a[split+1], plan['environment']))
    a = argv.copy(); a[split+2] = str(cwd / 'tools/xexec/changed.c'); bad.append(('wrong source', a, str(cwd), plan['output'], plan['environment']))
    a = argv.copy(); a[1] = '-O2'; bad.append(('wrong flags', a, str(cwd), plan['output'], plan['environment']))
    bad.append(('extra execute', argv + ['&&', plan['output']], str(cwd), plan['output'], plan['environment']))
    bad.append(('wrong cwd', argv, '/tmp', plan['output'], plan['environment']))
    bad.append(('wrong output carrier', argv, str(cwd), sources[0], plan['environment']))
    bad.append(('extra environment', argv, str(cwd), plan['output'], dict(plan['environment'], LD_PRELOAD='/tmp/fake.so')))
    rejected = []
    for name, *args in bad:
        try: ns['validate_spec'](*args)
        except ValueError: rejected.append(name)
        else: raise AssertionError(name)
    calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call)]
    popens = [n for n in calls if isinstance(n.func, ast.Attribute) and n.func.attr == 'Popen']
    assert len(popens) == 1 and ast.unparse(popens[0].args[0]) == 'argv'
    assert not any(isinstance(n.func, ast.Attribute) and n.func.attr in ['run', 'system', 'execv', 'execve'] for n in calls)
    assert '--version' not in s and 'shell=True' not in s
    # Guard the distinct attempt/PID chronology and exclusive output creation in the actual source.
    assert s.index("result['top_level_compiler_attempts'] = 1") < s.index('child = subprocess.Popen(') < s.index("result['returned_pid'] = child.pid")
    assert 'DEST.mkdir()' in s and "open('x')" in s and "open('xb')" in s
    assert 'start_new_session=True' in s and 'preexec_fn=no_core' in s and 'stdin=subprocess.DEVNULL' in s
    assert 'TIMEOUT = 45' in s and 'os.killpg(child.pid, signal.SIGKILL)' in s
    assert 'rebuilt == historic' in s and "'MISMATCH_UNRESOLVED'" in s
    delta = plan['source_delta']['line_edits']; parent = Path(plan['method_parent']['path'])
    assert identity(parent) == plan['method_parent']
    restored = parent.read_text().splitlines(keepends=True)
    for e in reversed(delta):
        lo, hi = e['old_line_start'], e['old_line_end']
        assert hashlib.sha256(''.join(restored[lo:hi]).encode()).hexdigest() == e['old_text_sha256']
        restored[lo:hi] = e['replacement'].splitlines(keepends=True)
    assert ''.join(restored) == s
    assert 'CWD.rglob' not in s and 'old_paths = sorted([SOURCE, OLD])' in s
    if (P / 'manifest.json').exists():
        m = json.loads((P / 'manifest.json').read_text())
        assert sorted(p.name for p in P.iterdir()) == sorted([r['path'] for r in m['files']] + ['manifest.json'])
        for r in m['files']:
            got = identity(P / r['path']); assert (got['bytes'], got['sha256']) == (r['bytes'], r['sha256'])
    after = {str(p): identity(p) for p in watched}; assert before == after
    print(json.dumps(dict(status='PASS PREPARATION ONLY', pins=len(inputs['pins']), watched=len(watched),
          unchanged=True, valid_controls=1, unsafe_scope_rejections=rejected, direct_Popen_sites=1,
          compiler_or_output_or_original_execution=False, future_destination_absent=True), indent=2))
    return 0
if __name__ == '__main__': raise SystemExit(main())
