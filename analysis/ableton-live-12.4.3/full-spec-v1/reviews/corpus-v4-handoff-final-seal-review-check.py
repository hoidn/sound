"""Focused final metadata/hash checks only; no comparator or numeric replay."""
from pathlib import Path
import hashlib
import json
import re
import sys

ROOT = Path('/home/ollie/Documents/sound')
BASE = ROOT/'analysis/ableton-live-12.4.3'
P = BASE/'handoff-staging/device-corpus-v4'
A = P.parent/'device-corpus-v4-analysis'
R = BASE/'full-spec-v1/reviews'


def identity(path):
    raw = path.read_bytes()
    return dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())


def digest(text):
    raw=text.encode(); return dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())


def main():
    assert sys.argv[1:] == ['--check']
    paths = set(p for p in P.rglob('*') if p.is_file())
    paths.update(p for p in R.glob('corpus-v4-handoff-review*') if p.is_file())
    paths.update((A/n) for n in ('final-metadata-before.json','final-metadata-change.json','final-metadata-change-r2.json'))
    paths.add(Path(__file__))
    before_watch={str(p):identity(p) for p in sorted(paths)}
    before=json.loads((A/'final-metadata-before.json').read_text())
    change=json.loads((A/'final-metadata-change-r2.json').read_text())
    first=json.loads((A/'final-metadata-change.json').read_text())
    assert identity(P/'manifest.json')==dict(bytes=20279,sha256='5375571b14812cfc901e0970ab0c627b2e6a6a1a51e0ab3e4c6c29f9a959a1ad')
    assert identity(A/'final-metadata-before.json')=={k:change['before_snapshot'][k] for k in ('bytes','sha256')}
    assert identity(A/'final-metadata-change.json')=={k:change['correction']['supersedes_audit_record_only'][k] for k in ('bytes','sha256')}
    old_inventory={r['path']:{k:r[k] for k in ('bytes','sha256')} for r in before['all_before_files']}
    assert len(old_inventory)==88
    old_manifest=json.loads(before['texts']['manifest.json'])
    assert digest(before['texts']['manifest.json'])==old_inventory['manifest.json']==dict(bytes=20042,sha256='8b306ac4e25128b2790bdb46e8e9bd1dae9e6fe06770755a4b126bc714f78c5d')
    assert old_inventory=={**{row['path']:{k:row[k] for k in ('bytes','sha256')} for row in old_manifest['files']},'manifest.json':digest(before['texts']['manifest.json'])}
    manifest=json.loads((P/'manifest.json').read_text())
    assert {k:v for k,v in old_manifest.items() if k!='files'}==change['manifest_before_noninventory']
    assert {k:v for k,v in manifest.items() if k!='files'}==change['manifest_after_noninventory']
    differing_old=[k for k in change['manifest_before_noninventory'] if change['manifest_before_noninventory'][k]!=first['manifest_before_noninventory'][k]]
    assert differing_old==['compatibility_dimensions','readiness']
    assert {k:v for k,v in change.items() if k not in ('captured_utc','manifest_before_noninventory','correction')}=={k:v for k,v in first.items() if k not in ('captured_utc','manifest_before_noninventory','correction')}
    for name,ops in change['literal_operations'].items():
        if name=='cases.json':
            rendered=(P/name).read_text()
            for op in reversed(ops):
                assert rendered.count(op['after'])==1
                rendered=rendered.replace(op['after'],op['before'])
            assert digest(rendered)==old_inventory[name]
            assert json.loads(rendered)['cases']==json.loads((P/name).read_text())['cases']
        else:
            rendered=before['texts'][name]
            assert digest(rendered)==old_inventory[name]
            for op in ops:
                assert rendered.count(op['before'])==1
                rendered=rendered.replace(op['before'],op['after'])
            assert rendered==(P/name).read_text()
    assert digest(before['texts']['REVIEW.md'])==old_inventory['REVIEW.md']
    unchanged=[];changed=[]
    for name,old in old_inventory.items():
        (unchanged if identity(P/name)==old else changed).append(name)
    assert set(changed)=={'README.md','REVIEW.md','spec.md','cases.json','manifest.json'} and len(unchanged)==83
    for row in change['identities']:
        assert old_inventory[row['path']]==dict(bytes=row['before_bytes'],sha256=row['before_sha256'])
        assert identity(P/row['path'])==dict(bytes=row['after_bytes'],sha256=row['after_sha256'])
    assert len(manifest['files'])==87
    assert {str(p.relative_to(P)) for p in P.rglob('*') if p.is_file()}=={'manifest.json'}|{r['path'] for r in manifest['files']}
    for row in manifest['files']:
        assert identity(P/row['path'])=={k:row[k] for k in ('bytes','sha256')}
    allowed={'release_status','release_date','review','readiness','compatibility_dimensions','files'}
    assert {k:v for k,v in old_manifest.items() if k not in allowed}=={k:v for k,v in manifest.items() if k not in allowed}
    assert manifest['compatibility_dimensions']|{'audio':''}==old_manifest['compatibility_dimensions']|{'audio':''}
    assert {k:v for k,v in manifest['readiness'].items() if k not in ('handoff_review','numeric_validation')}=={k:v for k,v in old_manifest['readiness'].items() if k not in ('handoff_review','numeric_validation')}
    assert manifest['release_status']=='reviewed-local-release' and manifest['release_date']=='2026-10-20'
    assert manifest['review']['status']=='approved-finite-scope' and manifest['review']['findings']==[]
    cases=json.loads((P/'cases.json').read_text())
    assert cases['status']=='reviewed-finite-scope' and len(cases['cases'])==26
    assert sum(len(c['evaluations']) for c in cases['cases'])==72
    assert len(list(P.rglob('*.f32')))==81 and identity(P/'compare.py')==old_inventory['compare.py']
    links=0
    for p in P.rglob('*'):
        if p.is_file() and p.suffix!='.f32':
            text=p.read_text();assert all(line==line.rstrip() for line in text.splitlines())
            assert not re.search(r'/home/|/var/tmp|analysis/|wiki/research|0x10[0-9a-fA-F]{6}',text)
            if p.suffix=='.md':
                for target in re.findall(r'\]\(([^)]+)\)',text):
                    assert (p.parent/target).is_file();links+=1
    assert before_watch=={str(p):identity(p) for p in sorted(paths)}
    print(json.dumps(dict(status='PASS exact final tree; metadata-only correction',manifest=identity(P/'manifest.json'),
        payloads=87,tree_files=88,changed=changed,unchanged=83,case_objects_unchanged=26,evaluations_unchanged=72,
        F32_unchanged=81,comparator_unchanged=True,literal_operations=sum(map(len,change['literal_operations'].values())),
        corrected_before_projection_fields=differing_old,first_audit_record_preserved=True,links=links,
        watched=len(paths),watch_unchanged=True,watch_sha256=hashlib.sha256(json.dumps(before_watch,sort_keys=True).encode()).hexdigest(),
        numerical_replays=0,original_calls=0,application_grade=None),indent=2))


if __name__=='__main__':
    main()
