"""Read-only analyst packet integrity; run with python -B; stdout only."""
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
    assert len(data) == record['bytes'], path
    assert hashlib.sha256(data).hexdigest() == record['sha256'], path
    return data


def slug(heading):
    heading = re.sub(r'<[^>]*>|[`*]', '', heading)
    return re.sub(r'[^\w\- ]', '', heading.strip().lower()).replace(' ', '-')


initial = load(P / 'initial-capture-pins.json')
assert len(initial) == 22
for name, record in initial.items():
    pin(P / name, record)
authorities = load(P / 'authority-pins.json')
assert len(authorities) == 13
for record in authorities:
    pin(ROOT / record['path'], record)
sources, derivations = load(P / 'sources.json'), load(P / 'derivations.json')
assert len(sources) == len(derivations) == 9
assert [s['article_id'] for s in sources] == sorted(s['article_id'] for s in sources)
assert len({s['id'] for s in sources}) == 9
extract = runpy.run_path(str(P / 'source_parser.py'))['extract']
blocks = {}
for source, derived in zip(sources, derivations):
    assert derived['source_id'] == source['id']
    raw = pin(P / source['file'], source)
    article = json.loads(raw)['article']
    assert source['status'] == 200 and source['error'] is None
    assert source['url'] == source['final_url'] == f"https://help.ableton.com/api/v2/help_center/en-us/articles/{source['article_id']}.json"
    assert source['capture_utc'] and '12.4.3 applicability unknown' in source['version']
    assert article['id'] == source['article_id'] and article['title'] == source['article_title']
    assert article['created_at'] == source['article_created_utc']
    assert article['updated_at'] == source['article_updated_utc']
    assert article['html_url'] == source['public_article_url']
    assert article['locale'] == source['article_locale'] == 'en-us' and article['draft'] is False
    assert source['article_body_pointer'] == '/article/body'
    capture = load(P / source['capture_record'])
    for field in ('id', 'url', 'final_url', 'capture_utc', 'status', 'file', 'bytes', 'sha256', 'error'):
        assert source[field] == capture[field], (source['id'], field)
    body = article['body']
    assert (P / derived['body_file']).read_bytes() == body.encode()
    assert len(body.encode()) == source['article_body_bytes']
    assert hashlib.sha256(body.encode()).hexdigest() == source['article_body_sha256']
    rows = extract(body, derived['prefix'], source['id'])
    assert len(rows) == derived['blocks'] and rows == load(P / derived['blocks_file'])
    assert (P / derived['text_file']).read_text() == ''.join(f"{r['id']} /article/body:HTML{r['body_html_line']} {r['text']}\n" for r in rows)
    assert not blocks.keys() & {r['id'] for r in rows}
    blocks.update({r['id']: r for r in rows})
assert len(blocks) == 300
scopes = load(P / 'source-scope.json')
assert [s['source_id'] for s in scopes] == [s['id'] for s in sources]
for scope in scopes:
    assert scope['target_12_4_3'] == 'U' and scope['platforms'] and scope['versions']
    assert set(scope['source_blocks']) <= blocks.keys()
    assert all(blocks[bid]['source_id'] == scope['source_id'] for bid in scope['source_blocks'])
failures = load(P / 'failed-retrievals.json')
assert failures == [load(P / 'install-capture.json')] and failures[0]['status'] == 403
pin(P / failures[0]['file'], failures[0])
assert all(s['file'] != failures[0]['file'] for s in sources)

requirements, cases = load(P / 'requirements.json'), load(P / 'cases.json')
reqmap = {r['id']: r for r in requirements}
assert len(reqmap) == len(requirements) == 45
assert Counter(r['provenance'] for r in requirements) == {'Dhelp': 30, 'U': 15}
assert len({c['id'] for c in cases}) == len(cases) == 60
assert {rid for c in cases for rid in c['requirements']} == reqmap.keys()
for requirement in requirements:
    assert requirement['target_applicability'] == 'U' and requirement['contract'] and requirement['source_blocks']
    assert set(requirement['source_blocks']) <= blocks.keys()
    assert (requirement['provenance'] == 'U') == ('-U-' in requirement['id'])
for case in cases:
    assert len(case['requirements']) == 1 and case['setup_and_action'] and case['title']
    requirement = reqmap[case['requirements'][0]]
    assert case['preconditions'] == ['F0', 'positive-path-gate']
    assert case['source_blocks'] == requirement['source_blocks']
    assert case['expected'] is None and case['comparison'] is None
    assert case['target_grade'] == 'U' and case['executed'] is False
    assert case['source_claim'] == (requirement['source_claim'] or (requirement['contract'] if requirement['provenance'] == 'Dhelp' else None))
    visible = case['kind'] in ('control', 'state') and requirement['provenance'] == 'Dhelp'
    if visible:
        assert case['documentary_expected'] == requirement['contract']
        assert case['documentary_comparator'].startswith('Compare only named visible')
    else:
        assert case['documentary_expected'] is None and case['documentary_comparator'] is None
counts = dict(requirements=45, requirement_grades=dict(Counter(r['provenance'] for r in requirements)),
              cases=60, case_kinds=dict(Counter(c['kind'] for c in cases)),
              documentary_oracles=sum(c['documentary_expected'] is not None for c in cases),
              null_documentary_oracles=sum(c['documentary_expected'] is None for c in cases),
              retained_blocks=300, source_records=9, failed_retrievals=1, target_oracles=0)
assert counts == load(P / 'counts.json') and counts['documentary_oracles'] == 13 and counts['null_documentary_oracles'] == 47
fixtures = load(P / 'fixtures.json')
assert len(fixtures['not_provided']) == 7
assert all(text in fixtures['positive-path-gate'] for text in ('valid owned', 'nonempty eligible source', 'enabled active path/control', 'nonzero', 'nonmuted return/output', 'calibrated positive', 'Monitor/arm/clip/record/transport', 'no real disk exhaustion or account mutation'))
assert 'no original/native/app/hardware/account/install/update/reset/recovery/destructive action' in fixtures['F0']

specpath = ROOT / 'wiki/specs/delivery-recovery-workflows.md'
researchpath = ROOT / 'wiki/research/delivery-recovery-workflows.md'
spec = specpath.read_text()
headings = re.findall(r'^### (REQ-DRW-[A-Z0-9-]+) — (.+)$', spec, re.M)
assert len(headings) == 45 and {r[0] for r in headings} == reqmap.keys()
for requirement in requirements:
    assert f"### {requirement['id']} — {requirement['title']}\n\n**{requirement['provenance']}/target-U.** {requirement['contract']}" in spec
    for bid in requirement['source_blocks']:
        assert f"{bid} /article/body:HTML{blocks[bid]['body_html_line']}" in spec
for case in cases:
    assert f"| {case['id']} | {case['requirements'][0]} | {case['kind']} | {case['title']} |" in spec
browser = spec_rows(specpath, spec)
assert len(browser) == 45 and {r['id'] for r in browser} == reqmap.keys()
for i in range(1, 6):
    question = f'Q-DRW-{i:03d}'
    assert question in spec and question in researchpath.read_text()
links = 0
for path in (specpath, researchpath):
    text = path.read_text()
    match = re.match(r'---\n(.*?)\n---\n', text, re.S)
    assert match
    meta = dict(line.split(': ', 1) for line in match.group(1).splitlines() if ': ' in line)
    assert {'id', 'type', 'status', 'updated', 'access', 'revision', 'target'} <= meta.keys()
    assert meta['access'] == 'analysis' and meta['status'] == 'draft' and meta['revision'] == '1'
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
assert {str(f.relative_to(P)) for f in P.rglob('*') if f.is_file()} == set(manifest['files']) | {'manifest-author-r1.json'}
assert len(manifest['files']) == 61
for name, record in manifest['files'].items():
    pin(P / name, record)
assert len(manifest['canonical_snapshots']) == 2
for snapshot, canonical in manifest['canonical_snapshots'].items():
    assert (P / snapshot).read_bytes() == (ROOT / canonical).read_bytes()
for path in [specpath, researchpath, P / 'manifest-author-r1.json'] + [P / name for name in manifest['files'] if Path(name).suffix in ('.json', '.txt', '.md', '.py')]:
    if path.suffix == '.json':
        load(path)
    result = subprocess.run(['git', 'diff', '--no-index', '--check', '/dev/null', str(path)], capture_output=True, text=True)
    assert result.returncode in (0, 1) and not result.stdout and not result.stderr, (path, result.stdout, result.stderr)
print(json.dumps(dict(status='pass', scope='Partial analyst source/document integrity only', **counts,
                      initial_capture_pins=22, authority_reuse_tool_pins=13, frozen_payloads=61,
                      canonical_snapshot_pairs=2, browser_ID_equality=45, local_links_and_anchors=links,
                      all_target_expected_comparison_null_U_unexecuted=True,
                      nonvisible_documentary_oracles_null=True, writes=False,
                      original_runtime_account_installer_recovery_execution=False), indent=2))
