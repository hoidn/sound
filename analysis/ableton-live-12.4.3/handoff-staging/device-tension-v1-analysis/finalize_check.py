"""Verify metadata-only finalization against the approved private snapshot."""
import hashlib
import json
from pathlib import Path
import re

HERE=Path(__file__).resolve().parent
PAYLOAD=HERE.with_name('device-tension-v1')


def sha(data):return hashlib.sha256(data).hexdigest()


def main():
    before=json.loads((HERE/'approved-pre-release-manifest.json').read_text())
    assert sha((HERE/'approved-pre-release-manifest.json').read_bytes())=='5c42bd304d14e2d2ac6eba02c8ee3dfe704c1977bbd19c500ede759529833fe4'
    old_files={r['path']:r for r in before['files']}
    protected=[name for name in old_files if name=='compare.py' or name.startswith(('reference/','signals/'))]
    for name in protected:
        data=(PAYLOAD/name).read_bytes();assert sha(data)==old_files[name]['sha256'] and len(data)==old_files[name]['bytes'],name
    old_bytes=(HERE/'approved-pre-release-cases.json').read_bytes();assert sha(old_bytes)==old_files['cases.json']['sha256']
    new_bytes=(PAYLOAD/'cases.json').read_bytes()
    assert new_bytes==old_bytes.replace(b'"status": "reviewed-staged"',b'"status": "released"',1)
    old_cases=json.loads(old_bytes);new_cases=json.loads(new_bytes)
    assert old_cases['cases']==new_cases['cases']
    assert old_cases.pop('status')=='reviewed-staged' and new_cases.pop('status')=='released' and old_cases==new_cases
    manifest=json.loads((PAYLOAD/'manifest.json').read_text());assert manifest['release_status']=='released' and manifest['release_date']=='2026-10-19'
    assert manifest['reviewer_disposition']==before['reviewer_disposition']
    assert manifest['specification']['parent_revision']==2
    actual={str(p.relative_to(PAYLOAD)) for p in PAYLOAD.rglob('*') if p.is_file()}
    assert actual=={r['path'] for r in manifest['files']}|{'manifest.json'}
    assert not any(p.is_symlink() for p in PAYLOAD.rglob('*'))
    for row in manifest['files']:
        path=PAYLOAD/row['path'];data=path.read_bytes();assert sha(data)==row['sha256'] and len(data)==row['bytes']
        if path.suffix=='.md':
            text=path.read_text()
            for link in re.findall(r'\]\(([^)]+)\)',text):assert (path.parent/link.split('#')[0]).is_file()
            assert 'unreviewed' not in text.lower() and 'unpublished' not in text.lower()
    final_hash=sha((PAYLOAD/'manifest.json').read_bytes())
    evidence=json.loads((HERE/'approved-pre-release-reviewer-validation.json').read_text())
    assert evidence['manifest_sha256']=='5c42bd304d14e2d2ac6eba02c8ee3dfe704c1977bbd19c500ede759529833fe4'
    evidence['approved_pre_finalization_manifest_sha256']=evidence['manifest_sha256']
    evidence['manifest_sha256']=final_hash
    evidence['finalization']={'status':'pass','scope':'Only release metadata and four prose documents changed; cases top-level status is the sole JSON case-file change','case_evaluation_objects_identical':True,'numeric_code_reference_signal_files_byte_identical':protected,'numeric_checks_rerun':False,'reason':'No numerical inputs, audio, signals, code, modes, windows or bounds changed','inventory_links_hashes':'pass','final_prose_read':'all four clean Markdown documents reread after final metadata promotion','local_publication':'pending; parent coordinator will copy exact bytes'}
    (HERE/'reviewer-validation.json').write_text(json.dumps(evidence,indent=1,allow_nan=False)+'\n')
    (HERE/'finalization-validation.json').write_text(json.dumps({'status':'pass','manifest_sha256':final_hash,'protected_files_identical':len(protected),'case_evaluation_objects_identical':True,'sole_case_metadata_change':'status reviewed-staged -> released','inventory_links_hashes':'pass','numeric_checks_rerun':False,'publication':'pending'},indent=1)+'\n')
    print(json.dumps({'status':'pass','manifest_sha256':final_hash,'protected_files_identical':len(protected),'publication':'pending'},indent=1))


if __name__=='__main__':main()
