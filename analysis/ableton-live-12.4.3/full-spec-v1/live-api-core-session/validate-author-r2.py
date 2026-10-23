"""Read-only focused successor checks; all original R1 tools remain unchanged."""
from pathlib import Path
from contextlib import redirect_stdout
from io import StringIO
import copy
import hashlib
import json

P = Path(__file__).resolve().parent
A = P / 'archive-r1'
ROOT = P.parents[3]
read = lambda path: json.loads(path.read_text())
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()


def pointer(record, path, replacement):
    keys = path.strip('/').split('/')
    for key in keys[:-1]:
        record = record[int(key)] if isinstance(record, list) else record[key]
    key = keys[-1]
    record[int(key) if isinstance(record, list) else key] = replacement


def check():
    before = {str(f.relative_to(P)): sha(f) for f in P.rglob('*') if f.is_file()}
    r1 = read(A / 'manifest-author-r1.json')
    assert sha(A / 'manifest-author-r1.json') == 'bdf008faa891620132a1e93ff20b0381f5de9418c517fbc644bda685848e65c6'
    assert len(r1['files']) == 16 and len(list(A.iterdir())) == 17
    assert set(f.name for f in A.iterdir()) == set(r1['files']) | {'manifest-author-r1.json'}
    for name, pin in r1['files'].items():
        path = A / name
        assert path.stat().st_size == pin['bytes'] and sha(path) == pin['sha256'], name
        if name not in {'requirements.json', 'member-ledger.json', 'cases.json'}:
            assert path.read_bytes() == (P / name).read_bytes(), name
    assert (A / 'manifest-author-r1.json').read_bytes() == (P / 'manifest-author-r1.json').read_bytes()
    response = read(P / 'response-r2.json')
    assert response['findings'] == ['CORE-REVIEW-001', 'CORE-REVIEW-002', 'CORE-REVIEW-003']
    assert response['review_sha256'] == sha(P / response['review']) == 'c4a95649303cfad6fa56bba492b11b1a900b2467fce9ad82f25fc00565abdddc'
    expected_evidence = dict(source='C74-LOM-SONG', block='B0175', exact_prose='If destinaton is not set or it is set to auto, the Clip is inserted into the view currently visible in the focused Live window.', optional=True, default_token=None)
    assert response['optionality_evidence'] == expected_evidence
    sources = read(P / 'source-blocks.json')
    assert expected_evidence['exact_prose'] in next(b['text'] for b in sources['C74-LOM-SONG'] if b['block'] == 'B0175')
    expected = {name: copy.deepcopy(read(A / name)) for name in ['requirements.json', 'member-ledger.json', 'cases.json']}
    requirement = next(r for r in expected['requirements.json'] if r['id'] == 'REQ-LAPI-CORE-082')
    member = next(m for m in expected['member-ledger.json'] if m['requirement'] == requirement['id'])
    for row in [requirement, member]:
        assert row['signature']['arguments'] == [dict(name='destination', type='int', optional=None, source_default=None)]
        row['signature']['arguments'][0]['optional'] = True
        assert row['unknown_fields'].count('some-argument-optionality-not-stated') == 1
        row['unknown_fields'].remove('some-argument-optionality-not-stated')
    actions = {
        'LCS-173': 'Use editable nonfrozen audio track not recording and an independently supported readable owned audio file; request creation at independently admitted member-specific position 4, retaining file reference and Arrangement clip. Units are unstated for this Track function and remain unknown.',
        'LCS-174': 'Use editable nonfrozen MIDI track not recording; request a clip at independently admitted member-specific start_time 4 and length 4, retaining Arrangement content without note/default laws. Units are unstated for this Track function and remain unknown.',
        'LCS-098': 'Use a known Arrangement position; request each source-listed format 0 through 5 in separate trials. Retain the raw result and representation without assuming a string type or frame-rate rounding/drop-frame algorithms.',
    }
    for case in expected['cases.json']:
        if case['id'] in actions:
            case['setup_and_action'] = actions[case['id']]
    for name, value in expected.items():
        assert read(P / name) == value, name
    assert len(response['field_deltas']) == 7
    reproduced = {name: copy.deepcopy(read(A / name)) for name in expected}
    for delta in response['field_deltas']:
        assert delta['file'] in reproduced
        previous = reproduced[delta['file']]
        for key in delta['json_pointer'].strip('/').split('/'):
            previous = previous[int(key)] if isinstance(previous, list) else previous[key]
        assert previous == delta['old']
        pointer(reproduced[delta['file']], delta['json_pointer'], delta['new'])
    assert reproduced == expected
    assert response['spec_replacements'] == [
        dict(old='revision: 1\n', new='revision: 2\n'),
        dict(old='manifest-author-r1.json', new='manifest-author-r2.json'),
        dict(old='`destination` (int, optionality unstated)', new='`destination` (int, optionality optional; omission explicitly supported by Song B0175 prose)'),
    ]
    expected_spec = (A / 'spec-r1.md').read_text()
    for change in response['spec_replacements']:
        assert expected_spec.count(change['old']) == 1
        expected_spec = expected_spec.replace(change['old'], change['new'])
    assert (P / 'spec-r2.md').read_text() == expected_spec
    assert response['research_replacements'] == [dict(old='revision: 1\n', new='revision: 2\n')]
    expected_research = (A / 'research-r1.md').read_text().replace('revision: 1\n', 'revision: 2\n', 1) + response['research_suffix']
    assert (P / 'research-r2.md').read_text() == expected_research
    assert (P / 'spec-r2.md').read_bytes() == (ROOT / 'wiki/specs/live-api-core-session.md').read_bytes()
    assert (P / 'research-r2.md').read_bytes() == (ROOT / 'wiki/research/live-api-core-session.md').read_bytes()
    original = (A / 'validate.py').read_text()
    adapted = original.replace('spec-r1.md', 'spec-r2.md').replace('research-r1.md', 'research-r2.md').replace('manifest-author-r1.json', 'manifest-author-r2.json')
    assert adapted.count("meta['revision'] == '1'") == 1
    adapted = adapted.replace("meta['revision'] == '1'", "meta['revision'] == '2'")
    old_guard = "assert 'optional' in body"
    assert adapted.count(old_guard) == 1
    # Only this member's explicit omission prose extends the historical marker check.
    new_guard = "assert 'optional' in body or (r['title'] == 'Song.capture_midi' and a['name'] == 'destination' and a['type'] == 'int' and a['source_default'] is None and " + repr(expected_evidence['exact_prose']) + " in body)"
    adapted = adapted.replace(old_guard, new_guard)
    output = StringIO()
    with redirect_stdout(output):
        exec(compile(adapted, str(P / 'validate.py'), 'exec'), {'__file__': str(P / 'validate.py'), '__name__': '_core_r2_readonly_integrity'})
    result = json.loads(output.getvalue())
    assert result['status'] == 'pass' and result['writes'] is False
    manifest_path = P / 'manifest-author-r2.json'
    if manifest_path.exists():
        manifest = read(manifest_path)
        assert len(manifest['files']) == 39 and len(manifest['archive_pins']) == 17
        for record in manifest['archive_pins']:
            path = P / record['file']
            assert path.stat().st_size == record['bytes'] and sha(path) == record['sha256']
        assert manifest['review_sha256'] == response['review_sha256']
    assert before == {str(f.relative_to(P)): sha(f) for f in P.rglob('*') if f.is_file()}
    result.update(revision=2, resolved_findings=response['findings'], archived_R1_payloads=16,
                  archived_R1_files_with_manifest=17, exact_JSON_field_deltas=7,
                  changed_cases=['LCS-173 setup_and_action', 'LCS-174 setup_and_action', 'LCS-098 setup_and_action'],
                  only_changed_requirement_and_member='REQ-LAPI-CORE-082 destination optionality and removal of false omission flag',
                  sources_counts_other_actions_contracts_oracles_unchanged=True, packet_mutated_by_validation=False)
    return result


if __name__ == '__main__':
    print(json.dumps(check(), indent=2))
