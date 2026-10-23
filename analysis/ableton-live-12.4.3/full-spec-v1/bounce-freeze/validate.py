"""Read-only analyst packet checks. Run with python -B; never writes results."""
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
assert len(sources) == 5
source_map = {s['id']: s for s in sources}
assert len(source_map) == 5
for source in sources:
    path = Path(source['path'])
    pin(path if path.is_absolute() else P / path, source)
for capture, source_id in [('bounce-capture.json', 'D12-BOUNCE'),
                           ('resources-12-capture.json', 'D12-RESOURCES'),
                           ('resources-11-capture.json', 'D11-RESOURCES')]:
    assert load(P / capture) == source_map[source_id]
    source = source_map[source_id]
    text = (P / source['path']).read_text()
    assert source['url'] == source['final_url']
    assert 'Version 12' in source['declared_version'] if source_id.startswith('D12') else 'Version 11' in source['declared_version']
    assert '<html' in text and 'Ableton Reference Manual' in text
mix = source_map['D12-MIXING']
original = load(Path(source_map['ROUTING-MONITORING-CAPTURE-CATALOG']['path']))
retained = [r for r in original if r['id'] == mix['id']]
assert len(retained) == 1
for field in ['id', 'url', 'final_url', 'captured_utc', 'bytes', 'sha256', 'path']:
    assert retained[0][field] == mix[field]
mix_lines = Path(mix['path']).read_text().splitlines()
assert '/en/live-manual/12/computer-audio-resources-and-strategies/#track-freeze' in mix_lines[629]

all_blocks = {}
derivations = load(P / 'derivations.json')
assert [(r['name'], r['blocks']) for r in derivations] == [('bounce', 21), ('freeze12', 20), ('freeze11', 18)]
for derived in derivations:
    source = source_map[derived['source_id']]
    rows = extract((P / source['path']).read_text(), derived['name'], derived['start_anchor'], derived['stop_heading_level'])
    assert len(rows) == derived['blocks']
    assert rows == load(P / derived['blocks_path'])
    view = ''.join(f"{r['locator']} HTML:{r['html_line']} {r['text']}\n" for r in rows)
    assert (P / derived['line_view']).read_text() == view
    all_blocks.update({r['locator']: r for r in rows})
assert len(all_blocks) == 59

requirements = load(P / 'requirements.json')
cases = load(P / 'cases.json')
by_id = {r['id']: r for r in requirements}
assert len(by_id) == len(requirements) == 41
assert len({c['id'] for c in cases}) == len(cases) == 77
assert Counter(r['provenance'] for r in requirements) == {'D12': 36, 'U': 5}
assert {r for c in cases for r in c['requirements']} == by_id.keys()
for requirement in requirements:
    assert requirement['target_applicability'] == 'U'
    assert set(requirement['source_blocks']) <= all_blocks.keys()
    assert not any(b.startswith('freeze11:') for b in requirement['source_blocks']) or requirement['id'] == 'REQ-BF-U-FLATTEN'
    if requirement['provenance'] == 'D12':
        assert requirement['source_blocks']
for case in cases:
    assert len(case['requirements']) == 1
    requirement = by_id[case['requirements'][0]]
    assert case['source_blocks'] == requirement['source_blocks']
    assert case['expected'] is None and case['comparison'] is None
    assert case['target_grade'] == 'U' and case['executed'] is False
    assert case['preconditions'] == ['F0', 'positive-path-gate']
    assert case['setup_and_action'] and case['title']
    visible = case['kind'] in ('control', 'state', 'boundary') and requirement['provenance'] == 'D12'
    if visible:
        assert case['documentary_expected'] == requirement['contract']
        assert case['documentary_comparator'].startswith('Compare only named visible')
    else:
        assert case['documentary_expected'] is None and case['documentary_comparator'] is None
counts = dict(requirements=len(requirements), requirement_grades=dict(Counter(r['provenance'] for r in requirements)),
              cases=len(cases), case_kinds=dict(Counter(c['kind'] for c in cases)),
              documentary_oracles=sum(c['documentary_expected'] is not None for c in cases),
              null_documentary_oracles=sum(c['documentary_expected'] is None for c in cases),
              target_oracles=0, retained_blocks=59)
assert counts == load(P / 'counts.json')
assert counts['documentary_oracles'] == 42 and counts['null_documentary_oracles'] == 35
fixtures = load(P / 'fixtures.json')
for fixture in ['F0', 'F-TRACK', 'F-VIEWS', 'F-SIGNAL', 'F-GROUP', 'F-PASTE', 'F-FREEZE', 'F-FILES', 'F-HARDWARE', 'positive-path-gate', 'not_provided']:
    assert fixture in fixtures
assert 'nonempty eligible source' in fixtures['positive-path-gate']
assert 'positive source/return/output baseline' in fixtures['positive-path-gate']

canonicals = [ROOT / 'wiki/specs/bounce-freeze-workflows.md', ROOT / 'wiki/research/bounce-freeze-workflows.md']
spec = canonicals[0].read_text()
headings = re.findall(r'^### (REQ-BF-[A-Z0-9-]+) — (.+)$', spec, re.M)
assert len(headings) == 41 and {r[0] for r in headings} == by_id.keys()
for requirement in requirements:
    assert f"### {requirement['id']} — {requirement['title']}\n\n**{requirement['provenance']}/target-U.** {requirement['contract']}" in spec
    for owner in requirement['dependencies']:
        assert f']({owner})' in spec
for case in cases:
    assert f"| {case['id']} | {case['requirements'][0]} | {case['kind']} | {case['title']} |" in spec
browser = spec_rows(canonicals[0], spec)
assert len(browser) == 41 and {r['id'] for r in browser} == by_id.keys()
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
assert manifest['requirements'] == 41 and manifest['cases'] == 77
assert manifest['requirement_grades'] == counts['requirement_grades']
assert manifest['case_kinds'] == counts['case_kinds']
assert manifest['documentary_oracles'] == 42 and manifest['null_documentary_oracles'] == 35
assert manifest['all_target_expected_comparison_null_U_unexecuted'] is True
assert len(manifest['files']) == 22
actual = {str(f.relative_to(P)) for f in P.rglob('*') if f.is_file()}
assert actual == set(manifest['files']) | {'manifest-author-r1.json'}
for name, record in manifest['files'].items():
    pin(P / name, record)
for snapshot, canonical in manifest['canonical_snapshots'].items():
    assert (P / snapshot).read_bytes() == (ROOT / canonical).read_bytes()
for file in [P / name for name in manifest['files'] if Path(name).suffix in ('.md', '.json', '.txt', '.py')] + [P / 'manifest-author-r1.json'] + canonicals:
    if file.suffix == '.json':
        load(file)
    result = subprocess.run(['git', 'diff', '--no-index', '--check', '/dev/null', str(file)], capture_output=True, text=True)
    assert result.returncode in (0, 1) and not result.stdout and not result.stderr, (file, result.stdout, result.stderr)
print(json.dumps(dict(status='pass', scope='analyst source and documentation integrity only', **counts,
                      source_records=5, new_official_captures=3, original_reused_capture_identities=1,
                      frozen_payloads=22, canonical_snapshot_pairs=2, local_links_and_anchors=links,
                      browser_rows_and_ID_equality=41, all_target_expected_comparison_null_U_unexecuted=True,
                      writes=False, runtime_execution=False), indent=2))
