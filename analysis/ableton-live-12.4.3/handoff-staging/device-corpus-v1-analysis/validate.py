"""Candidate-only integrity and metric validation. Does not execute reference code."""
import hashlib
import importlib.util
import json
import re
import tempfile
import sys
sys.dont_write_bytecode = True
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
PACKAGE = HERE.with_name('device-corpus-v1')


def module(path):
    spec=importlib.util.spec_from_file_location('corpus_audio_comparison',path)
    value=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def validate(package):
    package=Path(package)
    comparator=module(package/'compare.py')
    manifest=json.loads((package/'manifest.json').read_text())
    listed={r['path'] for r in manifest['files']}
    actual={str(p.relative_to(package)) for p in package.rglob('*') if p.is_file()}
    assert actual==listed|{'manifest.json'}
    assert not any(p.is_symlink() for p in package.rglob('*'))
    for row in manifest['files']:
        data=(package/row['path']).read_bytes()
        assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
    # The numerical windows and comparisons are the only executable payload code.
    assert {p.name for p in package.rglob('*.py')}=={'compare.py'}
    forbidden=re.compile(r'(?i)(0x[0-9a-f]{6,}|FUN_[0-9a-f]+|DAT_[0-9a-f]+|/home/|/var/tmp/|\.\./|harness|xexec|SNewCompound|AWarpMarker|CreateInstanceU|SetParameterA|CalcA|t12-device|DCO-\d)')
    for p in package.rglob('*'):
        if p.is_file() and p.suffix in ('.md','.json','.py'):
            assert not forbidden.search(p.read_text()), p
            if p.suffix=='.md':
                for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)',p.read_text()):
                    assert (p.parent/target).is_file(),(p,target)
    cases=json.loads((package/'cases.json').read_text())['cases']
    count=checks=0
    self_results=[]
    for case in cases:
        for e in case['evaluations']:
            ref=comparator.audio(package/e['reference'])
            assert len(e['parameters'])==len(set(e['parameter_order']))==38
            assert set(e['parameters'])==set(e['parameter_order'])
            assert len((package/e['signal']).read_bytes())==16384*2*4
            result=comparator.compare(ref,ref,e['metric'],e['sample_rate_hz'])
            assert result['pass'],e['id']
            checks+=len(result['measurements'])
            for ch in [0,1]:
                silent=ref.copy();silent[:,ch]=0
                try: rejected=not comparator.compare(silent,ref,e['metric'],e['sample_rate_hz'])['pass']
                except (ValueError,ZeroDivisionError):rejected=True
                assert rejected,(e['id'],'silent',ch)
                wrong=ref.copy()
                if e['metric']['kind']=='lfo':wrong[:,ch]=np.sin(2*np.pi*440*np.arange(16384)/e['sample_rate_hz'])
                else:wrong[:,ch]*=1.02
                assert not comparator.compare(wrong,ref,e['metric'],e['sample_rate_hz'])['pass'],(e['id'],'wrong',ch)
                count+=2
            self_results.append({'id':e['id'],'pass':True,'measurement_count':len(result['measurements'])})
    with tempfile.TemporaryDirectory() as directory:
        p=Path(directory)/'bad.f32'
        for size in [0,16384*2*4-4,16384*2*4+4]:
            p.write_bytes(b'\0'*size)
            try:comparator.audio(p)
            except ValueError:pass
            else:raise AssertionError('invalid byte length accepted')
        for value in [np.nan,np.inf,-np.inf]:
            bad=np.zeros((16384,2),np.float32);bad[9000,1]=value;bad.tofile(p)
            try:comparator.audio(p)
            except ValueError:pass
            else:raise AssertionError('nonfinite sample accepted')
        try:comparator.audio(Path(directory)/'missing.f32')
        except FileNotFoundError:pass
        else:raise AssertionError('missing output accepted')
    return {'status':'pass','scope':'candidate integrity and metric behavior only; no new reference or application execution',
        'manifest_sha256':hashlib.sha256((package/'manifest.json').read_bytes()).hexdigest(),
        'payload_files':len(listed),'case_count':len(cases),'evaluation_count':len(self_results),
        'self_measurements_passed':checks,'channel_mutations_rejected':count,'invalid_file_checks_rejected':7,'self_comparisons':self_results}


if __name__=='__main__':
    report=validate(PACKAGE)
    (HERE/'author-validation.json').write_text(json.dumps(report,indent=1)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='self_comparisons'},indent=1))
