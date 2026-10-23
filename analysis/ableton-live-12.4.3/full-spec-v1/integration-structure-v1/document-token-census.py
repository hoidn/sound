"""One exact retained-C text needle; metadata nominations, never a handler/xref proof."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent / 'component-resolution-v1'
NEEDLE = '0x72746f64'

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

if __name__ == '__main__':
    parent_raw = (PARENT / 'manifest.json').read_bytes()
    assert sha(parent_raw) == '392a738005f7d776dca96d7c78220cb94091081ef7086ec45b9397afccbe438b'
    inputs_raw = (PARENT / 'class-inputs.json').read_bytes()
    pin = next(r for r in json.loads(parent_raw)['files'] if r['path'] == 'class-inputs.json')
    assert (len(inputs_raw), sha(inputs_raw)) == (pin['bytes'], pin['sha256'])
    population = json.loads(inputs_raw)['decomp_chunk_pins']
    assert len(population) == 4185
    assert '0x72746f64' in 'case 0x72746f64:'
    assert '0x72746f64' not in 'case 191???decimal:'
    matches = []
    record_count = occurrences = 0
    for item in population:
        path = Path(item['path'])
        before = path.stat()
        h = hashlib.sha256()
        off = 0
        with path.open('rb') as f:
            for line, raw in enumerate(f, 1):
                h.update(raw)
                r = json.loads(raw)
                code = r.get('code') or ''
                n = code.count(NEEDLE)
                if n:
                    matches.append((str(path), line, off, len(raw), sha(raw)))
                    occurrences += n
                off += len(raw)
                record_count += 1
        assert (off, h.hexdigest()) == (item['bytes'], item['sha256'])
        after = path.stat()
        assert (before.st_size, before.st_mtime_ns, before.st_ino) == (after.st_size, after.st_mtime_ns, after.st_ino)
    metadata = []
    if len(matches) <= 20:
        for path, line, off, size, rawsha in matches:
            with Path(path).open('rb') as f:
                f.seek(off)
                raw = f.read(size)
            assert sha(raw) == rawsha
            r = json.loads(raw)
            assert sha(r['code'].encode()) == r['code_sha256']
            metadata.append({'source_file': path, 'line': line, 'byte': off, 'raw_bytes_including_LF': size, 'raw_sha256_including_LF': rawsha, 'metadata': {k: v for k, v in r.items() if k != 'code'}})
    result = {'needle': NEEDLE, 'predicate': 'literal case-sensitive substring in decoded code field; not native xref/caller/handler proof', 'population_manifest': {'path': str(PARENT / 'class-inputs.json'), 'sha256': sha(inputs_raw), 'chunk_count': len(population)}, 'all_chunk_hash_size_and_stat_checks': 'PASS', 'records_mechanically_scanned': record_count, 'matching_record_count': len(matches), 'substring_occurrences': occurrences, 'metadata_cap': 20, 'metadata': metadata, 'status': 'ALL_MATCH_METADATA' if len(matches) <= 20 else 'STOP_OVERCAP_NO_METADATA', 'limits': ['Code text may include comments, declarations or inlining; exact spelling misses decimal, alternate syntax or indirect routing.', 'No body was semantically read by this census and no callgraph, receiver, invocation or absence claim follows.'], 'method_sha256': sha(Path(__file__).read_bytes())}
    with (HERE / 'document-render-token-census.json').open('x') as f:
        json.dump(result, f, indent=2)
        f.write('\n')
    print(json.dumps({'status': result['status'], 'matching_records': len(matches), 'occurrences': occurrences, 'records_scanned': record_count, 'metadata': metadata}, indent=2))
