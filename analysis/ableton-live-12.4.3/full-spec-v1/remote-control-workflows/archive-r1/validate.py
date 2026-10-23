"""Read-only remote-control documentary integrity checks; no network or runtime."""
from collections import Counter
from pathlib import Path
import hashlib
import json
import re
import runpy
import subprocess
import sys

P = Path(__file__).resolve().parent
ROOT = P.parents[3]
load = lambda name: json.loads((P / name).read_text())
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()


def check():
    source = load('source.json')
    assert source['url'] == 'https://www.ableton.com/en/live-manual/12/midi-and-key-remote-control/'
    raw = (P / source['file']).read_bytes()
    assert len(raw) == source['bytes'] == 264686
    assert sha(P / source['file']) == source['sha256'] == '63dfe96294283a8f5d1bb0876dad48c29a9173a82fe81cfa1ce74ac24726b523'
    dependencies = load('dependencies.json')
    assert len(dependencies) == 1
    for pin in dependencies + load('owner-pins.json'):
        path = ROOT / pin['path']
        assert path.stat().st_size == pin['bytes'] and sha(path) == pin['sha256'], pin['path']
    parser = runpy.run_path(str(ROOT / dependencies[0]['path']))['Chapter']()
    parser.feed(raw.decode())
    for i, row in enumerate(parser.rows, 1):
        row['id'] = f'RC-B{i:03d}'
    assert parser.rows == load('source-blocks.json') and len(parser.rows) == 90
    assert (P / 'source-blocks.txt').read_text() == ''.join(
        f"{r['id']} #{r['anchor']} HTML{r['html_line']} {r['text']}\n" for r in parser.rows)
    blocks = {r['id']: r for r in parser.rows}
    requirements, cases = load('requirements.json'), load('cases.json')
    assert len(requirements) == len({r['id'] for r in requirements}) == 37
    assert len(cases) == len({c['id'] for c in cases}) == 47
    assert Counter(r['strength'] for r in requirements) == {'D12': 32, 'U': 5}
    assert Counter(c['provenance'] for c in cases) == {'D12': 32, 'U': 15}
    index = {r['id']: r for r in requirements}
    assert set(index) == {rid for c in cases for rid in c['requirements']}
    for r in requirements:
        assert r['target_applicability'] == 'U'
        linked = [c for c in cases if r['id'] in c['requirements']]
        if r['strength'] == 'D12':
            assert len(linked) == 1 and linked[0]['source_claim'] == r['contract']
            assert r['evidence']
        else:
            assert r['evidence'] == [] and all(c['unknown'] for c in linked)
        for e in r['evidence']:
            assert all(e[k] == blocks[e['id']][k] for k in ('id', 'anchor', 'html_line'))
    for c in cases:
        assert c['fixture'] == 'fixtures.json#RC-OWNED'
        assert c['preconditions'] == ['common', 'active-positive-guard']
        assert c['expected'] is None and c['comparison'] is None and c['target_grade'] == 'U' and c['executed'] is False
        assert c['evidence'] == index[c['requirements'][0]]['evidence']
        if c['kind'] == 'control':
            assert c['documentary_expected'] == c['source_claim'] and c['documentary_comparator']
        else:
            assert c['documentary_expected'] is None and c['documentary_comparator'] is None
    assert sum(c['documentary_expected'] is not None for c in cases) == 19
    fixture = load('fixtures.json')
    assert fixture['id'] == 'RC-OWNED' and not fixture['original_execution'] and not fixture['candidate_comparison']
    assert all(word in fixture['active-positive-guard'] for word in ['positive', 'nonzero', 'focus', 'channel', 'active mapped target'])
    counts = load('counts.json')
    assert counts['requirements'] == 37 and counts['cases'] == 47 and counts['source_blocks'] == 90
    assert counts['case_kinds'] == dict(Counter(c['kind'] for c in cases))
    release = ROOT / 'handoff/midi-config-v4'
    release_files = json.loads((release / 'manifest.json').read_text())['files']
    for pin in release_files:
        path = release / pin['path']
        assert path.stat().st_size == pin['bytes'] and sha(path) == pin['sha256'], pin['path']
    assert len(release_files) == load('release-boundary.json')['payloads_checked'] == 166
    sys.path.insert(0, str(ROOT / 'tools'))
    from spec_browser import spec_rows, anchor, frontmatter
    specpath = ROOT / 'wiki/specs/remote-control-workflows.md'
    spec = specpath.read_text()
    browser = spec_rows(specpath, spec)
    assert len(browser) == 37 and {r['id'] for r in browser} == set(index)
    links = 0
    for snapshot, canonical in [('spec-r1.md', specpath), ('research-r1.md', ROOT / 'wiki/research/remote-control-workflows.md')]:
        assert (P / snapshot).read_bytes() == canonical.read_bytes()
        text = canonical.read_text()
        meta = frontmatter(text)
        assert all(meta.get(key) for key in ('id', 'type', 'status', 'updated', 'access'))
        assert meta['access'] == 'analysis' and meta['updated'] == '2026-10-19'
        for dest in re.findall(r'(?<!!)\[[^\]]+\]\(([^)]+)\)', text):
            if '://' in dest or dest.startswith('#'):
                continue
            path, _, frag = dest.partition('#')
            target = canonical.parent / path
            assert target.is_file(), dest
            if frag and target.suffix == '.json':
                assert json.loads(target.read_text()).get('id') == frag, dest
            if frag and target.suffix == '.md':
                assert frag in {anchor(h) for h in re.findall(r'^#+ (.+)$', target.read_text(), re.M)}, dest
            links += 1
    manifest = load('manifest-author-r1.json')
    for name, pin in manifest['files'].items():
        path = P / name
        assert path.stat().st_size == pin['bytes'] and sha(path) == pin['sha256'], name
    for snapshot in manifest['canonical_snapshots']:
        assert sha(ROOT / snapshot['canonical']) == snapshot['sha256'] == sha(P / snapshot['snapshot'])
    checked = 0
    for path in [*P.iterdir(), specpath, ROOT / 'wiki/research/remote-control-workflows.md']:
        if path.is_file() and path.suffix in {'.json', '.md', '.py', '.txt'}:
            if path.suffix == '.json':
                json.loads(path.read_text())
            result = subprocess.run(['git', 'diff', '--no-index', '--check', '/dev/null', str(path)], capture_output=True)
            assert result.returncode in (0, 1) and not result.stdout and not result.stderr, path
            checked += 1
    return {'result': 'pass', 'scope': 'source/hash/locator/ID/case/null/guard/snapshot/link/untracked-whitespace integrity only; semantic review pending',
            'source_blocks': 90, 'requirements': 37, 'browser_exact_ID_set': 37,
            'cases': 47, 'documentary_control_proposals': 19, 'documentary_null_cases': 28,
            'all_target_null_U_unexecuted': True, 'owner_pins': len(load('owner-pins.json')),
            'release_payloads_checked': 166, 'payloads': len(manifest['files']),
            'local_links': links, 'untracked_whitespace_text_files': checked,
            'original_or_candidate_execution': False}


if __name__ == '__main__':
    print(json.dumps(check(), indent=2))
