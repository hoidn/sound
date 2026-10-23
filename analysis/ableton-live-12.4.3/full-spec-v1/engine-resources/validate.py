"""Read-only retained-source and analyst packet integrity; stdout only, run with -B."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import re
import runpy
import subprocess
import sys

P = Path(__file__).resolve().parent
ROOT = P.parents[3]
sys.path.insert(0, str(ROOT / 'tools'))
from spec_browser import spec_rows


def load(path):
    return json.loads(path.read_text())


def pin(path, record):
    data = path.read_bytes()
    assert len(data) == record['bytes'] and hashlib.sha256(data).hexdigest() == record['sha256'], path
    return data


def slug(heading):
    heading = re.sub(r'<[^>]*>|[`*]', '', heading)
    return re.sub(r'[^\w\- ]', '', heading.strip().lower()).replace(' ', '-')


initial = load(P / 'initial-input-pins.json')
assert len(initial) == 12
for name, record in initial.items():
    pin(P / name, record)
authorities = load(P / 'existing-authority-pins.json')
assert len(authorities) == 18
for record in authorities:
    pin(ROOT / record['path'], record)
parser_pin = authorities[0]
assert parser_pin['path'] == 'analysis/ableton-live-12.4.3/full-spec-v1/session-workflows/capture.py'
chapter_class = runpy.run_path(str(ROOT / parser_pin['path']))['Chapter']
sources = load(P / 'sources-all.json')
assert len(sources) == 3 and sources == load(P / 'sources.json') + [load(P / 'resources-source.json')]
assert [s['id'] for s in sources] == ['D12-AUDIO-FACT-SHEET', 'D12-MIDI-FACT-SHEET', 'D12-RESOURCES']
blocks = {}
inputs = [('FACT1', 'D12-AUDIO-FACT-SHEET-blocks', 88, 'audio-fact-sheet'),
          ('FACT2', 'D12-MIDI-FACT-SHEET-blocks', 51, 'midi-fact-sheet'),
          ('RES', 'resources-blocks', 56, 'computer-audio-resources-and-strategies')]
for source, (prefix, stem, count, anchor) in zip(sources, inputs):
    raw = pin(P / source['file'], source)
    assert source['url'] == source['final_url'] and source['capture_utc']
    assert '12.4.3 applicability unknown' in source['version']
    assert '<html' in raw.decode() and 'Ableton Reference Manual' in raw.decode()
    parser = chapter_class()
    parser.feed(raw.decode())
    for i, row in enumerate(parser.rows, 1):
        row['id'] = f'{prefix}-B{i:03d}'
    assert len(parser.rows) == count and parser.rows[0]['anchor'] == anchor
    assert parser.rows == load(P / (stem + '.json'))
    assert (P / (stem + '.txt')).read_text() == ''.join(f"{r['id']} #{r['anchor']} HTML{r['html_line']} {r['text']}\n" for r in parser.rows)
    blocks.update({r['id']: r for r in parser.rows})
assert len(blocks) == 195
resource = sources[2]
assert pin(ROOT / resource['reused_from'], resource) == (P / resource['file']).read_bytes()
original = load(ROOT / 'analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/resources-12-capture.json')
for field in ('id', 'url', 'final_url', 'bytes', 'sha256'):
    assert resource[field] == original[field]
assert resource['capture_utc'] == original['captured_utc'] and resource['version'] == original['declared_version']

requirements, cases = load(P / 'requirements.json'), load(P / 'cases.json')
reqmap = {r['id']: r for r in requirements}
assert len(reqmap) == len(requirements) == 28
assert Counter(r['provenance'] for r in requirements) == {'D12': 13, 'U': 15}
assert len({c['id'] for c in cases}) == len(cases) == 50
assert {rid for c in cases for rid in c['requirements']} == set(reqmap)
for requirement in requirements:
    assert requirement['target_applicability'] == 'U' and requirement['contract']
    assert set(requirement['source_blocks']) <= blocks.keys()
for case in cases:
    assert len(case['requirements']) == 1 and case['setup_and_action']
    requirement = reqmap[case['requirements'][0]]
    assert case['source_blocks'] == requirement['source_blocks']
    assert case['preconditions'] == ['F0', 'positive-path-gate']
    assert case['expected'] is None and case['comparison'] is None and case['target_grade'] == 'U' and case['executed'] is False
    claim = requirement['source_claim'] or (requirement['contract'] if requirement['provenance'] == 'D12' else None)
    assert case['source_claim'] == claim
    visible = case['kind'] in ('control', 'state') and requirement['provenance'] == 'D12'
    if visible:
        assert case['documentary_expected'] == requirement['contract']
        assert case['documentary_comparator'].startswith('Compare only named visible')
    else:
        assert case['documentary_expected'] is None and case['documentary_comparator'] is None
counts = dict(requirements=len(requirements), requirement_grades=dict(Counter(r['provenance'] for r in requirements)),
              cases=len(cases), case_kinds=dict(Counter(c['kind'] for c in cases)),
              documentary_oracles=sum(c['documentary_expected'] is not None for c in cases),
              null_documentary_oracles=sum(c['documentary_expected'] is None for c in cases), retained_blocks=195, target_oracles=0)
assert counts == load(P / 'counts.json') and counts['documentary_oracles'] == 10 and counts['null_documentary_oracles'] == 40
fixtures = load(P / 'fixtures.json')
assert {'F0', 'F-UI', 'F-IO', 'F-LOAD', 'F-AUDIO', 'F-ROUTE', 'F-RECORD', 'F-FREEZE', 'F-MIDI', 'positive-path-gate', 'not_provided'} == fixtures.keys()
assert all(x in fixtures['positive-path-gate'] for x in ('nonempty eligible source', 'nonzero', 'nonmuted', 'Monitor/arm/clip/record', 'calibrated positive', 'running transport'))

specpath = ROOT / 'wiki/specs/engine-resource-workflows.md'
researchpath = ROOT / 'wiki/research/engine-resource-workflows.md'
spec = specpath.read_text()
headings = re.findall(r'^### (REQ-ER-[A-Z0-9-]+) — (.+)$', spec, re.M)
assert len(headings) == 28 and {r[0] for r in headings} == set(reqmap)
for requirement in requirements:
    assert f"### {requirement['id']} — {requirement['title']}\n\n**{requirement['provenance']}/target-U.** {requirement['contract']}" in spec
    for owner in requirement['owners']:
        assert f']({owner})' in spec
for case in cases:
    assert f"| {case['id']} | {case['requirements'][0]} | {case['kind']} | {case['title']} |" in spec
browser = spec_rows(specpath, spec)
assert len(browser) == 28 and {r['id'] for r in browser} == set(reqmap)
for question in ['Q-ER-001', 'Q-ER-002', 'Q-ER-003', 'Q-ER-004', 'Q-ER-005']:
    assert question in spec and question in researchpath.read_text()
links = 0
for path in (specpath, researchpath):
    text = path.read_text()
    match = re.match(r'---\n(.*?)\n---\n', text, re.S)
    assert match
    metadata = dict(line.split(': ', 1) for line in match.group(1).splitlines() if ': ' in line)
    assert {'id', 'type', 'status', 'updated', 'access', 'revision', 'target'} <= metadata.keys()
    assert metadata['access'] == 'analysis' and metadata['revision'] == '1'
    for target in re.findall(r'\[[^\]]*\]\(([^)\s]+)\)', text):
        if re.match(r'[A-Za-z]+:', target):
            continue
        name, _, fragment = target.partition('#')
        dest = (path.parent / name).resolve() if name else path
        assert dest.exists(), (path, target)
        if fragment and dest.suffix == '.md':
            assert fragment in {slug(h) for h in re.findall(r'^#+\s+(.+)$', dest.read_text(), re.M)}, (path, target)
        links += 1
manifest = load(P / 'manifest-author-r1.json')
assert manifest['counts'] == counts
assert len(manifest['files']) == 21
assert {str(f.relative_to(P)) for f in P.rglob('*') if f.is_file()} == set(manifest['files']) | {'manifest-author-r1.json'}
for name, record in manifest['files'].items():
    pin(P / name, record)
for snapshot, canonical in manifest['canonical_snapshots'].items():
    assert (P / snapshot).read_bytes() == (ROOT / canonical).read_bytes()
for path in [specpath, researchpath, P / 'manifest-author-r1.json'] + [P / n for n in manifest['files'] if Path(n).suffix in ('.json', '.txt', '.md', '.py')]:
    if path.suffix == '.json':
        load(path)
    result = subprocess.run(['git', 'diff', '--no-index', '--check', '/dev/null', str(path)], capture_output=True, text=True)
    assert result.returncode in (0, 1) and not result.stdout and not result.stderr, (path, result.stdout, result.stderr)
print(json.dumps(dict(status='pass', scope='Analyst source/documentation integrity only', **counts, source_records=3,
                      initial_input_pins=12, authority_reuse_parser_pins=18, frozen_payloads=21,
                      canonical_snapshot_pairs=2, browser_ID_equality=28, local_links_and_anchors=links,
                      all_target_expected_comparison_null_U_unexecuted=True,
                      signal_timing_numeric_file_cancel_documentary_oracles_null=True,
                      writes=False, runtime_execution=False), indent=2))
