"""Read-only r2 correction/archive checks; keep the frozen r1 validator unchanged."""
from pathlib import Path
import hashlib
import json

P = Path(__file__).resolve().parent
A = P / 'archive-r1'
ROOT = P.parents[3]
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
read = lambda path: json.loads(path.read_text())


def check():
    before = {str(q.relative_to(P)): sha(q) for q in P.rglob('*') if q.is_file()}
    r1 = read(A / 'manifest-author-r1.json')
    assert sha(A / 'manifest-author-r1.json') == '14827b06b4f86e8e67652127bc14e6603c1115db6eb510842f523bcf1cfd0062'
    assert len(r1['files']) == 15 and len(list(A.iterdir())) == 18
    for name, pin in r1['files'].items():
        path = A / name
        assert path.stat().st_size == pin['bytes'] and sha(path) == pin['sha256'], name
        if name not in {'requirements.json', 'cases.json'}:
            assert path.read_bytes() == (P / name).read_bytes(), name
    for pin in read(A / 'freeze-author-r1.json')['pins']:
        path = A / pin['file']
        assert path.stat().st_size == pin['bytes'] and sha(path) == pin['sha256']
    for name in ('manifest-author-r1.json', 'freeze-author-r1.json', 'validation-author-r1.json'):
        assert (A / name).read_bytes() == (P / name).read_bytes(), name
    response = read(P / 'response-r2.json')
    assert response['finding'] == 'RC-REVIEW-001'
    review = P / response['review']
    assert sha(review) == response['review_sha256']
    for name, target, field in [('requirements.json', 'REQ-REMOTE-WORKFLOW-023', 'contract'),
                                ('cases.json', 'RC-023', 'source_claim')]:
        old, new = read(A / name), read(P / name)
        assert len(old) == len(new)
        for previous, current in zip(old, new):
            assert previous['id'] == current['id']
            if current['id'] == target:
                expected = dict(previous)
                assert response['old_predicate'] in previous[field]
                expected[field] = previous[field].replace(response['old_predicate'], response['new_predicate'])
                assert current == expected, target
            else:
                assert previous == current, current['id']
    old_spec = (A / 'spec-r1.md').read_text()
    expected_spec = old_spec.replace(response['old_predicate'], response['new_predicate']).replace(
        'revision: 1\n', 'revision: 2\n', 1).replace('manifest-author-r1.json', 'manifest-author-r2.json')
    assert (P / 'spec-r2.md').read_text() == expected_spec
    original = (P / 'validate.py').read_text()
    # Replay existing read-only integrity logic against the new manifest/snapshots.
    # No old schema/file is overwritten, and the guarded main remains inactive.
    adapted = original.replace('spec-r1.md', 'spec-r2.md').replace('research-r1.md', 'research-r2.md').replace(
        'manifest-author-r1.json', 'manifest-author-r2.json')
    namespace = {'__file__': str(P / 'validate.py'), '__name__': '_remote_r2_integrity'}
    exec(compile(adapted, str(P / 'validate.py'), 'exec'), namespace)
    result = namespace['check']()
    manifest = read(P / 'manifest-author-r2.json')
    assert len(manifest['archive_pins']) == 18
    for pin in manifest['archive_pins']:
        path = P / pin['file']
        assert path.stat().st_size == pin['bytes'] and sha(path) == pin['sha256']
    assert before == {str(q.relative_to(P)): sha(q) for q in P.rglob('*') if q.is_file()}
    result.update({'revision': 2, 'finding': 'RC-REVIEW-001', 'archived_r1_payloads': 15,
                   'archived_r1_files_with_seal_validation_freeze': 18,
                   'only_changed_requirement': 'REQ-REMOTE-WORKFLOW-023 contract',
                   'only_changed_case': 'RC-023 source_claim',
                   'source_evidence_actions_fixtures_oracles_counts_unchanged': True,
                   'packet_mutated_by_validation': False})
    return result


if __name__ == '__main__':
    print(json.dumps(check(), indent=2))
