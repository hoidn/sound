"""Read-only stdlib structural check. Never imports measurement/audio code."""
from pathlib import Path
import ast
import copy
import hashlib
import json
import re
import sys

HERE = Path(__file__).resolve().parent
STAGE = HERE.parent.parent / 'device-corpus-v5-r2'


def identity(path):
    raw = path.read_bytes()
    return {'path': str(path), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def cases_check(current, previous, source):
    assert current['cases'][:-1] == previous['cases']
    assert len(current['cases']) == 27
    assert sum(len(c['evaluations']) for c in current['cases']) == 73
    group = current['cases'][-1]
    assert group['id'] == 'CORPUS-AUDIO-027'
    assert group['requirements'] == ['REQ-DEVICE-CORPUS-001', 'REQ-DEVICE-CORPUS-012']
    assert len(group['evaluations']) == 1
    expected = copy.deepcopy(source['evaluation'])
    expected['id'] = 'CORPUS-AUDIO-027-01'
    expected['reference'] = 'reference/CORPUS-AUDIO-027-01.f32'
    expected['parameter_updates'] = [{'frame': 8192, 'index': 15, 'parameter': 'ListeningXL', 'value': 0.75}]
    assert group['evaluations'][0] == expected


def code_check(current, previous, delta):
    branch, guard = delta['literal_branch'], delta['literal_hash_guard']
    assert current.count(branch) == current.count(guard) == 1
    assert current.replace(branch, '', 1).replace(guard, '', 1) == previous
    ast.parse(current)


def metadata_check(manifest, correction):
    expected = correction['after_values']
    assert set(expected) == {'/supersedes', '/change_list', '/readiness/finite_method',
                             '/readiness/parent_owner', '/readiness/handoff_review', '/readiness/numeric_validation'}
    for pointer, value in expected.items():
        actual = manifest
        for key in pointer.strip('/').split('/'):
            actual = actual[key]
        assert actual == value, pointer
    assert manifest['supersedes'] == 'device-corpus-v4'
    assert 'R7' in manifest['readiness']['parent_owner']
    assert 'pickup-step' in manifest['readiness']['finite_method']
    assert manifest['readiness']['handoff_review'].startswith('PENDING')
    assert manifest['readiness']['numeric_validation'].startswith('PENDING')
    assert 'HISTORICAL release4' in manifest['readiness']['numeric_validation']


def main():
    if sys.argv[1:] != ['--check']:
        raise SystemExit('Read-only --check only; no audio/comparator/numerical execution.')
    providers = json.loads((HERE/'providers.json').read_text())
    roles = {row['role']: Path(row['path']) for row in providers['pins']}
    watched = set(roles.values()) | {p for p in STAGE.rglob('*') if p.is_file()} | {p for p in HERE.iterdir() if p.is_file()}
    before = {p: identity(p) for p in watched}
    for row in providers['pins']:
        assert identity(Path(row['path'])) == {k: row[k] for k in ['path', 'bytes', 'sha256']}
    for role in ['v4_manifest', 'actual_validation_manifest', 'prior_candidate_manifest', 'prior_preflight_manifest']:
        manifest = roles[role]
        for row in json.loads(manifest.read_text())['files']:
            path = manifest.parent/row['path']
            got = identity(path)
            assert got['bytes'] == row['bytes'] and got['sha256'] == row['sha256']
            watched.add(path)
            before.setdefault(path, got)
    candidate = json.loads((HERE/'candidate-binding.json').read_text())
    assert identity(STAGE/'manifest.json') == candidate['manifest']
    manifest = json.loads((STAGE/'manifest.json').read_text())
    assert len(manifest['files']) == 88 and manifest['case_count'] == 27 and manifest['evaluation_count'] == 73
    assert manifest['specification']['parent_sha256'] == '26a95052328ca15005cea18bd2985ca9b1044cd7b21c02d320b512bbb308d366'
    assert manifest['review']['status'] == 'pending' and manifest['review']['reviewers'] == []
    assert {r['path'] for r in manifest['files']} == {str(p.relative_to(STAGE)) for p in STAGE.rglob('*') if p.is_file() and p.name != 'manifest.json'}
    for row in manifest['files']:
        got = identity(STAGE/row['path'])
        assert got['bytes'] == row['bytes'] and got['sha256'] == row['sha256']
    correction = json.loads((HERE/'metadata-correction.json').read_text())
    metadata_check(manifest, correction)
    prior = json.loads(roles['prior_candidate_manifest'].read_text())
    assert manifest['files'] == prior['files']
    expected_manifest = copy.deepcopy(prior)
    expected_manifest['supersedes'] = correction['after_values']['/supersedes']
    expected_manifest['change_list'] = correction['after_values']['/change_list']
    expected_manifest['readiness'] = {key: correction['after_values']['/readiness/'+key] for key in prior['readiness']}
    assert manifest == expected_manifest, 'Only the six disclosed metadata pointers may change'
    prior_runner = (roles['prior_preflight_manifest'].parent/'validate_once.py').read_text()
    assert (HERE/'validate_once.py').read_text() == prior_runner.replace(
        "STAGE = HERE.parent.parent / 'device-corpus-v5'",
        "STAGE = HERE.parent.parent / 'device-corpus-v5-r2'", 1)
    old_manifest = json.loads(roles['v4_manifest'].read_text())
    fixture_count = 0
    for row in old_manifest['files']:
        if row['path'].endswith('.f32') or row['path'] == 'AGENTS.md':
            assert (STAGE/row['path']).read_bytes() == (roles['v4_manifest'].parent/row['path']).read_bytes()
            fixture_count += row['path'].endswith('.f32')
    assert fixture_count == 81
    current = json.loads((STAGE/'cases.json').read_text())
    previous = json.loads(roles['v4_cases'].read_text())
    source = json.loads(roles['R7_case'].read_text())[0]
    cases_check(current, previous, source)
    assert identity(STAGE/'reference/CORPUS-AUDIO-027-01.f32')['sha256'] == source['evaluation']['reference']['sha256']
    delta = json.loads((HERE/'comparator-delta.json').read_text())
    code, oldcode = (STAGE/'compare.py').read_text(), roles['v4_compare'].read_text()
    code_check(code, oldcode, delta)
    adoption = json.loads(roles['R7_adoption'].read_text())
    op = adoption['only_canonical_delta_from_frozen_source']
    frozen = roles['R7_spec'].read_text()
    assert frozen.count(op['anchor']) == 1
    adopted = frozen.replace(op['anchor'], op['anchor']+op['exact_banner'], 1).encode()
    assert len(adopted) == 66141 and hashlib.sha256(adopted).hexdigest() == manifest['specification']['parent_sha256']
    rejected = []
    for label, mutation in [('wrong boundary', lambda e: e['parameter_updates'][0].update(frame=8200)),
                            ('wrong pickup', lambda e: e['parameter_updates'][0].update(index=16)),
                            ('wrong value', lambda e: e['parameter_updates'][0].update(value=0.5)),
                            ('missing update', lambda e: e.update(parameter_updates=[]))]:
        bad = copy.deepcopy(current)
        mutation(bad['cases'][-1]['evaluations'][0])
        try:
            cases_check(bad, previous, source)
        except AssertionError:
            rejected.append(label)
        else:
            raise AssertionError('unsafe case accepted: '+label)
    bad = copy.deepcopy(current)
    bad['cases'][0]['evaluations'][0]['unrequested'] = True
    try:
        cases_check(bad, previous, source)
    except AssertionError:
        rejected.append('changed old object')
    else:
        raise AssertionError('old object change accepted')
    try:
        code_check(code.replace('Pickup step reference hash differs', 'wrong hash message'), oldcode, delta)
    except AssertionError:
        rejected.append('changed fixed code/guard')
    else:
        raise AssertionError('changed guard accepted')
    for pointer, old_value in correction['before_values'].items():
        bad = copy.deepcopy(manifest)
        target = bad
        keys = pointer.strip('/').split('/')
        for key in keys[:-1]:
            target = target[key]
        target[keys[-1]] = old_value
        try:
            metadata_check(bad, correction)
        except AssertionError:
            rejected.append('stale '+pointer)
        else:
            raise AssertionError('stale metadata accepted: '+pointer)
    links = 0
    for path in [*STAGE.glob('*.md'), HERE/'README.md']:
        text = path.read_text()
        for target in re.findall(r'\]\(([^)]+)\)', text):
            local = target.split('#', 1)[0]
            if local and not local.startswith(('http:', 'https:')):
                assert (path.parent/local).is_file(), (path, target)
                links += 1
    for path in [p for p in STAGE.iterdir() if p.is_file()] + [p for p in HERE.iterdir() if p.is_file()]:
        text = path.read_text()
        assert text.endswith('\n') and all(line.rstrip() == line for line in text.splitlines())
        if path.parent == STAGE:
            assert not re.search(r'/home/|/tmp/|analysis/|wiki/research/|0x[0-9a-fA-F]{8,}', text), path
    preseal = HERE/'manifest.json'
    if preseal.exists():
        seal = json.loads(preseal.read_text())
        assert {r['path'] for r in seal['files']} == {p.name for p in HERE.iterdir() if p.is_file() and p != preseal}
        for row in seal['files']:
            got = identity(HERE/row['path'])
            assert got['bytes'] == row['bytes'] and got['sha256'] == row['sha256']
    assert before == {p: identity(p) for p in watched}
    print(json.dumps({'status': 'PASS structure only', 'old_evaluations_preserved': 72,
                     'old_F32_preserved': fixture_count, 'candidate_evaluations': 73,
                     'source_R7_adoption_reconstructed': True, 'literal_comparator_inverse': True,
                     'only_six_metadata_pointers_changed': True, 'all88_R1_payloads_unchanged': True,
                     'numerical_runner_only_fixed_path_changed': True,
                     'negative_fixtures': rejected, 'links': links, 'watched': len(watched),
                     'unchanged': True, 'audio_decodes': 0, 'comparator_execution': 0,
                     'numeric_execution': 0, 'native_calls': 0, 'grade': None}, indent=2))


if __name__ == '__main__':
    main()
