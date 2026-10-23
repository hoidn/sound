#!/usr/bin/env python3
"""Materialize only the 48 Root-selected raw export ranges, once."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def pinned(path, size, digest):
    data = path.read_bytes()
    assert len(data) == size and hashlib.sha256(data).hexdigest() == digest
    return data


def main():
    selection = json.loads(pinned(HERE / 'selection-source-read.json', 2421,
        'd2961dd9fe36ca26f28bb25d96fd5b5f09494710682576ef3de939b50b9dd5d1'))
    census = json.loads(pinned(HERE / 'candidate-census.json', 79348,
        '6c7964af415066f9cee129a1bd4eea95d3fcf6db57904ab51251cf7d207d055f'))
    assert selection['entries'] == [row['entry'] for row in census['records']]
    assert len(selection['entries']) == 48
    output = HERE / 'selected-records.jsonl'
    receipt_path = HERE / 'source-retention-receipt.json'
    assert not output.exists() and not receipt_path.exists()
    receipts = []
    total = 0
    # No full chunk replay: custody hashes are inherited from the selected
    # metadata census; each new read is one exact selected raw record range.
    with output.open('xb') as stream:
        for row in census['records']:
            with Path(row['source_path']).open('rb', buffering=0) as source:
                source.seek(row['source_byte'])
                raw = source.read(row['raw_bytes'])
            assert len(raw) == row['raw_bytes']
            assert hashlib.sha256(raw).hexdigest() == row['raw_sha256']
            record = json.loads(raw)
            assert record['entry'] == row['entry']
            code = (record.get('code') or '').encode('utf-8')
            assert len(code) == row['code_utf8_bytes']
            assert hashlib.sha256(code).hexdigest() == row['code_sha256']
            assert len(code.decode().splitlines()) == row['C_lines']
            stream.write(raw)
            receipts.append(dict(entry=row['entry'], retained_byte=total,
                raw_bytes=len(raw), raw_sha256=row['raw_sha256'],
                original_path=row['source_path'], original_line=row['source_line'],
                original_byte=row['source_byte']))
            total += len(raw)
    retained = output.read_bytes()
    receipt = dict(schema='fixed48-selected-source-retention-v1', records=receipts,
        raw_range_reads=48, raw_content_bytes=total,
        retained=dict(path=output.name, bytes=len(retained),
                      sha256=hashlib.sha256(retained).hexdigest()),
        code_utf8_bytes=296613, C_lines=8116,
        custody='Three whole chunk hashes inherited from the immediately preceding metadata census. Fresh acquisition read each selected raw range once and checked its exact retained SHA; no new full chunk/index scan.',
        semantic_reading='Materialized now; full source reading and anchored assessment follow separately.',
        expansion=False, required_unsupported='U', coverage_gate='OPEN')
    with receipt_path.open('x') as stream:
        json.dump(receipt, stream, indent=2)
        stream.write('\n')
    print(json.dumps({k: receipt[k] for k in ('raw_range_reads', 'raw_content_bytes',
                                            'code_utf8_bytes', 'C_lines')}))


if __name__ == '__main__':
    main()
