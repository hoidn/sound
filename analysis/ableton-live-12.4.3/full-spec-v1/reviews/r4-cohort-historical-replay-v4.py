"""Read-only finite historical replay after reviewed Media/Recording case refinements.

V4 preserves V1/V2/V3 and adds only the two exact Warp R1 canonical reads. Only inspected analyst validators/parsers run.

Only fourteen known historical wiki reads resolve to exact pinned snapshots.
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
# These two case-only successors preserve the exact earlier canonical bytes.
for packet, new_seal, old_seal, suffix in [
    ('media-file-workflows', 'ce0d45e76d34facbe0e792efaaee0556a717c8932a0677371caf3176b1fe5909',
     '3f6a1d3c3265181023a55aaca5badd80ce45504320e285d1e87dacf2bf418843', 'r4'),
    ('recording', 'de5050c0b0f53240cb0e19c6f1ea9d4c8729a68790dce2d632da6ed9a05a6264',
     '0b1dd1222cfded8bdddad25a367eb7822c743a6bd783f8f183458cb9a97656c1', 'r3'),
]:
    manifest = B / packet / ('manifest-author-' + suffix + '.json')
    prior = B / packet / 'manifest.json'
    assert sha(manifest) == new_seal and sha(prior) == old_seal
    data, previous = load(manifest), load(prior)
    watched.update([manifest, prior])
    for domain, kind in [('specs', 'spec'), ('research', 'research')]:
        slug = 'media-file-workflows' if packet == 'media-file-workflows' else 'recording-comping'
        current = R / 'wiki' / domain / (slug + '.md')
        old = manifest.parent / (kind + '-before-' + suffix + '.md')
        pin = data['files'][old.name]
        assert len(read_bytes(old)) == pin['bytes'] and sha(old) == pin['sha256']
        canonical = str(current.relative_to(R))
        if packet == 'recording':
            assert previous['canonical_documents'][canonical] == pin['sha256']
        else:
            previous_pin = next(row for row in previous['payloads'] if row['path'] == canonical)
            assert {k: previous_pin[k] for k in ['bytes', 'sha256']} == pin
        assert current not in redirects
        redirects[current] = old
        descriptors.append({'canonical_route': canonical,
                            'historical_snapshot': str(old.relative_to(R)), **pin})
        watched.update([current, old])
# Warp R2 is a provider transition only; preserve the exact R1 dependency bytes.
warp_old_seal = B / 'warping-workflows/manifest-author-r1.json'
warp_new_seal = B / 'warping-workflows/manifest-author-r2.json'
assert sha(warp_old_seal) == 'b17efb2eb29b165239bab421e53e49f69117e69fa80f97927ad0e54dac76ba68'
assert sha(warp_new_seal) == 'bc98964e2a6fbb0661ba6e1892a477039f7db76f8706a901a4a0b9352ff896bd'
warp_old, warp_new = load(warp_old_seal), load(warp_new_seal)
warp_watched = {warp_old_seal, warp_new_seal}
for name, provider_pin in warp_old['files'].items():
    provider = warp_old_seal.parent / name
    assert len(read_bytes(provider)) == provider_pin['bytes'] and sha(provider) == provider_pin['sha256']
    assert warp_new['files'][name] == provider_pin
    warp_watched.add(provider)
for provider_pin in warp_new['canonical_snapshots']:
    provider = warp_new_seal.parent / provider_pin['snapshot']
    current = R / provider_pin['canonical']
    assert len(read_bytes(provider)) == len(read_bytes(current)) == provider_pin['bytes']
    assert sha(provider) == sha(current) == provider_pin['sha256']
    warp_watched.update([provider, current])
warp_spec = R / 'wiki/specs/warping-workflows.md'
warp_spec_snapshot = B / 'warping-workflows/spec-r1.md'
warp_spec_pin = warp_old['files']['spec-r1.md']
assert warp_spec_pin == {'bytes': 47351, 'sha256': '68fdbf97e822819a83627bb06233bce4dbd77d2ed83d74aeb972d6a543352249'}
watched.update(warp_watched)
for snapshot_name, domain in [('spec-r1.md', 'specs'), ('research-r1.md', 'research')]:
    current = R / 'wiki' / domain / 'warping-workflows.md'
    old = warp_old_seal.parent / snapshot_name
    pin = warp_old['files'][snapshot_name]
    assert current not in redirects
    redirects[current] = old
    descriptors.append({'canonical_route': str(current.relative_to(R)),
                        'historical_snapshot': str(old.relative_to(R)), **pin})
assert len(redirects) == 14


def historical_path(path):
    # Fixed absolute paths only. No alias, prefix, arbitrary hash or new owner resolver.
    return redirects.get(path, path)


sample = R / 'wiki/specs/stem-separation.md'
assert historical_path(sample) == B / 'stem-separation/spec-r1.md'
assert historical_path(R / 'wiki/specs/stem-separation-extra.md') == R / 'wiki/specs/stem-separation-extra.md'
assert historical_path(R / 'wiki/specs/unrelated.md') == R / 'wiki/specs/unrelated.md'
for current, old in redirects.items():
    assert historical_path(current) == old
    for lookalike in [current.relative_to(R), current.with_name(current.name[0].upper() + current.name[1:]),
                      current.with_name(current.stem + '-extra.md')]:
        assert historical_path(lookalike) == lookalike

checks = [
    ('inventory-revisions/r4-citation-crosswalk/derive.py', '1093f1ee1da0d3576479dc2c87fe18f3e4db488b54510378a6f5cd4c1555a372'),
    ('stem-separation-source-audit/derive.py', 'eb569370a062d740943b415601576dcf9a4ce34596c7b1c75fe89e241839ec6c'),
    ('video-source-audit/derive.py', '1ec6a25fe6c5fd5c1eb58650bc03aa0d46d38f178136493fd8450874d5fc4720'),
    ('synchronization-source-audit/validate-r2.py', '5a81abfd103996cdba30900a5e02c90322a0b3133be8be0574d3ffee3755ab07'),
    ('inventory-revisions/r6-citation-crosswalk/derive.py', '62b8a9324f48e3059b0b9d0c2462d9979db30af1e7ab1c65c17674f1ac4af1af'),
    ('browser-content/validate.py', '5c626a9bd68ad54cc75789c9ff7d58aa25d00e97062d02bb3bf3f3003a44e7db'),
    ('delivery-recovery/validate.py', 'be6ffd3c398c223efbd3d09889f183d63487a9f228757b5f891ef8bef1424e31'),
    ('live-api-clip-sample/validate.py', '66b1cf360585d63a562ae5e7bc597a1a9333f784ce53c6830410ff40ea830429'),
]
input_names = {
    'inventory-revisions/r4-citation-crosswalk/derive.py': 'inputs.json',
    'inventory-revisions/r6-citation-crosswalk/derive.py': 'inputs.json',
    'synchronization-source-audit/validate-r2.py': 'inputs.json',
    'stem-separation-source-audit/derive.py': 'input-pins.json',
    'video-source-audit/derive.py': 'input-pins.json',
    'browser-content/validate.py': 'owner-pins.json',
    'delivery-recovery/validate.py': 'authority-pins.json',
    'live-api-clip-sample/validate.py': 'external-pins.json',
}
# Explicit nested analyst entrypoints; vendor source text remains inert data.
for name, digest in [
    ('live-api-clip-sample/author.py', 'ced309f36bed7a386681c15c117483d1da96ff065a07e94a3456013fe55285b2'),
    ('max-api/derive_inventory.py', 'ddf46be4d3fc1fe793ebfdd3e3945690ee13baa6d8cf2e82c45dea3eb1faac54'),
    ('delivery-recovery/source_parser.py', '5329b6f9612e533cd5e3b2849259f3444a2b49fbb4b35aa448a300fea08d8f2c'),
    ('session-workflows/capture.py', '981e07b15aea93a7bb646f40efdffc45ddb335399100533cf04bbec7bf77715d'),
]:
    assert sha(B / name) == digest
    watched.add(B / name)
for name, digest in checks:
    tool = B / name
    assert sha(tool) == digest
    watched.update(p for p in tool.parent.rglob('*') if p.is_file())
    inputs = load(tool.parent / input_names[name])
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
        sys.argv = [str(B / name)] + (['--check'] if name.endswith('derive.py') else [])
        captured = io.StringIO()
        with redirect_stdout(captured):
            runpy.run_path(str(B / name), run_name='__main__')
        result = json.loads(captured.getvalue())
        if name.startswith('inventory'):
            assert result == load((B / name).parent / 'summary.json')
        else:
            assert result['status'] == ('passed-read-only-frozen' if name.startswith(('stem-', 'video-')) else 'pass'), result
        outputs.append({'checker': name, 'checker_sha256': digest, 'result': result})
finally:
    Path.read_bytes, Path.read_text, Path.stat = read_bytes, read_text, stat
    sys.argv = old_argv
assert before == {str(p): sha(p) for p in watched}, 'Concurrent or checker mutation; no stable pass'
print(json.dumps({'status': 'pass', 'scope': 'Finite historical structural/citation/audit replay only; eight known consumers',
                  'historical_snapshots': descriptors, 'checker_results': outputs,
                  'watched_files_unchanged': len(before),
                  'resolver_selfchecks': ['all 14 exact approved paths', 'all 14 relative, case and prefix lookalikes unchanged', 'unrelated path unchanged'],
                  'checker_sha256': sha(Path(__file__)), 'writes': False,
                  'current_owner_or_semantic_or_compatibility_approval': False,
                  'original_runtime_network_hardware_candidate_execution': False}, indent=2))
