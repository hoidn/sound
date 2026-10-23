"""Read-only retained-block assessment integrity, not a semantic/runtime pass."""
from pathlib import Path
import copy
import hashlib
import json
import re
import runpy
import subprocess
import sys

assert sys.argv[1:] == ['--check'], 'Only read-only --check is supported'
P = Path(__file__).resolve().parent
R = P.parents[3]
S = P.parent / 'settings-learning'
read = lambda p: json.loads(p.read_text())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
pins = read(P / 'input-pins.json')
watched = list(P.iterdir()) + [R / x['path'] for x in pins]
before = {str(p): sha(p) for p in watched}
for pin in pins:
    path = R / pin['path']
    assert path.stat().st_size == pin['bytes'] and sha(path) == pin['sha256'], path
source = read(S / 'source.json')
raw = (S / source['file']).read_bytes()
assert len(raw) == source['bytes'] and hashlib.sha256(raw).hexdigest() == source['sha256']
# Existing analyst HTML parser only; its guarded writer is inactive under runpy.
parser = runpy.run_path(str(P.parent / 'session-workflows/capture.py'))['Chapter']()
parser.feed(raw.decode())
for i, block in enumerate(parser.rows, 1):
    block['id'] = f'SET-B{i:03d}'
blocks = read(S / 'source-blocks.json')
assert parser.rows == blocks and len(blocks) == 70
requirements, cases = read(S / 'requirements.json'), read(S / 'cases.json')


def validate(assessments, proposals):
    assert len(assessments) == len({x['id'] for x in assessments}) == 70
    assert [x['source_block'] for x in assessments] == blocks
    for i, row in enumerate(assessments):
        assert row['block_pointer'] == '/' + str(i)
        assert row['text_pointer'] == '/' + str(i) + '/text'
        assert row['source_sha256'] == source['sha256']
        assert row['scope'] == '; '.join(row['explicit_facets'])
        assert row['assessment'] and row['disposition']
        assert row['complete'] is False and row['target_applicability'] == 'U'
        assert row['behavioral_coverage_credit'] == 0
        for reference in row['existing_requirements']:
            record = requirements[int(reference['json_pointer'][1:])]
            assert (reference['id'], reference['contract']) == (record['id'], record['contract'])
        for reference in row['existing_cases']:
            record = cases[int(reference['json_pointer'][1:])]
            assert (reference['id'], reference['action']) == (record['id'], record['setup_and_action'])
    assert len(proposals) == len({x['id'] for x in proposals}) == 11
    for proposal in proposals:
        assert proposal['status'] == 'audit-proposal-only-not-normative'
        assert proposal['expected'] is None and proposal['comparison'] is None
        assert proposal['documentary_expected'] is None and proposal['documentary_comparator'] is None
        assert proposal['target_grade'] == 'U' and proposal['executed'] is False
        assert proposal['complete'] is False
        assert set(proposal['source_blocks']) <= {x['id'] for x in blocks}


assessments, proposals = read(P / 'block-assessments.json'), read(P / 'proposed-deltas.json')
validate(assessments, proposals)
for mode in ['dropped-block', 'changed-source-text', 'wrong-requirement-pointer', 'graded-proposal']:
    a, p = copy.deepcopy(assessments), copy.deepcopy(proposals)
    if mode == 'dropped-block':
        a.pop()
    elif mode == 'changed-source-text':
        a[2]['source_block']['text'] += ' altered'
    elif mode == 'wrong-requirement-pointer':
        next(x for x in a if x['existing_requirements'])['existing_requirements'][0]['json_pointer'] = '/20'
    else:
        p[0]['expected'] = 'unsupported pass'
    try:
        validate(a, p)
    except AssertionError:
        pass
    else:
        raise AssertionError('Fixture should be rejected: ' + mode)
unknowns = read(P / 'operational-unknowns.json')
assert [x['record'] for x in unknowns['requirement_records']] == [x for x in requirements if x['strength'] == 'U']
assert [x['record'] for x in unknowns['case_records']] == [x for x in cases if x['id'].startswith('SET-U-')]
for record in cases:
    assert record['expected'] is None and record['comparison'] is None
    assert record['target_grade'] == 'U' and record['executed'] is False
manifest = read(P / 'manifest.json')
assert set(before) == {str(P / n) for n in manifest['files']} | {str(P / 'manifest.json')} | {str(R / x['path']) for x in pins}
for name, record in manifest['files'].items():
    path = P / name
    assert path.stat().st_size == record['bytes'] and sha(path) == record['sha256']
for target in re.findall(r'\[[^\]]*\]\(([^)\s]+)\)', (P / 'README.md').read_text()):
    if not re.match(r'[a-zA-Z]+:', target):
        assert (P / target.split('#')[0]).exists(), target
for path in P.iterdir():
    if path.suffix in {'.json', '.py', '.md'}:
        result = subprocess.run(['git', 'diff', '--no-index', '--check', '/dev/null', str(path)], capture_output=True)
        assert result.returncode in (0, 1) and not result.stdout and not result.stderr, path
assert before == {str(p): sha(p) for p in watched}
print(json.dumps({'status': 'pass', 'writes': False, 'retained_blocks': 70, 'proposal_groups': 11,
                  'pins': len(pins), 'original_cases_retained_U': 30,
                  'rejection_fixtures': 4, 'semantic_completeness_claim': False,
                  'original_runtime_network_account_install_candidate_execution': False}, indent=2))
