"""Read-only assertions for authored scope/pins; never an application test."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import subprocess
from capture import extract, SOURCE, DIGEST

P = Path(__file__).resolve().parent
ROOT = P.parents[3]
load = lambda name: json.loads((P / name).read_text())
digest = lambda raw: hashlib.sha256(raw).hexdigest()
rows = extract()
assert load('source-blocks.json') == rows and len(rows) == 77
assert digest(SOURCE.read_bytes()) == DIGEST
index = {x['id']: x for x in rows}
requirements, cases = load('requirements.json'), load('cases.json')
assert len(requirements) == len({r['id'] for r in requirements}) == 29
assert len(cases) == len({c['id'] for c in cases}) == 40
assert Counter(r['strength'] for r in requirements) == {'D12': 28, 'U': 1}
req_index = {r['id']: r for r in requirements}
for r in requirements:
    assert r['target_applicability'] == 'U'
    for e in r['evidence']:
        assert e['anchor'] == index[e['block']]['anchor']
        assert e['html_line'] == index[e['block']]['html_line']
for c in cases:
    assert c['expected'] is None and c['comparison'] is None
    assert c['target_grade'] == 'U' and c['executed'] is False
    assert len(c['requirements']) == 1 and c['requirements'][0] in req_index
    assert c['evidence'] == req_index[c['requirements'][0]]['evidence']
    if c['kind'] == 'signal-obligation' or c['id'].startswith('SV-U-'):
        assert c['documentary_comparator'] is None
    if c['id'].startswith('SV-U-'):
        assert c['documentary_expected'] is None
assert {c['requirements'][0] for c in cases} == set(req_index)
for snap, canonical in [('spec-r1.md', 'wiki/specs/session-view-workflows.md'),
                        ('research-r1.md', 'wiki/research/session-view-workflows.md')]:
    assert (P / snap).read_bytes() == (ROOT / canonical).read_bytes()
    assert all(r['id'] in (P / 'spec-r1.md').read_text() for r in requirements)
for path in P.iterdir():
    if path.suffix in {'.py', '.md', '.json', '.txt'}:
        if path.suffix == '.json':
            json.loads(path.read_text())
        result = subprocess.run(['git', 'diff', '--no-index', '--check', '/dev/null', str(path)], capture_output=True)
        assert not result.stdout and not result.stderr, (path, result.stdout, result.stderr)
manifest = P / 'manifest-author-r1.json'
if manifest.exists():
    for name, info in load(manifest.name)['files'].items():
        raw = (P / name).read_bytes()
        assert len(raw) == info['bytes'] and digest(raw) == info['sha256'], name
print(json.dumps({'status': 'pass', 'scope': 'author integrity only; independent semantic review pending',
                  'source_blocks': len(rows), 'requirements': len(requirements), 'cases': len(cases),
                  'all_target_null_U_unexecuted': True, 'case_kinds': dict(Counter(c['kind'] for c in cases)),
                  'original_or_candidate_execution': False}, indent=2))
