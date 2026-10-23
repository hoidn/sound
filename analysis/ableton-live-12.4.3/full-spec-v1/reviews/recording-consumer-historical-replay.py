"""Replay four current partial owners with their one exact pre-R3 Recording read.

This preserves the old Recording dependency, not a new semantic review. Other
canonical reads stay current, including Stem R2; the R1 cohort tool is separate.
"""
from pathlib import Path
from contextlib import redirect_stdout
import hashlib
import io
import json
import runpy
import sys

assert sys.dont_write_bytecode and sys.argv[1:] == ['--check']
R = Path(__file__).resolve().parents[4]
B = R / 'analysis/ableton-live-12.4.3/full-spec-v1'
read_bytes, read_text, stat = Path.read_bytes, Path.read_text, Path.stat
sha = lambda p: hashlib.sha256(read_bytes(p)).hexdigest()
load = lambda p: json.loads(read_text(p))
canonical = R / 'wiki/specs/recording-comping.md'
snapshot = B / 'recording/spec-before-r3.md'
old_seal = B / 'recording/manifest.json'
new_seal = B / 'recording/manifest-author-r3.json'
assert sha(old_seal) == '0b1dd1222cfded8bdddad25a367eb7822c743a6bd783f8f183458cb9a97656c1'
assert sha(new_seal) == 'de5050c0b0f53240cb0e19c6f1ea9d4c8729a68790dce2d632da6ed9a05a6264'
pin = load(new_seal)['files'][snapshot.name]
assert sha(snapshot) == pin['sha256'] == load(old_seal)['canonical_documents'][str(canonical.relative_to(R))]
assert len(read_bytes(snapshot)) == pin['bytes']


def historical(path):
    return snapshot if path == canonical else path


assert historical(canonical) == snapshot
for path in [Path('wiki/specs/recording-comping.md'), R / 'wiki/specs/Recording-comping.md',
             R / 'wiki/specs/recording-comping-extra.md', R / 'wiki/specs/stem-separation.md']:
    assert historical(path) == path
checks = [
    ('stem-separation/validate-r2.py', 'a117e881bee80acf455d8ae3eaa93c087009e1e36acff15875b5bd73966e9d24', 'inputs-r2.json', ['--check']),
    ('engine-resources/validate.py', '88da57d1a11f60ef1ad3d7c6426398cfc431cffce1b3b0a67c16d11892b829cd', 'existing-authority-pins.json', []),
    ('mixing-workflows/validate.py', 'd61f0f97aacf6988b048d41d579f9545731e54f27af500ec4f0b3ef04fd65c84', 'input-owner-pins.json', []),
    ('live-api-core-session/validate-author-r2.py', '2619221fb6a73b06c99bdc3d8e879bb07e590a7183080a10680fb17cc838e7ee', 'owner-pins.json', []),
]
watched = {canonical, snapshot, old_seal, new_seal, Path(__file__)}
for name, digest in [
    ('live-api-core-session/validate.py', 'cc10e668c4b09014e69dfffd132a872f8d8a8529b5d38449e41c5948c94875d3'),
    ('routing-monitoring/capture.py', 'b50736f8342a05c778a42a83d92fe493c255b694dedd70e3e5d59dfe4827936b'),
    ('mixing-workflows/author.py', '384852fafa46422118ec93efa382de3e08da09b2e9392468e0ceab79575527f9'),
    ('session-workflows/capture.py', '981e07b15aea93a7bb646f40efdffc45ddb335399100533cf04bbec7bf77715d'),
    ('max-api/derive_inventory.py', 'ddf46be4d3fc1fe793ebfdd3e3945690ee13baa6d8cf2e82c45dea3eb1faac54'),
]:
    assert sha(B / name) == digest
    watched.add(B / name)
for name, digest, inputs, args in checks:
    tool = B / name
    assert sha(tool) == digest
    watched.update(p for p in tool.parent.rglob('*') if p.is_file())
    rows = load(tool.parent / inputs)
    recording = [p for p in rows if p['path'] == str(canonical.relative_to(R))]
    assert len(recording) == 1 and {k: recording[0][k] for k in ['bytes', 'sha256']} == pin
    for p in rows:
        actual = historical(R / p['path'])
        assert sha(actual) == p['sha256'] and len(read_bytes(actual)) == p['bytes'], p['path']
        watched.add(actual)
before = {str(p): sha(p) for p in watched}
argv, search_path = sys.argv[:], sys.path[:]
results = []
try:
    Path.read_bytes = lambda p: read_bytes(historical(p))
    Path.read_text = lambda p, *a, **kw: read_text(historical(p), *a, **kw)
    Path.stat = lambda p, *a, **kw: stat(historical(p), *a, **kw)
    for name, digest, inputs, args in checks:
        sys.argv = [str(B / name)] + args
        output = io.StringIO()
        with redirect_stdout(output):
            runpy.run_path(str(B / name), run_name='__main__')
        result = json.loads(output.getvalue())
        assert result['status'] == ('passed-read-only-frozen' if name.startswith('stem-') else 'pass')
        assert result['writes'] is False
        results.append({'checker': name, 'checker_sha256': digest, 'result': result})
finally:
    Path.read_bytes, Path.read_text, Path.stat = read_bytes, read_text, stat
    sys.argv, sys.path = argv, search_path
assert before == {str(p): sha(p) for p in watched}, 'Mutation or concurrent change; no stable pass'
print(json.dumps({'status': 'pass', 'scope': 'Four current partial-owner integrity replays with one historical Recording dependency',
                  'historical_snapshot': {'canonical_route': str(canonical.relative_to(R)),
                                          'historical_snapshot': str(snapshot.relative_to(R)), **pin},
                  'checker_results': results, 'watched_files_unchanged': len(before),
                  'resolver_selfchecks': ['exact path', 'relative, case and prefix lookalikes unchanged', 'current Stem untouched'],
                  'checker_sha256': sha(Path(__file__)), 'writes': False,
                  'new_semantic_or_compatibility_approval': False,
                  'original_runtime_network_hardware_candidate_execution': False}, indent=2))
