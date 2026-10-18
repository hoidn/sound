"""N6: write manifest.json (SHA-256 of every file in this directory; pinned inputs, tools and commands).

usage: python3 -I make_manifest.py <evidence dir> <app bundle> <Live.arm64>
"""
import hashlib, json, os, platform, sys


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


ev, app, live = sys.argv[1:4]
root = os.path.abspath(os.path.join(ev, '../../../..'))  # repository root
files = {}
for d, _, fs in os.walk(ev):
    if '__pycache__' in d:
        continue
    for f in fs:
        p = os.path.join(d, f)
        rel = os.path.relpath(p, ev)
        if rel != 'manifest.json':
            files[rel] = {'bytes': os.path.getsize(p), 'sha256': sha(p)}
repo = lambda rel: {rel: sha(os.path.join(root, rel))}
inputs = {}
for rel in ['analysis/ableton-live-12.4.3/r2/h4-devices-v1/out/param_table.tsv',
            'analysis/ableton-live-12.4.3/r2/h4-devices-v1/out/param_tables.json',
            'analysis/ableton-live-12.4.3/r2/h4-devices-v1/out/inputs.jsonl',
            'analysis/ableton-live-12.4.3/r2/h4-devices-v1/out/occurrences.jsonl']:
    inputs.update(repo(rel))
inputs['analysis/ableton-live-12.4.3/derived/Live.arm64'] = sha(live)
for p in ['/var/tmp/sound-analysis/corpus/decomp/run.json', '/var/tmp/sound-analysis/corpus/indexes/manifest.json']:
    inputs[p] = sha(p)
inputs['Contents/Info.plist (read-only app bundle)'] = sha(os.path.join(app, 'Contents/Info.plist'))
tools = {}
for rel in ['analysis/ableton-live-12.4.3/r2/n1-transport-state-v1/corpus_lookup.py',
            'analysis/ableton-live-12.4.3/r2/n1-transport-state-v1/check_number_format.py',
            'analysis/ableton-live-12.4.3/r2/n5-device-mapping-v1/conversions.py',
            'tools/ghidra/R2FunctionDossier.java']:
    tools.update(repo(rel))
manifest = {
    'packet': 'N6 device tables v1', 'created': '2026-10-17', 'static_only': True,
    'environment': {'python': platform.python_version(), 'invocation': 'python3 -I, cwd = this directory, N1_CACHE = session scratch file'},
    'commands': [
        'python3 -I extract_nested.py out ../h4-devices-v1/out ../../derived/Live.arm64',
        'python3 -I constructors.py out ../h4-devices-v1/out ../../derived/Live.arm64 results',
        'python3 -I conversions_nested.py out ../h4-devices-v1/out',
        'python3 -I asm_order_check.py out results',
        'python3 -I loader_slots.py out ../../derived/Live.arm64',
        'python3 -I number_text_check.py out ../h4-devices-v1/out "<app>/Contents/App-Resources"',
        'python3 -I spec_tables.py out ../h4-devices-v1/out',
        'python3 -I ../n1-transport-state-v1/corpus_lookup.py excerpt out/live_corpus_excerpts.jsonl <71 entries in notes.md>',
        'python3 -I make_manifest.py . "<app>" ../../derived/Live.arm64',
    ],
    'query_server_requests': ['n6-0001', 'n6-0002', 'n6-0003'],
    'inputs_sha256': inputs, 'tools_sha256': tools, 'files': dict(sorted(files.items())),
}
json.dump(manifest, open(os.path.join(ev, 'manifest.json'), 'w'), indent=1)
print(len(files), 'files')
