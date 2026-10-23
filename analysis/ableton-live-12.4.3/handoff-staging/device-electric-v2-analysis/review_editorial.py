"""Independent check of Electric's editorial supersession; no device execution."""
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
PACKAGE=HERE.with_name('device-electric-v2')
OLD=ROOT/'handoff/device-electric-v1'
OLD_SHA='1f4e84947bf1ffa9fd605f73381a9778ad8ab4af1b6f9e14662458d606e0dd4f'
sha=lambda path:hashlib.sha256(path.read_bytes()).hexdigest()


def check():
    assert sha(OLD/'manifest.json')==OLD_SHA
    original=json.loads((OLD/'manifest.json').read_text())
    current=json.loads((PACKAGE/'manifest.json').read_text())
    for package,manifest in [(OLD,original),(PACKAGE,current)]:
        actual={str(p.relative_to(package)) for p in package.rglob('*') if p.is_file()}
        assert actual=={r['path'] for r in manifest['files']}|{'manifest.json'}
        assert not any(p.is_symlink() for p in package.rglob('*'))
        for r in manifest['files']:
            p=package/r['path'];assert sha(p)==r['sha256'] and p.stat().st_size==r['bytes']
    paths={r['path'] for r in original['files']}
    assert paths=={r['path'] for r in current['files']}
    changes=sorted(path for path in paths if (OLD/path).read_bytes()!=(PACKAGE/path).read_bytes())
    assert changes==['README.md','REVIEW.md','spec.md'],changes
    before=(OLD/'spec.md').read_text()
    after=(PACKAGE/'spec.md').read_text()
    corrected=before.replace('scheduling. No\nimplementation may use this reviewed release only inside a restricted workspace.',
                             'scheduling.\n\nImplementation may use this reviewed release only inside a restricted workspace.')
    assert corrected==after,'unexpected contract change'
    assert 'Implementation may use this reviewed release only inside a restricted workspace.' in after
    assert not re.search(r'No\s+implementation may use',after)
    assert 'pending review' not in (PACKAGE/'README.md').read_text()
    assert current['supersedes']['release']=='device-electric-v1'
    assert current['supersedes']['manifest_sha256']==OLD_SHA
    for key in ['partial_requirement_scopes','unreleased_requirements','compatibility_dimensions','exclusions','case_count','evaluation_count']:
        assert current[key]==original[key],key
    proof=ROOT/'analysis/ableton-live-12.4.3/handoff-staging/device-electric-v1-analysis'
    inherited={}
    for filename in ['review-validation.json','author-validation.json']:
        record=json.loads((proof/filename).read_text());assert record['status']=='pass' and record['manifest_sha256']==OLD_SHA
        inherited[filename]={'sha256':sha(proof/filename),'result':record}
    links=0
    forbidden=re.compile(r'0x[0-9a-fA-F]{5,}|FUN_|DAT_|_ZN|::|analysis/|wiki/|/home/|/var/|/tmp/|CreateInstanceU|SetParameterA|CalcA|xexec|Ghidra|vtable')
    for path in PACKAGE.rglob('*'):
        if path.suffix not in {'.md','.json','.py'}:continue
        text=path.read_text();assert not forbidden.search(text),(path.name,forbidden.search(text).group())
        if path.suffix=='.md':
            for link in re.findall(r'\]\(([^)\s]+)\)',text):
                dest=(path.parent/link).resolve();assert dest.is_file() and PACKAGE.resolve() in dest.parents,(path,link)
                links+=1
    program="""import importlib.util,json,sys
from pathlib import Path
p=Path(sys.argv[1]);spec=importlib.util.spec_from_file_location('comparison',p/'compare.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
evaluations=[e for c in json.loads((p/'cases.json').read_text())['cases'] for e in c['evaluations']]
chosen=[next(e for e in evaluations if e['metric']['kind']!='silence' and e['metric']['partials']),next(e for e in evaluations if e['metric']['kind']=='silence'),next(e for e in evaluations if e['during_processing'])]
results=[]
for e in chosen:
 result=m.compare(m.audio(p/e['reference'],e['frames']),e);assert result['pass'],e['id'];results.append({'id':e['id'],**result})
print(json.dumps({'pass':True,'representative_evaluations':results}))
"""
    with tempfile.TemporaryDirectory(prefix='electric-v2-review-') as tmp:
        export=Path(tmp)/PACKAGE.name;shutil.copytree(PACKAGE,export)
        for path in [*paths,'manifest.json']:
            assert (PACKAGE/path).read_bytes()==(export/path).read_bytes()
        run=subprocess.run([sys.executable,'-I','-B','-c',program,str(export)],capture_output=True,text=True)
        assert run.returncode==0,(run.returncode,run.stderr)
        smoke=json.loads(run.stdout);assert smoke['pass'] and len(smoke['representative_evaluations'])==3
    return {'date':'2026-10-19','predecessor_manifest_sha256':OLD_SHA,'manifest_sha256':sha(PACKAGE/'manifest.json'),
            'predecessor_payload_files_verified':len(paths),'unchanged_payload_files':len(paths)-len(changes),
            'changed_payload_files':changes,'numerical_artifacts_unchanged':True,'final_contract_delta':'Only contradictory permission sentence corrected; paragraph wrapping changed',
            'original_source_review_inherited':inherited,'isolated_measurement_smoke':smoke,'markdown_links_verified':links,
            'inventory_hash_size_mismatches':[],'sanitizer_hits':[],'published_predecessor_unchanged':sha(OLD/'manifest.json')==OLD_SHA,
            'prose_read_after_metadata_edits':True,'original_or_candidate_renderer_executed':False}


if __name__=='__main__':
    report=check();(HERE/'review-validation.json').write_text(json.dumps(report,indent=1)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='original_source_review_inherited'},indent=1))
