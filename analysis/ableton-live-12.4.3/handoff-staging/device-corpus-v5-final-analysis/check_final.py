"""Read-only metadata/text/hash verification; no measurement or audio imports."""
from pathlib import Path
import copy
import hashlib
import json
import re
import sys

HERE = Path(__file__).resolve().parent
FINAL = HERE.parent/'device-corpus-v5-final'


def identity(path):
    raw = path.read_bytes()
    return {'path': str(path), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def reverse_json(value, operations):
    value = copy.deepcopy(value)
    for operation in operations:
        parts = operation['pointer'].strip('/').split('/')
        target = value
        for part in parts[:-1]:
            target = target[int(part)] if isinstance(target, list) else target[part]
        key = int(parts[-1]) if isinstance(target, list) else parts[-1]
        assert target[key] == operation['after']
        target[key] = operation['before']
    return value


def main():
    if sys.argv[1:] != ['--check']:
        raise SystemExit('Read-only --check only; no numeric/audio/native execution.')
    pins = json.loads((HERE/'inputs.json').read_text())['pins']
    roles = {r['role']: Path(r['path']) for r in pins}
    watched = set(roles.values()) | {p for p in FINAL.rglob('*') if p.is_file()} | {p for p in HERE.iterdir() if p.is_file()}
    for row in pins:
        assert identity(Path(row['path'])) == {k: row[k] for k in ['path', 'bytes', 'sha256']}
    for role in ['R1_stage', 'R1_preflight', 'R2_stage', 'R2_preflight', 'numeric_manifest']:
        manifest = roles[role]
        for row in json.loads(manifest.read_text())['files']:
            p = manifest.parent/row['path']
            got = identity(p)
            assert got['bytes'] == row['bytes'] and got['sha256'] == row['sha256']
            watched.add(p)
    before = {p: identity(p) for p in watched}
    delta = json.loads((HERE/'delta.json').read_text())
    old = roles['R2_stage'].parent
    changed = sorted(str(p.relative_to(FINAL)) for p in FINAL.rglob('*') if p.is_file() and p.read_bytes() != (old/p.relative_to(FINAL)).read_bytes())
    assert changed == delta['only_changed_paths'] == ['README.md', 'REVIEW.md', 'cases.json', 'manifest.json', 'spec.md']
    assert {str(p.relative_to(FINAL)) for p in FINAL.rglob('*') if p.is_file()} == {str(p.relative_to(old)) for p in old.rglob('*') if p.is_file()}
    for name, record in delta['files'].items():
        assert identity(old/name) == record['before'] and identity(FINAL/name) == record['after']
        if record['kind'] == 'literal-text':
            restored = (FINAL/name).read_text()
            for op in reversed(record['operations']):
                assert restored.count(op['after']) == 1
                restored = restored.replace(op['after'], op['before'], 1)
            assert restored.encode() == (old/name).read_bytes()
        else:
            restored = reverse_json(json.loads((FINAL/name).read_text()), record['operations'])
            assert (json.dumps(restored, indent=2)+'\n').encode() == (old/name).read_bytes()
    original_cases = (old/'cases.json').read_text()
    final_cases = (FINAL/'cases.json').read_text()
    assert original_cases.split('  "cases": [', 1)[1] == final_cases.split('  "cases": [', 1)[1]
    groups = json.loads(final_cases)['cases']
    assert len(groups) == 27 and sum(len(c['evaluations']) for c in groups) == 73
    assert 'author-freeze history' in json.loads(final_cases)['status']
    a = (old/'spec.md').read_text().split('## Input and protocol\n', 1)[1].split('## Proposed changes from release4 to release5', 1)[0]
    b = (FINAL/'spec.md').read_text().split('## Input and protocol\n', 1)[1].split('## Changes from release4 to release5', 1)[0]
    assert a == b, 'Normative body and historical sections must remain literal'
    for name in ['compare.py', 'AGENTS.md']:
        assert (FINAL/name).read_bytes() == (old/name).read_bytes()
    fixtures = [p for p in FINAL.rglob('*.f32')]
    assert len(fixtures) == 82
    assert all(p.read_bytes() == (old/p.relative_to(FINAL)).read_bytes() for p in fixtures)
    review = json.loads(roles['content_review'].read_text())
    assert review['required_findings'] == [] and review['disposition'] == 'APPROVED_FINITE_CONTENT_AND_ACTUAL_VALIDATION_PENDING_FINAL_METADATA_SEAL'
    manifest = json.loads((FINAL/'manifest.json').read_text())
    assert manifest['release_status'] == 'reviewed-finite-scope-ready-for-coordinator-publication'
    assert manifest['supersedes'] == 'device-corpus-v4' and len(manifest['files']) == 88
    assert manifest['review']['reviewers'] == ['delay_reverb_correction (separate Codex handoff-review context)']
    assert '73reference-self' in manifest['readiness']['numeric_validation'] and '4799measurements' in manifest['readiness']['numeric_validation']
    assert 'fixture author-freeze history' in manifest['readiness']['handoff_review']
    assert {r['path'] for r in manifest['files']} == {str(p.relative_to(FINAL)) for p in FINAL.rglob('*') if p.is_file() and p.name != 'manifest.json'}
    for row in manifest['files']:
        got = identity(FINAL/row['path'])
        assert got['bytes'] == row['bytes'] and got['sha256'] == row['sha256']
    links = 0
    for p in [p for p in FINAL.iterdir() if p.is_file()] + [p for p in HERE.iterdir() if p.is_file()]:
        text = p.read_text()
        assert text.endswith('\n') and all(line.rstrip() == line for line in text.splitlines())
        if p.parent == FINAL:
            assert not re.search(r'/home/|/tmp/|analysis/|wiki/research/|0x[0-9a-fA-F]{8,}', text)
        if p.suffix == '.md':
            for target in re.findall(r'\]\(([^)]+)\)', text):
                local = target.split('#', 1)[0]
                if local and not local.startswith(('http:', 'https:')):
                    assert (p.parent/local).is_file(), (p, target)
                    links += 1
    seal = HERE/'manifest.json'
    if seal.exists():
        inventory = json.loads(seal.read_text())['files']
        assert {r['path'] for r in inventory} == {p.name for p in HERE.iterdir() if p.is_file() and p != seal}
        for row in inventory:
            got = identity(HERE/row['path'])
            assert got['bytes'] == row['bytes'] and got['sha256'] == row['sha256']
    assert before == {p: identity(p) for p in watched}
    print(json.dumps({'status': 'PASS final metadata only', 'changed_paths': changed,
                     'all27_groups_and73_evaluations_exact': True, 'F32_exact': 82,
                     'normative_body_exact': True, 'reversible': True, 'links': links,
                     'watched': len(watched), 'unchanged': True,
                     'numeric_or_audio_execution': 0, 'publication': False}, indent=2))


if __name__ == '__main__':
    main()
