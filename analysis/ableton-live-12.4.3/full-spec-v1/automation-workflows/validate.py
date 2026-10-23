"""Read-only analyst integrity checks. Run with python3 -B; stdout only."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import re
import subprocess
import sys
from urllib.parse import unquote
from source_parser import extract

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


sources = load(P / 'sources.json')
assert len(sources) == 2 and len({s['id'] for s in sources}) == 2
blocks = {}
for source, count in zip(sources, [114, 78]):
    name = source['id'].removeprefix('D12-').lower()
    assert source['url'] == source['final_url'] == f'https://www.ableton.com/en/live-manual/12/{name}/'
    assert source['captured_utc'] and 'Version 12' in source['declared_version'] and '12.4.3 applicability U' in source['declared_version']
    text = pin(P / source['path'], source).decode()
    assert '<html' in text and 'Ableton Reference Manual Version 12' in text
    rows = extract(text, name)
    assert len(rows) == count
    assert rows == load(P / f'manual-{name}-blocks.json')
    assert (P / f'manual-{name}.txt').read_text() == ''.join(f"{r['locator']} HTML:{r['html_line']} {r['text']}\n" for r in rows)
    assert all(r['html_line'] > 0 and r['heading_context'] for r in rows)
    blocks.update({r['locator']: r for r in rows})
assert len(blocks) == 192

authorities = load(P / 'existing-authority-pins.json')
assert len(authorities) == 13
for record in authorities:
    pin(Path(record['path']), record)
release = ROOT / 'handoff/automation-envelopes-v2'
release_manifest = load(release / 'manifest.json')
for record in release_manifest['files']:
    pin(release / record['path'], record)
assert len(load(release / 'cases.json')['cases']) == 21

requirements, cases, counts = [load(P / f'{n}.json') for n in ['requirements', 'cases', 'counts']]
reqmap = {r['id']: r for r in requirements}
assert len(reqmap) == len(requirements) == 62
assert Counter(r['provenance'] for r in requirements) == {'D12': 54, 'U': 8}
assert len({c['id'] for c in cases}) == len(cases) == 76
assert {rid for c in cases for rid in c['requirements']} == set(reqmap)
for r in requirements:
    assert r['target_applicability'] == 'U' and r['contract']
    assert set(r['source_blocks']) <= blocks.keys()
    if r['provenance'] == 'D12':
        assert r['source_blocks']
for c in cases:
    assert len(c['requirements']) == 1 and c['setup_and_action']
    r = reqmap[c['requirements'][0]]
    assert c['source_blocks'] == r['source_blocks']
    assert c['preconditions'] == ['F0', 'positive-path-gate']
    assert c['expected'] is None and c['comparison'] is None and c['target_grade'] == 'U' and c['executed'] is False
    visible = c['kind'] in ('state', 'control', 'boundary') and r['provenance'] == 'D12'
    if visible:
        assert c['documentary_expected'] == c['source_claim'] == r['contract']
        assert c['documentary_comparator'].startswith('Compare only named visible')
    else:
        assert c['documentary_expected'] is None and c['documentary_comparator'] is None
        assert c['source_claim'] == (r['contract'] if r['provenance'] == 'D12' else None)
assert {'signal', 'timing', 'recording', 'transport', 'boundary', 'source-loss', 'midi-output', 'mapping', 'negative', 'undo', 'cancel', 'persistence', 'sample-rate', 'malformed', 'teardown', 'concurrency'} <= {c['kind'] for c in cases}
calculated = dict(requirements=len(requirements), requirement_grades=dict(Counter(r['provenance'] for r in requirements)), cases=len(cases), case_kinds=dict(Counter(c['kind'] for c in cases)), documentary_oracles=sum(c['documentary_expected'] is not None for c in cases), null_documentary_oracles=sum(c['documentary_expected'] is None for c in cases), retained_blocks=192, target_oracles=0)
assert counts == calculated and counts['documentary_oracles'] == 44 and counts['null_documentary_oracles'] == 32
fixtures = load(P / 'fixtures.json')
assert {'F0', 'F-EDITOR', 'F-REC', 'F-OVERRIDE', 'F-VIEWS', 'F-AUDIO', 'F-LOOP', 'F-MAPPING', 'F-MIDI', 'positive-path-gate', 'not_provided'} == fixtures.keys()
assert all(name in fixtures['positive-path-gate'] for name in ['nonempty eligible source', 'nonzero', 'positive', 'Automation Arm', 'running transport', 'matched positive'])

specpath = ROOT / 'wiki/specs/automation-workflows.md'
researchpath = ROOT / 'wiki/research/automation-workflows.md'
spec = specpath.read_text()
headings = re.findall(r'^### (REQ-AUTO-WF-[A-Z0-9-]+) — (.+)$', spec, re.M)
assert len(headings) == 62 and {r[0] for r in headings} == set(reqmap)
for r in requirements:
    assert f"### {r['id']} — {r['title']}\n\n**{r['provenance']}/target-U.** {r['contract']}" in spec
for c in cases:
    assert f"| {c['id']} | {c['requirements'][0]} | {c['kind']} | {c['title']} |" in spec
browser = spec_rows(specpath, spec)
assert len(browser) == 62 and {r['id'] for r in browser} == set(reqmap)
assert 'remains unknown' in spec and 'REQ-AUTOMATION-ENVELOPES-013' in spec
assert '21-case partial storage release' in spec and 'Re-Enable Automation is distinct from Back to Arrangement' in spec
for local in ['Q-AW-001', 'Q-AW-002', 'Q-AW-003']:
    assert local in researchpath.read_text()


def slug(heading):
    heading = re.sub(r'<[^>]*>|[`*]', '', heading)
    return re.sub(r'[^\w\- ]', '', heading.strip().lower()).replace(' ', '-')


links = 0
for path in [specpath, researchpath]:
    text = path.read_text()
    frontmatter = re.match(r'---\n(.*?)\n---\n', text, re.S)
    assert frontmatter
    metadata = dict(line.split(': ', 1) for line in frontmatter.group(1).splitlines() if ': ' in line)
    assert {'id', 'type', 'status', 'updated', 'access', 'revision', 'target'} <= metadata.keys()
    assert metadata['access'] == 'analysis' and metadata['revision'] == '1'
    for target in re.findall(r'\[[^\]]*\]\(([^)\s]+)\)', text):
        if re.match(r'[A-Za-z]+:', target):
            continue
        name, _, fragment = unquote(target).partition('#')
        dest = (path.parent / name).resolve() if name else path
        if dest == P / 'manifest-author-r1.json' and not dest.exists():
            continue  # Pre-seal author audit; final pass also checks manifest inventory.
        assert dest.exists(), (path, target)
        if fragment and dest.suffix == '.md':
            assert fragment in {slug(h) for h in re.findall(r'^#+\s+(.+)$', dest.read_text(), re.M)}, (path, target)
        links += 1
assert (P / 'spec-r1.md').read_bytes() == specpath.read_bytes()
assert (P / 'research-r1.md').read_bytes() == researchpath.read_bytes()
for path in [specpath, researchpath] + [p for p in P.rglob('*') if p.is_file() and p.suffix in ('.py', '.json', '.md', '.txt')]:
    if path.suffix == '.json':
        load(path)
    result = subprocess.run(['git', 'diff', '--no-index', '--check', '/dev/null', str(path)], capture_output=True, text=True)
    assert result.returncode in (0, 1) and not result.stdout and not result.stderr, (path, result.stdout, result.stderr)

manifest_path = P / 'manifest-author-r1.json'
if manifest_path.exists():
    manifest = load(manifest_path)
    assert manifest['counts'] == counts
    actual = {str(path.relative_to(P)) for path in P.rglob('*') if path.is_file()}
    assert actual == set(manifest['files']) | {'manifest-author-r1.json'}
    for name, record in manifest['files'].items():
        pin(P / name, record)
    assert manifest['canonical_snapshots'] == {'spec-r1.md': 'wiki/specs/automation-workflows.md', 'research-r1.md': 'wiki/research/automation-workflows.md'}

print(json.dumps(dict(status='pass', scope='Analyst documentary/source integrity only; no runtime', **counts, source_records=2, existing_authority_pins=13, finite_release_payload_hashes=len(release_manifest['files']), canonical_snapshot_pairs=2, browser_ID_equality=62, local_links_and_anchors=links, sealed_manifest_checked=manifest_path.exists(), all_target_expected_comparison_null_U_unexecuted=True, writes=False, original_execution=False, candidate_execution=False), indent=2))
