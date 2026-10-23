"""Validate finite measurements and exact captures without running an instrument."""
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
import scipy
from scipy.io import wavfile

sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
PACKAGE=HERE.with_name('device-analog-v1')
SOURCE=ROOT/'analysis/ableton-live-12.4.3/r2/t12-analog-v1'


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def validate():
    m=json.loads((PACKAGE/'manifest.json').read_text())
    listed={r['path'] for r in m['files']}
    actual={str(p.relative_to(PACKAGE)) for p in PACKAGE.rglob('*') if p.is_file()}
    assert actual==listed|{'manifest.json'} and not any(p.is_symlink() for p in PACKAGE.rglob('*'))
    for row in m['files']:
        p=PACKAGE/row['path'];assert p.stat().st_size==row['bytes'] and sha(p)==row['sha256']
    deny=re.compile(r'(?i)(0x[0-9a-f]{6,}|FUN_[0-9a-f]+|DAT_[0-9a-f]+|/home/|/var/tmp/|\.\./|xexec|t12-analog|DAN-\d|SetParameterA|CalcA|CreateInstanceU|ToggleDummy|second output of index)')
    for p in PACKAGE.rglob('*'):
        if p.is_file() and p.suffix in ('.md','.json','.py'):
            assert not deny.search(p.read_text()),p
            if p.suffix=='.md':
                for link in re.findall(r'\[[^\]]+\]\(([^)]+)\)',p.read_text()):assert (p.parent/link).is_file(),link
    assert {p.name for p in PACKAGE.rglob('*.py')}=={'compare.py'}
    source_manifest=json.loads((SOURCE/'manifest.json').read_text())
    for file,info in source_manifest['files'].items():assert sha(SOURCE/file)==info['sha256']
    for name,info in source_manifest['external_inputs'].items():
        if name.startswith('n6-'):assert sha(Path(info['path']))==info['sha256']
    for row in json.loads((HERE/'source-inventory.json').read_text())['files']:
        p=ROOT/row['path'];assert sha(p)==row['sha256'] and p.stat().st_size==row['bytes']
    spec=importlib.util.spec_from_file_location('analog_metric',PACKAGE/'compare.py');tool=importlib.util.module_from_spec(spec);spec.loader.exec_module(tool)
    cases=json.loads((PACKAGE/'cases.json').read_text())['cases']
    ev={e['id']:e for c in cases for e in c['evaluations']}
    for row in json.loads((HERE/'traceability.json').read_text())['evaluations']:
        e=ev[row['evaluation']]
        rate,mono=wavfile.read(ROOT/row['source_wav']);stereo=np.stack([mono,mono],axis=1).astype('<f4')
        assert stereo.tobytes()==(PACKAGE/e['reference']).read_bytes()
        assert hashlib.sha256(stereo.tobytes()).hexdigest()==row['stereo_sample_sha256']
        lines=(ROOT/row['source_script']).read_text().splitlines()
        params=[(int(i),float(v)) for i,v in (re.fullmatch(r'param (\d+) (.+)',line).groups() for line in lines if line.startswith('param '))]
        assert len(params)==203 and [i for i,v in params]==list(range(203))
        for i,value in params:assert np.float32(value)==np.float32(e['parameters'][e['parameter_order'][i]])
        events=[(int(f),int(s,0),int(k),int(v)) for f,s,k,v in (line.split()[1:] for line in lines if line.startswith('event '))]
        public=[(r['frame'],(144 if r['kind']=='note_on' else 128)+r['channel'],r['key'],r['velocity']) for r in e['events']]
        assert events==public
        signal=np.zeros((e['frames'],2),dtype='<f4').tobytes();assert signal==(PACKAGE/e['signal']).read_bytes()
    measurements=mutations=0;checks=[]
    for e in ev.values():
        y=tool.audio(PACKAGE/e['reference'],e['frames'])
        result=tool.compare(y,y,e['metric'],e['sample_rate_hz']);assert result['pass'],e['id']
        measurements+=len(result['measurements'])
        for ch in [0,1]:
            for kind in ['silent','gain','late_gain']:
                changed=y.copy()
                if kind=='silent':changed[:,ch]=0
                elif kind=='gain':changed[:,ch]*=1.02
                else:
                    start=max(w[1] for w in e['metric']['onset_windows']);changed[start:,ch]*=1.02
                try:rejected=not tool.compare(changed,y,e['metric'],e['sample_rate_hz'])['pass']
                except (ValueError,ZeroDivisionError):rejected=True
                assert rejected,(e['id'],ch,kind)
                mutations+=1
        checks.append({'id':e['id'],'self_pass':True,'measurements':len(result['measurements'])})
    malformed=0
    with tempfile.TemporaryDirectory() as directory:
        p=Path(directory)/'invalid.f32';frames=next(iter(ev.values()))['frames']
        for size in [0,frames*8-4,frames*8+4]:
            p.write_bytes(b'\0'*size)
            try:tool.audio(p,frames)
            except ValueError:malformed+=1
            else:raise AssertionError('bad size accepted')
        for value in [np.nan,np.inf,-np.inf]:
            b=np.zeros((frames,2),np.float32);b[8000,1]=value;b.tofile(p)
            try:tool.audio(p,frames)
            except ValueError:malformed+=1
            else:raise AssertionError('nonfinite accepted')
        try:tool.audio(Path(directory)/'missing.f32',frames)
        except FileNotFoundError:malformed+=1
        else:raise AssertionError('missing output accepted')
    export=Path(tempfile.mkdtemp(prefix='analog-handoff-export-'))/'device-analog-v1';shutil.copytree(PACKAGE,export)
    with (export.parent/'self-comparison.json').open('w') as f:
        result=subprocess.run([sys.executable,str(export/'compare.py'),str(export/'reference')],stdout=f,check=False)
    report=json.loads((export.parent/'self-comparison.json').read_text());assert result.returncode==0 and report['pass'] and len(report['results'])==42
    assert {str(p.relative_to(export)) for p in export.rglob('*') if p.is_file()}==listed|{'manifest.json'}
    out={'status':'pass','scope':'candidate-only integrity and numerical comparison; no original code or application run','manifest_sha256':sha(PACKAGE/'manifest.json'),
        'case_count':len(cases),'evaluation_count':len(ev),'self_measurements_passed':measurements,'per_channel_mutations_rejected':mutations,'malformed_files_rejected':malformed,
        'retained_source_manifest_files_verified':len(source_manifest['files']),'exact_vectors_events_and_sample_captures_checked':len(ev),
        'isolated_export':{'directory':str(export),'cli_exit_code':result.returncode,'evaluation_count':len(report['results']),'exact_inventory':True},
        'environment':{'python':sys.version,'numpy':np.__version__,'scipy':scipy.__version__,'byteorder':sys.byteorder},'checks':checks}
    (HERE/'author-validation.json').write_text(json.dumps(out,indent=1)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='checks'},indent=1))


if __name__=='__main__':validate()
