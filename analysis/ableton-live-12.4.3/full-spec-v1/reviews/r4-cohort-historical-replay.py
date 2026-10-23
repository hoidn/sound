"""Read-only R1 replay for the finite four-owner R4 cohort and two source audits.

Only eight known historical wiki reads resolve to exact pinned R1 snapshots.
Current owner validation and semantic approval remain separate.
"""
from pathlib import Path
from contextlib import redirect_stdout
import hashlib
import io
import json
import runpy
import sys

assert sys.argv[1:] == ['--check'] and sys.dont_write_bytecode, 'Use -B and --check'
R = Path(__file__).resolve().parents[4]
B = R / 'analysis/ableton-live-12.4.3/full-spec-v1'
read_bytes, read_text, stat = Path.read_bytes, Path.read_text, Path.stat
sha = lambda p: hashlib.sha256(read_bytes(p)).hexdigest()
load = lambda p: json.loads(read_text(p))
owner_seals = {
    'stem-separation': 'e7d75c3e9d692b3bf15187bb2284510c1c0e9b0362145cbe67bd91ec90d0d9d2',
    'synchronization': 'e94dddb2bd443a5a20ffbacc03bc9b0ab48cde0c97cc085c2175481e13ea26d4',
    'settings-learning': '0c4d506425f34a330e7f668563c63824be3746407ff00d358f5bf4df5fc4509c',
    'video-workflows': 'ba9c19eb8836759b57c33e939aa294a390dd9d0199b00948396b769d0566467e',
}
slugs = {'stem-separation': 'stem-separation', 'synchronization': 'synchronization-workflows',
         'settings-learning': 'settings-learning-workflows', 'video-workflows': 'video-workflows'}
redirects, descriptors, watched = {}, [], set()
for owner, seal in owner_seals.items():
    manifest = B / owner / 'manifest-author-r1.json'
    assert sha(manifest) == seal
    data = load(manifest)
    watched.add(manifest)
    for name, pin in data['files'].items():
        p = manifest.parent / name
        assert len(read_bytes(p)) == pin['bytes'] and sha(p) == pin['sha256']
        watched.add(p)
    for snapshot, domain in [('spec-r1.md', 'specs'), ('research-r1.md', 'research')]:
        current = R / 'wiki' / domain / (slugs[owner] + '.md')
        old = manifest.parent / snapshot
        pin = data['files'][snapshot]
        assert len(read_bytes(old)) == pin['bytes'] and sha(old) == pin['sha256']
        redirects[current] = old
        descriptors.append({'canonical_route': str(current.relative_to(R)),
                            'historical_snapshot': str(old.relative_to(R)), **pin})
        watched.add(current)
assert len(redirects) == 8


def historical_path(path):
    # Fixed absolute paths only. No alias, prefix, arbitrary hash or new owner resolver.
    return redirects.get(path, path)


sample = R / 'wiki/specs/stem-separation.md'
assert historical_path(sample) == B / 'stem-separation/spec-r1.md'
assert historical_path(R / 'wiki/specs/stem-separation-extra.md') == R / 'wiki/specs/stem-separation-extra.md'
assert historical_path(R / 'wiki/specs/unrelated.md') == R / 'wiki/specs/unrelated.md'
checks = [
    ('inventory-revisions/r4-citation-crosswalk/derive.py', '1093f1ee1da0d3576479dc2c87fe18f3e4db488b54510378a6f5cd4c1555a372'),
    ('stem-separation-source-audit/derive.py', 'eb569370a062d740943b415601576dcf9a4ce34596c7b1c75fe89e241839ec6c'),
    ('video-source-audit/derive.py', '1ec6a25fe6c5fd5c1eb58650bc03aa0d46d38f178136493fd8450874d5fc4720'),
]
for name, digest in checks:
    tool = B / name
    assert sha(tool) == digest
    watched.update(p for p in tool.parent.rglob('*') if p.is_file())
    inputs = load(tool.parent / ('inputs.json' if name.startswith('inventory') else 'input-pins.json'))
    for pin in inputs['pins'] if isinstance(inputs, dict) else inputs:
        path = historical_path(R / pin['path'])
        assert len(read_bytes(path)) == pin['bytes'] and sha(path) == pin['sha256'], pin['path']
        watched.add(path)
before = {str(p): sha(p) for p in watched}
outputs, old_argv = [], sys.argv[:]
try:
    Path.read_bytes = lambda p: read_bytes(historical_path(p))
    Path.read_text = lambda p, *a, **kw: read_text(historical_path(p), *a, **kw)
    Path.stat = lambda p, *a, **kw: stat(historical_path(p), *a, **kw)
    for name, digest in checks:
        sys.argv = [str(B / name), '--check']
        captured = io.StringIO()
        with redirect_stdout(captured):
            runpy.run_path(str(B / name), run_name='__main__')
        result = json.loads(captured.getvalue())
        if name.startswith('inventory'):
            assert result == load(B / 'inventory-revisions/r4-citation-crosswalk/summary.json')
        else:
            assert result['status'] == 'passed-read-only-frozen', result
        outputs.append({'checker': name, 'checker_sha256': digest, 'result': result})
finally:
    Path.read_bytes, Path.read_text, Path.stat = read_bytes, read_text, stat
    sys.argv = old_argv
assert before == {str(p): sha(p) for p in watched}, 'Concurrent or checker mutation; no stable pass'
print(json.dumps({'status': 'pass', 'scope': 'Historical R1 structural/citation/audit replay only',
                  'historical_snapshots': descriptors, 'checker_results': outputs,
                  'watched_files_unchanged': len(before),
                  'resolver_selfchecks': ['exact approved path', 'prefix lookalike unchanged', 'unrelated path unchanged'],
                  'checker_sha256': sha(Path(__file__)), 'writes': False,
                  'current_owner_or_semantic_or_compatibility_approval': False,
                  'original_runtime_network_hardware_candidate_execution': False}, indent=2))
