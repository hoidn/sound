"""Retain the separately selected67 exact raw ranges once, without chunk/index replay."""
from pathlib import Path
import hashlib
import json

P=Path(__file__).resolve().parent


def sha(b):
    return hashlib.sha256(b).hexdigest()


def main():
    sr=(P/'selection-source-read.json').read_bytes()
    assert (len(sr),sha(sr))==(3582,'4994ea2c0ff9281d75280b173507b17650747a08914aea7133048b5e0e3d432c')
    cb=(P/'candidate-census.json').read_bytes()
    assert (len(cb),sha(cb))==(125476,'a8d46906206e5be905d34866467be349734102bc28b1410ffff28ccccf02dfc5')
    s,c=json.loads(sr),json.loads(cb)
    assert s['entries']==[x['entry'] for x in c['records']] and len(s['entries'])==67
    assert not (P/'selected-records.jsonl').exists() and not (P/'source-retention-receipt.json').exists()
    raws=[];receipts=[];offset=0
    for x in c['records']:
        with Path(x['source_path']).open('rb') as f:
            f.seek(x['source_byte']);raw=f.read(x['raw_bytes'])
        assert len(raw)==x['raw_bytes'] and sha(raw)==x['raw_sha256']
        d=json.loads(raw);assert d['entry']==x['entry']
        code=(d.get('code') or '').encode()
        assert len(code)==x['code_utf8_bytes'] and sha(code)==x['code_sha256'] and len(code.decode().splitlines())==x['C_lines']
        assert d['warnings']==x['warnings'] and d['body_bytes']==x['body_bytes'] and d['body_ranges']==x['body_ranges']
        raws.append(raw);receipts.append(dict(entry=x['entry'],retained_byte=offset,raw_bytes=len(raw),raw_sha256=sha(raw),original_path=x['source_path'],original_line=x['source_line'],original_byte=x['source_byte']))
        offset+=len(raw)
    payload=b''.join(raws)
    with (P/'selected-records.jsonl').open('xb') as f:f.write(payload)
    receipt=dict(schema='fixed67-source-retention-v1',records=receipts,raw_range_reads=67,raw_content_bytes=len(payload),retained_sha256=sha(payload),C_utf8_bytes=29288,C_lines=1231,source_selection_sha256=sha(sr),chunk_custody='23chunks/4,030,080B inherited census custody; no fresh chunk hash or alias/index pass',semantic_reading='retained now; complete source read follows',source_expansion=False,original_calls=0)
    with (P/'source-retention-receipt.json').open('x') as f:json.dump(receipt,f,indent=2);f.write('\n')
    print(json.dumps(dict(raw_records=67,raw_bytes=len(payload),raw_sha256=sha(payload),C_utf8_bytes=29288,C_lines=1231)))


if __name__=='__main__':
    main()
