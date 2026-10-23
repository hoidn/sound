"""Read-only evidence/author consistency checks; no workspace or application execution."""
from pathlib import Path
import hashlib
import json
import runpy
import subprocess
import sys

P = Path(__file__).resolve().parent
ROOT = P.parents[3]
load = lambda name: json.loads((P / name).read_text())
sha = lambda raw: hashlib.sha256(raw).hexdigest()
source = load('source.json')
raw = (P / source['file']).read_bytes()
assert len(raw) == source['bytes'] and sha(raw) == source['sha256']
for dependency in load('dependencies.json'):
    path = ROOT / dependency['path']
    assert path.stat().st_size == dependency['bytes'] and sha(path.read_bytes()) == dependency['sha256']
parser = runpy.run_path(str(ROOT / load('dependencies.json')[0]['path']))['Chapter']()
parser.feed(raw.decode())
for i, row in enumerate(parser.rows, 1):
    row['id'] = f'CONCEPT-B{i:03d}'
assert parser.rows == load('source-blocks.json') and len(parser.rows) == 125
assert parser.rows[0]['anchor'] == 'live-concepts' and parser.rows[-1]['anchor'] == 'saving-and-exporting'
blocks = {r['id']: r for r in parser.rows}
requirements, cases = load('requirements.json'), load('cases.json')
assert len(requirements) == len({r['id'] for r in requirements}) == 13
assert len(cases) == len({c['id'] for c in cases}) == 23
assert all(r['target_applicability'] == 'U' for r in requirements)
index = {r['id']: r for r in requirements}
for r in requirements:
    for e in r['evidence']:
        assert e['anchor'] == blocks[e['block']]['anchor'] and e['html_line'] == blocks[e['block']]['html_line']
for c in cases:
    assert c['expected'] is None and c['comparison'] is None and c['target_grade'] == 'U' and c['executed'] is False
    assert c['evidence'] == index[c['requirements'][0]]['evidence']
    if c['kind'] in {'signal', 'timing'} or c['id'].startswith('WORKSPACE-U-'):
        assert c['documentary_comparator'] is None and c['documentary_expected'] is None
    if c['id'].startswith('WORKSPACE-U-'):
        assert c['documentary_expected'] is None
assert {c['requirements'][0] for c in cases} == set(index)
for snapshot, canonical in [('spec-r1.md', 'wiki/specs/application-workspace.md'), ('research-r1.md', 'wiki/research/application-workspace.md')]:
    assert (P / snapshot).read_bytes() == (ROOT / canonical).read_bytes()
sys.path.insert(0, str(ROOT / 'tools'))
import spec_browser
assert {r['id'] for r in spec_browser.spec_rows(ROOT / 'wiki/specs/application-workspace.md', (P / 'spec-r1.md').read_text())} == set(index)
for path in P.iterdir():
    if path.suffix in {'.json', '.py', '.md', '.txt'}:
        if path.suffix == '.json':
            json.loads(path.read_text())
        result = subprocess.run(['git', 'diff', '--no-index', '--check', '/dev/null', str(path)], capture_output=True)
        assert not result.stdout and not result.stderr, (path, result.stdout, result.stderr)
manifest = P / 'manifest-author-r1.json'
if manifest.exists():
    for name, info in load(manifest.name)['files'].items():
        data = (P / name).read_bytes()
        assert len(data) == info['bytes'] and sha(data) == info['sha256'], name
print(json.dumps({'status': 'pass', 'scope': 'author integrity only; separate semantic review pending', 'source_blocks': 125,
                  'requirements': 13, 'browser_requirement_ids': 13, 'cases': 23, 'all_target_null_U_unexecuted': True,
                  'original_workspace_or_candidate_execution': False}, indent=2))
