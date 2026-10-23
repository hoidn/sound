"""Read-only Browser content evidence checks; no account/network/application work."""
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
load = lambda path: json.loads(path.read_text())
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()


def check():
    before = {str(q.relative_to(P)): sha(q) for q in P.rglob('*') if q.is_file()}
    initial = load(P / 'pre-author-inputs.json')
    assert len(initial) == 8
    for name, pin in initial.items():
        path = P / name
        assert path.stat().st_size == pin['bytes'] and sha(path) == pin['sha256'], name
    owners = load(P / 'owner-pins.json')
    assert len(owners) == 28
    for pin in owners:
        path = ROOT / pin['path']
        assert path.stat().st_size == pin['bytes'] and sha(path) == pin['sha256'], pin['path']
    parser_path = ROOT / 'analysis/ableton-live-12.4.3/full-spec-v1/session-workflows/capture.py'
    assert any(p['path'] == str(parser_path.relative_to(ROOT)) for p in owners)
    Chapter = runpy.run_path(str(parser_path))['Chapter']
    sources = load(P / 'sources.json')
    assert len(sources) == 2 and sources[0] == load(P / 'source.json')
    blocks = {}
    for source, stem, prefix, expected in zip(sources, ['source-blocks', 'similarity-blocks'], ['BC', 'SIM'], [268, 6]):
        raw = (P / source['file']).read_bytes()
        assert len(raw) == source['bytes'] and sha(P / source['file']) == source['sha256']
        assert raw == (ROOT / source['reused_from']).read_bytes()
        meta = load(ROOT / source['capture_metadata'])
        assert source['url'] == meta['url'] and source['final_url'] == meta['final_url']
        assert source['capture_utc'] == meta['captured_utc']
        if prefix == 'BC':
            assert source['sha256'] == meta['sha256'] == '4e34895d5d37d6579e29cb65156b83c53672e89bd01b3bd8233596fc5b17e8b3'
            assert source['bytes'] == meta['bytes'] == 334122
        else:
            assert source['sha256'] == meta['files']['manual-concepts.html'] == 'da51ae19eab185813aac3b4240b7fad6022885421a3794155ca1207fd6e2eed5'
            assert source['bytes'] == 306807 and source['selected_anchor'] == 'sound-similarity'
        parser = Chapter()
        parser.feed(raw.decode())
        rows = parser.rows
        if prefix == 'SIM':
            rows = [r for r in rows if r['anchor'] == 'sound-similarity']
        for i, row in enumerate(rows, 1):
            row['id'] = f'{prefix}-B{i:03d}'
        assert len(rows) == expected and rows == load(P / (stem + '.json'))
        assert (P / (stem + '.txt')).read_text() == ''.join(
            f"{r['id']} #{r['anchor']} HTML{r['html_line']} {r['text']}\n" for r in rows)
        blocks.update({r['id']: r for r in rows})
    assert len(blocks) == 274
    rs, cs = load(P / 'requirements.json'), load(P / 'cases.json')
    assert len(rs) == len({r['id'] for r in rs}) == 56
    assert len(cs) == len({c['id'] for c in cs}) == 71
    assert Counter(r['provenance'] for r in rs) == {'D12': 50, 'U': 6}
    assert Counter(c['provenance'] for c in cs) == {'D12': 50, 'U': 21}
    reqs = {r['id']: r for r in rs}
    assert set(reqs) == {r for c in cs for r in c['requirements']}
    for r in rs:
        assert r['target_applicability'] == 'U'
        linked = [c for c in cs if r['id'] in c['requirements']]
        if r['provenance'] == 'D12':
            assert r['evidence'] and len(linked) == 1 and linked[0]['source_claim'] == r['contract']
        else:
            assert not r['evidence'] and all(c['unknown'] for c in linked)
        for e in r['evidence']:
            b = blocks[e['block']]
            assert e['anchor'] == b['anchor'] and e['html_line'] == b['html_line']
            assert e['source'] == ('D12-SOUND-SIMILARITY' if e['block'].startswith('SIM-') else 'D12-BROWSER-CONTENT')
    for c in cs:
        assert c['fixture'] == 'fixtures.json#BC-OWNED' and c['preconditions'] == ['common', 'active-positive-guard']
        assert c['expected'] is None and c['comparison'] is None and c['target_grade'] == 'U' and c['executed'] is False
        r = reqs[c['requirements'][0]]
        assert c['evidence'] == r['evidence']
        if c['kind'] == 'control':
            assert c['provenance'] == 'D12' and c['documentary_expected'] == c['source_claim'] == r['contract']
            assert c['documentary_comparator'].startswith('Named text-supported visible')
        else:
            assert c['documentary_expected'] is None and c['documentary_comparator'] is None
    assert sum(c['documentary_expected'] is not None for c in cs) == 33
    fixture = load(P / 'fixtures.json')
    assert fixture['id'] == 'BC-OWNED' and not fixture['original_execution'] and not fixture['candidate_comparison']
    assert all(word in fixture['active-positive-guard'] for word in ['nonempty', 'nonzero', 'nonmuted', 'positive', 'account', 'hardware', 'focus'])
    assert 'Push3 Standalone' in fixture['setups']['push']
    counts = load(P / 'counts.json')
    assert counts['requirements'] == 56 and counts['cases'] == 71 and counts['documentary_null_cases'] == 38
    assert counts['case_kinds'] == dict(Counter(c['kind'] for c in cs))
    release = ROOT / 'handoff/browser-index-v1'
    files = load(release / 'manifest.json')['files']
    records = files if isinstance(files, list) else [dict(path=n, **v) for n, v in files.items()]
    for pin in records:
        path = release / pin['path']
        assert path.stat().st_size == pin['bytes'] and sha(path) == pin['sha256']
    assert len(records) == load(P / 'release-boundary.json')['payload_hashes_checked'] == 31
    sys.path.insert(0, str(ROOT / 'tools'))
    from spec_browser import spec_rows, anchor, frontmatter
    spec = ROOT / 'wiki/specs/browser-content-workflows.md'
    parsed = spec_rows(spec, spec.read_text())
    assert len(parsed) == 56 and {r['id'] for r in parsed} == set(reqs)
    links = 0
    for name, folder in [('spec-r1.md', 'specs'), ('research-r1.md', 'research')]:
        canonical = ROOT / 'wiki' / folder / 'browser-content-workflows.md'
        assert (P / name).read_bytes() == canonical.read_bytes()
        text = canonical.read_text()
        meta = frontmatter(text)
        assert all(meta.get(k) for k in ['id', 'type', 'status', 'updated', 'access', 'revision', 'target'])
        assert meta['access'] == 'analysis' and meta['revision'] == '1'
        for dest in re.findall(r'(?<!!)\[[^\]]+\]\(([^)]+)\)', text):
            if '://' in dest or dest.startswith('#'):
                continue
            name, _, frag = dest.partition('#')
            path = canonical.parent / name
            assert path.is_file(), dest
            if frag and path.suffix == '.md':
                assert frag in {anchor(h) for h in re.findall(r'^#+ (.+)$', path.read_text(), re.M)}, dest
            if frag and path.suffix == '.json':
                assert load(path).get('id') == frag
            links += 1
    manifest = load(P / 'manifest-author-r1.json')
    expected = set(manifest['files']) | {'manifest-author-r1.json', 'validation-author-r1.json', 'freeze-author-r1.json'}
    assert set(before) <= expected and set(manifest['files']) | {'manifest-author-r1.json'} <= set(before)
    for name, pin in manifest['files'].items():
        path = P / name
        assert path.stat().st_size == pin['bytes'] and sha(path) == pin['sha256'], name
    for row in manifest['canonical_snapshots']:
        assert sha(ROOT / row['canonical']) == row['sha256'] == sha(P / row['snapshot'])
    whitespace = 0
    for path in [spec, ROOT / 'wiki/research/browser-content-workflows.md'] + [x for x in P.iterdir() if x.is_file()]:
        if path.suffix in {'.json', '.py', '.md', '.txt'}:
            if path.suffix == '.json':
                load(path)
            result = subprocess.run(['git', 'diff', '--no-index', '--check', '/dev/null', str(path)], capture_output=True)
            assert result.returncode in (0, 1) and not result.stdout and not result.stderr, path
            whitespace += 1
    assert before == {str(q.relative_to(P)): sha(q) for q in P.rglob('*') if q.is_file()}
    return dict(status='pass', scope='Source/identity/ID/case/null/guard/pin/link integrity only; semantic review pending',
                requirements=56, cases=71, browser_exact_ID_set=56,
                source_records=2, Browser_source_blocks=268, SoundSimilarity_source_blocks=6,
                pre_author_inputs=8, owner_reuse_parser_pins=28, immutable_release_payloads=31,
                documentary_visible_proposals=33, documentary_null_cases=38,
                all_target_null_U_unexecuted=True, canonical_snapshot_pairs=2,
                payloads=len(manifest['files']), local_links=links,
                untracked_whitespace_text_files=whitespace, writes=False,
                original_network_account_hardware_or_candidate_execution=False)


if __name__ == '__main__':
    print(json.dumps(check(), indent=2))
