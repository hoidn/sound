"""Author-only preparation: execute ONLY after Root selects this exact sealed source.

Uses the NEW public comparator as data-only measurement code. No synthesis,
collector, original/device functions, old comparator/model/main, or new fits
outside the preserved public comparator. Writes only the exclusive result dir.
"""
from pathlib import Path
import copy
import datetime
import hashlib
import json
import os
import runpy
import shutil
import subprocess
import sys
import tempfile
import traceback

HERE = Path(__file__).resolve().parent
STAGE = HERE.parent.parent / 'device-corpus-v5'
OUT = HERE.parent / 'numeric-validation'
STEP = '1336d90115bd24c058e556aa95e9140014d168dad7111dec64eb8edd1d977e73'
LABELS = [('left pickup pre waveform', 'preL'), ('left pickup post waveform', 'postL'),
          ('right pickup pre waveform', 'preR'), ('right pickup post waveform', 'postR')]


def identity(path):
    raw = path.read_bytes()
    return {'path': str(path), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def write(name, data):
    (OUT/name).write_text(json.dumps(data, indent=2, allow_nan=False)+'\n')


def main():
    if len(sys.argv) != 3 or sys.argv[1] != '--approved-preflight-sha':
        raise SystemExit('Requires Root selection and exact --approved-preflight-sha HASH; no implicit run.')
    seal = HERE/'manifest.json'
    assert identity(seal)['sha256'] == sys.argv[2], 'Preflight source SHA differs'
    for row in json.loads(seal.read_text())['files']:
        got = identity(HERE/row['path'])
        assert got['bytes'] == row['bytes'] and got['sha256'] == row['sha256']
    providers = json.loads((HERE/'providers.json').read_text())
    roles = {row['role']: Path(row['path']) for row in providers['pins']}
    watched = set(roles.values()) | {p for p in HERE.iterdir() if p.is_file()} | {p for p in STAGE.rglob('*') if p.is_file()}
    for row in providers['pins']:
        assert identity(Path(row['path'])) == {k: row[k] for k in ['path', 'bytes', 'sha256']}
    for role in ['v4_manifest', 'actual_validation_manifest']:
        path = roles[role]
        for row in json.loads(path.read_text())['files']:
            p = path.parent/row['path']
            got = identity(p)
            assert got['bytes'] == row['bytes'] and got['sha256'] == row['sha256']
            watched.add(p)
    binding = json.loads((HERE/'candidate-binding.json').read_text())
    assert identity(STAGE/'manifest.json') == binding['manifest']
    stage_rows = json.loads((STAGE/'manifest.json').read_text())['files']
    assert {r['path'] for r in stage_rows} == {str(p.relative_to(STAGE)) for p in STAGE.rglob('*') if p.is_file() and p.name != 'manifest.json'}
    for row in stage_rows:
        got = identity(STAGE/row['path'])
        assert got['bytes'] == row['bytes'] and got['sha256'] == row['sha256']
    before = {str(p): identity(p) for p in sorted(watched)}
    OUT.mkdir(exist_ok=False)
    write('watch-before.json', before)
    write('attempt.json', {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                          'argv': sys.argv, 'preflight_sha256': sys.argv[2],
                          'original_calls': 0, 'purpose': 'ONE data-only integration/control calculation'})
    previous_bytecode = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    failure = None
    controls, guard_results = [], []
    try:
        with tempfile.TemporaryDirectory(prefix='isolated-', dir=OUT) as tmp:
            work = Path(tmp)
            export = work/'export'
            shutil.copytree(STAGE, export)
            ns = runpy.run_path(str(export/'compare.py'), run_name='reviewed_corpus_v5_measurement')
            public_cases = json.loads((export/'cases.json').read_text())
            flat = [e for c in public_cases['cases'] for e in c['evaluations']]
            assert len(flat) == 73
            candidate = work/'reference-self'
            candidate.mkdir()
            for e in flat:
                shutil.copyfile(export/e['reference'], candidate/(e['id']+'.f32'))
            env = os.environ.copy()
            env.update(PYTHONDONTWRITEBYTECODE='1', PYTHONNOUSERSITE='1')
            cmd = [sys.executable, '-B', str(export/'compare.py'), str(candidate)]
            process = subprocess.run(cmd, cwd=work, env=env, capture_output=True, timeout=300)
            (OUT/'public-cli.stdout.json').write_bytes(process.stdout)
            (OUT/'public-cli.stderr.txt').write_bytes(process.stderr)
            write('public-cli-receipt.json', {'argv': cmd, 'exit': process.returncode,
                                             'isolated_export': True, 'candidate_is_reference_copy': True})
            assert process.returncode == 0, 'NEW public CLI regression failed'
            regression = json.loads(process.stdout)
            assert regression['pass'] and len(regression['results']) == 73
            assert [r['id'] for r in regression['results']] == [e['id'] for e in flat]
            count = sum(len(r['measurements']) for r in regression['results'])
            assert count == 4799
            new_result = regression['results'][-1]
            assert [m['check'] for m in new_result['measurements']] == [a for a, b in LABELS]
            assert all(m['error'] == 0 and m['pass'] for m in new_result['measurements'])
            run = ns['run']
            original_here = run.__globals__['HERE']

            def one_case(evaluation, value_path, reference_path):
                """Test ONLY the NEW run() with isolated minimal input files."""
                test = work/'single-case'
                if test.exists():
                    shutil.rmtree(test)
                test.mkdir()
                values = test/'candidate'
                values.mkdir()
                e = copy.deepcopy(evaluation)
                e['reference'] = 'reference.f32'
                shutil.copyfile(reference_path, test/e['reference'])
                shutil.copyfile(value_path, values/(e['id']+'.f32'))
                (test/'cases.json').write_text(json.dumps({'cases': [{'evaluations': [e]}]}))
                run.__globals__['HERE'] = test
                try:
                    return run(values)['results'][0]
                finally:
                    run.__globals__['HERE'] = original_here

            actual = json.loads(roles['actual_validation_results'].read_text())
            source_manifest = json.loads(roles['actual_validation_manifest'].read_text())
            by_hash = {}
            for row in source_manifest['files']:
                if row['path'].endswith('.f32'):
                    by_hash.setdefault(row['sha256'], roles['actual_validation_manifest'].parent/row['path'])
            for row in actual['comparisons']:
                value_path = Path(row['path'])
                reference_path = by_hash[row['reference_sha256']]
                expected = row['result']
                if not row['synthetic_arithmetic_only'] and row['reference_sha256'] != STEP:
                    result = one_case(flat[-1], value_path, reference_path)
                    controls.append({'name': row['name'], 'source_expected': expected, 'public_guard_result': result})
                    assert not result['pass'] and result['error'] == 'Pickup step reference hash differs from the pinned capture'
                    controls[-1]['match'] = True
                    continue
                try:
                    y, ref = ns['audio'](value_path), ns['audio'](reference_path)
                    result = ns['compare'](y, ref, {'kind': 'pickup_step_waveform'}, 44100)
                except ValueError as error:
                    controls.append({'name': row['name'], 'source_expected': expected, 'public_invalid': str(error),
                                     'granularity': 'Public case fails as a whole; no invented partial-axis measurements'})
                    assert not expected['valid'] and not expected['pass']
                    controls[-1]['match'] = True
                else:
                    controls.append({'name': row['name'], 'synthetic_arithmetic_only': row['synthetic_arithmetic_only'],
                                     'source_expected': expected, 'public_result': result})
                    assert expected['valid'] and result['pass'] == expected['pass']
                    axes = {a['axis']: a for a in expected['axes']}
                    assert len(result['measurements']) == 4
                    for measured, (label, axis) in zip(result['measurements'], LABELS):
                        a = axes[axis]
                        assert measured == {'check': label, 'error': a['error'], 'tolerance': a['tolerance'], 'pass': a['pass']}
                    controls[-1]['match'] = True
            assert len(controls) == 38
            for kind, message in [('ramp_waveform', 'Ramp reference hash differs from the pinned capture'),
                                  ('noteoff_decay_zero_waveform', 'NoteOff zero endpoint reference hash differs from the pinned capture'),
                                  ('pickup_step_waveform', 'Pickup step reference hash differs from the pinned capture')]:
                evaluation = next(e for e in flat if e['metric']['kind'] == kind)
                result = one_case(evaluation, roles['step_reference'], roles['matched_control'])
                guard_results.append({'kind': kind, 'result': result})
                assert not result['pass'] and result['error'] == message
            write('summary.json', {'status': 'PASS data-only NEW comparator integration/control validation',
                                   'evaluations': 73, 'measurements': count, 'old_evaluations': 72,
                                   'old_measurements': count-4, 'new_measurements': 4,
                                   'nonzero_self_errors': sum(m['error'] != 0 for r in regression['results'] for m in r['measurements']),
                                   'controls': len(controls), 'hash_guard_controls': len(guard_results),
                                   'python': sys.version, 'numpy': ns['np'].__version__, 'scipy': sys.modules['scipy'].__version__,
                                   'original_calls': 0, 'candidate_or_application_grade': None})
    except BaseException:
        failure = traceback.format_exc()
        (OUT/'failure.txt').write_text(failure)
    finally:
        sys.dont_write_bytecode = previous_bytecode
        write('controls.json', {'comparisons': controls, 'strict_hash_guards': guard_results,
                                'complete': len(controls) == 38 and len(guard_results) == 3 and failure is None,
                                'whole_case_invalidity_not_partial_axis_report': True})
        after = {str(p): identity(p) for p in sorted(watched)}
        write('watch-after.json', after)
        write('receipt.json', {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                              'status': 'PASS' if failure is None and after == before else 'FAILED',
                              'watched': len(watched), 'unchanged': after == before,
                              'original_calls': 0, 'candidate_or_application_grade': None})
        inventory = [identity(p) for p in sorted(OUT.iterdir()) if p.is_file()]
        write('manifest.json', {'status': 'actual one-shot data-only result, not candidate grade', 'files': inventory})
    if failure is not None:
        raise SystemExit(failure)
    assert before == after, 'Watched source/package bytes changed'
    print(json.dumps({'status': 'PASS', 'result_directory': str(OUT), 'watched': len(watched), 'unchanged': True}))


if __name__ == '__main__':
    main()
