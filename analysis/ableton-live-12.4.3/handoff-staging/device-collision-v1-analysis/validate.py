"""Author checks only. No original renderer is imported or executed."""
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import re
import shutil
import struct
import subprocess
import sys
import tempfile

HERE=Path(__file__).resolve().parent
PAYLOAD=HERE.with_name('device-collision-v1')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    spec=importlib.util.spec_from_file_location('collision_measurement',PAYLOAD/'compare.py')
    comparator=importlib.util.module_from_spec(spec);spec.loader.exec_module(comparator)
    cases=json.loads((PAYLOAD/'cases.json').read_text())['cases'];assert len(cases)==2
    results=[]
    for case in cases:
        path=PAYLOAD/case['reference'];data,ref=comparator.audio(path,case['frames'])
        values=case['parameter_values'];assert len(values)==139
        for row in values:
            assert struct.pack('<f',row['value']).hex()==row['binary32_hex']
        assert comparator.measure(ref,ref,case['metric'])['pass']
        for name,mutation in [('silence',tuple(0.0 for x in ref)),('gain2',tuple(2*x for x in ref))]:
            measured=comparator.measure(mutation,ref,case['metric'])
            expected=(case['metric']['kind']=='peak')
            assert measured['pass']==expected,(case['id'],name,measured)
            results.append({'case':case['id'],'mutation':name,'expected_pass':expected,**measured})
        if case['metric']['kind']=='peak':
            injected=list(ref);injected[100]=1e-3
            assert not comparator.measure(tuple(injected),ref,case['metric'])['pass']
            results.append({'case':case['id'],'mutation':'audible injection','expected_pass':False,'pass':False})
        with tempfile.TemporaryDirectory(prefix='collision-invalid-') as tmp:
            tmp=Path(tmp)
            invalid={'empty':b'','truncated':data[:-4],'extra':data+b'\0'*8,'odd_bytes':data+b'\0', 'NaN':struct.pack('<f',math.nan)+data[4:],'positive infinity':struct.pack('<f',math.inf)+data[4:],'negative infinity':struct.pack('<f',-math.inf)+data[4:]}
            for name,broken in invalid.items():
                p=tmp/'bad.f32';p.write_bytes(broken)
                try:
                    comparator.audio(p,case['frames'])
                except ValueError:
                    results.append({'case':case['id'],'malformed':name,'rejected':True})
                else:
                    raise AssertionError((case['id'],name,'accepted malformed audio'))
        for bad in [(),tuple(math.nan for _ in ref)]:
            try:comparator.measure(bad,ref,case['metric'])
            except ValueError:pass
            else:raise AssertionError('invalid direct measurement accepted')
    manifest=json.loads((PAYLOAD/'manifest.json').read_text());actual={str(p.relative_to(PAYLOAD)) for p in PAYLOAD.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
    expected={r['path'] for r in manifest['files']}|{'manifest.json'};assert actual==expected
    assert not any(p.is_symlink() for p in PAYLOAD.rglob('*'))
    for row in manifest['files']:
        data=(PAYLOAD/row['path']).read_bytes();assert digest(data)==row['sha256'] and len(data)==row['bytes']
    forbidden=[r'\bDCL-\d+',r'\.bundle',r'raw/',r'recovery/',r'run_collision',r'xdev',r'SetParameter',r'0x[0-9a-fA-F]{5,}',r'/home/',r'/var/tmp/',r'\.script',r'__ZN',r'Resonator1/',r'ListeningXL',r'NoiseAmount']
    for p in PAYLOAD.rglob('*'):
        if p.is_file() and p.suffix in ['.md','.json','.py']:
            text=p.read_text()
            for pattern in forbidden:assert not re.search(pattern,text),(p,pattern)
            if p.suffix=='.md':
                for target in re.findall(r'\]\(([^)]+)\)',text):
                    if not target.startswith(('https://','http://')):assert (p.parent/target.split('#')[0]).is_file(),(p,target)
    export=Path(tempfile.mkdtemp(prefix='collision-isolated-export-'))/'device-collision-v1'
    shutil.copytree(PAYLOAD,export,ignore=shutil.ignore_patterns('__pycache__'))
    completed=subprocess.run([sys.executable,'-I',str(export/'compare.py'),str(export/'reference')],capture_output=True,text=True,cwd=export.parent,check=False)
    self_result=json.loads(completed.stdout);assert completed.returncode==0 and self_result['pass'] and len(self_result['results'])==2
    bad_dir=export.parent/'invalid';bad_dir.mkdir()
    missing=subprocess.run([sys.executable,'-I',str(export/'compare.py'),str(bad_dir)],capture_output=True,text=True,cwd=export.parent,check=False)
    assert missing.returncode==1 and not json.loads(missing.stdout)['pass']
    report={'pass':True,'case_count':len(cases),'self_comparison':self_result,'mutation_and_malformed_checks':results,'inventory_exact':True,'links_resolve':True,'source_exclusion_scan':'pass; requires independent semantic review','isolated_export':str(export),'isolated_cli_exit_code':completed.returncode,'missing_files_cli_exit_code':missing.returncode,'manifest_sha256':digest((PAYLOAD/'manifest.json').read_bytes()),'limitations':'Self-comparison and mutations measure tool behavior; no original/candidate rendering or arm64 comparison. Silence/gain mutations validly pass the effectively silent boundary.'}
    (HERE/'author-validation.json').write_text(json.dumps(report,indent=1,allow_nan=False)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ['mutation_and_malformed_checks','self_comparison']},indent=1))


if __name__=='__main__':main()
