"""One selected exact122-range retention; no alias/chunk hash replay or source follow."""
from pathlib import Path
import datetime
import hashlib
import json

P = Path(__file__).resolve().parent


def sha(b):
    return hashlib.sha256(b).hexdigest()


def main():
    assert not (P / 'selected-records.jsonl').exists()
    assert not (P / 'source-retention-receipt.json').exists()
    sr = (P / 'selection-source-read.json').read_bytes()
    assert (len(sr), sha(sr)) == (4802, '47a667a169e41814599378859b2574adc224763e68b02602b9b7be0637bfd3f9')
    cb = (P / 'candidate-census.json').read_bytes()
    assert (len(cb), sha(cb)) == (287764, '1f430f3aed445c6de42bc3ffcc495ba3248ae75e2c186d71021fa9fdc7dd31ad')
    selection, census = json.loads(sr), json.loads(cb)
    assert selection['entries'] == [r['entry'] for r in census['records']] and len(selection['entries']) == 122
    receipt, offset, digest = [], 0, hashlib.sha256()
    with (P / 'selected-records.jsonl').open('xb') as retained:
        for meta in census['records']:
            with Path(meta['source_path']).open('rb') as original:
                original.seek(meta['source_byte'])
                raw = original.read(meta['raw_bytes'])
            assert len(raw) == meta['raw_bytes'] and sha(raw) == meta['raw_sha256']
            row = json.loads(raw)
            assert row['entry'] == meta['entry']
            code = row['code'].encode()
            assert len(code) == meta['code_utf8_bytes'] and sha(code) == meta['code_sha256']
            assert len(row['code'].splitlines()) == meta['C_lines']
            for key in ['warnings', 'body_bytes', 'body_ranges', 'thunk', 'state', 'error', 'partial_code', 'timed_out']:
                assert row[key] == meta[key]
            retained.write(raw)
            retained.flush()
            digest.update(raw)
            receipt.append(dict(entry=meta['entry'], retained_byte=offset, raw_bytes=len(raw), raw_sha256=sha(raw),
                original_path=meta['source_path'], original_line=meta['source_line'], original_byte=meta['source_byte']))
            offset += len(raw)
    result = dict(schema='fixed122-source-retention-v1', utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        records=receipt, raw_range_reads=122, raw_content_bytes=offset, retained_sha256=digest.hexdigest(),
        C_utf8_bytes=360530, C_lines=9041, source_selection_sha256=sha(sr),
        chunk_custody='12chunks/2412471B inherited metadata custody; no second hash or alias/index pass',
        semantic_reading='retained now; complete direct/lossless source read follows', source_expansion=False, original_calls=0)
    with (P / 'source-retention-receipt.json').open('x') as f:
        json.dump(result, f, indent=2)
        f.write('\n')
    print(json.dumps(dict(raw_records=122, raw_bytes=offset, raw_sha256=digest.hexdigest(), C_utf8_bytes=360530, C_lines=9041)))


if __name__ == '__main__':
    main()
