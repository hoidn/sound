#!/usr/bin/env python3
"""Analyst-only storage probe: materialize a complete R2 chunk corpus in the export_native_corpus.py
per-function layout (functions/<entry>/<revision>/{metadata.json,pseudocode.c,manifest.json}) and
measure apparent bytes, allocated bytes and file counts for both layouts. Metadata mirrors
metadata_for() field names with placeholder identities; this measures storage shape only and is
not an ingestible corpus. Usage: layout_probe.py CORPUS SCRATCH_OUTPUT"""
import hashlib, json, os, sys
from pathlib import Path

def encoded(value):  # export_native_corpus.encoded
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + '\n').encode()

def usage(root):
    files = dirs = apparent = allocated = 0
    for base, dirnames, filenames in os.walk(root):
        dirs += len(dirnames)
        allocated += os.lstat(base).st_blocks * 512
        for name in filenames:
            st = os.lstat(os.path.join(base, name))
            files += 1; apparent += st.st_size; allocated += st.st_blocks * 512
    return {'files': files, 'directories': dirs, 'apparent_bytes': apparent, 'allocated_bytes': allocated}

corpus, out = Path(sys.argv[1]), Path(sys.argv[2])
out.mkdir()
functions = 0
for chunk in sorted((corpus / 'chunks').glob('chunk-*.jsonl')):
    for line in chunk.read_bytes().splitlines():
        r = json.loads(line); functions += 1
        code = r.pop('code')
        revision = 'ev_' + '0' * 64 + '-0'
        meta = {'address': r['entry'], 'revision': revision, 'evidence_id': 'ev_' + '0' * 64,
                'source_sha256': '0' * 64, 'source_record_index': 0, 'source_item_index': functions,
                'state': r['state'], 'warnings': r['warnings'], 'limitations': [],
                'partial_pseudocode': r['partial_code'], 'error': r['error'] and {'message': r['error']},
                'details': {'procedure': {k: r[k] for k in ('name', 'thunk', 'body_bytes', 'body_ranges', 'signature')}},
                'analysis_profile': {'digest': '0' * 64}}
        d = out / 'functions' / r['entry'] / revision; d.mkdir(parents=True)
        payload = {'metadata.json': encoded(meta)}
        if code: payload['pseudocode.c'] = code.encode()
        for name, data in payload.items(): (d / name).write_bytes(data)
        (d / 'manifest.json').write_bytes(encoded({n: hashlib.sha256(b).hexdigest() for n, b in payload.items()}))
result = {'functions': functions, 'per_function_layout': usage(out / 'functions'), 'chunk_layout': usage(corpus),
          'block_size': os.statvfs(out).f_bsize}
print(json.dumps(result, indent=2))
