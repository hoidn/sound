"""Read-only Push documentary packet checks; use python3 -B, stdout only."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import re
import subprocess
import sys
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
assert len(sources) == 2
allblocks = {}
for model, source, count in zip([1, 2], sources, [303, 403]):
    name = f'using-push-{model}'
    assert source['id'] == f'D12-{name.upper()}'
    assert source['url'] == source['final_url'] == f'https://www.ableton.com/en/live-manual/12/{name}/'
    assert source['captured_utc'] and 'Version 12' in source['declared_version'] and '12.4.3 applicability U' in source['declared_version']
    text = pin(P / source['path'], source).decode()
    assert 'Ableton Reference Manual Version 12' in text
    rows = extract(text, name)
    assert len(rows) == count
    for i, row in enumerate(rows, 1):
        row['locator'] = f'P{model}-B{i:03d}'
    assert rows == load(P / f'manual-push-{model}-blocks.json')
    assert (P / f'manual-push-{model}.txt').read_text() == ''.join(f"{r['locator']} HTML:{r['html_line']} {r['text']}\n" for r in rows)
    assert all(r['heading_context'] and r['html_line'] > 0 for r in rows)
    allblocks.update({r['locator']: r for r in rows})
assert len(allblocks) == 706
pins = load(P / 'owner-pins.json')
assert len(pins) == 15
for record in pins:
    pin(Path(record['path']), record)
origin = load(P / 'parser-origin.json')
assert pin(Path(origin['path']), origin) == (P / 'source_parser.py').read_bytes()

rs, cs, counts = [load(P / f'{name}.json') for name in ['requirements', 'cases', 'counts']]
reqmap = {r['id']: r for r in rs}
assert len(reqmap) == len(rs) == 65
assert Counter(r['provenance'] for r in rs) == {'D12': 53, 'U': 12}
assert len({c['id'] for c in cs}) == len(cs) == 77
assert {rid for c in cs for rid in c['requirements']} == set(reqmap)
for r in rs:
    assert r['model'] in (1, 2) and r['target_applicability'] == 'U'
    assert all(ref in allblocks and ref.startswith(f"P{r['model']}-") for ref in r['source_blocks'])
    assert bool(r['source_blocks']) == (r['provenance'] == 'D12')
for c in cs:
    assert len(c['requirements']) == 1 and c['setup_and_action']
    r = reqmap[c['requirements'][0]]
    assert c['model'] == r['model'] and c['source_blocks'] == r['source_blocks']
    assert c['preconditions'] == ['common', f"Push{r['model']}", 'active-positive-guard']
    assert c['expected'] is None and c['comparison'] is None and c['target_grade'] == 'U' and c['executed'] is False
    visible = c['kind'] == 'control' and r['provenance'] == 'D12'
    if visible:
        assert c['documentary_expected'] == c['source_claim'] == r['contract']
        assert c['documentary_comparator'].startswith('Compare only text-supported named controls')
    else:
        assert c['documentary_expected'] is None and c['documentary_comparator'] is None
        assert c['source_claim'] == (r['contract'] if r['provenance'] == 'D12' else None)
calculated = dict(requirements=len(rs), requirement_grades=dict(Counter(r['provenance'] for r in rs)), cases=len(cs), case_kinds=dict(Counter(c['kind'] for c in cs)), documentary_oracles=sum(c['documentary_expected'] is not None for c in cs), null_documentary_oracles=sum(c['documentary_expected'] is None for c in cs), retained_blocks={'Push1':303,'Push2':403}, target_oracles=0, per_model={str(m):dict(requirements=sum(r['model']==m for r in rs),D12=sum(r['model']==m and r['provenance']=='D12' for r in rs),U=6,cases=sum(c['model']==m for c in cs)) for m in [1,2]})
assert counts == calculated and counts['documentary_oracles'] == 18 and counts['null_documentary_oracles'] == 59
for model in [1, 2]:
    assert {'negative', 'boundary', 'malformed', 'undo', 'cancel', 'persistence', 'automation', 'sample-rate', 'source-loss', 'teardown', 'protocol'} <= {c['kind'] for c in cs if c['model'] == model}
fixtures = load(P / 'fixtures.json')
assert all(k in fixtures for k in ['common', 'Push1', 'Push2', 'active-positive-guard', 'not_provided'])
assert all(word in fixtures['active-positive-guard'] for word in ['matching hardware/firmware', 'nonempty source', 'nonzero', 'running transport', 'paired positive pass', 'Missing hardware/target'])

specpath, researchpath = [ROOT / 'wiki' / folder / 'push-controller-workflows.md' for folder in ['specs', 'research']]
spec = specpath.read_text()
headings = re.findall(r'^### (REQ-PUSH[12]-WF-[A-Z0-9-]+) — (.+)$', spec, re.M)
assert len(headings) == 65 and {h[0] for h in headings} == set(reqmap)
for r in rs:
    assert f"### {r['id']} — {r['title']}\n\n**{r['provenance']}/target-U.** {r['contract']}" in spec
for c in cs:
    assert f"| {c['id']} | {c['requirements'][0]} | {c['kind']} | {c['title']} |" in spec
browser = spec_rows(specpath, spec)
assert len(browser) == 65 and {row['id'] for row in browser} == set(reqmap)
assert 'REQ013' in spec and '149' in spec and 'Push 1 text is not Push 2 or Push 3 evidence' in spec
assert all(q in researchpath.read_text() for q in ['Q-PUSH-001', 'Q-PUSH-002', 'Q-PUSH-003'])


def slug(heading):
    return re.sub(r'[^\w\- ]', '', re.sub(r'[`*]|<[^>]*>', '', heading).strip().lower()).replace(' ', '-')


links = 0
for canonical, snapshot in [(specpath, 'spec-r1.md'), (researchpath, 'research-r1.md')]:
    assert canonical.read_bytes() == (P / snapshot).read_bytes()
    text = canonical.read_text()
    front = re.match(r'---\n(.*?)\n---\n', text, re.S)
    assert front
    metadata = dict(line.split(': ', 1) for line in front.group(1).splitlines() if ': ' in line)
    assert {'id', 'type', 'status', 'updated', 'access', 'revision', 'target'} <= metadata.keys()
    assert metadata['access'] == 'analysis' and metadata['revision'] == '1'
    for target in re.findall(r'\[[^\]]*\]\(([^)\s]+)\)', text):
        if re.match(r'[A-Za-z]+:', target):
            continue
        name, _, fragment = target.partition('#')
        path = (canonical.parent / name).resolve() if name else canonical
        if path == P / 'manifest-author-r1.json' and not path.exists():
            continue  # Pre-seal audit; final pass checks full manifest and inventory.
        assert path.exists(), (canonical, target)
        if fragment and path.suffix == '.md':
            assert fragment in {slug(h) for h in re.findall(r'^#+\s+(.+)$', path.read_text(), re.M)}, target
        links += 1
for path in [specpath, researchpath] + [p for p in P.rglob('*') if p.is_file() and p.suffix in ('.py', '.json', '.md', '.txt')]:
    if path.suffix == '.json':
        load(path)
    result = subprocess.run(['git', 'diff', '--no-index', '--check', '/dev/null', str(path)], capture_output=True, text=True)
    assert result.returncode in (0, 1) and not result.stdout and not result.stderr, (path, result.stdout, result.stderr)
manifest_path = P / 'manifest-author-r1.json'
if manifest_path.exists():
    manifest = load(manifest_path)
    assert manifest['counts'] == counts
    assert {str(f.relative_to(P)) for f in P.rglob('*') if f.is_file()} == set(manifest['files']) | {'manifest-author-r1.json'}
    for name, record in manifest['files'].items():
        pin(P / name, record)
    assert manifest['canonical_snapshots'] == {'spec-r1.md': 'wiki/specs/push-controller-workflows.md', 'research-r1.md': 'wiki/research/push-controller-workflows.md'}
print(json.dumps(dict(status='pass', scope='Analyst documentary/source integrity only; no hardware or runtime', **counts, source_records=2, owner_pins=15, parser_origin_pin=1, browser_ID_equality=65, canonical_snapshot_pairs=2, local_links_and_anchors=links, sealed_manifest_checked=manifest_path.exists(), all_target_expected_comparison_null_U_unexecuted=True, writes=False, hardware_execution=False, original_execution=False, candidate_execution=False), indent=2))
