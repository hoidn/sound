"""One gated exact208-range retention; no alias/index/chunk-scan/hash replay.

A mismatch aborts without retry or truncation. Historical reader not imported.
"""
from pathlib import Path
import datetime
import hashlib
import json
import sys

P=Path(__file__).resolve().parent

def sha(b):
    return hashlib.sha256(b).hexdigest()

def main():
    assert sys.argv[1:]==['--retain']
    assert not (P/'selected-records.jsonl').exists() and not (P/'source-retention-receipt.json').exists()
    sr=(P/'selection-source-read.json').read_bytes()
    assert (len(sr),sha(sr))==(4571,'f69ed8f8ac6d6fd5c5b851f76acef4c3d27242da19e7c46315447a66eb7bdf02')
    gate=json.loads(sr)
    for q in gate['metadata8']:
        b=Path(q['path']).read_bytes()
        assert (len(b),sha(b))==(q['bytes'],q['sha256'])
    cb=(P/'candidate-census.json').read_bytes()
    assert (len(cb),sha(cb))==(481191,'11ada505c395ef6b94258981210bde4f116ce2c9c10843f11e7ad517f6eb9c8c')
    census=json.loads(cb);rows=census['records']
    assert len(rows)==len(set(r['entry'] for r in rows))==208
    assert gate['caps']==dict(records=208,C_bytes=2097152,C_lines=50000)
    assert sum(r['code_utf8_bytes'] for r in rows)==666796<=2097152
    assert sum(r['C_lines'] for r in rows)==15298<=50000
    receipt=[];offset=0;digest=hashlib.sha256()
    with (P/'selected-records.jsonl').open('xb') as retained:
        for meta in rows:
            with Path(meta['source_path']).open('rb') as original:
                original.seek(meta['source_byte']);raw=original.read(meta['raw_bytes'])
            assert len(raw)==meta['raw_bytes'] and sha(raw)==meta['raw_sha256']
            row=json.loads(raw)
            assert row['entry']==meta['entry'] and row.get('name')==meta['export_record_name']
            assert row.get('signature')==meta['signature']
            code=row['code'].encode('utf-8')
            assert (len(code),sha(code),len(row['code'].splitlines()))==(meta['code_utf8_bytes'],meta['code_sha256'],meta['C_lines'])
            for key in ['warnings','body_bytes','body_ranges','thunk','state','error','partial_code','timed_out']:
                assert row.get(key)==meta[key]
            retained.write(raw);retained.flush();digest.update(raw)
            receipt.append(dict(entry=meta['entry'],retained_byte=offset,raw_bytes=len(raw),raw_sha256=sha(raw),original_path=meta['source_path'],original_line=meta['source_line'],original_byte=meta['source_byte']))
            offset+=len(raw)
    result=dict(schema='fixed208-source-retention-v1',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),records=receipt,raw_range_reads=208,raw_content_bytes=offset,retained_sha256=digest.hexdigest(),C_utf8_bytes=666796,C_lines=15298,source_selection_sha256=sha(sr),chunk_custody='13chunks/3303905B inherited metadata custody; no second hash/scan or alias/index pass',semantic_reading='Retained now; complete direct/lossless source read follows',source_expansion=False,original_calls=0)
    with (P/'source-retention-receipt.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    for name in ['selected-records.jsonl','source-retention-receipt.json']:(P/name).chmod(0o444)
    print(json.dumps({k:result[k] for k in ['raw_range_reads','raw_content_bytes','retained_sha256','C_utf8_bytes','C_lines']}))

if __name__=='__main__':main()
