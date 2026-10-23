"""Validate the new finite measurement draft; never execute original or candidate DSP."""
from pathlib import Path
import hashlib
import importlib.util
import json
import math
import os
import shutil
import struct
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[4]
STAGE = Path(__file__).resolve().parent.with_name('device-corpus-v2')
OLD = ROOT / 'handoff/device-corpus-v1'

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    if sys.argv[1:] != ['--check']:
        raise SystemExit('usage: check_draft.py --check (read-only payload validation)')
    payloads = [p for p in STAGE.rglob('*') if p.is_file()]
    before = {str(p): sha(p) for p in payloads}
    previous = json.loads((OLD / 'cases.json').read_text())['cases']
    current = json.loads((STAGE / 'cases.json').read_text())['cases']
    old_e = {e['id']: e for g in previous for e in g['evaluations']}
    new_e = {e['id']: e for g in current for e in g['evaluations']}
    assert len(current) == 24 and len(old_e) == 68 and len(new_e) == 69
    assert all(new_e[k] == v for k, v in old_e.items())
    fixtures = [p for p in OLD.rglob('*.f32')]
    assert len(fixtures) == 77 and all(sha(p) == sha(STAGE / p.relative_to(OLD)) for p in fixtures)
    measure = load('corpus_v2_measure', STAGE / 'compare.py')
    pure = load('ramp_pure_measure', ROOT / 'analysis/ableton-live-12.4.3/full-spec-v1/depth-corpus-lfo-ramp-criterion/compare_ramp.py')
    assert len(pure.self_test()) == 19
    checks = []
    ramp_id = 'CORPUS-AUDIO-020-02'
    ramp = new_e[ramp_id]
    nominal = (STAGE / ramp['reference']).read_bytes()
    reference = measure.audio(STAGE / ramp['reference'])
    base = ROOT / 'analysis/ableton-live-12.4.3/full-spec-v1'
    vectors = [nominal, (base/'depth-corpus-lfo-ramp-sensitivity/raw/plus1.f32').read_bytes(),
               (base/'depth-corpus-lfo-ramp-sensitivity/raw/minus1.f32').read_bytes(),
               (base/'depth-corpus-lfo-ramp-up/raw/sine-baseline.f32').read_bytes()]
    with tempfile.TemporaryDirectory(prefix='corpus-v2-finite-check-') as directory:
        temp = Path(directory)
        for n, raw in enumerate(vectors):
            trial = temp / 'trial.f32'; trial.write_bytes(raw)
            result = measure.compare(measure.audio(trial), reference, ramp['metric'], 44100)
            expected = pure.compare_bytes(nominal, raw)
            assert result['pass'] == expected['accepted']
            assert [r['error'] for r in result['measurements']] == [r['relative_rms_error'] for r in expected['channels']]
            checks.append('retained-vector-exact-' + str(n))
        # Mathematical boundary fixtures are independent of the pinned reference file.
        synthetic = measure.np.zeros((16384, 2), dtype=measure.np.float64)
        synthetic[4096] = [100.0, 100.0]
        word = struct.unpack('<I', struct.pack('<f', 101.0))[0]
        adjacent = [struct.unpack('<f', struct.pack('<I', word + k))[0] for k in (-1, 0, 1)]
        for name, left, right, accepted in [('below',adjacent[0],adjacent[0],True),
                ('inclusive',101.0,101.0,True), ('above',adjacent[2],adjacent[2],False),
                ('left-fails',adjacent[2],100.0,False),('right-fails',100.0,adjacent[2],False)]:
            trial = synthetic.copy();trial[4096] = [left, right]
            result = measure.compare(trial, synthetic, ramp['metric'], 44100)
            assert result['pass'] is accepted
            checks.append(name)
        for channel in (0, 1):
            trial = reference.copy(); trial[4096:,channel] = 0
            try: measure.compare(trial, reference, ramp['metric'], 44100)
            except ValueError: checks.append('zero-energy-channel-' + str(channel))
            else: raise AssertionError('silent channel accepted')
        for name, raw in [('short',nominal[:-4]),('oversized',nominal+bytes(8)),
                          ('nonfinite-prefix',struct.pack('<f',float('nan'))+nominal[4:]),
                          ('nonfinite-active',nominal[:32768]+struct.pack('<f',float('inf'))+nominal[32772:])]:
            trial = temp/'invalid.f32';trial.write_bytes(raw)
            try: measure.audio(trial)
            except ValueError: checks.append(name)
            else: raise AssertionError('invalid output admitted: '+name)
        trial = reference.copy();trial[:4096] = 123
        assert measure.compare(trial, reference, ramp['metric'], 44100)['pass']
        checks.append('finite-prefix-explicitly-ungraded')
        # A minimal trusted-case fixture exercises the new run-time reference hash gate.
        fixture = temp/'hash-gate';fixture.mkdir();(fixture/'cases.json').write_text(json.dumps({'cases':[{'evaluations':[ramp]}]}))
        (fixture/'reference').mkdir();(fixture/ramp['reference']).write_bytes(vectors[3])
        output = temp/'candidate';output.mkdir();(output/(ramp_id+'.f32')).write_bytes(nominal)
        original_here = measure.HERE;measure.HERE = fixture
        try:
            result = measure.run(output)
            assert not result['pass'] and 'reference hash' in result['results'][0]['error']
            checks.append('wrong-reference-hash-refused')
        finally: measure.HERE = original_here
        # Export has no analyst siblings; only the new measurement tool is executed.
        export = temp/'export';shutil.copytree(STAGE,export)
        env = os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1'
        process = subprocess.run([sys.executable,'-B',str(export/'compare.py'),str(export/'reference')],cwd=export,env=env,capture_output=True,text=True)
        assert process.returncode == 0, process.stderr
        report = json.loads(process.stdout)
        assert report['pass'] and len(report['results']) == 69
        count = sum(len(r['measurements']) for r in report['results'])
        assert count == 4603
        checks.append('isolated-export-69-selfcomparisons-4603-measurements')
    assert before == {str(p):sha(p) for p in payloads}
    result = {'status':'pass','checks':checks,'old_evaluations_exact':68,'old_fixture_files_exact':77,
              'new_eval_mapping':{'DCO-029':ramp_id},'pure_comparator_selftests':19,
              'all_self_evaluations':69,'all_self_measurements':count,
              'self_report_sha256':hashlib.sha256(process.stdout.encode()).hexdigest(),
              'all_watched_draft_payloads_exact':len(before),'original_execution':False,'candidate_device_execution':False,
              'note':'Generated data and reference self-comparison validate measurements only; not candidate conformance.'}
    print(json.dumps(result,indent=2))

if __name__ == '__main__':
    main()
