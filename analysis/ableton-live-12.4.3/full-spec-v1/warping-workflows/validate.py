"""Read-only source/documentation checks. Run python -B; emits stdout only."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import re
import subprocess
import sys

P = Path(__file__).resolve().parent
ROOT = P.parents[3]
sys.path.insert(0, str(P))
from source_parser import extract
sys.path.insert(0, str(ROOT / 'tools'))
from spec_browser import spec_rows


def load(path):
    return json.loads(path.read_text())


def pin(path, record):
    data = path.read_bytes()
    assert len(data) == record['bytes'], path
    assert hashlib.sha256(data).hexdigest() == record['sha256'], path
    return data


def slug(heading):
    heading = re.sub(r'<[^>]*>|[`*]', '', heading)
    return re.sub(r'[^\w\- ]', '', heading.strip().lower()).replace(' ', '-')


sources = load(P / 'sources.json')
assert len(sources) == 1 and sources[0] == load(P / 'capture.json')
source = sources[0]
assert source['id'] == 'D12-WARP-WORKFLOWS'
assert source['url'] == source['final_url'] == 'https://www.ableton.com/en/live-manual/12/audio-clips-tempo-and-warping/'
assert source['bytes'] == 283979
assert source['sha256'] == '295a442252730b7f1bb6154b9cbfe041f09c6d40d45d487a42e793ae8423c2ad'
source_bytes = pin(P / source['path'], source)
assert 'Version 12' in source['declared_version'] and '12.4.3 applicability unknown' in source['declared_version']
derived = load(P / 'derivations.json')
assert derived['source_id'] == source['id'] and derived['blocks'] == 131
rows = extract(source_bytes.decode(), derived['name'], derived['start_anchor'], derived['stop_heading_level'])
assert len(rows) == 131 and rows == load(P / derived['blocks_path'])
assert (P / derived['line_view']).read_text() == ''.join(f"{r['locator']} HTML:{r['html_line']} {r['text']}\n" for r in rows)
blocks = {r['locator']: r for r in rows}
assert len(blocks) == 131
requirements, cases = load(P / 'requirements.json'), load(P / 'cases.json')
by_id = {r['id']: r for r in requirements}
assert len(by_id) == len(requirements) == 50
assert len({c['id'] for c in cases}) == len(cases) == 88
assert Counter(r['provenance'] for r in requirements) == {'D12': 44, 'U': 6}
assert {r for c in cases for r in c['requirements']} == by_id.keys()
for requirement in requirements:
    assert requirement['target_applicability'] == 'U'
    assert set(requirement['source_blocks']) <= blocks.keys()
    if requirement['provenance'] == 'D12':
        assert requirement['source_blocks']
for case in cases:
    assert len(case['requirements']) == 1
    requirement = by_id[case['requirements'][0]]
    assert case['source_blocks'] == requirement['source_blocks']
    assert case['expected'] is None and case['comparison'] is None
    assert case['target_grade'] == 'U' and case['executed'] is False
    assert case['source_claim'] == requirement['contract']
    assert case['preconditions'] == ['F0', 'positive-path-gate']
    assert case['setup_and_action'] and case['title']
    visible = case['kind'] in ('control', 'state', 'boundary') and requirement['provenance'] == 'D12'
    if visible:
        assert case['documentary_expected'] == requirement['contract']
        assert case['documentary_comparator'].startswith('Only named visible control')
    else:
        assert case['documentary_expected'] is None and case['documentary_comparator'] is None
counts = dict(requirements=len(requirements), requirement_grades=dict(Counter(r['provenance'] for r in requirements)),
              cases=len(cases), case_kinds=dict(Counter(c['kind'] for c in cases)),
              documentary_oracles=sum(c['documentary_expected'] is not None for c in cases),
              null_documentary_oracles=sum(c['documentary_expected'] is None for c in cases),
              target_oracles=0, retained_blocks=131)
assert counts == load(P / 'counts.json')
assert counts['documentary_oracles'] == 41 and counts['null_documentary_oracles'] == 47
fixtures = load(P / 'fixtures.json')
for name in ['F0', 'F-TEMPO', 'F-LEAD', 'F-AUTO', 'F-MARKER', 'F-LOOP', 'F-MULTI', 'F-QUANT', 'F-MODES', 'positive-path-gate', 'not_provided']:
    assert name in fixtures
assert 'nonempty eligible source' in fixtures['positive-path-gate']
assert 'positive source/return/output baseline' in fixtures['positive-path-gate']

canonicals = [ROOT / 'wiki/specs/warping-workflows.md', ROOT / 'wiki/research/warping-workflows.md']
spec = canonicals[0].read_text()
headings = re.findall(r'^### (REQ-WFW-[A-Z0-9-]+) — (.+)$', spec, re.M)
assert len(headings) == 50 and {r[0] for r in headings} == by_id.keys()
for requirement in requirements:
    assert f"### {requirement['id']} — {requirement['title']}\n\n**{requirement['provenance']}/target-U.** {requirement['contract']}" in spec
    for owner in requirement['dependencies']:
        assert f']({owner})' in spec
for case in cases:
    assert f"| {case['id']} | {case['requirements'][0]} | {case['kind']} | {case['title']} |" in spec
browser = spec_rows(canonicals[0], spec)
assert len(browser) == 50 and {r['id'] for r in browser} == by_id.keys()
links = 0
for canonical in canonicals:
    text = canonical.read_text()
    frontmatter = re.match(r'---\n(.*?)\n---\n', text, re.S)
    assert frontmatter
    metadata = dict(line.split(': ', 1) for line in frontmatter.group(1).splitlines() if ': ' in line)
    assert {'id', 'type', 'status', 'updated', 'access', 'revision', 'target'} <= metadata.keys()
    assert metadata['access'] == 'analysis' and metadata['revision'] == '1'
    for target in re.findall(r'\[[^\]]*\]\(([^)\s]+)\)', text):
        if re.match(r'[A-Za-z]+:', target):
            continue
        path, _, fragment = target.partition('#')
        dest = (canonical.parent / path).resolve() if path else canonical
        assert dest.exists(), (canonical, target)
        if fragment and dest.suffix == '.md':
            anchors = {slug(h) for h in re.findall(r'^#+\s+(.+)$', dest.read_text(), re.M)}
            assert fragment in anchors, (canonical, target)
        links += 1
manifest = load(P / 'manifest-author-r1.json')
assert manifest['requirements'] == 50 and manifest['cases'] == 88
for key in ('requirement_grades', 'case_kinds', 'documentary_oracles', 'null_documentary_oracles', 'target_oracles', 'retained_blocks'):
    assert manifest[key] == counts[key]
assert manifest['all_target_expected_comparison_null_U_unexecuted'] is True
assert len(manifest['files']) == 14
assert {str(f.relative_to(P)) for f in P.rglob('*') if f.is_file()} == set(manifest['files']) | {'manifest-author-r1.json'}
for name, record in manifest['files'].items():
    pin(P / name, record)
for snapshot, canonical in manifest['canonical_snapshots'].items():
    assert (P / snapshot).read_bytes() == (ROOT / canonical).read_bytes()
for file in [P / name for name in manifest['files'] if Path(name).suffix in ('.md', '.json', '.txt', '.py')] + [P / 'manifest-author-r1.json'] + canonicals:
    if file.suffix == '.json':
        load(file)
    result = subprocess.run(['git', 'diff', '--no-index', '--check', '/dev/null', str(file)], capture_output=True, text=True)
    assert result.returncode in (0, 1) and not result.stdout and not result.stderr, (file, result.stdout, result.stderr)
print(json.dumps(dict(status='pass', scope='analyst source/documentation integrity only', **counts,
                      source_records=1, frozen_payloads=14, canonical_snapshot_pairs=2,
                      local_links_and_anchors=links, browser_rows_and_ID_equality=50,
                      all_target_expected_comparison_null_U_unexecuted=True,
                      signal_timing_analysis_documentary_oracles_null=True,
                      writes=False, runtime_execution=False), indent=2))
