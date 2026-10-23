"""Validate finite comparisons and an isolated export; no device code is executed."""
import hashlib
import importlib.util
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
PACKAGE = HERE.with_name('device-tension-v1')


def main():
    manifest = json.loads((PACKAGE/'manifest.json').read_text())
    listed = {r['path'] for r in manifest['files']}
    assert {str(p.relative_to(PACKAGE)) for p in PACKAGE.rglob('*') if p.is_file()} == listed | {'manifest.json'}
    assert not any(p.is_symlink() for p in PACKAGE.rglob('*'))
    for row in manifest['files']:
        data = (PACKAGE/row['path']).read_bytes()
        assert len(data) == row['bytes'] and hashlib.sha256(data).hexdigest() == row['sha256']
    deny = re.compile(r'(?i)(0x[0-9a-f]{6,}|FUN_[0-9a-f]+|DAT_[0-9a-f]+|/home/|/var/tmp/|\.\./|harness|xexec|CreateInstanceU|SetParameterA|CalcA|t12-tension|DTN-\d)')
    for path in PACKAGE.rglob('*'):
        if path.is_file() and path.suffix in ['.md', '.json', '.py']:
            assert not deny.search(path.read_text()), path
            if path.suffix == '.md':
                for target in re.findall(r'\]\(([^)]+)\)', path.read_text()): assert (path.parent/target).is_file(), target
    spec = importlib.util.spec_from_file_location('finite_tension_comparison', PACKAGE/'compare.py')
    comparator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(comparator)
    cases = json.loads((PACKAGE/'cases.json').read_text())['cases']
    results, mutations, checks = [], 0, 0
    for case in cases:
        for e in case['evaluations']:
            assert len(e['parameter_order']) == len(set(e['parameter_order'])) == len(e['parameters']) == 129
            assert set(e['parameter_order']) == set(e['parameters'])
            assert (PACKAGE/e['signal']).read_bytes() == bytes(e['frames']*4)
            value = comparator.audio(PACKAGE/e['reference'], e['frames'])
            result = comparator.compare(value, value, e['metric'], e['sample_rate_hz'])
            assert result['pass'], e['id']
            checks += result['checks']
            for mutant in ['silence', 'gain', 'early-impulse']:
                wrong = value.copy()
                if mutant == 'silence': wrong[:] = 0
                elif mutant == 'gain': wrong *= 2
                else: wrong[0] = 0.01
                try: rejected = not comparator.compare(wrong, value, e['metric'], e['sample_rate_hz'])['pass']
                except (ValueError, ZeroDivisionError, FloatingPointError): rejected = True
                assert rejected, (e['id'], mutant)
                mutations += 1
            results.append({'id': e['id'], 'pass': True, 'checks': result['checks']})
    with tempfile.TemporaryDirectory(prefix='tension-export-') as temporary:
        export = Path(temporary)/'package'
        shutil.copytree(PACKAGE, export)
        run = subprocess.run([sys.executable, '-I', str(export/'compare.py'), str(export/'reference')], capture_output=True, text=True, cwd=temporary)
        assert run.returncode == 0, run.stderr+run.stdout
        isolated = json.loads(run.stdout)
        assert isolated['pass'] and len(isolated['results']) == len(results)
        (HERE/'isolated-self-comparison.json').write_text(json.dumps(isolated, indent=1)+'\n')
        path = Path(temporary)/'bad.f32'
        frames = cases[0]['evaluations'][0]['frames']
        for size in [0, frames*4-4, frames*4+4]:
            path.write_bytes(bytes(size))
            try: comparator.audio(path, frames)
            except ValueError: pass
            else: raise AssertionError('invalid byte length accepted')
        for number in [float('nan'), float('inf'), -float('inf')]:
            value = np.zeros(frames, dtype='<f4'); value[0] = number; value.tofile(path)
            try: comparator.audio(path, frames)
            except ValueError: pass
            else: raise AssertionError('nonfinite output accepted')
        try: comparator.audio(Path(temporary)/'missing.f32', frames)
        except FileNotFoundError: pass
        else: raise AssertionError('missing output accepted')
    report = {'status': 'pass', 'scope': 'author integrity and comparison behavior only; no application or original-code execution',
              'manifest_sha256': hashlib.sha256((PACKAGE/'manifest.json').read_bytes()).hexdigest(),
              'case_count': len(cases), 'self_comparisons': results, 'self_measurements_passed': checks,
              'mutants_rejected': mutations, 'invalid_files_rejected': 7, 'isolated_export': 'pass'}
    (HERE/'author-validation.json').write_text(json.dumps(report, indent=1)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k != 'self_comparisons'}, indent=1))


if __name__ == '__main__': main()
